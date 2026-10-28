# FÁBRICA DE REGRAS — ronda 2 (DECISIONS D60)

Gerado por tools/rule_factory.py (ccp-rule-factory-0.4). D60: o vocabulário das regras ganha prazo_candidaturas_dias e data_envio_convite (o prompt diz o que cada campo quer dizer). Alvos: os da ronda 1 cujas únicas lacunas estes valores fecham. As duas famílias leem de novo às cegas; uma regra já no registo recebe uma correção (nova revisão), não uma segunda proposta. Propõe leitor:a8 (AMALIA + adaptador v7), leitor:b revê às cegas; só fica settled a leitura que leitor:b replica em forma canónica (D43).

Lidas contra a lei, as leituras da ronda 2 mostraram mais três lacunas, agora verificadas por código: setores especiais (art. 174.º n.º 3), anúncio periódico indicativo (art. 198.º n.º 2) e um prazo «em regra» com outro mínimo absoluto (174.º n.º 3: 30 dias em regra, nunca menos de 15; as duas famílias deram 30). Um alvo com uma lacuna ainda aberta é lido e mostrado aqui, não registado.

| regra | passagem | estado | exato | direção | lacunas do vocabulário |
|---|---|---|---|---|---|
| regra:ccp:auto-prazo-minimo-art174-1@v1 | ccp:art174.1 | settled | sim | sim | — |
| regra:ccp:auto-prazo-minimo-art174-3@v1 | ccp:art174.3 | proposed | sim | sim | setores especiais: água, energia, transportes, serviços postais (sem campo no vocabulário); um prazo «em regra» e outro mínimo absoluto (a regra só tem um mínimo) |
| regra:ccp:auto-prazo-minimo-art190-1@v1 | ccp:art190.1 | proposed | não | sim | — |
| regra:ccp:auto-prazo-minimo-art191-1@v1 | ccp:art191.1 | proposed | não | sim | — |
| regra:ccp:auto-prazo-minimo-art192-2@v1 | ccp:art192.2 | proposed | não | sim | — |
| regra:ccp:auto-prazo-minimo-art198-1@v1 | ccp:art198.1 | proposed | não | sim | — |
| regra:ccp:auto-prazo-minimo-art198-2@v1 | ccp:art198.2 | proposed | não | sim | anúncio periódico indicativo / de pré-informação (sem campo no vocabulário) |
| regra:ccp:auto-prazo-minimo-art218@v1 | ccp:art218 | settled | sim | sim | — |

## regra:ccp:auto-prazo-minimo-art174-1@v1

- leitor:a8: passagens ccp:art174.1; condições [{"field": "publicado_joue", "op": "eq", "value": true}, {"field": "tipo_procedimento", "op": "eq", "value": "concurso_limitado_previa_qualificacao"}]; params {"minimum_days": 30, "deadline_field": "prazo_candidaturas_dias", "counted_from": "data_envio_anuncio"}
- leitor:b: passagens ccp:art174.1; condições [{"field": "publicado_joue", "op": "eq", "value": true}, {"field": "tipo_procedimento", "op": "eq", "value": "concurso_limitado_previa_qualificacao"}]; params {"minimum_days": 30, "deadline_field": "prazo_candidaturas_dias", "counted_from": "data_envio_anuncio"}

## regra:ccp:auto-prazo-minimo-art174-3@v1

- leitor:a8: passagens ccp:art174.3; condições [{"field": "publicado_joue", "op": "eq", "value": true}, {"field": "tipo_procedimento", "op": "eq", "value": "concurso_limitado_previa_qualificacao"}]; params {"minimum_days": 30, "deadline_field": "prazo_candidaturas_dias", "counted_from": "data_envio_anuncio"}
- leitor:b: passagens ccp:art174.3; condições [{"field": "publicado_joue", "op": "eq", "value": true}, {"field": "tipo_procedimento", "op": "eq", "value": "concurso_limitado_previa_qualificacao"}]; params {"minimum_days": 30, "deadline_field": "prazo_candidaturas_dias", "counted_from": "data_envio_anuncio"}

## regra:ccp:auto-prazo-minimo-art190-1@v1

- leitor:a8: passagens ccp:art190.1; condições [{"field": "publicado_joue", "op": "eq", "value": false}, {"field": "tipo_procedimento", "op": "eq", "value": "concurso_limitado_previa_qualificacao"}]; params {"minimum_days": 6, "deadline_field": "prazo_propostas_dias", "counted_from": "data_envio_anuncio"}
- leitor:b: passagens ccp:art190.1; condições [{"field": "publicado_joue", "op": "eq", "value": false}, {"field": "tipo_contrato", "op": "ne", "value": "obras"}, {"field": "tipo_procedimento", "op": "eq", "value": "concurso_limitado_previa_qualificacao"}]; params {"minimum_days": 6, "deadline_field": "prazo_propostas_dias", "counted_from": "data_envio_convite"}

## regra:ccp:auto-prazo-minimo-art191-1@v1

- leitor:a8: passagens ccp:art191.1; condições [{"field": "publicado_joue", "op": "eq", "value": true}, {"field": "tipo_procedimento", "op": "eq", "value": "concurso_limitado_previa_qualificacao"}]; params {"minimum_days": 25, "deadline_field": "prazo_propostas_dias", "counted_from": "data_envio_anuncio"}
- leitor:b: passagens ccp:art191.1; condições [{"field": "publicado_joue", "op": "eq", "value": true}, {"field": "tipo_procedimento", "op": "eq", "value": "concurso_limitado_previa_qualificacao"}]; params {"minimum_days": 25, "deadline_field": "prazo_propostas_dias", "counted_from": "data_envio_convite"}

## regra:ccp:auto-prazo-minimo-art192-2@v1

- leitor:a8: passagens ccp:art192.2; condições [{"field": "tipo_procedimento", "op": "eq", "value": "concurso_limitado_previa_qualificacao"}]; params {"minimum_days": 10, "deadline_field": "prazo_propostas_dias", "counted_from": "data_envio_anuncio"}
- leitor:b: passagens ccp:art192.1, ccp:art192.2; condições [{"field": "tipo_procedimento", "op": "eq", "value": "concurso_limitado_previa_qualificacao"}]; params {"minimum_days": 10, "deadline_field": "prazo_propostas_dias", "counted_from": "data_envio_convite"}

## regra:ccp:auto-prazo-minimo-art198-1@v1

- leitor:a8: passagens ccp:art198.1; condições []; params {"minimum_days": 30, "deadline_field": "prazo_candidaturas_dias", "counted_from": "data_envio_anuncio"}
- leitor:b: passagens ccp:art198.1; condições [{"field": "publicado_joue", "op": "eq", "value": true}, {"field": "tipo_procedimento", "op": "eq", "value": "procedimento_negociacao"}]; params {"minimum_days": 30, "deadline_field": "prazo_candidaturas_dias", "counted_from": "data_envio_anuncio"}

## regra:ccp:auto-prazo-minimo-art198-2@v1

- leitor:a8: passagens ccp:art198.2; condições [{"field": "publicado_joue", "op": "eq", "value": true}]; params {"minimum_days": 25, "deadline_field": "prazo_candidaturas_dias", "counted_from": "data_envio_anuncio"}
- leitor:b: passagens ccp:art198.2; condições [{"field": "publicado_joue", "op": "eq", "value": true}, {"field": "tipo_procedimento", "op": "eq", "value": "procedimento_negociacao"}]; params {"minimum_days": 25, "deadline_field": "prazo_candidaturas_dias", "counted_from": "data_envio_convite"}

## regra:ccp:auto-prazo-minimo-art218@v1

- leitor:a8: passagens ccp:art218; condições [{"field": "tipo_procedimento", "op": "eq", "value": "dialogo_concorrencial"}]; params {"minimum_days": 30, "deadline_field": "prazo_propostas_dias", "counted_from": "data_envio_convite"}
- leitor:b: passagens ccp:art218; condições [{"field": "tipo_procedimento", "op": "eq", "value": "dialogo_concorrencial"}]; params {"minimum_days": 30, "deadline_field": "prazo_propostas_dias", "counted_from": "data_envio_convite"}

