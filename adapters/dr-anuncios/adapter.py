"""Diário da República notice PDFs of the BASE procedures -> raw + documento objects, facts with position, conflicts.

    /usr/bin/python3 -I adapters/dr-anuncios/adapter.py fetch [--limit N]       one GET every 10 s, resumable
    /usr/bin/python3 -I adapters/dr-anuncios/adapter.py text                    pypdf text layer of every stored PDF
    .venv/bin/python -I adapters/dr-anuncios/adapter.py build --recorded-at T --principal P
    .venv/bin/python -I adapters/dr-anuncios/adapter.py check
    .venv/bin/python -I adapters/dr-anuncios/adapter.py register --at T

fetch   the procedures are the proc units of adaptador:base-anuncios; each one's notice URL is the `url` field of its
        record (the raw slice in data/raw_bytes/). Only files.diariodarepublica.pt PDFs are read. One GET every 10 s
        with the User-Agent below; a 403 or 429 stops the run and is logged, and fetch refuses to start until an hour
        after the last refusal; network errors are logged and retried by the next run; a stored PDF is never fetched
        again. Bytes go to data/raw/dr-anuncios/raw_bytes/<sha256> (gitignored), every attempt to fetch-log.jsonl.
text    for each stored PDF, the text layer exactly as the E1b test made it (pypdf, page by page, extract_text), kept
        per page in data/raw/dr-anuncios/text/<sha256>.json (gitignored). Runs on the interpreter and pypdf of the test.
build   reads the fetch log and the text, runs the frozen parser (parse.py, sha256 checked) on the joined pages, finds
        each value's position with the parser's own patterns, and writes: one raw and one documento per PDF, the facts
        of mapping.json with origin (documento, page, offsets in that page's text, quote), and a conflito where the
        notice's deadline date differs from the dump's fact. Plus COVERAGE.md. Same inputs, same bytes.
check   rebuilds in memory and compares every file byte for byte.
register registers this file as ferramenta:adapter-dr-anuncios and proposes (or corrects) the adaptador in the log.

No model reads anything. Nothing is sent: GET only.
"""
import argparse
import datetime
import hashlib
import json
import os
import re
import shutil
import sys
import time
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
DATA = ROOT / "data"
PDF_DIR = DATA / "raw/dr-anuncios/raw_bytes"
TEXT_DIR = DATA / "raw/dr-anuncios/text"
LOG = HERE / "fetch-log.jsonl"
VERSION = "dr-anuncios-adapter-0.1"
SOURCE = "dr-anuncios"
TOOL = "adapter-dr-anuncios"
USER_AGENT = "ccp-engine research (passive read)"
PACE_S = 10.0
REFUSAL_WAIT_S = 3600
DR_PDF = re.compile(r"https://files\.diariodarepublica\.pt/\S+\.pdf")
CUT_WORDS = {"a", "da", "das", "de", "do", "dos", "e", "o", "por", "uma", "um"}
PARSER_SHA256 = "a29220df924331dbda8cb7d8d83c1d45e06ab58b2e28631f0c5e4532879612e3"
MAPPING = json.loads((HERE / "mapping.json").read_text(encoding="utf-8"))


def now_utc():
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


# ---- the procedures and their notice URLs (from adaptador:base-anuncios's raws) ---------------------------------------
def procedures():
    """[(key, unit id, record raw id, record dict, record raw)] sorted by key, from data/raw/base-anuncios/raw/."""
    out = []
    for f in sorted((DATA / "raw/base-anuncios/raw").glob("base-anuncios-2*.jsonl")):
        for line in f.read_text(encoding="utf-8").splitlines():
            r = json.loads(line)
            if r["kind"] != "anuncio":
                continue
            rec = json.loads((DATA / r["bytes"]).read_bytes().decode("utf-8"))
            key = r["id"].split(":", 3)[3]
            out.append((key, f"proc:base:{key}", r["id"], rec, r))
    return sorted(out, key=lambda x: x[0])


def read_log():
    if not LOG.exists():
        return []
    return [json.loads(l) for l in LOG.read_text(encoding="utf-8").splitlines() if l.strip()]


def stored(log):
    """{key: last ok log entry whose bytes are on disk}."""
    out = {}
    for e in log:
        if e.get("status") == 200 and e.get("sha256") and (PDF_DIR / e["sha256"]).exists():
            out[e["key"]] = e
    return out


# ---- fetch ---------------------------------------------------------------------------------------------------------
NEW_REGIME = "2026-10"


def priority_order(items):
    """Order of the download (the pace does not change): first the notices published since 2026-10-01 (the new regime),
    then the other months interleaved, one notice of each month in turn, so every month's coverage grows together."""
    def month(dpub):
        return f"{dpub[6:10]}-{dpub[3:5]}" if len(dpub) == 10 else "sem-data"
    first = [x for x in items if month(x[2]) >= NEW_REGIME]
    by_month = defaultdict(list)
    for x in items:
        if month(x[2]) < NEW_REGIME:
            by_month[month(x[2])].append(x)
    rest = []
    queues = [by_month[m] for m in sorted(by_month)]
    for i in range(max((len(q) for q in queues), default=0)):
        rest.extend(q[i] for q in queues if i < len(q))
    return first + rest


def cmd_fetch(a):
    import socket
    import urllib.error
    import urllib.request
    log = read_log()
    refusals = [e for e in log if e.get("status") in (403, 429)]
    if refusals:
        last = datetime.datetime.strptime(refusals[-1]["at"], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=datetime.timezone.utc)
        wait = REFUSAL_WAIT_S - (datetime.datetime.now(datetime.timezone.utc) - last).total_seconds()
        if wait > 0:
            print(f"last refusal {refusals[-1]['status']} at {refusals[-1]['at']}; resume no sooner than {int(wait)} s from now")
            return 3
    done = stored(log)
    gone = {e["key"] for e in log if e.get("status") == 404}
    todo = [(k, rec["url"], rec.get("dataPublicacao") or "") for k, _, _, rec, _ in procedures()
            if DR_PDF.fullmatch(rec.get("url") or "") and k not in done and k not in gone]
    todo = [(k, u) for k, u, _ in priority_order(todo)]
    if a.limit:
        todo = todo[:a.limit]
    print(f"{len(done)} stored, {len(todo)} to fetch, one GET every {PACE_S:g} s", flush=True)
    PDF_DIR.mkdir(parents=True, exist_ok=True)
    last_start = 0.0
    with open(LOG, "a", encoding="utf-8") as logf:
        for i, (key, url) in enumerate(todo):
            if shutil.disk_usage(PDF_DIR).free < 1_000_000_000:
                print("less than 1 GB free on disk; stopping", flush=True)
                return 4
            pause = PACE_S - (time.monotonic() - last_start)
            if pause > 0:
                time.sleep(pause)
            last_start = time.monotonic()
            at = now_utc()
            entry = {"key": key, "url": url, "at": at}
            try:
                req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT}, method="GET")
                with urllib.request.urlopen(req, timeout=60) as resp:
                    body = resp.read()
                    entry["status"] = resp.status
                if not body.startswith(b"%PDF"):
                    entry.update(status=entry["status"], error="not a PDF", bytes=len(body))
                else:
                    digest = sha256(body)
                    tmp = PDF_DIR / f".{digest}.part"
                    tmp.write_bytes(body)
                    os.replace(tmp, PDF_DIR / digest)
                    entry.update(sha256=digest, bytes=len(body))
            except urllib.error.HTTPError as exc:
                entry.update(status=exc.code, error=str(exc.reason))
            except (urllib.error.URLError, socket.timeout, TimeoutError, ConnectionError, OSError) as exc:
                entry.update(status=None, error=f"network: {exc!r}"[:300])
            logf.write(json.dumps(entry, ensure_ascii=False, sort_keys=True) + "\n")
            logf.flush()
            if entry.get("status") in (403, 429):
                print(f"{at} refused with {entry['status']} on {key}; stopped (resume no sooner than one hour)", flush=True)
                return 2
            if i % 100 == 0:
                print(f"{at} {i + 1}/{len(todo)} {key} {entry.get('status')}", flush=True)
    print(f"{now_utc()} fetch finished", flush=True)
    return 0


# ---- text ----------------------------------------------------------------------------------------------------------
def cmd_text(a):
    import site
    sys.path.append(site.getusersitepackages())  # -I keeps the cwd and script dir out; pypdf of the test lives in the user site
    import pypdf
    if pypdf.__version__ != "6.14.2":
        raise SystemExit(f"pypdf {pypdf.__version__}; the E1b test ran 6.14.2")
    TEXT_DIR.mkdir(parents=True, exist_ok=True)
    n = 0
    for e in stored(read_log()).values():
        out = TEXT_DIR / f"{e['sha256']}.json"
        if out.exists():
            continue
        try:
            pages = [(pg.extract_text() or "") for pg in pypdf.PdfReader(str(PDF_DIR / e["sha256"])).pages]
            doc = {"pages": pages, "error": None}
        except Exception as exc:  # a PDF pypdf cannot read is counted, never guessed
            doc = {"pages": [], "error": repr(exc)[:500]}
        doc["pypdf"] = pypdf.__version__
        out.write_text(json.dumps(doc, ensure_ascii=False), encoding="utf-8")
        n += 1
    print(f"text: {n} new, pypdf {pypdf.__version__}, python {sys.version.split()[0]}")
    return 0


# ---- build ---------------------------------------------------------------------------------------------------------
def frozen_parser():
    src = (HERE / "parse.py").read_bytes()
    if sha256(src) != PARSER_SHA256:
        raise SystemExit("adapters/dr-anuncios/parse.py is not the parser the E1b test froze (sha256 differs)")
    sys.path.insert(0, str(HERE))
    import parse  # noqa: E402  (frozen: sha256 a29220df…, checked above)
    sys.path.pop(0)
    return parse


def dump_facts():
    """{unit id: {field: facto}} of adaptador:base-anuncios for the fields build needs."""
    out = defaultdict(dict)
    for f in sorted((DATA / "facts/facto").glob("base-anuncios-*.jsonl")):
        for line in f.read_text(encoding="utf-8").splitlines():
            o = json.loads(line)
            if o["field"] in ("data_publicacao_anuncio", "data_limite_propostas", "adjudicante"):
                out[o["unit"]][o["field"]] = o
    return out


def span_of(parse, pfield, text):
    """(start, end) of the value the parser read, by the parser's own pattern: the first match, as parse() takes it."""
    m = re.search(parse.PATTERNS[pfield], text)
    if not m:
        return None, None
    if pfield in ("data_envio_anuncio", "prazo_propostas_data"):
        return (m.start(1), m.end(3)), m
    s, e = m.start(1), m.end(1)
    value = m.group(1)
    s += len(value) - len(value.lstrip())
    e -= len(value) - len(value.rstrip())
    return (s, e), m


def to_page(pages, s, e):
    """Joined-text offsets -> (page number from 1, offsets in that page's text); None when the span crosses a page break."""
    base = 0
    for n, p in enumerate(pages, 1):
        if s < base + len(p) + 1:
            if e > base + len(p):
                return None
            return n, s - base, e - base
        base += len(p) + 1
    return None


def territorio_of(nut):
    table = MAPPING["territorio_by_nut_iii_prefix"]
    return next((table[p] for p in sorted(table, key=len, reverse=True) if nut.startswith(p)), None)


def build(recorded_at, principal):
    from engine import schema
    from engine.canon import canonical
    parse = frozen_parser()
    log = read_log()
    ok = stored(log)
    last = {}
    for e in log:
        last[e["key"]] = e
    base = dump_facts()
    adaptador_id = MAPPING["adaptador"]["id"]
    rows = {m["canonical_field"]: m for m in MAPPING["adaptador"]["mapping"]}
    files = {}
    st = {"procs": 0, "expected_by_month": Counter(), "docs_by_month": Counter(), "not_read": defaultdict(list), "field": defaultdict(Counter),
          "omitted": defaultdict(lambda: defaultdict(list)), "conflicts": defaultdict(list), "cross": Counter(), "cross_ex": defaultdict(list),
          "territorio_parser_differs": 0, "envio_minus_pub": Counter(), "joue": Counter(), "territorio": Counter(), "norma": Counter()}
    out = defaultdict(lambda: {"raw": [], "documento": [], "facto": [], "conflito": []})
    seen_sha = {}
    for key, unit, rec_raw_id, rec, rec_raw in procedures():
        st["procs"] += 1
        pub = base[unit].get("data_publicacao_anuncio")
        month = pub["value"][:7] if pub else "sem-data"
        url = rec.get("url") or ""
        if not DR_PDF.fullmatch(url):
            host = re.sub(r"^https?://([^/#]+).*$", r"\1", url) if url else "(empty)"
            st["not_read"][f"url is not a files.diariodarepublica.pt PDF ({host})"].append(rec["nAnuncio"])
            continue
        st["expected_by_month"][month] += 1
        if key not in ok:
            e = last.get(key)
            reason = ("not fetched yet" if e is None else f"refused {e['status']}" if e.get("status") in (403, 429)
                      else f"HTTP {e['status']}" if e.get("status") not in (None, 200) else (e.get("error") or "unknown").split(":")[0])
            st["not_read"][reason].append(rec["nAnuncio"])
            continue
        e = ok[key]
        bucket = out[month]
        raw_id = f"raw:{SOURCE}:anuncio-pdf:{key}"
        bucket["raw"].append({"id": raw_id, "revision": 1, "recorded_at": recorded_at, "source": SOURCE, "kind": "anuncio-pdf",
                              "source_id": rec["IdIncm"], "sha256": e["sha256"], "bytes": f"raw_bytes/{e['sha256']}", "media_type": "application/pdf",
                              "encoding": "binary", "url": url, "captured_at": e["at"], "request": {"method": "GET", "reads_of_page": 1}})
        tpath = TEXT_DIR / f"{e['sha256']}.json"
        if not tpath.exists():
            st["not_read"]["text not extracted yet"].append(rec["nAnuncio"])
            continue
        tdoc = json.loads(tpath.read_text(encoding="utf-8"))
        if tdoc["error"]:
            st["not_read"]["pypdf could not read the PDF"].append(rec["nAnuncio"])
            continue
        if e["sha256"] in seen_sha:
            st["not_read"][f"same PDF bytes as another procedure's notice"].append(rec["nAnuncio"])
            continue
        seen_sha[e["sha256"]] = key
        pages = tdoc["pages"]
        text = "\n".join(pages)
        doc_id = f"doc:{e['sha256']}"
        bucket["documento"].append({"id": doc_id, "revision": 1, "recorded_at": recorded_at, "sha256": e["sha256"], "raw": raw_id,
                                    "pages": max(1, len(pages)), "has_text_layer": bool(text.strip()), "origin": {"unit": unit, "piece": "anuncio", "url": url}})
        st["docs_by_month"][month] += 1
        if not text.strip():
            st["not_read"]["no text layer"].append(rec["nAnuncio"])
            continue
        vals = parse.parse(text)
        if vals["nut_iii"] and territorio_of(vals["nut_iii"]) != vals["territorio"]:
            st["territorio_parser_differs"] += 1
        facts = {}
        for field, pfield in MAPPING["parser_field"].items():
            v = vals[pfield]
            if v is None:
                st["omitted"][field][f"label not in the notice text ({rec.get('modeloAnuncio')})"].append(rec["nAnuncio"])
                continue
            span, m = span_of(parse, pfield, text)
            pos = to_page(pages, *span)
            if pos is None:
                st["omitted"][field]["the value crosses a page break"].append(rec["nAnuncio"])
                continue
            page, s, en = pos
            quote = pages[page - 1][s:en]
            if field == "publicado_joue":
                value = MAPPING["boolean"][v]
            elif field == "territorio":
                value = territorio_of(v)
            else:
                value = v
            f = {"id": f"facto:{unit.replace(':', '-')}:{field}:{SOURCE}", "revision": 1, "recorded_at": recorded_at, "unit": unit, "field": field,
                 "value": value, "origin": {"documento": doc_id, "page": page, "offsets": {"start": s, "end": en}, "quote": quote},
                 "adapter": adaptador_id, "valid_at": pub["value"] if pub else vals["data_envio_anuncio"] or e["at"][:10], "known_at": e["at"]}
            facts[field] = (f, m)
            bucket["facto"].append(f)
            st["field"][field][month] += 1
        if "publicado_joue" in facts:
            st["joue"][vals["publicado_joue"]] += 1
        if "territorio" in facts:
            st["territorio"][facts["territorio"][0]["value"]] += 1
        if "norma_juridica_adjudicante" in facts:
            st["norma"][vals["norma_juridica"]] += 1
        if "data_envio_anuncio" in facts and pub:
            st["envio_minus_pub"][(datetime.date.fromisoformat(vals["data_envio_anuncio"]) - datetime.date.fromisoformat(pub["value"])).days] += 1
        # cross-checks against the dump (reported, not facts)
        dnif = base[unit].get("adjudicante", {}).get("value")
        if vals["nif"] and dnif:
            same = vals["nif"] == dnif
            st["cross"][f"nif {'equal' if same else 'differs'}"] += 1
            if not same:
                st["cross_ex"]["nif differs"].append(rec["nAnuncio"])
        dl = base[unit].get("data_limite_propostas")
        if "data_limite_propostas" in facts and dl:
            pf, m = facts["data_limite_propostas"]
            if pf["value"] == dl["value"]:
                st["cross"]["data_limite_propostas equal"] += 1
            else:
                after = text[m.end(3):m.end(3) + 12]
                hhmm = re.match(r"\s*(\d{2}:\d{2})", after)
                delta = (datetime.date.fromisoformat(pf["value"]) - datetime.date.fromisoformat(dl["value"])).days
                kind = f"notice {delta:+d} day(s) from the dump" + (f", notice time {hhmm.group(1)}" if hhmm and hhmm.group(1) == "00:59" else ", notice time " + (hhmm.group(1) if hhmm else "not printed") if delta == 1 else "")
                st["conflicts"][kind].append(rec["nAnuncio"])
                bucket["conflito"].append({"id": f"conflito:{unit.replace(':', '-')}:data_limite_propostas", "revision": 1, "recorded_at": recorded_at,
                                           "unit": unit, "field": "data_limite_propostas",
                                           "values": [{"facto": dl["id"], "value": dl["value"], "source": "base-anuncios", "known_at": dl["known_at"]},
                                                      {"facto": pf["id"], "value": pf["value"], "source": SOURCE, "known_at": pf["known_at"]}],
                                           "resolution": {"kind": "nao_avaliado"}})
    for month, b in sorted(out.items()):
        tag = f"{SOURCE}-{month}"
        for type_, objs in (("raw", b["raw"]), ("documento", b["documento"]), ("facto", b["facto"]), ("conflito", b["conflito"])):
            if objs:
                rel = f"raw/{SOURCE}/raw/{tag}.jsonl" if type_ == "raw" else f"facts/{type_}/{tag}.jsonl"
                files[rel] = "".join(canonical(o) + "\n" for o in sorted(objs, key=lambda o: o["id"])).encode("utf-8")
    a = MAPPING["adaptador"]
    adaptador = {"id": a["id"], "revision": 1, "recorded_at": recorded_at, "source": a["source"], "version": a["version"], "code": a["code"],
                 "mapping": a["mapping"], "coverage": [{"period": m, "expected": st["expected_by_month"][m], "captured": st["docs_by_month"][m]}
                                                        for m in sorted(st["expected_by_month"])],
                 "proposed_by": principal, "state": "proposed"}
    files[f"facts/adaptador/{SOURCE}-{a['version']}.json"] = (json.dumps(adaptador, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    for rel, data in files.items():
        type_ = Path(rel).parent.name
        lines = data.decode("utf-8").splitlines() if rel.endswith(".jsonl") else [data.decode("utf-8")]
        for l in lines if rel.endswith(".jsonl") else lines:
            o = json.loads(l)
            errs = schema.validate(type_, o)
            if errs:
                raise SystemExit(f"{rel}: {o.get('id')}: {errs[0]}")
    st["log"] = Counter("ok" if e.get("status") == 200 and e.get("sha256") else f"HTTP {e['status']}" if e.get("status") else "network" for e in log)
    st["first_at"] = log[0]["at"] if log else None
    st["last_at"] = log[-1]["at"] if log else None
    return files, st


def coverage_md(st):
    months = sorted(st["expected_by_month"])
    docs = sum(st["docs_by_month"].values())
    expected = sum(st["expected_by_month"].values())
    pct = lambda k, n: f"{100 * k / n:.1f} %" if n else "-"  # noqa: E731
    L = ["# DR notice PDFs: coverage of adaptador:dr-anuncios@1", "",
         f"Generated by `adapters/dr-anuncios/adapter.py` ({VERSION}); `adapter.py check` re-derives it byte for byte. Text by pypdf 6.14.2 on",
         "Python 3.9.6 (the E1b test's versions); values by the frozen parser parse.py (sha256 a29220df…), unchanged.", "",
         "## Download", "",
         f"- Fetch attempts logged: {sum(st['log'].values())} ({', '.join(f'{k} {v}' for k, v in sorted(st['log'].items()))}), from {st['first_at']} to {st['last_at']};"
         " one GET every 10 s, User-Agent «ccp-engine research (passive read)».",
         f"- Procedures (proc units of adaptador:base-anuncios@1): {st['procs']}; with a files.diariodarepublica.pt notice PDF: {expected}.",
         f"- Notices read into a `documento` (with its `raw`): {docs} ({pct(docs, expected)} of those with a DR PDF).",
         f"- Conflicts written (notice vs dump, data_limite_propostas): {sum(len(v) for v in st['conflicts'].values())}.", "",
         "| month (dataPublicacao) | procedures with a DR PDF | documents read |", "|---|---:|---:|"]
    for m in months:
        L.append(f"| {m} | {st['expected_by_month'][m]} | {st['docs_by_month'][m]} |")
    L += ["", "## Procedures whose notice was not read, by reason", "", "| reason | procedures | three examples (nAnuncio) |", "|---|---:|---|"]
    for reason, ids in sorted(st["not_read"].items(), key=lambda kv: (-len(kv[1]), kv[0])):
        L.append(f"| {reason} | {len(ids)} | {', '.join(ids[:3])} |")
    L += ["", "## Procedures carrying each fact from the notice, per month", "",
          "| field | " + " | ".join(months) + " | total | of documents read |", "|---|" + "---:|" * (len(months) + 2)]
    for field in MAPPING["parser_field"]:
        c = st["field"].get(field, Counter())
        total = sum(c.values())
        L.append(f"| {field} | " + " | ".join(str(c.get(m, 0)) for m in months) + f" | {total} | {pct(total, docs)} |")
    L += ["", "## Documents read without a fact for a field, by reason", "", "| field | reason | documents | three examples (nAnuncio) |", "|---|---|---:|---|"]
    for field in MAPPING["parser_field"]:
        for reason, ids in sorted(st["omitted"].get(field, {}).items(), key=lambda kv: (-len(kv[1]), kv[0])):
            L.append(f"| {field} | {reason} | {len(ids)} | {', '.join(ids[:3])} |")
    L += ["", "## Conflicts with the dump, by kind (data_limite_propostas; resolution nao_avaliado, neither value chosen)", "",
          "| kind | conflicts | three examples (nAnuncio) |", "|---|---:|---|"]
    for kind, ids in sorted(st["conflicts"].items(), key=lambda kv: (-len(kv[1]), kv[0])):
        L.append(f"| {kind} | {len(ids)} | {', '.join(ids[:3])} |")
    L += ["", "## Cross-checks with the dump (not facts)", ""]
    for k, v in sorted(st["cross"].items()):
        L.append(f"- {k}: {v}" + (f" (e.g. {', '.join(st['cross_ex'][k][:3])})" if st["cross_ex"].get(k) else ""))
    L.append(f"- territorio by the mapping vs the parser's own: {st['territorio_parser_differs']} differ.")
    L += ["", "## Values", "",
          f"- publicado_joue: {dict(sorted(st['joue'].items()))}.",
          f"- territorio: {dict(sorted(st['territorio'].items()))}.",
          f"- data_envio_anuncio minus data_publicacao_anuncio, in days: {dict(sorted(st['envio_minus_pub'].items()))}.",
          "- norma_juridica_adjudicante (stored as printed, not mapped to tipo_entidade): " + "; ".join(f"«{k}» {v}" for k, v in st["norma"].most_common()) + ".",
          f"- The parser reads a label's value to the end of its line, so a value that wraps in the PDF is cut: at least {sum(v for k, v in st['norma'].items() if k.split()[-1] in CUT_WORDS)} norma_juridica_adjudicante facts end in a word that cannot end the value ({', '.join(sorted(CUT_WORDS))}). The quote is exactly the printed first line; the parser is not changed.", "",
          "## Not derived", ""]
    for field, reason in MAPPING["not_derived"].items():
        L.append(f"- `{field}`: {reason}.")
    L.append("")
    return "\n".join(L)


def cmd_build(a):
    files, st = build(a.recorded_at, a.principal)
    for rel, data in sorted(files.items()):
        p = DATA / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        if not p.exists() or p.read_bytes() != data:
            p.write_bytes(data)
    (HERE / "COVERAGE.md").write_text(coverage_md(st), encoding="utf-8")
    (HERE / "build.json").write_text(json.dumps({"tool": VERSION, "recorded_at": a.recorded_at, "principal": a.principal, "fetch_log_lines": sum(st["log"].values()),
                                                 "files": len(files)}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"procs": st["procs"], "documents": sum(st["docs_by_month"].values()), "facts": sum(sum(c.values()) for c in st["field"].values()),
                      "conflicts": sum(len(v) for v in st["conflicts"].values()), "files": len(files)}))
    return 0


def cmd_check(a):
    meta = json.loads((HERE / "build.json").read_text(encoding="utf-8"))
    files, st = build(meta["recorded_at"], meta["principal"])
    bad = [rel for rel, data in sorted(files.items()) if not (DATA / rel).exists() or (DATA / rel).read_bytes() != data]
    ours = [f"raw/{SOURCE}/raw", "facts/documento", "facts/facto", "facts/conflito", "facts/adaptador"]
    extra = [str(p.relative_to(DATA)) for d in ours for p in sorted((DATA / d).glob(f"{SOURCE}*")) if str(p.relative_to(DATA)) not in files]
    if (HERE / "COVERAGE.md").read_text(encoding="utf-8") != coverage_md(st):
        bad.append("adapters/dr-anuncios/COVERAGE.md")
    for rel in bad + extra:
        print("DIFFERS" if rel in bad else "EXTRA", rel)
    print(f"check: {len(files)} files re-derived; {len(bad)} differ, {len(extra)} extra")
    return 1 if bad or extra else 0


def cmd_register(a):
    sys.path.insert(0, str(ROOT / "tools"))
    import register_tool  # noqa: E402  (the builder's registration of a ferramenta by the sha256 of its code)
    from engine.canon import content_hash
    from engine.governance import Log
    gov = ROOT / "governance"
    code = str(Path(__file__).resolve().relative_to(ROOT))
    pid = register_tool.register(gov, TOOL, code, "DR notice PDFs -> raw, documento, facts with position, conflicts (extractor E1b)")
    log = Log(gov)
    aid = MAPPING["adaptador"]["id"]
    payload = {"code": code, "code_sha256": sha256(Path(__file__).read_bytes()), "parser": "adapters/dr-anuncios/parse.py", "parser_sha256": PARSER_SHA256,
               "mapping": "adapters/dr-anuncios/mapping.json", "mapping_sha256": content_hash(MAPPING["adaptador"]["mapping"])}
    known = [ev for _, ev in log.events if ev["assertion_type"] == "adaptador" and ev["assertion"] == aid and ev["action"] in ("propose", "correct")]
    if not known:
        print(pid, log.propose(pid, "adaptador", aid, payload, a.at))
    elif known[-1]["payload"] != payload:
        rev = log.replay().assertions[("adaptador", aid)]["revision"]
        print(pid, log.correct(pid, "adaptador", aid, rev, payload, "the adapter's code changed", a.at))
    else:
        print(pid, "already proposed with this code and mapping")
    return 0


# ---- commands ------------------------------------------------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    f = sub.add_parser("fetch"); f.add_argument("--limit", type=int, default=0)
    sub.add_parser("text")
    b = sub.add_parser("build"); b.add_argument("--recorded-at", required=True); b.add_argument("--principal", required=True)
    sub.add_parser("check")
    r = sub.add_parser("register"); r.add_argument("--at", required=True)
    a = ap.parse_args()
    if a.cmd in ("build", "check", "register"):
        sys.path.insert(0, str(ROOT))
    return {"fetch": cmd_fetch, "text": cmd_text, "build": cmd_build, "check": cmd_check, "register": cmd_register}[a.cmd](a) or 0


if __name__ == "__main__":
    sys.exit(main())
