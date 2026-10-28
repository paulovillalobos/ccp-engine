# Medição — leitura de regras, v11 (2026-10-28)

Gerado por tools/measure_rule_readings_v11.py (ccp-measure-rule-readings-v11-0.1). Cada leitura comparada com a de ouro em forma canónica, regra a regra (D43); «replica (D64)» = as mesmas regras sem as passagens, todas citando a passagem-alvo. Intervalos de Wilson a 95 %.

## dev (203 artigos)

| leitor | regras exatas | replica (D64) | conteúdo exato | número de regras certo | dias ou limites certos | inválidas |
|---|---|---|---|---|---|---|
| leitor-a12 (base + adaptador v10) | 84.7 % [79.1, 89.0] (172/203) | 87.7 % [82.5, 91.5] (178/203) | 87.7 % [82.5, 91.5] (178/203) | 100.0 % [98.1, 100.0] (203/203) | 99.5 % [97.3, 99.9] (202/203) | 0 |
| leitor-b (Reader B (família B)) | 78.8 % [72.7, 83.9] (160/203) | 98.0 % [95.0, 99.2] (199/203) | 98.0 % [95.0, 99.2] (199/203) | 99.5 % [97.3, 99.9] (202/203) | 99.5 % [97.3, 99.9] (202/203) | 0 |

Erros de leitor-a12 (leituras sem conteúdo exato; uma leitura conta uma vez em cada tipo): condição com outro valor: tipo_contrato 6; condição a mais: publicado_joue 4; condição em falta: tipo_contrato 4; condição a mais: tipo_procedimento 3; condição a mais: urgencia_fundamentada 3; limiar: comparator 2; condição a mais: tipo_contrato 1; condição com outro valor: modalidade_concecao 1; condição com outro valor: tipo_entidade 1; condição em falta: modalidade_concecao 1; condição em falta: publicado_joue 1; prazo: counted_from 1; prazo: deadline_field 1; prazo: minimum_days 1.
Por estilo: prazo_distratores 6; prazo_casos 5; limiar_dois_casos 4; limiar_tipos 3; prazo_reducao 2; prazo_em_regra 1; prazo_epigrafe 1; prazo_joue 1; prazo_nao_indicado 1; prazo_outros 1.

Erros de leitor-b (leituras sem conteúdo exato; uma leitura conta uma vez em cada tipo): condição a mais: urgencia_fundamentada 1; condição com outro valor: tipo_contrato 1; número de regras a mais 1; prazo: usual_days 1.
Por estilo: prazo_distratores 2; limiar_dois_casos 1; prazo_reducao 1.

## sealed (184 artigos)

| leitor | regras exatas | replica (D64) | conteúdo exato | número de regras certo | dias ou limites certos | inválidas |
|---|---|---|---|---|---|---|
| leitor-a12 (base + adaptador v10) | 87.0 % [81.3, 91.1] (160/184) | 91.3 % [86.3, 94.6] (168/184) | 91.3 % [86.3, 94.6] (168/184) | 100.0 % [98.0, 100.0] (184/184) | 99.5 % [97.0, 99.9] (183/184) | 0 |
| leitor-b (Reader B (família B)) | 81.0 % [74.7, 86.0] (149/184) | 98.9 % [96.1, 99.7] (182/184) | 98.9 % [96.1, 99.7] (182/184) | 99.5 % [97.0, 99.9] (183/184) | 99.5 % [97.0, 99.9] (183/184) | 1 |

## held_out_v10 (82 artigos)

| leitor | regras exatas | replica (D64) | conteúdo exato | número de regras certo | dias ou limites certos | inválidas |
|---|---|---|---|---|---|---|
| leitor-a12 (base + adaptador v10) | 69.5 % [58.9, 78.4] (57/82) | 76.8 % [66.6, 84.6] (63/82) | 76.8 % [66.6, 84.6] (63/82) | 98.8 % [93.4, 99.8] (81/82) | 97.6 % [91.5, 99.3] (80/82) | 0 |
| leitor-b (Reader B (família B)) | 85.4 % [76.1, 91.4] (70/82) | 98.8 % [93.4, 99.8] (81/82) | 98.8 % [93.4, 99.8] (81/82) | 100.0 % [95.5, 100.0] (82/82) | 100.0 % [95.5, 100.0] (82/82) | 0 |

