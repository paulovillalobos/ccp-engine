"""The quote grammar (readers/quote_grammar.py): leitor:a can only quote words that are in a passage it may cite. Local, no
Modal: every gold answer of data-v12 is in the language; v12's dev answers whose quotes the checker refused are not; the
grammar's own text, read back by a small EBNF interpreter below, is the same language as accepts(); the slots cite the
roles the checker allows; literals round-trip; the reader builds the grammars (with a stand-in for modal). With xgrammar
installed, it also compiles the grammars and accepts the gold. Sealed rows are run, never shown: a failure there names
the row only."""
import ast
import copy
import importlib.util
import json
import random
import re
import sys
import types
from functools import lru_cache
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT)); sys.path.insert(0, str(ROOT / "tools")); sys.path.insert(0, str(ROOT / "readers"))
import make_rule_readings_v12 as data  # noqa: E402
import quote_grammar as qg  # noqa: E402
import read_rules_v3 as v3  # noqa: E402

sys.setrecursionlimit(20000)  # the interpreter follows a quote's token chain one rule per token
SETS = {"dev": 104, "sealed": 96, "dev_antigo": 393, "train": 1318}
CONTEXTS = ROOT / "governance/readings/avaliacao-v13/contexts"
V12_DEV = ROOT / "governance/readings/avaliacao-v12/dev/leitor-a14.jsonl"


@lru_cache(maxsize=None)
def articles():
    return {f"{data.TASK}:{ex['id']}": ex for pattern, _ in data.SOURCES for ex in data.load(pattern)}


@lru_cache(maxsize=None)
def rows(name):
    return [json.loads(line) for line in (ROOT / f"training/data-v12/regra_lida/{name}.jsonl").read_text(encoding="utf-8").splitlines() if line.strip()]


def context_of(row):
    return v3.context_record(data.ctx_of(articles()[row["id"]]))


def compact(answer):
    return json.dumps(answer, ensure_ascii=False, separators=(",", ":"))


# ---- the grammar's text, read back --------------------------------------------------------------------------------------
class Ebnf:
    """The EBNF quote_grammar writes, parsed and run: one rule per line «name ::= body»; literals "…" with \\-escapes
    (\\uXXXX, \\xHH, C's), classes [...] and [^...], names, ( ), |, ?, *, +. accept() follows every alternative (the
    end positions each rule can reach, memoised), so it is the grammar's language, whatever accepts() does."""

    ESC = {"n": "\n", "t": "\t", "r": "\r", "0": "\0", "b": "\b", "f": "\f", "v": "\v", "a": "\a", "e": "\x1b",
           "\\": "\\", '"': '"', "'": "'", "?": "?", "[": "[", "]": "]", "-": "-", "^": "^"}

    def __init__(self, text):
        self.rules, self.firsts = {}, {}
        for line in text.splitlines():
            if line.strip():
                name, body = line.split(" ::= ", 1)
                assert re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", name) and name not in self.rules, name
                self.rules[name] = self.parse(body)
        for name in self.rules:
            self.first(("ref", name))

    def escape(self, s, j):
        c = s[j + 1]
        if c == "u":
            return chr(int(s[j + 2:j + 6], 16)), j + 6
        if c == "x":
            return chr(int(s[j + 2:j + 4], 16)), j + 4
        return self.ESC[c], j + 2

    def lex(self, s):
        i, out = 0, []
        while i < len(s):
            c = s[i]
            if c == " ":
                i += 1
            elif c == '"':
                j, buf = i + 1, []
                while s[j] != '"':
                    if s[j] == "\\":
                        ch, j = self.escape(s, j)
                    else:
                        ch, j = s[j], j + 1
                    buf.append(ch)
                out.append(("lit", "".join(buf)))
                i = j + 1
            elif c == "[":
                j = i + 1
                neg = s[j] == "^"
                j += neg
                ranges = []
                while s[j] != "]":
                    lo, j = self.escape(s, j) if s[j] == "\\" else (s[j], j + 1)
                    hi = lo
                    if s[j] == "-" and s[j + 1] != "]":
                        hi, j = self.escape(s, j + 1) if s[j + 1] == "\\" else (s[j + 1], j + 2)
                    ranges.append((lo, hi))
                out.append(("cls", (neg, tuple(ranges))))
                i = j + 1
            elif c in "()|?*+":
                out.append((c, None))
                i += 1
            else:
                m = re.match(r"[A-Za-z_][A-Za-z0-9_]*", s[i:])
                assert m, s[i:i + 20]
                out.append(("ref", m.group(0)))
                i += m.end()
        return out

    def parse(self, body):
        toks, pos = self.lex(body), 0

        def alt():
            nonlocal pos
            opts = [seq()]
            while pos < len(toks) and toks[pos][0] == "|":
                pos += 1
                opts.append(seq())
            return opts[0] if len(opts) == 1 else ("alt", opts)

        def seq():
            nonlocal pos
            items = []
            while pos < len(toks) and toks[pos][0] not in ("|", ")"):
                items.append(post())
            assert items, body
            return items[0] if len(items) == 1 else ("seq", items)

        def post():
            nonlocal pos
            a = atom()
            while pos < len(toks) and toks[pos][0] in ("?", "*", "+"):
                a = ({"?": "opt", "*": "star", "+": "plus"}[toks[pos][0]], a)
                pos += 1
            return a

        def atom():
            nonlocal pos
            k, v = toks[pos]
            pos += 1
            if k == "(":
                a = alt()
                assert toks[pos][0] == ")", body
                pos += 1
                return a
            assert k in ("lit", "cls", "ref"), body
            return (k, v)
        tree = alt()
        assert pos == len(toks), body
        return tree

    def first(self, node):
        """The characters a node can start with, or None (unknown, or it can be empty)."""
        k = node[0]
        if k == "lit":
            return {node[1][0]} if node[1] else None
        if k == "ref":
            if node[1] not in self.firsts:
                self.firsts[node[1]] = None
                self.firsts[node[1]] = self.first(self.rules[node[1]])
            return self.firsts[node[1]]
        if k == "seq":
            return self.first(node[1][0])
        if k == "alt":
            fs = [self.first(n) for n in node[1]]
            return None if any(f is None for f in fs) else set().union(*fs)
        if k == "plus":
            return self.first(node[1])
        return None

    def ends(self, node, t, i, memo):
        k = node[0]
        if k == "lit":
            return {i + len(node[1])} if t.startswith(node[1], i) else set()
        if k == "cls":
            neg, ranges = node[1]
            return {i + 1} if i < len(t) and any(a <= t[i] <= b for a, b in ranges) != neg else set()
        if k == "ref":
            key = (node[1], i)
            if key not in memo:
                memo[key] = set()
                memo[key] = self.ends(self.rules[node[1]], t, i, memo)
            return memo[key]
        if k == "seq":
            cur = {i}
            for n in node[1]:
                cur = set().union(*[self.ends(n, t, j, memo) for j in cur])
                if not cur:
                    break
            return cur
        if k == "alt":
            out = set()
            for n in node[1]:
                f = self.first(n)
                if f is None or (i < len(t) and t[i] in f):
                    out |= self.ends(n, t, i, memo)
            return out
        if k == "opt":
            return {i} | self.ends(node[1], t, i, memo)
        out = frontier = self.ends(node[1], t, i, memo) if k == "plus" else {i}
        out = set(out)
        while frontier:
            frontier = set().union(*[self.ends(node[1], t, j, memo) for j in frontier]) - out
            out |= frontier
        return out

    def accept(self, text):
        return len(text) in self.ends(("ref", "root"), text, 0, {})

    def literals(self, name):
        """The literals of a rule's body, in order."""
        out = []

        def walk(n):
            if n[0] == "lit":
                out.append(n[1])
            elif n[0] in ("seq", "alt"):
                for x in n[1]:
                    walk(x)
            elif n[0] in ("opt", "star", "plus"):
                walk(n[1])
        walk(self.rules[name])
        return out


def quotes_of(answer):
    """Every quote object of a parsed answer, in order."""
    out = []
    for r in answer.get("regras") or []:
        for c in r.get("condicoes") or []:
            out += c.get("fontes") or []
        for fs in (r.get("fontes") or {}).values():
            out += fs or []
    if answer.get("nao_tipavel"):
        out += answer["nao_tipavel"].get("fontes") or []
    return out


# ---- the slots cite what the checker allows -------------------------------------------------------------------------------
ROLES = ["alvo", "proemio", "remissao", "remissao_epigrafe", "epigrafe", "titulo", "vizinho"]


def synthetic(is_rest):
    roles = {f"x:{r}": r for r in ROLES}
    allowed = {p: "Palavras da passagem." for p in roles}
    if is_rest:
        allowed["x:alvo"] = "Nos restantes casos, palavras da passagem."
    return {"alvo": "x:alvo", "date": "2026-10-01", "article": "x:epigrafe", "roles": roles, "allowed": allowed}


def q(pid):
    return [{"texto": "passagem", "de": pid}]


def answers_citing(pid):
    """(slot, rtype, where the checker reports it, answer) with one quote from pid, every other quote from the target."""
    out = []
    for op in ("eq", "ne", "in", "not_in", "lt"):
        v = ["concurso_publico"] if op in ("in", "not_in") else "concurso_publico"
        rule = {"tipo": "prazo_minimo", "condicoes": [{"field": "tipo_procedimento", "op": op, "value": v, "fontes": q(pid)}],
                "params": {"minimum_days": 10, "deadline_field": "prazo_propostas_dias", "counted_from": "data_envio_anuncio", "usual_days": 5},
                "fontes": {k: q("x:alvo") for k in ("minimum_days", "deadline_field", "counted_from", "usual_days")}}
        out.append((("condicao", op), "prazo_minimo", f"regra 1, tipo_procedimento {op} {v}: ", {"regras": [rule], "nao_tipavel": None}))
    for k in ("minimum_days", "deadline_field", "counted_from", "usual_days"):
        rule = {"tipo": "prazo_minimo", "condicoes": [],
                "params": {"minimum_days": 10, "deadline_field": "prazo_propostas_dias", "counted_from": "data_envio_anuncio", "usual_days": 5},
                "fontes": {x: q(pid if x == k else "x:alvo") for x in ("minimum_days", "deadline_field", "counted_from", "usual_days")}}
        out.append((("param", k), "prazo_minimo", f"regra 1, {k}: ", {"regras": [rule], "nao_tipavel": None}))
    for k in ("field", "comparator", "value"):
        rule = {"tipo": "limiar", "condicoes": [{"field": "tipo_procedimento", "op": "eq", "value": "ajuste_direto", "fontes": q("x:alvo")}],
                "params": {"threshold": {"field": next(iter(v3.VOC["threshold_fields"])), "comparator": "lt", "value": 1000, "currency": "EUR"}},
                "fontes": {x: q(pid if x == k else "x:alvo") for x in ("field", "comparator", "value")}}
        out.append((("param_field" if k == "field" else "param", k), "limiar", f"regra 1, {k}: ", {"regras": [rule], "nao_tipavel": None}))
    nt = {"motivo": next(iter(v3.VOC["nao_tipavel_motivos"])), "fontes": q(pid), "falta": "o texto não o diz"}
    out.append((("nao_tipavel", None), "prazo_minimo", "não tipável: ", {"regras": [], "nao_tipavel": nt}))
    return out


def test_role_sets_are_the_checkers():
    assert qg.CONDITION_ROLES == v3.CONDITION_ROLES and qg.PARAM_ROLES == v3.PARAM_ROLES


@pytest.mark.parametrize("is_rest", [False, True])
def test_each_slot_cites_what_the_checker_allows(is_rest):
    """For every slot and role: the checker reports no L1 refusal for the quote exactly when the slot's roles hold the
    role, and the grammar (accepts() and its own text) admits the answer exactly then."""
    ctx = synthetic(is_rest)
    assert qg.rest(ctx) is is_rest
    seen = 0
    for role in ROLES:
        pid = f"x:{role}"
        for (slot, key), rtype, where, ans in answers_citing(pid):
            errs = v3.check(ans, ctx, rtype)
            l1 = any(e.startswith(where) and f"fonte em {pid}, que é {role} (L1)" in e for e in errs)
            name = ("condicao_resto" if is_rest and key in qg.REST_OPS else "condicao") if slot == "condicao" else slot
            allowed = role in qg.SLOT_ROLES[name]
            assert (not l1) == allowed, (slot, key, role, errs)
            schema = v3.schema(ctx, rtype)
            assert qg.accepts(compact(ans), schema, ctx) is allowed, (slot, key, role, qg.why_not(compact(ans), schema, ctx))
            assert Ebnf(qg.grammar(schema, ctx)).accept(compact(ans)) is allowed, (slot, key, role)
            seen += 1
    assert seen == len(ROLES) * 13


def test_nullable_parameter_quotes():
    ctx = synthetic(False)
    for k in ("counted_from", "usual_days"):
        _, rtype, _, ans = next(x for x in answers_citing("x:alvo") if x[0] == ("param", k))
        ans["regras"][0]["fontes"][k] = None
        schema = v3.schema(ctx, rtype)
        assert qg.accepts(compact(ans), schema, ctx) and Ebnf(qg.grammar(schema, ctx)).accept(compact(ans))
        ans["regras"][0]["fontes"]["minimum_days"] = None  # not nullable
        assert not qg.accepts(compact(ans), schema, ctx) and not Ebnf(qg.grammar(schema, ctx)).accept(compact(ans))


# ---- the gold --------------------------------------------------------------------------------------------------------------
@pytest.mark.parametrize("name", list(SETS))
def test_every_gold_answer_is_in_the_language(name):
    rs = rows(name)
    assert len(rs) == SETS[name]
    bad = []
    for r in rs:
        why = qg.why_not(r["answer"], r["schema"], context_of(r))
        if why:
            bad.append(r["id"] if name == "sealed" else f"{r['id']}: {why}")
    assert not bad, f"{len(bad)} of {len(rs)} gold answers outside the grammar: {bad[:10]}"


@pytest.mark.parametrize("name", list(SETS))
def test_the_grammar_text_accepts_the_gold(name):
    """The grammar's own text, run by the interpreter, takes every gold answer of the set."""
    bad = [r["id"] for r in rows(name) if not Ebnf(qg.grammar(r["schema"], context_of(r))).accept(r["answer"])]
    assert not bad, bad[:10]


def test_the_grammar_is_the_same_with_the_schema_in_answer_order():
    """Keys follow each object's required list, so the stored (alphabetised) schema and the reader's give one grammar."""
    order = reader_functions("in_answer_order")["in_answer_order"]
    for r in rows("dev")[:20]:
        ctx = context_of(r)
        assert qg.grammar(r["schema"], ctx) == qg.grammar(order(r["schema"]), ctx)


def test_context_files_are_the_rows_contexts():
    for name in ("dev", "sealed", "dev_antigo"):
        lines = [json.loads(line) for line in (CONTEXTS / f"{name}.jsonl").read_text(encoding="utf-8").splitlines()]
        assert [x["id"] for x in lines] == [r["id"] for r in rows(name)], name
        assert all(x["context"] == json.loads(json.dumps(context_of(r))) for x, r in zip(lines, rows(name))), name


# ---- v12's refused quotes ----------------------------------------------------------------------------------------------------
def test_v12_quotes_the_checker_refused_are_outside_the_language():
    """leitor-a14 on dev: each answer whose first refusal is a quote «não está em» its passage, or a source in a vizinho
    the condition may not cite, is rejected, written compact (its own text has the schema path's «, » and «: », which
    alone would keep it out) and for a quote."""
    by_id = {r["id"]: r for r in rows("dev")}
    kinds, seen = {"não está em": 0, "vizinho": 0}, 0
    for line in V12_DEV.read_text(encoding="utf-8").splitlines():
        a = json.loads(line)
        reading = v3.parse(a["answer"])
        if reading is None:
            continue
        r, ex = by_id[a["id"]], articles()[a["id"]]
        errs = v3.check(reading, data.ctx_of(ex), ex["tipo"])
        kind = "não está em" if errs and "não está em" in errs[0] else "vizinho" if errs and "que é vizinho (L1)" in errs[0] else None
        if kind is None:
            continue
        kinds[kind] += 1
        text, ctx = compact(json.loads(a["answer"])), context_of(r)
        why = qg.why_not(text, r["schema"], ctx)
        assert why and ("«texto»" in why or "«de»" in why), (a["id"], why)
        assert not Ebnf(qg.grammar(r["schema"], ctx)).accept(text), a["id"]
        seen += 1
    assert kinds == {"não está em": 18, "vizinho": 2} and seen == 20


# ---- accepts() and the grammar's text are one language ---------------------------------------------------------------------
def mutations(answer, ctx, rng):
    """Copies of a gold answer with one thing changed: a quote cut, grown, recased or respaced, another passage, blanks."""
    a = json.loads(answer)
    out = [answer.replace(":", ": ", 1), answer.replace(",", ", ", 1), answer + "\n", answer[:-1]]
    n = len(quotes_of(a))
    pids = sorted(ctx["roles"])
    for k in range(n):
        t = quotes_of(a)[k]["texto"]
        for new in {t[:-1], t[1:], t + "s", t + ".", " " + t, t.upper(), t.lower(), t.capitalize(), t.replace(" ", "  ", 1),
                    t.replace(" ", " ", 1), t[: len(t) // 2]}:
            b = copy.deepcopy(a)
            quotes_of(b)[k]["texto"] = new
            out.append(compact(b))
        for pid in rng.sample(pids, min(3, len(pids))):
            b = copy.deepcopy(a)
            quotes_of(b)[k]["de"] = pid
            out.append(compact(b))
        allowed = ctx["allowed"][quotes_of(a)[k]["de"]]
        sp = qg.tokens(allowed)
        for _ in range(3):  # another piece of the same passage, aligned or not
            i, j = sorted(rng.sample(range(len(sp)), 2)) if len(sp) > 1 else (0, 0)
            for s, e in ((sp[i][0], sp[j][1]), (sp[i][0] + 1, sp[j][1]), (sp[i][0], max(sp[j][1] - 1, sp[i][0] + 1))):
                b = copy.deepcopy(a)
                quotes_of(b)[k]["texto"] = allowed[s:e]
                out.append(compact(b))
    return out


def test_accepts_and_the_grammar_text_agree_on_mutated_gold():
    rng = random.Random(0)
    counts = {True: 0, False: 0}
    for r in rows("dev") + rows("dev_antigo")[::8]:
        ctx = context_of(r)
        e = Ebnf(qg.grammar(r["schema"], ctx))
        for m in mutations(r["answer"], ctx, rng):
            got = qg.accepts(m, r["schema"], ctx)
            assert got == e.accept(m), (r["id"], m, qg.why_not(m, r["schema"], ctx))
            counts[got] += 1
    assert counts[True] > 3000 and counts[False] > 10000, counts


def test_a_piece_the_grammar_admits_passes_the_checker_word_test():
    """Every token-aligned piece of a passage is a quote the checker's contains() finds in it."""
    rng = random.Random(1)
    n = 0
    for name in ("dev", "dev_antigo"):
        for r in rows(name):
            for pid, text in context_of(r)["allowed"].items():
                sp = qg.tokens(text)
                for _ in range(min(20, len(sp))):
                    i, j = sorted(rng.choice(range(len(sp))) for _ in range(2))
                    piece = text[sp[i][0]:sp[j][1]]
                    assert qg.aligned(text, piece) and v3.contains(text, piece), (r["id"], pid, piece)
                    n += 1
    assert n > 10000


# ---- the EBNF text ---------------------------------------------------------------------------------------------------------
TRICKY = 'Diz «assim»: "aspas", uma barra \\ e duas \\\\,\nnova linha;\tum tab, nbsp aqui, sino \x07, del \x7f e fim.'


def test_literals_round_trip():
    """A passage with « », quotes, backslashes, a newline, a tab, a no-break space and control characters: the grammar's
    literals for it, read back, are its JSON-escaped text; quotes of it are admitted exactly as they are written."""
    ctx = {"alvo": "x:1", "date": "2026-10-01", "article": "x:1", "roles": {"x:1": "alvo"}, "allowed": {"x:1": TRICKY}}
    schema = v3.schema(ctx, "prazo_minimo")
    g = qg.grammar(schema, ctx)
    assert all(re.match(r"[A-Za-z_][A-Za-z0-9_]* ::= ", line) and all(ord(c) >= 0x20 for c in line) for line in g.splitlines())
    e = Ebnf(g)
    chain = sorted((n for n in e.rules if re.fullmatch(r"t0_\d+", n)), key=lambda n: int(n.split("_")[1]))
    written = "".join("".join(e.literals(n)) for n in chain)
    assert written == json.dumps(TRICKY, ensure_ascii=False)[1:-1] and json.loads(f'"{written}"') == TRICKY
    for piece, ok in [(TRICKY, True), ("«assim»", True), ('"aspas"', True), ("\\ e duas \\\\", True), (",\nnova", True),
                      ("tab, nbsp aqui", True), ("sino \x07, del \x7f", True), ("\t", False), (", nova", False),
                      ("nbsp aqui", False), ("ssim", False), ("Diz «assim", True), ("diz", False), ("", False), (" Diz", False)]:
        ans = compact({"regras": [], "nao_tipavel": {"motivo": "sem_vocabulario", "fontes": [{"texto": piece, "de": "x:1"}], "falta": "x"}})
        assert qg.accepts(ans, schema, ctx) is ok and e.accept(ans) is ok, (piece, qg.why_not(ans, schema, ctx))


def test_unknown_schema_keywords_are_refused():
    ctx = synthetic(False)
    s = v3.schema(ctx, "prazo_minimo")
    s["properties"]["regras"]["uniqueItems"] = True
    with pytest.raises(ValueError):
        qg.grammar(s, ctx)
    with pytest.raises(ValueError):
        qg.accepts("{}", s, ctx)


# ---- the reader ------------------------------------------------------------------------------------------------------------
def reader_functions(*names):
    """Functions taken from the reader's source (it imports modal), as tests/test_reader_order.py does."""
    tree = ast.parse((ROOT / "readers/leitor_a_modal.py").read_text(encoding="utf-8"))
    ns = {"sys": sys, "Path": type(ROOT), "__file__": str(ROOT / "readers/leitor_a_modal.py")}
    fns = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name in names + ("in_answer_order",)]
    exec(compile(ast.Module(fns, type_ignores=[]), "readers/leitor_a_modal.py", "exec"), ns)
    return ns


def fake_modal():
    """Enough of modal for the reader's module to load; app.function's object records what .remote gets."""
    class Chain:
        def __getattr__(self, name):
            return lambda *a, **k: self

    class Remote:
        calls = []

        def remote(self, items, lora=""):
            self.calls.append(items)
            return [{"key": i["key"], "prompt_tokens": 1, "completion_tokens": 1, "finish_reason": "stop", "text": "{}"} for i in items]

    class App:
        def __init__(self, *a, **k):
            pass

        def function(self, **k):
            return lambda fn: Remote()

        def local_entrypoint(self):
            return lambda fn: fn
    m = types.ModuleType("modal")
    m.App, m.Image, m.Volume = App, Chain(), Chain()
    return m


@pytest.fixture
def reader(monkeypatch):
    monkeypatch.setitem(sys.modules, "modal", fake_modal())
    spec = importlib.util.spec_from_file_location("leitor_a_modal_under_test", ROOT / "readers/leitor_a_modal.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    mod.answer.calls.clear()
    return mod


def test_reader_jsonl_mode_with_and_without_quotes(reader, tmp_path):
    rs = rows("dev")[:5]
    src = tmp_path / "rows.jsonl"
    src.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rs), encoding="utf-8")
    reader.main(jsonl=str(src), out=str(tmp_path / "plain.jsonl"), order="required")
    assert all(set(i) == {"key", "prompt", "schema"} for i in reader.answer.calls[-1])  # without the option, as before
    assert all("quotes" not in json.loads(line) for line in (tmp_path / "plain.jsonl").read_text(encoding="utf-8").splitlines())
    with pytest.raises(SystemExit):
        reader.main(jsonl=str(src), out=str(tmp_path / "q.jsonl"), quotes="text")
    reader.main(jsonl=str(src), out=str(tmp_path / "q.jsonl"), quotes="text", contexts=str(CONTEXTS / "dev.jsonl"))
    items = reader.answer.calls[-1]
    assert [i["key"] for i in items] == [r["id"] for r in rs]
    assert all(i["grammar"] == qg.grammar(r["schema"], context_of(r)) for i, r in zip(items, rs))
    assert all(json.loads(line)["quotes"] == "text" for line in (tmp_path / "q.jsonl").read_text(encoding="utf-8").splitlines())
    with pytest.raises(SystemExit):  # a row without its context
        reader.main(jsonl=str(src), out=str(tmp_path / "q2.jsonl"), quotes="text", contexts=str(CONTEXTS / "dev_antigo.jsonl"))


def test_reader_directory_mode_reads_the_context_of_prompt_json(reader, tmp_path):
    r = rows("dev")[0]
    case = tmp_path / "caso"
    case.mkdir()
    (case / "prompt.json").write_text(json.dumps({"prompt": r["prompt"], "schema": r["schema"], "context": context_of(r)}, ensure_ascii=False), encoding="utf-8")
    reader.main(dir=str(tmp_path), out_dir=str(tmp_path / "out"), quotes="text")
    assert reader.answer.calls[-1][0]["grammar"] == qg.grammar(r["schema"], context_of(r))
    assert json.loads((tmp_path / "out/caso/leitor-a.json").read_text(encoding="utf-8"))["quotes"] == "text"
    (case / "prompt.json").write_text(json.dumps({"prompt": r["prompt"], "schema": r["schema"]}), encoding="utf-8")
    with pytest.raises(SystemExit):
        reader.main(dir=str(tmp_path), out_dir=str(tmp_path / "out2"), quotes="text")


# ---- xgrammar, where it is installed -------------------------------------------------------------------------------------
def test_xgrammar_compiles_the_grammars_and_accepts_the_gold():
    xgr = pytest.importorskip("xgrammar")
    from xgrammar.testing import _is_grammar_accept_string
    for r in rows("dev")[:20]:
        g = xgr.Grammar.from_ebnf(qg.grammar(r["schema"], context_of(r)))
        assert _is_grammar_accept_string(g, r["answer"]), r["id"]
        assert not _is_grammar_accept_string(g, r["answer"].replace('"texto":"', '"texto":"x', 1)), r["id"]
