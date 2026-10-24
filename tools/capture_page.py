"""Capture one document that needs no rendering (a PDF, a static page) by a single passive GET and record it.

    .venv/bin/python tools/capture_page.py --url URL --source SOURCE --kind KIND --source-id ID [--store law]

The response bytes are the raw record (engine.sources.record_raw), with the media type the server sent; no working
text is derived (PDFs have no extractor in the gate, DECISIONS D17). One GET, no retry, nothing sent (invariant 10).
Prints the record id, size, sha256 and, for a PDF, whether it carries a text layer (has_text_layer).

    has_text_layer(data) -> bool   a PDF whose content streams (inflated with zlib when FlateDecode) show text with the
                                   Tj / TJ operators; a scanned PDF (images only) has none
"""
import argparse
import re
import sys
import urllib.request
import zlib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from engine.sources import now_utc, record_raw  # noqa: E402

VERSION = "ccp-capture-page-0.1"
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
    ap.add_argument("--url", required=True); ap.add_argument("--source", required=True); ap.add_argument("--kind", required=True)
    ap.add_argument("--source-id", required=True); ap.add_argument("--store", default="law")
    a = ap.parse_args()
    captured_at = now_utc()
    req = urllib.request.Request(a.url, headers={"User-Agent": AGENT}, method="GET")
    with urllib.request.urlopen(req, timeout=60) as resp:
        data = resp.read()
        media = (resp.headers.get("Content-Type") or "application/octet-stream").split(";")[0].strip()
    pdf = data[:5] == b"%PDF-"
    obj = record_raw(ROOT / a.store, a.source, a.kind, a.source_id, a.url, data, "application/pdf" if pdf else media,
                     "binary" if pdf else "utf-8", captured_at, renderer=f"{VERSION}: one urllib GET")
    print(f"{obj['id']}: {len(data)} bytes, sha256 {obj['sha256']}, {obj['media_type']}" + (f", text layer: {has_text_layer(data)}" if pdf else ""))


if __name__ == "__main__":
    main()
