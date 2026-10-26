"""The Postgres store (DECISIONS D48): connection, migrations, load and export. Code that talks to the network lives
here, outside engine/, tools/ and verify.py (verify's code guard keeps them free of it), as readers/ does for models.

    .venv/bin/python -I db/pg.py migrate                 apply supabase/migrations/*.sql not yet applied
    .venv/bin/python -I db/pg.py load <store root>...    insert every data object of those roots (existing (id, revision) skipped)
    .venv/bin/python -I db/pg.py roundtrip <root>...     export back and compare every object of those roots (canonical JSON)
    .venv/bin/python -I db/pg.py load-files <file>...    insert (or revise) the objects of those store files, then compare them back
    .venv/bin/python -I db/pg.py sizes                   rows and bytes per table of schema ccp
    .venv/bin/python -I db/pg.py selftest                the load rules (new, unchanged, revised) on made-up objects, rolled back

Credentials: SUPABASE_PROJECT_REF and SUPABASE_DB_PASSWORD from the environment (on Modal, the secret ccp-db) or from
.env at the repository root (gitignored); the connection goes
through Supabase's session pooler (eu-west-1), TLS required. Nothing here prints a secret.
"""
import json
import os
import re
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
    """The credentials from the environment (the Modal secret ccp-db) or else from .env."""
    env = {k: os.environ[k] for k in ("SUPABASE_PROJECT_REF", "SUPABASE_DB_PASSWORD") if k in os.environ}
    if len(env) < 2:
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


# ---- D49: the compact layout of facto, raw and unidade ----------------------------------------------------------------
COMPACT = {"facto": "facto_c", "raw": "raw_c", "unidade": "unidade_c"}
TS = re.compile(r"[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z")
DAY = re.compile(r"[0-9]{4}-[0-9]{2}-[0-9]{2}")
SHA = re.compile(r"[0-9a-f]{64}")


def encode(type_, o):
    """(row with names still as strings, names used). Every key a column cannot say exactly goes to rest, so the view
    rebuilds the object as it was; the round trip checks it."""
    rest = dict(o)
    take = lambda k, ok: rest.pop(k) if k in rest and ok(rest[k]) else None  # noqa: E731
    is_str = lambda v: isinstance(v, str)  # noqa: E731
    rev, rec = o["revision"], o["recorded_at"]
    if not (isinstance(rev, int) and 1 <= rev < 32768 and is_str(rec) and TS.fullmatch(rec)):
        raise ValueError(f"{o.get('id')}: revision or recorded_at outside the envelope")
    del rest["revision"], rest["recorded_at"]
    if type_ == "facto":
        unit, field = take("unit", is_str), take("field", is_str)
        src = o["id"].rsplit(":", 1)[-1]
        if unit is None or field is None or o["id"] != f"facto:{unit.replace(':', '-')}:{field}:{src}":
            raise ValueError(f"{o['id']}: a fact id must be facto:<unit>:<field>:<source> (D49)")
        del rest["id"]
        origin = take("origin", lambda v: isinstance(v, dict) and set(v) == {"raw", "field"} and all(map(is_str, v.values())))
        row = {"unit": unit, "field": field, "src": src, "revision": rev, "recorded_at": rec, "adapter": take("adapter", is_str),
               "value": json.dumps(rest.pop("value"), ensure_ascii=False) if "value" in rest else None,
               "valid_at": take("valid_at", lambda v: is_str(v) and DAY.fullmatch(v)), "known_at": take("known_at", lambda v: is_str(v) and TS.fullmatch(v)),
               "oraw": origin and origin["raw"], "ofield": origin and origin["field"]}
        names = ("unit", "field", "src", "adapter", "oraw", "ofield")
    elif type_ == "raw":
        del rest["id"]
        sha = take("sha256", lambda v: is_str(v) and SHA.fullmatch(v) and o.get("bytes") == f"raw_bytes/{v}")
        if sha:
            del rest["bytes"]
        req = take("request", lambda v: isinstance(v, dict))
        row = {"id": o["id"], "revision": rev, "recorded_at": rec, "source": take("source", is_str), "kind": take("kind", is_str),
               "source_id": take("source_id", is_str), "sha256": sha and bytes.fromhex(sha), "media_type": take("media_type", is_str),
               "encoding": take("encoding", is_str), "url": take("url", is_str), "captured_at": take("captured_at", lambda v: is_str(v) and TS.fullmatch(v)),
               "request": req and canonical(req)}
        names = ("id", "source", "kind", "media_type", "encoding", "url", "request")
    else:
        del rest["id"]
        raw = take("raw", lambda v: isinstance(v, list) and all(map(is_str, v)))
        row = {"id": o["id"], "revision": rev, "recorded_at": rec, "kind": take("kind", is_str), "parent": take("parent", is_str), "raw": raw}
        names = ("id", "kind", "parent")
    row["rest"] = json.dumps(rest, ensure_ascii=False) if rest else None
    used = {row[k] for k in names if row[k] is not None} | set(row.get("raw") or [] if type_ == "unidade" else [])
    return row, names, used


def name_numbers(conn, txts, cache):
    """The ccp.nome number of each string, adding the new ones."""
    todo = sorted(t for t in txts if t not in cache)
    for i in range(0, len(todo), 50000):
        chunk = todo[i:i + 50000]
        conn.execute("insert into ccp.nome (txt) select unnest(%s::text[]) on conflict (txt) do nothing", (chunk,))
        cache.update(conn.execute("select txt, no from ccp.nome where txt = any(%s)", (chunk,)).fetchall())
    return cache


# what makes two revisions of an object differ: not when or from which download it was read (recorded_at, known_at,
# url, captured_at), only what it says
SAME = {"facto": ["adapter", "value", "valid_at", "oraw", "ofield"], "raw": ["source", "kind", "source_id", "sha256", "media_type", "encoding", "request"],
        "unidade": ["kind", "parent", "raw"]}
KEY = {"facto": ["unit", "field", "src"], "raw": ["id"], "unidade": ["id"]}


def load_compact(conn, type_, objs, cache):
    """New objects are inserted as they are; an object already stored is skipped when it says the same as its latest
    revision, and otherwise stored as the next revision, superseding it (the store keeps every revision)."""
    table, key = COMPACT[type_], KEY[type_]
    rows, used = [], set()
    for o in objs:
        row, names, u = encode(type_, o)
        rows.append((row, names)); used |= u
    name_numbers(conn, used, cache)
    cols = list(rows[0][0]) if rows else []
    on = " and ".join(f"t.{k} = l.{k}" for k in key)
    same = " and ".join([f"t.{c} is not distinct from l.{c}" for c in SAME[type_]] +
                        ["coalesce(t.rest - 'supersedes', '{}') = coalesce(l.rest - 'supersedes', '{}')"])
    with conn.transaction():
        conn.execute(f"drop table if exists load_{table}")   # inside an outer transaction (selftest) on commit has not come yet
        conn.execute(f"create temp table load_{table} (like ccp.{table}) on commit drop")
        with conn.cursor().copy(f"copy load_{table} ({', '.join(cols)}) from stdin") as cp:
            for row, names in rows:
                out = dict(row)
                for k in names:
                    if out[k] is not None:
                        out[k] = cache[out[k]]
                if type_ == "unidade" and out["raw"] is not None:
                    out["raw"] = "{" + ",".join(str(cache[r]) for r in out["raw"]) + "}"
                cp.write_row([out[c] for c in cols])
        inserted = conn.execute(f"insert into ccp.{table} select l.* from load_{table} l where not exists (select 1 from ccp.{table} t where {on})").rowcount
        others = [c for c in cols if c not in ("revision", "rest")]
        revised = conn.execute(f"""insert into ccp.{table} ({', '.join(others)}, revision, rest)
            select {', '.join('l.' + c for c in others)},
                   case when l.revision > t.revision then l.revision else t.revision + 1 end,
                   case when l.revision > t.revision then l.rest else coalesce(l.rest, '{{}}') || jsonb_build_object('supersedes', t.revision) end
            from load_{table} l cross join lateral (select * from ccp.{table} t where {on} order by t.revision desc limit 1) t
            where l.revision > t.revision or (l.revision <= t.revision and not ({same}))""").rowcount   # a later revision as it comes
    return {"in_store": len(objs), "inserted": inserted, "revised": revised, "unchanged": len(objs) - inserted - revised}


def load_objects(conn, objects, cache=None):
    """objects: {type: [store object]}. The big three go to the compact tables (D49), the rest as in D48."""
    cache = {} if cache is None else cache
    counts = {}
    for type_, objs in objects.items():
        if not objs:
            continue
        if type_ in COMPACT:
            counts[type_] = load_compact(conn, type_, objs, cache)
            continue
        cols = list(columns(type_, objs[0]))
        names = ["id", "revision", "recorded_at", *cols, "doc"]
        with conn.transaction():
            conn.execute(f"drop table if exists load_{type_}")
            conn.execute(f"create temp table load_{type_} (like ccp.{type_} including defaults) on commit drop")
            with conn.cursor().copy(f"copy load_{type_} ({', '.join(names)}) from stdin") as cp:
                for o in objs:
                    c = columns(type_, o)
                    cp.write_row([o["id"], o["revision"], o.get("recorded_at") or o.get("at"), *[c[k] for k in cols], json.dumps(o, ensure_ascii=False)])
            inserted = conn.execute(f"insert into ccp.{type_} select * from load_{type_} on conflict (id, revision) do nothing").rowcount
            # D48 tables keep the object's own revision: a different object under a stored (id, revision) is reported, not stored
            differ = conn.execute(f"""select count(*) from load_{type_} l join ccp.{type_} t using (id, revision)
                                      where (t.doc - 'recorded_at') <> (l.doc - 'recorded_at')""").fetchone()[0]
        counts[type_] = {"in_store": len(objs), "inserted": inserted, "unchanged": len(objs) - inserted - differ, "differ_not_stored": differ}
    return counts


def objects_from_files(paths):
    """{type: [object]} from store files: <root>/raw/<source>/raw/*.jsonl are raws, <root>/facts/<type>/* are that type."""
    out = {}
    for path in map(Path, paths):
        type_ = "raw" if path.parent.name == "raw" and path.parent.parent.parent.name == "raw" else path.parent.name
        if type_ not in TABLES:
            raise SystemExit(f"{path}: not a store file of a known type")
        text = path.read_text(encoding="utf-8")
        objs = [json.loads(l) for l in text.splitlines() if l.strip()] if path.suffix == ".jsonl" else [json.loads(text)]
        out.setdefault(type_, []).extend(objs)
    return out


def load(conn, roots):
    by_type = {}
    for type_, o in store_objects(roots):
        by_type.setdefault(type_, []).append(o)
    return load_objects(conn, by_type)




def roundtrip_objects(conn, objects, view=""):
    """Every object, read back from Postgres, is the same object (canonical JSON). objects: {type: [store object]}."""
    missing = differ = n = 0
    for t, objs in objects.items():
        want = {(o["id"], o["revision"]): canonical(o) for o in objs}
        n += len(want)
        key = "unit" if t == "facto" else "id"   # the facto view derives id; its unit goes through an index
        keys = sorted({o[key] for o in objs})
        got = {}
        for i in range(0, len(keys), 20000):
            got.update({(r[0], r[1]): canonical(r[2]) for r in conn.execute(f"select id, revision, doc from ccp.{t}{view} where {key} = any(%s)", (keys[i:i + 20000],))})
        for k, c in want.items():
            if k not in got:
                missing += 1
            elif got[k] != c:
                differ += 1
    return {"objects": n, "missing": missing, "differ": differ}


def roundtrip(conn, roots):
    by_type = {}
    for type_, o in store_objects(roots):
        by_type.setdefault(type_, []).append(o)
    return roundtrip_objects(conn, by_type)


def sizes(conn):
    """Rows and bytes per table of schema ccp (tables only; the views hold nothing)."""
    out = {}
    for (name,) in conn.execute("select c.relname from pg_class c join pg_namespace n on n.oid = c.relnamespace where n.nspname = 'ccp' and c.relkind = 'r' order by 1").fetchall():
        rows, size = conn.execute(f"select (select count(*) from ccp.{name}), pg_total_relation_size('ccp.{name}')").fetchone()
        out[name] = {"rows": rows, "bytes": size}
    out["_database_bytes"] = conn.execute("select pg_database_size(current_database())").fetchone()[0]
    return out


def move_d48(conn):
    """Once (D49): the D48 rows of facto, raw and unidade into the compact tables, then every object compared."""
    report = {}
    for t in COMPACT:
        objs = [r[0] for r in conn.execute(f"select doc from ccp.{t}")]
        report[t] = {"load": load_compact(conn, t, objs, {}), "roundtrip": roundtrip_objects(conn, {t: objs}, view="_v")}
    return report


def selftest(conn):
    """The load rules on made-up objects, inside a transaction that is rolled back: nothing stays in the store."""
    out = []
    try:
        with conn.transaction():
            unit, raw = "proc:selftest:1", "raw:selftest:x:1"
            f = {"id": f"facto:{unit.replace(':', '-')}:preco_base:selftest", "revision": 1, "recorded_at": "2026-01-01T00:00:00Z", "unit": unit,
                 "field": "preco_base", "value": 100, "origin": {"raw": raw, "field": "PrecoBase"}, "adapter": "adaptador:selftest@1",
                 "valid_at": "2026-01-01", "known_at": "2026-01-01T00:00:00Z"}
            r = {"id": raw, "revision": 1, "recorded_at": "2026-01-01T00:00:00Z", "source": "selftest", "kind": "x", "source_id": "1",
                 "sha256": "0" * 64, "bytes": "raw_bytes/" + "0" * 64, "media_type": "application/json", "encoding": "utf-8",
                 "url": "https://example.org/a", "captured_at": "2026-01-01T00:00:00Z", "request": {"method": "GET", "reads_of_page": 1}}
            u = {"id": unit, "revision": 1, "recorded_at": "2026-01-01T00:00:00Z", "kind": "proc", "parent": None, "raw": [raw], "consumer_ids": {}}
            later = {"recorded_at": "2026-02-01T00:00:00Z"}
            steps = [("new", {"facto": [f], "raw": [r], "unidade": [u]}, "inserted"),
                     ("read again, nothing changed", {"facto": [dict(f, **later, known_at="2026-02-01T00:00:00Z")],
                                                      "raw": [dict(r, **later, url="https://example.org/b", captured_at="2026-02-01T00:00:00Z")],
                                                      "unidade": [dict(u, **later)]}, "unchanged"),
                     ("read again, changed", {"facto": [dict(f, **later, value=120)], "raw": [dict(r, **later, sha256="1" * 64, bytes="raw_bytes/" + "1" * 64)],
                                              "unidade": [dict(u, **later, consumer_ids={"base_id": "1"})]}, "revised")]
            for name, objs, expect in steps:
                counts = load_objects(conn, objs)
                out.append((name, all(c[expect] == 1 for c in counts.values()), {t: c[expect] for t, c in counts.items()}))
            docs = {t: [row[0] for row in conn.execute(f"select doc from ccp.{t} where id = %s order by revision", (i,))]
                    for t, i in (("facto", f["id"]), ("raw", raw), ("unidade", unit))}
            out.append(("revision 2 supersedes 1, revision 1 kept", all(len(d) == 2 and d[1]["revision"] == 2 and d[1]["supersedes"] == 1
                                                                        and d[0] == canonical_obj(d[0]) for d in docs.values()), {t: len(d) for t, d in docs.items()}))
            out.append(("round trip of revision 1", roundtrip_objects(conn, {"facto": [f], "raw": [r], "unidade": [u]})["differ"] == 0, None))
            raise psycopg.Rollback()
    except psycopg.Rollback:
        pass
    return out


def canonical_obj(o):
    return json.loads(canonical(o))


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
        elif cmd == "load-files":
            objs = objects_from_files(roots)
            print(json.dumps({"load": load_objects(conn, objs), "roundtrip": roundtrip_objects(conn, objs)}, indent=1))
        elif cmd == "move-d48":
            print(json.dumps(move_d48(conn), indent=1))
        elif cmd == "selftest":
            conn.autocommit = False
            res = selftest(conn)
            for name, ok, detail in res:
                print("ok  " if ok else "FAIL", name, detail or "")
            raise SystemExit(0 if all(ok for _, ok, _ in res) else 1)
        elif cmd == "sizes":
            print(json.dumps(sizes(conn), indent=1))
        else:
            raise SystemExit(f"unknown command {cmd}")


if __name__ == "__main__":
    main()
