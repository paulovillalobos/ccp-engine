"""The quote grammar: the family-A reader can only quote words that are in a passage it may cite.

    grammar(schema, context) -> str                      an xgrammar EBNF grammar (GBNF style, «root ::= …»), given to
                                                         vLLM as StructuredOutputsParams(grammar=…)
    accepts(answer_text, schema, context) -> bool        the same language, checked in plain Python (no xgrammar)
    why_not(answer_text, schema, context) -> str | None  where and why a text is outside it

With the answer schema alone, guided decoding keeps AMALIA to the JSON shape but not to the text: on v12's dev set, 11 of
her answers quote words that are nowhere in the text and 7 cite a passage that does not hold them. The grammar's language
is the compact JSON the schema allows (no whitespace, keys in each object's required order, the same enums, consts,
types, item counts and nullables), with one change: a quote object {"texto", "de"} is a choice of passages. In the branch
of passage P, «texto» is a token-aligned piece of P's text as P writes it (tokens: maximal runs of word characters, and
each other non-space character on its own; what lies between two tokens is the text's own), JSON-escaped, and «de» is P.
Each passage's pieces take one rule per token: t_i ::= tok_i (sep_i t_i+1)?, and texto ::= t_1 | t_2 | … .

The passages a slot may cite are the checker's (tools/read_rules_v3.py check() and _sources()):
- a condition: CONDITION_ROLES; with op ne or not_in, also the article's other passages (vizinho) when the target's text
  holds one of the vocabulary's rest_phrases («nos restantes casos»): the condition object is split by its op;
- a parameter (every «fontes» of params, the nullable counted_from and usual_days included): PARAM_ROLES, and for a
  limiar's field also remissao_epigrafe;
- «não tipável»: alvo, proemio, remissao, epigrafe and titulo (L3: a title can be the reason).
The checker compares words after norm() (case, spacing, «» and old spellings aside); the grammar asks for the text's own
characters, which is stricter: a quote the grammar admits always passes the checker's «não está em» test, and its «de» is
never a passage the slot may not cite.

readers/ imports neither engine/ nor tools/ (DECISIONS D38), so the role sets and the target's rest test are copied here;
tests/test_quote_grammar.py holds them equal to the checker's, and checks the gold answers and the grammar's text.
Stdlib only; schemas/vocabulario-v3.json is read as data. A schema keyword the grammar does not know is an error, never
ignored.
"""
import json
import re
from functools import lru_cache
from pathlib import Path

VOCABULARY = Path(__file__).resolve().parent.parent / "schemas/vocabulario-v3.json"
CONDITION_ROLES = frozenset({"alvo", "proemio", "remissao", "remissao_epigrafe", "epigrafe", "titulo"})  # read_rules_v3
PARAM_ROLES = frozenset({"alvo", "proemio", "remissao", "epigrafe"})  # read_rules_v3
SLOT_ROLES = {"condicao": CONDITION_ROLES, "condicao_resto": CONDITION_ROLES | {"vizinho"}, "param": PARAM_ROLES,
              "param_field": PARAM_ROLES | {"remissao_epigrafe"},
              "nao_tipavel": frozenset({"alvo", "proemio", "remissao", "epigrafe", "titulo"})}
REST_OPS = ("ne", "not_in")  # check(): rest_ok=op in ("ne", "not_in") and rest
TOKEN = re.compile(r"\w+|[^\w\s]")
KEYWORDS = {"type", "properties", "required", "additionalProperties", "items", "minItems", "maxItems", "enum", "const",
            "anyOf", "minimum", "pattern"}
ANNOTATIONS = {"title", "description", "$schema", "examples"}


# ---- the text ---------------------------------------------------------------------------------------------------------
def tokens(text):
    """(start, end) of each token of text."""
    return [m.span() for m in TOKEN.finditer(text or "")]


def aligned(text, piece):
    """True when piece is text[a:b] with a a token's start and b a token's end."""
    if not piece or not text:
        return False
    sp = tokens(text)
    starts, ends = {a for a, _ in sp}, {b for _, b in sp}
    k = text.find(piece)
    while k >= 0:
        if k in starts and k + len(piece) in ends:
            return True
        k = text.find(piece, k + 1)
    return False


@lru_cache(maxsize=1)
def _vocabulary():
    return json.loads(VOCABULARY.read_text(encoding="utf-8"))


def _norm(s):
    """read_rules_v3.norm, copied."""
    s = s.replace(" ", " ").replace("’", "'").replace("«", '"').replace("»", '"').replace("“", '"').replace("”", '"')
    s = re.sub(r"\s+", " ", s).strip().lower()
    for a, b in _vocabulary()["old_spelling"].items():
        s = re.sub(rf"(?<!\w){a}(?!\w)", b, s)
    return s


def rest(context):
    """The checker's rest test: the target's text holds a rest phrase (read_rules_v3.check, with contains())."""
    t = _norm(context["allowed"][context["alvo"]])
    return any(w.strip() and _norm(w) in t for w in _vocabulary()["rest_phrases"])


def citable(context, slot, enum=None):
    """The passages a quote in slot may cite, in id order: an allowed role, in the schema's «de» enum, a text with words."""
    roles, allowed = context["roles"], context["allowed"]
    return [p for p in sorted(roles) if roles[p] in SLOT_ROLES[slot] and (enum is None or p in enum) and tokens(allowed.get(p))]


# ---- where a quote sits -------------------------------------------------------------------------------------------------
def _slot(lpath, rtype):
    if lpath == ("regras", "condicoes", "fontes"):
        return "condicao"
    if len(lpath) == 3 and lpath[:2] == ("regras", "fontes"):
        return "param_field" if rtype == "limiar" and lpath[2] == "field" else "param"
    if lpath == ("nao_tipavel", "fontes"):
        return "nao_tipavel"
    raise ValueError(f"a quote object at {'.'.join(lpath) or '$'}: the checker reads no quotes there")


def _rtype(schema):
    try:
        enum = schema["properties"]["regras"]["items"]["properties"]["tipo"]["enum"]
    except (KeyError, TypeError):
        return None
    if len(enum) != 1:
        raise ValueError(f"tipo {enum}: one rule type per schema")
    return enum[0]


def _variants(s, lpath, is_rest):
    """A condition object as the checker reads it: [(schema, {property: slot})]. When the target holds a rest phrase,
    two objects: op ne / not_in with quotes from vizinho passages too, and every other op without them."""
    if lpath != ("regras", "condicoes") or not is_rest:
        return [(s, {})]
    props = s["properties"]
    op = props.get("op")
    if not isinstance(op, dict) or "enum" not in op or "fontes" not in props:
        raise ValueError("regras.condicoes: an op enum and fontes are needed to split the condition by its op")
    out = []
    for ops, slot in (([x for x in op["enum"] if x in REST_OPS], "condicao_resto"), ([x for x in op["enum"] if x not in REST_OPS], "condicao")):
        if ops:
            out.append(({**s, "properties": {**props, "op": {**op, "enum": ops}}}, {"fontes": slot}))
    return out


def _is_quote(s):
    return isinstance(s.get("properties"), dict) and set(s["properties"]) == {"texto", "de"}


# ---- schema checks shared by grammar() and accepts() ------------------------------------------------------------------
def _clean(s, where):
    if not isinstance(s, dict):
        raise ValueError(f"{where}: a schema must be an object")
    s = {k: v for k, v in s.items() if k not in ANNOTATIONS}
    unknown = set(s) - KEYWORDS
    if unknown:
        raise ValueError(f"{where}: schema keywords the grammar does not know: {sorted(unknown)}")
    t = s.get("type")
    allowed = {"object": {"properties", "required", "additionalProperties"}, "array": {"items", "minItems", "maxItems"},
               "string": {"pattern"}, "integer": {"minimum"}, "number": set(), "boolean": set(), "null": set()}
    if "anyOf" in s and set(s) != {"anyOf"}:
        raise ValueError(f"{where}: anyOf with other keywords")
    if isinstance(t, str):
        extra = set(s) - {"type", "enum", "const"} - allowed.get(t, set())
        if t not in allowed or extra:
            raise ValueError(f"{where}: type {t} with {sorted(extra)}")
    elif t is not None and not isinstance(t, list):
        raise ValueError(f"{where}: type {t!r}")
    if t == "object":
        props, req = s.get("properties", {}), s.get("required", [])
        if s.get("additionalProperties") is not False:
            raise ValueError(f"{where}: additionalProperties must be false")
        if sorted(props) != sorted(req) or len(set(req)) != len(req):
            raise ValueError(f"{where}: every property must be required, once (keys are written in the required order)")
    if t == "integer" and s.get("minimum") not in (None, 0, 1):
        raise ValueError(f"{where}: integer minimum {s.get('minimum')}")
    if t == "array" and not isinstance(s.get("items"), dict):
        raise ValueError(f"{where}: an array needs one items schema")
    return s


def _check_schema(s, where="$"):
    """_clean() over the whole schema, so accepts() refuses what grammar() refuses, whatever the text."""
    s = _clean(s, where)
    for i, x in enumerate(s.get("anyOf", [])):
        _check_schema(x, f"{where}.anyOf[{i}]")
    for k, x in (s.get("properties") or {}).items():
        _check_schema(x, f"{where}.{k}")
    if isinstance(s.get("items"), dict):
        _check_schema(s["items"], f"{where}[]")
    if "pattern" in s:
        _pattern(s["pattern"])


def _fits(v, t):
    """Does the JSON value v have type t (enum and const values outside the type are not in the language)?"""
    if t is None:
        return True
    ts = t if isinstance(t, list) else [t]
    kind = ("null" if v is None else "boolean" if isinstance(v, bool) else "integer" if isinstance(v, int) else
            "number" if isinstance(v, float) else "string" if isinstance(v, str) else "array" if isinstance(v, list) else "object")
    return kind in ts or (kind == "integer" and "number" in ts) or (kind == "number" and "integer" in ts and float(v).is_integer())


def _json(v):
    return json.dumps(v, ensure_ascii=False, separators=(",", ":"))


def _pattern(p):
    """A pattern of the small kind the schema uses (^\\d{4}-\\d{2}-\\d{2}$): [(class or char, min, max)], anchored, each
    atom a character JSON writes as itself. Anything else is an error."""
    if not (p.startswith("^") and p.endswith("$")):
        raise ValueError(f"pattern {p}: only anchored patterns")
    body, i, atoms = p[1:-1], 0, []
    while i < len(body):
        c = body[i]
        if c == "\\" and body[i + 1:i + 2] == "d":
            atom, i = ("class", "0-9"), i + 2
        elif c == "\\" and body[i + 1:i + 2] and not body[i + 1].isalnum():
            atom, i = ("char", body[i + 1]), i + 2
        elif c == "[":
            j = body.index("]", i)
            inner = body[i + 1:j]
            if not inner or not re.fullmatch(r"(?:[0-9A-Za-z](?:-[0-9A-Za-z])?)+", inner):
                raise ValueError(f"pattern {p}: class [{inner}]")
            atom, i = ("class", inner), j + 1
        elif c in ".()|*+?{}^$\\":
            raise ValueError(f"pattern {p}: {c!r} is not handled")
        else:
            atom, i = ("char", c), i + 1
        if atom[0] == "char" and (atom[1] in '"\\' or ord(atom[1]) < 0x20):
            raise ValueError(f"pattern {p}: {atom[1]!r} is written escaped in JSON")
        lo, hi = 1, 1
        m = re.match(r"\{(\d+)(,(\d*))?\}|[?*+]", body[i:])
        if m:
            q = m.group(0)
            lo, hi = {"?": (0, 1), "*": (0, None), "+": (1, None)}.get(q, (None, None))
            if lo is None:
                lo = int(m.group(1))
                hi = lo if m.group(2) is None else (int(m.group(3)) if m.group(3) else None)
            i += len(q)
        atoms.append((atom, lo, hi))
    return atoms


def _pattern_regex(p):
    out = []
    for (kind, x), lo, hi in _pattern(p):
        out.append((f"[{x}]" if kind == "class" else re.escape(x)) + ("" if (lo, hi) == (1, 1) else f"{{{lo},{'' if hi is None else hi}}}"))
    return "".join(out)


# ---- the grammar --------------------------------------------------------------------------------------------------------
def _ebnf(raw):
    """An EBNF string literal that matches the characters raw: backslash and double quote escaped, control characters
    as \\u escapes, everything else (« », accents, º) as itself."""
    out = []
    for c in raw:
        if c in '"\\':
            out.append("\\" + c)
        elif ord(c) < 0x20 or 0x7f <= ord(c) <= 0x9f:
            out.append(f"\\u{ord(c):04x}")
        else:
            out.append(c)
    return '"' + "".join(out) + '"'


def _escaped(text):
    """text as it is written inside a JSON string (json.dumps, ensure_ascii=False)."""
    return json.dumps(text, ensure_ascii=False)[1:-1]


class _Seq:
    """A sequence of EBNF atoms; adjacent literals are joined."""

    def __init__(self, *atoms):
        self.items = []
        for a in atoms:
            self.add(a)

    def add(self, atom):
        kind, x = atom
        if kind == "lit" and self.items and self.items[-1][0] == "lit":
            self.items[-1] = ("lit", self.items[-1][1] + x)
        elif kind != "lit" or x:
            self.items.append(atom)
        return self

    def render(self):
        return " ".join(_ebnf(x) if k == "lit" else x for k, x in self.items) or '""'


def _render(atom):
    return _ebnf(atom[1]) if atom[0] == "lit" else atom[1]


SHARED = {"string": '"\\"" char* "\\""', "char": '[^\\0-\\x1f\\"\\\\] | "\\\\" (["\\\\/bfnrt] | "u" hex hex hex hex)',
          "hex": "[0-9a-fA-F]", "number": '"-"? ("0" | [1-9] [0-9]*) ("." [0-9]+)? ([eE] ("+" | "-")? [0-9]+)?',
          "integer": '"-"? ("0" | [1-9] [0-9]*)', "integer0": '"0" | [1-9] [0-9]*', "integer1": "[1-9] [0-9]*",
          "boolean": '"true" | "false"'}
NEEDS = {"string": ["char"], "char": ["hex"]}


class _Grammar:
    def __init__(self, schema, context):
        self.context, self.rtype, self.rest = context, _rtype(schema), rest(context)
        self.rules, self.by_body, self.texts = {}, {}, {}

    def add(self, name, body, share=True):
        """A rule; with share, a rule with the same body is reused, and a taken name gets a suffix. A passage's rules
        are not shared and keep their names (they refer to each other by them)."""
        if share and body in self.by_body:
            return self.by_body[body]
        base, k = name, 1
        while share and (name in self.rules or name in SHARED or re.fullmatch(r"t\d+_\d+|texto\d+", name)):
            k += 1
            name = f"{base}_{k}"
        if name in self.rules:
            raise ValueError(f"rule {name} twice")
        self.rules[name] = body
        if share:
            self.by_body[body] = name
        return name

    def shared(self, name):
        for n in [name] + NEEDS.get(name, []):
            if n not in self.rules:
                self.rules[n] = SHARED[n]
                for m in NEEDS.get(n, []):
                    self.shared(m)
        return ("rule", name)

    def value(self, s, lpath, nm, slot=None):
        """An atom ("lit", raw json) or ("rule", ebnf) for the compact JSON of s, or None when s allows no text."""
        s = _clean(s, nm)
        if "anyOf" in s:
            alts = [a for a in (self.value(x, lpath, f"{nm}_{i}", slot) for i, x in enumerate(s["anyOf"])) if a is not None]
            return None if not alts else alts[0] if len(alts) == 1 else ("rule", self.add(nm, " | ".join(_render(a) for a in alts)))
        if "const" in s or "enum" in s:
            vals = [_json(v) for v in ([s["const"]] if "const" in s else s["enum"]) if _fits(v, s.get("type"))
                    and ("enum" not in s or "const" not in s or v in s["enum"])]
            vals = list(dict.fromkeys(vals))
            return None if not vals else ("lit", vals[0]) if len(vals) == 1 else ("rule", self.add(nm, " | ".join(_ebnf(v) for v in vals)))
        t = s.get("type")
        if isinstance(t, list):
            return self.value({"anyOf": [{**s, "type": x} for x in t]}, lpath, nm, slot)
        if t == "object":
            return self.object(s, lpath, nm, slot)
        if t == "array":
            return self.array(s, lpath, nm, slot)
        if t == "string":
            if "pattern" not in s:
                return self.shared("string")
            seq = _Seq(("lit", '"'))
            for (kind, x), lo, hi in _pattern(s["pattern"]):
                a = ("rule", f"[{x}]") if kind == "class" else ("lit", x)
                for _ in range(lo):
                    seq.add(a)
                if hi is None:
                    seq.add(("rule", f"{_render(a)}*"))
                elif hi > lo:
                    seq.add(("rule", self.optional([], a, hi - lo)))
            return ("rule", self.add(nm, seq.add(("lit", '"')).render()))
        if t == "integer":
            return self.shared({None: "integer", 0: "integer0", 1: "integer1"}[s.get("minimum")])
        if t == "number":
            return self.shared("number")
        if t == "boolean":
            return self.shared("boolean")
        if t == "null":
            return ("lit", "null")
        raise ValueError(f"{nm}: no type")

    def optional(self, prefix, a, k):
        """Up to k more of a, each after prefix: (p a (p a (…)?)?)?"""
        out = ""
        for _ in range(k):
            out = "(" + _Seq(*prefix, a).render() + (" " + out if out else "") + ")?"
        return out

    def object(self, s, lpath, nm, slot):
        if _is_quote(s):
            return self.quote(s, lpath, nm, slot)
        req, alts = s["required"], []
        for v, slots in _variants(s, lpath, self.rest):
            seq = _Seq(("lit", "{" if req else "{}"))
            for i, k in enumerate(req):
                a = self.value(v["properties"][k], lpath + (k,), k if nm == "root" else f"{nm}_{k}", slots.get(k))
                if a is None:
                    seq = None
                    break
                seq.add(("lit", ("," if i else "") + _json(k) + ":")).add(a)
            if seq is not None:
                alts.append(seq.add(("lit", "}" if req else "")).render())
        return ("rule", self.add(nm, " | ".join(alts))) if alts else None

    def array(self, s, lpath, nm, slot):
        mn, mx = s.get("minItems", 0), s.get("maxItems")
        if mx is not None and mx < mn:
            return None
        item = self.value(s["items"], lpath, f"{nm}_item", slot)
        if item is None or mx == 0:
            return ("lit", "[]") if mn == 0 else None
        comma = ("lit", ",")
        more = (("rule", "(" + _Seq(comma, item).render() + ")*"),) if mx is None else \
            ((("rule", self.optional([comma], item, mx - max(mn, 1))),) if mx > max(mn, 1) else ())
        if mn == 0:
            seq = _Seq(("lit", "["), ("rule", "(" + _Seq(item, *more).render() + ")?"), ("lit", "]"))
        else:
            seq = _Seq(("lit", "["), item)
            for _ in range(mn - 1):
                seq.add(comma).add(item)
            for a in more:
                seq.add(a)
            seq.add(("lit", "]"))
        return ("rule", self.add(nm, seq.render()))

    def quote(self, s, lpath, nm, slot):
        slot = slot or _slot(lpath, self.rtype)
        props, req = s["properties"], s["required"]
        texto, de = _clean(props["texto"], f"{nm}.texto"), _clean(props["de"], f"{nm}.de")
        if texto != {"type": "string"} or de.get("type") != "string" or set(de) - {"type", "enum"}:
            raise ValueError(f"{nm}: a quote is {{texto: string, de: string enum}}")
        alts = []
        for p in citable(self.context, slot, de.get("enum")):
            seq = _Seq(("lit", "{"))
            for i, k in enumerate(req):
                seq.add(("lit", ("," if i else "") + _json(k) + ":"))
                if k == "texto":
                    seq.add(("lit", '"')).add(("rule", self.passage(p))).add(("lit", '"'))
                else:
                    seq.add(("lit", _json(p)))
            alts.append(seq.add(("lit", "}")).render())
        return ("rule", self.add(f"quote_{slot}", " | ".join(alts))) if alts else None

    def passage(self, pid):
        """texto<k> ::= t<k>_0 | t<k>_1 | …, t<k>_i ::= tok_i (sep_i t<k>_i+1)?: the token-aligned pieces of pid's text."""
        text = self.context["allowed"][pid]
        if text in self.texts:
            return self.texts[text]
        k = len(self.texts)
        sp = tokens(text)
        names = [f"t{k}_{i}" for i in range(len(sp))]
        for i, (a, b) in enumerate(sp):
            tok = _ebnf(_escaped(text[a:b]))
            if i + 1 == len(sp):
                body = tok
            else:
                sep = text[b:sp[i + 1][0]]
                body = f"{tok} ({_ebnf(_escaped(sep))} {names[i + 1]})?" if sep else f"{tok} {names[i + 1]}?"
            self.add(names[i], body, share=False)
        self.texts[text] = self.add(f"texto{k}", " | ".join(names), share=False)
        return self.texts[text]


def grammar(schema, context):
    """The EBNF text: root first, one rule per line."""
    _check_schema(schema)
    g = _Grammar(schema, context)
    top = g.value(schema, (), "root")
    if top is None:
        raise ValueError("the schema and context allow no answer")
    if top != ("rule", "root"):
        g.rules = {"root": _render(top), **{k: v for k, v in g.rules.items() if k != "root"}}
    lines = [f"root ::= {g.rules['root']}"] + [f"{n} ::= {b}" for n, b in g.rules.items() if n != "root"]
    return "\n".join(lines) + "\n"


# ---- the same language in Python --------------------------------------------------------------------------------------
STRING = re.compile(r'"(?:[^"\\\x00-\x1f]|\\(?:["\\/bfnrt]|u[0-9a-fA-F]{4}))*"')
NUMBER = re.compile(r"-?(?:0|[1-9][0-9]*)(?:\.[0-9]+)?(?:[eE][+-]?[0-9]+)?")
INTEGER = {None: re.compile(r"-?(?:0|[1-9][0-9]*)"), 0: re.compile(r"(?:0|[1-9][0-9]*)"), 1: re.compile(r"[1-9][0-9]*")}


class _No(Exception):
    def __init__(self, pos, why):
        super().__init__(why)
        self.pos, self.why = pos, why


class _Reader:
    """A recursive-descent reading of the text against the schema: each value's extent is fixed by the text (compact
    JSON), so the first alternative that reads is the one."""

    def __init__(self, text, schema, context):
        self.t, self.context, self.rtype, self.rest = text, context, _rtype(schema), rest(context)
        self.citable = {}

    def lit(self, raw, i):
        if not self.t.startswith(raw, i):
            raise _No(i, f"expected {raw!r}, found {self.t[i:i + 20]!r}")
        return i + len(raw)

    def first(self, tries, i):
        fails = []
        for f in tries:
            try:
                return f()
            except _No as e:
                fails.append(e)
        raise max(fails, key=lambda e: e.pos) if fails else _No(i, "nothing is allowed here")

    def value(self, s, lpath, i, slot=None):
        s = _clean(s, ".".join(lpath) or "$")
        if "anyOf" in s:
            return self.first([lambda x=x: self.value(x, lpath, i, slot) for x in s["anyOf"]], i)
        if "const" in s or "enum" in s:
            vals = [_json(v) for v in ([s["const"]] if "const" in s else s["enum"]) if _fits(v, s.get("type"))
                    and ("enum" not in s or "const" not in s or v in s["enum"])]
            hit = max((len(v) for v in vals if self.t.startswith(v, i)), default=None)
            if hit is None:
                raise _No(i, f"not one of {vals[:8]}{'…' if len(vals) > 8 else ''}")
            return i + hit
        t = s.get("type")
        if isinstance(t, list):
            return self.value({"anyOf": [{**s, "type": x} for x in t]}, lpath, i, slot)
        if t == "object":
            return self.object(s, lpath, i, slot)
        if t == "array":
            return self.array(s, lpath, i, slot)
        if t == "string":
            m = STRING.match(self.t, i)
            if not m:
                raise _No(i, "not a JSON string")
            if "pattern" in s and not re.fullmatch(_pattern_regex(s["pattern"]), m.group(0)[1:-1]):
                raise _No(i, f"{m.group(0)} does not match {s['pattern']}")
            return m.end()
        if t in ("integer", "number"):
            m = (NUMBER if t == "number" else INTEGER[s.get("minimum")]).match(self.t, i)
            if not m:
                raise _No(i, f"not a JSON {t}{' ≥ ' + str(s['minimum']) if 'minimum' in s else ''}")
            return m.end()
        if t == "boolean":
            return self.first([lambda: self.lit("true", i), lambda: self.lit("false", i)], i)
        if t == "null":
            return self.lit("null", i)
        raise _No(i, "no type")

    def object(self, s, lpath, i, slot):
        if _is_quote(s):
            return self.quote(s, lpath, i, slot)
        req = s["required"]
        if not req:
            return self.lit("{}", i)

        def read(v, slots):
            j = self.lit("{", i)
            for n, k in enumerate(req):
                j = self.lit(("," if n else "") + _json(k) + ":", j)
                j = self.value(v["properties"][k], lpath + (k,), j, slots.get(k))
            return self.lit("}", j)
        return self.first([lambda v=v, slots=slots: read(v, slots) for v, slots in _variants(s, lpath, self.rest)], i)

    def array(self, s, lpath, i, slot):
        mn, mx = s.get("minItems", 0), s.get("maxItems")
        j, n = self.lit("[", i), 0
        if not self.t.startswith("]", j):
            while True:
                j = self.value(s["items"], lpath, j, slot)
                n += 1
                if mx is not None and n > mx:
                    raise _No(j, f"more than {mx} items")
                if not self.t.startswith(",", j):
                    break
                j += 1
        j = self.lit("]", j)
        if n < mn:
            raise _No(i, f"{n} items, fewer than {mn}")
        return j

    def quote(self, s, lpath, i, slot):
        slot = slot or _slot(lpath, self.rtype)
        props, req = s["properties"], s["required"]
        texto, de = _clean(props["texto"], "texto"), _clean(props["de"], "de")
        if texto != {"type": "string"} or de.get("type") != "string" or set(de) - {"type", "enum"}:
            raise ValueError("a quote is {texto: string, de: string enum}")
        j, got = i, {}
        for n, k in enumerate(req):
            j = self.lit(("{" if not n else ",") + _json(k) + ":", j)
            m = STRING.match(self.t, j)
            if not m:
                raise _No(j, f"«{k}» is not a JSON string")
            got[k] = (j, m.group(0), json.loads(m.group(0)))
            j = m.end()
        j = self.lit("}", j)
        (dp, dlex, dv), (tp, tlex, tv) = got["de"], got["texto"]
        roles = self.context["roles"]
        key = (slot, None if de.get("enum") is None else tuple(de["enum"]))
        if key not in self.citable:
            self.citable[key] = set(citable(self.context, slot, de.get("enum")))
        if dlex != _json(dv) or dv not in self.citable[key]:
            raise _No(dp, f"«de» {dv} ({roles.get(dv, 'not in the text')}): a {slot} quote cites only {sorted(SLOT_ROLES[slot])}")
        if tlex != _json(tv):
            raise _No(tp, f"«texto» {tlex[:40]}: not JSON-escaped as the grammar writes it")
        if not aligned(self.context["allowed"][dv], tv):
            raise _No(tp, f"«texto» «{tv[:60]}» is not a token-aligned piece of {dv}")
        return j


def why_not(answer_text, schema, context):
    """None when answer_text is in grammar(schema, context)'s language; otherwise where and why it is not."""
    _check_schema(schema)
    r = _Reader(answer_text, schema, context)
    try:
        end = r.value(schema, (), 0)
        if end != len(answer_text):
            raise _No(end, f"text after the answer: {answer_text[end:end + 20]!r}")
    except _No as e:
        return f"at {e.pos}: {e.why}"
    return None


def accepts(answer_text, schema, context):
    return why_not(answer_text, schema, context) is None
