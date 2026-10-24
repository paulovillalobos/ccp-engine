"""Phase 3, D0 — red until the three debts the phase-2 audit listed are cleared.

Done when: (1) the four EU delegated regulations of 2025 (thresholds) have passages with offsets, extracted by a
versioned EUR-Lex extractor, with an entra_em_vigor vigencia, and the threshold words are in the passage text; (2) the
six codes structure@1 could not read (CC, CPPT, CSC, CT, Lei 98/97, CRCSPSS) have their articles as passages, by a
second, versioned layout; (3) at least 90 % of the CCP's references that name an article of another act resolve to a
passage of that act (Portuguese acts: the EU directives are not captured), and law/COVERAGE.md says so."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
EU = {"norma:eu-2025-2152": "140 000 EUR", "norma:eu-2025-2150": "432 000 EUR", "norma:eu-2025-2151": "5 404 000 EUR", "norma:eu-2025-2487": "432 000 EUR"}
CODES = {"norma:cc": 2000, "norma:cppt": 250, "norma:csc": 500, "norma:ct": 500, "norma:lei-98-1997": 100, "norma:crcspss": 250}


def repo_store():
    from engine.store import Store
    return Store([ROOT / "law", ROOT / "rules", ROOT / "governance"]).load()


def current(store, type_):
    out = {}
    for o in store.objects[type_]:
        if o["id"] not in out or o["revision"] > out[o["id"]]["revision"]:
            out[o["id"]] = o
    return out


def test_eu_threshold_regulations_are_structured_by_a_versioned_extractor():
    s = repo_store()
    passages = current(s, "passagem")
    vig = current(s, "vigencia")
    for nid, words in EU.items():
        norma = s.current(nid)
        raws = [s.current(r) for r in norma["source"]["raw"]]
        assert any(r and r["text"] and r["text"]["extractor"].startswith("eurlex-html@") for r in raws), nid
        ps = [p for p in passages.values() if p["norma"] == nid]
        assert any(p["kind"] == "artigo" for p in ps), nid
        assert any(words in p["versions"][-1]["text"] for p in ps), (nid, words)
        assert any(v["altered_by"] == nid and v["effect"] == "entra_em_vigor" for v in vig.values()), nid


def test_the_six_codes_have_their_articles_as_passages():
    s = repo_store()
    counts = {}
    for p in current(s, "passagem").values():
        if p["kind"] == "artigo" and ".q" not in p["id"]:
            counts[p["norma"]] = counts.get(p["norma"], 0) + 1
    short = {nid: counts.get(nid, 0) for nid in CODES if counts.get(nid, 0) < CODES[nid]}
    assert short == {}, short


def test_remissoes_naming_an_article_resolve_to_a_passage():
    from tools import coverage
    s = repo_store()
    rep = coverage.remissoes_report(s)
    # Portuguese acts only: the EU directives the CCP names are not captured in this phase (11 measured on 2026-10-24;
    # the first draft of this test counted the 16 EU references too and asked for 20)
    assert rep["with_artigo_pt"] >= 10, rep["with_artigo_pt"]
    assert rep["resolved_pt"] / rep["with_artigo_pt"] >= 0.9, {k: rep[k] for k in ("with_artigo_pt", "resolved_pt")}
    assert (ROOT / "law/COVERAGE.md").read_text(encoding="utf-8") == coverage.render(s)
