"""leitor:b by its command-line client: the family-B reader answers the B3 prompts blind.

    python3 readers/leitor_b_cli.py [--only SLUG] [--model M] [--effort high] [--dir governance/readings]
    python3 readers/leitor_b_cli.py --jsonl FILE --out FILE [--workers 4]   one line per example {"id", "at", "sha256", "answer"}

For each governance/readings/<rule>/prompt.json without leitor-b.json: `reader-b exec`, read-only sandbox, ephemeral, in a
fresh empty working directory (it sees the prompt and the answer schema, no repository, no other reader's answer), and
writes leitor-b.json {"at", "sha256" of the answer text, "answer"}. The engine is the principal's motor field; the model
option is given on the command line and written nowhere. readers/ holds the code that runs a model (D38).
JSONL mode (D52, the ceiling on the written questions): the same blind call per example of a file {id, prompt, schema};
resumable (an id already in --out is skipped; answers are written as they come, a call stuck 30 minutes is skipped). Reader B's structured output wants every property listed, so the schema is
made strict (each optional property required and nullable, no pattern or length bounds); the measurement drops nulls.
"""
import concurrent.futures
import argparse
import hashlib
import json
import subprocess
import tempfile
import time
from pathlib import Path

READINGS = Path(__file__).resolve().parent.parent / "governance/readings"


def strict(s):
    """The schema in the form Reader B's structured output accepts: every property required, an optional one nullable."""
    if not isinstance(s, dict):
        return s
    s = {k: strict(v) if isinstance(v, dict) else [strict(x) for x in v] if isinstance(v, list) else v for k, v in s.items()
         if k not in ("pattern", "minItems", "maxItems")}
    if s.get("type") == "object" and "properties" in s:
        req = set(s.get("required", []))
        s["properties"] = {k: v if k in req else {"anyOf": [v, {"type": "null"}]} for k, v in s["properties"].items()}
        s["required"] = list(s["properties"]); s["additionalProperties"] = False
    return s


def ask(prompt, schema, a):
    with tempfile.TemporaryDirectory() as empty:  # blind: an empty working root
        sf = Path(empty) / "schema.json"
        sf.write_text(json.dumps(schema), encoding="utf-8")
        out = Path(empty) / "answer.txt"
        cmd = ["reader-b", "exec", "--skip-git-repo-check", "--sandbox", "read-only", "--ephemeral", "-C", empty, "-c", f'model_reasoning_effort="{a.effort}"']
        cmd += ["-m", a.model] if a.model else []
        try:
            res = subprocess.run(cmd + ["--output-schema", str(sf), "-o", str(out), "-"], input=prompt, capture_output=True, text=True, timeout=1800)
        except subprocess.TimeoutExpired:  # one stuck call is skipped, not the batch; a rerun asks it again
            return "", subprocess.CompletedProcess(cmd, -1, "", "timed out after 1800 s")
        return (out.read_text(encoding="utf-8") if out.exists() else ""), res


def jsonl_mode(a):
    out = Path(a.out)
    done = {json.loads(l)["id"] for l in out.read_text(encoding="utf-8").splitlines() if l.strip()} if out.exists() else set()
    todo = [e for e in (json.loads(l) for l in Path(a.jsonl).read_text(encoding="utf-8").splitlines() if l.strip()) if e["id"] not in done]

    def one(e):
        return e, ask(e["prompt"], strict(e["schema"]), a)

    with concurrent.futures.ThreadPoolExecutor(a.workers) as pool, out.open("a", encoding="utf-8") as fh:
        for e, (text, res) in (f.result() for f in concurrent.futures.as_completed([pool.submit(one, e) for e in todo])):
            if not text.strip():
                print(f"{e['id']}: no answer (exit {res.returncode}): {res.stderr[-200:]}", flush=True)
                continue
            fh.write(json.dumps({"id": e["id"], "at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                                 "sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(), "answer": text}, ensure_ascii=False) + "\n")
            fh.flush()
    print(f"{len(todo)} asked -> {out}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only"); ap.add_argument("--model"); ap.add_argument("--effort", default="high"); ap.add_argument("--dir", default=str(READINGS))
    ap.add_argument("--jsonl"); ap.add_argument("--out"); ap.add_argument("--workers", type=int, default=4)
    a = ap.parse_args()
    if a.jsonl:
        return jsonl_mode(a)
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
