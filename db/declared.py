"""What BASE's contract records declare, for the engine (DECISIONS D96): the contracts an agregada rule sums, the regime
the entity declared, and the buyer's declared activity of the special sectors.

    .venv/bin/python -I db/declared.py cache OUT.jsonl            ccp.base_contrato -> one compact line per contract (read once)
    .venv/bin/python -I db/declared.py facts CACHE.jsonl [--write] the declared facts per procedure; --write loads them (ccp.facto)
    .venv/bin/python -I db/declared.py stats CACHE.jsonl          the regimes and activities declared, counted

records(path or conn) -> [record]   the fields engine/aggregate.py reads, with "fundp" = db/fundamento.passages(fundamentação)
facts(records, at) -> [facto]       per procedure (proc:base:idproc-<id>):
    regime_declarado          the acts BASE's «regime» names, by their short ids (db/fundamento.act_short): «Código dos
                              Contratos Públicos (DL111-B/2017) e Lei n.º 30/2021, de 21.05» -> ["ccp", "lei-30-2021"]. The
                              decree-laws that approve or republish the Code (DL 18/2008, DL 111-B/2017) name the Code itself.
    atividade_setor_especial  the activities of the special sectors the adjudicante declared in the EU's Official Journal under
                              Directive 2014/25/EU (db/ted_sectors.py OUT.json, by NIF), cited by the notice that says so.
                              BASE's adjudicante.atividadeEntidade gives no such value (2026-11-13: its 11 values are all
                              the eForms authority-activity list; none for IP, NAV, EEM, APS, Metropolitano de Lisboa)
Each fact cites its contract's raw (raw:base-contratos:contrato:<id>) and the field it read. Declared, never checked:
what the entity said, read word by word; the engine abstains on it (product_rule:regime-especial-declarado), it does not
decide with it.
"""
import argparse
import collections
import json
import re
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path[:0] = [str(ROOT), str(ROOT / "db")]
import fundamento  # noqa: E402
DOCS_FIELD = "fundamento_nos_documentos"

VERSION = "ccp-declared-0.1"
ADAPTER = "adaptador:base-declarado@1"
SOURCE = "base-declarado"
CODE_DECREES = {"dl-18-2008", "dl-111-b-2017"}  # the decree-laws that approve (2008) and republish (2017) the Code


def _nifs(xs):
    out = []
    for x in xs or []:
        out.append(str(x.get("nifEntContrato") or "").strip() if isinstance(x, dict) else str(x).split(" - ")[0].strip())
    return out


def reduce(cid, ano, raw, d):
    """One BASE record (base_detail.unpack) as the line the engine reads."""
    adj = d.get("adjudicante") or []
    a0 = adj[0] if adj and isinstance(adj[0], dict) else {}
    return {"id": cid, "ano": ano, "raw": raw, "proc": d.get("idprocedimento"), "adjudicante": _nifs(adj), "adjudicatarios": _nifs(d.get("adjudicatarios")),
            "preco": d.get("precoContratual"), "fund": d.get("fundamentacao"), "tp": d.get("tipoprocedimento"), "tc": d.get("tipoContrato"),
            "dadj": d.get("dataDecisaoAdjudicacao"), "dcel": d.get("dataCelebracaoContrato"), "dpub": d.get("dataPublicacao"),
            "regime": d.get("regime"), "atividade": a0.get("atividadeEntidade"), "tipoEnt": a0.get("tipoEntidade")}


def cache(conn, out):
    import base_detail
    conn.execute("set statement_timeout = 0")
    cur = conn.cursor(name="declared")
    cur.itersize = 5000
    cur.execute("select id, ano, raw, doc from ccp.base_contrato")
    n, t = 0, time.time()
    with open(out, "w", encoding="utf-8") as f:
        for cid, ano, raw, doc in cur:
            f.write(json.dumps(reduce(cid, ano, raw, base_detail.unpack(bytes(doc))), ensure_ascii=False) + "\n")
            n += 1
            if n % 200000 == 0:
                print(f"... {n} contracts, {time.time() - t:.0f} s", file=sys.stderr, flush=True)
    return n


def records(path, keep=None):
    """The cache's lines, each with fundp; keep(record) -> bool drops the ones a caller cannot use (memory)."""
    out = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            r = json.loads(line)
            if keep and not keep(r):
                continue
            r["fundp"] = fundamento.passages(r["fund"]) if r.get("fund") else []
            out.append(r)
    return out


def may_count(r):
    """A record an art. 19.º / 20.º-based aggregate can count or be uncertain about: a basis naming those articles, a
    basis with words that name no article, or none; or a record of a procedure that may itself be judged."""
    f = (r.get("fund") or "")
    if not f.strip():
        return True
    if re.search(r"(?i)\bartigos?\s+(19|20)\b", f):
        return True
    return all(p.startswith("?:") for p in fundamento.passages(f))


def regime_acts(text):
    """The acts a BASE regime label names, by short id, as written: «Código dos Contratos Públicos (DL111-B/2017) e Lei n.º
    30/2021, de 21.05» -> [ccp, lei-30-2021]; «Medidas Especiais de Contratação Pública (Lei n.º 30/2021, de 21.05)» ->
    [lei-30-2021]; «Decreto-Lei n.º 10-A/2020, de 13.03» -> [dl-10-a-2020]."""
    acts = []
    for m in fundamento.ACT.finditer(" ".join((text or "").split())):
        a = fundamento.act_short(m)
        a = "ccp" if a in CODE_DECREES else a
        if a not in acts:
            acts.append(a)
    return sorted(acts)


def facts(recs, at, sectors=None):
    """sectors: db/ted_sectors.py's by_nif ({NIF: {activity: {"first": {"raw", "date"}, ...}}}), or None."""
    by_proc = collections.defaultdict(list)
    for r in recs:
        if r.get("proc"):
            by_proc[str(r["proc"])].append(r)
    out = []
    for proc, rs in sorted(by_proc.items()):
        unit = f"proc:base:idproc-{proc}"
        rs = sorted(rs, key=lambda r: int(r["id"]))
        first = next((r for r in rs if r.get("regime")), None)
        if first:
            acts = sorted({a for r in rs if r.get("regime") for a in regime_acts(r["regime"])})
            if acts:
                out.append(fact(unit, "regime_declarado", acts, first, "regime", at))
        nif = next((a for r in rs for a in (r.get("adjudicante") or []) if a), None)
        acts = (sectors or {}).get(nif) or {}
        if acts:
            first = min((x["first"] for x in acts.values()), key=lambda x: x["date"])
            out.append({**fact(unit, "atividade_setor_especial", "; ".join(sorted(acts)), rs[0], "ContractingActivity", at),
                        "origin": {"raw": first["raw"], "field": "CE_ACTIVITY / ActivityTypeCode (Directive 2014/25/EU)"},
                        "adapter": "adaptador:ted-setores@1", "valid_at": first["date"] or at[:10]})
    return out


def fact(unit, field, value, rec, src_field, at):
    raw = rec.get("raw") or f"raw:base-contratos:contrato:{rec['id']}"
    return {"id": f"facto:{unit.replace(':', '-')}:{field}:{SOURCE}", "revision": 1, "recorded_at": at, "unit": unit, "field": field, "value": value,
            "origin": {"raw": raw, "field": src_field}, "adapter": ADAPTER, "valid_at": str(rec.get("dpub") or at)[:10], "known_at": at}


ESTADO = {"A": ("verificado", "GERAL"), "B": ("medidas_especiais", "ESPECIAL"), "E": ("outra_base", "OUTRA"), "C": ("nao_identificado", None)}


def documents(results, log_path, at):
    """D97: the facts fundamento_nos_documentos (and the raws of the documents they quote) from
    adapters/plataformas/check_regime.py's results and its request log (url, sha256 and time of each document)."""
    by_sha = {}
    for line in Path(log_path).read_text(encoding="utf-8").splitlines():
        e = json.loads(line)
        if e.get("status") == 200 and e.get("sha256"):
            by_sha.setdefault(e["sha256"], e)
    raws, facts = {}, []
    for x in results:
        if x.get("grupo") not in ESTADO:
            continue
        estado, key = ESTADO[x["grupo"]]
        q = (x["encontrado"].get(key) or [None])[0] if key else None
        e = by_sha.get(q["sha256"]) if q else None
        if e is None:  # a member of a pieces ZIP, or a «not identified» case: the platform's ZIP or BASE's contract document
            url = x.get("link") if q and not q["ficheiro"].startswith("BASE:") else None
            e = next((by_sha[s] for s in by_sha if by_sha[s]["url"] == url), None) if url else None
        if e is None:  # BASE's contract document: its id from the portal's detail response (an index kept outside the raws)
            sys.path.insert(0, str(ROOT / "adapters/plataformas"))
            import check_regime
            det = next((v for v in reversed(list(by_sha.values())) if (v.get("post") or {}).get("id") == str(x["contrato"])), None)
            docs = json.loads((check_regime.INDEX / det["sha256"]).read_bytes()).get("documents") or [] if det else []
            urls = [f"https://www.base.gov.pt/Base4/pt/resultados/?type=doc_documentos&id={d['id']}&ext=.pdf" for d in docs]
            e = next((v for v in by_sha.values() if v["url"] in urls), None)
        if e is None:
            continue  # nothing read to cite
        sys.path.insert(0, str(ROOT / "adapters/plataformas"))
        import check_regime
        rid = check_regime.raw_id(e)  # the raw record adapters/plataformas/check_regime.py raws writes for these bytes
        raws[rid] = next(r for r in check_regime.raw_records(log_path) if r["id"] == rid)
        value = {"estado": estado, "lidos": len(x.get("lidos") or [])}
        if q:
            t = " ".join(q["texto"].split())
            a, b = t.find(" ", 40), t.rfind(" ", 0, 300)  # whole words, about the middle of check_regime's ±160 characters
            value.update(citacao=t[a + 1:b if b > a else None].strip(), documento=q["ficheiro"], pagina=q["pagina"], url=e["url"])
        facts.append({"id": f"facto:{x['unit'].replace(':', '-')}:{DOCS_FIELD}:check-regime", "revision": 1, "recorded_at": at, "unit": x["unit"],
                      "field": DOCS_FIELD, "value": value, "origin": {"raw": rid, "field": q["ficheiro"] if q else "documentos lidos"},
                      "adapter": "adaptador:check-regime@1", "valid_at": e["at"][:10], "known_at": at})
    return list(raws.values()), facts


def adapter_objects(at):
    return [adapter_object(at), {"id": "adaptador:ted-setores@1", "revision": 1, "recorded_at": at, "source": "ted", "version": 1, "code": "db/ted_sectors.py",
            "mapping": [{"source_field": "CE_ACTIVITY / ContractingActivity.ActivityTypeCode", "canonical_field": "atividade_setor_especial", "transform": "identity",
                         "note": "D96: the activity the buyer declared in notices under Directive 2014/25/EU, by NIF; the procedure's adjudicante"}],
            "coverage": [], "proposed_by": "ferramenta:ted-sectors@1", "state": "proposed"},
            {"id": "adaptador:check-regime@1", "revision": 1, "recorded_at": at, "source": "plataformas", "version": 1, "code": "adapters/plataformas/check_regime.py",
             "mapping": [{"source_field": "the procedure's documents (BASE contract, platform pieces)", "canonical_field": DOCS_FIELD, "transform": "identity",
                          "note": "D97: verificado / medidas_especiais / outra_base / nao_identificado, with the quote, the document and its page"}],
             "coverage": [], "proposed_by": "ferramenta:check-regime@1", "state": "proposed"}]


def adapter_object(at):
    return {"id": ADAPTER, "revision": 1, "recorded_at": at, "source": SOURCE, "version": 1, "code": "db/declared.py",
            "mapping": [{"source_field": "regime", "canonical_field": "regime_declarado", "transform": "identity",
                         "note": "D96: the acts the entity declared as the regime, by short id; the Code's own decree-laws name the Code"},
],
            "coverage": [], "proposed_by": "ferramenta:declared@1", "state": "proposed"}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["cache", "facts", "stats", "documents"])
    ap.add_argument("--log", default=str(ROOT / "adapters/plataformas/check-log.jsonl"))
    ap.add_argument("path")
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--sectors", help="db/ted_sectors.py OUT.json")
    ap.add_argument("--only-blocking", action="store_true", help="D96: regime_declarado only where it lacks the Code (the only ones that change a verdict)")
    a = ap.parse_args()
    if a.cmd == "cache":
        import pg
        print(json.dumps({"tool": VERSION, "contracts": cache(pg.connect(), a.path)}))
        return
    if a.cmd == "documents":  # D97: a.path = check_regime.py's results
        at = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        raws, fs = documents(json.loads(Path(a.path).read_text(encoding="utf-8"))["casos"], a.log, at)
        print(json.dumps({"tool": VERSION, "raws": len(raws), "facts": len(fs), "by_estado": collections.Counter(f["value"]["estado"] for f in fs)}, ensure_ascii=False))
        if a.write:
            import pg
            conn = pg.connect()
            print(pg.load_objects(conn, {"adaptador": adapter_objects(at), "raw": raws, "facto": fs}))
            conn.commit()
        else:
            print(json.dumps(fs[0], ensure_ascii=False, indent=1)[:900])
        return
    recs = records(a.path)
    if a.cmd == "stats":
        reg = collections.Counter(r.get("regime") for r in recs)
        act = collections.Counter(r.get("atividade") for r in recs)
        print(json.dumps({"regime": reg.most_common(30), "atividade": act.most_common(40)}, ensure_ascii=False, indent=1))
        return
    at = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    fs = facts(recs, at, json.loads(Path(a.sectors).read_text(encoding="utf-8"))["by_nif"] if a.sectors else None)
    if a.only_blocking:  # a regime that includes the Code changes no verdict (product_rule:regime-especial-declarado): not loaded
        fs = [f for f in fs if f["field"] != "regime_declarado" or "ccp" not in f["value"]]
    print(json.dumps({"tool": VERSION, "facts": len(fs), "by_field": collections.Counter(f["field"] for f in fs),
                      "values": collections.Counter(json.dumps(f["value"], ensure_ascii=False) for f in fs).most_common(20)}, ensure_ascii=False, indent=1))
    if a.write:
        import pg
        conn = pg.connect()
        print(pg.load_objects(conn, {"adaptador": adapter_objects(at), "facto": fs}))
        conn.commit()


if __name__ == "__main__":
    main()
