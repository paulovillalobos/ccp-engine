"""Store: append-only, bitemporal. Nothing overwritten; two clocks never mixed."""
import json
import shutil

import pytest

from engine.store import Store, WriteError, Writer, facts_of, query
from tests.helpers import ROOT, VALID


@pytest.fixture
def store_dir(tmp_path):
    shutil.copytree(VALID, tmp_path / "s")
    return tmp_path / "s"


def test_load_counts_every_type_and_no_errors():
    s = Store([VALID]).load()
    assert s.errors == []
    assert all(s.objects[t] for t in s.objects), [t for t, v in s.objects.items() if not v]
    assert len(s.events) >= 20 and s.principals


def test_append_refuses_same_id_and_revision(store_dir):
    w = Writer(store_dir)
    r = w.store.current("regra:ccp:limiar-ajuste-direto-bens@v1")
    with pytest.raises(WriteError, match="already exists"):
        w.append(dict(r))


def test_revise_creates_next_revision_and_keeps_the_old(store_dir):
    w = Writer(store_dir)
    r = w.store.current("regra:ccp:limiar-ajuste-direto-bens@v1")
    new = w.revise(r, {"title": "retitled"}, "2026-10-25T00:00:00Z")
    assert new["revision"] == 2 and new["supersedes"] == 1
    reloaded = Store([store_dir]).load()
    assert reloaded.errors == [] and len(reloaded.revisions(r["id"])) == 2
    assert reloaded.revisions(r["id"])[0]["title"] == r["title"]


def test_revision_gap_is_refused(store_dir):
    w = Writer(store_dir)
    r = w.store.current("regra:ccp:limiar-ajuste-direto-bens@v1")
    bad = dict(r, revision=3, supersedes=2, recorded_at="2026-10-25T00:00:00Z")
    with pytest.raises(WriteError, match="must follow"):
        w.append(bad)


def test_mark_stale_is_a_new_revision_not_a_delete(store_dir):
    w = Writer(store_dir)
    l = w.store.current("link:fx-2")
    stale = w.mark_stale(l, "name match was wrong", "2026-10-25T00:00:00Z")
    assert stale["stale"] is True and stale["revision"] == 2
    s = Store([store_dir]).load()
    assert s.errors == []
    assert query(s, "link", known_at="2026-10-24T23:00:00Z") and any(x["id"] == "link:fx-2" for x in query(s, "link", known_at="2026-10-24T23:00:00Z"))
    assert not any(x["id"] == "link:fx-2" for x in query(s, "link", known_at="2026-10-25T00:00:00Z"))
    assert any(x["id"] == "link:fx-2" for x in query(s, "link", known_at="2026-10-25T00:00:00Z", include_stale=True))


def test_query_separates_known_at_from_valid_at():
    s = Store([VALID]).load()
    facts = query(s, "facto", known_at="2026-10-24T18:40:00Z")           # before the base-api capture
    assert all(f["origin"]["raw"] != "raw:base-api:contrato:99000001" for f in facts) and facts
    facts = query(s, "facto", known_at="2026-10-24T19:00:00Z", valid_at="2026-10-02")  # before the facts were valid
    assert facts == []
    rules = query(s, "regra", valid_at="2026-09-30")
    assert rules == []                                                     # every fixture rule is valid from 2026-10-01
    passages = query(s, "passagem", valid_at="2026-10-01")
    assert passages and all(len(p["versions"]) == 1 for p in passages)


def test_facts_of_walks_up_to_the_procedure():
    s = Store([VALID]).load()
    assert {f["field"] for f in facts_of(s, "contrato:base:99000001")} >= {"preco_base", "prazo_propostas_dias"}
