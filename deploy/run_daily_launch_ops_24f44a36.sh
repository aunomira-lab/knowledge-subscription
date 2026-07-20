#!/usr/bin/env bash
set -euo pipefail
ROOT="/home/AgentAdmin/.hermes/shared/dev-team/projects/knowledge-subscription"
cd "$ROOT"
mkdir -p reports/daily metrics
STAMP=$(date -u +%Y-%m-%dT%H:%M:%SZ)
{
  echo "# Daily launch ops check $STAMP"
  echo
  bash deploy/verify_public_url_24f44a36.sh || true
  echo
  echo "## Pending channel links"
  awk -F, 'NR==1 || $7 ~ /待回填/ || $8 ~ /待回填/ {print}' metrics/launch_channels.csv || true
  echo
  echo "## Today money action"
  echo "发布/跟进免费样例；对高意向线索报价 Pro ¥99/月或定制 ¥499/次；记录曝光、线索、付费、收入。"
} > "reports/daily/launch_ops_${STAMP//[:]/}.md"
python3 scripts/validate_24f44a36_launch.py
