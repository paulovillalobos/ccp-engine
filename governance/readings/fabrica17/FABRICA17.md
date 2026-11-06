# FÁBRICA DE REGRAS — ronda 17 (DECISIONS D83)

Gerado por tools/rule_factory.py (ccp-rule-factory-0.10) com o protocolo de leitura v3 (tools/read_rules_v3.py, ccp-read-rules-v3-0.6). D75: a atualização diária — as passagens cujo texto mudou ou entrou no depósito desde a última, que dizem dias ou euros. Propõe leitor:a19 (AMALIA + adaptador v7), leitor:b revê às cegas.

Protocolo 0.5. Um programa confirma cada palavra citada; o «não tipável» com o mesmo motivo também assenta.

| grupo | alvos | leitor A válido | leitor B válido | assentes | regras | «não tipável» |
|---|---|---|---|---|---|---|
| contagem | 5 | 3 | 5 | 3 | 3 | 0 |
| todos | 5 | 3 | 5 | 3 | 3 | 0 |

| regra | passagem | estado | replica | verificador: leitor A | verificador: leitor B |
|---|---|---|---|---|---|
| regra:cpa:auto-contagem-prazo-art87-b@v1 | cpa:art87.b | settled | sim | ok | ok |
| regra:cpa:auto-contagem-prazo-art87-c@v1 | cpa:art87.c | settled | sim | ok | ok |
| regra:cpa:auto-contagem-prazo-art87-f@v1 | cpa:art87.f | settled | sim | ok | ok |
| regra:ccp:auto-contagem-prazo-art470-2@v1 | ccp:art470.2 | sem leitura válida de leitor:a19 | — | regra 1: as fontes de aspecto não dizem fins_de_semana continuo (palavras da lei no vocabulário) | ok |
| regra:ccp:auto-contagem-prazo-art470-3@v1 | ccp:art470.3 | sem leitura válida de leitor:a19 | — | regra 1, tipo_procedimento eq concurso_publico_urgente: as fontes não nomeiam ['concurso_publico_urgente'] | ok |

## regra:cpa:auto-contagem-prazo-art87-b@v1

- leitor:a19: {"tipo": "contagem_prazo", "condicoes": [], "params": {"valor": "nao_conta", "aspecto": "primeiro_dia", "deadline_field": "todos"}}
- leitor:b: {"tipo": "contagem_prazo", "condicoes": [], "params": {"valor": "nao_conta", "aspecto": "primeiro_dia", "deadline_field": "todos"}}

## regra:cpa:auto-contagem-prazo-art87-c@v1

- leitor:a19: {"tipo": "contagem_prazo", "condicoes": [], "params": {"valor": "suspende", "aspecto": "fins_de_semana", "deadline_field": "todos"}}
- leitor:b: {"tipo": "contagem_prazo", "condicoes": [], "params": {"valor": "suspende", "aspecto": "fins_de_semana", "deadline_field": "todos"}}

## regra:cpa:auto-contagem-prazo-art87-f@v1

- leitor:a19: {"tipo": "contagem_prazo", "condicoes": [], "params": {"valor": "transfere", "aspecto": "termo", "deadline_field": "todos"}}
- leitor:b: {"tipo": "contagem_prazo", "condicoes": [], "params": {"valor": "transfere", "aspecto": "termo", "deadline_field": "todos"}}

## regra:ccp:auto-contagem-prazo-art470-2@v1

- leitor:a19: {"tipo": "contagem_prazo", "condicoes": [{"field": "tipo_procedimento", "op": "eq", "value": "concurso_publico_urgente"}], "params": {"valor": "continuo", "aspecto": "fins_de_semana", "deadline_field": "prazo_propostas_dias"}}
- leitor:b: {"tipo": "contagem_prazo", "condicoes": [{"field": "tipo_procedimento", "op": "eq", "value": "concurso_publico_urgente"}], "params": {"valor": "conta", "aspecto": "primeiro_dia", "deadline_field": "prazo_propostas_dias"}}
- verificador (A): regra 1: as fontes de aspecto não dizem fins_de_semana continuo (palavras da lei no vocabulário)

## regra:ccp:auto-contagem-prazo-art470-3@v1

- leitor:a19: {"tipo": "contagem_prazo", "condicoes": [{"field": "tipo_procedimento", "op": "eq", "value": "concurso_publico_urgente"}], "params": {"valor": "continuo", "aspecto": "fins_de_semana", "deadline_field": "prazo_propostas_dias"}}
- leitor:b: {"tipo": "contagem_prazo", "condicoes": [], "params": {"valor": "continuo", "aspecto": "fins_de_semana", "deadline_field": "prazo_propostas_dias"}} || {"tipo": "contagem_prazo", "condicoes": [], "params": {"valor": "continuo", "aspecto": "fins_de_semana", "deadline_field": "prazo_candidaturas_dias"}} || {"tipo": "contagem_prazo", "condicoes": [], "params": {"valor": "continuo", "aspecto": "fins_de_semana", "deadline_field": "prazo_solucoes_dias"}}
- verificador (A): regra 1, tipo_procedimento eq concurso_publico_urgente: as fontes não nomeiam ['concurso_publico_urgente']

