"""Phase 11 measurement (DECISIONS D54): the readers on the v8 written questions, with and without the guard. No model.

    .venv/bin/python tools/measure_written_v8.py --date 2027-... --out reports/measure/escritas-v8-<date>.json

Golds: training/data-v8/factos_v8/held_out.jsonl (dev, 400) and final.jsonl (sealed, 400; half in the 20 styles of D54). Answers:
governance/readings/avaliacao-v8/<set>/<leitor>.jsonl. Each reader is measured as it answered and after the guard
(tools/fact_guard.py), applied here to the stored answers, so the guarded score is recomputed from the same files every
time. The metrics are tools/measure_written's.
"""
import argparse
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
import fact_guard  # noqa: E402
import measure_written as mw  # noqa: E402

SETS = {"dev": ROOT / "training/data-v8/factos_v8/held_out.jsonl", "final": ROOT / "training/data-v8/factos_v8/final.jsonl",
        "reais": ROOT / "training/real-questions/ccdr-alentejo-v1.jsonl"}  # reais: 16 real questions to CCDR Alentejo, never trained
ANSWERS = ROOT / "governance/readings/avaliacao-v8"
READERS = [("leitor-a8", "base + adaptador v7"), ("leitor-a10", "base + adaptador v8"), ("leitor-a11", "base + adaptador v9"),
           ("leitor-b", "Reader B (família B), teto")]
VERSION = "ccp-measure-written-v8-0.1"


def score(gold, today, ans):
    c = dict(exact=0, facts_exact=0, given=0, stated=0, invented=0, missed=0, wrong=0, marks_gold=0, marks_found=0, marks_given=0, marks_false=0,
             cites_exact=0, default_fill=0, invalid=0)
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
    n, w = len(gold), mw.wil
    return {"invalid": c["invalid"], "exact": w(c["exact"], n), "facts_exact": w(c["facts_exact"], n), "invented": w(c["invented"], c["given"]),
            "missed": w(c["missed"], c["stated"]), "wrong": w(c["wrong"], c["stated"]), "markers_found": w(c["marks_found"], c["marks_gold"]),
            "markers_false": w(c["marks_false"], c["marks_given"]), "citations_exact": w(c["cites_exact"], n), "default_fill": c["default_fill"], "counts": c}


def report(date, only=None):
    """only: the readers a stored report holds (verify MEAS), so a reader added later does not change an earlier report."""
    known = fact_guard.known_ids()
    rep = {"tool": VERSION, "guard": fact_guard.VERSION, "date": date, "sets": {}}
    for name, gf in SETS.items():
        lines = [json.loads(l) for l in gf.read_text(encoding="utf-8").splitlines() if l.strip()]
        gold = {r["id"]: mw.parse(r["answer"]) for r in lines}
        today = {r["id"]: r["prompt"].split("Data de hoje: ", 1)[1][:10] for r in lines}
        question = {r["id"]: r["prompt"].split("Pergunta: ", 1)[1] for r in lines}
        s = {"gold": str(gf.relative_to(ROOT)), "gold_sha256": hashlib.sha256(gf.read_bytes()).hexdigest(), "examples": len(gold), "readers": {}}
        for leitor, label in READERS:
            f = ANSWERS / name / f"{leitor}.jsonl"
            if (only is not None and leitor not in only) or not f.exists():
                continue
            raw = {json.loads(l)["id"]: json.loads(l)["answer"] for l in f.read_text(encoding="utf-8").splitlines() if l.strip()}
            ans = {i: mw.parse(t) for i, t in raw.items()}
            guarded = {}
            for i, t in raw.items():
                try:
                    a = json.loads(t)
                except json.JSONDecodeError:
                    continue
                if i in question:
                    guarded[i] = mw.parse(json.dumps(fact_guard.guard(question[i], today[i], a, known), ensure_ascii=False))
            s["readers"][leitor] = {"label": label, "answers_sha256": hashlib.sha256(f.read_bytes()).hexdigest(),
                                    "as_answered": score(gold, today, ans), "after_guard": score(gold, today, guarded)}
        rep["sets"][name] = s
    return rep


def render_md(rep):
    pct = mw.pct
    L = [f"# Medição — perguntas escritas, v8 ({rep["date"]})", "",
         f"Gerado por tools/measure_written_v7.py ({rep['tool']}, guarda {rep['guard']}). dev 400 e final 400 (selado, metade nos 20 estilos), tal como escritas. "
         "Cada leitor tal como respondeu e depois da guarda. Intervalos de Wilson a 95 %.", ""]
    for name, s in rep["sets"].items():
        L += [f"## {name} ({s['examples']} perguntas)", "",
              "| leitor | | factos exatos | resposta exata | factos inventados | factos em falta | marcadores achados | marcadores sem causa | inválidas |",
              "|---|---|---|---|---|---|---|---|---|"]
        for leitor, r in s["readers"].items():
            for k, tag in (("as_answered", "como respondeu"), ("after_guard", "com a guarda")):
                x = r[k]
                L.append(f"| {leitor} ({r['label']}) | {tag} | {pct(x['facts_exact'])} | {pct(x['exact'])} | {pct(x['invented'])} | {pct(x['missed'])} | "
                         f"{pct(x['markers_found'])} | {pct(x['markers_false'])} | {x['invalid']} |")
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
