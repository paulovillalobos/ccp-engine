"""The join rates (DECISIONS D56), per year, from the views of migration 20261027000300: what share of the records is linked,
by which identifier, and three unmatched examples of each kind. Reads only (plus the refresh of ccp.ted_candidato).

    .venv/bin/python -I db/joins.py [--date 2026-10-27]      -> reports/data/joins-<date>.json and .md

Procedures are BASE anúncio procedures by the year of their DR publication; contracts by the year of their publication on
BASE; TED notices by the year of their OJ S publication. A TED match counts only when it is the single candidate both ways.
"""
import argparse
import datetime
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from db import pg  # noqa: E402

YEARS = "extract(year from d.valid_at)::int"
PROCS = """select u.txt as unit, d.valid_at from ccp.facto_atual d join ccp.nome u on u.no = d.unit
           where d.field = ccp.n('data_publicacao_anuncio') and d.src = ccp.n('base-anuncios')"""
CONTRACTS = """select u.txt as unit, d.valid_at from ccp.facto_atual d join ccp.nome u on u.no = d.unit
               where d.field = ccp.n('data_publicacao_contrato') and d.src = ccp.n('base-contratos')"""
TEDS = """select u.txt as unit, d.valid_at from ccp.facto_atual d join ccp.nome u on u.no = d.unit
          where d.field = ccp.n('data_publicacao_joue') and d.src = ccp.n('ted')"""
UNIQUE = "alternativas_base = 1 and alternativas_ted = 1"

# (table, base set, name, condition on d.unit) -> per year: total, linked, three unmatched
MEASURES = [
    ("procedimentos", PROCS, "com contrato", "exists (select 1 from ccp.contrato_proc c where c.proc = d.unit)"),
    ("procedimentos", PROCS, "com anúncio DR lido", "exists (select 1 from ccp.proc_dr r where r.proc = d.unit)"),
    ("procedimentos", PROCS, "com anúncio TED (candidato único)", f"exists (select 1 from ccp.ted_candidato t where t.base_proc = d.unit and {UNIQUE})"),
    ("procedimentos", PROCS, "com anúncio TED (algum candidato)", "exists (select 1 from ccp.ted_candidato t where t.base_proc = d.unit)"),
    ("contratos", CONTRACTS, "ligados ao anúncio (nAnuncio+IdIncm)", "exists (select 1 from ccp.contrato_proc c where c.contrato = d.unit and c.metodo = 'nAnuncio+IdIncm')"),
    ("contratos", CONTRACTS, "com NIF do adjudicatário", "exists (select 1 from ccp.entidade_papel e where e.unit = d.unit and e.papel = 'adjudicatario')"),
    ("avisos TED", TEDS, "com procedimento BASE (candidato único)", f"exists (select 1 from ccp.ted_candidato t where t.ted_proc = d.unit and {UNIQUE})"),
]


def measure(conn, base, cond):
    rows = conn.execute(f"""select {YEARS} as y, count(*), count(*) filter (where {cond}),
                                   (array_agg(d.unit order by d.unit) filter (where not ({cond})))[1:3]
                            from ({base}) d group by 1 order by 1""").fetchall()
    return {y: {"total": n, "ligados": k, "pct": round(100 * k / n, 1) if n else None, "sem_ligacao": n - k, "exemplos": ex or []}
            for y, n, k, ex in rows}


def report(conn):
    conn.execute("refresh materialized view ccp.ted_candidato")
    out = {"tool": "db/joins.py", "measures": []}
    for table, base, name, cond in MEASURES:
        out["measures"].append({"conjunto": table, "medida": name, "por_ano": measure(conn, base, cond)})
        print(table, name, flush=True)
    out["ted_candidatos"] = dict(zip(("pares", "unicos"), conn.execute(f"select count(*), count(*) filter (where {UNIQUE}) from ccp.ted_candidato").fetchone()))
    out["entidades"] = dict(zip(("nifs", "adjudicantes", "adjudicatarios"), conn.execute(
        "select count(distinct nif), count(distinct nif) filter (where papel = 'adjudicante'), count(distinct nif) filter (where papel = 'adjudicatario') from ccp.entidade_papel").fetchone()))
    return out


def render_md(rep, date):
    L = [f"# Ligações entre registos ({date})", "", "Gerado por db/joins.py a partir das vistas de D56 (ccp.contrato_proc, ccp.proc_dr, "
         "ccp.entidade_papel, ccp.ted_candidato). Uma ligação exata nomeia o identificador em que assenta; uma ligação TED sem "
         "identificador comum é um candidato (mesmo NIF do adjudicante, mesmo tipo de contrato, envio ao JOUE nos 10 dias antes da "
         "publicação no DR até 2 dias depois) e só conta quando é o único candidato nos dois sentidos.", "",
         f"Entidades por NIF: {rep['entidades']['nifs']} ({rep['entidades']['adjudicantes']} adjudicantes, {rep['entidades']['adjudicatarios']} adjudicatários). "
         f"Pares candidatos BASE–TED: {rep['ted_candidatos']['pares']}, dos quais únicos: {rep['ted_candidatos']['unicos']}.", ""]
    for m in rep["measures"]:
        L += [f"## {m['conjunto']}: {m['medida']}", "", "| ano | total | ligados | % | sem ligação | três exemplos sem ligação |", "|---|---:|---:|---:|---:|---|"]
        for y, v in sorted(m["por_ano"].items()):
            L.append(f"| {y} | {v['total']} | {v['ligados']} | {v['pct']} | {v['sem_ligacao']} | {', '.join(v['exemplos'])} |")
        L.append("")
    return "\n".join(L)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--date", default=datetime.date.today().isoformat())
    a = ap.parse_args()
    with pg.connect() as conn:
        conn.autocommit = True
        rep = report(conn)
    rep["date"] = a.date
    out = ROOT / f"reports/data/joins-{a.date}.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(rep, ensure_ascii=False, indent=1, sort_keys=True) + "\n", encoding="utf-8")
    out.with_suffix(".md").write_text(render_md(rep, a.date), encoding="utf-8")
    print(render_md(rep, a.date))


if __name__ == "__main__":
    main()
