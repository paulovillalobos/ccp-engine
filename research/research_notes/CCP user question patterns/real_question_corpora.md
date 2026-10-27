# Real written CCP question corpora (European Portuguese): where they live and what they look like

Research date: 2026-10-27. Scope: real, written questions about the Código dos Contratos Públicos (CCP) from municipal staff, officials, suppliers and citizens. All quotes are short (under 15 words) and copied from the linked page or PDF. Where a CCDR parecer *restates* the question rather than transcribing it, the example is marked "(restated by CCDR)". Placeholders such as "Câmara Municipal de ..." are the source's own anonymisation.

Method note: CCDR Alentejo pareceres were fetched in bulk (IDs 500-1325 of `https://www.ccdr-a.gov.pt/app_ext/pareceres/printpdf.php?id=N`) and text-extracted locally. About 35 of the ~800 retrievable documents in that range are procurement or contract-related; the rest are local-government HR, eleitos locais and similar topics.

## Which public sources hold real written CCP questions, and who asks?

### Takeaway
The richest open corpus of *real* written CCP questions is the CCDR legal-opinion (parecer) archive. CCDR Alentejo's archive is the most useful, because it often transcribes the câmara's or junta's question verbatim in quotation marks, dates it, and runs from 2005 to late 2025. Official FAQs (BASE/IMPIC, Segurança Social) are editorial questions written by the institution, not real user questions. Supplier questions appear in published "pedidos de esclarecimento" for individual procedures. I could not access Reddit, forums or LinkedIn from this environment.

### Cited Findings
**CCDR Alentejo pareceres jurídicos (real; best source)**
- Each document has a fixed header (Título, Data, Parecer N.º, Informação N.º) and then a stock formula: "Solicitou a Câmara Municipal de ... parecer jurídico ... sobre a seguinte questão:", followed by the question in quotes — [CCDR-A parecer 1300 (2024)](https://www.ccdr-a.gov.pt/app_ext/pareceres/printpdf.php?id=1300); [CCDR-A parecer 1150 (2021)](https://www.ccdr-a.gov.pt/app_ext/pareceres/printpdf.php?id=1150)
- The askers are câmaras municipais, juntas/uniões de freguesia, comunidades intermunicipais and other local bodies (e.g., a Região de Turismo). Requests come by ofício, by email, and even forwarded from DGAL — [parecer 737 (2008, Marvão, email forwarded by DGAL)](https://www.ccdr-a.gov.pt/app_ext/pareceres/printpdf.php?id=737); [parecer 705 (2006, Região de Turismo de Évora)](https://www.ccdr-a.gov.pt/app_ext/pareceres/printpdf.php?id=705); [parecer 1200 (2022, Comunidade Intermunicipal)](https://www.ccdr-a.gov.pt/app_ext/pareceres/printpdf.php?id=1200)
- Older pareceres name the municipality (Marvão, Elvas, Viana do Alentejo, Almodôvar, Castro Verde, Grândola, Monsaraz, Pias). Most pareceres from about 2018 onward anonymise it as "Município de ...", though 2025's parecer 1325 still names Portel — [parecer 801 (2009, Elvas)](https://www.ccdr-a.gov.pt/app_ext/pareceres/printpdf.php?id=801); [parecer 1325 (2025, Portel)](https://www.ccdr-a.gov.pt/app_ext/pareceres/printpdf.php?id=1325)
- Procurement-related titles found in the scan include: ajuste direto for a PDM revision (2008), two ajustes diretos for obras with the same company in consecutive years (2009), art. 113.º/128.º counting (2009, 2023), hiring an excavator with operator (2016), continuous labour supply (2015), extraordinary price revision in empreitadas (2023-2024), project-review exemptions under DL 108/2024 (2025), and expense authorisation for empreitadas (2025) — [CCDR-A archive, printpdf ids 565, 616, 801, 1262, 1047, 1023, 1237, 1315, 1323](https://www.ccdr-a.gov.pt/app_ext/pareceres/printpdf.php?id=1262)
- CCDR-A frames its role as "apoio técnico às autarquias locais" under DL 36/2023 and calls its opinions "meramente opinativo" — [parecer 1323 (2025)](https://www.ccdr-a.gov.pt/app_ext/pareceres/printpdf.php?id=1323)

**CCDR Lisboa e Vale do Tejo pareceres (real; older)**
- Uses a "QUESTÃO" block that transcribes the câmara's numbered questions in quotes. Example: Parecer 72/CCDR-LVT/2011 has 3 main questions and nested sub-questions (1.1, 1.2, 1.2.1) — [CCDR-LVT Parecer 72/2011](https://www.ccdr-lvt.pt/wp-content/uploads/2022/03/532d4f2ce29c1dedd33f5248fc3984496322de9e.pdf)
- Other 2011 LVT pareceres in the same upload batch are about HR (recruitment) rather than procurement — [CCDR-LVT Parecer 49/2011](https://www.ccdr-lvt.pt/wp-content/uploads/2022/03/ecb0e08469ad6a5c89c28883c91957e8665de0e1.pdf)

**CCDR Centro pareceres (exist, but not retrievable here)**
- The site lists numbered pareceres (e.g., "Parecer DAJ 201/2021" on an ajuste direto for an artistic performance under art. 24.º/1/e)/i)), but both WebFetch and curl were blocked (redirect loop / empty response) — [CCDRC Parecer DAJ 201/2021](https://www.ccdrc.pt/en/?p=28060); [CCDRC Parecer DSAJAL 104/20](https://www.ccdrc.pt/pt/?p=26994)
- CCDRC also published a contratação pública guide for freguesias (2015) — [CCDRC Guia Contratação Pública Freguesia 2015](https://www.ccdrc.pt/wp-content/uploads/2016/07/Guia_Contratacao_Publica_Freguesia_2015_Parte_I-361.pdf)

**Official FAQs (editorial, not real user questions)**
- The Portal BASE "Perguntas frequentes" page is still live and holds 54 question-form headings. They are institutional and definitional (e.g., "O que é o ajuste direto?", "Quando é que se pode adotar o procedimento de ...?"), one per procedure type: ajuste direto, simplificado, consulta prévia, concurso público, urgente, CLPQ, negociação, diálogo concorrencial, parceria para a inovação — [BASE perguntas frequentes](https://www.base.gov.pt/Base4/pt/perguntas-frequentes/)
- A Segurança Social FAQ for IPSS beneficiaries ("Mobilidade Verde Social") reuses the BASE wording almost verbatim (P6 "O que é o ajuste direto?", P7 "Quando é que se pode adotar...") and adds a beneficiary-specific question on whether the entity is an entidade adjudicante. Its disclaimer says the FAQs "não respondem a casos concretos" — [Seg. Social FAQ Contratação Pública (PDF)](https://sisscontent.seg-social.pt/documents/10152/18433474/FAQ%27+s+_+Contra%C3%A7%C3%A3o+P%C3%BAblica_Mobilidade+Verde+Social.pdf/49e26ced-3dae-4d17-b011-e5f3ca4d6251)
- The IMPIC FAQ URLs either returned HTTP 500 (`/contratacao-publica/perguntas-frequentes`) or redirected to a 404 (`/faqs`) on 2026-10-27 — [IMPIC](https://www.impic.pt/impic/pt-pt/contratacao-publica/perguntas-frequentes)

**Supplier questions: "pedidos de esclarecimento" in published procedures (real)**
- Municipalities publish the clarification requests and the júri's answers as PDFs. Example: Lamego CP/DFP/022/2025 (cleaning services, concurso público). An incumbent supplier complains that the preço base is too low, and the júri answers with the arithmetic — [Município de Lamego, esclarecimentos](https://www.cm-lamego.pt/cmlamego/uploads/document/file/2385/esclarecimentos.pdf)

**Explainers in Q&A form (journalistic, not real user questions)**
- ECO's "12 perguntas e respostas" on the 2026 CCP reform is a press explainer — [ECO descodificador](https://eco.sapo.pt/descodificador/12-perguntas-e-respostas-para-perceber-as-novas-regras-da-contratacao-publica/)
- Context for the 2026 thresholds: press reports that DL 177/2026 (DR 4 Sep 2026, in force 1 Oct 2026) raised the ajuste direto ceiling to €150k for obras and €75k for bens/serviços. This is a secondary source, not checked against DR here — [Postal do Algarve](https://postal.pt/nacional/nova-lei-da-contratacao-publica-entra-em-vigor-ajustes-diretos-podem-chegar-aos-150-mil-euros/); [Fieldfisher](https://www.fieldfisher.com/pt-pt/locations/portugal/insights/que-procedimento-posso-escolher-a-partir-de-1-de-outubro)

### Inferences
- For a generator imitating *public-official* questions, CCDR pareceres (Alentejo first, LVT second) are the most authentic and best-dated corpus. They span pre-CCP (2005-2007), the first CCP years (2008-2010), the 2017/2018 revision era and post-2023 CCDR I.P.
- Official FAQs are useful only as the "textbook" register: short, definitional, no facts. They show what a question looks like with *every* procedure fact missing.
- Supplier questions are of a different kind. They challenge a specific procedure's preço base or requirements rather than ask which procedure applies.

### Gaps
- **Reddit (r/portugal, r/literaciafinanceira, r/portugueses):** the reddit.com JSON API returned non-JSON (blocked), and WebSearch refuses reddit.com ("domains are not accessible to our user agent"). No Reddit threads were checked.
- **Portuguese forums, LinkedIn groups, Ordem dos Advogados, OCC consultório, Ciberdúvidas:** searches returned nothing usable. I found no CCP question on Ciberdúvidas or the OCC site.
- **CCDR Norte and CCDR Algarve:** I found no parecer database with question text. CCDR Centro exists but blocks automated fetch.
- **DGAL "soluções interpretativas uniformes", ANMP, ANAFRE:** none surfaced in search. No question text was obtained.
- **Vortal/acinGov/anoGov help forums, espap FAQs:** the espap FAQ URL returned 200 but was not parsed for content. No platform user forums were found.
- **Brazil (Lei 14.133) Q&A forums for contrast:** searches returned municipal legal documents, not forum Q&A. Not characterised.

## For each source: length, register, vagueness, which procedure facts are stated, wrong premises

### Takeaway
Real official questions (CCDR) are formal, often long (1 sentence to a 300+ word ofício with numbered sub-questions), and organised around a legal doubt rather than a fact sheet. They usually state the object (and so imply tipo_contrato), sometimes a value in loose form, and occasionally the procedure. They almost never state JOUE publication, territory, entity type "Estado", or a procedure start date. Several rest on contestable premises or informal terms.

### Cited Findings
**CCDR pareceres: register and length**
- The register is formal-administrative ("solicita-se a V.Ex.ª se digne emitir parecer"), often with legal citations by the asker, e.g., the CPV code 45500000-2 or Regulamento (CE) 213/2008 — [parecer 1047 (2016)](https://www.ccdr-a.gov.pt/app_ext/pareceres/printpdf.php?id=1047); [parecer 1023 (2015)](https://www.ccdr-a.gov.pt/app_ext/pareceres/printpdf.php?id=1023)
- Lengths range from one sentence (Marvão 2008, one question; Região de Turismo 2006, one question) to multi-paragraph ofícios with numbered points 1-3 and a closing request — [parecer 737](https://www.ccdr-a.gov.pt/app_ext/pareceres/printpdf.php?id=737); [parecer 705](https://www.ccdr-a.gov.pt/app_ext/pareceres/printpdf.php?id=705); [parecer 1023](https://www.ccdr-a.gov.pt/app_ext/pareceres/printpdf.php?id=1023)
- CCDR sometimes notes that the asker gave too little: Marvão "não emitiu o seu entendimento", so the parecer "será necessariamente genérico". Grândola "não indicam ... quais os preceitos legais" — [parecer 737](https://www.ccdr-a.gov.pt/app_ext/pareceres/printpdf.php?id=737); [parecer 616](https://www.ccdr-a.gov.pt/app_ext/pareceres/printpdf.php?id=616)
- Some askers attach their own legal analysis, or another body's (ANMP and ANAFRE notes; the municipality's consultor jurídico) and ask for confirmation — [parecer 985 (2014)](https://www.ccdr-a.gov.pt/app_ext/pareceres/printpdf.php?id=985); [parecer 1310 (2025)](https://www.ccdr-a.gov.pt/app_ext/pareceres/printpdf.php?id=1310)
- Triggers include a training session ("Na sequência de uma formação") and a Tribunal de Contas devolution of a contract — [parecer 1262 (2023)](https://www.ccdr-a.gov.pt/app_ext/pareceres/printpdf.php?id=1262); [parecer 1319 (2025)](https://www.ccdr-a.gov.pt/app_ext/pareceres/printpdf.php?id=1319)

**Facts stated or omitted (target fields)**
- **preco_base:** rarely called "preço base" by officials. Values appear as "valor", "valor estimado", ranges, "ronda os", "não chega a", or a number with odd separators ("até 149,639,37"). Some values are per item, not per contract. Examples: Marvão, each purchase under €4,000; Monsaraz, a van at €19,000; PDM revision €25k-75k; RSU contract about €70k; Grândola obras of €65,572.57 (2008) and €22,000 (2009) — [737](https://www.ccdr-a.gov.pt/app_ext/pareceres/printpdf.php?id=737), [804](https://www.ccdr-a.gov.pt/app_ext/pareceres/printpdf.php?id=804), [565](https://www.ccdr-a.gov.pt/app_ext/pareceres/printpdf.php?id=565), [728](https://www.ccdr-a.gov.pt/app_ext/pareceres/printpdf.php?id=728), [616](https://www.ccdr-a.gov.pt/app_ext/pareceres/printpdf.php?id=616), [1323](https://www.ccdr-a.gov.pt/app_ext/pareceres/printpdf.php?id=1323)
- **tipo_contrato:** usually *implied by the object* (viatura usada, brita/areia/tout-venant, beberete, carrinha, limpeza), not named. It is sometimes explicitly contested: the excavator-with-operator case asks whether it is aquisição de serviços or empreitada, and the labour case asks about "fornecimento em contínuo de serviços de mão-de-obra" for paving work — [1047](https://www.ccdr-a.gov.pt/app_ext/pareceres/printpdf.php?id=1047), [1023](https://www.ccdr-a.gov.pt/app_ext/pareceres/printpdf.php?id=1023), [737](https://www.ccdr-a.gov.pt/app_ext/pareceres/printpdf.php?id=737)
- **tipo_procedimento:** stated when the doubt is about a procedure ("ajuste directo simplificado", "ajuste direto"). It is absent when the asker wants the procedure chosen for them ("que procedimentos são necessários?", "qual o procedimento a adoptar") — [801](https://www.ccdr-a.gov.pt/app_ext/pareceres/printpdf.php?id=801), [737](https://www.ccdr-a.gov.pt/app_ext/pareceres/printpdf.php?id=737), [1047](https://www.ccdr-a.gov.pt/app_ext/pareceres/printpdf.php?id=1047)
- **tipo_entidade:** always implicit through the asker's identity (Câmara, Junta, Comunidade Intermunicipal, Região de Turismo). I found no case where an asker said "Estado". The Seg. Social FAQ shows IPSS beneficiaries unsure whether they are even an entidade adjudicante — [705](https://www.ccdr-a.gov.pt/app_ext/pareceres/printpdf.php?id=705), [1200](https://www.ccdr-a.gov.pt/app_ext/pareceres/printpdf.php?id=1200), [Seg. Social FAQ](https://sisscontent.seg-social.pt/documents/10152/18433474/FAQ%27+s+_+Contra%C3%A7%C3%A3o+P%C3%BAblica_Mobilidade+Verde+Social.pdf/49e26ced-3dae-4d17-b011-e5f3ca4d6251)
- **publicado_joue / territorio / data_inicio_procedimento:** not stated in any question inspected. Time is anchored indirectly: "novo Código" (Dec 2008), "no ano de 2008 ... no ano de 2009", "procedimento concursal desenvolvido em maio de 2020", "Decreto-Lei n.º 108/2024" — [737](https://www.ccdr-a.gov.pt/app_ext/pareceres/printpdf.php?id=737), [616](https://www.ccdr-a.gov.pt/app_ext/pareceres/printpdf.php?id=616), [1200](https://www.ccdr-a.gov.pt/app_ext/pareceres/printpdf.php?id=1200), [1315](https://www.ccdr-a.gov.pt/app_ext/pareceres/printpdf.php?id=1315)
- **Territory** is implied only by which CCDR answers (Alentejo or LVT = continente). No question mentions Açores or Madeira — [CCDR-A archive](https://www.ccdr-a.gov.pt/app_ext/pareceres/printpdf.php?id=1262)

**Wrong or contestable premises and non-standard terms**
- "vulgo requisição" is used as the colloquial name for ajuste direto simplificado — [CCDR-LVT 72/2011](https://www.ccdr-lvt.pt/wp-content/uploads/2022/03/532d4f2ce29c1dedd33f5248fc3984496322de9e.pdf)
- The asker infers the contract type from a CPV code and a BASE portal behaviour ("o aluguer de máquina escavadora é objeto de ... empreitada"). This is a premise CCDR had to analyse, not a settled fact — [1047](https://www.ccdr-a.gov.pt/app_ext/pareceres/printpdf.php?id=1047)
- Grândola justifies a repeat ajuste direto because the firm is the "única disponível ... no prazo previsto". CCDR says it will also examine the legal basis the junta "pensaria ser aplicável" — [616](https://www.ccdr-a.gov.pt/app_ext/pareceres/printpdf.php?id=616)
- Elvas argued that art. 113.º/2 limits do not apply to the simplified ajuste direto. The 2023 Alentejo câmara took the opposite view, calling it "claro" that they count — [801 (2009)](https://www.ccdr-a.gov.pt/app_ext/pareceres/printpdf.php?id=801); [1262 (2023)](https://www.ccdr-a.gov.pt/app_ext/pareceres/printpdf.php?id=1262)
- The question about cancelling completed procedures and asking suppliers to return money shows an asker worried about drastic consequences — [CCDR-LVT 72/2011](https://www.ccdr-lvt.pt/wp-content/uploads/2022/03/532d4f2ce29c1dedd33f5248fc3984496322de9e.pdf)
- Marvão splits one need into several purchases under €4,000 and asks what procedure applies. The fractioning issue is unstated — [737](https://www.ccdr-a.gov.pt/app_ext/pareceres/printpdf.php?id=737)

**Supplier clarification requests**
- Informal-commercial register: the request opens "Como é do vosso conhecimento", mixes complaint and demand, ends "Aguardamos retificação / Cumprimentos". It cites wage agreements and the previous procedure, and its key fact is the preço base — [Lamego esclarecimentos](https://www.cm-lamego.pt/cmlamego/uploads/document/file/2385/esclarecimentos.pdf)
- The júri disputes a factual premise of the supplier ("o júri não compreendeu ... o mapa é idêntico ao procedimento de 2024") — [Lamego esclarecimentos](https://www.cm-lamego.pt/cmlamego/uploads/document/file/2385/esclarecimentos.pdf)

### Inferences
- A generator imitating real askers should drop most procedure fields by default. Officials state the object and maybe a fuzzy value. JOUE, territory and start date almost always have to be inferred or asked for.
- Values should be produced in messy forms: "não chega a 4.000 €", "ronda os € 70 000", "entre € 25 000 e € 75 000", "149,639,37", with and without IVA, per item vs per contract.
- tipo_contrato should often be ambiguous (machinery with operator, labour for paving, project design as "bem ou serviço"). These are exactly the cases where real askers write in.
- Time is expressed through law references and years, not ISO dates. The 1 Oct 2026 threshold change will likely produce "a partir de 1 de outubro" style anchors, as the Fieldfisher article title already shows (inferred, not observed in user questions).

### Gaps
- No informal citizen or SME question corpus was inspected (Reddit and forums inaccessible), so the informal register is only represented by one supplier clarification.
- Lengths are characterised qualitatively. No word-count statistics were computed across the corpus.

## Real examples (short quotes with URLs)

### Takeaway
36 real quotes from 3 kinds of source (CCDR pareceres, a supplier clarification request, official FAQs). Each is under 15 words. "(restated)" marks text written by the CCDR jurist paraphrasing the request; everything else is the asker's own words as transcribed.

### Cited Findings
**Câmaras/juntas to CCDR Alentejo**
1. "A autarquia precisa de comprar uma viatura usada à empresa X" — Marvão, 2008 — [737](https://www.ccdr-a.gov.pt/app_ext/pareceres/printpdf.php?id=737)
2. "cada aquisição não chega a 4.000 €." — Marvão, 2008 — [737](https://www.ccdr-a.gov.pt/app_ext/pareceres/printpdf.php?id=737)
3. "Conforme o novo Código de Contratos Públicos que procedimentos são necessários?" — Marvão, 2008 — [737](https://www.ccdr-a.gov.pt/app_ext/pareceres/printpdf.php?id=737)
4. "adquirir uma carrinha no valor de € 19 000" (restated) — JF Monsaraz, 2010 — [804](https://www.ccdr-a.gov.pt/app_ext/pareceres/printpdf.php?id=804)
5. "valor do contrato se deve situar entre € 25 000 e € 75 000" (restated) — PDM revision, 2008 — [565](https://www.ccdr-a.gov.pt/app_ext/pareceres/printpdf.php?id=565)
6. "o valor estimado para tal contrato ronda os € 70 000" (restated) — Castro Verde, 2007 — [728](https://www.ccdr-a.gov.pt/app_ext/pareceres/printpdf.php?id=728)
7. "única disponível para iniciar e concluir a obra no prazo previsto" — JF Grândola, 2009 — [616](https://www.ccdr-a.gov.pt/app_ext/pareceres/printpdf.php?id=616)
8. "a interpretação das normas que regulam o acima mencionado, não são consensuais" — JF Grândola, 2009 — [616](https://www.ccdr-a.gov.pt/app_ext/pareceres/printpdf.php?id=616)
9. "deve ser considerado na \"contagem mencionada no nº 2 do artº. 113º\"" — Elvas, 2009 — [801](https://www.ccdr-a.gov.pt/app_ext/pareceres/printpdf.php?id=801)
10. "qual o procedimento a adoptar pela Câmara Municipal em futuros alugueres de máquinas" — 2016 — [1047](https://www.ccdr-a.gov.pt/app_ext/pareceres/printpdf.php?id=1047)
11. "o aluguer de máquina escavadora é objeto de \"contratação de empreitada de obras públicas\"" — 2016 — [1047](https://www.ccdr-a.gov.pt/app_ext/pareceres/printpdf.php?id=1047)
12. "Temos conhecimento de vários profissionais (da zona) que podem efetuar esses trabalhos" — 2015 — [1023](https://www.ccdr-a.gov.pt/app_ext/pareceres/printpdf.php?id=1023)
13. "através de um contrato de fornecimento em contínuo de serviços de mão-de-obra" — 2015 — [1023](https://www.ccdr-a.gov.pt/app_ext/pareceres/printpdf.php?id=1023)
14. "Na sequência de uma formação frequentada por colaboradoras da Secção de Contratualização Pública" — 2023 — [1262](https://www.ccdr-a.gov.pt/app_ext/pareceres/printpdf.php?id=1262)
15. "será o valor acumulado do ajuste direto simplificado (5.000, 00 euros) também por triénio?" — 2023 — [1262](https://www.ccdr-a.gov.pt/app_ext/pareceres/printpdf.php?id=1262)
16. "tem competência para autorizar a despesa para obras e empreitadas até 149,639,37?" — 2025 — [1323](https://www.ccdr-a.gov.pt/app_ext/pareceres/printpdf.php?id=1323)
17. "Em caso afirmativo, qual o fundamento legal?" — 2025 — [1323](https://www.ccdr-a.gov.pt/app_ext/pareceres/printpdf.php?id=1323)
18. "possibilidade legal de contratação de um jurista licenciado em Direito não inscrito" — Portel, 2025 — [1325](https://www.ccdr-a.gov.pt/app_ext/pareceres/printpdf.php?id=1325)
19. "estaria reservada exclusivamente a advogados com inscrição em vigor na Ordem dos Advogados" — Portel, 2025 — [1325](https://www.ccdr-a.gov.pt/app_ext/pareceres/printpdf.php?id=1325)
20. "uma pessoa para abrir e fechar as portas do mercado público" (restated) — JF Pias, 2013 — [928](https://www.ccdr-a.gov.pt/app_ext/pareceres/printpdf.php?id=928)
21. "contratos de prestação de serviços com valores inferiores a € 5 000,00" (restated) — Viana do Alentejo, 2014 — [985](https://www.ccdr-a.gov.pt/app_ext/pareceres/printpdf.php?id=985)
22. "pode vir a celebrar contratos de prestação de serviços e/ou de empreitada com o Município" (restated) — Almodôvar, 2014 — [994](https://www.ccdr-a.gov.pt/app_ext/pareceres/printpdf.php?id=994)
23. "A Autarquia questiona se a Presidente da Junta pode votar a aquisição do imóvel" — União de Freguesias, 2019 — [1107](https://www.ccdr-a.gov.pt/app_ext/pareceres/printpdf.php?id=1107)
24. "existe obrigatoriedade ou não de preencher o formulário do Reporte Estatístico" (restated) — JF São Brás e São Lourenço, 2013 — [909](https://www.ccdr-a.gov.pt/app_ext/pareceres/printpdf.php?id=909)
25. "Pedido de esclarecimento sobre a aplicação do Decreto-Lei n.º 108/2024 - dispensa de revisão de projeto" (email subject line) — 2025 — [1315](https://www.ccdr-a.gov.pt/app_ext/pareceres/printpdf.php?id=1315)
26. "qual é o código de Nuts" — Região de Turismo de Évora, 2006 — [705](https://www.ccdr-a.gov.pt/app_ext/pareceres/printpdf.php?id=705)
27. "a confirmação da possibilidade de ser adjudicada uma aquisição de serviços a uma pessoa" (restated) — JF, 2022 — [1222](https://www.ccdr-a.gov.pt/app_ext/pareceres/printpdf.php?id=1222)

**Câmara to CCDR LVT**
28. "todas as prestações de serviço ao abrigo do ajuste directo simplificado (vulgo requisição)" — 2011 — [CCDR-LVT 72/2011](https://www.ccdr-lvt.pt/wp-content/uploads/2022/03/532d4f2ce29c1dedd33f5248fc3984496322de9e.pdf)
29. "deverão ser anulados, solicitada a devolução das verbas e reiniciar o procedimento" — 2011 — [CCDR-LVT 72/2011](https://www.ccdr-lvt.pt/wp-content/uploads/2022/03/532d4f2ce29c1dedd33f5248fc3984496322de9e.pdf)
30. "Ou podemos daí excluir este serviço, pois também nos é fornecido um bem" — 2011 — [CCDR-LVT 72/2011](https://www.ccdr-lvt.pt/wp-content/uploads/2022/03/532d4f2ce29c1dedd33f5248fc3984496322de9e.pdf)

**Supplier to júri (pedido de esclarecimento)**
31. "se lança um caderno de encargos, com valor base insuficiente" — Lamego CP, 2025 — [Lamego](https://www.cm-lamego.pt/cmlamego/uploads/document/file/2385/esclarecimentos.pdf)
32. "O Valor base é claramente insuficiente. Aguardamos retificação" — Lamego CP, 2025 — [Lamego](https://www.cm-lamego.pt/cmlamego/uploads/document/file/2385/esclarecimentos.pdf)

**Editorial FAQs (institution-written; for contrast)**
33. "Quando é que se pode adotar o procedimento de ajuste direto?" — [BASE FAQ](https://www.base.gov.pt/Base4/pt/perguntas-frequentes/)
34. "Quando é que se pode adotar o procedimento de parceria para inovação?" — [BASE FAQ](https://www.base.gov.pt/Base4/pt/perguntas-frequentes/)
35. "Como saber se somos enquadrados como entidade adjudicante ou não adjudicante?" — [Seg. Social FAQ](https://sisscontent.seg-social.pt/documents/10152/18433474/FAQ%27+s+_+Contra%C3%A7%C3%A3o+P%C3%BAblica_Mobilidade+Verde+Social.pdf/49e26ced-3dae-4d17-b011-e5f3ca4d6251)
36. "Quais os procedimentos de Contratação Pública a adotar?" — [Seg. Social FAQ](https://sisscontent.seg-social.pt/documents/10152/18433474/FAQ%27+s+_+Contra%C3%A7%C3%A3o+P%C3%BAblica_Mobilidade+Verde+Social.pdf/49e26ced-3dae-4d17-b011-e5f3ca4d6251)

### Inferences
- Examples 1-3 (Marvão) are the closest real analogue to the target input: one shared object list, a per-purchase value, and an open "which procedure?" question. Treat them as an anchor style.
- Quotes from 2005-2018 use pre-Acordo Ortográfico spelling ("directo", "adoptar", "contratos ... Contrtos" typo). Real text mixes old and new orthography, and a generator should too.

### Gaps
- No quotes from citizens, Reddit, forums, LinkedIn or Ciberdúvidas (sources not reachable or nothing found). Treat the corpus as biased toward local-government officials.

## Which question shapes recur?

### Takeaway
Five shapes recur in the real material: (A) context then an open "which procedure?" question; (B) a yes/no "can we do X?" with an embedded value; (C) a numbered multi-question ofício with conditional branches ("Caso a resposta seja não..."); (D) "is our interpretation right?", with the asker's own view or an attached third-party opinion; (E) a complaint/demand from a supplier on the preço base. The literal "Posso fazer ajuste direto para X de Y euros?" shape appears only in restated form in these sources.

### Cited Findings
- **(A) Context → open procedure question:** Marvão lists 3 purchases and values, then asks "que procedimentos são necessários?". The excavator case gives a long CPV argument, then asks "qual o procedimento a adoptar" — [737](https://www.ccdr-a.gov.pt/app_ext/pareceres/printpdf.php?id=737); [1047](https://www.ccdr-a.gov.pt/app_ext/pareceres/printpdf.php?id=1047)
- **(B) Can-we yes/no with value:** "pretende saber se pode escolher o procedimento por ajuste directo" with €25k-75k; whether buying a €19,000 van requires the electronic platform — [565](https://www.ccdr-a.gov.pt/app_ext/pareceres/printpdf.php?id=565); [804](https://www.ccdr-a.gov.pt/app_ext/pareceres/printpdf.php?id=804)
- **(C) Numbered multi-question with conditional branches:** LVT 72/2011 (1, 1.1 "Caso a resposta seja não", 1.2 "No caso de sim", 1.2.1 "Ainda se sim", 2, 3); 2025 expense-competence case ("Em caso afirmativo, qual o fundamento legal?" followed by a fallback question) — [CCDR-LVT 72/2011](https://www.ccdr-lvt.pt/wp-content/uploads/2022/03/532d4f2ce29c1dedd33f5248fc3984496322de9e.pdf); [1323](https://www.ccdr-a.gov.pt/app_ext/pareceres/printpdf.php?id=1323)
- **(D) Interpretation check:** Elvas states its own reading of arts. 113.º/128.º. A 2024 câmara describes "a interpretação dos serviços deste Município" and asks for a parecer. Viana do Alentejo attaches ANMP/ANAFRE notes — [801](https://www.ccdr-a.gov.pt/app_ext/pareceres/printpdf.php?id=801); [1300](https://www.ccdr-a.gov.pt/app_ext/pareceres/printpdf.php?id=1300); [985](https://www.ccdr-a.gov.pt/app_ext/pareceres/printpdf.php?id=985)
- **(E) Supplier complaint/demand:** Lamego clarification request — [Lamego](https://www.cm-lamego.pt/cmlamego/uploads/document/file/2385/esclarecimentos.pdf)
- **Editorial FAQ shape:** "O que é X?" / "Quando é que se pode adotar X?", one pair per procedure — [BASE FAQ](https://www.base.gov.pt/Base4/pt/perguntas-frequentes/)

### Inferences
- The generator should produce all five real shapes, not just the "Posso fazer ajuste direto...?" template. Shape A (facts first, open question last) and shape C (multi-question) are the most common in official writing. Shape C forces the parser to handle several procedures or contracts in one message.
- Questions are often *about* procedure facts (counting art. 113.º limits, competence by value, contract-type qualification) rather than asking for the procedure outright. A parser should still extract the facts from the context paragraph.

### Gaps
- Frequencies are not quantified. Shape labels come from about 30 inspected documents, not a full-corpus count.

## Are any of these corpora licensed for reuse?

### Takeaway
I found no explicit open licence on the CCDR parecer archives, the BASE FAQ, the Seg. Social FAQ or the municipal clarification PDFs. They are public administrative documents, but reuse terms were not stated on the pages inspected. (Notes only; no training use planned.)

### Cited Findings
- IMPIC publishes BASE *contract/announcement datasets* on dados.gov.pt. That is open data, but it covers contracts, not FAQs or questions — [dados.gov.pt BASE anúncios dataset](https://dados.gov.pt/en/datasets/contratos-publicos-portal-base-impic-anuncios-de-2012-a-2026/)
- The CCDR-A parecer PDFs carry only a header "Pareceres Jurídicos CCDRAlentejo, I.P. - http://www.ccdr-a.gov.pt", with no licence text in the extracted pages — [CCDR-A parecer 1323](https://www.ccdr-a.gov.pt/app_ext/pareceres/printpdf.php?id=1323)
- The Seg. Social FAQ states it is general information, not legal advice, and gives no reuse licence — [Seg. Social FAQ](https://sisscontent.seg-social.pt/documents/10152/18433474/FAQ%27+s+_+Contra%C3%A7%C3%A3o+P%C3%BAblica_Mobilidade+Verde+Social.pdf/49e26ced-3dae-4d17-b011-e5f3ca4d6251)

### Inferences
- Short quotation for analysis is the safe use. The CCDR archives' anonymisation ("Município de ...") already strips most identifying data from recent pareceres. Older ones name municipalities and, in one case, a private company (Grândola 2009), which argues for anonymising before any reuse.

### Gaps
- I did not check the site-level legal notices (aviso legal/termos de utilização) of ccdr-a.gov.pt, ccdr-lvt.pt, base.gov.pt or seg-social.pt. Reddit's licensing was not checked because Reddit was inaccessible.
