"""leitor:a / leitor:a2 on Modal: the family-A reader answers prompts with guided JSON (vLLM, temperature 0, one batch).

    <a Python 3.12 venv with modal>/bin/modal run readers/leitor_a_modal.py [--only SLUG] [--dir governance/readings/casos]
        [--lora v1|v2|v3|v4] [--out-dir DIR] [--jsonl FILE --out FILE]

readers/ holds the code that runs a model (DECISIONS D38): nothing in engine/, tools/ or verify.py imports it, and
verify's code guard keeps it that way.

Directory mode (B3, B5): reads <dir>/<key>/prompt.json, skips a key that already has its answer file, sends the prompts
and their answer schemas to one GPU container, and writes each answer as <out-dir or dir>/<key>/<leitor>.json
{"at", "sha256" of the answer text, "answer"}: the same record leitor:b gets. <leitor> is leitor-a (the base model) or,
with --lora v1, leitor-a2 (the base model + the adapter amalia-ccp-lei-v1 from the Modal volume amalia-lora; phase 4); with
--lora v2, leitor-a3 (+ amalia-ccp-lei-v2; phase 5, D46).
JSONL mode (phase 4, T3): reads a file of examples {id, prompt, schema, ...} (training/data/<task>/held_out.jsonl) and
writes one line per example {"id", "at", "sha256", "answer"} to --out.
A prompt longer than the window is skipped and listed, never truncated. The grammar admits no free whitespace, set on
the engine (attempt 1, free whitespace: 8 of 18 answers looped on blanks until max_tokens; attempt 2, the flag per
request only: 7 of 18, the flag was not honoured; both kept as leitor-a.attempt1.json / attempt2.json). The model,
revision and adapter are the principal's motor (governance/principals.json, leitor:a / leitor:a2); nothing here decides:
tools/read_rules.py record and tools/measure_reader.py read the answer files. Self-contained on purpose (the Modal
client venv does not carry the engine's dependencies).
"""
import hashlib
import json
import time
from pathlib import Path

import modal

MODEL = "amalia-llm/AMALIA-9B-0626-DPO"
REVISION = "c4614b9b5c7b4fe303fa20902e692fc7dface640"  # leitor:a motor versao c4614b9b5c7b
ADAPTERS = {"v1": "amalia-ccp-lei-v1", "v2": "amalia-ccp-lei-v2", "v3": "amalia-ccp-lei-v3", "v4": "amalia-ccp-lei-v4", "v5": "amalia-ccp-lei-v5", "v6": "amalia-ccp-lei-v6", "v7": "amalia-ccp-lei-v7", "v7r64": "amalia-ccp-lei-v7r64", "v8": "amalia-ccp-lei-v8", "v9": "amalia-ccp-lei-v9", "v10": "amalia-ccp-lei-v10"}  # adapter directories in the volume amalia-lora
LEITOR_OF = {"": "leitor-a", "v1": "leitor-a2", "v2": "leitor-a3", "v3": "leitor-a4", "v4": "leitor-a5", "v5": "leitor-a6", "v6": "leitor-a7", "v7": "leitor-a8", "v7r64": "leitor-a9", "v8": "leitor-a10", "v9": "leitor-a11", "v10": "leitor-a12"}  # base, phase 4, 5 (D46), 6 (D47), 7 (D49), 8 (D50, never trained), 9 (D52)
WINDOW, MAX_TOKENS = 32768, 1500
SYSTEM = "Responde unicamente com o objeto JSON pedido, sem texto antes nem depois."
READINGS = Path(__file__).resolve().parent.parent / "governance/readings"

image = modal.Image.from_registry("nvidia/cuda:12.9.1-devel-ubuntu22.04", add_python="3.12").pip_install(
    "vllm==0.30.0", "huggingface_hub[hf_transfer]")
image = image.env({"HF_HUB_ENABLE_HF_TRANSFER": "1", "VLLM_USE_FLASHINFER_SAMPLER": "0"})
weights = modal.Volume.from_name("amalia-weights", create_if_missing=True)
adapters = modal.Volume.from_name("amalia-lora", create_if_missing=True)
app = modal.App("ccp-leitor-a", image=image)


@app.function(gpu="L40S", volumes={"/weights": weights, "/lora": adapters}, timeout=3600)
def answer(prompts: list[dict], lora: str = "") -> list[dict]:
    from huggingface_hub import snapshot_download
    from vllm import LLM, SamplingParams
    from vllm.sampling_params import StructuredOutputsParams

    path = snapshot_download(MODEL, revision=REVISION, cache_dir="/weights")
    extra = {"enable_lora": True, "max_lora_rank": 64 if lora.endswith("r64") else 16} if lora else {}  # D53: the rank-64 adapter
    llm = LLM(model=path, max_model_len=WINDOW, enable_prefix_caching=True, gpu_memory_utilization=0.92, seed=0,
              structured_outputs_config={"backend": "xgrammar", "disable_any_whitespace": True}, **extra)
    request = None
    if lora:
        from vllm.lora.request import LoRARequest
        adapter = Path("/lora") / ADAPTERS[lora]
        if not adapter.exists():
            raise SystemExit(f"{adapter} missing in the volume amalia-lora")
        request = LoRARequest(ADAPTERS[lora], 1, str(adapter))
    tok = llm.get_tokenizer()
    keep, out = [], []
    for p in prompts:
        msgs = [{"role": "system", "content": SYSTEM}, {"role": "user", "content": p["prompt"]}]
        n = len(tok.encode(tok.apply_chat_template(msgs, add_generation_prompt=True, tokenize=False), add_special_tokens=False))
        if n + MAX_TOKENS > WINDOW:
            out.append({"key": p["key"], "skipped": "window", "prompt_tokens": n})
        else:
            keep.append((p, msgs, n))
    # compact JSON: the grammar allows no free whitespace (with it, the model looped on blanks until max_tokens: attempt 1)
    params = [SamplingParams(temperature=0.0, max_tokens=MAX_TOKENS, seed=0,
                             structured_outputs=StructuredOutputsParams(json=k[0]["schema"], disable_any_whitespace=True)) for k in keep]
    res = llm.chat([k[1] for k in keep], params, use_tqdm=False, lora_request=request)
    for (p, _, n), r in zip(keep, res):
        o = r.outputs[0]
        out.append({"key": p["key"], "prompt_tokens": n, "completion_tokens": len(o.token_ids), "finish_reason": o.finish_reason, "text": o.text})
    return out


def record(text, at):
    return {"at": at, "sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(), "answer": text}


@app.local_entrypoint()
def main(only: str = "", dir: str = "", lora: str = "", out_dir: str = "", jsonl: str = "", out: str = ""):
    leitor = LEITOR_OF[lora]
    if jsonl:
        rows = [json.loads(l) for l in Path(jsonl).read_text(encoding="utf-8").splitlines() if l.strip()]
        target = Path(out)
        done = {json.loads(l)["id"] for l in target.read_text(encoding="utf-8").splitlines() if l.strip()} if target.exists() else set()
        items = [{"key": r["id"], "prompt": r["prompt"], "schema": r["schema"]} for r in rows if r["id"] not in done]
        if not items:
            print("nothing to answer"); return
        result = answer.remote(items, lora)
        at = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        target.parent.mkdir(parents=True, exist_ok=True)
        with target.open("a", encoding="utf-8") as f:
            for r in result:
                if "text" not in r:
                    print(f"{r['key']}: skipped ({r['skipped']}, {r['prompt_tokens']} tokens)"); continue
                f.write(json.dumps({"id": r["key"], **record(r["text"], at), "finish_reason": r["finish_reason"]}, ensure_ascii=False, sort_keys=True) + "\n")
        print(f"{sum('text' in r for r in result)} answers -> {target} ({leitor})")
        return
    base = Path(dir).resolve() if dir else READINGS  # --dir governance/readings/casos for the B5 cases
    dest = Path(out_dir).resolve() if out_dir else base
    items = []
    for d in sorted(base.iterdir()):
        f = d / "prompt.json"
        if not f.exists() or (dest / d.name / f"{leitor}.json").exists() or (only and only not in d.name):
            continue
        body = json.loads(f.read_text(encoding="utf-8"))
        items.append({"key": d.name, "prompt": body["prompt"], "schema": body["schema"]})
    if not items:
        print("nothing to answer")
        return
    result = answer.remote(items, lora)
    at = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    for r in result:
        if "text" not in r:
            print(f"{r['key']}: skipped ({r['skipped']}, {r['prompt_tokens']} tokens)")
            continue
        (dest / r["key"]).mkdir(parents=True, exist_ok=True)
        (dest / r["key"] / f"{leitor}.json").write_text(json.dumps(record(r["text"], at), ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        print(f"{r['key']}: answered ({r['prompt_tokens']} prompt tokens, {r['completion_tokens']} out, {r['finish_reason']}) -> {leitor}")
