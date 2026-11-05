# FÁBRICA DE REGRAS — ronda 16 (DECISIONS D76)

Gerado por tools/rule_factory.py (ccp-rule-factory-0.8) com o protocolo de leitura v3 (tools/read_rules_v3.py, ccp-read-rules-v3-0.4). D76: v16 relê a ronda 11 (os mesmos prompts, protocolo 0.4; as respostas cegas do leitor:b vêm da ronda 11). O exame é o grupo reservado; um alvo já assente é lido e medido mas não volta a ser registado. Propõe leitor:a18 (AMALIA + adaptador v16), leitor:b revê às cegas.

Um programa confirma cada palavra citada; o «não tipável» com o mesmo motivo também assenta.

| grupo | alvos | leitor A válido | leitor B válido | assentes | regras | «não tipável» |
|---|---|---|---|---|---|---|
| reservado | 13 | 7 | 12 | 2 | 0 | 2 |
| texto_visto | 7 | 4 | 7 | 0 | 0 | 0 |
| todos | 20 | 11 | 19 | 2 | 0 | 2 |

| regra | passagem | estado | replica | verificador: leitor A | verificador: leitor B |
|---|---|---|---|---|---|
| regra:ccp:auto-limiar-art127-b@v1 | ccp:art127-b | sem leitura válida de leitor:a18 | — | regra 1, tipo_contrato in ['concessao_obras', 'concessao_servicos', 'obras', 'servicos_sociais']: as fontes não nomeiam  | ok |
| regra:ccp:auto-limiar-art129-a-1-a@v1 | ccp:art129-a.1.a | sem leitura válida de leitor:a18 | — | regra 1: field valor_estimado e as fontes nomeiam nada (L10) | ok |
| regra:ccp:auto-limiar-art129-a-1-b@v1 | ccp:art129-a.1.b | sem leitura válida de leitor:a18 | — | regra 1, tipo_procedimento eq ajuste_direto_simplificado: as fontes não nomeiam ['ajuste_direto_simplificado'] | ok |
| regra:ccp:auto-prazo-minimo-art143-1@v1 | ccp:art143.1 | proposed (não tipável: sem_vocabulario) | não | ok | ok |
| regra:ccp:auto-prazo-minimo-art147@v1 | ccp:art147 | proposed | não | ok | ok |
| regra:ccp:auto-prazo-minimo-art161-b-1-b@v1 | ccp:art161-b.1.b | proposed (não tipável: nao_e_prazo_minimo) | não | ok | ok |
| regra:ccp:auto-prazo-minimo-art161-b-4@v1 | ccp:art161-b.4 | proposed (não tipável: nao_e_prazo_minimo) | não | ok | ok |
| regra:ccp:auto-prazo-minimo-art185@v1 | ccp:art185 | proposed | — | ok | regra 1: deadline_field prazo_pronuncia_dias e as fontes dizem nada (L9) |
| regra:ccp:auto-prazo-minimo-art188-2@v1 | ccp:art188.2 | proposed (não tipável: nao_e_prazo_minimo) | não | ok | ok |
| regra:ccp:auto-prazo-minimo-art198-3@v1 | ccp:art198.3 | proposed | não | ok | ok |
| regra:ccp:auto-prazo-minimo-art273@v1 | ccp:art273 | proposed (não tipável: nao_e_prazo_minimo) | não | ok | ok |
| regra:ccp:auto-limiar-art474-2@v1 | ccp:art474.2 | sem leitura válida de leitor:a18 | — | regra 1: um limiar tem sempre o procedimento que permite abaixo do valor; sem ele, L12 (nao_e_limiar) | ok |
| regra:ccp:auto-limiar-art474-3-a@v1 | ccp:art474.3.a | sem leitura válida de leitor:a18 | — | regra 1, tipo_entidade eq estado: as fontes não nomeiam ['estado'] | ok |
| regra:ccp:auto-limiar-art474-3-b@v1 | ccp:art474.3.b | sem leitura válida de leitor:a18 | — | regra 1, tipo_contrato in ['concessao_obras', 'concessao_servicos']: as fontes não nomeiam ['concessao_obras', 'concessa | ok |
| regra:ccp:auto-limiar-art474-3-c@v1 | ccp:art474.3.c | sem leitura válida de leitor:a18 | — | regra 1, tipo_contrato in ['concessao_obras', 'concessao_servicos']: as fontes não nomeiam ['concessao_obras', 'concessa | ok |
| regra:ccp:auto-limiar-art474-4-a@v1 | ccp:art474.4.a | sem leitura válida de leitor:a18 | — | regra 1, publicado_joue eq 0000-00-00: facto de dois lados usa eq true/false (L7) | ok |
| regra:ccp:auto-limiar-art474-4-b@v1 | ccp:art474.4.b | sem leitura válida de leitor:a18 | — | regra 1, setores_especiais eq False: as fontes não negam o facto (L7) | ok |
| regra:ccp:auto-prazo-minimo-art64-2@v1 | ccp:art64.2 | proposed (não tipável: nao_e_prazo_minimo) | não | ok | ok |
| regra:ccp:auto-prazo-minimo-art78-5@v1 | ccp:art78.5 | settled (não tipável: nao_e_prazo_minimo) | sim | ok | ok |
| regra:ccp:auto-prazo-minimo-art90-1@v1 | ccp:art90.1 | settled (não tipável: nao_e_prazo_minimo) | sim | ok | ok |

## regra:ccp:auto-limiar-art127-b@v1

- leitor:a18: {"tipo": "limiar", "condicoes": [{"field": "tipo_contrato", "op": "in", "value": ["concessao_obras", "concessao_servicos", "obras", "servicos_sociais"]}, {"field": "tipo_procedimento", "op": "eq", "value": "consulta_previa_especial"}], "params": {"threshold": {"field": "valor_estimado", "comparator": "lt", "value": 2000000, "currency": "EUR"}}}
- leitor:b: não tipável (sem_vocabulario): O vocabulário não permite representar a condição de o contrato ter um dos objetos previstos nas alíneas a) a f), necessária para delimitar a adoção da consulta prévia especial.
- verificador (A): regra 1, tipo_contrato in ['concessao_obras', 'concessao_servicos', 'obras', 'servicos_sociais']: as fontes não nomeiam ['servicos_sociais']

## regra:ccp:auto-limiar-art129-a-1-a@v1

- leitor:a18: {"tipo": "limiar", "condicoes": [{"field": "tipo_contrato", "op": "eq", "value": "obras"}, {"field": "tipo_procedimento", "op": "eq", "value": "ajuste_direto_simplificado"}], "params": {"threshold": {"field": "valor_estimado", "comparator": "lt", "value": 500000, "currency": "EUR"}}}
- leitor:b: não tipável (sem_vocabulario): O vocabulário não permite representar a condição relativa à finalidade das intervenções e à sua ligação a eventos que impliquem uma declaração de estado de sítio, de estado de emergência ou de situação de calamidade.
- verificador (A): regra 1: field valor_estimado e as fontes nomeiam nada (L10); regra 1: comparator lt e as fontes dizem nada (L8)

## regra:ccp:auto-limiar-art129-a-1-b@v1

- leitor:a18: {"tipo": "limiar", "condicoes": [{"field": "tipo_contrato", "op": "in", "value": ["bens", "servicos"]}, {"field": "tipo_procedimento", "op": "eq", "value": "ajuste_direto_simplificado"}], "params": {"threshold": {"field": "valor_estimado", "comparator": "lt", "value": 100000, "currency": "EUR"}}}
- leitor:b: não tipável (sem_vocabulario): O vocabulário não permite representar a finalidade das intervenções e a sua ligação a eventos que impliquem declaração de estado de sítio, de estado de emergência ou de situação de calamidade.
- verificador (A): regra 1, tipo_procedimento eq ajuste_direto_simplificado: as fontes não nomeiam ['ajuste_direto_simplificado']; regra 1: field valor_estimado e as fontes nomeiam nada (L10); regra 1: comparator lt e as fontes dizem nada (L8)

## regra:ccp:auto-prazo-minimo-art143-1@v1

- leitor:a18: não tipável (sem_vocabulario): O vocabulário não prevê um campo de prazo para o início do leilão eletrónico.
- leitor:b: não tipável (nao_e_prazo_minimo): O prazo regula o início do leilão electrónico e não a apresentação de qualquer elemento.

## regra:ccp:auto-prazo-minimo-art147@v1

- leitor:a18: {"tipo": "prazo_minimo", "condicoes": [{"field": "tipo_procedimento", "op": "eq", "value": "concurso_publico"}], "params": {"minimum_days": 5, "deadline_field": "prazo_pronuncia_dias", "counted_from": "nao_indicado", "usual_days": null}}
- leitor:b: não tipável (sem_vocabulario): O vocabulário não permite representar a condição que exclui o caso de apresentação de uma única proposta.

## regra:ccp:auto-prazo-minimo-art161-b-1-b@v1

- leitor:a18: não tipável (nao_e_prazo_minimo): O prazo é de três dias, e não um mínimo para apresentar algo.
- leitor:b: não tipável (sem_vocabulario): O vocabulário não permite representar a condição de adoção do regime de flexibilização do concurso público.

## regra:ccp:auto-prazo-minimo-art161-b-4@v1

- leitor:a18: não tipável (nao_e_prazo_minimo): Os três dias são prazos de impugnação, pronúncia dos contrainteressados e decisão, não um prazo para apresentar algo.
- leitor:b: não tipável (sem_vocabulario): O vocabulário não permite representar a aplicação do regime de flexibilização do concurso público nem o prazo de apresentação de impugnações.

## regra:ccp:auto-prazo-minimo-art185@v1

- leitor:a18: {"tipo": "prazo_minimo", "condicoes": [{"field": "tipo_procedimento", "op": "eq", "value": "concurso_limitado_previa_qualificacao"}], "params": {"minimum_days": 5, "deadline_field": "prazo_pronuncia_dias", "counted_from": "nao_indicado", "usual_days": null}}
- leitor:b: {"tipo": "prazo_minimo", "condicoes": [{"field": "tipo_procedimento", "op": "eq", "value": "concurso_limitado_previa_qualificacao"}], "params": {"minimum_days": 5, "deadline_field": "prazo_pronuncia_dias", "counted_from": "nao_indicado", "usual_days": null}}
- verificador (B): regra 1: deadline_field prazo_pronuncia_dias e as fontes dizem nada (L9)

## regra:ccp:auto-prazo-minimo-art188-2@v1

- leitor:a18: não tipável (nao_e_prazo_minimo): O prazo é de cinco dias, e não um mínimo para apresentar algo.
- leitor:b: não tipável (sem_vocabulario): O vocabulário não prevê um campo de prazo para apresentar documentos comprovativos dos requisitos de capacidade técnica e financeira e confirmar compromissos de terceiras entidades.

## regra:ccp:auto-prazo-minimo-art198-3@v1

- leitor:a18: {"tipo": "prazo_minimo", "condicoes": [{"field": "publicado_joue", "op": "eq", "value": true}, {"field": "tipo_procedimento", "op": "eq", "value": "procedimento_negociacao"}], "params": {"minimum_days": 23, "deadline_field": "prazo_candidaturas_dias", "counted_from": "data_envio_convite", "usual_days": null}}
- leitor:b: não tipável (sem_vocabulario): Falta no vocabulário um campo para a preparação e o envio dos anúncios por meios electrónicos no formato e nas modalidades indicados no portal referido.

## regra:ccp:auto-prazo-minimo-art273@v1

- leitor:a18: não tipável (nao_e_prazo_minimo): O prazo é do próprio órgão da administração para notificar, não um prazo mínimo para os interessados apresentarem algo.
- leitor:b: não tipável (sem_vocabulario): O vocabulário não permite representar a condição relativa ao objeto da impugnação administrativa.

## regra:ccp:auto-limiar-art474-2@v1

- leitor:a18: {"tipo": "limiar", "condicoes": [{"field": "tipo_contrato", "op": "in", "value": ["concessao_obras", "concessao_servicos"]}], "params": {"threshold": {"field": "valor_estimado", "comparator": "lt", "value": 5404000, "currency": "EUR"}}}
- leitor:b: não tipável (nao_e_limiar): A passagem fixa um limiar europeu, sem estabelecer um limite de valor até ao qual um procedimento pode ser escolhido.
- verificador (A): regra 1: um limiar tem sempre o procedimento que permite abaixo do valor; sem ele, L12 (nao_e_limiar); regra 1: field valor_estimado e as fontes nomeiam nada (L10); regra 1: comparator lt e as fontes dizem nada (L8)

## regra:ccp:auto-limiar-art474-3-a@v1

- leitor:a18: {"tipo": "limiar", "condicoes": [{"field": "tipo_contrato", "op": "eq", "value": "obras"}, {"field": "tipo_entidade", "op": "eq", "value": "estado"}], "params": {"threshold": {"field": "valor_estimado", "comparator": "lt", "value": 5404000, "currency": "EUR"}}}
- leitor:b: não tipável (nao_e_limiar): A passagem fixa um montante de limiar europeu, sem estabelecer um limite de valor para a escolha de um procedimento.
- verificador (A): regra 1, tipo_entidade eq estado: as fontes não nomeiam ['estado']; regra 1: um limiar tem sempre o procedimento que permite abaixo do valor; sem ele, L12 (nao_e_limiar); regra 1: field valor_estimado e as fontes nomeiam nada (L10); regra 1: comparator lt e as fontes dizem nada (L8)

## regra:ccp:auto-limiar-art474-3-b@v1

- leitor:a18: {"tipo": "limiar", "condicoes": [{"field": "tipo_contrato", "op": "in", "value": ["concessao_obras", "concessao_servicos"]}, {"field": "tipo_entidade", "op": "eq", "value": "estado"}, {"field": "tipo_procedimento", "op": "eq", "value": "concurso_concecao"}], "params": {"threshold": {"field": "valor_estimado", "comparator": "lt", "value": 139000, "currency": "EUR"}}}
- leitor:b: não tipável (nao_e_limiar): A passagem fixa um montante de limiar europeu, não um limite de valor até ao qual um procedimento pode ser escolhido.
- verificador (A): regra 1, tipo_contrato in ['concessao_obras', 'concessao_servicos']: as fontes não nomeiam ['concessao_obras', 'concessao_servicos']; regra 1: field valor_estimado e as fontes nomeiam nada (L10); regra 1: comparator lt e as fontes dizem nada (L8)

## regra:ccp:auto-limiar-art474-3-c@v1

- leitor:a18: {"tipo": "limiar", "condicoes": [{"field": "tipo_contrato", "op": "in", "value": ["concessao_obras", "concessao_servicos"]}, {"field": "tipo_entidade", "op": "eq", "value": "outra"}], "params": {"threshold": {"field": "valor_estimado", "comparator": "lt", "value": 216000, "currency": "EUR"}}}
- leitor:b: não tipável (nao_e_limiar): A passagem não fixa um limite de valor até ao qual possa ser escolhido um procedimento.
- verificador (A): regra 1, tipo_contrato in ['concessao_obras', 'concessao_servicos']: as fontes não nomeiam ['concessao_obras', 'concessao_servicos']; regra 1: um limiar tem sempre o procedimento que permite abaixo do valor; sem ele, L12 (nao_e_limiar); regra 1: field valor_estimado e as fontes nomeiam nada (L10); regra 1: comparator lt e as fontes dizem nada (L8)

## regra:ccp:auto-limiar-art474-4-a@v1

- leitor:a18: {"tipo": "limiar", "condicoes": [{"field": "publicado_joue", "op": "eq", "value": "0000-00-00"}, {"field": "tipo_contrato", "op": "eq", "value": "obras"}, {"field": "tipo_entidade", "op": "eq", "value": "estado"}], "params": {"threshold": {"field": "valor_estimado", "comparator": "lt", "value": 5404000, "currency": "EUR"}}}
- leitor:b: não tipável (nao_e_limiar): O montante é um limiar europeu, não um limite até ao qual um procedimento pode ser escolhido.
- verificador (A): regra 1, publicado_joue eq 0000-00-00: facto de dois lados usa eq true/false (L7); regra 1, tipo_entidade eq estado: as fontes não nomeiam ['estado']; regra 1: um limiar tem sempre o procedimento que permite abaixo do valor; sem ele, L12 (nao_e_limiar); regra 1: field valor_estimado e as fontes nomeiam nada (L10); regra 1: comparator lt e as fontes dizem nada (L8)

## regra:ccp:auto-limiar-art474-4-b@v1

- leitor:a18: {"tipo": "limiar", "condicoes": [{"field": "setores_especiais", "op": "eq", "value": false}, {"field": "tipo_contrato", "op": "eq", "value": "bens"}, {"field": "tipo_procedimento", "op": "in", "value": ["concurso_concecao", "consulta_previa"]}], "params": {"threshold": {"field": "valor_estimado", "comparator": "lt", "value": 432000, "currency": "EUR"}}}
- leitor:b: não tipável (nao_e_limiar): A passagem fixa um limiar europeu, não um valor até ao qual um procedimento pode ser escolhido.
- verificador (A): regra 1, setores_especiais eq False: as fontes não negam o facto (L7); regra 1, tipo_procedimento in ['concurso_concecao', 'consulta_previa']: as fontes não nomeiam ['consulta_previa']; regra 1: field valor_estimado e as fontes nomeiam nada (L10); regra 1: comparator lt e as fontes dizem nada (L8)

## regra:ccp:auto-prazo-minimo-art64-2@v1

- leitor:a18: não tipável (nao_e_prazo_minimo): O prazo é um mínimo de prorrogação, não um prazo para apresentar algo.
- leitor:b: não tipável (sem_vocabulario): O vocabulário não contém um campo para o período de prorrogação do prazo de apresentação das propostas.

## regra:ccp:auto-prazo-minimo-art78-5@v1

- leitor:a18: não tipável (nao_e_prazo_minimo): O prazo é de 30 dias para publicar os contratos celebrados ao abrigo de um acordo-quadro ou de um sistema de aquisição dinâmico, acumulados por trimestre, e não um prazo mínimo para apresentar algo.
- leitor:b: não tipável (nao_e_prazo_minimo): O prazo destina-se à publicação do anúncio pela entidade adjudicante, não à apresentação de elementos num prazo mínimo.

## regra:ccp:auto-prazo-minimo-art90-1@v1

- leitor:a18: não tipável (nao_e_prazo_minimo): O prazo é da própria entidade adjudicante para prestar a caução, não um prazo mínimo para o adjudicatário apresentar algo.
- leitor:b: não tipável (nao_e_prazo_minimo): A passagem fixa um prazo máximo para prestar a caução, não um prazo mínimo.

