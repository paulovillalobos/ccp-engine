"""Phase 15 measurement (DECISIONS D67): the rule readers on data-v13's measured sets, read with the protocol 0.4. No model.

    .venv/bin/python tools/measure_rule_readings_v13.py --date <date> --out reports/measure/regras-v13-<date>.json [--sets dev,sealed]

Gold: training/data-v13/regra_lida/{dev,sealed,dev_antigo}.jsonl, data-v12's articles and gold with the prompts rendered in
the protocol 0.4 (make_rule_readings_v13.measured_in_protocol). Answers: governance/readings/avaliacao-v13/<set>/<leitor>.jsonl.
An answer is read as tools/measure_rule_readings_v12.py reads one, with the checker of the protocol 0.4: it settles when it
passes the factory's checker against the article's context and has the gold's canonical content. The answers a reader
decoded under the quote grammar (readers/quote_grammar.py, --quotes text) are counted, so a scaffolded reading shows as one.
"""
import argparse
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT)); sys.path.insert(0, str(ROOT / "tools"))
import make_rule_readings_v12 as v12  # noqa: E402  (the article behind each row, and its context)
import make_rule_readings_v13 as data  # noqa: E402  (PROTOCOL: the protocol data-v13's prompts are rendered with)
import measure_rule_readings_v12 as m12  # noqa: E402  (the articles, and why an answer does not settle)
import measure_written as mw  # noqa: E402  (Wilson intervals)
import read_rules_v3 as v3  # noqa: E402

VERSION = "ccp-measure-rule-readings-v13-0.1"
SETS = {name: ROOT / f"training/data-v13/regra_lida/{name}.jsonl" for name in ("dev", "sealed", "dev_antigo")}
ANSWERS = ROOT / "governance/readings/avaliacao-v13"
READERS = [("leitor-a14", "base + adaptador v12"), ("leitor-a15", "base + adaptador v13"), ("leitor-b", "Reader B (família B)")]


def score(rows, ans, arts, errors):
    n = len(rows)
    answered = valid = settles = 0
    kinds, by_style = Counter(), Counter()
    for r in rows:
        ex = arts[r["id"]]
        g = json.loads(r["answer"])
        a = v3.parse(ans[r["id"]]) if r["id"] in ans else None
        if r["id"] in ans:
            answered += 1
        if a is None:
            if errors and r["id"] in ans:
                kinds["a resposta não é o objeto pedido"] += 1; by_style[ex.get("estilo")] += 1
            continue
        errs = v3.check(a, v12.ctx_of(ex), ex["tipo"], data.PROTOCOL)
        if not errs:
            valid += 1
        rep = not errs and v3.replicate(a, g)
        settles += rep
        if errors and not rep:
            kinds.update({f"verificador: {m12.kind_of(errs[0])}"} if errs else set(m12.differences(a, g)))
            by_style[ex.get("estilo")] += 1
    out = {"answered": mw.wil(answered, n), "valid": mw.wil(valid, n), "settles": mw.wil(settles, n)}
    if errors:
        out["errors"] = {"by_kind": dict(sorted(kinds.items(), key=lambda kv: (-kv[1], kv[0]))),
                         "by_style": dict(sorted(by_style.items(), key=lambda kv: (-kv[1], str(kv[0]))))}
    return out


def report(date, sets=None):
    rep = {"tool": VERSION, "protocol": data.PROTOCOL, "date": date, "sets": {}}
    arts = m12.articles()
    for name, path in SETS.items():
        if (sets is not None and name not in sets) or not path.exists():
            continue
        rows = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
        s = rep["sets"][name] = {"gold": str(path.relative_to(ROOT)), "gold_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                                 "examples": len(rows), "readers": {}}
        for leitor, label in READERS:
            f = ANSWERS / name / f"{leitor}.jsonl"
            if not f.exists():
                continue
            recs = [json.loads(line) for line in f.read_text(encoding="utf-8").splitlines() if line.strip()]
            s["readers"][leitor] = {"label": label, "answers_sha256": hashlib.sha256(f.read_bytes()).hexdigest(),
                                    "quoted_by_grammar": sum(rec.get("quotes") == "text" for rec in recs),
                                    **score(rows, {rec["id"]: rec["answer"] for rec in recs}, arts, errors=(name == "dev"))}
    return rep


def render_md(rep):
    f = lambda x: f"{100 * x['value']:.1f} % [{100 * x['wilson95'][0]:.1f}, {100 * x['wilson95'][1]:.1f}] ({x['k']}/{x['n']})"  # noqa: E731
    g = lambda r: "" if not r["quoted_by_grammar"] else ", citações pela gramática" + ("" if r["quoted_by_grammar"] == r["answered"]["k"] else f" em {r['quoted_by_grammar']}")  # noqa: E731
    L = [f"# Medição — leitura de regras com o protocolo v3 0.4 ({rep['date']})", "",
         f"Gerado por tools/measure_rule_readings_v13.py ({rep['tool']}, protocolo {rep['protocol']}). Os artigos e o ouro "
         "de data-v12, os enunciados no protocolo 0.4. «Válida» = passa o verificador da fábrica contra o texto do artigo; "
         "«assenta» = válida e com o mesmo conteúdo canónico que a de ouro (as mesmas regras, citações e passagens à parte, ou "
         "o mesmo motivo de «não tipável»): o que a fábrica regista. «Citações pela gramática» = a resposta foi descodificada "
         "com a gramática que só deixa citar o texto (readers/quote_grammar.py). Intervalos de Wilson a 95 %.", ""]
    for name, s in rep["sets"].items():
        L += [f"## {name} ({s['examples']} artigos)", "", "| leitor | respondidas | válidas | assenta |", "|---|---|---|---|"]
        for k, r in s["readers"].items():
            L.append(f"| {k} ({r['label']}{g(r)}) | {f(r['answered'])} | {f(r['valid'])} | {f(r['settles'])} |")
        L.append("")
        for k, r in s["readers"].items():
            if "errors" in r:
                L += [f"Por que não assentam as de {k}: " + "; ".join(f"{e} {n}" for e, n in r["errors"]["by_kind"].items()) + ".",
                      "Por estilo: " + "; ".join(f"{e} {n}" for e, n in r["errors"]["by_style"].items()) + ".", ""]
    return "\n".join(L) + "\n"


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--date", required=True); ap.add_argument("--out", required=True); ap.add_argument("--sets")
    a = ap.parse_args()
    rep = report(a.date, set(a.sets.split(",")) if a.sets else None)
    out = Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(rep, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    out.with_suffix(".md").write_text(render_md(rep), encoding="utf-8")
    print(render_md(rep))


if __name__ == "__main__":
    main()
