"""Training tasks for the regime selector (phase 6, DECISIONS D47), generated from law/ by code: no model, no network.

    .venv/bin/python tools/make_regimes.py generate [--out DIR]   training/data-v3/<task>/{train,held_out}.jsonl and
                                                                  INDEX.json (verify TRAIN re-derives them)

entrada_em_vigor   an act's entry-into-force article among other articles of the act -> {"data": the date the act enters
                   into force}; only acts whose own article prints a date equal to the date of the act's entra_em_vigor
                   vigências (D31/D36, from the DR notes); up to 3 examples per act, with different companion articles.
periodos_vigencia  the version history of a passage with more than one version (each version's start and text) -> the
                   partition of time {"periodos": [{"de", "ate", "versao"}]}: one period per version in order, «ate» the
                   day before the next version starts, the last «ate» null (the regimes' convention: contiguous,
                   inclusive, open end).
Not taught on purpose (D47): whether a procedure started on the day of entry into force is before or after; the start
of a first regime before the first version; transitional norms. The reservation of D40 splits both tasks: an example
whose sources touch a reserved article, or whose entry article's text equals a reserved passage's, is held out.
"""
import argparse
import hashlib
import json
import re
import sys
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT)); sys.path.insert(0, str(ROOT / "tools"))
import make_training as mt  # noqa: E402  (the reservation, the passage map and the reader's prompt pieces)
from make_conditions import fold  # noqa: E402
from engine.canon import sha256_text  # noqa: E402

VERSION = "ccp-make-regimes-0.1"
DATA = ROOT / "training/data-v3"
FROZEN_AT = mt.FROZEN_AT
TASKS = ["entrada_em_vigor", "periodos_vigencia"]
PER_ACT = 3
COMPANIONS = 5
MAX_PROMPT_CHARS = mt.MAX_PROMPT_CHARS
DATE = "^[0-9]{4}-[0-9]{2}-[0-9]{2}$"
MONTHS = {m: i for i, m in enumerate(["janeiro", "fevereiro", "marco", "abril", "maio", "junho", "julho", "agosto", "setembro",
                                       "outubro", "novembro", "dezembro"], 1)}
DATE_IN_TEXT = re.compile(r"\b(\d{1,2})\.?º? de (" + "|".join(MONTHS) + r") de (\d{4})\b")
RULES_DATE = "Regras: responde só com o objeto JSON pedido; as datas em formato ISO (ano-mês-dia)."
Q_ENTRADA = "Em que data entra em vigor este diploma, no seu todo? Dê a data."
Q_PERIODOS = ("Divide o tempo de vigência desta passagem em períodos: um período por versão, por ordem; «de» é o dia em que a "
              "versão começa a vigorar, «ate» o dia anterior ao início da versão seguinte e, no último período, null; «versao» "
              "é a data de início da versão.")


def schema_entrada():
    return {"type": "object", "properties": {"data": {"type": "string", "pattern": DATE}}, "required": ["data"], "additionalProperties": False}


def schema_periodos():
    item = {"type": "object", "properties": {"de": {"type": "string", "pattern": DATE},
                                             "ate": {"anyOf": [{"type": "string", "pattern": DATE}, {"type": "null"}]},
                                             "versao": {"type": "string", "pattern": DATE}},
            "required": ["de", "ate", "versao"], "additionalProperties": False}
    return {"type": "object", "properties": {"periodos": {"type": "array", "minItems": 2, "items": item}}, "required": ["periodos"],
            "additionalProperties": False}


def dates_in(text):
    out = set()
    for d, m, y in DATE_IN_TEXT.findall(fold(text)):
        try:
            out.add(date(int(y), MONTHS[m], int(d)).isoformat())
        except ValueError:
            pass
    return out


def entrada(ctx):
    act_date = {}
    for v in ctx.store.objects["vigencia"]:
        if v.get("effect") == "entra_em_vigor" and not v.get("stale"):
            act_date.setdefault(v["passage"].split(":", 1)[0], set()).add(v["valid_from"])
    out = []
    for act in sorted(act_date):
        if len(act_date[act]) != 1:
            continue
        d = next(iter(act_date[act]))
        arts = sorted((pid for pid, p in ctx.passages.items() if pid.split(":", 1)[0] == act and p["kind"] == "artigo"
                       and mt.version_at(p, FROZEN_AT)), key=ctx.order)
        entry = [pid for pid in arts if re.search(r"entra(?:m)? em vigor", fold(mt.version_at(ctx.passages[pid], FROZEN_AT)["text"])[:400])
                 and d in dates_in(mt.version_at(ctx.passages[pid], FROZEN_AT)["text"])]
        if len(entry) != 1:
            continue
        e = entry[0]
        held = ctx.is_reserved(e)
        others = [pid for pid in arts if pid != e and (held or not ctx.is_reserved(pid))
                  and len(mt.version_at(ctx.passages[pid], FROZEN_AT)["text"]) <= mt.MAX_PASSAGE_CHARS]
        for k in range(PER_ACT):
            comp = sorted(others, key=lambda pid: sha256_text(f"entrada|{k}|{pid}"))[:COMPANIONS]
            ids = sorted(comp + [e], key=lambda pid: sha256_text(f"ordem|{k}|{pid}"))
            prompt = mt.compose(RULES_DATE, FROZEN_AT, "entrada_em_vigor", mt.candidate_block(ctx.passages, ids, FROZEN_AT), Q_ENTRADA)
            if len(prompt) > MAX_PROMPT_CHARS:
                continue
            out.append({"task": "entrada_em_vigor", "prompt": prompt, "answer": json.dumps({"data": d}, separators=(",", ":")),
                        "sources": ids, "held": held or any(ctx.is_reserved(x) for x in ids), "schema": schema_entrada()})
    return out


def periodos(ctx):
    out = []
    for pid in sorted(ctx.passages):
        p = ctx.passages[pid]
        vs = sorted(p["versions"], key=lambda v: v["valid_from"])
        if len(vs) < 2 or ".q" in pid:
            continue
        block = [f"[{pid}] histórico de versões:"]
        for v in vs:
            block += [f"Versão em vigor desde {v['valid_from']}:", v["text"], ""]
        prompt = mt.compose(RULES_DATE, FROZEN_AT, "periodos_vigencia", block, Q_PERIODOS)
        if len(prompt) > MAX_PROMPT_CHARS:
            continue
        per = []
        for i, v in enumerate(vs):
            nxt = vs[i + 1]["valid_from"] if i + 1 < len(vs) else None
            per.append({"de": v["valid_from"], "ate": (date.fromisoformat(nxt) - timedelta(days=1)).isoformat() if nxt else None, "versao": v["valid_from"]})
        out.append({"task": "periodos_vigencia", "prompt": prompt, "answer": json.dumps({"periodos": per}, separators=(",", ":")),
                    "sources": [pid], "held": ctx.is_reserved(pid), "schema": schema_periodos()})
    return out


def generate(store, held_doc):
    """{relative path: bytes} of training/data-v3 (INDEX.json included). Pure: same store and reservation -> same bytes."""
    ctx = mt.Ctx(store, held_doc)
    by_prompt = {}
    for ex in entrada(ctx) + periodos(ctx):
        if ex["prompt"] not in by_prompt or (ex["held"] and not by_prompt[ex["prompt"]]["held"]):
            by_prompt[ex["prompt"]] = ex
    examples = sorted(by_prompt.values(), key=lambda e: (e["task"], sha256_text(e["prompt"])))
    files = {}
    index = {"version": VERSION, "frozen_at": FROZEN_AT, "train_held_out_definition_sha256": held_doc.get("sha256"), "tasks": {}, "files": {}}
    for task in TASKS:
        for split in ("train", "held_out"):
            rows = []
            for e in examples:
                if e["task"] != task or e["held"] != (split == "held_out"):
                    continue
                if split == "train" and any(ctx.is_reserved(s) for s in e["sources"]):
                    raise SystemExit(f"{task}: a train example touches a reserved article: {e['sources']}")
                rows.append(json.dumps({"id": f"{task}:{sha256_text(e['prompt'])[:16]}", "task": task, "prompt": e["prompt"], "answer": e["answer"],
                                        "sources": e["sources"], "schema": e["schema"]}, ensure_ascii=False))  # schema keeps its order (D46)
            rel = f"{task}/{split}.jsonl"
            files[rel] = ("\n".join(rows) + ("\n" if rows else "")).encode("utf-8")
            index["tasks"].setdefault(task, {})[split] = len(rows)
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
    print(json.loads(files["INDEX.json"])["tasks"])


if __name__ == "__main__":
    main()
