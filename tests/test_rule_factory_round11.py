"""D69: round 11's 60 real passages are drawn as its comment says. Each states days or euros in its own words and no earlier round
read it; the 28 «reservado» are in reserved articles, the 32 «texto_visto» are the first unreserved candidates by sha256 of the
id, and no rule-reading row v14 trained on shows any of the 60."""
import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT)); sys.path.insert(0, str(ROOT / "tools"))
import read_rules_v3 as v3  # noqa: E402
import rule_factory as rf  # noqa: E402
from engine.store import Store  # noqa: E402

STORE = Store([ROOT / "law", ROOT / "rules", ROOT / "governance"]).load()
LAW = v3.Law(STORE)
PICK = rf.FROUNDS[11]["pick"]
DAYS = re.compile(r"\b(\d+|um|dois|três|quatro|cinco|seis|sete|oito|nove|dez|quinze|vinte|trinta|sessenta|noventa)\s+dias\b", re.I)
EUR = re.compile(r"€|euros", re.I)
RESERVED = set(json.loads((ROOT / "law/TRAIN-HELD-OUT.json").read_text(encoding="utf-8"))["reserved_articles"])
PRACTICED = {"ccp:art190.2", "ccp:art191.2.a", "ccp:art191.3"}  # printed in data-v14's practice contexts


def candidates():
    own = {p: LAW.own(p, rf.DATE) or "" for p in LAW.p if p.startswith("ccp:art")}
    hits = [p for p, t in own.items() if DAYS.search(t) or EUR.search(t)]
    read = {t["source_passage"] for t in rf.targets(STORE)}
    return [p for p in hits if not any(o != p and o.startswith(p + ".") for o in hits) and p not in read
            and p.split(".")[0] not in rf.HAND_READ]


def test_the_pick_is_the_draw():
    cands = candidates()
    reserved = sorted(p for p in cands if LAW.article_of(p) in RESERVED and p not in PRACTICED)
    rest = sorted((p for p in cands if LAW.article_of(p) not in RESERVED), key=lambda p: hashlib.sha256(p.encode()).hexdigest())
    assert len(cands) == 136 and len(reserved) == 28
    assert {p for p, (_, k) in PICK.items() if k == "reservado"} == set(reserved)
    assert {p for p, (_, k) in PICK.items() if k == "texto_visto"} == set(rest[:32])


def test_types_and_targets():
    for p, (type_, _) in PICK.items():
        assert type_ == ("limiar" if EUR.search(LAW.own(p, rf.DATE)) else "prazo_minimo"), p
    T = rf.targets(STORE, 11)
    assert len(T) == 60 and {t["source_passage"] for t in T} == set(PICK)
    assert not {t["rule"] for t in T} & {t["rule"] for t in rf.targets(STORE)}


def test_no_rule_reading_row_shows_the_pick():
    for sub in ("data-v13", "data-v14"):
        raw = (ROOT / "training" / sub / "regra_lida/train.jsonl").read_text(encoding="utf-8")
        shown = set(re.findall(r"\[(ccp:art[^\]\s]+)\]", raw)) | set(re.findall(r"\"(ccp:art[^\"@\s]+)(?:@[^\"]*)?\"", raw))
        assert not shown & set(PICK), (sub, sorted(shown & set(PICK)))
