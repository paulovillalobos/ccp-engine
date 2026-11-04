# FÁBRICA DE REGRAS — ronda 12 (DECISIONS D72)

Gerado por tools/rule_factory.py (ccp-rule-factory-0.8) com o protocolo de leitura v3 (tools/read_rules_v3.py, ccp-read-rules-v3-0.5). D72: toda a lei real que o depósito tem e que diz dias ou euros, ainda não perguntada: o CCP em vigor, as versões anteriores do CCP cujos números diferem dos de hoje, e as diretivas da União sobre contratação pública (D70). Protocolo 0.5: o tipo prazo_maximo e os nomes de procedimento das diretivas (D71). Adaptador v14; grupo reservado (exame) pela regra do TRAIN-HELD-OUT, o resto é prática. Propõe leitor:a16 (AMALIA + adaptador v14), leitor:b revê às cegas.

Uma passagem é lida na data em que o texto estava em vigor. Um programa confirma cada palavra citada; a leitura que falha não fica registada; o «não tipável» com o mesmo motivo também assenta.

| grupo | alvos | leitor A válido | leitor B válido | assentes | regras | «não tipável» |
|---|---|---|---|---|---|---|
| pratica | 296 | 247 | 271 | 67 | 6 | 61 |
| reservado | 81 | 55 | 74 | 14 | 5 | 9 |
| todos | 377 | 302 | 345 | 81 | 11 | 70 |

| regra | passagem | estado | replica | verificador: leitor A | verificador: leitor B |
|---|---|---|---|---|---|
| regra:ccp:auto-prazo-maximo-art35-b-3@v1 | ccp:art35-b.3 | proposed (não tipável: nao_e_prazo_minimo) | não | ok | ok |
| regra:ccp:auto-prazo-maximo-art35-c-2-c@v1 | ccp:art35-c.2.c | settled (não tipável: nao_e_prazo_maximo) | sim | ok | ok |
| regra:ccp:auto-prazo-maximo-art43-v20180101@v1 | ccp:art43 | proposed (não tipável: nao_e_prazo_maximo) | — | ok | não tipável: fonte em ccp:art43.10.a, que é vizinho (L1) |
| regra:ccp:auto-prazo-maximo-art43-v20251028@v1 | ccp:art43 | proposed (não tipável: nao_e_prazo_maximo) | — | ok | não tipável: fonte em ccp:art43.10.a, que é vizinho (L1) |
| regra:ccp:auto-prazo-maximo-art43-10-a@v1 | ccp:art43.10.a | settled (não tipável: nao_e_prazo_maximo) | sim | ok | ok |
| regra:ccp:auto-prazo-maximo-art43-10-b@v1 | ccp:art43.10.b | settled (não tipável: nao_e_prazo_maximo) | sim | ok | ok |
| regra:ccp:auto-prazo-maximo-art43-10-c@v1 | ccp:art43.10.c | settled (não tipável: nao_e_prazo_maximo) | sim | ok | ok |
| regra:ccp:auto-limiar-art46-a-2@v1 | ccp:art46-a.2 | settled (não tipável: nao_e_limiar) | sim | ok | ok |
| regra:ccp:auto-limiar-art55-3-a@v1 | ccp:art55.3.a | settled (não tipável: nao_e_limiar) | sim | ok | ok |
| regra:ccp:auto-prazo-maximo-art61-4-v20120811@v1 | ccp:art61.4 | settled (não tipável: nao_e_prazo_maximo) | sim | ok | ok |
| regra:ccp:auto-prazo-maximo-art65@v1 | ccp:art65 | proposed (não tipável: nao_e_prazo_minimo) | não | ok | ok |
| regra:ccp:auto-prazo-maximo-art72-v20180101@v1 | ccp:art72 | proposed (não tipável: nao_e_prazo_maximo) | não | ok | ok |
| regra:ccp:auto-prazo-maximo-art72-v20221202@v1 | ccp:art72 | proposed (não tipável: nao_e_prazo_maximo) | não | ok | ok |
| regra:ccp:auto-prazo-maximo-art72-3@v1 | ccp:art72.3 | proposed (não tipável: nao_e_prazo_maximo) | não | ok | ok |
| regra:ccp:auto-prazo-maximo-art78-v20180101@v1 | ccp:art78 | proposed (não tipável: nao_e_prazo_maximo) | — | ok | não tipável: fonte em ccp:art78.5, que é vizinho (L1) |
| regra:ccp:auto-prazo-maximo-art78-1-v20080730@v1 | ccp:art78.1 | proposed (não tipável: nao_e_prazo_minimo) | não | ok | ok |
| regra:ccp:auto-prazo-maximo-art78-1@v1 | ccp:art78.1 | proposed (não tipável: nao_e_prazo_minimo) | não | ok | ok |
| regra:ccp:auto-prazo-maximo-art78-5@v1 | ccp:art78.5 | proposed (não tipável: sem_vocabulario) | não | ok | ok |
| regra:ccp:auto-prazo-maximo-art85-2@v1 | ccp:art85.2 | proposed (não tipável: nao_e_prazo_minimo) | não | ok | ok |
| regra:ccp:auto-prazo-maximo-art86-v20120811@v1 | ccp:art86 | proposed (não tipável: nao_e_prazo_minimo) | — | ok | não tipável: fonte em ccp:art86.2, que é vizinho (L1) |
| regra:ccp:auto-prazo-maximo-art86-2-v20091007@v1 | ccp:art86.2 | proposed (não tipável: nao_e_prazo_minimo) | não | ok | ok |
| regra:ccp:auto-prazo-maximo-art86-3@v1 | ccp:art86.3 | proposed (não tipável: nao_e_prazo_minimo) | não | ok | ok |
| regra:ccp:auto-prazo-maximo-art87-a-2@v1 | ccp:art87-a.2 | proposed (não tipável: nao_e_prazo_maximo) | não | ok | ok |
| regra:ccp:auto-prazo-maximo-art90-1@v1 | ccp:art90.1 | proposed (não tipável: nao_e_prazo_minimo) | não | ok | ok |
| regra:ccp:auto-prazo-maximo-art91-2@v1 | ccp:art91.2 | proposed (não tipável: nao_e_prazo_maximo) | não | ok | ok |
| regra:ccp:auto-prazo-maximo-art93-2@v1 | ccp:art93.2 | proposed (não tipável: nao_e_prazo_maximo) | não | ok | ok |
| regra:ccp:auto-prazo-maximo-art95-v20080730@v1 | ccp:art95 | proposed (não tipável: nao_e_prazo_maximo) | — | ok | não tipável: fonte em ccp:art95.1.c.i, que é vizinho (L1) |
| regra:ccp:auto-limiar-art95-1-a@v1 | ccp:art95.1.a | sem leitura válida de leitor:a16 | — | regra 1, tipo_procedimento eq ajuste_direto: as fontes não nomeiam ['ajuste_direto'] | ok |
| regra:ccp:auto-prazo-maximo-art95-1-c-i@v1 | ccp:art95.1.c.i | proposed (não tipável: sem_vocabulario) | não | ok | ok |
| regra:ccp:auto-limiar-art95-1-d@v1 | ccp:art95.1.d | settled (não tipável: nao_e_limiar) | sim | ok | ok |
| regra:ccp:auto-prazo-maximo-art95-3@v1 | ccp:art95.3 | proposed (não tipável: nao_e_prazo_minimo) | não | ok | ok |
| regra:ccp:auto-prazo-maximo-art101@v1 | ccp:art101 | proposed (não tipável: nao_e_prazo_minimo) | — | ok | regra 1: as fontes de maximum_days não dizem um máximo («não pode ser superior a», «no prazo de», L8) |
| regra:ccp:auto-prazo-maximo-art102-v20080730@v1 | ccp:art102 | proposed (não tipável: nao_e_prazo_minimo) | — | ok | não tipável: fonte em ccp:art102.2, que é vizinho (L1) |
| regra:ccp:auto-prazo-maximo-art102-2@v1 | ccp:art102.2 | proposed (não tipável: nao_e_prazo_minimo) | não | ok | ok |
| regra:ccp:auto-prazo-minimo-art104-v20080730@v1 | ccp:art104 | proposed (não tipável: nao_e_prazo_minimo) | — | ok | não tipável: fonte em ccp:art104.1, que é vizinho (L1) |
| regra:ccp:auto-prazo-maximo-art104-1-a@v1 | ccp:art104.1.a | proposed (não tipável: nao_e_prazo_minimo) | não | ok | ok |
| regra:ccp:auto-prazo-maximo-art108-1-v20080730@v1 | ccp:art108.1 | proposed (não tipável: nao_e_prazo_minimo) | não | ok | ok |
| regra:ccp:auto-prazo-maximo-art115-1-j-v20180101@v1 | ccp:art115.1.j | proposed (não tipável: nao_e_prazo_maximo) | não | ok | ok |
| regra:ccp:auto-prazo-maximo-art115-1-k@v1 | ccp:art115.1.k | proposed (não tipável: nao_e_prazo_maximo) | não | ok | ok |
| regra:ccp:auto-prazo-maximo-art122-v20180101@v1 | ccp:art122 | proposed (não tipável: nao_e_prazo_minimo) | — | ok | não tipável: fonte em ccp:art122.1, que é vizinho (L1) |
| regra:ccp:auto-prazo-maximo-art122-1@v1 | ccp:art122.1 | proposed (não tipável: nao_e_prazo_minimo) | não | ok | ok |
| regra:ccp:auto-prazo-maximo-art129-a-6@v1 | ccp:art129-a.6 | settled (não tipável: nao_e_prazo_maximo) | sim | ok | ok |
| regra:ccp:auto-prazo-minimo-art135-1-v20080730@v1 | ccp:art135.1 | settled (2 regras) | sim | ok | ok |
| regra:ccp:auto-prazo-minimo-art135-2-v20080730@v1 | ccp:art135.2 | sem leitura válida de leitor:a16 | — | regra 1, urgencia_fundamentada eq False: as fontes não negam o facto (L7) | ok |
| regra:ccp:auto-prazo-minimo-art136-1-v20080730@v1 | ccp:art136.1 | sem leitura válida de leitor:a16 | — | regra 1, publicado_joue eq True: as fontes não afirmam o facto (L7) | ok |
| regra:ccp:auto-prazo-minimo-art136-2-a-v20080730@v1 | ccp:art136.2.a | settled (não tipável: sem_vocabulario) | sim | ok | ok |
| regra:ccp:auto-prazo-minimo-art136-3-v20080730@v1 | ccp:art136.3 | proposed | não | ok | ok |
| regra:ccp:auto-prazo-minimo-art136-4-v20080730@v1 | ccp:art136.4 | sem leitura válida de leitor:a16 | — | regra 1: counted_from data_envio_anuncio e as fontes dizem nada (L9) | ok |
| regra:ccp:auto-prazo-maximo-art138-3@v1 | ccp:art138.3 | proposed (não tipável: nao_e_prazo_minimo) | não | ok | ok |
| regra:ccp:auto-prazo-minimo-art147-v20180101@v1 | ccp:art147 | settled | sim | ok | ok |
| regra:ccp:auto-limiar-art155-a@v1 | ccp:art155.a | sem leitura válida de leitor:a16 | — | regra 1, tipo_procedimento eq concurso_publico_urgente: as fontes não nomeiam ['concurso_publico_urgente'] | ok |
| regra:ccp:auto-prazo-maximo-art159@v1 | ccp:art159 | proposed (não tipável: nao_e_prazo_minimo) | não | ok | ok |
| regra:ccp:auto-prazo-maximo-art161@v1 | ccp:art161 | proposed (não tipável: nao_e_prazo_minimo) | não | ok | ok |
| regra:ccp:auto-prazo-maximo-art161-b-1-b@v1 | ccp:art161-b.1.b | proposed (não tipável: nao_e_prazo_minimo) | não | ok | ok |
| regra:ccp:auto-prazo-maximo-art161-b-4@v1 | ccp:art161-b.4 | sem leitura válida de leitor:a16 | — | regra 1: as fontes de maximum_days não dizem um máximo («não pode ser superior a», «no prazo de», L8) | ok |
| regra:ccp:auto-prazo-minimo-art173@v1 | ccp:art173 | sem leitura válida de leitor:a16 | — | regra 1: counted_from data_envio_anuncio e as fontes dizem nada (L9) | ok |
| regra:ccp:auto-prazo-minimo-art174-v20180101@v1 | ccp:art174 | proposed (2 regras) | — | ok | regra 1, tipo_procedimento eq concurso_limitado_previa_qualificacao: fonte em ccp:art174.1, que é vizinho (L1) |
| regra:ccp:auto-prazo-minimo-art174-1-v20080730@v1 | ccp:art174.1 | sem leitura válida de leitor:a16 | — | regra 1, publicado_joue eq True: as fontes não afirmam o facto (L7) | ok |
| regra:ccp:auto-prazo-minimo-art174-2-v20080730@v1 | ccp:art174.2 | sem leitura válida de leitor:a16 | — | regra 1, publicado_joue eq True: as fontes não afirmam o facto (L7) | ok |
| regra:ccp:auto-prazo-minimo-art174-3-v20080730@v1 | ccp:art174.3 | sem leitura válida de leitor:a16 | — | regra 1, tipo_contrato not_in ['concessao_obras', 'concessao_servicos']: as fontes não nomeiam ['concessao_servicos'] | ok |
| regra:ccp:auto-prazo-minimo-art174-4@v1 | ccp:art174.4 | proposed (não tipável: texto_em_falta) | não | ok | ok |
| regra:ccp:auto-prazo-maximo-art177-3@v1 | ccp:art177.3 | proposed (não tipável: nao_e_prazo_minimo) | não | ok | ok |
| regra:ccp:auto-prazo-maximo-art187-1-v20080730@v1 | ccp:art187.1 | proposed (não tipável: nao_e_prazo_minimo) | não | ok | ok |
| regra:ccp:auto-prazo-maximo-art187-1-v20180101@v1 | ccp:art187.1 | proposed (não tipável: nao_e_prazo_minimo) | não | ok | ok |
| regra:ccp:auto-prazo-maximo-art187-1@v1 | ccp:art187.1 | proposed (não tipável: nao_e_prazo_minimo) | não | ok | ok |
| regra:ccp:auto-prazo-minimo-art187-2-v20180101@v1 | ccp:art187.2 | proposed (não tipável: nao_e_prazo_minimo) | não | ok | ok |
| regra:ccp:auto-prazo-maximo-art187-4-v20180101@v1 | ccp:art187.4 | proposed (não tipável: nao_e_prazo_minimo) | não | ok | ok |
| regra:ccp:auto-prazo-maximo-art188-4@v1 | ccp:art188.4 | proposed (não tipável: nao_e_prazo_minimo) | não | ok | ok |
| regra:ccp:auto-prazo-minimo-art190-1-v20080730@v1 | ccp:art190.1 | settled (2 regras) | sim | ok | ok |
| regra:ccp:auto-prazo-minimo-art190-2-v20080730@v1 | ccp:art190.2 | sem leitura válida de leitor:a16 | — | regra 1: minimum_days 8 não está nas fontes (L8, L4) | ok |
| regra:ccp:auto-prazo-minimo-art190-2@v1 | ccp:art190.2 | proposed (2 regras) | não | ok | ok |
| regra:ccp:auto-prazo-minimo-art191-v20180101@v1 | ccp:art191 | proposed (3 regras) | — | ok | não tipável: fonte em ccp:art191.2, que é vizinho (L1) |
| regra:ccp:auto-prazo-minimo-art191-1-v20080730@v1 | ccp:art191.1 | settled | sim | ok | ok |
| regra:ccp:auto-prazo-minimo-art191-2-a-v20080730@v1 | ccp:art191.2.a | sem leitura válida de leitor:a16 | — | regra 1, data_inicio_procedimento ge 2008-07-30: as fontes não fixam uma data (L13) | ok |
| regra:ccp:auto-prazo-minimo-art191-2-a@v1 | ccp:art191.2.a | proposed | não | ok | ok |
| regra:ccp:auto-prazo-minimo-art191-3-v20080730@v1 | ccp:art191.3 | settled | sim | ok | ok |
| regra:ccp:auto-prazo-minimo-art191-3@v1 | ccp:art191.3 | settled | sim | ok | ok |
| regra:ccp:auto-prazo-maximo-art192-3@v1 | ccp:art192.3 | proposed (não tipável: nao_e_prazo_minimo) | não | ok | ok |
| regra:ccp:auto-prazo-maximo-art192-4@v1 | ccp:art192.4 | proposed (não tipável: texto_em_falta) | não | ok | ok |
| regra:ccp:auto-prazo-minimo-art198-1-v20080730@v1 | ccp:art198.1 | sem leitura válida de leitor:a16 | — | regra 1, publicado_joue eq True: as fontes não afirmam o facto (L7) | regra 1, publicado_joue eq True: as fontes não afirmam o facto (L7) |
| regra:ccp:auto-prazo-minimo-art198-2-v20080730@v1 | ccp:art198.2 | settled | sim | ok | ok |
| regra:ccp:auto-prazo-minimo-art214-1@v1 | ccp:art214.1 | settled (não tipável: nao_e_prazo_minimo) | sim | ok | ok |
| regra:ccp:auto-prazo-minimo-art218-v20080730@v1 | ccp:art218 | proposed | — | ok | regra 1, tipo_procedimento eq dialogo_concorrencial: «diálogo concorrencial» não está em ccp:art218 |
| regra:ccp:auto-prazo-maximo-art219-c-3-v20180101@v1 | ccp:art219-c.3 | proposed (não tipável: texto_em_falta) | não | ok | ok |
| regra:ccp:auto-prazo-maximo-art219-c-3@v1 | ccp:art219-c.3 | proposed (não tipável: texto_em_falta) | não | ok | ok |
| regra:ccp:auto-prazo-maximo-art219-i-5@v1 | ccp:art219-i.5 | proposed (não tipável: nao_e_prazo_maximo) | não | ok | ok |
| regra:ccp:auto-prazo-maximo-art234-1-v20080730@v1 | ccp:art234.1 | proposed (não tipável: nao_e_prazo_minimo) | não | ok | ok |
| regra:ccp:auto-prazo-maximo-art235-v20080730@v1 | ccp:art235 | proposed (não tipável: texto_em_falta) | não | ok | ok |
| regra:ccp:auto-prazo-minimo-art240-1-b@v1 | ccp:art240.1.b | settled (não tipável: sem_vocabulario) | sim | ok | ok |
| regra:ccp:auto-prazo-maximo-art241-3-v20080730@v1 | ccp:art241.3 | proposed (não tipável: sem_vocabulario) | não | ok | ok |
| regra:ccp:auto-prazo-maximo-art241-a-3@v1 | ccp:art241-a.3 | proposed (não tipável: sem_vocabulario) | não | ok | ok |
| regra:ccp:auto-prazo-maximo-art241-d@v1 | ccp:art241-d | settled (não tipável: sem_vocabulario) | sim | ok | ok |
| regra:ccp:auto-prazo-minimo-art242-3-v20080730@v1 | ccp:art242.3 | proposed (não tipável: sem_vocabulario) | não | ok | ok |
| regra:ccp:auto-prazo-minimo-art242-4-v20080730@v1 | ccp:art242.4 | settled (não tipável: sem_vocabulario) | sim | ok | ok |
| regra:ccp:auto-prazo-minimo-art243-2-a-v20080730@v1 | ccp:art243.2.a | settled (não tipável: sem_vocabulario) | sim | ok | ok |
| regra:ccp:auto-prazo-maximo-art270@v1 | ccp:art270 | proposed (não tipável: nao_e_prazo_minimo) | não | ok | ok |
| regra:ccp:auto-prazo-maximo-art273@v1 | ccp:art273 | proposed (não tipável: nao_e_prazo_minimo) | não | ok | ok |
| regra:ccp:auto-prazo-maximo-art274-1@v1 | ccp:art274.1 | proposed (não tipável: nao_e_prazo_minimo) | não | ok | ok |
| regra:ccp:auto-prazo-minimo-art276-v20120811@v1 | ccp:art276 | sem leitura válida de leitor:a16 | — | regra 1, tipo_entidade eq estado: as fontes não nomeiam ['estado'] | ok |
| regra:ccp:auto-prazo-minimo-art276-v20180101@v1 | ccp:art276 | sem leitura válida de leitor:a16 | — | regra 1, tipo_procedimento eq concurso_publico: as fontes não nomeiam ['concurso_publico'] | ok |
| regra:ccp:auto-prazo-minimo-art276-v20210620@v1 | ccp:art276 | sem leitura válida de leitor:a16 | — | regra 1, tipo_procedimento eq ajuste_direto: as fontes não nomeiam ['ajuste_direto'] | ok |
| regra:ccp:auto-prazo-minimo-art276-5-v20080730@v1 | ccp:art276.5 | sem leitura válida de leitor:a16 | — | regra 1, tipo_procedimento eq concurso_publico: as fontes não nomeiam ['concurso_publico'] | ok |
| regra:ccp:auto-prazo-minimo-art276-7-v20080730@v1 | ccp:art276.7 | settled (não tipável: sem_vocabulario) | sim | ok | ok |
| regra:ccp:auto-prazo-maximo-art283-a-v20110113@v1 | ccp:art283-a | proposed (não tipável: texto_em_falta) | — | ok | não tipável: fonte em ccp:art283-a.2.c, que é vizinho (L1) |
| regra:ccp:auto-prazo-maximo-art283-a-v20210620@v1 | ccp:art283-a | proposed (não tipável: texto_em_falta) | — | ok | não tipável: fonte em ccp:art283-a.2.c, que é vizinho (L1) |
| regra:ccp:auto-prazo-maximo-art283-a-2-c@v1 | ccp:art283-a.2.c | proposed (não tipável: nao_e_prazo_minimo) | não | ok | ok |
| regra:ccp:auto-prazo-maximo-art287-6-c-v20180101@v1 | ccp:art287.6.c | proposed (não tipável: nao_e_prazo_minimo) | não | ok | ok |
| regra:ccp:auto-prazo-minimo-art295-v20091007@v1 | ccp:art295 | proposed (não tipável: nao_e_prazo_minimo) | — | ok | não tipável: fonte em ccp:art295.3, que é vizinho (L1) |
| regra:ccp:auto-prazo-maximo-art295-3@v1 | ccp:art295.3 | settled (não tipável: nao_e_prazo_maximo) | sim | ok | ok |
| regra:ccp:auto-prazo-minimo-art295-4@v1 | ccp:art295.4 | settled (não tipável: nao_e_prazo_minimo) | sim | ok | ok |
| regra:ccp:auto-prazo-maximo-art295-5-a-v20080730@v1 | ccp:art295.5.a | proposed (não tipável: nao_e_prazo_minimo) | não | ok | ok |
| regra:ccp:auto-prazo-maximo-art295-5-b-v20080730@v1 | ccp:art295.5.b | settled (não tipável: nao_e_prazo_maximo) | sim | ok | ok |
| regra:ccp:auto-prazo-minimo-art295-6-v20080730@v1 | ccp:art295.6 | settled (não tipável: nao_e_prazo_minimo) | sim | ok | ok |
| regra:ccp:auto-prazo-maximo-art295-9@v1 | ccp:art295.9 | settled (não tipável: nao_e_prazo_maximo) | sim | ok | ok |
| regra:ccp:auto-prazo-maximo-art296-2@v1 | ccp:art296.2 | proposed (não tipável: nao_e_prazo_minimo) | não | ok | ok |
| regra:ccp:auto-prazo-maximo-art299-1-v20080730@v1 | ccp:art299.1 | proposed (não tipável: nao_e_prazo_minimo) | não | ok | ok |
| regra:ccp:auto-prazo-maximo-art299-1-a@v1 | ccp:art299.1.a | proposed (não tipável: nao_e_prazo_minimo) | não | ok | ok |
| regra:ccp:auto-prazo-maximo-art299-1-b@v1 | ccp:art299.1.b | proposed (não tipável: nao_e_prazo_minimo) | não | ok | ok |
| regra:ccp:auto-prazo-maximo-art299-1-c@v1 | ccp:art299.1.c | proposed (não tipável: nao_e_prazo_minimo) | não | ok | ok |
| regra:ccp:auto-prazo-maximo-art299-1-d@v1 | ccp:art299.1.d | proposed (não tipável: nao_e_prazo_minimo) | não | ok | ok |
| regra:ccp:auto-prazo-maximo-art299-2-v20080730@v1 | ccp:art299.2 | settled (não tipável: nao_e_prazo_maximo) | sim | ok | ok |
| regra:ccp:auto-prazo-maximo-art299-2@v1 | ccp:art299.2 | sem leitura válida de leitor:a16 | — | regra 1, tipo_procedimento eq procedimento_concorrencial_negociacao: as fontes não nomeiam ['procedimento_concorrencial_ | ok |
| regra:ccp:auto-prazo-maximo-art299-3@v1 | ccp:art299.3 | proposed (não tipável: nao_e_prazo_minimo) | não | ok | ok |
| regra:ccp:auto-prazo-maximo-art299-4@v1 | ccp:art299.4 | settled (não tipável: nao_e_prazo_maximo) | sim | ok | ok |
| regra:ccp:auto-prazo-maximo-art299-a-1@v1 | ccp:art299-a.1 | proposed (não tipável: nao_e_prazo_minimo) | não | ok | ok |
| regra:ccp:auto-prazo-maximo-art304-3@v1 | ccp:art304.3 | settled (não tipável: nao_e_prazo_maximo) | sim | ok | ok |
| regra:ccp:auto-prazo-maximo-art315-v20210620@v1 | ccp:art315 | proposed (não tipável: nao_e_prazo_minimo) | — | ok | não tipável: fonte em ccp:art315.1, que é vizinho (L1) |
| regra:ccp:auto-prazo-maximo-art315-1-v20180101@v1 | ccp:art315.1 | proposed (não tipável: nao_e_prazo_minimo) | não | ok | ok |
| regra:ccp:auto-prazo-maximo-art315-1@v1 | ccp:art315.1 | proposed (não tipável: nao_e_prazo_minimo) | não | ok | ok |
| regra:ccp:auto-prazo-maximo-art319-3-v20080730@v1 | ccp:art319.3 | proposed (não tipável: nao_e_prazo_minimo) | não | ok | ok |
| regra:ccp:auto-prazo-maximo-art319-3-v20180101@v1 | ccp:art319.3 | proposed (não tipável: nao_e_prazo_minimo) | não | ok | ok |
| regra:ccp:auto-prazo-maximo-art319-a-7@v1 | ccp:art319-a.7 | settled (não tipável: nao_e_prazo_maximo) | sim | ok | ok |
| regra:ccp:auto-prazo-maximo-art321-a-2@v1 | ccp:art321-a.2 | settled (não tipável: nao_e_prazo_maximo) | sim | ok | ok |
| regra:ccp:auto-prazo-minimo-art327-v20080730@v1 | ccp:art327 | proposed (não tipável: texto_em_falta) | — | ok | não tipável: fonte em ccp:art327.3, que é vizinho (L1) |
| regra:ccp:auto-prazo-maximo-art327-4@v1 | ccp:art327.4 | proposed (não tipável: nao_e_prazo_minimo) | não | ok | ok |
| regra:ccp:auto-prazo-maximo-art329-5@v1 | ccp:art329.5 | settled (não tipável: nao_e_prazo_maximo) | sim | ok | ok |
| regra:ccp:auto-prazo-maximo-art332-4@v1 | ccp:art332.4 | proposed (não tipável: nao_e_prazo_minimo) | não | ok | ok |
| regra:ccp:auto-prazo-maximo-art333-4@v1 | ccp:art333.4 | proposed (não tipável: nao_e_prazo_minimo) | não | ok | ok |
| regra:ccp:auto-prazo-maximo-art334-3@v1 | ccp:art334.3 | proposed (não tipável: nao_e_prazo_minimo) | não | ok | ok |
| regra:ccp:auto-prazo-maximo-art345-3@v1 | ccp:art345.3 | proposed (não tipável: nao_e_prazo_minimo) | — | ok | regra 1: as fontes de maximum_days não dizem um máximo («não pode ser superior a», «no prazo de», L8) |
| regra:ccp:auto-prazo-maximo-art345-4@v1 | ccp:art345.4 | proposed (não tipável: nao_e_prazo_minimo) | não | ok | ok |
| regra:ccp:auto-prazo-maximo-art345-5@v1 | ccp:art345.5 | settled (não tipável: nao_e_prazo_maximo) | sim | ok | ok |
| regra:ccp:auto-prazo-maximo-art354-v20080730@v1 | ccp:art354 | proposed (não tipável: nao_e_prazo_minimo) | — | ok | não tipável: fonte em ccp:art354.2, que é vizinho (L1) |
| regra:ccp:auto-prazo-maximo-art354-2@v1 | ccp:art354.2 | proposed (não tipável: nao_e_prazo_minimo) | não | ok | ok |
| regra:ccp:auto-prazo-maximo-art354-4@v1 | ccp:art354.4 | settled (não tipável: nao_e_prazo_maximo) | sim | ok | ok |
| regra:ccp:auto-prazo-maximo-art358-2-v20080730@v1 | ccp:art358.2 | proposed (não tipável: nao_e_prazo_minimo) | não | ok | ok |
| regra:ccp:auto-prazo-maximo-art359-1@v1 | ccp:art359.1 | proposed (não tipável: nao_e_prazo_minimo) | não | ok | ok |
| regra:ccp:auto-prazo-maximo-art361-5@v1 | ccp:art361.5 | settled (não tipável: nao_e_prazo_maximo) | sim | ok | ok |
| regra:ccp:auto-prazo-maximo-art366-1@v1 | ccp:art366.1 | proposed (não tipável: nao_e_prazo_minimo) | não | ok | ok |
| regra:ccp:auto-prazo-minimo-art366-5@v1 | ccp:art366.5 | settled (não tipável: nao_e_prazo_minimo) | sim | ok | ok |
| regra:ccp:auto-prazo-maximo-art366-6@v1 | ccp:art366.6 | proposed (não tipável: nao_e_prazo_minimo) | não | ok | ok |
| regra:ccp:auto-prazo-maximo-art372-1-v20080730@v1 | ccp:art372.1 | proposed (não tipável: nao_e_prazo_minimo) | não | ok | ok |
| regra:ccp:auto-prazo-maximo-art372-1-v20180101@v1 | ccp:art372.1 | proposed (não tipável: nao_e_prazo_minimo) | não | ok | ok |
| regra:ccp:auto-prazo-maximo-art372-1-v20210620@v1 | ccp:art372.1 | proposed (não tipável: nao_e_prazo_minimo) | não | ok | ok |
| regra:ccp:auto-prazo-maximo-art372-1@v1 | ccp:art372.1 | proposed (não tipável: nao_e_prazo_minimo) | não | ok | ok |
| regra:ccp:auto-prazo-maximo-art372-2@v1 | ccp:art372.2 | proposed (não tipável: nao_e_prazo_minimo) | não | ok | ok |
| regra:ccp:auto-prazo-maximo-art373-v20210620@v1 | ccp:art373 | proposed (não tipável: nao_e_prazo_maximo) | — | ok | não tipável: fonte em ccp:art373.2, que é vizinho (L1) |
| regra:ccp:auto-prazo-maximo-art373-2-v20080730@v1 | ccp:art373.2 | proposed (não tipável: nao_e_prazo_minimo) | não | ok | ok |
| regra:ccp:auto-prazo-maximo-art373-2-v20091007@v1 | ccp:art373.2 | proposed (não tipável: nao_e_prazo_minimo) | não | ok | ok |
| regra:ccp:auto-prazo-maximo-art373-2@v1 | ccp:art373.2 | sem leitura válida de leitor:a16 | — | regra 1, tipo_procedimento eq concurso_publico: as fontes não nomeiam ['concurso_publico'] | ok |
| regra:ccp:auto-prazo-maximo-art373-3-v20080730@v1 | ccp:art373.3 | settled (não tipável: nao_e_prazo_maximo) | sim | ok | ok |
| regra:ccp:auto-prazo-maximo-art373-3@v1 | ccp:art373.3 | sem leitura válida de leitor:a16 | — | regra 1: as fontes de maximum_days não dizem um máximo («não pode ser superior a», «no prazo de», L8) | ok |
| regra:ccp:auto-prazo-maximo-art373-5@v1 | ccp:art373.5 | settled (não tipável: nao_e_prazo_maximo) | sim | ok | ok |
| regra:ccp:auto-prazo-maximo-art376-6-v20080730@v1 | ccp:art376.6 | proposed (não tipável: nao_e_prazo_minimo) | não | ok | ok |
| regra:ccp:auto-prazo-maximo-art376-7-v20120811@v1 | ccp:art376.7 | proposed (não tipável: nao_e_prazo_minimo) | não | ok | ok |
| regra:ccp:auto-prazo-maximo-art378-3-v20180101@v1 | ccp:art378.3 | proposed (não tipável: nao_e_prazo_minimo) | não | ok | ok |
| regra:ccp:auto-prazo-maximo-art378-4-v20080730@v1 | ccp:art378.4 | proposed (não tipável: nao_e_prazo_minimo) | não | ok | ok |
| regra:ccp:auto-prazo-maximo-art378-4-v20120811@v1 | ccp:art378.4 | proposed (não tipável: nao_e_prazo_minimo) | não | ok | ok |
| regra:ccp:auto-prazo-maximo-art378-4-v20180101@v1 | ccp:art378.4 | proposed (não tipável: nao_e_prazo_minimo) | não | ok | ok |
| regra:ccp:auto-prazo-maximo-art378-4@v1 | ccp:art378.4 | proposed (não tipável: nao_e_prazo_minimo) | não | ok | ok |
| regra:ccp:auto-prazo-maximo-art378-5@v1 | ccp:art378.5 | proposed (não tipável: sem_vocabulario) | não | ok | ok |
| regra:ccp:auto-prazo-maximo-art385-v20230715@v1 | ccp:art385 | proposed (não tipável: nao_e_prazo_minimo) | — | ok | não tipável: fonte em ccp:art385.3, que é vizinho (L1) |
| regra:ccp:auto-prazo-maximo-art385-3-v20080730@v1 | ccp:art385.3 | proposed (não tipável: nao_e_prazo_minimo) | não | ok | ok |
| regra:ccp:auto-prazo-maximo-art385-3@v1 | ccp:art385.3 | proposed (não tipável: nao_e_prazo_minimo) | não | ok | ok |
| regra:ccp:auto-prazo-maximo-art386-2@v1 | ccp:art386.2 | proposed (não tipável: nao_e_prazo_minimo) | não | ok | ok |
| regra:ccp:auto-prazo-maximo-art389-1@v1 | ccp:art389.1 | proposed (não tipável: nao_e_prazo_minimo) | não | ok | ok |
| regra:ccp:auto-prazo-minimo-art394-3@v1 | ccp:art394.3 | settled (não tipável: nao_e_prazo_minimo) | sim | ok | ok |
| regra:ccp:auto-prazo-maximo-art394-5@v1 | ccp:art394.5 | proposed (não tipável: nao_e_prazo_minimo) | não | ok | ok |
| regra:ccp:auto-prazo-maximo-art394-7@v1 | ccp:art394.7 | settled (não tipável: nao_e_prazo_maximo) | sim | ok | ok |
| regra:ccp:auto-prazo-maximo-art401-1@v1 | ccp:art401.1 | proposed (não tipável: nao_e_prazo_minimo) | não | ok | ok |
| regra:ccp:auto-prazo-maximo-art401-3@v1 | ccp:art401.3 | proposed (não tipável: nao_e_prazo_minimo) | não | ok | ok |
| regra:ccp:auto-prazo-maximo-art402-1@v1 | ccp:art402.1 | proposed (não tipável: nao_e_prazo_minimo) | não | ok | ok |
| regra:ccp:auto-prazo-maximo-art404-1@v1 | ccp:art404.1 | proposed (não tipável: nao_e_prazo_minimo) | não | ok | ok |
| regra:ccp:auto-prazo-maximo-art405-v20080730@v1 | ccp:art405 | proposed (não tipável: nao_e_prazo_minimo) | — | ok | não tipável: fonte em ccp:art405.1, que é vizinho (L1) |
| regra:ccp:auto-prazo-maximo-art405-v20210620@v1 | ccp:art405 | proposed (não tipável: nao_e_prazo_maximo) | — | ok | não tipável: fonte em ccp:art405.1.d, que é vizinho (L1) |
| regra:ccp:auto-prazo-maximo-art405-1-d@v1 | ccp:art405.1.d | proposed (não tipável: nao_e_prazo_minimo) | não | ok | ok |
| regra:ccp:auto-prazo-maximo-art405-2@v1 | ccp:art405.2 | proposed (não tipável: nao_e_prazo_minimo) | não | ok | ok |
| regra:ccp:auto-prazo-maximo-art406-b@v1 | ccp:art406.b | proposed (não tipável: nao_e_prazo_minimo) | não | ok | ok |
| regra:ccp:auto-prazo-maximo-art464-a-v20210620@v1 | ccp:art464-a | proposed (não tipável: nao_e_prazo_minimo) | — | ok | não tipável: fonte em ccp:art464-a.1, que é vizinho (L1) |
| regra:ccp:auto-prazo-maximo-art464-a-2-v20180101@v1 | ccp:art464-a.2 | proposed (não tipável: nao_e_prazo_minimo) | não | ok | ok |
| regra:ccp:auto-prazo-maximo-art464-e-2@v1 | ccp:art464-e.2 | proposed (não tipável: nao_e_prazo_minimo) | não | ok | ok |
| regra:ccp:auto-prazo-maximo-art464-e-3@v1 | ccp:art464-e.3 | proposed (não tipável: nao_e_prazo_minimo) | não | ok | ok |
| regra:ccp:auto-prazo-maximo-art464-g@v1 | ccp:art464-g | proposed (não tipável: nao_e_prazo_minimo) | não | ok | ok |
| regra:eu-1989-665:auto-prazo-minimo-art1-5@v1 | eu-1989-665:art1.5 | proposed (não tipável: sem_vocabulario) | não | ok | ok |
| regra:eu-1989-665:auto-prazo-minimo-art2-a-2@v1 | eu-1989-665:art2-a.2 | proposed (não tipável: texto_em_falta) | não | ok | ok |
| regra:eu-1989-665:auto-prazo-minimo-art2-c@v1 | eu-1989-665:art2-c | proposed (não tipável: nao_e_prazo_minimo) | — | ok | não tipável: «Prazos para interposição de recurso» não está em eu-1989-665:art2-c |
| regra:eu-1989-665:auto-prazo-minimo-art2-d-4@v1 | eu-1989-665:art2-d.4 | settled (não tipável: nao_e_prazo_minimo) | sim | ok | ok |
| regra:eu-1989-665:auto-prazo-minimo-art2-d-5@v1 | eu-1989-665:art2-d.5 | proposed (não tipável: texto_em_falta) | não | ok | ok |
| regra:eu-1989-665:auto-prazo-minimo-art2-f-1-a@v1 | eu-1989-665:art2-f.1.a | settled (não tipável: sem_vocabulario) | sim | ok | ok |
| regra:eu-1989-665:auto-prazo-maximo-art3-3@v1 | eu-1989-665:art3.3 | proposed (não tipável: nao_e_prazo_minimo) | não | ok | ok |
| regra:eu-1992-13:auto-prazo-minimo-art1-5@v1 | eu-1992-13:art1.5 | proposed (não tipável: sem_vocabulario) | não | ok | ok |
| regra:eu-1992-13:auto-prazo-minimo-art2-a-2@v1 | eu-1992-13:art2-a.2 | proposed (não tipável: texto_em_falta) | não | ok | ok |
| regra:eu-1992-13:auto-prazo-minimo-art2-c@v1 | eu-1992-13:art2-c | proposed (não tipável: texto_em_falta) | — | ok | não tipável: «Prazos para interposição de recurso» não está em eu-1992-13:art2-c |
| regra:eu-1992-13:auto-prazo-minimo-art2-d-4@v1 | eu-1992-13:art2-d.4 | proposed (não tipável: sem_vocabulario) | não | ok | ok |
| regra:eu-1992-13:auto-prazo-minimo-art2-d-5@v1 | eu-1992-13:art2-d.5 | proposed (não tipável: texto_em_falta) | não | ok | ok |
| regra:eu-1992-13:auto-prazo-minimo-art2-f-1-a@v1 | eu-1992-13:art2-f.1.a | settled (não tipável: sem_vocabulario) | sim | ok | ok |
| regra:eu-1992-13:auto-prazo-maximo-art8-3@v1 | eu-1992-13:art8.3 | proposed (não tipável: nao_e_prazo_minimo) | não | ok | ok |
| regra:eu-2004-17:auto-prazo-maximo-art15-4-v20041101@v1 | eu-2004-17:art15.4 | proposed (não tipável: sem_vocabulario) | não | ok | ok |
| regra:eu-2004-17:auto-prazo-minimo-art15-5-v20041101@v1 | eu-2004-17:art15.5 | settled (não tipável: sem_vocabulario) | sim | ok | ok |
| regra:eu-2004-17:auto-limiar-art16-a-v20160101@v1 | eu-2004-17:art16.a | sem leitura válida de leitor:a16 | — | regra 1, tipo_contrato eq bens: as fontes não nomeiam ['bens'] | ok |
| regra:eu-2004-17:auto-limiar-art16-b-v20160101@v1 | eu-2004-17:art16.b | sem leitura válida de leitor:a16 | — | regra 1: um limiar tem sempre o procedimento que permite abaixo do valor; sem ele, L12 (nao_e_limiar) | ok |
| regra:eu-2004-17:auto-limiar-art17-6-b-v20090101@v1 | eu-2004-17:art17.6.b | settled (não tipável: nao_e_limiar) | sim | ok | ok |
| regra:eu-2004-17:auto-limiar-art41-1-a-v20041101@v1 | eu-2004-17:art41.1.a | proposed (não tipável: sem_vocabulario) | não | ok | ok |
| regra:eu-2004-17:auto-limiar-art41-1-b-v20041101@v1 | eu-2004-17:art41.1.b | proposed (não tipável: texto_em_falta) | não | ok | ok |
| regra:eu-2004-17:auto-prazo-maximo-art44-3-v20041101@v1 | eu-2004-17:art44.3 | proposed (não tipável: sem_vocabulario) | não | ok | ok |
| regra:eu-2004-17:auto-prazo-minimo-art45-2-v20041101@v1 | eu-2004-17:art45.2 | settled | sim | ok | ok |
| regra:eu-2004-17:auto-prazo-minimo-art45-3-a-v20041101@v1 | eu-2004-17:art45.3.a | sem leitura válida de leitor:a16 | — | regra 1, tipo_procedimento in ['concurso_limitado_previa_qualificacao', 'procedimento_concorrencial_negociacao', 'proced | ok |
| regra:eu-2004-17:auto-prazo-minimo-art45-3-c-v20041101@v1 | eu-2004-17:art45.3.c | sem leitura válida de leitor:a16 | — | regra 1, tipo_procedimento in ['concurso_limitado_previa_qualificacao', 'procedimento_concorrencial_negociacao', 'proced | ok |
| regra:eu-2004-17:auto-prazo-minimo-art45-4-v20041101@v1 | eu-2004-17:art45.4 | sem leitura válida de leitor:a16 | — | regra 1: deadline_field prazo_propostas_dias e as fontes dizem nada (L9) | ok |
| regra:eu-2004-17:auto-prazo-maximo-art45-5-v20041101@v1 | eu-2004-17:art45.5 | sem leitura válida de leitor:a16 | — | regra 1: maximum_days 19 não está nas fontes (L8, L4) | ok |
| regra:eu-2004-17:auto-prazo-maximo-art45-6-v20041101@v1 | eu-2004-17:art45.6 | settled (não tipável: nao_e_prazo_maximo) | sim | ok | ok |
| regra:eu-2004-17:auto-prazo-minimo-art45-7-v20041101@v1 | eu-2004-17:art45.7 | proposed | não | ok | ok |
| regra:eu-2004-17:auto-prazo-minimo-art45-8-v20041101@v1 | eu-2004-17:art45.8 | proposed (não tipável: nao_e_prazo_minimo) | não | ok | ok |
| regra:eu-2004-17:auto-prazo-maximo-art46-1-v20041101@v1 | eu-2004-17:art46.1 | proposed (não tipável: nao_e_prazo_minimo) | não | ok | ok |
| regra:eu-2004-17:auto-prazo-maximo-art46-2-v20041101@v1 | eu-2004-17:art46.2 | settled (não tipável: nao_e_prazo_maximo) | sim | ok | ok |
| regra:eu-2004-17:auto-prazo-maximo-art47-3-v20041101@v1 | eu-2004-17:art47.3 | settled (não tipável: nao_e_prazo_maximo) | sim | ok | ok |
| regra:eu-2004-17:auto-prazo-maximo-art49-2-v20041101@v1 | eu-2004-17:art49.2 | settled (não tipável: nao_e_prazo_maximo) | sim | ok | ok |
| regra:eu-2004-17:auto-prazo-maximo-art49-4-v20041101@v1 | eu-2004-17:art49.4 | proposed (não tipável: sem_vocabulario) | não | ok | ok |
| regra:eu-2004-17:auto-prazo-minimo-art49-5-v20041101@v1 | eu-2004-17:art49.5 | proposed (não tipável: sem_vocabulario) | não | ok | ok |
| regra:eu-2004-17:auto-prazo-maximo-art56-4-v20041101@v1 | eu-2004-17:art56.4 | proposed (não tipável: sem_vocabulario) | não | ok | ok |
| regra:eu-2004-17:auto-limiar-art61-1-v20160101@v1 | eu-2004-17:art61.1 | sem leitura válida de leitor:a16 | — | regra 1, tipo_procedimento eq concurso_concecao: as fontes não nomeiam ['concurso_concecao'] | ok |
| regra:eu-2004-17:auto-limiar-art61-2-v20160101@v1 | eu-2004-17:art61.2 | proposed (não tipável: texto_em_falta) | não | ok | ok |
| regra:eu-2004-17:auto-limiar-art69-1-v20090807@v1 | eu-2004-17:art69.1 | proposed (não tipável: texto_em_falta) | não | ok | ok |
| regra:eu-2004-17:auto-limiar-art69-2-v20090807@v1 | eu-2004-17:art69.2 | settled (não tipável: nao_e_limiar) | sim | ok | ok |
| regra:eu-2004-18:auto-limiar-art7-a-v20160101@v1 | eu-2004-18:art7.a | sem leitura válida de leitor:a16 | — | regra 1, tipo_contrato in ['bens', 'servicos']: as fontes não nomeiam ['bens'] | ok |
| regra:eu-2004-18:auto-limiar-art7-b-v20160101@v1 | eu-2004-18:art7.b | sem leitura válida de leitor:a16 | — | regra 1, tipo_contrato in ['bens', 'servicos']: as fontes não nomeiam ['bens'] | ok |
| regra:eu-2004-18:auto-limiar-art7-c-v20160101@v1 | eu-2004-18:art7.c | sem leitura válida de leitor:a16 | — | regra 1: um limiar tem sempre o procedimento que permite abaixo do valor; sem ele, L12 (nao_e_limiar) | ok |
| regra:eu-2004-18:auto-limiar-art8-a-v20160101@v1 | eu-2004-18:art8.a | settled (não tipável: nao_e_limiar) | sim | ok | ok |
| regra:eu-2004-18:auto-limiar-art8-b-v20160101@v1 | eu-2004-18:art8.b | settled (não tipável: nao_e_limiar) | sim | ok | ok |
| regra:eu-2004-18:auto-limiar-art9-4-a-v20040430@v1 | eu-2004-18:art9.4.a | proposed (não tipável: sem_vocabulario) | não | ok | ok |
| regra:eu-2004-18:auto-limiar-art9-4-b-v20040430@v1 | eu-2004-18:art9.4.b | proposed (não tipável: texto_em_falta) | não | ok | ok |
| regra:eu-2004-18:auto-limiar-art9-5-b-v20041101@v1 | eu-2004-18:art9.5.b | proposed (não tipável: sem_vocabulario) | não | ok | ok |
| regra:eu-2004-18:auto-prazo-maximo-art33-4-v20040430@v1 | eu-2004-18:art33.4 | proposed (não tipável: sem_vocabulario) | não | ok | ok |
| regra:eu-2004-18:auto-prazo-minimo-art33-5-v20040430@v1 | eu-2004-18:art33.5 | settled (não tipável: sem_vocabulario) | sim | ok | ok |
| regra:eu-2004-18:auto-limiar-art35-1-a-v20040430@v1 | eu-2004-18:art35.1.a | proposed (não tipável: sem_vocabulario) | não | ok | ok |
| regra:eu-2004-18:auto-limiar-art35-1-b-v20040430@v1 | eu-2004-18:art35.1.b | proposed (não tipável: texto_em_falta) | não | ok | ok |
| regra:eu-2004-18:auto-prazo-maximo-art35-4-v20040430@v1 | eu-2004-18:art35.4 | settled (não tipável: nao_e_prazo_maximo) | sim | ok | ok |
| regra:eu-2004-18:auto-prazo-maximo-art36-3-v20040430@v1 | eu-2004-18:art36.3 | proposed (não tipável: sem_vocabulario) | não | ok | ok |
| regra:eu-2004-18:auto-prazo-minimo-art38-2-v20040430@v1 | eu-2004-18:art38.2 | settled | sim | ok | ok |
| regra:eu-2004-18:auto-prazo-minimo-art38-3-a-v20040430@v1 | eu-2004-18:art38.3.a | sem leitura válida de leitor:a16 | — | regra 1, tipo_procedimento eq concurso_publico: as fontes não nomeiam ['concurso_publico'] | ok |
| regra:eu-2004-18:auto-prazo-minimo-art38-3-b-v20040430@v1 | eu-2004-18:art38.3.b | settled | sim | ok | ok |
| regra:eu-2004-18:auto-prazo-minimo-art38-4-v20040430@v1 | eu-2004-18:art38.4 | sem leitura válida de leitor:a16 | — | regra 1: usual_days sem «em regra» e os dias nas fontes (L11) | ok |
| regra:eu-2004-18:auto-prazo-maximo-art38-5-v20040430@v1 | eu-2004-18:art38.5 | sem leitura válida de leitor:a16 | — | regra 1, publicado_joue eq True: as fontes não afirmam o facto (L7) | ok |
| regra:eu-2004-18:auto-prazo-maximo-art38-6-v20040430@v1 | eu-2004-18:art38.6 | proposed (não tipável: nao_e_prazo_minimo) | não | ok | ok |
| regra:eu-2004-18:auto-prazo-minimo-art38-8-a-v20040430@v1 | eu-2004-18:art38.8.a | sem leitura válida de leitor:a16 | — | regra 1: deadline_field prazo_reclamacao_dias e as fontes dizem ['prazo_candidaturas_dias'] (L9) | ok |
| regra:eu-2004-18:auto-prazo-minimo-art38-8-b-v20040430@v1 | eu-2004-18:art38.8.b | sem leitura válida de leitor:a16 | — | regra 1, tipo_procedimento in ['procedimento_negociacao', 'procedimento_concorrencial_negociacao']: as fontes não nomeia | ok |
| regra:eu-2004-18:auto-prazo-maximo-art39-1-v20040430@v1 | eu-2004-18:art39.1 | proposed (não tipável: nao_e_prazo_minimo) | não | ok | ok |
| regra:eu-2004-18:auto-prazo-maximo-art39-2-v20040430@v1 | eu-2004-18:art39.2 | proposed (não tipável: nao_e_prazo_minimo) | não | ok | ok |
| regra:eu-2004-18:auto-prazo-maximo-art40-4-v20040430@v1 | eu-2004-18:art40.4 | proposed (não tipável: sem_vocabulario) | não | ok | ok |
| regra:eu-2004-18:auto-prazo-maximo-art41-2-v20040430@v1 | eu-2004-18:art41.2 | proposed (não tipável: sem_vocabulario) | não | ok | ok |
| regra:eu-2004-18:auto-prazo-maximo-art54-4-v20040430@v1 | eu-2004-18:art54.4 | proposed (não tipável: sem_vocabulario) | não | ok | ok |
| regra:eu-2004-18:auto-limiar-art56-v20160101@v1 | eu-2004-18:art56 | proposed (não tipável: texto_em_falta) | não | ok | ok |
| regra:eu-2004-18:auto-prazo-minimo-art59-v20040430@v1 | eu-2004-18:art59 | proposed | não | ok | ok |
| regra:eu-2004-18:auto-limiar-art63-1-v20160101@v1 | eu-2004-18:art63.1 | proposed (não tipável: sem_vocabulario) | não | ok | ok |
| regra:eu-2004-18:auto-prazo-minimo-art65-v20040430@v1 | eu-2004-18:art65 | sem leitura válida de leitor:a16 | — | regra 1, tipo_procedimento in ['concurso_publico', 'concurso_limitado_previa_qualificacao', 'dialogo_concorrencial', 'pr | ok |
| regra:eu-2004-18:auto-limiar-art67-1-a-v20160101@v1 | eu-2004-18:art67.1.a | sem leitura válida de leitor:a16 | — | regra 1, tipo_contrato eq servicos: as fontes não nomeiam ['servicos'] | ok |
| regra:eu-2004-18:auto-limiar-art67-1-b-v20160101@v1 | eu-2004-18:art67.1.b | sem leitura válida de leitor:a16 | — | regra 1, tipo_contrato eq servicos: as fontes não nomeiam ['servicos'] | ok |
| regra:eu-2004-18:auto-limiar-art67-1-c-v20160101@v1 | eu-2004-18:art67.1.c | proposed (não tipável: sem_vocabulario) | não | ok | ok |
| regra:eu-2004-18:auto-limiar-art78-1-v20090807@v1 | eu-2004-18:art78.1 | proposed (não tipável: texto_em_falta) | não | ok | ok |
| regra:eu-2004-18:auto-limiar-art78-3-v20040430@v1 | eu-2004-18:art78.3 | proposed (não tipável: texto_em_falta) | não | ok | ok |
| regra:eu-2009-81:auto-limiar-art8-a@v1 | eu-2009-81:art8.a | sem leitura válida de leitor:a16 | — | regra 1, tipo_contrato eq bens: as fontes não nomeiam ['bens'] | ok |
| regra:eu-2009-81:auto-limiar-art8-b@v1 | eu-2009-81:art8.b | proposed (não tipável: sem_vocabulario) | não | ok | ok |
| regra:eu-2009-81:auto-limiar-art9-4-a@v1 | eu-2009-81:art9.4.a | proposed (não tipável: sem_vocabulario) | não | ok | ok |
| regra:eu-2009-81:auto-limiar-art9-4-b@v1 | eu-2009-81:art9.4.b | sem leitura válida de leitor:a16 | — | regra 1, tipo_contrato eq bens: as fontes não nomeiam ['bens'] | ok |
| regra:eu-2009-81:auto-limiar-art9-5-b-v20100101@v1 | eu-2009-81:art9.5.b | proposed (não tipável: sem_vocabulario) | não | ok | ok |
| regra:eu-2009-81:auto-prazo-maximo-art30-3@v1 | eu-2009-81:art30.3 | settled (não tipável: nao_e_prazo_maximo) | sim | ok | ok |
| regra:eu-2009-81:auto-prazo-maximo-art32-3@v1 | eu-2009-81:art32.3 | proposed (não tipável: sem_vocabulario) | não | ok | ok |
| regra:eu-2009-81:auto-prazo-minimo-art33-2@v1 | eu-2009-81:art33.2 | sem leitura válida de leitor:a16 | — | regra 1, tipo_procedimento in ['concurso_limitado_previa_qualificacao', 'procedimento_concorrencial_negociacao', 'dialog | ok |
| regra:eu-2009-81:auto-prazo-minimo-art33-3@v1 | eu-2009-81:art33.3 | sem leitura válida de leitor:a16 | — | regra 1, publicado_joue eq True: as fontes não afirmam o facto (L7) | ok |
| regra:eu-2009-81:auto-prazo-maximo-art33-4@v1 | eu-2009-81:art33.4 | proposed (não tipável: texto_em_falta) | não | ok | ok |
| regra:eu-2009-81:auto-prazo-maximo-art33-5@v1 | eu-2009-81:art33.5 | proposed (não tipável: nao_e_prazo_minimo) | não | ok | ok |
| regra:eu-2009-81:auto-prazo-minimo-art33-7@v1 | eu-2009-81:art33.7 | sem leitura válida de leitor:a16 | — | regra 1, publicado_joue eq True: as fontes não afirmam o facto (L7) | ok |
| regra:eu-2009-81:auto-prazo-maximo-art34-4@v1 | eu-2009-81:art34.4 | sem leitura válida de leitor:a16 | — | regra 1, tipo_procedimento in ['concurso_limitado_previa_qualificacao', 'procedimento_concorrencial_negociacao', 'proced | ok |
| regra:eu-2009-81:auto-prazo-maximo-art35-2@v1 | eu-2009-81:art35.2 | settled (não tipável: nao_e_prazo_maximo) | sim | ok | ok |
| regra:eu-2009-81:auto-prazo-maximo-art48-4@v1 | eu-2009-81:art48.4 | settled (não tipável: nao_e_prazo_maximo) | sim | ok | ok |
| regra:eu-2009-81:auto-prazo-minimo-art55-6@v1 | eu-2009-81:art55.6 | settled (não tipável: nao_e_prazo_minimo) | sim | ok | ok |
| regra:eu-2009-81:auto-prazo-minimo-art57-2@v1 | eu-2009-81:art57.2 | proposed (não tipável: sem_vocabulario) | não | ok | ok |
| regra:eu-2009-81:auto-prazo-minimo-art59@v1 | eu-2009-81:art59 | proposed (não tipável: nao_e_prazo_minimo) | — | ok | não tipável: «Prazos para interposição de recurso» não está em eu-2009-81:art59 |
| regra:eu-2009-81:auto-prazo-minimo-art60-4@v1 | eu-2009-81:art60.4 | proposed (não tipável: sem_vocabulario) | não | ok | ok |
| regra:eu-2009-81:auto-prazo-minimo-art60-5@v1 | eu-2009-81:art60.5 | proposed (não tipável: sem_vocabulario) | não | ok | ok |
| regra:eu-2009-81:auto-prazo-minimo-art62-1-a@v1 | eu-2009-81:art62.1.a | settled (não tipável: sem_vocabulario) | sim | ok | ok |
| regra:eu-2009-81:auto-prazo-maximo-art63-3@v1 | eu-2009-81:art63.3 | proposed (não tipável: nao_e_prazo_minimo) | não | ok | ok |
| regra:eu-2014-23:auto-limiar-art8-1@v1 | eu-2014-23:art8.1 | sem leitura válida de leitor:a16 | — | regra 1, tipo_contrato eq concessao_obras: as fontes não nomeiam ['concessao_obras'] | ok |
| regra:eu-2014-23:auto-limiar-art9-1@v1 | eu-2014-23:art9.1 | proposed (não tipável: texto_em_falta) | não | ok | ok |
| regra:eu-2014-23:auto-limiar-art9-2@v1 | eu-2014-23:art9.2 | proposed (não tipável: texto_em_falta) | não | ok | ok |
| regra:eu-2014-23:auto-prazo-maximo-art32-1@v1 | eu-2014-23:art32.1 | proposed (não tipável: nao_e_prazo_minimo) | não | ok | ok |
| regra:eu-2014-23:auto-prazo-maximo-art33-2@v1 | eu-2014-23:art33.2 | proposed (não tipável: sem_vocabulario) | não | ok | ok |
| regra:eu-2014-23:auto-prazo-maximo-art34-3@v1 | eu-2014-23:art34.3 | settled (não tipável: nao_e_prazo_maximo) | sim | ok | ok |
| regra:eu-2014-23:auto-prazo-minimo-art39-3@v1 | eu-2014-23:art39.3 | sem leitura válida de leitor:a16 | — | regra 1, tipo_contrato eq concessao_obras: as fontes não nomeiam ['concessao_obras'] | ok |
| regra:eu-2014-23:auto-prazo-minimo-art39-4@v1 | eu-2014-23:art39.4 | sem leitura válida de leitor:a16 | — | regra 1, tipo_contrato eq concessao_obras: as fontes não nomeiam ['concessao_obras'] | ok |
| regra:eu-2014-23:auto-prazo-maximo-art39-5@v1 | eu-2014-23:art39.5 | proposed (não tipável: texto_em_falta) | não | ok | ok |
| regra:eu-2014-23:auto-prazo-maximo-art40-1@v1 | eu-2014-23:art40.1 | proposed (não tipável: nao_e_prazo_minimo) | não | ok | ok |
| regra:eu-2014-24:auto-limiar-art4-a@v1 | eu-2014-24:art4.a | sem leitura válida de leitor:a16 | — | regra 1, tipo_entidade eq estado: as fontes não nomeiam ['estado'] | ok |
| regra:eu-2014-24:auto-limiar-art4-b@v1 | eu-2014-24:art4.b | sem leitura válida de leitor:a16 | — | regra 1, tipo_contrato in ['bens', 'servicos']: as fontes não nomeiam ['bens'] | ok |
| regra:eu-2014-24:auto-limiar-art4-c@v1 | eu-2014-24:art4.c | sem leitura válida de leitor:a16 | — | regra 1, tipo_contrato in ['bens', 'servicos_sociais']: as fontes não nomeiam ['bens', 'servicos_sociais'] | ok |
| regra:eu-2014-24:auto-limiar-art4-d@v1 | eu-2014-24:art4.d | sem leitura válida de leitor:a16 | — | regra 1, tipo_entidade eq estado: as fontes não nomeiam ['estado'] | ok |
| regra:eu-2014-24:auto-limiar-art5-10@v1 | eu-2014-24:art5.10 | proposed (não tipável: sem_vocabulario) | não | ok | ok |
| regra:eu-2014-24:auto-limiar-art6-1@v1 | eu-2014-24:art6.1 | proposed (não tipável: texto_em_falta) | não | ok | ok |
| regra:eu-2014-24:auto-limiar-art6-3@v1 | eu-2014-24:art6.3 | proposed (não tipável: texto_em_falta) | não | ok | ok |
| regra:eu-2014-24:auto-limiar-art13-a@v1 | eu-2014-24:art13.a | sem leitura válida de leitor:a16 | — | regra 1, tipo_procedimento eq concurso_publico: as fontes não nomeiam ['concurso_publico'] | ok |
| regra:eu-2014-24:auto-limiar-art13-b@v1 | eu-2014-24:art13.b | settled (não tipável: nao_e_limiar) | sim | ok | ok |
| regra:eu-2014-24:auto-prazo-minimo-art27-1@v1 | eu-2014-24:art27.1 | settled | sim | ok | ok |
| regra:eu-2014-24:auto-prazo-minimo-art27-2-b@v1 | eu-2014-24:art27.2.b | sem leitura válida de leitor:a16 | — | regra 1, anuncio_pre_informacao eq False: as fontes não negam o facto (L7) | ok |
| regra:eu-2014-24:auto-prazo-minimo-art27-3@v1 | eu-2014-24:art27.3 | sem leitura válida de leitor:a16 | — | regra 1, publicado_joue eq True: as fontes não afirmam o facto (L7) | ok |
| regra:eu-2014-24:auto-prazo-maximo-art27-4@v1 | eu-2014-24:art27.4 | proposed (não tipável: nao_e_prazo_minimo) | não | ok | ok |
| regra:eu-2014-24:auto-prazo-minimo-art28-1@v1 | eu-2014-24:art28.1 | sem leitura válida de leitor:a16 | — | regra 1: deadline_field prazo_reclamacao_dias e as fontes dizem ['prazo_candidaturas_dias'] (L9) | ok |
| regra:eu-2014-24:auto-prazo-minimo-art28-2@v1 | eu-2014-24:art28.2 | sem leitura válida de leitor:a16 | — | regra 1, tipo_procedimento eq concurso_limitado_previa_qualificacao: as fontes não nomeiam ['concurso_limitado_previa_qu | ok |
| regra:eu-2014-24:auto-prazo-minimo-art28-3-b@v1 | eu-2014-24:art28.3.b | sem leitura válida de leitor:a16 | — | regra 1, anuncio_pre_informacao eq False: as fontes não negam o facto (L7) | ok |
| regra:eu-2014-24:auto-prazo-minimo-art28-4@v1 | eu-2014-24:art28.4 | sem leitura válida de leitor:a16 | — | regra 1, tipo_procedimento eq concurso_limitado_previa_qualificacao: as fontes não nomeiam ['concurso_limitado_previa_qu | ok |
| regra:eu-2014-24:auto-prazo-maximo-art28-5@v1 | eu-2014-24:art28.5 | sem leitura válida de leitor:a16 | — | regra 1: as fontes de maximum_days não dizem um máximo («não pode ser superior a», «no prazo de», L8) | ok |
| regra:eu-2014-24:auto-prazo-minimo-art28-6-a@v1 | eu-2014-24:art28.6.a | sem leitura válida de leitor:a16 | — | regra 1, tipo_procedimento eq concurso_limitado_previa_qualificacao: as fontes não nomeiam ['concurso_limitado_previa_qu | ok |
| regra:eu-2014-24:auto-prazo-minimo-art28-6-b@v1 | eu-2014-24:art28.6.b | sem leitura válida de leitor:a16 | — | regra 1, tipo_procedimento eq concurso_limitado_previa_qualificacao: as fontes não nomeiam ['concurso_limitado_previa_qu | ok |
| regra:eu-2014-24:auto-prazo-minimo-art29-1@v1 | eu-2014-24:art29.1 | sem leitura válida de leitor:a16 | — | regra 1, tipo_procedimento eq procedimento_concorrencial_negociacao: as fontes não nomeiam ['procedimento_concorrencial_ | ok |
| regra:eu-2014-24:auto-prazo-minimo-art30-1@v1 | eu-2014-24:art30.1 | sem leitura válida de leitor:a16 | — | regra 1, tipo_procedimento eq dialogo_concorrencial: as fontes não nomeiam ['dialogo_concorrencial'] | regra 1, tipo_procedimento eq dialogo_concorrencial: as fontes não nomeiam ['dialogo_concorrencial'] |
| regra:eu-2014-24:auto-prazo-minimo-art31-1@v1 | eu-2014-24:art31.1 | sem leitura válida de leitor:a16 | — | regra 1: deadline_field prazo_reclamacao_dias e as fontes dizem ['prazo_candidaturas_dias'] (L9) | ok |
| regra:eu-2014-24:auto-prazo-minimo-art34-2-a@v1 | eu-2014-24:art34.2.a | settled (não tipável: sem_vocabulario) | sim | ok | ok |
| regra:eu-2014-24:auto-prazo-minimo-art34-2-b@v1 | eu-2014-24:art34.2.b | settled (não tipável: sem_vocabulario) | sim | ok | ok |
| regra:eu-2014-24:auto-prazo-maximo-art34-5@v1 | eu-2014-24:art34.5 | proposed (não tipável: sem_vocabulario) | não | ok | ok |
| regra:eu-2014-24:auto-prazo-maximo-art34-7@v1 | eu-2014-24:art34.7 | settled (não tipável: sem_vocabulario) | sim | ok | ok |
| regra:eu-2014-24:auto-prazo-maximo-art35-5@v1 | eu-2014-24:art35.5 | settled (não tipável: nao_e_prazo_maximo) | sim | ok | ok |
| regra:eu-2014-24:auto-prazo-minimo-art47-3-a@v1 | eu-2014-24:art47.3.a | sem leitura válida de leitor:a16 | — | regra 1, publicado_joue eq False: as fontes não negam o facto (L7) | ok |
| regra:eu-2014-24:auto-prazo-maximo-art48-2-d@v1 | eu-2014-24:art48.2.d | proposed (não tipável: sem_vocabulario) | não | ok | ok |
| regra:eu-2014-24:auto-prazo-maximo-art50-1@v1 | eu-2014-24:art50.1 | proposed (não tipável: nao_e_prazo_minimo) | não | ok | ok |
| regra:eu-2014-24:auto-prazo-maximo-art50-2@v1 | eu-2014-24:art50.2 | proposed (não tipável: texto_em_falta) | não | ok | ok |
| regra:eu-2014-24:auto-prazo-maximo-art50-3@v1 | eu-2014-24:art50.3 | proposed (não tipável: sem_vocabulario) | não | ok | ok |
| regra:eu-2014-24:auto-prazo-maximo-art51-2@v1 | eu-2014-24:art51.2 | proposed (não tipável: texto_em_falta) | não | ok | ok |
| regra:eu-2014-24:auto-prazo-maximo-art53-1@v1 | eu-2014-24:art53.1 | proposed (não tipável: texto_em_falta) | não | ok | ok |
| regra:eu-2014-24:auto-prazo-maximo-art53-2@v1 | eu-2014-24:art53.2 | proposed (não tipável: nao_e_prazo_minimo) | não | ok | ok |
| regra:eu-2014-24:auto-prazo-maximo-art55-2@v1 | eu-2014-24:art55.2 | proposed (não tipável: sem_vocabulario) | não | ok | ok |
| regra:eu-2014-24:auto-prazo-maximo-art75-2@v1 | eu-2014-24:art75.2 | settled (não tipável: nao_e_prazo_maximo) | sim | ok | ok |
| regra:eu-2014-24:auto-limiar-art83-6-a@v1 | eu-2014-24:art83.6.a | settled (não tipável: nao_e_limiar) | sim | ok | ok |
| regra:eu-2014-24:auto-limiar-art83-6-b@v1 | eu-2014-24:art83.6.b | settled (não tipável: nao_e_limiar) | sim | ok | ok |
| regra:eu-2014-25:auto-limiar-art15-a@v1 | eu-2014-25:art15.a | sem leitura válida de leitor:a16 | — | regra 1, tipo_contrato in ['bens', 'servicos', 'servicos_sociais']: as fontes não nomeiam ['servicos_sociais'] | ok |
| regra:eu-2014-25:auto-limiar-art15-b@v1 | eu-2014-25:art15.b | sem leitura válida de leitor:a16 | — | regra 1, tipo_procedimento in ['concurso_concecao']: as fontes não nomeiam ['concurso_concecao'] | ok |
| regra:eu-2014-25:auto-limiar-art15-c@v1 | eu-2014-25:art15.c | sem leitura válida de leitor:a16 | — | regra 1, tipo_procedimento in ['concurso_aberto', 'concurso_concecao', 'concurso_publico', 'dialogo_concorrencial', 'par | ok |
| regra:eu-2014-25:auto-limiar-art16-10@v1 | eu-2014-25:art16.10 | sem leitura válida de leitor:a16 | — | regra 1, tipo_procedimento eq concurso_aberto: as fontes não nomeiam ['concurso_aberto'] | ok |
| regra:eu-2014-25:auto-limiar-art17-1@v1 | eu-2014-25:art17.1 | proposed (não tipável: texto_em_falta) | não | ok | ok |
| regra:eu-2014-25:auto-limiar-art17-2@v1 | eu-2014-25:art17.2 | proposed (não tipável: texto_em_falta) | não | ok | ok |
| regra:eu-2014-25:auto-prazo-minimo-art45-1@v1 | eu-2014-25:art45.1 | proposed | não | ok | ok |
| regra:eu-2014-25:auto-prazo-minimo-art45-2-b@v1 | eu-2014-25:art45.2.b | sem leitura válida de leitor:a16 | — | regra 1, anuncio_pre_informacao eq False: as fontes não negam o facto (L7) | ok |
| regra:eu-2014-25:auto-prazo-minimo-art45-3@v1 | eu-2014-25:art45.3 | sem leitura válida de leitor:a16 | — | regra 1, publicado_joue eq True: as fontes não afirmam o facto (L7) | ok |
| regra:eu-2014-25:auto-prazo-maximo-art45-4@v1 | eu-2014-25:art45.4 | proposed (não tipável: sem_vocabulario) | — | ok | não tipável: fonte em eu-2014-25:art45.1, que é vizinho (L1) |
| regra:eu-2014-25:auto-prazo-minimo-art46-1@v1 | eu-2014-25:art46.1 | sem leitura válida de leitor:a16 | — | regra 1: deadline_field prazo_reclamacao_dias e as fontes dizem ['prazo_candidaturas_dias'] (L9) | ok |
| regra:eu-2014-25:auto-prazo-minimo-art46-2@v1 | eu-2014-25:art46.2 | proposed (não tipável: texto_em_falta) | não | ok | ok |
| regra:eu-2014-25:auto-prazo-minimo-art47-1@v1 | eu-2014-25:art47.1 | sem leitura válida de leitor:a16 | — | regra 1: deadline_field prazo_reclamacao_dias e as fontes dizem ['prazo_candidaturas_dias'] (L9) | ok |
| regra:eu-2014-25:auto-prazo-minimo-art47-2@v1 | eu-2014-25:art47.2 | proposed (não tipável: texto_em_falta) | não | ok | ok |
| regra:eu-2014-25:auto-prazo-minimo-art48-1@v1 | eu-2014-25:art48.1 | sem leitura válida de leitor:a16 | — | regra 1, tipo_procedimento eq dialogo_concorrencial: as fontes não nomeiam ['dialogo_concorrencial'] | regra 1, tipo_procedimento eq dialogo_concorrencial: as fontes não nomeiam ['dialogo_concorrencial'] |
| regra:eu-2014-25:auto-prazo-minimo-art49-1@v1 | eu-2014-25:art49.1 | sem leitura válida de leitor:a16 | — | regra 1: deadline_field prazo_reclamacao_dias e as fontes dizem ['prazo_candidaturas_dias'] (L9) | regra 1: usual_days sem «em regra» e os dias nas fontes (L11) |
| regra:eu-2014-25:auto-prazo-minimo-art52-2-a@v1 | eu-2014-25:art52.2.a | settled (não tipável: sem_vocabulario) | sim | ok | ok |
| regra:eu-2014-25:auto-prazo-minimo-art52-2-b@v1 | eu-2014-25:art52.2.b | settled (não tipável: sem_vocabulario) | sim | ok | ok |
| regra:eu-2014-25:auto-prazo-maximo-art52-5@v1 | eu-2014-25:art52.5 | proposed (não tipável: sem_vocabulario) | não | ok | ok |
| regra:eu-2014-25:auto-prazo-maximo-art52-7@v1 | eu-2014-25:art52.7 | settled (não tipável: sem_vocabulario) | sim | ok | ok |
| regra:eu-2014-25:auto-prazo-maximo-art53-5@v1 | eu-2014-25:art53.5 | settled (não tipável: nao_e_prazo_maximo) | sim | ok | ok |
| regra:eu-2014-25:auto-prazo-minimo-art66-3-a@v1 | eu-2014-25:art66.3.a | proposed (não tipável: texto_em_falta) | não | ok | ok |
| regra:eu-2014-25:auto-prazo-maximo-art67-2-d@v1 | eu-2014-25:art67.2.d | proposed (não tipável: texto_em_falta) | não | ok | ok |
| regra:eu-2014-25:auto-prazo-maximo-art70-1@v1 | eu-2014-25:art70.1 | proposed (não tipável: nao_e_prazo_minimo) | não | ok | ok |
| regra:eu-2014-25:auto-prazo-maximo-art70-2@v1 | eu-2014-25:art70.2 | proposed (não tipável: texto_em_falta) | não | ok | ok |
| regra:eu-2014-25:auto-prazo-maximo-art71-2@v1 | eu-2014-25:art71.2 | proposed (não tipável: texto_em_falta) | não | ok | ok |
| regra:eu-2014-25:auto-prazo-maximo-art73-1@v1 | eu-2014-25:art73.1 | proposed (não tipável: nao_e_prazo_minimo) | não | ok | ok |
| regra:eu-2014-25:auto-prazo-maximo-art73-2@v1 | eu-2014-25:art73.2 | proposed (não tipável: nao_e_prazo_minimo) | não | ok | ok |
| regra:eu-2014-25:auto-prazo-maximo-art75-2@v1 | eu-2014-25:art75.2 | proposed (não tipável: sem_vocabulario) | não | ok | ok |
| regra:eu-2014-25:auto-prazo-maximo-art75-5@v1 | eu-2014-25:art75.5 | proposed (não tipável: sem_vocabulario) | não | ok | ok |
| regra:eu-2014-25:auto-prazo-minimo-art75-6@v1 | eu-2014-25:art75.6 | proposed (não tipável: sem_vocabulario) | não | ok | ok |
| regra:eu-2014-25:auto-prazo-maximo-art92-2@v1 | eu-2014-25:art92.2 | settled (não tipável: nao_e_prazo_maximo) | sim | ok | ok |
| regra:eu-2014-25:auto-prazo-maximo-art96-2@v1 | eu-2014-25:art96.2 | proposed (não tipável: texto_em_falta) | não | ok | ok |
| regra:eu-2014-25:auto-limiar-art99-6-a@v1 | eu-2014-25:art99.6.a | settled (não tipável: nao_e_limiar) | sim | ok | ok |
| regra:eu-2014-25:auto-limiar-art99-6-b@v1 | eu-2014-25:art99.6.b | settled (não tipável: nao_e_limiar) | sim | ok | ok |

## regra:ccp:auto-prazo-maximo-art35-b-3@v1

- leitor:a16: não tipável (nao_e_prazo_minimo): O prazo é da própria entidade adjudicante para analisar a iniciativa, não um prazo para os interessados apresentarem algo.
- leitor:b: não tipável (nao_e_prazo_maximo): O prazo é para a própria entidade adjudicante analisar a iniciativa espontânea.

## regra:ccp:auto-prazo-maximo-art35-c-2-c@v1

- leitor:a16: não tipável (nao_e_prazo_maximo): O prazo é o de um período de teste, não um prazo para apresentar algo.
- leitor:b: não tipável (nao_e_prazo_maximo): O prazo limita a duração do período de teste, não sendo um prazo para apresentar nada.

## regra:ccp:auto-prazo-maximo-art43-v20180101@v1

- leitor:a16: não tipável (nao_e_prazo_maximo): O prazo é de apresentação do projeto de execução, não um prazo máximo para os interessados apresentarem algo.
- leitor:b: não tipável (nao_e_prazo_maximo): Os prazos de cinco dias destinam-se à própria entidade adjudicante ou ao contraente público para sanar a nulidade.
- verificador (B): não tipável: fonte em ccp:art43.10.a, que é vizinho (L1); não tipável: fonte em ccp:art43.10.b, que é vizinho (L1); não tipável: fonte em ccp:art43.10.c, que é vizinho (L1)

## regra:ccp:auto-prazo-maximo-art43-v20251028@v1

- leitor:a16: não tipável (nao_e_prazo_maximo): O prazo é de apresentação do projeto de execução, não um prazo máximo para os interessados.
- leitor:b: não tipável (nao_e_prazo_maximo): Os prazos de cinco dias são para a própria entidade adjudicante ou para o contraente público sanar a nulidade.
- verificador (B): não tipável: fonte em ccp:art43.10.a, que é vizinho (L1); não tipável: fonte em ccp:art43.10.b, que é vizinho (L1); não tipável: fonte em ccp:art43.10.c, que é vizinho (L1)

## regra:ccp:auto-prazo-maximo-art43-10-a@v1

- leitor:a16: não tipável (nao_e_prazo_maximo): O prazo de cinco dias é o da prorrogação, não um prazo máximo para os interessados apresentarem algo.
- leitor:b: não tipável (nao_e_prazo_maximo): O prazo de cinco dias destina-se à própria entidade adjudicante para juntar os elementos em falta.

## regra:ccp:auto-prazo-maximo-art43-10-b@v1

- leitor:a16: não tipável (nao_e_prazo_maximo): O prazo de cinco dias é o da própria entidade adjudicante para sanar a nulidade, não um prazo máximo para os concorrentes apresentarem propostas.
- leitor:b: não tipável (nao_e_prazo_maximo): O prazo destina-se à própria entidade adjudicante para juntar os elementos em falta.

## regra:ccp:auto-prazo-maximo-art43-10-c@v1

- leitor:a16: não tipável (nao_e_prazo_maximo): O prazo de cinco dias é o da própria entidade adjudicante para apresentar as razões que justificam a não exigência dos elementos, não um prazo máximo para os interessados.
- leitor:b: não tipável (nao_e_prazo_maximo): O prazo de cinco dias é para a própria entidade adjudicante apresentar razões.

## regra:ccp:auto-limiar-art46-a-2@v1

- leitor:a16: não tipável (nao_e_limiar): O valor não é o limite até ao qual um procedimento pode ser escolhido.
- leitor:b: não tipável (nao_e_limiar): Os valores indicados determinam a obrigação de fundamentar a não adjudicação por lotes, não um limite até ao qual um procedimento pode ser escolhido.

## regra:ccp:auto-limiar-art55-3-a@v1

- leitor:a16: não tipável (nao_e_limiar): O valor dispensa a participação nos procedimentos de formação de contratos públicos; não é o limite até ao qual um procedimento pode ser escolhido.
- leitor:b: não tipável (nao_e_limiar): O valor limita a dívida para autorizar a participação de operadores económicos, não o valor do contrato até ao qual um procedimento pode ser escolhido.

## regra:ccp:auto-prazo-maximo-art61-4-v20120811@v1

- leitor:a16: não tipável (nao_e_prazo_maximo): O período de suspensão é um máximo de mais 60 dias, não um prazo para os interessados apresentarem algo.
- leitor:b: não tipável (nao_e_prazo_maximo): O prazo limita a manutenção da suspensão pelo órgão competente, não a apresentação de elementos pelos interessados.

## regra:ccp:auto-prazo-maximo-art65@v1

- leitor:a16: não tipável (nao_e_prazo_minimo): O prazo é de manutenção das propostas já apresentadas, não um prazo para as apresentar.
- leitor:b: não tipável (nao_e_prazo_maximo): O prazo é para manter as propostas, não para apresentar algo.

## regra:ccp:auto-prazo-maximo-art72-v20180101@v1

- leitor:a16: não tipável (nao_e_prazo_maximo): O prazo de cinco dias é o máximo para o júri pedir o suprimento das irregularidades, não um prazo para os concorrentes apresentarem algo.
- leitor:b: não tipável (sem_vocabulario): O vocabulário não prevê um campo de prazo para o suprimento de irregularidades das propostas e candidaturas.

## regra:ccp:auto-prazo-maximo-art72-v20221202@v1

- leitor:a16: não tipável (nao_e_prazo_maximo): O prazo de cinco dias é o máximo para o suprimento de irregularidades, não um prazo para apresentar algo.
- leitor:b: não tipável (sem_vocabulario): O vocabulário não prevê um campo de prazo para o suprimento de irregularidades formais de candidaturas e propostas.

## regra:ccp:auto-prazo-maximo-art72-3@v1

- leitor:a16: não tipável (nao_e_prazo_maximo): O prazo é de cinco dias, o máximo para o júri pedir o suprimento de irregularidades, não um prazo para os concorrentes apresentarem algo.
- leitor:b: não tipável (sem_vocabulario): O vocabulário não contém um campo de prazo para o suprimento de irregularidades formais de candidaturas e propostas.

## regra:ccp:auto-prazo-maximo-art78-v20180101@v1

- leitor:a16: não tipável (nao_e_prazo_maximo): O prazo é da própria entidade adjudicante para publicar o anúncio da adjudicação, não um prazo máximo para os interessados apresentarem algo.
- leitor:b: não tipável (nao_e_prazo_maximo): Os prazos são para a publicação de anúncios pela entidade adjudicante, não para apresentar elementos.
- verificador (B): não tipável: fonte em ccp:art78.5, que é vizinho (L1)

## regra:ccp:auto-prazo-maximo-art78-1-v20080730@v1

- leitor:a16: não tipável (nao_e_prazo_minimo): O prazo é da própria entidade adjudicante para enviar o anúncio, não um prazo para os interessados apresentarem algo.
- leitor:b: não tipável (nao_e_prazo_maximo): O prazo é para a própria entidade adjudicante enviar um anúncio de adjudicação.

## regra:ccp:auto-prazo-maximo-art78-1@v1

- leitor:a16: não tipável (nao_e_prazo_minimo): O prazo é da própria entidade adjudicante para publicar o anúncio da adjudicação, não um prazo para os interessados apresentarem algo.
- leitor:b: não tipável (nao_e_prazo_maximo): O prazo é para a própria entidade adjudicante publicar um anúncio de adjudicação.

## regra:ccp:auto-prazo-maximo-art78-5@v1

- leitor:a16: não tipável (sem_vocabulario): A regra só vale para contratos celebrados ao abrigo de acordo-quadro ou de sistema de aquisição dinâmico, instrumentos que o vocabulário não tem.
- leitor:b: não tipável (nao_e_prazo_maximo): O prazo destina-se à publicação do anúncio pela entidade adjudicante, não à apresentação de elementos pelos interessados.

## regra:ccp:auto-prazo-maximo-art85-2@v1

- leitor:a16: não tipável (nao_e_prazo_minimo): O prazo é um máximo de prorrogação do prazo de apresentação dos documentos de habilitação, não um prazo para os apresentar.
- leitor:b: não tipável (sem_vocabulario): O vocabulário não permite representar o máximo de cinco dias da prorrogação, distinto do prazo total para apresentar os documentos de habilitação.

## regra:ccp:auto-prazo-maximo-art86-v20120811@v1

- leitor:a16: não tipável (nao_e_prazo_minimo): O prazo é máximo para o próprio órgão competente para a decisão de contratar, não para os adjudicatários apresentarem documentos.
- leitor:b: não tipável (sem_vocabulario): O vocabulário não permite representar a condição de ocorrência de um facto que determine a caducidade da adjudicação nos termos do n.º 1.
- verificador (B): não tipável: fonte em ccp:art86.2, que é vizinho (L1)

## regra:ccp:auto-prazo-maximo-art86-2-v20091007@v1

- leitor:a16: não tipável (nao_e_prazo_minimo): O prazo é máximo para o próprio órgão competente para a decisão de contratar, não um prazo para os interessados apresentarem algo.
- leitor:b: não tipável (sem_vocabulario): O vocabulário não permite representar a condição de ocorrência de um facto que determine a caducidade da adjudicação nos termos do n.º 1.

## regra:ccp:auto-prazo-maximo-art86-3@v1

- leitor:a16: não tipável (nao_e_prazo_minimo): O prazo é máximo para a própria entidade adjudicante fixar o prazo de pronúncia, não um prazo para o adjudicatário apresentar algo.
- leitor:b: não tipável (sem_vocabulario): Falta no vocabulário uma condição que represente a ocorrência de um facto que determine a caducidade da adjudicação nos termos do n.º 2.

## regra:ccp:auto-prazo-maximo-art87-a-2@v1

- leitor:a16: não tipável (nao_e_prazo_maximo): O prazo é de cinco dias, máximo do órgão competente para a decisão de contratar, para que o adjudicatário se pronuncie, e não um prazo para apresentar algo.
- leitor:b: não tipável (sem_vocabulario): Falta um campo para representar a condição de caducidade da adjudicação fundada nas situações indicadas.

## regra:ccp:auto-prazo-maximo-art90-1@v1

- leitor:a16: não tipável (nao_e_prazo_minimo): O prazo é de 10 dias para prestar a caução, não um máximo para apresentar algo.
- leitor:b: {"tipo": "prazo_maximo", "condicoes": [], "params": {"maximum_days": 10, "deadline_field": "prazo_caucao_dias", "counted_from": "data_notificacao"}}

## regra:ccp:auto-prazo-maximo-art91-2@v1

- leitor:a16: não tipável (nao_e_prazo_maximo): O prazo é de cinco dias, máximo do órgão competente para a decisão de contratar, para que o adjudicatário se pronuncie, e não um prazo para apresentar algo.
- leitor:b: não tipável (sem_vocabulario): O vocabulário não permite representar a condição de não prestação da caução pelo adjudicatário por facto que lhe seja imputável.

## regra:ccp:auto-prazo-maximo-art93-2@v1

- leitor:a16: não tipável (nao_e_prazo_maximo): O prazo é de cinco dias, máximo para a própria entidade adjudicante notificar, e não um prazo para os interessados apresentarem algo.
- leitor:b: não tipável (sem_vocabulario): Falta um campo que permita condicionar o prazo à não confirmação dos compromissos pelo adjudicatário no prazo fixado ou até ao termo da respetiva prorrogação.

## regra:ccp:auto-prazo-maximo-art95-v20080730@v1

- leitor:a16: não tipável (nao_e_prazo_maximo): O prazo é de redução do contrato a escrito, não um prazo máximo para apresentar algo.
- leitor:b: não tipável (nao_e_prazo_maximo): O prazo máximo respeita ao fornecimento dos bens ou à prestação dos serviços, não à apresentação de elementos.
- verificador (B): não tipável: fonte em ccp:art95.1.c.i, que é vizinho (L1)

## regra:ccp:auto-limiar-art95-1-a@v1

- leitor:a16: {"tipo": "limiar", "condicoes": [{"field": "tipo_contrato", "op": "in", "value": ["bens", "servicos"]}, {"field": "tipo_procedimento", "op": "eq", "value": "ajuste_direto"}], "params": {"threshold": {"field": "preco_contratual", "comparator": "le", "value": 30000, "currency": "EUR"}}}
- leitor:b: não tipável (nao_e_limiar): O valor dispensa a redução do contrato a escrito, não fixa um limite para a escolha de um procedimento.
- verificador (A): regra 1, tipo_procedimento eq ajuste_direto: as fontes não nomeiam ['ajuste_direto']

## regra:ccp:auto-prazo-maximo-art95-1-c-i@v1

- leitor:a16: não tipável (sem_vocabulario): A regra é de um contrato de fornecimento de bens ou prestação de serviços que se extingue em 20 dias, prazo que o vocabulário não tem.
- leitor:b: não tipável (nao_e_prazo_maximo): O prazo é para o fornecimento dos bens ou a prestação dos serviços, não para apresentar algo.

## regra:ccp:auto-limiar-art95-1-d@v1

- leitor:a16: não tipável (nao_e_limiar): O valor dispensa a redução do contrato a escrito; não é o limite até ao qual um procedimento pode ser escolhido.
- leitor:b: não tipável (nao_e_limiar): O valor dispensa a redução do contrato a escrito; não fixa um limite para a escolha de um procedimento.

## regra:ccp:auto-prazo-maximo-art95-3@v1

- leitor:a16: não tipável (nao_e_prazo_minimo): O prazo é de 10 dias, e não um máximo para os interessados apresentarem algo.
- leitor:b: não tipável (nao_e_prazo_maximo): A passagem fixa um prazo mínimo de espera para iniciar a execução do contrato, não um prazo máximo para apresentar algo.

## regra:ccp:auto-prazo-maximo-art101@v1

- leitor:a16: não tipável (nao_e_prazo_minimo): O prazo é da própria entidade adjudicante para decidir, não um prazo para os interessados apresentarem algo.
- leitor:b: {"tipo": "prazo_maximo", "condicoes": [{"field": "tipo_procedimento", "op": "not_in", "value": ["ajuste_direto", "consulta_previa"]}], "params": {"maximum_days": 5, "deadline_field": "prazo_reclamacao_dias", "counted_from": "data_notificacao"}} || {"tipo": "prazo_maximo", "condicoes": [{"field": "tipo_procedimento", "op": "in", "value": ["ajuste_direto", "consulta_previa"]}], "params": {"maximum_days": 2, "deadline_field": "prazo_reclamacao_dias", "counted_from": "data_notificacao"}}
- verificador (B): regra 1: as fontes de maximum_days não dizem um máximo («não pode ser superior a», «no prazo de», L8); regra 2: as fontes de maximum_days não dizem um máximo («não pode ser superior a», «no prazo de», L8)

## regra:ccp:auto-prazo-maximo-art102-v20080730@v1

- leitor:a16: não tipável (nao_e_prazo_minimo): O prazo é o da ordem dos documentos no contrato, não um prazo para apresentar algo.
- leitor:b: não tipável (nao_e_prazo_maximo): O prazo é para a própria entidade adjudicante notificar a decisão sobre a reclamação.
- verificador (B): não tipável: fonte em ccp:art102.2, que é vizinho (L1)

## regra:ccp:auto-prazo-maximo-art102-2@v1

- leitor:a16: não tipável (nao_e_prazo_minimo): O prazo é da própria entidade adjudicante para notificar a decisão, não um prazo para apresentar algo.
- leitor:b: não tipável (nao_e_prazo_maximo): O prazo é para a própria entidade adjudicante notificar o adjudicatário da sua decisão.

## regra:ccp:auto-prazo-minimo-art104-v20080730@v1

- leitor:a16: não tipável (nao_e_prazo_minimo): O prazo é da própria entidade adjudicante para outorgar o contrato, não um prazo para os interessados apresentarem algo.
- leitor:b: não tipável (nao_e_prazo_minimo): Os prazos regulam a outorga do contrato e a sua comunicação pela entidade adjudicante, não a apresentação de elementos.
- verificador (B): não tipável: fonte em ccp:art104.1, que é vizinho (L1); não tipável: fonte em ccp:art104.1.a, que é vizinho (L1); não tipável: fonte em ccp:art104.3, que é vizinho (L1)

## regra:ccp:auto-prazo-maximo-art104-1-a@v1

- leitor:a16: não tipável (nao_e_prazo_minimo): O prazo é da própria entidade adjudicante para outorgar o contrato, não um prazo para os interessados apresentarem algo.
- leitor:b: não tipável (nao_e_prazo_maximo): A passagem fixa um período mínimo de espera para a outorga do contrato, não um prazo máximo para apresentar algo.

## regra:ccp:auto-prazo-maximo-art108-1-v20080730@v1

- leitor:a16: não tipável (nao_e_prazo_minimo): O prazo é da própria entidade adjudicante para enviar o relatório, não um prazo para os interessados apresentarem algo.
- leitor:b: não tipável (nao_e_prazo_maximo): O prazo é para a própria entidade adjudicante enviar o relatório de contratação.

## regra:ccp:auto-prazo-maximo-art115-1-j-v20180101@v1

- leitor:a16: não tipável (nao_e_prazo_maximo): O prazo é o máximo de cinco dias para a apresentação dos documentos de habilitação, não um prazo para apresentar algo.
- leitor:b: {"tipo": "prazo_maximo", "condicoes": [{"field": "tipo_procedimento", "op": "in", "value": ["ajuste_direto", "consulta_previa"]}], "params": {"maximum_days": 5, "deadline_field": "prazo_habilitacao_dias", "counted_from": "nao_indicado"}}

## regra:ccp:auto-prazo-maximo-art115-1-k@v1

- leitor:a16: não tipável (nao_e_prazo_maximo): O prazo é o máximo de dias que o adjudicatário tem para apresentar os documentos de habilitação, não um prazo para apresentar algo.
- leitor:b: {"tipo": "prazo_maximo", "condicoes": [{"field": "tipo_procedimento", "op": "in", "value": ["ajuste_direto", "consulta_previa"]}], "params": {"maximum_days": 5, "deadline_field": "prazo_habilitacao_dias", "counted_from": "nao_indicado"}}

## regra:ccp:auto-prazo-maximo-art122-v20180101@v1

- leitor:a16: não tipável (nao_e_prazo_minimo): O prazo de três dias é do próprio júri para elaborar o relatório preliminar, não um prazo para os concorrentes apresentarem algo.
- leitor:b: não tipável (nao_e_prazo_maximo): O prazo destina-se à elaboração do relatório preliminar pelo júri, não à apresentação de elementos pelos interessados.
- verificador (B): não tipável: fonte em ccp:art122.1, que é vizinho (L1)

## regra:ccp:auto-prazo-maximo-art122-1@v1

- leitor:a16: não tipável (nao_e_prazo_minimo): O prazo é do próprio júri para elaborar o relatório preliminar, não um prazo para os concorrentes apresentarem algo.
- leitor:b: não tipável (nao_e_prazo_maximo): O prazo destina-se à elaboração do relatório preliminar pelo júri, não à apresentação de elementos pelos interessados.

## regra:ccp:auto-prazo-maximo-art129-a-6@v1

- leitor:a16: não tipável (nao_e_prazo_maximo): O prazo é um máximo para a própria estipulação e redução a escrito, não um prazo para os interessados apresentarem algo.
- leitor:b: não tipável (nao_e_prazo_maximo): O prazo respeita à estipulação e redução a escrito, não à apresentação de elementos.

## regra:ccp:auto-prazo-minimo-art135-1-v20080730@v1

- leitor:a16: {"tipo": "prazo_minimo", "condicoes": [{"field": "publicado_joue", "op": "eq", "value": false}, {"field": "tipo_contrato", "op": "ne", "value": "obras"}, {"field": "tipo_procedimento", "op": "eq", "value": "concurso_publico"}], "params": {"minimum_days": 9, "deadline_field": "prazo_propostas_dias", "counted_from": "data_envio_anuncio", "usual_days": null}} || {"tipo": "prazo_minimo", "condicoes": [{"field": "publicado_joue", "op": "eq", "value": false}, {"field": "tipo_contrato", "op": "eq", "value": "obras"}, {"field": "tipo_procedimento", "op": "eq", "value": "concurso_publico"}], "params": {"minimum_days": 20, "deadline_field": "prazo_propostas_dias", "counted_from": "data_envio_anuncio", "usual_days": null}}
- leitor:b: {"tipo": "prazo_minimo", "condicoes": [{"field": "publicado_joue", "op": "eq", "value": false}, {"field": "tipo_contrato", "op": "ne", "value": "obras"}, {"field": "tipo_procedimento", "op": "eq", "value": "concurso_publico"}], "params": {"minimum_days": 9, "deadline_field": "prazo_propostas_dias", "counted_from": "data_envio_anuncio", "usual_days": null}} || {"tipo": "prazo_minimo", "condicoes": [{"field": "publicado_joue", "op": "eq", "value": false}, {"field": "tipo_contrato", "op": "eq", "value": "obras"}, {"field": "tipo_procedimento", "op": "eq", "value": "concurso_publico"}], "params": {"minimum_days": 20, "deadline_field": "prazo_propostas_dias", "counted_from": "data_envio_anuncio", "usual_days": null}}

## regra:ccp:auto-prazo-minimo-art135-2-v20080730@v1

- leitor:a16: {"tipo": "prazo_minimo", "condicoes": [{"field": "publicado_joue", "op": "eq", "value": false}, {"field": "tipo_contrato", "op": "eq", "value": "obras"}, {"field": "tipo_procedimento", "op": "eq", "value": "concurso_publico"}, {"field": "urgencia_fundamentada", "op": "eq", "value": false}], "params": {"minimum_days": 19, "deadline_field": "prazo_propostas_dias", "counted_from": "data_envio_anuncio", "usual_days": null}} || {"tipo": "prazo_minimo", "condicoes": [{"field": "publicado_joue", "op": "eq", "value": false}, {"field": "tipo_contrato", "op": "ne", "value": "obras"}, {"field": "tipo_procedimento", "op": "eq", "value": "concurso_publico"}, {"field": "urgencia_fundamentada", "op": "eq", "value": false}], "params": {"minimum_days": 9, "deadline_field": "prazo_propostas_dias", "counted_from": "data_envio_anuncio", "usual_days": null}}
- leitor:b: não tipável (sem_vocabulario): Falta no vocabulário uma condição para a manifesta simplicidade dos trabalhos necessários à realização da obra.
- verificador (A): regra 1, urgencia_fundamentada eq False: as fontes não negam o facto (L7); regra 1: minimum_days 19 não está nas fontes (L8, L4); regra 2, urgencia_fundamentada eq False: as fontes não negam o facto (L7)

## regra:ccp:auto-prazo-minimo-art136-1-v20080730@v1

- leitor:a16: {"tipo": "prazo_minimo", "condicoes": [{"field": "publicado_joue", "op": "eq", "value": true}, {"field": "tipo_procedimento", "op": "eq", "value": "concurso_publico"}], "params": {"minimum_days": 47, "deadline_field": "prazo_propostas_dias", "counted_from": "data_envio_anuncio", "usual_days": null}}
- leitor:b: {"tipo": "prazo_minimo", "condicoes": [{"field": "publicado_joue", "op": "eq", "value": true}, {"field": "tipo_procedimento", "op": "eq", "value": "concurso_publico"}], "params": {"minimum_days": 47, "deadline_field": "prazo_propostas_dias", "counted_from": "data_envio_anuncio", "usual_days": null}}
- verificador (A): regra 1, publicado_joue eq True: as fontes não afirmam o facto (L7)

## regra:ccp:auto-prazo-minimo-art136-2-a-v20080730@v1

- leitor:a16: não tipável (sem_vocabulario): A antecedência mínima e a duração máxima são contadas em meses, unidade que o vocabulário não tem.
- leitor:b: não tipável (sem_vocabulario): O vocabulário não permite representar a antecedência exigida entre o envio do anúncio de pré-informação ou periódico indicativo e o envio do anúncio do concurso.

## regra:ccp:auto-prazo-minimo-art136-3-v20080730@v1

- leitor:a16: {"tipo": "prazo_minimo", "condicoes": [{"field": "publicado_joue", "op": "eq", "value": true}, {"field": "tipo_procedimento", "op": "eq", "value": "concurso_publico"}], "params": {"minimum_days": 7, "deadline_field": "prazo_propostas_dias", "counted_from": "data_envio_anuncio", "usual_days": null}}
- leitor:b: não tipável (sem_vocabulario): O vocabulário não permite representar a condição de preparação e envio do anúncio por meios electrónicos conforme o formato e as modalidades de transmissão indicados.

## regra:ccp:auto-prazo-minimo-art136-4-v20080730@v1

- leitor:a16: {"tipo": "prazo_minimo", "condicoes": [{"field": "setores_especiais", "op": "eq", "value": true}, {"field": "tipo_procedimento", "op": "eq", "value": "concurso_publico"}], "params": {"minimum_days": 22, "deadline_field": "prazo_propostas_dias", "counted_from": "data_envio_anuncio", "usual_days": null}}
- leitor:b: não tipável (sem_vocabulario): O vocabulário não permite representar a condição de preparação e envio do anúncio por meios electrónicos conforme o formato e as modalidades exigidos.
- verificador (A): regra 1: counted_from data_envio_anuncio e as fontes dizem nada (L9)

## regra:ccp:auto-prazo-maximo-art138-3@v1

- leitor:a16: não tipável (nao_e_prazo_minimo): Os três dias são o prazo para reclamar, não um prazo máximo para apresentar algo.
- leitor:b: não tipável (sem_vocabulario): O vocabulário não prevê a condição de o interessado não ter sido incluído na lista dos concorrentes nem o início da contagem na publicitação dessa lista.

## regra:ccp:auto-prazo-minimo-art147-v20180101@v1

- leitor:a16: {"tipo": "prazo_minimo", "condicoes": [{"field": "tipo_procedimento", "op": "eq", "value": "concurso_publico"}], "params": {"minimum_days": 5, "deadline_field": "prazo_pronuncia_dias", "counted_from": "nao_indicado", "usual_days": null}}
- leitor:b: {"tipo": "prazo_minimo", "condicoes": [{"field": "tipo_procedimento", "op": "eq", "value": "concurso_publico"}], "params": {"minimum_days": 5, "deadline_field": "prazo_pronuncia_dias", "counted_from": "nao_indicado", "usual_days": null}}

## regra:ccp:auto-limiar-art155-a@v1

- leitor:a16: {"tipo": "limiar", "condicoes": [{"field": "tipo_contrato", "op": "eq", "value": "bens"}, {"field": "tipo_procedimento", "op": "eq", "value": "concurso_publico_urgente"}], "params": {"threshold": {"field": "valor_estimado", "comparator": "le", "value": 300000, "currency": "EUR"}}} || {"tipo": "limiar", "condicoes": [{"field": "tipo_contrato", "op": "eq", "value": "servicos"}, {"field": "tipo_procedimento", "op": "eq", "value": "concurso_publico_urgente"}], "params": {"threshold": {"field": "valor_estimado", "comparator": "le", "value": 300000, "currency": "EUR"}}} || {"tipo": "limiar", "condicoes": [{"field": "tipo_contrato", "op": "eq", "value": "obras"}, {"field": "tipo_procedimento", "op": "eq", "value": "concurso_publico_urgente"}], "params": {"threshold": {"field": "valor_estimado", "comparator": "le", "value": 300000, "currency": "EUR"}}}
- leitor:b: não tipável (texto_em_falta): Faltam os montantes dos limiares do artigo 474.º aplicáveis à locação ou aquisição de bens móveis e à aquisição de serviços.
- verificador (A): regra 1, tipo_procedimento eq concurso_publico_urgente: as fontes não nomeiam ['concurso_publico_urgente']; regra 2, tipo_procedimento eq concurso_publico_urgente: as fontes não nomeiam ['concurso_publico_urgente']; regra 3, tipo_procedimento eq concurso_publico_urgente: as fontes não nomeiam ['concurso_publico_urgente']

## regra:ccp:auto-prazo-maximo-art159@v1

- leitor:a16: não tipável (nao_e_prazo_minimo): O prazo é um máximo, não um mínimo.
- leitor:b: não tipável (nao_e_prazo_maximo): O prazo refere-se à manutenção das propostas, não à apresentação de algo.

## regra:ccp:auto-prazo-maximo-art161@v1

- leitor:a16: não tipável (nao_e_prazo_minimo): O prazo é da própria entidade adjudicante para apresentar os documentos de habilitação, e não um prazo para os interessados apresentarem algo.
- leitor:b: {"tipo": "prazo_maximo", "condicoes": [{"field": "tipo_procedimento", "op": "eq", "value": "concurso_publico_urgente"}], "params": {"maximum_days": 2, "deadline_field": "prazo_habilitacao_dias", "counted_from": "data_notificacao"}}

## regra:ccp:auto-prazo-maximo-art161-b-1-b@v1

- leitor:a16: não tipável (nao_e_prazo_minimo): O prazo é de três dias, um máximo para a própria entidade adjudicante, e não um prazo para os concorrentes apresentarem algo.
- leitor:b: não tipável (nao_e_prazo_maximo): A passagem autoriza a redução do prazo para três dias, mas não fixa um prazo máximo.

## regra:ccp:auto-prazo-maximo-art161-b-4@v1

- leitor:a16: {"tipo": "prazo_maximo", "condicoes": [], "params": {"maximum_days": 3, "deadline_field": "prazo_reclamacao_dias", "counted_from": "nao_indicado"}}
- leitor:b: não tipável (sem_vocabulario): O vocabulário não contém campos de prazo para apresentação de impugnações, pronúncia dos contrainteressados ou decisão de impugnações administrativas.
- verificador (A): regra 1: as fontes de maximum_days não dizem um máximo («não pode ser superior a», «no prazo de», L8); regra 1: deadline_field prazo_reclamacao_dias e as fontes dizem nada (L9)

## regra:ccp:auto-prazo-minimo-art173@v1

- leitor:a16: {"tipo": "prazo_minimo", "condicoes": [{"field": "publicado_joue", "op": "eq", "value": false}, {"field": "tipo_procedimento", "op": "eq", "value": "concurso_limitado_previa_qualificacao"}], "params": {"minimum_days": 6, "deadline_field": "prazo_candidaturas_dias", "counted_from": "data_envio_anuncio", "usual_days": null}}
- leitor:b: {"tipo": "prazo_minimo", "condicoes": [{"field": "publicado_joue", "op": "eq", "value": false}, {"field": "tipo_procedimento", "op": "eq", "value": "concurso_limitado_previa_qualificacao"}], "params": {"minimum_days": 6, "deadline_field": "prazo_candidaturas_dias", "counted_from": "data_envio_anuncio", "usual_days": null}}
- verificador (A): regra 1: counted_from data_envio_anuncio e as fontes dizem nada (L9)

## regra:ccp:auto-prazo-minimo-art174-v20180101@v1

- leitor:a16: {"tipo": "prazo_minimo", "condicoes": [{"field": "publicado_joue", "op": "eq", "value": true}, {"field": "setores_especiais", "op": "eq", "value": true}, {"field": "tipo_procedimento", "op": "eq", "value": "concurso_limitado_previa_qualificacao"}], "params": {"minimum_days": 30, "deadline_field": "prazo_candidaturas_dias", "counted_from": "data_envio_anuncio", "usual_days": null}} || {"tipo": "prazo_minimo", "condicoes": [{"field": "publicado_joue", "op": "eq", "value": true}, {"field": "setores_especiais", "op": "eq", "value": true}, {"field": "tipo_procedimento", "op": "eq", "value": "concurso_limitado_previa_qualificacao"}, {"field": "urgencia_fundamentada", "op": "eq", "value": true}], "params": {"minimum_days": 15, "deadline_field": "prazo_candidaturas_dias", "counted_from": "data_envio_anuncio", "usual_days": null}}
- leitor:b: {"tipo": "prazo_minimo", "condicoes": [{"field": "publicado_joue", "op": "eq", "value": true}, {"field": "tipo_procedimento", "op": "eq", "value": "concurso_limitado_previa_qualificacao"}], "params": {"minimum_days": 30, "deadline_field": "prazo_candidaturas_dias", "counted_from": "data_envio_anuncio", "usual_days": null}} || {"tipo": "prazo_minimo", "condicoes": [{"field": "publicado_joue", "op": "eq", "value": true}, {"field": "tipo_procedimento", "op": "eq", "value": "concurso_limitado_previa_qualificacao"}, {"field": "urgencia_fundamentada", "op": "eq", "value": true}], "params": {"minimum_days": 15, "deadline_field": "prazo_candidaturas_dias", "counted_from": "data_envio_anuncio", "usual_days": null}} || {"tipo": "prazo_minimo", "condicoes": [{"field": "publicado_joue", "op": "eq", "value": true}, {"field": "setores_especiais", "op": "eq", "value": true}, {"field": "tipo_procedimento", "op": "eq", "value": "concurso_limitado_previa_qualificacao"}], "params": {"minimum_days": 15, "deadline_field": "prazo_candidaturas_dias", "counted_from": "data_envio_anuncio", "usual_days": 30}}
- verificador (B): regra 1, tipo_procedimento eq concurso_limitado_previa_qualificacao: fonte em ccp:art174.1, que é vizinho (L1); regra 1, publicado_joue eq True: fonte em ccp:art174.1, que é vizinho (L1); regra 1, minimum_days: fonte em ccp:art174.1, que é vizinho (L1); regra 1, deadline_field: fonte em ccp:art174.1, que é vizinho (L1); regra 1, counted_from: fonte em ccp:art174.1, que é vizinho (L1); regra 2, tipo_procedimento eq concurso_limitado_previa_qualificacao: fonte em ccp:art174.1, que é vizinho (L1)

## regra:ccp:auto-prazo-minimo-art174-1-v20080730@v1

- leitor:a16: {"tipo": "prazo_minimo", "condicoes": [{"field": "publicado_joue", "op": "eq", "value": true}, {"field": "tipo_procedimento", "op": "eq", "value": "concurso_limitado_previa_qualificacao"}], "params": {"minimum_days": 37, "deadline_field": "prazo_candidaturas_dias", "counted_from": "data_envio_anuncio", "usual_days": null}} || {"tipo": "prazo_minimo", "condicoes": [{"field": "publicado_joue", "op": "eq", "value": true}, {"field": "tipo_contrato", "op": "eq", "value": "concessao_obras"}], "params": {"minimum_days": 52, "deadline_field": "prazo_candidaturas_dias", "counted_from": "data_envio_anuncio", "usual_days": null}}
- leitor:b: {"tipo": "prazo_minimo", "condicoes": [{"field": "publicado_joue", "op": "eq", "value": true}, {"field": "tipo_contrato", "op": "ne", "value": "concessao_obras"}, {"field": "tipo_procedimento", "op": "eq", "value": "concurso_limitado_previa_qualificacao"}], "params": {"minimum_days": 37, "deadline_field": "prazo_candidaturas_dias", "counted_from": "data_envio_anuncio", "usual_days": null}} || {"tipo": "prazo_minimo", "condicoes": [{"field": "publicado_joue", "op": "eq", "value": true}, {"field": "tipo_contrato", "op": "eq", "value": "concessao_obras"}, {"field": "tipo_procedimento", "op": "eq", "value": "concurso_limitado_previa_qualificacao"}], "params": {"minimum_days": 52, "deadline_field": "prazo_candidaturas_dias", "counted_from": "data_envio_anuncio", "usual_days": null}}
- verificador (A): regra 1, publicado_joue eq True: as fontes não afirmam o facto (L7); regra 2, publicado_joue eq True: as fontes não afirmam o facto (L7)

## regra:ccp:auto-prazo-minimo-art174-2-v20080730@v1

- leitor:a16: {"tipo": "prazo_minimo", "condicoes": [{"field": "anuncio_pre_informacao", "op": "eq", "value": true}, {"field": "publicado_joue", "op": "eq", "value": true}, {"field": "tipo_procedimento", "op": "eq", "value": "concurso_limitado_previa_qualificacao"}], "params": {"minimum_days": 37, "deadline_field": "prazo_candidaturas_dias", "counted_from": "data_envio_convite", "usual_days": null}}
- leitor:b: {"tipo": "prazo_minimo", "condicoes": [{"field": "anuncio_pre_informacao", "op": "eq", "value": true}, {"field": "publicado_joue", "op": "eq", "value": true}, {"field": "tipo_procedimento", "op": "eq", "value": "concurso_limitado_previa_qualificacao"}], "params": {"minimum_days": 37, "deadline_field": "prazo_candidaturas_dias", "counted_from": "data_envio_convite", "usual_days": null}}
- verificador (A): regra 1, publicado_joue eq True: as fontes não afirmam o facto (L7); regra 1: counted_from data_envio_convite e as fontes dizem nada (L9)

## regra:ccp:auto-prazo-minimo-art174-3-v20080730@v1

- leitor:a16: {"tipo": "prazo_minimo", "condicoes": [{"field": "publicado_joue", "op": "eq", "value": true}, {"field": "tipo_contrato", "op": "not_in", "value": ["concessao_obras", "concessao_servicos"]}, {"field": "tipo_procedimento", "op": "eq", "value": "concurso_limitado_previa_qualificacao"}], "params": {"minimum_days": 29, "deadline_field": "prazo_candidaturas_dias", "counted_from": "data_envio_anuncio", "usual_days": null}}
- leitor:b: não tipável (sem_vocabulario): O vocabulário não permite representar a condição relativa à preparação e ao envio dos anúncios por meios electrónicos no formato e nas modalidades indicados no portal referido.
- verificador (A): regra 1, tipo_contrato not_in ['concessao_obras', 'concessao_servicos']: as fontes não nomeiam ['concessao_servicos']; regra 1: minimum_days 29 não está nas fontes (L8, L4); regra 1: counted_from data_envio_anuncio e as fontes dizem ['data_envio_convite'] (L9)

## regra:ccp:auto-prazo-minimo-art174-4@v1

- leitor:a16: não tipável (texto_em_falta): Os dias de prorrogação estão no n.º 1 e no n.º 3 do artigo 174.º, que não estão mostrados.
- leitor:b: não tipável (sem_vocabulario): O vocabulário não permite representar a condição de as peças procedimentais não poderem ser disponibilizadas sem restrições de acesso.

## regra:ccp:auto-prazo-maximo-art177-3@v1

- leitor:a16: não tipável (nao_e_prazo_minimo): O prazo de três dias é o da própria entidade adjudicante para publicitar a lista, não um prazo para os interessados apresentarem algo.
- leitor:b: não tipável (sem_vocabulario): O vocabulário não prevê a condição de o interessado não ter sido incluído na lista dos candidatos nem a contagem desde a publicitação dessa lista.

## regra:ccp:auto-prazo-maximo-art187-1-v20080730@v1

- leitor:a16: não tipável (nao_e_prazo_minimo): O prazo é da própria entidade adjudicante para tomar a decisão de qualificação, não um prazo para os candidatos apresentarem algo.
- leitor:b: não tipável (nao_e_prazo_maximo): O prazo é para a própria entidade adjudicante tomar e notificar a decisão de qualificação.

## regra:ccp:auto-prazo-maximo-art187-1-v20180101@v1

- leitor:a16: não tipável (nao_e_prazo_minimo): O prazo é um máximo do órgão competente para a decisão de qualificar, não um prazo mínimo para os candidatos apresentarem algo.
- leitor:b: não tipável (nao_e_prazo_maximo): O prazo é para a própria entidade adjudicante tomar e notificar a decisão de qualificação.

## regra:ccp:auto-prazo-maximo-art187-1@v1

- leitor:a16: não tipável (nao_e_prazo_minimo): O prazo é um máximo para a própria entidade adjudicante tomar a decisão de qualificação, e não um prazo para os candidatos apresentarem algo.
- leitor:b: não tipável (nao_e_prazo_maximo): O prazo é para a própria entidade adjudicante tomar e notificar a decisão de qualificação.

## regra:ccp:auto-prazo-minimo-art187-2-v20180101@v1

- leitor:a16: não tipável (nao_e_prazo_minimo): O prazo é um mínimo para os candidatos apresentarem documentos, não um prazo para apresentarem algo.
- leitor:b: não tipável (sem_vocabulario): O vocabulário não prevê um campo de prazo para apresentar documentos comprovativos dos requisitos de capacidade técnica e financeira nem para confirmar compromissos de terceiras entidades.

## regra:ccp:auto-prazo-maximo-art187-4-v20180101@v1

- leitor:a16: não tipável (nao_e_prazo_minimo): O prazo é fixado pela entidade adjudicante para que o candidato se pronuncie, e não é um prazo para os candidatos apresentarem algo.
- leitor:b: não tipável (sem_vocabulario): O vocabulário não permite representar a ocorrência de um facto que determine a caducidade da qualificação.

## regra:ccp:auto-prazo-maximo-art188-4@v1

- leitor:a16: não tipável (nao_e_prazo_minimo): O prazo é máximo, não mínimo: os cinco dias são o máximo para a pronúncia dos candidatos.
- leitor:b: não tipável (sem_vocabulario): O vocabulário não permite representar a ocorrência de um facto que determine a caducidade da qualificação.

## regra:ccp:auto-prazo-minimo-art190-1-v20080730@v1

- leitor:a16: {"tipo": "prazo_minimo", "condicoes": [{"field": "publicado_joue", "op": "eq", "value": false}, {"field": "tipo_contrato", "op": "eq", "value": "obras"}, {"field": "tipo_procedimento", "op": "eq", "value": "concurso_limitado_previa_qualificacao"}], "params": {"minimum_days": 20, "deadline_field": "prazo_propostas_dias", "counted_from": "data_envio_convite", "usual_days": null}} || {"tipo": "prazo_minimo", "condicoes": [{"field": "publicado_joue", "op": "eq", "value": false}, {"field": "tipo_contrato", "op": "ne", "value": "obras"}, {"field": "tipo_procedimento", "op": "eq", "value": "concurso_limitado_previa_qualificacao"}], "params": {"minimum_days": 9, "deadline_field": "prazo_propostas_dias", "counted_from": "data_envio_convite", "usual_days": null}}
- leitor:b: {"tipo": "prazo_minimo", "condicoes": [{"field": "publicado_joue", "op": "eq", "value": false}, {"field": "tipo_contrato", "op": "ne", "value": "obras"}, {"field": "tipo_procedimento", "op": "eq", "value": "concurso_limitado_previa_qualificacao"}], "params": {"minimum_days": 9, "deadline_field": "prazo_propostas_dias", "counted_from": "data_envio_convite", "usual_days": null}} || {"tipo": "prazo_minimo", "condicoes": [{"field": "publicado_joue", "op": "eq", "value": false}, {"field": "tipo_contrato", "op": "eq", "value": "obras"}, {"field": "tipo_procedimento", "op": "eq", "value": "concurso_limitado_previa_qualificacao"}], "params": {"minimum_days": 20, "deadline_field": "prazo_propostas_dias", "counted_from": "data_envio_convite", "usual_days": null}}

## regra:ccp:auto-prazo-minimo-art190-2-v20080730@v1

- leitor:a16: {"tipo": "prazo_minimo", "condicoes": [{"field": "publicado_joue", "op": "eq", "value": false}, {"field": "tipo_contrato", "op": "eq", "value": "obras"}, {"field": "tipo_procedimento", "op": "eq", "value": "concurso_limitado_previa_qualificacao"}], "params": {"minimum_days": 8, "deadline_field": "prazo_propostas_dias", "counted_from": "data_envio_convite", "usual_days": null}} || {"tipo": "prazo_minimo", "condicoes": [{"field": "publicado_joue", "op": "eq", "value": false}, {"field": "tipo_contrato", "op": "ne", "value": "obras"}, {"field": "tipo_procedimento", "op": "eq", "value": "concurso_limitado_previa_qualificacao"}], "params": {"minimum_days": 20, "deadline_field": "prazo_propostas_dias", "counted_from": "data_envio_convite", "usual_days": null}}
- leitor:b: não tipável (sem_vocabulario): O vocabulário não permite representar a condição de manifesta simplicidade dos trabalhos necessários à realização da obra.
- verificador (A): regra 1: minimum_days 8 não está nas fontes (L8, L4)

## regra:ccp:auto-prazo-minimo-art190-2@v1

- leitor:a16: {"tipo": "prazo_minimo", "condicoes": [{"field": "publicado_joue", "op": "eq", "value": false}, {"field": "tipo_contrato", "op": "eq", "value": "obras"}, {"field": "tipo_procedimento", "op": "eq", "value": "concurso_limitado_previa_qualificacao"}], "params": {"minimum_days": 6, "deadline_field": "prazo_propostas_dias", "counted_from": "data_envio_convite", "usual_days": null}} || {"tipo": "prazo_minimo", "condicoes": [{"field": "publicado_joue", "op": "eq", "value": false}, {"field": "tipo_contrato", "op": "ne", "value": "obras"}, {"field": "tipo_procedimento", "op": "eq", "value": "concurso_limitado_previa_qualificacao"}], "params": {"minimum_days": 14, "deadline_field": "prazo_propostas_dias", "counted_from": "data_envio_convite", "usual_days": null}}
- leitor:b: não tipável (sem_vocabulario): O vocabulário não permite representar a condição de manifesta simplicidade dos trabalhos necessários à realização da obra.

## regra:ccp:auto-prazo-minimo-art191-v20180101@v1

- leitor:a16: {"tipo": "prazo_minimo", "condicoes": [{"field": "publicado_joue", "op": "eq", "value": true}, {"field": "tipo_procedimento", "op": "eq", "value": "concurso_limitado_previa_qualificacao"}], "params": {"minimum_days": 25, "deadline_field": "prazo_propostas_dias", "counted_from": "data_envio_convite", "usual_days": null}} || {"tipo": "prazo_minimo", "condicoes": [{"field": "anuncio_pre_informacao", "op": "eq", "value": true}, {"field": "publicado_joue", "op": "eq", "value": true}, {"field": "tipo_procedimento", "op": "eq", "value": "concurso_limitado_previa_qualificacao"}], "params": {"minimum_days": 10, "deadline_field": "prazo_propostas_dias", "counted_from": "data_envio_convite", "usual_days": null}} || {"tipo": "prazo_minimo", "condicoes": [{"field": "setores_especiais", "op": "eq", "value": true}, {"field": "tipo_procedimento", "op": "eq", "value": "concurso_limitado_previa_qualificacao"}], "params": {"minimum_days": 10, "deadline_field": "prazo_propostas_dias", "counted_from": "data_envio_convite", "usual_days": null}}
- leitor:b: não tipável (sem_vocabulario): O vocabulário não permite representar as condições de cobertura das prestações, antecedência e conteúdo do anúncio de pré-informação necessárias à redução para 10 dias.
- verificador (B): não tipável: fonte em ccp:art191.2, que é vizinho (L1); não tipável: fonte em ccp:art191.2.a, que é vizinho (L1); não tipável: fonte em ccp:art191.2.b, que é vizinho (L1)

## regra:ccp:auto-prazo-minimo-art191-1-v20080730@v1

- leitor:a16: {"tipo": "prazo_minimo", "condicoes": [{"field": "publicado_joue", "op": "eq", "value": true}, {"field": "tipo_procedimento", "op": "eq", "value": "concurso_limitado_previa_qualificacao"}], "params": {"minimum_days": 35, "deadline_field": "prazo_propostas_dias", "counted_from": "data_envio_convite", "usual_days": null}}
- leitor:b: {"tipo": "prazo_minimo", "condicoes": [{"field": "publicado_joue", "op": "eq", "value": true}, {"field": "tipo_procedimento", "op": "eq", "value": "concurso_limitado_previa_qualificacao"}], "params": {"minimum_days": 35, "deadline_field": "prazo_propostas_dias", "counted_from": "data_envio_convite", "usual_days": null}}

## regra:ccp:auto-prazo-minimo-art191-2-a-v20080730@v1

- leitor:a16: {"tipo": "prazo_minimo", "condicoes": [{"field": "anuncio_pre_informacao", "op": "eq", "value": true}, {"field": "data_inicio_procedimento", "op": "ge", "value": "2008-07-30"}, {"field": "publicado_joue", "op": "eq", "value": true}, {"field": "tipo_procedimento", "op": "eq", "value": "concurso_limitado_previa_qualificacao"}], "params": {"minimum_days": 36, "deadline_field": "prazo_propostas_dias", "counted_from": "data_envio_convite", "usual_days": null}}
- leitor:b: não tipável (sem_vocabulario): O vocabulário não permite representar a condição de antecedência do envio do anúncio de pré-informação necessária à aplicação do prazo mínimo de 22 dias.
- verificador (A): regra 1, data_inicio_procedimento ge 2008-07-30: as fontes não fixam uma data (L13)

## regra:ccp:auto-prazo-minimo-art191-2-a@v1

- leitor:a16: {"tipo": "prazo_minimo", "condicoes": [{"field": "publicado_joue", "op": "eq", "value": true}, {"field": "tipo_procedimento", "op": "eq", "value": "concurso_limitado_previa_qualificacao"}], "params": {"minimum_days": 10, "deadline_field": "prazo_propostas_dias", "counted_from": "data_envio_convite", "usual_days": null}}
- leitor:b: não tipável (sem_vocabulario): O vocabulário não permite representar a condição de antecedência do envio do anúncio de pré-informação, entre 35 dias e 12 meses, relativamente ao envio do anúncio do concurso.

## regra:ccp:auto-prazo-minimo-art191-3-v20080730@v1

- leitor:a16: {"tipo": "prazo_minimo", "condicoes": [{"field": "publicado_joue", "op": "eq", "value": true}, {"field": "setores_especiais", "op": "eq", "value": true}, {"field": "tipo_procedimento", "op": "eq", "value": "concurso_limitado_previa_qualificacao"}], "params": {"minimum_days": 19, "deadline_field": "prazo_propostas_dias", "counted_from": "data_envio_convite", "usual_days": null}}
- leitor:b: {"tipo": "prazo_minimo", "condicoes": [{"field": "publicado_joue", "op": "eq", "value": true}, {"field": "setores_especiais", "op": "eq", "value": true}, {"field": "tipo_procedimento", "op": "eq", "value": "concurso_limitado_previa_qualificacao"}], "params": {"minimum_days": 19, "deadline_field": "prazo_propostas_dias", "counted_from": "data_envio_convite", "usual_days": null}}

## regra:ccp:auto-prazo-minimo-art191-3@v1

- leitor:a16: {"tipo": "prazo_minimo", "condicoes": [{"field": "publicado_joue", "op": "eq", "value": true}, {"field": "setores_especiais", "op": "eq", "value": true}, {"field": "tipo_procedimento", "op": "eq", "value": "concurso_limitado_previa_qualificacao"}], "params": {"minimum_days": 10, "deadline_field": "prazo_propostas_dias", "counted_from": "data_envio_convite", "usual_days": null}}
- leitor:b: {"tipo": "prazo_minimo", "condicoes": [{"field": "publicado_joue", "op": "eq", "value": true}, {"field": "setores_especiais", "op": "eq", "value": true}, {"field": "tipo_procedimento", "op": "eq", "value": "concurso_limitado_previa_qualificacao"}], "params": {"minimum_days": 10, "deadline_field": "prazo_propostas_dias", "counted_from": "data_envio_convite", "usual_days": null}}

## regra:ccp:auto-prazo-maximo-art192-3@v1

- leitor:a16: não tipável (nao_e_prazo_minimo): O prazo de dois dias é um prazo para a falta de discordância, não um prazo mínimo para apresentar as propostas.
- leitor:b: não tipável (sem_vocabulario): O vocabulário não prevê a recepção do convite como início da contagem do prazo para manifestar discordância.

## regra:ccp:auto-prazo-maximo-art192-4@v1

- leitor:a16: não tipável (texto_em_falta): Os dias do novo prazo estão no n.º 3, que não está mostrado.
- leitor:b: não tipável (sem_vocabulario): O vocabulário não permite representar a condição de algum candidato qualificado manifestar por escrito discordância sobre o prazo fixado.

## regra:ccp:auto-prazo-minimo-art198-1-v20080730@v1

- leitor:a16: {"tipo": "prazo_minimo", "condicoes": [{"field": "publicado_joue", "op": "eq", "value": true}, {"field": "tipo_procedimento", "op": "eq", "value": "procedimento_negociacao"}], "params": {"minimum_days": 37, "deadline_field": "prazo_candidaturas_dias", "counted_from": "data_envio_anuncio", "usual_days": null}}
- leitor:b: {"tipo": "prazo_minimo", "condicoes": [{"field": "publicado_joue", "op": "eq", "value": true}, {"field": "tipo_procedimento", "op": "eq", "value": "procedimento_negociacao"}], "params": {"minimum_days": 37, "deadline_field": "prazo_candidaturas_dias", "counted_from": "data_envio_anuncio", "usual_days": null}}
- verificador (A): regra 1, publicado_joue eq True: as fontes não afirmam o facto (L7)
- verificador (B): regra 1, publicado_joue eq True: as fontes não afirmam o facto (L7)

## regra:ccp:auto-prazo-minimo-art198-2-v20080730@v1

- leitor:a16: {"tipo": "prazo_minimo", "condicoes": [{"field": "anuncio_pre_informacao", "op": "eq", "value": true}, {"field": "tipo_procedimento", "op": "eq", "value": "procedimento_negociacao"}], "params": {"minimum_days": 37, "deadline_field": "prazo_candidaturas_dias", "counted_from": "data_envio_convite", "usual_days": null}}
- leitor:b: {"tipo": "prazo_minimo", "condicoes": [{"field": "anuncio_pre_informacao", "op": "eq", "value": true}, {"field": "tipo_procedimento", "op": "eq", "value": "procedimento_negociacao"}], "params": {"minimum_days": 37, "deadline_field": "prazo_candidaturas_dias", "counted_from": "data_envio_convite", "usual_days": null}}

## regra:ccp:auto-prazo-minimo-art214-1@v1

- leitor:a16: não tipável (nao_e_prazo_minimo): O prazo é de três dias, antecedência mínima do júri para notificar os candidatos, não um prazo para os candidatos apresentarem algo.
- leitor:b: não tipável (nao_e_prazo_minimo): Trata-se de um prazo para o júri notificar os candidatos da primeira sessão de diálogo.

## regra:ccp:auto-prazo-minimo-art218-v20080730@v1

- leitor:a16: {"tipo": "prazo_minimo", "condicoes": [{"field": "tipo_procedimento", "op": "eq", "value": "dialogo_concorrencial"}], "params": {"minimum_days": 40, "deadline_field": "prazo_propostas_dias", "counted_from": "data_envio_convite", "usual_days": null}}
- leitor:b: {"tipo": "prazo_minimo", "condicoes": [{"field": "tipo_procedimento", "op": "eq", "value": "dialogo_concorrencial"}], "params": {"minimum_days": 40, "deadline_field": "prazo_propostas_dias", "counted_from": "data_envio_convite", "usual_days": null}}
- verificador (B): regra 1, tipo_procedimento eq dialogo_concorrencial: «diálogo concorrencial» não está em ccp:art218; regra 1, tipo_procedimento eq dialogo_concorrencial: as fontes não nomeiam ['dialogo_concorrencial']

## regra:ccp:auto-prazo-maximo-art219-c-3-v20180101@v1

- leitor:a16: não tipável (texto_em_falta): Os dias do prazo estão no anexo x, que não é mostrado.
- leitor:b: não tipável (nao_e_prazo_maximo): O prazo é para a própria entidade adjudicante enviar um anúncio.

## regra:ccp:auto-prazo-maximo-art219-c-3@v1

- leitor:a16: não tipável (texto_em_falta): Os dias do prazo estão nas alíneas b) e c) do n.º 3 do artigo 474.º, que não estão mostradas.
- leitor:b: não tipável (nao_e_prazo_maximo): O prazo é para a própria entidade adjudicante enviar um anúncio.

## regra:ccp:auto-prazo-maximo-art219-i-5@v1

- leitor:a16: não tipável (nao_e_prazo_maximo): O prazo é da própria entidade adjudicante para exigir os documentos, não um prazo máximo para os concorrentes apresentarem algo.
- leitor:b: não tipável (sem_vocabulario): Falta um campo para representar a condição de os termos de referência exigirem aos concorrentes habilitações profissionais específicas.

## regra:ccp:auto-prazo-maximo-art234-1-v20080730@v1

- leitor:a16: não tipável (nao_e_prazo_minimo): O prazo é de cinco dias para apresentar documentos comprovativos, não um prazo máximo para os concorrentes apresentarem algo.
- leitor:b: não tipável (sem_vocabulario): Falta no vocabulário uma condição que represente a exigência de habilitações profissionais específicas pelos termos de referência.

## regra:ccp:auto-prazo-maximo-art235-v20080730@v1

- leitor:a16: não tipável (texto_em_falta): Os dias do prazo estão no anexo xiii, que não é mostrado.
- leitor:b: não tipável (nao_e_prazo_maximo): O prazo é para a própria entidade adjudicante enviar um anúncio.

## regra:ccp:auto-prazo-minimo-art240-1-b@v1

- leitor:a16: não tipável (sem_vocabulario): A regra é de um sistema de aquisição dinâmico, instrumento que o vocabulário não tem.
- leitor:b: não tipável (sem_vocabulario): O vocabulário não permite limitar a regra aos sistemas de aquisição dinâmicos.

## regra:ccp:auto-prazo-maximo-art241-3-v20080730@v1

- leitor:a16: não tipável (sem_vocabulario): A regra é de um sistema de aquisição dinâmico, instrumento que o vocabulário não tem.
- leitor:b: não tipável (nao_e_prazo_maximo): O prazo destina-se à entidade adjudicante para notificar a aceitação ou rejeição, não à apresentação de algo.

## regra:ccp:auto-prazo-maximo-art241-a-3@v1

- leitor:a16: não tipável (sem_vocabulario): A regra é de um sistema de aquisição dinâmico, instrumento que o vocabulário não tem.
- leitor:b: não tipável (nao_e_prazo_maximo): O prazo é para a própria entidade adjudicante analisar as candidaturas.

## regra:ccp:auto-prazo-maximo-art241-d@v1

- leitor:a16: não tipável (sem_vocabulario): A regra é de um sistema de aquisição dinâmico, instrumento que o vocabulário não tem.
- leitor:b: não tipável (sem_vocabulario): O vocabulário não contempla os sistemas de aquisição dinâmicos, aos quais a regra se limita.

## regra:ccp:auto-prazo-minimo-art242-3-v20080730@v1

- leitor:a16: não tipável (sem_vocabulario): A regra é de um sistema de aquisição dinâmico, instrumento que o vocabulário não tem.
- leitor:b: não tipável (nao_e_prazo_minimo): O prazo regula a publicação do anúncio simplificado pela entidade adjudicante, não a apresentação de elementos pelos interessados.

## regra:ccp:auto-prazo-minimo-art242-4-v20080730@v1

- leitor:a16: não tipável (sem_vocabulario): A regra é de um sistema de aquisição dinâmico, instrumento que o vocabulário não tem.
- leitor:b: não tipável (sem_vocabulario): O vocabulário não permite limitar a regra aos sistemas de aquisição dinâmicos.

## regra:ccp:auto-prazo-minimo-art243-2-a-v20080730@v1

- leitor:a16: não tipável (sem_vocabulario): A regra é de um sistema de aquisição dinâmico, instrumento que o vocabulário não tem.
- leitor:b: não tipável (sem_vocabulario): O vocabulário não permite limitar a regra aos sistemas de aquisição dinâmicos.

## regra:ccp:auto-prazo-maximo-art270@v1

- leitor:a16: não tipável (nao_e_prazo_minimo): O prazo é de cinco dias, e não um mínimo para apresentar algo.
- leitor:b: não tipável (sem_vocabulario): O vocabulário não contém um campo de prazo para a apresentação de impugnações administrativas.

## regra:ccp:auto-prazo-maximo-art273@v1

- leitor:a16: não tipável (nao_e_prazo_minimo): O prazo é do próprio órgão da administração para notificar, não um prazo para os interessados apresentarem algo.
- leitor:b: não tipável (sem_vocabulario): Falta vocabulário para representar a condição relativa ao objeto da impugnação administrativa.

## regra:ccp:auto-prazo-maximo-art274-1@v1

- leitor:a16: não tipável (nao_e_prazo_minimo): O prazo é da própria entidade adjudicante para decidir, não um prazo para os interessados apresentarem algo.
- leitor:b: não tipável (nao_e_prazo_maximo): O prazo é para decidir as impugnações administrativas, não para apresentar algo.

## regra:ccp:auto-prazo-minimo-art276-v20120811@v1

- leitor:a16: {"tipo": "prazo_minimo", "condicoes": [{"field": "tipo_contrato", "op": "eq", "value": "obras"}, {"field": "tipo_entidade", "op": "eq", "value": "estado"}, {"field": "tipo_procedimento", "op": "eq", "value": "ajuste_direto"}], "params": {"minimum_days": 37, "deadline_field": "prazo_candidaturas_dias", "counted_from": "data_envio_anuncio", "usual_days": null}} || {"tipo": "prazo_minimo", "condicoes": [{"field": "tipo_contrato", "op": "eq", "value": "obras"}, {"field": "tipo_entidade", "op": "eq", "value": "estado"}, {"field": "tipo_procedimento", "op": "eq", "value": "ajuste_direto"}], "params": {"minimum_days": 40, "deadline_field": "prazo_propostas_dias", "counted_from": "data_envio_anuncio", "usual_days": null}}
- leitor:b: não tipável (sem_vocabulario): O vocabulário não permite representar a condição de o contrato ser celebrado por um concessionário de obras públicas que não seja entidade adjudicante.
- verificador (A): regra 1, tipo_entidade eq estado: as fontes não nomeiam ['estado']; regra 1, tipo_procedimento eq ajuste_direto: as fontes não nomeiam ['ajuste_direto']; regra 2, tipo_entidade eq estado: as fontes não nomeiam ['estado']; regra 2, tipo_procedimento eq ajuste_direto: as fontes não nomeiam ['ajuste_direto']

## regra:ccp:auto-prazo-minimo-art276-v20180101@v1

- leitor:a16: {"tipo": "prazo_minimo", "condicoes": [{"field": "tipo_contrato", "op": "eq", "value": "obras"}, {"field": "tipo_procedimento", "op": "eq", "value": "concurso_publico"}], "params": {"minimum_days": 37, "deadline_field": "prazo_candidaturas_dias", "counted_from": "data_envio_anuncio", "usual_days": null}} || {"tipo": "prazo_minimo", "condicoes": [{"field": "tipo_contrato", "op": "eq", "value": "obras"}, {"field": "tipo_procedimento", "op": "eq", "value": "concurso_publico"}], "params": {"minimum_days": 40, "deadline_field": "prazo_propostas_dias", "counted_from": "data_envio_anuncio", "usual_days": null}}
- leitor:b: não tipável (sem_vocabulario): O vocabulário não permite representar a condição de o contratante ser um concessionário de obras públicas que não seja entidade adjudicante.
- verificador (A): regra 1, tipo_procedimento eq concurso_publico: as fontes não nomeiam ['concurso_publico']; regra 2, tipo_procedimento eq concurso_publico: as fontes não nomeiam ['concurso_publico']

## regra:ccp:auto-prazo-minimo-art276-v20210620@v1

- leitor:a16: {"tipo": "prazo_minimo", "condicoes": [{"field": "tipo_contrato", "op": "eq", "value": "obras"}, {"field": "tipo_procedimento", "op": "eq", "value": "ajuste_direto"}], "params": {"minimum_days": 37, "deadline_field": "prazo_candidaturas_dias", "counted_from": "data_envio_anuncio", "usual_days": null}} || {"tipo": "prazo_minimo", "condicoes": [{"field": "tipo_contrato", "op": "eq", "value": "obras"}, {"field": "tipo_procedimento", "op": "eq", "value": "ajuste_direto"}], "params": {"minimum_days": 40, "deadline_field": "prazo_propostas_dias", "counted_from": "data_envio_anuncio", "usual_days": null}}
- leitor:b: não tipável (sem_vocabulario): O vocabulário não permite representar a condição de os contratos serem celebrados por concessionários de obras públicas que não sejam entidades adjudicantes.
- verificador (A): regra 1, tipo_procedimento eq ajuste_direto: as fontes não nomeiam ['ajuste_direto']; regra 2, tipo_procedimento eq ajuste_direto: as fontes não nomeiam ['ajuste_direto']

## regra:ccp:auto-prazo-minimo-art276-5-v20080730@v1

- leitor:a16: {"tipo": "prazo_minimo", "condicoes": [{"field": "tipo_contrato", "op": "eq", "value": "obras"}, {"field": "tipo_procedimento", "op": "eq", "value": "concurso_publico"}], "params": {"minimum_days": 37, "deadline_field": "prazo_candidaturas_dias", "counted_from": "data_envio_anuncio", "usual_days": null}} || {"tipo": "prazo_minimo", "condicoes": [{"field": "tipo_contrato", "op": "eq", "value": "obras"}, {"field": "tipo_procedimento", "op": "eq", "value": "concurso_publico"}], "params": {"minimum_days": 40, "deadline_field": "prazo_propostas_dias", "counted_from": "data_envio_anuncio", "usual_days": null}}
- leitor:b: não tipável (sem_vocabulario): O vocabulário não permite limitar a regra aos concessionários de obras públicas que não sejam entidades adjudicantes.
- verificador (A): regra 1, tipo_procedimento eq concurso_publico: as fontes não nomeiam ['concurso_publico']; regra 2, tipo_procedimento eq concurso_publico: as fontes não nomeiam ['concurso_publico']

## regra:ccp:auto-prazo-minimo-art276-7-v20080730@v1

- leitor:a16: não tipável (sem_vocabulario): A regra depende do número de dias que as peças não são disponibilizadas, facto que o vocabulário não tem.
- leitor:b: não tipável (sem_vocabulario): O vocabulário não permite representar uma prorrogação mínima equivalente ao atraso verificado, a pedido dos interessados.

## regra:ccp:auto-prazo-maximo-art283-a-v20110113@v1

- leitor:a16: não tipável (texto_em_falta): Os dias do prazo de suspensão estão no n.º 3 do artigo 95.º, que não é mostrado.
- leitor:b: não tipável (nao_e_prazo_maximo): Os prazos respeitam à outorga do contrato, não à apresentação de elementos, pelo que não existe um prazo máximo tipável.
- verificador (B): não tipável: fonte em ccp:art283-a.2.c, que é vizinho (L1)

## regra:ccp:auto-prazo-maximo-art283-a-v20210620@v1

- leitor:a16: não tipável (texto_em_falta): Os dias do prazo de suspensão estão no n.º 3 do artigo 95.º, que não é mostrado.
- leitor:b: não tipável (nao_e_prazo_maximo): A passagem estabelece um prazo de suspensão da outorga do contrato, não um prazo máximo para apresentar algo.
- verificador (B): não tipável: fonte em ccp:art283-a.2.c, que é vizinho (L1)

## regra:ccp:auto-prazo-maximo-art283-a-2-c@v1

- leitor:a16: não tipável (nao_e_prazo_minimo): O prazo é de 10 dias antes da outorga do contrato, não um prazo para apresentar algo.
- leitor:b: não tipável (nao_e_prazo_maximo): A passagem fixa um prazo mínimo para a outorga do contrato, não um prazo máximo para apresentar algo.

## regra:ccp:auto-prazo-maximo-art287-6-c-v20180101@v1

- leitor:a16: não tipável (nao_e_prazo_minimo): O prazo é de 10 dias antes da publicação do contrato, não um prazo para apresentar algo.
- leitor:b: não tipável (nao_e_prazo_maximo): A passagem fixa um prazo mínimo de espera para a outorga do contrato, não um prazo máximo para apresentar algo.

## regra:ccp:auto-prazo-minimo-art295-v20091007@v1

- leitor:a16: não tipável (nao_e_prazo_minimo): O prazo é do próprio contraente público para promover a liberação da caução, não um prazo mínimo para os interessados apresentarem algo.
- leitor:b: não tipável (nao_e_prazo_minimo): Os prazos regulam a liberação da caução pelo contraente público, não um prazo mínimo para apresentar algo.
- verificador (B): não tipável: fonte em ccp:art295.3, que é vizinho (L1)

## regra:ccp:auto-prazo-maximo-art295-3@v1

- leitor:a16: não tipável (nao_e_prazo_maximo): O prazo é de 30 dias para o próprio contraente público promover a liberação da caução, não um prazo máximo para os interessados apresentarem algo.
- leitor:b: não tipável (nao_e_prazo_maximo): O prazo é para o contraente público liberar a caução, não para apresentar algo.

## regra:ccp:auto-prazo-minimo-art295-4@v1

- leitor:a16: não tipável (nao_e_prazo_minimo): O prazo é do próprio contraente público para promover a liberação da caução, não um prazo mínimo para os interessados apresentarem algo.
- leitor:b: não tipável (nao_e_prazo_minimo): A passagem fixa um prazo máximo para o contraente público liberar a caução, não um prazo mínimo para apresentar algo.

## regra:ccp:auto-prazo-maximo-art295-5-a-v20080730@v1

- leitor:a16: não tipável (nao_e_prazo_minimo): O prazo é de 30 dias para a libertação de parte da caução, não um prazo máximo para a entidade adjudicante apresentar algo.
- leitor:b: não tipável (nao_e_prazo_maximo): O prazo é para o contraente público promover a liberação parcial da caução, não para apresentar algo.

## regra:ccp:auto-prazo-maximo-art295-5-b-v20080730@v1

- leitor:a16: não tipável (nao_e_prazo_maximo): O prazo é de 30 dias para a parte da caução que não é libertada integralmente, não um prazo máximo para a entidade pública.
- leitor:b: não tipável (nao_e_prazo_maximo): O prazo é para o contraente público liberar a caução, não para apresentar algo.

## regra:ccp:auto-prazo-minimo-art295-6-v20080730@v1

- leitor:a16: não tipável (nao_e_prazo_minimo): O prazo é de 75 % de libertação da caução, não um prazo mínimo para os interessados apresentarem algo.
- leitor:b: não tipável (nao_e_prazo_minimo): O prazo é um máximo para a liberação da caução, não um mínimo para apresentar algo.

## regra:ccp:auto-prazo-maximo-art295-9@v1

- leitor:a16: não tipável (nao_e_prazo_maximo): O prazo é o da própria entidade adjudicante para libertar a caução, não um prazo máximo para os cocontratantes apresentarem algo.
- leitor:b: não tipável (nao_e_prazo_maximo): O prazo respeita à liberação da caução pelo contraente público, não à apresentação de elementos.

## regra:ccp:auto-prazo-maximo-art296-2@v1

- leitor:a16: não tipável (nao_e_prazo_minimo): O prazo é da própria entidade adjudicante para renovar o valor da caução, não um prazo para os interessados apresentarem algo.
- leitor:b: não tipável (nao_e_prazo_maximo): O prazo é para renovar o valor da caução, não para apresentar algo.

## regra:ccp:auto-prazo-maximo-art299-1-v20080730@v1

- leitor:a16: não tipável (nao_e_prazo_minimo): O prazo é da própria entidade adjudicante para pagar, não um prazo para os interessados apresentarem algo.
- leitor:b: não tipável (nao_e_prazo_maximo): O prazo é para o contraente público efetuar pagamentos, não para apresentar algo.

## regra:ccp:auto-prazo-maximo-art299-1-a@v1

- leitor:a16: não tipável (nao_e_prazo_minimo): O prazo é de pagamento, não um prazo para apresentar algo.
- leitor:b: não tipável (nao_e_prazo_maximo): A passagem fixa o vencimento de uma obrigação de pagamento, não um prazo para apresentar algo.

## regra:ccp:auto-prazo-maximo-art299-1-b@v1

- leitor:a16: não tipável (nao_e_prazo_minimo): O prazo é um máximo para o próprio contraente público pagar, não um prazo para apresentar algo.
- leitor:b: não tipável (nao_e_prazo_maximo): O prazo respeita ao vencimento de uma obrigação pecuniária, não à apresentação de elementos.

## regra:ccp:auto-prazo-maximo-art299-1-c@v1

- leitor:a16: não tipável (nao_e_prazo_minimo): O prazo é de pagamento do contraente público, não um prazo para apresentar algo.
- leitor:b: não tipável (nao_e_prazo_maximo): O prazo é de pagamento pelo contraente público, não de apresentação de elementos.

## regra:ccp:auto-prazo-maximo-art299-1-d@v1

- leitor:a16: não tipável (nao_e_prazo_minimo): O prazo é o máximo de pagamento, não um prazo para apresentar algo.
- leitor:b: não tipável (nao_e_prazo_maximo): O prazo respeita ao vencimento de uma obrigação pecuniária, não à apresentação de elementos.

## regra:ccp:auto-prazo-maximo-art299-2-v20080730@v1

- leitor:a16: não tipável (nao_e_prazo_maximo): O prazo é um máximo para o próprio contrato, não um prazo para apresentar algo.
- leitor:b: não tipável (nao_e_prazo_maximo): O prazo é para pagamentos pelo contraente público, não para apresentar elementos.

## regra:ccp:auto-prazo-maximo-art299-2@v1

- leitor:a16: {"tipo": "prazo_maximo", "condicoes": [{"field": "tipo_contrato", "op": "in", "value": ["bens", "servicos"]}, {"field": "tipo_procedimento", "op": "eq", "value": "procedimento_concorrencial_negociacao"}], "params": {"maximum_days": 30, "deadline_field": "prazo_pronuncia_dias", "counted_from": "nao_indicado"}}
- leitor:b: não tipável (nao_e_prazo_maximo): O prazo limita a duração do procedimento de aceitação ou verificação, não sendo um prazo para apresentar algo.
- verificador (A): regra 1, tipo_procedimento eq procedimento_concorrencial_negociacao: as fontes não nomeiam ['procedimento_concorrencial_negociacao']; regra 1: as fontes de maximum_days não dizem um máximo («não pode ser superior a», «no prazo de», L8); regra 1: deadline_field prazo_pronuncia_dias e as fontes dizem nada (L9)

## regra:ccp:auto-prazo-maximo-art299-3@v1

- leitor:a16: não tipável (nao_e_prazo_minimo): O prazo é de pagamento do contraente público, não um prazo para apresentar algo.
- leitor:b: não tipável (nao_e_prazo_maximo): O prazo é para o contraente público efetuar pagamentos, não para apresentar algo.

## regra:ccp:auto-prazo-maximo-art299-4@v1

- leitor:a16: não tipável (nao_e_prazo_maximo): O prazo é o máximo do próprio contrato, não um prazo para apresentar algo.
- leitor:b: não tipável (nao_e_prazo_maximo): O prazo é para o pagamento pelo contraente público, não para apresentar elementos.

## regra:ccp:auto-prazo-maximo-art299-a-1@v1

- leitor:a16: não tipável (nao_e_prazo_minimo): O prazo é um máximo para o vencimento das obrigações, não um prazo para apresentar algo.
- leitor:b: não tipável (nao_e_prazo_maximo): O prazo refere-se ao vencimento de obrigações pecuniárias, não à apresentação de elementos.

## regra:ccp:auto-prazo-maximo-art304-3@v1

- leitor:a16: não tipável (nao_e_prazo_maximo): O prazo de cinco dias é da própria entidade para reduzir a ordem à escrita e notificá-la, não um prazo para os co-contratantes apresentarem algo.
- leitor:b: não tipável (nao_e_prazo_maximo): O prazo destina-se à redução a escrito e notificação de ordens, directivas ou instruções pelo contraente público, não à apresentação de elementos.

## regra:ccp:auto-prazo-maximo-art315-v20210620@v1

- leitor:a16: não tipável (nao_e_prazo_minimo): O prazo é de publicitação do contraente público, não um prazo para apresentar algo.
- leitor:b: não tipável (nao_e_prazo_maximo): Os prazos respeitam à publicitação das modificações pelo contraente público e à manutenção dessa publicidade.
- verificador (B): não tipável: fonte em ccp:art315.1, que é vizinho (L1)

## regra:ccp:auto-prazo-maximo-art315-1-v20180101@v1

- leitor:a16: não tipável (nao_e_prazo_minimo): O prazo é de publicitação das modificações, não um prazo para apresentar algo.
- leitor:b: não tipável (nao_e_prazo_maximo): Os prazos são para o contraente público publicitar modificações contratuais e manter essa publicidade, não para apresentar elementos.

## regra:ccp:auto-prazo-maximo-art315-1@v1

- leitor:a16: não tipável (nao_e_prazo_minimo): O prazo é da própria entidade adjudicante para publicitar as modificações, não um prazo para os interessados apresentarem algo.
- leitor:b: não tipável (nao_e_prazo_maximo): Os prazos regulam a publicitação pelo contraente público e a manutenção da publicidade, não a apresentação de elementos.

## regra:ccp:auto-prazo-maximo-art319-3-v20080730@v1

- leitor:a16: não tipável (nao_e_prazo_minimo): O prazo é do próprio contraente público para se pronunciar, não um prazo para os interessados apresentarem algo.
- leitor:b: não tipável (nao_e_prazo_maximo): O prazo é para o próprio contraente público se pronunciar, não para apresentar algo.

## regra:ccp:auto-prazo-maximo-art319-3-v20180101@v1

- leitor:a16: não tipável (nao_e_prazo_minimo): O prazo é do próprio contraente público para se pronunciar, não um prazo para os cocontratantes apresentarem algo.
- leitor:b: não tipável (nao_e_prazo_maximo): O prazo destina-se à pronúncia do próprio contraente público.

## regra:ccp:auto-prazo-maximo-art319-a-7@v1

- leitor:a16: não tipável (nao_e_prazo_maximo): O prazo é do próprio contraente público para se pronunciar, não um prazo para os cocontratantes apresentarem algo.
- leitor:b: não tipável (nao_e_prazo_maximo): O prazo destina-se à pronúncia do próprio contraente público.

## regra:ccp:auto-prazo-maximo-art321-a-2@v1

- leitor:a16: não tipável (nao_e_prazo_maximo): O prazo é um máximo da própria entidade adjudicante para notificar o cocontratante, não um prazo para os interessados apresentarem algo.
- leitor:b: não tipável (nao_e_prazo_maximo): O prazo destina-se à liquidação da dívida ao subcontratado, não à apresentação de elementos.

## regra:ccp:auto-prazo-minimo-art327-v20080730@v1

- leitor:a16: não tipável (texto_em_falta): Os dias do prazo estão no artigo 332.º, que não é mostrado.
- leitor:b: não tipável (nao_e_prazo_minimo): O prazo é uma antecedência de notificação para exercer o direito de recusar o cumprimento, não um prazo para apresentar algo previsto no vocabulário.
- verificador (B): não tipável: fonte em ccp:art327.3, que é vizinho (L1)

## regra:ccp:auto-prazo-maximo-art327-4@v1

- leitor:a16: não tipável (nao_e_prazo_minimo): O prazo é do próprio contraente público para se opor, não um prazo para os cocontratantes apresentarem algo.
- leitor:b: não tipável (nao_e_prazo_maximo): O prazo destina-se ao próprio contraente público exercer oposição.

## regra:ccp:auto-prazo-maximo-art329-5@v1

- leitor:a16: não tipável (nao_e_prazo_maximo): O prazo é da própria entidade adjudicante para comunicar, não um prazo máximo para os interessados apresentarem algo.
- leitor:b: não tipável (nao_e_prazo_maximo): O prazo de 10 dias destina-se a uma comunicação pela própria entidade adjudicante.

## regra:ccp:auto-prazo-maximo-art332-4@v1

- leitor:a16: não tipável (nao_e_prazo_minimo): Os 30 dias são o prazo para produzir efeitos da resolução, não um prazo para apresentar algo.
- leitor:b: não tipável (nao_e_prazo_maximo): Os 30 dias determinam a produção de efeitos da declaração de resolução, não um prazo máximo para apresentar algo.

## regra:ccp:auto-prazo-maximo-art333-4@v1

- leitor:a16: não tipável (nao_e_prazo_minimo): O prazo é da própria entidade adjudicante para comunicar o facto, não um prazo para os interessados apresentarem algo.
- leitor:b: não tipável (nao_e_prazo_maximo): O prazo de 10 dias é para uma comunicação pelo próprio contraente público, não para apresentar elementos.

## regra:ccp:auto-prazo-maximo-art334-3@v1

- leitor:a16: não tipável (nao_e_prazo_minimo): O prazo é de 30 dias para o co-contratante reclamar juros de mora, não um prazo para apresentar algo.
- leitor:b: não tipável (nao_e_prazo_maximo): O prazo respeita ao pagamento de uma indemnização e não à apresentação de elementos.

## regra:ccp:auto-prazo-maximo-art345-3@v1

- leitor:a16: não tipável (nao_e_prazo_minimo): O prazo é de 10 dias, e não um máximo para apresentar algo.
- leitor:b: {"tipo": "prazo_maximo", "condicoes": [{"field": "tipo_contrato", "op": "eq", "value": "obras"}], "params": {"maximum_days": 10, "deadline_field": "prazo_reclamacao_dias", "counted_from": "data_notificacao"}}
- verificador (B): regra 1: as fontes de maximum_days não dizem um máximo («não pode ser superior a», «no prazo de», L8)

## regra:ccp:auto-prazo-maximo-art345-4@v1

- leitor:a16: não tipável (nao_e_prazo_minimo): O prazo de 15 dias é o da exposição fundamentada, não um prazo mínimo para apresentar algo.
- leitor:b: não tipável (sem_vocabulario): O vocabulário não permite representar a condição de as reclamações ou reservas terem sido exaradas no próprio auto e limitadas ao enunciado genérico do respetivo objeto.

## regra:ccp:auto-prazo-maximo-art345-5@v1

- leitor:a16: não tipável (nao_e_prazo_maximo): O prazo de 15 dias é do próprio dono da obra para decidir a reclamação ou se pronunciar, não um prazo máximo para o empreiteiro apresentar algo.
- leitor:b: não tipável (nao_e_prazo_maximo): O prazo é para o dono da obra decidir e notificar o empreiteiro, não para apresentar elementos.

## regra:ccp:auto-prazo-maximo-art354-v20080730@v1

- leitor:a16: não tipável (nao_e_prazo_minimo): O prazo é de caducidade do direito, não um prazo para apresentar algo.
- leitor:b: não tipável (sem_vocabulario): O vocabulário de counted_from não contempla o evento constitutivo do direito nem o momento em que o empreiteiro dele tome conhecimento.
- verificador (B): não tipável: fonte em ccp:art354.2, que é vizinho (L1)

## regra:ccp:auto-prazo-maximo-art354-2@v1

- leitor:a16: não tipável (nao_e_prazo_minimo): O prazo é de caducidade do direito à reposição do equilíbrio financeiro, não um prazo para apresentar algo.
- leitor:b: não tipável (sem_vocabulario): O vocabulário não prevê o início da contagem no evento constitutivo do direito ou no momento em que o empreiteiro dele tome conhecimento.

## regra:ccp:auto-prazo-maximo-art354-4@v1

- leitor:a16: não tipável (nao_e_prazo_maximo): O prazo é da própria entidade adjudicante para decidir a reclamação, não um prazo máximo para os interessados apresentarem algo.
- leitor:b: não tipável (nao_e_prazo_maximo): O prazo é para o dono da obra apreciar e decidir a reclamação, não para apresentar algo.

## regra:ccp:auto-prazo-maximo-art358-2-v20080730@v1

- leitor:a16: não tipável (nao_e_prazo_minimo): O prazo é da própria entidade adjudicante para comunicar ao Instituto da Construção e do Imobiliário, I. P.; não é um prazo para os interessados apresentarem algo.
- leitor:b: não tipável (nao_e_prazo_maximo): O prazo destina-se à comunicação pelo dono da obra, não à apresentação de elementos por um interessado.

## regra:ccp:auto-prazo-maximo-art359-1@v1

- leitor:a16: não tipável (nao_e_prazo_minimo): O prazo é um máximo para a própria entidade adjudicante concluir a consignação, não um prazo para os interessados apresentarem algo.
- leitor:b: não tipável (nao_e_prazo_maximo): O prazo é para concluir a consignação da obra, não para apresentar algo.

## regra:ccp:auto-prazo-maximo-art361-5@v1

- leitor:a16: não tipável (nao_e_prazo_maximo): O prazo é da própria entidade adjudicante para aprovar o plano de trabalhos, não um prazo para o empreiteiro apresentar algo.
- leitor:b: não tipável (nao_e_prazo_maximo): O prazo é para a aprovação do plano de trabalhos pelo dono da obra, não para apresentar algo.

## regra:ccp:auto-prazo-maximo-art366-1@v1

- leitor:a16: não tipável (nao_e_prazo_minimo): O período é o máximo de suspensão, não um prazo para apresentar algo.
- leitor:b: não tipável (nao_e_prazo_maximo): O prazo limita a duração da suspensão dos trabalhos, não sendo um prazo para apresentar nada.

## regra:ccp:auto-prazo-minimo-art366-5@v1

- leitor:a16: não tipável (nao_e_prazo_minimo): O prazo é da própria entidade adjudicante, para a antecipação da comunicação, e não um prazo mínimo para o empreiteiro apresentar algo.
- leitor:b: não tipável (nao_e_prazo_minimo): O prazo fixa a antecedência da comunicação da suspensão pelo empreiteiro, não um prazo para apresentar algo.

## regra:ccp:auto-prazo-maximo-art366-6@v1

- leitor:a16: não tipável (nao_e_prazo_minimo): O prazo é de cinco dias para formalizar a comunicação, não um prazo máximo para a suspensão.
- leitor:b: não tipável (nao_e_prazo_maximo): O prazo destina-se à formalização escrita das comunicações de suspensão, não à apresentação de elementos abrangidos pelos campos de prazo do vocabulário.

## regra:ccp:auto-prazo-maximo-art372-1-v20080730@v1

- leitor:a16: não tipável (nao_e_prazo_minimo): O prazo é de 10 dias para reclamar, não um máximo para apresentar algo.
- leitor:b: não tipável (sem_vocabulario): O vocabulário não prevê como início da contagem a recepção da ordem do dono da obra de execução dos trabalhos a mais.

## regra:ccp:auto-prazo-maximo-art372-1-v20180101@v1

- leitor:a16: não tipável (nao_e_prazo_minimo): O prazo é de 10 dias para reclamar, não um máximo.
- leitor:b: não tipável (sem_vocabulario): O vocabulário não prevê como início da contagem a receção da ordem do dono da obra de execução dos trabalhos complementares.

## regra:ccp:auto-prazo-maximo-art372-1-v20210620@v1

- leitor:a16: não tipável (nao_e_prazo_minimo): O prazo é de 10 dias para reclamar, não um máximo para apresentar algo.
- leitor:b: não tipável (sem_vocabulario): O vocabulário não permite representar os pressupostos da reclamação nem o início da contagem na receção da ordem de execução dos trabalhos complementares.

## regra:ccp:auto-prazo-maximo-art372-1@v1

- leitor:a16: não tipável (nao_e_prazo_minimo): O prazo é de 10 dias, não um máximo.
- leitor:b: não tipável (sem_vocabulario): O vocabulário não permite representar os pressupostos específicos da reclamação nem o início da contagem na receção da ordem de execução dos trabalhos complementares.

## regra:ccp:auto-prazo-maximo-art372-2@v1

- leitor:a16: não tipável (nao_e_prazo_minimo): O prazo é da própria entidade adjudicante para apreciar a reclamação, não um prazo mínimo para os interessados apresentarem algo.
- leitor:b: não tipável (nao_e_prazo_maximo): O prazo é para o dono da obra apreciar a reclamação, não para apresentar algo.

## regra:ccp:auto-prazo-maximo-art373-v20210620@v1

- leitor:a16: não tipável (nao_e_prazo_maximo): Os 15 dias são o prazo do dono da obra para se pronunciar, não um prazo máximo para o empreiteiro apresentar algo.
- leitor:b: não tipável (sem_vocabulario): O vocabulário não permite representar as condições relativas à espécie e à execução dos trabalhos nem o início da contagem na receção do pedido de apresentação da proposta.
- verificador (B): não tipável: fonte em ccp:art373.2, que é vizinho (L1); não tipável: fonte em ccp:art373.1.b, que é vizinho (L1); não tipável: fonte em ccp:art373.2, que é vizinho (L1)

## regra:ccp:auto-prazo-maximo-art373-2-v20080730@v1

- leitor:a16: não tipável (nao_e_prazo_minimo): O prazo é da própria entidade adjudicante para se pronunciar, não um prazo para o empreiteiro apresentar algo.
- leitor:b: não tipável (sem_vocabulario): O vocabulário não permite representar a falta de estipulação contratual nem as condições relativas à espécie dos trabalhos e às condições da sua execução.

## regra:ccp:auto-prazo-maximo-art373-2-v20091007@v1

- leitor:a16: não tipável (nao_e_prazo_minimo): O prazo é de 10 dias para o empreiteiro apresentar a sua proposta, não um prazo máximo para a entidade adjudicante.
- leitor:b: não tipável (sem_vocabulario): O vocabulário não permite representar as condições relativas à estipulação contratual e à espécie e condições de execução dos trabalhos, nem o início da contagem na recepção da ordem de execução.

## regra:ccp:auto-prazo-maximo-art373-2@v1

- leitor:a16: {"tipo": "prazo_maximo", "condicoes": [{"field": "tipo_contrato", "op": "eq", "value": "obras"}, {"field": "tipo_procedimento", "op": "eq", "value": "concurso_publico"}], "params": {"maximum_days": 15, "deadline_field": "prazo_propostas_dias", "counted_from": "data_envio_convite"}}
- leitor:b: não tipável (sem_vocabulario): O vocabulário não permite representar a falta de estipulação contratual, as condições relativas à espécie e execução dos trabalhos nem a contagem desde a receção do pedido.
- verificador (A): regra 1, tipo_procedimento eq concurso_publico: as fontes não nomeiam ['concurso_publico']; regra 1: as fontes de maximum_days não dizem um máximo («não pode ser superior a», «no prazo de», L8); regra 1: deadline_field prazo_propostas_dias e as fontes dizem nada (L9); regra 1: counted_from data_envio_convite e as fontes dizem nada (L9)

## regra:ccp:auto-prazo-maximo-art373-3-v20080730@v1

- leitor:a16: não tipável (nao_e_prazo_maximo): Os 10 dias são o prazo do dono da obra para se pronunciar, não um prazo máximo para o empreiteiro apresentar algo.
- leitor:b: não tipável (nao_e_prazo_maximo): O prazo é para a própria entidade adjudicante se pronunciar sobre a proposta do empreiteiro.

## regra:ccp:auto-prazo-maximo-art373-3@v1

- leitor:a16: {"tipo": "prazo_maximo", "condicoes": [{"field": "tipo_contrato", "op": "eq", "value": "obras"}], "params": {"maximum_days": 15, "deadline_field": "prazo_propostas_dias", "counted_from": "data_notificacao"}}
- leitor:b: não tipável (sem_vocabulario): O vocabulário não permite limitar a regra aos contratos de empreitada de conceção-construção.
- verificador (A): regra 1: as fontes de maximum_days não dizem um máximo («não pode ser superior a», «no prazo de», L8); regra 1: deadline_field prazo_propostas_dias e as fontes dizem nada (L9); regra 1: counted_from data_notificacao e as fontes dizem nada (L9)

## regra:ccp:auto-prazo-maximo-art373-5@v1

- leitor:a16: não tipável (nao_e_prazo_maximo): Os 15 dias são o prazo do dono da obra para se pronunciar, não um prazo para o empreiteiro apresentar algo.
- leitor:b: não tipável (nao_e_prazo_maximo): O prazo é para a própria entidade adjudicante se pronunciar sobre a proposta do empreiteiro.

## regra:ccp:auto-prazo-maximo-art376-6-v20080730@v1

- leitor:a16: não tipável (nao_e_prazo_minimo): O prazo é da própria entidade adjudicante para pronunciar-se, não um prazo para o empreiteiro apresentar algo.
- leitor:b: não tipável (nao_e_prazo_maximo): O prazo é para o dono da obra se pronunciar e comunicar a sua posição ao empreiteiro, sendo um prazo para a própria entidade adjudicante.

## regra:ccp:auto-prazo-maximo-art376-7-v20120811@v1

- leitor:a16: não tipável (nao_e_prazo_minimo): O prazo é da própria entidade adjudicante para se pronunciar, não um prazo para o empreiteiro apresentar algo.
- leitor:b: não tipável (nao_e_prazo_maximo): O prazo é para a própria entidade adjudicante se pronunciar e comunicar a sua posição ao empreiteiro.

## regra:ccp:auto-prazo-maximo-art378-3-v20180101@v1

- leitor:a16: não tipável (nao_e_prazo_minimo): O prazo é de 60 dias para reclamar, não um mínimo.
- leitor:b: não tipável (sem_vocabulario): O vocabulário não prevê a consignação como início da contagem nem a exclusão dos erros ou omissões só detetáveis durante a execução da obra.

## regra:ccp:auto-prazo-maximo-art378-4-v20080730@v1

- leitor:a16: não tipável (nao_e_prazo_minimo): O prazo é o de apresentação das correções, não um prazo mínimo para a entidade adjudicante.
- leitor:b: não tipável (nao_e_prazo_maximo): O prazo respeita à identificação de erros e omissões pelo empreiteiro, não à apresentação de elementos.

## regra:ccp:auto-prazo-maximo-art378-4-v20120811@v1

- leitor:a16: não tipável (nao_e_prazo_minimo): O prazo é de 30 dias, e não é um mínimo para apresentar algo.
- leitor:b: não tipável (nao_e_prazo_maximo): O prazo refere-se à identificação de erros e omissões pelo empreiteiro, não à apresentação de elementos.

## regra:ccp:auto-prazo-maximo-art378-4-v20180101@v1

- leitor:a16: não tipável (nao_e_prazo_minimo): O prazo é de 30 dias, um máximo para o empreiteiro não apresentar os trabalhos complementares, não um prazo para apresentar algo.
- leitor:b: não tipável (nao_e_prazo_maximo): O prazo é para identificar erros e omissões, não para apresentar algo.

## regra:ccp:auto-prazo-maximo-art378-4@v1

- leitor:a16: não tipável (nao_e_prazo_minimo): O prazo é do próprio empreiteiro para reclamar, não um prazo mínimo para os interessados apresentarem algo.
- leitor:b: não tipável (sem_vocabulario): O vocabulário não prevê este início da contagem nem a condição de os erros ou omissões serem só detetáveis nesse momento.

## regra:ccp:auto-prazo-maximo-art378-5@v1

- leitor:a16: não tipável (sem_vocabulario): A regra só vale para os trabalhos complementares de suprimento de erros e omissões, facto que o vocabulário não tem.
- leitor:b: não tipável (nao_e_prazo_maximo): O prazo refere-se à identificação de erros e omissões pelo empreiteiro, não à apresentação de elementos.

## regra:ccp:auto-prazo-maximo-art385-v20230715@v1

- leitor:a16: não tipável (nao_e_prazo_minimo): O prazo é de cinco dias, um máximo para o próprio empreiteiro comunicar a subempreitada, e não um prazo para apresentar algo.
- leitor:b: não tipável (nao_e_prazo_maximo): O prazo destina-se à comunicação da celebração de uma subempreitada ao dono da obra, e não a uma apresentação prevista no vocabulário.
- verificador (B): não tipável: fonte em ccp:art385.3, que é vizinho (L1)

## regra:ccp:auto-prazo-maximo-art385-3-v20080730@v1

- leitor:a16: não tipável (nao_e_prazo_minimo): O prazo é de cinco dias, e não um mínimo.
- leitor:b: não tipável (nao_e_prazo_maximo): O prazo destina-se à comunicação da celebração de uma subempreitada ao dono da obra, não a uma apresentação abrangida pelos campos de prazo.

## regra:ccp:auto-prazo-maximo-art385-3@v1

- leitor:a16: não tipável (nao_e_prazo_minimo): O prazo é de cinco dias, e não um mínimo.
- leitor:b: não tipável (nao_e_prazo_maximo): O prazo destina-se à comunicação da celebração de uma subempreitada, não à apresentação de elementos abrangidos pelos campos de prazo.

## regra:ccp:auto-prazo-maximo-art386-2@v1

- leitor:a16: não tipável (nao_e_prazo_minimo): O prazo é da própria entidade adjudicante para comunicar ao instituto, não um prazo para os interessados apresentarem algo.
- leitor:b: não tipável (nao_e_prazo_maximo): O prazo destina-se a uma comunicação do dono da obra, não à apresentação de elementos.

## regra:ccp:auto-prazo-maximo-art389-1@v1

- leitor:a16: não tipável (nao_e_prazo_minimo): O prazo é da própria entidade adjudicante para elaborar a conta corrente, não um prazo para os interessados apresentarem algo.
- leitor:b: não tipável (nao_e_prazo_maximo): O prazo é para elaborar a conta corrente, não para apresentar algo.

## regra:ccp:auto-prazo-minimo-art394-3@v1

- leitor:a16: não tipável (nao_e_prazo_minimo): O prazo é uma antecedência mínima do dono da obra para convocar o empreiteiro, não um prazo para o empreiteiro apresentar algo.
- leitor:b: não tipável (nao_e_prazo_minimo): A passagem fixa uma antecedência mínima para convocar o empreiteiro para a vistoria, não um prazo para apresentar algo.

## regra:ccp:auto-prazo-maximo-art394-5@v1

- leitor:a16: não tipável (nao_e_prazo_minimo): O prazo é do próprio dono da obra para realizar a vistoria, não um prazo para os interessados apresentarem algo.
- leitor:b: não tipável (nao_e_prazo_maximo): O prazo é para o dono da obra realizar a vistoria, não para apresentar algo.

## regra:ccp:auto-prazo-maximo-art394-7@v1

- leitor:a16: não tipável (nao_e_prazo_maximo): O prazo é o de não agendamento da vistoria pelo dono da obra; falta um prazo para apresentar algo.
- leitor:b: não tipável (nao_e_prazo_maximo): O prazo destina-se ao agendamento ou à realização da vistoria pelo dono da obra, não à apresentação de elementos.

## regra:ccp:auto-prazo-maximo-art401-1@v1

- leitor:a16: não tipável (nao_e_prazo_minimo): O prazo é da própria entidade adjudicante para enviar a conta final, não um prazo para o empreiteiro apresentar algo.
- leitor:b: {"tipo": "prazo_maximo", "condicoes": [{"field": "tipo_contrato", "op": "eq", "value": "obras"}], "params": {"maximum_days": 15, "deadline_field": "prazo_reclamacao_dias", "counted_from": "nao_indicado"}}

## regra:ccp:auto-prazo-maximo-art401-3@v1

- leitor:a16: não tipável (nao_e_prazo_minimo): O prazo é do próprio dono da obra para comunicar a decisão, não um prazo para o empreiteiro apresentar algo.
- leitor:b: não tipável (nao_e_prazo_maximo): O prazo destina-se à comunicação da decisão pelo dono da obra, não à apresentação de elementos pelo interessado.

## regra:ccp:auto-prazo-maximo-art402-1@v1

- leitor:a16: não tipável (nao_e_prazo_minimo): O prazo é de 10 dias, não um máximo.
- leitor:b: não tipável (nao_e_prazo_maximo): O prazo é para o dono da obra enviar o relatório final da obra, obrigação da própria entidade adjudicante.

## regra:ccp:auto-prazo-maximo-art404-1@v1

- leitor:a16: não tipável (nao_e_prazo_minimo): O prazo é do próprio dono da obra para notificar o empreiteiro, não um prazo para o empreiteiro apresentar algo.
- leitor:b: não tipável (sem_vocabulario): O vocabulário não contém um campo de prazo para a apresentação de um plano de trabalhos modificado.

## regra:ccp:auto-prazo-maximo-art405-v20080730@v1

- leitor:a16: não tipável (nao_e_prazo_minimo): O atraso é de quem não dá início à obra; falta um prazo máximo para apresentar algo.
- leitor:b: não tipável (nao_e_prazo_maximo): A passagem fixa fundamentos de resolução do contrato, não um prazo máximo para apresentar algo.
- verificador (B): não tipável: fonte em ccp:art405.1, que é vizinho (L1); não tipável: fonte em ccp:art405.1.d, que é vizinho (L1)

## regra:ccp:auto-prazo-maximo-art405-v20210620@v1

- leitor:a16: não tipável (nao_e_prazo_maximo): O prazo é de 15 dias, contados da notificação da decisão do dono da obra que indefere a reclamação, e é o tempo que o dono da obra pode esperar a apresentação de um plano de trabalhos modificado. Não é um prazo máximo para a apresentação de algo.
- leitor:b: não tipável (nao_e_prazo_maximo): O prazo refere-se ao início da execução dos trabalhos, não à apresentação de elementos.
- verificador (B): não tipável: fonte em ccp:art405.1.d, que é vizinho (L1)

## regra:ccp:auto-prazo-maximo-art405-1-d@v1

- leitor:a16: não tipável (nao_e_prazo_minimo): O prazo é de 15 dias para o dono da obra não iniciar a execução, não um prazo para os interessados apresentarem algo.
- leitor:b: não tipável (nao_e_prazo_maximo): O prazo refere-se ao início da execução dos trabalhos, não à apresentação de qualquer elemento.

## regra:ccp:auto-prazo-maximo-art405-2@v1

- leitor:a16: não tipável (nao_e_prazo_minimo): O prazo é da própria entidade adjudicante para informar o Instituto dos Mercados Públicos, do Imobiliário e da Construção, I. P.; não é um prazo para os interessados apresentarem algo.
- leitor:b: não tipável (nao_e_prazo_maximo): O prazo destina-se ao cumprimento de um dever de informação pelo dono da obra, não à apresentação de elementos pelos interessados.

## regra:ccp:auto-prazo-maximo-art406-b@v1

- leitor:a16: não tipável (nao_e_prazo_minimo): O prazo é de mais de 120 dias, não um mínimo.
- leitor:b: não tipável (nao_e_prazo_maximo): Os 120 dias constituem um fundamento de resolução pelo empreiteiro, não um prazo para apresentar algo.

## regra:ccp:auto-prazo-maximo-art464-a-v20210620@v1

- leitor:a16: não tipável (nao_e_prazo_minimo): O prazo é de um ano, período durante o qual a sanção pode ser aplicada, e não um prazo para apresentar algo.
- leitor:b: não tipável (nao_e_prazo_maximo): Os prazos fixam a duração de uma sanção e uma obrigação de comunicação dos contraentes públicos, não um prazo máximo para apresentação de elementos pelos participantes.
- verificador (B): não tipável: fonte em ccp:art464-a.1, que é vizinho (L1); não tipável: fonte em ccp:art464-a.2, que é vizinho (L1)

## regra:ccp:auto-prazo-maximo-art464-a-2-v20180101@v1

- leitor:a16: não tipável (nao_e_prazo_minimo): O prazo é da própria entidade pública para comunicar, não um prazo para os contraentes apresentarem algo.
- leitor:b: não tipável (nao_e_prazo_maximo): O prazo destina-se à comunicação de situações de incumprimento pelos contraentes públicos.

## regra:ccp:auto-prazo-maximo-art464-e-2@v1

- leitor:a16: não tipável (nao_e_prazo_minimo): O prazo é da própria parte requerida para responder, não um prazo para apresentar algo.
- leitor:b: não tipável (sem_vocabulario): O vocabulário não contém um campo de prazo para apresentar resposta e indicar um membro para a comissão.

## regra:ccp:auto-prazo-maximo-art464-e-3@v1

- leitor:a16: não tipável (nao_e_prazo_minimo): O prazo é um máximo para a própria comissão fazer a tentativa de conciliação, não um prazo para as partes apresentarem algo.
- leitor:b: não tipável (nao_e_prazo_maximo): O prazo é para a realização da tentativa de conciliação, não para apresentar algo.

## regra:ccp:auto-prazo-maximo-art464-g@v1

- leitor:a16: não tipável (nao_e_prazo_minimo): O prazo é de prescrição, não um prazo para apresentar algo.
- leitor:b: não tipável (nao_e_prazo_maximo): Os 30 dias determinam o reinício dos prazos de prescrição e de caducidade, não um prazo máximo para apresentar algo.

## regra:eu-1989-665:auto-prazo-minimo-art1-5@v1

- leitor:a16: não tipável (sem_vocabulario): A suspensão é fixada em dias, mas depende do meio de comunicação e não é um prazo para apresentar algo.
- leitor:b: não tipável (nao_e_prazo_minimo): O prazo fixa a duração da suspensão da possibilidade de celebrar o contrato, não um prazo para apresentar algo.

## regra:eu-1989-665:auto-prazo-minimo-art2-a-2@v1

- leitor:a16: não tipável (texto_em_falta): Os dias do prazo suspensivo começam na data em que a decisão de adjudicação é recebida, facto que não está no texto mostrado.
- leitor:b: não tipável (nao_e_prazo_minimo): O prazo suspende a celebração do contrato; não é um prazo para apresentar nada.

## regra:eu-1989-665:auto-prazo-minimo-art2-c@v1

- leitor:a16: não tipável (nao_e_prazo_minimo): O prazo é o mínimo para interpor um recurso, não um prazo para apresentar algo no procedimento.
- leitor:b: não tipável (sem_vocabulario): O vocabulário não contém um campo de prazo para a interposição de recurso.
- verificador (B): não tipável: «Prazos para interposição de recurso» não está em eu-1989-665:art2-c

## regra:eu-1989-665:auto-prazo-minimo-art2-d-4@v1

- leitor:a16: não tipável (nao_e_prazo_minimo): O prazo é fixado só quando a adjudicação sem publicação prévia de anúncio é permitida; falta um procedimento que dependa dele.
- leitor:b: não tipável (nao_e_prazo_minimo): O prazo limita a celebração do contrato pela entidade adjudicante; não é um prazo para apresentar nada.

## regra:eu-1989-665:auto-prazo-minimo-art2-d-5@v1

- leitor:a16: não tipável (texto_em_falta): Os dias do prazo mínimo só estão fixados para os meios de comunicação: telecópia ou outros meios, e não estão no texto mostrado.
- leitor:b: não tipável (nao_e_prazo_minimo): O prazo é de espera para a celebração do contrato, não para apresentar algo.

## regra:eu-1989-665:auto-prazo-minimo-art2-f-1-a@v1

- leitor:a16: não tipável (sem_vocabulario): O prazo é fixado em meses, unidade que o vocabulário não tem.
- leitor:b: não tipável (sem_vocabulario): O vocabulário não prevê um campo de prazo para a apresentação de pedidos de recurso.

## regra:eu-1989-665:auto-prazo-maximo-art3-3@v1

- leitor:a16: não tipável (nao_e_prazo_minimo): O prazo é de 21 dias, não um mínimo.
- leitor:b: não tipável (nao_e_prazo_maximo): O prazo destina-se à comunicação do Estado-Membro à Comissão, não à apresentação de elementos por participantes num procedimento de contratação.

## regra:eu-1992-13:auto-prazo-minimo-art1-5@v1

- leitor:a16: não tipável (sem_vocabulario): A suspensão é fixada em dias, mas depende do meio de comunicação e não é um prazo para apresentar algo.
- leitor:b: não tipável (nao_e_prazo_minimo): O prazo regula a suspensão da possibilidade de celebrar o contrato, não a apresentação de qualquer elemento.

## regra:eu-1992-13:auto-prazo-minimo-art2-a-2@v1

- leitor:a16: não tipável (texto_em_falta): Os dias do prazo suspensivo estão na decisão de adjudicação, que não é mostrada.
- leitor:b: não tipável (nao_e_prazo_minimo): A passagem fixa um prazo suspensivo para a celebração do contrato, não um prazo para apresentar algo.

## regra:eu-1992-13:auto-prazo-minimo-art2-c@v1

- leitor:a16: não tipável (texto_em_falta): Os dias em que se conta o prazo estão na alínea b) do n.º 1 do artigo 2.º, que não está mostrada.
- leitor:b: não tipável (sem_vocabulario): O vocabulário não prevê um campo de prazo para a interposição de recurso.
- verificador (B): não tipável: «Prazos para interposição de recurso» não está em eu-1992-13:art2-c

## regra:eu-1992-13:auto-prazo-minimo-art2-d-4@v1

- leitor:a16: não tipável (sem_vocabulario): A regra é de um procedimento que não está na lista do vocabulário: a privação de efeitos do contrato.
- leitor:b: não tipável (nao_e_prazo_minimo): O prazo regula a espera para a celebração do contrato, não a apresentação de elementos.

## regra:eu-1992-13:auto-prazo-minimo-art2-d-5@v1

- leitor:a16: não tipável (texto_em_falta): Os dias do prazo mínimo quando a decisão de adjudicação é enviada por telecópia ou por meios electrónicos não estão no texto mostrado.
- leitor:b: não tipável (nao_e_prazo_minimo): O prazo limita a celebração do contrato pela entidade adjudicante e não se destina à apresentação de nada.

## regra:eu-1992-13:auto-prazo-minimo-art2-f-1-a@v1

- leitor:a16: não tipável (sem_vocabulario): A contagem do prazo começa pelo dia seguinte à publicação do anúncio, facto que nenhum campo do vocabulário tem.
- leitor:b: não tipável (sem_vocabulario): O vocabulário não contém um campo para o prazo de apresentação de pedidos de recurso.

## regra:eu-1992-13:auto-prazo-maximo-art8-3@v1

- leitor:a16: não tipável (nao_e_prazo_minimo): O prazo é de 21 dias, não um máximo.
- leitor:b: não tipável (nao_e_prazo_maximo): O prazo destina-se a uma comunicação do Estado-Membro à Comissão, não à apresentação de elementos num procedimento de contratação.

## regra:eu-2004-17:auto-prazo-maximo-art15-4-v20041101@v1

- leitor:a16: não tipável (sem_vocabulario): A regra é de um sistema de aquisição dinâmico, instrumento que o vocabulário não tem.
- leitor:b: não tipável (nao_e_prazo_maximo): O prazo é para a entidade adjudicante concluir a avaliação, não para apresentar algo.

## regra:eu-2004-17:auto-prazo-minimo-art15-5-v20041101@v1

- leitor:a16: não tipável (sem_vocabulario): A regra é de um sistema de aquisição dinâmico, instrumento que o vocabulário não tem.
- leitor:b: não tipável (sem_vocabulario): O vocabulário não permite limitar a regra aos sistemas de aquisição dinâmicos.

## regra:eu-2004-17:auto-limiar-art16-a-v20160101@v1

- leitor:a16: {"tipo": "limiar", "condicoes": [{"field": "tipo_contrato", "op": "eq", "value": "bens"}, {"field": "tipo_procedimento", "op": "in", "value": ["ajuste_direto", "concurso_aberto", "concurso_publico", "concurso_publico_urgente", "consulta_previa", "consulta_previa_especial", "procedimento_concorrencial_negociacao", "procedimento_negociacao", "procedimento_negociacao_com_concurso"]}], "params": {"threshold": {"field": "valor_estimado", "comparator": "ge", "value": 418000, "currency": "EUR"}}}
- leitor:b: não tipável (nao_e_limiar): O valor delimita a aplicação da diretiva, não o limite até ao qual um procedimento pode ser escolhido.
- verificador (A): regra 1, tipo_contrato eq bens: as fontes não nomeiam ['bens']; regra 1, tipo_procedimento in ['ajuste_direto', 'concurso_aberto', 'concurso_publico', 'concurso_publico_urgente', 'consulta_previa', 'consulta_previa_especial', 'procedimento_concorrencial_negociacao', 'procedimento_negociacao', 'procedimento_negociacao_com_concurso']: as fontes não nomeiam ['ajuste_direto', 'concurso_aberto', 'concurso_publico', 'concurso_publico_urgente', 'consulta_previa', 'consulta_previa_especial', 'procedimento_concorrencial_negociacao', 'procedimento_negociacao', 'procedimento_negociacao_com_concurso']; regra 1: value 418000 não está nas fontes (L10)

## regra:eu-2004-17:auto-limiar-art16-b-v20160101@v1

- leitor:a16: {"tipo": "limiar", "condicoes": [{"field": "tipo_contrato", "op": "eq", "value": "obras"}], "params": {"threshold": {"field": "valor_estimado", "comparator": "ge", "value": 5225000, "currency": "EUR"}}}
- leitor:b: não tipável (nao_e_limiar): O valor delimita a aplicação da diretiva, não o limite até ao qual um procedimento pode ser escolhido.
- verificador (A): regra 1: um limiar tem sempre o procedimento que permite abaixo do valor; sem ele, L12 (nao_e_limiar); regra 1: value 5225000 não está nas fontes (L10)

## regra:eu-2004-17:auto-limiar-art17-6-b-v20090101@v1

- leitor:a16: não tipável (nao_e_limiar): O valor é somado para os lotes; não é o limite até ao qual um procedimento pode ser escolhido.
- leitor:b: não tipável (nao_e_limiar): O valor permite derrogar a aplicação da diretiva a lotes, não fixa um limite até ao qual um procedimento pode ser escolhido.

## regra:eu-2004-17:auto-limiar-art41-1-a-v20041101@v1

- leitor:a16: não tipável (sem_vocabulario): A regra só vale para acordos-quadro de fornecimentos por grupos de produtos, instrumento que o vocabulário não tem.
- leitor:b: não tipável (nao_e_limiar): O valor agrega vários contratos ou acordos-quadro para efeitos de anúncio periódico indicativo; não fixa um limite para a escolha de um procedimento.

## regra:eu-2004-17:auto-limiar-art41-1-b-v20041101@v1

- leitor:a16: não tipável (texto_em_falta): Os valores dos contratos por cada categoria de serviços estão no anexo XVII A, que não é mostrado.
- leitor:b: não tipável (nao_e_limiar): O montante refere-se ao valor agregado dos contratos a divulgar num anúncio periódico indicativo, sem fixar um limite para a escolha de um procedimento.

## regra:eu-2004-17:auto-prazo-maximo-art44-3-v20041101@v1

- leitor:a16: não tipável (sem_vocabulario): O prazo é fixado em dias, mas o instrumento em que se aplica é o anúncio eletrónico, que o vocabulário não tem.
- leitor:b: não tipável (nao_e_prazo_maximo): O prazo é para a publicação de anúncios, não para apresentar elementos pelos interessados.

## regra:eu-2004-17:auto-prazo-minimo-art45-2-v20041101@v1

- leitor:a16: {"tipo": "prazo_minimo", "condicoes": [{"field": "tipo_procedimento", "op": "eq", "value": "concurso_publico"}], "params": {"minimum_days": 52, "deadline_field": "prazo_propostas_dias", "counted_from": "data_envio_anuncio", "usual_days": null}}
- leitor:b: {"tipo": "prazo_minimo", "condicoes": [{"field": "tipo_procedimento", "op": "eq", "value": "concurso_publico"}], "params": {"minimum_days": 52, "deadline_field": "prazo_propostas_dias", "counted_from": "data_envio_anuncio", "usual_days": null}}

## regra:eu-2004-17:auto-prazo-minimo-art45-3-a-v20041101@v1

- leitor:a16: {"tipo": "prazo_minimo", "condicoes": [{"field": "tipo_procedimento", "op": "in", "value": ["concurso_limitado_previa_qualificacao", "procedimento_concorrencial_negociacao", "procedimento_negociacao_com_concurso"]}], "params": {"minimum_days": 37, "deadline_field": "prazo_reclamacao_dias", "counted_from": "data_envio_anuncio", "usual_days": null}}
- leitor:b: não tipável (sem_vocabulario): O vocabulário não permite distinguir o envio do anúncio por meios electrónicos ou fax do envio por outros meios, condição que determina os mínimos de 15 ou 22 dias.
- verificador (A): regra 1, tipo_procedimento in ['concurso_limitado_previa_qualificacao', 'procedimento_concorrencial_negociacao', 'procedimento_negociacao_com_concurso']: as fontes não nomeiam ['procedimento_concorrencial_negociacao', 'procedimento_negociacao_com_concurso']; regra 1: deadline_field prazo_reclamacao_dias e as fontes dizem ['prazo_candidaturas_dias'] (L9); regra 1: counted_from data_envio_anuncio e as fontes dizem nada (L9)

## regra:eu-2004-17:auto-prazo-minimo-art45-3-c-v20041101@v1

- leitor:a16: {"tipo": "prazo_minimo", "condicoes": [{"field": "tipo_procedimento", "op": "in", "value": ["concurso_limitado_previa_qualificacao", "procedimento_concorrencial_negociacao", "procedimento_negociacao"]}], "params": {"minimum_days": 24, "deadline_field": "prazo_reclamacao_dias", "counted_from": "data_envio_convite", "usual_days": null}}
- leitor:b: não tipável (sem_vocabulario): Falta um campo que represente a impossibilidade de acordo sobre o prazo de recepção das propostas.
- verificador (A): regra 1, tipo_procedimento in ['concurso_limitado_previa_qualificacao', 'procedimento_concorrencial_negociacao', 'procedimento_negociacao']: as fontes não nomeiam ['procedimento_concorrencial_negociacao', 'procedimento_negociacao']; regra 1: deadline_field prazo_reclamacao_dias e as fontes dizem ['prazo_propostas_dias'] (L9); regra 1: counted_from data_envio_convite e as fontes dizem nada (L9)

## regra:eu-2004-17:auto-prazo-minimo-art45-4-v20041101@v1

- leitor:a16: {"tipo": "prazo_minimo", "condicoes": [{"field": "anuncio_pre_informacao", "op": "eq", "value": true}, {"field": "tipo_procedimento", "op": "eq", "value": "concurso_publico"}], "params": {"minimum_days": 36, "deadline_field": "prazo_propostas_dias", "counted_from": "data_envio_anuncio", "usual_days": null}}
- leitor:b: não tipável (sem_vocabulario): O vocabulário não permite representar a condição de antecedência do envio do anúncio periódico indicativo relativamente ao envio do anúncio de concurso.
- verificador (A): regra 1: deadline_field prazo_propostas_dias e as fontes dizem nada (L9)

## regra:eu-2004-17:auto-prazo-maximo-art45-5-v20041101@v1

- leitor:a16: {"tipo": "prazo_maximo", "condicoes": [{"field": "tipo_procedimento", "op": "eq", "value": "concurso_publico"}], "params": {"maximum_days": 19, "deadline_field": "prazo_reclamacao_dias", "counted_from": "nao_indicado"}}
- leitor:b: não tipável (nao_e_prazo_maximo): A passagem permite uma redução dos prazos, mas não fixa um prazo máximo.
- verificador (A): regra 1: maximum_days 19 não está nas fontes (L8, L4); regra 1: deadline_field prazo_reclamacao_dias e as fontes dizem ['prazo_propostas_dias'] (L9)

## regra:eu-2004-17:auto-prazo-maximo-art45-6-v20041101@v1

- leitor:a16: não tipável (nao_e_prazo_maximo): O prazo é uma redução, não um máximo.
- leitor:b: não tipável (nao_e_prazo_maximo): A passagem permite reduzir prazos mínimos de recepção das propostas, mas não fixa um prazo máximo.

## regra:eu-2004-17:auto-prazo-minimo-art45-7-v20041101@v1

- leitor:a16: {"tipo": "prazo_minimo", "condicoes": [{"field": "tipo_procedimento", "op": "eq", "value": "concurso_publico"}], "params": {"minimum_days": 15, "deadline_field": "prazo_propostas_dias", "counted_from": "data_envio_anuncio", "usual_days": null}}
- leitor:b: não tipável (sem_vocabulario): Falta um campo para distinguir o envio do anúncio por fax ou por meios electrónicos do envio por outros meios, necessário para separar os mínimos de 15 e 22 dias.

## regra:eu-2004-17:auto-prazo-minimo-art45-8-v20041101@v1

- leitor:a16: não tipável (nao_e_prazo_minimo): O limite é um prazo máximo para a recepção dos pedidos de participação, não um prazo mínimo.
- leitor:b: não tipável (sem_vocabulario): O vocabulário não permite representar a acumulação das reduções nem a exceção dos prazos fixados de comum acordo.

## regra:eu-2004-17:auto-prazo-maximo-art46-1-v20041101@v1

- leitor:a16: não tipável (nao_e_prazo_minimo): O prazo é da própria entidade adjudicante para enviar os documentos, não um prazo mínimo para os operadores económicos apresentarem algo.
- leitor:b: não tipável (nao_e_prazo_maximo): O prazo é para a entidade adjudicante enviar os cadernos de encargos e os documentos complementares aos operadores económicos.

## regra:eu-2004-17:auto-prazo-maximo-art46-2-v20041101@v1

- leitor:a16: não tipável (nao_e_prazo_maximo): O prazo é da própria entidade adjudicante para comunicar as informações, não um prazo para os operadores apresentarem algo.
- leitor:b: não tipável (nao_e_prazo_maximo): O prazo é para as próprias entidades adjudicantes ou os serviços competentes comunicarem informações complementares.

## regra:eu-2004-17:auto-prazo-maximo-art47-3-v20041101@v1

- leitor:a16: não tipável (nao_e_prazo_maximo): O prazo é um máximo das entidades adjudicantes para comunicarem informações, não um prazo para os interessados apresentarem algo.
- leitor:b: não tipável (nao_e_prazo_maximo): O prazo é para as entidades adjudicantes ou os serviços competentes comunicarem informações complementares.

## regra:eu-2004-17:auto-prazo-maximo-art49-2-v20041101@v1

- leitor:a16: não tipável (nao_e_prazo_maximo): O prazo é um máximo de 15 dias para a comunicação das entidades adjudicantes, não um prazo para os interessados apresentarem algo.
- leitor:b: não tipável (nao_e_prazo_maximo): O prazo é para a própria entidade adjudicante comunicar informações.

## regra:eu-2004-17:auto-prazo-maximo-art49-4-v20041101@v1

- leitor:a16: não tipável (sem_vocabulario): A regra é de um sistema de qualificação, instrumento que o vocabulário não tem.
- leitor:b: não tipável (nao_e_prazo_maximo): O prazo destina-se à entidade adjudicante informar os requerentes da recusa de qualificação, não à apresentação de elementos pelos interessados.

## regra:eu-2004-17:auto-prazo-minimo-art49-5-v20041101@v1

- leitor:a16: não tipável (sem_vocabulario): A regra só vale para os critérios de qualificação, instrumento que o vocabulário não tem.
- leitor:b: não tipável (nao_e_prazo_minimo): O prazo é para a entidade adjudicante notificar a intenção de pôr termo à qualificação, não para apresentar algo.

## regra:eu-2004-17:auto-prazo-maximo-art56-4-v20041101@v1

- leitor:a16: não tipável (sem_vocabulario): A regra vale só para o leilão eletrónico, instrumento que o vocabulário não tem.
- leitor:b: não tipável (nao_e_prazo_maximo): A passagem fixa um prazo mínimo para o início do leilão electrónico, não um prazo máximo para apresentar elementos.

## regra:eu-2004-17:auto-limiar-art61-1-v20160101@v1

- leitor:a16: {"tipo": "limiar", "condicoes": [{"field": "tipo_contrato", "op": "eq", "value": "servicos"}, {"field": "tipo_procedimento", "op": "eq", "value": "concurso_concecao"}], "params": {"threshold": {"field": "valor_estimado", "comparator": "ge", "value": 418000, "currency": "EUR"}}}
- leitor:b: não tipável (nao_e_limiar): O valor determina a aplicação do Título III, não um limite até ao qual um procedimento pode ser escolhido.
- verificador (A): regra 1, tipo_procedimento eq concurso_concecao: as fontes não nomeiam ['concurso_concecao']; regra 1: value 418000 não está nas fontes (L10)

## regra:eu-2004-17:auto-limiar-art61-2-v20160101@v1

- leitor:a16: não tipável (texto_em_falta): Os valores dos contratos que possam ser somados para atingir o limiar estão no n.º 3 do artigo 40.º, que não é mostrado.
- leitor:b: não tipável (nao_e_limiar): O valor fixa o âmbito de aplicação do Título III, não um limite até ao qual um procedimento pode ser escolhido.

## regra:eu-2004-17:auto-limiar-art69-1-v20090807@v1

- leitor:a16: não tipável (texto_em_falta): O valor dos limiares revistos é o contravalor do euro, que não está no texto mostrado.
- leitor:b: não tipável (nao_e_limiar): A passagem regula a verificação e revisão dos limiares, sem fixar um valor até ao qual um procedimento pode ser escolhido.

## regra:eu-2004-17:auto-limiar-art69-2-v20090807@v1

- leitor:a16: não tipável (nao_e_limiar): O valor alinha os limiares de um procedimento com o de outro; não é o limite até ao qual um procedimento pode ser escolhido.
- leitor:b: não tipável (nao_e_limiar): A passagem regula a revisão e o alinhamento dos limiares, sem fixar um valor até ao qual um procedimento pode ser escolhido.

## regra:eu-2004-18:auto-limiar-art7-a-v20160101@v1

- leitor:a16: {"tipo": "limiar", "condicoes": [{"field": "tipo_contrato", "op": "in", "value": ["bens", "servicos"]}, {"field": "tipo_entidade", "op": "eq", "value": "estado"}], "params": {"threshold": {"field": "valor_estimado", "comparator": "ge", "value": 135000, "currency": "EUR"}}}
- leitor:b: não tipável (nao_e_limiar): O valor delimita a aplicação da diretiva, não o limite até ao qual um procedimento pode ser escolhido.
- verificador (A): regra 1, tipo_contrato in ['bens', 'servicos']: as fontes não nomeiam ['bens']; regra 1, tipo_entidade eq estado: as fontes não nomeiam ['estado']; regra 1: um limiar tem sempre o procedimento que permite abaixo do valor; sem ele, L12 (nao_e_limiar); regra 1: value 135000 não está nas fontes (L10)

## regra:eu-2004-18:auto-limiar-art7-b-v20160101@v1

- leitor:a16: {"tipo": "limiar", "condicoes": [{"field": "tipo_contrato", "op": "in", "value": ["bens", "servicos"]}, {"field": "tipo_entidade", "op": "eq", "value": "outra"}], "params": {"threshold": {"field": "valor_estimado", "comparator": "ge", "value": 209000, "currency": "EUR"}}}
- leitor:b: não tipável (nao_e_limiar): O valor delimita a aplicação da diretiva, não o valor até ao qual um procedimento pode ser escolhido.
- verificador (A): regra 1, tipo_contrato in ['bens', 'servicos']: as fontes não nomeiam ['bens']; regra 1, tipo_entidade eq outra: as fontes não nomeiam ['outra']; regra 1: um limiar tem sempre o procedimento que permite abaixo do valor; sem ele, L12 (nao_e_limiar); regra 1: field valor_estimado e as fontes nomeiam nada (L10); regra 1: value 209000 não está nas fontes (L10)

## regra:eu-2004-18:auto-limiar-art7-c-v20160101@v1

- leitor:a16: {"tipo": "limiar", "condicoes": [{"field": "tipo_contrato", "op": "eq", "value": "obras"}], "params": {"threshold": {"field": "valor_estimado", "comparator": "ge", "value": 5225000, "currency": "EUR"}}}
- leitor:b: não tipável (nao_e_limiar): O montante delimita a aplicação da diretiva, não o valor até ao qual um procedimento pode ser escolhido.
- verificador (A): regra 1: um limiar tem sempre o procedimento que permite abaixo do valor; sem ele, L12 (nao_e_limiar); regra 1: value 5225000 não está nas fontes (L10)

## regra:eu-2004-18:auto-limiar-art8-a-v20160101@v1

- leitor:a16: não tipável (nao_e_limiar): o valor não é o limite até ao qual um procedimento pode ser escolhido
- leitor:b: não tipável (nao_e_limiar): O valor delimita a aplicação da diretiva, não o limite até ao qual um procedimento pode ser escolhido.

## regra:eu-2004-18:auto-limiar-art8-b-v20160101@v1

- leitor:a16: não tipável (nao_e_limiar): O valor não é o limite até ao qual um procedimento pode ser escolhido.
- leitor:b: não tipável (nao_e_limiar): O valor delimita a aplicação da diretiva, não o limite até ao qual um procedimento pode ser escolhido.

## regra:eu-2004-18:auto-limiar-art9-4-a-v20040430@v1

- leitor:a16: não tipável (sem_vocabulario): A regra só vale para a adjudicação simultânea de contratos por lotes separados, facto que nenhum campo do vocabulário tem.
- leitor:b: não tipável (nao_e_limiar): Os valores delimitam uma derrogação à aplicação da diretiva a lotes, sem fixarem um limite para a escolha de um procedimento.

## regra:eu-2004-18:auto-limiar-art9-4-b-v20040430@v1

- leitor:a16: não tipável (texto_em_falta): Os valores dos lotes estão no artigo 7.º, que não é mostrado.
- leitor:b: não tipável (nao_e_limiar): O valor permite derrogar a aplicação da diretiva a certos lotes; não fixa um limite até ao qual um procedimento pode ser escolhido.

## regra:eu-2004-18:auto-limiar-art9-5-b-v20041101@v1

- leitor:a16: não tipável (sem_vocabulario): A regra depende da percentagem do valor cumulado dos lotes, facto que o vocabulário não tem.
- leitor:b: não tipável (nao_e_limiar): O valor permite derrogar a aplicação da diretiva a certos lotes; não é um limite até ao qual um procedimento pode ser escolhido.

## regra:eu-2004-18:auto-prazo-maximo-art33-4-v20040430@v1

- leitor:a16: não tipável (sem_vocabulario): A regra é de um sistema de aquisição dinâmico, instrumento que o vocabulário não tem.
- leitor:b: não tipável (nao_e_prazo_maximo): O prazo é para a própria entidade adjudicante concluir a avaliação, não para apresentar elementos.

## regra:eu-2004-18:auto-prazo-minimo-art33-5-v20040430@v1

- leitor:a16: não tipável (sem_vocabulario): A regra é de um sistema de aquisição dinâmico, instrumento que o vocabulário não tem.
- leitor:b: não tipável (sem_vocabulario): O vocabulário não permite limitar a regra aos sistemas de aquisição dinâmicos.

## regra:eu-2004-18:auto-limiar-art35-1-a-v20040430@v1

- leitor:a16: não tipável (sem_vocabulario): A regra só vale para os acordos-quadro de fornecimentos por grupos de produtos, instrumento que o vocabulário não tem.
- leitor:b: não tipável (nao_e_limiar): O valor agrega vários contratos ou acordos-quadro para efeitos de pré-informação; não limita a escolha de um procedimento.

## regra:eu-2004-18:auto-limiar-art35-1-b-v20040430@v1

- leitor:a16: não tipável (texto_em_falta): Os valores dos limites para cada categoria de serviços estão no anexo II A, que não é mostrado.
- leitor:b: não tipável (nao_e_limiar): O valor agrega vários contratos para efeitos de anúncio de pré-informação; não limita a escolha de um procedimento.

## regra:eu-2004-18:auto-prazo-maximo-art35-4-v20040430@v1

- leitor:a16: não tipável (nao_e_prazo_maximo): O prazo é da própria entidade adjudicante para enviar o anúncio dos resultados, não um prazo máximo para os interessados apresentarem algo.
- leitor:b: não tipável (nao_e_prazo_maximo): Os prazos fixados destinam-se ao envio de anúncios pelas próprias entidades adjudicantes.

## regra:eu-2004-18:auto-prazo-maximo-art36-3-v20040430@v1

- leitor:a16: não tipável (sem_vocabulario): O prazo é fixado em dias, mas o instrumento em que se aplica é o procedimento por negociação com publicação de anúncio, que o vocabulário não tem.
- leitor:b: não tipável (nao_e_prazo_maximo): Os prazos respeitam à publicação dos anúncios, não à apresentação de elementos.

## regra:eu-2004-18:auto-prazo-minimo-art38-2-v20040430@v1

- leitor:a16: {"tipo": "prazo_minimo", "condicoes": [{"field": "tipo_procedimento", "op": "eq", "value": "concurso_publico"}], "params": {"minimum_days": 52, "deadline_field": "prazo_propostas_dias", "counted_from": "data_envio_anuncio", "usual_days": null}}
- leitor:b: {"tipo": "prazo_minimo", "condicoes": [{"field": "tipo_procedimento", "op": "eq", "value": "concurso_publico"}], "params": {"minimum_days": 52, "deadline_field": "prazo_propostas_dias", "counted_from": "data_envio_anuncio", "usual_days": null}}

## regra:eu-2004-18:auto-prazo-minimo-art38-3-a-v20040430@v1

- leitor:a16: {"tipo": "prazo_minimo", "condicoes": [{"field": "tipo_procedimento", "op": "eq", "value": "concurso_publico"}], "params": {"minimum_days": 37, "deadline_field": "prazo_reclamacao_dias", "counted_from": "data_envio_anuncio", "usual_days": null}}
- leitor:b: {"tipo": "prazo_minimo", "condicoes": [{"field": "tipo_procedimento", "op": "in", "value": ["concurso_limitado_previa_qualificacao", "dialogo_concorrencial", "procedimento_negociacao_com_concurso"]}], "params": {"minimum_days": 37, "deadline_field": "prazo_candidaturas_dias", "counted_from": "data_envio_anuncio", "usual_days": null}}
- verificador (A): regra 1, tipo_procedimento eq concurso_publico: as fontes não nomeiam ['concurso_publico']; regra 1: deadline_field prazo_reclamacao_dias e as fontes dizem ['prazo_candidaturas_dias'] (L9)

## regra:eu-2004-18:auto-prazo-minimo-art38-3-b-v20040430@v1

- leitor:a16: {"tipo": "prazo_minimo", "condicoes": [{"field": "tipo_procedimento", "op": "eq", "value": "concurso_limitado_previa_qualificacao"}], "params": {"minimum_days": 40, "deadline_field": "prazo_propostas_dias", "counted_from": "data_envio_convite", "usual_days": null}}
- leitor:b: {"tipo": "prazo_minimo", "condicoes": [{"field": "tipo_procedimento", "op": "eq", "value": "concurso_limitado_previa_qualificacao"}], "params": {"minimum_days": 40, "deadline_field": "prazo_propostas_dias", "counted_from": "data_envio_convite", "usual_days": null}}

## regra:eu-2004-18:auto-prazo-minimo-art38-4-v20040430@v1

- leitor:a16: {"tipo": "prazo_minimo", "condicoes": [{"field": "anuncio_pre_informacao", "op": "eq", "value": true}, {"field": "tipo_procedimento", "op": "eq", "value": "concurso_publico"}], "params": {"minimum_days": 22, "deadline_field": "prazo_propostas_dias", "counted_from": "data_envio_anuncio", "usual_days": 36}} || {"tipo": "prazo_minimo", "condicoes": [{"field": "anuncio_pre_informacao", "op": "eq", "value": true}, {"field": "tipo_procedimento", "op": "in", "value": ["concurso_publico", "dialogo_concorrencial", "procedimento_concorrencial_negociacao"]}], "params": {"minimum_days": 22, "deadline_field": "prazo_propostas_dias", "counted_from": "data_envio_anuncio", "usual_days": 36}}
- leitor:b: não tipável (sem_vocabulario): O vocabulário não permite representar as condições relativas ao conteúdo do anúncio de pré-informação e ao intervalo entre o seu envio e o envio do anúncio de concurso.
- verificador (A): regra 1: usual_days sem «em regra» e os dias nas fontes (L11); regra 2, tipo_procedimento in ['concurso_publico', 'dialogo_concorrencial', 'procedimento_concorrencial_negociacao']: as fontes não nomeiam ['procedimento_concorrencial_negociacao']; regra 2: usual_days sem «em regra» e os dias nas fontes (L11)

## regra:eu-2004-18:auto-prazo-maximo-art38-5-v20040430@v1

- leitor:a16: {"tipo": "prazo_maximo", "condicoes": [{"field": "publicado_joue", "op": "eq", "value": true}, {"field": "tipo_procedimento", "op": "eq", "value": "concurso_publico"}], "params": {"maximum_days": 29, "deadline_field": "prazo_propostas_dias", "counted_from": "data_envio_anuncio"}}
- leitor:b: não tipável (nao_e_prazo_maximo): A passagem reduz prazos mínimos de recepção de propostas e de pedidos de participação; não fixa um prazo máximo.
- verificador (A): regra 1, publicado_joue eq True: as fontes não afirmam o facto (L7); regra 1: maximum_days 29 não está nas fontes (L8, L4)

## regra:eu-2004-18:auto-prazo-maximo-art38-6-v20040430@v1

- leitor:a16: não tipável (nao_e_prazo_minimo): A redução é de cinco dias, não um prazo máximo.
- leitor:b: não tipável (nao_e_prazo_maximo): A passagem reduz prazos mínimos de recepção das propostas e não fixa um prazo máximo.

## regra:eu-2004-18:auto-prazo-minimo-art38-8-a-v20040430@v1

- leitor:a16: {"tipo": "prazo_minimo", "condicoes": [{"field": "tipo_procedimento", "op": "in", "value": ["concurso_limitado_previa_qualificacao", "procedimento_negociacao_com_concurso"]}], "params": {"minimum_days": 15, "deadline_field": "prazo_reclamacao_dias", "counted_from": "data_envio_anuncio", "usual_days": null}}
- leitor:b: não tipável (sem_vocabulario): O vocabulário não permite representar o envio electrónico do anúncio nas condições indicadas, necessário para distinguir os mínimos de quinze e dez dias.
- verificador (A): regra 1: deadline_field prazo_reclamacao_dias e as fontes dizem ['prazo_candidaturas_dias'] (L9)

## regra:eu-2004-18:auto-prazo-minimo-art38-8-b-v20040430@v1

- leitor:a16: {"tipo": "prazo_minimo", "condicoes": [{"field": "tipo_procedimento", "op": "in", "value": ["procedimento_concorrencial_negociacao", "procedimento_negociacao"]}], "params": {"minimum_days": 10, "deadline_field": "prazo_reclamacao_dias", "counted_from": "data_envio_convite", "usual_days": null}}
- leitor:b: não tipável (sem_vocabulario): Falta um campo que represente a urgência tornar impraticáveis os prazos mínimos, condição distinta de urgencia_fundamentada.
- verificador (A): regra 1, tipo_procedimento in ['procedimento_negociacao', 'procedimento_concorrencial_negociacao']: as fontes não nomeiam ['procedimento_concorrencial_negociacao', 'procedimento_negociacao']; regra 1: deadline_field prazo_reclamacao_dias e as fontes dizem ['prazo_propostas_dias'] (L9)

## regra:eu-2004-18:auto-prazo-maximo-art39-1-v20040430@v1

- leitor:a16: não tipável (nao_e_prazo_minimo): O prazo é da própria entidade adjudicante para enviar os documentos, não um prazo mínimo para os operadores económicos apresentarem algo.
- leitor:b: não tipável (nao_e_prazo_maximo): O prazo destina-se ao envio de documentos pela entidade adjudicante, não à apresentação de elementos pelos operadores económicos.

## regra:eu-2004-18:auto-prazo-maximo-art39-2-v20040430@v1

- leitor:a16: não tipável (nao_e_prazo_minimo): O prazo é um máximo para a comunicação das informações complementares, não um mínimo para apresentar algo.
- leitor:b: não tipável (nao_e_prazo_maximo): O prazo é para a comunicação de informações complementares pelas entidades adjudicantes ou pelos serviços competentes.

## regra:eu-2004-18:auto-prazo-maximo-art40-4-v20040430@v1

- leitor:a16: não tipável (sem_vocabulario): A regra é dos serviços competentes, não de uma entidade adjudicante.
- leitor:b: não tipável (nao_e_prazo_maximo): O prazo é para a comunicação de informações pelas entidades adjudicantes ou pelos serviços competentes, não para apresentar elementos pelos interessados.

## regra:eu-2004-18:auto-prazo-maximo-art41-2-v20040430@v1

- leitor:a16: não tipável (sem_vocabulario): A regra é de um sistema de aquisição dinâmico, instrumento que o vocabulário não tem.
- leitor:b: não tipável (nao_e_prazo_maximo): O prazo é para a própria entidade adjudicante prestar informações.

## regra:eu-2004-18:auto-prazo-maximo-art54-4-v20040430@v1

- leitor:a16: não tipável (sem_vocabulario): O prazo vale só para o leilão eletrónico, instrumento que o vocabulário não tem.
- leitor:b: não tipável (nao_e_prazo_maximo): A passagem fixa um intervalo mínimo para o início do leilão electrónico, não um prazo máximo para apresentar algo.

## regra:eu-2004-18:auto-limiar-art56-v20160101@v1

- leitor:a16: não tipável (texto_em_falta): O valor está no artigo 9.º, que não é mostrado.
- leitor:b: não tipável (nao_e_limiar): O valor delimita o âmbito de aplicação do capítulo, sem fixar um limite até ao qual um procedimento pode ser escolhido.

## regra:eu-2004-18:auto-prazo-minimo-art59-v20040430@v1

- leitor:a16: {"tipo": "prazo_minimo", "condicoes": [{"field": "tipo_contrato", "op": "eq", "value": "concessao_obras"}], "params": {"minimum_days": 52, "deadline_field": "prazo_candidaturas_dias", "counted_from": "data_envio_anuncio", "usual_days": null}}
- leitor:b: não tipável (sem_vocabulario): Falta no vocabulário a condição de os anúncios serem preparados e enviados por meios electrónicos, da qual depende a redução do prazo.

## regra:eu-2004-18:auto-limiar-art63-1-v20160101@v1

- leitor:a16: não tipável (sem_vocabulario): A regra só vale para os contratos de empreitada de obras celebrados por concessionários que não sejam entidades adjudicantes, instrumento que o vocabulário não tem.
- leitor:b: não tipável (nao_e_limiar): O valor determina a aplicação de regras de publicidade, não o limite até ao qual um procedimento pode ser escolhido.

## regra:eu-2004-18:auto-prazo-minimo-art65-v20040430@v1

- leitor:a16: {"tipo": "prazo_minimo", "condicoes": [{"field": "tipo_contrato", "op": "eq", "value": "obras"}, {"field": "tipo_procedimento", "op": "in", "value": ["concurso_limitado_previa_qualificacao", "concurso_publico", "dialogo_concorrencial", "procedimento_concorrencial_negociacao"]}], "params": {"minimum_days": 40, "deadline_field": "prazo_propostas_dias", "counted_from": "data_envio_anuncio", "usual_days": null}} || {"tipo": "prazo_minimo", "condicoes": [{"field": "tipo_contrato", "op": "eq", "value": "obras"}, {"field": "tipo_procedimento", "op": "in", "value": ["concurso_limitado_previa_qualificacao", "concurso_publico", "dialogo_concorrencial", "procedimento_concorrencial_negociacao"]}], "params": {"minimum_days": 37, "deadline_field": "prazo_propostas_dias", "counted_from": "data_envio_anuncio", "usual_days": null}}
- leitor:b: não tipável (sem_vocabulario): O vocabulário não permite representar a qualidade de concessionário que não seja entidade adjudicante nem as condições de envio eletrónico dos anúncios e de acesso eletrónico à documentação que permitem reduzir os prazos.
- verificador (A): regra 1, tipo_procedimento in ['concurso_publico', 'concurso_limitado_previa_qualificacao', 'dialogo_concorrencial', 'procedimento_concorrencial_negociacao']: as fontes não nomeiam ['procedimento_concorrencial_negociacao']; regra 2, tipo_procedimento in ['concurso_publico', 'concurso_limitado_previa_qualificacao', 'dialogo_concorrencial', 'procedimento_concorrencial_negociacao']: as fontes não nomeiam ['procedimento_concorrencial_negociacao']

## regra:eu-2004-18:auto-limiar-art67-1-a-v20160101@v1

- leitor:a16: {"tipo": "limiar", "condicoes": [{"field": "publicado_joue", "op": "eq", "value": false}, {"field": "tipo_contrato", "op": "eq", "value": "servicos"}, {"field": "tipo_entidade", "op": "eq", "value": "estado"}, {"field": "tipo_procedimento", "op": "eq", "value": "concurso_concecao"}], "params": {"threshold": {"field": "valor_estimado", "comparator": "ge", "value": 135000, "currency": "EUR"}}}
- leitor:b: não tipável (nao_e_limiar): O valor determina a aplicação do título, não um limite até ao qual um procedimento pode ser escolhido.
- verificador (A): regra 1, tipo_contrato eq servicos: as fontes não nomeiam ['servicos']; regra 1, tipo_procedimento eq concurso_concecao: as fontes não nomeiam ['concurso_concecao']; regra 1, publicado_joue eq False: as fontes não negam o facto (L7); regra 1, tipo_entidade eq estado: as fontes não nomeiam ['estado']; regra 1: value 135000 não está nas fontes (L10)

## regra:eu-2004-18:auto-limiar-art67-1-b-v20160101@v1

- leitor:a16: {"tipo": "limiar", "condicoes": [{"field": "tipo_contrato", "op": "eq", "value": "servicos"}, {"field": "tipo_procedimento", "op": "eq", "value": "concurso_concecao"}], "params": {"threshold": {"field": "valor_estimado", "comparator": "ge", "value": 209000, "currency": "EUR"}}}
- leitor:b: não tipável (nao_e_limiar): O valor determina a aplicação do título, não um limite até ao qual um procedimento pode ser escolhido.
- verificador (A): regra 1, tipo_contrato eq servicos: as fontes não nomeiam ['servicos']; regra 1, tipo_procedimento eq concurso_concecao: as fontes não nomeiam ['concurso_concecao']; regra 1: value 209000 não está nas fontes (L10)

## regra:eu-2004-18:auto-limiar-art67-1-c-v20160101@v1

- leitor:a16: não tipável (sem_vocabulario): A regra só vale para os serviços da categoria 8 do anexo II A e os serviços de telecomunicações da categoria 5 cujas posições no CPV sejam equivalentes aos números de referência CPC 7524, 7525 e 7526, factos que o vocabulário não tem.
- leitor:b: não tipável (nao_e_limiar): O valor determina a aplicação das regras do título, não o limite até ao qual um procedimento pode ser escolhido.

## regra:eu-2004-18:auto-limiar-art78-1-v20090807@v1

- leitor:a16: não tipável (texto_em_falta): Os anos de revisão estão no n.º 1 do artigo 7.º, que não está mostrado.
- leitor:b: não tipável (nao_e_limiar): A passagem regula a verificação e revisão dos limiares, sem fixar um valor até ao qual um procedimento pode ser escolhido.

## regra:eu-2004-18:auto-limiar-art78-3-v20040430@v1

- leitor:a16: não tipável (texto_em_falta): Os anos de revisão estão no n.º 1 do artigo 7.º, que não é mostrado.
- leitor:b: não tipável (nao_e_limiar): A passagem regula a revisão e o cálculo do contravalor dos limiares, sem fixar um limite de valor para a escolha de um procedimento.

## regra:eu-2009-81:auto-limiar-art8-a@v1

- leitor:a16: {"tipo": "limiar", "condicoes": [{"field": "tipo_contrato", "op": "eq", "value": "bens"}, {"field": "tipo_procedimento", "op": "in", "value": ["concurso_aberto", "concurso_publico", "concurso_publico_urgente", "procedimento_concorrencial_negociacao", "procedimento_negociacao_com_concurso"]}], "params": {"threshold": {"field": "valor_estimado", "comparator": "ge", "value": 432000, "currency": "EUR"}}}
- leitor:b: não tipável (nao_e_limiar): O valor delimita a aplicação da diretiva, não o limite até ao qual um procedimento pode ser escolhido.
- verificador (A): regra 1, tipo_contrato eq bens: as fontes não nomeiam ['bens']; regra 1, tipo_procedimento in ['concurso_aberto', 'concurso_publico', 'concurso_publico_urgente', 'procedimento_concorrencial_negociacao', 'procedimento_negociacao_com_concurso']: as fontes não nomeiam ['concurso_aberto', 'concurso_publico', 'concurso_publico_urgente', 'procedimento_concorrencial_negociacao', 'procedimento_negociacao_com_concurso']; regra 1: value 432000 não está nas fontes (L10)

## regra:eu-2009-81:auto-limiar-art8-b@v1

- leitor:a16: não tipável (sem_vocabulario): O valor é o limite até ao qual um contrato de empreitada pode ser escolhido, e o instrumento é uma central de compras, que o vocabulário não tem.
- leitor:b: não tipável (nao_e_limiar): O valor delimita a aplicação da diretiva, não o limite até ao qual um procedimento pode ser escolhido.

## regra:eu-2009-81:auto-limiar-art9-4-a@v1

- leitor:a16: não tipável (sem_vocabulario): A regra só vale para a adjudicação simultânea de contratos por lotes separados, facto que nenhum campo do vocabulário tem.
- leitor:b: não tipável (nao_e_limiar): A passagem agrega o valor dos lotes e permite uma derrogação da aplicação da diretiva, sem fixar um limite de valor para a escolha de um procedimento.

## regra:eu-2009-81:auto-limiar-art9-4-b@v1

- leitor:a16: {"tipo": "limiar", "condicoes": [{"field": "tipo_contrato", "op": "eq", "value": "bens"}, {"field": "tipo_procedimento", "op": "in", "value": ["concurso_aberto", "concurso_limitado_previa_qualificacao", "concurso_publico", "procedimento_concorrencial_negociacao", "procedimento_negociacao_com_concurso"]}], "params": {"threshold": {"field": "valor_estimado", "comparator": "ge", "value": 80000, "currency": "EUR"}}}
- leitor:b: não tipável (nao_e_limiar): O valor permite dispensar a aplicação da directiva a determinados lotes; não limita a escolha de um procedimento.
- verificador (A): regra 1, tipo_contrato eq bens: as fontes não nomeiam ['bens']; regra 1, tipo_procedimento in ['concurso_publico', 'concurso_aberto', 'concurso_limitado_previa_qualificacao', 'procedimento_concorrencial_negociacao', 'procedimento_negociacao_com_concurso']: as fontes não nomeiam ['concurso_aberto', 'concurso_limitado_previa_qualificacao', 'concurso_publico', 'procedimento_concorrencial_negociacao', 'procedimento_negociacao_com_concurso']; regra 1: value 80000 não está nas fontes (L10)

## regra:eu-2009-81:auto-limiar-art9-5-b-v20100101@v1

- leitor:a16: não tipável (sem_vocabulario): A regra depende do valor cumulado de vários lotes, facto que o vocabulário não tem.
- leitor:b: não tipável (nao_e_limiar): O valor permite derrogar a aplicação da diretiva a determinados lotes; não fixa um limite para a escolha de um procedimento.

## regra:eu-2009-81:auto-prazo-maximo-art30-3@v1

- leitor:a16: não tipável (nao_e_prazo_maximo): O prazo é da própria entidade adjudicante para enviar o anúncio dos resultados, não um prazo máximo para os interessados apresentarem algo.
- leitor:b: não tipável (nao_e_prazo_maximo): O prazo é para a própria entidade adjudicante enviar um anúncio com os resultados do processo.

## regra:eu-2009-81:auto-prazo-maximo-art32-3@v1

- leitor:a16: não tipável (sem_vocabulario): O prazo é fixado em dias, mas o vocabulário só tem prazos em dias úteis.
- leitor:b: não tipável (nao_e_prazo_maximo): Os prazos destinam-se à publicação de anúncios, não à apresentação de elementos pelos interessados.

## regra:eu-2009-81:auto-prazo-minimo-art33-2@v1

- leitor:a16: {"tipo": "prazo_minimo", "condicoes": [{"field": "tipo_procedimento", "op": "in", "value": ["concurso_limitado_previa_qualificacao", "dialogo_concorrencial", "procedimento_concorrencial_negociacao"]}], "params": {"minimum_days": 37, "deadline_field": "prazo_propostas_dias", "counted_from": "data_envio_anuncio", "usual_days": null}}
- leitor:b: {"tipo": "prazo_minimo", "condicoes": [{"field": "tipo_procedimento", "op": "eq", "value": "concurso_limitado_previa_qualificacao"}], "params": {"minimum_days": 40, "deadline_field": "prazo_propostas_dias", "counted_from": "data_envio_convite", "usual_days": null}}
- verificador (A): regra 1, tipo_procedimento in ['concurso_limitado_previa_qualificacao', 'procedimento_concorrencial_negociacao', 'dialogo_concorrencial']: as fontes não nomeiam ['procedimento_concorrencial_negociacao']

## regra:eu-2009-81:auto-prazo-minimo-art33-3@v1

- leitor:a16: {"tipo": "prazo_minimo", "condicoes": [{"field": "anuncio_pre_informacao", "op": "eq", "value": true}, {"field": "publicado_joue", "op": "eq", "value": true}, {"field": "tipo_procedimento", "op": "in", "value": ["concurso_limitado_previa_qualificacao", "dialogo_concorrencial", "procedimento_concorrencial_negociacao"]}], "params": {"minimum_days": 22, "deadline_field": "prazo_propostas_dias", "counted_from": "data_envio_convite", "usual_days": null}}
- leitor:b: não tipável (sem_vocabulario): O vocabulário não permite representar as condições relativas ao conteúdo do anúncio de pré-informação e à antecedência do seu envio para publicação.
- verificador (A): regra 1, publicado_joue eq True: as fontes não afirmam o facto (L7); regra 1, tipo_procedimento in ['concurso_limitado_previa_qualificacao', 'dialogo_concorrencial', 'procedimento_concorrencial_negociacao']: as fontes não nomeiam ['procedimento_concorrencial_negociacao']; regra 1: minimum_days 22 não está nas fontes (L8, L4)

## regra:eu-2009-81:auto-prazo-maximo-art33-4@v1

- leitor:a16: não tipável (texto_em_falta): Os dias de que se parte e a data do envio do anúncio estão no primeiro parágrafo do n.º 2, que não é mostrado.
- leitor:b: não tipável (nao_e_prazo_maximo): A passagem reduz um prazo mínimo, não fixa um prazo máximo.

## regra:eu-2009-81:auto-prazo-maximo-art33-5@v1

- leitor:a16: não tipável (nao_e_prazo_minimo): O prazo reduzido é um máximo de cinco dias, não um mínimo.
- leitor:b: não tipável (nao_e_prazo_maximo): A passagem reduz um prazo mínimo de recepção das propostas e não fixa um prazo máximo.

## regra:eu-2009-81:auto-prazo-minimo-art33-7@v1

- leitor:a16: {"tipo": "prazo_minimo", "condicoes": [{"field": "publicado_joue", "op": "eq", "value": true}, {"field": "tipo_procedimento", "op": "in", "value": ["concurso_limitado_previa_qualificacao", "procedimento_concorrencial_negociacao"]}, {"field": "urgencia_fundamentada", "op": "eq", "value": true}], "params": {"minimum_days": 10, "deadline_field": "prazo_propostas_dias", "counted_from": "data_envio_convite", "usual_days": null}}
- leitor:b: não tipável (sem_vocabulario): Falta um campo para representar o envio do anúncio por meios electrónicos, condição que distingue os mínimos de 15 e 10 dias para os pedidos de participação.
- verificador (A): regra 1, publicado_joue eq True: as fontes não afirmam o facto (L7); regra 1, tipo_procedimento in ['concurso_limitado_previa_qualificacao', 'procedimento_concorrencial_negociacao']: as fontes não nomeiam ['procedimento_concorrencial_negociacao']; regra 1: counted_from data_envio_convite e as fontes dizem nada (L9)

## regra:eu-2009-81:auto-prazo-maximo-art34-4@v1

- leitor:a16: {"tipo": "prazo_maximo", "condicoes": [{"field": "tipo_procedimento", "op": "in", "value": ["concurso_limitado_previa_qualificacao", "procedimento_concorrencial_negociacao", "procedimento_negociacao_com_concurso"]}], "params": {"maximum_days": 4, "deadline_field": "prazo_propostas_dias", "counted_from": "nao_indicado"}} || {"tipo": "prazo_maximo", "condicoes": [{"field": "tipo_procedimento", "op": "in", "value": ["concurso_limitado_previa_qualificacao", "procedimento_concorrencial_negociacao", "procedimento_negociacao_com_concurso"]}], "params": {"maximum_days": 6, "deadline_field": "prazo_propostas_dias", "counted_from": "nao_indicado"}}
- leitor:b: não tipável (nao_e_prazo_maximo): O prazo é para as autoridades/entidades adjudicantes ou os serviços competentes comunicarem informações complementares.
- verificador (A): regra 1, tipo_procedimento in ['concurso_limitado_previa_qualificacao', 'procedimento_concorrencial_negociacao', 'procedimento_negociacao_com_concurso']: as fontes não nomeiam ['procedimento_concorrencial_negociacao', 'procedimento_negociacao_com_concurso']; regra 1: as fontes de maximum_days não dizem um máximo («não pode ser superior a», «no prazo de», L8); regra 2, tipo_procedimento in ['concurso_limitado_previa_qualificacao', 'procedimento_concorrencial_negociacao', 'procedimento_negociacao_com_concurso']: as fontes não nomeiam ['procedimento_concorrencial_negociacao', 'procedimento_negociacao_com_concurso']; regra 2: as fontes de maximum_days não dizem um máximo («não pode ser superior a», «no prazo de», L8)

## regra:eu-2009-81:auto-prazo-maximo-art35-2@v1

- leitor:a16: não tipável (nao_e_prazo_maximo): O prazo é de quinze dias, máximo para a comunicação, não um prazo para apresentar algo.
- leitor:b: não tipável (nao_e_prazo_maximo): O prazo destina-se à própria autoridade/entidade adjudicante para comunicar informações.

## regra:eu-2009-81:auto-prazo-maximo-art48-4@v1

- leitor:a16: não tipável (nao_e_prazo_maximo): O prazo é o da avaliação prévia das propostas, não um prazo para apresentar algo.
- leitor:b: não tipável (nao_e_prazo_maximo): A passagem fixa um prazo mínimo para o início do leilão electrónico, não um prazo máximo para apresentar algo.

## regra:eu-2009-81:auto-prazo-minimo-art55-6@v1

- leitor:a16: não tipável (nao_e_prazo_minimo): O prazo é de suspensão da possibilidade de celebrar o contrato, não um prazo para apresentar algo.
- leitor:b: não tipável (nao_e_prazo_minimo): O prazo regula a duração da suspensão da possibilidade de celebrar o contrato, não um prazo para apresentar algo.

## regra:eu-2009-81:auto-prazo-minimo-art57-2@v1

- leitor:a16: não tipável (sem_vocabulario): A regra é de um procedimento de recurso, que o vocabulário não tem.
- leitor:b: não tipável (nao_e_prazo_minimo): O prazo suspensivo limita a celebração do contrato, não sendo um prazo para apresentar algo.

## regra:eu-2009-81:auto-prazo-minimo-art59@v1

- leitor:a16: não tipável (nao_e_prazo_minimo): O prazo é de interposição de recurso, não um prazo para apresentar algo.
- leitor:b: não tipável (sem_vocabulario): O vocabulário não prevê um campo de prazo para a interposição de recurso.
- verificador (B): não tipável: «Prazos para interposição de recurso» não está em eu-2009-81:art59

## regra:eu-2009-81:auto-prazo-minimo-art60-4@v1

- leitor:a16: não tipável (sem_vocabulario): A regra só vale para a autoridade adjudicante, que não é um campo do vocabulário.
- leitor:b: não tipável (nao_e_prazo_minimo): O prazo refere-se à celebração do contrato, não à apresentação de qualquer elemento.

## regra:eu-2009-81:auto-prazo-minimo-art60-5@v1

- leitor:a16: não tipável (sem_vocabulario): A regra só vale para os contratos celebrados por decisão de adjudicação enviada por telecópia ou por meios electrónicos, facto que nenhum campo do vocabulário tem.
- leitor:b: não tipável (nao_e_prazo_minimo): O prazo é de espera para a celebração do contrato, não para apresentar algo.

## regra:eu-2009-81:auto-prazo-minimo-art62-1-a@v1

- leitor:a16: não tipável (sem_vocabulario): A contagem do prazo é feita em dias consecutivos, unidade que o vocabulário não tem.
- leitor:b: não tipável (sem_vocabulario): O vocabulário não prevê um campo para a apresentação de pedidos de recurso nem prazos expressos em meses.

## regra:eu-2009-81:auto-prazo-maximo-art63-3@v1

- leitor:a16: não tipável (nao_e_prazo_minimo): O prazo é de 21 dias, um máximo para a própria autoridade/entidade adjudicante comunicar, não um prazo para os interessados apresentarem algo.
- leitor:b: não tipável (nao_e_prazo_maximo): O prazo destina-se à comunicação do Estado-Membro à Comissão, não à apresentação de elementos num procedimento de contratação.

## regra:eu-2014-23:auto-limiar-art8-1@v1

- leitor:a16: {"tipo": "limiar", "condicoes": [{"field": "tipo_contrato", "op": "eq", "value": "concessao_obras"}], "params": {"threshold": {"field": "valor_estimado", "comparator": "ge", "value": 5404000, "currency": "EUR"}}}
- leitor:b: não tipável (nao_e_limiar): O valor delimita o âmbito de aplicação da diretiva, não o limite até ao qual um procedimento pode ser escolhido.
- verificador (A): regra 1, tipo_contrato eq concessao_obras: as fontes não nomeiam ['concessao_obras']; regra 1: um limiar tem sempre o procedimento que permite abaixo do valor; sem ele, L12 (nao_e_limiar); regra 1: value 5404000 não está nas fontes (L10)

## regra:eu-2014-23:auto-limiar-art9-1@v1

- leitor:a16: não tipável (texto_em_falta): O valor do limiar está no Acordo sobre Contratos Públicos da Organização Mundial do Comércio, que não é mostrado.
- leitor:b: não tipável (nao_e_limiar): A passagem estabelece a revisão e o cálculo do limiar, sem fixar um valor até ao qual um procedimento pode ser escolhido.

## regra:eu-2014-23:auto-limiar-art9-2@v1

- leitor:a16: não tipável (texto_em_falta): Falta o valor do contravalor, que está no n.º 1 do artigo 8.º, n.º 1, e nas moedas nacionais dos Estados-Membros cuja moeda não seja o euro.
- leitor:b: não tipável (nao_e_limiar): A passagem regula a determinação do contravalor dos limiares, sem fixar um limite de valor para a escolha de um procedimento.

## regra:eu-2014-23:auto-prazo-maximo-art32-1@v1

- leitor:a16: não tipável (nao_e_prazo_minimo): O prazo é da própria entidade adjudicante para enviar o anúncio de adjudicação, não um prazo para os interessados apresentarem algo.
- leitor:b: não tipável (nao_e_prazo_maximo): Os prazos são para o envio de anúncios pelas próprias autoridades e entidades adjudicantes, não para apresentar elementos pelos participantes.

## regra:eu-2014-23:auto-prazo-maximo-art33-2@v1

- leitor:a16: não tipável (sem_vocabulario): A regra limita os anúncios de concessão a 5 dias, prazo que o vocabulário não tem.
- leitor:b: não tipável (nao_e_prazo_maximo): O prazo é para a publicação dos anúncios, não para apresentar algo.

## regra:eu-2014-23:auto-prazo-maximo-art34-3@v1

- leitor:a16: não tipável (nao_e_prazo_maximo): O prazo é de seis dias no máximo para a comunicação de informações adicionais, não um prazo para os candidatos apresentarem algo.
- leitor:b: não tipável (nao_e_prazo_maximo): O prazo é para as autoridades adjudicantes, entidades adjudicantes ou serviços competentes comunicarem informações adicionais, não para os candidatos ou proponentes apresentarem algo.

## regra:eu-2014-23:auto-prazo-minimo-art39-3@v1

- leitor:a16: {"tipo": "prazo_minimo", "condicoes": [{"field": "tipo_contrato", "op": "eq", "value": "concessao_obras"}], "params": {"minimum_days": 30, "deadline_field": "prazo_propostas_dias", "counted_from": "data_envio_anuncio", "usual_days": null}}
- leitor:b: {"tipo": "prazo_minimo", "condicoes": [], "params": {"minimum_days": 30, "deadline_field": "prazo_candidaturas_dias", "counted_from": "data_envio_anuncio", "usual_days": null}}
- verificador (A): regra 1, tipo_contrato eq concessao_obras: as fontes não nomeiam ['concessao_obras']; regra 1: deadline_field prazo_propostas_dias e as fontes dizem ['prazo_candidaturas_dias'] (L9)

## regra:eu-2014-23:auto-prazo-minimo-art39-4@v1

- leitor:a16: {"tipo": "prazo_minimo", "condicoes": [{"field": "tipo_contrato", "op": "eq", "value": "concessao_obras"}, {"field": "tipo_procedimento", "op": "eq", "value": "concurso_aberto"}], "params": {"minimum_days": 22, "deadline_field": "prazo_propostas_dias", "counted_from": "data_envio_convite", "usual_days": null}}
- leitor:b: não tipável (sem_vocabulario): O vocabulário não permite representar a condição de o procedimento se desenrolar em fases sucessivas.
- verificador (A): regra 1, tipo_contrato eq concessao_obras: as fontes não nomeiam ['concessao_obras']; regra 1, tipo_procedimento eq concurso_aberto: as fontes não nomeiam ['concurso_aberto']

## regra:eu-2014-23:auto-prazo-maximo-art39-5@v1

- leitor:a16: não tipável (texto_em_falta): Os dias de que se parte e a data a que se conta os 5 dias estão no artigo 29.º, que não é mostrado.
- leitor:b: não tipável (nao_e_prazo_maximo): A passagem prevê uma redução do prazo de receção das propostas, sem fixar um prazo máximo.

## regra:eu-2014-23:auto-prazo-maximo-art40-1@v1

- leitor:a16: não tipável (nao_e_prazo_minimo): O prazo é da própria entidade adjudicante para informar, não um prazo mínimo para os interessados apresentarem algo.
- leitor:b: não tipável (nao_e_prazo_maximo): O prazo é para a própria autoridade ou entidade adjudicante prestar informações, não para apresentar elementos.

## regra:eu-2014-24:auto-limiar-art4-a@v1

- leitor:a16: {"tipo": "limiar", "condicoes": [{"field": "tipo_contrato", "op": "eq", "value": "obras"}, {"field": "tipo_entidade", "op": "eq", "value": "estado"}, {"field": "tipo_procedimento", "op": "in", "value": ["concurso_aberto", "concurso_publico"]}], "params": {"threshold": {"field": "valor_estimado", "comparator": "ge", "value": 5404000, "currency": "EUR"}}}
- leitor:b: não tipável (nao_e_limiar): O montante delimita a aplicação da diretiva, sem fixar um valor até ao qual um procedimento pode ser escolhido.
- verificador (A): regra 1, tipo_entidade eq estado: as fontes não nomeiam ['estado']; regra 1, tipo_procedimento in ['concurso_publico', 'concurso_aberto']: as fontes não nomeiam ['concurso_aberto', 'concurso_publico']; regra 1: value 5404000 não está nas fontes (L10)

## regra:eu-2014-24:auto-limiar-art4-b@v1

- leitor:a16: {"tipo": "limiar", "condicoes": [{"field": "tipo_contrato", "op": "in", "value": ["bens", "servicos"]}, {"field": "tipo_entidade", "op": "eq", "value": "estado"}, {"field": "tipo_procedimento", "op": "in", "value": ["concurso_aberto", "concurso_concecao", "concurso_ideias", "concurso_limitado_previa_qualificacao", "concurso_publico", "dialogo_concorrencial", "procedimento_concorrencial_negociacao", "procedimento_negociacao", "procedimento_negociacao_com_concurso"]}], "params": {"threshold": {"field": "valor_estimado", "comparator": "ge", "value": 140000, "currency": "EUR"}}}
- leitor:b: não tipável (nao_e_limiar): O valor fixa o âmbito de aplicação da diretiva, não o limite até ao qual um procedimento pode ser escolhido.
- verificador (A): regra 1, tipo_contrato in ['bens', 'servicos']: as fontes não nomeiam ['bens']; regra 1, tipo_entidade eq estado: as fontes não nomeiam ['estado']; regra 1, tipo_procedimento in ['concurso_publico', 'concurso_aberto', 'concurso_ideias', 'concurso_concecao', 'concurso_limitado_previa_qualificacao', 'dialogo_concorrencial', 'procedimento_concorrencial_negociacao', 'procedimento_negociacao', 'procedimento_negociacao_com_concurso']: as fontes não nomeiam ['concurso_aberto', 'concurso_concecao', 'concurso_ideias', 'concurso_limitado_previa_qualificacao', 'concurso_publico', 'dialogo_concorrencial', 'procedimento_concorrencial_negociacao', 'procedimento_negociacao', 'procedimento_negociacao_com_concurso']; regra 1: field valor_estimado e as fontes nomeiam nada (L10); regra 1: value 140000 não está nas fontes (L10)

## regra:eu-2014-24:auto-limiar-art4-c@v1

- leitor:a16: {"tipo": "limiar", "condicoes": [{"field": "tipo_contrato", "op": "in", "value": ["bens", "servicos_sociais"]}, {"field": "tipo_entidade", "op": "eq", "value": "outra"}, {"field": "tipo_procedimento", "op": "in", "value": ["concurso_aberto", "concurso_ideias", "concurso_publico", "concurso_publico_urgente", "dialogo_concorrencial", "procedimento_concorrencial_negociacao", "procedimento_negociacao_com_concurso"]}], "params": {"threshold": {"field": "valor_estimado", "comparator": "ge", "value": 216000, "currency": "EUR"}}}
- leitor:b: não tipável (nao_e_limiar): O valor delimita o âmbito de aplicação da diretiva, não o limite até ao qual um procedimento pode ser escolhido.
- verificador (A): regra 1, tipo_contrato in ['bens', 'servicos_sociais']: as fontes não nomeiam ['bens', 'servicos_sociais']; regra 1, tipo_entidade eq outra: as fontes não nomeiam ['outra']; regra 1, tipo_procedimento in ['concurso_aberto', 'concurso_ideias', 'concurso_publico', 'concurso_publico_urgente', 'dialogo_concorrencial', 'procedimento_concorrencial_negociacao', 'procedimento_negociacao_com_concurso']: as fontes não nomeiam ['concurso_aberto', 'concurso_ideias', 'concurso_publico', 'concurso_publico_urgente', 'dialogo_concorrencial', 'procedimento_concorrencial_negociacao', 'procedimento_negociacao_com_concurso']; regra 1: value 216000 não está nas fontes (L10)

## regra:eu-2014-24:auto-limiar-art4-d@v1

- leitor:a16: {"tipo": "limiar", "condicoes": [{"field": "tipo_contrato", "op": "eq", "value": "servicos_sociais"}, {"field": "tipo_entidade", "op": "eq", "value": "estado"}, {"field": "tipo_procedimento", "op": "in", "value": ["concurso_aberto", "concurso_concecao", "concurso_publico", "concurso_publico_urgente", "dialogo_concorrencial", "parceria_inovacao"]}], "params": {"threshold": {"field": "valor_estimado", "comparator": "ge", "value": 750000, "currency": "EUR"}}}
- leitor:b: não tipável (nao_e_limiar): O valor delimita o âmbito de aplicação da diretiva, não o limite até ao qual um procedimento pode ser escolhido.
- verificador (A): regra 1, tipo_entidade eq estado: as fontes não nomeiam ['estado']; regra 1, tipo_procedimento in ['concurso_aberto', 'concurso_publico', 'concurso_publico_urgente', 'concurso_concecao', 'dialogo_concorrencial', 'parceria_inovacao']: as fontes não nomeiam ['concurso_aberto', 'concurso_concecao', 'concurso_publico', 'concurso_publico_urgente', 'dialogo_concorrencial', 'parceria_inovacao']; regra 1: value 750000 não está nas fontes (L10)

## regra:eu-2014-24:auto-limiar-art5-10@v1

- leitor:a16: não tipável (sem_vocabulario): A regra só vale para contratos divididos em lotes, facto que nenhum campo do vocabulário tem.
- leitor:b: não tipável (nao_e_limiar): A passagem prevê uma dispensa de aplicação dos procedimentos da diretiva a certos lotes, sem fixar um limite de valor para a escolha de um procedimento.

## regra:eu-2014-24:auto-limiar-art6-1@v1

- leitor:a16: não tipável (texto_em_falta): Os valores dos limiares estão no Acordo sobre Contratos Públicos da Organização Mundial do Comércio, que não é mostrado.
- leitor:b: não tipável (nao_e_limiar): A passagem regula o cálculo e a revisão dos limiares, sem fixar um limite de valor até ao qual um procedimento pode ser escolhido.

## regra:eu-2014-24:auto-limiar-art6-3@v1

- leitor:a16: não tipável (texto_em_falta): Os valores dos limiares revistos estão no artigo 4.º, alíneas a), b) e c), que não é mostrado.
- leitor:b: não tipável (nao_e_limiar): A passagem regula a determinação do contravalor dos limiares, sem fixar um limite de valor para a escolha de um procedimento.

## regra:eu-2014-24:auto-limiar-art13-a@v1

- leitor:a16: {"tipo": "limiar", "condicoes": [{"field": "tipo_contrato", "op": "eq", "value": "obras"}, {"field": "tipo_procedimento", "op": "eq", "value": "concurso_publico"}], "params": {"threshold": {"field": "valor_estimado", "comparator": "ge", "value": 5404000, "currency": "EUR"}}}
- leitor:b: não tipável (nao_e_limiar): O valor delimita a aplicação da diretiva, sem fixar um limite até ao qual um procedimento pode ser escolhido.
- verificador (A): regra 1, tipo_procedimento eq concurso_publico: as fontes não nomeiam ['concurso_publico']; regra 1: value 5404000 não está nas fontes (L10)

## regra:eu-2014-24:auto-limiar-art13-b@v1

- leitor:a16: não tipável (nao_e_limiar): o valor não é o limite até ao qual um procedimento pode ser escolhido
- leitor:b: não tipável (nao_e_limiar): A passagem delimita a aplicação e exige o cumprimento da diretiva, sem fixar um limite de valor até ao qual um procedimento pode ser escolhido.

## regra:eu-2014-24:auto-prazo-minimo-art27-1@v1

- leitor:a16: {"tipo": "prazo_minimo", "condicoes": [{"field": "tipo_procedimento", "op": "eq", "value": "concurso_aberto"}], "params": {"minimum_days": 35, "deadline_field": "prazo_propostas_dias", "counted_from": "data_envio_anuncio", "usual_days": null}}
- leitor:b: {"tipo": "prazo_minimo", "condicoes": [{"field": "tipo_procedimento", "op": "eq", "value": "concurso_aberto"}], "params": {"minimum_days": 35, "deadline_field": "prazo_propostas_dias", "counted_from": "data_envio_anuncio", "usual_days": null}}

## regra:eu-2014-24:auto-prazo-minimo-art27-2-b@v1

- leitor:a16: {"tipo": "prazo_minimo", "condicoes": [{"field": "anuncio_pre_informacao", "op": "eq", "value": false}, {"field": "publicado_joue", "op": "eq", "value": false}, {"field": "tipo_procedimento", "op": "eq", "value": "concurso_aberto"}, {"field": "urgencia_fundamentada", "op": "eq", "value": false}], "params": {"minimum_days": 15, "deadline_field": "prazo_propostas_dias", "counted_from": "data_envio_anuncio", "usual_days": null}}
- leitor:b: não tipável (nao_e_prazo_minimo): A passagem fixa a antecedência do envio de um anúncio pela entidade adjudicante, não um prazo para apresentar propostas.
- verificador (A): regra 1, anuncio_pre_informacao eq False: as fontes não negam o facto (L7); regra 1, publicado_joue eq False: as fontes não negam o facto (L7); regra 1, urgencia_fundamentada eq False: as fontes não negam o facto (L7)

## regra:eu-2014-24:auto-prazo-minimo-art27-3@v1

- leitor:a16: {"tipo": "prazo_minimo", "condicoes": [{"field": "publicado_joue", "op": "eq", "value": true}, {"field": "tipo_procedimento", "op": "eq", "value": "concurso_aberto"}, {"field": "urgencia_fundamentada", "op": "eq", "value": true}], "params": {"minimum_days": 15, "deadline_field": "prazo_propostas_dias", "counted_from": "data_envio_anuncio", "usual_days": null}}
- leitor:b: não tipável (sem_vocabulario): O vocabulário não permite representar a condição de a urgência inviabilizar o cumprimento do prazo fixado no n.º 1.
- verificador (A): regra 1, publicado_joue eq True: as fontes não afirmam o facto (L7)

## regra:eu-2014-24:auto-prazo-maximo-art27-4@v1

- leitor:a16: não tipável (nao_e_prazo_minimo): O prazo é reduzido em cinco dias; não é um prazo mínimo nem máximo.
- leitor:b: não tipável (nao_e_prazo_maximo): A passagem reduz um prazo mínimo, não fixa um prazo máximo.

## regra:eu-2014-24:auto-prazo-minimo-art28-1@v1

- leitor:a16: {"tipo": "prazo_minimo", "condicoes": [{"field": "tipo_procedimento", "op": "eq", "value": "concurso_limitado_previa_qualificacao"}], "params": {"minimum_days": 30, "deadline_field": "prazo_reclamacao_dias", "counted_from": "data_envio_anuncio", "usual_days": null}}
- leitor:b: não tipável (sem_vocabulario): O vocabulário não permite distinguir se o anúncio de pré-informação é utilizado como meio de abertura de concurso, facto que determina o início da contagem do prazo.
- verificador (A): regra 1: deadline_field prazo_reclamacao_dias e as fontes dizem ['prazo_candidaturas_dias'] (L9)

## regra:eu-2014-24:auto-prazo-minimo-art28-2@v1

- leitor:a16: {"tipo": "prazo_minimo", "condicoes": [{"field": "tipo_procedimento", "op": "eq", "value": "concurso_limitado_previa_qualificacao"}], "params": {"minimum_days": 30, "deadline_field": "prazo_propostas_dias", "counted_from": "data_envio_convite", "usual_days": null}}
- leitor:b: {"tipo": "prazo_minimo", "condicoes": [{"field": "tipo_procedimento", "op": "eq", "value": "concurso_limitado_previa_qualificacao"}], "params": {"minimum_days": 30, "deadline_field": "prazo_propostas_dias", "counted_from": "data_envio_convite", "usual_days": null}}
- verificador (A): regra 1, tipo_procedimento eq concurso_limitado_previa_qualificacao: as fontes não nomeiam ['concurso_limitado_previa_qualificacao']; regra 1: counted_from data_envio_convite e as fontes dizem nada (L9)

## regra:eu-2014-24:auto-prazo-minimo-art28-3-b@v1

- leitor:a16: {"tipo": "prazo_minimo", "condicoes": [{"field": "anuncio_pre_informacao", "op": "eq", "value": false}, {"field": "publicado_joue", "op": "eq", "value": false}, {"field": "tipo_procedimento", "op": "eq", "value": "concurso_limitado_previa_qualificacao"}], "params": {"minimum_days": 10, "deadline_field": "prazo_propostas_dias", "counted_from": "data_envio_convite", "usual_days": null}}
- leitor:b: não tipável (sem_vocabulario): O vocabulário não permite representar o intervalo exigido entre o envio do anúncio de pré-informação e o envio do anúncio de concurso, condição da redução do prazo para 10 dias.
- verificador (A): regra 1, anuncio_pre_informacao eq False: as fontes não negam o facto (L7); regra 1, publicado_joue eq False: as fontes não negam o facto (L7); regra 1, tipo_procedimento eq concurso_limitado_previa_qualificacao: as fontes não nomeiam ['concurso_limitado_previa_qualificacao']; regra 1: counted_from data_envio_convite e as fontes dizem nada (L9)

## regra:eu-2014-24:auto-prazo-minimo-art28-4@v1

- leitor:a16: {"tipo": "prazo_minimo", "condicoes": [{"field": "tipo_procedimento", "op": "eq", "value": "concurso_limitado_previa_qualificacao"}], "params": {"minimum_days": 10, "deadline_field": "prazo_propostas_dias", "counted_from": "data_envio_convite", "usual_days": null}}
- leitor:b: não tipável (sem_vocabulario): Faltam condições no vocabulário para representar as autoridades adjudicantes subcentrais e a falta de acordo com os candidatos selecionados sobre o prazo.
- verificador (A): regra 1, tipo_procedimento eq concurso_limitado_previa_qualificacao: as fontes não nomeiam ['concurso_limitado_previa_qualificacao']; regra 1: counted_from data_envio_convite e as fontes dizem nada (L9)

## regra:eu-2014-24:auto-prazo-maximo-art28-5@v1

- leitor:a16: {"tipo": "prazo_maximo", "condicoes": [{"field": "tipo_procedimento", "op": "eq", "value": "concurso_limitado_previa_qualificacao"}], "params": {"maximum_days": 5, "deadline_field": "prazo_propostas_dias", "counted_from": "data_envio_convite"}}
- leitor:b: não tipável (nao_e_prazo_maximo): A passagem reduz um prazo mínimo, não fixa um prazo máximo.
- verificador (A): regra 1: as fontes de maximum_days não dizem um máximo («não pode ser superior a», «no prazo de», L8)

## regra:eu-2014-24:auto-prazo-minimo-art28-6-a@v1

- leitor:a16: {"tipo": "prazo_minimo", "condicoes": [{"field": "tipo_procedimento", "op": "eq", "value": "concurso_limitado_previa_qualificacao"}, {"field": "urgencia_fundamentada", "op": "eq", "value": true}], "params": {"minimum_days": 15, "deadline_field": "prazo_reclamacao_dias", "counted_from": "data_envio_anuncio", "usual_days": null}}
- leitor:b: não tipável (sem_vocabulario): Falta um campo para representar a condição de a urgência inviabilizar o cumprimento dos prazos fixados no artigo.
- verificador (A): regra 1, tipo_procedimento eq concurso_limitado_previa_qualificacao: as fontes não nomeiam ['concurso_limitado_previa_qualificacao']; regra 1: deadline_field prazo_reclamacao_dias e as fontes dizem ['prazo_candidaturas_dias'] (L9)

## regra:eu-2014-24:auto-prazo-minimo-art28-6-b@v1

- leitor:a16: {"tipo": "prazo_minimo", "condicoes": [{"field": "tipo_procedimento", "op": "eq", "value": "concurso_limitado_previa_qualificacao"}, {"field": "urgencia_fundamentada", "op": "eq", "value": true}], "params": {"minimum_days": 10, "deadline_field": "prazo_propostas_dias", "counted_from": "data_envio_convite", "usual_days": null}}
- leitor:b: {"tipo": "prazo_minimo", "condicoes": [{"field": "tipo_procedimento", "op": "eq", "value": "concurso_limitado_previa_qualificacao"}, {"field": "urgencia_fundamentada", "op": "eq", "value": true}], "params": {"minimum_days": 10, "deadline_field": "prazo_propostas_dias", "counted_from": "data_envio_convite", "usual_days": null}}
- verificador (A): regra 1, tipo_procedimento eq concurso_limitado_previa_qualificacao: as fontes não nomeiam ['concurso_limitado_previa_qualificacao']; regra 1: counted_from data_envio_convite e as fontes dizem nada (L9)

## regra:eu-2014-24:auto-prazo-minimo-art29-1@v1

- leitor:a16: {"tipo": "prazo_minimo", "condicoes": [{"field": "tipo_procedimento", "op": "eq", "value": "procedimento_concorrencial_negociacao"}], "params": {"minimum_days": 30, "deadline_field": "prazo_reclamacao_dias", "counted_from": "data_envio_anuncio", "usual_days": null}}
- leitor:b: não tipável (texto_em_falta): Falta o texto dos n.os 3 a 6 do artigo 28.º, declarado aplicável, para determinar os prazos mínimos e as respetivas condições.
- verificador (A): regra 1, tipo_procedimento eq procedimento_concorrencial_negociacao: as fontes não nomeiam ['procedimento_concorrencial_negociacao']; regra 1: deadline_field prazo_reclamacao_dias e as fontes dizem ['prazo_candidaturas_dias'] (L9)

## regra:eu-2014-24:auto-prazo-minimo-art30-1@v1

- leitor:a16: {"tipo": "prazo_minimo", "condicoes": [{"field": "tipo_procedimento", "op": "eq", "value": "dialogo_concorrencial"}], "params": {"minimum_days": 30, "deadline_field": "prazo_reclamacao_dias", "counted_from": "data_envio_anuncio", "usual_days": null}}
- leitor:b: {"tipo": "prazo_minimo", "condicoes": [{"field": "tipo_procedimento", "op": "eq", "value": "dialogo_concorrencial"}], "params": {"minimum_days": 30, "deadline_field": "prazo_candidaturas_dias", "counted_from": "data_envio_anuncio", "usual_days": null}}
- verificador (A): regra 1, tipo_procedimento eq dialogo_concorrencial: as fontes não nomeiam ['dialogo_concorrencial']; regra 1: deadline_field prazo_reclamacao_dias e as fontes dizem ['prazo_candidaturas_dias'] (L9)
- verificador (B): regra 1, tipo_procedimento eq dialogo_concorrencial: as fontes não nomeiam ['dialogo_concorrencial']

## regra:eu-2014-24:auto-prazo-minimo-art31-1@v1

- leitor:a16: {"tipo": "prazo_minimo", "condicoes": [{"field": "tipo_procedimento", "op": "eq", "value": "parceria_inovacao"}], "params": {"minimum_days": 30, "deadline_field": "prazo_reclamacao_dias", "counted_from": "data_envio_anuncio", "usual_days": null}}
- leitor:b: {"tipo": "prazo_minimo", "condicoes": [{"field": "tipo_procedimento", "op": "eq", "value": "parceria_inovacao"}], "params": {"minimum_days": 30, "deadline_field": "prazo_candidaturas_dias", "counted_from": "data_envio_anuncio", "usual_days": null}}
- verificador (A): regra 1: deadline_field prazo_reclamacao_dias e as fontes dizem ['prazo_candidaturas_dias'] (L9)

## regra:eu-2014-24:auto-prazo-minimo-art34-2-a@v1

- leitor:a16: não tipável (sem_vocabulario): A regra é de um sistema de aquisição dinâmico, instrumento que o vocabulário não tem.
- leitor:b: não tipável (sem_vocabulario): O vocabulário não permite limitar a regra às aquisições no âmbito de um sistema de aquisição dinâmico.

## regra:eu-2014-24:auto-prazo-minimo-art34-2-b@v1

- leitor:a16: não tipável (sem_vocabulario): A regra é de um sistema de aquisição dinâmico, instrumento que o vocabulário não tem.
- leitor:b: não tipável (sem_vocabulario): O vocabulário não permite limitar a regra às aquisições no âmbito de um sistema de aquisição dinâmico.

## regra:eu-2014-24:auto-prazo-maximo-art34-5@v1

- leitor:a16: não tipável (sem_vocabulario): A regra é de um sistema de aquisição dinâmico, instrumento que o vocabulário não tem.
- leitor:b: não tipável (nao_e_prazo_maximo): A passagem fixa prazos para a própria entidade adjudicante avaliar pedidos e comunicar a admissão, não para apresentar algo.

## regra:eu-2014-24:auto-prazo-maximo-art34-7@v1

- leitor:a16: não tipável (sem_vocabulario): A regra é de um sistema de aquisição dinâmico, instrumento que o vocabulário não tem.
- leitor:b: não tipável (sem_vocabulario): O vocabulário não contempla sistemas de aquisição dinâmicos nem prazos em dias úteis.

## regra:eu-2014-24:auto-prazo-maximo-art35-5@v1

- leitor:a16: não tipável (nao_e_prazo_maximo): O prazo é o de início do leilão eletrónico, não um prazo máximo para os interessados apresentarem algo.
- leitor:b: não tipável (nao_e_prazo_maximo): A passagem fixa um intervalo mínimo para o início do leilão eletrónico, não um prazo máximo para apresentar algo.

## regra:eu-2014-24:auto-prazo-minimo-art47-3-a@v1

- leitor:a16: {"tipo": "prazo_minimo", "condicoes": [{"field": "publicado_joue", "op": "eq", "value": false}, {"field": "tipo_procedimento", "op": "eq", "value": "concurso_aberto"}, {"field": "urgencia_fundamentada", "op": "eq", "value": false}], "params": {"minimum_days": 6, "deadline_field": "prazo_propostas_dias", "counted_from": "nao_indicado", "usual_days": null}}
- leitor:b: não tipável (nao_e_prazo_minimo): A passagem fixa uma condição de prorrogação relativa ao fornecimento de informações adicionais pela entidade adjudicante.
- verificador (A): regra 1, publicado_joue eq False: as fontes não negam o facto (L7); regra 1, urgencia_fundamentada eq False: as fontes não negam o facto (L7)

## regra:eu-2014-24:auto-prazo-maximo-art48-2-d@v1

- leitor:a16: não tipável (sem_vocabulario): O prazo é contado em meses, unidade que o vocabulário não tem.
- leitor:b: não tipável (nao_e_prazo_maximo): O limite fixa o período abrangido pelo anúncio de pré-informação, não um prazo para apresentar algo.

## regra:eu-2014-24:auto-prazo-maximo-art50-1@v1

- leitor:a16: não tipável (nao_e_prazo_minimo): O prazo é um máximo para as autoridades adjudicantes enviarem o anúncio de adjudicação, não um prazo para os interessados apresentarem algo.
- leitor:b: não tipável (nao_e_prazo_maximo): O prazo é para a própria entidade adjudicante enviar o anúncio de adjudicação do contrato.

## regra:eu-2014-24:auto-prazo-maximo-art50-2@v1

- leitor:a16: não tipável (texto_em_falta): Os contratos baseados no acordo-quadro estão no artigo 33.º, que não é mostrado.
- leitor:b: não tipável (nao_e_prazo_maximo): O prazo é para a própria entidade adjudicante enviar os anúncios agrupados.

## regra:eu-2014-24:auto-prazo-maximo-art50-3@v1

- leitor:a16: não tipável (sem_vocabulario): A regra vale só para contratos celebrados em sistema de aquisição dinâmico, instrumento que o vocabulário não tem.
- leitor:b: não tipável (nao_e_prazo_maximo): Os prazos são para a própria autoridade adjudicante enviar anúncios de adjudicação.

## regra:eu-2014-24:auto-prazo-maximo-art51-2@v1

- leitor:a16: não tipável (texto_em_falta): Os cinco dias são o prazo do Serviço das Publicações da União Europeia para publicar os anúncios, e não um prazo máximo para os interessados apresentarem algo.
- leitor:b: não tipável (nao_e_prazo_maximo): O prazo é para a publicação dos anúncios, não para apresentar elementos.

## regra:eu-2014-24:auto-prazo-maximo-art53-1@v1

- leitor:a16: não tipável (texto_em_falta): Os dias a contar da publicação do anúncio estão no texto do artigo 22.º, n.º 1, segundo parágrafo, que não está mostrado.
- leitor:b: não tipável (nao_e_prazo_maximo): A passagem fixa uma prorrogação de cinco dias, sem estabelecer um prazo máximo para a apresentação de propostas.

## regra:eu-2014-24:auto-prazo-maximo-art53-2@v1

- leitor:a16: não tipável (nao_e_prazo_minimo): O prazo é um máximo para a comunicação de informações, não um prazo para apresentar algo.
- leitor:b: não tipável (nao_e_prazo_maximo): O prazo é para a própria entidade adjudicante comunicar informações adicionais aos concorrentes.

## regra:eu-2014-24:auto-prazo-maximo-art55-2@v1

- leitor:a16: não tipável (sem_vocabulario): A regra é de um sistema de aquisição dinâmico, instrumento que o vocabulário não tem.
- leitor:b: não tipável (nao_e_prazo_maximo): O prazo é para a própria entidade adjudicante comunicar informações.

## regra:eu-2014-24:auto-prazo-maximo-art75-2@v1

- leitor:a16: não tipável (nao_e_prazo_maximo): O prazo é o da própria entidade adjudicante para agrupar os anúncios, não um prazo para os interessados apresentarem algo.
- leitor:b: não tipável (nao_e_prazo_maximo): O prazo é para a própria entidade adjudicante enviar os anúncios agrupados.

## regra:eu-2014-24:auto-limiar-art83-6-a@v1

- leitor:a16: não tipável (nao_e_limiar): o valor não é o limite até ao qual um procedimento pode ser escolhido
- leitor:b: não tipável (nao_e_limiar): O valor determina a obrigação de conservar cópias dos contratos, sem fixar um limite até ao qual um procedimento pode ser escolhido.

## regra:eu-2014-24:auto-limiar-art83-6-b@v1

- leitor:a16: não tipável (nao_e_limiar): O valor obriga as autoridades adjudicantes a conservar os contratos, não é o limite até ao qual um procedimento pode ser escolhido.
- leitor:b: não tipável (nao_e_limiar): O valor determina uma obrigação de conservação de cópias dos contratos, não um limite para a escolha de um procedimento.

## regra:eu-2014-25:auto-limiar-art15-a@v1

- leitor:a16: {"tipo": "limiar", "condicoes": [{"field": "tipo_contrato", "op": "in", "value": ["bens", "servicos", "servicos_sociais"]}, {"field": "tipo_procedimento", "op": "eq", "value": "concurso_concecao"}], "params": {"threshold": {"field": "valor_estimado", "comparator": "ge", "value": 432000, "currency": "EUR"}}}
- leitor:b: não tipável (nao_e_limiar): O valor delimita a aplicação da diretiva, não fixa um limite até ao qual um procedimento pode ser escolhido.
- verificador (A): regra 1, tipo_contrato in ['bens', 'servicos', 'servicos_sociais']: as fontes não nomeiam ['servicos_sociais']; regra 1: value 432000 não está nas fontes (L10)

## regra:eu-2014-25:auto-limiar-art15-b@v1

- leitor:a16: {"tipo": "limiar", "condicoes": [{"field": "tipo_contrato", "op": "eq", "value": "obras"}, {"field": "tipo_procedimento", "op": "eq", "value": "concurso_concecao"}], "params": {"threshold": {"field": "valor_estimado", "comparator": "ge", "value": 5404000, "currency": "EUR"}}}
- leitor:b: não tipável (nao_e_limiar): O valor delimita a aplicação da diretiva, não o valor até ao qual um procedimento pode ser escolhido.
- verificador (A): regra 1, tipo_procedimento in ['concurso_concecao']: as fontes não nomeiam ['concurso_concecao']; regra 1: value 5404000 não está nas fontes (L10)

## regra:eu-2014-25:auto-limiar-art15-c@v1

- leitor:a16: {"tipo": "limiar", "condicoes": [{"field": "tipo_contrato", "op": "eq", "value": "servicos_sociais"}, {"field": "tipo_procedimento", "op": "in", "value": ["concurso_aberto", "concurso_concecao", "concurso_publico", "dialogo_concorrencial", "parceria_inovacao"]}], "params": {"threshold": {"field": "valor_estimado", "comparator": "ge", "value": 1000000, "currency": "EUR"}}}
- leitor:b: não tipável (nao_e_limiar): O valor delimita o âmbito de aplicação da diretiva, não o limite até ao qual um procedimento pode ser escolhido.
- verificador (A): regra 1, tipo_procedimento in ['concurso_aberto', 'concurso_concecao', 'concurso_publico', 'dialogo_concorrencial', 'parceria_inovacao']: as fontes não nomeiam ['concurso_aberto', 'concurso_concecao', 'concurso_publico', 'dialogo_concorrencial', 'parceria_inovacao']; regra 1: value 1000000 não está nas fontes (L10)

## regra:eu-2014-25:auto-limiar-art16-10@v1

- leitor:a16: {"tipo": "limiar", "condicoes": [{"field": "tipo_contrato", "op": "eq", "value": "bens"}, {"field": "tipo_procedimento", "op": "eq", "value": "concurso_aberto"}], "params": {"threshold": {"field": "valor_estimado", "comparator": "lt", "value": 80000, "currency": "EUR"}}}
- leitor:b: não tipável (nao_e_limiar): Os valores delimitam uma dispensa de aplicação dos procedimentos da diretiva, não um limite até ao qual um procedimento pode ser escolhido.
- verificador (A): regra 1, tipo_procedimento eq concurso_aberto: as fontes não nomeiam ['concurso_aberto']; regra 1: value 80000 não está nas fontes (L10)

## regra:eu-2014-25:auto-limiar-art17-1@v1

- leitor:a16: não tipável (texto_em_falta): Os valores dos limiares estão no Acordo sobre Contratos Públicos da Organização Mundial do Comércio, que não é mostrado.
- leitor:b: não tipável (nao_e_limiar): A passagem estabelece um método de revisão dos limiares, sem fixar um valor até ao qual um procedimento pode ser escolhido.

## regra:eu-2014-25:auto-limiar-art17-2@v1

- leitor:a16: não tipável (texto_em_falta): Os valores dos limiares estão nos artigos 15.º, alíneas a) e b), que não estão mostrados.
- leitor:b: não tipável (nao_e_limiar): A passagem regula a determinação do contravalor dos limiares em moedas nacionais, sem fixar um limite de valor para a escolha de um procedimento.

## regra:eu-2014-25:auto-prazo-minimo-art45-1@v1

- leitor:a16: {"tipo": "prazo_minimo", "condicoes": [{"field": "tipo_procedimento", "op": "eq", "value": "concurso_publico"}], "params": {"minimum_days": 35, "deadline_field": "prazo_propostas_dias", "counted_from": "data_envio_anuncio", "usual_days": null}}
- leitor:b: {"tipo": "prazo_minimo", "condicoes": [{"field": "tipo_procedimento", "op": "eq", "value": "concurso_aberto"}], "params": {"minimum_days": 35, "deadline_field": "prazo_propostas_dias", "counted_from": "data_envio_anuncio", "usual_days": null}}

## regra:eu-2014-25:auto-prazo-minimo-art45-2-b@v1

- leitor:a16: {"tipo": "prazo_minimo", "condicoes": [{"field": "anuncio_pre_informacao", "op": "eq", "value": false}, {"field": "publicado_joue", "op": "eq", "value": false}, {"field": "tipo_procedimento", "op": "eq", "value": "concurso_publico"}, {"field": "urgencia_fundamentada", "op": "eq", "value": false}], "params": {"minimum_days": 15, "deadline_field": "prazo_propostas_dias", "counted_from": "data_envio_anuncio", "usual_days": null}}
- leitor:b: não tipável (nao_e_prazo_minimo): A passagem fixa a antecedência do envio do anúncio periódico indicativo pela entidade adjudicante, sem fixar um prazo mínimo para apresentação de elementos pelos interessados.
- verificador (A): regra 1, anuncio_pre_informacao eq False: as fontes não negam o facto (L7); regra 1, publicado_joue eq False: as fontes não negam o facto (L7); regra 1, urgencia_fundamentada eq False: as fontes não negam o facto (L7)

## regra:eu-2014-25:auto-prazo-minimo-art45-3@v1

- leitor:a16: {"tipo": "prazo_minimo", "condicoes": [{"field": "publicado_joue", "op": "eq", "value": true}, {"field": "tipo_procedimento", "op": "eq", "value": "concurso_publico"}, {"field": "urgencia_fundamentada", "op": "eq", "value": true}], "params": {"minimum_days": 15, "deadline_field": "prazo_propostas_dias", "counted_from": "data_envio_anuncio", "usual_days": null}}
- leitor:b: {"tipo": "prazo_minimo", "condicoes": [{"field": "tipo_procedimento", "op": "eq", "value": "concurso_aberto"}, {"field": "urgencia_fundamentada", "op": "eq", "value": true}], "params": {"minimum_days": 15, "deadline_field": "prazo_propostas_dias", "counted_from": "data_envio_anuncio", "usual_days": null}}
- verificador (A): regra 1, publicado_joue eq True: as fontes não afirmam o facto (L7)

## regra:eu-2014-25:auto-prazo-maximo-art45-4@v1

- leitor:a16: não tipável (sem_vocabulario): A redução vale só para os contratos de empreitada de obras e os concursos de conceção, instrumentos que o vocabulário não tem.
- leitor:b: não tipável (nao_e_prazo_maximo): A passagem reduz um prazo mínimo de receção de propostas, não fixa um prazo máximo.
- verificador (B): não tipável: fonte em eu-2014-25:art45.1, que é vizinho (L1)

## regra:eu-2014-25:auto-prazo-minimo-art46-1@v1

- leitor:a16: {"tipo": "prazo_minimo", "condicoes": [{"field": "tipo_procedimento", "op": "eq", "value": "concurso_limitado_previa_qualificacao"}], "params": {"minimum_days": 15, "deadline_field": "prazo_reclamacao_dias", "counted_from": "data_envio_anuncio", "usual_days": 30}}
- leitor:b: não tipável (sem_vocabulario): O vocabulário não permite representar o início alternativo da contagem nem distinguir os casos de envio do anúncio e de envio do convite à confirmação de interesse.
- verificador (A): regra 1: deadline_field prazo_reclamacao_dias e as fontes dizem ['prazo_candidaturas_dias'] (L9); regra 1: usual_days sem «em regra» e os dias nas fontes (L11)

## regra:eu-2014-25:auto-prazo-minimo-art46-2@v1

- leitor:a16: não tipável (texto_em_falta): Os dias do prazo de preparação e apresentação das propostas estão no acordo entre a entidade adjudicante e os candidatos, e não são fixados na passagem-alvo.
- leitor:b: não tipável (sem_vocabulario): Falta no vocabulário uma condição que represente a ausência de acordo sobre o prazo de receção das propostas.

## regra:eu-2014-25:auto-prazo-minimo-art47-1@v1

- leitor:a16: {"tipo": "prazo_minimo", "condicoes": [{"field": "anuncio_pre_informacao", "op": "eq", "value": true}, {"field": "tipo_procedimento", "op": "eq", "value": "procedimento_negociacao_com_concurso"}], "params": {"minimum_days": 30, "deadline_field": "prazo_reclamacao_dias", "counted_from": "data_envio_anuncio", "usual_days": null}} || {"tipo": "prazo_minimo", "condicoes": [{"field": "anuncio_pre_informacao", "op": "eq", "value": false}, {"field": "tipo_procedimento", "op": "eq", "value": "procedimento_negociacao_com_concurso"}], "params": {"minimum_days": 15, "deadline_field": "prazo_reclamacao_dias", "counted_from": "data_envio_anuncio", "usual_days": null}}
- leitor:b: não tipável (sem_vocabulario): Falta uma condição que distinga a utilização do anúncio periódico indicativo como meio de abertura de concurso da sua mera publicação, pois essa utilização determina o início da contagem.
- verificador (A): regra 1: deadline_field prazo_reclamacao_dias e as fontes dizem ['prazo_candidaturas_dias'] (L9); regra 2: deadline_field prazo_reclamacao_dias e as fontes dizem ['prazo_candidaturas_dias'] (L9)

## regra:eu-2014-25:auto-prazo-minimo-art47-2@v1

- leitor:a16: não tipável (texto_em_falta): Os dias do prazo de receção das propostas só são fixados de comum acordo entre a entidade adjudicante e os candidatos, e o número não está no texto mostrado.
- leitor:b: não tipável (sem_vocabulario): O vocabulário não permite representar a falta de acordo sobre o prazo de receção das propostas.

## regra:eu-2014-25:auto-prazo-minimo-art48-1@v1

- leitor:a16: {"tipo": "prazo_minimo", "condicoes": [{"field": "tipo_procedimento", "op": "eq", "value": "dialogo_concorrencial"}], "params": {"minimum_days": 30, "deadline_field": "prazo_reclamacao_dias", "counted_from": "data_envio_anuncio", "usual_days": null}} || {"tipo": "prazo_minimo", "condicoes": [{"field": "anuncio_pre_informacao", "op": "eq", "value": true}, {"field": "publicado_joue", "op": "eq", "value": true}, {"field": "tipo_procedimento", "op": "eq", "value": "dialogo_concorrencial"}, {"field": "urgencia_fundamentada", "op": "eq", "value": false}], "params": {"minimum_days": 15, "deadline_field": "prazo_reclamacao_dias", "counted_from": "data_envio_anuncio", "usual_days": null}}
- leitor:b: {"tipo": "prazo_minimo", "condicoes": [{"field": "anuncio_pre_informacao", "op": "eq", "value": false}, {"field": "tipo_procedimento", "op": "eq", "value": "dialogo_concorrencial"}], "params": {"minimum_days": 15, "deadline_field": "prazo_candidaturas_dias", "counted_from": "data_envio_anuncio", "usual_days": 30}} || {"tipo": "prazo_minimo", "condicoes": [{"field": "anuncio_pre_informacao", "op": "eq", "value": true}, {"field": "tipo_procedimento", "op": "eq", "value": "dialogo_concorrencial"}], "params": {"minimum_days": 15, "deadline_field": "prazo_candidaturas_dias", "counted_from": "data_envio_convite", "usual_days": 30}}
- verificador (A): regra 1, tipo_procedimento eq dialogo_concorrencial: as fontes não nomeiam ['dialogo_concorrencial']; regra 1: deadline_field prazo_reclamacao_dias e as fontes dizem ['prazo_candidaturas_dias'] (L9); regra 2, tipo_procedimento eq dialogo_concorrencial: as fontes não nomeiam ['dialogo_concorrencial']; regra 2, anuncio_pre_informacao eq True: as fontes não afirmam o facto (L7); regra 2, publicado_joue eq True: as fontes não afirmam o facto (L7); regra 2, urgencia_fundamentada eq False: as fontes não negam o facto (L7)
- verificador (B): regra 1, tipo_procedimento eq dialogo_concorrencial: as fontes não nomeiam ['dialogo_concorrencial']; regra 1: usual_days sem «em regra» e os dias nas fontes (L11); regra 2, tipo_procedimento eq dialogo_concorrencial: as fontes não nomeiam ['dialogo_concorrencial']; regra 2: counted_from data_envio_convite e as fontes dizem ['data_envio_anuncio'] (L9); regra 2: usual_days sem «em regra» e os dias nas fontes (L11)

## regra:eu-2014-25:auto-prazo-minimo-art49-1@v1

- leitor:a16: {"tipo": "prazo_minimo", "condicoes": [{"field": "tipo_procedimento", "op": "eq", "value": "parceria_inovacao"}], "params": {"minimum_days": 30, "deadline_field": "prazo_reclamacao_dias", "counted_from": "data_envio_anuncio", "usual_days": null}}
- leitor:b: {"tipo": "prazo_minimo", "condicoes": [{"field": "tipo_procedimento", "op": "eq", "value": "parceria_inovacao"}], "params": {"minimum_days": 15, "deadline_field": "prazo_candidaturas_dias", "counted_from": "data_envio_anuncio", "usual_days": 30}}
- verificador (A): regra 1: deadline_field prazo_reclamacao_dias e as fontes dizem ['prazo_candidaturas_dias'] (L9)
- verificador (B): regra 1: usual_days sem «em regra» e os dias nas fontes (L11)

## regra:eu-2014-25:auto-prazo-minimo-art52-2-a@v1

- leitor:a16: não tipável (sem_vocabulario): A regra é de um sistema de aquisição dinâmico, instrumento que o vocabulário não tem.
- leitor:b: não tipável (sem_vocabulario): O vocabulário não permite limitar a regra às aquisições no âmbito de um sistema de aquisição dinâmico.

## regra:eu-2014-25:auto-prazo-minimo-art52-2-b@v1

- leitor:a16: não tipável (sem_vocabulario): A regra é de um sistema de aquisição dinâmico, instrumento que o vocabulário não tem.
- leitor:b: não tipável (sem_vocabulario): O vocabulário não permite limitar a regra às aquisições no âmbito de um sistema de aquisição dinâmico.

## regra:eu-2014-25:auto-prazo-maximo-art52-5@v1

- leitor:a16: não tipável (sem_vocabulario): O prazo é de 10 dias úteis para a avaliação dos pedidos de participação, prazo que só vale no sistema de aquisição dinâmico e que o vocabulário não tem.
- leitor:b: não tipável (nao_e_prazo_maximo): O prazo é para a própria entidade adjudicante avaliar os pedidos de participação, não para apresentar elementos.

## regra:eu-2014-25:auto-prazo-maximo-art52-7@v1

- leitor:a16: não tipável (sem_vocabulario): A regra é de um sistema de aquisição dinâmico, instrumento que o vocabulário não tem.
- leitor:b: não tipável (sem_vocabulario): O vocabulário não contempla sistemas de aquisição dinâmicos nem prazos em dias úteis.

## regra:eu-2014-25:auto-prazo-maximo-art53-5@v1

- leitor:a16: não tipável (nao_e_prazo_maximo): O prazo é o da própria entidade adjudicante para fazer a primeira avaliação completa das propostas, e não um prazo máximo para os interessados apresentarem algo.
- leitor:b: não tipável (nao_e_prazo_maximo): A passagem fixa um prazo mínimo para o início do leilão eletrónico, não um prazo máximo para apresentar algo.

## regra:eu-2014-25:auto-prazo-minimo-art66-3-a@v1

- leitor:a16: não tipável (texto_em_falta): Os dias de prorrogação estão nos artigos 45.º a 49.º, que não estão mostrados.
- leitor:b: não tipável (nao_e_prazo_minimo): A passagem estabelece quando a entidade adjudicante deve prorrogar o prazo por falta de informações adicionais, sem fixar um prazo mínimo para apresentação de propostas.

## regra:eu-2014-25:auto-prazo-maximo-art67-2-d@v1

- leitor:a16: não tipável (texto_em_falta): Os dias do período em que o anúncio periódico indicativo pode ser enviado antes do convite estão no artigo 92.º, n.º 1, alínea b), que não é mostrado.
- leitor:b: não tipável (nao_e_prazo_maximo): A passagem regula o envio e o período abrangido pelo anúncio periódico indicativo, sem fixar um prazo para apresentar elementos.

## regra:eu-2014-25:auto-prazo-maximo-art70-1@v1

- leitor:a16: não tipável (nao_e_prazo_minimo): O prazo é um máximo, não um mínimo.
- leitor:b: não tipável (nao_e_prazo_maximo): O prazo é para as próprias entidades adjudicantes enviarem um anúncio de adjudicação do contrato.

## regra:eu-2014-25:auto-prazo-maximo-art70-2@v1

- leitor:a16: não tipável (texto_em_falta): Os dias do prazo para não adjudicar mais contratos durante o período do anúncio periódico indicativo não estão no texto mostrado.
- leitor:b: não tipável (nao_e_prazo_maximo): Os prazos regulam o envio de anúncios pelas próprias entidades adjudicantes.

## regra:eu-2014-25:auto-prazo-maximo-art71-2@v1

- leitor:a16: não tipável (texto_em_falta): Os cinco dias são o prazo do Serviço das Publicações da União Europeia para publicar o anúncio, e não um prazo para os interessados apresentarem algo.
- leitor:b: não tipável (nao_e_prazo_maximo): O prazo é para a publicação dos anúncios, não para apresentar algo.

## regra:eu-2014-25:auto-prazo-maximo-art73-1@v1

- leitor:a16: não tipável (nao_e_prazo_minimo): O prazo é de acesso à documentação, não um prazo para apresentar algo.
- leitor:b: não tipável (nao_e_prazo_maximo): A passagem fixa uma prorrogação de cinco dias, sem estabelecer um prazo máximo para a apresentação de propostas.

## regra:eu-2014-25:auto-prazo-maximo-art73-2@v1

- leitor:a16: não tipável (nao_e_prazo_minimo): O prazo é um máximo para a comunicação de informações, não um prazo para apresentar algo.
- leitor:b: não tipável (nao_e_prazo_maximo): O prazo destina-se à própria entidade adjudicante, para comunicar informações adicionais aos concorrentes.

## regra:eu-2014-25:auto-prazo-maximo-art75-2@v1

- leitor:a16: não tipável (sem_vocabulario): A regra só vale para os sistemas de aquisição dinâmicos, instrumento que o vocabulário não tem.
- leitor:b: não tipável (nao_e_prazo_maximo): O prazo destina-se à própria entidade adjudicante para prestar informações.

## regra:eu-2014-25:auto-prazo-maximo-art75-5@v1

- leitor:a16: não tipável (sem_vocabulario): A regra é de um sistema de qualificação, instrumento que o vocabulário não tem.
- leitor:b: não tipável (nao_e_prazo_maximo): O prazo destina-se à entidade adjudicante informar os requerentes da recusa da qualificação e das suas razões, não à apresentação de elementos pelos interessados.

## regra:eu-2014-25:auto-prazo-minimo-art75-6@v1

- leitor:a16: não tipável (sem_vocabulario): A regra só vale para os operadores económicos que estão sob um sistema de qualificação, instrumento que o vocabulário não tem.
- leitor:b: não tipável (nao_e_prazo_minimo): O prazo destina-se à notificação pela entidade adjudicante, não à apresentação de elementos pelo operador económico.

## regra:eu-2014-25:auto-prazo-maximo-art92-2@v1

- leitor:a16: não tipável (nao_e_prazo_maximo): O prazo é de 30 dias para a publicação dos anúncios agrupados, não um prazo máximo para os interessados apresentarem algo.
- leitor:b: não tipável (nao_e_prazo_maximo): O prazo é para a própria entidade adjudicante enviar os anúncios agrupados.

## regra:eu-2014-25:auto-prazo-maximo-art96-2@v1

- leitor:a16: não tipável (texto_em_falta): Os dias do prazo estão no anexo XIX, que não é mostrado.
- leitor:b: não tipável (nao_e_prazo_maximo): O prazo destina-se à própria entidade adjudicante comunicar o anúncio dos resultados do concurso.

## regra:eu-2014-25:auto-limiar-art99-6-a@v1

- leitor:a16: não tipável (nao_e_limiar): o valor não é o limite até ao qual um procedimento pode ser escolhido
- leitor:b: não tipável (nao_e_limiar): O valor determina uma obrigação de conservação de cópias dos contratos, não um limite até ao qual um procedimento pode ser escolhido.

## regra:eu-2014-25:auto-limiar-art99-6-b@v1

- leitor:a16: não tipável (nao_e_limiar): o valor não é o limite até ao qual um procedimento pode ser escolhido
- leitor:b: não tipável (nao_e_limiar): O valor determina a obrigação de conservar cópias dos contratos, não o limite até ao qual um procedimento pode ser escolhido.

