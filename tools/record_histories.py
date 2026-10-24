"""Record the history views captured by tools/capture_dr_history.mjs into the law store, one raw per page.

    .venv/bin/python tools/record_histories.py --from DIR [--from DIR ...] [--store law] [--log BUILD-LOG-lines.txt]

For each entry of DIR/manifest.json: engine.sources.record_raw(source dr-consolidado, kind artigo-historico,
source_id <manifest id, e.g. ccp-art21 or ccp-dl-art14>, the page URL, the HTML bytes, captured_at from the manifest,
extractor dr-article-history@2, which also reads an annex's page). The page must show at least one version titled as
the manifest says, or it is refused and listed; "versions" counts the title lines (the page's versions, before
rectifications are folded). Prints the report (articles with a note on the consolidated page / histories recorded / versions per article)
and, with --log, writes one line per page: captured_at, id, sha256, bytes. Nothing is fetched here.
"""
import argparse
import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from engine import extract  # noqa: E402
from engine.sources import record_raw  # noqa: E402

VERSION = "ccp-record-histories-0.2"
RENDERER = "headless Chrome DevTools (tools/capture_dr_history.mjs): one click per page in a session that loaded the consolidated page once"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--from", dest="src", required=True, action="append"); ap.add_argument("--store", default="law"); ap.add_argument("--log")
    a = ap.parse_args()
    recorded, refused, versions, lines = [], [], Counter(), []
    pages, failures, visited = [], [], 0
    for d in a.src:
        man = json.loads((Path(d) / "manifest.json").read_text(encoding="utf-8"))
        pages += [(Path(d), p) for p in man["pages"]]
        failures += man.get("failures", [])
        visited += len(man.get("visited", []))
    for src, p in pages:
        data = (src / p["file"]).read_bytes()
        try:
            text = extract.dr_article_history_v2(data)
            n = sum(1 for line in text.split("\n") if line == p["title"])  # one title line per version
            if n == 0:
                raise ValueError(f"no version titled {p['title']!r}")
        except ValueError as exc:
            refused.append((p["id"], str(exc)))
            continue
        obj = record_raw(ROOT / a.store, "dr-consolidado", "artigo-historico", p["id"], p["url"], data, "text/html", "utf-8", p["captured_at"],
                         extractor="dr-article-history@2", renderer=RENDERER)
        recorded.append(obj["id"])
        versions[n] += 1
        lines.append(f"{p['captured_at']}  {p['id']:<22} sha256 {obj['sha256']}  {len(data)} bytes")
    print(json.dumps({"pages_in_manifests": len(pages), "recorded": len(recorded), "refused": refused, "walk_failures": failures,
                      "visited": visited, "versions_per_article": dict(sorted(versions.items()))}, ensure_ascii=False, indent=1))
    if a.log:
        Path(a.log).write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
