"""D92: the law watch holds the rules of a changed article, records differences once, and never reads a failed check as
"no change". The database and the network are replaced by fakes."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path[:0] = [str(ROOT / "db"), str(ROOT), str(ROOT / "tools")]
import law_watch  # noqa: E402
import run_engine  # noqa: E402

RULE = {"id": "regra:x", "revision": 2, "passages": [{"passage": "ccp:art19.c"}]}


def test_a_rule_waits_when_its_article_or_a_part_of_it_changed():
    assert run_engine.cites_pending(RULE, ["ccp:art19"])           # the whole article changed
    assert run_engine.cites_pending(RULE, ["ccp:art19.c"])         # the passage itself
    assert run_engine.cites_pending(RULE, ["ccp:art19.c.i"])       # a part of it
    assert not run_engine.cites_pending(RULE, ["ccp:art190", "ccp:art1"])  # another article, even with the same digits
    assert not run_engine.cites_pending(RULE, [])
    assert run_engine.rules_signature([RULE]) == ["regra:x#2"]


class Conn:
    def __init__(self, open_):
        self.open, self.sql = list(open_), []

    def execute(self, q, args=()):
        self.sql.append((q, args))
        rows = [(p, "2026-11-09") for p in self.open] if "lei_pendente" in q else []
        return type("R", (), {"fetchall": lambda s: rows, "fetchone": lambda s: None})()

    def commit(self):
        pass


def test_a_difference_is_opened_once_and_closed_when_it_is_gone():
    conn = Conn(["ccp:art37", "ccp:art61"])
    new, gone = law_watch.record(conn, ["ccp:art61", "ccp:art405"], "sha")
    assert new == ["ccp:art405"] and gone == ["ccp:art37"]
    inserts = [a for q, a in conn.sql if q.startswith("insert")]
    assert inserts == [("ccp:art405", "sha")]


def test_a_failed_read_alerts_and_is_never_no_change(monkeypatch):
    import capture_dr_consolidated as cap
    sent = []
    monkeypatch.setattr(cap, "render", lambda url, ms: (_ for _ in ()).throw(SystemExit("render failed: 1")))
    monkeypatch.setattr(law_watch, "alert", lambda title, text, *a, **k: sent.append(title) or True)
    conn = Conn([])
    out = law_watch.check(conn)
    assert out["ok"] is False and "render failed" in out["erro"]
    assert any("lei_vigia" in q and a[0].startswith("SystemExit") for q, a in conn.sql)
    assert sent and "no pude leer" in sent[0]
    assert not any("lei_alteracao" in q for q, _ in conn.sql)  # nothing closed: a failed read changes no pending article


def test_no_topic_no_push(monkeypatch):
    monkeypatch.setattr(law_watch, "topic", lambda: None)
    assert law_watch.alert("t", "m") is False
