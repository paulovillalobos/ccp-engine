"""The read-only API of ARQUITECTURA.md §9, v1 (local; nothing is deployed). Standard library and the engine only.

    .venv/bin/python tools/serve.py [--host 127.0.0.1] [--port 5340] [--token <secret>] [--stores law rules governance data]

    public   GET  /v1/saude                       liveness and what is loaded
             GET  /v1/openapi.json                this contract
             GET  /v1/lei.json?data=AAAA-MM-DD[&norma=norma:ccp]   the passage versions in force on that date
             GET  /v1/manifesto.json              packages (law version, hash, rules, log head), code, log head, verify
             GET  /v1/exemplo/<nome>              a ready request from examples/ and the answer computed now
    keyed    POST /v1/verificar                   {"id_consumidor": {"n_anuncio": ...} | {"base_id": ...}} or {"factos": {...}}
                                                  -> per rule: resultado, motivo, regra (id, revision, state), passagem,
                                                  citação, versão, manifesto, afirmação declarada beside it
             GET  /v1/regras/<id> | /v1/regras/indice
             GET  /v1/diff?de=pacote:..&a=pacote:..
             GET  /v1/entidade/<nif>              no name for a pessoa_singular (invariant 11)

The rules applied are the package the regime selects: the settled seletor_regime when there is one, else the package
whose law version is in force on the procedure's start date; with no package for that date the answer says so and
judges nothing. Facts sent in a request live only for that request (never written). What it never does: write a file,
read a path a request names, call a model, call the network, log a request body, echo a request path back, or return
a stack trace. Limits: JSON only, 64 KB body, 30 s socket timeout. Bound to localhost by default; with --token (or
CCP_TOKEN) every keyed route needs X-API-Key. Copied from rjue-engine's service tool and versioned here.
"""
import hmac
import json
import os
import re
import subprocess
import sys
import time
import traceback
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlsplit

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
import verify  # noqa: E402  (its readers of the store: the same ones RED uses)
from engine import evaluate as evaluate_mod  # noqa: E402
from engine import manifest as manifest_mod  # noqa: E402
from engine import rules as rules_mod  # noqa: E402
from engine.canon import canonical, sha256_text  # noqa: E402
from engine.governance import head  # noqa: E402
from engine.store import Store, facts_of  # noqa: E402
from engine.vigente import vigente  # noqa: E402

VERSION = "ccp-serve-1.0"
MAX_BODY = 64 * 1024
TOKEN = None
STORE = None
COMMIT = None
REPOSITORY = "github.com/paulovillalobos/ccp-engine"
DATE = re.compile(r"^[0-9]{4}-[0-9]{2}-[0-9]{2}$")
FIELDS = {"data_inicio_procedimento", "tipo_procedimento", "tipo_contrato", "preco_base", "publicado_joue", "prazo_propostas_dias", "prazo_candidaturas_dias", "data_envio_convite",
          "prazo_trabalhos_concecao_dias", "urgencia_fundamentada", "setores_especiais", "anuncio_pre_informacao", "modalidade_concecao",
          "data_envio_anuncio", "data_publicacao_anuncio", "territorio", "tipo_entidade", "adjudicante"}
PUBLIC = ("/v1/saude", "/v1/openapi.json", "/v1/lei.json", "/v1/manifesto.json")
KEYED_GET = ("/v1/diff",)
PREFIX_PUBLIC = ("/v1/exemplo/",)
PREFIX_KEYED = ("/v1/regras/", "/v1/entidade/")


class ApiError(Exception):
    def __init__(self, status, message):
        super().__init__(message)
        self.status, self.message = status, message


def openapi():
    ok = {"200": {"description": "ok", "content": {"application/json": {"schema": {"type": "object"}}}}}
    keyed = {"401": {"description": "X-API-Key em falta ou errada"}}
    bad = {"400": {"description": "pedido inválido"}}
    return {"openapi": "3.1.0",
            "info": {"title": "ccp-engine: o CCP decomposto em regras com vigência e citação verificada", "version": VERSION,
                     "description": "Só leitura. Cada veredicto diz cumpre / nao_cumpre / nao_avaliado com o motivo tipado, a passagem, a "
                                    "citação literal, a versão vigente e o manifesto que o torna reproduzível. Nenhum modelo é chamado."},
            "paths": {"/v1/saude": {"get": {"responses": ok}}, "/v1/openapi.json": {"get": {"responses": ok}},
                      "/v1/lei.json": {"get": {"parameters": [{"name": "data", "in": "query", "required": True, "schema": {"type": "string", "format": "date"}},
                                                              {"name": "norma", "in": "query", "schema": {"type": "string"}}], "responses": {**ok, **bad}}},
                      "/v1/manifesto.json": {"get": {"responses": ok}}, "/v1/exemplo/{nome}": {"get": {"responses": {**ok, "404": {"description": "não existe"}}}},
                      "/v1/verificar": {"post": {"responses": {**ok, **bad, **keyed, "413": {"description": f"corpo acima de {MAX_BODY} bytes"}, "415": {"description": "só JSON"}}}},
                      "/v1/regras/{id}": {"get": {"responses": {**ok, **keyed}}},
                      "/v1/diff": {"get": {"parameters": [{"name": "de", "in": "query", "schema": {"type": "string"}}, {"name": "a", "in": "query", "schema": {"type": "string"}}],
                                           "responses": {**ok, **bad, **keyed}}},
                      "/v1/entidade/{nif}": {"get": {"responses": {**ok, **keyed}}}}}


# ---- what the routes compute ----------------------------------------------------------------------------------
def packages():
    return verify.current_of(STORE, "pacote")


def manifesto():
    return {"pacotes": [{"id": p["id"], "law_version": p["law_version"], "hash": p["hash"], "regras": len(p["rules"]), "log_head": p["log_head"], "built_at": p["built_at"]}
                        for p in sorted(packages().values(), key=lambda p: p["id"])],
            "log_head": head(STORE.events), "eventos": len(STORE.events),
            "code": {"repository": REPOSITORY, "commit": COMMIT, "engine_version": evaluate_mod.VERSION, "serve": VERSION}, "verify": verify.VERSION}


def lei(query):
    data = (query.get("data") or [None])[0]
    if not data or not DATE.match(data):
        raise ApiError(400, "data em falta ou não é AAAA-MM-DD")
    norma = (query.get("norma") or [None])[0]
    found = vigente(STORE, data)
    if norma:
        prefix = STORE.current(norma)["short"] + ":" if STORE.current(norma) else None
        if prefix is None:
            raise ApiError(404, "norma desconhecida")
        found = {k: v for k, v in found.items() if k.startswith(prefix)}
    return {"data": data, "norma": norma, "contagem": len(found), "passagens": dict(sorted(found.items()))}


def selector():
    for pk in sorted(packages().values(), key=lambda p: p["id"]):
        rules, _ = verify.package_rules(STORE, pk["id"])
        for r in rules:
            if r["type"] == "seletor_regime" and r["state"] == "settled":
                return r
    return None


def choose_package(start):
    """(package id, law version, how): by the settled selector, else the package whose law is in force on the date."""
    sel = selector()
    if sel:
        for g in sel["params"]["regimes"]:
            if g["from"] <= start and (g["to"] is None or start < g["to"]):
                return g["package"], g["law_version"], f"seletor {sel['id']}"
    dated = [p for p in packages().values() if p["law_version"].split("@")[1] <= start]
    if not dated:
        return None, None, "nenhum pacote em vigor na data de início"
    p = max(dated, key=lambda p: p["law_version"])
    return p["id"], p["law_version"], "pacote em vigor na data (sem seletor settled)"


def verdict_out(v, rule):
    c = v["citation"]
    return {"regra": {"id": v["rule"]["id"], "revision": v["rule"]["revision"], "estado": rule["state"], "titulo": rule["title"]},
            "resultado": v["result"], "motivo": v["reason"], "detalhe": v["detail"],
            "passagem": c["passage"] if c else None, "versao": c["version"] if c else None, "citacao": c["quote"] if c else None,
            "afirmacoes_declaradas": v["assertions_compared"], "factos_usados": v["facts_used"]}


def verificar(body):
    if not isinstance(body, dict) or (("id_consumidor" in body) == ("factos" in body)):
        raise ApiError(400, "envie id_consumidor ou factos (um dos dois)")
    now = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    if "id_consumidor" in body:
        ids = body["id_consumidor"]
        if not isinstance(ids, dict) or not ids or not all(isinstance(v, str) for v in ids.values()):
            raise ApiError(400, "id_consumidor: objeto com n_anuncio ou base_id")
        unit = next((u for u in verify.current_of(STORE, "unidade").values() if u["kind"] == "proc" and any(u["consumer_ids"].get(k) == v for k, v in ids.items())), None)
        if unit is None:
            raise ApiError(404, "procedimento desconhecido")
        facts = facts_of(STORE, unit["id"])
        known_at = max((f["known_at"] for f in facts), default=now)
        adapters = sorted({f["adapter"] for f in facts})
        snaps = [{"source": STORE.current(r)["source"], "sha256": STORE.current(r)["sha256"], "captured_at": STORE.current(r)["captured_at"]}
                 for r in sorted({f["origin"]["raw"] for f in facts if f.get("origin")}) if STORE.current(r)]
        assertions = [a for a in verify.current_of(STORE, "afirmacao").values() if a["unit"] == unit["id"]]
    else:
        given = body["factos"]
        if not isinstance(given, dict) or set(given) - FIELDS:
            raise ApiError(400, f"factos: só os campos {sorted(FIELDS)}")
        known_at = now
        unit = {"id": f"proc:pedido:{sha256_text(canonical(given))[:16]}", "revision": 1, "recorded_at": now, "kind": "proc", "parent": None, "raw": [], "consumer_ids": {}}
        start = given.get("data_inicio_procedimento", now[:10])
        facts = [{"id": f"facto:pedido:{k}", "revision": 1, "recorded_at": now, "unit": unit["id"], "field": k, "value": v,
                  "origin": None, "adapter": "adaptador:pedido@1", "valid_at": start, "known_at": now} for k, v in sorted(given.items())]
        adapters = ["adaptador:pedido@1"]
        snaps = [{"source": "pedido", "sha256": sha256_text(canonical(given)), "captured_at": now}]
        assertions = []
    start = next((f["value"] for f in facts if f["field"] == "data_inicio_procedimento"), None)
    if not isinstance(start, str) or not DATE.match(start):
        return {"procedimento": unit["id"], "regime": None, "veredictos": [], "nota": "sem data_inicio_procedimento: nenhuma regra é avaliada (facto_ausente)"}
    package, law_version, how = choose_package(start)
    if package is None:
        return {"procedimento": unit["id"], "regime": {"data_inicio": start, "como": how}, "veredictos": [], "nota": how}
    rules, _ = verify.package_rules(STORE, package)
    rules = [r for r in rules if "proc" in r["applies_to"]]
    manifest = manifest_mod.build(law_version, package, adapters or ["adaptador:pedido@1"], snaps or [{"source": "pedido", "sha256": sha256_text(canonical(facts)), "captured_at": now}],  # D98: the facts read, never a placeholder
                                  {"repository": REPOSITORY, "commit": COMMIT, "engine_version": evaluate_mod.VERSION}, head(STORE.events), known_at)
    out = evaluate_mod.evaluate(unit, rules, facts, known_at, start, manifest=manifest, assertions=assertions)
    by_id = {r["id"]: r for r in rules}
    return {"procedimento": unit["id"], "regime": {"data_inicio": start, "pacote": package, "law_version": law_version, "como": how},
            "manifesto": manifest, "veredictos": [verdict_out(v, by_id[v["rule"]["id"]]) for v in sorted(out, key=lambda v: v["rule"]["id"])]}


def regras(name):
    rules = verify.current_of(STORE, "regra")
    if name == "indice":
        return {"regras": [{"id": r["id"], "tipo": r["type"], "estado": r["state"], "valid_from": r["valid_from"], "valid_to": r["valid_to"]}
                           for r in sorted(rules.values(), key=lambda r: r["id"])]}
    rid = name if name.startswith("regra:") else f"regra:{name}"
    if rid not in rules:
        raise ApiError(404, "regra desconhecida")
    return rules[rid]


def diff(query):
    de, a = (query.get("de") or [None])[0], (query.get("a") or [None])[0]
    pk = packages()
    if not de or not a:
        raise ApiError(400, "de e a: dois pacotes")
    if de not in pk or a not in pk:
        raise ApiError(404, "pacote desconhecido")
    return {"de": de, "a": a, **rules_mod.diff(pk[de], pk[a], verify.current_of(STORE, "regra"))}


def entidade(nif):
    if not re.match(r"^[0-9]{9}$", nif):
        raise ApiError(400, "nif: nove algarismos")
    e = next((e for e in verify.current_of(STORE, "entidade").values() if e.get("nif") == nif), None)
    if e is None:
        raise ApiError(404, "entidade desconhecida")
    out = {k: v for k, v in e.items() if k in ("id", "type", "nif", "roles", "name")}
    if e["type"] == "pessoa_singular":
        out.pop("name", None)  # invariant 11: a natural person is never named in what the service publishes
    return out


def exemplo(name):
    if not re.match(r"^[a-z0-9-]{1,60}$", name):
        raise ApiError(404, "não existe")
    path = ROOT / "examples" / f"{name}.json"
    if not path.exists():
        raise ApiError(404, "não existe")
    request = json.loads(path.read_text(encoding="utf-8"))
    return {"pedido": request, "resposta": verificar(request["corpo"]) if request.get("rota") == "POST /v1/verificar" else None}


# ---- HTTP ----------------------------------------------------------------------------------------------------
class Handler(BaseHTTPRequestHandler):
    server_version = "ccp-engine/" + VERSION
    sys_version = ""
    timeout = 30

    def log_message(self, fmt, *args):  # method, path, status: never a body
        sys.stderr.write("%s %s\n" % (time.strftime("%Y-%m-%dT%H:%M:%S"), fmt % args))

    def send_json(self, status, body, cache=None):
        """cache: a Cache-Control value for a public read that only changes with the daily run; default no-store."""
        data = json.dumps(body, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", cache if cache and status == 200 else "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()
        self.wfile.write(data)

    def authorised(self):
        return TOKEN is None or hmac.compare_digest(self.headers.get("X-API-Key", "").encode("utf-8"), TOKEN.encode("utf-8"))

    def route(self, method):
        try:
            parts = urlsplit(self.path)
            path, query = parts.path, parse_qs(parts.query)
            keyed = path in KEYED_GET or path.startswith(PREFIX_KEYED) or (method == "POST" and path == "/v1/verificar")
            known = keyed or path in PUBLIC or path.startswith(PREFIX_PUBLIC)
            if not known or (method == "POST") != (path == "/v1/verificar"):
                return self.send_json(404, {"erro": "não existe", "caminhos": list(PUBLIC) + ["/v1/exemplo/<nome>", "POST /v1/verificar", "/v1/regras/<id>", "/v1/diff", "/v1/entidade/<nif>"]})
            if keyed and not self.authorised():
                return self.send_json(401, {"erro": "X-API-Key em falta ou errada"})
            body = None
            if method == "POST":
                try:
                    length = int(self.headers.get("Content-Length", "0"))
                except ValueError:
                    return self.send_json(400, {"erro": "Content-Length inválido"})
                if length > MAX_BODY:
                    return self.send_json(413, {"erro": f"corpo acima de {MAX_BODY} bytes"})
                if (self.headers.get("Content-Type") or "").split(";")[0].strip() != "application/json":
                    return self.send_json(415, {"erro": "só JSON"})
                try:
                    body = json.loads(self.rfile.read(length).decode("utf-8"))
                except (UnicodeDecodeError, json.JSONDecodeError):
                    return self.send_json(400, {"erro": "corpo não é JSON"})
            if path == "/v1/saude":
                return self.send_json(200, {"ok": True, "version": VERSION, "objetos": sum(len(v) for v in STORE.objects.values()), "eventos": len(STORE.events)})
            if path == "/v1/openapi.json":
                return self.send_json(200, openapi())
            if path == "/v1/lei.json":
                return self.send_json(200, lei(query))
            if path == "/v1/manifesto.json":
                return self.send_json(200, manifesto())
            if path.startswith("/v1/exemplo/"):
                return self.send_json(200, exemplo(path[len("/v1/exemplo/"):]))
            if path == "/v1/verificar":
                return self.send_json(200, verificar(body))
            if path.startswith("/v1/regras/"):
                return self.send_json(200, regras(path[len("/v1/regras/"):]))
            if path == "/v1/diff":
                return self.send_json(200, diff(query))
            if path.startswith("/v1/entidade/"):
                return self.send_json(200, entidade(path[len("/v1/entidade/"):]))
            return self.send_json(404, {"erro": "não existe"})
        except ApiError as exc:
            return self.send_json(exc.status, {"erro": exc.message})
        except Exception:  # never a trace to the caller; the log has it
            traceback.print_exc(file=sys.stderr)
            return self.send_json(500, {"erro": "falha interna; o registo do servidor diz porquê"})

    def do_GET(self):
        self.route("GET")

    def do_POST(self):
        self.route("POST")


def load(stores, commit=None):
    global STORE, COMMIT
    STORE = Store([ROOT / s if not Path(s).is_absolute() else Path(s) for s in stores]).load()
    COMMIT = commit or subprocess.run(["git", "rev-parse", "--short=9", "HEAD"], capture_output=True, text=True, cwd=ROOT).stdout.strip() or "0000000"


def make_server(host, port, token=None, stores=("law", "rules", "governance", "data"), commit=None):
    global TOKEN
    TOKEN = token
    load(stores, commit)
    server = ThreadingHTTPServer((host, port), Handler)
    server.daemon_threads = True
    return server


def main():
    args = sys.argv[1:]
    host = args[args.index("--host") + 1] if "--host" in args else os.environ.get("CCP_HOST", "127.0.0.1")
    port = int(args[args.index("--port") + 1]) if "--port" in args else int(os.environ.get("PORT", "5340"))
    token = args[args.index("--token") + 1] if "--token" in args else (os.environ.get("CCP_TOKEN") or None)
    stores = args[args.index("--stores") + 1:] if "--stores" in args else ["law", "rules", "governance", "data"]
    server = make_server(host, port, token, stores)
    sys.stderr.write(f"ccp-engine service on http://{host}:{port}/v1/ ({'token required on keyed routes' if token else 'no token'})\n")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
