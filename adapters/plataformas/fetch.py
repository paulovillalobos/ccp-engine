"""Read the procurement platforms the BASE notices link to (the person's decision of 2026-10-25, BUILD-LOG M.4).

    /usr/bin/python3 -I adapters/plataformas/fetch.py vortal  [--limit N]    notice JSON of every 2026 procedure on Vortal
    /usr/bin/python3 -I adapters/plataformas/fetch.py acingov [--limit N]    the pieces ZIP of the October procedures on acinGov

The procedures are the proc units of adaptador:base-anuncios; each one's link is the PecasProcedimento field of its
record (the raw slice in data/raw_bytes/). Order: October 2026 first, then the other months interleaved.
vortal   per procedure two GETs of Vortal's public JSON API: GetPublicTenderInformation (the link's encrypted id ->
         the notice address PT1.NTC.*) and GetRegionConfigurationByContractNoticeUId (the notice as typed fields and its
         documents list). No document is downloaded.
acingov  per procedure one GET of the link, which serves the pieces as one ZIP. Only procedures published in 2026-10.
Rules, as for the DR notices: one GET every 10 s to each host, User-Agent «ccp-engine research (passive read)»; a 403 or
429 stops the run and is logged, and a run refuses to start until an hour after the last refusal; network errors are
logged and retried by the next run; what is stored is never fetched again; the run stops when less than 2 GB is free.
Bytes go to data/raw/<source>/raw_bytes/<sha256> (gitignored); every attempt to adapters/plataformas/<platform>-log.jsonl.
Nothing is sent but the GETs; no model reads anything.
"""
import argparse
import datetime
import hashlib
import json
import os
import re
import shutil
import socket
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
DATA = ROOT / "data"
UA = "ccp-engine research (passive read)"
PACE_S, REFUSAL_WAIT_S, MIN_FREE = 10.0, 3600, 2_000_000_000
NEW_REGIME = "2026-10"
VORTAL = "https://community.vortal.biz"
PLATFORMS = {"vortal": ("community.vortal.biz", "vortal"), "acingov": ("www.acingov.pt", "pecas")}


def now():
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def month_of(dpub):
    return f"{dpub[6:10]}-{dpub[3:5]}" if len(dpub or "") == 10 else "sem-data"


def procedures(host):
    """[(key, link, month)] of the proc units whose PecasProcedimento link is on host: October first, then months interleaved."""
    items = []
    for f in sorted((DATA / "raw/base-anuncios/raw").glob("base-anuncios-2*.jsonl")):
        for line in f.read_text(encoding="utf-8").splitlines():
            r = json.loads(line)
            if r["kind"] != "anuncio":
                continue
            rec = json.loads((DATA / r["bytes"]).read_bytes().decode("utf-8"))
            link = rec.get("PecasProcedimento") or ""
            if re.match(rf"https://{re.escape(host)}/", link):
                items.append((r["id"].split(":", 3)[3], link, month_of(rec.get("dataPublicacao"))))
    items.sort()
    first = [x for x in items if x[2] >= NEW_REGIME]
    by = defaultdict(list)
    for x in items:
        if x[2] < NEW_REGIME:
            by[x[2]].append(x)
    queues, rest = [by[m] for m in sorted(by)], []
    for i in range(max((len(q) for q in queues), default=0)):
        rest.extend(q[i] for q in queues if i < len(q))
    return first + rest


def read_log(path):
    return [json.loads(l) for l in path.read_text(encoding="utf-8").splitlines() if l.strip()] if path.exists() else []


class Pacer:
    def __init__(self):
        self.last = 0.0

    def get(self, url):
        """One GET, at least PACE_S after the previous one. Returns (status, body, content type, error)."""
        pause = PACE_S - (time.monotonic() - self.last)
        if pause > 0:
            time.sleep(pause)
        self.last = time.monotonic()
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": UA}, method="GET"), timeout=90) as resp:
                return resp.status, resp.read(), (resp.headers.get("Content-Type") or "").split(";")[0].strip().lower(), None
        except urllib.error.HTTPError as exc:
            return exc.code, b"", "", str(exc.reason)
        except (urllib.error.URLError, socket.timeout, TimeoutError, ConnectionError, OSError) as exc:
            return None, b"", "", f"network: {exc!r}"[:300]


def store(source, body):
    d = DATA / f"raw/{source}/raw_bytes"
    d.mkdir(parents=True, exist_ok=True)
    sha = hashlib.sha256(body).hexdigest()
    tmp = d / f".{sha}.part"
    tmp.write_bytes(body)
    os.replace(tmp, d / sha)
    return sha


def run(platform, limit):
    host, source = PLATFORMS[platform]
    log_path = HERE / f"{platform}-log.jsonl"
    log = read_log(log_path)
    refusals = [e for e in log if e.get("status") in (403, 429)]
    if refusals:
        last = datetime.datetime.strptime(refusals[-1]["at"], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=datetime.timezone.utc)
        wait = REFUSAL_WAIT_S - (datetime.datetime.now(datetime.timezone.utc) - last).total_seconds()
        if wait > 0:
            print(f"last refusal at {refusals[-1]['at']}; resume no sooner than {int(wait)} s from now")
            return 3
    done = {e["key"] for e in log if e.get("done")}
    if platform == "acingov":  # the pieces the probe of M.2 already stored are not fetched again
        done |= {e["key"] for e in read_log(ROOT / "adapters/pecas/probe-log.jsonl") if e.get("sha256") and "acingov" in e.get("host", "")}
    todo = [x for x in procedures(host) if x[0] not in done and (platform == "vortal" or x[2] == NEW_REGIME)]
    if limit:
        todo = todo[:limit]
    print(f"{now()} {platform}: {len(done)} done, {len(todo)} to read, one GET every {PACE_S:g} s", flush=True)
    pacer = Pacer()
    with open(log_path, "a", encoding="utf-8") as lf:
        def write(e):
            lf.write(json.dumps(e, ensure_ascii=False, sort_keys=True) + "\n")
            lf.flush()
        for i, (key, link, month) in enumerate(todo):
            if shutil.disk_usage(DATA).free < MIN_FREE:
                print("less than 2 GB free; stopping", flush=True)
                return 4
            if platform == "acingov":
                at = now()
                status, body, ctype, err = pacer.get(link)
                e = {"key": key, "url": link, "at": at, "status": status, "content_type": ctype, "bytes": len(body)}
                if err:
                    e["error"] = err
                elif status == 200 and body.startswith(b"PK"):
                    e.update(sha256=store(source, body), done=True)
                else:
                    e["error"] = "not a ZIP"
                write(e)
            else:
                token = link.rstrip("/").rsplit("/", 1)[-1]
                at = now()
                url1 = f"{VORTAL}/public/api/PublicTenderDocuments/GetPublicTenderInformation?uniqueIdentifierEncrypted={urllib.parse.quote(token, safe='')}&languageCode=pt"
                status, body, ctype, err = pacer.get(url1)
                e = {"key": key, "step": "information", "url": url1, "at": at, "status": status, "bytes": len(body)}
                ntc = None
                if status == 200 and not err:
                    try:
                        m = re.search(r"/contract-notice-view/(PT1\.NTC\.[0-9]+)", json.loads(body).get("contractNoticeUrl") or "")
                        ntc = m.group(1) if m else None
                    except (ValueError, AttributeError):
                        pass
                    e["sha256"] = store(source, body)
                    e["ntc"] = ntc
                    if not ntc:
                        e.update(error="no contract notice address", done=True)
                elif err:
                    e["error"] = err
                write(e)
                if e.get("status") in (403, 429):
                    print(f"{at} refused {e['status']} on {key}; stopped", flush=True)
                    return 2
                if ntc:
                    at = now()
                    url2 = f"{VORTAL}/public/api/ContractNoticeDetail/GetRegionConfigurationByContractNoticeUId?contractNoticeUId={ntc}&langCode=pt"
                    status, body, ctype, err = pacer.get(url2)
                    e = {"key": key, "step": "contract-notice", "ntc": ntc, "url": url2, "at": at, "status": status, "bytes": len(body)}
                    if status == 200 and not err and body[:1] in (b"{", b"["):
                        e.update(sha256=store(source, body), done=True)
                    else:
                        e["error"] = err or "not JSON"
                    write(e)
            if e.get("status") in (403, 429):
                print(f"{e['at']} refused {e['status']} on {key}; stopped", flush=True)
                return 2
            if i % 50 == 0:
                print(f"{e['at']} {platform} {i + 1}/{len(todo)} {key} {e.get('status')}", flush=True)
    print(f"{now()} {platform} finished", flush=True)
    return 0


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("platform", choices=sorted(PLATFORMS))
    ap.add_argument("--limit", type=int, default=0)
    a = ap.parse_args()
    sys.exit(run(a.platform, a.limit))
