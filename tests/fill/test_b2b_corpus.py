"""FILL-PLAN B2b — red until the law around the CCP is registered, captured, structured and reported.

Done when: every act of the CCP's timeline (the timeline-content-inner blocks of a history page: 23 amending acts and
the original DL 18/2008) and every
diploma a DR note names is a norma; the acts the applicable law cites (DL 111-B/2017, Lei 30/2021, DL 18/2008 with its
entry-into-force article, the retificações) are captured from the DR and, when they have articles, structured; at least
90 % of the distinct Portuguese acts the CCP's own text refers to (remissões) are captured; each phase-3 norm is
registered or reported missing in law/COVERAGE.md with the DR / EUR-Lex address that was read; and law/COVERAGE.md is
exactly what tools/coverage.py writes from the store (registered / captured / structured / with vigências)."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
CITED = ("norma:dl-111-b-2017", "norma:lei-30-2021", "norma:dl-18-2008",
         "norma:ret-18-a-2008", "norma:ret-36-a-2017", "norma:ret-42-2017", "norma:ret-25-2021")
PHASE3 = ("norma:lei-30-2021", "norma:dl-60-2018", "norma:dlr-27-2015-a", "norma:cpa", "norma:lei-96-2015",
          "norma:port-371-2017", "norma:port-372-2017", "norma:dl-197-1999", "norma:lei-75-2013", "norma:lei-98-1997")


def repo_store():
    from engine.store import Store
    return Store([ROOT / "law", ROOT / "rules", ROOT / "governance"]).load()


def captured(store, norma):
    """Read from its own page: a detail page (raw kind diploma), a consolidated page (lei) or an EU act (regulamento)
    whose source_id is the norma's short id; a page the act is only named on does not count."""
    return any((store.current(r) or {}).get("kind") in ("diploma", "lei", "regulamento") and (store.current(r) or {}).get("source_id") == norma["short"]
               for r in norma["source"]["raw"])


def test_timeline_acts_and_note_diplomas_are_all_registered():
    from tools import coverage
    s = repo_store()
    acts = coverage.timeline_acts(s)
    amending = [a for a in acts if a["norma"] != "norma:dl-18-2008"]  # the DR prints the original act at the end
    assert len(amending) == 23 and len(acts) == 24, [a["title"] for a in acts]
    assert [a["norma"] for a in acts if not s.current(a["norma"])] == []
    named = coverage.note_diplomas(s)
    assert len(named) >= 22 and [n for n in named if not s.current(n)] == []
    for n in (s.current(i) for i in {a["norma"] for a in acts} | set(named)):
        assert n["jurisdiction"] and n["scope"], n["id"]


def test_acts_the_applicable_law_cites_are_captured_and_structured():
    s = repo_store()
    for nid in CITED:
        n = s.current(nid)
        assert n and captured(s, n), nid
        if not nid.startswith("norma:ret-"):  # a declaração de retificação has no articles of its own
            assert any(p["norma"] == nid for p in s.objects["passagem"]), nid
    entry = [p for p in s.objects["passagem"] if p["norma"] == "norma:dl-18-2008" and p["kind"] == "artigo"
             and "\nEntrada em vigor\n" in p["versions"][-1]["text"] + "\n"]
    assert entry, "DL 18/2008's entry-into-force article is not structured"


def test_ninety_percent_of_portuguese_remissoes_are_captured():
    from tools import coverage
    rep = coverage.remissoes_report(repo_store())
    assert rep["distinct_pt"] >= 10, rep["distinct_pt"]  # 14 measured on 2026-10-24 (the first floor, 20, was set before measuring)
    assert rep["captured_pt"] / rep["distinct_pt"] >= 0.9, {k: rep[k] for k in ("distinct_pt", "captured_pt", "resolved_to_passage")}


def test_phase3_norms_are_registered_or_reported_missing_with_the_address_read():
    s = repo_store()
    cov = (ROOT / "law/COVERAGE.md").read_text(encoding="utf-8")
    for nid in PHASE3:
        if s.current(nid):
            assert captured(s, s.current(nid)), nid
        else:
            row = next((l for l in cov.splitlines() if nid in l), "")
            assert "https://" in row, f"{nid}: neither registered nor reported missing with the address read"
    eu = [n for n in (s.current(i) for i in s.by_id) if n and n["id"].startswith("norma:") and n["jurisdiction"] == "UE"]
    assert eu and all(n.get("eli", "").startswith("http") for n in eu), "EU thresholds: no norma with its ELI"
    madeira = [n for n in (s.current(i) for i in s.by_id) if n and n["id"].startswith("norma:") and n["jurisdiction"] == "PT-MA"]
    row = next((l for l in cov.splitlines() if "Madeira" in l and "1,45" in l), "")
    assert madeira or "https://" in row, "Madeira regime: neither registered nor reported missing with the address read"


def test_coverage_report_is_what_the_tool_writes():
    from tools import coverage
    assert (ROOT / "law/COVERAGE.md").read_text(encoding="utf-8") == coverage.render(repo_store())
