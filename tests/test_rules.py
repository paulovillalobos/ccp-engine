"""Rules as data: eight types, required params, evaluation order, package hash, diff rebuild."""
import pytest

from engine import rules
from tests.helpers import load_all, one


def test_eight_types_with_required_params():
    assert len(rules.RULE_TYPES) == 8 and set(rules.RULE_TYPES) == set(rules.REQUIRED_PARAMS)
    for r in load_all("regra"):
        rules.check(r)


def test_unknown_type_or_missing_param_is_refused():
    r = dict(load_all("regra")[0], type="costume")
    with pytest.raises(rules.RuleError):
        rules.check(r)
    agg = next(r for r in load_all("regra") if r["type"] == "agregada")
    bad = dict(agg, params={k: v for k, v in agg["params"].items() if k != "completeness_threshold"})
    with pytest.raises(rules.RuleError, match="completeness_threshold"):
        rules.check(bad)


def test_order_selector_then_jurisdiction_then_simple_then_aggregate():
    staged = rules.order(load_all("regra"))
    assert [r["type"] for r in staged["seletor"]] == ["seletor_regime"]
    assert [r["type"] for r in staged["jurisdicao"]] == ["jurisdicao"]
    assert [r["type"] for r in staged["agregada"]] == ["agregada"]
    assert len(staged["simples"]) == 5


def test_applies_distinguishes_false_from_unreadable():
    lim = next(r for r in load_all("regra") if r["type"] == "limiar")
    assert rules.applies(lim, {"tipo_procedimento": "ajuste_direto", "tipo_contrato": "bens"}) == (True, None)
    assert rules.applies(lim, {"tipo_procedimento": "concurso_publico", "tipo_contrato": "bens"}) == (False, None)
    assert rules.applies(lim, {"tipo_procedimento": "ajuste_direto"}) == (None, "tipo_contrato")
    assert rules.applies(lim, {"tipo_procedimento": rules.Conflict("conflito:x"), "tipo_contrato": "bens"}) == (None, "tipo_procedimento")


def test_package_hash_and_diff_match_the_fixtures():
    regras = {r["id"]: r for r in load_all("regra")}
    for pk in load_all("pacote"):
        built = rules.package(pk["id"], pk["law_version"], [regras[r["id"]] for r in pk["rules"]], pk["log_head"], pk["built_at"], pk["recorded_at"])
        assert built["hash"] == pk["hash"] and built["rules"] == pk["rules"]
    d = one("diff", "ccp-2026-09-30..2026-10-01")
    a, b = one("pacote", "ccp-2026-09-30"), one("pacote", "ccp-2026-10-01")
    built = rules.diff(a, b, regras)
    assert built["by_rule"] == d["by_rule"] and built["by_consumer_field"] == d["by_consumer_field"]
    assert {c["change"] for c in built["by_rule"]} == {"added"}
