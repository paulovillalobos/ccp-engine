"""Checks the written questions (D52) against the label rules of training/written-questions/LABELS.md. No model.

    .venv/bin/python tools/check_written_questions.py        exit 1 and one line per problem

Each line: the keys of LABELS.md only; ids unique; `hoje` an ISO date; facts in the engine's vocabulary; a field in
at most one of factos / ambiguos / contraditorios; ambiguos and contraditorios lists of allowed values (a value field
may hold the raw amount as written); every citation an act or passage id in law/.
"""
import json
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
import read_rules  # noqa: E402  (the engine's fact vocabulary)

DIR = ROOT / "training/written-questions"
KEYS = {"id", "hoje", "pergunta", "factos", "ambiguos", "contraditorios", "citacoes", "fenomenos"}
FIELDS = list(read_rules.VOCAB) + ["preco_base", "data_inicio_procedimento"]
TAGS = set("typo sem_acentos pre_ao pt_br ditado abreviaturas telegrafico carta multi seguimento premissa citacao_errada limiar_antigo iva "
           "intervalo por_item contradicao nao_sabe distrator lugar_ambiguo entidade_ambigua objeto_ambiguo concurso_nu lancamento sem_factos".split())


def known_ids():
    ids = {p.name.rsplit(".r", 1)[0] for p in (ROOT / "law/passagem").glob("*.json")}
    ids |= {p.name.rsplit(".r", 1)[0].removeprefix("norma-") for p in (ROOT / "law/norma").glob("*.json")}
    return {i.replace("-art", ":art", 1) if "-art" in i else i for i in ids}


def ok_value(field, v, raw_ok):
    if field in read_rules.VOCAB:
        return v in read_rules.VOCAB[field]
    if field == "preco_base":
        return isinstance(v, (int, float)) and not isinstance(v, bool) or (raw_ok and isinstance(v, str))
    try:
        date.fromisoformat(v)
        return True
    except (TypeError, ValueError):
        return False


def check(rows, ids):
    out, seen = [], set()
    for f, n, q in rows:
        at = f"{f}:{n} {q.get('id')}"
        if set(q) - KEYS or not {"id", "hoje", "pergunta", "factos"} <= set(q):
            out.append(f"{at}: keys {sorted(q)}")
            continue
        if q["id"] in seen:
            out.append(f"{at}: duplicate id")
        seen.add(q["id"])
        try:
            date.fromisoformat(q["hoje"])
        except ValueError:
            out.append(f"{at}: hoje {q['hoje']!r}")
        used = []
        for k, v in q["factos"].items():
            used.append(k)
            if k not in FIELDS or not ok_value(k, v, False):
                out.append(f"{at}: factos.{k} = {v!r}")
        for part in ("ambiguos", "contraditorios"):
            for k, vs in (q.get(part) or {}).items():
                used.append(k)
                if k not in FIELDS or not isinstance(vs, list) or not vs or not all(ok_value(k, v, True) for v in vs):
                    out.append(f"{at}: {part}.{k} = {vs!r}")
                if part == "contraditorios" and len(vs) != 2:
                    out.append(f"{at}: contraditorios.{k} needs two values")
        if len(used) != len(set(used)):
            out.append(f"{at}: a field in more than one of factos / ambiguos / contraditorios")
        for c in q.get("citacoes") or []:
            if c not in ids:
                out.append(f"{at}: citação {c!r} not in law/")
        for t in q.get("fenomenos") or []:
            if t not in TAGS:
                out.append(f"{at}: fenómeno {t!r}")
    return out


def load():
    rows = []
    for f in sorted(DIR.glob("batch-*.jsonl")):
        for n, line in enumerate(f.read_text(encoding="utf-8").splitlines(), 1):
            if line.strip():
                rows.append((f.name, n, json.loads(line)))
    return rows


def main():
    rows = load()
    problems = check(rows, known_ids())
    for p in problems:
        print(p)
    print(f"{len(rows)} questions, {len(problems)} problem(s)")
    sys.exit(1 if problems else 0)


if __name__ == "__main__":
    main()
