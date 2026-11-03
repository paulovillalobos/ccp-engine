"""Pre-flight gate (DECISIONS D67): a training set's rule-reading rows against the measured articles, before any spend.

    .venv/bin/python tools/preflight_data.py [--train training/data-v13/regra_lida/train.jsonl] [--json OUT]

What the model will learn from is compared with what it will be measured on, the dev set (training/data-v12/regra_lida/
dev.jsonl, the set error analysis may use), and with what it must read, the real law (make_rule_readings_v13.texture of
every CCP passage that states days or euros). The sealed set's article texts are used for the leak test only. Exit 1 when
a check fails; training/train_lora.py runs this before a run that names it. Why each check: reports/DATA-AUDIT-v12.md.
- labels: the «não tipável» share is within 5 points of dev's, and each reason holds at least 20 % of them;
- titles: at least 95 % of the training articles sit under titles, as every article of the law does;
- kinds: every kind of dev has at least 100 training articles («não tipável» counted by the gold);
- texture: the D67 rows (BRIEF-D67) are at least 40 % of the rows and, taken together, inside BRIEF-D67's bands around the
  real law (text shown, passages, target length, values named, cross-references, qualifiers, other laws, other units);
  the old spelling is within 10 points of the real law's share;
- wording: where the vocabulary lists several phrases for a value, the share of values the text names by the first one is
  within 10 points of the real law's (the prompt prints the first phrases; a reader trained on them copies them);
- order: every stored schema is the factory's (read_rules_v3.schema), property order included, and every answer's keys
  follow it (the decoder writes keys in the schema's order: D66);
- leaks: no training article is, or is close to (difflib, make_rule_readings.LEAK), a measured article.
"""
import argparse
import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT)); sys.path.insert(0, str(ROOT / "tools"))
import make_rule_readings_v12 as v12  # noqa: E402
import make_rule_readings_v13 as v13  # noqa: E402
import read_rules_v3 as v3  # noqa: E402

VERSION = "ccp-preflight-data-0.2"
NT_BAND, NT_REASON_MIN, TITLED_MIN, KIND_MIN, D67_MIN, REAL_SLACK = 0.05, 0.20, 0.95, 100, 0.40, 0.10


def key_order_ok(a, s):
    if isinstance(s, dict) and "anyOf" in s:
        return any(key_order_ok(a, b) for b in s["anyOf"] if (b.get("type") == "object") == isinstance(a, dict) and (b.get("type") == "array") == isinstance(a, list)) or a is None
    if isinstance(a, dict) and isinstance(s, dict) and isinstance(s.get("properties"), dict):
        return list(a) == [k for k in s.get("required", list(s["properties"])) if k in a] and all(key_order_ok(v, s["properties"][k]) for k, v in a.items() if k in s["properties"])
    if isinstance(a, list) and isinstance(s, dict) and "items" in s:
        return all(key_order_ok(v, s["items"]) for v in a)
    return True


def shown(ex, prompt):
    """The article as its row's prompt shows it: as data-v13 writes it (neutral titles, old spelling) when the prompt shows
    that text, as written otherwise (data-v12)."""
    for cand in (v13.aged(v13.housed(ex)), v13.housed(ex)):
        if cand is not ex and all(t in prompt for t in v12.ctx_of(cand)["allowed"].values()):
            return cand
    return ex


def articles():
    return {f"{v12.TASK}:{ex['id']}": ex for p in v13.SOURCES + v13.MEASURED_SOURCES for ex in v12.load(p)}


def gate(train_path, arts=None):
    arts = arts or articles()
    rows = [json.loads(line) for line in Path(train_path).read_text(encoding="utf-8").splitlines() if line.strip()]
    pairs = [(shown(arts[r["id"]], r["prompt"]) if r["id"] in arts else None, r) for r in rows]
    missing = [r["id"] for ex, r in pairs if ex is None]
    pairs = [(ex, r) for ex, r in pairs if ex is not None]
    train, dev = v13.profile(pairs), v13.profile(v13.measured_pairs("dev"))
    checks = []

    def add(name, ok, have, want):
        checks.append({"check": name, "ok": bool(ok), "train": have, "dev_or_limit": want})

    add("labels: «não tipável» share", abs(train["nao_tipavel"] - dev["nao_tipavel"]) <= NT_BAND, train["nao_tipavel"], f"{dev['nao_tipavel']} ± {NT_BAND}")
    nt_n = max(1, round(train["nao_tipavel"] * train["rows"]))
    low = {m: round(train["motivos"].get(m, 0) / nt_n, 3) for m in v3.VOC["nao_tipavel_motivos"] if train["motivos"].get(m, 0) / nt_n < NT_REASON_MIN}
    add("labels: each reason ≥ 20 % of «não tipável»", not low, train["motivos"], f"short: {low}" if low else "≥ 0.20 each")
    add("titles: articles under titles", train["titled"] >= TITLED_MIN, train["titled"], f"≥ {TITLED_MIN} (dev {dev['titled']})")
    counts = dict(train["kinds"]); counts["nao_tipavel"] = nt_n
    short = {k: counts.get(k, 0) for k in dev["kinds"] if counts.get(k, 0) < KIND_MIN}
    add("kinds: every dev kind ≥ 100 training articles", not short, {k: counts.get(k, 0) for k in dev["kinds"]}, f"short: {short}" if short else f"≥ {KIND_MIN} each")
    real = v13.texture(v13.real_contexts())
    d67 = [ex for ex, r in pairs if r["id"].startswith(f"{v12.TASK}:v4-")]
    every, new = v13.texture([v12.ctx_of(ex) for ex, _ in pairs]), v13.texture([v12.ctx_of(ex) for ex in d67])
    add("texture: D67 rows ≥ 40 % of the training rows", len(d67) >= D67_MIN * len(pairs), f"{len(d67)} of {len(pairs)}", f"≥ {D67_MIN}")
    for k, (lo, hi) in v13.TEXTURE_BRIEF.items():
        if k != "first_phrase":
            add(f"texture: D67 rows' {k} inside BRIEF-D67's band", new.get(k) is not None and lo <= new[k] <= hi, new.get(k), f"{lo}–{hi} (real law {real[k]})")
    add("texture: old spelling like the real law", abs(every["old_spelling"] - real["old_spelling"]) <= REAL_SLACK, every["old_spelling"], f"{real['old_spelling']} ± {REAL_SLACK}")
    add("wording: values named by their first listed phrase, like the real law", abs(every["first_phrase"] - real["first_phrase"]) <= REAL_SLACK,
        every["first_phrase"], f"{real['first_phrase']} ± {REAL_SLACK}")
    bad_schema = bad_answer = 0
    for ex, r in pairs:
        want = v3.schema(v12.ctx_of(ex), ex["tipo"])
        bad_schema += json.dumps(r["schema"], ensure_ascii=False) != json.dumps(want, ensure_ascii=False)
        bad_answer += not key_order_ok(json.loads(r["answer"]), want)
    add("order: stored schema = the factory's, order included", bad_schema == 0, f"{bad_schema} of {len(pairs)} differ", 0)
    add("order: answer keys follow the schema", bad_answer == 0, f"{bad_answer} of {len(pairs)} differ", 0)
    measured = {}
    for name in ("dev", "sealed", "dev_antigo"):
        for line in (v13.MEASURED / f"{name}.jsonl").read_text(encoding="utf-8").splitlines():
            if line.strip():
                rid = json.loads(line)["id"]
                measured[rid] = v12.alvo_text(arts[rid])
    texts = list(measured.values())
    leaks = [r["id"] for ex, r in pairs if r["id"] in measured or v12.close(v12.alvo_text(ex), texts)]
    add("leaks: no training article is or is close to a measured one", not leaks and not missing, f"{len(leaks)} close" + (f", {len(missing)} unknown ids" if missing else ""), 0)
    return {"tool": VERSION, "train": str(train_path), "ok": all(c["ok"] for c in checks), "checks": checks,
            "profile": {"train": train, "dev": dev}, "texture": {"real_law": real, "all_rows": every, "d67_rows": new}, "leaks": leaks[:50]}


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--train", default=str(v13.DATA / "regra_lida/train.jsonl")); ap.add_argument("--json")
    a = ap.parse_args()
    rep = gate(a.train)
    for c in rep["checks"]:
        print(f"{'PASS' if c['ok'] else 'FAIL'}  {c['check']}: train {c['train']} | {c['dev_or_limit']}")
    if a.json:
        Path(a.json).write_text(json.dumps(rep, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print("pre-flight:", "PASS" if rep["ok"] else "FAIL")
    sys.exit(0 if rep["ok"] else 1)


if __name__ == "__main__":
    main()
