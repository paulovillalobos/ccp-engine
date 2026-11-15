"""The special-sector activity each buyer declared in the EU's Official Journal (DECISIONS D96).

    .venv/bin/python -I db/ted_sectors.py --workdir W OUT.json [--years 2018-2026]

A contracting entity of the water, energy, transport and postal sectors publishes its notices under Directive
2014/25/EU and names its activity there: TED-XML CE_ACTIVITY (with LEGAL_BASIS 32014L0025; the free text CE_ACTIVITY_OTHER is not read), eForms
cac:ContractingActivity/cbc:ActivityTypeCode of the list «entity-activity» (RegulatoryDomain 32014L0025). This reads
every Portuguese notice of the monthly bundles (adapters/ted/manifest.json, H.5: the same bytes db/history.py ted loads,
checked against their sha256) and writes, per buyer NIF, each activity it declared with the first and last notice that
says so (raw:ted:aviso:<publication number>). The activity is what the buyer declared in the Official Journal, read
word for word from the element; nothing is inferred from a name.

db/declared.py reads OUT.json as the source of the fact atividade_setor_especial of a procedure whose adjudicante is that NIF.
"""
import argparse
import io
import json
import sys
import tarfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path[:0] = [str(ROOT), str(ROOT / "db")]
import history  # noqa: E402
from engine.canon import sha256_bytes  # noqa: E402

VERSION = "ccp-ted-sectors-0.1"
UTILITIES = "32014L0025"


def _ted():
    import importlib.util
    spec = importlib.util.spec_from_file_location("ted_adapter", ROOT / "adapters/ted/adapter.py")
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def activities(root, ted, fmt):
    """(NIF or None, [activity codes], publication number, publication date) of one notice under Directive 2014/25/EU."""
    import xml.etree.ElementTree as ET  # noqa: F401
    if fmt == "eforms":
        pub, _, got, _ = ted.read_eforms(root)
        if ted.first_text(root, "RegulatoryDomain") != UTILITIES:
            return None, [], pub, None
        acts = sorted({e.text.strip() for e in ted.find(root, "ContractingParty", "ContractingActivity", "ActivityTypeCode")
                       if e.text and e.get("listName") == "entity-activity"})
    else:
        pub, _, got, _ = ted.read_tedxml(root)
        forms = [f for f in ted.find(root, "FORM_SECTION", "*") if f.get("CATEGORY") == "ORIGINAL"] or ted.find(root, "FORM_SECTION", "*")
        if not forms:
            return None, [], pub, None
        form = forms[0]
        basis = {e.get("VALUE") for e in ted.find(form, "LEGAL_BASIS")}
        if UTILITIES not in basis:  # only a notice under Directive 2014/25/EU; its coded activity only (CE_ACTIVITY_OTHER is free text)
            return None, [], pub, None
        acts = sorted({e.get("VALUE") for e in ted.find(form, "CONTRACTING_BODY", "CE_ACTIVITY") if e.get("VALUE")})
    nif = (got.get("adjudicante") or (None,))[0]
    return nif, acts, pub, (got.get("data_publicacao_joue") or (None,))[0]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("out"); ap.add_argument("--workdir", required=True); ap.add_argument("--years", default="2018-2026")
    a = ap.parse_args()
    y0, y1 = (int(x) for x in a.years.split("-"))
    import xml.etree.ElementTree as ET
    ted = _ted()
    manifest = json.loads((ROOT / "adapters/ted/manifest.json").read_text(encoding="utf-8"))
    by_nif, seen = {}, 0
    for month in manifest:
        if not y0 <= int(month["month"][:4]) <= y1:
            continue
        index = json.loads(history.fetch(month["index_sha256"], ["ted"], a.workdir))
        bundle = tarfile.open(fileobj=io.BytesIO(history.fetch(month["pt_bundle_sha256"], ["ted"], a.workdir)))
        for m in index["kept"]:
            xml = bundle.extractfile(m["member"].replace("!", "/")).read()
            if sha256_bytes(xml) != m["sha256"]:
                raise SystemExit(f"ted {month['month']} {m['member']}: bytes differ from the index")
            seen += 1
            nif, acts, pub, date = activities(ET.fromstring(xml), ted, m["format"])
            if not nif or not acts:
                continue
            for act in acts:
                x = by_nif.setdefault(nif, {}).setdefault(act, {"notices": 0, "first": None, "last": None})
                x["notices"] += 1
                if x["first"] is None or (date or "") < x["first"]["date"]:
                    x["first"] = {"raw": f"raw:ted:aviso:{pub}", "date": date or ""}
                if x["last"] is None or (date or "") > x["last"]["date"]:
                    x["last"] = {"raw": f"raw:ted:aviso:{pub}", "date": date or ""}
        print(month["month"], len(by_nif), file=sys.stderr, flush=True)
    Path(a.out).write_text(json.dumps({"tool": VERSION, "notices_read": seen, "by_nif": by_nif}, ensure_ascii=False, indent=1, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"tool": VERSION, "notices_read": seen, "buyers": len(by_nif)}))


if __name__ == "__main__":
    main()
