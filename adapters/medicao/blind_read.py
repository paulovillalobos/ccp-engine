"""Check C of CRITERIA-ted-contratos-v1.md: the family-B reader reads each sampled record blind (reader-b exec, read-only
sandbox, empty working directory, the same flags as the DR test's blind_read.py). It never sees the parsers' output.

    python3 -I adapters/medicao/blind_read.py OUT ted|contratos READER_B_BIN [MODEL]

OUT/<source>/items/<n>.xml|json are the records (unchanged source text); answers go to OUT/<source>/blind/batch-NN.json
with the sha256 of the raw answer. A batch already answered is kept. Two batches at a time.
"""
import hashlib
import json
import subprocess
import sys
import tempfile
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

OUT, SOURCE, READER_B = Path(sys.argv[1]), sys.argv[2], sys.argv[3]
MODEL = sys.argv[4] if len(sys.argv) > 4 else None
B = OUT / SOURCE
out = B / "blind"
out.mkdir(exist_ok=True)
FIELDS = {
    "ted": ["dispatch_date", "buyer_name", "buyer_nif", "buyer_country", "procedure_type", "contract_type", "deadline_date",
            "deadline_time", "estimated_value", "main_cpv"],
    "contratos": ["tipoprocedimento", "precoBaseProcedimento", "adjudicante_nif", "tipoContrato", "precoContratual",
                  "dataCelebracaoContrato", "dataPublicacao", "adjudicatarios_nifs"],
}[SOURCE]
HEAD = {
    "ted": ("Lê cada anúncio do TED (XML) abaixo e devolve, para cada um, só o que está no texto, sem inferir:\n"
            "- dispatch_date: a data de envio do anúncio ao Serviço de Publicações (AAAA-MM-DD)\n"
            "- buyer_name: o nome oficial da entidade adjudicante (o comprador)\n"
            "- buyer_nif: o número de identificação nacional (NIF/NIPC) dessa entidade, se estiver no texto\n"
            "- buyer_country: o país dessa entidade, como código do texto (p. ex. PT ou PRT)\n"
            "- procedure_type: o tipo de procedimento como codificado no texto (p. ex. «1 Open procedure» ou «open»)\n"
            "- contract_type: a natureza do contrato como codificada (p. ex. SUPPLIES, SERVICES, WORKS, services, works)\n"
            "- deadline_date: a data-limite de receção das propostas ou candidaturas (AAAA-MM-DD), a do primeiro lote se houver vários\n"
            "- deadline_time: a hora dessa data-limite, tal como escrita\n"
            "- estimated_value: o valor total estimado do contrato, só o número, como escrito\n"
            "- main_cpv: o código CPV principal, só os dígitos\n"),
    "contratos": ("Lê cada registo de contrato do Portal BASE (JSON) abaixo e devolve, para cada um, só o que está no registo, sem inferir:\n"
                  "- tipoprocedimento: o tipo de procedimento tal como escrito\n- precoBaseProcedimento: o preço base, só o número\n"
                  "- adjudicante_nif: o NIF da entidade adjudicante, 9 dígitos\n- tipoContrato: o(s) tipo(s) de contrato, separados por «; »\n"
                  "- precoContratual: o preço contratual, só o número\n- dataCelebracaoContrato: a data de celebração, AAAA-MM-DD\n"
                  "- dataPublicacao: a data de publicação, AAAA-MM-DD\n"
                  "- adjudicatarios_nifs: os NIF dos adjudicatários, 9 dígitos cada, separados por «; » (null se algum não tiver NIF)\n"),
}[SOURCE] + "Se um campo não estiver no texto, null. O id é o número que vem em cada cabeçalho.\n\n"
item = {"type": "object", "additionalProperties": False, "required": ["id"] + FIELDS,
        "properties": {"id": {"type": "string"}, **{k: {"type": ["string", "null"]} for k in FIELDS}}}
schema = {"type": "object", "additionalProperties": False, "required": ["records"], "properties": {"records": {"type": "array", "items": item}}}
ext = "xml" if SOURCE == "ted" else "json"
ids = sorted(p.stem for p in (B / "items").glob(f"*.{ext}"))
per_batch = 5 if SOURCE == "ted" else 10


def run(batch):
    n, chunk = batch
    f = out / f"batch-{n:02d}.json"
    if f.exists():
        return f"{f.name} kept"
    prompt = HEAD + "".join(f"===== REGISTO id={i} =====\n{(B / 'items' / f'{i}.{ext}').read_text(encoding='utf-8')}\n\n" for i in chunk)
    with tempfile.TemporaryDirectory() as empty:
        (Path(empty) / "schema.json").write_text(json.dumps(schema), encoding="utf-8")
        o = Path(empty) / "answer.txt"
        cmd = [READER_B, "exec", "--skip-git-repo-check", "--sandbox", "read-only", "--ephemeral", "-C", empty, "-c", 'model_reasoning_effort="medium"',
               *(["-m", MODEL] if MODEL else []), "--output-schema", str(Path(empty) / "schema.json"), "-o", str(o), "-"]
        res = subprocess.run(cmd, input=prompt, capture_output=True, text=True, timeout=1800)
        text = o.read_text(encoding="utf-8") if o.exists() else ""
    if not text.strip():
        return f"{f.name}: no answer (exit {res.returncode}) {res.stderr[-200:]}"
    f.write_text(json.dumps({"at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "ids": chunk, "sha256": hashlib.sha256(text.encode()).hexdigest(),
                             "answer": json.loads(text)}, ensure_ascii=False, indent=1), encoding="utf-8")
    return f"{f.name} answered"


batches = [(n, ids[k:k + per_batch]) for n, k in enumerate(range(0, len(ids), per_batch))]
with ThreadPoolExecutor(2) as ex:
    for msg in ex.map(run, batches):
        print(msg, flush=True)
