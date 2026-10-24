"""Verification gate. Exit 0 only when everything stored can be traced to its sources and no invariant is broken.

No model is called; no network module is imported (the gate checks that about itself and the engine: I03, I10).
Run: python -I verify.py            every store below, then every broken overlay must fail with its EXPECT code
     python -I verify.py --store P  one store (a directory or several), report and exit code only

Stores (DECISIONS D3): fixtures/valid (the contract's examples), the repository's own law/ + rules/ + governance/ (the
builder's), data/ (the extractor's). Each is loaded by engine/store.py and checked by every function below.

Check codes (one per invariant of ARQUITECTURA.md §2, plus the structural ones):
  SCHEMA  an object fails the schema of the directory it sits in; a JSON file where none belongs (LAYOUT)
  REF     an id named by an object does not exist in the store (passages, facts, units, raw records, adapters, events...)
  I01     a raw record's bytes hash to something other than its sha256, or the bytes are missing; a derived text is not
          what its versioned extractor produces from the bytes; a passage version's text is not what its offsets select
  I02     a citation's quote is not the passage version's text at its offsets; a DR note's quote is not in its raw text
  I03     a module of engine/, tools/ or verify.py imports a model client or inference library
  I04     the governance replay refuses an event (unregistered principal, capability, machine approval, missing reason,
          self-review, stale revision, human approval of a reading of the law, disputant adjudicating); a link's
          proponent is not a registered principal
  I05     a rule is `settled` without two readings of distinct families with one blind uphold from the other family, or
          its state differs from the log's replay, or a reading names an event that is not its own
  I06     nao_avaliado without a typed reason, cumpre / nao_cumpre without citation or facts, incomplete manifest
  I07     a verdict lists something other than a facto id in facts_used (an assertion used as a fact)
  I08     a fact's known_at differs from its raw record's captured_at; a verdict's known_at precedes a fact it used
  I09     the same (id, revision) twice, revisions with gaps, a revision without supersedes, a broken hash chain
  I10     a raw record not read by a single GET; code in engine/ or verify.py that imports a network module; code in
          tools/ that sends (POST / data=)
  I11     a pessoa_singular with a name inside a publishable object (veredicto.entities)
  I12     an aggregate rule's completeness threshold not decided by a pessoa's product_rule decision in the log
  PROV    a ferramenta principal whose code no longer hashes to the hash registered for its version
  PACK    a package's hash is not the hash of its rule list, or it names rules that are not in the store
  DIFF    a stored diff differs from the one rebuilt from its two packages (engine/rules.py once A4 lands; D14)
"""
import ast
import hashlib
import json
import re
import shutil
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
from engine import evaluate as evaluate_mod  # noqa: E402
from engine import extract, governance, manifest, schema  # noqa: E402
from engine.canon import content_hash  # noqa: E402
from engine.store import Store, facts_of  # noqa: E402

VERSION = "ccp-verify-0.1"
STORES = {
    "fixtures": [ROOT / "fixtures/valid"],
    "repo": [ROOT / "law", ROOT / "rules", ROOT / "governance"],
    "data": [ROOT / "data"],
}
MODEL_MODULES = {"openai", "anthropic", "modal", "vllm", "transformers", "torch", "peft", "google.generativeai", "mistralai", "cohere", "ollama", "litellm", "langchain"}
NETWORK_MODULES = {"requests", "httpx", "aiohttp", "urllib.request", "urllib3", "socket", "http.client", "ftplib", "smtplib", "websocket", "websockets"}
SEND_PATTERNS = [re.compile(r"\.post\("), re.compile(r"method\s*=\s*[\"']POST[\"']"), re.compile(r"urlopen\([^)]*\bdata\s*="), re.compile(r"\.put\("), re.compile(r"\.delete\(")]


# ---- helpers -----------------------------------------------------------------------------------------------------
def current_of(store, type_):
    """Highest revision of each id of a type."""
    seen = {}
    for obj in store.objects[type_]:
        ident = obj.get("id")
        if ident is None:
            continue
        if ident not in seen or obj["revision"] > seen[ident]["revision"]:
            seen[ident] = obj
    return seen


def unit_chain(store, unit_id):
    """The unit and its ancestors, nearest first; (chain, cycle) where cycle is True when a parent repeats."""
    chain, u = [], store.current(unit_id)
    while u is not None:
        if u["id"] in chain:
            return chain, True
        chain.append(u["id"])
        u = store.current(u["parent"]) if u.get("parent") else None
    return chain, False


def coverage_of(store, adapter_ids):
    """{(adapter id, "YYYY-MM"): captured / expected | None} for the adapters a manifest names."""
    out = {}
    for aid in adapter_ids:
        a = store.current(aid)
        for c in (a or {}).get("coverage", []):
            out[(aid, c["period"])] = c["captured"] / c["expected"] if c.get("expected") else None
    return out


def package_rules(store, package_id):
    """The regra objects a package names, each at the exact revision it names; (rules, missing ids)."""
    pk = store.current(package_id)
    rules, missing = [], []
    for ref in (pk or {}).get("rules", []):
        rev = next((r for r in store.revisions(ref["id"]) if r["revision"] == ref["revision"]), None)
        (rules if rev else missing).append(rev or f"{ref['id']}@r{ref['revision']}")
    return rules, missing


def passage_text(store, passage_id, version):
    p = store.current(passage_id)
    if not p:
        return None
    for v in p.get("versions", []):
        if v.get("version") == version:
            return v.get("text")
    return None


# ---- checks ------------------------------------------------------------------------------------------------------
def check_references(store, out):
    def need(ident, where, kinds=None):
        if ident is None:
            return
        if not store.exists(ident):
            out.append(("REF", f"{where}: {ident} does not exist in the store"))
        elif kinds and schema.type_of(store.current(ident)) not in kinds:
            out.append(("REF", f"{where}: {ident} is not a {'/'.join(kinds)}"))
    events = {ev.get("id") for _, ev in store.events}
    principals = {p["id"] for p in (store.principals or {}).get("principals", [])}

    def need_event(eid, where):
        if eid is not None and eid not in events:
            out.append(("REF", f"{where}: {eid} is not in the governance log"))

    def need_principal(pid, where):
        if pid is not None and pid not in principals:
            out.append(("I04", f"{where}: principal {pid} is not registered"))

    for n in store.objects["norma"]:
        for r in n["source"]["raw"]:
            need(r, n["id"], {"raw"})
    for p in store.objects["passagem"]:
        need(p["norma"], p["id"], {"norma"})
        need(p["parent"], p["id"], {"passagem"})
        for v in p["versions"]:
            need(v["raw"], p["id"], {"raw"})
    for v in store.objects["vigencia"]:
        need(v["passage"], v["id"], {"passagem"}); need(v["altered_by"], v["id"], {"norma"}); need(v["note"]["raw"], v["id"], {"raw"})
    for r in store.objects["regra"]:
        need(r["norma"], r["id"], {"norma"})
        for c in r["passages"]:
            need(c["passage"], r["id"], {"passagem"})
        for e in r["exceptions"]:
            need(e["citation"]["passage"], r["id"], {"passagem"})
        for rd in r["readings"]:
            need_event(rd["evento"], r["id"]); need_principal(rd["principal"], r["id"])
            for pid in rd["chosen_passages"]:
                need(pid, r["id"], {"passagem"})
        ct = r["params"].get("completeness_threshold")
        if ct:
            need_event(ct["decided_by"], r["id"])
    for pk in store.objects["pacote"]:
        for r in pk["rules"]:
            need(r["id"], pk["id"], {"regra"})
    for d in store.objects["diff"]:
        need(d["from"], d["id"], {"pacote"}); need(d["to"], d["id"], {"pacote"})
    for a in store.objects["adaptador"]:
        need_principal(a["proposed_by"], a["id"])
    for u in store.objects["unidade"]:
        need(u["parent"], u["id"], {"unidade"})
        for r in u["raw"]:
            need(r, u["id"], {"raw"})
    for e in store.objects["entidade"]:
        for r in e["raw"]:
            need(r, e["id"], {"raw"})
        for role in e["roles"]:
            need(role["unit"], e["id"], {"unidade"})
    for a in store.objects["alias"]:
        need(a["raw"], a["id"], {"raw"}); need(a["link"], a["id"], {"link"})
    for l in store.objects["link"]:
        need(l["from"], l["id"], {"raw", "alias"}); need(l["to"], l["id"], {"entidade"}); need_principal(l["proponent"], l["id"]); need_event(l["evento"], l["id"])
    for f in store.objects["facto"]:
        need(f["unit"], f["id"], {"unidade"}); need(f["adapter"], f["id"], {"adaptador"})
        o = f["origin"]
        need(o.get("raw"), f["id"], {"raw"}); need(o.get("documento"), f["id"], {"documento"})
    for a in store.objects["afirmacao"]:
        need(a["unit"], a["id"], {"unidade"}); need(a["origin"]["raw"], a["id"], {"raw"}); need_principal(a["converted_by"], a["id"]); need_event(a["conversion_evento"], a["id"])
        for pid in a["passages"]:
            need(pid, a["id"], {"passagem"})
    for c in store.objects["conflito"]:
        need(c["unit"], c["id"], {"unidade"})
        for v in c["values"]:
            need(v["facto"], c["id"], {"facto"})
        if c["resolution"]["kind"] == "precedencia":
            need_event(c["resolution"]["rule_evento"], c["id"]); need(c["resolution"]["chosen"], c["id"], {"facto"})
    for d in store.objects["documento"]:
        need(d["raw"], d["id"], {"raw"}); need(d["origin"]["unit"], d["id"], {"unidade"})
    for v in store.objects["veredicto"]:
        need(v["rule"]["id"], v["id"], {"regra"}); need(v["unit"], v["id"], {"unidade"})
        if v.get("citation"):
            need(v["citation"]["passage"], v["id"], {"passagem"})
        for f in v["facts_used"]:
            if f.startswith("facto:"):
                need(f, v["id"], {"facto"})
        for a in v["assertions_compared"]:
            need(a["afirmacao"], v["id"], {"afirmacao"})
        for e in v["entities"]:
            need(e["id"], v["id"], {"entidade"})
        need(v["manifest"]["package"], v["id"], {"pacote"})
        for a in v["manifest"]["adapters"]:
            need(a, v["id"], {"adaptador"})
    for d in store.objects["disputa"]:
        need(d["veredicto"], d["id"], {"veredicto"}); need_principal(d["raised_by"], d["id"]); need_event(d["evento"], d["id"])
        if d["adjudication"]:
            need_principal(d["adjudication"]["by"], d["id"]); need_event(d["adjudication"]["evento"], d["id"])
    for c in store.objects["caso_referencia"]:
        need(c["unit"], c["id"], {"unidade"})
        for e in c["expected"]:
            need(e["rule"], c["id"], {"regra"})
        for a in c["annotators"]:
            need_principal(a["principal"], c["id"])


def check_sources(store, out):
    """I01: bytes hash to sha256; passage version text sits at its offsets in the raw text. I10: single passive GET."""
    for r in store.objects["raw"]:
        path = store.raw_path(r)
        if path is None:
            out.append(("I01", f"{r['id']}: bytes {r['bytes']} not in the store"))
        elif hashlib.sha256(path.read_bytes()).hexdigest() != r["sha256"]:
            out.append(("I01", f"{r['id']}: bytes do not hash to {r['sha256'][:12]}..."))
        text = r.get("text")
        if text and path is not None:
            fn = extract.EXTRACTORS.get(text["extractor"])
            tpath = store.raw_bytes.get(text["sha256"])
            if fn is None:
                out.append(("I01", f"{r['id']}: unknown extractor {text['extractor']}"))
            elif tpath is None:
                out.append(("I01", f"{r['id']}: derived text {text['bytes']} not in the store"))
            else:
                try:
                    derived = fn(path.read_bytes())
                except Exception as exc:  # the extractor refuses: the text cannot be re-derived
                    derived = None
                    out.append(("I01", f"{r['id']}: {text['extractor']} fails on the stored bytes: {exc}"))
                if derived is not None and (hashlib.sha256(derived.encode("utf-8")).hexdigest() != text["sha256"] or tpath.read_text(encoding="utf-8") != derived):
                    out.append(("I01", f"{r['id']}: derived text is not what {text['extractor']} produces from the bytes"))
        req = r.get("request") or {}
        if req.get("method") != "GET" or req.get("reads_of_page", 1) > 1:
            out.append(("I10", f"{r['id']}: captured by {req.get('method')} with {req.get('reads_of_page')} reads; only one passive GET per page"))
    for p in store.objects["passagem"]:
        for v in p["versions"]:
            raw = store.current(v["raw"])
            text = store.raw_text(raw) if raw else None
            if text is None:
                continue
            s, e = v["offsets"]["start"], v["offsets"]["end"]
            if text[s:e] != v["text"]:
                out.append(("I01", f"{p['id']} version {v['version']}: text is not raw[{s}:{e}] of {v['raw']}"))


def check_citations(store, out):
    """I02: every quote equals the passage version's text at its offsets."""
    def check(c, where):
        text = passage_text(store, c["passage"], c["version"])
        if text is None:
            out.append(("I02", f"{where}: {c['passage']} has no version {c['version']}"))
            return
        s, e = c["offsets"]["start"], c["offsets"]["end"]
        if text[s:e] != c["quote"]:
            out.append(("I02", f"{where}: quote {c['quote']!r} is not {c['passage']}@{c['version']}[{s}:{e}]"))
    for r in store.objects["regra"]:
        for c in r["passages"]:
            check(c, r["id"])
        for ex in r["exceptions"]:
            check(ex["citation"], r["id"])
    for v in store.objects["veredicto"]:
        if v.get("citation"):
            check(v["citation"], v["id"])
    for vg in store.objects["vigencia"]:
        raw = store.current(vg["note"]["raw"])
        text = store.raw_text(raw) if raw else None
        if text is not None:
            s, e = vg["note"]["offsets"]["start"], vg["note"]["offsets"]["end"]
            if text[s:e] != vg["note"]["quote"]:
                out.append(("I02", f"{vg['id']}: note quote is not raw[{s}:{e}]"))


def check_governance(store, out):
    """I04 / I09 via replay; I05 rule states against the replay; I12 product rules."""
    rp = governance.replay(store.events, store.principals)
    out.extend(rp.errors)
    if store.events and store.principals is None:
        out.append(("I04", f"{store.governance_dir}: events without principals.json"))
    events = {ev["id"]: ev for _, ev in store.events}
    for r in current_of(store, "regra").values():
        fams = {rd["family"] for rd in r["readings"]}
        blind_other = any(rd["blind"] and rd["family"] != r["readings"][0]["family"] for rd in r["readings"][1:]) if r["readings"] else False
        if r["state"] == "settled" and (len(fams) < 2 or not blind_other):
            out.append(("I05", f"{r['id']}: settled with families {sorted(fams)} and blind other-family reading={blind_other}; two families and one blind uphold are required"))
        for rd in r["readings"]:
            ev = events.get(rd["evento"])
            if ev and (ev["assertion"] != r["id"] or ev["principal"] != rd["principal"] or ev["action"] not in ("propose", "review", "correct")):
                out.append(("I05", f"{r['id']}: reading by {rd['principal']} names {rd['evento']}, which is not its own event"))
        replayed = rp.state_of("regra", r["id"])
        if replayed is not None and replayed != r["state"]:
            out.append(("I05", f"{r['id']}: stored state {r['state']} but the log replays {replayed}"))
        ct = r["params"].get("completeness_threshold")
        if ct:
            ev = events.get(ct["decided_by"])
            decided = bool(ev) and ev["assertion_type"] == "product_rule" and ev["principal"].startswith("pessoa:") and (
                ev["action"] == "approve" or (ev["action"] == "propose" and ev.get("reason")))
            if not decided:
                out.append(("I12", f"{r['id']}: completeness threshold decided by {ct['decided_by']}, which is not a pessoa's product_rule decision"))
    for l in store.objects["link"]:
        if not l.get("proponent"):
            out.append(("I04", f"{l['id']}: link without proponent"))
    for p in (store.principals or {}).get("principals", []):
        if p.get("papel") == "ferramenta" and not p.get("retired") and p.get("code"):
            path = ROOT / p["code"]
            if path.exists() and hashlib.sha256(path.read_bytes()).hexdigest() != p.get("hash"):
                out.append(("PROV", f"{p['id']}: {p['code']} no longer hashes to the registered hash; register a new version and retire this one"))
    return rp


def check_verdicts(store, out):
    """I06, I07, I08, I11."""
    facts = current_of(store, "facto")
    raws = current_of(store, "raw")
    for f in facts.values():
        raw = raws.get(f["origin"].get("raw"))
        if raw and f["known_at"] != raw["captured_at"]:
            out.append(("I08", f"{f['id']}: known_at {f['known_at']} differs from its raw record's captured_at {raw['captured_at']}"))
    for v in store.objects["veredicto"]:
        if v["result"] == "nao_avaliado" and not v.get("reason"):
            out.append(("I06", f"{v['id']}: nao_avaliado without a typed reason"))
        if v["result"] != "nao_avaliado":
            if v.get("reason"):
                out.append(("I06", f"{v['id']}: {v['result']} with a reason"))
            if not v.get("citation"):
                out.append(("I06", f"{v['id']}: {v['result']} without a citation"))
            if not v["facts_used"]:
                out.append(("I06", f"{v['id']}: {v['result']} without facts"))
        missing = manifest.is_complete(v.get("manifest"))
        if missing:
            out.append(("I06", f"{v['id']}: manifest incomplete: {', '.join(missing)}"))
        for fid in v["facts_used"]:
            if not fid.startswith("facto:"):
                out.append(("I07", f"{v['id']}: {fid} used as a fact; only facto ids may ground a verdict"))
            elif fid in facts and facts[fid]["known_at"] > v["known_at"]:
                out.append(("I08", f"{v['id']}: known_at {v['known_at']} precedes fact {fid} known at {facts[fid]['known_at']}"))
        for e in v["entities"]:
            if e.get("type") == "pessoa_singular" and e.get("name"):
                out.append(("I11", f"{v['id']}: natural person {e['id']} published with a name"))


def log_prefix_heads(store):
    """{head after event n: event n} for every prefix of the governance log (GENESIS for the empty prefix)."""
    heads = {governance.GENESIS: None}
    for line, ev in store.events:
        heads[hashlib.sha256(line.encode("utf-8")).hexdigest()] = ev
    return heads


def check_manifest(store, out):
    """MAN: a manifest is checked against the store, not trusted (§7). log_head is the head of a prefix of the log whose
    last event is not after produced_at (DECISIONS D25: the log as it stood; later events do not void a verdict); the
    package exists, has the manifest's law_version and names the verdict's rule at its exact revision; every adapter of
    the facts used is listed; every source snapshot names a raw record with that sha256, source and captured_at. A
    package's own log_head is a prefix head too."""
    heads = log_prefix_heads(store)
    facts = current_of(store, "facto")
    raws_by_sha = {}
    for r in current_of(store, "raw").values():
        raws_by_sha.setdefault(r["sha256"], []).append(r)
    for pk in current_of(store, "pacote").values():
        if pk["log_head"] not in heads:
            out.append(("MAN", f"{pk['id']}: log_head {pk['log_head'][:12]}... is not the head of any prefix of the governance log"))
    for v in current_of(store, "veredicto").values():
        m, where = v["manifest"], v["id"]
        if m["log_head"] not in heads:
            out.append(("MAN", f"{where}: manifest.log_head {m['log_head'][:12]}... is not the head of any prefix of the governance log"))
        elif heads[m["log_head"]] is not None and heads[m["log_head"]]["at"] > m["produced_at"]:
            out.append(("MAN", f"{where}: manifest.log_head is the log after {heads[m['log_head']]['id']} ({heads[m['log_head']]['at']}), later than produced_at {m['produced_at']}"))
        pk = store.current(m["package"])
        if pk is None:
            out.append(("MAN", f"{where}: manifest.package {m['package']} is not in the store"))
        else:
            if pk["law_version"] != m["law_version"]:
                out.append(("MAN", f"{where}: manifest.law_version {m['law_version']} but package {pk['id']} is {pk['law_version']}"))
            named = {r["id"]: r["revision"] for r in pk["rules"]}
            if v["rule"]["id"] not in named:
                out.append(("MAN", f"{where}: package {pk['id']} does not name rule {v['rule']['id']}"))
            elif named[v["rule"]["id"]] != v["rule"]["revision"]:
                out.append(("MAN", f"{where}: package {pk['id']} names {v['rule']['id']} at revision {named[v['rule']['id']]}, the verdict at {v['rule']['revision']}"))
        if not any(r["revision"] == v["rule"]["revision"] for r in store.revisions(v["rule"]["id"])):
            out.append(("MAN", f"{where}: rule {v['rule']['id']} has no revision {v['rule']['revision']} in the store"))
        for fid in v["facts_used"]:
            f = facts.get(fid)
            if f and f["adapter"] not in m["adapters"]:
                out.append(("MAN", f"{where}: fact {fid} comes from {f['adapter']}, which the manifest does not list"))
        for snap in m["source_snapshots"]:
            if not any(r["source"] == snap["source"] and r["captured_at"] == snap["captured_at"] for r in raws_by_sha.get(snap["sha256"], [])):
                out.append(("MAN", f"{where}: source snapshot {snap['source']} {snap['sha256'][:12]}... names no raw record with that sha256, source and captured_at"))


RED_FIELDS = ("id", "rule", "result", "reason", "citation", "assertions_compared")


def check_rederive(store, out):
    """RED (invariant 3): every current, non-stale verdict is re-computed by engine.evaluate from the store and must come
    out the same. Inputs, all read from the store: the facts of the verdict's unit and its ancestors (store.facts_of,
    as known at the verdict's known_at), the conflitos and documentos of that chain, the afirmações of the unit, the
    entidades with a role in the unit, the rules of manifest.package at the revisions it names, and the coverage of the
    manifest's adapters. Compared: id, rule, result, reason, citation, assertions_compared, set(facts_used); and the
    unit's kind must be one the rule applies_to. detail is free text and is not compared."""
    for v in current_of(store, "veredicto").values():
        if v.get("stale"):
            continue
        where = v["id"]
        chain, cycle = unit_chain(store, v["unit"])
        unit = store.current(v["unit"])
        if unit is None or cycle:
            out.append(("RED", f"{where}: cannot re-derive: unit {v['unit']} " + ("is unknown" if unit is None else "sits in a parent cycle")))
            continue
        rules, _ = package_rules(store, v["manifest"]["package"])
        rule_rec = next((r for r in store.revisions(v["rule"]["id"]) if r["revision"] == v["rule"]["revision"]), None)
        if rule_rec and unit["kind"] not in rule_rec["applies_to"]:
            out.append(("RED", f"{where}: unit {unit['id']} is a {unit['kind']}; rule {rule_rec['id']} applies to {rule_rec['applies_to']}"))
        try:
            produced = evaluate_mod.evaluate(
                unit, rules, facts_of(store, unit["id"], known_at=v["known_at"]), v["known_at"], v["valid_at"], manifest=v["manifest"],
                conflicts=[c for c in current_of(store, "conflito").values() if c["unit"] in chain],
                assertions=[a for a in current_of(store, "afirmacao").values() if a["unit"] == unit["id"]],
                entities=[e for e in current_of(store, "entidade").values() if any(r["unit"] == unit["id"] for r in e["roles"])],
                documents=[d for d in current_of(store, "documento").values() if d["origin"]["unit"] in chain],
                coverage=coverage_of(store, v["manifest"]["adapters"]))
        except Exception as exc:  # an incomplete manifest or an unknown rule type: the verdict cannot be replayed
            out.append(("RED", f"{where}: evaluate refuses to re-derive it: {exc}"))
            continue
        got = next((p for p in produced if p["rule"]["id"] == v["rule"]["id"]), None)
        if got is None:
            out.append(("RED", f"{where}: re-derivation produces no verdict for {v['rule']['id']} from package {v['manifest']['package']}"))
            continue
        diffs = [k for k in RED_FIELDS if got.get(k) != v.get(k)]
        if set(got["facts_used"]) != set(v["facts_used"]):
            diffs.append("facts_used")
        if diffs:
            shown = ", ".join(f"{k}: stored {v.get(k)!r} re-derived {got.get(k)!r}" for k in diffs if k in ("result", "reason", "rule", "id"))
            out.append(("RED", f"{where}: re-derived verdict differs in {', '.join(diffs)}" + (f" ({shown})" if shown else "")))


def check_packages(store, out):
    for pk in store.objects["pacote"]:
        rules = sorted(pk["rules"], key=lambda r: r["id"])
        if content_hash(rules) != pk["hash"]:
            out.append(("PACK", f"{pk['id']}: hash is not the hash of its rule list"))
        if rules != pk["rules"]:
            out.append(("PACK", f"{pk['id']}: rules are not sorted by id"))
    try:
        from engine import rules as rules_mod
    except ImportError:
        return
    packages = current_of(store, "pacote")
    regras = current_of(store, "regra")
    for d in store.objects["diff"]:
        a, b = packages.get(d["from"]), packages.get(d["to"])
        if a and b:
            built = rules_mod.diff(a, b, regras)
            if built["by_rule"] != d["by_rule"] or built["by_consumer_field"] != d["by_consumer_field"]:
                out.append(("DIFF", f"{d['id']}: differs from the diff rebuilt from its packages"))


def check_layout(store, out):
    for path in store.unknown_files:
        out.append(("LAYOUT", f"{path}: a JSON file outside any typed directory under facts/"))


def check_code(paths=None):
    """I03 and I10 over the engine's own code. Static: imports are read from the AST, never executed."""
    out = []
    paths = paths or [ROOT / "engine", ROOT / "tools", ROOT / "verify.py"]
    for base in paths:
        files = [base] if base.is_file() else sorted(base.rglob("*.py"))
        for f in files:
            if "__pycache__" in f.parts:
                continue
            src = f.read_text(encoding="utf-8")
            try:
                tree = ast.parse(src)
            except SyntaxError as exc:
                out.append(("I03", f"{f}: cannot parse: {exc}"))
                continue
            names = set()
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    names.update(a.name for a in node.names)
                elif isinstance(node, ast.ImportFrom) and node.module:
                    names.add(node.module)
                    names.update(f"{node.module}.{a.name}" for a in node.names)
            for name in sorted(names):
                top = name.split(".")[0]
                if top in MODEL_MODULES or name in MODEL_MODULES:
                    out.append(("I03", f"{f.relative_to(ROOT) if f.is_relative_to(ROOT) else f}: imports {name}; no model inside the engine or the gate"))
                in_tools = "tools" in f.parts
                if (name in NETWORK_MODULES or top in NETWORK_MODULES) and not in_tools:
                    out.append(("I10", f"{f.relative_to(ROOT) if f.is_relative_to(ROOT) else f}: imports {name}; engine and gate never touch the network"))
            if "tools" in f.parts:
                for pat in SEND_PATTERNS:
                    if pat.search(src):
                        out.append(("I10", f"{f.relative_to(ROOT)}: matches {pat.pattern}; tools read, never send"))
    return out


def check_store(roots):
    store = Store(roots).load()
    out = list(store.errors)
    check_layout(store, out)
    check_references(store, out)
    check_sources(store, out)
    check_citations(store, out)
    check_governance(store, out)
    check_verdicts(store, out)
    check_manifest(store, out)
    check_rederive(store, out)
    check_packages(store, out)
    return store, out


# ---- broken overlays ---------------------------------------------------------------------------------------------
def run_broken(valid_root, broken_root):
    results = []
    for overlay in sorted(p for p in broken_root.iterdir() if p.is_dir()):
        expect = {c for c in (overlay / "EXPECT").read_text().split()} if (overlay / "EXPECT").exists() else set()
        mutation = overlay / "engine_mutation"
        if mutation.is_dir():
            codes = {c for c, _ in check_code([mutation])}
        else:
            with tempfile.TemporaryDirectory() as tmp:
                merged = Path(tmp) / "store"
                shutil.copytree(valid_root, merged)
                for f in overlay.rglob("*"):
                    if f.is_file() and f.name != "EXPECT":
                        dest = merged / f.relative_to(overlay)
                        dest.parent.mkdir(parents=True, exist_ok=True)
                        shutil.copy(f, dest)
                _, out = check_store([merged])
                codes = {c for c, _ in out}
        results.append((overlay.name, expect, codes))
    return results


def main(argv) -> int:
    if len(argv) >= 2 and argv[1] == "--store":
        _, out = check_store([Path(p) for p in argv[2:]])
        for code, msg in out:
            print(f"FAIL {code}  {msg}")
        print(f"verify --store: {len(out)} failure(s)")
        return 1 if out else 0
    failed = False
    code_out = check_code()
    for code, msg in code_out:
        print(f"FAIL {code}  {msg}")
    failed |= bool(code_out)
    print(f"code guard (I03/I10): {'ok' if not code_out else 'FAILED'}")
    for name, roots in STORES.items():
        store, out = check_store(roots)
        for code, msg in out:
            print(f"FAIL {code}  {msg}")
        n = sum(len(v) for v in store.objects.values())
        print(f"store {name}: {n} objects, {len(store.events)} events, {len(out)} failure(s)")
        failed |= bool(out)
    for name, expect, codes in run_broken(ROOT / "fixtures/valid", ROOT / "fixtures/broken"):
        ok = bool(expect) and expect <= codes
        print(f"broken {name}: expected {sorted(expect)} got {sorted(codes)} -> {'ok' if ok else 'NOT REFUSED'}")
        failed |= not ok
    print("verify:", "FAILED" if failed else "ok", f"({VERSION}; no model called)")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
