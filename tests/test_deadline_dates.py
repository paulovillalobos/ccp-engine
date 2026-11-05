"""D80: a deadline the facts state as two dates. The engine counts the days from the rule's own counted_from date to the
deadline's date only with a settled counting rule; without one the verdict is regra_ausente (no count the code chose),
and a stated number of days is read as before."""
from engine import evaluate as ev
from tests.helpers import one
from tests.test_most_specific import KNOWN, UNIT, VALID_AT, facts, prazo, rule

COUNT_EXCL = {"id": "regra:teste:contagem@v1", "first_day_counts": False}
COUNT_INCL = {"id": "regra:teste:contagem-b@v1", "first_day_counts": True}


def run(rules, counting=None, **values):
    out = ev.evaluate(UNIT, rules, facts(**values), KNOWN, VALID_AT, manifest=one("manifesto", "exemplo"), counting=counting)
    return {v["rule"]["id"]: v for v in out}


def thirty(counted_from="data_publicacao_anuncio"):
    return rule(prazo(), "regra:teste:trinta@v1", [], minimum_days=30, deadline_field="prazo_propostas_dias", counted_from=counted_from)


DATES = {"data_publicacao_anuncio": "2026-01-02", "data_limite_propostas": "2026-01-28"}  # 26 days apart


def test_two_dates_without_a_counting_rule_are_not_assessed():
    v = run([thirty()], **DATES)["regra:teste:trinta@v1"]
    assert v["result"] == "nao_avaliado" and v["reason"] == "regra_ausente"
    assert "counting rule" in v["detail"]


def test_two_dates_with_a_counting_rule_give_a_verdict_that_names_it():
    v = run([thirty()], COUNT_EXCL, **DATES)["regra:teste:trinta@v1"]
    assert v["result"] == "nao_cumpre" and "prazo_propostas_dias=26 < 30" in v["detail"]
    assert "regra:teste:contagem@v1" in v["detail"]
    assert set(v["facts_used"]) == {"facto:teste:data_limite_propostas", "facto:teste:data_publicacao_anuncio"}


def test_the_first_day_is_the_counting_rule_s():
    assert "=27 <" in run([thirty()], COUNT_INCL, **DATES)["regra:teste:trinta@v1"]["detail"]


def test_the_rule_s_counted_from_picks_the_date():
    v = run([thirty("data_envio_anuncio")], COUNT_EXCL, **DATES)["regra:teste:trinta@v1"]
    assert v["result"] == "nao_avaliado" and v["reason"] == "facto_ausente" and "data_envio_anuncio" in v["detail"]
    w = run([thirty("data_envio_anuncio")], COUNT_EXCL, data_envio_anuncio="2025-12-29", **DATES)["regra:teste:trinta@v1"]
    assert w["result"] == "cumpre" and "=30 >= 30" in w["detail"]


def test_an_unstated_start_does_not_count_from_any_date():
    v = run([thirty("nao_indicado")], COUNT_EXCL, **DATES)["regra:teste:trinta@v1"]
    assert v["result"] == "nao_avaliado" and v["reason"] == "facto_ausente"


def test_stated_days_are_read_as_before():
    v = run([thirty()], prazo_propostas_dias=31, **DATES)["regra:teste:trinta@v1"]
    assert v["result"] == "cumpre" and "counting rule" not in v["detail"]
