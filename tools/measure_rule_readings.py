"""Phase 13 measurement (DECISIONS D63): the readers on the held-out rule readings of data-v10. No model.

    .venv/bin/python tools/measure_rule_readings.py --date 2026-10-28 --out reports/measure/regras-v10-<date>.json

Gold: training/data-v10/regra_lida/held_out.jsonl (82 written articles, never trained). Answers:
governance/readings/avaliacao-v10/dev/<leitor>.jsonl. A reading is scored as the rules factory scores two readers
(read_rules.parse_answers, canonical form, D43): rules exact = the same rules, one by one; count exact = the same number
of rules; days exact = the same days or limits, rule by rule; invalid = not JSON, or a passage outside the candidates.
"""
import argparse
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT)); sys.path.insert(0, str(ROOT / "tools"))
import measure_written as mw  # noqa: E402  (Wilson intervals)
import read_rules as rr  # noqa: E402

GOLD = ROOT / "training/data-v10/regra_lida/held_out.jsonl"
ANSWERS = ROOT / "governance/readings/avaliacao-v10/dev"
READERS = [("leitor-a11", "base + adaptador v9"), ("leitor-a12", "base + adaptador v10"), ("leitor-b", "Reader B (família B)")]
VERSION = "ccp-measure-rule-readings-0.1"


def target_of(row):
    items = row["schema"]["properties"]["regras"]["items"]["properties"]
    return {"type": items["tipo"]["enum"][0], "candidates": items["passagens"]["items"]["enum"]}


def score(gold, ans):
    c = dict(rules_exact=0, count_exact=0, days_exact=0, invalid=0, padded=0)
    for i, (t, g) in gold.items():
        a = rr.parse_answers({"answer": ans[i]}, t) if i in ans else None
        if a is None:
            c["invalid"] += 1
            continue
        c["count_exact"] += len(a) == len(g)
        c["padded"] += len(a) > len(g)
        c["days_exact"] += sorted(map(str, map(rr.key_param, a))) == sorted(map(str, map(rr.key_param, g)))
        c["rules_exact"] += len(a) == len(g) and all(rr.same_reading(x, y) for x, y in zip(a, g))
    n, w = len(gold), mw.wil
    return {"rules_exact": w(c["rules_exact"], n), "count_exact": w(c["count_exact"], n), "days_exact": w(c["days_exact"], n),
            "more_rules_than_gold": w(c["padded"], n), "invalid": c["invalid"], "counts": c}


def report(date, only=None):
    rows = [json.loads(l) for l in GOLD.read_text(encoding="utf-8").splitlines() if l.strip()]
    gold = {r["id"]: (target_of(r), rr.parse_answers({"answer": r["answer"]}, target_of(r))) for r in rows}
    rep = {"tool": VERSION, "date": date, "gold": str(GOLD.relative_to(ROOT)), "gold_sha256": hashlib.sha256(GOLD.read_bytes()).hexdigest(),
           "examples": len(gold), "readers": {}}
    for leitor, label in READERS:
        f = ANSWERS / f"{leitor}.jsonl"
        if (only is not None and leitor not in only) or not f.exists():
            continue
        ans = {json.loads(l)["id"]: json.loads(l)["answer"] for l in f.read_text(encoding="utf-8").splitlines() if l.strip()}
        rep["readers"][leitor] = {"label": label, "answers_sha256": hashlib.sha256(f.read_bytes()).hexdigest(), **score(gold, ans)}
    return rep


def render_md(rep):
    f = lambda x: f"{100 * x['value']:.1f} % [{100 * x['wilson95'][0]:.1f}, {100 * x['wilson95'][1]:.1f}] ({x['k']}/{x['n']})"
    L = [f"# Medição — leitura de regras, v10 ({rep['date']})", "",
         f"Gerado por tools/measure_rule_readings.py ({rep['tool']}). {rep['examples']} artigos escritos (held_out de data-v10, nunca "
         "treinados); cada leitura comparada com a de ouro em forma canónica, regra a regra (D43). Intervalos de Wilson a 95 %.", "",
         "| leitor | regras exatas | número de regras certo | dias ou limites certos | mais regras que o ouro | inválidas |", "|---|---|---|---|---|---|"]
    for k, r in rep["readers"].items():
        L.append(f"| {k} ({r['label']}) | {f(r['rules_exact'])} | {f(r['count_exact'])} | {f(r['days_exact'])} | {f(r['more_rules_than_gold'])} | {r['invalid']} |")
    return "\n".join(L) + "\n"


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--date", required=True); ap.add_argument("--out", required=True)
    a = ap.parse_args()
    rep = report(a.date)
    out = Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(rep, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    out.with_suffix(".md").write_text(render_md(rep), encoding="utf-8")
    print(render_md(rep))


if __name__ == "__main__":
    main()
