# Procedure documents probe (person's decision of 2026-10-25, BUILD-LOG M.0)

- 10 procedures published in October 2026 (the first five by key on acinGov and on Vortal), one GET of each
  PecasProcedimento link every 10 s, 22:33:18Z–22:34:48Z; no refusal. Log: adapters/pecas/probe-log.jsonl.
- acinGov (9 781 procedures of 2026 link there): 5/5 answered 200 with the whole set of pieces as one ZIP
  (`pecas_procedimento_*.zip`, 368 157 to 19 158 203 bytes), 3 to 5 files each, PDFs (one held a 7z, two a nested
  zip). Stored as `raw:pecas:documento:<key>` (bytes in data/raw/pecas/raw_bytes/, not in git).
- Vortal (10 506 procedures): 5/5 answered 200 with the same 686-byte HTML shell titled «Vision» (a JavaScript
  application); the documents are not reachable with a plain GET. Reading them would need a rendering browser, which
  is outside passive reading as done so far: a decision for the person.
- No facts: the architecture fetches documents in bulk only when a rule asks for them (conteudo_obrigatorio).
  These are the PT documents without fixed labels where AMALIA as extractora would matter.
