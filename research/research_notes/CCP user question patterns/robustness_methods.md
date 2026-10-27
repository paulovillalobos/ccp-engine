# Robustness methods for a small fine-tuned LLM extracting structured facts from noisy, vague and false-premise questions

Setting: AMALIA 9B (Portuguese), LoRA, trained only on code-generated examples, maps a question to a JSON of facts (enum fields, a number, a date) and leaves out what is not stated. Observed: 100% on held-out template wordings, 10-15% exact match on 40 hand-written real-style questions. That is template overfitting. The project forbids model-written labels.

Research budget note: about 20 tool calls. Numbers below were read from the papers or their abstracts. Items I know of but did not open this session are listed under Gaps and marked unverified.

## 1. Synthetic noise injection: typo models, rates, and whether they transfer to real noise

### Takeaway
Character-level synthetic noise reliably makes models robust to the same kind of noise. Whether it transfers to real human noise depends on the noise model. Two results point different ways. Belinkov & Bisk found almost no transfer from scramble or keyboard noise to natural errors in MT. NAT found that a plain uniform insert/delete/substitute model at 10% recovered most of the loss on real OCR and misspelling noise in NER. The robust recipe is a mix of noise types, plus a small amount of "natural-like" noise: phonetic substitutions, omissions and, for Portuguese, accent stripping. Clean copies stay in the mix, and noise rates are kept at 10-30%.

### Cited Findings
- **Synthetic noise does not transfer by itself (MT).** Belinkov & Bisk (ICLR 2018) tested Swap (adjacent letters), Mid (scramble inner letters), Rand (scramble the whole word), Key (adjacent keyboard key) and Nat (real errors from Wikipedia edits and learner corpora). A French charCNN trained clean scores 42.54 BLEU clean and 17.42 on Nat. Training on Swap, Rand or Key alone gives only 16.4-16.9 on Nat, about the clean baseline. Rand+Key gives 18.71 on Nat. Only training that includes Nat helps on Nat: Nat alone gives 36.00, and Rand+Key+Nat gives 31.77 on Nat with at least 35.25 on every synthetic type. Nat-only training collapses on synthetic noise (1.03 on Rand). — [Belinkov & Bisk 2018, ar5iv](https://ar5iv.labs.arxiv.org/html/1711.02173)
- Belinkov & Bisk say the most common natural errors are phonological changes and omissions, which scramble and keyboard generators do not produce. They argue that "good synthetic errors will likely require more explicit phonemic and linguistic knowledge." Noise classes did not help each other except under mixed training. — [Belinkov & Bisk 2018](https://ar5iv.labs.arxiv.org/html/1711.02173)
- Clean text also suffers: Rand+Key+Nat drops clean BLEU from 42.54 to 36.97, and Nat-only drops it to 28.77. — [Belinkov & Bisk 2018](https://ar5iv.labs.arxiv.org/html/1711.02173)
- **A different synthetic recipe does transfer (MT).** Karpukhin, Levy, Eisenstein & Ghazvininejad (W-NUT 2019) trained on a mix of simple synthetic noise types and tested on natural noise from frequent Wikipedia edit corrections. The model never saw natural noise or its distribution. It became "much more tolerant" of natural spelling errors at no cost on clean text. Synthetic noise was in training only and natural noise in test only. — [Karpukhin et al. 2019, ACL Anthology](https://aclanthology.org/D19-5506/); [summary](https://deepai.org/publication/training-on-synthetic-noise-improves-robustness-to-natural-noise-in-machine-translation)
- **Sequence labelling (closest to slot/fact extraction): NAT.** Namysl, Behnke & Köhler (ACL 2020) used a vanilla character noise model: insertion, deletion and substitution equally likely, replacement characters drawn uniformly, noise level η_train = 10%. The best range was η between 10% and 30%, "roughly where a human could still infer the label." Each sentence is paired with one noisy copy at equal weight (α = 1.0). — [NAT, ar5iv](https://ar5iv.labs.arxiv.org/html/2005.07162)
- NAT results on English CoNLL-03 (FLAIR+GloVe):
  - Baseline: clean 92.05, real OCR 76.44, misspellings 75.09 / 87.57.
  - With NAT data augmentation: clean 92.56, OCR 84.79, misspellings 83.57 / 90.50.
  - With BERT: OCR rises from 68.23 to 79.34, and clean stays about the same (90.91 to 90.84).
  - Training on the real OCR error distribution helped "only slightly more" than the synthetic model.
  — [NAT](https://ar5iv.labs.arxiv.org/html/2005.07162); [ACL Anthology](https://aclanthology.org/2020.acl-main.138)
- **Noisy slot filling with human-annotated noise (Noise-SF).** Five real noise types, 861 utterances each.
  - A BiLSTM trained clean scores 95.8 clean F1, and much lower on noise: typos 64.3 (−31.5), speech/ASR 82.1, paraphrase 88.1, verbosity 82.2, simplification 85.9.
  - BERT averages 82.6 over the noise sets. Typos again cost the most (−28.6).
  — [Noise-SF, ar5iv 2310.03518](https://ar5iv.labs.arxiv.org/html/2310.03518)
- In Noise-SF, rule-based character augmentation (CharAug) gave the best gain on typos: a relative denoising rate of 38.1%, but only 15.7% overall.
  - Word-level insert, delete and substitute gave small or negative gains on sentence-level noise (InsertWord −2.2% on speech).
  - The authors conclude rule-based methods struggle to simulate sentence-level noise.
  - Feature-level methods transferred better: adversarial training reached ρ = 22.2% on sentence-level noise, TokenCut reached 19.4% overall, and CharAug+TokenCut reached 27.0%.
  - On BERT, the methods were not effective for sentence-level noise, and some were negative.
  - Caveat: small, crowdsourced benchmark.
  — [Noise-SF](https://ar5iv.labs.arxiv.org/html/2310.03518)
- Noise-BERT (2024) says rule-based augmentation generalises poorly to unknown noise, and uses noise-alignment pre-training plus contrastive and adversarial fine-tuning instead. — [Noise-BERT, arXiv 2402.14494](https://arxiv.org/html/2402.14494v3)
- **Label noise is a related warning.** NoiseBench (EMNLP 2024) shows that simulated corruption is "far easier to handle than real noise." Real noise makes plausible mistakes, for example labelling "Swiss" as LOC, while simulated noise makes implausible ones, for example "Grand Prix" as LOC. That paper is about label noise, but the lesson carries over: implausible synthetic corruptions overstate robustness. — [NoiseBench, arXiv 2405.07609](https://arxiv.org/html/2405.07609v2); [GitHub](https://github.com/elenamer/NoiseBench)

### Inferences
- Use a mixture of typo operators, not one. Per-character operators: keyboard-adjacent substitution (Portuguese/ABNT layout), deletion, insertion, adjacent transposition.
- Add natural-like operators, the part that gave transfer in Belinkov & Bisk:
  - accent and cedilla stripping (é→e, ç→c, ã→a), which is the most common real Portuguese "error" and costs nothing to generate;
  - phonetic confusions (ss/ç/s, x/ch, ão/am, lh/li);
  - omitted words and vowels;
  - casing loss;
  - common abbreviations (q, pq, vc, nº, "art.", "mil" for thousands, "1,5M");
  - number and date surface forms (10.000 / 10 000 / 10k / dez mil; 1/10 / 1 de outubro / out.).
- Rates: noise roughly 10-30% of words or characters per noisy example (NAT's optimum). Keep a clean copy of each example (NAT used 1:1). Higher rates and natural-only noise cost clean accuracy (Belinkov & Bisk clean BLEU 42.5 → 37.0 / 28.8).
- Typo noise addresses only part of the gap. Noise-SF shows paraphrase, verbosity and simplification noise are not fixed by character rules. The 10-15% real-question exact match is far more likely driven by structural and wording mismatch (Section 2) than by typos.
- For a 9B LLM with a subword tokenizer, character noise mostly breaks token boundaries. The "vanilla noise transfers" evidence (NAT, LAUG) comes from 2020-era encoders, so expect smaller but still positive gains.

### Gaps
- Exact BLEU numbers and noise probabilities in Karpukhin et al. 2019: the PDF could not be rendered here (poppler not installed).
- No Portuguese-specific study of typo or accent-stripping augmentation was found. Its value is inferred.
- TextFlint, nlpaug and TextAttack documentation were not opened this session (unverified). TextFlint is a multilingual robustness toolkit with typo, keyboard, OCR and spelling transforms, and nlpaug offers KeyboardAug, OcrAug and RandomCharAug. Use them as a reference for operator lists, not as evidence of transfer.
- No study found for 7-9B decoder LLMs that measures synthetic-to-natural typo transfer under LoRA specifically.

## 2. Paraphrase and structure diversity without a teacher model; template data vs real data

### Takeaway
Template- and grammar-generated data can get within about 5-6 points of human-paraphrased data, but only with very rich, compositional templates plus filtering. The main failure mode is a distribution mismatch in both wording and structure: "what is asked" differs as well as "how it is phrased." This is exactly the 100% → 10-15% gap observed. The fix with the best evidence is to collect unlabeled real-style questions, measure the mismatch, and grow the grammar to cover it. Adding more instances of the same templates does not fix it.

### Cited Findings
- **Template and paraphrase data mismatches real usage.** Herzig & Berant (EMNLP 2019) find that collecting data by generating canonical utterances and then paraphrasing them creates two gaps: (a) which logical forms appear and (b) how language is phrased.
  - Paraphrase-based collection: 51.3% accuracy on the true distribution.
  - Their alternative, which labels real unlabeled utterances with a detection or paraphrase model plus crowd checking: 70.6%.
  — [Herzig & Berant 2019](https://aclanthology.org/D19-1394/); [arXiv](https://arxiv.org/abs/1908.09940v1)
- **Purely synthetic can get close if templates are rich.** AutoQA (EMNLP 2020) generates questions from schema and data, with template-based grammars and filtered automatic paraphrase.
  - Schema2QA: 62.9% logical-form accuracy on natural questions, 6.4 points below expert annotation plus crowd paraphrase.
  - Overnight: 69.8% answer accuracy, 16.4 points above prior zero-shot and 5.2 points below training on human data.
  - The earlier Schema2QA pipeline relied on templates with a few manual annotations per attribute and about 2% manually paraphrased data.
  - Note: AutoQA's paraphraser is a neural model (BART), which the project's no-teacher rule would exclude for labels. Its grammar side is the part that transfers to this setting.
  — [AutoQA, ACL Anthology](https://aclanthology.org/2020.emnlp-main.31); [arXiv PDF](https://arxiv.org/pdf/2010.04806)
- **Paraphrase and verbosity are distinct noise axes.** In Noise-SF, a clean-trained slot filler loses 7.7 F1 on paraphrase, 13.6 on verbosity and 9.9 on simplification. Simple word insert, delete and substitute rules do not recover it. — [Noise-SF](https://ar5iv.labs.arxiv.org/html/2310.03518)
- **Perturbation-augmented training for dialog NLU (LAUG, ACL 2021).** Four augmentations: word perturbation, text paraphrasing, simulated speech-recognition errors, speech disfluency.
  - On MultiWOZ 2.3, BERT averages 86.95 F1 over perturbed sets trained on original data and 91.06 trained on augmented data. CopyNet goes from 80.34 to 88.56.
  - Clean-set F1 changes by under 1 point.
  - On 240 real spoken user utterances, BERT rises from 65.22 to 69.12 and MILU from 63.55 to 66.77. Real data stays much harder than any augmented set.
  — [LAUG, arXiv HTML](https://arxiv.org/html/2012.15262v3); [ACL Anthology](https://preview.aclanthology.org/setup/2021.acl-long.192)
- **Diversity over volume.** "Data Diversity Matters for Robust Instruction Tuning" (Findings of EMNLP 2024) reports a quality-diversity trade-off. More diverse data "significantly improves the worst case instruction following performance." — [Bukharin et al., arXiv 2311.14736](https://arxiv.org/abs/2311.14736)

### Inferences
- **Diagnosis.** A 100% held-out-template score with 10-15% on real questions means the held-out split leaks template skeletons. Re-split by template ID and by slot combination, then report both. A held-out wording drawn from the same grammar is not a test of generalisation. This follows Herzig & Berant's "two mismatches."
- **Generator design without a teacher LLM.** Use a compositional grammar rather than sentence templates:
  - **Separate content from surface.** First sample the fact set: which fields are present, absent or ambiguous, including combinations never seen together. Then realise each fact through many independent surface realisers:
    - lexical synonyms per enum value, including colloquial and wrong-but-common names;
    - several syntactic frames per fact (noun phrase, relative clause, prepositional phrase, fronted topic, parenthetical);
    - number and date formatters.
  - **Vary order and wrapping.** Permute fact order. Add chit-chat or context prefixes and suffixes for verbosity ("Boa tarde, trabalho numa câmara e tenho uma dúvida..."). Allow telegraphic and simplified forms with no verb. Use multi-sentence questions where facts are split across sentences, and questions where a fact is implied by a domain phrase rather than named.
  - **Distractors.** Add numbers and dates that are not the target fact (a year in a law name, an article number) so the model learns not to grab every number. This targets over-extraction.
  - **Real wording.** Mine real phrasing from the 40 hand-written questions and from public forum text (unlabeled) into the grammar's lexicon. Do not train on those 40.
- **How much diversity.** No paper gives a threshold. Use operational proxies:
  - the number of distinct skeletons (frame × order × wrapper);
  - type/token and distinct-n-gram ratios;
  - nearest-neighbour similarity between real test questions and the generator's output (embedding or n-gram);
  - grow the grammar until real questions are not outliers.
- **Back-translation without an LLM.** Rule-based round trips are possible (for example, convert passive to active), but no evidence was found that they help. Treat it as low priority.

### Gaps
- MASSIVE (51 languages including pt-PT, slot filling), ATIS and SNIPS noise studies, and the Overnight (Wang, Berant & Liang 2015) grammar-plus-paraphrase method were not opened this session (unverified). They are relevant background on cross-lingual slot filling and grammar-generated data.
- No quantitative "N templates needed" rule exists in the sources found. Evidence on the needed amount of diversity is weak.
- No study found on purely rule-based (no-neural) paraphrase transferring to real questions for LLM fine-tuning.

## 3. Vagueness and false premises: abstention, "unknown" vs omission, clarification, contradiction markers

### Takeaway
Real users often embed false or unsupported premises: about 25% of naturally occurring forum questions in CREPE. Models can learn to flag them from a modest number of examples (about 256 in FalseQA) if ordinary questions are mixed in so they do not over-reject. For an extractor, this supports an explicit, schema-level representation of "stated but ambiguous" and "stated but contradictory," kept distinct from "not stated" (omitted). Generating these cases with code is feasible because the contradiction is constructed, so the label is known.

### Cited Findings
- **CREPE (ACL 2023).** 25% of real information-seeking questions from online forums contain false presuppositions. Baselines detect presuppositions moderately well but struggle to judge whether they are true, mainly because of evidence retrieval. — [CREPE, ACL Anthology](https://aclanthology.org/2023.acl-long.583); [ar5iv](https://ar5iv.labs.arxiv.org/html/2211.17257)
- **FalseQA (ACL 2023).** 2,365 human-written false-premise questions, each with an explanation and a corrected true-premise version.
  - Fine-tuning on a moderate number of examples (about 256) let models identify false-premise questions and produce rebuttals.
  - Mixing a few general questions into training kept performance on both false-premise and normal questions.
  - The authors argue models are not missing the knowledge, only the behaviour.
  — [Hu et al. 2023, ACL Anthology](https://aclanthology.org/2023.acl-long.309); [arXiv](https://arxiv.org/abs/2307.02394v1)

### Inferences
- **Use a three-way distinction per field.** Omitted means not mentioned. Explicit value means stated. `AMBIGUOUS` or `CONFLICT` means mentioned but not resolvable, or two incompatible values given. Collapsing "mentioned but vague" into omission throws away a signal the downstream engine needs, for example to ask a clarifying question. Emitting a guessed value is over-extraction. A marker can be generated by code with certainty: the generator knows when it inserted two different values or a vague quantifier ("uns milhares", "no início do ano").
- **False premises are mostly not the extractor's job.** "Is the false premise true?" needs the law and the data (CREPE's hard part). The extractor should faithfully record what the user asserted, for example `user_asserted_regime: X`. The rule engine then checks it against the law.
  - This fits the project rule that code applies the law and AI only decomposes.
  - The useful marker for the extractor is internal inconsistency within the question, which is detectable from the text alone.
- **Include negative and abstention examples in proportion.** FalseQA's lesson is to mix them with ordinary questions to avoid over-flagging. A reasonable start is 10-20% vague or conflict examples. This is not from a paper; tune it on the dev set while watching false-flag rates.
- **Clarification questions belong downstream.** If the system wants to ask a clarifying question, generate it deterministically from the `AMBIGUOUS` field list, not with the extractor.

### Gaps
- ClariQ (Aliannejadi et al. 2020), Qulac (2019), AmbigQA (Min et al. EMNLP 2020) and SQuAD 2.0 (Rajpurkar et al. 2018, unanswerable questions) were not opened this session (unverified). They are the standard references for clarification need, ambiguity and abstention.
- No paper found that directly compares an "unknown" token vs omission vs an ambiguous marker for JSON extraction with LLMs. The recommendation rests on design reasoning, not direct evidence.
- Exact FalseQA accuracy numbers were not retrieved.

## 4. LoRA-specific evidence: quantity vs diversity, forgetting, examples per noise type

### Takeaway
LoRA at standard ranks learns less from the target data than full fine-tuning but forgets less. Its limiting factor is the coverage of the training distribution, which favours diverse over repetitive data. Small mixed-in sets of general or old-task examples are an established guard against narrowing behaviour (FalseQA). No source gives a per-noise-type example count.

### Cited Findings
- **LoRA Learns Less and Forgets Less** (Biderman et al., TMLR 2024; about 100K instruction pairs and about 20B tokens of continued pre-training on code and maths):
  - at standard low ranks, LoRA substantially underperforms full fine-tuning on the target domain;
  - it better preserves performance outside the target domain;
  - full fine-tuning learns weight perturbations with 10-100x higher rank than typical LoRA configurations;
  - LoRA can match full fine-tuning in instruction tuning at higher ranks.
  — [arXiv 2405.09673](https://arxiv.org/abs/2405.09673v2); [TMLR / mlanthology](https://mlanthology.org/tmlr/2024/biderman2024tmlr-lora)
- A follow-up reports that LoRA's lower forgetting is a property of LoRA itself, not just a result of underfitting. — [LoRA vs Full Fine-tuning: An Illusion of Equivalence, arXiv 2410.21228](https://arxiv.org/pdf/2410.21228)
- Diversity improves worst-case robustness in instruction tuning. — [Bukharin et al.](https://arxiv.org/abs/2311.14736)
- About 256 examples were enough to teach false-premise detection, and mixing in general questions prevented over-application. — [FalseQA](https://aclanthology.org/2023.acl-long.309)

### Inferences
- **Diversity over volume.** With limited LoRA capacity, thousands of near-duplicate template instances waste capacity and teach the template. Deduplicate by skeleton and cap instances per skeleton (for example ≤3-5). Spend the budget on more skeletons and fact combinations.
- **Examples per noise type: no sourced number exists.** A defensible start, by analogy with FalseQA (about 256) and NAT (1 noisy copy per clean example):
  - a few hundred examples per behaviour class (typo, accent-stripped, verbose, telegraphic, distractor-number, ambiguous, conflict);
  - every clean skeleton also seen in at least one noisy form.
  Then run ablations, adding or removing one class at a time.
- **Forgetting.** If AMALIA must keep its general Portuguese ability, or earlier tasks from v1-v4 adapters, replay a small fraction of earlier-task examples, for example 5-10%. LoRA already limits forgetting, so the main risk is behavioural narrowing (always emitting JSON, over-extracting), not knowledge loss.
- **Rank.** If the task's surface diversity grows a lot, the Biderman results suggest that higher rank (or more target modules) may be needed for LoRA to absorb it. Test r = 16 vs 64 on the real-question dev set.

### Gaps
- No study found that gives examples needed per noise type for LoRA on 7-9B models.
- No direct evidence on the right replay ratio for LoRA multi-task extraction adapters.

## 5. Evaluation design: held-out noise types, hand-written sets, per-field metrics, over-extraction

### Takeaway
The strongest evaluation pattern in the literature has three parts:
- a clean set;
- a set of real, human-written or human-annotated noisy inputs, kept separate by noise type;
- held-out noise types the training never saw.

Report the drop and recovery for each type. Real inputs stay harder than any synthetic proxy (LAUG real users ~65-69 F1 vs ~89-93 on augmented sets), so the hand-written set is the score that matters. Synthetic test sets mainly serve regression testing.

### Cited Findings
- **Noise-SF pattern.** Every clean test utterance has a human-annotated noisy counterpart for each of 5 noise types (861 × 5). Results are reported per type plus an average and a "relative denoising rate." — [Noise-SF](https://ar5iv.labs.arxiv.org/html/2310.03518)
- **LAUG pattern.** Report the original score, the score on each perturbation, the average, the drop, and the recovery after augmented training. Separately, report a small real-user set (240 utterances), which stays much harder than the synthetic perturbations. — [LAUG](https://arxiv.org/html/2012.15262v3)
- **Cross-noise matrix.** Belinkov & Bisk train on each noise type and test on every type, including natural noise. This exposes when gains come only on the same noise type. — [Belinkov & Bisk](https://ar5iv.labs.arxiv.org/html/1711.02173)
- **Real vs simulated noise.** NoiseBench shows simulated noise overstates robustness and argues for evaluating on real noise. — [NoiseBench](https://arxiv.org/html/2405.07609v2)
- **Real distribution vs paraphrase.** Herzig & Berant evaluate on the true utterance distribution, not on paraphrases of generated forms; the gap was 51.3% vs 70.6%. — [Herzig & Berant](https://aclanthology.org/D19-1394/)

### Inferences
Recommended evaluation design:

1. **Splits.**
   - (a) In-grammar held-out, split by skeleton ID and by unseen field combinations, not by random instance.
   - (b) Held-out noise operators never used in training, for example OCR-style confusions (rn/m, l/1), ASR-style homophones, an unseen abbreviation lexicon, unseen wrapper or verbosity frames.
   - (c) The hand-written real-style set. Expand it from 40 to at least 150-200 to cut the confidence interval: at n = 40 the 95% CI on 12% is roughly ±10 points. Tag each item by phenomenon (typo, accent, verbose, telegraphic, vague, conflict, distractor number, false premise).
   - (d) A frozen, never-inspected final test slice of the hand-written set, used only at milestones.
2. **Metrics.**
   - Per-field precision, recall and F1, with each field-value pair as the unit.
   - Exact JSON match as a secondary metric.
   - **Over-extraction rate**: the share of predicted fields not supported by the question, i.e. hallucinated facts. Report it separately, because false positives are worse than omissions for a law engine.
   - **Omission rate**: stated facts the model missed.
   - For ambiguous or conflict markers: precision and recall of the marker, plus the false-flag rate on clean questions.
   - Value-normalisation accuracy for numbers and dates, separated from field detection.
3. **Report as a matrix.** Training mixture × test noise type (Belinkov-style), plus clean vs noisy drop and recovery (LAUG-style). The decision metric is real-set per-field F1 with an over-extraction ceiling.
4. **Behaviour tests.** CheckList-style invariance and directional tests, generated by code:
   - **Invariance:** accent stripping, typos and reordering must not change the JSON.
   - **Directional:** adding "não" or a second conflicting value must change it in the expected way.

   These are cheap, code-labelled and diagnostic.

### Gaps
- CheckList (Ribeiro et al., ACL 2020) was not opened this session (unverified). It is the standard reference for invariance and directional behaviour tests.
- No published standard for measuring over-extraction in LLM JSON extraction was found. The metric definition above is a proposal.
- The confidence-interval figure is a standard binomial approximation, not from a source.
