"""Phase 7 measurement (DECISIONS D49): the family-A reader on condicoes_pergunta held_out (phrasings never trained on).
A ferramenta; no model: it reads the stored answers.

    .venv/bin/python tools/measure_question_conditions.py --date 2026-10-26 --out reports/measure/pergunta-v4-2026-10-26.json

Gold: training/data-v4/condicoes_pergunta/held_out.jsonl (labelled by code). Answers:
governance/readings/avaliacao-v4/condicoes_pergunta/<leitor>.jsonl for leitor-a (base), leitor-a4 (v3), leitor-a5 (v4).
Conditions are compared in the person's canonical form (D43: tools/read_rules). Per reader: the share of questions whose
condition set equals the gold; the conditions added (not stated by the question) and missed; 95 % Wilson intervals; each
answer file's sha256 is in the report, so verify MEAS recomputes it from those exact files.
"""
import argparse
import hashlib
import json
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
import read_rules  # noqa: E402  (the canonical form of a condition, D43)
from engine.canon import canonical  # noqa: E402

GOLD = ROOT / "training/data-v4/condicoes_pergunta/held_out.jsonl"
ANSWERS = ROOT / "governance/readings/avaliacao-v4/condicoes_pergunta"
READERS = [("leitor-a", "base"), ("leitor-a4", "base + adaptador v3"), ("leitor-a5", "base + adaptador v4")]
VERSION = "ccp-measure-question-conditions-0.1"


def wil(k, n, z=1.96):
    if n == 0:
        return {"k": 0, "n": 0, "value": None, "wilson95": [0.0, 1.0]}
    p = k / n; d = 1 + z * z / n; c = (p + z * z / (2 * n)) / d; h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return {"k": k, "n": n, "value": round(p, 4), "wilson95": [round(max(0.0, c - h), 4), round(min(1.0, c + h), 4)]}


def conds(text):
    try:
        a = json.loads(text)
        return {canonical(read_rules._ccond(c)) for c in a["condicoes"]}
    except (json.JSONDecodeError, TypeError, KeyError, AttributeError):
        return None


def report(date):
    gold = {}
    for line in GOLD.read_text(encoding="utf-8").splitlines():
        ex = json.loads(line)
        gold[ex["id"]] = conds(ex["answer"])
    rep = {"tool": VERSION, "date": date, "gold": str(GOLD.relative_to(ROOT)), "gold_sha256": hashlib.sha256(GOLD.read_bytes()).hexdigest(),
           "examples": len(gold), "readers": {}}
    for leitor, label in READERS:
        f = ANSWERS / f"{leitor}.jsonl"
        if not f.exists():
            continue
        ans = {json.loads(l)["id"]: conds(json.loads(l)["answer"]) for l in f.read_text(encoding="utf-8").splitlines() if l.strip()}
        exact = added = missed = named = stated = invalid = 0
        for i, g in gold.items():
            a = ans.get(i)
            if a is None:
                invalid += 1; missed += len(g); stated += len(g)
                continue
            exact += a == g
            added += len(a - g); missed += len(g - a); named += len(a); stated += len(g)
        n = len(gold)
        rep["readers"][leitor] = {"label": label, "answers_sha256": hashlib.sha256(f.read_bytes()).hexdigest(), "invalid": invalid,
                                  "exact": wil(exact, n), "added": wil(added, named), "missed": wil(missed, stated),
                                  "conditions": {"stated": stated, "answered": named, "added": added, "missed": missed}}
    return rep


def pct(m):
    return "—" if m["value"] is None else f"{100 * m['value']:.1f} % [{100 * m['wilson95'][0]:.1f}, {100 * m['wilson95'][1]:.1f}] ({m['k']}/{m['n']})"


def render_md(rep):
    L = [f"# Medição — condicoes_pergunta, reservados ({rep['date']})", "",
         f"Gerado por tools/measure_question_conditions.py ({rep['tool']}). {rep['examples']} perguntas com formulações nunca treinadas, "
         "rotuladas por código (D49); condições comparadas em forma canónica (D43). Intervalos de Wilson a 95 %.", "",
         "| leitor | conjunto de condições exato | condições acrescentadas | condições em falta | inválidas |", "|---|---|---|---|---|"]
    for leitor, r in rep["readers"].items():
        L.append(f"| {leitor} ({r['label']}) | {pct(r['exact'])} | {pct(r['added'])} | {pct(r['missed'])} | {r['invalid']} |")
    return "\n".join(L) + "\n"


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--date", required=True); ap.add_argument("--out", required=True)
    a = ap.parse_args()
    rep = report(a.date)
    out = Path(a.out); out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(rep, ensure_ascii=False, indent=1, sort_keys=True) + "\n", encoding="utf-8")
    out.with_suffix(".md").write_text(render_md(rep), encoding="utf-8")
    print(render_md(rep))


if __name__ == "__main__":
    main()
