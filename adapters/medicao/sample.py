"""Draw the samples of CRITERIA-ted-contratos-v1.md and run the frozen parsers on them (outputs sealed by sha256).

    .venv/bin/python -I adapters/medicao/sample.py ted --bundles DIR --out OUT
    .venv/bin/python -I adapters/medicao/sample.py contratos --zip contratos2026.zip --out OUT

ted        DIR holds the monthly Portuguese bundles <yyyy-mm>.tar.gz (from the Modal volume or Storage); the development
           months 2018-01 and 2026-01 are left out; a notice is in the population when the parser's buyer_country is PT
           or PRT; 100 TED-XML and 100 eForms drawn with random.Random(20261027) from each format's population sorted by
           member name. Writes OUT/ted/items/<n>.xml (the notice, unchanged), OUT/ted/sample.json (member, month, sha256)
           and OUT/ted/parsed.json (the parser's fields), and prints the sha256 of both JSON files.
contratos  the records of the zip's member, without those BASE published in 2026-10 and without repeated idcontrato,
           sorted by idcontrato; 200 drawn with random.Random(20261027). Writes OUT/contratos/items/<n>.json (the record's
           exact bytes), sample.json and parsed.json (the adapter's contract_values, value and source field per field).
No model is called here.
"""
import argparse
import hashlib
import importlib.util
import io
import json
import random
import sys
import tarfile
import zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
SEED = 20261027
DEV_MONTHS = {"2018-01", "2026-01"}


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def write_json(path, obj):
    data = (json.dumps(obj, ensure_ascii=False, indent=1, sort_keys=True) + "\n").encode("utf-8")
    path.write_bytes(data)
    return hashlib.sha256(data).hexdigest()


def cmd_ted(a):
    parse = load("ted_parse", ROOT / "adapters/ted/parse.py")
    pop = {"ted-xml": [], "eforms": []}
    for b in sorted(Path(a.bundles).glob("*.tar.gz")):
        month = b.name[:7]
        if month in DEV_MONTHS:
            continue
        with tarfile.open(b, "r:gz") as t:
            for m in t:
                if not m.isfile() or not m.name.endswith(".xml"):
                    continue
                data = t.extractfile(m).read()
                r = parse.parse(data)
                if r["buyer_country"] in ("PT", "PRT"):
                    pop[r["format"]].append((m.name, month, data, r))
    out = Path(a.out) / "ted"
    (out / "items").mkdir(parents=True, exist_ok=True)
    sample, parsed = [], []
    for fmt in ("ted-xml", "eforms"):
        items = sorted(pop[fmt], key=lambda x: x[0])
        for name, month, data, r in random.Random(SEED).sample(items, 100):
            n = len(sample)
            (out / "items" / f"{n:03d}.xml").write_bytes(data)
            sample.append({"n": n, "member": name, "month": month, "format": fmt, "sha256": hashlib.sha256(data).hexdigest()})
            parsed.append(dict(r, n=n))
    print("population", {k: len(v) for k, v in pop.items()})
    print("sample.json", write_json(out / "sample.json", sample), "parsed.json", write_json(out / "parsed.json", parsed))


def cmd_contratos(a):
    adapter = load("base_contratos", ROOT / "adapters/base-contratos/adapter.py")
    with zipfile.ZipFile(a.zip) as z:
        text = z.read(adapter.MEMBER).decode("utf-8")
    recs = adapter.records(text)
    ids = {}
    for r, _ in recs:
        ids[r["idcontrato"]] = ids.get(r["idcontrato"], 0) + 1
    pop = sorted(((r, b) for r, b in recs if ids[r["idcontrato"]] == 1 and (adapter.date_pt(r.get("dataPublicacao")) or "")[:7] != "2026-10"),
                 key=lambda x: x[0]["idcontrato"])
    out = Path(a.out) / "contratos"
    (out / "items").mkdir(parents=True, exist_ok=True)
    sample, parsed = [], []
    for n, (r, b) in enumerate(random.Random(SEED).sample(pop, 200)):
        (out / "items" / f"{n:03d}.json").write_bytes(b)
        got, why = adapter.contract_values(r)
        sample.append({"n": n, "idcontrato": r["idcontrato"], "sha256": hashlib.sha256(b).hexdigest(), "nAnuncio": r.get("nAnuncio"), "idINCM": r.get("idINCM")})
        parsed.append({"n": n, **{k: v[0] for k, v in got.items()}, "_missing": why})
    print("population", len(pop))
    print("sample.json", write_json(out / "sample.json", sample), "parsed.json", write_json(out / "parsed.json", parsed))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    t = sub.add_parser("ted"); t.add_argument("--bundles", required=True); t.add_argument("--out", required=True)
    c = sub.add_parser("contratos"); c.add_argument("--zip", required=True); c.add_argument("--out", required=True)
    a = ap.parse_args()
    sys.exit({"ted": cmd_ted, "contratos": cmd_contratos}[a.cmd](a))
