"""Record one downloaded TED daily package as a raw object (probe of the person's decision, BUILD-LOG M.0).

    python -I adapters/ted/record.py PACKAGE URL CAPTURED_AT RECORDED_AT
Stores the bytes under data/raw/ted/raw_bytes/<sha256> (gitignored) and writes data/raw/ted/raw/ted-<issue>.jsonl.
No facts: the probe only counts (adapters/ted/count.py). Nothing is sent; no model reads anything.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT))
from engine import schema  # noqa: E402
from engine.canon import canonical, sha256_bytes  # noqa: E402

pkg, url, at, rec_at = sys.argv[1:5]
data = Path(pkg).read_bytes()
sha = sha256_bytes(data)
issue = url.rstrip("/").split("/")[-1]
obj = {"id": f"raw:ted:pacote-diario:{issue}", "revision": 1, "recorded_at": rec_at, "source": "ted", "kind": "pacote-diario", "source_id": issue,
       "sha256": sha, "bytes": f"raw_bytes/{sha}", "media_type": "application/gzip", "encoding": "binary", "url": url, "captured_at": at,
       "request": {"method": "GET", "reads_of_page": 1}}
errs = schema.validate("raw", obj)
if errs:
    raise SystemExit(errs[0])
(ROOT / "data/raw/ted/raw_bytes").mkdir(parents=True, exist_ok=True)
(ROOT / f"data/raw/ted/raw_bytes/{sha}").write_bytes(data)
(ROOT / "data/raw/ted/raw").mkdir(parents=True, exist_ok=True)
(ROOT / f"data/raw/ted/raw/ted-{issue}.jsonl").write_text(canonical(obj) + "\n", encoding="utf-8")
print(obj["id"], sha)
