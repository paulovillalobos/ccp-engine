"""The Postgres store (DECISIONS D48): connection, migrations, load and export. Code that talks to the network lives
here, outside engine/, tools/ and verify.py (verify's code guard keeps them free of it), as readers/ does for models.

    .venv/bin/python -I db/pg.py migrate                 apply supabase/migrations/*.sql not yet applied
    .venv/bin/python -I db/pg.py load <store root>...    insert every data object of those roots (existing (id, revision) skipped)
    .venv/bin/python -I db/pg.py roundtrip <root>...     load, export back and compare every object (canonical JSON)

Credentials: .env at the repository root (gitignored), SUPABASE_PROJECT_REF and SUPABASE_DB_PASSWORD; the connection goes
through Supabase's session pooler (eu-west-1), TLS required. Nothing here prints a secret.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
import psycopg  # noqa: E402
from engine.canon import canonical  # noqa: E402
from engine.store import Store  # noqa: E402

MIGRATIONS = ROOT / "supabase/migrations"
POOLER = "aws-0-eu-west-1.pooler.supabase.com"


def columns(type_, o):
    """The query columns of a store object, by type (the whole object goes to doc)."""
    origin = o.get("origin") or {}
    return {
        "raw": lambda: {"source": o.get("source"), "sha256": o.get("sha256"), "url": o.get("url"), "fetched_at": o.get("fetched_at")},
        "adaptador": lambda: {"source": o.get("source"), "version": o.get("version"), "state": o.get("state")},
        "unidade": lambda: {"kind": o["kind"], "parent": o.get("parent")},
        "facto": lambda: {"unit": o["unit"], "field": o["field"], "value": json.dumps(o.get("value"), ensure_ascii=False), "valid_at": o.get("valid_at"),
                  "known_at": o["known_at"], "adapter": o.get("adapter"), "raw": origin.get("raw")},
        "entidade": lambda: {"nif": o.get("nif"), "name": o.get("name"), "country": o.get("country"), "type": o.get("type")},
        "alias": lambda: {"link": o.get("link"), "raw": o.get("raw"), "name_as_appears": o.get("name_as_appears")},
        "link": lambda: {"from_id": o["from"], "to_id": o["to"], "method": o.get("method"), "state": o.get("state")},
        "documento": lambda: {},
        "conflito": lambda: {"unit": o.get("unit"), "field": o.get("field")},
        "afirmacao": lambda: {"unit": o.get("unit")},
        "veredicto": lambda: {"unit": o["unit"], "rule": o["rule"]["id"] if isinstance(o.get("rule"), dict) else o.get("rule"), "result": o["result"],
                      "valid_at": o.get("valid_at"), "known_at": o.get("known_at")},
        "regra": lambda: {"type": o.get("type"), "state": o.get("state"), "valid_from": o.get("valid_from"), "valid_to": o.get("valid_to")},
    }[type_]()


TABLES = ["raw", "adaptador", "unidade", "facto", "entidade", "alias", "link", "documento", "conflito", "afirmacao", "veredicto", "regra"]


def connect():
    env = dict(l.split("=", 1) for l in (ROOT / ".env").read_text(encoding="utf-8").splitlines() if "=" in l and not l.startswith("#"))
    ref, pw = env["SUPABASE_PROJECT_REF"].strip(), env["SUPABASE_DB_PASSWORD"].strip()
    return psycopg.connect(host=POOLER, port=5432, user=f"postgres.{ref}", password=pw, dbname="postgres", sslmode="require", connect_timeout=15)


def migrate(conn):
    """Apply each migration once, in order, recording it as the Supabase CLI does (supabase_migrations.schema_migrations)."""
    conn.execute("create schema if not exists supabase_migrations")
    conn.execute("create table if not exists supabase_migrations.schema_migrations (version text primary key, statements text[], name text)")
    done = {r[0] for r in conn.execute("select version from supabase_migrations.schema_migrations")}
    for f in sorted(MIGRATIONS.glob("*.sql")):
        version, name = f.stem.split("_", 1)
        if version in done:
            continue
        sql = f.read_text(encoding="utf-8")
        with conn.transaction():
            conn.execute(sql)
            conn.execute("insert into supabase_migrations.schema_migrations (version, statements, name) values (%s, %s, %s)", (version, [sql], name))
        print("applied", f.name)


def store_objects(roots):
    st = Store([Path(r) for r in roots]).load()
    for type_ in TABLES:
        for o in st.objects.get(type_, []):
            yield type_, o


def load(conn, roots):
    counts = {}
    rows_by_type = {}
    for type_, o in store_objects(roots):
        rows_by_type.setdefault(type_, []).append(o)
    for type_, objs in rows_by_type.items():
        cols = list(columns(type_, objs[0]))
        names = ["id", "revision", "recorded_at", *cols, "doc"]
        before = conn.execute(f"select count(*) from ccp.{type_}").fetchone()[0]
        with conn.transaction():
            conn.execute(f"create temp table load_{type_} (like ccp.{type_} including defaults) on commit drop")
            with conn.cursor().copy(f"copy load_{type_} ({', '.join(names)}) from stdin") as cp:
                for o in objs:
                    c = columns(type_, o)
                    cp.write_row([o["id"], o["revision"], o.get("recorded_at") or o.get("at"), *[c[k] for k in cols], json.dumps(o, ensure_ascii=False)])
            conn.execute(f"insert into ccp.{type_} select * from load_{type_} on conflict (id, revision) do nothing")
        after = conn.execute(f"select count(*) from ccp.{type_}").fetchone()[0]
        counts[type_] = {"in_store": len(objs), "inserted": after - before, "in_table": after}
    return counts


def roundtrip(conn, roots):
    """Every object of the roots, exported back from Postgres, is the same object (canonical JSON)."""
    src = {(t, o["id"], o["revision"]): canonical(o) for t, o in store_objects(roots)}
    missing = differ = 0
    for t in {k[0] for k in src}:
        got = {(r[0], r[1]): canonical(r[2]) for r in conn.execute(f"select id, revision, doc from ccp.{t}")}
        for (tt, i, rev), c in src.items():
            if tt != t:
                continue
            if (i, rev) not in got:
                missing += 1
            elif got[(i, rev)] != c:
                differ += 1
    return {"objects": len(src), "missing": missing, "differ": differ}


def main():
    cmd, roots = sys.argv[1], sys.argv[2:]
    with connect() as conn:
        conn.autocommit = True
        if cmd == "migrate":
            migrate(conn)
        elif cmd == "load":
            print(json.dumps(load(conn, roots), indent=1))
        elif cmd == "roundtrip":
            print(json.dumps(roundtrip(conn, roots), indent=1))
        else:
            raise SystemExit(f"unknown command {cmd}")


if __name__ == "__main__":
    main()
