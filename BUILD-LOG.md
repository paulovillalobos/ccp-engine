# BUILD-LOG

One entry per commit: done / next / why. Written so a model change loses nothing. Newest at the bottom.

## 2026-10-24 A1 — skeleton (commit: Skeleton: layers, ownership boundary, CI)
- Done: the eleven directories with a README stating the owner of each; `.venv` on Python 3.12 with `jsonschema` and
  `pytest` pinned in requirements.txt; CI job `verify` (verify.py + scaffold tests, blocking) and job `fill` (tests/fill,
  `continue-on-error`, visible but never blocking); placeholder verify.py; README with principle, the 12 invariants and
  the ownership table.
- Next: A2, the contract: one JSON schema per object of ARQUITECTURA.md §3, one valid fixture per object, one broken
  overlay per invariant, schemas/DECISIONS.md.
- Why: the extractor cannot write a byte until schemas/ and fixtures/ exist and verify passes (§14).

## 2026-10-24 A2 — the contract (commit: Contract: one schema per object...)
- Done: 23 schemas (defs + 20 objects of §3 + manifesto + principals), JSON Schema 2020-12, resolved locally by
  engine/schema.py; 59 valid fixtures (one per object, all eight rule types, a 21-event hash-chained governance log,
  four raw captures with their bytes under raw_bytes/) and 12 broken overlays, one per invariant, each with its EXPECT
  code; schemas/DECISIONS.md D1–D21; tests/test_schemas.py (7 tests green).
- Next: A3, verify.py v0: load the three stores, validate, run checks I01–I12 + references + uniqueness, require every
  broken overlay to fail with its code; CI green.
- Why: the extractor starts from schemas/ and fixtures/ alone (§14); the broken overlays are what proves verify bites.

## 2026-10-24 A3 — verify.py v0 (commit: verify v0: ...)
- Done: verify.py loads three stores (fixtures/valid; law/+rules/+governance/; data/) through engine/store.py (read side,
  I09 at load), checks REF, I01, I02, I04 (engine/governance.py replay), I05, I06 (engine/manifest.is_complete), I07,
  I08, I10, I11, I12, PACK, LAYOUT, and the static code guard I03/I10 over engine/, tools/ and itself; runs every broken
  overlay and requires its EXPECT code among the failures. Result: 0 failures on the three stores, 12/12 overlays refused.
  tests/test_verify.py (5 tests). Dispute events now carry payload.disputa so the replay can match the adjudication.
- Next: A4, the write side and the core signatures: store.append/revise/mark_stale/query(known_at, valid_at),
  rules.py (eight types as data, order, diff), evaluate.py, entities.py, governance.py Log (propose, review, approve,
  dispute, adjudicate), manifest.build; a test that evaluate reproduces the three fixture verdicts.
- Why: the gate had to exist before any engine code so that A4 is written against it, not the other way round.
