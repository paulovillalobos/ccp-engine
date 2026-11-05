"""Phase 18 data (DECISIONS D73): data-v15, AMALIA's one push on everything the real law showed in rounds 11 and 12.

    .venv/bin/python tools/make_rule_readings_v15.py check      the rows each part gives and what is left out; writes nothing
    .venv/bin/python tools/make_rule_readings_v15.py generate   training/data-v15

Three parts, every row rendered and checked with the protocol 0.5 (read_rules_v3.V05):
- keys: the real passages both families settled blind in rounds 11 (texto_visto) and 12 (pratica), under
  product_rule:leituras-assentes-como-pratica (evento:276). The gold is family A's reading the log holds settled; each passage
  gives its own row and VARIANTS more with its days or euro amounts moved by code where its quotes are. A key is left out when
  any passage its reader sees is in a reserved article (TRAIN-HELD-OUT's list, or for an act that list did not yet hold its
  frozen hash rule), is an exam target, or is close to one (difflib ratio LEAK).
- written: invented articles (norma:exemplo) in the shapes round 12 showed AMALIA does not read: a deadline the interested
  party has at most N days for (prazo_maximo); a deadline the entity itself must meet, a duration or an obligation to keep
  («não tipável»: nao_e_prazo_maximo, or nao_e_prazo_minimo when asked for a minimum); the directives' minimum deadlines with
  their own procedure names, their reductions for urgency and pré-informação; a directive's thresholds (nao_e_limiar); a
  deadline in working days (sem_vocabulario). Drawn by code from WRITTEN_SEED; the gold is quoted by data-v12's code (derive)
  with the 0.5 tables, and a row exists only when the factory's checker passes it. An article close to an exam passage is
  dropped.
- remind: data-v14's practice rows and the first REMIND of data-v13's training rows by sha256 of the id (protocol 0.4), so v15,
  trained from v14, keeps what v13 and v14 learned.
Out: regra_lida/train.jsonl, REJECTED.json, INDEX.json. Nothing here calls a model.
"""
import argparse
import copy
import hashlib
import json
import random
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT)); sys.path.insert(0, str(ROOT / "tools"))
import make_rule_readings_v12 as v12  # noqa: E402  (written article -> law, derive, close)
import make_rule_readings_v13 as v13  # noqa: E402  (dump, data-v13's rows)
import make_rule_readings_v14 as v14  # noqa: E402  (move_days, move_amount, replace_in, AMOUNTS)
import read_rules_v3 as v3  # noqa: E402
import rule_factory as rf  # noqa: E402
from engine.governance import Log  # noqa: E402

VERSION = "ccp-make-rule-readings-v15-0.1"
PROTOCOL = v3.V05
DATA = ROOT / "training/data-v15"
TASK = v12.TASK
PRODUCT_RULE = v14.PRODUCT_RULE
VARIANTS = 24
REMIND = 600
WRITTEN_SEED = "D73"
KEY_STRATA = {11: "texto_visto", 12: "pratica"}  # the strata a round may give as practice; reservado is the exam
COUNTS = {"maximo": 350, "entidade_max": 250, "entidade_min": 100, "ue_minimo": 300, "ue_limiar": 60, "uteis": 60}


# ---- what no row may show ----------------------------------------------------------------------------------------------
def reserved_article(law, reserved, pid):
    art = law.article_of(pid) or pid
    return art in reserved or (not pid.startswith(("ccp:", "exemplo:")) and int(hashlib.sha256(art.encode()).hexdigest(), 16) % 5 == 0)


def exam(store):
    """Every passage a round holds as exam: round 10's open targets (data-v14's EXAM), the reservado of rounds 11 and 12."""
    out = set(v14.EXAM)
    out |= {pid for pid, (_, k) in rf.FROUNDS[11]["pick"].items() if k == "reservado"}
    out |= {pid for pid, _, _, k in rf.FROUNDS[12]["pick"] if k == "reservado"}
    return out


# ---- keys ------------------------------------------------------------------------------------------------------------------
def settled_keys(store):
    """[(round, target, gold answer, prompt version)] for every practice-stratum target whose reading the log holds settled."""
    rp = Log(store.governance_dir).replay()
    out = []
    for n, stratum in KEY_STRATA.items():
        for t in rf.targets(store, n):
            k = t.get("stratum")
            if k != stratum:
                continue
            d = rf.FROUNDS[n]["dir"] / rf.rr.slug(t["rule"])
            body = json.loads((d / "prompt.json").read_text(encoding="utf-8"))
            a, errs = rf.checked(json.loads((d / rf.FROUNDS[n]["proposer"][1]).read_text(encoding="utf-8")), body["context"], t["type"], body.get("protocol_version"))
            if errs or a is None:
                continue
            nt = bool(a.get("nao_tipavel"))
            aid = t["rule"].replace("regra:", "nao_tipavel:", 1) if nt else t["rule"]
            if rp.state_of("nao_tipavel" if nt else "regra", aid) == "settled":
                out.append((n, t, a))
    return out


def move(answer, ctx, rtype, rng):
    """(answer, ctx) with each rule's days or amount moved where its quotes are; a «não tipável» moves the target's first number."""
    a, c = copy.deepcopy(answer), copy.deepcopy(ctx)
    if a.get("nao_tipavel"):
        text = c["allowed"][c["alvo"]]
        d, m = v14.DAYS_RE.search(text), next(v12.AMOUNT.finditer(text), None)
        if m and (d is None or m.start() < d.start()):
            old = int(re.sub(r"[ . ]", "", m.group(1) or m.group(2)))
            new = rng.choice([x for x in v14.AMOUNTS if x != old])
            moved = v14.move_amount(text, old, new)
            mover = lambda s: v14.move_amount(s, old, new)  # noqa: E731
        elif d:
            old = int(d.group(1)); new = rng.choice([x for x in range(3, 91) if x != old])
            moved = v14.move_days(text, old, new)
            mover = lambda s: v14.move_days(s, old, new)  # noqa: E731
        else:
            raise v12.Gap("no number in the target to move")
        if moved == text:
            raise v12.Gap("the number did not move")
        v14.replace_in(c, c["alvo"], text, moved)
        for f in a["nao_tipavel"]["fontes"]:
            if f["de"] == c["alvo"] and not v3.contains(moved, f["texto"]):
                f["texto"] = mover(f["texto"])
        return a, c
    used = set()
    for r in a["regras"]:
        p = r["params"]
        if rtype in v3.PRAZOS:
            key = v3.DAYS_KEY[rtype]
            old = p[key]
            new = rng.choice([x for x in range(3, 91) if x != old and x not in used])
            for f in r["fontes"][key]:
                t2 = v14.move_days(f["texto"], old, new)
                v14.replace_in(c, f["de"], f["texto"], t2)
                f["texto"] = t2
            p[key] = new
        else:
            th = p["threshold"]
            old = th["value"]
            new = rng.choice([x for x in v14.AMOUNTS if x != old and x not in used])
            for f in r["fontes"]["value"]:
                t2 = v14.move_amount(f["texto"], old, new)
                v14.replace_in(c, f["de"], f["texto"], t2)
                f["texto"] = t2
            th["value"] = new
        used.add(new)
    return a, c


def row(rid, rtype, ctx, answer, estilo, sources=()):
    return {"id": f"{TASK}:{rid}", "task": TASK, "prompt": v3.render(ctx, rtype, PROTOCOL), "schema": v3.schema(ctx, rtype, PROTOCOL),
            "answer": json.dumps(answer, ensure_ascii=False, separators=(",", ":")), "sources": sorted(sources), "estilo": estilo}


def key_rows(store):
    law = v3.Law(store)
    reserved = set(json.loads((ROOT / "law/TRAIN-HELD-OUT.json").read_text(encoding="utf-8"))["reserved_articles"])
    ex_set = exam(store)
    ex_texts = [x for x in (law.text(p, rf.DATE) for p in ex_set) if x]
    rows, per, rejected = [], {}, {}
    for n, t, gold in settled_keys(store):
        pid, rtype, date = t["source_passage"], t["type"], t["date"]
        ctx = v3.context(law, pid, date)
        seen = [q for q in ctx["allowed"] if not q.startswith("norma:") and ":" in q]
        why = next((f"its reader sees {q}, in a reserved article" for q in seen if ctx["roles"].get(q) != "titulo" and reserved_article(law, reserved, q)), None)
        why = why or next((f"its reader sees {q}, an exam passage" for q in seen if q in ex_set), None)
        why = why or next((f"its reader sees {q}, close to an exam passage" for q in seen if ctx["allowed"][q] and v12.close(ctx["allowed"][q], ex_texts)), None)
        if why:
            rejected[t["rule"]] = why
            continue
        errs = v3.check(gold, ctx, rtype, PROTOCOL)
        if errs:
            rejected[t["rule"]] = f"checker 0.5: {errs[0]}"
            continue
        src = {q for q in seen if ctx["roles"].get(q) != "titulo"}
        base = f"real:{pid}:{date}"
        mine = [row(f"{base}:00", rtype, ctx, gold, "real", src)]
        for k in range(1, VARIANTS + 1):
            rng = random.Random(f"{VERSION}:{t['rule']}:{k}")
            try:
                a2, c2 = move(gold, ctx, rtype, rng)
            except (v12.Gap, KeyError, ValueError):
                continue
            if v3.check(a2, c2, rtype, PROTOCOL):
                continue
            mine.append(row(f"{base}:{k:02d}", rtype, c2, a2, "real", src))
        rows += mine
        per[t["rule"]] = {"round": n, "rows": len(mine), "nao_tipavel": bool(gold.get("nao_tipavel"))}
    return rows, per, rejected


# ---- written articles ------------------------------------------------------------------------------------------------------
NUM_WORDS = {3: "três", 5: "cinco", 6: "seis", 8: "oito", 10: "dez", 15: "quinze", 20: "vinte", 30: "trinta", 60: "sessenta", 90: "noventa"}
CCP_PLACES = [("Capítulo II — Concurso público", "concurso_publico"), ("Capítulo III — Concurso limitado por prévia qualificação", "concurso_limitado_previa_qualificacao"),
              ("Capítulo IV — Procedimento de negociação", "procedimento_negociacao"), ("Capítulo V — Diálogo concorrencial", "dialogo_concorrencial"),
              ("Capítulo II — Consulta prévia", "consulta_previa"), ("Capítulo VI — Disposições comuns", None), ("Capítulo VII — Fase de habilitação", None)]
EU_PROC = [("Concurso aberto", "Nos concursos abertos", "concurso_aberto"), ("Concurso limitado", "Nos concursos limitados", "concurso_limitado_previa_qualificacao"),
           ("Procedimento concorrencial com negociação", "Nos procedimentos concorrenciais com negociação", "procedimento_concorrencial_negociacao"),
           ("Procedimento por negociação com abertura prévia de concurso", "Nos procedimentos por negociação com abertura prévia de concurso", "procedimento_negociacao_com_concurso")]
FILLERS = ["O anúncio é publicado no Diário da República e disponibilizado na plataforma eletrónica utilizada pela entidade adjudicante.",
           "As peças do procedimento são disponibilizadas desde a data da publicação do anúncio, em condições de igualdade.",
           "A decisão é notificada em simultâneo a todos os concorrentes, com cópia do relatório que a fundamenta.",
           "Os documentos são redigidos em língua portuguesa ou acompanhados de tradução devidamente legalizada.",
           "A entidade adjudicante pode exigir que os documentos sejam apresentados por meios eletrónicos.",
           "O programa do procedimento indica o modo de apresentação dos documentos e a forma da sua assinatura."]
MAXIMA = [("pronunciar-se", "prazo_pronuncia_dias", "Os concorrentes podem pronunciar-se por escrito sobre o relatório preliminar"),
          ("reclamação", "prazo_reclamacao_dias", "Os interessados podem apresentar reclamação da lista dos concorrentes"),
          ("prestar a caução", "prazo_caucao_dias", "O adjudicatário deve prestar a caução"),
          ("documentos de habilitação", "prazo_habilitacao_dias", "O adjudicatário apresenta os documentos de habilitação"),
          ("pedidos de esclarecimentos", "prazo_esclarecimentos_dias", "Os interessados podem apresentar pedidos de esclarecimentos")]
MAX_WORDS = ["no prazo de", "no prazo máximo de", "até"]
FROM = [("a contar da data da notificação", "data_notificacao"), ("a contar da notificação", "data_notificacao")]
ENTITY = [("A entidade adjudicante envia o anúncio de adjudicação ao Serviço das Publicações da União Europeia {m} {d} após a celebração do contrato", "enviar o anúncio de adjudicação"),
          ("O júri elabora o relatório preliminar fundamentado {m} {d}", "elaborar o relatório preliminar"),
          ("O órgão competente para a decisão de contratar decide a reclamação {m} {d} a contar da sua apresentação", "decidir a reclamação"),
          ("Os pagamentos devidos pelo contraente público são efetuados {m} {d} após a entrega das respetivas faturas", "efetuar os pagamentos"),
          ("O dono da obra realiza a vistoria {m} {d} contados da receção da solicitação do empreiteiro", "realizar a vistoria"),
          ("O contraente público pronuncia-se sobre a proposta do cocontratante {m} {d} a contar da respetiva entrega", "se pronunciar sobre a proposta do cocontratante"),
          ("A entidade adjudicante comunica ao instituto competente a aplicação da sanção {m} {d} após a sua aplicação", "comunicar a sanção ao instituto"),
          ("A entidade adjudicante publicita a modificação do contrato no portal dos contratos públicos {m} {d} após a sua concretização", "publicitar a modificação do contrato"),
          ("O órgão competente decide as impugnações administrativas {m} {d} a contar da data da sua entrega", "decidir as impugnações"),
          ("A entidade adjudicante promove a liberação integral da caução {m} {d} após o termo do prazo de garantia", "liberar a caução")]
KEEP = [("Os concorrentes são obrigados a manter as respetivas propostas pelo prazo de {d} contados do termo do prazo fixado para a sua entrega", "manter as propostas")]


def days_text(d, rng):
    return f"{NUM_WORDS[d]} dias" if d in NUM_WORDS and rng.random() < 0.4 else f"{d} dias"


def article(rid, tipo, lugar, epigrafe, nums, alvo, gold):
    ex = {"id": rid, "tipo": tipo, "lugar": lugar, "artigo": f"{rid_num(rid)}.º", "epigrafe": epigrafe,
          "numeros": [{"n": str(i), "texto": t} for i, t in enumerate(nums, 1)], "alvo": str(alvo)}
    ex.update(gold)
    return ex


def rid_num(rid):
    return 6000 + int(hashlib.sha256(rid.encode()).hexdigest(), 16) % 3000


def numbered(texts, eu):
    return [(f"{i}. " if eu else f"{i} - ") + t for i, t in enumerate(texts, 1)]


def written_examples():
    rng = random.Random(WRITTEN_SEED)
    out = []
    for k in range(COUNTS["maximo"]):  # a deadline the interested party has at most N days for
        phrase, field, subject = rng.choice(MAXIMA)
        place, proc = rng.choice(CCP_PLACES)
        d = rng.randint(3, 30)
        cf_words, cf = rng.choice(FROM if field != "prazo_esclarecimentos_dias" else [("a contar da data do envio do convite", "data_envio_convite")])
        m = rng.choice(MAX_WORDS)
        target = f"{subject} {m} {days_text(d, rng)} {cf_words}."
        texts = [rng.choice(FILLERS), target] if rng.random() < 0.5 else [target, rng.choice(FILLERS)]
        alvo = texts.index(target) + 1
        conds = [{"field": "tipo_procedimento", "op": "eq", "value": proc}] if proc else []
        out.append(article(f"w15-max-{k:03d}", "prazo_maximo", ["Título III — Tramitação procedimental", place], "Prazos dos interessados",
                           numbered(texts, False), alvo, {"regras": [{"condicoes": conds, "params": {"maximum_days": d, "deadline_field": field, "counted_from": cf}}], "estilo": "w15-maximo"}))
    for kind, motivo, count in (("entidade_max", "nao_e_prazo_maximo", COUNTS["entidade_max"]), ("entidade_min", "nao_e_prazo_minimo", COUNTS["entidade_min"])):
        for k in range(count):  # the entity's own deadline, a duration, an obligation to keep: no rule of the type asked
            tmpl, act = rng.choice(ENTITY + KEEP) if rng.random() < 0.9 else rng.choice(KEEP)
            d = rng.randint(3, 90)
            m = rng.choice(["no prazo de", "no prazo máximo de", "até"]) if "{m}" in tmpl else ""
            dt = days_text(d, rng)
            target = tmpl.format(m=m, d=dt).replace("  ", " ") + "."
            fonte = target[:target.index(dt) + len(dt)]
            falta = (f"O prazo é para {act}, não para os interessados apresentarem algo." if act != "manter as propostas"
                     else "O prazo é para manter as propostas, não para as apresentar.")
            place, _ = rng.choice(CCP_PLACES)
            texts = [target, rng.choice(FILLERS)]
            out.append(article(f"w15-{kind}-{k:03d}", "prazo_maximo" if kind == "entidade_max" else "prazo_minimo", ["Título IV — Execução e decisão", place],
                               "Prazos da entidade adjudicante", numbered(texts, False), 1,
                               {"regras": [], "nao_tipavel": {"motivo": motivo, "fonte": fonte, "falta": falta}, "estilo": f"w15-{kind}"}))
    for k in range(COUNTS["ue_minimo"]):  # the directives' minimum deadlines, their own procedure names, reductions
        epig, opening, proc = rng.choice(EU_PROC)
        d = rng.choice([30, 35, 40, 45, 50, 52]) if rng.random() < 0.6 else rng.randint(20, 60)
        cand = proc != "concurso_aberto" and rng.random() < 0.5
        base = (f"{opening}, o prazo mínimo de receção dos pedidos de participação é de {d} dias a contar da data de envio do anúncio de concurso."
                if cand else f"{opening}, o prazo mínimo de receção das propostas é de {d} dias a contar da data de envio do anúncio de concurso.")
        field = "prazo_candidaturas_dias" if cand else "prazo_propostas_dias"
        shape = rng.random()
        lugar = ["TÍTULO II — REGRAS APLICÁVEIS AOS CONTRATOS PÚBLICOS", "CAPÍTULO I — Procedimentos"]
        if shape < 0.5:
            texts, alvo = [base, rng.choice(FILLERS)], 1
            rule = {"condicoes": [{"field": "tipo_procedimento", "op": "eq", "value": proc}], "params": {"minimum_days": d, "deadline_field": field, "counted_from": "data_envio_anuncio"}}
        elif shape < 0.75:
            r = rng.randint(10, max(11, d - 5))
            texts = [base, f"Nos casos em que uma situação de urgência devidamente fundamentada torne impraticável o prazo fixado no n.º 1, as autoridades adjudicantes podem fixar um prazo que não será inferior a {r} dias a contar da data de envio do anúncio de concurso."]
            alvo = 2
            rule = {"condicoes": [{"field": "tipo_procedimento", "op": "eq", "value": proc}, {"field": "urgencia_fundamentada", "op": "eq", "value": True}],
                    "params": {"minimum_days": r, "deadline_field": field, "counted_from": "data_envio_anuncio"}}
        else:
            r = rng.randint(10, max(11, d - 5))
            texts = [base, f"Se as autoridades adjudicantes tiverem publicado um anúncio de pré-informação, o prazo mínimo fixado no n.º 1 pode ser reduzido para {r} dias."]
            alvo = 2
            rule = {"condicoes": [{"field": "tipo_procedimento", "op": "eq", "value": proc}, {"field": "anuncio_pre_informacao", "op": "eq", "value": True}],
                    "params": {"minimum_days": r, "deadline_field": field, "counted_from": "data_envio_anuncio"}}
        out.append(article(f"w15-ue-{k:03d}", "prazo_minimo", lugar, epig, numbered(texts, True), alvo, {"regras": [rule], "estilo": "w15-ue-minimo"}))
    for k in range(COUNTS["ue_limiar"]):  # a directive's threshold: the act's scope, no procedure chosen below it
        v = rng.choice([134000, 139000, 140000, 143000, 207000, 214000, 216000, 221000, 750000, 5186000, 5350000, 5404000, 5538000])
        what = rng.choice(["para os contratos de empreitada de obras públicas", "para os contratos públicos de fornecimento e de serviços", "para os contratos de serviços sociais"])
        amount = f"{v:,}".replace(",", " ")
        fonte = f"seja igual ou superior a {amount} EUR {what}"
        target = f"A presente diretiva aplica-se aos contratos cujo valor estimado, sem imposto sobre o valor acrescentado, {fonte}."
        out.append(article(f"w15-uelim-{k:03d}", "limiar", ["TÍTULO I — ÂMBITO DE APLICAÇÃO", "CAPÍTULO I — Âmbito de aplicação e definições"], "Montantes limiares",
                           [f"1. {target}", "2. " + rng.choice(FILLERS)], 1,
                           {"regras": [], "nao_tipavel": {"motivo": "nao_e_limiar", "fonte": fonte,
                                                          "falta": "O valor delimita os contratos a que a diretiva se aplica; não é o limite até ao qual um procedimento pode ser escolhido."},
                            "estilo": "w15-ue-limiar"}))
    for k in range(COUNTS["uteis"]):  # working days: a unit the vocabulary does not hold
        phrase, field, subject = rng.choice(MAXIMA)
        d = rng.randint(3, 20)
        dt = f"{d} dias úteis"
        target = f"{subject} no prazo de {dt} a contar da notificação."
        out.append(article(f"w15-uteis-{k:03d}", "prazo_maximo", ["Título III — Tramitação procedimental", rng.choice(CCP_PLACES)[0]], "Prazos dos interessados",
                           numbered([target, rng.choice(FILLERS)], False), 1,
                           {"regras": [], "nao_tipavel": {"motivo": "sem_vocabulario", "fonte": f"no prazo de {dt}", "falta": "Um prazo em dias úteis, unidade que o vocabulário não tem."}, "estilo": "w15-uteis"}))
    return out


def max_answer(ex, ctx):
    """A prazo_maximo article's gold: data-v12's quotes for the same deadline as a minimum, the days quote taken back to the
    words that make it a maximum («no prazo de», «até»), as the checker asks."""
    as_min = copy.deepcopy(ex)
    as_min["tipo"] = "prazo_minimo"
    for r in as_min["regras"]:
        p = r["params"]
        r["params"] = {"minimum_days": p["maximum_days"], "deadline_field": p["deadline_field"], "counted_from": p["counted_from"], "usual_days": None}
    a = v12.derive(as_min, ctx)
    for r in a["regras"]:
        r["tipo"] = "prazo_maximo"
        p = r["params"]
        r["params"] = {"maximum_days": p["minimum_days"], "deadline_field": p["deadline_field"], "counted_from": p["counted_from"]}
        q = r["fontes"].pop("minimum_days")
        r["fontes"].pop("usual_days", None)
        f = q[0]
        text = ctx["allowed"][f["de"]]
        at = text.find(f["texto"])
        lead = max((text.rfind(w, 0, at) for w in v3.VOC["since_0_5"]["maximum_phrases"] if 0 <= text.rfind(w, 0, at) >= at - 25), default=-1)
        if lead < 0:
            raise v12.Gap("no maximum words before the days")
        r["fontes"] = {"maximum_days": [{"texto": text[lead:at + len(f["texto"])], "de": f["de"]}], "deadline_field": r["fontes"]["deadline_field"],
                       "counted_from": r["fontes"]["counted_from"]}
    return a


def written_rows(store):
    law = v3.Law(store)
    ex_texts = [x for x in (law.text(p, rf.DATE) for p in exam(store)) if x]
    rows, rejected = [], {}
    saved = v12.VOC
    try:
        v12.VOC = v3.VOC5  # the 0.5 tables: the directives' procedure names, «pedidos de participação»
        with v3._using(PROTOCOL):
            for ex in written_examples():
                try:
                    ctx = v12.ctx_of(ex)
                    target = ctx["allowed"][ctx["alvo"]]
                    if v12.close(target, ex_texts):
                        rejected[ex["id"]] = "close to an exam passage"; continue
                    answer = max_answer(ex, ctx) if ex["tipo"] == "prazo_maximo" and not ex.get("nao_tipavel") else v12.derive(ex, ctx)
                except (v12.Gap, KeyError, ValueError, IndexError) as exc:
                    rejected[ex["id"]] = f"gold: {exc}"; continue
                errs = v3.check(answer, ctx, ex["tipo"], PROTOCOL)
                if errs:
                    rejected[ex["id"]] = f"checker: {errs[0]}"; continue
                rows.append(row(ex["id"], ex["tipo"], ctx, answer, ex["estilo"]))
    finally:
        v12.VOC = saved
    return rows, rejected


# ---- the set -------------------------------------------------------------------------------------------------------------
def remind():
    v14_rows = [json.loads(line) for line in (v14.DATA / "regra_lida/train.jsonl").read_text(encoding="utf-8").splitlines() if line.strip()]
    practice = [r for r in v14_rows if r.get("estilo") == "real"]
    v13_rows = [json.loads(line) for line in (v13.DATA / "regra_lida/train.jsonl").read_text(encoding="utf-8").splitlines() if line.strip()]
    return practice + sorted(v13_rows, key=lambda r: hashlib.sha256(r["id"].encode()).hexdigest())[:REMIND]


def allowed_sources(store):
    """What verify lets a key row cite inside a reserved article: nothing (a key that shows one is left out)."""
    return set()


def build(store=None):
    from engine.store import Store
    store = store or Store([ROOT / "law", ROOT / "rules", ROOT / "governance"]).load()
    keys, per, rej_k = key_rows(store)
    written, rej_w = written_rows(store)
    return keys, written, remind(), per, {**rej_k, **rej_w}


def generate(store=None, held_doc=None):
    keys, written, old, per, rejected = build(store)
    files = {"regra_lida/train.jsonl": v13.dump(keys + written + old),
             "REJECTED.json": (json.dumps(rejected, ensure_ascii=False, indent=1, sort_keys=True) + "\n").encode("utf-8")}
    styles = {}
    for r in written:
        styles[r["estilo"]] = styles.get(r["estilo"], 0) + 1
    index = {"tool": VERSION, "protocol": PROTOCOL, "product_rule": PRODUCT_RULE, "keys": per, "key_rows": len(keys), "written_rows": len(written),
             "written_by_style": styles, "remind_rows": len(old), "rejected": len(rejected),
             "files": {k: {"rows": v.count(b"\n"), "sha256": hashlib.sha256(v).hexdigest()} for k, v in sorted(files.items())},
             "note": "D73: the settled real readings of rounds 11-12 with their numbers moved, invented articles in the shapes round 12 showed, and v13/v14 rows kept"}
    files["INDEX.json"] = (json.dumps(index, ensure_ascii=False, indent=1) + "\n").encode("utf-8")
    return files


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("cmd", choices=["check", "generate"])
    a = ap.parse_args()
    if a.cmd == "check":
        keys, written, old, per, rejected = build()
        print(f"keys {len(per)} -> rows {len(keys)}; written rows {len(written)}; remind {len(old)}; left out {len(rejected)}")
        why = {}
        for k, w in rejected.items():
            why[w.split(":")[0][:60]] = why.get(w.split(":")[0][:60], 0) + 1
        print(sorted(why.items(), key=lambda x: -x[1])[:12])
        return
    files = generate()
    for rel, b in files.items():
        f = DATA / rel
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_bytes(b)
    print({k: v for k, v in json.loads(files["INDEX.json"]).items() if k not in ("files", "keys")})


if __name__ == "__main__":
    main()
