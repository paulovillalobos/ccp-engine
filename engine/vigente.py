"""The law's clock: validity notes of the Diário da República as data, passage versions, the text in force at a date.

What the DR gives (read 2026-10-24, DECISIONS D24):
  - the consolidated page: per article, the current text followed by every note, newest first (735 notes for the CCP);
  - one history page per altered article (opened by a click, tools/capture_dr_history.mjs): per version, title +
    epigraph + text, then the note that produced that version; the oldest version is "Versão inicial" and has no note.
  - a note reads: "<Efeito> pelo/a [Artigo N.º do/a] <diploma> - Diário da República n.º <n>/<ano>[, <k>º Suplemento],
    Série I[-A|-B] de <AAAA-MM-DD>, em vigor a partir de <AAAA-MM-DD>[, produz efeitos a partir de <AAAA-MM-DD>][.]"
    (NOTE_RE; valid_from is the date in force, the effects date stays in the quoted note)

    parse_note(text) -> dict | None       {effect, article_of_act, diploma, dr_issue, published, valid_from}; None if not a note
    EFFECTS                               Alterado -> altera, Aditado -> adita, Revogado -> revoga, Retificado -> retifica,
                                          Republicado -> republica
    versions_from_history(text, initial_valid_from) -> list[dict]
        the working text of a history page (extractor dr-article-history@1) -> versions oldest first:
        {label, epigraph, lines, note, valid_from, valid_to}. valid_from = the note's date; the initial version gets
        initial_valid_from (the norm's entry into force); valid_to = the next version's valid_from or None.
        Rectifications: versions sharing a valid_from are one legal version; the newest text wins and the others are
        kept in "rectified" (a retificação replaces the text as of the same date).
    notes_to_vigencias(text, raw_id, passages, normas) -> list[vigencia]      one per (passage, valid_from); see its docstring
    vigente(store, date) -> dict[passage_id, version]                          the version of every passage in force at date
    entry_into_force(published, article_text) -> str | None                    an act's own entry-into-force article, read
    resolve_note_dates(notes, passages) -> {(diploma, published): date}       the dates of dateless notes (D28)
    norma_slug(diploma) -> str            "Decreto-Lei n.º 177/2026" -> "dl-177-2026"; "Lei n.º 30/2021" -> "lei-30-2021";
                                          "Declaração de Retificação n.º 42/2017" -> "ret-42-2017";
                                          "Resolução da Assembleia da República n.º 16/2020" -> "rar-16-2020";
                                          "Lei n.º 98/97" -> "lei-98-1997" (two-digit years are 19xx)
    A note's amending provision may be "Artigo N.º", "Parte III" or "Anexo [N]" of the act (article_of_act carries it).
No network, no model.
"""
import bisect
import re
from datetime import date, timedelta

VERSION = "ccp-vigente-0.1"
EFFECTS = {"Alterado": "altera", "Aditado": "adita", "Revogado": "revoga", "REVOGADO": "revoga", "Retificado": "retifica", "Rectificado": "retifica", "Republicado": "republica"}
# Read on the CCP page (735 notes): 53 are "REVOGADO" in capitals; 4 carry no "em vigor a partir de" (valid_from None:
# B2 decides from the act's own entry-into-force article and records the decision in the vigencia's note).
NOTE_RE = re.compile(
    r"^(?:NOTA: )?(?P<effect>Alterado|Aditado|Revogado|REVOGADO|Retificado|Rectificado|Republicado) pelo/a "
    r"(?:(?P<article>Artigo [0-9]+\.º(?:-[A-Z])?|Parte [IVXLC]+|Anexo(?: [IVXLC]+)?) do/a )?(?P<diploma>.+?) - Diário da República n\.º (?P<issue>[0-9]+(?:-[A-Z])?/[0-9]{4})"
    r"(?:, (?P<supl>[0-9]+º Suplemento))?, Série I(?:-[AB])? de (?P<published>[0-9]{4}-[0-9]{2}-[0-9]{2})(?:, em vigor a partir de (?P<valid_from>[0-9]{4}-[0-9]{2}-[0-9]{2}))?"
    r"(?:, produz efeitos a partir de [0-9]{4}-[0-9]{2}-[0-9]{2})?\.?$")
ACT_KINDS = {"decreto-lei": "dl", "lei": "lei", "declaração de retificação": "ret", "declaração de rectificação": "ret", "lei orgânica": "lo",
             "decreto legislativo regional": "dlr", "portaria": "port", "decreto regulamentar": "dreg",
             "resolução da assembleia da república": "rar"}


def parse_note(text):
    m = NOTE_RE.match(text.strip())
    if not m:
        return None
    art = m["article"][len("Artigo "):] if m["article"] and m["article"].startswith("Artigo ") else m["article"]
    return {"effect": EFFECTS[m["effect"]], "article_of_act": art, "diploma": m["diploma"], "dr_issue": m["issue"] + (f" {m['supl']}" if m["supl"] else ""),
            "published": m["published"], "valid_from": m["valid_from"]}


def norma_slug(diploma: str) -> str:
    m = re.match(r"^(?P<kind>.+?) n\.º (?P<num>[0-9]+(?:-[A-Z])?)/(?P<year>[0-9]{4}|[0-9]{2})(?:/(?P<reg>[A-Z]))?$", diploma.strip())
    if not m:
        raise ValueError(f"not a DR act reference: {diploma!r}")
    kind = ACT_KINDS.get(m["kind"].lower())
    if not kind:
        raise ValueError(f"unknown act kind in {diploma!r}")
    year = m["year"] if len(m["year"]) == 4 else "19" + m["year"]  # the DR prints acts before 2000 as n.º 98/97
    return f"{kind}-{m['num'].lower()}-{year}" + (f"-{m['reg'].lower()}" if m["reg"] else "")


ART_RE = re.compile(r"^Artigo [0-9]+(?:\.º)?(?:-[A-Z])?$")


def versions_from_history(text: str, initial_valid_from: str) -> list:
    lines = text.splitlines()
    blocks, cur = [], None
    for line in lines:
        if ART_RE.match(line):
            cur = {"label": line, "epigraph": None, "lines": [], "note": None}
            blocks.append(cur)
        elif cur is None:
            continue
        elif line.startswith("NOTA: "):
            cur["note"] = parse_note(line)
            if cur["note"] is None:
                raise ValueError(f"unparsed note: {line[:120]!r}")
            cur = None
        elif cur["epigraph"] is None:
            cur["epigraph"] = line
        else:
            cur["lines"].append(line)
    if not blocks:
        raise ValueError("no article versions in text")
    # newest first in the page; the note after a version is the act that produced it
    versions = []
    for b in blocks:
        versions.append({"label": b["label"], "epigraph": b["epigraph"], "lines": b["lines"], "note": b["note"],
                         "valid_from": b["note"]["valid_from"] if b["note"] else initial_valid_from, "valid_to": None, "rectified": []})
    versions.reverse()  # oldest first
    merged = []
    for v in versions:
        if merged and merged[-1]["valid_from"] == v["valid_from"]:
            v["rectified"] = merged[-1]["rectified"] + [{k: merged[-1][k] for k in ("lines", "note")}]
            merged[-1] = v
        else:
            merged.append(v)
    for a, b in zip(merged, merged[1:]):
        a["valid_to"] = b["valid_from"]
    return merged


GENERAL_RULE = "lei-74-1998:art2.2"  # "Na falta de fixação do dia, ... entram em vigor ... no 5.º dia após a publicação."
EFFECT_PRIORITY = {"revoga": 0, "adita": 1, "altera": 2, "republica": 3, "retifica": 4}
MONTHS_PT = {"um": 1, "dois": 2, "três": 3, "quatro": 4, "cinco": 5, "seis": 6, "sete": 7, "oito": 8, "nove": 9, "dez": 10, "onze": 11, "doze": 12}
NUMBERS_PT = {"cinco": 5, "dez": 10, "quinze": 15, "vinte": 20, "trinta": 30, "sessenta": 60, "noventa": 90, "cento e vinte": 120, "cento e oitenta": 180}


def entry_into_force(published: str, article_text: str):
    """The date an act enters into force, from its own entry-into-force article and its publication date, for the
    phrasings read in the DR; None when the article says something else (the caller then fails, it never guesses).
        "entra em vigor no dia seguinte ao da sua publicação"            published + 1 day
        "entra em vigor no primeiro dia do mês seguinte ao da sua publicação"   the 1st of the next month
        "entra em vigor <n> dias após a (data da) sua publicação"        published + n days (digits or words)
        "entram em vigor ... no 5.º dia após a publicação"               published + 5 days (Lei 74/98, art. 2.º, n.º 2)
        "entra em vigor (no dia|em) <AAAA-MM-DD | d de mês de aaaa>"      that date"""
    t = " ".join(article_text.split()).lower()
    d = date.fromisoformat(published)
    if "no dia seguinte ao da sua publicação" in t:
        return (d + timedelta(days=1)).isoformat()
    m = re.search(r"no ([0-9]+)\.º dia após a (?:sua )?publicação", t)
    if m:
        return (d + timedelta(days=int(m.group(1)))).isoformat()
    if "no primeiro dia do mês seguinte ao da sua publicação" in t:
        return (date(d.year + (d.month == 12), d.month % 12 + 1, 1)).isoformat()
    m = re.search(r"entra(?:m)? em vigor (?:([0-9]+)|(" + "|".join(sorted(NUMBERS_PT, key=len, reverse=True)) + r")) dias após a (?:data da )?sua publicação", t)
    if m:
        return (d + timedelta(days=int(m.group(1)) if m.group(1) else NUMBERS_PT[m.group(2)])).isoformat()
    m = re.search(r"entra(?:m)? em vigor (?:no dia|em|a) ([0-9]{1,2}) de ([a-zç]+) de ([0-9]{4})", t)
    months = ["janeiro", "fevereiro", "março", "abril", "maio", "junho", "julho", "agosto", "setembro", "outubro", "novembro", "dezembro"]
    if m and m.group(2) in months:
        return date(int(m.group(3)), months.index(m.group(2)) + 1, int(m.group(1))).isoformat()
    return None


def resolve_note_dates(notes, passages) -> dict:
    """{(diploma, published): valid_from} for every note in `notes` (parse_note dicts) that carries no "em vigor a
    partir de" (DECISIONS D28, D31): the single date the other notes of the same act carry among `notes`; else the act's
    own "Entrada em vigor" article among `passages`, read by entry_into_force; else, when the act's own articles are
    among `passages` and none is an entry-into-force article, the general rule of Lei n.º 74/98, art. 2.º, n.º 2
    (passage GENERAL_RULE, read the same way); else ValueError."""
    siblings = {}
    for n in notes:
        if n["valid_from"]:
            siblings.setdefault((n["diploma"], n["published"]), set()).add(n["valid_from"])
    out = {}
    for n in notes:
        key = (n["diploma"], n["published"])
        if n["valid_from"] or key in out:
            continue
        known = siblings.get(key, set())
        if len(known) == 1:
            out[key] = next(iter(known))
            continue
        slug = norma_slug(n["diploma"])
        art = next((p for p in passages if p["id"].startswith(slug + ":") and p["kind"] == "artigo" and ".q" not in p["id"]
                    and "\nEntrada em vigor\n" in p["versions"][-1]["text"] + "\n"), None)
        found = entry_into_force(n["published"], art["versions"][-1]["text"]) if art else None
        own = [p for p in passages if p["id"].startswith(slug + ":") and p["kind"] == "artigo" and ".q" not in p["id"]]
        if not found and own and art is None:
            # the act was read and fixes no day: the general rule (Lei n.º 74/98, art. 2.º, n.º 2), read from its passage
            rule = next((p for p in passages if p["id"] == GENERAL_RULE), None)
            found = entry_into_force(n["published"], rule["versions"][-1]["text"]) if rule else None
        if not found:
            raise ValueError(f"note of {n['diploma']} without a date: no single sibling date ({sorted(known)}) and no readable entry-into-force article of {slug}")
        out[key] = found
    return out


def notes_to_vigencias(text: str, raw_id: str, passages: list, normas: dict) -> list:
    """The DR validity notes of a consolidated working text (lines "NOTA: ...", engine/extract.dr_article_history) ->
    vigencia objects.
        text      the working text of raw_id
        passages  passagem objects; those whose version sits in raw_id, of kind artigo or anexo and not inside an
                  amending quotation, own the notes that follow them (a note belongs to the article above it)
        normas    {norma id: norma}: every amending act a note names must be registered (altered_by = norma:<slug>)
    One vigencia per (passage, valid_from): several notes of one article with one date (an act and the retificações
    of it, D24) are one validity interval; the vigencia quotes the note of highest effect (revoga > adita > altera >
    republica > retifica), the newest first among equals. note = {raw, quote (the DR text, without "NOTA: "),
    offsets}; valid_to = the passage's next vigencia date or None.
    A note without "em vigor a partir de" takes, in order (DECISIONS D28): the single date the other notes of the same
    act (same diploma and publication date) carry in this text; else entry_into_force() over the act's own article
    whose epigraph is "Entrada em vigor" among `passages`; else ValueError. A note above every owning passage concerns
    the whole act and is not a passage's vigencia (the caller reports it). Unparsed note -> ValueError."""
    from engine.sources import now_utc  # engine.sources loads the store; imported here to keep this module light
    owners = sorted((v["offsets"]["start"], p["id"]) for p in passages if p["kind"] in ("artigo", "anexo") and ".q" not in p["id"]
                    for v in p["versions"] if v["raw"] == raw_id)
    starts = [s for s, _ in owners]
    notes, pos = [], 0
    for line in text.split("\n"):
        if line.startswith("NOTA: "):
            body = line[len("NOTA: "):]
            parsed = parse_note(body)
            if parsed is None:
                raise ValueError(f"unparsed note at offset {pos}: {body[:120]!r}")
            k = bisect.bisect_left(starts, pos) - 1
            notes.append({"owner": owners[k][1] if k >= 0 else None, "start": pos + len("NOTA: "), "end": pos + len(line), "quote": body, **parsed})
        pos += len(line) + 1
    resolved = resolve_note_dates(notes, passages)
    for n in notes:
        n["valid_from"] = n["valid_from"] or resolved[(n["diploma"], n["published"])]
    groups = {}
    for n in notes:
        if n["owner"] is None:
            continue
        altered_by = f"norma:{norma_slug(n['diploma'])}"
        if altered_by not in normas:
            raise ValueError(f"{altered_by} is not registered (note on {n['owner']})")
        groups.setdefault((n["owner"], n["valid_from"]), []).append(n)
    recorded_at = now_utc()
    dates = {}
    for owner, vf in groups:
        dates.setdefault(owner, []).append(vf)
    out = []
    for (owner, vf), group in sorted(groups.items()):
        n = min(group, key=lambda x: (EFFECT_PRIORITY[x["effect"]], x["start"]))
        later = sorted(d for d in dates[owner] if d > vf)
        out.append({"id": f"{owner}@{vf}", "revision": 1, "recorded_at": recorded_at, "passage": owner, "valid_from": vf,
                    "valid_to": later[0] if later else None, "altered_by": f"norma:{norma_slug(n['diploma'])}",
                    "note": {"raw": raw_id, "quote": n["quote"], "offsets": {"start": n["start"], "end": n["end"]}}, "effect": n["effect"]})
    return out


def vigente(store, date: str) -> dict:  # noqa: F811 (the parameter shadows datetime.date inside this function only)
    """{passage id: version} for every current, non-stale passage that has a version in force on date
    (valid_from <= date < valid_to; valid_to None = still in force). A revoked version is in force: it says the
    passage is revoked. Passages with no version on that date are absent."""
    latest = {}
    for p in store.objects["passagem"]:
        if p["id"] not in latest or p["revision"] > latest[p["id"]]["revision"]:
            latest[p["id"]] = p
    out = {}
    for pid, p in latest.items():
        if p.get("stale"):
            continue
        for v in p["versions"]:
            if v["valid_from"] <= date and (v["valid_to"] is None or date < v["valid_to"]):
                out[pid] = v["version"]
                break
    return out
