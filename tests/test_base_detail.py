"""D93: the portal fields of a BASE contract, copied as published and compressed against the fixed dictionary."""
import hashlib
import io
import json
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path[:0] = [str(ROOT / "db"), str(ROOT)]
import base_detail  # noqa: E402

NEW = {"idcontrato": "14730315", "objectoContrato": "Reabilitação do Zimbório", "descContrato": "Reabilitação do Zimbório",
       "adjudicante": [{"nifEntContrato": "502177080", "descEntContrato": "Município de Mafra", "NUTsDesc": "Área Metropolitana de Lisboa"}],
       "CPV": [{"cpvID": "45212350-4", "cpvdescricao": "Edifícios", "cpvValor": 168780.91, "CPVObjeto": "Principal"}],
       "Lotes": [{"numLot": "0", "criterioAdjudicacaoTipo": "Monofator", "NumPropostas": 2}], "precoContratual": 168780.91,
       "dataFechoContrato": "", "PrecoTotalEfetivo": 0.0, "ocorrencias": False, "justifNReducEscrContrato": None, "Ano": 2026,
       "idINCM": "", "nifQualquer": "not a portal field"}
OLD = {"idcontrato": "12014814", "objectoContrato": "Selo", "descContrato": "Selo, outro texto", "dataPublicacao": "04/12/2025",
       "adjudicante": ["600052737 - Serviços de Ação Social"], "cpv": ["72210000-0 - Serviços de programação"], "CritMateriais": "Não", "Ano": 2026}


def test_the_fixed_dictionary_is_the_one_the_rows_were_written_with():
    assert hashlib.sha256(base_detail.ZDICT_PATH.read_bytes()).hexdigest() == base_detail.ZDICT_SHA256


def test_detail_keeps_the_portal_fields_as_published_and_leaves_out_empty_ones():
    d = base_detail.detail(NEW)
    assert d["adjudicante"] == NEW["adjudicante"] and d["CPV"] == NEW["CPV"] and d["Lotes"] == NEW["Lotes"]
    assert "descContrato" not in d                     # it repeats the object
    for empty in ("dataFechoContrato", "PrecoTotalEfetivo", "ocorrencias", "justifNReducEscrContrato"):
        assert empty not in d
    assert "nifQualquer" not in d and "idINCM" not in d   # only the portal's fields
    old = base_detail.detail(OLD)
    assert old["descContrato"] == "Selo, outro texto" and old["CritMateriais"] == "Não" and old["cpv"] == OLD["cpv"]


def test_pack_and_unpack_return_the_same_fields_and_compress():
    for rec in (NEW, OLD):
        d = base_detail.detail(rec)
        blob = base_detail.pack(d)
        assert base_detail.unpack(blob) == d
        assert len(blob) < len(json.dumps(d, ensure_ascii=False).encode("utf-8"))


def test_records_reads_the_one_json_member_of_a_dump():
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as z:
        z.writestr("Contratos2026.json", json.dumps([NEW, OLD], ensure_ascii=False))
    assert [r["idcontrato"] for r in base_detail.records(buf.getvalue())] == ["14730315", "12014814"]
