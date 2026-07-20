#!/usr/bin/env python3
from pathlib import Path
import csv, json, sys
root = Path(__file__).resolve().parents[1]
required = [
    'site/index.html', 'deploy/README.md', 'docs/launch_execution_plan.md',
    'metrics/launch_channels.csv', 'docs/deployment_blockers.md', 'reports/deployment_verification.md',
    'deploy/deploy_github_pages_24f44a36.sh', 'deploy/deploy_static_site_24f44a36.sh',
    'deploy/run_daily_launch_ops_24f44a36.sh', 'deploy/verify_public_url_24f44a36.sh'
]
missing = [p for p in required if not (root/p).exists()]
if missing:
    raise SystemExit('missing required files: ' + ', '.join(missing))
html = (root/'site/index.html').read_text(encoding='utf-8')
for token in ['AI赚钱机会雷达','¥29/月','¥99/月','¥499/次','mailto:contact@ai-radar.dev','不构成投资','广告投放前置条件','GitHub Pages']:
    if token not in html:
        raise SystemExit(f'missing html token: {token}')
plan = (root/'docs/launch_execution_plan.md').read_text(encoding='utf-8')
for token in ['7天获客计划','知乎','小红书','微信社群','广告投放前置条件','GO']:
    if token not in plan:
        raise SystemExit(f'missing plan token: {token}')
rows = list(csv.DictReader((root/'metrics/launch_channels.csv').open(encoding='utf-8')))
if len(rows) < 7:
    raise SystemExit('launch_channels.csv must contain at least 7 execution rows')
platforms = {r['platform'] for r in rows}
if len(platforms) < 3:
    raise SystemExit('need at least 3 acquisition platforms')
result = {'ok': True, 'required_files': required, 'platform_count': len(platforms), 'channel_rows': len(rows)}
print(json.dumps(result, ensure_ascii=False, indent=2))
