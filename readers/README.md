# readers/ — the code that runs a model (DECISIONS D38)

Readers propose; the code decides. These scripts only turn prompt files into answer files:

- `leitor_a_modal.py` — leitor:a (family A) on Modal, vLLM with guided JSON, temperature 0.
- `leitor_b_cli.py` — leitor:b (family B) by its command-line client, read-only, ephemeral, in an empty directory.

Nothing in `engine/`, `tools/` or `verify.py` imports or runs them (verify's code guard refuses a model import there).
The answers they write under `governance/readings/` are data: `tools/read_rules.py record` turns them into log events,
and `tools/measure.py` recomputes the measurement from them.
