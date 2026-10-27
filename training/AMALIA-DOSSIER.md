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

- Run: 745 steps, 5 484 s on one H100, 12 232 examples (0 dropped), 50.9 M trainable parameters, USD 6.20
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

## v3 (adapter `amalia-ccp-lei-v3`, 2026-10-26) — teaching it to split time into periods
- Why: for the regime selector (which version of the law applies to a procedure by its start date) AMALIA answered
  one period «from 2026-10-01 to 2026-10-01» where the second reader gave two periods split on that day.
- New tasks (`training/data-v3/`, `tools/make_regimes.py`), labelled by code from the validity notes of the Diário da
  República: the date an act enters into force, read from its own article (24 train / 8 reserved: few acts print it);
  the partition of a passage's version history into periods (1 314 train / 301 reserved). Not taught on purpose: whether
  a procedure started on the day of entry into force falls before or after. Mix: v2's plus these (14 908 examples).
- Run: 921 steps, 6 714 s on one H100, USD 7.61 once Modal closed the hours (first reading 5.74; `training/runs/v3/`).
- Reserved results (`reports/measure/regimes-v3-2026-10-26.md`; BEFORE in `training/runs/v3/BEFORE.md`):

| reader | periods: exact | periods: well-formed partition | entry date | conditions task, exact |
|---|---|---|---|---|
| base | 0.0 % (0/301) | 0.0 % | 6/8 | 2.8 % |
| base + v2 | 0.0 % (0/301) | 0.0 % (every period left open) | 6/8 | 91.2 % |
| base + v3 | **99.0 % [97.1, 99.7]** (298/301) | **99.3 %** | **8/8** | 91.8 % |

- Rule test, round 5 (`governance/readings/ronda5/RONDA5.md`, round 4's prompt unchanged): the skill did not carry
  over to the selector question; v3 still answers one period «from 2026-10-01 to 2026-10-01». On the deadline rules it
  read no better than v2 (identical answer on one, extra conditions on another, conditions dropped on the one already
  settled, which a later round does not reopen). Settled after five rounds: 1 of these 4.

## v4 (adapter `amalia-ccp-lei-v4`, 2026-10-27) — reading the conditions a question states
- Why: on the deadline rules the reader added conditions a question did not state, or dropped ones it did (v3 left out
  81.8 % of the stated conditions on reserved questions; the base model added 41 % of its own).
- New task (`training/data-v4/condicoes_pergunta/`, `tools/make_question_conditions.py`), labelled by code: a question
  with 0 to 4 constraints (procedure, JOUE, contract type, region, contracting entity, base price) -> exactly the typed
  conditions it states, in canonical form. Every constraint has phrasings used only in training and phrasings used only
  in the 400 reserved questions (checked: no reserved phrasing occurs in a training question). The constraint sets of the
  three real deadline questions are excluded from both, so the rule test stays unseen. Mix: v3's plus 4 000 (19 511).
- Run: 1 198 steps, 8 416 s on one H100, USD 9.53 (`training/runs/v4/`).
- Reserved results (`reports/measure/pergunta-v4-2026-10-27.md`; BEFORE committed before training in
  `training/runs/v4/BEFORE.md`):

| reader | exact condition set (400) | conditions added | conditions missed |
|---|---|---|---|
| base | 29.2 % [25.0, 33.9] | 41.0 % | 23.5 % |
| base + v3 | 5.8 % [3.9, 8.5] | 55.1 % | 81.8 % |
| base + v4 | **100.0 % [99.1, 100.0]** (400/400) | **0.0 %** (0/989) | **0.0 %** (0/989) |

- Earlier skills kept (`reports/measure/condicoes-v4-2026-10-27.md`, `regimes-v4-2026-10-27.md`): conditions in a
  passage 93.2 % exact (v3 91.8 %), periods 301/301 (v3 298/301), entry date 8/8.
- Limit: the reserved questions are built from the same sentence pattern as the training ones with other words; 100 %
  says it learned that pattern, not yet that it reads any question. The test that counts is the three real questions in
  round 6.
- Rule test, round 6 (`governance/readings/ronda6/RONDA6.md`): the two minimum-deadline rules without JOUE settle (v4 and
  the other family identical: 6 days for goods and services, 14 for works); with the JOUE rule of round 4, all three
  deadline rules are settled. On the real questions v4 read the stated conditions exactly on 2 of 3 (it left out
  «concurso público» on the JOUE one). The selector is still not settled: v4 gives only the regime from 1 Oct 2026.

## Not for publication
The rule-test log names the reader of the other family; findings about specific vendors or municipalities stay out.
