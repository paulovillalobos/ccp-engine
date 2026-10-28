"""Carries v8's and Reader B's stored answers on dev, final and reais into avaliacao-v9 (DECISIONS D61). No model.

    .venv/bin/python tools/carry_answers_v9.py

data-v9's dev and final are data-v8's questions; only labels changed (D61 errata). An answer is carried only when the v9 prompt is
byte-identical to the v8 prompt it answered; the id gets v9's task prefix. Refuses to overwrite a file that differs.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
V8, V9 = ROOT / "training/data-v8/factos_v8", ROOT / "training/data-v9/factos_v9"
SRC, DST = ROOT / "governance/readings/avaliacao-v8", ROOT / "governance/readings/avaliacao-v9"


def main():
    for name in ("held_out", "final"):
        s = {"held_out": "dev", "final": "final"}[name]
        p8 = {r["id"].split(":", 1)[1]: r["prompt"] for r in map(json.loads, (V8 / f"{name}.jsonl").read_text(encoding="utf-8").splitlines()) if r}
        p9 = {r["id"].split(":", 1)[1]: r["prompt"] for r in map(json.loads, (V9 / f"{name}.jsonl").read_text(encoding="utf-8").splitlines()) if r}
        assert p8 == p9, f"{name}: v9 prompts differ from v8's"
        for leitor in ("leitor-a10", "leitor-b"):
            rows = [json.loads(l) for l in (SRC / s / f"{leitor}.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
            out = "".join(json.dumps({**r, "id": "factos_v9:" + r["id"].split(":", 1)[1]}, ensure_ascii=False) + "\n" for r in rows)
            f = DST / s / f"{leitor}.jsonl"
            f.parent.mkdir(parents=True, exist_ok=True)
            if f.exists() and f.read_text(encoding="utf-8") != out:
                raise SystemExit(f"{f} exists and differs")
            f.write_text(out, encoding="utf-8")
            print(f"{len(rows)} -> {f.relative_to(ROOT)}")
    for leitor in ("leitor-a10", "leitor-b"):  # reais: the same gold file in both versions, answers carried unchanged
        src, f = SRC / "reais" / f"{leitor}.jsonl", DST / "reais" / f"{leitor}.jsonl"
        f.parent.mkdir(parents=True, exist_ok=True)
        if f.exists() and f.read_bytes() != src.read_bytes():
            raise SystemExit(f"{f} exists and differs")
        f.write_bytes(src.read_bytes())
        print(f"{src.read_text(encoding='utf-8').count(chr(10))} -> {f.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
