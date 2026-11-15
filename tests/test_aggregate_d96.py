"""D96: agregada rules over BASE's records (engine/aggregate.py, engine/evaluate.py), the declared special regime and
special-sector buyer (engine/rules.regime_blocks), the invitation dates of db/run_engine.py, the declared facts of
db/declared.py and protocol 0.7 of the reading (tools/read_rules_v3.py). Made-up contracts; no network."""
import copy
import datetime
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path[:0] = [str(ROOT), str(ROOT / "tools"), str(ROOT / "db")]
from engine import aggregate as agg  # noqa: E402
from engine import evaluate as ev  # noqa: E402
from engine import rules as rules_mod  # noqa: E402
from helpers import one  # noqa: E402

COUNTED = ["ccp:art19.c", "ccp:art19.d", "ccp:art20.1.c", "ccp:art20.1.d"]


def rule(value=150000, comparator="lt", conditions=None):
    return {"id": "regra:ccp:teste-agregada@v1", "revision": 1, "type": "agregada", "norma": "norma:ccp", "applies_to": ["proc"],
            "conditions": conditions if conditions is not None else [{"field": "tipo_procedimento", "op": "eq", "value": "consulta_previa"},
                                                                       {"field": "tipo_contrato", "op": "eq", "value": "obras"}],
            "exceptions": [], "valid_from": "2018-01-01", "valid_to": None, "title": "t", "jurisdiction": "PT",
            "passages": [{"passage": "ccp:art113.2", "version": "2018-01-01", "quote": "q", "offsets": {"start": 0, "end": 1}},
                         {"passage": "ccp:art19.c", "version": "2018-01-01", "quote": "q", "offsets": {"start": 0, "end": 1}}],
            "params": {"window": {"length": 3, "unit": "anos_economicos", "anchor": "data_envio_convite"}, "group_key": ["adjudicante", "adjudicatario"],
                       "counts": {"fundamento_em": COUNTED},
                       "aggregate": {"field": "preco_contratual", "op": "sum", "comparator": comparator, "value": value},
                       "completeness_threshold": {"ratio": 1.0, "measured_over": "janela", "decided_by": "evento:1"}}, "readings": [], "state": "settled"}


def rec(i, proc, price, dadj="2024-03-01", sup=("509000001",), fund="Artigo 19.º, alínea c) do Código dos Contratos Públicos", adj=("500000001",), dcel=None):
    import fundamento
    return {"id": i, "raw": f"raw:base-contratos:contrato:{i}", "proc": proc, "adjudicante": list(adj), "adjudicatarios": list(sup), "preco": price,
            "fund": fund, "fundp": fundamento.passages(fund) if fund else [], "dadj": dadj, "dcel": dcel or dadj, "dpub": dcel or dadj}


def test_sums_only_what_surely_counts_and_names_every_contract():
    idx = agg.contracts_of([
        rec(1, 900, 100000.0, "2023-02-01"),                       # counts
        rec(2, 901, 60000.0, "2025-01-10"),                        # counts
        rec(3, 902, 500000.0, "2020-05-01"),                       # before the window (2022-01-01)
        rec(4, 903, 70000.0, "2025-02-01", fund="Artigo 24.º, n.º 1, alínea c) do Código dos Contratos Públicos"),  # another basis
        rec(5, 904, 9000.0, "2025-02-02", sup=("509000002",)),     # another supplier
        rec(6, 905, 1000.0, "2025-02-03", sup=("509000001", "509000003")),  # a consortium: uncertain
        rec(7, 999, 120000.0, "2025-06-01"),                       # the procedure itself
        rec(8, 906, 5000.0, "2025-07-01"),                         # after the anchor
    ])
    g = agg.group_sums(rule(), idx, 999, "500000001", "2025-05-01")
    assert [c["id"] for c in g["sure"]] == ["1", "2"] and g["sum_min"] == 160000.0
    assert [c["id"] for c in g["maybe"]] == ["6"] and g["sum_max"] == 161000.0
    assert g["window"] == ["2023-01-01", "2025-05-01"] and all(c["url"].endswith(c["id"]) for c in g["sure"])
    assert rules_mod.aggregate_result(rule()["params"], g) == "nao_cumpre"
    assert rules_mod.aggregate_result(rule(200000)["params"], g) == "cumpre"
    assert rules_mod.aggregate_result(rule(160500)["params"], g) is None  # the consortium decides: not decidable


def test_an_undated_adjudication_is_uncertain_unless_its_signing_is_before_the_window():
    idx = agg.contracts_of([rec(1, 900, 100.0, dadj=None, dcel="2021-12-01"), rec(2, 901, 100.0, dadj=None, dcel="2024-01-05"), rec(3, 999, 1.0)])
    g = agg.group_sums(rule(), idx, 999, "500000001", "2025-05-01")
    assert g["sure"] == [] and [c["id"] for c in g["maybe"]] == ["2"]


def test_evaluate_names_the_sum_and_keeps_the_contracts_on_the_verdict():
    manifest = one("manifesto", "exemplo")
    unit = {"id": "proc:base:idproc-999", "revision": 1, "kind": "proc"}
    facts = [{"id": f"facto:x:{k}", "revision": 1, "recorded_at": "2025-06-01T00:00:00Z", "unit": unit["id"], "field": k, "value": v,
              "origin": {"raw": "raw:base-contratos:contrato:7"}, "adapter": "adaptador:base-contratos@1", "valid_at": "2025-06-01", "known_at": "2025-06-02T00:00:00Z"}
             for k, v in (("tipo_procedimento", "consulta_previa"), ("tipo_contrato", "obras"), ("fundamento_passagens", ["ccp:art19.c"]))]
    idx = agg.contracts_of([rec(1, 900, 100000.0, "2023-02-01"), rec(2, 901, 60000.0, "2025-01-10"), rec(7, 999, 120000.0, "2025-06-01")])
    r = rule()
    g = agg.group_sums(r, idx, 999, "500000001", "2025-05-01")
    v = ev.evaluate(unit, [r], facts, "2025-06-02T00:00:00Z", "2025-06-01", manifest=manifest, aggregates={r["id"]: g}, rules_at="2025-05-01")[0]
    assert v["result"] == "nao_cumpre" and v["citation"]["passage"] == "ccp:art113.2"
    assert v["aggregate"]["sum_min"] == 160000.0 and [c["id"] for c in v["aggregate"]["sure"]] == ["1", "2"]
    assert "160000.00" in v["detail"] and "lt 150000" in v["detail"]
    v = ev.evaluate(unit, [r], facts, "2025-06-02T00:00:00Z", "2025-06-01", manifest=manifest, aggregates={}, rules_at="2025-05-01")[0]
    assert (v["result"], v["reason"]) == ("nao_avaliado", "facto_ausente")
    other = [dict(f, value=["ccp:art24.1.c"]) if f["field"] == "fundamento_passagens" else f for f in facts]
    assert ev.evaluate(unit, [r], other, "2025-06-02T00:00:00Z", "2025-06-01", manifest=manifest, aggregates={r["id"]: g}, rules_at="2025-05-01") == []


def limiar():
    return {"id": "regra:ccp:limiar-x@v1", "revision": 1, "type": "limiar", "norma": "norma:ccp", "conditions": [], "params": {"threshold": {"field": "preco_base", "comparator": "lt", "value": 150000, "currency": "EUR"}}}


def test_a_declared_special_regime_or_sector_buyer_is_not_judged():
    assert rules_mod.regime_blocks(limiar(), {"regime_declarado": ["ccp"]}) is None
    assert rules_mod.regime_blocks(limiar(), {"regime_declarado": ["ccp", "lei-30-2021"]}) is None  # an act named beside the Code
    reason, detail = rules_mod.regime_blocks(limiar(), {"regime_declarado": ["lei-30-2021"]})
    assert reason == "regra_ausente" and "lei-30-2021" in detail
    reason, detail = rules_mod.regime_blocks(limiar(), {"atividade_setor_especial": "rail"})
    assert reason == "facto_ausente" and "setores_especiais" in detail
    prazo = dict(limiar(), type="prazo_minimo")
    assert rules_mod.regime_blocks(prazo, {"atividade_setor_especial": "Serviços ferroviários"}) is None
    sector_rule = dict(limiar(), conditions=[{"field": "setores_especiais", "op": "eq", "value": True}])
    assert rules_mod.regime_blocks(sector_rule, {"atividade_setor_especial": "Água"}) is None


def test_evaluate_turns_a_blocked_limit_into_not_assessed():
    manifest = one("manifesto", "exemplo")
    unit = {"id": "proc:base:idproc-1", "revision": 1, "kind": "proc"}
    r = dict(limiar(), applies_to=["proc"], exceptions=[], valid_from="2018-01-01", valid_to=None, title="t", jurisdiction="PT",
             passages=[{"passage": "ccp:art19.c", "version": "2018-01-01", "quote": "q", "offsets": {"start": 0, "end": 1}}], readings=[], state="settled")
    def f(k, v):
        return {"id": f"facto:y:{k}", "revision": 1, "recorded_at": "2025-01-01T00:00:00Z", "unit": unit["id"], "field": k, "value": v, "origin": {"raw": "raw:x"},
                "adapter": "adaptador:base-contratos@1", "valid_at": "2025-01-01", "known_at": "2025-01-01T00:00:00Z"}
    facts = [f("preco_base", 350000), f("regime_declarado", ["lei-30-2021"])]
    v = ev.evaluate(unit, [r], facts, "2025-01-01T00:00:00Z", "2025-01-01", manifest=manifest)[0]
    assert (v["result"], v["reason"]) == ("nao_avaliado", "regra_ausente") and "facto:y:regime_declarado" in v["facts_used"]
    v = ev.evaluate(unit, [r], facts[:1], "2025-01-01T00:00:00Z", "2025-01-01", manifest=manifest)[0]
    assert v["result"] == "nao_cumpre"


def test_invitation_days_cover_each_turn_of_the_economic_year():
    import importlib.util
    spec = importlib.util.spec_from_file_location("db_run_engine", ROOT / "db/run_engine.py")  # not tools/run_engine.py
    run_engine = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(run_engine)
    d = run_engine.invitation_days(datetime.date(2024, 6, 1), datetime.date(2025, 3, 1))
    assert d == [datetime.date(2024, 6, 1), datetime.date(2024, 12, 31), datetime.date(2025, 1, 1), datetime.date(2025, 3, 1)]


def test_declared_regime_names_the_code_by_its_decrees():
    import declared
    assert declared.regime_acts("Código dos Contratos Públicos (DL111-B/2017) e Lei n.º 30/2021, de 21.05") == ["ccp", "lei-30-2021"]
    assert declared.regime_acts("Código dos Contratos Públicos ( DL 111-B/2017 )") == ["ccp"]
    assert declared.regime_acts("Medidas Especiais de Contratação Pública (Lei n.º 30/2021, de 21.05)") == ["lei-30-2021"]
    sectors = {"503933813": {"rail": {"notices": 3, "first": {"raw": "raw:ted:aviso:123-2019", "date": "2019-01-02"}, "last": {"raw": "raw:ted:aviso:9-2024", "date": "2024-01-01"}}}}
    fs = declared.facts([{"id": 5, "proc": 77, "raw": "raw:base-contratos:contrato:5", "adjudicante": ["503933813"],
                          "regime": "Código dos Contratos Públicos (DL111-B/2017) e Lei n.º 30/2021, de 21.05", "dpub": "2024-02-02"}], "2026-11-13T00:00:00Z", sectors)
    by = {f["field"]: f for f in fs}
    assert by["regime_declarado"]["value"] == ["ccp", "lei-30-2021"] and by["regime_declarado"]["origin"]["raw"] == "raw:base-contratos:contrato:5"
    assert by["atividade_setor_especial"]["value"] == "rail" and by["atividade_setor_especial"]["origin"]["raw"] == "raw:ted:aviso:123-2019"


def test_protocol_07_agregada_example_and_its_broken_copies():
    import read_rules_v3 as v3
    assert v3.selftest_07()
    assert "agregada" in v3.render(v3.EXAMPLE_07_CTX | {"date": "2026-10-01", "place": [], "label": "Artigo 902.º", "heading": "h", "items": [], "refs": []}, "agregada", v3.V07)
    a = copy.deepcopy(v3.EXAMPLE_07)
    a["regras"].append(copy.deepcopy(a["regras"][0]))
    assert any("repete" in e for e in v3.check(a, v3.EXAMPLE_07_CTX, "agregada", v3.V07))
    assert v3.window_lengths("no ano económico em curso e nos dois anos económicos anteriores") == {3}


def test_protocol_06_prompts_do_not_change():
    import read_rules_v3 as v3
    assert "agregada" not in v3.STATIC_06 and "agregada" in v3.STATIC_07


def test_what_the_procedure_s_own_documents_say_decides_d97():
    manifest = one("manifesto", "exemplo")
    unit = {"id": "proc:base:idproc-2", "revision": 1, "kind": "proc"}
    r = dict(limiar(), applies_to=["proc"], exceptions=[], valid_from="2018-01-01", valid_to=None, title="t", jurisdiction="PT",
             passages=[{"passage": "ccp:art19.c", "version": "2018-01-01", "quote": "q", "offsets": {"start": 0, "end": 1}}], readings=[], state="settled")

    def run(doc):
        facts = [{"id": f"facto:z:{k}", "revision": 1, "recorded_at": "2025-01-01T00:00:00Z", "unit": unit["id"], "field": k, "value": v, "origin": {"raw": "raw:x"},
                  "adapter": "adaptador:base-contratos@1", "valid_at": "2025-01-01", "known_at": "2025-01-01T00:00:00Z"}
                 for k, v in (("preco_base", 350000), ("fundamento_nos_documentos", doc)) if v is not None]
        return ev.evaluate(unit, [r], facts, "2025-01-01T00:00:00Z", "2025-01-01", manifest=manifest)
    v = run({"estado": "verificado", "citacao": "nos termos da alínea c) do artigo 19.º", "documento": "BASE: contrato.pdf", "pagina": 2, "url": "u"})[0]
    assert v["result"] == "nao_cumpre" and v["prova_documental"]["citacao"].startswith("nos termos") and "facto:z:fundamento_nos_documentos" in v["facts_used"]
    assert run({"estado": "outra_base", "citacao": "critério material"}) == []
    v = run({"estado": "medidas_especiais", "citacao": "consulta prévia simplificada", "documento": "d"})[0]
    assert (v["result"], v["reason"]) == ("nao_avaliado", "regra_ausente") and rules_mod.DOCS_RULE in v["detail"]
    v = run({"estado": "nao_identificado", "lidos": 2})[0]
    assert (v["result"], v["reason"]) == ("nao_avaliado", "facto_ausente") and v["detail"].startswith("não decidível: fundamento não identificado")
    assert run(None)[0]["result"] == "nao_cumpre" and "prova_documental" not in run(None)[0]
