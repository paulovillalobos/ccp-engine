# FÁBRICA DE REGRAS — ronda 8 (DECISIONS D66)

Gerado por tools/rule_factory.py (ccp-rule-factory-0.7) com o protocolo de leitura v3 (tools/read_rules_v3.py, ccp-read-rules-v3-0.3). D66: AMALIA treinada no protocolo v3 (adaptador v12). Alvos: os da ronda 6 que ficaram abertos, com o protocolo 0.3. Propõe leitor:a14 (AMALIA + adaptador v12), leitor:b revê às cegas.

leitor:b responde de novo aos prompts 0.3. Um programa confirma cada palavra citada; a leitura que falha não fica registada.

| regra | passagem | estado | replica | verificador: leitor A | verificador: leitor B |
|---|---|---|---|---|---|
| regra:ccp:auto-limiar-art127-c-1-a@v1 | ccp:art127-c.1.a | sem leitura válida de leitor:a14 | — | regra 1, tipo_contrato in ['concessao_obras', 'concessao_servicos', 'obras', 'servicos']: as fontes não nomeiam ['servic | ok |
| regra:ccp:auto-limiar-art17-b-4@v1 | ccp:art17-b.4 | sem leitura válida de leitor:a14 | — | regra 1, tipo_entidade eq outra: as fontes não nomeiam ['outra'] | ok |
| regra:ccp:auto-limiar-art21-1-b@v1 | ccp:art21.1.b | sem leitura válida de leitor:a14 | — | regra 1, tipo_contrato not_in ['concessao_obras', 'concessao_servicos', 'bens', 'servicos']: as fontes não nomeiam ['ben | ok |
| regra:ccp:auto-limiar-art21-1-c@v1 | ccp:art21.1.c | sem leitura válida de leitor:a14 | — | regra 1, tipo_contrato not_in ['concessao_obras', 'concessao_servicos', 'bens', 'servicos']: «concessão de obras pública | ok |
| regra:ccp:auto-limiar-art31-4@v1 | ccp:art31.4 | sem leitura válida de leitor:a14 | — | regra 1, tipo_procedimento in ['ajuste_direto', 'concurso_limitado_previa_qualificacao', 'concurso_publico', 'consulta_p | ok |
| regra:ccp:auto-limiar-art54-a-1-b-ii@v1 | ccp:art54-a.1.b.ii | sem leitura válida de leitor:a14 | — | regra 1, tipo_contrato in ['bens', 'servicos']: «locação ou aquisição de bens» não está em ccp:art54-a.1.b | ok |
| regra:ccp:auto-limiar-art88-2-a@v1 | ccp:art88.2.a | sem leitura válida de leitor:a14 | — | regra 1, preco_contratual lt 1000000: num limiar o valor é o parâmetro, não uma condição (L10) | ok |
| regra:ccp:auto-prazo-minimo-art174-3@v1 | ccp:art174.3 | sem leitura válida de leitor:a14 | — | regra 1, publicado_joue eq True: fonte em ccp:art174.1, que é vizinho (L1) | ok |
| regra:ccp:auto-prazo-minimo-art192-2@v1 | ccp:art192.2 | sem leitura válida de leitor:a14 | — | regra 1, tipo_procedimento eq concurso_limitado_previa_qualificacao: «concurso limitado por prévia qualificação» não est | ok |
| regra:ccp:auto-prazo-minimo-art198-1@v1 | ccp:art198.1 | proposed | não | ok | ok |
| regra:ccp:auto-prazo-minimo-art198-2@v1 | ccp:art198.2 | sem leitura válida de leitor:a14 | — | regra 1, publicado_joue eq True: «publicado no Jornal Oficial da União Europeia» não está em ccp:art167.5 | ok |
| regra:ccp:auto-prazo-minimo-art241-b-3-b@v1 | ccp:art241-b.3.b | sem leitura válida de leitor:a14 | — | regra 1, tipo_contrato eq bens: «bem ou serviço» não está em ccp:art241-b.3 | ok |

## regra:ccp:auto-limiar-art127-c-1-a@v1

- leitor:a14: {"tipo": "limiar", "condicoes": [{"field": "tipo_contrato", "op": "in", "value": ["concessao_obras", "concessao_servicos", "obras", "servicos"]}, {"field": "tipo_procedimento", "op": "eq", "value": "consulta_previa_especial"}], "params": {"threshold": {"field": "preco_contratual", "comparator": "ge", "value": 2000000, "currency": "EUR"}}}
- leitor:b: não tipável (nao_e_limiar): O valor exclui entidades convidadas em função do preço contratual acumulado de vários contratos; não limita a escolha de um procedimento.
- verificador (A): regra 1, tipo_contrato in ['concessao_obras', 'concessao_servicos', 'obras', 'servicos']: as fontes não nomeiam ['servicos']; regra 1, tipo_procedimento eq consulta_previa_especial: «consulta prévia especial» não está em ccp:art127-c; regra 1, tipo_procedimento eq consulta_previa_especial: as fontes não nomeiam ['consulta_previa_especial']; regra 1, field: «preço contratual» não está em ccp:art127-c.1.a; regra 1: field preco_contratual e as fontes nomeiam nada (L10)

## regra:ccp:auto-limiar-art17-b-4@v1

- leitor:a14: {"tipo": "limiar", "condicoes": [{"field": "tipo_contrato", "op": "eq", "value": "obras"}, {"field": "tipo_entidade", "op": "eq", "value": "outra"}], "params": {"threshold": {"field": "valor_estimado", "comparator": "lt", "value": 1000000, "currency": "EUR"}}}
- leitor:b: não tipável (nao_e_limiar): Os valores fixam uma dispensa da obrigação de agregação, não um limite até ao qual um procedimento pode ser escolhido.
- verificador (A): regra 1, tipo_entidade eq outra: as fontes não nomeiam ['outra']; regra 1: um limiar tem sempre o procedimento que permite abaixo do valor; sem ele, L12 (nao_e_limiar)

## regra:ccp:auto-limiar-art21-1-b@v1

- leitor:a14: {"tipo": "limiar", "condicoes": [{"field": "publicado_joue", "op": "eq", "value": false}, {"field": "tipo_contrato", "op": "not_in", "value": ["bens", "concessao_obras", "concessao_servicos", "servicos"]}, {"field": "tipo_procedimento", "op": "eq", "value": "consulta_previa"}], "params": {"threshold": {"field": "valor_estimado", "comparator": "lt", "value": 130000, "currency": "EUR"}}}
- leitor:b: {"tipo": "limiar", "condicoes": [{"field": "tipo_contrato", "op": "not_in", "value": ["bens", "concessao_obras", "concessao_servicos", "obras", "servicos", "sociedade"]}, {"field": "tipo_procedimento", "op": "eq", "value": "consulta_previa"}], "params": {"threshold": {"field": "valor_estimado", "comparator": "lt", "value": 130000, "currency": "EUR"}}}
- verificador (A): regra 1, tipo_contrato not_in ['concessao_obras', 'concessao_servicos', 'bens', 'servicos']: as fontes não nomeiam ['bens', 'servicos']; regra 1, publicado_joue eq False: fonte em ccp:art21.1.a, que é vizinho (L1)

## regra:ccp:auto-limiar-art21-1-c@v1

- leitor:a14: {"tipo": "limiar", "condicoes": [{"field": "tipo_contrato", "op": "not_in", "value": ["bens", "concessao_obras", "concessao_servicos", "servicos"]}, {"field": "tipo_procedimento", "op": "eq", "value": "ajuste_direto"}], "params": {"threshold": {"field": "valor_estimado", "comparator": "lt", "value": 75000, "currency": "EUR"}}}
- leitor:b: {"tipo": "limiar", "condicoes": [{"field": "tipo_contrato", "op": "not_in", "value": ["bens", "concessao_obras", "concessao_servicos", "obras", "servicos", "sociedade"]}, {"field": "tipo_procedimento", "op": "eq", "value": "ajuste_direto"}], "params": {"threshold": {"field": "valor_estimado", "comparator": "lt", "value": 75000, "currency": "EUR"}}}
- verificador (A): regra 1, tipo_contrato not_in ['concessao_obras', 'concessao_servicos', 'bens', 'servicos']: «concessão de obras públicas ou de serviços» não está em ccp:art21.1; regra 1, tipo_contrato not_in ['concessao_obras', 'concessao_servicos', 'bens', 'servicos']: as fontes não nomeiam ['bens', 'concessao_obras', 'concessao_servicos', 'servicos']

## regra:ccp:auto-limiar-art31-4@v1

- leitor:a14: {"tipo": "limiar", "condicoes": [{"field": "tipo_contrato", "op": "in", "value": ["concessao_obras", "concessao_servicos"]}, {"field": "tipo_procedimento", "op": "in", "value": ["ajuste_direto", "concurso_limitado_previa_qualificacao", "concurso_publico", "consulta_previa"]}], "params": {"threshold": {"field": "valor_estimado", "comparator": "lt", "value": 1000000, "currency": "EUR"}}}
- leitor:b: {"tipo": "limiar", "condicoes": [{"field": "duracao_contrato_meses", "op": "lt", "value": 12}, {"field": "tipo_contrato", "op": "in", "value": ["concessao_obras", "concessao_servicos"]}, {"field": "tipo_procedimento", "op": "in", "value": ["ajuste_direto", "consulta_previa"]}], "params": {"threshold": {"field": "valor_estimado", "comparator": "lt", "value": 1000000, "currency": "EUR"}}}
- verificador (A): regra 1, tipo_procedimento in ['ajuste_direto', 'concurso_limitado_previa_qualificacao', 'concurso_publico', 'consulta_previa']: fonte em ccp:art31.3, que é vizinho (L1); regra 1, tipo_procedimento in ['ajuste_direto', 'concurso_limitado_previa_qualificacao', 'concurso_publico', 'consulta_previa']: fonte em ccp:art31.1, que é vizinho (L1); regra 1, tipo_procedimento in ['ajuste_direto', 'concurso_limitado_previa_qualificacao', 'concurso_publico', 'consulta_previa']: fonte em ccp:art31.1, que é vizinho (L1)

## regra:ccp:auto-limiar-art54-a-1-b-ii@v1

- leitor:a14: {"tipo": "limiar", "condicoes": [{"field": "publicado_joue", "op": "eq", "value": false}, {"field": "tipo_contrato", "op": "in", "value": ["bens", "servicos"]}, {"field": "tipo_entidade", "op": "eq", "value": "outra"}], "params": {"threshold": {"field": "valor_estimado", "comparator": "lt", "value": 500000, "currency": "EUR"}}}
- leitor:b: não tipável (nao_e_limiar): O valor delimita a reserva de participação, não o limite até ao qual um procedimento pode ser escolhido.
- verificador (A): regra 1, tipo_contrato in ['bens', 'servicos']: «locação ou aquisição de bens» não está em ccp:art54-a.1.b; regra 1, tipo_contrato in ['bens', 'servicos']: «aquisição de serviços» não está em ccp:art54-a.1.b; regra 1, tipo_contrato in ['bens', 'servicos']: as fontes não nomeiam ['bens', 'servicos']; regra 1, tipo_entidade eq outra: as fontes não nomeiam ['outra']; regra 1, publicado_joue eq False: «de valor inferior aos limiares referidos nas alíneas b) ou c» não está em ccp:art54-a.1.b; regra 1, publicado_joue eq False: as fontes não negam o facto (L7)

## regra:ccp:auto-limiar-art88-2-a@v1

- leitor:a14: {"tipo": "limiar", "condicoes": [{"field": "preco_contratual", "op": "lt", "value": 1000000}], "params": {"threshold": {"field": "preco_contratual", "comparator": "lt", "value": 1000000, "currency": "EUR"}}}
- leitor:b: não tipável (nao_e_limiar): O valor permite dispensar a prestação de caução, não fixa um limite para a escolha de um procedimento.
- verificador (A): regra 1, preco_contratual lt 1000000: num limiar o valor é o parâmetro, não uma condição (L10); regra 1: um limiar tem sempre o procedimento que permite abaixo do valor; sem ele, L12 (nao_e_limiar)

## regra:ccp:auto-prazo-minimo-art174-3@v1

- leitor:a14: {"tipo": "prazo_minimo", "condicoes": [{"field": "publicado_joue", "op": "eq", "value": true}, {"field": "tipo_procedimento", "op": "eq", "value": "concurso_limitado_previa_qualificacao"}, {"field": "urgencia_fundamentada", "op": "eq", "value": true}], "params": {"minimum_days": 15, "deadline_field": "prazo_propostas_dias", "counted_from": "data_envio_anuncio", "usual_days": null}}
- leitor:b: {"tipo": "prazo_minimo", "condicoes": [{"field": "publicado_joue", "op": "eq", "value": true}, {"field": "setores_especiais", "op": "eq", "value": true}, {"field": "tipo_procedimento", "op": "eq", "value": "concurso_limitado_previa_qualificacao"}], "params": {"minimum_days": 15, "deadline_field": "prazo_candidaturas_dias", "counted_from": "data_envio_anuncio", "usual_days": 30}}
- verificador (A): regra 1, publicado_joue eq True: fonte em ccp:art174.1, que é vizinho (L1); regra 1, tipo_procedimento eq concurso_limitado_previa_qualificacao: fonte em ccp:art174.1, que é vizinho (L1); regra 1, urgencia_fundamentada eq True: fonte em ccp:art174.2, que é vizinho (L1); regra 1, deadline_field: fonte em ccp:art174.1, que é vizinho (L1); regra 1: deadline_field prazo_propostas_dias e as fontes dizem ['prazo_candidaturas_dias'] (L9); regra 1, counted_from: fonte em ccp:art174.1, que é vizinho (L1)

## regra:ccp:auto-prazo-minimo-art192-2@v1

- leitor:a14: {"tipo": "prazo_minimo", "condicoes": [{"field": "publicado_joue", "op": "eq", "value": true}, {"field": "tipo_procedimento", "op": "eq", "value": "concurso_limitado_previa_qualificacao"}], "params": {"minimum_days": 10, "deadline_field": "prazo_propostas_dias", "counted_from": "data_envio_convite", "usual_days": null}}
- leitor:b: {"tipo": "prazo_minimo", "condicoes": [{"field": "publicado_joue", "op": "eq", "value": true}, {"field": "setores_especiais", "op": "eq", "value": true}, {"field": "tipo_procedimento", "op": "eq", "value": "concurso_limitado_previa_qualificacao"}], "params": {"minimum_days": 10, "deadline_field": "prazo_propostas_dias", "counted_from": "data_envio_convite", "usual_days": null}}
- verificador (A): regra 1, tipo_procedimento eq concurso_limitado_previa_qualificacao: «concurso limitado por prévia qualificação» não está em ccp:art192; regra 1, tipo_procedimento eq concurso_limitado_previa_qualificacao: as fontes não nomeiam ['concurso_limitado_previa_qualificacao']; regra 1, deadline_field: «apresentação das propostas» não está em ccp:art192.2; regra 1: deadline_field prazo_propostas_dias e as fontes dizem nada (L9)

## regra:ccp:auto-prazo-minimo-art198-1@v1

- leitor:a14: {"tipo": "prazo_minimo", "condicoes": [{"field": "tipo_procedimento", "op": "eq", "value": "procedimento_negociacao"}], "params": {"minimum_days": 30, "deadline_field": "prazo_candidaturas_dias", "counted_from": "data_envio_anuncio", "usual_days": null}}
- leitor:b: {"tipo": "prazo_minimo", "condicoes": [{"field": "publicado_joue", "op": "eq", "value": true}, {"field": "tipo_procedimento", "op": "eq", "value": "procedimento_negociacao"}], "params": {"minimum_days": 30, "deadline_field": "prazo_candidaturas_dias", "counted_from": "data_envio_anuncio", "usual_days": null}}

## regra:ccp:auto-prazo-minimo-art198-2@v1

- leitor:a14: {"tipo": "prazo_minimo", "condicoes": [{"field": "anuncio_pre_informacao", "op": "eq", "value": true}, {"field": "publicado_joue", "op": "eq", "value": true}, {"field": "tipo_procedimento", "op": "eq", "value": "procedimento_negociacao"}], "params": {"minimum_days": 25, "deadline_field": "prazo_candidaturas_dias", "counted_from": "data_envio_convite", "usual_days": null}}
- leitor:b: {"tipo": "prazo_minimo", "condicoes": [{"field": "anuncio_pre_informacao", "op": "eq", "value": true}, {"field": "tipo_procedimento", "op": "eq", "value": "procedimento_negociacao"}], "params": {"minimum_days": 25, "deadline_field": "prazo_candidaturas_dias", "counted_from": "data_envio_convite", "usual_days": null}}
- verificador (A): regra 1, publicado_joue eq True: «publicado no Jornal Oficial da União Europeia» não está em ccp:art167.5; regra 1, publicado_joue eq True: as fontes não afirmam o facto (L7); regra 1, tipo_procedimento eq procedimento_negociacao: fonte em ccp:art198.3, que é vizinho (L1); regra 1, tipo_procedimento eq procedimento_negociacao: «Procedimento de negociação» não está em ccp:art198.3; regra 1, tipo_procedimento eq procedimento_negociacao: as fontes não nomeiam ['procedimento_negociacao']

## regra:ccp:auto-prazo-minimo-art241-b-3-b@v1

- leitor:a14: {"tipo": "prazo_minimo", "condicoes": [{"field": "tipo_contrato", "op": "eq", "value": "bens"}, {"field": "tipo_procedimento", "op": "eq", "value": "concurso_concecao"}], "params": {"minimum_days": 10, "deadline_field": "prazo_propostas_dias", "counted_from": "nao_indicado", "usual_days": null}}
- leitor:b: não tipável (sem_vocabulario): O vocabulário não permite limitar a regra aos sistemas de aquisição dinâmicos.
- verificador (A): regra 1, tipo_contrato eq bens: «bem ou serviço» não está em ccp:art241-b.3; regra 1, tipo_contrato eq bens: as fontes não nomeiam ['bens']; regra 1, tipo_procedimento eq concurso_concecao: «Sistemas de aquisição dinâmicos» não está em ccp:art241-b.3; regra 1, tipo_procedimento eq concurso_concecao: as fontes não nomeiam ['concurso_concecao']

