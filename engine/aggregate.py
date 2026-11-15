"""The sums an agregada rule compares (DECISIONS D96), from the contracts BASE published, each one named.

    contracts_of(records) -> Index
    group_sums(rule, index, procedure_base_id, adjudicante, anchor) -> {rule_id-ready dict} for evaluate's `aggregates`

A record is one BASE contract as ccp.base_contrato holds it (db/aggregates.py reads it), reduced to:
    {"id": idcontrato, "raw", "proc": idprocedimento, "adjudicante": [NIF...], "adjudicatarios": [NIF...], "preco": number|None,
     "fund": the declared fundamentação (text), "fundp": its passage ids (db/fundamento.passages; «?:…» for an act
     the reader cannot name), "dadj": data da decisão de adjudicação, "dcel": data de celebração,
     "dpub": data de publicação}
Nothing here reads the law: the rule says which declared bases count (params.counts.fundamento_em, passage ids, read
by the readers), the window (params.window, in economic years: the calendar year, the current one and length-1
before it), the group (params.group_key: adjudicante and adjudicatário) and the field summed (preço contratual).

What the anchor is. The rule speaks of what the entity «já tenha adjudicado» when it invites: the anchor is the date
of the invitation. No source dates it; db/run_engine.py evaluates on every date the procedure can have started
(D82) and gives a verdict only when every date gives the same one.

Certainty, contract by contract. A contract counts surely when: it is not of this procedure; its adjudicante is this
one alone; its adjudicatário is this one alone; its declared basis names a counted passage and no other; its
adjudication is dated before the anchor and inside the window (when the decision is not dated, the signing or the
publication bounds it from above: before the anchor if they are, and in the window only if the decision is dated).
It may count when one of these is unknown (a consortium, no NIF, no declared basis, no date, no price). sum_min adds
the sure ones, sum_max the sure and the maybe ones (a maybe without a price makes sum_max infinite). The rule's
comparator decides on both (engine/rules.aggregate_result): «não cumpre» only on what surely counts.
"""
import datetime
import math


BASE_URL = "https://www.base.gov.pt/Base4/pt/detalhe/?type=contratos&id="


def _date(v):
    s = str(v or "")[:10]
    try:
        if len(s) == 10 and s[2] == "/" and s[5] == "/":  # dd/mm/aaaa (the older dumps)
            return datetime.date(int(s[6:]), int(s[3:5]), int(s[:2]))
        return datetime.date.fromisoformat(s)
    except ValueError:
        return None


class Index:
    """BASE contract records by adjudicante NIF, and by procedure id."""

    def __init__(self, records):
        self.by_adjudicante, self.by_proc = {}, {}
        for r in records:
            for a in set(r.get("adjudicante") or []):
                if a:
                    self.by_adjudicante.setdefault(a, []).append(r)
            if r.get("proc"):
                self.by_proc.setdefault(str(r["proc"]), []).append(r)


def contracts_of(records):
    return Index(records)


def _basis(rec, counted):
    """(True, ids) when the declared basis names a counted passage and no other; (False, ids) when it names none of
    them; (None, ids) when it names one with others, or is not declared."""
    ids = list(rec.get("fundp") or [])
    if not rec.get("fund") or not ids:
        return None, ids
    if any(p.startswith("?:") for p in ids):  # words that name no article: the basis is not known
        return None, ids
    hit = [p for p in ids if p in counted]
    if not hit:
        return False, ids
    return (True if len(hit) == len(ids) else None), ids


def _shown(rec, why=None):
    d = _date(rec.get("dadj")) or None
    out = {"id": str(rec["id"]), "registo": rec.get("raw") or f"raw:base-contratos:contrato:{rec['id']}", "url": BASE_URL + str(rec["id"]),
           "procedimento": rec.get("proc"), "data_adjudicacao": d and d.isoformat(),
           "data_celebracao": (_date(rec.get("dcel")) or None) and _date(rec.get("dcel")).isoformat(),
           "preco_contratual": rec.get("preco"), "fundamento": rec.get("fund")}
    if why:
        out["porque_incerto"] = why
    return out


def classify(rec, supplier, adjudicante, anchor, start, counted):
    """("sure" | "maybe" | None, why) for one record of the adjudicante, about the pair (adjudicante, supplier)."""
    adjs = [a for a in (rec.get("adjudicante") or []) if a]
    sup = [s for s in (rec.get("adjudicatarios") or [])]
    basis, _ = _basis(rec, counted)
    if basis is False:
        return None, None
    dadj = _date(rec.get("dadj"))
    bound = min([d for d in (_date(rec.get("dcel")), _date(rec.get("dpub"))) if d], default=None)
    if dadj:
        if not (start <= dadj < anchor):
            return None, None
        when_sure = True
    else:
        if bound is not None and bound < start:
            return None, None  # adjudicated before the signing or publication, which is already before the window
        when_sure = False
    why = []
    if supplier not in sup:
        if all(s and s != "-" for s in sup) and sup:
            return None, None
        why.append("adjudicatário sem NIF")
    elif len(set(sup)) > 1:
        why.append("vários adjudicatários")
    if len(set(adjs)) > 1:
        why.append("várias entidades adjudicantes")
    if basis is None:
        why.append("fundamento não declarado ou com outras passagens" if rec.get("fund") else "fundamento não declarado")
    if not when_sure:
        if bound is not None and bound < anchor:
            why.append("decisão de adjudicação não datada (assinado ou publicado antes; pode ser anterior à janela)")
        else:
            why.append("decisão de adjudicação não datada")
    if not isinstance(rec.get("preco"), (int, float)):
        why.append("sem preço contratual")
    return ("maybe", "; ".join(why)) if why else ("sure", None)


def group_sums(rule, index, proc_id, adjudicante, anchor):
    """For the rule's group (adjudicante, each adjudicatário of this procedure) at the anchor date (ISO): the dict
    evaluate reads as aggregates[rule id]. Several adjudicatários: the one that decides «não cumpre» (highest sum_min)
    when any does; otherwise the one with the highest sum_max."""
    p = rule["params"]
    w = p["window"]
    if w["unit"] != "anos_economicos":
        return {"why": ("regra_ausente", f"window unit {w['unit']} is not computed from BASE (D96)")}
    a = _date(anchor)
    start = datetime.date(a.year - (w["length"] - 1), 1, 1)
    counted = set(p["counts"]["fundamento_em"])
    mine = index.by_proc.get(str(proc_id), [])
    suppliers = sorted({s for r in mine for s in (r.get("adjudicatarios") or []) if s and s != "-"})
    if not adjudicante:
        return {"why": ("facto_ausente", "adjudicante")}
    if not suppliers:
        return {"why": ("facto_ausente", "o adjudicatário deste procedimento (com NIF) não está no registo BASE dos seus contratos")}
    own = {str(r["id"]) for r in mine}
    groups = []
    for s in suppliers:
        sure, maybe = [], []
        for rec in index.by_adjudicante.get(adjudicante, []):
            if str(rec["id"]) in own or str(rec.get("proc")) == str(proc_id):
                continue
            k, why = classify(rec, s, adjudicante, a, start, counted)
            if k == "sure":
                sure.append(_shown(rec))
            elif k == "maybe":
                maybe.append(_shown(rec, why))
        lo = round(sum(x["preco_contratual"] for x in sure), 2)
        hi = math.inf if any(not isinstance(x["preco_contratual"], (int, float)) for x in maybe) else round(lo + sum(x["preco_contratual"] for x in maybe), 2)
        groups.append({"group": {"adjudicante": adjudicante, "adjudicatario": s}, "sum_min": lo, "sum_max": hi,
                       "sure": sorted(sure, key=lambda x: (x["data_adjudicacao"] or x["data_celebracao"] or "", x["id"])),
                       "maybe": sorted(maybe, key=lambda x: (x["data_celebracao"] or "", x["id"]))})
    from engine.rules import aggregate_result
    res = {g["group"]["adjudicatario"]: aggregate_result(p, g) for g in groups}
    bad = [g for g in groups if res[g["group"]["adjudicatario"]] == "nao_cumpre"]
    pick = max(bad, key=lambda g: g["sum_min"]) if bad else max(groups, key=lambda g: (g["sum_max"], g["sum_min"]))
    return {**pick, "window": [start.isoformat(), a.isoformat()], "anchor": a.isoformat(),
            "window_text": f"adjudicações de {start.isoformat()} até antes de {a.isoformat()} (ano económico em curso e {w['length'] - 1} anteriores)"
                           + (f"; {len(groups)} adjudicatários neste procedimento" if len(groups) > 1 else "")}
