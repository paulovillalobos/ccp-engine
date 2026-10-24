"""Verification gate (v0 placeholder: replaced in A3). Exit 0 only if the skeleton is in place."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REQUIRED = ["schemas", "engine", "governance", "law", "rules", "fixtures", "tests", "tools", "adapters", "data"]


def main() -> int:
    missing = [d for d in REQUIRED if not (ROOT / d).is_dir()]
    if missing:
        print("verify: missing directories:", ", ".join(missing))
        return 1
    print("verify: skeleton ok (no store yet)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
