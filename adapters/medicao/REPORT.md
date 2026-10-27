# Extraction tests for TED and BASE contratos: v1, v2 and v3 side by side

Details: ted/REPORT-v1.md, ted-v2/REPORT-v2.md, ted-v3/REPORT-v3.md, contratos/REPORT-v1.md. Criteria:
CRITERIA-ted-contratos-v1.md, CRITERIA-ted-v2.md and CRITERIA-ted-v3.md, each sealed (sha256 in BUILD-LOG.md) before its sample was drawn. Wilson 95 % intervals.

| | TED v1 (X.0–X.2) | TED v2 (X.3–X.6) | TED v3, B only (X.8–X.10) | BASE contratos v1 (X.5–X.6) |
|---|---|---|---|---|
| sample | 100 TED-XML + 100 eForms, seed 20261027 | 100 + 100, seed 20261028, v1's 200 excluded | 100 + 100 contract notices, seed 20261029, v1's and v2's 400 excluded | 200 records of 2026, seed 20261027 |
| parser | cf1ee6bd… | b277c007… (eForms dispatch date fixed) | 715a2dd5… (ORIGINAL form; title) | adapter 0f4a52c3… |
| A, required fields | PASS (98.8–100 %) | PASS (all 100 %) | stands from v2 | PASS (99.5–100 %) |
| B, another source | NOT RUN (Storage closed) | **FAIL** 53/57 = 93.0 % (83.3–97.2); joined 31/93 | PASS 189/192 = 98.4 % (95.5–99.5); joinable 102/200 | PASS 64/64 (94.3–100); joined 17/26 |
| C, blind reader | **FAIL** 1 597/1 640 = 97.4 % (96.5–98.0) | PASS 1 652/1 653 = 99.9 % (99.7–100) | stands from v2 | PASS 1 514/1 514 (99.7–100) |
| disagreements | 39 code (eForms dispatch date), 2 joint buyers, 2 change notice that contradicts itself; reader 0 | C: 1 code (multilingual notice, first language form read); B: 4 wrong joins, parser 0 | 2 wrong joins, 1 sources differ (TED restricted, BASE Concurso público); parser 0 | none |
| verdict as written | not measured; fix and v2 | not measured (B) | with v2's A and C: **measured** | **measured** |

## How the two special kinds are counted
- Joint procurement (v1 n=127, six buyers): counted in C. v1 never said which buyer to give; v2 defines the buyer as the
  first one (the first ContractingParty in eForms, ADDRESS_CONTRACTING_BODY in TED-XML) for the parser and the reader
  alike. It stays one of v1's 43 disagreements. v2's sample had 9 notices with several buyers (5 eForms with two
  ContractingParty, 4 TED-XML with ADDRESS_CONTRACTING_BODY_ADDITIONAL); none disagreed on the buyer.
- A change notice whose coded deadline contradicts its change text (v1 n=125): counted in C as a disagreement classified
  «text ambiguous», not dropped; it is inside v1's 97.4 %. v2 kept v1's rule (every disagreement counted and classified).
  v2's sample had 18 notices carrying efac:Change; none disagreed on the deadline.

## Where TED stands
Measured: A and C on v2's sample, B on v3's (join key buyer + deadline + title containment 0.5, written as code before
the draw). C ran with v2's parser; v3's parser differs from it only in TED-XML's ORIGINAL form (one value of v2's 400
development notices changed) and the added title. B speaks for the joinable half of TED contract notices.
