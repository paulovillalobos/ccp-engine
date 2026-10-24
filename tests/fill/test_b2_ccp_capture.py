"""FILL-PLAN B2 — red until the consolidated CCP is captured with its validity notes.

Done when: law/ holds norma:ccp and norma:dl-177-2026 with their raw captures (bytes hashed); at least 589 passages of
kind artigo under norma:ccp; at least 607 vigencia records derived from the DR notes, each quoting its note at offsets in
the raw text (verify I01/I02 re-derive them); vigente(2026-09-30) and vigente(2026-10-01) differ exactly in the passages
whose vigencia names norma:dl-177-2026 with valid_from 2026-10-01; and that set is not empty."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent


def repo_store():
    from engine.store import Store
    return Store([ROOT / "law", ROOT / "rules", ROOT / "governance"]).load()


def test_ccp_norms_and_passages_are_captured():
    s = repo_store()
    assert s.errors == []
    assert s.current("norma:ccp") and s.current("norma:dl-177-2026")
    artigos = [p for p in s.objects["passagem"] if p["norma"] == "norma:ccp" and p["kind"] == "artigo"]
    assert len(artigos) >= 589, len(artigos)
    assert len(s.objects["vigencia"]) >= 607, len(s.objects["vigencia"])


def test_vigente_differs_exactly_as_the_dl_177_notes_say():
    from engine.vigente import vigente
    s = repo_store()
    before, after = vigente(s, "2026-09-30"), vigente(s, "2026-10-01")
    changed = {pid for pid in set(before) | set(after) if before.get(pid) != after.get(pid)}
    expected = {v["passage"] for v in s.objects["vigencia"] if v["altered_by"] == "norma:dl-177-2026" and v["valid_from"] == "2026-10-01"}
    assert expected, "no DL 177/2026 notes dated 2026-10-01 were derived"
    assert changed == expected, {"only_in_vigente": sorted(changed - expected)[:10], "only_in_notes": sorted(expected - changed)[:10]}


def test_verify_rederives_the_law_store():
    import verify
    store, out = verify.check_store([ROOT / "law", ROOT / "rules", ROOT / "governance"])
    assert out == [], out[:5]
    assert store.objects["passagem"] and store.objects["raw"], "law/ is still empty"
