"""Capture one document that needs no rendering (a PDF, a static page) by a single passive GET and record it.

    .venv/bin/python tools/capture_page.py --url URL --source SOURCE --kind KIND --source-id ID [--store law]
                                           [--accept TYPE] [--accept-language LANG]
    .venv/bin/python tools/capture_page.py --list FILE --source SOURCE --kind KIND [--accept …] [--accept-language …]

The response bytes are the raw record (engine.sources.record_raw), with the media type the server sent; no working
text is derived (PDFs have no extractor in the gate, DECISIONS D17). One GET, no retry, nothing sent (invariant 10).
--accept and --accept-language ask a server that negotiates content (the Publications Office's resource/celex/
addresses, D70) for one format and one language: request headers, not data. --list FILE takes one «URL<tab>ID» per
line: the store is loaded once, each document is still one GET, one second apart, and a failed GET is printed and
skipped (nothing recorded for it).
Prints the record id, size, sha256 and, for a PDF, whether it carries a text layer (has_text_layer).

    has_text_layer(data) -> bool   a PDF whose content streams (inflated with zlib when FlateDecode) show text with the
                                   Tj / TJ operators; a scanned PDF (images only) has none
"""
import argparse
import re
import sys
import time
import urllib.request
import zlib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from engine.sources import now_utc, record_raw  # noqa: E402
from engine.store import Store  # noqa: E402

VERSION = "ccp-capture-page-0.3"
AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0 Safari/537.36"


def has_text_layer(data: bytes) -> bool:
    for m in re.finditer(rb"stream\r?\n(.*?)\r?\nendstream", data, re.S):
        body = m.group(1)
        try:
            body = zlib.decompress(body)
        except zlib.error:
            pass
        if re.search(rb"\)\s*Tj|\]\s*TJ|>\s*Tj", body):
            return True
    return False


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--url"); ap.add_argument("--source", required=True); ap.add_argument("--kind", required=True)
    ap.add_argument("--source-id"); ap.add_argument("--store", default="law"); ap.add_argument("--list")
    ap.add_argument("--accept"); ap.add_argument("--accept-language")
    a = ap.parse_args()
    if bool(a.list) == bool(a.url and a.source_id):
        ap.error("give --url and --source-id, or --list")
    headers = {"User-Agent": AGENT, **({"Accept": a.accept} if a.accept else {}), **({"Accept-Language": a.accept_language} if a.accept_language else {})}
    jobs = [tuple(l.split("\t")[:2]) for l in Path(a.list).read_text(encoding="utf-8").split("\n") if l.strip()] if a.list else [(a.url, a.source_id)]
    store = Store([ROOT / a.store]).load()
    for k, (url, source_id) in enumerate(jobs):
        if k:
            time.sleep(1)
        captured_at = now_utc()
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=headers, method="GET"), timeout=60) as resp:
                data = resp.read()
                media = (resp.headers.get("Content-Type") or "application/octet-stream").split(";")[0].strip()
        except OSError as exc:
            if not a.list:
                raise
            print(f"{source_id}: not recorded ({exc})")
            continue
        pdf = data[:5] == b"%PDF-"
        obj = record_raw(ROOT / a.store, a.source, a.kind, source_id, url, data, "application/pdf" if pdf else media,
                         "binary" if pdf else "utf-8", captured_at, renderer=f"{VERSION}: one urllib GET", store=store)
        print(f"{obj['id']}: {len(data)} bytes, sha256 {obj['sha256']}, {obj['media_type']}" + (f", text layer: {has_text_layer(data)}" if pdf else ""), flush=True)


if __name__ == "__main__":
    main()
