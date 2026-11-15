"""Phase 22 data (DECISIONS D96): data-v19, for v19 trained from v18's adapter: the agregada type of protocol 0.7, on
invented articles only.

    .venv/bin/python tools/make_rule_readings_v19.py check | generate

- agregada: an invented article that bars inviting entities to which the entity already adjudicated, in a window of
  economic years, contracts under alíneas of other invented articles whose accumulated price reaches a limit those
  alíneas set. Every article says in its own words which earlier contracts count: those under the same alínea as the
  procedure («ao abrigo da mesma alínea») or under any of the alíneas named («ao abrigo de qualquer daquelas alíneas»);
  none uses the words «consoante o caso», so nothing here teaches how CCP art. 113.º n.º 2 reads them (round 18's exam,
  left out with every passage close to it, v12.close).
- nega: an invented article about invitations or accumulated prices that limits no sum (a gift, a publication duty, a
  ceiling on one contract): «não tipável», nao_e_agregada.
- and data-v18 whole (its rows keep the other types).
Every row passes the 0.7 checker. Nothing here calls a model.
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
import make_rule_readings_v18 as v18  # noqa: E402
import read_rules_v3 as v3  # noqa: E402

VERSION = "ccp-make-rule-readings-v19-0.1"
DATA = ROOT / "training/data-v19"
PROTOCOL = v3.V07
TASK = v12.TASK
POSITIVE, NEGATIVE = 360, 120
SEED = "D96"
EXAM = ("ccp:art113.2",)
LUGAR = ["Parte II — Contratação pública", "Capítulo III — Convites"]
EPIGRAFES = ["Limites aos convites", "Entidades que não podem ser convidadas", "Impedimentos de convite", "Restrições à escolha das entidades convidadas"]
# the referred article: its proémio names the contract type, its alíneas the procedures and their limits
CONTRATOS = [("obras", "Para a celebração de contratos de empreitada de obras públicas pode adotar-se:", "empreitada de obras públicas"),
             ("servicos", "Para a celebração de contratos de aquisição de serviços pode adotar-se:", "aquisição de serviços"),
             ("bens", "Para a celebração de contratos de aquisição de bens móveis pode adotar-se:", "aquisição de bens móveis")]
PROCS = [("ajuste_direto", "Ajuste direto"), ("consulta_previa", "Consulta prévia")]
WINDOWS = [(1, "no ano económico em curso", "no ano económico em curso"),
           (2, "no ano económico em curso e no ano económico anterior", "no ano económico em curso e no ano económico anterior"),
           (3, "no ano económico em curso e nos dois anos económicos anteriores", "no ano económico em curso e nos dois anos económicos anteriores"),
           (4, "no ano económico em curso e nos três anos económicos anteriores", "no ano económico em curso e nos três anos económicos anteriores")]
LEADS = [("Não podem ser convidadas", "Não podem ser convidadas"), ("Não pode ser dirigido convite a", "convite"),
         ("A entidade adjudicante não pode convidar", "convidar")]
GROUPS = [("entidades às quais a entidade adjudicante tenha adjudicado", "entidades às quais"),
          ("entidades com as quais a entidade adjudicante tenha celebrado", "entidades com as quais")]
COMPS = [("ge", "igual ou superior ao", "igual ou superior ao"), ("gt", "superior ao", "superior ao")]
FILLERS = ["O convite é enviado em simultâneo a todas as entidades convidadas.",
           "A escolha das entidades convidadas cabe ao órgão competente para a decisão de contratar.",
           "O disposto no presente artigo não prejudica a aplicação das regras sobre conflitos de interesses."]
NEGS = ["Não podem ser convidadas entidades que tenham prestado, a título gratuito, serviços à entidade adjudicante no ano económico em curso.",
        "O preço contratual acumulado dos contratos celebrados com cada entidade no ano económico é publicado no portal dos contratos públicos.",
        "Não podem ser convidadas entidades cujo preço contratual de um único contrato anterior tenha excedido 50 000 €.",
        "A entidade adjudicante comunica ao órgão de fiscalização a lista das entidades convidadas no ano económico em curso."]


def euros(n):
    return f"{n:,}".replace(",", " ") + " €"


def art_num(rid, k):
    return 6000 + int(hashlib.sha256(f"{rid}:{k}".encode()).hexdigest(), 16) % 3000


def positive(rng, rid):
    """(article, gold answer) of one invented cumulative limit."""
    n_t = art_num(rid, "t")
    n_r = art_num(rid, "r")
    if n_r == n_t:
        n_r += 1
    tipo, proemio, tc_words = rng.choice(CONTRATOS)
    k = rng.choice([1, 2, 2, 3])
    letters = "abcde"[:k + 1][1:]  # alíneas b), c), … (a) is a procedure with publication, never referred)
    procs = [rng.choice(PROCS) for _ in letters]
    limits = sorted(rng.sample(range(5, 300), k), reverse=True)
    limits = [x * 1000 for x in limits]
    alineas = [{"n": "1.a", "texto": "a) Concurso público, qualquer que seja o valor do contrato;"}]
    for L, (pv, pw), lim in zip(letters, procs, limits):
        alineas.append({"n": f"1.{L}", "texto": f"{L}) {pw}, quando o valor do contrato for inferior a {euros(lim)};"})
    ref = {"artigo": f"{n_r}.º", "epigrafe": "Escolha do procedimento", "numeros": [{"n": "1", "texto": "1 - " + proemio}] + alineas}
    names = " e ".join(f"{L})" for L in letters) if k > 1 else f"{letters[0]})"
    naming = f"na{'s' if k > 1 else ''} alínea{'s' if k > 1 else ''} {names} do n.º 1 do artigo {n_r}.º"
    same = k > 1 and rng.random() < 0.5
    how = "ao abrigo da mesma alínea" if same else ("ao abrigo de qualquer daquelas alíneas" if k > 1 else "ao abrigo dessa alínea")
    length, wtext, wquote = rng.choice(WINDOWS)
    lead, lquote = rng.choice(LEADS)
    group, gquote = rng.choice(GROUPS)
    comp, ctext, cquote = rng.choice(COMPS)
    target = (f"{lead} {group}, {wtext}, na sequência de procedimentos adotados nos termos do disposto {naming}, contratos {how} cujo preço "
              f"contratual acumulado seja {ctext} limite referido na alínea do procedimento a adotar.")
    texts = [rng.choice(FILLERS), target] if rng.random() < 0.5 else [target, rng.choice(FILLERS)]
    alvo = texts.index(target) + 1
    ex = {"id": rid, "tipo": "agregada", "lugar": LUGAR, "artigo": f"{n_t}.º", "epigrafe": rng.choice(EPIGRAFES),
          "numeros": [{"n": str(i), "texto": f"{i} - {t}"} for i, t in enumerate(texts, 1)], "alvo": str(alvo), "remissoes": [ref]}
    return ex, {"letters": letters, "procs": procs, "limits": limits, "tipo": tipo, "tc_words": tc_words, "n_r": n_r, "same": same, "length": length,
                "wquote": wquote, "lquote": lquote, "gquote": gquote, "comp": comp, "cquote": cquote, "naming": naming}


def gold(ctx, g):
    alvo = ctx["alvo"]
    ref = f"{v12.m.LAW}:art{g['n_r']}"
    rules = []
    for L, (pv, pw), lim in zip(g["letters"], g["procs"], g["limits"]):
        counted = [f"{ref}.1.{L}"] if g["same"] or len(g["letters"]) == 1 else [f"{ref}.1.{x}" for x in g["letters"]]
        rules.append({"tipo": "agregada",
                      "condicoes": [{"field": "tipo_procedimento", "op": "eq", "value": pv, "fontes": [{"texto": pw, "de": f"{ref}.1.{L}"}]},
                                    {"field": "tipo_contrato", "op": "eq", "value": g["tipo"], "fontes": [{"texto": g["tc_words"], "de": f"{ref}.1"}]}],
                      "params": {"window": {"length": g["length"], "unit": "anos_economicos", "anchor": "data_envio_convite"},
                                 "group_key": ["adjudicante", "adjudicatario"], "counts": {"fundamento_em": counted},
                                 "aggregate": {"field": "preco_contratual", "op": "sum", "comparator": g["comp"], "value": lim}},
                      "fontes": {"window": [{"texto": g["wquote"], "de": alvo}], "anchor": [{"texto": g["lquote"], "de": alvo}],
                                 "group_key": [{"texto": "entidade adjudicante", "de": alvo}, {"texto": g["gquote"], "de": alvo}],
                                 "counts": [{"texto": g["naming"].split("disposto ", 1)[-1], "de": alvo}],
                                 "field": [{"texto": "preço contratual acumulado", "de": alvo}], "op": [{"texto": "acumulado", "de": alvo}],
                                 "comparator": [{"texto": g["cquote"], "de": alvo}],
                                 "value": [{"texto": f"inferior a {euros(lim)}", "de": f"{ref}.1.{L}"}]}})
    return {"regras": rules, "nao_tipavel": None}


def written(store=None):
    from engine.store import Store
    store = store or Store([ROOT / "law"]).load()
    law = v3.Law(store)
    exam_texts = [t for d in ("2018-01-01", "2026-10-01") for t in (law.text(p, d) for p in EXAM) if t]
    rng = random.Random(SEED)
    rows, rejected = [], {}
    for k in range(POSITIVE + NEGATIVE):
        kind = "agregada" if k < POSITIVE else "nega"
        rid = f"w19-{kind}-{k:03d}"
        if kind == "agregada":
            ex, g = positive(rng, rid)
        else:
            n_t = art_num(rid, "t")
            target = rng.choice(NEGS)
            texts = [rng.choice(FILLERS), target]
            ex = {"id": rid, "tipo": "agregada", "lugar": LUGAR, "artigo": f"{n_t}.º", "epigrafe": rng.choice(EPIGRAFES),
                  "numeros": [{"n": str(i), "texto": f"{i} - {t}"} for i, t in enumerate(texts, 1)], "alvo": "2"}
        try:
            ctx = v12.ctx_of(ex)
        except (v12.Gap, KeyError, ValueError, IndexError) as e:
            rejected[rid] = f"context: {e}"; continue
        alvo = ctx["alvo"]
        if v12.close(ctx["allowed"][alvo], exam_texts):
            rejected[rid] = "close to the exam (CCP art. 113.º n.º 2)"; continue
        if kind == "agregada":
            answer = gold(ctx, g)
        else:
            answer = {"regras": [], "nao_tipavel": {"motivo": "nao_e_agregada", "fontes": [{"texto": ctx["allowed"][alvo][4:80], "de": alvo}],
                                                     "falta": "a passagem não limita a soma dos contratos já adjudicados a uma mesma entidade num período"}}
        errs = v3.check(answer, ctx, "agregada", PROTOCOL)
        if errs:
            rejected[rid] = f"checker: {errs[0]}"; continue
        rows.append({"id": f"{TASK}:{rid}", "task": TASK, "prompt": v3.render(ctx, "agregada", PROTOCOL), "schema": v3.schema(ctx, "agregada", PROTOCOL),
                     "answer": json.dumps(answer, ensure_ascii=False, separators=(",", ":")), "sources": [], "estilo": f"w19-{kind}" + ("-mesma" if kind == "agregada" and g["same"] else "")})
    return rows, rejected


def generate(store=None):
    rows, rejected = written(store)
    v18_rows = [json.loads(l) for l in (v18.DATA / "regra_lida/train.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
    files = {"regra_lida/train.jsonl": v13.dump(rows + v18_rows),
             "REJECTED.json": (json.dumps(rejected, ensure_ascii=False, indent=1, sort_keys=True) + "\n").encode("utf-8")}
    styles = {}
    for r in rows:
        styles[r["estilo"]] = styles.get(r["estilo"], 0) + 1
    index = {"tool": VERSION, "protocol": PROTOCOL, "written_rows": len(rows), "written_by_style": styles, "v18_rows": len(v18_rows),
             "rejected": len(rejected), "exam_left_out": list(EXAM),
             "files": {k: {"rows": v.count(b"\n"), "sha256": hashlib.sha256(v).hexdigest()} for k, v in sorted(files.items())},
             "note": "D96: the agregada type on invented articles, each saying in its own words which earlier contracts count; never «consoante o caso»; and data-v18"}
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
