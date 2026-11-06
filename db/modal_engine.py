"""db/run_engine.py on Modal CPU (DECISIONS D86): the engine over every procedure, in parallel containers.

    <modal venv>/bin/modal run db/modal_engine.py --cmd report [--limit N] [--window DAYS ...]
    <modal venv>/bin/modal run db/modal_engine.py --cmd write --window DAYS

The container gets the code and the law, the rules and the log of the repository (no raw bytes, no readings: the
engine reads neither) and the secret ccp-db. The procedure ids are read here, in chunks of CHUNK; each container loads
the store once (run_engine._init) and evaluates the chunks it is given (run_engine._chunk), at most MAX_CONTAINERS at
a time so Supabase's connection pool is not exhausted. write refuses as run_engine does: the window must be the
settled product_rule:janela-inicio-procedimento.
"""
import collections
import json
import sys
import time
from pathlib import Path

import modal

ROOT = Path(__file__).resolve().parent.parent
CHUNK, MAX_CONTAINERS = 2000, 12
app = modal.App("ccp-engine-run")
image = modal.Image.debian_slim(python_version="3.12").pip_install("psycopg[binary]==3.2.4", "jsonschema==4.25.1")
for d, ignore in (("engine", []), ("db", []), ("tools", []), ("schemas", []), ("rules", []),
                  ("law", ["raw_bytes/**"]), ("governance", ["readings/**"])):
    image = image.add_local_dir(ROOT / d, f"/root/ccp/{d}", ignore=["**/__pycache__", "**/*.pyc", "**/.env*", *ignore])
image = image.add_local_file(ROOT / "verify.py", "/root/ccp/verify.py")  # tools/serve.py reads the store through verify's readers


@app.cls(image=image, secrets=[modal.Secret.from_name("ccp-db")], cpu=2, memory=6144, timeout=3600, max_containers=MAX_CONTAINERS)
class Engine:
    write: bool = modal.parameter(default=False)
    commit: str = modal.parameter(default="0000000")  # the repository commit the manifests name (the container has no .git)

    @modal.enter()
    def load(self):
        sys.path[:0] = ["/root/ccp/db", "/root/ccp", "/root/ccp/tools"]  # db first: tools/ has a run_engine.py of its own
        import run_engine
        self.re = run_engine
        run_engine._init(self.write, self.commit)

    @modal.method()
    def chunk(self, units: list, windows: list):
        out, written, n = self.re._chunk((units, windows))
        return {str(w): [dict(t), dict(wn), dict(hw)] for w, (t, wn, hw) in out.items()}, dict(written), n


@app.local_entrypoint()
def main(cmd: str = "report", limit: int = 2000000, window: str = ""):
    sys.path[:0] = [str(ROOT / "db"), str(ROOT), str(ROOT / "tools")]  # db first: tools/ has a run_engine.py of its own
    import pg
    import run_engine
    windows = [int(x) for x in window.split(",") if x != ""] or [None]
    if cmd == "write":
        import serve
        from engine.governance import Log
        serve.load(("governance",))
        decided = run_engine.settled_window(Log(ROOT / "governance"))
        if decided is None or windows != [decided]:
            raise SystemExit(f"write needs --window {decided if decided is not None else 'N'}: {run_engine.WINDOW_RULE} settled in the log")
    conn = pg.connect()
    conn.execute("set statement_timeout = '900s'")
    ids = run_engine.all_procedures(conn)[:limit]
    jobs = [ids[i:i + CHUNK] for i in range(0, len(ids), CHUNK)]
    print(f"{len(ids)} procedures in {len(jobs)} chunks", flush=True)
    tally = {str(w): collections.Counter() for w in windows}
    why_none = {str(w): collections.Counter() for w in windows}
    written, done, t0 = collections.Counter(), 0, time.time()
    import subprocess
    commit = subprocess.run(["git", "rev-parse", "--short=9", "HEAD"], capture_output=True, text=True, cwd=ROOT).stdout.strip() or "0000000"
    for out, wr, n in Engine(write=cmd == "write", commit=commit).chunk.map(jobs, kwargs={"windows": windows}, order_outputs=False):
        for w, (t, wn, _) in out.items():
            tally[w].update({tuple(json.loads(json.dumps(k))) if isinstance(k, list) else k: v for k, v in t.items()})
            why_none[w].update(wn)
        written.update(wr)
        done += n
        if done % 100000 < CHUNK:
            print(f"... {done}/{len(ids)} in {time.time() - t0:.0f} s", flush=True)
    for w in tally:
        t = tally[w]
        res = collections.Counter(); per = collections.Counter()
        for (rid, r, why), n in t.items():
            res[r] += n
            if r != "nao_avaliado":
                per[(rid, r)] += n
        print(json.dumps({"window_days": w, "procedures": done, "seconds": round(time.time() - t0), "by_result": dict(res),
                          "without_verdicts": dict(why_none[w]), "decided_by_rule": {f"{a}|{b}": n for (a, b), n in sorted(per.items())},
                          **({"written": dict(written)} if cmd == "write" else {})}, ensure_ascii=False, indent=1))
