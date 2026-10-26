# AMALIA as a reader of Portuguese procurement law — what was fine-tuned, on what, and what it did

A record for the AMALIA team (amalia-llm). Every number here is recomputed by code from stored files in this
repository; nothing below is an estimate. Kept up to date at each run: BEFORE is written before training starts,
AFTER when its measurement exists.

## Base model
- `amalia-llm/AMALIA-9B-0626-DPO`, revision `c4614b9b5c7b4fe303fa20902e692fc7dface640`, bf16.
- Inference: vLLM 0.30.0 on Modal (L40S), temperature 0, guided JSON (the answer schema), 32 768-token window.
- Training: LoRA on Modal (H100), r 16, alpha 32, dropout 0.05, all projections (q, k, v, o, gate, up, down), 2 epochs,
  lr 1e-4, effective batch 16, bf16; loss on the answer tokens only. Script: `training/train_lora.py`.

## What the training data is (and is not)
- Generated **by code from the text of the law** held in `law/` (the CCP and related acts as published in the Diário da
  República, with their validity notes). No answer written by any other model is in it.
- About 20 % of the law's articles, plus every article used in the rule tests, are **reserved**: never in training, used
  only to measure (`law/TRAIN-HELD-OUT.json`, frozen 2026-10-25). A passage whose text equals a reserved one (the CCP
  republished inside an amending act) is reserved too.

## v1 (adapter `amalia-ccp-lei-v1`, 2026-10-25)
- Data: `training/data/` — 8 900 examples in the mix: choose the passage a statement refers to (4 450), say which
  version of a passage was in force on a date (3 942), read a Diário da República validity note (506), resolve a
  cross-reference (2).
- Run: 540 steps, 4 111 s on one H100, 50.9 M trainable parameters, USD 4.67 (`training/runs/v1/`).
- Reserved results, base → v1: choose the passage 94.6 % → 98.7 %; version in force 41.4 % → 99.5 %; read a validity note
  61.7 % → 98.3 % (`reports/measure/amalia-v1-2026-10-25.md`).

## v2 (adapter `amalia-ccp-lei-v2`, 2026-10-26) — teaching it not to add what the text does not say
- Why: in the rule tests (three rounds, `governance/readings/ronda2..4`) AMALIA got the numbers right (days, euro
  thresholds) but added conditions the law does not state and missed some it does, so it never agreed with the second
  reader.
- New task `condicoes_texto` (`training/data-v2/`, `tools/make_conditions.py`): one passage of a procurement act and the
  question «which procedure types, contract types and regions does this text name, and does it name the EU Official
  Journal»; the answer is decided by a declared word list, checked by code. 833 train, 353 reserved. Mix: v1's data plus
  this task counted twice (12 232 examples).
- BEFORE (353 reserved passages, `training/runs/v2/BEFORE.md`):

| reader | all fields exact | values named that the text does not name |
|---|---|---|
| base | 2.8 % (10/353) | 81.1 % (1 524 of 1 880) |
| base + v1 | 0.0 % (0/353) | 78.6 % (1 146 of 1 458) |

- Run: 745 steps, 5 484 s on one H100, 12 232 examples (0 dropped), 50.9 M trainable parameters, USD 5.12
  (`training/runs/v2/`).
- AFTER (the same 353 reserved passages, `reports/measure/condicoes-v2-2026-10-26.md`):

| reader | all fields exact | values named that the text does not name | values the text names that it missed |
|---|---|---|---|
| base | 2.8 % [1.6, 5.1] | 81.1 % (1 524 of 1 880) | 12.5 % (51 of 407) |
| base + v1 | 0.0 % [0.0, 1.1] | 78.6 % (1 146 of 1 458) | 23.3 % (95 of 407) |
| base + v2 | **91.2 % [87.8, 93.7]** (322/353) | **8.9 %** (39 of 436) | **2.5 %** (10 of 407) |

- Rule test, round 4 (`governance/readings/ronda4/RONDA4.md`): the same prompt and schema as round 3; v2 proposes, a
  reader of another family reviews blind. The minimum deadline of a public tender announced in the EU Official Journal
  (CCP art. 136.º n.º 1: 30 days from the sending of the notice, conditions «announced in the OJEU» and «concurso
  público») was read identically by both and is the first of these four rules to settle. The two other deadline rules
  now agree on the article, the days and where they count from, and still differ on conditions; the regime selector
  differs in substance.

## Not for publication
The rule-test log names the reader of the other family; findings about specific vendors or municipalities stay out.
