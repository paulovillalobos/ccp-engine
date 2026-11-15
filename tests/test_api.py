"""D90: the API over the Postgres store refuses what is not an id, pages by unit, and answers a verdict with its rule,
citation and manifest. The database is replaced by a fake: nothing here calls the network."""
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path[:0] = [str(ROOT / "db"), str(ROOT / "tools")]
import api  # noqa: E402
import serve  # noqa: E402

DOC = {"rule": {"id": "regra:teste:x@v1", "revision": 2}, "result": "nao_cumpre", "reason": None, "detail": "preco_base=350000 lt 150000",
       "citation": {"passage": "ccp:art19.c", "version": "2018-01-01", "quote": "c) Consulta prévia…"}, "facts_used": ["facto:a"],
       "valid_at": "2026-05-05", "known_at": "2026-11-06T20:14:46Z",
       "manifest": {"law_version": "lei:ccp@2026-05-04", "package": "pacote:ccp@2026-05-04", "code": {"commit": "d1dfa2b32", "engine_version": "ccp-engine-0.1"},
                    "log_head": "d0b9"}}


class FakeStore:
    def current(self, rid):
        return None


class FakeConn:
    def __init__(self, rows):
        self.rows, self.seen = rows, []

    def execute(self, q, args=()):
        self.seen.append((q, args))
        rows = self.rows
        return type("R", (), {"fetchall": lambda s: rows, "fetchone": lambda s: None})()


def test_ids_are_checked_before_any_query(monkeypatch):
    monkeypatch.setattr(api, "db", lambda: pytest.fail("no query for a bad id"))
    for bad in ("drop table", "proc:base:", "contrato:base:1", "proc:base:" + "x" * 100):
        with pytest.raises(serve.ApiError) as e:
            api.procedimento(bad)
        assert e.value.status == 400
    for bad in ({"resultado": ["x"]}, {"limite": ["a"]}, {"apos": ["; select"]}, {"regra": ["' or 1=1"]}):
        with pytest.raises(serve.ApiError):
            api.page(bad)
    with pytest.raises(serve.ApiError):
        api.entidade_veredictos("12345")


def test_a_page_is_bounded_and_ordered(monkeypatch):
    conn = FakeConn([("proc:base:idproc-1", DOC), ("proc:base:idproc-2", DOC)])
    monkeypatch.setattr(api, "db", lambda: conn)
    monkeypatch.setattr(api, "latest_run", lambda: {"id": "corrida:t"})
    monkeypatch.setattr(serve, "STORE", FakeStore())
    out = api.veredictos({"resultado": ["nao_cumpre"], "limite": ["2"]})
    q, args = conn.seen[0]
    assert "order by v.unit limit %s" in q and args[-1] == 2 and "nao_cumpre" in args
    assert out["seguinte"] == "proc:base:idproc-2" and len(out["veredictos"]) == 2
    assert api.page({"limite": ["10000"]})[3] == api.PAGE_MAX


def test_a_verdict_carries_its_proof(monkeypatch):
    monkeypatch.setattr(serve, "STORE", FakeStore())
    v = api.verdict_out(DOC)
    assert (v["resultado"], v["passagem"], v["versao"]) == ("nao_cumpre", "ccp:art19.c", "2018-01-01")
    assert v["manifesto"]["commit"] == "d1dfa2b32" and v["manifesto"]["registo"] == "d0b9" and v["factos_usados"] == ["facto:a"]


def test_report_steps_come_from_the_engine_functions():
    rule = {"type": "limiar", "conditions": [{"field": "tipo_contrato", "op": "in", "value": "obras"}],
            "passages": [{"passage": "ccp:art19.c"}], "params": {"threshold": {"field": "preco_base", "comparator": "lt", "value": 150000}}}
    steps = api._steps(rule, {"tipo_contrato": "obras", "preco_base": 350000, "fundamento_passagens": ["ccp:art19.c"]}, "nao_cumpre",
                       "preco_base=350000 lt 150000; início entre 2025-05-04 e 2026-05-04")
    assert [s["ok"] for s in steps] == [True, True, True, False] and steps[-1]["decide"] and steps[-1]["valor"] == 350000
    assert steps[1]["teste"].startswith("início entre")
    other = api._steps(rule, {"tipo_contrato": "obras", "preco_base": 9, "fundamento_passagens": ["ccp:art20.1.d"]}, "cumpre", "x")
    assert other[1]["ok"] is False  # a basis naming another passage: the limit does not count (D88)
    with pytest.raises(serve.ApiError):
        api.relatorio("proc:base:../x")


def test_an_aggregate_verdict_shows_and_steps_through_each_contract(monkeypatch):
    """D96: the contracts a cumulative limit summed reach the API and the report's steps, each with its BASE link."""
    monkeypatch.setattr(serve, "STORE", FakeStore())
    agg = {"group": {"adjudicante": "500000001", "adjudicatario": "509000001"}, "window": ["2023-01-01", "2025-05-01"], "anchor": "2025-05-01",
           "sum_min": 160000.0, "sum_max": 160000.0, "maybe": [],
           "sure": [{"id": "1", "url": "https://www.base.gov.pt/Base4/pt/detalhe/?type=contratos&id=1", "data_adjudicacao": "2023-02-01",
                     "fundamento": "Artigo 19.º, alínea c)", "preco_contratual": 100000.0},
                    {"id": "2", "url": "https://www.base.gov.pt/Base4/pt/detalhe/?type=contratos&id=2", "data_adjudicacao": "2025-01-10",
                     "fundamento": "Artigo 19.º, alínea c)", "preco_contratual": 60000.0}]}
    out = api.verdict_out({**DOC, "aggregate": agg})
    assert out["agregado"]["sum_min"] == 160000.0 and len(out["agregado"]["sure"]) == 2
    rule = {"id": "regra:x@v1", "type": "agregada", "conditions": [], "passages": [{"passage": "ccp:art113.2"}, {"passage": "ccp:art19.c"}],
            "params": {"counts": {"fundamento_em": ["ccp:art19.c"]}, "aggregate": {"field": "preco_contratual", "op": "sum", "comparator": "lt", "value": 150000}}}
    steps = api._steps(rule, {"fundamento_passagens": ["ccp:art19.c"]}, "nao_cumpre", "x", agg)
    assert [s.get("url") for s in steps if s.get("url")] == [c["url"] for c in agg["sure"]]
    assert steps[-1]["decide"] and steps[-1]["valor"] == 160000.0 and not steps[-1]["ok"]
