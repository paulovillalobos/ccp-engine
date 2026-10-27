"""Training task factos_v8 (phase 11, DECISIONS D54), built by code from the written questions: no model, no network.

    .venv/bin/python tools/make_written_v8.py generate [--out DIR]   training/data-v8/factos_v8/{train,held_out,final}.jsonl, INDEX.json

The 3 000 questions of training/written-questions (batches 01-60: 1 000 of D52/D53, 2 000 in 20 styles of D54), ERRATA.jsonl
applied. Split: the 1 000 of v7 keep their v7 split (training/data-v7/INDEX.json); the 2 000 new ones go by sha256 of the
id, 200 final, 200 held_out (dev), 1 600 train. So final and dev hold 400 each, never trained, half of each in the 20
styles. Train: each question clean and in make_written.NOISY_COPIES noisy copies, plus the same 2 000 D50 template questions.
Prompt and answer format: v6's (make_written).
"""
import argparse
import hashlib
import json
import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT)); sys.path.insert(0, str(ROOT / "tools"))
import make_training as mt  # noqa: E402
import make_written as mw  # noqa: E402  (prompt, answer, schema, noise)
import make_written_v7 as v7  # noqa: E402  (errata)
from engine.canon import sha256_text  # noqa: E402

VERSION = "ccp-make-written-v8-0.1"
DATA = ROOT / "training/data-v8"
TASK = "factos_v8"
SEED = 20261030
BATCHES = [f"batch-{i:02d}.jsonl" for i in range(1, 61)]
NEW_FINAL, NEW_DEV = 200, 200


def written():
    rows = []
    for b in BATCHES:
        rows += [json.loads(l) for l in (mw.WRITTEN / b).read_text(encoding="utf-8").splitlines() if l.strip()]
    return v7.errata(rows)


def split(rows):
    old = json.loads((ROOT / "training/data-v7/INDEX.json").read_text(encoding="utf-8"))["written"]
    where = {i: name for name, ids in old.items() for i in ids}
    parts, new = {"final": [], "held_out": [], "train": []}, []
    for q in rows:
        (parts[where[q["id"]]].append(q) if q["id"] in where else new.append(q))
    new.sort(key=lambda q: sha256_text(f"{SEED}|{q['id']}"))
    parts["final"] += new[:NEW_FINAL]; parts["held_out"] += new[NEW_FINAL:NEW_FINAL + NEW_DEV]; parts["train"] += new[NEW_FINAL + NEW_DEV:]
    return parts


def row(q, text, source, style=None):
    r = mw.row(q, text, source, style)
    r.update(id=TASK + r["id"][len(mw.TASK):], task=TASK)
    if q.get("estilo"):
        r["estilo"] = q["estilo"]
    return r


def generate(store=None, held_doc=None):
    """{relative path: bytes} of training/data-v8. Pure: same written questions, errata and code -> same bytes."""
    parts = split(written())
    rng = random.Random(SEED)
    files, index = {}, {"version": VERSION, "seed": SEED, "split": {}, "files": {}, "written": {k: [q["id"] for q in v] for k, v in parts.items()}}
    seen = set()
    for name in ("final", "held_out", "train"):
        rows = []
        for q in parts[name]:
            variants = [row(q, q["pergunta"], "written")]
            if name == "train":
                for _ in range(mw.NOISY_COPIES):
                    style = mw.pick_style(rng)
                    variants.append(row(q, mw.noisy(q["pergunta"], style, rng), "written", style))
            for r in variants:
                if r["prompt"] not in seen:
                    seen.add(r["prompt"]); rows.append(r)
        if name == "train":
            for r in mw.template_rows(random.Random(mw.SEED)):
                r = dict(r, id=TASK + r["id"][len(mw.TASK):], task=TASK)
                if r["prompt"] not in seen:
                    seen.add(r["prompt"]); rows.append(r)
        rel = f"{TASK}/{name}.jsonl"
        files[rel] = ("\n".join(json.dumps(r, ensure_ascii=False) for r in rows) + "\n").encode("utf-8")
        index["split"][name] = len(rows)
    for rel in sorted(files):
        index["files"][rel] = {"sha256": hashlib.sha256(files[rel]).hexdigest(), "lines": files[rel].count(b"\n")}
    files["INDEX.json"] = (json.dumps(index, ensure_ascii=False, sort_keys=True, indent=1) + "\n").encode("utf-8")
    return files


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["generate"]); ap.add_argument("--out", default=str(DATA))
    a = ap.parse_args()
    files = generate()
    mt.write(files, Path(a.out))
    print(json.loads(files["INDEX.json"])["split"])


if __name__ == "__main__":
    main()
