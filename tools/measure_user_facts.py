"""Phase 8 measurement (DECISIONS D50): the family-A reader on a person's question -> facts. A ferramenta; no model.

    .venv/bin/python tools/measure_user_facts.py --date 2026-10-27 --out reports/measure/factos-v5-2026-10-27.json

Two golds: training/data-v5/factos_utilizador/held_out.jsonl (generated, wordings never trained) and
training/real-questions/factos-v1.jsonl (hand-written, no template; the transfer test). Answers:
governance/readings/avaliacao-v5/<set>/<leitor>.jsonl. Per reader and set: the share of questions whose facts equal the
gold; facts added (not stated), missed (stated, not given) and wrong (given with another value); 95 % Wilson intervals;
each answer file's sha256, so verify MEAS recomputes the report from those exact files.
"""
import argparse
import hashlib
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SETS = {"factos_utilizador": ROOT / "training/data-v5/factos_utilizador/held_out.jsonl",
        "factos_reais": ROOT / "training/real-questions/factos-v1.jsonl"}
ANSWERS = ROOT / "governance/readings/avaliacao-v5"
READERS = [("leitor-a", "base"), ("leitor-a5", "base + adaptador v4"), ("leitor-a6", "base + adaptador v5")]
VERSION = "ccp-measure-user-facts-0.1"


def wil(k, n, z=1.96):
    if n == 0:
        return {"k": 0, "n": 0, "value": None, "wilson95": [0.0, 1.0]}
    p = k / n; d = 1 + z * z / n; c = (p + z * z / (2 * n)) / d; h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return {"k": k, "n": n, "value": round(p, 4), "wilson95": [round(max(0.0, c - h), 4), round(min(1.0, c + h), 4)]}


def facts(text):
    try:
        f = json.loads(text)["factos"]
    except (json.JSONDecodeError, TypeError, KeyError):
        return None
    if not isinstance(f, dict):
        return None
    return {k: (int(v) if isinstance(v, float) and v.is_integer() else v) for k, v in f.items() if v is not None}


def report(date, only=None):
    """only: the readers a stored report holds (verify MEAS), so a reader added later does not change an earlier report."""
    rep = {"tool": VERSION, "date": date, "sets": {}}
    for name, gf in SETS.items():
        gold = {json.loads(l)["id"]: facts(json.loads(l)["answer"]) for l in gf.read_text(encoding="utf-8").splitlines() if l.strip()}
        s = {"gold": str(gf.relative_to(ROOT)), "gold_sha256": hashlib.sha256(gf.read_bytes()).hexdigest(), "examples": len(gold), "readers": {}}
        for leitor, label in READERS:
            f = ANSWERS / name / f"{leitor}.jsonl"
            if (only is not None and leitor not in only) or not f.exists():
                continue
            ans = {json.loads(l)["id"]: facts(json.loads(l)["answer"]) for l in f.read_text(encoding="utf-8").splitlines() if l.strip()}
            exact = added = missed = wrong = given = stated = invalid = 0
            for i, g in gold.items():
                a = ans.get(i)
                stated += len(g)
                if a is None:
                    invalid += 1; missed += len(g)
                    continue
                exact += a == g; given += len(a)
                added += sum(1 for k in a if k not in g); missed += sum(1 for k in g if k not in a)
                wrong += sum(1 for k in g if k in a and a[k] != g[k])
            s["readers"][leitor] = {"label": label, "answers_sha256": hashlib.sha256(f.read_bytes()).hexdigest(), "invalid": invalid,
                                    "exact": wil(exact, len(gold)), "added": wil(added, given), "missed": wil(missed, stated), "wrong": wil(wrong, stated),
                                    "facts": {"stated": stated, "given": given, "added": added, "missed": missed, "wrong": wrong}}
        rep["sets"][name] = s
    return rep


def pct(m):
    return "—" if m["value"] is None else f"{100 * m['value']:.1f} % [{100 * m['wilson95'][0]:.1f}, {100 * m['wilson95'][1]:.1f}] ({m['k']}/{m['n']})"


def render_md(rep):
    L = [f"# Medição — pergunta de uma pessoa → factos ({rep['date']})", "",
         f"Gerado por tools/measure_user_facts.py ({rep['tool']}). factos_utilizador: perguntas geradas com formulações nunca treinadas; "
         "factos_reais: perguntas escritas à mão, sem modelo de frase (D50). Intervalos de Wilson a 95 %.", ""]
    for name, s in rep["sets"].items():
        L += [f"## {name} ({s['examples']} perguntas)", "", "| leitor | factos exatos | acrescentados | em falta | com outro valor | inválidas |", "|---|---|---|---|---|---|"]
        for leitor, r in s["readers"].items():
            L.append(f"| {leitor} ({r['label']}) | {pct(r['exact'])} | {pct(r['added'])} | {pct(r['missed'])} | {pct(r['wrong'])} | {r['invalid']} |")
        L.append("")
    return "\n".join(L)


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
