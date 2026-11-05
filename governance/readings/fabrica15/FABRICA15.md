# FÁBRICA DE REGRAS — ronda 15 (DECISIONS D76)

Gerado por tools/rule_factory.py (ccp-rule-factory-0.8) com o protocolo de leitura v3 (tools/read_rules_v3.py, ccp-read-rules-v3-0.5). D76: v16 relê a ronda 12 (os mesmos prompts, byte a byte; as respostas cegas do leitor:b vêm da ronda 12). O exame é o grupo reservado; um alvo já assente é lido e medido mas não volta a ser registado. Propõe leitor:a18 (AMALIA + adaptador v16), leitor:b revê às cegas.

Protocolo 0.5. Um programa confirma cada palavra citada; o «não tipável» com o mesmo motivo também assenta.

| grupo | alvos | leitor A válido | leitor B válido | assentes | regras | «não tipável» |
|---|---|---|---|---|---|---|
| pratica | 110 | 95 | 85 | 13 | 1 | 12 |
| reservado | 30 | 23 | 23 | 4 | 0 | 4 |
| todos | 140 | 118 | 108 | 17 | 1 | 16 |

| regra | passagem | estado | replica | verificador: leitor A | verificador: leitor B |
|---|---|---|---|---|---|
| regra:ccp:auto-prazo-maximo-art43-v20180101@v1 | ccp:art43 | proposed (não tipável: nao_e_prazo_maximo) | — | ok | não tipável: fonte em ccp:art43.10.a, que é vizinho (L1) |
| regra:ccp:auto-prazo-maximo-art43-v20251028@v1 | ccp:art43 | proposed (não tipável: nao_e_prazo_maximo) | — | ok | não tipável: fonte em ccp:art43.10.a, que é vizinho (L1) |
| regra:ccp:auto-prazo-maximo-art72-v20180101@v1 | ccp:art72 | proposed (não tipável: nao_e_prazo_maximo) | não | ok | ok |
| regra:ccp:auto-prazo-maximo-art72-v20221202@v1 | ccp:art72 | proposed (não tipável: nao_e_prazo_maximo) | não | ok | ok |
| regra:ccp:auto-prazo-maximo-art72-3@v1 | ccp:art72.3 | proposed (não tipável: nao_e_prazo_maximo) | não | ok | ok |
| regra:ccp:auto-prazo-maximo-art78-v20180101@v1 | ccp:art78 | proposed (não tipável: nao_e_prazo_maximo) | — | ok | não tipável: fonte em ccp:art78.5, que é vizinho (L1) |
| regra:ccp:auto-prazo-maximo-art85-2@v1 | ccp:art85.2 | proposed (não tipável: nao_e_prazo_maximo) | não | ok | ok |
| regra:ccp:auto-prazo-maximo-art86-v20120811@v1 | ccp:art86 | proposed (não tipável: nao_e_prazo_maximo) | — | ok | não tipável: fonte em ccp:art86.2, que é vizinho (L1) |
| regra:ccp:auto-prazo-maximo-art86-2-v20091007@v1 | ccp:art86.2 | proposed (não tipável: nao_e_prazo_maximo) | não | ok | ok |
| regra:ccp:auto-prazo-maximo-art86-3@v1 | ccp:art86.3 | proposed (não tipável: nao_e_prazo_maximo) | não | ok | ok |
| regra:ccp:auto-prazo-maximo-art87-a-2@v1 | ccp:art87-a.2 | proposed (não tipável: nao_e_prazo_maximo) | não | ok | ok |
| regra:ccp:auto-prazo-maximo-art90-1@v1 | ccp:art90.1 | proposed (não tipável: nao_e_prazo_maximo) | não | ok | ok |
| regra:ccp:auto-prazo-maximo-art91-2@v1 | ccp:art91.2 | proposed (não tipável: nao_e_prazo_maximo) | não | ok | ok |
| regra:ccp:auto-prazo-maximo-art93-2@v1 | ccp:art93.2 | proposed (não tipável: nao_e_prazo_maximo) | não | ok | ok |
| regra:ccp:auto-prazo-maximo-art95-v20080730@v1 | ccp:art95 | proposed (não tipável: nao_e_prazo_maximo) | — | ok | não tipável: fonte em ccp:art95.1.c.i, que é vizinho (L1) |
| regra:ccp:auto-prazo-maximo-art101@v1 | ccp:art101 | proposed (não tipável: nao_e_prazo_maximo) | — | ok | regra 1: as fontes de maximum_days não dizem um máximo («não pode ser superior a», «no prazo de», L8) |
| regra:ccp:auto-prazo-maximo-art102-v20080730@v1 | ccp:art102 | proposed (não tipável: nao_e_prazo_maximo) | — | ok | não tipável: fonte em ccp:art102.2, que é vizinho (L1) |
| regra:ccp:auto-prazo-minimo-art104-v20080730@v1 | ccp:art104 | proposed (não tipável: nao_e_prazo_minimo) | — | ok | não tipável: fonte em ccp:art104.1, que é vizinho (L1) |
| regra:ccp:auto-prazo-maximo-art115-1-j-v20180101@v1 | ccp:art115.1.j | proposed (não tipável: nao_e_prazo_maximo) | não | ok | ok |
| regra:ccp:auto-prazo-maximo-art115-1-k@v1 | ccp:art115.1.k | proposed (não tipável: nao_e_prazo_maximo) | não | ok | ok |
| regra:ccp:auto-prazo-maximo-art122-v20180101@v1 | ccp:art122 | proposed (não tipável: nao_e_prazo_maximo) | — | ok | não tipável: fonte em ccp:art122.1, que é vizinho (L1) |
| regra:ccp:auto-prazo-minimo-art135-2-v20080730@v1 | ccp:art135.2 | sem leitura válida de leitor:a18 | — | regra 1: counted_from data_envio_anuncio e as fontes dizem nada (L9) | ok |
| regra:ccp:auto-prazo-minimo-art136-1-v20080730@v1 | ccp:art136.1 | sem leitura válida de leitor:a18 | — | regra 1, publicado_joue eq True: as fontes não afirmam o facto (L7) | ok |
| regra:ccp:auto-prazo-minimo-art136-3-v20080730@v1 | ccp:art136.3 | proposed (não tipável: nao_e_prazo_minimo) | não | ok | ok |
| regra:ccp:auto-prazo-minimo-art136-4-v20080730@v1 | ccp:art136.4 | proposed (não tipável: nao_e_prazo_minimo) | não | ok | ok |
| regra:ccp:auto-prazo-maximo-art138-3@v1 | ccp:art138.3 | proposed (não tipável: nao_e_prazo_maximo) | não | ok | ok |
| regra:ccp:auto-limiar-art155-a@v1 | ccp:art155.a | proposed (2 regras) | não | ok | ok |
| regra:ccp:auto-prazo-maximo-art161@v1 | ccp:art161 | proposed (não tipável: nao_e_prazo_maximo) | não | ok | ok |
| regra:ccp:auto-prazo-maximo-art161-b-4@v1 | ccp:art161-b.4 | proposed (não tipável: nao_e_prazo_maximo) | não | ok | ok |
| regra:ccp:auto-prazo-minimo-art173@v1 | ccp:art173 | sem leitura válida de leitor:a18 | — | regra 1: counted_from data_envio_anuncio e as fontes dizem nada (L9) | ok |
| regra:ccp:auto-prazo-minimo-art174-v20180101@v1 | ccp:art174 | proposed (3 regras) | — | ok | regra 1, tipo_procedimento eq concurso_limitado_previa_qualificacao: fonte em ccp:art174.1, que é vizinho (L1) |
| regra:ccp:auto-prazo-minimo-art174-1-v20080730@v1 | ccp:art174.1 | sem leitura válida de leitor:a18 | — | regra 1, publicado_joue eq True: as fontes não afirmam o facto (L7) | ok |
| regra:ccp:auto-prazo-minimo-art174-2-v20080730@v1 | ccp:art174.2 | sem leitura válida de leitor:a18 | — | regra 1: counted_from data_envio_convite e as fontes dizem nada (L9) | ok |
| regra:ccp:auto-prazo-minimo-art174-3-v20080730@v1 | ccp:art174.3 | proposed (não tipável: nao_e_prazo_minimo) | não | ok | ok |
| regra:ccp:auto-prazo-minimo-art174-4@v1 | ccp:art174.4 | proposed (não tipável: nao_e_prazo_minimo) | não | ok | ok |
| regra:ccp:auto-prazo-maximo-art177-3@v1 | ccp:art177.3 | proposed (não tipável: nao_e_prazo_maximo) | não | ok | ok |
| regra:ccp:auto-prazo-minimo-art187-2-v20180101@v1 | ccp:art187.2 | proposed (não tipável: nao_e_prazo_minimo) | não | ok | ok |
| regra:ccp:auto-prazo-maximo-art187-4-v20180101@v1 | ccp:art187.4 | proposed (não tipável: nao_e_prazo_maximo) | não | ok | ok |
| regra:ccp:auto-prazo-maximo-art188-4@v1 | ccp:art188.4 | proposed (não tipável: nao_e_prazo_maximo) | não | ok | ok |
| regra:ccp:auto-prazo-minimo-art190-2-v20080730@v1 | ccp:art190.2 | sem leitura válida de leitor:a18 | — | regra 1: minimum_days 8 não está nas fontes (L8, L4) | ok |
| regra:ccp:auto-prazo-minimo-art190-2@v1 | ccp:art190.2 | proposed (2 regras) | não | ok | ok |
| regra:ccp:auto-prazo-minimo-art191-v20180101@v1 | ccp:art191 | proposed (3 regras) | — | ok | não tipável: fonte em ccp:art191.2, que é vizinho (L1) |
| regra:ccp:auto-prazo-maximo-art192-3@v1 | ccp:art192.3 | proposed (não tipável: nao_e_prazo_maximo) | não | ok | ok |
| regra:ccp:auto-prazo-maximo-art192-4@v1 | ccp:art192.4 | proposed (não tipável: nao_e_prazo_maximo) | não | ok | ok |
| regra:ccp:auto-prazo-minimo-art198-1-v20080730@v1 | ccp:art198.1 | proposed | — | ok | regra 1, publicado_joue eq True: as fontes não afirmam o facto (L7) |
| regra:ccp:auto-prazo-minimo-art218-v20080730@v1 | ccp:art218 | proposed | — | ok | regra 1, tipo_procedimento eq dialogo_concorrencial: «diálogo concorrencial» não está em ccp:art218 |
| regra:ccp:auto-prazo-maximo-art219-i-5@v1 | ccp:art219-i.5 | proposed (não tipável: nao_e_prazo_maximo) | não | ok | ok |
| regra:ccp:auto-prazo-maximo-art234-1-v20080730@v1 | ccp:art234.1 | proposed (não tipável: nao_e_prazo_minimo) | não | ok | ok |
| regra:ccp:auto-prazo-maximo-art241-3-v20080730@v1 | ccp:art241.3 | proposed (não tipável: sem_vocabulario) | não | ok | ok |
| regra:ccp:auto-prazo-maximo-art241-a-3@v1 | ccp:art241-a.3 | proposed (não tipável: sem_vocabulario) | não | ok | ok |
| regra:ccp:auto-prazo-minimo-art242-3-v20080730@v1 | ccp:art242.3 | proposed (não tipável: sem_vocabulario) | não | ok | ok |
| regra:ccp:auto-prazo-maximo-art270@v1 | ccp:art270 | proposed (não tipável: nao_e_prazo_minimo) | não | ok | ok |
| regra:ccp:auto-prazo-maximo-art273@v1 | ccp:art273 | proposed (não tipável: nao_e_prazo_maximo) | não | ok | ok |
| regra:ccp:auto-prazo-minimo-art276-v20120811@v1 | ccp:art276 | proposed (não tipável: nao_e_prazo_minimo) | não | ok | ok |
| regra:ccp:auto-prazo-minimo-art276-v20180101@v1 | ccp:art276 | proposed (não tipável: nao_e_prazo_minimo) | não | ok | ok |
| regra:ccp:auto-prazo-minimo-art276-v20210620@v1 | ccp:art276 | proposed (não tipável: nao_e_prazo_minimo) | não | ok | ok |
| regra:ccp:auto-prazo-minimo-art276-5-v20080730@v1 | ccp:art276.5 | proposed (não tipável: nao_e_prazo_minimo) | não | ok | ok |
| regra:ccp:auto-prazo-maximo-art283-a-v20110113@v1 | ccp:art283-a | proposed (não tipável: nao_e_prazo_maximo) | — | ok | não tipável: fonte em ccp:art283-a.2.c, que é vizinho (L1) |
| regra:ccp:auto-prazo-maximo-art283-a-v20210620@v1 | ccp:art283-a | proposed (não tipável: nao_e_prazo_maximo) | — | ok | não tipável: fonte em ccp:art283-a.2.c, que é vizinho (L1) |
| regra:ccp:auto-prazo-minimo-art295-v20091007@v1 | ccp:art295 | proposed (não tipável: nao_e_prazo_minimo) | — | ok | não tipável: fonte em ccp:art295.3, que é vizinho (L1) |
| regra:ccp:auto-prazo-maximo-art315-v20210620@v1 | ccp:art315 | proposed (não tipável: nao_e_prazo_maximo) | — | ok | não tipável: fonte em ccp:art315.1, que é vizinho (L1) |
| regra:ccp:auto-prazo-minimo-art327-v20080730@v1 | ccp:art327 | proposed (não tipável: nao_e_prazo_minimo) | — | ok | não tipável: fonte em ccp:art327.3, que é vizinho (L1) |
| regra:ccp:auto-prazo-maximo-art345-3@v1 | ccp:art345.3 | proposed (não tipável: nao_e_prazo_maximo) | — | ok | regra 1: as fontes de maximum_days não dizem um máximo («não pode ser superior a», «no prazo de», L8) |
| regra:ccp:auto-prazo-maximo-art345-4@v1 | ccp:art345.4 | proposed (não tipável: nao_e_prazo_maximo) | não | ok | ok |
| regra:ccp:auto-prazo-maximo-art354-v20080730@v1 | ccp:art354 | proposed (não tipável: nao_e_prazo_maximo) | — | ok | não tipável: fonte em ccp:art354.2, que é vizinho (L1) |
| regra:ccp:auto-prazo-maximo-art354-2@v1 | ccp:art354.2 | proposed (não tipável: nao_e_prazo_maximo) | não | ok | ok |
| regra:ccp:auto-prazo-maximo-art372-1-v20080730@v1 | ccp:art372.1 | proposed (não tipável: nao_e_prazo_maximo) | não | ok | ok |
| regra:ccp:auto-prazo-maximo-art372-1-v20180101@v1 | ccp:art372.1 | proposed (não tipável: nao_e_prazo_maximo) | não | ok | ok |
| regra:ccp:auto-prazo-maximo-art372-1-v20210620@v1 | ccp:art372.1 | proposed (não tipável: nao_e_prazo_maximo) | não | ok | ok |
| regra:ccp:auto-prazo-maximo-art372-1@v1 | ccp:art372.1 | proposed (não tipável: nao_e_prazo_maximo) | não | ok | ok |
| regra:ccp:auto-prazo-maximo-art373-v20210620@v1 | ccp:art373 | proposed (não tipável: nao_e_prazo_maximo) | — | ok | não tipável: fonte em ccp:art373.2, que é vizinho (L1) |
| regra:ccp:auto-prazo-maximo-art373-2-v20080730@v1 | ccp:art373.2 | proposed (não tipável: nao_e_prazo_maximo) | não | ok | ok |
| regra:ccp:auto-prazo-maximo-art373-2-v20091007@v1 | ccp:art373.2 | proposed (não tipável: nao_e_prazo_maximo) | não | ok | ok |
| regra:ccp:auto-prazo-maximo-art373-2@v1 | ccp:art373.2 | proposed (não tipável: nao_e_prazo_maximo) | não | ok | ok |
| regra:ccp:auto-prazo-maximo-art373-3@v1 | ccp:art373.3 | proposed (não tipável: nao_e_prazo_maximo) | não | ok | ok |
| regra:ccp:auto-prazo-maximo-art378-3-v20180101@v1 | ccp:art378.3 | proposed (não tipável: nao_e_prazo_maximo) | não | ok | ok |
| regra:ccp:auto-prazo-maximo-art378-4@v1 | ccp:art378.4 | proposed (não tipável: nao_e_prazo_maximo) | não | ok | ok |
| regra:ccp:auto-prazo-maximo-art385-v20230715@v1 | ccp:art385 | proposed (não tipável: nao_e_prazo_maximo) | — | ok | não tipável: fonte em ccp:art385.3, que é vizinho (L1) |
| regra:ccp:auto-prazo-maximo-art401-1@v1 | ccp:art401.1 | proposed (não tipável: nao_e_prazo_maximo) | não | ok | ok |
| regra:ccp:auto-prazo-maximo-art404-1@v1 | ccp:art404.1 | proposed (não tipável: nao_e_prazo_maximo) | não | ok | ok |
| regra:ccp:auto-prazo-maximo-art405-v20080730@v1 | ccp:art405 | proposed (não tipável: nao_e_prazo_maximo) | — | ok | não tipável: fonte em ccp:art405.1, que é vizinho (L1) |
| regra:ccp:auto-prazo-maximo-art405-v20210620@v1 | ccp:art405 | proposed (não tipável: nao_e_prazo_maximo) | — | ok | não tipável: fonte em ccp:art405.1.d, que é vizinho (L1) |
| regra:ccp:auto-prazo-maximo-art464-a-v20210620@v1 | ccp:art464-a | proposed (não tipável: nao_e_prazo_maximo) | — | ok | não tipável: fonte em ccp:art464-a.1, que é vizinho (L1) |
| regra:ccp:auto-prazo-maximo-art464-e-2@v1 | ccp:art464-e.2 | proposed (não tipável: nao_e_prazo_maximo) | não | ok | ok |
| regra:eu-1989-665:auto-prazo-minimo-art2-a-2@v1 | eu-1989-665:art2-a.2 | settled (não tipável: nao_e_prazo_minimo) | sim | ok | ok |
| regra:eu-1989-665:auto-prazo-minimo-art2-c@v1 | eu-1989-665:art2-c | proposed (não tipável: sem_vocabulario) | — | ok | não tipável: «Prazos para interposição de recurso» não está em eu-1989-665:art2-c |
| regra:eu-1992-13:auto-prazo-minimo-art2-c@v1 | eu-1992-13:art2-c | proposed (não tipável: sem_vocabulario) | — | ok | não tipável: «Prazos para interposição de recurso» não está em eu-1992-13:art2-c |
| regra:eu-2004-17:auto-prazo-maximo-art15-4-v20041101@v1 | eu-2004-17:art15.4 | proposed (não tipável: sem_vocabulario) | não | ok | ok |
| regra:eu-2004-17:auto-prazo-minimo-art45-3-a-v20041101@v1 | eu-2004-17:art45.3.a | sem leitura válida de leitor:a18 | — | regra 1, tipo_procedimento in ['concurso_limitado_previa_qualificacao', 'procedimento_negociacao_com_concurso']: as font | ok |
| regra:eu-2004-17:auto-prazo-minimo-art45-3-c-v20041101@v1 | eu-2004-17:art45.3.c | sem leitura válida de leitor:a18 | — | regra 1, tipo_procedimento in ['concurso_limitado_previa_qualificacao', 'procedimento_negociacao_com_concurso']: as font | ok |
| regra:eu-2004-17:auto-prazo-minimo-art45-4-v20041101@v1 | eu-2004-17:art45.4 | proposed | não | ok | ok |
| regra:eu-2004-17:auto-prazo-maximo-art45-5-v20041101@v1 | eu-2004-17:art45.5 | settled (não tipável: nao_e_prazo_maximo) | sim | ok | ok |
| regra:eu-2004-17:auto-prazo-minimo-art45-7-v20041101@v1 | eu-2004-17:art45.7 | proposed (não tipável: nao_e_prazo_minimo) | não | ok | ok |
| regra:eu-2004-17:auto-prazo-minimo-art45-8-v20041101@v1 | eu-2004-17:art45.8 | proposed (não tipável: nao_e_prazo_minimo) | não | ok | ok |
| regra:eu-2004-18:auto-limiar-art9-4-a-v20040430@v1 | eu-2004-18:art9.4.a | settled (não tipável: nao_e_limiar) | sim | ok | ok |
| regra:eu-2004-18:auto-limiar-art9-4-b-v20040430@v1 | eu-2004-18:art9.4.b | settled (não tipável: nao_e_limiar) | sim | ok | ok |
| regra:eu-2004-18:auto-limiar-art9-5-b-v20041101@v1 | eu-2004-18:art9.5.b | settled (não tipável: nao_e_limiar) | sim | ok | ok |
| regra:eu-2004-18:auto-prazo-maximo-art33-4-v20040430@v1 | eu-2004-18:art33.4 | proposed (não tipável: sem_vocabulario) | não | ok | ok |
| regra:eu-2004-18:auto-limiar-art35-1-a-v20040430@v1 | eu-2004-18:art35.1.a | settled (não tipável: nao_e_limiar) | sim | ok | ok |
| regra:eu-2004-18:auto-prazo-minimo-art38-3-a-v20040430@v1 | eu-2004-18:art38.3.a | sem leitura válida de leitor:a18 | — | regra 1: deadline_field prazo_reclamacao_dias e as fontes dizem ['prazo_candidaturas_dias'] (L9) | ok |
| regra:eu-2004-18:auto-prazo-minimo-art38-4-v20040430@v1 | eu-2004-18:art38.4 | proposed (não tipável: nao_e_prazo_minimo) | não | ok | ok |
| regra:eu-2004-18:auto-prazo-maximo-art38-5-v20040430@v1 | eu-2004-18:art38.5 | settled (não tipável: nao_e_prazo_maximo) | sim | ok | ok |
| regra:eu-2004-18:auto-prazo-minimo-art38-8-a-v20040430@v1 | eu-2004-18:art38.8.a | sem leitura válida de leitor:a18 | — | regra 1, tipo_procedimento in ['procedimento_negociacao', 'procedimento_concorrencial_negociacao']: as fontes não nomeia | ok |
| regra:eu-2004-18:auto-prazo-minimo-art38-8-b-v20040430@v1 | eu-2004-18:art38.8.b | proposed (não tipável: nao_e_prazo_minimo) | não | ok | ok |
| regra:eu-2004-18:auto-prazo-minimo-art59-v20040430@v1 | eu-2004-18:art59 | proposed | não | ok | ok |
| regra:eu-2004-18:auto-prazo-minimo-art65-v20040430@v1 | eu-2004-18:art65 | sem leitura válida de leitor:a18 | — | regra 1, tipo_procedimento in ['concurso_limitado_previa_qualificacao', 'concurso_publico', 'dialogo_concorrencial', 'pr | ok |
| regra:eu-2004-18:auto-limiar-art67-1-a-v20160101@v1 | eu-2004-18:art67.1.a | settled (não tipável: nao_e_limiar) | sim | ok | ok |
| regra:eu-2004-18:auto-limiar-art67-1-b-v20160101@v1 | eu-2004-18:art67.1.b | settled (não tipável: nao_e_limiar) | sim | ok | ok |
| regra:eu-2009-81:auto-limiar-art8-a@v1 | eu-2009-81:art8.a | settled (não tipável: nao_e_limiar) | sim | ok | ok |
| regra:eu-2009-81:auto-limiar-art8-b@v1 | eu-2009-81:art8.b | settled (não tipável: nao_e_limiar) | sim | ok | ok |
| regra:eu-2009-81:auto-limiar-art9-4-a@v1 | eu-2009-81:art9.4.a | settled (não tipável: nao_e_limiar) | sim | ok | ok |
| regra:eu-2009-81:auto-prazo-minimo-art33-2@v1 | eu-2009-81:art33.2 | sem leitura válida de leitor:a18 | — | regra 1: deadline_field prazo_reclamacao_dias e as fontes dizem ['prazo_candidaturas_dias'] (L9) | ok |
| regra:eu-2009-81:auto-prazo-minimo-art33-3@v1 | eu-2009-81:art33.3 | sem leitura válida de leitor:a18 | — | regra 1: counted_from data_envio_convite e as fontes dizem nada (L9) | ok |
| regra:eu-2009-81:auto-prazo-minimo-art59@v1 | eu-2009-81:art59 | proposed (não tipável: sem_vocabulario) | — | ok | não tipável: «Prazos para interposição de recurso» não está em eu-2009-81:art59 |
| regra:eu-2014-23:auto-prazo-maximo-art33-2@v1 | eu-2014-23:art33.2 | settled (não tipável: nao_e_prazo_maximo) | sim | ok | ok |
| regra:eu-2014-23:auto-prazo-minimo-art39-3@v1 | eu-2014-23:art39.3 | sem leitura válida de leitor:a18 | — | regra 1, tipo_contrato eq concessao_obras: as fontes não nomeiam ['concessao_obras'] | ok |
| regra:eu-2014-23:auto-prazo-minimo-art39-4@v1 | eu-2014-23:art39.4 | sem leitura válida de leitor:a18 | — | regra 1, tipo_contrato eq concessao_obras: as fontes não nomeiam ['concessao_obras'] | ok |
| regra:eu-2014-24:auto-prazo-minimo-art27-2-b@v1 | eu-2014-24:art27.2.b | settled (não tipável: nao_e_prazo_minimo) | sim | ok | ok |
| regra:eu-2014-24:auto-prazo-minimo-art27-3@v1 | eu-2014-24:art27.3 | proposed | não | ok | ok |
| regra:eu-2014-24:auto-prazo-minimo-art28-1@v1 | eu-2014-24:art28.1 | proposed | não | ok | ok |
| regra:eu-2014-24:auto-prazo-minimo-art28-2@v1 | eu-2014-24:art28.2 | sem leitura válida de leitor:a18 | — | regra 1, tipo_procedimento eq concurso_limitado_previa_qualificacao: as fontes não nomeiam ['concurso_limitado_previa_qu | ok |
| regra:eu-2014-24:auto-prazo-minimo-art28-3-b@v1 | eu-2014-24:art28.3.b | proposed (não tipável: nao_e_prazo_minimo) | não | ok | ok |
| regra:eu-2014-24:auto-prazo-minimo-art28-4@v1 | eu-2014-24:art28.4 | proposed (não tipável: nao_e_prazo_minimo) | não | ok | ok |
| regra:eu-2014-24:auto-prazo-minimo-art28-6-a@v1 | eu-2014-24:art28.6.a | proposed (não tipável: nao_e_prazo_minimo) | não | ok | ok |
| regra:eu-2014-24:auto-prazo-minimo-art28-6-b@v1 | eu-2014-24:art28.6.b | proposed (não tipável: nao_e_prazo_minimo) | não | ok | ok |
| regra:eu-2014-24:auto-prazo-minimo-art29-1@v1 | eu-2014-24:art29.1 | proposed | não | ok | ok |
| regra:eu-2014-24:auto-prazo-minimo-art30-1@v1 | eu-2014-24:art30.1 | sem leitura válida de leitor:a18 | — | regra 1, tipo_procedimento eq dialogo_concorrencial: as fontes não nomeiam ['dialogo_concorrencial'] | regra 1, tipo_procedimento eq dialogo_concorrencial: as fontes não nomeiam ['dialogo_concorrencial'] |
| regra:eu-2014-24:auto-prazo-maximo-art34-5@v1 | eu-2014-24:art34.5 | proposed (não tipável: sem_vocabulario) | não | ok | ok |
| regra:eu-2014-24:auto-prazo-maximo-art50-3@v1 | eu-2014-24:art50.3 | settled (não tipável: nao_e_prazo_maximo) | sim | ok | ok |
| regra:eu-2014-25:auto-limiar-art15-b@v1 | eu-2014-25:art15.b | sem leitura válida de leitor:a18 | — | regra 1, tipo_procedimento in ['concurso_aberto', 'concurso_concecao']: as fontes não nomeiam ['concurso_aberto', 'concu | ok |
| regra:eu-2014-25:auto-prazo-minimo-art45-3@v1 | eu-2014-25:art45.3 | settled | sim | ok | ok |
| regra:eu-2014-25:auto-prazo-maximo-art45-4@v1 | eu-2014-25:art45.4 | proposed (não tipável: nao_e_prazo_maximo) | — | ok | não tipável: fonte em eu-2014-25:art45.1, que é vizinho (L1) |
| regra:eu-2014-25:auto-prazo-minimo-art46-1@v1 | eu-2014-25:art46.1 | sem leitura válida de leitor:a18 | — | regra 1: usual_days sem «em regra» e os dias nas fontes (L11) | ok |
| regra:eu-2014-25:auto-prazo-minimo-art46-2@v1 | eu-2014-25:art46.2 | proposed (não tipável: nao_e_prazo_minimo) | não | ok | ok |
| regra:eu-2014-25:auto-prazo-minimo-art47-1@v1 | eu-2014-25:art47.1 | sem leitura válida de leitor:a18 | — | regra 1: usual_days sem «em regra» e os dias nas fontes (L11) | ok |
| regra:eu-2014-25:auto-prazo-minimo-art47-2@v1 | eu-2014-25:art47.2 | proposed (não tipável: nao_e_prazo_minimo) | não | ok | ok |
| regra:eu-2014-25:auto-prazo-minimo-art48-1@v1 | eu-2014-25:art48.1 | sem leitura válida de leitor:a18 | — | regra 1, tipo_procedimento eq dialogo_concorrencial: as fontes não nomeiam ['dialogo_concorrencial'] | regra 1, tipo_procedimento eq dialogo_concorrencial: as fontes não nomeiam ['dialogo_concorrencial'] |
| regra:eu-2014-25:auto-prazo-minimo-art49-1@v1 | eu-2014-25:art49.1 | sem leitura válida de leitor:a18 | — | regra 1: usual_days sem «em regra» e os dias nas fontes (L11) | regra 1: usual_days sem «em regra» e os dias nas fontes (L11) |
| regra:eu-2014-25:auto-prazo-maximo-art52-5@v1 | eu-2014-25:art52.5 | proposed (não tipável: sem_vocabulario) | não | ok | ok |
| regra:eu-2014-25:auto-prazo-maximo-art70-2@v1 | eu-2014-25:art70.2 | settled (não tipável: nao_e_prazo_maximo) | sim | ok | ok |

## regra:ccp:auto-prazo-maximo-art43-v20180101@v1

- leitor:a18: não tipável (nao_e_prazo_maximo): O prazo é o da própria entidade adjudicante para incluir o projeto de execução, não um prazo máximo para os interessados apresentarem algo.
- leitor:b: não tipável (nao_e_prazo_maximo): Os prazos de cinco dias destinam-se à própria entidade adjudicante ou ao contraente público para sanar a nulidade.
- verificador (B): não tipável: fonte em ccp:art43.10.a, que é vizinho (L1); não tipável: fonte em ccp:art43.10.b, que é vizinho (L1); não tipável: fonte em ccp:art43.10.c, que é vizinho (L1)

## regra:ccp:auto-prazo-maximo-art43-v20251028@v1

- leitor:a18: não tipável (nao_e_prazo_maximo): O prazo é o da própria entidade adjudicante para incluir o projeto de execução, não um prazo máximo para os interessados apresentarem algo.
- leitor:b: não tipável (nao_e_prazo_maximo): Os prazos de cinco dias são para a própria entidade adjudicante ou para o contraente público sanar a nulidade.
- verificador (B): não tipável: fonte em ccp:art43.10.a, que é vizinho (L1); não tipável: fonte em ccp:art43.10.b, que é vizinho (L1); não tipável: fonte em ccp:art43.10.c, que é vizinho (L1)

## regra:ccp:auto-prazo-maximo-art72-v20180101@v1

- leitor:a18: não tipável (nao_e_prazo_maximo): O prazo é um máximo de cinco dias para o suprimento das irregularidades, não um prazo para os concorrentes apresentarem algo.
- leitor:b: não tipável (sem_vocabulario): O vocabulário não prevê um campo de prazo para o suprimento de irregularidades das propostas e candidaturas.

## regra:ccp:auto-prazo-maximo-art72-v20221202@v1

- leitor:a18: não tipável (nao_e_prazo_maximo): O prazo é um máximo de cinco dias para suprir irregularidades, não um prazo para os concorrentes apresentarem algo.
- leitor:b: não tipável (sem_vocabulario): O vocabulário não prevê um campo de prazo para o suprimento de irregularidades formais de candidaturas e propostas.

## regra:ccp:auto-prazo-maximo-art72-3@v1

- leitor:a18: não tipável (nao_e_prazo_maximo): O prazo é um máximo de cinco dias para o suprimento de irregularidades, não um prazo para os interessados apresentarem algo.
- leitor:b: não tipável (sem_vocabulario): O vocabulário não contém um campo de prazo para o suprimento de irregularidades formais de candidaturas e propostas.

## regra:ccp:auto-prazo-maximo-art78-v20180101@v1

- leitor:a18: não tipável (nao_e_prazo_maximo): O prazo é da própria entidade adjudicante para publicar o anúncio, não um prazo máximo para os interessados apresentarem algo.
- leitor:b: não tipável (nao_e_prazo_maximo): Os prazos são para a publicação de anúncios pela entidade adjudicante, não para apresentar elementos.
- verificador (B): não tipável: fonte em ccp:art78.5, que é vizinho (L1)

## regra:ccp:auto-prazo-maximo-art85-2@v1

- leitor:a18: não tipável (nao_e_prazo_maximo): O prazo é um máximo de prorrogação do próprio órgão competente, não um prazo para os concorrentes apresentarem os documentos de habilitação.
- leitor:b: não tipável (sem_vocabulario): O vocabulário não permite representar o máximo de cinco dias da prorrogação, distinto do prazo total para apresentar os documentos de habilitação.

## regra:ccp:auto-prazo-maximo-art86-v20120811@v1

- leitor:a18: não tipável (nao_e_prazo_maximo): O prazo é do próprio órgão da entidade adjudicante para notificar, não um prazo máximo para os adjudicatários apresentarem os documentos.
- leitor:b: não tipável (sem_vocabulario): O vocabulário não permite representar a condição de ocorrência de um facto que determine a caducidade da adjudicação nos termos do n.º 1.
- verificador (B): não tipável: fonte em ccp:art86.2, que é vizinho (L1)

## regra:ccp:auto-prazo-maximo-art86-2-v20091007@v1

- leitor:a18: não tipável (nao_e_prazo_maximo): O prazo é um máximo de 15 dias para a própria entidade adjudicante notificar o adjudicatário, não um prazo para os interessados apresentarem algo.
- leitor:b: não tipável (sem_vocabulario): O vocabulário não permite representar a condição de ocorrência de um facto que determine a caducidade da adjudicação nos termos do n.º 1.

## regra:ccp:auto-prazo-maximo-art86-3@v1

- leitor:a18: não tipável (nao_e_prazo_maximo): O prazo é um máximo de cinco dias, não um prazo para apresentar algo.
- leitor:b: não tipável (sem_vocabulario): Falta no vocabulário uma condição que represente a ocorrência de um facto que determine a caducidade da adjudicação nos termos do n.º 2.

## regra:ccp:auto-prazo-maximo-art87-a-2@v1

- leitor:a18: não tipável (nao_e_prazo_maximo): O prazo é um máximo de cinco dias, não um prazo para apresentar algo.
- leitor:b: não tipável (sem_vocabulario): Falta um campo para representar a condição de caducidade da adjudicação fundada nas situações indicadas.

## regra:ccp:auto-prazo-maximo-art90-1@v1

- leitor:a18: não tipável (nao_e_prazo_maximo): O prazo é da própria entidade adjudicante para prestar a caução, não um prazo máximo para o adjudicatário apresentar algo.
- leitor:b: {"tipo": "prazo_maximo", "condicoes": [], "params": {"maximum_days": 10, "deadline_field": "prazo_caucao_dias", "counted_from": "data_notificacao"}}

## regra:ccp:auto-prazo-maximo-art91-2@v1

- leitor:a18: não tipável (nao_e_prazo_maximo): O prazo é um máximo de cinco dias para a própria entidade adjudicante notificar o adjudicatário, não um prazo para os interessados apresentarem algo.
- leitor:b: não tipável (sem_vocabulario): O vocabulário não permite representar a condição de não prestação da caução pelo adjudicatário por facto que lhe seja imputável.

## regra:ccp:auto-prazo-maximo-art93-2@v1

- leitor:a18: não tipável (nao_e_prazo_maximo): O prazo é um máximo para o próprio órgão competente notificar o adjudicatário, não um prazo para os interessados apresentarem algo.
- leitor:b: não tipável (sem_vocabulario): Falta um campo que permita condicionar o prazo à não confirmação dos compromissos pelo adjudicatário no prazo fixado ou até ao termo da respetiva prorrogação.

## regra:ccp:auto-prazo-maximo-art95-v20080730@v1

- leitor:a18: não tipável (nao_e_prazo_maximo): O prazo é de 10 dias antes de decorrido o prazo de redução do contrato a escrito, não um prazo máximo para apresentar algo.
- leitor:b: não tipável (nao_e_prazo_maximo): O prazo máximo respeita ao fornecimento dos bens ou à prestação dos serviços, não à apresentação de elementos.
- verificador (B): não tipável: fonte em ccp:art95.1.c.i, que é vizinho (L1)

## regra:ccp:auto-prazo-maximo-art101@v1

- leitor:a18: não tipável (nao_e_prazo_maximo): O prazo é o da própria entidade adjudicante para notificar, não um prazo máximo para os interessados apresentarem algo.
- leitor:b: {"tipo": "prazo_maximo", "condicoes": [{"field": "tipo_procedimento", "op": "not_in", "value": ["ajuste_direto", "consulta_previa"]}], "params": {"maximum_days": 5, "deadline_field": "prazo_reclamacao_dias", "counted_from": "data_notificacao"}} || {"tipo": "prazo_maximo", "condicoes": [{"field": "tipo_procedimento", "op": "in", "value": ["ajuste_direto", "consulta_previa"]}], "params": {"maximum_days": 2, "deadline_field": "prazo_reclamacao_dias", "counted_from": "data_notificacao"}}
- verificador (B): regra 1: as fontes de maximum_days não dizem um máximo («não pode ser superior a», «no prazo de», L8); regra 2: as fontes de maximum_days não dizem um máximo («não pode ser superior a», «no prazo de», L8)

## regra:ccp:auto-prazo-maximo-art102-v20080730@v1

- leitor:a18: não tipável (nao_e_prazo_maximo): O prazo é do próprio órgão que aprova a minuta do contrato para notificar, não um prazo máximo para os interessados apresentarem algo.
- leitor:b: não tipável (nao_e_prazo_maximo): O prazo é para a própria entidade adjudicante notificar a decisão sobre a reclamação.
- verificador (B): não tipável: fonte em ccp:art102.2, que é vizinho (L1)

## regra:ccp:auto-prazo-minimo-art104-v20080730@v1

- leitor:a18: não tipável (nao_e_prazo_minimo): O prazo é da própria entidade adjudicante para outorgar o contrato, não um prazo mínimo para os interessados apresentarem algo.
- leitor:b: não tipável (nao_e_prazo_minimo): Os prazos regulam a outorga do contrato e a sua comunicação pela entidade adjudicante, não a apresentação de elementos.
- verificador (B): não tipável: fonte em ccp:art104.1, que é vizinho (L1); não tipável: fonte em ccp:art104.1.a, que é vizinho (L1); não tipável: fonte em ccp:art104.3, que é vizinho (L1)

## regra:ccp:auto-prazo-maximo-art115-1-j-v20180101@v1

- leitor:a18: não tipável (nao_e_prazo_maximo): O prazo é um máximo de cinco dias, não um prazo para apresentar algo.
- leitor:b: {"tipo": "prazo_maximo", "condicoes": [{"field": "tipo_procedimento", "op": "in", "value": ["ajuste_direto", "consulta_previa"]}], "params": {"maximum_days": 5, "deadline_field": "prazo_habilitacao_dias", "counted_from": "nao_indicado"}}

## regra:ccp:auto-prazo-maximo-art115-1-k@v1

- leitor:a18: não tipável (nao_e_prazo_maximo): O prazo é o máximo de apresentação dos documentos de habilitação pelo adjudicatário, não um prazo para os interessados apresentarem algo.
- leitor:b: {"tipo": "prazo_maximo", "condicoes": [{"field": "tipo_procedimento", "op": "in", "value": ["ajuste_direto", "consulta_previa"]}], "params": {"maximum_days": 5, "deadline_field": "prazo_habilitacao_dias", "counted_from": "nao_indicado"}}

## regra:ccp:auto-prazo-maximo-art122-v20180101@v1

- leitor:a18: não tipável (nao_e_prazo_maximo): O prazo é do próprio júri para elaborar o relatório preliminar, não um prazo máximo para os interessados apresentarem algo.
- leitor:b: não tipável (nao_e_prazo_maximo): O prazo destina-se à elaboração do relatório preliminar pelo júri, não à apresentação de elementos pelos interessados.
- verificador (B): não tipável: fonte em ccp:art122.1, que é vizinho (L1)

## regra:ccp:auto-prazo-minimo-art135-2-v20080730@v1

- leitor:a18: {"tipo": "prazo_minimo", "condicoes": [{"field": "publicado_joue", "op": "eq", "value": false}, {"field": "tipo_contrato", "op": "eq", "value": "obras"}, {"field": "tipo_procedimento", "op": "eq", "value": "concurso_publico"}], "params": {"minimum_days": 20, "deadline_field": "prazo_propostas_dias", "counted_from": "data_envio_anuncio", "usual_days": null}} || {"tipo": "prazo_minimo", "condicoes": [{"field": "publicado_joue", "op": "eq", "value": false}, {"field": "tipo_contrato", "op": "ne", "value": "obras"}, {"field": "tipo_procedimento", "op": "eq", "value": "concurso_publico"}], "params": {"minimum_days": 9, "deadline_field": "prazo_propostas_dias", "counted_from": "data_envio_anuncio", "usual_days": null}}
- leitor:b: não tipável (sem_vocabulario): Falta no vocabulário uma condição para a manifesta simplicidade dos trabalhos necessários à realização da obra.
- verificador (A): regra 1: counted_from data_envio_anuncio e as fontes dizem nada (L9); regra 2: counted_from data_envio_anuncio e as fontes dizem nada (L9)

## regra:ccp:auto-prazo-minimo-art136-1-v20080730@v1

- leitor:a18: {"tipo": "prazo_minimo", "condicoes": [{"field": "publicado_joue", "op": "eq", "value": true}, {"field": "tipo_procedimento", "op": "eq", "value": "concurso_publico"}], "params": {"minimum_days": 47, "deadline_field": "prazo_propostas_dias", "counted_from": "data_envio_anuncio", "usual_days": null}}
- leitor:b: {"tipo": "prazo_minimo", "condicoes": [{"field": "publicado_joue", "op": "eq", "value": true}, {"field": "tipo_procedimento", "op": "eq", "value": "concurso_publico"}], "params": {"minimum_days": 47, "deadline_field": "prazo_propostas_dias", "counted_from": "data_envio_anuncio", "usual_days": null}}
- verificador (A): regra 1, publicado_joue eq True: as fontes não afirmam o facto (L7)

## regra:ccp:auto-prazo-minimo-art136-3-v20080730@v1

- leitor:a18: não tipável (nao_e_prazo_minimo): O prazo é um máximo de redução dos prazos mínimos já fixados, não um prazo mínimo.
- leitor:b: não tipável (sem_vocabulario): O vocabulário não permite representar a condição de preparação e envio do anúncio por meios electrónicos conforme o formato e as modalidades de transmissão indicados.

## regra:ccp:auto-prazo-minimo-art136-4-v20080730@v1

- leitor:a18: não tipável (nao_e_prazo_minimo): O prazo é de 22 dias, e o n.º 3 prevê uma redução desse prazo em até sete dias. Não é um prazo mínimo absoluto.
- leitor:b: não tipável (sem_vocabulario): O vocabulário não permite representar a condição de preparação e envio do anúncio por meios electrónicos conforme o formato e as modalidades exigidos.

## regra:ccp:auto-prazo-maximo-art138-3@v1

- leitor:a18: não tipável (nao_e_prazo_maximo): O prazo é da própria entidade adjudicante para publicitar a lista dos concorrentes, não um prazo máximo para os interessados apresentarem algo.
- leitor:b: não tipável (sem_vocabulario): O vocabulário não prevê a condição de o interessado não ter sido incluído na lista dos concorrentes nem o início da contagem na publicitação dessa lista.

## regra:ccp:auto-limiar-art155-a@v1

- leitor:a18: {"tipo": "limiar", "condicoes": [{"field": "tipo_contrato", "op": "in", "value": ["bens", "servicos"]}, {"field": "tipo_procedimento", "op": "eq", "value": "concurso_publico"}], "params": {"threshold": {"field": "valor_estimado", "comparator": "le", "value": 300000, "currency": "EUR"}}} || {"tipo": "limiar", "condicoes": [{"field": "tipo_contrato", "op": "eq", "value": "obras"}, {"field": "tipo_procedimento", "op": "eq", "value": "concurso_publico"}], "params": {"threshold": {"field": "valor_estimado", "comparator": "le", "value": 300000, "currency": "EUR"}}}
- leitor:b: não tipável (texto_em_falta): Faltam os montantes dos limiares do artigo 474.º aplicáveis à locação ou aquisição de bens móveis e à aquisição de serviços.

## regra:ccp:auto-prazo-maximo-art161@v1

- leitor:a18: não tipável (nao_e_prazo_maximo): O prazo é da própria entidade adjudicante para exigir os documentos de habilitação, não um prazo máximo para os interessados apresentarem algo.
- leitor:b: {"tipo": "prazo_maximo", "condicoes": [{"field": "tipo_procedimento", "op": "eq", "value": "concurso_publico_urgente"}], "params": {"maximum_days": 2, "deadline_field": "prazo_habilitacao_dias", "counted_from": "data_notificacao"}}

## regra:ccp:auto-prazo-maximo-art161-b-4@v1

- leitor:a18: não tipável (nao_e_prazo_maximo): O prazo é de três dias para os contrainteressados se pronunciarem, não um prazo máximo para a entidade adjudicante decidir.
- leitor:b: não tipável (sem_vocabulario): O vocabulário não contém campos de prazo para apresentação de impugnações, pronúncia dos contrainteressados ou decisão de impugnações administrativas.

## regra:ccp:auto-prazo-minimo-art173@v1

- leitor:a18: {"tipo": "prazo_minimo", "condicoes": [{"field": "publicado_joue", "op": "eq", "value": false}, {"field": "tipo_procedimento", "op": "eq", "value": "concurso_limitado_previa_qualificacao"}], "params": {"minimum_days": 6, "deadline_field": "prazo_candidaturas_dias", "counted_from": "data_envio_anuncio", "usual_days": null}}
- leitor:b: {"tipo": "prazo_minimo", "condicoes": [{"field": "publicado_joue", "op": "eq", "value": false}, {"field": "tipo_procedimento", "op": "eq", "value": "concurso_limitado_previa_qualificacao"}], "params": {"minimum_days": 6, "deadline_field": "prazo_candidaturas_dias", "counted_from": "data_envio_anuncio", "usual_days": null}}
- verificador (A): regra 1: counted_from data_envio_anuncio e as fontes dizem nada (L9)

## regra:ccp:auto-prazo-minimo-art174-v20180101@v1

- leitor:a18: {"tipo": "prazo_minimo", "condicoes": [{"field": "publicado_joue", "op": "eq", "value": true}, {"field": "tipo_procedimento", "op": "eq", "value": "concurso_limitado_previa_qualificacao"}], "params": {"minimum_days": 30, "deadline_field": "prazo_candidaturas_dias", "counted_from": "data_envio_anuncio", "usual_days": null}} || {"tipo": "prazo_minimo", "condicoes": [{"field": "publicado_joue", "op": "eq", "value": true}, {"field": "setores_especiais", "op": "eq", "value": true}, {"field": "tipo_procedimento", "op": "eq", "value": "concurso_limitado_previa_qualificacao"}, {"field": "urgencia_fundamentada", "op": "eq", "value": true}], "params": {"minimum_days": 15, "deadline_field": "prazo_candidaturas_dias", "counted_from": "data_envio_anuncio", "usual_days": null}} || {"tipo": "prazo_minimo", "condicoes": [{"field": "publicado_joue", "op": "eq", "value": true}, {"field": "setores_especiais", "op": "eq", "value": true}], "params": {"minimum_days": 30, "deadline_field": "prazo_candidaturas_dias", "counted_from": "data_envio_anuncio", "usual_days": null}}
- leitor:b: {"tipo": "prazo_minimo", "condicoes": [{"field": "publicado_joue", "op": "eq", "value": true}, {"field": "tipo_procedimento", "op": "eq", "value": "concurso_limitado_previa_qualificacao"}], "params": {"minimum_days": 30, "deadline_field": "prazo_candidaturas_dias", "counted_from": "data_envio_anuncio", "usual_days": null}} || {"tipo": "prazo_minimo", "condicoes": [{"field": "publicado_joue", "op": "eq", "value": true}, {"field": "tipo_procedimento", "op": "eq", "value": "concurso_limitado_previa_qualificacao"}, {"field": "urgencia_fundamentada", "op": "eq", "value": true}], "params": {"minimum_days": 15, "deadline_field": "prazo_candidaturas_dias", "counted_from": "data_envio_anuncio", "usual_days": null}} || {"tipo": "prazo_minimo", "condicoes": [{"field": "publicado_joue", "op": "eq", "value": true}, {"field": "setores_especiais", "op": "eq", "value": true}, {"field": "tipo_procedimento", "op": "eq", "value": "concurso_limitado_previa_qualificacao"}], "params": {"minimum_days": 15, "deadline_field": "prazo_candidaturas_dias", "counted_from": "data_envio_anuncio", "usual_days": 30}}
- verificador (B): regra 1, tipo_procedimento eq concurso_limitado_previa_qualificacao: fonte em ccp:art174.1, que é vizinho (L1); regra 1, publicado_joue eq True: fonte em ccp:art174.1, que é vizinho (L1); regra 1, minimum_days: fonte em ccp:art174.1, que é vizinho (L1); regra 1, deadline_field: fonte em ccp:art174.1, que é vizinho (L1); regra 1, counted_from: fonte em ccp:art174.1, que é vizinho (L1); regra 2, tipo_procedimento eq concurso_limitado_previa_qualificacao: fonte em ccp:art174.1, que é vizinho (L1)

## regra:ccp:auto-prazo-minimo-art174-1-v20080730@v1

- leitor:a18: {"tipo": "prazo_minimo", "condicoes": [{"field": "publicado_joue", "op": "eq", "value": true}, {"field": "tipo_procedimento", "op": "eq", "value": "concurso_limitado_previa_qualificacao"}], "params": {"minimum_days": 37, "deadline_field": "prazo_candidaturas_dias", "counted_from": "data_envio_anuncio", "usual_days": null}} || {"tipo": "prazo_minimo", "condicoes": [{"field": "publicado_joue", "op": "eq", "value": true}, {"field": "tipo_contrato", "op": "eq", "value": "concessao_obras"}], "params": {"minimum_days": 52, "deadline_field": "prazo_candidaturas_dias", "counted_from": "data_envio_anuncio", "usual_days": null}}
- leitor:b: {"tipo": "prazo_minimo", "condicoes": [{"field": "publicado_joue", "op": "eq", "value": true}, {"field": "tipo_contrato", "op": "ne", "value": "concessao_obras"}, {"field": "tipo_procedimento", "op": "eq", "value": "concurso_limitado_previa_qualificacao"}], "params": {"minimum_days": 37, "deadline_field": "prazo_candidaturas_dias", "counted_from": "data_envio_anuncio", "usual_days": null}} || {"tipo": "prazo_minimo", "condicoes": [{"field": "publicado_joue", "op": "eq", "value": true}, {"field": "tipo_contrato", "op": "eq", "value": "concessao_obras"}, {"field": "tipo_procedimento", "op": "eq", "value": "concurso_limitado_previa_qualificacao"}], "params": {"minimum_days": 52, "deadline_field": "prazo_candidaturas_dias", "counted_from": "data_envio_anuncio", "usual_days": null}}
- verificador (A): regra 1, publicado_joue eq True: as fontes não afirmam o facto (L7); regra 2, publicado_joue eq True: as fontes não afirmam o facto (L7)

## regra:ccp:auto-prazo-minimo-art174-2-v20080730@v1

- leitor:a18: {"tipo": "prazo_minimo", "condicoes": [{"field": "anuncio_pre_informacao", "op": "eq", "value": true}, {"field": "tipo_procedimento", "op": "eq", "value": "concurso_limitado_previa_qualificacao"}], "params": {"minimum_days": 37, "deadline_field": "prazo_candidaturas_dias", "counted_from": "data_envio_convite", "usual_days": null}}
- leitor:b: {"tipo": "prazo_minimo", "condicoes": [{"field": "anuncio_pre_informacao", "op": "eq", "value": true}, {"field": "publicado_joue", "op": "eq", "value": true}, {"field": "tipo_procedimento", "op": "eq", "value": "concurso_limitado_previa_qualificacao"}], "params": {"minimum_days": 37, "deadline_field": "prazo_candidaturas_dias", "counted_from": "data_envio_convite", "usual_days": null}}
- verificador (A): regra 1: counted_from data_envio_convite e as fontes dizem nada (L9)

## regra:ccp:auto-prazo-minimo-art174-3-v20080730@v1

- leitor:a18: não tipável (nao_e_prazo_minimo): O prazo é um máximo de redução em sete dias, não um prazo mínimo.
- leitor:b: não tipável (sem_vocabulario): O vocabulário não permite representar a condição relativa à preparação e ao envio dos anúncios por meios electrónicos no formato e nas modalidades indicados no portal referido.

## regra:ccp:auto-prazo-minimo-art174-4@v1

- leitor:a18: não tipável (nao_e_prazo_minimo): O prazo é de cinco dias, e não um prazo mínimo para apresentar algo.
- leitor:b: não tipável (sem_vocabulario): O vocabulário não permite representar a condição de as peças procedimentais não poderem ser disponibilizadas sem restrições de acesso.

## regra:ccp:auto-prazo-maximo-art177-3@v1

- leitor:a18: não tipável (nao_e_prazo_maximo): O prazo é da própria entidade adjudicante para publicitar a lista dos candidatos, não um prazo máximo para os interessados apresentarem algo.
- leitor:b: não tipável (sem_vocabulario): O vocabulário não prevê a condição de o interessado não ter sido incluído na lista dos candidatos nem a contagem desde a publicitação dessa lista.

## regra:ccp:auto-prazo-minimo-art187-2-v20180101@v1

- leitor:a18: não tipável (nao_e_prazo_minimo): O prazo é de cinco dias para apresentar os documentos comprovativos, não um prazo mínimo para apresentar algo.
- leitor:b: não tipável (sem_vocabulario): O vocabulário não prevê um campo de prazo para apresentar documentos comprovativos dos requisitos de capacidade técnica e financeira nem para confirmar compromissos de terceiras entidades.

## regra:ccp:auto-prazo-maximo-art187-4-v20180101@v1

- leitor:a18: não tipável (nao_e_prazo_maximo): O prazo é de cinco dias, máximo para a própria entidade adjudicante notificar o candidato, e não um prazo para os candidatos apresentarem algo.
- leitor:b: não tipável (sem_vocabulario): O vocabulário não permite representar a ocorrência de um facto que determine a caducidade da qualificação.

## regra:ccp:auto-prazo-maximo-art188-4@v1

- leitor:a18: não tipável (nao_e_prazo_maximo): O prazo é um máximo de cinco dias, não um mínimo.
- leitor:b: não tipável (sem_vocabulario): O vocabulário não permite representar a ocorrência de um facto que determine a caducidade da qualificação.

## regra:ccp:auto-prazo-minimo-art190-2-v20080730@v1

- leitor:a18: {"tipo": "prazo_minimo", "condicoes": [{"field": "publicado_joue", "op": "eq", "value": false}, {"field": "tipo_contrato", "op": "eq", "value": "obras"}, {"field": "tipo_procedimento", "op": "eq", "value": "concurso_limitado_previa_qualificacao"}], "params": {"minimum_days": 8, "deadline_field": "prazo_propostas_dias", "counted_from": "data_envio_convite", "usual_days": null}} || {"tipo": "prazo_minimo", "condicoes": [{"field": "publicado_joue", "op": "eq", "value": false}, {"field": "tipo_contrato", "op": "ne", "value": "obras"}, {"field": "tipo_procedimento", "op": "eq", "value": "concurso_limitado_previa_qualificacao"}], "params": {"minimum_days": 21, "deadline_field": "prazo_propostas_dias", "counted_from": "data_envio_convite", "usual_days": null}}
- leitor:b: não tipável (sem_vocabulario): O vocabulário não permite representar a condição de manifesta simplicidade dos trabalhos necessários à realização da obra.
- verificador (A): regra 1: minimum_days 8 não está nas fontes (L8, L4); regra 2: minimum_days 21 não está nas fontes (L8, L4)

## regra:ccp:auto-prazo-minimo-art190-2@v1

- leitor:a18: {"tipo": "prazo_minimo", "condicoes": [{"field": "publicado_joue", "op": "eq", "value": false}, {"field": "tipo_contrato", "op": "eq", "value": "obras"}, {"field": "tipo_procedimento", "op": "eq", "value": "concurso_limitado_previa_qualificacao"}], "params": {"minimum_days": 6, "deadline_field": "prazo_propostas_dias", "counted_from": "data_envio_convite", "usual_days": null}} || {"tipo": "prazo_minimo", "condicoes": [{"field": "publicado_joue", "op": "eq", "value": false}, {"field": "tipo_contrato", "op": "ne", "value": "obras"}, {"field": "tipo_procedimento", "op": "eq", "value": "concurso_limitado_previa_qualificacao"}], "params": {"minimum_days": 6, "deadline_field": "prazo_propostas_dias", "counted_from": "data_envio_convite", "usual_days": null}}
- leitor:b: não tipável (sem_vocabulario): O vocabulário não permite representar a condição de manifesta simplicidade dos trabalhos necessários à realização da obra.

## regra:ccp:auto-prazo-minimo-art191-v20180101@v1

- leitor:a18: {"tipo": "prazo_minimo", "condicoes": [{"field": "publicado_joue", "op": "eq", "value": true}, {"field": "tipo_procedimento", "op": "eq", "value": "concurso_limitado_previa_qualificacao"}], "params": {"minimum_days": 25, "deadline_field": "prazo_propostas_dias", "counted_from": "data_envio_convite", "usual_days": null}} || {"tipo": "prazo_minimo", "condicoes": [{"field": "anuncio_pre_informacao", "op": "eq", "value": true}, {"field": "publicado_joue", "op": "eq", "value": true}, {"field": "setores_especiais", "op": "eq", "value": true}, {"field": "tipo_procedimento", "op": "eq", "value": "concurso_limitado_previa_qualificacao"}], "params": {"minimum_days": 10, "deadline_field": "prazo_propostas_dias", "counted_from": "data_envio_convite", "usual_days": null}} || {"tipo": "prazo_minimo", "condicoes": [{"field": "setores_especiais", "op": "eq", "value": true}, {"field": "tipo_procedimento", "op": "eq", "value": "concurso_limitado_previa_qualificacao"}], "params": {"minimum_days": 10, "deadline_field": "prazo_propostas_dias", "counted_from": "data_envio_convite", "usual_days": null}}
- leitor:b: não tipável (sem_vocabulario): O vocabulário não permite representar as condições de cobertura das prestações, antecedência e conteúdo do anúncio de pré-informação necessárias à redução para 10 dias.
- verificador (B): não tipável: fonte em ccp:art191.2, que é vizinho (L1); não tipável: fonte em ccp:art191.2.a, que é vizinho (L1); não tipável: fonte em ccp:art191.2.b, que é vizinho (L1)

## regra:ccp:auto-prazo-maximo-art192-3@v1

- leitor:a18: não tipável (nao_e_prazo_maximo): O prazo é o de manifestação de concordância dos candidatos, não um prazo máximo para os interessados apresentarem algo.
- leitor:b: não tipável (sem_vocabulario): O vocabulário não prevê a recepção do convite como início da contagem do prazo para manifestar discordância.

## regra:ccp:auto-prazo-maximo-art192-4@v1

- leitor:a18: não tipável (nao_e_prazo_maximo): O prazo é de 15 dias, só para os candidatos que manifestem discordância, e não um prazo máximo para todos os candidatos apresentarem propostas.
- leitor:b: não tipável (sem_vocabulario): O vocabulário não permite representar a condição de algum candidato qualificado manifestar por escrito discordância sobre o prazo fixado.

## regra:ccp:auto-prazo-minimo-art198-1-v20080730@v1

- leitor:a18: {"tipo": "prazo_minimo", "condicoes": [{"field": "tipo_procedimento", "op": "eq", "value": "procedimento_negociacao"}], "params": {"minimum_days": 37, "deadline_field": "prazo_candidaturas_dias", "counted_from": "data_envio_anuncio", "usual_days": null}}
- leitor:b: {"tipo": "prazo_minimo", "condicoes": [{"field": "publicado_joue", "op": "eq", "value": true}, {"field": "tipo_procedimento", "op": "eq", "value": "procedimento_negociacao"}], "params": {"minimum_days": 37, "deadline_field": "prazo_candidaturas_dias", "counted_from": "data_envio_anuncio", "usual_days": null}}
- verificador (B): regra 1, publicado_joue eq True: as fontes não afirmam o facto (L7)

## regra:ccp:auto-prazo-minimo-art218-v20080730@v1

- leitor:a18: {"tipo": "prazo_minimo", "condicoes": [{"field": "tipo_procedimento", "op": "eq", "value": "dialogo_concorrencial"}], "params": {"minimum_days": 40, "deadline_field": "prazo_propostas_dias", "counted_from": "data_envio_convite", "usual_days": null}}
- leitor:b: {"tipo": "prazo_minimo", "condicoes": [{"field": "tipo_procedimento", "op": "eq", "value": "dialogo_concorrencial"}], "params": {"minimum_days": 40, "deadline_field": "prazo_propostas_dias", "counted_from": "data_envio_convite", "usual_days": null}}
- verificador (B): regra 1, tipo_procedimento eq dialogo_concorrencial: «diálogo concorrencial» não está em ccp:art218; regra 1, tipo_procedimento eq dialogo_concorrencial: as fontes não nomeiam ['dialogo_concorrencial']

## regra:ccp:auto-prazo-maximo-art219-i-5@v1

- leitor:a18: não tipável (nao_e_prazo_maximo): O prazo é da própria entidade adjudicante para notificar os concorrentes, não um prazo máximo para os concorrentes apresentarem algo.
- leitor:b: não tipável (sem_vocabulario): Falta um campo para representar a condição de os termos de referência exigirem aos concorrentes habilitações profissionais específicas.

## regra:ccp:auto-prazo-maximo-art234-1-v20080730@v1

- leitor:a18: não tipável (nao_e_prazo_minimo): O prazo é da própria entidade adjudicante para selecionar os concorrentes, não um prazo para os concorrentes apresentarem algo.
- leitor:b: não tipável (sem_vocabulario): Falta no vocabulário uma condição que represente a exigência de habilitações profissionais específicas pelos termos de referência.

## regra:ccp:auto-prazo-maximo-art241-3-v20080730@v1

- leitor:a18: não tipável (sem_vocabulario): A regra é de um sistema de aquisição dinâmico, instrumento que o vocabulário não tem.
- leitor:b: não tipável (nao_e_prazo_maximo): O prazo destina-se à entidade adjudicante para notificar a aceitação ou rejeição, não à apresentação de algo.

## regra:ccp:auto-prazo-maximo-art241-a-3@v1

- leitor:a18: não tipável (sem_vocabulario): A regra é de um sistema de aquisição dinâmico, instrumento que o vocabulário não tem.
- leitor:b: não tipável (nao_e_prazo_maximo): O prazo é para a própria entidade adjudicante analisar as candidaturas.

## regra:ccp:auto-prazo-minimo-art242-3-v20080730@v1

- leitor:a18: não tipável (sem_vocabulario): A regra é de um sistema de aquisição dinâmico, instrumento que o vocabulário não tem.
- leitor:b: não tipável (nao_e_prazo_minimo): O prazo regula a publicação do anúncio simplificado pela entidade adjudicante, não a apresentação de elementos pelos interessados.

## regra:ccp:auto-prazo-maximo-art270@v1

- leitor:a18: não tipável (nao_e_prazo_minimo): O prazo é de cinco dias, não um máximo.
- leitor:b: não tipável (sem_vocabulario): O vocabulário não contém um campo de prazo para a apresentação de impugnações administrativas.

## regra:ccp:auto-prazo-maximo-art273@v1

- leitor:a18: não tipável (nao_e_prazo_maximo): O prazo é do próprio órgão competente para notificar, não um prazo máximo para os interessados apresentarem algo.
- leitor:b: não tipável (sem_vocabulario): Falta vocabulário para representar a condição relativa ao objeto da impugnação administrativa.

## regra:ccp:auto-prazo-minimo-art276-v20120811@v1

- leitor:a18: não tipável (nao_e_prazo_minimo): O prazo é de 37 dias, e não um mínimo para a entidade adjudicante.
- leitor:b: não tipável (sem_vocabulario): O vocabulário não permite representar a condição de o contrato ser celebrado por um concessionário de obras públicas que não seja entidade adjudicante.

## regra:ccp:auto-prazo-minimo-art276-v20180101@v1

- leitor:a18: não tipável (nao_e_prazo_minimo): O prazo é de 37 dias, e não um mínimo para a entidade adjudicante.
- leitor:b: não tipável (sem_vocabulario): O vocabulário não permite representar a condição de o contratante ser um concessionário de obras públicas que não seja entidade adjudicante.

## regra:ccp:auto-prazo-minimo-art276-v20210620@v1

- leitor:a18: não tipável (nao_e_prazo_minimo): O prazo é de publicitação do contrato no Diário da República, não um prazo para apresentar algo.
- leitor:b: não tipável (sem_vocabulario): O vocabulário não permite representar a condição de os contratos serem celebrados por concessionários de obras públicas que não sejam entidades adjudicantes.

## regra:ccp:auto-prazo-minimo-art276-5-v20080730@v1

- leitor:a18: não tipável (nao_e_prazo_minimo): O prazo é um mínimo para o concessionário não fixar, não um prazo para os interessados apresentarem algo.
- leitor:b: não tipável (sem_vocabulario): O vocabulário não permite limitar a regra aos concessionários de obras públicas que não sejam entidades adjudicantes.

## regra:ccp:auto-prazo-maximo-art283-a-v20110113@v1

- leitor:a18: não tipável (nao_e_prazo_maximo): O prazo é de anulação do contrato, não um prazo para apresentar algo.
- leitor:b: não tipável (nao_e_prazo_maximo): Os prazos respeitam à outorga do contrato, não à apresentação de elementos, pelo que não existe um prazo máximo tipável.
- verificador (B): não tipável: fonte em ccp:art283-a.2.c, que é vizinho (L1)

## regra:ccp:auto-prazo-maximo-art283-a-v20210620@v1

- leitor:a18: não tipável (nao_e_prazo_maximo): O prazo é de 10 dias antes de outorga do contrato, não um prazo para apresentar algo.
- leitor:b: não tipável (nao_e_prazo_maximo): A passagem estabelece um prazo de suspensão da outorga do contrato, não um prazo máximo para apresentar algo.
- verificador (B): não tipável: fonte em ccp:art283-a.2.c, que é vizinho (L1)

## regra:ccp:auto-prazo-minimo-art295-v20091007@v1

- leitor:a18: não tipável (nao_e_prazo_minimo): O prazo é de 30 dias para o próprio contraente público promover a liberação da caução, não um prazo mínimo para os interessados apresentarem algo.
- leitor:b: não tipável (nao_e_prazo_minimo): Os prazos regulam a liberação da caução pelo contraente público, não um prazo mínimo para apresentar algo.
- verificador (B): não tipável: fonte em ccp:art295.3, que é vizinho (L1)

## regra:ccp:auto-prazo-maximo-art315-v20210620@v1

- leitor:a18: não tipável (nao_e_prazo_maximo): O prazo é da própria entidade adjudicante para publicitar as modificações, não um prazo máximo para os interessados apresentarem algo.
- leitor:b: não tipável (nao_e_prazo_maximo): Os prazos respeitam à publicitação das modificações pelo contraente público e à manutenção dessa publicidade.
- verificador (B): não tipável: fonte em ccp:art315.1, que é vizinho (L1)

## regra:ccp:auto-prazo-minimo-art327-v20080730@v1

- leitor:a18: não tipável (nao_e_prazo_minimo): O prazo é de 15 dias antes de invocar a exceção, não um prazo para apresentar algo.
- leitor:b: não tipável (nao_e_prazo_minimo): O prazo é uma antecedência de notificação para exercer o direito de recusar o cumprimento, não um prazo para apresentar algo previsto no vocabulário.
- verificador (B): não tipável: fonte em ccp:art327.3, que é vizinho (L1)

## regra:ccp:auto-prazo-maximo-art345-3@v1

- leitor:a18: não tipável (nao_e_prazo_maximo): O prazo é da própria entidade adjudicante para apresentar as reclamações ou reservas, não um prazo máximo para o empreiteiro apresentar algo.
- leitor:b: {"tipo": "prazo_maximo", "condicoes": [{"field": "tipo_contrato", "op": "eq", "value": "obras"}], "params": {"maximum_days": 10, "deadline_field": "prazo_reclamacao_dias", "counted_from": "data_notificacao"}}
- verificador (B): regra 1: as fontes de maximum_days não dizem um máximo («não pode ser superior a», «no prazo de», L8)

## regra:ccp:auto-prazo-maximo-art345-4@v1

- leitor:a18: não tipável (nao_e_prazo_maximo): O prazo é do próprio empreiteiro para apresentar uma exposição fundamentada, não um prazo máximo para a entidade adjudicante.
- leitor:b: não tipável (sem_vocabulario): O vocabulário não permite representar a condição de as reclamações ou reservas terem sido exaradas no próprio auto e limitadas ao enunciado genérico do respetivo objeto.

## regra:ccp:auto-prazo-maximo-art354-v20080730@v1

- leitor:a18: não tipável (nao_e_prazo_maximo): O prazo é o da caducidade do direito, não um prazo para apresentar algo.
- leitor:b: não tipável (sem_vocabulario): O vocabulário de counted_from não contempla o evento constitutivo do direito nem o momento em que o empreiteiro dele tome conhecimento.
- verificador (B): não tipável: fonte em ccp:art354.2, que é vizinho (L1)

## regra:ccp:auto-prazo-maximo-art354-2@v1

- leitor:a18: não tipável (nao_e_prazo_maximo): O prazo é o da caducidade do direito, não um prazo para a entidade adjudicante decidir.
- leitor:b: não tipável (sem_vocabulario): O vocabulário não prevê o início da contagem no evento constitutivo do direito ou no momento em que o empreiteiro dele tome conhecimento.

## regra:ccp:auto-prazo-maximo-art372-1-v20080730@v1

- leitor:a18: não tipável (nao_e_prazo_maximo): O prazo é do próprio empreiteiro para reclamar, não um prazo máximo para o dono da obra.
- leitor:b: não tipável (sem_vocabulario): O vocabulário não prevê como início da contagem a recepção da ordem do dono da obra de execução dos trabalhos a mais.

## regra:ccp:auto-prazo-maximo-art372-1-v20180101@v1

- leitor:a18: não tipável (nao_e_prazo_maximo): O prazo é da própria entidade adjudicante para fundamentar a reclamação do empreiteiro, não um prazo máximo para o empreiteiro apresentar algo.
- leitor:b: não tipável (sem_vocabulario): O vocabulário não prevê como início da contagem a receção da ordem do dono da obra de execução dos trabalhos complementares.

## regra:ccp:auto-prazo-maximo-art372-1-v20210620@v1

- leitor:a18: não tipável (nao_e_prazo_maximo): O prazo é do próprio empreiteiro para reclamar, não um prazo máximo para o dono da obra.
- leitor:b: não tipável (sem_vocabulario): O vocabulário não permite representar os pressupostos da reclamação nem o início da contagem na receção da ordem de execução dos trabalhos complementares.

## regra:ccp:auto-prazo-maximo-art372-1@v1

- leitor:a18: não tipável (nao_e_prazo_maximo): O prazo é do próprio empreiteiro para reclamar, não um prazo máximo para a entidade adjudicante.
- leitor:b: não tipável (sem_vocabulario): O vocabulário não permite representar os pressupostos específicos da reclamação nem o início da contagem na receção da ordem de execução dos trabalhos complementares.

## regra:ccp:auto-prazo-maximo-art373-v20210620@v1

- leitor:a18: não tipável (nao_e_prazo_maximo): O prazo é do próprio empreiteiro para apresentar uma proposta, não um prazo máximo para o dono da obra se pronunciar.
- leitor:b: não tipável (sem_vocabulario): O vocabulário não permite representar as condições relativas à espécie e à execução dos trabalhos nem o início da contagem na receção do pedido de apresentação da proposta.
- verificador (B): não tipável: fonte em ccp:art373.2, que é vizinho (L1); não tipável: fonte em ccp:art373.1.b, que é vizinho (L1); não tipável: fonte em ccp:art373.2, que é vizinho (L1)

## regra:ccp:auto-prazo-maximo-art373-2-v20080730@v1

- leitor:a18: não tipável (nao_e_prazo_maximo): O prazo é do próprio empreiteiro para apresentar uma proposta, não um prazo máximo para o dono da obra se pronunciar.
- leitor:b: não tipável (sem_vocabulario): O vocabulário não permite representar a falta de estipulação contratual nem as condições relativas à espécie dos trabalhos e às condições da sua execução.

## regra:ccp:auto-prazo-maximo-art373-2-v20091007@v1

- leitor:a18: não tipável (nao_e_prazo_maximo): O prazo é do próprio empreiteiro para apresentar uma proposta, não um prazo máximo para o dono da obra se pronunciar.
- leitor:b: não tipável (sem_vocabulario): O vocabulário não permite representar as condições relativas à estipulação contratual e à espécie e condições de execução dos trabalhos, nem o início da contagem na recepção da ordem de execução.

## regra:ccp:auto-prazo-maximo-art373-2@v1

- leitor:a18: não tipável (nao_e_prazo_maximo): O prazo é do próprio empreiteiro para apresentar uma proposta, não um prazo máximo para o dono da obra.
- leitor:b: não tipável (sem_vocabulario): O vocabulário não permite representar a falta de estipulação contratual, as condições relativas à espécie e execução dos trabalhos nem a contagem desde a receção do pedido.

## regra:ccp:auto-prazo-maximo-art373-3@v1

- leitor:a18: não tipável (nao_e_prazo_maximo): O prazo é do próprio empreiteiro para apresentar uma proposta, não um prazo máximo para o dono da obra se pronunciar.
- leitor:b: não tipável (sem_vocabulario): O vocabulário não permite limitar a regra aos contratos de empreitada de conceção-construção.

## regra:ccp:auto-prazo-maximo-art378-3-v20180101@v1

- leitor:a18: não tipável (nao_e_prazo_maximo): O prazo é do próprio empreiteiro para reclamar, não um prazo máximo para os interessados apresentarem algo.
- leitor:b: não tipável (sem_vocabulario): O vocabulário não prevê a consignação como início da contagem nem a exclusão dos erros ou omissões só detetáveis durante a execução da obra.

## regra:ccp:auto-prazo-maximo-art378-4@v1

- leitor:a18: não tipável (nao_e_prazo_maximo): O prazo é da própria entidade adjudicante para reclamar, não um prazo máximo para os interessados apresentarem algo.
- leitor:b: não tipável (sem_vocabulario): O vocabulário não prevê este início da contagem nem a condição de os erros ou omissões serem só detetáveis nesse momento.

## regra:ccp:auto-prazo-maximo-art385-v20230715@v1

- leitor:a18: não tipável (nao_e_prazo_maximo): O prazo é do próprio empreiteiro para comunicar, não um prazo máximo para os interessados apresentarem algo.
- leitor:b: não tipável (nao_e_prazo_maximo): O prazo destina-se à comunicação da celebração de uma subempreitada ao dono da obra, e não a uma apresentação prevista no vocabulário.
- verificador (B): não tipável: fonte em ccp:art385.3, que é vizinho (L1)

## regra:ccp:auto-prazo-maximo-art401-1@v1

- leitor:a18: não tipável (nao_e_prazo_maximo): O prazo é da própria entidade adjudicante para enviar a conta final, não um prazo máximo para o empreiteiro apresentar algo.
- leitor:b: {"tipo": "prazo_maximo", "condicoes": [{"field": "tipo_contrato", "op": "eq", "value": "obras"}], "params": {"maximum_days": 15, "deadline_field": "prazo_reclamacao_dias", "counted_from": "nao_indicado"}}

## regra:ccp:auto-prazo-maximo-art404-1@v1

- leitor:a18: não tipável (nao_e_prazo_maximo): O prazo é do próprio dono da obra para notificar o empreiteiro, não um prazo máximo para o empreiteiro apresentar algo.
- leitor:b: não tipável (sem_vocabulario): O vocabulário não contém um campo de prazo para a apresentação de um plano de trabalhos modificado.

## regra:ccp:auto-prazo-maximo-art405-v20080730@v1

- leitor:a18: não tipável (nao_e_prazo_maximo): O prazo é o da própria entidade adjudicante para informar a Inspecção-Geral das Obras Públicas, Transportes e Comunicações e o Instituto da Construção e do Imobiliário, I. P.; não é um prazo máximo para os interessados apresentarem algo.
- leitor:b: não tipável (nao_e_prazo_maximo): A passagem fixa fundamentos de resolução do contrato, não um prazo máximo para apresentar algo.
- verificador (B): não tipável: fonte em ccp:art405.1, que é vizinho (L1); não tipável: fonte em ccp:art405.1.d, que é vizinho (L1)

## regra:ccp:auto-prazo-maximo-art405-v20210620@v1

- leitor:a18: não tipável (nao_e_prazo_maximo): O prazo é o da própria entidade adjudicante para informar a Inspecção-Geral das Obras Públicas, Transportes e Comunicações e o Instituto da Construção e do Imobiliário, I. P.; não é um prazo máximo para os interessados apresentarem algo.
- leitor:b: não tipável (nao_e_prazo_maximo): O prazo refere-se ao início da execução dos trabalhos, não à apresentação de elementos.
- verificador (B): não tipável: fonte em ccp:art405.1.d, que é vizinho (L1)

## regra:ccp:auto-prazo-maximo-art464-a-v20210620@v1

- leitor:a18: não tipável (nao_e_prazo_maximo): O prazo é o de aplicação da sanção, não um prazo para os interessados apresentarem algo.
- leitor:b: não tipável (nao_e_prazo_maximo): Os prazos fixam a duração de uma sanção e uma obrigação de comunicação dos contraentes públicos, não um prazo máximo para apresentação de elementos pelos participantes.
- verificador (B): não tipável: fonte em ccp:art464-a.1, que é vizinho (L1); não tipável: fonte em ccp:art464-a.2, que é vizinho (L1)

## regra:ccp:auto-prazo-maximo-art464-e-2@v1

- leitor:a18: não tipável (nao_e_prazo_maximo): O prazo é da própria parte requerida para responder, não um prazo máximo para a comissão fazer algo.
- leitor:b: não tipável (sem_vocabulario): O vocabulário não contém um campo de prazo para apresentar resposta e indicar um membro para a comissão.

## regra:eu-1989-665:auto-prazo-minimo-art2-a-2@v1

- leitor:a18: não tipável (nao_e_prazo_minimo): O prazo é de 10 dias antes de celebrar um contrato, não um prazo para apresentar algo.
- leitor:b: não tipável (nao_e_prazo_minimo): O prazo suspende a celebração do contrato; não é um prazo para apresentar nada.

## regra:eu-1989-665:auto-prazo-minimo-art2-c@v1

- leitor:a18: não tipável (sem_vocabulario): O prazo é fixado em dias consecutivos, unidade que o vocabulário não tem.
- leitor:b: não tipável (sem_vocabulario): O vocabulário não contém um campo de prazo para a interposição de recurso.
- verificador (B): não tipável: «Prazos para interposição de recurso» não está em eu-1989-665:art2-c

## regra:eu-1992-13:auto-prazo-minimo-art2-c@v1

- leitor:a18: não tipável (sem_vocabulario): O prazo é fixado em dias consecutivos, unidade que o vocabulário não tem.
- leitor:b: não tipável (sem_vocabulario): O vocabulário não prevê um campo de prazo para a interposição de recurso.
- verificador (B): não tipável: «Prazos para interposição de recurso» não está em eu-1992-13:art2-c

## regra:eu-2004-17:auto-prazo-maximo-art15-4-v20041101@v1

- leitor:a18: não tipável (sem_vocabulario): A regra é de um sistema de aquisição dinâmico, instrumento que o vocabulário não tem.
- leitor:b: não tipável (nao_e_prazo_maximo): O prazo é para a entidade adjudicante concluir a avaliação, não para apresentar algo.

## regra:eu-2004-17:auto-prazo-minimo-art45-3-a-v20041101@v1

- leitor:a18: {"tipo": "prazo_minimo", "condicoes": [{"field": "tipo_procedimento", "op": "in", "value": ["concurso_limitado_previa_qualificacao", "procedimento_negociacao_com_concurso"]}], "params": {"minimum_days": 37, "deadline_field": "prazo_reclamacao_dias", "counted_from": "data_envio_anuncio", "usual_days": null}}
- leitor:b: não tipável (sem_vocabulario): O vocabulário não permite distinguir o envio do anúncio por meios electrónicos ou fax do envio por outros meios, condição que determina os mínimos de 15 ou 22 dias.
- verificador (A): regra 1, tipo_procedimento in ['concurso_limitado_previa_qualificacao', 'procedimento_negociacao_com_concurso']: as fontes não nomeiam ['procedimento_negociacao_com_concurso']; regra 1: deadline_field prazo_reclamacao_dias e as fontes dizem ['prazo_candidaturas_dias'] (L9); regra 1: counted_from data_envio_anuncio e as fontes dizem nada (L9)

## regra:eu-2004-17:auto-prazo-minimo-art45-3-c-v20041101@v1

- leitor:a18: {"tipo": "prazo_minimo", "condicoes": [{"field": "tipo_procedimento", "op": "in", "value": ["concurso_limitado_previa_qualificacao", "procedimento_negociacao_com_concurso"]}], "params": {"minimum_days": 24, "deadline_field": "prazo_reclamacao_dias", "counted_from": "data_envio_convite", "usual_days": null}}
- leitor:b: não tipável (sem_vocabulario): Falta um campo que represente a impossibilidade de acordo sobre o prazo de recepção das propostas.
- verificador (A): regra 1, tipo_procedimento in ['concurso_limitado_previa_qualificacao', 'procedimento_negociacao_com_concurso']: as fontes não nomeiam ['procedimento_negociacao_com_concurso']; regra 1: minimum_days 24 não está nas fontes (L8, L4); regra 1: deadline_field prazo_reclamacao_dias e as fontes dizem ['prazo_propostas_dias'] (L9); regra 1: counted_from data_envio_convite e as fontes dizem nada (L9)

## regra:eu-2004-17:auto-prazo-minimo-art45-4-v20041101@v1

- leitor:a18: {"tipo": "prazo_minimo", "condicoes": [{"field": "anuncio_pre_informacao", "op": "eq", "value": true}, {"field": "tipo_procedimento", "op": "eq", "value": "concurso_publico"}], "params": {"minimum_days": 36, "deadline_field": "prazo_propostas_dias", "counted_from": "data_envio_anuncio", "usual_days": null}}
- leitor:b: não tipável (sem_vocabulario): O vocabulário não permite representar a condição de antecedência do envio do anúncio periódico indicativo relativamente ao envio do anúncio de concurso.

## regra:eu-2004-17:auto-prazo-maximo-art45-5-v20041101@v1

- leitor:a18: não tipável (nao_e_prazo_maximo): O número reduz os prazos em sete dias; não é um prazo máximo.
- leitor:b: não tipável (nao_e_prazo_maximo): A passagem permite uma redução dos prazos, mas não fixa um prazo máximo.

## regra:eu-2004-17:auto-prazo-minimo-art45-7-v20041101@v1

- leitor:a18: não tipável (nao_e_prazo_minimo): O prazo é um máximo: não pode ser inferior a 15 dias.
- leitor:b: não tipável (sem_vocabulario): Falta um campo para distinguir o envio do anúncio por fax ou por meios electrónicos do envio por outros meios, necessário para separar os mínimos de 15 e 22 dias.

## regra:eu-2004-17:auto-prazo-minimo-art45-8-v20041101@v1

- leitor:a18: não tipável (nao_e_prazo_minimo): O prazo é um máximo para a recepção de pedidos de participação, não um mínimo.
- leitor:b: não tipável (sem_vocabulario): O vocabulário não permite representar a acumulação das reduções nem a exceção dos prazos fixados de comum acordo.

## regra:eu-2004-18:auto-limiar-art9-4-a-v20040430@v1

- leitor:a18: não tipável (nao_e_limiar): O valor é a soma de vários contratos; não é o limite até ao qual um procedimento pode ser escolhido.
- leitor:b: não tipável (nao_e_limiar): Os valores delimitam uma derrogação à aplicação da diretiva a lotes, sem fixarem um limite para a escolha de um procedimento.

## regra:eu-2004-18:auto-limiar-art9-4-b-v20040430@v1

- leitor:a18: não tipável (nao_e_limiar): O valor é somado sobre vários lotes para aplicar o artigo 7.º; não é o limite até ao qual um lote pode ser adjudicado.
- leitor:b: não tipável (nao_e_limiar): O valor permite derrogar a aplicação da diretiva a certos lotes; não fixa um limite até ao qual um procedimento pode ser escolhido.

## regra:eu-2004-18:auto-limiar-art9-5-b-v20041101@v1

- leitor:a18: não tipável (nao_e_limiar): O valor cumulado dos lotes é somado para aplicar o artigo 7.º; não é o limite até ao qual um procedimento pode ser escolhido.
- leitor:b: não tipável (nao_e_limiar): O valor permite derrogar a aplicação da diretiva a certos lotes; não é um limite até ao qual um procedimento pode ser escolhido.

## regra:eu-2004-18:auto-prazo-maximo-art33-4-v20040430@v1

- leitor:a18: não tipável (sem_vocabulario): A regra é de um sistema de aquisição dinâmico, instrumento que o vocabulário não tem.
- leitor:b: não tipável (nao_e_prazo_maximo): O prazo é para a própria entidade adjudicante concluir a avaliação, não para apresentar elementos.

## regra:eu-2004-18:auto-limiar-art35-1-a-v20040430@v1

- leitor:a18: não tipável (nao_e_limiar): O valor delimita os contratos que estão sujeitos à publicitação no perfil de adquirente; não é o limite até ao qual um procedimento pode ser escolhido.
- leitor:b: não tipável (nao_e_limiar): O valor agrega vários contratos ou acordos-quadro para efeitos de pré-informação; não limita a escolha de um procedimento.

## regra:eu-2004-18:auto-prazo-minimo-art38-3-a-v20040430@v1

- leitor:a18: {"tipo": "prazo_minimo", "condicoes": [{"field": "tipo_procedimento", "op": "eq", "value": "concurso_limitado_previa_qualificacao"}], "params": {"minimum_days": 37, "deadline_field": "prazo_reclamacao_dias", "counted_from": "data_envio_anuncio", "usual_days": null}}
- leitor:b: {"tipo": "prazo_minimo", "condicoes": [{"field": "tipo_procedimento", "op": "in", "value": ["concurso_limitado_previa_qualificacao", "dialogo_concorrencial", "procedimento_negociacao_com_concurso"]}], "params": {"minimum_days": 37, "deadline_field": "prazo_candidaturas_dias", "counted_from": "data_envio_anuncio", "usual_days": null}}
- verificador (A): regra 1: deadline_field prazo_reclamacao_dias e as fontes dizem ['prazo_candidaturas_dias'] (L9)

## regra:eu-2004-18:auto-prazo-minimo-art38-4-v20040430@v1

- leitor:a18: não tipável (nao_e_prazo_minimo): O prazo é um máximo que pode ser reduzido em sete dias, não um prazo mínimo.
- leitor:b: não tipável (sem_vocabulario): O vocabulário não permite representar as condições relativas ao conteúdo do anúncio de pré-informação e ao intervalo entre o seu envio e o envio do anúncio de concurso.

## regra:eu-2004-18:auto-prazo-maximo-art38-5-v20040430@v1

- leitor:a18: não tipável (nao_e_prazo_maximo): O prazo é um máximo que pode ser reduzido em sete dias, não um prazo máximo absoluto.
- leitor:b: não tipável (nao_e_prazo_maximo): A passagem reduz prazos mínimos de recepção de propostas e de pedidos de participação; não fixa um prazo máximo.

## regra:eu-2004-18:auto-prazo-minimo-art38-8-a-v20040430@v1

- leitor:a18: {"tipo": "prazo_minimo", "condicoes": [{"field": "publicado_joue", "op": "eq", "value": true}, {"field": "tipo_procedimento", "op": "in", "value": ["procedimento_concorrencial_negociacao", "procedimento_negociacao"]}, {"field": "urgencia_fundamentada", "op": "eq", "value": false}], "params": {"minimum_days": 15, "deadline_field": "prazo_reclamacao_dias", "counted_from": "data_envio_anuncio", "usual_days": null}} || {"tipo": "prazo_minimo", "condicoes": [{"field": "publicado_joue", "op": "eq", "value": false}, {"field": "tipo_procedimento", "op": "in", "value": ["procedimento_concorrencial_negociacao", "procedimento_negociacao"]}, {"field": "urgencia_fundamentada", "op": "eq", "value": false}], "params": {"minimum_days": 10, "deadline_field": "prazo_reclamacao_dias", "counted_from": "data_envio_anuncio", "usual_days": null}}
- leitor:b: não tipável (sem_vocabulario): O vocabulário não permite representar o envio electrónico do anúncio nas condições indicadas, necessário para distinguir os mínimos de quinze e dez dias.
- verificador (A): regra 1, tipo_procedimento in ['procedimento_negociacao', 'procedimento_concorrencial_negociacao']: as fontes não nomeiam ['procedimento_concorrencial_negociacao', 'procedimento_negociacao']; regra 1, publicado_joue eq True: as fontes não afirmam o facto (L7); regra 1, urgencia_fundamentada eq False: as fontes não negam o facto (L7); regra 1: deadline_field prazo_reclamacao_dias e as fontes dizem ['prazo_candidaturas_dias'] (L9); regra 2, tipo_procedimento in ['procedimento_negociacao', 'procedimento_concorrencial_negociacao']: as fontes não nomeiam ['procedimento_concorrencial_negociacao', 'procedimento_negociacao']; regra 2, publicado_joue eq False: as fontes não negam o facto (L7)

## regra:eu-2004-18:auto-prazo-minimo-art38-8-b-v20040430@v1

- leitor:a18: não tipável (nao_e_prazo_minimo): O prazo é um mínimo para as entidades adjudicantes poderem fixar outro prazo, não um prazo para os interessados apresentarem algo.
- leitor:b: não tipável (sem_vocabulario): Falta um campo que represente a urgência tornar impraticáveis os prazos mínimos, condição distinta de urgencia_fundamentada.

## regra:eu-2004-18:auto-prazo-minimo-art59-v20040430@v1

- leitor:a18: {"tipo": "prazo_minimo", "condicoes": [{"field": "tipo_contrato", "op": "eq", "value": "concessao_obras"}], "params": {"minimum_days": 52, "deadline_field": "prazo_candidaturas_dias", "counted_from": "data_envio_anuncio", "usual_days": null}}
- leitor:b: não tipável (sem_vocabulario): Falta no vocabulário a condição de os anúncios serem preparados e enviados por meios electrónicos, da qual depende a redução do prazo.

## regra:eu-2004-18:auto-prazo-minimo-art65-v20040430@v1

- leitor:a18: {"tipo": "prazo_minimo", "condicoes": [{"field": "tipo_contrato", "op": "eq", "value": "obras"}, {"field": "tipo_procedimento", "op": "in", "value": ["concurso_limitado_previa_qualificacao", "concurso_publico", "dialogo_concorrencial", "procedimento_negociacao"]}], "params": {"minimum_days": 40, "deadline_field": "prazo_propostas_dias", "counted_from": "data_envio_anuncio", "usual_days": null}} || {"tipo": "prazo_minimo", "condicoes": [{"field": "tipo_contrato", "op": "eq", "value": "obras"}, {"field": "tipo_procedimento", "op": "in", "value": ["concurso_limitado_previa_qualificacao", "concurso_publico", "dialogo_concorrencial", "procedimento_negociacao"]}], "params": {"minimum_days": 37, "deadline_field": "prazo_propostas_dias", "counted_from": "data_envio_anuncio", "usual_days": null}}
- leitor:b: não tipável (sem_vocabulario): O vocabulário não permite representar a qualidade de concessionário que não seja entidade adjudicante nem as condições de envio eletrónico dos anúncios e de acesso eletrónico à documentação que permitem reduzir os prazos.
- verificador (A): regra 1, tipo_procedimento in ['concurso_limitado_previa_qualificacao', 'concurso_publico', 'dialogo_concorrencial', 'procedimento_negociacao']: as fontes não nomeiam ['procedimento_negociacao']; regra 2, tipo_procedimento in ['concurso_limitado_previa_qualificacao', 'concurso_publico', 'dialogo_concorrencial', 'procedimento_negociacao']: as fontes não nomeiam ['procedimento_negociacao']

## regra:eu-2004-18:auto-limiar-art67-1-a-v20160101@v1

- leitor:a18: não tipável (nao_e_limiar): O valor delimita os contratos a que o título se aplica; não é o limite até ao qual um procedimento pode ser escolhido.
- leitor:b: não tipável (nao_e_limiar): O valor determina a aplicação do título, não um limite até ao qual um procedimento pode ser escolhido.

## regra:eu-2004-18:auto-limiar-art67-1-b-v20160101@v1

- leitor:a18: não tipável (nao_e_limiar): O valor delimita os concursos a que o título se aplica; não é o limite até ao qual um procedimento pode ser escolhido.
- leitor:b: não tipável (nao_e_limiar): O valor determina a aplicação do título, não um limite até ao qual um procedimento pode ser escolhido.

## regra:eu-2009-81:auto-limiar-art8-a@v1

- leitor:a18: não tipável (nao_e_limiar): O valor delimita os contratos a que os limiares se aplicam; não é o limite até ao qual um procedimento pode ser escolhido.
- leitor:b: não tipável (nao_e_limiar): O valor delimita a aplicação da diretiva, não o limite até ao qual um procedimento pode ser escolhido.

## regra:eu-2009-81:auto-limiar-art8-b@v1

- leitor:a18: não tipável (nao_e_limiar): O valor delimita os contratos a que a directiva é aplicável; não é o limite até ao qual um procedimento pode ser escolhido.
- leitor:b: não tipável (nao_e_limiar): O valor delimita a aplicação da diretiva, não o limite até ao qual um procedimento pode ser escolhido.

## regra:eu-2009-81:auto-limiar-art9-4-a@v1

- leitor:a18: não tipável (nao_e_limiar): O valor é o da totalidade dos lotes; não é o limite até ao qual um procedimento pode ser escolhido.
- leitor:b: não tipável (nao_e_limiar): A passagem agrega o valor dos lotes e permite uma derrogação da aplicação da diretiva, sem fixar um limite de valor para a escolha de um procedimento.

## regra:eu-2009-81:auto-prazo-minimo-art33-2@v1

- leitor:a18: {"tipo": "prazo_minimo", "condicoes": [{"field": "tipo_procedimento", "op": "in", "value": ["concurso_limitado_previa_qualificacao", "procedimento_negociacao_com_concurso"]}], "params": {"minimum_days": 37, "deadline_field": "prazo_reclamacao_dias", "counted_from": "data_envio_anuncio", "usual_days": null}}
- leitor:b: {"tipo": "prazo_minimo", "condicoes": [{"field": "tipo_procedimento", "op": "eq", "value": "concurso_limitado_previa_qualificacao"}], "params": {"minimum_days": 40, "deadline_field": "prazo_propostas_dias", "counted_from": "data_envio_convite", "usual_days": null}}
- verificador (A): regra 1: deadline_field prazo_reclamacao_dias e as fontes dizem ['prazo_candidaturas_dias'] (L9)

## regra:eu-2009-81:auto-prazo-minimo-art33-3@v1

- leitor:a18: {"tipo": "prazo_minimo", "condicoes": [{"field": "anuncio_pre_informacao", "op": "eq", "value": true}, {"field": "tipo_procedimento", "op": "in", "value": ["concurso_limitado_previa_qualificacao", "procedimento_negociacao_com_concurso"]}], "params": {"minimum_days": 22, "deadline_field": "prazo_propostas_dias", "counted_from": "data_envio_convite", "usual_days": null}}
- leitor:b: não tipável (sem_vocabulario): O vocabulário não permite representar as condições relativas ao conteúdo do anúncio de pré-informação e à antecedência do seu envio para publicação.
- verificador (A): regra 1: counted_from data_envio_convite e as fontes dizem nada (L9)

## regra:eu-2009-81:auto-prazo-minimo-art59@v1

- leitor:a18: não tipável (sem_vocabulario): O prazo é fixado em dias consecutivos, unidade que o vocabulário não tem.
- leitor:b: não tipável (sem_vocabulario): O vocabulário não prevê um campo de prazo para a interposição de recurso.
- verificador (B): não tipável: «Prazos para interposição de recurso» não está em eu-2009-81:art59

## regra:eu-2014-23:auto-prazo-maximo-art33-2@v1

- leitor:a18: não tipável (nao_e_prazo_maximo): O prazo é um máximo para a própria União publicar os anúncios, não um prazo para os interessados apresentarem algo.
- leitor:b: não tipável (nao_e_prazo_maximo): O prazo é para a publicação dos anúncios, não para apresentar algo.

## regra:eu-2014-23:auto-prazo-minimo-art39-3@v1

- leitor:a18: {"tipo": "prazo_minimo", "condicoes": [{"field": "tipo_contrato", "op": "eq", "value": "concessao_obras"}], "params": {"minimum_days": 30, "deadline_field": "prazo_candidaturas_dias", "counted_from": "data_envio_anuncio", "usual_days": null}}
- leitor:b: {"tipo": "prazo_minimo", "condicoes": [], "params": {"minimum_days": 30, "deadline_field": "prazo_candidaturas_dias", "counted_from": "data_envio_anuncio", "usual_days": null}}
- verificador (A): regra 1, tipo_contrato eq concessao_obras: as fontes não nomeiam ['concessao_obras']

## regra:eu-2014-23:auto-prazo-minimo-art39-4@v1

- leitor:a18: {"tipo": "prazo_minimo", "condicoes": [{"field": "tipo_contrato", "op": "eq", "value": "concessao_obras"}, {"field": "tipo_procedimento", "op": "eq", "value": "concurso_aberto"}], "params": {"minimum_days": 22, "deadline_field": "prazo_propostas_dias", "counted_from": "data_envio_convite", "usual_days": null}}
- leitor:b: não tipável (sem_vocabulario): O vocabulário não permite representar a condição de o procedimento se desenrolar em fases sucessivas.
- verificador (A): regra 1, tipo_contrato eq concessao_obras: as fontes não nomeiam ['concessao_obras']; regra 1, tipo_procedimento eq concurso_aberto: as fontes não nomeiam ['concurso_aberto']

## regra:eu-2014-24:auto-prazo-minimo-art27-2-b@v1

- leitor:a18: não tipável (nao_e_prazo_minimo): O prazo é fixado em função do momento em que o anúncio de pré-informação é enviado, não um prazo para apresentar algo.
- leitor:b: não tipável (nao_e_prazo_minimo): A passagem fixa a antecedência do envio de um anúncio pela entidade adjudicante, não um prazo para apresentar propostas.

## regra:eu-2014-24:auto-prazo-minimo-art27-3@v1

- leitor:a18: {"tipo": "prazo_minimo", "condicoes": [{"field": "tipo_procedimento", "op": "eq", "value": "concurso_aberto"}, {"field": "urgencia_fundamentada", "op": "eq", "value": true}], "params": {"minimum_days": 15, "deadline_field": "prazo_propostas_dias", "counted_from": "data_envio_anuncio", "usual_days": null}}
- leitor:b: não tipável (sem_vocabulario): O vocabulário não permite representar a condição de a urgência inviabilizar o cumprimento do prazo fixado no n.º 1.

## regra:eu-2014-24:auto-prazo-minimo-art28-1@v1

- leitor:a18: {"tipo": "prazo_minimo", "condicoes": [{"field": "tipo_procedimento", "op": "eq", "value": "concurso_limitado_previa_qualificacao"}], "params": {"minimum_days": 30, "deadline_field": "prazo_candidaturas_dias", "counted_from": "data_envio_anuncio", "usual_days": null}}
- leitor:b: não tipável (sem_vocabulario): O vocabulário não permite distinguir se o anúncio de pré-informação é utilizado como meio de abertura de concurso, facto que determina o início da contagem do prazo.

## regra:eu-2014-24:auto-prazo-minimo-art28-2@v1

- leitor:a18: {"tipo": "prazo_minimo", "condicoes": [{"field": "tipo_procedimento", "op": "eq", "value": "concurso_limitado_previa_qualificacao"}], "params": {"minimum_days": 30, "deadline_field": "prazo_candidaturas_dias", "counted_from": "data_envio_convite", "usual_days": null}}
- leitor:b: {"tipo": "prazo_minimo", "condicoes": [{"field": "tipo_procedimento", "op": "eq", "value": "concurso_limitado_previa_qualificacao"}], "params": {"minimum_days": 30, "deadline_field": "prazo_propostas_dias", "counted_from": "data_envio_convite", "usual_days": null}}
- verificador (A): regra 1, tipo_procedimento eq concurso_limitado_previa_qualificacao: as fontes não nomeiam ['concurso_limitado_previa_qualificacao']; regra 1: deadline_field prazo_candidaturas_dias e as fontes dizem ['prazo_propostas_dias'] (L9); regra 1: counted_from data_envio_convite e as fontes dizem nada (L9)

## regra:eu-2014-24:auto-prazo-minimo-art28-3-b@v1

- leitor:a18: não tipável (nao_e_prazo_minimo): O prazo é de 30 dias, e a passagem reduz esse prazo para 10 dias em casos específicos.
- leitor:b: não tipável (sem_vocabulario): O vocabulário não permite representar o intervalo exigido entre o envio do anúncio de pré-informação e o envio do anúncio de concurso, condição da redução do prazo para 10 dias.

## regra:eu-2014-24:auto-prazo-minimo-art28-4@v1

- leitor:a18: não tipável (nao_e_prazo_minimo): O prazo é de 10 dias no mínimo só quando não há acordo entre as autoridades adjudicantes e os candidatos selecionados.
- leitor:b: não tipável (sem_vocabulario): Faltam condições no vocabulário para representar as autoridades adjudicantes subcentrais e a falta de acordo com os candidatos selecionados sobre o prazo.

## regra:eu-2014-24:auto-prazo-minimo-art28-6-a@v1

- leitor:a18: não tipável (nao_e_prazo_minimo): O prazo é de 15 dias, e não um prazo para apresentar algo.
- leitor:b: não tipável (sem_vocabulario): Falta um campo para representar a condição de a urgência inviabilizar o cumprimento dos prazos fixados no artigo.

## regra:eu-2014-24:auto-prazo-minimo-art28-6-b@v1

- leitor:a18: não tipável (nao_e_prazo_minimo): O prazo é um mínimo para as autoridades adjudicantes fixarem, não um prazo para os interessados apresentarem algo.
- leitor:b: {"tipo": "prazo_minimo", "condicoes": [{"field": "tipo_procedimento", "op": "eq", "value": "concurso_limitado_previa_qualificacao"}, {"field": "urgencia_fundamentada", "op": "eq", "value": true}], "params": {"minimum_days": 10, "deadline_field": "prazo_propostas_dias", "counted_from": "data_envio_convite", "usual_days": null}}

## regra:eu-2014-24:auto-prazo-minimo-art29-1@v1

- leitor:a18: {"tipo": "prazo_minimo", "condicoes": [{"field": "tipo_procedimento", "op": "eq", "value": "procedimento_concorrencial_negociacao"}], "params": {"minimum_days": 30, "deadline_field": "prazo_candidaturas_dias", "counted_from": "data_envio_anuncio", "usual_days": null}}
- leitor:b: não tipável (texto_em_falta): Falta o texto dos n.os 3 a 6 do artigo 28.º, declarado aplicável, para determinar os prazos mínimos e as respetivas condições.

## regra:eu-2014-24:auto-prazo-minimo-art30-1@v1

- leitor:a18: {"tipo": "prazo_minimo", "condicoes": [{"field": "tipo_procedimento", "op": "eq", "value": "dialogo_concorrencial"}], "params": {"minimum_days": 30, "deadline_field": "prazo_candidaturas_dias", "counted_from": "data_envio_anuncio", "usual_days": null}}
- leitor:b: {"tipo": "prazo_minimo", "condicoes": [{"field": "tipo_procedimento", "op": "eq", "value": "dialogo_concorrencial"}], "params": {"minimum_days": 30, "deadline_field": "prazo_candidaturas_dias", "counted_from": "data_envio_anuncio", "usual_days": null}}
- verificador (A): regra 1, tipo_procedimento eq dialogo_concorrencial: as fontes não nomeiam ['dialogo_concorrencial']
- verificador (B): regra 1, tipo_procedimento eq dialogo_concorrencial: as fontes não nomeiam ['dialogo_concorrencial']

## regra:eu-2014-24:auto-prazo-maximo-art34-5@v1

- leitor:a18: não tipável (sem_vocabulario): A regra é de um sistema de aquisição dinâmico, instrumento que o vocabulário não tem.
- leitor:b: não tipável (nao_e_prazo_maximo): A passagem fixa prazos para a própria entidade adjudicante avaliar pedidos e comunicar a admissão, não para apresentar algo.

## regra:eu-2014-24:auto-prazo-maximo-art50-3@v1

- leitor:a18: não tipável (nao_e_prazo_maximo): O prazo é de 30 dias para enviar um anúncio de adjudicação, não um prazo máximo para os interessados apresentarem algo.
- leitor:b: não tipável (nao_e_prazo_maximo): Os prazos são para a própria autoridade adjudicante enviar anúncios de adjudicação.

## regra:eu-2014-25:auto-limiar-art15-b@v1

- leitor:a18: {"tipo": "limiar", "condicoes": [{"field": "tipo_contrato", "op": "eq", "value": "obras"}, {"field": "tipo_procedimento", "op": "in", "value": ["concurso_aberto", "concurso_concecao"]}], "params": {"threshold": {"field": "valor_estimado", "comparator": "ge", "value": 5404000, "currency": "EUR"}}}
- leitor:b: não tipável (nao_e_limiar): O valor delimita a aplicação da diretiva, não o valor até ao qual um procedimento pode ser escolhido.
- verificador (A): regra 1, tipo_procedimento in ['concurso_aberto', 'concurso_concecao']: as fontes não nomeiam ['concurso_aberto', 'concurso_concecao']; regra 1: value 5404000 não está nas fontes (L10)

## regra:eu-2014-25:auto-prazo-minimo-art45-3@v1

- leitor:a18: {"tipo": "prazo_minimo", "condicoes": [{"field": "tipo_procedimento", "op": "eq", "value": "concurso_aberto"}, {"field": "urgencia_fundamentada", "op": "eq", "value": true}], "params": {"minimum_days": 15, "deadline_field": "prazo_propostas_dias", "counted_from": "data_envio_anuncio", "usual_days": null}}
- leitor:b: {"tipo": "prazo_minimo", "condicoes": [{"field": "tipo_procedimento", "op": "eq", "value": "concurso_aberto"}, {"field": "urgencia_fundamentada", "op": "eq", "value": true}], "params": {"minimum_days": 15, "deadline_field": "prazo_propostas_dias", "counted_from": "data_envio_anuncio", "usual_days": null}}

## regra:eu-2014-25:auto-prazo-maximo-art45-4@v1

- leitor:a18: não tipável (nao_e_prazo_maximo): O prazo é reduzido em cinco dias, não um máximo.
- leitor:b: não tipável (nao_e_prazo_maximo): A passagem reduz um prazo mínimo de receção de propostas, não fixa um prazo máximo.
- verificador (B): não tipável: fonte em eu-2014-25:art45.1, que é vizinho (L1)

## regra:eu-2014-25:auto-prazo-minimo-art46-1@v1

- leitor:a18: {"tipo": "prazo_minimo", "condicoes": [{"field": "tipo_procedimento", "op": "eq", "value": "concurso_limitado_previa_qualificacao"}], "params": {"minimum_days": 15, "deadline_field": "prazo_candidaturas_dias", "counted_from": "data_envio_anuncio", "usual_days": 30}}
- leitor:b: não tipável (sem_vocabulario): O vocabulário não permite representar o início alternativo da contagem nem distinguir os casos de envio do anúncio e de envio do convite à confirmação de interesse.
- verificador (A): regra 1: usual_days sem «em regra» e os dias nas fontes (L11)

## regra:eu-2014-25:auto-prazo-minimo-art46-2@v1

- leitor:a18: não tipável (nao_e_prazo_minimo): O prazo é um mínimo para a própria entidade adjudicante fixar o de receção das propostas, não um prazo para os candidatos apresentarem algo.
- leitor:b: não tipável (sem_vocabulario): Falta no vocabulário uma condição que represente a ausência de acordo sobre o prazo de receção das propostas.

## regra:eu-2014-25:auto-prazo-minimo-art47-1@v1

- leitor:a18: {"tipo": "prazo_minimo", "condicoes": [{"field": "tipo_procedimento", "op": "eq", "value": "procedimento_negociacao_com_concurso"}], "params": {"minimum_days": 15, "deadline_field": "prazo_candidaturas_dias", "counted_from": "data_envio_anuncio", "usual_days": 30}}
- leitor:b: não tipável (sem_vocabulario): Falta uma condição que distinga a utilização do anúncio periódico indicativo como meio de abertura de concurso da sua mera publicação, pois essa utilização determina o início da contagem.
- verificador (A): regra 1: usual_days sem «em regra» e os dias nas fontes (L11)

## regra:eu-2014-25:auto-prazo-minimo-art47-2@v1

- leitor:a18: não tipável (nao_e_prazo_minimo): O prazo é de 10 dias, no mínimo, para a própria entidade adjudicante convidar os interessados a apresentar propostas, não um prazo para os candidatos apresentarem algo.
- leitor:b: não tipável (sem_vocabulario): O vocabulário não permite representar a falta de acordo sobre o prazo de receção das propostas.

## regra:eu-2014-25:auto-prazo-minimo-art48-1@v1

- leitor:a18: {"tipo": "prazo_minimo", "condicoes": [{"field": "tipo_procedimento", "op": "eq", "value": "dialogo_concorrencial"}], "params": {"minimum_days": 30, "deadline_field": "prazo_candidaturas_dias", "counted_from": "data_envio_anuncio", "usual_days": null}} || {"tipo": "prazo_minimo", "condicoes": [{"field": "anuncio_pre_informacao", "op": "eq", "value": true}, {"field": "tipo_procedimento", "op": "eq", "value": "dialogo_concorrencial"}], "params": {"minimum_days": 15, "deadline_field": "prazo_candidaturas_dias", "counted_from": "data_envio_anuncio", "usual_days": null}}
- leitor:b: {"tipo": "prazo_minimo", "condicoes": [{"field": "anuncio_pre_informacao", "op": "eq", "value": false}, {"field": "tipo_procedimento", "op": "eq", "value": "dialogo_concorrencial"}], "params": {"minimum_days": 15, "deadline_field": "prazo_candidaturas_dias", "counted_from": "data_envio_anuncio", "usual_days": 30}} || {"tipo": "prazo_minimo", "condicoes": [{"field": "anuncio_pre_informacao", "op": "eq", "value": true}, {"field": "tipo_procedimento", "op": "eq", "value": "dialogo_concorrencial"}], "params": {"minimum_days": 15, "deadline_field": "prazo_candidaturas_dias", "counted_from": "data_envio_convite", "usual_days": 30}}
- verificador (A): regra 1, tipo_procedimento eq dialogo_concorrencial: as fontes não nomeiam ['dialogo_concorrencial']; regra 2, tipo_procedimento eq dialogo_concorrencial: as fontes não nomeiam ['dialogo_concorrencial']
- verificador (B): regra 1, tipo_procedimento eq dialogo_concorrencial: as fontes não nomeiam ['dialogo_concorrencial']; regra 1: usual_days sem «em regra» e os dias nas fontes (L11); regra 2, tipo_procedimento eq dialogo_concorrencial: as fontes não nomeiam ['dialogo_concorrencial']; regra 2: counted_from data_envio_convite e as fontes dizem ['data_envio_anuncio'] (L9); regra 2: usual_days sem «em regra» e os dias nas fontes (L11)

## regra:eu-2014-25:auto-prazo-minimo-art49-1@v1

- leitor:a18: {"tipo": "prazo_minimo", "condicoes": [{"field": "tipo_procedimento", "op": "eq", "value": "parceria_inovacao"}], "params": {"minimum_days": 15, "deadline_field": "prazo_candidaturas_dias", "counted_from": "data_envio_anuncio", "usual_days": 30}}
- leitor:b: {"tipo": "prazo_minimo", "condicoes": [{"field": "tipo_procedimento", "op": "eq", "value": "parceria_inovacao"}], "params": {"minimum_days": 15, "deadline_field": "prazo_candidaturas_dias", "counted_from": "data_envio_anuncio", "usual_days": 30}}
- verificador (A): regra 1: usual_days sem «em regra» e os dias nas fontes (L11)
- verificador (B): regra 1: usual_days sem «em regra» e os dias nas fontes (L11)

## regra:eu-2014-25:auto-prazo-maximo-art52-5@v1

- leitor:a18: não tipável (sem_vocabulario): A regra é de um sistema de aquisição dinâmico, instrumento que o vocabulário não tem.
- leitor:b: não tipável (nao_e_prazo_maximo): O prazo é para a própria entidade adjudicante avaliar os pedidos de participação, não para apresentar elementos.

## regra:eu-2014-25:auto-prazo-maximo-art70-2@v1

- leitor:a18: não tipável (nao_e_prazo_maximo): O prazo é de 30 dias para publicar um anúncio de adjudicação com indicação, não um prazo máximo para os interessados apresentarem algo.
- leitor:b: não tipável (nao_e_prazo_maximo): Os prazos regulam o envio de anúncios pelas próprias entidades adjudicantes.

