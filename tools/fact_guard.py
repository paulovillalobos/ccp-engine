"""The guard (DECISIONS D53): code checks a reader's answer to a person's question against the question's own text before
the engine reads it. No model. It never adds a fact the text does not carry; it settles what code can read exactly.

    from fact_guard import guard;  guard(question, today, answer_dict) -> answer_dict
    .venv/bin/python tools/fact_guard.py --in FILE --gold GOLD --out FILE   guard every answer of a reader's JSONL

territorio   from law/gazetteer/municipios.json (308 municipalities, INE/CAOP via GeoAPI.pt), the islands and the
             regions' names. One region found -> that fact; several, or a name in two regions (Calheta, Lagoa, Santa
             Cruz, São Vicente, Madalena) -> ambiguos; none -> the reader's territorio is dropped (not in the text).
             Names that are also common words (Porto, Horta, Velas, Corvo, Pico, Flores, Terceira, Madeira…) count only
             written with a capital or after «ilha»/«região».
preco_base   a fact only with «preço base» / «PB» in the text, and not with «IVA», «valor», «orçamento», «entre»,
             «cada», «por ano»: otherwise the reader's amount goes to ambiguos (never converted, never dropped); a
             single candidate the text does call preço base, with none of those words, becomes the fact.
citacoes     read by code: «art.º 20.º, n.º 1, al. d)» -> ccp:art20.1.d (the store decides between art20.d and
             art20.1.d), «art. 17.º-B» -> ccp:art17-b, «DL 177/2026», «decreto-lei 177 de 2026» -> dl-177-2026,
             «Lei 30/2021» -> lei-30-2021, «DLR 27/2015/A» -> dlr-27-2015-a; only ids present in law/.
data_inicio  a date the text does not carry (no digit date, month, «hoje», «amanhã», «ontem», weekday) is dropped; a
             date said only with a launch or notice verb («lançámos», «abre», «o anúncio sai») goes to ambiguos.
"""
import argparse
import json
import re
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
VERSION = "ccp-fact-guard-0.2"
GAZ = json.loads((ROOT / "law/gazetteer/municipios.json").read_text(encoding="utf-8"))["municipios"]
FREG = json.loads((ROOT / "law/gazetteer/freguesias.json").read_text(encoding="utf-8"))["freguesias"]
TWO_REGIONS = {"calheta": ["PT-MA", "PT-AC"], "lagoa": ["PT", "PT-AC"], "santa cruz": ["PT-MA", "PT"], "sao vicente": ["PT-MA", "PT"],
               "madalena": ["PT-AC", "PT"], "vila franca": ["PT", "PT-AC"]}
SHORT_NAMES = {"angra": "PT-AC", "gaia": "PT", "vila franca de xira": "PT", "vila franca do campo": "PT-AC", "praia": None}
COMMON_WORDS = {"porto", "horta", "velas", "corvo", "nordeste", "santana", "lagos", "batalha", "moura", "mira", "feira", "madalena", "angra"}
ISLANDS = {"sao miguel": "PT-AC", "terceira": "PT-AC", "faial": "PT-AC", "pico": "PT-AC", "sao jorge": "PT-AC", "graciosa": "PT-AC",
           "flores": "PT-AC", "santa maria": "PT-AC", "corvo": "PT-AC", "porto santo": "PT-MA"}
ISLAND_WORDS = {"terceira", "pico", "flores", "santa maria", "corvo"}
REGIONS = [(r"\ba[cç]ores\b", "PT-AC"), (r"\b(na|da|regi[aã]o aut[oó]noma da) madeira\b", "PT-MA"),
           (r"\b(alentejo|algarve|minho|tr[aá]s-os-montes|beira (alta|baixa|interior|litoral)|continente|[nd]o interior|distrito d[eo])\b", "PT")]
LOOSE = re.compile(r"\b(com|c/)\s*iva\b|\biva inclu[ií]do|\bincluindo (o )?iva|\b(or[cç]amento|entre|cada|por ano|por lote|por item|por unidade|cabimento)\b|/ano|\bou\s+\d", re.I)
HINT = [(r"madeira|porto santo|funchal", "PT-MA"), (r"algarve|continente", "PT"), (r"a[cç]ores|s[aã]o miguel|s[aã]o jorge|terceira|faial|pico|flores|graciosa", "PT-AC")]
OWNER = r"(c[aâ]mara( municipal)?|munic[ií]pio|concelho|freguesia|autarquia)\s+d[aeo]s?\s+$"  # «câmara do porto»: a name, even lowercase


def fold(s):
    return "".join(c for c in unicodedata.normalize("NFD", s.lower()) if unicodedata.category(c) != "Mn")


def _names():
    out = {}
    for name, reg in GAZ.items():
        out.setdefault(fold(re.sub(r"\s*\(.*\)", "", name)), set()).add(reg)
    for name, reg in SHORT_NAMES.items():
        if reg:
            out.setdefault(name, set()).add(reg)
    for name in TWO_REGIONS:
        out.setdefault(name, set()).update(TWO_REGIONS[name])
    return out


NAMES = _names()
LONGEST = sorted(NAMES, key=len, reverse=True)
PARISHES = {fold(k): set(v) for k, v in FREG.items()}


def places(text):
    """({region} the text names, {regions} of a name found in more than one region with no hint)."""
    f, found, two, taken = fold(text), set(), set(), []
    first_two = None  # where the first name in two regions is, so only a region named before it can settle it

    def free(a, b):
        return not any(x < b and a < y for x, y in taken)

    for m in re.finditer(r"freguesia\s+d[aeo]s?\s+([a-z][a-z\s-]{1,40}?)(?=[,.;:)!?]|\s+(e|que|quer|vai|pode|em|no|na|para)\b|$)", f):
        name = m.group(1).strip()
        while name and name not in PARISHES and " " in name:
            name = name.rsplit(" ", 1)[0]
        if name in PARISHES and name not in NAMES:
            taken.append((m.start(1), m.start(1) + len(name)))
            regs = PARISHES[name]
            (found if len(regs) == 1 else two).update(regs)
    for key in LONGEST:
        for m in re.finditer(rf"(?<![\w-]){re.escape(key)}(?![\w-])", f):
            if not free(m.start(), m.end()):
                continue
            if key in COMMON_WORDS and not (text[m.start()].isupper() or re.search(OWNER, f[max(0, m.start() - 30):m.start()])):
                continue
            taken.append((m.start(), m.end()))
            if key in TWO_REGIONS:
                after = f[m.end():m.end() + 25]
                hint = next((reg for pat, reg in HINT if re.match(rf"\s*[(,]?\s*(d[aoe]s?\s+)?(ilha d[aeo]s?\s+)?({pat})", after)), None)
                if hint:
                    found.add(hint)
                else:
                    two.update(TWO_REGIONS[key])
                    first_two = m.start() if first_two is None else min(first_two, m.start())
            else:
                found |= NAMES[key]
    for key, reg in ISLANDS.items():
        for m in re.finditer(rf"(?<![\w-]){re.escape(key)}(?![\w-])", f):
            if not free(m.start(), m.end()):
                continue
            if key in ISLAND_WORDS and not (text[m.start()].isupper() or re.search(r"ilha d[aeo]s? $", f[max(0, m.start() - 10):m.start()])):
                continue
            found.add(reg)
    before = set()
    for pat, reg in REGIONS:
        for m in re.finditer(pat, f):
            found.add(reg)
            if first_two is not None and m.start() < first_two:
                before.add(reg)
    if two and len(before) == 1 and before <= two and found == before:  # «uma câmara do Algarve, a de Lagoa»: the region named first settles it
        two = set()
    elif two and found and found <= two and not before:  # «Santa Cruz… Madeira ou continente?»: a region asked about settles nothing
        two |= found; found = set()
    return found, two


def citations(text, known):
    out = []
    f = fold(text)
    for m in re.finditer(r"\bart(?:igo|\.|º)?\s*(\d+)\s*\.?\s*º?(?:\s*-\s*([a-z]))?(?:\s*,?\s*n\.?\s*º?\s*(\d+))?(?:\s*,?\s*(?:al[ií]nea|al\.)\s*([a-z])\))?", f):
        n, letter, num, al = m.groups()
        base = f"ccp:art{n}" + (f"-{letter}" if letter else "")
        cands = [base + (f".{num}" if num else "") + (f".{al}" if al else "")]
        if al and not num:
            cands.append(f"{base}.1.{al}")
        hit = next((c for c in cands if c in known), base if base in known else None)
        if hit and hit not in out:
            out.append(hit)
    acts = [(r"\b(?:dl|decreto[- ]lei)\s*(?:n\.?\s*º?\s*)?(\d+)(?:-([a-z]))?\s*(?:/|de)\s*(\d{4})", "dl"),
            (r"\blei\s*(?:n\.?\s*º?\s*)?(\d+)/(\d{4})", "lei"),
            (r"\b(?:dlr|decreto legislativo regional)\s*(?:n\.?\s*º?\s*)?(\d+)/(\d{4})/([am])\b", "dlr")]
    for pat, kind in acts:
        for m in re.finditer(pat, f):
            g = m.groups()
            i = {"dl": lambda: f"dl-{g[0]}" + (f"-{g[1]}" if g[1] else "") + f"-{g[2]}", "lei": lambda: f"lei-{g[0]}-{g[1]}",
                 "dlr": lambda: f"dlr-{g[0]}-{g[1]}-{g[2]}"}[kind]()
            if i in known and i not in out:
                out.append(i)
    return out


DATE_CUE = re.compile(r"\d{1,2}\s*[/.-]\s*\d{1,2}|\d{4}-\d{2}-\d{2}|\b(janeiro|fevereiro|marco|abril|maio|junho|julho|agosto|setembro|outubro|novembro|dezembro|hoje|amanha|ontem|"
                      r"segunda|terca|quarta|quinta|sexta|sabado|domingo|dia \d+)\b")
START_CUE = re.compile(r"procedimento\s+(come[cç]|inici|tem in[ií]cio|arranc)|decis[aã]o (de )?contratar|in[ií]cio( do procedimento)?\s*[:=]?|come[cç]a|inicia", re.I)
LAUNCH_CUE = re.compile(r"lan[cç]|\babr[ei]|abriu|an[uú]ncio|arranca|public", re.I)


def guard(question, today, a, known):
    a = {"factos": dict(a.get("factos") or {}), "ambiguos": {k: v for k, v in (a.get("ambiguos") or {}).items() if v is not None},
         "contraditorios": {k: v for k, v in (a.get("contraditorios") or {}).items() if v is not None}, "citacoes": list(a.get("citacoes") or [])}
    a["factos"] = {k: v for k, v in a["factos"].items() if v is not None}
    F, A = a["factos"], a["ambiguos"]
    found, two = places(question)
    if "territorio" not in a["contraditorios"]:
        said = F.pop("territorio", None)
        doubt = A.pop("territorio", None)
        if doubt and not said and set(doubt) <= (found | two) and (found | two):
            A["territorio"] = sorted(set(doubt))  # the reader's own doubt, which the text allows, stays
        elif said and (said in found or (said in two and not found)):
            if said in found and not (two - found):
                F["territorio"] = said
            else:
                A["territorio"] = sorted(found | two)
        elif len(found) == 1 and not two:
            F["territorio"] = next(iter(found))
        elif found | two:
            A["territorio"] = sorted(found | two)
    has_pb = (re.search(r"(pre[cç]o[- ]?base|\bpb\b)[^?!\n]{0,40}?(\d|\bmil\b|milh|cento|duzentos|trezentos|quinhentos)", question, re.I)  # the amount after the words
              or re.search(r"(\d|\bmil\b|milh[oõ]es|milh[aã]o|\bmeio\b|euros?|€|\bk\b|m€)\s*,?\s*(de\s+)?(pre[cç]o[- ]?base|pb)\b", question, re.I))  # or before them
    loose = has_pb and LOOSE.search(question[max(0, has_pb.start() - 20):has_pb.end() + 30])
    if "preco_base" in F and (not has_pb or loose):
        A["preco_base"] = [F.pop("preco_base")]
    elif "preco_base" in A and has_pb and not loose and not re.search(r"n[aã]o sei|ou ser[aá]|n[aã]o tenho a certeza", question, re.I) and len(A["preco_base"]) == 1 and isinstance(A["preco_base"][0], (int, float)):
        F["preco_base"] = A.pop("preco_base")[0]
    a["citacoes"] = sorted(set(citations(question, known)) | {c for c in a["citacoes"] if c in known})
    if "data_inicio_procedimento" in F:
        f = fold(question)
        if not DATE_CUE.search(f):
            F.pop("data_inicio_procedimento")
        elif not START_CUE.search(question) and LAUNCH_CUE.search(question):
            A["data_inicio_procedimento"] = [F.pop("data_inicio_procedimento")]
    order = ["tipo_entidade", "tipo_procedimento", "tipo_contrato", "territorio", "preco_base", "publicado_joue", "data_inicio_procedimento"]
    return {"factos": {k: F[k] for k in order if k in F}, "ambiguos": {k: A[k] for k in order if k in A},
            "contraditorios": {k: a["contraditorios"][k] for k in order if k in a["contraditorios"]}, "citacoes": a["citacoes"]}


def known_ids():
    ids = {p.name.rsplit(".r", 1)[0] for p in (ROOT / "law/passagem").glob("*.json")}
    ids = {i.replace("-art", ":art", 1) if "-art" in i else i for i in ids}
    return ids | {p.name.rsplit(".r", 1)[0].removeprefix("norma-") for p in (ROOT / "law/norma").glob("*.json")}


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--in", dest="inp", required=True); ap.add_argument("--gold", required=True); ap.add_argument("--out", required=True)
    a = ap.parse_args()
    known = known_ids()
    q = {}
    for l in Path(a.gold).read_text(encoding="utf-8").splitlines():
        r = json.loads(l)
        q[r["id"]] = (r["prompt"].split("Pergunta: ", 1)[1], r["prompt"].split("Data de hoje: ", 1)[1][:10])
    lines = []
    for l in Path(a.inp).read_text(encoding="utf-8").splitlines():
        r = json.loads(l)
        try:
            ans = json.loads(r["answer"])
        except json.JSONDecodeError:
            lines.append(l); continue
        g = guard(*q[r["id"]], ans, known)
        text = json.dumps(g, ensure_ascii=False, separators=(",", ":"))
        lines.append(json.dumps({"id": r["id"], "at": r["at"], "source_sha256": r["sha256"], "guard": VERSION, "answer": text}, ensure_ascii=False))
    Path(a.out).write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"{len(lines)} guarded -> {a.out}")


if __name__ == "__main__":
    main()
