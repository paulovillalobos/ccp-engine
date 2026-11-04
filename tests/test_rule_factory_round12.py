"""D72: round 12's targets are drawn by code from the store (rule_factory.draw12) and kept as drawn in pick.json: every real
passage that states days or euros and that no round asked the same question of. Its strata follow TRAIN-HELD-OUT's frozen
rule, and every prompt prints what its reading may quote."""
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT)); sys.path.insert(0, str(ROOT / "tools"))
import read_rules_v3 as v3  # noqa: E402
import rule_factory as rf  # noqa: E402
from engine.store import Store  # noqa: E402

STORE = Store([ROOT / "law", ROOT / "rules", ROOT / "governance"]).load()
PICK = [tuple(x) for x in json.loads(rf.PICK12_FILE.read_text(encoding="utf-8"))["pick"]]
RESERVED = set(json.loads((ROOT / "law/TRAIN-HELD-OUT.json").read_text(encoding="utf-8"))["reserved_articles"])


def test_the_pick_is_the_draw():
    assert [tuple(x) for x in rf.draw12(STORE)] == PICK


def test_no_target_asks_again_what_a_round_asked():
    asked = {t["rule"] for m in rf.FROUNDS if m < 12 for t in rf.targets(STORE, m)}
    rules = [t["rule"] for t in rf.targets(STORE, 12)]
    assert len(rules) == len(set(rules)) == len(PICK) and not set(rules) & asked


def test_strata_follow_the_frozen_rule():
    law = v3.Law(STORE)
    for pid, _, _, k in PICK:
        art = law.article_of(pid) or pid
        hashed = not pid.startswith("ccp:") and int(hashlib.sha256(art.encode()).hexdigest(), 16) % 5 == 0
        assert k == ("reservado" if art in RESERVED or hashed else "pratica"), pid


def test_types_follow_the_words():
    law = v3.Law(STORE)
    for pid, d, type_, _ in PICK:
        assert type_ == rf.type12(law.own(pid, d)), (pid, d)


def test_every_prompt_prints_what_its_reading_may_quote():
    for t in rf.targets(STORE, 12):
        body = json.loads((rf.FROUNDS[12]["dir"] / rf.rr.slug(t["rule"]) / "prompt.json").read_text(encoding="utf-8"))
        assert body["protocol_version"] == v3.V05 and body["date"] == t["date"]
        shown = v3.norm(body["prompt"])
        assert all(v3.norm(line) in shown for text in body["context"]["allowed"].values() for line in (text or "").split("\n") if line.strip()), t["rule"]
