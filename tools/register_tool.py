"""Register a ferramenta principal with the sha256 of its code (product rule D22): a new version when the hash changed.

    .venv/bin/python tools/register_tool.py <name> <code path> [--nota TEXT] [--governance governance]

ferramenta:<name>@<n>: if the current (non-retired) entry has the same hash, nothing changes; otherwise it is retired
and ferramenta:<name>@<n+1> is added with the new hash. verify's PROV check requires the registered hash to match.
"""
import argparse
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from engine import schema  # noqa: E402

VERSION = "ccp-register-tool-0.1"


def register(gov_dir: Path, name: str, code: str, nota: str = None) -> str:
    pfile = gov_dir / "principals.json"
    doc = json.loads(pfile.read_text(encoding="utf-8")) if pfile.exists() else {"principals": []}
    digest = hashlib.sha256((ROOT / code).read_bytes()).hexdigest()
    current = [p for p in doc["principals"] if p["papel"] == "ferramenta" and p["id"].startswith(f"ferramenta:{name}@") and not p["retired"]]
    if current and current[0]["hash"] == digest:
        return current[0]["id"]
    n = max([int(p["id"].rsplit("@", 1)[1]) for p in doc["principals"] if p["id"].startswith(f"ferramenta:{name}@")] or [0]) + 1
    from engine.sources import now_utc
    for p in current:
        p["retired"] = True
        p["retired_at"] = now_utc()  # D41: its events up to this instant stay valid
    entry = {"id": f"ferramenta:{name}@{n}", "kind": "codigo", "papel": "ferramenta", "familia": None, "motor": None, "versao": n, "code": code, "hash": digest, "retired": False}
    if nota:
        entry["nota"] = nota
    doc["principals"].append(entry)
    errors = schema.validate("principals", doc)
    if errors:
        raise SystemExit(f"principals.json would be invalid: {errors[0]}")
    pfile.write_text(json.dumps(doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return entry["id"]


if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("name"); ap.add_argument("code"); ap.add_argument("--nota"); ap.add_argument("--governance", default="governance")
    a = ap.parse_args()
    print(register(ROOT / a.governance, a.name, a.code, a.nota))
