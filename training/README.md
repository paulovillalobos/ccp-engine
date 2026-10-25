# training/ — the reader's adapter, trained on data generated from law/

Nothing here is imported by `engine/`, `tools/` or `verify.py`. The model runs on Modal, never on the Mac.

| Path | What | Made by |
|---|---|---|
| `data/<task>/{train,held_out}.jsonl` | examples `{id, task, prompt, answer, sources, schema}` | `tools/make_training.py generate` (no model, no network; verify TRAIN re-derives it) |
| `data/ARTICLE-OF.json`, `data/INDEX.json` | passage → article map; sha256 and line count per file, counts per task and split | same |
| `data/REPORT.md` | examples per task and split, passages covered, mean token length (AMALIA's tokenizer.json) | `tools/make_training.py report --tokenizer …` |
| `train_lora.py` | LoRA training on Modal (H100) | run by hand: `<venv with modal>/bin/modal run training/train_lora.py --run v1` |
| `runs/<run>/MANIFEST.json` | sha256 of `data/INDEX.json`, mixture, hyper-parameters, repo commit, instants, loss log, adapter files' sha256, Modal app id | `train_lora.py` |
| `runs/<run>/COST.json` | the run's cost in USD as Modal's billing report gives it | `modal billing report` (raw output kept) |

Rules (phase 4 brief): the data contain no answer of any model; the reservation `law/TRAIN-HELD-OUT.json` and
`data/INDEX.json` are sealed in the governance log (tools/measure.py seal, D40); no train example touches a reserved
article; the adapter `amalia-ccp-lei-v1` lives in the Modal volume `amalia-lora` beside, and never mixed with, any other
adapter there (the earlier `amalia-rjue-v6` was trained on another model's answers and is not used). The trained model is
the principal `leitor:a2` (family A); `leitor:a` stays the base model.
