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
