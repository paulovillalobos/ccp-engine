"""Record every file the platform fetchers stored as a raw object (no facts yet).

    .venv/bin/python -I adapters/plataformas/record.py --recorded-at T

Reads adapters/plataformas/vortal-log.jsonl and acingov-log.jsonl; for every logged GET whose body was stored (sha256)
and is still in data/raw/<source>/raw_bytes/ or was offloaded and checked (offload-check-*.json), one raw: raw:vortal:tender-information:<key>,
raw:vortal:contract-notice:<key> (the notice of that procedure), raw:pecas:documento:<key> (acinGov's pieces ZIP). The
key is the procedure's key in adaptador:base-anuncios. captured_at is the GET's time; request is one passive GET.
Writes data/raw/vortal/raw/vortal-fetch.jsonl and data/raw/pecas/raw/pecas-acingov.jsonl, sorted: same log, same bytes.
"""
import argparse
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
DATA = ROOT / "data"
sys.path.insert(0, str(ROOT))
from engine import schema  # noqa: E402
from engine.canon import canonical  # noqa: E402

KINDS = {("vortal", "information"): ("vortal", "tender-information", "application/json", "utf-8"),
         ("vortal", "contract-notice"): ("vortal", "contract-notice", "application/json", "utf-8"),
         ("acingov", None): ("pecas", "documento", "application/zip", "binary")}


# files moved to the person's Modal volume ccp-raw-bytes after offload_check.py found sha256(file) == name (BUILD-LOG M.6)
OFFLOADED = {n for f in sorted(HERE.glob("offload-check-*.json")) for n in json.loads(f.read_text(encoding="utf-8"))["good"]}


def raws(platform, recorded_at):
    out = {}
    path = HERE / f"{platform}-log.jsonl"
    for line in path.read_text(encoding="utf-8").splitlines() if path.exists() else []:
        e = json.loads(line)
        if not e.get("sha256") or e.get("status") != 200:
            continue
        source, kind, media, enc = KINDS[(platform, e.get("step"))]
        if not (DATA / f"raw/{source}/raw_bytes/{e['sha256']}").exists() and e["sha256"] not in OFFLOADED:
            continue
        rid = f"raw:{source}:{kind}:{e['key']}"
        out[rid] = {"id": rid, "revision": 1, "recorded_at": recorded_at, "source": source, "kind": kind,
                    "source_id": e.get("ntc") or e["key"], "sha256": e["sha256"], "bytes": f"raw_bytes/{e['sha256']}",
                    "media_type": media, "encoding": enc, "url": e["url"], "captured_at": e["at"], "request": {"method": "GET", "reads_of_page": 1}}
    return sorted(out.values(), key=lambda o: o["id"])


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--recorded-at", required=True); a = ap.parse_args()
    for platform, rel in (("vortal", "raw/vortal/raw/vortal-fetch.jsonl"), ("acingov", "raw/pecas/raw/pecas-acingov.jsonl")):
        objs = raws(platform, a.recorded_at)
        for o in objs:
            errs = schema.validate("raw", o)
            if errs:
                raise SystemExit(f"{o['id']}: {errs[0]}")
        p = DATA / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text("".join(canonical(o) + "\n" for o in objs), encoding="utf-8")
        print(platform, len(objs), "raws ->", rel)


if __name__ == "__main__":
    main()
