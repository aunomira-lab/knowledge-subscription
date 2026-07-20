#!/usr/bin/env python3
from pathlib import Path
import csv, json, re, sys
root = Path(__file__).resolve().parents[1]
required = [
    'site/index.html',
    'deploy/README.md',
    'docs/launch_execution_plan.md',
    'metrics/launch_channels.csv',
    'deploy/deploy_github_pages.sh',
    'deploy/run_daily_subscription_ops.sh',
    'deploy/verify_public_url.sh',
    'docs/deployment_blockers.md',
]
errors=[]
for rel in required:
    p=root/rel
    if not p.exists() or p.stat().st_size < 80:
        errors.append(f'missing_or_too_small:{rel}')
html=(root/'site/index.html').read_text(encoding='utf-8')
checks={
 'paid_offers': all(x in html for x in ['¥29/月','¥99/月','¥499/次']),
 'contact_or_checkout': 'mailto:contact@ai-radar.dev' in html and 'PAYMENT_URL_TO_FILL_AFTER_USER_AUTH' in html,
 'subscription_entry': any(x in html for x in ['立即订阅','购买专业版','先领免费试读','订阅意向']),
 'platforms': all(x in html for x in ['知乎','小红书','即刻']),
 'utm': 'utm_campaign=ks_launch_24f44a36' in html and 'utm_source=' in html,
 'no_income_guarantee': '不承诺收益' in html,
 'ad_prerequisite': '广告投放前置条件' in html,
 'public_url': 'https://aunomira-lab.github.io/knowledge-subscription/' in html,
}
for k,v in checks.items():
    if not v: errors.append(k)
rows=list(csv.DictReader((root/'metrics/launch_channels.csv').open(encoding='utf-8')))
if len(rows) < 3: errors.append('less_than_3_channels')
for r in rows:
    if not r.get('ad_prerequisite') or not r.get('next_action') or not r.get('utm_campaign'):
        errors.append('channel_missing_required_fields:'+r.get('platform','UNKNOWN'))
plan=(root/'docs/launch_execution_plan.md').read_text(encoding='utf-8')
for token in ['Day 1','Day 7','广告投放前置条件','¥29','¥499','知乎','小红书','即刻','首周收入目标']:
    if token not in plan: errors.append('plan_missing:'+token)
readme=(root/'deploy/README.md').read_text(encoding='utf-8')
for token in ['GitHub Pages','Cloudflare Pages','用户账号授权步骤','收款/联系入口','crontab']:
    if token not in readme: errors.append('readme_missing:'+token)
print(json.dumps({'ok': not errors, 'errors': errors, 'files_checked': required, 'channels': len(rows), 'checks': checks}, ensure_ascii=False, indent=2))
sys.exit(1 if errors else 0)
