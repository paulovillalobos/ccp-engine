"""What the BASE portal shows of each contract (DECISIONS D93), into ccp.base_contrato: the procedure page shows it next
to the verdicts. The fields are copied as BASE publishes them, empty ones left out; nothing is read into a rule.

    .venv/bin/python -I db/base_detail.py load <contratosYYYY.zip> [...]     a dump (or several) into the table
    .venv/bin/python -I db/base_detail.py dict <contratos2026.zip>           made once: db/base_detail.zdict

Each row's fields are JSON compressed with zlib against a fixed dictionary (db/base_detail.zdict, 32 KB of the most
frequent field values of 4,000 records of the 2026 dump read on 2026-11-10): about 450 bytes a contract instead of 750 without it, 1,375 as jsonb.
The dictionary never changes; a new one would be a new file and a new column value, never a rewrite of this one.

db/daily.py loads the years whose dump changed after load_contratos; db/modal_daily.py base_detail loads every year
from the dumps on the volume (the first fill).
"""
import hashlib
import io
import json
import random
import sys
import zipfile
import zlib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path[:0] = [str(ROOT), str(ROOT / "db")]

VERSION = "ccp-base-detail-0.1"
# the portal's «Detalhe» of a contract, by the dump's own names
FIELDS = ("objectoContrato", "descContrato", "tipoContrato", "tipoprocedimento", "adjudicante", "adjudicatarios", "concorrentes",
          "dataPublicacao", "dataCelebracaoContrato", "dataDecisaoAdjudicacao", "precoBaseProcedimento", "precoContratual", "cpv",
          "prazoExecucao", "localExecucao", "fundamentacao", "fundamentAjusteDireto", "regime", "ProcedimentoCentralizado",
          "numAcordoQuadro", "DescrAcordoQuadro", "TipoCriterioAdjudicacao", "CritMateriais", "ContratEcologico",
          "justifNReducEscrContrato", "linkPecasProc", "Observacoes", "nAnuncio", "dataFechoContrato", "PrecoTotalEfetivo",
          "tipoFimContrato", "idprocedimento",
          # the newer dumps (2026-11): CPV as objects, the lots, the invited, the changes, the state
          "CPV", "Lotes", "entidadesConvidadas", "NUTs", "compraConjunta", "precoEstimadoProc", "estadoContrato",
          "CausasAlteraPrazo", "CausasAlteraPreco", "IDAnuncio", "TipoMEC")
EMPTY = (None, "", [], 0, 0.0)
ZDICT_PATH = ROOT / "db/base_detail.zdict"
ZDICT_SHA256 = "d2b4c8f8e2aaf1693b174f59f6dbb0877f8d9f21e03b67cfbe2fb55b7e925e46"
_ZD = []


def zdict():
    if not _ZD:
        zd = ZDICT_PATH.read_bytes()
        if hashlib.sha256(zd).hexdigest() != ZDICT_SHA256:
            raise SystemExit("db/base_detail.zdict is not the dictionary the rows were compressed with")
        _ZD.append(zd)
    return _ZD[0]


def pack(fields):
    c = zlib.compressobj(9, zlib.DEFLATED, 15, 9, zlib.Z_DEFAULT_STRATEGY, zdict())
    return c.compress(json.dumps(fields, ensure_ascii=False, separators=(",", ":"), sort_keys=True).encode("utf-8")) + c.flush()


def unpack(blob):
    d = zlib.decompressobj(15, zdict())
    return json.loads(d.decompress(blob) + d.flush())


def make_dict(data):
    """The dictionary: the most frequent «"field":value» strings of 4,000 records drawn with seed 1, most frequent last."""
    recs = records(data)
    random.seed(1)
    count = {}
    for r in random.sample(recs, 4000):
        for k, v in detail(r).items():
            x = json.dumps({k: v}, ensure_ascii=False, separators=(",", ":"))[1:-1].encode("utf-8")
            count[x] = count.get(x, 0) + 1
    zd = b""
    for x, n in sorted(count.items(), key=lambda kv: (-kv[1], kv[0])):
        if n < 8 or len(zd) + len(x) > 32000:
            break
        zd = x + zd
    return zd


def detail(rec):
    """The record's portal fields; empty ones left out, and descContrato when it repeats objectoContrato."""
    d = {k: rec[k] for k in FIELDS if k in rec and rec[k] not in EMPTY}
    if d.get("descContrato") == d.get("objectoContrato"):
        d.pop("descContrato", None)
    return d


def records(data):
    with zipfile.ZipFile(io.BytesIO(data)) as z:
        names = [n for n in z.namelist() if n.lower().endswith(".json")]
        if len(names) != 1:
            raise SystemExit(f"{names}: not one JSON member")
        return json.loads(z.read(names[0]).decode("utf-8"))


def load(conn, data, year=None):
    """One yearly contratos dump into ccp.base_contrato: a new idcontrato inserted, a changed one replaced. The same
    idcontrato in two years keeps the earliest year (as db/history.load_contratos keeps the record once)."""
    rows = {}
    for rec in records(data):
        cid = str(rec.get("idcontrato") or "").strip()
        if not cid.isdigit():
            continue
        y = int(rec.get("Ano") or year or 0)
        if cid in rows and rows[cid][0] <= y:
            continue
        rows[cid] = (y, pack(detail(rec)))
    with conn.cursor() as cur:
        cur.execute("create temp table if not exists _bc (id bigint, ano smallint, raw text, doc bytea) on commit drop")
        with cur.copy("copy _bc (id, ano, raw, doc) from stdin") as cp:
            for cid, (y, doc) in rows.items():
                cp.write_row((int(cid), y, f"raw:base-contratos:contrato:{cid}", doc))
        cur.execute("""insert into ccp.base_contrato (id, ano, raw, doc)
                       select distinct on (id) id, ano, raw, doc from _bc order by id, ano
                       on conflict (id) do update set ano = least(ccp.base_contrato.ano, excluded.ano), raw = excluded.raw,
                         doc = excluded.doc, recorded_at = now()
                       where ccp.base_contrato.doc is distinct from excluded.doc and excluded.ano <= ccp.base_contrato.ano""")
        n = cur.rowcount
    conn.commit()
    return {"records": len(rows), "written": n}


def for_unit(conn, unit):
    """The contracts of a procedure unit, with their portal fields, newest first."""
    rows = conn.execute("""select b.id, b.raw, b.doc from ccp.contrato_proc cp
                           join ccp.base_contrato b on b.id = split_part(cp.contrato, ':', 3)::bigint
                           where cp.proc = %s and split_part(cp.contrato, ':', 3) ~ '^[0-9]+$'
                           order by b.id desc""", (unit,)).fetchall()
    return [{"id": str(i), "registo": raw, "url": f"https://www.base.gov.pt/Base4/pt/detalhe/?type=contratos&id={i}", **unpack(doc)} for i, raw, doc in rows]


def main():
    import pg
    if len(sys.argv) == 3 and sys.argv[1] == "dict":
        zd = make_dict(Path(sys.argv[2]).read_bytes())
        ZDICT_PATH.write_bytes(zd)
        print(len(zd), hashlib.sha256(zd).hexdigest())
        return
    if len(sys.argv) < 3 or sys.argv[1] != "load":
        raise SystemExit(__doc__)
    conn = pg.connect()
    for p in sys.argv[2:]:
        print(p, load(conn, Path(p).read_bytes()), flush=True)


if __name__ == "__main__":
    main()
