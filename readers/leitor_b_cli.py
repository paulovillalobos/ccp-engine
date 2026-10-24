"""leitor:b by its command-line client: the family-B reader answers the B3 prompts blind.

    python3 readers/leitor_b_cli.py [--only SLUG] [--model M] [--effort high] [--dir governance/readings]

For each governance/readings/<rule>/prompt.json without leitor-b.json: `reader-b exec`, read-only sandbox, ephemeral, in a
fresh empty working directory (it sees the prompt and the answer schema, no repository, no other reader's answer), and
writes leitor-b.json {"at", "sha256" of the answer text, "answer"}. The engine is the principal's motor field; the model
option is given on the command line and written nowhere. readers/ holds the code that runs a model (D38).
"""
import argparse
import hashlib
import json
import subprocess
import tempfile
import time
from pathlib import Path

READINGS = Path(__file__).resolve().parent.parent / "governance/readings"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only"); ap.add_argument("--model"); ap.add_argument("--effort", default="high"); ap.add_argument("--dir", default=str(READINGS))
    a = ap.parse_args()
    for f in sorted(Path(a.dir).glob("*/prompt.json")):
        d = f.parent
        if (a.only and a.only not in d.name) or (d / "leitor-b.json").exists():
            continue
        body = json.loads(f.read_text(encoding="utf-8"))
        with tempfile.TemporaryDirectory() as empty:  # blind: an empty working root
            schema = Path(empty) / "schema.json"
            schema.write_text(json.dumps(body["schema"]), encoding="utf-8")
            out = Path(empty) / "answer.txt"
            cmd = ["reader-b", "exec", "--skip-git-repo-check", "--sandbox", "read-only", "--ephemeral", "-C", empty, "-c", f'model_reasoning_effort="{a.effort}"']
            cmd += ["-m", a.model] if a.model else []
            res = subprocess.run(cmd + ["--output-schema", str(schema), "-o", str(out), "-"], input=body["prompt"], capture_output=True, text=True, timeout=1800)
            text = out.read_text(encoding="utf-8") if out.exists() else ""
        if not text.strip():
            print(f"{d.name}: no answer (exit {res.returncode}): {res.stderr[-300:]}", flush=True)
            continue
        rec = {"at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(), "answer": text}
        (d / "leitor-b.json").write_text(json.dumps(rec, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        print(f"{d.name}: answered", flush=True)


if __name__ == "__main__":
    main()
