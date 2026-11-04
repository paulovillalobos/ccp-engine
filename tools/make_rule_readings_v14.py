"""Phase 17 data (DECISIONS D68): data-v14, AMALIA v14's practice on the real law.

    .venv/bin/python tools/make_rule_readings_v14.py check      the practice readings, their rows and what is left out; writes nothing
    .venv/bin/python tools/make_rule_readings_v14.py generate   training/data-v14

product_rule:leituras-assentes-como-pratica (D68): a reading of a real passage that both families settled blind may be practice
for family A. PRACTICE: the readings settled when round 9 ended (evento:275), each at its revision then; EXAM: the round-9
targets still open then, which round 10 reads and no training row may show. A reading is left out when the text it read is no
longer in force on the factory's date, when its passage's article holds an exam target, or when any passage its reader sees is
an exam passage or close to one (difflib ratio LEAK). Each kept passage gives its own row and VARIANTS more: the same context
with the reading's days or euro amounts moved by code where its quotes are, and the gold derived again from the moved text by
data-v12's code (make_rule_readings_v12.derive); every row passes the factory's checker with the protocol 0.4.

Out (train_lora keys a task by its folder; this regra_lida replaces data-v13's in v14's mix):
- regra_lida/train.jsonl: the practice rows («estilo» real), and REMIND of data-v13's training rows (the first by sha256 of
  the id), so v14, trained from v13 (training/train_lora.py RUNS v14), keeps reading written articles;
- REJECTED.json (each reading left out and why), INDEX.json. The measured sets stay data-v13's.
allowed_sources(store) is what verify lets a practice row cite inside a reserved article: the passages its reader sees, for a
reading the log holds settled now, under the product rule the log holds settled.
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
import make_rule_readings_v12 as v12  # noqa: E402  (derive: the gold's quotes found by code; close: the leak test)
import make_rule_readings_v13 as v13  # noqa: E402  (PROTOCOL 0.4, dump, data-v13's training rows)
import read_rules_v3 as v3  # noqa: E402

VERSION = "ccp-make-rule-readings-v14-0.1"
PROTOCOL = v13.PROTOCOL
DATA = ROOT / "training/data-v14"
TASK = v12.TASK
DATE = v12.DATE
PRODUCT_RULE = "product_rule:leituras-assentes-como-pratica"
VARIANTS = 24
REMIND = 800
# settled when round 9 ended (evento:275): a rule at its revision then, or a «não tipável» by leitor:a15's proposal and its passage
PRACTICE = {
    "regra:ccp:auto-prazo-minimo-art174-1@v1": 3, "regra:ccp:auto-prazo-minimo-art174-2@v1": 4,
    "regra:ccp:auto-prazo-minimo-art190-1@v1": 4, "regra:ccp:auto-prazo-minimo-art190-1-b@v1": 2,
    "regra:ccp:auto-prazo-minimo-art191-1@v1": 4, "regra:ccp:auto-prazo-minimo-art191-5@v1": 4,
    "regra:ccp:auto-prazo-minimo-art218@v1": 3, "regra:ccp:auto-prazo-minimo-art219-b-5@v1": 3,
    "regra:ccp:auto-prazo-minimo-art219-b-5-b@v1": 2, "regra:ccp:auto-prazo-minimo-art219-j-3@v1": 4,
    "regra:ccp:limiar-ajuste-direto-obras@v2": 1, "regra:ccp:limiar-consulta-previa-obras@v1": 2,
    "regra:ccp:limiar-consulta-previa-obras@v2": 2, "regra:ccp:prazo-minimo-concurso-joue@v1": 4,
    "regra:ccp:prazo-minimo-concurso-sem-joue-bens-servicos@v1": 6, "regra:ccp:prazo-minimo-concurso-sem-joue-obras@v1": 6,
    "nao_tipavel:ccp:auto-limiar-art17-b-4@v1": ("evento:257", "ccp:art17-b.4"),
    "nao_tipavel:ccp:auto-limiar-art88-2-a@v1": ("evento:267", "ccp:art88.2.a"),
    "nao_tipavel:ccp:auto-prazo-minimo-art241-b-3-b@v1": ("evento:273", "ccp:art241-b.3.b"),
}
EXAM = ["ccp:art127-c.1.a", "ccp:art21.1.b", "ccp:art21.1.c", "ccp:art31.4", "ccp:art54-a.1.b.ii", "ccp:art174.3", "ccp:art192.2",
        "ccp:art198.1", "ccp:art198.2"]
AMOUNTS = [5000, 10000, 15000, 20000, 25000, 30000, 40000, 50000, 60000, 75000, 80000, 100000, 120000, 125000, 150000, 200000,
           250000, 300000, 400000, 500000, 600000, 750000, 1000000, 1500000, 2000000, 3000000, 5000000]
DAYS_RE = re.compile(r"(?<![\d.])(\d+)(?=\s+dias)(?!\s+dias\s+úteis)")


def rule_file(rid, rev):
    return ROOT / "rules/regra" / f"regra-{rid[len('regra:'):].replace(':', '-').replace('@', '-at-')}.r{rev}.json"


def events_by_id():
    return {e["id"]: e for e in (json.loads(line) for line in (ROOT / "governance/events.jsonl").read_text(encoding="utf-8").splitlines() if line.strip())}


def readings(law):
    """[(reading id, passage, type, rule or «não tipável»)] at the pinned revisions, and {id: why left out}."""
    exam_arts, exam_texts = {law.article_of(p) for p in EXAM}, [law.text(p, DATE) for p in EXAM]
    evs, out, rejected = events_by_id(), [], {}
    for rid, pin in PRACTICE.items():
        if rid.startswith("regra:"):
            d = json.loads(rule_file(rid, pin).read_text(encoding="utf-8"))
            (pid,) = {x["passage"] for x in d["passages"]}
            rtype, body = d["type"], {"condicoes": d["conditions"], "params": d["params"]}
            if d.get("valid_to") and d["valid_to"] <= DATE:
                rejected[rid] = f"it reads the text before {d['valid_to']}, not the one in force on {DATE}"; continue
        else:
            ev, pid = pin
            p = evs[ev]["payload"]
            rtype, body = p["rule_type"], {"motivo": p["motivo"], "fonte": p["fontes"][0]["texto"], "falta": p["falta"]}
        if law.article_of(pid) in exam_arts:
            rejected[rid] = f"its article {law.article_of(pid)} holds an exam target"; continue
        ctx = v3.context(law, pid, DATE)
        shown = [q for q in ctx["roles"] if q in EXAM] or [q for q, t in ctx["allowed"].items() if t and v12.close(t, [x for x in exam_texts if x])]
        if shown:
            rejected[rid] = f"its reader sees {shown[0]}, an exam passage or close to one"; continue
        out.append((rid, pid, rtype, body))
    return out, rejected


def passages(law):
    """{passage: (type, the written-article shape data-v12's derive reads)}: a passage's rules are one answer."""
    kept, rejected = readings(law)
    by = {}
    for rid, pid, rtype, body in kept:
        ex = by.setdefault(pid, {"id": pid, "tipo": rtype, "regras": [], "nao_tipavel": None, "readings": []})
        ex["readings"].append(rid)
        if "motivo" in body:
            ex["nao_tipavel"] = body
        else:
            ex["regras"].append(body)
    return by, rejected


# ---- the numbers moved --------------------------------------------------------------------------------------------------
def fmt_amount(n, sep):
    return f"{n:,}".replace(",", sep) if n >= 1000 else str(n)


WORDS = {**{v: w for w, v in v3.UNITS.items() if w not in ("uma", "duas", "quatorze")}, **{v: w for w, v in v3.TENS.items()}}


def in_words(n):
    """«seis», «vinte e cinco»: the protocol's own words for n (1–99)."""
    return WORDS.get(n) or f"{WORDS[n - n % 10]} e {WORDS[n % 10]}"


def move_days(text, old, new):
    """old days become new, in digits where the text has digits and in words where it has words («seis dias»)."""
    moved = re.sub(rf"(?<![\d.]){old}(?=\s+dias)", str(new), text, count=1)
    if moved != text:
        return moved
    for w in sorted((w for w, v in {**v3.UNITS, **v3.TENS}.items() if v == old), key=len, reverse=True) + ([in_words(old)] if old > 20 and old % 10 else []):
        moved = re.sub(rf"(?<!\w){w}(?=\s+dias)", in_words(new), text, count=1, flags=re.I)
        if moved != text:
            return moved
    return text


def move_amount(text, old, new):
    for x in v12.AMOUNT.finditer(text):
        g = 1 if x.group(1) else 2
        if int(re.sub(r"[ . ]", "", x.group(g))) == old:
            sep = next((c for c in x.group(g) if not c.isdigit()), " ")
            return text[:x.start(g)] + fmt_amount(new, sep) + text[x.end(g):]
    return text


def replace_in(ctx, pid, old, new):
    """The context with old replaced by new once in the passage pid, as the checker and the reader both see it."""
    if old == new:
        return
    if old not in (ctx["allowed"].get(pid) or ""):
        raise v12.Gap(f"«{old[:40]}» is not in {pid}")
    ctx["allowed"][pid] = ctx["allowed"][pid].replace(old, new, 1)
    ctx["items"] = [(p, t.replace(old, new, 1) if p == pid else t, lvl) for p, t, lvl in ctx["items"]]


def variant(ex, ctx, gold, rng):
    """(ex, ctx) with each rule's days or amount moved where the gold quotes it; a «não tipável» moves the target's first number."""
    ex, ctx = copy.deepcopy(ex), copy.deepcopy(ctx)
    if ex["nao_tipavel"]:
        text = ctx["allowed"][ctx["alvo"]]
        d, a = DAYS_RE.search(text), next(v12.AMOUNT.finditer(text), None)
        if a and (d is None or a.start() < d.start()):
            old = int(re.sub(r"[ . ]", "", a.group(1) or a.group(2)))
            new = rng.choice([n for n in AMOUNTS if n != old])
            moved = move_amount(text, old, new)
        elif d:
            old = int(d.group(1)); new = rng.choice([n for n in range(5, 91) if n != old])
            moved = move_days(text, old, new)
        else:
            raise v12.Gap("no number in the target to move")
        old_part, new_part = (text, moved)
        replace_in(ctx, ctx["alvo"], old_part, new_part)
        nt = ex["nao_tipavel"]
        if nt["fonte"] not in new_part and nt["fonte"] in old_part:
            s = old_part.index(nt["fonte"])
            nt["fonte"] = new_part[s:s + len(nt["fonte"]) + len(new_part) - len(old_part)]
        return ex, ctx
    used = set()
    for r, g in zip(ex["regras"], gold["regras"]):
        p = r["params"]
        if "minimum_days" in p:
            moves = [("minimum_days", p["minimum_days"])] + ([("usual_days", p["usual_days"])] if p.get("usual_days") else [])
            for key, old in moves:
                new = rng.choice([n for n in range(5, 91) if n != old and n not in used])
                used.add(new)
                for f in g["fontes"][key]:
                    replace_in(ctx, f["de"], f["texto"], move_days(f["texto"], old, new))
                p[key] = new
        else:
            th = p["threshold"]
            old = th["value"]
            new = rng.choice([n for n in AMOUNTS if n != old and n not in used])
            used.add(new)
            for f in g["fontes"]["value"]:
                replace_in(ctx, f["de"], f["texto"], move_amount(f["texto"], old, new))
            th["value"] = new
    return ex, ctx


def row(pid, k, rtype, ctx, answer):
    srcs = sorted({pid} | {f["de"] for r in answer["regras"] for fs in [*(c["fontes"] for c in r["condicoes"]), *r["fontes"].values()] for f in fs or []}
                  | {f["de"] for f in ((answer.get("nao_tipavel") or {}).get("fontes") or [])})
    return {"id": f"{TASK}:real:{pid}:{k:02d}", "task": TASK, "prompt": v3.render(ctx, rtype, PROTOCOL), "schema": v3.schema(ctx, rtype),
            "answer": json.dumps(answer, ensure_ascii=False, separators=(",", ":")), "sources": srcs, "estilo": "real"}


def gold_of(ex, ctx):
    answer = v12.derive(ex, ctx)
    errs = v3.check(answer, ctx, ex["tipo"], PROTOCOL)
    if errs:
        raise v12.Gap(f"checker: {errs[0]}")
    return answer


def build(store=None):
    """The practice rows, {reading or passage: why left out}, {passage: rows}."""
    store = store or v12.m.Store([ROOT / "law", ROOT / "rules", ROOT / "governance"]).load()
    law = v3.Law(store)
    by, rejected = passages(law)
    rows, per = [], {}
    for pid, ex in sorted(by.items()):
        ctx = v3.context(law, pid, DATE)
        try:
            gold = gold_of(ex, ctx)
        except (v12.Gap, KeyError, ValueError) as exc:
            for rid in ex["readings"]:
                rejected[rid] = f"gold: {exc}"
            continue
        mine = [row(pid, 0, ex["tipo"], ctx, gold)]
        for k in range(1, VARIANTS + 1):
            rng = random.Random(f"{VERSION}:{pid}:{k}")
            try:
                ex2, ctx2 = variant(ex, ctx, gold, rng)
                mine.append(row(pid, k, ex["tipo"], ctx2, gold_of(ex2, ctx2)))
            except (v12.Gap, KeyError, ValueError):
                continue
        rows += mine
        per[pid] = {"readings": ex["readings"], "rows": len(mine)}
    return rows, rejected, per


def remind():
    rows = [json.loads(line) for line in (v13.DATA / "regra_lida/train.jsonl").read_text(encoding="utf-8").splitlines() if line.strip()]
    return sorted(rows, key=lambda r: hashlib.sha256(r["id"].encode()).hexdigest())[:REMIND]


def allowed_sources(store):
    """The passages a practice row may cite inside a reserved article: those its reader sees, for a reading the log holds settled
    now, while the log holds the product rule settled. verify reads the states from the store, not from PRACTICE's pins."""
    from engine.governance import Log
    rp = Log(store.governance_dir).replay()
    if rp.state_of("product_rule", PRODUCT_RULE) != "settled":
        return set()
    law, out = v3.Law(store), set()
    kept, _ = readings(law)
    for rid, pid, _, _ in kept:
        if rp.state_of(rid.split(":", 1)[0], rid) == "settled":
            out |= set(v3.context(law, pid, DATE)["allowed"])
    return out


def generate(store=None, held_doc=None):
    rows, rejected, per = build(store)
    old = remind()
    files = {"regra_lida/train.jsonl": v13.dump(rows + old),
             "REJECTED.json": (json.dumps(rejected, ensure_ascii=False, indent=1, sort_keys=True) + "\n").encode("utf-8")}
    index = {"tool": VERSION, "protocol": PROTOCOL, "date": DATE, "product_rule": PRODUCT_RULE, "practice": per,
             "practice_rows": len(rows), "remind_rows": len(old), "rejected": len(rejected), "exam": EXAM,
             "files": {k: {"rows": v.count(b"\n"), "sha256": hashlib.sha256(v).hexdigest()} for k, v in sorted(files.items())},
             "note": "D68: the readings both families settled blind by evento:275, their numbers moved by code; the exam is the targets still open then"}
    files["INDEX.json"] = (json.dumps(index, ensure_ascii=False, indent=1) + "\n").encode("utf-8")
    return files


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("cmd", choices=["check", "generate"])
    a = ap.parse_args()
    if a.cmd == "check":
        rows, rejected, per = build()
        print(f"practice passages {len(per)}, rows {len(rows)}; readings left out {len(rejected)}")
        for pid, x in per.items():
            print(f"  {pid}: {x['rows']} rows ({', '.join(x['readings'])})")
        for rid, why in sorted(rejected.items()):
            print(f"  left out {rid}: {why}")
        return
    files = generate()
    for rel, b in files.items():
        f = DATA / rel
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_bytes(b)
    print({k: v for k, v in json.loads(files["INDEX.json"]).items() if k not in ("files", "practice")})


if __name__ == "__main__":
    main()
