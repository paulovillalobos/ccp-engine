"""Capture one Diário da República page by a single passive read and record it with its working text.

    .venv/bin/python tools/capture_dr_consolidated.py --url URL --source dr-consolidado --kind lei --source-id ccp \
        [--store law] [--extractor dr-consolidated-fragments@1 | dr-html-blocks@1] [--budget-ms 30000]

The page is rendered once with headless Chrome (--dump-dom, the virtual-time budget given); the DOM bytes are the raw
record, the extractor's output is the working text (engine/sources.record_raw). Nothing is retried; nothing is sent
(GET only, invariant 10). Prints: lines of text, first and last "Artigo" line, how many lines look like validity notes.
Copied from rjue-engine's capture tool and versioned here.
"""
import argparse
import os
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from engine import extract  # noqa: E402
from engine.sources import now_utc, record_raw  # noqa: E402

VERSION = "ccp-capture-dr-0.2"
CHROME = os.environ.get("CCP_CHROME", "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome")  # D92: Chromium in the cloud
CONTAINER = ["--no-sandbox", "--disable-dev-shm-usage"] if "CCP_CHROME" in os.environ else []  # a container runs as root, /dev/shm small


def render(url, budget_ms) -> bytes:
    with tempfile.TemporaryDirectory() as profile:
        res = subprocess.run([CHROME, "--headless=new", "--disable-gpu", *CONTAINER, f"--user-data-dir={profile}", f"--virtual-time-budget={budget_ms}", "--dump-dom", url],
                             capture_output=True, text=True, timeout=max(300, budget_ms // 1000 * 6))
    if res.returncode != 0 or not res.stdout:
        raise SystemExit(f"render failed: {res.returncode} {res.stderr[-300:]}")
    return res.stdout.encode("utf-8")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--url", required=True); ap.add_argument("--source", required=True); ap.add_argument("--kind", required=True)
    ap.add_argument("--source-id", required=True); ap.add_argument("--store", default="law")
    ap.add_argument("--extractor", default="dr-consolidated-fragments@1", choices=sorted(extract.EXTRACTORS)); ap.add_argument("--budget-ms", type=int, default=30000)
    a = ap.parse_args()
    captured_at = now_utc()
    data = render(a.url, a.budget_ms)
    text = extract.EXTRACTORS[a.extractor](data)
    obj = record_raw(ROOT / a.store, a.source, a.kind, a.source_id, a.url, data, "text/html", "utf-8", captured_at,
                     extractor=a.extractor, renderer=f"headless Chrome --dump-dom virtual-time-budget {a.budget_ms}")
    lines = text.splitlines()
    arts = [l for l in lines if l.startswith("Artigo ")]
    notes = [l for l in lines if "em vigor" in l.lower() or l.lower().startswith(("alterado", "aditado", "revogado", "redação", "redacção"))]
    print(f"{obj['id']}: {len(data)} bytes, sha256 {obj['sha256'][:12]}; text {len(text)} chars, {len(lines)} lines, {len(arts)} 'Artigo' lines"
          f" (first {arts[0] if arts else None!r}, last {arts[-1] if arts else None!r}), {len(notes)} note-like lines")


if __name__ == "__main__":
    main()
