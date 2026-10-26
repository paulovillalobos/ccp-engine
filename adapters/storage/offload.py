"""Move raw bytes from the Mac to the person's Supabase Storage bucket ccp-raw (project ccp-engine), checked by sha256.

    .venv/bin/python -I adapters/storage/offload.py --workdir <linked supabase workdir> SOURCE [SOURCE ...]

SOURCE is a directory name under data/raw/ (its bytes in data/raw/<SOURCE>/raw_bytes/<sha256>). For each file: upload
to ss:///ccp-raw/<SOURCE>/raw_bytes/<sha256> with the Supabase CLI (linked to ccp-engine in --workdir, so no key is
handled here), download it back to a temporary file, and compare the sha256 with the file's name; only on a match is the
Mac copy deleted. Every step goes to adapters/storage/offload-log.jsonl (source, sha256, size, times, result). A file
already verified in the log is not uploaded again. The decision: the person created the private bucket (2026-10-26) and
the builder relayed «upload, download back and compare, only then delete the Mac copy».
"""
import argparse
import datetime
import hashlib
import json
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
DATA = ROOT / "data"
LOG = HERE / "offload-log.jsonl"
CLI = str(Path.home() / "bin/supabase")
BUCKET = "ccp-raw"


def now():
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def cli(workdir, *args):
    r = subprocess.run([CLI, "storage", *args, "--linked", "--experimental", "--workdir", workdir], capture_output=True, text=True)
    return r.returncode, (r.stdout + r.stderr).strip()[-400:]


def sha256_file(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--workdir", required=True)
    ap.add_argument("--min-bytes", type=int, default=0, help="only files at least this big (the dumps first, the record slices later)")
    ap.add_argument("--workers", type=int, default=1, help="parallel uploads (each one CLI process)")
    ap.add_argument("--require-text", action="store_true", help="dr-anuncios: only PDFs whose pypdf text is already extracted")
    ap.add_argument("sources", nargs="+")
    a = ap.parse_args()
    verified = set()
    if LOG.exists():
        verified = {(e["source"], e["sha256"]) for e in map(json.loads, LOG.read_text(encoding="utf-8").splitlines()) if e.get("verified")}
    totals = {"verified": 0, "bytes": 0, "failed": 0}
    jobs = []
    for source in a.sources:
        d = DATA / f"raw/{source}/raw_bytes"
        for p in sorted(x for x in d.iterdir() if not x.name.startswith(".")) if d.exists() else []:
            if p.stat().st_size < a.min_bytes:
                continue
            if a.require_text and not (DATA / f"raw/{source}/text/{p.name}.json").exists():
                continue
            if (source, p.name) in verified:
                p.unlink(); continue
            jobs.append((source, p))

    def one(job):
        source, p = job
        sha, size = p.name, p.stat().st_size
        e = {"source": source, "sha256": sha, "bytes": size, "object": f"{BUCKET}/{source}/raw_bytes/{sha}", "at": now()}
        if sha256_file(p) != sha:
            e.update(verified=False, error="local file does not hash to its name; not uploaded")
        else:
            code, out = cli(a.workdir, "cp", str(p), f"ss:///{BUCKET}/{source}/raw_bytes/{sha}")
            if code != 0 and "KeyAlreadyExists" in out:  # an earlier, interrupted run put it there: check it like a fresh upload
                code, e["already_there"] = 0, True
            if code != 0:
                e.update(verified=False, error=f"upload: {out}")
            else:
                with tempfile.TemporaryDirectory() as t:
                    back = Path(t) / sha
                    code, out = cli(a.workdir, "cp", f"ss:///{BUCKET}/{source}/raw_bytes/{sha}", str(back))
                    ok = code == 0 and back.exists() and sha256_file(back) == sha
                e.update(verified=ok, checked_at=now())
                if ok:
                    p.unlink()
                else:
                    e["error"] = f"download back: {out}" if code else "downloaded copy does not hash to the name"
        return e

    from concurrent.futures import ThreadPoolExecutor
    with open(LOG, "a", encoding="utf-8") as lf, ThreadPoolExecutor(max_workers=max(1, a.workers)) as pool:
        for e in pool.map(one, jobs):
            lf.write(json.dumps(e, ensure_ascii=False, sort_keys=True) + "\n"); lf.flush()
            totals["verified" if e.get("verified") else "failed"] += 1
            totals["bytes"] += e["bytes"] if e.get("verified") else 0
            if not e.get("verified") or totals["verified"] % 200 == 0:
                print(e["source"], e["sha256"][:12], e["bytes"], "ok" if e.get("verified") else e.get("error"), totals, flush=True)
    print(json.dumps(totals))
    return 0 if not totals["failed"] else 1


if __name__ == "__main__":
    sys.exit(main())
