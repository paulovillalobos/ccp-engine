from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def test_directories_exist():
    for d in ["schemas", "engine", "governance", "law", "rules", "fixtures", "tests", "tools", "adapters", "data"]:
        assert (ROOT / d).is_dir(), d


def test_readme_states_invariants_and_boundary():
    text = (ROOT / "README.md").read_text(encoding="utf-8")
    assert text.count("\n1. **") == 1 and "12. **" in text
    assert "Ownership boundary" in text and "Extractor" in text
