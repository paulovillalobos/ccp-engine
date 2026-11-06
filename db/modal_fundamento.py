"""The legal basis each entity declared (BASE contratos' `fundamentacao`) as a fact of its procedure (DECISIONS D88).

    <modal venv>/bin/modal run db/modal_fundamento.py [--years 2018,…,2026] [--dry-run]

One container per year reads that year's contratos dataset from the volume ccp-raw-bytes (daily/base/<sha256>, the
files db/daily.py keeps), parses each contract's fundamentação with db/fundamento.passages, and writes one fact per
procedure: fundamento_passagens, the sorted union of the passages its contracts declare, with the first contract's raw
as origin (adaptador:base-fundamento@1). The procedure is the contract unit's parent in ccp.unidade_atual. Inserts are
committed and counted in the database afterwards. No model; no network but the database.
"""
import json
import sys
from pathlib import Path

import modal

ROOT = Path(__file__).resolve().parent.parent
app = modal.App("ccp-fundamento")
vol = modal.Volume.from_name("ccp-raw-bytes")
image = modal.Image.debian_slim(python_version="3.12").pip_install("psycopg[binary]==3.2.4", "jsonschema==4.25.1")
for d in ("engine", "db", "schemas"):
    image = image.add_local_dir(ROOT / d, f"/root/ccp/{d}", ignore=["**/__pycache__", "**/*.pyc", "**/.env*"])
ADAPTER = "adaptador:base-fundamento@1"
SOURCE = "base-fundamento"


def adapter_object(at):
    return {"id": ADAPTER, "revision": 1, "recorded_at": at, "source": SOURCE, "version": 1, "code": "adapters/base-contratos/",
            "mapping": [{"source_field": "fundamentacao", "canonical_field": "fundamento_passagens", "transform": "identity",
                         "note": "D88: the passages the entity declared as its legal basis, read by db/fundamento.py; the union over the procedure's contracts"}],
            "coverage": [], "proposed_by": "ferramenta:modal-fundamento@1", "state": "proposed"}


@app.function(image=image, volumes={"/vol": vol}, secrets=[modal.Secret.from_name("ccp-db")], cpu=2, memory=8192, timeout=3600,
              max_containers=1)  # one year at a time: parallel loads deadlock on ccp.nome
def year(name: str, sha: str, dry: bool = False) -> dict:
    import io, zipfile, datetime
    sys.path[:0] = ["/root/ccp/db", "/root/ccp"]
    import pg
    import fundamento
    data = (Path("/vol/daily/base") / sha).read_bytes()
    blobs = [data]
    if data[:2] == b"PK":
        with zipfile.ZipFile(io.BytesIO(data)) as z:
            blobs = [z.read(n) for n in z.namelist()]
    recs = {}
    for b in blobs:
        try:
            for r in json.loads(b.decode("utf-8-sig")):
                i = str(r.get("idcontrato") or "")
                if i and r.get("fundamentacao"):
                    recs[i] = r
        except Exception:
            continue
    conn = pg.connect()
    conn.execute("set statement_timeout = '900s'")
    parent = {}
    ids = [f"contrato:base:{i}" for i in recs]
    for k in range(0, len(ids), 20000):
        q = """select n.txt, p.txt from ccp.unidade_atual u join ccp.nome n on n.no = u.id join ccp.nome p on p.no = u.parent
               where u.id = any(select no from ccp.nome where txt = any(%s))"""
        parent.update(dict(conn.execute(q, (ids[k:k + 20000],)).fetchall()))
    at = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    by_proc = {}
    for i, r in recs.items():
        proc = parent.get(f"contrato:base:{i}")
        if not proc:
            continue
        x = by_proc.setdefault(proc, {"p": set(), "raw": f"raw:base-contratos:contrato:{i}", "date": None})
        x["p"] |= set(fundamento.passages(r["fundamentacao"]))
        d = str(r.get("dataCelebracaoContrato") or "")[:10]
        if len(d) == 10 and d[4] == "-" and (x["date"] is None or d < x["date"]):
            x["date"] = d
    facts = [{"id": f"facto:{proc.replace(':', '-')}:fundamento_passagens:{SOURCE}", "revision": 1, "recorded_at": at, "unit": proc,
              "field": "fundamento_passagens", "value": sorted(x["p"]), "origin": {"raw": x["raw"], "field": "fundamentacao"},
              "adapter": ADAPTER, "valid_at": x["date"] or at[:10], "known_at": at} for proc, x in by_proc.items() if x["p"]]
    out = {"year": name, "records": len(recs), "procedures": len(facts)}
    if not dry and facts:
        out["load"] = pg.load_objects(conn, {"facto": facts})
        conn.commit()
    return out


@app.local_entrypoint()
def main(state: str, dry_run: bool = False):
    sys.path[:0] = [str(ROOT / "db"), str(ROOT)]
    s = json.loads(Path(state).read_text())
    years = sorted((k, v["sha256"]) for k, v in s["base_seen"].items() if k.startswith("contratos"))
    if not dry_run:
        import pg
        conn = pg.connect()
        import datetime
        print(pg.load_objects(conn, {"adaptador": [adapter_object(datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"))]}))
        conn.commit()
    for r in year.starmap([(k, v, dry_run) for k, v in years]):
        print(json.dumps(r, ensure_ascii=False))
