# RONDA 5 — B3, as quatro regras que o motor precisa primeiro (DECISIONS D47)

Gerado por tools/read_rules.py. O prompt e o esquema da ronda 4, sem mudança; propõe leitor:a4 (AMALIA + adaptador v3, treinado também em entrada_em_vigor e periodos_vigencia, D47), leitor:b revê às cegas. Só fica settled a leitura que leitor:b replica em forma canónica (D43).

| regra | estado | exato | direção |
|---|---|---|---|
| regra:dl-177-2026:seletor-regime@v1 | proposed | não | não |
| regra:ccp:prazo-minimo-concurso-sem-joue-bens-servicos@v1 | proposed | não | sim |
| regra:ccp:prazo-minimo-concurso-sem-joue-obras@v1 | proposed | não | sim |
| regra:ccp:prazo-minimo-concurso-joue@v1 | settled numa ronda anterior (não reaberta) | não | sim |

## regra:dl-177-2026:seletor-regime@v1

- leitor:a4: passagens dl-177-2026:art7.2; condições []; params {"selects_by": "data_inicio_procedimento", "regimes": [{"from": "2026-10-01", "to": "2026-10-01", "law_version": "lei:ccp@2026-10-01", "package": "pacote:ccp@2026-10-01"}]}
- leitor:b: passagens dl-177-2026:art10, dl-177-2026:art11, dl-177-2026:art7.2; condições []; params {"selects_by": "data_inicio_procedimento", "regimes": [{"from": "0001-01-01", "to": "2026-09-30", "law_version": "lei:ccp@2026-09-30", "package": "pacote:ccp@2026-09-30"}, {"from": "2026-10-01", "to": null, "law_version": "lei:ccp@2026-10-01", "package": "pacote:ccp@2026-10-01"}]}

## regra:ccp:prazo-minimo-concurso-sem-joue-bens-servicos@v1

- leitor:a4: passagens ccp:art135.1; condições [{"field": "tipo_contrato", "op": "not_in", "value": ["obras"]}]; params {"minimum_days": 6, "deadline_field": "prazo_propostas_dias", "counted_from": "data_envio_anuncio"}
- leitor:b: passagens ccp:art135.1; condições [{"field": "publicado_joue", "op": "eq", "value": false}, {"field": "tipo_contrato", "op": "ne", "value": "obras"}, {"field": "tipo_procedimento", "op": "eq", "value": "concurso_publico"}]; params {"minimum_days": 6, "deadline_field": "prazo_propostas_dias", "counted_from": "data_envio_anuncio"}

## regra:ccp:prazo-minimo-concurso-sem-joue-obras@v1

- leitor:a4: passagens ccp:art135.1; condições [{"field": "data_inicio_procedimento", "op": "ne", "value": "2026-10-01"}, {"field": "preco_base", "op": "ne", "value": 0}, {"field": "publicado_joue", "op": "ne", "value": false}, {"field": "territorio", "op": "in", "value": ["PT"]}, {"field": "tipo_contrato", "op": "in", "value": ["obras"]}, {"field": "tipo_entidade", "op": "ne", "value": "outra"}]; params {"minimum_days": 14, "deadline_field": "prazo_propostas_dias", "counted_from": "data_envio_anuncio"}
- leitor:b: passagens ccp:art135.1; condições [{"field": "publicado_joue", "op": "eq", "value": false}, {"field": "tipo_contrato", "op": "eq", "value": "obras"}, {"field": "tipo_procedimento", "op": "eq", "value": "concurso_publico"}]; params {"minimum_days": 14, "deadline_field": "prazo_propostas_dias", "counted_from": "data_envio_anuncio"}

## regra:ccp:prazo-minimo-concurso-joue@v1

- leitor:a4: passagens ccp:art136.1, ccp:art136.2, ccp:art136.3; condições []; params {"minimum_days": 30, "deadline_field": "prazo_propostas_dias", "counted_from": "data_envio_anuncio"}
- leitor:b: passagens ccp:art136.1; condições [{"field": "publicado_joue", "op": "eq", "value": true}, {"field": "tipo_procedimento", "op": "eq", "value": "concurso_publico"}]; params {"minimum_days": 30, "deadline_field": "prazo_propostas_dias", "counted_from": "data_envio_anuncio"}

