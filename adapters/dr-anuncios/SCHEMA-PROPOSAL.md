# Proposals and open questions from the DR notice adapter (E1b, 2026-10-25)

The extractor does not change schemas/, engine/, verify.py or tools/, and decides no reading of the law. Below: what is
for the person (product), for the readers (law), and for the builder (schemas, gate). Counts: COVERAGE.md.

## For the person (pessoa:paulo)
1. **PDF bytes and git.** Paulo's «yes» covered the 23 MB anúncios dump only, so the notice PDFs (about 1.5 GB) are kept
   out of git (data/raw/dr-anuncios/raw_bytes/, gitignored). Every PDF has a `raw` and a `documento` object with its
   sha256 and URL in git. Consequence: in CI, verify cannot re-hash them and reports I01 «bytes not in the store» for
   each PDF raw. Options: keep them out and let the data store's I01 skip bytes declared external (a builder change);
   keep them in a separate storage the CI reads; or commit them. The question is what the repository holds.
2. **Conflicts on the proposal deadline.** Where the notice prints «D+1 00:59» and the dump says «D», both facts are kept
   and a `conflito` with resolution nao_avaliado is written; neither value is chosen. A precedence rule (e.g. the notice
   as printed wins) would be a product rule recorded in the log; until then the rules that need the field say conflito.

## For the readers (law, with citations)
3. **territorio.** The fact is the adjudicante's NUT III (section 1, first occurrence) mapped PT2 -> PT-AC, PT3 -> PT-MA,
   other -> PT. Whether the rules' territorio means the adjudicante's seat (and not, say, the place of execution) is a
   reading question.
4. **tipo_entidade.** The notice's «Norma jurídica da Entidade Adjudicante» text is stored as norma_juridica_adjudicante,
   as printed. Mapping its values to estado / outra is a reading of the law.
5. **data_inicio_procedimento.** Not derived. Whether the sending date bounds the start of the procedure is a reading.
6. **prazo_propostas_dias.** data_envio_anuncio and data_limite_propostas are both facts now. The days between them is
   the transform days_between; which sending arts. 135.º/136.º count from, whether the first day counts, and what the
   printed time of day (00:59) means are readings. Until that is decided no prazo_propostas_dias fact is written.

## For the builder
7. **Quotes in documents cannot be re-derived by verify.** A fact's origin is (documento, page, offsets, quote), with
   offsets into that page's text as pypdf 6.14.2 extracts it. engine/extract.py has no PDF extractor, so verify checks
   the documento exists but not that the quote is at those offsets. Proposed: a versioned extractor (e.g.
   "pdf-pypdf-pages@1") whose text the raw names in raw.text, so verify can re-run it as it does for the DR pages.
8. **Two adapters for one canonical field.** data_limite_propostas now has a fact from each of base-anuncios and
   dr-anuncios; engine.evaluate.read_facts takes the latest known when no conflito names the field. That is right when
   they agree (the conflito covers the disagreements), but it is worth a line in schemas/DECISIONS.md.
