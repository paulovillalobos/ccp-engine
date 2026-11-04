"""D70: the EU procurement directives in Portuguese, every consolidated version the Publications Office serves (and the
OJ text as adopted where it serves one), read into passages with their dates. 2014/24's deadlines are the directive's
words from its entry into force; its threshold follows each consolidation; 2004/18 closes on the day 2014/24 repeals it."""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT)); sys.path.insert(0, str(ROOT / "tools"))
import read_rules as rr  # noqa: E402
from engine import extract  # noqa: E402
from engine.store import Store  # noqa: E402

STORE = Store([ROOT / "law"]).load()
DIRECTIVES = ("eu-1989-665", "eu-1992-13", "eu-2004-17", "eu-2004-18", "eu-2009-81", "eu-2014-23", "eu-2014-24", "eu-2014-25")


def test_every_capture_reads_and_is_a_norma():
    raws = [r for r in STORE.objects["raw"] if r["kind"] == "diretiva" and r["revision"] == 1]
    assert len(raws) == 66
    for r in raws:
        text = extract.eurlex_consolidated(STORE.raw_path(r).read_bytes())
        assert text.count("\nArtigo ") >= 5, r["id"]
        assert STORE.current(r["id"])["text"]["extractor"] == "eurlex-consolidated@1"
    for short in DIRECTIVES:
        n = STORE.current(f"norma:{short}")
        assert n["jurisdiction"] == "UE" and n["eli"].startswith("https://data.europa.eu/eli/dir/")


def test_a_deadline_as_the_directive_states_it():
    p = STORE.current("eu-2014-24:art27.1")
    v = rr.version_at(p, "2026-10-01")
    assert "O prazo mínimo de receção das propostas é de 35 dias a contar da data de envio do anúncio de concurso." in v["text"]
    assert p["versions"][0]["valid_from"] == "2014-04-17"  # the OJ of 28.3.2014, «no vigésimo dia seguinte ao da sua publicação»
    assert any(g["id"] == "eu-2014-24:art27.1@2014-04-17" and g["effect"] == "entra_em_vigor" for g in STORE.objects["vigencia"])


def test_a_threshold_follows_each_consolidation():
    p = STORE.current("eu-2014-24:art4.b")
    seen = {d: rr.version_at(p, d)["text"].split(" EUR")[0][3:] for d in ("2015-06-01", "2020-06-01", "2024-06-01", "2026-10-01")}
    assert seen == {"2015-06-01": "134 000", "2020-06-01": "139 000", "2024-06-01": "143 000", "2026-10-01": "140 000"}


def test_a_repealed_directive_closes_on_the_repeal_date():
    p = STORE.current("eu-2004-18:art38.2")
    assert "52 dias" in p["versions"][0]["text"]
    assert p["versions"][-2]["valid_to"] == "2016-04-18" and p["versions"][-1]["revoked"] and p["versions"][-1]["valid_from"] == "2016-04-18"
    v = next(g for g in STORE.objects["vigencia"] if g["id"] == "eu-2004-18:art38.2@2016-04-18")
    assert v["effect"] == "revoga" and v["altered_by"] == "norma:eu-2014-24" and "é revogada com efeitos a partir de 18 de abril de 2016" in v["note"]["quote"]
    assert rr.version_at(p, "2026-10-01")["revoked"]


def test_the_build_report_says_what_it_could_not_read():
    report = json.loads((ROOT / "law/build-report.json").read_text(encoding="utf-8"))
    assert set(k for k in report["not_structured"] if k.startswith("raw:eur-lex")) == {"raw:eur-lex:diretiva:eu-2014-23-20140328"}
