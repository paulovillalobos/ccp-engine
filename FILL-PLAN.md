# FILL-PLAN — phase B, against the red tests in tests/fill/

Rules for whoever fills (the builder, same session): do not change `schemas/` or the signatures and docstrings of `engine/`;
if there is no other way, add a row to `schemas/DECISIONS.md` and an entry to `BUILD-LOG.md` first. One commit per task,
`BUILD-LOG.md` after each. Each task is done when its test in `tests/fill/` is green and `python -I verify.py` stays green.
Never write in `adapters/` or `data/` (extractor's). Never download a dataset of facts. No model participates in verify.

Run the red tests: `.venv/bin/python -m pytest tests/fill -q`

## B1 — copy the rjue modules with their own version (`tests/fill/test_b1_copied_modules.py`)

Copy from `~/Downloads/rjue-engine`, adapt, and version as `ccp-<module>-0.1`; no `rjue` left in names or docstrings
(a "copied from rjue-engine" note is fine). Interfaces the test requires (callable, documented in the module docstring):

| Module | From rjue | Interface |
|---|---|---|
| `engine/sources.py` | `engine/sources.py` | `record_raw(root, source, kind, source_id, url, data: bytes, media_type, encoding, captured_at) -> raw dict` — writes `raw_bytes/<sha256>` and the `raw` object through `engine.store.Writer`; `request.method` is always `GET`, `reads_of_page` 1. `load_raw_text(store, raw_id) -> str` |
| `engine/structure.py` | `engine/structure.py` | `structure(norma: dict, raw_text: str, raw_id: str, version: str) -> list[passagem]` — the consolidated DR text to passages with `offsets` in the raw text, one per structural node (parte, titulo, capitulo, secao, artigo, numero, alinea), ids `ccp:art20.1.a` |
| `engine/passages.py` | `engine/passages.py` | `passage_text(store, passage_id, version) -> str`; `cite(store, passage_id, version, start, end) -> citation` — the code writes the quote as `text[start:end]`; a model only ever supplies `passage_id` |
| `engine/vigente.py` | `engine/vigente.py` | `notes_to_vigencias(raw_text, raw_id, passages, normas) -> list[vigencia]` — the 607 DR notes to `vigencia` objects, each quoting its note by offsets; `vigente(store, date) -> dict[passage_id, version]` — the version of every passage in force at `date` (law clock, invariant 8) |
| `tools/capture_dr_consolidated.py` | same | one passive GET per page of the consolidated act; writes through `record_raw`; never POST |
| `tools/serve.py` | same | the read-only API skeleton of §9 (routes may return 501 until B4); JSON only, bounded body and time, never a trace or a client path |
| `tools/package.sh` | same | builds the deployable package; no secrets inside |

Done when: `test_b1_copied_modules.py` green; `verify.check_code()` empty (tools may import `urllib.request`; engine may not).

## B2 — capture the consolidated CCP with its validity notes (`tests/fill/test_b2_ccp_capture.py`)

Source: CCP consolidated at diariodarepublica.pt (589 articles, 607 notes with dates) plus the DL 177/2026 text for
`dl-177-2026:art7`. Output into the repository's store: `law/raw/`, `law/raw_bytes/`, `law/norma/`, `law/passagem/`,
`law/vigencia/`, all through `engine.store.Writer` (append-only). `norma:ccp` and `norma:dl-177-2026` registered; each
passage version's `offsets` select its text inside the raw capture (verify I01); each `vigencia` quotes its note (I02).

Done when: at least 589 `artigo` passages under `norma:ccp`; at least 607 `vigencia` records; `vigente(store, "2026-09-30")`
and `vigente(store, "2026-10-01")` differ exactly in the passages whose `vigencia` names `norma:dl-177-2026` with
`valid_from 2026-10-01`; `python -I verify.py` re-derives everything with 0 failures. Record the capture in `BUILD-LOG.md`
with the sha256 of each raw page.

## B3 — rules v0 in the governance log, two families (`tests/fill/test_b3_rules_v0.py`)

Readers: AMALIA on Modal (CONTEXTO.md; scripts in `~/Downloads/foaap-core/amalia-benchmark-2026-10-23/`) proposes by
choosing passage ids; Reader B reviews blind. Both go through `engine.governance.Log` (`propose` by `ai:amalia-9b`, `review`
by `ai:reader-b` with `independence: blind`). The code writes every quote with `engine.passages.cite`. Rules:
`seletor_regime` on `dl-177-2026:art7*`; `limiar` on `ccp:art19*` and `ccp:art20*`; `prazo_minimo` on `ccp:art135*` and
`ccp:art136*`. `rules/regra/` is the replay of the log (`regra.readings`, `regra.state`), `rules/pacote/pacote:ccp@2026-10-01`
names them (`engine.rules.package`).

Done when: every rule has a citation verified by offsets, two readings of distinct families and a state; verify I02/I05/
PACK green; the AMALIA and Reader B answers are stored under `governance/readings/` so the measurement of §8 can replay them.

## B4 — engine v0 over the extractor's notices (`tests/fill/test_b4_engine_v0.py`)

Waits for `data/facts/` from the extractor (at least 1000 `proc` units with facts). `tools/run_engine.py --out PATH`
loads `data/`, `law/`, `rules/`, `governance/`, builds the manifest (`engine.manifest.build`: law version, package,
adapters, source snapshots, code commit, log head), runs `engine.evaluate.evaluate` for the `prazo_minimo` rules over
every `proc` with `engine.store.facts_of`, and writes `reports/prazos-minimos.json`: per rule the counts of `cumpre`,
`nao_cumpre` and `nao_avaliado` by reason, plus the manifest. Deterministic: same inputs, same bytes.

Done when: the report exists, recomputes byte for byte, counts at least 1000 units, and every verdict behind it passes
verify (complete manifest, no natural person named). The figure is internal until the measurement of §8 exists.

## After B4 (not in this plan; propose, do not start)
Diff by rule between packages served by the API; review queue; disputes; TED; Vortal; acinGov; documents with position.
