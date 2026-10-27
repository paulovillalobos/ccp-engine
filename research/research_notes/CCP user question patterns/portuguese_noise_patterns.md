# Noise patterns in Portuguese user-written questions for a public-procurement assistant (typed and dictated)

Scope note: European Portuguese (PT-PT) first, Brazilian (PT-BR) as a contrast. The best quantified typed-error data that exists is Brazilian. For PT-PT the published numbers are older, smaller, or qualitative. Every rate below says which variety and genre it comes from. Rates that are my own proposals for the generator appear only under "Inferences".

---

## 1. Typos and misspellings: accents, keyboard slips, transpositions, doubled or dropped letters, hyphens and clitics, homophones, capitalisation

### Takeaway
In typed Portuguese, diacritic errors (mostly accents simply left out) are the largest single error class: about 38–51% of all spelling errors, against roughly 10% insertions, 12–24% omissions, 3–13% substitutions and under 4% transpositions. Over 85% of misspelled words have exactly one error. Spontaneous text has 1.8–4.8 errors per 100 words. The best typed-text statistics are PT-BR. The PT-PT evidence (Medeiros 1995, higher-education and school corpora) points the same way: accent omission dominates, especially on proparoxytones.

### Cited Findings
**Error-type distribution in typed text (PT-BR, Gimenes, Roman & Carvalho 2015, *Computational Linguistics* 41(1))** — [ACL Anthology J15-1011](https://aclanthology.org/J15-1011.pdf)
- Corpora: C1 = 1,808 texts typed in a web browser by 452 participants, 62,858 words, no spell-checker. C2 = 192 travel-blog posts, 26,418 words. Only non-word errors were counted.
- **Error rate per word: C1 (university participants) 1.81%; C2 (blogs, more conversational) 4.77%.** The authors attribute part of the gap to blogs being "more conversation-like", with relaxed rules "especially when it comes to errors involving diacritics".
- C1 distribution of 1,139 errors: **missing diacritic 37.66%**, omission 17.12%, substitution 12.82%, insertion 10.45%, **missing cedilla 6.06%**, other 6.06%, transposition 3.69%, **missing space (glued words) 2.37%**, addition of a diacritic 1.67%, wrong diacritic on the right letter 0.96%, right diacritic on the wrong letter 0.79%, other space errors about 0.35%.
- C2 distribution of 1,260 errors: **missing diacritic 45.48%**, omission 24.13%, other 10.32%, insertion 9.44%, substitution 5.79%, missing cedilla 4.44%, transposition 0.24%, addition of a diacritic 0.16%.
- Diacritic errors including the cedilla make up 47.15% (C1) and 50.08% (C2) of all errors, and 49.48% and 58.84% of single errors.
- **Words with exactly one error: 92.3% (C1), 86.3% (C2).** Two errors: 6.7% and 9.0%. Three: 0.7% and 3.6%. More than three: 0.3% and 1.1%.
- Comparison with Spanish (Bustamante et al. 2006, Mexico and Spain), by share of misspelled words: missing diacritic 51.5% in Spanish against 42.16% (C1) and 50.71% (C2). There is no statistically significant difference between Spanish and PT-BR. The authors conclude the distribution depends on the character set more than on the language.
- The cedilla has its own category because Brazilian keyboards differ. ABNT-2 has a dedicated ç key. "US-accents" layouts need two keys (' then c), so a missing ç is either a keyboard slip or a diacritic omission depending on the layout.
- "Other" covers linguistic expression errors, first-letter capitalisation and wrong diminutive or augmentative forms.

**PT-PT data (via the Gimenes literature review)** — [J15-1011](https://aclanthology.org/J15-1011.pdf)
- Medeiros (1995), European Portuguese corpora (published error lists, handwritten high-school errors, some e-mail): **80.1% of spelling errors fall into Damerau's four categories**, and **about 20% of "linguistic" errors involve diacritics**. Gimenes et al. note that the data has no frequency analysis, so it is not suitable for statistical weighting.

**PT-PT higher-education and school writing**
- Castelo & Sousa (Universidade Aberta) studied 119 texts from master's entrance exams. Accentuation is a frequent problem even among highly educated writers. The most common errors are on proparoxytones and false proparoxytones, usually an accent left out. — [Repositório Aberto UAb](https://repositorioaberto.uab.pt/bitstream/10400.2/11999/1/Castelo__Sousa_Desempenhoortogrficoemestudantesdoensinosuperior-aacentuaogrfica.pdf) (finding taken from the search summary; I did not read the full PDF for counts)
- EFFE-On corpus, 2nd and 4th grade, 40 texts: accentuation and irregular spelling are the most common misspellings. — [eduCAPES / UAb](https://educapes.capes.gov.br/handle/10400.2/13135?mode=full)

**User-generated product reviews (PT-BR, Duran et al. 2014, WaC-9, and Duran, Avanço & Nunes 2015, WNUT)** — [W14-0404](https://aclanthology.org/W14-0404/); [W15-4305](https://aclanthology.org/W15-4305.pdf)
- The Buscapé corpus has 85,910 reviews, 4,097,905 tokens and 90,513 types. After stop-words, numbers and punctuation are removed there are 63,917 types, of which 34,774 are out of vocabulary (OOV). Of these, **3,652 (reported as 10.2%) were words missing a diacritic**.
- 1,323 OOV types were confirmed as misspellings: **791 typos (59.8%), 451 phonetically motivated errors (34.1%), 64 misused diacritics (4.8%), and 14 (1.1%) errors related to the new Acordo Ortográfico, mostly hyphens in compounds**. Note that missing diacritics had already been auto-corrected before this split, so diacritic errors are under-represented in it.
- **About 25,000 Portuguese word pairs differ only by a diacritic** (e.g. "varias" / "várias"). Because UGC systematically drops diacritics, these become real-word errors that a dictionary lookup cannot catch.
- Case noise: capitals missing after punctuation and on proper nouns; common words in capitals for emphasis ("MUITO BOM"); whole reviews in upper or lower case; random mid-sentence capitals ("De forma Discarada ... ORIGINAL!"). There is also missing punctuation and "uninterrupted" run-on text.
- Hand-annotated samples, 60 reviews each (counts of items needing normalisation):

| Noise type | Buscapé (3,179 tokens) | Mercado Livre (3,897 tokens) |
|---|---|---|
| common (non-word) misspellings | 56 | 108 |
| real-word misspellings (mostly a dropped accent producing another word) | 39 | 76 |
| internet slang | 6 | 25 |
| case: proper names and acronyms | 12 | 19 |
| case: sentence start | 14 | 12 |
| glued words | 2 | 6 |
| punctuation errors | 47 | 79 |

  From those counts, per token: misspellings in total 3.0% and 4.7%; punctuation errors 1.5% and 2.0%; case errors 0.8% for both; slang 0.2% and 0.6%; glued words 0.06% and 0.15%. My arithmetic, using the paper's counts and token totals.
- UGCNormal recall: 84% on non-word misspellings, **only 34% on real-word misspellings**, 61% on slang. Real-word (accent-pair) errors are the hardest class.

**Homophone and confusable pairs (qualitative, PT-PT and PT-BR)**
- "À muito tempo" for "há muito tempo" is listed as one of the most frequent errors in Portugal. — [e-konomista.pt](https://www.e-konomista.pt/erros-ortograficos/)
- "mas/mais" and "mal/mau" appear among common orthographic errors (PT-BR, Enem). — [Catraca Livre](https://catracalivre.com.br/educacao/enem-5-erros-ortograficos-portugues/)
- x/ch confusion (e.g. "mecher" for "mexer") is a typical error. — [Dicio](https://www.dicio.com.br/erros-de-ortografia/)

### Inferences
- The proposed injection table below anchors on Gimenes C2 (blog register, 4.77 errors per 100 words) as the "casual" level and C1 (1.81 per 100) as the "careful" level. These are PT-BR typed texts. They transfer reasonably to PT-PT because Gimenes et al. found the distribution tracks the character set, and PT-PT has the same set: á à â ã é ê í ó ô õ ú ç.
- Proposed per-word corruption probabilities for a generator (casual / careful):
  - Accent dropped on a word that has one: about 0.35 / 0.12 of accented tokens. **This is my estimate, not published.** It assumes missing diacritics are about 45% of a 4.8% error rate, concentrated on the roughly 12–15% of tokens that carry accents. Prioritise high-frequency function words and endings: é→e, à→a, há→ha, já, até, também→tambem, ção→cao, ções→coes, ão→ao, número→numero, público→publico, prévio, cláusula→clausula, específico. Proparoxytones (público, económico, título, válido) are the most error-prone per the PT-PT higher-education study.
  - ç→c: about 5% of errors (Gimenes). Apply to "-ção"/"-ções" (contratação, adjudicação, prestação). In PT-PT these words often lose both marks: "contratacao".
  - Letter omission 17–24% of errors; insertion or doubling about 10%; substitution 6–13%; transposition 0.2–4%; glued words 2.4%.
  - Real-word accent swaps should get their own explicit class. Procurement-relevant pairs: "é/e", "à/a/há", "público/publico" (publico is also a verb), "prévia/previa", "válido/valido", "último/ultimo", "está/esta", "têm/tem", "pôr/por", "contrário/contrario".
- Keyboard-adjacency substitutions should use the PT-PT QWERTY layout. On that layout ç sits to the right of L, and the accent keys are dead keys near Enter: ´/` and ~/^ as two keys. Plausible slips: "ç" replaced by "l" or "º"; a dead key pressed after the vowel ("e´"); a stray standalone "´" or "~" ("ac~ao"); "ã" typed as "â" because ~ and ^ share a key. **This layout detail comes from general knowledge. I did not verify it in this pass (see Gaps).**
- Hyphen and clitic errors (PT-PT specific): "faze-lo/fazê-lo/fazelo", "pode-se/podesse", "deve-se/devesse", "submete-se/submetesse", "encontra-se", and mesoclisis avoided or broken ("far-se-á" written "fará-se"). Duran et al. found AO-related hyphen errors at about 1% of misspellings in PT-BR UGC. PT-PT uses enclitics much more, so I expect clitic hyphen errors to be more frequent in PT-PT. That is unquantified.

### Gaps
- No published typed-error frequency table exists for **European Portuguese** typed text with frequencies. Medeiros (1995) lacks frequencies, and I did not open the full Castelo & Sousa PDF to get counts.
- I found no published keyboard-adjacency confusion matrix for the PT-PT layout, and no PT-PT data on dead-key errors.
- I found no published rate for há/à/a, mas/mais, or clitic-hyphen confusions. The available sources are prescriptive lists without counts.
- LanguageTool and Priberam/FLiP do not publish rule-hit statistics that I could find. CETEMPúblico-derived misspelling studies did not come up in search.

---

## 2. Pre- and post-Acordo Ortográfico 1990 variants in Portugal

### Takeaway
The 1990 Acordo became mandatory in Portugal on 13 May 2015. It changed about 1.5–1.6% of PT-PT words (against about 0.5% in Brazil), mostly by dropping silent consonants (acção→ação, actual→atual, efectivo→efetivo, direcção→direção, adopção→adoção) and by lower-casing months. Resistance has been sustained, including a petition of nearly 100,000 signatures, and old and new spellings coexist in submitted manuscripts and the press. I found **no measured share of pre-AO spelling in current PT-PT user text**.

### Cited Findings
- Implementation in Portugal is described as finalised: the AO entered into force on 13 May 2015. In Brazil, the transition ended at the close of 2015, and the new norm was mandatory from 1 Jan 2016. — [Observador 2016](https://observador.pt/2016/01/01/acordo-ortografico-falantes-portugues-sobem-215-milhoes/); [DN](https://www.dn.pt/sociedade/entra-em-vigor-no-brasil-e-ja-e-obrigatorio-para-215-milhoes-4960523.html)
- Share of words changed: **about 1.6% in Portugal against about 0.5% in Brazil**, a figure from critics reported by IJNet. — [IJNet](https://ijnet.org/en/node/2691). A 2009 news report gives **about 1.5%** for Portugal and the countries that follow its spelling. — [Olhar Direto](https://olhardireto.com.br/noticias/adocao-da-reforma-ortografica-em-portugal-continua-indefinida)
- Example changes cited: acção, afectivo, direcção, adopção (silent consonant dropped). — [IJNet](https://ijnet.org/en/node/2691)
- A petition against the AO reached nearly 100,000 signatures. — [IJNet](https://ijnet.org/en/node/2691)
- A Portuguese paediatrics journal describes manuscripts arriving in a mix of spellings, from pre-AO to post-AO, and the editors now require the AO. This is a testimony, not a count. — [PJP / SPP](https://ojs.pjp.spp.pt/article/download/3075/2480/7252)
- A 2019 Renascença column says many people in Portugal refuse to write according to the AO. — [RR.pt, Sarsfield Cabral 2019](https://rr.pt/artigo/francisco-sarsfield-cabral/2019/05/27/o-desacordo-ortografico/152809/)
- Some outlets adopted the AO early (Record, Correio da Manhã, two regional papers), and Expresso publicly supported it. These sources are older (2009–2019). — [Olhar Direto](https://olhardireto.com.br/noticias/adocao-da-reforma-ortografica-em-portugal-continua-indefinida)
- Garcia, Gamallo, Gayo & Pousada Cruz (2014), "PoS-tagging the Web in Portuguese. National varieties, text typologies and spelling systems" (*Procesamiento del Lenguaje Natural* 53): web Portuguese mixes varieties and spelling systems, and they built AO dictionaries and a mixed-variety test corpus. The abstract gives no proportions. — [Minerva USC](https://minerva.usc.gal/entities/publication/0eeb2b56-66c9-4a98-b1b5-2b9053b2c00f/full)
- In PT-BR UGC, AO-related errors (mostly hyphens in compounds) were 14 of 1,323 misspellings (1.1%). — [W15-4305](https://aclanthology.org/W15-4305.pdf)

### Inferences
- The generator should treat pre-AO spellings as a **whole-question style switch**, not as independent per-word noise. A writer who uses "acção" will usually also write "actual", "efectivo", "direcção" and "Junho". As a starting guess, give about 15–25% of PT-PT questions the pre-AO style, plus a smaller share (about 5%) of inconsistent mixing within a question. **These rates are my assumption, not measured.** Older public servants and lawyers are the most likely to keep pre-AO spelling, which matters for a procurement audience.
- Procurement-relevant pre-AO/post-AO pairs to inject: acção/ação, actual/atual, actualização/atualização, efectivo/efetivo, efectuar/efetuar, directo/direto (as in "ajuste directo"), direcção/direção, objecto/objeto (as in "objecto do contrato"), projecto/projeto, adjectivo, exacto/exato, contracto (not a standard spelling in either system; hypercorrection), selecção/seleção, colectivo/coletivo, sector (unchanged in PT-PT), Junho/junho, Janeiro/janeiro, "Diário da República" (unchanged). Also "facto" stays in PT-PT but is "fato" in PT-BR, which is a variety marker and not AO noise.
- Hypercorrections such as "contracto" and "fato" for "facto" are plausible but unquantified.

### Gaps
- I found no corpus count (CRPC, CETEMPúblico, Corpus do Português NOW, or Linguateca AcDC) of "acção" against "ação" after 2015, and no survey of AO adoption in private or informal PT-PT writing. A generator rate would need a direct corpus query, e.g. NOW-corpus counts for Portuguese .pt sites by year.
- I could not confirm the current editorial spelling policy of Público, Expresso or Observador from primary sources.

---

## 3. Abbreviations and shorthand in procurement talk

### Takeaway
I found no published study of shorthand in procurement-domain questions. General Portuguese texting shorthand is documented in learner and qualitative sources: hj, n, pq, mt, tb/tbm, cmg, fds, tou. The procurement acronym set has to be compiled from the CCP domain itself.

### Cited Findings
- European Portuguese texting abbreviations: hj (hoje), tou (estou), n (não), pq (porque/porquê), mt (muito), bjs/bjos (beijos), tb/tbm (também), cmg (comigo), ctg (contigo), fds (fim de semana). They date from the character-limited SMS era and persist out of habit. — [Practice Portuguese](https://www.practiceportuguese.com/blog/portuguese-text-abbreviations/)
- PT-PT qualitative work describes online writing as moving towards speech, with abbreviations and anglicisms spread by SMS and email. — [Janus 2004, Maia e Carmo](https://www.janusonline.pt/arquivo/docs2004/artigo_janus2004_2_17.doc). A Silves, Algarve case study looked at how texting affects mother-tongue use in 16–21-year-olds. — [Arias Montano (UHU)](https://ariasmontano.uhu.es/entities/publication/92c10084-8f89-4481-8093-6fc28cd47013)
- PT-BR internetês involves "drastic reduction of word forms", heavy abbreviation and dropped accents (Faraco, as summarised). Normalisers map expansions such as "vc"→"você". — [UNICAMP / revistas.iel](https://revistas.iel.unicamp.br/index.php/lle/article/view/1151/933); the UGCNormal pipeline uses separate siglas_map and internetes_map modules — [UGCNormal](https://backiee.wasmer.app/http_www_github_com/avanco/UGCNormal)
- UGCNormal's lexicons hold 420 internet-slang items and 156 acronyms, built from PT-BR product reviews. In product reviews, unlike SMS, abbreviations and agglutination are relatively rare. — [W15-4305](https://aclanthology.org/W15-4305.pdf)

### Inferences
- **The procurement acronym inventory below comes from my domain knowledge of the Código dos Contratos Públicos (DL 18/2008). It was not verified from a usage source in this pass.** Use it as the expansion dictionary, and inject both directions (full form to acronym, acronym to full form):
  - Procedures: CP (concurso público), CLPQ (concurso limitado por prévia qualificação), AD (ajuste direto / ajuste directo), "AD simplificado", "consulta prévia" (sometimes "CPrévia" or "CPr"), PN (procedimento de negociação), "diálogo concorrencial", "acordo-quadro" (AQ), SDA/SAD (sistema de aquisição dinâmico), "parceria para a inovação".
  - Legal and publication: CCP, DL (decreto-lei), "art." / "artº" / "art.º" (artigo), "nº / n.º / no / n°" (número, often with the wrong ordinal sign ° instead of º), "al." (alínea), DR / "D.R." (Diário da República), JOUE / JO / "JO UE" (Jornal Oficial da União Europeia), "BASE" / "portal base", "TdC" / "Tribunal de Contas", "visto prévio", CPV, "ESPAP", "TED", "DEUCP" (Documento Europeu Único de Contratação Pública, often confused with "DEUC"), "CE" (caderno de encargos), "PP" (programa do procedimento), PB (preço base), "PA" (preço anormalmente baixo; also "preço anormalmente baixo" written "PAB"), IVA, "s/IVA", "c/IVA", "+IVA", "IVA incl.".
  - Generic shorthand: "c/" (com), "s/" (sem), "p/" (para), "q" / "k" (que; "k" is more PT-PT youth register), "tb", "n" (não), "pq", "msm" (mesmo), "mt", "obg" (obrigado), "ref." (referência), "proc." (procedimento or processo), "adj." (adjudicação), "entid." (entidade).
- Money shorthand to inject: "k", "mil", "m€" (ambiguous between mil and milhão), "M€", "milhões", "1,5M", "1.5M", "€1500", "1500€", "1 500 €", "1.500,00 €", "EUR 1500", "1500 euros", "mil e quinhentos euros", "um milhão e meio".

### Gaps
- There is no corpus or frequency study of shorthand in Portuguese procurement or legal questions (helpdesk logs, Portal BASE FAQ, IMPIC or espap support tickets). Real rates would need such logs.
- I did not verify the full forms of "q", "k", "td", "msm", "p/", "c/" or "s/" against a linguistic source. They are standard but uncited here.

---

## 4. Number, money and date formats and their common mistakes

### Takeaway
I found no PT-PT error study of number and date formats. Locale conventions differ across sources: the EU says there is no single European rule and it is national practice. The generator should cover the format variants listed below as format diversity, not as measured error rates.

### Cited Findings
- The European Commission position, quoted on a W3C list: "there is no European rule on this, it is a matter for national rules and practices to determine" (currency formatting and thousands separators). — [W3C www-international 2000](https://lists.w3.org/Archives/Public/www-international/2000JulSep/0007.html)
- Locale software exposes separate flags for whether the currency symbol comes before or after the amount, and whether there is a space. — [PHP localeconv](https://www.php.net/manual/pt_BR/function.localeconv.php)
- The same number renders as 1.000.000,00 (German) or 1 000 000,00 (French), showing that point and space thousands separators coexist across EU locales. — [ArcGIS docs](https://enterprise.arcgis.com/pt-br/portal/10.6/use/format-numbers.htm)
- PT-BR dispensa thresholds are written as "R$ 130.984,20", i.e. currency symbol first with a point thousands separator. This is a PT-BR contrast. — [ConLicitação 2026](https://conlicitacao.com.br/lei-14133-atualizada/)

### Inferences
- Variants to generate for PT-PT money. **Comma decimal is the norm. The decimal-point confusion is my assumption, not measured.**
  - "1000€", "1000 €", "1 000 €", "1.000 €", "1.000,00 €", "€1000", "€ 1.000,00", "EUR 1.000", "1000 euros", "mil euros", "1 mil euros", "5 mil €", "5k", "5k€", "75.000€", "75 000", "75000", "750 mil", "1,5 M€", "1,5 milhões", "1.5 milhões" (point decimal, an anglicised error), "um milhão e meio", "meio milhão".
  - Ambiguity traps: "1.500" can mean 1500 or 1.5 when written English-style. "1,500" is ambiguous between EN-style 1500 and PT 1.5. "m€" and "M€" are confused (mil against milhão). "s/IVA" against "c/IVA" and an IVA percentage written "23%" or "23 %".
  - Thresholds a user might mention in procurement terms: "20 mil", "75 mil", "150 mil", "5 milhões e tal". These are plausible values; check them against the CCP.
- Variants for dates: "15/10/2026", "15-10-2026", "15.10.2026", "15/10/26", "15 de outubro", "15 de Outubro" (pre-AO capital), "dia 15", "a 15", "até dia 15", "próxima segunda", "segunda-feira que vem", "ontem", "anteontem", "há 3 dias", "daqui a 10 dias úteis", "no prazo de 10 dias", "fim do mês". Watch "10 dias" against "10 dias úteis", which is a real ambiguity in procurement deadlines. ISO "2026-10-15" appears rarely, from technical users. US-ordered "10/15/2026" appears rarely and is an error.
- Ordinals and article numbers: "art. 20º", "artigo 20.º", "art 20", "art.20", "20º", "20o", "20°" (degree sign instead of ordinal indicator), "nº 1 do art. 20", "al. a)", "alinea a" (missing accent).

### Gaps
- No Ciberdúvidas, Priberam or Portuguese official style-guide page came up in search. The EU Interinstitutional Style Guide Portuguese page (style-guide.europa.eu, section 370300) redirected and then returned 404, so I could not cite the official PT rule for "1 000" against "1.000" or for euro-sign position.
- I found no published frequency of number-format errors in Portuguese user text.

---

## 5. Brazilian vs European Portuguese differences, and informal register

### Takeaway
PT-BR procurement vocabulary is a different legal system. Lei 14.133/2021 has "licitação" with five modalities (pregão, concorrência, concurso, leilão, diálogo competitivo) plus direct contracting ("dispensa", "inexigibilidade"). PT-PT/CCP talks of "procedimento", "concurso público", "ajuste direto" and "consulta prévia". A Brazilian-styled question must be read as a variety marker, not mapped term by term. Informal register (no caps, no punctuation, run-ons, emphasis caps) is well documented in PT-BR UGC, at about 1.5–2% punctuation errors per token and about 0.8% case errors per token in product reviews.

### Cited Findings
- Lei 14.133/2021 modalities: pregão, concorrência, concurso, leilão, diálogo competitivo. Dispensa and inexigibilidade are not modalities but direct-contracting cases (art. 75 dispensa; art. 74 inexigibilidade, an open list). Convite and tomada de preços were abolished, and the Sistema de Registro de Preços is not a modality. — [ConLicitação](https://conlicitacao.com.br/quais-sao-as-modalidades-de-licitacao/); [ConLicitação 2026](https://conlicitacao.com.br/lei-14133-atualizada/)
- PT-BR dispensa limits under Decreto 12.807/2025, single source: R$ 130.984,20 for works and engineering, R$ 65.492,11 for other services and purchases. — [ConLicitação 2026](https://conlicitacao.com.br/lei-14133-atualizada/)
- Informal-register features in PT-BR UGC: missing capitals after punctuation and on proper nouns; capitals for emphasis; whole-text upper or lower case; missing punctuation and "uninterrupted" text that is hard to punctuate even for humans; emoticons (":)", ":-)", ":(") that need their own tokenizer handling. — [W15-4305](https://aclanthology.org/W15-4305.pdf)
- Per-token rates in two annotated review samples: punctuation errors 1.5% and 2.0%; case errors about 0.8%; slang 0.2% and 0.6% (counts in Section 1). — [W15-4305](https://aclanthology.org/W15-4305.pdf)
- A Lisbon classroom case study had a teacher converting a Brazilian-written Wikipedia text into European spelling, which shows PT-BR text reaching PT-PT readers. — [Revistas ULusófona](https://revistas.ulusofona.pt/index.php/rleducacao/article/view/1532/1258)

### Inferences
- PT-BR markers to inject as a contrast variant, or to detect: "licitação", "pregão (eletrônico)", "edital" (also used in PT-PT, but much more frequent in PT-BR), "dispensa de licitação", "inexigibilidade", "ata de registro de preços", "órgão", "você", "a gente" as subject, the gerund ("estou analisando" against PT-PT "estou a analisar"), proclisis ("me diga" against PT-PT "diga-me"), BR spellings ("eletrônico/econômico/Antônio" against PT-PT "eletrónico/económico/António"; "fato" against "facto"; "registro" against "registo"; "contato" against "contacto"), "R$", "CNPJ", "CPF" (BR IDs; the PT-PT equivalent is "NIF/NIPC").
- Lexical accent splits that are real differences, not errors: económico/econômico, académico/acadêmico, género/gênero, prémio/prêmio. A PT-PT writer typing "eletrônico" is showing a PT-BR influence or an autocorrect from a PT-BR keyboard locale. Phones defaulting to the PT-BR dictionary are a plausible noise source; unquantified.
- Informal-register transforms (to apply per question, not per token): all lowercase; no final "?"; question marks doubled or tripled ("??"); no commas; run-on joining of two questions with "e"; one ALL-CAPS emphasis word ("é OBRIGATÓRIO publicar?"); greeting and thanks ("bom dia, ... obg"); emoji (🙏, 😅) at the end. Start from the review rates: punctuation noise in about 1.5–2% of tokens, which in a 15–25 token question means most informal questions lose at least one punctuation mark.

### Gaps
- I found no study measuring how often PT-BR forms (gerund, "você", BR spellings) appear in PT-PT-authored text, or in text from Lusophone African users writing about Portuguese procurement.
- I found no data on emoji frequency in Portuguese questions to assistants.

---

## 6. Voice-to-text (ASR) artefacts in European Portuguese

### Takeaway
For PT-PT, the CAMÕES benchmark (INESC-ID/IST, ASRU 2025) is the authoritative source. **Zero-shot Whisper large-v3 averages 19.2% WER over five EP domains, and 12.5% after fine-tuning on 425 h of EP.** Whisper hallucinates on non-speech segments, and models trained on one variety degrade on others. I found no published PT-PT breakdown of ASR error types (homophones, numbers, punctuation). Those categories have to be modelled from general ASR behaviour.

### Cited Findings
- CAMÕES has 46.2 h of EP test data in 5 domains: read speech about 19.5 h, broadcast news 6.6 h, talks and lectures 3.0 h, conversational speech 6.8 h, sociolinguistic interviews 10.3 h. Models were fine-tuned or trained on 425 h of curated EP data. — [arXiv 2508.19721](https://arxiv.org/html/2508.19721v1)
- **WER on EP, domain-averaged: zero-shot WhisperLarge-v3 with VAD 19.2%; zero-shot Phi-4-Multimodal 21.7%; fine-tuned WhisperLarge-v3 12.5% (35% relative reduction).** An E-Branchformer trained from scratch comes within about 2 points absolute. — [arXiv 2508.19721](https://arxiv.org/html/2508.19721v1)
- Error behaviour: Whisper hallucinates frequently, partly due to noise in non-speech segments, most visibly in read speech and sociolinguistic interviews, and VAD reduces it. Fine-tuned models struggle most with young children (3–6) and the elderly (86+). Models fine-tuned on one Portuguese variety perform poorly on others. Prompting that names European Portuguese helped Phi-4 but not Whisper. — [arXiv 2508.19721](https://arxiv.org/html/2508.19721v1)
- All CAMÕES models were scored with the same Whisper-style text normaliser, so the reported WER **excludes** casing and punctuation errors. Real dictated text will be noisier than these WERs suggest. — [arXiv 2508.19721](https://arxiv.org/html/2508.19721v1)
- A 2025 EURASIP review reports Whisper at 5.11% WER on a 500-hour EP dataset. I could not verify the test split, and the figure conflicts with CAMÕES's 19.2% zero-shot average, probably because of domain (likely read or clean speech). Treat it as a clean-speech lower bound. — [DOAJ / EURASIP 2025](https://doaj.org/article/eba8888c4d1c443091722512eab58292)
- Fine-tuned Whisper-medium on Common Voice 11 (mixed PT varieties): 6.59% WER against 8.1% base. This is a model-card claim, not specific to PT-PT. — [PromptLayer model card](https://www.promptlayer.com/models/whisper-medium-portuguese)
- Whisper's punctuation prediction in Portuguese has been studied on NURC/SP (PT-BR spontaneous speech), the first such study for Portuguese. — [Repositório UFC](https://repositorio.ufc.br/handle/riufc/73941?locale=en)
- A transcription vendor claims PT-PT is harder than PT-BR (about 7–9% WER) because of "aggressive vowel reduction". The methodology is unpublished and the source is commercial, so it has low reliability. — [VexaScribe](https://vexascribe.com/compare/best-transcription-software-for-portuguese-audio)

### Inferences
- For dictated questions, the generator should target about **10–20% word-level corruption** in the "voice" condition (CAMÕES zero-shot about 19%, fine-tuned about 12.5%). On top of that, add casing and punctuation loss, which CAMÕES normalised away.
- PT-PT ASR noise classes to inject. **These are general ASR phenomena reasoned from PT-PT phonology. None is quantified by a PT-PT study.**
  - Homophones and near-homophones in PT-PT connected speech: há/à/a; "à" against "há" in "há prazo"; "concelho/conselho"; "cem/sem"; "censo/senso"; "cessão/sessão/secção"; "acento/assento"; "caçar/cassar"; "mas/mais"; "por/pôr"; "e/é"; "tem/têm"; "sem IVA" against "cem IVA".
  - Vowel reduction makes unstressed vowels drop: "p'ra", "dep'is", "concurso públic", "procediment" → wrong word boundaries, e.g. "ajuste direto" → "a juste direto" or "ajusta direto".
  - Acronyms spelled out or mis-segmented: "cê pê" / "CPE" for CP; "a dê" for AD; "cê cê pê" for CCP; "jo ue" / "joue"; "IVA" → "iva" / "Iva" / "e vá".
  - Numbers: ASR may output digits or words inconsistently ("setenta e cinco mil euros", "75 mil euros", "75000 euros", "75.000 €"), split them ("75 1000"), or mis-hear decimals ("um vírgula cinco milhões" → "1,5 milhões" / "1 vírgula 5 milhões").
  - Article numbers: "artigo vinte" → "artigo 20" / "artigo XX" / "art. 20º"; "número um do artigo..." / "n.º 1".
  - Missing punctuation and lowercase: no "?", one long run-on sentence, filler words kept ("pronto", "olhe", "portanto", "é assim", "tipo", "ok").
  - Hallucinated trailing text on silence (a Whisper behaviour per CAMÕES): e.g. a spurious "Obrigado." or a repeated phrase at the end.
  - Variety drift: a PT-BR-biased model renders PT-PT words in BR spelling or lexis ("econômico", "registro", "contato").

### Gaps
- I found no PT-PT ASR error-type analysis (substitution, deletion and insertion split, homophone confusion rates, number-rendering errors) for adult conversational speech. The 2014 PROPOR work on EP children's speech was not retrieved.
- I found no PT-PT data on how ASR renders money and dates (digits against words), or on punctuation and casing accuracy for EP dictation.
- I found no data on dictated questions to assistants (as opposed to broadcast or read speech) in PT-PT.

---

## Generator-ready summary (inferences, anchored to the sources above)

| Category | Unit | Casual typed | Careful typed | Voice (ASR) | Anchor |
|---|---|---|---|---|---|
| Total non-word spelling errors | per word | ~4.8% | ~1.8% | n/a | Gimenes C2/C1 (PT-BR) |
| Accent omission (share of errors) | share | ~45% | ~38% | low (ASR outputs accents) | Gimenes |
| ç→c (share of errors) | share | ~4–6% | ~6% | n/a | Gimenes |
| Letter omission / insertion / substitution / transposition | share | 24 / 9 / 6 / 0.2% | 17 / 10 / 13 / 4% | n/a | Gimenes C2/C1 |
| Glued words | share of errors | ~2% | ~2% | boundary errors common | Gimenes; Duran |
| Words with a single error | share | ~86% | ~92% | n/a | Gimenes |
| Real-word accent swaps (é/e, à/a, público/publico) | per token | ~1.2–2.0% | lower | homophones | Duran samples |
| Punctuation errors / missing | per token | ~1.5–2.0% | lower | near-total | Duran samples; CAMÕES normaliser |
| Case errors | per token | ~0.8% | lower | all lowercase | Duran samples |
| Slang / shorthand | per token | 0.2–0.6% | ~0 | ~0 | Duran samples |
| Word error rate | per word | n/a | n/a | 12.5–19.2% | CAMÕES (PT-PT) |
| Pre-AO spelling style | per question | unmeasured (my guess 15–25%) | same | n/a | Gap |
| PT-BR variety markers | per question | unmeasured | same | variety drift | Gap |
