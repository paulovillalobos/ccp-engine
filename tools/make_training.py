"""Training data for the reader, generated from law/ by code: no model, no network, no text that is not in law/.

    .venv/bin/python tools/make_training.py held-out          law/TRAIN-HELD-OUT.json (declared once, then sealed:
                                                              tools/measure.py seal)

The reservation is per article (the article ancestor of a passage; a passage without one is its own unit): an article
is reserved when int(sha256(article id as UTF-8).hexdigest(), 16) % 5 == 0 (about 20 %), and every article the 18 B3
rules cite (rules/ citations and exceptions) or offer as candidates (governance/readings/<rule>/prompt.json) is reserved
whole, so the measurement against the rules is clean. A reserved article covers all its descendant passages and all
their versions (and so their vigências). No training example in train may touch a reserved article.
"""
import argparse
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from engine.canon import canonical, sha256_text  # noqa: E402
from engine.sources import now_utc  # noqa: E402
from engine.store import Store  # noqa: E402

VERSION = "ccp-make-training-0.1"
HELD = ROOT / "law/TRAIN-HELD-OUT.json"
FROZEN_AT = "2026-10-25"


def current_passages(store):
    latest = {}
    for p in store.objects["passagem"]:
        if p["id"] not in latest or p["revision"] > latest[p["id"]]["revision"]:
            latest[p["id"]] = p
    return {k: v for k, v in latest.items() if not v.get("stale")}


def article_map(passages):
    """{passage id: the id of its article ancestor (itself for an article); its own id when it has none}."""
    above = {}  # passage id -> its article ancestor, or None when there is none

    def article_above(pid):
        if pid not in above:
            p = passages[pid]
            if p["kind"] == "artigo":
                above[pid] = pid
            else:
                parent = p.get("parent")
                above[pid] = article_above(parent) if parent in passages else None
        return above[pid]

    sys.setrecursionlimit(10000)
    return {pid: article_above(pid) or pid for pid in sorted(passages)}


def by_hash(article_id):
    return int(sha256_text(article_id), 16) % 5 == 0


def b3_articles(store, passages, art_of, readings=None):
    readings = readings or ROOT / "governance/readings"
    cited = set()
    for r in store.objects["regra"]:
        for c in r.get("passages", []):
            cited.add(c["passage"])
        for e in r.get("exceptions", []):
            for c in ([e.get("citation")] if isinstance(e.get("citation"), dict) else e.get("citations", [])):
                if isinstance(c, dict) and c.get("passage"):
                    cited.add(c["passage"])
    candidates = set()
    for f in sorted(readings.glob("*/prompt.json")) if readings.exists() else []:
        candidates.update(json.loads(f.read_text(encoding="utf-8")).get("candidates", []))
    return sorted({art_of[p] for p in cited | candidates if p in art_of})


def held_out_doc(store):
    passages = current_passages(store)
    art_of = article_map(passages)
    articles = sorted(set(art_of.values()))
    hashed = sorted(a for a in articles if by_hash(a))
    b3 = b3_articles(store, passages, art_of)
    definition = {
        "unit": "article: the article ancestor of a passage (kind artigo); a passage with no article above it is its own unit",
        "by_hash": {"rule": "int(sha256(article id as UTF-8).hexdigest(), 16) % 5 == 0", "share": "about 20 % of articles"},
        "by_b3": {"rule": "every article the 18 B3 rules cite (rules/ citations and exceptions) or offer as candidates "
                          "(governance/readings/<rule>/prompt.json), reserved whole",
                  "articles": b3},
        "covers": "every passage descending from a reserved article, all its versions and so its vigências",
        "held_out_when": "by_hash OR by_b3",
        "rule": "no example in any train.jsonl touches a reserved article (target, candidate or any source id); an example "
                "whose target is in a reserved article goes to held_out.jsonl",
    }
    reserved = sorted(set(hashed) | set(b3))
    return {"declared_at": now_utc(), "frozen_at": FROZEN_AT,
            "declared_before": "any training example was generated (training/ does not exist yet)",
            "definition": definition, "sha256": sha256_text(canonical(definition)),
            "counts": {"units": len(articles), "by_hash": len(hashed), "by_b3": len(b3), "reserved": len(reserved)},
            "reserved_articles": reserved}


def load_repo():
    return Store([ROOT / "law", ROOT / "rules", ROOT / "governance"]).load()


def main():
    ap = argparse.ArgumentParser(description="held-out")
    ap.add_argument("cmd", choices=["held-out"])
    a = ap.parse_args()
    if a.cmd == "held-out":
        if HELD.exists():
            raise SystemExit(f"{HELD.relative_to(ROOT)} exists: it is declared once and sealed, never redrawn")
        doc = held_out_doc(load_repo())
        HELD.write_text(json.dumps(doc, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        print(doc["counts"], "sha256", hashlib.sha256(HELD.read_bytes()).hexdigest())


if __name__ == "__main__":
    main()
