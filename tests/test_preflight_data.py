"""D67: the pre-flight gate refuses data-v12's training rows for the defects the audit found (reports/DATA-AUDIT-v12.md), and
data-v13's generator keeps what the gate asks: neutral titles that change no reading, the schema in the factory's order."""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT)); sys.path.insert(0, str(ROOT / "tools"))
import make_rule_readings_v12 as v12  # noqa: E402
import make_rule_readings_v13 as v13  # noqa: E402
import preflight_data as pf  # noqa: E402
import read_rules_v3 as v3  # noqa: E402


def test_the_gate_refuses_data_v12_for_what_the_audit_found():
    rep = pf.gate(ROOT / "training/data-v12/regra_lida/train.jsonl")
    assert not rep["ok"]
    # every check fails but one: v12's answers followed the factory's key order; its stored schemas did not
    assert [c["check"] for c in rep["checks"] if c["ok"]] == ["order: answer keys follow the schema"]


def test_neutral_titles_name_nothing():
    for chain in v13.NEUTRAL:
        for t in chain:
            assert v13.names_something(t) is None, t


def test_neutral_titles_change_no_reading():
    n = 0
    for pattern in ("batch-*.jsonl", "alvo-*.jsonl"):
        for ex in v12.load(pattern):
            if ex.get("lugar"):
                continue
            before, errs = v12.problems(ex)
            if errs:
                continue
            after, errs2 = v12.problems(v13.housed(ex))
            assert not errs2, (ex["id"], errs2[:1])
            assert v3.canonical(after[0]) == v3.canonical(before[0]), ex["id"]
            assert after[1]["alvo"] == before[1]["alvo"]
            n += 1
    assert n > 900


def test_rows_keep_the_factory_schema_order():
    ex = v13.housed(next(iter(v12.load("batch-01.jsonl"))))
    (answer, ctx), errs = v12.problems(ex)
    assert not errs
    row = json.loads(v13.dump([v12.row(ex, ctx, answer)]))
    assert json.dumps(row["schema"], ensure_ascii=False) == json.dumps(v3.schema(ctx, ex["tipo"]), ensure_ascii=False)
    assert pf.key_order_ok(json.loads(row["answer"]), row["schema"])


def test_old_spelling_changes_no_reading():
    n = 0
    for pattern in ("batch-*.jsonl", "alvo-*.jsonl", "v3-*.jsonl"):
        for ex in v12.load(pattern):
            ex = v13.housed(ex)
            old = v13.aged(ex)
            if old is ex:
                continue
            before, errs = v12.problems(ex)
            if errs:
                continue
            after, errs2 = v12.problems(old)
            assert not errs2, (ex["id"], errs2[:1])
            assert v3.canonical(after[0]) == v3.canonical(before[0]), ex["id"]
            n += 1
    assert n > 250
