"""Governance log: chain, capabilities, human-only approval, two-family settlement, no self-review."""
import json
import shutil

import pytest

from engine import governance as gov
from tests.helpers import ROOT, VALID

AT = "2026-10-25T10:00:00Z"


@pytest.fixture
def log(tmp_path):
    shutil.copytree(VALID / "governance", tmp_path / "g")
    return gov.Log(tmp_path / "g")


def test_fixture_log_replays_clean_and_head_matches_the_packages(log):
    rp = log.replay()
    assert rp.errors == []
    assert rp.state_of("regra", "regra:ccp:limiar-ajuste-direto-bens@v1") == "settled"
    assert rp.state_of("regra", "regra:ccp:proibicao-fracionamento@v1") == "proposed"
    assert rp.state_of("product_rule", "product_rule:completude-agregadas") == "settled"
    assert rp.disputes["disputa:fx-1"]["state"] == "adjudicated"
    pk = json.loads((VALID / "pacote/ccp-2026-10-01.json").read_text(encoding="utf-8"))
    assert log.head() == pk["log_head"]


def test_reading_settles_only_by_blind_other_family(log):
    rid = "regra:ccp:teste@v1"
    log.propose("leitor:a", "regra", rid, {"chosen_passages": ["ccp:art20.1"]}, AT)
    assert log.replay().state_of("regra", rid) == "proposed"
    with pytest.raises(gov.GovernanceError, match="reviews its own"):
        log.review("leitor:a", "regra", rid, 1, "q", "blind", "uphold", AT)
    with pytest.raises(gov.GovernanceError, match="never approved by a pessoa"):
        log.approve("pessoa:paulo", "regra", rid, 1, "I like it", AT)
    log.review("leitor:b", "regra", rid, 1, "Blind: which passages?", "informed", "uphold", AT)
    assert log.replay().state_of("regra", rid) == "ai_reviewed"
    log.review("leitor:b", "regra", rid, 1, "Blind: which passages?", "blind", "uphold", AT)
    assert log.replay().state_of("regra", rid) == "settled"


def test_machines_never_approve_and_reasons_are_required(log):
    log.propose("extrator:a", "adaptador", "adaptador:x@1", {"source": "x"}, AT)
    with pytest.raises(gov.GovernanceError):
        log.approve("leitor:b", "adaptador", "adaptador:x@1", 1, "ok", AT)
    with pytest.raises(gov.GovernanceError):
        log.approve("pessoa:paulo", "adaptador", "adaptador:x@1", 1, "", AT)
    with pytest.raises(gov.GovernanceError, match="names revision"):
        log.approve("pessoa:paulo", "adaptador", "adaptador:x@1", 2, "ok", AT)
    log.approve("pessoa:paulo", "adaptador", "adaptador:x@1", 1, "Mapping reviewed field by field.", AT)
    assert log.replay().state_of("adaptador", "adaptador:x@1") == "settled"
    log.propose("pessoa:paulo", "product_rule", "product_rule:x", {"ratio": 0.8}, AT)
    assert log.replay().state_of("product_rule", "product_rule:x") == "proposed"   # a pessoa's proposal without a reason is not a decision
    with pytest.raises(gov.GovernanceError):
        log.propose("redator:a", "product_rule", "product_rule:y", {}, AT)         # a redator records nothing


def test_disputant_never_adjudicates_and_chain_is_append_only(log, tmp_path):
    n = len(log.events)
    log.dispute("pessoa:paulo", "veredicto:x", "disputa:t", "Looks wrong.", AT)
    with pytest.raises(gov.GovernanceError, match="own dispute"):
        log.adjudicate("pessoa:paulo", "disputa:t", "upheld", "Fine.", AT)
    with pytest.raises(gov.GovernanceError):
        log.adjudicate("leitor:b", "disputa:t", "upheld", "Fine.", AT)
    log.adjudicate("pessoa:revisor-fixture", "disputa:t", "overturned", "The dump value was a typo.", AT)
    assert len(log.events) == n + 2
    lines = (tmp_path / "g/events.jsonl").read_text(encoding="utf-8").splitlines()
    lines[3] = lines[3].replace("2026", "2025", 1)
    tampered = [(l, json.loads(l)) for l in lines]
    assert any(c == "I09" for c, _ in gov.replay(tampered, log.principals).errors)
    state = json.loads(log.write_state().read_text(encoding="utf-8"))
    assert state["head"] == log.head() and state["errors"] == []


def test_unregistered_principal_is_refused(log):
    with pytest.raises(gov.GovernanceError, match="not registered"):
        log.propose("leitor:c", "regra", "regra:ccp:z@v1", {}, AT)
