"""The law watch (DECISIONS D92): read the consolidated CCP on the Diário da República, compare every article with the text
the repository holds in force (tools/refresh.ccp_changed, the same comparison the Mac's refresh makes), and keep
ccp.lei_alteracao current. A new difference pushes an alert to the person's phone (ntfy) so the readers can run on the Mac;
a failed read pushes one too: a page that cannot be read is never "no change".

    .venv/bin/python -I db/law_watch.py check [--no-alert]     one check now (the page rendered by Chrome, CCP_CHROME in the cloud)
    .venv/bin/python -I db/law_watch.py pending                 the articles waiting for the readers
    .venv/bin/python -I db/law_watch.py alert --title T --text M  one push (the Mac's runner uses it)

The topic is the secret NTFY_TOPIC (the Modal secret ccp-ntfy; on the Mac, NTFY_TOPIC in .env). Nothing is pushed without it.
"""
import argparse
import hashlib
import os
import sys
import traceback
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path[:0] = [str(ROOT / "db"), str(ROOT), str(ROOT / "tools")]  # db first: tools/ has a run_engine.py of its own
import pg  # noqa: E402

VERSION = "ccp-law-watch-0.1"
NTFY = "https://ntfy.sh/"


def topic():
    t = os.environ.get("NTFY_TOPIC")
    if not t:
        env = ROOT / ".env"
        if env.exists():
            t = next((l.split("=", 1)[1].strip() for l in env.read_text(encoding="utf-8").splitlines() if l.startswith("NTFY_TOPIC=")), None)
    return t


def alert(title, text, priority="default", tags=()):
    """One push to the person's ntfy topic; False when there is no topic or the push failed (the caller goes on)."""
    t = topic()
    if not t:
        print(f"[no NTFY_TOPIC] {title}: {text}", file=sys.stderr)
        return False
    req = urllib.request.Request(NTFY + t, data=text.encode("utf-8"), method="POST",
                                 headers={"Title": title.encode("utf-8").decode("latin-1", "ignore"), "Priority": priority, "Tags": ",".join(tags)})
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            return r.status == 200
    except OSError as e:
        print(f"ntfy failed: {e}", file=sys.stderr)
        return False


def pending(conn):
    return {p: d for p, d in conn.execute("select passagem, desde from ccp.lei_pendente").fetchall()}


def record(conn, differing, sha):
    """Open a row for each newly differing article, close the rows of articles that no longer differ. Returns the new ones."""
    open_ = set(pending(conn))
    new = sorted(set(differing) - open_)
    for p in new:
        conn.execute("insert into ccp.lei_alteracao (passagem, pagina_sha256) values (%s, %s)", (p, sha))
    gone = sorted(open_ - set(differing))
    if gone:
        conn.execute("update ccp.lei_alteracao set fechada_em = now() where fechada_em is null and passagem = any(%s)", (gone,))
    return new, gone


def check(conn, push=True):
    from engine.store import Store
    import capture_dr_consolidated as cap
    import refresh
    try:
        raw = cap.render(refresh.CCP_URL, 30000)
        store = Store([ROOT / "law"]).load()
        differing = refresh.ccp_changed(store, raw)
    except BaseException as e:  # SystemExit included: the page changed shape, the render failed
        err = f"{type(e).__name__}: {e}"[:500]
        traceback.print_exc()
        conn.execute("insert into ccp.lei_vigia (ok, erro) values (false, %s)", (err,))
        conn.commit()
        if push:
            alert("CCP: no pude leer el Diário", f"La vigilancia de la ley falló hoy: {err[:200]}. Nada se da por «sin cambios».", "high", ("warning",))
        return {"ok": False, "erro": err}
    sha = hashlib.sha256(raw).hexdigest()
    new, gone = record(conn, differing, sha)
    articles = raw.decode("utf-8", "ignore").count("Artigo ")
    conn.execute("insert into ccp.lei_vigia (ok, artigos, diferentes, novas) values (true, %s, %s, %s)", (articles, differing, new))
    conn.commit()
    if push and new:
        shown = ", ".join(p.replace("ccp:art", "art. ") for p in new[:12]) + (" …" if len(new) > 12 else "")
        alert(f"CCP: {len(new)} artículo(s) cambiaron en el Diário", f"{shown}. Abre el Mac: AMALIA y Reader B los leen al iniciar sesión. "
              "Hasta entonces, las reglas de esos artículos no dan veredicto.", "high", ("scroll",))
    return {"ok": True, "diferentes": differing, "novas": new, "fechadas": gone, "pagina_sha256": sha}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["check", "pending", "alert"])
    ap.add_argument("--no-alert", action="store_true"); ap.add_argument("--title"); ap.add_argument("--text")
    a = ap.parse_args()
    if a.cmd == "alert":
        sys.exit(0 if alert(a.title or "CCP", a.text or "") else 1)
    conn = pg.connect()
    if a.cmd == "pending":
        for p, d in sorted(pending(conn).items()):
            print(p, d.isoformat())
        return
    print(check(conn, push=not a.no_alert))


if __name__ == "__main__":
    main()
