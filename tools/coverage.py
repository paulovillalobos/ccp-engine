"""What law/ holds, counted from the store: law/COVERAGE.md (FILL-PLAN B2b). Nothing is fetched.

    .venv/bin/python tools/coverage.py [--write]      prints the report; --write writes law/COVERAGE.md

    timeline_acts(store) -> [{title, date, url, norma}]   the CCP's timeline as the DR prints it in every history view
                                                          (Navigation.TimelineItem blocks): the amending acts and the
                                                          original act (DL 18/2008)
    note_diplomas(store) -> [norma id]                    every act a validity note of the consolidated page names
    remissoes(store) -> [remissão]                        the references of the CCP's own text (current versions of the
                                                          code's passages, not the approving decree) to other acts: a
                                                          numbered act ("Lei n.º 41/2015"), a named code ("Código do
                                                          Procedimento Administrativo") or an EU act ("Diretiva
                                                          2014/24/UE"); each with the passage, the quoted words and,
                                                          when an "artigo N.º" precedes the act, the target passage
    remissoes_report(store) -> dict                       distinct acts (pt / eu), captured, resolved to a passage
    render(store) -> str                                  the markdown of law/COVERAGE.md
Counting rules: a norma is captured when one of its source raws is its own page (kind diploma, lei or regulamento;
a page the act is only named on does not count: the raw's source_id is the norma's short id); structured when it has
passages (the "artigos" column says how many are articles: a code whose page stops at its decree's closing formula
has few); with
vigências when a vigencia names it as altered_by or one of its passages. A named code is its own norma (cpa, cc, ...);
a numbered act that approves a named code counts as that code (CODES). Phase-3 findings are claims about the law: each
names the raw it was read in and the words that show it, and the report prints whether those words are in that raw.
No network, no model.
"""
import argparse
import json
import re
import sys
from html import unescape
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from engine import vigente  # noqa: E402
from engine.store import Store  # noqa: E402

VERSION = "ccp-coverage-0.1"
CONSOLIDATED = "raw:dr-consolidado:lei:ccp"
OWN_PAGE = ("diploma", "lei", "regulamento")
# named codes the CCP's text cites without a number -> (norma id, the act that approves it, as norma_slug writes it)
CODES = {
    "Código do Procedimento Administrativo": ("norma:cpa", "dl-4-2015"),
    "Código Civil": ("norma:cc", "dl-47344-1966"),
    "Código Penal": ("norma:cp", "dl-48-1995"),
    "Código de Processo nos Tribunais Administrativos": ("norma:cpta", "lei-15-2002"),
    "Código das Sociedades Comerciais": ("norma:csc", "dl-262-1986"),
    "Código do Trabalho": ("norma:ct", "lei-7-2009"),
    "Código de Procedimento e de Processo Tributário": ("norma:cppt", "dl-433-1999"),
    "Código dos Regimes Contributivos do Sistema Previdencial de Segurança Social": ("norma:crcspss", "lei-110-2009"),
    "Estatuto do Mecenato": ("norma:dl-74-1999", "dl-74-1999"),
}
APPROVING = {slug: nid for nid, slug in CODES.values()}
NUMBERED = re.compile(r"(Decreto-Lei|Lei Orgânica|Lei|Portaria|Decreto Legislativo Regional|Decreto Regulamentar) n\.º "
                      r"([0-9]+(?:-[A-Z])?)/([0-9]{2,4})(?:/([A-Z]))?")
EU = re.compile(r"(Diretiva|Regulamento(?: Delegado| de Execução)? \((?:UE|CE)\)|Decisão)(?: n\.º)? ([0-9]{2,4}/[0-9]+(?:/(?:UE|CE|CEE))?)")
NAMED = re.compile("|".join(re.escape(k) for k in sorted(CODES, key=len, reverse=True)))
ARTIGO_BEFORE = re.compile(r"(?:alínea ([a-z])\) do )?(?:n\.º ([0-9]+) do )?artigo ([0-9]+)\.º(?:-([A-Z]))? d[oa]s? (?:referid[oa] )?$")
# Phase 3 (FILL-PLAN B2b.3): item, norma id, the address read, the finding, and the words in that raw that show it
PHASE3 = [
    ("Lei 30/2021 (medidas especiais)", "norma:lei-30-2021", None, None, None),
    ("DL 60/2018 (I+D)", "norma:dl-60-2018", None, None, None),
    ("DLR 27/2015/A (Açores)", "norma:dlr-27-2015-a", None, None, None),
    ("Madeira: regime regional (DLR 34/2008/M) e coeficiente 1,45", "norma:dlr-34-2008-m", None,
     "art. 4.º, n.os 1 e 4, na redação do art. 75.º do DLR n.º 26/2022/M (em vigor desde 2022-12-30); a redação original "
     "fixava 1,35; o orçamento regional de 2026 (DLR n.º 8/2025/M, art. 100.º) só altera o art. 7.º; o n.º 1 remete para "
     "artigos do CCP anteriores à renumeração do DL n.º 177/2026", "coeficiente de 1,45"),
    ("Madeira: orçamento regional de 2026", "norma:dlr-8-2025-m", None, "não contém o coeficiente (procurado «1,45»: ausente)", None),
    ("Limiares UE 2026-2027 (Diretiva 2014/24/UE)", "norma:eu-2025-2152", None, None, "«140 000 EUR»"),
    ("Limiares UE 2026-2027 (Diretiva 2014/25/UE)", "norma:eu-2025-2150", None, None, "«432 000 EUR»"),
    ("Limiares UE 2026-2027 (Diretiva 2014/23/UE)", "norma:eu-2025-2151", None, None, "«5 404 000 EUR»"),
    ("Limiares UE 2026-2027 (Diretiva 2009/81/CE)", "norma:eu-2025-2487", None, None, "«432 000 EUR»"),
    ("CPA (cômputo de prazos)", "norma:cpa", None, None, None),
    ("Lei 96/2015 (plataformas eletrónicas)", "norma:lei-96-2015", None, None, None),
    ("Portaria 371/2017 (anúncios)", "norma:port-371-2017", None,
     "revogada pela Portaria n.º 318-A/2023, que aprova os modelos de anúncio em vigor", "É revogada a Portaria n.º 371/2017"),
    ("Portaria 372/2017 (BASE)", "norma:port-372-2017", None,
     "não é a do portal BASE: trata dos documentos de habilitação do adjudicatário", "documentos de habilitação do adjudicatário"),
    ("Portal BASE (a que de facto o regula)", "norma:port-318-b-2023", None,
     "Portaria n.º 318-B/2023, que revoga a Portaria n.º 57/2018", "portal BASE"),
    ("Modelos de anúncio em vigor", "norma:port-318-a-2023", None, "Portaria n.º 318-A/2023", "É revogada a Portaria n.º 371/2017"),
    ("DL 197/99 (autorização de despesa)", "norma:dl-197-1999", None, None, None),
    ("Lei 75/2013 (competências das autarquias)", "norma:lei-75-2013", None, None, None),
    ("Lei 98/97 (Tribunal de Contas, visto prévio)", "norma:lei-98-1997", None, None, None),
]
# where a finding is read: the raw whose text must hold the evidence words
EVIDENCE_RAW = {"norma:port-371-2017": "norma:port-318-a-2023"}


def current_all(store, type_):
    out = {}
    for o in store.objects[type_]:
        if o["id"] not in out or o["revision"] > out[o["id"]]["revision"]:
            out[o["id"]] = o
    return {k: v for k, v in out.items() if not v.get("stale")}


def own_raws(store, norma):
    """The captures of the norma's own page: a raw of kind diploma / lei / regulamento whose source_id is the norma's
    short id (a page an act is only named on, in a note, is not that act's capture)."""
    out = []
    for r in norma["source"]["raw"]:
        raw = store.current(r) or {}
        if raw.get("kind") in OWN_PAGE and raw.get("source_id") == norma["short"]:
            out.append(r)
    return out


def timeline_acts(store):
    pages = sorted(r["id"] for r in current_all(store, "raw").values() if r["kind"] == "artigo-historico")
    if not pages:
        return []
    html = store.raw_path(store.current(pages[0])).read_text(encoding="utf-8")
    out = []
    for item in html.split('data-block="Navigation.TimelineItem"')[1:]:
        link = re.search(r'<a [^>]*href="(/dr/detalhe/[^"]+)"[^>]*>(.*?)</a>', item, re.S)
        when = re.search(r">([0-9]{4}-[0-9]{2}-[0-9]{2})<", item)
        if not link:
            continue
        title = " ".join(unescape(re.sub("<[^>]+>", "", link.group(2))).split()).split(" - ")[0].strip()
        out.append({"title": title, "date": when.group(1) if when else None, "url": "https://diariodarepublica.pt" + link.group(1),
                    "norma": "norma:" + vigente.norma_slug(title), "page": pages[0]})
    return out


def note_diplomas(store):
    text = store.raw_text(store.current(CONSOLIDATED))
    names = {vigente.parse_note(l[len("NOTA: "):])["diploma"] for l in text.split("\n") if l.startswith("NOTA: ")}
    return sorted("norma:" + vigente.norma_slug(n) for n in names)


def _year(y):
    return y if len(y) == 4 else "19" + y


def remissoes(store):
    passages = current_all(store, "passagem")
    kids = {}
    for c in passages.values():
        kids.setdefault(c.get("parent"), []).append(c)
    out = []
    for p in passages.values():
        if p["norma"] != "norma:ccp" or p["id"].startswith("ccp:dl.") or p["kind"] in ("parte", "titulo", "capitulo", "secao"):
            continue
        v = p["versions"][-1]
        text = v["text"]
        if vigente.parse_note(text):
            continue  # a part an amendment removed: its last version is the DR note that removed it (D30), not law
        # a passage's text holds its parts: count a reference in the passage that holds it and no child does
        children = kids.get(p["id"], [])
        own = text
        for c in children:
            ct = c["versions"][-1]["text"]
            own = own.replace(ct, "\x00" * len(ct))
        found = []
        for m in NUMBERED.finditer(own):
            kind = vigente.ACT_KINDS[m[1].lower()]
            slug = f"{kind}-{m[2].lower()}-{_year(m[3])}" + (f"-{m[4].lower()}" if m[4] else "")
            found.append((m.start(), m.group(0), APPROVING.get(slug, f"norma:{slug}"), "pt"))
        for m in NAMED.finditer(own):
            found.append((m.start(), m.group(0), CODES[m.group(0)][0], "pt"))
        for m in EU.finditer(own):
            found.append((m.start(), m.group(0), "eu:" + m[2].split("/")[0] + "/" + m[2].split("/")[1], "eu"))
        taken = set()
        for start, words, target, scope in sorted(found):
            if any(a <= start < b for a, b in taken):
                continue  # "Código ..., aprovado pela Lei n.º 110/2009" is one reference
            approves = re.match(r",? aprovad[oa] pel[oa] ", own[start + len(words):])
            end = start + len(words)
            if approves:
                nxt = NUMBERED.match(own, end + approves.end())
                if nxt:
                    end = nxt.end()
            taken.add((start, end))
            art = ARTIGO_BEFORE.search(own[max(0, start - 90):start])
            out.append({"passage": p["id"], "version": v["version"], "words": text[start:end], "offsets": {"start": start, "end": end},
                        "target": target, "scope": scope, "artigo": (art[3] + (f"-{art[4].lower()}" if art[4] else "")) if art else None,
                        "numero": art[2] if art else None, "alinea": art[1] if art else None})
    return sorted(out, key=lambda r: (r["passage"], r["offsets"]["start"]))


def remissoes_report(store):
    rows = remissoes(store)
    normas = current_all(store, "norma")
    passages = set(current_all(store, "passagem"))
    acts = {}
    for r in rows:
        a = acts.setdefault(r["target"], {"target": r["target"], "scope": r["scope"], "count": 0, "passages": set(), "resolved": 0})
        a["count"] += 1
        a["passages"].add(r["passage"])
        n = normas.get(r["target"])
        r["resolved"] = resolve(n, r, passages) if n and r["artigo"] else None
        if r["resolved"]:
            a["resolved"] += 1
    for a in acts.values():
        n = normas.get(a["target"])
        a["registered"] = n is not None
        a["captured"] = bool(n and own_raws(store, n))
        a["passages"] = sorted(a["passages"])
    pt = [a for a in acts.values() if a["scope"] == "pt"]
    return {"rows": len(rows), "acts": sorted(acts.values(), key=lambda a: (a["scope"], -a["count"], a["target"])),
            "distinct_pt": len(pt), "captured_pt": sum(a["captured"] for a in pt),
            "distinct_eu": sum(a["scope"] == "eu" for a in acts.values()),
            "resolved_to_passage": sum(a["resolved"] for a in acts.values()),
            "with_artigo": sum(1 for r in rows if r["artigo"]),
            "with_artigo_pt": sum(1 for r in rows if r["artigo"] and r["scope"] == "pt"),
            "resolved_pt": sum(1 for r in rows if r["resolved"] and r["scope"] == "pt"),
            "resolved_below_article": sum(1 for r in rows if r["resolved"] and r["resolved"].count(".") > 0),
            "resolutions": [{"passage": r["passage"], "words": r["words"], "artigo": r["artigo"], "numero": r["numero"], "alinea": r["alinea"],
                             "to": r["resolved"]} for r in rows if r["artigo"]]}


def resolve(norma, r, passages):
    """The most specific passage of the cited act the words name: alínea of the number of the article, the number, the
    article; None when the act has no such passage (not structured, or not captured)."""
    base = f"{norma['short']}:art{r['artigo']}"
    tries = [f"{base}.{r['numero']}.{r['alinea']}"] if r["numero"] and r["alinea"] else []
    tries += [f"{base}.{r['numero']}"] if r["numero"] else ([f"{base}.{r['alinea']}"] if r["alinea"] else [])
    for pid in tries + [base]:
        if pid in passages:
            return pid
    return None


def norma_rows(store):
    normas = current_all(store, "norma")
    passages = current_all(store, "passagem")
    vig = current_all(store, "vigencia")
    by_norma, arts = {}, {}
    for p in passages.values():
        by_norma[p["norma"]] = by_norma.get(p["norma"], 0) + 1
        if p["kind"] == "artigo" and ".q" not in p["id"]:
            arts[p["norma"]] = arts.get(p["norma"], 0) + 1
    with_vig = {v["altered_by"] for v in vig.values()} | {passages[v["passage"]]["norma"] for v in vig.values() if v["passage"] in passages}
    rows = []
    for nid in sorted(normas):
        n = normas[nid]
        rows.append({"id": nid, "title": n["title"], "jurisdiction": n["jurisdiction"], "own": own_raws(store, n),
                     "passages": by_norma.get(nid, 0), "artigos": arts.get(nid, 0), "vigencias": nid in with_vig, "url": n["source"]["url"]})
    return rows


def phase3_rows(store):
    normas = current_all(store, "norma")
    out = []
    for item, nid, _, finding, words in PHASE3:
        n = normas.get(nid)
        where = normas.get(EVIDENCE_RAW.get(nid, nid))
        raws = own_raws(store, where) if where else []
        shown = None
        if words and raws:
            shown = any(words in (store.raw_text(store.current(r)) or "") for r in raws)
        out.append({"item": item, "norma": nid, "registered": n is not None, "captured": bool(n and own_raws(store, n)),
                    "url": (n or where or {}).get("source", {}).get("url"), "finding": finding, "words": words,
                    "evidence_raw": raws[0] if raws else None, "shown": shown})
    return out


def yes(b):
    return "sim" if b else "não"


def render(store):
    rows = norma_rows(store)
    tl = timeline_acts(store)
    notes = note_diplomas(store)
    rep = remissoes_report(store)
    vig = current_all(store, "vigencia")
    ccp = [p for p in current_all(store, "passagem").values() if p["norma"] == "norma:ccp"]
    L = ["# COVERAGE — o que law/ contém", "",
         f"Gerado por tools/coverage.py ({VERSION}) a partir do store; não editar à mão. Contagens em registos.", "",
         "## Normas", "",
         f"- registadas: {len(rows)}",
         f"- capturadas (página própria no DR ou no EUR-Lex, bytes com sha256 em law/raw_bytes/): {sum(1 for r in rows if r['own'])}",
         f"- estruturadas (com passagens): {sum(1 for r in rows if r['passages'])}",
         f"- com vigências: {sum(1 for r in rows if r['vigencias'])}",
         f"- CCP: {len(ccp)} passagens ({sum(p['kind'] == 'artigo' for p in ccp)} artigo), {sum(len(p['versions']) for p in ccp)} versões; "
         f"{sum(1 for v in vig.values() if v['passage'].startswith('ccp:'))} vigências", "",
         "| norma | título | jurisdição | capturada | passagens | artigos | vigências | endereço |", "|---|---|---|---|---|---|---|---|"]
    for r in rows:
        L.append(f"| {r['id']} | {r['title']} | {r['jurisdiction']} | {yes(r['own'])} | {r['passages']} | {r['artigos']} | {yes(r['vigencias'])} | {r['url']} |")
    L += ["", f"## Linha temporal do CCP ({len(tl)} itens: {len(tl) - 1} atos que o alteram e o ato original), lida em {tl[0]['page'] if tl else '—'}", "",
          "| data | ato | norma | registada | capturada |", "|---|---|---|---|---|"]
    normas = current_all(store, "norma")
    for a in tl:
        n = normas.get(a["norma"])
        L.append(f"| {a['date']} | {a['title']} | {a['norma']} | {yes(n)} | {yes(n and own_raws(store, n))} |")
    L += ["", f"Atos nomeados nas notas do consolidado: {len(notes)}; registados: {sum(1 for n in notes if n in normas)}.", "",
          "## Remissões do texto do CCP", "",
          f"- referências encontradas: {rep['rows']} (das quais {rep['with_artigo']} com «artigo N.º» do ato)",
          f"- atos portugueses distintos: {rep['distinct_pt']}; capturados: {rep['captured_pt']}"
          + (f" ({100 * rep['captured_pt'] // rep['distinct_pt']} %)" if rep["distinct_pt"] else ""),
          f"- atos da UE distintos: {rep['distinct_eu']} (não capturados nesta fase salvo os limiares)",
          f"- resolvidas a uma passagem do ato citado: {rep['resolved_to_passage']}; das que nomeiam um artigo de ato "
          f"português: {rep['resolved_pt']} de {rep['with_artigo_pt']}, {rep['resolved_below_article']} até ao número ou à alínea", "",
          "| passagem do CCP | palavras | artigo / n.º / alínea | resolvida a |", "|---|---|---|---|"]
    for x in rep["resolutions"]:
        L.append(f"| {x['passage']} | {x['words']} | {x['artigo']} / {x['numero'] or '—'} / {x['alinea'] or '—'} | {x['to'] or '—'} |")
    L += ["",
          "| alvo | âmbito | referências | registado | capturado | resolvidas | onde (primeiras) |", "|---|---|---|---|---|---|---|"]
    for a in rep["acts"]:
        L.append(f"| {a['target']} | {a['scope']} | {a['count']} | {yes(a['registered'])} | {yes(a['captured'])} | {a['resolved']} | {', '.join(a['passages'][:3])} |")
    L += ["", "## Normas da fase 3", "", "| item | norma | registada | capturada | endereço lido | achado | palavras no texto capturado |", "|---|---|---|---|---|---|---|"]
    for r in phase3_rows(store):
        shown = "—" if r["shown"] is None else (f"«{r['words']}» em {r['evidence_raw']}" if r["shown"] else f"NÃO encontradas: «{r['words']}»")
        L.append(f"| {r['item']} | {r['norma']} | {yes(r['registered'])} | {yes(r['captured'])} | {r['url'] or '—'} | {r['finding'] or '—'} | {shown} |")
    build = {}
    report = store.roots[0] / "build-report.json"
    if report.exists():
        build = json.loads(report.read_text(encoding="utf-8"))
    tl_ids = {a["norma"] for a in tl}
    ccp_scope = tl_ids | set(notes) | {a["target"] for a in rep["acts"] if a["scope"] == "pt"} | {r["norma"] for r in phase3_rows(store)}
    other = [r for r in rows if not r["own"] and r["id"] not in ccp_scope]
    L += ["", "## O que falta e porquê", "",
          "Atos da linha temporal, das notas do CCP, das remissões e da fase 3 sem página própria lida:", ""]
    for r in rows:
        if r["id"] in ccp_scope and not r["own"]:
            L.append(f"- {r['id']} ({r['title']}): registado; página própria ainda não lida ({r['url']}).")
    L += ["", "Capturados mas não estruturados (o motivo é o que tools/build_law.py registou em law/build-report.json):", ""]
    for nid, why in sorted(build.get("not_structured", {}).items()):
        L.append(f"- {nid}: {why}")
    L += ["", "Artigos deixados de fora por uma nota que não se lê ou não se data (D33):", ""]
    for nid, ids in sorted(build.get("articles_left_out", {}).items()):
        L.append(f"- {nid}: {len(ids)} ({', '.join(ids)})")
    L += ["", f"Registados só por aparecerem nas notas de outros códigos capturados (não citados pelo CCP): {len(other)}.", ""]
    return "\n".join(L) + "\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true")
    a = ap.parse_args()
    store = Store([ROOT / "law", ROOT / "rules", ROOT / "governance"]).load()
    out = render(store)
    if a.write:
        (ROOT / "law/COVERAGE.md").write_text(out, encoding="utf-8")
    print(out)


if __name__ == "__main__":
    main()
