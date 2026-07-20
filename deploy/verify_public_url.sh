#!/usr/bin/env bash
set -euo pipefail
URL="${1:-https://aunomira-lab.github.io/knowledge-subscription/}"
TMP="$(mktemp)"
CODE="$(curl -L -sS -o "$TMP" -w '%{http_code}' --max-time 30 "$URL")"
echo "http_code=$CODE url=$URL"
grep -q 'AI 赚钱机会雷达' "$TMP"
grep -q '¥29/月' "$TMP"
grep -q '¥99/月' "$TMP"
grep -q '¥499/次' "$TMP"
grep -q '不承诺收益' "$TMP"
test "$CODE" = "200"
echo "page_content_check=pass"
