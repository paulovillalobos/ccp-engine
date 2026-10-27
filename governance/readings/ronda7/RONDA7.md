# RONDA 7 — B3, as quatro regras que o motor precisa primeiro (DECISIONS D51)

Gerado por tools/read_rules.py. Só o seletor muda (D51): a pergunta lista os regimes que o sistema tem, mostra os art. 19.º c), d) e 20.º n.º 1 c), d) do Código com o texto anterior, e admite «from» = null; as outras perguntas são as da ronda 6. Propõe leitor:a5 (AMALIA + adaptador v4), leitor:b revê às cegas. Só fica settled a leitura que leitor:b replica em forma canónica (D43).

| regra | estado | exato | direção |
|---|---|---|---|
| regra:dl-177-2026:seletor-regime@v1 | proposed | não | não |

## regra:dl-177-2026:seletor-regime@v1

- leitor:a5: passagens ccp:art19.c, ccp:art19.d, ccp:art20.1.c, ccp:art20.1.d; condições []; params {"selects_by": "data_inicio_procedimento", "regimes": [{"from": "2018-01-01", "to": "2026-09-30", "law_version": "lei:ccp@2026-09-30", "package": "pacote:ccp@2026-09-30"}, {"from": "2026-10-01", "to": null, "law_version": "lei:ccp@2026-10-01", "package": "pacote:ccp@2026-10-01"}]}
- leitor:b: passagens dl-177-2026:art10, dl-177-2026:art11, dl-177-2026:art7.2; condições []; params {"selects_by": "data_inicio_procedimento", "regimes": [{"from": null, "to": "2026-09-30", "law_version": "lei:ccp@2026-09-30", "package": "pacote:ccp@2026-09-30"}, {"from": "2026-10-01", "to": null, "law_version": "lei:ccp@2026-10-01", "package": "pacote:ccp@2026-10-01"}]}

