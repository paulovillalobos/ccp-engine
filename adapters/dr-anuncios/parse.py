"""E1b parser: fields of a DR notice by their printed label (pypdf text layer). Code only, no model.
Written on the dev set (dev/), frozen (sha256 in RUN.log) before it reads the sample."""
import json, re, sys
from pathlib import Path

def lab(label):  # a label whose spaces may be any whitespace (line wraps)
    return r"\s+".join(re.escape(w) for w in label.split())

PATTERNS = {
    "data_envio_anuncio": lab("Data de Envio do Anúncio:") + r"\s*(\d{2})-(\d{2})-(\d{4})",
    "publicado_joue": lab("publicitado no Jornal Oficial da União Europeia?") + r"\s*(Sim|Não)\b",
    "nut_iii": lab("NUT III:") + r"\s*(PT[0-9A-Z]{3})\b",
    "nif": lab("NIPC:") + r"\s*(\d{9})\b",
    "prazo_propostas_data": lab("Prazo para apresentação das propostas:") + r"\s*(\d{2})-(\d{2})-(\d{4})",
    "tipo_procedimento": lab("Tipo de Procedimento:") + r"[ \t]*([^\n]+)",
    "distrito": lab("Distrito:") + r"[ \t]*([^\n]+)",
    "norma_juridica": lab("Norma jurídica da Entidade Adjudicante:") + r"[ \t]*([^\n]+)",
}

def parse(text):
    out = {}
    for k, pat in PATTERNS.items():
        m = re.search(pat, text)  # the first occurrence: section 1, the adjudicante, for NUT III and distrito
        if not m:
            out[k] = None
        elif k in ("data_envio_anuncio", "prazo_propostas_data"):
            out[k] = f"{m.group(3)}-{m.group(2)}-{m.group(1)}"
        else:
            out[k] = m.group(1).strip()
    out["territorio"] = None if not out["nut_iii"] else ("PT-AC" if out["nut_iii"].startswith("PT2") else "PT-MA" if out["nut_iii"].startswith("PT3") else "PT")
    return out

if __name__ == "__main__":
    res = {p.name.split(".")[0]: parse(p.read_text(encoding="utf-8")) for p in sorted(Path(sys.argv[1]).glob("*.pypdf.txt"))}
    Path(sys.argv[2]).write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
    for k in PATTERNS: print(k, sum(1 for v in res.values() if v[k]), "/", len(res))
