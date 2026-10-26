"""Phase 5 measurement (DECISIONS D46): the family-A reader before and after its adapters on condicoes_texto held_out.
A ferramenta; no model: it reads the stored answers.

    .venv/bin/python tools/measure_conditions.py --date 2026-10-26 --out reports/measure/condicoes-v2-2026-10-26.json

Gold: training/data-v2/condicoes_texto/held_out.jsonl (passages of reserved articles, labelled by code). Answers:
governance/readings/avaliacao-v2/condicoes_texto/<leitor>.jsonl ({"id", "at", "sha256", "answer"}; readers/leitor_a_modal.py
JSONL mode) for leitor-a (base), leitor-a2 (v1) and leitor-a3 (v2). Per reader: the share of examples whose answer equals
the gold on every field; per field the share equal; the values added (named in the answer, not in the text) and missed
(in the text, not in the answer) over all list fields; 95 % Wilson intervals. The report carries each answer file's
sha256, so verify MEAS recomputes it from those exact files.
"""
import argparse
import hashlib
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GOLD = ROOT / "training/data-v2/condicoes_texto/held_out.jsonl"
ANSWERS = ROOT / "governance/readings/avaliacao-v2/condicoes_texto"
READERS = [("leitor-a", "base"), ("leitor-a2", "base + adaptador v1"), ("leitor-a3", "base + adaptador v2"), ("leitor-a4", "base + adaptador v3")]
FIELDS = ["menciona_joue", "territorio", "tipo_contrato", "tipo_procedimento"]
LISTS = ["territorio", "tipo_contrato", "tipo_procedimento"]
VERSION = "ccp-measure-conditions-0.1"


def wil(k, n, z=1.96):
    if n == 0:
        return {"k": 0, "n": 0, "value": None, "wilson95": [0.0, 1.0]}
    p = k / n; d = 1 + z * z / n; c = (p + z * z / (2 * n)) / d; h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return {"k": k, "n": n, "value": round(p, 4), "wilson95": [round(max(0.0, c - h), 4), round(min(1.0, c + h), 4)]}


def parse(text):
    try:
        a = json.loads(text)
    except (json.JSONDecodeError, TypeError):
        return None
    if not isinstance(a, dict) or any(f not in a for f in FIELDS):
        return None
    return {"menciona_joue": a["menciona_joue"], **{f: sorted(set(a[f])) if isinstance(a[f], list) else None for f in LISTS}}


def report(date):
    gold = {}
    for line in GOLD.read_text(encoding="utf-8").splitlines():
        ex = json.loads(line)
        gold[ex["id"]] = json.loads(ex["answer"])
    rep = {"tool": VERSION, "date": date, "gold": str(GOLD.relative_to(ROOT)), "gold_sha256": hashlib.sha256(GOLD.read_bytes()).hexdigest(),
           "examples": len(gold), "readers": {}}
    for leitor, label in READERS:
        f = ANSWERS / f"{leitor}.jsonl"
        if not f.exists():
            continue
        ans = {}
        for line in f.read_text(encoding="utf-8").splitlines():
            r = json.loads(line)
            ans[r["id"]] = r["answer"]
        exact = invalid = 0
        per = {fl: 0 for fl in FIELDS}
        added = missed = named_gold = named_ans = 0
        for i, g in gold.items():
            a = parse(ans.get(i))
            if a is None:
                invalid += 1
                named_gold += sum(len(g[fl]) for fl in LISTS)
                missed += sum(len(g[fl]) for fl in LISTS)
                continue
            exact += all(a[fl] == g[fl] for fl in FIELDS)
            for fl in FIELDS:
                per[fl] += a[fl] == g[fl]
            for fl in LISTS:
                ga, aa = set(g[fl]), set(a[fl] or [])
                added += len(aa - ga); missed += len(ga - aa); named_gold += len(ga); named_ans += len(aa)
        n = len(gold)
        rep["readers"][leitor] = {"label": label, "answers_sha256": hashlib.sha256(f.read_bytes()).hexdigest(), "invalid": invalid,
                                  "exact": wil(exact, n), "per_field": {fl: wil(per[fl], n) for fl in FIELDS},
                                  "values": {"named_in_text": named_gold, "named_in_answer": named_ans, "added": added, "missed": missed,
                                             "added_share_of_answer": wil(added, named_ans), "missed_share_of_text": wil(missed, named_gold)}}
    return rep


def pct(m):
    return "—" if m["value"] is None else f"{100 * m['value']:.1f} % [{100 * m['wilson95'][0]:.1f}, {100 * m['wilson95'][1]:.1f}] ({m['k']}/{m['n']})"


def render_md(rep):
    L = [f"# Medição — condicoes_texto, reservados ({rep['date']})", "",
         f"Gerado por tools/measure_conditions.py ({rep['tool']}) a partir das respostas guardadas em governance/readings/avaliacao-v2/. "
         f"{rep['examples']} passagens de artigos reservados, rotuladas por código (D46). Intervalos de Wilson a 95 %.", "",
         "| leitor | exato (todos os campos) | menciona_joue | territorio | tipo_contrato | tipo_procedimento | valores acrescentados | valores em falta | inválidas |",
         "|---|---|---|---|---|---|---|---|---|"]
    for leitor, r in rep["readers"].items():
        pf = r["per_field"]; v = r["values"]
        L.append(f"| {leitor} ({r['label']}) | {pct(r['exact'])} | {pct(pf['menciona_joue'])} | {pct(pf['territorio'])} | {pct(pf['tipo_contrato'])} | "
                 f"{pct(pf['tipo_procedimento'])} | {v['added']} de {v['named_in_answer']} ({pct(v['added_share_of_answer'])}) | "
                 f"{v['missed']} de {v['named_in_text']} ({pct(v['missed_share_of_text'])}) | {r['invalid']} |")
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
