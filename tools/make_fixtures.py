"""Regenerates fixtures/valid and fixtures/broken from fixed text: hashes, offsets and the governance chain are computed,
everything else is literal. The fixtures in the repository must equal this script's output (tests/test_fixtures_rederive.py).

    python tools/make_fixtures.py            writes into <repo>/fixtures
    python tools/make_fixtures.py OUT_DIR    writes into OUT_DIR/{valid,broken}

Fixture law texts are paraphrases marked FIXTURE (DECISIONS D18). No network, no model.
"""
import json, shutil, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
OUT = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "fixtures"
sys.path.insert(0, str(ROOT))
from engine.canon import canonical, sha256_text, sha256_bytes, content_hash
from engine import schema

V = OUT / "valid"
B = OUT / "broken"
for d in (V, B):
    if d.exists():
        shutil.rmtree(d)
(V / "raw_bytes").mkdir(parents=True)
(V / "governance").mkdir()
REC = "2026-10-24T20:00:00Z"
CAP_LAW = "2026-10-24T18:00:00Z"
CAP_DUMP = "2026-10-24T18:30:00Z"
CAP_API = "2026-10-24T18:45:00Z"
CAP_DOC = "2026-10-24T18:50:00Z"

def env(obj, rev=1):
    return {"id": obj["id"], "revision": rev, "recorded_at": REC, **{k: v for k, v in obj.items() if k != "id"}}

def write(type_, name, obj):
    errs = schema.validate(type_, obj)
    assert not errs, (type_, name, errs)
    p = V / type_ / f"{name}.json"
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return obj

# ---- raw bytes -------------------------------------------------------------------------------------------------
LAW_LINES = [
    "FIXTURE: texto de exemplo com a forma da lei, não é a lei.",
    "Artigo 20.º",
    "1 - A escolha do ajuste direto permite a celebração de contratos:",
    "a) De valor inferior a 20 000 EUR, quando se trate de contratos de aquisição de bens ou serviços;",
    "Artigo 113.º",
    "2 - Não podem ser convidadas entidades às quais a entidade adjudicante já tenha adjudicado, no ano económico em curso e nos dois anos anteriores, propostas de valor acumulado igual ou superior ao limiar;",
    "Artigo 136.º",
    "1 - O prazo mínimo para a apresentação das propostas é de seis dias a contar da data do envio do anúncio;",
    "Artigo 131.º",
    "1 - O programa do procedimento indica o prazo para a apresentação das propostas e os critérios de adjudicação;",
    "Artigo 48.º",
    "1 - É proibido o fracionamento da despesa com o fim de a subtrair ao regime aplicável;",
    "Artigo 16.º",
    "1 - Para a formação de contratos as entidades adjudicantes adotam o concurso público, o concurso limitado por prévia qualificação, a consulta prévia ou o ajuste direto;",
    "Nota de vigência: Redação dada pelo Decreto-Lei n.º 177/2026, em vigor desde 2026-10-01.",
    "Decreto-Lei n.º 177/2026, Artigo 7.º",
    "1 - O presente decreto-lei aplica-se aos procedimentos iniciados a partir de 2026-10-01.",
    "Decreto Legislativo Regional n.º 27/2015/A, Artigo 3.º",
    "1 - Os limiares previstos no Código aplicam-se na Região com o coeficiente de 1,45.",
]
LAW_TEXT = "\n".join(LAW_LINES) + "\n"
def span(line):
    i = LAW_TEXT.index(line); return i, i + len(line)
SHA_LAW = sha256_text(LAW_TEXT)
(V / "raw_bytes" / SHA_LAW).write_text(LAW_TEXT, encoding="utf-8")

DUMP = {"nAnuncio": "FX-2026-000001", "tipoContrato": "Aquisição de bens móveis", "precoBase": "15000,00", "prazoPropostas": "9",
        "dataPublicacao": "03-10-2026", "tipoProcedimento": "Ajuste direto", "publicadoJOUE": "Não",
        "nifEntidadeAdjudicante": "500000000", "entidadeAdjudicante": "Município Fixture", "regime": "Código dos Contratos Públicos, artigo 20.º, n.º 1, alínea a)"}
DUMP_TEXT = json.dumps(DUMP, ensure_ascii=False, indent=1) + "\n"; SHA_DUMP = sha256_text(DUMP_TEXT)
(V / "raw_bytes" / SHA_DUMP).write_text(DUMP_TEXT, encoding="utf-8")
API = {"id": "99000001", "precoBase": 18000.0, "nAnuncio": "FX-2026-000001", "adjudicatario": {"nome": "Fornecedor Fixture Unipessoal", "nif": "200000000"}}
API_TEXT = json.dumps(API, ensure_ascii=False, indent=1) + "\n"; SHA_API = sha256_text(API_TEXT)
(V / "raw_bytes" / SHA_API).write_text(API_TEXT, encoding="utf-8")
DOC_BYTES = b"%PDF-1.4\n% FIXTURE scanned piece without text layer\n%%EOF\n"; SHA_DOC = sha256_bytes(DOC_BYTES)
(V / "raw_bytes" / SHA_DOC).write_bytes(DOC_BYTES)

def raw(id_, source, kind, sid, sha, media, enc, url, cap):
    return write("raw", id_.split(":", 1)[1].replace(":", "-"), env({"id": id_, "source": source, "kind": kind, "source_id": sid, "sha256": sha,
        "bytes": f"raw_bytes/{sha}", "media_type": media, "encoding": enc, "url": url, "captured_at": cap, "request": {"method": "GET", "reads_of_page": 1}}))
RAW_LAW = raw("raw:dr-consolidado:lei:ccp-fixture", "dr-consolidado", "lei", "ccp-fixture", SHA_LAW, "text/plain", "utf-8", "https://diariodarepublica.pt/dr/legislacao-consolidada/decreto-lei/2008-34455475", CAP_LAW)["id"]
RAW_DUMP = raw("raw:base-dump:anuncio:FX-2026-000001", "base-dump", "anuncio", "FX-2026-000001", SHA_DUMP, "application/json", "utf-8", "https://dados.gov.pt/pt/datasets/anuncios-2026/", CAP_DUMP)["id"]
RAW_API = raw("raw:base-api:contrato:99000001", "base-api", "contrato", "99000001", SHA_API, "application/json", "utf-8", "https://www.base.gov.pt/Base4/pt/detalhe/?type=contratos&id=99000001", CAP_API)["id"]
RAW_DOC = raw("raw:pecas:documento:FX-2026-000001-programa", "pecas", "documento", "FX-2026-000001-programa", SHA_DOC, "application/pdf", "binary", "https://www.acingov.pt/acingovprod/2/index.php/fixture/programa.pdf", CAP_DOC)["id"]

# ---- normas and passages --------------------------------------------------------------------------------------
write("norma", "ccp", env({"id": "norma:ccp", "title": "Código dos Contratos Públicos (Decreto-Lei n.º 18/2008, texto consolidado)", "short": "ccp", "jurisdiction": "PT",
    "scope": "contratação pública: formação e execução de contratos públicos", "eli": "https://data.dre.pt/eli/dec-lei/18/2008/01/29/p/dre/pt/html", "source": {"url": "https://diariodarepublica.pt/dr/legislacao-consolidada/decreto-lei/2008-34455475", "raw": [RAW_LAW]}}))
write("norma", "dl-177-2026", env({"id": "norma:dl-177-2026", "title": "Decreto-Lei n.º 177/2026 (altera o Código dos Contratos Públicos)", "short": "dl-177-2026", "jurisdiction": "PT",
    "scope": "alteração ao CCP; aplicação aos procedimentos iniciados desde 2026-10-01", "source": {"url": "https://diariodarepublica.pt/dr/detalhe/decreto-lei/177-2026-fixture", "raw": [RAW_LAW]}}))
write("norma", "dlr-27-2015-a", env({"id": "norma:dlr-27-2015-a", "title": "Decreto Legislativo Regional n.º 27/2015/A (Açores)", "short": "dlr-27-2015-a", "jurisdiction": "PT-AC",
    "scope": "regime regional de contratação pública", "source": {"url": "https://diariodarepublica.pt/dr/detalhe/decreto-legislativo-regional/27-2015-fixture", "raw": [RAW_LAW]}}))

def passage(id_, norma, parent, kind, label, line, vfrom="2026-10-01"):
    s, e = span(line)
    return write("passagem", id_.replace(":", "-"), env({"id": id_, "norma": norma, "parent": parent, "kind": kind, "label": label,
        "versions": [{"version": vfrom, "text": line, "raw": RAW_LAW, "offsets": {"start": s, "end": e}, "valid_from": vfrom, "valid_to": None, "revoked": False}]}))
P = {}
for id_, norma, parent, kind, label, line in [
    ("ccp:art20", "norma:ccp", None, "artigo", "Artigo 20.º", LAW_LINES[1]),
    ("ccp:art20.1", "norma:ccp", "ccp:art20", "numero", "1", LAW_LINES[2]),
    ("ccp:art20.1.a", "norma:ccp", "ccp:art20.1", "alinea", "a)", LAW_LINES[3]),
    ("ccp:art113.2", "norma:ccp", None, "numero", "2", LAW_LINES[5]),
    ("ccp:art136.1", "norma:ccp", None, "numero", "1", LAW_LINES[7]),
    ("ccp:art131.1", "norma:ccp", None, "numero", "1", LAW_LINES[9]),
    ("ccp:art48.1", "norma:ccp", None, "numero", "1", LAW_LINES[11]),
    ("ccp:art16.1", "norma:ccp", None, "numero", "1", LAW_LINES[13]),
    ("dl-177-2026:art7.1", "norma:dl-177-2026", None, "numero", "1", LAW_LINES[16]),
    ("dlr-27-2015-a:art3.1", "norma:dlr-27-2015-a", None, "numero", "1", LAW_LINES[18]),
]:
    P[id_] = passage(id_, norma, parent, kind, label, line)

NOTE = LAW_LINES[14]; ns, ne = span(NOTE)
write("vigencia", "ccp-art20.1.a@2026-10-01", env({"id": "ccp:art20.1.a@2026-10-01", "passage": "ccp:art20.1.a", "valid_from": "2026-10-01", "valid_to": None,
    "altered_by": "norma:dl-177-2026", "note": {"raw": RAW_LAW, "quote": NOTE, "offsets": {"start": ns, "end": ne}}, "effect": "altera"}))

def cite(pid, sub):
    text = P[pid]["versions"][0]["text"]; s = text.index(sub)
    return {"passage": pid, "version": "2026-10-01", "quote": sub, "offsets": {"start": s, "end": s + len(sub)}}

# ---- governance log --------------------------------------------------------------------------------------------
def principal(id_, kind, papel, familia=None, motor=None, versao=None, code=None, hash_=None, nota=None, retired=False):
    p = {"id": id_, "kind": kind, "papel": papel, "familia": familia, "motor": motor, "versao": versao, "code": code, "hash": hash_, "retired": retired}
    if nota: p["nota"] = nota
    return p
TOOL_CODE = "tools/make_fixtures.py"
TOOL_HASH = sha256_bytes(Path(__file__).read_bytes())
PRINCIPALS = {"principals": [
    principal("pessoa:paulo", "humano", "pessoa", nota="decides product rules and approves with a reason; never legal content"),
    principal("pessoa:revisor-fixture", "humano", "pessoa", nota="fixture: second person for adjudications"),
    principal("leitor:a", "automatizado", "leitor", "A", {"id": "fixture-engine-a", "versao": "0"}, nota="proposes readings by choosing passage ids"),
    principal("leitor:b", "automatizado", "leitor", "B", {"id": "fixture-engine-b", "versao": "0"}, nota="blind reader of the other family"),
    principal("extrator:a", "automatizado", "extrator", "A", {"id": "fixture-engine-a", "versao": "0"}, nota="proposes facts, links and conversions from records and documents"),
    principal("redator:a", "automatizado", "redator", "A", {"id": "fixture-engine-a", "versao": "0"}, nota="explains what is decided; records nothing"),
    principal("ferramenta:ccp-link@1", "codigo", "ferramenta", versao=1, code=TOOL_CODE, hash_=TOOL_HASH, nota="exact-NIF entity links (fixture: hashed to this generator)"),
    principal("ferramenta:verify@1", "codigo", "ferramenta", versao=1, code=TOOL_CODE, hash_=TOOL_HASH, nota="invalidates on failed re-derivation (fixture: hashed to this generator)"),
]}
assert not schema.validate("principals", PRINCIPALS)
(V / "governance/principals.json").write_text(json.dumps(PRINCIPALS, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

EVENTS = []
def event(principal, action, atype, assertion, *, payload=None, reason=None, question=None, independence=None, verdict=None, outcome=None, expected_revision=None, at=None):
    seq = len(EVENTS) + 1
    prev = "0" * 64 if not EVENTS else sha256_text(canonical(EVENTS[-1]))
    ev = {"id": f"evento:{seq}", "seq": seq, "at": at or f"2026-10-24T19:{seq:02d}:00Z", "prev": prev, "principal": principal, "action": action,
          "assertion_type": atype, "assertion": assertion, "expected_revision": expected_revision, "payload": payload or {}, "reason": reason,
          "question": question, "independence": independence, "verdict": verdict, "outcome": outcome}
    errs = schema.validate("evento", ev); assert not errs, errs
    EVENTS.append(ev); return ev["id"]

def read_pair(rule_id, passages, second=True):
    """propose by AMALIA, blind uphold by Reader B -> settled."""
    e1 = event("leitor:a", "propose", "regra", rule_id, payload={"chosen_passages": passages}, expected_revision=None)
    e2 = None
    if second:
        e2 = event("leitor:b", "review", "regra", rule_id, payload={"chosen_passages": passages}, expected_revision=1,
                   question=f"Blind: which passages ground {rule_id}? Proposed: {', '.join(passages)}", independence="blind", verdict="uphold")
    return e1, e2

def readings(rule_id, passages, e1, e2):
    r = [{"principal": "leitor:a", "family": "A", "at": EVENTS[int(e1.split(':')[1]) - 1]["at"], "chosen_passages": passages, "blind": False, "evento": e1}]
    if e2:
        r.append({"principal": "leitor:b", "family": "B", "at": EVENTS[int(e2.split(':')[1]) - 1]["at"], "chosen_passages": passages, "blind": True, "evento": e2})
    return r

# product rule: completeness threshold, a pessoa's decision with its reason (settled on record)
E_PR_OK = event("pessoa:paulo", "propose", "product_rule", "product_rule:completude-agregadas", payload={"ratio": 0.9, "measured_over": "mes", "recommendation": "ARQUITECTURA.md section 12"},
                reason="Product rule: aggregate rules answer cobertura_insuficiente below 90 percent monthly coverage of BASE for the period.")

RULES = []
def rule(name, type_, title, norma, jur, applies, conditions, exceptions, passages, params, second=True, state=None):
    rid = f"regra:{norma.split(':')[1]}:{name}@v1"
    pids = [c["passage"] for c in passages]
    e1, e2 = read_pair(rid, pids, second)
    st = state or ("settled" if second else "proposed")
    obj = env({"id": rid, "type": type_, "title": title, "norma": norma, "jurisdiction": jur, "applies_to": applies, "conditions": conditions,
               "exceptions": exceptions, "valid_from": "2026-10-01", "valid_to": None, "passages": passages, "params": params,
               "readings": readings(rid, pids, e1, e2), "state": st})
    write("regra", f"{norma.split(':')[1]}-{name}", obj); RULES.append(obj); return rid

R_SEL = rule("seletor-regime-dl-177-2026", "seletor_regime", "Regime aplicável pela data de início do procedimento (art. 7.º DL 177/2026)", "norma:dl-177-2026", "PT", ["proc"],
    [], [], [cite("dl-177-2026:art7.1", "aplica-se aos procedimentos iniciados a partir de 2026-10-01")],
    {"selects_by": "data_inicio_procedimento", "regimes": [
        {"from": "2008-07-30", "to": "2026-09-30", "law_version": "lei:ccp@2026-09-30", "package": "pacote:ccp@2026-09-30"},
        {"from": "2026-10-01", "to": None, "law_version": "lei:ccp@2026-10-01", "package": "pacote:ccp@2026-10-01"}]})
R_LIM = rule("limiar-ajuste-direto-bens", "limiar", "Ajuste direto: bens e serviços de valor inferior a 20 000 EUR (art. 20.º n.º 1 a))", "norma:ccp", "PT", ["proc"],
    [{"field": "tipo_procedimento", "op": "eq", "value": "ajuste_direto"}, {"field": "tipo_contrato", "op": "in", "value": ["bens", "servicos"]}], [],
    [cite("ccp:art20.1.a", "De valor inferior a 20 000 EUR"), cite("ccp:art20.1", "A escolha do ajuste direto permite a celebração de contratos")],
    {"threshold": {"field": "preco_base", "comparator": "lt", "value": 20000, "currency": "EUR"}})
R_PRA = rule("prazo-minimo-propostas-6-dias", "prazo_minimo", "Prazo mínimo de seis dias para propostas (art. 136.º n.º 1)", "norma:ccp", "PT", ["proc"],
    [{"field": "publicado_joue", "op": "eq", "value": False}], [],
    [cite("ccp:art136.1", "O prazo mínimo para a apresentação das propostas é de seis dias")],
    {"minimum_days": 6, "deadline_field": "prazo_propostas_dias", "counted_from": "data_publicacao_anuncio"})
R_PROC = rule("procedimentos-admissiveis", "procedimento_admissivel", "Procedimentos para a formação de contratos (art. 16.º n.º 1)", "norma:ccp", "PT", ["proc"],
    [], [], [cite("ccp:art16.1", "adotam o concurso público, o concurso limitado por prévia qualificação, a consulta prévia ou o ajuste direto")],
    {"procedures": ["concurso_publico", "concurso_limitado_previa_qualificacao", "consulta_previa", "ajuste_direto"]})
R_CONT = rule("programa-indica-prazo-e-criterios", "conteudo_obrigatorio", "O programa do procedimento indica prazo e critérios (art. 131.º n.º 1)", "norma:ccp", "PT", ["proc"],
    [], [], [cite("ccp:art131.1", "indica o prazo para a apresentação das propostas e os critérios de adjudicação")],
    {"required_elements": ["prazo_apresentacao_propostas", "criterios_adjudicacao"], "document_piece": "programa_procedimento"})
R_PROI = rule("proibicao-fracionamento", "proibicao", "Proibição de fracionamento da despesa (art. 48.º n.º 1)", "norma:ccp", "PT", ["proc", "contrato"],
    [], [], [cite("ccp:art48.1", "É proibido o fracionamento da despesa")],
    {"forbidden": [{"field": "fracionamento_detetado", "op": "eq", "value": True}]}, second=False)
R_AGG = rule("limite-acumulado-art113", "agregada", "Limite acumulado por adjudicante e adjudicatário em três anos (art. 113.º n.º 2)", "norma:ccp", "PT", ["contrato"],
    [{"field": "tipo_procedimento", "op": "eq", "value": "ajuste_direto"}], [],
    [cite("ccp:art113.2", "no ano económico em curso e nos dois anos anteriores, propostas de valor acumulado igual ou superior ao limiar")],
    {"window": {"length": 3, "unit": "anos", "anchor": "data_adjudicacao"}, "group_key": ["adjudicante", "adjudicatario"],
     "aggregate": {"field": "preco_contratual", "op": "sum", "comparator": "lt", "value": 20000},
     "completeness_threshold": {"ratio": 0.9, "measured_over": "mes", "decided_by": E_PR_OK}})
R_JUR = rule("coeficiente-acores", "jurisdicao", "Coeficiente regional dos Açores sobre os limiares (DLR 27/2015/A art. 3.º)", "norma:dlr-27-2015-a", "PT-AC", ["proc"],
    [], [], [cite("dlr-27-2015-a:art3.1", "aplicam-se na Região com o coeficiente de 1,45")],
    {"territory": "PT-AC", "predicate": [{"field": "territorio", "op": "eq", "value": "PT-AC"}], "effect": {"multiply_thresholds_by": 1.45}})

# entity link by name (AMALIA), assertion conversion, dispute + adjudication
E_LINK = event("extrator:a", "propose", "link", "link:fx-2", payload={"from": "alias:base-dump:FX-2026-000001-adjudicatario", "to": "ent:cand:PT:fornecedor-fixture-unipessoal", "score": 0.82})
E_CONV = event("extrator:a", "propose", "afirmacao_conversao", "afirmacao:proc-base-FX-2026-000001:regime", payload={"passages": ["ccp:art20.1.a"]})
VER_LIM = "veredicto:regra-ccp-limiar-ajuste-direto-bens@v1:proc-base-FX-2026-000001:2026-10-24T19:30:00Z"
E_DISP = event("pessoa:paulo", "dispute", "veredicto", VER_LIM, payload={"disputa": "disputa:fx-1"}, reason="The two sources disagree on preco_base; check whether the dump value is a typo before the conflict stands.")
E_ADJ = event("pessoa:revisor-fixture", "adjudicate", "disputa", "disputa:fx-1", reason="Both values are as captured; the conflict is real, nao_avaliado stands.", outcome="upheld", expected_revision=1)

(V / "governance/events.jsonl").write_text("".join(canonical(e) + "\n" for e in EVENTS), encoding="utf-8")
LOG_HEAD = sha256_text(canonical(EVENTS[-1]))

# ---- packages and diff -----------------------------------------------------------------------------------------
def pacote(id_, law_version, rule_ids):
    rules = sorted([{"id": r, "revision": 1} for r in rule_ids], key=lambda x: x["id"])
    return write("pacote", id_.split(":")[1].replace("@", "-"), env({"id": id_, "law_version": law_version, "rules": rules, "hash": content_hash(rules), "log_head": LOG_HEAD, "built_at": REC}))
PK_OLD = pacote("pacote:ccp@2026-09-30", "lei:ccp@2026-09-30", [R_PRA, R_PROC, R_CONT, R_JUR])
PK_NEW = pacote("pacote:ccp@2026-10-01", "lei:ccp@2026-10-01", [R_SEL, R_LIM, R_PRA, R_PROC, R_CONT, R_AGG, R_JUR])
def rule_fields(r):
    f = {c["field"] for c in r["conditions"]}
    p = r["params"]
    for k in ("threshold", "aggregate"):
        if k in p: f.add(p[k]["field"])
    for k in ("deadline_field", "counted_from", "selects_by"):
        if k in p: f.add(p[k])
    if "window" in p: f.add(p["window"]["anchor"])
    for k in ("forbidden", "predicate"):
        for c in p.get(k, []): f.add(c["field"])
    f.update(p.get("group_key", []))
    return f
old = {r["id"]: r["revision"] for r in PK_OLD["rules"]}; new = {r["id"]: r["revision"] for r in PK_NEW["rules"]}
by_rule = []
for rid in sorted(set(old) | set(new)):
    if rid in old and rid not in new: by_rule.append({"rule": rid, "change": "removed", "fields": []})
    elif rid in new and rid not in old: by_rule.append({"rule": rid, "change": "added", "fields": []})
    elif old[rid] != new[rid]: by_rule.append({"rule": rid, "change": "changed", "fields": []})
BYR = {r["id"]: r for r in RULES}
touched = {}
for ch in by_rule:
    for f in rule_fields(BYR[ch["rule"]]): touched.setdefault(f, set()).add(ch["rule"])
by_field = [{"field": f, "rules": sorted(rs)} for f, rs in sorted(touched.items())]
write("diff", "ccp-2026-09-30..2026-10-01", env({"id": f"diff:{PK_OLD['id']}..{PK_NEW['id']}", "from": PK_OLD["id"], "to": PK_NEW["id"], "by_rule": by_rule, "by_consumer_field": by_field}))

# ---- adapter, units, entities, aliases, links ------------------------------------------------------------------
AD = write("adaptador", "base-dump-1", env({"id": "adaptador:base-dump@1", "source": "base-dump", "version": 1, "code": "adapters/base-dump/", "mapping": [
    {"source_field": "nAnuncio", "canonical_field": "n_anuncio", "transform": "identity"},
    {"source_field": "tipoContrato", "canonical_field": "tipo_contrato", "transform": "enum_map", "enum_map": {"Aquisição de bens móveis": "bens", "Aquisição de serviços": "servicos", "Empreitadas de obras públicas": "obras"}},
    {"source_field": "precoBase", "canonical_field": "preco_base", "transform": "number_pt"},
    {"source_field": "prazoPropostas", "canonical_field": "prazo_propostas_dias", "transform": "integer"},
    {"source_field": "dataPublicacao", "canonical_field": "data_publicacao_anuncio", "transform": "date_pt"},
    {"source_field": "dataPublicacao", "canonical_field": "data_inicio_procedimento", "transform": "date_pt", "note": "start of procedure taken as the notice date until a better field exists"},
    {"source_field": "tipoProcedimento", "canonical_field": "tipo_procedimento", "transform": "enum_map", "enum_map": {"Ajuste direto": "ajuste_direto", "Consulta prévia": "consulta_previa", "Concurso público": "concurso_publico"}},
    {"source_field": "publicadoJOUE", "canonical_field": "publicado_joue", "transform": "boolean"},
    {"source_field": "nifEntidadeAdjudicante", "canonical_field": "adjudicante", "transform": "nif"}],
    "coverage": [{"period": "2026-09", "expected": 1000, "captured": 1000}, {"period": "2026-10", "expected": 1000, "captured": 400}],
    "proposed_by": "extrator:a", "state": "proposed"}))
AD_API = write("adaptador", "base-api-1", env({"id": "adaptador:base-api@1", "source": "base-api", "version": 1, "code": "adapters/base-api/", "mapping": [
    {"source_field": "precoBase", "canonical_field": "preco_base", "transform": "identity"}, {"source_field": "adjudicatario.nif", "canonical_field": "adjudicatario", "transform": "nif"}],
    "coverage": [{"period": "2026-10", "expected": None, "captured": 1}], "proposed_by": "extrator:a", "state": "proposed"}))

PROC = "proc:base:FX-2026-000001"; CONTR = "contrato:base:99000001"
write("unidade", "proc-base-FX-2026-000001", env({"id": PROC, "kind": "proc", "parent": None, "raw": [RAW_DUMP], "consumer_ids": {"n_anuncio": "FX-2026-000001"}}))
write("unidade", "contrato-base-99000001", env({"id": CONTR, "kind": "contrato", "parent": PROC, "raw": [RAW_API], "consumer_ids": {"base_id": "99000001"}}))
write("entidade", "nif-500000000", env({"id": "ent:nif:500000000", "type": "publica", "country": "PT", "nif": "500000000", "name": "Município Fixture", "roles": [{"unit": PROC, "role": "adjudicante"}], "raw": [RAW_DUMP]}))
write("entidade", "nif-200000000", env({"id": "ent:nif:200000000", "type": "pessoa_singular", "country": "PT", "nif": "200000000", "name": "Fornecedor Fixture Unipessoal", "roles": [{"unit": CONTR, "role": "adjudicatario"}], "raw": [RAW_API]}))
write("entidade", "cand-PT-fornecedor-fixture-unipessoal", env({"id": "ent:cand:PT:fornecedor-fixture-unipessoal", "type": "privada", "country": "PT", "nif": None, "roles": [], "raw": [RAW_DUMP]}))
write("alias", "base-dump-FX-2026-000001-adjudicante", env({"id": "alias:base-dump:FX-2026-000001-adjudicante", "raw": RAW_DUMP, "field": "entidadeAdjudicante", "name_as_appears": "Município Fixture", "link": "link:fx-1"}))
write("alias", "base-dump-FX-2026-000001-adjudicatario", env({"id": "alias:base-dump:FX-2026-000001-adjudicatario", "raw": RAW_API, "field": "adjudicatario.nome", "name_as_appears": "Fornecedor Fixture Unipessoal", "link": "link:fx-2"}))
write("link", "fx-1", env({"id": "link:fx-1", "from": "alias:base-dump:FX-2026-000001-adjudicante", "to": "ent:nif:500000000", "proponent": "ferramenta:ccp-link@1", "method": "nif_exact",
    "evidence": {"source_field": "nifEntidadeAdjudicante", "value": "500000000"}, "state": "settled", "at": CAP_DUMP, "evento": None}))
write("link", "fx-2", env({"id": "link:fx-2", "from": "alias:base-dump:FX-2026-000001-adjudicatario", "to": "ent:cand:PT:fornecedor-fixture-unipessoal", "proponent": "extrator:a", "method": "name_ai",
    "evidence": {"source_field": "adjudicatario.nome", "value": "Fornecedor Fixture Unipessoal", "score": 0.82, "note": "name match; the NIF in the API record was not read by the proposer (blind)"}, "state": "proposed", "at": EVENTS[int(E_LINK.split(':')[1]) - 1]["at"], "evento": E_LINK}))

# ---- facts, assertion, conflict, document ----------------------------------------------------------------------
FACTS = {}
def fact(field, value, raw_id, sfield, adapter, known, unit=PROC, valid="2026-10-03"):
    fid = f"facto:{unit.replace(':', '-')}:{field}:{raw_id.split(':')[1]}"
    FACTS[fid] = write("facto", fid.split(":", 1)[1].replace(":", "-"), env({"id": fid, "unit": unit, "field": field, "value": value, "origin": {"raw": raw_id, "field": sfield}, "adapter": adapter, "valid_at": valid, "known_at": known}))
    return fid
F_TIPO = fact("tipo_contrato", "bens", RAW_DUMP, "tipoContrato", AD["id"], CAP_DUMP)
F_PRECO = fact("preco_base", 15000, RAW_DUMP, "precoBase", AD["id"], CAP_DUMP)
F_PRECO2 = fact("preco_base", 18000, RAW_API, "precoBase", AD_API["id"], CAP_API)
F_PRAZO = fact("prazo_propostas_dias", 9, RAW_DUMP, "prazoPropostas", AD["id"], CAP_DUMP)
F_PUB = fact("data_publicacao_anuncio", "2026-10-03", RAW_DUMP, "dataPublicacao", AD["id"], CAP_DUMP)
F_INI = fact("data_inicio_procedimento", "2026-10-03", RAW_DUMP, "dataPublicacao", AD["id"], CAP_DUMP)
F_TP = fact("tipo_procedimento", "ajuste_direto", RAW_DUMP, "tipoProcedimento", AD["id"], CAP_DUMP)
F_JOUE = fact("publicado_joue", False, RAW_DUMP, "publicadoJOUE", AD["id"], CAP_DUMP)
F_ADJ = fact("adjudicante", "500000000", RAW_DUMP, "nifEntidadeAdjudicante", AD["id"], CAP_DUMP)
AF = write("afirmacao", "proc-base-FX-2026-000001-regime", env({"id": "afirmacao:proc-base-FX-2026-000001:regime", "unit": PROC, "kind": "regime", "declared_text": DUMP["regime"],
    "passages": ["ccp:art20.1.a"], "converted_by": "extrator:a", "conversion_evento": E_CONV, "origin": {"raw": RAW_DUMP, "field": "regime"}, "known_at": CAP_DUMP}))
write("conflito", "proc-base-FX-2026-000001-preco_base", env({"id": "conflito:proc-base-FX-2026-000001:preco_base", "unit": PROC, "field": "preco_base",
    "values": [{"facto": F_PRECO, "value": 15000, "source": "base-dump", "known_at": CAP_DUMP}, {"facto": F_PRECO2, "value": 18000, "source": "base-api", "known_at": CAP_API}], "resolution": {"kind": "nao_avaliado"}}))
write("documento", SHA_DOC[:16], env({"id": f"doc:{SHA_DOC}", "sha256": SHA_DOC, "raw": RAW_DOC, "pages": 12, "has_text_layer": False, "origin": {"unit": PROC, "piece": "programa_procedimento", "url": "https://www.acingov.pt/acingovprod/2/index.php/fixture/programa.pdf"}}))

# ---- manifest and verdicts -------------------------------------------------------------------------------------
MANIFEST = {"law_version": "lei:ccp@2026-10-01", "package": PK_NEW["id"], "adapters": [AD["id"], AD_API["id"]],
    "source_snapshots": [{"source": "dr-consolidado", "sha256": SHA_LAW, "captured_at": CAP_LAW}, {"source": "base-dump", "sha256": SHA_DUMP, "captured_at": CAP_DUMP}, {"source": "base-api", "sha256": SHA_API, "captured_at": CAP_API}],
    "code": {"repository": "github.com/paulovillalobos/ccp-engine", "commit": "6b49816", "engine_version": "ccp-engine-0.1"}, "log_head": LOG_HEAD, "produced_at": "2026-10-24T19:30:00Z"}
MANIFEST["adapters"].sort(); MANIFEST["source_snapshots"].sort(key=lambda s: s["source"])
write("manifesto", "exemplo", MANIFEST)
KNOWN_V = "2026-10-24T19:30:00Z"
ENTS = [{"id": "ent:nif:500000000", "type": "publica", "role": "adjudicante", "name": "Município Fixture"}, {"id": "ent:nif:200000000", "type": "pessoa_singular", "role": "adjudicatario"}]
def verdict(rule_id, result, reason, citation, facts, detail, unit=PROC):
    vid = f"veredicto:{rule_id.replace(':', '-')}:{unit.replace(':', '-')}:{KNOWN_V}"
    return write("veredicto", f"{rule_id.split(':')[2].split('@')[0]}-{unit.split(':')[2]}", env({"id": vid, "rule": {"id": rule_id, "revision": 1}, "unit": unit, "result": result, "reason": reason, "detail": detail,
        "citation": citation, "facts_used": facts, "assertions_compared": [{"afirmacao": AF["id"], "declared_passages": ["ccp:art20.1.a"], "agrees": None if result == "nao_avaliado" else True}] if rule_id == R_LIM else [],
        "entities": ENTS, "valid_at": "2026-10-03", "known_at": KNOWN_V, "engine_version": "ccp-engine-0.1", "manifest": MANIFEST}))
assert VER_LIM == f"veredicto:{R_LIM.replace(':', '-')}:{PROC.replace(':', '-')}:{KNOWN_V}", (VER_LIM)
V_PRA = verdict(R_PRA, "cumpre", None, cite("ccp:art136.1", "O prazo mínimo para a apresentação das propostas é de seis dias"), [F_PRAZO, F_JOUE], "prazo_propostas_dias=9 >= 6")
V_LIM = verdict(R_LIM, "nao_avaliado", "conflito", None, [F_TP, F_TIPO], "preco_base in conflict: 15000 (base-dump) vs 18000 (base-api); no precedence rule")
V_AGG = verdict(R_AGG, "nao_avaliado", "cobertura_insuficiente", None, [F_TP], "base-dump coverage 2026-10 = 0.40 < 0.90 (product_rule:completude-agregadas)", unit=CONTR)

write("disputa", "fx-1", env({"id": "disputa:fx-1", "veredicto": V_LIM["id"], "raised_by": "pessoa:paulo", "reason": EVENTS[int(E_DISP.split(':')[1]) - 1]["reason"], "at": EVENTS[int(E_DISP.split(':')[1]) - 1]["at"], "evento": E_DISP,
    "state": "adjudicated", "adjudication": {"by": "pessoa:revisor-fixture", "at": EVENTS[int(E_ADJ.split(':')[1]) - 1]["at"], "outcome": "upheld", "reason": EVENTS[int(E_ADJ.split(':')[1]) - 1]["reason"], "evento": E_ADJ}, "regression_class": "conflito-preco-base-entre-fontes"}))
write("caso_referencia", "fx-1", env({"id": "ref:fx-1", "unit": PROC, "expected": [{"rule": R_PRA, "result": "cumpre", "reason": None}, {"rule": R_LIM, "result": "nao_avaliado", "reason": "conflito"}],
    "annotators": [{"principal": "pessoa:paulo", "at": "2026-10-24T19:40:00Z", "agrees_with_expected": True}, {"principal": "pessoa:revisor-fixture", "at": "2026-10-24T19:41:00Z", "agrees_with_expected": True}],
    "adjudication": None, "held_out": False, "frozen_at": None}))

# ---- phase 4 (T1): the training data the generator writes from this fixture law (verify TRAIN re-derives it) ---------
sys.path.insert(0, str(ROOT / "tools"))
import make_training as _mt  # noqa: E402
from engine.store import Store as _Store  # noqa: E402
_st = _Store([V]).load()
_held = _mt.held_out_doc(_st, REC, readings=V / "governance" / "readings")
(V / "training").mkdir(parents=True, exist_ok=True)
(V / "training" / "TRAIN-HELD-OUT.json").write_text(json.dumps(_held, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
_mt.write(_mt.generate(_st, _held, V / "governance" / "readings"), V / "training" / "data")

# ---- broken overlays: one per invariant ------------------------------------------------------------------------
def overlay(name, expect, files):
    d = B / name; d.mkdir(parents=True)
    (d / "EXPECT").write_text(expect + "\n")
    for rel, content in files.items():
        p = d / rel; p.parent.mkdir(parents=True, exist_ok=True)
        if isinstance(content, (dict, list)):
            p.write_text(json.dumps(content, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        else:
            p.write_text(content, encoding="utf-8")
def load(rel): return json.loads((V / rel).read_text(encoding="utf-8"))
def mutate(rel, fn):
    o = load(rel); fn(o); return o

o = mutate("raw/dr-consolidado-lei-ccp-fixture.json", lambda o: o.update(sha256="f" * 64))
overlay("i01-source-hash-mismatch", "I01", {"raw/dr-consolidado-lei-ccp-fixture.json": o})
def bad_quote(o): o["passages"][0]["quote"] = "De valor inferior a 30 000 EUR"
overlay("i02-quote-not-in-passage", "I02", {"regra/ccp-limiar-ajuste-direto-bens.json": mutate("regra/ccp-limiar-ajuste-direto-bens.json", bad_quote)})
overlay("i03-model-call-in-engine", "I03", {"engine_mutation/calls_model.py": '"""A module that would call a model from inside the engine. verify must refuse it."""\nimport openai  # noqa: F401\n\n\ndef read(text):\n    return openai.chat(text)\n'})
bad_events = list(EVENTS)
ev = {"id": f"evento:{len(bad_events)+1}", "seq": len(bad_events) + 1, "at": "2026-10-24T19:59:00Z", "prev": sha256_text(canonical(bad_events[-1])), "principal": "leitor:b", "action": "approve",
      "assertion_type": "product_rule", "assertion": "product_rule:completude-agregadas", "expected_revision": 1, "payload": {}, "reason": "an AI approving: must be refused", "question": None, "independence": None, "verdict": None, "outcome": None}
bad_events.append(ev)
overlay("i04-machine-approval", "I04", {"governance/events.jsonl": "".join(canonical(e) + "\n" for e in bad_events)})
def same_family(o): o["readings"][1]["family"] = "A"; o["readings"][1]["principal"] = "leitor:a"
overlay("i05-settled-by-one-family", "I05", {"regra/ccp-limiar-ajuste-direto-bens.json": mutate("regra/ccp-limiar-ajuste-direto-bens.json", same_family)})
def no_adapters(o): o["manifest"] = dict(o["manifest"], adapters=[])
overlay("i06-manifest-incomplete", "I06", {"veredicto/prazo-minimo-propostas-6-dias-FX-2026-000001.json": mutate("veredicto/prazo-minimo-propostas-6-dias-FX-2026-000001.json", no_adapters)})
def assertion_as_fact(o): o["facts_used"] = [AF["id"]] + o["facts_used"]
overlay("i07-assertion-used-as-fact", "I07", {"veredicto/limiar-ajuste-direto-bens-FX-2026-000001.json": mutate("veredicto/limiar-ajuste-direto-bens-FX-2026-000001.json", assertion_as_fact)})
def known_before(o): o["known_at"] = "2026-10-24T18:00:00Z"
overlay("i08-verdict-before-its-facts", "I08", {"veredicto/prazo-minimo-propostas-6-dias-FX-2026-000001.json": mutate("veredicto/prazo-minimo-propostas-6-dias-FX-2026-000001.json", known_before)})
def retitle(o): o["title"] = "Overwritten in place: same id, same revision, other content"
overlay("i09-overwrite-same-revision", "I09", {"regra/ccp-limiar-ajuste-direto-bens-copy.json": mutate("regra/ccp-limiar-ajuste-direto-bens.json", retitle)})
def post(o): o["request"]["method"] = "POST"
overlay("i10-active-send", "I10", {"raw/base-dump-anuncio-FX-2026-000001.json": mutate("raw/base-dump-anuncio-FX-2026-000001.json", post)})
def named(o): o["entities"][1]["name"] = "Fornecedor Fixture Unipessoal"
overlay("i11-natural-person-named", "I11", {"veredicto/prazo-minimo-propostas-6-dias-FX-2026-000001.json": mutate("veredicto/prazo-minimo-propostas-6-dias-FX-2026-000001.json", named)})
def no_product_rule(o): o["params"]["completeness_threshold"]["decided_by"] = "evento:2"  # a leitor's regra proposal, not a product rule
overlay("i12-threshold-without-product-rule", "I12", {"regra/ccp-limite-acumulado-art113.json": mutate("regra/ccp-limite-acumulado-art113.json", no_product_rule)})
# ---- broken overlays for the cross-object checks of A3b: one per new check ----------------------------------------
PRAZO_V = "veredicto/prazo-minimo-propostas-6-dias-FX-2026-000001.json"
PRAZO_F = "facto/proc-base-FX-2026-000001-prazo_propostas_dias-base-dump.json"
def three_days(o): o["value"] = 3
overlay("red-cumpre-contradicted-by-its-fact", "RED", {PRAZO_F: mutate(PRAZO_F, three_days)})
def foreign_head(o): o["manifest"] = dict(o["manifest"], log_head="a" * 64)
overlay("man-log-head-never-in-the-log", "MAN", {PRAZO_V: mutate(PRAZO_V, foreign_head)})
def settled_by_ai(o): o["state"] = "settled"
overlay("state-link-settled-without-approval", "STATE", {"link/fx-2.json": mutate("link/fx-2.json", settled_by_ai)})
def overlapping(o): o["versions"].append(dict(o["versions"][0], version="2026-09-01", valid_from="2026-09-01"))
overlay("time-passage-versions-overlap", "TIME", {"passagem/ccp-art20.1.a.json": mutate("passagem/ccp-art20.1.a.json", overlapping)})
def cycle(o): o.update(kind="lote", parent=CONTR)
overlay("graph-unit-parent-cycle", "GRAPH", {"unidade/proc-base-FX-2026-000001.json": mutate("unidade/proc-base-FX-2026-000001.json", cycle)})
def unmapped(o): o["field"] = "prazo_inventado"
overlay("field-fact-not-in-adapter-mapping", "FIELD", {PRAZO_F: mutate(PRAZO_F, unmapped)})
def unfrozen(o): o["held_out"] = True
overlay("bench-held-out-not-frozen", "BENCH", {"caso_referencia/fx-1.json": mutate("caso_referencia/fx-1.json", unfrozen)})
overlay("i01-orphan-raw-bytes", "I01", {f"raw_bytes/{'b' * 64}": "orphan bytes no raw record names\n"})
def relabelled(o): o["entities"][1].update(type="privada", name="Fornecedor Fixture Unipessoal")
overlay("i11-entity-type-from-record", "I11", {PRAZO_V: mutate(PRAZO_V, relabelled)})
# audit of phase 1 (the independent review, 2026-10-24): five more
def drop_entity(o): o["entities"] = o["entities"][:1]
overlay("red-entity-omitted", "RED", {PRAZO_V: mutate(PRAZO_V, drop_entity)})
def revoked(o): o["versions"][0]["revoked"] = True
overlay("time-cited-version-revoked", "TIME", {"passagem/ccp-art136.1.json": mutate("passagem/ccp-art136.1.json", revoked)})
def with_gap(o):
    v0 = dict(o["versions"][0]); v0.update(version="2020-01-01", valid_from="2020-01-01", valid_to="2024-01-01"); o["versions"].insert(0, v0)
overlay("time-gap-between-versions", "TIME", {"passagem/ccp-art136.1.json": mutate("passagem/ccp-art136.1.json", with_gap)})
stale_ent = load("entidade/nif-500000000.json"); stale_ent.update(revision=2, supersedes=1, stale=True, stale_reason="fixture: duplicate record", recorded_at="2026-10-24T21:00:00Z")
overlay("state-link-to-stale-entity", "STATE", {"entidade/nif-500000000-r2.json": stale_ent})
def knew_too_early(o): o.update(known_at="2026-10-24T19:05:00Z", recorded_at="2026-10-24T19:05:00Z", id=o["id"].replace(KNOWN_V, "2026-10-24T19:05:00Z"))
overlay("man-verdict-before-log-head", "MAN", {PRAZO_V: mutate(PRAZO_V, knew_too_early)})
# phase 4 (T1): the training data must be the generator's output and keep reserved articles out of train
_idx = json.loads((V / "training/data/INDEX.json").read_text(encoding="utf-8")); _idx["tasks"]["nota_dr"]["train"] += 1
overlay("train-index-not-regenerated", "TRAIN", {"training/data/INDEX.json": json.dumps(_idx, ensure_ascii=False, sort_keys=True, indent=1) + "\n"})
_reserved = sorted(_held["reserved_articles"])[0]
_leak = json.dumps({"answer": json.dumps({"passagem": _reserved}), "id": "escolha_passagem:fixture-leak", "prompt": "FIXTURE", "schema": {}, "sources": [_reserved], "task": "escolha_passagem"}, ensure_ascii=False, sort_keys=True) + "\n"
overlay("train-example-touches-reserved-article", "TRAIN", {"training/data/escolha_passagem/train.jsonl": (V / "training/data/escolha_passagem/train.jsonl").read_text(encoding="utf-8") + _leak})
_edited = dict(_held, reserved_articles=_held["reserved_articles"][1:])
overlay("train-reservation-edited", "TRAIN", {"training/TRAIN-HELD-OUT.json": json.dumps(_edited, ensure_ascii=False, indent=1) + "\n"})
# D43: a rule revision above the log's may carry a review's new state, never new content
_above = load("regra/ccp-limiar-ajuste-direto-bens.json"); _above.update(revision=2, supersedes=1, title="Ajuste direto: outra redação", recorded_at="2026-10-24T21:00:00Z")
overlay("state-rule-above-log-changes-content", "STATE", {"regra/ccp-limiar-ajuste-direto-bens.r2.json": _above})
print("valid objects:", sum(1 for p in V.rglob("*.json")), "events:", len(EVENTS), "broken overlays:", len(list(B.iterdir())))
