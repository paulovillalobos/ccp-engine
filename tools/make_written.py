"""Training task factos_v6 (phase 9, DECISIONS D52), built by code from the written questions: no model, no network.

    .venv/bin/python tools/make_written.py generate [--out DIR]   training/data-v6/factos_v6/{train,held_out,final}.jsonl, INDEX.json

Source: training/written-questions/batch-*.jsonl (500 questions written one by one, labelled by LABELS.md) and the
train split of training/data-v5 (D50, template questions). Split of the written questions by sha256 of the id: 100
final (sealed: measured only at milestones), 100 held_out (dev), 300 train. Every train question appears clean and in
NOISY_COPIES noisy copies; a noise operator changes letters, case, punctuation, spelling or shorthand and never a
number, a date or a fact, so the label is unchanged. 2 000 of D50's template questions, re-labelled in this answer
format, each with one noise style. held_out and final are clean: they are what was written.

The answer: {"factos", "ambiguos", "contraditorios", "citacoes"} (LABELS.md); facts in a fixed field order.
"""
import argparse
import hashlib
import json
import random
import re
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT)); sys.path.insert(0, str(ROOT / "tools"))
import make_training as mt  # noqa: E402
import read_rules  # noqa: E402  (the engine's fact vocabulary)
from engine.canon import sha256_text  # noqa: E402

VERSION = "ccp-make-written-0.1"
DATA = ROOT / "training/data-v6"
WRITTEN = ROOT / "training/written-questions"
V5_TRAIN = ROOT / "training/data-v5/factos_utilizador/train.jsonl"
TASK = "factos_v6"
SEED = 20261028
N_FINAL, N_DEV = 100, 100
NOISY_COPIES = 5
N_TEMPLATE = 2000
FIELDS = ["tipo_entidade", "tipo_procedimento", "tipo_contrato", "territorio", "preco_base", "publicado_joue", "data_inicio_procedimento"]
OPENING = "És um leitor de perguntas sobre contratação pública. Lê a pergunta e responde com um objeto JSON e nada mais."
RULES_LINE = ("Regras: em «factos» põe só os factos do procedimento que a pergunta afirma, com estes campos e valores: "
              + "; ".join(f"{k}: {', '.join(json.dumps(v, ensure_ascii=False) for v in vals)}" for k, vals in read_rules.VOCAB.items())
              + "; preco_base: número em euros, só quando a pergunta diz preço base; data_inicio_procedimento: data ISO (ano-mês-dia) "
              "em que o procedimento começa. Um facto que a pergunta não afirma fica de fora; não o deduzas nem o adivinhes. "
              "Em «ambiguos» põe o campo que a pergunta refere de forma que admite mais de um valor, com a lista dos candidatos "
              "(um valor dito por outras palavras, como «valor», «orçamento» ou «com IVA», vai para ambiguos.preco_base). Em "
              "«contraditorios» o campo para o qual a pergunta dá dois valores. Em «citacoes» os artigos e diplomas que a pergunta "
              "cita, certos ou errados, como ids (ccp:art22, ccp:art20.1.d, dl-177-2026). O que a pergunta afirma sobre a lei não é um facto.")

ACCENTS = str.maketrans("áàâãéêíóôõúçÁÀÂÃÉÊÍÓÔÕÚÇ", "aaaaeeiooouCAAAAEEIOOOUC".replace("C", "c", 1))
KEYS = ["qwertyuiop", "asdfghjklç", "zxcvbnm"]
NEAR = {c: "".join(row[j] for j in (i - 1, i + 1) if 0 <= j < len(row)) for row in KEYS for i, c in enumerate(row)}
PRE_AO = [(r"\b([Dd])ireto\b", r"\1irecto"), (r"\b([Dd])ireta\b", r"\1irecta"), (r"\bação\b", "acção"), (r"\bações\b", "acções"),
          (r"\batua(l|is|lmente)\b", r"actua\1"), (r"\bprojeto(s?)\b", r"projecto\1"), (r"\bobjeto(s?)\b", r"objecto\1"),
          (r"\befetua", "efectua"), (r"\belétric", "eléctric"), (r"\beletrónic", "electrónic"), (r"\badotar\b", "adoptar"),
          (r"\bsetembro\b", "Setembro"), (r"\boutubro\b", "Outubro"), (r"\bnovembro\b", "Novembro"), (r"\bdiretor", "director"),
          (r"\bdireção\b", "direcção"), (r"\bproteção\b", "protecção"), (r"\bcoletiv", "colectiv"), (r"\bexato(s?)\b", r"exacto\1")]
SHORT = [("concurso público", "CP"), ("Concurso público", "CP"), ("ajuste direto", "AD"), ("Ajuste direto", "AD"), ("preço base", "PB"),
         ("Jornal Oficial da União Europeia", "JOUE"), ("concurso limitado por prévia qualificação", "CLPQ"), (" que ", " q "),
         (" para ", " p/ "), (" com ", " c/ "), (" sem ", " s/ "), (" também ", " tb "), (" porque ", " pq "), ("número", "nº")]
STYLES = [("cuidado", 0.25), ("casual", 0.35), ("ditado", 0.15), ("pre_ao", 0.15), ("abreviado", 0.10)]


def answer(q):
    f = q.get("factos") or {}
    return json.dumps({"factos": {k: f[k] for k in FIELDS if k in f}, "ambiguos": {k: q["ambiguos"][k] for k in FIELDS if k in (q.get("ambiguos") or {})},
                       "contraditorios": {k: q["contraditorios"][k] for k in FIELDS if k in (q.get("contraditorios") or {})},
                       "citacoes": list(q.get("citacoes") or [])}, ensure_ascii=False, separators=(",", ":"))


def prompt(question, today):
    return "\n".join([OPENING, RULES_LINE, f"Data de hoje: {today}.", "", "Pergunta: " + question])


def schema():
    one = {k: {"type": "string", "enum": v} for k, v in read_rules.VOCAB.items() if k != "publicado_joue"}
    one.update(publicado_joue={"type": "boolean"}, preco_base={"type": "number"},
               data_inicio_procedimento={"type": "string", "pattern": "^[0-9]{4}-[0-9]{2}-[0-9]{2}$"})
    vals = {k: one[k] for k in FIELDS}  # the answer's order: a guided decoder writes properties in schema order (D46)
    many = {"type": "array", "minItems": 1, "items": {"anyOf": [{"type": "string"}, {"type": "number"}, {"type": "boolean"}]}}
    obj = lambda props: {"type": "object", "properties": props, "additionalProperties": False}  # noqa: E731
    return {"type": "object", "properties": {"factos": obj(vals), "ambiguos": obj({k: many for k in FIELDS}),
                                             "contraditorios": obj({k: {**many, "minItems": 2, "maxItems": 2} for k in FIELDS}),
                                             "citacoes": {"type": "array", "items": {"type": "string"}}},
            "required": ["factos", "ambiguos", "contraditorios", "citacoes"], "additionalProperties": False}


# ---- noise: letters, case, punctuation, spelling, shorthand; never a digit ----------------------------------------
def strip_accents(text, rng, p):
    return "".join(c.translate(ACCENTS) if c in "áàâãéêíóôõúçÁÀÂÃÉÊÍÓÔÕÚÇ" and rng.random() < p else c for c in text)


def typo(word, rng):
    if len(word) < 4 or any(ch.isdigit() for ch in word):
        return word
    i = rng.randrange(1, len(word) - 1)
    op = rng.choice(["omit", "omit", "double", "near", "swap"])
    if op == "omit":
        return word[:i] + word[i + 1:]
    if op == "double":
        return word[:i] + word[i] + word[i:]
    if op == "near" and NEAR.get(word[i].lower()):
        return word[:i] + rng.choice(NEAR[word[i].lower()]) + word[i + 1:]
    return word[:i] + word[i + 1] + word[i] + word[i + 2:]


def typos(text, rng, per100):
    words = text.split(" ")
    for j in range(len(words)):
        if rng.random() < per100 / 100:
            words[j] = typo(words[j], rng)
    return " ".join(words)


def noisy(text, style, rng):
    if style == "cuidado":
        return typos(strip_accents(text, rng, 0.15), rng, 2)
    if style == "casual":
        t = typos(strip_accents(text, rng, 0.6), rng, 5).lower()
        t = re.sub(r"[.!]\s*$", "", t)
        return re.sub(r"\?$", rng.choice(["?", "??", ""]), t)
    if style == "ditado":
        t = strip_accents(text, rng, 0.5).lower()
        return re.sub(r"\s+", " ", re.sub(r"[,.;:!?()«»\"]", " ", t)).strip()
    if style == "pre_ao":
        for a, b in PRE_AO:
            text = re.sub(a, b, text)
        return typos(text, rng, 1)
    for a, b in SHORT:
        if rng.random() < 0.7:
            text = text.replace(a, b)
    return typos(strip_accents(text, rng, 0.3), rng, 2)


def pick_style(rng):
    x, acc = rng.random(), 0.0
    for s, w in STYLES:
        acc += w
        if x < acc:
            return s
    return STYLES[-1][0]


# ---- the split and the files ----------------------------------------------------------------------------------------
BATCHES = [f"batch-{i:02d}.jsonl" for i in range(1, 11)]  # v6 was trained on these 500; later batches belong to later versions


def written():
    rows = []
    for f in [WRITTEN / b for b in BATCHES]:
        rows += [json.loads(l) for l in f.read_text(encoding="utf-8").splitlines() if l.strip()]
    return rows


def split(rows):
    order = sorted(rows, key=lambda q: sha256_text(f"{SEED}|{q['id']}"))
    return {"final": order[:N_FINAL], "held_out": order[N_FINAL:N_FINAL + N_DEV], "train": order[N_FINAL + N_DEV:]}


def row(q, text, source, style=None):
    p = prompt(text, q["hoje"])
    r = {"id": f"{TASK}:{sha256_text(p)[:16]}", "task": TASK, "prompt": p, "answer": answer(q), "sources": [], "schema": schema(),
         "written_id": q["id"], "source": source}
    if style:
        r["noise"] = style
    return r


def template_rows(rng):
    out = []
    lines = [json.loads(l) for l in V5_TRAIN.read_text(encoding="utf-8").splitlines() if l.strip()]
    for ex in sorted(lines, key=lambda e: sha256_text(f"{SEED}|t|{e['id']}"))[:N_TEMPLATE]:
        question = ex["prompt"].split("Pergunta: ", 1)[1]
        today = ex["prompt"].split("Data de hoje: ", 1)[1][:10]
        q = {"id": ex["id"], "hoje": today, "factos": json.loads(ex["answer"])["factos"]}
        style = pick_style(rng)
        out.append(row(q, noisy(question, style, rng), "template-d50", style))
    return out


def generate(store=None, held_doc=None):
    """{relative path: bytes} of training/data-v6. Pure: same written questions and code -> same bytes."""
    parts = split(written())
    rng = random.Random(SEED)
    files, index = {}, {"version": VERSION, "seed": SEED, "split": {}, "files": {}, "written": {k: [q["id"] for q in v] for k, v in parts.items()}}
    seen = set()
    for name in ("final", "held_out", "train"):
        rows = []
        for q in parts[name]:
            variants = [row(q, q["pergunta"], "written")]
            if name == "train":
                for _ in range(NOISY_COPIES):
                    style = pick_style(rng)
                    variants.append(row(q, noisy(q["pergunta"], style, rng), "written", style))
            for r in variants:
                if r["prompt"] not in seen:
                    seen.add(r["prompt"])
                    rows.append(r)
        if name == "train":
            rows += [r for r in template_rows(rng) if r["prompt"] not in seen]
        rel = f"{TASK}/{name}.jsonl"
        files[rel] = ("\n".join(json.dumps(r, ensure_ascii=False) for r in rows) + "\n").encode("utf-8")
        index["split"][name] = len(rows)
    for rel in sorted(files):
        index["files"][rel] = {"sha256": hashlib.sha256(files[rel]).hexdigest(), "lines": files[rel].count(b"\n")}
    files["INDEX.json"] = (json.dumps(index, ensure_ascii=False, sort_keys=True, indent=1) + "\n").encode("utf-8")
    return files


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["generate"]); ap.add_argument("--out", default=str(DATA))
    a = ap.parse_args()
    files = generate()
    mt.write(files, Path(a.out))
    print(json.loads(files["INDEX.json"])["split"])


if __name__ == "__main__":
    main()
