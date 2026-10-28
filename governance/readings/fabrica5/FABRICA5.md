# FÁBRICA DE REGRAS — ronda 5 (DECISIONS D65)

Gerado por tools/rule_factory.py (ccp-rule-factory-0.6). D65: AMALIA treinada nos tipos de erro que v10 fez no dev (adaptador v11). Alvos: os 12 que a ronda 4 deixou abertos. Propõe leitor:a13 (AMALIA + adaptador v11), leitor:b revê às cegas; só fica settled a leitura que leitor:b replica com o mesmo conteúdo e a passagem-alvo citada (D64).

As respostas de leitor:b são as da ronda 4 (o mesmo prompt, byte a byte); uma regra já no registo recebe uma correção (nova revisão) de leitor:a13.

| regra | passagem | estado | exato | direção | lacunas do vocabulário |
|---|---|---|---|---|---|
| regra:ccp:auto-limiar-art127-c-1-a@v1 | ccp:art127-c.1.a | proposed | não | sim | — |
| regra:ccp:auto-limiar-art17-b-4@v1 | ccp:art17-b.4 | proposed (2 regras) | não | não | — |
| regra:ccp:auto-limiar-art21-1-b@v1 | ccp:art21.1.b | proposed | não | sim | — |
| regra:ccp:auto-limiar-art21-1-c@v1 | ccp:art21.1.c | proposed | não | sim | — |
| regra:ccp:auto-limiar-art31-4@v1 | ccp:art31.4 | proposed | não | sim | — |
| regra:ccp:auto-limiar-art54-a-1-b-ii@v1 | ccp:art54-a.1.b.ii | proposed | não | sim | — |
| regra:ccp:auto-limiar-art88-2-a@v1 | ccp:art88.2.a | settled | sim | sim | — |
| regra:ccp:auto-prazo-minimo-art174-3@v1 | ccp:art174.3 | proposed | não | sim | — |
| regra:ccp:auto-prazo-minimo-art192-2@v1 | ccp:art192.2 | proposed | não | sim | — |
| regra:ccp:auto-prazo-minimo-art198-1@v1 | ccp:art198.1 | proposed | não | sim | — |
| regra:ccp:auto-prazo-minimo-art198-2@v1 | ccp:art198.2 | proposed | não | sim | — |
| regra:ccp:auto-prazo-minimo-art241-b-3-b@v1 | ccp:art241-b.3.b | proposed | não | sim | — |

## regra:ccp:auto-limiar-art127-c-1-a@v1

- leitor:a13: passagens ccp:art127-c.1, ccp:art127-c.1.a; condições [{"field": "tipo_contrato", "op": "in", "value": ["concessao_obras", "concessao_servicos", "obras"]}, {"field": "tipo_procedimento", "op": "eq", "value": "consulta_previa"}]; params {"threshold": {"field": "preco_base", "comparator": "le", "value": 2000000, "currency": "EUR"}}
- leitor:b: passagens ccp:art127-c.1, ccp:art127-c.1.a; condições [{"field": "tipo_contrato", "op": "in", "value": ["concessao_obras", "concessao_servicos", "obras"]}, {"field": "tipo_procedimento", "op": "eq", "value": "consulta_previa"}]; params {"threshold": {"field": "preco_base", "comparator": "lt", "value": 2000000, "currency": "EUR"}}

## regra:ccp:auto-limiar-art17-b-4@v1

- leitor:a13: passagens ccp:art17-b.4; condições [{"field": "tipo_contrato", "op": "eq", "value": "bens"}]; params {"threshold": {"field": "preco_base", "comparator": "lt", "value": 80000, "currency": "EUR"}} || passagens ccp:art17-b.4; condições [{"field": "tipo_contrato", "op": "eq", "value": "obras"}]; params {"threshold": {"field": "preco_base", "comparator": "lt", "value": 1000000, "currency": "EUR"}}
- leitor:b: passagens ccp:art17-b.4; condições [{"field": "tipo_contrato", "op": "eq", "value": "obras"}]; params {"threshold": {"field": "preco_base", "comparator": "lt", "value": 1000000, "currency": "EUR"}} || passagens ccp:art17-b.4; condições [{"field": "tipo_contrato", "op": "in", "value": ["bens", "servicos"]}]; params {"threshold": {"field": "preco_base", "comparator": "lt", "value": 80000, "currency": "EUR"}}

## regra:ccp:auto-limiar-art21-1-b@v1

- leitor:a13: passagens ccp:art21.1.b, ccp:art21.1.c; condições [{"field": "tipo_contrato", "op": "not_in", "value": ["concessao_obras", "concessao_servicos"]}, {"field": "tipo_procedimento", "op": "eq", "value": "consulta_previa"}]; params {"threshold": {"field": "preco_base", "comparator": "lt", "value": 130000, "currency": "EUR"}}
- leitor:b: passagens ccp:art21.1, ccp:art21.1.b; condições [{"field": "tipo_contrato", "op": "not_in", "value": ["bens", "concessao_obras", "concessao_servicos", "obras", "servicos"]}, {"field": "tipo_procedimento", "op": "eq", "value": "consulta_previa"}]; params {"threshold": {"field": "preco_base", "comparator": "lt", "value": 130000, "currency": "EUR"}}

## regra:ccp:auto-limiar-art21-1-c@v1

- leitor:a13: passagens ccp:art21.1.c; condições [{"field": "tipo_contrato", "op": "not_in", "value": ["concessao_obras", "concessao_servicos"]}, {"field": "tipo_procedimento", "op": "eq", "value": "ajuste_direto"}]; params {"threshold": {"field": "preco_base", "comparator": "lt", "value": 75000, "currency": "EUR"}}
- leitor:b: passagens ccp:art21.1, ccp:art21.1.c; condições [{"field": "tipo_contrato", "op": "not_in", "value": ["bens", "concessao_obras", "concessao_servicos", "obras", "servicos"]}, {"field": "tipo_procedimento", "op": "eq", "value": "ajuste_direto"}]; params {"threshold": {"field": "preco_base", "comparator": "lt", "value": 75000, "currency": "EUR"}}

## regra:ccp:auto-limiar-art31-4@v1

- leitor:a13: passagens ccp:art31.4; condições [{"field": "tipo_contrato", "op": "in", "value": ["concessao_obras", "servicos"]}]; params {"threshold": {"field": "preco_base", "comparator": "lt", "value": 1000000, "currency": "EUR"}}
- leitor:b: passagens ccp:art31.4; condições [{"field": "tipo_contrato", "op": "in", "value": ["concessao_obras", "concessao_servicos"]}, {"field": "tipo_procedimento", "op": "in", "value": ["ajuste_direto", "consulta_previa"]}]; params {"threshold": {"field": "preco_base", "comparator": "lt", "value": 1000000, "currency": "EUR"}}

## regra:ccp:auto-limiar-art54-a-1-b-ii@v1

- leitor:a13: passagens ccp:art54-a.1.b.ii; condições []; params {"threshold": {"field": "preco_base", "comparator": "lt", "value": 500000, "currency": "EUR"}}
- leitor:b: passagens ccp:art54-a.1.b.ii; condições [{"field": "tipo_contrato", "op": "in", "value": ["concessao_obras", "concessao_servicos", "obras"]}]; params {"threshold": {"field": "preco_base", "comparator": "lt", "value": 500000, "currency": "EUR"}}

## regra:ccp:auto-limiar-art88-2-a@v1

- leitor:a13: passagens ccp:art88.2.a; condições []; params {"threshold": {"field": "preco_base", "comparator": "lt", "value": 1000000, "currency": "EUR"}}
- leitor:b: passagens ccp:art88.2.a; condições []; params {"threshold": {"field": "preco_base", "comparator": "lt", "value": 1000000, "currency": "EUR"}}

## regra:ccp:auto-prazo-minimo-art174-3@v1

- leitor:a13: passagens ccp:art174.3; condições [{"field": "publicado_joue", "op": "eq", "value": true}, {"field": "setores_especiais", "op": "eq", "value": true}, {"field": "tipo_contrato", "op": "not_in", "value": ["concessao_obras", "concessao_servicos"]}, {"field": "tipo_procedimento", "op": "eq", "value": "concurso_limitado_previa_qualificacao"}]; params {"minimum_days": 15, "deadline_field": "prazo_candidaturas_dias", "counted_from": "data_envio_anuncio", "usual_days": 30}
- leitor:b: passagens ccp:art174.3; condições [{"field": "publicado_joue", "op": "eq", "value": true}, {"field": "setores_especiais", "op": "eq", "value": true}, {"field": "tipo_procedimento", "op": "eq", "value": "concurso_limitado_previa_qualificacao"}]; params {"minimum_days": 15, "deadline_field": "prazo_candidaturas_dias", "counted_from": "data_envio_anuncio", "usual_days": 30}

## regra:ccp:auto-prazo-minimo-art192-2@v1

- leitor:a13: passagens ccp:art192.2; condições [{"field": "tipo_procedimento", "op": "eq", "value": "concurso_limitado_previa_qualificacao"}]; params {"minimum_days": 10, "deadline_field": "prazo_propostas_dias", "counted_from": "data_envio_convite"}
- leitor:b: passagens ccp:art192.1, ccp:art192.2; condições [{"field": "setores_especiais", "op": "eq", "value": true}, {"field": "tipo_procedimento", "op": "eq", "value": "concurso_limitado_previa_qualificacao"}]; params {"minimum_days": 10, "deadline_field": "prazo_propostas_dias", "counted_from": "data_envio_convite"}

## regra:ccp:auto-prazo-minimo-art198-1@v1

- leitor:a13: passagens ccp:art198.1; condições [{"field": "data_inicio_procedimento", "op": "eq", "value": "2026-10-01"}]; params {"minimum_days": 30, "deadline_field": "prazo_candidaturas_dias", "counted_from": "data_envio_anuncio"}
- leitor:b: passagens ccp:art198.1; condições [{"field": "publicado_joue", "op": "eq", "value": true}, {"field": "tipo_procedimento", "op": "eq", "value": "procedimento_negociacao"}]; params {"minimum_days": 30, "deadline_field": "prazo_candidaturas_dias", "counted_from": "data_envio_anuncio"}

## regra:ccp:auto-prazo-minimo-art198-2@v1

- leitor:a13: passagens ccp:art198.2; condições [{"field": "anuncio_pre_informacao", "op": "eq", "value": true}]; params {"minimum_days": 25, "deadline_field": "prazo_candidaturas_dias", "counted_from": "data_envio_convite"}
- leitor:b: passagens ccp:art198.2; condições [{"field": "anuncio_pre_informacao", "op": "eq", "value": true}, {"field": "tipo_procedimento", "op": "eq", "value": "procedimento_negociacao"}]; params {"minimum_days": 25, "deadline_field": "prazo_candidaturas_dias", "counted_from": "data_envio_convite"}

## regra:ccp:auto-prazo-minimo-art241-b-3-b@v1

- leitor:a13: passagens ccp:art241-b.3.b; condições [{"field": "tipo_procedimento", "op": "eq", "value": "concurso_concecao"}]; params {"minimum_days": 10, "deadline_field": "prazo_propostas_dias", "counted_from": "nao_indicado"}
- leitor:b: passagens ccp:art241-b.3.b; condições []; params {"minimum_days": 10, "deadline_field": "prazo_propostas_dias", "counted_from": "nao_indicado"}

