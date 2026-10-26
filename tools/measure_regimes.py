"""Phase 6 measurement (DECISIONS D47): the family-A reader on the selector tasks' held_out, before and after v3.
A ferramenta; no model: it reads the stored answers.

    .venv/bin/python tools/measure_regimes.py --date 2026-10-26 --out reports/measure/regimes-v3-2026-10-26.json

Gold: training/data-v3/<task>/held_out.jsonl (labelled by code). Answers: governance/readings/avaliacao-v3/<task>/<leitor>.jsonl
(readers/leitor_a_modal.py JSONL mode) for leitor-a (base), leitor-a3 (v2) and leitor-a4 (v3). entrada_em_vigor: the
date equal. periodos_vigencia: the list equal; the right number of periods; and a well-formed partition (each «ate» the
day before the next «de», the last «ate» null, no one-day period made of a «de» equal to its «ate» unless the gold has it).
95 % Wilson intervals; each answer file's sha256 is in the report, so verify MEAS recomputes it from those exact files.
"""
import argparse
import hashlib
import json
import math
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GOLD = ROOT / "training/data-v3"
ANSWERS = ROOT / "governance/readings/avaliacao-v3"
READERS = [("leitor-a", "base"), ("leitor-a3", "base + adaptador v2"), ("leitor-a4", "base + adaptador v3")]
TASKS = ["entrada_em_vigor", "periodos_vigencia"]
VERSION = "ccp-measure-regimes-0.1"


def wil(k, n, z=1.96):
    if n == 0:
        return {"k": 0, "n": 0, "value": None, "wilson95": [0.0, 1.0]}
    p = k / n; d = 1 + z * z / n; c = (p + z * z / (2 * n)) / d; h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return {"k": k, "n": n, "value": round(p, 4), "wilson95": [round(max(0.0, c - h), 4), round(min(1.0, c + h), 4)]}


def load(text):
    try:
        return json.loads(text)
    except (json.JSONDecodeError, TypeError):
        return None


def well_formed(per):
    try:
        for i, p in enumerate(per):
            nxt = per[i + 1]["de"] if i + 1 < len(per) else None
            if nxt is None:
                if p["ate"] is not None:
                    return False
            elif p["ate"] is None or date.fromisoformat(p["ate"]) != date.fromisoformat(nxt) - timedelta(days=1):
                return False
        return len(per) >= 2
    except (KeyError, TypeError, ValueError):
        return False


def report(date_):
    rep = {"tool": VERSION, "date": date_, "tasks": {}}
    for task in TASKS:
        gf = GOLD / task / "held_out.jsonl"
        gold = {json.loads(l)["id"]: load(json.loads(l)["answer"]) for l in gf.read_text(encoding="utf-8").splitlines() if l.strip()}
        t = {"gold": str(gf.relative_to(ROOT)), "gold_sha256": hashlib.sha256(gf.read_bytes()).hexdigest(), "examples": len(gold), "readers": {}}
        for leitor, label in READERS:
            f = ANSWERS / task / f"{leitor}.jsonl"
            if not f.exists():
                continue
            ans = {json.loads(l)["id"]: load(json.loads(l)["answer"]) for l in f.read_text(encoding="utf-8").splitlines() if l.strip()}
            n = len(gold)
            exact = sum(1 for i, g in gold.items() if ans.get(i) == g)
            r = {"label": label, "answers_sha256": hashlib.sha256(f.read_bytes()).hexdigest(), "invalid": sum(1 for i in gold if ans.get(i) is None),
                 "exact": wil(exact, n)}
            if task == "periodos_vigencia":
                count = sum(1 for i, g in gold.items() if isinstance(ans.get(i), dict) and len(ans[i].get("periodos") or []) == len(g["periodos"]))
                wf = sum(1 for i in gold if isinstance(ans.get(i), dict) and well_formed(ans[i].get("periodos") or []))
                r.update(right_number_of_periods=wil(count, n), well_formed_partition=wil(wf, n))
            t["readers"][leitor] = r
        rep["tasks"][task] = t
    return rep


def pct(m):
    return "—" if m["value"] is None else f"{100 * m['value']:.1f} % [{100 * m['wilson95'][0]:.1f}, {100 * m['wilson95'][1]:.1f}] ({m['k']}/{m['n']})"


def render_md(rep):
    L = [f"# Medição — tarefas do seletor de regime, reservados ({rep['date']})", "",
         f"Gerado por tools/measure_regimes.py ({rep['tool']}) a partir das respostas guardadas em governance/readings/avaliacao-v3/; "
         "rótulos por código (D47). Intervalos de Wilson a 95 %.", ""]
    for task, t in rep["tasks"].items():
        L += [f"## {task} ({t['examples']} exemplos reservados)", ""]
        if task == "periodos_vigencia":
            L += ["| leitor | exato | número de períodos certo | partição bem formada | inválidas |", "|---|---|---|---|---|"]
            for leitor, r in t["readers"].items():
                L.append(f"| {leitor} ({r['label']}) | {pct(r['exact'])} | {pct(r['right_number_of_periods'])} | {pct(r['well_formed_partition'])} | {r['invalid']} |")
        else:
            L += ["| leitor | data exata | inválidas |", "|---|---|---|"]
            for leitor, r in t["readers"].items():
                L.append(f"| {leitor} ({r['label']}) | {pct(r['exact'])} | {r['invalid']} |")
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
