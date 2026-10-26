"""FILL-PLAN B5 (§8 measurement) — red until the figure exists with its interval and freeze date.

Done when: law/HELD-OUT.json declares the held-out set (by entity and period) with frozen_at and the sha256 of its
definition, committed before any B3 rule entered the log; at least 100 reference cases from data/facts/, or 20 from
fixtures/measure/ while data/ is empty, each with two blind annotators (leitor:a, leitor:b) whose raw answers are kept,
disagreements queued in governance/readings/CASOS-DESACORDO.md for a pessoa; reports/measure/<date>.json and .md with
precision and recall per rule and a 95 % Wilson interval, split inside / held out, agreement A vs B, error classes;
tools/measure.py recomputes the JSON byte for byte; verify passes over the store the cases live in."""
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent


def test_held_out_is_declared_with_its_hash():
    from engine.canon import canonical, sha256_text
    doc = json.loads((ROOT / "law/HELD-OUT.json").read_text(encoding="utf-8"))
    assert doc["frozen_at"] and doc["definition"]["by_entity"] and doc["definition"]["by_period"]
    assert doc["sha256"] == sha256_text(canonical(doc["definition"]))


def test_reference_cases_have_two_blind_annotators_and_a_queue():
    from engine.store import Store
    data = Store([ROOT / "data"]).load()
    store_dir = ROOT / ("data" if any(u["kind"] == "proc" for u in data.objects["unidade"]) else "fixtures/measure")
    s = Store([store_dir]).load()
    # a case is annotated when both blind answers are stored; it becomes a caso_referencia record once at least one of its
    # (case, rule) pairs has an agreed verdict (the schema asks for one expected verdict); the rest wait in the queue
    answers = ROOT / "governance/readings/casos"
    annotated = [d for d in answers.iterdir() if (d / "leitor-a.json").exists() and (d / "leitor-b.json").exists()] if answers.exists() else []
    assert len(annotated) >= (100 if store_dir.name == "data" else 20), len(annotated)
    cases = s.objects["caso_referencia"]
    assert cases
    for c in cases:
        assert {a["principal"] for a in c["annotators"]} == {"leitor:a", "leitor:b"}, c["id"]
    assert (ROOT / "governance/readings/CASOS-DESACORDO.md").exists()


def test_measurement_report_recomputes_byte_for_byte(tmp_path):
    reports = sorted(p for p in (ROOT / "reports/measure").glob("*.json") if not p.name.startswith(("amalia-", "condicoes-")))  # amalia-*: phase 4 T3 (tools/measure_reader.py); condicoes-*: phase 5 (tools/measure_conditions.py)
    assert reports, "reports/measure/<date>.json missing"
    rep = json.loads(reports[-1].read_text(encoding="utf-8"))
    assert rep["frozen_at"] and rep["rules"] and rep["agreement"]
    for rule, m in rep["rules"].items():
        for split in ("dentro", "reservado"):
            assert {"precision", "recall"} <= set(m[split]), (rule, split)
            for k in ("precision", "recall"):
                if m[split][k]["value"] is not None:
                    lo, hi = m[split][k]["wilson95"]
                    assert 0 <= lo <= m[split][k]["value"] <= hi <= 1
    assert reports[-1].with_suffix(".md").exists()
    out = tmp_path / "m.json"
    subprocess.run([sys.executable, str(ROOT / "tools/measure.py"), "--out", str(out), "--date", reports[-1].stem], check=True, cwd=ROOT)
    assert out.read_bytes() == reports[-1].read_bytes()
