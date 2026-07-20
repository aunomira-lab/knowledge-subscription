#!/usr/bin/env bash
set -euo pipefail
URL="${1:-https://aunomira-lab.github.io/knowledge-subscription/}"
TMP="${TMPDIR:-/tmp}/knowledge_subscription_verify_24f44a36.html"
HTTP=$(curl -L -s -o "$TMP" -w '%{http_code}' "$URL")
echo "http_code=$HTTP url=$URL bytes=$(wc -c < "$TMP")"
case "$HTTP" in 200|301|302) ;; *) echo "ERROR: URL did not return success/redirect" >&2; exit 2;; esac
grep -q "AI赚钱机会雷达" "$TMP"
grep -q "¥99/月" "$TMP"
grep -q "订阅" "$TMP"
echo "PUBLIC_URL_OK"
