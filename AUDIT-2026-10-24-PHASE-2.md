# Audit of phase 2 (B1 + B2, the law) — 2026-10-24, by the builder — architecture 9/10

Scope: commits 2b507d46..edd64841 by the filler (B1 modules; red tests for B2b/B2c; B2a.1 histories; B2a.2 structure,
normas, vigencias; B2a.3 versions; B2b corpus; B2c municipal pilot). Checked from a clean tree against AUDIT.md,
FILL-PLAN.md and with three mutations on the real law store. Nothing edited: what was delivered stands.

## Numbers (re-derived here, not copied from the report)

| What | Count |
|---|---|
| Objects in the repository store | 31,787 (verify: 0 failures in 27 s; CI 6 min 17 s, green) |
| Raw captures | 371 records, 731 byte files tracked (275 MB on disk, 15 MB packed); 315 article/annex histories, 16 consolidated acts, 25 act detail pages, 4 EUR-Lex regulations, 11 municipal records |
| CCP | 596 artigo passages, 3,873 passages in all, 6,304 passage versions, 3,965 vigencias; 1,657 passages with more than one version, up to 7 |
| Histories | 381 articles and annexes with a note: 313 history views captured (0 failures), 68 added once and never changed (one version each) |
| `vigente(2026-09-30)` vs `vigente(2026-10-01)` | 2,583 passages differ = exactly the passages whose vigencia names `norma:dl-177-2026` with `valid_from` 2026-10-01 |
| Normas | 386 registered (24 timeline acts, every act a note names); 43 captured; 25 structured; regional: Açores DLR 27/2015/A (610 passages), Madeira DLR 34/2008/M (40) and DLR 8/2025/M (908); EU thresholds: 4 delegated regulations 2025 registered with ELI |
| Remissões of the CCP text | 71 references; 14 distinct Portuguese acts, 14 captured (100 %); 17 EU acts, not captured except thresholds; 6 resolved to a passage |
| Municipal pilot | 10 municípios, 12 records found, 11 captured, 7 with a text layer; linear estimate for 308 with its limits stated |
| Tests | 52 scaffold green; fill: B1, B2, B2b, B2c green, B3 and B4 red as designed |
| Contract | schemas: `passagem.kind` + `anexo` (D27), `vigencia.effect` + `entra_em_vigor` (D32), both with rows; D28–D33 recorded; no public signature changed (one comment on `vigente`) |

## Red team on the real law (through the full verify, ~30 s each)

| Mutation | Result |
|---|---|
| One word changed in a real passage version (art. 136.º n.º 1) | caught, I01 |
| A real vigencia (art. 20.º n.º 1, 2026-10-01) moved one day | caught, TIME |
| The derived working text of a real history page edited | caught, I01 |

## What stands out

- The republished CCP inside DL 111-B/2017 and DL 177/2026 is structured as quoted text of the amending article
  (`dl-177-2026:art2.q1.art11.1.a`), never as independent passages: the CCP text lives once, under `ccp:`.
- The selector passage exists and reads right: `dl-177-2026:art7.2`, Norma transitória.
- Honesty of the log: eight reads with an `http` ELI address were refused by the schema and disclosed; three failed
  walks of the consolidated page disclosed; dateless notes resolved by a stated order (D28, D31).

## Debts phase 3 must clear first (listed, not fixed)

1. The four EU delegated regulations (thresholds) are registered but have no passages: a `limiar` rule for JOUE
   thresholds cannot cite them yet. EUR-Lex layout needs its own extractor.
2. Six captured codes have no passages because `structure` meets a duplicate path (CC, CPPT, CSC, CT, Lei 98/97,
   CRCSPSS): structure@1 knows the CCP layout; a second layout is a versioned extractor, not a patch.
3. Only 6 of 71 remissões resolve to a passage of the cited act; resolution is at act level today.
4. tests/fill now take 100 s (the law store is loaded by several tests); acceptable for CI, worth one shared fixture.

## Rating by axis

| Axis | Phase 1 | Now | Why |
|---|---|---|---|
| Domain model | 8 | 8 | unchanged; annex as passage (D27) fits |
| Where the law lives | 8 | 9 | the real CCP, every version of every altered article, 3,965 notes as vigencias, 386 acts registered, Açores and Madeira structured; not 10 while EU thresholds and six codes are captured without passages |
| Law in time | 8 | 9 | `vigente(d)` over real history; the DL 177/2026 diff re-derives exactly; dateless notes resolved by rule |
| Explainability | 8 | 8 | unchanged until a verdict cites real law (phase 3) |
| Audit / verification | 8 | 9 | 31,787 objects re-derived from bytes in 27 s; three real mutations caught |
| Change handling | 8 | 8 | unchanged |

**Overall 9/10.** The law is in, versioned, dated and re-derivable. The last point is phase 3: rules read by two
families over this text, verdicts over the extractor's notices, and the measurement of §8.
