"""leitor:a on Modal: the family-A reader answers the B3 prompts with guided JSON (vLLM, temperature 0, one batch).

    <a Python 3.12 venv with modal>/bin/modal run readers/leitor_a_modal.py [--only SLUG] [--dir governance/readings/casos]

readers/ holds the code that runs a model (DECISIONS D38): nothing in engine/, tools/ or verify.py imports it, and
verify's code guard keeps it that way.

Reads governance/readings/<rule>/prompt.json (written by tools/read_rules.py prompts), skips a rule that already has
leitor-a.json, sends the prompts and their answer schemas to one GPU container, and writes each answer as
governance/readings/<rule>/leitor-a.json {"at", "sha256" of the answer text, "answer"}: the same record leitor:b gets.
A prompt longer than the window is skipped and listed, never truncated. The grammar admits no free whitespace, set on
the engine (attempt 1, free whitespace: 8 of 18 answers looped on blanks until max_tokens; attempt 2, the flag per
request only: 7 of 18, the flag was not honoured; both kept as leitor-a.attempt1.json / attempt2.json). The model and revision are the principal's
motor (governance/principals.json, leitor:a); nothing here decides: tools/read_rules.py record turns answers into log
events. Self-contained on purpose (the Modal client venv does not carry the engine's dependencies).
"""
import hashlib
import json
import time
from pathlib import Path

import modal

MODEL = "amalia-llm/AMALIA-9B-0626-DPO"
REVISION = "c4614b9b5c7b4fe303fa20902e692fc7dface640"  # leitor:a motor versao c4614b9b5c7b
WINDOW, MAX_TOKENS = 32768, 1500
SYSTEM = "Responde unicamente com o objeto JSON pedido, sem texto antes nem depois."
READINGS = Path(__file__).resolve().parent.parent / "governance/readings"

image = modal.Image.from_registry("nvidia/cuda:12.9.1-devel-ubuntu22.04", add_python="3.12").pip_install(
    "vllm==0.30.0", "huggingface_hub[hf_transfer]")
image = image.env({"HF_HUB_ENABLE_HF_TRANSFER": "1", "VLLM_USE_FLASHINFER_SAMPLER": "0"})
weights = modal.Volume.from_name("amalia-weights", create_if_missing=True)
app = modal.App("ccp-leitor-a", image=image)


@app.function(gpu="L40S", volumes={"/weights": weights}, timeout=3600)
def answer(prompts: list[dict]) -> list[dict]:
    from huggingface_hub import snapshot_download
    from vllm import LLM, SamplingParams
    from vllm.sampling_params import StructuredOutputsParams

    path = snapshot_download(MODEL, revision=REVISION, cache_dir="/weights")
    llm = LLM(model=path, max_model_len=WINDOW, enable_prefix_caching=True, gpu_memory_utilization=0.92, seed=0,
              structured_outputs_config={"backend": "xgrammar", "disable_any_whitespace": True})
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
    res = llm.chat([k[1] for k in keep], params, use_tqdm=False)
    for (p, _, n), r in zip(keep, res):
        o = r.outputs[0]
        out.append({"key": p["key"], "prompt_tokens": n, "completion_tokens": len(o.token_ids), "finish_reason": o.finish_reason, "text": o.text})
    return out


@app.local_entrypoint()
def main(only: str = "", dir: str = ""):
    base = Path(dir).resolve() if dir else READINGS  # --dir governance/readings/casos for the B5 cases
    items = []
    for d in sorted(base.iterdir()):
        f = d / "prompt.json"
        if not f.exists() or (d / "leitor-a.json").exists() or (only and only not in d.name):
            continue
        body = json.loads(f.read_text(encoding="utf-8"))
        items.append({"key": d.name, "prompt": body["prompt"], "schema": body["schema"]})
    if not items:
        print("nothing to answer")
        return
    result = answer.remote(items)
    at = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    for r in result:
        if "text" not in r:
            print(f"{r['key']}: skipped ({r['skipped']}, {r['prompt_tokens']} tokens)")
            continue
        rec = {"at": at, "sha256": hashlib.sha256(r["text"].encode("utf-8")).hexdigest(), "answer": r["text"]}
        (base / r["key"] / "leitor-a.json").write_text(json.dumps(rec, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        print(f"{r['key']}: answered ({r['prompt_tokens']} prompt tokens, {r['completion_tokens']} out, {r['finish_reason']})")
