"""The municipal pilot (FILL-PLAN B2c): law/MUNICIPIOS-PILOTO.md from law/municipios/piloto.json and the store.

    .venv/bin/python tools/pilot_municipios.py [--write]

law/municipios/piloto.json lists, per município, the records of its own law that matter to a procurement verdict
(norma de controlo interno, delegação de competências da câmara no presidente / subdelegações with spending limits,
regulamento de compras or de contratação): where each was looked for, where it was found (URL), its format, and the
raw record when it was captured. Everything counted here is read from the store, never from the file's prose:
    found     records with a URL
    captured  records whose raw exists in law/ (bytes by sha256)
    with text a captured HTML page (working text) or a PDF whose text layer holds at least 500 characters per page
              (stdlib zlib over the content streams; a scanned PDF has none; an encrypted PDF, as the DR's 2.ª série
              files are, is captured but its text is not verified)
The estimate for the 308 municípios is the pilot's own cost per município (reads, records, share with text) times
308, stated with what it does not cover. No network, no model.
"""
import argparse
import json
import re
import sys
import zlib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from engine.store import Store  # noqa: E402

VERSION = "ccp-pilot-municipios-0.1"
DATA = ROOT / "law/municipios/piloto.json"
TEXT_PER_PAGE = 500


def pdf_text_stats(data: bytes):
    """(pages, bytes of text shown by Tj / TJ) of a PDF: literal and hex strings (a CID font's glyph codes are two bytes
    per character, so this is an upper bound for them; the 500-per-page bar is meant for a scan / not-a-scan test)."""
    pages = len(re.findall(rb"/Type\s*/Page[^s]", data))
    chars = 0
    for m in re.finditer(rb"stream\r?\n(.*?)\r?\nendstream", data, re.S):
        body = m.group(1)
        try:
            body = zlib.decompress(body)
        except zlib.error:
            continue
        for a, h, b in re.findall(rb"\(((?:[^()\\]|\\.)*)\)\s*Tj|<([0-9A-Fa-f\s]*)>\s*Tj|\[(.*?)\]\s*TJ", body, re.S):
            # literal strings count their bytes; hex strings (CID fonts) two hex digits per byte
            chars += len(a) + len(re.sub(rb"\s", b"", h)) // 2
            if b:
                chars += sum(len(x) for x in re.findall(rb"\(((?:[^()\\]|\\.)*)\)", b))
                chars += sum(len(re.sub(rb"\s", b"", x)) // 2 for x in re.findall(rb"<([0-9A-Fa-f\s]*)>", b))
    return pages, chars


def record_state(store, rec):
    raw = store.current(rec["raw"]) if rec.get("raw") else None
    if raw is None:
        return {"captured": False, "text": False, "detail": "não capturado"}
    data = store.raw_path(raw).read_bytes()
    if raw["media_type"] == "application/pdf":
        if re.search(rb"/Encrypt\b", data):  # the DR's 2.ª série PDFs: streams cannot be read without a PDF library (D17)
            return {"captured": True, "text": False, "detail": "PDF cifrado (/Encrypt): camada de texto não verificável aqui"}
        pages, chars = pdf_text_stats(data)
        ok = pages > 0 and chars / pages >= TEXT_PER_PAGE
        return {"captured": True, "text": ok, "detail": f"PDF {pages} p., {chars} car. de texto"}
    text = store.raw_text(raw) or ""
    return {"captured": True, "text": len(text) > TEXT_PER_PAGE, "detail": f"HTML, {len(text)} car. de texto"}


def render(store, data):
    L = ["# MUNICÍPIOS — piloto (FILL-PLAN B2c)", "",
         f"Gerado por tools/pilot_municipios.py ({VERSION}) a partir de law/municipios/piloto.json e do store; não editar à mão.",
         "", data["method"], "", "## Cobertura por município", "",
         "| município | registos encontrados | capturados | com texto | onde |", "|---|---|---|---|---|"]
    totals = {"found": 0, "captured": 0, "text": 0, "reads": 0}
    detail = []
    for m in data["municipios"]:
        recs = m["records"]
        states = [record_state(store, r) for r in recs]
        found = sum(1 for r in recs if r.get("url"))
        cap = sum(s["captured"] for s in states)
        txt = sum(s["text"] for s in states)
        where = sorted({r["where"] for r in recs if r.get("url")}) or ["—"]
        L.append(f"| {m['name']} | {found} | {cap} | {txt} | {', '.join(where)} |")
        totals["found"] += found; totals["captured"] += cap; totals["text"] += txt; totals["reads"] += m.get("reads", 0)
        detail.append(f"### {m['name']}")
        for r, s in zip(recs, states):
            detail.append(f"- {r['type']}: {r.get('title', '—')} — {r.get('where', '—')} — {r.get('url') or 'não encontrado'}"
                          f" — {s['detail']}" + (f" — raw {r['raw']}" if r.get("raw") else "") + (f" — {r['note']}" if r.get("note") else ""))
        detail.append(f"- procurado: {m['searched']}")
        detail.append("")
    n = len(data["municipios"])
    L += ["", f"Totais: {totals['found']} encontrados, {totals['captured']} capturados, {totals['text']} com texto, em {n} municípios.", "",
          "## Estimativa para os 308 municípios", ""]
    per = {k: (v / n if n else 0) for k, v in totals.items()}
    L += [f"- registos por município no piloto: {per['found']:.1f} encontrados, {per['captured']:.1f} capturados, {per['text']:.1f} com texto",
          f"- estimativa linear para 308: ~{round(per['found'] * 308)} registos encontrados, ~{round(per['captured'] * 308)} capturáveis, "
          f"~{round(per['text'] * 308)} com texto utilizável sem OCR",
          f"- leituras passivas no piloto: {totals['reads']} ({per['reads']:.1f} por município); para 308: ~{round(per['reads'] * 308)} leituras, "
          f"a 3 s entre páginas, ~{round(per['reads'] * 308 * 15 / 3600, 1)} h de captura (15 s por leitura com renderização)",
          ""] + [f"- {x}" for x in data["estimate_notes"]] + ["", "## Detalhe por município", ""] + detail
    return "\n".join(L) + "\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true")
    a = ap.parse_args()
    store = Store([ROOT / "law"]).load()
    data = json.loads(DATA.read_text(encoding="utf-8"))
    out = render(store, data)
    if a.write:
        (ROOT / "law/MUNICIPIOS-PILOTO.md").write_text(out, encoding="utf-8")
    print(out)


if __name__ == "__main__":
    main()
