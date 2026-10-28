"""Phase 14 measurement (DECISIONS D65): the rule readers on data-v11's dev and sealed articles and on data-v10's held out. No model.

    .venv/bin/python tools/measure_rule_readings_v11.py --date <date> --out reports/measure/regras-v11-<date>.json [--sets dev]

Gold: training/data-v11/regra_lida/{dev,sealed}.jsonl and training/data-v10/regra_lida/held_out.jsonl. Answers:
governance/readings/avaliacao-v11/<set>/<leitor>.jsonl. Scored as tools/measure_rule_readings.py scores (D43, rule by rule in
canonical form), plus «replicates (D64)»: the same rules with the passages aside, every rule citing the target passage — what
the rules factory now settles on. On dev only, each reading that is not content exact is sorted by what differs, rule by rule
(the rules paired by their days or limit, then by canonical form): which condition field is missing, extra or has another
value; which param differs; or the number of rules.
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
import measure_rule_readings as mr  # noqa: E402  (D63's scoring)
import measure_written as mw  # noqa: E402  (Wilson intervals)
import read_rules as rr  # noqa: E402
from engine.canon import canonical  # noqa: E402

VERSION = "ccp-measure-rule-readings-v11-0.1"
SETS = {"dev": ROOT / "training/data-v11/regra_lida/dev.jsonl", "sealed": ROOT / "training/data-v11/regra_lida/sealed.jsonl",
        "held_out_v10": ROOT / "training/data-v10/regra_lida/held_out.jsonl"}
ANSWERS = ROOT / "governance/readings/avaliacao-v11"
READERS = [("leitor-a12", "base + adaptador v10"), ("leitor-a13", "base + adaptador v11"), ("leitor-b", "Reader B (família B)")]
ALVO = re.compile(r"fixa a passagem (\S+): ")


def gold_of(path):
    rows = [json.loads(l) for l in path.read_text(encoding="utf-8").splitlines() if l.strip()]
    out = {}
    for r in rows:
        t = mr.target_of(r)
        out[r["id"]] = (t, rr.parse_answers({"answer": r["answer"]}, t), ALVO.search(r["prompt"]).group(1), r.get("estilo"))
    return out


def bare(r):
    return {**r, "passages": []}


def paired(a, g):
    key = lambda r: (str(rr.key_param(r)), canonical(rr.canonical_reading(bare(r))))  # noqa: E731
    return list(zip(sorted(a, key=key), sorted(g, key=key)))


def differences(a, g):
    """What differs between a reading and the gold, as short labels (Counter keys)."""
    if len(a) != len(g):
        return ["número de regras " + ("a mais" if len(a) > len(g) else "a menos")]
    out = []
    for x, y in paired(a, g):
        cx = {c["field"]: canonical(rr.canonical_reading({"passages": [], "type": x["type"], "conditions": [c], "params": {}})["conditions"])
              for c in x["conditions"]}
        cy = {c["field"]: canonical(rr.canonical_reading({"passages": [], "type": y["type"], "conditions": [c], "params": {}})["conditions"])
              for c in y["conditions"]}
        for f in sorted(set(cx) | set(cy)):
            if f not in cx:
                out.append(f"condição em falta: {f}")
            elif f not in cy:
                out.append(f"condição a mais: {f}")
            elif cx[f] != cy[f]:
                out.append(f"condição com outro valor: {f}")
        px, py = rr.canonical_reading(x)["params"], rr.canonical_reading(y)["params"]
        if x["type"] == "limiar":
            tx, ty = px.get("threshold") or {}, py.get("threshold") or {}
            out += [f"limiar: {k}" for k in sorted(set(tx) | set(ty)) if tx.get(k) != ty.get(k)]
        else:
            out += [f"prazo: {k}" for k in sorted(set(px) | set(py)) if px.get(k) != py.get(k)]
    return out


def score(gold, ans, errors):
    base = mr.score({i: (t, g) for i, (t, g, _, _) in gold.items()}, ans)
    rep, kinds, by_style = 0, Counter(), Counter()
    for i, (t, g, alvo, estilo) in gold.items():
        a = rr.parse_answers({"answer": ans[i]}, t) if i in ans else None
        if a is None:
            continue
        ok = len(a) == len(g) and all(alvo in x["passages"] for x in a) and \
            sorted(canonical(rr.canonical_reading(bare(x))) for x in a) == sorted(canonical(rr.canonical_reading(bare(y))) for y in g)
        rep += ok
        if errors and sorted(canonical(rr.canonical_reading(bare(x))) for x in a) != sorted(canonical(rr.canonical_reading(bare(y))) for y in g):
            kinds.update(set(differences(a, g)))
            by_style[estilo] += 1
    out = {**base, "replicates_d64": mw.wil(rep, len(gold))}
    if errors:
        out["errors"] = {"by_kind": dict(sorted(kinds.items(), key=lambda kv: (-kv[1], kv[0]))),
                         "by_style": dict(sorted(by_style.items(), key=lambda kv: (-kv[1], str(kv[0]))))}
    return out


def report(date, sets=None):
    rep = {"tool": VERSION, "date": date, "sets": {}}
    for name, path in SETS.items():
        if (sets is not None and name not in sets) or not path.exists():
            continue
        gold = gold_of(path)
        s = rep["sets"][name] = {"gold": str(path.relative_to(ROOT)), "gold_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                                 "examples": len(gold), "readers": {}}
        for leitor, label in READERS:
            f = ANSWERS / name / f"{leitor}.jsonl"
            if not f.exists():
                continue
            ans = {json.loads(l)["id"]: json.loads(l)["answer"] for l in f.read_text(encoding="utf-8").splitlines() if l.strip()}
            s["readers"][leitor] = {"label": label, "answers_sha256": hashlib.sha256(f.read_bytes()).hexdigest(),
                                    **score(gold, ans, errors=(name == "dev"))}
    return rep


def render_md(rep):
    f = lambda x: f"{100 * x['value']:.1f} % [{100 * x['wilson95'][0]:.1f}, {100 * x['wilson95'][1]:.1f}] ({x['k']}/{x['n']})"  # noqa: E731
    L = [f"# Medição — leitura de regras, v11 ({rep['date']})", "",
         f"Gerado por tools/measure_rule_readings_v11.py ({rep['tool']}). Cada leitura comparada com a de ouro em forma canónica, "
         "regra a regra (D43); «replica (D64)» = as mesmas regras sem as passagens, todas citando a passagem-alvo. Intervalos de "
         "Wilson a 95 %.", ""]
    for name, s in rep["sets"].items():
        L += [f"## {name} ({s['examples']} artigos)", "",
              "| leitor | regras exatas | replica (D64) | conteúdo exato | número de regras certo | dias ou limites certos | inválidas |",
              "|---|---|---|---|---|---|---|"]
        for k, r in s["readers"].items():
            L.append(f"| {k} ({r['label']}) | {f(r['rules_exact'])} | {f(r['replicates_d64'])} | {f(r['content_exact'])} | "
                     f"{f(r['count_exact'])} | {f(r['days_exact'])} | {r['invalid']} |")
        L.append("")
        for k, r in s["readers"].items():
            if "errors" in r:
                L += [f"Erros de {k} (leituras sem conteúdo exato; uma leitura conta uma vez em cada tipo): "
                      + "; ".join(f"{e} {n}" for e, n in r["errors"]["by_kind"].items()) + ".",
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
