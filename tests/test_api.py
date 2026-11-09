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
