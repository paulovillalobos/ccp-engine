"""Phase 15 measurement (DECISIONS D66): the rule readers on data-v12's written articles, read with the protocol v3. No model.

    .venv/bin/python tools/measure_rule_readings_v12.py --date <date> --out reports/measure/regras-v12-<date>.json [--sets dev,sealed]

Gold: training/data-v12/regra_lida/{dev,sealed,dev_antigo}.jsonl (each row's answer: the article's gold with quotes derived
by code). Answers: governance/readings/avaliacao-v12/<set>/<leitor>.jsonl. Each answer is read as the rules factory reads it:
it must pass the factory's checker against the article's context (read_rules_v3.check), and it replicates the gold when the
canonical content is equal (the same rules with quotes and passages aside, or the same «não tipável» reason) — what the
factory settles on. On dev, each answer that does not settle is sorted by the checker's first refusal, or by what differs.
"""
import argparse
import hashlib
import json
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT)); sys.path.insert(0, str(ROOT / "tools"))
import make_rule_readings_v12 as data  # noqa: E402  (the article behind each row, and its context)
import measure_written as mw  # noqa: E402  (Wilson intervals)
import read_rules_v3 as v3  # noqa: E402

VERSION = "ccp-measure-rule-readings-v12-0.1"
SETS = {name: ROOT / f"training/data-v12/regra_lida/{name}.jsonl" for name in ("dev", "sealed", "dev_antigo")}
ANSWERS = ROOT / "governance/readings/avaliacao-v12"
READERS = [("leitor-a13", "base + adaptador v11"), ("leitor-a14", "base + adaptador v12"), ("leitor-b", "Reader B (família B)")]


def articles():
    out = {}
    for pattern, _ in data.SOURCES:
        for ex in data.load(pattern):
            out[f"{data.TASK}:{ex['id']}"] = ex
    return out


def kind_of(err):
    """A checker refusal without its values, so refusals of the same kind count together."""
    return re.sub(r"\d+|«[^»]*»|\[[^\]]*\]|regra \d+, ", "…", err.split(": ", 1)[-1] if err.startswith("regra") else err)[:90]


def differences(a, g):
    if bool(a.get("nao_tipavel")) != bool(g.get("nao_tipavel")):
        return ["não tipável num e regras no outro"]
    if a.get("nao_tipavel"):
        return [f"motivo {a['nao_tipavel'].get('motivo')} em vez de {g['nao_tipavel'].get('motivo')}"]
    A, G = v3.canonical(a)["regras"], v3.canonical(g)["regras"]
    if len(A) != len(G):
        return [f"{len(A)} regras em vez de {len(G)}"]
    out = []
    for x, y in zip(A, G):
        cx = {c["field"]: c for c in x["condicoes"]}
        cy = {c["field"]: c for c in y["condicoes"]}
        out += [f"condição a mais: {k}" for k in sorted(set(cx) - set(cy))]
        out += [f"condição em falta: {k}" for k in sorted(set(cy) - set(cx))]
        out += [f"condição com outro valor: {k}" for k in sorted(set(cx) & set(cy)) if cx[k] != cy[k]]
        px = x["params"].get("threshold", x["params"])
        py = y["params"].get("threshold", y["params"])
        out += [f"parâmetro: {k}" for k in sorted(set(px) | set(py)) if px.get(k) != py.get(k)]
    return out or ["regras pela ordem trocada"]


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
        errs = v3.check(a, data.ctx_of(ex), ex["tipo"])
        if not errs:
            valid += 1
        rep = not errs and v3.replicate(a, g)
        settles += rep
        if errors and not rep:
            kinds.update({f"verificador: {kind_of(errs[0])}"} if errs else set(differences(a, g)))
            by_style[ex.get("estilo")] += 1
    out = {"answered": mw.wil(answered, n), "valid": mw.wil(valid, n), "settles": mw.wil(settles, n)}
    if errors:
        out["errors"] = {"by_kind": dict(sorted(kinds.items(), key=lambda kv: (-kv[1], kv[0]))),
                         "by_style": dict(sorted(by_style.items(), key=lambda kv: (-kv[1], str(kv[0]))))}
    return out


def report(date, sets=None):
    rep = {"tool": VERSION, "protocol": v3.VERSION, "date": date, "sets": {}}
    arts = articles()
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
            ans = {json.loads(line)["id"]: json.loads(line)["answer"] for line in f.read_text(encoding="utf-8").splitlines() if line.strip()}
            s["readers"][leitor] = {"label": label, "answers_sha256": hashlib.sha256(f.read_bytes()).hexdigest(),
                                    **score(rows, ans, arts, errors=(name == "dev"))}
    return rep


def render_md(rep):
    f = lambda x: f"{100 * x['value']:.1f} % [{100 * x['wilson95'][0]:.1f}, {100 * x['wilson95'][1]:.1f}] ({x['k']}/{x['n']})"  # noqa: E731
    L = [f"# Medição — leitura de regras com o protocolo v3 ({rep['date']})", "",
         f"Gerado por tools/measure_rule_readings_v12.py ({rep['tool']}, protocolo {rep['protocol']}). «Válida» = passa o "
         "verificador da fábrica contra o texto do artigo; «assenta» = válida e com o mesmo conteúdo canónico que a de ouro "
         "(as mesmas regras, citações e passagens à parte, ou o mesmo motivo de «não tipável»): o que a fábrica regista. "
         "Intervalos de Wilson a 95 %.", ""]
    for name, s in rep["sets"].items():
        L += [f"## {name} ({s['examples']} artigos)", "", "| leitor | respondidas | válidas | assenta |", "|---|---|---|---|"]
        for k, r in s["readers"].items():
            L.append(f"| {k} ({r['label']}) | {f(r['answered'])} | {f(r['valid'])} | {f(r['settles'])} |")
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
