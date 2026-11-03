"""D67: the rules factory names its own principal (TOOL) and checks, before record, recheck or withdraw writes anything, that
it is the current registration with the file's hash. Round 9's first record stopped half-way: TOOL still named
ferramenta:rule-factory@16, retired when @17 was registered, and the log refused the invalidation that follows a settled
«não tipável»."""
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT)); sys.path.insert(0, str(ROOT / "tools"))
import rule_factory  # noqa: E402


def test_tool_is_the_current_registration():
    rule_factory.tool_is_current()


def test_a_retired_version_is_refused(monkeypatch):
    monkeypatch.setattr(rule_factory, "TOOL", "ferramenta:rule-factory@16")
    with pytest.raises(SystemExit):
        rule_factory.tool_is_current()
