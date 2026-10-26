"""Offload a raw file larger than Storage's 50 MB limit as byte parts with a manifest (the person's decision, BUILD-LOG H.6).

    .venv/bin/python -I adapters/storage/split_offload.py --workdir <linked supabase workdir> SOURCE SHA256 [--part-bytes N]

The person's words, relayed by the builder: «Divide contratos2025.zip en partes de menos de 50 MB con sus huellas, sin
tocar el spend cap». The file data/raw/<SOURCE>/raw_bytes/<SHA256> is cut at byte offsets (not re-zipped) into parts of
at most --part-bytes (40 000 000 by default); each goes to ccp-raw/<SOURCE>/raw_bytes/<SHA256>.partNN, and a manifest
(the whole file's sha256 and size; each part's name, order, offset, size and sha256) goes next to them as
<SHA256>.manifest.json and into git at adapters/storage/parts/<SHA256>.manifest.json. Verified by downloading every
part and the manifest back, joining the parts in order and hashing the result; only if it hashes to SHA256 is the Mac
copy deleted. Every step in adapters/storage/offload-log.jsonl. No Supabase setting is changed.
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
CLI = str(Path.home() / "bin/supabase")
BUCKET = "ccp-raw"


def now():
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def cp(workdir, src, dst):
    r = subprocess.run([CLI, "storage", "cp", src, dst, "--linked", "--experimental", "--workdir", workdir], capture_output=True, text=True)
    if r.returncode != 0:
        raise SystemExit(f"supabase storage cp {src} -> {dst}: {(r.stdout + r.stderr).strip()[-300:]}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--workdir", required=True)
    ap.add_argument("--part-bytes", type=int, default=40_000_000)
    ap.add_argument("source")
    ap.add_argument("sha256")
    a = ap.parse_args()
    if a.part_bytes >= 50_000_000:
        raise SystemExit("parts must stay under Storage's 50 MB limit")
    path = DATA / f"raw/{a.source}/raw_bytes/{a.sha256}"
    whole = path.read_bytes()
    if hashlib.sha256(whole).hexdigest() != a.sha256:
        raise SystemExit("the local file does not hash to its name")
    prefix = f"ss:///{BUCKET}/{a.source}/raw_bytes/{a.sha256}"
    parts = []
    with tempfile.TemporaryDirectory() as t:
        for n, off in enumerate(range(0, len(whole), a.part_bytes), 1):
            chunk = whole[off:off + a.part_bytes]
            name = f"{a.sha256}.part{n:02d}"
            (Path(t) / name).write_bytes(chunk)
            parts.append({"name": name, "order": n, "offset": off, "bytes": len(chunk), "sha256": hashlib.sha256(chunk).hexdigest()})
        manifest = {"sha256": a.sha256, "bytes": len(whole), "source": a.source, "bucket": BUCKET,
                    "split": "byte offsets, parts joined in order give the file", "parts": parts}
        mtext = json.dumps(manifest, ensure_ascii=False, indent=1) + "\n"
        (Path(t) / f"{a.sha256}.manifest.json").write_text(mtext, encoding="utf-8")
        for p in parts:
            cp(a.workdir, str(Path(t) / p["name"]), f"{prefix}.part{p['order']:02d}")
        cp(a.workdir, str(Path(t) / f"{a.sha256}.manifest.json"), f"{prefix}.manifest.json")
        back = Path(t) / "back"
        back.mkdir()
        joined = hashlib.sha256()
        for p in parts:
            cp(a.workdir, f"{prefix}.part{p['order']:02d}", str(back / p["name"]))
            b = (back / p["name"]).read_bytes()
            if len(b) != p["bytes"] or hashlib.sha256(b).hexdigest() != p["sha256"]:
                raise SystemExit(f"part {p['name']} came back different")
            joined.update(b)
        cp(a.workdir, f"{prefix}.manifest.json", str(back / "manifest.json"))
        ok = joined.hexdigest() == a.sha256 and (back / "manifest.json").read_text(encoding="utf-8") == mtext
    (HERE / "parts").mkdir(exist_ok=True)
    (HERE / "parts" / f"{a.sha256}.manifest.json").write_text(mtext, encoding="utf-8")
    e = {"source": a.source, "sha256": a.sha256, "bytes": len(whole), "object": f"{BUCKET}/{a.source}/raw_bytes/{a.sha256}.part01..{len(parts):02d}",
         "parts": len(parts), "at": now(), "checked_at": now(), "verified": ok, "how": "parts downloaded back, joined in order, sha256 of the whole"}
    with open(HERE / "offload-log.jsonl", "a", encoding="utf-8") as lf:
        lf.write(json.dumps(e, ensure_ascii=False, sort_keys=True) + "\n")
    if not ok:
        raise SystemExit("the joined parts do not hash to the file; the Mac copy is kept")
    path.unlink()
    print(json.dumps({"parts": [(p["name"][-6:], p["bytes"]) for p in parts], "whole": len(whole), "verified": ok}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
