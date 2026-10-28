# FÁBRICA DE REGRAS — ronda 3 (DECISIONS D62)

Gerado por tools/rule_factory.py (ccp-rule-factory-0.5). D62: o vocabulário cresce pelas escolhas da pessoa: urgência fundamentada, setores especiais, anúncio periódico indicativo, concurso de conceção e de ideias (com a modalidade e o prazo dos trabalhos de conceção), um prazo «em regra» (usual_days) ao lado do mínimo absoluto, e uma resposta com até três regras. Alvos: os da ronda 1 com uma lacuna que isto fecha, e o 190.º n.º 1 (duas regras numa passagem). Propõe leitor:a8 (AMALIA + adaptador v7), leitor:b revê às cegas; só fica settled a leitura que leitor:b replica em forma canónica (D43).

As leituras replicam quando cada regra replica, os dois conjuntos ordenados pela forma canónica; a 2.ª e a 3.ª regra de um alvo têm ids terminados em -b e -c.

| regra | passagem | estado | exato | direção | lacunas do vocabulário |
|---|---|---|---|---|---|
| regra:ccp:auto-prazo-minimo-art174-2@v1 | ccp:art174.2 | proposed (3 regras) | não | não | — |
| regra:ccp:auto-prazo-minimo-art174-3@v1 | ccp:art174.3 | proposed (2 regras) | não | não | — |
| regra:ccp:auto-prazo-minimo-art190-1@v1 | ccp:art190.1 | proposed (3 regras) | não | não | — |
| regra:ccp:auto-prazo-minimo-art191-5@v1 | ccp:art191.5 | proposed (3 regras) | não | não | — |
| regra:ccp:auto-prazo-minimo-art198-2@v1 | ccp:art198.2 | proposed (3 regras) | não | não | — |
| regra:ccp:auto-prazo-minimo-art219-b-5@v1 | ccp:art219-b.5 | proposed (2 regras) | não | sim | — |
| regra:ccp:auto-prazo-minimo-art219-j-3@v1 | ccp:art219-j.3 | proposed (3 regras) | não | não | — |

## regra:ccp:auto-prazo-minimo-art174-2@v1

- leitor:a8: passagens ccp:art174.2; condições [{"field": "setores_especiais", "op": "eq", "value": true}, {"field": "urgencia_fundamentada", "op": "eq", "value": true}]; params {"minimum_days": 15, "deadline_field": "prazo_candidaturas_dias", "counted_from": "data_envio_anuncio"} || passagens ccp:art174.2; condições [{"field": "setores_especiais", "op": "eq", "value": true}]; params {"minimum_days": 15, "deadline_field": "prazo_candidaturas_dias", "counted_from": "data_envio_anuncio"} || passagens ccp:art174.2; condições [{"field": "urgencia_fundamentada", "op": "eq", "value": true}]; params {"minimum_days": 15, "deadline_field": "prazo_candidaturas_dias", "counted_from": "data_envio_anuncio"}
- leitor:b: passagens ccp:art174.1, ccp:art174.2; condições [{"field": "publicado_joue", "op": "eq", "value": true}, {"field": "tipo_procedimento", "op": "eq", "value": "concurso_limitado_previa_qualificacao"}, {"field": "urgencia_fundamentada", "op": "eq", "value": true}]; params {"minimum_days": 15, "deadline_field": "prazo_candidaturas_dias", "counted_from": "data_envio_anuncio"}

## regra:ccp:auto-prazo-minimo-art174-3@v1

- leitor:a8: passagens ccp:art174.3; condições [{"field": "setores_especiais", "op": "eq", "value": true}]; params {"minimum_days": 30, "deadline_field": "prazo_candidaturas_dias", "counted_from": "data_envio_anuncio", "usual_days": 30} || passagens ccp:art174.3; condições []; params {"minimum_days": 15, "deadline_field": "prazo_candidaturas_dias", "counted_from": "data_envio_anuncio"}
- leitor:b: passagens ccp:art174.3; condições [{"field": "publicado_joue", "op": "eq", "value": true}, {"field": "setores_especiais", "op": "eq", "value": true}, {"field": "tipo_procedimento", "op": "eq", "value": "concurso_limitado_previa_qualificacao"}]; params {"minimum_days": 15, "deadline_field": "prazo_candidaturas_dias", "counted_from": "data_envio_anuncio", "usual_days": 30}

## regra:ccp:auto-prazo-minimo-art190-1@v1

- leitor:a8: passagens ccp:art190.1; condições [{"field": "publicado_joue", "op": "eq", "value": false}, {"field": "tipo_contrato", "op": "eq", "value": "obras"}]; params {"minimum_days": 14, "deadline_field": "prazo_propostas_dias", "counted_from": "data_envio_anuncio"} || passagens ccp:art190.1; condições [{"field": "publicado_joue", "op": "eq", "value": false}, {"field": "tipo_contrato", "op": "eq", "value": "obras"}]; params {"minimum_days": 6, "deadline_field": "prazo_propostas_dias", "counted_from": "data_envio_anuncio", "usual_days": 14} || passagens ccp:art190.1; condições [{"field": "publicado_joue", "op": "eq", "value": false}, {"field": "tipo_contrato", "op": "eq", "value": "obras"}]; params {"minimum_days": 6, "deadline_field": "prazo_candidaturas_dias", "counted_from": "data_envio_convite"}
- leitor:b: passagens ccp:art190.1; condições [{"field": "publicado_joue", "op": "eq", "value": false}, {"field": "tipo_contrato", "op": "eq", "value": "obras"}, {"field": "tipo_procedimento", "op": "eq", "value": "concurso_limitado_previa_qualificacao"}]; params {"minimum_days": 14, "deadline_field": "prazo_propostas_dias", "counted_from": "data_envio_convite"} || passagens ccp:art190.1; condições [{"field": "publicado_joue", "op": "eq", "value": false}, {"field": "tipo_contrato", "op": "ne", "value": "obras"}, {"field": "tipo_procedimento", "op": "eq", "value": "concurso_limitado_previa_qualificacao"}]; params {"minimum_days": 6, "deadline_field": "prazo_propostas_dias", "counted_from": "data_envio_convite"}

## regra:ccp:auto-prazo-minimo-art191-5@v1

- leitor:a8: passagens ccp:art191.2.b; condições [{"field": "anuncio_pre_informacao", "op": "eq", "value": true}]; params {"minimum_days": 10, "deadline_field": "prazo_propostas_dias", "counted_from": "data_envio_anuncio"} || passagens ccp:art191.5; condições [{"field": "urgencia_fundamentada", "op": "eq", "value": true}]; params {"minimum_days": 10, "deadline_field": "prazo_propostas_dias", "counted_from": "data_envio_anuncio"} || passagens ccp:art191.1; condições [{"field": "urgencia_fundamentada", "op": "eq", "value": true}]; params {"minimum_days": 25, "deadline_field": "prazo_propostas_dias", "counted_from": "data_envio_anuncio"}
- leitor:b: passagens ccp:art191.1, ccp:art191.5; condições [{"field": "publicado_joue", "op": "eq", "value": true}, {"field": "tipo_procedimento", "op": "eq", "value": "concurso_limitado_previa_qualificacao"}, {"field": "urgencia_fundamentada", "op": "eq", "value": true}]; params {"minimum_days": 10, "deadline_field": "prazo_propostas_dias", "counted_from": "data_envio_convite"}

## regra:ccp:auto-prazo-minimo-art198-2@v1

- leitor:a8: passagens ccp:art198.2; condições [{"field": "anuncio_pre_informacao", "op": "eq", "value": true}]; params {"minimum_days": 25, "deadline_field": "prazo_candidaturas_dias", "counted_from": "data_envio_anuncio", "usual_days": 30} || passagens ccp:art198.1; condições []; params {"minimum_days": 30, "deadline_field": "prazo_candidaturas_dias", "counted_from": "data_envio_anuncio"} || passagens ccp:art198.3; condições []; params {"minimum_days": 7, "deadline_field": "prazo_candidaturas_dias", "counted_from": "data_envio_anuncio"}
- leitor:b: passagens ccp:art198.2; condições [{"field": "anuncio_pre_informacao", "op": "eq", "value": true}, {"field": "tipo_procedimento", "op": "eq", "value": "procedimento_negociacao"}]; params {"minimum_days": 25, "deadline_field": "prazo_candidaturas_dias", "counted_from": "data_envio_convite"}

## regra:ccp:auto-prazo-minimo-art219-b-5@v1

- leitor:a8: passagens ccp:art219-b.5; condições [{"field": "modalidade_concecao", "op": "eq", "value": "simplificado"}]; params {"minimum_days": 15, "deadline_field": "prazo_candidaturas_dias", "counted_from": "data_envio_convite", "usual_days": 15} || passagens ccp:art219-b.5; condições []; params {"minimum_days": 30, "deadline_field": "prazo_candidaturas_dias", "counted_from": "data_envio_convite", "usual_days": 30}
- leitor:b: passagens ccp:art219-b.5; condições [{"field": "modalidade_concecao", "op": "eq", "value": "simplificado"}, {"field": "tipo_procedimento", "op": "eq", "value": "concurso_concecao"}]; params {"minimum_days": 15, "deadline_field": "prazo_trabalhos_concecao_dias", "counted_from": "nao_indicado"} || passagens ccp:art219-b.5; condições [{"field": "modalidade_concecao", "op": "in", "value": ["limitado", "publico"]}, {"field": "tipo_procedimento", "op": "eq", "value": "concurso_concecao"}]; params {"minimum_days": 30, "deadline_field": "prazo_trabalhos_concecao_dias", "counted_from": "nao_indicado"}

## regra:ccp:auto-prazo-minimo-art219-j-3@v1

- leitor:a8: passagens ccp:art219-j.3; condições []; params {"minimum_days": 60, "deadline_field": "prazo_propostas_dias", "counted_from": "data_publicacao_anuncio"} || passagens ccp:art219-j.3; condições []; params {"minimum_days": 60, "deadline_field": "prazo_propostas_dias", "counted_from": "data_publicacao_anuncio"} || passagens ccp:art219-j.3; condições []; params {"minimum_days": 60, "deadline_field": "prazo_propostas_dias", "counted_from": "data_publicacao_anuncio"}
- leitor:b: passagens ccp:art219-j.3; condições [{"field": "tipo_procedimento", "op": "eq", "value": "concurso_ideias"}]; params {"minimum_days": 60, "deadline_field": "prazo_propostas_dias", "counted_from": "data_publicacao_anuncio"}

