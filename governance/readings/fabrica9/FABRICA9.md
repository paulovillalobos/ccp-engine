# FÁBRICA DE REGRAS — ronda 9 (DECISIONS D67)

Gerado por tools/rule_factory.py (ccp-rule-factory-0.7) com o protocolo de leitura v3 (tools/read_rules_v3.py, ccp-read-rules-v3-0.4). D67: AMALIA treinada em artigos com a textura da lei (adaptador v13), as citações presas ao texto por uma gramática. Alvos: os da ronda 6 que ficaram abertos, com o protocolo 0.4. Propõe leitor:a15 (AMALIA + adaptador v13), leitor:b revê às cegas.

leitor:b responde de novo aos prompts 0.4. Um programa confirma cada palavra citada; a leitura que falha não fica registada.

| regra | passagem | estado | replica | verificador: leitor A | verificador: leitor B |
|---|---|---|---|---|---|
| regra:ccp:auto-limiar-art127-c-1-a@v1 | ccp:art127-c.1.a | sem leitura válida de leitor:a15 | — | regra 1, tipo_contrato in ['concessao_obras', 'concessao_servicos', 'obras']: as fontes não nomeiam ['obras'] | ok |
| regra:ccp:auto-limiar-art17-b-4@v1 | ccp:art17-b.4 | settled (não tipável: nao_e_limiar) | sim | ok | ok |
| regra:ccp:auto-limiar-art21-1-b@v1 | ccp:art21.1.b | proposed | não | ok | ok |
| regra:ccp:auto-limiar-art21-1-c@v1 | ccp:art21.1.c | proposed | não | ok | ok |
| regra:ccp:auto-limiar-art31-4@v1 | ccp:art31.4 | proposed | não | ok | ok |
| regra:ccp:auto-limiar-art54-a-1-b-ii@v1 | ccp:art54-a.1.b.ii | sem leitura válida de leitor:a15 | — | regra 1, tipo_entidade eq outra: as fontes não nomeiam ['outra'] | ok |
| regra:ccp:auto-limiar-art88-2-a@v1 | ccp:art88.2.a | settled (não tipável: nao_e_limiar) | sim | ok | ok |
| regra:ccp:auto-prazo-minimo-art174-3@v1 | ccp:art174.3 | sem leitura válida de leitor:a15 | — | regra 1: deadline_field prazo_propostas_dias e as fontes dizem ['prazo_candidaturas_dias'] (L9) | ok |
| regra:ccp:auto-prazo-minimo-art192-2@v1 | ccp:art192.2 | proposed | não | ok | ok |
| regra:ccp:auto-prazo-minimo-art198-1@v1 | ccp:art198.1 | proposed | não | ok | ok |
| regra:ccp:auto-prazo-minimo-art198-2@v1 | ccp:art198.2 | sem leitura válida de leitor:a15 | — | regra 1: counted_from data_envio_convite e as fontes dizem nada (L9) | ok |
| regra:ccp:auto-prazo-minimo-art241-b-3-b@v1 | ccp:art241-b.3.b | settled (não tipável: sem_vocabulario) | sim | ok | ok |

## regra:ccp:auto-limiar-art127-c-1-a@v1

- leitor:a15: {"tipo": "limiar", "condicoes": [{"field": "tipo_contrato", "op": "in", "value": ["concessao_obras", "concessao_servicos", "obras"]}, {"field": "tipo_procedimento", "op": "eq", "value": "consulta_previa_especial"}], "params": {"threshold": {"field": "preco_contratual", "comparator": "ge", "value": 2000000, "currency": "EUR"}}}
- leitor:b: não tipável (nao_e_limiar): O valor exclui entidades convidadas em função do preço contratual acumulado de contratos anteriores; não é um limite para a escolha do procedimento.
- verificador (A): regra 1, tipo_contrato in ['concessao_obras', 'concessao_servicos', 'obras']: as fontes não nomeiam ['obras']; regra 1: comparator ge e as fontes dizem nada (L8)

## regra:ccp:auto-limiar-art17-b-4@v1

- leitor:a15: não tipável (nao_e_limiar): O valor dispensa a observância de um procedimento; não é o limite até ao qual um procedimento pode ser escolhido.
- leitor:b: não tipável (nao_e_limiar): Os valores delimitam uma dispensa da agregação de valores, sem fixar um limite até ao qual um procedimento pode ser escolhido.

## regra:ccp:auto-limiar-art21-1-b@v1

- leitor:a15: {"tipo": "limiar", "condicoes": [{"field": "tipo_contrato", "op": "not_in", "value": ["concessao_obras", "concessao_servicos", "sociedade"]}, {"field": "tipo_procedimento", "op": "eq", "value": "consulta_previa"}], "params": {"threshold": {"field": "valor_estimado", "comparator": "lt", "value": 130000, "currency": "EUR"}}}
- leitor:b: {"tipo": "limiar", "condicoes": [{"field": "tipo_contrato", "op": "not_in", "value": ["bens", "concessao_obras", "concessao_servicos", "obras", "servicos", "sociedade"]}, {"field": "tipo_procedimento", "op": "eq", "value": "consulta_previa"}], "params": {"threshold": {"field": "valor_estimado", "comparator": "lt", "value": 130000, "currency": "EUR"}}}

## regra:ccp:auto-limiar-art21-1-c@v1

- leitor:a15: {"tipo": "limiar", "condicoes": [{"field": "tipo_contrato", "op": "eq", "value": "obras"}, {"field": "tipo_procedimento", "op": "eq", "value": "ajuste_direto"}], "params": {"threshold": {"field": "valor_estimado", "comparator": "lt", "value": 75000, "currency": "EUR"}}}
- leitor:b: {"tipo": "limiar", "condicoes": [{"field": "tipo_contrato", "op": "not_in", "value": ["bens", "concessao_obras", "concessao_servicos", "obras", "servicos", "sociedade"]}, {"field": "tipo_procedimento", "op": "eq", "value": "ajuste_direto"}], "params": {"threshold": {"field": "valor_estimado", "comparator": "lt", "value": 75000, "currency": "EUR"}}}

## regra:ccp:auto-limiar-art31-4@v1

- leitor:a15: {"tipo": "limiar", "condicoes": [{"field": "tipo_contrato", "op": "in", "value": ["concessao_obras", "concessao_servicos"]}, {"field": "tipo_procedimento", "op": "in", "value": ["ajuste_direto", "consulta_previa"]}], "params": {"threshold": {"field": "valor_estimado", "comparator": "lt", "value": 1000000, "currency": "EUR"}}}
- leitor:b: {"tipo": "limiar", "condicoes": [{"field": "duracao_contrato_meses", "op": "lt", "value": 12}, {"field": "tipo_contrato", "op": "in", "value": ["concessao_obras", "concessao_servicos"]}, {"field": "tipo_procedimento", "op": "in", "value": ["ajuste_direto", "consulta_previa"]}], "params": {"threshold": {"field": "valor_estimado", "comparator": "lt", "value": 1000000, "currency": "EUR"}}}

## regra:ccp:auto-limiar-art54-a-1-b-ii@v1

- leitor:a15: {"tipo": "limiar", "condicoes": [{"field": "tipo_contrato", "op": "in", "value": ["concessao_obras", "concessao_servicos", "obras"]}, {"field": "tipo_entidade", "op": "eq", "value": "outra"}, {"field": "tipo_procedimento", "op": "in", "value": ["ajuste_direto", "concurso_publico"]}], "params": {"threshold": {"field": "valor_estimado", "comparator": "lt", "value": 500000, "currency": "EUR"}}}
- leitor:b: não tipável (nao_e_limiar): O valor limita a reserva de participação, não a escolha de um procedimento.
- verificador (A): regra 1, tipo_entidade eq outra: as fontes não nomeiam ['outra']; regra 1, tipo_procedimento in ['ajuste_direto', 'concurso_publico']: as fontes não nomeiam ['ajuste_direto', 'concurso_publico']

## regra:ccp:auto-limiar-art88-2-a@v1

- leitor:a15: não tipável (nao_e_limiar): O valor dispensa a prestação de caução; não é o limite até ao qual um procedimento pode ser escolhido.
- leitor:b: não tipável (nao_e_limiar): O valor permite dispensar a prestação de caução; não limita a escolha de um procedimento.

## regra:ccp:auto-prazo-minimo-art174-3@v1

- leitor:a15: {"tipo": "prazo_minimo", "condicoes": [{"field": "setores_especiais", "op": "eq", "value": true}, {"field": "tipo_procedimento", "op": "eq", "value": "concurso_limitado_previa_qualificacao"}], "params": {"minimum_days": 30, "deadline_field": "prazo_propostas_dias", "counted_from": "data_envio_anuncio", "usual_days": null}}
- leitor:b: {"tipo": "prazo_minimo", "condicoes": [{"field": "publicado_joue", "op": "eq", "value": true}, {"field": "setores_especiais", "op": "eq", "value": true}, {"field": "tipo_procedimento", "op": "eq", "value": "concurso_limitado_previa_qualificacao"}], "params": {"minimum_days": 15, "deadline_field": "prazo_candidaturas_dias", "counted_from": "data_envio_anuncio", "usual_days": 30}}
- verificador (A): regra 1: deadline_field prazo_propostas_dias e as fontes dizem ['prazo_candidaturas_dias'] (L9)

## regra:ccp:auto-prazo-minimo-art192-2@v1

- leitor:a15: {"tipo": "prazo_minimo", "condicoes": [{"field": "publicado_joue", "op": "eq", "value": true}, {"field": "tipo_procedimento", "op": "eq", "value": "concurso_limitado_previa_qualificacao"}], "params": {"minimum_days": 10, "deadline_field": "prazo_propostas_dias", "counted_from": "data_envio_convite", "usual_days": null}}
- leitor:b: {"tipo": "prazo_minimo", "condicoes": [{"field": "publicado_joue", "op": "eq", "value": true}, {"field": "setores_especiais", "op": "eq", "value": true}, {"field": "tipo_procedimento", "op": "eq", "value": "concurso_limitado_previa_qualificacao"}], "params": {"minimum_days": 10, "deadline_field": "prazo_propostas_dias", "counted_from": "data_envio_convite", "usual_days": null}}

## regra:ccp:auto-prazo-minimo-art198-1@v1

- leitor:a15: {"tipo": "prazo_minimo", "condicoes": [{"field": "tipo_procedimento", "op": "eq", "value": "procedimento_negociacao"}], "params": {"minimum_days": 30, "deadline_field": "prazo_candidaturas_dias", "counted_from": "data_envio_anuncio", "usual_days": null}}
- leitor:b: {"tipo": "prazo_minimo", "condicoes": [{"field": "publicado_joue", "op": "eq", "value": true}, {"field": "tipo_procedimento", "op": "eq", "value": "procedimento_negociacao"}], "params": {"minimum_days": 30, "deadline_field": "prazo_candidaturas_dias", "counted_from": "data_envio_anuncio", "usual_days": null}}

## regra:ccp:auto-prazo-minimo-art198-2@v1

- leitor:a15: {"tipo": "prazo_minimo", "condicoes": [{"field": "anuncio_pre_informacao", "op": "eq", "value": true}, {"field": "tipo_procedimento", "op": "eq", "value": "procedimento_negociacao"}], "params": {"minimum_days": 25, "deadline_field": "prazo_candidaturas_dias", "counted_from": "data_envio_convite", "usual_days": null}}
- leitor:b: {"tipo": "prazo_minimo", "condicoes": [{"field": "anuncio_pre_informacao", "op": "eq", "value": true}, {"field": "tipo_procedimento", "op": "eq", "value": "procedimento_negociacao"}], "params": {"minimum_days": 25, "deadline_field": "prazo_candidaturas_dias", "counted_from": "data_envio_convite", "usual_days": null}}
- verificador (A): regra 1: counted_from data_envio_convite e as fontes dizem nada (L9)

## regra:ccp:auto-prazo-minimo-art241-b-3-b@v1

- leitor:a15: não tipável (sem_vocabulario): A regra é de um sistema de aquisição dinâmico, instrumento que o vocabulário não tem.
- leitor:b: não tipável (sem_vocabulario): O vocabulário não permite limitar a regra aos sistemas de aquisição dinâmicos.

