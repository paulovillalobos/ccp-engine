# Extraction test v2 for TED: pass/fail criteria (written before the v2 sample is drawn)

v1 (CRITERIA-ted-contratos-v1.md) failed check C for TED on a parser error (ted/REPORT-v1.md). As v1 says, the parser
is fixed and a new sample is drawn. Everything in v1 holds for TED unless changed here. Written 2026-10-26, after v1's
result and before v2's sample; its sha256 goes into BUILD-LOG.md in the commit that adds it; not edited after results.
BASE contratos stays under v1 (its sample is not drawn yet).

## What changed, and why
- Parser (adapters/ted/parse.py, new sha256 in BUILD-LOG.md): the eForms dispatch date is the `cbc:IssueDate` directly
  under the root (BT-05). v1 read the first IssueDate anywhere, which in result notices is the SettledContract's (BT-145).
  On v1's 200 notices the fix changes those 39 values and no other field.
- The buyer, when a notice names several, is the first: the first `cac:ContractingParty` in eForms (as v1's parser
  already did), ADDRESS_CONTRACTING_BODY in TED-XML. The reader is told the same (blind_read.py), since v1 never said.
- Scoring: deadline_time is compared as hour and minute (v1 compared the first five characters, so «19:00:59+01:00»
  and «19h00» differed).
- Nothing else changed: same fields, same checks and lines, same reader (reader-b-cli, model-b, read-only sandbox,
  empty working directory).

## Population and sample
- The v1 population (Portuguese buyer, all months except 2018-01 and 2026-01) without the 200 notices of v1's sample,
  which are now development data. 100 TED-XML + 100 eForms drawn with random.Random(20261028), each format sorted by
  member name (adapters/medicao/sample.py ted --seed 20261028 --exclude adapters/medicao/ted/sample.json).
- Outputs in adapters/medicao/ted-v2/ (sample.json and parsed.json sealed before the blind reading).

## Checks and lines (as v1)
- A: TED dispatch_date, notice_type, notice_id, buyer_name, main_cpv, and deadline_date for contract notices, each >= 95 %.
- B: against BASE anúncios as v1 says, when Storage is readable; until then NOT RUN, and TED cannot be called measured.
- C: >= 98 % agreement on values both give; every disagreement settled by quoting the XML and classified.
- Wilson 95 % intervals.

## Verdict, applied as written
A, B and C pass: TED's extraction is measured. C fails again: no third attempt is claimed from these criteria; the
failure is reported with its numbers.
