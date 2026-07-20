#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SITE_DIR="$ROOT/site"
DIST_DIR="$ROOT/deploy/dist"
PUBLIC_URL="${PUBLIC_URL:-https://aunomira-lab.github.io/knowledge-subscription/}"
PAYMENT_URL="${PAYMENT_URL:-PAYMENT_URL_TO_FILL_AFTER_USER_AUTH}"
CONTACT_EMAIL="${CONTACT_EMAIL:-contact@ai-radar.dev}"
mkdir -p "$DIST_DIR"
cp "$SITE_DIR/index.html" "$DIST_DIR/index.html"
python3 - "$DIST_DIR/index.html" "$PUBLIC_URL" "$PAYMENT_URL" "$CONTACT_EMAIL" <<'PY'
from pathlib import Path
import sys
path=Path(sys.argv[1]); public_url,payment_url,contact_email=sys.argv[2:5]
text=path.read_text(encoding='utf-8')
text=text.replace('PUBLIC_URL_TO_FILL_AFTER_DEPLOY', public_url).replace('PAYMENT_URL_TO_FILL_AFTER_USER_AUTH', payment_url).replace('contact@ai-radar.dev', contact_email)
path.write_text(text, encoding='utf-8')
PY
printf 'Generated deployable static site: %s
Verify with: curl -I "%s"
' "$DIST_DIR/index.html" "$PUBLIC_URL"
