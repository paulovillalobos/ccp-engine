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
- From v6, also **500 user questions written one by one** for this project (not collected from people), labelled by
  documented rules (`training/written-questions/LABELS.md`), with noisy copies made by code. They teach how a person's
  question maps to the engine's facts; they carry no reading of the law.
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

## v6 (adapter `amalia-ccp-lei-v6`, 2026-10-28) — reading questions as people write them
- Why: on questions written as people write (typos, missing accents, old spelling, shorthand, dictation, loose amounts,
  wrong citations, vague wording) v4 got the facts exactly right on about one question in five and invented a third of
  the facts it gave.
- Data (`training/written-questions/`, `tools/make_written.py`): 500 questions written one by one, not from a template,
  labelled by `LABELS.md`. The answer gives the facts, the fields stated ambiguously (with candidates), contradictions,
  and every article or act the question cites. 300 for training, each clean and in 5 noisy copies made by code; 100 dev;
  100 sealed final. Plus 2 000 of v5's template questions relabelled and noised. Mix: v4's (the law) plus these (22 787).
- Run: 1 353 steps, 9 192 s on one H100, USD 9.83 (`training/runs/v6/`).
- Results (`reports/measure/escritas-v6-2026-10-28.md`), sealed final 100:

| reader | facts exact | facts invented | facts missed | ambiguous fields found | default fills |
|---|---|---|---|---|---|
| base | 14 % | 49 % | 54 % | 65 % (flags 65 % without cause) | 21 |
| base + v4 | 19 % | 34 % | 58 % | 11 % | 11 |
| base + v6 | **64 % [54, 73]** | **7.9 %** | **11.9 %** | 50 % (flags 46 % without cause) | **0** |

## v7 (adapter `amalia-ccp-lei-v7`, 2026-10-28) — 1 000 written questions, a code guard, rank 16 vs 64
- Data (`tools/make_written_v7.py`): the 500 questions of v6 plus 500 more aimed at v6's errors; 600 trained (each clean and
  in 5 noisy copies), 200 dev, 200 sealed final; plus 16 real questions put by câmaras and juntas to CCDR Alentejo
  (2006-2025), evaluation only. The same mix trained at LoRA rank 16 and rank 64.
- Code between the reader and the engine (`tools/fact_guard.py`): places from the official list of municipalities and
  parishes, «preço base» wording, citations and start dates checked against the question's own text; it never adds a fact.
- Runs: 1 394 steps each, 9 464 s (rank 16) and 10 536 s (rank 64) on one H100, about USD 10 each.
- Results (`reports/measure/escritas-v7-2026-10-28.md`), facts exact with the guard:

| reader | sealed 200 | dev 200 | real 16 | facts invented (sealed) |
|---|---|---|---|---|
| base + v6 | 71.0 % | 67.5 % | 10 | 6.4 % |
| base + v7, rank 16 | **85.0 %** | **80.0 %** | 13 | **2.3 %** |
| base + v7, rank 64 | 83.0 % | 79.5 % | **14** | 3.3 % |
| another family's frontier model, same guard | 83.5 % | 83.0 % | 9 | 4.1 % |

  Rank 64 brings no clear gain over rank 16 at this data size; the next run stays at rank 16.

## v8 (adapter `amalia-ccp-lei-v8`, 2026-10-28) — 3 000 written questions in 20 styles
- Data (`tools/make_written_v8.py`): v7's 1 000 written questions plus 2 000 more in 20 writing styles (`STYLES.md`: from a
  parish clerk's dictated note to a lawyer's letter), written one by one for this project (not collected from people); v7's
  split kept, the new ones 1 600 train / 200 dev / 200 sealed final, so dev and sealed are 400 each. Mix: v4's plus these
  (31 670 examples). Rank 16.
- Run: 1 754 steps, 11 375 s on one H100, USD 12.52 (`training/runs/v8/`).
- Results (`reports/measure/escritas-v8-2026-10-28.md`), facts exact with the guard:

| reader | sealed 400 | dev 400 | real 16 | facts invented (sealed) |
|---|---|---|---|---|
| base + v7, rank 16 | 76.8 % | 71.2 % | 13 | 5.6 % |
| base + v8 | **88.2 % [84.7, 91.0]** | **84.8 %** | 13 | **2.6 %** |
| another family's frontier model, same guard | 75.5 % | 77.2 % | 9 | 7.7 % |

  v7 scored 85.0 % on v7's sealed 200; on these 400, half in styles it never saw, it drops to 76.8 %. v8 holds 88.2 %.
  On the 16 real questions v8 and v7 both have 13 facts-exact; v8 invents fewer facts (1 of 35 vs 2 of 36) and gives no
  marker without cause (0 of 9).

## v9 (adapter `amalia-ccp-lei-v9`, 2026-10-28) — v8's dev errors fixed in the labels and the data
- Data (`tools/make_written_v9.py`, D61): v8's written questions with two new label rules (the procedure asked about is a
  fact; one candidate goes to the ambiguous list only for three named cases) and 204 errata, plus 600 new questions on v8's
  five dev error kinds; 100 of them held out as a targeted set (alvo), never trained. Dev 400 and sealed 400 are v8's
  questions with corrected gold. Mix 34 152 examples. Rank 16.
- Run: training ended 05:34Z on one H100, USD 11.19 for the hours billed so far (`training/runs/v9/`).
- Results (`reports/measure/escritas-v9-2026-10-28.md`), facts exact with the guard, corrected gold:

| reader | sealed 400 | dev 400 | alvo 100 | real 16 | answer exact (sealed) | facts invented (sealed) |
|---|---|---|---|---|---|---|
| base + v8 | 87.5 % | 83.5 % | 85 % | 13 | 70.0 % | 2.1 % |
| base + v9 | 87.5 % [83.9, 90.4] | **87.0 %** | **92 %** | 13 | **75.2 %** | **1.1 %** |
| another family's frontier model, same guard | 74.5 % | 75.5 % | 72 % | 9 | 63.2 % | 7.2 % |

  On facts alone v9 ties v8 on the sealed set; the gain is in the whole answer (markers included: found 74 % to 86 %) and
  in fewer invented facts. On the targeted set the procedure-as-topic questions go from 11 of 19 to 17 of 19. The cost: more
  markers without cause (sealed 4 % to 12 %), mostly tipo_contrato and tipo_procedimento flagged ambiguous when the
  question settles them. Without the guard v9 scores 96 % on alvo; the guard takes 4 of those away.

## v10 (adapter `amalia-ccp-lei-v10`, 2026-10-28) — reading a typed rule out of a law passage
- Data (`tools/make_rule_readings.py`, D63): v9's mix plus a new task, regra_lida. It is built from 600 articles written for
  this project in the CCP's style, with invented numbers, and gold rule readings written from the text (never from the
  other family's readings). Every example is checked by code, and near-copies of real target passages are dropped (18).
  The task has 1 000 train rows (each article twice, with different offered field lists) and 82 held-out articles, never
  trained on. Mix 35 152 examples. Rank 16.
- Run: training ended 14:11Z on one H100, USD 13.17 for the hours billed so far (`training/runs/v10/`).
- Results (`reports/measure/regras-v10-2026-10-28.md`), 82 held-out articles, compared with the gold rule by rule in
  canonical form:

| reader | rules exact | content exact (passages aside) | right number of rules | right days or limits |
|---|---|---|---|---|
| base + v9 | 2.4 % | 2.4 % | 73.2 % | 72.0 % |
| base + v10 | **69.5 %** [58.9, 78.4] | **76.8 %** | **98.8 %** | **97.6 %** |
| another family's frontier model | 85.4 % | 98.8 % | 100 % | 100 % |

  v10 learned the task's shape (number of rules, days, limits). It still differs from the gold on conditions in about a
  quarter of the articles. On the real law (rules round 4, 18 open targets) it replicated the other family exactly on 4,
  and the days or limits agreed on 17 of 18.

## v11 (adapter `amalia-ccp-lei-v11`, 2026-10-28) — trained on the kinds of error v10 made
- Data (`tools/make_rule_readings_v11.py`, D65): a new measurement pool of 400 written articles, 13 near-twins dropped by
  code, split by id into dev 203 (studied) and sealed 184 (committed before any reader answered it). v10's errors on dev
  were sorted by code into kinds (a fact from a neighbouring number, the «restantes casos» complement, exception lists,
  reductions that carry the referred number's conditions, a comparator per case, a procedure only when stated, the
  target among several deadlines, modalidade). 400 targeted training articles were written on those kinds, checked so none
  is close to a measured one: task regra_lida_alvo, 800 train rows. v11 = v10's mix plus those rows, from the base.
- Run: training ended 20:11Z on one H100, USD 13.85 for the hours billed so far (`training/runs/v11/`).
- Results (`reports/measure/regras-v11-2026-10-28.md`), «replicates» = the same rules with passages aside, every rule
  citing the target passage (D64):

| set | base + v10 | base + v11 | another family's frontier model |
|---|---|---|---|
| sealed, 184 (never studied) | 91.3 % | **96.7 %** [93.1, 98.5] | 98.9 % |
| dev, 203 (studied for errors) | 87.7 % | 97.5 % | 98.0 % |
| data-v10's held out, 82 | 76.8 % | **89.0 %** [80.4, 94.1] | 98.8 % |

  Rules exact (passages included) on sealed: v11 93.5 %, v10 87.0 %, the frontier model 81.0 %. v11 got the days or limits
  right on every sealed article.
- On the real law (rules round 5, the 12 targets left open after round 4), v11 replicated the other family on 1
  (88.º n.º 2 a)). Days and limits agree on all 12; the readings differ in conditions or the comparator. Written
  articles are now close to solved; the real passages that are left are the hardest ones, and the gain does not carry
  over to them in full.

## v12 (adapter `amalia-ccp-lei-v12`, 2026-11-03) — reading with the protocol v3, every word quoted
- Data (`tools/make_rule_readings_v12.py`, D66): the rule readings in the reading protocol v3. Every written article
  becomes a law of its own and is rendered by the factory's own code (the law's titles above the article, the article,
  the passages it refers to). Its gold is the article's rules, or a «não tipável» reason, with every quote derived by code
  from the text and checked by the factory's checker. Train 1 318 rows: the 957 earlier training articles rendered again,
  plus 359 new articles written in the v3 shape (titles that name the procedure, remissões, alíneas, «não tipável»,
  gt/ge, amounts as conditions); 98 rows are «não tipável». v11's old-format rule rows were taken out. Mix 35 470
  examples, rank 16, from the base.
- Measured on 200 new articles in the v3 shape, split by id into dev 104 (studied) and sealed 96 (committed before any
  reader answered it), and on v11's 393 measured articles rendered in v3 (never trained on).
- Run: training ended 07:12Z on one H100, USD 16.33 for the hours billed so far (`training/runs/v12/`).
- Serving correction, disclosed: the first read gave v12 each answer schema with its keys in alphabetical order (the
  data rows are written with sorted keys), while v12 was trained on answers in the factory's order. A guided decoder
  writes the keys in the schema's order, so v12 had to begin every answer with «nao_tipavel», and set it on 100 of 104
  dev answers (the gold has 25). Sealed settled 10.4 % that way. The reader now restores the factory's order
  (`--order required`, checked on all 593 measured rows); the first read is kept (`leitor-a14.attempt1.jsonl`).
- Results (`reports/measure/regras-v12-2026-11-03.md`). «Settles» = passes the factory's checker against the article's
  text and has the same canonical content as the gold: what the factory records.

| set | base + v11 | base + v12 | another family's frontier model |
|---|---|---|---|
| sealed, 96 (never studied) | 4.2 % | **55.2 %** [45.2, 64.8] | 81.2 % |
| dev, 104 (studied for errors) | 4.8 % | 44.2 % | 80.8 % |
| v11's articles in v3, 393 | 0.0 % | **63.9 %** [59.0, 68.5] | — |

  v11 was never trained on v3 and was read with the alphabetised schema. On dev, v12 settles 44 of the 79 articles that
  hold a rule (the frontier model 59) and 2 of the 25 that hold none (the frontier model 25): it seldom says a passage
  holds no rule of the type. When its answer passes the checker it settles in 46 of 58; the 46 that fail mostly quote
  words that are not the passage's own (the vocabulary's wording instead of the text's, words in another order), or
  quote a source that does not say the value.
- On the real law (rules round 8, the 12 targets left open), v12's reading passed the checker on 1 (198.º n.º 1) and did
  not replicate the other family's: it leaves out the JOUE publication. Nothing settled. On the real passages v12 takes
  conditions from neighbouring numbers, names procedures and contract types the words do not name, and writes rules for
  the 5 targets that hold none.

## Not for publication
The rule-test log names the reader of the other family; findings about specific vendors or municipalities stay out.
