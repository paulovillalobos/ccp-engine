"""Phase 4 T3: the reader before and after its adapter (leitor:a = base, leitor:a2 = base + amalia-ccp-lei-v1), measured
from stored answers only. No model is called here: the answers are files the readers wrote (readers/leitor_a_modal.py).

    .venv/bin/python tools/measure_reader.py --date <date> --out reports/measure/amalia-v1-<date>.json   (+ .md)

Answers read (governance/readings/avaliacao-v1/, sealed by tools/measure.py seal, D42):
  tarefas/<task>/leitor-a.jsonl, leitor-a2.jsonl   one line per held-out example of training/data/<task>/held_out.jsonl
  regras/<rule slug>/leitor-a2.json                 the 18 B3 prompts (governance/readings/<slug>/prompt.json); the base
                                                    answers are the B3 ones (governance/readings/<slug>/leitor-a.json),
                                                    produced by the same reader code, temperature 0, guided JSON
  casos/<case>/leitor-a2.json                       the 20 B5 cases (governance/readings/casos/<case>/prompt.json); base
                                                    and leitor:b answers are the B5 ones
Tables:
  a) per task, held_out: exact accuracy (the answer's canonical JSON equals the generator's answer), base vs v1, each with
     its 95 % Wilson interval; an unparseable or missing answer counts as wrong
  b) the 18 rules: agreement with leitor:b's reading and with the settled rule, exact (passages, conditions, params) and
     of direction (the value the rule turns on: tools/read_rules.key_param), base vs v1
  c) the 20 cases, as in B5, with leitor:a2 as third column: agreement A-B, A2-B, A-A2 (exact; direction = breach or
     not) over the (case, rule) pairs both sides answered, and agreement with the expected verdicts (pairs A and B agree)
Deterministic: sorted, no clock; the date is an argument.
"""
import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "tools"))
import measure  # noqa: E402  (tools/measure.py: wilson, annotations; no model)
import read_rules  # noqa: E402  (tools/read_rules.py: TARGETS, slug, parse_answer, key_param; no model)
from engine.canon import canonical  # noqa: E402

VERSION = "ccp-measure-reader-0.1"
EVAL = ROOT / "governance/readings/avaliacao-v1"
DATA = ROOT / "training/data"
TASKS = ["escolha_passagem", "texto_vigente", "nota_dr", "remissao", "regra_tipada"]
READERS = ["leitor-a", "leitor-a2"]


def norm(x):
    """The value a comparison reads: an integral float is that integer (150000.0 is 150000, as JSON and Python equality
    say; B3's uphold compares with ==), a list of objects is sorted by canonical form and «passagens» is a set (as
    tools/read_rules.parse_answer reads a reading: sorted passages, conditions in canonical order)."""
    if isinstance(x, float) and x.is_integer():
        return int(x)
    if isinstance(x, dict):
        return {k: (sorted(norm(v)) if k in ("passagens", "passages") and isinstance(v, list) else norm(v)) for k, v in x.items()}
    if isinstance(x, list):
        items = [norm(v) for v in x]
        return sorted(items, key=canonical) if items and all(isinstance(v, dict) for v in items) else items
    return x


def canon_answer(text):
    try:
        return canonical(norm(json.loads(text)))
    except (json.JSONDecodeError, TypeError):
        return None


def wil(k, n):
    v, ci = measure.wilson(k, n)
    return {"k": k, "n": n, "value": v, "wilson95": ci}


def tasks_table():
    out = {}
    for task in TASKS:
        gold = {}
        f = DATA / task / "held_out.jsonl"
        for line in f.read_text(encoding="utf-8").splitlines() if f.exists() else []:
            ex = json.loads(line)
            gold[ex["id"]] = canonical(norm(json.loads(ex["answer"])))
        row = {"held_out": len(gold)}
        for r in READERS:
            af = EVAL / "tarefas" / task / f"{r}.jsonl"
            got = {}
            for line in af.read_text(encoding="utf-8").splitlines() if af.exists() else []:
                a = json.loads(line)
                got.setdefault(a["id"], canon_answer(a["answer"]))
            ok = sum(1 for i, g in gold.items() if got.get(i) == g)
            row[r] = dict(wil(ok, len(gold)), answered=sum(1 for i in gold if i in got), unparseable=sum(1 for i in gold if i in got and got[i] is None))
        out[task] = row
    return out


def rules_table():
    rules = {}
    for f in sorted((ROOT / "rules/regra").glob("*.json")):
        o = json.loads(f.read_text(encoding="utf-8"))
        if o["id"] not in rules or o["revision"] > rules[o["id"]]["revision"]:
            rules[o["id"]] = o
    rows, totals = {}, {r: {"vs_b_exact": 0, "vs_b_direction": 0, "vs_settled_exact": 0, "vs_settled_direction": 0, "parsed": 0} for r in READERS}
    settled_n = 0
    for t in read_rules.TARGETS:
        s = read_rules.slug(t["rule"])
        d = ROOT / "governance/readings" / s
        b_rec = json.loads((d / "leitor-b.json").read_text(encoding="utf-8")) if (d / "leitor-b.json").exists() else None
        b = read_rules.parse_answer(b_rec, t) if b_rec else None
        rule = rules.get(t["rule"])
        settled = None
        if rule and rule["state"] == "settled":
            settled = {"passages": sorted({c["passage"] for c in rule["passages"]}), "type": rule["type"],
                       "conditions": read_rules.norm_conditions(rule["conditions"]), "params": rule["params"]}
            settled_n += 1
        row = {"state": rule["state"] if rule else None}
        for r in READERS:
            path = (d / "leitor-a.json") if r == "leitor-a" else (EVAL / "regras" / s / "leitor-a2.json")
            rec = json.loads(path.read_text(encoding="utf-8")) if path.exists() else None
            a = read_rules.parse_answer(rec, t) if rec else None
            same = lambda x, y: x is not None and y is not None and canonical(norm(x)) == canonical(norm(y))  # noqa: E731
            sdir = lambda x, y: x is not None and y is not None and read_rules.key_param(x) == read_rules.key_param(y)  # noqa: E731
            cell = {"parsed": a is not None, "vs_b_exact": same(a, b), "vs_b_direction": sdir(a, b),
                    "vs_settled_exact": same(a, settled) if settled else None, "vs_settled_direction": sdir(a, settled) if settled else None}
            row[r] = cell
            for k in totals[r]:
                totals[r][k] += 1 if cell.get(k) else 0
        rows[t["rule"]] = row
    n = len(read_rules.TARGETS)
    summary = {r: {"vs_b_exact": wil(totals[r]["vs_b_exact"], n), "vs_b_direction": wil(totals[r]["vs_b_direction"], n),
                   "vs_settled_exact": wil(totals[r]["vs_settled_exact"], settled_n), "vs_settled_direction": wil(totals[r]["vs_settled_direction"], settled_n),
                   "parsed": totals[r]["parsed"]} for r in READERS}
    return {"rules": rows, "summary": summary, "n": n, "settled": settled_n}


def cases_table():
    casos = ROOT / "governance/readings/casos"
    triples = []
    for d in sorted(p for p in casos.iterdir() if p.is_dir() and (p / "prompt.json").exists()) if casos.exists() else []:
        rules = json.loads((d / "prompt.json").read_text(encoding="utf-8"))["rules"]
        a, _ = measure.annotations(d / "leitor-a.json", rules)
        b, _ = measure.annotations(d / "leitor-b.json", rules)
        a2, _ = measure.annotations(EVAL / "casos" / d.name / "leitor-a2.json", rules)
        for rid in rules:
            triples.append((d.name, rid, a.get(rid), b.get(rid), a2.get(rid)))

    def agree(i, j):
        both = [t for t in triples if t[i] is not None and t[j] is not None]
        exact = sum(1 for t in both if t[i] == t[j])
        direc = sum(1 for t in both if (t[i] == "nao_cumpre") == (t[j] == "nao_cumpre"))
        return {"answered_by_both": len(both), "exact": wil(exact, len(both)), "direction": wil(direc, len(both))}

    expected = [t for t in triples if t[2] is not None and t[2] == t[3] and t[2] != "nao_aplica"]
    return {"cases": len({t[0] for t in triples}), "pairs": len(triples),
            "A_vs_B": agree(2, 3), "A2_vs_B": agree(4, 3), "A_vs_A2": agree(2, 4),
            "vs_expected": {"pairs": len(expected), "leitor-a": wil(sum(1 for t in expected if t[2] == t[2]), len(expected)),
                            "leitor-a2": wil(sum(1 for t in expected if t[4] == t[2]), len(expected))},
            "answered": {"leitor-a": sum(1 for t in triples if t[2] is not None), "leitor-b": sum(1 for t in triples if t[3] is not None),
                         "leitor-a2": sum(1 for t in triples if t[4] is not None)}}


def report(date):
    index = json.loads((DATA / "INDEX.json").read_text(encoding="utf-8"))
    return {"tool": VERSION, "date": date, "readers": {"leitor-a": "leitor:a (base)", "leitor-a2": "leitor:a2 (base + adaptador v1)"},
            "training_index_examples": index["examples"], "tasks": tasks_table(), "rules": rules_table(), "cases": cases_table()}


def render_md(rep):
    f = lambda w: "—" if w["value"] is None else f"{round(100 * w['value'], 1)} % [{round(100 * w['wilson95'][0], 1)}, {round(100 * w['wilson95'][1], 1)}] ({w['k']}/{w['n']})"  # noqa: E731
    L = [f"# Leitor A antes e depois do adaptador v1 — {rep['date']}", "",
         f"Gerado por tools/measure_reader.py ({rep['tool']}) a partir das respostas guardadas em governance/readings/avaliacao-v1/ "
         "(e das de B3/B5 para a base e o leitor:b). Temperatura 0, JSON guiado. IC de Wilson a 95 %.", "",
         "## a) Tarefas, conjunto reservado (exatidão)", "", "| tarefa | n | base | v1 |", "|---|---|---|---|"]
    for t, row in rep["tasks"].items():
        L.append(f"| {t} | {row['held_out']} | {f(row['leitor-a'])} | {f(row['leitor-a2'])} |")
    L += ["", "Linha por tarefa:"]
    for t, row in rep["tasks"].items():
        b, v = row["leitor-a"], row["leitor-a2"]
        L.append(f"- {t}: base {f(b)} → v1 {f(v)}")
    s = rep["rules"]["summary"]
    L += ["", f"## b) As {rep['rules']['n']} regras de B3", "", "| medida | base | v1 |", "|---|---|---|",
          f"| acordo exato com o leitor:b | {f(s['leitor-a']['vs_b_exact'])} | {f(s['leitor-a2']['vs_b_exact'])} |",
          f"| acordo de direção com o leitor:b | {f(s['leitor-a']['vs_b_direction'])} | {f(s['leitor-a2']['vs_b_direction'])} |",
          f"| exato com a regra settled ({rep['rules']['settled']}) | {f(s['leitor-a']['vs_settled_exact'])} | {f(s['leitor-a2']['vs_settled_exact'])} |",
          f"| direção com a regra settled | {f(s['leitor-a']['vs_settled_direction'])} | {f(s['leitor-a2']['vs_settled_direction'])} |", "",
          "| regra | estado | base: exato B | base: direção B | v1: exato B | v1: direção B |", "|---|---|---|---|---|---|"]
    yn = lambda x: "sim" if x else "não"  # noqa: E731
    for rid, row in rep["rules"]["rules"].items():
        L.append(f"| {rid} | {row['state']} | {yn(row['leitor-a']['vs_b_exact'])} | {yn(row['leitor-a']['vs_b_direction'])} | {yn(row['leitor-a2']['vs_b_exact'])} | {yn(row['leitor-a2']['vs_b_direction'])} |")
    c = rep["cases"]
    L += ["", f"## c) Os {c['cases']} casos de fixtures/measure ({c['pairs']} pares caso-regra), como em B5 com o leitor:a2", "",
          "| par | respondidos por ambos | exato | direção |", "|---|---|---|---|"]
    for k, lab in (("A_vs_B", "leitor:a vs leitor:b"), ("A2_vs_B", "leitor:a2 vs leitor:b"), ("A_vs_A2", "leitor:a vs leitor:a2")):
        L.append(f"| {lab} | {c[k]['answered_by_both']} | {f(c[k]['exact'])} | {f(c[k]['direction'])} |")
    L += ["", f"Veredictos esperados (pares em que A e B concordam, sem nao_aplica): {c['vs_expected']['pairs']}; o leitor:a2 dá o mesmo em "
          f"{f(c['vs_expected']['leitor-a2'])} (o leitor:a coincide por construção)."]
    return "\n".join(L) + "\n"


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--date", required=True); ap.add_argument("--out", required=True)
    a = ap.parse_args()
    rep = report(a.date)
    out = Path(a.out); out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(rep, ensure_ascii=False, indent=1, sort_keys=True) + "\n", encoding="utf-8")
    out.with_suffix(".md").write_text(render_md(rep), encoding="utf-8")
    print(render_md(rep))


if __name__ == "__main__":
    main()
