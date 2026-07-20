#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
URL="${1:-${PUBLIC_URL:-$(cat .deployed_url 2>/dev/null || echo https://aunomira-lab.github.io/knowledge-subscription/)}}"
TMP="/tmp/ks_public_verify_24f44a36.html"
HTTP_CODE="$(curl -L --max-time 20 --connect-timeout 8 -s -o "$TMP" -w '%{http_code}' "$URL" || true)"
BYTES="$(wc -c < "$TMP" 2>/dev/null || echo 0)"
TEXT_HITS="$(grep -c 'AI商机雷达' "$TMP" 2>/dev/null || true)"
CHECKED_AT="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
RESULT="FAIL_PUBLIC_URL"
if [ "$HTTP_CODE" = "200" ] && [ "${TEXT_HITS:-0}" -gt 0 ]; then RESULT="PASS_PUBLIC_URL_REACHABLE"; fi
cat > reports/deployment_verification.md <<EOF
# Deployment verification

- task_id: 24f44a36
- checked_at_utc: $CHECKED_AT
- public_url: $URL
- http_code: $HTTP_CODE
- bytes: $BYTES
- contains_ai_radar_text: $TEXT_HITS
- result: $RESULT

## Commands actually run

- curl -L --max-time 20 --connect-timeout 8 -s -o $TMP -w '%{http_code}' $URL
- grep -c 'AI商机雷达' $TMP

## Important note

This verifies the current public URL is reachable. If local files changed after the last successful push, rerun: bash deploy/deploy_github_pages.sh after GitHub/Cloudflare authorization, then rerun this verifier.
EOF
cat reports/deployment_verification.md
[ "$RESULT" = "PASS_PUBLIC_URL_REACHABLE" ]
