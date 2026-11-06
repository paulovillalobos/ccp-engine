"""The legal basis an entity declared for a contract (BASE's `fundamentacao`) as passage ids (DECISIONS D88).

    passages("Artigo 19.º, alínea c) do Código dos Contratos Públicos e artigo 4.º, nº 1 do DLR nº 34/2008/M")
        -> ["ccp:art19.c", "dlr-34-2008-m:art4.1"]

Each «artigo N.º[-X][, n.º M][, alínea x)]» is read with the act named after it («do Código dos Contratos Públicos»,
«da Lei n.º 30/2021», «do Decreto-Lei 59-A/2024», «do DLR nº 34/2008/M»); an article with no act named after it is of the
act the text named last, else the CCP. An act the code cannot name gives «?:<its words>»: never silently the CCP. This
is what the entity declared, read word by word; it says nothing about whether the basis is right.
"""
import re

VERSION = "ccp-fundamento-0.1"
CODES = {"código dos contratos públicos": "ccp", "ccp": "ccp", "código do procedimento administrativo": "cpa"}
ART = re.compile(r"(?i)\bartigos?\s+(\d+)\s*\.?\s*[ºo°]?(?:\s*-\s*([A-Z]))?(?:\s*,?\s*n\s*\.?\s*[ºo°]\s*(\d+))?(?:\s*,?\s*al[íi]nea\s+([a-z])\s*\))?")
ACT = re.compile(r"(?i)\b(?:d[oa]s?\s+)?(c[óo]digo dos contratos p[úu]blicos|c[óo]digo do procedimento administrativo|ccp\b|"
                 r"(decreto[\s-]+lei|dl|lei|dlr|decreto legislativo regional|decreto regulamentar regional|portaria)\s*(?:n\s*\.?\s*[ºo°]\s*)?(\d+(?:\s*-\s*[a-z])?)\s*/\s*(\d{4})(?:\s*/\s*([am]))?)")


def act_short(m):
    """«Código dos Contratos Públicos» -> ccp; «Decreto-Lei n.º 59-A/2024» -> dl-59-a-2024; «DLR nº 34/2008/M» -> dlr-34-2008-m."""
    if m.group(2) is None:
        name = m.group(1).lower()
        return "cpa" if "procedimento" in name else "ccp"
    kind = " ".join(m.group(2).lower().replace("-", " ").split())
    kind = {"decreto lei": "dl", "decreto legislativo regional": "dlr", "decreto regulamentar regional": "drr"}.get(kind, kind)
    num = re.sub(r"\s+", "", m.group(3)).lower()
    return f"{kind}-{num}-{m.group(4)}" + (f"-{m.group(5).lower()}" if m.group(5) else "")


def passages(text):
    text = " ".join((text or "").split())
    if not text:
        return []
    acts = [(m.start(), m.end(), act_short(m)) for m in ACT.finditer(text)]
    out, last = [], None
    for a in ART.finditer(text):
        after = next((s for st, en, s in acts if st >= a.end() and st - a.end() < 120 and not ART.search(text[a.end():st])), None)
        act = after or last or "ccp"
        last = act
        pid = f"{act}:art{a.group(1)}" + (f"-{a.group(2).lower()}" if a.group(2) else "") + (f".{a.group(3)}" if a.group(3) else "") + (f".{a.group(4).lower()}" if a.group(4) else "")
        out.append(pid)
    if not out:
        out.append("?:" + text[:120])
    return sorted(set(out))
