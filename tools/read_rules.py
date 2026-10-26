"""The reading protocol of B3: two readers of different families read the same passages and answer the same typed
question; the code turns the first reading into a rule, the second reviews it blind, and the log decides the state.

    .venv/bin/python tools/read_rules.py prompts            writes governance/readings/<rule>/prompt.json (question,
                                                             candidate passages with their text, answer schema)
    (the readers answer the prompt files from readers/, D38: leitor:a on Modal, readers/leitor_a_modal.py; leitor:b by
     its command-line client, readers/leitor_b_cli.py, read-only, ephemeral, in an empty directory)
    .venv/bin/python tools/read_rules.py record             log, rules, packages, diff, DESACORDOS.md, RESUMO.md

A reader answers JSON only: the passage ids it chooses among the candidates, the rule type, conditions and params as
data of the regra schema. It never writes a quote: the rule's citations are written here with engine.passages.cite
(the whole text of each chosen passage version). Each raw answer is kept as
governance/readings/<rule>/<leitor>.json {"at", "sha256" of the answer text, "answer"} and the log events carry that
sha256. Flow (DECISIONS D37): Log.propose by leitor:a with its reading; the rule is built from it; Log.review by
leitor:b, independence blind, verdict uphold when B chose the same passages, conditions and params, else
request_evidence with B's reading in the payload (the rule stays proposed; its passages are then the union of both
readings, so each reading names only passages the rule cites); a pessoa never approves a reading of the law.
Packages hold the settled rules valid on their date; rules/ is the replay of the log. Nothing here calls a model:
the readers' answers are files.
"""
import argparse
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from engine import passages as passages_mod  # noqa: E402
from engine import rules as rules_mod  # noqa: E402
from engine import schema  # noqa: E402
from engine.canon import canonical  # noqa: E402
from engine.governance import Log  # noqa: E402
from engine.sources import now_utc  # noqa: E402
from engine.store import Store, Writer  # noqa: E402

VERSION = "ccp-read-rules-0.1"
READINGS = ROOT / "governance/readings"
# D44: round 2 of B3 for the rules the engine needs first (the person's order, 2026-10-26), with the round-1 prompt defects fixed
ROUND2 = ["regra:dl-177-2026:seletor-regime@v1", "regra:ccp:prazo-minimo-concurso-joue@v1",
          "regra:ccp:prazo-minimo-concurso-sem-joue-bens-servicos@v1", "regra:ccp:prazo-minimo-concurso-sem-joue-obras@v1"]
RONDA2 = READINGS / "ronda2"
# D45: round 3, the same rules, proposed by leitor:a2 (the person's decision) with conditions typed by field
ROUNDS = {2: {"dir": RONDA2, "proposer": "leitor:a", "file": "leitor-a.json", "decision": "D44"},
          3: {"dir": READINGS / "ronda3", "proposer": "leitor:a2", "file": "leitor-a2.json", "decision": "D45"},
          4: {"dir": READINGS / "ronda4", "proposer": "leitor:a3", "file": "leitor-a3.json", "decision": "D46"},
          5: {"dir": READINGS / "ronda5", "proposer": "leitor:a4", "file": "leitor-a4.json", "decision": "D47"}}
FIELDS = ["tipo_contrato", "tipo_procedimento", "publicado_joue", "territorio", "tipo_entidade", "preco_base", "data_inicio_procedimento"]
VOCAB = {
    "tipo_contrato": ["obras", "bens", "servicos", "concessao_obras", "concessao_servicos", "servicos_sociais"],
    "tipo_procedimento": ["ajuste_direto", "consulta_previa", "concurso_publico", "concurso_limitado_previa_qualificacao",
                          "procedimento_negociacao", "dialogo_concorrencial", "parceria_inovacao"],
    "publicado_joue": [True, False],
    "territorio": ["PT", "PT-AC", "PT-MA"],
    "tipo_entidade": ["estado", "outra"],
}
OPS = ["eq", "ne", "lt", "le", "gt", "ge", "in", "not_in"]
LAWS = ["lei:ccp@2026-09-30", "lei:ccp@2026-10-01"]
PACKAGES = ["pacote:ccp@2026-09-30", "pacote:ccp@2026-10-01"]
NEW, OLD = "2026-10-01", "2026-09-30"
DATE = "^[0-9]{4}-[0-9]{2}-[0-9]{2}$"  # answer schemas mirror the regra schema's constraints (a looser one let two readings fail it)


def art(prefix, n, parts):
    return [f"{prefix}:art{n}"] + [f"{prefix}:art{n}.{p}" for p in parts]


TARGETS = [
    {"rule": "regra:dl-177-2026:seletor-regime@v1", "type": "seletor_regime", "norma": "norma:dl-177-2026", "jurisdiction": "PT", "date": NEW,
     "title": "Regime aplicável consoante a data de início do procedimento (DL n.º 177/2026)",
     "candidates": art("dl-177-2026", 7, ["1", "2", "3"]) + art("dl-177-2026", 10, []) + art("dl-177-2026", 11, []),
     "question": "Que passagem fixa a que procedimentos se aplicam os valores atualizados do Código pelo presente decreto-lei, "
                 "e por que facto se escolhe o regime? Dê o campo que seleciona o regime e os regimes (de, até, versão da lei, pacote)."},
] + [
    {"rule": f"regra:ccp:limiar-{proc}-{kind}@v{v}", "type": "limiar", "norma": "norma:ccp", "jurisdiction": "PT", "date": date,
     "title": f"{label}: valor máximo para {what}",
     "candidates": cands,
     "question": f"Para a formação de {what} por {label.lower()}, qual é o valor (limiar) abaixo do qual esse procedimento pode ser "
                 "adotado? Dê as condições em que a regra se aplica (tipo de procedimento, tipo de contrato) e o limiar como campo, "
                 "comparação e valor em euros."}
    for proc, label in (("ajuste-direto", "Ajuste direto"), ("consulta-previa", "Consulta prévia"))
    for kind, what, cands in (("bens-servicos", "contratos de locação ou aquisição de bens móveis e de aquisição de serviços",
                                art("ccp", 20, ["1", "1.a", "1.b", "1.c", "1.d"])),
                               ("obras", "contratos de empreitada de obras públicas", art("ccp", 19, ["a", "b", "c", "d"])))
    for v, date in ((1, OLD), (2, NEW))
] + [
    {"rule": "regra:ccp:limiar-concurso-sem-joue-bens-servicos-estado@v1", "type": "limiar", "norma": "norma:ccp", "jurisdiction": "PT", "date": NEW,
     "title": "Concurso sem anúncio no JOUE: limiar europeu para bens e serviços adjudicados pelo Estado",
     "candidates": art("ccp", 20, ["1.a", "1.b"]) + ["ccp:art474.3", "ccp:art474.3.b", "ccp:art474.3.c"] + art("eu-2025-2152", 1, ["1", "1.a", "1.b", "1.c"]),
     "question": "Um concurso público ou limitado por prévia qualificação para locação ou aquisição de bens móveis ou aquisição de serviços, "
                 "adjudicado pelo Estado e sem anúncio no Jornal Oficial da União Europeia, só é admissível abaixo de que valor? "
                 "Escolha as passagens que fixam esse valor hoje e dê condições e limiar."},
    {"rule": "regra:ccp:limiar-concurso-sem-joue-obras@v1", "type": "limiar", "norma": "norma:ccp", "jurisdiction": "PT", "date": NEW,
     "title": "Concurso sem anúncio no JOUE: limiar europeu para empreitadas de obras públicas",
     "candidates": art("ccp", 19, ["a", "b"]) + ["ccp:art474.3", "ccp:art474.3.a"] + art("eu-2025-2152", 1, ["1", "1.a"]),
     "question": "Um concurso público ou limitado por prévia qualificação para empreitada de obras públicas, sem anúncio no Jornal Oficial "
                 "da União Europeia, só é admissível abaixo de que valor? Escolha as passagens que fixam esse valor hoje e dê condições e limiar."},
    {"rule": "regra:dlr-34-2008-m:coeficiente-madeira@v1", "type": "jurisdicao", "norma": "norma:dlr-34-2008-m", "jurisdiction": "PT-MA", "date": NEW,
     "title": "Região Autónoma da Madeira: coeficiente aplicado aos valores de escolha do procedimento",
     "candidates": art("dlr-34-2008-m", 4, ["1", "2", "3", "4"]),
     "question": "Que efeito tem o regime regional sobre os valores que determinam a escolha do procedimento no Código, para procedimentos "
                 "na Região Autónoma da Madeira? Dê o território, o predicado que identifica esses procedimentos e o efeito."},
    {"rule": "regra:dlr-27-2015-a:regime-acores@v1", "type": "jurisdicao", "norma": "norma:dlr-27-2015-a", "jurisdiction": "PT-AC", "date": NEW,
     "title": "Região Autónoma dos Açores: regime regional de contratação pública",
     "candidates": art("dlr-27-2015-a", 1, []) + art("dlr-27-2015-a", 16, []) + art("dlr-27-2015-a", 19, ["a"]) + art("dlr-27-2015-a", 20, ["a"]),
     "question": "Que efeito tem o regime regional dos Açores sobre os valores de escolha do procedimento do Código, para entidades "
                 "adjudicantes regionais? Dê o território, o predicado e o efeito (coeficiente ou norma que substitui)."},
] + [
    {"rule": f"regra:ccp:prazo-minimo-{slug}@v1", "type": "prazo_minimo", "norma": "norma:ccp", "jurisdiction": "PT", "date": NEW,
     "title": title, "candidates": cands, "question": q}
    for slug, title, cands, q in (
        ("concurso-sem-joue-bens-servicos", "Concurso público sem anúncio no JOUE: prazo mínimo das propostas (bens e serviços)",
         art("ccp", 135, ["1", "2"]) + art("ccp", 136, ["1"]),
         "Num concurso público cujo anúncio não é publicado no Jornal Oficial da União Europeia, para contrato que não é de empreitada, qual "
         "é o prazo mínimo para apresentação das propostas? Dê condições, dias, o campo do prazo e de onde se conta."),
        ("concurso-sem-joue-obras", "Concurso público sem anúncio no JOUE: prazo mínimo das propostas (empreitadas)",
         art("ccp", 135, ["1", "2"]) + art("ccp", 136, ["1"]),
         "Num concurso público cujo anúncio não é publicado no Jornal Oficial da União Europeia, para empreitada de obras públicas, qual é o "
         "prazo mínimo para apresentação das propostas? Dê condições, dias, o campo do prazo e de onde se conta."),
        ("concurso-joue", "Concurso público com anúncio no JOUE: prazo mínimo das propostas",
         art("ccp", 136, ["1", "2", "3"]) + art("ccp", 135, ["1"]),
         "Num concurso público cujo anúncio é publicado no Jornal Oficial da União Europeia, qual é o prazo mínimo geral para apresentação "
         "das propostas? Dê condições, dias, o campo do prazo e de onde se conta."))
] + [
    {"rule": f"regra:ccp:procedimentos-admissiveis@v{v}", "type": "procedimento_admissivel", "norma": "norma:ccp", "jurisdiction": "PT", "date": date,
     "title": "Tipos de procedimento para a formação de contratos submetidos à concorrência",
     "candidates": art("ccp", 16, ["1", "1.a", "1.b", "1.c", "1.d", "1.e", "1.f", "1.g", "2"]),
     "question": "Que tipos de procedimento podem as entidades adjudicantes adotar para formar contratos cujo objeto está submetido à "
                 "concorrência de mercado? Dê a lista de procedimentos e as condições."}
    for v, date in ((1, OLD), (2, NEW))
]


# ---- prompts ---------------------------------------------------------------------------------------------------
def slug(rule_id):
    return rule_id.split(":", 1)[1].replace(":", "--").replace("@", "-at-")


def version_at(p, date):
    return next((v for v in p["versions"] if v["valid_from"] <= date and (v["valid_to"] is None or date < v["valid_to"])), None)


def typed_condition():
    """D45: a condition whose value is typed by its field (round 3 on)."""
    def var(field, ops, value):
        return {"type": "object", "properties": {"field": {"type": "string", "enum": [field]}, "op": {"type": "string", "enum": ops}, "value": value},
                "required": ["field", "op", "value"], "additionalProperties": False}
    out = []
    for f in ("tipo_contrato", "tipo_procedimento", "territorio", "tipo_entidade"):
        out.append(var(f, ["eq", "ne"], {"type": "string", "enum": VOCAB[f]}))
        out.append(var(f, ["in", "not_in"], {"type": "array", "items": {"type": "string", "enum": VOCAB[f]}, "minItems": 1}))
    out.append(var("publicado_joue", ["eq", "ne"], {"type": "boolean"}))
    out.append(var("preco_base", ["eq", "ne", "lt", "le", "gt", "ge"], {"type": "number"}))
    out.append(var("data_inicio_procedimento", ["eq", "ne", "lt", "le", "gt", "ge"], {"type": "string", "pattern": DATE}))
    return {"anyOf": out}


def schema_for(t, rnd=1):
    array = {"type": "array", "items": {"type": "string"}, **({"minItems": 1} if rnd == 2 else {})}  # D44 (2): no empty list as a value
    value = {"anyOf": [{"type": "string"}, {"type": "number"}, {"type": "boolean"}, array]}
    cond = typed_condition() if rnd >= 3 else {"type": "object", "properties": {"field": {"type": "string", "enum": FIELDS}, "op": {"type": "string", "enum": OPS}, "value": value},
                                               "required": ["field", "op", "value"], "additionalProperties": False}
    params = {
        "limiar": {"threshold": {"type": "object", "properties": {"field": {"type": "string", "enum": ["preco_base"]}, "comparator": {"type": "string", "enum": ["lt", "le"]},
                                                                  "value": {"type": "number"}, "currency": {"type": "string", "enum": ["EUR"]}},
                                 "required": ["field", "comparator", "value", "currency"], "additionalProperties": False}},
        "prazo_minimo": {"minimum_days": {"type": "integer", "minimum": 1}, "deadline_field": {"type": "string", "enum": ["prazo_propostas_dias"]},
                         "counted_from": {"type": "string", "enum": ["data_publicacao_anuncio", "data_envio_anuncio"]}},
        "procedimento_admissivel": {"procedures": {"type": "array", "minItems": 1, "items": {"type": "string", "enum": VOCAB["tipo_procedimento"]}}},
        "seletor_regime": {"selects_by": {"type": "string", "enum": ["data_inicio_procedimento"]},
                           "regimes": {"type": "array", "minItems": 1, "items": {"type": "object", "properties": {
                               "from": {"type": "string", "pattern": DATE}, "to": {"anyOf": [{"type": "string", "pattern": DATE}, {"type": "null"}]},
                               "law_version": {"type": "string", "enum": LAWS},
                               "package": {"type": "string", "enum": PACKAGES}}, "required": ["from", "to", "law_version", "package"], "additionalProperties": False}}},
        "jurisdicao": {"territory": {"type": "string", "enum": ["PT-AC", "PT-MA"]}, "predicate": {"type": "array", "minItems": 1, "items": cond},
                       "effect": {"type": "object", "properties": {"multiply_thresholds_by": {"type": ["number", "null"]},
                                                                   "replace_norma": {"type": ["string", "null"], "enum": ["norma:dlr-27-2015-a", "norma:dlr-34-2008-m", None]}},
                                  "required": ["multiply_thresholds_by", "replace_norma"], "additionalProperties": False}},
    }[t["type"]]
    return {"type": "object", "properties": {
        "passagens": {"type": "array", "minItems": 1, "items": {"type": "string", "enum": t["candidates"]}},
        "tipo": {"type": "string", "enum": [t["type"]]},
        "condicoes": {"type": "array", "items": cond},
        "params": {"type": "object", "properties": params, "required": list(params), "additionalProperties": False}},
        "required": ["passagens", "tipo", "condicoes", "params"], "additionalProperties": False}


def prompt_text(store, t, rnd=1):
    date_fmt = "uma data no formato ISO (ano-mês-dia)" if rnd >= 2 else "data AAAA-MM-DD"  # D44 (1): round 1 named a literal leitor:a copied
    lines = ["És um leitor da lei portuguesa. Lê as passagens candidatas e responde à pergunta com um objeto JSON e nada mais.",
             "Regras: escolhe em «passagens» os ids das passagens que fundamentam a resposta (só ids da lista, nunca texto); "
             "«condicoes» são condições sobre factos do procedimento; usa só estes campos e valores:",
             "  " + "; ".join(f"{k}: {', '.join(json.dumps(v, ensure_ascii=False) for v in vals)}" for k, vals in VOCAB.items()) + f"; preco_base: número em euros; data_inicio_procedimento: {date_fmt}.",
             f"Data de referência: {t['date']}. Tipo de regra pedido: {t['type']}.", "", "Passagens candidatas:"]
    for pid in t["candidates"]:
        p = store.current(pid)
        v = version_at(p, t["date"])
        lines.append(f"[{pid}] (versão em vigor a {t['date']}, desde {v['valid_from']})")
        lines.append(v["text"])
        prev = [x for x in p["versions"] if x["valid_to"] == v["valid_from"]]
        if prev and prev[0]["text"] != v["text"]:
            lines.append(f"[{pid}] texto anterior (em vigor de {prev[0]['valid_from']} a {prev[0]['valid_to']}):")
            lines.append(prev[0]["text"])
        lines.append("")
    question = t["question"]
    if rnd >= 2 and t["type"] == "seletor_regime":  # D44 (3): how an open-ended regime is written
        question += " Um regime sem data final tem «to» = null."
    lines += ["Pergunta: " + question]
    return "\n".join(lines)


def cmd_prompts(store, only=None, rnd=1):
    for t in TARGETS:
        if only and only not in t["rule"]:
            continue
        if rnd >= 2 and t["rule"] not in ROUND2:
            continue
        for pid in t["candidates"]:
            p = store.current(pid)
            if p is None or version_at(p, t["date"]) is None:
                raise SystemExit(f"{t['rule']}: candidate {pid} has no version in force on {t['date']}")
        d = (ROUNDS[rnd]["dir"] if rnd >= 2 else READINGS) / slug(t["rule"])
        d.mkdir(parents=True, exist_ok=True)
        if rnd >= 2 and (d / "prompt.json").exists():
            continue  # a round's prompt is fixed once written: its answers are read against it
        text = prompt_text(store, t, rnd)
        body = {"rule": t["rule"], "type": t["type"], "date": t["date"], "candidates": t["candidates"], "prompt": text, "schema": schema_for(t, rnd)}
        if rnd >= 2:
            body["round"] = rnd
        (d / "prompt.json").write_text(json.dumps(body, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"{len(ROUND2) if rnd >= 2 else len(TARGETS)} prompts in {ROUNDS[rnd]['dir'] if rnd >= 2 else READINGS}")


def store_answer(path, text):
    path.write_text(json.dumps({"at": now_utc(), "sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(), "answer": text},
                               ensure_ascii=False, indent=1) + "\n", encoding="utf-8")


# ---- record ------------------------------------------------------------------------------------------------------
def parse_answer(rec, t):
    """The reader's JSON, or None when it is not JSON or names a passage outside the candidates."""
    try:
        a = json.loads(rec["answer"])
    except (json.JSONDecodeError, TypeError):
        return None
    if not isinstance(a, dict) or not a.get("passagens") or any(p not in t["candidates"] for p in a["passagens"]):
        return None
    params = dict(a.get("params") or {})
    if t["type"] == "jurisdicao" and isinstance(params.get("effect"), dict):
        params["effect"] = {k: v for k, v in params["effect"].items() if v is not None}
    if t["type"] == "procedimento_admissivel" and isinstance(params.get("procedures"), list):
        params["procedures"] = sorted(set(params["procedures"]))
    return {"passages": sorted(set(a["passagens"])), "type": a.get("tipo"), "conditions": norm_conditions(a.get("condicoes") or []), "params": params}


def norm_conditions(conds):
    out = []
    for c in conds:
        c = dict(c)
        if isinstance(c.get("value"), list):
            c["value"] = sorted(c["value"], key=str)
        out.append(c)
    return sorted(out, key=lambda c: canonical(c))


# ---- canonical form of a reading (product rule product_rule:forma-canonica-da-leitura, evento:43; DECISIONS D43) -----
CANON_RULE = "product_rule:forma-canonica-da-leitura"


def _num(x):
    return int(x) if isinstance(x, float) and x.is_integer() else x


def _cval(v):
    if isinstance(v, list):
        return [json.loads(i) for i in sorted({json.dumps(_num(x), ensure_ascii=False) for x in v})]
    return _num(v)


def _ccond(c):
    op, v = c.get("op"), _cval(c.get("value"))
    if op in ("in", "not_in"):
        items = v if isinstance(v, list) else [v]
        if len(items) == 1:
            return {"field": c.get("field"), "op": "eq" if op == "in" else "ne", "value": items[0]}
        return {"field": c.get("field"), "op": op, "value": items}
    if op in ("eq", "ne") and isinstance(v, list) and len(v) == 1:
        return {"field": c.get("field"), "op": op, "value": v[0]}
    return {"field": c.get("field"), "op": op, "value": v}


def _cparams(p):
    if isinstance(p, dict):
        return {k: (sorted({canonical(_ccond(c)) for c in v}) if k == "predicate" and isinstance(v, list) else _cparams(v))
                for k, v in p.items() if v is not None}
    if isinstance(p, list):
        items = [_cparams(x) for x in p]
        return sorted(items, key=canonical) if items and all(isinstance(x, (dict, list)) for x in items) else sorted(items, key=str)
    return _num(p)


def canonical_reading(r):
    """What a reading says, not how it is written: passages and conditions as sets, a one-value «in» is «eq», integral
    numbers as integers, params' lists of objects as sets, null fields dropped. Two readings replicate each other when
    their canonical forms are equal (the person's product rule, evento:43)."""
    return {"passages": sorted(set(r["passages"])), "type": r.get("type"),
            "conditions": sorted({canonical(_ccond(c)) for c in r["conditions"]}), "params": _cparams(r["params"])}


def same_reading(a, b):
    return a is not None and b is not None and canonical_reading(a) == canonical_reading(b)


def key_param(r):
    """The number or list a reading turns on (agreement 'of direction', RESUMO.md)."""
    p, t = r["params"], r["type"]
    return {"limiar": lambda: (p.get("threshold") or {}).get("value"), "prazo_minimo": lambda: p.get("minimum_days"),
            "procedimento_admissivel": lambda: tuple(p.get("procedures") or []),
            "seletor_regime": lambda: tuple(sorted((x.get("from"), x.get("law_version")) for x in p.get("regimes") or [])),
            "jurisdicao": lambda: canonical(p.get("effect") or {})}[t]()


def build_rule(store, t, a, passages, readings, state, revision=1):
    cits, froms, tos = [], [], []
    for pid in passages:
        v = version_at(store.current(pid), t["date"])
        cits.append(passages_mod.cite(store, pid, v["version"], 0, len(v["text"])))  # the code writes the quote
        froms.append(v["valid_from"])
        if v["valid_to"]:
            tos.append(v["valid_to"])
    return {"id": t["rule"], "revision": revision, "recorded_at": now_utc(), "type": t["type"], "title": t["title"], "norma": t["norma"],
            "jurisdiction": t["jurisdiction"], "applies_to": ["proc"], "conditions": a["conditions"], "exceptions": [],
            "valid_from": max(froms), "valid_to": min(tos) if tos else None, "passages": cits, "params": a["params"],
            "readings": readings, "state": state}


def cmd_record():
    store = Store([ROOT / "law", ROOT / "rules", ROOT / "governance"]).load()
    log = Log(ROOT / "governance")
    writer = Writer(ROOT / "rules", Store([ROOT / "rules"]).load())
    known = {aid for (atype, aid) in log.replay().assertions if atype == "regra"}
    summary, disagreements = [], []
    for t in TARGETS:
        d = READINGS / slug(t["rule"])
        ra, rb = [json.loads((d / f).read_text(encoding="utf-8")) if (d / f).exists() else None for f in ("leitor-a.json", "leitor-b.json")]
        a = parse_answer(ra, t) if ra else None
        b = parse_answer(rb, t) if rb else None
        row = {"rule": t["rule"], "type": t["type"], "a": a, "b": b, "state": None, "exact": None, "direction": None}
        summary.append(row)
        if a is None or a["type"] != t["type"]:
            row["state"] = "sem leitura válida de leitor:a"
            continue
        if b is not None:
            row["exact"] = same_reading(a, b)  # D43: replication is equality of canonical forms (evento:43)
            row["direction"] = key_param(a) == key_param(b)
        if t["rule"] in known:
            row["state"] = log.replay().state_of("regra", t["rule"])
            if b is not None and not row["exact"]:
                disagreements.append((t, a, b))
            elif b is not None and row["state"] == "proposed":
                # D43: the stored blind answer of leitor:b replicates leitor:a's under the person's canonical form (evento:43):
                # the same answer (same sha256) is recorded again as an uphold that names the product rule; nothing is re-asked
                question = json.loads((d / "prompt.json").read_text(encoding="utf-8"))["prompt"].split("Pergunta: ", 1)[1]
                canon_ev = next(ev["id"] for _, ev in log.events if ev["assertion"] == CANON_RULE)
                ev_b = log.review("leitor:b", "regra", t["rule"], 1, f"Blind, same prompt as leitor:a: {question}", "blind", "uphold", now_utc(),
                                  payload={"chosen_passages": b["passages"], "conditions": b["conditions"], "params": b["params"],
                                           "answer_sha256": rb["sha256"], "replication": CANON_RULE, "product_rule_event": canon_ev})
                rule = store.current(t["rule"])
                readings = [x for x in rule["readings"] if x["principal"] != "leitor:b"] + [
                    {"principal": "leitor:b", "family": "B", "at": rb["at"], "chosen_passages": b["passages"], "blind": True, "evento": ev_b}]
                row["state"] = log.replay().state_of("regra", t["rule"])
                writer.revise(rule, {"readings": readings, "state": row["state"]}, now_utc())
            continue
        # the rule leitor:a's reading would make must be a valid regra before anything enters the log
        draft = build_rule(store, t, a, a["passages"], [{"principal": "leitor:a", "family": "A", "at": ra["at"], "chosen_passages": a["passages"],
                                                         "blind": False, "evento": "evento:1"}], "proposed")
        problems = schema.validate("regra", draft)
        try:
            rules_mod.check(draft)
        except rules_mod.RuleError as exc:
            problems.append(str(exc))
        if problems:
            row["state"] = "sem leitura válida de leitor:a"
            row["why"] = str(problems[0])[:200]
            continue
        ev_a = log.propose("leitor:a", "regra", t["rule"], {"chosen_passages": a["passages"], "conditions": a["conditions"], "params": a["params"],
                                                           "answer_sha256": ra["sha256"]}, ra["at"])
        readings = [{"principal": "leitor:a", "family": "A", "at": ra["at"], "chosen_passages": a["passages"], "blind": False, "evento": ev_a}]
        passages = list(a["passages"])
        if b is not None:
            question = json.loads((d / "prompt.json").read_text(encoding="utf-8"))["prompt"].split("Pergunta: ", 1)[1]
            verdict = "uphold" if row["exact"] else "request_evidence"
            ev_b = log.review("leitor:b", "regra", t["rule"], 1, f"Blind, same prompt as leitor:a: {question}", "blind", verdict, rb["at"],
                              payload={"chosen_passages": b["passages"], "conditions": b["conditions"], "params": b["params"], "answer_sha256": rb["sha256"]})
            readings.append({"principal": "leitor:b", "family": "B", "at": rb["at"], "chosen_passages": b["passages"], "blind": True, "evento": ev_b})
            if not row["exact"]:
                disagreements.append((t, a, b))  # D39: the rule cites the proposer's passages only; B's reading stays in its review payload
        state = log.replay().state_of("regra", t["rule"])
        row["state"] = state
        writer.append(build_rule(store, t, a, passages, readings, state))
    later = {rnd: record_round(store, log, writer, rnd) for rnd in sorted(ROUNDS)}
    log.write_state()
    packs = write_packages(writer)
    write_reports(summary, disagreements, packs)
    for rnd, rows in later.items():
        write_round_report(rows, rnd)


def record_round(store, log, writer, rnd):
    """D44/D45: the round's proposer `correct`s the current revision from its answer (revision + 1), then leitor:b's blind
    review of that revision. Recorded once per answer (an answer whose sha256 is already in a correct event is not
    recorded again). Rounds are recorded in order, each on the revision the previous one left."""
    R = ROUNDS[rnd]
    rows = []
    content = ("conditions", "params", "passages", "valid_from", "valid_to", "readings", "state")
    for t in TARGETS:
        if t["rule"] not in ROUND2:
            continue
        d = R["dir"] / slug(t["rule"])
        ra, rb = [json.loads((d / f).read_text(encoding="utf-8")) if (d / f).exists() else None for f in (R["file"], "leitor-b.json")]
        if ra is None:
            continue
        a = parse_answer(ra, t)
        b = parse_answer(rb, t) if rb else None
        row = {"rule": t["rule"], "type": t["type"], "a": a, "b": b, "state": None, "exact": None, "direction": None}
        rows.append(row)
        if b is not None and a is not None:
            row["exact"] = same_reading(a, b)
            row["direction"] = key_param(a) == key_param(b)
        cur = log.replay().assertions.get(("regra", t["rule"]))
        if cur is None:
            row["state"] = "sem proposta da ronda 1"
            continue
        done = any(ev["action"] == "correct" and ev["assertion"] == t["rule"] and (ev.get("payload") or {}).get("answer_sha256") == ra["sha256"]
                   for _, ev in log.events)
        if done:
            row["state"] = log.replay().state_of("regra", t["rule"])
            continue
        if a is None or a["type"] != t["type"]:
            row["state"] = f"sem leitura válida de {R['proposer']}"
            continue
        draft = build_rule(store, t, a, a["passages"], [{"principal": R["proposer"], "family": "A", "at": ra["at"], "chosen_passages": a["passages"],
                                                         "blind": False, "evento": "evento:1"}], "proposed")
        problems = schema.validate("regra", draft)
        try:
            rules_mod.check(draft)
        except rules_mod.RuleError as exc:
            problems.append(str(exc))
        if problems:
            row["state"] = f"sem leitura válida de {R['proposer']}"
            row["why"] = str(problems[0])[:200]
            continue
        question = json.loads((d / "prompt.json").read_text(encoding="utf-8"))["prompt"].split("Pergunta: ", 1)[1]
        ev_a = log.correct(R["proposer"], "regra", t["rule"], cur["revision"], {"chosen_passages": a["passages"], "conditions": a["conditions"],
                           "params": a["params"], "answer_sha256": ra["sha256"], "round": rnd},
                           f"Round {rnd} (DECISIONS {R['decision']})", ra["at"])
        readings = [{"principal": R["proposer"], "family": "A", "at": ra["at"], "chosen_passages": a["passages"], "blind": False, "evento": ev_a}]
        if b is not None:
            ev_b = log.review("leitor:b", "regra", t["rule"], cur["revision"] + 1, f"Blind, same prompt as {R['proposer']} (round {rnd}): {question}", "blind",
                              "uphold" if row["exact"] else "request_evidence", rb["at"],
                              payload={"chosen_passages": b["passages"], "conditions": b["conditions"], "params": b["params"],
                                       "answer_sha256": rb["sha256"], "round": rnd})
            readings.append({"principal": "leitor:b", "family": "B", "at": rb["at"], "chosen_passages": b["passages"], "blind": True, "evento": ev_b})
        row["state"] = log.replay().state_of("regra", t["rule"])
        new = build_rule(store, t, a, a["passages"], readings, row["state"])
        writer.revise(writer.store.current(t["rule"]), {k: new[k] for k in content}, now_utc())
    return rows


ROUND_NOTE = {2: "As mesmas perguntas e candidatas da ronda 1, com três defeitos do prompt corrigidos (D44); leitor:a corrige a sua proposta, leitor:b revê às cegas.",
              3: "O prompt da ronda 2 com as condições tipadas por campo; propõe leitor:a2 (AMALIA + adaptador, decisão da pessoa, D45), leitor:b revê às cegas.",
              4: "O prompt e o esquema da ronda 3, sem mudança; propõe leitor:a3 (AMALIA + adaptador v2, treinado em condicoes_texto, D46), leitor:b revê às cegas.",
              5: "O prompt e o esquema da ronda 4, sem mudança; propõe leitor:a4 (AMALIA + adaptador v3, treinado também em entrada_em_vigor e periodos_vigencia, D47), leitor:b revê às cegas."}


def write_round_report(rows, rnd):
    if not rows:
        return
    L = [f"# RONDA {rnd} — B3, as quatro regras que o motor precisa primeiro (DECISIONS {ROUNDS[rnd]['decision']})", "",
         f"Gerado por tools/read_rules.py. {ROUND_NOTE[rnd]} Só fica settled a leitura que leitor:b replica em forma canónica (D43).", "",
         "| regra | estado | exato | direção |", "|---|---|---|---|"]
    for r in rows:
        L.append(f"| {r['rule']} | {r['state']}{' (' + r['why'] + ')' if r.get('why') else ''} | "
                 f"{'—' if r['exact'] is None else ('sim' if r['exact'] else 'não')} | {'—' if r['direction'] is None else ('sim' if r['direction'] else 'não')} |")
    L.append("")
    for r in rows:
        L += [f"## {r['rule']}", "", f"- {ROUNDS[rnd]['proposer']}: {show(r['a'])}", f"- leitor:b: {show(r['b'])}", ""]
    (ROUNDS[rnd]["dir"] / f"RONDA{rnd}.md").write_text("\n".join(L) + "\n", encoding="utf-8")


def write_packages(writer):
    store = Store([ROOT / "law", ROOT / "rules", ROOT / "governance"]).load()
    rules = {}
    for r in store.objects["regra"]:
        if r["id"] not in rules or r["revision"] > rules[r["id"]]["revision"]:
            rules[r["id"]] = r
    head = Log(ROOT / "governance").head()
    built = now_utc()
    packs = {}
    for date, pid, law in ((OLD, "pacote:ccp@2026-09-30", "lei:ccp@2026-09-30"), (NEW, "pacote:ccp@2026-10-01", "lei:ccp@2026-10-01")):
        # the regime selector routes every procedure, before or after its own date: it sits in both packages
        chosen = [r for r in rules.values() if r["state"] == "settled" and (rules_mod.valid_at(r, date) or r["type"] == "seletor_regime")]
        if not chosen:  # no settled rule valid that day: no package (a package names at least one rule)
            continue
        pk = rules_mod.package(pid, law, chosen, head, built, built)
        prev = store.current(pid)
        if prev is None:
            writer.append(pk)
        elif prev["hash"] != pk["hash"] or prev["log_head"] != pk["log_head"]:
            pk = writer.revise(prev, {k: v for k, v in pk.items() if k not in ("id", "revision", "recorded_at")}, built)
        packs[pid] = pk
    if len(packs) < 2:
        return sorted(packs)
    d = rules_mod.diff(packs["pacote:ccp@2026-09-30"], packs["pacote:ccp@2026-10-01"], rules)
    did = "diff:pacote:ccp@2026-09-30..pacote:ccp@2026-10-01"
    obj = {"id": did, "revision": 1, "recorded_at": built, "from": "pacote:ccp@2026-09-30", "to": "pacote:ccp@2026-10-01", **d}
    prev = store.current(did)
    if prev is None:
        writer.append(obj)
    elif (prev["by_rule"], prev["by_consumer_field"]) != (obj["by_rule"], obj["by_consumer_field"]):
        writer.revise(prev, {"by_rule": obj["by_rule"], "by_consumer_field": obj["by_consumer_field"]}, built)
    return sorted(packs)


def show(r):
    if r is None:
        return "—"
    return f"passagens {', '.join(r['passages'])}; condições {json.dumps(r['conditions'], ensure_ascii=False)}; params {json.dumps(r['params'], ensure_ascii=False)}"


def write_reports(summary, disagreements, packs=()):
    L = ["# DESACORDOS — leituras em que leitor:b, cego, não coincide com leitor:a", "",
         "Gerado por tools/read_rules.py a partir das respostas guardadas. Para a pessoa ver: decide produto (que regras entram, que "
         "campos o motor lê), nunca o conteúdo de uma leitura da lei; uma leitura só fica settled quando leitor:b, cego e de outra família, "
         "coincide (D37).", ""]
    for t, a, b in disagreements:
        L += [f"## {t['rule']} ({t['type']})", "", f"- leitor:a: {show(a)}", f"- leitor:b: {show(b)}",
              f"- difere em: {', '.join(k for k in ('passages', 'conditions', 'params') if a[k] != b[k])}", ""]
    (READINGS / "DESACORDOS.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    by_type = {}
    for r in summary:
        x = by_type.setdefault(r["type"], {"propostas": 0, "settled": 0, "ai_reviewed": 0, "proposed": 0, "sem_leitura": 0})
        if r["state"] in ("settled", "ai_reviewed", "proposed"):
            x["propostas"] += 1
            x[r["state"]] += 1
        else:
            x["sem_leitura"] += 1
    R = ["# RESUMO — leituras de B3", "", "Gerado por tools/read_rules.py a partir das respostas guardadas em governance/readings/.", "",
         "| tipo | propostas | settled | ai_reviewed | proposed | sem leitura válida de A |", "|---|---|---|---|---|---|"]
    for k, x in sorted(by_type.items()):
        R.append(f"| {k} | {x['propostas']} | {x['settled']} | {x['ai_reviewed']} | {x['proposed']} | {x['sem_leitura']} |")
    both = [r for r in summary if r["exact"] is not None]
    R += ["", f"Acordo exato A vs B (a mesma leitura em forma canónica: regra de produto da pessoa, evento:43): {sum(r['exact'] for r in both)} de {len(both)}.",
          f"Acordo de direção A vs B (o valor de que a regra depende: limiar, dias, lista de procedimentos, regimes, efeito): "
          f"{sum(r['direction'] for r in both)} de {len(both)}.", "",
          f"Pacotes escritos: {', '.join(packs) or 'nenhum'} (um pacote só nomeia regras settled válidas na sua data; sem pacote dos dois "
          "lados não há diff).", "",
          "| regra | tipo | estado | exato | direção |", "|---|---|---|---|---|"]
    for r in summary:
        R.append(f"| {r['rule']} | {r['type']} | {r['state']}{' (' + r['why'] + ')' if r.get('why') else ''} | "
                 f"{'—' if r['exact'] is None else ('sim' if r['exact'] else 'não')} | {'—' if r['direction'] is None else ('sim' if r['direction'] else 'não')} |")
    (READINGS / "RESUMO.md").write_text("\n".join(R) + "\n", encoding="utf-8")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["prompts", "record"])
    ap.add_argument("--only", help="prompts for the rules whose id contains this text")
    ap.add_argument("--round", type=int, default=1, choices=[1, 2, 3, 4, 5], help="2-5: the D44-D47 round prompts, in governance/readings/ronda<n>/")
    a = ap.parse_args()
    if a.cmd == "prompts":
        cmd_prompts(Store([ROOT / "law"]).load(), a.only, a.round)
    else:
        cmd_record()


if __name__ == "__main__":
    main()
