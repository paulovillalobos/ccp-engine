"""The engine over the Postgres store (DECISIONS D80, D82): every procedure's facts from Supabase × the settled CCP rules
in force when it started → verdicts, each with its complete manifest.

    .venv/bin/python -I db/run_engine.py report [--limit N] [--after UNIT] [--window DAYS ...]   evaluate, write nothing
    .venv/bin/python -I db/run_engine.py write  [--limit N] [--after UNIT] --window DAYS           insert into ccp.veredicto

The law, the rules and the log come from the repository's files (git is their source of truth); the facts come from
ccp.facto, read in pages of procedures, with the dates of each procedure's contracts (its child units).

The start date (D82). A procedure starts with the decisão de contratar (CCP art. 36.º n.º 1), a date no source holds.
When a procedure has a fact data_inicio_procedimento it is used. Otherwise the decision is bounded above by the
earliest act the sources date (the notice's sending or publication, the EU notice's sending, a contract's signing or
publication: `upper`), and below by `upper` − window days. The rules are evaluated on every date in that interval at
which a settled rule starts or stops being in force (and at both ends); when every one of those dates gives the same
result for each (rule type, field), that is the verdict, its detail naming the interval; when they differ, the
verdict is nao_avaliado (facto_ausente: data_inicio_procedimento). The window is a product rule of the person's: write
refuses to run until product_rule:janela-inicio-procedimento is settled in the log with that number of days. report
shows the counts for each window it is given, so the person decides on numbers.

A deadline stated as two dates is counted by the settled contagem_prazo rules in force (D83: the CCP's and, by CCP
art. 470.º n.º 1, CPA art. 87.º's), with the holidays of Código do Trabalho art. 234.º in force; until those rules are
settled the verdicts read regra_ausente. A verdict is immutable: one already stored under its (id, revision)
is skipped.
"""
import argparse
import collections
import datetime
import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT)); sys.path.insert(0, str(ROOT / "tools")); sys.path.insert(0, str(ROOT / "db"))
import pg  # noqa: E402
import serve  # noqa: E402
from engine import evaluate as evaluate_mod  # noqa: E402
from engine import manifest as manifest_mod  # noqa: E402
from engine import rules as rules_mod  # noqa: E402
from engine.governance import Log, head  # noqa: E402

VERSION = "ccp-run-engine-0.5"
START = "data_inicio_procedimento"
BOUNDS = ("data_envio_anuncio", "data_publicacao_anuncio", "data_envio_joue")  # the procedure's own dated acts
CHILD_BOUNDS = ("data_celebracao_contrato", "data_publicacao_contrato")  # its contracts'
WINDOW_RULE = "product_rule:janela-inicio-procedimento"
PAGE = 500


def procedures(conn, after, limit):
    """Procedure unit ids (kind proc) in id order after `after`, at most `limit`."""
    q = """select n.txt from ccp.unidade_atual u join ccp.nome n on n.no = u.id
           where u.kind = ccp.n('proc') and n.txt > %s order by n.txt limit %s"""
    return [r[0] for r in conn.execute(q, (after, limit)).fetchall()]


def all_procedures(conn):
    """D86: every procedure id in one read, sorted here (the paged query sorts 3 M names on every page: ~30 s a page)."""
    q = "select n.txt from ccp.unidade_atual u join ccp.nome n on n.no = u.id where u.kind = ccp.n('proc')"
    return sorted(r[0] for r in conn.execute(q).fetchall())


def facts_of(conn, units):
    out = collections.defaultdict(list)
    for unit, doc in conn.execute("select unit, doc from ccp.facto where unit = any(%s)", (units,)).fetchall():
        out[unit].append(doc)
    return out


def child_dates(conn, units):
    """{procedure: [dates of its contracts' CHILD_BOUNDS facts]}."""
    q = """select p.txt, f.value #>> '{}' from ccp.unidade_atual u join ccp.nome p on p.no = u.parent
           join ccp.facto_atual f on f.unit = u.id
           where p.txt = any(%s) and f.field = any(select no from ccp.nome where txt = any(%s))"""
    out = collections.defaultdict(list)
    for proc, value in conn.execute(q, (units, list(CHILD_BOUNDS))).fetchall():
        out[proc].append(value)
    return out


def iso(v):
    try:
        return datetime.date.fromisoformat(str(v)[:10])
    except ValueError:
        return None


def upper_bound(facts, dates):
    found = [iso(f["value"]) for f in facts if f["field"] in BOUNDS] + [iso(d) for d in dates]
    found = [d for d in found if d]
    return min(found) if found else None


def check_dates(rules, upper, window):
    """The dates of [upper − window, upper] on which the rules in force can change, both ends included."""
    low = upper - datetime.timedelta(days=window)
    edges = {low, upper}
    for r in rules:
        for k in ("valid_from", "valid_to"):
            d = iso(r.get(k)) if r.get(k) else None
            if d and low < d <= upper:
                edges.add(d)
    return sorted(edges)


def key_of(rules_by_id, v):
    r = rules_by_id[v["rule"]["id"]]
    p = r["params"]
    field = p.get("deadline_field") or (p.get("threshold") or {}).get("field") or r["id"]
    return (r["type"], field)


def evaluate_unit(unit_id, facts, dates, rules, window, now):
    """(verdicts, why none, how): the engine on each date the start may fall on; one result per (type, field) or none."""
    known_at = max((f["known_at"] for f in facts), default=now)
    raws = sorted({f["origin"]["raw"] for f in facts if (f.get("origin") or {}).get("raw")})
    snaps = [{"source": r.split(":")[1], "sha256": "0" * 64, "captured_at": known_at} for r in raws[:1]] or [{"source": "ccp", "sha256": "0" * 64, "captured_at": known_at}]
    unit = {"id": unit_id, "revision": 1, "kind": "proc"}
    by_id = {r["id"]: r for r in rules}

    def run(day):
        package = rules_mod.package(f"pacote:ccp@{day}", f"lei:ccp@{day}", [r for r in rules if rules_mod.valid_at(r, day)] or rules[:1],
                                    head(serve.STORE.events), known_at, known_at)
        manifest = manifest_mod.build(f"lei:ccp@{day}", package["id"], sorted({f["adapter"] for f in facts}) or ["adaptador:ccp@1"], snaps,
                                      {"repository": serve.REPOSITORY, "commit": serve.COMMIT, "engine_version": evaluate_mod.VERSION},
                                      head(serve.STORE.events), known_at)
        return evaluate_mod.evaluate(unit, rules, facts, known_at, facts_at, manifest=manifest, rules_at=day, calendar=holidays_text)

    upper = upper_bound(facts, dates)
    # every fact counts as of the latest date it is valid (the start only chooses the rules)
    facts_at = max([f["valid_at"] for f in facts if f.get("valid_at")] + ([upper.isoformat()] if upper else []), default=now[:10])
    start = next((f["value"] for f in facts if f["field"] == START), None)
    if isinstance(start, str) and serve.DATE.match(start):
        return run(start), None, "data_inicio_procedimento"
    if upper is None:
        return [], "sem data nenhuma", None
    if window is None:
        return [], "janela por decidir", None
    days = check_dates(rules, upper, window)
    runs = {d: run(d.isoformat()) for d in days}
    seen = [{key_of(by_id, v): (v["result"], v["reason"]) for v in out} for out in runs.values()]
    last = runs[days[-1]]
    if all(s == seen[-1] for s in seen):
        note = f"; início entre {days[0]} e {upper} (decisão de contratar não datada): o mesmo resultado em {len(days)} datas"
        return [{**v, "detail": (v["detail"] or "") + note} for v in last], None, "janela"
    keys = {k for s in seen for k in s}
    split = {k for k in keys if len({s.get(k) for s in seen}) > 1}
    return [v if key_of(by_id, v) not in split else
            {**v, "result": "nao_avaliado", "reason": "facto_ausente", "citation": None,
             "detail": f"data_inicio_procedimento: as regras em vigor entre {days[0]} e {upper} dão resultados diferentes"}
            for v in last], None, "janela (em parte)"


_LAW = {}


def holidays_text(year):
    """D83: the text of Código do Trabalho art. 234.º in force at the end of `year` (engine/calendario.py reads it)."""
    if "law" not in _LAW:
        import read_rules_v3 as v3
        _LAW["law"] = v3.Law(serve.STORE)
    return _LAW["law"].text("ct:art234", f"{year}-12-31") or ""


def settled_window(log):
    rp = log.replay()
    if rp.state_of("product_rule", WINDOW_RULE) != "settled":
        return None
    ev = [e for _, e in serve.STORE.events if e.get("assertion") == WINDOW_RULE and e["action"] in ("propose", "correct")][-1]
    return int(ev["payload"]["days"])


def counting_complete():
    """D85: (complete, pending): the counting provisions are used only when every one the rule factory asked about
    (its contagem_prazo targets) is settled, as rules or as «não tipável»; with one missing, a count made of the others
    could be wrong (CPA 87.º c) suspends a deadline that CCP 470.º n.º 3 makes continuous)."""
    import rule_factory as rf
    from engine.governance import Log
    log = Log(ROOT / "governance")
    pending = [t["source_passage"] for n, R in rf.FROUNDS.items() if any(isinstance(p, tuple) and p[2] == "contagem_prazo" for p in (R.get("pick") or []))
               for t in rf.targets(serve.STORE, n) if t["type"] == "contagem_prazo" and not rf.settled_before(log, t)]
    return not pending, sorted(set(pending))


def load_rules():
    current = {}
    for r in serve.STORE.objects["regra"]:
        if r["id"] not in current or r["revision"] > current[r["id"]]["revision"]:
            current[r["id"]] = r
    complete, pending = counting_complete()
    if pending:
        print(f"counting withheld: {len(pending)} counting passages not settled ({', '.join(pending)})", file=sys.stderr)
    return sorted((r for r in current.values() if r["state"] == "settled" and "proc" in r["applies_to"] and
                   (r["type"] != "contagem_prazo" or complete) and
                   (r["norma"] == "norma:ccp" or (r["type"] == "contagem_prazo" and r["norma"] == "norma:cpa"))),  # D83: CPA art. 87.º counts the CCP's deadlines (CCP art. 470.º n.º 1)
                  key=lambda r: r["id"])


_W = {}


def _init(write, commit=None):
    """D84: a worker process loads the store, the rules and a connection once (D86: on Modal the commit is given: no .git)."""
    serve.load(("law", "rules", "governance"), commit=commit)
    _W.update(rules=load_rules(), conn=pg.connect(), write=write, now=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()))


def _chunk(job):
    """D84: one chunk of procedure ids → (tallies per window, written counts, how many)."""
    units, windows = job
    conn, rules = _W["conn"], _W["rules"]
    facts, dates = facts_of(conn, units), child_dates(conn, units)
    out = {w: (collections.Counter(), collections.Counter(), collections.Counter()) for w in windows}
    written = collections.Counter()
    for w in windows:
        tally, why_none, how = out[w]
        page = []
        for u in units:
            verdicts, why, h = evaluate_unit(u, facts.get(u, []), dates.get(u, []), rules, w, _W["now"])
            if why:
                why_none[why] += 1
            if h:
                how[h] += 1
            for v in verdicts:
                tally[(v["rule"]["id"], v["result"], v["reason"])] += 1
            page.extend(verdicts)
        if _W["write"] and page:
            for k, n in pg.load_objects(conn, {"veredicto": page}).get("veredicto", {}).items():
                written[k] += n
    return out, written, len(units)


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("cmd", choices=["report", "write"])
    ap.add_argument("--limit", type=int, default=1000); ap.add_argument("--after", default="")
    ap.add_argument("--window", type=int, nargs="*", default=[])
    ap.add_argument("--workers", type=int, default=1, help="D84: processes, each with its own store and connection")
    a = ap.parse_args()
    serve.load(("law", "rules", "governance"))
    if a.cmd == "write":
        decided = settled_window(Log(ROOT / "governance"))
        if decided is None or a.window != [decided]:
            raise SystemExit(f"write needs --window {decided if decided is not None else 'N'}: {WINDOW_RULE} settled in the log with those days")
    rules = load_rules()
    windows = a.window or [None]
    conn = pg.connect()
    ids, after = [], a.after
    while len(ids) < a.limit:
        page = procedures(conn, after, min(50000, a.limit - len(ids)))
        if not page:
            break
        ids += page
        after = page[-1]
    jobs = [(ids[i:i + PAGE], windows) for i in range(0, len(ids), PAGE)]
    tally = {w: collections.Counter() for w in windows}
    why_none = {w: collections.Counter() for w in windows}
    how = {w: collections.Counter() for w in windows}
    written, done, t0 = collections.Counter(), 0, time.time()
    if a.workers > 1:
        import multiprocessing as mp
        pool = mp.get_context("spawn").Pool(a.workers, initializer=_init, initargs=(a.cmd == "write",))
        results = pool.imap_unordered(_chunk, jobs)
    else:
        _init(a.cmd == "write")
        results = map(_chunk, jobs)
    for out, wr, n in results:
        for w, (tl, wn, hw) in out.items():
            tally[w].update(tl); why_none[w].update(wn); how[w].update(hw)
        written.update(wr)
        done += n
        if done % 20000 < PAGE:
            print(f"... {done}/{len(ids)} procedures, {time.time() - t0:.0f} s", file=sys.stderr, flush=True)
    for w in windows:
        t = tally[w]
        print(json.dumps({"tool": VERSION, "window_days": w, "procedures": done, "last": ids[-1] if ids else a.after, "rules": len(rules),
                          "without_verdicts": dict(why_none[w]), "start_from": dict(how[w]), "verdicts": sum(t.values()),
                          "by_result": dict(collections.Counter(r for (_, r, _) in t.elements())),
                          "by_reason": dict(collections.Counter(x for (_, _, x) in t.elements() if x)),
                          "seconds": round(time.time() - t0),
                          **({"written": dict(written)} if a.cmd == "write" else {})}, ensure_ascii=False, indent=1))
        for (rid, res, why), n in sorted(t.items(), key=lambda x: -x[1])[:12]:
            print(f"{n:7d}  {res:13s} {why or '':15s} {rid}")


if __name__ == "__main__":
    main()
