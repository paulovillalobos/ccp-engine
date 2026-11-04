"""LoRA v1 of the reader (leitor:a2): AMALIA-9B-0626-DPO base + an adapter trained on training/data/*/train.jsonl, which
tools/make_training.py generates from law/ by code (no model answer inside). Runs on Modal, never on the Mac.

    <a Python 3.12 venv with modal>/bin/modal run training/train_lora.py --run v1

Mixture (proportional per task, capped): every train example of every task, except escolha_passagem, which is cut to at
most the sum of the other tasks (so it is never more than 50 % of the mix); the cut is deterministic (sha256 of the
example id). Format: chat, the reader's system prompt (readers/leitor_a_modal.py SYSTEM), the example's prompt as the
user turn, its answer (compact JSON) as the assistant turn; the loss is on the answer tokens only and the vocabulary
projection is applied only at those positions. Micro-batches of length-sorted examples (<= TOKENS_PER_BATCH tokens with
padding), gradient accumulation to EFFECTIVE_BATCH examples, AdamW, linear warm-up then linear decay, bf16, gradient
checkpointing, LoRA r=16 / alpha 32 / dropout 0.05 on every projection (q, k, v, o, gate, up, down).

Writes the adapter to the Modal volume amalia-lora as amalia-ccp-lei-v1 (never touches any other adapter there) and
training/runs/<run>/MANIFEST.json here: sha256 of training/data/INDEX.json, the mixture, the hyper-parameters, the repo
commit, start and end instants, the loss log, the adapter files' sha256 and the Modal app id (the cost in USD is read
from Modal's billing report afterwards: training/runs/<run>/COST.json, `modal billing report`).
"""
import hashlib
import json
import subprocess
import time
from pathlib import Path

import modal

MODEL = "amalia-llm/AMALIA-9B-0626-DPO"
REVISION = "c4614b9b5c7b4fe303fa20902e692fc7dface640"
SYSTEM = "Responde unicamente com o objeto JSON pedido, sem texto antes nem depois."  # = readers/leitor_a_modal.py SYSTEM
ADAPTER = "amalia-ccp-lei-v1"
# phase 5 (DECISIONS D46): v2 adds training/data-v2 (condicoes_texto, generated from law/ by code), counted twice in the mix
RUNS = {"v1": {"adapter": "amalia-ccp-lei-v1", "data": ["training/data"], "repeat": {}},
        "v2": {"adapter": "amalia-ccp-lei-v2", "data": ["training/data", "training/data-v2"], "repeat": {"condicoes_texto": 2}},
        # phase 6 (D47): v3 = v2's mix plus training/data-v3 (entrada_em_vigor, periodos_vigencia)
        "v3": {"adapter": "amalia-ccp-lei-v3", "data": ["training/data", "training/data-v2", "training/data-v3"], "repeat": {"condicoes_texto": 2}},
        # phase 7 (D49): v4 = v3's mix plus training/data-v4 (condicoes_pergunta)
        "v4": {"adapter": "amalia-ccp-lei-v4", "data": ["training/data", "training/data-v2", "training/data-v3", "training/data-v4"],
               "repeat": {"condicoes_texto": 2}},
        # phase 8 (D50): v5 = v4's mix plus training/data-v5 (factos_utilizador: a person's question -> facts)
        "v5": {"adapter": "amalia-ccp-lei-v5", "data": ["training/data", "training/data-v2", "training/data-v3", "training/data-v4", "training/data-v5"],
               "repeat": {"condicoes_texto": 2}},
        # phase 9 (D52): v6 = v4's mix (the law) plus training/data-v6 (written questions, their noisy copies, D50 templates relabelled)
        "v6": {"adapter": "amalia-ccp-lei-v6", "data": ["training/data", "training/data-v2", "training/data-v3", "training/data-v4", "training/data-v6"],
               "repeat": {"condicoes_texto": 2}},
        # phase 10 (D53): v7 = v4's mix plus training/data-v7 (1 000 written questions); the same mix at LoRA rank 16 and 64
        "v7": {"adapter": "amalia-ccp-lei-v7", "data": ["training/data", "training/data-v2", "training/data-v3", "training/data-v4", "training/data-v7"],
               "repeat": {"condicoes_texto": 2}},
        "v7r64": {"adapter": "amalia-ccp-lei-v7r64", "data": ["training/data", "training/data-v2", "training/data-v3", "training/data-v4", "training/data-v7"],
                  "repeat": {"condicoes_texto": 2}, "hp": {"lora_r": 64, "lora_alpha": 128}},
        # phase 11 (D54): v8 = v4's mix plus training/data-v8 (3 000 written questions in 20 styles: 2 200 trained), rank 16
        "v8": {"adapter": "amalia-ccp-lei-v8", "data": ["training/data", "training/data-v2", "training/data-v3", "training/data-v4", "training/data-v8"],
               "repeat": {"condicoes_texto": 2}},
        # phase 12 (D61): v9 = v4's mix plus training/data-v9 (3 600 written questions: v8's plus 600 on v8's dev errors; D61 errata), rank 16
        "v9": {"adapter": "amalia-ccp-lei-v9", "data": ["training/data", "training/data-v2", "training/data-v3", "training/data-v4", "training/data-v9"],
               "repeat": {"condicoes_texto": 2}},
        # phase 13 (D63): v10 = v9's mix plus training/data-v10 (reading typed rules out of written articles), rank 16
        "v10": {"adapter": "amalia-ccp-lei-v10", "data": ["training/data", "training/data-v2", "training/data-v3", "training/data-v4", "training/data-v9",
                                                           "training/data-v10"],
                "repeat": {"condicoes_texto": 2}},
        # phase 14 (D65): v11 = v10's mix plus training/data-v11 (targeted articles on v10's dev errors), rank 16
        "v11": {"adapter": "amalia-ccp-lei-v11", "data": ["training/data", "training/data-v2", "training/data-v3", "training/data-v4", "training/data-v9",
                                                           "training/data-v10", "training/data-v11"],
                "repeat": {"condicoes_texto": 2}},
        # phase 15 (D66): v12 = v11's mix with the rule-reading rows in the protocol v3 (training/data-v12 replaces regra_lida and
        # empties regra_lida_alvo), rank 16
        "v12": {"adapter": "amalia-ccp-lei-v12", "data": ["training/data", "training/data-v2", "training/data-v3", "training/data-v4", "training/data-v9",
                                                           "training/data-v10", "training/data-v11", "training/data-v12"],
                "repeat": {"condicoes_texto": 2}},
        # phase 16 (D67): v13 = v12's mix with data-v13's rule-reading rows (BRIEF-D67's articles added, every article under
        # titles, schema in the factory's order), rank 16; tools/preflight_data.py must pass on them before the run starts
        "v13": {"adapter": "amalia-ccp-lei-v13", "data": ["training/data", "training/data-v2", "training/data-v3", "training/data-v4", "training/data-v9",
                                                           "training/data-v10", "training/data-v11", "training/data-v12", "training/data-v13"],
                "repeat": {"condicoes_texto": 2}, "preflight": "training/data-v13/regra_lida/train.jsonl", "hp": {"max_len": 12288}},
        # phase 17 (D68): v14 starts from v13's adapter (init) and trains one epoch on data-v14's rule rows (the real readings both
        # families settled, their numbers moved by code, plus 800 of data-v13's) and a tenth of every other task, so v13's skills stay
        "v14": {"adapter": "amalia-ccp-lei-v14", "init": "amalia-ccp-lei-v13",
                "data": ["training/data", "training/data-v2", "training/data-v3", "training/data-v4", "training/data-v9", "training/data-v10",
                         "training/data-v11", "training/data-v12", "training/data-v14"],
                "repeat": {"condicoes_texto": 2}, "sample": {"*": 0.1, "regra_lida": 1.0}, "hp": {"max_len": 12288, "epochs": 1, "warmup_steps": 10}}}
HP = {"lora_r": 16, "lora_alpha": 32, "lora_dropout": 0.05, "target_modules": ["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"],
      "epochs": 2, "lr": 1e-4, "warmup_steps": 20, "effective_batch": 16, "tokens_per_batch": 24000, "max_len": 8192,
      "optimizer": "AdamW (weight_decay 0)", "schedule": "linear warm-up, linear decay to 0", "precision": "bf16", "grad_clip": 1.0, "seed": 0,
      "gpu": "H100"}
ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "training/data"

image = (modal.Image.from_registry("nvidia/cuda:12.9.1-devel-ubuntu22.04", add_python="3.12")
         .pip_install("vllm==0.30.0", "huggingface_hub[hf_transfer]", "peft==0.21.2")
         .env({"HF_HUB_ENABLE_HF_TRANSFER": "1", "VLLM_USE_FLASHINFER_SAMPLER": "0"}))
weights = modal.Volume.from_name("amalia-weights", create_if_missing=True)
adapters = modal.Volume.from_name("amalia-lora", create_if_missing=True)
app = modal.App("ccp-train-leitor-a2", image=image)


def mixture(run="v1"):
    by_task = {}
    for d in RUNS[run]["data"]:
        for f in sorted((ROOT / d).glob("*/train.jsonl")):
            rows = [json.loads(l) for l in f.read_text(encoding="utf-8").splitlines() if l.strip()]
            by_task[f.parent.name] = rows * RUNS[run]["repeat"].get(f.parent.name, 1)
    sample = RUNS[run].get("sample", {})
    for k in by_task:  # D68: a run from an earlier adapter keeps a share of each task, the first by sha256 of the id (and of its copy)
        share = sample.get(k, sample.get("*", 1.0))
        if share < 1.0:
            keyed = sorted(enumerate(by_task[k]), key=lambda x: hashlib.sha256(f"{x[1]['id']}#{x[0]}".encode()).hexdigest())
            by_task[k] = [r for _, r in keyed[:max(1, round(share * len(keyed)))]]
    others = sum(len(v) for k, v in by_task.items() if k != "escolha_passagem")
    esc = sorted(by_task.get("escolha_passagem", []), key=lambda r: hashlib.sha256(r["id"].encode()).hexdigest())
    by_task["escolha_passagem"] = esc[:others]
    mix = [{"id": r["id"], "task": r["task"], "prompt": r["prompt"], "answer": r["answer"]} for k in sorted(by_task) for r in by_task[k]]
    return mix, {k: len(v) for k, v in sorted(by_task.items())}


@app.function(gpu="H100", volumes={"/weights": weights, "/lora": adapters}, timeout=9 * 3600)  # D67: v13 ≈ 5.5 h (v12 4.2 h × 1.31); the adapter is saved only at the end
def train_remote(rows: list[dict], hp: dict, adapter: str = ADAPTER, init: str = "") -> dict:
    import math
    import random

    import torch
    from huggingface_hub import snapshot_download
    from peft import LoraConfig, PeftModel, get_peft_model
    from transformers import AutoModelForCausalLM, AutoTokenizer

    out_dir = Path("/lora") / adapter
    if out_dir.exists():
        raise SystemExit(f"{out_dir} exists: an adapter is never overwritten")
    path = snapshot_download(MODEL, revision=REVISION, cache_dir="/weights")
    tok = AutoTokenizer.from_pretrained(path)
    pad = tok.pad_token_id if tok.pad_token_id is not None else tok.eos_token_id
    examples, dropped = [], 0
    for r in rows:
        head = [{"role": "system", "content": SYSTEM}, {"role": "user", "content": r["prompt"]}]
        p_txt = tok.apply_chat_template(head, add_generation_prompt=True, tokenize=False)
        f_txt = tok.apply_chat_template(head + [{"role": "assistant", "content": r["answer"]}], tokenize=False)
        if not f_txt.startswith(p_txt):
            dropped += 1
            continue
        p_ids = tok(p_txt, add_special_tokens=False)["input_ids"]
        a_ids = tok(f_txt[len(p_txt):], add_special_tokens=False)["input_ids"]
        if len(p_ids) + len(a_ids) > hp["max_len"]:
            dropped += 1
            continue
        examples.append((p_ids + a_ids, len(p_ids)))
    if len(examples) < 0.95 * len(rows):
        raise SystemExit(f"{len(rows) - len(examples)} of {len(rows)} examples dropped")
    total_tokens = sum(len(e[0]) for e in examples)

    def batches(seed):
        r = random.Random(seed)
        order = sorted(range(len(examples)), key=lambda i: (len(examples[i][0]), r.random()))
        out, cur, cur_max = [], [], 0
        for i in order:
            n = len(examples[i][0])
            if cur and max(cur_max, n) * (len(cur) + 1) > hp["tokens_per_batch"]:
                out.append(cur); cur, cur_max = [], 0
            cur.append(i); cur_max = max(cur_max, n)
        if cur:
            out.append(cur)
        r.shuffle(out)
        return out

    model = AutoModelForCausalLM.from_pretrained(path, torch_dtype=torch.bfloat16, attn_implementation="sdpa").cuda()
    model.config.use_cache = False
    model.gradient_checkpointing_enable(gradient_checkpointing_kwargs={"use_reentrant": False})
    model.enable_input_require_grads()
    if init:  # D68: training goes on from an earlier adapter in the volume (its rank and modules), which stays as it is
        model = PeftModel.from_pretrained(model, str(Path("/lora") / init), is_trainable=True)
    else:
        model = get_peft_model(model, LoraConfig(r=hp["lora_r"], lora_alpha=hp["lora_alpha"], lora_dropout=hp["lora_dropout"],
                                                 task_type="CAUSAL_LM", target_modules=hp["target_modules"]))
    trainable = sum(p.numel() for p in model.parameters() if p.requires_grad)
    inner = model.base_model.model
    torch.manual_seed(hp["seed"])
    epochs = [batches(hp["seed"] + e) for e in range(hp["epochs"])]
    steps = math.ceil(sum(len(b) for ep in epochs for b in ep) / hp["effective_batch"])
    opt = torch.optim.AdamW([p for p in model.parameters() if p.requires_grad], lr=hp["lr"], weight_decay=0.0)
    sched = torch.optim.lr_scheduler.LambdaLR(opt, lambda s: min(1.0, (s + 1) / hp["warmup_steps"]) * max(0.0, 1 - s / steps))
    model.train()
    log, t0, seen, run_loss, run_n, step = [], time.time(), 0, 0.0, 0, 0
    for ep, ep_batches in enumerate(epochs):
        for b in ep_batches:
            L = max(len(examples[i][0]) for i in b)
            ids = torch.full((len(b), L), pad, dtype=torch.long)
            att = torch.zeros((len(b), L), dtype=torch.long)
            sel = torch.zeros((len(b), L), dtype=torch.bool)  # positions whose next token is an answer token
            for row, i in enumerate(b):
                seq, plen = examples[i]
                ids[row, :len(seq)] = torch.tensor(seq)
                att[row, :len(seq)] = 1
                sel[row, plen - 1:len(seq) - 1] = True
            ids, att, sel = ids.cuda(), att.cuda(), sel.cuda()
            hidden = inner.model(input_ids=ids, attention_mask=att).last_hidden_state
            logits = inner.lm_head(hidden[sel]).float()
            targets = ids[:, 1:][sel[:, :-1]]
            loss = torch.nn.functional.cross_entropy(logits, targets)
            (loss * len(b) / hp["effective_batch"]).backward()
            run_loss += loss.item() * len(b); run_n += len(b); seen += len(b)
            if run_n >= hp["effective_batch"]:
                torch.nn.utils.clip_grad_norm_(model.parameters(), hp["grad_clip"])
                opt.step(); sched.step(); opt.zero_grad(set_to_none=True); step += 1
                if step % 10 == 0 or step == 1:
                    log.append({"step": step, "epoch": ep + 1, "loss": round(run_loss / run_n, 4), "seen": seen, "seconds": round(time.time() - t0, 1)})
                    print(log[-1], flush=True)
                run_loss, run_n = 0.0, 0
    if run_n:
        torch.nn.utils.clip_grad_norm_(model.parameters(), hp["grad_clip"])
        opt.step(); opt.zero_grad(set_to_none=True); step += 1
    model.save_pretrained(str(out_dir))
    files = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(out_dir.iterdir()) if p.is_file()}
    adapters.commit()
    return {"examples": len(examples), "dropped": dropped, "tokens": total_tokens, "trainable_params": trainable, "steps": step,
            "seconds": round(time.time() - t0, 1), "log": log, "adapter_files": files}


@app.local_entrypoint()
def main(run: str = "v1"):
    out = ROOT / "training/runs" / run
    if (out / "MANIFEST.json").exists():
        raise SystemExit(f"{out}/MANIFEST.json exists: a run is never redone in place")
    if RUNS[run].get("preflight"):  # D67: the training rows against the measured articles, before anything is spent
        gate = subprocess.run([str(ROOT / ".venv/bin/python"), str(ROOT / "tools/preflight_data.py"), "--train", str(ROOT / RUNS[run]["preflight"])], cwd=ROOT)
        if gate.returncode:
            raise SystemExit("tools/preflight_data.py failed: no run")
    rows, mix = mixture(run)
    adapter = RUNS[run]["adapter"]
    index = DATA / "INDEX.json"
    indexes = {d: hashlib.sha256((ROOT / d / "INDEX.json").read_bytes()).hexdigest() for d in RUNS[run]["data"]}
    commit = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, capture_output=True, text=True).stdout.strip()
    dirty = bool(subprocess.run(["git", "status", "--porcelain", *RUNS[run]["data"], "law"], cwd=ROOT, capture_output=True, text=True).stdout.strip())
    started = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    hp = {**HP, **RUNS[run].get("hp", {})}  # a run may change hyper-parameters (D53: rank 64)
    call = train_remote.spawn(rows, hp, adapter, RUNS[run].get("init", ""))
    print("modal function call", call.object_id, flush=True)
    res = call.get()
    finished = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    out.mkdir(parents=True, exist_ok=True)
    manifest = {"adapter": adapter, "volume": "amalia-lora", "base": {"model": MODEL, "revision": REVISION}, "init": RUNS[run].get("init"),
                "training_index_sha256": hashlib.sha256(index.read_bytes()).hexdigest(), "data_index_sha256": indexes,
                "repeat": RUNS[run]["repeat"], "mixture": mix, "examples_in_mix": len(rows),
                "hyperparameters": hp, "repo_commit": commit, "repo_dirty_training_or_law": dirty, "started": started, "finished": finished,
                "modal_app": app.app_id, "modal_function_call": call.object_id, "result": res, "cost_usd": "see COST.json (modal billing report)"}
    (out / "MANIFEST.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(json.dumps({k: v for k, v in manifest.items() if k != "result"}, indent=1))
    print({k: v for k, v in res.items() if k != "log"})
