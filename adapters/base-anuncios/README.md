BASE anúncios dump (dados.gov.pt, IMPIC, weekly JSON) -> `data/`. Owned by the extractor.

- `mapping.json`: the mapping declared as data: the `adaptador` rows (source field -> canonical field, transform, enum
  map), the record key, which notice types are procedures, the NIF table that decides an entity's type, and the
  canonical fields the dump does not give, each with the reason.
- `adapter.py`: the code. `build` reads the downloaded file and writes the store objects; `check` rebuilds everything
  from the stored download and compares byte for byte; `register` registers this file as a ferramenta and proposes the
  adaptador in the governance log.
- `build.json`: the arguments of the build that produced `data/` (URL, captured_at, recorded_at, principal, sha256).
- `COVERAGE.md`: records in, procedures out, coverage per canonical field and month, unmapped records by reason.
- `SCHEMA-PROPOSAL.md`: what does not fit the schemas or the gate, for the builder.

Reproduce (the bytes are not in git; download the resource named in build.json once, check its sha256, then):

```
.venv/bin/python -I adapters/base-anuncios/adapter.py build --dump PATH --url URL --captured-at T --recorded-at T --principal P
.venv/bin/python -I adapters/base-anuncios/adapter.py check
```
