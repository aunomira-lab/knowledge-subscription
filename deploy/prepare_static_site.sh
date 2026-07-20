#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
mkdir -p dist reports/sample_pack
cp site/index.html dist/index.html
if [ -f reports/sample_pack/free_preview.md ]; then
  mkdir -p dist/reports/sample_pack
  cp reports/sample_pack/free_preview.md dist/reports/sample_pack/free_preview.md
fi
python3 -m html.parser site/index.html >/dev/null
printf 'Prepared static site at %s/dist
' "$ROOT"
