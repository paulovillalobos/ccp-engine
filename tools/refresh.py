"""The daily refresh (DECISIONS D75): keep the law current and its rules read, with no step a person has to remember.

    .venv/bin/python tools/refresh.py            what changed, read passively; writes nothing
    .venv/bin/python tools/refresh.py --apply    capture, rebuild, read the changed passages blind, record, verify, package

1. EU: the Publications Office's SPARQL endpoint lists the consolidated versions of the directives in the store (D70); a
   version the store does not hold is captured (tools/capture_page.py --list, Portuguese XHTML, one GET each).
2. CCP: the consolidated page of the Diário da República is rendered once (tools/capture_dr_consolidated.render) and its
   articles compared with the text in force in the store. When one differs, the history views are walked again
   (tools/capture_dr_history.mjs) and recorded (tools/record_histories.py): build_law takes each version from them (D24).
3. tools/build_law.py and tools/coverage.py.
4. Every passage whose current revision was recorded after the last refresh and that states days or euros, and that no round
   asked the same question of, becomes a target of a refresh round (governance/readings/refresh-<date>/pick.json, drawn by
   rule_factory.draw_since); both families read it blind (AMALIA with the latest adapter on Modal, Reader B through the Reader B
   app's client in disjoint shards), the factory records it, verify must pass.
5. A commit, a push, tools/package.sh. The service is deployed only when deploy/AUTODEPLOY exists (the person's «publícalo»).
State: law/REFRESH.json (when the last refresh ran and what it saw). Every step stops the run on failure and says why; nothing
is retried. No model is called here except through the two readers of step 4.
"""
import argparse
import json
import re
import subprocess
import sys
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT)); sys.path.insert(0, str(ROOT / "tools"))
from engine import extract  # noqa: E402
from engine.sources import now_utc  # noqa: E402
from engine.store import Store  # noqa: E402

VERSION = "ccp-refresh-0.3"
STATE = ROOT / "law/REFRESH.json"
PY = str(ROOT / ".venv/bin/python")
MODAL = str(Path.home() / "Downloads/foaap-core/.venv-modal/bin/modal")
READER_B_PATH = "/usr/local/bin"
SPARQL = "https://publications.europa.eu/webapi/rdf/sparql"
CCP_URL = "https://diariodarepublica.pt/dr/legislacao-consolidada/decreto-lei/2008-34455475"
LATEST_LORA = "v17"  # D92: the adapter that settled the counting rules (D85)


def run(cmd, **kw):
    print("$", " ".join(cmd), flush=True)
    res = subprocess.run(cmd, cwd=ROOT, **kw)
    if res.returncode != 0:
        raise SystemExit(f"refresh stopped: {cmd[1] if len(cmd) > 1 else cmd[0]} exited {res.returncode}")
    return res


def eu_new(store, unavailable=()):
    """[(url, source id)] of consolidated versions the Publications Office lists and the store does not hold, less those it
    did not serve in Portuguese before (law/REFRESH.json eu_unavailable)."""
    shorts = sorted({r["source_id"].rsplit("-", 1)[0] for r in store.objects["raw"] if (r["source"], r["kind"]) == ("eur-lex", "diretiva")})
    have = {r["source_id"] for r in store.objects["raw"] if (r["source"], r["kind"]) == ("eur-lex", "diretiva")}
    out = []
    for short in shorts:
        _, y, n = short.split("-")
        prefix = f"0{y}L{int(n):04d}"
        q = ("PREFIX cdm: <http://publications.europa.eu/ontology/cdm#> SELECT ?celex WHERE { ?w cdm:resource_legal_id_celex ?celex . "
             f'FILTER(STRSTARTS(STR(?celex), "{prefix}")) }}')
        req = urllib.request.Request(SPARQL, data=urllib.parse.urlencode({"query": q}).encode(), headers={"Accept": "application/sparql-results+json"})
        with urllib.request.urlopen(req, timeout=60) as resp:
            celexes = [b["celex"]["value"] for b in json.load(resp)["results"]["bindings"]]
        for c in celexes:
            sid = f"{short}-{c.rsplit('-', 1)[1]}"
            if sid not in have and sid not in unavailable:
                out.append((f"https://publications.europa.eu/resource/celex/{c}", sid))
    return out


def ccp_changed(store, raw=None):
    """The code's articles (after its «Anexo» line: the approving decree's own articles come first) whose text on the
    consolidated page differs from the text in force in the store, each cut at the next heading. An article the store holds
    revoked is unchanged while the page shows its heading only. One render of the page."""
    import capture_dr_consolidated as cap  # noqa: E402
    import read_rules_v3 as v3  # noqa: E402
    from engine import structure  # noqa: E402
    raw = raw or cap.render(CCP_URL, 30000)
    text = extract.EXTRACTORS["dr-consolidated-fragments@1"](raw)
    marks = [m.start() for m in re.finditer(r"^(?:Anexo|ANEXO)$", text, re.M)]
    if not marks:
        raise SystemExit("refresh stopped: the consolidated page has no «Anexo» line (the page changed shape)")
    revoked_on_page = set()  # D95: the DR prints a revoked article's last text under a «REVOGADO» note (art. 61)
    noted = extract.EXTRACTORS["dr-article-history@1"](raw)
    anexo = [m.start() for m in re.finditer(r"^(?:Anexo|ANEXO)$", noted, re.M)]
    for m in re.finditer(r"^Artigo (\d+(?:\.º)?(?:-[A-Z])?)\n(.+?)(?=^Artigo \d|\Z)", noted[anexo[0]:] if anexo else "", re.M | re.S):
        first = next((l for l in m.group(2).split("\n") if l.startswith("NOTA: ")), "")
        if first.startswith("NOTA: REVOGADO"):
            revoked_on_page.add("ccp:art" + m.group(1).replace(".º", "").lower())
    law, today, changed = v3.Law(store), now_utc()[:10], []
    for m in re.finditer(r"^Artigo (\d+(?:\.º)?(?:-[A-Z])?)\n(.+?)(?=^Artigo \d|\Z)", text[marks[0]:], re.M | re.S):  # «Artigo 410-A» has no º
        pid = "ccp:art" + m.group(1).replace(".º", "").lower()
        lines = []
        for line in ("Artigo " + m.group(1) + "\n" + m.group(2)).split("\n"):
            if structure.HEADING.match(line.strip()) or structure.CODE_TITLE.match(line.strip()) or structure.ANNEX_LINE.match(line.strip()):
                break
            if line.strip():
                lines.append(line)
        same = lambda x: re.sub(r"^Artigo (\d+)(?:\.º)?", r"Artigo \1", " ".join(x.split()))  # noqa: E731  (the DR prints «Artigo 410» and «Artigo 410.º»)
        page, mine = same(" ".join(lines)), law.text(pid, today)
        if mine is None:
            if len(lines) > 2 and not re.search(r"Revogad", page) and pid not in revoked_on_page:
                changed.append(pid)
        elif page != same(mine):
            changed.append(pid)
    return changed


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--apply", action="store_true")
    a = ap.parse_args()
    state = json.loads(STATE.read_text(encoding="utf-8")) if STATE.exists() else {"last_run": "2026-11-04T00:00:00Z", "eu_unavailable": []}
    unavailable = set(state.get("eu_unavailable", []))
    store = Store([ROOT / "law"]).load()
    report = {"tool": VERSION, "at": now_utc(), "since": state["last_run"]}
    eu = eu_new(store, unavailable)
    report["eu_new_versions"] = [sid for _, sid in eu]
    report["ccp_changed_articles"] = ccp_changed(store)
    print(json.dumps(report, ensure_ascii=False, indent=1))
    if not a.apply:
        return
    if report["eu_new_versions"]:
        lst = ROOT / "law/.refresh-eu.tsv"
        lst.write_text("".join(f"{u}\t{s}\n" for u, s in eu), encoding="utf-8")
        res = run([PY, "-I", "tools/capture_page.py", "--list", str(lst), "--source", "eur-lex", "--kind", "diretiva",
                   "--accept", "application/xhtml+xml", "--accept-language", "por"], capture_output=True, text=True)
        print(res.stdout)
        unavailable |= {line.split(":")[0] for line in res.stdout.splitlines() if ": not recorded" in line}
        lst.unlink()
    if report["ccp_changed_articles"]:
        out = ROOT / "law/.refresh-history"
        run(["node", "tools/capture_dr_history.mjs", "--out", str(out)])
        run([PY, "-I", "tools/record_histories.py", "--from", str(out)])
    changed_law = bool(report["eu_new_versions"] or report["ccp_changed_articles"])
    if changed_law:
        run([PY, "-I", "tools/build_law.py"])
        run([PY, "-I", "tools/coverage.py"])
    import rule_factory as rf  # noqa: E402  (after the build: it reads the store it draws from)
    full = Store([ROOT / "law", ROOT / "rules", ROOT / "governance"]).load()
    pick = rf.draw_since(full, state["last_run"])
    report["targets"] = len(pick)
    if pick:
        d = rf.rr.READINGS / f"refresh-{report['at'][:10].replace('-', '')}"
        d.mkdir(parents=True, exist_ok=True)
        (d / "pick.json").write_text(json.dumps({"tool": rf.VERSION, "decision": "D75", "drawn_at": report["at"], "since": state["last_run"], "pick": pick},
                                                ensure_ascii=False, indent=0) + "\n", encoding="utf-8")
        n = rf.refresh_round_of(d)
        run([PY, "-I", "tools/rule_factory.py", "prompts", "--round", str(n)])
        run([MODAL, "run", "readers/leitor_a_modal.py", "--dir", str(d.relative_to(ROOT)), "--lora", LATEST_LORA, "--quotes", "text"])
        env = {**__import__("os").environ, "PATH": f"{READER_B_PATH}:{__import__('os').environ['PATH']}"}
        run([sys.executable, "-I", "readers/leitor_b_cli.py", "--dir", str(d.relative_to(ROOT)), "--model", "model-b"], env=env)
        run([PY, "-I", "tools/rule_factory.py", "record", "--round", str(n)])
    if changed_law or pick:
        run([PY, "-I", "verify.py"])
        STATE.write_text(json.dumps({"last_run": report["at"], "eu_unavailable": sorted(unavailable), "seen": report}, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        run(["git", "add", "-A", "law", "rules", "governance"])
        run(["git", "commit", "-q", "-m", f"D75: refresh {report['at'][:10]} — {len(report['eu_new_versions'])} EU versions, "
                                         f"{len(report['ccp_changed_articles'])} CCP articles changed, {report['targets']} passages read"])
        run(["git", "push", "-q", "origin", "main"])
        run(["zsh", "tools/package.sh"])
        if (ROOT / "deploy/AUTODEPLOY").exists():
            token = (ROOT / "deploy/.ccp-token").read_text(encoding="utf-8").strip()
            run(["gcloud", "run", "deploy", "ccp-engine", "--project", "gen-lang-client-0698758883", "--source", "dist/ccp-service",
                 "--region", "europe-southwest1", "--allow-unauthenticated", "--set-env-vars", f"CCP_TOKEN={token}", "--memory", "1Gi",
                 "--cpu", "1", "--timeout", "120", "--concurrency", "1", "--max-instances", "4", "--quiet"])
    else:
        STATE.write_text(json.dumps({"last_run": report["at"], "eu_unavailable": sorted(unavailable), "seen": report}, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
