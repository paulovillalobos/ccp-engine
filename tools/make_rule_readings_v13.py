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
- a stored schema keeps the factory's property order (data-v12's sort_keys sorted it: D66's serving trap);
- the measured sets stay data-v12's (training/data-v12/regra_lida/{dev,sealed,dev_antigo}.jsonl).
profile() is what tools/preflight_data.py compares with the measured set before a run.
"""
import argparse
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT)); sys.path.insert(0, str(ROOT / "tools"))
import make_rule_readings_v12 as v12  # noqa: E402  (render, quotes by code, the factory's checker, the leak test)
import read_rules_v3 as v3  # noqa: E402

VERSION = "ccp-make-rule-readings-v13-0.1"
DATA = ROOT / "training/data-v13"
MEASURED = ROOT / "training/data-v12/regra_lida"
TASK = v12.TASK
VOC = v3.VOC
SOURCES = ["batch-*.jsonl", "alvo-*.jsonl", "v3-*.jsonl", "v4-*.jsonl"]
MEASURED_SOURCES = ["eval-*.jsonl", "eval3-*.jsonl"]
# BRIEF-D67: the kinds of one batch of 100 (comparador: lt and le only until the limiar product rule is decided)
BRIEF_MIX = {"nao_tipavel": 40, "contagem": 9, "grandeza": 8, "valor_condicao": 8, "casos": 8, "comparador": 8, "alineas": 7, "remissao": 6, "capitulo": 6}
FIRST_WHERE_OTHERS_MAX = 0.40
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


def measured_texts():
    return [v12.alvo_text(ex) for pattern in MEASURED_SOURCES for ex in v12.load(pattern)]


def build(store=None, only=None):
    """[(ex, row)] for training, {id: why left out}."""
    real, measured = v12.m.reference_texts(store), measured_texts()
    train, rejected = [], {}
    for pattern in SOURCES:
        for ex in v12.load(pattern):
            if only and not ex["id"].startswith(only):
                continue
            if pattern.startswith("v4") and not ex.get("lugar"):
                rejected[ex["id"]] = "no lugar (BRIEF-D67: every article sits under titles)"; continue
            t = v12.alvo_text(ex)
            if v12.close(t, real) or v12.close(t, measured):
                rejected[ex["id"]] = "close to a real passage or a measured article"; continue
            ex = housed(ex)
            res, errs = v12.problems(ex)
            if errs:
                rejected[ex["id"]] = errs[0]; continue
            train.append((ex, v12.row(ex, res[1], res[0])))
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


def measured_pairs(name="dev"):
    arts = {f"{TASK}:{ex['id']}": ex for pattern in MEASURED_SOURCES for ex in v12.load(pattern)}
    rows = [json.loads(line) for line in (MEASURED / f"{name}.jsonl").read_text(encoding="utf-8").splitlines() if line.strip()]
    return [(arts[r["id"]], r) for r in rows]


# ---- out -----------------------------------------------------------------------------------------------------------------
def dump(rows):
    return "".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows).encode("utf-8")  # no sort_keys: the schema keeps the factory's order


def generate(store=None):
    train, rejected = build(store)
    files = {"regra_lida/train.jsonl": dump(r for _, r in sorted(train, key=lambda x: x[1]["id"])),
             "REJECTED.json": (json.dumps(rejected, ensure_ascii=False, indent=1, sort_keys=True) + "\n").encode("utf-8")}
    index = {"tool": VERSION, "protocol": v3.VERSION, "date": v12.DATE, "rejected": len(rejected),
             "files": {k: {"rows": v.count(b"\n"), "sha256": hashlib.sha256(v).hexdigest()} for k, v in sorted(files.items())},
             "measured_sets": str(MEASURED.relative_to(ROOT)), "profile": profile(train),
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
            fw = p["quote_first_where_others"]
            print(f"quotes that are the vocabulary's first phrase where it lists others: {100 * (fw or 0):.0f} % "
                  f"(BRIEF-D67: at most {100 * FIRST_WHERE_OTHERS_MAX:.0f} %){'  <- too many' if fw and fw > FIRST_WHERE_OTHERS_MAX else ''}")
        return
    files = generate()
    for rel, b in files.items():
        f = DATA / rel
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_bytes(b)
    print({k: v for k, v in json.loads(files["INDEX.json"]).items() if k != "profile"})


if __name__ == "__main__":
    main()
