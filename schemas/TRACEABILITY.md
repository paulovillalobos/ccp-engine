# TRACEABILITY — every point of ARQUITECTURA.md has a place in code and a test

A row without a file, a symbol and a test means the scaffold is not finished. Tests under `tests/fill/` are red by design
until phase B lands (FILL-PLAN.md). `fixtures/broken/<name>` is the mutation that proves the check bites.

## §2 Invariants

| # | Invariant | File · symbol | Test · broken fixture |
|---|---|---|---|
| 1 | Immutable sources | `schemas/raw.schema.json` (`sha256`, `bytes`) · `verify.check_sources` I01 · `engine/store.Store.raw_path` | `tests/test_verify.py::test_every_broken_overlay_is_refused_with_its_code` · `fixtures/broken/i01-source-hash-mismatch` |
| 2 | Exact citation | `schemas/defs.schema.json#citation` · `verify.check_citations` I02 · `engine/passages.cite` (B1: code writes the quote) | same test · `i02-quote-not-in-passage`; `tests/fill/test_b1_copied_modules.py` |
| 3 | Verification in code, no model | `verify.py` (`MODEL_MODULES`, `check_code`) I03 | `tests/test_verify.py::test_code_guard_is_clean_and_catches_a_model_import` · `i03-model-call-in-engine` |
| 4 | AI proposes, never approves, never writes the quote | `schemas/evento.schema.json` (approve ⇒ `pessoa:`) · `engine/governance.replay` + `Log.approve` I04 · `schemas/link.schema.json` `proponent` | `tests/test_governance.py::test_machines_never_approve_and_reasons_are_required` · `i04-machine-approval` |
| 5 | Two readers of different families | `engine/governance.replay` (`LEGAL_TYPES`, blind other-family ⇒ settled) · `verify.check_governance` I05 · `principals.schema.json` `family` | `tests/test_governance.py::test_reading_settles_only_by_blind_other_family` · `i05-settled-by-one-family` |
| 6 | `nao_avaliado` before a false `cumpre` | `defs.schema.json#reason_not_assessed` (closed enum) · `veredicto.schema.json` if/then · `engine/evaluate.evaluate` (`na`) · `verify.check_verdicts` I06 | `tests/test_evaluate.py::test_without_the_selector_fact_everything_is_not_assessed`, `tests/test_schemas.py::test_verdict_reason_enumeration_is_closed` · `i06-manifest-incomplete` |
| 7 | Assertions are not facts | `schemas/afirmacao.schema.json` · `facto.schema.json` `origin` (raw or document only) · `verify.check_verdicts` I07 · `evaluate._verdict` `assertions_compared` | `tests/test_evaluate.py::test_reproduces_the_fixture_verdicts` (compared beside, never used) · `i07-assertion-used-as-fact` |
| 8 | Bitemporal | `engine/store.query(known_at, valid_at)` · `facto`/`veredicto` `known_at`, `valid_at` · `verify.check_verdicts` I08 | `tests/test_store.py::test_query_separates_known_at_from_valid_at` · `i08-verdict-before-its-facts` |
| 9 | Nothing merged, nothing overwritten | `engine/store.Writer.append/revise/mark_stale` · `Store._check_revisions` I09 · `engine/entities.merge` (raises) · `governance.replay` chain I09 | `tests/test_store.py::test_append_refuses_same_id_and_revision`, `tests/test_entities.py::test_proponent_and_event_are_required_and_merge_does_not_exist`, `tests/test_governance.py::test_disputant_never_adjudicates_and_chain_is_append_only` · `i09-overwrite-same-revision` |
| 10 | Public data, passive reading | `raw.schema.json` `request.method` = GET, `reads_of_page` ≤ 1 · `verify.check_sources` I10 · `verify.check_code` (`NETWORK_MODULES`, `SEND_PATTERNS`) | `tests/test_verify.py::test_every_broken_overlay_is_refused_with_its_code` · `i10-active-send` |
| 11 | Natural persons never published by name | `veredicto.schema.json` `entities` if/then · `engine/evaluate._verdict` (strips `name`) · `verify.check_verdicts` I11 | `tests/test_evaluate.py::test_natural_person_is_never_named_and_manifest_must_be_complete`, `tests/test_schemas.py::test_natural_person_name_is_refused_in_a_verdict` · `i11-natural-person-named` |
| 12 | Founder decides product rules, not legal content | `regra.schema.json` `completeness_threshold.decided_by` · `evento.schema.json` `product_rule` · `governance.replay` (regra never human-approved) · `verify.check_governance` I12 | `tests/test_governance.py::test_reading_settles_only_by_blind_other_family` (approve refused), `test_fixture_log_replays_clean...` · `i12-threshold-without-product-rule` |

## §3 Objects (one schema, one valid fixture, one loader entry each)

| Object | Schema · engine symbol | Fixture · test |
|---|---|---|
| Norma | `norma.schema.json` · `store.Store.objects["norma"]` | `fixtures/valid/norma/` · `tests/test_schemas.py::test_one_valid_fixture_per_object_type` |
| Pasaje (passagem) | `passagem.schema.json` (versions with offsets) · `verify.passage_text`, `store.query` (version filter), `engine/passages.py` (B1) | `fixtures/valid/passagem/` · same; `tests/test_store.py::test_query_separates_known_at_from_valid_at` |
| Vigencia de pasaje | `vigencia.schema.json` · `verify.check_citations` (note quote) · `engine/vigente.py` (B1/B2) | `fixtures/valid/vigencia/` · same; `tests/fill/test_b2_ccp_capture.py` |
| Regla | `regra.schema.json` · `engine/rules.check/order/applies/fields_of` | `fixtures/valid/regra/` (8) · `tests/test_rules.py` |
| Paquete + Diff | `pacote.schema.json`, `diff.schema.json` · `rules.package`, `rules.diff` · `verify.check_packages` PACK/DIFF | `fixtures/valid/pacote/`, `diff/` · `tests/test_rules.py::test_package_hash_and_diff_match_the_fixtures` |
| Registro crudo | `raw.schema.json` · `Store.raw_path/raw_text` · `engine/sources.record_raw` (B1) | `fixtures/valid/raw/` + `raw_bytes/` · `tests/test_verify.py::test_valid_fixtures_pass` |
| Adaptador | `adaptador.schema.json` (mapping as data, coverage per month) · `evaluate` coverage input | `fixtures/valid/adaptador/` · `tests/test_evaluate.py::test_aggregate_answers_coverage_before_facts` |
| Procedimiento / Lote / Contrato / Modificación | `unidade.schema.json` (kind, parent) · `store.facts_of` | `fixtures/valid/unidade/` · `tests/test_store.py::test_facts_of_walks_up_to_the_procedure` |
| Entidad | `entidade.schema.json` · `engine/entities.candidate_id/nif_id` | `fixtures/valid/entidade/` (publica, pessoa_singular, candidate) · `tests/test_entities.py` |
| Alias | `alias.schema.json` · `verify.check_references` | `fixtures/valid/alias/` · schema test |
| Enlace | `link.schema.json` (proposed/settled/stale, proponent) · `entities.propose_link/settle/mark_stale/links_to` | `fixtures/valid/link/` · `tests/test_entities.py::test_link_lifecycle_never_deletes` |
| Hecho | `facto.schema.json` · `evaluate.read_facts`, `store.query` | `fixtures/valid/facto/` · `tests/test_evaluate.py` |
| Afirmación | `afirmacao.schema.json` · `evaluate._verdict` (compared) | `fixtures/valid/afirmacao/` · `tests/test_evaluate.py::test_reproduces_the_fixture_verdicts` |
| Conflicto | `conflito.schema.json` · `rules.Conflict`, `evaluate.read_facts` | `fixtures/valid/conflito/` · same (limiar ⇒ `conflito`) |
| Documento | `documento.schema.json` · `evaluate` conteudo_obrigatorio branch | `fixtures/valid/documento/` · same (`documento_sem_texto`) |
| Veredicto | `veredicto.schema.json` · `evaluate._verdict` · `verify.check_verdicts` | `fixtures/valid/veredicto/` (3) · `tests/test_evaluate.py` |
| Manifiesto | `manifesto.schema.json` · `engine/manifest.build/is_complete/manifest_hash` | `fixtures/valid/manifesto/` · `tests/test_manifest.py` |
| Evento de gobernanza | `evento.schema.json` · `governance.Log._record`, `replay`, `head` | `fixtures/valid/governance/events.jsonl` · `tests/test_governance.py` |
| Disputa / Adjudicación | `disputa.schema.json` · `Log.dispute/adjudicate`, `replay.disputes` | `fixtures/valid/disputa/` · `tests/test_governance.py::test_disputant_never_adjudicates_and_chain_is_append_only` |
| Caso de referencia | `caso_referencia.schema.json` (two annotators, held_out) | `fixtures/valid/caso_referencia/` · schema test; measurement replay is after B4 (FILL-PLAN) |
| Principals (needed by Evento) | `principals.schema.json` · `governance/principals.json` | `fixtures/valid/governance/principals.json` · `tests/test_schemas.py::test_governance_fixture_validates` |

## §5 Rule types

| Type | Schema branch · engine | Fixture · test |
|---|---|---|
| Umbral (`limiar`) | `regra.schema.json` if/then `threshold` · `rules.REQUIRED_PARAMS` · `evaluate` (`multiplier`) | `regra/ccp-limiar-ajuste-direto-bens.json` · `tests/test_evaluate.py::test_jurisdiction_multiplies_thresholds` |
| Procedimiento admisible | `procedures` · `evaluate` | `regra/ccp-procedimentos-admissiveis.json` · `test_reproduces_the_fixture_verdicts` (`cumpre`) |
| Plazo mínimo | `minimum_days`, `deadline_field`, `counted_from` · `evaluate` | `regra/ccp-prazo-minimo-propostas-6-dias.json` · same (`cumpre`, 9 ≥ 6); at scale: `tests/fill/test_b4_engine_v0.py` |
| Contenido obligatorio | `required_elements`, `document_piece` · `evaluate` (documents) | `regra/ccp-programa-indica-prazo-e-criterios.json` · same (`documento_sem_texto`) |
| Prohibición | `forbidden` · `evaluate` | `regra/ccp-proibicao-fracionamento.json` · same (`facto_ausente`) |
| Agregada | `window`, `group_key`, `aggregate`, `completeness_threshold` · `evaluate` (coverage first) · verify I12 | `regra/ccp-limite-acumulado-art113.json` · `test_aggregate_answers_coverage_before_facts` |
| Selector de régimen | `selects_by`, `regimes` · `rules.order` stage `seletor` · `evaluate` step 1 | `regra/dl-177-2026-seletor-regime-dl-177-2026.json` · `test_without_the_selector_fact_everything_is_not_assessed`; `tests/fill/test_b3_rules_v0.py` |
| Jurisdicción | `territory`, `predicate`, `effect` · `evaluate` step 2 | `regra/dlr-27-2015-a-coeficiente-acores.json` · `test_jurisdiction_multiplies_thresholds` |

## §7 Three clocks

| Clock | File · symbol | Test |
|---|---|---|
| Law validity (per passage) | `passagem.versions[].valid_from/valid_to`, `vigencia` · `store.query(valid_at)` for `passagem`/`regra` · `rules.valid_at` · `evaluate` (`regime_date`) · `engine/vigente.vigente` (B1/B2) | `tests/test_store.py::test_query_separates_known_at_from_valid_at`; `tests/fill/test_b2_ccp_capture.py::test_vigente_differs_exactly_as_the_dl_177_notes_say` |
| Fact validity (`valid_at`) | `facto.valid_at`, `veredicto.valid_at` · `evaluate.read_facts` | `tests/test_store.py` (facts before `valid_at` excluded); `tests/test_evaluate.py` |
| Knowledge (`known_at`) | `facto.known_at` = raw `captured_at` (verify I08) · `veredicto.known_at` ≥ facts · `store.query(known_at)` | `tests/test_store.py` (base-api fact invisible before its capture); `fixtures/broken/i08` |
| Record clock (D2, mechanical) | `envelope.recorded_at` · `Writer.revise` | `tests/test_store.py::test_mark_stale_is_a_new_revision_not_a_delete` |
| Replay months later | `manifesto` embedded; `evaluate` requires a complete manifest | `tests/test_evaluate.py` (manifest equality with the fixture) |

## The six pieces of the 10 (builder's reading: the three fundamental changes of the 2026-10-24 revision and the three new rule types; plus the founder's "entities are their own layer")

| Piece | File · symbol | Test |
|---|---|---|
| Facts and assertions are distinct objects | `facto.schema.json`, `afirmacao.schema.json` · verify I07 · `evaluate` `assertions_compared` ("declared vs evaluated") | `tests/test_evaluate.py::test_reproduces_the_fixture_verdicts`; `i07` |
| The unit is a graph (proc → lote → contrato → mod) | `unidade.schema.json` (`kind`, `parent`) · `store.facts_of` | `tests/test_store.py::test_facts_of_walks_up_to_the_procedure` |
| The adapter is a governed artefact | `adaptador.schema.json` (`mapping` as data, `coverage`, `proposed_by`, `state`) · `evento.assertion_type: adaptador` · `governance.APPROVABLE_TYPES` | `tests/test_schemas.py`; `tests/test_evaluate.py::test_aggregate_answers_coverage_before_facts` |
| Regime selector rule | see §5 | see §5 |
| Jurisdiction rule | see §5 | see §5 |
| Aggregate rule with completeness threshold | see §5 · verify I12 | see §5; `i12` |
| Entities as their own layer | `engine/entities.py` · `entidade`, `alias`, `link` schemas | `tests/test_entities.py` |

## §4 Layers → modules, §9 API, §10 steps

| Layer / item | Where | Test |
|---|---|---|
| 0 Sources | `engine/sources.py`, `tools/capture_dr_consolidated.py` (B1) · `raw` schema | `tests/fill/test_b1_copied_modules.py` |
| 1 Law structure | `engine/structure.py`, `engine/passages.py`, `engine/vigente.py` (B1/B2) | `tests/fill/test_b1`, `test_b2` |
| 2 Rules | `engine/rules.py` | `tests/test_rules.py` |
| 3 Governance | `engine/governance.py`, `governance/` | `tests/test_governance.py` |
| 4 Entities | `engine/entities.py` | `tests/test_entities.py` |
| 5 Facts and assertions | `facto`, `afirmacao`, `conflito`, `documento` schemas · `store.facts_of` | `tests/test_store.py`, `tests/test_evaluate.py` |
| 6 Engine | `engine/evaluate.py` | `tests/test_evaluate.py` |
| 7 Measurement | `caso_referencia`, `disputa` schemas (regression class) · replay after B4 | schema tests; FILL-PLAN "after B4" |
| 8 API | `tools/serve.py` (B1 skeleton, B4 figures) | `tests/fill/test_b1_copied_modules.py::test_tools_exist` |
| §10 step 1 (skeleton, verify green on empty store) | `verify.STORES["repo"]`, `["data"]` | `tests/test_verify.py::test_empty_stores_pass` |
| §10 step 2 (CCP captured) | B2 | `tests/fill/test_b2_ccp_capture.py` |
| §10 step 3 (rules v0, two families) | B3 | `tests/fill/test_b3_rules_v0.py` |
| §10 step 5 (engine v0, first figure) | B4 | `tests/fill/test_b4_engine_v0.py` |
| §14 ownership boundary | `README.md`, `adapters/README.md`, `data/README.md` · AUDIT.md row 8 | `tests/test_skeleton.py::test_readme_states_invariants_and_boundary` |
