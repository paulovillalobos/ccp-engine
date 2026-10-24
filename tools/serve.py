"""The read-only API of ARQUITECTURA.md §9, skeleton: every route exists and answers, the computing ones with 501 until
phase 3 (rules and engine over facts). Standard library only.

    .venv/bin/python -I tools/serve.py [--host 127.0.0.1] [--port 5340] [--token <secret>]

    public   GET  /v1/saude              liveness (200)
             GET  /v1/openapi.json       this contract (200)
             GET  /v1/lei.json?data=     norms and passages in force on a date          501 until phase 3
             GET  /v1/manifesto.json     law, package, code and log versions             501 until phase 3
             GET  /v1/exemplo/<name>     a ready request and its answer                  501 until phase 3
    keyed    POST /v1/verificar          by consumer id or by facts sent                 501 until phase 3
             GET  /v1/regras/<name>      the rules                                       501 until phase 3
             GET  /v1/diff?de=&a=        diff by rule between two packages               501 until phase 3
             GET  /v1/entidade/<nif>     an entity (no name for a natural person)        501 until phase 3

What it never does: write a file, read a path a request names, call a model, call the network, log a request body,
echo a request path back, or return a stack trace. Limits: JSON only, 64 KB body, 30 s socket timeout. Bound to
localhost by default; with --token (or CCP_TOKEN) every keyed route needs X-API-Key.
Copied from rjue-engine's service tool and versioned here.
"""
import hmac
import json
import os
import sys
import time
import traceback
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlsplit

VERSION = "ccp-serve-0.1"
MAX_BODY = 64 * 1024
TOKEN = None
PHASE3 = {"erro": "não implementado até à fase 3 (regras e motor sobre factos)", "estado": 501}
PUBLIC = ("/v1/saude", "/v1/openapi.json", "/v1/lei.json", "/v1/manifesto.json")
KEYED_GET = ("/v1/diff",)
PREFIX_PUBLIC = ("/v1/exemplo/",)
PREFIX_KEYED = ("/v1/regras/", "/v1/entidade/")


def openapi():
    later = {"501": {"description": "não implementado até à fase 3"}}
    ok = {"200": {"description": "ok", "content": {"application/json": {"schema": {"type": "object"}}}}}
    keyed = {"401": {"description": "X-API-Key em falta ou errada"}}
    return {"openapi": "3.1.0",
            "info": {"title": "ccp-engine: o CCP decomposto em regras com vigência e citação verificada", "version": VERSION,
                     "description": "Só leitura. Cada veredicto diz cumpre / nao_cumpre / nao_avaliado com o motivo tipado, o passagem, a "
                                    "citação literal, a versão vigente e o manifesto que o torna reproduzível. Nenhum modelo é chamado."},
            "paths": {"/v1/saude": {"get": {"responses": ok}}, "/v1/openapi.json": {"get": {"responses": ok}},
                      "/v1/lei.json": {"get": {"parameters": [{"name": "data", "in": "query", "schema": {"type": "string", "format": "date"}}], "responses": later}},
                      "/v1/manifesto.json": {"get": {"responses": later}}, "/v1/exemplo/{nome}": {"get": {"responses": later}},
                      "/v1/verificar": {"post": {"responses": {**later, **keyed, "413": {"description": f"corpo acima de {MAX_BODY} bytes"}}}},
                      "/v1/regras/{nome}": {"get": {"responses": {**later, **keyed}}},
                      "/v1/diff": {"get": {"parameters": [{"name": "de", "in": "query", "schema": {"type": "string"}}, {"name": "a", "in": "query", "schema": {"type": "string"}}],
                                           "responses": {**later, **keyed}}},
                      "/v1/entidade/{nif}": {"get": {"responses": {**later, **keyed}}}}}


class Handler(BaseHTTPRequestHandler):
    server_version = "ccp-engine/" + VERSION
    sys_version = ""
    timeout = 30

    def log_message(self, fmt, *args):  # method, path, status: never a body
        sys.stderr.write("%s %s\n" % (time.strftime("%Y-%m-%dT%H:%M:%S"), fmt % args))

    def send_json(self, status, body):
        data = json.dumps(body, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()
        self.wfile.write(data)

    def authorised(self):
        return TOKEN is None or hmac.compare_digest(self.headers.get("X-API-Key", "").encode("utf-8"), TOKEN.encode("utf-8"))

    def route(self, method):
        try:
            path = urlsplit(self.path).path
            keyed = path in KEYED_GET or path.startswith(PREFIX_KEYED) or (method == "POST" and path == "/v1/verificar")
            known = keyed or path in PUBLIC or path.startswith(PREFIX_PUBLIC)
            if not known or (method == "POST") != (path == "/v1/verificar"):
                return self.send_json(404, {"erro": "não existe", "caminhos": list(PUBLIC) + ["/v1/exemplo/<nome>", "POST /v1/verificar", "/v1/regras/<nome>", "/v1/diff", "/v1/entidade/<nif>"]})
            if keyed and not self.authorised():
                return self.send_json(401, {"erro": "X-API-Key em falta ou errada"})
            if method == "POST":
                try:
                    length = int(self.headers.get("Content-Length", "0"))
                except ValueError:
                    return self.send_json(400, {"erro": "Content-Length inválido"})
                if length > MAX_BODY:
                    return self.send_json(413, {"erro": f"corpo acima de {MAX_BODY} bytes"})
                if (self.headers.get("Content-Type") or "").split(";")[0].strip() != "application/json":
                    return self.send_json(415, {"erro": "só JSON"})
            if path == "/v1/saude":
                return self.send_json(200, {"ok": True, "version": VERSION})
            if path == "/v1/openapi.json":
                return self.send_json(200, openapi())
            return self.send_json(501, PHASE3)
        except Exception:  # never a trace to the caller; the log has it
            traceback.print_exc(file=sys.stderr)
            return self.send_json(500, {"erro": "falha interna; o registo do servidor diz porquê"})

    def do_GET(self):
        self.route("GET")

    def do_POST(self):
        self.route("POST")


def main():
    global TOKEN
    args = sys.argv[1:]
    host = args[args.index("--host") + 1] if "--host" in args else os.environ.get("CCP_HOST", "127.0.0.1")
    port = int(args[args.index("--port") + 1]) if "--port" in args else int(os.environ.get("PORT", "5340"))
    TOKEN = args[args.index("--token") + 1] if "--token" in args else (os.environ.get("CCP_TOKEN") or None)
    server = ThreadingHTTPServer((host, port), Handler)
    server.daemon_threads = True
    sys.stderr.write(f"ccp-engine service on http://{host}:{port}/v1/ ({'token required on keyed routes' if TOKEN else 'no token'})\n")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
