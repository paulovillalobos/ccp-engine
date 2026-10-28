# Rule readings — how the examples are written (DECISIONS D63)

AMALIA reads people's questions well and has never been taught to read a rule out of a law passage (regra_tipada had 0
training examples). These examples teach that task. They are **written law**: articles drafted for this project in the
style of the Código dos Contratos Públicos, with invented article numbers, never copied from a real article. The real
passages cannot be used: every CCP passage that states a minimum deadline or a value limit is either reserved for
measurement or a rules-factory target, and the amending decrees quote those articles word for word.

The gold readings are written here, from the text, never from another reader's answer: family A must not learn family
B's readings, or the blind check that settles a rule (D43) would compare a reader with its own copy.

## One example = one line of JSON

```json
{"id": "r01-001", "tipo": "prazo_minimo",
 "artigo": "47.º-C", "epigrafe": "Prazo mínimo para a apresentação das propostas no procedimento de negociação",
 "numeros": [{"n": "1", "texto": "1 - ..."}, {"n": "2", "texto": "2 - ..."}, {"n": "2.a", "texto": "a) ..."}],
 "alvo": "2",
 "regras": [{"passagens": ["2"], "condicoes": [...], "params": {...}}],
 "estilo": "dois_casos"}
```

- `artigo` is an invented number (`47.º-C`, `312.º`); `epigrafe` is its heading. `numeros` are its numbers and alíneas
  in order, each `texto` starting exactly as the CCP writes them: `1 - `, `a) `, `i) `. `n` is the path: `1`, `2`, `2.a`,
  `2.a.i`. An article with a single paragraph has `numeros: []` and its text in `texto` (no «1 - »); then `alvo` is `""`
  (the article itself).
- `alvo` is the passage the question asks about. `regras[].passagens` are paths from `numeros` (or `""` for the
  article); they must include `alvo`, and add another number only when the rule cannot be read without it (a number that
  says «o prazo previsto no número anterior» cites both).
- `tipo` is `prazo_minimo` or `limiar`. `estilo` is a short tag of what the example practises.

## The rule, field by field

`condicoes`: a list of `{"field", "op", "value"}`. Fields and values (no others):

- `tipo_contrato`: obras, bens, servicos, concessao_obras, concessao_servicos, servicos_sociais
- `tipo_procedimento`: ajuste_direto, consulta_previa, concurso_publico, concurso_limitado_previa_qualificacao,
  procedimento_negociacao, dialogo_concorrencial, parceria_inovacao, concurso_concecao, concurso_ideias
- `modalidade_concecao`: publico, limitado, simplificado
- `territorio`: PT, PT-AC, PT-MA; `tipo_entidade`: estado, outra
- `publicado_joue`, `urgencia_fundamentada`, `setores_especiais`, `anuncio_pre_informacao`: true / false
- `preco_base` (number, euros), `data_inicio_procedimento` (ISO date)
- `op`: eq, ne for single values; in, not_in with a list; lt, le, gt, ge for numbers and dates.

`params` for `prazo_minimo`: `minimum_days` (integer), `deadline_field`, `counted_from`, and `usual_days` (integer or
null). For `limiar`: `threshold` = `{"field": "preco_base", "comparator": "lt" | "le", "value": <euros>, "currency": "EUR"}`.

Deadline fields (`deadline_field`), by what the passage says the deadline is for:

| field | the passage's words |
|---|---|
| prazo_propostas_dias | apresentação das propostas |
| prazo_candidaturas_dias | apresentação das candidaturas |
| prazo_trabalhos_concecao_dias | apresentação dos documentos que materializam os trabalhos de conceção |
| prazo_solucoes_dias | apresentação das soluções |
| prazo_esclarecimentos_dias | pedidos de esclarecimentos |
| prazo_pronuncia_dias | pronúncia dos interessados (audiência prévia) |
| prazo_reclamacao_dias | reclamação |
| prazo_caucao_dias | prestação da caução |
| prazo_habilitacao_dias | apresentação dos documentos de habilitação |

Starting points (`counted_from`):

| value | the passage's words |
|---|---|
| data_envio_anuncio | a contar da data do envio do anúncio (ao Serviço das Publicações da União Europeia, ou para publicação) |
| data_publicacao_anuncio | a contar da data de publicação do anúncio |
| data_envio_convite | a contar da data do envio do convite |
| data_notificacao | a contar da data da notificação |
| data_disponibilizacao_pecas | a contar da data da disponibilização das peças do procedimento |
| nao_indicado | the passage, read with the number it refers to, does not say when the count starts |

## Conventions (the ones the settled rules follow)

1. **The procedure goes in when the passage or its article names it.** A heading «… no concurso limitado por prévia
   qualificação» or a number «Quando o anúncio do concurso público …» gives `tipo_procedimento eq …`. A number that
   names two procedures gives `in [a, b]`.
2. **JOUE goes in when the passage states it.** «seja publicado no Jornal Oficial da União Europeia» → `publicado_joue eq
   true`; «não seja publicado …» → `eq false`. Not stated → no condition.
3. **One rule per case.** «inferior a 6 dias ou, no caso de empreitada de obras públicas, inferior a 14 dias» is two rules:
   `tipo_contrato ne obras` with 6 and `tipo_contrato eq obras` with 14. «30 dias nos concursos público e limitado e 15
   dias no concurso simplificado» is two rules with `modalidade_concecao in [limitado, publico]` and `eq simplificado`.
   A passage with one deadline is **one** rule. Never repeat a rule; never add a rule another number states.
4. **A number that changes another number's deadline** («O prazo mínimo previsto no n.º 1 pode ser reduzido para 10 dias
   nos casos de urgência devidamente fundamentada») is one rule: the referred number's conditions, deadline field and
   starting point, plus the new condition (`urgencia_fundamentada eq true`) and the new days; `passagens` = [the number
   referred to, the alvo].
5. **«Em regra» beside an absolute minimum** («é, em regra, de 30 dias …, não podendo em caso algum ser inferior a 15
   dias»): `minimum_days` = the absolute minimum (15), `usual_days` = the «em regra» days (30). Otherwise `usual_days`
   is null.
6. **Value limits** read as the passage writes them: «inferior a 75 000 €» → `lt 75000`; «igual ou inferior a» → `le`.
   The procedure or contract type the passage ties the limit to are conditions. Only write `limiar` examples a `lt` or
   `le` threshold can hold.
7. Write only what the text says. A condition the passage does not state is not added; a fact the vocabulary has no
   value for means the example is not written.

## Style

European Portuguese as the CCP writes it today (conceção, receção, ação; «entidade adjudicante», «peças do
procedimento», «não pode ser fixado um prazo … inferior a»), numbers in figures («30 dias», «75 000 €») and sometimes in
words («cinco dias»). Articles of 1 to 6 numbers; the other numbers say related things (who publishes, what the convite
contains, other deadlines) so the reader has to find the alvo's rule among them. Vary the procedures, contract types,
deadlines, starting points and wording; do not reuse a sentence from one example to the next.
