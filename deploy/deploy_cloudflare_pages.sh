#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
PROJECT_NAME="${CF_PAGES_PROJECT:-knowledge-subscription}"
cd "$ROOT"
bash deploy/prepare_static_site.sh
if [ -z "${CLOUDFLARE_ACCOUNT_ID:-}" ] || [ -z "${CLOUDFLARE_API_TOKEN:-}" ]; then
  echo "BLOCKED_BY_USER: set CLOUDFLARE_ACCOUNT_ID and CLOUDFLARE_API_TOKEN with Pages edit permission." >&2
  exit 42
fi
if ! command -v npx >/dev/null 2>&1; then
  echo "ERROR: npx is required for wrangler deployment." >&2
  exit 43
fi
npx --yes wrangler pages deploy dist --project-name "$PROJECT_NAME" --branch main
