"""db/run_engine.py on Modal CPU (DECISIONS D86, D92): the engine over the procedures, in parallel containers.

    <modal venv>/bin/modal run db/modal_engine.py --cmd report [--limit N] [--window DAYS ...]
    <modal venv>/bin/modal run db/modal_engine.py --cmd write --window DAYS
    <modal venv>/bin/modal deploy db/modal_engine.py        after_load, which db/modal_daily.py calls every day (D92)

The container gets the code and the law, the rules and the log of the repository (no raw bytes, no readings: the
engine reads neither) and the secret ccp-db. The procedure ids are read here, in chunks of CHUNK; each container loads
the store once (run_engine._init) and evaluates the chunks it is given (run_engine._chunk), at most MAX_CONTAINERS at
a time so Supabase's connection pool is not exhausted. write refuses as run_engine does: the window must be the
settled product_rule:janela-inicio-procedimento.

after_load (D92), once the daily ingest is done: the law watch (db/law_watch.py: the CCP on the Diário da República
compared with the repository's text, ntfy on a new difference or a failed read), then a run: incremental (only the
procedures touched since the previous run, every other verdict carried) unless the rules in use changed since that run
(a reading settled, a pending article held or released), then full. The image is built at deploy time with the commit
deployed (CCP_COMMIT): the Mac's runner deploys again after the readers recorded new rules.
"""
import collections
import json
import os
import subprocess
import sys
import time
from pathlib import Path

import modal

ROOT = Path(__file__).resolve().parent.parent
CHUNK, MAX_CONTAINERS = 2000, 12
app = modal.App("ccp-engine-run")


def _commit():
    if os.environ.get("CCP_COMMIT"):
        return os.environ["CCP_COMMIT"]
    return subprocess.run(["git", "rev-parse", "--short=9", "HEAD"], capture_output=True, text=True, cwd=ROOT).stdout.strip() or "0000000"


image = (modal.Image.debian_slim(python_version="3.12").apt_install("chromium")
         .pip_install("psycopg[binary]==3.2.4", "jsonschema==4.25.1")
         .env({"CCP_CHROME": "/usr/bin/chromium", "CCP_COMMIT": _commit()}))
for d, ignore in (("engine", []), ("db", []), ("tools", []), ("schemas", []), ("rules", []),
                  ("law", ["raw_bytes/**"]), ("governance", ["readings/**"])):
    image = image.add_local_dir(ROOT / d, f"/root/ccp/{d}", ignore=["**/__pycache__", "**/*.pyc", "**/.env*", *ignore])
image = image.add_local_file(ROOT / "verify.py", "/root/ccp/verify.py")  # tools/serve.py reads the store through verify's readers
SECRETS = [modal.Secret.from_name("ccp-db")]


@app.cls(image=image, secrets=SECRETS, cpu=2, memory=6144, timeout=3600, max_containers=MAX_CONTAINERS)
class Engine:
    write: bool = modal.parameter(default=False)
    commit: str = modal.parameter(default="0000000")  # the repository commit the manifests name (the container has no .git)
    corrida: str = modal.parameter(default="")  # D88: the run every verdict written is linked to

    @modal.enter()
    def load(self):
        sys.path[:0] = ["/root/ccp/db", "/root/ccp", "/root/ccp/tools"]  # db first: tools/ has a run_engine.py of its own
        import run_engine
        self.re = run_engine
        run_engine._init(self.write, self.commit, self.corrida or None)

    @modal.method()
    def chunk(self, units: list, windows: list):
        out, written, n = self.re._chunk((units, windows))
        return {str(w): [dict(t), dict(wn), dict(hw)] for w, (t, wn, hw) in out.items()}, dict(written), n


def evaluate(ids, windows, write, commit, corrida):
    """Map the chunks over the Engine containers; (tally, why none, written, done) per window."""
    jobs = [ids[i:i + CHUNK] for i in range(0, len(ids), CHUNK)]
    print(f"{len(ids)} procedures in {len(jobs)} chunks", flush=True)
    tally = {str(w): collections.Counter() for w in windows}
    why_none = {str(w): collections.Counter() for w in windows}
    written, done, t0 = collections.Counter(), 0, time.time()
    if not jobs:
        return tally, why_none, written, 0
    for out, wr, n in Engine(write=write, commit=commit, corrida=corrida).chunk.map(jobs, kwargs={"windows": windows}, order_outputs=False):
        for w, (t, wn, _) in out.items():
            tally[w].update({tuple(json.loads(json.dumps(k))) if isinstance(k, list) else k: v for k, v in t.items()})
            why_none[w].update(wn)
        written.update(wr)
        done += n
        if done % 100000 < CHUNK:
            print(f"... {done}/{len(ids)} in {time.time() - t0:.0f} s", flush=True)
    return tally, why_none, written, done


def summary(t):
    res, per = collections.Counter(), collections.Counter()
    for (rid, r, why), n in t.items():
        res[r] += n
        if r != "nao_avaliado":
            per[(rid, r)] += n
    return dict(res), {f"{a}|{b}": n for (a, b), n in sorted(per.items())}


@app.function(image=image, secrets=SECRETS + [modal.Secret.from_name("ccp-ntfy")], cpu=2, memory=6144, timeout=6 * 3600)
def after_load(full: bool = False, watch: bool = True) -> dict:
    """D92: the law watch, then the day's run (incremental, or full when the rules in use changed)."""
    sys.path[:0] = ["/root/ccp/db", "/root/ccp", "/root/ccp/tools"]
    import law_watch
    import pg
    import run_engine
    import serve
    from engine.governance import Log
    conn = pg.connect()
    report = {"commit": os.environ.get("CCP_COMMIT")}
    if watch:
        report["lei"] = law_watch.check(conn)
    serve.load(("law", "rules", "governance"), commit=os.environ.get("CCP_COMMIT"))
    window = run_engine.settled_window(Log(Path("/root/ccp/governance")))
    pending = run_engine.pending_passages(conn)
    signature = run_engine.rules_signature(run_engine.load_rules(pending))
    prev = conn.execute("select id, at, doc from ccp.corrida order by at desc limit 1").fetchone()
    full = full or prev is None or prev[2].get("regras") != signature or str(prev[2].get("window_days")) != str(window)
    ids = run_engine.all_procedures(conn) if full else run_engine.touched_since(conn, prev[1])
    report.update(modo="completa" if full else "incremental", procedimentos=len(ids))
    if not full and not ids:
        report["corrida"] = None
        print(json.dumps(report, ensure_ascii=False, default=str))
        return report
    corrida = f"corrida:{time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())}"
    tally, why_none, written, done = evaluate(ids, [window], True, os.environ.get("CCP_COMMIT", "0000000"), corrida)
    carried = 0 if full else run_engine.carry(conn, prev[0], corrida, ids)
    res, per = summary(tally[str(window)])
    counts = run_engine.run_counts(conn, corrida)
    total = conn.execute("select count(*) from ccp.unidade_atual where kind = ccp.n('proc')").fetchone()[0]
    doc = {"window_days": window, "commit": os.environ.get("CCP_COMMIT"), "procedures": total, "modo": report["modo"],
           "avaliados": done, "herdados": carried, "base": None if full else prev[0], "regras": signature, "pendentes": pending,
           "by_result": {**counts, "nao_avaliado": res.get("nao_avaliado") if full else None}, "decided_by_rule": per, "written": dict(written)}
    run_engine.close_run(conn, corrida, doc)
    report.update(corrida=corrida, herdados=carried, by_result=counts)
    print(json.dumps(report, ensure_ascii=False, default=str))
    return report


@app.local_entrypoint()
def main(cmd: str = "report", limit: int = 2000000, window: str = "", full: bool = False):
    if cmd == "after-load":
        print(after_load.remote(full))
        return
    sys.path[:0] = [str(ROOT / "db"), str(ROOT), str(ROOT / "tools")]  # db first: tools/ has a run_engine.py of its own
    import pg
    import run_engine
    windows = [int(x) for x in window.split(",") if x != ""] or [None]
    if cmd == "write":
        import serve
        from engine.governance import Log
        serve.load(("law", "rules", "governance"))
        decided = run_engine.settled_window(Log(ROOT / "governance"))
        if decided is None or windows != [decided]:
            raise SystemExit(f"write needs --window {decided if decided is not None else 'N'}: {run_engine.WINDOW_RULE} settled in the log")
    conn = pg.connect()
    conn.execute("set statement_timeout = '900s'")
    ids = run_engine.all_procedures(conn)[:limit]
    commit = _commit()
    corrida = f"corrida:{time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())}" if cmd == "write" else ""
    tally, why_none, written, done = evaluate(ids, windows, cmd == "write", commit, corrida)
    for w in tally:
        res, per = summary(tally[w])
        print(json.dumps({"window_days": w, "procedures": done, "by_result": res, "without_verdicts": dict(why_none[w]), "decided_by_rule": per,
                          **({"written": dict(written)} if cmd == "write" else {})}, ensure_ascii=False, indent=1))
        if cmd == "write":
            serve_rules = run_engine.load_rules(run_engine.pending_passages(conn))
            run_engine.close_run(conn, corrida, {"window_days": w, "commit": commit, "procedures": done, "modo": "completa", "by_result": res,
                                                 "regras": run_engine.rules_signature(serve_rules), "decided_by_rule": per, "written": dict(written)})
            print(f"run {corrida} closed")
