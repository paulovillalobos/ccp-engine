"""The contract: every schema compiles; every valid fixture validates against the schema its directory names."""
import json
from pathlib import Path

import pytest

from engine import schema

ROOT = Path(__file__).resolve().parent.parent
VALID = ROOT / "fixtures/valid"


def test_every_schema_compiles():
    for stem in list(schema.TYPES) + ["evento", "principals", "defs"]:
        if stem != "defs":
            schema.validator(stem)
    assert len(list(schema.SCHEMAS.glob("*.schema.json"))) == len(schema.TYPES) + 3  # defs, evento, principals


def test_one_valid_fixture_per_object_type():
    for type_ in schema.TYPES:
        files = list((VALID / type_).glob("*.json"))
        assert files, f"no valid fixture for {type_}"
        for f in files:
            obj = json.loads(f.read_text(encoding="utf-8"))
            assert schema.validate(type_, obj) == [], f.name
            if type_ != "manifesto":
                assert schema.type_of(obj) == type_, (f.name, schema.type_of(obj))


def test_governance_fixture_validates():
    principals = json.loads((VALID / "governance/principals.json").read_text(encoding="utf-8"))
    assert schema.validate("principals", principals) == []
    lines = (VALID / "governance/events.jsonl").read_text(encoding="utf-8").splitlines()
    assert len(lines) >= 1
    for line in lines:
        assert schema.validate("evento", json.loads(line)) == []


@pytest.mark.parametrize("type_,bad", [
    ("veredicto", {"result": "nao_avaliado", "reason": None}),
    ("veredicto", {"result": "cumpre", "reason": "facto_ausente"}),
    ("veredicto", {"result": "talvez"}),
])
def test_verdict_reason_enumeration_is_closed(type_, bad):
    base = json.loads(next((VALID / "veredicto").glob("*.json")).read_text(encoding="utf-8"))
    obj = dict(base, **bad)
    assert schema.validate(type_, obj) != []


def test_rule_type_enumeration_has_ten_members_and_fixtures_cover_them():  # D71 prazo_maximo, D83 contagem_prazo
    defs = json.loads((schema.SCHEMAS / "defs.schema.json").read_text(encoding="utf-8"))
    types = defs["$defs"]["rule_type"]["enum"]
    assert len(types) == 10
    seen = {json.loads(f.read_text(encoding="utf-8"))["type"] for f in (VALID / "regra").glob("*.json")}
    assert seen == set(types)


def test_natural_person_name_is_refused_in_a_verdict():
    base = json.loads(next((VALID / "veredicto").glob("*.json")).read_text(encoding="utf-8"))
    obj = json.loads(json.dumps(base))
    obj["entities"] = [{"id": "ent:nif:200000000", "type": "pessoa_singular", "role": "adjudicatario", "name": "X"}]
    assert schema.validate("veredicto", obj) != []


def test_machine_approval_is_refused_by_the_event_schema():
    ev = json.loads((VALID / "governance/events.jsonl").read_text(encoding="utf-8").splitlines()[0])
    ev.update(action="approve", principal="leitor:b", reason="x")
    assert schema.validate("evento", ev) != []
