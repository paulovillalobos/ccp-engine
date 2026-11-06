"""Phase 20 data (DECISIONS D85): data-v17, for v17 trained from v16's adapter on one rule type only, contagem_prazo
(protocol 0.6), on the person's «Yes, counting only» (2026-11-06).

    .venv/bin/python tools/make_rule_readings_v17.py check | generate

- written: COUNT invented articles of the counting of deadlines, each asked as contagem_prazo with protocol 0.6: an
  aspect (primeiro_dia, fins_de_semana, termo) and its value in the law's words, for one deadline (propostas,
  candidaturas) or todos, sometimes for one procedure only (a case of its own, L5); and NEGATIVE articles that fix a
  deadline's length or its start and say nothing of how its days are counted (nao_e_contagem). The answers are written
  here, every quote a piece of the text, and every row passes the 0.6 checker. Nothing is read from round 17: the real
  passages it asks about (CPA art. 87.º, CCP art. 470.º) are never a row, and a row whose target is close to one of
  them is left out (v12.close), so round 17 stays a blind read.
- remind: REMIND rows of data-v16 by sha256 of the id, so v17 keeps what v16 reads.
Nothing here calls a model.
"""
import hashlib
import json
import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT)); sys.path.insert(0, str(ROOT / "tools"))
import make_rule_readings_v12 as v12  # noqa: E402
import make_rule_readings_v13 as v13  # noqa: E402
import make_rule_readings_v15 as v15  # noqa: E402
import read_rules_v3 as v3  # noqa: E402

VERSION = "ccp-make-rule-readings-v17-0.1"
DATA = ROOT / "training/data-v17"
PROTOCOL = v3.V06
TASK = v12.TASK
COUNT, NEGATIVE, REMIND = 360, 120, 600
SEED = "D85"
ROUND17 = ("cpa:art87.b", "cpa:art87.c", "cpa:art87.f", "ccp:art470.2", "ccp:art470.3")  # the exam of this round: never a row
LUGAR = ["Parte V — Disposições finais", "Título I — Prazos"]
FIELDS = {"prazo_propostas_dias": ["apresentação das propostas", "entrega das propostas"],
          "prazo_candidaturas_dias": ["apresentação das candidaturas", "entrega das candidaturas"]}
PROCS = [("concurso_publico_urgente", "concurso público urgente"), ("ajuste_direto_simplificado", "ajuste direto simplificado"),
         ("consulta_previa", "consulta prévia")]
EPIGRAFES = ["Contagem dos prazos", "Regras de contagem", "Cômputo dos prazos", "Contagem dos prazos procedimentais"]
# (aspecto, valor, sentence with {f} for a deadline's words or none, the law's words the answer quotes)
ASPECT_TEXTS = [
    ("primeiro_dia", "nao_conta", "Não se inclui na contagem o dia em que ocorrer o facto a partir do qual {o} começa a correr", "Não se inclui na contagem o dia"),
    ("primeiro_dia", "nao_conta", "Na contagem {d}, não se inclui na contagem o dia do evento que marca o seu início", "não se inclui na contagem o dia"),
    ("fins_de_semana", "suspende", "{O} suspende-se nos sábados, domingos e feriados", "suspende-se nos sábados, domingos e feriados"),
    ("fins_de_semana", "continuo", "{O} são contínuos", "são contínuos"),
    ("fins_de_semana", "continuo", "{O} correm sem interrupção, não se suspendendo nos sábados, domingos e feriados", "não se suspendendo nos sábados, domingos e feriados"),
    ("termo", "transfere", "O termo {d} que coincida com dia em que o serviço não esteja aberto ao público transfere-se para o primeiro dia útil seguinte",
     "transfere-se para o primeiro dia útil seguinte"),
    ("termo", "transfere", "Quando o último dia {d} for feriado ou o serviço estiver encerrado, o termo transfere-se para o 1.º dia útil seguinte",
     "transfere-se para o 1.º dia útil seguinte"),
]
CONTA = ("primeiro_dia", "conta", "Ao prazo para a {w} no {p} não é aplicável o disposto na alínea b) do artigo {n}.º", "não é aplicável o disposto na alínea b)")
NEGATIVES = ["O prazo para a {w} é de {k} dias a contar da data do envio do convite.",
             "A entidade adjudicante fixa no programa do procedimento o prazo para a {w}, que não pode ser inferior a {k} dias.",
             "O prazo para a {w} é prorrogado por período equivalente ao do atraso, quando as peças não sejam disponibilizadas.",
             "Os concorrentes podem pedir esclarecimentos no primeiro terço do prazo para a {w}."]
FILLERS = ["As notificações previstas no presente Código são feitas através da plataforma eletrónica.",
           "O disposto no presente artigo aplica-se aos procedimentos de formação dos contratos.",
           "A entidade adjudicante publica no portal dos contratos públicos as informações previstas na lei."]


def sentence(rng, field, aspect_text):
    a, val, tmpl, quote = aspect_text
    if field == "todos":
        o, O, d = "o prazo", "Os prazos", "dos prazos"
    else:
        w = rng.choice(FIELDS[field])
        o, O, d = f"o prazo para a {w}", f"Os prazos fixados para a {w}", f"do prazo para a {w}"
    text = tmpl.format(o=o, O=O, d=d) + "."
    return a, val, text[0].upper() + text[1:], quote, (None if field == "todos" else w)


def trained_schema(ctx):
    """The answer schema as v17 was trained on it (aspecto before valor, one object): the protocol puts the value first
    since round 17's second read (D85), after these rows were written; the rows keep the schema they were trained with."""
    sc = v3.schema(ctx, "contagem_prazo", PROTOCOL)
    rule = sc["properties"]["regras"]["items"]
    rule["properties"]["params"] = {"type": "object", "properties": {
        "deadline_field": {"type": "string", "enum": list(v3.V06 and v3.VOC6["deadline_fields"]) + ["todos"]},
        "aspecto": {"type": "string", "enum": list(v3.ASPECTS)},
        "valor": {"type": "string", "enum": sorted({v for vs in v3.ASPECTS.values() for v in vs})}},
        "required": ["deadline_field", "aspecto", "valor"], "additionalProperties": False}
    return sc


def row(rid, ctx, answer, estilo):
    return {"id": f"{TASK}:{rid}", "task": TASK, "prompt": v3.render(ctx, "contagem_prazo", PROTOCOL), "schema": trained_schema(ctx),
            "answer": json.dumps(answer, ensure_ascii=False, separators=(",", ":")), "sources": [], "estilo": estilo}


def written(store=None):
    from engine.store import Store
    store = store or Store([ROOT / "law"]).load()
    law = v3.Law(store)
    exam_texts = [law.text(p, "2026-10-01") for p in ROUND17]
    rng = random.Random(SEED)
    rows, rejected = [], {}
    examples = [("c", k) for k in range(COUNT)] + [("n", k) for k in range(NEGATIVE)]
    for kind, k in examples:
        rid = f"w17-{'contagem' if kind == 'c' else 'nao-contagem'}-{k:03d}"
        cond = []
        if kind == "n":
            field = rng.choice(list(FIELDS))
            w = rng.choice(FIELDS[field])
            target = rng.choice(NEGATIVES).format(w=w, k=rng.choice([5, 6, 9, 12, 15, 20, 30]))
        elif rng.random() < 0.18:  # a procedure of its own: the first day counts (L5 case)
            field = rng.choice(list(FIELDS))
            proc, words = rng.choice(PROCS)
            w = rng.choice(FIELDS[field])
            target = CONTA[2].format(w=w, p=words, n=rng.randint(60, 400)) + "."
            a, val, quote = CONTA[0], CONTA[1], CONTA[3]
            cond = [{"field": "tipo_procedimento", "op": "eq", "value": proc, "fontes": [{"texto": words, "de": None}]}]
        else:
            field = rng.choice(["todos", "todos", "prazo_propostas_dias", "prazo_candidaturas_dias"])
            a, val, target, quote, w = sentence(rng, field, rng.choice(ASPECT_TEXTS))
        texts = [target] if rng.random() < 0.3 else ([rng.choice(FILLERS), target] if rng.random() < 0.5 else [target, rng.choice(FILLERS)])
        ex = v15.article(rid, "contagem_prazo", LUGAR, rng.choice(EPIGRAFES), v15.numbered(texts, False), texts.index(target) + 1, {"regras": []})
        try:
            ctx = v12.ctx_of(ex)
        except (v12.Gap, KeyError, ValueError, IndexError) as e:
            rejected[rid] = f"context: {e}"; continue
        alvo = ctx["alvo"]
        if v12.close(ctx["allowed"][alvo], [t for t in exam_texts if t]):
            rejected[rid] = "close to a round-17 passage"; continue
        if kind == "n":
            answer = {"regras": [], "nao_tipavel": {"motivo": "nao_e_contagem", "fontes": [{"texto": target.rstrip("."), "de": alvo}],
                                                    "falta": "A passagem fixa um prazo, não diz como se contam os seus dias."}}
            estilo = "w17-nao-e-contagem"
        else:
            for c in cond:
                c["fontes"][0]["de"] = alvo
            answer = {"regras": [{"tipo": "contagem_prazo", "condicoes": cond,
                                  "params": {"deadline_field": field, "aspecto": a, "valor": val},
                                  "fontes": {"aspecto": [{"texto": quote, "de": alvo}],
                                             "deadline_field": None if field == "todos" else [{"texto": w, "de": alvo}]}}], "nao_tipavel": None}
            estilo = f"w17-{a}-{val}" + ("-caso" if cond else "")
        errs = v3.check(answer, ctx, "contagem_prazo", PROTOCOL)
        if errs:
            rejected[rid] = f"checker: {errs[0]}"; continue
        rows.append(row(rid, ctx, answer, estilo))
    return rows, rejected


def remind():
    rows = [json.loads(line) for line in (ROOT / "training/data-v16/regra_lida/train.jsonl").read_text(encoding="utf-8").splitlines() if line.strip()]
    return sorted(rows, key=lambda r: hashlib.sha256(r["id"].encode()).hexdigest())[:REMIND]


import make_rule_readings_v16 as v16  # noqa: E402
allowed_sources = v16.allowed_sources  # the remind rows are data-v16's: the same reserved passages they may cite


def generate(store=None, held_doc=None):
    rows, rejected = written(store)
    old = remind()
    files = {"regra_lida/train.jsonl": v13.dump(rows + old),
             "REJECTED.json": (json.dumps(rejected, ensure_ascii=False, indent=1, sort_keys=True) + "\n").encode("utf-8")}
    styles = {}
    for r in rows:
        styles[r["estilo"]] = styles.get(r["estilo"], 0) + 1
    index = {"tool": VERSION, "protocol": PROTOCOL, "written_rows": len(rows), "written_by_style": styles, "remind_rows": len(old), "rejected": len(rejected),
             "exam_left_out": list(ROUND17),
             "files": {k: {"rows": v.count(b"\n"), "sha256": hashlib.sha256(v).hexdigest()} for k, v in sorted(files.items())},
             "note": "D85: the counting of deadlines (contagem_prazo) on invented articles only, and part of data-v16"}
    files["INDEX.json"] = (json.dumps(index, ensure_ascii=False, indent=1) + "\n").encode("utf-8")
    return files


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser(); ap.add_argument("cmd", choices=["check", "generate"])
    a = ap.parse_args()
    if a.cmd == "check":
        rows, rejected = written()
        styles = {}
        for r in rows:
            styles[r["estilo"]] = styles.get(r["estilo"], 0) + 1
        print(f"written {len(rows)}; left out {len(rejected)}; {styles}")
        for k, v in list(rejected.items())[:8]:
            print(" ", k, v)
    else:
        files = generate()
        for rel, b in files.items():
            f = DATA / rel
            f.parent.mkdir(parents=True, exist_ok=True)
            f.write_bytes(b)
        print({k: v for k, v in json.loads(files["INDEX.json"]).items() if k != "files"})
