# Extraction test v1 for TED and BASE contratos: pass/fail criteria (written before any sample is drawn)

Same question and method as the DR notices' test (foaap-core/ccp-mother-data/e1b-sample-2026-10-25/CRITERIA-v2.md): can
the fields be read correctly, by code, from each new source? Asked by the person (relayed by the builder, 2026-10-26):
«8 = each new source measured, not assumed», 200 per source. Written 2026-10-26 before either sample was drawn; its
sha256 goes into BUILD-LOG.md in the commit that adds it. Not edited after results exist; a change makes a v2 with a new
sample.

## Frozen code (sha256)
- TED parser: adapters/ted/parse.py, cf1ee6bdf9811b1a73d37eb885f1e9ee0f73203a03c83286c3516bc51f982dca. Written on the
  development months 2018-01 and 2026-01 only.
- BASE contratos parser: adapters/base-contratos/adapter.py, 0f4a52c364e30d7368446bc4408781d9c55be9949bd2e03d23fc5e093d3e7eec
  (contract_values) with adapters/base-contratos/mapping.json, 65b9c384a5a05bad70e70cc6eda683948cca334f331adfb664eeeed90dbbd79b.
  Written on the contracts BASE published in October 2026 only.
- The sampling and scoring scripts are committed, with their sha256 in BUILD-LOG.md, before the sample is drawn.

## Populations and samples
- TED: the Portuguese notices kept by adapters/ted/modal_ted.py (manifest.json), whose buyer's country (by the parser)
  is PT / PRT, in every month except the development months 2018-01 and 2026-01. Sample: 100 TED-XML notices and 100
  eForms notices, each drawn uniformly at random with random.Random(20261027) from that format's population, sorted by
  member name before drawing.
- BASE contratos: the records of contratos2026.zip (raw sha256 2ac78c54690f2e64…), excluding the contracts BASE published
  in October 2026 (development) and every idcontrato held by more than one record of the year. Sample: 200 records,
  random.Random(20261027), sorted by idcontrato before drawing.

## Checks and pass lines
- A. Coverage, per field, share of the sample with a value. Reported for every field. PASS lines only where the source
  always has the field: TED dispatch_date, notice_type, notice_id, buyer_name, main_cpv, and deadline_date for contract
  notices (TED-XML code 3, eForms subtypes 16–18); BASE contratos preco_contratual, data_publicacao_contrato,
  adjudicante. PASS if >= 95 % for each of those.
- B. Against another source, where the same procedure can be found:
  - BASE contratos: a sampled contract whose (nAnuncio, idINCM) is the key of a procedure of adaptador:base-anuncios is
    compared with that notice's facts: preco_base, tipo_procedimento, adjudicante, tipo_contrato.
  - TED contract notices: a BASE anúncio of the same year with the same deadline date and the same buyer (NIF for eForms;
    the name, accents and case folded, for TED-XML, which rarely carries a NIF) is the same procedure; compared: the
    estimated value with PrecoBase (equal to the cent) and the procedure type (open with Concurso público, restricted
    with Concurso limitado por prévia qualificação, negotiated with Procedimento de negociação).
  - Reported: the join rate, and the agreement among joined pairs. PASS if >= 95 % agree, and every disagreement is
    listed with both values and classified (parser error / the sources differ, with the text quoted).
- C. Blind second reading by the family-B reader (reader B's bundled client, reader-b exec, read-only sandbox, the model
  the person named for the DR test, model-b, unless he names another before the reading; its version written in
  BUILD-LOG.md). The reader gets only the source text of each sampled record (the TED XML; the BASE JSON record), never
  the parser's output, and answers the same fields; its answers are saved with their sha256 before scoring. PASS if code
  and reader agree on >= 98 % of the values both give (dates as dates, amounts to the cent, NIFs as nine digits, names
  accents and case folded), and every disagreement is settled by quoting the source and classified (code error / reader
  error / text ambiguous). If the client cannot run, C is NOT RUN and the source's test cannot pass.
- Intervals: Wilson 95 % for every share.

## Verdict, applied as written
- A, B and C pass for a source: that source's extraction is measured; it counts towards the 8.
- A fails for a field: that field is partial and reported with its number.
- B or C fails: the parser is wrong for that source; fix it and draw a new sample (v2) before claiming a pass.

## Not settled by this test
Whether TED's dispatch date is the «envio» arts. 135.º/136.º count from (a reading of the law, for the two readers).
