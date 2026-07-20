#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
URL="${1:-https://aunomira-lab.github.io/knowledge-subscription/}"
cd "$ROOT"
python3 -m html.parser site/index.html >/dev/null
for needle in "¥29/月" "¥99/月" "¥499/次" "contact@ai-radar.dev" "不承诺收益" "7天获客"; do
  grep -q "$needle" site/index.html
  echo "local contains: $needle"
done
code="$(curl -L -s -o /tmp/knowledge_subscription_verify.html -w '%{http_code}' "$URL" || true)"
echo "public_url=$URL http_code=$code bytes=$(wc -c < /tmp/knowledge_subscription_verify.html 2>/dev/null || echo 0)"
if [ "$code" != "200" ]; then
  echo "PUBLIC_URL_NOT_200" >&2
  exit 44
fi
if ! grep -Eq "AI赚钱机会雷达|AI Opportunity Radar|订阅" /tmp/knowledge_subscription_verify.html; then
  echo "PUBLIC_URL_CONTENT_MISMATCH" >&2
  exit 45
fi
