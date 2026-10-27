# Extraction test v3 for TED, check B only: pass/fail criteria (written before the v3 sample is drawn)

v2 (CRITERIA-ted-v2.md) passed A and C for TED and failed B at 93.0 %. All 4 B misses were joins to a different
procedure of the same buyer with the same deadline, not parser errors (ted-v2/REPORT-v2.md). The builder relayed a yes
to a B-only v3 (2026-10-26), with the protocol the DR notices' test used in its v2: the join key written as code, the
threshold written before the draw, and a pair under it counted as «not joinable», outside B's denominator. Written
2026-10-26; its sha256 goes into BUILD-LOG.md in the commit that adds it; not edited after results.

## A and C
Not run again. They stand from v2: A PASS; C 1 652 / 1 653 = 99.9 % (99.7–100).

## Parser that v3 runs
adapters/ted/parse.py at the sha256 BUILD-LOG.md records with this file. Two changes since v2's parser (b277c007…):
- TED-XML: the form fields are read from the form whose CATEGORY is ORIGINAL (v2's one C disagreement: a translation's
  buyer name was read first). PR_PROC and the other coded data stay read from the coded section.
- A `title` field (TED-XML OBJECT_CONTRACT/TITLE, R2.0.8 TITLE_CONTRACT; eForms the root ProcurementProject's cbc:Name),
  needed by the join.
On the 400 development notices of v1 and v2 the change alters one value (v2 n=85's buyer name, now the ORIGINAL's) besides
adding the title. C passed on v2 with the old parser; v3 does not re-run C, so v3's numbers are for the new parser's B
fields (estimated_value, procedure_type, buyer, deadline, title) only.

## Population and sample
- TED contract notices (TED-XML code 3, eForms subtypes 16–18) with a deadline date and a Portuguese buyer, in every
  month except 2018-01 and 2026-01, without the 400 notices of v1's and v2's samples. B only applies to contract notices,
  so v3 draws from them alone (v2's 200 held 93).
- 100 TED-XML + 100 eForms, random.Random(20261029), each format sorted by member name (adapters/medicao/sample.py ted
  --contract-only --seed 20261029 --exclude adapters/medicao/ted/sample.json adapters/medicao/ted-v2/sample.json).
- Outputs in adapters/medicao/ted-v3/ (sample.json and parsed.json sealed before scoring).

## Check B, the join as code (adapters/medicao/score.py score_ted_b)
- BASE anúncios 2018–2026 (the dumps in Storage, sha256 checked on download; 2026 in data/raw_bytes/9605b59b…).
- Candidates: anúncios with the same DataLimitePropostas date as the TED deadline, and the same buyer: the NIF (last nine
  digits) when the TED notice gives one, else the official name with accents and case folded.
- Title containment: words of 4+ letters, accents and case folded, of the TED title and of the anúncio's
  descricaoAnuncio; containment = |words in both| / the smaller of the two word sets.
- **Threshold: 0.5.** Joinable: the best candidate has containment >= 0.5 and strictly more than any other candidate.
- Not joinable, counted by reason and left out of the denominator: no candidate with the same buyer and deadline;
  best containment under 0.5; two candidates tie.
- Compared on each joinable pair: the estimated value with PrecoBase (equal to the cent), and the procedure type (open
  with Concurso público, restricted with Concurso limitado por prévia qualificação, negotiated with call with
  Procedimento de negociação).
- PASS if >= 95 % of compared values agree; every disagreement is listed with both values and classified (parser error /
  the sources differ / wrong join), the text quoted. Reported too: the join rate and each not-joinable count, with Wilson
  95 % intervals.
- The threshold 0.5 was set with v2's pairs seen (true pairs at 1.00, the 4 wrong ones at 0.00–0.22); v2's notices are
  development data and are excluded from v3.

## Verdict, applied as written
B passes: with v2's A and C, TED's extraction is measured. B fails: reported with its numbers; no v4 is claimed from these
criteria.
