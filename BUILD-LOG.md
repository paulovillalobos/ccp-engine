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

## 2026-10-24 A4 — core signatures (commit: Core: append-only bitemporal store, rules as data, evaluate, entities, governance log)
- Done: engine/store.py Writer (append refuses an existing (id, revision), revise = next revision with supersedes,
  mark_stale = revision with reason) + query(type, known_at, valid_at) + facts_of(unit) walking up the graph;
  engine/rules.py (RULE_TYPES, REQUIRED_PARAMS, order by stage, applies() with None for unreadable, package(), diff());
  engine/evaluate.py (selector → jurisdiction → simple → aggregate with coverage first; typed reasons; manifest required;
  natural persons unnamed); engine/entities.py (candidate ids, link lifecycle as new revisions, merge raises);
  engine/governance.py Log (propose/correct/review/approve/reject/dispute/adjudicate/invalidate, each replayed before
  it is written; human-only approve; readings settle only by blind other-family uphold; write_state);
  engine/manifest.build; governance/principals.json for production (empty events.jsonl); tools/make_fixtures.py and a
  test that the committed fixtures re-derive byte for byte. 44 tests green; verify green.
- Next: A5, FILL-PLAN.md (B1–B4 with their red tests in tests/fill/), AUDIT.md, schemas/TRACEABILITY.md.
- Why: evaluate() reproduces the three fixture verdicts, so the fixtures are now executable examples, not prose.

## 2026-10-24 A5 — the fill plan (commit: Fill plan: red tests B1–B4, FILL-PLAN, AUDIT, TRACEABILITY)
- Done: tests/fill/test_b1..b4 (8 tests, all red: modules, CCP capture with 607 notes and the vigente diff, rules v0 with
  two families, engine v0 at scale); FILL-PLAN.md with the interface each B1 module must expose and the done criterion of
  each task; AUDIT.md (13 checks for Monday, compare against tag phase-a); schemas/TRACEABILITY.md (12 invariants, 21
  objects, 8 rule types, three clocks + record clock, the six pieces as the builder reads them, layers and §10 steps).
- Next: phase B in this order: B1 → B2 → B3 → B4 (B4 waits for the extractor's data/facts/). Each against its red test.
- Why: the scaffold dictates the fill: whoever continues implements against the signatures, schemas and red tests, and
  writes a DECISIONS row before changing any of them.
- Phase A done criterion checked: verify ok (3 stores, 12/12 overlays refused); 44 scaffold tests green; 8 fill tests
  red; TRACEABILITY without gaps; DECISIONS, FILL-PLAN, AUDIT, BUILD-LOG written; an extractor can start from schemas/ +
  fixtures/ (data/README.md says where and in what shape).

## 2026-10-24 audit of phase A (commit: Audit of phase A: 22 of 24 red-team mutations pass verify; rating 6/10)
- Done: AUDIT-2026-10-24-PHASE-A.md; tools/redteam_verify.py (24 mutations, 22 MISSED, 2 caught by side effects). Gate re-run clean; CI green.
- Next: A3b (six items in the audit) before B1: re-derive every verdict in verify, reconcile every stored state with the
  log, manifest cross-checks, law-clock consistency; one overlay per new check; redteam prints 0 MISSED.
- Why: verify v0 checks invariants object by object; a `cumpre` contradicted by its own fact passes today (M16).

## 2026-10-24 product rule: principals by role (commit: Product rule: principals by role ...)
- Done: schemas/principals.schema.json rewritten to the five roles (pessoa, leitor A/B, extrator, redator, ferramenta
  with version and code hash); id prefix = role; model_family enum = A/B; approve/adjudicate require `pessoa:`;
  governance CAPABILITIES by role; a pessoa's product_rule with a reason settles on record; verify PROV checks every
  non-retired ferramenta's code hash; tools/register_tool.py; production governance/principals.json (pessoa:paulo,
  leitor:a/b, extrator:a, redator:a, five ferramentas) and event 1 = the product rule in Paulo's words. DECISIONS D22.
  NORMALISE layer (D23): raw.text derived by a versioned extractor (engine/extract.py), re-derived by verify I01;
  engine/sources.record_raw; tools/capture_dr_consolidated.py (headless Chrome, one read). Fixtures regenerated;
  verify ok; 44 tests green.
- Next: the two DR captures into law/ (CCP consolidated; DL 177/2026), inspect notes and per-article history, fit
  passagem/vigencia to the real shape; then A3b.
- Why: Paulo's product rule for the log; and the DR page is a rendered DOM, so offsets need a re-derivable text.
