# Audit of phase 1 (A3b, the gate) — 2026-10-24, by the builder — architecture 8/10

Scope: commits 0e6ad46..cbbd3ce by the filler (six commits: RED, MAN, STATE, TIME, cross-object checks, overlays + red
team + docs). Checked from a clean tree against AUDIT.md and with eleven new mutations the filler had not seen.

## What the filler delivered

| Check | Result |
|---|---|
| verify | ok on the three stores; 21 overlays refused with their code |
| Scaffold tests | 52 green; tests/fill 8 red (untouched) |
| Red team | 37 mutations, 37 caught, 0 MISSED |
| Contract | `git diff f45988d..HEAD -- schemas/*.json`: 0 lines; no public signature of engine/ changed |
| Decisions | D25 (manifest.log_head = head of a prefix of the log not after produced_at) and D26 (a rule's validity is the validity of the text it cites) recorded |
| CI | green; tools re-registered (PROV) |
| False alarm control | a fact known after the verdict that would flip it does not break the stored verdict (bitemporal read respected) |

## What it missed (five of eleven new mutations passed verify) — fixed in this audit

| # | Mutation | Fix | Overlay |
|---|---|---|---|
| N3 / N4 | an entity omitted from, or invented in, `veredicto.entities` | RED now reads the entities of the unit's lineage (ancestors and descendants) and compares `entities` | `red-entity-omitted` |
| N5 | a verdict citing a passage version marked `revoked` | TIME refuses a revoked cited version | `time-cited-version-revoked` |
| N6 | a gap between two versions of a passage | TIME requires contiguous versions (`valid_to` = next `valid_from`) | `time-gap-between-versions` |
| N9 | a settled link whose target entity's head revision is stale | STATE refuses a live link to a stale entity | `state-link-to-stale-entity` |
| N11 | a verdict whose `known_at` precedes the log head it claims | MAN requires the head event's `at` ≤ the verdict's `known_at` | `man-verdict-before-log-head` |

After the fixes: 26 overlays, 43 mutations, 0 MISSED, 52 tests green, verify ok, PROV re-registered (verify@8,
make-fixtures@3).

## Rating by axis

| Axis | Phase A | Now | Why |
|---|---|---|---|
| Domain model | 8 | 8 | unchanged |
| Where the law lives | 8 | 8 | unchanged since the DR capture; B2 still to load it |
| Law in time | 7 | 8 | TIME: versions ordered, contiguous, no overlap; vigencias start versions; rules inside the text they cite; verdicts cite text in force and not revoked |
| Explainability | 7 | 8 | manifest verified against log, package, adapters, snapshots; entities reconciled |
| Audit / verification | 4 | 8 | every stored verdict re-derived by `evaluate`; every stored state the log's replay; 43 mutations caught. Not 9: the law is not loaded yet, so RED has only run over fixtures; no measurement replay exists |
| Change handling | 8 | 8 | unchanged; PROV proved itself by firing on the audit's own edits |

**Overall 8/10.** The gate now does what invariant 3 says. The next two points are data, not code: the law (phase 2, B1
+ B2) and the facts with their measurement (phase 3, B3 + B4 + §8).
