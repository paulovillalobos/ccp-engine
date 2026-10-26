"""db/daily.py on the person's Modal account, every day at 05:00 UTC (DECISIONS D49).

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


@app.function(image=image, volumes={"/vol": volume}, secrets=[modal.Secret.from_name("ccp-db")], schedule=modal.Cron("0 5 * * *"),
              timeout=6 * 3600, cpu=2, memory=8192)
def daily(only: str = "base,dr,ted", dr_limit: int = 300, ted_limit: int = 10) -> dict:
    import sys
    sys.path.insert(0, "/root/ccp")
    from db import daily as job
    try:
        return job.run(Path("/vol/daily"), only.split(","), dr_limit, ted_limit)
    finally:
        volume.commit()


@app.local_entrypoint()
def main(only: str = "base,dr,ted", dr_limit: int = 300, ted_limit: int = 10):
    print(daily.remote(only, dr_limit, ted_limit))
