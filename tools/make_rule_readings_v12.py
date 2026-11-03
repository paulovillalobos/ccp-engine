"""Phase 15 data (DECISIONS D66): data-v12, the written articles in the reading protocol v3.

    .venv/bin/python tools/make_rule_readings_v12.py check [--only PREFIX]   render, derive the quotes, run the checker; writes nothing
    .venv/bin/python tools/make_rule_readings_v12.py generate                training/data-v12

Every written article (training/rule-readings: batch-* (D63), alvo-* (D65), eval-* (D65); v3-* and eval3-* (D66), written
in the v3 shape: titles, remissões, alíneas, «não tipável», gt/ge, amounts as conditions) becomes a law of its own in
memory (read_rules_v3.Law.from_passages) and is rendered by the factory's own code: the same context, prompt and schema
as a real target. Its gold is the article's rules, or its «não tipável», with every quote derived by code from the text;
the gold must pass the factory's checker, or the example is listed and left out. The threshold field is the amount the
text names next to the value (product_rule:vocabulario-v3); conditions are written in canonical form (L14).

Out (train_lora keys a task by its folder; a later data directory's folder replaces an earlier one's):
- regra_lida/train.jsonl: batch-*, alvo-* and v3-*, each once; replaces data-v10's old-format regra_lida
- regra_lida_alvo/train.jsonl: empty, which takes data-v11's old-format rows out of the mix
- regra_lida/dev_antigo.jsonl: eval-* (data-v11's dev and sealed, both measured already; never trained)
- regra_lida/dev.jsonl and sealed.jsonl: eval3-*, split by sha256 of the id; sealed is read by no reader until v12 is
  trained and BEFORE is committed. In id order, an eval3 article whose target passage is close to an earlier one's is
  dropped; a training article close to an eval3 or real passage is dropped (difflib ratio LEAK).
- REJECTED.json: every article left out and why; INDEX.json.
"""
import argparse
import difflib
import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT)); sys.path.insert(0, str(ROOT / "tools"))
import make_rule_readings as m  # noqa: E402  (the written articles' ids and the real passages they must not copy)
import read_rules_v3 as v3  # noqa: E402  (D66: the factory's context, prompt, schema and checker)

VERSION = "ccp-make-rule-readings-v12-0.1"
PROTOCOL = "ccp-read-rules-v3-0.3"  # data-v12 is rendered and checked with this protocol (a later one passes its own: D67)
DATA = ROOT / "training/data-v12"
TASK = "regra_lida"
DATE = "2026-10-01"
LEAK = m.LEAK
SOURCES = [("batch-*.jsonl", "train"), ("alvo-*.jsonl", "train"), ("v3-*.jsonl", "train"), ("eval-*.jsonl", "dev_antigo"), ("eval3-*.jsonl", "eval3")]
VOC = v3.VOC
REV_OLD = {}
for _old, _new in VOC["old_spelling"].items():
    REV_OLD.setdefault(_new, []).append(_old)
ORDER = ["alvo", "proemio", "remissao", "epigrafe", "remissao_epigrafe", "titulo"]
PARAM_ORDER = ["alvo", "proemio", "remissao", "epigrafe"]


class Gap(ValueError):
    """The gold says something the code cannot find words for in the text."""


# ---- the written article as a law ------------------------------------------------------------------------------------
def kind_of(path):
    last = path.split(".")[-1]
    return "numero" if last.isdigit() else ("subalinea" if re.fullmatch(r"[ivx]+", last) else "alinea")


def version(text):
    return [{"version": DATE, "text": text, "valid_from": "2000-01-01", "valid_to": None, "revoked": False}]


def article_passages(artigo, epigrafe, numeros, texto, parent):
    aid = f"{m.LAW}:{m.slug_art(artigo)}"
    body = [x["texto"] for x in numeros] if numeros else [texto]
    out = [{"id": aid, "revision": 1, "kind": "artigo", "parent": parent, "norma": "norma:exemplo", "versions": version("\n".join([f"Artigo {artigo}", epigrafe] + body))}]
    for x in numeros:
        up = x["n"].rsplit(".", 1)[0] if "." in x["n"] else ""
        out.append({"id": f"{aid}.{x['n']}", "revision": 1, "kind": kind_of(x["n"]), "parent": f"{aid}.{up}" if up else aid, "norma": "norma:exemplo", "versions": version(x["texto"])})
    return out


def law_of(ex):
    """The written article (its titles, its numbers and the articles it refers to) as passage objects of one law."""
    passages, parent = [], None
    for k, titulo in enumerate(ex.get("lugar") or [], 1):
        kind = "secao" if titulo.lower().startswith("secção") else ("titulo" if titulo.lower().startswith("título") else "capitulo")
        head, _, rest = titulo.partition(" — ")
        passages.append({"id": f"{m.LAW}:lugar-{k}", "revision": 1, "kind": kind, "parent": parent, "norma": "norma:exemplo", "versions": version(f"{head}\n{rest}" if rest else head)})
        parent = f"{m.LAW}:lugar-{k}"
    passages += article_passages(ex["artigo"], ex["epigrafe"], ex["numeros"], ex.get("texto", ""), parent)
    for r in ex.get("remissoes") or []:
        passages += article_passages(r["artigo"], r["epigrafe"], r.get("numeros") or [], r.get("texto", ""), parent if r.get("mesmo_lugar") else None)
    return v3.Law.from_passages(passages), m.pid_of(ex, ex["alvo"])


def ctx_of(ex):
    law, alvo = law_of(ex)
    return v3.context(law, alvo, DATE)


# ---- quotes found by code ----------------------------------------------------------------------------------------------
def pattern_of(phrase):
    parts = []
    for tok in phrase.split():
        alts = [re.escape(tok)] + [re.escape(o) for o in REV_OLD.get(tok.lower(), [])]
        parts.append("(?:" + "|".join(alts) + ")")
    return re.compile(r"(?<!\w)" + r"\s+".join(parts) + r"(?!\w)", re.I)


def spans(text, phrase):
    return [(x.start(), x.end()) for x in pattern_of(phrase).finditer(text)]


def sources(ctx, order, extra=()):
    roles = list(order) + list(extra)
    return sorted((pid for pid, role in ctx["roles"].items() if role in roles), key=lambda pid: (roles.index(ctx["roles"][pid]), pid))


def other_phrases(field, value):
    spec = VOC["condition_fields"][field]
    out = [w for v, ws in spec["values"].items() if v != value for w in ws]
    if field == "tipo_contrato" and value not in ("concessao_obras", "concessao_servicos"):
        out += spec["both_concessions"]
    return out


def inside_other(field, value, text, s, e):
    """True when text[s:e] lies inside a longer phrase that names another value («serviços» in «concessão de serviços»)."""
    for w in other_phrases(field, value):
        for s2, e2 in spans(text, w):
            if s2 <= s and e <= e2 and (e2 - s2) > (e - s):
                return True
    return False


def enum_quotes(field, values, ctx, extra=()):
    spec = VOC["condition_fields"][field]
    left, out = set(values), []
    for pid in sources(ctx, ORDER, extra):
        text = ctx["allowed"][pid]
        for pair, key in (({"concessao_obras", "concessao_servicos"}, "both_concessions"), ({"PT-AC", "PT-MA"}, "both_regions")):
            if key in spec and pair <= left:
                for w in sorted(spec[key], key=len, reverse=True):
                    sp = spans(text, w)
                    if sp:
                        out.append({"texto": text[sp[0][0]:sp[0][1]], "de": pid})
                        left -= pair
                        break
        for v in sorted(left):
            for w in sorted(spec["values"][v], key=len, reverse=True):
                hit = next(((s, e) for s, e in spans(text, w) if not inside_other(field, v, text, s, e)), None)
                if hit:
                    out.append({"texto": text[hit[0]:hit[1]], "de": pid})
                    left.discard(v)
                    break
        if not left:
            return out
    alvo = ctx["allowed"][ctx["alvo"]]
    for w in VOC["rest_phrases"]:  # the values the passage's other cases do not name (L5); the checker confirms it
        sp = spans(alvo, w)
        if sp:
            return out + [{"texto": alvo[sp[0][0]:sp[0][1]], "de": ctx["alvo"]}]
    raise Gap(f"{field}: no words for {sorted(left)}")


NEG = re.compile(r"(?<!\w)(não|sem|fora d[oa]s?)(?!\w)", re.I)


def bool_quotes(field, value, ctx):
    phrases = sorted(VOC["condition_fields"][field]["phrases"], key=len, reverse=True)
    for pid in sources(ctx, ORDER):
        text = ctx["allowed"][pid]
        for w in phrases:
            for s, e in spans(text, w):
                before = text[max(0, s - 45):s]
                both = [b for b in VOC.get("both_polarities", []) for x in [spans(before, b)] if x]
                if both:
                    k = max(sp[0] for b in both for sp in spans(before, b))
                    return [{"texto": text[max(0, s - 45) + k:e], "de": pid}]
                neg = list(NEG.finditer(before))
                if value is True and not neg:
                    return [{"texto": text[s:e], "de": pid}]
                if value is False and neg:
                    return [{"texto": text[max(0, s - 45) + neg[-1].start():e], "de": pid}]
    if value is False:  # a case of the same passage completes another (L5), or «quando o não seja»
        text = ctx["allowed"][ctx["alvo"]]
        for alt in VOC.get("alternative_negations", []):
            for s2, e2 in spans(text, alt):
                for w in phrases:
                    before = [(s, e) for s, e in spans(text, w) if e <= s2]
                    if before:
                        return [{"texto": text[before[-1][0]:e2], "de": ctx["alvo"]}]
        for w in phrases:
            for s, e in spans(text, w):
                return [{"texto": text[s:e], "de": ctx["alvo"]}]
    if value is True:  # «25 dias ou, quando o anúncio não seja publicado…, 15 dias»: the other case of a fact the passage denies
        text = ctx["allowed"][ctx["alvo"]]
        for w in phrases:
            for s, e in spans(text, w):
                neg = list(NEG.finditer(text[max(0, s - 45):s]))
                if neg:
                    return [{"texto": text[max(0, s - 45) + neg[-1].start():e], "de": ctx["alvo"]}]
    raise Gap(f"{field} {value}: no words that {'state' if value else 'deny'} it")


AMOUNT = re.compile(r"(\d{1,3}(?:[ . ]\d{3})+|\d+)(?:,\d+)?\s*(?:€|euros?\b)|\(euro\)\s*(\d{1,3}(?:[ . ]\d{3})+|\d+)", re.I)


def amount_spans(text, value):
    out = []
    for x in AMOUNT.finditer(text):
        n = int(re.sub(r"[ . ]", "", x.group(1) or x.group(2)))
        if n == value:
            out.append((x.start(), x.end()))
    words = "|".join(sorted(list(v3.WORD_NUM) + ["mil", "milhão", "milhões", "e"], key=len, reverse=True))
    for x in re.finditer(rf"(?<!\w)((?:(?:{words})\s+)+)(?:de\s+)?euros\b", text, re.I):
        if v3.words_value(x.group(1).strip().lower()) == value:
            out.append((x.start(), x.end()))
    return out


def near_before(text, s, table, window):
    """The longest phrase of table that ends closest before s, within window characters: (start, end, value) or None."""
    best = None
    for v, ws in table.items():
        for w in ws:
            for s2, e2 in spans(text[max(0, s - window):s], w):
                a, b = s2 + max(0, s - window), e2 + max(0, s - window)
                if best is None or b > best[1] or (b == best[1] and a < best[0]):
                    best = (a, b, v)
    return best


def amount_condition_quotes(field, op, value, ctx):
    phrases = VOC["condition_fields"][field]["phrases"]
    for pid in sources(ctx, ORDER):
        text = ctx["allowed"][pid]
        for s, e in amount_spans(text, value):
            f = near_before(text, s, {field: phrases}, 140)
            if f:
                q = text[f[0]:e]
                if op in v3.comparators_in(q):
                    return [{"texto": q, "de": pid}]
                for x in re.finditer(r"(?:esse|aquele|o mesmo) (?:valor|montante|preço)", text[e:], re.I):
                    q = text[(f[0] if f else s):e + x.end()]
                    if op in v3.comparators_in(text[e:e + x.end()]):
                        return [{"texto": q, "de": pid}]
    raise Gap(f"{field} {op} {value}: no words for it")


DAYS = r"(?:\s+dias)"


def day_spans(text, n):
    out = [(x.start(), x.end()) for x in re.finditer(rf"(?<![\d.]){n}{DAYS}(?!\s+úteis)", text)]
    for w, v in {**v3.UNITS, **v3.TENS}.items():
        if v == n:
            out += [(x.start(), x.end()) for x in re.finditer(rf"(?<!\w){w}{DAYS}(?!\s+úteis)", text, re.I)]
    if n > 20 and n % 10:
        tens, units = n - n % 10, n % 10
        for wt, vt in v3.TENS.items():
            for wu, vu in v3.UNITS.items():
                if vt == tens and vu == units:
                    out += [(x.start(), x.end()) for x in re.finditer(rf"(?<!\w){wt} e {wu}{DAYS}", text, re.I)]
    return sorted(out)


def first(ctx, order, finder):
    for pid in sources(ctx, order):
        text = ctx["allowed"][pid]
        hit = finder(text)
        if hit:
            return [{"texto": text[hit[0]:hit[1]], "de": pid}]
    return None


def phrase_finder(table, value):
    ws = sorted(table[value], key=len, reverse=True)

    def f(text):
        for w in ws:
            sp = spans(text, w)
            if sp:
                return sp[0]
        return None
    return f


def prazo_quotes(p, ctx):
    out = {}
    q = first(ctx, PARAM_ORDER, lambda t: (day_spans(t, p["minimum_days"]) or [None])[0])
    if q is None:  # «reduzido em até N dias»: the referred number's days less N (L4)
        for pid in sources(ctx, PARAM_ORDER):
            text = ctx["allowed"][pid]
            for w in VOC["reduction_by_phrases"]:
                for s, e in spans(text, w):
                    tail = re.match(r"\s*(\d+|\w+)\s+dias", text[e:])
                    if tail:
                        n = int(tail.group(1)) if tail.group(1).isdigit() else v3.WORD_NUM.get(tail.group(1).lower())
                        base = first(ctx, PARAM_ORDER, lambda t, b=(n or 0) + p["minimum_days"]: (day_spans(t, b) or [None])[0])
                        if n and base:
                            q = [{"texto": text[s:e + tail.end()], "de": pid}] + base
                            break
                if q:
                    break
            if q:
                break
    if q is None:
        raise Gap(f"minimum_days {p['minimum_days']}: not in the text")
    out["minimum_days"] = q
    q = first(ctx, PARAM_ORDER, phrase_finder(VOC["deadline_fields"], p["deadline_field"]))
    if q is None:
        raise Gap(f"deadline_field {p['deadline_field']}: no words for it")
    out["deadline_field"] = q
    if p["counted_from"] == "nao_indicado":
        out["counted_from"] = None
    else:
        q = first(ctx, PARAM_ORDER, phrase_finder(VOC["counted_from"], p["counted_from"]))
        if q is None and p["counted_from"] == "data_publicacao_anuncio":  # «a contar da sua publicação», after «anúncio»
            for pid in sources(ctx, PARAM_ORDER):
                text = ctx["allowed"][pid]
                for w in VOC.get("anaphoric_publication", []):
                    for s, e in spans(text, w):
                        k = max((x.start() for x in re.finditer(r"an[úu]ncio", text[:s], re.I)), default=None)
                        if k is not None:
                            q = [{"texto": text[k:e], "de": pid}]
                            break
                    if q:
                        break
                if q:
                    break
        if q is None:  # «contados do seu envio»: from the document the sentence names last before those words
            for pid in sources(ctx, PARAM_ORDER):
                text = ctx["allowed"][pid]
                for w in VOC.get("anaphoric_sending", []):
                    for s, e in spans(text, w):
                        doc = "convite" if p["counted_from"] == "data_envio_convite" else "anúncio"
                        k = max((x.start() for x in re.finditer(doc, text[:s], re.I)), default=None)
                        if k is not None:
                            q = [{"texto": text[k:e], "de": pid}]
                            break
                    if q:
                        break
                if q:
                    break
        if q is None:
            raise Gap(f"counted_from {p['counted_from']}: no words for it")
        out["counted_from"] = q
    if p.get("usual_days"):
        def usual(t):
            for s, e in spans(t, "em regra"):
                stop = min([k for k in (t.find(";", e), t.find(". ", e)) if k > 0] or [len(t)])
                d = [x for x in day_spans(t, p["usual_days"]) if s <= x[0] < stop]
                if d:
                    return (s, d[0][1])
            return None
        q = first(ctx, PARAM_ORDER, usual)
        if q is None:
            raise Gap(f"usual_days {p['usual_days']}: no «em regra» with those days")
        out["usual_days"] = q
    else:
        out["usual_days"] = None
    return out


def limiar_quotes(th, ctx):
    """value, comparator and field of a limiar, and the field the text names (it replaces the gold's, D66)."""
    for pid in sources(ctx, PARAM_ORDER):
        text = ctx["allowed"][pid]
        for s, e in amount_spans(text, th["value"]):
            value_q = [{"texto": text[s:e], "de": pid}]
            comp = near_before(text, s, VOC["comparators"], 60)
            field = near_before(text, s, VOC["threshold_fields"], 160)
            if comp is None or field is None:  # a value by reference: the words are in the target or its proémio
                for pid2 in sources(ctx, ["alvo", "proemio"]):
                    t2 = ctx["allowed"][pid2]
                    end = len(t2)
                    comp = comp or (lambda c: c and (c[0], c[1], c[2], pid2))(near_before(t2, end, VOC["comparators"], end))
                    field = field or (lambda c: c and (c[0], c[1], c[2], pid2))(near_before(t2, end, VOC["threshold_fields"], end))
            if comp is None or field is None:
                continue
            cq = {"texto": (ctx["allowed"][comp[3]] if len(comp) > 3 else text)[comp[0]:comp[1]], "de": comp[3] if len(comp) > 3 else pid}
            fq = {"texto": (ctx["allowed"][field[3]] if len(field) > 3 else text)[field[0]:field[1]], "de": field[3] if len(field) > 3 else pid}
            return {"value": value_q, "comparator": [cq], "field": [fq]}, comp[2], field[2]
    raise Gap(f"value {th['value']}: not in the text")


# ---- the gold in v3 ----------------------------------------------------------------------------------------------------
def canon_condition(c):
    f, op, v = c["field"], c["op"], c["value"]
    if isinstance(v, list):
        v = sorted(set(v))
        if len(v) == 1:
            op, v = {"in": "eq", "not_in": "ne"}.get(op, op), v[0]
    if f in v3.TWO_VALUED and op == "ne":
        a, b = v3.TWO_VALUED[f]
        op, v = "eq", (b if v == a else a)
    if isinstance(v, bool) and op == "ne":
        op, v = "eq", not v
    return {"field": f, "op": op, "value": v}


def derive(ex, ctx):
    """The article's gold as a v3 answer, every quote found by code in the text it shows."""
    rtype = ex["tipo"]
    if ex.get("nao_tipavel"):
        nt = ex["nao_tipavel"]
        hit = None
        for pid in sources(ctx, ["alvo", "proemio", "remissao"]):
            if v3.contains(ctx["allowed"][pid], nt["fonte"]):
                sp = spans(ctx["allowed"][pid], nt["fonte"])
                hit = {"texto": ctx["allowed"][pid][sp[0][0]:sp[0][1]] if sp else nt["fonte"], "de": pid}
                break
        if hit is None:
            raise Gap(f"não tipável: «{nt['fonte'][:50]}» is not in the target, its proémio or a remissão")
        return {"regras": [], "nao_tipavel": {"motivo": nt["motivo"], "fontes": [hit], "falta": nt["falta"]}}
    alvo_text = ctx["allowed"][ctx["alvo"]]
    rest = any(v3.contains(alvo_text, w) for w in VOC["rest_phrases"])
    if rtype == "limiar" and not any(c["field"] == "tipo_procedimento" for r in ex["regras"] for c in r["condicoes"]):
        named = set()
        for pid, role in ctx["roles"].items():
            if role in ORDER:
                named |= v3.values_named("tipo_procedimento", ctx["allowed"][pid])
        if named:
            raise Gap(f"limiar without the procedure the text names ({sorted(named)})")
        return {"regras": [], "nao_tipavel": {"motivo": "nao_e_limiar", "fontes": [{"texto": alvo_text.split(";")[0].split(". ")[0][:300].strip(), "de": ctx["alvo"]}],
                                              "falta": "o valor não é o limite até ao qual um procedimento pode ser escolhido"}}
    rules = []
    for r in ex["regras"]:
        conds = sorted((canon_condition(c) for c in r["condicoes"]), key=lambda c: json.dumps(c, sort_keys=True, ensure_ascii=False))
        rules.append({"tipo": rtype, "condicoes": conds, "params": dict(r["params"])})
    for i, r in enumerate(rules):
        for c in r["condicoes"]:
            spec = VOC["condition_fields"].get(c["field"])
            if spec is None:
                raise Gap(f"{c['field']}: not in the v3 vocabulary")
            if spec["kind"] == "enum":
                vals = c["value"] if isinstance(c["value"], list) else [c["value"]]
                c["fontes"] = enum_quotes(c["field"], vals, ctx, ("vizinho",) if rest and c["op"] in ("ne", "not_in") else ())
            elif spec["kind"] == "boolean":
                c["fontes"] = bool_quotes(c["field"], c["value"], ctx)
            elif spec["kind"] == "amount":
                c["fontes"] = amount_condition_quotes(c["field"], c["op"], c["value"], ctx)
            elif spec["kind"] == "date":
                q = first(ctx, ORDER, lambda t: (lambda x: x and x.span())(re.search(r"(?:a partir de |até |antes de |depois de )?\d{1,2} de \w+ de \d{4}|\d{4}-\d{2}-\d{2}", t)))
                if q is None:
                    raise Gap(f"{c['field']}: the text fixes no date")
                c["fontes"] = q
            else:
                raise Gap(f"{c['field']}: the code finds no quotes for a {spec['kind']} yet")
        if rtype == "prazo_minimo":
            p = r["params"]
            p.setdefault("usual_days", None)
            r["params"] = {"minimum_days": p["minimum_days"], "deadline_field": p["deadline_field"], "counted_from": p["counted_from"], "usual_days": p.get("usual_days")}
            r["fontes"] = prazo_quotes(r["params"], ctx)
        else:
            th = dict(r["params"]["threshold"])
            q, comparator, field = limiar_quotes(th, ctx)
            if comparator != th["comparator"]:
                raise Gap(f"comparator {th['comparator']}: the text says {comparator}")
            th["field"] = field
            r["params"] = {"threshold": th}
            r["fontes"] = q
        r["condicoes"] = [{"field": c["field"], "op": c["op"], "value": c["value"], "fontes": c["fontes"]} for c in r["condicoes"]]
        r["fontes"] = {k: r["fontes"][k] for k in (("minimum_days", "deadline_field", "counted_from", "usual_days") if rtype == "prazo_minimo" else ("field", "comparator", "value"))}
        rules[i] = {"tipo": r["tipo"], "condicoes": r["condicoes"], "params": r["params"], "fontes": r["fontes"]}
    return {"regras": rules, "nao_tipavel": None}


def row(ex, ctx, answer, version=PROTOCOL):
    return {"id": f"{TASK}:{ex['id']}", "task": TASK, "prompt": v3.render(ctx, ex["tipo"], version), "schema": v3.schema(ctx, ex["tipo"]),
            "answer": json.dumps(answer, ensure_ascii=False, separators=(",", ":")), "sources": [], "estilo": ex.get("estilo")}


def problems(ex, version=PROTOCOL):
    """(answer, []) when the article renders and its gold, quoted by code, passes the factory's checker; (None, [why]) otherwise."""
    try:
        if ex["tipo"] not in ("prazo_minimo", "limiar"):
            return None, [f"tipo {ex['tipo']}"]
        if ex["alvo"] not in {""} | {x["n"] for x in ex["numeros"]}:
            return None, [f"alvo {ex['alvo']!r} is not a path"]
        ctx = ctx_of(ex)
        answer = derive(ex, ctx)
    except Gap as exc:
        return None, [f"gold: {exc}"]
    except (KeyError, TypeError, AttributeError, IndexError, ValueError) as exc:
        return None, [f"malformed: {exc!r}"[:200]]
    errs = v3.check(answer, ctx, ex["tipo"], version)
    return (answer, ctx), [f"checker: {e}" for e in errs]


# ---- sets ----------------------------------------------------------------------------------------------------------------
def load(pattern):
    rows = []
    for f in sorted(m.WRITTEN.glob(pattern)):
        rows += [json.loads(line) for line in f.read_text(encoding="utf-8").splitlines() if line.strip()]
    return rows


def alvo_text(ex):
    return next((x["texto"] for x in ex["numeros"] if x["n"] == ex["alvo"]), ex.get("texto", ""))


def close(a, refs):
    for x in refs:
        if abs(len(x) - len(a)) < 0.5 * len(a):
            sm = difflib.SequenceMatcher(None, a, x)
            if sm.real_quick_ratio() >= LEAK and sm.quick_ratio() >= LEAK and sm.ratio() >= LEAK:
                return True
    return False


def split_of(ex_id):
    return "sealed" if int(hashlib.sha256(ex_id.encode("utf-8")).hexdigest(), 16) % 2 else "dev"


def build(store=None, only=None):
    """{set: [(ex, row)]}, {id: why left out}."""
    real = m.reference_texts(store)
    sets, rejected = {"train": [], "dev_antigo": [], "dev": [], "sealed": []}, {}
    evals = [ex for ex in load("eval3-*.jsonl")]
    eval_texts, kept_alvos = [], []
    for ex in sorted(evals, key=lambda e: e["id"]):
        if only and not ex["id"].startswith(only):
            continue
        t = alvo_text(ex)
        if close(t, real):
            rejected[ex["id"]] = "close to a real passage"; continue
        if close(t, kept_alvos):
            rejected[ex["id"]] = "close to an earlier eval3 article"; continue
        res, errs = problems(ex)
        if errs:
            rejected[ex["id"]] = errs[0]; continue
        kept_alvos.append(t)
        eval_texts.append(t)
        sets[split_of(ex["id"])].append((ex, row(ex, res[1], res[0])))
    for pattern, where in SOURCES:
        if where == "eval3":
            continue
        for ex in load(pattern):
            if only and not ex["id"].startswith(only):
                continue
            if pattern.startswith("v3") and (close(alvo_text(ex), real) or close(alvo_text(ex), eval_texts)):
                rejected[ex["id"]] = "close to a real passage or an eval3 article"; continue
            res, errs = problems(ex)
            if errs:
                rejected[ex["id"]] = errs[0]; continue
            sets[where].append((ex, row(ex, res[1], res[0])))
    return sets, rejected


def dump(rows):
    return "".join(json.dumps(r, ensure_ascii=False, sort_keys=True) + "\n" for r in rows).encode("utf-8")


def generate(store=None, held_doc=None):
    sets, rejected = build(store)
    files = {"regra_lida/train.jsonl": dump(r for _, r in sorted(sets["train"], key=lambda x: x[1]["id"])),
             "regra_lida_alvo/train.jsonl": b"",
             "regra_lida/dev_antigo.jsonl": dump(r for _, r in sorted(sets["dev_antigo"], key=lambda x: x[1]["id"])),
             "regra_lida/dev.jsonl": dump(r for _, r in sorted(sets["dev"], key=lambda x: x[1]["id"])),
             "regra_lida/sealed.jsonl": dump(r for _, r in sorted(sets["sealed"], key=lambda x: x[1]["id"])),
             "REJECTED.json": (json.dumps(rejected, ensure_ascii=False, indent=1, sort_keys=True) + "\n").encode("utf-8")}
    index = {"tool": VERSION, "protocol": PROTOCOL, "date": DATE, "files": {k: {"rows": v.count(b"\n"), "sha256": hashlib.sha256(v).hexdigest()} for k, v in sorted(files.items())},
             "rejected": len(rejected), "note": "D66: the written articles rendered by the factory's own v3 code, quotes derived by code, every gold checked"}
    files["INDEX.json"] = (json.dumps(index, ensure_ascii=False, indent=1, sort_keys=True) + "\n").encode("utf-8")
    return files


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("cmd", choices=["check", "generate"]); ap.add_argument("--only")
    a = ap.parse_args()
    if a.cmd == "check":
        sets, rejected = build(only=a.only)
        for k, v in sets.items():
            print(f"{k}: {len(v)}")
        from collections import Counter
        kinds = Counter(re.sub(r"\d+|\[.*?\]|«.*?»", "…", w)[:90] for w in rejected.values())
        for k, n in kinds.most_common(25):
            print(f"  {n:4} {k}")
        for i, (eid, why) in enumerate(sorted(rejected.items())):
            if a.only or i < 40:
                print(f"{eid}: {why}")
        return
    files = generate()
    for rel, b in files.items():
        f = DATA / rel
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_bytes(b)
    print(json.loads(files["INDEX.json"])["files"])


if __name__ == "__main__":
    main()
