# FÁBRICA DE REGRAS — ronda 13 (DECISIONS D74)

Gerado por tools/rule_factory.py (ccp-rule-factory-0.8) com o protocolo de leitura v3 (tools/read_rules_v3.py, ccp-read-rules-v3-0.5). D74: v15 relê a ronda 12 (os mesmos prompts, byte a byte; as respostas cegas do leitor:b vêm da ronda 12). O exame é o grupo reservado; um alvo já assente é lido e medido mas não volta a ser registado. Propõe leitor:a17 (AMALIA + adaptador v15), leitor:b revê às cegas.

Protocolo 0.5. Um programa confirma cada palavra citada; o «não tipável» com o mesmo motivo também assenta.

| grupo | alvos | leitor A válido | leitor B válido | assentes | regras | «não tipável» |
|---|---|---|---|---|---|---|
| pratica | 229 | 201 | 204 | 119 | 2 | 117 |
| reservado | 67 | 58 | 60 | 37 | 0 | 37 |
| todos | 296 | 259 | 264 | 156 | 2 | 154 |

| regra | passagem | estado | replica | verificador: leitor A | verificador: leitor B |
|---|---|---|---|---|---|
| regra:ccp:auto-prazo-maximo-art35-b-3@v1 | ccp:art35-b.3 | settled (não tipável: nao_e_prazo_maximo) | sim | ok | ok |
| regra:ccp:auto-prazo-maximo-art43-v20180101@v1 | ccp:art43 | proposed (não tipável: nao_e_prazo_maximo) | — | ok | não tipável: fonte em ccp:art43.10.a, que é vizinho (L1) |
| regra:ccp:auto-prazo-maximo-art43-v20251028@v1 | ccp:art43 | proposed (não tipável: nao_e_prazo_maximo) | — | ok | não tipável: fonte em ccp:art43.10.a, que é vizinho (L1) |
| regra:ccp:auto-prazo-maximo-art65@v1 | ccp:art65 | settled (não tipável: nao_e_prazo_maximo) | sim | ok | ok |
| regra:ccp:auto-prazo-maximo-art72-v20180101@v1 | ccp:art72 | proposed (não tipável: nao_e_prazo_maximo) | não | ok | ok |
| regra:ccp:auto-prazo-maximo-art72-v20221202@v1 | ccp:art72 | proposed (não tipável: nao_e_prazo_maximo) | não | ok | ok |
| regra:ccp:auto-prazo-maximo-art72-3@v1 | ccp:art72.3 | proposed (não tipável: nao_e_prazo_maximo) | não | ok | ok |
| regra:ccp:auto-prazo-maximo-art78-v20180101@v1 | ccp:art78 | proposed (não tipável: nao_e_prazo_maximo) | — | ok | não tipável: fonte em ccp:art78.5, que é vizinho (L1) |
| regra:ccp:auto-prazo-maximo-art78-1-v20080730@v1 | ccp:art78.1 | settled (não tipável: nao_e_prazo_maximo) | sim | ok | ok |
| regra:ccp:auto-prazo-maximo-art78-1@v1 | ccp:art78.1 | settled (não tipável: nao_e_prazo_maximo) | sim | ok | ok |
| regra:ccp:auto-prazo-maximo-art78-5@v1 | ccp:art78.5 | settled (não tipável: nao_e_prazo_maximo) | sim | ok | ok |
| regra:ccp:auto-prazo-maximo-art85-2@v1 | ccp:art85.2 | proposed (não tipável: nao_e_prazo_maximo) | não | ok | ok |
| regra:ccp:auto-prazo-maximo-art86-v20120811@v1 | ccp:art86 | proposed (não tipável: nao_e_prazo_maximo) | — | ok | não tipável: fonte em ccp:art86.2, que é vizinho (L1) |
| regra:ccp:auto-prazo-maximo-art86-2-v20091007@v1 | ccp:art86.2 | proposed (não tipável: nao_e_prazo_maximo) | não | ok | ok |
| regra:ccp:auto-prazo-maximo-art86-3@v1 | ccp:art86.3 | proposed (não tipável: nao_e_prazo_maximo) | não | ok | ok |
| regra:ccp:auto-prazo-maximo-art87-a-2@v1 | ccp:art87-a.2 | proposed (não tipável: nao_e_prazo_maximo) | não | ok | ok |
| regra:ccp:auto-prazo-maximo-art90-1@v1 | ccp:art90.1 | proposed (não tipável: nao_e_prazo_maximo) | não | ok | ok |
| regra:ccp:auto-prazo-maximo-art91-2@v1 | ccp:art91.2 | proposed (não tipável: nao_e_prazo_maximo) | não | ok | ok |
| regra:ccp:auto-prazo-maximo-art93-2@v1 | ccp:art93.2 | proposed (não tipável: nao_e_prazo_maximo) | não | ok | ok |
| regra:ccp:auto-prazo-maximo-art95-v20080730@v1 | ccp:art95 | proposed (não tipável: nao_e_prazo_maximo) | — | ok | não tipável: fonte em ccp:art95.1.c.i, que é vizinho (L1) |
| regra:ccp:auto-limiar-art95-1-a@v1 | ccp:art95.1.a | settled (não tipável: nao_e_limiar) | sim | ok | ok |
| regra:ccp:auto-prazo-maximo-art95-1-c-i@v1 | ccp:art95.1.c.i | settled (não tipável: nao_e_prazo_maximo) | sim | ok | ok |
| regra:ccp:auto-prazo-maximo-art95-3@v1 | ccp:art95.3 | settled (não tipável: nao_e_prazo_maximo) | sim | ok | ok |
| regra:ccp:auto-prazo-maximo-art101@v1 | ccp:art101 | proposed (não tipável: nao_e_prazo_maximo) | — | ok | regra 1: as fontes de maximum_days não dizem um máximo («não pode ser superior a», «no prazo de», L8) |
| regra:ccp:auto-prazo-maximo-art102-v20080730@v1 | ccp:art102 | proposed (não tipável: nao_e_prazo_maximo) | — | ok | não tipável: fonte em ccp:art102.2, que é vizinho (L1) |
| regra:ccp:auto-prazo-maximo-art102-2@v1 | ccp:art102.2 | settled (não tipável: nao_e_prazo_maximo) | sim | ok | ok |
| regra:ccp:auto-prazo-minimo-art104-v20080730@v1 | ccp:art104 | proposed (não tipável: nao_e_prazo_minimo) | — | ok | não tipável: fonte em ccp:art104.1, que é vizinho (L1) |
| regra:ccp:auto-prazo-maximo-art104-1-a@v1 | ccp:art104.1.a | settled (não tipável: nao_e_prazo_maximo) | sim | ok | ok |
| regra:ccp:auto-prazo-maximo-art108-1-v20080730@v1 | ccp:art108.1 | settled (não tipável: nao_e_prazo_maximo) | sim | ok | ok |
| regra:ccp:auto-prazo-maximo-art115-1-j-v20180101@v1 | ccp:art115.1.j | proposed (não tipável: nao_e_prazo_maximo) | não | ok | ok |
| regra:ccp:auto-prazo-maximo-art115-1-k@v1 | ccp:art115.1.k | proposed (não tipável: nao_e_prazo_maximo) | não | ok | ok |
| regra:ccp:auto-prazo-maximo-art122-v20180101@v1 | ccp:art122 | proposed (não tipável: nao_e_prazo_maximo) | — | ok | não tipável: fonte em ccp:art122.1, que é vizinho (L1) |
| regra:ccp:auto-prazo-maximo-art122-1@v1 | ccp:art122.1 | settled (não tipável: nao_e_prazo_maximo) | sim | ok | ok |
| regra:ccp:auto-prazo-minimo-art135-2-v20080730@v1 | ccp:art135.2 | sem leitura válida de leitor:a17 | — | regra 1: minimum_days 19 não está nas fontes (L8, L4) | ok |
| regra:ccp:auto-prazo-minimo-art136-1-v20080730@v1 | ccp:art136.1 | sem leitura válida de leitor:a17 | — | regra 1, publicado_joue eq True: as fontes não afirmam o facto (L7) | ok |
| regra:ccp:auto-prazo-minimo-art136-3-v20080730@v1 | ccp:art136.3 | proposed | não | ok | ok |
| regra:ccp:auto-prazo-minimo-art136-4-v20080730@v1 | ccp:art136.4 | sem leitura válida de leitor:a17 | — | regra 1: counted_from data_envio_anuncio e as fontes dizem nada (L9) | ok |
| regra:ccp:auto-prazo-maximo-art138-3@v1 | ccp:art138.3 | proposed (não tipável: nao_e_prazo_maximo) | não | ok | ok |
| regra:ccp:auto-limiar-art155-a@v1 | ccp:art155.a | proposed | não | ok | ok |
| regra:ccp:auto-prazo-maximo-art159@v1 | ccp:art159 | settled (não tipável: nao_e_prazo_maximo) | sim | ok | ok |
| regra:ccp:auto-prazo-maximo-art161@v1 | ccp:art161 | sem leitura válida de leitor:a17 (params: Additional properties are not allowed ('maximum_days' was unexpected)) | sim | ok | ok |
| regra:ccp:auto-prazo-maximo-art161-b-1-b@v1 | ccp:art161-b.1.b | settled (não tipável: nao_e_prazo_maximo) | sim | ok | ok |
| regra:ccp:auto-prazo-maximo-art161-b-4@v1 | ccp:art161-b.4 | proposed (não tipável: nao_e_prazo_maximo) | não | ok | ok |
| regra:ccp:auto-prazo-minimo-art173@v1 | ccp:art173 | sem leitura válida de leitor:a17 | — | regra 1: counted_from data_envio_anuncio e as fontes dizem nada (L9) | ok |
| regra:ccp:auto-prazo-minimo-art174-v20180101@v1 | ccp:art174 | proposed (2 regras) | — | ok | regra 1, tipo_procedimento eq concurso_limitado_previa_qualificacao: fonte em ccp:art174.1, que é vizinho (L1) |
| regra:ccp:auto-prazo-minimo-art174-1-v20080730@v1 | ccp:art174.1 | sem leitura válida de leitor:a17 | — | regra 1, publicado_joue eq True: as fontes não afirmam o facto (L7) | ok |
| regra:ccp:auto-prazo-minimo-art174-2-v20080730@v1 | ccp:art174.2 | sem leitura válida de leitor:a17 | — | regra 1: counted_from data_envio_convite e as fontes dizem nada (L9) | ok |
| regra:ccp:auto-prazo-minimo-art174-3-v20080730@v1 | ccp:art174.3 | sem leitura válida de leitor:a17 | — | regra 1, tipo_contrato not_in ['concessao_obras', 'concessao_servicos']: as fontes não nomeiam ['concessao_servicos'] | ok |
| regra:ccp:auto-prazo-minimo-art174-4@v1 | ccp:art174.4 | proposed (não tipável: nao_e_prazo_minimo) | não | ok | ok |
| regra:ccp:auto-prazo-maximo-art177-3@v1 | ccp:art177.3 | proposed (não tipável: nao_e_prazo_maximo) | não | ok | ok |
| regra:ccp:auto-prazo-maximo-art187-1-v20080730@v1 | ccp:art187.1 | settled (não tipável: nao_e_prazo_maximo) | sim | ok | ok |
| regra:ccp:auto-prazo-maximo-art187-1-v20180101@v1 | ccp:art187.1 | settled (não tipável: nao_e_prazo_maximo) | sim | ok | ok |
| regra:ccp:auto-prazo-maximo-art187-1@v1 | ccp:art187.1 | settled (não tipável: nao_e_prazo_maximo) | sim | ok | ok |
| regra:ccp:auto-prazo-minimo-art187-2-v20180101@v1 | ccp:art187.2 | sem leitura válida de leitor:a17 | — | regra 1: deadline_field prazo_candidaturas_dias e as fontes dizem nada (L9) | ok |
| regra:ccp:auto-prazo-maximo-art187-4-v20180101@v1 | ccp:art187.4 | proposed (não tipável: nao_e_prazo_maximo) | não | ok | ok |
| regra:ccp:auto-prazo-maximo-art188-4@v1 | ccp:art188.4 | proposed (não tipável: nao_e_prazo_maximo) | não | ok | ok |
| regra:ccp:auto-prazo-minimo-art190-2-v20080730@v1 | ccp:art190.2 | sem leitura válida de leitor:a17 | — | regra 1: minimum_days 8 não está nas fontes (L8, L4) | ok |
| regra:ccp:auto-prazo-minimo-art190-2@v1 | ccp:art190.2 | proposed (2 regras) | não | ok | ok |
| regra:ccp:auto-prazo-minimo-art191-v20180101@v1 | ccp:art191 | sem leitura válida de leitor:a17 | — | regra 3, setores_especiais eq True: as fontes não afirmam o facto (L7) | não tipável: fonte em ccp:art191.2, que é vizinho (L1) |
| regra:ccp:auto-prazo-minimo-art191-2-a-v20080730@v1 | ccp:art191.2.a | settled (não tipável: sem_vocabulario) | sim | ok | ok |
| regra:ccp:auto-prazo-minimo-art191-2-a@v1 | ccp:art191.2.a | settled (não tipável: sem_vocabulario) | sim | ok | ok |
| regra:ccp:auto-prazo-maximo-art192-3@v1 | ccp:art192.3 | proposed (não tipável: nao_e_prazo_maximo) | não | ok | ok |
| regra:ccp:auto-prazo-maximo-art192-4@v1 | ccp:art192.4 | proposed (não tipável: nao_e_prazo_maximo) | não | ok | ok |
| regra:ccp:auto-prazo-minimo-art198-1-v20080730@v1 | ccp:art198.1 | proposed | — | ok | regra 1, publicado_joue eq True: as fontes não afirmam o facto (L7) |
| regra:ccp:auto-prazo-minimo-art218-v20080730@v1 | ccp:art218 | proposed | — | ok | regra 1, tipo_procedimento eq dialogo_concorrencial: «diálogo concorrencial» não está em ccp:art218 |
| regra:ccp:auto-prazo-maximo-art219-c-3-v20180101@v1 | ccp:art219-c.3 | settled (não tipável: nao_e_prazo_maximo) | sim | ok | ok |
| regra:ccp:auto-prazo-maximo-art219-c-3@v1 | ccp:art219-c.3 | settled (não tipável: nao_e_prazo_maximo) | sim | ok | ok |
| regra:ccp:auto-prazo-maximo-art219-i-5@v1 | ccp:art219-i.5 | sem leitura válida de leitor:a17 | — | regra 1: deadline_field prazo_habilitacao_dias e as fontes dizem nada (L9) | ok |
| regra:ccp:auto-prazo-maximo-art234-1-v20080730@v1 | ccp:art234.1 | sem leitura válida de leitor:a17 | — | regra 1: deadline_field prazo_habilitacao_dias e as fontes dizem nada (L9) | ok |
| regra:ccp:auto-prazo-maximo-art235-v20080730@v1 | ccp:art235 | settled (não tipável: nao_e_prazo_maximo) | sim | ok | ok |
| regra:ccp:auto-prazo-maximo-art241-3-v20080730@v1 | ccp:art241.3 | proposed (não tipável: sem_vocabulario) | não | ok | ok |
| regra:ccp:auto-prazo-maximo-art241-a-3@v1 | ccp:art241-a.3 | proposed (não tipável: sem_vocabulario) | não | ok | ok |
| regra:ccp:auto-prazo-minimo-art242-3-v20080730@v1 | ccp:art242.3 | proposed (não tipável: sem_vocabulario) | não | ok | ok |
| regra:ccp:auto-prazo-maximo-art270@v1 | ccp:art270 | proposed (não tipável: nao_e_prazo_maximo) | não | ok | ok |
| regra:ccp:auto-prazo-maximo-art273@v1 | ccp:art273 | proposed (não tipável: nao_e_prazo_maximo) | não | ok | ok |
| regra:ccp:auto-prazo-maximo-art274-1@v1 | ccp:art274.1 | settled (não tipável: nao_e_prazo_maximo) | sim | ok | ok |
| regra:ccp:auto-prazo-minimo-art276-v20120811@v1 | ccp:art276 | proposed (não tipável: nao_e_prazo_minimo) | não | ok | ok |
| regra:ccp:auto-prazo-minimo-art276-v20180101@v1 | ccp:art276 | sem leitura válida de leitor:a17 | — | regra 1, tipo_procedimento in ['ajuste_direto', 'concurso_limitado_previa_qualificacao', 'dialogo_concorrencial']: as fo | ok |
| regra:ccp:auto-prazo-minimo-art276-v20210620@v1 | ccp:art276 | proposed (não tipável: nao_e_prazo_minimo) | não | ok | ok |
| regra:ccp:auto-prazo-minimo-art276-5-v20080730@v1 | ccp:art276.5 | proposed (não tipável: nao_e_prazo_minimo) | não | ok | ok |
| regra:ccp:auto-prazo-maximo-art283-a-v20110113@v1 | ccp:art283-a | proposed (não tipável: nao_e_prazo_maximo) | — | ok | não tipável: fonte em ccp:art283-a.2.c, que é vizinho (L1) |
| regra:ccp:auto-prazo-maximo-art283-a-v20210620@v1 | ccp:art283-a | proposed (não tipável: nao_e_prazo_maximo) | — | ok | não tipável: fonte em ccp:art283-a.2.c, que é vizinho (L1) |
| regra:ccp:auto-prazo-maximo-art283-a-2-c@v1 | ccp:art283-a.2.c | settled (não tipável: nao_e_prazo_maximo) | sim | ok | ok |
| regra:ccp:auto-prazo-maximo-art287-6-c-v20180101@v1 | ccp:art287.6.c | settled (não tipável: nao_e_prazo_maximo) | sim | ok | ok |
| regra:ccp:auto-prazo-minimo-art295-v20091007@v1 | ccp:art295 | proposed (não tipável: nao_e_prazo_minimo) | — | ok | não tipável: fonte em ccp:art295.3, que é vizinho (L1) |
| regra:ccp:auto-prazo-maximo-art295-5-a-v20080730@v1 | ccp:art295.5.a | settled (não tipável: nao_e_prazo_maximo) | sim | ok | ok |
| regra:ccp:auto-prazo-maximo-art296-2@v1 | ccp:art296.2 | settled (não tipável: nao_e_prazo_maximo) | sim | ok | ok |
| regra:ccp:auto-prazo-maximo-art299-1-v20080730@v1 | ccp:art299.1 | settled (não tipável: nao_e_prazo_maximo) | sim | ok | ok |
| regra:ccp:auto-prazo-maximo-art299-1-a@v1 | ccp:art299.1.a | settled (não tipável: nao_e_prazo_maximo) | sim | ok | ok |
| regra:ccp:auto-prazo-maximo-art299-1-b@v1 | ccp:art299.1.b | settled (não tipável: nao_e_prazo_maximo) | sim | ok | ok |
| regra:ccp:auto-prazo-maximo-art299-1-c@v1 | ccp:art299.1.c | settled (não tipável: nao_e_prazo_maximo) | sim | ok | ok |
| regra:ccp:auto-prazo-maximo-art299-1-d@v1 | ccp:art299.1.d | settled (não tipável: nao_e_prazo_maximo) | sim | ok | ok |
| regra:ccp:auto-prazo-maximo-art299-2@v1 | ccp:art299.2 | settled (não tipável: nao_e_prazo_maximo) | sim | ok | ok |
| regra:ccp:auto-prazo-maximo-art299-3@v1 | ccp:art299.3 | settled (não tipável: nao_e_prazo_maximo) | sim | ok | ok |
| regra:ccp:auto-prazo-maximo-art299-a-1@v1 | ccp:art299-a.1 | settled (não tipável: nao_e_prazo_maximo) | sim | ok | ok |
| regra:ccp:auto-prazo-maximo-art315-v20210620@v1 | ccp:art315 | proposed (não tipável: nao_e_prazo_maximo) | — | ok | não tipável: fonte em ccp:art315.1, que é vizinho (L1) |
| regra:ccp:auto-prazo-maximo-art315-1-v20180101@v1 | ccp:art315.1 | settled (não tipável: nao_e_prazo_maximo) | sim | ok | ok |
| regra:ccp:auto-prazo-maximo-art315-1@v1 | ccp:art315.1 | settled (não tipável: nao_e_prazo_maximo) | sim | ok | ok |
| regra:ccp:auto-prazo-maximo-art319-3-v20080730@v1 | ccp:art319.3 | settled (não tipável: nao_e_prazo_maximo) | sim | ok | ok |
| regra:ccp:auto-prazo-maximo-art319-3-v20180101@v1 | ccp:art319.3 | settled (não tipável: nao_e_prazo_maximo) | sim | ok | ok |
| regra:ccp:auto-prazo-minimo-art327-v20080730@v1 | ccp:art327 | proposed (não tipável: nao_e_prazo_minimo) | — | ok | não tipável: fonte em ccp:art327.3, que é vizinho (L1) |
| regra:ccp:auto-prazo-maximo-art327-4@v1 | ccp:art327.4 | settled (não tipável: nao_e_prazo_maximo) | sim | ok | ok |
| regra:ccp:auto-prazo-maximo-art332-4@v1 | ccp:art332.4 | settled (não tipável: nao_e_prazo_maximo) | sim | ok | ok |
| regra:ccp:auto-prazo-maximo-art333-4@v1 | ccp:art333.4 | settled (não tipável: nao_e_prazo_maximo) | sim | ok | ok |
| regra:ccp:auto-prazo-maximo-art334-3@v1 | ccp:art334.3 | settled (não tipável: nao_e_prazo_maximo) | sim | ok | ok |
| regra:ccp:auto-prazo-maximo-art345-3@v1 | ccp:art345.3 | proposed (não tipável: nao_e_prazo_maximo) | — | ok | regra 1: as fontes de maximum_days não dizem um máximo («não pode ser superior a», «no prazo de», L8) |
| regra:ccp:auto-prazo-maximo-art345-4@v1 | ccp:art345.4 | proposed (não tipável: nao_e_prazo_maximo) | não | ok | ok |
| regra:ccp:auto-prazo-maximo-art354-v20080730@v1 | ccp:art354 | proposed (não tipável: nao_e_prazo_maximo) | — | ok | não tipável: fonte em ccp:art354.2, que é vizinho (L1) |
| regra:ccp:auto-prazo-maximo-art354-2@v1 | ccp:art354.2 | proposed (não tipável: nao_e_prazo_maximo) | não | ok | ok |
| regra:ccp:auto-prazo-maximo-art358-2-v20080730@v1 | ccp:art358.2 | settled (não tipável: nao_e_prazo_maximo) | sim | ok | ok |
| regra:ccp:auto-prazo-maximo-art359-1@v1 | ccp:art359.1 | settled (não tipável: nao_e_prazo_maximo) | sim | ok | ok |
| regra:ccp:auto-prazo-maximo-art366-1@v1 | ccp:art366.1 | settled (não tipável: nao_e_prazo_maximo) | sim | ok | ok |
| regra:ccp:auto-prazo-maximo-art366-6@v1 | ccp:art366.6 | settled (não tipável: nao_e_prazo_maximo) | sim | ok | ok |
| regra:ccp:auto-prazo-maximo-art372-1-v20080730@v1 | ccp:art372.1 | proposed (não tipável: nao_e_prazo_maximo) | não | ok | ok |
| regra:ccp:auto-prazo-maximo-art372-1-v20180101@v1 | ccp:art372.1 | proposed (não tipável: nao_e_prazo_maximo) | não | ok | ok |
| regra:ccp:auto-prazo-maximo-art372-1-v20210620@v1 | ccp:art372.1 | proposed (não tipável: nao_e_prazo_maximo) | não | ok | ok |
| regra:ccp:auto-prazo-maximo-art372-1@v1 | ccp:art372.1 | proposed (não tipável: nao_e_prazo_maximo) | não | ok | ok |
| regra:ccp:auto-prazo-maximo-art372-2@v1 | ccp:art372.2 | settled (não tipável: nao_e_prazo_maximo) | sim | ok | ok |
| regra:ccp:auto-prazo-maximo-art373-v20210620@v1 | ccp:art373 | proposed (não tipável: nao_e_prazo_maximo) | — | ok | não tipável: fonte em ccp:art373.2, que é vizinho (L1) |
| regra:ccp:auto-prazo-maximo-art373-2-v20080730@v1 | ccp:art373.2 | sem leitura válida de leitor:a17 | — | regra 1: deadline_field prazo_propostas_dias e as fontes dizem nada (L9) | ok |
| regra:ccp:auto-prazo-maximo-art373-2-v20091007@v1 | ccp:art373.2 | proposed (não tipável: nao_e_prazo_maximo) | não | ok | ok |
| regra:ccp:auto-prazo-maximo-art373-2@v1 | ccp:art373.2 | proposed (não tipável: nao_e_prazo_maximo) | não | ok | ok |
| regra:ccp:auto-prazo-maximo-art373-3@v1 | ccp:art373.3 | proposed (não tipável: nao_e_prazo_maximo) | não | ok | ok |
| regra:ccp:auto-prazo-maximo-art376-6-v20080730@v1 | ccp:art376.6 | settled (não tipável: nao_e_prazo_maximo) | sim | ok | ok |
| regra:ccp:auto-prazo-maximo-art376-7-v20120811@v1 | ccp:art376.7 | settled (não tipável: nao_e_prazo_maximo) | sim | ok | ok |
| regra:ccp:auto-prazo-maximo-art378-3-v20180101@v1 | ccp:art378.3 | proposed (não tipável: nao_e_prazo_maximo) | não | ok | ok |
| regra:ccp:auto-prazo-maximo-art378-4-v20080730@v1 | ccp:art378.4 | settled (não tipável: nao_e_prazo_maximo) | sim | ok | ok |
| regra:ccp:auto-prazo-maximo-art378-4-v20120811@v1 | ccp:art378.4 | settled (não tipável: nao_e_prazo_maximo) | sim | ok | ok |
| regra:ccp:auto-prazo-maximo-art378-4-v20180101@v1 | ccp:art378.4 | settled (não tipável: nao_e_prazo_maximo) | sim | ok | ok |
| regra:ccp:auto-prazo-maximo-art378-4@v1 | ccp:art378.4 | proposed (não tipável: nao_e_prazo_maximo) | não | ok | ok |
| regra:ccp:auto-prazo-maximo-art378-5@v1 | ccp:art378.5 | settled (não tipável: nao_e_prazo_maximo) | sim | ok | ok |
| regra:ccp:auto-prazo-maximo-art385-v20230715@v1 | ccp:art385 | proposed (não tipável: nao_e_prazo_maximo) | — | ok | não tipável: fonte em ccp:art385.3, que é vizinho (L1) |
| regra:ccp:auto-prazo-maximo-art385-3-v20080730@v1 | ccp:art385.3 | settled (não tipável: nao_e_prazo_maximo) | sim | ok | ok |
| regra:ccp:auto-prazo-maximo-art385-3@v1 | ccp:art385.3 | settled (não tipável: nao_e_prazo_maximo) | sim | ok | ok |
| regra:ccp:auto-prazo-maximo-art386-2@v1 | ccp:art386.2 | settled (não tipável: nao_e_prazo_maximo) | sim | ok | ok |
| regra:ccp:auto-prazo-maximo-art389-1@v1 | ccp:art389.1 | settled (não tipável: nao_e_prazo_maximo) | sim | ok | ok |
| regra:ccp:auto-prazo-maximo-art394-5@v1 | ccp:art394.5 | settled (não tipável: nao_e_prazo_maximo) | sim | ok | ok |
| regra:ccp:auto-prazo-maximo-art401-1@v1 | ccp:art401.1 | proposed (não tipável: nao_e_prazo_maximo) | não | ok | ok |
| regra:ccp:auto-prazo-maximo-art401-3@v1 | ccp:art401.3 | settled (não tipável: nao_e_prazo_maximo) | sim | ok | ok |
| regra:ccp:auto-prazo-maximo-art402-1@v1 | ccp:art402.1 | settled (não tipável: nao_e_prazo_maximo) | sim | ok | ok |
| regra:ccp:auto-prazo-maximo-art404-1@v1 | ccp:art404.1 | proposed (não tipável: nao_e_prazo_maximo) | não | ok | ok |
| regra:ccp:auto-prazo-maximo-art405-v20080730@v1 | ccp:art405 | proposed (não tipável: nao_e_prazo_maximo) | — | ok | não tipável: fonte em ccp:art405.1, que é vizinho (L1) |
| regra:ccp:auto-prazo-maximo-art405-v20210620@v1 | ccp:art405 | proposed (não tipável: nao_e_prazo_maximo) | — | ok | não tipável: fonte em ccp:art405.1.d, que é vizinho (L1) |
| regra:ccp:auto-prazo-maximo-art405-1-d@v1 | ccp:art405.1.d | settled (não tipável: nao_e_prazo_maximo) | sim | ok | ok |
| regra:ccp:auto-prazo-maximo-art405-2@v1 | ccp:art405.2 | settled (não tipável: nao_e_prazo_maximo) | sim | ok | ok |
| regra:ccp:auto-prazo-maximo-art406-b@v1 | ccp:art406.b | settled (não tipável: nao_e_prazo_maximo) | sim | ok | ok |
| regra:ccp:auto-prazo-maximo-art464-a-v20210620@v1 | ccp:art464-a | proposed (não tipável: nao_e_prazo_maximo) | — | ok | não tipável: fonte em ccp:art464-a.1, que é vizinho (L1) |
| regra:ccp:auto-prazo-maximo-art464-a-2-v20180101@v1 | ccp:art464-a.2 | settled (não tipável: nao_e_prazo_maximo) | sim | ok | ok |
| regra:ccp:auto-prazo-maximo-art464-e-2@v1 | ccp:art464-e.2 | proposed (não tipável: nao_e_prazo_maximo) | não | ok | ok |
| regra:ccp:auto-prazo-maximo-art464-e-3@v1 | ccp:art464-e.3 | settled (não tipável: nao_e_prazo_maximo) | sim | ok | ok |
| regra:ccp:auto-prazo-maximo-art464-g@v1 | ccp:art464-g | settled (não tipável: nao_e_prazo_maximo) | sim | ok | ok |
| regra:eu-1989-665:auto-prazo-minimo-art1-5@v1 | eu-1989-665:art1.5 | settled (não tipável: nao_e_prazo_minimo) | sim | ok | ok |
| regra:eu-1989-665:auto-prazo-minimo-art2-a-2@v1 | eu-1989-665:art2-a.2 | proposed (não tipável: sem_vocabulario) | não | ok | ok |
| regra:eu-1989-665:auto-prazo-minimo-art2-c@v1 | eu-1989-665:art2-c | proposed (não tipável: sem_vocabulario) | — | ok | não tipável: «Prazos para interposição de recurso» não está em eu-1989-665:art2-c |
| regra:eu-1989-665:auto-prazo-minimo-art2-d-5@v1 | eu-1989-665:art2-d.5 | settled (não tipável: nao_e_prazo_minimo) | sim | ok | ok |
| regra:eu-1989-665:auto-prazo-maximo-art3-3@v1 | eu-1989-665:art3.3 | settled (não tipável: nao_e_prazo_maximo) | sim | ok | ok |
| regra:eu-1992-13:auto-prazo-minimo-art1-5@v1 | eu-1992-13:art1.5 | settled (não tipável: nao_e_prazo_minimo) | sim | ok | ok |
| regra:eu-1992-13:auto-prazo-minimo-art2-a-2@v1 | eu-1992-13:art2-a.2 | settled (não tipável: nao_e_prazo_minimo) | sim | ok | ok |
| regra:eu-1992-13:auto-prazo-minimo-art2-c@v1 | eu-1992-13:art2-c | proposed (não tipável: sem_vocabulario) | — | ok | não tipável: «Prazos para interposição de recurso» não está em eu-1992-13:art2-c |
| regra:eu-1992-13:auto-prazo-minimo-art2-d-4@v1 | eu-1992-13:art2-d.4 | settled (não tipável: nao_e_prazo_minimo) | sim | ok | ok |
| regra:eu-1992-13:auto-prazo-minimo-art2-d-5@v1 | eu-1992-13:art2-d.5 | settled (não tipável: nao_e_prazo_minimo) | sim | ok | ok |
| regra:eu-1992-13:auto-prazo-maximo-art8-3@v1 | eu-1992-13:art8.3 | settled (não tipável: nao_e_prazo_maximo) | sim | ok | ok |
| regra:eu-2004-17:auto-prazo-maximo-art15-4-v20041101@v1 | eu-2004-17:art15.4 | proposed (não tipável: sem_vocabulario) | não | ok | ok |
| regra:eu-2004-17:auto-limiar-art16-a-v20160101@v1 | eu-2004-17:art16.a | settled (não tipável: nao_e_limiar) | sim | ok | ok |
| regra:eu-2004-17:auto-limiar-art16-b-v20160101@v1 | eu-2004-17:art16.b | settled (não tipável: nao_e_limiar) | sim | ok | ok |
| regra:eu-2004-17:auto-limiar-art41-1-a-v20041101@v1 | eu-2004-17:art41.1.a | settled (não tipável: nao_e_limiar) | sim | ok | ok |
| regra:eu-2004-17:auto-limiar-art41-1-b-v20041101@v1 | eu-2004-17:art41.1.b | settled (não tipável: nao_e_limiar) | sim | ok | ok |
| regra:eu-2004-17:auto-prazo-maximo-art44-3-v20041101@v1 | eu-2004-17:art44.3 | settled (não tipável: nao_e_prazo_maximo) | sim | ok | ok |
| regra:eu-2004-17:auto-prazo-minimo-art45-3-a-v20041101@v1 | eu-2004-17:art45.3.a | sem leitura válida de leitor:a17 | — | regra 1, tipo_procedimento in ['concurso_limitado_previa_qualificacao', 'procedimento_negociacao_com_concurso']: as font | ok |
| regra:eu-2004-17:auto-prazo-minimo-art45-3-c-v20041101@v1 | eu-2004-17:art45.3.c | sem leitura válida de leitor:a17 | — | regra 1, tipo_procedimento in ['concurso_limitado_previa_qualificacao', 'procedimento_negociacao_com_concurso']: as font | ok |
| regra:eu-2004-17:auto-prazo-minimo-art45-4-v20041101@v1 | eu-2004-17:art45.4 | proposed | não | ok | ok |
| regra:eu-2004-17:auto-prazo-maximo-art45-5-v20041101@v1 | eu-2004-17:art45.5 | sem leitura válida de leitor:a17 | — | regra 1, tipo_procedimento in ['concurso_limitado_previa_qualificacao', 'procedimento_negociacao', 'concurso_publico']:  | ok |
| regra:eu-2004-17:auto-prazo-minimo-art45-7-v20041101@v1 | eu-2004-17:art45.7 | proposed (não tipável: nao_e_prazo_minimo) | não | ok | ok |
| regra:eu-2004-17:auto-prazo-minimo-art45-8-v20041101@v1 | eu-2004-17:art45.8 | proposed (não tipável: nao_e_prazo_minimo) | não | ok | ok |
| regra:eu-2004-17:auto-prazo-maximo-art46-1-v20041101@v1 | eu-2004-17:art46.1 | settled (não tipável: nao_e_prazo_maximo) | sim | ok | ok |
| regra:eu-2004-17:auto-prazo-maximo-art49-4-v20041101@v1 | eu-2004-17:art49.4 | settled (não tipável: nao_e_prazo_maximo) | sim | ok | ok |
| regra:eu-2004-17:auto-prazo-minimo-art49-5-v20041101@v1 | eu-2004-17:art49.5 | settled (não tipável: nao_e_prazo_minimo) | sim | ok | ok |
| regra:eu-2004-17:auto-prazo-maximo-art56-4-v20041101@v1 | eu-2004-17:art56.4 | settled (não tipável: nao_e_prazo_maximo) | sim | ok | ok |
| regra:eu-2004-17:auto-limiar-art61-1-v20160101@v1 | eu-2004-17:art61.1 | settled (não tipável: nao_e_limiar) | sim | ok | ok |
| regra:eu-2004-17:auto-limiar-art61-2-v20160101@v1 | eu-2004-17:art61.2 | settled (não tipável: nao_e_limiar) | sim | ok | ok |
| regra:eu-2004-17:auto-limiar-art69-1-v20090807@v1 | eu-2004-17:art69.1 | settled (não tipável: nao_e_limiar) | sim | ok | ok |
| regra:eu-2004-18:auto-limiar-art7-a-v20160101@v1 | eu-2004-18:art7.a | settled (não tipável: nao_e_limiar) | sim | ok | ok |
| regra:eu-2004-18:auto-limiar-art7-b-v20160101@v1 | eu-2004-18:art7.b | settled (não tipável: nao_e_limiar) | sim | ok | ok |
| regra:eu-2004-18:auto-limiar-art7-c-v20160101@v1 | eu-2004-18:art7.c | settled (não tipável: nao_e_limiar) | sim | ok | ok |
| regra:eu-2004-18:auto-limiar-art9-4-a-v20040430@v1 | eu-2004-18:art9.4.a | proposed (não tipável: sem_vocabulario) | não | ok | ok |
| regra:eu-2004-18:auto-limiar-art9-4-b-v20040430@v1 | eu-2004-18:art9.4.b | proposed (não tipável: sem_vocabulario) | não | ok | ok |
| regra:eu-2004-18:auto-limiar-art9-5-b-v20041101@v1 | eu-2004-18:art9.5.b | proposed (não tipável: sem_vocabulario) | não | ok | ok |
| regra:eu-2004-18:auto-prazo-maximo-art33-4-v20040430@v1 | eu-2004-18:art33.4 | proposed (não tipável: sem_vocabulario) | não | ok | ok |
| regra:eu-2004-18:auto-limiar-art35-1-a-v20040430@v1 | eu-2004-18:art35.1.a | proposed (não tipável: sem_vocabulario) | não | ok | ok |
| regra:eu-2004-18:auto-limiar-art35-1-b-v20040430@v1 | eu-2004-18:art35.1.b | settled (não tipável: nao_e_limiar) | sim | ok | ok |
| regra:eu-2004-18:auto-prazo-maximo-art36-3-v20040430@v1 | eu-2004-18:art36.3 | settled (não tipável: nao_e_prazo_maximo) | sim | ok | ok |
| regra:eu-2004-18:auto-prazo-minimo-art38-3-a-v20040430@v1 | eu-2004-18:art38.3.a | sem leitura válida de leitor:a17 | — | regra 1: deadline_field prazo_reclamacao_dias e as fontes dizem ['prazo_candidaturas_dias'] (L9) | ok |
| regra:eu-2004-18:auto-prazo-minimo-art38-4-v20040430@v1 | eu-2004-18:art38.4 | sem leitura válida de leitor:a17 | — | regra 2, tipo_procedimento in ['concurso_limitado_previa_qualificacao', 'dialogo_concorrencial', 'procedimento_concorren | ok |
| regra:eu-2004-18:auto-prazo-maximo-art38-5-v20040430@v1 | eu-2004-18:art38.5 | sem leitura válida de leitor:a17 | — | regra 1, tipo_procedimento in ['concurso_publico', 'dialogo_concorrencial', 'procedimento_negociacao_com_concurso']: as  | ok |
| regra:eu-2004-18:auto-prazo-maximo-art38-6-v20040430@v1 | eu-2004-18:art38.6 | settled (não tipável: nao_e_prazo_maximo) | sim | ok | ok |
| regra:eu-2004-18:auto-prazo-minimo-art38-8-a-v20040430@v1 | eu-2004-18:art38.8.a | sem leitura válida de leitor:a17 | — | regra 1: deadline_field prazo_reclamacao_dias e as fontes dizem ['prazo_candidaturas_dias'] (L9) | ok |
| regra:eu-2004-18:auto-prazo-minimo-art38-8-b-v20040430@v1 | eu-2004-18:art38.8.b | proposed (não tipável: nao_e_prazo_minimo) | não | ok | ok |
| regra:eu-2004-18:auto-prazo-maximo-art39-1-v20040430@v1 | eu-2004-18:art39.1 | settled (não tipável: nao_e_prazo_maximo) | sim | ok | ok |
| regra:eu-2004-18:auto-prazo-maximo-art39-2-v20040430@v1 | eu-2004-18:art39.2 | settled (não tipável: nao_e_prazo_maximo) | sim | ok | ok |
| regra:eu-2004-18:auto-prazo-maximo-art40-4-v20040430@v1 | eu-2004-18:art40.4 | settled (não tipável: nao_e_prazo_maximo) | sim | ok | ok |
| regra:eu-2004-18:auto-prazo-maximo-art41-2-v20040430@v1 | eu-2004-18:art41.2 | settled (não tipável: nao_e_prazo_maximo) | sim | ok | ok |
| regra:eu-2004-18:auto-prazo-maximo-art54-4-v20040430@v1 | eu-2004-18:art54.4 | settled (não tipável: nao_e_prazo_maximo) | sim | ok | ok |
| regra:eu-2004-18:auto-limiar-art56-v20160101@v1 | eu-2004-18:art56 | settled (não tipável: nao_e_limiar) | sim | ok | ok |
| regra:eu-2004-18:auto-prazo-minimo-art59-v20040430@v1 | eu-2004-18:art59 | proposed | não | ok | ok |
| regra:eu-2004-18:auto-limiar-art63-1-v20160101@v1 | eu-2004-18:art63.1 | settled (não tipável: nao_e_limiar) | sim | ok | ok |
| regra:eu-2004-18:auto-prazo-minimo-art65-v20040430@v1 | eu-2004-18:art65 | sem leitura válida de leitor:a17 | — | regra 1, tipo_procedimento in ['concurso_limitado_previa_qualificacao', 'concurso_publico', 'dialogo_concorrencial', 'pr | ok |
| regra:eu-2004-18:auto-limiar-art67-1-a-v20160101@v1 | eu-2004-18:art67.1.a | sem leitura válida de leitor:a17 | — | regra 1, tipo_contrato eq servicos: as fontes não nomeiam ['servicos'] | ok |
| regra:eu-2004-18:auto-limiar-art67-1-b-v20160101@v1 | eu-2004-18:art67.1.b | sem leitura válida de leitor:a17 | — | regra 1, tipo_procedimento eq concurso_ideias: as fontes não nomeiam ['concurso_ideias'] | ok |
| regra:eu-2004-18:auto-limiar-art67-1-c-v20160101@v1 | eu-2004-18:art67.1.c | settled (não tipável: nao_e_limiar) | sim | ok | ok |
| regra:eu-2004-18:auto-limiar-art78-1-v20090807@v1 | eu-2004-18:art78.1 | settled (não tipável: nao_e_limiar) | sim | ok | ok |
| regra:eu-2004-18:auto-limiar-art78-3-v20040430@v1 | eu-2004-18:art78.3 | settled (não tipável: nao_e_limiar) | sim | ok | ok |
| regra:eu-2009-81:auto-limiar-art8-a@v1 | eu-2009-81:art8.a | proposed (não tipável: sem_vocabulario) | não | ok | ok |
| regra:eu-2009-81:auto-limiar-art8-b@v1 | eu-2009-81:art8.b | proposed (não tipável: sem_vocabulario) | não | ok | ok |
| regra:eu-2009-81:auto-limiar-art9-4-a@v1 | eu-2009-81:art9.4.a | proposed (não tipável: sem_vocabulario) | não | ok | ok |
| regra:eu-2009-81:auto-limiar-art9-4-b@v1 | eu-2009-81:art9.4.b | settled (não tipável: nao_e_limiar) | sim | ok | ok |
| regra:eu-2009-81:auto-limiar-art9-5-b-v20100101@v1 | eu-2009-81:art9.5.b | settled (não tipável: nao_e_limiar) | sim | ok | ok |
| regra:eu-2009-81:auto-prazo-maximo-art32-3@v1 | eu-2009-81:art32.3 | settled (não tipável: nao_e_prazo_maximo) | sim | ok | ok |
| regra:eu-2009-81:auto-prazo-minimo-art33-2@v1 | eu-2009-81:art33.2 | proposed (2 regras) | não | ok | ok |
| regra:eu-2009-81:auto-prazo-minimo-art33-3@v1 | eu-2009-81:art33.3 | sem leitura válida de leitor:a17 | — | regra 1, publicado_joue eq False: as fontes não negam o facto (L7) | ok |
| regra:eu-2009-81:auto-prazo-maximo-art33-4@v1 | eu-2009-81:art33.4 | settled (não tipável: nao_e_prazo_maximo) | sim | ok | ok |
| regra:eu-2009-81:auto-prazo-maximo-art33-5@v1 | eu-2009-81:art33.5 | settled (não tipável: nao_e_prazo_maximo) | sim | ok | ok |
| regra:eu-2009-81:auto-prazo-minimo-art33-7@v1 | eu-2009-81:art33.7 | settled (não tipável: sem_vocabulario) | sim | ok | ok |
| regra:eu-2009-81:auto-prazo-maximo-art34-4@v1 | eu-2009-81:art34.4 | settled (não tipável: nao_e_prazo_maximo) | sim | ok | ok |
| regra:eu-2009-81:auto-prazo-minimo-art57-2@v1 | eu-2009-81:art57.2 | settled (não tipável: nao_e_prazo_minimo) | sim | ok | ok |
| regra:eu-2009-81:auto-prazo-minimo-art59@v1 | eu-2009-81:art59 | proposed (não tipável: sem_vocabulario) | — | ok | não tipável: «Prazos para interposição de recurso» não está em eu-2009-81:art59 |
| regra:eu-2009-81:auto-prazo-minimo-art60-4@v1 | eu-2009-81:art60.4 | settled (não tipável: nao_e_prazo_minimo) | sim | ok | ok |
| regra:eu-2009-81:auto-prazo-minimo-art60-5@v1 | eu-2009-81:art60.5 | settled (não tipável: nao_e_prazo_minimo) | sim | ok | ok |
| regra:eu-2009-81:auto-prazo-maximo-art63-3@v1 | eu-2009-81:art63.3 | settled (não tipável: nao_e_prazo_maximo) | sim | ok | ok |
| regra:eu-2014-23:auto-limiar-art8-1@v1 | eu-2014-23:art8.1 | settled (não tipável: nao_e_limiar) | sim | ok | ok |
| regra:eu-2014-23:auto-limiar-art9-1@v1 | eu-2014-23:art9.1 | settled (não tipável: nao_e_limiar) | sim | ok | ok |
| regra:eu-2014-23:auto-limiar-art9-2@v1 | eu-2014-23:art9.2 | settled (não tipável: nao_e_limiar) | sim | ok | ok |
| regra:eu-2014-23:auto-prazo-maximo-art32-1@v1 | eu-2014-23:art32.1 | settled (não tipável: nao_e_prazo_maximo) | sim | ok | ok |
| regra:eu-2014-23:auto-prazo-maximo-art33-2@v1 | eu-2014-23:art33.2 | sem leitura válida de leitor:a17 | — | regra 1: deadline_field prazo_propostas_dias e as fontes dizem nada (L9) | ok |
| regra:eu-2014-23:auto-prazo-minimo-art39-3@v1 | eu-2014-23:art39.3 | sem leitura válida de leitor:a17 | — | regra 1, tipo_contrato eq concessao_obras: as fontes não nomeiam ['concessao_obras'] | ok |
| regra:eu-2014-23:auto-prazo-minimo-art39-4@v1 | eu-2014-23:art39.4 | sem leitura válida de leitor:a17 | — | regra 1, tipo_contrato eq concessao_obras: as fontes não nomeiam ['concessao_obras'] | ok |
| regra:eu-2014-23:auto-prazo-maximo-art39-5@v1 | eu-2014-23:art39.5 | settled (não tipável: nao_e_prazo_maximo) | sim | ok | ok |
| regra:eu-2014-23:auto-prazo-maximo-art40-1@v1 | eu-2014-23:art40.1 | settled (não tipável: nao_e_prazo_maximo) | sim | ok | ok |
| regra:eu-2014-24:auto-limiar-art4-a@v1 | eu-2014-24:art4.a | settled (não tipável: nao_e_limiar) | sim | ok | ok |
| regra:eu-2014-24:auto-limiar-art4-b@v1 | eu-2014-24:art4.b | settled (não tipável: nao_e_limiar) | sim | ok | ok |
| regra:eu-2014-24:auto-limiar-art4-c@v1 | eu-2014-24:art4.c | settled (não tipável: nao_e_limiar) | sim | ok | ok |
| regra:eu-2014-24:auto-limiar-art4-d@v1 | eu-2014-24:art4.d | settled (não tipável: nao_e_limiar) | sim | ok | ok |
| regra:eu-2014-24:auto-limiar-art5-10@v1 | eu-2014-24:art5.10 | settled (não tipável: nao_e_limiar) | sim | ok | ok |
| regra:eu-2014-24:auto-limiar-art6-1@v1 | eu-2014-24:art6.1 | settled (não tipável: nao_e_limiar) | sim | ok | ok |
| regra:eu-2014-24:auto-limiar-art6-3@v1 | eu-2014-24:art6.3 | settled (não tipável: nao_e_limiar) | sim | ok | ok |
| regra:eu-2014-24:auto-limiar-art13-a@v1 | eu-2014-24:art13.a | settled (não tipável: nao_e_limiar) | sim | ok | ok |
| regra:eu-2014-24:auto-prazo-minimo-art27-2-b@v1 | eu-2014-24:art27.2.b | sem leitura válida de leitor:a17 | — | regra 1, publicado_joue eq True: as fontes não afirmam o facto (L7) | ok |
| regra:eu-2014-24:auto-prazo-minimo-art27-3@v1 | eu-2014-24:art27.3 | proposed | não | ok | ok |
| regra:eu-2014-24:auto-prazo-maximo-art27-4@v1 | eu-2014-24:art27.4 | settled (não tipável: nao_e_prazo_maximo) | sim | ok | ok |
| regra:eu-2014-24:auto-prazo-minimo-art28-1@v1 | eu-2014-24:art28.1 | proposed | não | ok | ok |
| regra:eu-2014-24:auto-prazo-minimo-art28-2@v1 | eu-2014-24:art28.2 | sem leitura válida de leitor:a17 | — | regra 1, tipo_procedimento eq concurso_limitado_previa_qualificacao: as fontes não nomeiam ['concurso_limitado_previa_qu | ok |
| regra:eu-2014-24:auto-prazo-minimo-art28-3-b@v1 | eu-2014-24:art28.3.b | proposed (não tipável: nao_e_prazo_minimo) | não | ok | ok |
| regra:eu-2014-24:auto-prazo-minimo-art28-4@v1 | eu-2014-24:art28.4 | sem leitura válida de leitor:a17 | — | regra 1, tipo_procedimento eq concurso_limitado_previa_qualificacao: as fontes não nomeiam ['concurso_limitado_previa_qu | ok |
| regra:eu-2014-24:auto-prazo-maximo-art28-5@v1 | eu-2014-24:art28.5 | settled (não tipável: nao_e_prazo_maximo) | sim | ok | ok |
| regra:eu-2014-24:auto-prazo-minimo-art28-6-a@v1 | eu-2014-24:art28.6.a | sem leitura válida de leitor:a17 | — | regra 1, tipo_procedimento eq concurso_limitado_previa_qualificacao: as fontes não nomeiam ['concurso_limitado_previa_qu | ok |
| regra:eu-2014-24:auto-prazo-minimo-art28-6-b@v1 | eu-2014-24:art28.6.b | sem leitura válida de leitor:a17 | — | regra 1, tipo_procedimento eq concurso_limitado_previa_qualificacao: as fontes não nomeiam ['concurso_limitado_previa_qu | ok |
| regra:eu-2014-24:auto-prazo-minimo-art29-1@v1 | eu-2014-24:art29.1 | proposed | não | ok | ok |
| regra:eu-2014-24:auto-prazo-minimo-art30-1@v1 | eu-2014-24:art30.1 | sem leitura válida de leitor:a17 | — | regra 1, tipo_procedimento eq dialogo_concorrencial: as fontes não nomeiam ['dialogo_concorrencial'] | regra 1, tipo_procedimento eq dialogo_concorrencial: as fontes não nomeiam ['dialogo_concorrencial'] |
| regra:eu-2014-24:auto-prazo-minimo-art31-1@v1 | eu-2014-24:art31.1 | settled | sim | ok | ok |
| regra:eu-2014-24:auto-prazo-maximo-art34-5@v1 | eu-2014-24:art34.5 | proposed (não tipável: sem_vocabulario) | não | ok | ok |
| regra:eu-2014-24:auto-prazo-minimo-art47-3-a@v1 | eu-2014-24:art47.3.a | settled (não tipável: nao_e_prazo_minimo) | sim | ok | ok |
| regra:eu-2014-24:auto-prazo-maximo-art48-2-d@v1 | eu-2014-24:art48.2.d | settled (não tipável: nao_e_prazo_maximo) | sim | ok | ok |
| regra:eu-2014-24:auto-prazo-maximo-art50-1@v1 | eu-2014-24:art50.1 | settled (não tipável: nao_e_prazo_maximo) | sim | ok | ok |
| regra:eu-2014-24:auto-prazo-maximo-art50-2@v1 | eu-2014-24:art50.2 | settled (não tipável: nao_e_prazo_maximo) | sim | ok | ok |
| regra:eu-2014-24:auto-prazo-maximo-art50-3@v1 | eu-2014-24:art50.3 | proposed (não tipável: sem_vocabulario) | não | ok | ok |
| regra:eu-2014-24:auto-prazo-maximo-art51-2@v1 | eu-2014-24:art51.2 | settled (não tipável: nao_e_prazo_maximo) | sim | ok | ok |
| regra:eu-2014-24:auto-prazo-maximo-art53-1@v1 | eu-2014-24:art53.1 | settled (não tipável: nao_e_prazo_maximo) | sim | ok | ok |
| regra:eu-2014-24:auto-prazo-maximo-art53-2@v1 | eu-2014-24:art53.2 | settled (não tipável: nao_e_prazo_maximo) | sim | ok | ok |
| regra:eu-2014-24:auto-prazo-maximo-art55-2@v1 | eu-2014-24:art55.2 | settled (não tipável: nao_e_prazo_maximo) | sim | ok | ok |
| regra:eu-2014-25:auto-limiar-art15-a@v1 | eu-2014-25:art15.a | settled (não tipável: nao_e_limiar) | sim | ok | ok |
| regra:eu-2014-25:auto-limiar-art15-b@v1 | eu-2014-25:art15.b | sem leitura válida de leitor:a17 | — | regra 1, tipo_procedimento in ['concurso_concecao']: as fontes não nomeiam ['concurso_concecao'] | ok |
| regra:eu-2014-25:auto-limiar-art15-c@v1 | eu-2014-25:art15.c | settled (não tipável: nao_e_limiar) | sim | ok | ok |
| regra:eu-2014-25:auto-limiar-art16-10@v1 | eu-2014-25:art16.10 | settled (não tipável: nao_e_limiar) | sim | ok | ok |
| regra:eu-2014-25:auto-limiar-art17-1@v1 | eu-2014-25:art17.1 | settled (não tipável: nao_e_limiar) | sim | ok | ok |
| regra:eu-2014-25:auto-limiar-art17-2@v1 | eu-2014-25:art17.2 | settled (não tipável: nao_e_limiar) | sim | ok | ok |
| regra:eu-2014-25:auto-prazo-minimo-art45-1@v1 | eu-2014-25:art45.1 | settled | sim | ok | ok |
| regra:eu-2014-25:auto-prazo-minimo-art45-2-b@v1 | eu-2014-25:art45.2.b | settled (não tipável: nao_e_prazo_minimo) | sim | ok | ok |
| regra:eu-2014-25:auto-prazo-minimo-art45-3@v1 | eu-2014-25:art45.3 | proposed | não | ok | ok |
| regra:eu-2014-25:auto-prazo-maximo-art45-4@v1 | eu-2014-25:art45.4 | proposed (não tipável: nao_e_prazo_maximo) | — | ok | não tipável: fonte em eu-2014-25:art45.1, que é vizinho (L1) |
| regra:eu-2014-25:auto-prazo-minimo-art46-1@v1 | eu-2014-25:art46.1 | sem leitura válida de leitor:a17 | — | regra 1: usual_days sem «em regra» e os dias nas fontes (L11) | ok |
| regra:eu-2014-25:auto-prazo-minimo-art46-2@v1 | eu-2014-25:art46.2 | proposed (não tipável: nao_e_prazo_minimo) | não | ok | ok |
| regra:eu-2014-25:auto-prazo-minimo-art47-1@v1 | eu-2014-25:art47.1 | proposed (2 regras) | não | ok | ok |
| regra:eu-2014-25:auto-prazo-minimo-art47-2@v1 | eu-2014-25:art47.2 | proposed (não tipável: nao_e_prazo_minimo) | não | ok | ok |
| regra:eu-2014-25:auto-prazo-minimo-art48-1@v1 | eu-2014-25:art48.1 | sem leitura válida de leitor:a17 | — | regra 1, tipo_procedimento eq dialogo_concorrencial: as fontes não nomeiam ['dialogo_concorrencial'] | regra 1, tipo_procedimento eq dialogo_concorrencial: as fontes não nomeiam ['dialogo_concorrencial'] |
| regra:eu-2014-25:auto-prazo-minimo-art49-1@v1 | eu-2014-25:art49.1 | proposed | — | ok | regra 1: usual_days sem «em regra» e os dias nas fontes (L11) |
| regra:eu-2014-25:auto-prazo-maximo-art52-5@v1 | eu-2014-25:art52.5 | proposed (não tipável: sem_vocabulario) | não | ok | ok |
| regra:eu-2014-25:auto-prazo-minimo-art66-3-a@v1 | eu-2014-25:art66.3.a | settled (não tipável: nao_e_prazo_minimo) | sim | ok | ok |
| regra:eu-2014-25:auto-prazo-maximo-art67-2-d@v1 | eu-2014-25:art67.2.d | settled (não tipável: nao_e_prazo_maximo) | sim | ok | ok |
| regra:eu-2014-25:auto-prazo-maximo-art70-1@v1 | eu-2014-25:art70.1 | settled (não tipável: nao_e_prazo_maximo) | sim | ok | ok |
| regra:eu-2014-25:auto-prazo-maximo-art70-2@v1 | eu-2014-25:art70.2 | proposed (não tipável: sem_vocabulario) | não | ok | ok |
| regra:eu-2014-25:auto-prazo-maximo-art71-2@v1 | eu-2014-25:art71.2 | settled (não tipável: nao_e_prazo_maximo) | sim | ok | ok |
| regra:eu-2014-25:auto-prazo-maximo-art73-1@v1 | eu-2014-25:art73.1 | settled (não tipável: nao_e_prazo_maximo) | sim | ok | ok |
| regra:eu-2014-25:auto-prazo-maximo-art73-2@v1 | eu-2014-25:art73.2 | settled (não tipável: nao_e_prazo_maximo) | sim | ok | ok |
| regra:eu-2014-25:auto-prazo-maximo-art75-2@v1 | eu-2014-25:art75.2 | settled (não tipável: nao_e_prazo_maximo) | sim | ok | ok |
| regra:eu-2014-25:auto-prazo-maximo-art75-5@v1 | eu-2014-25:art75.5 | settled (não tipável: nao_e_prazo_maximo) | sim | ok | ok |
| regra:eu-2014-25:auto-prazo-minimo-art75-6@v1 | eu-2014-25:art75.6 | settled (não tipável: nao_e_prazo_minimo) | sim | ok | ok |
| regra:eu-2014-25:auto-prazo-maximo-art96-2@v1 | eu-2014-25:art96.2 | settled (não tipável: nao_e_prazo_maximo) | sim | ok | ok |

## regra:ccp:auto-prazo-maximo-art35-b-3@v1

- leitor:a17: não tipável (nao_e_prazo_maximo): O prazo é da própria entidade adjudicante para analisar a iniciativa, não um prazo máximo para os interessados apresentarem algo.
- leitor:b: não tipável (nao_e_prazo_maximo): O prazo é para a própria entidade adjudicante analisar a iniciativa espontânea.

## regra:ccp:auto-prazo-maximo-art43-v20180101@v1

- leitor:a17: não tipável (nao_e_prazo_maximo): O prazo é para incluir um projeto de execução, não um prazo máximo para os interessados.
- leitor:b: não tipável (nao_e_prazo_maximo): Os prazos de cinco dias destinam-se à própria entidade adjudicante ou ao contraente público para sanar a nulidade.
- verificador (B): não tipável: fonte em ccp:art43.10.a, que é vizinho (L1); não tipável: fonte em ccp:art43.10.b, que é vizinho (L1); não tipável: fonte em ccp:art43.10.c, que é vizinho (L1)

## regra:ccp:auto-prazo-maximo-art43-v20251028@v1

- leitor:a17: não tipável (nao_e_prazo_maximo): O prazo é para apresentar o projecto de execução, não um prazo máximo para os interessados.
- leitor:b: não tipável (nao_e_prazo_maximo): Os prazos de cinco dias são para a própria entidade adjudicante ou para o contraente público sanar a nulidade.
- verificador (B): não tipável: fonte em ccp:art43.10.a, que é vizinho (L1); não tipável: fonte em ccp:art43.10.b, que é vizinho (L1); não tipável: fonte em ccp:art43.10.c, que é vizinho (L1)

## regra:ccp:auto-prazo-maximo-art65@v1

- leitor:a17: não tipável (nao_e_prazo_maximo): O prazo é de manutenção das propostas já apresentadas, não um prazo para as apresentar.
- leitor:b: não tipável (nao_e_prazo_maximo): O prazo é para manter as propostas, não para apresentar algo.

## regra:ccp:auto-prazo-maximo-art72-v20180101@v1

- leitor:a17: não tipável (nao_e_prazo_maximo): O prazo é o máximo de cinco dias para suprir irregularidades, não um prazo para os concorrentes apresentarem algo.
- leitor:b: não tipável (sem_vocabulario): O vocabulário não prevê um campo de prazo para o suprimento de irregularidades das propostas e candidaturas.

## regra:ccp:auto-prazo-maximo-art72-v20221202@v1

- leitor:a17: não tipável (nao_e_prazo_maximo): O prazo é o máximo de cinco dias para suprir irregularidades, não um prazo para apresentar algo.
- leitor:b: não tipável (sem_vocabulario): O vocabulário não prevê um campo de prazo para o suprimento de irregularidades formais de candidaturas e propostas.

## regra:ccp:auto-prazo-maximo-art72-3@v1

- leitor:a17: não tipável (nao_e_prazo_maximo): O prazo é o máximo de cinco dias para suprir irregularidades, não um prazo para os concorrentes apresentarem algo.
- leitor:b: não tipável (sem_vocabulario): O vocabulário não contém um campo de prazo para o suprimento de irregularidades formais de candidaturas e propostas.

## regra:ccp:auto-prazo-maximo-art78-v20180101@v1

- leitor:a17: não tipável (nao_e_prazo_maximo): O prazo é da própria entidade adjudicante para publicar o anúncio da adjudicação, não um prazo máximo para os interessados apresentarem algo.
- leitor:b: não tipável (nao_e_prazo_maximo): Os prazos são para a publicação de anúncios pela entidade adjudicante, não para apresentar elementos.
- verificador (B): não tipável: fonte em ccp:art78.5, que é vizinho (L1)

## regra:ccp:auto-prazo-maximo-art78-1-v20080730@v1

- leitor:a17: não tipável (nao_e_prazo_maximo): O prazo é da própria entidade adjudicante para enviar o anúncio, não um prazo máximo para os interessados apresentarem algo.
- leitor:b: não tipável (nao_e_prazo_maximo): O prazo é para a própria entidade adjudicante enviar um anúncio de adjudicação.

## regra:ccp:auto-prazo-maximo-art78-1@v1

- leitor:a17: não tipável (nao_e_prazo_maximo): O prazo é da própria entidade adjudicante para publicar o anúncio da adjudicação, não um prazo máximo para os interessados apresentarem algo.
- leitor:b: não tipável (nao_e_prazo_maximo): O prazo é para a própria entidade adjudicante publicar um anúncio de adjudicação.

## regra:ccp:auto-prazo-maximo-art78-5@v1

- leitor:a17: não tipável (nao_e_prazo_maximo): O prazo é de 30 dias para a entidade adjudicante publicar os anúncios, não um prazo máximo para os interessados apresentarem algo.
- leitor:b: não tipável (nao_e_prazo_maximo): O prazo destina-se à publicação do anúncio pela entidade adjudicante, não à apresentação de elementos pelos interessados.

## regra:ccp:auto-prazo-maximo-art85-2@v1

- leitor:a17: não tipável (nao_e_prazo_maximo): O prazo é um máximo de prorrogação do próprio prazo, não um prazo para apresentar os documentos.
- leitor:b: não tipável (sem_vocabulario): O vocabulário não permite representar o máximo de cinco dias da prorrogação, distinto do prazo total para apresentar os documentos de habilitação.

## regra:ccp:auto-prazo-maximo-art86-v20120811@v1

- leitor:a17: não tipável (nao_e_prazo_maximo): O prazo é um máximo de 15 dias para o próprio órgão da entidade adjudicante notificar o adjudicatário, não um prazo para os interessados apresentarem algo.
- leitor:b: não tipável (sem_vocabulario): O vocabulário não permite representar a condição de ocorrência de um facto que determine a caducidade da adjudicação nos termos do n.º 1.
- verificador (B): não tipável: fonte em ccp:art86.2, que é vizinho (L1)

## regra:ccp:auto-prazo-maximo-art86-2-v20091007@v1

- leitor:a17: não tipável (nao_e_prazo_maximo): O prazo é um máximo da entidade adjudicante para notificar o adjudicatário, não um prazo para os interessados apresentarem algo.
- leitor:b: não tipável (sem_vocabulario): O vocabulário não permite representar a condição de ocorrência de um facto que determine a caducidade da adjudicação nos termos do n.º 1.

## regra:ccp:auto-prazo-maximo-art86-3@v1

- leitor:a17: não tipável (nao_e_prazo_maximo): O prazo é um máximo da própria entidade adjudicante para notificar, não um prazo para o adjudicatário apresentar algo.
- leitor:b: não tipável (sem_vocabulario): Falta no vocabulário uma condição que represente a ocorrência de um facto que determine a caducidade da adjudicação nos termos do n.º 2.

## regra:ccp:auto-prazo-maximo-art87-a-2@v1

- leitor:a17: não tipável (nao_e_prazo_maximo): O prazo é de cinco dias, máximo do órgão competente para decidir contratar, antes de se pronunciar o adjudicatário, e não um prazo para apresentar algo.
- leitor:b: não tipável (sem_vocabulario): Falta um campo para representar a condição de caducidade da adjudicação fundada nas situações indicadas.

## regra:ccp:auto-prazo-maximo-art90-1@v1

- leitor:a17: não tipável (nao_e_prazo_maximo): O prazo é o da própria entidade adjudicante para prestar a caução, não um prazo máximo para o adjudicatário apresentar algo.
- leitor:b: {"tipo": "prazo_maximo", "condicoes": [], "params": {"maximum_days": 10, "deadline_field": "prazo_caucao_dias", "counted_from": "data_notificacao"}}

## regra:ccp:auto-prazo-maximo-art91-2@v1

- leitor:a17: não tipável (nao_e_prazo_maximo): O prazo é um máximo da própria entidade adjudicante para notificar o adjudicatário, não um prazo para os interessados apresentarem algo.
- leitor:b: não tipável (sem_vocabulario): O vocabulário não permite representar a condição de não prestação da caução pelo adjudicatário por facto que lhe seja imputável.

## regra:ccp:auto-prazo-maximo-art93-2@v1

- leitor:a17: não tipável (nao_e_prazo_maximo): O prazo é um máximo da entidade adjudicante para notificar, não um prazo para os adjudicatários apresentarem algo.
- leitor:b: não tipável (sem_vocabulario): Falta um campo que permita condicionar o prazo à não confirmação dos compromissos pelo adjudicatário no prazo fixado ou até ao termo da respetiva prorrogação.

## regra:ccp:auto-prazo-maximo-art95-v20080730@v1

- leitor:a17: não tipável (nao_e_prazo_maximo): O prazo é de 10 dias para não reduzir o contrato a escrito, não um prazo máximo para apresentar algo.
- leitor:b: não tipável (nao_e_prazo_maximo): O prazo máximo respeita ao fornecimento dos bens ou à prestação dos serviços, não à apresentação de elementos.
- verificador (B): não tipável: fonte em ccp:art95.1.c.i, que é vizinho (L1)

## regra:ccp:auto-limiar-art95-1-a@v1

- leitor:a17: não tipável (nao_e_limiar): O valor dispensa a redução do contrato a escrito; não é o limite até ao qual um procedimento pode ser escolhido.
- leitor:b: não tipável (nao_e_limiar): O valor dispensa a redução do contrato a escrito, não fixa um limite para a escolha de um procedimento.

## regra:ccp:auto-prazo-maximo-art95-1-c-i@v1

- leitor:a17: não tipável (nao_e_prazo_maximo): O prazo é um máximo de 20 dias para a prestação dos bens ou serviços, não um prazo para apresentar algo.
- leitor:b: não tipável (nao_e_prazo_maximo): O prazo é para o fornecimento dos bens ou a prestação dos serviços, não para apresentar algo.

## regra:ccp:auto-prazo-maximo-art95-3@v1

- leitor:a17: não tipável (nao_e_prazo_maximo): O prazo é de 10 dias antes de iniciar a execução do contrato, não um prazo para apresentar algo.
- leitor:b: não tipável (nao_e_prazo_maximo): A passagem fixa um prazo mínimo de espera para iniciar a execução do contrato, não um prazo máximo para apresentar algo.

## regra:ccp:auto-prazo-maximo-art101@v1

- leitor:a17: não tipável (nao_e_prazo_maximo): O prazo é o da aceitação do contrato, não um prazo para apresentar algo.
- leitor:b: {"tipo": "prazo_maximo", "condicoes": [{"field": "tipo_procedimento", "op": "not_in", "value": ["ajuste_direto", "consulta_previa"]}], "params": {"maximum_days": 5, "deadline_field": "prazo_reclamacao_dias", "counted_from": "data_notificacao"}} || {"tipo": "prazo_maximo", "condicoes": [{"field": "tipo_procedimento", "op": "in", "value": ["ajuste_direto", "consulta_previa"]}], "params": {"maximum_days": 2, "deadline_field": "prazo_reclamacao_dias", "counted_from": "data_notificacao"}}
- verificador (B): regra 1: as fontes de maximum_days não dizem um máximo («não pode ser superior a», «no prazo de», L8); regra 2: as fontes de maximum_days não dizem um máximo («não pode ser superior a», «no prazo de», L8)

## regra:ccp:auto-prazo-maximo-art102-v20080730@v1

- leitor:a17: não tipável (nao_e_prazo_maximo): O prazo é do próprio órgão que aprova a minuta do contrato para notificar, não um prazo máximo para os interessados apresentarem algo.
- leitor:b: não tipável (nao_e_prazo_maximo): O prazo é para a própria entidade adjudicante notificar a decisão sobre a reclamação.
- verificador (B): não tipável: fonte em ccp:art102.2, que é vizinho (L1)

## regra:ccp:auto-prazo-maximo-art102-2@v1

- leitor:a17: não tipável (nao_e_prazo_maximo): O prazo é do próprio órgão que aprova a minuta do contrato para notificar, não um prazo máximo para os interessados apresentarem algo.
- leitor:b: não tipável (nao_e_prazo_maximo): O prazo é para a própria entidade adjudicante notificar o adjudicatário da sua decisão.

## regra:ccp:auto-prazo-minimo-art104-v20080730@v1

- leitor:a17: não tipável (nao_e_prazo_minimo): O prazo é da própria entidade adjudicante para outorgar o contrato, não um prazo mínimo para os interessados apresentarem algo.
- leitor:b: não tipável (nao_e_prazo_minimo): Os prazos regulam a outorga do contrato e a sua comunicação pela entidade adjudicante, não a apresentação de elementos.
- verificador (B): não tipável: fonte em ccp:art104.1, que é vizinho (L1); não tipável: fonte em ccp:art104.1.a, que é vizinho (L1); não tipável: fonte em ccp:art104.3, que é vizinho (L1)

## regra:ccp:auto-prazo-maximo-art104-1-a@v1

- leitor:a17: não tipável (nao_e_prazo_maximo): O prazo é de 30 dias antes de outorgar o contrato, não um prazo para apresentar algo.
- leitor:b: não tipável (nao_e_prazo_maximo): A passagem fixa um período mínimo de espera para a outorga do contrato, não um prazo máximo para apresentar algo.

## regra:ccp:auto-prazo-maximo-art108-1-v20080730@v1

- leitor:a17: não tipável (nao_e_prazo_maximo): O prazo é da própria entidade adjudicante para enviar o relatório, não um prazo máximo para os interessados apresentarem algo.
- leitor:b: não tipável (nao_e_prazo_maximo): O prazo é para a própria entidade adjudicante enviar o relatório de contratação.

## regra:ccp:auto-prazo-maximo-art115-1-j-v20180101@v1

- leitor:a17: não tipável (nao_e_prazo_maximo): O prazo é o máximo de cinco dias para a apresentação dos documentos de habilitação, não um prazo para apresentar alguma coisa.
- leitor:b: {"tipo": "prazo_maximo", "condicoes": [{"field": "tipo_procedimento", "op": "in", "value": ["ajuste_direto", "consulta_previa"]}], "params": {"maximum_days": 5, "deadline_field": "prazo_habilitacao_dias", "counted_from": "nao_indicado"}}

## regra:ccp:auto-prazo-maximo-art115-1-k@v1

- leitor:a17: não tipável (nao_e_prazo_maximo): O prazo é o máximo de habilitação, não um prazo para apresentar algo.
- leitor:b: {"tipo": "prazo_maximo", "condicoes": [{"field": "tipo_procedimento", "op": "in", "value": ["ajuste_direto", "consulta_previa"]}], "params": {"maximum_days": 5, "deadline_field": "prazo_habilitacao_dias", "counted_from": "nao_indicado"}}

## regra:ccp:auto-prazo-maximo-art122-v20180101@v1

- leitor:a17: não tipável (nao_e_prazo_maximo): O prazo é do próprio júri para elaborar o relatório preliminar, não um prazo máximo para os concorrentes apresentarem algo.
- leitor:b: não tipável (nao_e_prazo_maximo): O prazo destina-se à elaboração do relatório preliminar pelo júri, não à apresentação de elementos pelos interessados.
- verificador (B): não tipável: fonte em ccp:art122.1, que é vizinho (L1)

## regra:ccp:auto-prazo-maximo-art122-1@v1

- leitor:a17: não tipável (nao_e_prazo_maximo): O prazo é do próprio júri para elaborar o relatório preliminar, não um prazo máximo para os concorrentes apresentarem algo.
- leitor:b: não tipável (nao_e_prazo_maximo): O prazo destina-se à elaboração do relatório preliminar pelo júri, não à apresentação de elementos pelos interessados.

## regra:ccp:auto-prazo-minimo-art135-2-v20080730@v1

- leitor:a17: {"tipo": "prazo_minimo", "condicoes": [{"field": "publicado_joue", "op": "eq", "value": false}, {"field": "tipo_contrato", "op": "eq", "value": "obras"}, {"field": "tipo_procedimento", "op": "eq", "value": "concurso_publico"}], "params": {"minimum_days": 19, "deadline_field": "prazo_propostas_dias", "counted_from": "data_envio_anuncio", "usual_days": null}} || {"tipo": "prazo_minimo", "condicoes": [{"field": "publicado_joue", "op": "eq", "value": false}, {"field": "tipo_contrato", "op": "ne", "value": "obras"}, {"field": "tipo_procedimento", "op": "eq", "value": "concurso_publico"}], "params": {"minimum_days": 20, "deadline_field": "prazo_propostas_dias", "counted_from": "data_envio_anuncio", "usual_days": null}}
- leitor:b: não tipável (sem_vocabulario): Falta no vocabulário uma condição para a manifesta simplicidade dos trabalhos necessários à realização da obra.
- verificador (A): regra 1: minimum_days 19 não está nas fontes (L8, L4); regra 1: counted_from data_envio_anuncio e as fontes dizem nada (L9); regra 2: counted_from data_envio_anuncio e as fontes dizem nada (L9)

## regra:ccp:auto-prazo-minimo-art136-1-v20080730@v1

- leitor:a17: {"tipo": "prazo_minimo", "condicoes": [{"field": "publicado_joue", "op": "eq", "value": true}, {"field": "tipo_procedimento", "op": "eq", "value": "concurso_publico"}], "params": {"minimum_days": 47, "deadline_field": "prazo_propostas_dias", "counted_from": "data_envio_anuncio", "usual_days": null}}
- leitor:b: {"tipo": "prazo_minimo", "condicoes": [{"field": "publicado_joue", "op": "eq", "value": true}, {"field": "tipo_procedimento", "op": "eq", "value": "concurso_publico"}], "params": {"minimum_days": 47, "deadline_field": "prazo_propostas_dias", "counted_from": "data_envio_anuncio", "usual_days": null}}
- verificador (A): regra 1, publicado_joue eq True: as fontes não afirmam o facto (L7)

## regra:ccp:auto-prazo-minimo-art136-3-v20080730@v1

- leitor:a17: {"tipo": "prazo_minimo", "condicoes": [{"field": "publicado_joue", "op": "eq", "value": true}, {"field": "tipo_procedimento", "op": "eq", "value": "concurso_publico"}], "params": {"minimum_days": 7, "deadline_field": "prazo_propostas_dias", "counted_from": "data_envio_anuncio", "usual_days": null}}
- leitor:b: não tipável (sem_vocabulario): O vocabulário não permite representar a condição de preparação e envio do anúncio por meios electrónicos conforme o formato e as modalidades de transmissão indicados.

## regra:ccp:auto-prazo-minimo-art136-4-v20080730@v1

- leitor:a17: {"tipo": "prazo_minimo", "condicoes": [{"field": "setores_especiais", "op": "eq", "value": true}, {"field": "tipo_procedimento", "op": "eq", "value": "concurso_publico"}], "params": {"minimum_days": 22, "deadline_field": "prazo_propostas_dias", "counted_from": "data_envio_anuncio", "usual_days": null}}
- leitor:b: não tipável (sem_vocabulario): O vocabulário não permite representar a condição de preparação e envio do anúncio por meios electrónicos conforme o formato e as modalidades exigidos.
- verificador (A): regra 1: counted_from data_envio_anuncio e as fontes dizem nada (L9)

## regra:ccp:auto-prazo-maximo-art138-3@v1

- leitor:a17: não tipável (nao_e_prazo_maximo): O prazo é da própria entidade adjudicante para reclamar, não um prazo máximo para os concorrentes apresentarem algo.
- leitor:b: não tipável (sem_vocabulario): O vocabulário não prevê a condição de o interessado não ter sido incluído na lista dos concorrentes nem o início da contagem na publicitação dessa lista.

## regra:ccp:auto-limiar-art155-a@v1

- leitor:a17: {"tipo": "limiar", "condicoes": [{"field": "tipo_contrato", "op": "in", "value": ["bens", "obras", "servicos"]}, {"field": "tipo_procedimento", "op": "eq", "value": "concurso_publico"}], "params": {"threshold": {"field": "valor_estimado", "comparator": "le", "value": 300000, "currency": "EUR"}}}
- leitor:b: não tipável (texto_em_falta): Faltam os montantes dos limiares do artigo 474.º aplicáveis à locação ou aquisição de bens móveis e à aquisição de serviços.

## regra:ccp:auto-prazo-maximo-art159@v1

- leitor:a17: não tipável (nao_e_prazo_maximo): O prazo é de manutenção das propostas já apresentadas, não um prazo para as apresentar.
- leitor:b: não tipável (nao_e_prazo_maximo): O prazo refere-se à manutenção das propostas, não à apresentação de algo.

## regra:ccp:auto-prazo-maximo-art161@v1

- leitor:a17: {"tipo": "prazo_maximo", "condicoes": [{"field": "tipo_procedimento", "op": "eq", "value": "concurso_publico_urgente"}], "params": {"maximum_days": 2, "deadline_field": "prazo_habilitacao_dias", "counted_from": "data_notificacao"}}
- leitor:b: {"tipo": "prazo_maximo", "condicoes": [{"field": "tipo_procedimento", "op": "eq", "value": "concurso_publico_urgente"}], "params": {"maximum_days": 2, "deadline_field": "prazo_habilitacao_dias", "counted_from": "data_notificacao"}}

## regra:ccp:auto-prazo-maximo-art161-b-1-b@v1

- leitor:a17: não tipável (nao_e_prazo_maximo): O prazo é de três dias, o mínimo para a pronúncia dos concorrentes, e não um prazo máximo.
- leitor:b: não tipável (nao_e_prazo_maximo): A passagem autoriza a redução do prazo para três dias, mas não fixa um prazo máximo.

## regra:ccp:auto-prazo-maximo-art161-b-4@v1

- leitor:a17: não tipável (nao_e_prazo_maximo): O prazo é de três dias para impugnar, pronunciar-se e decidir, não um prazo máximo para os interessados apresentarem algo.
- leitor:b: não tipável (sem_vocabulario): O vocabulário não contém campos de prazo para apresentação de impugnações, pronúncia dos contrainteressados ou decisão de impugnações administrativas.

## regra:ccp:auto-prazo-minimo-art173@v1

- leitor:a17: {"tipo": "prazo_minimo", "condicoes": [{"field": "publicado_joue", "op": "eq", "value": false}, {"field": "tipo_procedimento", "op": "eq", "value": "concurso_limitado_previa_qualificacao"}], "params": {"minimum_days": 6, "deadline_field": "prazo_candidaturas_dias", "counted_from": "data_envio_anuncio", "usual_days": null}}
- leitor:b: {"tipo": "prazo_minimo", "condicoes": [{"field": "publicado_joue", "op": "eq", "value": false}, {"field": "tipo_procedimento", "op": "eq", "value": "concurso_limitado_previa_qualificacao"}], "params": {"minimum_days": 6, "deadline_field": "prazo_candidaturas_dias", "counted_from": "data_envio_anuncio", "usual_days": null}}
- verificador (A): regra 1: counted_from data_envio_anuncio e as fontes dizem nada (L9)

## regra:ccp:auto-prazo-minimo-art174-v20180101@v1

- leitor:a17: {"tipo": "prazo_minimo", "condicoes": [{"field": "publicado_joue", "op": "eq", "value": true}, {"field": "tipo_procedimento", "op": "eq", "value": "concurso_limitado_previa_qualificacao"}], "params": {"minimum_days": 30, "deadline_field": "prazo_candidaturas_dias", "counted_from": "data_envio_anuncio", "usual_days": null}} || {"tipo": "prazo_minimo", "condicoes": [{"field": "publicado_joue", "op": "eq", "value": true}, {"field": "setores_especiais", "op": "eq", "value": true}, {"field": "tipo_procedimento", "op": "eq", "value": "concurso_limitado_previa_qualificacao"}], "params": {"minimum_days": 15, "deadline_field": "prazo_candidaturas_dias", "counted_from": "data_envio_anuncio", "usual_days": null}}
- leitor:b: {"tipo": "prazo_minimo", "condicoes": [{"field": "publicado_joue", "op": "eq", "value": true}, {"field": "tipo_procedimento", "op": "eq", "value": "concurso_limitado_previa_qualificacao"}], "params": {"minimum_days": 30, "deadline_field": "prazo_candidaturas_dias", "counted_from": "data_envio_anuncio", "usual_days": null}} || {"tipo": "prazo_minimo", "condicoes": [{"field": "publicado_joue", "op": "eq", "value": true}, {"field": "tipo_procedimento", "op": "eq", "value": "concurso_limitado_previa_qualificacao"}, {"field": "urgencia_fundamentada", "op": "eq", "value": true}], "params": {"minimum_days": 15, "deadline_field": "prazo_candidaturas_dias", "counted_from": "data_envio_anuncio", "usual_days": null}} || {"tipo": "prazo_minimo", "condicoes": [{"field": "publicado_joue", "op": "eq", "value": true}, {"field": "setores_especiais", "op": "eq", "value": true}, {"field": "tipo_procedimento", "op": "eq", "value": "concurso_limitado_previa_qualificacao"}], "params": {"minimum_days": 15, "deadline_field": "prazo_candidaturas_dias", "counted_from": "data_envio_anuncio", "usual_days": 30}}
- verificador (B): regra 1, tipo_procedimento eq concurso_limitado_previa_qualificacao: fonte em ccp:art174.1, que é vizinho (L1); regra 1, publicado_joue eq True: fonte em ccp:art174.1, que é vizinho (L1); regra 1, minimum_days: fonte em ccp:art174.1, que é vizinho (L1); regra 1, deadline_field: fonte em ccp:art174.1, que é vizinho (L1); regra 1, counted_from: fonte em ccp:art174.1, que é vizinho (L1); regra 2, tipo_procedimento eq concurso_limitado_previa_qualificacao: fonte em ccp:art174.1, que é vizinho (L1)

## regra:ccp:auto-prazo-minimo-art174-1-v20080730@v1

- leitor:a17: {"tipo": "prazo_minimo", "condicoes": [{"field": "publicado_joue", "op": "eq", "value": true}, {"field": "tipo_contrato", "op": "ne", "value": "concessao_obras"}, {"field": "tipo_procedimento", "op": "eq", "value": "concurso_limitado_previa_qualificacao"}], "params": {"minimum_days": 37, "deadline_field": "prazo_candidaturas_dias", "counted_from": "data_envio_anuncio", "usual_days": null}} || {"tipo": "prazo_minimo", "condicoes": [{"field": "publicado_joue", "op": "eq", "value": true}, {"field": "tipo_contrato", "op": "eq", "value": "concessao_obras"}, {"field": "tipo_procedimento", "op": "eq", "value": "concurso_limitado_previa_qualificacao"}], "params": {"minimum_days": 52, "deadline_field": "prazo_candidaturas_dias", "counted_from": "data_envio_anuncio", "usual_days": null}}
- leitor:b: {"tipo": "prazo_minimo", "condicoes": [{"field": "publicado_joue", "op": "eq", "value": true}, {"field": "tipo_contrato", "op": "ne", "value": "concessao_obras"}, {"field": "tipo_procedimento", "op": "eq", "value": "concurso_limitado_previa_qualificacao"}], "params": {"minimum_days": 37, "deadline_field": "prazo_candidaturas_dias", "counted_from": "data_envio_anuncio", "usual_days": null}} || {"tipo": "prazo_minimo", "condicoes": [{"field": "publicado_joue", "op": "eq", "value": true}, {"field": "tipo_contrato", "op": "eq", "value": "concessao_obras"}, {"field": "tipo_procedimento", "op": "eq", "value": "concurso_limitado_previa_qualificacao"}], "params": {"minimum_days": 52, "deadline_field": "prazo_candidaturas_dias", "counted_from": "data_envio_anuncio", "usual_days": null}}
- verificador (A): regra 1, publicado_joue eq True: as fontes não afirmam o facto (L7); regra 2, publicado_joue eq True: as fontes não afirmam o facto (L7)

## regra:ccp:auto-prazo-minimo-art174-2-v20080730@v1

- leitor:a17: {"tipo": "prazo_minimo", "condicoes": [{"field": "anuncio_pre_informacao", "op": "eq", "value": true}, {"field": "tipo_procedimento", "op": "eq", "value": "concurso_limitado_previa_qualificacao"}], "params": {"minimum_days": 37, "deadline_field": "prazo_candidaturas_dias", "counted_from": "data_envio_convite", "usual_days": null}}
- leitor:b: {"tipo": "prazo_minimo", "condicoes": [{"field": "anuncio_pre_informacao", "op": "eq", "value": true}, {"field": "publicado_joue", "op": "eq", "value": true}, {"field": "tipo_procedimento", "op": "eq", "value": "concurso_limitado_previa_qualificacao"}], "params": {"minimum_days": 37, "deadline_field": "prazo_candidaturas_dias", "counted_from": "data_envio_convite", "usual_days": null}}
- verificador (A): regra 1: counted_from data_envio_convite e as fontes dizem nada (L9)

## regra:ccp:auto-prazo-minimo-art174-3-v20080730@v1

- leitor:a17: {"tipo": "prazo_minimo", "condicoes": [{"field": "publicado_joue", "op": "eq", "value": true}, {"field": "tipo_contrato", "op": "not_in", "value": ["concessao_obras", "concessao_servicos"]}, {"field": "tipo_procedimento", "op": "eq", "value": "concurso_limitado_previa_qualificacao"}], "params": {"minimum_days": 30, "deadline_field": "prazo_candidaturas_dias", "counted_from": "data_envio_anuncio", "usual_days": null}} || {"tipo": "prazo_minimo", "condicoes": [{"field": "publicado_joue", "op": "eq", "value": true}, {"field": "tipo_contrato", "op": "in", "value": ["concessao_obras", "concessao_servicos"]}, {"field": "tipo_procedimento", "op": "eq", "value": "concurso_limitado_previa_qualificacao"}], "params": {"minimum_days": 52, "deadline_field": "prazo_candidaturas_dias", "counted_from": "data_envio_anuncio", "usual_days": null}}
- leitor:b: não tipável (sem_vocabulario): O vocabulário não permite representar a condição relativa à preparação e ao envio dos anúncios por meios electrónicos no formato e nas modalidades indicados no portal referido.
- verificador (A): regra 1, tipo_contrato not_in ['concessao_obras', 'concessao_servicos']: as fontes não nomeiam ['concessao_servicos']; regra 2, tipo_contrato in ['concessao_obras', 'concessao_servicos']: as fontes não nomeiam ['concessao_servicos']

## regra:ccp:auto-prazo-minimo-art174-4@v1

- leitor:a17: não tipável (nao_e_prazo_minimo): O prazo é prorrogado em cinco dias; falta um prazo mínimo que se aplique sem redução.
- leitor:b: não tipável (sem_vocabulario): O vocabulário não permite representar a condição de as peças procedimentais não poderem ser disponibilizadas sem restrições de acesso.

## regra:ccp:auto-prazo-maximo-art177-3@v1

- leitor:a17: não tipável (nao_e_prazo_maximo): O prazo é da própria entidade adjudicante para publicitar a lista dos candidatos, não um prazo máximo para os interessados apresentarem algo.
- leitor:b: não tipável (sem_vocabulario): O vocabulário não prevê a condição de o interessado não ter sido incluído na lista dos candidatos nem a contagem desde a publicitação dessa lista.

## regra:ccp:auto-prazo-maximo-art187-1-v20080730@v1

- leitor:a17: não tipável (nao_e_prazo_maximo): O prazo é para tomar a decisão de qualificação, não para os candidatos apresentarem algo.
- leitor:b: não tipável (nao_e_prazo_maximo): O prazo é para a própria entidade adjudicante tomar e notificar a decisão de qualificação.

## regra:ccp:auto-prazo-maximo-art187-1-v20180101@v1

- leitor:a17: não tipável (nao_e_prazo_maximo): O prazo é o máximo do próprio órgão da entidade adjudicante para tomar a decisão de qualificação, não um prazo para os candidatos apresentarem algo.
- leitor:b: não tipável (nao_e_prazo_maximo): O prazo é para a própria entidade adjudicante tomar e notificar a decisão de qualificação.

## regra:ccp:auto-prazo-maximo-art187-1@v1

- leitor:a17: não tipável (nao_e_prazo_maximo): O prazo é o da própria entidade adjudicante para tomar a decisão de qualificação, não um prazo máximo para os candidatos apresentarem algo.
- leitor:b: não tipável (nao_e_prazo_maximo): O prazo é para a própria entidade adjudicante tomar e notificar a decisão de qualificação.

## regra:ccp:auto-prazo-minimo-art187-2-v20180101@v1

- leitor:a17: {"tipo": "prazo_minimo", "condicoes": [{"field": "tipo_procedimento", "op": "eq", "value": "concurso_limitado_previa_qualificacao"}], "params": {"minimum_days": 5, "deadline_field": "prazo_candidaturas_dias", "counted_from": "nao_indicado", "usual_days": null}}
- leitor:b: não tipável (sem_vocabulario): O vocabulário não prevê um campo de prazo para apresentar documentos comprovativos dos requisitos de capacidade técnica e financeira nem para confirmar compromissos de terceiras entidades.
- verificador (A): regra 1: deadline_field prazo_candidaturas_dias e as fontes dizem nada (L9)

## regra:ccp:auto-prazo-maximo-art187-4-v20180101@v1

- leitor:a17: não tipável (nao_e_prazo_maximo): O prazo é um máximo de cinco dias para a própria entidade adjudicante notificar o candidato, não um prazo para os candidatos apresentarem algo.
- leitor:b: não tipável (sem_vocabulario): O vocabulário não permite representar a ocorrência de um facto que determine a caducidade da qualificação.

## regra:ccp:auto-prazo-maximo-art188-4@v1

- leitor:a17: não tipável (nao_e_prazo_maximo): O prazo é um máximo de cinco dias, não um prazo para apresentar algo.
- leitor:b: não tipável (sem_vocabulario): O vocabulário não permite representar a ocorrência de um facto que determine a caducidade da qualificação.

## regra:ccp:auto-prazo-minimo-art190-2-v20080730@v1

- leitor:a17: {"tipo": "prazo_minimo", "condicoes": [{"field": "publicado_joue", "op": "eq", "value": false}, {"field": "tipo_contrato", "op": "eq", "value": "obras"}, {"field": "tipo_procedimento", "op": "eq", "value": "concurso_limitado_previa_qualificacao"}], "params": {"minimum_days": 8, "deadline_field": "prazo_propostas_dias", "counted_from": "data_envio_convite", "usual_days": null}} || {"tipo": "prazo_minimo", "condicoes": [{"field": "publicado_joue", "op": "eq", "value": false}, {"field": "tipo_contrato", "op": "ne", "value": "obras"}, {"field": "tipo_procedimento", "op": "eq", "value": "concurso_limitado_previa_qualificacao"}], "params": {"minimum_days": 20, "deadline_field": "prazo_propostas_dias", "counted_from": "data_envio_convite", "usual_days": null}}
- leitor:b: não tipável (sem_vocabulario): O vocabulário não permite representar a condição de manifesta simplicidade dos trabalhos necessários à realização da obra.
- verificador (A): regra 1: minimum_days 8 não está nas fontes (L8, L4)

## regra:ccp:auto-prazo-minimo-art190-2@v1

- leitor:a17: {"tipo": "prazo_minimo", "condicoes": [{"field": "publicado_joue", "op": "eq", "value": false}, {"field": "tipo_contrato", "op": "eq", "value": "obras"}, {"field": "tipo_procedimento", "op": "eq", "value": "concurso_limitado_previa_qualificacao"}], "params": {"minimum_days": 6, "deadline_field": "prazo_propostas_dias", "counted_from": "data_envio_convite", "usual_days": null}} || {"tipo": "prazo_minimo", "condicoes": [{"field": "publicado_joue", "op": "eq", "value": false}, {"field": "tipo_contrato", "op": "ne", "value": "obras"}, {"field": "tipo_procedimento", "op": "eq", "value": "concurso_limitado_previa_qualificacao"}], "params": {"minimum_days": 14, "deadline_field": "prazo_propostas_dias", "counted_from": "data_envio_convite", "usual_days": null}}
- leitor:b: não tipável (sem_vocabulario): O vocabulário não permite representar a condição de manifesta simplicidade dos trabalhos necessários à realização da obra.

## regra:ccp:auto-prazo-minimo-art191-v20180101@v1

- leitor:a17: {"tipo": "prazo_minimo", "condicoes": [{"field": "publicado_joue", "op": "eq", "value": true}, {"field": "tipo_procedimento", "op": "eq", "value": "concurso_limitado_previa_qualificacao"}], "params": {"minimum_days": 25, "deadline_field": "prazo_propostas_dias", "counted_from": "data_envio_convite", "usual_days": null}} || {"tipo": "prazo_minimo", "condicoes": [{"field": "anuncio_pre_informacao", "op": "eq", "value": true}, {"field": "publicado_joue", "op": "eq", "value": true}, {"field": "tipo_procedimento", "op": "eq", "value": "concurso_limitado_previa_qualificacao"}], "params": {"minimum_days": 10, "deadline_field": "prazo_propostas_dias", "counted_from": "data_envio_convite", "usual_days": null}} || {"tipo": "prazo_minimo", "condicoes": [{"field": "setores_especiais", "op": "eq", "value": true}, {"field": "tipo_procedimento", "op": "eq", "value": "concurso_limitado_previa_qualificacao"}], "params": {"minimum_days": 10, "deadline_field": "prazo_propostas_dias", "counted_from": "data_envio_convite", "usual_days": null}}
- leitor:b: não tipável (sem_vocabulario): O vocabulário não permite representar as condições de cobertura das prestações, antecedência e conteúdo do anúncio de pré-informação necessárias à redução para 10 dias.
- verificador (A): regra 3, setores_especiais eq True: as fontes não afirmam o facto (L7)
- verificador (B): não tipável: fonte em ccp:art191.2, que é vizinho (L1); não tipável: fonte em ccp:art191.2.a, que é vizinho (L1); não tipável: fonte em ccp:art191.2.b, que é vizinho (L1)

## regra:ccp:auto-prazo-minimo-art191-2-a-v20080730@v1

- leitor:a17: não tipável (sem_vocabulario): A contagem do prazo começa pela antecedência do envio do anúncio de pré-informação, facto que nenhum campo do vocabulário tem.
- leitor:b: não tipável (sem_vocabulario): O vocabulário não permite representar a condição de antecedência do envio do anúncio de pré-informação necessária à aplicação do prazo mínimo de 22 dias.

## regra:ccp:auto-prazo-minimo-art191-2-a@v1

- leitor:a17: não tipável (sem_vocabulario): A contagem do prazo começa pela antecedência do envio do anúncio de pré-informação, facto que nenhum campo do vocabulário tem.
- leitor:b: não tipável (sem_vocabulario): O vocabulário não permite representar a condição de antecedência do envio do anúncio de pré-informação, entre 35 dias e 12 meses, relativamente ao envio do anúncio do concurso.

## regra:ccp:auto-prazo-maximo-art192-3@v1

- leitor:a17: não tipável (nao_e_prazo_maximo): O prazo é o de inação dos candidatos; falta um prazo máximo para os candidatos apresentarem algo.
- leitor:b: não tipável (sem_vocabulario): O vocabulário não prevê a recepção do convite como início da contagem do prazo para manifestar discordância.

## regra:ccp:auto-prazo-maximo-art192-4@v1

- leitor:a17: não tipável (nao_e_prazo_maximo): O prazo é o da própria entidade adjudicante para notificar os candidatos, não um prazo máximo para os candidatos apresentarem algo.
- leitor:b: não tipável (sem_vocabulario): O vocabulário não permite representar a condição de algum candidato qualificado manifestar por escrito discordância sobre o prazo fixado.

## regra:ccp:auto-prazo-minimo-art198-1-v20080730@v1

- leitor:a17: {"tipo": "prazo_minimo", "condicoes": [{"field": "tipo_procedimento", "op": "eq", "value": "procedimento_negociacao"}], "params": {"minimum_days": 37, "deadline_field": "prazo_candidaturas_dias", "counted_from": "data_envio_anuncio", "usual_days": null}}
- leitor:b: {"tipo": "prazo_minimo", "condicoes": [{"field": "publicado_joue", "op": "eq", "value": true}, {"field": "tipo_procedimento", "op": "eq", "value": "procedimento_negociacao"}], "params": {"minimum_days": 37, "deadline_field": "prazo_candidaturas_dias", "counted_from": "data_envio_anuncio", "usual_days": null}}
- verificador (B): regra 1, publicado_joue eq True: as fontes não afirmam o facto (L7)

## regra:ccp:auto-prazo-minimo-art218-v20080730@v1

- leitor:a17: {"tipo": "prazo_minimo", "condicoes": [{"field": "tipo_procedimento", "op": "eq", "value": "dialogo_concorrencial"}], "params": {"minimum_days": 40, "deadline_field": "prazo_propostas_dias", "counted_from": "data_envio_convite", "usual_days": null}}
- leitor:b: {"tipo": "prazo_minimo", "condicoes": [{"field": "tipo_procedimento", "op": "eq", "value": "dialogo_concorrencial"}], "params": {"minimum_days": 40, "deadline_field": "prazo_propostas_dias", "counted_from": "data_envio_convite", "usual_days": null}}
- verificador (B): regra 1, tipo_procedimento eq dialogo_concorrencial: «diálogo concorrencial» não está em ccp:art218; regra 1, tipo_procedimento eq dialogo_concorrencial: as fontes não nomeiam ['dialogo_concorrencial']

## regra:ccp:auto-prazo-maximo-art219-c-3-v20180101@v1

- leitor:a17: não tipável (nao_e_prazo_maximo): O prazo é da própria entidade adjudicante para enviar um anúncio, não um prazo máximo para os concorrentes apresentarem algo.
- leitor:b: não tipável (nao_e_prazo_maximo): O prazo é para a própria entidade adjudicante enviar um anúncio.

## regra:ccp:auto-prazo-maximo-art219-c-3@v1

- leitor:a17: não tipável (nao_e_prazo_maximo): O prazo é da própria entidade adjudicante para enviar um anúncio, não um prazo máximo para os interessados apresentarem algo.
- leitor:b: não tipável (nao_e_prazo_maximo): O prazo é para a própria entidade adjudicante enviar um anúncio.

## regra:ccp:auto-prazo-maximo-art219-i-5@v1

- leitor:a17: {"tipo": "prazo_maximo", "condicoes": [{"field": "tipo_procedimento", "op": "eq", "value": "concurso_concecao"}], "params": {"maximum_days": 5, "deadline_field": "prazo_habilitacao_dias", "counted_from": "data_notificacao"}}
- leitor:b: não tipável (sem_vocabulario): Falta um campo para representar a condição de os termos de referência exigirem aos concorrentes habilitações profissionais específicas.
- verificador (A): regra 1: deadline_field prazo_habilitacao_dias e as fontes dizem nada (L9)

## regra:ccp:auto-prazo-maximo-art234-1-v20080730@v1

- leitor:a17: {"tipo": "prazo_maximo", "condicoes": [{"field": "tipo_procedimento", "op": "eq", "value": "concurso_concecao"}], "params": {"maximum_days": 5, "deadline_field": "prazo_habilitacao_dias", "counted_from": "data_notificacao"}}
- leitor:b: não tipável (sem_vocabulario): Falta no vocabulário uma condição que represente a exigência de habilitações profissionais específicas pelos termos de referência.
- verificador (A): regra 1: deadline_field prazo_habilitacao_dias e as fontes dizem nada (L9)

## regra:ccp:auto-prazo-maximo-art235-v20080730@v1

- leitor:a17: não tipável (nao_e_prazo_maximo): O prazo é da própria entidade adjudicante para enviar o anúncio, não um prazo máximo para os interessados apresentarem algo.
- leitor:b: não tipável (nao_e_prazo_maximo): O prazo é para a própria entidade adjudicante enviar um anúncio.

## regra:ccp:auto-prazo-maximo-art241-3-v20080730@v1

- leitor:a17: não tipável (sem_vocabulario): A regra é de um sistema de aquisição dinâmico, instrumento que o vocabulário não tem.
- leitor:b: não tipável (nao_e_prazo_maximo): O prazo destina-se à entidade adjudicante para notificar a aceitação ou rejeição, não à apresentação de algo.

## regra:ccp:auto-prazo-maximo-art241-a-3@v1

- leitor:a17: não tipável (sem_vocabulario): A regra é de um sistema de aquisição dinâmico, instrumento que o vocabulário não tem.
- leitor:b: não tipável (nao_e_prazo_maximo): O prazo é para a própria entidade adjudicante analisar as candidaturas.

## regra:ccp:auto-prazo-minimo-art242-3-v20080730@v1

- leitor:a17: não tipável (sem_vocabulario): A regra é de um sistema de aquisição dinâmico, instrumento que o vocabulário não tem.
- leitor:b: não tipável (nao_e_prazo_minimo): O prazo regula a publicação do anúncio simplificado pela entidade adjudicante, não a apresentação de elementos pelos interessados.

## regra:ccp:auto-prazo-maximo-art270@v1

- leitor:a17: não tipável (nao_e_prazo_maximo): O prazo é para apresentar uma impugnação, não para apresentar algo.
- leitor:b: não tipável (sem_vocabulario): O vocabulário não contém um campo de prazo para a apresentação de impugnações administrativas.

## regra:ccp:auto-prazo-maximo-art273@v1

- leitor:a17: não tipável (nao_e_prazo_maximo): O prazo é do próprio órgão da administração para notificar, não um prazo máximo para os interessados apresentarem algo.
- leitor:b: não tipável (sem_vocabulario): Falta vocabulário para representar a condição relativa ao objeto da impugnação administrativa.

## regra:ccp:auto-prazo-maximo-art274-1@v1

- leitor:a17: não tipável (nao_e_prazo_maximo): O prazo é da própria entidade adjudicante para decidir, não um prazo máximo para os interessados apresentarem algo.
- leitor:b: não tipável (nao_e_prazo_maximo): O prazo é para decidir as impugnações administrativas, não para apresentar algo.

## regra:ccp:auto-prazo-minimo-art276-v20120811@v1

- leitor:a17: não tipável (nao_e_prazo_minimo): O prazo é de publicitação no Diário da República, não um prazo para apresentar algo.
- leitor:b: não tipável (sem_vocabulario): O vocabulário não permite representar a condição de o contrato ser celebrado por um concessionário de obras públicas que não seja entidade adjudicante.

## regra:ccp:auto-prazo-minimo-art276-v20180101@v1

- leitor:a17: {"tipo": "prazo_minimo", "condicoes": [{"field": "tipo_contrato", "op": "eq", "value": "obras"}, {"field": "tipo_procedimento", "op": "in", "value": ["ajuste_direto", "concurso_limitado_previa_qualificacao", "dialogo_concorrencial"]}], "params": {"minimum_days": 37, "deadline_field": "prazo_candidaturas_dias", "counted_from": "data_envio_anuncio", "usual_days": null}} || {"tipo": "prazo_minimo", "condicoes": [{"field": "tipo_contrato", "op": "eq", "value": "obras"}, {"field": "tipo_procedimento", "op": "in", "value": ["ajuste_direto", "concurso_limitado_previa_qualificacao", "dialogo_concorrencial"]}], "params": {"minimum_days": 40, "deadline_field": "prazo_propostas_dias", "counted_from": "data_envio_anuncio", "usual_days": null}}
- leitor:b: não tipável (sem_vocabulario): O vocabulário não permite representar a condição de o contratante ser um concessionário de obras públicas que não seja entidade adjudicante.
- verificador (A): regra 1, tipo_procedimento in ['ajuste_direto', 'concurso_limitado_previa_qualificacao', 'dialogo_concorrencial']: as fontes não nomeiam ['ajuste_direto']; regra 2, tipo_procedimento in ['ajuste_direto', 'concurso_limitado_previa_qualificacao', 'dialogo_concorrencial']: as fontes não nomeiam ['ajuste_direto']

## regra:ccp:auto-prazo-minimo-art276-v20210620@v1

- leitor:a17: não tipável (nao_e_prazo_minimo): O prazo é de publicitação do contrato no Diário da República, não um prazo para apresentar algo.
- leitor:b: não tipável (sem_vocabulario): O vocabulário não permite representar a condição de os contratos serem celebrados por concessionários de obras públicas que não sejam entidades adjudicantes.

## regra:ccp:auto-prazo-minimo-art276-5-v20080730@v1

- leitor:a17: não tipável (nao_e_prazo_minimo): O prazo é um mínimo para o concessionário não fixar um prazo, não um prazo para os interessados apresentarem algo.
- leitor:b: não tipável (sem_vocabulario): O vocabulário não permite limitar a regra aos concessionários de obras públicas que não sejam entidades adjudicantes.

## regra:ccp:auto-prazo-maximo-art283-a-v20110113@v1

- leitor:a17: não tipável (nao_e_prazo_maximo): O prazo é um dos casos em que os contratos são anuláveis; falta um prazo para apresentar algo.
- leitor:b: não tipável (nao_e_prazo_maximo): Os prazos respeitam à outorga do contrato, não à apresentação de elementos, pelo que não existe um prazo máximo tipável.
- verificador (B): não tipável: fonte em ccp:art283-a.2.c, que é vizinho (L1)

## regra:ccp:auto-prazo-maximo-art283-a-v20210620@v1

- leitor:a17: não tipável (nao_e_prazo_maximo): O prazo é de 15 dias, quando aplicável, antes de decorrido o prazo de suspensão previsto no n.º 3 do artigo 95.º ou na alínea a) do n.º 1 do artigo 104.º, e não um prazo para apresentar algo.
- leitor:b: não tipável (nao_e_prazo_maximo): A passagem estabelece um prazo de suspensão da outorga do contrato, não um prazo máximo para apresentar algo.
- verificador (B): não tipável: fonte em ccp:art283-a.2.c, que é vizinho (L1)

## regra:ccp:auto-prazo-maximo-art283-a-2-c@v1

- leitor:a17: não tipável (nao_e_prazo_maximo): O prazo é de 10 dias antes da outorga do contrato, não um prazo para apresentar algo.
- leitor:b: não tipável (nao_e_prazo_maximo): A passagem fixa um prazo mínimo para a outorga do contrato, não um prazo máximo para apresentar algo.

## regra:ccp:auto-prazo-maximo-art287-6-c-v20180101@v1

- leitor:a17: não tipável (nao_e_prazo_maximo): O prazo é de 10 dias antes da outorga do contrato, não um prazo para apresentar algo.
- leitor:b: não tipável (nao_e_prazo_maximo): A passagem fixa um prazo mínimo de espera para a outorga do contrato, não um prazo máximo para apresentar algo.

## regra:ccp:auto-prazo-minimo-art295-v20091007@v1

- leitor:a17: não tipável (nao_e_prazo_minimo): O prazo é do próprio contraente público para promover a liberação da caução, não um prazo mínimo para os interessados apresentarem algo.
- leitor:b: não tipável (nao_e_prazo_minimo): Os prazos regulam a liberação da caução pelo contraente público, não um prazo mínimo para apresentar algo.
- verificador (B): não tipável: fonte em ccp:art295.3, que é vizinho (L1)

## regra:ccp:auto-prazo-maximo-art295-5-a-v20080730@v1

- leitor:a17: não tipável (nao_e_prazo_maximo): O prazo é de 30 dias para a libertação de parte da caução, não um prazo máximo para a entidade pública.
- leitor:b: não tipável (nao_e_prazo_maximo): O prazo é para o contraente público promover a liberação parcial da caução, não para apresentar algo.

## regra:ccp:auto-prazo-maximo-art296-2@v1

- leitor:a17: não tipável (nao_e_prazo_maximo): O prazo é da própria entidade adjudicante para renovar o valor da caução, não um prazo máximo para os co-contratantes apresentarem algo.
- leitor:b: não tipável (nao_e_prazo_maximo): O prazo é para renovar o valor da caução, não para apresentar algo.

## regra:ccp:auto-prazo-maximo-art299-1-v20080730@v1

- leitor:a17: não tipável (nao_e_prazo_maximo): O prazo é para efetuar o pagamento, não para apresentar algo.
- leitor:b: não tipável (nao_e_prazo_maximo): O prazo é para o contraente público efetuar pagamentos, não para apresentar algo.

## regra:ccp:auto-prazo-maximo-art299-1-a@v1

- leitor:a17: não tipável (nao_e_prazo_maximo): O prazo é o de pagamento, não um prazo para apresentar algo.
- leitor:b: não tipável (nao_e_prazo_maximo): A passagem fixa o vencimento de uma obrigação de pagamento, não um prazo para apresentar algo.

## regra:ccp:auto-prazo-maximo-art299-1-b@v1

- leitor:a17: não tipável (nao_e_prazo_maximo): O prazo é de 30 dias para a própria entidade adjudicante determinar a recepção dos bens ou serviços; falta um prazo máximo para os interessados apresentarem algo.
- leitor:b: não tipável (nao_e_prazo_maximo): O prazo respeita ao vencimento de uma obrigação pecuniária, não à apresentação de elementos.

## regra:ccp:auto-prazo-maximo-art299-1-c@v1

- leitor:a17: não tipável (nao_e_prazo_maximo): O prazo é de 30 dias para efetuar o pagamento, não um prazo máximo para apresentar algo.
- leitor:b: não tipável (nao_e_prazo_maximo): O prazo é de pagamento pelo contraente público, não de apresentação de elementos.

## regra:ccp:auto-prazo-maximo-art299-1-d@v1

- leitor:a17: não tipável (nao_e_prazo_maximo): O prazo é o máximo do próprio procedimento de aceitação ou verificação, não um prazo para apresentar algo.
- leitor:b: não tipável (nao_e_prazo_maximo): O prazo respeita ao vencimento de uma obrigação pecuniária, não à apresentação de elementos.

## regra:ccp:auto-prazo-maximo-art299-2@v1

- leitor:a17: não tipável (nao_e_prazo_maximo): O prazo é o máximo da duração do procedimento de aceitação ou verificação, não um prazo para apresentar algo.
- leitor:b: não tipável (nao_e_prazo_maximo): O prazo limita a duração do procedimento de aceitação ou verificação, não sendo um prazo para apresentar algo.

## regra:ccp:auto-prazo-maximo-art299-3@v1

- leitor:a17: não tipável (nao_e_prazo_maximo): O prazo é de 30 dias para efetuar o pagamento, não um prazo máximo para apresentar algo.
- leitor:b: não tipável (nao_e_prazo_maximo): O prazo é para o contraente público efetuar pagamentos, não para apresentar algo.

## regra:ccp:auto-prazo-maximo-art299-a-1@v1

- leitor:a17: não tipável (nao_e_prazo_maximo): O prazo é um máximo de 15 dias antes do vencimento das obrigações; não é um prazo para apresentar nada.
- leitor:b: não tipável (nao_e_prazo_maximo): O prazo refere-se ao vencimento de obrigações pecuniárias, não à apresentação de elementos.

## regra:ccp:auto-prazo-maximo-art315-v20210620@v1

- leitor:a17: não tipável (nao_e_prazo_maximo): O prazo é de seis meses, tempo de manutenção da publicidade, e não um prazo para apresentar algo.
- leitor:b: não tipável (nao_e_prazo_maximo): Os prazos respeitam à publicitação das modificações pelo contraente público e à manutenção dessa publicidade.
- verificador (B): não tipável: fonte em ccp:art315.1, que é vizinho (L1)

## regra:ccp:auto-prazo-maximo-art315-1-v20180101@v1

- leitor:a17: não tipável (nao_e_prazo_maximo): O prazo é da própria entidade adjudicante para publicitar, não um prazo máximo para os interessados apresentarem algo.
- leitor:b: não tipável (nao_e_prazo_maximo): Os prazos são para o contraente público publicitar modificações contratuais e manter essa publicidade, não para apresentar elementos.

## regra:ccp:auto-prazo-maximo-art315-1@v1

- leitor:a17: não tipável (nao_e_prazo_maximo): O prazo é o da manutenção da publicidade no portal, não um prazo para apresentar algo.
- leitor:b: não tipável (nao_e_prazo_maximo): Os prazos regulam a publicitação pelo contraente público e a manutenção da publicidade, não a apresentação de elementos.

## regra:ccp:auto-prazo-maximo-art319-3-v20080730@v1

- leitor:a17: não tipável (nao_e_prazo_maximo): O prazo é da própria entidade adjudicante para se pronunciar, não um prazo máximo para os interessados apresentarem algo.
- leitor:b: não tipável (nao_e_prazo_maximo): O prazo é para o próprio contraente público se pronunciar, não para apresentar algo.

## regra:ccp:auto-prazo-maximo-art319-3-v20180101@v1

- leitor:a17: não tipável (nao_e_prazo_maximo): O prazo é da própria entidade adjudicante para se pronunciar, não um prazo máximo para os cocontratantes apresentarem algo.
- leitor:b: não tipável (nao_e_prazo_maximo): O prazo destina-se à pronúncia do próprio contraente público.

## regra:ccp:auto-prazo-minimo-art327-v20080730@v1

- leitor:a17: não tipável (nao_e_prazo_minimo): O prazo é da própria entidade adjudicante, para notificar, e não um prazo mínimo para os interessados apresentarem algo.
- leitor:b: não tipável (nao_e_prazo_minimo): O prazo é uma antecedência de notificação para exercer o direito de recusar o cumprimento, não um prazo para apresentar algo previsto no vocabulário.
- verificador (B): não tipável: fonte em ccp:art327.3, que é vizinho (L1)

## regra:ccp:auto-prazo-maximo-art327-4@v1

- leitor:a17: não tipável (nao_e_prazo_maximo): O prazo é da própria entidade adjudicante para se opor, não um prazo máximo para os cocontratantes apresentarem algo.
- leitor:b: não tipável (nao_e_prazo_maximo): O prazo destina-se ao próprio contraente público exercer oposição.

## regra:ccp:auto-prazo-maximo-art332-4@v1

- leitor:a17: não tipável (nao_e_prazo_maximo): O prazo é o da produção de efeitos da resolução, não um prazo para apresentar algo.
- leitor:b: não tipável (nao_e_prazo_maximo): Os 30 dias determinam a produção de efeitos da declaração de resolução, não um prazo máximo para apresentar algo.

## regra:ccp:auto-prazo-maximo-art333-4@v1

- leitor:a17: não tipável (nao_e_prazo_maximo): O prazo é da própria entidade adjudicante para comunicar, não um prazo máximo para os interessados apresentarem algo.
- leitor:b: não tipável (nao_e_prazo_maximo): O prazo de 10 dias é para uma comunicação pelo próprio contraente público, não para apresentar elementos.

## regra:ccp:auto-prazo-maximo-art334-3@v1

- leitor:a17: não tipável (nao_e_prazo_maximo): O prazo é o da própria entidade adjudicante para pagar a indemnização, não um prazo máximo para os interessados apresentarem algo.
- leitor:b: não tipável (nao_e_prazo_maximo): O prazo respeita ao pagamento de uma indemnização e não à apresentação de elementos.

## regra:ccp:auto-prazo-maximo-art345-3@v1

- leitor:a17: não tipável (nao_e_prazo_maximo): O prazo é o da empreiteira para reclamar ou apresentar reservas, não um prazo máximo para a entidade adjudicante formalizar algo em auto.
- leitor:b: {"tipo": "prazo_maximo", "condicoes": [{"field": "tipo_contrato", "op": "eq", "value": "obras"}], "params": {"maximum_days": 10, "deadline_field": "prazo_reclamacao_dias", "counted_from": "data_notificacao"}}
- verificador (B): regra 1: as fontes de maximum_days não dizem um máximo («não pode ser superior a», «no prazo de», L8)

## regra:ccp:auto-prazo-maximo-art345-4@v1

- leitor:a17: não tipável (nao_e_prazo_maximo): O prazo é da empreiteira para apresentar uma exposição fundamentada, não um prazo máximo para a entidade adjudicante.
- leitor:b: não tipável (sem_vocabulario): O vocabulário não permite representar a condição de as reclamações ou reservas terem sido exaradas no próprio auto e limitadas ao enunciado genérico do respetivo objeto.

## regra:ccp:auto-prazo-maximo-art354-v20080730@v1

- leitor:a17: não tipável (nao_e_prazo_maximo): O prazo é o da caducidade do direito à reposição do equilíbrio, não um prazo para apresentar algo.
- leitor:b: não tipável (sem_vocabulario): O vocabulário de counted_from não contempla o evento constitutivo do direito nem o momento em que o empreiteiro dele tome conhecimento.
- verificador (B): não tipável: fonte em ccp:art354.2, que é vizinho (L1)

## regra:ccp:auto-prazo-maximo-art354-2@v1

- leitor:a17: não tipável (nao_e_prazo_maximo): O prazo é o da caducidade do direito à reposição do equilíbrio financeiro, não um prazo máximo para os interessados apresentarem algo.
- leitor:b: não tipável (sem_vocabulario): O vocabulário não prevê o início da contagem no evento constitutivo do direito ou no momento em que o empreiteiro dele tome conhecimento.

## regra:ccp:auto-prazo-maximo-art358-2-v20080730@v1

- leitor:a17: não tipável (nao_e_prazo_maximo): O prazo é da própria entidade adjudicante para comunicar, não um prazo máximo para os interessados apresentarem algo.
- leitor:b: não tipável (nao_e_prazo_maximo): O prazo destina-se à comunicação pelo dono da obra, não à apresentação de elementos por um interessado.

## regra:ccp:auto-prazo-maximo-art359-1@v1

- leitor:a17: não tipável (nao_e_prazo_maximo): O prazo é o da própria entidade adjudicante para celebrar o contrato, não um prazo máximo para o empreiteiro apresentar algo.
- leitor:b: não tipável (nao_e_prazo_maximo): O prazo é para concluir a consignação da obra, não para apresentar algo.

## regra:ccp:auto-prazo-maximo-art366-1@v1

- leitor:a17: não tipável (nao_e_prazo_maximo): O prazo é o de suspensão da execução da obra, não um prazo para apresentar algo.
- leitor:b: não tipável (nao_e_prazo_maximo): O prazo limita a duração da suspensão dos trabalhos, não sendo um prazo para apresentar nada.

## regra:ccp:auto-prazo-maximo-art366-6@v1

- leitor:a17: não tipável (nao_e_prazo_maximo): O prazo é um máximo de cinco dias para a formalização da comunicação, não um prazo para apresentar algo.
- leitor:b: não tipável (nao_e_prazo_maximo): O prazo destina-se à formalização escrita das comunicações de suspensão, não à apresentação de elementos abrangidos pelos campos de prazo do vocabulário.

## regra:ccp:auto-prazo-maximo-art372-1-v20080730@v1

- leitor:a17: não tipável (nao_e_prazo_maximo): O prazo é o da própria entidade adjudicante para decidir a reclamação, não um prazo máximo para o empreiteiro apresentar algo.
- leitor:b: não tipável (sem_vocabulario): O vocabulário não prevê como início da contagem a recepção da ordem do dono da obra de execução dos trabalhos a mais.

## regra:ccp:auto-prazo-maximo-art372-1-v20180101@v1

- leitor:a17: não tipável (nao_e_prazo_maximo): O prazo é o da própria entidade adjudicante para decidir se o empreiteiro pode reclamar, não um prazo máximo para o empreiteiro apresentar algo.
- leitor:b: não tipável (sem_vocabulario): O vocabulário não prevê como início da contagem a receção da ordem do dono da obra de execução dos trabalhos complementares.

## regra:ccp:auto-prazo-maximo-art372-1-v20210620@v1

- leitor:a17: não tipável (nao_e_prazo_maximo): O prazo é o da empreiteiro para reclamar, não um prazo máximo para a dono da obra.
- leitor:b: não tipável (sem_vocabulario): O vocabulário não permite representar os pressupostos da reclamação nem o início da contagem na receção da ordem de execução dos trabalhos complementares.

## regra:ccp:auto-prazo-maximo-art372-1@v1

- leitor:a17: não tipável (nao_e_prazo_maximo): O prazo é o da própria entidade adjudicante para decidir a reclamação, não um prazo máximo para o empreiteiro apresentar algo.
- leitor:b: não tipável (sem_vocabulario): O vocabulário não permite representar os pressupostos específicos da reclamação nem o início da contagem na receção da ordem de execução dos trabalhos complementares.

## regra:ccp:auto-prazo-maximo-art372-2@v1

- leitor:a17: não tipável (nao_e_prazo_maximo): O prazo é da própria entidade adjudicante para apreciar a reclamação, não um prazo máximo para os interessados apresentarem algo.
- leitor:b: não tipável (nao_e_prazo_maximo): O prazo é para o dono da obra apreciar a reclamação, não para apresentar algo.

## regra:ccp:auto-prazo-maximo-art373-v20210620@v1

- leitor:a17: não tipável (nao_e_prazo_maximo): O prazo é do próprio dono da obra para se pronunciar, não um prazo para o empreiteiro apresentar algo.
- leitor:b: não tipável (sem_vocabulario): O vocabulário não permite representar as condições relativas à espécie e à execução dos trabalhos nem o início da contagem na receção do pedido de apresentação da proposta.
- verificador (B): não tipável: fonte em ccp:art373.2, que é vizinho (L1); não tipável: fonte em ccp:art373.1.b, que é vizinho (L1); não tipável: fonte em ccp:art373.2, que é vizinho (L1)

## regra:ccp:auto-prazo-maximo-art373-2-v20080730@v1

- leitor:a17: {"tipo": "prazo_maximo", "condicoes": [{"field": "tipo_contrato", "op": "eq", "value": "obras"}], "params": {"maximum_days": 10, "deadline_field": "prazo_propostas_dias", "counted_from": "data_notificacao"}}
- leitor:b: não tipável (sem_vocabulario): O vocabulário não permite representar a falta de estipulação contratual nem as condições relativas à espécie dos trabalhos e às condições da sua execução.
- verificador (A): regra 1: deadline_field prazo_propostas_dias e as fontes dizem nada (L9)

## regra:ccp:auto-prazo-maximo-art373-2-v20091007@v1

- leitor:a17: não tipável (nao_e_prazo_maximo): O prazo é da própria entidade adjudicante para apresentar uma proposta de preço e de prazo, não um prazo máximo para o empreiteiro apresentar algo.
- leitor:b: não tipável (sem_vocabulario): O vocabulário não permite representar as condições relativas à estipulação contratual e à espécie e condições de execução dos trabalhos, nem o início da contagem na recepção da ordem de execução.

## regra:ccp:auto-prazo-maximo-art373-2@v1

- leitor:a17: não tipável (nao_e_prazo_maximo): O prazo é da própria entidade adjudicante para apresentar os elementos de projeto, não um prazo máximo para o empreiteiro apresentar algo.
- leitor:b: não tipável (sem_vocabulario): O vocabulário não permite representar a falta de estipulação contratual, as condições relativas à espécie e execução dos trabalhos nem a contagem desde a receção do pedido.

## regra:ccp:auto-prazo-maximo-art373-3@v1

- leitor:a17: não tipável (nao_e_prazo_maximo): O prazo é o da própria entidade adjudicante para se pronunciar, não um prazo máximo para o empreiteiro apresentar algo.
- leitor:b: não tipável (sem_vocabulario): O vocabulário não permite limitar a regra aos contratos de empreitada de conceção-construção.

## regra:ccp:auto-prazo-maximo-art376-6-v20080730@v1

- leitor:a17: não tipável (nao_e_prazo_maximo): O prazo é da própria entidade adjudicante para pronunciar-se, não um prazo máximo para o empreiteiro apresentar algo.
- leitor:b: não tipável (nao_e_prazo_maximo): O prazo é para o dono da obra se pronunciar e comunicar a sua posição ao empreiteiro, sendo um prazo para a própria entidade adjudicante.

## regra:ccp:auto-prazo-maximo-art376-7-v20120811@v1

- leitor:a17: não tipável (nao_e_prazo_maximo): O prazo é do próprio dono da obra para se pronunciar, não um prazo máximo para o empreiteiro apresentar algo.
- leitor:b: não tipável (nao_e_prazo_maximo): O prazo é para a própria entidade adjudicante se pronunciar e comunicar a sua posição ao empreiteiro.

## regra:ccp:auto-prazo-maximo-art378-3-v20180101@v1

- leitor:a17: não tipável (nao_e_prazo_maximo): O prazo é o da própria entidade adjudicante para reclamar, não um prazo máximo para o empreiteiro apresentar algo.
- leitor:b: não tipável (sem_vocabulario): O vocabulário não prevê a consignação como início da contagem nem a exclusão dos erros ou omissões só detetáveis durante a execução da obra.

## regra:ccp:auto-prazo-maximo-art378-4-v20080730@v1

- leitor:a17: não tipável (nao_e_prazo_maximo): O prazo é o da própria entidade adjudicante para exigir a identificação dos erros e omissões, não um prazo máximo para os interessados apresentarem algo.
- leitor:b: não tipável (nao_e_prazo_maximo): O prazo respeita à identificação de erros e omissões pelo empreiteiro, não à apresentação de elementos.

## regra:ccp:auto-prazo-maximo-art378-4-v20120811@v1

- leitor:a17: não tipável (nao_e_prazo_maximo): O prazo é o da própria entidade adjudicante para não ser exigível a deteção dos erros e omissões, não um prazo máximo para os interessados apresentarem algo.
- leitor:b: não tipável (nao_e_prazo_maximo): O prazo refere-se à identificação de erros e omissões pelo empreiteiro, não à apresentação de elementos.

## regra:ccp:auto-prazo-maximo-art378-4-v20180101@v1

- leitor:a17: não tipável (nao_e_prazo_maximo): O prazo é o da própria entidade adjudicante para exigir a deteção dos erros e omissões; falta um prazo para apresentar algo.
- leitor:b: não tipável (nao_e_prazo_maximo): O prazo é para identificar erros e omissões, não para apresentar algo.

## regra:ccp:auto-prazo-maximo-art378-4@v1

- leitor:a17: não tipável (nao_e_prazo_maximo): O prazo é da própria entidade adjudicante para reclamar, não um prazo máximo para o empreiteiro apresentar algo.
- leitor:b: não tipável (sem_vocabulario): O vocabulário não prevê este início da contagem nem a condição de os erros ou omissões serem só detetáveis nesse momento.

## regra:ccp:auto-prazo-maximo-art378-5@v1

- leitor:a17: não tipável (nao_e_prazo_maximo): O prazo é de 30 dias para não serem identificados os trabalhos complementares, não um prazo máximo para os reclamar.
- leitor:b: não tipável (nao_e_prazo_maximo): O prazo refere-se à identificação de erros e omissões pelo empreiteiro, não à apresentação de elementos.

## regra:ccp:auto-prazo-maximo-art385-v20230715@v1

- leitor:a17: não tipável (nao_e_prazo_maximo): O prazo é de cinco dias para comunicar a subempreitada, não um prazo máximo para os interessados apresentarem algo.
- leitor:b: não tipável (nao_e_prazo_maximo): O prazo destina-se à comunicação da celebração de uma subempreitada ao dono da obra, e não a uma apresentação prevista no vocabulário.
- verificador (B): não tipável: fonte em ccp:art385.3, que é vizinho (L1)

## regra:ccp:auto-prazo-maximo-art385-3-v20080730@v1

- leitor:a17: não tipável (nao_e_prazo_maximo): O prazo é de cinco dias para comunicar o contrato de subempreitada, não um prazo máximo para os interessados apresentarem algo.
- leitor:b: não tipável (nao_e_prazo_maximo): O prazo destina-se à comunicação da celebração de uma subempreitada ao dono da obra, não a uma apresentação abrangida pelos campos de prazo.

## regra:ccp:auto-prazo-maximo-art385-3@v1

- leitor:a17: não tipável (nao_e_prazo_maximo): O prazo é da própria entidade adjudicante para comunicar, não um prazo máximo para o empreiteiro apresentar algo.
- leitor:b: não tipável (nao_e_prazo_maximo): O prazo destina-se à comunicação da celebração de uma subempreitada, não à apresentação de elementos abrangidos pelos campos de prazo.

## regra:ccp:auto-prazo-maximo-art386-2@v1

- leitor:a17: não tipável (nao_e_prazo_maximo): O prazo é da própria entidade adjudicante para comunicar o facto, não um prazo máximo para os interessados apresentarem algo.
- leitor:b: não tipável (nao_e_prazo_maximo): O prazo destina-se a uma comunicação do dono da obra, não à apresentação de elementos.

## regra:ccp:auto-prazo-maximo-art389-1@v1

- leitor:a17: não tipável (nao_e_prazo_maximo): O prazo é da empreiteira para elaborar a conta corrente, não um prazo máximo para a entidade adjudicante apresentar algo.
- leitor:b: não tipável (nao_e_prazo_maximo): O prazo é para elaborar a conta corrente, não para apresentar algo.

## regra:ccp:auto-prazo-maximo-art394-5@v1

- leitor:a17: não tipável (nao_e_prazo_maximo): O prazo é do próprio dono da obra para vistoriar, não um prazo máximo para os interessados apresentarem algo.
- leitor:b: não tipável (nao_e_prazo_maximo): O prazo é para o dono da obra realizar a vistoria, não para apresentar algo.

## regra:ccp:auto-prazo-maximo-art401-1@v1

- leitor:a17: não tipável (nao_e_prazo_maximo): O prazo é da própria entidade adjudicante para enviar a conta final, não um prazo máximo para o empreiteiro apresentar algo.
- leitor:b: {"tipo": "prazo_maximo", "condicoes": [{"field": "tipo_contrato", "op": "eq", "value": "obras"}], "params": {"maximum_days": 15, "deadline_field": "prazo_reclamacao_dias", "counted_from": "nao_indicado"}}

## regra:ccp:auto-prazo-maximo-art401-3@v1

- leitor:a17: não tipável (nao_e_prazo_maximo): O prazo é da própria entidade adjudicante para comunicar a sua decisão, não um prazo máximo para o empreiteiro apresentar algo.
- leitor:b: não tipável (nao_e_prazo_maximo): O prazo destina-se à comunicação da decisão pelo dono da obra, não à apresentação de elementos pelo interessado.

## regra:ccp:auto-prazo-maximo-art402-1@v1

- leitor:a17: não tipável (nao_e_prazo_maximo): O prazo é do próprio dono da obra para enviar o relatório final, não um prazo máximo para os interessados apresentarem algo.
- leitor:b: não tipável (nao_e_prazo_maximo): O prazo é para o dono da obra enviar o relatório final da obra, obrigação da própria entidade adjudicante.

## regra:ccp:auto-prazo-maximo-art404-1@v1

- leitor:a17: não tipável (nao_e_prazo_maximo): O prazo é do próprio dono da obra para notificar o empreiteiro, não um prazo máximo para o empreiteiro apresentar algo.
- leitor:b: não tipável (sem_vocabulario): O vocabulário não contém um campo de prazo para a apresentação de um plano de trabalhos modificado.

## regra:ccp:auto-prazo-maximo-art405-v20080730@v1

- leitor:a17: não tipável (nao_e_prazo_maximo): O prazo é o da própria entidade adjudicante para dar conhecimento da resolução, não um prazo máximo para os interessados apresentarem algo.
- leitor:b: não tipável (nao_e_prazo_maximo): A passagem fixa fundamentos de resolução do contrato, não um prazo máximo para apresentar algo.
- verificador (B): não tipável: fonte em ccp:art405.1, que é vizinho (L1); não tipável: fonte em ccp:art405.1.d, que é vizinho (L1)

## regra:ccp:auto-prazo-maximo-art405-v20210620@v1

- leitor:a17: não tipável (nao_e_prazo_maximo): O prazo é de comunicação da resolução do contrato ao Instituto da Construção e do Imobiliário, I. P.; falta um prazo para apresentar algo.
- leitor:b: não tipável (nao_e_prazo_maximo): O prazo refere-se ao início da execução dos trabalhos, não à apresentação de elementos.
- verificador (B): não tipável: fonte em ccp:art405.1.d, que é vizinho (L1)

## regra:ccp:auto-prazo-maximo-art405-1-d@v1

- leitor:a17: não tipável (nao_e_prazo_maximo): O prazo é o da própria entidade adjudicante para informar o dono da obra, não um prazo máximo para o empreiteiro apresentar algo.
- leitor:b: não tipável (nao_e_prazo_maximo): O prazo refere-se ao início da execução dos trabalhos, não à apresentação de qualquer elemento.

## regra:ccp:auto-prazo-maximo-art405-2@v1

- leitor:a17: não tipável (nao_e_prazo_maximo): O prazo é da própria entidade adjudicante para informar o Instituto dos Mercados Públicos, do Imobiliário e da Construção, I. P.; não é um prazo máximo para os interessados apresentarem algo.
- leitor:b: não tipável (nao_e_prazo_maximo): O prazo destina-se ao cumprimento de um dever de informação pelo dono da obra, não à apresentação de elementos pelos interessados.

## regra:ccp:auto-prazo-maximo-art406-b@v1

- leitor:a17: não tipável (nao_e_prazo_maximo): O prazo é o de interrupção dos trabalhos, não um prazo para apresentar algo.
- leitor:b: não tipável (nao_e_prazo_maximo): Os 120 dias constituem um fundamento de resolução pelo empreiteiro, não um prazo para apresentar algo.

## regra:ccp:auto-prazo-maximo-art464-a-v20210620@v1

- leitor:a17: não tipável (nao_e_prazo_maximo): O valor é um limite de acumulação de sanções; falta um prazo para apresentar algo.
- leitor:b: não tipável (nao_e_prazo_maximo): Os prazos fixam a duração de uma sanção e uma obrigação de comunicação dos contraentes públicos, não um prazo máximo para apresentação de elementos pelos participantes.
- verificador (B): não tipável: fonte em ccp:art464-a.1, que é vizinho (L1); não tipável: fonte em ccp:art464-a.2, que é vizinho (L1)

## regra:ccp:auto-prazo-maximo-art464-a-2-v20180101@v1

- leitor:a17: não tipável (nao_e_prazo_maximo): O prazo é da própria entidade adjudicante para comunicar, não um prazo máximo para os contraentes públicos apresentarem algo.
- leitor:b: não tipável (nao_e_prazo_maximo): O prazo destina-se à comunicação de situações de incumprimento pelos contraentes públicos.

## regra:ccp:auto-prazo-maximo-art464-e-2@v1

- leitor:a17: não tipável (nao_e_prazo_maximo): O prazo é da própria parte requerida para responder, não um prazo máximo para a comissão.
- leitor:b: não tipável (sem_vocabulario): O vocabulário não contém um campo de prazo para apresentar resposta e indicar um membro para a comissão.

## regra:ccp:auto-prazo-maximo-art464-e-3@v1

- leitor:a17: não tipável (nao_e_prazo_maximo): O prazo é o máximo da própria tentativa de conciliação, não um prazo para os interessados apresentarem algo.
- leitor:b: não tipável (nao_e_prazo_maximo): O prazo é para a realização da tentativa de conciliação, não para apresentar algo.

## regra:ccp:auto-prazo-maximo-art464-g@v1

- leitor:a17: não tipável (nao_e_prazo_maximo): O prazo é de prescrição e caducidade, não um prazo para apresentar algo.
- leitor:b: não tipável (nao_e_prazo_maximo): Os 30 dias determinam o reinício dos prazos de prescrição e de caducidade, não um prazo máximo para apresentar algo.

## regra:eu-1989-665:auto-prazo-minimo-art1-5@v1

- leitor:a17: não tipável (nao_e_prazo_minimo): O prazo é de suspensão da possibilidade de celebrar o contrato, não um prazo para apresentar algo.
- leitor:b: não tipável (nao_e_prazo_minimo): O prazo fixa a duração da suspensão da possibilidade de celebrar o contrato, não um prazo para apresentar algo.

## regra:eu-1989-665:auto-prazo-minimo-art2-a-2@v1

- leitor:a17: não tipável (sem_vocabulario): A contagem do prazo é feita em dias consecutivos, unidade que o vocabulário não tem.
- leitor:b: não tipável (nao_e_prazo_minimo): O prazo suspende a celebração do contrato; não é um prazo para apresentar nada.

## regra:eu-1989-665:auto-prazo-minimo-art2-c@v1

- leitor:a17: não tipável (sem_vocabulario): A contagem do prazo é feita em dias consecutivos, unidade que o vocabulário não tem.
- leitor:b: não tipável (sem_vocabulario): O vocabulário não contém um campo de prazo para a interposição de recurso.
- verificador (B): não tipável: «Prazos para interposição de recurso» não está em eu-1989-665:art2-c

## regra:eu-1989-665:auto-prazo-minimo-art2-d-5@v1

- leitor:a17: não tipável (nao_e_prazo_minimo): O prazo é de 10 dias consecutivos antes da celebração do contrato, não um prazo para apresentar algo.
- leitor:b: não tipável (nao_e_prazo_minimo): O prazo é de espera para a celebração do contrato, não para apresentar algo.

## regra:eu-1989-665:auto-prazo-maximo-art3-3@v1

- leitor:a17: não tipável (nao_e_prazo_maximo): O prazo é de 30 dias, contados da recepção da notificação, para comunicar à Comissão; falta um prazo máximo.
- leitor:b: não tipável (nao_e_prazo_maximo): O prazo destina-se à comunicação do Estado-Membro à Comissão, não à apresentação de elementos por participantes num procedimento de contratação.

## regra:eu-1992-13:auto-prazo-minimo-art1-5@v1

- leitor:a17: não tipável (nao_e_prazo_minimo): O prazo é de suspensão da possibilidade de celebrar o contrato, não um prazo para apresentar algo.
- leitor:b: não tipável (nao_e_prazo_minimo): O prazo regula a suspensão da possibilidade de celebrar o contrato, não a apresentação de qualquer elemento.

## regra:eu-1992-13:auto-prazo-minimo-art2-a-2@v1

- leitor:a17: não tipável (nao_e_prazo_minimo): O prazo suspensivo é de 10 dias antes de um recurso, não um prazo para apresentar algo.
- leitor:b: não tipável (nao_e_prazo_minimo): A passagem fixa um prazo suspensivo para a celebração do contrato, não um prazo para apresentar algo.

## regra:eu-1992-13:auto-prazo-minimo-art2-c@v1

- leitor:a17: não tipável (sem_vocabulario): A contagem do prazo é feita em dias consecutivos, unidade que o vocabulário não tem.
- leitor:b: não tipável (sem_vocabulario): O vocabulário não prevê um campo de prazo para a interposição de recurso.
- verificador (B): não tipável: «Prazos para interposição de recurso» não está em eu-1992-13:art2-c

## regra:eu-1992-13:auto-prazo-minimo-art2-d-4@v1

- leitor:a17: não tipável (nao_e_prazo_minimo): O prazo é um caso em que a publicação do anúncio é permitida; falta um prazo mínimo para apresentar algo.
- leitor:b: não tipável (nao_e_prazo_minimo): O prazo regula a espera para a celebração do contrato, não a apresentação de elementos.

## regra:eu-1992-13:auto-prazo-minimo-art2-d-5@v1

- leitor:a17: não tipável (nao_e_prazo_minimo): O prazo é de 10 dias consecutivos antes de celebrar o contrato, não um prazo para apresentar algo.
- leitor:b: não tipável (nao_e_prazo_minimo): O prazo limita a celebração do contrato pela entidade adjudicante e não se destina à apresentação de nada.

## regra:eu-1992-13:auto-prazo-maximo-art8-3@v1

- leitor:a17: não tipável (nao_e_prazo_maximo): O prazo é do próprio Estado-Membro para comunicar, não um prazo máximo para os interessados apresentarem algo.
- leitor:b: não tipável (nao_e_prazo_maximo): O prazo destina-se a uma comunicação do Estado-Membro à Comissão, não à apresentação de elementos num procedimento de contratação.

## regra:eu-2004-17:auto-prazo-maximo-art15-4-v20041101@v1

- leitor:a17: não tipável (sem_vocabulario): A regra é de um sistema de aquisição dinâmico, instrumento que o vocabulário não tem.
- leitor:b: não tipável (nao_e_prazo_maximo): O prazo é para a entidade adjudicante concluir a avaliação, não para apresentar algo.

## regra:eu-2004-17:auto-limiar-art16-a-v20160101@v1

- leitor:a17: não tipável (nao_e_limiar): O valor delimita os contratos a que a directiva se aplica; não é o limite até ao qual um procedimento pode ser escolhido.
- leitor:b: não tipável (nao_e_limiar): O valor delimita a aplicação da diretiva, não o limite até ao qual um procedimento pode ser escolhido.

## regra:eu-2004-17:auto-limiar-art16-b-v20160101@v1

- leitor:a17: não tipável (nao_e_limiar): O valor delimita os contratos a que a directiva se aplica; não é o limite até ao qual um procedimento pode ser escolhido.
- leitor:b: não tipável (nao_e_limiar): O valor delimita a aplicação da diretiva, não o limite até ao qual um procedimento pode ser escolhido.

## regra:eu-2004-17:auto-limiar-art41-1-a-v20041101@v1

- leitor:a17: não tipável (nao_e_limiar): O valor delimita os contratos que estão sujeitos à publicitação no perfil de adquirente; não é o limite até ao qual um procedimento pode ser escolhido.
- leitor:b: não tipável (nao_e_limiar): O valor agrega vários contratos ou acordos-quadro para efeitos de anúncio periódico indicativo; não fixa um limite para a escolha de um procedimento.

## regra:eu-2004-17:auto-limiar-art41-1-b-v20041101@v1

- leitor:a17: não tipável (nao_e_limiar): O valor delimita os contratos que dão acesso a um anúncio periódico indicativo; não é o limite até ao qual um procedimento pode ser escolhido.
- leitor:b: não tipável (nao_e_limiar): O montante refere-se ao valor agregado dos contratos a divulgar num anúncio periódico indicativo, sem fixar um limite para a escolha de um procedimento.

## regra:eu-2004-17:auto-prazo-maximo-art44-3-v20041101@v1

- leitor:a17: não tipável (nao_e_prazo_maximo): O prazo é da própria Comissão para publicar o anúncio, não um prazo máximo para os interessados apresentarem algo.
- leitor:b: não tipável (nao_e_prazo_maximo): O prazo é para a publicação de anúncios, não para apresentar elementos pelos interessados.

## regra:eu-2004-17:auto-prazo-minimo-art45-3-a-v20041101@v1

- leitor:a17: {"tipo": "prazo_minimo", "condicoes": [{"field": "tipo_procedimento", "op": "in", "value": ["concurso_limitado_previa_qualificacao", "procedimento_negociacao_com_concurso"]}], "params": {"minimum_days": 37, "deadline_field": "prazo_reclamacao_dias", "counted_from": "data_envio_anuncio", "usual_days": null}} || {"tipo": "prazo_minimo", "condicoes": [{"field": "tipo_procedimento", "op": "in", "value": ["concurso_limitado_previa_qualificacao", "procedimento_negociacao_com_concurso"]}], "params": {"minimum_days": 22, "deadline_field": "prazo_reclamacao_dias", "counted_from": "data_envio_anuncio", "usual_days": null}} || {"tipo": "prazo_minimo", "condicoes": [{"field": "tipo_procedimento", "op": "in", "value": ["concurso_limitado_previa_qualificacao", "procedimento_negociacao_com_concurso"]}], "params": {"minimum_days": 15, "deadline_field": "prazo_reclamacao_dias", "counted_from": "data_envio_anuncio", "usual_days": null}}
- leitor:b: não tipável (sem_vocabulario): O vocabulário não permite distinguir o envio do anúncio por meios electrónicos ou fax do envio por outros meios, condição que determina os mínimos de 15 ou 22 dias.
- verificador (A): regra 1, tipo_procedimento in ['concurso_limitado_previa_qualificacao', 'procedimento_negociacao_com_concurso']: as fontes não nomeiam ['procedimento_negociacao_com_concurso']; regra 1: deadline_field prazo_reclamacao_dias e as fontes dizem ['prazo_candidaturas_dias'] (L9); regra 1: counted_from data_envio_anuncio e as fontes dizem nada (L9); regra 2, tipo_procedimento in ['concurso_limitado_previa_qualificacao', 'procedimento_negociacao_com_concurso']: as fontes não nomeiam ['procedimento_negociacao_com_concurso']; regra 2: deadline_field prazo_reclamacao_dias e as fontes dizem ['prazo_candidaturas_dias'] (L9); regra 2: counted_from data_envio_anuncio e as fontes dizem nada (L9)

## regra:eu-2004-17:auto-prazo-minimo-art45-3-c-v20041101@v1

- leitor:a17: {"tipo": "prazo_minimo", "condicoes": [{"field": "tipo_procedimento", "op": "in", "value": ["concurso_limitado_previa_qualificacao", "procedimento_negociacao_com_concurso"]}], "params": {"minimum_days": 24, "deadline_field": "prazo_propostas_dias", "counted_from": "data_envio_convite", "usual_days": null}} || {"tipo": "prazo_minimo", "condicoes": [{"field": "tipo_procedimento", "op": "in", "value": ["concurso_limitado_previa_qualificacao", "procedimento_negociacao_com_concurso"]}], "params": {"minimum_days": 10, "deadline_field": "prazo_propostas_dias", "counted_from": "data_envio_convite", "usual_days": null}}
- leitor:b: não tipável (sem_vocabulario): Falta um campo que represente a impossibilidade de acordo sobre o prazo de recepção das propostas.
- verificador (A): regra 1, tipo_procedimento in ['concurso_limitado_previa_qualificacao', 'procedimento_negociacao_com_concurso']: as fontes não nomeiam ['procedimento_negociacao_com_concurso']; regra 1: counted_from data_envio_convite e as fontes dizem nada (L9); regra 2, tipo_procedimento in ['concurso_limitado_previa_qualificacao', 'procedimento_negociacao_com_concurso']: as fontes não nomeiam ['procedimento_negociacao_com_concurso']; regra 2: counted_from data_envio_convite e as fontes dizem nada (L9)

## regra:eu-2004-17:auto-prazo-minimo-art45-4-v20041101@v1

- leitor:a17: {"tipo": "prazo_minimo", "condicoes": [{"field": "anuncio_pre_informacao", "op": "eq", "value": true}, {"field": "tipo_procedimento", "op": "eq", "value": "concurso_publico"}], "params": {"minimum_days": 36, "deadline_field": "prazo_propostas_dias", "counted_from": "data_envio_anuncio", "usual_days": null}}
- leitor:b: não tipável (sem_vocabulario): O vocabulário não permite representar a condição de antecedência do envio do anúncio periódico indicativo relativamente ao envio do anúncio de concurso.

## regra:eu-2004-17:auto-prazo-maximo-art45-5-v20041101@v1

- leitor:a17: {"tipo": "prazo_maximo", "condicoes": [{"field": "tipo_procedimento", "op": "in", "value": ["concurso_limitado_previa_qualificacao", "concurso_publico", "procedimento_negociacao"]}], "params": {"maximum_days": 15, "deadline_field": "prazo_reclamacao_dias", "counted_from": "nao_indicado"}}
- leitor:b: não tipável (nao_e_prazo_maximo): A passagem permite uma redução dos prazos, mas não fixa um prazo máximo.
- verificador (A): regra 1, tipo_procedimento in ['concurso_limitado_previa_qualificacao', 'procedimento_negociacao', 'concurso_publico']: as fontes não nomeiam ['procedimento_negociacao']; regra 1: maximum_days 15 não está nas fontes (L8, L4); regra 1: deadline_field prazo_reclamacao_dias e as fontes dizem ['prazo_candidaturas_dias'] (L9)

## regra:eu-2004-17:auto-prazo-minimo-art45-7-v20041101@v1

- leitor:a17: não tipável (nao_e_prazo_minimo): O prazo é um máximo: 15 dias é o mínimo que não pode ser ultrapassado.
- leitor:b: não tipável (sem_vocabulario): Falta um campo para distinguir o envio do anúncio por fax ou por meios electrónicos do envio por outros meios, necessário para separar os mínimos de 15 e 22 dias.

## regra:eu-2004-17:auto-prazo-minimo-art45-8-v20041101@v1

- leitor:a17: não tipável (nao_e_prazo_minimo): O prazo é um máximo: não pode ser inferior a 15 dias.
- leitor:b: não tipável (sem_vocabulario): O vocabulário não permite representar a acumulação das reduções nem a exceção dos prazos fixados de comum acordo.

## regra:eu-2004-17:auto-prazo-maximo-art46-1-v20041101@v1

- leitor:a17: não tipável (nao_e_prazo_maximo): O prazo é da própria entidade adjudicante para enviar os documentos, não um prazo máximo para os operadores apresentarem algo.
- leitor:b: não tipável (nao_e_prazo_maximo): O prazo é para a entidade adjudicante enviar os cadernos de encargos e os documentos complementares aos operadores económicos.

## regra:eu-2004-17:auto-prazo-maximo-art49-4-v20041101@v1

- leitor:a17: não tipável (nao_e_prazo_maximo): O prazo é um máximo de 15 dias para a comunicação da decisão de qualificação, não um prazo para apresentar algo.
- leitor:b: não tipável (nao_e_prazo_maximo): O prazo destina-se à entidade adjudicante informar os requerentes da recusa de qualificação, não à apresentação de elementos pelos interessados.

## regra:eu-2004-17:auto-prazo-minimo-art49-5-v20041101@v1

- leitor:a17: não tipável (nao_e_prazo_minimo): O prazo é da própria entidade adjudicante para pôr termo à qualificação, não um prazo mínimo para os interessados apresentarem algo.
- leitor:b: não tipável (nao_e_prazo_minimo): O prazo é para a entidade adjudicante notificar a intenção de pôr termo à qualificação, não para apresentar algo.

## regra:eu-2004-17:auto-prazo-maximo-art56-4-v20041101@v1

- leitor:a17: não tipável (nao_e_prazo_maximo): O prazo é o da própria entidade adjudicante para iniciar o leilão, não um prazo máximo para os interessados apresentarem algo.
- leitor:b: não tipável (nao_e_prazo_maximo): A passagem fixa um prazo mínimo para o início do leilão electrónico, não um prazo máximo para apresentar elementos.

## regra:eu-2004-17:auto-limiar-art61-1-v20160101@v1

- leitor:a17: não tipável (nao_e_limiar): O valor delimita os concursos a que o título se aplica; não é o limite até ao qual um procedimento pode ser escolhido.
- leitor:b: não tipável (nao_e_limiar): O valor determina a aplicação do Título III, não um limite até ao qual um procedimento pode ser escolhido.

## regra:eu-2004-17:auto-limiar-art61-2-v20160101@v1

- leitor:a17: não tipável (nao_e_limiar): O valor soma prémios e pagamentos; não é o limite até ao qual um procedimento pode ser escolhido.
- leitor:b: não tipável (nao_e_limiar): O valor fixa o âmbito de aplicação do Título III, não um limite até ao qual um procedimento pode ser escolhido.

## regra:eu-2004-17:auto-limiar-art69-1-v20090807@v1

- leitor:a17: não tipável (nao_e_limiar): O valor dos limiares é revisto periodicamente pela Comissão; não é o limite até ao qual um procedimento pode ser escolhido.
- leitor:b: não tipável (nao_e_limiar): A passagem regula a verificação e revisão dos limiares, sem fixar um valor até ao qual um procedimento pode ser escolhido.

## regra:eu-2004-18:auto-limiar-art7-a-v20160101@v1

- leitor:a17: não tipável (nao_e_limiar): o valor não é o limite até ao qual um procedimento pode ser escolhido
- leitor:b: não tipável (nao_e_limiar): O valor delimita a aplicação da diretiva, não o limite até ao qual um procedimento pode ser escolhido.

## regra:eu-2004-18:auto-limiar-art7-b-v20160101@v1

- leitor:a17: não tipável (nao_e_limiar): O valor delimita os contratos a que a directiva se aplica; não é o limite até ao qual um procedimento pode ser escolhido.
- leitor:b: não tipável (nao_e_limiar): O valor delimita a aplicação da diretiva, não o valor até ao qual um procedimento pode ser escolhido.

## regra:eu-2004-18:auto-limiar-art7-c-v20160101@v1

- leitor:a17: não tipável (nao_e_limiar): O valor delimita os contratos a que a directiva se aplica; não é o limite até ao qual um procedimento pode ser escolhido.
- leitor:b: não tipável (nao_e_limiar): O montante delimita a aplicação da diretiva, não o valor até ao qual um procedimento pode ser escolhido.

## regra:eu-2004-18:auto-limiar-art9-4-a-v20040430@v1

- leitor:a17: não tipável (sem_vocabulario): A regra só vale para contratos de empreitada de obras públicas, e o vocabulário não tem um campo para o tipo de contrato.
- leitor:b: não tipável (nao_e_limiar): Os valores delimitam uma derrogação à aplicação da diretiva a lotes, sem fixarem um limite para a escolha de um procedimento.

## regra:eu-2004-18:auto-limiar-art9-4-b-v20040430@v1

- leitor:a17: não tipável (sem_vocabulario): A regra só vale para a adjudicação de lotes; o vocabulário não tem campo para o valor de vários lotes.
- leitor:b: não tipável (nao_e_limiar): O valor permite derrogar a aplicação da diretiva a certos lotes; não fixa um limite até ao qual um procedimento pode ser escolhido.

## regra:eu-2004-18:auto-limiar-art9-5-b-v20041101@v1

- leitor:a17: não tipável (sem_vocabulario): A regra depende do valor total dos lotes, soma de vários contratos, e o vocabulário não tem campo para somar lotes.
- leitor:b: não tipável (nao_e_limiar): O valor permite derrogar a aplicação da diretiva a certos lotes; não é um limite até ao qual um procedimento pode ser escolhido.

## regra:eu-2004-18:auto-prazo-maximo-art33-4-v20040430@v1

- leitor:a17: não tipável (sem_vocabulario): A regra é de um sistema de aquisição dinâmico, instrumento que o vocabulário não tem.
- leitor:b: não tipável (nao_e_prazo_maximo): O prazo é para a própria entidade adjudicante concluir a avaliação, não para apresentar elementos.

## regra:eu-2004-18:auto-limiar-art35-1-a-v20040430@v1

- leitor:a17: não tipável (sem_vocabulario): A regra limita-se aos acordos-quadro de fornecimentos por grupos de produtos, instrumento que o vocabulário não tem.
- leitor:b: não tipável (nao_e_limiar): O valor agrega vários contratos ou acordos-quadro para efeitos de pré-informação; não limita a escolha de um procedimento.

## regra:eu-2004-18:auto-limiar-art35-1-b-v20040430@v1

- leitor:a17: não tipável (nao_e_limiar): O valor delimita as categorias de serviços que podem ser abrangidas por um acordo-quadro; não é o limite até ao qual um procedimento pode ser escolhido.
- leitor:b: não tipável (nao_e_limiar): O valor agrega vários contratos para efeitos de anúncio de pré-informação; não limita a escolha de um procedimento.

## regra:eu-2004-18:auto-prazo-maximo-art36-3-v20040430@v1

- leitor:a17: não tipável (nao_e_prazo_maximo): O prazo é da própria entidade adjudicante para publicar os anúncios, não um prazo máximo para os interessados apresentarem algo.
- leitor:b: não tipável (nao_e_prazo_maximo): Os prazos respeitam à publicação dos anúncios, não à apresentação de elementos.

## regra:eu-2004-18:auto-prazo-minimo-art38-3-a-v20040430@v1

- leitor:a17: {"tipo": "prazo_minimo", "condicoes": [{"field": "tipo_procedimento", "op": "eq", "value": "concurso_limitado_previa_qualificacao"}], "params": {"minimum_days": 37, "deadline_field": "prazo_reclamacao_dias", "counted_from": "data_envio_anuncio", "usual_days": null}}
- leitor:b: {"tipo": "prazo_minimo", "condicoes": [{"field": "tipo_procedimento", "op": "in", "value": ["concurso_limitado_previa_qualificacao", "dialogo_concorrencial", "procedimento_negociacao_com_concurso"]}], "params": {"minimum_days": 37, "deadline_field": "prazo_candidaturas_dias", "counted_from": "data_envio_anuncio", "usual_days": null}}
- verificador (A): regra 1: deadline_field prazo_reclamacao_dias e as fontes dizem ['prazo_candidaturas_dias'] (L9)

## regra:eu-2004-18:auto-prazo-minimo-art38-4-v20040430@v1

- leitor:a17: {"tipo": "prazo_minimo", "condicoes": [{"field": "anuncio_pre_informacao", "op": "eq", "value": true}, {"field": "tipo_procedimento", "op": "eq", "value": "concurso_publico"}], "params": {"minimum_days": 36, "deadline_field": "prazo_propostas_dias", "counted_from": "data_envio_anuncio", "usual_days": null}} || {"tipo": "prazo_minimo", "condicoes": [{"field": "anuncio_pre_informacao", "op": "eq", "value": true}, {"field": "tipo_procedimento", "op": "in", "value": ["concurso_limitado_previa_qualificacao", "dialogo_concorrencial", "procedimento_concorrencial_negociacao"]}], "params": {"minimum_days": 22, "deadline_field": "prazo_propostas_dias", "counted_from": "data_envio_anuncio", "usual_days": null}}
- leitor:b: não tipável (sem_vocabulario): O vocabulário não permite representar as condições relativas ao conteúdo do anúncio de pré-informação e ao intervalo entre o seu envio e o envio do anúncio de concurso.
- verificador (A): regra 2, tipo_procedimento in ['concurso_limitado_previa_qualificacao', 'dialogo_concorrencial', 'procedimento_concorrencial_negociacao']: as fontes não nomeiam ['procedimento_concorrencial_negociacao']

## regra:eu-2004-18:auto-prazo-maximo-art38-5-v20040430@v1

- leitor:a17: {"tipo": "prazo_maximo", "condicoes": [{"field": "tipo_procedimento", "op": "in", "value": ["concurso_publico", "dialogo_concorrencial", "procedimento_negociacao_com_concurso"]}], "params": {"maximum_days": 39, "deadline_field": "prazo_propostas_dias", "counted_from": "nao_indicado"}} || {"tipo": "prazo_maximo", "condicoes": [{"field": "tipo_procedimento", "op": "eq", "value": "concurso_limitado_previa_qualificacao"}], "params": {"maximum_days": 43, "deadline_field": "prazo_propostas_dias", "counted_from": "data_envio_convite"}}
- leitor:b: não tipável (nao_e_prazo_maximo): A passagem reduz prazos mínimos de recepção de propostas e de pedidos de participação; não fixa um prazo máximo.
- verificador (A): regra 1, tipo_procedimento in ['concurso_publico', 'dialogo_concorrencial', 'procedimento_negociacao_com_concurso']: as fontes não nomeiam ['procedimento_negociacao_com_concurso']; regra 1: maximum_days 39 não está nas fontes (L8, L4); regra 1: nao_indicado, mas o texto diz ['data_envio_anuncio'] (L9); regra 2: maximum_days 43 não está nas fontes (L8, L4); regra 2: counted_from data_envio_convite e as fontes dizem nada (L9)

## regra:eu-2004-18:auto-prazo-maximo-art38-6-v20040430@v1

- leitor:a17: não tipável (nao_e_prazo_maximo): O prazo é uma redução, não um máximo.
- leitor:b: não tipável (nao_e_prazo_maximo): A passagem reduz prazos mínimos de recepção das propostas e não fixa um prazo máximo.

## regra:eu-2004-18:auto-prazo-minimo-art38-8-a-v20040430@v1

- leitor:a17: {"tipo": "prazo_minimo", "condicoes": [{"field": "tipo_procedimento", "op": "in", "value": ["concurso_limitado_previa_qualificacao", "procedimento_negociacao_com_concurso"]}], "params": {"minimum_days": 15, "deadline_field": "prazo_reclamacao_dias", "counted_from": "data_envio_anuncio", "usual_days": null}} || {"tipo": "prazo_minimo", "condicoes": [{"field": "publicado_joue", "op": "eq", "value": false}, {"field": "tipo_procedimento", "op": "in", "value": ["concurso_limitado_previa_qualificacao", "procedimento_negociacao_com_concurso"]}], "params": {"minimum_days": 15, "deadline_field": "prazo_reclamacao_dias", "counted_from": "data_envio_anuncio", "usual_days": null}}
- leitor:b: não tipável (sem_vocabulario): O vocabulário não permite representar o envio electrónico do anúncio nas condições indicadas, necessário para distinguir os mínimos de quinze e dez dias.
- verificador (A): regra 1: deadline_field prazo_reclamacao_dias e as fontes dizem ['prazo_candidaturas_dias'] (L9); regra 2, publicado_joue eq False: as fontes não negam o facto (L7); regra 2: deadline_field prazo_reclamacao_dias e as fontes dizem ['prazo_candidaturas_dias'] (L9)

## regra:eu-2004-18:auto-prazo-minimo-art38-8-b-v20040430@v1

- leitor:a17: não tipável (nao_e_prazo_minimo): O prazo é um mínimo para as entidades adjudicantes poderem fixar um prazo mais longo, não um prazo para os interessados apresentarem algo.
- leitor:b: não tipável (sem_vocabulario): Falta um campo que represente a urgência tornar impraticáveis os prazos mínimos, condição distinta de urgencia_fundamentada.

## regra:eu-2004-18:auto-prazo-maximo-art39-1-v20040430@v1

- leitor:a17: não tipável (nao_e_prazo_maximo): O prazo é da própria entidade adjudicante para enviar os documentos, não um prazo máximo para os operadores apresentarem algo.
- leitor:b: não tipável (nao_e_prazo_maximo): O prazo destina-se ao envio de documentos pela entidade adjudicante, não à apresentação de elementos pelos operadores económicos.

## regra:eu-2004-18:auto-prazo-maximo-art39-2-v20040430@v1

- leitor:a17: não tipável (nao_e_prazo_maximo): O prazo é um máximo das entidades adjudicantes para comunicarem as informações, não um prazo para os interessados apresentarem algo.
- leitor:b: não tipável (nao_e_prazo_maximo): O prazo é para a comunicação de informações complementares pelas entidades adjudicantes ou pelos serviços competentes.

## regra:eu-2004-18:auto-prazo-maximo-art40-4-v20040430@v1

- leitor:a17: não tipável (nao_e_prazo_maximo): O prazo é um máximo das entidades adjudicantes para comunicarem informações, não um prazo para os interessados apresentarem algo.
- leitor:b: não tipável (nao_e_prazo_maximo): O prazo é para a comunicação de informações pelas entidades adjudicantes ou pelos serviços competentes, não para apresentar elementos pelos interessados.

## regra:eu-2004-18:auto-prazo-maximo-art41-2-v20040430@v1

- leitor:a17: não tipável (nao_e_prazo_maximo): O prazo é um máximo de 15 dias para a própria entidade adjudicante prestar informações, não um prazo para os interessados apresentarem algo.
- leitor:b: não tipável (nao_e_prazo_maximo): O prazo é para a própria entidade adjudicante prestar informações.

## regra:eu-2004-18:auto-prazo-maximo-art54-4-v20040430@v1

- leitor:a17: não tipável (nao_e_prazo_maximo): O prazo é o da própria entidade adjudicante para iniciar o leilão, não um prazo máximo para os interessados apresentarem algo.
- leitor:b: não tipável (nao_e_prazo_maximo): A passagem fixa um intervalo mínimo para o início do leilão electrónico, não um prazo máximo para apresentar algo.

## regra:eu-2004-18:auto-limiar-art56-v20160101@v1

- leitor:a17: não tipável (nao_e_limiar): O valor delimita os contratos a que o capítulo se aplica; não é o limite até ao qual um procedimento pode ser escolhido.
- leitor:b: não tipável (nao_e_limiar): O valor delimita o âmbito de aplicação do capítulo, sem fixar um limite até ao qual um procedimento pode ser escolhido.

## regra:eu-2004-18:auto-prazo-minimo-art59-v20040430@v1

- leitor:a17: {"tipo": "prazo_minimo", "condicoes": [{"field": "tipo_contrato", "op": "eq", "value": "concessao_obras"}], "params": {"minimum_days": 52, "deadline_field": "prazo_candidaturas_dias", "counted_from": "data_envio_anuncio", "usual_days": null}}
- leitor:b: não tipável (sem_vocabulario): Falta no vocabulário a condição de os anúncios serem preparados e enviados por meios electrónicos, da qual depende a redução do prazo.

## regra:eu-2004-18:auto-limiar-art63-1-v20160101@v1

- leitor:a17: não tipável (nao_e_limiar): O valor é o de um contrato de empreitada de obras; falta um procedimento que se possa escolher até esse valor.
- leitor:b: não tipável (nao_e_limiar): O valor determina a aplicação de regras de publicidade, não o limite até ao qual um procedimento pode ser escolhido.

## regra:eu-2004-18:auto-prazo-minimo-art65-v20040430@v1

- leitor:a17: {"tipo": "prazo_minimo", "condicoes": [{"field": "tipo_contrato", "op": "eq", "value": "obras"}, {"field": "tipo_procedimento", "op": "in", "value": ["concurso_limitado_previa_qualificacao", "concurso_publico", "dialogo_concorrencial", "procedimento_negociacao"]}], "params": {"minimum_days": 40, "deadline_field": "prazo_propostas_dias", "counted_from": "data_envio_anuncio", "usual_days": null}} || {"tipo": "prazo_minimo", "condicoes": [{"field": "tipo_contrato", "op": "eq", "value": "obras"}, {"field": "tipo_procedimento", "op": "in", "value": ["concurso_limitado_previa_qualificacao", "concurso_publico", "dialogo_concorrencial", "procedimento_negociacao"]}], "params": {"minimum_days": 37, "deadline_field": "prazo_propostas_dias", "counted_from": "data_envio_anuncio", "usual_days": null}}
- leitor:b: não tipável (sem_vocabulario): O vocabulário não permite representar a qualidade de concessionário que não seja entidade adjudicante nem as condições de envio eletrónico dos anúncios e de acesso eletrónico à documentação que permitem reduzir os prazos.
- verificador (A): regra 1, tipo_procedimento in ['concurso_limitado_previa_qualificacao', 'concurso_publico', 'dialogo_concorrencial', 'procedimento_negociacao']: as fontes não nomeiam ['procedimento_negociacao']; regra 2, tipo_procedimento in ['concurso_limitado_previa_qualificacao', 'concurso_publico', 'dialogo_concorrencial', 'procedimento_negociacao']: as fontes não nomeiam ['procedimento_negociacao']

## regra:eu-2004-18:auto-limiar-art67-1-a-v20160101@v1

- leitor:a17: {"tipo": "limiar", "condicoes": [{"field": "tipo_contrato", "op": "eq", "value": "servicos"}, {"field": "tipo_procedimento", "op": "eq", "value": "concurso_concecao"}], "params": {"threshold": {"field": "valor_estimado", "comparator": "ge", "value": 135000, "currency": "EUR"}}}
- leitor:b: não tipável (nao_e_limiar): O valor determina a aplicação do título, não um limite até ao qual um procedimento pode ser escolhido.
- verificador (A): regra 1, tipo_contrato eq servicos: as fontes não nomeiam ['servicos']; regra 1, tipo_procedimento eq concurso_concecao: as fontes não nomeiam ['concurso_concecao']; regra 1: value 135000 não está nas fontes (L10)

## regra:eu-2004-18:auto-limiar-art67-1-b-v20160101@v1

- leitor:a17: {"tipo": "limiar", "condicoes": [{"field": "tipo_procedimento", "op": "eq", "value": "concurso_ideias"}], "params": {"threshold": {"field": "valor_estimado", "comparator": "ge", "value": 209000, "currency": "EUR"}}}
- leitor:b: não tipável (nao_e_limiar): O valor determina a aplicação do título, não um limite até ao qual um procedimento pode ser escolhido.
- verificador (A): regra 1, tipo_procedimento eq concurso_ideias: as fontes não nomeiam ['concurso_ideias']; regra 1: comparator ge e as fontes dizem ['gt'] (L8); regra 1: value 209000 não está nas fontes (L10)

## regra:eu-2004-18:auto-limiar-art67-1-c-v20160101@v1

- leitor:a17: não tipável (nao_e_limiar): O valor delimita os serviços a que o concurso se pode referir; não é o limite até ao qual um procedimento pode ser escolhido.
- leitor:b: não tipável (nao_e_limiar): O valor determina a aplicação das regras do título, não o limite até ao qual um procedimento pode ser escolhido.

## regra:eu-2004-18:auto-limiar-art78-1-v20090807@v1

- leitor:a17: não tipável (nao_e_limiar): O prazo é da Comissão para rever os limiares; não é um limite para os interessados apresentarem algo.
- leitor:b: não tipável (nao_e_limiar): A passagem regula a verificação e revisão dos limiares, sem fixar um valor até ao qual um procedimento pode ser escolhido.

## regra:eu-2004-18:auto-limiar-art78-3-v20040430@v1

- leitor:a17: não tipável (nao_e_limiar): O valor é o contravalor dos limiares em euros, não o limite até ao qual um procedimento pode ser escolhido.
- leitor:b: não tipável (nao_e_limiar): A passagem regula a revisão e o cálculo do contravalor dos limiares, sem fixar um limite de valor para a escolha de um procedimento.

## regra:eu-2009-81:auto-limiar-art8-a@v1

- leitor:a17: não tipável (sem_vocabulario): A regra é de um procedimento que usa uma central de compras, instrumento que o vocabulário não tem.
- leitor:b: não tipável (nao_e_limiar): O valor delimita a aplicação da diretiva, não o limite até ao qual um procedimento pode ser escolhido.

## regra:eu-2009-81:auto-limiar-art8-b@v1

- leitor:a17: não tipável (sem_vocabulario): A regra limita-se aos contratos de empreitada, instrumento que o vocabulário não tem.
- leitor:b: não tipável (nao_e_limiar): O valor delimita a aplicação da diretiva, não o limite até ao qual um procedimento pode ser escolhido.

## regra:eu-2009-81:auto-limiar-art9-4-a@v1

- leitor:a17: não tipável (sem_vocabulario): A regra só vale para a adjudicação de vários lotes; falta um campo do vocabulário para o valor de um lote.
- leitor:b: não tipável (nao_e_limiar): A passagem agrega o valor dos lotes e permite uma derrogação da aplicação da diretiva, sem fixar um limite de valor para a escolha de um procedimento.

## regra:eu-2009-81:auto-limiar-art9-4-b@v1

- leitor:a17: não tipável (nao_e_limiar): O valor é somado sobre vários lotes para aplicar o artigo 8.º; não é o limite até ao qual um lote pode ser escolhido.
- leitor:b: não tipável (nao_e_limiar): O valor permite dispensar a aplicação da directiva a determinados lotes; não limita a escolha de um procedimento.

## regra:eu-2009-81:auto-limiar-art9-5-b-v20100101@v1

- leitor:a17: não tipável (nao_e_limiar): O valor é somado sobre vários lotes para aplicar o artigo 8.º; não é o limite até ao qual um lote pode ser escolhido.
- leitor:b: não tipável (nao_e_limiar): O valor permite derrogar a aplicação da diretiva a determinados lotes; não fixa um limite para a escolha de um procedimento.

## regra:eu-2009-81:auto-prazo-maximo-art32-3@v1

- leitor:a17: não tipável (nao_e_prazo_maximo): O prazo é de 12 dias para os anúncios que não sejam enviados por meios eletrónicos em conformidade com o formato, e de 5 dias no caso do procedimento acelerado. Não é um prazo máximo para a apresentação de algo.
- leitor:b: não tipável (nao_e_prazo_maximo): Os prazos destinam-se à publicação de anúncios, não à apresentação de elementos pelos interessados.

## regra:eu-2009-81:auto-prazo-minimo-art33-2@v1

- leitor:a17: {"tipo": "prazo_minimo", "condicoes": [{"field": "tipo_procedimento", "op": "in", "value": ["concurso_limitado_previa_qualificacao", "dialogo_concorrencial", "procedimento_negociacao_com_concurso"]}], "params": {"minimum_days": 37, "deadline_field": "prazo_propostas_dias", "counted_from": "data_envio_anuncio", "usual_days": null}} || {"tipo": "prazo_minimo", "condicoes": [{"field": "tipo_procedimento", "op": "eq", "value": "concurso_limitado_previa_qualificacao"}], "params": {"minimum_days": 40, "deadline_field": "prazo_propostas_dias", "counted_from": "data_envio_convite", "usual_days": null}}
- leitor:b: {"tipo": "prazo_minimo", "condicoes": [{"field": "tipo_procedimento", "op": "eq", "value": "concurso_limitado_previa_qualificacao"}], "params": {"minimum_days": 40, "deadline_field": "prazo_propostas_dias", "counted_from": "data_envio_convite", "usual_days": null}}

## regra:eu-2009-81:auto-prazo-minimo-art33-3@v1

- leitor:a17: {"tipo": "prazo_minimo", "condicoes": [{"field": "publicado_joue", "op": "eq", "value": false}, {"field": "tipo_procedimento", "op": "in", "value": ["concurso_limitado_previa_qualificacao", "dialogo_concorrencial", "procedimento_negociacao_com_concurso"]}], "params": {"minimum_days": 22, "deadline_field": "prazo_propostas_dias", "counted_from": "data_envio_convite", "usual_days": null}} || {"tipo": "prazo_minimo", "condicoes": [{"field": "publicado_joue", "op": "eq", "value": false}, {"field": "tipo_procedimento", "op": "eq", "value": "concurso_limitado_previa_qualificacao"}], "params": {"minimum_days": 36, "deadline_field": "prazo_propostas_dias", "counted_from": "data_envio_convite", "usual_days": null}}
- leitor:b: não tipável (sem_vocabulario): O vocabulário não permite representar as condições relativas ao conteúdo do anúncio de pré-informação e à antecedência do seu envio para publicação.
- verificador (A): regra 1, publicado_joue eq False: as fontes não negam o facto (L7); regra 2, publicado_joue eq False: as fontes não negam o facto (L7)

## regra:eu-2009-81:auto-prazo-maximo-art33-4@v1

- leitor:a17: não tipável (nao_e_prazo_maximo): O prazo é reduzido em sete dias; falta um prazo máximo para apresentar algo.
- leitor:b: não tipável (nao_e_prazo_maximo): A passagem reduz um prazo mínimo, não fixa um prazo máximo.

## regra:eu-2009-81:auto-prazo-maximo-art33-5@v1

- leitor:a17: não tipável (nao_e_prazo_maximo): O prazo é uma redução, não um máximo.
- leitor:b: não tipável (nao_e_prazo_maximo): A passagem reduz um prazo mínimo de recepção das propostas e não fixa um prazo máximo.

## regra:eu-2009-81:auto-prazo-minimo-art33-7@v1

- leitor:a17: não tipável (sem_vocabulario): A regra só vale por urgência e não é um prazo para apresentar algo.
- leitor:b: não tipável (sem_vocabulario): Falta um campo para representar o envio do anúncio por meios electrónicos, condição que distingue os mínimos de 15 e 10 dias para os pedidos de participação.

## regra:eu-2009-81:auto-prazo-maximo-art34-4@v1

- leitor:a17: não tipável (nao_e_prazo_maximo): O prazo é um máximo das entidades adjudicantes para comunicarem informações, não um prazo para os interessados apresentarem algo.
- leitor:b: não tipável (nao_e_prazo_maximo): O prazo é para as autoridades/entidades adjudicantes ou os serviços competentes comunicarem informações complementares.

## regra:eu-2009-81:auto-prazo-minimo-art57-2@v1

- leitor:a17: não tipável (nao_e_prazo_minimo): O prazo é de 10 dias antes da celebração do contrato, não um prazo para apresentar algo.
- leitor:b: não tipável (nao_e_prazo_minimo): O prazo suspensivo limita a celebração do contrato, não sendo um prazo para apresentar algo.

## regra:eu-2009-81:auto-prazo-minimo-art59@v1

- leitor:a17: não tipável (sem_vocabulario): O prazo é fixado em dias consecutivos, unidade que o vocabulário não tem.
- leitor:b: não tipável (sem_vocabulario): O vocabulário não prevê um campo de prazo para a interposição de recurso.
- verificador (B): não tipável: «Prazos para interposição de recurso» não está em eu-2009-81:art59

## regra:eu-2009-81:auto-prazo-minimo-art60-4@v1

- leitor:a17: não tipável (nao_e_prazo_minimo): O prazo é de 10 dias antes de um contrato não ser celebrado, não um prazo para apresentar algo.
- leitor:b: não tipável (nao_e_prazo_minimo): O prazo refere-se à celebração do contrato, não à apresentação de qualquer elemento.

## regra:eu-2009-81:auto-prazo-minimo-art60-5@v1

- leitor:a17: não tipável (nao_e_prazo_minimo): O prazo é de 10 dias consecutivos antes de celebrar o contrato, não um prazo para apresentar algo.
- leitor:b: não tipável (nao_e_prazo_minimo): O prazo é de espera para a celebração do contrato, não para apresentar algo.

## regra:eu-2009-81:auto-prazo-maximo-art63-3@v1

- leitor:a17: não tipável (nao_e_prazo_maximo): O prazo é de 30 dias, contados da data de recepção da notificação, para comunicar algo à Comissão; falta um prazo máximo para os interessados apresentarem algo.
- leitor:b: não tipável (nao_e_prazo_maximo): O prazo destina-se à comunicação do Estado-Membro à Comissão, não à apresentação de elementos num procedimento de contratação.

## regra:eu-2014-23:auto-limiar-art8-1@v1

- leitor:a17: não tipável (nao_e_limiar): O valor delimita o âmbito de aplicação da diretiva; não é o limite até ao qual um procedimento pode ser escolhido.
- leitor:b: não tipável (nao_e_limiar): O valor delimita o âmbito de aplicação da diretiva, não o limite até ao qual um procedimento pode ser escolhido.

## regra:eu-2014-23:auto-limiar-art9-1@v1

- leitor:a17: não tipável (nao_e_limiar): O valor é revisto pela Comissão e corresponde ao GPA; não é o limite até ao qual um procedimento pode ser escolhido.
- leitor:b: não tipável (nao_e_limiar): A passagem estabelece a revisão e o cálculo do limiar, sem fixar um valor até ao qual um procedimento pode ser escolhido.

## regra:eu-2014-23:auto-limiar-art9-2@v1

- leitor:a17: não tipável (nao_e_limiar): O valor é o contravalor do limiar em moedas que não são o euro; não é o limite até ao qual um procedimento pode ser escolhido.
- leitor:b: não tipável (nao_e_limiar): A passagem regula a determinação do contravalor dos limiares, sem fixar um limite de valor para a escolha de um procedimento.

## regra:eu-2014-23:auto-prazo-maximo-art32-1@v1

- leitor:a17: não tipável (nao_e_prazo_maximo): O prazo é da própria entidade adjudicante para enviar o anúncio de adjudicação, não um prazo máximo para os interessados apresentarem algo.
- leitor:b: não tipável (nao_e_prazo_maximo): Os prazos são para o envio de anúncios pelas próprias autoridades e entidades adjudicantes, não para apresentar elementos pelos participantes.

## regra:eu-2014-23:auto-prazo-maximo-art33-2@v1

- leitor:a17: {"tipo": "prazo_maximo", "condicoes": [], "params": {"maximum_days": 5, "deadline_field": "prazo_propostas_dias", "counted_from": "data_envio_anuncio"}}
- leitor:b: não tipável (nao_e_prazo_maximo): O prazo é para a publicação dos anúncios, não para apresentar algo.
- verificador (A): regra 1: deadline_field prazo_propostas_dias e as fontes dizem nada (L9)

## regra:eu-2014-23:auto-prazo-minimo-art39-3@v1

- leitor:a17: {"tipo": "prazo_minimo", "condicoes": [{"field": "tipo_contrato", "op": "eq", "value": "concessao_obras"}], "params": {"minimum_days": 30, "deadline_field": "prazo_propostas_dias", "counted_from": "data_envio_anuncio", "usual_days": null}}
- leitor:b: {"tipo": "prazo_minimo", "condicoes": [], "params": {"minimum_days": 30, "deadline_field": "prazo_candidaturas_dias", "counted_from": "data_envio_anuncio", "usual_days": null}}
- verificador (A): regra 1, tipo_contrato eq concessao_obras: as fontes não nomeiam ['concessao_obras']; regra 1: deadline_field prazo_propostas_dias e as fontes dizem ['prazo_candidaturas_dias'] (L9)

## regra:eu-2014-23:auto-prazo-minimo-art39-4@v1

- leitor:a17: {"tipo": "prazo_minimo", "condicoes": [{"field": "tipo_contrato", "op": "eq", "value": "concessao_obras"}, {"field": "tipo_procedimento", "op": "eq", "value": "concurso_publico"}], "params": {"minimum_days": 22, "deadline_field": "prazo_propostas_dias", "counted_from": "data_envio_convite", "usual_days": null}}
- leitor:b: não tipável (sem_vocabulario): O vocabulário não permite representar a condição de o procedimento se desenrolar em fases sucessivas.
- verificador (A): regra 1, tipo_contrato eq concessao_obras: as fontes não nomeiam ['concessao_obras']; regra 1, tipo_procedimento eq concurso_publico: as fontes não nomeiam ['concurso_publico']

## regra:eu-2014-23:auto-prazo-maximo-art39-5@v1

- leitor:a17: não tipável (nao_e_prazo_maximo): O prazo é um máximo que pode ser reduzido em 5 dias, não um prazo para apresentar algo.
- leitor:b: não tipável (nao_e_prazo_maximo): A passagem prevê uma redução do prazo de receção das propostas, sem fixar um prazo máximo.

## regra:eu-2014-23:auto-prazo-maximo-art40-1@v1

- leitor:a17: não tipável (nao_e_prazo_maximo): O prazo é da própria entidade adjudicante para informar, não um prazo máximo para os interessados apresentarem algo.
- leitor:b: não tipável (nao_e_prazo_maximo): O prazo é para a própria autoridade ou entidade adjudicante prestar informações, não para apresentar elementos.

## regra:eu-2014-24:auto-limiar-art4-a@v1

- leitor:a17: não tipável (nao_e_limiar): O valor delimita os contratos a que a diretiva se aplica; não é o limite até ao qual um procedimento pode ser escolhido.
- leitor:b: não tipável (nao_e_limiar): O montante delimita a aplicação da diretiva, sem fixar um valor até ao qual um procedimento pode ser escolhido.

## regra:eu-2014-24:auto-limiar-art4-b@v1

- leitor:a17: não tipável (nao_e_limiar): O valor delimita os contratos a que a diretiva se aplica; não é o limite até ao qual um procedimento pode ser escolhido.
- leitor:b: não tipável (nao_e_limiar): O valor fixa o âmbito de aplicação da diretiva, não o limite até ao qual um procedimento pode ser escolhido.

## regra:eu-2014-24:auto-limiar-art4-c@v1

- leitor:a17: não tipável (nao_e_limiar): O valor delimita os contratos a que a diretiva se aplica; não é o limite até ao qual um procedimento pode ser escolhido.
- leitor:b: não tipável (nao_e_limiar): O valor delimita o âmbito de aplicação da diretiva, não o limite até ao qual um procedimento pode ser escolhido.

## regra:eu-2014-24:auto-limiar-art4-d@v1

- leitor:a17: não tipável (nao_e_limiar): O valor delimita os contratos a que a diretiva se aplica; não é o limite até ao qual um procedimento pode ser escolhido.
- leitor:b: não tipável (nao_e_limiar): O valor delimita o âmbito de aplicação da diretiva, não o limite até ao qual um procedimento pode ser escolhido.

## regra:eu-2014-24:auto-limiar-art5-10@v1

- leitor:a17: não tipável (nao_e_limiar): O valor delimita os lotes que ficam fora da aplicação da diretiva; não é o limite até ao qual um procedimento pode ser escolhido.
- leitor:b: não tipável (nao_e_limiar): A passagem prevê uma dispensa de aplicação dos procedimentos da diretiva a certos lotes, sem fixar um limite de valor para a escolha de um procedimento.

## regra:eu-2014-24:auto-limiar-art6-1@v1

- leitor:a17: não tipável (nao_e_limiar): O valor é revisto periodicamente pela Comissão; não é o limite até ao qual um procedimento pode ser escolhido.
- leitor:b: não tipável (nao_e_limiar): A passagem regula o cálculo e a revisão dos limiares, sem fixar um limite de valor até ao qual um procedimento pode ser escolhido.

## regra:eu-2014-24:auto-limiar-art6-3@v1

- leitor:a17: não tipável (nao_e_limiar): O valor é o contravalor de um limiar em moeda que não seja o euro; não é o limite até ao qual um procedimento pode ser escolhido.
- leitor:b: não tipável (nao_e_limiar): A passagem regula a determinação do contravalor dos limiares, sem fixar um limite de valor para a escolha de um procedimento.

## regra:eu-2014-24:auto-limiar-art13-a@v1

- leitor:a17: não tipável (nao_e_limiar): O valor delimita os contratos que podem ser subsidiados; não é o limite até ao qual um procedimento pode ser escolhido.
- leitor:b: não tipável (nao_e_limiar): O valor delimita a aplicação da diretiva, sem fixar um limite até ao qual um procedimento pode ser escolhido.

## regra:eu-2014-24:auto-prazo-minimo-art27-2-b@v1

- leitor:a17: {"tipo": "prazo_minimo", "condicoes": [{"field": "anuncio_pre_informacao", "op": "eq", "value": true}, {"field": "publicado_joue", "op": "eq", "value": true}, {"field": "tipo_procedimento", "op": "eq", "value": "concurso_aberto"}, {"field": "urgencia_fundamentada", "op": "eq", "value": false}], "params": {"minimum_days": 15, "deadline_field": "prazo_propostas_dias", "counted_from": "data_envio_anuncio", "usual_days": null}}
- leitor:b: não tipável (nao_e_prazo_minimo): A passagem fixa a antecedência do envio de um anúncio pela entidade adjudicante, não um prazo para apresentar propostas.
- verificador (A): regra 1, publicado_joue eq True: as fontes não afirmam o facto (L7); regra 1, urgencia_fundamentada eq False: as fontes não negam o facto (L7)

## regra:eu-2014-24:auto-prazo-minimo-art27-3@v1

- leitor:a17: {"tipo": "prazo_minimo", "condicoes": [{"field": "tipo_procedimento", "op": "eq", "value": "concurso_aberto"}, {"field": "urgencia_fundamentada", "op": "eq", "value": true}], "params": {"minimum_days": 15, "deadline_field": "prazo_propostas_dias", "counted_from": "data_envio_anuncio", "usual_days": null}}
- leitor:b: não tipável (sem_vocabulario): O vocabulário não permite representar a condição de a urgência inviabilizar o cumprimento do prazo fixado no n.º 1.

## regra:eu-2014-24:auto-prazo-maximo-art27-4@v1

- leitor:a17: não tipável (nao_e_prazo_maximo): O prazo é reduzido em cinco dias; falta um prazo máximo para os casos em que a apresentação possa ser feita por meios eletrónicos.
- leitor:b: não tipável (nao_e_prazo_maximo): A passagem reduz um prazo mínimo, não fixa um prazo máximo.

## regra:eu-2014-24:auto-prazo-minimo-art28-1@v1

- leitor:a17: {"tipo": "prazo_minimo", "condicoes": [{"field": "tipo_procedimento", "op": "eq", "value": "concurso_limitado_previa_qualificacao"}], "params": {"minimum_days": 30, "deadline_field": "prazo_candidaturas_dias", "counted_from": "data_envio_anuncio", "usual_days": null}}
- leitor:b: não tipável (sem_vocabulario): O vocabulário não permite distinguir se o anúncio de pré-informação é utilizado como meio de abertura de concurso, facto que determina o início da contagem do prazo.

## regra:eu-2014-24:auto-prazo-minimo-art28-2@v1

- leitor:a17: {"tipo": "prazo_minimo", "condicoes": [{"field": "tipo_procedimento", "op": "eq", "value": "concurso_limitado_previa_qualificacao"}], "params": {"minimum_days": 30, "deadline_field": "prazo_propostas_dias", "counted_from": "data_envio_convite", "usual_days": null}}
- leitor:b: {"tipo": "prazo_minimo", "condicoes": [{"field": "tipo_procedimento", "op": "eq", "value": "concurso_limitado_previa_qualificacao"}], "params": {"minimum_days": 30, "deadline_field": "prazo_propostas_dias", "counted_from": "data_envio_convite", "usual_days": null}}
- verificador (A): regra 1, tipo_procedimento eq concurso_limitado_previa_qualificacao: as fontes não nomeiam ['concurso_limitado_previa_qualificacao']

## regra:eu-2014-24:auto-prazo-minimo-art28-3-b@v1

- leitor:a17: não tipável (nao_e_prazo_minimo): O prazo é de 30 dias, o mínimo para a receção das propostas, e não um prazo para apresentar algo.
- leitor:b: não tipável (sem_vocabulario): O vocabulário não permite representar o intervalo exigido entre o envio do anúncio de pré-informação e o envio do anúncio de concurso, condição da redução do prazo para 10 dias.

## regra:eu-2014-24:auto-prazo-minimo-art28-4@v1

- leitor:a17: {"tipo": "prazo_minimo", "condicoes": [{"field": "tipo_procedimento", "op": "eq", "value": "concurso_limitado_previa_qualificacao"}], "params": {"minimum_days": 10, "deadline_field": "prazo_propostas_dias", "counted_from": "data_envio_convite", "usual_days": null}}
- leitor:b: não tipável (sem_vocabulario): Faltam condições no vocabulário para representar as autoridades adjudicantes subcentrais e a falta de acordo com os candidatos selecionados sobre o prazo.
- verificador (A): regra 1, tipo_procedimento eq concurso_limitado_previa_qualificacao: as fontes não nomeiam ['concurso_limitado_previa_qualificacao']; regra 1: counted_from data_envio_convite e as fontes dizem nada (L9)

## regra:eu-2014-24:auto-prazo-maximo-art28-5@v1

- leitor:a17: não tipável (nao_e_prazo_maximo): O prazo é de 10 dias, menos 5 do que o mínimo do n.º 2, e não um máximo.
- leitor:b: não tipável (nao_e_prazo_maximo): A passagem reduz um prazo mínimo, não fixa um prazo máximo.

## regra:eu-2014-24:auto-prazo-minimo-art28-6-a@v1

- leitor:a17: {"tipo": "prazo_minimo", "condicoes": [{"field": "tipo_procedimento", "op": "eq", "value": "concurso_limitado_previa_qualificacao"}], "params": {"minimum_days": 15, "deadline_field": "prazo_propostas_dias", "counted_from": "data_envio_anuncio", "usual_days": null}}
- leitor:b: não tipável (sem_vocabulario): Falta um campo para representar a condição de a urgência inviabilizar o cumprimento dos prazos fixados no artigo.
- verificador (A): regra 1, tipo_procedimento eq concurso_limitado_previa_qualificacao: as fontes não nomeiam ['concurso_limitado_previa_qualificacao']; regra 1: deadline_field prazo_propostas_dias e as fontes dizem ['prazo_candidaturas_dias'] (L9)

## regra:eu-2014-24:auto-prazo-minimo-art28-6-b@v1

- leitor:a17: {"tipo": "prazo_minimo", "condicoes": [{"field": "tipo_procedimento", "op": "eq", "value": "concurso_limitado_previa_qualificacao"}], "params": {"minimum_days": 10, "deadline_field": "prazo_propostas_dias", "counted_from": "data_envio_convite", "usual_days": null}}
- leitor:b: {"tipo": "prazo_minimo", "condicoes": [{"field": "tipo_procedimento", "op": "eq", "value": "concurso_limitado_previa_qualificacao"}, {"field": "urgencia_fundamentada", "op": "eq", "value": true}], "params": {"minimum_days": 10, "deadline_field": "prazo_propostas_dias", "counted_from": "data_envio_convite", "usual_days": null}}
- verificador (A): regra 1, tipo_procedimento eq concurso_limitado_previa_qualificacao: as fontes não nomeiam ['concurso_limitado_previa_qualificacao']

## regra:eu-2014-24:auto-prazo-minimo-art29-1@v1

- leitor:a17: {"tipo": "prazo_minimo", "condicoes": [{"field": "tipo_procedimento", "op": "eq", "value": "procedimento_concorrencial_negociacao"}], "params": {"minimum_days": 30, "deadline_field": "prazo_candidaturas_dias", "counted_from": "data_envio_anuncio", "usual_days": null}}
- leitor:b: não tipável (texto_em_falta): Falta o texto dos n.os 3 a 6 do artigo 28.º, declarado aplicável, para determinar os prazos mínimos e as respetivas condições.

## regra:eu-2014-24:auto-prazo-minimo-art30-1@v1

- leitor:a17: {"tipo": "prazo_minimo", "condicoes": [{"field": "tipo_procedimento", "op": "eq", "value": "dialogo_concorrencial"}], "params": {"minimum_days": 30, "deadline_field": "prazo_candidaturas_dias", "counted_from": "data_envio_anuncio", "usual_days": null}}
- leitor:b: {"tipo": "prazo_minimo", "condicoes": [{"field": "tipo_procedimento", "op": "eq", "value": "dialogo_concorrencial"}], "params": {"minimum_days": 30, "deadline_field": "prazo_candidaturas_dias", "counted_from": "data_envio_anuncio", "usual_days": null}}
- verificador (A): regra 1, tipo_procedimento eq dialogo_concorrencial: as fontes não nomeiam ['dialogo_concorrencial']
- verificador (B): regra 1, tipo_procedimento eq dialogo_concorrencial: as fontes não nomeiam ['dialogo_concorrencial']

## regra:eu-2014-24:auto-prazo-minimo-art31-1@v1

- leitor:a17: {"tipo": "prazo_minimo", "condicoes": [{"field": "tipo_procedimento", "op": "eq", "value": "parceria_inovacao"}], "params": {"minimum_days": 30, "deadline_field": "prazo_candidaturas_dias", "counted_from": "data_envio_anuncio", "usual_days": null}}
- leitor:b: {"tipo": "prazo_minimo", "condicoes": [{"field": "tipo_procedimento", "op": "eq", "value": "parceria_inovacao"}], "params": {"minimum_days": 30, "deadline_field": "prazo_candidaturas_dias", "counted_from": "data_envio_anuncio", "usual_days": null}}

## regra:eu-2014-24:auto-prazo-maximo-art34-5@v1

- leitor:a17: não tipável (sem_vocabulario): A contagem do prazo é em dias úteis, unidade que o vocabulário não tem.
- leitor:b: não tipável (nao_e_prazo_maximo): A passagem fixa prazos para a própria entidade adjudicante avaliar pedidos e comunicar a admissão, não para apresentar algo.

## regra:eu-2014-24:auto-prazo-minimo-art47-3-a@v1

- leitor:a17: não tipável (nao_e_prazo_minimo): O prazo é de prorrogação quando faltem informações; falta um prazo mínimo para apresentar algo.
- leitor:b: não tipável (nao_e_prazo_minimo): A passagem fixa uma condição de prorrogação relativa ao fornecimento de informações adicionais pela entidade adjudicante.

## regra:eu-2014-24:auto-prazo-maximo-art48-2-d@v1

- leitor:a17: não tipável (nao_e_prazo_maximo): O prazo é o da publicação do anúncio de pré-informação, não um prazo para os interessados apresentarem algo.
- leitor:b: não tipável (nao_e_prazo_maximo): O limite fixa o período abrangido pelo anúncio de pré-informação, não um prazo para apresentar algo.

## regra:eu-2014-24:auto-prazo-maximo-art50-1@v1

- leitor:a17: não tipável (nao_e_prazo_maximo): O prazo é das próprias autoridades adjudicantes para enviarem o anúncio de adjudicação, não um prazo máximo para os interessados apresentarem algo.
- leitor:b: não tipável (nao_e_prazo_maximo): O prazo é para a própria entidade adjudicante enviar o anúncio de adjudicação do contrato.

## regra:eu-2014-24:auto-prazo-maximo-art50-2@v1

- leitor:a17: não tipável (nao_e_prazo_maximo): O prazo é de 30 dias para publicar um anúncio de adjudicação com indicação, não um prazo máximo para os interessados apresentarem algo.
- leitor:b: não tipável (nao_e_prazo_maximo): O prazo é para a própria entidade adjudicante enviar os anúncios agrupados.

## regra:eu-2014-24:auto-prazo-maximo-art50-3@v1

- leitor:a17: não tipável (sem_vocabulario): A regra é de um sistema de aquisição dinâmico, instrumento que o vocabulário não tem.
- leitor:b: não tipável (nao_e_prazo_maximo): Os prazos são para a própria autoridade adjudicante enviar anúncios de adjudicação.

## regra:eu-2014-24:auto-prazo-maximo-art51-2@v1

- leitor:a17: não tipável (nao_e_prazo_maximo): O prazo é da própria entidade adjudicante para publicar o anúncio, não um prazo máximo para os interessados apresentarem algo.
- leitor:b: não tipável (nao_e_prazo_maximo): O prazo é para a publicação dos anúncios, não para apresentar elementos.

## regra:eu-2014-24:auto-prazo-maximo-art53-1@v1

- leitor:a17: não tipável (nao_e_prazo_maximo): O prazo é o da disponibilização dos documentos do concurso, não um prazo para os interessados apresentarem algo.
- leitor:b: não tipável (nao_e_prazo_maximo): A passagem fixa uma prorrogação de cinco dias, sem estabelecer um prazo máximo para a apresentação de propostas.

## regra:eu-2014-24:auto-prazo-maximo-art53-2@v1

- leitor:a17: não tipável (nao_e_prazo_maximo): O prazo é um máximo da própria entidade adjudicante para comunicar informações, não um prazo para os concorrentes apresentarem algo.
- leitor:b: não tipável (nao_e_prazo_maximo): O prazo é para a própria entidade adjudicante comunicar informações adicionais aos concorrentes.

## regra:eu-2014-24:auto-prazo-maximo-art55-2@v1

- leitor:a17: não tipável (nao_e_prazo_maximo): O prazo é da própria entidade adjudicante para comunicar, não um prazo máximo para os interessados apresentarem algo.
- leitor:b: não tipável (nao_e_prazo_maximo): O prazo é para a própria entidade adjudicante comunicar informações.

## regra:eu-2014-25:auto-limiar-art15-a@v1

- leitor:a17: não tipável (nao_e_limiar): O valor delimita os contratos a que a diretiva se aplica; não é o limite até ao qual um procedimento pode ser escolhido.
- leitor:b: não tipável (nao_e_limiar): O valor delimita a aplicação da diretiva, não fixa um limite até ao qual um procedimento pode ser escolhido.

## regra:eu-2014-25:auto-limiar-art15-b@v1

- leitor:a17: {"tipo": "limiar", "condicoes": [{"field": "tipo_contrato", "op": "eq", "value": "obras"}, {"field": "tipo_procedimento", "op": "eq", "value": "concurso_concecao"}], "params": {"threshold": {"field": "valor_estimado", "comparator": "ge", "value": 5404000, "currency": "EUR"}}}
- leitor:b: não tipável (nao_e_limiar): O valor delimita a aplicação da diretiva, não o valor até ao qual um procedimento pode ser escolhido.
- verificador (A): regra 1, tipo_procedimento in ['concurso_concecao']: as fontes não nomeiam ['concurso_concecao']; regra 1: value 5404000 não está nas fontes (L10)

## regra:eu-2014-25:auto-limiar-art15-c@v1

- leitor:a17: não tipável (nao_e_limiar): O valor delimita os contratos a que a diretiva se aplica; não é o limite até ao qual um procedimento pode ser escolhido.
- leitor:b: não tipável (nao_e_limiar): O valor delimita o âmbito de aplicação da diretiva, não o limite até ao qual um procedimento pode ser escolhido.

## regra:eu-2014-25:auto-limiar-art16-10@v1

- leitor:a17: não tipável (nao_e_limiar): O valor delimita os lotes que ficam fora da aplicação da diretiva; não é o limite até ao qual um procedimento pode ser escolhido.
- leitor:b: não tipável (nao_e_limiar): Os valores delimitam uma dispensa de aplicação dos procedimentos da diretiva, não um limite até ao qual um procedimento pode ser escolhido.

## regra:eu-2014-25:auto-limiar-art17-1@v1

- leitor:a17: não tipável (nao_e_limiar): O valor é revisto pela Comissão; não é o limite até ao qual um procedimento pode ser escolhido.
- leitor:b: não tipável (nao_e_limiar): A passagem estabelece um método de revisão dos limiares, sem fixar um valor até ao qual um procedimento pode ser escolhido.

## regra:eu-2014-25:auto-limiar-art17-2@v1

- leitor:a17: não tipável (nao_e_limiar): O valor é o contravalor dos limiares em euros, não o limite até ao qual um procedimento pode ser escolhido.
- leitor:b: não tipável (nao_e_limiar): A passagem regula a determinação do contravalor dos limiares em moedas nacionais, sem fixar um limite de valor para a escolha de um procedimento.

## regra:eu-2014-25:auto-prazo-minimo-art45-1@v1

- leitor:a17: {"tipo": "prazo_minimo", "condicoes": [{"field": "tipo_procedimento", "op": "eq", "value": "concurso_aberto"}], "params": {"minimum_days": 35, "deadline_field": "prazo_propostas_dias", "counted_from": "data_envio_anuncio", "usual_days": null}}
- leitor:b: {"tipo": "prazo_minimo", "condicoes": [{"field": "tipo_procedimento", "op": "eq", "value": "concurso_aberto"}], "params": {"minimum_days": 35, "deadline_field": "prazo_propostas_dias", "counted_from": "data_envio_anuncio", "usual_days": null}}

## regra:eu-2014-25:auto-prazo-minimo-art45-2-b@v1

- leitor:a17: não tipável (nao_e_prazo_minimo): O prazo é fixado em função do momento em que o anúncio periódico indicativo é enviado, não um prazo para apresentar algo.
- leitor:b: não tipável (nao_e_prazo_minimo): A passagem fixa a antecedência do envio do anúncio periódico indicativo pela entidade adjudicante, sem fixar um prazo mínimo para apresentação de elementos pelos interessados.

## regra:eu-2014-25:auto-prazo-minimo-art45-3@v1

- leitor:a17: {"tipo": "prazo_minimo", "condicoes": [{"field": "tipo_procedimento", "op": "eq", "value": "concurso_publico"}, {"field": "urgencia_fundamentada", "op": "eq", "value": true}], "params": {"minimum_days": 15, "deadline_field": "prazo_propostas_dias", "counted_from": "data_envio_anuncio", "usual_days": null}}
- leitor:b: {"tipo": "prazo_minimo", "condicoes": [{"field": "tipo_procedimento", "op": "eq", "value": "concurso_aberto"}, {"field": "urgencia_fundamentada", "op": "eq", "value": true}], "params": {"minimum_days": 15, "deadline_field": "prazo_propostas_dias", "counted_from": "data_envio_anuncio", "usual_days": null}}

## regra:eu-2014-25:auto-prazo-maximo-art45-4@v1

- leitor:a17: não tipável (nao_e_prazo_maximo): O prazo é reduzido em cinco dias; falta um prazo máximo para os quais os 15 dias sejam o máximo.
- leitor:b: não tipável (nao_e_prazo_maximo): A passagem reduz um prazo mínimo de receção de propostas, não fixa um prazo máximo.
- verificador (B): não tipável: fonte em eu-2014-25:art45.1, que é vizinho (L1)

## regra:eu-2014-25:auto-prazo-minimo-art46-1@v1

- leitor:a17: {"tipo": "prazo_minimo", "condicoes": [{"field": "tipo_procedimento", "op": "eq", "value": "concurso_limitado_previa_qualificacao"}], "params": {"minimum_days": 15, "deadline_field": "prazo_candidaturas_dias", "counted_from": "data_envio_anuncio", "usual_days": 30}}
- leitor:b: não tipável (sem_vocabulario): O vocabulário não permite representar o início alternativo da contagem nem distinguir os casos de envio do anúncio e de envio do convite à confirmação de interesse.
- verificador (A): regra 1: usual_days sem «em regra» e os dias nas fontes (L11)

## regra:eu-2014-25:auto-prazo-minimo-art46-2@v1

- leitor:a17: não tipável (nao_e_prazo_minimo): O prazo é de 10 dias, no mínimo, para a receção das propostas, não um prazo para apresentar algo.
- leitor:b: não tipável (sem_vocabulario): Falta no vocabulário uma condição que represente a ausência de acordo sobre o prazo de receção das propostas.

## regra:eu-2014-25:auto-prazo-minimo-art47-1@v1

- leitor:a17: {"tipo": "prazo_minimo", "condicoes": [{"field": "tipo_procedimento", "op": "eq", "value": "procedimento_negociacao_com_concurso"}], "params": {"minimum_days": 30, "deadline_field": "prazo_candidaturas_dias", "counted_from": "data_envio_anuncio", "usual_days": null}} || {"tipo": "prazo_minimo", "condicoes": [{"field": "anuncio_pre_informacao", "op": "eq", "value": true}, {"field": "tipo_procedimento", "op": "eq", "value": "procedimento_negociacao_com_concurso"}], "params": {"minimum_days": 15, "deadline_field": "prazo_candidaturas_dias", "counted_from": "data_envio_anuncio", "usual_days": null}}
- leitor:b: não tipável (sem_vocabulario): Falta uma condição que distinga a utilização do anúncio periódico indicativo como meio de abertura de concurso da sua mera publicação, pois essa utilização determina o início da contagem.

## regra:eu-2014-25:auto-prazo-minimo-art47-2@v1

- leitor:a17: não tipável (nao_e_prazo_minimo): O prazo é de 10 dias no mínimo para a receção das propostas, não um prazo para apresentar algo.
- leitor:b: não tipável (sem_vocabulario): O vocabulário não permite representar a falta de acordo sobre o prazo de receção das propostas.

## regra:eu-2014-25:auto-prazo-minimo-art48-1@v1

- leitor:a17: {"tipo": "prazo_minimo", "condicoes": [{"field": "tipo_procedimento", "op": "eq", "value": "dialogo_concorrencial"}], "params": {"minimum_days": 30, "deadline_field": "prazo_candidaturas_dias", "counted_from": "data_envio_anuncio", "usual_days": null}} || {"tipo": "prazo_minimo", "condicoes": [{"field": "anuncio_pre_informacao", "op": "eq", "value": true}, {"field": "tipo_procedimento", "op": "eq", "value": "dialogo_concorrencial"}], "params": {"minimum_days": 15, "deadline_field": "prazo_candidaturas_dias", "counted_from": "data_envio_anuncio", "usual_days": null}}
- leitor:b: {"tipo": "prazo_minimo", "condicoes": [{"field": "anuncio_pre_informacao", "op": "eq", "value": false}, {"field": "tipo_procedimento", "op": "eq", "value": "dialogo_concorrencial"}], "params": {"minimum_days": 15, "deadline_field": "prazo_candidaturas_dias", "counted_from": "data_envio_anuncio", "usual_days": 30}} || {"tipo": "prazo_minimo", "condicoes": [{"field": "anuncio_pre_informacao", "op": "eq", "value": true}, {"field": "tipo_procedimento", "op": "eq", "value": "dialogo_concorrencial"}], "params": {"minimum_days": 15, "deadline_field": "prazo_candidaturas_dias", "counted_from": "data_envio_convite", "usual_days": 30}}
- verificador (A): regra 1, tipo_procedimento eq dialogo_concorrencial: as fontes não nomeiam ['dialogo_concorrencial']; regra 2, tipo_procedimento eq dialogo_concorrencial: as fontes não nomeiam ['dialogo_concorrencial']
- verificador (B): regra 1, tipo_procedimento eq dialogo_concorrencial: as fontes não nomeiam ['dialogo_concorrencial']; regra 1: usual_days sem «em regra» e os dias nas fontes (L11); regra 2, tipo_procedimento eq dialogo_concorrencial: as fontes não nomeiam ['dialogo_concorrencial']; regra 2: counted_from data_envio_convite e as fontes dizem ['data_envio_anuncio'] (L9); regra 2: usual_days sem «em regra» e os dias nas fontes (L11)

## regra:eu-2014-25:auto-prazo-minimo-art49-1@v1

- leitor:a17: {"tipo": "prazo_minimo", "condicoes": [{"field": "tipo_procedimento", "op": "eq", "value": "parceria_inovacao"}], "params": {"minimum_days": 30, "deadline_field": "prazo_candidaturas_dias", "counted_from": "data_envio_anuncio", "usual_days": null}}
- leitor:b: {"tipo": "prazo_minimo", "condicoes": [{"field": "tipo_procedimento", "op": "eq", "value": "parceria_inovacao"}], "params": {"minimum_days": 15, "deadline_field": "prazo_candidaturas_dias", "counted_from": "data_envio_anuncio", "usual_days": 30}}
- verificador (B): regra 1: usual_days sem «em regra» e os dias nas fontes (L11)

## regra:eu-2014-25:auto-prazo-maximo-art52-5@v1

- leitor:a17: não tipável (sem_vocabulario): A regra é de um sistema de aquisição dinâmico, instrumento que o vocabulário não tem.
- leitor:b: não tipável (nao_e_prazo_maximo): O prazo é para a própria entidade adjudicante avaliar os pedidos de participação, não para apresentar elementos.

## regra:eu-2014-25:auto-prazo-minimo-art66-3-a@v1

- leitor:a17: não tipável (nao_e_prazo_minimo): O prazo é de prorrogação por falta de informação; falta um prazo mínimo para apresentar algo.
- leitor:b: não tipável (nao_e_prazo_minimo): A passagem estabelece quando a entidade adjudicante deve prorrogar o prazo por falta de informações adicionais, sem fixar um prazo mínimo para apresentação de propostas.

## regra:eu-2014-25:auto-prazo-maximo-art67-2-d@v1

- leitor:a17: não tipável (nao_e_prazo_maximo): O prazo é o da própria entidade adjudicante para enviar o anúncio, não um prazo máximo para os interessados apresentarem algo.
- leitor:b: não tipável (nao_e_prazo_maximo): A passagem regula o envio e o período abrangido pelo anúncio periódico indicativo, sem fixar um prazo para apresentar elementos.

## regra:eu-2014-25:auto-prazo-maximo-art70-1@v1

- leitor:a17: não tipável (nao_e_prazo_maximo): O prazo é da própria entidade adjudicante para enviar o anúncio de adjudicação, não um prazo máximo para os interessados apresentarem algo.
- leitor:b: não tipável (nao_e_prazo_maximo): O prazo é para as próprias entidades adjudicantes enviarem um anúncio de adjudicação do contrato.

## regra:eu-2014-25:auto-prazo-maximo-art70-2@v1

- leitor:a17: não tipável (sem_vocabulario): A regra é de um acordo-quadro, instrumento que o vocabulário não tem.
- leitor:b: não tipável (nao_e_prazo_maximo): Os prazos regulam o envio de anúncios pelas próprias entidades adjudicantes.

## regra:eu-2014-25:auto-prazo-maximo-art71-2@v1

- leitor:a17: não tipável (nao_e_prazo_maximo): O prazo é da própria entidade adjudicante para publicar os anúncios, não um prazo máximo para os interessados apresentarem algo.
- leitor:b: não tipável (nao_e_prazo_maximo): O prazo é para a publicação dos anúncios, não para apresentar algo.

## regra:eu-2014-25:auto-prazo-maximo-art73-1@v1

- leitor:a17: não tipável (nao_e_prazo_maximo): O prazo é de 10 dias para oferecer o acesso, não um prazo para apresentar algo.
- leitor:b: não tipável (nao_e_prazo_maximo): A passagem fixa uma prorrogação de cinco dias, sem estabelecer um prazo máximo para a apresentação de propostas.

## regra:eu-2014-25:auto-prazo-maximo-art73-2@v1

- leitor:a17: não tipável (nao_e_prazo_maximo): O prazo é da própria entidade adjudicante para comunicar informações, não um prazo máximo para os concorrentes apresentarem algo.
- leitor:b: não tipável (nao_e_prazo_maximo): O prazo destina-se à própria entidade adjudicante, para comunicar informações adicionais aos concorrentes.

## regra:eu-2014-25:auto-prazo-maximo-art75-2@v1

- leitor:a17: não tipável (nao_e_prazo_maximo): O prazo é de 15 dias antes de pôr termo à qualificação, não um prazo máximo para a entidade adjudicante.
- leitor:b: não tipável (nao_e_prazo_maximo): O prazo destina-se à própria entidade adjudicante para prestar informações.

## regra:eu-2014-25:auto-prazo-maximo-art75-5@v1

- leitor:a17: não tipável (nao_e_prazo_maximo): O prazo é o da própria entidade adjudicante para informar os requerentes, não um prazo máximo para os interessados apresentarem algo.
- leitor:b: não tipável (nao_e_prazo_maximo): O prazo destina-se à entidade adjudicante informar os requerentes da recusa da qualificação e das suas razões, não à apresentação de elementos pelos interessados.

## regra:eu-2014-25:auto-prazo-minimo-art75-6@v1

- leitor:a17: não tipável (nao_e_prazo_minimo): O prazo é de 15 dias antes de pôr termo à qualificação, não um prazo para apresentar algo.
- leitor:b: não tipável (nao_e_prazo_minimo): O prazo destina-se à notificação pela entidade adjudicante, não à apresentação de elementos pelo operador económico.

## regra:eu-2014-25:auto-prazo-maximo-art96-2@v1

- leitor:a17: não tipável (nao_e_prazo_maximo): O prazo é da Comissão para incluir informação nos anexos, não um prazo máximo para os interessados apresentarem algo.
- leitor:b: não tipável (nao_e_prazo_maximo): O prazo destina-se à própria entidade adjudicante comunicar o anúncio dos resultados do concurso.

