"""The committed fixtures are exactly what tools/make_fixtures.py produces: hashes, offsets and chain are re-derivable."""
import filecmp
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def test_fixtures_rederive_byte_for_byte(tmp_path):
    subprocess.run([sys.executable, str(ROOT / "tools/make_fixtures.py"), str(tmp_path)], check=True, cwd=ROOT)
    for sub in ("valid", "broken"):
        cmp = filecmp.dircmp(ROOT / "fixtures" / sub, tmp_path / sub)
        diffs = []
        def walk(c):
            diffs.extend(c.left_only + c.right_only + c.diff_files)
            for s in c.subdirs.values():
                walk(s)
        walk(cmp)
        assert diffs == [], (sub, diffs)
