# Audit of phase A (2026-10-24, same day, by the builder) — architecture rating 6/10

Scope: the scaffold at tag `phase-a` (commit 82134e9). Method: the gate re-run from a clean tree; 24 mutations outside
the twelve broken overlays (`tools/redteam_verify.py`); the architecture graded on function, not stack: domain model, where
the law lives, law in time, explainability, audit, change handling. "Works" is a 5.

## What holds

| Check | Result |
|---|---|
| `python -I verify.py` | ok: 3 stores, 0 failures; 12/12 overlays refused with their code; no model or network import in engine/, tools/, verify.py |
| Scaffold tests | 44 green; fixtures re-derive byte for byte from `tools/make_fixtures.py` |
| Fill tests | 8 red, as designed (B1–B4) |
| CI | green on `main` and on `phase-a` (17 s) |
| Boundary | `adapters/` and `data/` untouched; `git diff phase-a..HEAD` empty |
| Attribution | 0 AI-attribution lines in 6 commits |
| `evaluate()` | reproduces the three fixture verdicts (result, reason, citation, facts, manifest) and answers `nao_avaliado` with the right reason for selector absent, conflict, coverage, document without text |
| Governance | human-only approve, no human approval of a reading, blind other-family settlement, no self-review, no self-adjudication, chain tamper detected: all refused by `Log` and by replay |

## What does not hold: 22 of 24 red-team mutations pass verify

verify v0 checks each invariant **locally** (one object against its schema, one quote against its passage, one event
against the replay). It does not check **consistency across objects** and it does not **re-derive verdicts**, which
invariant 3 says it must. The two caught (M05, M17) were caught by side effects (a stale diff, a wrong quote), not by
the check that should exist.

| # | Mutation that passes verify | Invariant breached | Severity |
|---|---|---|---|
| M16 | a `cumpre` verdict whose fact says 3 days against a 6-day minimum | 3 (re-derive verdicts), 6 (false `cumpre`) | **critical**: this is the exact failure the system exists to prevent |
| M06 | `manifest.log_head` ≠ the log's head | 3, §7 reproducibility | high |
| M01/M01b | `manifest.package` does not contain the verdict's rule | §7 | high |
| M02 | verdict names a rule revision that does not exist | 2, §7 | high |
| M03 | verdict `valid_at` before the cited passage version was in force | 8 (law clock) | high |
| M04 | verdict uses a fact of another unit | 6 | high |
| M08 | fact `valid_at` after the verdict's `valid_at` | 8 | high |
| M09 / M10 / M22 | link or adapter `settled`, dispute adjudicated by X, with no matching log event | 4, 9 (stored state ≠ replay) | high; only `regra` state is cross-checked (I05) |
| M07 | a reading chose passages the rule does not cite | 4, 5 | medium |
| M11 / M15 | vigencia date matches no passage version; passage versions overlap | 8 | medium |
| M19 | rule `valid_from` after the only passage version it cites | 8 | medium |
| M13 | unit parent cycle | §3 graph | medium (facts_of would loop forever) |
| M12 | conflict declared on a field its facts do not carry | 7 | medium |
| M18 | fact field absent from its adapter's mapping | §6 adapter as data | medium |
| M20 | two revisions with different content, both "current" by state | 9 | low (store picks highest; verify should check only the head is non-stale-current) |
| M21 | `held_out: true` without `frozen_at` | §8 | low |
| M23 | natural person relabelled `privada` in the verdict, with name | 11 | medium: I11 trusts the verdict's own `type`; it must read the entity record |
| M14 | orphan `raw_bytes` file | 1 | low |
| M05 | a package naming a `proposed` rule | §3 package = replay of settled rules | medium; caught only because the stored diff went stale (DIFF), not by a state check |

## Rating by axis (architecture as code, not as paper)

| Axis | Score | Why |
|---|---|---|
| Domain model | 8 | Every object of §3 has a schema with stable ids; facts ≠ assertions; unit graph; entities linked, never merged; eight rule types as data with required params enforced. Missing: adapter mapping is declared but not used to validate facts (M18); no object for the measurement run itself |
| Where the law lives | 6 | Passages with versions, offsets into the raw capture, citations verified by offsets; the AI picks ids and code writes quotes. But no law is captured yet (B2), `vigente` and `structure` are interfaces only, and the fixture law is a marked paraphrase |
| Law in time | 6 | Three clocks are separate in schema, store query and engine; regime selector first. But the law clock is not cross-checked against anything (M03, M11, M15, M19) |
| Explainability | 7 | Typed reasons, `detail` as data, citation, facts used, assertion compared beside, complete manifest embedded. But the manifest is trusted, not verified (M01, M02, M06) |
| Audit / verification | 4 | The gate exists, bites on the twelve overlays and refuses a model in its own code. It does not re-derive a single verdict and lets 22 cross-object inconsistencies through. A "works" gate would re-run `evaluate` on every stored verdict |
| Change handling | 7 | Append-only revisions with `supersedes`, hash-chained log, packages hashed, diff rebuilt, DECISIONS/AUDIT discipline, fixtures re-derivable. But only rule states are reconciled with the log; links, adapters, disputes are not |

**Overall 6/10.** The contract and the shape are right and executable: an extractor can start, a filler cannot change
shape unnoticed, and the engine already answers `nao_avaliado` for the right reasons. The gate is the weak layer: it is
a schema-plus-local-invariant checker, not yet the re-derivation gate invariant 3 describes. Until it re-computes verdicts
from facts and rules and reconciles every stored state with the log, a wrong `cumpre` can be committed and CI stays green.

## What closes the gap (A3b, before B1; one commit)

1. `verify.check_rederive`: for every stored verdict, gather the unit's facts, conflicts, documents and coverage from
   the store, call `evaluate` with the verdict's own `known_at`, `valid_at` and manifest, and require result, reason,
   citation and facts_used to match (M16, M04, M08). Code `I03R`.
2. `verify.check_manifest`: `manifest.log_head == governance.head(events)`; `manifest.package` exists and names the
   verdict's rule at the verdict's revision; every adapter of the facts used is in `manifest.adapters` (M01, M02, M06).
3. `verify.check_states`: stored `state` of links, adapters, disputes, afirmacao conversions equals the replay (M09, M10, M22);
   packages name only settled rules (M05); readings' chosen passages ⊆ rule passages (M07).
4. `verify.check_law_time`: passage versions do not overlap; every vigencia `valid_from` is a version of its passage;
   a rule's `valid_from` is inside some version of every passage it cites; a verdict's citation version is in force at
   `valid_at` (M03, M11, M15, M19).
5. Smaller: parent cycles (M13), conflict field ⊆ its facts' fields (M12), fact field ∈ adapter mapping (M18),
   I11 reads the entity record's type (M23), `held_out ⇒ frozen_at` (M21), orphan raw bytes (M14), at most one
   non-stale head per id (M20).
6. One broken overlay per new check, generated by `tools/make_fixtures.py`; `tools/redteam_verify.py` must print 0 MISSED.

Expected rating after A3b: 7–8 (audit axis to 8; the remaining points are B2's law and §8's measurement, which no
scaffold can supply).
