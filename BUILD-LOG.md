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

## 2026-10-24 phase 2 decision before B1 (no commit of its own; lands with B1)
- Done: DECISIONS D27 written before touching the schema: `anexo` added to passagem.kind.
- Next: B1 with engine/structure.py emitting anexo passages for the code's own annexes.
- Why: the consolidated CCP's Anexos I–XIV carry validity notes (Anexo V revoked by DL 177/2026, art. 8.º); without an
  anexo kind those notes have no passage and would be lost from the vigencias.

## 2026-10-24 B1 modules with their own version (commit: B1: structure, passages, vigente notes and clock, read-only API skeleton, package)
- Done: engine/structure.py (ccp-structure-0.1): a DR working text -> passagem objects with offsets (anexo, parte,
  titulo, capitulo, secao, artigo, numero, alinea, subalinea; amending quotations hang from the quoting passage as
  .qN; a code approved in a decree's annex keeps the decree's own articles under "dl."; an act stops at its first
  annex line or closing formula; fails on duplicates, numbers outside articles, unbalanced quotations). On the
  consolidated CCP page (dr-article-history@1 text): 3425 passages, 594 artigo (570 code + 18 decree + 8 quoted - 2
  shared numbering noted by kind), 14 anexo, offsets exact, schema-valid. engine/passages.py (ccp-passages-0.1):
  passage_text, cite (quote written by code as text[start:end]). engine/vigente.py: notes_to_vigencias (one vigencia
  per (passage, valid_from), highest effect quoted, valid_to = next date; dateless notes per D28), vigente(store,
  date), entry_into_force; NOTE_RE also reads "Parte III do/a" and "Resolução da Assembleia da República" (rar-).
  tools/serve.py (ccp-serve-0.1): the §9 routes; saude/openapi 200, the rest 501 until phase 3; keyed routes 401
  without X-API-Key; 64 KB body (413), JSON only (415), 30 s socket timeout, no trace, no path echoed (404 lists
  routes). tools/package.sh: dist/ccp-service without data/, fixtures, tests or secrets; smoke test /v1/saude OK.
  Schema: passagem.kind + anexo (DECISIONS D27, written before the change). DECISIONS D28 (dateless notes).
  Registered ferramenta:vigente@2, structure@1, passages@1. test_b1 green; verify ok; 52 tests green.
- Next: B2a.1 capture the history view of every article with a note (368 on the page: 365 code, 3 decree).
- Why: the law can only be loaded once the text has a structure with offsets and the notes have a grammar.

## 2026-10-24 red tests for B2b and B2c (commit: Tests: red criteria for B2b (corpus around the CCP) and B2c (municipal pilot))
- Done: tests/fill/test_b2b_corpus.py (timeline acts 23/23 and every note diploma registered with jurisdiction and
  scope; DL 111-B/2017, Lei 30/2021, DL 18/2008 with its entry-into-force article and the four retificações captured,
  the acts with articles structured; >= 90 % of the distinct Portuguese acts the CCP refers to captured; each phase-3
  norm registered and captured or reported missing in law/COVERAGE.md with the address read; an EU norma with its ELI;
  Madeira registered or reported; COVERAGE.md equal to what tools/coverage.py renders) and tests/fill/test_b2c_pilot.py
  (10 município rows with found / captured / with text counts, the default ten unless chosen by BASE volume, and an
  estimate for 308). All six red. data/ holds no BASE anúncios yet, so the pilot is the default ten.
- Correction to the B1 entry: the 594 artigo passages of the consolidated page are 568 of the code, 18 of the
  approving decree (ccp:dl.artN) and 8 inside the decree's quotations (ccp:dl.art5.q1.art1 ...).
- Next: B2a.1 (the history walk is running).
- Why: the phase asks for the red tests before the work they judge.

## 2026-10-24 B2a.1 history views of every article and annex with a note (commit: B2a.1: history view of every CCP article and annex with a note, recorded as artigo-historico)
- Done: tools/capture_dr_history.mjs 0.5 walked the consolidated DL 18/2008 page in one headless Chrome session:
  index entry "Artigo 1.º", then one click on "Artigo seguinte" per article and one on "Ver alterações ao texto"
  per article that has it, at least 3 s between clicks (16:01:56–16:57:33 UTC, 588 views visited, 301 histories,
  0 failures); the walk ends at art. 476.º, so the nine annexes with history were opened by name from the index in
  the same session (16:59–17:00 UTC, 9 histories, 0 failures). tools/record_histories.py (ccp-record-histories-0.2)
  recorded the 310 pages with engine.sources.record_raw as raw:dr-consolidado:artigo-historico:<id>, working text by
  the new extractor dr-article-history@2 (= @1, but an annex's page, which has no "Artigo" line, is accepted).
- Report. Articles and annexes with at least one note on the consolidated page (counted from its text): 381 = 365
  code articles + 3 decree articles + 13 annexes. Histories in law/: 313 = 301 + 3 (arts. 20, 113, 136 from before) +
  9 annexes. Without history: 68, all added once and never changed (their only notes are one "Aditado" date); the
  DR shows no "Ver alterações" for them and the consolidated text is their one version (B2a.3). Versions per page
  (title lines, before rectifications are folded): 1: 1, 2: 146, 3: 77, 4: 49, 5: 17, 6: 16, 7: 4.
- Reads, disclosed: three earlier runs of the walk failed at the start (the first "Ver alterações" link of the page
  is the act's own, not an article's) and each loaded the consolidated page once more and opened the act's history
  view; the fourth run reused the Chrome tab the third left open, so nothing was loaded again after that. In all,
  this phase read the consolidated page 3 times besides the capture in law/ (which was not recaptured) and the act's
  history view 3 times; the index panel loaded twice (once scrolled to its end to list the annexes). Nothing was
  submitted. The DOM of each failure is kept outside the repo.
- Size: a history page is the full rendered DOM (~0.7 MB); the 310 pages add ~220 MB to law/raw_bytes.
- Registered: ferramenta:capture-dr-history@2, extract@3, record-histories@1.
- Next: B2a.2 structure the consolidated page into passages, register every act a note names, notes into vigencias.
- Why: the history view is where the DR keeps the text of every earlier version (D24); without it a vigencia has no
  version to start.
- Pages (captured_at, id, sha256, bytes):
```
2026-10-24T16:02:26Z  ccp-dl-art7            sha256 790b2eaf12fedba9538f08a863a5e466ba3284de916947bea9d4e9cb82cae80f  711290 bytes
2026-10-24T16:02:38Z  ccp-dl-art9            sha256 e31cf1adda657d1f7fe96a1baaf6aabbf440b42827f1ac9e22514bbf763d0c4f  708163 bytes
2026-10-24T16:02:49Z  ccp-dl-art11           sha256 0ae31fccf8d8842361f49c1c6c17ed88b096793de1a1eccf1c32d455d96f2692  707885 bytes
2026-10-24T16:03:21Z  ccp-art1               sha256 09696a1bfc62248e700a65eb9451c4dbc793540eccd67e38cf0e9eb533ad39a7  716371 bytes
2026-10-24T16:03:29Z  ccp-art1-a             sha256 da2cbe28dcb92014fd585b7826c1b9db2597172213463a0849811efe9e73ee8f  712827 bytes
2026-10-24T16:03:44Z  ccp-art2               sha256 644860bbbddb145fc899ad875572546a4c830b7d8a86b36d0b38d354d5158c7e  720844 bytes
2026-10-24T16:03:55Z  ccp-art4               sha256 017ab5f58a9e573fcfb5fe2d4c39ff12f4ede13f279cb5af5e73430cd72b6b22  723505 bytes
2026-10-24T16:04:03Z  ccp-art5               sha256 84ba1c51b3833664e4532725b1ce5ed1294281597cb0e3668176efbddb7138dc  747157 bytes
2026-10-24T16:04:11Z  ccp-art5-a             sha256 18e80f703dbbe749b14523fef4dd1ddac43bc30264ce6baf60755a1b27e9d423  717777 bytes
2026-10-24T16:04:18Z  ccp-art5-b             sha256 e91bfced394ec0dcf751bf3051a365d324cc42c751bd05f727f165ecdff1991f  707133 bytes
2026-10-24T16:04:26Z  ccp-art6               sha256 63e48446b54496daa5b265e790697f1668147e983645d64881f1b0c82cc9ac6f  707307 bytes
2026-10-24T16:04:34Z  ccp-art6-a             sha256 116b8d7eb45ac4bcf3a0bed4268520856ee77dc1b78f4c700b7c98600017c931  711656 bytes
2026-10-24T16:04:52Z  ccp-art9               sha256 77c1bcc82082641a6d29314f0136440277cef32735e7f1881bea553c15b5207c  710976 bytes
2026-10-24T16:05:00Z  ccp-art10              sha256 0b366239f10fb9b9a811a062338a74914edc031b0d660a8f795e5cf0ceab231e  708763 bytes
2026-10-24T16:05:07Z  ccp-art11              sha256 65b0a8122ec3be653ff3172c96d36d33dbf0d746102032a9609ddcc291d63982  714475 bytes
2026-10-24T16:05:15Z  ccp-art12              sha256 fbec1b0f30b6d5360823c48357118b8107ba42f7c500bd14b1542bbcbca35758  706570 bytes
2026-10-24T16:05:23Z  ccp-art13              sha256 9a0e4f12610bccff48b4dc8f92c07468da63d2f9251ed31d7fa22d7eedcb074a  728408 bytes
2026-10-24T16:05:30Z  ccp-art14              sha256 73477c310bc623991304a64bb8bf4e066898f4f4098a433713f4b47125bf630a  708091 bytes
2026-10-24T16:05:38Z  ccp-art15              sha256 65be7dc93d2089a69b4d1e0e49946164f8fc060a3eb8c269f1b4f6973cae9178  707277 bytes
2026-10-24T16:05:46Z  ccp-art16              sha256 5e5e3649a24df43cfcf1cb9601c0be819509f3a7b6826ebc7a6532f62f635740  709691 bytes
2026-10-24T16:05:53Z  ccp-art17              sha256 2d6c4035dfd87a362faa06292a167226aebfe585430cb0a5e53e5d8987e9e896  715195 bytes
2026-10-24T16:06:08Z  ccp-art18              sha256 15348882db22c04611b15c93a3bc067403d623ddc1694c4ec54bfeb83b1b43cd  707983 bytes
2026-10-24T16:06:16Z  ccp-art19              sha256 71ab98a17dc2626cf80fe852880b7a91938c7dc24d8f3a9fddcee627c123ec7e  711846 bytes
2026-10-24T16:06:27Z  ccp-art21              sha256 13e68044e13c852897130eb8669ffe44d2cea60638c39f1e4099855de56e2d97  714605 bytes
2026-10-24T16:06:35Z  ccp-art22              sha256 64f46267a88d5d5f900af5bb808d63080dea032a520435db70d0e95914bda57f  714824 bytes
2026-10-24T16:06:46Z  ccp-art24              sha256 d22ed497b5a252942bfa894b631376fdd7e759f491148a6cd7ad4c33fc582864  740643 bytes
2026-10-24T16:06:54Z  ccp-art25              sha256 d815e444ac02cc9a96a31d1f2e00abdb484c0fe4199743574e53cc31d0046aa2  720583 bytes
2026-10-24T16:07:01Z  ccp-art26              sha256 ad930027b24e83ea816ba4440b9e09ad4639d58cf5256dae41ff5a764758c306  726179 bytes
2026-10-24T16:07:09Z  ccp-art27              sha256 a78c2deb52f31766219480cb0c537a1ce4f9ad9aef427679b80d5567502075fe  742252 bytes
2026-10-24T16:07:17Z  ccp-art27-a            sha256 0fb5b8833d5050064060181abab4b29e7e1c3898da968210bab8d15f8c6ae5e0  707386 bytes
2026-10-24T16:07:28Z  ccp-art29              sha256 3cbc2a9c6c147066c14175caaec7f7193da25d9073723b1e40332ab2538e02db  720937 bytes
2026-10-24T16:07:36Z  ccp-art30              sha256 9cc721dfb8a0f8a74b79c0fe940e971474f74ab648d956d4fb88cef98de7f20c  707963 bytes
2026-10-24T16:07:43Z  ccp-art30-a            sha256 b94e133dc90d45db06c4a91c56b922e571cd8479473ac181a70e42ba7c663519  706942 bytes
2026-10-24T16:07:51Z  ccp-art31              sha256 4bc1d86ffa86a2bc130b78c243f9adb6841d44d46b1ec403ccc1a25deb16b34d  712356 bytes
2026-10-24T16:07:59Z  ccp-art32              sha256 a8a6e4cb71aab4c984f49908a9ce1f05b144fbbd978a83058d5ad584d16d22dc  720114 bytes
2026-10-24T16:08:06Z  ccp-art33              sha256 7dc9a33456a22130f64f9112b103ac4c263a262df6cdfb5d3d21ae83639990e1  711304 bytes
2026-10-24T16:08:14Z  ccp-art34              sha256 fa5fb726257773b253a1434c64afa2aa2d8dcd0160ad0c98307e26f13791085b  720610 bytes
2026-10-24T16:08:22Z  ccp-art35              sha256 d8cf9f99e75a8489f2ab585ce0decde1587946cc7a101f08567cc6b3e363105c  710167 bytes
2026-10-24T16:08:29Z  ccp-art35-a            sha256 48afe11f199fc13de21cdeed26458cdd7ce7d45db91d38eff5c27cb18b6f2e07  715173 bytes
2026-10-24T16:08:48Z  ccp-art36              sha256 0bd8d92910ea825888c11d9e6e7e6cedd619edb5d748a29c9465b16fb2cbd36a  714915 bytes
2026-10-24T16:08:55Z  ccp-art37              sha256 2525f996300f93ba619992bbc662e8af096d86834861c52d02f645690d03f6ff  710661 bytes
2026-10-24T16:09:07Z  ccp-art39              sha256 d8dc76815d378f48026950b27108a2e4507029d02a43a53b3f1f7f7dd03a46f2  718437 bytes
2026-10-24T16:09:14Z  ccp-art40              sha256 5159b745347cd3a490ba9d88652dd281db6376393e0e86039c0bbd6734beab8a  711509 bytes
2026-10-24T16:09:26Z  ccp-art42              sha256 4f097bd9c6a8db3eabf5aead2bf6c8c3b09049bbca4647d67a6d8941d80357e4  729508 bytes
2026-10-24T16:09:33Z  ccp-art43              sha256 1a350cb12e53e758be669934d70ed807a4cf80d9bee3bc0d31a64f28f6db52db  733840 bytes
2026-10-24T16:09:45Z  ccp-art44              sha256 5a0705d93965553b46e1e75bb9fb67b3fdb63d3faecf234e560b5a7a67d75bbf  708454 bytes
2026-10-24T16:09:56Z  ccp-art46              sha256 4dab504ff001cadcbffd4905093518be490e927673ba1ecdb50a936fa726fa7b  706871 bytes
2026-10-24T16:10:03Z  ccp-art46-a            sha256 2ccb5ac0b31588b97bbd1908d5e8fa37aa0e1ba8ec22fe454bbba32de336411e  709709 bytes
2026-10-24T16:10:11Z  ccp-art47              sha256 ca9033a935b2d097f3a16fff1c4f692cdd5ae993d577fc79c1d401a2223b9a29  711644 bytes
2026-10-24T16:10:22Z  ccp-art49              sha256 b36650f670e8908082c2578bce0f1358e3282a01a2ceddc99f6a091a8c6ae119  739211 bytes
2026-10-24T16:10:37Z  ccp-art50              sha256 d47021970b63d710ef76e71cc2a781751800b1003d21be84e133eec74bbac57c  717499 bytes
2026-10-24T16:10:48Z  ccp-art52              sha256 ebccecfda487ef6d146ecb964d6a624c2e8e4f723ba0192c2dfba0a9e836ef2a  705969 bytes
2026-10-24T16:11:03Z  ccp-art54-a            sha256 cbcb8d3d005f67e7e4b30052e96e7b416de1da2173d1c12abb003f5e10c73280  714734 bytes
2026-10-24T16:11:11Z  ccp-art55              sha256 d36fdb6363f0c85d8930720eac807aca526d33f39ba4fff5e9d75fbab52ffbd0  744939 bytes
2026-10-24T16:11:19Z  ccp-art55-a            sha256 c0f9c86df08d8b1a528972eddc163a1e1a3ac328e695deb16e3ec5689c488f4e  709110 bytes
2026-10-24T16:11:26Z  ccp-art56              sha256 9aee7aabe405de1054476c3099665caa7fca8213d5f5bc909e9b2686f5366fc4  707149 bytes
2026-10-24T16:11:34Z  ccp-art57              sha256 d12f8fdbbf1450fa1a8c362365d81b21337e5a43da1f2cdc9d445bf37ea59305  726150 bytes
2026-10-24T16:11:42Z  ccp-art57-a            sha256 ca499dc90d8d5a2abda988fce94f7e51d05afe5d27df3c7fd8affe8941d14061  708314 bytes
2026-10-24T16:11:49Z  ccp-art58              sha256 69cd62068604919529939660de3beb0fd6a0b70a45ce2eb994d84de45f11d71e  711248 bytes
2026-10-24T16:11:57Z  ccp-art59              sha256 6935bd615a80530c90e49f0a560b3a92785f880596676a5a9d78ee40b23d6818  714337 bytes
2026-10-24T16:12:05Z  ccp-art60              sha256 dcd3bacde8f707682744d8f534aa2f6cfc416fbe5e1a28eda0d95ef5712406dd  709943 bytes
2026-10-24T16:12:12Z  ccp-art61              sha256 c77fb188079f2536d2b291cb30e3c4029a8a3b56bc7b8a58874e1c7dff1b4067  716206 bytes
2026-10-24T16:12:20Z  ccp-art62              sha256 4c9eabc531db54a3e739e7fd8e751db80a9c3d0794de60bbb27a1f68c5cfe05e  710773 bytes
2026-10-24T16:12:35Z  ccp-art64              sha256 348a86ea2684647087088ce910e37ba8d53ad47956f2181c195659a275d11b29  715154 bytes
2026-10-24T16:12:46Z  ccp-art66              sha256 122201c45d792d68629f203bf68a0e9d714af83c191c708de4cf0f7f250db48b  708936 bytes
2026-10-24T16:12:54Z  ccp-art67              sha256 7c29221a5bd457e5134712c9e40a274a71a2e79c9cad28d7b00f36e1fd6feb1e  710136 bytes
2026-10-24T16:13:05Z  ccp-art69              sha256 4d8cc71ca1fcbea61f9449b69184017702c63a1fb6b4139bd77b0e1776c1e3ae  708657 bytes
2026-10-24T16:13:13Z  ccp-art70              sha256 32e2e390c85123b482ae85d35db3a1b2d3084b0b7ec8c1cf84bce310b3e232d6  733573 bytes
2026-10-24T16:13:20Z  ccp-art71              sha256 6cae519e9ce6a3ca880c7fbf09a73d8d1c49743fdcad64394d652134222ce207  717041 bytes
2026-10-24T16:13:28Z  ccp-art72              sha256 5ae23bab9ecaf5b8132a9580744d45b4fbae8285d3d576f037ee82979afd5e6e  715331 bytes
2026-10-24T16:13:36Z  ccp-art73              sha256 c19bdf70594eb82145967c7cad386c80a16f7d4723686d28178434665206adce  706188 bytes
2026-10-24T16:13:43Z  ccp-art74              sha256 ea34119beef90a00b88d3444a5e616864321a55bf4109224ac9a696f7301550c  714514 bytes
2026-10-24T16:13:51Z  ccp-art75              sha256 a0a4a7e95cc00bfe480c16cc1d415187d806d4e198b72714b5f999659e3e7c63  731364 bytes
2026-10-24T16:13:59Z  ccp-art76              sha256 eb27fd9d9884b6f83c286a38324c29af0a31002e4bd58fee03a6b256c7842fcd  707055 bytes
2026-10-24T16:14:06Z  ccp-art77              sha256 e697ce6db00a669138d0b406ce4ce3e512e445783e71df6bf6f19b1790e56d2d  712695 bytes
2026-10-24T16:14:14Z  ccp-art78              sha256 171dc4f0e5124f2ebbf880e490a62ef4ff3c0bf699f432c723671043bd6d3398  721805 bytes
2026-10-24T16:14:22Z  ccp-art78-a            sha256 c9a71b73c4a2f2f1c65cd840d4ba952a6ee42cc0e5cb8789813e4446eb558086  709998 bytes
2026-10-24T16:14:30Z  ccp-art79              sha256 44990e926b604f40415a26e783e06158fbb2591c77e6c8ae60969eb07aefb221  715308 bytes
2026-10-24T16:14:37Z  ccp-art80              sha256 47f38ed2e5b58b71a3ce5c663ba617b67163d7b2735b95ba224ea7b99d474ffb  705950 bytes
2026-10-24T16:14:48Z  ccp-art81              sha256 f2ea51086140b02becd864ab220bc1915e5be58ed72c5499ac7d1679c42f3e89  723503 bytes
2026-10-24T16:14:56Z  ccp-art82              sha256 fcfc187831c1c0fc56d4c26cd36f2a9132f552d0c6bd98868a65b50eaf8f06e3  706929 bytes
2026-10-24T16:15:04Z  ccp-art83              sha256 7c0426b9bcd796b3fa8c0df0d967d957319125f93078260719a9778a5575321c  711531 bytes
2026-10-24T16:15:12Z  ccp-art83-a            sha256 8aaafc515906908367af23e5016408e94dafef20c3046196b203b21603136b23  711335 bytes
2026-10-24T16:15:19Z  ccp-art84              sha256 61c9f81b05927f09238b9dc4464801d00f254aca1512a33e07dc0f6eb55205dd  707824 bytes
2026-10-24T16:15:27Z  ccp-art85              sha256 a05b718bf6fcd7d5fd4a9a4eca34e4a5185f35aba62085f4c6f69594f255e924  708910 bytes
2026-10-24T16:15:35Z  ccp-art86              sha256 18ea7357299edb68f4aeb35ad05a2abc61b3ca8feabb4e52b4b47e11b8ab4f58  720937 bytes
2026-10-24T16:15:46Z  ccp-art87-a            sha256 7582adf6a1a32829bb6bb5455e83e2d3ca6dc34505700f27b18d2026ab28d2b7  708252 bytes
2026-10-24T16:15:53Z  ccp-art88              sha256 209129c7e3632ccaaf33e08f99251472a290b8105f0c03426aa5ca21822dbbf9  714643 bytes
2026-10-24T16:16:01Z  ccp-art89              sha256 e5cd8455f96cb6e1876c2b1890c6784748f6d6525fa5eafa730956d666b11f08  713115 bytes
2026-10-24T16:16:12Z  ccp-art91              sha256 169c035772b463b4dc98969ac02d399e5b07b0924b0ac90cd69f525c1d025ffb  709514 bytes
2026-10-24T16:16:24Z  ccp-art93              sha256 649bb2d9b4a2eba14b9a4398978160c755ac5a8fac37d67c245e7cabb3f6b90c  706394 bytes
2026-10-24T16:16:31Z  ccp-art94              sha256 2cad31cd5394247abb048b1b263ac21f3142eae94fbbd8cb9a5e7845ae3995c7  706465 bytes
2026-10-24T16:16:39Z  ccp-art95              sha256 fb15a1aafae04438dc4097a4acf6771b6758910a69c9c194bf3102f2b16a18a7  715800 bytes
2026-10-24T16:16:47Z  ccp-art96              sha256 980964aca39142eaf0621af49a9791658010254907de013005039b0912034b56  716106 bytes
2026-10-24T16:16:58Z  ccp-art98              sha256 273236b086ce176c4b671eb514ad85ad7ea54e8f41f2d478b5beda141a1f2177  709297 bytes
2026-10-24T16:17:06Z  ccp-art99              sha256 bb45803ce8599445f1d6c285d8e3a71622014361e09844a1867c75618dd83886  707344 bytes
2026-10-24T16:17:13Z  ccp-art100             sha256 1f7c9161e34ef5c0c5fb8eacd43b8a67b28f557c23bedac0b02ca04576af3500  706180 bytes
2026-10-24T16:17:21Z  ccp-art101             sha256 afedd852c0eebd79e5b44348c8079c27009335e136468a55ac87511d55b872cf  706006 bytes
2026-10-24T16:17:29Z  ccp-art102             sha256 dae0792841e9d0bd17dc9bc1f29bfeeff46a7ab6bea530c646bfb63a738df7df  707053 bytes
2026-10-24T16:17:40Z  ccp-art104             sha256 498d5e84aa2fa2b71c407785c3770141e20eaa09e8dd88d43e8637a1362cd97f  714522 bytes
2026-10-24T16:17:48Z  ccp-art105             sha256 3a3e9585581618f054f2a9e2f667ac168692f4c370b73a7e179f7da03b5865c7  708113 bytes
2026-10-24T16:17:55Z  ccp-art106             sha256 d31718cb0dcda59784b9c5b34bbdebcb8d7a3f67322ebe60d0003cfcc732e462  707674 bytes
2026-10-24T16:18:07Z  ccp-art108             sha256 1d6e8a72f04060084c94cdbe08fa416b04cc07ca916aae569c48557eddd134f3  706994 bytes
2026-10-24T16:18:14Z  ccp-art109             sha256 6965efeb3ea917d06439f3880ab88c6e620934c33bf79e1072f56c05aaa3e054  709753 bytes
2026-10-24T16:18:29Z  ccp-art112             sha256 1e53f9b0d2e9356c7777e3658ec8d51cbceeaad93dcc797d06569330083dd01b  706077 bytes
2026-10-24T16:18:40Z  ccp-art114             sha256 f29482bfd762bb5d62776c8cf6d41c4976a05c56d225b65224bbdffbc504fe72  713134 bytes
2026-10-24T16:18:48Z  ccp-art115             sha256 e013c7b742fafd22e623b3fa34eeac8b8eca90da24cde6d8e118d020acf231a3  723731 bytes
2026-10-24T16:18:56Z  ccp-art116             sha256 2c3d3cab44dc43f9be1653f6745e7931d88484a6d85af56bf330c0301c886a45  705993 bytes
2026-10-24T16:19:03Z  ccp-art117             sha256 30c464b641e288728c20d43ad0a841bfa86e47ddf8e9c4136b2b90284e89c585  707771 bytes
2026-10-24T16:19:11Z  ccp-art118             sha256 286111f75368179606ba1f27ef99b504fbeca5df0a1158bb37840ec4118a7e62  711019 bytes
2026-10-24T16:19:29Z  ccp-art122             sha256 352eaaa3a27600287cacf5f7f2a15e75c7e8dce3fd0a8f6f5b69088335331638  709325 bytes
2026-10-24T16:19:37Z  ccp-art123             sha256 7c67bed578784ae8843ee8baa3540ec1a06ce879533fdde780f2cb8897d16cf4  707827 bytes
2026-10-24T16:19:45Z  ccp-art124             sha256 8284432a8d29859f9f09fcd499fa68449c5dfb0bec4c9a7681703d36b918c374  707696 bytes
2026-10-24T16:19:56Z  ccp-art126             sha256 feab4db75c5f6e42a097c423b15c6026740c0e062203a0b263563b2d8ed138d8  707569 bytes
2026-10-24T16:20:04Z  ccp-art127             sha256 97301305ade1aecf030e3b685f72595429c004d27a5f78cd62e505d136b80fa8  713045 bytes
2026-10-24T16:20:22Z  ccp-art128             sha256 8c78b1a0c1f930646796172a94c32eb734293329d85bcd810bc2e710904e2dc6  715765 bytes
2026-10-24T16:20:30Z  ccp-art129             sha256 bfc5baa01e0b426597bf0edcbe3468ae2358f06f5ce241d4556940eb6ae98f5b  706341 bytes
2026-10-24T16:20:45Z  ccp-art131             sha256 9886105d4975e80f16a36a84f54c4a319441220a7e0010ede3b0d085279aaa4b  717789 bytes
2026-10-24T16:20:52Z  ccp-art132             sha256 f6a1caed8be033fdbeb6aed9b354e912e772bfdb95e69cfb0af33afc4a8f5fb9  731441 bytes
2026-10-24T16:21:00Z  ccp-art133             sha256 b36664231c96c9a9a548e56186a3a05bdef11b88418316be6772c8127037906d  714441 bytes
2026-10-24T16:21:08Z  ccp-art134             sha256 f77895feddc2911eb81880caecc001d0d46435d34e717a3353a4e8b17dbb52ab  707358 bytes
2026-10-24T16:21:15Z  ccp-art135             sha256 0ae90afce79a384a2ecbc940e15d5e07879ec0ddcbd2bf40846945e68ccd20c1  706798 bytes
2026-10-24T16:21:34Z  ccp-art139             sha256 ed03bd0e819060ba2d3618f6216217607e27089a3349b39989ec5490064f2987  711159 bytes
2026-10-24T16:21:41Z  ccp-art140             sha256 c2520f47ec8fad900ddf3fe103637852cb1ae2e2f870d8cf4889c1ad94c4ead3  707302 bytes
2026-10-24T16:22:03Z  ccp-art145             sha256 3b5b3a48405ca9bb342d506331a8a5aa8d7f031be0e85b723f37f361d7a274fa  706555 bytes
2026-10-24T16:22:11Z  ccp-art146             sha256 e3a6ac6168e02ed432f25912bd39a8f87214aa12c1dba809f32ef8dce9f62604  730960 bytes
2026-10-24T16:22:18Z  ccp-art147             sha256 cb9cdccf137f7a05aa6fea318ab6f38374a043f58e0c9e61b577007197ce8c2b  707613 bytes
2026-10-24T16:22:26Z  ccp-art148             sha256 43c1db712a768c959d6c801044028f2eb13ad43cb795144c13d3f9d7b201f9c6  707971 bytes
2026-10-24T16:22:34Z  ccp-art149             sha256 20496d87de3a5f27c0d17d819ce4b371c691b78a2d557136dee23981dcb5eecd  708947 bytes
2026-10-24T16:22:45Z  ccp-art151             sha256 deefd98f9496099f86b27091fe11cadc128d4d538f99ea05a9d474874fa4dcdc  705855 bytes
2026-10-24T16:22:53Z  ccp-art152             sha256 92f609ec07c85ef129079cac96460215a6d0b5d010d543b022a0a9e5e09229df  707760 bytes
2026-10-24T16:23:07Z  ccp-art155             sha256 ecc9cb950a8a78672857aa6dd399619f497bcfbf53e53a3f40122ddc7890891d  708745 bytes
2026-10-24T16:23:15Z  ccp-art156             sha256 7b5feb7725dacac46a9faa623f438d48ddb98bfef638c1238f6999b438762ddd  706323 bytes
2026-10-24T16:23:23Z  ccp-art157             sha256 7117145fdc55609c006969197e30c5af9218cb69d19a38ef4b4d4f5fe75aa397  706165 bytes
2026-10-24T16:23:30Z  ccp-art158             sha256 5d9bfe391bf1021a1982423977c22f287ce3bc1ed0183fbbf26b58b9e7fe4b49  705914 bytes
2026-10-24T16:23:42Z  ccp-art160             sha256 c220979935d0fbbb4f80f44590136999dab8a672ac209978c7e67877606f7617  707540 bytes
2026-10-24T16:24:18Z  ccp-art164             sha256 1e7245116192523f19c029fcabf61055d4fb35f7d0d2318b3e4a8d80f364fb91  738167 bytes
2026-10-24T16:24:25Z  ccp-art165             sha256 6cda89f9b50592fed725c71cd6b52bfa2f9f4d37b371012b3279afd669e982de  713941 bytes
2026-10-24T16:24:44Z  ccp-art168             sha256 d0302aa35507a2b41dd10b5a7d2ca2bbee645aaea7a690047e1dd2fb4dd6075a  711936 bytes
2026-10-24T16:24:52Z  ccp-art169             sha256 43e1c7ab031e789afc03866ee198b43b7f92244f7fa9ed37de828a3b5400a82c  706744 bytes
2026-10-24T16:25:10Z  ccp-art173             sha256 56b2b3a91105d83926e654d346656da78f36fbc97898b54a704a479ce57ebdab  706296 bytes
2026-10-24T16:25:18Z  ccp-art174             sha256 7120bedb83e6660e9abdf370292ba226ab61c454a54398be5981437ff167e0f8  710648 bytes
2026-10-24T16:25:43Z  ccp-art179             sha256 d2eaccdf08846a0da0b1f65c1301f5b69186925f0a7e1487032c043ac38510e0  707703 bytes
2026-10-24T16:25:51Z  ccp-art180             sha256 28d74018ca1dfa1da1be46255e4f7932329cbff68a16e1a685bbc51ed55a8a5e  709206 bytes
2026-10-24T16:25:59Z  ccp-art181             sha256 dc8d5512f6a40e32f966ea900785124996d0beeee88dedcc89306a9eb68ee473  707467 bytes
2026-10-24T16:26:06Z  ccp-art182             sha256 715abe93931cbe237628d8fc3738cf6d670dfd95ce5fd5a559358b94867ce6c8  707138 bytes
2026-10-24T16:26:17Z  ccp-art184             sha256 d5d36daf9c0aea56a7938c2cb8794c69e70fa103c2aee0bae94a5ad71987df7d  714952 bytes
2026-10-24T16:26:29Z  ccp-art186             sha256 3678922c58f2d74d6252b3763b4893103df87e855a195f6d728a2d5dbc432210  707723 bytes
2026-10-24T16:26:36Z  ccp-art187             sha256 fac80a8dcba83eae6914a9d733ec6d47c5619837cdca6eef0ea90f42b700e6d1  710464 bytes
2026-10-24T16:26:44Z  ccp-art188             sha256 ede59a6f7db39af3a0e3b3416f94e4371310b7c9c3125977bf9108ef6cfd25b6  709186 bytes
2026-10-24T16:26:52Z  ccp-art189             sha256 f53c79829133f5ed76cb5498ba44fb980e29bb3417b9a272e92460f7e645b012  713499 bytes
2026-10-24T16:26:59Z  ccp-art190             sha256 d84df614c1ccef22f54d68a350852f3a220e4c758be6f26454c98902989d6d45  706822 bytes
2026-10-24T16:27:07Z  ccp-art191             sha256 66f318030de7e98fed16adbcc0df4da5ff09e2305063b2c752643c93a4aea2fd  712276 bytes
2026-10-24T16:27:29Z  ccp-art196             sha256 c80e73988b2b627266f59b57aadb13623284895f63594689d3e077797636f8a8  708701 bytes
2026-10-24T16:27:37Z  ccp-art197             sha256 0acf5b1c04633eb38b7b02cd1173168f1ea2c4b1e378386e2013008953000a10  708383 bytes
2026-10-24T16:27:44Z  ccp-art198             sha256 fb03a5ccbc4c7bf83a08c3cc846d15831c723f4da5970a218257730ba1b363fd  707156 bytes
2026-10-24T16:28:06Z  ccp-art203             sha256 2962cb91dcad130f3580a54727fb70c2971dc054a962146aa32e72ae774377d1  705742 bytes
2026-10-24T16:28:21Z  ccp-art206             sha256 40d39892adeca8d5d1782baefa796a4fe2370862b580989da4c3e3218d48af75  707402 bytes
2026-10-24T16:28:32Z  ccp-art208             sha256 471b7ef90f31eabaaadd85c3661ed16de8b33cec2fee3a833b29727f9044359f  709190 bytes
2026-10-24T16:29:09Z  ccp-art217             sha256 ada7704cfaf6577ffc417d21d457d976823d84d2962db433a367e514101e0fb3  706826 bytes
2026-10-24T16:29:16Z  ccp-art218             sha256 75d7660278f4a8208b336efb0663800133adb2903e7787623e33ddb769e75e8e  705774 bytes
2026-10-24T16:29:38Z  ccp-art219             sha256 0f3f4557967d9cb0524de59953079c9831b388e8bb17994f3de183bcfd5eba73  709494 bytes
2026-10-24T16:29:53Z  ccp-art219-c           sha256 6557b804ee6409a03448ece5080af2d8ea62a2223c5766cbd0bb3240add07329  709109 bytes
2026-10-24T16:30:19Z  ccp-art219-i           sha256 6fccbe11a7f78e1d47cd38c1891ae00acfa56365de2f9e371ebd9072036f77e3  712014 bytes
2026-10-24T16:30:30Z  ccp-art220             sha256 921ba76eb504584aaa90bd9f843bffd6f6e65764cf8743662452fa0705c48641  707259 bytes
2026-10-24T16:30:38Z  ccp-art221             sha256 bd4b63168162346d76fdf49c04af5964e80a27dec9ac19eccc5e19e2c0504b9a  707205 bytes
2026-10-24T16:30:46Z  ccp-art222             sha256 4eb383f705039f280954b9a154ccc36d18664142e3d25342feacbf7486523979  706916 bytes
2026-10-24T16:30:53Z  ccp-art223             sha256 9e636b99642b725068b60b1e3124b2b45c1c9ea32b0ba1782f9bd443c3705d8f  706810 bytes
2026-10-24T16:31:01Z  ccp-art224             sha256 38578d1fcf2e8e4ca0c570cbcefb082a15ebae4c1c50fe2de807d10adf5eafa4  707145 bytes
2026-10-24T16:31:09Z  ccp-art225             sha256 73fca13923d60b3f590996b818eb7d92abe5b957c043ca233db7b49b0765c6cd  710477 bytes
2026-10-24T16:31:17Z  ccp-art226             sha256 b6b4a70fcf826a1ae824528331222aed5e2b27e6b00b20b2bcfd5adf618aec2b  710224 bytes
2026-10-24T16:31:24Z  ccp-art227             sha256 189c9bc192a21fc3573fcba9960aac6fb6945bd9570c0e5160ed92fc94cdc257  710104 bytes
2026-10-24T16:31:32Z  ccp-art228             sha256 c85513723738201ffd4b40dbde6781278958de9e21c7533217693143737517fb  707108 bytes
2026-10-24T16:31:40Z  ccp-art229             sha256 6e0885d4e77e0fccb16407f58dc72c2ca5a488ab1634225a87e185c165d22354  706698 bytes
2026-10-24T16:31:47Z  ccp-art230             sha256 7482a330d17742545349123cc76feca0c3ce7f1fb6bff6ba6da5525774daf7ac  707129 bytes
2026-10-24T16:31:55Z  ccp-art231             sha256 1926839bad6eb539c8854fa3804a90f2e11bff220eb509bfa6b5c804f6a5038c  714672 bytes
2026-10-24T16:32:03Z  ccp-art232             sha256 aab38f1e1bc503ad03b12aa77de95b8dabfdce1507ed76402888a257297d4d7a  708768 bytes
2026-10-24T16:32:10Z  ccp-art233             sha256 869f874491895267765f2b6dff29b47b57718244ca5670a884b3a091b0f1e226  707536 bytes
2026-10-24T16:32:18Z  ccp-art234             sha256 a59b350ab96c901867d303d4977c559f1635d4a7befc39f4352d8aeecd4ba718  707255 bytes
2026-10-24T16:32:26Z  ccp-art235             sha256 1ee2989bd00903a03f58f24dd1895326c6ef4456e7bfca67431ba35d414995ef  707129 bytes
2026-10-24T16:32:33Z  ccp-art236             sha256 874549cc5df2408a742fe8e28a689266deeadf9bb9b728235fff549ae0dde7fe  706779 bytes
2026-10-24T16:32:41Z  ccp-art237             sha256 dd566baf12daa994652499d563b141c46a558a529fb8a3959a64bc280ff25684  707675 bytes
2026-10-24T16:32:49Z  ccp-art238             sha256 c2b1d5b123d3768dc7bc55a46f76a8a7fcfdc16c9cef8344c7381b4628ee64ce  706077 bytes
2026-10-24T16:32:56Z  ccp-art239             sha256 1aec15c388c30d59c6e4a17bde95fbd26339c0946d59a6b10f815c2e087bafaa  707605 bytes
2026-10-24T16:33:04Z  ccp-art240             sha256 0182fccad26b8a64161a81b212fafee391a144510ca0ebc326209bd8569da3d1  707642 bytes
2026-10-24T16:33:12Z  ccp-art241             sha256 f457dce27c424d508b4f71b4cac69e44845748d718d37904ba6ebdf429964467  707765 bytes
2026-10-24T16:33:34Z  ccp-art242             sha256 356b680f6b079bf45a17174be1f39b321984f3eac528ca15da696bdd8d9b8b2a  711318 bytes
2026-10-24T16:33:41Z  ccp-art243             sha256 881eeb6d0dc84eb1776ba867cd07e8c8708a5986f9731489de9d2ede399e4e23  707164 bytes
2026-10-24T16:33:49Z  ccp-art244             sha256 5b1303111505331f2a9621a7fdfd458d08109dfc287e1b034cf956006f212d57  709013 bytes
2026-10-24T16:33:57Z  ccp-art245             sha256 884cf7a0b84438170bc2e5371cd10fcf5eaea5ed4cb5048158d731db907b74c5  712353 bytes
2026-10-24T16:34:22Z  ccp-art250-a           sha256 8ae055ff1f884194e8056345cb015c755873efc91c0fd60b070e7a618b8bd585  708912 bytes
2026-10-24T16:34:30Z  ccp-art250-b           sha256 b34c189a232ccb055137f4f4dc80f8edc2465c8e7349c77637b05f131fa248f3  715492 bytes
2026-10-24T16:34:38Z  ccp-art250-c           sha256 891899778d4c84e7ac826cb3b73bb161bbd670147bb8300a5868175cacc01e39  708584 bytes
2026-10-24T16:34:45Z  ccp-art250-d           sha256 6d1ac36461cbd37e87fbd27a04d56a8def3accdf73019bbc24991ec6c154eae4  710723 bytes
2026-10-24T16:34:57Z  ccp-art252             sha256 9bf9ba989ac69924198b1a88bbd81fac5075a080912879f9376e8a6dedb4d940  707133 bytes
2026-10-24T16:35:04Z  ccp-art253             sha256 07dcb80041cb1c6b3d30c3921695c8c4e76fd01f0405c8ac5ca5b00d43ffa50f  708024 bytes
2026-10-24T16:35:19Z  ccp-art256             sha256 c38bdb8c8b278176141f468f128566348db5ad28a7cacd70cb36174efeff7557  706900 bytes
2026-10-24T16:35:27Z  ccp-art256-a           sha256 29d4392906c3d3b89b305bbcb2b1f269b09efb94017fd03f798f00b119cdb8d0  720244 bytes
2026-10-24T16:35:35Z  ccp-art257             sha256 0375cc70e6867d318962b537cee9ce698dce8d3f56856f86b09c7b6c3dc6e021  708931 bytes
2026-10-24T16:35:42Z  ccp-art258             sha256 e309d63e655e0ad6218bd8e983fbea1a463375347cd3810b1babc4569b18432b  707036 bytes
2026-10-24T16:35:50Z  ccp-art259             sha256 ac70d4eb94379bab8d3890d518fffd1973e2b6db6c3d47adf8ff582feba9aefc  709043 bytes
2026-10-24T16:35:58Z  ccp-art260             sha256 2ab1ab4c7983bf2c340e4a20fe42d3fb69b8d456a00ed1218fabc3204cca5552  706965 bytes
2026-10-24T16:36:05Z  ccp-art261             sha256 f1fe965bcb7d5689ced2aac2d5873cf27227d1597316135581a2e4e4034d647b  707807 bytes
2026-10-24T16:36:41Z  ccp-art267             sha256 bad81ad2ea107c13edd2807f8009b3c85b0a01dbcf417e6cd93594f43e6c8aa5  706290 bytes
2026-10-24T16:37:14Z  ccp-art275             sha256 ba3d79f2a6f28c1ca930122f8f6f694d424eec80390ce66721d5352404c0b32f  722438 bytes
2026-10-24T16:37:22Z  ccp-art276             sha256 6d9a9bfc3255537c761cdeff0aa33283f53c1caac22b504dfa943fef8c3606e1  724762 bytes
2026-10-24T16:37:30Z  ccp-art277             sha256 1cb56a2f562847f189183ba954ba026ecb3c765cefb982e0425d1fa9eeb788c5  707319 bytes
2026-10-24T16:37:44Z  ccp-art280             sha256 f50b7dbc952329b185bcd2bb988241c5d6fdef65a7f12042d6110e8600e29042  723415 bytes
2026-10-24T16:37:59Z  ccp-art283             sha256 4fd9d36e5ed40f600bf93ff8c4d45c1a3ac8db87787d25b7895d480de463653d  709886 bytes
2026-10-24T16:38:07Z  ccp-art283-a           sha256 14dc894a08224f2b3662e88eb299780b45e1285248be0328a6529d3898ca2a47  717739 bytes
2026-10-24T16:38:15Z  ccp-art284             sha256 a76719b45b1e746d23ded4fb45da3cda0ed7b17648a430e5919d0257bf92f45c  708956 bytes
2026-10-24T16:38:22Z  ccp-art285             sha256 8cf3537d4b573942baaa21f6766b6d4a692e9e1e477d7ec933eea854a51caa75  712155 bytes
2026-10-24T16:38:33Z  ccp-art287             sha256 98d59ad2fde5bca17d02a783d5e25902bd76ba81aa72b73f39c6ff0574abae0f  715849 bytes
2026-10-24T16:38:45Z  ccp-art289             sha256 1a18c7df50fc9f4731b0285b8b9f1a2195b457b71fbe5fb384685a46c73e44a3  705906 bytes
2026-10-24T16:38:56Z  ccp-art290-a           sha256 eb3e1e47979a40100a3a3617b5cd769b765b291cfebf0d1dba8757a6b48bd344  711807 bytes
2026-10-24T16:39:18Z  ccp-art295             sha256 db63afcc62a54da9a569cdd0e17ab02b59d885a57d0e6f4668e17a89c582f510  723872 bytes
2026-10-24T16:39:36Z  ccp-art299             sha256 bb27b358856167e419978ba542b8523870271e07859ff9ee3010e181d5da56dc  707212 bytes
2026-10-24T16:39:51Z  ccp-art300             sha256 94ce54b40970a8d8b7d3c63b5a2c4cbf99aa456db7bb816cdbfa56c3d7ea9863  705822 bytes
2026-10-24T16:40:06Z  ccp-art302             sha256 259ba930171cda671d750d8107e831aba46216091e74b78f2013146efb29db42  708854 bytes
2026-10-24T16:40:28Z  ccp-art307             sha256 f777026ca71bba756d6403824c6bcbb68c19b428aae3a371855f60893efb6ab9  707332 bytes
2026-10-24T16:40:46Z  ccp-art311             sha256 cf5ab88cce0d392b94ee8b7e0aac0d821e57781410092516e5f17dd03d432e42  708314 bytes
2026-10-24T16:40:54Z  ccp-art312             sha256 8f4fc9628c0d1b7735234bc1cf0dc4af13676dd1837acea26203a8412364a3b3  712577 bytes
2026-10-24T16:41:02Z  ccp-art313             sha256 f28ef9b0378d6bbc33eeb83b16f44f03a85eee104b49cff423f056cec20c4b22  721692 bytes
2026-10-24T16:41:09Z  ccp-art314             sha256 edba92e3f5dc41a2b460bd527741b6c0c86c6295a8d762fa8d4fafdbdec4579a  711313 bytes
2026-10-24T16:41:24Z  ccp-art315             sha256 71e2e14f5df7758bf3d2cfe1916460747316144a3a1e5a18bd6466afa50de234  711699 bytes
2026-10-24T16:41:32Z  ccp-art316             sha256 d4807752cd7a97adf231024a72753555a2ae5c332fa740723666dac0e1e2a5be  705795 bytes
2026-10-24T16:41:43Z  ccp-art318             sha256 ecc3f19498ef651e3babb0e60ef20a9522f05662e2e06bc42ac4de476a099bbe  717620 bytes
2026-10-24T16:41:51Z  ccp-art318-a           sha256 cb0ce254dd94eb1887dfe40aa2048356a1d9a28298d00dab05abaa3fa28a8c22  717691 bytes
2026-10-24T16:41:59Z  ccp-art319             sha256 c0cac02ec783cc2d0c78bf96447b289cc2949560240dd52da65b885b48ce62ba  709865 bytes
2026-10-24T16:42:17Z  ccp-art321-a           sha256 08983bc57fc7d8afdb0243b80730686a3a7c8c44fd2362766a8845106452952d  711712 bytes
2026-10-24T16:42:28Z  ccp-art323             sha256 559b8d108f1077708bb8db7823ba534bdac245ab81928dda9c8960aaf03bdd47  706222 bytes
2026-10-24T16:42:43Z  ccp-art326             sha256 261cef35fca44874e5502da5e42bd4986c775fdeeb433e98628e1d611792e7c8  707569 bytes
2026-10-24T16:42:51Z  ccp-art327             sha256 1a72d22dd965b0c1ad0f442d9b8b96061ee883685dc465b3cecf6b138fc72006  708262 bytes
2026-10-24T16:43:02Z  ccp-art329             sha256 01ba5956fc508eceb080f4c09238d41fb902adfef51f032e90c80b8b32f19682  709975 bytes
2026-10-24T16:43:20Z  ccp-art333             sha256 f21a70da45b6fc2e53023d83408a48c6dbc0149c1b84a7bb0e78a84423f98860  709291 bytes
2026-10-24T16:43:32Z  ccp-art335             sha256 a15a74bc4ddce4465c77df845bb006bd13e3719e9076c04d979d06a28b295dee  708652 bytes
2026-10-24T16:43:46Z  ccp-art338             sha256 a5529b4bfcdae4390ab44250a3463b87891fda9a7d1509bc4f68a8b621466485  706530 bytes
2026-10-24T16:43:58Z  ccp-art340             sha256 7e7467e007898e278bf3d2e00eecae05ca18f6a4b59af9a90728352f8e3c921c  709984 bytes
2026-10-24T16:44:16Z  ccp-art344             sha256 1830dc4a2db2227899ca4f461f9db752f36311ad4cc894b52359e638eaa0c901  707492 bytes
2026-10-24T16:44:34Z  ccp-art348             sha256 230cc6a985149ecfb6b57e4862137745ff930e52c85f9cac4161e130c2617dc0  710245 bytes
2026-10-24T16:45:00Z  ccp-art354             sha256 6b48cdd1c5ae03e3544e29092965adf4219b00fb56568cab9709f9f635af2ee7  707547 bytes
2026-10-24T16:45:15Z  ccp-art357             sha256 b55dda27e818aecb5b6207ecf8e74b7be5b70a85be9611760b02013c9d920d80  706052 bytes
2026-10-24T16:45:22Z  ccp-art358             sha256 d691948c7bbab03e655d430035d4a90d1da79baea5a4327e3ec7c22a993ea0a7  709320 bytes
2026-10-24T16:45:37Z  ccp-art361             sha256 57f343565c5d5a7073bde39abb9fe9417d6d8d8c937701275ee6c497bcc10976  711642 bytes
2026-10-24T16:45:44Z  ccp-art361-a           sha256 3528a157aac5048b7e9cb2ca10d0dcc53a9aba9477f00b7f784b3444c2f38fc6  708165 bytes
2026-10-24T16:46:21Z  ccp-art370             sha256 cb99b4136c06b07b5b3633c221463dc78c5cb4a3167e619b035533cadd528f08  723242 bytes
2026-10-24T16:46:32Z  ccp-art371             sha256 ae65f6597a441a89768044906bbe6badad0c0c4315f41dbe70fa74cc3e96f8ff  710091 bytes
2026-10-24T16:46:40Z  ccp-art372             sha256 79f4c9223366d51e2cfabdd250a04cf982ddc047239e06e286d46bb1bb8e824e  714509 bytes
2026-10-24T16:46:47Z  ccp-art373             sha256 4ec0a30b39c5d4dcc3b94ddf5b4c99cfc4c6300e58e68aad8ecfa0ab97aa0df7  716477 bytes
2026-10-24T16:46:55Z  ccp-art374             sha256 ffd69b9b45c9009d10b5ce3a5432350f4faaed3f218a141534740f36273b4f4c  706221 bytes
2026-10-24T16:47:03Z  ccp-art375             sha256 b20a15212e2e7cf3e2b8364c93669d4d65ec0f483e6191cc633eb8a53bd0b19e  706453 bytes
2026-10-24T16:47:10Z  ccp-art376             sha256 6c246ffefec4bc54c4d8b9918a57523c1a9e06deee96c5ad582a0f2fe3317daf  717594 bytes
2026-10-24T16:47:18Z  ccp-art377             sha256 c02a8454df4385943e6a3f3611fedf89d6fae2d8311b98c9702b0971620cb472  710138 bytes
2026-10-24T16:47:26Z  ccp-art378             sha256 af21061ac12dc948dc0ca5f45ee02df9e11dca7fae4bac907bb800e3d334a9c7  717650 bytes
2026-10-24T16:47:37Z  ccp-art380             sha256 e795ee669465779c0bc1b7750e28810b3a9286c70a1c95b334b77db4dc0b8ee2  706339 bytes
2026-10-24T16:47:45Z  ccp-art381             sha256 a19e7ec6ad5749382a2d963046253264bd3183842ae9d6dd10a6260d27b50ad4  710280 bytes
2026-10-24T16:47:56Z  ccp-art383             sha256 bcc4076c446b5df5870f4990e3fe6a325cd13dda97589e9d3d105e1d9b6094bc  708129 bytes
2026-10-24T16:48:04Z  ccp-art384             sha256 3376c55476d0d6c3b466d1df3f4e6511ca319959f82598a5d9c5d1788d90ce52  707607 bytes
2026-10-24T16:48:11Z  ccp-art385             sha256 624e3419c6872109858e3fe638c3a54486d8cbe1efb74c881e3b54d8c6227464  710428 bytes
2026-10-24T16:48:55Z  ccp-art394             sha256 63344f71cca670b4efa6ddb436e078654195cae345ce94f61a43d62b3b481e72  709397 bytes
2026-10-24T16:49:09Z  ccp-art397             sha256 da4279a4787c85c428cbb759f4859b58230092af078ddf0d48dbb538604b0ec3  709559 bytes
2026-10-24T16:49:35Z  ccp-art403             sha256 5318babc031ed97d5460d24b0470bdebc895f04d0769b73e44d2229b2dc935ce  707089 bytes
2026-10-24T16:49:46Z  ccp-art405             sha256 fc46e7368ab4e3073ece153c5ab08b39d345af86b8107886f8f35fa81286df0a  714906 bytes
2026-10-24T16:49:58Z  ccp-art407             sha256 da726e2fe11fbaf2689adf70d2f0d31517ed56b02e967b924b5194fdefea85a0  706962 bytes
2026-10-24T16:50:12Z  ccp-art409             sha256 6f3f4fbe96c4101c46d3b541525cfdd86a0d734a0a0f6e66418637cc78083771  706837 bytes
2026-10-24T16:50:20Z  ccp-art410             sha256 cdafce877ea7428a729a730863c00a80f7e117ab1caf7d9872ffe93cf10d7a0e  706651 bytes
2026-10-24T16:50:38Z  ccp-art413             sha256 54bc9b0fdf924dcc50cf04cd15ccafb10c3e42b23f983556243189d0ff7699a6  709050 bytes
2026-10-24T16:50:46Z  ccp-art414             sha256 6e3372e96a5c72f2cb456a4a8ced89b0425d1914fedd6b38a7b32c183c4131bc  706842 bytes
2026-10-24T16:50:54Z  ccp-art415             sha256 83c0329793419f9e4c2b9954cb36366ce41cae540c9a9b6808796732f8a51027  706151 bytes
2026-10-24T16:51:01Z  ccp-art416             sha256 149bb14dcd1e6c1067f24e30a7a87ce2c1772b73fe02453f98d17d052c54a405  706194 bytes
2026-10-24T16:51:13Z  ccp-art418             sha256 19b3320a50ce911b14e18be010fe231edeafd4e43acf0bd8b8d7b37da4886974  706871 bytes
2026-10-24T16:51:20Z  ccp-art419             sha256 d732952e4297361ed7bd2c79026873979cc95c9f66c30e33448831733f08d001  709576 bytes
2026-10-24T16:51:28Z  ccp-art419-a           sha256 fe91e270edc739cf20f61fbe21f02fd18d9db11ec561f1bf736811dbb2131a55  707645 bytes
2026-10-24T16:51:35Z  ccp-art420             sha256 0d000407448c1cee3502a54ba459197441e3c378f3ae53ed737079176231fa3f  706378 bytes
2026-10-24T16:51:43Z  ccp-art420-a           sha256 a262f667bad7234e9cd8fd0b34f1a1ea696918092c0bc24b387138bfaffa5c06  706767 bytes
2026-10-24T16:52:01Z  ccp-art424             sha256 de2c87258e5388b628d38d6425551d820d81cf460a605474eb8d51c9c252eb36  706280 bytes
2026-10-24T16:52:09Z  ccp-art425             sha256 406cdaefb7222811c12741e21215a3f5e9f4548c21761bcc4c06c79efe4ca390  708178 bytes
2026-10-24T16:52:31Z  ccp-art429             sha256 2a6d8541d420508bc0b0e15883bc0e4a15262bf095fb5d79b81163038f724bba  707906 bytes
2026-10-24T16:52:39Z  ccp-art430             sha256 b04dadba0e79873b16b3d0a833ce2643f48bed2e422ae0567310273769da681a  705907 bytes
2026-10-24T16:53:11Z  ccp-art438             sha256 7ed90308ebfff389f33dc0e72f481676d857db5a5ac49bcda4a490c81788275e  706722 bytes
2026-10-24T16:53:37Z  ccp-art444             sha256 b298ad329049019cd25e56c561a0ce04211b589ab5bad5da59a356430bd15830  708609 bytes
2026-10-24T16:54:10Z  ccp-art451             sha256 d85e1e293c44ac612b133ce78e5cd70011091038aea805ea99847b1e483a65e8  705923 bytes
2026-10-24T16:54:24Z  ccp-art454             sha256 7e56f2e8c87bb224b46bd63f84dde85de4b669458b0190392063277d19cb8594  715905 bytes
2026-10-24T16:54:43Z  ccp-art455             sha256 ba5261c32cb69ca54cbd7e79ca1a2ac9cc968475f2d78a481f80063bb6d72e4a  707231 bytes
2026-10-24T16:54:50Z  ccp-art456             sha256 edbbadf7bbce5d6d6bddb87a47f0cf2555cc184fbdb6766da6789ebd830273e8  715877 bytes
2026-10-24T16:54:58Z  ccp-art457             sha256 6a095c9212f952b41d2a204c861f247bd265dd0f9cbb6542753445edde62b0db  709821 bytes
2026-10-24T16:55:06Z  ccp-art458             sha256 335f35a05fdfca12b14dad85107f4ae354e336e4d145c6412a9ec52c7e4f1ed9  706201 bytes
2026-10-24T16:55:17Z  ccp-art460             sha256 dd70c0120468468f955f03710cb583b0d9cb702dfb23632cee28076f7fb1b83c  706462 bytes
2026-10-24T16:55:25Z  ccp-art461             sha256 f4e392a604202ca12262cac74615739fa3142d7bb0add697e32628625d796f8b  709656 bytes
2026-10-24T16:55:32Z  ccp-art462             sha256 7d13fdc4dc7184b70672036c85ee1cd26f9b1f802fae2d5bbdb1ea1e29338290  708392 bytes
2026-10-24T16:55:40Z  ccp-art463             sha256 69c0cd0c6214af7aede683fe4b691bb187c9e09092768febc16684841852ad16  705839 bytes
2026-10-24T16:55:48Z  ccp-art464             sha256 e164b3cf5d452d1f5a04e646a30f85789e0a1cfb49f2bb062f0d4e5680ee8b13  705778 bytes
2026-10-24T16:56:20Z  ccp-art465             sha256 7d95a9cb0a54639ddaf3c84f0e04e62f0efcfaf42a9270b4e2c1f7390133084f  709918 bytes
2026-10-24T16:56:28Z  ccp-art466             sha256 c8bb4e099f18b35268f4f5f08590ec3795f7687c5e19908e717f86f24933fa6d  707723 bytes
2026-10-24T16:56:43Z  ccp-art469             sha256 42f821e998541a990e9bfc6259e49a3b1ada9d66da65e41c2107d92a0cd3ad64  707002 bytes
2026-10-24T16:56:51Z  ccp-art470             sha256 60a6c22ece3360a3cb44a855ea68377ae1f876e50459dafe907ce0ec91fc9956  706738 bytes
2026-10-24T16:57:02Z  ccp-art472             sha256 16a3025d024c759c34d6595a6f156d403aa5c5847460858294d8089853d1344b  717460 bytes
2026-10-24T16:57:10Z  ccp-art473             sha256 e472c2b4e218d1509104e9a2c323bec9d05b5dcf684e8f1c852228a5794e2796  705744 bytes
2026-10-24T16:57:17Z  ccp-art474             sha256 0ba32e027778a0215982fa5b36d8eb5f5c80a75bf6ae5af0244dd03e07a3a6a0  713485 bytes
2026-10-24T16:57:25Z  ccp-art475             sha256 23e80d2a70ba598c70618dccc85e830b4e95d9eb259f148b6d363513b9179a6b  707337 bytes
2026-10-24T16:57:33Z  ccp-art476             sha256 e8410b3d7d628a8c2005821fe3acbb0932b51b80875e601207d55885885d5b1b  709915 bytes
2026-10-24T16:59:35Z  ccp-anexo-i            sha256 907d41569c0678248a07a4146c08f3c81dd4d849f923f206d93cd2970db03c2a  746915 bytes
2026-10-24T16:59:43Z  ccp-anexo-ii           sha256 f56923be3aace78899b021a1aa3d1f1c197f50f9b06e40c3f32957a4deb8ebca  740351 bytes
2026-10-24T16:59:51Z  ccp-anexo-iii          sha256 a4f4e5fcd547cd00eff45174333f562f1f8dde65f3794cdc78aadc1c1a9182a1  721369 bytes
2026-10-24T16:59:59Z  ccp-anexo-iv           sha256 63c69c8b0e11be4b3b523e0c04d4cb4ca8e3be9c081ba7fdfac0d07ccd05196a  725070 bytes
2026-10-24T17:00:08Z  ccp-anexo-v            sha256 c3b1de6488802cd792042ebca51fc346a4847b6174fbd1b45cdf574278b87b0d  736328 bytes
2026-10-24T17:00:16Z  ccp-anexo-viii         sha256 c9c8c0c4f4f101288214f627418ccac838a762ca0b46b1bc10747e25c605c8e5  721555 bytes
2026-10-24T17:00:24Z  ccp-anexo-ix           sha256 e7a167ffd376f6f11afd72aca0e15b0ae1d8d05b525e0ed006f440ddfa79ac99  720975 bytes
2026-10-24T17:00:32Z  ccp-anexo-xii          sha256 042a42f7ead1f9f2d26258ff40d9dea67c3ced35c47bd8b9e6fd8ece858be629  730307 bytes
2026-10-24T17:00:40Z  ccp-anexo-xiii         sha256 b5c346a921f288fdf6edb8e3b2525b620c2c1b3ffea137da9a78c4501351534e  727545 bytes
```

## 2026-10-24 B2a.2 structure, normas and vigencias (commit: B2a.2: CCP structured into passages, every act a note names registered, notes into vigencias)
- Done: tools/build_law.py (ccp-build-law-0.1, run with --no-history for this step). The consolidated raw got
  revision 2 (same bytes, working text by dr-article-history@1 so passages and notes share offsets, D29); verify's
  orphan rule now counts every revision's bytes. engine/structure 0.2 over that text: 3427 ccp passages, 596 artigo
  (570 code + 18 decree + 8 quoted; the two the DR prints without "º", "Artigo 410-A" and "Artigo 464-A", are now
  articles: before, their notes fell on arts. 410 and 464), 14 anexo, 1647 numero, 995 alinea, 61 subalinea, 114
  headings. notes_to_vigencias: 689 vigencias of the CCP (altera 513, adita 106, revoga 53, retifica 17 ... one per
  passage and date), each quoting its note at offsets of the consolidated text; the four dateless notes resolved by
  D28 (18-A/2008 -> 2008-07-30, 42/2017 -> 2018-01-01 by siblings; DL 214-G/2015 -> 2015-12-01 by its art. 15.º, «60
  dias após a sua publicação»; DL 278/2009 -> 2009-10-07: it fixes no day and its other notes carry two dates, so the
  general rule of Lei n.º 74/98, art. 2.º, n.º 2, «no 5.º dia após a publicação», read from its captured passage, D31).
  Normas: 28, all PT: norma:ccp, the 22 acts the notes name (title, DR address from the note's own link), and the
  captured acts dl-177-2026, dl-214-g-2015, dl-278-2009, lei-74-1998 (title and scope read from their pages). Acts'
  own passages: dl-177-2026 1440, dl-214-g-2015 1295, dl-278-2009 192, lei-74-1998 136, each dated by the act's entry
  into force, with an `entra_em_vigor` vigencia quoting the article that fixes it (D32, schema enum + one value).
- Captured in this step (one GET each, 3 s apart; nothing sent):
```
2026-10-24T17:03:57Z  dl-214-g-2015 (detail)   sha256 8681bb4e77c4cd799a349fc9459dd9fa7f6b09a68b8a1068cd5adda986c5061a  756879 bytes
2026-10-24T17:04:05Z  dl-278-2009 (detail)     sha256 83582a465c84b23347b36c1c4b01b4268b0bd2040b0eed8b741f9d19486bc968  751325 bytes
2026-10-24T17:05:13Z  lei-74-1998 (consol.)    sha256 5500ca94a7d0c31467fc9985828b7c3c69ee8c06d1451d0654a1f83e4771eb7b  237978 bytes
2026-10-24T17:08:18Z  ccp-art410-a (history)   sha256 536b84403bd0da8d788b8d662aa3151c620fdba4bc1b37650a611a7068ae783f  361073 bytes
2026-10-24T17:08:26Z  ccp-art464-a (history)   sha256 4ebf3e871aa0a3eed7dd06bf5bdf6363083802828a931a968e844ed6d053d1e2  363358 bytes
```
  The two histories complete B2a.1: the walk visited arts. 410-A and 464-A but could not name them (DR title without
  "º"); capture_dr_history 0.6 reads them and opens a given detail address (one GET, one click).
- DR data as read, not corrected: art. 132 dates its DL 278/2009 change from 2008-07-30; Anexo II dates its 36-A/2017
  retificação from 2008-07-30; art. 410's newest history version is titled "Artigo 410".
- verify at this commit: FAILED with 657 TIME (vigencias whose date starts no version yet: B2a.3 builds them). New
  decisions: D29, D30 (written before B2a.3), D31, D32 (schema: vigencia.effect + entra_em_vigor).
- Registered: verify@9, vigente@3, structure@2, capture-dr-history@3, build-law@1.
- Slip, disclosed: the B2a.1 commit also carried the bytes (and working texts) of the four EU threshold regulations
  read for B2b (8 files in law/raw_bytes); their raw records land with B2b, so until then verify lists them as orphans
  (I01), as it does at this commit.
- Next: B2a.3 versions from the histories.
- Why: a verdict cites a passage and a version; this step gives every article an id and every note a date.

## 2026-10-24 B2a.3 passage versions from the histories (commit: B2a.3: passage versions from the DR history views; vigente diff at 2026-10-01 equals the DL 177/2026 vigencias)
- Done: tools/build_law.py with histories (D24, D30): each of the 315 articles and annexes with a history page takes one
  version per date of that page, the newest text of a date winning (retificações folded), ordered by date (Anexo II's
  36-A/2017 retificação dates its text from 2008-07-30); a noteless repeat of a version (Anexo XII) is dropped; numbers,
  alíneas and subalíneas are structured inside each version, keep one version while their text is unchanged, and a
  part a version no longer has is closed by a revoked version quoting that date's note; each part's new version on a
  date of its article's vigencia gets the same note. The 68 articles added once and never changed keep the
  consolidated text from the date they were added. Writes: 2515 passages revised (revision 2), 446 parts added that
  exist only in earlier versions, 3975 unchanged; 3276 vigencias added.
- Result: CCP 3873 passages, 6304 versions; artigos by number of versions: 1: 297, 2: 157, 3: 77, 4: 45, 5: 15, 6: 4,
  7: 1; 45 articles revoked today. Vigencias 6912 (CCP 3965: altera 2661, adita 620, retifica 373, revoga 311; acts'
  own entra_em_vigor 2947). History dates vs note dates per article: 0 only in notes, 0 only in history.
- Done criterion: vigente(2026-09-30) and vigente(2026-10-01) differ in 2568 passages = exactly the passages whose
  vigencia names norma:dl-177-2026 from 2026-10-01 (1128 of the CCP, 1440 of DL 177/2026 itself entering into force,
  D32); first five: ccp:anexo-i, ccp:anexo-i.1, ccp:anexo-i.2, ccp:anexo-i.3, ccp:anexo-i.4. verify: ok.
  pytest tests/fill/test_b1_copied_modules.py tests/fill/test_b2_ccp_capture.py: 5 passed; tests --ignore=tests/fill:
  52 passed.
- The four EU threshold raw records (bytes already in the B2a.1 commit) are added here, so this commit verifies clean;
  their normas come with B2b.
- Next: B2b, the law around the CCP.
- Why: a verdict on a procedure is checked against the text in force on its date; this step makes that a lookup.

## 2026-10-24 B2b the law around the CCP (commit: B2b: the corpus around the CCP registered, captured and structured; law/COVERAGE.md)
- Done: 39 pages read (one GET each, 3 s apart, nothing sent): 4 EU threshold regulations from EUR-Lex (PT), 12
  consolidated DR pages (Lei 30/2021, CPA, Portaria 318-B/2023, DL 197/99, Lei 75/2013, Lei 98/97, CPTA, CPPT, CSC,
  CT, CP, CC), 21 DR detail pages and DLR 34/2008/M twice (detail + consolidated, the address read from the links of
  the DLR 6/2018/M page). Addresses came from note links, the ELI links printed on the DL 177/2026 page, the
  timeline, and searches restricted to diariodarepublica.pt; each page's title line was checked against the act
  meant (all matched). tools/build_law.py now builds every captured act (D33), registers the 24 timeline items and
  writes law/build-report.json; tools/coverage.py writes law/COVERAGE.md from the store.
- Report (law/COVERAGE.md): normas registered 373 / captured 43 / structured 25 / with vigências 54; timeline 24 items
  (23 amending acts + DL 18/2008), 24 registered; acts named in the CCP's notes 22, 22 registered; cited by the
  applicable law and captured: DL 111-B/2017, Lei 30/2021, DL 18/2008 (art. 18.º structured), the four retificações.
  Remissões of the CCP's text: 71 references, 14 distinct Portuguese acts, 14 captured (100 %), 6 resolved to a passage
  of the act cited; 17 distinct EU acts (not captured, except the thresholds). Phase 3: every item registered and
  captured; findings checked against the captured words: Madeira's 1,45 is DLR 34/2008/M art. 4.º n.os 1 and 4 (DLR
  26/2022/M art. 75.º, in force 2022-12-30; originally 1,35; its n.º 1 cites CCP articles by the pre-DL 177/2026
  numbering), not the 2026 budget (DLR 8/2025/M only amends art. 7.º); Portaria 371/2017 revoked by 318-A/2023;
  Portaria 372/2017 is about habilitação documents, BASE is Portaria 318-B/2023; EU thresholds 2026–2027 are
  Delegated Regulations 2025/2150, 2151, 2152 and 2487 (ELI stored in its https form, the schema's pattern).
- Not structured, with the reason recorded: CC, CPPT, CSC, CT, Lei 98/97, CRCSPSS (structure finds a duplicate path:
  their alínea / heading patterns are outside the grammar), CPTA (a note inside a quotation), DL 197/99 (its articles
  without notes cannot be dated: no readable entry into force), DL 74/99 and Lei 107/2001 (entry into force not in a
  phrasing entry_into_force reads), the EU acts (no EU grammar), the retificações (no articles of their own). Left out
  under D33: DL 197/99 arts. 15–22-A, 28, 29 (notes "Reposto em Vigor": the autorização-de-despesa articles phase 3
  needs; a decision, not a guess), CP art. 13, Lei 75/2013 arts. 4–5, Portaria 318-B/2023 arts. 18 and 20.
- Engine: vigente note grammar reads "Diário do Governo", supplement forms, "Artigo único", "00:00:00", Acórdãos do
  Tribunal Constitucional (actc-), two-letter suffixes (n.º 20-AS/2001); DL 18/2008's own articles dated 2008-07-30, the
  consolidated page's "Versão inicial" (INITIAL), quoting its art. 18.º. DECISIONS D33.
- Reads, disclosed: 8 detail pages were read with an http ELI address the raw schema refuses, so nothing was recorded;
  they were read again with the https form (a second read each: Portaria 371/2017, Lei 96/2015, DL 104/2011, Lei
  45/2011, Lei 21/2023, Lei 110/2009, Lei 107/2001, Lei 41/2015). The first reads' bytes were left in law/raw_bytes by
  the refused writes; they are moved out of the store (no record names them).
- Tests: the B2b red tests are green. Two of their assertions were set before measuring and are corrected here: the
  timeline has 24 items (23 amending acts and the original act, which the DR prints last) and the floor of distinct
  Portuguese remissões is 10 (14 measured; the first floor, 20, was a guess); captured() now requires the act's own page.
- Registered: vigente@5, build-law@4, coverage@1. verify: ok.
- Next: B2c municipal pilot.
- Why: a verdict on a procedure also cites the law the CCP points to and the regional and EU numbers that change it.
- Pages (captured_at, id, sha256, bytes):
```
2026-10-24T16:12:24Z  eu-2025-2152 (regulamento)   sha256 1162d1496dbbac6723276882138fb757ad6a123ef0461019c4c7646c1284ca43  19348 bytes
2026-10-24T16:12:44Z  eu-2025-2150 (regulamento)   sha256 d396e76527ac286eaa9456ac31b53bd108d7689d4d1aaba7f3f33983229ba336  15865 bytes
2026-10-24T16:12:51Z  eu-2025-2151 (regulamento)   sha256 08a51a63f81c307e89182d374da1e667a90e71a4244f2cf577348815ded1c66a  14005 bytes
2026-10-24T16:12:58Z  eu-2025-2487 (regulamento)   sha256 74ff010cafad382714ef5175a649650a359796bd1f57cccb9c5ba2027f47ec1a  18546 bytes
2026-10-24T17:17:33Z  lei-30-2021 (lei)            sha256 d93eaf9f1c15510e03b9f15671f5980c5122f312f5d8cab75392b29b57b4b29f  315184 bytes
2026-10-24T17:17:44Z  cpa (lei)                    sha256 73e281bff097ebf1fce88ebbc7c39e9c3ee59e813574a4360c52b7cd43b5fb25  734979 bytes
2026-10-24T17:17:56Z  port-318-b-2023 (lei)        sha256 5fb5b1764eea6cb243cc3e4e015c8538c9ed8d2c18f551a132ef7b9047ab320a  1286652 bytes
2026-10-24T17:18:08Z  dl-197-1999 (lei)            sha256 d2acd5385514bd4e354caf6ae74257afbf104a1fc2488acdd3aaacb8a73d7d2b  1028341 bytes
2026-10-24T17:18:19Z  lei-75-2013 (lei)            sha256 729211c2aae09d6ca317ded977fad30fece9f9c7d229d711d08f2ea321f1d9a7  562355 bytes
2026-10-24T17:18:31Z  lei-98-1997 (lei)            sha256 a368148a55b519041ebcff0470fb5c938c19841936d494a97b9dae31ff223b3c  571086 bytes
2026-10-24T17:18:43Z  cpta (lei)                   sha256 a554338c7f6d1f986d55307eae33a536f3ab83ea6bc80d1b412741732c61ae89  1007530 bytes
2026-10-24T17:18:54Z  cppt (lei)                   sha256 6abbf6cea3d4a0216943312cbcad85ca7ecc73dc7ed4e15f08c0ecb18637db1f  1435677 bytes
2026-10-24T17:19:06Z  csc (lei)                    sha256 1d8a350a88996732888b04c6c19c43a6e217ec63b2e96722d10608564fed41dc  2808548 bytes
2026-10-24T17:19:20Z  ct (lei)                     sha256 55ff901bae9c53c61217fc5dc11cf210f6abab07259624327882150044655405  2156067 bytes
2026-10-24T17:19:33Z  cp (lei)                     sha256 f4a6bfcb90e93b9f0d019a93ad55bef973913e0d21aa64f07d05c0ece2b5ef7c  1888474 bytes
2026-10-24T17:19:45Z  cc (lei)                     sha256 4a6289cd3aea2defbecb4befe4b277d3a2e18969412e7839b60d18ff3976f8cc  5954338 bytes
2026-10-24T17:20:02Z  dl-111-b-2017 (diploma)      sha256 62464e3357ba4050b7fbb337f029720c356017bba17160502fc72a49a85401b6  1161980 bytes
2026-10-24T17:20:13Z  dl-18-2008 (diploma)         sha256 ae58d108c5f1f747c1c5a4fb42dd9e50998935808794e7a90bf4e5ecb2e5b261  974270 bytes
2026-10-24T17:20:24Z  ret-18-a-2008 (diploma)      sha256 feb96e27fa5bc232b7d3dca497e23736410924e2ae30c7355bd37e3cf9b90195  128616 bytes
2026-10-24T17:20:35Z  ret-36-a-2017 (diploma)      sha256 44300c49e9de5a88f8587136f06d15249f914b520f7b1c7f7faaa96c4e3ec4bb  128198 bytes
2026-10-24T17:20:46Z  ret-42-2017 (diploma)        sha256 c148e9312539b1bfe2be6d766451c16dd729ef6c39a4e65d99d33f84431addbf  122932 bytes
2026-10-24T17:20:58Z  ret-25-2021 (diploma)        sha256 fb74b05300949b2a3cf2c764bd9660e9c739ee24bb9c37cf848937f03865e939  89638 bytes
2026-10-24T17:21:09Z  dl-60-2018 (diploma)         sha256 a2eef1ca41933d422ccf4fe7941f2a9ab0e499bda97918ae77bcc7455a8f10e9  113593 bytes
2026-10-24T17:21:20Z  dlr-27-2015-a (diploma)      sha256 82f7329621336f9824cd91517b297c384ebb0f96daec6000e8cf090da1b19219  291774 bytes
2026-10-24T17:21:31Z  dlr-6-2018-m (diploma)       sha256 bc09414f67ee5c9c2430f9394fb839cbef5b0434db13a83a37985fb657168287  147087 bytes
2026-10-24T17:21:41Z  dlr-8-2025-m (diploma)       sha256 e3f67e0d0ab1a4001e09e9f0b9441e5957fb66b2553b061cb5efaf0ad1a73c7e  440459 bytes
2026-10-24T17:21:53Z  port-372-2017 (diploma)      sha256 26df667df4306960a5871a2c9673852d68dd106f1821e59570a4652a9a20d7a5  98554 bytes
2026-10-24T17:22:05Z  port-318-a-2023 (diploma)    sha256 a45ca266ceead82cccb93c9c9805a6beb9d4661770ea3ebfc4976f66ba4a77da  908296 bytes
2026-10-24T17:22:27Z  dl-74-1999 (diploma)         sha256 b43043bc9a6948c3e29f9bbc547722d725e8b665db3e10dcec3ca9e128e00563  104315 bytes
2026-10-24T17:24:15Z  port-371-2017 (diploma)      sha256 249aa9cf6b9d20e25e799a7fd3a0ca6a9b441de1efa2ac32f8e529e5baec1d79  213336 bytes
2026-10-24T17:24:27Z  lei-96-2015 (diploma)        sha256 d4db84f52103a9ae954ad5c7435e3ecc32db6d948445fefab89766b34dbffdbd  272533 bytes
2026-10-24T17:24:37Z  dl-104-2011 (diploma)        sha256 5f742418231bcf05c34f88a83dc1f8e9f674e2950f78e1613b6994d1f77130e2  193557 bytes
2026-10-24T17:24:49Z  lei-45-2011 (diploma)        sha256 272e2b5b824be365cab7e55b0cbfc1544d8b028f70b10cb5146b4a64cf5ca6b7  111104 bytes
2026-10-24T17:25:00Z  lei-21-2023 (diploma)        sha256 8da9abfd6bb66ec2482d8db858d699fc0cb91859c1f23b81f00069e0543c6000  120353 bytes
2026-10-24T17:25:11Z  crcspss (diploma)            sha256 f91857d829eaff322ae37acf0f3c571f2a406c79d1a5a7b6911a7a0468c540d2  401841 bytes
2026-10-24T17:25:23Z  lei-107-2001 (diploma)       sha256 b5691caf55c28058a5801619f7e3699b10c8c62794ea14da9dce357e7c2e4d11  263648 bytes
2026-10-24T17:25:35Z  lei-41-2015 (diploma)        sha256 1dd4030bd85b460afc3f4997e87e18e330fb0ec99230888574dca0c5d8793c76  210188 bytes
2026-10-24T17:26:36Z  dlr-34-2008-m (diploma)      sha256 2db6e476b2eebd18431caef428bec23d67c0949f4fb90fa7c7cec5b286cfb790  133599 bytes
2026-10-24T17:27:04Z  dlr-34-2008-m (lei)          sha256 9c1d3fd573a8fba033b068423cad4284c75d9792553f3112f66ac1ee027c4da2  224283 bytes
```

## 2026-10-24 B2c municipal pilot (commit: B2c: municipal pilot of 10 municípios; law/MUNICIPIOS-PILOTO.md)
- Done: law/municipios/piloto.json (per município: what was looked for, where, what was found) and
  tools/pilot_municipios.py, which writes law/MUNICIPIOS-PILOTO.md counting only from the store (found = with a URL,
  captured = raw in law/, with text = HTML text or a PDF text layer of >= 500 characters per page). data/ holds no BASE
  anúncios, so the pilot is the default ten. Three record types: norma de controlo interno, delegação de competências
  (who authorises spending), regulamento de compras / orçamento. Searches restricted to each município's domain and to
  diariodarepublica.pt; a result counts only when the document names the município (one search summary attributed
  Famalicão's Edital n.º 1736/2025 to four other municípios).
- Result: 12 records found, 11 captured, 7 with text, in 10 municípios. Lisboa 2/2/1 (NCI = Deliberação 187/CM/2011,
  80 pages mostly scanned; budget regulation 2025), Porto 1/1/1 (NCI 2024), Gaia 1/1/0 (NCI 2024, 76 pages, ~200
  characters of text: a scan), Braga 0, Coimbra 2/2/2 (editais 414 and 406/2025: delegation and subdelegation, on its
  own site), Sintra 1/1/0 and Cascais 2/2/1 (DR 2.ª série avisos that cite their delegations: the DR's PDFs are
  encrypted, so their text is not verified here), Loures 1/0/0 (its site's TLS certificate does not verify from here;
  not bypassed), Funchal 2/2/2 (NCI 2025; an aviso that cites the delegation despacho of 2026-01-08 / Edital n.º
  19/2026), Ponta Delgada 0. Estimate for 308: ~370 records found, ~339 capturable, ~154 with text usable without OCR,
  ~370 reads (~1.5 h of capture); searching, not reading, is the cost, and 3 of 10 large municípios gave nothing. No
  municipal field was added to norma: that is a phase-3 DECISIONS row first.
- Captured (one GET each, 3 s apart, nothing sent; municipal sites by tools/capture_page.py, plain GET; the Funchal
  aviso by tools/capture_dr_consolidated.py):
```
2026-10-24T16:20:25Z  porto-nci-2024                     sha256 8461a9b7f41516a21da6142b1d5f6111aaa725eccd14655622e75b951d7c8b63  1650047 bytes
2026-10-24T16:20:29Z  gaia-nci-2024                      sha256 c0b6f49558354f5023de0b76dff1fd40274f427932e1f0ba95febdc3fcd5d5a9  782705 bytes
2026-10-24T16:20:33Z  cascais-nci-2022                   sha256 5ed2dacfc92b1ac0ececb48575d0fc8e496be040c727bb2c58f0998750ec19d0  514601 bytes
2026-10-24T16:20:37Z  funchal-nci-2025                   sha256 ad447f0f96e84d07f1eb3a46946fe921b87a86370415d971581b3fbf5f3a495b  4978846 bytes
2026-10-24T16:21:11Z  lisboa-nci-2011                    sha256 2ed32d06e6e96fcb6e477cef2058fb148389b1b25997a5e2d534583502dfd262  10384396 bytes
2026-10-24T16:21:15Z  lisboa-regulamento-orcamento-2025  sha256 bce7f5658291cd84255f86ee0e72bdd4b31b2d111b7bc00aeeca4ca37200cc94  398046 bytes
2026-10-24T17:18:14Z  coimbra-edital-414-2025            sha256 0c3fe50a1d949938d03a3aec5fa2dd9251acb1f0c89d196b06b43bd9daa6f98c  768708 bytes
2026-10-24T17:18:18Z  coimbra-edital-406-2025            sha256 76881d53496f9c0376c845ed4410ed12a6348872cf26d467f50e83cef46250c3  400697 bytes
2026-10-24T17:41:18Z  sintra-aviso-2033-2026             sha256 2fb520d735a27b4ffbcd2a530eec5fda9d21eaf0b97377be7b0f4069063376e9  57712 bytes
2026-10-24T17:41:29Z  cascais-aviso-22089-2025           sha256 c35ed7fe1899a7630e385c8cece13d6d90aacfe121fbcbc273543d232a2a54cf  552420 bytes
2026-10-24T17:41:41Z  funchal-aviso-6712-2026            sha256 dc0d2c28f04b917a062aa6541cfc80df1b505def19abef94de0647f5119389f4  116587 bytes
```
- Correction to the B2b entry: the tools registered there are vigente@4 and build-law@3 (not @5 / @4).
- Registered: capture-page@1, pilot-municipios@1. verify: ok; tests/fill/test_b2c_pilot.py green.
- Next: close the phase (four commands, CI, report for the independent review).
- Why: the 308 municípios are contracting authorities; who may authorise a spend is their own law, and the pilot says
  where it lives and what reading it costs before any of it enters the engine.

## 2026-10-24 audit of phase 2 (commit: Audit of phase 2: the law stands; 9/10)
- Done: AUDIT-2026-10-24-PHASE-2.md; the filler's seven commits accepted without edits; numbers re-derived here; three
  real-law mutations caught; debts for phase 3 listed (EU thresholds and six codes without passages, remissões at act
  level, slow fill tests).
- Next: phase 3 (the builder): B3 rules by two families over the real text, B4 engine over the extractor's notices, §8.
- Why: the law layer is now data someone can be wrong about, and verify says when.

## 2026-10-24 phase 3 opens: red tests for the phase-2 debts (commit: Tests: red D0, the three debts the phase-2 audit listed)
- Done: tests/fill/test_d0_phase2_debts.py, red against 6c3115fb: (1) the four EU threshold regulations structured by a
  versioned EUR-Lex extractor with an entra_em_vigor vigencia and their amounts in the passage text; (2) CC, CPPT, CSC,
  CT, Lei 98/97 and CRCSPSS with their articles as passages (floors 2000 / 250 / 500 / 500 / 100 / 250); (3) at least
  90 % of the CCP's references naming an article of a Portuguese act resolved to a passage, COVERAGE.md as the tool
  writes it. Baseline (commands of the phase prompt): verify ok; 52 passed; fill 3 failed (B3, B4 x2), 11 passed;
  redteam 0 MISSED; data/facts and data/raw empty, adapters/ holds a README only.
- Correction before green, disclosed: test (3) first counted the 16 references to EU directives (not captured in this
  phase) and asked for 20 article references; it now counts Portuguese acts (11 measured).
- Next: D0.2, D0.1, D0.3 (in that order: the EU acts use the second layout).
- Why: the audit listed them as what phase 3 must clear before rules cite the law around the CCP.

## 2026-10-24 D0.2 a second structure layout for the codes (commit: D0.2: second structure layout (dr-codigo) for the codes the CCP grammar cannot read)
- Done: engine/structure.py 0.3 adds `structure_codigo` (layout dr-codigo, D34) beside the unchanged `structure`;
  tools/build_law.py picks it per act (the CCP layout refuses the text or reads under 90 % of its articles), records the
  layout in law/build-report.json, gives an object it no longer produces a stale revision, and dates a consolidated
  act's notes against the acts already read; engine/vigente.py: `whole_act_clause` (D36: Lei 7/2009's art. 14.º dates
  only some provisions); verify TIME skips a stale vigencia (withdrawn, with its reason). Captured, one GET each, 3 s
  apart, to date the dateless notes on the codes' pages (D28): DL 114-D/2023, DL 321-B/90, Lei 143/2015, Lei 90/2019,
  DL 262/83, Lei 150/2015, DL 379/86, DL 200-C/80, Lei 137/2015, DL 605/76.
- Result: articles as passages: CC 2082 (of 2405; 323 left out by D33, notes nothing dates), CPPT 323, CSC 550, CT 575,
  Lei 98/97 117, CRCSPSS 290; also CPTA 216 (was 8) and Código Penal 442 (was 13), whose code text follows the decree's
  closing formula; DL 197/99 199. DR slips kept as -dupN: 7 passages (cppt:art188-dup2 = the article printed with the
  next one's number, cppt:art89.5-dup2, csc:art132.1.a-dup2 ...). Store: 36524 passages, 28193 vigencias; 9 passages and
  13 vigencias of CP's decree articles (now cp:dl.artN) marked stale. verify ok; redteam 0 MISSED; test_d0 (2) green.
- Pages (captured_at, id, sha256, bytes):
```
2026-10-24T20:06:02Z  dl-114-d-2023    sha256 16ec4c72648917cdefcce8e63450c2edcaab16a9ef36cac4ccc3978934f875ca  224121 bytes
2026-10-24T20:06:18Z  dl-321-b-1990    sha256 f5e3147179955864b93b9b64d326fe115a31f9ac5d74fc1b8f5080ca77ab102a  228779 bytes
2026-10-24T20:06:34Z  lei-143-2015     sha256 c8566e247d8864d452314fbdcf40ae38c38db2202a3bb8014ee51e450be33444  227571 bytes
2026-10-24T20:06:50Z  lei-90-2019      sha256 a8e0e92a781119f29f1c4a0b88e7e24ece24a9a2820956dc622871b40b7e940f  150060 bytes
2026-10-24T20:07:06Z  dl-262-1983      sha256 bba255dd4ead74f291ac6682f1aca1fc4e2989344a6f380c67c61cddd72b6c0a  90331 bytes
2026-10-24T20:07:21Z  lei-150-2015     sha256 b6450db25488343f4f823c7180c05802b7f942ccdfe835cce0e8a78010c1a8f1  230923 bytes
2026-10-24T20:07:37Z  dl-379-1986      sha256 beb9cd2ef0eb6aa60ee724e5a131a459fb8a06d63a0fbdc8869efda42976a31b  97116 bytes
2026-10-24T20:07:52Z  dl-200-c-1980    sha256 3130d2887f7c03aec647b563d1b1c59d897f8ac34899e1bf8342bf0d60c27581  83742 bytes
2026-10-24T20:08:08Z  lei-137-2015     sha256 ace2ded0c88be98c3e51065ea30c4bc7f801253d99fddfa1daf04324383cf669  91560 bytes
2026-10-24T20:08:24Z  dl-605-1976      sha256 b2bcf79d2c70785dbd666238461b94f515658f48af846c735b9fb0e5181ab25b  92177 bytes
```
- Registered: structure, extract, build-law, vigente, coverage, verify (new versions). DECISIONS D34, D36 (and D35,
  written with them, used by D0.1).
- Next: D0.1 EU acts.
- Why: a rule that points to the Civil Code or the CPTA must find the article it points to.
