# Medição — leitura de regras com o protocolo v3 (2026-11-03)

Gerado por tools/measure_rule_readings_v12.py (ccp-measure-rule-readings-v12-0.1, protocolo ccp-read-rules-v3-0.3). «Válida» = passa o verificador da fábrica contra o texto do artigo; «assenta» = válida e com o mesmo conteúdo canónico que a de ouro (as mesmas regras, citações e passagens à parte, ou o mesmo motivo de «não tipável»): o que a fábrica regista. Intervalos de Wilson a 95 %.

## dev (104 artigos)

| leitor | respondidas | válidas | assenta |
|---|---|---|---|
| leitor-a13 (base + adaptador v11) | 100.0 % [96.4, 100.0] (104/104) | 81.7 % [73.2, 88.0] (85/104) | 4.8 % [2.1, 10.8] (5/104) |
| leitor-b (Reader B (família B)) | 100.0 % [96.4, 100.0] (104/104) | 92.3 % [85.5, 96.0] (96/104) | 80.8 % [72.2, 87.2] (84/104) |

Por que não assentam as de leitor-a13: não tipável num e regras no outro 64; verificador: não tipável: … não está em exemplo:art….… 10; verificador: não tipável com regras 7; motivo sem_vocabulario em vez de nao_e_prazo_minimo 6; motivo sem_vocabulario em vez de nao_e_limiar 4; motivo sem_vocabulario em vez de texto_em_falta 4; a resposta não é o objeto pedido 2; motivo texto_em_falta em vez de nao_e_prazo_minimo 1; motivo texto_em_falta em vez de sem_vocabulario 1.
Por estilo: nao_tipavel 20; remissao 15; capitulo 13; alineas 10; grandeza 10; casos 9; contagem 9; valor_condicao 9; comparador 4.

Por que não assentam as de leitor-b: não tipável num e regras no outro 10; condição em falta: tipo_contrato 2; verificador: counted_from data_envio_convite e as fontes dizem nada (L…) 2; verificador: … não está em exemplo:art….… 2; condição em falta: tipo_entidade 1; verificador: as fontes nomeiam também … (fonte mais curta, ou a condição está incompleta) 1; verificador: counted_from data_envio_anuncio e as fontes dizem nada (L…) 1; verificador: counted_from data_publicacao_anuncio e as fontes dizem nada (L…) 1; verificador: minimum_days … não está nas fontes (L…, L…) 1.
Por estilo: remissao 5; contagem 4; casos 3; grandeza 3; capitulo 2; alineas 1; comparador 1; valor_condicao 1.

## sealed (96 artigos)

| leitor | respondidas | válidas | assenta |
|---|---|---|---|
| leitor-a13 (base + adaptador v11) | 100.0 % [96.2, 100.0] (96/96) | 86.5 % [78.2, 91.9] (83/96) | 4.2 % [1.6, 10.2] (4/96) |
| leitor-b (Reader B (família B)) | 100.0 % [96.2, 100.0] (96/96) | 94.8 % [88.4, 97.8] (91/96) | 81.2 % [72.3, 87.8] (78/96) |

## dev_antigo (393 artigos)

| leitor | respondidas | válidas | assenta |
|---|---|---|---|
| leitor-a13 (base + adaptador v11) | 100.0 % [99.0, 100.0] (393/393) | 77.6 % [73.2, 81.5] (305/393) | 0.0 % [0.0, 1.0] (0/393) |

