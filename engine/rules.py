"""Rules as data: the eight types of ARQUITECTURA.md §5, their required params, evaluation order, packages and diffs.

    RULE_TYPES                      the eight type names, in the order the engine evaluates them within a stage
    REQUIRED_PARAMS[type]           params every rule of that type must carry (mirrors regra.schema.json if/then)
    STAGES                          ("seletor", "jurisdicao", "simples", "agregada"): the evaluation order of §4 layer 6
    stage_of(rule) -> str
    order(rules) -> dict[stage, list[rule]]        rules grouped by stage, each list sorted by id
    applies(rule, facts) -> tuple[bool | None, str | None]
        (True, None) when every condition holds; (False, None) when one fails; (None, field) when a condition needs a
        field that is absent or in conflict — the engine turns that into nao_avaliado, never into False
    fields_of(rule) -> set[str]     every canonical field the rule reads (conditions, params)
    package(id, law_version, rules, log_head, built_at, recorded_at) -> pacote dict (hash per DECISIONS D20)
    diff(pacote_a, pacote_b, regras_by_id) -> {"by_rule": [...], "by_consumer_field": [...]} (DECISIONS D14)
    valid_at(rule, date) -> bool    valid_from <= date < valid_to (law clock)

A rule never carries code. Adding a type is a schema change (schemas/DECISIONS.md) and a row in REQUIRED_PARAMS; the
engine refuses a rule whose type is not here.
"""
from engine.canon import content_hash

VERSION = "ccp-rules-0.1"
RULE_TYPES = ("seletor_regime", "jurisdicao", "limiar", "procedimento_admissivel", "prazo_minimo", "prazo_maximo", "conteudo_obrigatorio", "proibicao", "agregada",
              "contagem_prazo")
REQUIRED_PARAMS = {
    "limiar": ("threshold",),
    "procedimento_admissivel": ("procedures",),
    "prazo_minimo": ("minimum_days", "deadline_field", "counted_from"),
    "prazo_maximo": ("maximum_days", "deadline_field", "counted_from"),  # D71: the same deadline, bounded from above
    "conteudo_obrigatorio": ("required_elements", "document_piece"),
    "proibicao": ("forbidden",),
    "agregada": ("window", "group_key", "aggregate", "completeness_threshold"),
    "seletor_regime": ("selects_by", "regimes"),
    "jurisdicao": ("territory", "predicate", "effect"),
    "contagem_prazo": ("deadline_field", "aspecto", "valor"),  # D83: how a deadline's days are counted; never a verdict of its own
}
STAGES = ("seletor", "jurisdicao", "simples", "agregada", "contagem")
STAGE_OF = {"seletor_regime": "seletor", "jurisdicao": "jurisdicao", "agregada": "agregada", "contagem_prazo": "contagem"}
ASPECTS = ("primeiro_dia", "fins_de_semana", "termo")
MISSING = object()


class RuleError(ValueError):
    pass


def check(rule) -> None:
    """Raise RuleError when the type is unknown or a required param is missing."""
    t = rule.get("type")
    if t not in REQUIRED_PARAMS:
        raise RuleError(f"{rule.get('id')}: unknown rule type {t!r}")
    missing = [p for p in REQUIRED_PARAMS[t] if p not in (rule.get("params") or {})]
    if missing:
        raise RuleError(f"{rule.get('id')}: {t} needs params {missing}")


def stage_of(rule) -> str:
    return STAGE_OF.get(rule["type"], "simples")


def order(rules) -> dict:
    out = {s: [] for s in STAGES}
    for r in rules:
        check(r)
        out[stage_of(r)].append(r)
    for s in STAGES:
        out[s].sort(key=lambda r: (RULE_TYPES.index(r["type"]), r["id"]))
    return out


def valid_at(rule, date: str) -> bool:
    return rule["valid_from"] <= date and (rule["valid_to"] is None or date < rule["valid_to"])


def comparable(x) -> bool:
    """D98: a value an order comparison may read: a finite int or float that is not a bool, or a string (dates)."""
    if isinstance(x, bool):
        return False
    if isinstance(x, (int, float)):
        return x == x and x not in (float("inf"), float("-inf"))
    return isinstance(x, str)


def amount(x) -> bool:
    """D98: a money value or a number of days a limiar or prazo rule may judge: a finite number >= 0 that is not a bool."""
    return isinstance(x, (int, float)) and comparable(x) and x >= 0


def holds(condition, facts) -> "bool | None":
    """facts: {field: value}; a field whose value is MISSING (absent) or a Conflict yields None."""
    value = facts.get(condition["field"], MISSING)
    if value is MISSING or isinstance(value, Conflict):
        return None
    op, ref = condition["op"], condition.get("value")
    if op == "present":
        return True
    if op == "absent":
        return False
    if op in ("in", "not_in") and isinstance(ref, str):
        ref = [ref]  # D98: «in "obras"» is membership in a one-value list, never a substring test ("" and "o" are not "obras")
    if op in ("lt", "le", "gt", "ge") and not (comparable(value) and comparable(ref)):
        return None  # D98: a bool, NaN or infinity is not an amount, a count or a date: the rule cannot read it
    try:
        return {"eq": lambda: value == ref, "ne": lambda: value != ref, "lt": lambda: value < ref, "le": lambda: value <= ref,
                "gt": lambda: value > ref, "ge": lambda: value >= ref, "in": lambda: value in ref, "not_in": lambda: value not in ref}[op]()
    except TypeError:
        return None


def counting_for(field, rules, facts):
    """D83: how the days of `field` are counted, from the contagem_prazo rules in force whose conditions hold: per aspect,
    the rule naming the field beats one for todos, and more conditions beat fewer; two rules of the same weight with
    different values, or an aspect no rule gives, leave the count undecided. Returns (counting, why): counting is
    {"id", "first_day_counts", "continuous", "shift_to_working_day"} or None, why the aspect that blocks it."""
    best = {}
    for r in rules:
        p = r["params"]
        if p["deadline_field"] not in (field, "todos"):
            continue
        ok, _ = applies(r, facts)
        if ok is not True:
            continue
        weight = (p["deadline_field"] == field, len(r.get("conditions", [])))
        cur = best.get(p["aspecto"])
        if cur is None or weight > cur[0]:
            best[p["aspecto"]] = (weight, p["valor"], [r["id"]])
        elif weight == cur[0] and p["valor"] != cur[1]:
            best[p["aspecto"]] = (weight, None, cur[2] + [r["id"]])
        elif weight == cur[0]:
            cur[2].append(r["id"])
    for a in ASPECTS:
        if a not in best:
            return None, f"no settled counting rule gives {a} for {field}"
        if best[a][1] is None:
            return None, f"counting rules disagree on {a} for {field}: {best[a][2]}"
    return {"id": ", ".join(sorted({i for a in ASPECTS for i in best[a][2]})), "first_day_counts": best["primeiro_dia"][1] == "conta",
            "continuous": best["fins_de_semana"][1] == "continuo", "shift_to_working_day": best["termo"][1] == "transfere"}, None


def basis_allows(rule, declared) -> bool:
    """D88 (product_rule:limiar-segundo-fundamento-declarado): a limiar rule judges a procedure whose declared legal basis
    names no passage other than the rule's own (a passage it cites, or one of their parts or wholes), or names none."""
    if not declared:
        return True
    cited = [c["passage"] for c in rule.get("passages", [])]
    def fits(d):
        return any(d == c or c.startswith(d + ".") or d.startswith(c + ".") for c in cited)
    return all(fits(d) for d in declared)


REGIME_FIELD = "regime_declarado"          # D96: the acts the entity declared as the procedure's regime (BASE «regime»)
SECTOR_FIELD = "atividade_setor_especial"  # D96: the activity of the special sectors the buyer declared (BASE, eForms entity-activity)


def regime_blocks(rule, values):
    """D96 (product_rule:regime-especial-declarado): None when a rule of the general regime may judge the procedure;
    otherwise (reason, detail) of the «não avaliado» it gets instead. Two declared facts stop it:
      regime_declarado names acts and not the rule's own («Medidas Especiais de Contratação Pública (Lei n.º 30/2021)»,
      «Decreto-Lei n.º 10-A/2020»): no settled rule of that regime covers the case -> regra_ausente. An act named beside
      the Code («Código dos Contratos Públicos (DL111-B/2017) e Lei n.º 30/2021», BASE's label on 42 % of its contracts)
      leaves the Code's rules to judge, with the declared basis (D88);
      the buyer declared, in the EU's Official Journal under Directive 2014/25/EU, an activity of the special sectors
      (water, energy, transport, postal; db/ted_sectors.py): whether this contract concerns it is the fact
      setores_especiais, which no source gives -> facto_ausente.
    Only limiar and agregada rules (the choice of a procedure by value and the cumulative limit) are stopped by the
    second; every rule of the general regime by the first. A rule whose conditions name setores_especiais decides itself."""
    own = rule.get("norma", "").split(":", 1)[-1]
    declared = values.get(REGIME_FIELD)
    if isinstance(declared, list) and declared and own not in declared:  # a regime of its own, without the rule's act
        return "regra_ausente", (f"a entidade declarou o regime de {', '.join(sorted(declared))}, não o do {own}: nenhuma regra assente desse "
                                 f"regime cobre o caso (product_rule:regime-especial-declarado)")
    activity = values.get(SECTOR_FIELD)
    if (isinstance(activity, str) and activity and rule["type"] in ("limiar", "agregada")
            and not any(c["field"] == "setores_especiais" for c in rule.get("conditions", []))):
        return "facto_ausente", (f"a entidade adjudicante declarou a atividade «{activity}» dos setores especiais: se o contrato lhe diz "
                                 f"respeito, a escolha do procedimento é a desses setores; o facto setores_especiais não está nas fontes "
                                 f"(product_rule:regime-especial-declarado)")
    return None


DOCS_FIELD = "fundamento_nos_documentos"  # D97: what the procedure's own documents state as its basis (check_regime.py)
DOCS_RULE = "product_rule:fundamento-verificado-nos-documentos"


def documents_block(rule, values):
    """D97 (product_rule:fundamento-verificado-nos-documentos), for limiar and agregada rules of a procedure whose
    documents were read: None (judge it; the verdict carries the quote) when they state the rule's own basis or were not
    read; "skip" (no verdict, as D88) when they state another basis; (reason, detail) of a «não avaliado» when they name
    the special measures or state no basis."""
    doc = values.get(DOCS_FIELD)
    if rule["type"] not in ("limiar", "agregada") or not isinstance(doc, dict):
        return None
    where = f"{doc.get('documento')}" + (f", p. {doc.get('pagina')}" if doc.get("pagina") not in (None, "") else "")
    estado = doc.get("estado")
    if estado == "outra_base":
        return "skip"
    if estado == "medidas_especiais":
        return "regra_ausente", (f"os documentos do procedimento dizem que foi adotado ao abrigo das medidas especiais de contratação pública "
                                 f"(«{doc.get('citacao', '')[:200]}», {where}): nenhuma regra assente desse regime cobre o caso ({DOCS_RULE})")
    if estado == "nao_identificado":
        return "facto_ausente", (f"não decidível: fundamento não identificado nos documentos (lidos: {doc.get('lidos', '?')}) ({DOCS_RULE})")
    return None


def aggregate_result(p, agg):
    """D96: an agregada rule on a group's sums. agg: {"sum_min", "sum_max", ...}: sum_min counts only the contracts that
    surely count (dated before the anchor, in the window, with the declared basis the rule counts, this pair alone),
    sum_max every contract that may count. comparator/value say when the rule is complied with (cumpre). Returns
    "cumpre" when even sum_max complies, "nao_cumpre" when even sum_min does not, None when the uncertain contracts decide."""
    ok_min = holds({"field": "_v", "op": p["aggregate"]["comparator"], "value": p["aggregate"]["value"]}, {"_v": agg["sum_min"]})
    ok_max = True if agg["sum_max"] == float("inf") and p["aggregate"]["comparator"] in ("gt", "ge") else \
        False if agg["sum_max"] == float("inf") else \
        holds({"field": "_v", "op": p["aggregate"]["comparator"], "value": p["aggregate"]["value"]}, {"_v": agg["sum_max"]})
    if ok_min is None or ok_max is None:
        return None  # D98: a sum the comparison cannot read decides nothing
    if ok_max:
        return "cumpre"
    if not ok_min:
        return "nao_cumpre"
    return None


class Conflict:
    """Marker for a field whose facts disagree without a precedence rule (conflito.resolution nao_avaliado)."""
    def __init__(self, conflito_id):
        self.conflito_id = conflito_id


def applies(rule, facts) -> tuple:
    """(True, None) when every condition holds; (False, None) when one known fact fails a condition, whatever the others
    lack (D82: a concurso_publico rule does not apply to an ajuste_direto that lacks publicado_joue); else (None, the
    first condition field without a fact)."""
    missing = None
    for c in rule.get("conditions", []):
        h = holds(c, facts)
        if h is None:
            missing = missing or c["field"]
        elif not h:
            return False, None
    return (None, missing) if missing else (True, None)


def fields_of(rule) -> set:
    f = {c["field"] for c in rule.get("conditions", [])}
    p = rule.get("params", {})
    for k in ("threshold", "aggregate"):
        if k in p:
            f.add(p[k]["field"])
    for k in ("deadline_field", "counted_from", "selects_by"):
        if k in p:
            f.add(p[k])
    if "window" in p:
        f.add(p["window"]["anchor"])
    if "counts" in p:  # D96: which earlier contracts the aggregate counts
        f.add("fundamento_passagens")
    for k in ("forbidden", "predicate"):
        for c in p.get(k, []):
            f.add(c["field"])
    f.update(p.get("group_key", []))
    return f


def package(id_, law_version, rules, log_head, built_at, recorded_at, revision=1) -> dict:
    lst = sorted([{"id": r["id"], "revision": r["revision"]} for r in rules], key=lambda x: x["id"])
    return {"id": id_, "revision": revision, "recorded_at": recorded_at, "law_version": law_version, "rules": lst,
            "hash": content_hash(lst), "log_head": log_head, "built_at": built_at}


def diff(pacote_a, pacote_b, regras_by_id) -> dict:
    old = {r["id"]: r["revision"] for r in pacote_a["rules"]}
    new = {r["id"]: r["revision"] for r in pacote_b["rules"]}
    by_rule = []
    for rid in sorted(set(old) | set(new)):
        if rid in old and rid not in new:
            by_rule.append({"rule": rid, "change": "removed", "fields": []})
        elif rid in new and rid not in old:
            by_rule.append({"rule": rid, "change": "added", "fields": []})
        elif old[rid] != new[rid]:
            by_rule.append({"rule": rid, "change": "changed", "fields": []})
    touched = {}
    for ch in by_rule:
        rule = regras_by_id.get(ch["rule"])
        if rule:
            for f in fields_of(rule):
                touched.setdefault(f, set()).add(ch["rule"])
    return {"by_rule": by_rule, "by_consumer_field": [{"field": f, "rules": sorted(rs)} for f, rs in sorted(touched.items())]}
