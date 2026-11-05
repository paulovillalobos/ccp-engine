# CCP Engine — system plan (2026-11-05, DECISIONS D78)

What we are building: an open-source system that checks every Portuguese public procurement procedure against the law in
force on its date (the CCP and the EU directives it transposes) and shows the proof of every answer. The law is read into
rules once, by two independent model families that must agree blind; code applies the rules to the facts of each
procedure. No model is called when a user asks.

Go public only when every layer below is built (Phase 7).

## 1. The layers

| # | Layer | What it does | AI? | Runs on | State today |
|---|---|---|---|---|---|
| L1 | Law store | the CCP and the EU directives, every version with its dates, from the DR and the Publications Office | no | files in the repo | done: 373 acts, 36 533 passages, 2008–2026 |
| L2 | Rule reading | AMALIA proposes each rule from the law's words; a second family checks it blind; a rule settles only when both agree | yes | GPU, only when the law changes | done with Reader B as checker: 318 real-law rules settled, exam 82 % (D77) |
| L3 | Proof log | every proposal, review and settlement hash-chained; `verify.py` re-proves all of it | no | files in the repo | done: 1 792 events, verify ok |
| L4 | Ingest | BASE (IMPIC), TED and DR notices → units and facts | no | CPU, daily | done for history: 3.14 M units, 12.6 M facts in Supabase; daily job written, not deployed |
| L5 | Derived facts | facts the rules need, computed from stored facts (e.g. bid days = data_limite_propostas − data_publicacao_anuncio) | no | CPU | missing |
| L6 | Engine run | every procedure's facts × the rules in force on its date → a verdict with citation and manifest | no | CPU, batch then daily | engine done (`engine/evaluate.py`); not run over Supabase |
| L7 | API | read verdicts, laws, rules, proof; check a procedure sent as facts or OCDS | no | container | built (`tools/serve.py`, Cloud Run recipe); reads files, not Supabase; no OCDS |
| L8 | Frontend | search a procedure → each rule's verdict, the law quoted, the proof, dispute | no | static site + API | mockup only |

## 2. Where it lives (sovereign by design)

| What | Now | Target | Why |
|---|---|---|---|
| Law, rules, proof log | GitHub repo (private) | GitHub repo (public, Apache-2.0) | anyone can rerun verify |
| Facts and verdicts | Supabase Pro, eu-west-1 (AWS Ireland) | Supabase now; Postgres on Scaleway or OVHcloud later | data in the EU now; an EU provider later, with no code change (plain Postgres) |
| Reader: AMALIA CCP | Modal (`amalia-weights` + `amalia-lora/amalia-ccp-lei-v16`) | Scaleway GPU, Paris | Portuguese model on a European host; only the CCP adapter is copied, urban licensing (`amalia-rjue-v6`) and saneamento stay on Modal |
| Checker | Reader B (model-b, the person's subscription) | Mistral open model on the same Scaleway GPU | European family, independent of AMALIA, no subscription usage |
| Ingest + engine batch | Modal CPU | Scaleway CPU | same code; one provider for compute |
| API | Cloud Run recipe (europe-southwest1) | Scaleway Serverless Containers | EU provider |
| Frontend | — | static build on Scaleway (or the API's container) | EU provider |

## 3. Data flow

```
DR + Publications Office ──► L1 law store ──► L2 AMALIA proposes ─┐
                                                                ├─► settled rule (L3 log) ─┐
                                    Mistral checks blind ──────┘                          │
BASE + TED + DR notices ──► L4 facts (Supabase) ──► L5 derived facts ──► L6 engine ◄──────┘
                                                                            │
                                                     verdicts + manifests (Supabase)
                                                                            │
                                                       L7 API ──► L8 frontend ──► user
```

A user's request reads stored verdicts, or sends facts for a fresh check: database reads and code, no model.

## 4. Phases (in order; each ends with verify ok and a commit)

**Phase 1 — The GPU to Scaleway, and the checker to Mistral there (L2)** (the person, 2026-11-05: no reason to set the
checker up twice).
1. A Scaleway project in Paris with an L40S GPU (the person creates the account and API key).
2. Copy the base weights and `amalia-ccp-lei-v16` from Modal; AMALIA gives the same answers on a fixed sample.
3. Mistral open model (Mistral Small) downloaded straight there as `leitor:c`, a registered principal of a third family;
   reader code beside `readers/leitor_b_cli.py`.
4. Mistral reads blind every prompt of the settled rules and of the exam (rounds 11–16); a rule stays settled only where
   AMALIA and Mistral agree.
5. Done when: both readers run on Scaleway, the settled count under AMALIA + Mistral is known, verify ok, the refresh uses
   them, Reader B retired. Modal keeps only rjue and saneamento.

**Phase 2 — Derived facts (L5).**
1. The engine's fields mapped to Supabase's: `data_inicio_procedimento` ← `data_publicacao_anuncio`;
   `prazo_propostas_dias` = `data_limite_propostas` − `data_publicacao_anuncio`; and the rest the 318 rules use.
2. Each derived fact is a fact of its own with its inputs named, so the proof reaches the BASE row.
3. Done when: for a sample of 1 000 procedures, every rule's needed fields are present or marked missing with why.

**Phase 3 — Engine over Supabase (L6).**
1. A batch job: load the rules package once, stream procedures from Supabase, evaluate, write `ccp.veredicto`.
2. Full run over the 1.48 M procedures, then each day's new ones after the ingest.
3. Done when: verdicts for every procedure, each with its manifest; counts by rule and result; a sample re-checked by
   `verify`.

**Phase 4 — Missing facts from DR notices (L4).**
1. The daily job deployed (needs the person's «deploy the loader»): BASE, TED and DR kept current.
2. The DR notice adapters fill what BASE lacks (deadlines, EU publication) for the procedures still "missing fact".
3. Tender PDFs only where a needed fact is nowhere else: measured on 100 procedures, cost stated before any spend.

**Phase 5 — CPU jobs to Scaleway.** Ingest and the engine batch move from Modal to Scaleway CPU (same code).

**Phase 6 — API (L7) and frontend (L8).**
1. The API reads Supabase: `/v1/procedimento/<id>`, `/v1/entidade/<nif>`, `/v1/regras`, `/v1/lei`, `POST /v1/verificar`
   (facts or OCDS release).
2. The frontend in the FOAAP design system (minimum weight 500, no gray text): search, procedure page (verdict cards
   with the law quoted and the proof panel), buyer page, rule page, dispute.
3. Done when: a stranger can find a procedure, read why it complies or not, and reproduce the proof.

**Phase 7 — Go public, all at once** (the person's «publícalo»). Repo public with a license, API and frontend live,
daily ingest and refresh on, the first published finding.

## 5. Costs (stated before each spend)

| Item | Estimate |
|---|---|
| Ingest + derived facts + engine batch | CPU only: a few dollars for the full run, cents a day after |
| Supabase | Pro plan plus disk growth to ~8 GB |
| Mistral re-check of rounds 11–16 | measured on 50 prompts first |
| GPU for the law refresh | minutes on the days the law changes |
| Tender PDFs | measured on 100 procedures first |

## 6. Open decisions for the person

1. Mistral model and how it runs: open weights on our GPU (most sovereign) or Mistral's EU API (no hosting).
2. When to move Facts and verdicts from Supabase to an EU provider.
3. «deploy the loader» (daily ingest on Modal until Phase 5).
4. «publícalo» (Phase 7).
