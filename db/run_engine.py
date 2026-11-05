"""The engine over the Postgres store (DECISIONS D80): every procedure's facts from Supabase × the settled rules of the
package in force on its start date → verdicts, each with its complete manifest.

    .venv/bin/python -I db/run_engine.py report [--limit N] [--after UNIT]   evaluate, write nothing, print counts by rule and result
    .venv/bin/python -I db/run_engine.py write  [--limit N] [--after UNIT]   evaluate and insert the verdicts into ccp.veredicto

The law, the rules and the log come from the repository's files (git is their source of truth); the facts come from
ccp.facto (the compact view), read in pages of procedures. The package is chosen as the API chooses it (tools/serve.choose_package) from
the fact data_inicio_procedimento; a procedure without it is counted as «sem data de início» and gets no verdict (which
date starts a procedure is a reading of the law, D80, not a choice of this code). A deadline stated as two dates needs a
settled counting rule (engine/evaluate.deadline_days); none is passed until one is settled, so those verdicts read
regra_ausente. A verdict is immutable: one already stored under its (id, revision) is skipped.
"""
import argparse
import collections
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT)); sys.path.insert(0, str(ROOT / "tools")); sys.path.insert(0, str(ROOT / "db"))
import pg  # noqa: E402
import serve  # noqa: E402
import verify  # noqa: E402
from engine import evaluate as evaluate_mod  # noqa: E402
from engine import manifest as manifest_mod  # noqa: E402
from engine.governance import head  # noqa: E402

VERSION = "ccp-run-engine-0.1"
START = "data_inicio_procedimento"
PAGE = 500


def procedures(conn, after, limit):
    """Procedure unit ids (kind proc) in id order after `after`, at most `limit`."""
    q = """select n.txt from ccp.unidade_atual u join ccp.nome n on n.no = u.id
           where u.kind = ccp.n('proc') and n.txt > %s order by n.txt limit %s"""
    return [r[0] for r in conn.execute(q, (after, limit)).fetchall()]


def facts_of(conn, units):
    out = collections.defaultdict(list)
    for unit, doc in conn.execute("select unit, doc from ccp.facto where unit = any(%s)", (units,)).fetchall():
        out[unit].append(doc)
    return out


def evaluate_unit(unit_id, facts, rules_of, now):
    """(verdicts, why none): the API's choice of package and manifest, over facts read from Postgres."""
    start = next((f["value"] for f in facts if f["field"] == START), None)
    if not isinstance(start, str) or not serve.DATE.match(start):
        return [], "sem data de início"
    package, law_version, how = serve.choose_package(start)
    if package is None:
        return [], how
    rules = rules_of(package)
    known_at = max((f["known_at"] for f in facts), default=now)
    raws = sorted({f["origin"]["raw"] for f in facts if f.get("origin", {}).get("raw")})
    snaps = [{"source": r.split(":")[1], "sha256": "0" * 64, "captured_at": known_at} for r in raws[:1]] or [{"source": "ccp", "sha256": "0" * 64, "captured_at": known_at}]
    manifest = manifest_mod.build(law_version, package, sorted({f["adapter"] for f in facts}), snaps,
                                  {"repository": serve.REPOSITORY, "commit": serve.COMMIT, "engine_version": evaluate_mod.VERSION}, head(serve.STORE.events), known_at)
    unit = {"id": unit_id, "revision": 1, "kind": "proc"}
    return evaluate_mod.evaluate(unit, rules, facts, known_at, start, manifest=manifest), None


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("cmd", choices=["report", "write"])
    ap.add_argument("--limit", type=int, default=1000); ap.add_argument("--after", default="")
    a = ap.parse_args()
    serve.load(("law", "rules", "governance"))
    cache = {}

    def rules_of(package):
        if package not in cache:
            rules, _ = verify.package_rules(serve.STORE, package)
            cache[package] = [r for r in rules if "proc" in r["applies_to"]]
        return cache[package]

    import time
    now = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    conn = pg.connect()
    tally, why_none, done, after = collections.Counter(), collections.Counter(), 0, a.after
    written = collections.Counter()
    while done < a.limit:
        units = procedures(conn, after, min(PAGE, a.limit - done))
        if not units:
            break
        facts = facts_of(conn, units)
        page = []
        for u in units:
            verdicts, why = evaluate_unit(u, facts.get(u, []), rules_of, now)
            if why:
                why_none[why] += 1
            for v in verdicts:
                tally[(v["rule"]["id"], v["result"], v["reason"])] += 1
            page.extend(verdicts)
        if a.cmd == "write" and page:
            for k, v in pg.load_objects(conn, {"veredicto": page}).get("veredicto", {}).items():
                written[k] += v
        done += len(units)
        after = units[-1]
    print(json.dumps({"tool": VERSION, "procedures": done, "last": after, "without_verdicts": dict(why_none),
                      "verdicts": sum(tally.values()), "by_result": dict(collections.Counter(r for (_, r, _) in tally.elements())),
                      "by_reason": dict(collections.Counter(x for (_, _, x) in tally.elements() if x)),
                      **({"written": dict(written)} if a.cmd == "write" else {})}, ensure_ascii=False, indent=1))
    for (rid, res, why), n in sorted(tally.items(), key=lambda x: -x[1])[:25]:
        print(f"{n:7d}  {res:13s} {why or '':15s} {rid}")


if __name__ == "__main__":
    main()
