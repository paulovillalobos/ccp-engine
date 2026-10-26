# TED extraction test v2: result (CRITERIA-ted-v2.md applied as written)

Sample: 100 TED-XML + 100 eForms notices with a Portuguese buyer, seed 20261028, v1's 200 left out (sample.json ca9824d2…,
parsed.json 2ae15b5c…, sealed in X.4). Blind answers: blind/batch-00..39.json (reader-b-cli, model-b),
saved before scoring. Scores: score.json (adapters/medicao/score.py e997664b…, with --anuncios: BASE anúncios 2018–2025
back from Storage, sha256 checked, and the 2026 dump in data/raw_bytes/9605b59b…).

**Verdict as written: A passes, C passes, B fails (93.0 %, line 95 %).** TED therefore does not count as measured under
v2. Every B disagreement is a wrong join (two different procedures), not a parser error; see below.

## A. Coverage (Wilson 95 %)
| field | share | interval | line |
|---|---|---|---|
| dispatch_date | 200/200 | 98.1–100 | PASS |
| notice_type | 200/200 | 98.1–100 | PASS |
| notice_id | 200/200 | 98.1–100 | PASS |
| buyer_name | 200/200 | 98.1–100 | PASS |
| main_cpv | 200/200 | 98.1–100 | PASS |
| deadline_date (contract notices) | 93/93 | 96.0–100 | PASS |
| buyer_country | 200/200 | 98.1–100 | — |
| buyer_nuts | 192/200 | 92.3–98.0 | — |
| procedure_type | 192/200 | 92.3–98.0 | — |
| contract_type | 192/200 | 92.3–98.0 | — |
| buyer_nif | 170/200 | 79.4–89.3 | — |
| estimated_value | 120/200 | 53.1–66.5 | — |
| deadline_time | 90/200 | 38.3–51.9 | — |

## C. Code against the blind reader
- All: 1 652 / 1 653 = 99.9 % (99.7–100). **PASS.** TED-XML 799/800 (99.3–100); eForms 853/853 (99.6–100).
- dispatch_date 200/200 (v1: 161/200). Every other field 98–100 %.
- The one disagreement, **code error**: n=85, an EU agency's notice (EMSA) published in 24 languages. The parser reads
  the first `OFFICIALNAME`, which is in the first form, `<F02_2014 CATEGORY="TRANSLATION" … LG="DA">`: «Det Europæiske
  Agentur for Søfartssikkerhed». The reader gave the name from `CATEGORY="ORIGINAL" … LG="EN"`: «European Maritime
  Safety Agency». Fix for later: read the form whose CATEGORY is ORIGINAL. Reader errors: 0.

## B. Against BASE anúncios (same deadline date and same buyer; a unique candidate)
- Contract notices with a deadline: 93; joined: 31 (33.3 %, 24.6–43.4). Agreement among joined pairs: 53 / 57 = 93.0 %
  (83.3–97.2). **FAIL.**
- The 4 disagreements, all **not the same procedure**: the buyer had another procedure with the same deadline in BASE,
  and the TED notice's own anúncio was not the unique candidate.
  - n=21: TED «Fornecimento de refeições em estabelecimentos escolares do Municipio de Vale de Cambra» (239 100.72) vs
    BASE 9953/2022 «Aquisição de serviços de Comunicações Móveis e Fixas» (140 000.00).
  - n=71: TED «CPN 56/2023/DICP … Requalificação da Escola Básica … D. Dinis - Leiria» (7 353 405.90) vs BASE 11804/2023
    «Concurso Público n.º 58/2023/DICP - Aquisição, por lotes, de material elétrico» (37 282.94).
  - n=78: TED «Fornecimento contínuo de combustíveis rodoviários» (330 000.00) vs BASE 6373/2023 «Aluguer de equipamentos
    audiovisuais … Festival da Juventude» (13 500.00).
  - n=127: TED «CPI n.º 26/2024» (AMA, three lots, 2 303 747.62) vs BASE 7025/2024 «Serviços de cibersegurança» (189 729.92).
- Parser errors found by B: 0. Checked after the result, not a pre-registered rule: of the 31 joins, 27 share the title
  with the BASE anúncio and agree on every compared value; the 4 that do not share it are exactly the 4 disagreements.
- The join rate (one third) is the larger weakness: the deadline date and buyer are not a reliable key between TED and
  BASE.

## What would settle B (not done; needs a decision)
A v3 for B only, written before its sample: join on buyer and deadline **and** the title (or the TED notice number BASE
carries, where it does), on a fresh sample of contract notices that excludes v1's and v2's. The C result above stands
for the parser.
