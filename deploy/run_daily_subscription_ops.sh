#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DAY="$(date -u +%F)"
OUT="$ROOT/reports/daily_launch_${DAY}.md"
cat > "$OUT" <<EOF
# AI 赚钱机会雷达每日获客动作 - $DAY

公开 URL：https://aunomira-lab.github.io/knowledge-subscription/

## 今日必须执行
1. 检查 metrics/launch_channels.csv，选择 1 个主渠道和 1 个补充渠道。
2. 发布或复发 1 条免费样例内容，CTA：回复“AI雷达”领取试看。
3. 私信/触达 10 个潜在客户，记录咨询、深聊、付款。
4. 若有付款，24 小时内交付首周内容包。
5. 若自然 PV <100 或咨询 <3，不投广告。

## 今日记录
- 曝光：
- 点击：
- 咨询：
- 付款：
- 收入：
- 阻塞：真实收款/客服入口若未授权，继续使用人工意向收集。
EOF
echo "$OUT"
