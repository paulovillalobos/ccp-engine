"""tools/run_engine.py over the fixture store: deterministic to the byte, every verdict it writes re-derived by verify
(RED, MAN, TIME ...), no natural person named. The real run waits for data/facts (B4)."""
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def run(tmp, name, verdicts=True):
    out = tmp / f"{name}.json"
    cmd = [sys.executable, str(ROOT / "tools/run_engine.py"), "--out", str(out), "--stores", str(ROOT / "fixtures/valid"),
           "--known-at", "2026-10-25T00:00:00Z", "--commit", "abcdef1"]
    if verdicts:
        cmd += ["--verdicts", str(tmp / "v")]
    subprocess.run(cmd, check=True, cwd=ROOT, capture_output=True)
    return out


def test_engine_over_fixtures_is_deterministic_and_rederived(tmp_path):
    import verify
    a = run(tmp_path, "a")
    b = run(tmp_path, "b", verdicts=False)
    assert a.read_bytes() == b.read_bytes()
    report = json.loads(a.read_text(encoding="utf-8"))
    assert report["units"] == 1 and report["rules"], report
    for counts in report["rules"].values():
        assert set(counts) == {"cumpre", "nao_cumpre", "nao_avaliado"}
    _, out = verify.check_store([ROOT / "fixtures/valid", tmp_path / "v"])
    assert out == [], out[:5]
    for f in (tmp_path / "v/veredicto").glob("*.json"):
        v = json.loads(f.read_text(encoding="utf-8"))
        assert all("name" not in e for e in v["entities"] if e["type"] == "pessoa_singular")
