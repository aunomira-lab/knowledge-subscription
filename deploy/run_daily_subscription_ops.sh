#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
mkdir -p logs/daily metrics reports
TODAY="$(date -u +%Y-%m-%d)"
PUBLIC_URL="${PUBLIC_URL:-$(cat .deployed_url 2>/dev/null || echo https://aunomira-lab.github.io/knowledge-subscription/)}"
HTTP_CODE="$(curl -L -s -o /tmp/ks_daily_site.html -w '%{http_code}' "$PUBLIC_URL" || true)"
LEADS_FILE="metrics/leads.csv"
[ -f "$LEADS_FILE" ] || echo "date,channel,lead_name,contact,status,next_action" > "$LEADS_FILE"
[ -f "metrics/payment_delivery_tracker.csv" ] || echo "date,customer,plan,amount,status,delivery_link,next_action" > metrics/payment_delivery_tracker.csv
REPORT="logs/daily/${TODAY}_subscription_ops.md"
cat > "$REPORT" <<EOF
# Daily subscription ops - $TODAY

## Site health
- URL: $PUBLIC_URL
- HTTP: $HTTP_CODE

## Today's money actions
1. Publish one launch post from docs/launch_execution_plan.md on Zhihu/Xiaohongshu/Jike-WeChat.
2. DM/comment 20 target prospects with the free preview offer.
3. Record every reply in metrics/leads.csv.
4. Send ¥29 early-bird payment/contact entry to warm leads within 24 hours.
5. If paid, record in metrics/payment_delivery_tracker.csv and deliver sample pack.

## Funnel targets
- Visitors: 100/day
- Trial leads: 8/day
- Paid early-bird: 1/day
- Revenue target: ¥29-499/day during validation week

## Escalation
- If checkout/contact link is broken: mark BLOCKED_BY_USER in docs/deployment_blockers.md.
- If HTTP is not 200: rerun deploy/verify_public_url.sh and repair deployment.
EOF
cat "$REPORT"
[ "$HTTP_CODE" = "200" ] || exit 4
