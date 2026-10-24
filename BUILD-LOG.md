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

## 2026-10-24 law as it is served (commit: Law: DR notes grammar, per-article history, DL 177/2026 ...)
- Done: four more raws in law/ from the builder's passive reads (DL 177/2026 detail page 14:53:11Z; history views of arts. 20,
  113, 136 at 14:56Z via tools/capture_dr_history.mjs, copied into the repo); extractor dr-article-history@1 (fragments +
  notes); engine/vigente.py: NOTE_RE parses all 735 notes of the consolidated page (53 REVOGADO in capitals, 4 without
  date), norma_slug, versions_from_history (rectifications folded; art. 20 -> 4 legal versions, art. 136 -> 3, untouched
  by DL 177/2026), signatures of notes_to_vigencias and vigente (B2); tests/test_vigente.py against the real strings;
  FILL-PLAN B2 rewritten to the real shape (selector passage = dl-177-2026:art7.2 Norma transitória n.º 2; the DL page
  carries the republished CCP after "Republicação"); DECISIONS D24. Tools re-registered (hashes).
- Next: A3b (verify re-derives verdicts and reconciles states) if the independent review quota remains; else the builder: B1 (structure,
  passages, serve, package), then B2 per FILL-PLAN with the history capture over ~384 articles.
- Why: the form of the law is now fixed from the pages themselves, not from a description.

## 2026-10-24 A3b.1 verify re-derives every verdict (commit: verify: re-derive every stored verdict with evaluate (RED))
- Done: verify.check_rederive (code RED). For each current non-stale veredicto: facts of the unit and its ancestors
  (store.facts_of at the verdict's known_at), conflitos and documentos of that chain, afirmações of the unit, entidades
  with a role in the unit, the rules of manifest.package at the revisions it names, coverage of the manifest's adapters;
  engine.evaluate with the verdict's known_at, valid_at and manifest; id, rule, result, reason, citation,
  assertions_compared and set(facts_used) must be equal, and the unit's kind must be in the rule's applies_to. detail is
  free text and is not compared. Helpers unit_chain (cycle-safe), coverage_of, package_rules. Valid fixtures: 0
  failures (the three stored verdicts re-derive). Red team: M16, M04, M08 now RED (also M01b, M02, M03, M19 by side
  effect). ferramenta:verify@2 registered.
- Next: A3b.2 check_manifest (MAN).
- Why: a `cumpre` contradicted by its own fact (M16) passed the gate; invariant 3 says verify re-derives verdicts.

## 2026-10-24 A3b.2 verify checks manifests against the store (commit: verify: manifests checked against log, packages, adapters and snapshots (MAN))
- Done: verify.check_manifest (code MAN). log_head is the head of a prefix of the governance log whose last event is not
  after produced_at (also for each pacote's log_head); manifest.package exists, has the manifest's law_version and names
  the verdict's rule at its exact revision; the rule revision exists; every adapter of a fact used is in
  manifest.adapters; every source snapshot names a raw record with that sha256, source and captured_at. Red team: M01,
  M01b, M02, M06 now MAN. ferramenta:verify@3. Deviation from the A3b wording: DECISIONS D25 (prefix head, not equality
  with the current head).
- Next: A3b.3 check_states (STATE).
- Why: the manifest was trusted; a verdict could name a package without its rule, a revision that does not exist or a
  log head the log never had.

## 2026-10-24 A3b.3 verify reconciles every stored state with the log (commit: verify: stored states of links, adapters, disputes, conversions, packages and rule heads are the log's replay (STATE))
- Done: verify.check_states (code STATE), fed by the replay check_governance already builds. Link with evento: its
  replayed state; link without evento: only a ferramenta's nif_exact. Adaptador: replayed state, `proposed` when the log
  has never seen it. Disputa: (raised_by, veredicto, state, adjudicator, outcome) equal to the replayed dispute, and its
  adjudication event is one of that dispute's events. Afirmação: conversion_evento is the afirmacao_conversao of that
  afirmação by its converted_by. Pacote: every rule it names is settled at the named revision. Regra: every reading's
  chosen_passages ⊆ the passages the rule cites (passages + exceptions); the highest stored revision equals the log's
  revision. Red team: M05, M07, M09, M10, M20, M22 now STATE. ferramenta:verify@4.
- Next: A3b.4 check_law_time (TIME).
- Why: only regra states were cross-checked (I05); a link, adapter or dispute could claim a state the log never gave it.

## 2026-10-24 A3b.4 verify checks the law clock across objects (commit: verify: law clock across passages, vigencias, rules and verdicts (TIME))
- Done: verify.check_law_time (code TIME). Passage versions in strictly increasing valid_from, each closed before the
  next opens, valid_to after valid_from, only the last open. Every vigencia.valid_from starts a version of its passage.
  Regra: valid_from equals the latest valid_from among the versions it cites (passages + exceptions), lies inside every
  cited version, and does not outlive a closed one (DECISIONS D26, stricter than the A3b wording). Veredicto: the cited
  version is in force on valid_at. Red team: M03, M11, M15, M19 now TIME. ferramenta:verify@5.
- Next: A3b.5 small cross-object checks (GRAPH, FIELD, I11, BENCH, I01 orphans).
- Why: the law clock was checked per object only; a rule could claim validity its text never had.

## 2026-10-24 A3b.5 smaller cross-object checks (commit: verify: unit graph, fact and conflict fields against adapters, entity types from records, frozen held-out cases, orphan bytes)
- Done: verify.check_cross. GRAPH: a unit in a parent cycle, or whose parent is not of an earlier kind (proc -> lote ->
  contrato -> mod). FIELD: a conflito's facts carry its field, its recorded value and sit in its unit's chain; a fact's
  field is in its adapter's mapping and, for a raw origin, the mapping row names the raw's source field. I11 now reads
  the entidade record: a published type that differs from the record, or a name on a record that is a pessoa_singular.
  BENCH: held_out implies frozen_at. I01: raw_bytes no raw record (bytes or derived text) names. Red team: M12, M18
  FIELD; M13 GRAPH; M14 I01; M21 BENCH; M23 I11 — 24 of 24 caught. ferramenta:verify@6.
- Next: A3b.6 one broken overlay per new check from tools/make_fixtures.py, test count, redteam additions, docstring,
  TRACEABILITY, AUDIT, tool registration.
- Why: the audit's smaller gaps; facts_of would loop forever on a parent cycle (now guarded by unit_chain in RED).

## 2026-10-24 A3b.6 overlays, red team, docs (commit: Fixtures: one broken overlay per cross-object check; red team 37 mutations, 0 MISSED; docs and tool registration)
- Done: tools/make_fixtures.py generates nine new overlays (red-cumpre-contradicted-by-its-fact RED,
  man-log-head-never-in-the-log MAN, state-link-settled-without-approval STATE, time-passage-versions-overlap TIME,
  graph-unit-parent-cycle GRAPH, field-fact-not-in-adapter-mapping FIELD, bench-held-out-not-frozen BENCH,
  i01-orphan-raw-bytes I01, i11-entity-type-from-record I11); fixtures regenerated (21 overlays, all refused with
  their EXPECT). tests/test_verify.py: 21 overlays, first codes I01..I12 + RED MAN STATE TIME GRAPH FIELD BENCH.
  tools/redteam_verify.py: 13 mutations added while implementing (M24..M36), a final "N MISSED" line and exit code;
  37 CAUGHT, 0 MISSED. verify.py docstring code block for the new checks; VERSION ccp-verify-0.2.
  schemas/TRACEABILITY.md: a row per new check; AUDIT.md: criterion 1 (21/21) and 1b (red team 0 MISSED).
  ferramenta:verify@7, ferramenta:make-fixtures@2. No schema JSON, no engine/ signature, nothing in adapters/ or data/.
- Next: the independent review's audit of A3b; then phase B per FILL-PLAN (B1 copied modules, B2 the CCP capture).
- Why: a check without a broken fixture is a check nobody has seen fail; the red team is the list of gaps to keep at 0.

## 2026-10-24 audit of phase 1 (commit: Audit of phase 1: five more cross-object checks ...)
- Done: AUDIT-2026-10-24-PHASE-1.md; the filler's six commits accepted; five gaps found with new mutations and closed
  (entities reconciled in RED; revoked and non-contiguous versions in TIME; live link to stale entity in STATE; log head
  after known_at in MAN); five overlays generated; redteam 43/43; tools re-registered. Rating 8/10.
- Next: phase 2 (the builder): B1 then B2 per FILL-PLAN.md; the independent review audits at the end.
- Why: a gate audited only by the person who wrote it is not audited.
