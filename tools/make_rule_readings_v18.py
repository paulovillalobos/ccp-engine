"""Phase 21 data (DECISIONS D89): data-v18, for v18 trained from v17's adapter: contagem_prazo's two misreadings of
round 17's third read, on invented articles only.

    .venv/bin/python tools/make_rule_readings_v18.py check | generate

- excecao: an article whose n.º 1 says the event's day is not counted and whose target says that rule «não é
  aplicável» to one deadline of one procedure: the target's rule is primeiro_dia conta, with that procedure as its
  condition, whatever the neighbour says (v17 copied the neighbour's nao_conta).
- continuo: an article whose n.º 1 speaks of one procedure and whose target makes two deadlines continuous: one rule
  per deadline and no condition (v17 copied the neighbour's procedure into the target's rule).
- and data-v17 whole (its 434 rows and 600 of data-v16).
Every row passes the 0.6 checker; a target close to a round-17 passage is left out (v12.close). Nothing here calls a model.
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
import make_rule_readings_v17 as v17  # noqa: E402
import read_rules_v3 as v3  # noqa: E402

VERSION = "ccp-make-rule-readings-v18-0.1"
DATA = ROOT / "training/data-v18"
PROTOCOL = v3.V06
EXCECAO, CONTINUO = 180, 180
SEED = "D89"
FIRST = ["Não se inclui na contagem o dia em que se verifica o facto a partir do qual o prazo começa a correr.",
         "Na contagem dos prazos não se inclui o dia em que ocorre o evento que lhes dá início."]
EXC = ["Para a {w} no {p}, não é aplicável o disposto na alínea b) do artigo {n}.º do Código.",
       "No {p}, ao prazo fixado para a {w} não é aplicável o disposto na alínea b) do artigo {n}.º."]
CONT = ["Para a {w1} e para a {w2}, os prazos são contínuos.",
        "No procedimento, os prazos destinados à {w1} e à {w2} são contínuos."]
NEIGH = ["No {p}, a entidade adjudicante fundamenta a urgência na decisão de contratar.",
         "Ao prazo para a {w} no {p} não é aplicável o disposto na alínea b) do artigo {n}.º."]


def answer_rule(field, aspecto, valor, quote, wq, alvo, cond=()):
    return {"tipo": "contagem_prazo", "condicoes": list(cond), "params": {"valor": valor, "aspecto": aspecto, "deadline_field": field},
            "fontes": {"aspecto": [{"texto": quote, "de": alvo}], "deadline_field": [{"texto": wq, "de": alvo}]}}


def written(store=None):
    from engine.store import Store
    store = store or Store([ROOT / "law"]).load()
    law = v3.Law(store)
    exam_texts = [t for t in (law.text(p, "2026-10-01") for p in v17.ROUND17) if t]
    rng = random.Random(SEED)
    rows, rejected = [], {}
    for kind, n in (("excecao", EXCECAO), ("continuo", CONTINUO)):
        for k in range(n):
            rid = f"w18-{kind}-{k:03d}"
            if kind == "excecao":
                field = rng.choice(list(v17.FIELDS)); w = rng.choice(v17.FIELDS[field]); proc, words = rng.choice(v17.PROCS)
                target = rng.choice(EXC).format(w=w, p=words, n=rng.randint(60, 400))
                texts = [rng.choice(FIRST), target]
            else:
                f1, f2 = list(v17.FIELDS)
                w1, w2 = rng.choice(v17.FIELDS[f1]), rng.choice(v17.FIELDS[f2])
                if rng.random() < 0.5:
                    (f1, w1), (f2, w2) = (f2, w2), (f1, w1)
                proc, words = rng.choice(v17.PROCS)
                target = rng.choice(CONT).format(w1=w1, w2=w2)
                texts = [rng.choice(NEIGH).format(w=rng.choice(v17.FIELDS[f1]), p=words, n=rng.randint(60, 400)), target]
            ex = v15.article(rid, "contagem_prazo", v17.LUGAR, rng.choice(v17.EPIGRAFES), v15.numbered(texts, False), 2, {"regras": []})
            try:
                ctx = v12.ctx_of(ex)
            except (v12.Gap, KeyError, ValueError, IndexError) as e:
                rejected[rid] = f"context: {e}"; continue
            alvo = ctx["alvo"]
            if v12.close(ctx["allowed"][alvo], exam_texts):
                rejected[rid] = "close to a round-17 passage"; continue
            if kind == "excecao":
                cond = [{"field": "tipo_procedimento", "op": "eq", "value": proc, "fontes": [{"texto": words, "de": alvo}]}]
                answer = {"regras": [answer_rule(field, "primeiro_dia", "conta", "não é aplicável o disposto na alínea b)", w, alvo, cond)], "nao_tipavel": None}
            else:
                answer = {"regras": [answer_rule(f1, "fins_de_semana", "continuo", "são contínuos", w1, alvo),
                                     answer_rule(f2, "fins_de_semana", "continuo", "são contínuos", w2, alvo)], "nao_tipavel": None}
            errs = v3.check(answer, ctx, "contagem_prazo", PROTOCOL)
            if errs:
                rejected[rid] = f"checker: {errs[0]}"; continue
            rows.append({"id": f"{v17.TASK}:{rid}", "task": v17.TASK, "prompt": v3.render(ctx, "contagem_prazo", PROTOCOL),
                         "schema": v3.schema(ctx, "contagem_prazo", PROTOCOL),
                         "answer": json.dumps(answer, ensure_ascii=False, separators=(",", ":")), "sources": [], "estilo": f"w18-{kind}"})
    return rows, rejected


allowed_sources = v17.allowed_sources


def generate(store=None, held_doc=None):
    rows, rejected = written(store)
    v17_rows = [json.loads(l) for l in (v17.DATA / "regra_lida/train.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
    files = {"regra_lida/train.jsonl": v13.dump(rows + v17_rows),
             "REJECTED.json": (json.dumps(rejected, ensure_ascii=False, indent=1, sort_keys=True) + "\n").encode("utf-8")}
    styles = {}
    for r in rows:
        styles[r["estilo"]] = styles.get(r["estilo"], 0) + 1
    index = {"tool": VERSION, "protocol": PROTOCOL, "written_rows": len(rows), "written_by_style": styles, "v17_rows": len(v17_rows),
             "rejected": len(rejected), "exam_left_out": list(v17.ROUND17),
             "files": {k: {"rows": v.count(b"\n"), "sha256": hashlib.sha256(v).hexdigest()} for k, v in sorted(files.items())},
             "note": "D89: the exception to the first-day rule and two continuous deadlines beside one procedure, on invented articles; and data-v17"}
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
        for k, v in list(rejected.items())[:6]:
            print(" ", k, v)
    else:
        files = generate()
        for rel, b in files.items():
            f = DATA / rel
            f.parent.mkdir(parents=True, exist_ok=True)
            f.write_bytes(b)
        print({k: v for k, v in json.loads(files["INDEX.json"]).items() if k != "files"})
