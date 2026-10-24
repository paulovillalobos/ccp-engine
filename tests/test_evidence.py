"""READ and SEAL: reader answers and measurement annotations are evidence anchored in the log (DECISIONS D39)."""
import hashlib
import json
import shutil

from engine.governance import Log
from engine.store import Store
import verify
from tests.helpers import VALID

AT = "2026-10-25T10:00:00Z"


def _store(tmp_path):
    shutil.copytree(VALID, tmp_path / "s")
    return tmp_path / "s"


def test_reader_answer_must_hash_to_the_logged_sha256(tmp_path):
    root = _store(tmp_path)
    answer = '{"passages": ["ccp:art20.1"]}'
    sha = hashlib.sha256(answer.encode("utf-8")).hexdigest()
    d = root / "governance/readings/ccp--teste-at-v1"
    d.mkdir(parents=True)
    (d / "leitor-a.json").write_text(json.dumps({"at": AT, "sha256": sha, "answer": answer}), encoding="utf-8")
    Log(root / "governance").propose("leitor:a", "regra", "regra:ccp:teste@v1", {"chosen_passages": ["ccp:art20.1"], "answer_sha256": sha}, AT)
    out = []
    verify.check_readings(Store([root]).load(), out)
    assert out == []
    (d / "leitor-a.json").write_text(json.dumps({"at": AT, "sha256": sha, "answer": answer + " "}), encoding="utf-8")
    out = []
    verify.check_readings(Store([root]).load(), out)
    assert [c for c, _ in out] == ["READ"]


def test_annotations_need_a_seal_and_cannot_change_after_it(tmp_path):
    root = _store(tmp_path)
    casos = root / "governance/readings/casos/m-01"
    casos.mkdir(parents=True)
    (casos / "leitor-a.json").write_text('{"answer": "cumpre"}', encoding="utf-8")
    held = tmp_path / "HELD-OUT.json"
    held.write_text('{"frozen_at": "2026-10-24"}', encoding="utf-8")
    out = []
    verify.check_seal(Store([root]).load(), out, held_out=held)
    assert [c for c, _ in out] == ["SEAL"]  # files without a seal
    index = {"files": {"m-01/leitor-a.json": hashlib.sha256((casos / "leitor-a.json").read_bytes()).hexdigest()}}
    (casos.parent / "INDEX.json").write_text(json.dumps(index, sort_keys=True), encoding="utf-8")
    Log(root / "governance").propose("ferramenta:ccp-link@1", "caso_referencia", "selo:casos:1",
                                     {"index_sha256": hashlib.sha256(verify.canonical_json(index).encode("utf-8")).hexdigest(), "held_out_sha256": hashlib.sha256(held.read_bytes()).hexdigest(), "files": 1}, AT)
    out = []
    verify.check_seal(Store([root]).load(), out, held_out=held)
    assert out == []
    held.write_text('{"frozen_at": "2026-10-25"}', encoding="utf-8")
    out = []
    verify.check_seal(Store([root]).load(), out, held_out=held)
    assert [c for c, _ in out] == ["SEAL"]
    held.write_text('{"frozen_at": "2026-10-24"}', encoding="utf-8")
    (casos / "leitor-a.json").write_text('{"answer": "nao_cumpre"}', encoding="utf-8")
    out = []
    verify.check_seal(Store([root]).load(), out, held_out=held)
    assert [c for c, _ in out] == ["SEAL"]


def test_rule_content_is_the_log_replay(tmp_path):
    root = _store(tmp_path)
    f = root / "regra/ccp-limiar-ajuste-direto-bens.json"
    o = json.loads(f.read_text(encoding="utf-8"))
    o["passages"] = o["passages"][:1]
    f.write_text(json.dumps(o, ensure_ascii=False), encoding="utf-8")
    out = []
    verify.check_rule_content(Store([root]).load(), out)
    assert [c for c, _ in out] == ["STATE"]
