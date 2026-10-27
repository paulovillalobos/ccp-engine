"""Vortal's copy of the DR notice, as a second source of the notice PDF (BUILD-LOG H.4; the M.3 probe found it byte-identical).

    <modal venv>/bin/modal run --detach adapters/plataformas/modal_vortal_dr.py [--limit N]

On the person's Modal account, volume ccp-raw-bytes: for every procedure whose Vortal notice JSON is already stored
(/logs/vortal-log.jsonl, step contract-notice, done), the documents list of that JSON is read and the document named
"<IdIncm>.pdf" (IdIncm: the last part of the procedure key, the DR notice number) is downloaded once, by its public
download URL. Only procedures whose PecasProcedimento link is on Vortal (they are the only ones with a Vortal notice), and
never as a way around a refusal of the Diário da República. One GET every 20 s (the Vortal notice fetcher runs beside it),
User-Agent «ccp-engine research (passive read)», a 403 or 429 stops the run, network errors are logged and retried by a
later run. Bytes under /vol/vortal-dr/raw_bytes/<sha256>; every attempt in /logs/vortal-dr-log.jsonl. The comparison with
the DR's own PDF (same sha256 or not) is made on the Mac against adapters/dr-anuncios/fetch-log.jsonl.
Nothing is sent but the GETs; no model reads anything.
"""
import json

import modal

app = modal.App("ccp-vortal-dr-copy")
volume = modal.Volume.from_name("ccp-raw-bytes")
image = modal.Image.debian_slim(python_version="3.12")


@app.function(image=image, volumes={"/vol": volume}, timeout=24 * 3600, cpu=0.5, memory=1024)
def run(limit: int = 0) -> dict:
    import datetime
    import hashlib
    import os
    import socket
    import time
    import urllib.error
    import urllib.request

    UA, PACE = "ccp-engine research (passive read)", 20.0
    os.makedirs("/vol/vortal-dr/raw_bytes", exist_ok=True)
    log_path = "/vol/logs/vortal-dr-log.jsonl"
    done = set()
    if os.path.exists(log_path):
        done = {e["key"] for e in map(json.loads, open(log_path, encoding="utf-8")) if e.get("done")}
    notices = {}
    for line in open("/vol/logs/vortal-log.jsonl", encoding="utf-8"):
        e = json.loads(line)
        if e.get("step") == "contract-notice" and e.get("done") and e.get("sha256"):
            notices[e["key"]] = e
    todo = [k for k in sorted(notices) if k not in done]
    if limit:
        todo = todo[:limit]
    stats = {"notices": len(notices), "todo": len(todo), "found": 0, "not_listed": 0, "downloaded": 0, "stopped": None}
    last = 0.0

    def now():
        return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    with open(log_path, "a", encoding="utf-8") as lf:
        def write(e):
            lf.write(json.dumps(e, ensure_ascii=False, sort_keys=True) + "\n")
            lf.flush()
        for i, key in enumerate(todo):
            incm = key.rsplit(".", 1)[-1]
            n = notices[key]
            doc = None
            try:
                region = json.load(open(f"/vol/vortal/raw_bytes/{n['sha256']}", encoding="utf-8"))
                for f in region.get("regionConfiguration", []):
                    if f.get("name", "").startswith("EA2_") and isinstance(f.get("value"), list):
                        doc = next((d for d in f["value"] if d.get("name") == f"{incm}.pdf" and d.get("isPublic")), None)
            except (OSError, ValueError):
                pass
            if doc is None:
                stats["not_listed"] += 1
                write({"key": key, "ntc": n.get("ntc"), "at": now(), "done": True, "found": False})
                continue
            stats["found"] += 1
            pause = PACE - (time.monotonic() - last)
            if pause > 0:
                time.sleep(pause)
            last = time.monotonic()
            at = now()
            e = {"key": key, "ntc": n.get("ntc"), "at": at, "found": True, "url": doc["downloadUrl"], "listed_bytes": doc.get("size")}
            try:
                with urllib.request.urlopen(urllib.request.Request(doc["downloadUrl"], headers={"User-Agent": UA}, method="GET"), timeout=120) as r:
                    body, e["status"] = r.read(), r.status
                if body.startswith(b"%PDF"):
                    sha = hashlib.sha256(body).hexdigest()
                    p = f"/vol/vortal-dr/raw_bytes/{sha}"
                    if not os.path.exists(p):
                        with open(p + ".part", "wb") as f:
                            f.write(body)
                        os.replace(p + ".part", p)
                    e.update(sha256=sha, bytes=len(body), done=True)
                    stats["downloaded"] += 1
                else:
                    e["error"] = "not a PDF"
            except urllib.error.HTTPError as exc:
                e.update(status=exc.code, error=str(exc.reason))
            except (urllib.error.URLError, socket.timeout, TimeoutError, ConnectionError, OSError) as exc:
                e.update(status=None, error=f"network: {exc!r}"[:300])
            write(e)
            if e.get("status") in (403, 429):
                stats["stopped"] = f"refused {e['status']} at {at}"
                break
            if i % 25 == 24:
                volume.commit()
    volume.commit()
    return stats


@app.local_entrypoint()
def main(limit: int = 0):
    print(json.dumps(run.remote(limit)))
