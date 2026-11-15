"""Check, in the procedure's own documents, which regime it was run under (DECISIONS D96): what is found, and what needs
the person's analysis. Never a «very likely».

    <python with pypdf> -I adapters/plataformas/check_regime.py CASES.json OUT.json
    <python> -I adapters/plataformas/check_regime.py raws data/raw/pecas/raw/pecas-check.jsonl   the raw record of each stored response

CASES.json: [{"unit", "contrato", "link", ...}] (link = BASE's linkPecasProc). For each case:
  1. the documents BASE publishes with the contract (the portal's detail request; usually the signed contract, which
     states the procedure and its basis), and the documents as the platform publishes them: acinGov serves the pieces as one ZIP (one GET of the link); Vortal's
     public API gives the notice and its public documents (GetPublicTenderInformation, GetRegionConfigurationByContractNoticeUId,
     then each PublicDownload). Another platform, or no link: nothing is fetched.
     The rules of fetch.py: one GET every 10 s per host, User-Agent «ccp-engine research (passive read)», a 403/429 stops.
     Bytes kept in data/raw/pecas/raw_bytes/<sha256> (gitignored); every GET logged in adapters/plataformas/check-log.jsonl.
  2. the text of each PDF (pypdf text layer; a scan is read by OCR, ocrmypdf -l por) and DOCX (word/document.xml);
     other files listed, not read.
  3. what the text says, quoted with file and page:
       GERAL     the general regime's basis: «alínea c) do [n.º 1 do] artigo 19.º», «artigo 19.º, alínea c)»
       ESPECIAL  the special measures: «consulta prévia simplificada», «medidas especiais de contratação», an article
                 «da Lei n.º 30/2021» other than its art. 1.º (the act that amends the Code)
       MENCAO    the Code «na redação dada/conferida pela Lei n.º 30/2021», or Lei n.º 30/2021 named otherwise
  4. the result:
       verificado_regime_geral   GERAL found, ESPECIAL not found in any document read
       para_analise              ESPECIAL found (the quotes say where), or GERAL not found, or no document could be read
     A MENCAO alone decides nothing: Lei n.º 30/2021 also amends the Code (its art. 1.º b)).
Nothing here judges the law; it reports what the documents say and who must read them.
"""
import io
import json
import re
import sys
import time
import urllib.parse
import urllib.request
import zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
sys.path.insert(0, str(ROOT))
from engine.canon import sha256_bytes  # noqa: E402

VERSION = "ccp-check-regime-0.1"
UA, PACE_S = "ccp-engine research (passive read)", 10.0
STORE = ROOT / "data/raw/pecas/raw_bytes"  # gitignored, as fetch.py's pieces; each named by a raw record (raw_records, data/raw/pecas/raw/pecas-check.jsonl)
TEXTS = ROOT / "data/pecas-texto"  # gitignored: the text of each document (pypdf or OCR), cached by sha256
INDEX = TEXTS / "detalhe"  # gitignored: BASE's detail responses (a POST: the list of the contract's documents, not evidence)
LOG = HERE / "check-log.jsonl"
VORTAL = "https://community.vortal.biz"
_N19 = r"19\s*[.,]?\s*[ºo°09]?"  # «19.º» as printed or as OCR reads it («19,º», «19.0», «19.9», «19º»)
_ALC = r"al(?:[íi]nea|\.)\s*c\)"
_ART = r"art(?:igo|\.?\s*[ºo°]|\.)s?"
GERAL = re.compile(rf"{_ALC}\s*,?\s*do\s+(?:n\.?\s*[ºo°]\s*1\s+do\s+)?{_ART}\s*{_N19}(?!\d)|"
                   rf"{_ART}\s*(?:18\s*[.,]?\s*[ºo°]?\s*e\s+)?{_N19}(?!\d)\s*[,|]?\s*(?:n\.?\s*[ºo°]\s*1\s*,?\s*)?{_ALC}", re.I)
# another basis the documents state for this procedure: material criteria (arts. 24.º–27.º-A), another act, another procedure
OUTRA = re.compile(r"crit[ée]rios?\s+materia(?:l|is)|ao\s+abrigo\s+(?:da\s+al[íi]nea\s+\w\)\s+do\s+(?:n\.?\s*[ºo°]\s*\d\s+do\s+)?)?artigo\s+2[4-7]|"
                   r"al[íi]nea\s+[a-z]\)\s+do\s+(?:n\.?\s*[ºo°]\s*\d\s+do\s+)?artigo\s+2[4-7]\s*\.?\s*[ºo°]|artigo\s+27\s*[.,]?\s*[ºo°]?\s*[-–]?\s*(?-i:A)\b(?!/)|"
                   r"Decreto-Lei\s+n[.,]?\s*[ºo°]?\s*135\s*[-—]\s*A/2017|concurso\s+p[úu]blico\s+realizado\s+nos\s+termos", re.I)
ESPECIAL = re.compile(r"consulta\s+pr[ée]via\s+simplificada|medidas\s+especiais\s+de\s+contrata[çc][ãa]o|"
                      r"artigo\s+(?!1\.?\s*[ºo°]\s)\d+\.?\s*[ºo°](?:-[A-Z])?(?:[^.;]{0,40}?)\s+da\s+Lei\s+n\.?\s*[ºo°]?\s*30/2021", re.I)
MENCAO = re.compile(r"Lei\s+n\.?\s*[ºo°]?\s*30/2021", re.I)
# the invitation form's own question, answered (acinGov's model): «O procedimento é realizado para as medidas especiais de
# contratação pública? Não|Sim» — an explicit answer, read as such, never as a mention of the special measures
RESPOSTA = re.compile(r"medidas\s+especiais\s+de\s+contrata[çc][ãa]o\s+p[úu]blica\s*\?\s*(Sim|N[ãa]o)\b", re.I)
_last = {}


def _ctx():
    """TLS verified against the Mozilla CA bundle (certifi) when installed: base.gov.pt's Sectigo chain does not verify
    against this Python's default store. Verification is never turned off."""
    import ssl
    try:
        import certifi
        return ssl.create_default_context(cafile=certifi.where())
    except ImportError:
        return ssl.create_default_context()


CTX = _ctx()


def stored(url, post=None):
    """Bytes already fetched (a 200 in the log, kept by sha256): what is stored is never fetched again (fetch.py's rule)."""
    if not LOG.exists():
        return None
    key = json.dumps(post, sort_keys=True)
    for line in reversed(LOG.read_text(encoding="utf-8").splitlines()):
        e = json.loads(line)
        where = INDEX if e.get("post") else STORE
        if e.get("url") == url and json.dumps(e.get("post"), sort_keys=True) == key and e.get("status") == 200 and (where / e["sha256"]).exists():
            return (where / e["sha256"]).read_bytes()
    return None


def get(url):
    have = stored(url)
    if have is not None:
        return have
    host = urllib.parse.urlsplit(url).netloc
    wait = PACE_S - (time.time() - _last.get(host, 0))
    if wait > 0:
        time.sleep(wait)
    _last[host] = time.time()
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    entry = {"at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "url": url}
    try:
        with urllib.request.urlopen(req, timeout=120, context=CTX) as r:
            body = r.read()
        entry.update(status=200, sha256=sha256_bytes(body), bytes=len(body))
        STORE.mkdir(parents=True, exist_ok=True)
        (STORE / entry["sha256"]).write_bytes(body)
        return body
    except urllib.error.HTTPError as e:
        entry.update(status=e.code)
        if e.code in (403, 429):
            raise SystemExit(f"{host} refused ({e.code}): stopped")
        return None
    except Exception as e:  # noqa: BLE001
        entry.update(status=None, error=str(e)[:200])
        return None
    finally:
        with open(LOG, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")


def documents(link):
    """[(name, bytes, url)] as the platform publishes them, and how they were got."""
    if not link:
        return [], "sem ligação às peças no registo BASE"
    host = urllib.parse.urlsplit(link).netloc
    if host == "www.acingov.pt":
        body = get(link)
        if not body or body[:2] != b"PK":
            return [], "acinGov não serviu o ZIP das peças"
        z = zipfile.ZipFile(io.BytesIO(body))
        return [(n, z.read(n), link) for n in z.namelist() if not n.endswith("/")], "acinGov: ZIP das peças"
    if host in ("community.vortal.biz", "www.vortal.biz"):
        token = link.rstrip("/").rsplit("/", 1)[-1]
        info = get(f"{VORTAL}/public/api/PublicTenderDocuments/GetPublicTenderInformation?uniqueIdentifierEncrypted={urllib.parse.quote(token, safe='')}&languageCode=pt")
        if not info:
            return [], "Vortal não respondeu"
        info = json.loads(info)
        docs = [(d.get("name") or d.get("fileName") or "?", d.get("downloadUrl")) for d in info.get("documentList") or [] if d.get("downloadUrl")]
        m = re.search(r"(PT1\.NTC\.\d+)", info.get("contractNoticeUrl") or "")
        if m:
            ntc = get(f"{VORTAL}/public/api/ContractNoticeDetail/GetRegionConfigurationByContractNoticeUId?contractNoticeUId={m.group(1)}&langCode=pt")
            if ntc:
                def walk(x):
                    if isinstance(x, dict):
                        if x.get("downloadUrl") and x.get("isPublic", True):
                            docs.append((x.get("name") or "?", x["downloadUrl"]))
                        for v in x.values():
                            walk(v)
                    elif isinstance(x, list):
                        for v in x:
                            walk(v)
                walk(json.loads(ntc))
        out, seen = [], set()
        for name, url in docs:
            if url in seen or not re.search(r"\.(pdf|docx)$", name, re.I):
                continue
            seen.add(url)
            body = get(url)
            if body:
                out.append((name, body, url))
        return out, f"Vortal: {len(out)} documentos públicos lidos de {len(seen)}"
    return [], f"plataforma {host}: não lida por esta ferramenta"


def base_documents(contrato):
    """The documents BASE publishes with the contract (usually the signed contract): the portal's own detail request,
    then each document by its id. [(name, bytes, url)]."""
    detail = get_post("https://www.base.gov.pt/Base4/pt/resultados/", {"type": "detail_contratos", "id": str(contrato), "version": "136.0"})
    if not detail:
        return []
    try:
        docs = json.loads(detail).get("documents") or []
    except ValueError:
        return []
    out = []
    for d in docs:
        url = f"https://www.base.gov.pt/Base4/pt/resultados/?type=doc_documentos&id={d['id']}&ext=.pdf"
        body = get(url)
        if body:
            out.append((f"BASE: {d.get('description') or d['id']}", body, url))
    return out


def get_post(url, form):
    """The portal's detail request is a form POST that reads (no state changes); logged and paced like a GET."""
    have = stored(url, form)
    if have is not None:
        return have
    host = urllib.parse.urlsplit(url).netloc
    wait = PACE_S - (time.time() - _last.get(host, 0))
    if wait > 0:
        time.sleep(wait)
    _last[host] = time.time()
    data = urllib.parse.urlencode(form).encode()
    entry = {"at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "url": url, "post": form}
    try:
        with urllib.request.urlopen(urllib.request.Request(url, data=data, headers={"User-Agent": UA}), timeout=120, context=CTX) as r:
            body = r.read()
        entry.update(status=200, sha256=sha256_bytes(body), bytes=len(body))
        INDEX.mkdir(parents=True, exist_ok=True)
        (INDEX / entry["sha256"]).write_bytes(body)  # the portal's index of the contract's documents: never a raw (I10: only a passive GET is)
        return body
    except urllib.error.HTTPError as e:
        entry.update(status=e.code)
        if e.code in (403, 429):
            raise SystemExit(f"{host} refused ({e.code}): stopped")
        return None
    except Exception as e:  # noqa: BLE001
        entry.update(status=None, error=str(e)[:200])
        return None
    finally:
        with open(LOG, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")


def ocr(body):
    """The text of a scanned PDF (ocrmypdf + tesseract, Portuguese), one page string; '' when the tools are absent."""
    import shutil
    import subprocess
    import tempfile
    if not shutil.which("ocrmypdf"):
        return ""
    with tempfile.TemporaryDirectory() as t:
        src, txt = Path(t) / "in.pdf", Path(t) / "out.txt"
        src.write_bytes(body)
        r = subprocess.run(["ocrmypdf", "-q", "-l", "por", "--force-ocr", "--sidecar", str(txt), "--output-type", "none", str(src), "-"],
                           capture_output=True, timeout=900)
        return txt.read_text(encoding="utf-8", errors="replace") if r.returncode == 0 and txt.exists() else ""


def texts(name, body):
    """[(page, text)] of one file, cached beside its bytes (<sha256>.pages.json)."""
    cache = TEXTS / f"{sha256_bytes(body)}.pages.json"
    if cache.exists():
        return [tuple(x) for x in json.loads(cache.read_text(encoding="utf-8"))]
    out = _texts(name, body)
    TEXTS.mkdir(parents=True, exist_ok=True)
    cache.write_text(json.dumps(out, ensure_ascii=False), encoding="utf-8")
    return out


def _texts(name, body):
    """[(page, text)] of one file; [] when it has no text layer the code can read. A PDF without one is read by OCR
    (page «ocr»: the words are tesseract's, so a quote may differ from the printed text by a letter)."""
    if name.lower().endswith(".pdf"):
        try:
            import pypdf
            pages = [(i + 1, p.extract_text() or "") for i, p in enumerate(pypdf.PdfReader(io.BytesIO(body)).pages)]
        except Exception:  # noqa: BLE001
            pages = []
        if sum(len(t.strip()) for _, t in pages) < 200:
            t = ocr(body)
            return [("ocr", t)] if t.strip() else pages
        return pages
    if name.lower().endswith(".docx"):
        try:
            xml = zipfile.ZipFile(io.BytesIO(body)).read("word/document.xml").decode("utf-8", "replace")
            return [(1, re.sub(r"<[^>]+>", " ", xml))]
        except Exception:  # noqa: BLE001
            return []
    if name.lower().endswith(".zip"):
        try:
            z = zipfile.ZipFile(io.BytesIO(body))
            return [(f"{n}:{p}", t) for n in z.namelist() for p, t in _texts(n, z.read(n))]
        except Exception:  # noqa: BLE001
            return []
    return []


def quote(text, m):
    s = " ".join(text[max(0, m.start() - 160):m.end() + 160].split())
    return s


def check(case):
    docs, how = documents(case.get("link"))
    if case.get("contrato"):  # BASE's own documents of the contract, always read too
        bd = base_documents(case["contrato"])
        docs, how = docs + bd, how + f"; BASE: {len(bd)} documento(s) do contrato"
    found = {"GERAL": [], "ESPECIAL": [], "OUTRA": [], "MENCAO": []}
    read, unread = [], []
    for name, body, url in docs:
        pages = texts(name, body)
        if not any(t.strip() for _, t in pages):
            unread.append(name)
            continue
        read.append(name)
        for page, t in pages:
            for m in RESPOSTA.finditer(t):  # the form's answer: Não → the general regime declared; Sim → the special measures
                k = "ESPECIAL" if m.group(1).lower() == "sim" else "GERAL"
                found[k].append({"ficheiro": name, "pagina": page, "sha256": sha256_bytes(body), "texto": quote(t, m), "resposta_do_formulario": m.group(1)})
            t = RESPOSTA.sub(" ", t)
            for k, pat in (("GERAL", GERAL), ("ESPECIAL", ESPECIAL), ("OUTRA", OUTRA), ("MENCAO", MENCAO)):
                for m in pat.finditer(t):
                    if len(found[k]) < 6:
                        found[k].append({"ficheiro": name, "pagina": page, "sha256": sha256_bytes(body), "texto": quote(t, m)})
    if found["ESPECIAL"]:
        result, why = "para_analise", "os documentos falam das medidas especiais (citações abaixo): ler se são a base deste procedimento"
    elif found["OUTRA"] and not found["GERAL"]:
        result, why = "para_analise", "os documentos dão outra base ao procedimento (critério material, outro ato ou outro procedimento): citações abaixo"
    elif found["OUTRA"]:
        result, why = "para_analise", "os documentos citam a alínea c) do art. 19.º e também outra base: ler qual é a do procedimento"
    elif not read:
        result, why = "para_analise", f"nenhum documento lido ({how}; sem texto: {len(unread)})"
    elif not found["GERAL"]:
        result, why = "para_analise", "os documentos lidos não dizem a base legal (nem alínea c) do art. 19.º, nem medidas especiais)"
    else:
        result, why = "verificado_regime_geral", "os documentos dizem a alínea c) do art. 19.º e nada das medidas especiais"
    grupo = ("A" if result == "verificado_regime_geral" else "B" if found["ESPECIAL"] else "E" if found["OUTRA"] else "C" if read else "D")
    return {**case, "resultado": result, "grupo": grupo, "porque": why, "como": how, "lidos": read, "sem_texto": unread, "encontrado": found}


def raw_id(entry):
    """raw:pecas:documento:<first 24 hex of sha256> for one document of the log (a passive GET)."""
    return f"raw:pecas:documento:{entry['sha256'][:24]}"


def raw_records(log=LOG, recorded_at=None):
    """One raw record per stored response (the first 200 with those bytes), as data/raw/pecas/raw/*.jsonl holds them."""
    out = {}
    for line in Path(log).read_text(encoding="utf-8").splitlines():
        e = json.loads(line)
        if e.get("status") != 200 or not e.get("sha256") or e.get("post") or raw_id(e) in out:
            continue  # a POST (BASE's detail) is an index, never a raw
        out[raw_id(e)] = {"bytes": f"raw_bytes/{e['sha256']}", "captured_at": e["at"], "encoding": "binary", "id": raw_id(e),
                          "kind": "documento", "media_type": "application/octet-stream",
                          "recorded_at": recorded_at or e["at"], "request": {"method": "GET", "reads_of_page": 1},
                          "revision": 1, "sha256": e["sha256"], "source": "pecas", "source_id": e["sha256"][:24], "url": e["url"]}
    return list(out.values())


def main():
    if sys.argv[1] == "raws":  # write the raw records of every stored response
        rows = raw_records()
        Path(sys.argv[2]).write_text("".join(json.dumps(r, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n" for r in rows), encoding="utf-8")
        print(f"{len(rows)} raw records")
        return
    cases = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    out = []
    for i, c in enumerate(cases, 1):
        r = check(c)
        out.append(r)
        print(f"{i}/{len(cases)} {c['unit']}: {r['resultado']} ({r['como']})", flush=True)
        Path(sys.argv[2]).write_text(json.dumps({"tool": VERSION, "casos": out}, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
