"""evaluate() reproduces the fixture verdicts and answers nao_avaliado with a typed reason wherever it cannot say more."""
import pytest

from engine import evaluate as ev
from engine.store import Store, facts_of
from tests.helpers import VALID, load_all, one

KNOWN = "2026-10-24T19:30:00Z"
VALID_AT = "2026-10-03"


def setup():
    s = Store([VALID]).load()
    manifest = one("manifesto", "exemplo")
    rules = [r for r in load_all("regra") if r["type"] in ("seletor_regime", "limiar", "prazo_minimo", "agregada", "jurisdicao", "procedimento_admissivel", "proibicao", "conteudo_obrigatorio")]
    coverage = {(a["id"], c["period"]): (c["captured"] / c["expected"] if c["expected"] else None) for a in load_all("adaptador") for c in a["coverage"]}
    return s, manifest, rules, coverage


def by_rule(verdicts):
    return {v["rule"]["id"]: v for v in verdicts}


def test_reproduces_the_fixture_verdicts():
    s, manifest, rules, coverage = setup()
    proc = s.current("proc:base:FX-2026-000001")
    out = by_rule(ev.evaluate(proc, rules, facts_of(s, proc["id"]), KNOWN, VALID_AT, manifest=manifest, conflicts=load_all("conflito"),
                              assertions=load_all("afirmacao"), entities=load_all("entidade"), documents=load_all("documento"), coverage=coverage))
    for fx in load_all("veredicto"):
        if fx["unit"] != proc["id"]:
            continue
        got = out[fx["rule"]["id"]]
        assert (got["result"], got["reason"], got["citation"]) == (fx["result"], fx["reason"], fx["citation"]), fx["id"]
        assert set(got["facts_used"]) == set(fx["facts_used"]), fx["id"]
        assert got["id"] == fx["id"] and got["assertions_compared"] == fx["assertions_compared"]
        assert got["manifest"] == fx["manifest"]
    assert out["regra:ccp:procedimentos-admissiveis@v1"]["result"] == "cumpre"
    assert out["regra:ccp:proibicao-fracionamento@v1"]["reason"] == "facto_ausente"
    assert out["regra:ccp:programa-indica-prazo-e-criterios@v1"]["reason"] == "documento_sem_texto"


def test_aggregate_answers_coverage_before_facts():
    s, manifest, rules, coverage = setup()
    contrato = s.current("contrato:base:99000001")
    fx = one("veredicto", "limite-acumulado-art113-99000001")
    out = by_rule(ev.evaluate(contrato, rules, facts_of(s, contrato["id"]), KNOWN, VALID_AT, manifest=manifest, coverage=coverage, entities=load_all("entidade")))
    got = out[fx["rule"]["id"]]
    assert (got["result"], got["reason"]) == ("nao_avaliado", "cobertura_insuficiente") and got["id"] == fx["id"]
    full = {k: 1.0 for k in coverage}
    out = by_rule(ev.evaluate(contrato, rules, facts_of(s, contrato["id"]), KNOWN, VALID_AT, manifest=manifest, coverage=full))
    assert out[fx["rule"]["id"]]["reason"] == "facto_ausente"
    out = by_rule(ev.evaluate(contrato, rules, facts_of(s, contrato["id"]), KNOWN, VALID_AT, manifest=manifest, coverage=full, aggregates={fx["rule"]["id"]: 25000}))
    assert out[fx["rule"]["id"]]["result"] == "nao_cumpre"


def test_without_the_selector_fact_everything_is_not_assessed():
    s, manifest, rules, coverage = setup()
    proc = s.current("proc:base:FX-2026-000001")
    facts = [f for f in facts_of(s, proc["id"]) if f["field"] != "data_inicio_procedimento"]
    out = ev.evaluate(proc, rules, facts, KNOWN, VALID_AT, manifest=manifest, coverage=coverage)
    assert out and all(v["result"] == "nao_avaliado" and v["reason"] == "facto_ausente" for v in out)
    assert all("data_inicio_procedimento" in v["detail"] for v in out)


def test_natural_person_is_never_named_and_manifest_must_be_complete():
    s, manifest, rules, coverage = setup()
    proc = s.current("proc:base:FX-2026-000001")
    out = ev.evaluate(proc, rules, facts_of(s, proc["id"]), KNOWN, VALID_AT, manifest=manifest, entities=load_all("entidade"))
    for v in out:
        for e in v["entities"]:
            assert not (e["type"] == "pessoa_singular" and "name" in e)
    with pytest.raises(ev.EvaluateError):
        ev.evaluate(proc, rules, [], KNOWN, VALID_AT, manifest=dict(manifest, adapters=[]))


def test_jurisdiction_multiplies_thresholds():
    s, manifest, rules, coverage = setup()
    proc = s.current("proc:base:FX-2026-000001")
    facts = [f for f in facts_of(s, proc["id"]) if f["origin"]["raw"] != "raw:base-api:contrato:99000001"]
    extra = dict(facts[0], id="facto:x:territorio", field="territorio", value="PT-AC")
    price = dict(facts[0], id="facto:x:preco", field="preco_base", value=25000)
    out = by_rule(ev.evaluate(proc, rules, facts + [extra, price], KNOWN, VALID_AT, manifest=manifest))
    assert out["regra:ccp:limiar-ajuste-direto-bens@v1"]["result"] == "cumpre"   # 25000 < 20000 * 1.45
    out = by_rule(ev.evaluate(proc, rules, facts + [price], KNOWN, VALID_AT, manifest=manifest))
    assert out["regra:ccp:limiar-ajuste-direto-bens@v1"]["result"] == "nao_cumpre"
