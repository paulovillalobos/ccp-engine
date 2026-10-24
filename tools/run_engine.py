"""The engine over a store of facts: every proc evaluated against the package its regime selects (FILL-PLAN B4).

    .venv/bin/python tools/run_engine.py --out reports/prazos-minimos.json [--stores data law rules governance]
                                          [--verdicts reports/veredictos] [--known-at 2026-10-24T00:00:00Z] [--commit SHA]

For each unidade of kind proc: its facts (engine.store.facts_of, known at --known-at), the regime its data_inicio_
procedimento selects (the settled seletor_regime of the packages: params.regimes -> package), and engine.evaluate with
that package's rules at the revisions it names, valid_at = the procedure's start date. Each verdict is written to
--verdicts as a store (veredicto/<id>.json) so verify re-derives it (RED); the report counts, per prazo_minimo rule,
cumpre / nao_cumpre / nao_avaliado by reason, and "declarado vs avaliado" where an afirmação sits beside a verdict.
The manifest (engine.manifest.build) names the law version, the package, the adapters of the facts, one source snapshot
per source (the latest raw record of each source the facts and the law come from), the code (repository, --commit or
git HEAD, engine version), the log head and produced_at = known_at. Same inputs, same bytes: everything is sorted and
known_at is fixed. Nothing here calls a model or the network.
"""
import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
import verify  # noqa: E402  (its readers of the store are the ones RED uses: same inputs, same verdicts)
from engine import evaluate as evaluate_mod  # noqa: E402
from engine import manifest as manifest_mod  # noqa: E402
from engine.governance import head  # noqa: E402
from engine.store import Store, Writer, facts_of  # noqa: E402

VERSION = "ccp-run-engine-0.1"
REPOSITORY = "github.com/paulovillalobos/ccp-engine"


def selector(store):
    """The settled seletor_regime named by the packages, or None."""
    for pk in sorted(verify.current_of(store, "pacote").values(), key=lambda p: p["id"]):
        rules, _ = verify.package_rules(store, pk["id"])
        for r in rules:
            if r["type"] == "seletor_regime":
                return r
    return None


def regime_package(sel, start):
    for g in sel["params"]["regimes"]:
        if g["from"] <= start and (g["to"] is None or start < g["to"]):
            return g["package"], g["law_version"]
    return None, None


def snapshots(store, facts, law_raw):
    """One snapshot per source: the latest raw record of that source among the facts' origins and the law."""
    raws = {f["origin"]["raw"] for f in facts if f.get("origin")} | ({law_raw} if law_raw else set())
    latest = {}
    for rid in raws:
        r = store.current(rid)
        if r and (r["source"] not in latest or (r["captured_at"], r["sha256"]) > (latest[r["source"]]["captured_at"], latest[r["source"]]["sha256"])):
            latest[r["source"]] = r
    return [{"source": s, "sha256": r["sha256"], "captured_at": r["captured_at"]} for s, r in sorted(latest.items())]


def run(stores, known_at, commit, verdict_dir=None):
    store = Store(stores).load()
    sel = selector(store)
    head_ = head(store.events)
    procs = sorted((u for u in verify.current_of(store, "unidade").values() if u["kind"] == "proc" and not u.get("stale")), key=lambda u: u["id"])
    report = {"rules": {}, "declarado_vs_avaliado": {}, "units": 0, "sem_regime": 0}
    manifests, verdicts = {}, []
    for unit in procs:
        facts = facts_of(store, unit["id"], known_at=known_at)
        start = next((f["value"] for f in sorted(facts, key=lambda f: (f["known_at"], f["id"])) if f["field"] == "data_inicio_procedimento"), None)
        if sel is None or start is None:
            report["sem_regime"] += 1
            continue
        package, law_version = regime_package(sel, start)
        if package is None or store.current(package) is None:
            report["sem_regime"] += 1
            continue
        rules, _ = verify.package_rules(store, package)
        rules = [r for r in rules if unit["kind"] in r["applies_to"] or r["type"] == "seletor_regime"]  # a rule judges only its kinds
        chain, _ = verify.unit_chain(store, unit["id"])
        lineage = set(chain) | {u["id"] for u in verify.current_of(store, "unidade").values() if unit["id"] in verify.unit_chain(store, u["id"])[0]}
        manifest = manifest_mod.build(law_version, package, sorted({f["adapter"] for f in facts}),
                                      snapshots(store, facts, "raw:dr-consolidado:lei:ccp"),
                                      {"repository": REPOSITORY, "commit": commit, "engine_version": evaluate_mod.VERSION}, head_, known_at)
        produced = evaluate_mod.evaluate(
            unit, rules, facts, known_at, start, manifest=manifest,
            conflicts=[c for c in verify.current_of(store, "conflito").values() if c["unit"] in chain],
            assertions=[a for a in verify.current_of(store, "afirmacao").values() if a["unit"] == unit["id"]],
            entities=[e for e in verify.current_of(store, "entidade").values() if any(r["unit"] in lineage for r in e["roles"])],
            documents=[d for d in verify.current_of(store, "documento").values() if d["origin"]["unit"] in chain],
            coverage=verify.coverage_of(store, manifest["adapters"]))
        report["units"] += 1
        manifests[manifest_mod.manifest_hash(manifest)] = manifest
        for v in produced:
            verdicts.append(v)
            rule = next(r for r in rules if r["id"] == v["rule"]["id"])
            if rule["type"] != "prazo_minimo":
                continue
            c = report["rules"].setdefault(v["rule"]["id"], {"cumpre": 0, "nao_cumpre": 0, "nao_avaliado": {}})
            if v["result"] == "nao_avaliado":
                c["nao_avaliado"][v["reason"]] = c["nao_avaliado"].get(v["reason"], 0) + 1
            else:
                c[v["result"]] += 1
            for a in v["assertions_compared"]:
                d = report["declarado_vs_avaliado"].setdefault(v["rule"]["id"], {"concorda": 0, "discorda": 0, "nao_avaliado": 0})
                d["concorda" if a["agrees"] is True else "discorda" if a["agrees"] is False else "nao_avaliado"] += 1
    report["manifest"] = sorted(manifests.values(), key=lambda m: (m["package"], manifest_mod.manifest_hash(m)))
    report["engine"] = {"tool": VERSION, "known_at": known_at, "verdicts": len(verdicts)}
    if verdict_dir:
        vd = Path(verdict_dir)
        vd.mkdir(parents=True, exist_ok=True)
        existing = Store([vd]).load()
        writer = Writer(vd, existing)
        for v in sorted(verdicts, key=lambda v: v["id"]):
            if existing.current(v["id"]) is None:
                writer.append(v)
    return report


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--stores", nargs="+", default=["data", "law", "rules", "governance"])
    ap.add_argument("--verdicts")
    ap.add_argument("--known-at", default=None)
    ap.add_argument("--commit", default=None)
    a = ap.parse_args()
    stores = [ROOT / s if not Path(s).is_absolute() else Path(s) for s in a.stores]
    store = Store(stores).load()
    known_at = a.known_at or max((f["known_at"] for f in store.objects["facto"]), default="1970-01-01T00:00:00Z")
    commit = a.commit or subprocess.run(["git", "rev-parse", "--short=9", "HEAD"], capture_output=True, text=True, cwd=ROOT).stdout.strip() or "unknown"
    report = run(stores, known_at, commit, a.verdicts)
    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    Path(a.out).write_text(json.dumps(report, ensure_ascii=False, indent=1, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"units": report["units"], "sem_regime": report["sem_regime"], "verdicts": report["engine"]["verdicts"], "rules": len(report["rules"])}))


if __name__ == "__main__":
    main()
