# Proposals for the builder from the BASE anúncios adapter (E1, 2026-10-25)

The extractor adapts the source to the schemas and does not change schemas/, engine/, verify.py or tools/. Below is
what did not fit, what was done meanwhile, and the change proposed. Counts are from the build of 2026-10-25
(adapters/base-anuncios/COVERAGE.md).

## 1. verify checks `data/` without the governance log (blocks "verify ok over data/")
- verify.STORES["data"] = [data]. That store has no principals.json, so `need_principal` fails for every principal
  data/ names: the adaptador's proposed_by and each link's proponent (I04). No adaptador can pass, and every fact needs one
  (REF). A second principals.json under data/ would make "two governance logs in one store" in the engine store, so the
  extractor did not write one.
- Meanwhile: the proposer, ferramenta:adapter-base-anuncios@1, is registered in governance/principals.json (by
  tools/register_tool.py) and the adaptador is proposed in governance/events.jsonl. `verify.py --store data governance`
  passes. The full `verify.py` reports 1 + 2 668 I04 lines on the data store and nothing else.
- Proposed: STORES["data"] = [ROOT / "data", ROOT / "governance"], as run_engine and tools/measure.py already load it.

## 2. Raw bytes kept out of git: CI cannot re-hash them (I01 in CI)
- As the brief asks, the download (23 669 469 bytes) and the 22 252 record slices live in data/raw_bytes/ (gitignored).
  Locally verify re-hashes them. In CI, `check_sources` will report I01 "bytes not in the store" for all 22 253 raws.
- Proposed (pick one): commit the slices (23 MB) and drop the dump bytes from git, or have verify accept a declared
  external bytes location for data/, or run the data store's I01 only where data/raw_bytes exists. It is a product
  decision (what the repository holds), so it is left to the person.

## 3. `engine.store.facts_of` scans every fact for each unit
- `facts_of` calls `query(store, "facto")` over all facts on every call: 0.071 s per call with 131 558 facts, measured on
  this store. tools/run_engine.py calls it for every proc (22 252 -> about 26 min) and verify's check_measure calls it
  again through measure.case_values (about 26 min more). CI's verify job has a 20-minute timeout.
- Proposed: index facts by unit once per store (e.g. a dict unit -> facts built at load or on first call). The result
  is the same; the cost goes from units x facts to facts.

## 4. entidade.type has no value for "legal person, public or private not stated"
- The dump gives the adjudicante's NIF and name, never whether it is public or private. The NIF's leading digits decide
  it only for 1, 2, 3, 45 (natural person) and 6 (public administration). Prefixes 5 and 9 (19 582 of 22 252 procedures,
  1 303 of 1 531 NIFs) do not. Writing "publica" because an entity publishes a procurement notice would be a guess
  (private entities in the special sectors publish too).
- Meanwhile: entities are written only for the 228 NIFs with prefix 6 (type publica). The `adjudicante` fact (the NIF)
  is written for every procedure with a NIF (22 250), so the held-out split by adjudicante is unaffected.
- Proposed: add a value to defs.entity_type (e.g. "coletiva": a legal person whose public or private nature the source
  does not state), or make entidade.type nullable.

## 5. adaptador.transform has no plain decimal
- PrecoBase is a dot-decimal string with no thousands separator ("318231.43"). The closest transform is `number_pt`,
  used with a note that says what the dump writes.
- Proposed: add "decimal" to the transform enum.

## 6. raw has no size field
- The brief asks for the size of the download. raw.schema has no such property (unevaluatedProperties false), so the size
  is in COVERAGE.md and BUILD-LOG.md only.
- Proposed: an optional raw.size (integer, bytes).

## 7. Vocabulary (tools/read_rules.py VOCAB) the dump uses and the rules do not have
These give no fact today. Adding a value is a question for the readers and the builder, not for the adapter:
- tipo_procedimento: 683 urgent tenders ("Anúncio de concurso urgente", modeloAnuncio "Concurso público"), 25 "Concurso
  público simplificado", 21 "Concurso de concepção", 14 "Instituição de sistema de aquisição dinâmico", 14 "Instituição
  de sistema de qualificação", 2 "Concurso de ideias".
- tipo_contrato: 429 "Locação de bens móveis" (the rules' bens-servicos thresholds name locação, but VOCAB has only
  "bens"), 24 "Outros", 324 procedures with several contract types.

## 8. link.method has no value for a link made by code from a normalised name
- The brief asks for a candidate by country and normalised name when there is no NIF. Methods are nif_exact, name_ai
  (a model, with an event) and person. In this dump the 2 procedures without NIF have no name either, so no candidate
  was needed. E2 (adjudicatários) will need one.
- Proposed: a method "name_normalised" for a ferramenta (deterministic, like nif_exact).
