"""BASE bulk dumps from dados.gov.pt (contratos and anúncios, one file per year), read once each (BUILD-LOG H.1).

    /usr/bin/python3 -I adapters/base-historico/fetch.py --from 2018 --to 2026
    .venv/bin/python -I adapters/base-historico/fetch.py record --recorded-at T

fetch   lists the resources of the two IMPIC datasets on dados.gov.pt (their public API), keeps contratos<year>.zip and
        anuncios<year>.json for the years asked, and GETs each file once: a file whose sha256 is already stored (here
        or under data/raw_bytes/ or data/raw/base-contratos/raw_bytes/) is not read again. The portal's sha1 checksum is
        compared with the bytes read; a mismatch is logged and the file is not kept. Bytes go to
        data/raw/base-historico/raw_bytes/<sha256> (gitignored); every attempt to adapters/base-historico/fetch-log.jsonl.
        Bulk files: no 10 s pacing is needed (the person's instruction relayed by the builder, 2026-10-26).
record  one raw per stored file (source base-dump, kind contratos-ano / anuncios-ano), with its size in COVERAGE.md
        (raw.schema has no size field).
Nothing is sent but the GETs; no model reads anything.
"""
import argparse
import datetime
import hashlib
import json
import re
import sys
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
DATA = ROOT / "data"
BYTES = DATA / "raw/base-historico/raw_bytes"
LOG = HERE / "fetch-log.jsonl"
UA = "ccp-engine research (passive read)"
DATASETS = {"contratos": "contratos-publicos-portal-base-impic-contratos-de-2012-a-2026",
            "anuncios": "contratos-publicos-portal-base-impic-anuncios-de-2012-a-2026"}
FILE = re.compile(r"(contratos)(20\d\d)\.zip$|(anuncios)(20\d\d)\.json$")


def now():
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def get(url):
    with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": UA}, method="GET"), timeout=600) as r:
        return r.read()


def resources(first, last):
    out = []
    for kind, slug in DATASETS.items():
        d = json.loads(get(f"https://dados.gov.pt/api/1/datasets/{slug}/"))
        for r in d["resources"]:
            m = FILE.match(r["title"])
            if not m:
                continue
            k, year = (m.group(1), m.group(2)) if m.group(1) else (m.group(3), m.group(4))
            if k == kind and first <= int(year) <= last:
                out.append({"kind": kind, "year": int(year), "title": r["title"], "url": r["url"],
                            "sha1": (r.get("checksum") or {}).get("value"), "portal_modified": r.get("last_modified")})
    return sorted(out, key=lambda x: (x["kind"], x["year"]))


def stored_shas():
    shas = set()
    for d in (BYTES, DATA / "raw_bytes", DATA / "raw/base-contratos/raw_bytes"):
        if d.exists():
            shas |= {p.name for p in d.iterdir() if not p.name.startswith(".")}
    return shas


def cmd_fetch(a):
    BYTES.mkdir(parents=True, exist_ok=True)
    log = [json.loads(l) for l in LOG.read_text(encoding="utf-8").splitlines()] if LOG.exists() else []
    done_urls = {e["url"]: e for e in log if e.get("sha256")}
    have = stored_shas()
    with open(LOG, "a", encoding="utf-8") as lf:
        for r in resources(a.first, a.last):
            prev = done_urls.get(r["url"])
            if prev and prev["sha256"] in have:
                print("stored", r["title"]); continue
            at = now()
            body = get(r["url"])
            sha1, sha = hashlib.sha1(body).hexdigest(), hashlib.sha256(body).hexdigest()
            e = dict(r, at=at, bytes=len(body), sha256=sha, sha1_read=sha1)
            if r["sha1"] and sha1 != r["sha1"]:
                e.pop("sha256"); e["error"] = "sha1 differs from the portal's checksum; not kept"
            elif sha not in have:
                tmp = BYTES / f".{sha}.part"; tmp.write_bytes(body); tmp.replace(BYTES / sha)
            lf.write(json.dumps(e, ensure_ascii=False, sort_keys=True) + "\n"); lf.flush()
            print(at, r["title"], len(body), e.get("error") or "ok")
    return 0


def cmd_record(a):
    sys.path.insert(0, str(ROOT))
    from engine import schema
    from engine.canon import canonical
    out = {}
    for line in LOG.read_text(encoding="utf-8").splitlines():
        e = json.loads(line)
        if not e.get("sha256"):
            continue
        res = e["url"].rstrip("/").split("/")
        rid = f"raw:base-dump:{e['kind']}-ano:{res[-1]}.{res[-2]}"
        media = "application/zip" if e["title"].endswith(".zip") else "application/json"
        out[rid] = {"id": rid, "revision": 1, "recorded_at": a.recorded_at, "source": "base-dump", "kind": f"{e['kind']}-ano",
                    "source_id": f"{res[-2]}/{res[-1]}", "sha256": e["sha256"], "bytes": f"raw_bytes/{e['sha256']}", "media_type": media,
                    "encoding": "binary" if media == "application/zip" else "utf-8", "url": e["url"], "captured_at": e["at"],
                    "request": {"method": "GET", "reads_of_page": 1}}
    objs = sorted(out.values(), key=lambda o: o["id"])
    for o in objs:
        errs = schema.validate("raw", o)
        if errs:
            raise SystemExit(f"{o['id']}: {errs[0]}")
    p = DATA / "raw/base-historico/raw/base-historico.jsonl"
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text("".join(canonical(o) + "\n" for o in objs), encoding="utf-8")
    print(len(objs), "raws ->", p.relative_to(ROOT))
    return 0


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", nargs="?", default="fetch", choices=["fetch", "record"])
    ap.add_argument("--from", dest="first", type=int, default=2018)
    ap.add_argument("--to", dest="last", type=int, default=2026)
    ap.add_argument("--recorded-at")
    a = ap.parse_args()
    sys.exit({"fetch": cmd_fetch, "record": cmd_record}[a.cmd](a))
