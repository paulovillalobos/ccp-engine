# Medição — leitura de regras com o protocolo v3 0.4 (2026-11-03)

Gerado por tools/measure_rule_readings_v13.py (ccp-measure-rule-readings-v13-0.1, protocolo ccp-read-rules-v3-0.4). Os artigos e o ouro de data-v12, os enunciados no protocolo 0.4. «Válida» = passa o verificador da fábrica contra o texto do artigo; «assenta» = válida e com o mesmo conteúdo canónico que a de ouro (as mesmas regras, citações e passagens à parte, ou o mesmo motivo de «não tipável»): o que a fábrica regista. «Citações pela gramática» = a resposta foi descodificada com a gramática que só deixa citar o texto (readers/quote_grammar.py). Intervalos de Wilson a 95 %.

## dev (104 artigos)

| leitor | respondidas | válidas | assenta |
|---|---|---|---|
| leitor-b (Reader B (família B)) | 100.0 % [96.4, 100.0] (104/104) | 100.0 % [96.4, 100.0] (104/104) | 94.2 % [88.0, 97.3] (98/104) |

Por que não assentam as de leitor-b: não tipável num e regras no outro 4; condição em falta: tipo_contrato 1; motivo nao_e_limiar em vez de sem_vocabulario 1.
Por estilo: comparador 3; capitulo 1; grandeza 1; nao_tipavel 1.

## sealed (96 artigos)

| leitor | respondidas | válidas | assenta |
|---|---|---|---|
| leitor-b (Reader B (família B)) | 97.9 % [92.7, 99.4] (94/96) | 96.9 % [91.2, 98.9] (93/96) | 89.6 % [81.9, 94.2] (86/96) |

