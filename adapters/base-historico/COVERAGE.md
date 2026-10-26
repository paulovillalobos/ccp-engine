# BASE bulk dumps 2018–2026 (dados.gov.pt, IMPIC)

One GET per file (2026-10-26, 18:33–18:35Z), each file's sha1 equal to the checksum dados.gov.pt publishes for it.
Bytes in data/raw/base-historico/raw_bytes/ (gitignored; to be moved to Supabase Storage, project ccp-engine, when its
bucket exists); raws in data/raw/base-historico/raw/base-historico.jsonl. The 2026 files are the ones already stored by
E1 (anuncios2026.json, data/raw_bytes/9605b59b…) and the samples branch (contratos2026.zip, 2ac78c54…): same resources,
not read again.

| year | anúncios (records) | anúncios file (bytes) | contratos (records) | contratos zip (bytes) |
|---|---:|---:|---:|---:|
| 2018 | 13 787 | 10 312 607 | 127 936 | 23 234 265 |
| 2019 | 17 327 | 12 872 270 | 145 517 | 26 718 958 |
| 2020 | 19 071 | 15 413 292 | 176 534 | 31 849 822 |
| 2021 | 19 648 | 16 402 261 | 187 442 | 35 549 810 |
| 2022 | 21 153 | 17 951 507 | 176 605 | 34 752 748 |
| 2023 | 30 249 | 25 299 930 | 194 023 | 38 957 437 |
| 2024 | 27 772 | 24 233 389 | 227 509 | 44 611 566 |
| 2025 | 33 521 | 30 917 984 | 248 081 | 55 383 072 |
| 2026 | 25 609 | 23 669 469 | 199 701 | 46 720 122 |
| total | 208 137 | | 1 683 348 | |

Not mapped to facts yet: the adapters of E1 (anúncios) and of the October sample (contratos) apply to these years; the
Postgres load belongs to the D48 session.
