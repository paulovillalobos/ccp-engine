# DESACORDOS — leituras em que leitor:b, cego, não coincide com leitor:a

Gerado por tools/read_rules.py a partir das respostas guardadas. Para a pessoa ver: decide produto (que regras entram, que campos o motor lê), nunca o conteúdo de uma leitura da lei; uma leitura só fica settled quando leitor:b, cego e de outra família, coincide (D37).

## regra:dl-177-2026:seletor-regime@v1 (seletor_regime)

- leitor:a: passagens dl-177-2026:art7.2, dl-177-2026:art7.3; condições [{"field": "territorio", "op": "in", "value": ["PT"]}, {"field": "tipo_procedimento", "op": "in", "value": ["ajuste_direto", "concurso_limitado_previa_qualificacao", "concurso_publico", "dialogo_concorrencial", "procedimento_negociacao"]}]; params {"selects_by": "data_inicio_procedimento", "regimes": [{"from": "2026-10-01", "to": "9999-12-31", "law_version": "lei:ccp@2026-10-01", "package": "pacote:ccp@2026-10-01"}]}
- leitor:b: passagens dl-177-2026:art11, dl-177-2026:art7.2; condições []; params {"selects_by": "data_inicio_procedimento", "regimes": [{"from": "0001-01-01", "to": "2026-09-30", "law_version": "lei:ccp@2026-09-30", "package": "pacote:ccp@2026-09-30"}, {"from": "2026-10-01", "to": null, "law_version": "lei:ccp@2026-10-01", "package": "pacote:ccp@2026-10-01"}]}
- difere em: passages, conditions, params

## regra:ccp:limiar-ajuste-direto-bens-servicos@v1 (limiar)

- leitor:a: passagens ccp:art20.1.d; condições [{"field": "tipo_contrato", "op": "in", "value": ["bens", "concessao_obras", "concessao_servicos", "obras", "servicos", "servicos_sociais"]}, {"field": "tipo_procedimento", "op": "in", "value": "ajuste_direto"}]; params {"threshold": {"field": "preco_base", "comparator": "lt", "value": 20000.0, "currency": "EUR"}}
- leitor:b: passagens ccp:art20.1, ccp:art20.1.d; condições [{"field": "tipo_contrato", "op": "in", "value": ["bens", "servicos"]}, {"field": "tipo_procedimento", "op": "eq", "value": "ajuste_direto"}]; params {"threshold": {"field": "preco_base", "comparator": "lt", "value": 20000, "currency": "EUR"}}
- difere em: passages, conditions

## regra:ccp:limiar-ajuste-direto-bens-servicos@v2 (limiar)

- leitor:a: passagens ccp:art20.1, ccp:art20.1.d; condições [{"field": "tipo_contrato", "op": "in", "value": "obras"}, {"field": "tipo_procedimento", "op": "in", "value": "ajuste_direto"}]; params {"threshold": {"field": "preco_base", "comparator": "lt", "value": 75000.0, "currency": "EUR"}}
- leitor:b: passagens ccp:art20.1, ccp:art20.1.d; condições [{"field": "tipo_contrato", "op": "in", "value": ["bens", "servicos"]}, {"field": "tipo_procedimento", "op": "eq", "value": "ajuste_direto"}]; params {"threshold": {"field": "preco_base", "comparator": "lt", "value": 75000, "currency": "EUR"}}
- difere em: conditions

## regra:ccp:limiar-ajuste-direto-obras@v1 (limiar)

- leitor:a: passagens ccp:art19.a, ccp:art19.b, ccp:art19.c, ccp:art19.d; condições [{"field": "tipo_contrato", "op": "eq", "value": "obras"}, {"field": "tipo_procedimento", "op": "eq", "value": "ajuste_direto"}]; params {"threshold": {"field": "preco_base", "comparator": "lt", "value": 30000.0, "currency": "EUR"}}
- leitor:b: passagens ccp:art19.d; condições [{"field": "tipo_contrato", "op": "eq", "value": "obras"}, {"field": "tipo_procedimento", "op": "eq", "value": "ajuste_direto"}]; params {"threshold": {"field": "preco_base", "comparator": "lt", "value": 30000, "currency": "EUR"}}
- difere em: passages

## regra:ccp:limiar-consulta-previa-bens-servicos@v1 (limiar)

- leitor:a: passagens ccp:art20.1.c; condições [{"field": "tipo_contrato", "op": "in", "value": ["bens", "concessao_obras", "concessao_servicos", "obras", "servicos", "servicos_sociais"]}, {"field": "tipo_procedimento", "op": "in", "value": "consulta_previa"}]; params {"threshold": {"field": "preco_base", "comparator": "lt", "value": 75000.0, "currency": "EUR"}}
- leitor:b: passagens ccp:art20.1, ccp:art20.1.c; condições [{"field": "tipo_contrato", "op": "in", "value": ["bens", "servicos"]}, {"field": "tipo_procedimento", "op": "eq", "value": "consulta_previa"}]; params {"threshold": {"field": "preco_base", "comparator": "lt", "value": 75000, "currency": "EUR"}}
- difere em: passages, conditions

## regra:ccp:limiar-consulta-previa-bens-servicos@v2 (limiar)

- leitor:a: passagens ccp:art20.1.c; condições [{"field": "tipo_contrato", "op": "in", "value": "bens"}, {"field": "tipo_contrato", "op": "in", "value": "concessao_obras"}, {"field": "tipo_contrato", "op": "in", "value": "concessao_servicos"}, {"field": "tipo_contrato", "op": "in", "value": "obras"}, {"field": "tipo_contrato", "op": "in", "value": "servicos"}, {"field": "tipo_contrato", "op": "in", "value": "servicos_sociais"}, {"field": "tipo_procedimento", "op": "in", "value": "consulta_previa"}]; params {"threshold": {"field": "preco_base", "comparator": "lt", "value": 130000, "currency": "EUR"}}
- leitor:b: passagens ccp:art20.1.c; condições [{"field": "tipo_contrato", "op": "in", "value": ["bens", "servicos"]}, {"field": "tipo_procedimento", "op": "eq", "value": "consulta_previa"}]; params {"threshold": {"field": "preco_base", "comparator": "lt", "value": 130000, "currency": "EUR"}}
- difere em: conditions

## regra:ccp:limiar-concurso-sem-joue-bens-servicos-estado@v1 (limiar)

- leitor:a: passagens ccp:art20.1.b, ccp:art474.3.b, eu-2025-2152:art1.1.b; condições [{"field": "preco_base", "op": "lt", "value": 139000}, {"field": "tipo_entidade", "op": "eq", "value": "estado"}, {"field": "tipo_procedimento", "op": "eq", "value": "concurso_publico"}]; params {"threshold": {"field": "preco_base", "comparator": "lt", "value": 139000, "currency": "EUR"}}
- leitor:b: passagens ccp:art20.1.b, ccp:art474.3.b, eu-2025-2152:art1.1.b; condições [{"field": "publicado_joue", "op": "eq", "value": false}, {"field": "tipo_contrato", "op": "in", "value": ["bens", "servicos"]}, {"field": "tipo_entidade", "op": "eq", "value": "estado"}, {"field": "tipo_procedimento", "op": "in", "value": ["concurso_limitado_previa_qualificacao", "concurso_publico"]}]; params {"threshold": {"field": "preco_base", "comparator": "lt", "value": 140000, "currency": "EUR"}}
- difere em: conditions, params

## regra:ccp:limiar-concurso-sem-joue-obras@v1 (limiar)

- leitor:a: passagens ccp:art19.b; condições [{"field": "data_inicio_procedimento", "op": "eq", "value": "2026-10-01"}, {"field": "preco_base", "op": "lt", "value": 5404000}, {"field": "territorio", "op": "eq", "value": "PT"}, {"field": "tipo_entidade", "op": "eq", "value": "estado"}, {"field": "tipo_procedimento", "op": "eq", "value": "concurso_limitado_previa_qualificacao"}]; params {"threshold": {"field": "preco_base", "comparator": "lt", "value": 5404000, "currency": "EUR"}}
- leitor:b: passagens ccp:art19.b, ccp:art474.3.a, eu-2025-2152:art1.1.a; condições [{"field": "publicado_joue", "op": "eq", "value": false}, {"field": "tipo_contrato", "op": "eq", "value": "obras"}, {"field": "tipo_procedimento", "op": "in", "value": ["concurso_limitado_previa_qualificacao", "concurso_publico"]}]; params {"threshold": {"field": "preco_base", "comparator": "lt", "value": 5404000, "currency": "EUR"}}
- difere em: passages, conditions

## regra:dlr-34-2008-m:coeficiente-madeira@v1 (jurisdicao)

- leitor:a: passagens dlr-34-2008-m:art4, dlr-34-2008-m:art4.1, dlr-34-2008-m:art4.2, dlr-34-2008-m:art4.3, dlr-34-2008-m:art4.4; condições [{"field": "territorio", "op": "in", "value": "PT-MA"}, {"field": "tipo_procedimento", "op": "in", "value": "concurso_publico"}]; params {"territory": "PT-MA", "predicate": [{"field": "tipo_procedimento", "op": "in", "value": "concurso_publico"}], "effect": {"multiply_thresholds_by": 1.45, "replace_norma": "norma:dlr-34-2008-m"}}
- leitor:b: passagens dlr-34-2008-m:art4.1, dlr-34-2008-m:art4.2, dlr-34-2008-m:art4.3; condições [{"field": "territorio", "op": "eq", "value": "PT-MA"}]; params {"territory": "PT-MA", "predicate": [{"field": "territorio", "op": "eq", "value": "PT-MA"}], "effect": {"multiply_thresholds_by": 1.45}}
- difere em: passages, conditions, params

## regra:dlr-27-2015-a:regime-acores@v1 (jurisdicao)

- leitor:a: passagens dlr-27-2015-a:art19, dlr-27-2015-a:art19.a, dlr-27-2015-a:art20.a; condições [{"field": "territorio", "op": "in", "value": "PT-MA"}, {"field": "tipo_entidade", "op": "in", "value": "outra"}]; params {"territory": "PT-MA", "predicate": [{"field": "tipo_entidade", "op": "in", "value": "outra"}], "effect": {"multiply_thresholds_by": 1, "replace_norma": "norma:dlr-27-2015-a"}}
- leitor:b: passagens dlr-27-2015-a:art1, dlr-27-2015-a:art16, dlr-27-2015-a:art19, dlr-27-2015-a:art20; condições [{"field": "territorio", "op": "eq", "value": "PT-AC"}]; params {"territory": "PT-AC", "predicate": [{"field": "tipo_contrato", "op": "in", "value": ["obras", "bens", "servicos"]}], "effect": {"replace_norma": "norma:dlr-27-2015-a"}}
- difere em: passages, conditions, params

## regra:ccp:prazo-minimo-concurso-sem-joue-bens-servicos@v1 (prazo_minimo)

- leitor:a: passagens ccp:art135; condições [{"field": "publicado_joue", "op": "in", "value": true}, {"field": "territorio", "op": "in", "value": "PT"}, {"field": "tipo_contrato", "op": "not_in", "value": "concessao_obras"}, {"field": "tipo_procedimento", "op": "in", "value": "concurso_publico"}]; params {"minimum_days": 6, "deadline_field": "prazo_propostas_dias", "counted_from": "data_envio_anuncio"}
- leitor:b: passagens ccp:art135.1; condições [{"field": "publicado_joue", "op": "eq", "value": false}, {"field": "tipo_contrato", "op": "ne", "value": "obras"}, {"field": "tipo_procedimento", "op": "eq", "value": "concurso_publico"}]; params {"minimum_days": 6, "deadline_field": "prazo_propostas_dias", "counted_from": "data_envio_anuncio"}
- difere em: passages, conditions

## regra:ccp:prazo-minimo-concurso-sem-joue-obras@v1 (prazo_minimo)

- leitor:a: passagens ccp:art135; condições [{"field": "data_inicio_procedimento", "op": "not_in", "value": []}, {"field": "preco_base", "op": "not_in", "value": []}, {"field": "territorio", "op": "in", "value": "PT"}, {"field": "tipo_entidade", "op": "in", "value": "outra"}, {"field": "tipo_procedimento", "op": "in", "value": "concurso_publico"}]; params {"minimum_days": 14, "deadline_field": "prazo_propostas_dias", "counted_from": "data_envio_anuncio"}
- leitor:b: passagens ccp:art135.1; condições [{"field": "publicado_joue", "op": "eq", "value": false}, {"field": "tipo_contrato", "op": "eq", "value": "obras"}, {"field": "tipo_procedimento", "op": "eq", "value": "concurso_publico"}]; params {"minimum_days": 14, "deadline_field": "prazo_propostas_dias", "counted_from": "data_envio_anuncio"}
- difere em: passages, conditions

## regra:ccp:prazo-minimo-concurso-joue@v1 (prazo_minimo)

- leitor:a: passagens ccp:art136; condições [{"field": "data_inicio_procedimento", "op": "in", "value": "AAAA-MM-DD"}, {"field": "publicado_joue", "op": "eq", "value": true}]; params {"minimum_days": 30, "deadline_field": "prazo_propostas_dias", "counted_from": "data_envio_anuncio"}
- leitor:b: passagens ccp:art136.1; condições [{"field": "publicado_joue", "op": "eq", "value": true}, {"field": "tipo_procedimento", "op": "eq", "value": "concurso_publico"}]; params {"minimum_days": 30, "deadline_field": "prazo_propostas_dias", "counted_from": "data_envio_anuncio"}
- difere em: passages, conditions

## regra:ccp:procedimentos-admissiveis@v1 (procedimento_admissivel)

- leitor:a: passagens ccp:art16, ccp:art16.1; condições [{"field": "tipo_procedimento", "op": "in", "value": ["ajuste_direto", "concurso_limitado_previa_qualificacao", "concurso_publico", "consulta_previa", "dialogo_concorrencial", "parceria_inovacao", "procedimento_negociacao"]}]; params {"procedures": ["ajuste_direto", "concurso_limitado_previa_qualificacao", "concurso_publico", "consulta_previa", "dialogo_concorrencial", "parceria_inovacao", "procedimento_negociacao"]}
- leitor:b: passagens ccp:art16.1; condições []; params {"procedures": ["ajuste_direto", "concurso_limitado_previa_qualificacao", "concurso_publico", "consulta_previa", "dialogo_concorrencial", "parceria_inovacao", "procedimento_negociacao"]}
- difere em: passages, conditions

## regra:ccp:procedimentos-admissiveis@v2 (procedimento_admissivel)

- leitor:a: passagens ccp:art16, ccp:art16.1, ccp:art16.2; condições [{"field": "tipo_procedimento", "op": "in", "value": ["ajuste_direto", "concurso_limitado_previa_qualificacao", "concurso_publico", "consulta_previa", "dialogo_concorrencial", "parceria_inovacao", "procedimento_negociacao"]}]; params {"procedures": ["ajuste_direto", "concurso_limitado_previa_qualificacao", "concurso_publico", "consulta_previa", "dialogo_concorrencial", "parceria_inovacao", "procedimento_negociacao"]}
- leitor:b: passagens ccp:art16.1; condições []; params {"procedures": ["ajuste_direto", "concurso_limitado_previa_qualificacao", "concurso_publico", "consulta_previa", "dialogo_concorrencial", "parceria_inovacao", "procedimento_negociacao"]}
- difere em: passages, conditions

