"""Check, on Modal, that every file offloaded to the volume ccp-raw-bytes hashes to its own name (the sha256).

    <modal venv>/bin/modal run adapters/plataformas/offload_check.py --prefix pecas/raw_bytes --out RESULT.json

Raw bytes are stored under their sha256, so a copy is good exactly when sha256(file) == its name. The function runs on
a CPU container with the volume mounted read-only and returns {name: sha256 of the bytes}; the local side compares and
writes RESULT.json. Nothing here reads a document's content: it only hashes bytes. (The person's decision of 2026-10-26,
BUILD-LOG M.6: offload acinGov's pieces to his Modal account to free the disk.)
"""
import json

import modal

app = modal.App("ccp-offload-check")
volume = modal.Volume.from_name("ccp-raw-bytes")


@app.function(volumes={"/vol": volume.read_only()}, timeout=3600, cpu=2)
def hash_all(prefix: str) -> dict:
    import hashlib
    import os
    out = {}
    base = os.path.join("/vol", prefix)
    for name in sorted(os.listdir(base)):
        h = hashlib.sha256()
        with open(os.path.join(base, name), "rb") as f:
            for chunk in iter(lambda: f.read(1 << 20), b""):
                h.update(chunk)
        out[name] = h.hexdigest()
    return out


@app.local_entrypoint()
def main(prefix: str, out: str):
    got = hash_all.remote(prefix)
    good = sorted(n for n, h in got.items() if n == h)
    bad = sorted(n for n, h in got.items() if n != h)
    json.dump({"prefix": prefix, "files": len(got), "good": good, "bad": bad}, open(out, "w"), indent=1)
    print(f"{len(got)} files on the volume; {len(good)} hash to their name; {len(bad)} do not")
