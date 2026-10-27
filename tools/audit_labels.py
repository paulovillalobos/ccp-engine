"""Audits the written questions' labels with the guard (DECISIONS D53). No model.

    .venv/bin/python tools/audit_labels.py [batch-NN ...]     one block per question where the label and the guard differ

The guard (tools/fact_guard.py) reads places, «preço base» wording, citations and start dates exactly. A disagreement
is either a label that breaks LABELS.md (fix the label) or a case the guard cannot know (a place outside the gazetteer,
a doubt only a reader sees): read each one and decide.
"""
import glob
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
import fact_guard as fg  # noqa: E402


def main():
    only = sys.argv[1:]
    known = fg.known_ids()
    files = sorted(glob.glob(str(ROOT / "training/written-questions/batch-*.jsonl")))
    rows = [json.loads(l) for f in files if not only or any(o in f for o in only) for l in open(f, encoding="utf-8") if l.strip()]
    n = 0
    for q in rows:
        gold = {"factos": q["factos"], "ambiguos": q.get("ambiguos") or {}, "contraditorios": q.get("contraditorios") or {}, "citacoes": q.get("citacoes") or []}
        g = fg.guard(q["pergunta"], q["hoje"], gold, known)
        d = []
        for k in set(gold["factos"]) | set(g["factos"]):
            if gold["factos"].get(k) != g["factos"].get(k):
                d.append(f"factos.{k}: {gold['factos'].get(k)} -> {g['factos'].get(k)}")
        for k in ("territorio", "preco_base", "data_inicio_procedimento"):
            if sorted(map(str, gold["ambiguos"].get(k) or [])) != sorted(map(str, g["ambiguos"].get(k) or [])):
                d.append(f"ambiguos.{k}: {gold['ambiguos'].get(k)} -> {g['ambiguos'].get(k)}")
        if sorted(gold["citacoes"]) != sorted(g["citacoes"]):
            d.append(f"citacoes: {gold['citacoes']} -> {g['citacoes']}")
        if d:
            n += 1
            print(q["id"], "|", q["pergunta"][:100])
            for x in d:
                print("    ", x)
    print(n, "disagreements")


if __name__ == "__main__":
    main()
