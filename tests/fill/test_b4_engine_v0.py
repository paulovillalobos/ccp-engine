"""FILL-PLAN B4 — red until the engine has run over the extractor's notices.

Depends on the extractor delivering data/facts/ (adapters/ and data/ are theirs; the builder never writes there).
Done when: data/facts/ holds at least 1000 proc units with facts; reports/prazos-minimos.json exists with, per
prazo_minimo rule, the counts of cumpre / nao_cumpre / nao_avaliado by reason and the manifest; tools/run_engine.py
recomputes that file byte for byte; every verdict counted has a complete manifest and no natural person is named."""
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
REPORT = ROOT / "reports/prazos-minimos.json"


def test_extractor_delivered_notices():
    from engine.store import Store
    s = Store([ROOT / "data"]).load()
    assert s.errors == [], s.errors[:5]
    procs = [u for u in s.objects["unidade"] if u["kind"] == "proc"]
    assert len(procs) >= 1000, len(procs)


def test_first_figure_at_scale_is_reproducible(tmp_path):
    assert REPORT.exists(), "reports/prazos-minimos.json missing"
    report = json.loads(REPORT.read_text(encoding="utf-8"))
    assert report["manifest"] and report["rules"], report.keys()
    total = 0
    for rule_id, counts in report["rules"].items():
        assert rule_id.startswith("regra:")
        assert set(counts) == {"cumpre", "nao_cumpre", "nao_avaliado"} and isinstance(counts["nao_avaliado"], dict)
        total += counts["cumpre"] + counts["nao_cumpre"] + sum(counts["nao_avaliado"].values())
    assert total >= 1000
    out = tmp_path / "prazos-minimos.json"
    subprocess.run([sys.executable, str(ROOT / "tools/run_engine.py"), "--out", str(out)], check=True, cwd=ROOT)
    assert out.read_bytes() == REPORT.read_bytes()
