Owned by the extractor. `raw/<source>/` holds raw records with sha256; `facts/` holds facts, assertions, units and
candidate entities in the store layout of schemas/ (`facts/<type>/*.json` or `.jsonl`). verify.py validates everything
here against the schemas. The builder does not write here.
