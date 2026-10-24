"""tools/serve.py v1 over the fixture store: every route of §9, the key, the limits, invariant 11."""
import json
import sys
import threading
import urllib.error
import urllib.request
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))


@pytest.fixture(scope="module")
def base():
    import serve
    server = serve.make_server("127.0.0.1", 0, token="segredo", stores=[str(ROOT / "fixtures/valid")], commit="abcdef1")
    t = threading.Thread(target=server.serve_forever, daemon=True)
    t.start()
    yield f"http://127.0.0.1:{server.server_address[1]}"
    server.shutdown()


def call(base, path, body=None, key="segredo", ctype="application/json", raw=None):
    data = raw if raw is not None else (json.dumps(body).encode("utf-8") if body is not None else None)
    req = urllib.request.Request(base + path, data=data, method="POST" if data is not None else "GET")
    if key:
        req.add_header("X-API-Key", key)
    if data is not None:
        req.add_header("Content-Type", ctype)
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.status, json.loads(r.read())
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read())


def test_public_routes(base):
    assert call(base, "/v1/saude", key=None)[1]["ok"] is True
    assert call(base, "/v1/openapi.json", key=None)[0] == 200
    status, lei = call(base, "/v1/lei.json?data=2026-10-03", key=None)
    assert status == 200 and lei["contagem"] > 0 and lei["passagens"]
    assert call(base, "/v1/lei.json?data=ontem", key=None)[0] == 400
    status, m = call(base, "/v1/manifesto.json", key=None)
    assert status == 200 and m["pacotes"] and m["code"]["commit"] == "abcdef1"


def test_keyed_routes_need_the_key(base):
    assert call(base, "/v1/regras/indice", key=None)[0] == 401
    assert call(base, "/v1/regras/indice", key="errada")[0] == 401
    status, idx = call(base, "/v1/regras/indice")
    assert status == 200 and any(r["id"] == "regra:ccp:limiar-ajuste-direto-bens@v1" for r in idx["regras"])
    assert call(base, "/v1/regras/regra:ccp:limiar-ajuste-direto-bens@v1")[1]["type"] == "limiar"
    status, d = call(base, "/v1/diff?de=pacote:ccp@2026-09-30&a=pacote:ccp@2026-10-01")
    assert status == 200 and d["by_rule"]


def test_verificar_by_consumer_id_returns_verdict_citation_version_manifest(base):
    status, out = call(base, "/v1/verificar", {"id_consumidor": {"n_anuncio": "FX-2026-000001"}})
    assert status == 200 and out["regime"]["pacote"] == "pacote:ccp@2026-10-01"
    assert out["manifesto"]["law_version"] == "lei:ccp@2026-10-01"
    v = {x["regra"]["id"]: x for x in out["veredictos"]}
    prazo = v["regra:ccp:prazo-minimo-propostas-6-dias@v1"]
    assert prazo["resultado"] == "cumpre" and prazo["passagem"] and prazo["citacao"] and prazo["versao"]
    assert v["regra:ccp:limiar-ajuste-direto-bens@v1"]["afirmacoes_declaradas"], "the declared regime sits beside the verdict"
    assert call(base, "/v1/verificar", {"id_consumidor": {"n_anuncio": "NAO-EXISTE"}})[0] == 404


def test_verificar_by_facts_sent(base):
    facts = {"data_inicio_procedimento": "2026-10-03", "tipo_procedimento": "ajuste_direto", "tipo_contrato": "bens", "preco_base": 25000,
             "publicado_joue": False, "prazo_propostas_dias": 3}
    status, out = call(base, "/v1/verificar", {"factos": facts})
    assert status == 200
    v = {x["regra"]["id"]: x for x in out["veredictos"]}
    assert v["regra:ccp:limiar-ajuste-direto-bens@v1"]["resultado"] == "nao_cumpre"
    assert v["regra:ccp:prazo-minimo-propostas-6-dias@v1"]["resultado"] == "nao_cumpre"
    assert call(base, "/v1/verificar", {"factos": {"campo_estranho": 1}})[0] == 400
    assert call(base, "/v1/verificar", {"factos": {}, "id_consumidor": {"n_anuncio": "x"}})[0] == 400


def test_entity_without_name_for_a_natural_person(base):
    status, e = call(base, "/v1/entidade/200000000")
    assert status == 200 and e["type"] == "pessoa_singular" and "name" not in e
    status, e = call(base, "/v1/entidade/500000000")
    assert status == 200 and e["name"]


def test_limits_and_unknown_paths(base):
    assert call(base, "/v1/verificar", raw=b"{" + b" " * (64 * 1024 + 1) + b"}")[0] == 413
    assert call(base, "/v1/verificar", raw=b"{}", ctype="text/plain")[0] == 415
    assert call(base, "/v1/verificar", raw=b"nao json")[0] == 400
    status, out = call(base, "/v1/../../etc/passwd", key=None)
    assert status == 404 and "passwd" not in json.dumps(out)


def test_public_example_is_reproducible_from_the_repo(base):
    status, ex = call(base, "/v1/exemplo/verificar-empreitada-ajuste-direto", key=None)
    assert status == 200 and ex["pedido"]["rota"] == "POST /v1/verificar" and "resposta" in ex
    assert call(base, "/v1/exemplo/nao-existe", key=None)[0] == 404
