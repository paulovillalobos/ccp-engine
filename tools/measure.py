"""The measurement of ARQUITECTURA.md §8 (B5): reference cases annotated blind by two families, then precision and recall of
each rule against them, inside and held out, with 95 % Wilson intervals. Everything is recomputed from stored answers.

    .venv/bin/python tools/measure.py prompts [--store fixtures/measure]   governance/readings/casos/<case>/prompt.json
    (the readers answer them from readers/, D38: leitor-a.json, leitor-b.json beside each prompt)
    .venv/bin/python tools/measure.py record  [--store fixtures/measure]   caso_referencia per case; CASOS-DESACORDO.md
    .venv/bin/python tools/measure.py --out reports/measure/<date>.json --date <date> [--store ...]   the report (+ .md)

Annotation: for each case, every B3 rule valid on the procedure's start date, given as its id, title and the law it
cites (the quotes of its citations: law text, never the rule's params), and the case's facts; each reader says per rule
cumpre / nao_cumpre / nao_avaliado (a fact is missing) / nao_aplica. A (case, rule) pair both readers answer alike is
the expected verdict of the case (nao_aplica pairs are not expected verdicts); a pair they answer differently goes to
governance/readings/CASOS-DESACORDO.md: a fact's reading there is a pessoa's to adjudicate (Log.adjudicate), never a
reader's, and nothing is adjudicated here. Held out: law/HELD-OUT.json (by entity and period, frozen before the rules).
Report: per rule, against the expected verdicts, the engine's verdict (engine.evaluate with that rule alone, valid_at =
the procedure's start); "não cumpre" is the positive class: precision = TP / (TP + FP), recall = TP / (TP + FN), each
with its 95 % Wilson interval, split inside / held out; agreement A vs B over all pairs (exact: same answer; direction:
both say breach or both do not); pairs pending adjudication; error classes of the source (needs BASE notices: stated
as not measurable while data/ is empty). Deterministic: sorted, no clock; the date is an argument.
"""
import argparse
import json
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
import verify  # noqa: E402
from engine import evaluate as evaluate_mod  # noqa: E402
from engine import manifest as manifest_mod  # noqa: E402
from engine import rules as rules_mod  # noqa: E402
from engine.canon import canonical, sha256_text  # noqa: E402
from engine.store import Store, Writer, facts_of  # noqa: E402

VERSION = "ccp-measure-0.1"
CASES_DIR = ROOT / "governance/readings/casos"
RESULTS = ["cumpre", "nao_cumpre", "nao_avaliado", "nao_aplica"]
KNOWN_AT = "2026-10-24T21:00:00Z"


def load(store_dir):
    return Store([ROOT / store_dir, ROOT / "law", ROOT / "rules", ROOT / "governance"]).load()


def held_out_def():
    return json.loads((ROOT / "law/HELD-OUT.json").read_text(encoding="utf-8"))


def is_held_out(values, doc):
    nif = str(values.get("adjudicante", ""))
    by_entity = bool(nif) and int(sha256_text(nif), 16) % 5 == 0
    start = values.get("data_inicio_procedimento")
    by_period = bool(start) and start >= doc["definition"]["by_period"]["from"]
    return by_entity or by_period


def case_values(store, unit):
    return {f["field"]: f["value"] for f in facts_of(store, unit["id"], known_at=KNOWN_AT)}


def case_rules(store, start):
    rules = [r for r in verify.current_of(store, "regra").values() if not r.get("stale") and rules_mod.valid_at(r, start)]
    return sorted(rules, key=lambda r: r["id"])


def units(store):
    return sorted((u for u in verify.current_of(store, "unidade").values() if u["kind"] == "proc" and u["id"].startswith("proc:fixture-measure:")
                   or (u["kind"] == "proc" and not u["id"].startswith("proc:base:FX"))), key=lambda u: u["id"])


def case_key(unit):
    return unit["id"].split(":")[-1].lower()


# ---- prompts ---------------------------------------------------------------------------------------------------
def cmd_prompts(store):
    for unit in units(store):
        vals = case_values(store, unit)
        rules = case_rules(store, vals.get("data_inicio_procedimento", KNOWN_AT[:10]))
        lines = ["És um anotador de casos de contratação pública. Para cada regra abaixo lê o texto da lei que ela cita e os factos do "
                 "procedimento, e diz se o procedimento cumpre o que a lei exige, não cumpre, não pode ser avaliado porque falta um facto "
                 "de que a resposta depende (nao_avaliado), ou se esse texto não se aplica a este procedimento (nao_aplica). Responde só com JSON.",
                 "", "Factos do procedimento:"]
        lines += [f"  {k}: {json.dumps(v, ensure_ascii=False)}" for k, v in sorted(vals.items())]
        lines += ["  (um facto que não aparece não foi publicado)", "", "Regras:"]
        for r in rules:
            lines.append(f"[{r['id']}] {r['title']}")
            for c in r["passages"]:
                lines.append(f"  {c['passage']} (versão de {c['version']}): {c['quote']}")
            lines.append("")
        schema = {"type": "object", "properties": {"veredictos": {"type": "array", "minItems": len(rules), "items": {
            "type": "object", "properties": {"regra": {"type": "string", "enum": [r["id"] for r in rules]}, "resultado": {"type": "string", "enum": RESULTS}},
            "required": ["regra", "resultado"], "additionalProperties": False}}}, "required": ["veredictos"], "additionalProperties": False}
        d = CASES_DIR / case_key(unit)
        d.mkdir(parents=True, exist_ok=True)
        (d / "prompt.json").write_text(json.dumps({"unit": unit["id"], "rules": [r["id"] for r in rules], "prompt": "\n".join(lines), "schema": schema},
                                                  ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"prompts in {CASES_DIR}")


# ---- annotations -------------------------------------------------------------------------------------------------
def annotations(path, rules):
    """{rule: result} from a reader's stored answer; the first answer per rule counts; unknown rules ignored."""
    if not path.exists():
        return {}, None
    rec = json.loads(path.read_text(encoding="utf-8"))
    try:
        items = json.loads(rec["answer"])["veredictos"]
    except (json.JSONDecodeError, KeyError, TypeError):
        return {}, rec
    out = {}
    for it in items:
        if isinstance(it, dict) and it.get("regra") in rules and it.get("resultado") in RESULTS and it["regra"] not in out:
            out[it["regra"]] = it["resultado"]
    return out, rec


def pairs(store):
    """[(unit, rule id, A, B)] over every case and rule of its prompt."""
    out = []
    for unit in units(store):
        d = CASES_DIR / case_key(unit)
        if not (d / "prompt.json").exists():
            continue
        rules = json.loads((d / "prompt.json").read_text(encoding="utf-8"))["rules"]
        a, _ = annotations(d / "leitor-a.json", rules)
        b, _ = annotations(d / "leitor-b.json", rules)
        for rid in rules:
            out.append((unit, rid, a.get(rid), b.get(rid)))
    return out


def cmd_record(store_dir):
    store = load(store_dir)
    doc = held_out_def()
    writer = Writer(ROOT / store_dir, Store([ROOT / store_dir]).load())
    queue = ["# CASOS-DESACORDO — pares (caso, regra) em que os anotadores cegos diferem", "",
             "Gerado por tools/measure.py. Um facto (o prazo foi de 9 dias?) adjudica-o uma pessoa no log (Log.adjudicate); uma leitura da "
             "lei não. Nada aqui foi adjudicado: estes pares não entram nas cifras até o serem.", "",
             "| caso | regra | leitor:a | leitor:b |", "|---|---|---|---|"]
    by_unit = {}
    for unit, rid, a, b in pairs(store):
        by_unit.setdefault(unit["id"], (unit, []))[1].append((rid, a, b))
    for uid, (unit, items) in sorted(by_unit.items()):
        d = CASES_DIR / case_key(unit)
        ra = json.loads((d / "leitor-a.json").read_text(encoding="utf-8")) if (d / "leitor-a.json").exists() else None
        rb = json.loads((d / "leitor-b.json").read_text(encoding="utf-8")) if (d / "leitor-b.json").exists() else None
        expected = []
        for rid, a, b in items:
            if a is not None and a == b:
                if a != "nao_aplica":
                    expected.append({"rule": rid, "result": a, "reason": "facto_ausente" if a == "nao_avaliado" else None})
            else:
                queue.append(f"| {uid} | {rid} | {a or '—'} | {b or '—'} |")
        if not expected or ra is None or rb is None:
            continue
        held = is_held_out(case_values(store, unit), doc)
        obj = {"id": f"ref:{case_key(unit)}", "revision": 1, "recorded_at": KNOWN_AT, "unit": uid, "expected": sorted(expected, key=lambda e: e["rule"]),
               "annotators": [{"principal": "leitor:a", "at": ra["at"], "agrees_with_expected": True}, {"principal": "leitor:b", "at": rb["at"], "agrees_with_expected": True}],
               "adjudication": None, "held_out": held, "frozen_at": doc["frozen_at"] if held else None}
        prev = writer.store.current(obj["id"])
        if prev is None:
            writer.append(obj)
    (ROOT / "governance/readings/CASOS-DESACORDO.md").write_text("\n".join(queue) + "\n", encoding="utf-8")


# ---- report ------------------------------------------------------------------------------------------------------
def wilson(k, n, z=1.959964):
    if n == 0:
        return None, [0.0, 1.0]
    p = k / n
    den = 1 + z * z / n
    c = (p + z * z / (2 * n)) / den
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / den
    return round(p, 4), [round(max(0.0, c - h), 4), round(min(1.0, c + h), 4)]


def engine_result(store, unit, rule, vals):
    start = vals.get("data_inicio_procedimento", KNOWN_AT[:10])
    manifest = manifest_mod.build("lei:ccp@measure", "pacote:ccp@measure", ["adaptador:fixture-measure@1"],
                                  [{"source": "fixture-measure", "sha256": "0" * 64, "captured_at": KNOWN_AT}],
                                  {"repository": "measure", "commit": "0000000", "engine_version": evaluate_mod.VERSION}, "0" * 64, KNOWN_AT)
    out = evaluate_mod.evaluate(unit, [rule], facts_of(store, unit["id"], known_at=KNOWN_AT), KNOWN_AT, start, manifest=manifest)
    v = next((x for x in out if x["rule"]["id"] == rule["id"]), None)
    return v["result"] if v else "nao_aplica"


def report(store_dir, date):
    store = load(store_dir)
    doc = held_out_def()
    rules = verify.current_of(store, "regra")
    cases = {c["unit"]: c for c in verify.current_of(store, "caso_referencia").values()}
    per_rule = {}
    for unit in units(store):
        c = cases.get(unit["id"])
        if not c:
            continue
        vals = case_values(store, unit)
        split = "reservado" if c["held_out"] else "dentro"
        for e in c["expected"]:
            rule = rules[e["rule"]]
            got = engine_result(store, unit, rule, vals)
            m = per_rule.setdefault(e["rule"], {"state": rule["state"], "dentro": {"tp": 0, "fp": 0, "fn": 0, "tn": 0, "n": 0},
                                                "reservado": {"tp": 0, "fp": 0, "fn": 0, "tn": 0, "n": 0}})[split]
            m["n"] += 1
            pos_e, pos_g = e["result"] == "nao_cumpre", got == "nao_cumpre"
            m["tp" if pos_e and pos_g else "fp" if pos_g else "fn" if pos_e else "tn"] += 1
    for m in per_rule.values():
        for split in ("dentro", "reservado"):
            s = m[split]
            p, pi = wilson(s["tp"], s["tp"] + s["fp"])
            r, ri = wilson(s["tp"], s["tp"] + s["fn"])
            s["precision"] = {"value": p, "n": s["tp"] + s["fp"], "wilson95": pi}
            s["recall"] = {"value": r, "n": s["tp"] + s["fn"], "wilson95": ri}
    ps = pairs(store)
    answered = [(u, rid, a, b) for u, rid, a, b in ps if a is not None and b is not None]
    exact = sum(1 for _, _, a, b in answered if a == b)
    direction = sum(1 for _, _, a, b in answered if (a == "nao_cumpre") == (b == "nao_cumpre"))
    return {"tool": VERSION, "date": date, "frozen_at": doc["frozen_at"], "held_out_sha256": doc["sha256"], "store": store_dir,
            "cases": len(cases), "cases_held_out": sum(1 for c in cases.values() if c["held_out"]),
            "pairs": len(ps), "pending_adjudication": sum(1 for _, _, a, b in ps if a is None or a != b),
            "agreement": {"answered_by_both": len(answered), "exact": exact, "direction": direction,
                          "exact_rate": wilson(exact, len(answered))[0], "direction_rate": wilson(direction, len(answered))[0]},
            "rules": dict(sorted(per_rule.items())),
            "error_classes": {"regime_desatualizado": None, "note": "error classes of BASE notices (declared regime out of date, etc.) need the extractor's "
                                                                     "afirmações; data/ is empty, so they are not measured here"}}


def render_md(rep):
    L = [f"# Medição §8 — {rep['date']}", "", f"Gerado por tools/measure.py ({rep['tool']}). Conjunto reservado congelado a {rep['frozen_at']} "
         f"(law/HELD-OUT.json, sha256 {rep['held_out_sha256'][:12]}…). Casos: {rep['cases']} ({rep['cases_held_out']} reservados), store "
         f"{rep['store']} (FIXTURE enquanto data/ está vazio).", "",
         f"Acordo A vs B sobre {rep['agreement']['answered_by_both']} pares respondidos por ambos: exato {rep['agreement']['exact']} "
         f"({rep['agreement']['exact_rate']}), de direção (incumprimento ou não) {rep['agreement']['direction']} ({rep['agreement']['direction_rate']}). "
         f"Pares pendentes de adjudicação ou sem resposta: {rep['pending_adjudication']} de {rep['pairs']}.", "",
         "Classe positiva: «não cumpre». IC de Wilson a 95 %.", "",
         "| regra | estado | dentro: precisão | dentro: recall | reservado: precisão | reservado: recall |", "|---|---|---|---|---|---|"]
    fmt = lambda x: "—" if x["value"] is None else f"{x['value']} [{x['wilson95'][0]}, {x['wilson95'][1]}] n={x['n']}"  # noqa: E731
    for rid, m in rep["rules"].items():
        L.append(f"| {rid} | {m['state']} | {fmt(m['dentro']['precision'])} | {fmt(m['dentro']['recall'])} | {fmt(m['reservado']['precision'])} | {fmt(m['reservado']['recall'])} |")
    L += ["", f"Classes de erro de BASE: {rep['error_classes']['note']}."]
    return "\n".join(L) + "\n"


def cmd_seal():
    """Seal the raw annotations and the held-out definition in the log (verify SEAL)."""
    import hashlib
    from engine.governance import Log
    from engine.sources import now_utc
    files = sorted(p for p in CASES_DIR.rglob("*.json") if p.name != "INDEX.json") if CASES_DIR.exists() else []
    index = {"files": {str(p.relative_to(CASES_DIR)): hashlib.sha256(p.read_bytes()).hexdigest() for p in files}}
    (CASES_DIR / "INDEX.json").write_text(json.dumps(index, ensure_ascii=False, indent=1, sort_keys=True) + "\n", encoding="utf-8")
    held = ROOT / "law/HELD-OUT.json"
    train_held = ROOT / "law/TRAIN-HELD-OUT.json"  # D40: the training reservation and the training index ride on the same seal
    train_index = ROOT / "training/data/INDEX.json"
    log = Log(ROOT / "governance")
    n = 1 + sum(1 for _, ev in log.events if str(ev["assertion"]).startswith("selo:casos:"))
    tool = next(p["id"] for p in log.principals["principals"] if p["id"].startswith("ferramenta:measure@") and not p["retired"])
    payload = {"index_sha256": sha256_text(canonical(index)), "held_out_sha256": hashlib.sha256(held.read_bytes()).hexdigest() if held.exists() else None,
               "files": len(files)}
    if train_held.exists():
        payload["train_held_out_sha256"] = hashlib.sha256(train_held.read_bytes()).hexdigest()
    aval = ROOT / "governance/readings/avaliacao-v1"  # D42: the T3 answers (leitor:a / leitor:a2) ride on the same seal
    aval_files = sorted(p for p in aval.rglob("*") if p.is_file() and p.name != "INDEX.json") if aval.exists() else []
    if aval_files:
        aidx = {"files": {str(p.relative_to(aval)): hashlib.sha256(p.read_bytes()).hexdigest() for p in aval_files}}
        (aval / "INDEX.json").write_text(json.dumps(aidx, ensure_ascii=False, indent=1, sort_keys=True) + "\n", encoding="utf-8")
        payload["avaliacao_index_sha256"] = sha256_text(canonical(aidx))
    if train_index.exists():
        payload["training_index_sha256"] = sha256_text(canonical(json.loads(train_index.read_text(encoding="utf-8"))))
    ev = log.propose(tool, "caso_referencia", f"selo:casos:{n}", payload, now_utc())
    log.write_state()
    print(ev, len(files), "files sealed")


def main():
    ap = argparse.ArgumentParser(description="prompts | record | report | seal")
    ap.add_argument("cmd", nargs="?", choices=["prompts", "record", "seal"])
    ap.add_argument("--store", default="fixtures/measure"); ap.add_argument("--out"); ap.add_argument("--date")
    a = ap.parse_args()
    if a.cmd == "prompts":
        cmd_prompts(load(a.store))
    elif a.cmd == "record":
        cmd_record(a.store)
    elif a.cmd == "seal":
        cmd_seal()
    else:
        rep = report(a.store, a.date)
        out = Path(a.out)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(rep, ensure_ascii=False, indent=1, sort_keys=True) + "\n", encoding="utf-8")
        out.with_suffix(".md").write_text(render_md(rep), encoding="utf-8")


if __name__ == "__main__":
    main()
