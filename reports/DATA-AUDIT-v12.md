# Audit of data-v12's rule-reading rows (2026-11-03, DECISIONS D67)

What AMALIA v12 learned from (training/data-v12/regra_lida/train.jsonl, 1 318 rows) against what it was measured on
(dev.jsonl, 104 rows). Error analysis is on dev only; the sealed set appears here only in the leak count, by article
text. Scripts: tools/preflight_data.py (the gate), and the profile in tools/make_rule_readings_v13.py.

Every row is a written article: an invented article in the CCP's style, with invented numbers, and its gold reading,
written for this project; code finds the quoted words in the text and the factory's checker must accept the gold. So the
training set is not the law, chosen. It is text we wrote, and its mix is what we decided.

## The defects, one by one

| # | what | train (v12) | dev | what v12 did on dev |
|---|---|---|---|---|
| 1 | written for the reading prompt v3 | 359 of 1 318 (27 %); 959 were written for the old prompt (batch-* 572, alvo-* 387) and only re-rendered | 104 of 104 | settles 63.9 % of old-shape articles (dev_antigo), 44.2 % of dev |
| 2 | «não tipável» | 98 (7.4 %): nao_e_limiar 49, nao_e_prazo_minimo 18, sem_vocabulario 16, texto_em_falta 15 | 25 (24.0 %): 5 / 7 / 6 / 7 | of the 25: rules on 19, the wrong reason on 3, 2 settle |
| 3 | article under titles | 221 (16.8 %) | 104 (100 %) | quotes from a title: 1.5 % of training quotes, 9.4 % of dev's |
| 4 | rows per kind of dev | nao_tipavel 98, capitulo 52, remissao 51, alineas 39, grandeza 31, casos 31, comparador 30, contagem 30, valor_condicao 29 | 25, 13, 15, 10, 10, 9, 4, 9, 9 | settles 2/25, 10/13, 8/15, 7/10, 6/10, 4/9, 3/4, 2/9, 4/9 |
| 5 | a quote is the vocabulary's first phrase, where it lists others | 70.5 % | 46.3 % | 11 answers quote words the text does not have (the vocabulary's: «ajuste direto e consulta prévia» under the title «Consulta prévia e ajuste direto»); 18 quote words that do not name the value |
| 6 | quotes from the target passage | 83.1 % | 72.7 % | 7 answers cite the target (or a neighbour) for words that are in the proémio, a neighbour or the referred number |
| 7 | stored schema in the factory's order | 0 of 1 318 (sort_keys) | 0 of 104 | the decoder forced «nao_tipavel» first: attempt 1 said «não tipável» on 100 of 104 (D66; read again with --order required) |
| 8 | training article close to a measured one (difflib ≥ 0.85) | 21: 9 to sealed, 3 to dev, 9 to dev_antigo | | data-v12 compared only v3-* with the new sets; the 9 can only have raised v12's sealed score |
| 9 | size | 1 318 rows, 2 epochs, final loss ≈ 0.001 | | it learned its rows by heart |

Checked and fine: answer key order (0 of 1 318 out of the schema's order), threshold key order, duplicate ids (none),
prompt length (median 14 317 characters in train, 14 399 in dev). In the whole v12 mix, rule reading is 22.4 % of the
answer characters, so the v3-shaped rows were about 6 %.

## The fix: data-v13 (tools/make_rule_readings_v13.py, BRIEF-D67.md)

| # | fix | gate check (tools/preflight_data.py) |
|---|---|---|
| 1, 4 | 13 new batches of 100 articles in the v3 shape (training/rule-readings/v4-*); every kind of dev ≥ 100 rows | kinds: every dev kind ≥ 100 |
| 2 | 40 of each 100 «não tipável», 10 per reason, each one detail away from typable | share within 5 points of dev; each reason ≥ 20 % |
| 3 | every new article under 2–3 titles; old articles placed under neutral titles that name nothing (tests show they change no reading) | titles ≥ 95 % |
| 5 | writers rotate the vocabulary's phrases (first phrase ≤ 40 % where others exist) and write lists in the sentence's order | first-phrase share ≤ dev's + 10 points |
| 6 | in half the typable new articles, a condition or parameter is said outside the target | (profile: quote roles) |
| 7 | rows store the factory's schema (no sort_keys) | schema = factory's, order included; answer keys follow it |
| 8 | every training article compared with every measured article; close ones left out | no training article close to a measured one |
| 9 | about twice the rows (≈ 2 500), most of them new | (profile: rows) |

The gate on data-v12: 7 of 8 checks fail (tests/test_preflight_data.py). training/train_lora.py runs it before v13 and
refuses the run if it fails. The comparador batches hold lt and le only: «superior a» / «igual ou superior a» wait for the
limiar product rule (evento:250 or 251).

## Texture: our articles against the real law (added the same day)

The same v3 context a reader is shown, for the 112 real CCP passages that state a deadline in days or a euro amount
(make_rule_readings_v13.real_contexts), for v12's training articles, and for dev. Surface features only; no answer read.

| | real law (112) | v12 training (1 318) | dev (104) | pilot batch v4-01 (100) |
|---|---|---|---|---|
| text shown, median characters | 1 981 | 506 | 530 | 535 |
| passages shown, median | 12 | 5 | 7 | 7 |
| target passage, median characters | 447 | 176 | 170 | 152 |
| values named in the shown text, median | 4 | 2 | 2 | 2 |
| target with a cross-reference | 55 % | 12 % | 31 % | 25 % |
| target with a qualifier («sem prejuízo», «salvo», …) | 21 % | 4 % | 3 % | 1 % |
| another law named | 18 % | 0 % | 0 % | 0 % |
| units other than days (dias úteis, meses, horas, %) | 23 % | 3 % | 4 % | 9 % |
| old spelling (concepção, sector, projecto, acto) | 27 % | 0 % | 0 % | 0 % |
| values named by the vocabulary's first listed phrase | 37 % | 49 % | 48 % | 12 % |

Every written article so far, test sets included, is tidier than the law: a quarter of the text, half the values, few
cross-references, no other laws, no old spelling. That is consistent with written articles that settle and real ones that
do not (v11: 96.7 % replicated on written sealed, 1 of 12 on round 5's real targets; v12: 0 of 12 in round 8). The pilot
batch fixed the labels and kinds but not the texture, and over-corrected the wording (12 %).

Fix: BRIEF-D67 sections 7 and 8 (articles as long and messy as the law's, each read for two targets; wording at the law's
37 %); the old spelling by code (make_rule_readings_v13.aged, about 27 % of the articles; tests: no reading changes); and
11 more gate checks against the real law (tools/preflight_data.py 0.2: the D67 rows inside BRIEF-D67's bands, at least
40 % of the rows; old spelling and wording within 10 points of the law's). The gate on data-v12: 17 of 18 checks fail.
The measured sets stay as they are, so dev cannot show this gain; the real-law round can.
