# ccp-engine

The Portuguese Código dos Contratos Públicos (CCP) decomposed into typed rules with validity dates and
code-verified literal citations, applied to facts of real procedures, producing a deterministic verdict that says
`nao_avaliado` whenever it cannot say `cumpre` or `nao_cumpre`. Same method as rjue-engine (urbanismo): patterns
copied and versioned here, never imported.

Existing systems model notices, forms and documents. This one models **legal obligations with source and date**:
which norm, which literal text, in force when, applied to which facts of which procedure, with which result and why.

## Invariants (verify.py checks them; publishing fails if one fails)

1. **Immutable sources.** Every source byte is stored with sha256 and capture date; a text whose hash changed is not loaded.
2. **Exact citation.** Every rule, verdict, deadline and event that invokes the law carries a passage id, the literal quote
   and offsets; verify checks them against the captured text.
3. **Verification in code, no model.** `verify.py` calls no model; it re-derives texts, packages, verdicts and published
   figures; CI runs it.
4. **AI proposes, never approves, never writes the citation.** It picks passages by id and proposes decompositions; code
   verifies; approval requires a person with a reason; proposer, reviewer and adjudicator are distinct principals.
5. **Two readers of different families.** A reading is `settled` when a blind reader of another model family replicates
   it; AMALIA alone never closes anything.
6. **`nao_avaliado` before a false `cumpre`.** Missing fact, missing rule, insufficient source coverage, document without
   text layer, or conflict: the verdict is `nao_avaliado` with a typed reason.
7. **Assertions are not facts.** What an entity declared (`regime`, `fundamentação`) is stored as an assertion and
   compared with the verdict; it never enters the engine as a fact.
8. **Bitemporal.** Facts and verdicts answer to `known_at` (what we knew) and `valid_at` (what was valid) separately;
   the law answers to its validity per passage.
9. **Nothing is merged, nothing is overwritten.** Entities are linked with provenance (a wrong link becomes `stale`, it
   is not deleted); the governance log is append-only.
10. **Public data, passive reading.** One read per page on portals that block; public APIs within their limits; nothing
    is ever sent to any system.
11. **Natural persons.** Entities whose NIF is a natural person's are evaluated but never published by name.
12. **The founder decides product rules, not legal content.** Readings of the law belong to the readers, with
    code-verified citations; product decisions (completeness threshold, what is published) enter the log as such.

## Ownership boundary

| Owner | Owns | Does not touch |
|---|---|---|
| Builder | `schemas/`, `engine/`, `verify.py`, `governance/`, `law/`, `rules/`, `tools/`, `tests/`, CI | `adapters/`, `data/` |
| Extractor | `adapters/<source>/` (adapter code + mapping declared as data), `data/raw/<source>/` (raw records with hash), `data/facts/` (facts, assertions, candidate entities in the schema format) | `schemas/`, `engine/`, `verify.py` |

The contract between the two is `schemas/` plus `fixtures/valid/` (one valid example per object), checked by
`verify.py`. A schema change is proposed by whoever needs it and applied by the builder; the extractor adapts the
source to the schema, never the schema to the source.

## Layout

```
schemas/      one JSON schema per object of the model; DECISIONS.md; TRACEABILITY.md
engine/       store (append-only, bitemporal), rules as data, evaluate, entities, manifest, governance
verify.py     the gate: fixtures/ and data/ against the schemas, every checkable invariant, broken fixtures must fail
governance/   principals.json and the append-only, hash-chained events.jsonl
law/          norm registry, passages, validity notes (filled by the CCP capture)
rules/        rule packages, the replay of the governance log (never edited by hand)
fixtures/     valid/ (one per object) and broken/ (one overlay per invariant, each with the check it must trip)
tests/        unit tests of the scaffold; tests/fill/ the red tests of FILL-PLAN.md
tools/        capture, serve, package (copied from rjue with their own version)
adapters/     extractor's
data/         extractor's
```

Run:

```
.venv/bin/python -I verify.py
.venv/bin/python -m pytest tests --ignore=tests/fill
```
