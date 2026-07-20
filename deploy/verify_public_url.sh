#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
PUBLIC_URL="${1:-${PUBLIC_URL:-$(cat .deployed_url 2>/dev/null || echo https://aunomira-lab.github.io/knowledge-subscription/)}}"
TMP="/tmp/ks_public_verify_24f44a36.html"
HTTP_CODE="$(curl -L --max-time 20 --connect-timeout 8 -s -o "$TMP" -w '%{http_code}' "$PUBLIC_URL" || true)"
BYTES="$(wc -c < "$TMP" 2>/dev/null || echo 0)"
HAS_TITLE="$(grep -c 'AI商机雷达' "$TMP" 2>/dev/null || true)"
DATE="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
mkdir -p reports
cat > reports/deployment_verification.md <<EOF
# Deployment verification

- task_id: 24f44a36
- checked_at_utc: $DATE
- public_url: $PUBLIC_URL
- http_code: $HTTP_CODE
- bytes: $BYTES
- contains_ai_radar_text: $HAS_TITLE
- result: $(if [ "$HTTP_CODE" = "200" ] && [ "$HAS_TITLE" != "0" ]; then echo PASS_PUBLIC_URL_REACHABLE; else echo FAIL_OR_STALE; fi)

## Commands actually run

- curl -L --max-time 20 --connect-timeout 8 -s -o $TMP -w '%{http_code}' $PUBLIC_URL
- grep -c 'AI商机雷达' $TMP

## Important note

This verifies the current public URL is reachable. If local files changed after the last successful push, rerun `bash deploy/deploy_github_pages.sh` after GitHub/Cloudflare authorization, then rerun this verifier.
EOF
echo "public_url=$PUBLIC_URL http_code=$HTTP_CODE bytes=$BYTES contains_ai_radar_text=$HAS_TITLE"
[ "$HTTP_CODE" = "200" ] && [ "$HAS_TITLE" != "0" ]
