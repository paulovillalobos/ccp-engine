# TED Portuguese notices 2018–2026 (monthly packages, filtered on Modal)

Generated from adapters/ted/manifest.json (one entry per month). Packages read once each on the person's Modal account
(2026-10-26), kept on the volume ccp-raw-bytes under ted/packages/<sha256> (raws: data/raw/ted/raw/ted-mensal.jsonl).
Portuguese notices kept unchanged in one tar.gz per month, plus a per-notice index (member, sha256, size, format, why);
both in Supabase Storage ccp-raw/ted/raw_bytes/<sha256>, named in the manifest. Portuguese: TED-XML with ISO_COUNTRY PT
in the coded data (the buyer's country); eForms with an organisation whose country is PRT (this also keeps foreign
buyers with a Portuguese party: a buyer-country filter is the next refinement).

| year | months | EU notices | Portuguese | TED-XML | eForms | packages (GB) |
|---|---:|---:|---:|---:|---:|---:|
| 2018 | 12 | 578 501 | 7 607 | 7 607 | 0 | 1.8 |
| 2019 | 12 | 622 786 | 8 396 | 8 396 | 0 | 1.9 |
| 2020 | 12 | 643 552 | 7 860 | 7 860 | 0 | 1.9 |
| 2021 | 12 | 676 733 | 8 645 | 8 645 | 0 | 2.0 |
| 2022 | 12 | 735 067 | 9 036 | 9 036 | 0 | 2.2 |
| 2023 | 12 | 795 680 | 11 822 | 11 813 | 9 | 2.7 |
| 2024 | 12 | 801 444 | 13 521 | 1 433 | 12 088 | 3.8 |
| 2025 | 12 | 871 149 | 17 594 | 0 | 17 594 | 4.2 |
| 2026 | 9 | 674 224 | 14 471 | 0 | 14 471 | 3.4 |
| total | 105 | 6 399 136 | 98 952 | 54 790 | 44 162 | 23.9 |

Not comparable across the switch: from 2024 most notices are eForms, whose filter is broader than TED-XML's, so part
of the rise from 2024 on is the filter, not the market.

October 2026 is not in a monthly package yet (TED publishes it after the month ends).
