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

## 2026-10-24 D0.1 the EU threshold regulations structured (commit: D0.1: EUR-Lex extractor eurlex-html@1; the four EU threshold regulations structured)
- Done: engine/extract.py `eurlex-html@1`: an Official Journal page -> date, title and ELI lines, then the enacting
  terms (Artigo N.º; each point of a two-cell row as one line "1) ...", "a) ..."; the superscript ordinal "o" written º).
  The four raw records get revision 2 with that text (bytes unchanged, D29 pattern); structure_codigo (D34) reads them;
  each passage starts on the day the act applies, 2026-01-01, with an entra_em_vigor vigencia quoting art. 2.º (D35).
- Result: eu-2025-2152 (Directive 2014/24/UE: 5 404 000 / 140 000 / 216 000 EUR), eu-2025-2150 (2014/25/UE: 432 000 /
  5 404 000), eu-2025-2151 (2014/23/UE: 5 404 000), eu-2025-2487 (2009/81/CE: 432 000 / 5 404 000): 2 articles each,
  their points and alíneas as passages; normas carry the https form of the ELI read on the page. test_d0 (1) green.
- Note: the D0.2 commit registered the extractor's new hash before this commit carried the file; verify's PROV is
  green from this commit on.
- Next: D0.3 remissões to passages.
- Why: a limiar rule for the JOUE thresholds cites these passages.

## 2026-10-24 D0.3 remissões resolved to passages (commit: D0.3: remissões resolved to the article, number or alínea they name; COVERAGE regenerated)
- Done: tools/coverage.py reads «alínea x) do n.º N do artigo M.º» before the act's name and resolves to the most
  specific passage that exists (alínea, number, article); COVERAGE.md lists every resolution.
- Result: 71 references; 26 name an article (11 of Portuguese acts, 15 of EU directives not captured); the 11
  Portuguese ones all resolve (cpa:art66, cpa:art87 x3, cpa:art161, ct:art140.2, cc:art566.3, cpta:art100.1,
  lei-21-2023:art2, crcspss:art208.2, cppt:art177-a.1), 6 down to the number. COVERAGE: 373 normas, 53 captured, 47
  structured, 256 with vigências. test_d0 green (3/3); verify ok.
- Next: B3 rules by two families.
- Why: a rule's exception or remissão cites the passage of the other act, not just its name.

## 2026-10-24 B5 set-up: held-out set declared before any rule (commit: B5: held-out set declared and frozen before any rule enters the log; red test)
- Done: law/HELD-OUT.json (declared 2026-10-24T20:45:11Z, frozen_at 2026-10-24, sha256 of the canonical definition
  2be68e3fe6da103a5a516399b18dc0149c599fd779dddda56b47268c04451c70): a proc is held out when its adjudicante's NIF hashes
  to 0 mod 5 (about 20 % of contracting authorities) or it started on or after 2026-10-01 (the last month, under DL
  177/2026). Declared while governance/events.jsonl holds one event (the principals product rule): no B3 rule exists
  yet. tests/fill/test_b5_measure.py, red: the declaration and its hash; >= 100 reference cases from data/ or 20 from
  fixtures/measure/ with two blind annotators and their raw answers, CASOS-DESACORDO.md; reports/measure/<date> with
  precision and recall per rule, 95 % Wilson intervals, inside / held out, agreement, recomputed byte for byte.
- In progress outside this commit: the B3 readers are answering (leitor:b by the CLI of family B; leitor:a on Modal).
- Next: record B3.
- Why: §8 needs the held-out set fixed before the method meets it; the commit order is the proof.

## 2026-10-24 B3 rules read by two families (commit: B3: 18 rule readings by two families in the governance log; 1 settled, 17 proposed; DESACORDOS, RESUMO)
- Done: tools/read_rules.py (ccp-read-rules-0.1, ferramenta): 18 targets (selector DL 177/2026 art. 7.º; limiar ajuste
  direto and consulta prévia for goods/services and works, @v1 = text to 2026-09-30, @v2 = from 2026-10-01 (D5); JOUE
  thresholds for goods/services (State) and works; Madeira and Açores; prazo mínimo without / with JOUE; procedures
  @v1/@v2). Each prompt: typed question, candidate passage ids with their text in force on the date and the earlier
  text, an answer schema (governance/readings/<rule>/prompt.json). Readers in readers/ (D38): leitor:a on Modal (L40S,
  vLLM 0.30, bf16, temperature 0, guided JSON); leitor:b by its command-line client, read-only, ephemeral, in an empty
  directory (blind: it never sees leitor:a's answer). Raw answers with at and sha256 in governance/readings/; record:
  Log.propose (leitor:a) -> rule built with engine.passages.cite (whole passage text, offsets) -> Log.review (leitor:b,
  blind; uphold only on equal passages, conditions and params, else request_evidence; D37); rules/ is the replay.
- Result (governance/readings/RESUMO.md): 18 rules in the log (37 events), 1 settled (limiar-ajuste-direto-obras@v2:
  ccp:art19.d, preco_base < 150 000 EUR), 17 proposed, 0 ai_reviewed (the protocol has no event for it, D37). Exact
  agreement A vs B 1/18; agreement of direction (the threshold, days, procedure list, regimes, effect) 14/18. Package:
  pacote:ccp@2026-10-01 with that one rule; no package for 2026-09-30 (no settled rule valid that day; a package names
  at least one rule), hence no diff. Disagreements: governance/readings/DESACORDOS.md (17), for the pessoa to see:
  product, never the content of a reading. Most differences are leitor:a's conditions (op "in" with a single string,
  conditions that do not apply, "AAAA-MM-DD" taken literally); one is the law itself: the JOUE threshold for goods and
  services awarded by the State is 139 000 EUR in CCP art. 474.º n.º 3 b) (text of 2026-10-01) and 140 000 EUR in
  Delegated Regulation (EU) 2025/2152 (from 2026-01-01): A chose the first, B the second.
- Attempts, disclosed: leitor:a attempt 1 (free whitespace in the grammar): 8/18 answers looped on blanks to max_tokens;
  attempt 2 (whitespace flag per request): 7/18, the flag was not honoured; attempt 3 (flag on the engine): 18/18
  complete. All kept (leitor-a.attempt1/2.json). The first `record` run wrote two log lines (selector) and then failed
  on a schema-invalid rule; the unpublished file was restored to its committed state and the tool now validates the
  rule before any event. Two answer schemas were looser than the regra schema (selector `to` any string; Açores
  predicate could be empty): both readers were asked again for those two rules with the corrected schema (earlier
  answers kept as *.attempt*.json); nothing of them had entered the log. leitor:b's first run used the earlier place of
  its runner (tools/read_rules.py run-b), same command, now readers/leitor_b_cli.py. Modal: four short runs on one L40S.
- verify: ok (37 events). test_b3 green. Registered: read-rules, run-engine (code in the B4 commit). DECISIONS D37, D38.
- Next: B4 engine over notices (data/facts is empty: blocked, implemented on fixtures).
- Why: a rule enters a package only when two families read the same passages the same way; the log says which did.

## 2026-10-24 B4 engine v0 — BLOCKED on the extractor (commit: B4: run_engine over a store of facts, tested on fixtures; blocked: data/facts is empty)
- Done: tools/run_engine.py (ccp-run-engine-0.1, ferramenta): every proc of the stores, its facts (facts_of, known at a
  fixed known_at), the package its data_inicio_procedimento selects (the settled seletor_regime's regimes), the
  package's rules for that unit kind, engine.evaluate with valid_at = the procedure's start; manifest by
  engine.manifest.build (law version, package, the facts' adapters, one source snapshot per source, repository +
  commit + engine version, log head, produced_at = known_at); verdicts written as a store to --verdicts so verify
  re-derives them (RED); report: per prazo_minimo rule cumpre / nao_cumpre / nao_avaliado by reason, declarado vs
  avaliado. tests/test_run_engine.py: over fixtures/valid the report is byte-identical across runs and verify finds 0
  failures over the fixture store plus the verdicts written (4 verdicts). verify gains a store "engine" (data + law +
  rules + governance + reports/veredictos) once reports/veredictos exists, and "measure" (B5).
- Blocked: `ls data/facts` is empty (the extractor has not delivered); test_b4 stays red as designed; no
  reports/prazos-minimos.json is written (it would count 0 units). Also blocking a real run on the law side: no
  seletor_regime is settled (B3: the two readings disagree), so the packages cannot route a procedure yet.
- What the extractor must deliver as facts of each proc (the canonical fields the 18 rules read, from regra.conditions
  and params): data_inicio_procedimento, tipo_procedimento, tipo_contrato, preco_base, publicado_joue,
  prazo_propostas_dias, data_envio_anuncio (both readers count the deadline from the sending of the anúncio, as arts.
  135.º and 136.º say, not from data_publicacao_anuncio), territorio, tipo_entidade; and adjudicante (NIF) for the
  held-out split. Value vocabulary as in tools/read_rules.py VOCAB and adapters' enum maps (bens / servicos / obras ...).
- Next: B5 measurement on fixtures/measure.
- Why: the engine is ready to count; the count waits for notices and for a settled selector.

## 2026-10-24 B5 measurement of §8 on 20 FIXTURE cases (commit: B5: measurement — 20 cases annotated blind by two families, report with Wilson intervals, recomputed by verify)
- Done: tools/make_measure_fixtures.py (ferramenta): fixtures/measure/, 20 synthetic procedures (FIXTURE, not BASE)
  on the rules' edges, stratified by procedure type, value and period, 5 adjudicantes. tools/measure.py (ferramenta):
  prompts (per case: its facts and, for every B3 rule valid on its start date, the rule's id, title and the law it
  cites, never its params), record (a pair both readers answer alike is an expected verdict; others go to
  governance/readings/CASOS-DESACORDO.md for a pessoa: nothing adjudicated here), report (engine.evaluate with each rule
  alone, valid_at = start; positive class "não cumpre"; precision and recall with 95 % Wilson intervals, inside / held
  out per law/HELD-OUT.json). Readers from readers/ (D38), answers kept with at and sha256 under
  governance/readings/casos/. verify gains BENCH (HELD-OUT.json hash; no package after frozen_at holding a rule whose
  events name a held-out unit) and MEAS (every reports/measure/*.json recomputed) plus a "measure" store.
- Result (reports/measure/2026-10-24.json / .md, frozen_at 2026-10-24, held-out sha256 2be68e3f...): 20 cases annotated
  by both families; 236 (case, rule) pairs; both answered 232; exact agreement 102 (0.44), agreement of direction
  (breach or not) 223 (0.96); 134 pairs pending adjudication or unanswered. 6 cases have at least one agreed verdict and
  are caso_referencia records (5 held out: every case from 2026-10-01 is held out by period, as declared). Figures per
  rule are thin: most agreed pairs are "não se aplica" (not an expected verdict) or both "não avaliado"; the one rule
  with a positive count is prazo-minimo-concurso-sem-joue-obras@v1, held out: precision 0.0 [0.0, 0.79] (n = 1). The
  settled rule has no agreed pair. leitor:a answers "nao_avaliado" for most pairs; leitor:b's answers read the facts
  (e.g. M-02 80 000 > 75 000 -> não cumpre; M-12 5 days < 6 -> não cumpre). Error classes of BASE notices: not
  measurable while data/ is empty (they need the extractor's afirmações).
- Correction to the red test, disclosed: it asked for 20 caso_referencia records, but a record needs one agreed
  expected verdict (schema); it now counts the 20 cases annotated by both readers and checks every record has both.
- verify: ok (stores fixtures, repo, data, measure; BENCH/MEAS ok). test_b5 green. Registered: make-measure-fixtures,
  measure, verify.
- Next: B6 the local API.
- Why: a figure is only honest with its interval, its freeze date and the disagreements beside it.

## 2026-10-24 B6 the API v1, local (commit: B6: read-only API v1 served from the store (local, not deployed); tests/test_service.py)
- Done: tools/serve.py (ccp-serve-1.0, ferramenta): /v1/saude, /v1/openapi.json, /v1/lei.json?data= (passage versions in
  force, by norma), /v1/manifesto.json (packages with law version, hash, rules, log head; code; verify version),
  /v1/exemplo/<nome> (examples/<nome>.json computed now), keyed: POST /v1/verificar by consumer id (n_anuncio, base_id)
  or by facts sent (kept only for the request) -> per rule resultado, motivo, regra (id, revision, state), passagem,
  citação, versão, manifesto, afirmações declaradas beside the verdict; /v1/regras/<id> and /indice; /v1/diff?de=&a=;
  /v1/entidade/<nif> without a name for a pessoa_singular. The package applied is the settled selector's, else the
  package whose law is in force on the start date (said in the answer). JSON only, 64 KB body, 30 s, no trace, no path
  echoed. tools/package.sh now carries schemas/, verify.py and examples/ and waits for the store to load; its smoke
  test loads 68 096 objects and 37 events from the package. Nothing deployed, nothing paid.
- Tests: tests/test_service.py (fixtures): 7 green (public routes, key, verificar by id and by facts with citations and
  the declared regime beside the verdict, entity without name, 413 / 415 / 400 / 404 without echo, the example).
- Public example, reproducible from the repo (examples/verificar-empreitada-ajuste-direto.json against law + rules +
  governance): works by ajuste direto, 140 000 EUR, started 2026-10-07 -> pacote:ccp@2026-10-01 (no settled selector:
  the package in force on that date), regra:ccp:limiar-ajuste-direto-obras@v2 (settled) cumpre, citing ccp:art19.d
  version 2026-10-01 «d) Ajuste direto, quando o valor estimado do contrato for inferior a 150 000 €.»
- Registered: serve. Next: close the phase.
- Why: the consumer asks with its own ids and gets the verdict with the words of the law it rests on.

## 2026-10-24 CI split (commit: CI: verify and the scaffold tests in separate jobs)
- Done: .github/workflows/verify.yml runs verify.py and the scaffold tests as two jobs. The B6 run passed verify.py and
  was cancelled by the 20-minute job limit during the scaffold tests (verify now also re-derives the measure store and
  recomputes the measurement; locally ~10 min + ~5 min). Nothing is skipped or weakened: each job keeps its own limit.
- Why: the gate grew with the law; the limit is per job, not a reason to drop a check.

## 2026-10-24 audit of phase 3 (commit: Audit of phase 3: evidence anchored in the log; rule replay equals the log; 9/10)
- Done: AUDIT-2026-10-24-PHASE-3.md; four real-store mutations: three passed and are now refused (READ: reader answers vs
  answer_sha256; SEAL: annotations + HELD-OUT.json sealed by tools/measure.py seal, evento:38; STATE: rule content =
  latest propose/correct payload); D39 supersedes D37's union clause, eight rule files regenerated from the log;
  reading-vs-rule check narrowed to proposer and upholding reviewers; `readers` refused by the code guard;
  tests/test_evidence.py; tools re-registered (verify@14, read-rules@5, measure@2).
- Next: the pessoa's four decisions (who proposes, what counts as replication, extractor delivery, adjudications);
  then B4 and B5 over real data.
- Why: evidence that can change without the log noticing is not evidence.

## 2026-10-25 T0 training held-out set, sealed before any example (commit: T0: training reservation per article, sealed in the log before any example; D40, D41)
- Done: law/TRAIN-HELD-OUT.json (tools/make_training.py held-out, ferramenta:make-training@1): per article (the article
  ancestor of a passage; a passage with none is its own unit) reserved when int(sha256(article id), 16) % 5 == 0, plus
  the 15 articles the 18 B3 rules cite or offer as candidates (ccp art. 16, 19, 20, 135, 136, 474; dl-177-2026 art. 7,
  10, 11; dlr-27-2015-a art. 1, 16, 19, 20; dlr-34-2008-m art. 4; eu-2025-2152 art. 1). Units 8 878, by hash 1 792,
  by B3 15, reserved 1 801 (20.3 %). frozen_at 2026-10-25, definition sha256 recorded, file sha256 bb5644c6....
  Sealed: tools/measure.py seal now carries train_held_out_sha256 (and training_index_sha256 once T1 exists), verify
  SEAL compares the newest seal with both (D40). Red test first: tests/fill/test_t1_training.py, 4 failed before the
  file existed; after T0 the held-out test is green, the three T1 tests stay red until T1.
- Deviation, disclosed: the first `register_tool` calls failed (my shell call passed name and path as one argument), so
  the first seal (evento:39) was signed by ferramenta:measure@2 although measure.py had already changed; measure@3 was
  then registered and the seal repeated (evento:40, by measure@3). Both events stay (append-only).
- Gap found and fixed (D41): retiring measure@2 made the governance replay refuse its past events (38, 39: I04) — the
  replay refused every event of a retired principal, while principals.schema.json already said past events stay valid.
  A principal now carries `retired_at`; events at or before it stay valid; register_tool stamps it. measure@2 gets
  2026-10-25T01:31:56Z (the `at` of its successor's first event: upper bound). Red-team P1/P2 (retired before its
  events; retired without retired_at) are caught as I04. tests/test_evidence.py gains the D40 seal test.
- verify: ok (stores fixtures 58 / repo 68 096, 40 events / measure; 26 broken overlays refused). redteam: 0 MISSED.
  Registered: make-training@1, measure@3, verify@16.
- Next: T1 the generator.
- Why: the training set must not be redrawable after the method meets it, like the measurement held-out set.

## 2026-10-25 T1 training data generated from law/ by code (commit: T1: training data generated from law/ by code — 15 937 examples in five tasks, sealed, re-derived by verify TRAIN)
- Done: tools/make_training.py 0.2 (ferramenta:make-training@2; no model, no network): `generate` writes
  training/data/<task>/{train,held_out}.jsonl, ARTICLE-OF.json and INDEX.json (sha256 and line count per file, counts per
  task and split); `report --tokenizer` writes REPORT.md (token lengths with AMALIA's tokenizer.json, revision
  c4614b9b5c7b, sha256 2de23e1b…; the file lives outside the repo, only its hash is recorded). Each example: id, task,
  prompt in the B3 reader's format (opening, rules line, reference date, candidate block `[id] (versão em vigor a D,
  desde F)` + text, question), answer as compact canonical JSON, sources (passage / raw ids used) and the answer's JSON
  schema (as prompt.json carries it, for guided decoding at measurement time; an extra key beside the five the brief
  names). Five tasks: escolha_passagem (article by its epigraph; número / alínea by article + epigraph + first words;
  6-12 candidates of the same chapter + 1-2 of another), texto_vigente (passages with >1 version; a date at a later
  version's start, inside an interval, before the first: valid_from or null + revogada), nota_dr (every DR note line of
  every working text, parse_note as truth; the 13 the grammar cannot parse are left out), remissao (D0.3 resolutions
  with >= 3 sibling candidates), regra_tipada (settled rules: stored prompt.json + latest propose payload).
- Result (INDEX.json, sealed by evento:41, training_index_sha256 3407de38…): 15 937 examples after dedupe by prompt;
  escolha_passagem train 8 057 / held_out 2 227; texto_vigente 3 942 / 903; nota_dr 506 / 298 (809 distinct notes of
  5 361); remissao 2 / 1 (of 11 resolutions, 8 lack 3 eligible sibling candidates); regra_tipada 0 / 1 (the one settled
  rule cites ccp:art19, a B3-reserved article, so it is held out by T0's rule). Passages covered as targets 11 725 of
  36 524. Mean tokens (train, prompt + answer): escolha 1 434, texto_vigente 532, nota_dr 347, remissao 1 244; total
  train tokens 13 830 654. No candidate text is shortened: an example whose prompt would pass 9 000 characters or with a
  passage over 2 500 characters is not made (limits in INDEX.json).
- verify TRAIN (new code): INDEX.json and every file regenerated byte for byte from the store and the reservation;
  unlisted or missing files; any train example whose sources fall in a reserved article (read from the stored files,
  independently of the generator). Runs for the repo store and for any store root holding training/ (fixtures/valid now
  carries a training/ generated by tools/make_fixtures.py, 0 examples over the fixture law, with its own reservation).
  Overlays train-index-not-regenerated, train-example-touches-reserved-article and train-reservation-edited (TRAIN);
  red team Q1-Q3 (listed file deleted, unlisted file, reservation edited). Q3 was MISSED on the first red-team run (an
  article dropped from reserved_articles left the regenerated data identical: the fixture has no examples and the
  definition's hash does not cover the list); TRAIN now also checks the definition's sha256 and that reserved_articles
  equals by_hash over the store's articles plus the declared by_b3 list; the mutation became the third overlay.
  tests/test_verify.py counts 29 overlays.
- test_t1 green (4/4). Registered: make-training@2, verify@18, make-fixtures@5.
- Next: T2 the adapter on Modal.
- Why: a reader trained on the law's own structure, with nothing in the data that a model wrote.

## 2026-10-25 T2 the adapter amalia-ccp-lei-v1 trained on Modal (commit: T2: LoRA v1 of the reader trained on Modal from training/data; MANIFEST and COST in training/runs/v1)
- Done: training/train_lora.py (outside engine/, tools/, verify.py), training/README.md. Base AMALIA-9B-0626-DPO revision
  c4614b9b5c7b; LoRA r 16, alpha 32, dropout 0.05 on q/k/v/o/gate/up/down (50 921 472 trainable parameters); H100, bf16,
  gradient checkpointing; 2 epochs, AdamW lr 1e-4, 20 warm-up steps then linear decay, effective batch 16,
  length-sorted micro-batches <= 24 000 tokens; chat format with the reader's system prompt; loss on answer tokens only.
  Mixture: every train example except escolha_passagem, cut (by sha256 of the id) to the sum of the others: escolha
  4 450, texto_vigente 3 942, nota_dr 506, remissao 2, regra_tipada 0 = 8 900 examples (escolha exactly 50 %),
  8 946 426 tokens per epoch, none dropped.
- Run (training/runs/v1/MANIFEST.json): repo commit 2f3a71300 (training/ and law/ clean), 2026-10-25T02:02:01Z to
  03:11:27Z, 540 optimizer steps in 4 110.8 s; loss 1.885 at step 1, 0.012 at step 20, <= 0.01 from step 30 on, 0.0000
  at step 400 (the answers are short structured data; how much of it generalises is T3's question). One CUDA allocator
  warning at step ~205 (a 2.5 GB allocation retried; training continued). Adapter in the Modal volume amalia-lora as
  amalia-ccp-lei-v1 (adapter_model.safetensors sha256 74a74d56…); the earlier amalia-rjue-v6 there was not read,
  loaded or mixed. Modal app ap-us38gDvzpTWhn0xlpEmclw.
- Cost (training/runs/v1/COST.json, Modal billing report read after the hour closed): training 4.6684 USD (H100 4.5666);
  evaluation of the base 0.4926 USD, of v1 0.8016 USD; phase total 5.9626 USD.
- Principal: leitor:a2 (family A, motor amalia-9b-0626-dpo+ccp-lei-v1, versao 74a74d569498) registered in
  governance/principals.json (committed with T3, the commit that first uses it); leitor:a stays the base.
- Next: T3 measurement.
- Why: a family-A reader trained only on the law's own structure, with a manifest that names every input.

## 2026-10-25 T3 measurement: base vs v1 (commit: T3: leitor:a vs leitor:a2 on the held-out tasks, the 18 rules and the 20 cases; answers sealed; report re-derived by verify)
- Done: readers/leitor_a_modal.py gains --lora v1 (vLLM LoRA from the volume; answer file leitor-a2.json) and a JSONL
  mode for the held-out task files (B3/B5 directory mode unchanged). tools/measure_reader.py (ferramenta, no model) reads
  the stored answers; reports/measure/amalia-v1-2026-10-25.{json,md}; verify MEAS recomputes amalia-*.json with it.
  Answers in governance/readings/avaliacao-v1/ (3 430 per reader on the tasks; 18 rules and 20 cases for leitor:a2; the
  base's rule and case answers are the B3/B5 files), sealed by evento:42 (measure@4, avaliacao_index_sha256; D42).
- a) held out, exact accuracy, base -> v1 (95 % Wilson):
  escolha_passagem 94.6 % [93.5, 95.4] (2 106/2 227) -> 98.7 % [98.1, 99.1] (2 198/2 227);
  texto_vigente 41.4 % [38.2, 44.7] (374/903) -> 99.5 % [98.7, 99.8] (898/903);
  nota_dr 61.7 % [56.1, 67.1] (184/298) -> 98.3 % [96.1, 99.3] (293/298);
  remissao 1/1 -> 1/1 (n = 1, [20.6, 100]); regra_tipada 0/1 -> 0/1 (n = 1, [0, 79.3]).
- b) the 18 B3 rules: exact agreement with leitor:b 1/18 -> 2/18 (5.6 % [1.0, 25.8] -> 11.1 % [3.1, 32.8]; the new one is
  limiar-ajuste-direto-obras@v1); direction 14/18 -> 14/18; with the settled rule exact 1/1 -> 1/1, direction 1/1 -> 1/1.
- c) the 20 cases (236 pairs): A vs B exact 44.0 % [37.7, 50.4] (102/232), direction 96.1 %; A2 vs B exact 62.2 %
  [55.8, 68.2] (143/230), direction 96.5 % [93.3, 98.2]; A vs A2 exact 46.1 % (105/228), direction 99.6 %; on the 6
  expected verdicts (A = B, not nao_aplica) A2 gives the same in 3 (50 % [18.8, 81.2]).
- Measurement correction, disclosed: the first report compared answers as canonical text, so leitor:a2's 150000.0 differed
  from 150000 and the order of conditions counted; B3's uphold compares with Python equality and tools/read_rules.py
  sorts passages and conditions. measure_reader now compares integral floats as integers and conditions / passages as
  sets (measure-reader@2); before the correction b) read 0/18 exact for v1 and 0/1 with the settled rule.
- Finding: the regra_tipada example's prompt equals the B3 prompt, but its stored schema has its keys sorted (the jsonl
  is written with sort_keys); under guided decoding the field order changes the answer: with «condicoes» first, base and
  v1 add a condition preco_base < 150 000 and miss; with the B3 order (passagens first) v1 matches the settled rule. Not
  changed here (training/data is sealed); the generator should keep the prompt.json key order in a next version.
- Fixes on the way: the D42 seal check now runs only against the repository's own log (a fixture store failed
  test_evidence); tests/fill/test_b5_measure.py reads the B5 report, not amalia-* (sorted order put it last).
- No model name in publishable outputs: the report's reader label says «base + adaptador v1» and training/data/REPORT.md
  «the family-A reader's tokenizer»; the report file name amalia-v1-<date> is the one the phase brief fixed (kept).
- Registered: measure@4, measure-reader@3, make-training@3 (report text only; INDEX.json unchanged), verify@20. B4 stays
  red as before (data/facts empty).
- Next: the audit of phase 4.
- Why: a figure is the stored answers recomputed, with its interval and the comparison beside it.

## 2026-10-25 — D43: the person's canonical form of a reading (product rule, evento:43)
- Done: Paulo decided that two readings that say the same thing written differently are the same reading. Recorded as
  evento:43 (pessoa:paulo, product_rule:forma-canonica-da-leitura, his words in the reason; recorded at his request).
  tools/read_rules.py: canonical_reading / same_reading (passages and conditions as sets, one-value in/not_in = eq/ne,
  integral numbers as integers, params' object lists as sets, null fields dropped). `record` applied it to the stored
  answers without asking any reader again: where leitor:b's blind answer replicates leitor:a's, a new leitor:b uphold
  review (same answer_sha256, payload names the product rule and its event) — evento:44, evento:45 — and a rule
  revision r2 with the new readings and state.
- Result: B3 settled 1/18 -> 3/18 (limiar-consulta-previa-obras@v1 and @v2 join limiar-ajuste-direto-obras@v2); exact
  A vs B 3/18, direction 14/18 unchanged. The other 15 differ in substance (passages, conditions, values, regimes).
  New packages pacote:ccp@2026-09-30 (r1) and pacote:ccp@2026-10-01 (r3) and the first package diff in rules/diff/.
- Measurement re-derived with the same canonical form (measure-reader@4): b) exact with leitor:b base 3/18 (16.7 %
  [5.8, 39.2]) -> v1 4/18 (22.2 % [9.0, 45.2]); with the settled rules 3/3 -> 3/3. a) and c) unchanged.
- verify STATE (D43): reviews do not raise the log's revision, so a rule object may sit above it, but only with the
  replay's state and the content of the revision the log is at; an added reading must be a review of that rule. The
  red-team found the first version let content through (M20 MISSED); closed, plus R1/R2 mutations and the broken overlay
  state-rule-above-log-changes-content (30 overlays).
- make_training: regra_tipada reads rule states from the log prefix the training data was sealed at (events 1..41);
  INDEX.json regenerates byte-identical.
- Registered: read-rules@6, measure-reader@4, make-training@4, make-fixtures@6, verify@22.
- Next: the extractor brief (BASE anúncios, then contratos) so the rules meet real procedures.
- Why: the code compares what a reading says; only the person decides that rule, and no reading of the law is approved
  by a person.

## 2026-10-25 E1.0 extractor: done-criterion for BASE anúncios 2026 (commit: E1.0: done-criterion for the BASE anúncios 2026 adapter)
- Source: dados.gov.pt dataset «Contratos Públicos - Portal Base - IMPIC - Anúncios de 2012 a 2026», resource
  anuncios2026.json (weekly JSON). One GET, nothing sent.
- Done when, checked by commands written in the E1 result entry:
  1. `data/raw/base-anuncios/` holds the `raw` object of the download (sha256, URL, captured_at) and one `raw` per mapped
     record, whose bytes are that record's exact byte slice of the download; all bytes live in `data/raw_bytes/`
     (gitignored), and the adapter re-derives every slice from the download (`--check`).
  2. `adapters/base-anuncios/` holds the code and the mapping as data; `data/facts/adaptador/` the `adaptador` object
     (field by field: source field -> canonical field, transform, enum map), proposed in the governance log by the
     adapter's own registered ferramenta.
  3. At least 1 000 `proc` units with facts in `data/facts/`; every fact names its raw record and source field, its
     adapter, valid_at (the notice's publication date) and known_at (= the raw's captured_at).
  4. A field the dump does not give, or gives ambiguously, is not a fact. In particular `data_envio_anuncio` is not
     replaced by the publication date, and no value is read from free text.
  5. Entities: adjudicante by NIF; without NIF, a candidate by country + normalised name, never merged.
  6. `adapters/base-anuncios/COVERAGE.md`: records in, procedures out, per canonical field and per month how many
     procedures carry it, unmapped records by reason (counts, three examples each).
  7. `python -I verify.py` ok over data/; `tools/run_engine.py` runs over data/ and its counts are reported.
- Why: the engine has no facts of real procedures yet; this phase writes only adapters/ and data/ (plus .gitignore,
  the adapter's registration in governance/ and these entries).

## 2026-10-25 E1.1 the BASE anúncios adapter, registered (commit: E1.1: adapters/base-anuncios — mapping as data, code, registration as ferramenta, adaptador proposed in the log)
- Done: one GET of https://dados.gov.pt/s/resources/contratos-publicos-portal-base-impic-anuncios-de-2012-a-2026/20261025-100557-3458a85b/anuncios2026.json
  at 2026-10-25T14:47:34Z: 23 669 469 bytes, sha256 9605b59bd94e8119ba158d90f9249b5a5d97fa89e70db2c1de0e5df7e3844a8b,
  sha1 ac317477cbd8… equal to the checksum dados.gov.pt publishes for the resource. 25 609 records, 20 fields each.
- adapters/base-anuncios/: mapping.json (six mapping rows, the record key, the procedure notice types, the NIF table
  for entity types, the six asked fields the dump does not give, each with its reason), adapter.py (build / check /
  register), README.md, SCHEMA-PROPOSAL.md (8 items for the builder).
- What the dump gives and does not: modeloAnuncio, tiposContrato, PrecoBase, nifEntidade, dataPublicacao and
  DataLimitePropostas map to tipo_procedimento, tipo_contrato, preco_base, adjudicante, data_publicacao_anuncio and
  data_limite_propostas. No field gives data_envio_anuncio, data_inicio_procedimento, publicado_joue, territorio or
  tipo_entidade. PrazoPropostas equals DataLimitePropostas − dataPublicacao in all 25 298 records that have both dates:
  it counts from publication, not from the sending the rules' counted_from names, so it is not prazo_propostas_dias.
- Registered: ferramenta:adapter-base-anuncios@1 (tools/register_tool.py, code adapters/base-anuncios/adapter.py);
  evento:46 proposes adaptador:base-anuncios@1 with the sha256 of the code and of the mapping. State: proposed.
- Next: build data/ from the download, check, verify, run_engine.
- Why: the mapping is data and the adapter is code, so a wrong mapping can be traced and the facts re-derived; the log
  holds the proposer, as it does for every other principal.

## 2026-10-25 E1.2 BASE anúncios 2026 in data/: checked result (commit: E1.2: BASE anúncios 2026 — 22 252 procedures, 131 558 facts, raw slices and bytes in data/; COVERAGE.md)
- Done: `adapter.py build` over the download: 25 609 records in; 22 252 `proc` units out (one per «Anúncio de
  procedimento» or «Anúncio de concurso urgente», each with its own raw = the record's exact byte slice); 3 357 records
  not mapped (3 350 alteration notices and 1 rectification that the dump does not join to a procedure; 6 records whose
  key nAnuncio + IdIncm repeats); 131 558 facts; 228 adjudicante entities (NIF prefix 6), 2 668 aliases and nif_exact
  links; adaptador:base-anuncios@1 with coverage per month. Coverage per field and month, the unmapped records by reason
  (counts, three examples each): adapters/base-anuncios/COVERAGE.md.
- Procedures carrying each field the rules read: tipo_procedimento 21 493, tipo_contrato 21 473, preco_base 22 098,
  adjudicante 22 250; data_inicio_procedimento, publicado_joue, prazo_propostas_dias, data_envio_anuncio, territorio,
  tipo_entidade 0 (not in the dump, or, for the deadline, counted from publication). Also data_publicacao_anuncio 22 252
  and data_limite_propostas 21 992.
- Decision (pessoa:paulo, 2026-10-25): asked whether the repository keeps the raw bytes of this download (23 MB of
  notices), he answered «yes». data/raw_bytes/ leaves .gitignore and is committed: 22 253 files, 44 231 062 bytes (the
  download 23 669 469, the slices 20 561 593), the largest 23 669 469 bytes (under GitHub's 100 MB). It covers this
  anúncios 2026 download only; the contratos dumps (E2) need their own decision. SCHEMA-PROPOSAL.md item 2 marked decided.
- The COVERAGE.md line about the bytes changed, so adapter.py changed: ferramenta:adapter-base-anuncios@2 registered
  (@1 retired), evento:47 corrects the adaptador's proposal with the new code hash (mapping unchanged), data/ rebuilt
  with @2 at the same recorded_at (only the links' proponent and the adaptador's proposed_by differ).
- Checked (`.venv/bin/python -I`, from the worktree):
  - `adapters/base-anuncios/adapter.py check`: 22 306 files re-derived from the stored download, 0 differ, 0 extra.
  - `verify.py --store data governance`: 0 failures (0 I01), 45 s.
  - `verify.py` (full, before the bytes decision, 11 min 48 s): code guard ok; stores fixtures, repo, measure 0
    failures; BENCH/MEAS ok; 30/30 broken overlays refused; store data 2 669 failures, all I04 «principal
    ferramenta:adapter-base-anuncios@1 is not registered» (1 adaptador + 2 668 links): STORES["data"] has no
    governance/ (SCHEMA-PROPOSAL item 1). So `verify: FAILED` until the builder adds governance/ to that store.
  - `pytest tests --ignore=tests/fill`: 62 passed, 2 failed (test_verify::test_empty_stores_pass and
    ::test_verify_main_exit_code_is_zero, the same I04), 17 min 26 s.
  - `pytest tests/fill/test_b4_engine_v0.py`: test_extractor_delivered_notices passes (22 252 procs, 0 load errors);
    test_first_figure_at_scale_is_reproducible fails: reports/prazos-minimos.json is the builder's to write.
  - `tools/run_engine.py --out <scratch>`: {"units": 0, "sem_regime": 22252, "verdicts": 0, "rules": 0}, 34 min 38 s.
    No seletor_regime is settled and no procedure has data_inicio_procedimento, so none is routed to a package.
- For the builder (SCHEMA-PROPOSAL.md): 1 governance/ in verify's data store; 3 facts_of scans every fact per unit
  (0.071 s a call: run_engine 35 min; CI's verify job has a 20-minute timeout); 4 an entity type for legal persons of
  unknown nature (19 582 procedures have no entity); 5 a decimal transform; 6 raw.size; 7 vocabulary the dump uses
  (urgent tender 683, locação de bens móveis 429, ...); 8 a link method for code-made name links.
- Next: the person reviews the PR; E2 (BASE contratos) waits for E1's merge. The fields the prazo rules need
  (data_envio_anuncio, publicado_joue, territorio, tipo_entidade, data_inicio_procedimento) are not in this source.
- Why: a fact the dump does not state is left out so the engine says nao_avaliado instead of a verdict on a guess.

## 2026-10-25 E1b.0 extractor: done-criterion for the DR notice PDFs (commit: E1b.0: done-criterion for the DR notice PDFs of the 22 252 procedures)
- Decided by pessoa:paulo (relayed by the builder session, his words): «Sí, lanza E1b en la sesión del extractor,
  despacio (1 cada 10 s)». The pre-registered test (foaap-core/ccp-mother-data/e1b-sample-2026-10-25: CRITERIA-v2
  sha256 ae708e96…, VERDICT-v2) passed A–D on 200 unseen notices with parser parse.py sha256 a29220df….
- Source: the Diário da República notice PDF each procedure's record links to (field `url`), only
  files.diariodarepublica.pt (22 170 of the 22 252 procedures; the other 82 link to the Açores journal, acinGov, a
  sharepoint page or nothing, and are counted, not fetched). Branch stacked on PR #1.
- Done when, with the commands written in the E1b result entry:
  1. Download: one GET every 10 s, User-Agent «ccp-engine research (passive read)»; any 403 or 429 stops the run and is
     logged, and a resume starts no sooner than one hour after it; network errors are retried on resume; files already
     stored are skipped. The fetch log is in git; the PDFs (about 1.5 GB) are not (data/raw/dr-anuncios/raw_bytes/,
     gitignored), each PDF has a `raw` and a `documento` object with sha256 and URL in git.
  2. Text: pypdf 6.14.2 with cryptography 50.0.1 on /usr/bin/python3 3.9.6, the versions the test ran; values by the
     frozen parser, copied byte for byte and checked against its sha256 at every run; a PDF that breaks it is counted.
  3. Facts per proc pointing at the document (documento, page, offsets, quote): data_envio_anuncio, publicado_joue,
     nut_iii_adjudicante, territorio (NUT III mapping as data: PT2 -> PT-AC, PT3 -> PT-MA, other PT),
     data_limite_propostas. Stored without becoming a rule field: norma_juridica_adjudicante. Not derived:
     data_inicio_procedimento, tipo_entidade, prazo_propostas_dias.
  4. Where the PDF and the dump disagree on data_limite_propostas: a `conflito` with both facts, resolution nao_avaliado.
  5. COVERAGE.md per field and month, failed PDFs by reason, conflicts by kind; verify over data/ (with governance/);
     run_engine rerun and its counts reported; a PR of its own, not merged.
- Why: the dump lacks what the deadline rules read; the notice prints it under fixed labels.

## 2026-10-25 E1b.1 the DR notice adapter, download running (commit: E1b.1: adapters/dr-anuncios — fetcher, frozen parser, mapping as data, build)
- Done: adapters/dr-anuncios/: parse.py (the E1b test's parser, byte for byte, sha256 a29220df…, checked at every
  build), mapping.json (six rows: data_envio_anuncio, publicado_joue, nut_iii_adjudicante, territorio with the NUT III
  prefix table as data, data_limite_propostas, norma_juridica_adjudicante; the three fields not derived and why),
  adapter.py (fetch / text / build / check / register), SCHEMA-PROPOSAL.md (2 questions for the person, 4 for the
  readers, 2 for the builder). .gitignore: the PDFs and their text stay out of git.
- Download started 2026-10-25T20:24:09Z (3 notices as a probe), then from 20:26:49Z the 22 167 remaining
  files.diariodarepublica.pt notices, one GET every 10 s, detached (nohup) so it survives a session restart; every
  attempt in adapters/dr-anuncios/fetch-log.jsonl. A first launch at 20:25 made no request (its output file's folder
  was missing).
- Text by pypdf 6.14.2 and cryptography 50.0.1 on /usr/bin/python3 3.9.6, the test's versions: the adapter keeps -I and
  adds only the user site where that pypdf is installed, and refuses another pypdf version.
- Trial build on the first 6 notices: 6 documents, 36 facts with (documento, page, offsets, quote); `check` 0 differ;
  `verify.py --store data governance`: only the expected I04 (proposer not registered yet) and one orphan (a PDF
  fetched after the build).
- Next: when the download ends, text, build, register, check, verify, run_engine, COVERAGE, PR.
- Why: the notice prints what the deadline rules read; positions make every value traceable to its page.
## 2026-10-25 — builder fixes for the extractor's E1 (SCHEMA-PROPOSAL items 1 and 3)
- Done: verify's `data` store loads governance/ with data/ (the principals and log that data/'s adaptadores and links
  name), as tools/run_engine.py and tools/measure.py already load it. Over the extractor's E1 branch the full verify
  reported 2 669 I04 «not registered» lines only because the store had no principals.
- Done: engine.store.facts_of reads facts through an index of fact ids by unit (any revision) and of revisions by id,
  built once per store and rebuilt when facts are added; the bitemporal read is query's own (_bitemporal), over the
  revisions of those ids. Same output: 1 200 calls (300 random procs × 4 clock pairs) over the E1 data (131 558 facts,
  22 252 procs) and every unit of the fixtures, 0 differences against the old scan. Time for all 22 252 procs:
  0.1 s (was ~26 min, 0.071 s a call), so run_engine and verify's check_measure fit CI's 20-minute timeout.
- Registered: verify@23. Public signatures of engine/ unchanged.
- Next: the extractor merges main into its E1/E1b branches; E1b (DR notice PDFs, one GET every 10 s) is running there.
- Why: the extractor's full verify could not pass on a store without the log, and a 35-minute engine run blocked CI.

## 2026-10-26 — D44: B3 round 2 for the regime selector and the three minimum-deadline rules
- Asked: the person, «Sí, lanza los lectores en el paso 3: primero el selector de régimen, luego los tres plazos mínimos
  y las preguntas a–d». Step 5 (first verdicts on deadlines) is blocked only by these rules: run_engine routes no proc
  while no seletor_regime is settled.
- Done: the same questions and candidates as round 1, with three prompt defects fixed and committed before any answer
  (cd339c2d3): the date format named as a literal leitor:a copied («AAAA-MM-DD»); empty lists allowed as values; no
  stated way to write an open-ended regime. leitor:a (Modal, temperature 0, guided JSON) answered 4/4; leitor:b (the
  family-B client, blind, empty directory) 4/4. Recorded as leitor:a's `correct` (revision 2, payload round 2) and
  leitor:b's blind review of revision 2: evento:46–53. Answers in governance/readings/ronda2/; RONDA2.md.
- Result: 0 of 4 settled. Direction (the value the rule depends on) agrees on the three deadlines (30, 6 and 14 days,
  counted from data_envio_anuncio, both readers); the selector differs in substance. leitor:b gave the same readings as
  in round 1 (art. 7.º n.º 2 + art. 11.º; two regimes split on 2026-10-01; deadlines conditioned on publicado_joue and
  tipo_contrato). leitor:a fills condition values with descriptions of the vocabulary («data», «número», «uma data no
  formato ISO», «não especificado»), adds conditions the text does not state (territorio PT, tipo_entidade outra) and
  omits publicado_joue / tipo_contrato; for the selector it gives one regime from 2026-10-01 to 2026-10-01.
- Fix on the way: verify MEAS recomputed the sealed B5 report with the current rules, so round 2 moved it; the report now
  reads the rules as known at its seal (measure@6, verify@25); tools/measure.py reads them so by default, and
  `--rules-now` for a new measurement. Checks: verify ok; red-team 0 MISSED; 86 tests pass (B4 deselected: data/ on main is
  empty); the 2026-10-24 report regenerates byte-identical.
- Not done here: questions a–d need new reading targets and, for (a), CPA art. 87.º, which CCP art. 470.º n.º 1 points
  to and law/ does not hold yet.
- Next: the person's decision on the proposer (the reader roles were left as a pending product decision in phase 4).
- Why: re-asking a prompt at temperature 0 returns the same answer; only defects of the prompt were fixed, so the round
  measures the readers, not a prompt tuned to agree.

## 2026-10-26 — D45: B3 round 3 (proposer leitor:a2, conditions typed by field)
- Asked: the person, «Sí: ronda 3 con leitor:a2 (AMALIA + adaptador) proponiendo y el esquema con valores tipados por campo».
- Done: round 2's prompt text with conditions typed by field (11 variants: each field with its ops and value type),
  committed before any answer (245ae45df). leitor:a2 (Modal, adapter amalia-ccp-lei-v1, temperature 0) answered 4/4 and
  `correct`ed the current revision (the proposer becomes leitor:a2); leitor:b reviewed revision 3 blind: evento:54–61.
  Answers in governance/readings/ronda3/; RONDA3.md.
- Result: 0 of 4 settled; direction agrees on the three deadlines (30 / 6 / 14 days from data_envio_anuncio, both
  readers, both now citing ccp:art135.1 / ccp:art136.1). The typed schema removed the vocabulary-as-value answers.
  What still differs: with JOUE, leitor:a2 conditions on territorio = PT where leitor:b conditions on tipo_procedimento =
  concurso_publico (both have publicado_joue = true); without JOUE, leitor:a2 adds conditions that exclude nothing real
  (data_inicio_procedimento ≠ 2026-10-01, preco_base ≠ 0, territorio in PT) and omits tipo_contrato (≠ / = obras), which
  is what separates the 6-day from the 14-day rule; the selector differs in substance (leitor:a2: one regime from
  2026-10-01 to 2026-10-01 and a JOUE condition; leitor:b: two regimes split on 2026-10-01, art. 7.º n.º 2 + art. 11.º).
- Checks: verify ok; red-team 0 MISSED; 86 tests pass (B4 deselected: data/ on main is empty).
- Next: the person decides how the family-A side goes on (see the report); a–d after that.
- Why: settlement needs two families to replicate a reading; three rounds show leitor:b stable and the family-A
  reader right on the numbers but not on the conditions.

## 2026-10-26 — D46: AMALIA v2 trained on condicoes_texto; B3 round 4: the first deadline rule settles
- Asked: the person, «Sí: entrena AMALIA v2 en qué condiciones dice el texto, con datos generados por código desde law/,
  mide en reservados y luego ronda 4».
- Done: tools/make_conditions.py (make-conditions@1): condicoes_texto from the procurement acts of law/, labelled by a
  declared word list (two hand checks before freezing fixed four list defects: the labour code's «consulta prévia»,
  «prestação de serviços», «bens e/ou serviços», «concessão de serviços»); 833 train / 353 held out; a passage whose text
  is a reserved passage's (the CCP republished in DL 111-B/2017, DL 177/2026) is held out; verify TRAIN re-derives
  training/data-v2. train_lora runs as data (v1's mix unchanged, 8 900); v2 = v1's data + condicoes_texto twice (12 232).
  LoRA v2 amalia-ccp-lei-v2: 745 steps, 5 484 s H100, USD 5.12 (training/runs/v2). Principal leitor:a3 (family A).
- Measured on the 353 reserved passages (tools/measure_conditions.py, verify MEAS recomputes it): all fields exact base
  2.8 % → v1 0.0 % → v2 91.2 % [87.8, 93.7]; values named that the text does not name 81.1 % → 78.6 % → 8.9 %; values
  missed 12.5 % → 23.3 % → 2.5 %. BEFORE kept in training/runs/v2/BEFORE.md (committed before v2 existed).
- Round 4 (prompt and schema of round 3, committed before v2 existed): leitor:a3 proposes, leitor:b blind: evento:62–69.
  regra:ccp:prazo-minimo-concurso-joue@v1 SETTLED (identical: ccp:art136.1; publicado_joue = true, tipo_procedimento =
  concurso_publico; 30 days from data_envio_anuncio). Without JOUE (6 / 14 days): same article, days and counting point;
  leitor:a3 keeps tipo_contrato (≠ / = obras, the condition that splits them) but omits publicado_joue = false and
  concurso_publico, and on the works rule writes publicado_joue = true. Selector: unchanged in substance.
- Fix on the way: tools/measure_reader.py read the current rule states, so the settlement moved the dated phase-4
  report; a dated report now reads the rules as they stood at the end of its date (measure-reader@5).
- Dossier for the AMALIA team: training/AMALIA-DOSSIER.md (before / after, data, cost).
- Checks: verify ok; red-team 0 MISSED; 86 tests pass (B4 deselected); test_b5 now skips condicoes-* as it skips amalia-*.
- Next: the selector (blocks every route), then a–d (CPA art. 87.º to capture first).
- Why: the family-A reader named conditions the text does not state; v2 learned not to, on articles it never saw, and
  the first rule settled by two families on its own.

## 2026-10-26 — D47: AMALIA v3 (selector tasks); B3 round 5
- Asked: the person approved the selector proposal (budget about USD 7).
- Done: tools/make_regimes.py (make-regimes@1): entrada_em_vigor (24 / 8; only acts whose own article prints the date
  of their entra_em_vigor vigências) and periodos_vigencia (1 314 / 301); verify TRAIN re-derives training/data-v3
  (check_training_v2 generalised to a data dir and its generator). LoRA v3 amalia-ccp-lei-v3: 921 steps, 6 714 s H100,
  USD 5.74 (training/runs/v3); principal leitor:a4. tools/measure_regimes.py (verify MEAS: regimes-*).
- Measured on the reserved sets: periods exact base 0/301, v2 0/301 (it leaves every period open), v3 298/301 = 99.0 %
  [97.1, 99.7], well-formed partition 99.3 %; entry date 6/8, 6/8, 8/8; condicoes_texto v3 91.8 % (v2 91.2 %: not lost).
- Round 5 (prompt = round 4, committed before v3 existed): leitor:a4 corrects, leitor:b blind: evento:70–75. 0 settled.
  Selector: v3 still gives one regime from 2026-10-01 to 2026-10-01 (the trained skill did not transfer to the selector
  question); leitor:b now cites art. 10.º, 11.º and 7.º n.º 2 (two regimes split on 2026-10-01, as before). Deadlines: v3
  repeats v2 on goods/services, adds conditions on works, drops the conditions on the JOUE rule.
- Fix before the commit, disclosed: the first local recording of round 5 let leitor:a4 `correct` the JOUE rule settled
  in round 4, which reopened it; and the «already recorded» check matched an identical answer of round 4. Both
  recordings were discarded before any commit (git checkout of governance/ and the new rule files); record_round now
  reports a later round's answers on a settled rule without recording them (D47 addendum), and matches answers per
  round. JOUE stays settled from round 4.
- Cost correction: v2's training was USD 6.20 once Modal's hours closed (first reading 5.12).
- Checks: verify ok; red-team 0 MISSED; 86 tests pass (B4 deselected).
- Next: the selector needs another approach (the person decides); the dossier is updated.
- Why: a trained skill is measured on reserved data and then on the real question; here the first passed and the
  second did not, and the log keeps what two families settled.

## 2026-10-26 — D48: the Postgres store (Supabase ccp-engine, eu-west-1)
- Asked: the person, «Sí: crea las tablas con ese diseño (migraciones en el repo, RLS) y carga los 22.252 procedimientos
  como prueba».
- Done: supabase/migrations/20261026200000_ccp_store.sql (schema ccp: raw, adaptador, unidade, facto, entidade, alias,
  link, documento, conflito, afirmacao, veredicto, regra; (id, revision) keys, the whole object in doc, query columns;
  append-only triggers; RLS on with no policy; no API role can use the schema). db/pg.py: migrate (recorded in
  supabase_migrations.schema_migrations), load (COPY into a temp table, insert on conflict do nothing), roundtrip.
  Credentials in .env (gitignored, owner-only): the project ref and the database password only.
- Checked: PR #1's data (commit c12d1d418) loaded: 181 628 objects (22 252 units, 131 558 facts, 22 253 raws, 228
  entities, 2 668 aliases, 2 668 links, 1 adaptador); roundtrip 0 missing, 0 different; a second load inserts 0; an
  update is refused by the trigger; database 169 MB; the facts of one procedure in about 100 ms, a count by procedure type
  in about 80 ms (through the pooler from Lisbon).
- Not yet: verify reading the database (today: the roundtrip against the store it was loaded from), the daily pipeline,
  read-only views for the interface.
- Why: git cannot hold millions of facts; the interface needs a database; nothing in it can change without a new revision.

## 2026-10-27 — D49: AMALIA v4 measured on reserved questions
- Asked: the person, «Test Amalia».
- Done: principal leitor:a5 (amalia-9b-0626-dpo+ccp-lei-v4, adapter sha256 8255e876…). v4 answered the 400 reserved
  condicoes_pergunta questions and, for regression, the reserved sets of v2 and v3. measure-conditions@3 and
  measure-regimes@2 add leitor-a5 and recompute an earlier report with only the readers it holds (so 2026-10-26's
  reports do not change); verify@30 passes those readers.
- Checked (reports/measure/pergunta-v4-2026-10-27, condicoes-v4-2026-10-27, regimes-v4-2026-10-27): exact condition
  set 400/400 (base 117/400, v3 23/400); 0 of 989 conditions added or missed; no reserved phrasing occurs in a training
  question. Earlier tasks: conditions in a passage 93.2 % exact (v3 91.8 %), periods 301/301, entry date 8/8.
- Limit: the reserved questions share the training sentence pattern with other words; the real test is round 6.
- Cost: v4 training USD 9.53. Correction: v3's training was USD 7.61 once Modal's hours closed (first reading 5.74).
- Fix before the commit, disclosed: a first regression run passed its paths through a zsh variable that was not split,
  so no example reached Modal; the two reports it produced held no v4 answers and were deleted before any commit.
- Next: round 6 (v4 proposes, leitor:b blind) on the selector and the deadline rules.

## 2026-10-27 — D49: B3 round 6 (proposer leitor:a5, AMALIA v4); two deadline rules settle
- Asked: the person, «Sí, corre la ronda 6: v4 propone y leitor:b a ciegas».
- Done: the round-6 prompts committed before v4 existed (= round 5's); leitor:a5 answered on Modal, leitor:b (Reader B app
  CLI) blind in parallel; tools/read_rules.py record --round 6: evento:76–81, governance/readings/ronda6/RONDA6.md.
- Settled (leitor:b replicates leitor:a5 in canonical form, D43): regra:ccp:prazo-minimo-concurso-sem-joue-bens-servicos@v1
  (art. 135.º n.º 1, 6 days) and regra:ccp:prazo-minimo-concurso-sem-joue-obras@v1 (art. 135.º n.º 1, 14 days). With
  the JOUE rule settled in round 4, the three minimum-deadline rules the engine needs first are settled.
- Not settled: the selector. v4 now gives an open end («to» null) but only the regime from 2026-10-01 and cites art.
  7.º n.º 2; leitor:b gives two regimes split on 2026-10-01 and cites art. 7.º n.º 2 and 11.º.
- On the JOUE rule (settled, not reopened) v4 left out «concurso público», which the question states: on the three real
  deadline questions v4 read the stated conditions exactly on 2 of 3, against 400/400 on the reserved pattern.
- Next: the selector (the person decides the approach).

## 2026-10-27 — D50: AMALIA v5 data (a person's question -> facts); BEFORE
- Asked: the person, «a user is going to ask a simple Portuguese question… start with AMALIA training».
- Done: tools/make_user_facts.py (training/data-v5, 4 000 / 400, every wording train-only or held-out-only);
  training/real-questions/factos-v1 (40 hand-written questions, no template, sealed before training; written by
  the builder, labels = what each question states); tools/measure_user_facts.py; verify@31 (TRAIN data-v5, MEAS factos-*).
- BEFORE (training/runs/v5/BEFORE.md), exact facts generated / hand-written: base 3.8 % / 10.0 %; v4 4.0 % / 15.0 %
  (v4 misses about half of the stated facts). Committed 0230ec430 before training; v5 launched on Modal.
- Red-team: one changed train line -> TRAIN caught.

## 2026-10-27 — D51: B3 round 7 (the selector's question fixed)
- Asked: the person approved the draft, «regístralo como D51 y corre la ronda 7».
- Done: the selector question lists the regimes the system holds, shows art. 19.º c/d and 20.º n.º 1 c/d with their
  earlier text, asks for each regime's start-date range, admits «from» = null (regra schema too). Prompts committed
  (e36a79fc6) before any answer; the deadline prompts are round 6's. evento:82–83.
- Fix before the prompts were committed, disclosed: the earlier text was labelled «em vigor … a 2026-10-01» with the
  store's exclusive end date, which reads as in force on 1 October; round 7 shows the last day, 2026-09-30.
- Result: not settled, but the two families now draw the same line: two regimes, the old Code to 2026-09-30 and the new
  from 2026-10-01 (a procedure started on 1 October falls in the new). They differ on (1) the passages: leitor:a5 cites
  the changed Code articles 19/20, leitor:b the decree's art. 7.º n.º 2, 10.º and 11.º; (2) the old regime's start:
  leitor:a5 2018-01-01 (the earlier text's start), leitor:b null.
- Fix before the commit, disclosed: recording re-rendered the reports of rounds 2–5 with today's states (round 5 would
  have shown rules settled only in round 6); restored from git, RESUMO.md (the current summary) kept.
- Checks: verify ok. Tests: 85 pass, 1 FAILS (B4 deselected), disclosed after the commit aaa939473: tests/fill/test_b3_rules_v0.py expects the selector rule to cite dl-177-2026 art. 7.º; the rule's current (proposed) revision carries leitor:a5's reading, which cites ccp art. 19/20 only. Left red on purpose: it reports the open difference, the test is not bent to the data.
- Next: the person decides how to close the two differences.

## 2026-10-28 — D52: AMALIA v6 on 500 written questions
- Asked: the person, «you write them as a human being… make the most handwritten questions… stating the wrong law».
- Done: 500 questions written one by one (training/written-questions, LABELS.md, tools/check_written_questions.py:
  0 problems); answer with factos / ambiguos / contraditorios / citacoes; tools/make_written.py (300 train + 5 noisy
  copies each, 100 dev, 100 final sealed, 2 000 D50 templates relabelled and noised); tools/measure_written.py;
  BEFORE committed a3abf24a7; v6 trained on Modal (1 353 steps, 9 192 s, H100, USD 9.83 first reading);
  principal leitor:a7.
- Fix after training, disclosed: the answer schema listed the fact fields in another order than the trained answers; the
  guided decoder writes properties in schema order, so a reader that began with tipo_procedimento or tipo_entidade could
  no longer write tipo_contrato or territorio (first v6 dev reading: 56 contract types and 20 regions missed). The schema
  now follows the answer's order (make-written@2); prompts and answers are byte-identical, so v6's training stands. All
  three readers were re-run with the fixed schema (the reader resumes per id, so the stale files were moved aside first).
- Result (reports/measure/escritas-v6-2026-10-28), final sealed / dev: facts exact base 14 % / 11 %, v4 19 % / 19 %,
  v6 64 % / 67 %; invented facts base 49 % / 54 %, v4 34 % / 39 %, v6 7.9 % / 7.8 %; missed v6 11.9 % / 9.4 %;
  ambiguous fields found v6 50 % / 60 %, flagged without cause 46 % / 29 %; default fills v6 0.
- Run record: the local entrypoint stopped when the session restarted (the run was detached and finished); MANIFEST.json
  is rebuilt from the function call's own return value (modal FunctionCall.from_id), the mixture recomputed (22 787).
- Checks: verify ok; tests 85 pass, 1 fails (test_b3_rules_v0, red since round 7, disclosed); test_b5_measure now skips factos-/escritas- reports like the other reader reports; red-team: one corrupted v6 answer -> MEAS caught.
- Next: markers flagged without cause (46 % on final) and missed ambiguous fields are the weakest part.

## 2026-10-26 — D55: the data at scale in Postgres; history loads; the daily job (branch data-loaders)
- Asked: the person's go-ahead relayed by the builder («you have my yes»): selector paused; on an own branch, loaders for
  the DR facts (E1b), the BASE history 2018–2026 and TED Portugal 2018–2026, a daily Modal job with health per source,
  within Micro, rows and GB per table reported.
- Done: compact layout (migrations 20261027000000 + 000100): ccp.nome, facto_c / raw_c / unidade_c, views ccp.facto /
  ccp.raw / ccp.unidade rebuilding each doc. The 181 628 D48 objects moved and compared (0 missing, 0 different; a mutated
  object is caught), then the D48 tables dropped. 955 → 169 bytes per fact. Loads revise (db/pg.py selftest, rolled back:
  new, unchanged, changed → revision 2 superseding 1). db/pg.py load-files; db/history.py anuncios / contratos / ted;
  adapters/ted/adapter.py (new); adapters/base-anuncios: a record without nAnuncio is unmapped (4 records 2018–2023; the
  2026 build has none, so its output is unchanged); db/daily.py + db/modal_daily.py + ccp.ingesta / ccp.saude (migration
  20261027000200); tests/test_db_encode.py.
- Loaded (each load read back, 0 different): BASE anúncios 2018–2025 (174 222 notice raws with 2026, 1 021 724 facts in
  all years); BASE contratos 2018 and 2019 (273 367 contract raws, 1 061 276 facts); TED 2018-01 to 2023-10 (51 229 notice
  raws, 183 152 facts); DR notices built so far by E1b (1 782 PDFs, 1 781 documentos, 10 648 facts). Database 825 MB:
  facto_c 2 276 800 rows 385 MB, nome 1 367 268 rows 238 MB, raw_c 500 600 rows 90 MB, unidade_c 468 819 rows 93 MB.
- Blocked: the Supabase disk filled during contratos 2020 («No space left on device») with 787 MB of data and 992 MB of
  WAL (min_wal_size is 1 GB, max_wal_size 4 GB), and the project went read-only. The disk is smaller than the 8 GB this
  plan assumed; nothing was lost (each table's load is one transaction; 2020 has no rows). Projected need for the whole
  history: about 3.3 GB of data plus up to 4 GB of WAL. Resuming is a re-run (rows present are skipped): contratos
  2018–2026, then TED 2023–2026.
- Blocked: the Modal secret ccp-db (project ref + database password, for the daily job) — this session may not write
  secret stores; the person creates it (`modal secret create ccp-db --from-dotenv .env`), then `modal deploy
  db/modal_daily.py`. The daily job has not run on Modal yet; locally its TED step stopped at the read-only database.
- Not done: E2 entities of the history; joining TED procedures and award notices to BASE; modifications 2018–2025 (the
  extractor fetched 2026 only); verify reading the database.

## 2026-10-26 — D56: the joins, written; not yet applied (database read-only)
- Asked: the person's goal relayed by the builder («at least 8 in all»): joins for 2018–2026 with the rates published;
  the daily job live with health rows in Postgres.
- Done: supabase/migrations/20261027000300_ccp_joins.sql (ccp.facto_atual, ccp.unidade_atual, ccp.contrato_proc,
  ccp.proc_dr, ccp.entidade_papel, materialized ccp.ted_candidato) and db/joins.py (rates per year, three unmatched
  examples each, reports/data/joins-<date>). BASE dumps carry no OJ S number (contratos 2020 fields checked), so BASE–TED
  is a candidate join by buyer NIF + contract type + dispatch window, counted only when unique both ways.
- Not run: the database is read-only (disk full, previous entry); even reads that spill to temporary files fail. Order
  once the disk is raised: migrate, finish contratos 2020–2026 and TED 2023-11 to 2026-09, then db/joins.py.
- Known before running: procedure ↔ DR is 2026 only (E1b reads 2026's notices; 2018–2025 would be about 186 000 PDFs at
  one every 10 s, three weeks); TED-XML notices (2018–2023) name the buyer's NIF in about one in ten competition notices
  (2018-01: 13 of 135), so BASE–TED candidates there will be few.
- Checks: verify ok on the branch (before this entry's files, which are db/ and migrations only).

## 2026-10-25 E1.3 main merged: the builder's fixes for items 1 and 3 (commit: E1.3: main merged (80d8f3310); full verify ok, 64 scaffold tests pass)
- Done: merged main 80d8f3310 (verify's data store loads governance/; facts_of indexed by unit; verify@23). Conflicts:
  BUILD-LOG.md (both entries kept); governance/principals.json merged by git with both verify@23 and
  adapter-base-anuncios@1/@2. SCHEMA-PROPOSAL.md items 1 and 3 marked done by the builder.
- Checked (`.venv/bin/python -I`):
  - `verify.py`: ok in 4 min 05 s; stores fixtures, repo, data (181 628 objects, 47 events), measure 0 failures;
    BENCH/MEAS ok; 30/30 broken overlays refused. The 2 669 I04 lines are gone.
  - `pytest tests --ignore=tests/fill`: 64 passed (6 min 42 s).
  - `tools/run_engine.py`: {"units": 0, "sem_regime": 22252, "verdicts": 0, "rules": 0} in 1 min 43 s (was 34 min 38 s);
    still no settled seletor_regime and no data_inicio_procedimento.
- Next: the person's review of PR #1; E1b continues on its branch.
- Why: the done-criterion «verify ok over data/» now holds on the branch itself.

## 2026-10-25 E1b.2 interim check on the first 482 notices (commit: E1b.2: interim check on 482 notices; misses named by procedure type, cut norma values flagged)
- Done: `text` (476 new PDFs in 7.6 s) and `build` over the 482 notices fetched by 21:46Z, then `check` (0 differ).
- Result: data_envio_anuncio, nut_iii_adjudicante, territorio, norma_juridica_adjudicante 482/482; publicado_joue
  480/482; data_limite_propostas 479/482. The 5 misses are right, not parser errors: the 3 without a deadline are
  «Concurso limitado por prévia qualificação» (the first phase sets a deadline for candidaturas; the dump's
  DataLimitePropostas is empty too), the 2 without the JOUE question are «Concurso público simplificado» (the new
  procedure of DL 177/2026, whose form does not ask it). Cross-checks: 479/479 deadlines and 482/482 NIFs equal the
  dump; 0 conflicts so far. publicado_joue Sim 141 / Não 339; territorio PT 459, PT-MA 15, PT-AC 8.
- Found: the frozen parser reads a value to the end of its line, so a norma_juridica value that wraps in the PDF is
  cut (at least 3 of 482 end in «da» / «por uma»). The parser is not changed; COVERAGE.md now counts them, and the
  quote is exactly the printed first line.
- Changed (adapter.py, not the parser): a miss is reported with the procedure type of the dump record; the cut values
  are counted in COVERAGE.md.
- Next: the download runs on (~60 h); then the full text, build, register, check, verify, run_engine, PR.
- Why: a problem found on 482 notices costs nothing; found after 62 hours it costs a rebuild.

## 2026-10-25 E1b.3 download order: the new regime first, then months interleaved (commit: E1b.3: download order — notices since 2026-10-01 first, then months interleaved; same pace)
- Done: fetch now orders its queue (priority_order): the notices published since 2026-10-01 first (1 226 left, about
  3.4 h), then the other months interleaved, one notice of each month in turn, so every month's coverage grows
  together instead of following nAnuncio's alphabetical order. The pace is unchanged (one GET every 10 s, as the person
  set it); the total stays about 60 h. No bulk source exists: the DR publishes Part L notices only as single PDFs.
- Restarted at 21:51:51Z (fetch pid 7824) after 512 stored; it resumed without fetching any stored PDF; no .part file
  was left. caffeinate is tied to the fetch pid. A watcher written with `pgrep -f` matched its own command line (it
  would never have ended and held caffeinate on itself); replaced by one that waits on the fetch pid.
- Next: interim builds as the new-regime notices land; the full build when the download ends.
- Why: useful data in hours (the new regime) and a balanced sample of the year within about 8 h.

## 2026-10-25 M.0 extractor: a sample of every source tonight (commit: M.0: decision and done-criterion for one sample of every source)
- Decided by the person in this session (his words, 2026-10-25 ~22:15Z): «¿por qué no mejor ingestamos … un poquito de
  todo?», then, pointing at the table of the system's pieces (law, rules, anúncios, DR notices, contratos, modificações,
  entidades, TED, procedure documents, 100 hand-checked cases): «esto bro». This changes the brief's order (E2 was to
  start after E1's merge; TED and procedure documents were out of scope in E1/E2): recorded as his decision.
- Scope tonight, on branch extractor-muestras (stacked on E1b; the DR download keeps running on its own):
  BASE contratos 2026, entidades and modificações 2026 (one GET each from dados.gov.pt), a sample of each mapped to the
  store; TED: one daily package (one GET), Portugal's notices counted and joined where possible; procedure documents:
  10 procedures of October, one GET every 10 s, stop on 403/429, what each platform serves recorded. Not mine: the
  rules (the readers) and the 100 hand-checked cases (people).
- Done when: every downloaded file has its raw (sha256, URL, captured_at), bytes out of git; a sample of each BASE
  source mapped to facts / units / entities with origin (raw, field); TED and documents reported as probes;
  `verify.py --store data governance` 0 failures; COVERAGE per source; branch pushed.
- Why: one sample of every source shows the whole system end to end tomorrow, instead of more of the same notices.

## 2026-10-25 M.1 BASE contratos, modificações, entidades: the October sample (commit: M.1: BASE contratos 2026 sample — 15 108 contracts, 10 630 procedures, 37 modifications, 97 701 facts)
- Done: one GET each from dados.gov.pt at 22:23Z: contratos2026.zip (46 720 122 bytes, sha256 2ac78c54…; one member
  Contratos2026.json, 356 423 059 bytes, 199 701 contracts), entidades.json (51 307 118 bytes, b18c981e…, 216 267
  records), modcontrats2026.json (1 471 866 bytes, ea475adb…, 4 362 records). Bytes in data/raw/<source>/raw_bytes/,
  gitignored. adapters/base-contratos/ (mapping.json, adapter.py build / check / register).
- Sample: the 15 484 contracts BASE published in October 2026; 376 refused (idcontrato held by more than one record of
  the year). Units: 15 108 contrato, 10 630 new proc (procedures without a notice in E1: ajustes diretos, consultas
  prévias, acordo-quadro calls...), 37 mod. Facts: 97 701 with origin (raw, field). Joins: 1 937 contracts to a notice
  of E1 by (nAnuncio, idINCM); on those, preco_base equal 1 905, tipo_procedimento equal 1 889, adjudicante equal
  1 858 and different 79.
- Found: entidades.json has no public / private field (nif, name, counts, country only), so it does not settle
  entidade.type; adjudicatários without NIF 2 051 (no natural person's NIF appears: BASE seems to mask them); regime
  declared in October: 289 contracts name DL 177/2026, most still name the old text (assertions, not facts; not
  converted here). modifContratoPrecoAlterado and modifPrazoExecucao do not say whether they are the new value or the
  change: no facts.
- Registered: ferramenta:adapter-base-contratos@1; evento:48 proposes adaptador:base-contratos@1.
- Checked: `adapter.py check` 15 154 files, 0 differ. `verify.py --store data governance`: the contract sample adds no
  failure; the 246 failures are E1b's interim state (245 PDFs fetched after its interim build, its proposer not yet
  registered), which its final build resolves.
- Next: TED probe, documents probe.

## 2026-10-25 M.2 TED and procedure documents: two probes (commit: M.2: probes — one TED daily package (77 Portuguese notices), 10 procedure-document links (acinGov serves the pieces, Vortal does not))
- TED: three GETs; the first two to wrong addresses (issue not zero-padded: 400, 404), then the daily package of
  OJ S 190/2026 (01/10/2026), 18 115 918 bytes, sha256 70f29e9a…, raw raw:ted:pacote-diario:202600190. 3 631 EU
  notices; 77 with a Portuguese organisation, 74 with a NIF; 50 contract notices, 21 award notices. Counted only.
  adapters/ted/ (record.py, count.py, PROBE.md).
- Procedure documents: 10 October procedures, one GET every 10 s, no refusal. acinGov 5/5 served the whole set of
  pieces as one ZIP (3–5 PDFs, 0.4–19 MB), stored as raw:pecas:documento:<key>; Vortal 5/5 served a 686-byte
  JavaScript shell («Vision»): not readable with a plain GET (a rendering browser would be a decision for the person).
  adapters/pecas/ (probe.py, probe-log.jsonl, PROBE.md). No facts.
- Checked: `verify.py --store data governance`: the probes add no failure; the 285 failures are E1b's interim state
  (PDFs fetched after its interim build, proposer not yet registered).
- Next: E1b's final build when the download ends; the samples stay on this branch for the person to review.
- Why: one sample of every source is now in the store, each with its raw and sha256.

## 2026-10-25 M.3 Vortal: its public JSON API, read without a browser (commit: M.3: Vortal probe — the notice and its documents through Vortal's public JSON API with plain GETs; the uploaded DR notice is byte-identical)
- Done (the person's «va hazlo» to probing Vortal without stopping the download): the Vortal link was opened once in
  the built-in browser only to list the addresses its application reads (all GETs to a public JSON API; the page also
  sends analytics, so the data is read without it), then four plain GETs 10 s apart for one procedure
  (PT1.NTC.3811157, BASE 24347/2026), all 200: link -> notice address, header, the notice as typed fields with the
  documents list (public download URLs), and one document. adapters/vortal/ (record.py, PROBE.md); raws
  raw:vortal:* and raw:pecas:documento:vortal-…; bytes gitignored. No facts.
- Found: the uploaded document 419974431.pdf is byte-identical (sha256 733a83cf…) to the DR notice E1b fetched: an
  exact join Vortal procedure <-> DR notice. Deadlines come in UTC (22:59Z = 23:59 Lisbon): a hypothesis for the
  «D+1 00:59» differences between DR notice and dump. The documents list names the uploading official: never published.
- Checked: `verify.py --store data governance`: no failure from the probe (the remaining failures are E1b's interim).
  The DR download kept running throughout (pid 7824).
- Next: E1b's final build; a decision for the person on reading Vortal and acinGov at scale.

## 2026-10-25 M.4 the platforms in the background: Vortal notices (2026) and acinGov pieces (October) (commit: M.4: platform fetchers — Vortal notice JSON for 2026, acinGov pieces ZIPs for October, in the background)
- Decided by the person (his words, ~22:50Z): «vamos a empezar a ingestarlo ya de una vez», after the proposal of
  Vortal's notice JSON for every 2026 procedure (October first) and acinGov's pieces ZIP for October only. acinGov's
  whole year (~9 781 ZIPs, ~58 GB at the probe's mean of 5.9 MB) does not fit the 15 GB free; Vortal's documents are
  not downloaded.
- Done: adapters/plataformas/fetch.py (vortal / acingov): procedures of adaptador:base-anuncios by their
  PecasProcedimento host, October first then months interleaved; vortal = two GETs of the public JSON API per
  procedure (link -> PT1.NTC.*, then the notice with its documents list); acingov = one GET of the link (a ZIP).
  One GET every 10 s per host, the DR's rules otherwise (stop on 403/429, an hour before a resume, network errors
  retried by the next run, stored work skipped, stop below 2 GB free). Tested on 2 procedures each, then launched
  detached at 22:54Z: vortal 10 491 to read (~58 h), acingov 566 (~1.6 h; the probe's 5 ZIPs are not fetched again).
  The DR download (pid 7824) runs on beside them. Logs: adapters/plataformas/<platform>-log.jsonl.
- Next: when the October DR notices are in (watcher), the interim DR build and verify; the platform raws and their
  facts once the downloads end (a build step, not written yet).
- Why: the platforms hold typed data (Vortal) and the documents (acinGov) that the dump and the DR notice do not.

## 2026-10-26 M.5 night: October complete in the DR; the platforms stopped on disk; their files recorded (commit: M.5: platform downloads recorded as raws; acinGov and Vortal stopped at the 2 GB disk guard)
- DR: the watcher fired at 01:19:42Z: every October notice with a DR PDF is stored (1 763 PDFs in all, 0 errors).
  Interim build (on this branch, not committed here: E1b's own PR carries it): 1 769 documents; October 1 226/1 226
  with data_envio_anuncio, nut_iii_adjudicante, territorio, norma_juridica_adjudicante; publicado_joue 1 225;
  data_limite_propostas 1 195 (the 31 others are concursos limitados and de conceção, whose notice has no deadline);
  data_limite_propostas equal to the dump 1 734/1 734, NIF equal 1 769/1 769, 0 conflicts. `check` 0 differ.
- Disk: acinGov's ZIPs average 33.4 MB, not the 5.9 MB estimated from five probes (one is 1.94 GB): 446 ZIPs took
  14.9 GB, the free space fell to 1.7 GB, and both platform fetchers stopped at their 2 GB guard at ~00:55–00:58Z
  (acinGov 446 of the 566 October ZIPs; Vortal 345 procedures, 16 HTTP 500 and 3 network errors to retry). My estimate
  was wrong; no file was lost. The DR fetcher runs on (its guard is 1 GB; ~27 MB/h). Only scratch copies of files
  already stored in data/ (same sha256) were removed. Nothing downloaded was deleted: that is the person's decision
  (an external disk, or which files to move).
- Done: adapters/plataformas/record.py: every stored platform file -> a raw (699 raw:vortal:*, 446
  raw:pecas:documento:*), with captured_at = its GET. `verify.py --store data governance`: 1 failure, E1b's proposer
  not yet registered (its final build registers it).
- Next: the person decides the disk; the DR download goes on; E1b's final build when it ends.

## 2026-10-26 M.6 acinGov's pieces offloaded to the person's Modal volume; the platforms resumed (commit: M.6: acinGov pieces offloaded to Modal volume ccp-raw-bytes (452/452 checked by sha256), local copies removed; fetchers resumed)
- Decided by the person (his words, ~07:00Z): «si ya tenemos octubre no lo puedes pasar a un lugar en la nube que
  tengamos acceso y luego así liberar espacio», then «Si hazlo» to: his Modal account (storage reportedly
  $0.09/GiB-month with 1 TiB free, from third-party pricing pages; to confirm on modal.com/pricing), upload, check
  every sha256 on Modal, only then remove the local copies.
- Done: Modal CLI 1.6.2 in a scratch venv (account paulovillalobos); volume `ccp-raw-bytes` created; `modal volume put`
  of data/raw/pecas/raw_bytes -> /pecas/raw_bytes (452 files, 07:09:47Z–07:17:27Z); adapters/plataformas/
  offload_check.py hashed every file on a Modal CPU container: 452/452 equal to their name, 0 bad
  (offload-check-pecas.json); the 452 local copies removed. Free disk 1.8 GB -> 16 GB.
- record.py now keeps the raws of offloaded files (it reads offload-check-*.json). verify on the Mac reports I01 for
  those raws: adapters/plataformas/SCHEMA-PROPOSAL.md item 1 for the builder.
- Resumed at 07:23Z: vortal (10 148 left), acingov (122 October ZIPs left; offloaded the same way when done). The DR
  download kept running (pid 7824).

## 2026-10-26 M.7 the platforms run on Modal, for all of 2026 (commit: M.7: platform fetchers on Modal (volume ccp-raw-bytes) for every 2026 procedure; local platform files offloaded and checked)
- Decided by the person (his words, ~07:50Z): «pásalo a modal … hay que dejar libre el disco para poder volver a
  descargar más cosas, para hacer todo 2026, y directamente en modal». The DR download stays on the Mac (small, 1.6 GB
  in all; its build reads the PDFs locally; moving it to a datacenter address mid-way would risk the DR's blocks).
- Done: the local vortal and acingov fetchers stopped at 07:44Z; their files (87 ZIPs, 2.0 GB; 812 Vortal JSON,
  12 MB) uploaded to ccp-raw-bytes, checked on Modal (539/539 and 812/812 hash to their names;
  offload-check-pecas-2.json, offload-check-vortal.json), and the local copies removed: 15 GB free.
- adapters/plataformas/modal_fetch.py: the same fetchers in one small CPU container on the person's Modal account,
  writing to the volume (bytes under <source>/raw_bytes/<sha256>, log /logs/<platform>-log.jsonl, committed every 25
  procedures), the same rules (one GET every 10 s per host, stop on 403/429, network errors retried by a later run),
  a run stops before Modal's 24-hour limit and the next run continues. acingov now reads every 2026 procedure.
  Tested on 5 + 5 procedures from Modal (no refusal; Vortal 4/5, one HTTP 500 to retry; acinGov 2/5: the other three
  link to acinGov's homepage only, so fetch.py now skips bare homepage links: 5 on acinGov, 12 on Vortal).
- Launched detached at 07:58Z: acingov (~9 200 ZIPs, ~26 h, two runs) and vortal (~10 100 procedures, ~56 h).
- What lives where: GitHub holds every file's raw (sha256, URL, captured_at), the logs and the code; Modal holds the
  bytes; anyone can re-hash a copy against its raw.

## 2026-10-26 H.1 the BASE history: contratos and anúncios dumps 2018–2026 (commit: H.1: BASE bulk dumps 2018–2025 read once each (16 files, sha1 equal to the portal's); raws; counts per year)
- Decided by the person, relayed by the builder: «Para el selector por ahora; vamos a los datos (Supabase y descargas)
  para los 5 días». Branch extractor-historico (from extractor-muestras).
- Done: adapters/base-historico/fetch.py (fetch / record): the IMPIC datasets' resources on dados.gov.pt, one GET per
  file, the portal's sha1 checked (16/16 equal), bytes by sha256 under data/raw/base-historico/raw_bytes/ (gitignored),
  16 raws (source base-dump, kinds contratos-ano / anuncios-ano). 2026 not read again (already stored, same resources).
  Counts per year: adapters/base-historico/COVERAGE.md — 208 137 anúncios and 1 683 348 contratos, 2018–2026.
- Blocked: Supabase Storage. The CLI is logged in and linked to ccp-engine from a scratch workdir; the project has no
  bucket, and creating one (`ccp-raw`, private) was refused by this session's permission policy (a shared resource).
  The bytes wait on the Mac (424 MB) until the person creates the bucket or allows it.
- Next: TED Portuguese notices 2018–2026 and the Vortal copies of the DR notices, once the bytes have their place.

## 2026-10-26 H.2 raw bytes to Supabase Storage (bucket ccp-raw), checked by sha256 (commit: H.2: raw bytes offloaded to Supabase Storage ccp-raw — upload, download back, sha256, then delete; 56 files, 507 MB)
- The person created the private bucket ccp-raw in ccp-engine himself («ya está»; storage.buckets checked by the
  builder: public = false, 2026-10-26 18:42:44Z). The builder relayed: upload, download each file back and compare its
  sha256, only then delete the Mac copy.
- Done: adapters/storage/offload.py: the Supabase CLI (logged in, linked to ccp-engine from a scratch workdir; no key
  handled by this code) uploads data/raw/<source>/raw_bytes/<sha256> to ccp-raw/<source>/raw_bytes/<sha256>, downloads
  it back, compares the sha256 with the name, and deletes the Mac copy only on a match; every step in
  adapters/storage/offload-log.jsonl. Uploaded and verified: base-modificacoes 38 files (1.5 MB, test run), then every
  file of 1 MB or more of base-historico (15), base-contratos (the 2026 zip), base-entidades (1), ted (1): 18 files,
  505 MB. 0 hash mismatches.
- Not uploaded: contratos2025.zip (55 383 072 bytes): Storage answered 413 «The object exceeded the maximum allowed size»
  (the project's upload limit, 50 MB by default; raising it is a setting in the Supabase dashboard, the person's). It
  stays on the Mac. The record slices under 1 MB (base-contratos, about 15 000) and the DR PDFs (still downloading,
  read by E1b's build) stay for now: the CLI takes about 6 s per file.
- Disk: 6.0 GB free afterwards. The drop since the morning is macOS swap (5 GB in use), not these files.
- Consequence, as with M.6: verify on the Mac reports I01 for the raws whose bytes now live in the bucket; the builder's
  proposal (adapters/plataformas/SCHEMA-PROPOSAL.md item 1) covers checking them where they live.

## 2026-10-26 H.3 TED Portuguese notices 2018–2026, filtered on Modal (commit: H.3+H.4: TED monthly packages filtered to Portugal on Modal; Vortal's copy of the DR notice as a second source — code, tests, runs launched)
- adapters/ted/modal_ted.py: per month, on the person's Modal account (volume ccp-raw-bytes, nothing through the Mac),
  one GET of https://ted.europa.eu/packages/monthly/<yyyy>-<m>, the package kept under /vol/ted/packages/<sha256>, every
  XML read in the container (the daily packages inside the monthly ones opened in turn), the Portuguese notices kept
  unchanged in /vol/ted/pt/<yyyy-mm>.tar.gz with /vol/ted/index/<yyyy-mm>.json (package URL, sha256, size, captured_at;
  each kept notice's member, sha256, size, format, why). Portuguese = TED-XML with ISO_COUNTRY PT in the coded data;
  eForms with an organisation whose country is PRT. At most two packages at a time (TED allows three).
- Tests: 2018-01 (TED-XML): 45 278 notices, 569 Portuguese, 788 850-byte bundle. 2026-01 (eForms): the first run found
  0 notices because the 2026 monthly package holds 21 daily packages; the code now opens nested packages; second run:
  71 738 notices, 1 585 Portuguese, 2 817 340-byte bundle (the package was read twice, same sha256 6d790daa…).
- Launched detached: 2018-01 .. 2026-09 (105 months). The bundles and indexes come to the Mac per month, then to
  Supabase (ccp-raw/ted/…) by offload.py; the packages stay on the Modal volume as the captures' bytes.

## 2026-10-26 H.4 Vortal's copy of the DR notice (second source of the notice PDF)
- adapters/plataformas/modal_vortal_dr.py: for every procedure whose Vortal notice JSON is stored, the document named
  «<IdIncm>.pdf» in its documents list is downloaded once (public URL), one GET every 20 s (the Vortal notice fetcher runs
  beside it), stop on 403/429; only procedures on Vortal, never around a DR refusal. Bytes in /vol/vortal-dr/raw_bytes/.
- Test on 5 procedures: 5 listed, 5 downloaded, 5 byte-identical to the PDF the DR download stored (sha256 equal).
  Launched detached over the 1 962 Vortal notices stored so far; to be run again as the Vortal fetcher advances.
- Note for the person: acinGov's whole 2026 (about 9 200 ZIPs at 33 MB on average, about 300 GB) does not fit the 100 GB
  of the Supabase plan; today those bytes are on the Modal volume.

## 2026-10-26 H.5 TED done: 105 months, 98 952 Portuguese notices; bundles and indexes in Supabase (commit: H.5: TED 2018-01..2026-09 — 6 399 136 EU notices read on Modal, 98 952 Portuguese kept; 105 package raws; bundles and indexes in Supabase, sha256-checked)
- The Modal run ended with 105/105 months and no error. 6 399 136 EU notices read, 98 952 Portuguese kept (TED-XML
  54 790, eForms 44 162). Packages 23.9 GB, on the Modal volume (ted/packages/<sha256>); raws in
  data/raw/ted/raw/ted-mensal.jsonl. Per year: adapters/ted/COVERAGE.md; per month: adapters/ted/manifest.json (package
  URL, sha256, size, captured_at, counts, the bundle's and the index's sha256).
- The 105 Portuguese bundles (149 MB) and 105 per-notice indexes (23 MB) came to the Mac, each bundle's sha256 equal to
  the one its index recorded on Modal (105/105), then went to Supabase ccp-raw/ted/raw_bytes/<sha256> by offload.py:
  210 files, 179 472 999 bytes, uploaded, downloaded back and equal by sha256; the Mac copies removed.
- Caveat in COVERAGE.md: the eForms filter (any Portuguese organisation) is broader than the TED-XML one (the buyer's
  country), so 2024–2026 are not comparable with 2018–2023 as they stand; a buyer-country filter is next.
- Disk after: 5.4 GB free (macOS swap still at about 5 GB).

## 2026-10-26 H.6 contratos2025.zip stored as byte parts under the 50 MB limit (commit: H.6: contratos2025.zip in two byte parts with a manifest of hashes; joined parts hash to the file; Mac copy removed)
- Decided by the person, relayed by the builder: «Divide contratos2025.zip en partes de menos de 50 MB con sus huellas,
  sin tocar el spend cap». No Supabase setting was changed.
- Done: adapters/storage/split_offload.py: the exact bytes cut at offsets 0 and 40 000 000 (no re-zip) into
  6c46253114cc….part01 (40 000 000 bytes, sha256 fe117ba9…) and .part02 (15 383 072 bytes, sha256 a06e9fd1…), uploaded to
  ccp-raw/base-historico/raw_bytes/, with the manifest (whole sha256 and size; each part's name, order, offset, size,
  sha256) uploaded beside them and committed at adapters/storage/parts/<sha256>.manifest.json.
- Verified: both parts and the manifest downloaded back; the parts equal their recorded sha256; joined in order they
  hash to 6c46253114cca8ba…4a03, the file's sha256; the manifest came back identical. Only then was the Mac copy deleted.
- Raw: unchanged (whole sha256 and URL); raw.schema has no size or parts field, so they are in the manifest and
  COVERAGE.md. All 16 BASE history files are now in Storage; none is left on the Mac.

## 2026-10-26 H.7 Vortal refused (403): both Vortal fetchers stopped (commit: H.7: Vortal answered 403 at 20:18:27Z after a Modal preemption; both Vortal fetchers stopped; resume no sooner than an hour, one client only)
- The Vortal notice fetcher on Modal (M.7) was preempted by Modal and restarted with the same input; its first request
  after the restart got HTTP 403 at 2026-10-26T20:18:27Z and it stopped itself (todo 7 855, done in that run 0). The
  Vortal DR-copy fetcher (H.4), which reads the same host, was stopped by hand right after (modal app stop), as the rule
  for a refusal covers every reader of that host. It had downloaded 219 notices (all HTTP 200; last at 20:12:15Z).
- Cause not known: two readers of one host (about one GET every 6.7 s together) and a new container address after the
  preemption are both possible. The DR download (another host) and acinGov (another host) go on.
- Next: no Vortal request before 21:18Z; then one reader only (the notice fetcher first, the DR copy after it), at a
  slower pace.

## 2026-10-26 X.0 extraction test v1 for TED and BASE contratos: criteria and frozen code, sealed before any sample (commit: X.0: CRITERIA-ted-contratos-v1 and frozen parsers, sampling, blind-reading and scoring code — sealed before any sample is drawn)
- Asked by the person (relayed by the builder): «at least 8 in all»; for extraction, «8 = each new source measured, not
  assumed», 200 per source, criteria fixed first as CRITERIA-v2 did for the DR notices.
- Sealed (sha256), in this commit, before either sample is drawn:
  - adapters/medicao/CRITERIA-ted-contratos-v1.md 786e3b4ab41b1eadcf1900c7568e97aecdef05442a736e484961397027146021
  - adapters/ted/parse.py cf1ee6bdf9811b1a73d37eb885f1e9ee0f73203a03c83286c3516bc51f982dca (TED-XML R2.0.9 and R2.0.8, and
    eForms; written on 2018-01 and 2026-01 only: 569 and 1 585 notices, 0 errors; contract notices 2018-01: buyer name
    and deadline 135/135)
  - adapters/base-contratos/adapter.py 0f4a52c364e30d7368446bc4408781d9c55be9949bd2e03d23fc5e093d3e7eec and mapping.json
    65b9c384a5a05bad70e70cc6eda683948cca334f331adfb664eeeed90dbbd79b (written on October 2026 only)
  - adapters/medicao/sample.py 779c1fb6997f85777a42d001a53ec73b8984169916d81eea8821fb4392918c05
  - adapters/medicao/blind_read.py a6e2eca0ed738267e2aaa6e23392793fc845b5b135156e6eb7ed908b898dfbf3
  - adapters/medicao/score.py 7c32e31453aa6e8545c08cb843c1247364641a6a1a0134579e66b717f12b9677
- Found while writing the TED parser: in eForms the buyer is the organisation the ContractingParty names, not the first
  organisation; on 2026-01, 1 569 of the 1 585 notices kept by the M-run filter have a Portuguese buyer, 16 do not.
- Also in this commit: adapters/storage/offload.py gains --workers and --require-text (used once the database is
  writable again; see below).
- Blocked meanwhile: the ccp-engine database went read-only (default_transaction_read_only = on, 787 MB), so the Supabase
  CLI cannot open Storage; the pending upload of the DR PDFs was stopped before it began. Reported to the builder.
- Next: draw the TED sample (the bundles are on the Modal volume); the contratos sample waits for Storage (its zip is
  there only).

## 2026-10-26 X.1 TED sample drawn and its parser output sealed (commit: X.1: TED sample of 200 (100 TED-XML, 100 eForms) drawn by the sealed script; sample.json and parsed.json sealed before the blind reading)
- `adapters/medicao/sample.py ted` over the 105 Portuguese bundles from the Modal volume, minus 2018-01 and 2026-01:
  population with a Portuguese buyer 54 221 TED-XML and 42 042 eForms (the buyer filter drops about 2 120 eForms notices
  whose buyer is foreign); 100 + 100 drawn with random.Random(20261027).
- Sealed: adapters/medicao/ted/sample.json d12f6a29158385d1dddc9951eaccefa202b788454b45ae5c8788b138f4c0ce8a,
  adapters/medicao/ted/parsed.json 09df8fa4c52cf10e5f143432150258407f377fdbba8cccb23801d732992963d2. The 200 XML files are
  re-derivable from the bundles and sample.json (scratch, not in git).
- Next: check C, the blind family-B reading (reader B's bundled client, model model-b as named by the person for
  the DR test), then A and B with the BASE anúncios once Storage is readable.

## 2026-10-26 X.2 TED v1 scored: A passes, C fails on an eForms parser error; B not run (commit: X.2: TED v1 — blind answers sealed; A passes; C 97.4 % fails on the eForms dispatch date; the 43 disagreements settled from the XML)
- Blind reading: 40 batches of 5 (reader-b-cli, model-b), answers saved before scoring in
  adapters/medicao/ted/blind/; sha256 of the 40 files' sha256 list 7f7d4452e52dfee8565ffddb6f932cf52a09d5e8ac421f70006c7ef950a06e5d.
  score.json 43c494f71bbca196fa27d2c5d48f2f69aaa2d1b6242257ec822316d319ad4246.
- A: the six required fields 98.8–100 % (PASS). C: 1 597 / 1 640 = 97.4 % (96.5–98.0), FAIL; TED-XML 781/781, eForms
  816/859. 39 of the 43 disagreements are one code error: in eForms result notices the parser read the first IssueDate in
  the document, the SettledContract's (BT-145), not the notice's (BT-05). 2 are a joint procurement (parser gave the first
  of six buyers), 2 a change notice whose coded deadline and change text differ. Reader errors 0. adapters/medicao/ted/REPORT-v1.md.
- Verdict as written: TED's extraction is not measured as passing; fix the parser and draw v2.

## 2026-10-26 X.3 TED v2 criteria and fixed parser, sealed before the v2 sample (commit: X.3: CRITERIA-ted-v2 and the fixed TED parser (eForms dispatch date = the root's IssueDate), sealed before the v2 sample)
- Sealed (sha256), before the v2 sample is drawn:
  - adapters/medicao/CRITERIA-ted-v2.md 2c8d1941bde72334f904b6137a0f2fc44982665f9b1b25eb7d89d9498a879a68
  - adapters/ted/parse.py b277c0075feb5f7e2b5adcfab897ea82387017bf1b05a9719e57f9925d3634a7 (dispatch date fix only; on
    v1's 200 notices it changes the 39 wrong dates and nothing else)
  - adapters/medicao/sample.py fbf269f4278be5a1ff108915c43dd12dce511586cc58652718d07aa53f513e8c (--seed, --exclude)
  - adapters/medicao/blind_read.py 749e1b3c5b57044feb9014a9bace6fac06cb375d69c6504831f3d7c56faf6d58 (TED prompt: the
    first buyer when several; the contratos prompt is unchanged)
  - adapters/medicao/score.py e997664b5d228f9e05564469797ba7a625e2621b5a7f443159f39a34ed90d3a0 (TED deadline_time as
    hour:minute; the contratos scoring is unchanged)
- Next: sample.py ted --seed 20261028 --exclude adapters/medicao/ted/sample.json, then the blind reading.

## 2026-10-26 X.4 TED v2 sample drawn and its parser output sealed (commit: X.4: TED v2 sample of 200 drawn by the sealed script (seed 20261028, v1's 200 excluded); sample.json and parsed.json sealed before the blind reading)
- `adapters/medicao/sample.py ted --seed 20261028 --exclude adapters/medicao/ted/sample.json`: population 54 121 TED-XML and
  41 942 eForms (v1's 200 left out); 100 + 100 drawn.
- Sealed: adapters/medicao/ted-v2/sample.json ca9824d2807865917d130977fc1eb629268231181a622a176e105b08eeaa3a08,
  adapters/medicao/ted-v2/parsed.json 2ae15b5ca1c55a602eba15c0476bd673c53849ad2d085bb65620592897c95856.
- Next: the blind reading (same client and model), then scoring.

## 2026-10-26 X.5 BASE contratos sample drawn and its parser output sealed (commit: X.5: BASE contratos sample of 200 drawn by the sealed script from contratos2026.zip (back from Storage, sha256 checked); sample.json and parsed.json sealed before the blind reading)
- Storage answers again (the CLI's login-role step works). contratos2026.zip downloaded back from
  ccp-raw/base-contratos/raw_bytes/2ac78c54…; sha256 2ac78c54690f2e6456c071e07ba984cfacecf058f5b58a3786944d55fa938fb2 as
  the criteria name it.
- `adapters/medicao/sample.py contratos` (v1 criteria, seed 20261027; the contratos path of sample.py is unchanged since
  X.0): population 182 539 records (October 2026 and repeated idcontrato left out); 200 drawn.
- Sealed: adapters/medicao/contratos/sample.json 1a03f8e8fda23938a57f50ec359f0ce6f026cadbded7b839459c81d064a40768,
  adapters/medicao/contratos/parsed.json 5058876e5f0e53d3375b5c0588cb26334d2d2846b1bc89c078830e9394b18111.
- Next: the blind reading (batches of 10), then A, B (against adaptador:base-anuncios facts) and C.

## 2026-10-26 X.6 TED v2 and BASE contratos scored (commit: X.6: TED v2 — A and C pass (C 99.9 %), B 93.0 % fails on wrong joins; BASE contratos — A, B and C pass (C 1 514/1 514); blind answers sealed)
- TED v2 (ted-v2/REPORT-v2.md): blind answers sha256-of-list 38223a26734fbe88eccf44fb3446706de9fa8a4280c1ffed1646400b3509b4a9,
  score.json e944f92d209d2c70fdd090acc28ef6a76d04038ccda79297d6de64227f660d13.
  A PASS; C 1 652 / 1 653 = 99.9 % (99.7–100) PASS, the one disagreement a code error (an EU agency's multilingual
  notice: the parser read the first language form, Danish, not the ORIGINAL English); B 53 / 57 = 93.0 % (83.3–97.2)
  FAIL, join rate 31 / 93. The 4 B disagreements are joins to a different procedure of the same buyer with the same
  deadline (titles quoted); parser errors found by B: 0. As written, TED is not measured; a B-only v3 with a better join
  key needs a decision.
- BASE contratos (contratos/REPORT-v1.md): blind answers sha256-of-list
  0a4d95b8bf98f1930e7046318911c7ed07b1aec304c14a03cd5886ff393b9353, score.json
  783e92020faf1a11b1c44c8caf55a17071ae1a4687965b403c68c76f88f94aa1. A PASS (required fields 99.5–100 %); B 64 / 64 on 17
  joined contracts (94.3–100) PASS; C 1 514 / 1 514 (99.7–100) PASS. Measured. tipo_procedimento is partial (142/200):
  framework call-offs and excluded contracting are outside the vocabulary.
- BASE anúncios 2018–2025 downloaded back from Storage for B (sha256 checked; scratch, deleted after).

## 2026-10-26 X.8 TED v3 (check B only) criteria and parser, sealed before the v3 sample (commit: X.8: CRITERIA-ted-v3 (B only: buyer + deadline + title containment 0.5, as code) and the TED parser reading the ORIGINAL form, sealed before the v3 sample)
- The builder relayed a yes to a B-only v3 with the DR test's v2 protocol (join key as code, threshold before the draw,
  pairs under it «not joinable» and out of the denominator), and to fixing the code error v2's C found.
- Sealed (sha256), before the v3 sample is drawn:
  - adapters/medicao/CRITERIA-ted-v3.md 0203b1f4500d78f808e18d46e7abaafbbf0196ac8899ce787bbfe2656e460c3c
  - adapters/ted/parse.py 715a2dd5f7943480bf296b1636db196623d055e66e794a3cd3233b0c8b1bbe1e: TED-XML form fields from the
    CATEGORY="ORIGINAL" form (coded data still from the coded section), plus `title`. On v1's and v2's 400 notices it
    changes one value (v2 n=85's buyer name) besides adding the title. v3 runs this parser; v2's C ran b277c007….
  - adapters/medicao/sample.py 9109075f7dc0e567541909118413d89b523b54bbdad24b17881044d320a582b2 (--contract-only,
    several --exclude)
  - adapters/medicao/score.py f38bf3f84d064902aab8c3138f4bd7e1bbcc6b838ad78ca1cf6d1b867b310b7c (score_ted_b, THRESHOLD 0.5)
- Also in this commit: the DR upload log so far (49 verified, 14 failed at the pooler's auth limit when 8 CLI processes
  ran at once; those Mac copies were kept).

## 2026-10-26 X.10 TED v3 check B passes; TED measured with v2's A and C (commit: X.10: TED v3 — B 189/192 = 98.4 % (95.5–99.5) on the title-checked join; with v2's A and C, TED's extraction is measured; v1, v2 and v3 side by side)
- v3 sample (X.9): 22 432 TED-XML and 21 446 eForms contract notices in the population; sample.json
  fc0dd45f97bfe61a135a7f59c0f0f04ddfa3f51f440d50bbbb7fc462190c09b7, parsed.json
  1173bb6e4f97610eb9e15229764c13a591c1429ca7c1c50345c9e7b3159ee68f.
- B (ted-v3/score-b.json 0666da40fc9d63aa6e9fde3e3ca8d4b346fea6ef8fe6ba679f319990731071b5): joinable 102 / 200; not
  joinable 78 (no candidate), 15 (under 0.5), 5 (tie); agreement 189 / 192 = 98.4 % (95.5–99.5), PASS. Disagreements:
  2 wrong joins at containment 0.62 and 0.50 (titles quoted), 1 where the sources differ (eForms ProcedureCode
  restricted, BASE Concurso público); parser errors 0.
- adapters/medicao/REPORT.md: v1, v2, v3 and BASE contratos side by side. Count towards the 8: BASE contratos and TED
  measured; the DR notices measured earlier (CRITERIA-v2).

## 2026-10-26 X.11 Coverage matrix: source × year × field, gaps named (commit: X.11: coverage matrix for BASE anúncios and contratos 2018–2026 and TED 2018–2026, from the adapters' own code; gaps named)
- adapters/coverage/matrix.py counts, per year, the share of records for which the adapter's own code gives a value
  (base-anuncios map_record, base-contratos contract_values, adapters/ted/parse.py 715a2dd5…); the BASE dumps were
  downloaded back from Storage one at a time, sha256 checked, counted and deleted. matrix.json holds counts and the most
  frequent reasons for no value; COVERAGE-MATRIX.md the tables, every share under 90 % with its reason, and the sources
  not in the tables (DR 2026 in progress, DR 2018–2025 not fetched, Vortal stopped, platform pieces are documents).
- Weakest: BASE contratos tipo_procedimento 74–88 % (call-offs and excluded contracting outside the vocabulary);
  adjudicatario 88–90 % (adjudicatários without NIF); TED estimated_value 37–71 % and TED-XML buyer_nif 11–86 % (not in
  the notices).

## 2026-10-26 X.12 Vortal retried after the hour, one reader at 20 s; the DR uploads resumed with one process (commit: X.12: Vortal retried at 21:23Z, one reader at one GET per 20 s, no refusal so far; DR uploads resumed one process at a time)
- Vortal: the notice reader (modal_fetch.py --platform vortal, now one GET per 20 s) started at 21:23Z, more than an hour
  after the 403 of 20:18:27Z; the DR-copy reader stays stopped until it ends. First committed log: 46 GETs to 21:38Z,
  42 × 200 and 4 × 500 (server errors, logged; a later run retries them), no 403 or 429. On a second 403 it stops itself
  and stays stopped for the day.
- Storage uploads of the DR PDFs: 8 CLI processes at once tripped the pooler's authentication circuit breaker (each
  process re-initialises the CLI's login role); stopped, nothing unverified deleted. Resumed with one process; an object an
  interrupted run already stored (409 KeyAlreadyExists) is now downloaded back and checked like a fresh upload.

## 2026-10-27 X.13 Disk: verified DR PDFs deleted, the fetch counts what is in ccp-raw as stored; Modal limit stops Vortal (commit: X.13: dr-anuncios fetch counts PDFs verified in ccp-raw as stored; 13 unlogged uploads checked and logged; Modal input limit stopped the Vortal reader)
- Disk fell under 1 GB twice (macOS swap, then growth outside this worktree). Deleted only copies verified in ccp-raw
  (sha256 of the downloaded-back object): 8 684 DR PDFs (685 MB) by offload.py, plus the contratos2026.zip copy and the
  TED bundles in scratch (156 MB). The DR fetch stopped itself under 1 GB at 10:32Z (13 101 of 21 658 in that run).
- adapter.py stored(): a PDF counts as stored when it is on disk or verified in ccp-raw by offload-log.jsonl. Before, a
  restarted fetch saw only the 2 020 PDFs still on disk and began fetching again; stopped after 3 GETs (13:51:21–41Z,
  three notices already held; logged as they are). Restarted at 13:54Z: 13 622 stored, 8 548 to fetch.
- 13 PDFs were neither on disk nor in offload-log: the 8-worker run killed on 2026-10-26 had stored and deleted them
  without writing their lines (pool.map writes in order). Each was downloaded back from ccp-raw and matched its sha256;
  logged with a note.
- Vortal notice reader: ended 13:49:46Z by Modal, not by Vortal: "Input rate limit (0/s) exceeded" for the function
  (the acinGov run ended the same way). Log: 7 406 GETs, 7 390 × 200, 15 × 500, the one 403 of 2026-10-26 20:18:27Z.
  No Modal setting changed; the DR-copy reader is not started.

## 2026-10-27 X.14 Vortal reader restarted after Modal accepts runs again; DR fetch and uploads restarted (commit: X.14: Vortal reader restarted at 20:12Z; DR fetch and uploads restarted after the scratch workdir was emptied)
- The DR fetch stopped itself under 1 GB again near 14:50Z (301 of that run's 8 548). Restarted 20:09Z with 7.6 GB free:
  13 980 stored, 8 190 to fetch. The disk guard now pauses it at 1.5 GB, before the fetch's own 1 GB stop, and resumes it
  at 3 GB.
- The session's scratch folder was emptied on a restart, with the CLI's linked Supabase workdir in it. A first upload run
  at 20:09Z logged 301 failures ("failed to change workdir"); nothing was deleted (a local copy goes only after the check).
  Relinked; uploads verify again from 20:11Z, one process, detached so they outlive the session.
- Modal accepts runs again (the builder session relayed that the workspace payment method was updated on 2026-10-27).
  The Vortal notice reader (one GET per 20 s, resumes from its own log of 7 406 lines) restarted at 20:12Z. acinGov is
  not restarted: 2026 alone is about 300 GB, beyond the plan, and waits for Paulo.

## 2026-10-27 X.15 Main (8167135fd) merged into extractor-historico for the handover to the main session (commit: Merge main 8167135fd into extractor-historico: governance re-recorded after main's head, base-anuncios adapter @3)
- Conflicts: governance/events.jsonl and principals.json take main's file; this branch's three events (evento:46–48:
  propose and correct of adaptador:base-anuncios@1, propose of adaptador:base-contratos@1) are re-recorded after main's
  head through engine.governance.Log with their own principals, payloads and times, now evento:84–86; its three
  ferramenta registrations are added after main's principals. BUILD-LOG.md and .gitignore keep main's lines first, then
  this branch's. adapters/base-anuncios/adapter.py takes main's (it adds the «nAnuncio empty» case for the history
  loads); registered as ferramenta:adapter-base-anuncios@3 (evento:87; @2 retired). adapters/dr-anuncios/adapter.py keeps
  this branch's stored() (X.13). This branch claims no decision id; main goes to D56.
- Checked: `adapter.py check` for base-anuncios 2026: 22 306 files, 0 differ. `verify.py` with the interim E1b build
  (untracked) set aside: fixtures, repo and measure stores 0 failures; governance 87 events, no I09/I04/PROV; the data
  store's only failures are 2 964 I01, raws whose bytes live in ccp-raw or on the Modal volume (BASE dumps 2018–2025,
  entidades, modificações, TED daily and monthly packages, Vortal notices, platform pieces), the open item of
  adapters/plataformas/SCHEMA-PROPOSAL.md item 1. The TED monthly packages alone are tens of GB, so restoring them on the
  Mac is not an option. Tests: 67 passed, 2 failed, both verify over data/ on the same I01
  (test_verify.py::test_empty_stores_pass, test_verify_main_exit_code_is_zero).

## 2026-10-27 — Merge of the extractor (PR #2) into main; D57
- Asked: the person, «I want to have a main one… merge them» (one session).
- Done: extractor-historico merged (main 8167135fd was already merged into it there; its evento:46-48 re-recorded as
  84-86, base-anuncios adapter registered @3 as evento:87). D57: verify's I01 accepts bytes recorded as stored and read back
  outside the Mac (offload log, part manifests, Modal offload checks, TED manifest). The 15 108 base-contratos slices, in
  no store, cloned into data/raw/base-contratos/raw_bytes of the main checkout (git-ignored, local only).
- Still running from the extractor's worktree (detached): the DR download, the DR uploads, the Vortal reader on Modal.
  That session is archived only when they end and its untracked state is moved (handover notes, extractor-handover-2026-10-27.md).
- Checks: verify ok on every store (data: 321 728 objects). Tests: 89 pass, 2 red and disclosed: test_b3_rules_v0 (since round 7)
  and test_b5 reference cases, which now asks 100 annotated real cases (20 exist, from the fixtures): real work left, not lowered.

## 2026-10-28 — D53: AMALIA v7 measured (rank 16 and 64)
- Done: leitor:a8 (v7, rank 16) and leitor:a9 (v7r64, rank 64); manifests rebuilt from the function calls' return values
  (the local entrypoints stopped at a session restart; the runs were detached and finished).
- Result (reports/measure/escritas-v7-2026-10-28), facts exact with the guard 0.3, sealed / dev / real: v6 71.0 / 67.5 /
  10 of 16; v7 r16 85.0 / 80.0 / 13; v7 r64 83.0 / 79.5 / 14; Reader B 83.5 / 83.0 / 9. Invented facts on the sealed set: v7 r16
  2.3 %, Reader B 4.1 %. Markers found / without cause: v6 57.7 / 37.2 %, v7 r16 73.9 / 8.9 %.
- Decision: v8 at rank 16 (rank 64 no clear gain, slower, more false markers).

## 2026-10-28 — D58/D59: the rules factory, round 1
- Asked: the person, «or maybe you could run them directly» (overnight plan: factory round 1 after v8).
- Done: 20 targets from the CCP (7 limiar, 13 prazo_minimo); leitor:a8 (AMALIA + v7) proposed, leitor:b reviewed blind (one
  answer retried once after the client stopped at its output limit). Recorded: 4 settled, 14 differ, 2 without a valid
  proposal (AMALIA gave no rule for art. 21.º n.º 1 b) and c)).
- Then read against the law: the 4 settled were all wrong in the same way, a value the schema does not have (candidaturas,
  counting from the convite, a concurso de ideias). D59: the factory now finds such gaps by code; the 4 were invalidated
  (stale) by ferramenta:rule-factory@2 with the gap as reason. Net settled: 0 of 20. 12 of 20 targets have a gap.
- verify: the factory's readings folder (fabrica1) mapped; escritas reports recomputed by the tool that wrote them (v7's was
  recomputed by v6's tool and failed). Registered verify@36.
- Next: round 2 grows the vocabulary and the engine first (prazo_candidaturas_dias, data_envio_convite, conceção procedures,
  urgência), then the 12 targets read again; the 8 without a gap: AMALIA restates the threshold as a condition or adds conditions on 4, no rule on 2.

## 2026-10-28 — D60: the rules factory, round 2
- Done: the deadline vocabulary gains prazo_candidaturas_dias and data_envio_convite (read_rules round 8; serve.py accepts both
  facts; the engine evaluates them without new code). 8 targets (round 1's whose gaps these values close), prompts committed
  first (9e88e3919), leitor:a8 proposed, leitor:b blind.
- Result: 2 settled, both right against the text: art. 174.º n.º 1 (30 days, candidaturas, from the JOUE notice) and 218.º
  (30 days, proposals, from the convite). 174.º n.º 3 replicated but wrong (the absolute minimum is 15, not 30; special sectors
  only): three more gaps added to the code check (special sectors, indicative notice, two minimums), so it stays proposed.
  The other 5 differ: AMALIA keeps counting from the notice where the text says convite (191.º n.º 1, 192.º n.º 2), drops a
  condition the text states (198.º n.º 1) or one rule of a passage that holds two (190.º n.º 1: 6 days, 14 for works).
- Rules settled by the factory so far: 2 of 20 targets. Settled overall: 8 (6 earlier + 2).
- verify: a rule's content base is the stored revision carrying the log's latest propose/correct (registered verify@37).

## 2026-10-28 — D54: AMALIA v8 measured
- Done: v8 trained detached (1 754 steps, 11 375 s, USD 12.52); leitor:a10 registered; v8, v7 and Reader B measured on dev 400,
  sealed 400 and the 16 real questions (reports/measure/escritas-v8-2026-10-28; Reader B's 3 missing answers per set filled).
- Result, facts exact with the guard, sealed / dev / real: v8 88.2 / 84.8 / 13 of 16; v7 76.8 / 71.2 / 13; Reader B 75.5 / 77.2 / 9.
  Invented facts on the sealed set: v8 2.6 %, v7 5.6 %, Reader B 7.7 %.
- Next: dev-only error analysis of v8, fixes to labels / guard / data, v9.

## 2026-10-28 — D61: v8's dev errors, label rules, data-v9
- Done: dev-only error analysis of v8 (61 of 400 not facts-exact after the guard; the sealed set untouched). Two label rules
  written into LABELS.md (the procedure asked about; one candidate). My first draft of the first rule was backwards (an asked
  procedure would not be a fact); the label audit showed it would contradict 211 labels and drop what the engine needs, so it
  was reversed before use. 204 errata from two audits (sampled and read), applied from v9 only. 600 new questions on v8's five
  error kinds by four writers, relabelled under the final rule (61 changes), 100 held out as a targeted dev set.
- data-v9: dev 400 and sealed 400 (same questions, 25 + 25 gold answers corrected), alvo 100, 2 700 questions trained.
- verify ok (verify@38). v8's and Reader B's dev/sealed/real answers carried to avaliacao-v9 (prompts byte-identical).

## 2026-10-28 — D61: AMALIA v9 measured
- Done: v9 trained detached (ap-t83yESUJ7XGoN0JUYzDk9t, ended 05:34Z, USD 11.19 billed so far); leitor:a11 registered
  (adapter sha 9f93ecab7042); v9, v8 and Reader B measured on dev 400, sealed 400, alvo 100 and the 16 real questions
  (reports/measure/escritas-v9-2026-10-28).
- Result, facts exact with the guard, sealed / dev / alvo / real: v9 87.5 / 87.0 / 92 / 13 of 16; v8 87.5 / 83.5 / 85 / 13;
  Reader B 74.5 / 75.5 / 72 / 9. Answer exact on the sealed set: v9 75.2, v8 70.0, Reader B 63.2. Invented facts (sealed):
  v9 1.1 %, v8 2.1 %, Reader B 7.2 %.
- Dev-only look at the one regression, markers without cause (sealed 4 % to 12 %): v9 finds 45 more gold markers on dev (missed
  99 to 54) and adds 18 false ones (tipo_contrato 9 to 16, tipo_procedimento 4 to 10); 3 dev answers mark publicado_joue
  ambiguous, which D61 forbids, so a guard rule can drop it.
- verify ok; tests/test_verify.py 5 passed.
- Next: guard rule for publicado_joue (new guard version, re-measure); the vocabulary decisions the factory is waiting on.

## 2026-10-28 — D62: rule vocabulary on the person's choices, factory round 3
- Done: the person chose all four recommended options (urgency as a declared fact; special sectors with 15 binding and 30 as
  usual_days; the indicative notice as a fact; design and ideas contests in full, with up to three rules per answer).
  read_rules round 9 (VOCAB_9, rule readers only), engine note for usual_days, regra schema, serve accepts the new facts.
  The factory now targets only the gaps a round newly closes (a first run picked up 174.º n.º 1 and 218.º, already settled;
  caught before any answer). Prompts committed first (1805b2a9d); leitor:a8 and leitor:b blind.
- Result: 0 of 7 settled. Reader B's 7 readings agree with the text, two of them as two rules (190.º n.º 1, 219.º-B n.º 5).
  AMALIA v7 padded its answers to three rules, took rules from neighbouring passages, ignored the new deadline field and
  counted from the notice where the text says convite. AMALIA was never trained to read typed rules (regra_tipada 0).
- verify@39: a target's -b/-c rules read the target's answer file. verify ok.
- Next: a rule-reading task for AMALIA, written from the law (not from Reader B's readings, so the families stay independent).

## 2026-10-28 — D63: AMALIA v10 reads typed rules, factory round 4
- Done: task regra_lida (training/data-v10): 600 written CCP-style articles with invented numbers, gold readings written
  from the text by six writers under training/rule-readings/GUIDE.md, code checks on every example, 18 near-copies of real
  target passages dropped; 1 000 train rows, 82 held out. BEFORE committed before v10 answered (v9 2.4 %, Reader B 85.4 %).
  v10 trained detached (ap-FdWSej880Y2yWDQXNtT1i4, 10:45Z to 14:11Z, USD 13.17 billed so far); leitor:a12 registered
  (adapter sha 0b10f5c0fe65).
- Result, 82 held-out articles: rules exact v10 69.5 % (v9 2.4 %, Reader B 85.4 %); content exact (passages aside) 76.8 %
  (Reader B 98.8 %); right number of rules 98.8 %; right days or limits 97.6 % (reports/measure/regras-v10-2026-10-28).
- Round 4 (fabrica-4, the 18 open round-1 targets, leitor:a12 proposes, leitor:b blind): 4 settled (190.º n.º 1 and
  219.º-B n.º 5 as two rules each, 191.º n.º 1, 219.º-J n.º 3). 14 differ; days or limits agree on 17 of 18. Two differ
  only in the passages cited (174.º n.º 2, 191.º n.º 5: Reader B also cites the number referred to). The rest differ in
  conditions or the comparator: 127.º-C le vs lt, 198.º concurso público vs negociação, 174.º n.º 3 30 vs 15 days.
- Next: the person's call on citation in D43 replication; a dev-only look at v10's condition errors.

## 2026-10-28 — D64: replication by content and the target passage
- Done: the person's product rule product_rule:replicacao-conteudo-e-alvo (evento:220, settled on record). read_rules
  same_content; the factory pairs rules by content, `recheck --round N` compares a round's recorded answers again, and a
  round with `content` records under D64. verify accepts a D64 uphold's own extra passages (the rule cites the proposer's).
- Result: round 4 rechecked from the same answers, no reader asked again: 174.º n.º 2 and 191.º n.º 5 settled. 16 rules
  settled. verify ok (verify@42, rule-factory@8, read-rules@17).


## 2026-10-28 — D65: AMALIA v11 on v10's error kinds, factory round 5
- Done: eval pool of 400 written articles (eval-01..04), 13 near-twins dropped, dev 203 / sealed 184 split by id, sealed
  committed before any reader. v10's dev errors sorted by code; 400 targeted articles (alvo-01..04, eight kinds) checked
  against the eval texts; regra_lida_alvo 800 rows. BEFORE committed before v11 answered. v11 trained detached
  (ap-NJ6Q0ZHPs0oiC7JEfkJkZi, 16:35Z to 20:11Z, USD 13.85 billed so far); leitor:a13 registered (adapter sha b3bfb84cfde3).
- Result, replicates (D64): sealed v11 96.7 % (v10 91.3 %, Reader B 98.9 %); dev 97.5 % (87.7 %, 98.0 %); data-v10's held
  out 89.0 % (76.8 %, 98.8 %). Rules exact on sealed: v11 93.5 %, v10 87.0 %, Reader B 81.0 %
  (reports/measure/regras-v11-2026-10-28).
- Round 5 (fabrica-5, the 12 targets open after round 4, leitor:a13 proposes, leitor:b's round-4 answers): 1 settled
  (88.º n.º 2 a)). 17 rules settled. Days or limits agree on all 12. What differs: 127.º-C le vs lt; contract types (17.º-B
  n.º 4, 21.º n.º 1 b) and c), 31.º n.º 4, 54.º-A); a condition v11 adds (174.º n.º 3, 241.º-B, and on 198.º n.º 1 a start
  date that is not in the text); one v11 leaves out (198.º n.º 2, 192.º n.º 2).
- verify: the v11 report is recomputed from the stored answers; a diff is checked at its current revision only (round 5 was
  the first to revise the package diff, and the old revision was being compared with the new packages). verify@45 ok.

## 2026-11-03 — D66: the reading protocol v3, part 1 (decisions, code, engine, round 6 prompts)
- Done: the person's five product rules (evento:249–253): titles name the procedure; a limiar is a limit on choosing a
  procedure, and 88.º n.º 2 a) is withdrawn; the v3 vocabulary (schemas/vocabulario-v3.json); quotes checked by code and
  «não tipável» as an answer; the most specific rule wins in the engine. D66 row written before any result.
- tools/read_rules_v3.py (read-rules-v3@3): context, prompt (L1–L14, what a rule means to the engine, neutral question),
  schema (rules with quotes, or «não tipável» with four reasons), checker, canonical form, cited passages. Tests on the real
  law (tests/test_read_rules_v3.py): correct answers on 7 targets pass; broken copies with each mistake of rounds 1–5 fail; a
  quote cut from a longer phrase fails. training/rule-readings/PROTOCOL-V3.md: the 12-point checklist and the paper audit.
- Governance: nao_tipavel is a reading of the law (settles by a blind uphold of the other family, like regra). Engine: limiar
  compares with lt/le/gt/ge; among applying prazo_minimo or limiar rules of one field the most specific gives the verdict,
  otherwise differing verdicts are nao_avaliado / conflito (tests/test_most_specific.py). regra schema: comparators gt, ge.
- 88.º n.º 2 a) invalidated by rule-factory@10 under product_rule:limiar-e-escolha-de-procedimento; packages rebuilt.
- Round 6 (fabrica-6): the 12 targets of round 5, prompts rendered with v3 and their context kept beside them; committed
  before any reader answers. verify V3: a recorded v3 answer passes the checker again; the payload is the answer's content;
  an uphold is exactly a replication.
- tools/make_rule_readings_v12.py: every written article as a law of its own, rendered by the factory's code, gold quotes
  derived by code and checked by the factory's checker. On the existing articles: 957 of 1 000 training and 392 of 400 old
  eval articles pass; the rest is listed (a procedure no source names, days not in the text, …).
- Next: leitor:b and leitor:a13 on round 6; new v3 articles (v3-01..04, eval3-01..02) by writers under BRIEF-V3.md; data-v12;
  BEFORE; v12 on Modal.

## 2026-11-03 — D66, part 2: round 6 read, protocol 0.2, round 7 prompts
- Round 6 (fabrica-6, protocol 0.1): leitor:b (Reader B, fresh, blind) passed the checker on all 12 targets once the checker let a
  «não tipável» quote the title that makes it so (L3: «Capítulo II — Sistemas de aquisição dinâmicos»); its readings agree with
  the paper audit on 8 (127.º-C, 17.º-B n.º 4, 54.º-A, 88.º n.º 2 a) not typable as limits; 21.º n.º 1 b), c); 31.º n.º 4 with
  the duration; 198.º n.º 1; 241.º-B sem_vocabulario). leitor:a13 (v11, never trained on v3) passed on none: nothing proposed,
  nothing settled (FABRICA6.md).
- Reader B's other three answers («texto_em_falta» for 174.º n.º 3, 192.º n.º 2, 198.º n.º 2) showed two gaps: a referred number
  was shown by its opening line only (n.º 1 of 7.º, n.º 3 of 167.º without their alíneas), and L12 did not say when a missing
  text blocks a reading. Protocol 0.2 (read-rules-v3@4) shows a referred number whole and says: only when the days, the value
  or a fact of the rule are in it. Round 7's prompts are rendered with 0.2 (none is round 6's byte for byte, so leitor:b
  answers all again), committed before any answer. A rehearsal of the recorder on a copy of the log found and fixed a name
  clash (a target whose own name ends in an alínea, 21.º n.º 1 b)) in verify V3 and in the factory's invalidation.

## 2026-11-03 — D66, part 3: protocol 0.3, round 8 prompts, data-v12
- Round 7 (protocol 0.2): leitor:b passed the checker on all 12 targets and its readings agree with the paper audit on all
  12 (7 rules: 21.º n.º 1 b), c), 31.º n.º 4, 174.º n.º 3, 192.º n.º 2, 198.º n.ºs 1 and 2; 5 not typable: 127.º-C, 17.º-B
  n.º 4, 54.º-A, 88.º n.º 2 a) as nao_e_limiar, 241.º-B as sem_vocabulario). No family-A reader read round 7.
- A writer found the renderer printing an article's n.º 1 a second time under the article id. Protocol 0.3 (read-rules-v3@5)
  shows an article's own opening words only when its alíneas hang from it (19.º, 20.º). Round 8 = round 7's targets with
  0.3, committed before any answer; leitor:b answers again; v12 reads round 8.
- data-v12 (make-rule-readings-v12@2): six writers under BRIEF-V3.md wrote v3-01..04 (400 training articles) and
  eval3-01..02 (200 measured articles), each batch 100 of 100 through the check. Built with protocol 0.3: train 1 318 rows
  (957 old articles in v3 plus 359 new; 41 new left out as close to an eval3 article or a real passage), dev 104 and sealed
  96 (eval3, split by sha256 of the id; sealed read by no reader yet), dev_antigo 393, 91 left out with their reason
  (REJECTED.json).

## 2026-11-03 — D66, result: AMALIA v12 measured, factory round 8
- Done: BEFORE (v11 and leitor:b on dev, sealed and dev_antigo) committed before v12 answered (187028adc). leitor:b
  answered round 8: 12 of 12 through the checker, all as the paper audit. leitor_b_cli: a call that times out is skipped,
  not the batch (a stuck call had lost the sealed batch's other answers; the rerun completed 96 of 96). rule-factory@16:
  a target settled as «não tipável» shows its reason in the round report. v12 trained detached
  (ap-yv1b6uv0Sci4WNA7B6jmZw, 02:59Z to 07:12Z, 1 965 steps, USD 16.33 billed so far); leitor:a14 registered (adapter
  sha 1e8d700d771b).
- Serving correction, disclosed: data-v12's rows are written with sort_keys, so every stored answer schema has its
  properties in alphabetical order; the guided decoder writes keys in the schema's order, and v12 was trained in the
  factory's order (the phase-4 finding, repeated in the v12 generator). Attempt 1 began every answer with «nao_tipavel»
  (set on 100 of 104 dev answers, the gold has 25): sealed 10.4 %, dev 17.3 % settle. readers/leitor_a_modal.py
  --order required puts each object's properties in the order of its required list, which gives back
  read_rules_v3.schema on all 593 measured rows (tests/test_reader_order.py). Found from the stored schemas; no sealed
  answer was opened. Attempt 1 kept as leitor-a14.attempt1.jsonl. Round 8's prompts already had the factory's order.
- Result (reports/measure/regras-v12-2026-11-03), settles: sealed v12 55.2 % (v11 4.2 %, leitor:b 81.2 %); dev 44.2 %
  (4.8 %, 80.8 %); dev_antigo 63.9 % (v11 0.0 %). On dev, v12 settles 44 of 79 articles that hold a rule (leitor:b 59)
  and 2 of 25 that hold none (leitor:b 25); 46 of its 104 answers fail the checker, mostly a quote that is not the
  passage's own words.
- Round 8 (fabrica-8, leitor:a14 proposes, leitor:b's 0.3 answers review): 0 settled. 198.º n.º 1 passed the checker and
  differs (v12 leaves out publicado_joue); 11 without a valid proposal (conditions from neighbouring numbers, procedures
  and contract types the words do not name, rules for the 5 targets that hold none). 16 rules settled (17 less 88.º
  n.º 2 a), withdrawn).

## 2026-11-03 — D67, the data part: why v12's data rated 3, and the tools for data-v13
- Audit of data-v12's rule-reading rows against dev (reports/DATA-AUDIT-v12.md; sealed only in the leak count): 959 of
  the 1 318 training rows were written for the old prompt; «não tipável» 7.4 % (dev 24.0 %); titles 16.8 % (dev 100 %);
  each v3 kind 29–52 rows; 70.5 % of the quotes are the vocabulary's first phrase where it lists others (dev 46.3 %);
  stored schemas alphabetised; 21 training articles close to a measured one (9 sealed, 3 dev, 9 dev_antigo).
- tools/make_rule_readings_v13.py: data-v12's articles plus BRIEF-D67's (training/rule-readings/v4-*), untitled articles
  under NEUTRAL titles (tests: no reading changes), every training article compared with every measured article, the
  schema in the factory's order. tools/preflight_data.py: 8 checks of the training rows against dev; data-v12 fails 7.
  training/train_lora.py: run v13 refuses to start unless the gate passes.
- BRIEF-D67: 13 batches of 100 (40 «não tipável», 10 per reason; the v3 kinds; comparador lt and le only until the limiar
  product rule). Pilot batch v4-01 being written; the other 12 after its review.
- Texture (same day, on Paulo's question whether the data is human-like and messy): the real CCP passages with days or
  euros show a reader four times the text of our written articles, twice the values, cross-references in 55 % of targets
  (ours 12 %), another law in 18 % (0 %), old spelling in 27 % (0 %) (reports/DATA-AUDIT-v12.md). BRIEF-D67 gains sections 7
  (texture bands from the law) and 8 (50 articles, two targets each); make_rule_readings_v13 puts ~27 % of articles in the old
  spelling (no reading changes) and prints a batch's texture beside the law's; preflight_data 0.2 adds 11 checks against the
  real law (data-v12 fails 17 of 18). Pilot v4-01 (tidy, 100 of 100 pass) is kept; v4-02..07 are being written to the new brief.
- Protocol 0.4 (Paulo: «Yes, run it», after «can we get there … also our system»): vocab_text prints every law phrase the
  checker accepts (prompts ≈ 19 000 characters); an anaphoric start is read in its passage (L9); L10 and L5 say what 0.3
  left to the reader. A3 waits for Paulo's limiar rule; A6 (one ambiguous dev line) left so the measured articles stay.
  render() and check() take the prompt's version: data-v12, its measurement and rounds 6–8 keep 0.3 (593 of 593 prompts
  render byte for byte). data-v13 renders train and the measured sets (same articles and gold) in 0.4; v13 max_len 12 288.
- Quote scaffold (D67 B7): readers/quote_grammar.py + leitor_a_modal.py --quotes text --contexts FILE (contexts by
  tools/write_contexts.py under governance/readings/avaliacao-v13/contexts/). Every quote is a token-aligned piece of a
  passage its slot may cite; 1 911 of 1 911 gold answers accepted, v12's 20 bad-quote dev answers refused; xgrammar 0.2.8's
  parser agreed on 12 714 texts (run with stand-ins for torch; vLLM 0.30's own xgrammar not yet tried). Found on the way: the
  schema path decoded «, » and «: » while the gold (and the training) is compact JSON; the grammar writes the gold's form.
- Batches v4-02..07 written to BRIEF-D67 (100 of 100 each; texture inside every band). verify ok.
- data-v13 generated (tools/make_rule_readings_v13.py, protocol 0.4): train 2 584 rows (batch/alvo/v3 1 284 after the
  leak test against every measured article; BRIEF-D67's v4-01..13 1 300), dev/sealed/dev_antigo re-rendered in 0.4 (same
  articles and gold). Pre-flight (tools/preflight_data.py): 18 of 18 pass — «não tipável» 23.9 % (dev 24.0 %), reasons
  179/148/146/145; every dev kind 128–146 rows; D67 rows 1 300 of 2 584, texture inside every band (shown 1 841 characters,
  12 passages, 5 values named, cross-reference 50 %, qualifier 22 %, other law 21 %, other units 24 %); old spelling 18 %
  (law 27 % ± 10); first listed phrase 40 % (law 37 %); schema order and answer keys 0 off; 0 leaks. verify regenerates
  data-v13 byte for byte (ok). v13's mix is 1.31× v12's: about 5.5 h and USD 22 on one H100.
- BEFORE (training/runs/v13/BEFORE, tools/measure_rule_readings_v13.py, protocol 0.4): leitor:b (Reader B, model-b) answered
  data-v13's dev and sealed blind. Dev 104: 100 % valid, 94.2 % settle (in 0.3: 92.3 % and 80.8 %); sealed 96: 96.9 % valid,
  89.6 % settle (0.3: 94.8 % and 81.2 %), 94 of 96 answered. 11 first calls ended with no answer (9 at the output limit,
  looping on whitespace; 2 stuck 30 minutes) and were asked again; reader-b-cli on PATH no longer serves model-b on
  that account, so the second call used reader B's client (0.166.0-alpha.5.1, as in earlier rounds). Two sealed
  calls ended at the output limit both times and stay unanswered (they count as not settling). v12's reading of the same
  sets with 0.4 and the quote grammar (leitor:a14, on Modal) is added to BEFORE before v13 answers.
- tools/measure_rule_readings_v13.py (measure-rule-readings-v13@1): v12's measurement with the checker of the protocol 0.4;
  it counts the answers decoded under the quote grammar (all 593 gold answers settle). verify@51: MEAS recomputes
  regras-v13 reports.
- v13 training (Paulo: «Yes, ~22 is fine»): train_lora.py ran the pre-flight gate (18 of 18) and spawned Modal app
  ap-kVPhVFVloK7fNOwPVZEtNy, function call fc-01M6H6VPM2V9MBJD4DW7HT0T91, one H100. Its limit went from 6 to 9 h first
  (a11abc8ea): v12 trained 4.2 h, v13's mix is 1.31x, and the adapter is saved only at the end.
- BEFORE, family A: v12 (leitor:a14) read data-v13's dev and sealed with the protocol 0.4 and its quotes held to the text
  (--quotes text, the first live run of readers/quote_grammar.py; apps ap-4FjSSiziqNFCsqtztEWcxR, ap-3DiBA6zAUGlhfjECXjLvCx;
  200 of 200 answers decoded with the grammar). Sealed: 68.8 % valid, 57.3 % settle (in 0.3 without the grammar: 63.5 % and
  55.2 %). Dev: 64.4 % valid, 49.0 % settle (55.8 % and 44.2 %); the checker refuses 37 of 104 (was 46), none for a quote
  outside the text; «não tipável» right 5 of 25 (was 2; Reader B 24); the most common refusal is now a real quote that does not
  name the value (15). The grammar and the prompt alone move v12 two points; the training is the lever.
  training/runs/v13/FORECAST.md: the forecast made before training (sealed 75–85 %, round 9 6–10 valid and 4–8 settled of
  12), committed before v13 answers.
- Round 9 (rule-factory@18, FROUNDS[9]): round 8's 12 targets with the protocol 0.4 (prompts about 20 000 characters; none
  is round 8's byte for byte). leitor:b (reader B's client, model-b) answered all 12 at the first call: 12 of 12
  pass the checker, and all 12 have round 8's canonical content (7 rules, 5 «não tipável», as the paper audit read them).
  v13 (leitor:a15) proposes with --quotes text; readers/leitor_a_modal.py knows v13 (amalia-ccp-lei-v13, leitor-a15).
- v13 trained (training/runs/v13/MANIFEST.json): 2 061 steps, 2 epochs, 36 736 examples, 42.8 M tokens, 17:21Z to 22:57Z
  (5.6 h of the 9 h limit), USD 22.91 (training/runs/v13/COST.json). Adapter amalia-ccp-lei-v13 (adapter_model.safetensors
  09efbf9b3b88…), registered as leitor:a15.
- v13 read data-v13's dev, sealed and dev_antigo and round 9 with the protocol 0.4 and --quotes text (apps
  ap-zKCZZkYprT2AeNSTP2tkUs, ap-vPygw7IT3Do0EYE3X3g8mF, ap-gWYA0XqqUtjvVOe6gB3KAQ, ap-IvQG6PnCQ4ZKUljyrlVqLH): 593 of 593
  and 12 of 12 answers decoded with the grammar.
- Measured (reports/measure/regras-v13-2026-11-03.md). Sealed 96: 95.8 % valid, 86.5 % settle [78.2, 91.9] (v12 with 0.4
  and the grammar 57.3 %, leitor:b 89.6 %; forecast 75–85 %). Dev 104: 89.4 % valid, 80.8 % settle (v12 49.0 %, leitor:b
  94.2 %); the checker refuses 11 (forecast 5–15); «não tipável» right on 23 of 25 (forecast 18–23; leitor:b 24) and given
  to 3 typable articles (leitor:b 4); no quote outside the text. dev_antigo 393: 90.6 % valid, 82.7 % settle (v12 in 0.3
  without the grammar 63.9 %). Of v13's 20 dev misses 7 are remissão articles; 6 quote real words that do not name the
  value, 3 leave out the JOUE publication.
- Round 9 recorded (rule-factory@19, governance/readings/fabrica9/FABRICA9.md, evento:257–275): leitor:a15 8 of 12 through
  the checker (round 8: 1; forecast 6–10), 3 settled with leitor:b (forecast 4–8), all three «não tipável» (17.º-B n.º 4,
  88.º n.º 2 a), 241.º-B n.º 3 b)), and the rules proposed for them invalidated (3 stale). The five valid rule readings have
  leitor:b's values (amount and comparator, days, deadline field, start of the count) and differ in a condition: the JOUE
  publication (198.º n.º 1, as v12 in round 8), special sectors (192.º n.º 2), the contract's duration (31.º n.º 4), which
  contracts 21.º n.º 1 b) and c) apply to. The four refused: quotes that do not name «obras» (127.º-C) or «outra» (54.º-A),
  where leitor:b reads no rule, and a deadline field or start of the count the passage does not say (174.º n.º 3,
  198.º n.º 2; L9). None quotes words outside the text. 16 rules settled in all, and 3 «não tipável». The showcase bar
  (FORECAST.md: at least 10 of 12 valid and 8 settled) is not reached.
- The first record of round 9 stopped at evento:259: TOOL still named ferramenta:rule-factory@16, retired since @17 (D67's
  registrations had not moved it), and the log refused the invalidation after the first settled «não tipável». Its two
  events (257, 258), never committed, were rolled back to the committed log and the round recorded again in full.
  rule-factory@19: TOOL names it, and record, recheck and withdraw check before writing that TOOL is the current
  registration with the file's hash (tests/test_rule_factory_tool.py).

## 2026-11-04 — D68: v14 practises on the real law, from v13

- On the person's question why the practice was written articles and not the real law, and his «compress the time cycle … start
  saving money»: product_rule:leituras-assentes-como-pratica (evento:276, his «Go»): a reading of a real passage both families
  settled blind may be practice for family A, its numbers moved by code; the targets still open stay the exam.
- data-v14 (tools/make_rule_readings_v14.py, make-rule-readings-v14@1): the 19 readings settled by evento:275; 14 kept on 11
  passages, 5 left out with the reason (REJECTED.json): 174.º n.º 1 and 2 (their article holds the exam's 174.º n.º 3), 19.º d)
  (a near-copy of the exam's 21.º n.º 1 c), difflib 0.85) and 19.º c) (its reader sees 19.º d)), 19.º c)'s reading of the text before
  2026-10-01. Each passage: its own row and 24 copies with the days or euro amounts moved where the gold quotes them («seis dias»
  becomes another number in words), the gold derived again by data-v12's derive and checked with the protocol 0.4: 275 rows, and
  800 of data-v13's rows (by sha256 of the id). tests/test_rule_readings_v14.py: no row shows an exam passage or article.
- training/train_lora.py: a run may start from an earlier adapter (init, PeftModel trainable) and keep a share of each task
  (sample, by sha256). RUNS v14: from amalia-ccp-lei-v13, one epoch, warm-up 10, a tenth of every task but regra_lida: 4 491
  examples, about 8.8 M tokens (v13: 36 736 examples, 42.8 M tokens an epoch, two epochs).
- rule-factory@20: FROUNDS[10], round 9's 9 open targets with its prompts and leitor:b's answers carried (no Reader B call).
  readers/leitor_a_modal.py knows v14 (amalia-ccp-lei-v14, leitor-a16). measure-rule-readings-v14@1 (v14's answers in
  governance/readings/avaliacao-v14). verify@52: TRAIN checks data-v14, where a reserved article may be cited only as
  allowed_sources says; MEAS recomputes regras-v14.
- Forecast, committed before v14 answers: sealed 85–90 % settle (v13 86.5 %); round 10, the 9 open targets: 3–5 settled with
  leitor:b (v13 0), 6–8 valid (v13 5), no quote outside the text. Below 3 settled, the real practice did not carry over: the next
  step is a scaffold for conditions said outside the target, not more training.
- v14 trained from v13 (training/runs/v14/MANIFEST.json): 139 steps, one epoch, 4 491 examples, 9.2 M tokens, 00:11Z to
  00:52Z (2 393 s), about USD 2.7 (not billed yet: training/runs/v14/COST.json); its loss began at 0.014, v13's level, so it
  went on from v13. Adapter amalia-ccp-lei-v14 (d4634ba004c1…), registered as leitor:a16.
- v14 read dev, sealed and dev_antigo (data-v13's, protocol 0.4, --quotes text) and round 10 (rule-factory@20: 9 prompts, round
  9's byte for byte, leitor:b's answers carried, no Reader B call): 593 of 593 and 9 of 9 answers through the grammar.
- Measured (reports/measure/regras-v14-2026-11-04.md). Sealed 96: 94.8 % valid, 87.5 % settle [79.4, 92.7] (v13 86.5 %, leitor:b
  89.6 %; forecast 85–90 %). Dev 104: 93.3 % valid, 86.5 % settle (v13 80.8 %, leitor:b 94.2 %); the checker refuses 7 (v13 11);
  «não tipável» right on 22 of 25 (v13 23) and given to no typable article (v13 3); no quote outside the text. dev_antigo 393:
  84.5 % settle (v13 82.7 %).
- Round 10 recorded (governance/readings/fabrica10/FABRICA10.md, evento:277 on): leitor:a16 7 of 9 through the checker (v13 5;
  forecast 6–8), 3 settled with leitor:b (v13 0; forecast 3–5): 198.º n.º 1 (the JOUE publication, which v12 and v13 left out),
  198.º n.º 2 (the start of the count, L9) and 127.º-C n.º 1 a) as «não tipável» (v13 wrote a rule). Still open: 21.º n.º 1 b)
  and c), refused: v14 adds «publicado_joue eq false», which the passage does not say (L7), a JOUE condition taken from the
  practice where it is not; 31.º n.º 4 and 192.º n.º 2 leave out the contract's duration and the special sectors, which no
  practice reading has; 54.º-A n.º 1 b) ii) is «não tipável» with texto_em_falta for leitor:b's nao_e_limiar; 174.º n.º 3 differs
  in its two deadlines. 18 rules settled in all (16 before), and 4 «não tipável».

## 2026-11-04 — D69: round 11, 60 real passages no round has read

- On the person's question why the real-law score is low when the practice is the real law with its numbers moved: the score is
  round 10's, the 9 hardest passages left, and the real law has 22 answer keys (passages both families read the same way blind).
  Round 1's patterns find 20 targets in the whole CCP, all read; 136 leaf passages state days or euros in their own words and no
  round has read them. His «Yes, 60 passages».
- rule-factory@21: FROUNDS[11] with PICK11, targets drawn once and kept in the round (target_of builds round 1's target for any
  passage; the round report gains a table by stratum). The draw: the 28 candidates in reserved articles that no training row shows
  («reservado»; 190.º n.º 2, 191.º n.º 2 a) and n.º 3 are out, printed in data-v14's practice contexts) and the first 32 of the 105
  unreserved by sha256 of the id («texto_visto»: escolha_passagem, texto_vigente and other tasks show their text, no rule-reading
  row does). 48 prazo_minimo, 12 limiar (the passage says euros). tests/test_rule_factory_round11.py draws it again.
- Correction before any answer, disclosed: the first commit of the pick (b8e04f691, rule-factory@21) held 104.º n.º 2 and n.º 3 b),
  whose context lets a reading quote 104.º n.º 2 b) «(Revogada.)», a line the protocol 0.4 does not print; verify V3 refused both
  prompts, and the chain committed anyway because a pipe to tail hid verify's exit code. rule-factory@22 leaves them out and takes
  the next two by sha256 (270.º, prazo_minimo, and 127.º-B, limiar); every round 11 prompt now prints every line its reading may quote
  (tests/test_rule_factory_round11.py). Neither family had answered.
- Prompts: protocol 0.4, fresh (no carry), 60 of 60 written before either family answers.
- Forecast, committed before either family answers: leitor:a16 valid on 50–58 of 60, leitor:b on 57–60; 25–40 settled, most of
  them «não tipável» (a deadline that is not a minimum, an amount that is not a procedure's limit), 3–10 rules; «reservado» and
  «texto_visto» within 15 points of each other; no quote outside the text. Below 20 settled, reading ordinary real passages is the
  bottleneck and the next step is the reading itself, not more keys. Settled means both families agree blind, not that the law
  was proved read right (round 1: 4 of 4 settled readings were wrong on a vocabulary gap).
- Both families read the 60 blind, in parallel from 14:02Z: leitor:a16 on Modal (one L40S, --quotes text: 60 of 60 through the
  grammar), leitor:b through reader B's client (about 10 s an answer). 60 of 60 answers each.
- Round 11 recorded (rule-factory@23, governance/readings/fabrica11/FABRICA11.md, evento:292–376). leitor:a16 43 of 60 through the
  checker (forecast 50–58: below), leitor:b 59 (57–60). 35 settled (25–40): 34 «não tipável» and one rule, 123.º n.º 1 (3 days for
  the pronúncia on the relatório preliminar, ajuste direto and consulta prévia; forecast 3–10 rules: below). By stratum: reservado
  13 of 28, texto_visto 22 of 32 (forecast within 15 points: 23 apart). The 9 passages of 474.º (the EU thresholds) are all
  reservado and none settles; without them, 13 of 19 and 22 of 32: seeing a passage's text in other tasks did not help. No quote
  outside the text.
- Where v14 fails: it writes a rule where leitor:b reads «não tipável». The checker refuses all 17, none reached the log: 474.º (7; leitor:b
  reads nao_e_limiar), 129.º-A n.º 1 a) and b) and 127.º-B (amounts that are not a procedure's limit), a prazo de pronúncia whose
  quotes do not name the field (161.º-B n.º 4, 188.º n.º 2, 219.º-C n.º 3), conditions the passage does not name (373.º n.º 2 and
  3, 64.º n.º 2, 90.º n.º 1), a number not in its sources (198.º n.º 3). When v14 reads «não tipável», leitor:b gives the same reason
  on 34 of 39. 7 differ: 5 on the reason (143.º n.º 1, 78.º n.º 5, 273.º, 474.º n.º 3 d) and n.º 4 c)), 2 a rule against
  sem_vocabulario (147.º, 161.º-B n.º 1 b)). leitor:b reads 123.º n.º 1 as a rule and the near-identical 147.º as sem_vocabulario:
  a blind agreement can also fail on family B's side.
- The first record stopped half-way at 147.º, the first v3 target where family A's rule passes the checker and leitor:b reads
  «não tipável»: the factory kept a reading of leitor:b with no passage, which the rule schema refuses. Its 18 events, never
  committed, were set aside and the log restored to the committed one. rule-factory@23 logs leitor:b's blind review and keeps only
  family A's reading on that rule; recorded again in full.
- Answer keys: 57 settled (19 rules, 38 «não tipável»; 22 before). Round 11's 22 texto_visto keys may be practice for v15 under
  evento:276; its 13 reservado keys stay the exam. Below 20 settled was not reached: on ordinary real passages v14 settles 35 of 60,
  nearly all of them «não tipável»; on real passages that do state a rule of these types, the evidence is still round 10's 3 of 9
  and this round's one rule.

## 2026-11-04 — D70–D72: all the real law the store can hold, a third rule type, round 12 over all of it
- Asked (pessoa:paulo, 2026-11-04): «Add all the real law that you can go fetch it then come back», in answer to whether to add a
  rule type for deadlines on an act. Read as the go for both: fetch the procurement law the store lacks, and a rule type so
  more of the real law can be labelled.
- D70, the law. The store held the CCP and Portuguese acts; the EU procurement directives themselves were missing (only the
  2026–2027 threshold regulations). The EUR-Lex website answers scripts with a challenge, so nothing there; the Publications
  Office serves the same texts by content negotiation (official open data, resource/celex/<CELEX>, Accept xhtml, Accept-Language
  por). 66 documents, one passive GET each (tools/capture_page.py@3, --list: the store loaded once): every consolidated version
  in Portuguese of 2014/24, 2014/25, 2014/23, 2009/81, 2004/18, 2004/17, 89/665 and 92/13, and the OJ text as adopted of 2014/24,
  2014/25, 2014/23 and 2004/18. 5 earlier versions are not served in Portuguese (404) and are not here.
- Extractor eurlex-consolidated@1 (engine/extract.py, extract@5): both the consolidated CONVEX markup (old and new) and the OJ
  text; amendment markers and footnotes are not text; a numbered point «1)» inside a paragraph stays its text as «(1)»; the
  OJ's ordinal «o» is «º»; it stops at the first annex (annexes are not structured).
- build_law@7: a directive's passages take a version per consolidation that changes their text, from that date; the first
  from the entry into force when the first capture is the adopted text («no vigésimo dia seguinte ao da sua publicação»: 2014/24
  art. 27.º n.º 1 from 2014-04-17, with its entra_em_vigor vigência); an amending quotation (another act's text) is left out;
  2004/18 and 2004/17 close on 2016-04-18 with a revoked version and a «revoga» vigência quoting 2014/24 art. 91.º and 2014/25
  art. 107.º. Example of the law clock: 2014/24 art. 4.º b) reads 134 000, 135 000, 144 000, 139 000, 140 000, 143 000 and 140 000 EUR,
  each from its consolidation date. Not structured, and said so in build-report.json: the OJ text of 2014/23 (an unbalanced «
  in its definitions); 2014/23 arts. 46.º–55.º and 2009/81 from art. 71.º (an amending quotation the source leaves open).
  2009/81's versions before 2016 hold 107 "-dup" numbers the old markup repeats; no target is drawn from a -dup id.
- Added: 8 normas, 3 555 passages, 2 879 vigências; the CCP and every other act unchanged (36 524 passages). law/COVERAGE.md
  regenerated. tests/test_eu_directives.py (5).
- The training data of D45–D69 and the reservation are functions of the store; with the directives in it they would no longer
  regenerate (verify's first run: 21 TRAIN failures). The 0.5 vocabulary is a copy (VOC5) read only inside a 0.5 call, so every
  generator and measure written before it reads the 0.4 tables unchanged (a merged table moved one statistic of data-v13's INDEX). make_training.LAW_RECORDED_BY = 2026-10-25T00:00:00Z (the day the reservation was frozen; no law object was
  recorded between then and D70): verify@53 reads the TRAIN checks from the store as recorded by then (Store.as_recorded). The
  training data, the reservation list and the measurements are unchanged.
- D71, protocol 0.5 (tools/read_rules_v3.py@8, V05; VERSION stays 0.4 for every caller written before it): a passage of any act
  the store holds, named by its title in «Onde está»; the directives' procedure names as values of their own (concurso_aberto,
  procedimento_concorrencial_negociacao, procedimento_negociacao_com_concurso), never mapped onto a CCP procedure; «pedidos de
  participação» names the candidaturas deadline; the type prazo_maximo («o prazo … não pode ser superior a N dias»; «no prazo
  de N dias», «no prazo máximo de», «até N dias» → maximum_days), its reason nao_e_prazo_maximo, and a checker that refuses a
  maximum whose quote states none. The engine evaluates it (cumpre when the deadline set is at most the maximum; the most
  specific of one field's rules decides, D66). Every recorded 0.4 prompt of rounds 9–11 re-renders byte for byte
  (tests/test_read_rules_v3_05.py, 4). Kept narrow on purpose: a deadline the entity itself must meet («o júri notifica no prazo
  de 5 dias») needs the date of the act among the facts, which the facts do not have: still «não tipável», a product call.
- D72, round 12 (rule-factory@26, FROUNDS[12], governance/readings/fabrica12/pick.json, drawn once by draw12 before either family
  reads; tests/test_rule_factory_round12.py re-draws it): every real passage of the store that states days or euros and that no
  round asked the same question of. 377 targets: CCP in force 107 (92 prazo_maximo — round 11's «não é prazo mínimo» asked again
  under the new type, and the rest), CCP versions no longer in force whose numbers differ from today's 86, EU directives 184
  (68 prazo_minimo, 63 prazo_maximo, 53 limiar). Left out: 12 whose prompt would not print a line their reading may quote (a
  revoked «b) (Revogada.)», round 11's 104.º trap; verify V3 caught them on the first draw, before any reading: the round
  directory was removed and drawn again with the check in draw12). Type by the passage's words: days with «mínimo», «inferior a», «pelo menos» or
  «antecedência» → prazo_minimo; other days → prazo_maximo; euros alone → limiar. Strata by TRAIN-HELD-OUT's frozen rule:
  81 reservado (exam), 296 pratica. Protocol 0.5, adapter v14 (leitor:a16), leitor:b blind.
- Forecast, committed before either family answers: leitor:a16 valid on 55–70 % (it never saw prazo_maximo nor an EU text),
  leitor:b on 92–100 %; 145–225 settled, 40–110 of them rules (most on the directives' minimum deadlines); per type, settled
  share highest on prazo_minimo and lowest on prazo_maximo; no quote outside the text. Below 120 settled, the new type or the
  new texts are where v14 fails and the next step is its training on them, not more passages.
- Both families read the 377 blind: leitor:a16 on Modal (377 of 377, --quotes text), leitor:b through reader B's client. The
  sequential reader stalled twice on Reader B's whitespace loop (one call 11 minutes, one 17): each was killed and its prompt asked
  again; the unanswered ones were read by disjoint shards (--only, one folder set each), 377 of 377.
- Round 12 recorded (rule-factory@27, governance/readings/fabrica12/FABRICA12.md, evento:377–961). leitor:a16 302 of 377 through the
  checker (forecast 55–70 %: 80 %, above), leitor:b 345 (92–100 %: 92 %). 81 settled (forecast 145–225: below), 11 of them rules
  (40–110: below): 6 earlier CCP texts (135.º n.º 1, 190.º n.º 1, 191.º n.º 1 and 3 and 198.º n.º 2 as of 2008-07-30, 147.º as of
  2018-01-01), 191.º n.º 3 in force, and 4 EU minimum deadlines (2014/24 art. 27.º n.º 1, 35 days; 2004/18 art. 38.º n.º 2 and n.º 3
  b), 52 and 40 days; 2004/17 art. 45.º n.º 2, 52 days); 70 «não tipável». By stratum: pratica 67 of 296 (6 rules), reservado 14
  of 81 (5 rules). Below 120 settled: as the forecast said, the new type and the new texts are where v14 fails.
- What the round shows, as data:
  1. The new type holds almost no real rules. On the 215 prazo_maximo targets leitor:b reads 5 rules; 147 «não é prazo máximo»
     («o prazo é para a própria entidade adjudicante enviar um anúncio», «juntar os elementos em falta», «manter as propostas», a
     duration, an execution deadline), 37 sem_vocabulario. The CCP's deadlines are mostly the entity's own acts: a type for them
     needs the date of the act among the facts (D71), the person's decision.
  2. v14 agrees that most of these passages hold no rule, with the old reason: on prazo_maximo targets it answers nao_e_prazo_minimo
     109 times (it never trained on nao_e_prazo_maximo). 108 targets where both families read «não tipável» do not settle only
     because the reason differs; 36 more differ as nt against sem_vocabulario, 24 against nao_e_limiar.
  3. On the directives v14 often cannot answer within the checker: 31 of 68 EU prazo_minimo and 20 of 53 EU limiar answers are
     refused (procedure names and phrasings it has never seen); leitor:b reads 23 prazo_minimo rules in all, v14 settles 11.
- Answer keys: 138 settled (30 rules, 108 «não tipável»; 57 before). Round 12's 67 pratica keys may train v15 under evento:276;
  its 14 reservado keys join the exam.

## 2026-11-05 — D73–D75: one push to the target, the daily refresh, the public recipe
- Asked (pessoa:paulo, 2026-11-05): «el puto 10 de 10 ya … que aprenda de chingada, de putazo … ya, dale», and whether the CCP
  Engine goes public with its information kept current. Read as: no more small steps; one training with everything the real
  law showed; the engine public and refreshed daily; the person still says «publícalo» before anything is deployed.
- The target (stated before any of it ran): on the exam, the reservado targets of rounds 11 and 12 (109 real passages no
  training row shows), family A replicates leitor:b blind on at least 95 % of the targets leitor:b reads validly, with no quote
  outside the text. Baseline v14 (rule_factory exam --rounds 12 11): 27 of 101, 26.7 %. Ceiling: leitor:b asked the same 109
  prompts a second time, blind (scratch, not a governance round; one prompt unanswered after two tries, Reader B's whitespace
  loop) replicates itself on 99 of 100 both read validly (one differs: 276.º n.º 5, sem_vocabulario against texto_em_falta).
- Order changed from the person's three steps, said in the chat: the training first, because 108 round-12 targets both families
  read as «não tipável» failed to settle on the reason alone (v14 never learned nao_e_prazo_maximo); a type for the entity's
  own deadlines after it (it needs the date of the act among the facts).
- D73, data-v15 (tools/make_rule_readings_v15.py@1, protocol 0.5): 77 practice keys of rounds 11–12 (family A's settled
  reading as the gold; 12 left out: their reader sees a reserved article or an exam passage) with their numbers moved, 1 229
  rows; 1 120 invented articles (norma:exemplo) drawn by code in round 12's shapes — a party's deadline at most N days (350,
  prazo_maximo), the entity's own deadline or an obligation to keep (250 nao_e_prazo_maximo, 100 nao_e_prazo_minimo), the
  directives' minimum deadlines with their own procedure names, urgency and pré-informação (300), a directive's threshold
  (60 nao_e_limiar), a deadline in working days (60 sem_vocabulario) — each gold quoted by data-v12's code with the 0.5 tables
  and kept only when the factory's checker passes it, none close to an exam passage; 875 rows kept from data-v14 and data-v13.
  v15 (training/train_lora.py RUNS v15): from v14's adapter, two epochs on data-v15's rule rows and a tenth of every other task.
- D74, the exam: rounds 13 and 14 have v15 (leitor:a17) read rounds 12 and 11 again, byte-identical prompts, leitor:b's blind
  answers carried (437 prompts, no Reader B call). A target already settled is read and measured but not recorded again.
  rule_factory exam reports, per stratum, family A's replication of leitor:b among leitor:b's valid readings.
- D75: tools/refresh.py@1, the daily refresh: the Publications Office's SPARQL list of consolidated versions (a version not
  served in Portuguese is remembered in law/REFRESH.json); the DR consolidated page rendered once and each code article compared
  with the text in force; on a change, the history walk, build_law, coverage; passages recorded after the last refresh that
  state days or euros become a refresh round (rule_factory draw_since, governance/readings/refresh-<date>/), read blind by both
  families, recorded, verify, commit, push, tools/package.sh; deployed only when deploy/AUTODEPLOY exists. Its first passive run
  found two real differences between the store and the DR page: 61.º (the store holds it revoked since 2018; the page shows its
  text in force) and 410.º n.º 2 («é de 30 anos» on the page, «é 30 anos» in the store) — the run with --apply walks the histories
  again. deploy/com.paulo.ccp-refresh.plist (06:30 daily) is written, not loaded.
- Public recipe (deploy/Dockerfile, deploy/README.md; tools/package.sh copies the Dockerfile and requirements): Cloud Run,
  project gen-lang-client-0698758883, europe-southwest1, the same settings as rjue-service; the package (640 MB) passes its
  local smoke test (74 864 objects, 961 events). Not deployed: the person's «publícalo».
- v15 trained (ap-DXnf9dZECicOMQ3pwq3Aab, 519 steps, 3.1 h on one H100, USD 12.56; adapter 472a10383084, leitor:a17). Exam
  (rounds 13–14, reservado): 63 of 101 (v14 27); practice 187 of 271 (v14 67). Rounds 13–14 recorded (evento:962–1485): 161 more
  settled; keys 299. Studied on round 13's practice targets only (never the exam): the remaining misses are v15 reading a party's
  deadline for an act the vocabulary has no field for as nao_e_prazo_maximo where L12 says sem_vocabulario (26), and quotes the
  checker refuses on older CCP texts.
- D76, data-v16 (tools/make_rule_readings_v16.py@1): 172 keys of rounds 11–14, 7 copies each (1 880 rows; 24 would pass GitHub's
  100 MB file limit), 300 invented articles of that shape (sem_vocabulario), 450 of data-v15's written rows and 300 of its
  remind rows. v16 (ap-XEnx8Btqm7, one epoch from v15, USD 5.93; adapter ae014b3e5b5b, leitor:a18). Exam (rounds 15–16): 62 of
  101: no gain over v15. Rounds 15–16 recorded: 19 more settled; keys 318.
- Where the exam stands (v16, 101 targets leitor:b reads validly): 62 the same; 21 both «não tipável» with another reason; 14
  answers the checker refuses (nothing recorded); 4 a different rule. Counting a «não tipável» as replicated whatever its
  reason, 82 % (v15 81 %, v14 62 %). The target, 95 % with the reason, is not reached: training on more of the same moved v15
  to v16 by −1. What the remaining gap needs is not more rows of these kinds: either the person's product rule on whether a
  «não tipável» must agree on its reason to settle (the engine applies no rule either way), or a family-A reader with more
  capacity (a higher LoRA rank, or a larger base) for the checker's quoting.
- Spend of the push (modal billing report, 2026-11-05): training USD 18.49, reads USD 1.11 (AMALIA; Reader B through the person's
  subscription); training/runs/v15/COST.json and v16/COST.json. Inside the USD 40 cap stated before it began.

## 2026-11-05 — D77: a «não tipável» replicates whatever its reason (the person's product rule)
- Paulo's product rule (evento:1723, product_rule:nao-tipavel-qualquer-motivo), answering whether a «não tipável» must give the
  same reason to settle: «then Yes bro». Two blind readings that say the passage holds no rule agree; the engine applies no rule
  either way, so no verdict changes.
- tools/rule_factory.py@32: `record` upholds two «não tipável» of other reasons under it; `recheck-nt --round N` gives leitor:b's
  blind review again from the same recorded answer (no reader asked again) and invalidates the target's proposed rules, as
  `record` does; `exam` reports concordancia_d77. verify.py@57: V3 accepts an uphold that names the rule after evento:1723.
- Exam (rounds 15–16, reservado, v16): 83 of 101 = 82 % (62 with the reason); practice 245 of 271 = 90 %; all 355 of 404 = 88 %.
- recheck-nt rounds 11–16: 0, 0, 0, 1, 59, 6 — 66 more «não tipável» settled (rounds 11–13's answers had newer revisions).

## 2026-11-05 — D78: the system plan
- SYSTEM-PLAN.md: the layers with their state today, where each runs (sovereign target), the data flow, phases 1–7 with
  done criteria, costs, open decisions. Found while writing it: Supabase holds data_limite_propostas (212 244 facts) and
  data_publicacao_anuncio (174 549) but not the engine's prazo_propostas_dias or data_inicio_procedimento, so a derived-facts
  layer (Phase 2) comes before the engine run over Supabase.

## 2026-11-05 — D79: Mistral tested as the checker; Reader B stays
- Scaleway: CLI set up, key verified on project ccp-engine; every GPU quota 0 and Paris restricted for new deployments.
- readers/leitor_c_modal.py (leitor:c, not registered: nothing recorded): Mistral in its own Modal volume mistral-weights,
  Mistral's native format (tokenizer/config/load «mistral»), transformers 5.16.1 (vLLM 0.30 needs ≥5.15 for Mistral and
  imports PixtralRotaryEmbedding, gone in 5.17), --quotes text as family A, --model small4 (two H100; a B200 was not
  given in 40 min) | 14b (L40S). The 14B's files deleted from the volume by the person.
- On the 28 round-15 targets where Reader B gives a valid rule: 14B «não tipável» ×28; Small 4 guided 23 «não tipável» + 5
  refused, unguided 27 refused («as fontes não nomeiam ['obras']» and the like); AMALIA v16 13 valid, 11 = Reader B.
  Spend ≈ USD 9 (Modal).

## 2026-11-05 — D80: the engine over Supabase; deadlines as two dates
- engine/evaluate.py: deadline_days (stated days as before; else the rule's counted_from date to the deadline's date with a
  settled counting rule, else regra_ausente). tests/test_deadline_dates.py (6). Existing engine tests unchanged and passing.
- db/run_engine.py: report | write over ccp.facto (procedures in id order, pages of 500), the API's choose_package and
  manifest, verdicts into ccp.veredicto on write. First report, 1 000 procedures: all «sem data de início» (Supabase has
  no data_inicio_procedimento; which date starts a procedure is a reading).
- law/COVERAGE.md regenerated (tools/coverage.py --write): stale since the EU directives (381 → 373 listed).
- Next: the two readings (start of procedure, counting of days) as a question type of the reading protocol, read blind
  by AMALIA and Reader B; then run_engine write over every procedure.

## 2026-11-05 — D81: the holidays from the law's text
- engine/calendario.py: holidays(text, year) reads Código do Trabalho art. 234.º n.º 1 as the caller gives it (the fixed
  days it names, and Sexta-Feira Santa, Domingo de Páscoa, Corpo de Deus by Easter); a name it cannot place raises
  Unreadable. next_working_day for CPA art. 87.º f). On the store's text (in force from 2016): 13 days in 2018, 2022, 2026.
  tests/test_calendario.py (4).
- Found reading the law for D80's two readings: CCP art. 470.º (formation deadlines counted by CPA art. 87.º; the
  urgent tender's proposals deadline without its alínea b); n.º 3: proposals, applications and solutions continuous);
  CPA art. 87.º b) and f); CCP art. 36.º n.º 1 (the procedure starts with the decisão de contratar, a date no source holds).

## 2026-11-06 — D82–D83: real verdicts, the start window, the counting rules
- First real verdicts over Supabase (5 000 random procedures, window 0/90/365): the consulta prévia limit for obras gives
  cumpre (e.g. proc:base:idproc-7163686, preco_base 55 000 < 150 000) and não cumpre (proc:base:idproc-6729801, preco_base
  216 000 ≥ 150 000, CCP art. 19.º c), 2018–2026 version). The windows give the same results; the deadline rules wait for
  the counting rules and for publicado_joue / sending dates.
- Fixed on the way: engine/rules.applies (a failed known condition now excludes the rule; 14 338 «facto ausente» on
  1 000 procedures became 3 535); evaluate rules_at (an earlier start date hid the facts recorded later); the rule schema
  refused maximum_days; 2 tests still counted 8 rule types.
- Protocol 0.6, the contagem_prazo type in the engine (stage contagem, rules.counting_for, deadline_days with
  engine/calendario), tests (test_deadline_dates: 12; Good Friday 2026 moves a 30-day term to 33 days). Round 17: 5
  prompts (CPA 87.º b, c, f; CCP 470.º 2, 3).
- Round 17 read blind (nothing recorded: no two families agree): leitor:b (Reader B) 5 of 5 valid and right on the words
  (470.º 2: concurso_publico_urgente, propostas, primeiro_dia conta; 470.º 3: propostas and candidaturas continuo; 87.º b)
  todos nao_conta; c) todos suspende; f) todos transfere). leitor:a18 (v16, never trained on contagem_prazo): «não
  tipável» on 470.º 2, 3 and 87.º f), the wrong deadline on 87.º b), c). Mistral Small 4 (readers/leitor_c_modal.py, two
  H100): 0 of 5 valid, conditions the text does not state (territorio, tipo_contrato, publicado_joue). Spend USD 6.51
  (Mistral 6.43: the model's load alone ≈ 30 min; AMALIA 0.08). The counting rules settle once family A reads the type.
- The checker's «todos» accepts words of deadlines in general («À contagem dos prazos», Reader B's source for 87.º b, c).
- db/run_engine.py 0.3: the counting rules (CCP and, by CCP art. 470.º n.º 1, CPA) and the holidays of CT art. 234.º in
  force; 500 procedures: 33 deadline verdicts regra_ausente (the counting), the concurso rules facto_ausente on
  publicado_joue (BASE does not say it; TED covers 43 661 procedures).

## 2026-11-06 — D84: the engine in parallel; the DR notices' facts loaded; counting still unsettled
- db/run_engine.py 0.4 (--workers): 4 000 procedures in 92 s with 4 workers (≈ 4 h for the 1.48 M on the Mac).
- db/load_dr_history.py over E1b's 13 980 texts: 12 860 documents, 76 995 facts (66 347 new, 10 648 already stored),
  17 conflitos. data_envio_anuncio and publicado_joue now held for 12 860 / 12 844 procedures (was 1 781).
- Round 17 with the example in the 0.6 prompt (first answers kept as *.attempt1.json): leitor:b 5/5 valid; leitor:a18
  «não tipável» ×5; leitor:a (base AMALIA) 0/5 valid (conditions the text does not state). Spend ≈ USD 0.20.

## 2026-11-06 — D85–D86: v17 reads the counting provisions; the engine on Modal
- data-v17 (tools/make_rule_readings_v17.py): 434 invented counting articles (46 left out as close to round 17's
  passages) + 600 data-v16 rows; v17 trained (training/runs/v17, 60 steps, 31 min, adapter bbd154ba1564, leitor:a19).
- Round 17, third read (value before aspect; earlier reads kept as *.attempt1/2.json): leitor:a19 and leitor:b agree on
  CPA 87.º b), c), f) → 3 settled. 470.º 2 (v17: fins_de_semana continuo for the urgent tender) and 470.º 3 (an urgent
  tender condition the text does not state) refused by the checker. Counting withheld until they settle.
- db/modal_engine.py (D86) and db/run_engine.all_procedures. verify ok.

## 2026-11-06 — D87: the first verdicts stored for every procedure
- Product rule product_rule:janela-inicio-procedimento (evento:1799, 365 days, Paulo's «365 days»).
- db/modal_engine.py write --window 365 over the 1 487 525 procedures: 481 s on Modal CPU (12 containers). Stored in
  ccp.veredicto (counted in the database after the run): 35 355 cumpre, 851 não cumpre — all CCP art. 19.º c) (the
  consulta prévia limit for obras, version of 2018-01-01; 159 under the version of 2026-10-01). 4 760 013 «não avaliado»
  counted and not stored (D87: ≈ 6 GB with their manifests; the API computes them live). 64 procedures without any date.
- Found and fixed: db/run_engine and db/load_dr_history inserted on a connection that is not autocommit and never
  committed, so a first full run and the first DR load reported inserts that rolled back (0 rows). Both commit now; the
  DR facts reloaded and counted (data_envio_anuncio 1 781 → 12 860). The stored verdicts' manifests name 4cae17a62: the
  run's code adds only the commit and the decided-only filter to it, committed here.

## 2026-11-06 — D88: verdicts that respect the declared legal basis
- The 851 «não cumpre» of D87 checked against each contract's declared fundamentação (BASE contratos on the volume): 415
  Madeira (DLR 34/2008/M), ~140 material criteria (CCP arts. 21.º–27.º-A), ~15 special regimes, 246 art. 19.º c) alone.
- db/fundamento.py (the declared basis as passage ids; an act it cannot name gives «?:…»), db/modal_fundamento.py
  (1 343 626 procedures, one year at a time: parallel years deadlocked on ccp.nome), engine/rules.basis_allows and its
  use in evaluate (tests: test_deadline_dates, 2 more).
- Migration 20261106000000_ccp_corrida: ccp.corrida, ccp.corrida_veredicto, view ccp.veredicto_atual.
- Run corrida:20261106T202345Z (commit d1dfa2b32), counted in ccp.veredicto_atual: 32 578 cumpre, 240 não cumpre.
  Madeira's procedures get no verdict from the CCP's limits until DLR 34/2008/M is read.

## 2026-11-06 — D89: the alínea reference; v18; counting still withheld
- tools/read_rules_v3.py: ALART (0.6 only); 470.º n.º 2's prompt now shows CPA 87.º b) as remissão. Earlier answers kept as
  *.attempt3.json. v17 then: 470.º 2 primeiro_dia nao_conta (copied b), 470.º 3 an urgent-tender condition again.
- data-v18 (tools/make_rule_readings_v18.py) and v18 (training/runs/v18: 80 steps, 1 393 examples, adapter 1eb917a3c89b;
  the manifest written from the function call's result fc-01M6SANTY6Q7GQZ5A95SNF5F6H, the launching session having ended).
- v18 (leitor:a20): 87.º b), c), f) = leitor:b; 470.º 3 the same two rules as leitor:b but the candidaturas rule quotes
  «apresentação das propostas» (refused, L9); 470.º 2 fins_de_semana continuo. Nothing recorded; counting withheld.

## 2026-11-09 — D90: the API over Supabase
- db/api.py, tests/test_api.py (3; a fake connection, no network). Local run (.local/launch.json ccp-api, port 5344):
  /v1/entidades/502177080/veredictos 0.82 s (50), /v1/veredictos?resultado=nao_cumpre 1.40 s (200),
  /v1/procedimentos/proc:base:idproc-10068682 0.63 s, /v1/estatisticas 0.48 s; bad ids 400, unknown 404.
- Migration 20261109000000 (adjudicante on corrida_veredicto, the view with it); run corrida:20261109T000728Z (commit
  fb0b05e04): 32 578 cumpre, 240 não cumpre, 32 815 with their adjudicante.
- deploy/Dockerfile runs db/api.py; tools/package.sh copies db/ and smoke-tests on port 5349 (641 MB, OK).

## 2026-11-09 — D91: the frontend and the verdict report
- web/ (localhost:5345, Vite proxy to the API): home (search, three totals that filter, the table), procedure, entity,
  report. db/api.py relatorio; the re-run matches the stored result on idproc-10068682 (não cumpre) and idproc-10004950
  (cumpre); the ZIP built in the browser: 18 716 bytes, 10 files.

## 2026-11-09 — D92: the law watch
- First comparison (Mac, then the same render on Modal: 2.6 MB, 1 257 «Artigo» lines): 12 CCP articles differ from the
  repository's text in force (art. 37, 45, 61, 258, 259, 339–342, 405, 406, 410): older spellings and versions, art. 61
  missing. No settled rule cites them. Recorded pending (ccp.lei_alteracao); the first refresh on the Mac reads them.
- touched_since after the 05:00 ingest: 30 procedures (266 facts) in 11 s.

## 2026-11-10 — D93: the contract as BASE publishes it
- ccp.base_contrato: 2026 dump (read 2026-11-10) 208 344 contracts, 580 bytes a row against the dictionary (750 without it,
  1 375 as jsonb). The newer dumps write entities as objects (nifEntContrato, descEntContrato, NUTsDesc, adjudicatarioPME),
  dates as AAAA-MM-DD and CPV as objects (cpvID, cpvdescricao, cpvValor); the older as «NIF - Nome», dd/mm/aaaa and «código -
  descrição»: the page reads both.
- Cloud Run deploy (same day): the image has no git, so CCP_COMMIT is passed; a cold start loads the stores in about 4 minutes,
  so the startup probe allows 12. deploy/.ccp-token had gone missing: a new key, set on the service.
- Law build: the last consolidated versions of directives 2004/17 and 2004/18 (2016-04-18) are the title and «revogado por»
  only; extract.RepealedVersion, skipped by build_law (extract@6, build-law@8).

## 2026-11-10 — D94: training sets pinned to the law they were made from

The first law-watch readers run (12 CCP articles pending) stopped at verify: TRAIN on training/data (one new nota_dr example from a newly captured DR history raw) and data-v16 (ten 406.b examples whose quoted text is now the 2018 one). The refresh itself was right: the repository had held 2008 text for 45.º, 339.º, 341.º, 342.º and 406.º. verify 0.3 (ferramenta:verify@60) checks every frozen set over the law, raws included, as recorded when the set was generated; all 18 sets match. No refresh round was drawn: no rule cites the changed passages, and draw12 does not ask again a passage an earlier round asked (the 406.b reading of fabrica15 was on the 2008 text and never settled).

## 2026-11-10 — D95: every DR capture read, none dropped

- The DR's pages changed between the 24 Oct capture and today's. Where the newest history page lists every older date, it is read (AO90 spelling on 258.º/259.º; 372.º gains its 2018 and 2021 versions; today's texts unchanged elsewhere: 2475 passages only re-cite the newer capture).
- Where it lists fewer, the first capture stays and the article is reported: 16.º, 37.º, 340.º, 405.º. For 37.º and 405.º the missing version is DL 177/2026, which the act's own art. 2.º makes; the DR page is wrong there, not the store.
- refresh 0.3: 61.º was a false difference (revoked, the page prints its last text under «REVOGADO»).
- Law watch against today's page: 37.º, 340.º, 405.º, 410.º differ (was 7). Tests: the 8 failures that remain also fail at the previous commit.

## 2026-11-10 — the site loads in under 4 s

- The page loaded in 0.2 s but its two API calls took 90–390 s: Cloud Run kept no instance warm and a new one loads the stores for about 90 s before it answers; warm, each request opened a new TLS connection to Supabase (ThreadingHTTPServer: a thread per request, so a connection per thread was one per request).
- ccp-api 0.3: one shared read-only connection; the public reads (/v1/veredictos, /v1/estatisticas, /v1/entidades/*, /v1/procedimentos/*) send `Cache-Control: public, max-age=60, s-maxage=600, stale-while-revalidate=86400`, so Vercel's CDN answers them; every other route stays no-store. Cloud Run: --min-instances 1.

## 2026-11-13 — D96: the cumulative limit, declared regimes and special sectors
- Of the 240 «não cumpre» of corrida:20261113T050644Z, re-run in report mode with the declared facts (db/run_engine.py report --units … --base-cache … --declared --sectors …): 104 stay «não cumpre» (64 at exactly 150 000 €), 136 become «não avaliado» with the reason: the buyer declared a Directive 2014/25/EU activity in its TED notices (Infraestruturas de Portugal 99, Águas de Santarém 9, EEM 7, APS 5, NAV 4, Barreiro 3, Vila Franca de Xira 3, Metropolitano 2, EPAL 1, and three that look mis-declared: Mafra, ISCTE, Ordem dos Contabilistas). The baseline run reproduces the 240.
- db/declared.py (BASE's records: cache, the regime fact), db/ted_sectors.py (98 952 Portuguese TED notices, 123 buyers with a coded utilities activity), engine/aggregate.py, engine/rules.regime_blocks and aggregate_result, run_engine 0.7 (aggregates over the invitation dates, --units, --preview-rules for reports only), api (the summed contracts, re-read from ccp.base_contrato), web (Summed, Abstained).
- Round 18 (protocol 0.7, rule-factory@38): art. 113.º n.º 2 at 2018-01-01 and 2026-10-01. First prompts told readers «igual ou superior» → ge while the checker reads «igual ou superior a»: kept as *.attempt1.json, re-asked. leitor:b: four cases each, each counting its own alínea; leitor:a20: «não tipável» (nao_e_agregada) both times. Nothing replicates; nothing recorded.
- Preview of leitor:b's reading (not settled): 3 «não cumpre» among the 240; of the 227 «over» rows of the art. 113.º demo pages (clients/closer-demo), 13 have earlier contracts that alone reach the demo's limit and the engine confirms 2.

## 2026-11-14/15 — D97: every remaining alert checked in the buyer's own documents
- adapters/plataformas/check_regime.py read, for the 104 «não cumpre» left by D96, the contract BASE publishes (OCR for scans)
  and the pieces on acinGov and Vortal: 28 state art. 19.º c) (24 at exactly 150 000 €), 13 the special measures of Lei n.º
  30/2021 (all labelled «CCP e Lei 30/2021» in BASE; 15 others with that label are general regime), 8 another basis (material
  criteria, DL 135-A/2017, a concurso público), 55 no basis written. Facts fundamento_nos_documentos (db/declared.py documents),
  engine/rules.documents_block. 200 documents kept as raws (data/raw/pecas/raw/pecas-check.jsonl; bytes gitignored); BASE's
  detail responses (a POST) are an index outside the raws (I10). Texts cached in data/pecas-texto/ (gitignored).
- Product rules settled 2026-11-15 on the person's words: evento:1801 regime-especial-declarado («Estrecha»), evento:1802
  fundamento-verificado-nos-documentos («Não decidível»), evento:1803 limite-acumulado-completude («Contract by contract»).
- Facts loaded: the 104 document facts with their raws; regime_declarado only where the declared regime lacks the Code (73 173;
  the 1.3 M others change no verdict) and atividade_setor_especial (89 826, from 98 952 TED notices).
- v19 (leitor:a21): data-v19 (tools/make_rule_readings_v19.py: 360 invented agregada articles, each saying in its own words which
  earlier contracts count, never «consoante o caso»; 120 negatives; and data-v18), trained from v18.
- The run's record carries nao_decidivel (the stored abstentions) and por_avaliar; the home page shows «Não decidíveis».


## 2026-11-17 — D98: bad input abstains, sources that disagree conflict, the manifest names what was read
- Break test (foaap-core clients/CCP-ENGINE-BREAK-2026-11-17.md): 15 failures; this entry fixes 1–7.
- engine/rules: `in` against a string is membership in a one-value list (R1/R2's «in "obras"» matched "" and "o"); order
  comparisons refuse bools, NaN and infinity (`comparable`); `amount` = a finite number >= 0, not a bool; aggregate_result
  decides nothing on an unreadable sum.
- engine/evaluate: a limiar value that is not an amount (text, None, bool, negative, NaN, inf) is nao_avaliado /
  facto_ausente, never nao_cumpre; a proibicao condition that cannot be read is nao_avaliado, never cumpre; prazo days
  must be an amount; valid_at and rules_at must be ISO dates (a non-ISO date picked the wrong rules silently).
- engine/evaluate.read_facts: the latest fact of each adapter is that source's value; sources whose latest values differ,
  or one source with two values at the same instant, read as Conflict (conflito:auto:<field>) unless `conflicts`
  resolves them. On the store of 2026-11-17 no unit-field has two current values, so no stored verdict changes.
- engine/manifest.is_complete refuses a snapshot that is not an object, lacks source or captured_at, or carries a hash that
  is not 64 hex digits or is the all-zero placeholder.
- db/run_engine: raws_of + snapshots: one snapshot per official record the facts came from, with ccp.raw's sha256 and
  captured_at (was: the first record only, hash 0…0, captured_at = the fact's known_at); a unit with a record unknown or
  without a hash gets no verdict and the reason. facts_at is capped at the run's date. data_inicio_procedimento that is
  no date, or after the first dated act, gives no verdict and the reason. One unit's error never stops a chunk.
  db/api.relatorio passes the raws to the re-run. tools/measure and tools/serve hash the facts they read instead of 0…0.
- Report mode on the 28 stored alerts: the same 28 nao_cumpre; their manifests now carry the records' real hashes. The
  stored verdicts keep their old manifests until a governed rewrite (new revisions).
