"""Coverage per source × year × field: the share of records for which the adapter's own code gives a value.

    .venv/bin/python -I adapters/coverage/matrix.py anuncios FILE YEAR      (a BASE anúncios dump, anuncios<year>.json)
    .venv/bin/python -I adapters/coverage/matrix.py contratos FILE YEAR     (a BASE contratos zip, contratos<year>.zip)
    .venv/bin/python -I adapters/coverage/matrix.py ted DIR                 (the Portuguese TED bundles <yyyy-mm>.tar.gz)
    .venv/bin/python -I adapters/coverage/matrix.py report                  (writes COVERAGE-MATRIX.md from matrix.json)

Each counting command adds its rows to adapters/coverage/matrix.json (source, year, records, per field: count with a value
and the most frequent reasons for none). Values come from base-anuncios map_record, base-contratos contract_values and
adapters/ted/parse.py, unchanged; nothing here decides a value of its own. No model, no network.
"""
import collections
import importlib.util
import json
import sys
import tarfile
import zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
OUT = HERE / "matrix.json"
TED_FIELDS = ["dispatch_date", "notice_id", "buyer_name", "buyer_nif", "buyer_nuts", "procedure_type", "contract_type",
              "deadline_date", "estimated_value", "main_cpv"]


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def save(rows):
    old = json.loads(OUT.read_text(encoding="utf-8")) if OUT.exists() else []
    keys = {(r["source"], r["year"]) for r in rows}
    allr = sorted([r for r in old if (r["source"], r["year"]) not in keys] + rows, key=lambda r: (r["source"], r["year"]))
    OUT.write_text(json.dumps(allr, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    for r in rows:
        print(r["source"], r["year"], r["records"], {f: v["with_value"] for f, v in r["fields"].items()})


def tally(source, year, results, fields):
    n = len(results)
    out = {}
    for f in fields:
        k = sum(1 for got, _ in results if f in got)
        reasons = collections.Counter(why[f] for got, why in results if f not in got and f in why)
        out[f] = {"with_value": k, "pct": round(100 * k / n, 1) if n else None, "none_because": dict(reasons.most_common(4))}
    return {"source": source, "year": year, "records": n, "fields": out}


def cmd_anuncios(path, year):
    ad = load("base_anuncios", ROOT / "adapters/base-anuncios/adapter.py")
    recs = ad.records(Path(path).read_bytes())
    proc = [r for _, r, _ in recs if r.get("tipoActo") == "Anúncio de procedimento"]
    fields = [m["canonical_field"] for m in ad.MAPPING["adaptador"]["mapping"]]
    row = tally("base-anuncios", int(year), [ad.map_record(r) for r in proc], fields)
    row["records_all_acts"] = len(recs)
    save([row])


def cmd_contratos(path, year):
    ad = load("base_contratos", ROOT / "adapters/base-contratos/adapter.py")
    with zipfile.ZipFile(path) as z:
        member = next(n for n in z.namelist() if n.lower().endswith(".json"))
        text = z.read(member).decode("utf-8")
    fields = [m for m in ad.ROWS if m != "data_modificacao"]
    save([tally("base-contratos", int(year), [ad.contract_values(r) for r, _ in ad.records(text)], fields)])


def cmd_ted(d):
    parse = load("ted_parse", ROOT / "adapters/ted/parse.py")
    by_year = collections.defaultdict(list)
    for b in sorted(Path(d).glob("*.tar.gz")):
        with tarfile.open(b, "r:gz") as t:
            for m in t:
                if m.isfile() and m.name.endswith(".xml"):
                    r = parse.parse(t.extractfile(m).read())
                    if r["buyer_country"] in ("PT", "PRT"):
                        got = {f: r[f] for f in TED_FIELDS if r.get(f) not in (None, "")}
                        if (r.get("notice_type") or "").split(" ")[0] not in ("3", "16", "17", "18"):
                            got.pop("deadline_date", None)  # counted on contract notices only, below
                        by_year[int(b.name[:4])].append((r, got))
    rows = []
    for y, items in sorted(by_year.items()):
        res = [(got, {f: "not in the notice" for f in TED_FIELDS}) for _, got in items]
        row = tally("ted", y, res, TED_FIELDS)
        cn = [(r, got) for r, got in items if (r.get("notice_type") or "").split(" ")[0] in ("3", "16", "17", "18")]
        k = sum(1 for r, _ in cn if r.get("deadline_date"))
        row["fields"]["deadline_date"] = {"with_value": k, "pct": round(100 * k / len(cn), 1) if cn else None,
                                          "of": f"{len(cn)} contract notices", "none_because": {}}
        row["formats"] = dict(collections.Counter(r["format"] for r, _ in items))
        rows.append(row)
    save(rows)


def num(n):
    return f"{n:,}".replace(",", " ")


def ted_mix():
    rows = json.loads(OUT.read_text(encoding="utf-8"))
    f = next((r.get("formats", {}) for r in rows if r["source"] == "ted" and r["year"] == 2024), {})
    return ", ".join(f"{k} {num(v)}" for k, v in sorted(f.items()))


def cmd_report():
    rows = json.loads(OUT.read_text(encoding="utf-8"))
    lines = ["# Coverage matrix: source × year × field", "",
             "Share of records for which the adapter's own code gives a value (adapters/coverage/matrix.py; counts in",
             "matrix.json, with the most frequent reasons for no value). BASE anúncios: procedure notices only (tipoActo",
             "«Anúncio de procedimento»). TED: notices with a Portuguese buyer; deadline_date over contract notices only.",
             "A share is coverage, not correctness: correctness is measured in adapters/medicao/ (TED, BASE contratos) and",
             "in the DR notices' test.", ""]
    for source in ("base-anuncios", "base-contratos", "ted"):
        rs = [r for r in rows if r["source"] == source]
        if not rs:
            continue
        fields = list(rs[0]["fields"])
        lines += [f"## {source}", "", "| year | records | " + " | ".join(fields) + " |", "|---|---:|" + "---:|" * len(fields)]
        for r in rs:
            lines.append(f"| {r['year']} | {num(r['records'])} | " + " | ".join(f"{r['fields'][f]['pct']}" for f in fields) + " |")
        lines.append("")
        gaps = []
        for r in rs:
            for f in fields:
                v = r["fields"][f]
                if v["pct"] is not None and v["pct"] < 90:
                    why = "; ".join(f"{k} ({num(c)})" for k, c in v["none_because"].items())
                    gaps.append(f"- {r['year']} {f}: {v['pct']} %" + (f" — {why}" if why else ""))
        if gaps:
            lines += ["Gaps (under 90 %):", ""] + gaps + [""]
    log = ROOT / "adapters/dr-anuncios/fetch-log.jsonl"
    keys = {json.loads(x)["key"] for x in log.read_text(encoding="utf-8").splitlines() if '"status": 200' in x} if log.exists() else set()
    lines += ["## Not in the tables above (gaps by source)", "",
              f"- DR notice PDFs 2026: {num(len(keys))} procedures' notices downloaded of the 22 170 with a DR PDF (adapters/dr-anuncios/fetch-log.jsonl,",
              "  one GET every 10 s, still running); fields per notice in adapters/dr-anuncios/COVERAGE.md, which counts only the notices",
              "  already read into documents. DR 2018–2025: not fetched (next: concursos públicos, newest first).",
              "- Vortal (a second copy of DR notices, where the pieces are on Vortal): 219 copies, byte-identical to the DR; stopped by a",
              "  403 on 2026-10-26 20:18:27Z. Platform pieces (acinGov, Vortal) are documents, not fields: none in these tables.",
              "- TED forms by year: TED-XML to 2023, mixed in 2024 (" + ted_mix() + "), eForms only from 2025; buyer_nif and",
              "  procedure_type shift with the form, not with the year. TED keeps notices whose",
              "  buyer is Portuguese by the parser (contract notices, results, changes, all kinds); BASE anúncios are procedure notices.",
              "- BASE contratos tipo_procedimento: framework-agreement call-offs (arts. 258.º/259.º), «Contratação excluída II»,",
              "  special-sector exemptions and «Ajuste direto simplificado» are outside the adapter's vocabulary (a mapping choice).",
              "- BASE modificações and entidades: sampled only (2026), not in these tables.", ""]
    (HERE / "COVERAGE-MATRIX.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines)[:4000])


if __name__ == "__main__":
    cmd = sys.argv[1]
    {"anuncios": lambda: cmd_anuncios(sys.argv[2], sys.argv[3]), "contratos": lambda: cmd_contratos(sys.argv[2], sys.argv[3]),
     "ted": lambda: cmd_ted(sys.argv[2]), "report": cmd_report}[cmd]()
