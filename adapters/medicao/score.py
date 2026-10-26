"""Score checks A, B and C of CRITERIA-ted-contratos-v1.md from the sealed sample, the parsers' output and the blind answers.

    .venv/bin/python -I adapters/medicao/score.py ted OUT --anuncios DIR      (DIR: anuncios<year>.json of BASE)
    .venv/bin/python -I adapters/medicao/score.py contratos OUT

Writes OUT/<source>/score.json and prints it. Shares with Wilson 95 % intervals. Normalisation as the criteria say:
dates as dates, amounts to the cent, NIFs as nine digits, names accents and case folded, country PT = PRT.
No model is called here.
"""
import json
import math
import re
import sys
import unicodedata
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent


def wilson(k, n, z=1.96):
    if n == 0:
        return None
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return {"k": k, "n": n, "pct": round(100 * p, 1), "wilson95": [round(100 * (c - h), 1), round(100 * (c + h), 1)]}


def fold(s):
    s = unicodedata.normalize("NFKD", str(s)).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", " ", s).strip()


def num(v):
    try:
        return round(float(str(v).replace(" ", "").replace(",", ".")), 2)
    except ValueError:
        return None


def digits(v):
    d = re.sub(r"\D", "", str(v))
    return d[-9:] if len(d) >= 9 else d


def date(v):
    m = re.search(r"(\d{4})-(\d{2})-(\d{2})", str(v))
    if m:
        return m.group(0)
    m = re.search(r"(\d{2})/(\d{2})/(\d{4})", str(v))
    return f"{m.group(3)}-{m.group(2)}-{m.group(1)}" if m else None


TED_NORM = {"dispatch_date": date, "deadline_date": date, "buyer_name": fold, "buyer_nif": digits, "estimated_value": num,
            "buyer_country": lambda v: {"pt": "pt", "prt": "pt"}.get(fold(v), fold(v)), "contract_type": fold,
            "main_cpv": lambda v: re.sub(r"\D", "", str(v))[:8], "deadline_time": lambda v: str(v)[:5],
            "procedure_type": lambda v: fold(re.sub(r"^\d+\s+", "", str(v)))}


def check_a(parsed, fields, required, contract_only=()):
    out = {}
    for f in fields:
        rows = [p for p in parsed if not contract_only or f not in contract_only or p.get("_contract")]
        k = sum(1 for p in rows if p.get(f) not in (None, "", []))
        out[f] = dict(wilson(k, len(rows)) or {}, required=f in required, pass_=None if f not in required else (k / len(rows) >= 0.95 if rows else None))
    return out


def blind_answers(B):
    ans = {}
    for f in sorted((B / "blind").glob("batch-*.json")):
        for r in json.loads(f.read_text(encoding="utf-8"))["answer"]["records"]:
            ans[int(r["id"])] = r
    return ans


def check_c(parsed, ans, pairs):
    agree, total, dis = 0, 0, []
    for p in parsed:
        a = ans.get(p["n"])
        if a is None:
            continue
        for pf, af, norm in pairs:
            pv, av = p.get(pf), a.get(af)
            if pv in (None, "", []) or av in (None, ""):
                continue
            total += 1
            x, y = norm(pv), norm(av)
            if x == y:
                agree += 1
            else:
                dis.append({"n": p["n"], "field": pf, "parser": pv, "reader": av})
    return dict(wilson(agree, total) or {}, disagreements=dis, pass_=(agree / total >= 0.98) if total else None)


def score_ted(out, anuncios_dir):
    B = out / "ted"
    parsed = json.loads((B / "parsed.json").read_text(encoding="utf-8"))
    for p in parsed:
        p["_contract"] = (p.get("notice_type") or "").split(" ")[0] in ("3", "16", "17", "18")
    fields = ["dispatch_date", "notice_type", "notice_id", "buyer_name", "buyer_nif", "buyer_country", "buyer_nuts", "procedure_type",
              "contract_type", "deadline_date", "deadline_time", "estimated_value", "main_cpv"]
    a = check_a(parsed, fields, {"dispatch_date", "notice_type", "notice_id", "buyer_name", "main_cpv", "deadline_date"}, contract_only=("deadline_date",))
    ans = blind_answers(B) if (B / "blind").exists() else {}
    c = check_c(parsed, ans, [(f, f, TED_NORM[f]) for f in TED_NORM]) if ans else {"status": "NOT RUN"}
    # B: the same procedure among BASE anúncios of the same year (same deadline date; same buyer NIF for eForms, folded name for TED-XML)
    base = {}
    for f in sorted(Path(anuncios_dir).glob("anuncios*.json")) if anuncios_dir else []:
        for r in json.loads(f.read_text(encoding="utf-8")):
            d = date(r.get("DataLimitePropostas") or "")
            if d:
                base.setdefault(d, []).append(r)
    proc_map = {"open": "concurso publico", "restricted": "concurso limitado por previa qualificacao", "neg w call": "procedimento de negociacao",
                "1 open procedure": "concurso publico", "2 restricted procedure": "concurso limitado por previa qualificacao"}
    joined, agree, total, dis = 0, 0, 0, []
    contracts = [p for p in parsed if p["_contract"] and p.get("deadline_date")]
    for p in contracts:
        cands = base.get(p["deadline_date"], [])
        if p["format"] == "eforms" and p.get("buyer_nif"):
            cands = [r for r in cands if digits(r.get("nifEntidade")) == digits(p["buyer_nif"])]
        else:
            cands = [r for r in cands if fold(r.get("designacaoEntidade")) == fold(p.get("buyer_name"))]
        if len(cands) != 1:
            continue
        joined += 1
        r = cands[0]
        if p.get("estimated_value") and num(r.get("PrecoBase")) is not None:
            total += 1
            ok = num(p["estimated_value"]) == num(r["PrecoBase"])
            agree += ok
            if not ok:
                dis.append({"n": p["n"], "field": "estimated_value", "ted": p["estimated_value"], "base": r["PrecoBase"], "nAnuncio": r["nAnuncio"]})
        pt = proc_map.get(fold(p.get("procedure_type") or "")) or proc_map.get((p.get("procedure_type") or "").lower())
        if pt:
            total += 1
            ok = fold(r.get("modeloAnuncio")) == pt
            agree += ok
            if not ok:
                dis.append({"n": p["n"], "field": "procedure_type", "ted": p["procedure_type"], "base": r.get("modeloAnuncio"), "nAnuncio": r["nAnuncio"]})
    b = {"contract_notices": len(contracts), "joined": wilson(joined, len(contracts)), "agreement": dict(wilson(agree, total) or {}, pass_=(agree / total >= 0.95) if total else None),
         "disagreements": dis} if anuncios_dir else {"status": "NOT RUN (no anúncios given)"}
    return {"source": "ted", "A": a, "B": b, "C": c}


def score_contratos(out):
    B = out / "contratos"
    parsed = json.loads((B / "parsed.json").read_text(encoding="utf-8"))
    sample = {s["n"]: s for s in json.loads((B / "sample.json").read_text(encoding="utf-8"))}
    mapping = json.loads((ROOT / "adapters/base-contratos/mapping.json").read_text(encoding="utf-8"))["adaptador"]["mapping"]
    m_proc = next(m for m in mapping if m["canonical_field"] == "tipo_procedimento")["enum_map"]
    m_tipo = next(m for m in mapping if m["canonical_field"] == "tipo_contrato")["enum_map"]
    fields = ["tipo_procedimento", "preco_base", "adjudicante", "tipo_contrato", "preco_contratual", "data_celebracao_contrato", "data_publicacao_contrato", "adjudicatario"]
    a = check_a(parsed, fields, {"preco_contratual", "data_publicacao_contrato", "adjudicante"})
    ans = blind_answers(B) if (B / "blind").exists() else {}
    pairs = [("tipo_procedimento", "tipoprocedimento", lambda v: m_proc.get(str(v), v)),
             ("preco_base", "precoBaseProcedimento", num), ("adjudicante", "adjudicante_nif", digits),
             ("tipo_contrato", "tipoContrato", lambda v: m_tipo.get(str(v), v)), ("preco_contratual", "precoContratual", num),
             ("data_celebracao_contrato", "dataCelebracaoContrato", date), ("data_publicacao_contrato", "dataPublicacao", date),
             ("adjudicatario", "adjudicatarios_nifs", lambda v: sorted(digits(x) for x in (v if isinstance(v, list) else re.split(r"[;,]\s*", str(v))) if digits(x)))]
    c = check_c(parsed, ans, pairs) if ans else {"status": "NOT RUN"}
    facts = {}
    for f in sorted((ROOT / "data/facts/facto").glob("base-anuncios-*.jsonl")):
        for line in f.read_text(encoding="utf-8").splitlines():
            o = json.loads(line)
            facts.setdefault(o["unit"], {})[o["field"]] = o["value"]
    joined, agree, total, dis = 0, 0, 0, []
    for p in parsed:
        s = sample[p["n"]]
        if not s.get("nAnuncio"):
            continue
        key = re.sub(r"[^A-Za-z0-9]+", "-", s["nAnuncio"]).strip("-") + "." + (s.get("idINCM") or "x")
        e1 = facts.get(f"proc:base:{key}")
        if not e1:
            continue
        joined += 1
        for f in ("preco_base", "tipo_procedimento", "adjudicante", "tipo_contrato"):
            if p.get(f) is not None and e1.get(f) is not None:
                total += 1
                ok = p[f] == e1[f]
                agree += ok
                if not ok:
                    dis.append({"n": p["n"], "field": f, "contrato": p[f], "anuncio": e1[f], "unit": f"proc:base:{key}"})
    with_n = sum(1 for p in parsed if sample[p["n"]].get("nAnuncio"))
    b = {"with_nAnuncio": with_n, "joined": wilson(joined, with_n), "agreement": dict(wilson(agree, total) or {}, pass_=(agree / total >= 0.95) if total else None), "disagreements": dis}
    return {"source": "contratos", "A": a, "B": b, "C": c}


if __name__ == "__main__":
    source, out = sys.argv[1], Path(sys.argv[2])
    anuncios = sys.argv[sys.argv.index("--anuncios") + 1] if "--anuncios" in sys.argv else None
    res = score_ted(out, anuncios) if source == "ted" else score_contratos(out)
    (out / source / "score.json").write_text(json.dumps(res, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(json.dumps(res, ensure_ascii=False, indent=1)[:6000])
