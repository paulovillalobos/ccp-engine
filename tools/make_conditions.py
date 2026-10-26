"""Training task condicoes_texto (phase 5, DECISIONS D46), generated from law/ by code: no model, no network.

    .venv/bin/python tools/make_conditions.py generate [--out DIR]   training/data-v2/condicoes_texto/{train,held_out}.jsonl
                                                                     and INDEX.json (verify TRAIN re-derives them)

One passage in force at FROZEN_AT (an article, número or alínea; not a validity note; at most MAX_PASSAGE_CHARS) and the
question «which vocabulary values does this passage name expressly». The answer is, per field, the set of values whose
term the text contains, and whether it names the Jornal Oficial da União Europeia. The label is lexical by design:
LEXICON decides it (accent-folded, word-bounded), so the task teaches naming what the text names and nothing it does
not. Only the acts of public procurement (PROCUREMENT_ACTS). Passages that name nothing are negatives, at most one per two positives, chosen by sha256. The reservation of D40
(law/TRAIN-HELD-OUT.json) splits it: an example from a reserved article, or whose text is a reserved passage's text (a
republication of the CCP inside an amending act), goes to held_out, never to train.
"""
import argparse
import hashlib
import json
import re
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT)); sys.path.insert(0, str(ROOT / "tools"))
import make_training as mt  # noqa: E402  (the reservation, the passage map and the reader's prompt pieces)
from engine.canon import sha256_text  # noqa: E402

VERSION = "ccp-make-conditions-0.1"
DATA = ROOT / "training/data-v2"
TASK = "condicoes_texto"
FROZEN_AT = mt.FROZEN_AT
MAX_PASSAGE_CHARS = mt.MAX_PASSAGE_CHARS
VOCAB_CONTRATO = ["obras", "bens", "servicos", "concessao_obras", "concessao_servicos", "servicos_sociais"]
VOCAB_PROCEDIMENTO = ["ajuste_direto", "consulta_previa", "concurso_publico", "concurso_limitado_previa_qualificacao",
                      "procedimento_negociacao", "dialogo_concorrencial", "parceria_inovacao"]
VOCAB_TERRITORIO = ["PT-AC", "PT-MA"]
# term -> value; matched on the accent-folded, lower-cased text, word-bounded (D46). Order does not matter: a value is in
# the answer when any of its terms is in the text.
LEXICON = {
    "tipo_procedimento": [
        (r"ajustes? diretos?", "ajuste_direto"),
        (r"consultas? previas?(?! simplificad)", "consulta_previa"),
        (r"concursos? publicos?", "concurso_publico"),
        (r"concursos? limitados? por previa qualificacao", "concurso_limitado_previa_qualificacao"),
        (r"procedimentos? de negociacao", "procedimento_negociacao"),
        (r"dialogos? concorrencia(?:l|is)", "dialogo_concorrencial"),
        (r"parcerias? para a inovacao", "parceria_inovacao"),
    ],
    "tipo_contrato": [
        (r"empreitadas?", "obras"),
        (r"(?:locac(?:ao|oes)|aquisic(?:ao|oes))(?: ou (?:locacao|aquisicao))? de bens(?: moveis)?", "bens"),
        (r"aquisic(?:ao|oes) de servicos", "servicos"),
        (r"prestac(?:ao|oes) de servicos", "servicos"),
        (r"bens(?: moveis)? (?:e|ou) (?:de )?servicos", "servicos"),
        (r"bens(?: moveis)? (?:e|ou) (?:de )?servicos", "bens"),
        (r"concess(?:ao|oes) de obras publicas", "concessao_obras"),
        (r"concess(?:ao|oes) de servicos(?: publicos)?", "concessao_servicos"),  # «concessão de serviços» since DL 177/2026
        (r"servicos sociais", "servicos_sociais"),
    ],
    "territorio": [
        (r"acores", "PT-AC"),
    ],
}
# the acts of public procurement (D46): the CCP, the acts that approve or amend it, the special and regional regimes and
# the portarias it delegates to; other codes in law/ (labour, civil, penal...) use the same words for other things
PROCUREMENT_ACTS = {"ccp", "dl-18-2008", "dl-111-b-2017", "dl-177-2026", "lei-30-2021", "dl-60-2018", "dl-197-1999", "dlr-27-2015-a",
                    "dlr-34-2008-m", "port-318-a-2023", "port-318-b-2023", "port-371-2017", "port-372-2017"}
MADEIRA = re.compile(r"\bMadeira\b")  # capitalised only: «madeira» is also wood
JOUE = r"jornal oficial da uniao europeia"
RULES_LINE = ("Regras: responde só com valores destes vocabulários, e só os que o texto nomeia expressamente: tipo_contrato: "
              + ", ".join(json.dumps(v) for v in VOCAB_CONTRATO) + "; tipo_procedimento: " + ", ".join(json.dumps(v) for v in VOCAB_PROCEDIMENTO)
              + "; territorio: \"PT-AC\" (Região Autónoma dos Açores), \"PT-MA\" (Região Autónoma da Madeira).")
QUESTION = ("Que valores do vocabulário nomeia expressamente esta passagem? Para cada campo, a lista dos valores cujo termo o texto "
            "contém (lista vazia se não nomeia nenhum); menciona_joue: se o texto nomeia o Jornal Oficial da União Europeia.")


def fold(text):
    return "".join(c for c in unicodedata.normalize("NFD", text.lower()) if unicodedata.category(c) != "Mn")


def label(text):
    """The values the text names, by field (sorted lists), and menciona_joue; keys in the schema's order."""
    t = fold(text)
    out = {}
    for field in ("menciona_joue", "territorio", "tipo_contrato", "tipo_procedimento"):
        if field == "menciona_joue":
            out[field] = re.search(r"\b" + JOUE + r"\b", t) is not None
            continue
        vals = {v for pat, v in LEXICON.get(field, []) if re.search(r"\b" + pat + r"\b", t)}
        if field == "territorio" and MADEIRA.search(text):
            vals.add("PT-MA")
        out[field] = sorted(vals)
    return out


def schema():
    def arr(enum):
        return {"type": "array", "items": {"type": "string", "enum": enum}}
    return {"type": "object", "properties": {"menciona_joue": {"type": "boolean"}, "territorio": arr(VOCAB_TERRITORIO),
                                             "tipo_contrato": arr(VOCAB_CONTRATO), "tipo_procedimento": arr(VOCAB_PROCEDIMENTO)},
            "required": ["menciona_joue", "territorio", "tipo_contrato", "tipo_procedimento"], "additionalProperties": False}


def generate(store, held_doc):
    """{relative path: bytes} of training/data-v2 (INDEX.json included). Pure: same store and reservation -> same bytes."""
    ctx = mt.Ctx(store, held_doc)
    # a passage whose text is a reserved passage's text (a republication of the CCP inside an amending act) is held out too
    reserved_texts = set()
    for pid, p in ctx.passages.items():
        v = mt.version_at(p, FROZEN_AT)
        if v and ctx.is_reserved(pid):
            reserved_texts.add(fold(v["text"]).strip())
    pos, neg = [], []
    for pid in sorted(ctx.passages):
        p = ctx.passages[pid]
        if p["kind"] not in ("artigo", "numero", "alinea") or ".q" in pid or pid.split(":", 1)[0] not in PROCUREMENT_ACTS:
            continue
        v = mt.version_at(p, FROZEN_AT)
        if v is None or not v["text"].strip() or len(v["text"]) > MAX_PASSAGE_CHARS or mt.is_note_text(v["text"]):
            continue
        lab = label(v["text"])
        prompt = mt.compose(RULES_LINE, FROZEN_AT, TASK, mt.candidate_block(ctx.passages, [pid], FROZEN_AT), QUESTION)
        held = ctx.is_reserved(pid) or fold(v["text"]).strip() in reserved_texts
        ex = {"pid": pid, "prompt": prompt, "answer": json.dumps(lab, ensure_ascii=False, separators=(",", ":")), "held": held}
        (pos if any(lab[k] for k in lab) else neg).append(ex)
    neg.sort(key=lambda e: sha256_text("neg|" + e["pid"]))
    keep = pos + neg[: len(pos) // 2]
    by_prompt = {}
    for ex in keep:  # dedupe by prompt; a prompt seen with a reserved passage stays in held_out only
        if ex["prompt"] not in by_prompt or (ex["held"] and not by_prompt[ex["prompt"]]["held"]):
            by_prompt[ex["prompt"]] = ex
    examples = sorted(by_prompt.values(), key=lambda e: sha256_text(e["prompt"]))
    files = {}
    index = {"version": VERSION, "task": TASK, "frozen_at": FROZEN_AT, "train_held_out_definition_sha256": held_doc.get("sha256"),
             "positives": len(pos), "negatives_available": len(neg), "negatives_kept": len(keep) - len(pos), "files": {}, "split": {}}
    sch = schema()
    for split in ("train", "held_out"):
        rows = []
        for e in examples:
            if e["held"] != (split == "held_out"):
                continue
            if split == "train" and (ctx.is_reserved(e["pid"]) or e["held"]):
                raise SystemExit(f"{TASK}: a train example touches a reserved article: {e['pid']}")
            rows.append(json.dumps({"id": f"{TASK}:{sha256_text(e['prompt'])[:16]}", "task": TASK, "prompt": e["prompt"], "answer": e["answer"],
                                    "sources": [e["pid"]], "schema": sch}, ensure_ascii=False))  # no sort_keys: the schema keeps its order (D46)
        rel = f"{TASK}/{split}.jsonl"
        files[rel] = ("\n".join(rows) + ("\n" if rows else "")).encode("utf-8")
        index["split"][split] = len(rows)
    for rel in sorted(files):
        index["files"][rel] = {"sha256": hashlib.sha256(files[rel]).hexdigest(), "lines": files[rel].count(b"\n")}
    files["INDEX.json"] = (json.dumps(index, ensure_ascii=False, sort_keys=True, indent=1) + "\n").encode("utf-8")
    return files


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["generate"]); ap.add_argument("--out", default=str(DATA))
    a = ap.parse_args()
    store = mt.load_repo()
    held = json.loads(mt.HELD.read_text(encoding="utf-8"))
    files = generate(store, held)
    mt.write(files, Path(a.out))
    print(json.loads(files["INDEX.json"]))


if __name__ == "__main__":
    main()
