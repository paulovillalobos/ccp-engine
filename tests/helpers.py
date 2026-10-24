import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
VALID = ROOT / "fixtures/valid"


def load_all(type_):
    return [json.loads(p.read_text(encoding="utf-8")) for p in sorted((VALID / type_).glob("*.json"))]


def one(type_, name):
    return json.loads((VALID / type_ / f"{name}.json").read_text(encoding="utf-8"))
