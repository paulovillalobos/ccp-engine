"""Governance: the append-only, hash-chained log of who proposed, reviewed, approved, disputed and adjudicated (read side:
replay; the write side — propose, review, approve, dispute, adjudicate — is added in A4).

    governance/principals.json   who may act: id, kind (human | ai | parser | system), family, role, retired
    governance/events.jsonl      one event per line (canonical JSON), prev = sha256 of the previous line, seq 1, 2, 3 ...
    governance/state.json        the replay, never edited by hand (written by A4's Log.write_state)

Rules, enforced on replay (engine/verify.py code I04 unless stated) and again by the write side:
  - the log is a hash chain with consecutive sequence numbers; nothing is edited or removed (I09)
  - only registered, non-retired principals act, within their kind's CAPABILITIES
  - approve and adjudicate are human actions (invariant 4); machines never produce approval
  - approve, reject, dispute and adjudicate carry a reason; a review carries question, independence and verdict
  - a proposer never reviews or approves its own revision; an adjudicator is never the disputant
  - review, approve, reject and correct name the exact current revision (expected_revision)
  - a reading of the law (assertion_type regra) is never human-approved: it is `settled` when a blind review/uphold
    comes from a principal whose family differs from the proposer's (invariant 5); any other uphold gives `ai_reviewed`
  - product_rule, adaptador, link, afirmacao_conversao and caso_referencia settle by human approve (invariant 12 for product_rule)

    replay(events, principals) -> Replay   state per assertion, open disputes, errors as (code, message)
    head(events) -> str                    sha256 of the last canonical line (64 zeros when empty)
"""
from engine.canon import canonical, sha256_text

VERSION = "ccp-governance-0.1"
GENESIS = "0" * 64
CAPABILITIES = {
    "parser": {"propose", "correct"},
    "ai": {"propose", "correct", "review"},
    "system": {"invalidate"},
    "human": {"propose", "correct", "review", "approve", "reject", "dispute", "adjudicate", "invalidate"},
}
LEGAL_TYPES = {"regra"}
APPROVABLE_TYPES = {"product_rule", "adaptador", "link", "afirmacao_conversao", "caso_referencia"}
NEEDS_REASON = {"approve", "reject", "dispute", "adjudicate"}
NEEDS_CURRENT_REVISION = {"review", "approve", "reject", "correct"}


class Replay:
    def __init__(self):
        self.assertions = {}   # (type, id) -> {"revision", "proposer", "family", "reviews": [...], "state"}
        self.disputes = {}     # disputa id -> {"disputant", "veredicto", "state", "adjudicator"}
        self.errors = []
        self.head = GENESIS
        self.count = 0

    def state_of(self, type_, ident):
        a = self.assertions.get((type_, ident))
        return a["state"] if a else None


def head(events) -> str:
    if not events:
        return GENESIS
    line = events[-1][0] if isinstance(events[-1], tuple) else canonical(events[-1])
    return sha256_text(line)


def replay(events, principals) -> Replay:
    """events: list of (line, dict) or dicts; principals: the principals.json object."""
    rp = Replay()
    plist = (principals or {}).get("principals", [])
    kinds = {p["id"]: p for p in plist}
    prev = GENESIS
    for n, item in enumerate(events, 1):
        line, ev = item if isinstance(item, tuple) else (canonical(item), item)
        if ev.get("seq") != n:
            rp.errors.append(("I09", f"event {n}: seq {ev.get('seq')} breaks the sequence"))
        if ev.get("prev") != prev:
            rp.errors.append(("I09", f"event {n}: prev does not hash the previous line (chain broken)"))
        prev = sha256_text(line)
        rp.head, rp.count = prev, n
        pid, action, atype, aid = ev.get("principal"), ev.get("action"), ev.get("assertion_type"), ev.get("assertion")
        p = kinds.get(pid)
        if p is None:
            rp.errors.append(("I04", f"event {n}: principal {pid} is not registered"))
            continue
        if p.get("retired"):
            rp.errors.append(("I04", f"event {n}: principal {pid} is retired"))
        if action not in CAPABILITIES.get(p["kind"], set()):
            rp.errors.append(("I04", f"event {n}: {pid} ({p['kind']}) may not {action}"))
        if action in NEEDS_REASON and not ev.get("reason"):
            rp.errors.append(("I04", f"event {n}: {action} without a reason"))
        if action in ("approve", "adjudicate") and p["kind"] != "human":
            rp.errors.append(("I04", f"event {n}: {action} by {pid}: only a person approves or adjudicates"))
        key = (atype, aid)
        if action == "propose":
            if key in rp.assertions:
                rp.errors.append(("I04", f"event {n}: {aid} proposed twice; use correct for a new revision"))
            rp.assertions[key] = {"revision": 1, "proposer": pid, "family": p["family"], "reviews": [], "state": "proposed", "events": [n]}
            continue
        if action == "dispute":
            did = (ev.get("payload") or {}).get("disputa")
            if not did:
                rp.errors.append(("I04", f"event {n}: dispute without payload.disputa"))
                continue
            rp.disputes[did] = {"disputant": pid, "veredicto": aid, "state": "open", "adjudicator": None, "events": [n]}
            continue
        if action == "adjudicate":
            d = rp.disputes.get(aid)
            if d is None:
                rp.errors.append(("I04", f"event {n}: adjudicate on unknown dispute {aid}"))
                continue
            if d["disputant"] == pid:
                rp.errors.append(("I04", f"event {n}: {pid} adjudicates their own dispute"))
            if d["state"] != "open":
                rp.errors.append(("I04", f"event {n}: dispute {aid} already adjudicated"))
            d.update(state="adjudicated", adjudicator=pid, outcome=ev.get("outcome"))
            d["events"].append(n)
            continue
        a = rp.assertions.get(key)
        if a is None:
            rp.errors.append(("I04", f"event {n}: {action} on unknown assertion {atype} {aid}"))
            continue
        a["events"].append(n)
        if action in NEEDS_CURRENT_REVISION and ev.get("expected_revision") != a["revision"]:
            rp.errors.append(("I04", f"event {n}: {action} names revision {ev.get('expected_revision')}, current is {a['revision']}"))
        if action == "correct":
            a.update(revision=a["revision"] + 1, proposer=pid, family=p["family"], reviews=[], state="proposed")
        elif action == "review":
            if pid == a["proposer"]:
                rp.errors.append(("I04", f"event {n}: {pid} reviews its own proposal {aid}"))
            a["reviews"].append({"by": pid, "family": p["family"], "verdict": ev.get("verdict"), "independence": ev.get("independence")})
            if ev.get("verdict") == "reject":
                a["state"] = "rejected"
            elif ev.get("verdict") == "uphold" and a["state"] != "rejected":
                blind_other = ev.get("independence") == "blind" and p["family"] != a["family"]
                if atype in LEGAL_TYPES:
                    a["state"] = "settled" if blind_other else ("ai_reviewed" if a["state"] != "settled" else "settled")
                elif a["state"] == "proposed":
                    a["state"] = "ai_reviewed"
        elif action == "approve":
            if pid == a["proposer"]:
                rp.errors.append(("I04", f"event {n}: {pid} approves its own proposal {aid}"))
            if atype in LEGAL_TYPES:
                rp.errors.append(("I04", f"event {n}: a reading of the law ({aid}) is never human-approved; it settles by a blind reader of another family"))
            elif atype in APPROVABLE_TYPES:
                a["state"] = "settled"
            a["approved_by"] = pid
        elif action == "reject":
            a["state"] = "rejected"
        elif action == "invalidate":
            a["state"] = "stale"
    return rp
