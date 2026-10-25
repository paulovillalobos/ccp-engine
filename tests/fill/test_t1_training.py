"""Phase 4 T0/T1 — training data for the reader, generated from law/ by code — red until it exists, is sealed and is clean.

Done when: law/TRAIN-HELD-OUT.json declares, per article, the deterministic reservation (sha256 rule ~20 % + every
article the 18 B3 rules cite or offer as candidates), frozen_at and the sha256 of its definition; the newest seal in the
governance log carries the file's sha256 (tools/measure.py seal); training/data/INDEX.json lists every example file with
its sha256 and counts, its sha256 sealed too; tools/make_training.py regenerates INDEX.json byte for byte; no example in
any train.jsonl touches a reserved article (target, candidates, or any source id); every answer is data (JSON)."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
HELD = ROOT / "law/TRAIN-HELD-OUT.json"
DATA = ROOT / "training/data"
TASKS = {"escolha_passagem", "texto_vigente", "nota_dr", "remissao", "regra_tipada"}


def newest_seal():
    seals = []
    for line in (ROOT / "governance/events.jsonl").read_text(encoding="utf-8").splitlines():
        ev = json.loads(line)
        if ev["action"] == "propose" and ev["assertion_type"] == "caso_referencia" and str(ev["assertion"]).startswith("selo:casos:"):
            seals.append(ev)
    assert seals, "no seal event in the log"
    return seals[-1]["payload"]


def test_train_held_out_declared_frozen_and_sealed():
    from engine.canon import canonical, sha256_text
    assert HELD.exists(), "law/TRAIN-HELD-OUT.json missing"
    doc = json.loads(HELD.read_text(encoding="utf-8"))
    assert doc["frozen_at"] and doc["definition"]["by_hash"] and doc["definition"]["by_b3"]["articles"]
    assert doc["sha256"] == sha256_text(canonical(doc["definition"]))
    assert newest_seal().get("train_held_out_sha256") == hashlib.sha256(HELD.read_bytes()).hexdigest()


def test_training_index_sealed_and_files_match():
    index = json.loads((DATA / "INDEX.json").read_text(encoding="utf-8"))
    assert set(index["tasks"]) == TASKS
    from engine.canon import canonical, sha256_text
    assert newest_seal().get("training_index_sha256") == sha256_text(canonical(index))
    for rel, meta in index["files"].items():
        assert hashlib.sha256((DATA / rel).read_bytes()).hexdigest() == meta["sha256"], rel


def test_no_train_example_touches_a_reserved_article():
    doc = json.loads(HELD.read_text(encoding="utf-8"))
    reserved = set(doc["reserved_articles"])
    article_of = json.loads((DATA / "ARTICLE-OF.json").read_text(encoding="utf-8"))
    total = 0
    for f in sorted(DATA.glob("*/train.jsonl")):
        for line in f.read_text(encoding="utf-8").splitlines():
            ex = json.loads(line)
            total += 1
            assert ex["task"] in TASKS and {"id", "task", "prompt", "answer", "sources"} <= set(ex)
            json.loads(ex["answer"]) if isinstance(ex["answer"], str) else ex["answer"]
            for s in ex["sources"]:
                art = article_of.get(s.split("@")[0])
                assert art not in reserved, (ex["id"], s, art)
    assert 0 < total <= 40000


def test_generator_rederives_index(tmp_path):
    import subprocess
    import sys
    subprocess.run([sys.executable, str(ROOT / "tools/make_training.py"), "generate", "--out", str(tmp_path)], check=True, cwd=ROOT)
    assert (tmp_path / "INDEX.json").read_bytes() == (DATA / "INDEX.json").read_bytes()
