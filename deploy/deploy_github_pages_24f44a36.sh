#!/usr/bin/env bash
set -euo pipefail
ROOT="/home/AgentAdmin/.hermes/shared/dev-team/projects/knowledge-subscription"
cd "$ROOT"
python3 scripts/validate_24f44a36_launch.py
if ! gh auth status >/dev/null 2>&1; then
  echo "BLOCKED_BY_USER: GitHub CLI not authenticated. Run gh auth login." >&2
  exit 10
fi
git add site/index.html deploy/README.md docs/launch_execution_plan.md metrics/launch_channels.csv docs/deployment_blockers.md reports/deployment_verification.md deploy/local_preview_24f44a36.sh deploy/verify_public_url_24f44a36.sh deploy/run_daily_launch_ops_24f44a36.sh deploy/deploy_github_pages_24f44a36.sh deploy/deploy_static_site_24f44a36.sh scripts/validate_24f44a36_launch.py
if git diff --cached --quiet; then
  echo "No staged changes for task 24f44a36"
else
  git commit -m "deploy: refresh subscription landing page task 24f44a36"
  git push origin main
fi
bash deploy/verify_public_url_24f44a36.sh
