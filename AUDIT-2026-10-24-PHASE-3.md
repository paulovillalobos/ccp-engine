# Audit of phase 3 (B3 rules, B4 engine, B5 measurement, B6 API) — 2026-10-24, by the builder — architecture 9/10

Scope: commits e3642f8be..e142bbb69 by the filler (D0.1–D0.3 debts, B5 set-up, B3, B4, B5, B6, CI split). Checked from a
clean tree, with the fixture red team and four mutations on the real store. Three verification gaps found and closed here.

## What the filler delivered (re-derived)

| Item | Result |
|---|---|
| Gate | verify ok: fixtures 58 objects; repo 68,096 objects, 37 events; measure store 68,341; BENCH/MEAS ok; 43/43 fixture mutations caught; CI green (9 min 55 s, split in jobs) |
| Tests | 60 scaffold green (295 s); fill: 18 green, 2 red = B4 (data/facts empty) |
| D0 debts | EU threshold regulations structured by `eurlex-html@1`; six codes structured by `structure_codigo` (D34); remissões resolved to article/number/alínea (D0.3) |
| B3 | 18 rules read by two families on the real text: 36 log events (18 propose by leitor:a, 18 blind review by leitor:b); raw answers kept with sha256; **1 settled** (`regra:ccp:limiar-ajuste-direto-obras@v2`: art. 19.º d), 150 000 EUR, agrees with the DL 177/2026 reform), 17 `proposed`; exact agreement A vs B 1/18, direction agreement 14/18; `pacote:ccp@2026-10-01` names the one settled rule; no package for 2026-09-30 |
| B4 | `tools/run_engine.py` tested on fixtures; blocked: `data/facts/` is empty (the extractor has not delivered); the canonical fields the 18 rules read are listed in BUILD-LOG |
| B5 | held-out set declared and frozen before any rule entered the log (git: 4b518c21e before dca0342a6); 20 FIXTURE cases, 236 (case, rule) pairs, both readers answered 232, exact 0.44, direction 0.96, 134 pairs queued for a pessoa; Wilson intervals computed; figures mostly empty by design (no real data) |
| B6 | read-only API v1 served locally from the store, 7 tests green in 0.7 s, not deployed |
| Contract | no schema change; no public signature changed (two private helpers of structure.py renamed); D34–D38 recorded; model code isolated in `readers/` (D38), imported by nothing in engine/, tools/ or verify.py |

## Gaps found with mutations on the real store — fixed in this audit

| # | Mutation | Before | Fix | Code |
|---|---|---|---|---|
| R1 | a leitor's raw answer file edited | passed | every event with `answer_sha256` must have its file hashing to it | READ |
| R1b | a measurement annotation edited | passed | annotations and HELD-OUT.json sealed in the log by `tools/measure.py seal` (`ferramenta:measure`, evento:38); INDEX.json per file | SEAL |
| R2 | held-out frozen date moved | passed (its sha256 covered only its own `definition`) | the whole file's sha256 is in the seal event | SEAL |
| R3 | the settled rule's threshold changed in rules/ | passed | rule params, conditions and cited passages must equal the latest propose/correct payload | STATE |

A fourth finding: eight unsettled rule files cited the union of both readers' passages (D37), so the replay differed
from the log's proposal. D39 supersedes that clause: a rule cites the proposer's passages; the reviewer's differing
passages stay in its review payload; the eight files were regenerated from the log (same revision: a replay). The
reading-versus-rule check now applies to the proposer and to upholding reviewers only. `readers` added to the module
names the gate refuses.

## What stands out

- The reading protocol is honest: leitor:a (family A) proposes, leitor:b (family B) reviews blind, nothing settles
  without exact replication. With AMALIA as proposer, 1 of 18 settles; 14 of 18 agree on the value the rule depends
  on. The disagreements are mostly encodings (a list vs a scalar, extra parent passages), visible in DESACORDOS.md.
- Everything that needed data stopped where it should: B4 and the figures of B5 wait for `data/facts/`.

## Rating by axis

| Axis | Phase 2 | Now | Why |
|---|---|---|---|
| Domain model | 8 | 8 | unchanged |
| Where the law lives | 9 | 9 | EU thresholds and the six codes now structured; remissões resolved |
| Law in time | 9 | 9 | unchanged |
| Explainability | 8 | 9 | a settled rule cites real text with offsets; the API returns verdict + citation + version + manifest |
| Audit / verification | 9 | 9 | three real gaps closed; not 10 until RED has re-derived verdicts over real notices |
| Change handling | 8 | 9 | evidence files anchored in the log; tools versioned and hashed |

**Overall 9/10, unchanged.** The missing point is not code: real facts (the extractor), a settlement rate above 1/18
(a product decision on who proposes and who reviews), one hundred real cases with the pessoa's adjudications, and a
figure with an interval over them.

## Decisions for the pessoa (product, not legal content)

1. Who proposes: today leitor:a (AMALIA base) proposes and leitor:b (Reader B) reviews; 1/18 settles. Swapping roles keeps
   invariant 5 (two families, blind replication) and will raise the rate; AMALIA then measured as reviewer.
2. What counts as replication: exact equality of passages, conditions and params (today), or equality after a
   canonical form of conditions (`in [x]` = `eq x`, sorted lists) decided as a product rule.
3. The extractor's delivery: `data/facts/` with the fields BUILD-LOG lists; B4 and B5 run the moment it lands.
4. The 134 queued (case, rule) pairs: adjudications of facts in the log (`Log.adjudicate`), by the pessoa.
