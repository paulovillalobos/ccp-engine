"""Phase 12 training data (DECISIONS D61): data-v9, the written questions with v8's dev errors answered.

The 3 600 questions of training/written-questions: batches 01-60 (D52-D54) and 61-72 (D61, 600 questions written on the five
errors v8 made on dev: a procedure only asked about, a procedure as the subject, a contract type said in words, a mixed
object, dense telegraphic facts; each line names its target in `alvo`). ERRATA.jsonl applied in full: v7's entries and the
D61 ones (`since` "v9": the label rules «Asked, not stated» and «One candidate» of LABELS.md applied to batches 01-60).
Split: the 3 000 keep v8's split (final 400 and dev 400 unchanged in membership, never trained); the 600 new go by sha256 of
the id, 100 to a targeted dev set (held_out_alvo) and 500 to train. Train: each question clean and in make_written.NOISY_COPIES
noisy copies, plus the D50 template questions. Prompt and answer format: v6's (make_written).
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
from engine.canon import sha256_text  # noqa: E402

VERSION = "ccp-make-written-v9-0.1"
DATA = ROOT / "training/data-v9"
TASK = "factos_v9"
SEED = 20261031
BATCHES = [f"batch-{i:02d}.jsonl" for i in range(1, 73)]
NEW_ALVO = 100


def errata(rows):
    """Every entry of ERRATA.jsonl, in order. Ops: remove.factos, move_to_ambiguos (v7); set_facto, remove_facto,
    remove_ambiguo, set_ambiguo (D61). A set_facto on a field held in ambiguos moves it."""
    by = {q["id"]: q for q in rows}
    for e in (json.loads(l) for l in (mw.WRITTEN / "ERRATA.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()):
        q = by[e["id"]]
        amb = q.setdefault("ambiguos", {})
        for k in (e.get("remove") or {}).get("factos", []):
            q["factos"].pop(k)
        for k in e.get("move_to_ambiguos", []):
            amb[k] = [q["factos"].pop(k)]
        op, f = e.get("op"), e.get("field")
        if op == "set_facto":
            amb.pop(f, None); q["factos"][f] = e["value"]
        elif op == "remove_facto":
            q["factos"].pop(f)
        elif op == "remove_ambiguo":
            amb.pop(f)
        elif op == "set_ambiguo":
            q["factos"].pop(f, None); amb[f] = e["value"]
    return rows


def written():
    rows = []
    for b in BATCHES:
        rows += [json.loads(l) for l in (mw.WRITTEN / b).read_text(encoding="utf-8").splitlines() if l.strip()]
    return errata(rows)


def split(rows):
    old = json.loads((ROOT / "training/data-v8/INDEX.json").read_text(encoding="utf-8"))["written"]
    where = {i: name for name, ids in old.items() for i in ids}
    parts, new = {"final": [], "held_out": [], "held_out_alvo": [], "train": []}, []
    for q in rows:
        (parts[where[q["id"]]].append(q) if q["id"] in where else new.append(q))
    new.sort(key=lambda q: sha256_text(f"{SEED}|{q['id']}"))
    parts["held_out_alvo"] += new[:NEW_ALVO]; parts["train"] += new[NEW_ALVO:]
    return parts


def row(q, text, source, style=None):
    r = mw.row(q, text, source, style)
    r.update(id=TASK + r["id"][len(mw.TASK):], task=TASK)
    for k in ("estilo", "alvo"):
        if q.get(k):
            r[k] = q[k]
    return r


def generate(store=None, held_doc=None):
    """{relative path: bytes} of training/data-v9. Pure: same written questions, errata and code -> same bytes."""
    parts = split(written())
    rng = random.Random(SEED)
    files, index = {}, {"version": VERSION, "seed": SEED, "split": {}, "files": {}, "written": {k: [q["id"] for q in v] for k, v in parts.items()}}
    seen = set()
    for name in ("final", "held_out", "held_out_alvo", "train"):
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
