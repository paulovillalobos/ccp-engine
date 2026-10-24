#!/bin/zsh
# The deployable slice of the repo: what the service reads (engine, tools, law, rules, governance log and principals)
# and nothing else: no data/ (the extractor's facts), no fixtures, no tests, no secrets (.env, *token*, *.key, *.pem are
# refused). Writes dist/ccp-service/ with a VERSION file, then starts the service from there and checks /v1/saude.
#   tools/package.sh            # -> dist/ccp-service
# Copied from rjue-engine's package script and versioned here (ccp-package-0.1).
set -eo pipefail
cd "$(dirname "$0")/.."
OUT=dist/ccp-service
rm -rf "$OUT" && mkdir -p "$OUT/governance"
cp -R engine tools law rules "$OUT/"
cp governance/events.jsonl governance/principals.json "$OUT/governance/"
find "$OUT" -name "__pycache__" -type d -prune -exec rm -rf {} +
LEAK=$(find "$OUT" \( -name ".env*" -o -iname "*token*" -o -name "*.key" -o -name "*.pem" \) -print)
if [ -n "$LEAK" ]; then echo "refused: secrets in the package: $LEAK"; exit 1; fi
printf "commit %s\nbuilt %s\nverify must be ok at that commit (python -I verify.py)\n" "$(git rev-parse --short=9 HEAD)" "$(date -u +%FT%TZ)" > "$OUT/VERSION"
echo "package: $(du -sh "$OUT" | cut -f1) in $OUT"
# smoke test from the package, not from the repo: start, ask, stop
PORT=5341 python3 -I "$OUT/tools/serve.py" > "${TMPDIR:-/tmp}/ccp-package-serve.log" 2>&1 &
PID=$!
sleep 1
python3 - <<'PY'
import json, sys, urllib.request
out = json.loads(urllib.request.urlopen("http://127.0.0.1:5341/v1/saude", timeout=10).read())
print("smoke test from the package:", "OK" if out.get("ok") else "FAILED", out)
sys.exit(0 if out.get("ok") else 1)
PY
STATUS=$?
kill $PID 2>/dev/null || true
exit $STATUS
