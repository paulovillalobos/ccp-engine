# FÁBRICA DE REGRAS — ronda 6 (DECISIONS D66)

Gerado por tools/rule_factory.py (ccp-rule-factory-0.7) com o protocolo de leitura v3 (tools/read_rules_v3.py, ccp-read-rules-v3-0.2). D66: o protocolo de leitura v3 — a passagem-alvo no seu lugar na lei, as regras de leitura no prompt, cada condição e cada parâmetro com as palavras exatas e a passagem de onde vêm. Alvos: os 12 da ronda 5. Propõe leitor:a13 (AMALIA + adaptador v11), leitor:b revê às cegas.

Um programa confirma cada palavra citada; a leitura que falha não fica registada. Replicam o mesmo conteúdo canónico ou o mesmo motivo de «não tipável»; um «não tipável» assente invalida as regras propostas do alvo.

| regra | passagem | estado | replica | verificador: leitor A | verificador: leitor B |
|---|---|---|---|---|---|
| regra:ccp:auto-limiar-art127-c-1-a@v1 | ccp:art127-c.1.a | sem leitura válida de leitor:a13 | — | regra 1, preco_base ge 2000000: num limiar o valor é o parâmetro, não uma condição (L10) | ok |
| regra:ccp:auto-limiar-art17-b-4@v1 | ccp:art17-b.4 | sem leitura válida de leitor:a13 | — | regra 1, tipo_contrato eq bens: as fontes nomeiam também ['servicos'] (fonte mais curta, ou a condição está incompleta) | ok |
| regra:ccp:auto-limiar-art21-1-b@v1 | ccp:art21.1.b | sem leitura válida de leitor:a13 | — | regra 1, valor_estimado lt 130000: num limiar o valor é o parâmetro, não uma condição (L10) | ok |
| regra:ccp:auto-limiar-art21-1-c@v1 | ccp:art21.1.c | sem leitura válida de leitor:a13 | — | regra 1, tipo_contrato eq ajuste_direto: valores fora do vocabulário ['ajuste_direto'] | ok |
| regra:ccp:auto-limiar-art31-4@v1 | ccp:art31.4 | sem leitura válida de leitor:a13 | — | regra 1, valor_estimado lt 1000000: num limiar o valor é o parâmetro, não uma condição (L10) | ok |
| regra:ccp:auto-limiar-art54-a-1-b-ii@v1 | ccp:art54-a.1.b.ii | sem leitura válida de leitor:a13 | — | regra 1, tipo_contrato in ['concessao_obras', 'concessao_servicos', 'obras', 'servicos']: as fontes não nomeiam ['servic | ok |
| regra:ccp:auto-limiar-art88-2-a@v1 | ccp:art88.2.a | sem leitura válida de leitor:a13 | — | regra 1, preco_contratual lt 1000000: num limiar o valor é o parâmetro, não uma condição (L10) | ok |
| regra:ccp:auto-prazo-minimo-art174-3@v1 | ccp:art174.3 | sem leitura válida de leitor:a13 | — | regra 1, publicado_joue eq True: «Quando o anúncio do concurso limitado por prévia qualificaçã» não está em ccp:art174.3 | ok |
| regra:ccp:auto-prazo-minimo-art192-2@v1 | ccp:art192.2 | sem leitura válida de leitor:a13 | — | regra 1, tipo_procedimento eq concurso_limitado_previa_qualificacao: «Concurso limitado por prévia qualificação» não est | ok |
| regra:ccp:auto-prazo-minimo-art198-1@v1 | ccp:art198.1 | sem leitura válida de leitor:a13 | — | regra 1, tipo_procedimento eq procedimento_negociacao: fonte em ccp:art198.2, que é vizinho (L1) | ok |
| regra:ccp:auto-prazo-minimo-art198-2@v1 | ccp:art198.2 | sem leitura válida de leitor:a13 | — | regra 1, data_inicio_procedimento eq ajuste_direto_simplificado: as fontes não fixam uma data (L13) | ok |
| regra:ccp:auto-prazo-minimo-art241-b-3-b@v1 | ccp:art241-b.3.b | sem leitura válida de leitor:a13 | — | regra 1, tipo_procedimento eq simplificado: «sistema de aquisição dinâmico» não está em ccp:art241-b | ok |

## regra:ccp:auto-limiar-art127-c-1-a@v1

- leitor:a13: {"tipo": "limiar", "condicoes": [{"field": "preco_base", "op": "ge", "value": 2000000}, {"field": "tipo_contrato", "op": "in", "value": ["concessao_obras", "concessao_servicos", "obras"]}], "params": {"threshold": {"field": "preco_base", "comparator": "ge", "value": 2000000, "currency": "EUR"}}}
- leitor:b: não tipável (nao_e_limiar): O valor exclui entidades convidadas em função do preço contratual acumulado de vários contratos, não fixa um limite até ao qual o procedimento pode ser escolhido.
- verificador (A): regra 1, preco_base ge 2000000: num limiar o valor é o parâmetro, não uma condição (L10); regra 1, preco_base ge 2000000: as fontes não dizem preco_base ge 2000000 (L10); regra 1: um limiar tem sempre o procedimento que permite abaixo do valor; sem ele, L12 (nao_e_limiar); regra 1: field preco_base e as fontes nomeiam nada (L10)

## regra:ccp:auto-limiar-art17-b-4@v1

- leitor:a13: {"tipo": "limiar", "condicoes": [{"field": "tipo_contrato", "op": "eq", "value": "bens"}], "params": {"threshold": {"field": "valor_estimado", "comparator": "lt", "value": 80000, "currency": "EUR"}}}
- leitor:b: não tipável (nao_e_limiar): A passagem fixa uma dispensa da agregação dos valores estimados, não um limite até ao qual um procedimento pode ser escolhido.
- verificador (A): regra 1, tipo_contrato eq bens: as fontes nomeiam também ['servicos'] (fonte mais curta, ou a condição está incompleta); regra 1: um limiar tem sempre o procedimento que permite abaixo do valor; sem ele, L12 (nao_e_limiar); regra 1: field valor_estimado e as fontes nomeiam nada (L10)

## regra:ccp:auto-limiar-art21-1-b@v1

- leitor:a13: {"tipo": "limiar", "condicoes": [{"field": "tipo_procedimento", "op": "eq", "value": "consulta_previa"}, {"field": "valor_estimado", "op": "lt", "value": 130000}], "params": {"threshold": {"field": "valor_estimado", "comparator": "lt", "value": 130000, "currency": "EUR"}}}
- leitor:b: {"tipo": "limiar", "condicoes": [{"field": "tipo_contrato", "op": "not_in", "value": ["bens", "concessao_obras", "concessao_servicos", "obras", "servicos", "sociedade"]}, {"field": "tipo_procedimento", "op": "eq", "value": "consulta_previa"}], "params": {"threshold": {"field": "valor_estimado", "comparator": "lt", "value": 130000, "currency": "EUR"}}}
- verificador (A): regra 1, valor_estimado lt 130000: num limiar o valor é o parâmetro, não uma condição (L10); regra 1, valor_estimado lt 130000: as fontes não dizem valor_estimado lt 130000 (L10); regra 1, value: «.130.000» não está em ccp:art21.1.b; regra 1: value 130000 não está nas fontes (L10)

## regra:ccp:auto-limiar-art21-1-c@v1

- leitor:a13: {"tipo": "limiar", "condicoes": [{"field": "tipo_contrato", "op": "eq", "value": "ajuste_direto"}], "params": {"threshold": {"field": "preco_base", "comparator": "lt", "value": 75000, "currency": "EUR"}}}
- leitor:b: {"tipo": "limiar", "condicoes": [{"field": "tipo_contrato", "op": "not_in", "value": ["bens", "concessao_obras", "concessao_servicos", "obras", "servicos", "sociedade"]}, {"field": "tipo_procedimento", "op": "eq", "value": "ajuste_direto"}], "params": {"threshold": {"field": "valor_estimado", "comparator": "lt", "value": 75000, "currency": "EUR"}}}
- verificador (A): regra 1, tipo_contrato eq ajuste_direto: valores fora do vocabulário ['ajuste_direto']; regra 1, tipo_contrato eq ajuste_direto: as fontes não nomeiam ['ajuste_direto']; regra 1: um limiar tem sempre o procedimento que permite abaixo do valor; sem ele, L12 (nao_e_limiar); regra 1: field preco_base e as fontes nomeiam nada (L10); regra 1: value 75000 não está nas fontes (L10)

## regra:ccp:auto-limiar-art31-4@v1

- leitor:a13: {"tipo": "limiar", "condicoes": [{"field": "duracao_contrato_meses", "op": "lt", "value": 12}, {"field": "tipo_contrato", "op": "eq", "value": "concessao_obras"}, {"field": "valor_estimado", "op": "lt", "value": 1000000}], "params": {"threshold": {"field": "valor_estimado", "comparator": "lt", "value": 1000000, "currency": "EUR"}}}
- leitor:b: {"tipo": "limiar", "condicoes": [{"field": "duracao_contrato_meses", "op": "lt", "value": 12}, {"field": "tipo_contrato", "op": "in", "value": ["concessao_obras", "concessao_servicos"]}, {"field": "tipo_procedimento", "op": "in", "value": ["ajuste_direto", "consulta_previa"]}], "params": {"threshold": {"field": "valor_estimado", "comparator": "lt", "value": 1000000, "currency": "EUR"}}}
- verificador (A): regra 1, valor_estimado lt 1000000: num limiar o valor é o parâmetro, não uma condição (L10); regra 1, valor_estimado lt 1000000: as fontes não dizem valor_estimado lt 1000000 (L10); regra 1: um limiar tem sempre o procedimento que permite abaixo do valor; sem ele, L12 (nao_e_limiar)

## regra:ccp:auto-limiar-art54-a-1-b-ii@v1

- leitor:a13: {"tipo": "limiar", "condicoes": [{"field": "tipo_contrato", "op": "in", "value": ["concessao_obras", "concessao_servicos", "obras", "servicos"]}], "params": {"threshold": {"field": "preco_base", "comparator": "lt", "value": 500000, "currency": "EUR"}}}
- leitor:b: não tipável (nao_e_limiar): O valor delimita a reserva de participação, não o limite até ao qual um procedimento pode ser escolhido.
- verificador (A): regra 1, tipo_contrato in ['concessao_obras', 'concessao_servicos', 'obras', 'servicos']: as fontes não nomeiam ['servicos']; regra 1: um limiar tem sempre o procedimento que permite abaixo do valor; sem ele, L12 (nao_e_limiar); regra 1, field: «valor estimado do contrato» não está em ccp:art54-a.1.b.ii; regra 1: field preco_base e as fontes nomeiam nada (L10)

## regra:ccp:auto-limiar-art88-2-a@v1

- leitor:a13: {"tipo": "limiar", "condicoes": [{"field": "preco_contratual", "op": "lt", "value": 1000000}], "params": {"threshold": {"field": "preco_contratual", "comparator": "lt", "value": 1000000, "currency": "EUR"}}}
- leitor:b: não tipável (nao_e_limiar): O valor permite dispensar a prestação de caução; não fixa um limite até ao qual um procedimento pode ser escolhido.
- verificador (A): regra 1, preco_contratual lt 1000000: num limiar o valor é o parâmetro, não uma condição (L10); regra 1: um limiar tem sempre o procedimento que permite abaixo do valor; sem ele, L12 (nao_e_limiar); regra 1, field: «preco_contratual» não está em ccp:art88.2.a; regra 1: field preco_contratual e as fontes nomeiam nada (L10); regra 1, comparator: «lt» não está em ccp:art88.2.a; regra 1: comparator lt e as fontes dizem nada (L8)

## regra:ccp:auto-prazo-minimo-art174-3@v1

- leitor:a13: {"tipo": "prazo_minimo", "condicoes": [{"field": "publicado_joue", "op": "eq", "value": true}, {"field": "tipo_procedimento", "op": "eq", "value": "concurso_limitado_previa_qualificacao"}, {"field": "urgencia_fundamentada", "op": "eq", "value": false}], "params": {"minimum_days": 15, "deadline_field": "prazo_candidaturas_dias", "counted_from": "data_envio_anuncio", "usual_days": null}}
- leitor:b: não tipável (texto_em_falta): Faltam as alíneas do n.º 1 do artigo 7.º que identificam as entidades adjudicantes às quais a regra se aplica.
- verificador (A): regra 1, publicado_joue eq True: «Quando o anúncio do concurso limitado por prévia qualificaçã» não está em ccp:art174.3; regra 1, publicado_joue eq True: as fontes não afirmam o facto (L7); regra 1, urgencia_fundamentada eq False: as fontes não negam o facto (L7); regra 1, tipo_procedimento eq concurso_limitado_previa_qualificacao: «Concurso limitado por prévia qualificação» não está em ccp:art174.3; regra 1, tipo_procedimento eq concurso_limitado_previa_qualificacao: as fontes não nomeiam ['concurso_limitado_previa_qualificacao']

## regra:ccp:auto-prazo-minimo-art192-2@v1

- leitor:a13: {"tipo": "prazo_minimo", "condicoes": [{"field": "data_inicio_procedimento", "op": "eq", "value": "ajuste_direto_simplificado"}, {"field": "tipo_procedimento", "op": "eq", "value": "concurso_limitado_previa_qualificacao"}], "params": {"minimum_days": 10, "deadline_field": "prazo_propostas_dias", "counted_from": "data_envio_convite", "usual_days": null}}
- leitor:b: não tipável (texto_em_falta): Falta o n.º 1 do artigo 7.º, necessário para delimitar as entidades adjudicantes abrangidas pela condição herdada do número anterior.
- verificador (A): regra 1, tipo_procedimento eq concurso_limitado_previa_qualificacao: «Concurso limitado por prévia qualificação» não está em ccp:art192; regra 1, tipo_procedimento eq concurso_limitado_previa_qualificacao: as fontes não nomeiam ['concurso_limitado_previa_qualificacao']; regra 1, data_inicio_procedimento eq ajuste_direto_simplificado: «data_envio_convite» não está em ccp:art192.2; regra 1, data_inicio_procedimento eq ajuste_direto_simplificado: as fontes não fixam uma data (L13); regra 1, deadline_field: «apresentação das propostas» não está em ccp:art192.2; regra 1: deadline_field prazo_propostas_dias e as fontes dizem nada (L9)

## regra:ccp:auto-prazo-minimo-art198-1@v1

- leitor:a13: {"tipo": "prazo_minimo", "condicoes": [{"field": "anuncio_pre_informacao", "op": "eq", "value": true}, {"field": "data_inicio_procedimento", "op": "eq", "value": "ajuste_direto_simplificado"}, {"field": "tipo_procedimento", "op": "eq", "value": "procedimento_negociacao"}], "params": {"minimum_days": 25, "deadline_field": "prazo_candidaturas_dias", "counted_from": "data_envio_convite", "usual_days": null}}
- leitor:b: {"tipo": "prazo_minimo", "condicoes": [{"field": "publicado_joue", "op": "eq", "value": true}, {"field": "tipo_procedimento", "op": "eq", "value": "procedimento_negociacao"}], "params": {"minimum_days": 30, "deadline_field": "prazo_candidaturas_dias", "counted_from": "data_envio_anuncio", "usual_days": null}}
- verificador (A): regra 1, tipo_procedimento eq procedimento_negociacao: fonte em ccp:art198.2, que é vizinho (L1); regra 1, tipo_procedimento eq procedimento_negociacao: «Procedimento de negociação» não está em ccp:art198.2; regra 1, tipo_procedimento eq procedimento_negociacao: as fontes não nomeiam ['procedimento_negociacao']; regra 1, anuncio_pre_informacao eq True: «publicado o anúncio periódico indicativo» não está em ccp:art198.1; regra 1, anuncio_pre_informacao eq True: as fontes não afirmam o facto (L7); regra 1, data_inicio_procedimento eq ajuste_direto_simplificado: fonte em ccp:art198.2, que é vizinho (L1)

## regra:ccp:auto-prazo-minimo-art198-2@v1

- leitor:a13: {"tipo": "prazo_minimo", "condicoes": [{"field": "anuncio_pre_informacao", "op": "eq", "value": true}, {"field": "data_inicio_procedimento", "op": "eq", "value": "ajuste_direto_simplificado"}, {"field": "tipo_procedimento", "op": "eq", "value": "procedimento_negociacao"}], "params": {"minimum_days": 25, "deadline_field": "prazo_candidaturas_dias", "counted_from": "data_envio_convite", "usual_days": null}}
- leitor:b: não tipável (texto_em_falta): Faltam as alíneas do n.º 3 do artigo 167.º que especificam as indicações exigidas no anúncio periódico indicativo.
- verificador (A): regra 1, data_inicio_procedimento eq ajuste_direto_simplificado: as fontes não fixam uma data (L13)

## regra:ccp:auto-prazo-minimo-art241-b-3-b@v1

- leitor:a13: {"tipo": "prazo_minimo", "condicoes": [{"field": "preco_base", "op": "eq", "value": "1000-20-00"}, {"field": "tipo_procedimento", "op": "eq", "value": "simplificado"}], "params": {"minimum_days": 10, "deadline_field": "prazo_propostas_dias", "counted_from": "nao_indicado", "usual_days": null}}
- leitor:b: não tipável (sem_vocabulario): O vocabulário não permite limitar a regra aos sistemas de aquisição dinâmicos.
- verificador (A): regra 1, tipo_procedimento eq simplificado: «sistema de aquisição dinâmico» não está em ccp:art241-b; regra 1, tipo_procedimento eq simplificado: valores fora do vocabulário ['simplificado']; regra 1, tipo_procedimento eq simplificado: as fontes não nomeiam ['simplificado']; regra 1, preco_base eq 1000-20-00: as fontes não dizem preco_base eq 1000-20-00 (L10)

