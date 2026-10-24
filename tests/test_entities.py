import pytest

from engine import entities as en


def test_candidate_and_nif_ids_are_stable():
    assert en.candidate_id("FR", "NAMSA — Société Anonyme") == "ent:cand:FR:namsa-societe-anonyme"
    assert en.candidate_id("PT", "Município de Évora") == en.candidate_id("PT", "municipio de evora")
    assert en.nif_id("500000000") == "ent:nif:500000000"
    with pytest.raises(ValueError):
        en.nif_id("12")


def test_link_lifecycle_never_deletes():
    l = en.propose_link("link:t", "alias:base:x", "ent:nif:500000000", "ai:amalia-9b", "name_ai", {"source_field": "nome", "value": "X"}, "2026-10-24T00:00:00Z", "evento:9", "2026-10-24T00:00:00Z")
    assert l["state"] == "proposed" and l["revision"] == 1
    s = en.settle(l, "2026-10-25T00:00:00Z")
    assert s["state"] == "settled" and s["revision"] == 2 and s["supersedes"] == 1 and l["state"] == "proposed"
    st = en.mark_stale(s, "wrong person", "2026-10-26T00:00:00Z")
    assert st["stale"] and st["state"] == "stale" and st["revision"] == 3
    assert en.links_to([l, s, st], "ent:nif:500000000") == []
    assert en.links_to([l, s, st], "ent:nif:500000000", known_at="2026-10-25T00:00:00Z")[0]["state"] == "settled"


def test_proponent_and_event_are_required_and_merge_does_not_exist():
    with pytest.raises(ValueError):
        en.propose_link("link:t", "a", "b", None, "person", {"source_field": "x", "value": "y"}, "2026-10-24T00:00:00Z", None, "2026-10-24T00:00:00Z")
    with pytest.raises(ValueError):
        en.propose_link("link:t", "a", "b", "ai:amalia-9b", "name_ai", {"source_field": "x", "value": "y"}, "2026-10-24T00:00:00Z", None, "2026-10-24T00:00:00Z")
    with pytest.raises(NotImplementedError):
        en.merge("ent:nif:1", "ent:nif:2")
