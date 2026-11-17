"""db/daily.py on the person's Modal account, every day at 05:00 UTC (DECISIONS D55); then the law watch and the
engine's run of the day (D92: db/modal_engine.py after_load).

    <modal venv>/bin/modal deploy db/modal_daily.py          the schedule
    <modal venv>/bin/modal run db/modal_daily.py             one run now (same function)

The container gets the repository's code (engine, adapters, db, schemas: no data, no .env), the volume ccp-raw-bytes at
/vol (the run's bytes and state under /vol/daily) and the secret ccp-db (SUPABASE_PROJECT_REF, SUPABASE_DB_PASSWORD).
The volume is committed after the run, also when a source failed (its row in ccp.ingesta says why).
"""
from pathlib import Path

import modal

ROOT = Path(__file__).resolve().parent.parent
app = modal.App("ccp-daily")
volume = modal.Volume.from_name("ccp-raw-bytes")
image = modal.Image.debian_slim(python_version="3.12").pip_install("psycopg[binary]==3.2.4", "pypdf==6.14.2", "jsonschema==4.25.1")
for d in ("engine", "adapters", "db", "schemas"):
    image = image.add_local_dir(ROOT / d, f"/root/ccp/{d}", ignore=["**/__pycache__", "**/*.pyc", "**/.env*"])


@app.function(image=image, volumes={"/vol": volume}, secrets=[modal.Secret.from_name("ccp-db"), modal.Secret.from_name("ccp-ntfy")], schedule=modal.Cron("0 5 * * *"),
              timeout=6 * 3600, cpu=2, memory=8192)
def daily(only: str = "base,dr,ted", dr_limit: int = 300, ted_limit: int = 10) -> dict:
    import sys
    sys.path.insert(0, "/root/ccp")
    from db import daily as job
    try:
        result = job.run(Path("/vol/daily"), only.split(","), dr_limit, ted_limit)
    finally:
        volume.commit()
    # D92: then the law watch and the day's engine run (db/modal_engine.py after_load, deployed as ccp-engine-run)
    call = modal.Function.from_name("ccp-engine-run", "after_load").spawn()
    # A source that failed fails the run (after the other sources and the engine run went ahead), so Modal shows it red:
    # from 2026-11-04 to 11-16 the BASE step failed every day inside a run Modal showed as succeeded.
    failed = sorted(s for s, st in result.items() if st == "error")
    if failed:
        from db import law_watch
        law_watch.alert("ccp daily: " + ", ".join(failed) + " failed", "The daily BASE/DR/TED load failed for: " + ", ".join(failed)
                        + ". New procedures from that source are not coming in. ccp.ingesta has the trace.", priority="high", tags=("warning",))
        raise RuntimeError(f"ccp daily: {', '.join(failed)} failed (ccp.ingesta has the trace); after_load {call.object_id} still ran")
    return {"ingesta": result, "after_load": call.object_id}


@app.function(image=image, volumes={"/vol": volume}, secrets=[modal.Secret.from_name("ccp-db")], timeout=3 * 3600, cpu=2, memory=8192)
def base_detail() -> dict:
    """D93, the first fill of ccp.base_contrato: every year's contratos dump on the volume (the last one read)."""
    import json
    import sys
    sys.path.insert(0, "/root/ccp")
    from db import base_detail as bd, pg
    seen = json.loads(Path("/vol/daily/state.json").read_text(encoding="utf-8"))["base_seen"]
    conn = pg.connect()
    out = {}
    for name in sorted((n for n in seen if n.startswith("contratos")), reverse=True):  # newest first: a record kept once, its earliest year
        out[name] = bd.load(conn, (Path("/vol/daily/base") / seen[name]["sha256"]).read_bytes(), int(name[-4:]))
        print(name, out[name], flush=True)
    return out


@app.local_entrypoint()
def main(only: str = "base,dr,ted", dr_limit: int = 300, ted_limit: int = 10):
    print(daily.remote(only, dr_limit, ted_limit))
