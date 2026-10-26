"""The BASE history 2018–2026 into Postgres (DECISIONS D49): the dumps the extractor stored (Storage ccp-raw, H.1/H.2)
read through the adapters' own mapping code, straight into schema ccp, one year at a time; nothing is written to data/.

    .venv/bin/python -I db/history.py anuncios  --workdir W --recorded-at T [--years 2018-2025]
    .venv/bin/python -I db/history.py contratos --workdir W --recorded-at T [--years 2018-2026]
    .venv/bin/python -I db/history.py ted       --workdir W --recorded-at T [--years 2018-2026]

anuncios   each year's anúncios dump through adapters/base-anuncios build() unchanged: the dump's raw, one raw per mapped
           record, the proc units and their facts. Entities, aliases and links are not loaded here: across nine years
           they are the entity layer's own step (E2), not a by-product of one year's build.
contratos  each year's contratos zip through the field mapping of adapters/base-contratos (contract_values, unchanged),
           generalised from its one-month sample to every contract: a contract whose idcontrato appears in more than one
           record, in any year, with different bytes is refused (the same bytes twice keep the first year's record); a
           contract without a publication date has no valid_at and is refused; a contract joins the anúncio procedure
           whose key it names, else its procedure is a proc unit idproc-<idprocedimento> built from all its contracts of
           all years, with a procedure field only when every contract gives it and all agree (the adapter's rule).
           Modifications: the 2026 dump (the only year the extractor fetched), for the contracts loaded.
ted        each month's bundle of Portuguese notices (H.5, Storage ccp-raw/ted) through adapters/ted/adapter.py: one raw
           per notice (its member's sha256 checked against the month's index), and for competition notices a proc unit
           proc:ted:<publication number> with its facts. Not joined to BASE procedures yet (no shared identifier).

A record's raw names the sha256 of its exact byte slice; for these years the slices are not stored as files: the dump
is in Storage and cutting it again (the adapters' records()) gives the same bytes (D49). Dumps come from the local
extractor store when present, else from Storage with the Supabase CLI linked in --workdir (no key handled here); every
dump's sha256 is checked before use. The report (rows per year, refusals by reason, facts per field) goes to
reports/data/. Same dumps and --recorded-at, same objects; rows already present are skipped.
"""
import argparse
import datetime
import hashlib
import importlib.util
import io
import json
import subprocess
import sys
import tempfile
import zipfile
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from db import pg  # noqa: E402
from engine import schema  # noqa: E402
from engine.canon import sha256_bytes  # noqa: E402

CLI = str(Path.home() / "bin/supabase")
BUCKET = "ccp-raw"
EXTRACTOR = ROOT.parent.parent.parent / ".worktrees/extractor-e1-base-anuncios-6a70d2" if ".worktrees" in ROOT.parts else ROOT
LOCAL = [EXTRACTOR / "data/raw/{source}/raw_bytes/{sha}", EXTRACTOR / "data/raw_bytes/{sha}"]
REPORTS = ROOT / "reports/data"


def adapter(name):
    spec = importlib.util.spec_from_file_location(name.replace("-", "_"), ROOT / f"adapters/{name}/adapter.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


# ---- the dumps -------------------------------------------------------------------------------------------------------
def history_raws():
    """The extractor's raws of the yearly dumps (H.1), with 2026 from E1 and the October sample (same resources)."""
    log = [json.loads(l) for l in (ROOT / "adapters/base-historico/fetch-log.jsonl").read_text(encoding="utf-8").splitlines()]
    out = {(e["kind"], e["year"]): {"url": e["url"], "sha256": e["sha256"], "at": e["at"]} for e in log if e.get("sha256")}
    a = json.loads((ROOT / "adapters/base-anuncios/build.json").read_text(encoding="utf-8"))
    out[("anuncios", 2026)] = {"url": a["url"], "sha256": a["dump_sha256"], "at": a["captured_at"]}
    c = json.loads((ROOT / "adapters/base-contratos/build.json").read_text(encoding="utf-8"))
    out[("contratos", 2026)] = {"url": c["contratos"]["url"], "sha256": c["contratos"]["sha256"], "at": c["contratos"]["at"]}
    out[("modificacoes", 2026)] = {"url": c["modificacoes"]["url"], "sha256": c["modificacoes"]["sha256"], "at": c["modificacoes"]["at"]}
    return out


def cli(workdir, *args):
    r = subprocess.run([CLI, "storage", *args, "--linked", "--experimental", "--workdir", workdir], capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError((r.stdout + r.stderr).strip()[-300:])


def fetch(sha, sources, workdir):
    """The dump's bytes, checked against its sha256: the local extractor copy, else Storage (whole, or in parts)."""
    for source in sources:
        for pattern in LOCAL:
            p = Path(str(pattern).format(source=source, sha=sha))
            if p.exists():
                data = p.read_bytes()
                if sha256_bytes(data) == sha:
                    return data
    with tempfile.TemporaryDirectory() as t:
        for source in sources:
            obj, dst = f"ss:///{BUCKET}/{source}/raw_bytes/{sha}", f"{t}/{source}-{sha}"   # a failed cp leaves an empty file behind
            try:
                cli(workdir, "cp", obj, dst)
                data = Path(dst).read_bytes()
            except RuntimeError:
                try:
                    cli(workdir, "cp", obj + ".manifest.json", f"{t}/{source}-m.json")
                except RuntimeError:
                    continue
                parts = json.loads(Path(f"{t}/{source}-m.json").read_text(encoding="utf-8"))["parts"]
                data = b""
                for i, part in enumerate(sorted(parts, key=lambda x: x["order"])):   # the offload's split: byte ranges in order
                    name = part["name"]
                    cli(workdir, "cp", f"ss:///{BUCKET}/{source}/raw_bytes/{name}", f"{t}/{source}-p{i}")
                    data += Path(f"{t}/{source}-p{i}").read_bytes()
            if sha256_bytes(data) != sha:
                raise SystemExit(f"{source}/{sha}: the bytes from Storage do not hash to their name")
            return data
    raise SystemExit(f"{sha}: neither in the local extractor store nor in Storage ({', '.join(sources)})")


def dump_raw(source, url, data, at, recorded_at, media):
    res = url.rstrip("/").split("/")
    sha = sha256_bytes(data)
    return {"id": f"raw:{source}:dump:{res[-1]}.{res[-2]}", "revision": 1, "recorded_at": recorded_at, "source": source, "kind": "dump",
            "source_id": f"{res[-2]}/{res[-1]}", "sha256": sha, "bytes": f"raw_bytes/{sha}", "media_type": media,
            "encoding": "binary" if media == "application/zip" else "utf-8", "url": url, "captured_at": at,
            "request": {"method": "GET", "reads_of_page": 1}}


def checked(objects):
    for type_, objs in objects.items():
        for o in objs:
            errs = schema.validate(type_, o)
            if errs:
                raise SystemExit(f"{type_} {o.get('id')}: {errs[0]}")
    return objects


# ---- anúncios ----------------------------------------------------------------------------------------------------------
def load_anuncios(conn, dumps, get, recorded_at, keep=None):
    """dumps: {year: {url, sha256, at}}; get(dump, sources) -> its bytes. keep(year, files) sees each build (db/daily.py)."""
    ad = adapter("base-anuncios")
    rep = {}
    for y, d in dumps.items():
        data = get(d, ["base-historico", "base-anuncios"])
        files, st = ad.build(data, d["url"], d["at"], recorded_at, "ferramenta:adapter-base-anuncios@2")
        objects = defaultdict(list)
        for path, blob in files.items():
            type_ = "raw" if path.startswith("raw/") else Path(path).parent.name
            if path.startswith("raw_bytes/") or type_ not in ("raw", "unidade", "facto"):
                continue
            objects[type_] += [json.loads(l) for l in blob.decode("utf-8").splitlines() if l.strip()]
        counts = pg.load_objects(conn, dict(objects))
        if keep:
            keep(y, files)
        rep[y] = {"dump": d, "records": st["records"], "procedures": sum(st["procs_by_month"].values()), "facts": st["facts"],
                  "unmapped": {k: len(v) for k, v in st["unmapped"].items()},
                  "fields": {f: sum(c.values()) for f, c in st["field_counts"].items()},
                  "omitted": {f: {r: len(ids) for r, ids in rs.items()} for f, rs in st["omitted"].items()}, "load": counts}
        print(y, json.dumps({k: rep[y][k] for k in ("records", "procedures", "facts", "load")}), flush=True)
        del files, objects, data
    return rep


# ---- TED -----------------------------------------------------------------------------------------------------------
def load_ted(conn, years, get, recorded_at):
    import tarfile
    spec = importlib.util.spec_from_file_location("ted_adapter", ROOT / "adapters/ted/adapter.py")
    ted = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(ted)
    manifest = json.loads((ROOT / "adapters/ted/manifest.json").read_text(encoding="utf-8"))
    rep = {}
    for month in manifest:
        if int(month["month"][:4]) not in years:
            continue
        index = json.loads(get({"sha256": month["index_sha256"]}, ["ted"]))
        bundle = tarfile.open(fileobj=io.BytesIO(get({"sha256": month["pt_bundle_sha256"]}, ["ted"])))
        objects = {"raw": [], "unidade": [], "facto": []}
        st = {"notices": 0, "kinds": Counter(), "procedures": 0, "fields": Counter(), "why": defaultdict(Counter)}
        for m in index["kept"]:
            xml = bundle.extractfile(m["member"].replace("!", "/")).read()   # the index writes a nested package as name!member
            if sha256_bytes(xml) != m["sha256"]:
                raise SystemExit(f"ted {month['month']} {m['member']}: bytes differ from the index")
            raw, unit, facts, why, kind = ted.notice(xml, m, month, recorded_at)
            st["notices"] += 1; st["kinds"][kind] += 1
            objects["raw"].append(raw)
            if unit:
                st["procedures"] += 1
                objects["unidade"].append(unit)
                objects["facto"] += facts
                for f in facts:
                    st["fields"][f["field"]] += 1
                for f, r in why.items():
                    st["why"][f][r] += 1
        counts = pg.load_objects(conn, checked(objects))
        rep[month["month"]] = {"notices": st["notices"], "kinds": dict(st["kinds"]), "procedures": st["procedures"], "fields": dict(st["fields"]),
                               "why": {f: dict(c) for f, c in st["why"].items()}, "load": counts}
        print(month["month"], json.dumps({"notices": st["notices"], "procedures": st["procedures"], "facts": sum(st["fields"].values())}), flush=True)
    return rep


# ---- contratos -------------------------------------------------------------------------------------------------------
def year_records(ad, data, year):
    with zipfile.ZipFile(io.BytesIO(data)) as z:
        names = [n for n in z.namelist() if n.lower().endswith(".json")]
        if len(names) != 1:
            raise SystemExit(f"contratos {year}: {names}: not one JSON member")
        return ad.records(z.read(names[0]).decode("utf-8"))


def notice_keys(conn):
    """The anúncio procedures in the store: the keys a contract may name."""
    rows = conn.execute("""select n.txt from ccp.unidade_c u join ccp.nome n on n.no = u.id join ccp.nome k on k.no = u.kind
                           where k.txt = 'proc' and n.txt like 'proc:base:%' and n.txt not like 'proc:base:idproc-%'""").fetchall()
    return {r[0].split(":", 2)[2] for r in rows}


def load_contratos(conn, dumps, mods_dump, get, recorded_at, unchanged=()):
    """dumps: {year: {url, sha256, at}} of every year (the procedures without a notice gather contracts of all years);
    mods_dump: the modifications dump; unchanged: years already loaded from these same bytes, read but not written again."""
    ad = adapter("base-contratos")
    blobs = {y: get(d, ["base-historico", "base-contratos"]) for y, d in dumps.items()}   # about 340 MB in all
    # pass 0: which idcontrato appear more than once, and whether with the same bytes
    seen = defaultdict(set)
    for y, d in dumps.items():
        for rec, b in year_records(ad, blobs[y], y):
            seen[rec["idcontrato"]].add((hashlib.sha256(b).digest()[:12], y))
    keys = notice_keys(conn)
    rep = {"years": {}, "refused": Counter(), "procs_new": 0, "notices_known": len(keys)}
    procs = defaultdict(list)
    loaded_ids = set()
    for y, d in dumps.items():
        data = blobs.pop(y)
        zraw = dump_raw("base-contratos", d["url"], data, d["at"], recorded_at, "application/zip")
        objects = {"raw": [zraw], "unidade": [], "facto": []}
        st = {"records": 0, "contracts": 0, "joined": 0, "refused": Counter(), "fields": Counter(), "why": defaultdict(Counter)}
        for rec, b in year_records(ad, data, y):
            st["records"] += 1
            cid = rec["idcontrato"]
            versions = seen[cid]
            if len({h for h, _ in versions}) > 1:
                st["refused"]["idcontrato held by records with different bytes"] += 1
                continue
            if min(yy for _, yy in versions) != y or cid in loaded_ids:
                st["refused"]["the same record again (kept once, first year)"] += 1
                continue
            got, why = ad.contract_values(rec)
            valid_at = got.get("data_publicacao_contrato", (None,))[0]
            if valid_at is None:
                st["refused"]["no publication date: no valid_at"] += 1
                continue
            loaded_ids.add(cid)
            rid = f"raw:base-contratos:contrato:{cid}"
            objects["raw"].append(ad.raw_obj(rid, "base-contratos", "contrato", cid, b, d["url"], d["at"], recorded_at))
            joined = bool(rec.get("nAnuncio")) and ad.key_of(rec) in keys
            parent = f"proc:base:{ad.key_of(rec)}" if joined else f"proc:base:idproc-{rec['idprocedimento']}"
            st["joined"] += joined
            cunit = f"contrato:base:{cid}"
            objects["unidade"].append({"id": cunit, "revision": 1, "recorded_at": recorded_at, "kind": "contrato", "parent": parent,
                                       "raw": [rid], "consumer_ids": {"base_id": cid}})
            for f in ad.CONTRACT_FIELDS:
                if f in got:
                    objects["facto"].append(ad.fact(cunit, f, got[f][0], rid, got[f][1], valid_at, d["at"], recorded_at)); st["fields"][f] += 1
                else:
                    st["why"][f][why[f]] += 1
            if not joined:
                procs[parent].append((cid, rid, {f: got[f] for f in ad.PROC_FIELDS if f in got}, {f: why[f] for f in ad.PROC_FIELDS if f in why},
                                      valid_at, d["at"]))
            st["contracts"] += 1
        counts = "unchanged: not written" if y in unchanged else pg.load_objects(conn, checked(objects))
        rep["years"][y] = {"dump": d, **{k: v for k, v in st.items() if k not in ("why",)}, "why": {f: dict(c) for f, c in st["why"].items()}, "load": counts}
        rep["refused"].update(st["refused"])
        print(y, json.dumps({"records": st["records"], "contracts": st["contracts"], "joined": st["joined"], "refused": dict(st["refused"]),
                             "load": counts}), flush=True)
        del data, objects
    # the procedures without a notice, from all their contracts of all years
    objects, pst = {"unidade": [], "facto": []}, {"fields": Counter(), "why": defaultdict(Counter)}
    for pid, items in sorted(procs.items()):
        objects["unidade"].append({"id": pid, "revision": 1, "recorded_at": recorded_at, "kind": "proc", "parent": None,
                                   "raw": sorted(i[1] for i in items), "consumer_ids": {"base_id": pid.split("idproc-")[1]}})
        first = min(items, key=lambda i: i[0])
        for f in ad.PROC_FIELDS:
            vals = {json.dumps(i[2][f][0]) for i in items if f in i[2]}
            if f in first[2] and len(vals) == 1 and all(f in i[2] for i in items):
                objects["facto"].append(ad.fact(pid, f, first[2][f][0], first[1], first[2][f][1], first[4], first[5], recorded_at)); pst["fields"][f] += 1
            elif len(vals) > 1:
                pst["why"][f]["contracts of the procedure disagree"] += 1
            else:
                pst["why"][f][first[3].get(f, "absent in one contract")] += 1
    rep["procs_new"] = len(procs)
    rep["procedures"] = {"fields": dict(pst["fields"]), "why": {f: dict(c) for f, c in pst["why"].items()},
                         "load": pg.load_objects(conn, checked(objects))}
    print("procedures", json.dumps({"new": len(procs), "load": rep["procedures"]["load"]}), flush=True)
    # modifications: the 2026 dump, for the contracts loaded
    m = mods_dump
    mdata = get(m, ["base-modificacoes"])
    objects = {"raw": [dump_raw("base-modificacoes", m["url"], mdata, m["at"], recorded_at, "application/json")], "unidade": [], "facto": []}
    seq = Counter()
    mods = [(r, b) for r, b in ad.records(mdata.decode("utf-8")) if r["idcontrato"] in loaded_ids]
    for r, b in sorted(mods, key=lambda x: (x[0]["idcontrato"], ad.date_pt(x[0]["modifContratoData"]) or "", sha256_bytes(x[1]))):
        seq[r["idcontrato"]] += 1
        mid = f"{r['idcontrato']}.{seq[r['idcontrato']]}"
        rid = f"raw:base-modificacoes:modificacao:{mid}"
        objects["raw"].append(ad.raw_obj(rid, "base-modificacoes", "modificacao", mid, b, m["url"], m["at"], recorded_at))
        unit = f"mod:base:{mid}"
        objects["unidade"].append({"id": unit, "revision": 1, "recorded_at": recorded_at, "kind": "mod", "parent": f"contrato:base:{r['idcontrato']}",
                                   "raw": [rid], "consumer_ids": {"base_id": r["idcontrato"]}})
        dd = ad.date_pt(r.get("modifContratoData"))
        if dd:
            objects["facto"].append(ad.fact(unit, "data_modificacao", dd, rid, "modifContratoData", dd, m["at"], recorded_at))
    rep["modificacoes"] = {"dump": m, "records": len(json.loads(mdata)), "of_loaded_contracts": len(mods), "load": pg.load_objects(conn, checked(objects))}
    print("modificacoes", json.dumps(rep["modificacoes"]["load"]), flush=True)
    rep["refused"] = dict(rep["refused"])
    return rep


def years_arg(s):
    a, _, b = s.partition("-")
    return list(range(int(a), int(b or a) + 1))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("what", choices=["anuncios", "contratos", "ted"])
    ap.add_argument("--workdir", required=True)
    ap.add_argument("--recorded-at", required=True)
    ap.add_argument("--years")
    a = ap.parse_args()
    years = years_arg(a.years or ("2018-2025" if a.what == "anuncios" else "2018-2026"))
    raws = history_raws()
    get = lambda d, sources: fetch(d["sha256"], sources, a.workdir)  # noqa: E731
    run = {"anuncios": lambda c: load_anuncios(c, {y: raws[("anuncios", y)] for y in years}, get, a.recorded_at),
           "contratos": lambda c: load_contratos(c, {y: raws[("contratos", y)] for y in years}, raws[("modificacoes", 2026)], get, a.recorded_at),
           "ted": lambda c: load_ted(c, years, get, a.recorded_at)}[a.what]
    with pg.connect() as conn:
        conn.autocommit = True
        rep = run(conn)
        sizes = pg.sizes(conn)
    REPORTS.mkdir(parents=True, exist_ok=True)
    day = datetime.date.today().isoformat()
    out = {"tool": "db/history.py", "what": a.what, "years": years, "recorded_at": a.recorded_at, "report": rep, "sizes_after": sizes}
    (REPORTS / f"historico-{a.what}-{day}.json").write_text(json.dumps(out, ensure_ascii=False, indent=1, sort_keys=True, default=str) + "\n", encoding="utf-8")
    print(json.dumps(sizes))


if __name__ == "__main__":
    main()
