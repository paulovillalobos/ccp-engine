"""The readers' side of the law watch (DECISIONS D92), on the person's Mac: at login and every hour while logged in
(LaunchAgent com.paulo.ccp-readers, deploy/com.paulo.ccp-readers.plist).

    .venv/bin/python -I db/mac_readers.py [--force]

1. Asks Supabase which articles the cloud's law watch holds pending (ccp.lei_pendente). None, or the same set this Mac
   already handled (law/.readers-state.json): nothing to do, it exits in a second.
2. tools/refresh.py --apply: the changed articles' histories captured, the law rebuilt, the passages read blind by AMALIA
   (Modal, the latest settled adapter) and Reader B (reader B's client: the person's subscription, no API key), recorded,
   verified, committed and pushed. A disagreement settles nothing: the article's rules stay held and get no verdict.
3. The cloud gets the new law and rules (modal deploy db/modal_engine.py) and runs after_load at once: the watch closes
   the articles that now match, and the run is full when the rules in use changed.
4. One push to the person's phone: what was read, how many rules settled, what is still pending.
Every step stops the run on failure and pushes why. The person is never asked to decide a rule (feedback: he is not a
legal authority); a reading that does not replicate stays unsettled.
"""
import argparse
import fcntl
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path[:0] = [str(ROOT / "db"), str(ROOT), str(ROOT / "tools")]
import law_watch  # noqa: E402
import pg  # noqa: E402

VERSION = "ccp-mac-readers-0.1"
STATE = ROOT / "law/.readers-state.json"
LOCK = ROOT / "law/.readers.lock"
PY = str(ROOT / ".venv/bin/python")
MODAL = str(Path.home() / "Downloads/foaap-core/.venv-modal/bin/modal")


def sh(cmd, **kw):
    print("$", " ".join(cmd), flush=True)
    res = subprocess.run(cmd, cwd=ROOT, **kw)
    if res.returncode != 0:
        raise RuntimeError(f"{Path(cmd[1] if cmd[0] in (PY, MODAL) and len(cmd) > 1 else cmd[0]).name} salió con {res.returncode}")
    return res


def settled_rules_between(a, b):
    """Rule files a refresh commit added or changed whose state is settled."""
    names = subprocess.run(["git", "diff", "--name-only", f"{a}..{b}", "--", "rules/regra"], cwd=ROOT, capture_output=True, text=True).stdout.split()
    out = []
    for n in names:
        p = ROOT / n
        if p.exists() and json.loads(p.read_text(encoding="utf-8")).get("state") == "settled":
            out.append(json.loads(p.read_text(encoding="utf-8"))["id"])
    return sorted(set(out))


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--force", action="store_true")
    a = ap.parse_args()
    with open(LOCK, "w") as lock:
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            print("another run holds the lock"); return
        conn = pg.connect()
        pend = sorted(law_watch.pending(conn))
        conn.close()
        state = json.loads(STATE.read_text(encoding="utf-8")) if STATE.exists() else {}
        if not pend or (pend == state.get("handled") and not a.force):
            print(f"nothing to read ({len(pend)} pending, all handled before)"); return
        shown = ", ".join(p.replace("ccp:art", "art. ") for p in pend[:10]) + (" …" if len(pend) > 10 else "")
        law_watch.alert("CCP: leyendo la ley", f"AMALIA y Reader B empiezan con {shown}.", "default", ("hourglass",))
        before = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, capture_output=True, text=True).stdout.strip()
        try:
            sh([PY, "-I", "tools/refresh.py", "--apply"])
            after = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, capture_output=True, text=True).stdout.strip()
            sh([MODAL, "deploy", "db/modal_engine.py"])
            res = sh([MODAL, "run", "db/modal_engine.py", "--cmd", "after-load"], capture_output=True, text=True)
            print(res.stdout[-2000:])
        except Exception as e:  # noqa: BLE001
            law_watch.alert("CCP: la lectura se paró", f"{e}. Nada se publicó con la ley cambiada; los artículos siguen en espera.", "high", ("warning",))
            raise
        settled = settled_rules_between(before, after) if after != before else []
        conn = pg.connect()
        still = sorted(law_watch.pending(conn))
        STATE.write_text(json.dumps({"tool": VERSION, "handled": still, "read": pend, "commit": after, "settled": settled}, ensure_ascii=False, indent=1) + "\n",
                         encoding="utf-8")
        law_watch.alert("CCP: ley leída", f"Leídos {len(pend)} artículos. Reglas fijadas: {len(settled)}. "
                        + (f"Siguen en espera (sin acuerdo o sin regla): {', '.join(p.replace('ccp:art', 'art. ') for p in still)}." if still
                           else "Nada en espera: el sistema está al día."), "default", ("white_check_mark",))


if __name__ == "__main__":
    main()
