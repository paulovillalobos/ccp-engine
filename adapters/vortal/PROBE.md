# Vortal probe (person's decision of 2026-10-25, BUILD-LOG M.0)

- The BASE link `community.vortal.biz/Public/public-tender-documents/<encrypted id>` serves a JavaScript application
  («Vision»). Opened once in a browser (2026-10-25 ~22:42Z) only to see which addresses the application reads: all
  its own requests are GETs to a public JSON API; the page also sends analytics (Google Analytics, a help widget),
  which is why the data is read without the browser.
- Plain GETs, 10 s apart, User-Agent «ccp-engine research (passive read)», one procedure (BASE 24347/2026, Vortal
  PT1.NTC.3811157), 22:43:35Z–22:45:07Z, all 200:
  1. `public/api/PublicTenderDocuments/GetPublicTenderInformation?uniqueIdentifierEncrypted=<id>&languageCode=pt`:
     the BASE link -> the notice address (PT1.NTC.3811157); its documentList was empty.
  2. `public/api/ContractNoticeDetail/getHeaderInfo?contractNoticeUniqueIdentifier=PT1.NTC.3811157`: title, state
     (Awarded), dueDateForReceivingReplies 2026-10-07T22:59:00Z.
  3. `public/api/ContractNoticeDetail/GetRegionConfigurationByContractNoticeUId?contractNoticeUId=…&langCode=pt`:
     the whole notice as typed fields (managing authority with NIF, reference, procedure type, CPV, contract type,
     base price 125000, publication 2026-10-01T11:26:57Z, deadline 2026-10-07T22:59:00Z, review body…) and the
     documents list, each with a public download URL, type, size and upload time.
  4. `archive/api/PublicDownload/download?token=…`: one document, 419974431.pdf (71 547 bytes, PDF, 3 pages).
- Found: that document has the same sha256 (733a83cf…) as the DR notice 419974431 fetched by E1b from
  files.diariodarepublica.pt: the entity uploaded the DR notice itself, a byte-exact join between the Vortal
  procedure and its DR notice. The deadline is given in UTC (22:59Z = 23:59 in Lisbon, UTC+1 in early October): a
  possible reason for the «D+1 00:59» vs «D» differences the E1b test saw between the DR notice and the dump (a
  hypothesis, not checked).
- Privacy: the documents list names the official who uploaded each file (a natural person): kept in the raw bytes,
  never published.
- Raws: raw:vortal:tender-information / contract-notice-header / contract-notice (PT1.NTC.3811157) and
  raw:pecas:documento:vortal-PT1.NTC.3811157-419974431.pdf; bytes in data/raw/<source>/raw_bytes/, not in git. No facts.
- So Vortal's 10 506 procedures of 2026 are readable with three GETs each (plus one per document), no browser.
