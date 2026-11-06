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


# D83: the count from the settled contagem_prazo rules in force, as the law reads (CPA art. 87.º through CCP art. 470.º)
from tests.test_calendario import TEXT as HOLIDAYS  # noqa: E402


def counting_rule(rid, field, aspecto, valor, conditions=()):
    r = rule(prazo(), rid, list(conditions), deadline_field=field, aspecto=aspecto, valor=valor)
    r["type"] = "contagem_prazo"
    for k in ("minimum_days", "counted_from", "usual_days"):
        r["params"].pop(k, None)
    return r


URGENT = {"field": "tipo_procedimento", "op": "eq", "value": "concurso_publico_urgente"}
LAW = [counting_rule("regra:teste:cpa87b@v1", "todos", "primeiro_dia", "nao_conta"),
       counting_rule("regra:teste:cpa87c@v1", "todos", "fins_de_semana", "suspende"),
       counting_rule("regra:teste:cpa87f@v1", "todos", "termo", "transfere"),
       counting_rule("regra:teste:ccp470-3@v1", "prazo_propostas_dias", "fins_de_semana", "continuo"),
       counting_rule("regra:teste:ccp470-2@v1", "prazo_propostas_dias", "primeiro_dia", "conta", [URGENT])]


def run_law(rules, **values):
    out = ev.evaluate(UNIT, rules, facts(**values), KNOWN, VALID_AT, manifest=one("manifesto", "exemplo"), calendar=lambda y: HOLIDAYS)
    return {v["rule"]["id"]: v for v in out}


def test_counting_rules_make_no_verdict_of_their_own():
    assert set(run_law([thirty()] + LAW, **DATES)) == {"regra:teste:trinta@v1"}


def test_proposals_continuous_first_day_out():
    v = run_law([thirty()] + LAW, **DATES)["regra:teste:trinta@v1"]
    assert "=26 <" in v["detail"] and "regra:teste:ccp470-3@v1" in v["detail"] and "regra:teste:cpa87b@v1" in v["detail"]


def test_urgent_tender_counts_the_first_day():
    v = run_law([thirty()] + LAW, tipo_procedimento="concurso_publico_urgente", **DATES)["regra:teste:trinta@v1"]
    assert "=27 <" in v["detail"] and "regra:teste:ccp470-2@v1" in v["detail"]


def test_a_term_on_a_holiday_moves_to_the_next_working_day():
    v = run_law([thirty()] + LAW, data_publicacao_anuncio="2026-03-04", data_limite_propostas="2026-04-03")["regra:teste:trinta@v1"]
    assert v["result"] == "cumpre" and "=33 >=" in v["detail"]  # Good Friday 3 Apr → Monday 6 Apr: 33 days, not 30


def test_other_deadlines_skip_weekends_and_holidays():
    cand = rule(prazo(), "regra:teste:cand@v1", [], minimum_days=5, deadline_field="prazo_candidaturas_dias", counted_from="data_publicacao_anuncio")
    v = run_law([cand] + LAW[:3], data_publicacao_anuncio="2026-04-02", data_limite_candidaturas="2026-04-09")["regra:teste:cand@v1"]
    assert "=4 <" in v["detail"]  # 3 Apr Good Friday, 4–5 weekend: 6, 7, 8, 9 April


def test_an_aspect_no_rule_gives_blocks_the_count():
    v = run_law([thirty()] + LAW[:2] + LAW[3:], **DATES)["regra:teste:trinta@v1"]
    assert v["reason"] == "regra_ausente" and "termo" in v["detail"]
