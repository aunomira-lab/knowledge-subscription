#!/usr/bin/env bash
set -euo pipefail
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_DIR"

required=("site/index.html" "docs/launch_execution_plan.md" "metrics/launch_channels.csv")
for f in "${required[@]}"; do
  test -f "$f" || { echo "ERROR: missing $f" >&2; exit 2; }
done

grep -q "¥29/月" site/index.html || { echo "ERROR: missing entry price" >&2; exit 3; }
grep -q "¥99/月" site/index.html || { echo "ERROR: missing pro price" >&2; exit 3; }
grep -q "mailto:" site/index.html || { echo "ERROR: missing contact/payment entry" >&2; exit 3; }
grep -q "不保证收益" site/index.html || { echo "ERROR: missing compliance disclaimer" >&2; exit 3; }

if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  echo "BLOCKED_BY_USER: current directory is not a git repository. Create/authorize repo before publishing." >&2
  exit 10
fi

if ! git remote get-url origin >/dev/null 2>&1; then
  echo "BLOCKED_BY_USER: git remote origin missing. Add GitHub repo remote before publishing." >&2
  exit 11
fi

git status --short
if ! git diff --quiet -- site/index.html deploy/README.md docs/launch_execution_plan.md metrics/launch_channels.csv docs/deployment_blockers.md reports/deployment_verification.md; then
  git add site/index.html deploy/README.md deploy/deploy_github_pages.sh docs/launch_execution_plan.md metrics/launch_channels.csv docs/deployment_blockers.md reports/deployment_verification.md
  git commit -m "Deploy knowledge subscription sales page" || true
fi

echo "READY_TO_PUSH: run 'git push origin main' after confirming GitHub Pages branch/folder settings."
