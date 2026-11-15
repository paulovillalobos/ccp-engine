"""The API over the Postgres store (DECISIONS D90): tools/serve.py's routes plus the stored verdicts, read from Supabase.

    .venv/bin/python -I db/api.py [--host 127.0.0.1] [--port 5341] [--token <secret>]

    public   GET /v1/procedimentos/<unidade>             a procedure: its facts (with their origin) and the verdicts of the
                                                          latest engine run, each with its rule, citation and manifest
             GET /v1/veredictos?resultado=&regra=&apos=&limite=   the latest run's verdicts, by unit id, a page at a time
             GET /v1/entidades/<nif>/veredictos           the latest run's verdicts on the procedures of one adjudicante
             GET /v1/estatisticas                         the latest run: when, its window, commit and counts
             GET /v1/procedimentos/<unidade>/relatorio    D91: input, rule, steps and a re-run of the engine now
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
import time
from http.server import ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, unquote, urlsplit

ROOT = Path(__file__).resolve().parent.parent
sys.path[:0] = [str(ROOT / "db"), str(ROOT), str(ROOT / "tools")]
import base_detail  # noqa: E402
import pg  # noqa: E402
import serve  # noqa: E402

VERSION = "ccp-api-0.3"
UNIT = re.compile(r"^proc:base:[A-Za-z0-9._-]{1,80}$")
NIF = re.compile(r"^\d{9}$")
PAGE_MAX = 200
# The daily run changes these reads once a day: the CDN may serve them for 10 minutes and a stale copy while it refetches.
CACHE = "public, max-age=60, s-maxage=600, stale-while-revalidate=86400"


class _Shared:
    """One read-only connection for the whole server, reopened when it breaks. ThreadingHTTPServer starts a thread per
    request, so a connection per thread was a new TLS connection to Supabase on every request (about 2 s)."""
    lock = threading.Lock()
    conn = None

    def execute(self, *args):
        with self.lock:
            for attempt in (0, 1):
                c = self.conn
                if c is None or c.closed:
                    c = pg.connect()
                    c.autocommit = True
                    c.execute("set default_transaction_read_only = on")
                    c.execute("set statement_timeout = '20s'")
                    _Shared.conn = c
                try:
                    return _Rows(c.execute(*args).fetchall())
                except pg.psycopg.OperationalError:
                    _Shared.conn = None
                    if attempt:
                        raise

    def rollback(self):  # autocommit: a failed statement leaves no transaction to roll back
        pass


class _Rows:
    def __init__(self, rows):
        self.rows = rows

    def fetchall(self):
        return self.rows

    def fetchone(self):
        return self.rows[0] if self.rows else None


_SHARED = _Shared()


def db():
    return _SHARED


def rule_info(rid):
    r = serve.STORE.current(rid)
    return {"id": rid, "titulo": r["title"], "tipo": r["type"], "estado": r["state"]} if r else {"id": rid}


def verdict_out(doc):
    c = doc.get("citation") or {}
    m = doc.get("manifest") or {}
    return {"regra": {**rule_info(doc["rule"]["id"]), "revision": doc["rule"]["revision"]}, "resultado": doc["result"], "motivo": doc.get("reason"),
            "detalhe": doc.get("detail"), "passagem": c.get("passage"), "versao": c.get("version"), "citacao": c.get("quote"),
            "factos_usados": doc.get("facts_used", []), "valido_em": doc.get("valid_at"), "conhecido_em": doc.get("known_at"),
            **({"agregado": doc["aggregate"]} if doc.get("aggregate") else {}),  # D96: the contracts summed, each with its BASE id
            **({"prova_documental": doc["prova_documental"]} if doc.get("prova_documental") else {}),  # D97: the procedure's own document
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
            "contratos": base_detail.for_unit(db(), unit),  # D93: what BASE publishes of each contract, as published
            "nota": "Só os veredictos (cumpre, não cumpre) da última corrida; um «não avaliado» calcula-se em POST /v1/verificar."}


_RE = {}


def _engine():
    """db/run_engine.py's rules and settled window, loaded once: the report re-runs the engine on one procedure."""
    if not _RE:
        import run_engine
        from engine.governance import Log
        _RE.update(mod=run_engine, rules=run_engine.load_rules(run_engine.pending_passages(db())), window=run_engine.settled_window(Log(ROOT / "governance")))
    return _RE


def _rule_doc(rid, revision):
    return next((r for r in serve.STORE.objects["regra"] if r["id"] == rid and r["revision"] == revision), None) or serve.STORE.current(rid)


def _source(path):
    """The engine function the report names, as it is in the code serving this report."""
    import inspect
    import engine.rules as rules_mod
    return inspect.getsource(getattr(rules_mod, path))


def _steps(rule, values, result, detail, aggregate=None):
    """The calculation as steps, decided by the engine's own functions on the facts the verdict read (rules.holds,
    rules.basis_allows, the limiar comparison of engine/evaluate.py)."""
    import engine.rules as rules_mod
    steps = []
    for c in rule.get("conditions", []):
        h = rules_mod.holds(c, values)
        steps.append({"teste": f"{c['field']} {c['op']} {json.dumps(c.get('value'), ensure_ascii=False)}", "valor": values.get(c["field"]),
                      "ok": h, "efeito": "a regra aplica-se" if h else "a regra não se aplica"})
    p = rule.get("params", {})
    if rule["type"] == "limiar" and "threshold" in p:
        declared = values.get("fundamento_passagens") if isinstance(values.get("fundamento_passagens"), list) else None
        steps.append({"teste": "fundamento declarado compatível com " + ", ".join(x["passage"] for x in rule.get("passages", [])),
                      "valor": declared, "ok": rules_mod.basis_allows(rule, declared), "efeito": "este limite conta"})
        t = p["threshold"]
        steps.append({"teste": f"{t['field']} {t['comparator']} {t['value']:g}", "valor": values.get(t["field"]), "ok": result == "cumpre",
                      "efeito": "cumpre" if result == "cumpre" else "não cumpre", "decide": True})
    elif rule["type"] == "agregada" and aggregate:  # D96: each contract that counts, then the sum against the limit
        declared = values.get("fundamento_passagens") if isinstance(values.get("fundamento_passagens"), list) else None
        steps.append({"teste": "fundamento declarado compatível com " + ", ".join(x["passage"] for x in rule.get("passages", [])),
                      "valor": declared, "ok": rules_mod.basis_allows(rule, declared), "efeito": "este limite conta"})
        g = aggregate.get("group") or {}
        steps.append({"teste": f"contratos da entidade {g.get('adjudicante')} com o adjudicatário {g.get('adjudicatario')}, adjudicados de "
                               f"{aggregate['window'][0]} até antes de {aggregate['window'][1]}, ao abrigo de "
                               + ", ".join(p.get("counts", {}).get("fundamento_em", [])), "valor": len(aggregate.get("sure", [])), "ok": True, "efeito": "contam"})
        for c in aggregate.get("sure", []):
            steps.append({"teste": f"BASE {c['id']} · {c.get('data_adjudicacao') or c.get('data_celebracao')} · {c.get('fundamento')}",
                          "valor": c.get("preco_contratual"), "ok": True, "efeito": "soma-se", "url": c.get("url")})
        a = p["aggregate"]
        steps.append({"teste": f"soma {aggregate['sum_min']:.2f} {a['comparator']} {a['value']:g}", "valor": aggregate["sum_min"], "ok": result == "cumpre",
                      "efeito": "cumpre" if result == "cumpre" else "não cumpre", "decide": True})
    else:
        steps.append({"teste": (detail or "").split(";")[0], "valor": None, "ok": result == "cumpre", "efeito": result, "decide": True})
    window = (detail or "").split("; ", 1) if rule["type"] != "agregada" else []
    if len(window) == 2:
        steps.insert(len(rule.get("conditions", [])), {"teste": window[1], "valor": None, "ok": True, "efeito": "mesma lei em todas as datas possíveis"})
    return steps


def resum(conn, v, again):
    """D96: the stored aggregate checked against ccp.base_contrato: each contract it sums read again by its BASE id
    (adjudicante, adjudicatário, preço contratual, fundamentação), the sum recomputed and compared with the limit. The
    full re-run needs every BASE record of the adjudicante (db/declared.py cache), which the API does not hold."""
    agg, rule = v["aggregate"], _rule_doc(v["rule"]["id"], v["rule"]["revision"]) or {}
    ids = [int(c["id"]) for c in agg.get("sure", [])]
    rows = dict(conn.execute("select id, doc from ccp.base_contrato where id = any(%s)", (ids,)).fetchall()) if ids else {}
    import declared as declared_mod
    import fundamento
    total, wrong = 0.0, []
    for c in agg.get("sure", []):
        doc = rows.get(int(c["id"]))
        if doc is None:
            wrong.append(f"{c['id']}: não está em ccp.base_contrato")
            continue
        r = declared_mod.reduce(int(c["id"]), None, None, base_detail.unpack(bytes(doc)))
        fp = set(fundamento.passages(r["fund"] or ""))
        ok = (r["preco"] == c["preco_contratual"] and agg["group"]["adjudicante"] in r["adjudicante"]
              and r["adjudicatarios"] == [agg["group"]["adjudicatario"]] and fp <= set((rule.get("params") or {}).get("counts", {}).get("fundamento_em", [])))
        if not ok:
            wrong.append(f"{c['id']}: o registo BASE não diz o que o veredicto soma")
        total += r["preco"] or 0
    import engine.rules as rules_mod
    res = rules_mod.aggregate_result(rule["params"], {"sum_min": round(total, 2), "sum_max": float("inf") if agg.get("sum_max") is None else agg["sum_max"]}) if rule else None
    same = not wrong and abs(round(total, 2) - agg["sum_min"]) < 0.005 and res == v["result"]
    return {"result": v["result"] if same else (again or {}).get("result"), "detail": f"soma recalculada dos {len(ids)} registos BASE: {total:.2f}"
            + (f"; {'; '.join(wrong)}" if wrong else ""), "how": "agregada: registos BASE relidos"}


def relatorio(unit):
    """D91: everything behind the verdicts of one procedure: the input (each fact and the official record it came from),
    the logic (law, rule, readers), the calculation (steps) and a re-run of the engine now, compared with the stored result."""
    if not UNIT.match(unit):
        raise serve.ApiError(400, "unidade: proc:base:<id>")
    conn = db()
    facts = [d for (d,) in conn.execute("select doc from ccp.facto where unit = %s", (unit,)).fetchall()]
    if not facts:
        raise serve.ApiError(404, "procedimento desconhecido")
    stored = [d for (d,) in conn.execute("select doc from ccp.veredicto_atual where unit = %s", (unit,)).fetchall()]
    raw_ids = sorted({(f.get("origin") or {}).get("raw") for f in facts} - {None})
    raws = [d for (d,) in conn.execute("select doc from ccp.raw where id = any(%s)", (raw_ids,)).fetchall()] if raw_ids else []
    import engine.evaluate as evaluate_mod
    known = max(f["known_at"] for f in facts)
    values, _ = evaluate_mod.read_facts(facts, known, max((f.get("valid_at") or "0") for f in facts))

    e = _engine()
    dates = e["mod"].child_dates(conn, [unit]).get(unit, [])
    now = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    rerun, why, how = e["mod"].evaluate_unit(unit, facts, dates, e["rules"], e["window"], now)
    rerun_by = {v["rule"]["id"]: v for v in rerun}
    for v in stored:  # D96: an aggregate is re-derived from BASE's stored record of each contract it names
        if v.get("aggregate"):
            rerun_by[v["rule"]["id"]] = resum(conn, v, rerun_by.get(v["rule"]["id"]))

    out = []
    for v in sorted(stored, key=lambda d: d["rule"]["id"]):
        rule = _rule_doc(v["rule"]["id"], v["rule"]["revision"]) or {"id": v["rule"]["id"], "conditions": [], "type": "?"}
        again = rerun_by.get(v["rule"]["id"])
        out.append({**verdict_out(v),
                    "regra_completa": {k: rule.get(k) for k in ("id", "revision", "type", "title", "conditions", "exceptions", "params", "valid_from", "valid_to", "passages")},
                    "leitores": [{"leitor": r.get("principal"), "familia": r.get("family"), "em": r.get("at"), "evento": r.get("evento"),
                                  "passagens": r.get("chosen_passages")} for r in rule.get("readings", [])],
                    "passos": _steps(rule, values, v["result"], v.get("detail"), v.get("aggregate")),
                    "codigo": {"commit": serve.COMMIT, "repositorio": serve.REPOSITORY,
                               "ficheiros": ["engine/rules.py", "engine/evaluate.py", "db/run_engine.py"],
                               "funcoes": {n: _source(n) for n in ("applies", "holds", "basis_allows")}},
                    "reproducao": {"resultado_agora": again and again["result"], "detalhe_agora": again and again.get("detail"),
                                   "igual": bool(again) and again["result"] == v["result"], "commit": serve.COMMIT, "em": now, "como": how or why}})
    return {"procedimento": unit, "gerado_em": now, "corrida": (latest_run() or {}).get("id"),
            "entrada": {"registos": [{"id": r["id"], "fonte": r.get("source"), "id_na_fonte": r.get("source_id"), "url": r.get("url"),
                                      "sha256": r.get("sha256"), "capturado_em": r.get("captured_at"), "formato": r.get("media_type")} for r in raws],
                        "factos": sorted(({"campo": f["field"], "valor": f.get("value"), "valido_em": f.get("valid_at"), "conhecido_em": f.get("known_at"),
                                           "campo_na_fonte": (f.get("origin") or {}).get("field"), "registo": (f.get("origin") or {}).get("raw"),
                                           "adaptador": f.get("adapter"), "id": f["id"]} for f in facts), key=lambda x: x["campo"])},
            "veredictos": out}


def page(query):
    def one(k, default=None):
        return (query.get(k) or [default])[0]
    res = one("resultado")
    if res not in (None, "cumpre", "nao_cumpre", "nao_avaliado"):
        raise serve.ApiError(400, "resultado: cumpre, nao_cumpre ou nao_avaliado")
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
    else:  # D96: the stored abstentions (a declared special regime) are listed only when asked for
        where.append("v.result <> 'nao_avaliado'")
    if regra:
        where.append("v.rule = %s"); args.append(regra)
    if nif:  # D90: the run recorded each verdict's adjudicante
        where.append("v.adjudicante = %s"); args.append(nif)
    rows = db().execute(f"select v.unit, v.doc from ccp.veredicto_atual v where {' and '.join(where)} order by v.unit limit %s", (*args, limit)).fetchall()
    items = [{"procedimento": u, **verdict_out(d)} for u, d in rows]
    return {"corrida": (latest_run() or {}).get("id"), "veredictos": items, "seguinte": rows[-1][0] if len(rows) == limit else None}


def entidade_veredictos(nif, query=None):
    if not NIF.match(nif):
        raise serve.ApiError(400, "nif: nove algarismos")
    return {"nif": nif, **veredictos({k: v for k, v in (query or {}).items() if k in ("resultado", "apos", "limite")}, nif)}


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
            if method == "GET" and path.startswith("/v1/procedimentos/") and path.endswith("/relatorio"):
                return self.send_json(200, relatorio(path[len("/v1/procedimentos/"):-len("/relatorio")]), CACHE)
            if method == "GET" and path.startswith("/v1/procedimentos/"):
                return self.send_json(200, procedimento(path[len("/v1/procedimentos/"):]), CACHE)
            query = parse_qs(urlsplit(self.path).query)
            if method == "GET" and path == "/v1/veredictos":
                return self.send_json(200, veredictos(query), CACHE)
            if method == "GET" and path.startswith("/v1/entidades/") and path.endswith("/veredictos"):
                return self.send_json(200, entidade_veredictos(path[len("/v1/entidades/"):-len("/veredictos")], query), CACHE)
            if method == "GET" and path == "/v1/estatisticas":
                return self.send_json(200, estatisticas(), CACHE)
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
    threading.Thread(target=_engine, daemon=True).start()  # D91: the report's re-run needs the rules; load them before the first request
    print(f"ccp api {VERSION} on http://{a.host}:{a.port}", flush=True)
    ThreadingHTTPServer((a.host, a.port), Handler).serve_forever()


if __name__ == "__main__":
    main()
