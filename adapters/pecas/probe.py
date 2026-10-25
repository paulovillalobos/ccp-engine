"""Probe of procedure documents (peças) for 10 October procedures (person's decision, BUILD-LOG M.0).

    python -I adapters/pecas/probe.py --at-most 10
For each chosen procedure of adaptador:base-anuncios (published in 2026-10; the first five by key of acinGov and of
Vortal), one GET of its PecasProcedimento link, one every 10 s, User-Agent «ccp-engine research (passive read)»; a 403
or 429 stops it. Every attempt goes to adapters/pecas/probe-log.jsonl (status, content type, size, what came back).
A response that is a document (PDF, ZIP, DOCX) is stored under data/raw/pecas/raw_bytes/<sha256> (gitignored) with a
raw object in data/raw/pecas/raw/. No facts. Nothing is sent but the GET; no model reads anything.
"""
import argparse
import datetime
import hashlib
import json
import re
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
HERE = Path(__file__).resolve().parent
UA = "ccp-engine research (passive read)"
DOC_TYPES = {"application/pdf": "pdf", "application/zip": "zip", "application/x-zip-compressed": "zip",
             "application/vnd.openxmlformats-officedocument.wordprocessingml.document": "docx", "application/octet-stream": "binary"}


def now():
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def chosen(n):
    rows = []
    for line in (ROOT / "data/raw/base-anuncios/raw/base-anuncios-2026-10.jsonl").read_text(encoding="utf-8").splitlines():
        r = json.loads(line)
        rec = json.loads((ROOT / "data" / r["bytes"]).read_bytes())
        link = rec.get("PecasProcedimento") or ""
        host = re.sub(r"^https?://([^/]+).*$", r"\1", link)
        rows.append((host, r["id"].split(":", 3)[3], link))
    pick = []
    for host in ("www.acingov.pt", "community.vortal.biz"):
        pick += sorted(x for x in rows if x[0] == host)[: n // 2]
    return pick


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--at-most", type=int, default=10); a = ap.parse_args()
    log = HERE / "probe-log.jsonl"
    rawdir, bdir = ROOT / "data/raw/pecas/raw", ROOT / "data/raw/pecas/raw_bytes"
    rawdir.mkdir(parents=True, exist_ok=True); bdir.mkdir(parents=True, exist_ok=True)
    raws, last = [], 0.0
    for host, key, url in chosen(a.at_most):
        time.sleep(max(0.0, 10.0 - (time.monotonic() - last))); last = time.monotonic()
        e = {"key": key, "host": host, "url": url, "at": now()}
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": UA}, method="GET"), timeout=60) as resp:
                body = resp.read()
                ctype = (resp.headers.get("Content-Type") or "").split(";")[0].strip().lower()
                e.update(status=resp.status, content_type=ctype, bytes=len(body), final_url=resp.geturl(),
                         disposition=resp.headers.get("Content-Disposition"))
        except urllib.error.HTTPError as exc:
            e.update(status=exc.code, error=str(exc.reason))
            body, ctype = b"", ""
        except Exception as exc:  # network: logged, not retried here
            e.update(status=None, error=repr(exc)[:300])
            body, ctype = b"", ""
        kind = DOC_TYPES.get(ctype) or ("pdf" if body.startswith(b"%PDF") else "zip" if body.startswith(b"PK") else None)
        e["document"] = kind
        if kind and e.get("status") == 200:
            sha = hashlib.sha256(body).hexdigest()
            (bdir / sha).write_bytes(body)
            e["sha256"] = sha
            raws.append({"id": f"raw:pecas:documento:{key}", "revision": 1, "recorded_at": e["at"], "source": "pecas", "kind": "documento",
                         "source_id": key, "sha256": sha, "bytes": f"raw_bytes/{sha}", "media_type": ctype or "application/octet-stream",
                         "encoding": "binary", "url": url, "captured_at": e["at"], "request": {"method": "GET", "reads_of_page": 1}})
        elif ctype.startswith("text/html"):
            title = re.search(rb"<title[^>]*>(.*?)</title>", body, re.S | re.I)
            e["html_title"] = title.group(1).decode("utf-8", "replace").strip()[:120] if title else None
            e["login_or_js"] = bool(re.search(rb"(?i)login|iniciar sess|autentica|javascript is required|enable javascript", body))
        with open(log, "a", encoding="utf-8") as f:
            f.write(json.dumps(e, ensure_ascii=False, sort_keys=True) + "\n")
        print(e["at"], host, key, e.get("status"), ctype, e.get("bytes"), e.get("document") or e.get("html_title"))
        if e.get("status") in (403, 429):
            print("refused; stopped"); break
    if raws:
        (rawdir / "pecas-probe.jsonl").write_text("".join(json.dumps(r, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n" for r in raws), encoding="utf-8")


if __name__ == "__main__":
    main()
