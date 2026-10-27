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
  I11     a pessoa_singular with a name inside a publishable object (veredicto.entities); a published entity whose type is
          not its record's type (the record decides, not the verdict)
  I12     an aggregate rule's completeness threshold not decided by a pessoa's product_rule decision in the log
  PROV    a ferramenta principal whose code no longer hashes to the hash registered for its version
  READ    a leitor's raw answer file missing or not hashing to the answer_sha256 its log event recorded
  SEAL    measurement annotations, law/HELD-OUT.json, law/TRAIN-HELD-OUT.json, training/data/INDEX.json or the T3 answers
          (governance/readings/avaliacao-v1) not matching the newest seal event in the log (tools/measure.py seal; D40, D42)
  PACK    a package's hash is not the hash of its rule list, or it names rules that are not in the store
  DIFF    a stored diff differs from the one rebuilt from its two packages (engine/rules.py once A4 lands; D14)
Cross-object checks (A3b, audit of 2026-10-24; each has a broken overlay and red-team mutations):
  RED     a stored verdict is not what engine.evaluate re-derives from the store (facts of the unit chain, conflicts,
          documents, assertions, entities, the manifest package's rules at their revisions, the adapters' coverage):
          id, rule, result, reason, citation, assertions_compared or facts_used differ; or the rule does not apply to
          the unit's kind; or the unit cannot be read (unknown, parent cycle)
  MAN     a manifest or package log_head that is not the head of a prefix of the log (D25), or whose prefix ends after
          produced_at; a package that is missing, of another law_version, or does not name the verdict's rule at its
          revision; a rule revision that does not exist; a fact whose adapter the manifest omits; a source snapshot
          that names no raw record with that sha256, source and captured_at
  STATE   a stored state that is not the log's replay: link (an evento-less link only for a ferramenta's nif_exact),
          adaptador, disputa, afirmação conversion event; a package naming a non-settled rule revision; a reading
          choosing passages its rule does not cite; a rule whose highest stored revision is not the log's revision
  TIME    passage versions out of order, overlapping or closing before they open; a vigencia that starts no version of
          its passage; a rule whose validity is not that of the versions it cites (D26); a verdict citing a version not
          in force on its valid_at
  GRAPH   a unit in a parent cycle, or whose parent is not of an earlier kind (proc -> lote -> contrato -> mod)
  FIELD   a conflito whose facts do not carry its field, value or unit chain; a fact whose field (and, for a raw origin,
          source field) is not in its adapter's mapping
  BENCH   a held-out reference case without frozen_at; law/HELD-OUT.json changed after it was frozen; a package built
          after frozen_at holding a rule whose log events name a held-out unit
  MEAS    a reports/measure/<date>.json that tools/measure.py (amalia-*.json: tools/measure_reader.py) does not recompute
          from the stored answers
  TRAIN   training/data (INDEX.json and every example file) that tools/make_training.py does not regenerate byte for byte
          from the store and the training reservation; a train example touching a reserved article (phase 4, T1)
  I01 also: raw bytes that no raw record names (orphans)
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
from engine.canon import canonical as canonical_json, content_hash  # noqa: E402
from engine.store import Store, facts_of  # noqa: E402

VERSION = "ccp-verify-0.2"
STORES = {
    "fixtures": [ROOT / "fixtures/valid"],
    "repo": [ROOT / "law", ROOT / "rules", ROOT / "governance"],
    "data": [ROOT / "data", ROOT / "governance"],  # the principals and the log that data/'s adaptadores and links name
}
if (ROOT / "reports/veredictos").exists():  # B4: real verdicts are re-derived with the facts, law, rules and log they used
    STORES["engine"] = [ROOT / "data", ROOT / "law", ROOT / "rules", ROOT / "governance", ROOT / "reports/veredictos"]
if (ROOT / "fixtures/measure").exists():  # B5: reference cases measured while data/ is empty
    STORES["measure"] = [ROOT / "fixtures/measure", ROOT / "law", ROOT / "rules", ROOT / "governance"]
MODEL_MODULES = {"openai", "anthropic", "modal", "vllm", "transformers", "torch", "peft", "google.generativeai", "mistralai", "cohere", "ollama", "litellm", "langchain", "readers"}
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
        elif heads[m["log_head"]] is not None and heads[m["log_head"]]["at"] > v["known_at"]:
            out.append(("MAN", f"{where}: manifest.log_head is the log after {heads[m['log_head']]['id']} ({heads[m['log_head']]['at']}), later than the verdict's known_at {v['known_at']}"))
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


def check_states(store, rp, out):
    """STATE (invariants 4, 9): every stored state is the log's replay, not a claim. A link with an evento has the
    replayed state of that link; a link without one is only a ferramenta's nif_exact (deterministic). An adaptador has
    its replayed state, or `proposed` when the log has never seen it. A disputa is the replayed dispute (disputant,
    verdict, state, adjudicator, outcome, adjudication event). An afirmação's conversion_evento is the
    afirmacao_conversao event of that afirmação by its converted_by. A package names only rules whose named revision is
    settled. A reading chooses only passages its rule cites. A rule's highest stored revision is at least the log's revision
    (above it only for a state change by review, with unchanged content and the replay's state: D43)."""
    events = {ev["id"]: ev for _, ev in store.events}
    for l in current_of(store, "link").values():
        if l["evento"] is None:
            if not (l["method"] == "nif_exact" and l["proponent"].startswith("ferramenta:")):
                out.append(("STATE", f"{l['id']}: state {l['state']} with no log event; only a ferramenta's nif_exact link stands outside the log"))
            continue
        replayed = rp.state_of("link", l["id"])
        if replayed != l["state"]:
            out.append(("STATE", f"{l['id']}: stored state {l['state']} but the log replays {replayed}"))
    for l in current_of(store, "link").values():
        target = store.current(l["to"])
        if l["state"] != "stale" and not l.get("stale") and target is not None and target.get("stale"):
            out.append(("STATE", f"{l['id']}: {l['state']} link to {l['to']}, whose head revision is stale; mark the link stale or link the replacement"))
    for a in current_of(store, "adaptador").values():
        replayed = rp.state_of("adaptador", a["id"]) or "proposed"
        if replayed != a["state"]:
            out.append(("STATE", f"{a['id']}: stored state {a['state']} but the log replays {replayed}"))
    for d in current_of(store, "disputa").values():
        r = rp.disputes.get(d["id"])
        if r is None:
            out.append(("STATE", f"{d['id']}: no dispute event for it in the log"))
            continue
        adj = d.get("adjudication") or {}
        stored = (d["raised_by"], d["veredicto"], d["state"], adj.get("by"), adj.get("outcome"))
        log = (r["disputant"], r["veredicto"], r["state"], r["adjudicator"], r.get("outcome"))
        if stored != log:
            out.append(("STATE", f"{d['id']}: stored (raised_by, veredicto, state, adjudicator, outcome) {stored} but the log replays {log}"))
        if adj and int(str(adj.get("evento", "evento:0")).split(":")[1]) not in r["events"]:
            out.append(("STATE", f"{d['id']}: adjudication names {adj.get('evento')}, which is not this dispute's adjudication in the log"))
    for a in current_of(store, "afirmacao").values():
        ev = events.get(a["conversion_evento"])
        if ev and (ev["assertion_type"] != "afirmacao_conversao" or ev["assertion"] != a["id"] or ev["principal"] != a["converted_by"]):
            out.append(("STATE", f"{a['id']}: conversion_evento {a['conversion_evento']} is not the afirmacao_conversao of this afirmação by {a['converted_by']}"))
    for pk in current_of(store, "pacote").values():
        for ref in pk["rules"]:
            rec = next((r for r in store.revisions(ref["id"]) if r["revision"] == ref["revision"]), None)
            if rec and rec["state"] != "settled":
                out.append(("STATE", f"{pk['id']}: names {ref['id']} revision {ref['revision']}, whose state is {rec['state']}; a package holds settled rules only"))
    events_by_id = {ev["id"]: ev for _, ev in store.events}
    for r in current_of(store, "regra").values():
        cited = {c["passage"] for c in r["passages"]} | {e["citation"]["passage"] for e in r["exceptions"]}
        for rd in r["readings"]:
            ev = events_by_id.get(rd["evento"])
            # D39: the proposer's reading is the rule; an upholding review agrees with it; a disagreeing review keeps its own passages
            if ev and ev["action"] == "review" and ev.get("verdict") != "uphold":
                continue
            extra = sorted(set(rd["chosen_passages"]) - cited)
            if extra:
                out.append(("STATE", f"{r['id']}: reading {rd['evento']} chose {extra}, which the rule does not cite"))
        known = rp.assertions.get(("regra", r["id"]))
        if known and r["revision"] < known["revision"]:
            out.append(("STATE", f"{r['id']}: highest stored revision is {r['revision']} but the log is at revision {known['revision']}"))
        elif known and r["revision"] > known["revision"]:
            # D43: a review changes a rule's state, not its content: the object may gain revisions above the log's (a
            # correct is what raises the log's revision) only while its content is the log's latest (check_rule_content)
            # and its state is the replay's
            if r["state"] != rp.state_of("regra", r["id"]):
                out.append(("STATE", f"{r['id']}: revision {r['revision']} above the log's {known['revision']} with state {r['state']}, the replay says {rp.state_of('regra', r['id'])}"))
            base = next((x for x in store.revisions(r["id"]) if x["revision"] == known["revision"]), None)
            moving = {"revision", "recorded_at", "supersedes", "state", "readings"}
            if base is None or {k: v for k, v in r.items() if k not in moving} != {k: v for k, v in base.items() if k not in moving}:
                out.append(("STATE", f"{r['id']}: revision {r['revision']} above the log's {known['revision']} changes the rule's content; only a correct in the log may"))
            old = {rd["evento"] for rd in base["readings"]} if base else set()
            for rd in r["readings"]:
                ev = events_by_id.get(rd["evento"])
                if rd["evento"] not in old and not (ev and ev["action"] == "review" and ev["assertion"] == r["id"]):
                    out.append(("STATE", f"{r['id']}: revision {r['revision']} adds reading {rd['evento']}, which is not a review of this rule in the log"))


def _version(store, passage_id, version):
    p = store.current(passage_id)
    return next((v for v in (p or {}).get("versions", []) if v["version"] == version), None)


def _in_force(v, date):
    return v["valid_from"] <= date and (v["valid_to"] is None or date < v["valid_to"])


def check_law_time(store, out):
    """TIME (invariant 8, the law clock). A passage's versions are ordered by valid_from, each closes before the next
    opens and only the last may be open. A vigencia that is not stale starts a version of its passage. A rule's validity is the validity
    of the text it cites (DECISIONS D26): its valid_from is the latest valid_from among the versions it cites, it lies
    inside every cited version, and it does not outlive a closed one. The version a verdict cites is in force on the
    verdict's valid_at and is not revoked; versions are contiguous."""
    for p in current_of(store, "passagem").values():
        vs = p["versions"]
        if [v["valid_from"] for v in vs] != sorted(v["valid_from"] for v in vs) or len({v["valid_from"] for v in vs}) != len(vs):
            out.append(("TIME", f"{p['id']}: versions are not in strictly increasing valid_from order"))
        for v in vs:
            if v["valid_to"] is not None and v["valid_to"] <= v["valid_from"]:
                out.append(("TIME", f"{p['id']} version {v['version']}: valid_to {v['valid_to']} is not after valid_from {v['valid_from']}"))
        ordered = sorted(vs, key=lambda v: v["valid_from"])
        for a, b in zip(ordered, ordered[1:]):
            if a["valid_to"] is None or a["valid_to"] > b["valid_from"]:
                out.append(("TIME", f"{p['id']}: version {a['version']} ({a['valid_from']}..{a['valid_to']}) overlaps version {b['version']} from {b['valid_from']}"))
            elif a["valid_to"] < b["valid_from"]:
                out.append(("TIME", f"{p['id']}: gap between version {a['version']} (ends {a['valid_to']}) and version {b['version']} (starts {b['valid_from']}); versions are contiguous"))
    for vg in current_of(store, "vigencia").values():
        if vg.get("stale"):
            continue  # withdrawn with its reason (a stale revision): it no longer claims a version start
        p = store.current(vg["passage"])
        if p and not any(v["valid_from"] == vg["valid_from"] for v in p["versions"]):
            out.append(("TIME", f"{vg['id']}: valid_from {vg['valid_from']} starts no version of {vg['passage']}"))
    for r in current_of(store, "regra").values():
        cited = [_version(store, c["passage"], c["version"]) for c in r["passages"] + [e["citation"] for e in r["exceptions"]]]
        cited = [v for v in cited if v]  # a missing version is I02's
        if not cited:
            continue
        latest = max(v["valid_from"] for v in cited)
        if r["valid_from"] != latest:
            out.append(("TIME", f"{r['id']}: valid_from {r['valid_from']} but the latest version it cites starts {latest}"))
        for v in cited:
            if not _in_force(v, r["valid_from"]):
                out.append(("TIME", f"{r['id']}: valid_from {r['valid_from']} is outside the cited version {v['version']} ({v['valid_from']}..{v['valid_to']})"))
            if v["valid_to"] is not None and (r["valid_to"] is None or r["valid_to"] > v["valid_to"]):
                out.append(("TIME", f"{r['id']}: valid until {r['valid_to']} but cited version {v['version']} ends {v['valid_to']}"))
    for vd in current_of(store, "veredicto").values():
        c = vd.get("citation")
        v = _version(store, c["passage"], c["version"]) if c else None
        if v and not _in_force(v, vd["valid_at"]):
            out.append(("TIME", f"{vd['id']}: cites {c['passage']}@{c['version']} ({v['valid_from']}..{v['valid_to']}), not in force on valid_at {vd['valid_at']}"))
        if v and v.get("revoked"):
            out.append(("TIME", f"{vd['id']}: cites {c['passage']}@{c['version']}, a revoked version; a revoked text grounds no verdict"))


UNIT_ORDER = ("proc", "lote", "contrato", "mod")


def check_cross(store, out):
    """The smaller cross-object checks of A3b item 5.
    GRAPH  a unit sits in a parent cycle, or its parent is not of an earlier kind (proc -> lote -> contrato -> mod)
    FIELD  a conflito names a field, value or unit its facts do not carry; a fact's field is not in its adapter's mapping
           (for a fact read from a raw record, the mapping row must also name the record's source field)
    I11    a verdict's entity whose stored record is a pessoa_singular is published with a name, or under another type
    BENCH  a held-out reference case without frozen_at
    I01    a file in raw_bytes/ that no raw record (bytes or derived text) names"""
    for u in current_of(store, "unidade").values():
        chain, cycle = unit_chain(store, u["id"])
        if cycle:
            out.append(("GRAPH", f"{u['id']}: parent chain {' -> '.join(chain)} returns to itself"))
        parent = store.current(u["parent"]) if u.get("parent") else None
        if parent and u["kind"] in UNIT_ORDER and parent.get("kind") in UNIT_ORDER and UNIT_ORDER.index(parent["kind"]) >= UNIT_ORDER.index(u["kind"]):
            out.append(("GRAPH", f"{u['id']}: a {u['kind']} whose parent {parent['id']} is a {parent['kind']}"))
    facts = current_of(store, "facto")
    for c in current_of(store, "conflito").values():
        chain, _ = unit_chain(store, c["unit"])
        for val in c["values"]:
            f = facts.get(val["facto"])
            if f is None:
                continue
            if f["field"] != c["field"]:
                out.append(("FIELD", f"{c['id']}: conflict on {c['field']} but {f['id']} is a fact of {f['field']}"))
            if f["value"] != val["value"]:
                out.append(("FIELD", f"{c['id']}: records {val['value']!r} for {f['id']}, whose value is {f['value']!r}"))
            if f["unit"] not in chain:
                out.append(("FIELD", f"{c['id']}: {f['id']} belongs to {f['unit']}, outside {c['unit']} and its ancestors"))
    for f in facts.values():
        a = store.current(f["adapter"])
        if a is None:
            continue
        rows = [m for m in a["mapping"] if m["canonical_field"] == f["field"]]
        src = f["origin"].get("field")
        if not rows:
            out.append(("FIELD", f"{f['id']}: field {f['field']} is not in the mapping of {a['id']}"))
        elif src is not None and not any(m["source_field"] == src for m in rows):
            out.append(("FIELD", f"{f['id']}: {a['id']} maps {f['field']} from {[m['source_field'] for m in rows]}, not from {src}"))
    for v in current_of(store, "veredicto").values():
        for e in v["entities"]:
            rec = store.current(e["id"])
            if rec is None:
                continue
            if rec["type"] != e.get("type"):
                out.append(("I11", f"{v['id']}: entity {e['id']} published as {e.get('type')}, stored as {rec['type']}"))
            if rec["type"] == "pessoa_singular" and e.get("name"):
                out.append(("I11", f"{v['id']}: natural person {e['id']} (per its record) published with a name"))
    for c in current_of(store, "caso_referencia").values():
        if c["held_out"] and not c["frozen_at"]:
            out.append(("BENCH", f"{c['id']}: held out without frozen_at; a held-out case is frozen before any rule is measured on it"))
    named = set()
    for r in store.objects["raw"]:  # every revision: a superseded working text stays (nothing is deleted, D29)
        named.add(r["sha256"])
        if r.get("text"):
            named.add(r["text"]["sha256"])
    for sha, path in sorted(store.raw_bytes.items()):
        if sha not in named:
            out.append(("I01", f"{path}: raw bytes no raw record names (orphan)"))


RED_FIELDS = ("id", "rule", "result", "reason", "citation", "assertions_compared")


def check_rederive(store, out):
    """RED (invariant 3): every current, non-stale verdict is re-computed by engine.evaluate from the store and must come
    out the same. Inputs, all read from the store: the facts of the verdict's unit and its ancestors (store.facts_of,
    as known at the verdict's known_at), the conflitos and documentos of that chain, the afirmações of the unit, the
    entidades with a role in the unit's lineage (ancestors and descendants), the rules of manifest.package at the revisions it names, and the coverage of the
    manifest's adapters. Compared: id, rule, result, reason, citation, assertions_compared, set(facts_used), entities; and the
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
        lineage = set(chain) | {u["id"] for u in current_of(store, "unidade").values() if unit["id"] in unit_chain(store, u["id"])[0]}
        rule_rec = next((r for r in store.revisions(v["rule"]["id"]) if r["revision"] == v["rule"]["revision"]), None)
        if rule_rec and unit["kind"] not in rule_rec["applies_to"]:
            out.append(("RED", f"{where}: unit {unit['id']} is a {unit['kind']}; rule {rule_rec['id']} applies to {rule_rec['applies_to']}"))
        try:
            produced = evaluate_mod.evaluate(
                unit, rules, facts_of(store, unit["id"], known_at=v["known_at"]), v["known_at"], v["valid_at"], manifest=v["manifest"],
                conflicts=[c for c in current_of(store, "conflito").values() if c["unit"] in chain],
                assertions=[a for a in current_of(store, "afirmacao").values() if a["unit"] == unit["id"]],
                entities=[e for e in current_of(store, "entidade").values() if any(r["unit"] in lineage for r in e["roles"])],
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
        key = lambda e: (e["id"], e["type"], e["role"], e.get("name"))  # noqa: E731
        if sorted(map(key, got["entities"])) != sorted(map(key, v["entities"])):
            diffs.append("entities")
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
    check_law_time(store, out)
    rp = check_governance(store, out)
    check_states(store, rp, out)
    check_verdicts(store, out)
    check_cross(store, out)
    check_manifest(store, out)
    check_rederive(store, out)
    check_packages(store, out)
    check_rule_content(store, out)
    check_readings(store, out)
    check_seal(store, out)
    for tdir, held in training_dirs(roots):
        check_training(store, out, tdir, held)
        check_training_v2(store, out, tdir, held)
        check_training_v2(store, out, tdir, held, sub="data-v3", module="make_regimes")
        check_training_v2(store, out, tdir, held, sub="data-v4", module="make_question_conditions")
        check_training_v2(store, out, tdir, held, sub="data-v5", module="make_user_facts")
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


def reading_dir(rule_id: str) -> str:
    """governance/readings/<dir> for a rule id: regra:ccp:x@v2 -> ccp--x-at-v2 (tools/read_rules.slug)."""
    return rule_id.split(":", 1)[1].replace(":", "--").replace("@", "-at-")


def check_rule_content(store, out):
    """STATE: a rule file in rules/ is the replay of the log, in content too: its params, conditions and cited passage
    ids equal the payload of the latest propose/correct event of that rule (where the payload carries them)."""
    latest = {}
    for _, ev in store.events:
        if ev["assertion_type"] == "regra" and ev["action"] in ("propose", "correct"):
            latest[ev["assertion"]] = ev
    for r in current_of(store, "regra").values():
        ev = latest.get(r["id"])
        if ev is None:
            continue
        p = ev.get("payload") or {}
        if "params" in p and p["params"] != r["params"]:
            out.append(("STATE", f"{r['id']}: params differ from the log's proposal {ev['id']}"))
        if "conditions" in p and p["conditions"] != r["conditions"]:
            out.append(("STATE", f"{r['id']}: conditions differ from the log's proposal {ev['id']}"))
        if "chosen_passages" in p and set(p["chosen_passages"]) != {c["passage"] for c in r["passages"]}:
            out.append(("STATE", f"{r['id']}: cited passages differ from the log's proposal {ev['id']}"))


def check_readings(store, out, readings_root=None):
    """READ (invariants 4, 5): every log event that carries payload.answer_sha256 (a leitor's proposal or review of a
    rule) has its raw answer on disk, governance/readings/<rule>/leitor-<a|b>.json, whose "answer" text hashes to that
    sha256 and whose own "sha256" field says the same. The log is the anchor; the file is the evidence; neither can
    change alone."""
    root = Path(readings_root) if readings_root else (store.governance_dir / "readings" if store.governance_dir else None)
    if root is None:
        return
    for _, ev in store.events:
        want = (ev.get("payload") or {}).get("answer_sha256")
        if not want:
            continue
        leitor = ev["principal"].split(":")[1]
        rnd = (ev.get("payload") or {}).get("round", 1)  # D44: a later round's answers live in readings/ronda<n>/
        f = (root / f"ronda{rnd}" if rnd != 1 else root) / reading_dir(ev["assertion"]) / f"leitor-{leitor}.json"
        if not f.exists():
            out.append(("READ", f"{ev['id']}: answer file {f.relative_to(root)} missing for {ev['assertion']}"))
            continue
        try:
            doc = json.loads(f.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            out.append(("READ", f"{ev['id']}: {f.relative_to(root)} unreadable: {exc}"))
            continue
        got = hashlib.sha256(str(doc.get("answer", "")).encode("utf-8")).hexdigest()
        if got != want or doc.get("sha256") != want:
            out.append(("READ", f"{ev['id']}: {f.relative_to(root)} does not hash to the sha256 the log recorded ({want[:12]}...)"))


def check_seal(store, out, casos_root=None, held_out=None, train_files=None):
    """SEAL (§8 replay): the measurement's raw annotations (governance/readings/casos/**) and law/HELD-OUT.json are
    sealed in the log by a ferramenta (tools/measure.py seal: assertion_type caso_referencia, assertion selo:casos:<n>,
    payload {index_sha256, held_out_sha256, files}). The newest seal must match governance/readings/casos/INDEX.json
    (every annotation file listed with its sha256, none unlisted) and the current HELD-OUT.json bytes. Annotations
    without a seal are not evidence: with files present and no seal, SEAL fails."""
    gov = store.governance_dir
    if gov is None:
        return
    casos = Path(casos_root) if casos_root else gov / "readings" / "casos"
    held = Path(held_out) if held_out else ROOT / "law/HELD-OUT.json"
    files = sorted(p for p in casos.rglob("*.json") if p.name != "INDEX.json") if casos.exists() else []
    seals = [ev for _, ev in store.events if ev["action"] == "propose" and ev["assertion_type"] == "caso_referencia" and str(ev["assertion"]).startswith("selo:casos:")]
    if not files and not seals:
        return
    if files and not seals:
        out.append(("SEAL", f"{len(files)} annotation files under {casos.name}/ and no seal event in the log"))
        return
    seal = seals[-1]["payload"]
    index_path = casos / "INDEX.json"
    if not index_path.exists():
        out.append(("SEAL", "governance/readings/casos/INDEX.json missing"))
        return
    index = json.loads(index_path.read_text(encoding="utf-8"))
    if hashlib.sha256(canonical_json(index).encode("utf-8")).hexdigest() != seal.get("index_sha256"):
        out.append(("SEAL", f"INDEX.json does not hash to the sealed index_sha256 ({seals[-1]['id']})"))
    listed = index.get("files", {})
    for f in files:
        rel = str(f.relative_to(casos))
        if rel not in listed:
            out.append(("SEAL", f"{rel}: annotation file not in the sealed index"))
        elif hashlib.sha256(f.read_bytes()).hexdigest() != listed[rel]:
            out.append(("SEAL", f"{rel}: annotation file changed after it was sealed"))
    for rel in listed:
        if not (casos / rel).exists():
            out.append(("SEAL", f"{rel}: sealed annotation file missing"))
    if held.exists() and hashlib.sha256(held.read_bytes()).hexdigest() != seal.get("held_out_sha256"):
        out.append(("SEAL", f"{held.name} changed after the newest seal ({seals[-1]['id']})"))
    # D40: the training reservation and the training index are sealed by the same event once they exist (the
    # repository's own files against the repository's own log; another store passes its paths explicitly)
    if train_files is not None or Path(gov).resolve() == (ROOT / "governance").resolve():
        train_held, train_index = train_files or (ROOT / "law/TRAIN-HELD-OUT.json", ROOT / "training/data/INDEX.json")
        if train_held.exists() and hashlib.sha256(train_held.read_bytes()).hexdigest() != seal.get("train_held_out_sha256"):
            out.append(("SEAL", f"{train_held.name} not sealed, or changed after the newest seal ({seals[-1]['id']})"))
        aval = ROOT / "governance/readings/avaliacao-v1"
        repo_log = Path(gov).resolve() == (ROOT / "governance").resolve()
        aval_files = sorted(p for p in aval.rglob("*") if p.is_file() and p.name != "INDEX.json") if aval.exists() and repo_log else []
        if aval_files:  # D42: the T3 answers are sealed like the B5 annotations (the repository's own log only)
            aidx_path = aval / "INDEX.json"
            aidx = json.loads(aidx_path.read_text(encoding="utf-8")) if aidx_path.exists() else None
            if aidx is None or hashlib.sha256(canonical_json(aidx).encode("utf-8")).hexdigest() != seal.get("avaliacao_index_sha256"):
                out.append(("SEAL", f"governance/readings/avaliacao-v1/INDEX.json missing, not sealed, or changed after the newest seal ({seals[-1]['id']})"))
            else:
                for f in aval_files:
                    rel = str(f.relative_to(aval))
                    if aidx["files"].get(rel) != hashlib.sha256(f.read_bytes()).hexdigest():
                        out.append(("SEAL", f"avaliacao-v1/{rel}: not in the sealed index or changed after it"))
                for rel in aidx["files"]:
                    if not (aval / rel).exists():
                        out.append(("SEAL", f"avaliacao-v1/{rel}: sealed answer file missing"))
        if train_index.exists():
            idx = json.loads(train_index.read_text(encoding="utf-8"))
            if hashlib.sha256(canonical_json(idx).encode("utf-8")).hexdigest() != seal.get("training_index_sha256"):
                out.append(("SEAL", f"training/data/INDEX.json not sealed, or changed after the newest seal ({seals[-1]['id']})"))


def check_training(store, out, training_dir, held_path):
    """TRAIN (phase 4, T1): training/data is the generator's output over this store and this reservation. INDEX.json and
    every file it lists must be what tools/make_training.generate() writes (byte for byte), every listed file must hash
    to its sha256, no file may be unlisted, and no example of any train.jsonl may name a source inside a reserved article
    (read independently of the generator, from the stored files and law/TRAIN-HELD-OUT.json)."""
    data = Path(training_dir) / "data"
    index_path = data / "INDEX.json"
    if not index_path.exists():
        return
    if not Path(held_path).exists():
        out.append(("TRAIN", f"{index_path}: training data without its reservation file {held_path}"))
        return
    held = json.loads(Path(held_path).read_text(encoding="utf-8"))
    sys.path.insert(0, str(ROOT / "tools"))
    import make_training  # noqa: E402  (tools/make_training.py: the generator; no model, no network)
    readings = (store.governance_dir / "readings") if store.governance_dir is not None else None
    again = make_training.generate(store, held, readings)
    stored_index = index_path.read_bytes()
    if stored_index != again["INDEX.json"]:
        out.append(("TRAIN", f"{index_path}: not what tools/make_training.py regenerates from the store and the reservation"))
    index = json.loads(stored_index)
    listed = set(index.get("files", {}))
    for rel, meta in index.get("files", {}).items():
        f = data / rel
        if not f.exists():
            out.append(("TRAIN", f"{rel}: listed in INDEX.json and missing"))
            continue
        b = f.read_bytes()
        if hashlib.sha256(b).hexdigest() != meta.get("sha256"):
            out.append(("TRAIN", f"{rel}: does not hash to its INDEX.json sha256"))
        if again.get(rel) is not None and b != again[rel]:
            out.append(("TRAIN", f"{rel}: not what the generator writes"))
    for f in sorted(p for p in data.rglob("*") if p.is_file() and p.name not in ("INDEX.json", "REPORT.md")):
        if str(f.relative_to(data)) not in listed:
            out.append(("TRAIN", f"{f.relative_to(data)}: file not listed in INDEX.json"))
    from engine.canon import canonical as _canon, sha256_text as _sha
    if _sha(_canon(held.get("definition"))) != held.get("sha256"):
        out.append(("TRAIN", f"{held_path}: its definition no longer hashes to the sha256 recorded when it was declared"))
    units = set(make_training.article_map(make_training.current_passages(store)).values())
    expect = sorted({a for a in units if make_training.by_hash(a)} | set(held.get("definition", {}).get("by_b3", {}).get("articles", [])))
    if held.get("reserved_articles") != expect:
        out.append(("TRAIN", f"{held_path}: reserved_articles is not the declared rule (by_hash over the store's articles + by_b3)"))
    reserved = set(held.get("reserved_articles", []))
    art_path = data / "ARTICLE-OF.json"
    article_of = json.loads(art_path.read_text(encoding="utf-8")) if art_path.exists() else {}
    for f in sorted(data.glob("*/train.jsonl")):
        for n, line in enumerate(f.read_text(encoding="utf-8").splitlines(), 1):
            if not line.strip():
                continue
            ex = json.loads(line)
            hit = [s for s in ex.get("sources", []) if article_of.get(s.split("@")[0]) in reserved]
            if hit:
                out.append(("TRAIN", f"{f.relative_to(data)}:{n} ({ex.get('id')}): train example touches reserved article(s) {hit[:3]}"))


def check_training_v2(store, out, training_dir, held_path, sub="data-v2", module="make_conditions"):
    """TRAIN (phase 5, D46; phase 6, D47): training/data-v2 (tools/make_conditions.py) and training/data-v3
    (tools/make_regimes.py) are their generator's output over this store and reservation, byte for byte, nothing
    unlisted, and no train example's source is in a reserved article (read from the reservation)."""
    import importlib
    data = Path(training_dir) / sub
    if not (data / "INDEX.json").exists():
        return
    held = json.loads(Path(held_path).read_text(encoding="utf-8"))
    sys.path.insert(0, str(ROOT / "tools"))
    gen = importlib.import_module(module)  # no model, no network
    import make_training  # noqa: E402
    again = gen.generate(store, held)
    for rel, b in again.items():
        f = data / rel
        if not f.exists() or f.read_bytes() != b:
            out.append(("TRAIN", f"{sub}/{rel}: not what tools/{module}.py regenerates from the store and the reservation"))
    for f in sorted(p for p in data.rglob("*") if p.is_file()):
        if str(f.relative_to(data)) not in again:
            out.append(("TRAIN", f"{sub}/{f.relative_to(data)}: file the generator does not write"))
    art_of = make_training.article_map(make_training.current_passages(store))
    reserved = set(held.get("reserved_articles", []))
    for f in sorted(data.glob("*/train.jsonl")):
        for n, line in enumerate(f.read_text(encoding="utf-8").splitlines(), 1):
            ex = json.loads(line)
            hit = [x for x in ex.get("sources", []) if art_of.get(x.split("@")[0], x) in reserved]
            if hit:
                out.append(("TRAIN", f"{sub}/{f.relative_to(data)}:{n} ({ex.get('id')}): train example touches reserved article(s) {hit[:3]}"))


def training_dirs(roots):
    """(training dir, reservation file) pairs for a store: <root>/training for any root that holds one (a fixture store
    keeps its reservation inside it); the repository's training/ with law/TRAIN-HELD-OUT.json for the repository store (law/ + rules/ + governance/)."""
    out = []
    for r in roots:
        t = Path(r) / "training"
        if (t / "data/INDEX.json").exists():
            out.append((t, t / "TRAIN-HELD-OUT.json"))
    if {Path(r).resolve() for r in roots} == {Path(r).resolve() for r in STORES["repo"]} and (ROOT / "training/data/INDEX.json").exists():
        out.append((ROOT / "training", ROOT / "law/TRAIN-HELD-OUT.json"))
    return out


def check_measure():
    """BENCH and MEAS (B5), once over the repository: law/HELD-OUT.json still hashes to its sha256; a package built after
    frozen_at holds no rule whose log events name a held-out unit; every reports/measure/<date>.json is what
    tools/measure.py recomputes from the stored answers (the gate imports the tool's arithmetic, never a reader)."""
    out = []
    held = ROOT / "law/HELD-OUT.json"
    if not held.exists():
        return out
    from engine.canon import canonical, sha256_text
    doc = json.loads(held.read_text(encoding="utf-8"))
    if sha256_text(canonical(doc["definition"])) != doc["sha256"]:
        out.append(("BENCH", "law/HELD-OUT.json: its definition no longer hashes to the sha256 recorded when it was frozen"))
    sys.path.insert(0, str(ROOT / "tools"))
    import measure  # noqa: E402  (tools/measure.py: the report's arithmetic; no model)
    stores = [d for d in ("data", "fixtures/measure") if (ROOT / d).exists()]
    held_units = set()
    for d in stores:
        st = measure.load(d)
        for u in measure.units(st):
            if measure.is_held_out(measure.case_values(st, u), doc):
                held_units.add(u["id"])
    repo = Store([ROOT / "law", ROOT / "rules", ROOT / "governance"]).load()
    for pk in current_of(repo, "pacote").values():
        if pk["built_at"][:10] <= doc["frozen_at"]:
            continue
        named = {r["id"] for r in pk["rules"]}
        for _, ev in repo.events:
            if ev["assertion"] in named and any(u in json.dumps(ev.get("payload") or {}) for u in held_units):
                out.append(("BENCH", f"{pk['id']}: built after frozen_at {doc['frozen_at']} and holds {ev['assertion']}, whose event {ev['id']} names a held-out unit"))
    for f in sorted((ROOT / "reports/measure").glob("*.json")) if (ROOT / "reports/measure").exists() else []:
        stored = json.loads(f.read_text(encoding="utf-8"))
        if f.name.startswith("factos-"):  # phase 8 (D50): a person's question -> facts, generated and hand-written (tools/measure_user_facts.py)
            import measure_user_facts  # noqa: E402  (no model: it reads the stored answers)
            again = measure_user_facts.report(stored["date"], only={r for s in stored["sets"].values() for r in s["readers"]})
            if json.dumps(again, sort_keys=True, ensure_ascii=False) != json.dumps(stored, sort_keys=True, ensure_ascii=False):
                out.append(("MEAS", f"{f.relative_to(ROOT)}: not what tools/measure_user_facts.py recomputes from the stored answers"))
            continue
        if f.name.startswith("pergunta-"):  # phase 7 (D49): condicoes_pergunta held out, base / v3 / v4 (tools/measure_question_conditions.py)
            import measure_question_conditions  # noqa: E402  (no model: it reads the stored answers)
            again = measure_question_conditions.report(stored["date"])
            if json.dumps(again, sort_keys=True, ensure_ascii=False) != json.dumps(stored, sort_keys=True, ensure_ascii=False):
                out.append(("MEAS", f"{f.relative_to(ROOT)}: not what tools/measure_question_conditions.py recomputes from the stored answers"))
            continue
        if f.name.startswith("regimes-"):  # phase 6 (D47): the selector tasks held out, base / v2 / v3 (tools/measure_regimes.py)
            import measure_regimes  # noqa: E402  (no model: it reads the stored answers)
            again = measure_regimes.report(stored["date"], only={r for t in stored["tasks"].values() for r in t["readers"]})
            if json.dumps(again, sort_keys=True, ensure_ascii=False) != json.dumps(stored, sort_keys=True, ensure_ascii=False):
                out.append(("MEAS", f"{f.relative_to(ROOT)}: not what tools/measure_regimes.py recomputes from the stored answers"))
            continue
        if f.name.startswith("condicoes-"):  # phase 5 (D46): condicoes_texto held out, base / v1 / v2 (tools/measure_conditions.py)
            import measure_conditions  # noqa: E402  (no model: it reads the stored answers)
            again = measure_conditions.report(stored["date"], only=set(stored["readers"]))
            if json.dumps(again, sort_keys=True, ensure_ascii=False) != json.dumps(stored, sort_keys=True, ensure_ascii=False):
                out.append(("MEAS", f"{f.relative_to(ROOT)}: not what tools/measure_conditions.py recomputes from the stored answers"))
            continue
        if f.name.startswith("amalia-"):  # phase 4 T3: the reader before / after its adapter (tools/measure_reader.py)
            import measure_reader  # noqa: E402  (no model: it reads the stored answers)
            again = measure_reader.report(stored["date"])
            if json.dumps(again, sort_keys=True, ensure_ascii=False) != json.dumps(stored, sort_keys=True, ensure_ascii=False):
                out.append(("MEAS", f"{f.relative_to(ROOT)}: not what tools/measure_reader.py recomputes from the stored answers"))
            continue
        seals = [ev["at"] for _, ev in repo.events if str(ev["assertion"]).startswith("selo:casos:")]
        again = measure.report(stored["store"], stored["date"], rules_known_at=max(seals) if seals else None)  # D44: rules as sealed
        if json.dumps(again, sort_keys=True, ensure_ascii=False) != json.dumps(stored, sort_keys=True, ensure_ascii=False):
            out.append(("MEAS", f"{f.relative_to(ROOT)}: not what tools/measure.py recomputes from the stored answers"))
    return out


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
    meas = check_measure()
    for code, msg in meas:
        print(f"FAIL {code}  {msg}")
    print(f"measurement (BENCH/MEAS): {'ok' if not meas else 'FAILED'}")
    failed |= bool(meas)
    for name, expect, codes in run_broken(ROOT / "fixtures/valid", ROOT / "fixtures/broken"):
        ok = bool(expect) and expect <= codes
        print(f"broken {name}: expected {sorted(expect)} got {sorted(codes)} -> {'ok' if ok else 'NOT REFUSED'}")
        failed |= not ok
    print("verify:", "FAILED" if failed else "ok", f"({VERSION}; no model called)")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
