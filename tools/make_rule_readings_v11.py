"""Phase 14 data (DECISIONS D65): data-v11, a new dev and sealed set of written articles and v10's targeted training rows.

    .venv/bin/python tools/make_rule_readings_v11.py check      the code checks on every eval and targeted example, nothing written
    .venv/bin/python tools/make_rule_readings_v11.py generate   training/data-v11

Sources, written for this project as training/rule-readings/batch-*.jsonl were (GUIDE.md, invented article numbers, gold
written from the text, never from another reader's answer):
- eval-*.jsonl: the measurement pool, split by sha256 of the id into dev (studied: v10's errors are sorted here) and sealed
  (read by no one until v11 is trained and BEFORE is committed). Never trained.
- alvo-*.jsonl: targeted training articles, written after v10's dev errors were sorted, on those error kinds.
The 82 held-out articles of data-v10 stay as they are (v10 was measured on them once).

The code checks are make_rule_readings' (D63), with more reference texts: an eval article must not be close to a real target
passage nor to a data-v10 training article (batch-*); a targeted article must not be close to a real passage nor to an eval
article (difflib ratio below LEAK); and, in id order, an eval article whose cited passage is close to one an earlier eval
article cites is dropped (it would measure the same reading twice, perhaps once in dev and once in sealed). Out: regra_lida/dev.jsonl and sealed.jsonl (no train.jsonl, so train_lora does not replace
data-v10's regra_lida), regra_lida_alvo/train.jsonl (each targeted article twice, as in data-v10).
"""
import argparse
import difflib
import hashlib
import json
import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT)); sys.path.insert(0, str(ROOT / "tools"))
import make_rule_readings as m  # noqa: E402  (texts, prompts, answers, code checks: D63's)
import make_training as mt  # noqa: E402

VERSION = "ccp-make-rule-readings-v11-0.1"
DATA = ROOT / "training/data-v11"
SEED = 20261029


def load(pattern):
    rows = []
    for f in sorted(m.WRITTEN.glob(pattern)):
        rows += [json.loads(l) for l in f.read_text(encoding="utf-8").splitlines() if l.strip()]
    return rows


def passage_texts(rows):
    return [t for ex in rows for pid, t in m.texts(ex).items() if pid != m.pid_of(ex, "")]


def near(ex, refs):
    """The reference texts that could be close to one of the example's passages: quick_ratio bounds ratio from above, so
    the full check in m.problems sees every text that can reach LEAK and no other."""
    mine = [t for pid, t in m.texts(ex).items() if pid != m.pid_of(ex, "")]
    out = []
    for x in refs:
        for t in mine:
            if abs(len(x) - len(t)) < 0.5 * len(t):
                sm = difflib.SequenceMatcher(None, t, x)
                if sm.real_quick_ratio() >= m.LEAK and sm.quick_ratio() >= m.LEAK:
                    out.append(x)
                    break
    return out


def split_of(ex):
    return "dev" if int(hashlib.sha256(ex["id"].encode()).hexdigest(), 16) % 2 == 0 else "sealed"


def checked(store=None):
    """(eval examples, targeted examples, {id: problems}) after the code checks."""
    real = m.reference_texts(store)
    ev, tg = load("eval-*.jsonl"), load("alvo-*.jsonl")
    ids = [ex.get("id") for ex in m.written() + ev + tg]
    dup = {i for i in ids if ids.count(i) > 1}
    train_txt = passage_texts(m.written())  # the targeted articles come later: one close to an eval article is dropped, never the eval one
    eval_txt = passage_texts(ev)
    dropped = {}
    for ex, refs in [(ex, real + train_txt) for ex in ev] + [(ex, real + eval_txt) for ex in tg]:
        pr = (["id used twice"] if ex.get("id") in dup else []) or m.problems(ex, near(ex, refs))
        if pr:
            dropped[ex.get("id", "?")] = pr
    kept = []  # an eval article whose cited passage is close to one an earlier article cites measures the same reading twice
    for ex in sorted((ex for ex in ev if ex.get("id") not in dropped), key=lambda ex: ex["id"]):
        mine = cited_texts(ex)
        twin = next((k for k, t in kept for x in mine if close(x, t)), None)
        if twin:
            dropped[ex["id"]] = [f"a cited passage close to one {twin} cites"]
        else:
            kept += [(ex["id"], t) for t in mine]
    return [ex for ex in ev if ex.get("id") not in dropped], [ex for ex in tg if ex.get("id") not in dropped], dropped


def cited_texts(ex):
    tx = m.texts(ex)
    return sorted({tx[m.pid_of(ex, x)] for r in ex["regras"] for x in r["passagens"] if x != ""})


def close(a, b):
    if abs(len(a) - len(b)) >= 0.5 * len(a):
        return False
    sm = difflib.SequenceMatcher(None, a, b)
    return sm.real_quick_ratio() >= m.LEAK and sm.quick_ratio() >= m.LEAK and sm.ratio() >= m.LEAK


def generate(store=None, held_doc=None):
    """{relative path: bytes} of training/data-v11. Pure: same written examples, store and code -> same bytes."""
    ev, tg, dropped = checked(store)
    rng = random.Random(SEED)
    parts = {"regra_lida/dev": [], "regra_lida/sealed": [], "regra_lida_alvo/train": []}
    for ex in ev:
        parts[f"regra_lida/{split_of(ex)}"].append(m.row(ex, rng, factory=rng.random() < 0.5))
    for ex in tg:
        parts["regra_lida_alvo/train"] += [m.row(ex, rng, factory=(k == 0 and rng.random() < 0.6)) for k in range(m.COPIES)]
    files, index = {}, {"version": VERSION, "seed": SEED, "split": {}, "files": {}, "dropped": dropped}
    for name, rs in parts.items():
        if not rs:
            continue
        rel = f"{name}.jsonl"
        files[rel] = ("\n".join(json.dumps(r, ensure_ascii=False) for r in rs) + "\n").encode("utf-8")
        index["split"][name] = len(rs)
    for rel in sorted(files):
        index["files"][rel] = {"sha256": hashlib.sha256(files[rel]).hexdigest(), "lines": files[rel].count(b"\n")}
    files["INDEX.json"] = (json.dumps(index, ensure_ascii=False, sort_keys=True, indent=1) + "\n").encode("utf-8")
    return files


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["check", "generate"]); ap.add_argument("--out", default=str(DATA)); ap.add_argument("--only")
    a = ap.parse_args()
    if a.cmd == "check":
        ev, tg, dropped = checked()
        for i, pr in dropped.items():
            if not a.only or str(i).startswith(a.only):
                print(i, "|", "; ".join(pr))
        print(f"{len(ev)} eval and {len(tg)} targeted examples pass, {len(dropped)} with problems")
        return
    files = generate()
    mt.write(files, Path(a.out))
    idx = json.loads(files["INDEX.json"])
    print(idx["split"], f"dropped {len(idx['dropped'])}")


if __name__ == "__main__":
    main()
