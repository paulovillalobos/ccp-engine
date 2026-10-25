"""BASE contratos 2026 (and modificações 2026, entidades) -> a sample of contract units, their procedures and facts.

    python -I adapters/base-contratos/adapter.py build --contratos ZIP --contratos-url U --contratos-at T
                                                      --modificacoes JSON --modificacoes-url U --modificacoes-at T
                                                      --entidades JSON --entidades-url U --entidades-at T
                                                      --recorded-at T --principal P
    python -I adapters/base-contratos/adapter.py check
    python -I adapters/base-contratos/adapter.py register --at T

build   stores the three downloads under data/raw/<source>/raw_bytes/<sha256> (gitignored), cuts every sampled record's
        exact byte slice out of its JSON array (the contracts out of the zip's one member, Contratos2026.json) and writes
        one raw per download and per sampled record, the units (proc, contrato, mod), the facts of mapping.json with
        origin (raw, field), the adaptador and COVERAGE.md. The sample is the contracts BASE published in mapping.json's
        sample_month, and their modifications. A value that is absent or ambiguous is not a fact. Same inputs, same bytes.
check   rebuilds from the stored downloads and compares every file byte for byte.
register registers this file as ferramenta:adapter-base-contratos and proposes (or corrects) the adaptador in the log.

No model reads anything; nothing is sent anywhere.
"""
import argparse
import datetime
import json
import re
import sys
import zipfile
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
DATA = ROOT / "data"
sys.path.insert(0, str(ROOT))
from engine import schema  # noqa: E402
from engine.canon import canonical, content_hash, sha256_bytes  # noqa: E402

VERSION = "base-contratos-adapter-0.1"
SOURCE, SOURCE_MOD, SOURCE_ENT = "base-contratos", "base-modificacoes", "base-entidades"
TOOL = "adapter-base-contratos"
MEMBER = "Contratos2026.json"
MAPPING = json.loads((HERE / "mapping.json").read_text(encoding="utf-8"))
ROWS = {m["canonical_field"]: m for m in MAPPING["adaptador"]["mapping"]}
NIF_NAME = re.compile(r"([0-9]{9}) - .+")


def records(text):
    """[(record, exact UTF-8 bytes of the record in the array)] of a JSON array of objects."""
    dec, out, i, n = json.JSONDecoder(), [], 0, len(text)

    def skip(i):
        while i < n and text[i] in " \t\r\n":
            i += 1
        return i
    i = skip(i)
    assert text[i] == "[", "not a JSON array"
    i = skip(i + 1)
    while i < n and text[i] != "]":
        obj, end = dec.raw_decode(text, i)
        out.append((obj, text[i:end].encode("utf-8")))
        i = skip(end)
        if text[i] == ",":
            i = skip(i + 1)
    return out


def date_pt(v):
    m = re.fullmatch(r"([0-9]{2})/([0-9]{2})/([0-9]{4})( [0-9:]{8})?", v or "")
    if not m:
        return None
    try:
        return datetime.date(int(m.group(3)), int(m.group(2)), int(m.group(1))).isoformat()
    except ValueError:
        return None


def money(v):
    if isinstance(v, bool) or not isinstance(v, (int, float)) or v <= 0:
        return None
    return int(v) if float(v).is_integer() else v


def e1_keys():
    keys = set()
    for f in sorted((DATA / "raw/base-anuncios/raw").glob("base-anuncios-2*.jsonl")):
        for line in f.read_text(encoding="utf-8").splitlines():
            keys.add(json.loads(line)["id"].split(":", 3)[3])
    return keys


def e1_facts():
    out = defaultdict(dict)
    for f in sorted((DATA / "facts/facto").glob("base-anuncios-*.jsonl")):
        for line in f.read_text(encoding="utf-8").splitlines():
            o = json.loads(line)
            if o["field"] in ("preco_base", "tipo_procedimento", "adjudicante"):
                out[o["unit"]][o["field"]] = o["value"]
    return out


def key_of(rec):
    n = re.sub(r"[^A-Za-z0-9]+", "-", rec["nAnuncio"]).strip("-")
    return f"{n}.{rec['idINCM'] or 'x'}"


def raw_obj(rid, source, kind, source_id, data, url, at, recorded_at, media="application/json", enc="utf-8"):
    sha = sha256_bytes(data)
    return {"id": rid, "revision": 1, "recorded_at": recorded_at, "source": source, "kind": kind, "source_id": source_id, "sha256": sha,
            "bytes": f"raw_bytes/{sha}", "media_type": media, "encoding": enc, "url": url, "captured_at": at,
            "request": {"method": "GET", "reads_of_page": 1}}


def contract_values(rec):
    """{field: (value, source field)} and {field: reason} for one contract."""
    got, why = {}, {}
    m = ROWS["tipo_procedimento"]["enum_map"]
    if rec.get("tipoprocedimento") in m:
        got["tipo_procedimento"] = (m[rec["tipoprocedimento"]], "tipoprocedimento")
    else:
        why["tipo_procedimento"] = f"'{rec.get('tipoprocedimento')}' outside the vocabulary"
    v = money(rec.get("precoBaseProcedimento"))
    (got.__setitem__("preco_base", (v, "precoBaseProcedimento")) if v is not None else why.__setitem__("preco_base", "0 or absent"))
    adj = rec.get("adjudicante") or []
    mm = NIF_NAME.fullmatch(adj[0]) if len(adj) == 1 else None
    (got.__setitem__("adjudicante", (mm.group(1), "adjudicante")) if mm else why.__setitem__("adjudicante", "not one 'NIF - name'"))
    tipos, tm = rec.get("tipoContrato") or [], ROWS["tipo_contrato"]["enum_map"]
    if len(tipos) == 1 and tipos[0] in tm:
        got["tipo_contrato"] = (tm[tipos[0]], "tipoContrato")
    else:
        why["tipo_contrato"] = "several contract types" if len(tipos) > 1 else f"{tipos[:1]} outside the vocabulary"
    v = money(rec.get("precoContratual"))
    (got.__setitem__("preco_contratual", (v, "precoContratual")) if v is not None else why.__setitem__("preco_contratual", "0 or absent"))
    d = date_pt(rec.get("dataCelebracaoContrato"))
    (got.__setitem__("data_celebracao_contrato", (d, "dataCelebracaoContrato")) if d else why.__setitem__("data_celebracao_contrato", "not a date"))
    d = date_pt(rec.get("dataPublicacao"))
    (got.__setitem__("data_publicacao_contrato", (d, "dataPublicacao")) if d else why.__setitem__("data_publicacao_contrato", "not a date"))
    adjs = rec.get("adjudicatarios") or []
    nifs = [NIF_NAME.fullmatch(a) for a in adjs]
    if adjs and all(nifs):
        got["adjudicatario"] = ([x.group(1) for x in nifs], "adjudicatarios")
    else:
        why["adjudicatario"] = "an adjudicatário without NIF ('-')" if adjs else "empty list"
    return got, why


PROC_FIELDS = ("tipo_procedimento", "preco_base", "adjudicante", "tipo_contrato")
CONTRACT_FIELDS = ("preco_contratual", "data_celebracao_contrato", "data_publicacao_contrato", "adjudicatario")


def fact(unit, field, value, raw_id, src, valid_at, known_at, recorded_at):
    return {"id": f"facto:{unit.replace(':', '-')}:{field}:{SOURCE}", "revision": 1, "recorded_at": recorded_at, "unit": unit, "field": field,
            "value": value, "origin": {"raw": raw_id, "field": src}, "adapter": MAPPING["adaptador"]["id"], "valid_at": valid_at, "known_at": known_at}


def build(src, recorded_at, principal):
    """src: {name: (bytes, url, captured_at)} for contratos (zip), modificacoes, entidades."""
    files, st = {}, {"why": defaultdict(lambda: defaultdict(list)), "field": Counter(), "cross": Counter(), "cross_ex": defaultdict(list)}
    zbytes, zurl, zat = src["contratos"]
    mbytes, murl, mat = src["modificacoes"]
    ebytes, eurl, eat = src["entidades"]
    raws = defaultdict(list)
    for name, (data, url, at), source, media in (("contratos", src["contratos"], SOURCE, "application/zip"), ("modificacoes", src["modificacoes"], SOURCE_MOD, "application/json"),
                                                 ("entidades", src["entidades"], SOURCE_ENT, "application/json")):
        files[f"raw/{source}/raw_bytes/{sha256_bytes(data)}"] = data
        res = url.rstrip("/").split("/")
        raws[source].append(raw_obj(f"raw:{source}:dump:{res[-1]}.{res[-2]}", source, "dump", f"{res[-2]}/{res[-1]}", data, url, at, recorded_at,
                                    media, "binary" if media == "application/zip" else "utf-8"))
    import io
    with zipfile.ZipFile(io.BytesIO(zbytes)) as z:
        ctext = z.read(MEMBER).decode("utf-8")
    allc = records(ctext)
    st["contracts_year"] = len(allc)
    ids = Counter(r["idcontrato"] for r, _ in allc)
    month = MAPPING["sample_month"]
    sample = [(r, b) for r, b in allc if (date_pt(r.get("dataPublicacao")) or "")[:7] == month]
    st["contracts_sample"] = len(sample)
    st["tipoprocedimento"] = Counter(r["tipoprocedimento"] for r, _ in sample)
    st["regime"] = Counter(r.get("regime") or "(vazio)" for r, _ in sample)
    st["fundamentacao"] = Counter(r.get("fundamentacao") or "(vazio)" for r, _ in sample)
    keys, base = e1_keys(), e1_facts()
    units, facts, procs = {}, [], defaultdict(list)
    st["refused"] = defaultdict(list)
    for rec, b in sorted(sample, key=lambda x: x[0]["idcontrato"]):
        cid = rec["idcontrato"]
        if ids[cid] > 1:
            st["refused"]["idcontrato held by more than one record of the year"].append(cid)
            continue
        rid = f"raw:{SOURCE}:contrato:{cid}"
        raws[SOURCE].append(raw_obj(rid, SOURCE, "contrato", cid, b, zurl, zat, recorded_at))
        files[f"raw/{SOURCE}/raw_bytes/{sha256_bytes(b)}"] = b
        joined = bool(rec.get("nAnuncio")) and key_of(rec) in keys
        parent = f"proc:base:{key_of(rec)}" if joined else f"proc:base:idproc-{rec['idprocedimento']}"
        st["cross"]["joined to a notice of adaptador:base-anuncios" if joined else "procedure without a notice in E1 (new proc unit)"] += 1
        got, why = contract_values(rec)
        valid_at = got.get("data_publicacao_contrato", (None,))[0] or f"{month}-01"
        cunit = f"contrato:base:{cid}"
        units[cunit] = {"id": cunit, "revision": 1, "recorded_at": recorded_at, "kind": "contrato", "parent": parent, "raw": [rid], "consumer_ids": {"base_id": cid}}
        for f in CONTRACT_FIELDS:
            if f in got:
                facts.append(fact(cunit, f, got[f][0], rid, got[f][1], valid_at, zat, recorded_at)); st["field"][f] += 1
            else:
                st["why"][f][why[f]].append(cid)
        if joined:
            e1 = base.get(parent, {})
            for f in ("preco_base", "tipo_procedimento", "adjudicante"):
                if f in got and f in e1:
                    same = got[f][0] == e1[f]
                    st["cross"][f"{f} {'equals' if same else 'differs from'} the notice's"] += 1
                    if not same:
                        st["cross_ex"][f].append(cid)
        else:
            procs[parent].append((rec, rid, got, why, valid_at))
    for pid, items in sorted(procs.items()):
        units[pid] = {"id": pid, "revision": 1, "recorded_at": recorded_at, "kind": "proc", "parent": None, "raw": sorted(i[1] for i in items),
                      "consumer_ids": {"base_id": pid.split("idproc-")[1]}}
        first = min(items, key=lambda i: i[0]["idcontrato"])
        for f in PROC_FIELDS:
            vals = {json.dumps(i[2][f][0]) for i in items if f in i[2]}
            if f in first[2] and len(vals) == 1 and all(f in i[2] for i in items):
                facts.append(fact(pid, f, first[2][f][0], first[1], first[2][f][1], first[4], zat, recorded_at)); st["field"][f] += 1
            elif len(vals) > 1:
                st["why"][f]["contracts of the procedure disagree"].append(pid)
            else:
                st["why"][f][first[3].get(f, "absent in one contract")].append(pid)
    st["procs_new"] = len(procs)
    sample_ids = {u.split(":")[2] for u in units if u.startswith("contrato:")}
    mods = [(r, b) for r, b in records(mbytes.decode("utf-8")) if r["idcontrato"] in sample_ids]
    st["mods_year"] = len(json.loads(mbytes))
    seq = Counter()
    for r, b in sorted(mods, key=lambda x: (x[0]["idcontrato"], date_pt(x[0]["modifContratoData"]) or "", sha256_bytes(x[1]))):
        seq[r["idcontrato"]] += 1
        mid = f"{r['idcontrato']}.{seq[r['idcontrato']]}"
        rid = f"raw:{SOURCE_MOD}:modificacao:{mid}"
        raws[SOURCE_MOD].append(raw_obj(rid, SOURCE_MOD, "modificacao", mid, b, murl, mat, recorded_at))
        files[f"raw/{SOURCE_MOD}/raw_bytes/{sha256_bytes(b)}"] = b
        unit = f"mod:base:{mid}"
        units[unit] = {"id": unit, "revision": 1, "recorded_at": recorded_at, "kind": "mod", "parent": f"contrato:base:{r['idcontrato']}", "raw": [rid], "consumer_ids": {"base_id": r["idcontrato"]}}
        d = date_pt(r.get("modifContratoData"))
        if d:
            facts.append(fact(unit, "data_modificacao", d, rid, "modifContratoData", d, mat, recorded_at)); st["field"]["data_modificacao"] += 1
    st["mods_sample"] = len(mods)
    ents = json.loads(ebytes)
    st["entidades"] = {"records": len(ents), "fields": sorted({k for e in ents for k in e}), "countries": len({e.get("AliasPais") for e in ents}),
                       "without_nif": sum(1 for e in ents if not re.fullmatch(r"[0-9]{9}", e.get("nifEntidade") or ""))}
    tag = f"{SOURCE}-{month}"
    for source, objs in raws.items():
        files[f"raw/{source}/raw/{source}-{month}.jsonl"] = jsonl(sorted(objs, key=lambda o: o["id"]))
    files[f"facts/unidade/{tag}.jsonl"] = jsonl(sorted(units.values(), key=lambda o: o["id"]))
    files[f"facts/facto/{tag}.jsonl"] = jsonl(sorted(facts, key=lambda o: o["id"]))
    a = MAPPING["adaptador"]
    adaptador = {"id": a["id"], "revision": 1, "recorded_at": recorded_at, "source": a["source"], "version": a["version"], "code": a["code"], "mapping": a["mapping"],
                 "coverage": [{"period": month, "expected": st["contracts_sample"], "captured": sum(1 for u in units if u.startswith("contrato:"))}],
                 "proposed_by": principal, "state": "proposed"}
    files[f"facts/adaptador/{SOURCE}-{a['version']}.json"] = (json.dumps(adaptador, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    st["units"] = Counter(u.split(":")[0] for u in units)
    st["facts"] = len(facts)
    for rel, data in files.items():
        if "/raw_bytes/" in rel:
            continue
        type_ = Path(rel).parent.name
        text = data.decode("utf-8")
        for line in (text.splitlines() if rel.endswith(".jsonl") else [text]):
            o = json.loads(line)
            errs = schema.validate(type_, o)
            if errs:
                raise SystemExit(f"{rel}: {o.get('id')}: {errs[0]}")
    return files, st


def jsonl(objs):
    return "".join(canonical(o) + "\n" for o in objs).encode("utf-8")


def coverage_md(st, meta):
    L = ["# BASE contratos 2026 (sample): coverage of adaptador:base-contratos@1", "",
         f"Generated by `adapters/base-contratos/adapter.py` ({VERSION}); `adapter.py check` re-derives it byte for byte.",
         "A sample by the person's decision of 2026-10-25 (BUILD-LOG M.0): the contracts BASE published in October 2026.", "",
         "## Sources (one GET each, bytes in data/raw/<source>/raw_bytes/, not in git)", "", "| source | URL | fetched | sha256 |", "|---|---|---|---|"]
    for k in ("contratos", "modificacoes", "entidades"):
        L.append(f"| {k} | {meta[k]['url']} | {meta[k]['at']} | `{meta[k]['sha256'][:16]}…` |")
    L += ["", "## Records, units, joins", "",
          f"- Contracts in the 2026 dump: {st['contracts_year']}; published in October 2026 (the sample): {st['contracts_sample']}.",
          f"- Refused: {', '.join(f'{k}: {len(v)}' for k, v in st['refused'].items()) or 'none'}.",
          f"- Units written: {dict(st['units'])}; facts written: {st['facts']}.",
          f"- Modifications in the 2026 dump: {st['mods_year']}; of sampled contracts: {st['mods_sample']}.", ""]
    for k, v in sorted(st["cross"].items()):
        L.append(f"- {k}: {v}" + (f" (e.g. {', '.join(st['cross_ex'][k.split()[0]][:3])})" if "differs" in k else ""))
    L += ["", "## Facts per canonical field", "", "| field | facts | without a fact, by reason |", "|---|---:|---|"]
    for f in list(ROWS):
        reasons = "; ".join(f"{r} {len(ids)} (e.g. {', '.join(ids[:3])})" for r, ids in sorted(st["why"].get(f, {}).items(), key=lambda kv: -len(kv[1])))
        L.append(f"| {f} | {st['field'].get(f, 0)} | {reasons or '-'} |")
    L += ["", "## Procedure types in the sample (tipoprocedimento)", ""]
    L += [f"- {k}: {v}" for k, v in st["tipoprocedimento"].most_common()]
    L += ["", "## Declared, not facts (regime, fundamentação)", "",
          "What the entity declared is an assertion, not a fact; converting it to passage ids is a registered principal's step with a log event, not done here.", "",
          "| regime declared | contracts |", "|---|---:|"] + [f"| {k} | {v} |" for k, v in st["regime"].most_common(8)]
    L += ["", "| fundamentação declared (top 8) | contracts |", "|---|---:|"] + [f"| {k} | {v} |" for k, v in st["fundamentacao"].most_common(8)]
    e = st["entidades"]
    L += ["", "## Entidades (downloaded, recorded, not mapped)", "",
          f"- {e['records']} records; fields: {', '.join(e['fields'])}; {e['countries']} countries; {e['without_nif']} without a nine-digit NIF.",
          "- No field says whether an entity is public or private, so this dataset does not settle entidade.type (SCHEMA-PROPOSAL of base-anuncios, item 4). "
          "It gives the country of entities without a Portuguese NIF, which the name candidates of E2 will need.",
          "- No entidade object is written in this sample: the NIFs of E1's entities would need new revisions with these roles; E2 does that.", ""]
    return "\n".join(L)


def cmd_build(a):
    src = {"contratos": (Path(a.contratos).read_bytes(), a.contratos_url, a.contratos_at), "modificacoes": (Path(a.modificacoes).read_bytes(), a.modificacoes_url, a.modificacoes_at),
           "entidades": (Path(a.entidades).read_bytes(), a.entidades_url, a.entidades_at)}
    files, st = build(src, a.recorded_at, a.principal)
    for rel, data in sorted(files.items()):
        p = DATA / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        if not p.exists() or p.read_bytes() != data:
            p.write_bytes(data)
    meta = {k: {"url": v[1], "at": v[2], "sha256": sha256_bytes(v[0])} for k, v in src.items()}
    meta.update(recorded_at=a.recorded_at, principal=a.principal, tool=VERSION)
    (HERE / "build.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (HERE / "COVERAGE.md").write_text(coverage_md(st, meta), encoding="utf-8")
    print(json.dumps({"sample": st["contracts_sample"], "units": dict(st["units"]), "facts": st["facts"], "files": len(files)}))
    return 0


def cmd_check(a):
    meta = json.loads((HERE / "build.json").read_text(encoding="utf-8"))
    dirs = {"contratos": SOURCE, "modificacoes": SOURCE_MOD, "entidades": SOURCE_ENT}
    src = {k: ((DATA / f"raw/{dirs[k]}/raw_bytes/{meta[k]['sha256']}").read_bytes(), meta[k]["url"], meta[k]["at"]) for k in dirs}
    files, st = build(src, meta["recorded_at"], meta["principal"])
    bad = [rel for rel, data in sorted(files.items()) if not (DATA / rel).exists() or (DATA / rel).read_bytes() != data]
    if (HERE / "COVERAGE.md").read_text(encoding="utf-8") != coverage_md(st, meta):
        bad.append("adapters/base-contratos/COVERAGE.md")
    for rel in bad:
        print("DIFFERS", rel)
    print(f"check: {len(files)} files re-derived; {len(bad)} differ")
    return 1 if bad else 0


def cmd_register(a):
    sys.path.insert(0, str(ROOT / "tools"))
    import register_tool  # noqa: E402
    from engine.governance import Log
    gov = ROOT / "governance"
    code = str(Path(__file__).resolve().relative_to(ROOT))
    pid = register_tool.register(gov, TOOL, code, "BASE contratos / modificações / entidades sample -> units, facts (extractor, sample M)")
    log = Log(gov)
    aid = MAPPING["adaptador"]["id"]
    payload = {"code": code, "code_sha256": sha256_bytes(Path(__file__).read_bytes()), "mapping_sha256": content_hash(MAPPING["adaptador"]["mapping"])}
    known = [ev for _, ev in log.events if ev["assertion_type"] == "adaptador" and ev["assertion"] == aid and ev["action"] in ("propose", "correct")]
    if not known:
        print(pid, log.propose(pid, "adaptador", aid, payload, a.at))
    elif known[-1]["payload"] != payload:
        print(pid, log.correct(pid, "adaptador", aid, log.replay().assertions[("adaptador", aid)]["revision"], payload, "the adapter's code changed", a.at))
    else:
        print(pid, "already proposed with this code and mapping")
    return 0


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    b = sub.add_parser("build")
    for k in ("contratos", "modificacoes", "entidades"):
        b.add_argument(f"--{k}", required=True); b.add_argument(f"--{k}-url", required=True); b.add_argument(f"--{k}-at", required=True)
    b.add_argument("--recorded-at", required=True); b.add_argument("--principal", required=True)
    sub.add_parser("check")
    r = sub.add_parser("register"); r.add_argument("--at", required=True)
    a = ap.parse_args()
    return {"build": cmd_build, "check": cmd_check, "register": cmd_register}[a.cmd](a) or 0


if __name__ == "__main__":
    sys.exit(main())
