"""The gate bites: valid fixtures pass, every broken overlay fails with its EXPECT code, no model or network in the code."""
from pathlib import Path

import verify

ROOT = Path(__file__).resolve().parent.parent


def test_valid_fixtures_pass():
    store, out = verify.check_store([ROOT / "fixtures/valid"])
    assert out == [], out
    assert sum(len(v) for v in store.objects.values()) >= 20 and len(store.events) >= 1


def test_empty_stores_pass():
    for roots in (verify.STORES["repo"], verify.STORES["data"]):
        _, out = verify.check_store(roots)
        assert out == [], out


def test_every_broken_overlay_is_refused_with_its_code():
    results = verify.run_broken(ROOT / "fixtures/valid", ROOT / "fixtures/broken")
    assert len(results) == 29, [r[0] for r in results]
    for name, expect, codes in results:
        assert expect and expect <= codes, (name, expect, codes)
    assert {next(iter(e)) for _, e, _ in results} == {f"I{n:02d}" for n in range(1, 13)} | {"RED", "MAN", "STATE", "TIME", "GRAPH", "FIELD", "BENCH", "TRAIN"}


def test_code_guard_is_clean_and_catches_a_model_import(tmp_path):
    assert verify.check_code() == []
    bad = tmp_path / "m.py"
    bad.write_text("from anthropic import Anthropic\nimport requests\n")
    codes = {c for c, _ in verify.check_code([tmp_path])}
    assert codes == {"I03", "I10"}


def test_verify_main_exit_code_is_zero():
    assert verify.main(["verify.py"]) == 0
