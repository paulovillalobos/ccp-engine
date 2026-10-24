"""Schema registry: loads schemas/*.schema.json once and validates any object against the schema of its type.

    TYPES                       the object types (schema file stems) that live in a store, with their directory name
    load() -> Registry          every schema under schemas/, resolvable by its $id
    validator(type) -> Draft202012Validator
    validate(type, obj) -> list[str]   empty when valid; else one message per error, each with its JSON path
    type_of(obj) -> str | None  the type an object claims, from its id prefix (None when unknown)

No network: $ref resolution is local to the registry. No model.
"""
import json
import re
from functools import lru_cache
from pathlib import Path

from jsonschema import Draft202012Validator
from referencing import Registry, Resource

VERSION = "ccp-schema-0.1"
ROOT = Path(__file__).resolve().parent.parent
SCHEMAS = ROOT / "schemas"

# store directory name -> schema stem. Directory names equal schema stems; listed to make the contract explicit.
TYPES = {
    "norma": "norma", "passagem": "passagem", "vigencia": "vigencia", "regra": "regra", "pacote": "pacote",
    "diff": "diff", "raw": "raw", "adaptador": "adaptador", "unidade": "unidade", "entidade": "entidade",
    "alias": "alias", "link": "link", "facto": "facto", "afirmacao": "afirmacao", "conflito": "conflito",
    "documento": "documento", "veredicto": "veredicto", "manifesto": "manifesto", "disputa": "disputa",
    "caso_referencia": "caso_referencia",
}
# Governance lives in <store>/governance/{principals.json,events.jsonl}, validated with these schemas.
GOVERNANCE_TYPES = {"evento": "evento", "principals": "principals"}

ID_PREFIX = [
    (re.compile(r"^norma:"), "norma"), (re.compile(r"^regra:"), "regra"), (re.compile(r"^pacote:"), "pacote"),
    (re.compile(r"^diff:"), "diff"), (re.compile(r"^raw:"), "raw"), (re.compile(r"^adaptador:"), "adaptador"),
    (re.compile(r"^(proc|lote|contrato|mod):"), "unidade"), (re.compile(r"^ent:"), "entidade"),
    (re.compile(r"^alias:"), "alias"), (re.compile(r"^link:"), "link"), (re.compile(r"^facto:"), "facto"),
    (re.compile(r"^afirmacao:"), "afirmacao"), (re.compile(r"^conflito:"), "conflito"), (re.compile(r"^doc:"), "documento"),
    (re.compile(r"^veredicto:"), "veredicto"), (re.compile(r"^evento:"), "evento"), (re.compile(r"^disputa:"), "disputa"),
    (re.compile(r"^ref:"), "caso_referencia"),
    (re.compile(r"^[a-z0-9-]+:[a-z0-9.-]+@\d{4}-\d{2}-\d{2}$"), "vigencia"),
    (re.compile(r"^[a-z0-9-]+:[a-z0-9.-]+$"), "passagem"),
]


@lru_cache(maxsize=1)
def load() -> Registry:
    registry = Registry()
    for path in sorted(SCHEMAS.glob("*.schema.json")):
        schema = json.loads(path.read_text(encoding="utf-8"))
        Draft202012Validator.check_schema(schema)
        registry = registry.with_resource(schema["$id"], Resource.from_contents(schema))
    return registry


@lru_cache(maxsize=None)
def validator(type_: str) -> Draft202012Validator:
    schema = json.loads((SCHEMAS / f"{type_}.schema.json").read_text(encoding="utf-8"))
    return Draft202012Validator(schema, registry=load())


def validate(type_: str, obj) -> list:
    errors = []
    for err in sorted(validator(type_).iter_errors(obj), key=lambda e: list(e.absolute_path)):
        where = "/".join(str(p) for p in err.absolute_path) or "."
        errors.append(f"{where}: {err.message}")
    return errors


def type_of(obj) -> "str | None":
    ident = obj.get("id") if isinstance(obj, dict) else None
    if not isinstance(ident, str):
        return None
    for pattern, type_ in ID_PREFIX:
        if pattern.match(ident):
            return type_
    return None
