`valid/`: one valid object per schema, in the store layout (`valid/<type>/<name>.json`). An extractor can start from
these alone. `broken/<name>/`: an overlay on valid/ that trips exactly one invariant; its `EXPECT` file names the check
code verify.py must fail with.
