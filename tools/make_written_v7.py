"""Training task factos_v7 (phase 10, DECISIONS D53), built by code from the written questions: no model, no network.

    .venv/bin/python tools/make_written_v7.py generate [--out DIR]   training/data-v7/factos_v7/{train,held_out,final}.jsonl, INDEX.json

The 1 000 questions of training/written-questions (batches 01-20), with ERRATA.jsonl applied (corrections found by
tools/fact_guard.py auditing the labels; the batch files stay as written). Split: the 500 of v6 keep their v6 split
(training/data-v6/INDEX.json); the 500 new ones go by sha256 of the id, 100 final, 100 held_out (dev), 300 train. So
final and dev hold 200 each, none ever trained. Train: each question clean and in make_written.NOISY_COPIES noisy
copies, plus the same 2 000 D50 template questions as v6. Prompt and answer format: v6's (make_written).
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
import make_written as mw  # noqa: E402  (prompt, answer, schema, noise: the same as v6)
from engine.canon import sha256_text  # noqa: E402

VERSION = "ccp-make-written-v7-0.1"
DATA = ROOT / "training/data-v7"
TASK = "factos_v7"
SEED = 20261029
BATCHES = [f"batch-{i:02d}.jsonl" for i in range(1, 21)]
NEW_FINAL, NEW_DEV = 100, 100


def errata(rows):
    by = {q["id"]: q for q in rows}
    for e in (json.loads(l) for l in (mw.WRITTEN / "ERRATA.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()):
        if e.get("since"):
            continue  # D61: an erratum for a later version (applied by its own generator) leaves data-v7 and data-v8 as built
        q = by[e["id"]]
        for k in (e.get("remove") or {}).get("factos", []):
            q["factos"].pop(k)
        for k in e.get("move_to_ambiguos", []):
            q.setdefault("ambiguos", {})[k] = [q["factos"].pop(k)]
    return rows


def written():
    rows = []
    for b in BATCHES:
        rows += [json.loads(l) for l in (mw.WRITTEN / b).read_text(encoding="utf-8").splitlines() if l.strip()]
    return errata(rows)


def split(rows):
    v6 = json.loads((ROOT / "training/data-v6/INDEX.json").read_text(encoding="utf-8"))["written"]
    where = {i: name for name, ids in v6.items() for i in ids}
    parts = {"final": [], "held_out": [], "train": []}
    new = []
    for q in rows:
        (parts[where[q["id"]]].append(q) if q["id"] in where else new.append(q))
    new.sort(key=lambda q: sha256_text(f"{SEED}|{q['id']}"))
    parts["final"] += new[:NEW_FINAL]; parts["held_out"] += new[NEW_FINAL:NEW_FINAL + NEW_DEV]; parts["train"] += new[NEW_FINAL + NEW_DEV:]
    return parts


def row(q, text, source, style=None):
    r = mw.row(q, text, source, style)
    r["id"] = TASK + r["id"][len(mw.TASK):]
    r["task"] = TASK
    return r


def generate(store=None, held_doc=None):
    """{relative path: bytes} of training/data-v7. Pure: same written questions, errata and code -> same bytes."""
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
