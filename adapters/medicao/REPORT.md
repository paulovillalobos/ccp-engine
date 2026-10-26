# Extraction tests for TED and BASE contratos: v1 and v2 side by side

Details: ted/REPORT-v1.md, ted-v2/REPORT-v2.md, contratos/REPORT-v1.md. Criteria: CRITERIA-ted-contratos-v1.md and
CRITERIA-ted-v2.md, each sealed (sha256 in BUILD-LOG.md) before its sample was drawn. Wilson 95 % intervals.

| | TED v1 (X.0–X.2) | TED v2 (X.3–X.6) | BASE contratos v1 (X.5–X.6) |
|---|---|---|---|
| sample | 100 TED-XML + 100 eForms, seed 20261027 | 100 + 100, seed 20261028, v1's 200 excluded | 200 records of 2026, seed 20261027 |
| A, required fields | PASS (98.8–100 %) | PASS (all 100 %) | PASS (99.5–100 %) |
| B, another source | NOT RUN (Storage closed) | **FAIL** 53/57 = 93.0 % (83.3–97.2); joined 31/93 | PASS 64/64 (94.3–100); joined 17/26 |
| C, blind reader | **FAIL** 1 597/1 640 = 97.4 % (96.5–98.0) | PASS 1 652/1 653 = 99.9 % (99.7–100) | PASS 1 514/1 514 (99.7–100) |
| disagreements | 39 code (eForms dispatch date), 2 joint buyers, 2 change notice that contradicts itself; reader 0 | C: 1 code (multilingual notice, first language form read); B: 4 wrong joins, parser 0 | none |
| verdict as written | not measured; fix and v2 | not measured (B) | **measured** |

## How the two special kinds are counted
- Joint procurement (v1 n=127, six buyers): counted in C. v1 never said which buyer to give; v2 defines the buyer as the
  first one (the first ContractingParty in eForms, ADDRESS_CONTRACTING_BODY in TED-XML) for the parser and the reader
  alike. It stays one of v1's 43 disagreements; v2's sample had joint notices with no disagreement.
- A change notice whose coded deadline contradicts its change text (v1 n=125): counted in C as a disagreement classified
  «text ambiguous», not dropped; it is inside v1's 97.4 %. v2 kept v1's rule (every disagreement counted and classified);
  v2's sample had no such case.

## Where TED stands
The parser now reads what a second reader reads (C 99.9 %). What fails is B's join key (same buyer and same deadline): 4
of its 31 pairs are different procedures, which is also why only a third of TED contract notices find a BASE anúncio. A
B-only v3 with a better key (buyer, deadline and title, or the TED number BASE carries) on a fresh sample would settle it;
not started without a decision.
