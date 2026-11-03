"""D66: the most specific of the applying rules gives the verdict (product_rule:regra-mais-especifica), and a limiar
compares with the comparator its passage writes (lt, le, gt, ge)."""
import copy

from engine import evaluate as ev
from tests.helpers import load_all, one

KNOWN = "2026-10-24T19:30:00Z"
VALID_AT = "2026-10-03"
UNIT = {"id": "proc:base:TESTE-0001", "type": "proc"}


def facts(**values):
    return [{"id": f"facto:teste:{k}", "revision": 1, "recorded_at": KNOWN, "unit": UNIT["id"], "field": k, "value": v,
             "origin": {"raw": "raw:teste", "field": k}, "adapter": "adaptador:teste@1", "valid_at": VALID_AT, "known_at": KNOWN}
            for k, v in values.items()]


def rule(base, rid, conditions, **params):
    r = copy.deepcopy(base)
    r["id"], r["conditions"] = rid, conditions
    r["params"] = {**r["params"], **params}
    return r


def run(rules, **values):
    out = ev.evaluate(UNIT, rules, facts(**values), KNOWN, VALID_AT, manifest=one("manifesto", "exemplo"))
    return {v["rule"]["id"]: v for v in out}


def prazo():
    return next(r for r in load_all("regra") if r["type"] == "prazo_minimo")


def limiar():
    return next(r for r in load_all("regra") if r["type"] == "limiar")


JOUE = {"field": "publicado_joue", "op": "eq", "value": True}
URG = {"field": "urgencia_fundamentada", "op": "eq", "value": True}
SET = {"field": "setores_especiais", "op": "eq", "value": True}


def test_a_reduction_prevails_over_its_base():
    base = rule(prazo(), "regra:teste:base@v1", [JOUE], minimum_days=30)
    reduced = rule(prazo(), "regra:teste:reducao@v1", [JOUE, URG], minimum_days=15)
    out = run([base, reduced], publicado_joue=True, urgencia_fundamentada=True, prazo_propostas_dias=20)
    assert set(out) == {"regra:teste:reducao@v1"} and out["regra:teste:reducao@v1"]["result"] == "cumpre"
    out = run([base, reduced], publicado_joue=True, urgencia_fundamentada=False, prazo_propostas_dias=20)
    assert set(out) == {"regra:teste:base@v1"} and out["regra:teste:base@v1"]["result"] == "nao_cumpre"


def test_two_rules_neither_more_specific_disagree_into_a_conflict():
    a = rule(prazo(), "regra:teste:urgencia@v1", [JOUE, URG], minimum_days=15)
    b = rule(prazo(), "regra:teste:setores@v1", [JOUE, SET], minimum_days=25)
    out = run([a, b], publicado_joue=True, urgencia_fundamentada=True, setores_especiais=True, prazo_propostas_dias=20)
    assert {v["result"] for v in out.values()} == {"nao_avaliado"} and {v["reason"] for v in out.values()} == {"conflito"}
    out = run([a, b], publicado_joue=True, urgencia_fundamentada=True, setores_especiais=True, prazo_propostas_dias=30)
    assert {v["result"] for v in out.values()} == {"cumpre"}  # the same result: no conflict to report


def test_a_limiar_reads_its_comparator():
    for comparator, limit, result in (("lt", 101, "cumpre"), ("lt", 100, "nao_cumpre"), ("le", 100, "cumpre"), ("gt", 100, "nao_cumpre"),
                                      ("gt", 99, "cumpre"), ("ge", 100, "cumpre"), ("ge", 101, "nao_cumpre")):
        r = rule(limiar(), "regra:teste:limiar@v1", [{"field": "tipo_procedimento", "op": "eq", "value": "ajuste_direto"}],
                 threshold={"field": "valor_estimado", "comparator": comparator, "value": limit, "currency": "EUR"})
        out = run([r], tipo_procedimento="ajuste_direto", valor_estimado=100)
        assert out["regra:teste:limiar@v1"]["result"] == result, (comparator, limit)
