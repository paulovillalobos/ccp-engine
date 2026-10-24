"""FILL-PLAN B1 — red until the rjue modules are copied with their own version.

Done when: engine/sources.py, engine/structure.py, engine/passages.py, engine/vigente.py import; each declares VERSION
starting with "ccp-" and never mentions rjue; they expose the interfaces named in FILL-PLAN.md; tools/capture_dr_consolidated.py,
tools/serve.py and tools/package.sh exist; verify's code guard stays clean (tools may GET, never send)."""
import importlib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
INTERFACES = {
    "engine.sources": ["record_raw", "load_raw_text"],
    "engine.structure": ["structure"],
    "engine.passages": ["cite", "passage_text"],
    "engine.vigente": ["vigente", "notes_to_vigencias"],
}


def test_modules_exist_with_own_version_and_interfaces():
    for name, symbols in INTERFACES.items():
        mod = importlib.import_module(name)
        assert getattr(mod, "VERSION", "").startswith("ccp-"), name
        assert "rjue" not in Path(mod.__file__).read_text(encoding="utf-8").lower().replace("copied from rjue-engine", ""), f"{name}: leftover rjue naming"
        for s in symbols:
            assert callable(getattr(mod, s, None)), f"{name}.{s} missing"


def test_tools_exist():
    for rel in ("tools/capture_dr_consolidated.py", "tools/serve.py", "tools/package.sh"):
        assert (ROOT / rel).exists(), rel
    import verify
    assert verify.check_code() == []
