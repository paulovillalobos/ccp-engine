"""The DR note grammar and the per-article history, against the real strings captured on 2026-10-24."""
import pytest

from engine import vigente
from engine.store import Store
from tests.helpers import ROOT

NOTES = [
    ("Alterado pelo/a Artigo 2.º do/a Decreto-Lei n.º 177/2026 - Diário da República n.º 172/2026, Série I de 2026-09-04, em vigor a partir de 2026-10-01.", "altera", "Decreto-Lei n.º 177/2026", "2026-10-01"),
    ("Retificado pelo/a Declaração de Retificação n.º 36-A/2017 - Diário da República n.º 209/2017, 2º Suplemento, Série I de 2017-10-30, em vigor a partir de 2018-01-01", "retifica", "Declaração de Retificação n.º 36-A/2017", "2018-01-01"),
    ("Alterado pelo/a Artigo 21.º do/a Lei n.º 30/2021 - Diário da República n.º 99/2021, Série I de 2021-05-21, em vigor a partir de 2021-06-20", "altera", "Lei n.º 30/2021", "2021-06-20"),
    ("NOTA: Retificado pelo/a Declaração de Rectificação n.º 18-A/2008 - Diário da República n.º 62/2008, 1º Suplemento, Série I de 2008-03-28, em vigor a partir de 2008-07-30", "retifica", "Declaração de Rectificação n.º 18-A/2008", "2008-07-30"),
]


@pytest.mark.parametrize("text,effect,diploma,valid_from", NOTES)
def test_parse_note_reads_the_real_strings(text, effect, diploma, valid_from):
    n = vigente.parse_note(text)
    assert n and (n["effect"], n["diploma"], n["valid_from"]) == (effect, diploma, valid_from)


def test_norma_slug():
    assert vigente.norma_slug("Decreto-Lei n.º 177/2026") == "dl-177-2026"
    assert vigente.norma_slug("Lei n.º 30/2021") == "lei-30-2021"
    assert vigente.norma_slug("Declaração de Retificação n.º 36-A/2017") == "ret-36-a-2017"
    assert vigente.norma_slug("Decreto Legislativo Regional n.º 27/2015/A") == "dlr-27-2015-a"


def law_text(source_id):
    s = Store([ROOT / "law"]).load()
    raw = next(r for r in s.objects["raw"] if r["source_id"] == source_id)
    return s.raw_text(raw)


def test_art20_history_gives_four_legal_versions_with_rectifications_folded():
    v = vigente.versions_from_history(law_text("ccp-art20"), "2008-07-30")
    assert [x["valid_from"] for x in v] == ["2008-07-30", "2012-08-11", "2018-01-01", "2026-10-01"]
    assert [x["valid_to"] for x in v] == ["2012-08-11", "2018-01-01", "2026-10-01", None]
    assert len(v[2]["rectified"]) == 2 and v[2]["note"]["diploma"] == "Declaração de Retificação n.º 42/2017"
    assert v[0]["note"] is None and v[-1]["note"]["diploma"] == "Decreto-Lei n.º 177/2026"
    assert all(x["label"] == "Artigo 20.º" and x["lines"] for x in v)


def test_art136_history_is_untouched_by_dl_177():
    v = vigente.versions_from_history(law_text("ccp-art136"), "2008-07-30")
    assert [x["valid_from"] for x in v] == ["2008-07-30", "2018-01-01", "2021-06-20"]
    assert all("177/2026" not in (x["note"] or {}).get("diploma", "") for x in v)


def test_consolidated_page_notes_all_parse():
    text = law_text("ccp")
    s = Store([ROOT / "law"]).load()
    raw = next(r for r in s.objects["raw"] if r["source_id"] == "ccp")
    from engine import extract
    hist = extract.dr_article_history((ROOT / "law" / raw["bytes"]).read_bytes())
    notes = [l for l in hist.splitlines() if l.startswith("NOTA: ")]
    assert len(notes) >= 607, len(notes)
    parsed = [vigente.parse_note(n) for n in notes]
    assert all(parsed), [n for n, p in zip(notes, parsed) if p is None][:3]
    assert sum(1 for p in parsed if p["effect"] == "revoga") >= 50
    assert sum(1 for p in parsed if p["valid_from"] is None) <= 4
    assert sum(1 for n in notes if "177/2026" in n) >= 200
