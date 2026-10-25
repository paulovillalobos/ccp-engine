# TED probe (person's decision of 2026-10-25, BUILD-LOG M.0)

- Source: TED daily packages, `https://ted.europa.eu/packages/daily/{yyyy}{issue, 5 digits}` (listing:
  https://ted.europa.eu/en/simap/xml-bulk-download; S 190/2026 is 01/10/2026). Three GETs: two to wrong addresses
  (`/packages/daily/202620000`, 400; `/packages/notice/daily/202620000`, 404: the issue was not zero-padded), then
  `/packages/daily/202600190` at 2026-10-25T22:31:50Z, 200, 18 115 918 bytes (tar.gz, 190 MB unpacked), sha256
  70f29e9ae08c40978084af7948cefc15a2171c9b274b4b940cadf6ed8d1948d0, raw `raw:ted:pacote-diario:202600190`
  (bytes in data/raw/ted/raw_bytes/, not in git).
- Counted by `adapters/ted/count.py` (no facts): 3 631 notices that day in the EU; 77 with an organisation in Portugal
  (country PRT), 74 with a nine-digit NIF; eForms subtypes 16 (contract notice) 50, 29 (award notice) 21, 38 2, 15 2,
  E4 1, 17 1.
- Use: the contract notices (16) are the DR notices whose publicado_joue is Sim, so TED can confirm the flag, the
  dispatch date and the deadline by NIF and date (the E1b test's check D did this with TED's API on 200 notices). Not
  joined tonight.
