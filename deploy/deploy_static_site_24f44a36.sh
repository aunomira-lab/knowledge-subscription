#!/usr/bin/env bash
set -euo pipefail
ROOT="/home/AgentAdmin/.hermes/shared/dev-team/projects/knowledge-subscription"
cd "$ROOT"
python3 scripts/validate_24f44a36_launch.py
if ! wrangler whoami >/dev/null 2>&1; then
  echo "BLOCKED_BY_USER: Cloudflare wrangler is not authenticated. Run: wrangler login" >&2
  exit 11
fi
PROJECT_NAME="${CF_PAGES_PROJECT:-knowledge-subscription}"
wrangler pages deploy site --project-name "$PROJECT_NAME" --commit-dirty=true
