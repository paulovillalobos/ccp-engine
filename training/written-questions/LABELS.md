# How a question is labelled (D52)

Each line of `batch-NN.jsonl` is one question written one by one (not from a template), as people write to a CCDR, a
platform help desk or a colleague: typos, missing accents, old spelling, shorthand, dictation, wrong citations, loose
amounts. The label says only what the question states; the engine applies the law and code writes the answer.

    {"id", "hoje", "pergunta", "factos": {...}, "ambiguos": {campo: [candidatos]}, "contraditorios": {campo: [v1, v2]},
     "citacoes": ["ccp:art22", ...], "fenomenos": [...]}

`factos` — the engine's fields, only when stated or mapped by everyday words:
- tipo_entidade: câmara, município, junta, união de freguesias, "a autarquia" -> outra; ministério, direção-geral,
  secretaria-geral -> estado. Instituto, universidade, escola, hospital, empresa municipal, Governo Regional, "somos do
  Estado" -> ambiguos [estado, outra]. The asker's own IPSS, associação, misericórdia, bombeiros voluntários, private fundação
  or cooperativa -> ambiguos ["outra"] (it may not be an entidade adjudicante at all); such a body named only as supplier or
  beneficiary gives no entity.
- tipo_procedimento: the procedure's name or a common short form: CP = concurso público, AD = ajuste direto, CLPQ, CPrév or
  «consulta» = consulta prévia (when the text itself says what CP stands for, the text decides). Bare "concurso",
  "requisição", "AD com três orçamentos", "concurso internacional" -> ambiguos with the candidates.
- tipo_contrato: named, or implied by an object whose type is not in doubt (construir, reparar, pavimentar -> obras;
  comprar, adquirir, fornecimento de coisas -> bens; limpeza, vigilância, consultoria, manutenção, transporte ->
  servicos). Máquina com operador, software, refeições, projeto, mão-de-obra -> ambiguos.
- territorio: a place found in only one region; "Açores", "Madeira", an island. Lagoa, Calheta, Santa Cruz without the
  region -> ambiguos.
- publicado_joue: "vai ao JOUE / jornal oficial europeu / publicidade internacional" -> true ("concurso internacional"
  too); "só no DR / sem JOUE" -> false. Bare "anúncio" -> nothing.
- preco_base: only with the words "preço base" (also "PB", "anda nos" with preço base). The amount under "valor",
  "valor estimado", "orçamento", "cabimento", a range, a per-item value, an amount "com IVA", a malformed number ->
  ambiguos.preco_base [the number as written, never converted].
- data_inicio_procedimento: "o procedimento começa/inicia", "decisão de contratar a…", or a hypothetical start ("se
  tiver começado a…"), resolved against `hoje`. Launch or notice verbs ("lançámos", "o concurso abre", "o anúncio sai")
  -> ambiguos.data_inicio_procedimento [the date] (art. 36.º n.º 1: the procedure starts with the decisão de contratar;
  the question names another event). Year alone, law names, contract or adjudicação dates -> nothing.

Not a fact: what the user says they do not know ("não sabemos se é CP ou AD"); claims about the law ("o limite do AD
é 20 mil", "o colega diz que não vai ao JOUE", "por ser urgente"); distractor numbers and dates (quantities, durations,
law numbers, article numbers).

`contraditorios` — the question states two values for one field ("PB 60 mil… afinal 80 mil").
`citacoes` — every article or act the user cites, as store ids, whether right, revoked or wrong: "art. 22.º do CCP" ->
ccp:art22, "art. 20.º n.º 1 d)" -> ccp:art20.1.d, "DL 177/2026" -> dl-177-2026, "o código antigo" -> nothing.
The engine compares them with the store (revoked, changed, not the governing article) and says so in the answer.
`fenomenos` — tags for measurement: typo, sem_acentos, pre_ao, pt_br, ditado, abreviaturas, telegrafico, carta,
multi, seguimento, premissa, citacao_errada, limiar_antigo, iva, intervalo, por_item, contradicao, nao_sabe, distrator,
lugar_ambiguo, entidade_ambigua, objeto_ambiguo, concurso_nu, lancamento, sem_factos.
