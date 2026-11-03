"""The reading protocol v3 (DECISIONS D66): what a reader of the rules factory sees, the prompt and answer schema, and
the checker that confirms every quoted word against the shown text. schemas/vocabulario-v3.json is the one list of values
and of the law's words for them (product_rule:vocabulario-v3); the prompt prints it, the checker reads it.

    context(law, alvo, date) -> ctx        the target in its place in the law: the law's title and Parte/Título/Capítulo/
                                           Secção, the article with each passage once, the target's proémio and alíneas,
                                           the passages it refers to (a deadline's or limit's base followed in a chain);
                                           roles say which passages a condition may come from (L1)
    render(ctx, type) -> str               the prompt: task, what a rule means to the engine, the rules L1-L14, the
                                           vocabulary, the answer format with an example, the text, a neutral question
    schema(ctx, type) -> dict              the answer schema: rules with quotes, or «não tipável» with one of four reasons
    check(reading, ctx, type) -> [str]     what keeps a reading from being recorded (product_rule:fontes-verificadas-e-nao-tipavel)
    canonical(reading)                     the content two readings replicate on (quotes and passages aside)
    cited(reading, ctx)                    the passages each rule cites: the target and those its quotes come from
    selftest() -> bool                     the prompt's own example passes; nine broken copies of it fail

Nothing here calls a model.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
VOC = json.loads((ROOT / "schemas/vocabulario-v3.json").read_text(encoding="utf-8"))
VERSION = "ccp-read-rules-v3-0.2"  # 0.2: a referred number is shown whole (with its alíneas); L12 says when a missing text blocks the reading

# ---- words ----------------------------------------------------------------------------------------------------------
OLD = VOC["old_spelling"]


def norm(s):
    s = s.replace(" ", " ").replace("’", "'").replace("«", '"').replace("»", '"').replace("“", '"').replace("”", '"')
    s = re.sub(r"\s+", " ", s).strip().lower()
    for a, b in OLD.items():
        s = re.sub(rf"(?<!\w){a}(?!\w)", b, s)
    return s


def contains(text, quote):
    return bool(quote.strip()) and norm(quote) in norm(text)


def _named(text, table, consume_first=()):
    """Values whose law words occur in text, longest words first, each span used once («concessão de serviços» is not
    also «serviços»; «ajuste direto simplificado» is not also «ajuste direto»)."""
    t, found = " " + norm(text) + " ", set()
    for words, values in consume_first:
        for w in words:
            pat = rf"(?<!\w){re.escape(norm(w))}(?!\w)"
            if re.search(pat, t):
                found |= set(values)
                t = re.sub(pat, " § ", t)
    pairs = sorted(((norm(w), v) for v, ws in table.items() for w in ws), key=lambda x: -len(x[0]))
    for w, v in pairs:
        pat = rf"(?<!\w){re.escape(w)}(?!\w)"
        if re.search(pat, t):
            found.add(v)
            t = re.sub(pat, " § ", t)
    return found


def values_named(field, text):
    spec = VOC["condition_fields"][field]
    first = [(spec["both_concessions"], ["concessao_obras", "concessao_servicos"])] if field == "tipo_contrato" else \
        [(spec["both_regions"], ["PT-AC", "PT-MA"])] if field == "territorio" else []
    return _named(text, spec["values"], first)


def polarity(field, text):
    """True / False for each place the text states a two-sided fact: false when «não» or «sem» comes just before."""
    t, out = norm(text), set()
    for w in sorted(VOC["condition_fields"][field]["phrases"], key=len, reverse=True):
        for m in re.finditer(re.escape(norm(w)), t):
            before = t[max(0, m.start() - 45):m.start()]
            if any(norm(b) in before[-20:] for b in VOC.get("both_polarities", [])):
                out |= {True, False}
                continue
            out.add(not any(re.search(rf"(?<!\w){re.escape(n)}(?!\w)", before) for n in VOC.get("negations_words", ["não", "sem"])))
    return out


def counted_named(text):
    """The starting points a text states. «Contados do seu envio», «a contar do envio deste» count from the document the
    sentence names last before those words (the convite or the anúncio)."""
    found = _named(text, VOC["counted_from"])
    t = norm(text)
    for w in VOC.get("anaphoric_sending", []):
        for m in re.finditer(re.escape(norm(w)), t):
            if "convite" in w:
                found.add("data_envio_convite")
                continue
            before = t[:m.start()]
            c, a = before.rfind("convite"), max(before.rfind("anúncio"), before.rfind("anuncio"))
            if c > a:
                found.add("data_envio_convite")
            elif a > c:
                found.add("data_envio_anuncio")
    for w in VOC.get("anaphoric_publication", []):
        if re.search(re.escape(norm(w)), t) and ("anúncio" in t or "anuncio" in t):
            found.add("data_publicacao_anuncio")
    return found


def comparators_in(text):
    return _named(text, VOC["comparators"])


UNITS = {"um": 1, "uma": 1, "dois": 2, "duas": 2, "três": 3, "quatro": 4, "cinco": 5, "seis": 6, "sete": 7, "oito": 8,
         "nove": 9, "dez": 10, "onze": 11, "doze": 12, "treze": 13, "catorze": 14, "quatorze": 14, "quinze": 15,
         "dezasseis": 16, "dezassete": 17, "dezoito": 18, "dezanove": 19}
TENS = {"vinte": 20, "trinta": 30, "quarenta": 40, "cinquenta": 50, "sessenta": 60, "setenta": 70, "oitenta": 80, "noventa": 90}


def numbers_in(text):
    t, out = norm(text), set()
    t = re.sub(r"n\.º\s*\d+|artigo \d+\.º(-[a-z])?|\d{1,3}(?:[ .]\d{3})+(?:,\d+)?\s*€", " ", t)  # not article or number ids, not euros
    out |= {int(x) for x in re.findall(r"(?<![\w.])\d+(?![\w.])", t)}
    for m in re.finditer(r"(?<!\w)(vinte|trinta|quarenta|cinquenta|sessenta|setenta|oitenta|noventa)(?: e (um|uma|dois|duas|três|quatro|cinco|seis|sete|oito|nove))?(?!\w)", t):
        out.add(TENS[m.group(1)] + (UNITS[m.group(2)] if m.group(2) else 0))
    out |= {v for w, v in UNITS.items() if re.search(rf"(?<!\w){w}(?!\w)", t)}
    return out


HUNDREDS = {"cem": 100, "cento": 100, "duzentos": 200, "trezentos": 300, "quatrocentos": 400, "quinhentos": 500,
            "seiscentos": 600, "setecentos": 700, "oitocentos": 800, "novecentos": 900}
WORD_NUM = {**UNITS, **TENS, **HUNDREDS}


def words_value(words):
    """«quarenta e um mil e oitocentos» = 41800; «cento e doze mil» = 112000; «dois milhões» = 2000000."""
    total, part = 0, 0
    for w in words.split():
        if w == "e":
            continue
        if w in WORD_NUM:
            part += WORD_NUM[w]
        elif w == "mil":
            total += (part or 1) * 1000
            part = 0
        elif w in ("milhão", "milhões"):
            total += (part or 1) * 1000000
            part = 0
        else:
            return None
    return total + part


def euros_in(text):
    t, out = text.replace(" ", " "), set()
    alts = "|".join(sorted(list(WORD_NUM) + ["mil", "milhão", "milhões", "e"], key=len, reverse=True))
    for m in re.finditer(rf"(?<!\w)((?:(?:{alts})\s+)+)(?:de\s+)?euros\b", norm(t)):
        v = words_value(m.group(1).strip())
        if v:
            out.add(v)
    for m in re.finditer(r"(\d{1,3}(?:[ .]\d{3})+|\d+)(?:,\d+)?\s*(?:€|euros?\b)", t):
        out.add(int(re.sub(r"[ .]", "", m.group(1))))
    for m in re.finditer(r"\(euro\)\s*(\d{1,3}(?:[ .]\d{3})+|\d+)", t):
        out.add(int(re.sub(r"[ .]", "", m.group(1))))
    return out


# ---- the law --------------------------------------------------------------------------------------------------------
class Law:
    def __init__(self, store=None):
        sys.path[:0] = [str(ROOT), str(ROOT / "tools")]
        from engine.store import Store  # noqa: E402
        from read_rules import version_at  # noqa: E402
        self.version_at = version_at
        store = store or Store([ROOT / "law"]).load()
        self.p = {}
        for o in store.objects["passagem"]:
            if o["id"] not in self.p or o["revision"] > self.p[o["id"]]["revision"]:
                self.p[o["id"]] = o
        self.kids = {}
        for o in self.p.values():
            self.kids.setdefault(o.get("parent"), []).append(o["id"])
        for k in self.kids:
            self.kids[k].sort(key=self.key)
        self._arts = {}
        for a, o in self.p.items():
            if o.get("kind") == "artigo" and ":art" in a:
                self._arts.setdefault(a.split(":", 1)[0], []).append(a)
        for v in self._arts.values():
            v.sort(key=self.key)

    @classmethod
    def from_passages(cls, passages):
        """A law built from passage objects in memory (the written articles of the training data: D66)."""
        sys.path[:0] = [str(ROOT), str(ROOT / "tools")]
        from read_rules import version_at  # noqa: E402
        law = cls.__new__(cls)
        law.version_at = version_at
        law.p = {o["id"]: o for o in passages}
        law.kids = {}
        for o in law.p.values():
            law.kids.setdefault(o.get("parent"), []).append(o["id"])
        for k in law.kids:
            law.kids[k].sort(key=cls.key)
        law._arts = {}
        for a, o in law.p.items():
            if o.get("kind") == "artigo" and ":art" in a:
                law._arts.setdefault(a.split(":", 1)[0], []).append(a)
        for v in law._arts.values():
            v.sort(key=cls.key)
        return law

    def arts(self, aid):
        """The articles of aid's law, in order."""
        return self._arts.get(aid.split(":", 1)[0], [])

    @staticmethod
    def key(pid):
        tail = pid.split(":art", 1)[1] if ":art" in pid else pid
        out = []
        for part in tail.split("."):
            m = re.match(r"(\d+)(?:-([a-z]))?$", part)
            out.append((0, int(m.group(1)), m.group(2) or "") if m else (1, 0, part))
        return out

    def text(self, pid, date):
        o = self.p.get(pid)
        v = self.version_at(o, date) if o else None
        return None if not v or v.get("revoked") else v["text"]

    def kind(self, pid):
        return (self.p.get(pid) or {}).get("kind")

    def parent(self, pid):
        return (self.p.get(pid) or {}).get("parent")

    def children(self, pid, date):
        return [c for c in self.kids.get(pid, []) if self.text(c, date)]

    def heading(self, aid, date):
        lines = (self.text(aid, date) or "").split("\n")
        return lines[1] if len(lines) > 1 else ""

    def label(self, aid, date):
        return (self.text(aid, date) or "").split("\n")[0]

    def own(self, pid, date):
        """A number's or alínea's own words: the text before its first alínea (or subalínea). An article without numbers:
        its body."""
        t = self.text(pid, date) or ""
        if self.kind(pid) == "artigo":
            return "\n".join(t.split("\n")[2:])
        if self.children(pid, date):
            return re.split(r"\n(?=(?:[a-z]|[ivx]+)\) )", t, maxsplit=1)[0]
        return t

    def article_of(self, pid):
        while pid and self.kind(pid) != "artigo":
            pid = self.parent(pid)
        return pid


NORMA_TITLES = {"norma:ccp": "Código dos Contratos Públicos", "norma:exemplo": "Lei de exemplo (artigos escritos para treino)"}

# ---- references ------------------------------------------------------------------------------------------------------
SEG = re.compile(r"(?:(?:sub)?al[íi]neas? ((?:[a-z]|[ivx]+)\)(?:\s*(?:,|e|ou)\s*(?:[a-z]|[ivx]+)\))*)\s+(?:do|da|dos|das)\s+)?"
                 r"n\.(?:º|ºs|os)\s*(\d+(?:\s*(?:,|e|ou)\s*\d+)*)")
ARTM = re.compile(r"(?<!\w)artigos?\s+((?:\d+\.º(?:-[A-Z])?)(?:\s*(?:,|e|ou)\s*\d+\.º(?:-[A-Z])?)*)|(?<!\w)mesmo artigo|(?<!\w)artigos? anterior(?:es)?")
NUMREL = re.compile(r"(?<!\w)n[úu]meros? anterior(?:es)?|(?<!\w)(?:aquele|esse|o mesmo) prazo")
ALREL = re.compile(r"(?<!\w)al[íi]nea anterior")


def art_pid(token, ns="ccp"):
    m = re.match(r"(\d+)\.º(?:-([A-Z]))?", token)
    return f"{ns}:art{m.group(1)}" + (f"-{m.group(2).lower()}" if m.group(2) else "")


def references(law, pid, text, date):
    """(id, 'texto' | 'epigrafe') the text refers to: «n.º 3 do artigo 167.º», «alíneas b) ou c) do n.º 3 do artigo 474.º»,
    «n.º 5 do mesmo artigo», «n.º 2 do artigo anterior», «o número anterior», «os números anteriores», «a alínea
    anterior»; a whole article («artigo 131.º», «artigos anteriores») gives its heading."""
    aid = law.article_of(pid)
    ns = pid.split(":", 1)[0]
    out, used, last = [], set(), None
    arts = list(ARTM.finditer(text))

    def article_for(m_end):
        nonlocal last
        for a in arts:
            if a.start() >= m_end and ";" not in text[m_end:a.start()] and len(text[m_end:a.start()]) < 140 \
                    and not re.search(r"\.\s+[A-ZÁÉÍÓÚ]", text[m_end:a.start()]):
                used.add(a.start())
                g = a.group(0)
                if g.startswith("mesmo"):
                    return last or aid
                if "anterior" in g:
                    seq = law.arts(aid)
                    i = seq.index(aid) if aid in seq else 0
                    return seq[i - 1] if i else None
                last = art_pid(re.findall(r"\d+\.º(?:-[A-Z])?", a.group(1))[0], ns)
                return last
        return aid

    def base(start):  # «o prazo previsto no n.º 1», «os limiares referidos nas alíneas b) ou c)»: the referred passage holds the deadline or limit itself
        w = text[max(0, start - 90):start]
        return bool(re.search(r"(prazos?|limiar(?:es)?|limites?|montantes?|valor(?:es)?)(?: mínimos?)?(?: para a apresentação d[ao]s? \w+)?,? (?:previstos?|referidos?|fixados?|estabelecidos?) (?:n[oa]s?|em) ?$", w))

    for m in SEG.finditer(text):
        art = article_for(m.end())
        if not art:
            continue
        nums = re.findall(r"\d+", m.group(2))
        als = re.findall(r"([a-z]|[ivx]+)\)", m.group(1) or "")
        for n in nums:
            for target in ([f"{art}.{n}.{a}" for a in als] if als else [f"{art}.{n}"]):
                if target != pid and law.text(target, date):
                    out.append((target, "texto", base(m.start())))
    for a in arts:
        if a.start() in used:
            continue
        g = a.group(0)
        if g.startswith("artigos anterior"):
            h = law.heading(aid, date).split()[:4]
            seq = law.arts(aid)
            prev = [x for x in seq[:seq.index(aid) if aid in seq else 0] if law.parent(x) == law.parent(aid) and law.heading(x, date).split()[:4] == h]
            out += [(x, "epigrafe", False) for x in prev[-3:]]
        elif g.startswith("artigo anterior"):
            seq = law.arts(aid)
            i = seq.index(aid) if aid in seq else 0
            if i:
                out.append((seq[i - 1], "epigrafe", False))
        elif a.group(1):
            for tok in re.findall(r"\d+\.º(?:-[A-Z])?", a.group(1)):
                x = art_pid(tok, ns)
                if x != aid and law.text(x, date):
                    out.append((x, "epigrafe", False))
    num = pid if law.kind(pid) == "numero" else (law.parent(pid) if law.kind(pid) in ("alinea", "subalinea") else None)
    while num and law.kind(num) != "numero":
        num = law.parent(num)
    if num:
        sibs = law.children(aid, date)
        i = sibs.index(num) if num in sibs else -1
        for m in re.finditer(r"(?<!\w)al[íi]nea ([a-z])\) do n[úu]mero anterior", text):
            if i > 0 and law.text(f"{sibs[i - 1]}.{m.group(1)}", date):
                out.append((f"{sibs[i - 1]}.{m.group(1)}", "texto", base(m.start())))
        for m in NUMREL.finditer(text):
            if m.group(0).endswith("prazo"):
                if i > 0:
                    out.append((sibs[i - 1], "texto", True))
                continue
            if "anteriores" in m.group(0):
                out += [(s, "texto", base(m.start())) for s in sibs[:i]]
            elif i > 0:
                out.append((sibs[i - 1], "texto", base(m.start())))
    if law.kind(pid) == "alinea" and ALREL.search(text):
        sibs = law.children(law.parent(pid), date)
        i = sibs.index(pid)
        if i > 0:
            out.append((sibs[i - 1], "texto", base(ALREL.search(text).start())))
    seen, res = set(), []
    for x in out:
        if x[0] not in seen:
            seen.add(x[0])
            res.append(x)
    return res


# ---- context ---------------------------------------------------------------------------------------------------------
def context(law, alvo, date, depth=3):
    """What the reader sees and what the checker may accept as a source. Roles: alvo, proemio (the number or alínea the
    target belongs to), remissao (referred to by the target, its proémio or a referred passage), remissao_epigrafe,
    epigrafe (the article's heading), titulo (chapter, section…), vizinho (the article's other passages)."""
    aid = law.article_of(alvo)
    roles, allowed = {}, {}
    chain, x = [], law.parent(alvo)
    while x and x != aid:
        chain.append(x)
        x = law.parent(x)
    roles[alvo] = "alvo"
    allowed[alvo] = law.own(alvo, date) if law.kind(alvo) == "artigo" else (law.text(alvo, date) or "")

    def mark_parts(pid):  # a target with alíneas is read with them: they complete its sentence
        for c in law.children(pid, date):
            roles[c], allowed[c] = "alvo", law.own(c, date)
            mark_parts(c)
    if law.kind(alvo) != "artigo":
        mark_parts(alvo)
    for c in chain:
        roles[c], allowed[c] = "proemio", law.own(c, date)
    roles[aid] = roles.get(aid) or "epigrafe"
    if aid != alvo:
        allowed[aid] = law.heading(aid, date)
        if law.parent(alvo) == aid and law.kind(alvo) in ("alinea", "subalinea"):  # «Para a celebração de … pode adotar-se:»
            body = re.split(r"\n(?=(?:[a-z]|[ivx]+)\) )", "\n".join((law.text(aid, date) or "").split("\n")[2:]), maxsplit=1)[0]
            allowed[aid] = allowed[aid] + "\n" + body
            roles[aid] = "proemio"
    place, x = [], law.parent(aid)
    while x:
        t = law.text(x, date)
        if t:
            place.append((x, t.replace("\n", " — ")))
            roles[x], allowed[x] = "titulo", t.replace("\n", " — ")
        x = law.parent(x)
    norma = (law.p.get(aid) or {}).get("norma")
    if norma:
        title = NORMA_TITLES.get(norma) or norma
        place.append((norma, title))
        roles[norma], allowed[norma] = "titulo", title
    place.reverse()
    # references, breadth first from the target and its proémio
    refs, frontier = [], [(alvo, 0)] + [(c, 0) for c in chain]
    while frontier:
        src, d = frontier.pop(0)
        if d >= depth:
            continue
        for target, kind, is_base in references(law, src, allowed.get(src) or law.own(src, date), date):
            if d > 0 and not is_base:
                continue
            if target in roles and roles[target] not in ("vizinho",):
                continue
            if kind == "epigrafe":
                roles[target], allowed[target] = "remissao_epigrafe", law.heading(target, date)
                refs.append((target, "epigrafe"))
                continue
            # a reference to a number is to all of it: its alíneas are shown with it (0.2)
            whole = law.kind(target) == "numero" and law.children(target, date)
            roles[target], allowed[target] = "remissao", (law.text(target, date) if whole else law.own(target, date))
            refs.append((target, "texto"))
            p = law.parent(target)
            if law.kind(target) in ("alinea", "subalinea") and p and p not in roles:  # a referred alínea is read with its proémio
                roles[p], allowed[p] = "remissao", law.own(p, date)
                refs.append((p, "texto"))
            if is_base:
                frontier.append((target, d + 1))
    # the article as shown: each passage once, the target and referred passages marked
    items = []

    def walk(pid, level):
        for c in law.children(pid, date):
            items.append((c, law.own(c, date), level))
            if c not in roles:
                roles[c] = "vizinho"
                allowed[c] = law.own(c, date)
            walk(c, level + 1)
    if law.children(aid, date):
        body = re.split(r"\n(?=(?:[a-z]|[ivx]+)\) |\d+ - )", "\n".join((law.text(aid, date) or "").split("\n")[2:]), maxsplit=1)[0].strip()
        if body:
            items.append((aid, body, 0))
        walk(aid, 0)
    else:
        items.append((aid, law.own(aid, date), 0))
        allowed[aid] = law.own(aid, date) if alvo == aid else allowed.get(aid, "")
    inside = {i[0] for i in items}
    return {"alvo": alvo, "date": date, "article": aid, "label": law.label(aid, date), "heading": law.heading(aid, date),
            "place": place, "items": items, "refs": sorted((r for r in refs if r[0] not in inside), key=lambda r: Law.key(r[0])), "roles": roles, "allowed": allowed,
            "heading_of": {r[0]: f"{law.label(law.article_of(r[0]), date)} — {law.heading(law.article_of(r[0]), date)}" for r in refs}}


# ---- the prompt ------------------------------------------------------------------------------------------------------
def vocab_text():
    c = VOC["condition_fields"]

    def words(field, v, n=2):
        return "«" + "», «".join(c[field]["values"][v][:n]) + "»"
    tc = ", ".join(f"{v} ({words('tipo_contrato', v)})" for v in c["tipo_contrato"]["values"])
    tp = ", ".join(c["tipo_procedimento"]["values"])
    return "\n".join([
        "VOCABULÁRIO (só estes campos e valores; entre «», palavras da lei para cada um)",
        f"tipo_contrato: {tc}. «Concessão de obras públicas ou de serviços» nomeia as duas concessões.",
        f"tipo_procedimento: {tp} — cada um pelo seu nome na lei; «ajuste direto simplificado», «consulta prévia especial» e «concurso público urgente» são procedimentos à parte.",
        "publicado_joue (true/false): o anúncio é publicado no Jornal Oficial da União Europeia; «envio do anúncio ao Serviço das Publicações da União Europeia» e «publicidade internacional» afirmam-no.",
        "urgencia_fundamentada (true/false): a entidade adjudicante fundamentou uma situação de urgência.",
        "setores_especiais (true/false): o contrato diz direta e principalmente respeito a atividades dos setores da água, da energia, dos transportes ou dos serviços postais.",
        "anuncio_pre_informacao (true/false): foi publicado o anúncio periódico indicativo.",
        "modalidade_concecao: publico, limitado, simplificado — a modalidade do concurso de conceção.",
        f"tipo_entidade: estado ({words('tipo_entidade', 'estado')}), outra ({words('tipo_entidade', 'outra')}).",
        "territorio: PT, PT-AC, PT-MA («Regiões Autónomas» = PT-AC e PT-MA). duracao_contrato_meses: número de meses («um ano» = 12). data_inicio_procedimento: data ISO (ano-mês-dia).",
        "valor_estimado, preco_base, preco_contratual: euros, como condição de um prazo que muda com o valor do contrato (L10).",
        "Operadores: eq, ne (um valor); in, not_in (uma lista); lt, le, gt, ge (números e datas).",
        "prazo_minimo — params: minimum_days (inteiro), deadline_field, counted_from, usual_days (inteiro ou null).",
        "deadline_field: " + ", ".join(f"{k} («{v[0]}»)" for k, v in VOC["deadline_fields"].items()) + ".",
        "counted_from: " + ", ".join(f"{k} («{v[0]}»)" for k, v in VOC["counted_from"].items()) + ", nao_indicado (L9).",
        "limiar — params: threshold = {field: " + " | ".join(f"{k} («{v[0]}»)" for k, v in VOC["threshold_fields"].items())
        + ", comparator: lt | le | gt | ge, value: euros, currency: \"EUR\"}."])


STATIC = """TAREFA
És um leitor da lei portuguesa. Lês uma passagem do Código dos Contratos Públicos — a passagem-alvo, marcada no texto — e escreves em JSON a regra que ela fixa, com o vocabulário e o formato abaixo. Só conta o texto mostrado: o que saibas da lei para além dele não entra. Outro leitor lê a mesma passagem com estas mesmas regras, sem ver a tua resposta; a regra só fica registada quando as duas leituras coincidem, e um programa confirma cada palavra que citares.

O QUE UMA REGRA QUER DIZER (é assim que o motor a aplica)
- prazo_minimo: «quando todas as condições se verificam, o prazo <deadline_field>, contado desde <counted_from>, não pode ser inferior a <minimum_days> dias». O motor dá «não cumpre» a um procedimento que fixe menos.
- limiar: «quando todas as condições se verificam, <field> do contrato tem de ser <comparator> <value> euros». O motor dá «não cumpre» a um procedimento cujo valor fique do outro lado. Um limiar é sempre o valor até ao qual um procedimento pode ser escolhido; esse procedimento é uma das condições.
- Antes de responder, aplica a tua regra assim: daria «não cumpre» a um procedimento que a passagem permite, ou «cumpre» a um que ela não permite? Se sim, corrige-a; se o vocabulário não chega para a escrever certa, aplica L12.

COMO LER (as mesmas regras para todos os leitores)
L1 Fontes. Cada condição e cada parâmetro vem de uma destas fontes, e só delas: a passagem-alvo, com as alíneas que a completam; o proémio do número ou da alínea de que ela faz parte; as passagens marcadas «remetida» (aquelas para que a passagem-alvo remete, e as que essas remetem); a epígrafe do artigo; os títulos do capítulo e da secção. Os outros números do artigo mostram-se só como contexto: um facto que apenas eles dizem não entra (exceção em L5).
L2 Fonte copiada. Em cada condição e em cada parâmetro, «fontes» tem as palavras exatas do texto que o dizem — as mais curtas que o digam — e o id de onde as copiaste. Sem palavras que o digam, a condição não existe. Condição é o que diz quando a regra se aplica; uma exigência sobre o que se faz («com convite a, pelo menos, três entidades», «o convite deve indicar») é outra regra e não entra.
L3 Procedimento, contrato e modalidade nomeados por um título. Entra tipo_procedimento quando uma fonte de L1 nomeia o procedimento; um título de capítulo ou de secção que é o nome de um procedimento nomeia-o. Decide o mais próximo da passagem: a passagem-alvo, o proémio, a epígrafe, a secção, o capítulo. Um título que nomeia dois procedimentos dá in [os dois]. O mesmo vale para tipo_contrato e modalidade_concecao. Um capítulo ou secção de um instrumento que o vocabulário não tem ({INSTR}) limita a regra a esse instrumento: aplica L12 (sem_vocabulario).
L4 Número que muda outro. Um número que reduz, alarga ou substitui o prazo ou o limite de outro («o prazo previsto no número anterior pode ser reduzido para 15 dias») dá uma regra com todas as condições do número para que remete — e as que esse herda —, o seu campo do prazo e o seu início da contagem, mais as condições e os dias do próprio número. «Reduzido para N dias» → N; «reduzido em até N dias» → os dias do número remetido menos N.
L5 Casos. Uma regra por caso: «seis dias ou, nas empreitadas de obras públicas, 14 dias» são duas regras (tipo_contrato ne obras com 6; eq obras com 14), cada uma com o seu comparador e o seu valor. «Nos restantes casos», «nos demais casos», «nos outros contratos» → not_in [todos os tipos nomeados nos outros casos], ou ne quando é um só; para isso, os números do artigo que fixam esses outros casos contam como fonte. Os casos de uma mesma passagem completam-se: «30 dias, ou 15 dias se a urgência for fundamentada» são duas regras, urgencia_fundamentada eq false na de 30 e eq true na de 15; «quando o não seja» nega o facto que a frase nomeia. Números diferentes não se completam: cada número dá a sua regra, e o motor aplica a mais específica. Uma passagem com um só prazo ou um só valor é uma regra. Nunca repitas uma regra nem dês a de outro número.
L6 Listas. «Com exceção de A e de B», «excetuados A e B», «salvo A ou B» → not_in [A, B]; «apenas», «só», «exclusivamente» → in [A, B]. «Contratos distintos dos previstos nos artigos anteriores» (ou «nos artigos X e Y») → not_in os tipos que as epígrafes desses artigos nomeiam (mostradas nas remissões), mais os que a passagem exclui por palavras.
L7 Factos de dois lados (publicado_joue, urgencia_fundamentada, setores_especiais, anuncio_pre_informacao): true quando uma fonte o afirma; false quando o nega («não seja publicado», «sem publicação de anúncio»); nenhuma condição quando nenhuma fonte o diz e nenhum caso da passagem o dá (L5) — nunca false por omissão.
L8 Comparação, como a fonte a escreve: «inferior a» → lt; «igual ou inferior a», «não superior a», «que não exceda» → le; «superior a» → gt; «igual ou superior a» → ge. No prazo, «não pode ser inferior a N dias», «nunca pode ficar abaixo de N dias», «de, pelo menos, N dias», «o prazo mínimo é de N dias» → minimum_days N.
L9 O prazo da passagem-alvo. Num artigo com vários prazos, a regra é a do prazo que a passagem-alvo fixa: o seu campo (o que se apresenta) e o seu início de contagem, pelas palavras do vocabulário; «contados do seu envio», «a contar do envio deste» contam-se do envio do documento que a frase nomeia (o convite ou o anúncio). Se a passagem, lida com as que remete, não diz de quando se conta, counted_from = nao_indicado, sem fonte.
L10 Números e grandezas. Dias e euros como o texto os escreve, em algarismos ou por extenso («seis dias» = 6; «1 000 000 €» = 1000000). No limiar, field é a grandeza que a fonte nomeia: «valor estimado do contrato» → valor_estimado; «preço base» → preco_base; «preço contratual» → preco_contratual. Um valor dado por remissão («inferior aos limiares referidos na alínea b) do n.º 3 do artigo 474.º») lê-se na passagem remetida, e cada valor remetido é um caso (L5). Quando é o prazo que muda com o valor do contrato («quando o preço base seja igual ou superior a 1 000 000 €»), o valor é uma condição — valor_estimado, preco_base ou preco_contratual, com lt, le, gt ou ge; num limiar, o valor é o parâmetro e nunca uma condição.
L11 «Em regra». Se a passagem fixa um prazo «em regra» e um mínimo «em caso algum», minimum_days = o mínimo e usual_days = o prazo «em regra»; senão, usual_days = null.
L12 Não tipável. Responde {"regras": [], "nao_tipavel": {...}} quando: nao_e_limiar — o valor não é o limite até ao qual um procedimento pode ser escolhido (dispensa uma obrigação, reserva um contrato, exclui um convidado, ou soma o valor de vários contratos); nao_e_prazo_minimo — o prazo é um máximo («não pode ser superior a»), é um prazo para a própria entidade adjudicante, ou não é para apresentar nada; sem_vocabulario — a regra precisa de um facto, de um valor ou de uma unidade que o vocabulário não tem (um procedimento fora da lista, um prazo em horas, dias úteis ou meses); texto_em_falta — os dias, o valor ou um facto de que a regra precisa estão num texto para que a passagem remete e que não está mostrado; uma remissão que só descreve (quem são as entidades, o que o anúncio ou o convite indicam) não impede a leitura. Em «falta», diz numa frase o que falta.
L13 Datas. data_inicio_procedimento só entra quando a própria passagem fixa a data a partir da qual se aplica. A data de referência escolhe o texto em vigor; nunca é uma condição.
L14 Forma. Um só valor → eq (ou ne); vários → in (ou not_in). tipo_entidade usa sempre eq («quando a entidade adjudicante não seja o Estado» → eq outra). As passagens que a regra cita são a passagem-alvo e as das tuas fontes: não as escrevas.

{VOCAB}

FORMATO — responde só com um objeto JSON:
{"regras": [{"tipo": "…", "condicoes": [{"field": "…", "op": "…", "value": …, "fontes": [{"texto": "…", "de": "…"}]}], "params": {…}, "fontes": {"<parâmetro>": [{"texto": "…", "de": "…"}]}}], "nao_tipavel": null}
ou, quando L12 se aplica: {"regras": [], "nao_tipavel": {"motivo": "nao_e_limiar | nao_e_prazo_minimo | sem_vocabulario | texto_em_falta", "fontes": [{"texto": "…", "de": "…"}], "falta": "…"}}
«fontes» dos params: minimum_days, deadline_field, counted_from (salvo nao_indicado) e usual_days (quando não é null), no prazo_minimo; field, comparator e value, no limiar.

Exemplo (artigo inventado, só para mostrar a forma):
Onde está: [exemplo:cap-ii] Capítulo II — Concurso público
[exemplo:art900] Artigo 900.º — Prazos para a apresentação das propostas
[exemplo:art900.1] 1 - Quando o anúncio seja publicado no Jornal Oficial da União Europeia, o prazo para a apresentação das propostas não pode ser inferior a 30 dias a contar da data do envio do anúncio.   ◀ remetida
[exemplo:art900.2] 2 - Em caso de urgência devidamente fundamentada, o prazo previsto no número anterior pode ser reduzido para 15 dias.   ◀ PASSAGEM-ALVO
Resposta: {EXAMPLE}"""

EXAMPLE = {"regras": [{"tipo": "prazo_minimo", "condicoes": [
    {"field": "tipo_procedimento", "op": "eq", "value": "concurso_publico", "fontes": [{"texto": "Concurso público", "de": "exemplo:cap-ii"}]},
    {"field": "publicado_joue", "op": "eq", "value": True, "fontes": [{"texto": "Quando o anúncio seja publicado no Jornal Oficial da União Europeia", "de": "exemplo:art900.1"}]},
    {"field": "urgencia_fundamentada", "op": "eq", "value": True, "fontes": [{"texto": "Em caso de urgência devidamente fundamentada", "de": "exemplo:art900.2"}]}],
    "params": {"minimum_days": 15, "deadline_field": "prazo_propostas_dias", "counted_from": "data_envio_anuncio", "usual_days": None},
    "fontes": {"minimum_days": [{"texto": "pode ser reduzido para 15 dias", "de": "exemplo:art900.2"}],
               "deadline_field": [{"texto": "apresentação das propostas", "de": "exemplo:art900.1"}],
               "counted_from": [{"texto": "a contar da data do envio do anúncio", "de": "exemplo:art900.1"}]}}],
    "nao_tipavel": None}
EXAMPLE_CTX = {"alvo": "exemplo:art900.2", "article": "exemplo:art900",
               "roles": {"exemplo:art900.2": "alvo", "exemplo:art900.1": "remissao", "exemplo:art900": "epigrafe", "exemplo:cap-ii": "titulo"},
               "allowed": {"exemplo:art900.2": "2 - Em caso de urgência devidamente fundamentada, o prazo previsto no número anterior pode ser reduzido para 15 dias.",
                           "exemplo:art900.1": "1 - Quando o anúncio seja publicado no Jornal Oficial da União Europeia, o prazo para a apresentação das propostas não pode ser inferior a 30 dias a contar da data do envio do anúncio.",
                           "exemplo:art900": "Prazos para a apresentação das propostas", "exemplo:cap-ii": "Capítulo II — Concurso público"}}


def render(ctx, rtype):
    mark = {"alvo": "   ◀ PASSAGEM-ALVO", "remissao": "   ◀ remetida", "proemio": "   ◀ proémio da passagem-alvo"}
    lines = [STATIC.replace("{VOCAB}", vocab_text()).replace("{INSTR}", ", ".join("«" + w + "»" for w in VOC["instrumentos_sem_valor"][::2])).replace("{EXAMPLE}", json.dumps(EXAMPLE, ensure_ascii=False)), "",
             f"O TEXTO (versão em vigor a {ctx['date']})",
             "Onde está: " + (" > ".join(f"[{i}] {t}" for i, t in ctx["place"]) or "—"),
             f"[{ctx['article']}] {ctx['label']} — {ctx['heading']}"]
    for pid, text, level in ctx["items"]:
        lines.append("  " * level + f"[{pid}] {text}" + mark.get(ctx["roles"].get(pid), ""))
    if ctx["refs"]:
        lines += ["", "Remissões (texto para que a passagem-alvo remete, em vigor na mesma data):"]
        for pid, kind in ctx["refs"]:
            if kind == "epigrafe":
                lines.append(f"[{pid}] {ctx['heading_of'][pid]} (epígrafe)   ◀ remetida")
            else:
                lines.append(f"[{pid}] ({ctx['heading_of'][pid]}) {ctx['allowed'][pid]}   ◀ remetida")
    lines += ["", "PERGUNTA", f"Que regra do tipo {rtype} fixa a passagem {ctx['alvo']}? Se fixa mais de uma, dá uma por caso; "
              "se não fixa nenhuma regra deste tipo, aplica L12."]
    return "\n".join(lines)


def schema(ctx, rtype):
    ids = sorted(i for i in ctx["roles"])
    src = {"type": "array", "minItems": 1, "items": {"type": "object", "properties": {
        "texto": {"type": "string"}, "de": {"type": "string", "enum": ids}}, "required": ["texto", "de"], "additionalProperties": False}}
    c = VOC["condition_fields"]
    enum_vals = sorted({v for f in c.values() if f["kind"] == "enum" for v in f["values"]})
    cond = {"type": "object", "properties": {
        "field": {"type": "string", "enum": list(c)},
        "op": {"type": "string", "enum": ["eq", "ne", "in", "not_in", "lt", "le", "gt", "ge"]},
        "value": {"anyOf": [{"type": "string", "enum": enum_vals}, {"type": "boolean"}, {"type": "number"},
                            {"type": "array", "minItems": 1, "items": {"type": "string", "enum": enum_vals}},
                            {"type": "string", "pattern": r"^\d{4}-\d{2}-\d{2}$"}]},
        "fontes": src}, "required": ["field", "op", "value", "fontes"], "additionalProperties": False}
    nullable_src = {"anyOf": [src, {"type": "null"}]}
    if rtype == "prazo_minimo":
        params = {"type": "object", "properties": {
            "minimum_days": {"type": "integer", "minimum": 1},
            "deadline_field": {"type": "string", "enum": list(VOC["deadline_fields"])},
            "counted_from": {"type": "string", "enum": list(VOC["counted_from"]) + ["nao_indicado"]},
            "usual_days": {"anyOf": [{"type": "integer", "minimum": 1}, {"type": "null"}]}},
            "required": ["minimum_days", "deadline_field", "counted_from", "usual_days"], "additionalProperties": False}
        fontes = {"type": "object", "properties": {"minimum_days": src, "deadline_field": src, "counted_from": nullable_src, "usual_days": nullable_src},
                  "required": ["minimum_days", "deadline_field", "counted_from", "usual_days"], "additionalProperties": False}
    else:
        params = {"type": "object", "properties": {"threshold": {"type": "object", "properties": {
            "field": {"type": "string", "enum": list(VOC["threshold_fields"])},
            "comparator": {"type": "string", "enum": ["lt", "le", "gt", "ge"]},
            "value": {"type": "number"}, "currency": {"type": "string", "enum": ["EUR"]}},
            "required": ["field", "comparator", "value", "currency"], "additionalProperties": False}},
            "required": ["threshold"], "additionalProperties": False}
        fontes = {"type": "object", "properties": {"field": src, "comparator": src, "value": src},
                  "required": ["field", "comparator", "value"], "additionalProperties": False}
    rule = {"type": "object", "properties": {"tipo": {"type": "string", "enum": [rtype]}, "condicoes": {"type": "array", "items": cond},
                                             "params": params, "fontes": fontes},
            "required": ["tipo", "condicoes", "params", "fontes"], "additionalProperties": False}
    nt = {"type": "object", "properties": {"motivo": {"type": "string", "enum": list(VOC["nao_tipavel_motivos"])}, "fontes": src,
                                           "falta": {"type": "string"}},
          "required": ["motivo", "fontes", "falta"], "additionalProperties": False}
    return {"type": "object", "properties": {"regras": {"type": "array", "maxItems": 4, "items": rule},
                                             "nao_tipavel": {"anyOf": [nt, {"type": "null"}]}},
            "required": ["regras", "nao_tipavel"], "additionalProperties": False}


# ---- the checker -----------------------------------------------------------------------------------------------------
CONDITION_ROLES = {"alvo", "proemio", "remissao", "remissao_epigrafe", "epigrafe", "titulo"}
PARAM_ROLES = {"alvo", "proemio", "remissao", "epigrafe"}
TWO_VALUED = {"tipo_entidade": ("estado", "outra")}


def _sources(ctx, fontes, roles_ok, where, errs, rest_ok=False):
    texts = []
    for f in fontes or []:
        de, txt = f.get("de"), f.get("texto", "")
        role = ctx["roles"].get(de)
        if role is None:
            errs.append(f"{where}: «de» {de} não está no texto mostrado")
            continue
        if role not in roles_ok and not (rest_ok and role == "vizinho"):
            errs.append(f"{where}: fonte em {de}, que é {role} (L1)")
        if not contains(ctx["allowed"].get(de, ""), txt):
            errs.append(f"{where}: «{txt[:60]}» não está em {de}")
            continue
        texts.append(txt)
    return " ‖ ".join(texts)


def check(reading, ctx, rtype):
    """Errors that keep a reading from being recorded; [] when every quoted word is in the text, comes from a source L1
    allows and says the value it is quoted for."""
    errs = []
    nt, rules = reading.get("nao_tipavel"), reading.get("regras") or []
    if nt:
        if rules:
            errs.append("não tipável com regras")
        if nt.get("motivo") not in VOC["nao_tipavel_motivos"]:
            errs.append(f"motivo {nt.get('motivo')} fora da lista")
        _sources(ctx, nt.get("fontes"), {"alvo", "proemio", "remissao", "epigrafe", "titulo"}, "não tipável", errs)  # L3: a title can be the reason
        return errs
    if not rules:
        return ["nem regras nem não tipável"]
    alvo_text = ctx["allowed"][ctx["alvo"]]
    rest = any(contains(alvo_text, w) for w in VOC["rest_phrases"])
    seen = set()
    for i, r in enumerate(rules, 1):
        w = f"regra {i}"
        if r.get("tipo") != rtype:
            errs.append(f"{w}: tipo {r.get('tipo')}")
        for c in r.get("condicoes", []):
            f, op, v = c.get("field"), c.get("op"), c.get("value")
            spec = VOC["condition_fields"].get(f)
            cw = f"{w}, {f} {op} {v}"
            if spec is None:
                errs.append(f"{cw}: campo fora do vocabulário")
                continue
            t = _sources(ctx, c.get("fontes"), CONDITION_ROLES, cw, errs, rest_ok=op in ("ne", "not_in") and rest)
            if spec["kind"] == "enum":
                vals = set(v if isinstance(v, list) else [v])
                if op not in ("eq", "ne", "in", "not_in") or (op in ("eq", "ne")) != (not isinstance(v, list)):
                    errs.append(f"{cw}: operador e valor não combinam (L14)")
                if spec.get("always_eq") and op != "eq":
                    errs.append(f"{cw}: {f} usa sempre eq (L14)")
                bad = vals - set(spec["values"])
                if bad:
                    errs.append(f"{cw}: valores fora do vocabulário {sorted(bad)}")
                named = values_named(f, t)
                if rest and op in ("eq", "in") and any(contains(t, w) for w in VOC["rest_phrases"]):
                    others = {x for j, r2 in enumerate(rules, 1) if j != i for c2 in r2.get("condicoes", [])
                              if c2.get("field") == f and c2.get("op") in ("eq", "in") for x in (c2["value"] if isinstance(c2["value"], list) else [c2["value"]])}
                    named |= (set(spec["values"]) - others) & vals
                for fq in c.get("fontes") or []:  # a quote that is part of a longer phrase naming another value («serviços» in «concessão de serviços»)
                    ns, nq = norm(ctx["allowed"].get(fq.get("de"), "")), norm(fq.get("texto", ""))
                    k = ns.find(nq) if nq else -1
                    if k >= 0 and not values_named(f, nq) <= values_named(f, ns[max(0, k - 40):k + len(nq) + 40]):
                        errs.append(f"{cw}: «{fq['texto'][:40]}» é parte de uma expressão que nomeia outro valor (L2)")
                if not vals <= named:
                    errs.append(f"{cw}: as fontes não nomeiam {sorted(vals - named)}")
                elif f != "modalidade_concecao" and named - vals:
                    errs.append(f"{cw}: as fontes nomeiam também {sorted(named - vals)} (fonte mais curta, ou a condição está incompleta)")
            elif spec["kind"] == "boolean":
                if op != "eq" or not isinstance(v, bool):
                    errs.append(f"{cw}: facto de dois lados usa eq true/false (L7)")
                elif v not in polarity(f, t) and not complement(f, t, rules, i, v):
                    errs.append(f"{cw}: as fontes não {'afirmam' if v else 'negam'} o facto (L7)")
            elif spec["kind"] == "number":
                months = {n * mult for n in numbers_in(t) for u, mult in spec["unit_words"].items() if re.search(rf"(?<!\w){u}(?!\w)", norm(t))}
                if not isinstance(v, (int, float)) or v not in months:
                    errs.append(f"{cw}: as fontes não dizem {v} meses")
                if op not in comparators_in(t):
                    errs.append(f"{cw}: as fontes não dizem «{op}» (L8)")
            elif spec["kind"] == "date":
                if not re.search(r"\d{1,2} de \w+ de \d{4}|\d{4}-\d{2}-\d{2}", t):
                    errs.append(f"{cw}: as fontes não fixam uma data (L13)")
            elif spec["kind"] == "amount":
                if rtype == "limiar":
                    errs.append(f"{cw}: num limiar o valor é o parâmetro, não uma condição (L10)")
                if not any(contains(t, ph) for ph in spec["phrases"]) or v not in euros_in(t) or op not in comparators_in(t):
                    errs.append(f"{cw}: as fontes não dizem {f} {op} {v} (L10)")
        p, pf = r.get("params", {}), r.get("fontes", {})
        if rtype == "prazo_minimo":
            t = _sources(ctx, pf.get("minimum_days"), PARAM_ROLES, f"{w}, minimum_days", errs)
            nums = numbers_in(t)
            reduction_by = any(contains(t, x) for x in VOC["reduction_by_phrases"])
            ok = p.get("minimum_days") in nums or (reduction_by and any(a - b == p.get("minimum_days") for a in nums for b in nums))
            if not ok:
                errs.append(f"{w}: minimum_days {p.get('minimum_days')} não está nas fontes (L8, L4)")
            t = _sources(ctx, pf.get("deadline_field"), PARAM_ROLES, f"{w}, deadline_field", errs)
            got = _named(t, VOC["deadline_fields"])
            if got != {p.get("deadline_field")}:
                errs.append(f"{w}: deadline_field {p.get('deadline_field')} e as fontes dizem {sorted(got) or 'nada'} (L9)")
            if p.get("counted_from") == "nao_indicado":
                said = set()
                counting = {k: [w for w in ws if re.search(r"a contar|contad[oa]s?|desde|após|a partir", w)] for k, ws in VOC["counted_from"].items()}
                for pid, role in ctx["roles"].items():
                    if role in ("alvo", "proemio", "remissao"):
                        said |= _named(ctx["allowed"][pid], counting)
                if said:
                    errs.append(f"{w}: nao_indicado, mas o texto diz {sorted(said)} (L9)")
            else:
                t = _sources(ctx, pf.get("counted_from"), PARAM_ROLES, f"{w}, counted_from", errs)
                got = counted_named(t)
                if got != {p.get("counted_from")}:
                    errs.append(f"{w}: counted_from {p.get('counted_from')} e as fontes dizem {sorted(got) or 'nada'} (L9)")
            if p.get("usual_days") is not None:
                t = _sources(ctx, pf.get("usual_days"), PARAM_ROLES, f"{w}, usual_days", errs)
                if not contains(t, "em regra") or p["usual_days"] not in numbers_in(t):
                    errs.append(f"{w}: usual_days sem «em regra» e os dias nas fontes (L11)")
        else:
            th = p.get("threshold", {})
            if not any(c.get("field") == "tipo_procedimento" and c.get("op") in ("eq", "in") for c in r.get("condicoes", [])):
                errs.append(f"{w}: um limiar tem sempre o procedimento que permite abaixo do valor; sem ele, L12 (nao_e_limiar)")
            t = _sources(ctx, pf.get("field"), PARAM_ROLES | {"remissao_epigrafe"}, f"{w}, field", errs)
            if _named(t, VOC["threshold_fields"]) != {th.get("field")}:
                errs.append(f"{w}: field {th.get('field')} e as fontes nomeiam {sorted(_named(t, VOC['threshold_fields'])) or 'nada'} (L10)")
            t = _sources(ctx, pf.get("comparator"), PARAM_ROLES, f"{w}, comparator", errs)
            if comparators_in(t) != {th.get("comparator")}:
                errs.append(f"{w}: comparator {th.get('comparator')} e as fontes dizem {sorted(comparators_in(t)) or 'nada'} (L8)")
            t = _sources(ctx, pf.get("value"), PARAM_ROLES, f"{w}, value", errs)
            if th.get("value") not in euros_in(t):
                errs.append(f"{w}: value {th.get('value')} não está nas fontes (L10)")
        k = json.dumps(canonical_rule(r), sort_keys=True, ensure_ascii=False)
        if k in seen:
            errs.append(f"{w}: repete outra regra (L5)")
        seen.add(k)
    return errs


def complement(field, text, rules, i, value=False):
    """A case of one passage completes another (L5): «30 dias, ou 15 dias se a urgência…» gives false to the 30-day rule
    when another rule of the same answer has the fact true, and «25 dias ou, quando o anúncio não seja publicado…, 15 dias»
    gives true to the 25-day rule when another has it false; «quando o não seja» negates the fact the sentence names."""
    if not value and any(contains(text, w) for w in VOC.get("alternative_negations", [])) and polarity(field, text):
        return True
    return (not value) in polarity(field, text) and any(
        j != i and any(c.get("field") == field and c.get("value") is (not value) for c in r.get("condicoes", r.get("conditions", [])))
        for j, r in enumerate(rules, 1))


def canonical_rule(r):
    conds = []
    for c in r.get("condicoes", []):
        f, op, v = c["field"], c["op"], c["value"]
        if isinstance(v, list):
            v = sorted(set(v))
            if len(v) == 1:
                op, v = {"in": "eq", "not_in": "ne"}.get(op, op), v[0]
        if f in TWO_VALUED and op == "ne":
            a, b = TWO_VALUED[f]
            op, v = "eq", (b if v == a else a)
        if isinstance(v, bool) and op == "ne":
            op, v = "eq", not v
        conds.append({"field": f, "op": op, "value": v})
    return {"tipo": r.get("tipo"), "condicoes": sorted(conds, key=lambda c: json.dumps(c, sort_keys=True, ensure_ascii=False)), "params": r.get("params")}


def canonical(reading):
    if reading.get("nao_tipavel"):
        return {"nao_tipavel": reading["nao_tipavel"].get("motivo")}
    return {"regras": sorted((canonical_rule(r) for r in reading["regras"]), key=lambda r: json.dumps(r, sort_keys=True, ensure_ascii=False))}


def cited(reading, ctx):
    """The passages a rule cites: the target and every passage its quotes come from (L14)."""
    out = []
    for r in reading.get("regras") or []:
        ids = {ctx["alvo"]}
        for c in r.get("condicoes", []):
            ids |= {f["de"] for f in c.get("fontes", [])}
        for fs in (r.get("fontes") or {}).values():
            ids |= {f["de"] for f in fs or []}
        out.append(sorted(ids))
    return out


# ---- support: old answers and written gold, which carry no quotes -----------------------------------------------------
def support(rule, ctx, rtype, rules=()):
    """What an answer written without quotes claims that no allowed source says (the v3 sources and words, L1-L13)."""
    errs = []
    alvo_text = ctx["allowed"][ctx["alvo"]]
    rest = any(contains(alvo_text, w) for w in VOC["rest_phrases"])
    cond_text = " ‖ ".join(t for pid, t in ctx["allowed"].items() if ctx["roles"][pid] in CONDITION_ROLES)
    near_text = cond_text + (" ‖ " + " ‖ ".join(t for pid, t in ctx["allowed"].items() if ctx["roles"][pid] == "vizinho") if rest else "")
    param_text = " ‖ ".join(t for pid, t in ctx["allowed"].items() if ctx["roles"][pid] in PARAM_ROLES)
    for c in rule.get("conditions") or rule.get("condicoes") or []:
        f, op, v = c["field"], c["op"], c["value"]
        spec = VOC["condition_fields"].get(f)
        cw = f"{f} {op} {v}"
        if spec is None:
            errs.append(f"{cw}: campo fora do vocabulário v3")
            continue
        t = near_text if op in ("ne", "not_in") else cond_text
        if spec["kind"] == "enum":
            vals = set(v if isinstance(v, list) else [v])
            missing = vals - values_named(f, t)
            if missing and rest and op in ("eq", "in"):  # «nas restantes modalidades»: the values the other cases do not name
                others = {x for r2 in rules if r2 is not rule for c2 in (r2.get("conditions") or r2.get("condicoes") or [])
                          if c2["field"] == f and c2["op"] in ("eq", "in") for x in (c2["value"] if isinstance(c2["value"], list) else [c2["value"]])}
                missing -= set(spec["values"]) - others
            if missing:
                errs.append(f"{cw}: nenhuma fonte nomeia {sorted(missing)}")
        elif spec["kind"] == "boolean":
            rs = list(rules) or [rule]
            k = next((n for n, x in enumerate(rs, 1) if x is rule), 0)
            if v not in polarity(f, cond_text) and not (v is False and complement(f, alvo_text, rs, k)):
                errs.append(f"{cw}: nenhuma fonte {'afirma' if v else 'nega'} (L7)")
        elif spec["kind"] == "amount":
            if rtype == "limiar":
                errs.append(f"{cw}: num limiar o valor é o parâmetro, não uma condição (L10)")
            elif not any(contains(cond_text, ph) for ph in spec["phrases"]) or v not in euros_in(cond_text):
                errs.append(f"{cw}: nenhuma fonte diz {f} {v} (L10)")
        elif spec["kind"] == "date":
            if not re.search(r"\d{1,2} de \w+ de \d{4}|\d{4}-\d{2}-\d{2}", cond_text):
                errs.append(f"{cw}: nenhuma fonte fixa uma data (L13)")
    p = rule.get("params") or {}
    if rtype == "prazo_minimo":
        if p.get("minimum_days") not in numbers_in(param_text) and not any(contains(param_text, x) for x in VOC["reduction_by_phrases"]):
            errs.append(f"minimum_days {p.get('minimum_days')}: não está no texto")
        if p.get("deadline_field") not in _named(param_text, VOC["deadline_fields"]):
            errs.append(f"deadline_field {p.get('deadline_field')}: o texto não o diz")
        said = counted_named(param_text)
        if p.get("counted_from") == "nao_indicado" and said:
            errs.append(f"counted_from nao_indicado: o texto diz {sorted(said)}")
        elif p.get("counted_from") not in ("nao_indicado", None) and p.get("counted_from") not in said:
            errs.append(f"counted_from {p.get('counted_from')}: o texto não o diz")
    else:
        th = p.get("threshold") or {}
        if th.get("value") not in euros_in(param_text):
            errs.append(f"value {th.get('value')}: não está no texto")
        if th.get("comparator") not in comparators_in(param_text):
            errs.append(f"comparator {th.get('comparator')}: o texto diz {sorted(comparators_in(param_text))}")
        named = _named(param_text, VOC["threshold_fields"])
        if th.get("field") not in named:
            errs.append(f"field {th.get('field')}: o texto nomeia {sorted(named) or 'nada'} (L10)")
    return errs


def selftest():
    errs = check(EXAMPLE, EXAMPLE_CTX, "prazo_minimo")
    if __name__ == "__main__":
        print("prompt example:", errs or "passes")
    import copy
    broken = []

    def mutate(name, fn):
        r = copy.deepcopy(EXAMPLE)
        fn(r["regras"][0])
        e = check(r, EXAMPLE_CTX, "prazo_minimo")
        broken.append((name, e))
    mutate("urgência false sem fonte que a negue", lambda r: r["condicoes"].__setitem__(2, {"field": "urgencia_fundamentada", "op": "eq", "value": False, "fontes": [{"texto": "Em caso de urgência devidamente fundamentada", "de": "exemplo:art900.2"}]}))
    mutate("JOUE eq false acrescentado", lambda r: r["condicoes"].append({"field": "publicado_joue", "op": "eq", "value": False, "fontes": [{"texto": "Jornal Oficial", "de": "exemplo:art900.1"}]}))
    mutate("procedimento inventado", lambda r: r["condicoes"].append({"field": "tipo_procedimento", "op": "eq", "value": "concurso_concecao", "fontes": [{"texto": "Concurso público", "de": "exemplo:cap-ii"}]}))
    mutate("citação que não está no texto", lambda r: r["condicoes"][1]["fontes"][0].__setitem__("texto", "quando o anúncio não seja publicado"))
    mutate("dias errados", lambda r: r["params"].__setitem__("minimum_days", 10))
    mutate("campo do prazo errado", lambda r: r["params"].__setitem__("deadline_field", "prazo_candidaturas_dias"))
    mutate("nao_indicado quando o texto diz de quando", lambda r: (r["params"].__setitem__("counted_from", "nao_indicado"), r["fontes"].__setitem__("counted_from", None)))
    mutate("data de referência como condição", lambda r: r["condicoes"].append({"field": "data_inicio_procedimento", "op": "eq", "value": "2026-10-01", "fontes": [{"texto": "Em caso de urgência", "de": "exemplo:art900.2"}]}))
    mutate("fonte num id que não existe", lambda r: r["condicoes"][0]["fontes"][0].__setitem__("de", "exemplo:art899"))
    for name, e in broken:
        if __name__ == "__main__":
            print(f"  {'rejected' if e else 'ACCEPTED (checker gap)'} — {name}: {e[0] if e else ''}")
    return all(e for _, e in broken) and not errs


# ---- the factory's side ------------------------------------------------------------------------------------------------
def parse(text):
    """An answer text as {"regras", "nao_tipavel"}; None when it is not that object."""
    try:
        a = json.loads(text)
    except (TypeError, json.JSONDecodeError):
        return None
    if not isinstance(a, dict) or "regras" not in a or not isinstance(a.get("regras"), list):
        return None
    a.setdefault("nao_tipavel", None)
    return a


def context_record(ctx):
    """What prompt.json keeps of the context, so the checker reads an answer against the text its reader saw."""
    return {"alvo": ctx["alvo"], "date": ctx["date"], "article": ctx["article"], "roles": ctx["roles"], "allowed": ctx["allowed"]}


def to_readings(reading, ctx, rtype):
    """The rules of a checked v3 reading in the shape read_rules builds a regra from: type, passages (cited, L14),
    conditions without their quotes, params (usual_days null left out)."""
    out = []
    for r, ids in zip(reading.get("regras") or [], cited(reading, ctx)):
        conds = [{"field": c["field"], "op": c["op"], "value": c["value"]} for c in r.get("condicoes", [])]
        params = {k: v for k, v in (r.get("params") or {}).items() if v is not None}
        out.append({"type": rtype, "passages": [i for i in ids if i in ctx["allowed"] and ctx["roles"].get(i) != "titulo" and not i.startswith("norma:")],
                    "conditions": conds, "params": params})
    return out


def replicate(a, b):
    """Two checked v3 readings replicate when their canonical content is equal: the same rules (quotes and passages aside)
    or the same «não tipável» reason."""
    return a is not None and b is not None and json.dumps(canonical(a), sort_keys=True, ensure_ascii=False) == json.dumps(canonical(b), sort_keys=True, ensure_ascii=False)


if __name__ == "__main__":
    sys.exit(0 if selftest() else 1)
