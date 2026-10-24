"""The structure of a Diário da República text: the working text of a capture -> passagem objects with offsets.

    structure(norma, raw_text, raw_id, version) -> list[passagem]
        one passage per structural node: anexo (a code's own annexes, D27), parte, titulo, capitulo, secao (Secção and
        Subsecção), artigo, numero ("1 - "),
        alinea ("a) "), subalinea ("i) "), each with ONE version keyed `version` (= valid_from, valid_to None) whose text
        is raw_text[start:end] — verify re-derives it (I01). Ids: <norma.short>:<path>
            ccp:art20  ccp:art20.1  ccp:art20.1.a  ccp:art20.1.a.i       articles and their parts
            ccp:parte-ii.titulo-i.capitulo-ii                            headings, nested by rank
            ccp:dl.art18                                                 an article of the approving decree (see Regions)
            dl-177-2026:art2.q1.art20.1                                  an amending quotation («...») hangs from the
                                                                         passage that quotes it, never from the act
        An article's text runs from its "Artigo N.º" line to its last line before the next article, heading, validity
        note ("NOTA: ", engine/extract.dr_article_history) or closing formula; a number's to the next number; and so on.
        A heading's text is its line and the name on the next line. Lines before the first article or heading (the
        preamble) are not passages.

Regions (what is structured):
    - an act (norma.short is an act slug: dl-, lei-, ret-, lo-, dlr-, port-, dreg-): its own articles only, from the
      first article to the first annex line ("ANEXO", "ANEXO I", "Anexo") or the closing formula ("Visto e aprovado em
      Conselho de Ministros", "Promulgado em", ...), so an act that republishes another (DL 177/2026 republishes the
      CCP after its "ANEXO") does not structure the republished text as its own articles;
    - a code approved in the annex of a decree (any other norma.short, e.g. ccp on the consolidated DL 18/2008 page):
      the annex is the code (ccp:artN) and the decree's own articles before the "Anexo" line are kept under the path
      prefix "dl." (ccp:dl.art18), so their numbering does not collide with the code's.

Revoked: a version whose text, past its label, is only "(Revogado.)" / "[Revogado.]" / "(Revogada.)" is `revoked`.
Fails instead of guessing: an unknown structure line raises ValueError naming the line (a number outside any article, a
duplicate id, an unbalanced quotation, an alínea with no holder). No network, no model.
Copied from rjue-engine's structure module (the line grammar and the quotation contexts) and versioned here.
"""
import re

from engine.sources import now_utc

VERSION = "ccp-structure-0.1"

ACT_SHORT = re.compile(r"^(dl|lei|ret|lo|dlr|port|dreg)-")
ANNEX_LINE = re.compile(r"^(ANEXO|Anexo)(?: [IVXLC]+(?:-[A-Z])?)?$")
HEADING = re.compile(r"^(Parte|Título|Capítulo|Secção|Subsecção|PARTE|TÍTULO|CAPÍTULO|SECÇÃO|SUBSECÇÃO) ([IVXLC]+|ÚNICO|ÚNICA|[0-9]+)(?:-([A-Z]))?$")
HEADING_KIND = {"parte": ("parte", 1), "título": ("titulo", 2), "capítulo": ("capitulo", 3), "secção": ("secao", 4), "subsecção": ("secao", 5)}
HEADING_SLUG = {"parte": "parte", "título": "titulo", "capítulo": "capitulo", "secção": "seccao", "subsecção": "subseccao"}
ARTICLE = re.compile(r"^Artigo ([0-9]+)\.º(?:-([A-Z]+))?$")
NUMBER = re.compile(r"^([0-9]+(?:-[A-Z])?) - ")
LETTER = re.compile(r"^([a-z]{1,4})\) ")
ROMAN = re.compile(r"^(?:x{0,1}(?:ix|iv|v?i{0,3}))$")
REVOKED = re.compile(r"^[\(\[]?Revogad[oa]s?\.?[\)\]]?\.?$")
CLOSING = re.compile(r"^(Visto e aprovado em Conselho de Ministros|Promulgado em|Publique-se\.|Referendado em)")
NOTE_PREFIX = "NOTA: "
RANK = {"anexo": 10, "artigo": 10, "numero": 20, "alinea": 30, "subalinea": 40}
LETTERS = "abcdefghijklmnopqrstuvwxyz"
LETTERS_PT = "abcdefghijlmnopqrstuvxz"  # Portuguese legislative lists skip k, w and y


def _next_letters(label):
    out = set()
    for alphabet in (LETTERS, LETTERS_PT):
        if len(label) == 1 and label in alphabet and alphabet.index(label) + 1 < len(alphabet):
            out.add(alphabet[alphabet.index(label) + 1])
    return out


def _slug(label):
    return label.lower().replace("ú", "u")


class _Ctx:
    """One structural context: the text itself, or an amending quotation inside it."""

    def __init__(self, prefix, quoted, parent_path):
        self.prefix, self.quoted, self.parent_path = prefix, quoted, parent_path
        self.headings = []   # open headings: (rank, path)
        self.stack = []      # open article / number / alínea / subalínea nodes
        self.letters = {}    # holder path -> expected next alínea letters


def _regions(norma, lines):
    """[(first line, last line + 1, path prefix, annexes are passages)] to structure, per the module docstring."""
    is_act = bool(ACT_SHORT.match(norma["short"]))
    depth, annex = 0, None
    for i, line in enumerate(lines):
        if depth == 0 and ANNEX_LINE.match(line.strip()):
            annex = i
            break
        depth += line.count("«") - line.count("»")
    if is_act:
        return [(0, annex if annex is not None else len(lines), "", False)]
    if annex is None:
        return [(0, len(lines), "", True)]
    return [(0, annex, "dl.", False), (annex + 1, len(lines), "", True)]


def parse(lines, first, last, prefix, annexes=False):
    """The nodes of lines[first:last]: dicts {path, kind, label, parent, start_line, last_line, quoted}. With annexes, an
    "Anexo N" line outside a quotation opens an anexo passage (DECISIONS D27) that holds numbers and alíneas."""
    nodes, by_path = [], {}
    root = _Ctx(prefix, False, None)
    contexts = [root]
    depth, quotes, started = 0, {}, False

    def join(base, part):
        return f"{base}{part}" if base.endswith(".") or not base else f"{base}.{part}"

    def add(i, path, kind, label, parent, quoted):
        if path in by_path:
            raise ValueError(f"line {i + 1}: duplicate passage {path!r} ({lines[i][:80]!r})")
        node = {"path": path, "kind": kind, "label": label, "parent": parent, "start_line": i, "last_line": i, "quoted": quoted}
        nodes.append(node)
        by_path[path] = node
        return node

    def touch(i, ctx):
        for c in contexts:
            for n in c.stack:
                n["last_line"] = i
        if ctx.quoted and ctx.parent_path and ctx.parent_path in by_path:
            by_path[ctx.parent_path]["last_line"] = i

    for i in range(first, last):
        raw = lines[i]
        line = raw.strip()
        if not line:
            continue
        ctx = contexts[-1]
        if line.startswith(NOTE_PREFIX):
            if depth != 0:
                raise ValueError(f"line {i + 1}: a validity note inside a quotation")
            for c in contexts:
                c.stack.clear()  # a note closes the article it follows
            continue
        if depth == 0 and CLOSING.match(line):
            break
        opens, closes = raw.count("«"), raw.count("»")
        if depth == 0 and line.startswith("«") and opens > closes:
            holder = ctx.stack[-1] if ctx.stack else None
            if holder is None:
                raise ValueError(f"line {i + 1}: a quotation with no passage quoting it ({line[:80]!r})")
            n = quotes[holder["path"]] = quotes.get(holder["path"], 0) + 1
            ctx = _Ctx(join(holder["path"], f"q{n}") + ".", True, holder["path"])
            contexts.append(ctx)
        text = re.sub(r"»+\.?$", "", line.lstrip("«")).strip() if ctx.quoted else line
        depth += opens - closes
        h, a, nm, lt = HEADING.match(text), ARTICLE.match(text), NUMBER.match(text), LETTER.match(text)
        an = ANNEX_LINE.match(text) if annexes and not ctx.quoted else None
        if an:
            started = True
            ctx.stack.clear()
            ctx.headings.clear()
            numeral = text.split(" ", 1)[1].lower() if " " in text else ""
            node = add(i, join(ctx.prefix, f"anexo-{numeral}" if numeral else "anexo"), "anexo", text, None, False)
            ctx.stack.append(node)
            touch(i, ctx)
        elif h:
            started = True
            kind, rank = HEADING_KIND[h.group(1).lower()]
            ctx.stack.clear()
            while ctx.headings and ctx.headings[-1][0] >= rank:
                ctx.headings.pop()
            parent = ctx.headings[-1][1] if ctx.headings else ctx.parent_path
            label_slug = _slug(h.group(2)) + (f"-{h.group(3).lower()}" if h.group(3) else "")
            base = ctx.headings[-1][1] if ctx.headings else ctx.prefix
            path = join(base, f"{HEADING_SLUG[h.group(1).lower()]}-{label_slug}")
            node = add(i, path, kind, text, parent, ctx.quoted)
            nxt = lines[i + 1].strip() if i + 1 < last else ""
            if nxt and not (HEADING.match(nxt) or ARTICLE.match(nxt) or nxt.startswith(NOTE_PREFIX)):
                node["last_line"] = i + 1  # the heading's name
            ctx.headings.append((rank, path))
            touch(i, ctx)
        elif a:
            started = True
            ctx.stack.clear()
            parent = ctx.headings[-1][1] if ctx.headings else ctx.parent_path
            path = join(ctx.prefix, f"art{a.group(1)}" + (f"-{a.group(2).lower()}" if a.group(2) else ""))
            node = add(i, path, "artigo", text, parent, ctx.quoted)
            ctx.stack.append(node)
            touch(i, ctx)
        elif not started:
            pass  # preamble
        elif nm:
            art = next((n for n in reversed(ctx.stack) if n["kind"] in ("artigo", "anexo")), None)
            if art is None:
                raise ValueError(f"line {i + 1}: a number outside any article ({text[:80]!r})")
            while ctx.stack and RANK[ctx.stack[-1]["kind"]] >= RANK["numero"]:
                ctx.stack.pop()
            node = add(i, join(art["path"], nm.group(1).lower()), "numero", nm.group(1), art["path"], ctx.quoted)
            ctx.stack.append(node)
            touch(i, ctx)
        elif lt and ctx.stack:
            label = lt.group(1)
            holder = next((n for n in reversed(ctx.stack) if n["kind"] in ("numero", "artigo", "anexo")), None)
            expected = ctx.letters.get(holder["path"], {"a"})
            if label in expected or not ROMAN.match(label) or not any(n["kind"] == "alinea" for n in ctx.stack):
                while ctx.stack and RANK[ctx.stack[-1]["kind"]] >= RANK["alinea"]:
                    ctx.stack.pop()
                node = add(i, join(holder["path"], label), "alinea", f"{label})", holder["path"], ctx.quoted)
                ctx.letters[holder["path"]] = _next_letters(label)
            else:
                while ctx.stack and RANK[ctx.stack[-1]["kind"]] >= RANK["subalinea"]:
                    ctx.stack.pop()
                alinea = ctx.stack[-1]
                node = add(i, join(alinea["path"], label), "subalinea", f"{label})", alinea["path"], ctx.quoted)
            ctx.stack.append(node)
            touch(i, ctx)
        elif ctx.stack or (ctx.quoted and ctx.parent_path):
            touch(i, ctx)  # a body line of the open passage(s)
        if ctx.quoted and depth == 0:
            contexts.pop()
    if depth != 0:
        raise ValueError(f"unbalanced quotation at the end of the structured region (depth {depth})")
    return nodes


def _revoked(kind, text):
    """An article whose body (past the "Artigo" line and at most an epigraph) is a single revocation marker, or a
    number / alínea / subalínea whose text past its label is one."""
    lines = [l.strip().lstrip("«").rstrip("»") for l in text.split("\n") if l.strip()]
    if kind == "artigo":
        body = lines[1:]
        return 1 <= len(body) <= 2 and REVOKED.match(body[-1]) is not None
    if kind in ("numero", "alinea", "subalinea") and len(lines) == 1:
        return REVOKED.match(re.sub(r"^([0-9]+(?:-[A-Z])? - |[a-z]{1,4}\) )", "", lines[0])) is not None
    return False


def structure(norma: dict, raw_text: str, raw_id: str, version: str) -> list:
    lines = raw_text.split("\n")
    starts, pos = [], 0
    for line in lines:
        starts.append(pos)
        pos += len(line) + 1
    out = []
    recorded_at = now_utc()
    short = norma["short"]
    for first, last, prefix, annexes in _regions(norma, lines):
        for n in parse(lines, first, last, prefix, annexes):
            s, e = starts[n["start_line"]], starts[n["last_line"]] + len(lines[n["last_line"]])
            text = raw_text[s:e]
            revoked = _revoked(n["kind"], text)
            out.append({"id": f"{short}:{n['path']}", "revision": 1, "recorded_at": recorded_at, "norma": norma["id"],
                        "parent": f"{short}:{n['parent']}" if n["parent"] else None, "kind": n["kind"], "label": n["label"],
                        "versions": [{"version": version, "text": text, "raw": raw_id, "offsets": {"start": s, "end": e},
                                      "valid_from": version, "valid_to": None, "revoked": revoked}]})
    return out
