# AUDIT — the Monday list (An independent review audits phase B against the scaffold)

Run from a clean checkout of `main`:

```
.venv/bin/python -I verify.py
.venv/bin/python -m pytest tests --ignore=tests/fill -q
.venv/bin/python -m pytest tests/fill -q
```

| # | Check | Pass when |
|---|---|---|
| 1 | verify | `verify: ok`; three stores with 0 failures; 12/12 broken overlays refused with their EXPECT code |
| 2 | Scaffold tests | every test outside `tests/fill` green (44 at the end of phase A) |
| 3 | FILL-PLAN tests | `tests/fill/test_b1..b4` green; a still-red B4 is acceptable only if `data/facts/` has not been delivered by the extractor and BUILD-LOG says so |
| 4 | Contract untouched | `git diff <phase-A-tag>..HEAD -- schemas/` is empty, or every changed file has a new row in `schemas/DECISIONS.md` that names it |
| 5 | Signatures untouched | the public functions of `engine/{store,rules,evaluate,entities,manifest,governance,schema,canon}.py` keep their names, parameters and docstring contracts; any change has a DECISIONS row |
| 6 | TRACEABILITY complete | every row of `schemas/TRACEABILITY.md` names a file, a symbol and a test that exist; no row says "pending" |
| 7 | Fixtures re-derive | `tests/test_fixtures_rederive.py` green (fixtures equal `tools/make_fixtures.py` output) |
| 8 | Boundary respected | no commit in phase B touches `adapters/` or `data/` (`git log --stat -- adapters data` shows only the extractor's commits, if any) |
| 9 | No model in the gate | `verify.check_code()` empty; no module of `engine/` or `verify.py` imports a model or network library |
| 10 | Governance | `governance/events.jsonl` replays with 0 errors; every B3 rule has two readings of distinct families; no `approve` on a `regra`; every `approve` is `pessoa:` with a reason |
| 11 | Law re-derived | B2's raw pages hash to their sha256; `vigente(2026-09-30)` vs `vigente(2026-10-01)` differ exactly per the DL 177/2026 notes |
| 12 | BUILD-LOG | one entry per phase-B commit with done / next / why; every deviation from FILL-PLAN named there and in DECISIONS |
| 13 | No AI attribution | no `Co-Authored-By` or model names in commits, PRs or GitHub-visible prose |

Tag of the end of phase A: `phase-a`. Compare against it.
