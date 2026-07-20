#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
PUBLIC_URL="${PUBLIC_URL:-$(cat .deployed_url 2>/dev/null || echo https://aunomira-lab.github.io/knowledge-subscription/)}"
python3 scripts/validate_24f44a36_deployment.py
if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  echo "BLOCKED_BY_USER: not a git repository; upload site/ manually to Cloudflare Pages/Vercel/GitHub Pages."
  exit 3
fi
if ! git ls-remote --exit-code origin >/dev/null 2>&1; then
  echo "BLOCKED_BY_USER: git remote not reachable with current credentials. See docs/deployment_blockers.md"
  exit 3
fi
git add site/index.html deploy/README.md deploy/deploy_github_pages.sh deploy/run_daily_subscription_ops.sh deploy/verify_public_url.sh docs/launch_execution_plan.md docs/deployment_blockers.md metrics/launch_channels.csv scripts/validate_24f44a36_deployment.py reports/deployment_verification.md .deployed_url
if ! git diff --cached --quiet; then
  git commit -m "Deploy knowledge subscription sales page 24f44a36" || true
  git push origin HEAD:main
else
  echo "No staged changes to push."
fi
bash deploy/verify_public_url.sh "$PUBLIC_URL"
