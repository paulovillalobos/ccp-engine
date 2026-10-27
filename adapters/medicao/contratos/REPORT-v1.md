# BASE contratos extraction test v1: result (CRITERIA-ted-contratos-v1.md applied as written)

Sample: 200 records of contratos2026.zip (sha256 2ac78c54…, back from Storage and checked), October 2026 and repeated
idcontrato left out (population 182 539), seed 20261027 (sample.json 1a03f8e8…, parsed.json 5058876e…, sealed in X.5).
Blind answers: blind/batch-00..19.json (reader-b-cli, model-b, batches of 10), saved before scoring.
Scores: score.json.

**Verdict as written: A, B and C pass. BASE contratos' extraction is measured.**

## A. Coverage (Wilson 95 %)
| field | share | interval | line |
|---|---|---|---|
| adjudicante | 200/200 | 98.1–100 | PASS |
| preco_contratual | 199/200 | 97.2–99.9 | PASS |
| data_publicacao_contrato | 200/200 | 98.1–100 | PASS |
| data_celebracao_contrato | 199/200 | 97.2–99.9 | — |
| preco_base | 197/200 | 95.7–99.5 | — |
| tipo_contrato | 191/200 | 91.7–97.6 | — (5 with several types, 4 «Locação de bens móveis» outside the vocabulary) |
| adjudicatario | 186/200 | 88.6–95.8 | — (14 with an adjudicatário without NIF, «-») |
| tipo_procedimento | 142/200 | 64.4–76.8 | — **partial**: 58 outside the vocabulary (43 «Ao abrigo de acordo-quadro» arts. 258.º/259.º, 12 «Contratação excluída II», 2 «Setores especiais – isenção parte II», 1 «Ajuste direto simplificado … Lei n.º 30/2021») |

## B. Against the anúncio's facts (adaptador:base-anuncios), by (nAnuncio, idINCM)
- With an nAnuncio: 26; joined to a 2026 procedure of E1: 17 (65.4 %, 46.2–80.6).
- Agreement on preco_base, tipo_procedimento, adjudicante, tipo_contrato: 64 / 64 = 100 % (94.3–100). **PASS.**
  Small: 17 contracts. Disagreements: none.

## C. Code against the blind reader
- 1 514 / 1 514 values = 100 % (99.7–100). **PASS.** Disagreements: none.

## Not settled here
tipo_procedimento's vocabulary leaves 29 % of 2026 contracts without a procedure type (framework-agreement call-offs and
excluded contracting). That is a mapping choice, recorded as partial, not a reading error.
