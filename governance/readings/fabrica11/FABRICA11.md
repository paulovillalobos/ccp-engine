# FÁBRICA DE REGRAS — ronda 11 (DECISIONS D69)

Gerado por tools/rule_factory.py (ccp-rule-factory-0.7) com o protocolo de leitura v3 (tools/read_rules_v3.py, ccp-read-rules-v3-0.4). D69: um exame real maior. Alvos: 60 passagens do CCP em vigor que dizem dias ou euros e que nenhuma ronda leu, tiradas uma vez: as 28 de artigos reservados que nenhum exemplo de treino mostra (reservado) e 32 das outras pelo sha256 do id (texto_visto: outras tarefas mostram o texto, nenhuma leitura de regra o faz). Adaptador v14. Propõe leitor:a16 (AMALIA + adaptador v14), leitor:b revê às cegas.

Muitas destas passagens dizem um prazo que não é um mínimo ou um valor que não é um limiar: o «não tipável» com o mesmo motivo também assenta. leitor:b responde a prompts novos (protocolo 0.4). Um programa confirma cada palavra citada; a leitura que falha não fica registada.

| grupo | alvos | leitor A válido | leitor B válido | assentes | regras | «não tipável» |
|---|---|---|---|---|---|---|
| reservado | 28 | 19 | 27 | 13 | 0 | 13 |
| texto_visto | 32 | 24 | 32 | 22 | 1 | 21 |
| todos | 60 | 43 | 59 | 35 | 1 | 34 |

| regra | passagem | estado | replica | verificador: leitor A | verificador: leitor B |
|---|---|---|---|---|---|
| regra:ccp:auto-prazo-minimo-art101@v1 | ccp:art101 | settled (não tipável: nao_e_prazo_minimo) | sim | ok | ok |
| regra:ccp:auto-prazo-minimo-art102-2@v1 | ccp:art102.2 | settled (não tipável: nao_e_prazo_minimo) | sim | ok | ok |
| regra:ccp:auto-prazo-minimo-art116@v1 | ccp:art116 | settled (não tipável: nao_e_prazo_minimo) | sim | ok | ok |
| regra:ccp:auto-prazo-minimo-art120-1@v1 | ccp:art120.1 | settled (não tipável: nao_e_prazo_minimo) | sim | ok | ok |
| regra:ccp:auto-prazo-minimo-art123-1@v1 | ccp:art123.1 | settled | sim | ok | ok |
| regra:ccp:auto-limiar-art127-b@v1 | ccp:art127-b | sem leitura válida de leitor:a16 | — | regra 1, tipo_contrato in ['concessao_obras', 'concessao_servicos', 'obras', 'servicos', 'servicos_sociais']: as fontes  | ok |
| regra:ccp:auto-limiar-art129-a-1-a@v1 | ccp:art129-a.1.a | sem leitura válida de leitor:a16 | — | regra 1: field valor_estimado e as fontes nomeiam nada (L10) | ok |
| regra:ccp:auto-limiar-art129-a-1-b@v1 | ccp:art129-a.1.b | sem leitura válida de leitor:a16 | — | regra 1, tipo_procedimento eq ajuste_direto_simplificado: as fontes não nomeiam ['ajuste_direto_simplificado'] | ok |
| regra:ccp:auto-prazo-minimo-art129-a-6@v1 | ccp:art129-a.6 | settled (não tipável: nao_e_prazo_minimo) | sim | ok | ok |
| regra:ccp:auto-prazo-minimo-art138-3@v1 | ccp:art138.3 | settled (não tipável: nao_e_prazo_minimo) | sim | ok | ok |
| regra:ccp:auto-prazo-minimo-art143-1@v1 | ccp:art143.1 | proposed (não tipável: sem_vocabulario) | não | ok | ok |
| regra:ccp:auto-prazo-minimo-art147@v1 | ccp:art147 | proposed | não | ok | ok |
| regra:ccp:auto-prazo-minimo-art161-b-1-b@v1 | ccp:art161-b.1.b | proposed | não | ok | ok |
| regra:ccp:auto-prazo-minimo-art161-b-4@v1 | ccp:art161-b.4 | sem leitura válida de leitor:a16 | — | regra 1: deadline_field prazo_pronuncia_dias e as fontes dizem nada (L9) | ok |
| regra:ccp:auto-prazo-minimo-art177-3@v1 | ccp:art177.3 | settled (não tipável: nao_e_prazo_minimo) | sim | ok | ok |
| regra:ccp:auto-prazo-minimo-art185@v1 | ccp:art185 | proposed | — | ok | regra 1: deadline_field prazo_pronuncia_dias e as fontes dizem nada (L9) |
| regra:ccp:auto-prazo-minimo-art188-2@v1 | ccp:art188.2 | sem leitura válida de leitor:a16 | — | regra 1: deadline_field prazo_pronuncia_dias e as fontes dizem nada (L9) | ok |
| regra:ccp:auto-prazo-minimo-art188-4@v1 | ccp:art188.4 | settled (não tipável: nao_e_prazo_minimo) | sim | ok | ok |
| regra:ccp:auto-prazo-minimo-art198-3@v1 | ccp:art198.3 | sem leitura válida de leitor:a16 | — | regra 2: minimum_days 18 não está nas fontes (L8, L4) | ok |
| regra:ccp:auto-prazo-minimo-art219-c-3@v1 | ccp:art219-c.3 | sem leitura válida de leitor:a16 | — | regra 1: deadline_field prazo_pronuncia_dias e as fontes dizem nada (L9) | ok |
| regra:ccp:auto-prazo-minimo-art266-b-3@v1 | ccp:art266-b.3 | settled (não tipável: nao_e_prazo_minimo) | sim | ok | ok |
| regra:ccp:auto-prazo-minimo-art270@v1 | ccp:art270 | settled (não tipável: nao_e_prazo_minimo) | sim | ok | ok |
| regra:ccp:auto-prazo-minimo-art273@v1 | ccp:art273 | proposed (não tipável: nao_e_prazo_minimo) | não | ok | ok |
| regra:ccp:auto-prazo-minimo-art274-1@v1 | ccp:art274.1 | settled (não tipável: nao_e_prazo_minimo) | sim | ok | ok |
| regra:ccp:auto-prazo-minimo-art283-a-2-c@v1 | ccp:art283-a.2.c | settled (não tipável: nao_e_prazo_minimo) | sim | ok | ok |
| regra:ccp:auto-prazo-minimo-art299-1-c@v1 | ccp:art299.1.c | settled (não tipável: nao_e_prazo_minimo) | sim | ok | ok |
| regra:ccp:auto-prazo-minimo-art304-3@v1 | ccp:art304.3 | settled (não tipável: nao_e_prazo_minimo) | sim | ok | ok |
| regra:ccp:auto-prazo-minimo-art327-3@v1 | ccp:art327.3 | settled (não tipável: nao_e_prazo_minimo) | sim | ok | ok |
| regra:ccp:auto-prazo-minimo-art327-4@v1 | ccp:art327.4 | settled (não tipável: nao_e_prazo_minimo) | sim | ok | ok |
| regra:ccp:auto-prazo-minimo-art333-4@v1 | ccp:art333.4 | settled (não tipável: nao_e_prazo_minimo) | sim | ok | ok |
| regra:ccp:auto-prazo-minimo-art345-5@v1 | ccp:art345.5 | settled (não tipável: nao_e_prazo_minimo) | sim | ok | ok |
| regra:ccp:auto-prazo-minimo-art359-1@v1 | ccp:art359.1 | settled (não tipável: nao_e_prazo_minimo) | sim | ok | ok |
| regra:ccp:auto-limiar-art36-4@v1 | ccp:art36.4 | settled (não tipável: nao_e_limiar) | sim | ok | ok |
| regra:ccp:auto-prazo-minimo-art372-3-a@v1 | ccp:art372.3.a | settled (não tipável: nao_e_prazo_minimo) | sim | ok | ok |
| regra:ccp:auto-prazo-minimo-art373-2@v1 | ccp:art373.2 | sem leitura válida de leitor:a16 | — | regra 1, tipo_procedimento eq concurso_publico: as fontes não nomeiam ['concurso_publico'] | ok |
| regra:ccp:auto-prazo-minimo-art373-3@v1 | ccp:art373.3 | sem leitura válida de leitor:a16 | — | regra 1: deadline_field prazo_propostas_dias e as fontes dizem nada (L9) | ok |
| regra:ccp:auto-prazo-minimo-art389-1@v1 | ccp:art389.1 | settled (não tipável: nao_e_prazo_minimo) | sim | ok | ok |
| regra:ccp:auto-prazo-minimo-art394-7@v1 | ccp:art394.7 | settled (não tipável: nao_e_prazo_minimo) | sim | ok | ok |
| regra:ccp:auto-prazo-minimo-art401-1@v1 | ccp:art401.1 | settled (não tipável: nao_e_prazo_minimo) | sim | ok | ok |
| regra:ccp:auto-prazo-minimo-art404-1@v1 | ccp:art404.1 | settled (não tipável: nao_e_prazo_minimo) | sim | ok | ok |
| regra:ccp:auto-prazo-minimo-art405-2@v1 | ccp:art405.2 | settled (não tipável: nao_e_prazo_minimo) | sim | ok | ok |
| regra:ccp:auto-prazo-minimo-art43-10-c@v1 | ccp:art43.10.c | settled (não tipável: nao_e_prazo_minimo) | sim | ok | ok |
| regra:ccp:auto-prazo-minimo-art464-g@v1 | ccp:art464-g | settled (não tipável: nao_e_prazo_minimo) | sim | ok | ok |
| regra:ccp:auto-limiar-art474-2@v1 | ccp:art474.2 | sem leitura válida de leitor:a16 | — | regra 1: um limiar tem sempre o procedimento que permite abaixo do valor; sem ele, L12 (nao_e_limiar) | ok |
| regra:ccp:auto-limiar-art474-3-a@v1 | ccp:art474.3.a | sem leitura válida de leitor:a16 | — | regra 1, tipo_entidade eq estado: as fontes não nomeiam ['estado'] | ok |
| regra:ccp:auto-limiar-art474-3-b@v1 | ccp:art474.3.b | sem leitura válida de leitor:a16 | — | regra 1, tipo_contrato in ['bens', 'servicos', 'concessao_servicos', 'concessao_obras']: as fontes não nomeiam ['concess | ok |
| regra:ccp:auto-limiar-art474-3-c@v1 | ccp:art474.3.c | sem leitura válida de leitor:a16 | — | regra 1, tipo_contrato in ['concessao_obras', 'concessao_servicos', 'servicos_sociais']: as fontes não nomeiam ['concess | ok |
| regra:ccp:auto-limiar-art474-3-d@v1 | ccp:art474.3.d | proposed (não tipável: texto_em_falta) | não | ok | ok |
| regra:ccp:auto-limiar-art474-4-a@v1 | ccp:art474.4.a | sem leitura válida de leitor:a16 | — | regra 1, tipo_entidade eq estado: as fontes não nomeiam ['estado'] | ok |
| regra:ccp:auto-limiar-art474-4-b@v1 | ccp:art474.4.b | sem leitura válida de leitor:a16 | — | regra 1, setores_especiais eq False: as fontes não negam o facto (L7) | ok |
| regra:ccp:auto-limiar-art474-4-c@v1 | ccp:art474.4.c | proposed (não tipável: texto_em_falta) | não | ok | ok |
| regra:ccp:auto-prazo-minimo-art64-2@v1 | ccp:art64.2 | sem leitura válida de leitor:a16 | — | regra 1, tipo_procedimento eq concurso_publico: as fontes não nomeiam ['concurso_publico'] | ok |
| regra:ccp:auto-prazo-minimo-art65@v1 | ccp:art65 | settled (não tipável: nao_e_prazo_minimo) | sim | ok | ok |
| regra:ccp:auto-prazo-minimo-art72-3@v1 | ccp:art72.3 | settled (não tipável: nao_e_prazo_minimo) | sim | ok | ok |
| regra:ccp:auto-prazo-minimo-art78-1@v1 | ccp:art78.1 | settled (não tipável: nao_e_prazo_minimo) | sim | ok | ok |
| regra:ccp:auto-prazo-minimo-art78-5@v1 | ccp:art78.5 | proposed (não tipável: sem_vocabulario) | não | ok | ok |
| regra:ccp:auto-prazo-minimo-art85-2@v1 | ccp:art85.2 | settled (não tipável: nao_e_prazo_minimo) | sim | ok | ok |
| regra:ccp:auto-prazo-minimo-art87-a-2@v1 | ccp:art87-a.2 | settled (não tipável: nao_e_prazo_minimo) | sim | ok | ok |
| regra:ccp:auto-prazo-minimo-art90-1@v1 | ccp:art90.1 | sem leitura válida de leitor:a16 | — | regra 1, tipo_contrato eq servicos_sociais: as fontes não nomeiam ['servicos_sociais'] | ok |
| regra:ccp:auto-prazo-minimo-art93-2@v1 | ccp:art93.2 | settled (não tipável: nao_e_prazo_minimo) | sim | ok | ok |

## regra:ccp:auto-prazo-minimo-art101@v1

- leitor:a16: não tipável (nao_e_prazo_minimo): O prazo é da própria entidade adjudicante para decidir, não um prazo para os interessados apresentarem algo.
- leitor:b: não tipável (nao_e_prazo_minimo): A passagem fixa o período para reclamar antes da aceitação tácita da minuta, sem estabelecer um prazo mínimo.

## regra:ccp:auto-prazo-minimo-art102-2@v1

- leitor:a16: não tipável (nao_e_prazo_minimo): O prazo é do próprio órgão que aprova a minuta do contrato para notificar, não um prazo mínimo para os interessados apresentarem algo.
- leitor:b: não tipável (nao_e_prazo_minimo): O prazo destina-se à notificação da decisão pela entidade adjudicante, não à apresentação de elementos.

## regra:ccp:auto-prazo-minimo-art116@v1

- leitor:a16: não tipável (nao_e_prazo_minimo): O prazo é o máximo de dias para os esclarecimentos e retificações, não um prazo mínimo para apresentar algo.
- leitor:b: não tipável (nao_e_prazo_minimo): A passagem estabelece um prazo para prestar esclarecimentos e efetuar retificações, sem fixar um prazo mínimo para apresentar a proposta.

## regra:ccp:auto-prazo-minimo-art120-1@v1

- leitor:a16: não tipável (nao_e_prazo_minimo): O prazo é da própria entidade adjudicante para notificar os concorrentes, não um prazo para os concorrentes apresentarem algo.
- leitor:b: não tipável (nao_e_prazo_minimo): A passagem fixa uma antecedência mínima para a notificação pelo júri, não um prazo para apresentar algo.

## regra:ccp:auto-prazo-minimo-art123-1@v1

- leitor:a16: {"tipo": "prazo_minimo", "condicoes": [{"field": "tipo_procedimento", "op": "in", "value": ["ajuste_direto", "consulta_previa"]}], "params": {"minimum_days": 3, "deadline_field": "prazo_pronuncia_dias", "counted_from": "nao_indicado", "usual_days": null}}
- leitor:b: {"tipo": "prazo_minimo", "condicoes": [{"field": "tipo_procedimento", "op": "in", "value": ["ajuste_direto", "consulta_previa"]}], "params": {"minimum_days": 3, "deadline_field": "prazo_pronuncia_dias", "counted_from": "nao_indicado", "usual_days": null}}

## regra:ccp:auto-limiar-art127-b@v1

- leitor:a16: {"tipo": "limiar", "condicoes": [{"field": "tipo_contrato", "op": "in", "value": ["concessao_obras", "concessao_servicos", "obras", "servicos", "servicos_sociais"]}, {"field": "tipo_procedimento", "op": "eq", "value": "consulta_previa_especial"}], "params": {"threshold": {"field": "valor_estimado", "comparator": "lt", "value": 2000000, "currency": "EUR"}}}
- leitor:b: não tipável (sem_vocabulario): O vocabulário não permite representar a condição de o contrato ter um dos objetos previstos nas alíneas a) a f), necessária para delimitar a adoção da consulta prévia especial.
- verificador (A): regra 1, tipo_contrato in ['concessao_obras', 'concessao_servicos', 'obras', 'servicos', 'servicos_sociais']: as fontes não nomeiam ['servicos_sociais']

## regra:ccp:auto-limiar-art129-a-1-a@v1

- leitor:a16: {"tipo": "limiar", "condicoes": [{"field": "tipo_contrato", "op": "eq", "value": "obras"}, {"field": "tipo_procedimento", "op": "eq", "value": "ajuste_direto_simplificado"}], "params": {"threshold": {"field": "valor_estimado", "comparator": "lt", "value": 500000, "currency": "EUR"}}}
- leitor:b: não tipável (sem_vocabulario): O vocabulário não permite representar a condição relativa à finalidade das intervenções e à sua ligação a eventos que impliquem uma declaração de estado de sítio, de estado de emergência ou de situação de calamidade.
- verificador (A): regra 1: field valor_estimado e as fontes nomeiam nada (L10); regra 1: comparator lt e as fontes dizem nada (L8)

## regra:ccp:auto-limiar-art129-a-1-b@v1

- leitor:a16: {"tipo": "limiar", "condicoes": [{"field": "tipo_contrato", "op": "in", "value": ["bens", "servicos"]}, {"field": "tipo_procedimento", "op": "eq", "value": "ajuste_direto_simplificado"}], "params": {"threshold": {"field": "valor_estimado", "comparator": "lt", "value": 100000, "currency": "EUR"}}}
- leitor:b: não tipável (sem_vocabulario): O vocabulário não permite representar a finalidade das intervenções e a sua ligação a eventos que impliquem declaração de estado de sítio, de estado de emergência ou de situação de calamidade.
- verificador (A): regra 1, tipo_procedimento eq ajuste_direto_simplificado: as fontes não nomeiam ['ajuste_direto_simplificado']; regra 1: field valor_estimado e as fontes nomeiam nada (L10); regra 1: comparator lt e as fontes dizem nada (L8)

## regra:ccp:auto-prazo-minimo-art129-a-6@v1

- leitor:a16: não tipável (nao_e_prazo_minimo): Os 30 dias são um prazo máximo para a estipulação e redução a escrito, não um prazo mínimo para apresentar algo.
- leitor:b: não tipável (nao_e_prazo_minimo): A passagem fixa um prazo máximo para a estipulação e redução a escrito, não um prazo mínimo para apresentar algo.

## regra:ccp:auto-prazo-minimo-art138-3@v1

- leitor:a16: não tipável (nao_e_prazo_minimo): Os três dias são o prazo para reclamar, não um prazo mínimo para apresentar alguma coisa.
- leitor:b: não tipável (nao_e_prazo_minimo): A passagem fixa um prazo máximo para reclamar, não um prazo mínimo.

## regra:ccp:auto-prazo-minimo-art143-1@v1

- leitor:a16: não tipável (sem_vocabulario): A regra é de um leilão eletrónico, instrumento que o vocabulário não tem.
- leitor:b: não tipável (nao_e_prazo_minimo): O prazo regula o início do leilão electrónico e não a apresentação de qualquer elemento.

## regra:ccp:auto-prazo-minimo-art147@v1

- leitor:a16: {"tipo": "prazo_minimo", "condicoes": [{"field": "tipo_procedimento", "op": "eq", "value": "concurso_publico"}], "params": {"minimum_days": 5, "deadline_field": "prazo_pronuncia_dias", "counted_from": "nao_indicado", "usual_days": null}}
- leitor:b: não tipável (sem_vocabulario): O vocabulário não permite representar a condição que exclui o caso de apresentação de uma única proposta.

## regra:ccp:auto-prazo-minimo-art161-b-1-b@v1

- leitor:a16: {"tipo": "prazo_minimo", "condicoes": [{"field": "tipo_procedimento", "op": "eq", "value": "concurso_publico"}], "params": {"minimum_days": 3, "deadline_field": "prazo_pronuncia_dias", "counted_from": "nao_indicado", "usual_days": null}}
- leitor:b: não tipável (sem_vocabulario): O vocabulário não permite representar a condição de adoção do regime de flexibilização do concurso público.

## regra:ccp:auto-prazo-minimo-art161-b-4@v1

- leitor:a16: {"tipo": "prazo_minimo", "condicoes": [{"field": "tipo_procedimento", "op": "eq", "value": "concurso_publico"}], "params": {"minimum_days": 3, "deadline_field": "prazo_pronuncia_dias", "counted_from": "nao_indicado", "usual_days": null}}
- leitor:b: não tipável (sem_vocabulario): O vocabulário não permite representar a aplicação do regime de flexibilização do concurso público nem o prazo de apresentação de impugnações.
- verificador (A): regra 1: deadline_field prazo_pronuncia_dias e as fontes dizem nada (L9)

## regra:ccp:auto-prazo-minimo-art177-3@v1

- leitor:a16: não tipável (nao_e_prazo_minimo): O prazo é de três dias para reclamar, não um prazo mínimo para apresentar algo.
- leitor:b: não tipável (nao_e_prazo_minimo): A passagem fixa um prazo máximo para reclamar, não um prazo mínimo.

## regra:ccp:auto-prazo-minimo-art185@v1

- leitor:a16: {"tipo": "prazo_minimo", "condicoes": [{"field": "tipo_procedimento", "op": "eq", "value": "concurso_limitado_previa_qualificacao"}], "params": {"minimum_days": 5, "deadline_field": "prazo_pronuncia_dias", "counted_from": "nao_indicado", "usual_days": null}}
- leitor:b: {"tipo": "prazo_minimo", "condicoes": [{"field": "tipo_procedimento", "op": "eq", "value": "concurso_limitado_previa_qualificacao"}], "params": {"minimum_days": 5, "deadline_field": "prazo_pronuncia_dias", "counted_from": "nao_indicado", "usual_days": null}}
- verificador (B): regra 1: deadline_field prazo_pronuncia_dias e as fontes dizem nada (L9)

## regra:ccp:auto-prazo-minimo-art188-2@v1

- leitor:a16: {"tipo": "prazo_minimo", "condicoes": [{"field": "tipo_procedimento", "op": "eq", "value": "concurso_limitado_previa_qualificacao"}], "params": {"minimum_days": 5, "deadline_field": "prazo_pronuncia_dias", "counted_from": "nao_indicado", "usual_days": null}}
- leitor:b: não tipável (sem_vocabulario): O vocabulário não prevê um campo de prazo para apresentar documentos comprovativos dos requisitos de capacidade técnica e financeira e confirmar compromissos de terceiras entidades.
- verificador (A): regra 1: deadline_field prazo_pronuncia_dias e as fontes dizem nada (L9)

## regra:ccp:auto-prazo-minimo-art188-4@v1

- leitor:a16: não tipável (nao_e_prazo_minimo): O prazo é máximo: cinco dias, e não um mínimo.
- leitor:b: não tipável (nao_e_prazo_minimo): A passagem fixa um prazo máximo de cinco dias para pronúncia, não um prazo mínimo.

## regra:ccp:auto-prazo-minimo-art198-3@v1

- leitor:a16: {"tipo": "prazo_minimo", "condicoes": [{"field": "publicado_joue", "op": "eq", "value": true}, {"field": "tipo_procedimento", "op": "eq", "value": "procedimento_negociacao"}], "params": {"minimum_days": 23, "deadline_field": "prazo_candidaturas_dias", "counted_from": "data_envio_anuncio", "usual_days": null}} || {"tipo": "prazo_minimo", "condicoes": [{"field": "anuncio_pre_informacao", "op": "eq", "value": true}, {"field": "publicado_joue", "op": "eq", "value": true}, {"field": "tipo_procedimento", "op": "eq", "value": "procedimento_negociacao"}], "params": {"minimum_days": 18, "deadline_field": "prazo_candidaturas_dias", "counted_from": "data_envio_convite", "usual_days": null}}
- leitor:b: não tipável (sem_vocabulario): Falta no vocabulário um campo para a preparação e o envio dos anúncios por meios electrónicos no formato e nas modalidades indicados no portal referido.
- verificador (A): regra 2: minimum_days 18 não está nas fontes (L8, L4)

## regra:ccp:auto-prazo-minimo-art219-c-3@v1

- leitor:a16: {"tipo": "prazo_minimo", "condicoes": [{"field": "publicado_joue", "op": "eq", "value": true}, {"field": "tipo_procedimento", "op": "eq", "value": "concurso_concecao"}], "params": {"minimum_days": 30, "deadline_field": "prazo_pronuncia_dias", "counted_from": "data_publicacao_anuncio", "usual_days": null}}
- leitor:b: não tipável (nao_e_prazo_minimo): O prazo é para a própria entidade adjudicante enviar um anúncio.
- verificador (A): regra 1: deadline_field prazo_pronuncia_dias e as fontes dizem nada (L9); regra 1: counted_from data_publicacao_anuncio e as fontes dizem nada (L9)

## regra:ccp:auto-prazo-minimo-art266-b-3@v1

- leitor:a16: não tipável (nao_e_prazo_minimo): O prazo é a duração da publicitação, não um prazo para apresentar algo.
- leitor:b: não tipável (nao_e_prazo_minimo): O prazo refere-se à duração da publicitação pela entidade adjudicante, não à apresentação de qualquer elemento pelos interessados.

## regra:ccp:auto-prazo-minimo-art270@v1

- leitor:a16: não tipável (nao_e_prazo_minimo): O prazo é de cinco dias para apresentar uma impugnação, não um prazo mínimo para apresentar algo.
- leitor:b: não tipável (nao_e_prazo_minimo): O prazo de cinco dias é um prazo máximo para apresentar impugnações administrativas, não um prazo mínimo.

## regra:ccp:auto-prazo-minimo-art273@v1

- leitor:a16: não tipável (nao_e_prazo_minimo): O prazo é do próprio órgão da administração para notificar, não um prazo mínimo para os interessados apresentarem algo.
- leitor:b: não tipável (sem_vocabulario): O vocabulário não permite representar a condição relativa ao objeto da impugnação administrativa.

## regra:ccp:auto-prazo-minimo-art274-1@v1

- leitor:a16: não tipável (nao_e_prazo_minimo): O prazo é da própria entidade adjudicante para decidir, não um prazo para os interessados apresentarem algo.
- leitor:b: não tipável (nao_e_prazo_minimo): O prazo é para decidir as impugnações administrativas, não para apresentar algo.

## regra:ccp:auto-prazo-minimo-art283-a-2-c@v1

- leitor:a16: não tipável (nao_e_prazo_minimo): O prazo é de 10 dias antes da outorga do contrato, não um prazo para apresentar algo.
- leitor:b: não tipável (nao_e_prazo_minimo): O prazo respeita à outorga do contrato, não à apresentação de qualquer elemento.

## regra:ccp:auto-prazo-minimo-art299-1-c@v1

- leitor:a16: não tipável (nao_e_prazo_minimo): O prazo é de 30 dias para efetuar o pagamento, não um prazo mínimo para apresentar algo.
- leitor:b: não tipável (nao_e_prazo_minimo): O prazo fixa o vencimento de uma obrigação pecuniária e não é para apresentar nada.

## regra:ccp:auto-prazo-minimo-art304-3@v1

- leitor:a16: não tipável (nao_e_prazo_minimo): O prazo de cinco dias é da própria entidade adjudicante para reduzir a forma, não um prazo mínimo para os interessados.
- leitor:b: não tipável (nao_e_prazo_minimo): O prazo de cinco dias destina-se à redução a escrito e notificação de ordens, directivas ou instruções, não sendo um prazo mínimo para apresentar algo.

## regra:ccp:auto-prazo-minimo-art327-3@v1

- leitor:a16: não tipável (nao_e_prazo_minimo): Os 15 dias são o prazo do próprio cocontratante para notificar a intenção de exercício do direito, não um prazo mínimo para a entidade adjudicante.
- leitor:b: não tipável (nao_e_prazo_minimo): O prazo estabelece a antecedência da notificação da intenção de exercer um direito, não um prazo para apresentar algo.

## regra:ccp:auto-prazo-minimo-art327-4@v1

- leitor:a16: não tipável (nao_e_prazo_minimo): O prazo é do próprio contraente público para se opor, não um prazo mínimo para o cocontratante apresentar algo.
- leitor:b: não tipável (nao_e_prazo_minimo): O prazo destina-se ao contraente público para exercer oposição e não fixa um prazo mínimo de apresentação.

## regra:ccp:auto-prazo-minimo-art333-4@v1

- leitor:a16: não tipável (nao_e_prazo_minimo): O prazo é da própria entidade pública para comunicar, não um prazo mínimo para os interessados apresentarem algo.
- leitor:b: não tipável (nao_e_prazo_minimo): O prazo é para uma comunicação do contraente público, não um prazo mínimo para apresentar algo.

## regra:ccp:auto-prazo-minimo-art345-5@v1

- leitor:a16: não tipável (nao_e_prazo_minimo): O prazo é do próprio dono da obra para notificar, não um prazo mínimo para o empreiteiro apresentar algo.
- leitor:b: não tipável (nao_e_prazo_minimo): A passagem fixa um prazo para o dono da obra decidir e notificar o empreiteiro, não um prazo mínimo de apresentação.

## regra:ccp:auto-prazo-minimo-art359-1@v1

- leitor:a16: não tipável (nao_e_prazo_minimo): O prazo é um máximo, não um mínimo.
- leitor:b: não tipável (nao_e_prazo_minimo): A passagem fixa um prazo máximo para concluir a consignação, não um prazo mínimo para apresentar algo.

## regra:ccp:auto-limiar-art36-4@v1

- leitor:a16: não tipável (nao_e_limiar): O valor não é o limite até ao qual um procedimento pode ser escolhido
- leitor:b: não tipável (nao_e_limiar): Os valores determinam uma obrigação de fundamentação, não um limite até ao qual um procedimento pode ser escolhido.

## regra:ccp:auto-prazo-minimo-art372-3-a@v1

- leitor:a16: não tipável (nao_e_prazo_minimo): O prazo é do próprio dono da obra para notificar, não um prazo mínimo para o empreiteiro apresentar algo.
- leitor:b: não tipável (nao_e_prazo_minimo): O prazo é de antecedência da notificação para execução de trabalhos, não para apresentar algo.

## regra:ccp:auto-prazo-minimo-art373-2@v1

- leitor:a16: {"tipo": "prazo_minimo", "condicoes": [{"field": "tipo_contrato", "op": "eq", "value": "obras"}, {"field": "tipo_procedimento", "op": "eq", "value": "concurso_publico"}], "params": {"minimum_days": 15, "deadline_field": "prazo_propostas_dias", "counted_from": "data_disponibilizacao_pecas", "usual_days": null}}
- leitor:b: não tipável (nao_e_prazo_minimo): O prazo de 15 dias é um prazo máximo para apresentar a proposta, não um prazo mínimo.
- verificador (A): regra 1, tipo_procedimento eq concurso_publico: as fontes não nomeiam ['concurso_publico']; regra 1: deadline_field prazo_propostas_dias e as fontes dizem nada (L9); regra 1: counted_from data_disponibilizacao_pecas e as fontes dizem nada (L9)

## regra:ccp:auto-prazo-minimo-art373-3@v1

- leitor:a16: {"tipo": "prazo_minimo", "condicoes": [{"field": "tipo_contrato", "op": "eq", "value": "obras"}], "params": {"minimum_days": 15, "deadline_field": "prazo_propostas_dias", "counted_from": "data_notificacao", "usual_days": null}}
- leitor:b: não tipável (nao_e_prazo_minimo): A passagem fixa um prazo máximo para o empreiteiro apresentar a proposta, não um prazo mínimo.
- verificador (A): regra 1: deadline_field prazo_propostas_dias e as fontes dizem nada (L9); regra 1: counted_from data_notificacao e as fontes dizem nada (L9)

## regra:ccp:auto-prazo-minimo-art389-1@v1

- leitor:a16: não tipável (nao_e_prazo_minimo): O prazo é da empreiteira para elaborar a conta corrente, não um prazo mínimo para a entidade adjudicante apresentar algo.
- leitor:b: não tipável (nao_e_prazo_minimo): A passagem fixa um prazo para elaborar a conta corrente, sem estabelecer um prazo mínimo de apresentação.

## regra:ccp:auto-prazo-minimo-art394-7@v1

- leitor:a16: não tipável (nao_e_prazo_minimo): O prazo é do próprio dono da obra para vistoriar, não um prazo para os interessados apresentarem algo.
- leitor:b: não tipável (nao_e_prazo_minimo): O prazo refere-se ao agendamento ou realização da vistoria pelo dono da obra, com efeitos de receção tácita, e não à apresentação de algo.

## regra:ccp:auto-prazo-minimo-art401-1@v1

- leitor:a16: não tipável (nao_e_prazo_minimo): O prazo é da própria entidade adjudicante para enviar a conta final, não um prazo mínimo para o empreiteiro apresentar algo.
- leitor:b: não tipável (nao_e_prazo_minimo): A passagem fixa prazos máximos para enviar a conta final e para a assinar ou apresentar reclamação, sem estabelecer um prazo mínimo.

## regra:ccp:auto-prazo-minimo-art404-1@v1

- leitor:a16: não tipável (nao_e_prazo_minimo): O prazo é do próprio dono da obra para notificar o empreiteiro, não um prazo mínimo para o empreiteiro apresentar algo.
- leitor:b: não tipável (nao_e_prazo_minimo): A passagem fixa um prazo máximo para apresentar um plano de trabalhos modificado, e não um prazo mínimo.

## regra:ccp:auto-prazo-minimo-art405-2@v1

- leitor:a16: não tipável (nao_e_prazo_minimo): O prazo é da própria entidade adjudicante para informar o Instituto dos Mercados Públicos, do Imobiliário e da Construção, I. P.; não é um prazo mínimo para os interessados apresentarem algo.
- leitor:b: não tipável (nao_e_prazo_minimo): O prazo destina-se ao cumprimento de uma obrigação de informação pelo dono da obra.

## regra:ccp:auto-prazo-minimo-art43-10-c@v1

- leitor:a16: não tipável (nao_e_prazo_minimo): Os cinco dias são o prazo da entidade adjudicante para apresentar as razões que justificam a não exigência dos elementos do n.º 5, não um prazo mínimo para os interessados apresentarem algo.
- leitor:b: não tipável (nao_e_prazo_minimo): O prazo destina-se à própria entidade adjudicante para apresentar razões que justificam a não exigência de elementos; não fixa um prazo mínimo.

## regra:ccp:auto-prazo-minimo-art464-g@v1

- leitor:a16: não tipável (nao_e_prazo_minimo): O prazo é de prescrição e caducidade, não um prazo para apresentar algo.
- leitor:b: não tipável (nao_e_prazo_minimo): A passagem fixa o reinício dos prazos de prescrição e de caducidade, não um prazo mínimo para apresentar algo.

## regra:ccp:auto-limiar-art474-2@v1

- leitor:a16: {"tipo": "limiar", "condicoes": [{"field": "tipo_contrato", "op": "eq", "value": "concessao_obras"}], "params": {"threshold": {"field": "valor_estimado", "comparator": "ge", "value": 5404000, "currency": "EUR"}}}
- leitor:b: não tipável (nao_e_limiar): A passagem fixa um limiar europeu, sem estabelecer um limite de valor até ao qual um procedimento pode ser escolhido.
- verificador (A): regra 1: um limiar tem sempre o procedimento que permite abaixo do valor; sem ele, L12 (nao_e_limiar); regra 1: field valor_estimado e as fontes nomeiam nada (L10); regra 1: comparator ge e as fontes dizem nada (L8)

## regra:ccp:auto-limiar-art474-3-a@v1

- leitor:a16: {"tipo": "limiar", "condicoes": [{"field": "tipo_contrato", "op": "eq", "value": "obras"}, {"field": "tipo_entidade", "op": "eq", "value": "estado"}], "params": {"threshold": {"field": "valor_estimado", "comparator": "lt", "value": 5404000, "currency": "EUR"}}}
- leitor:b: não tipável (nao_e_limiar): A passagem fixa um montante de limiar europeu, sem estabelecer um limite de valor para a escolha de um procedimento.
- verificador (A): regra 1, tipo_entidade eq estado: as fontes não nomeiam ['estado']; regra 1: um limiar tem sempre o procedimento que permite abaixo do valor; sem ele, L12 (nao_e_limiar); regra 1: field valor_estimado e as fontes nomeiam nada (L10); regra 1: comparator lt e as fontes dizem nada (L8)

## regra:ccp:auto-limiar-art474-3-b@v1

- leitor:a16: {"tipo": "limiar", "condicoes": [{"field": "tipo_contrato", "op": "in", "value": ["bens", "concessao_obras", "concessao_servicos", "servicos"]}, {"field": "tipo_entidade", "op": "eq", "value": "estado"}, {"field": "tipo_procedimento", "op": "in", "value": ["concurso_concecao", "concurso_publico", "consulta_previa"]}], "params": {"threshold": {"field": "valor_estimado", "comparator": "lt", "value": 139000, "currency": "EUR"}}}
- leitor:b: não tipável (nao_e_limiar): A passagem fixa um montante de limiar europeu, não um limite de valor até ao qual um procedimento pode ser escolhido.
- verificador (A): regra 1, tipo_contrato in ['bens', 'servicos', 'concessao_servicos', 'concessao_obras']: as fontes não nomeiam ['concessao_obras', 'concessao_servicos']; regra 1, tipo_procedimento in ['concurso_concecao', 'consulta_previa', 'concurso_publico']: as fontes não nomeiam ['concurso_publico', 'consulta_previa']; regra 1: field valor_estimado e as fontes nomeiam nada (L10); regra 1: comparator lt e as fontes dizem nada (L8)

## regra:ccp:auto-limiar-art474-3-c@v1

- leitor:a16: {"tipo": "limiar", "condicoes": [{"field": "tipo_contrato", "op": "in", "value": ["concessao_obras", "concessao_servicos", "servicos_sociais"]}, {"field": "tipo_entidade", "op": "eq", "value": "outra"}, {"field": "tipo_procedimento", "op": "eq", "value": "concurso_concecao"}], "params": {"threshold": {"field": "valor_estimado", "comparator": "lt", "value": 216000, "currency": "EUR"}}}
- leitor:b: não tipável (nao_e_limiar): A passagem não fixa um limite de valor até ao qual possa ser escolhido um procedimento.
- verificador (A): regra 1, tipo_contrato in ['concessao_obras', 'concessao_servicos', 'servicos_sociais']: as fontes não nomeiam ['concessao_obras', 'concessao_servicos', 'servicos_sociais']; regra 1: field valor_estimado e as fontes nomeiam nada (L10); regra 1: comparator lt e as fontes dizem nada (L8)

## regra:ccp:auto-limiar-art474-3-d@v1

- leitor:a16: não tipável (texto_em_falta): Os serviços sociais e outros serviços específicos estão no anexo ix, que não é mostrado.
- leitor:b: não tipável (nao_e_limiar): A passagem fixa um limiar europeu, sem estabelecer um limite de valor até ao qual um procedimento pode ser escolhido.

## regra:ccp:auto-limiar-art474-4-a@v1

- leitor:a16: {"tipo": "limiar", "condicoes": [{"field": "tipo_contrato", "op": "eq", "value": "obras"}, {"field": "tipo_entidade", "op": "eq", "value": "estado"}, {"field": "tipo_procedimento", "op": "eq", "value": "concurso_concecao"}], "params": {"threshold": {"field": "valor_estimado", "comparator": "lt", "value": 5404000, "currency": "EUR"}}}
- leitor:b: não tipável (nao_e_limiar): O montante é um limiar europeu, não um limite até ao qual um procedimento pode ser escolhido.
- verificador (A): regra 1, tipo_entidade eq estado: as fontes não nomeiam ['estado']; regra 1, tipo_procedimento eq concurso_concecao: as fontes não nomeiam ['concurso_concecao']; regra 1: field valor_estimado e as fontes nomeiam nada (L10); regra 1: comparator lt e as fontes dizem nada (L8)

## regra:ccp:auto-limiar-art474-4-b@v1

- leitor:a16: {"tipo": "limiar", "condicoes": [{"field": "setores_especiais", "op": "eq", "value": false}, {"field": "tipo_contrato", "op": "in", "value": ["bens", "servicos", "servicos_sociais"]}, {"field": "tipo_entidade", "op": "eq", "value": "estado"}, {"field": "tipo_procedimento", "op": "in", "value": ["concurso_concecao", "concurso_publico", "consulta_previa"]}], "params": {"threshold": {"field": "valor_estimado", "comparator": "lt", "value": 432000, "currency": "EUR"}}}
- leitor:b: não tipável (nao_e_limiar): A passagem fixa um limiar europeu, não um valor até ao qual um procedimento pode ser escolhido.
- verificador (A): regra 1, setores_especiais eq False: as fontes não negam o facto (L7); regra 1, tipo_contrato in ['bens', 'servicos', 'servicos_sociais']: as fontes não nomeiam ['servicos_sociais']; regra 1, tipo_entidade eq estado: as fontes não nomeiam ['estado']; regra 1, tipo_procedimento in ['concurso_concecao', 'consulta_previa', 'concurso_publico']: as fontes não nomeiam ['concurso_publico', 'consulta_previa']; regra 1: field valor_estimado e as fontes nomeiam nada (L10); regra 1: comparator lt e as fontes dizem nada (L8)

## regra:ccp:auto-limiar-art474-4-c@v1

- leitor:a16: não tipável (texto_em_falta): Os serviços sociais e outros serviços específicos estão no anexo ix, que não é mostrado.
- leitor:b: não tipável (nao_e_limiar): A passagem fixa um limiar europeu, não um limite de valor até ao qual um procedimento pode ser escolhido.

## regra:ccp:auto-prazo-minimo-art64-2@v1

- leitor:a16: {"tipo": "prazo_minimo", "condicoes": [{"field": "publicado_joue", "op": "eq", "value": true}, {"field": "tipo_procedimento", "op": "eq", "value": "concurso_publico"}, {"field": "urgencia_fundamentada", "op": "eq", "value": true}], "params": {"minimum_days": 6, "deadline_field": "prazo_propostas_dias", "counted_from": "data_envio_anuncio", "usual_days": null}} || {"tipo": "prazo_minimo", "condicoes": [{"field": "publicado_joue", "op": "eq", "value": true}, {"field": "setores_especiais", "op": "eq", "value": true}, {"field": "tipo_procedimento", "op": "eq", "value": "concurso_publico"}, {"field": "urgencia_fundamentada", "op": "eq", "value": true}], "params": {"minimum_days": 15, "deadline_field": "prazo_propostas_dias", "counted_from": "data_envio_anuncio", "usual_days": null}}
- leitor:b: não tipável (sem_vocabulario): O vocabulário não contém um campo para o período de prorrogação do prazo de apresentação das propostas.
- verificador (A): regra 1, tipo_procedimento eq concurso_publico: as fontes não nomeiam ['concurso_publico']; regra 2, tipo_procedimento eq concurso_publico: as fontes não nomeiam ['concurso_publico']

## regra:ccp:auto-prazo-minimo-art65@v1

- leitor:a16: não tipável (nao_e_prazo_minimo): O prazo é de manutenção das propostas já apresentadas, não um prazo para as apresentar.
- leitor:b: não tipável (nao_e_prazo_minimo): O prazo é para manter as propostas, não para apresentar algo.

## regra:ccp:auto-prazo-minimo-art72-3@v1

- leitor:a16: não tipável (nao_e_prazo_minimo): O prazo é um máximo de cinco dias para suprir irregularidades, não um prazo mínimo para apresentar algo.
- leitor:b: não tipável (nao_e_prazo_minimo): A passagem fixa um prazo máximo para o suprimento de irregularidades formais, e não um prazo mínimo.

## regra:ccp:auto-prazo-minimo-art78-1@v1

- leitor:a16: não tipável (nao_e_prazo_minimo): O prazo é da própria entidade adjudicante para publicar o anúncio da adjudicação, não um prazo mínimo para os interessados apresentarem algo.
- leitor:b: não tipável (nao_e_prazo_minimo): O prazo destina-se à publicação de um anúncio pela entidade adjudicante, não à apresentação de elementos pelos interessados.

## regra:ccp:auto-prazo-minimo-art78-5@v1

- leitor:a16: não tipável (sem_vocabulario): A regra só vale para contratos celebrados ao abrigo de acordo-quadro ou de sistema de aquisição dinâmico, instrumentos que o vocabulário não tem.
- leitor:b: não tipável (nao_e_prazo_minimo): O prazo destina-se à publicação do anúncio pela entidade adjudicante, não à apresentação de elementos num prazo mínimo.

## regra:ccp:auto-prazo-minimo-art85-2@v1

- leitor:a16: não tipável (nao_e_prazo_minimo): O prazo é uma prorrogação, não um prazo mínimo para apresentar os documentos.
- leitor:b: não tipável (nao_e_prazo_minimo): A passagem fixa um prazo máximo de prorrogação, não um prazo mínimo para apresentação dos documentos de habilitação.

## regra:ccp:auto-prazo-minimo-art87-a-2@v1

- leitor:a16: não tipável (nao_e_prazo_minimo): O prazo é máximo, não mínimo.
- leitor:b: não tipável (nao_e_prazo_minimo): A passagem fixa um prazo máximo de cinco dias para pronúncia, não um prazo mínimo.

## regra:ccp:auto-prazo-minimo-art90-1@v1

- leitor:a16: {"tipo": "prazo_minimo", "condicoes": [{"field": "tipo_contrato", "op": "eq", "value": "servicos_sociais"}], "params": {"minimum_days": 10, "deadline_field": "prazo_caucao_dias", "counted_from": "data_notificacao", "usual_days": null}}
- leitor:b: não tipável (nao_e_prazo_minimo): A passagem fixa um prazo máximo para prestar a caução, não um prazo mínimo.
- verificador (A): regra 1, tipo_contrato eq servicos_sociais: as fontes não nomeiam ['servicos_sociais']

## regra:ccp:auto-prazo-minimo-art93-2@v1

- leitor:a16: não tipável (nao_e_prazo_minimo): O prazo é um máximo, não um mínimo.
- leitor:b: não tipável (nao_e_prazo_minimo): A passagem fixa um prazo máximo de cinco dias, não um prazo mínimo.

