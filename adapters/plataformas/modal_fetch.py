"""The platform fetchers, run on the person's Modal account and writing to the volume ccp-raw-bytes (BUILD-LOG M.7).

    <modal venv>/bin/modal run --detach adapters/plataformas/modal_fetch.py --platform acingov|vortal [--limit N]

The queue is built here, on the Mac, exactly as adapters/plataformas/fetch.py builds it (procedures of
adaptador:base-anuncios by their PecasProcedimento host, October first, then months interleaved), minus the keys already
done in the local logs (adapters/plataformas/<platform>-log.jsonl). acingov reads every 2026 procedure here (the local
fetcher read October only). The remote function, on one small CPU container, skips the keys already done in its own log
on the volume and reads the rest with the same rules: one GET every 10 s to the host, User-Agent «ccp-engine research
(passive read)», a 403 or 429 stops it, network errors are logged (a later run retries them), bodies are stored under
/vol/<source>/raw_bytes/<sha256>, every attempt is appended to /vol/logs/<platform>-log.jsonl, the volume is committed
every 25 procedures. A run stops itself before Modal's 24-hour limit; running the command again continues.
Nothing is sent but the GETs; no model reads anything.
"""
import importlib.util
import json
from pathlib import Path

import modal

HERE = Path(__file__).resolve().parent
app = modal.App("ccp-platform-fetch")
volume = modal.Volume.from_name("ccp-raw-bytes")
image = modal.Image.debian_slim(python_version="3.12")
RUN_SECONDS = 23 * 3600


@app.function(image=image, volumes={"/vol": volume}, timeout=24 * 3600, cpu=0.5, memory=1024)
def fetch_run(platform: str, items: list) -> dict:
    import datetime
    import hashlib
    import os
    import re
    import socket
    import time
    import urllib.error
    import urllib.parse
    import urllib.request

    UA, PACE, VORTAL = "ccp-engine research (passive read)", 10.0, "https://community.vortal.biz"
    source = {"vortal": "vortal", "acingov": "pecas"}[platform]
    os.makedirs(f"/vol/{source}/raw_bytes", exist_ok=True)
    os.makedirs("/vol/logs", exist_ok=True)
    log_path = f"/vol/logs/{platform}-log.jsonl"
    done = set()
    if os.path.exists(log_path):
        for line in open(log_path, encoding="utf-8"):
            e = json.loads(line)
            if e.get("done"):
                done.add(e["key"])
    todo = [x for x in items if x[0] not in done]
    started, last = time.monotonic(), 0.0
    stats = {"todo": len(todo), "done_now": 0, "stopped": None}

    def now():
        return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    def get(url):
        nonlocal last
        pause = PACE - (time.monotonic() - last)
        if pause > 0:
            time.sleep(pause)
        last = time.monotonic()
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": UA}, method="GET"), timeout=120) as r:
                return r.status, r.read(), None
        except urllib.error.HTTPError as exc:
            return exc.code, b"", str(exc.reason)
        except (urllib.error.URLError, socket.timeout, TimeoutError, ConnectionError, OSError) as exc:
            return None, b"", f"network: {exc!r}"[:300]

    def store(body):
        sha = hashlib.sha256(body).hexdigest()
        p = f"/vol/{source}/raw_bytes/{sha}"
        if not os.path.exists(p):
            with open(p + ".part", "wb") as f:
                f.write(body)
            os.replace(p + ".part", p)
        return sha

    with open(log_path, "a", encoding="utf-8") as lf:
        def write(e):
            lf.write(json.dumps(e, ensure_ascii=False, sort_keys=True) + "\n")
            lf.flush()
        for i, (key, link, month) in enumerate(todo):
            if time.monotonic() - started > RUN_SECONDS:
                stats["stopped"] = "time"
                break
            refused = False
            if platform == "acingov":
                at = now()
                status, body, err = get(link)
                e = {"key": key, "url": link, "at": at, "status": status, "bytes": len(body), "where": "modal"}
                if err:
                    e["error"] = err
                elif status == 200 and body.startswith(b"PK"):
                    e.update(sha256=store(body), done=True)
                else:
                    e["error"] = "not a ZIP"
                write(e)
                refused = status in (403, 429)
            else:
                token = link.rstrip("/").rsplit("/", 1)[-1]
                at = now()
                url1 = f"{VORTAL}/public/api/PublicTenderDocuments/GetPublicTenderInformation?uniqueIdentifierEncrypted={urllib.parse.quote(token, safe='')}&languageCode=pt"
                status, body, err = get(url1)
                e = {"key": key, "step": "information", "url": url1, "at": at, "status": status, "bytes": len(body), "where": "modal"}
                ntc = None
                if status == 200 and not err:
                    try:
                        m = re.search(r"/contract-notice-view/(PT1\.NTC\.[0-9]+)", json.loads(body).get("contractNoticeUrl") or "")
                        ntc = m.group(1) if m else None
                    except (ValueError, AttributeError):
                        pass
                    e.update(sha256=store(body), ntc=ntc)
                    if not ntc:
                        e.update(error="no contract notice address", done=True)
                elif err:
                    e["error"] = err
                write(e)
                refused = status in (403, 429)
                if ntc and not refused:
                    at = now()
                    url2 = f"{VORTAL}/public/api/ContractNoticeDetail/GetRegionConfigurationByContractNoticeUId?contractNoticeUId={ntc}&langCode=pt"
                    status, body, err = get(url2)
                    e = {"key": key, "step": "contract-notice", "ntc": ntc, "url": url2, "at": at, "status": status, "bytes": len(body), "where": "modal"}
                    if status == 200 and not err and body[:1] in (b"{", b"["):
                        e.update(sha256=store(body), done=True)
                    else:
                        e["error"] = err or "not JSON"
                    write(e)
                    refused = status in (403, 429)
            if e.get("done"):
                stats["done_now"] += 1
            if refused:
                stats["stopped"] = f"refused {e['status']} at {e['at']}"
                break
            if i % 25 == 24:
                volume.commit()
    volume.commit()
    stats["left"] = len(todo) - stats["done_now"]
    return stats


@app.local_entrypoint()
def main(platform: str, limit: int = 0):
    spec = importlib.util.spec_from_file_location("plataformas_fetch", HERE / "fetch.py")
    fetch = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(fetch)
    host, _ = fetch.PLATFORMS[platform]
    done = {e["key"] for e in fetch.read_log(HERE / f"{platform}-log.jsonl") if e.get("done")}
    if platform == "acingov":
        done |= {e["key"] for e in fetch.read_log(HERE.parent / "pecas/probe-log.jsonl") if e.get("sha256") and "acingov" in e.get("host", "")}
    items = [list(x) for x in fetch.procedures(host) if x[0] not in done]
    if limit:
        items = items[:limit]
    print(f"{platform}: {len(done)} done locally, {len(items)} sent to Modal")
    print(json.dumps(fetch_run.remote(platform, items)))
