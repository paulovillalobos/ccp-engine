"""leitor:c on Modal: the family-C reader (Mistral, D79) answers the rules factory's prompts blind, with guided JSON (vLLM,
temperature 0, one batch). It replaces leitor:b (Reader B) as the blind checker of family A (AMALIA).

    <a Python 3.12 venv with modal>/bin/modal run readers/leitor_c_modal.py --dir governance/readings/fabrica12 [--only SLUG]
        [--limit N] [--out-dir DIR]

readers/ holds the code that runs a model (DECISIONS D38): nothing in engine/, tools/ or verify.py imports it.

Directory mode only: reads <dir>/<key>/prompt.json, skips a key that already has leitor-c.json, sends the prompts and their
answer schemas to one GPU container, and writes each answer as <out-dir or dir>/<key>/leitor-c.json {"at", "sha256" of the
answer text, "answer"}: the same record leitor:b wrote. The decoder keeps the answer to the schema's JSON shape only, as
leitor:b's was; with --quotes text, the quote grammar family A reads with: the checker (read_rules_v3.check) decides which answers can be recorded.
The weights (Apache-2.0, pinned revisions, MODELS) are mistralai/Mistral-Small-4-119B-2603 on two H100 (--model small4, the
default; leitor-c.json) or mistralai/Ministral-3-14B-Instruct-2512 on one L40S (--model 14b; leitor-c14.json), in the Modal volume
mistral-weights (its own volume: the AMALIA volumes are only read by leitor_a_modal.py and are never mounted here).
A prompt longer than the window is skipped and listed, never truncated.
"""
import hashlib
import json
import time
from pathlib import Path

import modal

MODELS = {  # --model: the motor (repo, revision, files) and the answer file it writes
    "small4": ("mistralai/Mistral-Small-4-119B-2603", "a11f36bebf709121056b1dbcc943d1c6afbe494d", ["params.json", "consolidated-*.safetensors",
               "consolidated.safetensors.index.json", "tekken.json"], "leitor-c"),  # 119B, FP8 (~120 GB): two H100, tensor parallel
    "14b": ("mistralai/Ministral-3-14B-Instruct-2512", "29439f81c2be264d8d393273f99e7db9c0961120",
            ["params.json", "consolidated.safetensors", "tekken.json"], "leitor-c14"),  # D79 first test: «não tipável» on all 28 rule targets
}
WINDOW, MAX_TOKENS = 32768, 3000
SYSTEM = "Responde unicamente com o objeto JSON pedido, sem texto antes nem depois."
READINGS = Path(__file__).resolve().parent.parent / "governance/readings"

image = modal.Image.from_registry("nvidia/cuda:12.9.1-devel-ubuntu22.04", add_python="3.12").pip_install(
    "vllm==0.30.0", "transformers==5.16.1", "huggingface_hub[hf_transfer]")  # 5.15–5.16 only: vLLM 0.30 needs >=5.15 for Mistral and imports PixtralRotaryEmbedding, gone from 5.17
image = image.env({"HF_HUB_ENABLE_HF_TRANSFER": "1", "VLLM_USE_FLASHINFER_SAMPLER": "0"})
weights = modal.Volume.from_name("mistral-weights", create_if_missing=True)
app = modal.App("ccp-leitor-c", image=image)


@app.function(gpu="L40S", volumes={"/weights": weights}, timeout=3600)
def answer_14b(prompts: list[dict]) -> list[dict]:
    return run("14b", prompts)


@app.function(gpu="H100:2", volumes={"/weights": weights}, timeout=2 * 3600)  # D79: a B200 was not given in 40 min
def answer_small4(prompts: list[dict]) -> list[dict]:
    return run("small4", prompts)


def run(name, prompts):
    from huggingface_hub import snapshot_download
    from vllm import LLM, SamplingParams
    from vllm.sampling_params import StructuredOutputsParams

    model, revision, files, _ = MODELS[name]
    path = snapshot_download(model, revision=revision, cache_dir="/weights", allow_patterns=files)
    weights.commit()
    # Mistral's own format (params.json, consolidated.safetensors, tekken.json): vLLM 0.30's Hugging Face path for Mistral3
    # needs one transformers release for the tokenizer and an earlier one for the vision encoder it imports
    llm = LLM(model=path, tensor_parallel_size=2 if name == "small4" else 1, tokenizer_mode="mistral", config_format="mistral", load_format="mistral", max_model_len=WINDOW,
              enable_prefix_caching=True, gpu_memory_utilization=0.92, seed=0, limit_mm_per_prompt={"image": 0},
              structured_outputs_config={"backend": "xgrammar", "disable_any_whitespace": True})
    tok = llm.get_tokenizer()
    keep, out = [], []
    for p in prompts:
        msgs = [{"role": "system", "content": SYSTEM}, {"role": "user", "content": p["prompt"]}]
        n = len(tok.encode(SYSTEM + "\n" + p["prompt"])) + 16  # the chat markers: a few tokens
        if n + MAX_TOKENS > WINDOW:
            out.append({"key": p["key"], "skipped": "window", "prompt_tokens": n})
        else:
            keep.append((p, msgs, n))
    params = [SamplingParams(temperature=0.0, max_tokens=MAX_TOKENS, seed=0,
                             structured_outputs=StructuredOutputsParams(grammar=k[0]["grammar"]) if k[0].get("grammar") else
                             StructuredOutputsParams(json=k[0]["schema"], disable_any_whitespace=True)) for k in keep]
    res = llm.chat([k[1] for k in keep], params, use_tqdm=False)
    for (p, _, n), r in zip(keep, res):
        o = r.outputs[0]
        out.append({"key": p["key"], "prompt_tokens": n, "completion_tokens": len(o.token_ids), "finish_reason": o.finish_reason, "text": o.text})
    return out


def with_grammars(items, contexts):
    """--quotes text: each item's quote grammar (readers/quote_grammar.py, built here, never in the GPU container), the same
    as family A's: the quotes can only be pieces of the passages the checker lets that slot cite."""
    import sys
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from leitor_a_modal import in_answer_order
    from quote_grammar import grammar
    for i in items:
        i["grammar"] = grammar(in_answer_order(i["schema"]), contexts[i["key"]])
    return items


@app.local_entrypoint()
def main(dir: str = "", only: str = "", limit: int = 0, out_dir: str = "", quotes: str = "", model: str = "small4"):
    LEITOR = MODELS[model][3]
    base = Path(dir).resolve() if dir else READINGS
    dest = Path(out_dir).resolve() if out_dir else base
    if quotes not in ("", "text"):
        raise SystemExit(f"--quotes {quotes}: only «text»")
    items, found = [], {}
    for d in sorted(base.iterdir()):
        f = d / "prompt.json"
        if not f.exists() or (dest / d.name / f"{LEITOR}.json").exists() or (only and only not in d.name):
            continue
        body = json.loads(f.read_text(encoding="utf-8"))
        items.append({"key": d.name, "prompt": body["prompt"], "schema": body["schema"]})
        found[d.name] = body.get("context")
    if limit:
        items = items[:limit]
    if quotes:
        with_grammars(items, found)
    if not items:
        print("nothing to answer")
        return
    result = (answer_small4 if model == "small4" else answer_14b).remote(items)
    at = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    for r in result:
        if "text" not in r:
            print(f"{r['key']}: skipped ({r['skipped']}, {r['prompt_tokens']} tokens)")
            continue
        (dest / r["key"]).mkdir(parents=True, exist_ok=True)
        text = r["text"]
        (dest / r["key"] / f"{LEITOR}.json").write_text(json.dumps({"at": at, "sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(), "answer": text,
                                                                    **({"quotes": quotes} if quotes else {})},
                                                                   ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        print(f"{r['key']}: answered ({r['prompt_tokens']} prompt tokens, {r['completion_tokens']} out, {r['finish_reason']}) -> {LEITOR}")
