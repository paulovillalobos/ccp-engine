"""Build law/ from what was captured: normas, passages with their versions, vigencias. Nothing is fetched.

    .venv/bin/python tools/build_law.py [--store law | --store /abs/copy/of/law] [--no-history]

Inputs (all already in the store, each a raw record with bytes by hash):
    raw:dr-consolidado:lei:ccp                     the consolidated DL 18/2008 page (decree + the CCP in its annex)
    raw:dr-consolidado:artigo-historico:<id>       one opened "Ver alterações ao texto" view per article / annex
    raw:dr-consolidado:diploma:<slug>              the detail page of an act (DL 177/2026, DL 214-G/2015, ...)
Steps:
    1. the consolidated raw's working text is the history extractor's (fragments + the notes, dr-article-history@1),
       so passages and notes share one text and one set of offsets (DECISIONS D29); a raw whose text was derived by
       another extractor gets a revision with the new text (bytes unchanged)
    2. normas: norma:ccp; every act a note names (norma:<norma_slug>), its DR address read from the note's own link;
       every act with a diploma capture. source.raw = the captures the record is read from
    3. passages: engine.structure over the consolidated text (ccp:...) and over each captured act (its own articles)
    4. vigencias: engine.vigente.notes_to_vigencias over the consolidated notes (one per article and date)
    5. versions (skipped with --no-history): an article or annex added once and never changed (its only vigencia is
       an "adita") keeps the consolidated text as its one version, from that date, and its parts get the same
       vigencia; an article or annex with a history capture takes one version per date
       of that page (D24: the newest text of a date wins); its numbers, alíneas and subalíneas are structured inside
       each version and keep one version while their text does not change; a part that a version no longer has
       closes with a version whose text is the DR note of that date (the one the article's vigencia quotes), revoked
       (D30). Every part's version that starts
       on a date the article has a vigencia for gets a vigencia quoting the same note (same act, same effect)
    6. writes: a new id is appended; a changed object becomes a new revision; an equal one is left alone (the store
       is append-only: nothing is rewritten). Prints the counts and writes <store>/build-report.json: the captured acts
       not structured and why, the articles left out and why (read by tools/coverage.py).
No network, no model.
"""
import argparse
import json
import re
import sys
from collections import Counter
from html import unescape
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from engine import extract, structure, vigente  # noqa: E402
from engine.canon import sha256_text  # noqa: E402
from engine.sources import now_utc  # noqa: E402
from engine.store import Store, Writer  # noqa: E402

VERSION = "ccp-build-law-0.1"
CONSOLIDATED = "raw:dr-consolidado:lei:ccp"
TEXT_EXTRACTOR = "dr-article-history@1"
INITIAL = "2008-07-30"  # the CCP's (and DL 18/2008's) entry into force: the date of every "Versão inicial"
DR = "https://diariodarepublica.pt"
NOTE_LINK = re.compile(r'<a [^>]*href="(/dr/detalhe/[^"]+)"[^>]*>([^<]+)</a>')
ENVELOPE = ("revision", "recorded_at", "supersedes")


def act_links(html: str) -> dict:
    """{act name as the notes print it: DR address}, read from the links inside the notes of a DR page."""
    out = {}
    for href, label in NOTE_LINK.findall(html):
        name = " ".join(unescape(label).split()).split(" - Diário da República")[0].strip()
        if re.match(r"^.+ n\.º [0-9]+(?:-[A-Z]{1,2})?/(?:[0-9]{4}|[0-9]{2})(?:/[A-Z0-9])?$", name):
            out.setdefault(name, DR + href)
    return out


def ensure_text(root, store, writer, raw_id, extractor, dry):
    """Step 1: the raw's working text by `extractor`; a new revision when it had another one (D29)."""
    raw = store.current(raw_id)
    if raw["text"] and raw["text"]["extractor"] == extractor:
        return raw
    data = store.raw_path(raw).read_bytes()
    derived = extract.EXTRACTORS[extractor](data)
    sha = sha256_text(derived)
    if not dry:
        (root / "raw_bytes" / sha).write_text(derived, encoding="utf-8")
        return writer.revise(raw, {"text": {"extractor": extractor, "sha256": sha, "bytes": f"raw_bytes/{sha}"}}, now_utc())
    return dict(raw, text={"extractor": extractor, "sha256": sha, "bytes": f"raw_bytes/{sha}"})


def note_lines(text):
    """[(offset of the line, parsed note, quote start, quote end)] for every "NOTA: " line of a working text."""
    out, pos = [], 0
    for line in text.split("\n"):
        if line.startswith("NOTA: "):
            parsed = vigente.parse_note(line[len("NOTA: "):])
            if parsed is None:
                raise ValueError(f"unparsed note at offset {pos}: {line[:120]!r}")
            out.append((pos, parsed, pos + len("NOTA: "), pos + len(line)))
        pos += len(line) + 1
    return out


TITLE = re.compile(r"^(?:Decreto-Lei|Lei Orgânica|Lei|Portaria|Declaração de Re(?:c)?tificação|Decreto Legislativo Regional|Decreto Regulamentar"
                   r"|Resolução da Assembleia da República) n\.º [0-9A-Za-z/-]+, de [0-9]{1,2} de [a-zç]+$")
STATUS = ("Em vigor", "Revogado", "Revogada", "Caducado", "Cessação de vigência")
VERBS = {"altera": "altera", "adita": "adita", "revoga": "revoga", "retifica": "retifica", "republica": "republica"}


def jurisdiction(short):
    if short.startswith("eu-"):
        return "UE"
    if re.match(r"^dlr-.*-a$", short):
        return "PT-AC"
    if re.match(r"^dlr-.*-m$", short):
        return "PT-MA"
    return "PT"


def own_pages(store):
    """The captures of an act's own page (current revision): a DR detail page (diploma), a DR consolidated page (lei),
    an EU act (regulamento). Not the per-article history views."""
    ids = sorted({r["id"] for r in store.objects["raw"] if (r["source"], r["kind"]) in
                  (("dr-consolidado", "diploma"), ("dr-consolidado", "lei"), ("eur-lex", "regulamento"))})
    return [store.current(i) for i in ids]


def structured_page(store, raws, raw):
    """The page an act's passages come from: its consolidated page when both were read (it holds the text in force)."""
    return not (raw["kind"] == "diploma" and any(r["kind"] == "lei" and r["source_id"] == raw["source_id"] for r in raws))


def header(store, raw):
    """{title, scope, status, published, eli} as the page prints them; scope is the page's own summary line."""
    text = store.raw_text(raw)
    html = store.raw_path(raw).read_text(encoding="utf-8")
    lines = text.split("\n")
    out = {"status": None, "eli": None}
    if raw["kind"] == "diploma":
        i = next((k for k, l in enumerate(lines) if TITLE.match(l)), None)
        if i is None:
            raise ValueError(f"{raw['id']}: no act title line")
        out["title"] = lines[i]
        out["status"] = lines[i + 1] if i + 1 < len(lines) and lines[i + 1] in STATUS else None
        out["scope"] = lines[lines.index("SUMÁRIO") + 1] if "SUMÁRIO" in lines else lines[i]
        m = re.search(r"Data de Publicação:([0-9]{4}-[0-9]{2}-[0-9]{2})", text)
        out["published"] = m.group(1) if m else None
    elif raw["kind"] == "lei":
        m = re.search(r"<title>([^<]+)</title>", html)
        out["title"] = out["scope"] = unescape(m.group(1)).split(" | ")[0].strip() if m else raw["source_id"]
        m = re.search(r"Série I(?:-A|-B)? de ([0-9]{4}-[0-9]{2}-[0-9]{2})", unescape(re.sub("<[^>]+>", " ", html)))
        out["published"] = m.group(1) if m else None
    else:
        out["title"] = next(l for l in lines if l.startswith(("REGULAMENTO", "DIRETIVA", "DECISÃO")) and "(UE)" in l)
        out["scope"] = next((l for l in lines if l.startswith("que altera") or l.startswith("relativ")), out["title"])
        elis = re.findall(r"ELI: (http://data\.europa\.eu/eli/\S+?/oj)", text)
        out["eli"] = elis[-1].replace("http://", "https://", 1) if elis else None  # the schema's https form of the same ELI
        out["published"] = None
    return out


def masked(text):
    """(text, lines masked): a note the grammar cannot read, or whose act has no DR number, is written "nota: " (same
    length, so every offset stays) and so is not a note to notes_to_vigencias. Only for other acts' pages: the CCP's
    735 notes all read (D33)."""
    out, bad = [], []
    for line in text.split("\n"):
        if line.startswith("NOTA: "):
            n = vigente.parse_note(line[len("NOTA: "):])
            ok = n is not None
            if ok:
                try:
                    vigente.norma_slug(n["diploma"])
                except ValueError:
                    ok = False
            if not ok:
                bad.append(line)
                line = "nota: " + line[len("NOTA: "):]
        out.append(line)
    return "\n".join(out), bad


def register_from_notes(normas, raw, text, recorded_at, of_title):
    """Every act a note of this consolidated page names, registered from the note (title, its own DR link)."""
    links = act_links(store_html(raw))
    effects = {}
    for _, n, _, _ in note_lines(masked(text)[0] if raw["id"] != CONSOLIDATED else text):
        effects.setdefault(n["diploma"], set()).add(n["effect"])
    for diploma in sorted(effects):
        slug = vigente.norma_slug(diploma)
        nid = f"norma:{slug}"
        if diploma not in links and raw["id"] == CONSOLIDATED:
            raise ValueError(f"{diploma}: no DR link in the notes of {raw['id']}")
        # a note with no link of its own: the address is the page the note was read on
        n = normas.setdefault(nid, {"id": nid, "revision": 1, "recorded_at": recorded_at, "title": diploma, "short": slug,
                                    "jurisdiction": jurisdiction(slug), "scope": "", "source": {"url": links.get(diploma, raw["url"]), "raw": []}})
        if raw["id"] not in n["source"]["raw"]:
            n["source"]["raw"].append(raw["id"])
        if not n.get("_own"):
            done = n["scope"].split("; ") if n["scope"] else []
            done.append("ato que " + " / ".join(VERBS[e] for e in sorted(effects[diploma])) + f" passagens de {of_title} (notas do DR)")
            n["scope"] = "; ".join(sorted(set(done)))


_HTML = {}
SKIPPED_PARTS = {}  # norma id -> articles left out because a note after them cannot be read (D33)


def store_html(raw):
    return _HTML[raw["id"]]


def build_normas(store, recorded_at):
    """Step 2: one norma per captured page (title and scope read from it) and per act a note names."""
    normas, texts = {}, {}
    for raw in own_pages(store):
        _HTML[raw["id"]] = store.raw_path(raw).read_text(encoding="utf-8")
        texts[raw["id"]] = store.raw_text(raw)
        short = raw["source_id"]
        h = header(store, raw)
        nid = f"norma:{short}"
        n = {"id": nid, "revision": 1, "recorded_at": recorded_at, "title": h["title"], "short": short, "jurisdiction": jurisdiction(short),
             "scope": h["scope"] + (f" ({h['status']} na data da captura)" if h["status"] and h["status"] != "Em vigor" else ""),
             "source": {"url": raw["url"], "raw": [raw["id"]]}, "_own": True, "_header": h}
        if h["eli"]:
            n["eli"] = h["eli"]
        if nid == "norma:ccp":
            n["source"]["raw"] += sorted(r["id"] for r in store.objects["raw"] if r["kind"] == "artigo-historico" and r["revision"] == 1)
        prev = normas.get(nid)
        if prev and prev.get("_own"):  # the same act read twice: its detail page and its consolidated page
            prev["source"]["raw"].append(raw["id"])
            if raw["kind"] == "lei":
                prev["source"]["url"] = raw["url"]
            continue
        normas[nid] = n
    for raw in own_pages(store):
        if raw["kind"] == "lei":
            register_from_notes(normas, raw, texts[raw["id"]], recorded_at, normas[f"norma:{raw['source_id']}"]["title"])
    register_timeline(store, normas, recorded_at)
    return normas


def register_timeline(store, normas, recorded_at):
    """Every act of the CCP's timeline as the DR prints it on a history page (Navigation.TimelineItem): title and
    address from the item's own link; an act already registered only gains that page among its sources."""
    pages = sorted(r["id"] for r in store.objects["raw"] if r["kind"] == "artigo-historico")
    if not pages:
        return
    raw = store.current(pages[0])
    html = store.raw_path(raw).read_text(encoding="utf-8")
    for item in html.split('data-block="Navigation.TimelineItem"')[1:]:
        link = re.search(r'<a [^>]*href="(/dr/detalhe/[^"]+)"[^>]*>(.*?)</a>', item, re.S)
        if not link:
            continue
        title = " ".join(unescape(re.sub("<[^>]+>", "", link.group(2))).split()).split(" - ")[0].strip()
        slug = vigente.norma_slug(title)
        nid = f"norma:{slug}"
        if nid in normas:
            continue
        normas[nid] = {"id": nid, "revision": 1, "recorded_at": recorded_at, "title": title, "short": slug, "jurisdiction": jurisdiction(slug),
                       "scope": "ato da linha temporal do Código dos Contratos Públicos no DR", "source": {"url": DR + link.group(1), "raw": [raw["id"]]}}


def public(normas):
    return {k: {f: v for f, v in n.items() if not f.startswith("_")} for k, n in normas.items()}


def entry_article(passages):
    """An act's own "Entrada em vigor" article, or None."""
    return next((p for p in passages if p["kind"] == "artigo" and ".q" not in p["id"] and "\nEntrada em vigor\n" in p["versions"][0]["text"] + "\n"), None)


def general_rule(store, normas):
    """The version of Lei n.º 74/98, art. 2.º, n.º 2 (vigente.GENERAL_RULE) when that page was captured, else None."""
    raw = store.current("raw:dr-consolidado:lei:lei-74-1998")
    if raw is None or "norma:lei-74-1998" not in normas:
        return None
    for p in structure.structure(normas["norma:lei-74-1998"], store.raw_text(raw), raw["id"], "0001-01-01"):
        if p["id"] == vigente.GENERAL_RULE:
            return p["versions"][0]
    return None


def act_start(ps, published, rule, norma_id=None):
    """(date, the passage version that says it) for an act's own articles: its "Entrada em vigor" article; when it has
    none, the general rule of Lei n.º 74/98, art. 2.º, n.º 2 (D31). Read, never guessed: (None, None) when neither."""
    if not published:
        return None, None
    art = entry_article(ps)
    if norma_id == "norma:dl-18-2008" and art:
        # «seis meses após a data da sua publicação»: the day the DR's consolidated page gives as the "Versão inicial"
        # of the decree and the code it approves (INITIAL, D24), quoted from art. 18.º
        return INITIAL, art["versions"][0]
    src = art["versions"][0] if art else rule
    return (vigente.entry_into_force(published, src["text"]), src) if src else (None, None)


def in_force_vigencias(ps, norma, start, src, recorded_at):
    """D32: the vigencia of each passage of an act whose version starts on the act's entry into force; the note
    quotes the article (or general rule) that fixes that day."""
    out = []
    for p in ps:
        if p["versions"][0]["valid_from"] != start:
            continue
        out.append({"id": f"{p['id']}@{start}", "revision": 1, "recorded_at": recorded_at, "passage": p["id"], "valid_from": start,
                    "valid_to": None, "altered_by": norma["id"], "effect": "entra_em_vigor",
                    "note": {"raw": src["raw"], "quote": src["text"], "offsets": dict(src["offsets"])}})
    return out


def dated(ps, start):
    for p in ps:
        for v in p["versions"]:
            v["version"] = v["valid_from"] = start
    return ps


def drop_owners_of_masked(ps, text):
    """(passages without the articles a masked note follows, the ids left out)."""
    import bisect
    lines = text.split("\n")
    starts, pos = [], 0
    for line in lines:
        starts.append(pos)
        pos += len(line) + 1
    owners = sorted((p["versions"][0]["offsets"]["start"], p["id"]) for p in ps if p["kind"] in ("artigo", "anexo") and ".q" not in p["id"])
    keys = [o for o, _ in owners]
    drop = set()
    for i, line in enumerate(lines):
        if line.startswith("nota: "):
            k = bisect.bisect_left(keys, starts[i]) - 1
            if k >= 0:
                drop.add(owners[k][1])
    return [p for p in ps if not any(p["id"] == d or p["id"].startswith(d + ".") for d in drop)], drop


def consolidated_act(store, raw, norma, normas, rule):
    """Another act's consolidated page (no history captured): one version per passage, the text in force at capture,
    from the date of its article's newest note (else the act's entry into force); the vigencia of that date only."""
    text, bad = masked(store.raw_text(raw))
    ps = structure.structure(norma, text, raw["id"], "0001-01-01")
    if bad:  # an article followed by a note that cannot be read is left out: its date would be a guess (D33)
        ps, drop = drop_owners_of_masked(ps, text)
        SKIPPED_PARTS[norma["id"]] = sorted(drop)
    for _ in range(50):
        try:
            vg = vigente.notes_to_vigencias(text, raw["id"], ps, normas)
            break
        except ValueError as exc:  # a dateless note nothing dates: masked like an unreadable one, its article left out
            m = re.match(r"note of (.+?) without a date", str(exc))
            if not m:
                raise
            lines = text.split("\n")
            for i, line in enumerate(lines):
                if line.startswith("NOTA: "):
                    n = vigente.parse_note(line[len("NOTA: "):])
                    if n and n["diploma"] == m.group(1) and not n["valid_from"]:
                        lines[i] = "nota: " + line[len("NOTA: "):]
            text = "\n".join(lines)
            ps, dropped = drop_owners_of_masked(ps, text)
            SKIPPED_PARTS.setdefault(norma["id"], [])
            SKIPPED_PARTS[norma["id"]] = sorted(set(SKIPPED_PARTS[norma["id"]]) | dropped)
    latest = {}
    for v in vg:
        if v["valid_to"] is None:
            latest[v["passage"]] = v
    start, src = act_start(ps, norma["_header"]["published"], rule)
    by_id = {p["id"]: p for p in ps}
    owner_of = {}
    for p in ps:
        q = p
        while q and q["kind"] not in ("artigo", "anexo"):
            q = by_id.get(q["parent"]) if q.get("parent") else None
        owner_of[p["id"]] = q["id"] if q else None
    for p in ps:
        own = latest.get(owner_of[p["id"]])
        d = own["valid_from"] if own else start
        if d is None:
            raise ValueError(f"{norma['id']}: {p['id']} has no note and the act's entry into force is not readable")
        for v in p["versions"]:
            v["version"] = v["valid_from"] = d
            if own and own["effect"] == "revoga" and p["id"] == owner_of[p["id"]]:
                v["revoked"] = True
    return ps, list(latest.values()) + (in_force_vigencias(ps, norma, start, src, now_utc()) if start else [])


def build_passages(store, normas):
    """Step 3: ({id: passagem}, {id: vigencia}, {norma id: why it is not structured})."""
    out, vigs, skipped = {}, {}, {}
    rule = general_rule(store, normas)
    ccp = store.current(CONSOLIDATED)
    text = store.raw_text(ccp)
    for p in structure.structure(normas["norma:ccp"], text, ccp["id"], INITIAL):
        out[p["id"]] = p
    pages = own_pages(store)
    for raw in pages:
        norma = normas[f"norma:{raw['source_id']}"]
        if raw["id"] == CONSOLIDATED or not structured_page(store, pages, raw):
            continue
        try:
            if raw["kind"] == "regulamento":
                raise ValueError("EU layout (\"Artigo 1.o\", points \"1)\" on their own line) has no grammar in engine/structure yet")
            if raw["kind"] == "lei":
                ps, vg = consolidated_act(store, raw, norma, public(normas), rule)
            else:
                ps = structure.structure(norma, store.raw_text(raw), raw["id"], INITIAL)
                if not ps:
                    raise ValueError("no articles of its own (a declaração de retificação lists corrections)")
                start, src = act_start(ps, norma["_header"]["published"], rule, norma["id"])  # read, never guessed
                if not start:
                    raise ValueError("no readable entry-into-force article nor general rule; its passages would have no date")
                ps = dated(ps, start)
                vg = in_force_vigencias(ps, norma, start, src, now_utc())
        except ValueError as exc:
            skipped[norma["id"]] = str(exc)
            continue
        for p in ps:
            out[p["id"]] = p
        for v in vg:
            vigs[v["id"]] = v
    return out, vigs, skipped


def history_blocks(text, label):
    """The versions of one history page, newest first: dicts {first line, last line + 1, note, quote}. A version starts
    at a line equal to the owner's label ("Artigo 20.º", "Anexo XII") and ends at the note that produced it. The DR
    sometimes shows a version twice with no note between the copies (Anexo XII): a noteless version that is not the
    oldest is dropped when its text is the next version's; any other noteless version fails (D30)."""
    lines = text.split("\n")
    blocks, cur, pos = [], None, 0
    for i, line in enumerate(lines):
        if line.strip().replace(".º", "") == label.replace(".º", ""):  # the DR prints "Artigo 410" on one version
            if cur is not None and not cur["closed"]:
                cur["last"] = i
            cur = {"first": i, "last": len(lines), "note": None, "quote": None, "closed": False}
            blocks.append(cur)
        elif line.startswith("NOTA: ") and cur is not None and not cur["closed"]:
            cur["last"], cur["closed"] = i, True
            cur["note"] = vigente.parse_note(line[len("NOTA: "):])
            if cur["note"] is None:
                raise ValueError(f"unparsed note: {line[:120]!r}")
            cur["quote"] = (pos + len("NOTA: "), pos + len(line), line[len("NOTA: "):])
        pos += len(line) + 1
    body = lambda b: lines[b["first"]:b["last"]]  # noqa: E731
    kept = []
    for k, b in enumerate(blocks):
        if b["note"] is None and k < len(blocks) - 1:
            if body(b) == body(blocks[k + 1]):
                continue
            raise ValueError(f"a version without a note that is not the oldest, at line {b['first'] + 1}")
        kept.append(b)
    return lines, kept


def versions_from_page(owner, raw, text, prefix, short, dates, owner_vigencias):
    """Step 5 for one owner: {passage id: passagem} for the owner and every part inside it, versions from one page."""
    lines, blocks = history_blocks(text, owner["label"])
    starts, pos = [], 0
    for line in lines:
        starts.append(pos)
        pos += len(line) + 1
    kept, seen = [], set()
    for b in blocks:  # newest first: the first block of a date is the text in force from that date (D24)
        vf = (b["note"]["valid_from"] or dates[(b["note"]["diploma"], b["note"]["published"])]) if b["note"] else INITIAL
        if vf in seen:
            continue
        seen.add(vf)
        kept.append((vf, b))
    kept.sort(key=lambda x: x[0])  # by date: a retificação may date its text back (Anexo II: 36-A/2017 from 2008-07-30)
    parts = {}  # id -> passagem
    order = []
    for k, (vf, b) in enumerate(kept):
        nodes = structure.parse(lines, b["first"], b["last"], prefix, annexes=owner["kind"] == "anexo")
        present = {}
        for n in nodes:
            s, e = starts[n["start_line"]], starts[n["last_line"]] + len(lines[n["last_line"]])
            present[f"{short}:{n['path']}"] = (n, s, e)
        if owner["id"] not in present:
            raise ValueError(f"{raw['id']}: the version from {vf} does not hold {owner['id']}")
        for pid, (n, s, e) in present.items():
            t = text[s:e]
            p = parts.get(pid)
            if p is None:
                p = parts[pid] = {"id": pid, "revision": 1, "recorded_at": None, "norma": owner["norma"],
                                  "parent": owner["parent"] if pid == owner["id"] else (f"{short}:{n['parent']}" if n["parent"] else None),
                                  "kind": n["kind"], "label": n["label"], "versions": []}
                order.append(pid)
            last = p["versions"][-1] if p["versions"] else None
            if pid != owner["id"] and last and last["text"] == t and not last.get("_ceased"):
                continue  # the part's text did not change: one version goes on
            revoked = structure._revoked(n["kind"], t) or (pid == owner["id"] and b["note"] is not None and b["note"]["effect"] == "revoga")
            p["versions"].append({"version": vf, "text": t, "raw": raw["id"], "offsets": {"start": s, "end": e},
                                  "valid_from": vf, "valid_to": None, "revoked": revoked})
        for pid in order:  # a part this version no longer has: closed by the version's own note (D30)
            if pid in present or not parts[pid]["versions"] or parts[pid]["versions"][-1].get("_ceased"):
                continue
            src = owner_vigencias.get(vf)  # the note the article's vigencia of that date quotes; else the page's own
            note = src["note"] if src else {"raw": raw["id"], "quote": b["quote"][2], "offsets": {"start": b["quote"][0], "end": b["quote"][1]}}
            parts[pid]["versions"].append({"version": vf, "text": note["quote"], "raw": note["raw"], "offsets": dict(note["offsets"]),
                                           "valid_from": vf, "valid_to": None, "revoked": True, "_ceased": True})
    for p in parts.values():
        for a, b in zip(p["versions"], p["versions"][1:]):
            a["valid_to"] = b["valid_from"]
        for v in p["versions"]:
            v.pop("_ceased", None)
    return parts


def apply_histories(store, passages, vigencias, ccp_text, ccp_raw_id):
    """Step 5 over every history capture. Returns (passages, vigencias, report)."""
    notes = [n for _, n, _, _ in note_lines(ccp_text)]
    dates = vigente.resolve_note_dates(notes, list(passages.values()))
    pages = {r["source_id"]: store.current(r["id"]) for r in store.objects["raw"] if r["kind"] == "artigo-historico"}
    by_owner = {}
    for v in vigencias.values():
        by_owner.setdefault(v["passage"], {})[v["valid_from"]] = v
    report = {"owners_with_history": 0, "owners_with_notes_without_history": [], "dates_only_in_notes": [], "dates_only_in_history": []}
    for pid in sorted(passages):
        if pid not in passages:  # a part an earlier owner's history replaced
            continue
        owner = passages[pid]
        if owner["norma"] != "norma:ccp" or owner["kind"] not in ("artigo", "anexo") or ".q" in pid:
            continue
        local = pid.split(":", 1)[1]
        key = "ccp-" + local.replace("dl.art", "dl-art")
        raw = pages.get(key)
        if raw is None:
            owner_dates = set(by_owner.get(pid, {}))
            if len(owner_dates) == 1 and by_owner[pid][next(iter(owner_dates))]["effect"] == "adita":
                # added once and never changed: the consolidated text is its only version, from the date it was added
                d = next(iter(owner_dates))
                src = by_owner[pid][d]
                for q in [q for q in passages if q == pid or q.startswith(pid + ".")]:
                    for v in passages[q]["versions"]:
                        v["version"] = v["valid_from"] = d
                    if q != pid:
                        vigencias[f"{q}@{d}"] = {"id": f"{q}@{d}", "revision": 1, "recorded_at": src["recorded_at"], "passage": q,
                                                 "valid_from": d, "valid_to": None, "altered_by": src["altered_by"], "note": src["note"],
                                                 "effect": src["effect"]}
                report["added_once_no_history"] = report.get("added_once_no_history", 0) + 1
            elif owner_dates and owner_dates != {INITIAL}:
                report["owners_with_notes_without_history"].append(pid)
            continue
        report["owners_with_history"] += 1
        text = store.raw_text(raw)
        prefix = "dl." if local.startswith("dl.") else ""
        parts = versions_from_page(owner, raw, text, prefix, "ccp", dates, by_owner.get(pid, {}))
        hist_dates = {v["valid_from"] for v in parts[pid]["versions"]}
        note_dates = set(by_owner.get(pid, {}))
        report["dates_only_in_notes"] += [f"{pid}@{d}" for d in sorted(note_dates - hist_dates)]
        report["dates_only_in_history"] += [f"{pid}@{d}" for d in sorted(hist_dates - note_dates - {INITIAL})]
        for old in [q for q in passages if q == pid or q.startswith(pid + ".")]:
            if old not in parts:
                report.setdefault("parts_only_in_consolidated", []).append(old)
            del passages[old]
        passages.update(parts)
        for cid, p in parts.items():  # the owner's notes, mirrored on every part that changes on that date
            if cid == pid:
                continue
            starts = [v["valid_from"] for v in p["versions"] if v["valid_from"] in by_owner.get(pid, {})]
            for k, d in enumerate(starts):
                src = by_owner[pid][d]
                vigencias[f"{cid}@{d}"] = {"id": f"{cid}@{d}", "revision": 1, "recorded_at": src["recorded_at"], "passage": cid,
                                           "valid_from": d, "valid_to": starts[k + 1] if k + 1 < len(starts) else None,
                                           "altered_by": src["altered_by"], "note": src["note"], "effect": src["effect"]}
    return passages, vigencias, report


def same(a, b):
    strip = lambda o: {k: v for k, v in o.items() if k not in ENVELOPE}  # noqa: E731
    return json.dumps(strip(a), sort_keys=True, ensure_ascii=False) == json.dumps(strip(b), sort_keys=True, ensure_ascii=False)


def write_all(store, writer, objects, recorded_at, dry):
    counts = Counter()
    for obj in objects:
        cur = store.current(obj["id"])
        obj = dict(obj, recorded_at=recorded_at)
        if cur is None:
            counts["added"] += 1
            if not dry:
                writer.append(obj)
        elif cur.get("stale") or not same(cur, obj):
            counts["revised"] += 1
            if not dry:
                writer.revise(cur, {k: v for k, v in obj.items() if k not in ENVELOPE}, recorded_at)
        else:
            counts["unchanged"] += 1
    return counts


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--store", default="law", help="a store directory (relative to the repo, or absolute: a copy for a trial run)")
    ap.add_argument("--no-history", action="store_true")
    a = ap.parse_args()
    root = ROOT / a.store
    store = Store([root]).load()
    writer = Writer(root, store)
    recorded_at = now_utc()
    ensure_text(root, store, writer, CONSOLIDATED, TEXT_EXTRACTOR, False)
    store = Store([root]).load()
    writer = Writer(root, store)
    ccp_raw = store.current(CONSOLIDATED)
    ccp_text = store.raw_text(ccp_raw)
    normas = build_normas(store, recorded_at)
    passages, other_vigs, skipped = build_passages(store, normas)
    vigencias = {v["id"]: v for v in vigente.notes_to_vigencias(ccp_text, ccp_raw["id"], list(passages.values()), public(normas))}
    vigencias.update(other_vigs)
    report = {}
    if not a.no_history:
        passages, vigencias, report = apply_histories(store, passages, vigencias, ccp_text, ccp_raw["id"])
    counts = {}
    for name, objs in (("norma", public(normas).values()), ("passagem", passages.values()), ("vigencia", vigencias.values())):
        counts[name] = dict(write_all(store, writer, sorted(objs, key=lambda o: o["id"]), recorded_at, False))
    (root / "build-report.json").write_text(json.dumps({"tool": VERSION, "not_structured": skipped, "articles_left_out": SKIPPED_PARTS},
                                                      ensure_ascii=False, indent=1, sort_keys=True) + "\n", encoding="utf-8")
    kinds = Counter(p["kind"] for p in passages.values() if p["norma"] == "norma:ccp")
    print(json.dumps({"tool": VERSION, "store": str(root), "normas": len(normas), "passages": len(passages),
                      "ccp_passages_by_kind": dict(kinds.most_common()), "ccp_artigos": kinds["artigo"],
                      "vigencias": len(vigencias), "versions": sum(len(p["versions"]) for p in passages.values()),
                      "not_structured": skipped, "articles_left_out": {k: {"count": len(v), "ids": v[:6]} for k, v in SKIPPED_PARTS.items()},
                      "writes": counts,
                      "history": {k: (v if isinstance(v, int) else {"count": len(v), "first": v[:8]}) for k, v in report.items()}},
                     ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
