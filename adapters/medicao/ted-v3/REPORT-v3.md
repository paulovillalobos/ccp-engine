# TED extraction test v3, check B only: result (CRITERIA-ted-v3.md applied as written)

Sample: 100 TED-XML + 100 eForms contract notices with a deadline and a Portuguese buyer, seed 20261029, v1's and v2's
400 left out (population 22 432 + 21 446; sample.json fc0dd45f…, parsed.json 1173bb6e…, sealed in X.9). Parser
adapters/ted/parse.py 715a2dd5… (ORIGINAL form, title). Join and scoring: adapters/medicao/score.py f38bf3f8…
(score_ted_b, threshold 0.5), against BASE anúncios 2018–2026 (2018–2025 back from Storage, sha256 checked). Result:
score-b.json.

**Verdict as written: B passes, 189 / 192 = 98.4 % (95.5–99.5).** With v2's A (PASS) and C (99.9 %), TED's extraction is
measured.

## Joins
- Joinable: 102 / 200 (51.0 %, 44.1–57.8); eForms 85, TED-XML 17. Containment of the joined pairs: 1.0 for 93, 0.9 for 5,
  0.6 for 2, 0.5 for 2.
- Not joinable, out of the denominator: no BASE anúncio with the same buyer and deadline 78; best title containment under
  0.5: 15; two candidates tie: 5.

## The 3 disagreements
- **n=59, wrong join** (containment 0.62): TED «[DAG] Aquisição de serviços de manutenção corretiva e evolutiva da
  plataforma SIGLIC [2022…» (100 000.00) vs BASE 4539/2022 «[DAG] Aquisição de serviços de desenvolvimento, ativação e
  manutenção evolutiva e corretiv…» (172 800.00). Same buyer and deadline, overlapping words, two procedures.
- **n=70, wrong join** (containment 0.50, at the line): TED «(DAG) Aquisição de serviços para a reforma dos SI
  disponibilizados ao Cidadão - Grupo III» (four lots, 824 199.60) vs BASE 11888/2021 «[DAG]Aquisição de serviços para a
  reforma do SI dos Registos Nacionais Interoperabilidade…» (2 748 487.00).
- **n=165, the sources differ** (containment 1.0, same procedure, same value 520 000): TED's eForms codes
  `<cbc:ProcedureCode>restricted</cbc:ProcedureCode>`; BASE 17723/2024 gives modeloAnuncio «Concurso público». The parser
  read what the notice codes.
- Parser errors found by B: 0. The two wrong joins are counted, not dropped; without them B would read 189 / 190.

## Limits
- One TED contract notice in two finds its BASE anúncio by buyer, deadline and title; TED-XML years join much less
  (17 of 100) than eForms (85 of 100). B speaks for the joinable half.
- Pairs at 0.5–0.6 containment can still be wrong joins (n=59, n=70). A stricter line would trade joins for certainty;
  not changed after the result.
