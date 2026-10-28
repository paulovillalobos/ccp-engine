# FÁBRICA DE REGRAS — ronda 4 (DECISIONS D63)

Gerado por tools/rule_factory.py (ccp-rule-factory-0.5). D63: AMALIA aprendeu a ler regras (adaptador v10, treinado em artigos escritos para isso, nunca nas leituras de leitor:b). Alvos: todos os da ronda 1 que não estavam settled quando o treino começou, com o vocabulário da ronda 3. Propõe leitor:a12 (AMALIA + adaptador v10), leitor:b revê às cegas; só fica settled a leitura que leitor:b replica em forma canónica (D43).

Uma regra já no registo recebe uma correção (nova revisão) de leitor:a12; leitor:b lê de novo às cegas.

| regra | passagem | estado | exato | direção | lacunas do vocabulário |
|---|---|---|---|---|---|
| regra:ccp:auto-limiar-art127-c-1-a@v1 | ccp:art127-c.1.a | proposed | não | sim | — |
| regra:ccp:auto-limiar-art17-b-4@v1 | ccp:art17-b.4 | proposed (2 regras) | não | não | — |
| regra:ccp:auto-limiar-art21-1-b@v1 | ccp:art21.1.b | proposed | não | sim | — |
| regra:ccp:auto-limiar-art21-1-c@v1 | ccp:art21.1.c | proposed | não | sim | — |
| regra:ccp:auto-limiar-art31-4@v1 | ccp:art31.4 | proposed | não | sim | — |
| regra:ccp:auto-limiar-art54-a-1-b-ii@v1 | ccp:art54-a.1.b.ii | proposed | não | sim | — |
| regra:ccp:auto-limiar-art88-2-a@v1 | ccp:art88.2.a | proposed | não | sim | — |
| regra:ccp:auto-prazo-minimo-art174-2@v1 | ccp:art174.2 | proposed | não | sim | — |
| regra:ccp:auto-prazo-minimo-art174-3@v1 | ccp:art174.3 | proposed | não | não | — |
| regra:ccp:auto-prazo-minimo-art190-1@v1 | ccp:art190.1 | settled (2 regras) | sim | sim | — |
| regra:ccp:auto-prazo-minimo-art191-1@v1 | ccp:art191.1 | settled | sim | sim | — |
| regra:ccp:auto-prazo-minimo-art191-5@v1 | ccp:art191.5 | proposed | não | sim | — |
| regra:ccp:auto-prazo-minimo-art192-2@v1 | ccp:art192.2 | proposed | não | sim | — |
| regra:ccp:auto-prazo-minimo-art198-1@v1 | ccp:art198.1 | proposed | não | sim | — |
| regra:ccp:auto-prazo-minimo-art198-2@v1 | ccp:art198.2 | proposed | não | sim | — |
| regra:ccp:auto-prazo-minimo-art219-b-5@v1 | ccp:art219-b.5 | settled (2 regras) | sim | sim | — |
| regra:ccp:auto-prazo-minimo-art219-j-3@v1 | ccp:art219-j.3 | settled | sim | sim | — |
| regra:ccp:auto-prazo-minimo-art241-b-3-b@v1 | ccp:art241-b.3.b | proposed | não | sim | — |

## regra:ccp:auto-limiar-art127-c-1-a@v1

- leitor:a12: passagens ccp:art127-c.1.a; condições [{"field": "tipo_contrato", "op": "in", "value": ["concessao_obras", "concessao_servicos", "obras"]}, {"field": "tipo_procedimento", "op": "eq", "value": "consulta_previa"}]; params {"threshold": {"field": "preco_base", "comparator": "le", "value": 2000000, "currency": "EUR"}}
- leitor:b: passagens ccp:art127-c.1, ccp:art127-c.1.a; condições [{"field": "tipo_contrato", "op": "in", "value": ["concessao_obras", "concessao_servicos", "obras"]}, {"field": "tipo_procedimento", "op": "eq", "value": "consulta_previa"}]; params {"threshold": {"field": "preco_base", "comparator": "lt", "value": 2000000, "currency": "EUR"}}

## regra:ccp:auto-limiar-art17-b-4@v1

- leitor:a12: passagens ccp:art17-b.4; condições [{"field": "tipo_contrato", "op": "eq", "value": "bens"}, {"field": "tipo_procedimento", "op": "in", "value": ["ajuste_direto", "concurso_limitado_previa_qualificacao", "concurso_publico"]}]; params {"threshold": {"field": "preco_base", "comparator": "lt", "value": 80000, "currency": "EUR"}} || passagens ccp:art17-b.4; condições [{"field": "tipo_contrato", "op": "eq", "value": "obras"}, {"field": "tipo_procedimento", "op": "in", "value": ["concurso_limitado_previa_qualificacao", "concurso_publico"]}]; params {"threshold": {"field": "preco_base", "comparator": "lt", "value": 1000000, "currency": "EUR"}}
- leitor:b: passagens ccp:art17-b.4; condições [{"field": "tipo_contrato", "op": "eq", "value": "obras"}]; params {"threshold": {"field": "preco_base", "comparator": "lt", "value": 1000000, "currency": "EUR"}} || passagens ccp:art17-b.4; condições [{"field": "tipo_contrato", "op": "in", "value": ["bens", "servicos"]}]; params {"threshold": {"field": "preco_base", "comparator": "lt", "value": 80000, "currency": "EUR"}}

## regra:ccp:auto-limiar-art21-1-b@v1

- leitor:a12: passagens ccp:art21.1.b; condições [{"field": "tipo_contrato", "op": "ne", "value": "concessao_obras"}, {"field": "tipo_procedimento", "op": "eq", "value": "consulta_previa"}]; params {"threshold": {"field": "preco_base", "comparator": "lt", "value": 130000, "currency": "EUR"}}
- leitor:b: passagens ccp:art21.1, ccp:art21.1.b; condições [{"field": "tipo_contrato", "op": "not_in", "value": ["bens", "concessao_obras", "concessao_servicos", "obras", "servicos"]}, {"field": "tipo_procedimento", "op": "eq", "value": "consulta_previa"}]; params {"threshold": {"field": "preco_base", "comparator": "lt", "value": 130000, "currency": "EUR"}}

## regra:ccp:auto-limiar-art21-1-c@v1

- leitor:a12: passagens ccp:art21.1.c; condições [{"field": "tipo_contrato", "op": "ne", "value": "concessao_obras"}, {"field": "tipo_procedimento", "op": "eq", "value": "ajuste_direto"}]; params {"threshold": {"field": "preco_base", "comparator": "lt", "value": 75000, "currency": "EUR"}}
- leitor:b: passagens ccp:art21.1, ccp:art21.1.c; condições [{"field": "tipo_contrato", "op": "not_in", "value": ["bens", "concessao_obras", "concessao_servicos", "obras", "servicos"]}, {"field": "tipo_procedimento", "op": "eq", "value": "ajuste_direto"}]; params {"threshold": {"field": "preco_base", "comparator": "lt", "value": 75000, "currency": "EUR"}}

## regra:ccp:auto-limiar-art31-4@v1

- leitor:a12: passagens ccp:art31.4; condições [{"field": "tipo_contrato", "op": "eq", "value": "concessao_obras"}, {"field": "tipo_procedimento", "op": "in", "value": ["ajuste_direto", "consulta_previa"]}]; params {"threshold": {"field": "preco_base", "comparator": "lt", "value": 1000000, "currency": "EUR"}}
- leitor:b: passagens ccp:art31.4; condições [{"field": "tipo_contrato", "op": "in", "value": ["concessao_obras", "concessao_servicos"]}, {"field": "tipo_procedimento", "op": "in", "value": ["ajuste_direto", "consulta_previa"]}]; params {"threshold": {"field": "preco_base", "comparator": "lt", "value": 1000000, "currency": "EUR"}}

## regra:ccp:auto-limiar-art54-a-1-b-ii@v1

- leitor:a12: passagens ccp:art54-a.1.b.ii; condições [{"field": "tipo_contrato", "op": "in", "value": ["concessao_obras", "concessao_servicos", "obras", "servicos"]}, {"field": "tipo_procedimento", "op": "in", "value": ["ajuste_direto", "concurso_limitado_previa_qualificacao", "concurso_publico", "dialogo_concorrencial", "parceria_inovacao"]}]; params {"threshold": {"field": "preco_base", "comparator": "lt", "value": 500000, "currency": "EUR"}}
- leitor:b: passagens ccp:art54-a.1.b.ii; condições [{"field": "tipo_contrato", "op": "in", "value": ["concessao_obras", "concessao_servicos", "obras"]}]; params {"threshold": {"field": "preco_base", "comparator": "lt", "value": 500000, "currency": "EUR"}}

## regra:ccp:auto-limiar-art88-2-a@v1

- leitor:a12: passagens ccp:art88.2.a; condições [{"field": "preco_base", "op": "lt", "value": 1000000}]; params {"threshold": {"field": "preco_base", "comparator": "lt", "value": 1000000, "currency": "EUR"}}
- leitor:b: passagens ccp:art88.2.a; condições []; params {"threshold": {"field": "preco_base", "comparator": "lt", "value": 1000000, "currency": "EUR"}}

## regra:ccp:auto-prazo-minimo-art174-2@v1

- leitor:a12: passagens ccp:art174.2; condições [{"field": "publicado_joue", "op": "eq", "value": true}, {"field": "tipo_procedimento", "op": "eq", "value": "concurso_limitado_previa_qualificacao"}, {"field": "urgencia_fundamentada", "op": "eq", "value": true}]; params {"minimum_days": 15, "deadline_field": "prazo_candidaturas_dias", "counted_from": "data_envio_anuncio"}
- leitor:b: passagens ccp:art174.1, ccp:art174.2; condições [{"field": "publicado_joue", "op": "eq", "value": true}, {"field": "tipo_procedimento", "op": "eq", "value": "concurso_limitado_previa_qualificacao"}, {"field": "urgencia_fundamentada", "op": "eq", "value": true}]; params {"minimum_days": 15, "deadline_field": "prazo_candidaturas_dias", "counted_from": "data_envio_anuncio"}

## regra:ccp:auto-prazo-minimo-art174-3@v1

- leitor:a12: passagens ccp:art174.3; condições [{"field": "setores_especiais", "op": "eq", "value": true}, {"field": "tipo_contrato", "op": "in", "value": ["concessao_obras", "concessao_servicos", "servicos_sociais"]}, {"field": "tipo_procedimento", "op": "eq", "value": "concurso_limitado_previa_qualificacao"}]; params {"minimum_days": 30, "deadline_field": "prazo_candidaturas_dias", "counted_from": "data_envio_anuncio", "usual_days": 30}
- leitor:b: passagens ccp:art174.3; condições [{"field": "publicado_joue", "op": "eq", "value": true}, {"field": "setores_especiais", "op": "eq", "value": true}, {"field": "tipo_procedimento", "op": "eq", "value": "concurso_limitado_previa_qualificacao"}]; params {"minimum_days": 15, "deadline_field": "prazo_candidaturas_dias", "counted_from": "data_envio_anuncio", "usual_days": 30}

## regra:ccp:auto-prazo-minimo-art190-1@v1

- leitor:a12: passagens ccp:art190.1; condições [{"field": "publicado_joue", "op": "eq", "value": false}, {"field": "tipo_contrato", "op": "eq", "value": "obras"}, {"field": "tipo_procedimento", "op": "eq", "value": "concurso_limitado_previa_qualificacao"}]; params {"minimum_days": 14, "deadline_field": "prazo_propostas_dias", "counted_from": "data_envio_convite"} || passagens ccp:art190.1; condições [{"field": "publicado_joue", "op": "eq", "value": false}, {"field": "tipo_contrato", "op": "ne", "value": "obras"}, {"field": "tipo_procedimento", "op": "eq", "value": "concurso_limitado_previa_qualificacao"}]; params {"minimum_days": 6, "deadline_field": "prazo_propostas_dias", "counted_from": "data_envio_convite"}
- leitor:b: passagens ccp:art190.1; condições [{"field": "publicado_joue", "op": "eq", "value": false}, {"field": "tipo_contrato", "op": "eq", "value": "obras"}, {"field": "tipo_procedimento", "op": "eq", "value": "concurso_limitado_previa_qualificacao"}]; params {"minimum_days": 14, "deadline_field": "prazo_propostas_dias", "counted_from": "data_envio_convite"} || passagens ccp:art190.1; condições [{"field": "publicado_joue", "op": "eq", "value": false}, {"field": "tipo_contrato", "op": "ne", "value": "obras"}, {"field": "tipo_procedimento", "op": "eq", "value": "concurso_limitado_previa_qualificacao"}]; params {"minimum_days": 6, "deadline_field": "prazo_propostas_dias", "counted_from": "data_envio_convite"}

## regra:ccp:auto-prazo-minimo-art191-1@v1

- leitor:a12: passagens ccp:art191.1; condições [{"field": "publicado_joue", "op": "eq", "value": true}, {"field": "tipo_procedimento", "op": "eq", "value": "concurso_limitado_previa_qualificacao"}]; params {"minimum_days": 25, "deadline_field": "prazo_propostas_dias", "counted_from": "data_envio_convite"}
- leitor:b: passagens ccp:art191.1; condições [{"field": "publicado_joue", "op": "eq", "value": true}, {"field": "tipo_procedimento", "op": "eq", "value": "concurso_limitado_previa_qualificacao"}]; params {"minimum_days": 25, "deadline_field": "prazo_propostas_dias", "counted_from": "data_envio_convite"}

## regra:ccp:auto-prazo-minimo-art191-5@v1

- leitor:a12: passagens ccp:art191.5; condições [{"field": "publicado_joue", "op": "eq", "value": true}, {"field": "tipo_procedimento", "op": "eq", "value": "concurso_limitado_previa_qualificacao"}, {"field": "urgencia_fundamentada", "op": "eq", "value": true}]; params {"minimum_days": 10, "deadline_field": "prazo_propostas_dias", "counted_from": "data_envio_convite"}
- leitor:b: passagens ccp:art191.1, ccp:art191.5; condições [{"field": "publicado_joue", "op": "eq", "value": true}, {"field": "tipo_procedimento", "op": "eq", "value": "concurso_limitado_previa_qualificacao"}, {"field": "urgencia_fundamentada", "op": "eq", "value": true}]; params {"minimum_days": 10, "deadline_field": "prazo_propostas_dias", "counted_from": "data_envio_convite"}

## regra:ccp:auto-prazo-minimo-art192-2@v1

- leitor:a12: passagens ccp:art192.2; condições [{"field": "tipo_procedimento", "op": "eq", "value": "concurso_limitado_previa_qualificacao"}]; params {"minimum_days": 10, "deadline_field": "prazo_propostas_dias", "counted_from": "data_envio_convite"}
- leitor:b: passagens ccp:art192.1, ccp:art192.2; condições [{"field": "setores_especiais", "op": "eq", "value": true}, {"field": "tipo_procedimento", "op": "eq", "value": "concurso_limitado_previa_qualificacao"}]; params {"minimum_days": 10, "deadline_field": "prazo_propostas_dias", "counted_from": "data_envio_convite"}

## regra:ccp:auto-prazo-minimo-art198-1@v1

- leitor:a12: passagens ccp:art198.1; condições [{"field": "publicado_joue", "op": "eq", "value": true}, {"field": "tipo_procedimento", "op": "eq", "value": "concurso_publico"}]; params {"minimum_days": 30, "deadline_field": "prazo_candidaturas_dias", "counted_from": "data_envio_anuncio"}
- leitor:b: passagens ccp:art198.1; condições [{"field": "publicado_joue", "op": "eq", "value": true}, {"field": "tipo_procedimento", "op": "eq", "value": "procedimento_negociacao"}]; params {"minimum_days": 30, "deadline_field": "prazo_candidaturas_dias", "counted_from": "data_envio_anuncio"}

## regra:ccp:auto-prazo-minimo-art198-2@v1

- leitor:a12: passagens ccp:art198.2; condições [{"field": "anuncio_pre_informacao", "op": "eq", "value": true}]; params {"minimum_days": 25, "deadline_field": "prazo_candidaturas_dias", "counted_from": "data_envio_convite"}
- leitor:b: passagens ccp:art198.2; condições [{"field": "anuncio_pre_informacao", "op": "eq", "value": true}, {"field": "tipo_procedimento", "op": "eq", "value": "procedimento_negociacao"}]; params {"minimum_days": 25, "deadline_field": "prazo_candidaturas_dias", "counted_from": "data_envio_convite"}

## regra:ccp:auto-prazo-minimo-art219-b-5@v1

- leitor:a12: passagens ccp:art219-b.5; condições [{"field": "modalidade_concecao", "op": "eq", "value": "simplificado"}, {"field": "tipo_procedimento", "op": "eq", "value": "concurso_concecao"}]; params {"minimum_days": 15, "deadline_field": "prazo_trabalhos_concecao_dias", "counted_from": "nao_indicado"} || passagens ccp:art219-b.5; condições [{"field": "modalidade_concecao", "op": "in", "value": ["limitado", "publico"]}, {"field": "tipo_procedimento", "op": "eq", "value": "concurso_concecao"}]; params {"minimum_days": 30, "deadline_field": "prazo_trabalhos_concecao_dias", "counted_from": "nao_indicado"}
- leitor:b: passagens ccp:art219-b.5; condições [{"field": "modalidade_concecao", "op": "eq", "value": "simplificado"}, {"field": "tipo_procedimento", "op": "eq", "value": "concurso_concecao"}]; params {"minimum_days": 15, "deadline_field": "prazo_trabalhos_concecao_dias", "counted_from": "nao_indicado"} || passagens ccp:art219-b.5; condições [{"field": "modalidade_concecao", "op": "in", "value": ["limitado", "publico"]}, {"field": "tipo_procedimento", "op": "eq", "value": "concurso_concecao"}]; params {"minimum_days": 30, "deadline_field": "prazo_trabalhos_concecao_dias", "counted_from": "nao_indicado"}

## regra:ccp:auto-prazo-minimo-art219-j-3@v1

- leitor:a12: passagens ccp:art219-j.3; condições [{"field": "tipo_procedimento", "op": "eq", "value": "concurso_ideias"}]; params {"minimum_days": 60, "deadline_field": "prazo_propostas_dias", "counted_from": "data_publicacao_anuncio"}
- leitor:b: passagens ccp:art219-j.3; condições [{"field": "tipo_procedimento", "op": "eq", "value": "concurso_ideias"}]; params {"minimum_days": 60, "deadline_field": "prazo_propostas_dias", "counted_from": "data_publicacao_anuncio"}

## regra:ccp:auto-prazo-minimo-art241-b-3-b@v1

- leitor:a12: passagens ccp:art241-b.3.b; condições [{"field": "tipo_contrato", "op": "eq", "value": "bens"}, {"field": "tipo_procedimento", "op": "eq", "value": "ajuste_direto"}]; params {"minimum_days": 10, "deadline_field": "prazo_propostas_dias", "counted_from": "data_envio_convite"}
- leitor:b: passagens ccp:art241-b.3.b; condições []; params {"minimum_days": 10, "deadline_field": "prazo_propostas_dias", "counted_from": "nao_indicado"}

