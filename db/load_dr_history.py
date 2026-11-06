"""The DR notices already downloaded and read to text (E1b, the extractor's data folder) → their facts in Postgres
(DECISIONS D84): data_envio_anuncio and publicado_joue for the procedures whose notice says them, which the
deadline rules need and BASE does not hold.

    .venv/bin/python -I db/load_dr_history.py --data DIR --log FILE [--dry-run]

DIR is a data folder laid out as adapters/dr-anuncios reads it (raw/base-anuncios, raw/dr-anuncios/text, the BASE
facts); FILE its fetch log. Nothing in DIR is written: the adapter's build runs in memory, as db/daily.py runs it, and its
raw, documento, facto and conflito objects are loaded (an object already stored under its (id, revision) is skipped,
a changed one becomes its next revision). No network but the database; no model.
"""
import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT)); sys.path.insert(0, str(ROOT / "db"))
import history  # noqa: E402
import pg  # noqa: E402
from engine.sources import now_utc  # noqa: E402

VERSION = "ccp-load-dr-history-0.1"


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--data", required=True); ap.add_argument("--log", required=True)
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    ad = history.adapter("dr-anuncios")
    data = Path(a.data)
    ad.DATA, ad.PDF_DIR, ad.TEXT_DIR, ad.LOG = data, data / "raw/dr-anuncios/raw_bytes", data / "raw/dr-anuncios/text", Path(a.log)
    files, st = ad.build(now_utc(), "ferramenta:adapter-dr-anuncios@1")
    objects = {}
    for path, blob in files.items():
        type_ = "raw" if path.startswith("raw/") else Path(path).parent.name
        if path.startswith("raw/dr-anuncios/raw/") or type_ in ("documento", "facto", "conflito"):
            objects.setdefault(type_, []).extend(json.loads(l) for l in blob.decode("utf-8").splitlines() if l.strip())
    fields = {}
    for o in objects.get("facto", []):
        fields[o["field"]] = fields.get(o["field"], 0) + 1
    print(json.dumps({"tool": VERSION, "objects": {k: len(v) for k, v in objects.items()}, "facts_by_field": fields}, ensure_ascii=False, indent=1), flush=True)
    if a.dry_run:
        return
    print(json.dumps(pg.load_objects(pg.connect(), history.checked(objects)), ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
