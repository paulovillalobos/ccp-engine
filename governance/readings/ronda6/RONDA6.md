# RONDA 6 — B3, as quatro regras que o motor precisa primeiro (DECISIONS D49)

Gerado por tools/read_rules.py. O prompt e o esquema da ronda 5, sem mudança; propõe leitor:a5 (AMALIA + adaptador v4, treinado também em condicoes_pergunta, D49), leitor:b revê às cegas. Só fica settled a leitura que leitor:b replica em forma canónica (D43).

| regra | estado | exato | direção |
|---|---|---|---|
| regra:dl-177-2026:seletor-regime@v1 | proposed | não | não |
| regra:ccp:prazo-minimo-concurso-sem-joue-bens-servicos@v1 | settled | sim | sim |
| regra:ccp:prazo-minimo-concurso-sem-joue-obras@v1 | settled | sim | sim |
| regra:ccp:prazo-minimo-concurso-joue@v1 | settled numa ronda anterior (não reaberta) | não | sim |

## regra:dl-177-2026:seletor-regime@v1

- leitor:a5: passagens dl-177-2026:art7.2; condições []; params {"selects_by": "data_inicio_procedimento", "regimes": [{"from": "2026-10-01", "to": null, "law_version": "lei:ccp@2026-10-01", "package": "pacote:ccp@2026-10-01"}]}
- leitor:b: passagens dl-177-2026:art11, dl-177-2026:art7.2; condições []; params {"selects_by": "data_inicio_procedimento", "regimes": [{"from": "0001-01-01", "to": "2026-09-30", "law_version": "lei:ccp@2026-09-30", "package": "pacote:ccp@2026-09-30"}, {"from": "2026-10-01", "to": null, "law_version": "lei:ccp@2026-10-01", "package": "pacote:ccp@2026-10-01"}]}

## regra:ccp:prazo-minimo-concurso-sem-joue-bens-servicos@v1

- leitor:a5: passagens ccp:art135.1; condições [{"field": "publicado_joue", "op": "eq", "value": false}, {"field": "tipo_contrato", "op": "ne", "value": "obras"}, {"field": "tipo_procedimento", "op": "eq", "value": "concurso_publico"}]; params {"minimum_days": 6, "deadline_field": "prazo_propostas_dias", "counted_from": "data_envio_anuncio"}
- leitor:b: passagens ccp:art135.1; condições [{"field": "publicado_joue", "op": "eq", "value": false}, {"field": "tipo_contrato", "op": "ne", "value": "obras"}, {"field": "tipo_procedimento", "op": "eq", "value": "concurso_publico"}]; params {"minimum_days": 6, "deadline_field": "prazo_propostas_dias", "counted_from": "data_envio_anuncio"}

## regra:ccp:prazo-minimo-concurso-sem-joue-obras@v1

- leitor:a5: passagens ccp:art135.1; condições [{"field": "publicado_joue", "op": "eq", "value": false}, {"field": "tipo_contrato", "op": "eq", "value": "obras"}, {"field": "tipo_procedimento", "op": "eq", "value": "concurso_publico"}]; params {"minimum_days": 14, "deadline_field": "prazo_propostas_dias", "counted_from": "data_envio_anuncio"}
- leitor:b: passagens ccp:art135.1; condições [{"field": "publicado_joue", "op": "eq", "value": false}, {"field": "tipo_contrato", "op": "eq", "value": "obras"}, {"field": "tipo_procedimento", "op": "eq", "value": "concurso_publico"}]; params {"minimum_days": 14, "deadline_field": "prazo_propostas_dias", "counted_from": "data_envio_anuncio"}

## regra:ccp:prazo-minimo-concurso-joue@v1

- leitor:a5: passagens ccp:art136.1; condições [{"field": "publicado_joue", "op": "eq", "value": true}]; params {"minimum_days": 30, "deadline_field": "prazo_propostas_dias", "counted_from": "data_envio_anuncio"}
- leitor:b: passagens ccp:art136.1; condições [{"field": "publicado_joue", "op": "eq", "value": true}, {"field": "tipo_procedimento", "op": "eq", "value": "concurso_publico"}]; params {"minimum_days": 30, "deadline_field": "prazo_propostas_dias", "counted_from": "data_envio_anuncio"}

