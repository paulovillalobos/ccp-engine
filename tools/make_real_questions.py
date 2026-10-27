"""The real questions (D53) in the reader's prompt and answer format. No model.

    .venv/bin/python tools/make_real_questions.py      training/real-questions/<name>.jsonl from <name>.questions.jsonl (v6 label format)

training/real-questions/ccdr-alentejo-v1.questions.jsonl: 16 procurement questions put to CCDR Alentejo by câmaras,
juntas and a regional tourism body (2006-2025), each with its source, whether it is the asker's text quoted by the
opinion («citacao») or the opinion's restatement of it («reformulacao»), labelled by training/written-questions/LABELS.md.
Licence unknown: internal evaluation only, never training, never publication.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
import make_written as mw  # noqa: E402

NAMES = ["ccdr-alentejo-v1"]


def build(name):
    rows = []
    for l in (ROOT / f"training/real-questions/{name}.questions.jsonl").read_text(encoding="utf-8").splitlines():
        q = json.loads(l)
        rows.append(json.dumps({"id": q["id"], "task": "factos_reais", "prompt": mw.prompt(q["pergunta"], q["hoje"]), "answer": mw.answer(q),
                                "sources": [], "schema": mw.schema(), "fonte": q["fonte"], "forma": q["forma"]}, ensure_ascii=False))
    out = ROOT / f"training/real-questions/{name}.jsonl"
    out.write_text("\n".join(rows) + "\n", encoding="utf-8")
    return out


if __name__ == "__main__":
    for n in NAMES:
        print(build(n))
