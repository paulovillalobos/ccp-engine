"""FILL-PLAN B3 — red until the v0 rules are in the governance log with two readings each.

Done when: rules/regra/ holds (as the replay of governance/events.jsonl) at least one seletor_regime citing a passage of
norma:dl-177-2026 (art. 7.º), limiar rules citing ccp:art19* and ccp:art20*, and prazo_minimo rules citing ccp:art135* or
ccp:art136*; every one of them has a citation that verify I02 confirms by offsets, at least two readings from distinct
families (amalia and reader-b), and a state; rules/pacote/ holds pacote:ccp@2026-10-01 naming them with a correct hash."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
EXPECTED = {
    "seletor_regime": ("dl-177-2026:art7",),
    "limiar": ("ccp:art19", "ccp:art20"),
    "prazo_minimo": ("ccp:art135", "ccp:art136"),
}


def test_v0_rules_exist_with_two_readings_and_verified_citations():
    from engine.store import Store
    import verify
    s = Store([ROOT / "law", ROOT / "rules", ROOT / "governance"]).load()
    rules = [r for r in verify.current_of(s, "regra").values()]
    for type_, prefixes in EXPECTED.items():
        matching = [r for r in rules if r["type"] == type_ and any(c["passage"].startswith(p) for c in r["passages"] for p in prefixes)]
        assert matching, f"no {type_} rule citing {prefixes}"
        for r in matching:
            families = {rd["family"] for rd in r["readings"]}
            assert len(families) >= 2, (r["id"], families)
            assert r["state"] in ("proposed", "ai_reviewed", "settled"), r["id"]
    out = []
    verify.check_citations(s, out)
    verify.check_governance(s, out)
    assert out == [], out[:5]
    assert any(pk["id"] == "pacote:ccp@2026-10-01" for pk in s.objects["pacote"])
