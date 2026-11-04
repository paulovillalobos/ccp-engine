"""Phase 17 measurement (DECISIONS D68): v14 beside v13 and leitor:b on data-v13's measured sets, read with the protocol 0.4.
No model.

    .venv/bin/python tools/measure_rule_readings_v14.py --date <date> --out reports/measure/regras-v14-<date>.json [--sets dev,sealed]

tools/measure_rule_readings_v13.py's reading and score, with each reader's answers where they were written: v14's
(leitor-a16) in governance/readings/avaliacao-v14/<set>/, v13's and leitor:b's in governance/readings/avaliacao-v13/<set>/,
so v13's report keeps recomputing as it was committed.
"""
import argparse
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT)); sys.path.insert(0, str(ROOT / "tools"))
import make_rule_readings_v13 as data  # noqa: E402  (PROTOCOL)
import measure_rule_readings_v12 as m12  # noqa: E402  (the articles)
import measure_rule_readings_v13 as m13  # noqa: E402  (SETS, score, render_md)

VERSION = "ccp-measure-rule-readings-v14-0.1"
READERS = [("leitor-a15", "base + adaptador v13", ROOT / "governance/readings/avaliacao-v13"),
           ("leitor-a16", "base + adaptador v14 (de v13)", ROOT / "governance/readings/avaliacao-v14"),
           ("leitor-b", "Reader B (família B)", ROOT / "governance/readings/avaliacao-v13")]


def report(date, sets=None):
    rep = {"tool": VERSION, "protocol": data.PROTOCOL, "date": date, "sets": {}}
    arts = m12.articles()
    for name, path in m13.SETS.items():
        if (sets is not None and name not in sets) or not path.exists():
            continue
        rows = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
        s = rep["sets"][name] = {"gold": str(path.relative_to(ROOT)), "gold_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                                 "examples": len(rows), "readers": {}}
        for leitor, label, where in READERS:
            f = where / name / f"{leitor}.jsonl"
            if not f.exists():
                continue
            recs = [json.loads(line) for line in f.read_text(encoding="utf-8").splitlines() if line.strip()]
            s["readers"][leitor] = {"label": label, "answers": str(f.relative_to(ROOT)), "answers_sha256": hashlib.sha256(f.read_bytes()).hexdigest(),
                                    "quoted_by_grammar": sum(rec.get("quotes") == "text" for rec in recs),
                                    **m13.score(rows, {rec["id"]: rec["answer"] for rec in recs}, arts, errors=(name == "dev"))}
    return rep


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--date", required=True); ap.add_argument("--out", required=True); ap.add_argument("--sets")
    a = ap.parse_args()
    rep = report(a.date, set(a.sets.split(",")) if a.sets else None)
    out = Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(rep, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    md = m13.render_md(rep).replace("tools/measure_rule_readings_v13.py", "tools/measure_rule_readings_v14.py")
    out.with_suffix(".md").write_text(md, encoding="utf-8")
    print(md)


if __name__ == "__main__":
    main()
