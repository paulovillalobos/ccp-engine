"""The API over the Postgres store (DECISIONS D90): tools/serve.py's routes plus the stored verdicts, read from Supabase.

    .venv/bin/python -I db/api.py [--host 127.0.0.1] [--port 5341] [--token <secret>]

    public   GET /v1/procedimentos/<unidade>             a procedure: its facts (with their origin) and the verdicts of the
                                                          latest engine run, each with its rule, citation and manifest
             GET /v1/veredictos?resultado=&regra=&apos=&limite=   the latest run's verdicts, by unit id, a page at a time
             GET /v1/entidades/<nif>/veredictos           the latest run's verdicts on the procedures of one adjudicante
             GET /v1/estatisticas                         the latest run: when, its window, commit and counts
    and every route of tools/serve.py (lei, manifesto, regras, diff, exemplo, POST verificar, …), unchanged.

Read-only: the connection is opened read only and every query is a SELECT on ccp.veredicto_atual, ccp.facto or
ccp.corrida. A verdict the latest run does not give is not shown (verdicts are append-only: D88). A «não avaliado» is not
stored (D87): POST /v1/verificar computes it live. Nothing here writes, calls a model, or echoes a request path back.
"""
import argparse
import json
import os
import re
import sys
import threading
from http.server import ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parent.parent
sys.path[:0] = [str(ROOT / "db"), str(ROOT), str(ROOT / "tools")]
import pg  # noqa: E402
import serve  # noqa: E402

VERSION = "ccp-api-0.1"
UNIT = re.compile(r"^proc:base:[A-Za-z0-9._-]{1,80}$")
NIF = re.compile(r"^\d{9}$")
PAGE_MAX = 200
_local = threading.local()


def db():
    """One read-only connection per server thread, reopened when it breaks."""
    c = getattr(_local, "conn", None)
    if c is None or c.closed:
        c = pg.connect()
        c.autocommit = True
        c.execute("set default_transaction_read_only = on")
        c.execute("set statement_timeout = '20s'")
        _local.conn = c
    return c


def rule_info(rid):
    r = serve.STORE.current(rid)
    return {"id": rid, "titulo": r["title"], "tipo": r["type"], "estado": r["state"]} if r else {"id": rid}


def verdict_out(doc):
    c = doc.get("citation") or {}
    m = doc.get("manifest") or {}
    return {"regra": {**rule_info(doc["rule"]["id"]), "revision": doc["rule"]["revision"]}, "resultado": doc["result"], "motivo": doc.get("reason"),
            "detalhe": doc.get("detail"), "passagem": c.get("passage"), "versao": c.get("version"), "citacao": c.get("quote"),
            "factos_usados": doc.get("facts_used", []), "valido_em": doc.get("valid_at"), "conhecido_em": doc.get("known_at"),
            "manifesto": {"lei": m.get("law_version"), "pacote": m.get("package"), "commit": (m.get("code") or {}).get("commit"),
                          "motor": (m.get("code") or {}).get("engine_version"), "registo": m.get("log_head")}}


def latest_run():
    r = db().execute("select id, at, doc from ccp.corrida order by at desc limit 1").fetchone()
    return {"id": r[0], "em": r[1].strftime("%Y-%m-%dT%H:%M:%SZ"), **r[2]} if r else None


def procedimento(unit):
    if not UNIT.match(unit):
        raise serve.ApiError(400, "unidade: proc:base:<id>")
    facts = [d for (d,) in db().execute("select doc from ccp.facto where unit = %s", (unit,)).fetchall()]
    if not facts:
        raise serve.ApiError(404, "procedimento desconhecido")
    verdicts = [d for (d,) in db().execute("select doc from ccp.veredicto_atual where unit = %s", (unit,)).fetchall()]
    run = latest_run()
    return {"procedimento": unit, "corrida": run and run["id"],
            "factos": sorted(({"campo": f["field"], "valor": f.get("value"), "valido_em": f.get("valid_at"), "origem": f.get("origin"),
                               "adaptador": f.get("adapter"), "id": f["id"]} for f in facts), key=lambda x: x["campo"]),
            "veredictos": [verdict_out(d) for d in sorted(verdicts, key=lambda d: d["rule"]["id"])],
            "nota": "Só os veredictos (cumpre, não cumpre) da última corrida; um «não avaliado» calcula-se em POST /v1/verificar."}


def page(query):
    def one(k, default=None):
        return (query.get(k) or [default])[0]
    res = one("resultado")
    if res not in (None, "cumpre", "nao_cumpre"):
        raise serve.ApiError(400, "resultado: cumpre ou nao_cumpre")
    regra = one("regra")
    if regra is not None and not re.match(r"^regra:[A-Za-z0-9:@._-]{1,160}$", regra):
        raise serve.ApiError(400, "regra: um id de regra")
    after = one("apos", "")
    if after and not UNIT.match(after):
        raise serve.ApiError(400, "apos: proc:base:<id>")
    try:
        limit = max(1, min(PAGE_MAX, int(one("limite", "50"))))
    except ValueError:
        raise serve.ApiError(400, "limite: número")
    return res, regra, after, limit


def veredictos(query, nif=None):
    res, regra, after, limit = page(query)
    where, args = ["v.unit > %s"], [after]
    if res:
        where.append("v.result = %s"); args.append(res)
    if regra:
        where.append("v.rule = %s"); args.append(regra)
    if nif:  # D90: the run recorded each verdict's adjudicante
        where.append("v.adjudicante = %s"); args.append(nif)
    rows = db().execute(f"select v.unit, v.doc from ccp.veredicto_atual v where {' and '.join(where)} order by v.unit limit %s", (*args, limit)).fetchall()
    items = [{"procedimento": u, **verdict_out(d)} for u, d in rows]
    return {"corrida": (latest_run() or {}).get("id"), "veredictos": items, "seguinte": rows[-1][0] if len(rows) == limit else None}


def entidade_veredictos(nif):
    if not NIF.match(nif):
        raise serve.ApiError(400, "nif: nove algarismos")
    return {"nif": nif, **veredictos({}, nif)}


def estatisticas():
    run = latest_run()
    if run is None:
        raise serve.ApiError(404, "nenhuma corrida")
    return {"corrida": run}


class Handler(serve.Handler):
    server_version = "ccp-engine-api/" + VERSION

    def route(self, method):
        path = unquote(self.path.split("?", 1)[0])
        try:
            if method == "GET" and path.startswith("/v1/procedimentos/"):
                return self.send_json(200, procedimento(path[len("/v1/procedimentos/"):]))
            if method == "GET" and path == "/v1/veredictos":
                from urllib.parse import parse_qs, urlsplit
                return self.send_json(200, veredictos(parse_qs(urlsplit(self.path).query)))
            if method == "GET" and path.startswith("/v1/entidades/") and path.endswith("/veredictos"):
                return self.send_json(200, entidade_veredictos(path[len("/v1/entidades/"):-len("/veredictos")]))
            if method == "GET" and path == "/v1/estatisticas":
                return self.send_json(200, estatisticas())
        except serve.ApiError as exc:
            return self.send_json(exc.status, {"erro": exc.message})
        except Exception:  # never a trace to the caller
            import traceback
            traceback.print_exc(file=sys.stderr)
            return self.send_json(500, {"erro": "falha interna; o registo do servidor diz porquê"})
        return super().route(method)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--host", default="127.0.0.1"); ap.add_argument("--port", type=int, default=int(os.environ.get("PORT", 5341)))
    ap.add_argument("--token", default=os.environ.get("CCP_TOKEN"))
    a = ap.parse_args()
    serve.TOKEN = a.token
    serve.load(("law", "rules", "governance"), commit=os.environ.get("CCP_COMMIT"))
    print(f"ccp api {VERSION} on http://{a.host}:{a.port}", flush=True)
    ThreadingHTTPServer((a.host, a.port), Handler).serve_forever()


if __name__ == "__main__":
    main()
