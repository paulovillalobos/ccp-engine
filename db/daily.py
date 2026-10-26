"""The daily ingest (DECISIONS D49): BASE, DR and TED kept current in schema ccp, each source's run recorded in
ccp.ingesta (its health: ccp.saude).

    .venv/bin/python -I db/daily.py run --work DIR [--only base,dr,ted] [--dr-limit N] [--ted-limit N]
    .venv/bin/python -I db/daily.py health

On Modal, db/modal_daily.py runs `run` every day at 05:00 UTC with DIR on the volume ccp-raw-bytes (bytes and state
persist there). Every step is the adapters' own code; every read is a plain GET with the User-Agent below.

base  the IMPIC datasets on dados.gov.pt (anúncios, contratos, modificações): a resource is read again only when the
      portal's sha1 changed since the last run (the bytes are checked against it and kept in DIR/base/<sha256>). When
      anúncios or contratos changed: the 2026 anúncios through db/history.py load_anuncios, then every year's contratos
      through load_contratos (the procedures without a notice gather contracts of all years), years whose bytes were
      already loaded read but not written. An object that changed becomes its next revision; one that did not is skipped.
dr    the Diário da República notice PDFs of procedures published from DR_FROM on (the earlier ones are E1b's, on the
      Mac): adapters/dr-anuncios fetch (one GET every 10 s, at most --dr-limit per run, 403/429 stops it), text and
      build, run on a store laid out in DIR/dr/data from today's anúncios build; the objects go to Postgres.
ted   the TED daily packages after the last one read (from 202600190, the first after the monthly bundles of H.5): the
      Portuguese notices kept as in adapters/ted/modal_ted.py, each through adapters/ted/adapter.py; the package raw and
      the notices' bytes under DIR/ted/. Stops at the first package not yet published.
"""
import argparse
import datetime
import hashlib
import io
import json
import re
import sys
import tarfile
import traceback
import urllib.error
import urllib.request
from pathlib import Path
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from db import history, pg  # noqa: E402
from engine.canon import sha256_bytes  # noqa: E402

UA = "ccp-engine research (passive read)"
DATASETS = {"anuncios": "contratos-publicos-portal-base-impic-anuncios-de-2012-a-2026",
            "contratos": "contratos-publicos-portal-base-impic-contratos-de-2012-a-2026",
            "modificacoes": "contratos-publicos-portal-base-impic-modificacoes-contratuais-de-2012-a-2026"}
FILE = re.compile(r"(anuncios|contratos|modcontrats)(20\d\d)\.(json|zip)$")
FIRST_YEAR, DR_FROM, TED_FIRST = 2018, "2026-10-25", 202600190


def now():
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def get(url, timeout=900):
    with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": UA}, method="GET"), timeout=timeout) as r:
        return r.read()


def load_state(work):
    p = work / "state.json"
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else {}


def save_state(work, state):
    p = work / "state.json"
    p.write_text(json.dumps(state, ensure_ascii=False, indent=1, sort_keys=True) + "\n", encoding="utf-8")


def seed_state():
    """What db/history.py loaded (the extractor's dumps of 2026-10-25/26): sha256 by (kind, year)."""
    return {f"{k}{y}": d["sha256"] for (k, y), d in history.history_raws().items()}


# ---- base --------------------------------------------------------------------------------------------------------------
def portal_resources():
    out = {}
    for kind, slug in DATASETS.items():
        for r in json.loads(get(f"https://dados.gov.pt/api/1/datasets/{slug}/", 120))["resources"]:
            m = FILE.match(r["title"])
            if m and int(m.group(2)) >= FIRST_YEAR:
                k = {"modcontrats": "modificacoes"}.get(m.group(1), m.group(1))
                out[f"{k}{m.group(2)}"] = {"url": r["url"], "sha1": (r.get("checksum") or {}).get("value"), "kind": k, "year": int(m.group(2))}
    return out


def run_base(conn, work, recorded_at, state, dr_inputs):
    res = portal_resources()
    loaded = state.setdefault("base_loaded", seed_state())        # sha256 loaded, by name
    seen = state.setdefault("base_seen", {})                       # the portal's sha1 last read, by name
    cache = work / "base"
    cache.mkdir(parents=True, exist_ok=True)
    dumps, read = {}, []
    for name, r in sorted(res.items()):
        if seen.get(name, {}).get("sha1") == r["sha1"] and r["sha1"] and (cache / seen[name]["sha256"]).exists():
            dumps[name] = {"url": seen[name]["url"], "sha256": seen[name]["sha256"], "at": seen[name]["at"]}
            continue
        at, body = now(), get(r["url"])
        if r["sha1"] and hashlib.sha1(body).hexdigest() != r["sha1"]:
            raise RuntimeError(f"{name}: the bytes read do not match the portal's sha1")
        sha = sha256_bytes(body)
        (cache / sha).write_bytes(body)
        seen[name] = {"sha1": r["sha1"], "sha256": sha, "url": r["url"], "at": at}
        dumps[name] = {"url": r["url"], "sha256": sha, "at": at}
        read.append(name)
    years = sorted(r["year"] for r in res.values() if r["kind"] == "contratos")
    this = max(years)
    changed = [n for n in (f"anuncios{this}", f"contratos{this}", f"modificacoes{this}") if loaded.get(n) != dumps[n]["sha256"]]
    changed += [f"contratos{y}" for y in years if loaded.get(f"contratos{y}") != dumps[f"contratos{y}"]["sha256"] and f"contratos{y}" not in changed]
    if not changed:
        return "nothing_new", {"read": read, "latest": {n: dumps[n]["at"] for n in (f"anuncios{this}", f"contratos{this}")}}
    by_sha = lambda d, sources: (cache / d["sha256"]).read_bytes()  # noqa: E731
    rep = {"read": read, "changed": changed}
    rep["anuncios"] = history.load_anuncios(conn, {this: dumps[f"anuncios{this}"]}, by_sha, recorded_at,
                                            keep=lambda y, files: dr_inputs.update(files=files))
    loaded[f"anuncios{this}"] = dumps[f"anuncios{this}"]["sha256"]
    unchanged = [y for y in years if loaded.get(f"contratos{y}") == dumps[f"contratos{y}"]["sha256"]]
    c = history.load_contratos(conn, {y: dumps[f"contratos{y}"] for y in years}, dumps[f"modificacoes{this}"], by_sha, recorded_at, unchanged=unchanged)
    rep["contratos"] = {"refused": c["refused"], "procs_new": c["procs_new"], "procedures": c["procedures"]["load"],
                        "modificacoes": c["modificacoes"]["load"], "years": {y: v["load"] for y, v in c["years"].items()}}
    for y in years:
        loaded[f"contratos{y}"] = dumps[f"contratos{y}"]["sha256"]
    loaded[f"modificacoes{this}"] = dumps[f"modificacoes{this}"]["sha256"]
    return "ok", rep


# ---- dr ----------------------------------------------------------------------------------------------------------------
def dr_store(work, files):
    """The anúncios of procedures published from DR_FROM on, laid out as the DR adapter reads them (DIR/dr/data)."""
    data = work / "dr/data"
    keep = set()
    for path, blob in files.items():
        if path.startswith("facts/facto/base-anuncios-"):
            for line in blob.decode("utf-8").splitlines():
                o = json.loads(line)
                if o["field"] == "data_publicacao_anuncio" and o["value"] >= DR_FROM:
                    keep.add(o["unit"])
    for path, blob in files.items():
        if not (path.startswith("raw/base-anuncios/raw/base-anuncios-2") or path.startswith("facts/facto/base-anuncios-")):
            continue
        lines = [l for l in blob.decode("utf-8").splitlines()
                 if (json.loads(l).get("unit") or "proc:base:" + json.loads(l)["id"].split(":", 3)[3]) in keep]
        (data / path).parent.mkdir(parents=True, exist_ok=True)
        (data / path).write_text("".join(l + "\n" for l in lines), encoding="utf-8")
        if path.startswith("raw/"):
            for l in lines:
                r = json.loads(l)
                (data / "raw_bytes").mkdir(parents=True, exist_ok=True)
                (data / r["bytes"]).write_bytes(files[r["bytes"]])
    return len(keep)


def run_dr(conn, work, recorded_at, limit, dr_inputs):
    ad = history.adapter("dr-anuncios")
    data = work / "dr/data"
    procs = dr_store(work, dr_inputs["files"]) if dr_inputs.get("files") else None
    if not (data / "raw/base-anuncios/raw").exists():
        return "nothing_new", {"why": "no anúncios published since " + DR_FROM + " laid out yet"}
    ad.DATA, ad.PDF_DIR, ad.TEXT_DIR, ad.LOG = data, data / "raw/dr-anuncios/raw_bytes", data / "raw/dr-anuncios/text", work / "dr/fetch-log.jsonl"
    before = len(ad.read_log())
    ad.cmd_fetch(SimpleNamespace(limit=limit))
    log = ad.read_log()
    ad.cmd_text(SimpleNamespace())
    files, st = ad.build(recorded_at, "ferramenta:adapter-dr-anuncios@1")
    objects = {}
    for path, blob in files.items():
        type_ = "raw" if path.startswith("raw/") else Path(path).parent.name
        if path.startswith("raw/dr-anuncios/raw/") or type_ in ("documento", "facto", "conflito"):
            objects.setdefault(type_, []).extend(json.loads(l) for l in blob.decode("utf-8").splitlines() if l.strip())
    counts = pg.load_objects(conn, history.checked(objects))
    new = log[before:]
    refused = [e for e in new if e.get("status") in (403, 429)]
    detail = {"procedures_laid_out": procs, "fetched": sum(1 for e in new if e.get("status") == 200), "attempts": len(new),
              "refused_by_server": len(refused), "load": counts}
    return ("error" if refused else "ok" if new or any(c.get("inserted") or c.get("revised") for c in counts.values()) else "nothing_new"), detail


# ---- ted ---------------------------------------------------------------------------------------------------------------
EFORMS_PT = re.compile(rb'listName="country">\s*PRT\s*<')
TEDXML_PT = re.compile(rb'<ISO_COUNTRY\s+VALUE="PT"')


def portuguese(pkg):
    """The Portuguese notices of a daily package, as adapters/ted/modal_ted.py keeps them: [(member, bytes, format, why)]."""
    out = []
    with tarfile.open(fileobj=io.BytesIO(pkg), mode="r:gz") as tar:
        for mem in tar:
            if not (mem.isfile() and mem.name.lower().endswith(".xml")):
                continue
            data = tar.extractfile(mem).read()
            fmt = "eforms" if b"urn:oasis:names:specification:ubl" in data[:4000] or b"efac:" in data else "ted-xml"
            if fmt == "eforms" and EFORMS_PT.search(data):
                out.append((mem.name, data, fmt, "an organisation with country PRT"))
            elif fmt == "ted-xml" and TEDXML_PT.search(data):
                out.append((mem.name, data, fmt, "ISO_COUNTRY PT in the coded data"))
    return out


def run_ted(conn, work, recorded_at, state, limit):
    ted = history.adapter("ted")
    nxt = state.get("ted_next", TED_FIRST)
    store = work / "ted/raw_bytes"
    store.mkdir(parents=True, exist_ok=True)
    done, rep = [], {"packages": {}}
    for _ in range(limit):
        url = f"https://ted.europa.eu/packages/daily/{nxt}"
        at = now()
        try:
            pkg = get(url)
        except urllib.error.HTTPError as exc:
            if exc.code == 404 and nxt // 100000 < datetime.date.today().year and not done:
                nxt = (nxt // 100000 + 1) * 100000 + 1        # the year turned: issue 1 of the next year
                continue
            if exc.code == 404:
                break
            raise
        sha = sha256_bytes(pkg)
        (store / sha).write_bytes(pkg)
        month = {"package_url": url, "captured_at": at}
        objects = {"raw": [{"id": f"raw:ted:pacote-diario:{nxt}", "revision": 1, "recorded_at": recorded_at, "source": "ted", "kind": "pacote-diario",
                            "source_id": str(nxt), "sha256": sha, "bytes": f"raw_bytes/{sha}", "media_type": "application/gzip", "encoding": "binary",
                            "url": url, "captured_at": at, "request": {"method": "GET", "reads_of_page": 1}}], "unidade": [], "facto": []}
        procs = 0
        for name, data, fmt, why in portuguese(pkg):
            msha = sha256_bytes(data)
            (store / msha).write_bytes(data)
            raw, unit, facts, _, _ = ted.notice(data, {"member": name, "sha256": msha, "format": fmt, "why": why}, month, recorded_at)
            objects["raw"].append(raw)
            if unit:
                procs += 1
                objects["unidade"].append(unit)
                objects["facto"] += facts
        rep["packages"][nxt] = {"portuguese": len(objects["raw"]) - 1, "procedures": procs, "load": pg.load_objects(conn, history.checked(objects))}
        done.append(nxt)
        nxt += 1
        state["ted_next"] = nxt
    rep["next"] = nxt
    return ("ok" if done else "nothing_new"), rep


# ---- the run -------------------------------------------------------------------------------------------------------------
def record(conn, run_id, source, started, status, detail):
    conn.execute("insert into ccp.ingesta (run_id, source, started_at, finished_at, status, detail) values (%s, %s, %s, %s, %s, %s)",
                 (run_id, source, started, now(), status, json.dumps(detail, ensure_ascii=False, default=str)))


def run(work, only, dr_limit, ted_limit):
    work.mkdir(parents=True, exist_ok=True)
    state = load_state(work)
    recorded_at = now()
    run_id = recorded_at
    out, dr_inputs = {}, {}
    with pg.connect() as conn:
        conn.autocommit = True
        steps = [("base", lambda: run_base(conn, work, recorded_at, state, dr_inputs)),
                 ("dr", lambda: run_dr(conn, work, recorded_at, dr_limit, dr_inputs)),
                 ("ted", lambda: run_ted(conn, work, recorded_at, state, ted_limit))]
        for source, step in steps:
            if source not in only:
                continue
            started = now()
            try:
                status, detail = step()
            except Exception as exc:  # one source failing does not stop the others; its row says why
                status, detail = "error", {"error": repr(exc)[:500], "trace": traceback.format_exc()[-1500:]}
            save_state(work, state)
            record(conn, run_id, source, started, status, detail)
            out[source] = status
            print(source, status, json.dumps(detail, ensure_ascii=False, default=str)[:600], flush=True)
        sizes = pg.sizes(conn)
        record(conn, run_id, "store", recorded_at, "ok", {"sizes": sizes})
    return out


def health():
    with pg.connect() as conn:
        rows = conn.execute("select source, last_run, last_ok, last_status, last_detail from ccp.saude order by source").fetchall()
    for source, last_run, last_ok, status, detail in rows:
        print(f"{source:6} {status:12} last run {last_run:%Y-%m-%d %H:%M} · last ok {last_ok:%Y-%m-%d %H:%M}" if last_ok else f"{source:6} {status} (never ok)")
    return rows


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("run")
    r.add_argument("--work", required=True)
    r.add_argument("--only", default="base,dr,ted")
    r.add_argument("--dr-limit", type=int, default=300)
    r.add_argument("--ted-limit", type=int, default=10)
    sub.add_parser("health")
    a = ap.parse_args()
    if a.cmd == "run":
        res = run(Path(a.work), a.only.split(","), a.dr_limit, a.ted_limit)
        sys.exit(1 if "error" in res.values() else 0)
    health()


if __name__ == "__main__":
    main()
