"""The deterministic engine: evaluate(unit, rules, facts, known_at, valid_at) -> verdicts, each with a typed reason and a
complete manifest. Nothing here interprets text; nothing here calls a model.

    evaluate(unit, rules, facts, known_at, valid_at, *, manifest, conflicts=(), assertions=(), entities=(),
             documents=(), coverage=None, aggregates=None, engine_version=VERSION) -> list[dict]

Inputs
    unit        the unidade object evaluated (proc, lote, contrato, mod)
    rules       regra objects (any state; the caller decides which package); unknown types are refused
    facts       facto objects of the unit and its ancestors (the caller gathers them; see Store.facts_of in A4)
    known_at    the instant of evaluation (UTC): only facts with known_at <= known_at are read; it becomes the verdicts' known_at
    valid_at    the date the facts are read at: the latest fact per field with valid_at <= valid_at wins
    manifest    a complete manifest (engine/manifest.build): law version, package, adapters, snapshots, code, log head
    conflicts   conflito objects: a field in an unresolved conflict reads as Conflict -> nao_avaliado / conflito
    assertions  afirmacao objects of the unit: compared beside each verdict whose rule cites one of their passages
    entities    entidade objects involved: listed on each verdict without the name of a pessoa_singular (invariant 11)
    documents   documento objects of the unit (for conteudo_obrigatorio)
    coverage    {(adapter_id, "YYYY-MM"): ratio | None} measured source coverage, for aggregate rules
    aggregates  {rule_id: number} precomputed aggregate values over the group (the window query is B4's; absent -> facto_ausente)

Order (ARQUITECTURA.md §4 layer 6): 1 seletor_regime fixes the regime from the fact it selects by; without that fact every
other rule is nao_avaliado / facto_ausente. 2 jurisdicao rules whose predicate holds adjust thresholds. 3 simple rules
(limiar, procedimento_admissivel, prazo_minimo, prazo_maximo, conteudo_obrigatorio, proibicao); among prazo_minimo, prazo_maximo or limiar rules of one
field that apply, the most specific gives the verdict (D66). 4 agregada: completeness first (below
the product threshold -> cobertura_insuficiente), then the aggregate.
A rule whose conditions do not hold yields no verdict (it does not apply); a rule whose conditions cannot be read yields
nao_avaliado with the missing or conflicted field in detail. A rule outside its validity at the regime date is skipped.
Verdict id: veredicto:<rule id>:<unit id>:<known_at> with ':' of the ids replaced by '-'.
"""
from engine import manifest as manifest_mod
from engine.canon import canonical
from engine import rules as rules_mod
from engine.rules import MISSING, Conflict

VERSION = "ccp-engine-0.1"


class EvaluateError(ValueError):
    pass


def _ident(x: str) -> str:
    return x.replace(":", "-")


def read_facts(facts, known_at, valid_at, conflicts=()):
    """Latest value per field among facts known by known_at and valid by valid_at; a conflicted field reads as Conflict.
    Returns ({field: value}, {field: facto id})."""
    chosen, ids = {}, {}
    for f in sorted(facts, key=lambda f: (f["valid_at"], f["known_at"], f["id"])):
        if f["known_at"] <= known_at and f["valid_at"] <= valid_at:
            chosen[f["field"]], ids[f["field"]] = f["value"], f["id"]
    for c in conflicts:
        if c["resolution"]["kind"] == "nao_avaliado":
            chosen[c["field"]] = Conflict(c["id"])
            ids[c["field"]] = None
        else:
            chosen_fact = next((f for f in facts if f["id"] == c["resolution"]["chosen"]), None)
            if chosen_fact:
                chosen[c["field"]], ids[c["field"]] = chosen_fact["value"], chosen_fact["id"]
    return chosen, ids


def _verdict(rule, unit, result, reason, detail, citation, facts_used, assertions, entities, known_at, valid_at, manifest, engine_version):
    cited = {c["passage"] for c in rule["passages"]}
    compared = [{"afirmacao": a["id"], "declared_passages": list(a["passages"]), "agrees": None if result == "nao_avaliado" else (result == "cumpre")}
                for a in assertions if cited & set(a["passages"])]
    ents = [{k: v for k, v in {"id": e["id"], "type": e["type"], "role": role["role"], "name": e.get("name")}.items() if v is not None and not (k == "name" and e["type"] == "pessoa_singular")}
            for e in entities for role in e.get("roles", [])]
    return {"id": f"veredicto:{_ident(rule['id'])}:{_ident(unit['id'])}:{known_at}", "revision": 1, "recorded_at": known_at,
            "rule": {"id": rule["id"], "revision": rule["revision"]}, "unit": unit["id"], "result": result, "reason": reason, "detail": detail,
            "citation": citation, "facts_used": [f for f in dict.fromkeys(facts_used) if f], "assertions_compared": compared, "entities": ents,
            "valid_at": valid_at, "known_at": known_at, "engine_version": engine_version, "manifest": manifest}


# D80: a deadline the facts state as two dates. The days between the rule's own counted_from date and the deadline's
# date are counted by a settled counting rule (counting: {"id": regra id, "first_day_counts": bool}); without one the
# verdict is regra_ausente, never a count the code chose.
DEADLINE_END = {"prazo_propostas_dias": "data_limite_propostas", "prazo_candidaturas_dias": "data_limite_candidaturas"}


def deadline_days(p, values, counting):
    """(days, fields used, None) or (None, fields, (reason, detail)) for a prazo_minimo / prazo_maximo rule's params."""
    field, start, end = p["deadline_field"], p.get("counted_from"), DEADLINE_END.get(p["deadline_field"])
    if values.get(field, MISSING) is not MISSING:
        return values[field], [field], None
    if not end or start in (None, "nao_indicado"):
        return None, [field], ("facto_ausente", f"{p.get('type', 'prazo')} needs {field}")
    for f in (end, start):
        v = values.get(f, MISSING)
        if v is MISSING or isinstance(v, Conflict):
            return None, [field, f], ("conflito" if isinstance(v, Conflict) else "facto_ausente",
                                       f"{field} needs {f}" + (f" (in conflict: {v.conflito_id})" if isinstance(v, Conflict) else ""))
    if counting is None:
        return None, [end, start], ("regra_ausente", f"{field}: the days from {start} to {end} need a settled counting rule")
    import datetime
    try:
        a, b = datetime.date.fromisoformat(values[start][:10]), datetime.date.fromisoformat(values[end][:10])
    except (TypeError, ValueError):
        return None, [end, start], ("facto_ausente", f"{field}: {start} or {end} is not a date")
    return (b - a).days + (1 if counting["first_day_counts"] else 0), [end, start], None


def evaluate(unit, rules, facts, known_at, valid_at, *, manifest, conflicts=(), assertions=(), entities=(), documents=(), coverage=None, aggregates=None,
             counting=None, engine_version=VERSION):
    missing = manifest_mod.is_complete(manifest)
    if missing:
        raise EvaluateError(f"incomplete manifest: {missing}")
    staged = rules_mod.order(rules)
    values, fact_ids = read_facts(facts, known_at, valid_at, conflicts)
    coverage = coverage or {}
    aggregates = aggregates or {}

    def na(rule, reason, detail, used):
        return _verdict(rule, unit, "nao_avaliado", reason, detail, None, used, assertions, entities, known_at, valid_at, manifest, engine_version)

    def done(rule, result, detail, used):
        return _verdict(rule, unit, result, None, detail, dict(rule["passages"][0]), used, assertions, entities, known_at, valid_at, manifest, engine_version)

    def used_for(fields):
        return [fact_ids.get(f) for f in fields if fact_ids.get(f)]

    verdicts = []
    # 1. regime selector
    regime_date = valid_at
    selectors = staged["seletor"]
    if selectors:
        field = selectors[0]["params"]["selects_by"]
        value = values.get(field, MISSING)
        if value is MISSING or isinstance(value, Conflict):
            reason = "conflito" if isinstance(value, Conflict) else "facto_ausente"
            for r in rules:
                if r["type"] != "seletor_regime":
                    verdicts.append(na(r, reason, f"regime selector needs {field}", []))
            return verdicts
        regime_date = value
    applicable = [r for stage in ("jurisdicao", "simples", "agregada") for r in staged[stage] if rules_mod.valid_at(r, regime_date)]

    # 2. jurisdiction effects
    multiplier = 1.0
    for r in [r for r in applicable if r["type"] == "jurisdicao"]:
        ok, _ = rules_mod.applies({"conditions": r["params"]["predicate"]}, values)
        if ok:
            multiplier *= r["params"]["effect"].get("multiply_thresholds_by", 1.0)

    # 3 and 4
    for r in [r for r in applicable if r["type"] != "jurisdicao"]:
        ok, field = rules_mod.applies(r, values)
        cond_fields = [c["field"] for c in r["conditions"]]
        if ok is None:
            verdicts.append(na(r, "conflito" if isinstance(values.get(field), Conflict) else "facto_ausente", f"condition needs {field}", used_for(cond_fields)))
            continue
        if not ok:
            continue
        p, t = r["params"], r["type"]
        if t == "agregada":
            period = valid_at[:7]
            ratios = [coverage.get((a, period)) for a in manifest["adapters"]]
            ratio = min((x for x in ratios if x is not None), default=None)
            threshold = p["completeness_threshold"]["ratio"]
            if ratio is None or ratio < threshold:
                shown = "unknown" if ratio is None else f"{ratio:.2f}"
                verdicts.append(na(r, "cobertura_insuficiente", f"source coverage {period} = {shown} < {threshold:.2f} (product rule {p['completeness_threshold']['decided_by']})", used_for(cond_fields)))
                continue
            if r["id"] not in aggregates:
                verdicts.append(na(r, "facto_ausente", f"aggregate {p['aggregate']['op']}({p['aggregate']['field']}) over {p['group_key']} not available", used_for(cond_fields)))
                continue
            value = aggregates[r["id"]]
            result = "cumpre" if rules_mod.holds({"field": "_agg", "op": p["aggregate"]["comparator"], "value": p["aggregate"]["value"]}, {"_agg": value}) else "nao_cumpre"
            verdicts.append(done(r, result, f"{p['aggregate']['op']}({p['aggregate']['field']})={value} {p['aggregate']['comparator']} {p['aggregate']['value']}", used_for(cond_fields)))
            continue
        if t in ("prazo_minimo", "prazo_maximo"):  # D80: stated as days, or as two dates and a settled counting rule
            days, needed, why = deadline_days({**p, "type": t}, values, counting)
            if why:
                verdicts.append(na(r, why[0], why[1], used_for(cond_fields + needed)))
                continue
            used = used_for(needed + cond_fields)
            if not isinstance(days, (int, float)):
                verdicts.append(na(r, "facto_ausente", f"{p['deadline_field']} is not a number of days", used))
                continue
            how = "" if needed == [p["deadline_field"]] else f" ({needed[1]} to {needed[0]}, counting rule {counting['id']})"
            if t == "prazo_minimo":
                detail = (f"{p['deadline_field']}={days:g} >= {p['minimum_days']}" if days >= p["minimum_days"] else f"{p['deadline_field']}={days:g} < {p['minimum_days']}") + how
                if days >= p["minimum_days"] and p.get("usual_days") and days < p["usual_days"]:  # D62: under the «em regra» days, not under the floor
                    detail += f"; below the usual {p['usual_days']} days the passage sets as a rule"
                verdicts.append(done(r, "cumpre" if days >= p["minimum_days"] else "nao_cumpre", detail, used))
            else:  # D71
                ok2 = days <= p["maximum_days"]
                verdicts.append(done(r, "cumpre" if ok2 else "nao_cumpre", f"{p['deadline_field']}={days:g} {'<=' if ok2 else '>'} {p['maximum_days']}" + how, used))
            continue
        needed = {"limiar": [p["threshold"]["field"]] if "threshold" in p else [], "procedimento_admissivel": ["tipo_procedimento"],
                  "proibicao": [c["field"] for c in p.get("forbidden", [])], "conteudo_obrigatorio": []}[t]
        blocked = next((f for f in needed if values.get(f, MISSING) is MISSING or isinstance(values.get(f), Conflict)), None)
        if blocked is not None:
            v = values.get(blocked, MISSING)
            verdicts.append(na(r, "conflito" if isinstance(v, Conflict) else "facto_ausente", f"{t} needs {blocked}" + (f" (in conflict: {v.conflito_id})" if isinstance(v, Conflict) else ""), used_for(cond_fields + needed)))
            continue
        used = used_for(needed + cond_fields)
        if t == "limiar":
            limit = p["threshold"]["value"] * multiplier
            value = values[p["threshold"]["field"]]
            ok2 = rules_mod.holds({"field": "_v", "op": p["threshold"]["comparator"], "value": limit}, {"_v": value})  # D66: lt, le, gt, ge
            verdicts.append(done(r, "cumpre" if ok2 else "nao_cumpre", f"{p['threshold']['field']}={value} {p['threshold']['comparator']} {limit:g}", used))
        elif t == "procedimento_admissivel":
            proc = values["tipo_procedimento"]
            verdicts.append(done(r, "cumpre" if proc in p["procedures"] else "nao_cumpre", f"tipo_procedimento={proc} in {p['procedures']}", used))
        elif t == "proibicao":
            all_hold = all(rules_mod.holds(c, values) for c in p["forbidden"])
            verdicts.append(done(r, "nao_cumpre" if all_hold else "cumpre", "forbidden conditions " + ("hold" if all_hold else "do not all hold"), used))
        elif t == "conteudo_obrigatorio":
            docs = [d for d in documents if d["origin"]["piece"] == p["document_piece"] and d["origin"]["unit"] == unit["id"]]
            if not docs:
                verdicts.append(na(r, "facto_ausente", f"no {p['document_piece']} document for {unit['id']}", used))
                continue
            if not any(d["has_text_layer"] for d in docs):
                verdicts.append(na(r, "documento_sem_texto", f"{p['document_piece']} has no text layer", used))
                continue
            present = [e for e in p["required_elements"] if values.get(e, MISSING) is not MISSING]
            if len(present) < len(p["required_elements"]):
                verdicts.append(na(r, "facto_ausente", f"elements not extracted: {sorted(set(p['required_elements']) - set(present))}", used))
                continue
            verdicts.append(done(r, "cumpre", f"elements present: {present}", used + used_for(present)))
    return most_specific(applicable, verdicts, na)


def most_specific(applicable, verdicts, na):
    """D66 (product_rule:regra-mais-especifica): among the prazo_minimo or limiar rules of one deadline or threshold field
    that apply, the one whose conditions contain every other's gives the verdict and the others give none; when no applying
    rule contains the others and their results differ, each is nao_avaliado / conflito."""
    by_rule = {v["rule"]["id"]: v for v in verdicts}
    groups = {}
    for r in applicable:
        v = by_rule.get(r["id"])
        if v is None or v["result"] == "nao_avaliado" or r["type"] not in ("prazo_minimo", "prazo_maximo", "limiar"):
            continue
        key = (r["type"], r["params"]["deadline_field"] if r["type"] in ("prazo_minimo", "prazo_maximo") else r["params"]["threshold"]["field"])
        groups.setdefault(key, []).append(r)
    drop, conflict = set(), {}
    for rs in groups.values():
        conds = {r["id"]: {canonical(c) for c in r["conditions"]} for r in rs}
        top = [r for r in rs if not any(conds[r["id"]] < conds[o["id"]] for o in rs if o["id"] != r["id"])]
        drop |= {r["id"] for r in rs} - {r["id"] for r in top}
        if len(top) > 1 and len({by_rule[r["id"]]["result"] for r in top}) > 1:
            names = ", ".join(sorted(r["id"] for r in top))
            for r in top:
                conflict[r["id"]] = na(r, "conflito", f"{names} apply and none contains the others' conditions (product_rule:regra-mais-especifica)",
                                       by_rule[r["id"]]["facts_used"])
    return [conflict.get(v["rule"]["id"], v) for v in verdicts if v["rule"]["id"] not in drop]
