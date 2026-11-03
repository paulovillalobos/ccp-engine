"""Phase 16 data (DECISIONS D67): data-v13, AMALIA v13's rule-reading rows in the reading protocol v3.

    .venv/bin/python tools/make_rule_readings_v13.py check [--only PREFIX]   render, quote, check, and the mix of what passes; writes nothing
    .venv/bin/python tools/make_rule_readings_v13.py generate                training/data-v13

The articles are rendered, quoted and checked by data-v12's code (tools/make_rule_readings_v12.py). The audit of data-v12
(reports/DATA-AUDIT-v12.md) found its training rows unlike the articles they were measured on. What changes:
- the D67 articles (training/rule-readings/v4-*.jsonl, written to BRIEF-D67.md) join batch-*, alvo-* and v3-*;
- every training article is compared with the real passages and with every measured article (eval-*, eval3-*); data-v12
  compared v3-* only;
- an article written without titles (batch-*, alvo-*) is placed under NEUTRAL titles, as every article of the law sits under
  some: titles that name no field value, deadline, starting point, amount field or comparator (checked at import);
- AGED_SHARE of the articles (aged_ids: by id, among those with a word that has an old form) are written in the spelling
  before the 1990 agreement (the vocabulary's old_spelling forms), as that share of the real law's passages is (texture());
- a stored schema keeps the factory's property order (data-v12's sort_keys sorted it: D66's serving trap);
- the measured sets keep data-v12's articles and gold (training/data-v12/regra_lida/{dev,sealed,dev_antigo}.jsonl); their
  prompts are rendered again with the protocol 0.4 (training/data-v13/regra_lida/), as every prompt here is.
profile() and texture() are what tools/preflight_data.py compares with dev and with the real law before a run.
"""
import argparse
import hashlib
import json
import re
import statistics as st
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT)); sys.path.insert(0, str(ROOT / "tools"))
import make_rule_readings_v12 as v12  # noqa: E402  (render, quotes by code, the factory's checker, the leak test)
import read_rules as rr  # noqa: E402
import read_rules_v3 as v3  # noqa: E402
import rule_factory as rf  # noqa: E402  (PATTERNS: a passage that states a deadline in days or a euro amount)

VERSION = "ccp-make-rule-readings-v13-0.1"
PROTOCOL = v3.VERSION  # D67: the reading protocol 0.4
DATA = ROOT / "training/data-v13"
MEASURED = ROOT / "training/data-v12/regra_lida"
TASK = v12.TASK
VOC = v3.VOC
SOURCES = ["batch-*.jsonl", "alvo-*.jsonl", "v3-*.jsonl", "v4-*.jsonl"]
MEASURED_SOURCES = ["eval-*.jsonl", "eval3-*.jsonl"]
# BRIEF-D67: the kinds of one batch of 100 (comparador: lt and le only until the limiar product rule is decided)
BRIEF_MIX = {"nao_tipavel": 40, "contagem": 9, "grandeza": 8, "valor_condicao": 8, "casos": 8, "comparador": 8, "alineas": 7, "remissao": 6, "capitulo": 6}
AGED_SHARE = 0.27  # the real law's passages with days or euros that show a pre-1990 spelling (texture(real_contexts()), 2026-11-03)
# BRIEF-D67 section 7: a batch's texture, from the real law's (112 passages: shown text median 1 981 characters, 12 passages,
# target 447, 4 values named; cross-reference in the target 55 %, qualifier 21 %, another law 18 %, other units 23 %,
# revoked 7 %; first listed phrase 37 % of the values named)
TEXTURE_BRIEF = {"shown_chars": (1500, 3500), "passages": (9, 18), "target_chars": (250, 900), "values_named": (4, 14),
                 "xref": (0.40, 0.70), "qualifier": (0.12, 0.35), "other_law": (0.10, 0.30), "units": (0.15, 0.35),
                 "first_phrase": (0.27, 0.47)}
NEW_TO_OLD = {new: old for old, new in VOC["old_spelling"].items()}
NEUTRAL = [
    ["Título II — Fase de formação do contrato", "Capítulo I — Disposições comuns"],
    ["Título III — Tramitação procedimental", "Capítulo IV — Prazos"],
    ["Título II — Disposições gerais", "Capítulo II — Regras comuns de tramitação"],
    ["Título IV — Formação dos contratos", "Capítulo III — Disposições gerais", "Secção I — Regras comuns"],
    ["Título V — Tramitação", "Capítulo VI — Fases do procedimento"],
    ["Título III — Regras gerais", "Capítulo II — Prazos procedimentais"],
    ["Título II — Formação do contrato", "Capítulo V — Disposições comuns à tramitação"],
    ["Título VI — Disposições comuns", "Capítulo I — Âmbito", "Secção II — Regras de tramitação"],
]


def names_something(title):
    """What a title names in the vocabulary (a field, a deadline, a start, an amount field, a comparator or a phrase list), or None."""
    for field, spec in VOC["condition_fields"].items():
        if spec["kind"] == "enum" and v3.values_named(field, title):
            return field
        if spec["kind"] == "boolean" and v3.polarity(field, title):
            return field
    for key, table in VOC.items():
        if key in ("about", "condition_fields", "old_spelling", "nao_tipavel_motivos"):
            continue
        words = [w for ws in table.values() for w in (ws if isinstance(ws, list) else [])] if isinstance(table, dict) else table
        if isinstance(words, list) and any(isinstance(w, str) and v3.contains(title, w) for w in words):
            return key
    return None


for _chain in NEUTRAL:
    for _t in _chain:
        if names_something(_t):
            raise SystemExit(f"NEUTRAL title «{_t}» names {names_something(_t)}")


def housed(ex):
    """The article under its own titles, or under neutral ones chosen by its id."""
    if ex.get("lugar"):
        return ex
    return {**ex, "lugar": list(NEUTRAL[int(hashlib.sha256(ex["id"].encode("utf-8")).hexdigest(), 16) % len(NEUTRAL)])}


def old_spelling(text):
    def back(mt):
        w = NEW_TO_OLD[mt.group(0).lower()]
        return w[0].upper() + w[1:] if mt.group(0)[0].isupper() else w
    return re.sub(r"(?<!\w)(?:" + "|".join(sorted(map(re.escape, NEW_TO_OLD), key=len, reverse=True)) + r")(?!\w)", back, text, flags=re.I) if text else text


def aged(ex):
    """The article in the spelling before the 1990 agreement; itself when none of its words has an old form. The gold does
    not change: the factory's checker and the quote finder read both spellings."""
    nums = lambda xs: [{**x, "texto": old_spelling(x["texto"])} for x in xs or []]  # noqa: E731
    out = {**ex, "epigrafe": old_spelling(ex["epigrafe"]), "texto": old_spelling(ex.get("texto", "")), "numeros": nums(ex["numeros"]),
           "lugar": [old_spelling(t) for t in ex.get("lugar") or []] or ex.get("lugar"),
           "remissoes": [{**r, "epigrafe": old_spelling(r["epigrafe"]), "texto": old_spelling(r.get("texto", "")), "numeros": nums(r.get("numeros"))}
                         for r in ex.get("remissoes") or []] or ex.get("remissoes")}
    if "texto" not in ex:
        out.pop("texto")
    return ex if json.dumps(out, ensure_ascii=False, sort_keys=True) == json.dumps(ex, ensure_ascii=False, sort_keys=True) else out


def aged_ids(exs):
    """The articles written in the old spelling: AGED_SHARE of them all, the first by sha256 of the id among those with a
    word that has an old form (a long article almost always has one, a short one half the time)."""
    eligible = sorted((ex["id"] for ex in exs if aged(ex) is not ex), key=lambda i: hashlib.sha256(("aged:" + i).encode("utf-8")).hexdigest())
    return set(eligible[:round(AGED_SHARE * len(exs))])


def measured_texts():
    return [v12.alvo_text(ex) for pattern in MEASURED_SOURCES for ex in v12.load(pattern)]


def build(store=None, only=None):
    """[(ex, row)] for training, {id: why left out}."""
    real, measured = v12.m.reference_texts(store), measured_texts()
    cands, train, rejected = [], [], {}
    for pattern in SOURCES:
        for ex in v12.load(pattern):
            if only and not ex["id"].startswith(only):
                continue
            if pattern.startswith("v4") and not ex.get("lugar"):
                rejected[ex["id"]] = "no lugar (BRIEF-D67: every article sits under titles)"; continue
            t = v12.alvo_text(ex)
            if v12.close(t, real) or v12.close(t, measured):
                rejected[ex["id"]] = "close to a real passage or a measured article"; continue
            cands.append(housed(ex))
    old = aged_ids(cands)
    for ex in cands:
        ex = aged(ex) if ex["id"] in old else ex
        res, errs = v12.problems(ex, PROTOCOL)
        if errs:
            rejected[ex["id"]] = errs[0]; continue
        train.append((ex, v12.row(ex, res[1], res[0], PROTOCOL)))
    return train, rejected


# ---- the profile of a set of rows ----------------------------------------------------------------------------------------
def phrase_table(field):
    if field == "deadline_field":
        return VOC["deadline_fields"]
    if field == "counted_from":
        return VOC["counted_from"]
    spec = VOC["condition_fields"].get(field)
    if spec and spec["kind"] == "enum":
        return spec["values"]
    if spec and spec["kind"] == "boolean":
        return {True: spec["phrases"]}
    return None


def share(k, n):
    return round(k / n, 4) if n else None


def profile(pairs):
    """Labels, kinds, titles and quotes of [(article, row)]: what preflight_data.py compares."""
    kinds, motivos, roles, q = Counter(), Counter(), Counter(), Counter()
    titled = nt = 0
    for ex, r in pairs:
        g = json.loads(r["answer"])
        ctx = v12.ctx_of(ex)
        kinds[ex.get("estilo") or "-"] += 1
        titled += bool(ex.get("lugar"))
        if g.get("nao_tipavel"):
            nt += 1
            motivos[g["nao_tipavel"]["motivo"]] += 1
            roles.update(ctx["roles"].get(f["de"], "?") for f in g["nao_tipavel"]["fontes"])
        for rule in g["regras"]:
            for c in rule["condicoes"]:
                roles.update(ctx["roles"].get(f["de"], "?") for f in c["fontes"])
            for fs in rule["fontes"].values():
                roles.update(ctx["roles"].get(f["de"], "?") for f in fs or [])
            items = [(c["field"], c["value"], c["fontes"]) for c in rule["condicoes"]]
            items += [(k, rule["params"].get(k), fs) for k, fs in rule["fontes"].items() if k in ("deadline_field", "counted_from") and fs]
            for field, value, fs in items:
                t = phrase_table(field)
                vals = [x for x in (value if isinstance(value, list) else [value]) if t and x in t]
                if not vals:
                    continue
                firsts = {v3.norm(t[x][0]) for x in vals}
                others = any(len(t[x]) > 1 for x in vals)
                for f in fs:
                    first = v3.norm(f["texto"]) in firsts
                    q["quotes"] += 1; q["first"] += first
                    if others:
                        q["could_vary"] += 1; q["first_where_others"] += first
    n, nq = len(pairs), sum(roles.values())
    return {"rows": n, "nao_tipavel": share(nt, n), "motivos": dict(motivos.most_common()), "titled": share(titled, n),
            "kinds": dict(kinds.most_common()), "quote_first_phrase": share(q["first"], q["quotes"]),
            "quote_first_where_others": share(q["first_where_others"], q["could_vary"]),
            "quote_roles": {k: share(v, nq) for k, v in roles.most_common()}}


# ---- texture: what a reader is shown, in the real law and in a written article -----------------------------------------
OTHER_LAW = re.compile(r"Decreto-Lei n\.º|Lei n\.º|Diretiva|Regulamento \(|Regulamento Delegado|Portaria n\.º|Decreto Regulamentar|Resolução do Conselho|"
                       r"Código do Procedimento Administrativo|Código do Trabalho|Código Civil|regime jurídico", re.I)
QUALIFIER = re.compile(r"sem prejuízo|salvo|exceto|excepto|com exce[cç][ãa]o|ressalvad|nos termos d|para efeitos d", re.I)
XREF = re.compile(r"n\.º\s*\d+\s+do\s+artigo|artigo anterior|n[úu]mero anterior|al[íi]nea anterior|presente artigo|presente c[óo]digo|do artigo \d+", re.I)
UNITS = re.compile(r"dias úteis|\bmeses\b|\bhoras\b|\bpor cento\b|%", re.I)
REVOKED = re.compile(r"revogad[oa]", re.I)
OLD_FORMS = re.compile(r"(?<!\w)(?:" + "|".join(sorted(map(re.escape, VOC["old_spelling"]), key=len, reverse=True)) + r")(?!\w)", re.I)


def first_phrase_uses(text):
    """For each value the text names, among those the vocabulary gives several phrases: is one of them its first listed phrase?"""
    t, out = v3.norm(text), []
    for spec in VOC["condition_fields"].values():
        if spec["kind"] != "enum":
            continue
        for ws in spec["values"].values():
            if len(ws) > 1:
                hits = [v3.norm(w) for w in ws if re.search(rf"(?<!\w){re.escape(v3.norm(w))}(?!\w)", t)]
                if hits:
                    out.append(v3.norm(ws[0]) in hits)
    return out


def features(ctx):
    allowed, alvo = ctx["allowed"], ctx["alvo"]
    text, a = "\n".join(allowed.values()), allowed[ctx["alvo"]]
    return {"shown_chars": len(text), "passages": len(allowed), "target_chars": len(a),
            "values_named": sum(len(v3.values_named(f, text)) for f, s in VOC["condition_fields"].items() if s["kind"] == "enum"),
            "xref": bool(XREF.search(a)), "qualifier": bool(QUALIFIER.search(a)), "other_law": bool(OTHER_LAW.search(text)),
            "units": bool(UNITS.search(text)), "revoked": bool(REVOKED.search(text)), "old_spelling": bool(OLD_FORMS.search(text)),
            "first_phrase": first_phrase_uses(text)}


def texture(ctxs):
    fs = [features(c) for c in ctxs]
    n = len(fs)
    if not n:
        return {"n": 0}
    out = {"n": n, **{k: st.median(f[k] for f in fs) for k in ("shown_chars", "passages", "target_chars", "values_named")},
           **{k: share(sum(f[k] for f in fs), n) for k in ("xref", "qualifier", "other_law", "units", "revoked", "old_spelling")}}
    uses = [u for f in fs for u in f["first_phrase"]]
    out["first_phrase"] = share(sum(uses), len(uses))
    return out


def real_contexts(store=None):
    """The v3 context of every CCP passage in force that states a deadline in days or a euro amount (the factory's PATTERNS)."""
    store = store or v12.m.Store([ROOT / "law", ROOT / "rules", ROOT / "governance"]).load()
    law, out = v3.Law(store), []
    for p in store.objects["passagem"]:
        v = rr.version_at(store.current(p["id"]), v12.DATE) if p["id"].startswith("ccp:art") else None
        if v and any(pat.search(v["text"]) for pat in rf.PATTERNS.values()):
            try:
                out.append(v3.context(law, p["id"], v12.DATE))
            except (KeyError, ValueError, IndexError):
                continue
    return out


def measured_pairs(name="dev"):
    arts = {f"{TASK}:{ex['id']}": ex for pattern in MEASURED_SOURCES for ex in v12.load(pattern)}
    rows = [json.loads(line) for line in (MEASURED / f"{name}.jsonl").read_text(encoding="utf-8").splitlines() if line.strip()]
    return [(arts[r["id"]], r) for r in rows]


# ---- out -----------------------------------------------------------------------------------------------------------------
def dump(rows):
    return "".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows).encode("utf-8")  # no sort_keys: the schema keeps the factory's order


def measured_in_protocol(name):
    """A measured set of data-v12 with the same articles and gold, its prompts rendered with this protocol (0.4)."""
    out = []
    for ex, r in measured_pairs(name):
        res, errs = v12.problems(ex, PROTOCOL)
        if errs or json.dumps(res[0], ensure_ascii=False, separators=(",", ":")) != r["answer"]:
            raise SystemExit(f"{r['id']}: its gold does not pass protocol {PROTOCOL} as it is ({errs[:1]})")
        out.append(v12.row(ex, res[1], res[0], PROTOCOL))
    return out


def generate(store=None, held_doc=None):
    train, rejected = build(store)
    files = {"regra_lida/train.jsonl": dump(r for _, r in sorted(train, key=lambda x: x[1]["id"])),
             "REJECTED.json": (json.dumps(rejected, ensure_ascii=False, indent=1, sort_keys=True) + "\n").encode("utf-8")}
    for name in ("dev", "sealed", "dev_antigo"):  # the same articles and gold as data-v12's, read with the protocol 0.4
        files[f"regra_lida/{name}.jsonl"] = dump(measured_in_protocol(name))
    index = {"tool": VERSION, "protocol": PROTOCOL, "date": v12.DATE, "rejected": len(rejected),
             "files": {k: {"rows": v.count(b"\n"), "sha256": hashlib.sha256(v).hexdigest()} for k, v in sorted(files.items())},
             "measured_sets": f"{MEASURED.relative_to(ROOT)}'s articles and gold, prompts in {PROTOCOL}", "profile": profile(train),
             "note": "D67: data-v12's articles plus BRIEF-D67's, every one under titles, compared with every measured article, schema in the factory's order"}
    files["INDEX.json"] = (json.dumps(index, ensure_ascii=False, indent=1) + "\n").encode("utf-8")
    return files


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("cmd", choices=["check", "generate"]); ap.add_argument("--only")
    a = ap.parse_args()
    if a.cmd == "check":
        train, rejected = build(only=a.only)
        print(f"pass: {len(train)}, left out: {len(rejected)}")
        for i, (eid, why) in enumerate(sorted(rejected.items())):
            if a.only or i < 40:
                print(f"{eid}: {why}")
        if a.only and a.only.startswith("v4"):
            p = profile(train)
            have = p["kinds"]
            print("kinds (have / BRIEF-D67 per 100): " + ", ".join(f"{k} {have.get(k, 0)}/{n}" for k, n in BRIEF_MIX.items())
                  + (f"; not in the brief: {sorted(set(have) - set(BRIEF_MIX))}" if set(have) - set(BRIEF_MIX) else ""))
            print("não tipável by reason (10 each): " + ", ".join(f"{m} {p['motivos'].get(m, 0)}" for m in VOC["nao_tipavel_motivos"]))
            mine, real = texture([v12.ctx_of(ex) for ex, _ in train]), texture(real_contexts())
            print("texture, your batch | the real law (BRIEF-D67 section 7):")
            for k, want in TEXTURE_BRIEF.items():
                lo, hi = want
                x = mine.get(k)
                flag = "" if x is not None and lo <= x <= hi else "  <- outside the brief"
                print(f"  {k:14} {x} | {real.get(k)}   brief: {lo}–{hi}{flag}")
        return
    files = generate()
    for rel, b in files.items():
        f = DATA / rel
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_bytes(b)
    print({k: v for k, v in json.loads(files["INDEX.json"]).items() if k != "profile"})


if __name__ == "__main__":
    main()
