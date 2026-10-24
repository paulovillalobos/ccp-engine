"""Entities: NIF as key, name candidates per country, links with provenance. Linked, never merged (invariant 9).

    candidate_id(country, name) -> str          ent:cand:<ISO2>:<slug of name>; the same name gives the same id
    nif_id(nif) -> str                          ent:nif:<9 digits>; raises on anything else
    propose_link(from_id, to_id, proponent, method, evidence, at, evento, recorded_at) -> link dict (state proposed)
        proponent is required and is a principal id (invariant 4; verify I04 checks it is registered)
        method nif_exact is the parser's; name_ai is a model's (needs evento); person is a human's
    settle(link, recorded_at) -> dict           a NEW revision with state settled (the old one stays in the store)
    mark_stale(link, reason, recorded_at) -> dict   a NEW revision with state stale and the reason; nothing is deleted
    links_to(links, entity_id, known_at=None) -> list   current links pointing at an entity as known at known_at
    merge(*_)                                   always raises: two ids stay two ids, joined by links

Every function returns a new dict; none mutates its input; none writes a file (the store does).
"""
import re
import unicodedata

VERSION = "ccp-entities-0.1"
METHODS = ("nif_exact", "name_ai", "person")


def _slug(name: str) -> str:
    s = unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode().lower()
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s or "sem-nome"


def candidate_id(country: str, name: str) -> str:
    if not re.fullmatch(r"[A-Z]{2}", country or ""):
        raise ValueError(f"country must be ISO-3166 alpha-2, got {country!r}")
    return f"ent:cand:{country}:{_slug(name)}"


def nif_id(nif: str) -> str:
    if not re.fullmatch(r"[0-9]{9}", nif or ""):
        raise ValueError(f"NIF must be nine digits, got {nif!r}")
    return f"ent:nif:{nif}"


def propose_link(link_id, from_id, to_id, proponent, method, evidence, at, evento, recorded_at) -> dict:
    if not proponent:
        raise ValueError("a link needs a proponent (invariant 4)")
    if method not in METHODS:
        raise ValueError(f"method must be one of {METHODS}")
    if method == "name_ai" and not evento:
        raise ValueError("a link proposed by a model names its governance event")
    return {"id": link_id, "revision": 1, "recorded_at": recorded_at, "from": from_id, "to": to_id, "proponent": proponent,
            "method": method, "evidence": dict(evidence), "state": "proposed", "at": at, "evento": evento}


def _next(link, recorded_at, **changes) -> dict:
    new = dict(link, **changes)
    new["revision"] = link["revision"] + 1
    new["supersedes"] = link["revision"]
    new["recorded_at"] = recorded_at
    return new


def settle(link, recorded_at) -> dict:
    if link["state"] == "stale":
        raise ValueError("a stale link is not settled; propose a new link")
    return _next(link, recorded_at, state="settled")


def mark_stale(link, reason, recorded_at) -> dict:
    if not reason:
        raise ValueError("marking a link stale needs a reason")
    return _next(link, recorded_at, state="stale", stale=True, stale_reason=reason)


def links_to(links, entity_id, known_at=None) -> list:
    latest = {}
    for l in sorted(links, key=lambda l: (l["id"], l["revision"])):
        if l["to"] == entity_id and (known_at is None or l["recorded_at"] <= known_at):
            latest[l["id"]] = l
    return [l for l in latest.values() if l["state"] != "stale"]


def merge(*_args, **_kwargs):
    raise NotImplementedError("entities are linked, never merged (invariant 9); propose a link and settle it")
