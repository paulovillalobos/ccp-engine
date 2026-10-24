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


# ---- write side --------------------------------------------------------------------------------------------------
import fcntl  # noqa: E402
import json  # noqa: E402
from contextlib import contextmanager  # noqa: E402
from pathlib import Path  # noqa: E402

from engine import schema  # noqa: E402


class GovernanceError(ValueError):
    pass


class Log:
    """The write side. Every method builds one event, validates it against evento.schema.json, replays the whole log with
    it appended and refuses to write if the replay reports a new error. One writer at a time (events.lock).

        Log(directory)                      reads principals.json and events.jsonl (both may be absent: empty log)
        .propose(principal, assertion_type, assertion, payload, at)
        .correct(principal, assertion_type, assertion, expected_revision, payload, reason, at)
        .review(principal, assertion_type, assertion, expected_revision, question, independence, verdict, at, payload=None)
        .approve(principal, assertion_type, assertion, expected_revision, reason, at)      human only
        .reject(principal, assertion_type, assertion, expected_revision, reason, at)
        .dispute(principal, veredicto, disputa, reason, at)                                 human only (capability)
        .adjudicate(principal, disputa, outcome, reason, at)                                human only, not the disputant
        .invalidate(principal, assertion_type, assertion, reason, at)                        system or human
        .head() -> str                       sha256 of the last line (GENESIS when empty) — what manifests record
        .replay() -> Replay
        .write_state()                       governance/state.json: the replay, for people to read; never a source
    Each method returns the event id (evento:n)."""

    def __init__(self, directory):
        self.dir = Path(directory)
        self.dir.mkdir(parents=True, exist_ok=True)
        pfile = self.dir / "principals.json"
        self.principals = json.loads(pfile.read_text(encoding="utf-8")) if pfile.exists() else {"principals": []}
        self.events = []
        efile = self.dir / "events.jsonl"
        if efile.exists():
            for line in efile.read_text(encoding="utf-8").splitlines():
                if line.strip():
                    self.events.append((line, json.loads(line)))

    @contextmanager
    def _lock(self):
        with open(self.dir / "events.lock", "w") as fh:
            fcntl.flock(fh, fcntl.LOCK_EX)
            try:
                yield
            finally:
                fcntl.flock(fh, fcntl.LOCK_UN)

    def head(self) -> str:
        return head(self.events)

    def replay(self) -> Replay:
        return replay(self.events, self.principals)

    def _record(self, **fields) -> str:
        with self._lock():
            seq = len(self.events) + 1
            ev = {"id": f"evento:{seq}", "seq": seq, "at": fields.pop("at"), "prev": self.head(), "principal": fields.pop("principal"),
                  "action": fields.pop("action"), "assertion_type": fields.pop("assertion_type"), "assertion": fields.pop("assertion"),
                  "expected_revision": fields.pop("expected_revision", None), "payload": fields.pop("payload", None) or {},
                  "reason": fields.pop("reason", None), "question": fields.pop("question", None), "independence": fields.pop("independence", None),
                  "verdict": fields.pop("verdict", None), "outcome": fields.pop("outcome", None)}
            errors = schema.validate("evento", ev)
            if errors:
                raise GovernanceError(f"event refused by schema: {errors[0]}")
            before = {m for _, m in self.replay().errors}
            line = canonical(ev)
            after = replay(self.events + [(line, ev)], self.principals).errors
            new = [m for _, m in after if m not in before]
            if new:
                raise GovernanceError(f"event refused: {new[0]}")
            with open(self.dir / "events.jsonl", "a", encoding="utf-8") as fh:
                fh.write(line + "\n")
            self.events.append((line, ev))
            return ev["id"]

    def propose(self, principal, assertion_type, assertion, payload, at):
        return self._record(principal=principal, action="propose", assertion_type=assertion_type, assertion=assertion, payload=payload, at=at)

    def correct(self, principal, assertion_type, assertion, expected_revision, payload, reason, at):
        return self._record(principal=principal, action="correct", assertion_type=assertion_type, assertion=assertion, expected_revision=expected_revision, payload=payload, reason=reason, at=at)

    def review(self, principal, assertion_type, assertion, expected_revision, question, independence, verdict, at, payload=None):
        return self._record(principal=principal, action="review", assertion_type=assertion_type, assertion=assertion, expected_revision=expected_revision,
                            question=question, independence=independence, verdict=verdict, payload=payload, at=at)

    def approve(self, principal, assertion_type, assertion, expected_revision, reason, at):
        return self._record(principal=principal, action="approve", assertion_type=assertion_type, assertion=assertion, expected_revision=expected_revision, reason=reason, at=at)

    def reject(self, principal, assertion_type, assertion, expected_revision, reason, at):
        return self._record(principal=principal, action="reject", assertion_type=assertion_type, assertion=assertion, expected_revision=expected_revision, reason=reason, at=at)

    def dispute(self, principal, veredicto, disputa, reason, at):
        return self._record(principal=principal, action="dispute", assertion_type="veredicto", assertion=veredicto, payload={"disputa": disputa}, reason=reason, at=at)

    def adjudicate(self, principal, disputa, outcome, reason, at):
        return self._record(principal=principal, action="adjudicate", assertion_type="disputa", assertion=disputa, expected_revision=1, outcome=outcome, reason=reason, at=at)

    def invalidate(self, principal, assertion_type, assertion, reason, at):
        return self._record(principal=principal, action="invalidate", assertion_type=assertion_type, assertion=assertion, reason=reason, at=at)

    def write_state(self) -> Path:
        rp = self.replay()
        state = {"head": rp.head, "events": rp.count, "assertions": {f"{t}|{i}": a for (t, i), a in sorted(rp.assertions.items())}, "disputes": rp.disputes, "errors": rp.errors}
        path = self.dir / "state.json"
        path.write_text(json.dumps(state, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        return path
