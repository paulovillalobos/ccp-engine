"""Phase 13 training data (DECISIONS D63): data-v10, reading a typed rule out of a law passage (task regra_lida).

    .venv/bin/python tools/make_rule_readings.py check      the code checks on every written example, nothing written
    .venv/bin/python tools/make_rule_readings.py generate   training/data-v10

Source: training/rule-readings/batch-*.jsonl, articles written for this project in the CCP's drafting style with their gold
readings (GUIDE.md). No real passage is used: every CCP passage that states a minimum deadline or a value limit is reserved
or a rules-factory target, and the amending decrees quote them word for word; the gold is written from the text, never
from another reader's answer (D43: the families stay independent). Each example becomes a prompt in the layout of
read_rules round 9 (the factory's): the article and its numbers as candidates, the rule vocabulary, the deadline fields
and starting points offered for that example with what each means (the gold's and others, so the reader matches words to
meanings rather than learning a list), the question of tools/rule_factory.py; the answer is {"regras": [...]} in the
schema's key order. About one in three prompts offers exactly the factory's lists, when the gold fits them.

Code checks (an example that fails one is dropped and listed in INDEX.json): the answer validates against its schema; the
cited passages exist and include the alvo; every number of days or euros appears in the cited text; the deadline field,
the starting point, usual_days, JOUE and the new facts each have their words in the cited text (or the heading); no rule
repeats; no written passage is close to a factory target or a settled rule's passage (difflib ratio below LEAK).
Split by sha256 of the id: one in six to held_out (never trained); train has each example twice, with different offered
lists and candidate dates.
"""
import argparse
import difflib
import hashlib
import json
import random
import re
import sys
from pathlib import Path

import jsonschema

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT)); sys.path.insert(0, str(ROOT / "tools"))
import make_training as mt  # noqa: E402
import read_rules as rr  # noqa: E402
import rule_factory as rf  # noqa: E402
from engine.canon import canonical  # noqa: E402
from engine.store import Store  # noqa: E402

VERSION = "ccp-make-rule-readings-0.1"
WRITTEN = ROOT / "training/rule-readings"
DATA = ROOT / "training/data-v10"
TASK = "regra_lida"
SEED = 20261028
DATE = rr.NEW
LAW = "exemplo"
LEAK = 0.85
COPIES = 2
DEADLINES = {
    "prazo_propostas_dias": ("prazo para a apresentação das propostas", r"propostas?\b"),
    "prazo_candidaturas_dias": ("prazo para a apresentação das candidaturas", r"candidaturas?\b"),
    "prazo_trabalhos_concecao_dias": ("prazo para a apresentação dos documentos que materializam os trabalhos de conceção", r"trabalhos de conce[çc][ãa]o"),
    "prazo_solucoes_dias": ("prazo para a apresentação das soluções", r"solu[çc][õo]es"),
    "prazo_esclarecimentos_dias": ("prazo para os pedidos de esclarecimentos", r"esclarecimentos"),
    "prazo_pronuncia_dias": ("prazo para a pronúncia dos interessados em audiência prévia", r"pron[úu]ncia|audi[êe]ncia"),
    "prazo_reclamacao_dias": ("prazo para a reclamação", r"reclam"),
    "prazo_caucao_dias": ("prazo para a prestação da caução", r"cau[çc][ãa]o"),
    "prazo_habilitacao_dias": ("prazo para a apresentação dos documentos de habilitação", r"habilita[çc][ãa]o"),
}
STARTS = {
    "data_envio_anuncio": ("envio do anúncio (ao Serviço das Publicações da União Europeia)", r"envio d[oa][^.;]{0,40}an[úu]ncio|an[úu]ncio[^.;]{0,80}envi"),
    "data_publicacao_anuncio": ("publicação do anúncio", r"publica[çc][ãa]o"),
    "data_envio_convite": ("envio do convite", r"convite"),
    "data_notificacao": ("notificação", r"notifica[çc]"),
    "data_disponibilizacao_pecas": ("disponibilização das peças do procedimento", r"disponibiliza"),
    "nao_indicado": ("a passagem não diz de quando se conta", None),
}
FACTORY_DEADLINES = rr.DEADLINE_FIELDS_9
FACTORY_STARTS = rr.COUNTED_FROM_9
CUES = {"urgencia_fundamentada": r"urg[êe]ncia", "setores_especiais": r"setores|sectores|[áa]gua|energia|transportes|postais",
        "anuncio_pre_informacao": r"indicativo|pr[ée]-informa[çc]", "modalidade_concecao": r"conce[çc][ãa]o",
        "publicado_joue": r"Jornal Oficial da Uni[ãa]o Europeia|JOUE"}
WORDS = {"um": 1, "dois": 2, "três": 3, "quatro": 4, "cinco": 5, "seis": 6, "sete": 7, "oito": 8, "nove": 9, "dez": 10, "onze": 11,
         "doze": 12, "treze": 13, "catorze": 14, "quinze": 15, "dezasseis": 16, "dezassete": 17, "dezoito": 18, "dezanove": 19,
         "vinte": 20, "vinte e cinco": 25, "trinta": 30, "trinta e cinco": 35, "quarenta": 40, "quarenta e cinco": 45,
         "cinquenta": 50, "sessenta": 60, "noventa": 90, "cento e vinte": 120}
SINCE = ["2008-07-29", "2012-03-02", "2017-08-31", "2018-01-01", "2021-06-07", "2023-04-01", "2026-10-01"]


def written():
    rows = []
    for f in sorted(WRITTEN.glob("batch-*.jsonl")):
        rows += [json.loads(l) for l in f.read_text(encoding="utf-8").splitlines() if l.strip()]
    return rows


def slug_art(n):
    return "art" + re.sub(r"[^0-9a-z]+", "-", n.lower().replace("º", "").replace("ª", "").replace(".", "")).strip("-")


def pid_of(ex, path):
    base = f"{LAW}:{slug_art(ex['artigo'])}"
    return base if path == "" else f"{base}.{path}"


def texts(ex):
    """{passage id: text}: the article (heading and every number) and each number or alínea on its own."""
    head = f"Artigo {ex['artigo']}\n{ex['epigrafe']}"
    out = {pid_of(ex, ""): "\n".join([head] + ([ex["texto"]] if not ex["numeros"] else [x["texto"] for x in ex["numeros"]]))}
    for x in ex["numeros"]:
        out[pid_of(ex, x["n"])] = x["texto"]
    return out


def numbers_in(text):
    nums = {int(x.replace(" ", "").replace(".", "")) for x in re.findall(r"\d[\d .]*\d|\d", text)}
    low = text.lower()
    nums |= {v for w, v in WORDS.items() if re.search(rf"\b{w}\b", low)}
    return nums


def answer_obj(ex):
    regras = []
    for r in ex["regras"]:
        p = r["params"]
        if ex["tipo"] == "prazo_minimo":
            params = {"minimum_days": p["minimum_days"], "deadline_field": p["deadline_field"], "counted_from": p["counted_from"],
                      "usual_days": p.get("usual_days")}
        else:
            t = p["threshold"]
            params = {"threshold": {"field": t["field"], "comparator": t["comparator"], "value": t["value"], "currency": t["currency"]}}
        conds = rr.norm_conditions([{"field": c["field"], "op": c["op"], "value": c["value"]} for c in r["condicoes"]])
        regras.append({"passagens": sorted(pid_of(ex, x) for x in set(r["passagens"])), "tipo": ex["tipo"], "condicoes": conds, "params": params})
    return {"regras": regras}


def offered(ex, rng, factory):
    """The deadline fields and starting points this prompt offers: the factory's lists, or the gold's plus others."""
    if ex["tipo"] != "prazo_minimo":
        return [], []
    gold_d = {r["params"]["deadline_field"] for r in ex["regras"]}
    gold_s = {r["params"]["counted_from"] for r in ex["regras"]}
    if factory and gold_d <= set(FACTORY_DEADLINES) and gold_s <= set(FACTORY_STARTS):
        return list(FACTORY_DEADLINES), list(FACTORY_STARTS)
    d = sorted(gold_d | set(rng.sample(sorted(set(DEADLINES) - gold_d), rng.randint(1, 3))))
    s = sorted(gold_s | set(rng.sample(sorted(set(STARTS) - gold_s - {"nao_indicado"}), rng.randint(1, 3))) | {"nao_indicado"})
    rng.shuffle(d); rng.shuffle(s)
    return d, s


def prompt(ex, cands, tx, rng, d, s):
    t = {"type": ex["tipo"], "candidates": cands, "date": DATE}
    lines = ["És um leitor da lei portuguesa. Lê as passagens candidatas e responde à pergunta com um objeto JSON e nada mais.",
             "Regras: escolhe em «passagens» os ids das passagens que fundamentam a resposta (só ids da lista, nunca texto); "
             "«condicoes» são condições sobre factos do procedimento; usa só estes campos e valores:",
             "  " + "; ".join(f"{k}: {', '.join(json.dumps(v, ensure_ascii=False) for v in vals)}" for k, vals in rr.VOCAB_9.items())
             + "; preco_base: número em euros; data_inicio_procedimento: uma data no formato ISO (ano-mês-dia).",
             f"Data de referência: {DATE}. Tipo de regra pedido: {ex['tipo']}.", "", "Passagens candidatas:"]
    for pid in cands:
        lines += [f"[{pid}] (versão em vigor a {DATE}, desde {rng.choice(SINCE)})", tx[pid], ""]
    if ex["tipo"] == "prazo_minimo":
        lines += ["Campos do prazo: " + "; ".join(f"{k} = {DEADLINES[k][0]}" for k in d) + ". Início da contagem: "
                  + "; ".join(f"{k} = {STARTS[k][0]}" for k in s) + ".",
                  "Factos: urgencia_fundamentada = a entidade adjudicante fundamentou uma situação de urgência; setores_especiais = o "
                  "contrato diz direta e principalmente respeito a atividades dos setores da água, da energia, dos transportes ou dos "
                  "serviços postais; anuncio_pre_informacao = foi publicado o anúncio periódico indicativo; modalidade_concecao = a "
                  "modalidade do concurso de conceção. «minimum_days» é o mínimo abaixo do qual o prazo nunca pode ficar; «usual_days» é "
                  "o prazo que a passagem fixa «em regra» quando fixa também esse mínimo absoluto, e null quando não fixa.",
                  "Se a passagem fixa mais de uma regra (casos diferentes com prazos diferentes), dá uma regra por caso em «regras»; "
                  "senão, uma só.", ""]
    lines += ["Pergunta: " + rf.QUESTION[ex["tipo"]].format(pid=pid_of(ex, ex["alvo"]))]
    schema = rr.schema_for(t, 9)
    if ex["tipo"] == "prazo_minimo":
        props = schema["properties"]["regras"]["items"]["properties"]["params"]["properties"]
        props["deadline_field"]["enum"] = d
        props["counted_from"]["enum"] = s
    return "\n".join(lines), schema


def problems(ex, refs):
    """What the code checks find wrong in one written example (GUIDE.md); [] when it passes."""
    out = []
    try:
        paths = {""} | {x["n"] for x in ex["numeros"]}
        if ex["tipo"] not in ("prazo_minimo", "limiar"):
            return [f"tipo {ex['tipo']}"]
        if ex["alvo"] not in paths:
            return [f"alvo {ex['alvo']!r} not a path"]
        if not 1 <= len(ex["regras"]) <= 3:
            return [f"{len(ex['regras'])} rules"]
        tx = texts(ex)
        cands = sorted(tx)
        ans = answer_obj(ex)
        d, s = offered(ex, random.Random(0), False)
        _, schema = prompt(ex, cands, tx, random.Random(0), d, s)
        jsonschema.validate(ans, schema)
    except (KeyError, TypeError, AttributeError) as exc:
        return [f"malformed: {exc!r}"]
    except jsonschema.ValidationError as exc:
        return [f"schema: {exc.message[:160]}"]
    head = ex["epigrafe"]
    seen = set()
    for i, r in enumerate(ex["regras"]):
        if not set(r["passagens"]) <= paths:
            out.append(f"rule {i}: passage outside the article"); continue
        if ex["alvo"] not in r["passagens"]:
            out.append(f"rule {i}: does not cite the alvo")
        cited = "\n".join(tx[pid_of(ex, x)] for x in r["passagens"])
        nums = numbers_in(cited)
        p = r["params"]
        if ex["tipo"] == "prazo_minimo":
            for k in ("minimum_days", "usual_days"):
                if p.get(k) is not None and p[k] not in nums:
                    out.append(f"rule {i}: {k} {p[k]} not in the cited text")
            above = "\n".join(tx[pid_of(ex, x.rsplit(".", 1)[0])] for x in r["passagens"] if "." in x)  # an alínea's number
            if not re.search(DEADLINES[p["deadline_field"]][1], cited + "\n" + above + "\n" + head, re.I):
                out.append(f"rule {i}: {p['deadline_field']} has no words in the text")
            cue = STARTS[p["counted_from"]][1]
            if cue and not re.search(cue, cited, re.I):
                out.append(f"rule {i}: {p['counted_from']} has no words in the cited text")
            if p.get("usual_days") is not None and (not re.search(r"em regra", cited, re.I) or p["usual_days"] <= p["minimum_days"]):
                out.append(f"rule {i}: usual_days without «em regra» or not above the minimum")
            if p.get("usual_days") is None and re.search(r"em regra[^.;]{0,160}em caso algum", tx[pid_of(ex, ex["alvo"])], re.I):
                out.append(f"rule {i}: «em regra … em caso algum» without usual_days")
        else:
            v = p["threshold"]["value"]
            if v not in nums and not re.search(r"\bmil\b|milh", cited, re.I):
                out.append(f"rule {i}: threshold {v} not in the cited text")
        for c in r["condicoes"]:
            if c["field"] in CUES and not re.search(CUES[c["field"]], cited + "\n" + head + "\n" + tx[pid_of(ex, "")], re.I):
                out.append(f"rule {i}: condition {c['field']} has no words in the text")
        key = canonical(rr.canonical_reading({"passages": r["passagens"], "type": ex["tipo"], "conditions": r["condicoes"], "params": p}))
        if key in seen:
            out.append(f"rule {i}: repeats another rule")
        seen.add(key)
    for pid, t in tx.items():
        if pid == pid_of(ex, ""):
            continue
        near = max((difflib.SequenceMatcher(None, t, x).ratio() for x in refs if abs(len(x) - len(t)) < 0.5 * len(t)), default=0)
        if near >= LEAK:
            out.append(f"{pid}: close to a real target passage ({near:.2f})")
    return out


def reference_texts(store):
    """The real passages the examples must not copy: the factory's targets and the settled rules' passages."""
    store_l = store or Store([ROOT / "law", ROOT / "rules", ROOT / "governance"]).load()
    pids = {t["source_passage"] for t in rf.targets(store_l)}
    pids |= {c["passage"] for r in store_l.objects.get("regra", []) for c in r.get("passages", [])}
    out = []
    for pid in sorted(pids):
        p = store_l.current(pid)
        v = rr.version_at(p, DATE) if p else None
        if v:
            out.append(v["text"])
    return out


def row(ex, rng, factory):
    tx = texts(ex)
    cands = sorted(tx)
    d, s = offered(ex, rng, factory)
    text, schema = prompt(ex, cands, tx, rng, d, s)
    return {"id": f"{TASK}:{ex['id']}", "task": TASK, "prompt": text, "schema": schema,
            "answer": json.dumps(answer_obj(ex), ensure_ascii=False, separators=(",", ":")), "sources": [], "estilo": ex.get("estilo")}


def generate(store=None, held_doc=None):
    """{relative path: bytes} of training/data-v10. Pure: same written examples, store and code -> same bytes."""
    refs = reference_texts(store)
    rows = written()
    dropped = {ex.get("id", "?"): pr for ex in rows for pr in [problems(ex, refs)] if pr}
    good = [ex for ex in rows if ex.get("id") not in dropped]
    rng = random.Random(SEED)
    parts = {"held_out": [], "train": []}
    for ex in good:
        dev = int(hashlib.sha256(ex["id"].encode()).hexdigest(), 16) % 6 == 0
        if dev:
            parts["held_out"].append(row(ex, rng, factory=rng.random() < 0.5))
        else:
            parts["train"] += [row(ex, rng, factory=(k == 0 and rng.random() < 0.6)) for k in range(COPIES)]
    files, index = {}, {"version": VERSION, "seed": SEED, "split": {}, "files": {}, "dropped": dropped}
    for name, rs in parts.items():
        rel = f"{TASK}/{name}.jsonl"
        files[rel] = ("\n".join(json.dumps(r, ensure_ascii=False) for r in rs) + "\n").encode("utf-8")
        index["split"][name] = len(rs)
    for rel in sorted(files):
        index["files"][rel] = {"sha256": hashlib.sha256(files[rel]).hexdigest(), "lines": files[rel].count(b"\n")}
    files["INDEX.json"] = (json.dumps(index, ensure_ascii=False, sort_keys=True, indent=1) + "\n").encode("utf-8")
    return files


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["check", "generate"]); ap.add_argument("--out", default=str(DATA))
    a = ap.parse_args()
    if a.cmd == "check":
        refs = reference_texts(None)
        rows = written()
        bad = [(ex.get("id"), pr) for ex in rows for pr in [problems(ex, refs)] if pr]
        for i, pr in bad:
            print(i, "|", "; ".join(pr))
        print(f"{len(rows)} examples, {len(bad)} with problems")
        return
    files = generate()
    mt.write(files, Path(a.out))
    idx = json.loads(files["INDEX.json"])
    print(idx["split"], f"dropped {len(idx['dropped'])}")


if __name__ == "__main__":
    main()
