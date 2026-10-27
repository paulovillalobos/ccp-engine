# Misconceptions and false premises in questions about Portuguese public procurement (CCP), and how a fact-extraction step should treat them

Scope note: Portugal, current as of 2026-10-27. Two kinds of source are used. (1) Web sources (law-firm notes, press, EU/ACL papers), cited by URL. (2) The project's own capture of the Diário da República (DR) text, versioned by date, in `~/ccp-engine/law/passagem/` (each JSON file holds the article text per `valid_from`/`valid_to`, captured from the DR consolidated CCP at https://diariodarepublica.pt/dr/legislacao-consolidada/decreto-lei/2008-34455475 and DL 177/2026 at https://diariodarepublica.pt/dr/detalhe/decreto-lei/177-2026-1166969779). Where these are cited they are cited as "[DR capture: file]". No threshold below is stated from memory.

## 1. Which misconceptions do people commonly bring to CCP questions, and what is the legal baseline that makes them wrong?

### Takeaway
The recurring error classes are: (a) procedure names used loosely (bare "concurso"; ajuste direto vs consulta prévia); (b) thresholds out of date, made much worse by the 1 Oct 2026 reform (DL 177/2026), which raised the national thresholds several-fold, revoked art. 22.º and replaced "valor do contrato" with "valor estimado do contrato"; (c) the value terms valor / valor estimado / preço base / preço contratual / orçamento / cabimento used as synonyms, plus IVA included or not; (d) splitting contracts (fracionamento); (e) entity types (câmara vs município vs freguesia vs empresa municipal vs instituto vs "Estado" in the narrow art. 474.º sense); (f) DR vs JOUE publication; (g) the date that decides the applicable regime (decisão de contratar, not anúncio or contrato). Most of these become *false premises about the law* once a user states them as rules; only some are *facts* the extraction step should capture.

### Cited Findings

**A. The 2026 reform (the main source of outdated-threshold premises)**
- DL 177/2026 was published in DR on 4 Sep 2026 and enters into force on 1 Oct 2026; it applies to procedures started after that date, with modificação objetiva and dispute resolution applying also to procedures in progress and contracts in execution. — [CMS](https://cms.law/pt/prt/news-information/alteracao-ao-codigo-dos-contratos-publicos); [ECO, 12 perguntas](https://eco.sapo.pt/descodificador/12-perguntas-e-respostas-para-perceber-as-novas-regras-da-contratacao-publica/)
- The transitional norm reads: the changes apply to procedures "iniciados após a data da sua entrada em vigor" (art. 10.º, n.º 1), with n.º 2 extending modificação objetiva and resolução alternativa de litígios to pending procedures and contracts. — [DR capture: dl-177-2026-art10.r1.json]; DR: https://diariodarepublica.pt/dr/detalhe/decreto-lei/177-2026-1166969779
- Art. 7.º, n.º 2 of DL 177/2026 states the updated values in arts. 19.º c)/d) and 20.º, n.º 1 c)/d) apply to procedures started after entry into force, and the art. 113.º, n.º 2 invitee limit is computed on contracts of the current and two previous economic years. — [DR capture: dl-177-2026-art7.2.r1.json]
- Threshold change table (old → new), per CMS: obras ajuste direto 30.000 € → 150.000 €; obras consulta prévia 150.000 € → 1.000.000 €; bens/serviços ajuste direto 20.000 € → 75.000 €; bens/serviços consulta prévia 75.000 € → 130.000 €; concessões < 1 ano 75.000 € → 1.000.000 €; "outros contratos" 50.000 € → 75.000 € (AD) and 100.000 € → 130.000 € (CP). — [CMS](https://cms.law/pt/prt/news-information/alteracao-ao-codigo-dos-contratos-publicos); the same four main figures in [ECO](https://eco.sapo.pt/descodificador/12-perguntas-e-respostas-para-perceber-as-novas-regras-da-contratacao-publica/)
- Primary text confirms the dates of these values: art. 19.º d) "Ajuste direto, quando o valor do contrato for inferior a (euro) 30 000" valid 2018-01-01 to 2026-10-01, replaced from 2026-10-01 by "valor estimado do contrato for inferior a 150 000 €"; art. 19.º c) consulta prévia < 150 000 (2018-01-01 to 2026-10-01, "com convite a pelo menos três entidades") → < 1 000 000 € (from 2026-10-01); art. 20.º, n.º 1 d) < 20 000 → < 75 000 €; art. 20.º, n.º 1 c) < 75 000 → < 130 000 €. — [DR capture: ccp-art19.c.r2.json, ccp-art19.d.r2.json, ccp-art20.1.c.r2.json, ccp-art20.1.d.r2.json]
- So there are at least three dated threshold regimes a user may carry in their head: pre-2018 (the 2008 text, where consulta prévia did not exist as a separate procedure in arts. 19/20 — the 2018-01-01 versions are the first with "Consulta prévia"), 2018-01-01 to 2026-09-30 (20k/30k AD, 75k/150k CP, DL 111-B/2017), and from 2026-10-01 (75k/150k AD, 130k/1M CP). — [DR capture: ccp-art19.*.r2.json, ccp-art20.1.*.r2.json]
- 2021 layer: Lei 30/2021 created EU-funds special measures, including a "consulta prévia simplificada" allowed below the art. 474.º thresholds and below 750.000 €, with at least five invitees. — [Diário da República, Lei 30/2021](https://diariodarepublica.pt/dre/detalhe/lei/30-2021-163728569); later amended by Lei 43/2024 per [Ecija](https://www.ecija.com/adcecija/alteracao-regime-juridico-medidas-especiais-contratacao-publica/). DL 177/2026 art. 7.º, n.º 3 now counts prior Lei 30/2021 simplified consultations toward the new art. 127.º-C limits. — [DR capture: dl-177-2026-art7.3.r1.json]
- An APCMC circular mentions a new "consulta prévia especial" up to 2.000.000 € for strategic areas; not confirmed in other sources found. — [APCMC circular 70/2026](https://apcmc.pt/wp-content/uploads/circular-70-2026.pdf) (via search snippet; unverified)
- Press simplification that itself seeds a false premise: a headline says "ajustes diretos podem chegar aos 150 mil euros" — [Postal.pt](https://postal.pt/nacional/nova-lei-da-contratacao-publica-entra-em-vigor-ajustes-diretos-podem-chegar-aos-150-mil-euros/). True only for obras; for bens/serviços the AD ceiling is < 75.000 € (art. 20.º, n.º 1 d)). — [DR capture: ccp-art20.1.d.r2.json]
- ECO explicitly corrects three reform misconceptions: higher thresholds do not let an already-launched procedure be simplified; discretion is not unlimited; artificial splitting stays prohibited. — [ECO](https://eco.sapo.pt/descodificador/12-perguntas-e-respostas-para-perceber-as-novas-regras-da-contratacao-publica/)

**B. EU (JOUE) thresholds — and a conflict between sources**
- Delegated Regulations (EU) 2025/2150, 2025/2151, 2025/2152 were published in the OJ on 23 Oct 2025 and apply from 1 Jan 2026 to end-2027; Cuatrecasas gives 5.404.000 € (works), 140.000 € (bens/serviços, Estado = art. 474.º, n.º 3 b)), 216.000 € (other entities), 750.000 € (social services). — [Cuatrecasas](https://www.cuatrecasas.com/pt/portugal/publico-1/art/novos-limiares-ue-contratacao-publica-2026-2027-1); CMS describes a downward revision vs 2024–2025 — [CMS](https://cms.law/pt/prt/news-information/novos-limiares-de-contratacao-publica)
- Conflict: the CCP text republished by DL 177/2026 (in force from 2026-10-01) still reads art. 474.º, n.º 3 b) "139 000 €" for Estado and n.º 1 still cites Delegated Regulations 2019/1827–1829; n.º 3 a) 5 404 000 € and c) 216 000 € match Cuatrecasas. — [DR capture: ccp-art474.r2.json, ccp-art474.3.b.r2.json]. A Fieldfisher summary (search snippet) also gives 139.000 €. — [Fieldfisher](https://www.fieldfisher.com/pt-pt/locations/portugal/insights/que-procedimento-posso-escolher-a-partir-de-1-de-outubro). Art. 474.º, n.º 5 says a Commission delegated act revising thresholds "determina a modificação do presente artigo". — [DR capture: ccp-art474.r2.json]. Not resolved here: which figure (139k vs 140k) the engine should use for Estado bens/serviços is a law-reading decision for the engine, not the extractor.
- Art. 474.º, n.º 3 distinguishes "adjudicados pelo Estado" (b) from "outras entidades adjudicantes" (c); history of b): 135 000 (2018-01-01 to 2021-06-20), 139 000 (from 2021-06-20). — [DR capture: ccp-art474.3.b.r2.json]
- Since 2026-10-01, arts. 19.º a)/b) and 20.º, n.º 1 a)/b): concurso público / limitado with JOUE announcement "qualquer que seja o valor estimado"; without JOUE only when below the art. 474.º thresholds. — [DR capture: ccp-art19.r2.json, ccp-art20.r2.json]. So "concurso" ≠ "concurso internacional/JOUE", and an anúncio in the DR alone is a distinct fact from JOUE publication.

**C. Value terms (valor / valor estimado / preço base / IVA)**
- DL 177/2026 replaces "valor do contrato" ("valor máximo do benefício económico que pode ser obtido pelo adjudicatário") with "valor estimado do contrato" ("preço estimado a pagar pela entidade adjudicante"), relevant to procedure choice and to the competent organ for the expense. — [CMS](https://cms.law/pt/prt/news-information/alteracao-ao-codigo-dos-contratos-publicos); text versions 2008-07-30, 2021-06-20, 2026-10-01 in [DR capture: ccp-art17.1.r2.json]
- New art. 17.º, n.º 2: the valor estimado "condiciona a escolha do procedimento" and determines the competent organ for authorising the expense. — [DR capture: ccp-art17.r2.json]
- Art. 47.º, n.º 1 (from 2026-10-01): the entity "pode fixar" a preço base = maximum it will pay, including extensions; i.e. preço base is optional and is not the procedure-choice value. — [DR capture: ccp-art47.1.r2.json]; Fieldfisher (search snippet): from 1 Oct 2026 valor estimado is the reference for procedure choice and preço base becomes optional — [Fieldfisher](https://www.fieldfisher.com/pt-pt/locations/portugal/insights/alteracoes-ao-codigo-dos-contratos-publicos-novas-regras-para-o-valor-estimado-e-preco-base)
- Pre-reform case law treated preço base as the maximum the entity will pay, tied to art. 47.º, n.º 1 b) and the procedure chosen. — [TCA Norte, proc. 02935/13.1BEPRT (2014), via vLex](https://vlex.pt/vid/acordao-n-02935-13-1044139269)
- IVA: art. 473.º — all amounts in the Code, the valor estimado, preço base and preço contratual "não incluem o imposto sobre o valor acrescentado" (wording "valor do contrato" until 2026-10-01, "valor estimado do contrato" from 2026-10-01). Art. 60.º: proposal prices do not include IVA. — [DR capture: ccp-art473.r2.json, ccp-art60*.json]
- "Orçamento" and "cabimento" are budget/expense-authorisation concepts (art. 36.º ties the decision to contract to the organ competent to authorise the expense) and are not CCP procedure-choice values. — [DR capture: ccp-art36.1.r2.json]. No web source was found that documents users conflating cabimento with preço base (see Gaps).

**D. Fracionamento**
- Art. 22.º (division into lots / aggregation) is REVOKED by art. 8.º of DL 177/2026 from 2026-10-01. — [DR capture: ccp-art22.1.r1.json]
- Its role passes to new art. 17.º-B "Fracionamento e regras de agregação do valor estimado do contrato": n.º 1 forbids calculating the value or splitting the object "com o intuito de excluir a observância de quaisquer exigências legais"; n.º 3 aggregates the valores estimados of same-type prestações; n.º 4 exempts contracts < 80 000 € (bens/serviços) or < 1 000 000 € (obras) if ≤ 20 % of the aggregate; n.º 5 sets a 12-month rule for recurring purchases. — [DR capture: ccp-art17-b.r2.json, valid_from 2026-10-01]
- Practice evidence: an audit-authority note (Agência para o Desenvolvimento e Coesão / IGF audits) classes artificial splitting of expenses or contracts as a breach of art. 22.º CCP, leading to a 100 % financial correction, and flags ajustes diretos breaching art. 113.º, n.º 2. — [CIG, Informação de gestão 8 jun 2021](https://www.cig.gov.pt/wp-content/uploads/2021/06/Informacao-de-gestao_8-de-junho-2021.pdf) (via search snippet)
- Invitee limits (anti-recurrence, a cousin of splitting): IMPIC Orientação Técnica 01/CCP/2018 explains art. 113.º — entities already awarded contracts in the current and two previous economic years by AD or CP cannot be invited once cumulative values reach the limits. — [IMPIC OT 01/CCP/2018](https://www.base.gov.pt/Base4/media/1pklcuvi/orientacao_tecnica_impic_ccp_final_2018-1.pdf). Art. 113.º, n.º 3 counts per gabinete/serviço for the Estado and autonomously per município, i.e. entity structure changes the arithmetic. — [DR capture: ccp-art113.3.r2.json]

**E. Tribunal de Contas audit findings (procedure-choice and publication errors in practice)**
- Marvão: TdC audit after a complaint about ajustes diretos in Jul–Sep 2017; recommended favouring competitive procedures over consulta prévia or ajuste direto and timely, accurate Portal BASE publication. — [24noticias/SAPO](https://24noticias.sapo.pt/atualidade/artigos/tribunal-de-contas-identifica-falhas-em-27-contratos-na-camara-municipal-de-marvao)
- IHRU: three ajuste-direto contracts paid before Portal BASE publication (art. 127.º CCP), treated as possible ground for sanction. — [idealista](https://www.idealista.pt/news/node/21771)
- Águas de Portugal: of 81 ajuste-direto files audited, 85 % showed irregularities (justification, competition). — [ECO, 2017](https://eco.sapo.pt/2017/05/10/aguas-de-portugal-85-dos-ajustes-diretos-tem-irregularidades/)

**F. Dates**
- Art. 36.º, n.º 1: the procedure "inicia-se com a decisão de contratar" (versions 2008, 2018-01-01 adding "deve ser fundamentada", 2026-10-01 dropping "podendo essa decisão estar implícita nesta última"). — [DR capture: ccp-art36.1.r2.json]. So the regime-deciding date is the decisão de contratar, not the anúncio, the invitation, the adjudicação or the contract date.
- Neither CMS nor ECO defines how "início do procedimento" is determined for the transition; CMS summary says so explicitly. — [CMS](https://cms.law/pt/prt/news-information/alteracao-ao-codigo-dos-contratos-publicos); [ECO](https://eco.sapo.pt/descodificador/12-perguntas-e-respostas-para-perceber-as-novas-regras-da-contratacao-publica/)

### Inferences
- Taxonomy of user errors (for the extraction policy in section 3):
  1. **Procedure naming.** Bare "concurso" (could be concurso público or limitado por prévia qualificação; lay users also use it for any competitive call, including consulta prévia); "concurso internacional" used for JOUE publication; "ajuste direto com três propostas" / "ajuste direto com consulta" used for consulta prévia (pre-2018 mental model; consulta prévia only appears in arts. 19/20 from 2018-01-01); "concurso" used when the user actually means ajuste direto with a request for quotes.
  2. **Outdated thresholds.** 20k/30k/75k/150k (valid 2018-01-01 → 2026-09-30) stated as current; 2026 headline "150 mil" applied to bens/serviços; EU thresholds from the wrong biennium (135k, 139k, 140k, 214k/215k/221k etc.); Lei 30/2021 simplified-consultation 750k cap treated as general.
  3. **Value terms.** "valor do contrato" (pre-2026 concept) vs "valor estimado"; "preço base" assumed mandatory and assumed to be the procedure-choice value; "orçamento", "cabimento", "verba", "dotação" used for the value; amounts "com IVA" fed into thresholds that are defined without IVA (art. 473.º).
  4. **Fracionamento.** Premise that splitting into lots or successive contracts lets each stay under the AD threshold; citing art. 22.º for a post-2026-10-01 procedure (revoked; now art. 17.º-B, with a different 80k/1M/20 % exemption).
  5. **Entity type.** "Câmara" (organ) vs "município" (legal person); junta de freguesia; empresa municipal (possibly organismo de direito público, not Estado); instituto público / universidade / hospital EPE / escola (whether "Estado" for art. 474.º, n.º 3 b) is a law question); "Governo" vs "ministério" vs "direção-geral".
  6. **Publication.** "Anúncio" without saying DR or JOUE; belief that only "big" concursos need DR; belief that concurso público always goes to JOUE (false since arts. 19.º b)/20.º b) allow no-JOUE below thresholds), or never needs it below the national thresholds.
  7. **Dates.** "O concurso abre / arranca / foi lançado" (= anúncio/convite date) used as the start of procedure (= decisão de contratar, art. 36.º); contract date or adjudicação date used for the regime switch; the boundary case of a procedure started on 2026-10-01 itself ("após" in art. 10.º, n.º 1 of DL 177/2026 is ambiguous on that day — this is a law-reading question for the engine).
- Several errors are *coupled to the reform*: the same sentence ("ajuste direto até 20 mil") was true on 2026-09-30 and false on 2026-10-01 for bens/serviços, so "wrong" depends on data_inicio_procedimento — another reason the extractor must not judge premises.

### Gaps
- No primary tcontas.pt audit report or recomendação text was retrieved; TdC findings above come from press. Searches for "fracionamento" + "artigo 22.º" returned only Brazilian TCE-MT results, which were discarded as wrong jurisdiction.
- No CCDR parecer, DGAL, or ANMP guidance on misconceptions was found in the searches made.
- No source found that documents user confusion of cabimento/orçamento with preço base, or IVA-inclusive amounts in practice; these classes rest on the primary law text (arts. 36.º, 47.º, 473.º) plus inference.
- Fieldfisher pages returned HTTP 403; their content is from search snippets only.
- The 139.000 € (CCP art. 474.º, n.º 3 b) as republished) vs 140.000 € (Cuatrecasas, Reg. 2025/2152) conflict is unresolved.
- The APCMC "consulta prévia especial" up to 2 M€ is unconfirmed.
- How DL 177/2026 treats a procedure whose decisão de contratar is dated exactly 2026-10-01 was not found in any commentary.

## 2. Short real examples of such errors (quotes under 15 words, with URL)

### Takeaway
Verbatim user-question errors from public forums were not found; the citable real examples are press/law-firm phrasings that seed false premises and audit findings of actual misuse. The project's own question corpus (`factos-v1`) contains realistic user phrasings that exhibit each error class and can serve as test cases, but its provenance (real vs authored) is not documented.

### Cited Findings
- Headline overgeneralising the new AD threshold: "ajustes diretos podem chegar aos 150 mil euros" — [Postal.pt](https://postal.pt/nacional/nova-lei-da-contratacao-publica-entra-em-vigor-ajustes-diretos-podem-chegar-aos-150-mil-euros/) (only obras; bens/serviços < 75.000 €).
- Old value concept still in circulation: "valor máximo do benefício económico que pode ser obtido pelo adjudicatário" — [CMS](https://cms.law/pt/prt/news-information/alteracao-ao-codigo-dos-contratos-publicos) (the pre-2026 definition now replaced).
- Audit evidence of misuse: 85 % of 81 ajuste-direto files with irregularities — [ECO 2017](https://eco.sapo.pt/2017/05/10/aguas-de-portugal-85-dos-ajustes-diretos-tem-irregularidades/); Marvão AD contracts questioned — [24noticias](https://24noticias.sapo.pt/atualidade/artigos/tribunal-de-contas-identifica-falhas-em-27-contratos-na-camara-municipal-de-marvao); IHRU paid AD contracts before BASE publication — [idealista](https://www.idealista.pt/news/node/21771); artificial splitting under art. 22.º → 100 % correction — [CIG 2021](https://www.cig.gov.pt/wp-content/uploads/2021/06/Informacao-de-gestao_8-de-junho-2021.pdf).
- Project corpus examples (file `~/ccp-engine/training/real-questions/factos-v1.questions.jsonl`, 40 items, "hoje" mostly 2026-10-27):
  - Bare procedure uncertainty: "Não sabemos se é concurso ou ajuste direto." (real-factos-06)
  - preço base used as the procedure-choice value: "O preço base anda nos 45 mil euros." (real-factos-02, AD for bens)
  - Launch date as start date: "Lançámos ontem um concurso público…" (real-factos-14) and "O concurso arranca … a 3 de novembro" (real-factos-01).
  - JOUE premise from a colleague: "O colega diz que … não precisa de ir ao JOUE." (real-factos-26)
  - Entity-type question: "uma universidade pública conta como Estado para o CCP?" (real-factos-40)
  - Regime boundary: "Se o procedimento tiver começado no próprio dia 1 de outubro…" (real-factos-31)
  - Urgency premise (not a fact field): "Podemos fazer por ajuste direto por ser urgente?" (real-factos-12)
- How these items are currently labelled in the gold file: "Câmara Municipal" → `tipo_entidade: "outra"`; "Ministério"/"direção-geral"/"secretaria-geral do ministério" → `"estado"`; "instituto", "escola secundária", "universidade" → `tipo_entidade` omitted; place names (Viana do Castelo, Matosinhos, Évora) → `territorio: "PT"`, Ribeira Grande/Ponta Delgada/São Jorge → `"PT-AC"`, Funchal/Câmara de Lobos/Santa Cruz → `"PT-MA"`; "O concurso arranca/abre/lançámos" → `data_inicio_procedimento`; "preço base" → `preco_base`; real-factos-26 (colleague's JOUE claim) → no `publicado_joue`. — [project file: factos-v1.questions.jsonl]

### Inferences
- The gold labels already apply a sensible policy (premises and colleague's claims are not facts; ambiguous entity types are left out), but two mappings embed law-adjacent judgements that should be explicit: (i) anúncio/launch date → `data_inicio_procedimento` although art. 36.º, n.º 1 says the procedure starts with the decisão de contratar; (ii) `preco_base` is the only value field, although from 2026-10-01 procedure choice is by valor estimado (art. 17.º, n.º 2) and preço base is optional (art. 47.º, n.º 1). The engine (not the extractor) must decide whether a stated preço base can stand in for valor estimado; the extractor should only report which term the user used.
- "Câmara Municipal → outra" is safe because no reading of art. 474.º, n.º 3 b) puts a municipality under "Estado"; "instituto/universidade → omit" is also right because it requires a legal classification.

### Gaps
- No verbatim public-forum user errors (e.g., Reddit r/portugal, Citius/ordem forums, ANMP Q&A) were found; searches in Portuguese for forum-style errors returned irrelevant results.
- Whether `factos-v1` questions are real user questions or authored is not stated in the file.

## 3. How should the fact-extraction step label each error class?

### Takeaway
Use five statuses per field: **stated** (extract the user's fact as stated, even if their legal conclusion is wrong), **not stated** (omit), **contradictory** (two incompatible values for the same field → omit the field and emit a conflict marker), **ambiguous** (a term maps to several enum values → omit and emit an ambiguity marker naming the candidates), and **premise about the law** (a rule, threshold or legal classification the user asserts → never a fact; drop it, optionally log it verbatim for the engine to check). The extractor never "fixes" the law, never converts a stated amount (e.g. strips IVA) and never derives one field from another via a legal rule.

### Cited Findings
- Legal anchors that make the following splits necessary: valor estimado drives procedure choice (art. 17.º, n.º 2) — [DR capture: ccp-art17.r2.json]; preço base optional (art. 47.º, n.º 1) — [DR capture: ccp-art47.1.r2.json]; all CCP amounts exclude IVA (art. 473.º) — [DR capture: ccp-art473.r2.json]; procedure starts with decisão de contratar (art. 36.º, n.º 1) — [DR capture: ccp-art36.1.r2.json]; "Estado" vs "outras entidades" is the art. 474.º, n.º 3 b)/c) split — [DR capture: ccp-art474.r2.json]; JOUE vs no-JOUE concurso both exist — [DR capture: ccp-art19.r2.json, ccp-art20.r2.json].
- The project's extraction prompt already states: "Um facto que a pergunta não afirma fica de fora; não o deduzas nem o adivinhes." — [project file: ~/ccp-engine/training/real-questions/factos-v1.jsonl]

Proposed per-class policy (each row is grounded in the law anchors above; the policy itself is a design inference):

| Error class | Example phrasing | Label | Extractor output |
|---|---|---|---|
| Wrong legal claim around a correct fact | "Posso fazer AD para bens de 45 mil?" | stated (fact) + premise ignored | `tipo_procedimento: ajuste_direto`, `tipo_contrato: bens`, amount as stated; no judgement on legality |
| Outdated threshold asserted | "o limite do AD é 20 mil, certo?" | premise about the law | no field; optionally `premissas: ["limite AD 20 mil"]` verbatim for the engine |
| Bare "concurso" | "vamos abrir um concurso" | ambiguous | omit `tipo_procedimento`; `ambiguo: {tipo_procedimento: [concurso_publico, concurso_limitado_previa_qualificacao]}` (consulta prévia possible in lay use) |
| "concurso público" explicit | | stated | `concurso_publico` |
| "concurso internacional" / "anúncio europeu" | | stated (for JOUE) | `publicado_joue: true`; procedure only if named |
| "anúncio" without DR/JOUE | | not stated (for JOUE) | omit `publicado_joue` |
| "só no Diário da República" | | stated | `publicado_joue: false` |
| Bare "valor", "orçamento", "cabimento", "verba" | "o valor é 90 mil" | ambiguous (which value) | do not fill `preco_base`; `ambiguo: {valor: 90000, termo: "valor"}` — or, if the schema keeps one amount field, record the user's term alongside it |
| "preço base X" | | stated | `preco_base: X` (engine decides if it may proxy valor estimado) |
| "com IVA" / "IVA incluído" | "120 mil com IVA" | stated amount + qualifier | keep 120000 as stated and add `iva_incluido: true`; never divide by 1.23 (rate depends on goods and region) |
| Fracionamento intent | "dividimos em três AD de 25 mil" | stated facts (each lot) + premise | extract what is stated (per-lot amount, procedure); the aggregation question (art. 17.º-B) is the engine's |
| Entity: ministério / direção-geral / secretaria-geral | | stated → mapped | `tipo_entidade: estado` (direct central government) |
| Entity: câmara / município / junta / freguesia | | stated → mapped | `tipo_entidade: outra` |
| Entity: instituto, universidade, hospital EPE, escola, empresa municipal, "o Governo Regional" | | ambiguous / law question | omit; `ambiguo: {tipo_entidade: "instituto"}` (classification is a legal reading) |
| "Estado" in the loose sense ("somos do Estado") | | ambiguous unless a central-government body is named | omit or mark ambiguous |
| Date: "a decisão de contratar foi a 2 de outubro" | | stated | `data_inicio_procedimento: 2026-10-02` |
| Date: "o concurso abre / lançámos / anúncio a …" | | stated but different event | keep separate (`data_anuncio`) or, if only one field, fill and flag `data_tipo: anuncio`; never treat as decisão de contratar silently |
| Date: contract signing / adjudicação | | different event | not `data_inicio_procedimento` |
| Relative dates ("amanhã", "próxima semana") | | stated relative to "hoje" | resolve only when exact ("amanhã"); "próxima semana" without a day → ambiguous |
| Two incompatible values | "consulta prévia… é um ajuste direto"; "preço base 60 mil… 80 mil" | contradictory | omit both; `conflito: {campo: [v1, v2]}` |
| Colleague's / third party's claim | "o colega diz que não vai ao JOUE" | premise (reported) | not a fact; omit `publicado_joue` (current gold label already does this, real-factos-26) |
| Urgency, "por ser urgente", "imperiosa" | | premise / material criterion | no field in schema; leave to engine (material criteria such as urgency are law) |
| Place name only | "em Matosinhos" | stated → mapped | `territorio` (geographic mapping is fact, not law) |

### Inferences
- The key line is between **mapping** (lexical/geographic: "Ponta Delgada" → PT-AC; "ministério" → estado; "empreitada" → obras) and **legal classification** (whether a universidade is "Estado"; whether refeições escolares are bens or serviços — real-factos-38 rightly leaves `tipo_contrato` out). Mapping is allowed; legal classification is the engine's job or a clarifying question.
- Because the engine is deterministic, the safest response to contradiction and ambiguity is to *withhold the field and surface a marker*, letting the engine either ask a clarifying question or return conditional answers per candidate value. Guessing a value converts an extraction error into a wrong legal answer.
- Recording the user's own term (e.g. `termo_valor: "valor"|"preço base"|"orçamento"`, `iva_incluido`, `data_tipo`) costs little and lets the engine detect premise errors (like using preço base for procedure choice, or IVA-inclusive amounts) without the extractor making a legal call.
- False premises about the law should be captured verbatim at most (`premissas: [...]`), never normalised into a rule, because the same sentence can be true or false depending on the date regime (section 1).

### Gaps
- No Portuguese procurement-specific literature on question-extraction policies was found; the table is a design derived from the law text plus the QA literature in section 4.

## 4. What does QA research say about false premises, and when to ask vs extract vs abstain?

### Takeaway
False-premise questions are common (about a quarter of Reddit questions in CREPE) and models detect them poorly without training; the recommended response is to identify and correct the premise rather than answer as if true. Ambiguity research finds models under-ask and over-answer. For a pipeline split into extractor + deterministic engine, this supports: the extractor neither corrects nor answers, it only separates facts from premises and flags ambiguity; the engine (with the law) corrects premises and decides whether to ask.

### Cited Findings
- **CREPE** (ACL 2023): 8,400 Reddit questions annotated for false presuppositions and corrections; about a quarter contain false presuppositions; best response is a correction; models detect presuppositions moderately but struggle to verify them, largely because of evidence retrieval. — [ACL Anthology 2023.acl-long.583](https://aclanthology.org/2023.acl-long.583); [arXiv 2211.17257](https://arxiv.org/abs/2211.17257v1)
- **(QA)²** (ACL 2023, Kim, Htut, Bowman, Petty): real search-engine queries, some with false or unverifiable assumptions (e.g. "When did Marie Curie discover Uranium?"); models struggle; one summary reports best model ~59 % human acceptability. — [ACL Anthology 2023.acl-long.472](https://aclanthology.org/2023.acl-long.472); [Google Research](https://research.google/pubs/qa2-question-answering-with-questionable-assumptions/)
- **FalseQA** ("Won't Get Fooled Again", ACL 2023): 2,365 human-written false-premise questions with explanations and revised true-premise versions; PLMs can learn to discriminate FPQs with moderate fine-tuning (~256 examples). — [ACL 2023 virtual](https://virtual2023.aclweb.org/paper_P3014.html); later work: models often recognise but fail to explicitly refute false premises — [KG-FPQ, arXiv 2407.05868](https://arxiv.org/html/2407.05868v1)
- **KG-FPQ**: ~178k automatically generated false-premise questions from knowledge graphs. — [arXiv 2407.05868](https://arxiv.org/html/2407.05868v1). **MultiHoax**: multi-hop false premises requiring consistency checks across steps. — [arXiv 2506.00264](https://arxiv.org/html/2506.00264v1)
- **CLAMBER** (ACL 2024): ~12K items on a taxonomy of query ambiguity; LLMs are weak at identifying and clarifying ambiguity; CoT/few-shot gives marginal gains and may increase overconfidence; clarifying questions are low quality. — [arXiv 2405.12063](https://arxiv.org/html/2405.12063v2)
- **ClarifyMT-Bench**: multi-turn; consistent under-clarification bias, models answer prematurely, worse with dialogue depth. — [arXiv 2512.21120](https://arxiv.org/html/2512.21120v1)

### Inferences
- Applied to the CCP pipeline:
  - **Extract** when a field value is stated or lexically/geographically mappable (no legal reasoning).
  - **Withhold + flag** (ambiguous/contradictory) when the user's term maps to several enum values or two values conflict; the evidence (CLAMBER, ClarifyMT) says models under-flag, so the training set should over-represent such cases with explicit `ambiguo`/`conflito` targets.
  - **Ask a clarifying question** only at the engine/dialogue layer and only when the missing or ambiguous field changes the legal outcome (e.g. bare "concurso" matters for prazos; it may not matter for "quais os limiares"). The engine can compute this by checking whether all candidate values give the same answer.
  - **Abstain/correct** is the engine's job for false premises about the law (CREPE/(QA)² recommend correcting the premise), using the dated law, never the extractor's knowledge.
- FalseQA's finding that ~256 examples suffice to learn FPQ discrimination suggests a small, targeted set of CCP premise examples (outdated thresholds, art. 22.º citations, IVA-inclusive amounts, launch-date-as-start) is enough to teach the extractor to *not* turn premises into facts.

### Gaps
- No paper found on false premises in a domain-specific legal fact-extraction setting (extractor + rule engine); the mapping above is inference.
- "Clarify When Necessary" (as a named paper) was not confirmed by the searches; only CLAMBER and ClarifyMT-Bench were.
- FalseQA author list and exact metrics were not verified from the paper itself (abstract-level only).
