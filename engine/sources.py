"""Sources: raw bytes by hash, one passive read per page, with a re-derivable working text (layer 0; FILL-PLAN B1).

    record_raw(root, source, kind, source_id, url, data, media_type, encoding, captured_at, *, extractor=None,
               renderer=None, recorded_at=None) -> raw dict
        writes <root>/raw_bytes/<sha256 of data>; when extractor is given, runs engine.extract.EXTRACTORS[extractor]
        on data and writes the text under raw_bytes/<sha256 of text>, recording raw.text = {extractor, sha256, bytes};
        appends the raw object through engine.store.Writer (append-only; the same bytes from the same address are
        not recorded twice: the existing record is returned). request = {method GET, reads_of_page 1[, renderer]}.
    load_raw_text(store, raw_id) -> str | None   the working text (derived when present, else decoded bytes)
Nothing here fetches: fetching is the tools' job (tools/capture_*.py); this module only records what they read.
Copied from rjue-engine's sources module and versioned here.
"""
from datetime import datetime, timezone
from pathlib import Path

from engine import extract
from engine.canon import sha256_bytes, sha256_text
from engine.store import Store, Writer

VERSION = "ccp-sources-0.1"


def now_utc() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def record_raw(root, source, kind, source_id, url, data: bytes, media_type, encoding, captured_at, *, extractor=None, renderer=None, recorded_at=None) -> dict:
    root = Path(root)
    store = Store([root]).load()
    sha = sha256_bytes(data)
    for existing in store.objects["raw"]:
        if existing["sha256"] == sha and existing["url"] == url:
            return existing
    (root / "raw_bytes").mkdir(parents=True, exist_ok=True)
    bpath = root / "raw_bytes" / sha
    if not bpath.exists():
        bpath.write_bytes(data)
    text = None
    if extractor:
        derived = extract.EXTRACTORS[extractor](data)
        tsha = sha256_text(derived)
        tpath = root / "raw_bytes" / tsha
        if not tpath.exists():
            tpath.write_text(derived, encoding="utf-8")
        text = {"extractor": extractor, "sha256": tsha, "bytes": f"raw_bytes/{tsha}"}
    n = sum(1 for r in store.objects["raw"] if r["source"] == source and r["kind"] == kind and r["source_id"] == source_id)
    ident = f"raw:{source}:{kind}:{source_id}" + (f"-{n + 1}" if n else "")
    request = {"method": "GET", "reads_of_page": 1}
    if renderer:
        request["renderer"] = renderer
    obj = {"id": ident, "revision": 1, "recorded_at": recorded_at or now_utc(), "source": source, "kind": kind, "source_id": source_id,
           "sha256": sha, "bytes": f"raw_bytes/{sha}", "media_type": media_type, "encoding": encoding, "url": url, "captured_at": captured_at,
           "request": request, "text": text}
    Writer(root, store).append(obj)
    return obj


def load_raw_text(store, raw_id):
    raw = store.current(raw_id)
    return store.raw_text(raw) if raw else None
