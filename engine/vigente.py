"""The law's clock: validity notes of the Diário da República as data, passage versions, the text in force at a date.

What the DR gives (read 2026-10-24, DECISIONS D24):
  - the consolidated page: per article, the current text followed by every note, newest first (735 notes for the CCP);
  - one history page per altered article (opened by a click, tools/capture_dr_history.mjs): per version, title +
    epigraph + text, then the note that produced that version; the oldest version is "Versão inicial" and has no note.
  - a note reads: "<Efeito> pelo/a [Artigo N.º do/a] <diploma> - Diário da República n.º <n>/<ano>[, <k>º Suplemento],
    Série I de <AAAA-MM-DD>, em vigor a partir de <AAAA-MM-DD>[.]"  (NOTE_RE)

    parse_note(text) -> dict | None       {effect, article_of_act, diploma, dr_issue, published, valid_from}; None if not a note
    EFFECTS                               Alterado -> altera, Aditado -> adita, Revogado -> revoga, Retificado -> retifica,
                                          Republicado -> republica
    versions_from_history(text, initial_valid_from) -> list[dict]
        the working text of a history page (extractor dr-article-history@1) -> versions oldest first:
        {label, epigraph, lines, note, valid_from, valid_to}. valid_from = the note's date; the initial version gets
        initial_valid_from (the norm's entry into force); valid_to = the next version's valid_from or None.
        Rectifications: versions sharing a valid_from are one legal version; the newest text wins and the others are
        kept in "rectified" (a retificação replaces the text as of the same date).
    notes_to_vigencias(text, raw_id, passages, normas) -> list[vigencia]      B2 (red: tests/fill/test_b2_ccp_capture.py)
    vigente(store, date) -> dict[passage_id, version]                          B2 (red)
    norma_slug(diploma) -> str            "Decreto-Lei n.º 177/2026" -> "dl-177-2026"; "Lei n.º 30/2021" -> "lei-30-2021";
                                          "Declaração de Retificação n.º 42/2017" -> "ret-42-2017"
No network, no model.
"""
import re

VERSION = "ccp-vigente-0.1"
EFFECTS = {"Alterado": "altera", "Aditado": "adita", "Revogado": "revoga", "REVOGADO": "revoga", "Retificado": "retifica", "Rectificado": "retifica", "Republicado": "republica"}
# Read on the CCP page (735 notes): 53 are "REVOGADO" in capitals; 4 carry no "em vigor a partir de" (valid_from None:
# B2 decides from the act's own entry-into-force article and records the decision in the vigencia's note).
NOTE_RE = re.compile(
    r"^(?:NOTA: )?(?P<effect>Alterado|Aditado|Revogado|REVOGADO|Retificado|Rectificado|Republicado) pelo/a "
    r"(?:Artigo (?P<article>[0-9]+\.º(?:-[A-Z])?) do/a )?(?P<diploma>.+?) - Diário da República n\.º (?P<issue>[0-9]+(?:-[A-Z])?/[0-9]{4})"
    r"(?:, (?P<supl>[0-9]+º Suplemento))?, Série I de (?P<published>[0-9]{4}-[0-9]{2}-[0-9]{2})(?:, em vigor a partir de (?P<valid_from>[0-9]{4}-[0-9]{2}-[0-9]{2}))?\.?$")
ACT_KINDS = {"decreto-lei": "dl", "lei": "lei", "declaração de retificação": "ret", "declaração de rectificação": "ret", "lei orgânica": "lo",
             "decreto legislativo regional": "dlr", "portaria": "port", "decreto regulamentar": "dreg"}


def parse_note(text):
    m = NOTE_RE.match(text.strip())
    if not m:
        return None
    return {"effect": EFFECTS[m["effect"]], "article_of_act": m["article"], "diploma": m["diploma"], "dr_issue": m["issue"] + (f" {m['supl']}" if m["supl"] else ""),
            "published": m["published"], "valid_from": m["valid_from"]}


def norma_slug(diploma: str) -> str:
    m = re.match(r"^(?P<kind>.+?) n\.º (?P<num>[0-9]+(?:-[A-Z])?)/(?P<year>[0-9]{4})(?:/(?P<reg>[A-Z]))?$", diploma.strip())
    if not m:
        raise ValueError(f"not a DR act reference: {diploma!r}")
    kind = ACT_KINDS.get(m["kind"].lower())
    if not kind:
        raise ValueError(f"unknown act kind in {diploma!r}")
    return f"{kind}-{m['num'].lower()}-{m['year']}" + (f"-{m['reg'].lower()}" if m["reg"] else "")


ART_RE = re.compile(r"^Artigo [0-9]+\.º(?:-[A-Z])?$")


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


def notes_to_vigencias(text: str, raw_id: str, passages: list, normas: dict) -> list:
    raise NotImplementedError("FILL-PLAN B2: consolidated working text -> vigencia objects, one per note, quoted by offsets")


def vigente(store, date: str) -> dict:
    raise NotImplementedError("FILL-PLAN B2: the version of every passage in force at date, from passagem.versions")
