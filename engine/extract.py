"""Versioned extractors: raw bytes -> working text, byte-identical on every run (NORMALISE layer, DECISIONS D23).

    EXTRACTORS[id](raw: bytes) -> str      "dr-consolidated-fragments@1": the rendered DR consolidated-legislation page
                                           (headless Chrome DOM dump) -> one line per fragment: title, epigraph, text
                                           "dr-html-blocks@1": a rendered DR detail page -> one line per paragraph block
                                           "dr-article-history@1" / "@2": an opened history view (@2 also an annex's)
                                           "eurlex-html@1": an EUR-Lex Official Journal page -> date, title and ELI
                                           lines, then the enacting terms (Artigo N.º, points "1) ...", "a) ...")
                                           "utf-8@1": the bytes decoded as UTF-8, unchanged
An extractor raises when the bytes are not what it expects; nothing is stored then. No network, no model.
Copied from rjue-engine's extract module and versioned here.
"""
import re
from html.parser import HTMLParser

VERSION = "ccp-extract-0.1"
FRAGMENT_CLASSES = ("Fragmento_Titulo", "Fragmento_Epigrafe", "Fragmento_Texto")
LINE_BREAK_TAGS = {"div", "p", "br", "li", "tr"}
VOID = {"br", "img", "input", "meta", "link", "hr", "source"}


class _Fragments(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack, self.buf, self.lines = [], [], []

    def _inside(self):
        return any(self.stack)

    def handle_starttag(self, tag, attrs):
        cls = dict(attrs).get("class") or ""
        if tag == "br":
            if self._inside():
                self.buf.append("\n")
            return
        if tag in VOID:
            return
        self.stack.append(any(c in cls.split() for c in FRAGMENT_CLASSES))
        if self.stack[-1] and sum(self.stack) == 1:
            self.buf = []

    def handle_endtag(self, tag):
        if tag in VOID or not self.stack:
            return
        opened = self.stack.pop()
        if self._inside() and tag in LINE_BREAK_TAGS:
            self.buf.append("\n")
        if opened and not self._inside():
            for line in "".join(self.buf).split("\n"):
                line = re.sub(r"[ \t ]+", " ", line).strip()
                if line:
                    self.lines.append(line)

    def handle_data(self, data):
        if self._inside():
            self.buf.append(data)


def dr_consolidated_fragments(raw: bytes) -> str:
    parser = _Fragments()
    parser.feed(raw.decode("utf-8"))
    if not any(line.startswith("Artigo ") for line in parser.lines):
        raise ValueError("no article fragments: not a rendered DR consolidated-legislation page")
    return "\n".join(parser.lines) + "\n"


BLOCK_TAGS = {"p", "li", "h1", "h2", "h3", "h4", "h5", "h6", "td", "th", "div"}
DROP = {"script", "style", "noscript", "template", "svg", "head"}


class _Blocks(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.blocks, self.buf, self.drop = [], [], 0

    def flush(self):
        line = re.sub(r"[ \t ]+", " ", "".join(self.buf)).strip()
        if line:
            self.blocks.append(line)
        self.buf = []

    def handle_starttag(self, tag, attrs):
        if tag in DROP:
            self.drop += 1
        elif tag == "br" and not self.drop:
            self.buf.append("\n")
        elif tag in BLOCK_TAGS and not self.drop:
            self.flush()

    def handle_endtag(self, tag):
        if tag in DROP:
            self.drop = max(0, self.drop - 1)
        elif tag in BLOCK_TAGS and not self.drop:
            self.flush()

    def handle_data(self, data):
        if not self.drop:
            self.buf.append(data)


def dr_html_blocks(raw: bytes) -> str:
    parser = _Blocks()
    parser.feed(raw.decode("utf-8"))
    parser.flush()
    lines = [l for block in parser.blocks for l in block.split("\n") if l.strip()]
    if not lines:
        raise ValueError("no paragraph blocks: not a rendered DR detail page")
    return "\n".join(l.strip() for l in lines) + "\n"


def utf8(raw: bytes) -> str:
    return raw.decode("utf-8")


NOTE_CLASS = "texto-alteracao-container"


class _History(_Fragments):
    """Fragments plus the validity notes, in document order; a note line is prefixed with NOTA_PREFIX."""

    def handle_starttag(self, tag, attrs):
        cls = dict(attrs).get("class") or ""
        if tag == "br":
            if self._inside():
                self.buf.append("\n")
            return
        if tag in VOID:
            return
        kind = "N" if NOTE_CLASS in cls.split() else (any(c in cls.split() for c in FRAGMENT_CLASSES) or None)
        self.stack.append(kind)
        if kind and sum(1 for x in self.stack if x) == 1:
            self.buf, self.kind = [], kind

    def handle_endtag(self, tag):
        if tag in VOID or not self.stack:
            return
        opened = self.stack.pop()
        if self._inside() and tag in LINE_BREAK_TAGS:
            self.buf.append("\n")
        if opened and not self._inside():
            for line in "".join(self.buf).split("\n"):
                line = re.sub(r"[ \t\u00a0]+", " ", line).strip()
                if line:
                    self.lines.append((NOTA_PREFIX + line) if opened == "N" else line)


NOTA_PREFIX = "NOTA: "


def dr_article_history(raw: bytes) -> str:
    """The opened "Ver alterações ao texto" view of one article (tools/capture_dr_history.mjs) -> the versions, newest
    first: for each, the title, epigraph and text lines, then the note that produced it ("NOTA: Alterado pelo/a ... em
    vigor a partir de AAAA-MM-DD"); the oldest ("Versão inicial") has no note. Also works on the consolidated page,
    where each article's current text is followed by all its notes."""
    parser = _History()
    parser.feed(raw.decode("utf-8"))
    if not any(line.startswith("Artigo ") for line in parser.lines):
        raise ValueError("no article fragments: not a rendered DR page")
    return "\n".join(parser.lines) + "\n"


ANNEX_TITLE = re.compile(r"^Anexo [IVXLC]+$")


def dr_article_history_v2(raw: bytes) -> str:
    """dr-article-history@1 with one change: the history view of one of a code's annexes ("Anexo XII", no "Artigo"
    line) is accepted too. Same lines, same order, same note prefix."""
    parser = _History()
    parser.feed(raw.decode("utf-8"))
    if not any(line.startswith("Artigo ") or ANNEX_TITLE.match(line) for line in parser.lines):
        raise ValueError("no article or annex fragments: not a rendered DR page")
    return "\n".join(parser.lines) + "\n"


EURLEX_HEAD = {"oj-hd-date", "oj-doc-ti", "oj-doc-end"}
EURLEX_ART = {"oj-ti-art", "oj-sti-art", "oj-normal", "oj-final"}
EURLEX_LABEL = re.compile(r"^(?:[0-9]+|[a-z]{1,4}|[ivxlc]+)\)$")


class _EurLex(HTMLParser):
    """The Official Journal HTML of EUR-Lex (div#docHtml): the head lines (date, title, ELI) and every line of the
    enacting terms (div id art_N): article title, its own lines, and each numbered or lettered point as one line."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack, self.lines, self.buf, self.keep, self.label, self.sup = [], [], None, None, None, 0

    def _inside(self, pred):
        return any(pred(t, c, i) for t, c, i in self.stack)

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        cls, ident = set((a.get("class") or "").split()), a.get("id") or ""
        if tag in VOID:
            return
        self.stack.append((tag, cls, ident))
        if tag == "span" and "oj-super" in cls:
            self.sup += 1
        if tag != "p" or not self._inside(lambda t, c, i: i == "docHtml"):
            return
        in_art = self._inside(lambda t, c, i: t == "div" and i.startswith("art_"))
        if cls & EURLEX_HEAD or (in_art and cls & EURLEX_ART):
            self.buf, self.keep = [], True

    def handle_endtag(self, tag):
        if tag in VOID or not self.stack:
            return
        t, cls, _ = self.stack.pop()
        if t == "span" and "oj-super" in cls:
            self.sup -= 1
        if t == "p" and self.keep:
            line = re.sub(r"[ \t\u00a0]+", " ", "".join(self.buf)).strip()
            self.buf, self.keep = None, None
            if not line:
                return
            if EURLEX_LABEL.match(line):  # the label cell of a point: it opens the next line
                self.label = line
                return
            self.lines.append(f"{self.label} {line}" if self.label else line)
            self.label = None

    def handle_data(self, data):
        if self.keep:
            # the ordinal indicator is printed as a superscript "o" (1.o, 4.o): it is the º of the text
            self.buf.append("º" if self.sup and data.strip() == "o" else data)


def eurlex_html(raw: bytes) -> str:
    parser = _EurLex()
    parser.feed(raw.decode("utf-8"))
    if not any(line.startswith("Artigo ") for line in parser.lines):
        raise ValueError("no article in the enacting terms: not an EUR-Lex Official Journal page")
    return "\n".join(parser.lines) + "\n"


EURLEX_C_SKIP = {"arrow", "disclaimer", "reference", "hd-modifiers", "footnote", "title-toc", "toc-item", "hd-toc-1", "hd-toc-2", "hd-toc-3",
                 "oj-note", "modref"}
EURLEX_C_MARK = re.compile(r"\s*(?:[►▼][A-Z][0-9]*|◄)\s*")  # the consolidation's amendment markers: ►M6 … ◄, ▼B, ▼M1
EURLEX_C_LETTER = re.compile(r"^(?:[a-z]{1,4}|[ivxlc]+)\)$")
EURLEX_C_NUMBER = re.compile(r"^[0-9]+\.$")
EURLEX_C_HEAD = {"title-doc-first", "title-doc-oj-reference", "oj-doc-ti", "oj-hd-date"}
EURLEX_C_ENACTING = re.compile(r"^(?:tis|prt|cpt|sct|art)_")  # the ELI ids of the enacting terms' subdivisions
EURLEX_C_ANNEX = re.compile(r"^ANEXO(?: [IVXLC]+)?$")
EURLEX_C_START = {"title-division-1", "title-article-norm", "oj-ti-section-1", "oj-ti-art"}


class _EurLexConsolidated(HTMLParser):
    """An EU directive in the Publications Office's XHTML: a consolidated version (CONVEX: title-article-norm, norm,
    grid-list points) or the Official Journal text as adopted (oj-ti-art, oj-normal, points in table cells). The head
    lines (title, OJ date or reference), then the enacting terms, from the first ELI subdivision (tis_, cpt_, art_ …),
    or in a version without ELI ids the first heading or article, up to the first annex. A paragraph number (span no-parag «1.») or a point label («a)» in its own cell) opens the
    next line; a numbered point «1)» inside a paragraph stays in its text as «(1)», so the definitions of a number stay
    one passage. Amendment markers and footnotes are not text; the ordinal printed as «o» is the «º» of the text."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack, self.lines, self.buf, self.label, self.sup = [], [], [], None, 0
        self.body = self.done = False
        self.skip = 0

    def _flush(self):
        line = EURLEX_C_MARK.sub(" ", "".join(self.buf))
        line = re.sub(r"[ \t\u00a0\n]+", " ", line).strip()
        line = re.sub(r"\b([0-9]+)\.o\b", r"\1.º", re.sub(r"\bn\.o\b", "n.º", line))  # the OJ prints the ordinal indicator as a plain «o»
        self.buf = []
        if not line:
            return
        if self.body and (EURLEX_C_LETTER.match(line) or EURLEX_C_NUMBER.match(line) or re.match(r"^[0-9]+\)$", line)):
            self.label = f"({line[:-1]})" if re.match(r"^[0-9]+\)$", line) else line  # a label cell (OJ table): it opens the next line
            return
        if self.body and EURLEX_C_ANNEX.match(line):
            self.done = True
            return
        if self.body and not self.label:  # a version that prints a numbered point inline («1) …»): part of its paragraph, as «(1)»
            line = re.sub(r"^([0-9]+)\) ", r"(\1) ", line)
        if self.label:
            line, self.label = f"{self.label} {line}", None
        self.lines.append(line)

    def handle_starttag(self, tag, attrs):
        if self.done or tag in VOID:
            if tag == "br" and self.body and not self.done:
                self.buf.append(" ")
            return
        a = dict(attrs)
        cls, ident = set((a.get("class") or "").split()), a.get("id") or ""
        skip = bool(cls & EURLEX_C_SKIP) or (tag == "a" and (a.get("href") or "").startswith("#"))
        self.stack.append((tag, cls, skip))
        self.skip += skip
        if tag == "span" and cls & {"superscript", "oj-super"}:
            self.sup += 1
        if ident.startswith("anx_") or "title-annex-1" in cls:
            self._flush()
            self.done = True
            return
        if not self.body and ((tag == "div" and EURLEX_C_ENACTING.match(ident)) or cls & EURLEX_C_START):  # older versions have no ELI ids
            self._flush()
            self.body = True
        if tag in ("p", "td") or (tag == "div" and "inline-element" in cls):
            self._flush()
        if tag == "span" and "no-parag" in cls:
            self._flush()

    def handle_endtag(self, tag):
        if tag in VOID or not self.stack:
            return
        t, cls, skip = self.stack.pop()
        self.skip -= skip
        if t == "span" and cls & {"superscript", "oj-super"}:
            self.sup -= 1
        if self.done:
            return
        if t == "span" and ("no-parag" in cls or self._in_list_cell()):
            label = re.sub(r"\s+", "", "".join(self.buf))
            self.buf = []
            if EURLEX_C_NUMBER.match(label) or EURLEX_C_LETTER.match(label):
                self.label = label
            elif re.match(r"^[0-9]+\)$", label):
                self.label = f"({label[:-1]})"  # a numbered point inside a paragraph is part of its text
            elif label:
                self.label = label
            return
        if t in ("p", "td") or (t == "div" and "inline-element" in cls):
            if self.body or (EURLEX_C_HEAD & cls):
                self._flush()
            else:
                self.buf = []

    def _in_list_cell(self):
        return any(t == "div" and "grid-list-column-1" in c for t, c, _ in self.stack)

    def handle_data(self, data):
        if self.done or self.skip:
            return
        if not self.body and not any((EURLEX_C_HEAD & c) for _, c, _ in self.stack):
            return
        self.buf.append("º" if self.sup and data.strip() == "o" else data)


def eurlex_consolidated(raw: bytes) -> str:
    parser = _EurLexConsolidated()
    parser.feed(raw.decode("utf-8"))
    parser._flush()
    if not any(re.match(r"^Artigo [0-9]+\.º$", line) for line in parser.lines):
        raise ValueError("no article in the enacting terms: not a consolidated text of the Publications Office")
    return "\n".join(parser.lines) + "\n"


EXTRACTORS = {"dr-consolidated-fragments@1": dr_consolidated_fragments, "dr-article-history@1": dr_article_history,
              "dr-article-history@2": dr_article_history_v2, "eurlex-html@1": eurlex_html,
              "eurlex-consolidated@1": eurlex_consolidated, "dr-html-blocks@1": dr_html_blocks, "utf-8@1": utf8}
