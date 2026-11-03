"""The context of each data-v12 row, for the reader's quote grammar: one line per row {"id", "context"}, the context the
checker reads the row's answer against (read_rules_v3.context_record of make_rule_readings_v12.ctx_of(article), the article
looked up by id in make_rule_readings_v12.SOURCES as tools/measure_rule_readings_v12.py does). No model.

    .venv/bin/python tools/write_contexts.py [FILE.jsonl ...] [--out-dir governance/readings/avaliacao-v13/contexts]

Default: training/data-v12/regra_lida/{dev,sealed,dev_antigo}.jsonl, each to <out-dir>/<set>.jsonl (the set is the file's
name). readers/leitor_a_modal.py --quotes text --contexts <out-dir>/<set>.jsonl builds each row's grammar from its line
(readers/quote_grammar.py): readers/ imports nothing from tools/ (DECISIONS D38), so the contexts go to it as data. A row
with no article, or whose schema cites other passages than its context holds (the article changed since the row was
written), stops the run and nothing is written.
"""
import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT)); sys.path.insert(0, str(ROOT / "tools"))
import make_rule_readings_v12 as data  # noqa: E402  (the article behind each row, and its context)
import read_rules_v3 as v3  # noqa: E402

VERSION = "ccp-write-contexts-0.1"
SETS = [ROOT / f"training/data-v12/regra_lida/{name}.jsonl" for name in ("dev", "sealed", "dev_antigo")]
OUT = ROOT / "governance/readings/avaliacao-v13/contexts"


def articles():
    """{row id: written article}."""
    out = {}
    for pattern, _ in data.SOURCES:
        for ex in data.load(pattern):
            out[f"{data.TASK}:{ex['id']}"] = ex
    return out


def de_enums(s):
    """The «de» enum of every quote object in a schema."""
    if isinstance(s, dict):
        if isinstance(s.get("properties"), dict) and set(s["properties"]) == {"texto", "de"}:
            yield s["properties"]["de"].get("enum")
        for v in s.values():
            yield from de_enums(v)
    elif isinstance(s, list):
        for v in s:
            yield from de_enums(v)


def contexts(path, arts):
    """The lines for one file of rows."""
    out = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        r = json.loads(line)
        ex = arts.get(r["id"])
        if ex is None:
            raise SystemExit(f"{path.name}: {r['id']}: no written article with this id")
        ctx = v3.context_record(data.ctx_of(ex))
        if any(e != sorted(ctx["roles"]) for e in de_enums(r["schema"])):
            raise SystemExit(f"{path.name}: {r['id']}: the schema's passages are not the context's")
        out.append(json.dumps({"id": r["id"], "context": ctx}, ensure_ascii=False, sort_keys=True) + "\n")
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("files", nargs="*", type=Path)
    ap.add_argument("--out-dir", type=Path, default=OUT)
    a = ap.parse_args()
    arts = articles()
    done = {f: contexts(f, arts) for f in (a.files or SETS)}
    a.out_dir.mkdir(parents=True, exist_ok=True)
    for f, lines in done.items():
        target = a.out_dir / f"{f.stem}.jsonl"
        target.write_text("".join(lines), encoding="utf-8")
        print(f"{len(lines)} contexts -> {target.relative_to(ROOT) if target.is_relative_to(ROOT) else target}")


if __name__ == "__main__":
    main()
