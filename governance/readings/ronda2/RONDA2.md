# RONDA 2 — B3, as quatro regras que o motor precisa primeiro (DECISIONS D44)

Gerado por tools/read_rules.py. As mesmas perguntas e candidatas da ronda 1, com três defeitos do prompt corrigidos (D44); leitor:a corrige a sua proposta, leitor:b revê às cegas. Só fica settled a leitura que leitor:b replica em forma canónica (D43).

| regra | estado | exato | direção |
|---|---|---|---|
| regra:dl-177-2026:seletor-regime@v1 | proposed | não | não |
| regra:ccp:prazo-minimo-concurso-sem-joue-bens-servicos@v1 | proposed | não | sim |
| regra:ccp:prazo-minimo-concurso-sem-joue-obras@v1 | proposed | não | sim |
| regra:ccp:prazo-minimo-concurso-joue@v1 | settled | não | sim |

## regra:dl-177-2026:seletor-regime@v1

- leitor:a: passagens dl-177-2026:art7.2, dl-177-2026:art7.3; condições [{"field": "territorio", "op": "in", "value": ["PT"]}, {"field": "tipo_procedimento", "op": "in", "value": ["ajuste_direto", "concurso_limitado_previa_qualificacao", "concurso_publico", "dialogo_concorrencial", "procedimento_negociacao"]}]; params {"selects_by": "data_inicio_procedimento", "regimes": [{"from": "2026-10-01", "to": "2026-10-01", "law_version": "lei:ccp@2026-10-01", "package": "pacote:ccp@2026-10-01"}]}
- leitor:b: passagens dl-177-2026:art11, dl-177-2026:art7.2; condições []; params {"selects_by": "data_inicio_procedimento", "regimes": [{"from": "0001-01-01", "to": "2026-09-30", "law_version": "lei:ccp@2026-09-30", "package": "pacote:ccp@2026-09-30"}, {"from": "2026-10-01", "to": null, "law_version": "lei:ccp@2026-10-01", "package": "pacote:ccp@2026-10-01"}]}

## regra:ccp:prazo-minimo-concurso-sem-joue-bens-servicos@v1

- leitor:a: passagens ccp:art135; condições [{"field": "data_inicio_procedimento", "op": "not_in", "value": "data"}, {"field": "preco_base", "op": "not_in", "value": "número"}, {"field": "publicado_joue", "op": "in", "value": "true"}, {"field": "territorio", "op": "in", "value": "PT"}, {"field": "tipo_entidade", "op": "in", "value": "outra"}, {"field": "tipo_procedimento", "op": "in", "value": "concurso_publico"}]; params {"minimum_days": 6, "deadline_field": "prazo_propostas_dias", "counted_from": "data_envio_anuncio"}
- leitor:b: passagens ccp:art135.1; condições [{"field": "publicado_joue", "op": "eq", "value": false}, {"field": "tipo_contrato", "op": "ne", "value": "obras"}, {"field": "tipo_procedimento", "op": "eq", "value": "concurso_publico"}]; params {"minimum_days": 6, "deadline_field": "prazo_propostas_dias", "counted_from": "data_envio_anuncio"}

## regra:ccp:prazo-minimo-concurso-sem-joue-obras@v1

- leitor:a: passagens ccp:art135; condições [{"field": "data_inicio_procedimento", "op": "not_in", "value": "uma data no formato ISO"}, {"field": "preco_base", "op": "not_in", "value": "número em euros"}, {"field": "territorio", "op": "in", "value": "PT"}, {"field": "tipo_entidade", "op": "in", "value": "outra"}, {"field": "tipo_procedimento", "op": "in", "value": "concurso_publico"}]; params {"minimum_days": 14, "deadline_field": "prazo_propostas_dias", "counted_from": "data_envio_anuncio"}
- leitor:b: passagens ccp:art135.1; condições [{"field": "publicado_joue", "op": "eq", "value": false}, {"field": "tipo_contrato", "op": "eq", "value": "obras"}, {"field": "tipo_procedimento", "op": "eq", "value": "concurso_publico"}]; params {"minimum_days": 14, "deadline_field": "prazo_propostas_dias", "counted_from": "data_envio_anuncio"}

## regra:ccp:prazo-minimo-concurso-joue@v1

- leitor:a: passagens ccp:art136.1; condições [{"field": "data_inicio_procedimento", "op": "not_in", "value": "não especificado"}, {"field": "territorio", "op": "eq", "value": "PT"}]; params {"minimum_days": 30, "deadline_field": "prazo_propostas_dias", "counted_from": "data_envio_anuncio"}
- leitor:b: passagens ccp:art136.1; condições [{"field": "publicado_joue", "op": "eq", "value": true}, {"field": "tipo_procedimento", "op": "eq", "value": "concurso_publico"}]; params {"minimum_days": 30, "deadline_field": "prazo_propostas_dias", "counted_from": "data_envio_anuncio"}

