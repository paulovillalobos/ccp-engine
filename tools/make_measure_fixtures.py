"""The 20 measurement cases of B5 while data/ is empty: fixtures/measure/, a store of FIXTURE procedures.

    .venv/bin/python tools/make_measure_fixtures.py        rewrites fixtures/measure/ (deterministic: same bytes every run)

Each case is a synthetic proc (marked FIXTURE in its raw record, never BASE data) with the canonical facts the B3 rules
read, chosen to sit on the edges the rules turn on: values just under and over each threshold before and after
2026-10-01, deadlines short and long with and without JOUE publication, a Madeira and an Açores procedure, missing
facts. Stratified by procedure type (ajuste direto, consulta prévia, concurso público), value and period. Held out per
law/HELD-OUT.json (adjudicante NIF hashing to 0 mod 5, or started on or after 2026-10-01); the split is computed by
tools/measure.py from that file, not stored here. One adapter (adaptador:fixture-measure@1) maps the raw fields.
"""
import hashlib
import json
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from engine.canon import canonical  # noqa: E402

VERSION = "ccp-make-measure-fixtures-0.1"
OUT = ROOT / "fixtures/measure"
AT = "2026-10-24T21:00:00Z"
NIFS = ["500000011", "500000028", "500000035", "500000042", "500000059"]
# (case, procedure, contract, price, start, joue, days, territory, entity, nif index, note)
CASES = [
    ("M-01", "ajuste_direto", "bens", 60000, "2026-10-05", False, 5, "PT", "outra", 0, "under 75 000 (from 2026-10-01)"),
    ("M-02", "ajuste_direto", "bens", 80000, "2026-10-06", False, 5, "PT", "outra", 1, "over 75 000"),
    ("M-03", "ajuste_direto", "servicos", 18000, "2026-09-10", False, 5, "PT", "outra", 2, "under 20 000 (until 2026-09-30)"),
    ("M-04", "ajuste_direto", "servicos", 25000, "2026-09-12", False, 5, "PT", "outra", 3, "over 20 000 before, under 75 000 after"),
    ("M-05", "ajuste_direto", "obras", 140000, "2026-10-07", False, 5, "PT", "outra", 4, "works under 150 000 (from 2026-10-01)"),
    ("M-06", "ajuste_direto", "obras", 40000, "2026-09-15", False, 5, "PT", "outra", 0, "works over 30 000 (until 2026-09-30)"),
    ("M-07", "consulta_previa", "bens", 120000, "2026-10-08", False, 5, "PT", "outra", 1, "under 130 000"),
    ("M-08", "consulta_previa", "servicos", 90000, "2026-09-20", False, 5, "PT", "outra", 2, "over 75 000 before"),
    ("M-09", "consulta_previa", "obras", 900000, "2026-10-09", False, 5, "PT", "outra", 3, "works under 1 000 000"),
    ("M-10", "consulta_previa", "obras", 200000, "2026-09-22", False, 5, "PT", "outra", 4, "works over 150 000 before"),
    ("M-11", "concurso_publico", "bens", 135000, "2026-10-10", False, 7, "PT", "estado", 0, "no JOUE, under both readings of the JOUE threshold; 7 days"),
    ("M-12", "concurso_publico", "bens", 139500, "2026-10-11", False, 5, "PT", "estado", 1, "no JOUE, between 139 000 and 140 000; 5 days"),
    ("M-13", "concurso_publico", "obras", 3000000, "2026-10-12", False, 12, "PT", "outra", 2, "works no JOUE under 5 404 000; 12 days"),
    ("M-14", "concurso_publico", "obras", 6000000, "2026-09-25", False, 20, "PT", "outra", 3, "works no JOUE over the threshold; 20 days"),
    ("M-15", "concurso_publico", "servicos", 400000, "2026-10-13", True, 30, "PT", "outra", 4, "JOUE, 30 days"),
    ("M-16", "concurso_publico", "bens", 500000, "2026-09-28", True, 25, "PT", "estado", 0, "JOUE, 25 days"),
    ("M-17", "ajuste_direto", "bens", 90000, "2026-10-14", False, 5, "PT-MA", "outra", 1, "Madeira: over 75 000, under 75 000 x 1,45"),
    ("M-18", "consulta_previa", "servicos", 100000, "2026-10-15", False, 5, "PT-AC", "outra", 2, "Açores entity"),
    ("M-19", "ajuste_direto", "servicos", None, "2026-09-18", False, 5, "PT", "outra", 3, "no price published"),
    ("M-20", "concurso_publico", "bens", 100000, "2026-10-16", False, None, "PT", "outra", 4, "no deadline published"),
]
MAPPING = [("dataInicio", "data_inicio_procedimento", "date_iso"), ("tipoProcedimento", "tipo_procedimento", "identity"),
           ("tipoContrato", "tipo_contrato", "identity"), ("precoBase", "preco_base", "number_pt"), ("publicadoJOUE", "publicado_joue", "boolean"),
           ("prazoPropostas", "prazo_propostas_dias", "integer"), ("dataEnvioAnuncio", "data_envio_anuncio", "date_iso"),
           ("territorio", "territorio", "identity"), ("tipoEntidade", "tipo_entidade", "identity"), ("nifEntidadeAdjudicante", "adjudicante", "nif")]


def write(path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=1, sort_keys=True) + "\n", encoding="utf-8")


def main():
    if OUT.exists():
        shutil.rmtree(OUT)
    adapter = {"id": "adaptador:fixture-measure@1", "revision": 1, "recorded_at": AT, "source": "fixture-measure", "version": 1,
               "code": "adapters/fixture-measure/", "mapping": [{"source_field": s, "canonical_field": c, "transform": t} for s, c, t in MAPPING],
               "coverage": [{"period": "2026-09", "expected": None, "captured": 10}, {"period": "2026-10", "expected": None, "captured": 10}],
               "proposed_by": "ferramenta:make-measure-fixtures@1", "state": "proposed"}
    write(OUT / "adaptador/fixture-measure-1.json", adapter)
    for case, proc, kind, price, start, joue, days, terr, ent, nif, note in CASES:
        record = {"FIXTURE": "synthetic measurement case, not BASE data", "nAnuncio": case, "dataInicio": start, "tipoProcedimento": proc,
                  "tipoContrato": kind, "precoBase": price, "publicadoJOUE": joue, "prazoPropostas": days, "dataEnvioAnuncio": start,
                  "territorio": terr, "tipoEntidade": ent, "nifEntidadeAdjudicante": NIFS[nif], "note": note}
        data = canonical(record).encode("utf-8")
        sha = hashlib.sha256(data).hexdigest()
        (OUT / "raw_bytes").mkdir(parents=True, exist_ok=True)
        (OUT / "raw_bytes" / sha).write_bytes(data)
        raw_id = f"raw:fixture-measure:caso:{case.lower()}"
        write(OUT / f"raw/{raw_id.replace(':', '-')}.r1.json", {
            "id": raw_id, "revision": 1, "recorded_at": AT, "source": "fixture-measure", "kind": "caso", "source_id": case.lower(), "sha256": sha,
            "bytes": f"raw_bytes/{sha}", "media_type": "application/json", "encoding": "utf-8", "url": f"https://example.invalid/ccp-engine/fixture-measure/{case}",
            "captured_at": AT, "request": {"method": "GET", "reads_of_page": 1, "renderer": f"{VERSION}: generated, not read"}, "text": None})
        unit = f"proc:fixture-measure:{case}"
        write(OUT / f"unidade/{unit.replace(':', '-')}.json", {"id": unit, "revision": 1, "recorded_at": AT, "kind": "proc", "parent": None,
                                                             "raw": [raw_id], "consumer_ids": {"n_anuncio": case}})
        for source_field, field, _ in MAPPING:
            value = record[source_field]
            if value is None:
                continue  # an unpublished fact is absent, never null
            fid = f"facto:{unit.replace(':', '-')}:{field}:fixture-measure"
            write(OUT / f"facto/{fid.split(':', 1)[1].replace(':', '-')}.json", {
                "id": fid, "revision": 1, "recorded_at": AT, "unit": unit, "field": field, "value": value,
                "origin": {"raw": raw_id, "field": source_field}, "adapter": adapter["id"], "valid_at": start, "known_at": AT})
    print(f"{len(CASES)} cases in {OUT}")


if __name__ == "__main__":
    main()
