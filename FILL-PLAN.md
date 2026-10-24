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

What the DR serves (captured 2026-10-24, in `law/raw/`; DECISIONS D24):
- `raw:dr-consolidado:lei:ccp`: the consolidated page, one rendered DOM (2.6 MB). Working text `dr-consolidated-fragments@1`
  (591 "Artigo" lines, 4376 lines) and, with `dr-article-history@1`, the same plus 735 notes (`NOTA: ...`), each article's
  current text followed by its notes newest first. `engine/vigente.parse_note` reads every one of the 735 (53 are
  `REVOGADO`, 4 have no "em vigor a partir de").
- `raw:dr-consolidado:artigo-historico:ccp-art20 / -art113 / -art136`: the opened "Ver alterações ao texto" view, one per
  article, captured by `tools/capture_dr_history.mjs` (DevTools protocol: load the consolidated page, click the article's
  link, dump the live DOM; a plain `--dump-dom` of the article URL does not bring the history). Working text
  `dr-article-history@1`: per version, title + epigraph + text, then the note that produced it; oldest = "Versão inicial"
  with no note. `engine/vigente.versions_from_history` turns it into legal versions (rectifications with the same
  `valid_from` folded into one version; `tests/test_vigente.py` fixes art. 20 = 4 versions, art. 136 = 3).
- `raw:dr-consolidado:diploma:dl-177-2026`: the amending act's detail page (`dr-html-blocks@1`). Its own **Artigo 7.º,
  Norma transitória, n.º 2** is the regime selector's passage (`dl-177-2026:art7.2`); the page also carries the
  republished CCP after the line "Republicação", so `structure` must stop the act's own articles there.
  Official PDF: https://files.diariodarepublica.pt/1s/2026/09/17200/0000200283.pdf (sha256 e2c9ae64fe97e336…, 27.8 MB,
  not stored in git; capture into `law/raw_bytes/` when the edition check is built).

Steps:
1. `engine/structure.structure(norma, text, raw_id, version)`: the consolidated working text -> passages `ccp:artN`,
   `ccp:artN.M`, `ccp:artN.M.a` (numbers "1 - ", alíneas "a) ", subalíneas "i) ") with offsets into that text; parts,
   titles, chapters from the "Anexo > Parte II > Título I > Capítulo II" path lines.
2. `tools/capture_dr_history.mjs` over every article that has at least one note (count them from the consolidated text;
   expect about 384), 3 s apart, one click each, stored through `engine.sources.record_raw` as `artigo-historico` raws.
3. `engine/vigente.notes_to_vigencias`: one `vigencia` per note of the consolidated text, `passage` = the article (or the
   number/alínea the note's text names), `altered_by` = `norma:` + `norma_slug(diploma)`, `effect` from the note, `note`
   quoted by offsets in the consolidated working text; register every amending act as a `norma` (title from the note).
4. Passage versions from the history raws (`versions_from_history`, `initial_valid_from` = 2008-07-30); articles without
   history have one version; `vigente(store, date)` = the version with `valid_from <= date < valid_to`.

Done when: ≥ 589 `artigo` passages; ≥ 607 vigencias, every quote re-derived by verify; `vigente(2026-09-30)` and
`vigente(2026-10-01)` differ exactly in the passages whose vigencia names `norma:dl-177-2026` with `valid_from`
2026-10-01 (211 notes carry that date); `python -I verify.py` 0 failures; the capture log (dates, sha256 per page) in
BUILD-LOG.md.

## B3 — rules v0 in the governance log, two families (`tests/fill/test_b3_rules_v0.py`)

Readers: AMALIA on Modal (CONTEXTO.md; scripts in `~/Downloads/foaap-core/amalia-benchmark-2026-10-23/`) proposes by
choosing passage ids; Reader B reviews blind. Both go through `engine.governance.Log` (`propose` by `ai:amalia-9b`, `review`
by `ai:reader-b` with `independence: blind`). The code writes every quote with `engine.passages.cite`. Rules:
`seletor_regime` on `dl-177-2026:art7.2` (Norma transitória, n.º 2); `limiar` on `ccp:art19*` and `ccp:art20*`; `prazo_minimo` on `ccp:art135*` and
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
