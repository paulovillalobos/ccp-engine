"""BASE anúncios dump (dados.gov.pt, IMPIC, weekly JSON) -> raw records, proc units, facts and adjudicante entities.

    python -I adapters/base-anuncios/adapter.py build    --dump PATH --url URL --captured-at T --recorded-at T --principal P
    python -I adapters/base-anuncios/adapter.py check    [--data data]
    python -I adapters/base-anuncios/adapter.py register --at T

build   reads the downloaded file (never the network), stores its bytes under data/raw_bytes/<sha256>, cuts every record's
        exact byte slice out of the JSON array and stores it under its own sha256, and writes, in the store layout of
        schemas/: one raw for the download and one per mapped record (data/raw/base-anuncios/raw/), one proc unit per
        procedure notice, one fact per canonical field the record gives unambiguously (mapping.json, field by field),
        the adjudicante entities whose type the NIF decides, their aliases and nif_exact links, the adaptador object with
        its coverage per month, and adapters/base-anuncios/COVERAGE.md. Same inputs, same bytes: everything is sorted and
        recorded_at is given. A file that exists with other bytes is refused (nothing is rewritten).
check   rebuilds, in memory, from the stored download (the raw of kind dump) and compares every file byte for byte with
        data/ and COVERAGE.md: the record slices, their raws, units, facts, entities, aliases, links and the adaptador.
register registers this file as ferramenta:adapter-base-anuncios (tools/register_tool.py) and proposes the adaptador in
        the governance log, with the sha256 of this code and of mapping.json in the payload; when either changed since,
        it records a correct with the new hashes instead. The log decides its state.

No model reads anything here and nothing is sent anywhere: the dump is structured and this is code.
"""
import argparse
import datetime
import json
import re
import sys
from collections import Counter, defaultdict
from decimal import Decimal, InvalidOperation
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
sys.path.insert(0, str(ROOT))
from engine import schema  # noqa: E402
from engine.canon import canonical, content_hash, sha256_bytes  # noqa: E402
from engine.entities import nif_id  # noqa: E402

VERSION = "base-anuncios-adapter-0.2"
SOURCE = "base-anuncios"
TOOL = "adapter-base-anuncios"
MAPPING = json.loads((HERE / "mapping.json").read_text(encoding="utf-8"))
CANONICAL_ASKED = ["data_inicio_procedimento", "tipo_procedimento", "tipo_contrato", "preco_base", "publicado_joue",
                   "prazo_propostas_dias", "data_envio_anuncio", "territorio", "tipo_entidade", "adjudicante"]
DATE_PT = re.compile(r"([0-9]{2})/([0-9]{2})/([0-9]{4})")
DATE_ISO = re.compile(r"([0-9]{4})-([0-9]{2})-([0-9]{2})")
PRICE = re.compile(r"[0-9]+\.[0-9]{2}")


# ---- reading the download ------------------------------------------------------------------------------------------
def records(data: bytes):
    """[(index, record dict, exact bytes of the record inside the array)]. The download is a JSON array of objects."""
    text = data.decode("utf-8")
    dec = json.JSONDecoder()
    out, i, n = [], 0, len(text)

    def skip(i):
        while i < n and text[i] in " \t\r\n":
            i += 1
        return i
    i = skip(i)
    if text[i] != "[":
        raise ValueError("the download is not a JSON array")
    i = skip(i + 1)
    while i < n and text[i] != "]":
        obj, end = dec.raw_decode(text, i)
        out.append((len(out), obj, text[i:end].encode("utf-8")))
        i = skip(end)
        if text[i] == ",":
            i = skip(i + 1)
    if json.loads(text) != [o for _, o, _ in out]:
        raise ValueError("record slices do not reproduce the array")
    return out


def key_of(rec):
    n = re.sub(r"[^A-Za-z0-9]+", "-", rec["nAnuncio"]).strip("-")
    incm = rec["IdIncm"] if rec["IdIncm"] not in ("-1", "", None) else "x"
    return f"{n}.{incm}"


def date_pt(value):
    """dd/mm/yyyy (dumps up to 2026-11-03) or yyyy-mm-dd (from 2026-11-04)."""
    m = DATE_PT.fullmatch(value or "")
    iso = DATE_ISO.fullmatch(value or "") if not m else None
    if not m and not iso:
        return None
    d, mo, y = m.groups() if m else iso.groups()[::-1]
    try:
        return datetime.date(int(y), int(mo), int(d)).isoformat()
    except ValueError:
        return None


def price(value):
    if not PRICE.fullmatch(value or ""):
        return None
    try:
        v = Decimal(value)
    except InvalidOperation:
        return None
    if v == 0:
        return None
    return int(v) if v == v.to_integral_value() else float(v)


# ---- mapping, field by field ---------------------------------------------------------------------------------------
def row(field):
    return next(m for m in MAPPING["adaptador"]["mapping"] if m["canonical_field"] == field)


def map_record(rec):
    """{canonical field: (value, source field)} and {canonical field: reason it gave no fact}."""
    got, why = {}, {}
    published = date_pt(rec.get("dataPublicacao"))

    r = row("tipo_procedimento")
    if rec.get("tipoActo") != "Anúncio de procedimento":
        why["tipo_procedimento"] = f"tipoActo '{rec.get('tipoActo')}'"
    elif rec.get("modeloAnuncio") not in r["enum_map"]:
        why["tipo_procedimento"] = f"modeloAnuncio '{rec.get('modeloAnuncio')}' outside the vocabulary"
    else:
        got["tipo_procedimento"] = (r["enum_map"][rec["modeloAnuncio"]], r["source_field"])

    r = row("tipo_contrato")
    tipos = rec.get("tiposContrato") or []
    if len(tipos) != 1:
        why["tipo_contrato"] = "empty list" if not tipos else "several contract types"
    elif tipos[0] not in r["enum_map"]:
        why["tipo_contrato"] = f"'{tipos[0]}' outside the vocabulary"
    else:
        got["tipo_contrato"] = (r["enum_map"][tipos[0]], r["source_field"])

    r = row("preco_base")
    v = price(rec.get("PrecoBase"))
    if v is None:
        why["preco_base"] = f"PrecoBase '{rec.get('PrecoBase')}'"
    else:
        got["preco_base"] = (v, r["source_field"])

    r = row("adjudicante")
    nif = rec.get("nifEntidade") or ""
    if re.fullmatch(r"[0-9]{9}", nif):
        got["adjudicante"] = (nif, r["source_field"])
    else:
        why["adjudicante"] = "empty NIF" if not nif else "NIF not nine digits"

    r = row("data_publicacao_anuncio")
    if published:
        got["data_publicacao_anuncio"] = (published, r["source_field"])
    else:
        why["data_publicacao_anuncio"] = "not a dd/mm/yyyy date"

    r = row("data_limite_propostas")
    limit = date_pt(rec.get("DataLimitePropostas"))
    if limit is None:
        why["data_limite_propostas"] = "empty" if not rec.get("DataLimitePropostas") else "not a dd/mm/yyyy date"
    elif published and limit < published:
        why["data_limite_propostas"] = "earlier than dataPublicacao"
    else:
        got["data_limite_propostas"] = (limit, r["source_field"])

    for field, reason in MAPPING["not_in_source"].items():
        why[field] = "not in the dump"
    return got, why


def entity_type(nif):
    table = MAPPING["entities"]["type_by_nif_prefix"]
    for prefix in sorted(table, key=len, reverse=True):
        if nif.startswith(prefix):
            return table[prefix]
    return None


# ---- build ---------------------------------------------------------------------------------------------------------
def build(dump: bytes, url, captured_at, recorded_at, principal):
    """Everything the adapter writes, as {relative path: bytes}, plus the statistics behind COVERAGE.md."""
    files, stats = {}, {"records": 0}
    dump_sha = sha256_bytes(dump)
    files[f"raw_bytes/{dump_sha}"] = dump
    resource = url.rstrip("/").split("/")
    dump_raw = {"id": f"raw:{SOURCE}:dump:{resource[-1]}.{resource[-2]}", "revision": 1, "recorded_at": recorded_at, "source": SOURCE,
                "kind": "dump", "source_id": f"{resource[-2]}/{resource[-1]}", "sha256": dump_sha, "bytes": f"raw_bytes/{dump_sha}",
                "media_type": "application/json", "encoding": "utf-8", "url": url, "captured_at": captured_at,
                "request": {"method": "GET", "reads_of_page": 1}}
    recs = records(dump)
    stats["records"] = len(recs)
    acts = set(MAPPING["record"]["procedure_acts"])
    keys = Counter(key_of(r) for _, r, _ in recs if r.get("tipoActo") in acts)
    unmapped = defaultdict(list)       # reason -> [nAnuncio]
    by_month = defaultdict(list)       # YYYY-MM -> [(key, rec, slice)]
    records_by_month = Counter()
    for _, rec, raw_bytes in recs:
        published = date_pt(rec.get("dataPublicacao"))
        month = published[:7] if published else "sem-data"
        records_by_month[month] += 1
        act = rec.get("tipoActo")
        if act in MAPPING["record"]["unmapped_acts"]:
            unmapped[f"tipoActo '{act}': {MAPPING['record']['unmapped_acts'][act]}"].append(rec["nAnuncio"])
        elif act not in acts:
            unmapped[f"tipoActo '{act}' unknown to the adapter"].append(rec["nAnuncio"])
        elif not rec.get("nAnuncio"):
            unmapped["nAnuncio empty: the procedure has no key"].append(f"IdIncm {rec.get('IdIncm')}")
        elif keys[key_of(rec)] > 1:
            unmapped["key (nAnuncio, IdIncm) held by more than one procedure record; the procedure cannot be told apart"].append(rec["nAnuncio"])
        elif not published:
            unmapped["dataPublicacao is not a date; no valid_at for its facts"].append(rec["nAnuncio"])
        else:
            by_month[month].append((key_of(rec), rec, raw_bytes))

    field_counts = defaultdict(Counter)       # field -> month -> procs with the fact
    omitted = defaultdict(lambda: defaultdict(list))  # field -> reason -> [nAnuncio]
    entities = {}                             # nif -> entidade
    no_entity = defaultdict(list)             # reason -> [nAnuncio]
    procs_by_month = Counter()
    adaptador_id = MAPPING["adaptador"]["id"]
    for month in sorted(by_month):
        raws, units, facts, aliases, links = [], [], [], [], []
        for key, rec, raw_bytes in sorted(by_month[month], key=lambda x: x[0]):
            sha = sha256_bytes(raw_bytes)
            files[f"raw_bytes/{sha}"] = raw_bytes
            raw_id = f"raw:{SOURCE}:anuncio:{key}"
            raws.append({"id": raw_id, "revision": 1, "recorded_at": recorded_at, "source": SOURCE, "kind": "anuncio",
                         "source_id": rec["nAnuncio"], "sha256": sha, "bytes": f"raw_bytes/{sha}", "media_type": "application/json",
                         "encoding": "utf-8", "url": url, "captured_at": captured_at, "request": {"method": "GET", "reads_of_page": 1}})
            unit_id = f"proc:base:{key}"
            units.append({"id": unit_id, "revision": 1, "recorded_at": recorded_at, "kind": "proc", "parent": None, "raw": [raw_id],
                          "consumer_ids": {"n_anuncio": rec["nAnuncio"]}})
            procs_by_month[month] += 1
            got, why = map_record(rec)
            valid_at = got["data_publicacao_anuncio"][0]
            for field in sorted(got):
                value, src = got[field]
                facts.append({"id": f"facto:{unit_id.replace(':', '-')}:{field}:{SOURCE}", "revision": 1, "recorded_at": recorded_at,
                              "unit": unit_id, "field": field, "value": value, "origin": {"raw": raw_id, "field": src},
                              "adapter": adaptador_id, "valid_at": valid_at, "known_at": captured_at})
                field_counts[field][month] += 1
            for field, reason in why.items():
                omitted[field][reason].append(rec["nAnuncio"])
            nif = got.get("adjudicante", (None,))[0]
            name = (rec.get(MAPPING["entities"]["adjudicante_name_field"]) or "").strip()
            if nif is None:
                no_entity["no NIF" + ("" if name else " and no name: no candidate either")].append(rec["nAnuncio"])
                continue
            etype = entity_type(nif)
            if etype is None:
                no_entity[f"NIF prefix {nif[0]}: public or private not decided by the NIF (SCHEMA-PROPOSAL.md)"].append(rec["nAnuncio"])
                continue
            ent_id = nif_id(nif)
            e = entities.setdefault(nif, {"id": ent_id, "revision": 1, "recorded_at": recorded_at, "type": etype,
                                          "country": MAPPING["entities"]["country"], "nif": nif, "roles": [], "raw": []})
            if name and etype != "pessoa_singular" and "name" not in e:
                e["name"] = name
            e["roles"].append({"unit": unit_id, "role": "adjudicante"})
            e["raw"].append(raw_id)
            if name:
                link_id = f"link:{SOURCE}.{key}.adjudicante"
                alias_id = f"alias:{SOURCE}:{key}.adjudicante"
                aliases.append({"id": alias_id, "revision": 1, "recorded_at": recorded_at, "raw": raw_id,
                                "field": MAPPING["entities"]["adjudicante_name_field"], "name_as_appears": name, "link": link_id})
                links.append({"id": link_id, "revision": 1, "recorded_at": recorded_at, "from": alias_id, "to": ent_id, "proponent": principal,
                              "method": "nif_exact", "evidence": {"source_field": MAPPING["entities"]["adjudicante_nif_field"], "value": nif},
                              "state": "settled", "at": recorded_at, "evento": None})
        tag = f"{SOURCE}-{month}"
        files[f"raw/{SOURCE}/raw/{tag}.jsonl"] = jsonl(raws)
        files[f"facts/unidade/{tag}.jsonl"] = jsonl(units)
        files[f"facts/facto/{tag}.jsonl"] = jsonl(facts)
        if aliases:
            files[f"facts/alias/{tag}.jsonl"] = jsonl(aliases)
            files[f"facts/link/{tag}.jsonl"] = jsonl(links)
    files[f"raw/{SOURCE}/raw/{SOURCE}-download.jsonl"] = jsonl([dump_raw])
    for e in entities.values():
        e["roles"].sort(key=lambda r: r["unit"])
        e["raw"].sort()
    if entities:
        files[f"facts/entidade/{SOURCE}.jsonl"] = jsonl(sorted(entities.values(), key=lambda e: e["id"]))
    a = dict(MAPPING["adaptador"])
    a = {"id": a["id"], "revision": 1, "recorded_at": recorded_at, "source": a["source"], "version": a["version"], "code": a["code"],
         "mapping": a["mapping"], "coverage": [{"period": m, "expected": None, "captured": procs_by_month[m]} for m in sorted(procs_by_month)],
         "proposed_by": principal, "state": "proposed"}
    files[f"facts/adaptador/{SOURCE}-{a['version']}.json"] = (json.dumps(a, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    stats.update(dump_sha=dump_sha, dump_size=len(dump), dump_raw=dump_raw["id"], url=url, captured_at=captured_at,
                 records_by_month=dict(records_by_month), procs_by_month=dict(procs_by_month), unmapped=unmapped,
                 field_counts=field_counts, omitted=omitted, entities=entities, no_entity=no_entity,
                 facts=sum(sum(c.values()) for c in field_counts.values()))
    validate(files)
    return files, stats


def jsonl(objs):
    return "".join(canonical(o) + "\n" for o in objs).encode("utf-8")


def validate(files):
    """Every object against its schema before anything is written (the store validates again on load)."""
    for path, data in files.items():
        if path.startswith("raw_bytes/"):
            continue
        type_ = Path(path).parent.name
        text = data.decode("utf-8")
        objs = [json.loads(l) for l in text.splitlines() if l.strip()] if path.endswith(".jsonl") else [json.loads(text)]
        for o in objs:
            errs = schema.validate(type_, o)
            if errs:
                raise SystemExit(f"{path}: {o.get('id')}: {errs[0]}")


# ---- coverage report -----------------------------------------------------------------------------------------------
def coverage_md(stats):
    months = sorted(stats["procs_by_month"])
    procs = sum(stats["procs_by_month"].values())
    unmapped_n = sum(len(v) for v in stats["unmapped"].values())
    L = ["# BASE anúncios 2026: coverage of adaptador:base-anuncios@1", "",
         f"Generated by `adapters/base-anuncios/adapter.py` ({VERSION}); `adapter.py check` re-derives it byte for byte.", "",
         "## Source", "",
         "| | |", "|---|---|",
         "| dataset | dados.gov.pt, «Contratos Públicos - Portal Base - IMPIC - Anúncios de 2012 a 2026» (weekly) |",
         f"| resource | {stats['url']} |",
         f"| fetched (one GET) | {stats['captured_at']} |",
         f"| size | {stats['dump_size']} bytes |",
         f"| sha256 | `{stats['dump_sha']}` |",
         f"| raw | `{stats['dump_raw']}` (bytes in data/raw_bytes/, kept in the repository by pessoa:paulo's decision of 2026-10-25) |", "",
         "## Records and procedures", "",
         f"- Records in the dump: {stats['records']}.",
         f"- Procedures out (`proc` units, one per procedure notice, each with its own `raw` = the record's byte slice): {procs}.",
         f"- Records not mapped to a procedure: {unmapped_n}.",
         f"- Facts written: {stats['facts']}.",
         f"- Adjudicante entities written: {len(stats['entities'])} (by NIF; {sum(len(e['roles']) for e in stats['entities'].values())} roles).", "",
         "| month (dataPublicacao) | records | procedures |", "|---|---:|---:|"]
    for m in sorted(stats["records_by_month"]):
        L.append(f"| {m} | {stats['records_by_month'][m]} | {stats['procs_by_month'].get(m, 0)} |")
    L += ["", "## Records not mapped, by reason", "", "| reason | records | three examples (nAnuncio) |", "|---|---:|---|"]
    for reason, ids in sorted(stats["unmapped"].items(), key=lambda kv: (-len(kv[1]), kv[0])):
        L.append(f"| {reason} | {len(ids)} | {', '.join(ids[:3])} |")
    L += ["", "## Procedures carrying each canonical field, per month", "",
          "The ten fields the 18 rules read, then the two dates the dump does give. 0 means the field is not a fact of any procedure.", "",
          "| field | " + " | ".join(months) + " | total | of procedures |", "|---|" + "---:|" * (len(months) + 2)]
    for field in CANONICAL_ASKED + ["data_publicacao_anuncio", "data_limite_propostas"]:
        c = stats["field_counts"].get(field, Counter())
        total = sum(c.values())
        L.append(f"| {field} | " + " | ".join(str(c.get(m, 0)) for m in months) + f" | {total} | {100 * total / procs:.1f} % |")
    L += ["", "## Fields the dump does not give", ""]
    for field, reason in MAPPING["not_in_source"].items():
        L.append(f"- `{field}`: {reason}.")
    L += ["", "## Procedures without a fact for a mapped field, by reason", "", "| field | reason | procedures | three examples (nAnuncio) |", "|---|---|---:|---|"]
    for field in [m["canonical_field"] for m in MAPPING["adaptador"]["mapping"]]:
        for reason, ids in sorted(stats["omitted"].get(field, {}).items(), key=lambda kv: (-len(kv[1]), kv[0])):
            L.append(f"| {field} | {reason} | {len(ids)} | {', '.join(ids[:3])} |")
    L += ["", "## Adjudicante entities", "",
          f"- Distinct adjudicante NIFs among the procedures: {len({f for f in stats['nifs']})}.",
          f"- Entities written (`ent:nif:`, type decided by the NIF): {len(stats['entities'])}, types {dict(Counter(e['type'] for e in stats['entities'].values()))}.",
          "- Candidates by country and name (`ent:cand:`): 0. The procedures without NIF have no name either.", "",
          "| procedures without an entity | procedures | three examples (nAnuncio) |", "|---|---:|---|"]
    for reason, ids in sorted(stats["no_entity"].items(), key=lambda kv: (-len(kv[1]), kv[0])):
        L.append(f"| {reason} | {len(ids)} | {', '.join(ids[:3])} |")
    L += ["", "## Joins", "",
          "- Record -> raw: every procedure's raw is the exact byte slice of its record in the download (`adapter.py check` re-cuts them).",
          "- Procedure -> unit: one record, one `proc:base:<nAnuncio>.<IdIncm>` unit; `consumer_ids.n_anuncio` keeps nAnuncio for the BASE contratos join (E2).",
          "- Alteration and rectification notices -> procedure: none. The dump carries no reference to the notice they change.",
          "- Fact -> raw record and field: every fact's origin is its record's raw and the source field of its mapping row.", ""]
    return "\n".join(L)


# ---- commands ------------------------------------------------------------------------------------------------------
def write(files, data_root: Path, force=False):
    for rel, data in sorted(files.items()):
        p = data_root / rel
        if p.exists():
            if p.read_bytes() == data:
                continue
            if not force:
                raise SystemExit(f"{p} exists with other bytes; nothing is rewritten")
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(data)


def stored_dump(data_root: Path):
    for f in sorted((data_root / f"raw/{SOURCE}/raw").glob("*.jsonl")):
        for line in f.read_text(encoding="utf-8").splitlines():
            o = json.loads(line)
            if o["kind"] == "dump":
                return o
    raise SystemExit("no raw of kind dump under data/raw/base-anuncios/raw/")


def cmd_build(a):
    dump = Path(a.dump).read_bytes()
    files, stats = build(dump, a.url, a.captured_at, a.recorded_at, a.principal)
    data_root = ROOT / a.data
    write(files, data_root, a.force)
    stats["nifs"] = nifs_of(files)
    (HERE / "COVERAGE.md").write_text(coverage_md(stats), encoding="utf-8")
    (HERE / "build.json").write_text(json.dumps({"tool": VERSION, "url": a.url, "captured_at": a.captured_at, "recorded_at": a.recorded_at,
                                                 "principal": a.principal, "dump_sha256": stats["dump_sha"], "files": len(files)},
                                                ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"records": stats["records"], "procs": sum(stats["procs_by_month"].values()), "facts": stats["facts"],
                      "entities": len(stats["entities"]), "files": len(files)}))


def nifs_of(files):
    out = set()
    for rel, data in files.items():
        if rel.startswith("facts/facto/"):
            for line in data.decode("utf-8").splitlines():
                o = json.loads(line)
                if o["field"] == "adjudicante":
                    out.add(o["value"])
    return out


def cmd_check(a):
    data_root = ROOT / a.data
    meta = json.loads((HERE / "build.json").read_text(encoding="utf-8"))
    raw = stored_dump(data_root)
    dump = (data_root / raw["bytes"]).read_bytes()
    if sha256_bytes(dump) != raw["sha256"]:
        raise SystemExit("the stored download does not hash to its raw's sha256")
    files, stats = build(dump, raw["url"], raw["captured_at"], meta["recorded_at"], meta["principal"])
    stats["nifs"] = nifs_of(files)
    bad = [rel for rel, data in sorted(files.items()) if not (data_root / rel).exists() or (data_root / rel).read_bytes() != data]
    ours = {f"raw/{SOURCE}/raw", "facts/unidade", "facts/facto", "facts/alias", "facts/link", "facts/entidade", "facts/adaptador"}
    extra = [str(p.relative_to(data_root)) for d in ours for p in sorted((data_root / d).glob(f"{SOURCE}*")) if str(p.relative_to(data_root)) not in files]
    if (HERE / "COVERAGE.md").read_text(encoding="utf-8") != coverage_md(stats):
        bad.append("adapters/base-anuncios/COVERAGE.md")
    for rel in bad + extra:
        print("DIFFERS" if rel in bad else "EXTRA", rel)
    print(f"check: {len(files)} files re-derived from {raw['id']}; {len(bad)} differ, {len(extra)} extra")
    return 1 if bad or extra else 0


def cmd_register(a):
    sys.path.insert(0, str(ROOT / "tools"))
    import register_tool  # noqa: E402  (the builder's registration of a ferramenta by the sha256 of its code)
    from engine.governance import Log
    gov = ROOT / "governance"
    code = str(Path(__file__).resolve().relative_to(ROOT))
    pid = register_tool.register(gov, TOOL, code, "BASE anúncios dump -> raw, proc units, facts, adjudicante entities (extractor E1)")
    log = Log(gov)
    aid = MAPPING["adaptador"]["id"]
    payload = {"code": code, "code_sha256": sha256_bytes(Path(__file__).read_bytes()), "mapping": "adapters/base-anuncios/mapping.json",
               "mapping_sha256": content_hash(MAPPING["adaptador"]["mapping"])}
    known = [ev for _, ev in log.events if ev["assertion_type"] == "adaptador" and ev["assertion"] == aid and ev["action"] in ("propose", "correct")]
    if not known:
        print(pid, log.propose(pid, "adaptador", aid, payload, a.at))
    elif known[-1]["payload"] != payload:
        rev = log.replay().assertions[("adaptador", aid)]["revision"]
        print(pid, log.correct(pid, "adaptador", aid, rev, payload, "the adapter's code changed; same mapping", a.at))
    else:
        print(pid, "already proposed with this code and mapping")
    return 0


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    b = sub.add_parser("build")
    b.add_argument("--dump", required=True); b.add_argument("--url", required=True); b.add_argument("--captured-at", required=True)
    b.add_argument("--recorded-at", required=True); b.add_argument("--principal", required=True)
    b.add_argument("--data", default="data"); b.add_argument("--force", action="store_true")
    c = sub.add_parser("check"); c.add_argument("--data", default="data")
    r = sub.add_parser("register"); r.add_argument("--at", required=True)
    a = ap.parse_args()
    return {"build": cmd_build, "check": cmd_check, "register": cmd_register}[a.cmd](a) or 0


if __name__ == "__main__":
    sys.exit(main())
