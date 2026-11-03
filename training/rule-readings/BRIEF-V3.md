# Brief: 100 written articles in the v3 shape, with gold readings (ccp-engine, DECISIONS D66)

You are writing examples for a reader that turns a Portuguese public-procurement law passage into a typed rule, under
the reading protocol v3. The repository is ~/ccp-engine. Use `.venv/bin/python` for Python.

## Read first
- `tools/read_rules_v3.py`: the constant `STATIC`, which holds the reading rules L1–L14, what a rule means to the engine,
  and the answer format. Your gold follows these rules exactly; another reader will be held to the same rules.
- `schemas/vocabulario-v3.json`: the only fields and values, and the law's words for each. A condition is only valid when
  an allowed source says it in words the file lists (or with the same words in another order the checker accepts).
- `training/rule-readings/GUIDE.md`, for the JSON shape of an article. Below is what v3 adds to it.

## Do NOT read
`training/rule-readings/eval*.jsonl`, `law/`, `governance/readings/`, `training/data*`, `reports/`. Write the gold yourself from your own
text, never from a model's or another reader's answer.

## One article = one line of JSON (the GUIDE's shape, plus three optional fields)
```json
{"id": "v3-01-001", "tipo": "prazo_minimo",
 "lugar": ["Capítulo III — Concurso limitado por prévia qualificação", "Secção II — Fase da apresentação das candidaturas"],
 "artigo": "612.º", "epigrafe": "Prazo para a apresentação das candidaturas",
 "numeros": [{"n": "1", "texto": "1 - ..."}, {"n": "2", "texto": "2 - ..."}],
 "alvo": "2",
 "remissoes": [{"artigo": "640.º", "epigrafe": "Anúncio", "numeros": [{"n": "3", "texto": "3 - ..."}]}],
 "regras": [{"condicoes": [{"field": "tipo_procedimento", "op": "eq", "value": "concurso_limitado_previa_qualificacao"}],
             "params": {"minimum_days": 20, "deadline_field": "prazo_candidaturas_dias", "counted_from": "data_envio_anuncio", "usual_days": null}}],
 "estilo": "capitulo"}
```
- `lugar`: the titles above the article, outermost first, written as the CCP writes them («Capítulo II — Concurso
  público», «Secção VII — Concurso público urgente», «Capítulo IV — Serviços sociais e outros serviços específicos»).
- `remissoes`: the passages of OTHER invented articles that your target refers to by number («o prazo previsto no n.º 3 do
  artigo 640.º», «inferior aos limiares referidos nas alíneas b) ou c) do n.º 3 do artigo 650.º»). Give each referred
  article's number, heading and the referred numbers (and alíneas: `"n": "3.b"`). Write the reference in the target's text
  exactly in the CCP's form: «n.º 3 do artigo 640.º», «alínea b) do n.º 3 do artigo 650.º», «n.ºs 2 e 3 do artigo 641.º».
  For «contratos distintos dos previstos nos artigos 610.º e 611.º», give those two articles with their headings only:
  `{"artigo": "610.º", "epigrafe": "Escolha do procedimento de formação de contratos de empreitada de obras públicas", "numeros": []}`.
- `regras`: the gold, WITHOUT quotes or passages. Code finds the quoting words in your text, and the factory's checker must
  accept the result. One rule per case (L5). Conditions in canonical form: one value → eq/ne, several → in/not_in;
  tipo_entidade always eq; prazo params always have `usual_days` (null unless L11).
- For a passage that holds no rule of the article's `tipo`: `"regras": []` and
  `"nao_tipavel": {"motivo": "nao_e_limiar | nao_e_prazo_minimo | sem_vocabulario | texto_em_falta", "fonte": "<exact words of the target or its proémio that show it>", "falta": "<one sentence>"}`.
- A limiar is always the value up to which a procedure may be chosen, and that procedure is a condition. Use `valor_estimado`,
  `preco_base` or `preco_contratual` as the threshold field, whichever your text names next to the value.

## The kinds (estilo) and the mix for 100 articles
- `capitulo` 15: the procedure (or contract type, or design-contest modality) is named ONLY by a `lugar` title. Also a title
  naming two procedures («Capítulo I — Consulta prévia e ajuste direto» → in [both]), and a heading naming one procedure
  inside a chapter naming another (the nearer one decides, L3).
- `remissao` 15: the target refers to a number of another article given in `remissoes`. Either it changes that number's
  deadline or limit (the rule carries every condition of the referred number, L4), or it takes its value from it («inferior
  aos limiares referidos nas alíneas b) ou c) …, consoante o caso»: one rule per referred value, each with the referred
  alínea's conditions, L10).
- `alineas` 10: a number whose opening words («2 - Para a celebração de contratos de locação ou aquisição de bens móveis,
  pode adotar-se:») are completed by alíneas ("2.a", "2.b", …), the target being one alínea: its conditions come from the
  opening words too (the proémio, L1).
- `nao_tipavel` 20, five per reason:
  nao_e_limiar (a value that waives an obligation: «pode não ser exigida caução», «ficam dispensados de redução a
  escrito»; reserves a contract; excludes an invitee; sums contracts), nao_e_prazo_minimo («não pode ser superior a N
  dias»; a deadline of the contracting authority itself: «a entidade adjudicante decide no prazo de 10 dias»),
  sem_vocabulario (a `lugar` of an instrument: «Capítulo II — Sistemas de aquisição dinâmicos», «Capítulo III — Sistemas
  de qualificação»; a deadline in horas, dias úteis or meses; a procedure outside the list), texto_em_falta (the target
  refers to a number of another article that is NOT given in `remissoes`, and the rule cannot be read without it).
- `comparador` 8: limits with «superior a» / «igual ou superior a» (a procedure only from a value up: gt / ge), «não
  exceda», «até X €, inclusive» (le), «até X €, exclusive» (lt).
- `valor_condicao` 8: a deadline that changes with the contract's value («quando o preço base seja igual ou superior a
  1 000 000 €, 20 dias»): the amount is a condition (preco_base / valor_estimado / preco_contratual, with lt/le/gt/ge).
- `casos` 8: cases of one passage that complete each other with a fact («30 dias, ou 15 dias se a urgência for
  fundamentada» → urgencia false / true; «consoante o anúncio seja ou não publicado no Jornal Oficial da União Europeia»
  → publicado_joue true / false; «nos restantes casos» → not_in).
- `contagem` 8: starting points by anaphora («contados do seu envio» after «convite», «a contar do envio deste», «a contar
  da sua publicação» after «anúncio») and reductions by N days («podem ser reduzidos em até sete dias»: the referred
  number's days less 7, L4).
- `grandeza` 8: limits whose amount is named «valor estimado do contrato», «preço base» or «preço contratual» (the field
  follows the words).
About half prazo_minimo and half limiar overall. Vary procedures, contract types, numbers, wording, and the number of
numbers per article (2 to 6); the other numbers say related things so the reader must find the target's rule among them.

## Output
- File `training/rule-readings/{FILE}.jsonl`, ids `{PREFIX}-001` … `{PREFIX}-100`, invented article numbers in {RANGE}
  (remissões too), each article number used once.
- European Portuguese as the CCP writes it today; never copy or closely paraphrase a real CCP article (a code check drops an
  article whose target passage is close to a real one or to a measured article).

## Check, then fix until clean
Run `.venv/bin/python tools/make_rule_readings_v12.py check --only {PREFIX}` (about a minute and a half). Every line it
prints for your ids is a problem: the gold has no words in your text for something it says («gold: …»), or the factory's
checker refuses the reading code built from your gold («checker: …»), or the article is too close to another text. Fix the
text or the gold (never the code) and run again until no line names your ids. Then read your 100 gold readings once more
against your texts and fix any you would not defend.

Finish with one line: the file path and how many of your articles pass.
