# FÁBRICA DE REGRAS — ronda 1 (DECISIONS D58)

Gerado por tools/rule_factory.py (ccp-rule-factory-0.2). Alvos gerados por código a partir do CCP em vigor a 2026-10-01: cada passagem-folha que fixa um número mínimo de dias ou um limite em euros, fora dos artigos lidos à mão (19.º, 20.º, 135.º, 136.º). Propõe leitor:a8 (AMALIA + adaptador v7), leitor:b revê às cegas; só fica settled a leitura que leitor:b replica em forma canónica (D43).

D59: a passagem que diz o que o vocabulário das regras não tem (prazo de candidaturas, contagem desde o convite, urgência, procedimento fora do vocabulário) é marcada por código. Na ronda 1 as 4 leituras que ficaram settled eram todas destas: as duas famílias escolheram o valor mais próximo que o schema tinha. Foram invalidadas (stale) por esta ferramenta, com a razão no registo; o schema cresce antes da ronda 2.

| regra | passagem | estado | exato | direção | lacunas do vocabulário |
|---|---|---|---|---|---|
| regra:ccp:auto-limiar-art127-c-1-a@v1 | ccp:art127-c.1.a | proposed | não | sim | — |
| regra:ccp:auto-limiar-art17-b-4@v1 | ccp:art17-b.4 | proposed | não | não | — |
| regra:ccp:auto-limiar-art21-1-b@v1 | ccp:art21.1.b | sem leitura válida de leitor:a8 | — | — | — |
| regra:ccp:auto-limiar-art21-1-c@v1 | ccp:art21.1.c | sem leitura válida de leitor:a8 | — | — | — |
| regra:ccp:auto-limiar-art31-4@v1 | ccp:art31.4 | proposed | não | sim | — |
| regra:ccp:auto-limiar-art54-a-1-b-ii@v1 | ccp:art54-a.1.b.ii | proposed | não | sim | — |
| regra:ccp:auto-limiar-art88-2-a@v1 | ccp:art88.2.a | proposed | não | sim | — |
| regra:ccp:auto-prazo-minimo-art174-1@v1 | ccp:art174.1 | stale | sim | sim | prazo de candidaturas (o schema só tem prazo_propostas_dias) |
| regra:ccp:auto-prazo-minimo-art174-2@v1 | ccp:art174.2 | proposed | não | sim | urgência (sem campo no vocabulário) |
| regra:ccp:auto-prazo-minimo-art174-3@v1 | ccp:art174.3 | proposed | não | sim | prazo de candidaturas (o schema só tem prazo_propostas_dias) |
| regra:ccp:auto-prazo-minimo-art190-1@v1 | ccp:art190.1 | proposed | não | sim | conta-se do envio do convite (o schema só tem anúncio) |
| regra:ccp:auto-prazo-minimo-art191-1@v1 | ccp:art191.1 | stale | sim | sim | conta-se do envio do convite (o schema só tem anúncio) |
| regra:ccp:auto-prazo-minimo-art191-5@v1 | ccp:art191.5 | proposed | não | sim | urgência (sem campo no vocabulário) |
| regra:ccp:auto-prazo-minimo-art192-2@v1 | ccp:art192.2 | proposed | não | sim | conta-se do envio do convite (o schema só tem anúncio) |
| regra:ccp:auto-prazo-minimo-art198-1@v1 | ccp:art198.1 | proposed | não | sim | prazo de candidaturas (o schema só tem prazo_propostas_dias) |
| regra:ccp:auto-prazo-minimo-art198-2@v1 | ccp:art198.2 | proposed | não | sim | prazo de candidaturas (o schema só tem prazo_propostas_dias); conta-se do envio do convite (o schema só tem anúncio) |
| regra:ccp:auto-prazo-minimo-art218@v1 | ccp:art218 | stale | sim | sim | conta-se do envio do convite (o schema só tem anúncio) |
| regra:ccp:auto-prazo-minimo-art219-b-5@v1 | ccp:art219-b.5 | proposed | não | sim | procedimento fora do vocabulário (conceção, ideias, simplificado) |
| regra:ccp:auto-prazo-minimo-art219-j-3@v1 | ccp:art219-j.3 | stale | sim | sim | procedimento fora do vocabulário (conceção, ideias, simplificado) |
| regra:ccp:auto-prazo-minimo-art241-b-3-b@v1 | ccp:art241-b.3.b | proposed | não | sim | — |

## regra:ccp:auto-limiar-art127-c-1-a@v1

- leitor:a8: passagens ccp:art127-c.1.a; condições [{"field": "preco_base", "op": "ge", "value": 2000000}, {"field": "tipo_contrato", "op": "in", "value": ["concessao_obras", "concessao_servicos", "obras"]}, {"field": "tipo_procedimento", "op": "eq", "value": "consulta_previa"}]; params {"threshold": {"field": "preco_base", "comparator": "le", "value": 2000000, "currency": "EUR"}}
- leitor:b: passagens ccp:art127-c.1, ccp:art127-c.1.a; condições [{"field": "tipo_contrato", "op": "in", "value": ["concessao_obras", "concessao_servicos", "obras"]}, {"field": "tipo_procedimento", "op": "eq", "value": "consulta_previa"}]; params {"threshold": {"field": "preco_base", "comparator": "lt", "value": 2000000, "currency": "EUR"}}

## regra:ccp:auto-limiar-art17-b-4@v1

- leitor:a8: passagens ccp:art17-b.4; condições [{"field": "preco_base", "op": "le", "value": 1000000}, {"field": "preco_base", "op": "lt", "value": 80000}, {"field": "tipo_contrato", "op": "in", "value": ["bens", "obras"]}]; params {"threshold": {"field": "preco_base", "comparator": "le", "value": 1000000, "currency": "EUR"}}
- leitor:b: passagens ccp:art17-b.4; condições [{"field": "tipo_contrato", "op": "in", "value": ["bens", "servicos"]}]; params {"threshold": {"field": "preco_base", "comparator": "lt", "value": 80000, "currency": "EUR"}}

## regra:ccp:auto-limiar-art21-1-b@v1

- leitor:a8: —
- leitor:b: passagens ccp:art21.1, ccp:art21.1.b; condições [{"field": "tipo_contrato", "op": "not_in", "value": ["bens", "concessao_obras", "concessao_servicos", "obras", "servicos"]}, {"field": "tipo_procedimento", "op": "eq", "value": "consulta_previa"}]; params {"threshold": {"field": "preco_base", "comparator": "lt", "value": 130000, "currency": "EUR"}}

## regra:ccp:auto-limiar-art21-1-c@v1

- leitor:a8: —
- leitor:b: passagens ccp:art21.1, ccp:art21.1.c; condições [{"field": "data_inicio_procedimento", "op": "ge", "value": "2026-10-01"}, {"field": "tipo_contrato", "op": "not_in", "value": ["bens", "concessao_obras", "concessao_servicos", "obras", "servicos"]}, {"field": "tipo_procedimento", "op": "eq", "value": "ajuste_direto"}]; params {"threshold": {"field": "preco_base", "comparator": "lt", "value": 75000, "currency": "EUR"}}

## regra:ccp:auto-limiar-art31-4@v1

- leitor:a8: passagens ccp:art31.4; condições [{"field": "data_inicio_procedimento", "op": "ge", "value": "2026-10-01"}, {"field": "preco_base", "op": "lt", "value": 1000000}, {"field": "tipo_contrato", "op": "in", "value": ["concessao_obras", "concessao_servicos"]}]; params {"threshold": {"field": "preco_base", "comparator": "lt", "value": 1000000, "currency": "EUR"}}
- leitor:b: passagens ccp:art31.4; condições [{"field": "tipo_contrato", "op": "in", "value": ["concessao_obras", "concessao_servicos"]}, {"field": "tipo_procedimento", "op": "in", "value": ["ajuste_direto", "consulta_previa"]}]; params {"threshold": {"field": "preco_base", "comparator": "lt", "value": 1000000, "currency": "EUR"}}

## regra:ccp:auto-limiar-art54-a-1-b-ii@v1

- leitor:a8: passagens ccp:art54-a.1.b.ii; condições [{"field": "tipo_contrato", "op": "eq", "value": "obras"}]; params {"threshold": {"field": "preco_base", "comparator": "lt", "value": 500000, "currency": "EUR"}}
- leitor:b: passagens ccp:art54-a.1.b.ii; condições [{"field": "tipo_contrato", "op": "in", "value": ["concessao_obras", "concessao_servicos", "obras"]}]; params {"threshold": {"field": "preco_base", "comparator": "lt", "value": 500000, "currency": "EUR"}}

## regra:ccp:auto-limiar-art88-2-a@v1

- leitor:a8: passagens ccp:art88.2.a; condições [{"field": "preco_base", "op": "ge", "value": 1000000}]; params {"threshold": {"field": "preco_base", "comparator": "lt", "value": 1000000, "currency": "EUR"}}
- leitor:b: passagens ccp:art88.2.a; condições []; params {"threshold": {"field": "preco_base", "comparator": "lt", "value": 1000000, "currency": "EUR"}}

## regra:ccp:auto-prazo-minimo-art174-1@v1

- leitor:a8: passagens ccp:art174.1; condições [{"field": "publicado_joue", "op": "eq", "value": true}, {"field": "tipo_procedimento", "op": "eq", "value": "concurso_limitado_previa_qualificacao"}]; params {"minimum_days": 30, "deadline_field": "prazo_propostas_dias", "counted_from": "data_envio_anuncio"}
- leitor:b: passagens ccp:art174.1; condições [{"field": "publicado_joue", "op": "eq", "value": true}, {"field": "tipo_procedimento", "op": "eq", "value": "concurso_limitado_previa_qualificacao"}]; params {"minimum_days": 30, "deadline_field": "prazo_propostas_dias", "counted_from": "data_envio_anuncio"}

## regra:ccp:auto-prazo-minimo-art174-2@v1

- leitor:a8: passagens ccp:art174.2; condições [{"field": "publicado_joue", "op": "eq", "value": true}, {"field": "tipo_procedimento", "op": "eq", "value": "concurso_limitado_previa_qualificacao"}]; params {"minimum_days": 15, "deadline_field": "prazo_propostas_dias", "counted_from": "data_envio_anuncio"}
- leitor:b: passagens ccp:art174.1, ccp:art174.2; condições [{"field": "publicado_joue", "op": "eq", "value": true}, {"field": "tipo_procedimento", "op": "eq", "value": "concurso_limitado_previa_qualificacao"}]; params {"minimum_days": 15, "deadline_field": "prazo_propostas_dias", "counted_from": "data_envio_anuncio"}

## regra:ccp:auto-prazo-minimo-art174-3@v1

- leitor:a8: passagens ccp:art174.3; condições [{"field": "publicado_joue", "op": "eq", "value": true}, {"field": "tipo_contrato", "op": "in", "value": ["servicos"]}, {"field": "tipo_procedimento", "op": "eq", "value": "concurso_limitado_previa_qualificacao"}]; params {"minimum_days": 30, "deadline_field": "prazo_propostas_dias", "counted_from": "data_envio_anuncio"}
- leitor:b: passagens ccp:art174.3; condições [{"field": "publicado_joue", "op": "eq", "value": true}, {"field": "tipo_procedimento", "op": "eq", "value": "concurso_limitado_previa_qualificacao"}]; params {"minimum_days": 30, "deadline_field": "prazo_propostas_dias", "counted_from": "data_envio_anuncio"}

## regra:ccp:auto-prazo-minimo-art190-1@v1

- leitor:a8: passagens ccp:art190.1; condições [{"field": "publicado_joue", "op": "eq", "value": false}, {"field": "tipo_contrato", "op": "eq", "value": "obras"}, {"field": "tipo_procedimento", "op": "eq", "value": "concurso_limitado_previa_qualificacao"}]; params {"minimum_days": 6, "deadline_field": "prazo_propostas_dias", "counted_from": "data_envio_anuncio"}
- leitor:b: passagens ccp:art190.1; condições [{"field": "publicado_joue", "op": "eq", "value": false}, {"field": "tipo_contrato", "op": "ne", "value": "obras"}, {"field": "tipo_procedimento", "op": "eq", "value": "concurso_limitado_previa_qualificacao"}]; params {"minimum_days": 6, "deadline_field": "prazo_propostas_dias", "counted_from": "data_envio_anuncio"}

## regra:ccp:auto-prazo-minimo-art191-1@v1

- leitor:a8: passagens ccp:art191.1; condições [{"field": "publicado_joue", "op": "eq", "value": true}, {"field": "tipo_procedimento", "op": "eq", "value": "concurso_limitado_previa_qualificacao"}]; params {"minimum_days": 25, "deadline_field": "prazo_propostas_dias", "counted_from": "data_envio_anuncio"}
- leitor:b: passagens ccp:art191.1; condições [{"field": "publicado_joue", "op": "eq", "value": true}, {"field": "tipo_procedimento", "op": "eq", "value": "concurso_limitado_previa_qualificacao"}]; params {"minimum_days": 25, "deadline_field": "prazo_propostas_dias", "counted_from": "data_envio_anuncio"}

## regra:ccp:auto-prazo-minimo-art191-5@v1

- leitor:a8: passagens ccp:art191.5; condições [{"field": "preco_base", "op": "eq", "value": 0}, {"field": "publicado_joue", "op": "eq", "value": true}, {"field": "tipo_procedimento", "op": "eq", "value": "concurso_limitado_previa_qualificacao"}]; params {"minimum_days": 10, "deadline_field": "prazo_propostas_dias", "counted_from": "data_envio_anuncio"}
- leitor:b: passagens ccp:art191.1, ccp:art191.5; condições [{"field": "publicado_joue", "op": "eq", "value": true}, {"field": "tipo_procedimento", "op": "eq", "value": "concurso_limitado_previa_qualificacao"}]; params {"minimum_days": 10, "deadline_field": "prazo_propostas_dias", "counted_from": "data_envio_anuncio"}

## regra:ccp:auto-prazo-minimo-art192-2@v1

- leitor:a8: passagens ccp:art192.2; condições [{"field": "tipo_procedimento", "op": "eq", "value": "concurso_limitado_previa_qualificacao"}]; params {"minimum_days": 10, "deadline_field": "prazo_propostas_dias", "counted_from": "data_envio_anuncio"}
- leitor:b: passagens ccp:art192.1, ccp:art192.2; condições [{"field": "tipo_procedimento", "op": "eq", "value": "concurso_limitado_previa_qualificacao"}]; params {"minimum_days": 10, "deadline_field": "prazo_propostas_dias", "counted_from": "data_envio_anuncio"}

## regra:ccp:auto-prazo-minimo-art198-1@v1

- leitor:a8: passagens ccp:art198.1; condições [{"field": "tipo_procedimento", "op": "eq", "value": "concurso_publico"}]; params {"minimum_days": 30, "deadline_field": "prazo_propostas_dias", "counted_from": "data_envio_anuncio"}
- leitor:b: passagens ccp:art198.1; condições [{"field": "publicado_joue", "op": "eq", "value": true}, {"field": "tipo_procedimento", "op": "eq", "value": "procedimento_negociacao"}]; params {"minimum_days": 30, "deadline_field": "prazo_propostas_dias", "counted_from": "data_envio_anuncio"}

## regra:ccp:auto-prazo-minimo-art198-2@v1

- leitor:a8: passagens ccp:art198.2; condições [{"field": "publicado_joue", "op": "eq", "value": false}]; params {"minimum_days": 25, "deadline_field": "prazo_propostas_dias", "counted_from": "data_envio_anuncio"}
- leitor:b: passagens ccp:art198.2; condições [{"field": "tipo_procedimento", "op": "eq", "value": "procedimento_negociacao"}]; params {"minimum_days": 25, "deadline_field": "prazo_propostas_dias", "counted_from": "data_envio_anuncio"}

## regra:ccp:auto-prazo-minimo-art218@v1

- leitor:a8: passagens ccp:art218; condições [{"field": "tipo_procedimento", "op": "eq", "value": "dialogo_concorrencial"}]; params {"minimum_days": 30, "deadline_field": "prazo_propostas_dias", "counted_from": "data_envio_anuncio"}
- leitor:b: passagens ccp:art218; condições [{"field": "tipo_procedimento", "op": "eq", "value": "dialogo_concorrencial"}]; params {"minimum_days": 30, "deadline_field": "prazo_propostas_dias", "counted_from": "data_envio_anuncio"}

## regra:ccp:auto-prazo-minimo-art219-b-5@v1

- leitor:a8: passagens ccp:art219-b.5; condições [{"field": "tipo_procedimento", "op": "in", "value": ["concurso_limitado_previa_qualificacao", "concurso_publico"]}, {"field": "tipo_procedimento", "op": "ne", "value": "concurso_limitado_previa_qualificacao"}]; params {"minimum_days": 30, "deadline_field": "prazo_propostas_dias", "counted_from": "data_publicacao_anuncio"}
- leitor:b: passagens ccp:art219-b.5; condições [{"field": "tipo_procedimento", "op": "in", "value": ["concurso_limitado_previa_qualificacao", "concurso_publico"]}]; params {"minimum_days": 30, "deadline_field": "prazo_propostas_dias", "counted_from": "data_publicacao_anuncio"}

## regra:ccp:auto-prazo-minimo-art219-j-3@v1

- leitor:a8: passagens ccp:art219-j.3; condições []; params {"minimum_days": 60, "deadline_field": "prazo_propostas_dias", "counted_from": "data_publicacao_anuncio"}
- leitor:b: passagens ccp:art219-j.3; condições []; params {"minimum_days": 60, "deadline_field": "prazo_propostas_dias", "counted_from": "data_publicacao_anuncio"}

## regra:ccp:auto-prazo-minimo-art241-b-3-b@v1

- leitor:a8: passagens ccp:art241-b.3.b; condições []; params {"minimum_days": 10, "deadline_field": "prazo_propostas_dias", "counted_from": "data_publicacao_anuncio"}
- leitor:b: passagens ccp:art241-b.3.b; condições []; params {"minimum_days": 10, "deadline_field": "prazo_propostas_dias", "counted_from": "data_envio_anuncio"}

