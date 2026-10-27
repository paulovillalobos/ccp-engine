"""Phase 9 measurement (DECISIONS D52): the family-A reader on the written questions. A ferramenta; no model.

    .venv/bin/python tools/measure_written.py --date 2027-... --out reports/measure/escritas-v6-<date>.json

Golds: training/data-v6/factos_v6/held_out.jsonl (dev, 100) and final.jsonl (sealed, 100), both clean as written.
Answers: governance/readings/avaliacao-v6/<set>/<leitor>.jsonl. Per reader and set: the whole answer exact; the facts
exact; facts invented (given, not stated: the decision metric, an invented fact is worse than a missing one), missed and
with another value; markers (ambiguos + contraditorios fields) found and flagged without cause; citations exact;
default fills (today's date or a zero price given when the question states none). 95 % Wilson intervals; each answer
file's sha256 is in the report, so verify MEAS recomputes it from those exact files.
"""
import argparse
import hashlib
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SETS = {"dev": ROOT / "training/data-v6/factos_v6/held_out.jsonl", "final": ROOT / "training/data-v6/factos_v6/final.jsonl"}
ANSWERS = ROOT / "governance/readings/avaliacao-v6"
READERS = [("leitor-a", "base"), ("leitor-a5", "base + adaptador v4"), ("leitor-a7", "base + adaptador v6")]
VERSION = "ccp-measure-written-0.1"


def wil(k, n, z=1.96):
    if n == 0:
        return {"k": 0, "n": 0, "value": None, "wilson95": [0.0, 1.0]}
    p = k / n; d = 1 + z * z / n; c = (p + z * z / (2 * n)) / d; h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return {"k": k, "n": n, "value": round(p, 4), "wilson95": [round(max(0.0, c - h), 4), round(min(1.0, c + h), 4)]}


def num(v):
    return int(v) if isinstance(v, float) and v.is_integer() else v


def parse(text):
    try:
        a = json.loads(text)
    except (json.JSONDecodeError, TypeError):
        return None
    if not isinstance(a, dict) or not isinstance(a.get("factos"), dict):
        return None
    marks = lambda d: {k: sorted({json.dumps(num(x)) for x in (v if isinstance(v, list) else [v])}) for k, v in (d or {}).items()}  # noqa: E731
    return {"factos": {k: num(v) for k, v in a["factos"].items() if v is not None}, "ambiguos": marks(a.get("ambiguos")),
            "contraditorios": marks(a.get("contraditorios")), "citacoes": sorted(set(a.get("citacoes") or []))}


def report(date, only=None):
    """only: the readers a stored report holds (verify MEAS), so a reader added later does not change an earlier report."""
    rep = {"tool": VERSION, "date": date, "sets": {}}
    for name, gf in SETS.items():
        lines = [json.loads(l) for l in gf.read_text(encoding="utf-8").splitlines() if l.strip()]
        gold = {r["id"]: parse(r["answer"]) for r in lines}
        today = {r["id"]: r["prompt"].split("Data de hoje: ", 1)[1][:10] for r in lines}
        s = {"gold": str(gf.relative_to(ROOT)), "gold_sha256": hashlib.sha256(gf.read_bytes()).hexdigest(), "examples": len(gold), "readers": {}}
        for leitor, label in READERS:
            f = ANSWERS / name / f"{leitor}.jsonl"
            if (only is not None and leitor not in only) or not f.exists():
                continue
            ans = {json.loads(l)["id"]: parse(json.loads(l)["answer"]) for l in f.read_text(encoding="utf-8").splitlines() if l.strip()}
            c = dict(exact=0, facts_exact=0, given=0, stated=0, invented=0, missed=0, wrong=0, marks_gold=0, marks_found=0,
                     marks_given=0, marks_false=0, cites_exact=0, default_fill=0, invalid=0)
            for i, g in gold.items():
                a = ans.get(i)
                gm = set(g["ambiguos"]) | set(g["contraditorios"])
                c["stated"] += len(g["factos"]); c["marks_gold"] += len(gm)
                if a is None:
                    c["invalid"] += 1; c["missed"] += len(g["factos"])
                    continue
                am = set(a["ambiguos"]) | set(a["contraditorios"])
                c["exact"] += a == g; c["facts_exact"] += a["factos"] == g["factos"]; c["given"] += len(a["factos"])
                c["invented"] += sum(1 for k in a["factos"] if k not in g["factos"])
                c["missed"] += sum(1 for k in g["factos"] if k not in a["factos"])
                c["wrong"] += sum(1 for k in g["factos"] if k in a["factos"] and a["factos"][k] != g["factos"][k])
                c["marks_given"] += len(am); c["marks_found"] += len(am & gm); c["marks_false"] += len(am - gm)
                c["cites_exact"] += a["citacoes"] == g["citacoes"]
                c["default_fill"] += ("data_inicio_procedimento" not in g["factos"] and a["factos"].get("data_inicio_procedimento") == today[i]) \
                    + ("preco_base" not in g["factos"] and a["factos"].get("preco_base") == 0)
            n = len(gold)
            s["readers"][leitor] = {"label": label, "answers_sha256": hashlib.sha256(f.read_bytes()).hexdigest(), "invalid": c["invalid"],
                                    "exact": wil(c["exact"], n), "facts_exact": wil(c["facts_exact"], n), "invented": wil(c["invented"], c["given"]),
                                    "missed": wil(c["missed"], c["stated"]), "wrong": wil(c["wrong"], c["stated"]),
                                    "markers_found": wil(c["marks_found"], c["marks_gold"]), "markers_false": wil(c["marks_false"], c["marks_given"]),
                                    "citations_exact": wil(c["cites_exact"], n), "default_fill": c["default_fill"], "counts": c}
        rep["sets"][name] = s
    return rep


def pct(m):
    return "—" if m["value"] is None else f"{100 * m['value']:.1f} % [{100 * m['wilson95'][0]:.1f}, {100 * m['wilson95'][1]:.1f}] ({m['k']}/{m['n']})"


def render_md(rep):
    L = [f"# Medição — perguntas escritas → factos, marcadores e citações ({rep['date']})", "",
         f"Gerado por tools/measure_written.py ({rep['tool']}). Perguntas escritas uma a uma (D52), tal como escritas; dev e final (selado). "
         "Intervalos de Wilson a 95 %.", ""]
    for name, s in rep["sets"].items():
        L += [f"## {name} ({s['examples']} perguntas)", "",
              "| leitor | resposta exata | factos exatos | factos inventados | factos em falta | outro valor | marcadores achados | marcadores sem causa | citações exatas | preenchidos por defeito | inválidas |",
              "|---|---|---|---|---|---|---|---|---|---|---|"]
        for leitor, r in s["readers"].items():
            L.append(f"| {leitor} ({r['label']}) | {pct(r['exact'])} | {pct(r['facts_exact'])} | {pct(r['invented'])} | {pct(r['missed'])} | {pct(r['wrong'])} | "
                     f"{pct(r['markers_found'])} | {pct(r['markers_false'])} | {pct(r['citations_exact'])} | {r['default_fill']} | {r['invalid']} |")
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
