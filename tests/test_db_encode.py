"""D55: how db/pg.py spells an object in the compact tables. Offline: the view side (SQL) is checked by `db/pg.py
selftest` and by every load's round trip against the database; here, that encode never drops or bends a key."""
import pytest

from db.pg import encode

AT = "2026-10-26T21:00:00Z"


def fact(**kw):
    o = {"id": "facto:proc-base-1-2026.9:preco_base:base-anuncios", "revision": 1, "recorded_at": AT, "unit": "proc:base:1-2026.9",
         "field": "preco_base", "value": 100, "origin": {"raw": "raw:base-anuncios:anuncio:1-2026.9", "field": "PrecoBase"},
         "adapter": "adaptador:base-anuncios@1", "valid_at": "2026-01-02", "known_at": AT}
    o.update(kw)
    return o


def test_fact_columns_and_derived_id():
    row, names, used = encode("facto", fact())
    assert row["src"] == "base-anuncios" and row["rest"] is None
    assert {"proc:base:1-2026.9", "preco_base", "base-anuncios", "raw:base-anuncios:anuncio:1-2026.9"} <= used


def test_fact_id_that_is_not_derived_is_refused():
    with pytest.raises(ValueError):
        encode("facto", fact(id="facto:something-else:preco_base:base-anuncios"))


def test_what_no_column_says_stays_in_rest():
    origin = {"documento": "doc:" + "a" * 64, "page": 1, "offsets": {"start": 0, "end": 3}, "quote": "abc"}
    row, _, _ = encode("facto", fact(origin=origin, valid_at="2026-01-02T10:00:00Z", supersedes=1))
    assert row["oraw"] is None and row["valid_at"] is None
    assert '"documento"' in row["rest"] and '"valid_at": "2026-01-02T10:00:00Z"' in row["rest"] and '"supersedes": 1' in row["rest"]


def test_null_and_absent_stay_apart():
    unit = {"id": "proc:base:1-2026.9", "revision": 1, "recorded_at": AT, "kind": "proc", "parent": None, "raw": ["raw:x:y:1"], "consumer_ids": {}}
    row, _, _ = encode("unidade", unit)
    assert row["parent"] is None and '"parent": null' in row["rest"]
    raw = {"id": "raw:x:y:1", "revision": 1, "recorded_at": AT, "sha256": "0" * 64, "bytes": "elsewhere/0"}
    row, _, _ = encode("raw", raw)
    assert row["sha256"] is None and '"bytes": "elsewhere/0"' in row["rest"]


def test_envelope_outside_the_schema_is_refused():
    with pytest.raises(ValueError):
        encode("facto", fact(recorded_at="2026-10-26"))
