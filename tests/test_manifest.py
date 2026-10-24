import pytest

from engine import manifest as m
from tests.helpers import one


def test_fixture_manifest_is_complete_and_build_round_trips():
    fx = one("manifesto", "exemplo")
    assert m.is_complete(fx) == []
    built = m.build(fx["law_version"], fx["package"], fx["adapters"], fx["source_snapshots"], fx["code"], fx["log_head"], fx["produced_at"])
    assert built == fx and m.manifest_hash(built) == m.manifest_hash(fx)


def test_incomplete_is_named_and_refused():
    fx = one("manifesto", "exemplo")
    assert m.is_complete(dict(fx, adapters=[])) == ["adapters"]
    assert m.is_complete({k: v for k, v in fx.items() if k != "log_head"}) == ["log_head"]
    assert "code.commit" in m.is_complete(dict(fx, code={"repository": "r", "engine_version": "ccp-x"}))
    with pytest.raises(ValueError):
        m.build(fx["law_version"], fx["package"], [], fx["source_snapshots"], fx["code"], fx["log_head"], fx["produced_at"])
