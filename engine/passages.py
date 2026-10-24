"""Passages as the engine reads them, and citations written by code (invariant 2).

    passage_text(store, passage_id, version) -> str
        the text of one version of a passage, exactly as stored (raw text at the version's offsets; verify I01)
    cite(store, passage_id, version, start, end) -> citation
        {"passage", "version", "quote", "offsets"}: the quote is passage_text(...)[start:end], written here, never
        supplied by a caller. A reader (a model) only ever supplies passage_id and the span; the code writes the words.
Both raise LookupError when the passage or the version does not exist and ValueError for an empty or out-of-range span.
No network, no model. Copied from rjue-engine's passages module and versioned here.
"""

VERSION = "ccp-passages-0.1"


def _version(store, passage_id, version):
    p = store.current(passage_id)
    if p is None:
        raise LookupError(f"no passage {passage_id}")
    v = next((v for v in p["versions"] if v["version"] == version), None)
    if v is None:
        raise LookupError(f"{passage_id} has no version {version}; versions: {[x['version'] for x in p['versions']]}")
    return v


def passage_text(store, passage_id, version) -> str:
    return _version(store, passage_id, version)["text"]


def cite(store, passage_id, version, start, end) -> dict:
    text = passage_text(store, passage_id, version)
    if not (isinstance(start, int) and isinstance(end, int)) or not 0 <= start < end <= len(text):
        raise ValueError(f"{passage_id}@{version}: span [{start}:{end}] is outside its text of {len(text)} characters")
    return {"passage": passage_id, "version": version, "quote": text[start:end], "offsets": {"start": start, "end": end}}
