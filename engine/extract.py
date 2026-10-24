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


EXTRACTORS = {"dr-consolidated-fragments@1": dr_consolidated_fragments, "dr-article-history@1": dr_article_history,
              "dr-article-history@2": dr_article_history_v2, "eurlex-html@1": eurlex_html,
              "dr-html-blocks@1": dr_html_blocks, "utf-8@1": utf8}
