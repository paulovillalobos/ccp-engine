# The reading protocol v3 (DECISIONS D66): what 10/10 on paper means, and the proof

The protocol lives in code:
- `tools/read_rules_v3.py`: context, prompt, schema, checker, canonical form.
- `schemas/vocabulario-v3.json`: every value and the law's words for it.
- Tests: `tests/test_read_rules_v3.py`.

The person's product rules behind it are evento:249–253.

## The checklist (10/10 = all 12 pass)

| # | criterion | how it is tested | v1 (rounds 1–5) | v3 |
|---|---|---|---|---|
| C1 | **Context complete.** The reader needs nothing outside the prompt. | Every real target: the law's title, Parte/Título/Capítulo/Secção, the proémio (an article's own opening words too), the target's alíneas, and the passages it refers to. The passage holding a deadline or limit being modified is followed in a chain (192.2 → 192.1 → 191.3 → 191.1). | ✗ | ✓ |
| C2 | **No noise.** | Only the text in force, each passage once, the target and referred passages marked, only the references the target's chain uses. | ✗ | ✓ |
| C3 | **Neutral question.** | «Que regra do tipo X fixa a passagem Y?» presupposes no fact. | ✗ | ✓ |
| C4 | **One rulebook in the prompt, for both families.** | L1–L14 cover the 12 error kinds of rounds 1–5 and the 6 found by the v3 audit. | ✗ | ✓ |
| C5 | **Meaning defined.** | How the engine applies each rule type, and a test the reader runs before answering. | ✗ | ✓ |
| C6 | **Closed vocabulary in the law's words, one source.** | One JSON feeds the prompt and the checker. 95.7 % of the existing written training gold and 392 of the old eval articles pass as written, quotes derived by code (`make_rule_readings_v12.py check`). The rest is listed with a reason. | ½ | ✓ |
| C7 | **Every correct answer can be written, or the reader abstains honestly.** | lt/le/gt/ge; valor_estimado/preco_base/preco_contratual; amounts as conditions; several rules; «não tipável» with 4 closed reasons. | ✗ | ✓ |
| C8 | **Evidence.** | Every condition and parameter carries the exact words and the passage id. | ✗ | ✓ |
| C9 | **Verified by code.** | Correct answers on 7 real targets pass; broken copies with each mistake of rounds 1–5 fail. A quote cut out of a longer phrase fails. The prompt's own example passes and 9 broken copies fail. A recorded answer is checked again by verify (V3). | ✗ | ✓ |
| C10 | **Deterministic.** | All 33 real targets: each disputed point is decided by a named rule and shown words (below). Equivalent forms are normalised by code. | ✗ | ✓ |
| C11 | **Citations by code.** | Cited passages = the target + the passages its quotes come from. | ✗ | ✓ |
| C12 | **Train/serve parity.** | `make_rule_readings_v12.py` renders the training rows with the factory's own context, prompt and schema code, and checks every gold with the factory's own checker. | ✓ | ✓ |
| | **score** | | **2/12** | **12/12** |

Why it runs at about 9 rather than 10:
- AMALIA must learn to copy exact quotes.
- Real wording the glossary lacks shows up as rejected correct readings. Each is fixed with one line in the vocabulary file, and the rate is measured.
- Code decides which articles «artigos anteriores» names: the same chapter and the same start of heading (19.º and 20.º for 21.º).

## Paper audit of the real targets

This is not a reading. It is never gold, never training data, and never shown to a reader.

| target | v3 outcome | what decides it |
|---|---|---|
| 127.º-C n.º 1 a) | não tipável: nao_e_limiar | proémio «não podem ser convidadas»; a limiar must have the procedure it permits |
| 17.º-B n.º 4 | não tipável: nao_e_limiar | «ficam dispensadas do disposto no número anterior» |
| 54.º-A n.º 1 b) ii) | não tipável: nao_e_limiar | proémio «podem reservar» |
| 88.º n.º 2 a) | não tipável: nao_e_limiar | proémio «Pode não ser exigida prestação de caução»; the settled rule is withdrawn (D66) |
| 241.º-B n.º 3 b) | não tipável: sem_vocabulario | «Capítulo II — Sistemas de aquisição dinâmicos» |
| 21.º n.º 1 b), c) | limiar: the procedure; tipo_contrato not_in [bens, concessao_obras, concessao_servicos, obras, servicos, sociedade]; valor_estimado lt 130 000 / 75 000 | L6 with the headings of 19.º and 20.º shown as remissões; the proémio's exclusions; L2 («com convite a três entidades» is a requirement) |
| 31.º n.º 4 | limiar: in [ajuste_direto, consulta_previa]; both concessions; duracao_contrato_meses lt 12; valor_estimado lt 1 000 000 | «concessão de obras públicas ou de serviços» = both |
| 174.º n.º 3 | prazo: CLPQ; publicado_joue true; setores_especiais true; minimum 15, em regra 30 | L3, L7 (heading «com publicidade internacional»), L11 |
| 192.º n.º 2 | prazo: CLPQ; setores_especiais true; publicado_joue true; 10 days | L4 chain 192.1 → 191.3 → 191.1 |
| 198.º n.º 1 | prazo: procedimento_negociacao; publicado_joue true; 30 days | L3 «Capítulo IV — Procedimento de negociação»; L7; L13 |
| 198.º n.º 2 | prazo: procedimento_negociacao; anuncio_pre_informacao true; 25 days | L3, L7 |
| settled deadlines (174.1, 174.2, 190.1 ×2, 191.1, 191.5, 218, 219-B.5 ×2, 219-J.3, 135.1 ×2, 136.1) | the same content as settled | — |
| settled limits (19.º c), d)) | the same content; the threshold field becomes valor_estimado when read again | L10 |
