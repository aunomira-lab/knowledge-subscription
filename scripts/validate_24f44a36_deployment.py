#!/usr/bin/env python3
from pathlib import Path
import csv, json, sys, re
root = Path(__file__).resolve().parents[1]
required = ['site/index.html','deploy/README.md','docs/launch_execution_plan.md','metrics/launch_channels.csv','deploy/deploy_github_pages.sh','deploy/run_daily_subscription_ops.sh','deploy/verify_public_url.sh','docs/deployment_blockers.md']
errors=[]
for rel in required:
    p=root/rel
    if not p.exists() or p.stat().st_size < 80:
        errors.append(f'missing_or_too_small:{rel}')
html=(root/'site/index.html').read_text(encoding='utf-8')
checks={
 'paid_offers': all(x in html for x in ['¥29/月','¥99/月','¥499/次']),
 'contact_or_checkout': 'mailto:contact@ai-radar.dev' in html,
 'subscription_entry': any(x in html for x in ['立即订阅','购买专业版','索取免费试读']),
 'platforms': all(x in html for x in ['知乎','小红书','即刻']),
 'utm': 'utm_campaign=ks_launch_24f44a36' in html and 'utm_source=' in html,
 'no_income_guarantee': '不承诺收益' in html,
 'ad_prerequisite': '广告投放前置条件' in html,
}
for k,v in checks.items():
    if not v: errors.append(k)
rows=list(csv.DictReader((root/'metrics/launch_channels.csv').open(encoding='utf-8')))
if len(rows) < 3: errors.append('less_than_3_channels')
if not all(r.get('ad_prerequisite') and r.get('next_action') for r in rows): errors.append('channel_missing_prereq_or_next_action')
plan=(root/'docs/launch_execution_plan.md').read_text(encoding='utf-8')
for token in ['Day 1','Day 7','广告投放前置条件','¥29','¥499','知乎','小红书','即刻']:
    if token not in plan: errors.append('plan_missing:'+token)
print(json.dumps({'ok': not errors, 'errors': errors, 'files_checked': required, 'channels': len(rows), 'checks': checks}, ensure_ascii=False, indent=2))
sys.exit(1 if errors else 0)
