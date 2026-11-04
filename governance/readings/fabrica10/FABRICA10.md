# FÁBRICA DE REGRAS — ronda 10 (DECISIONS D68)

Gerado por tools/rule_factory.py (ccp-rule-factory-0.7) com o protocolo de leitura v3 (tools/read_rules_v3.py, ccp-read-rules-v3-0.4). D68: AMALIA treinada a partir de v13 nas leituras reais que as duas famílias assentaram às cegas, os números movidos por código (adaptador v14). Alvos: os 9 da ronda 9 ainda abertos, que nenhum exemplo de treino mostra. Propõe leitor:a16 (AMALIA + adaptador v14), leitor:b revê às cegas.

Os prompts são os da ronda 9, byte a byte; as respostas de leitor:b são as da ronda 9. Um programa confirma cada palavra citada; a leitura que falha não fica registada.

| regra | passagem | estado | replica | verificador: leitor A | verificador: leitor B |
|---|---|---|---|---|---|
| regra:ccp:auto-limiar-art127-c-1-a@v1 | ccp:art127-c.1.a | settled (não tipável: nao_e_limiar) | sim | ok | ok |
| regra:ccp:auto-limiar-art21-1-b@v1 | ccp:art21.1.b | sem leitura válida de leitor:a16 | — | regra 1, publicado_joue eq False: as fontes não negam o facto (L7) | ok |
| regra:ccp:auto-limiar-art21-1-c@v1 | ccp:art21.1.c | sem leitura válida de leitor:a16 | — | regra 1, publicado_joue eq False: as fontes não negam o facto (L7) | ok |
| regra:ccp:auto-limiar-art31-4@v1 | ccp:art31.4 | proposed | não | ok | ok |
| regra:ccp:auto-limiar-art54-a-1-b-ii@v1 | ccp:art54-a.1.b.ii | proposed (não tipável: texto_em_falta) | não | ok | ok |
| regra:ccp:auto-prazo-minimo-art174-3@v1 | ccp:art174.3 | proposed | não | ok | ok |
| regra:ccp:auto-prazo-minimo-art192-2@v1 | ccp:art192.2 | proposed | não | ok | ok |
| regra:ccp:auto-prazo-minimo-art198-1@v1 | ccp:art198.1 | settled | sim | ok | ok |
| regra:ccp:auto-prazo-minimo-art198-2@v1 | ccp:art198.2 | settled | sim | ok | ok |

## regra:ccp:auto-limiar-art127-c-1-a@v1

- leitor:a16: não tipável (nao_e_limiar): O valor exclui entidades do convite; não é o limite até ao qual um procedimento pode ser escolhido.
- leitor:b: não tipável (nao_e_limiar): O valor exclui entidades convidadas em função do preço contratual acumulado de contratos anteriores; não é um limite para a escolha do procedimento.

## regra:ccp:auto-limiar-art21-1-b@v1

- leitor:a16: {"tipo": "limiar", "condicoes": [{"field": "publicado_joue", "op": "eq", "value": false}, {"field": "tipo_contrato", "op": "not_in", "value": ["concessao_obras", "concessao_servicos"]}, {"field": "tipo_procedimento", "op": "eq", "value": "consulta_previa"}], "params": {"threshold": {"field": "valor_estimado", "comparator": "lt", "value": 130000, "currency": "EUR"}}}
- leitor:b: {"tipo": "limiar", "condicoes": [{"field": "tipo_contrato", "op": "not_in", "value": ["bens", "concessao_obras", "concessao_servicos", "obras", "servicos", "sociedade"]}, {"field": "tipo_procedimento", "op": "eq", "value": "consulta_previa"}], "params": {"threshold": {"field": "valor_estimado", "comparator": "lt", "value": 130000, "currency": "EUR"}}}
- verificador (A): regra 1, publicado_joue eq False: as fontes não negam o facto (L7)

## regra:ccp:auto-limiar-art21-1-c@v1

- leitor:a16: {"tipo": "limiar", "condicoes": [{"field": "publicado_joue", "op": "eq", "value": false}, {"field": "tipo_contrato", "op": "eq", "value": "obras"}, {"field": "tipo_procedimento", "op": "eq", "value": "ajuste_direto"}], "params": {"threshold": {"field": "valor_estimado", "comparator": "lt", "value": 75000, "currency": "EUR"}}}
- leitor:b: {"tipo": "limiar", "condicoes": [{"field": "tipo_contrato", "op": "not_in", "value": ["bens", "concessao_obras", "concessao_servicos", "obras", "servicos", "sociedade"]}, {"field": "tipo_procedimento", "op": "eq", "value": "ajuste_direto"}], "params": {"threshold": {"field": "valor_estimado", "comparator": "lt", "value": 75000, "currency": "EUR"}}}
- verificador (A): regra 1, publicado_joue eq False: as fontes não negam o facto (L7)

## regra:ccp:auto-limiar-art31-4@v1

- leitor:a16: {"tipo": "limiar", "condicoes": [{"field": "tipo_contrato", "op": "in", "value": ["concessao_obras", "concessao_servicos"]}, {"field": "tipo_procedimento", "op": "in", "value": ["ajuste_direto", "consulta_previa"]}], "params": {"threshold": {"field": "valor_estimado", "comparator": "lt", "value": 1000000, "currency": "EUR"}}}
- leitor:b: {"tipo": "limiar", "condicoes": [{"field": "duracao_contrato_meses", "op": "lt", "value": 12}, {"field": "tipo_contrato", "op": "in", "value": ["concessao_obras", "concessao_servicos"]}, {"field": "tipo_procedimento", "op": "in", "value": ["ajuste_direto", "consulta_previa"]}], "params": {"threshold": {"field": "valor_estimado", "comparator": "lt", "value": 1000000, "currency": "EUR"}}}

## regra:ccp:auto-limiar-art54-a-1-b-ii@v1

- leitor:a16: não tipável (texto_em_falta): Os limiares a que se refere o valor estão nas alíneas b) e c) do n.º 3 do artigo 474.º, que não estão mostradas.
- leitor:b: não tipável (nao_e_limiar): O valor limita a reserva de participação, não a escolha de um procedimento.

## regra:ccp:auto-prazo-minimo-art174-3@v1

- leitor:a16: {"tipo": "prazo_minimo", "condicoes": [{"field": "publicado_joue", "op": "eq", "value": true}, {"field": "setores_especiais", "op": "eq", "value": true}, {"field": "tipo_procedimento", "op": "eq", "value": "concurso_limitado_previa_qualificacao"}], "params": {"minimum_days": 30, "deadline_field": "prazo_candidaturas_dias", "counted_from": "data_envio_anuncio", "usual_days": null}}
- leitor:b: {"tipo": "prazo_minimo", "condicoes": [{"field": "publicado_joue", "op": "eq", "value": true}, {"field": "setores_especiais", "op": "eq", "value": true}, {"field": "tipo_procedimento", "op": "eq", "value": "concurso_limitado_previa_qualificacao"}], "params": {"minimum_days": 15, "deadline_field": "prazo_candidaturas_dias", "counted_from": "data_envio_anuncio", "usual_days": 30}}

## regra:ccp:auto-prazo-minimo-art192-2@v1

- leitor:a16: {"tipo": "prazo_minimo", "condicoes": [{"field": "publicado_joue", "op": "eq", "value": true}, {"field": "tipo_procedimento", "op": "eq", "value": "concurso_limitado_previa_qualificacao"}], "params": {"minimum_days": 10, "deadline_field": "prazo_propostas_dias", "counted_from": "data_envio_convite", "usual_days": null}}
- leitor:b: {"tipo": "prazo_minimo", "condicoes": [{"field": "publicado_joue", "op": "eq", "value": true}, {"field": "setores_especiais", "op": "eq", "value": true}, {"field": "tipo_procedimento", "op": "eq", "value": "concurso_limitado_previa_qualificacao"}], "params": {"minimum_days": 10, "deadline_field": "prazo_propostas_dias", "counted_from": "data_envio_convite", "usual_days": null}}

## regra:ccp:auto-prazo-minimo-art198-1@v1

- leitor:a16: {"tipo": "prazo_minimo", "condicoes": [{"field": "publicado_joue", "op": "eq", "value": true}, {"field": "tipo_procedimento", "op": "eq", "value": "procedimento_negociacao"}], "params": {"minimum_days": 30, "deadline_field": "prazo_candidaturas_dias", "counted_from": "data_envio_anuncio", "usual_days": null}}
- leitor:b: {"tipo": "prazo_minimo", "condicoes": [{"field": "publicado_joue", "op": "eq", "value": true}, {"field": "tipo_procedimento", "op": "eq", "value": "procedimento_negociacao"}], "params": {"minimum_days": 30, "deadline_field": "prazo_candidaturas_dias", "counted_from": "data_envio_anuncio", "usual_days": null}}

## regra:ccp:auto-prazo-minimo-art198-2@v1

- leitor:a16: {"tipo": "prazo_minimo", "condicoes": [{"field": "anuncio_pre_informacao", "op": "eq", "value": true}, {"field": "tipo_procedimento", "op": "eq", "value": "procedimento_negociacao"}], "params": {"minimum_days": 25, "deadline_field": "prazo_candidaturas_dias", "counted_from": "data_envio_convite", "usual_days": null}}
- leitor:b: {"tipo": "prazo_minimo", "condicoes": [{"field": "anuncio_pre_informacao", "op": "eq", "value": true}, {"field": "tipo_procedimento", "op": "eq", "value": "procedimento_negociacao"}], "params": {"minimum_days": 25, "deadline_field": "prazo_candidaturas_dias", "counted_from": "data_envio_convite", "usual_days": null}}

