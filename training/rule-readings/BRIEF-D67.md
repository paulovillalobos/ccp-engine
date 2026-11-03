# Brief: 100 more written articles in the v3 shape, for AMALIA v13 (ccp-engine, DECISIONS D67)

Read `training/rule-readings/BRIEF-V3.md` first: everything in it holds (what to read, what NOT to read, the JSON shape,
the kinds, the gold without quotes, European Portuguese as the CCP writes it, no copying of a real article). This file
changes six things. Where the two differ, this file wins.

Why: v12 was trained on 1 318 articles, and 73 % of them were written for the old reading prompt. Against the articles it
was measured on, it almost never says «não tipável», it copies the vocabulary's first phrase instead of the text's words,
and it cites the target passage when the words are in a title, the proémio or a referred number. These articles teach the
three things it does not know.

## 1. Output
`training/rule-readings/{FILE}.jsonl`, ids `{PREFIX}-001` … `{PREFIX}-100`, invented article numbers in {RANGE} (remissões
too), each article number used once. Do not read the other `v4-*.jsonl` files.

## 2. The mix of your 100 (replaces BRIEF-V3's)
| kind (`estilo`) | articles | what it practises (BRIEF-V3 describes each) |
|---|---|---|
| `nao_tipavel` | 40 | 10 per reason; section 6 below |
| `contagem` | 9 | starting points by anaphora; reductions by N days |
| `grandeza` | 8 | the amount's field follows the words (valor estimado / preço base / preço contratual) |
| `valor_condicao` | 8 | a deadline that changes with the contract's value |
| `casos` | 8 | cases of one passage that complete each other |
| `comparador` | 8 | **lt and le only** in this batch: «não exceda», «até X €, inclusive», «inferior a», «até X €, exclusive». No «superior a» / «igual ou superior a»: that waits for a product rule |
| `alineas` | 7 | the target is an alínea; its conditions come from the proémio too |
| `remissao` | 6 | the target refers to a number of another article given in `remissoes` |
| `capitulo` | 6 | the procedure (or contract type) is named only by a title |

About half `prazo_minimo` and half `limiar` (a «não tipável» article counts by its `tipo`).

## 3. Every article sits under titles
Every article has `lugar`: two or three titles, outermost first («Título II — …», «Capítulo III — …», «Secção I — …»).
Outside the `capitulo` kind, at least half of your titles name nothing in the vocabulary («Título II — Fase de formação do
contrato», «Capítulo IV — Disposições comuns»); the others may name a procedure or contract type that agrees with the text.
An article without `lugar` is left out by the check.

## 4. The law's words, not the vocabulary's first phrase
The reader's prompt shows only the first phrase or two of each value; the reader has to quote your text. So where
`schemas/vocabulario-v3.json` lists several phrases for a value, use the first one in at most one article in three: rotate
the others, inflected as the CCP writes them («de locação ou de aquisição de bens móveis», «de aquisição de serviços»,
«empreitadas de obras públicas»). Lists go in the order the sentence wants, not the vocabulary's: «a consulta prévia e o
ajuste direto», «ajuste direto ou consulta prévia». The check prints your share of first phrases; keep it at or under 40 %.

## 5. Where the words are
In about half of your typable articles, at least one condition or parameter is said outside the target passage: in the
proémio, the epígrafe, a title, or the referred number. Each article has 2 to 6 numbers, and the other numbers say related
things with other values (another procedure, another deadline, another amount), so a reader that quotes a neighbour fails
(L1).

## 6. «Não tipável», 10 per reason
Write each so that one changed detail would make it typable, and say in `falta`, in one sentence, what is missing:
- `nao_e_limiar`: a value that waives an obligation («pode não ser exigida caução quando o preço contratual seja inferior
  a …», «ficam dispensados de redução a escrito os contratos de valor inferior a …»); a value that reserves a contract,
  excludes an invitee («não podem ser convidadas entidades que, no ano em curso, já tenham celebrado contratos cujo preço
  contratual acumulado seja igual ou superior a …»), or sums contracts.
- `nao_e_prazo_minimo`: a maximum («não pode ser superior a 30 dias», «no prazo máximo de»); a deadline of the contracting
  authority or of the jury («a entidade adjudicante decide no prazo de 10 dias», «o júri elabora o relatório preliminar no
  prazo de …»); a period that is not for presenting anything (a contract's term, how long a guarantee lasts).
- `sem_vocabulario`: a deadline in horas, dias úteis or meses; a procedure or instrument outside the list, named by a title
  («Capítulo II — Sistemas de aquisição dinâmicos», «Capítulo III — Sistemas de qualificação»); a fact no field holds (the
  number of entities invited, the share of the price paid in advance).
- `texto_em_falta`: the target refers to a number of another article that is NOT given in `remissoes`, and its rule cannot
  be read without it («o prazo previsto no n.º 2 do artigo N.º», N an unused number of your range, with no remissão given).
The `fonte` is the exact words of the target or its proémio that show it.

## Check, then fix until clean
Run `.venv/bin/python tools/make_rule_readings_v13.py check --only {PREFIX}` (under a minute). It prints every problem
(«gold: …», «checker: …», «close to …», «no lugar»), then your mix against section 2, your «não tipável» by reason, and your
share of first phrases. Fix the text or the gold (never the code) until no problem line names your ids, the kinds match
section 2, each reason has 10, and the share is at or under 40 %. Then read your 100 gold readings once more against your
texts and fix any you would not defend.

Finish with one line: the file path, how many of your articles pass, and your share of first phrases.
