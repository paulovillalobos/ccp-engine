"""FILL-PLAN B2c — red until the municipal pilot is reported.

Done when: law/MUNICIPIOS-PILOTO.md has one row per pilot município (10; chosen by BASE volume when the extractor has
delivered anúncios, else Lisboa, Porto, Vila Nova de Gaia, Braga, Coimbra, Sintra, Loures, Cascais, Funchal, Ponta
Delgada) with the records found, captured and with text, and an estimate for the 308 municípios."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
DEFAULT = ("Lisboa", "Porto", "Vila Nova de Gaia", "Braga", "Coimbra", "Sintra", "Loures", "Cascais", "Funchal", "Ponta Delgada")


def test_pilot_report_names_ten_municipios_with_counts_and_the_308_estimate():
    text = (ROOT / "law/MUNICIPIOS-PILOTO.md").read_text(encoding="utf-8")
    rows = [l for l in text.splitlines() if l.startswith("| ") and re.search(r"\| *[0-9]+ *\| *[0-9]+ *\| *[0-9]+ *\|", l)]
    names = [r.split("|")[1].strip() for r in rows]
    assert len(names) == 10, names
    by_volume = "volume BASE" in text
    assert by_volume or sorted(names) == sorted(DEFAULT), names
    assert re.search(r"\b308\b", text) and "estimativa" in text.lower()
