# TED extraction test v1: result (CRITERIA-ted-contratos-v1.md applied as written)

Sample: 100 TED-XML + 100 eForms notices with a Portuguese buyer (sample.json d12f6a29…, parsed.json 09df8fa4…, sealed in
X.1). Blind answers: blind/batch-00..39.json (reader-b-cli, model model-b, read-only sandbox, empty
working directory), saved before scoring. Scores: score.json, from adapters/medicao/score.py (sha256 7c32e314…).

**Verdict: TED does not pass v1.** C fails (97.4 %, line 98 %) on a parser error in eForms; per the criteria the parser is
fixed and a new sample is drawn (v2) before any pass is claimed. B was not run (the BASE anúncios dumps are in Storage,
which the CLI cannot open while the database is read-only).

## A. Coverage (share of the 200 with a value; Wilson 95 %)
| field | share | interval | line |
|---|---|---|---|
| dispatch_date | 200/200 | 98.1–100 | PASS |
| notice_type | 200/200 | 98.1–100 | PASS |
| notice_id | 200/200 | 98.1–100 | PASS |
| buyer_name | 200/200 | 98.1–100 | PASS |
| main_cpv | 200/200 | 98.1–100 | PASS |
| deadline_date (contract notices) | 81/82 | 93.4–99.8 | PASS |
| buyer_country | 200/200 | 98.1–100 | — |
| buyer_nuts | 194/200 | 93.6–98.6 | — |
| contract_type | 192/200 | 92.3–98.0 | — |
| procedure_type | 190/200 | 91.0–97.3 | — |
| buyer_nif | 174/200 | 81.6–91.0 | — (TED-XML rarely carries it) |
| estimated_value | 124/200 | 55.1–68.4 | — (optional in both forms) |
| deadline_time | 83/200 | 34.9–48.4 | — (only notices with a deadline) |

A passes. dispatch_date has a value in all 200, but in eForms result notices it is the wrong value (C below).

## C. Code against the blind reader (values both give)
- All: 1 597 / 1 640 = 97.4 % (96.5–98.0). **FAIL.**
- TED-XML: 781 / 781 = 100 % (99.5–100). eForms: 816 / 859 = 95.0 % (93.3–96.3).
- Without dispatch_date: 1 436 / 1 440 = 99.7 % (99.3–99.9).
- Per field: dispatch_date 161/200; deadline_date 82/83; deadline_time 82/83; buyer_name 199/200; buyer_nif 172/173;
  estimated_value 119/119; buyer_country 200/200; contract_type 192/192; main_cpv 200/200; procedure_type 190/190.

### The 43 disagreements, settled from the XML
- **39 × dispatch_date, code error** (eForms result notices, subtypes 29, 30, 33, 38, 39). The parser takes the first
  `IssueDate` anywhere in the document; in result notices that is
  `ext:UBLExtensions/…/efac:NoticeResult/efac:SettledContract/cbc:IssueDate` (the contract's conclusion date, BT-145),
  which comes before the notice's own `ContractAwardNotice/cbc:IssueDate` (BT-05). Example n=101:
  `SettledContract/IssueDate 2019-03-15+01:00`, `ContractAwardNotice/IssueDate 2025-02-20Z`; the reader gave 2025-02-20.
  Every one of the 39 is this; the reader was right in all of them.
- **2 × buyer (n=127), code error by omission**: a joint procurement with six `cac:ContractingParty` (ORG-0002, 0003,
  0005, 0007, 0009, 0010). The parser gives the first (Águas de Santo André, S. A., 505600005); the reader listed all six.
  The first agrees; v1 never said which buyer to give when there are several.
- **2 × deadline (n=125), text ambiguous**: a change notice whose coded `TenderSubmissionDeadlinePeriod` says
  2025-09-22 19:00:59+01:00 while its `efbc:ChangeDescription` reads «Prorrogação do prazo para apresentação de
  propostas - 06/10/2025 - 19h00». The parser read the coded field; the reader read the change text. The source
  contradicts itself.
- Reader errors: 0.

## What v2 changes (written before its sample, see CRITERIA-ted-v2.md)
- dispatch_date in eForms: the `cbc:IssueDate` that is a direct child of the root.
- buyer: stated as the first buyer (first ContractingParty in eForms, ADDRESS_CONTRACTING_BODY in TED-XML) for both the
  parser and the reader.
- A fresh sample from the same population without these 200 notices, which are now development data.
