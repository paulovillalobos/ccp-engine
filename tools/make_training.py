"""Training data for the reader, generated from law/ by code: no model, no network, no text that is not in law/.

    .venv/bin/python tools/make_training.py held-out              law/TRAIN-HELD-OUT.json (declared once, then sealed:
                                                                  tools/measure.py seal)
    .venv/bin/python tools/make_training.py generate [--out DIR]  training/data/<task>/{train,held_out}.jsonl,
                                                                  ARTICLE-OF.json and INDEX.json (verify TRAIN re-derives them)
    .venv/bin/python tools/make_training.py report --tokenizer F  training/data/REPORT.md (token lengths need AMALIA's
                                                                  tokenizer.json; the counts are the INDEX's)

Reservation (T0, DECISIONS D40): per article (the article ancestor of a passage; a passage without one is its own unit),
reserved when int(sha256(article id), 16) % 5 == 0, plus every article the 18 B3 rules cite or offer as candidates. A
reserved article covers all its descendant passages and all their versions. No example in train touches a reserved
article: its target, its candidates and every source id are outside them; an example whose target is reserved goes to
held_out (its candidates may then be anywhere).

Examples: {"id", "task", "prompt", "answer", "sources", "schema"}. The prompt is the B3 reader's (tools/read_rules.py):
the same opening, rules line, reference date and candidate block ([id] (versão em vigor a D, desde F) + its text), then
the question; "schema" is the answer's JSON schema (what the reader's guided decoding gets, as in prompt.json). The
answer is data (compact canonical JSON: ids, dates, values), never free text. Tasks:
  escolha_passagem  a statement built from the passage itself (the article's epigraph; the article + epigraph + the
                    first words of a número or alínea) and 6-12 candidates of the same chapter (the target, its
                    neighbours, 1-2 of another chapter) -> {"passagem": id}
  texto_vigente     a passage with more than one version and a date (at a version's start, inside it, before the first)
                    -> {"versao": valid_from or null, "revogada": bool}
  nota_dr           a DR validity note, literally -> engine.vigente.parse_note's {effect, diploma, dr_issue,
                    published, valid_from} (notes the grammar cannot parse are left out: no truth)
  remissao          a passage whose text names another act and article (tools/coverage.py, resolved by D0.3) and
                    candidates of the target act -> {"passagem": target id}
  regra_tipada      the settled B3 rules: their stored prompt.json and the latest propose payload as the answer
Limits: <= 40 000 examples, <= 3 per passage and task, dedupe by prompt (a prompt seen with a reserved target is kept
in held_out only), candidate texts as stored (an example whose prompt would exceed MAX_PROMPT_CHARS is not made; no
text is shortened). Deterministic: choices by sha256 of ids, no clock, no randomness outside a seeded Random.
"""
import argparse
import hashlib
import json
import random
import sys
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from engine import vigente  # noqa: E402
from engine.canon import canonical, sha256_text  # noqa: E402
from engine.store import Store  # noqa: E402

VERSION = "ccp-make-training-0.2"
# D70: the training data of D45-D69 and the reservation are read from the law as the store held it when the reservation was
# frozen (2026-10-25): no law object was recorded between then and the EU directives (D70), which are not theirs.
LAW_RECORDED_BY = "2026-10-25T00:00:00Z"
HELD = ROOT / "law/TRAIN-HELD-OUT.json"
DATA = ROOT / "training/data"
FROZEN_AT = "2026-10-25"
TASKS = ["escolha_passagem", "texto_vigente", "nota_dr", "remissao", "regra_tipada"]
MAX_EXAMPLES = 40000
PER_PASSAGE = 3
MAX_PROMPT_CHARS = 9000
MAX_PASSAGE_CHARS = 2500
ESCOLHA_CAP = {"artigo": 4000, "numero": 5000, "alinea": 3000}
LOG_PREFIX = 41  # governance events at T1 generation (evento:41 sealed the training index)
OPENING = "És um leitor da lei portuguesa. Lê as passagens candidatas e responde à pergunta com um objeto JSON e nada mais."


# ---- reservation (T0) ---------------------------------------------------------------------------------------------
def current_passages(store):
    latest = {}
    for p in store.objects["passagem"]:
        if p["id"] not in latest or p["revision"] > latest[p["id"]]["revision"]:
            latest[p["id"]] = p
    return {k: v for k, v in latest.items() if not v.get("stale")}


def article_map(passages):
    """{passage id: the id of its article ancestor (itself for an article); its own id when it has none}."""
    above = {}  # passage id -> its article ancestor, or None when there is none

    def article_above(pid):
        if pid not in above:
            p = passages[pid]
            if p["kind"] == "artigo":
                above[pid] = pid
            else:
                parent = p.get("parent")
                above[pid] = article_above(parent) if parent in passages else None
        return above[pid]

    sys.setrecursionlimit(10000)
    return {pid: article_above(pid) or pid for pid in sorted(passages)}


def by_hash(article_id):
    return int(sha256_text(article_id), 16) % 5 == 0


def b3_articles(store, passages, art_of, readings=None):
    readings = readings or ROOT / "governance/readings"
    cited = set()
    for r in store.objects["regra"]:
        for c in r.get("passages", []):
            cited.add(c["passage"])
        for e in r.get("exceptions", []):
            for c in ([e.get("citation")] if isinstance(e.get("citation"), dict) else e.get("citations", [])):
                if isinstance(c, dict) and c.get("passage"):
                    cited.add(c["passage"])
    candidates = set()
    for f in sorted(readings.glob("*/prompt.json")) if readings.exists() else []:
        candidates.update(json.loads(f.read_text(encoding="utf-8")).get("candidates", []))
    return sorted({art_of[p] for p in cited | candidates if p in art_of})


def held_out_doc(store, declared_at, readings=None):
    passages = current_passages(store)
    art_of = article_map(passages)
    articles = sorted(set(art_of.values()))
    hashed = sorted(a for a in articles if by_hash(a))
    b3 = b3_articles(store, passages, art_of, readings)
    definition = {
        "unit": "article: the article ancestor of a passage (kind artigo); a passage with no article above it is its own unit",
        "by_hash": {"rule": "int(sha256(article id as UTF-8).hexdigest(), 16) % 5 == 0", "share": "about 20 % of articles"},
        "by_b3": {"rule": "every article the 18 B3 rules cite (rules/ citations and exceptions) or offer as candidates "
                          "(governance/readings/<rule>/prompt.json), reserved whole",
                  "articles": b3},
        "covers": "every passage descending from a reserved article, all its versions and so its vigências",
        "held_out_when": "by_hash OR by_b3",
        "rule": "no example in any train.jsonl touches a reserved article (target, candidate or any source id); an example "
                "whose target is in a reserved article goes to held_out.jsonl",
    }
    reserved = sorted(set(hashed) | set(b3))
    return {"declared_at": declared_at, "frozen_at": FROZEN_AT,
            "declared_before": "any training example was generated (training/ does not exist yet)",
            "definition": definition, "sha256": sha256_text(canonical(definition)),
            "counts": {"units": len(articles), "by_hash": len(hashed), "by_b3": len(b3), "reserved": len(reserved)},
            "reserved_articles": reserved}


# ---- prompt pieces (tools/read_rules.py's reader format) ------------------------------------------------------------
def version_at(p, d):
    return next((v for v in p["versions"] if v["valid_from"] <= d and (v["valid_to"] is None or d < v["valid_to"])), None)


def is_note_text(text):
    return vigente.parse_note(text.strip()) is not None


def candidate_block(passages, ids, d):
    lines = []
    for pid in ids:
        v = version_at(passages[pid], d)
        lines.append(f"[{pid}] (versão em vigor a {d}, desde {v['valid_from']})")
        lines.append(v["text"])
        lines.append("")
    return lines


def compose(rules_line, d, kind, block, question, before=None):
    lines = [OPENING, rules_line, f"Data de referência: {d}. Tipo de pergunta: {kind}.", ""]
    if before:
        lines += before + [""]
    lines += ["Passagens candidatas:"] + block + ["Pergunta: " + question]
    return "\n".join(lines)


def answer(obj):
    return canonical(obj)


def schema_pick(ids):
    return {"type": "object", "properties": {"passagem": {"type": "string", "enum": list(ids)}}, "required": ["passagem"], "additionalProperties": False}


PICK_RULE = "Regras: escolhe em «passagem» o id de uma passagem da lista (só ids da lista, nunca texto)."


def first_words(text, n=8):
    body = text.split("\n", 1)[0]
    for sep in (" - ", ") "):
        if sep in body[:8]:
            body = body.split(sep, 1)[1]
            break
    words = body.split()
    return " ".join(words[:n]) + (" …" if len(words) > n else "")


def epigraph(article_text):
    lines = article_text.split("\n")
    if len(lines) < 2:
        return None
    e = lines[1].strip()
    if not e or e[:1].isdigit() or e.startswith(("a)", "(")) or is_note_text(e):
        return None
    return e


# ---- tasks ----------------------------------------------------------------------------------------------------
class Ctx:
    def __init__(self, store, held):
        self.store = store
        self.passages = current_passages(store)
        self.art_of = article_map(self.passages)
        self.reserved = set(held["reserved_articles"])
        self.kids = {}
        for p in self.passages.values():
            self.kids.setdefault(p.get("parent"), []).append(p["id"])
        for k in self.kids:
            self.kids[k].sort(key=self.order)

    @staticmethod
    def order(pid):
        out = []
        for part in pid.replace(":", ".").split("."):
            digits = "".join(c for c in part if c.isdigit())
            out.append((int(digits) if digits else 0, part))
        return out

    def is_reserved(self, pid):
        return self.art_of.get(pid.split("@")[0], pid) in self.reserved

    def eligible(self, pid, d=FROZEN_AT):
        p = self.passages.get(pid)
        if p is None or ".q" in pid:
            return False
        v = version_at(p, d)
        return v is not None and not v.get("revoked") and not is_note_text(v["text"]) and len(v["text"]) <= MAX_PASSAGE_CHARS

    def free(self, ids, allow_reserved):
        return [i for i in ids if allow_reserved or not self.is_reserved(i)]


def rng(*keys):
    return random.Random(int(sha256_text("|".join(keys)), 16))


def escolha(ctx):
    out = []
    by_kind = {"artigo": [], "numero": [], "alinea": []}
    for pid, p in ctx.passages.items():
        if p["kind"] in by_kind and ctx.eligible(pid):
            by_kind[p["kind"]].append(pid)
    for kind, pool in by_kind.items():
        pool.sort(key=lambda i: sha256_text("escolha|" + i))
        made = 0
        for pid in pool:
            if made >= ESCOLHA_CAP[kind]:
                break
            ex = escolha_one(ctx, pid, kind)
            if ex:
                out.append(ex)
                made += 1
    return out


def escolha_one(ctx, pid, kind):
    p = ctx.passages[pid]
    held = ctx.is_reserved(pid)
    r = rng("escolha", pid)
    art_id = ctx.art_of[pid]
    art = ctx.passages.get(art_id)
    if art is None or art["kind"] != "artigo":
        return None
    art_text = version_at(art, FROZEN_AT)
    if art_text is None:
        return None
    epi = epigraph(art_text["text"])
    if epi is None:
        return None
    if kind == "artigo":
        near = [i for i in ctx.kids.get(p.get("parent"), []) if i != pid and ctx.passages[i]["kind"] == "artigo"]
        question = f"Que artigo regula: «{epi}»?"
        level = "artigo"
    elif kind == "numero":
        siblings = [i for i in ctx.kids.get(art_id, []) if i != pid and ctx.passages[i]["kind"] == "numero"]
        cousins = [n for a in ctx.kids.get(art.get("parent"), []) if a != art_id for n in ctx.kids.get(a, []) if ctx.passages[n]["kind"] == "numero"]
        near = siblings + cousins
        question = f"No «{art['label']}» ({epi}), que número diz «{first_words(version_at(p, FROZEN_AT)['text'])}»?"
        level = "numero"
    else:
        num = ctx.passages.get(p.get("parent"))
        siblings = [i for i in ctx.kids.get(p.get("parent"), []) if i != pid and ctx.passages[i]["kind"] == "alinea"]
        cousins = [a for n in ctx.kids.get(art_id, []) if n != p.get("parent") for a in ctx.kids.get(n, []) if ctx.passages[a]["kind"] == "alinea"]
        near = siblings + cousins
        where = f"no número {num['label']} do «{art['label']}»" if num and num["kind"] == "numero" else f"no «{art['label']}»"
        question = f"{where[0].upper() + where[1:]} ({epi}), que alínea diz «{first_words(version_at(p, FROZEN_AT)['text'])}»?"
        level = "alinea"
    near = [i for i in ctx.free(near, held) if ctx.eligible(i)]
    norma = p["norma"]
    far_pool = ctx.far.get((norma, level), []) if hasattr(ctx, "far") else []
    far = [i for i in far_pool if ctx.art_of[i] != art_id and ctx.passages[ctx.art_of[i]].get("parent") != art.get("parent")]
    far = [i for i in ctx.free(far, held) if ctx.eligible(i)]
    if len(near) < 4 or len(far) < 1:
        return None
    r.shuffle(near)
    n_far = 1 + (r.random() < 0.5)
    chosen_far = [far[r.randrange(len(far))] for _ in range(n_far)]
    chosen = list(dict.fromkeys([pid] + near[: 11 - n_far] + chosen_far))
    while len(chosen) >= 6:
        ids = sorted(chosen, key=ctx.order)
        prompt = compose(PICK_RULE, FROZEN_AT, f"escolha_passagem ({level})", candidate_block(ctx.passages, ids, FROZEN_AT), question)
        if len(prompt) <= MAX_PROMPT_CHARS:
            return {"task": "escolha_passagem", "prompt": prompt, "answer": answer({"passagem": pid}), "sources": ids,
                    "schema": schema_pick(ids), "target": pid, "held": held}
        drop = next((i for i in reversed(chosen) if i != pid and i not in chosen_far), None)
        if drop is None:
            break
        chosen.remove(drop)
    return None


def texto_vigente(ctx):
    out = []
    rule = ("Regras: responde em «versao» a data (AAAA-MM-DD) em que começa a versão em vigor na data de referência, ou null "
            "se nenhuma versão está em vigor nessa data; em «revogada» se nessa data a passagem está revogada.")
    for pid in sorted(ctx.passages):
        p = ctx.passages[pid]
        if len(p["versions"]) < 2 or ".q" in pid:
            continue
        vs = sorted(p["versions"], key=lambda v: v["valid_from"])
        if sum(len(v["text"]) for v in vs) > MAX_PROMPT_CHARS - 800:
            continue
        held = ctx.is_reserved(pid)
        r = rng("vigente", pid)
        block = []
        for v in vs:
            block.append(f"[{pid}] (versão desde {v['valid_from']}, até {v['valid_to'] or 'hoje'})")
            block.append(v["text"])
            block.append("")
        dates = []
        k = r.randrange(1, len(vs))
        dates.append(vs[k]["valid_from"])  # on the border: the day a later version starts
        j = r.randrange(len(vs))
        a = date.fromisoformat(vs[j]["valid_from"])
        b = date.fromisoformat(vs[j]["valid_to"] or FROZEN_AT)
        if (b - a).days >= 2:
            dates.append((a + timedelta(days=(b - a).days // 2)).isoformat())  # inside an interval
        first = date.fromisoformat(vs[0]["valid_from"])
        dates.append((first - timedelta(days=1)).isoformat())  # outside: before the first version
        for d in list(dict.fromkeys(dates))[:PER_PASSAGE]:
            v = version_at(p, d)
            ans = {"versao": v["valid_from"] if v else None, "revogada": bool(v and v.get("revoked"))}
            question = f"Que versão de [{pid}] está em vigor a {d}, e está revogada nessa data?"
            prompt = "\n".join([OPENING, rule, f"Data de referência: {d}. Tipo de pergunta: texto_vigente.", "", "Versões da passagem:"]
                               + block + ["Pergunta: " + question])
            schema = {"type": "object", "properties": {"versao": {"anyOf": [{"type": "string", "enum": [x["valid_from"] for x in vs]}, {"type": "null"}]},
                                                       "revogada": {"type": "boolean"}}, "required": ["versao", "revogada"], "additionalProperties": False}
            out.append({"task": "texto_vigente", "prompt": prompt, "answer": answer(ans), "sources": [pid] + sorted({x["raw"] for x in vs}),
                        "schema": schema, "target": pid, "held": held})
    return out


def note_owners(ctx):
    """{raw id: sorted [(start offset, article-or-anexo passage id)]} for the passages whose versions sit in that raw."""
    owners = {}
    for p in ctx.passages.values():
        if p["kind"] in ("artigo", "anexo") and ".q" not in p["id"]:
            for v in p["versions"]:
                owners.setdefault(v["raw"], []).append((v["offsets"]["start"], p["id"]))
    for k in owners:
        owners[k].sort()
    return owners


def nota_dr(ctx):
    import bisect
    out = []
    rule = ("Regras: extrai da nota os campos pedidos, como dados: «effect» (altera, adita, revoga, retifica, republica), "
            "«diploma» como impresso, «dr_issue» (número do Diário da República, com o suplemento se houver), «published» e "
            "«valid_from» (AAAA-MM-DD; null quando a nota não diz «em vigor a partir de»); «article_of_act» não se pede.")
    raws = {}
    for o in ctx.store.objects["raw"]:
        if o["id"] not in raws or o["revision"] > raws[o["id"]]["revision"]:
            raws[o["id"]] = o
    owners = note_owners(ctx)
    per = {}
    for rid in sorted(raws):
        r = raws[rid]
        if not r.get("text"):
            continue
        text = ctx.store.raw_text(r) or ""
        starts = [s for s, _ in owners.get(rid, [])]
        pos = 0
        for line in text.split("\n"):
            if line.startswith("NOTA: "):
                body = line[len("NOTA: "):]
                parsed = vigente.parse_note(body)
                if parsed:
                    k = bisect.bisect_left(starts, pos) - 1
                    owner = owners[rid][k][1] if k >= 0 else None
                    key = owner or rid
                    if per.get(key, 0) < PER_PASSAGE * 1000:  # dedupe by prompt below keeps one per distinct note
                        per[key] = per.get(key, 0) + 1
                        ans = {f: parsed[f] for f in ("effect", "diploma", "dr_issue", "published", "valid_from")}
                        prompt = "\n".join([OPENING, rule, "Tipo de pergunta: nota_dr.", "", "Nota do Diário da República:", body, "",
                                            "Pergunta: Que efeito, diploma, número do Diário da República, data de publicação e data de entrada em vigor diz esta nota?"])
                        str_or_null = {"anyOf": [{"type": "string"}, {"type": "null"}]}
                        schema = {"type": "object", "properties": {"effect": {"type": "string", "enum": sorted(set(vigente.EFFECTS.values()))},
                                                                   "diploma": {"type": "string"}, "dr_issue": {"type": "string"},
                                                                   "published": {"type": "string", "pattern": "^[0-9]{4}-[0-9]{2}-[0-9]{2}$"},
                                                                   "valid_from": str_or_null},
                                  "required": ["effect", "diploma", "dr_issue", "published", "valid_from"], "additionalProperties": False}
                        out.append({"task": "nota_dr", "prompt": prompt, "answer": answer(ans), "sources": ([owner] if owner else []) + [rid],
                                    "schema": schema, "target": owner or rid, "held": bool(owner and ctx.is_reserved(owner))})
            pos += len(line) + 1
    return out


def remissao(ctx):
    sys.path.insert(0, str(ROOT / "tools"))
    import coverage  # noqa: E402  (tools/coverage.py, a registered ferramenta: the D0.3 resolution)
    out = []
    normas = coverage.current_all(ctx.store, "norma")
    rule = "Regras: escolhe em «passagem» o id da passagem para que o texto de origem remete (só ids da lista, nunca texto)."
    count = {}
    for row in coverage.remissoes(ctx.store):
        n = normas.get(row["target"])
        target = coverage.resolve(n, row, set(ctx.passages)) if n and row["artigo"] else None
        if not target or row["scope"] != "pt" or not ctx.eligible(target) or count.get(row["passage"], 0) >= PER_PASSAGE:
            continue
        held = ctx.is_reserved(target) or ctx.is_reserved(row["passage"])
        r = rng("remissao", row["passage"], target, str(row["offsets"]["start"]))
        tp = ctx.passages[target]
        near = [i for i in ctx.kids.get(tp.get("parent"), []) if i != target and ctx.passages[i]["kind"] == tp["kind"]]
        near = [i for i in ctx.free(near, held) if ctx.eligible(i)]
        if len(near) < 3:
            continue
        r.shuffle(near)
        ids = sorted([target] + near[:7], key=ctx.order)
        src = ctx.passages[row["passage"]]
        sv = next(v for v in src["versions"] if v["version"] == row["version"])
        before = ["Texto de origem:", f"[{row['passage']}] (versão desde {sv['valid_from']})", sv["text"]]
        ref = f"artigo {row['artigo']}.º" + (f", n.º {row['numero']}" if row["numero"] else "") + (f", alínea {row['alinea']})" if row["alinea"] else "")
        question = f"O texto de origem remete para o {ref} de «{row['words']}». Que passagem é?"
        prompt = compose(rule, FROZEN_AT, "remissao", candidate_block(ctx.passages, ids, FROZEN_AT), question, before)
        if len(prompt) > MAX_PROMPT_CHARS:
            continue
        count[row["passage"]] = count.get(row["passage"], 0) + 1
        out.append({"task": "remissao", "prompt": prompt, "answer": answer({"passagem": target}), "sources": sorted(set(ids) | {row["passage"]}),
                    "schema": schema_pick(ids), "target": target, "held": held})
    return out


def regra_tipada(ctx, readings=None):
    readings = readings or ROOT / "governance/readings"
    out = []
    rules = {}
    for r in ctx.store.objects["regra"]:
        if r["id"] not in rules or r["revision"] > rules[r["id"]]["revision"]:
            rules[r["id"]] = r
    # the rule states as the log stood when training/data was generated and sealed (events 1..LOG_PREFIX): a later
    # settlement (D43) does not move a sealed training set; a v0.3 of the data would raise LOG_PREFIX on purpose
    from engine import governance as _gov
    prefix = ctx.store.events[:LOG_PREFIX]
    settled_then = {aid for (atype, aid), a in _gov.replay(prefix, ctx.store.principals).assertions.items() if atype == "regra" and a["state"] == "settled"}
    for rid, r in sorted(rules.items()):
        if rid not in settled_then:
            continue
        slug = rid.split(":", 1)[1].replace(":", "--").replace("@", "-at-")
        pf = readings / slug / "prompt.json"
        if not pf.exists():
            continue
        body = json.loads(pf.read_text(encoding="utf-8"))
        proposes = [ev for _, ev in ctx.store.events if ev["action"] in ("propose", "correct") and ev["assertion"] == rid]
        if not proposes:
            continue
        pay = proposes[-1]["payload"]
        ans = {"passagens": sorted(pay["chosen_passages"]), "tipo": r["type"], "condicoes": pay.get("conditions", []), "params": pay.get("params", {})}
        srcs = sorted(set(body["candidates"]) | set(pay["chosen_passages"]))
        out.append({"task": "regra_tipada", "prompt": body["prompt"], "answer": answer(ans), "sources": srcs, "schema": body["schema"],
                    "target": rid, "held": any(ctx.is_reserved(s) for s in srcs)})
    return out


# ---- assembly ---------------------------------------------------------------------------------------------------
def generate(store, held_doc, readings=None):
    """{relative path: bytes} of training/data (INDEX.json included). Pure: same store and reservation -> same bytes."""
    ctx = Ctx(store, held_doc)
    ctx.far = {}
    for pid, p in ctx.passages.items():
        if p["kind"] in ("artigo", "numero", "alinea") and ".q" not in pid:
            ctx.far.setdefault((p["norma"], p["kind"]), []).append(pid)
    for k in ctx.far:
        ctx.far[k].sort(key=lambda i: sha256_text("far|" + i))
        ctx.far[k] = ctx.far[k][:400]
    made = escolha(ctx) + texto_vigente(ctx) + nota_dr(ctx) + remissao(ctx) + regra_tipada(ctx, readings)
    by_prompt = {}
    for ex in made:  # dedupe by prompt; a prompt that ever had a reserved target stays in held_out only
        k = ex["prompt"]
        if k not in by_prompt:
            by_prompt[k] = ex
        elif ex["held"] and not by_prompt[k]["held"]:
            by_prompt[k] = ex
    examples = sorted(by_prompt.values(), key=lambda e: (e["task"], sha256_text(e["prompt"])))
    if len(examples) > MAX_EXAMPLES:
        raise SystemExit(f"{len(examples)} examples > {MAX_EXAMPLES}")
    files, index = {}, {"version": VERSION, "frozen_at": FROZEN_AT, "train_held_out_definition_sha256": held_doc.get("sha256"),
                        "limits": {"max_examples": MAX_EXAMPLES, "per_passage_and_task": PER_PASSAGE, "max_prompt_chars": MAX_PROMPT_CHARS,
                                   "max_passage_chars": MAX_PASSAGE_CHARS, "escolha_cap": ESCOLHA_CAP},
                        "tasks": {}, "files": {}}
    covered = set()
    for task in TASKS:
        for split in ("train", "held_out"):
            rows = []
            for e in examples:
                if e["task"] != task or e["held"] != (split == "held_out"):
                    continue
                if split == "train" and any(ctx.is_reserved(s) for s in e["sources"]):
                    raise SystemExit(f"{task}: a train example touches a reserved article: {e['target']}")
                covered.add(e["target"])
                rows.append(json.dumps({"id": f"{task}:{sha256_text(e['prompt'])[:16]}", "task": task, "prompt": e["prompt"],
                                        "answer": e["answer"], "sources": e["sources"], "schema": e["schema"]}, ensure_ascii=False, sort_keys=True))
            rel = f"{task}/{split}.jsonl"
            files[rel] = ("\n".join(rows) + ("\n" if rows else "")).encode("utf-8")
            index["tasks"].setdefault(task, {})[split] = len(rows)
    art = {pid: a for pid, a in ctx.art_of.items()}
    files["ARTICLE-OF.json"] = (json.dumps(art, ensure_ascii=False, sort_keys=True, indent=0) + "\n").encode("utf-8")
    index["passages_total"] = len(ctx.passages)
    index["passages_covered"] = len(covered & set(ctx.passages))
    index["examples"] = len(examples)
    for rel in sorted(files):
        b = files[rel]
        index["files"][rel] = {"sha256": hashlib.sha256(b).hexdigest(), "lines": b.count(b"\n")}
    files["INDEX.json"] = (json.dumps(index, ensure_ascii=False, sort_keys=True, indent=1) + "\n").encode("utf-8")
    return files


def write(files, out):
    out.mkdir(parents=True, exist_ok=True)
    for rel, b in files.items():
        p = out / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(b)


def report(out, tokenizer_path):
    """REPORT.md: examples per task and split, passages covered, mean length in tokens (AMALIA's tokenizer.json)."""
    from tokenizers import Tokenizer  # only here: the report's token figures; verify never imports it
    tok = Tokenizer.from_file(str(tokenizer_path))
    index = json.loads((out / "INDEX.json").read_text(encoding="utf-8"))
    lines = ["# Training data — report", "", f"Generated by tools/make_training.py ({index['version']}) from law/; frozen_at {index['frozen_at']}; "
             f"reservation law/TRAIN-HELD-OUT.json (definition sha256 {index['train_held_out_definition_sha256']}).", "",
             f"Examples: {index['examples']}. Passages covered as targets: {index['passages_covered']} of {index['passages_total']}.", "",
             f"Token lengths with the family-A reader's tokenizer (tokenizer.json sha256 {hashlib.sha256(Path(tokenizer_path).read_bytes()).hexdigest()}), prompt + answer, no chat template:", "",
             "| task | train | held_out | mean tokens (train) | max tokens (train) |", "|---|---|---|---|---|"]
    total_tokens = 0
    for task in TASKS:
        rows = [json.loads(l) for l in (out / task / "train.jsonl").read_text(encoding="utf-8").splitlines() if l]
        lens = [len(tok.encode(r["prompt"] + "\n" + r["answer"]).ids) for r in rows]
        total_tokens += sum(lens)
        mean = round(sum(lens) / len(lens)) if lens else 0
        lines.append(f"| {task} | {index['tasks'][task]['train']} | {index['tasks'][task]['held_out']} | {mean} | {max(lens) if lens else 0} |")
    lines += ["", f"Total train tokens (prompt + answer): {total_tokens}.", ""]
    (out / "REPORT.md").write_text("\n".join(lines), encoding="utf-8")
    print("\n".join(lines))


def load_repo():
    return Store([ROOT / "law", ROOT / "rules", ROOT / "governance"]).load()


def main():
    ap = argparse.ArgumentParser(description="held-out | generate | report")
    ap.add_argument("cmd", choices=["held-out", "generate", "report"])
    ap.add_argument("--out", default=str(DATA)); ap.add_argument("--tokenizer")
    a = ap.parse_args()
    if a.cmd == "held-out":
        from engine.sources import now_utc
        if HELD.exists():
            raise SystemExit(f"{HELD.relative_to(ROOT)} exists: it is declared once and sealed, never redrawn")
        doc = held_out_doc(load_repo(), now_utc())
        HELD.write_text(json.dumps(doc, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        print(doc["counts"], "sha256", hashlib.sha256(HELD.read_bytes()).hexdigest())
    elif a.cmd == "generate":
        files = generate(load_repo(), json.loads(HELD.read_text(encoding="utf-8")))
        write(files, Path(a.out))
        print(json.loads(files["INDEX.json"])["tasks"])
    else:
        report(Path(a.out), a.tokenizer)


if __name__ == "__main__":
    main()
