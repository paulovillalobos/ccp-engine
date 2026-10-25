"""Record files read from Vortal's public API (probe of the person's decision, BUILD-LOG M.0) as raw objects.

    python -I adapters/vortal/record.py FETCHED_TXT DIR RECORDED_AT
FETCHED_TXT has one line per GET: "<captured_at> <status> <url>"; DIR holds the bodies, named in the order below.
Bytes go to data/raw/<source>/raw_bytes/<sha256> (gitignored); raws to data/raw/<source>/raw/<source>-probe.jsonl.
No facts. Nothing is sent but the GETs; no model reads anything.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT))
from engine import schema  # noqa: E402
from engine.canon import canonical, sha256_bytes  # noqa: E402

FILES = [("info.json", "vortal", "tender-information", "application/json", "utf-8", "PT1.NTC.3811157-info"),
         ("header.json", "vortal", "contract-notice-header", "application/json", "utf-8", "PT1.NTC.3811157-header"),
         ("region.json", "vortal", "contract-notice", "application/json", "utf-8", "PT1.NTC.3811157"),
         ("doc.bin", "pecas", "documento", "application/pdf", "binary", "vortal-PT1.NTC.3811157-419974431.pdf")]
fetched, d, rec_at = sys.argv[1], Path(sys.argv[2]), sys.argv[3]
lines = [l.split(" ", 2) for l in Path(fetched).read_text().splitlines() if l.strip()]
ok = [l for l in lines if l[1] == "200"][-4:]
out = {}
for (name, source, kind, media, enc, sid), (at, status, url) in zip(FILES, ok):
    data = (d / name).read_bytes()
    sha = sha256_bytes(data)
    obj = {"id": f"raw:{source}:{kind}:{sid}", "revision": 1, "recorded_at": rec_at, "source": source, "kind": kind, "source_id": sid, "sha256": sha,
           "bytes": f"raw_bytes/{sha}", "media_type": media, "encoding": enc, "url": url, "captured_at": at, "request": {"method": "GET", "reads_of_page": 1}}
    errs = schema.validate("raw", obj)
    if errs:
        raise SystemExit(errs[0])
    (ROOT / f"data/raw/{source}/raw_bytes").mkdir(parents=True, exist_ok=True)
    (ROOT / f"data/raw/{source}/raw_bytes/{sha}").write_bytes(data)
    out.setdefault(source, []).append(obj)
    print(obj["id"], at, sha[:12])
for source, objs in out.items():
    (ROOT / f"data/raw/{source}/raw").mkdir(parents=True, exist_ok=True)
    name = "vortal-probe.jsonl" if source == "vortal" else "pecas-vortal-probe.jsonl"
    (ROOT / f"data/raw/{source}/raw/{name}").write_text("".join(canonical(o) + "\n" for o in objs), encoding="utf-8")
