# Coverage matrix: source × year × field

Share of records for which the adapter's own code gives a value (adapters/coverage/matrix.py; counts in
matrix.json, with the most frequent reasons for no value). BASE anúncios: procedure notices only (tipoActo
«Anúncio de procedimento»). TED: notices with a Portuguese buyer; deadline_date over contract notices only.
A share is coverage, not correctness: correctness is measured in adapters/medicao/ (TED, BASE contratos) and
in the DR notices' test.

## base-anuncios

| year | records | tipo_procedimento | tipo_contrato | preco_base | adjudicante | data_publicacao_anuncio | data_limite_propostas |
|---|---:|---:|---:|---:|---:|---:|---:|
| 2018 | 11 236 | 99.2 | 96.4 | 95.9 | 99.8 | 100.0 | 97.6 |
| 2019 | 14 361 | 98.8 | 95.8 | 97.3 | 99.8 | 100.0 | 98.9 |
| 2020 | 15 356 | 99.1 | 96.0 | 98.1 | 99.9 | 100.0 | 99.4 |
| 2021 | 16 330 | 99.0 | 95.7 | 98.0 | 99.9 | 100.0 | 99.5 |
| 2022 | 17 327 | 98.9 | 95.3 | 97.5 | 99.8 | 100.0 | 99.4 |
| 2023 | 25 323 | 99.0 | 92.2 | 97.2 | 96.6 | 100.0 | 99.5 |
| 2024 | 25 064 | 99.3 | 96.0 | 98.6 | 99.4 | 100.0 | 99.0 |
| 2025 | 28 472 | 99.2 | 96.5 | 99.0 | 99.9 | 100.0 | 98.2 |
| 2026 | 21 575 | 99.6 | 96.5 | 99.3 | 100.0 | 100.0 | 98.8 |

## base-contratos

| year | records | tipo_procedimento | preco_base | adjudicante | tipo_contrato | preco_contratual | data_celebracao_contrato | data_publicacao_contrato | adjudicatario |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 2018 | 127 936 | 88.0 | 96.0 | 99.9 | 97.7 | 99.7 | 100.0 | 100.0 | 88.0 |
| 2019 | 145 517 | 87.3 | 96.1 | 100.0 | 97.6 | 99.7 | 100.0 | 100.0 | 89.0 |
| 2020 | 176 534 | 74.3 | 81.3 | 100.0 | 98.1 | 99.7 | 84.9 | 100.0 | 90.4 |
| 2021 | 187 442 | 82.9 | 92.0 | 100.0 | 98.0 | 99.8 | 94.7 | 100.0 | 90.5 |
| 2022 | 176 605 | 84.8 | 95.6 | 100.0 | 97.9 | 99.7 | 98.6 | 100.0 | 89.4 |
| 2023 | 194 023 | 83.4 | 97.5 | 100.0 | 97.9 | 99.7 | 99.6 | 100.0 | 89.9 |
| 2024 | 227 509 | 82.1 | 97.9 | 99.8 | 98.1 | 99.8 | 99.9 | 100.0 | 90.2 |
| 2025 | 248 081 | 77.6 | 97.9 | 100.0 | 97.9 | 99.8 | 99.5 | 100.0 | 89.3 |
| 2026 | 199 701 | 74.0 | 98.4 | 100.0 | 98.3 | 99.8 | 99.7 | 100.0 | 88.2 |

Gaps (under 90 %):

- 2018 tipo_procedimento: 88.0 % — 'Ao abrigo de acordo-quadro (art.º 259.º)' outside the vocabulary (13 438); 'Ao abrigo de acordo-quadro (art.º 258.º)' outside the vocabulary (1 851); 'Ajuste direto simplificado' outside the vocabulary (14)
- 2018 adjudicatario: 88.0 % — an adjudicatário without NIF ('-') (15 158); empty list (133)
- 2019 tipo_procedimento: 87.3 % — 'Ao abrigo de acordo-quadro (art.º 259.º)' outside the vocabulary (15 947); 'Ao abrigo de acordo-quadro (art.º 258.º)' outside the vocabulary (2 545); 'Ajuste direto simplificado' outside the vocabulary (29); 'Contratação excluída II' outside the vocabulary (4)
- 2019 adjudicatario: 89.0 % — an adjudicatário without NIF ('-') (15 845); empty list (227)
- 2020 tipo_procedimento: 74.3 % — 'Ajuste direto simplificado' outside the vocabulary (26 262); 'Ao abrigo de acordo-quadro (art.º 259.º)' outside the vocabulary (15 154); 'Ao abrigo de acordo-quadro (art.º 258.º)' outside the vocabulary (3 514); 'Ajuste direto simplificado ao abrigo da Lei n.º 30/2021, de 21.05' outside the vocabulary (461)
- 2020 preco_base: 81.3 % — 0 or absent (32 935)
- 2020 data_celebracao_contrato: 84.9 % — not a date (26 723)
- 2021 tipo_procedimento: 82.9 % — 'Ao abrigo de acordo-quadro (art.º 259.º)' outside the vocabulary (17 164); 'Ajuste direto simplificado' outside the vocabulary (9 656); 'Ao abrigo de acordo-quadro (art.º 258.º)' outside the vocabulary (4 843); 'Ajuste direto simplificado ao abrigo da Lei n.º 30/2021, de 21.05' outside the vocabulary (281)
- 2022 tipo_procedimento: 84.8 % — 'Ao abrigo de acordo-quadro (art.º 259.º)' outside the vocabulary (18 977); 'Ao abrigo de acordo-quadro (art.º 258.º)' outside the vocabulary (4 720); 'Ajuste direto simplificado' outside the vocabulary (2 217); 'Contratação excluída II' outside the vocabulary (385)
- 2022 adjudicatario: 89.4 % — an adjudicatário without NIF ('-') (18 298); empty list (416)
- 2023 tipo_procedimento: 83.4 % — 'Ao abrigo de acordo-quadro (art.º 259.º)' outside the vocabulary (23 305); 'Ao abrigo de acordo-quadro (art.º 258.º)' outside the vocabulary (5 691); 'Contratação excluída II' outside the vocabulary (1 622); 'Ajuste direto simplificado' outside the vocabulary (489)
- 2023 adjudicatario: 89.9 % — an adjudicatário without NIF ('-') (19 154); empty list (487)
- 2024 tipo_procedimento: 82.1 % — 'Ao abrigo de acordo-quadro (art.º 259.º)' outside the vocabulary (27 156); 'Contratação excluída II' outside the vocabulary (6 267); 'Ao abrigo de acordo-quadro (art.º 258.º)' outside the vocabulary (5 595); 'Setores especiais – isenção parte II' outside the vocabulary (1 003)
- 2025 tipo_procedimento: 77.6 % — 'Ao abrigo de acordo-quadro (art.º 259.º)' outside the vocabulary (31 158); 'Contratação excluída II' outside the vocabulary (14 817); 'Ao abrigo de acordo-quadro (art.º 258.º)' outside the vocabulary (6 404); 'Setores especiais – isenção parte II' outside the vocabulary (1 412)
- 2025 adjudicatario: 89.3 % — an adjudicatário without NIF ('-') (26 516); empty list (70)
- 2026 tipo_procedimento: 74.0 % — 'Ao abrigo de acordo-quadro (art.º 259.º)' outside the vocabulary (29 330); 'Contratação excluída II' outside the vocabulary (15 204); 'Ao abrigo de acordo-quadro (art.º 258.º)' outside the vocabulary (4 971); 'Setores especiais – isenção parte II' outside the vocabulary (1 069)
- 2026 adjudicatario: 88.2 % — an adjudicatário without NIF ('-') (23 495); empty list (17)

## ted

| year | records | dispatch_date | notice_id | buyer_name | buyer_nif | buyer_nuts | procedure_type | contract_type | deadline_date | estimated_value | main_cpv |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 2018 | 7 607 | 100.0 | 100.0 | 99.2 | 11.4 | 68.9 | 100.0 | 69.4 | 99.6 | 37.5 | 100.0 |
| 2019 | 8 396 | 100.0 | 100.0 | 99.9 | 64.9 | 99.7 | 100.0 | 99.4 | 100.0 | 60.2 | 100.0 |
| 2020 | 7 860 | 100.0 | 100.0 | 100.0 | 80.5 | 99.6 | 100.0 | 99.1 | 100.0 | 50.5 | 100.0 |
| 2021 | 8 645 | 100.0 | 100.0 | 100.0 | 85.7 | 99.6 | 100.0 | 99.2 | 100.0 | 56.9 | 100.0 |
| 2022 | 9 036 | 100.0 | 100.0 | 100.0 | 86.4 | 99.9 | 100.0 | 99.3 | 100.0 | 58.2 | 100.0 |
| 2023 | 11 817 | 100.0 | 100.0 | 100.0 | 84.9 | 99.9 | 100.0 | 99.5 | 100.0 | 56.3 | 100.0 |
| 2024 | 13 385 | 100.0 | 100.0 | 100.0 | 98.3 | 98.7 | 93.8 | 99.3 | 97.8 | 69.0 | 100.0 |
| 2025 | 17 340 | 100.0 | 100.0 | 100.0 | 100.0 | 99.6 | 90.4 | 97.9 | 99.1 | 70.9 | 100.0 |
| 2026 | 14 315 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 86.1 | 97.9 | 99.1 | 70.2 | 100.0 |

Gaps (under 90 %):

- 2018 buyer_nif: 11.4 % — not in the notice (6 736)
- 2018 buyer_nuts: 68.9 % — not in the notice (2 364)
- 2018 contract_type: 69.4 % — not in the notice (2 327)
- 2018 estimated_value: 37.5 % — not in the notice (4 752)
- 2019 buyer_nif: 64.9 % — not in the notice (2 949)
- 2019 estimated_value: 60.2 % — not in the notice (3 340)
- 2020 buyer_nif: 80.5 % — not in the notice (1 535)
- 2020 estimated_value: 50.5 % — not in the notice (3 888)
- 2021 buyer_nif: 85.7 % — not in the notice (1 232)
- 2021 estimated_value: 56.9 % — not in the notice (3 730)
- 2022 buyer_nif: 86.4 % — not in the notice (1 232)
- 2022 estimated_value: 58.2 % — not in the notice (3 780)
- 2023 buyer_nif: 84.9 % — not in the notice (1 779)
- 2023 estimated_value: 56.3 % — not in the notice (5 159)
- 2024 estimated_value: 69.0 % — not in the notice (4 149)
- 2025 estimated_value: 70.9 % — not in the notice (5 049)
- 2026 procedure_type: 86.1 % — not in the notice (1 986)
- 2026 estimated_value: 70.2 % — not in the notice (4 265)

## Not in the tables above (gaps by source)

- DR notice PDFs 2026: 9 011 procedures' notices downloaded of the 22 170 with a DR PDF (adapters/dr-anuncios/fetch-log.jsonl,
  one GET every 10 s, still running); fields per notice in adapters/dr-anuncios/COVERAGE.md, which counts only the notices
  already read into documents. DR 2018–2025: not fetched (next: concursos públicos, newest first).
- Vortal (a second copy of DR notices, where the pieces are on Vortal): 219 copies, byte-identical to the DR; stopped by a
  403 on 2026-10-26 20:18:27Z. Platform pieces (acinGov, Vortal) are documents, not fields: none in these tables.
- TED forms by year: TED-XML to 2023, mixed in 2024 (eforms 11 952, ted-xml 1 433), eForms only from 2025; buyer_nif and
  procedure_type shift with the form, not with the year. TED keeps notices whose
  buyer is Portuguese by the parser (contract notices, results, changes, all kinds); BASE anúncios are procedure notices.
- BASE contratos tipo_procedimento: framework-agreement call-offs (arts. 258.º/259.º), «Contratação excluída II»,
  special-sector exemptions and «Ajuste direto simplificado» are outside the adapter's vocabulary (a mapping choice).
- BASE modificações and entidades: sampled only (2026), not in these tables.

