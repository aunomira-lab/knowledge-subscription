# KPI Dashboard: AI Architecture Weekly

**Project ID**: knowledge-subscription  
**Task ID**: 96cae9d2  
**Type**: monitoring  
**Last Updated**: 2026-05-21  
**Refresh Frequency**: Daily at 21:00 UTC  
**Owner**: dev-optimizer (profitability-analyst)

---

## 1. North Star Metrics

> 自动化脚本: 运行 `python scripts/daily_metrics_update.py` 自动生成日报并填充关键指标。

|| Metric | Definition | Target (M1) | Target (M3) | Target (M12) | Data Source |
|--------|-----------|-------------|-------------|--------------|-------------|
|| MRR (USD) | Monthly Recurring Revenue — Stripe | $75 | $375 | $3,750 | Stripe dashboard |
|| MRR (CNY) | Monthly Recurring Revenue — 小报童/知识星球 | ¥500 | ¥3,000 | ¥30,000 | 小报童后台 + 知识星球 |
|| Paid Subscribers (EN) | Active paying users — Substack | 5 | 25 | 250 | Substack + Stripe |
|| Paid Subscribers (CN) | Active paying users — 中文平台 | 10 | 50 | 300 | 小报童 + 知识星球 |
|| Free Subscribers (EN) | Email list size | 200 | 800 | 5,000 | Substack analytics |
|| Free Subscribers (CN) | 公众号关注 + 小红书粉丝 + 即刻关注 | 300 | 1,500 | 8,000 | 各平台后台 |
|| Free→Paid Conversion Rate (EN) | Paid / Free (cumulative) | 2.5% | 3.1% | 5.0% | Substack + Stripe |
|| Free→Paid Conversion Rate (CN) | 付费 / 免费受众 (累计) | 3.0% | 3.5% | 6.0% | 小报童 + 公众号 |
|| Net Revenue Retention | (MRR now - churned) / MRR last month | — | > 100% | > 100% | Stripe + 小报童 |
|| 定制/咨询收入 (CN) | 一次性报告 + 企业内训 | ¥1,000 | ¥5,000 | ¥20,000 | 微信/支付宝收款记录 |

---

## 2. Conversion Funnel Metrics

### 英文漏斗 (Substack → Stripe)

|| Stage | Metric | Target | Alert Threshold | Source |
|-------|--------|--------|-----------------|--------|
|| Awareness | Weekly impressions (Twitter+LinkedIn+HN) | 3,000 | < 1,000 | Twitter Analytics, LinkedIn Analytics, HN |
|| Interest | Substack unique visitors/week | 500 | < 200 | Substack analytics |
|| Sign-up | Free subscribers/week | 50 | < 20 | Substack analytics |
|| Activation | Free subscribers with > 2 min read time | 60% | < 40% | Substack analytics |
|| Conversion | Paid subscribers/week | 3 | < 1 | Stripe |
|| Retention | Monthly churn rate | < 8% | > 12% | Stripe + Substack |
|| Expansion | Upgrades to Team tier/month | 0 | — | Stripe |
|| Referral | Referral-driven free subs/week | 5 | < 2 | Substack referral stats |

### 中文漏斗 (公众号/小红书 → 小报童/知识星球)

|| Stage | Metric | Target | Alert Threshold | Source |
|-------|--------|--------|-----------------|--------|
|| Awareness | 公众号阅读量 + 小红书曝光/周 | 5,000 | < 2,000 | 公众号后台 + 小红书创作者中心 |
|| Interest | 小报童专栏访客/周 | 300 | < 100 | 小报童数据后台 |
|| Sign-up | 小报童试读 → 关注/周 | 30 | < 10 | 小报童 |
|| Conversion | 小报童付费订阅/周 | 5 | < 2 | 小报童收款记录 |
|| Conversion | 知识星球付费/周 | 3 | < 1 | 知识星球后台 |
|| Retention | 小报童/星球 月退订率 | < 10% | > 15% | 平台后台 |
|| 定制线索 | 微信询盘（定制/企业内训）/周 | 2 | < 1 | 微信聊天记录 |

---

## 3. Content Performance Metrics

### 英文内容

|| Metric | Definition | Target | Alert | Source |
|--------|-----------|--------|-------|--------|
|| Open Rate | Email opens / deliveries | > 45% | < 35% | Substack email stats |
|| Click-Through Rate | Clicks / opens | > 8% | < 4% | Substack email stats |
|| Read Time | Avg time on page | > 3 min | < 1.5 min | Substack analytics |
|| Reply Rate | Direct replies / deliveries | > 1% | < 0.2% | Substack + manual |
|| Share Rate | Social shares / opens | > 2% | < 0.5% | Substack + manual |
|| Unsubscribe Rate | Unsubscribes / deliveries | < 1% | > 3% | Substack analytics |

### 中文内容

|| Metric | Definition | Target | Alert | Source |
|--------|-----------|--------|-------|--------|
|| 公众号打开率 | 打开 / 送达 | > 10% | < 5% | 公众号后台 |
|| 小红书互动率 | (赞+藏+评) / 曝光 | > 5% | < 2% | 小红书创作者中心 |
|| 知乎赞同率 | 赞同 / 阅读 | > 3% | < 1% | 知乎创作者中心 |
|| 即刻赞评比 | (赞+评) / 曝光 | > 4% | < 1% | 即刻后台 |
|| 文末二维码扫码率 | 扫码 / 阅读 | > 2% | < 0.5% | 小报童渠道码统计 |
|| 私域加微率 | 加微信 / 阅读 | > 0.5% | < 0.1% | 微信个人号统计 |

---

## 4. Financial Metrics

|| Metric | Formula | M1 Target | M3 Target | M12 Target | Source |
|--------|---------|-----------|-----------|------------|--------|
|| ARR (USD) | MRR * 12 | $900 | $4,500 | $45,000 | Derived |
|| ARR (CNY) | MRR * 12 | ¥6,000 | ¥36,000 | ¥360,000 | Derived |
|| ARPU (EN avg) | Total EN revenue / EN paid subs | $150/yr | $150/yr | $180/yr | Stripe |
|| ARPU (CN avg) | Total CN revenue / CN paid subs | ¥200/yr | ¥250/yr | ¥300/yr | 小报童+星球 |
|| Gross Margin | (Revenue - direct costs) / Revenue | > 85% | > 85% | > 85% | Derived |
|| LTV (EN) | ARPU * avg lifespan | $280 | $300 | $360 | Derived |
|| LTV (CN) | ARPU * avg lifespan | ¥400 | ¥500 | ¥600 | Derived |
|| CAC (EN) | Total EN marketing spend / new EN paid subs | < $30 | < $25 | < $20 | Derived |
|| CAC (CN) | Total CN marketing spend / new CN paid subs | < ¥80 | < ¥60 | < ¥40 | Derived |
|| LTV:CAC (EN) | LTV / CAC | > 10:1 | > 12:1 | > 18:1 | Derived |
|| LTV:CAC (CN) | LTV / CAC | > 5:1 | > 8:1 | > 15:1 | Derived |
|| Payback Period | CAC / (MRR per sub) | < 3 months | < 2 months | < 1 month | Derived |
|| Operating Cash Flow | Revenue - content cost - fixed costs | -$900 | -$300 | +$2,500 | Derived |
|| 定制/咨询毛利率 | (收入 - 时间成本) / 收入 | > 90% | > 90% | > 90% | Derived |

---

## 5. Operational Health Metrics

|| Metric | Definition | Green | Yellow | Red | Action |
|--------|-----------|-------|--------|-----|--------|
|| Content Buffer (EN) | Issues ready to publish | >= 2 | 1 | 0 | Emergency writing sprint |
|| Content Buffer (CN) | 中文稿件储备 | >= 2 | 1 | 0 | 紧急翻译/改写 sprint |
|| Publish On-Time Rate | Issues published by 08:00 UTC | 100% | >= 80% | < 80% | Adjust workflow |
|| 中文发布准时率 | 中文内容在 11:00 UTC 前发布 | 100% | >= 80% | < 80% | 调整排期 |
|| Code Example Test Pass | All code examples run before publish | 100% | >= 90% | < 90% | Fix before publish |
|| Support Response Time | First reply to customer inquiry | < 4 hrs | < 24 hrs | > 24 hrs | See incident runbook |
|| 微信私域回复时效 | 首次回复微信消息 | < 2 hrs | < 8 hrs | > 8 hrs | 见 docs/customer_support.md |
|| Platform Uptime | Substack + Stripe + 小报童 可用性 | 99.9% | >= 99% | < 99% | Check status pages |
|| Daily Metrics Filled | experiment_tracker.csv 当日已更新 | Yes | — | No | 21:00 UTC 前必须完成 |
|| Daily Report Generated | daily_metrics_update.py 已运行 | Yes | — | No | 21:30 UTC 前必须完成 |

---

## 6. Daily Operations Board (Auto-generated + Manual)

### Auto-Generation
运行以下命令自动生成日报摘要：
```bash
cd /home/AgentAdmin/.hermes/shared/dev-team/projects/knowledge-subscription
python3 scripts/daily_metrics_update.py
```
输出位置: `reports/daily/DAILY_REPORT_YYYY-MM-DD.md`

### Manual Template (Fallback / Cross-check)

Fill this table daily. Copy-paste the template row and update values.

```
| Date | Free Subs Δ | Paid Subs Δ | MRR | Open Rate | CTR | Rev Today | Cum Rev | 中文付费 | 定制收入 | 获客动作完成 | Notes |
|------|-------------|-------------|-----|-----------|-----|-----------|---------|----------|----------|--------------|-------|
| YYYY-MM-DD | +0 | +0 | $0 | 0% | 0% | $0 | $0 | ¥0 | ¥0 | 0/5 | — |
```

### Live Rows (Week 1 — Experiment Period)

| Date | Free Subs Δ | Paid Subs Δ | MRR | Open Rate | CTR | Rev Today | Cum Rev | 中文付费 | 定制收入 | 获客动作完成 | Notes |
|------|-------------|-------------|-----|-----------|-----|-----------|---------|----------|----------|--------------|-------|
| 2026-05-21 | +0 | +0 | $0 | — | — | $0 | $0 | ¥0 | ¥0 | 0/5 | BLOCKED: Cloudflare auth missing; sales page offline |
| 2026-05-22 | +0 | +0 | $0 | — | — | $0 | $0 | ¥0 | ¥0 | 0/5 | BLOCKED: Payment channel not configured; funnel broken |
| 2026-05-23 | +0 | +0 | $0 | — | — | $0 | $0 | ¥0 | ¥0 | 0/5 | STOP gate triggered: 0 free subs (< 10). Halted content spend. |
| 2026-05-24 | — | — | — | — | — | — | — | — | — | — | ON HOLD pending deployment unblock |
| 2026-05-25 | — | — | — | — | — | — | — | — | — | — | ON HOLD — cannot execute conversion push without live funnel |
| 2026-05-26 | — | — | — | — | — | — | — | — | — | — | ON HOLD |
| 2026-05-27 | — | — | — | — | — | — | — | — | — | — | ON HOLD |
| 2026-05-28 | — | — | — | — | — | — | — | — | — | — | Retrospective: STOP verdict due to deployment block |

> **Action**: 每天 21:00 UTC 前，根据各平台后台数据填入上表。然后运行 `python scripts/daily_metrics_update.py` 生成日报。
> **Current Action (2026-05-23)**: Do NOT fill new content rows until deployment blockers resolved. Focus on unblocking per `docs/deployment_blockers.md`.

---

## 7. This Week's 3 Money-Making Actions (MUST DO)

**Status (2026-05-23)**: Experiment STOPPED due to deployment block. The original 3 actions below are ON HOLD. They cannot generate revenue until the sales page is live.

### Current Priority (Unblocking)
1. **获取 Cloudflare API Token 并完成首次部署** (最高阻塞): 没有这一步，销售页永远离线，所有获客动作归零。参考 `docs/deployment_blockers.md` Step 1-2。
2. **注册小报童并创建 ¥29/月专栏** (收款阻塞): 没有支付渠道，用户无法转化。参考 `docs/deployment_blockers.md` Step 3。
3. **替换销售页占位信息** (信任阻塞): 微信/邮箱/支付链接为占位符 = 用户无法联系或付款。参考 `docs/deployment_blockers.md` Step 4。

### Original Actions (Resume After Unblock)
1. **开通小报童专栏** (阻塞收款): 注册 xiaobot.net，上传 3 篇试读，设置 ¥29/月早鸟价。没有小报童 = 中文市场零收入。
2. **Day 5 转化冲刺** (决定实验成败): 给英文免费列表发 founding-member 限时邮件; 在中文社群发早鸟截止倒计时朋友圈。这是 7 天内唯一一次集中转化动作，必须全力执行。
3. **获取第一条用户 testimonial** (降低后续获客成本): 无论付费用户有多少，主动联系 3 位深度阅读免费内容的用户，询问"哪篇对你最有帮助?" 将回复截图保存为 `reports/testimonials/raw_001.md`，用于销售页社会证明。

---

## 8. Weekly Review Checklist

Every Monday at 09:00 UTC:
- [ ] Pull Stripe dashboard: MRR, new subs, churn, refunds
- [ ] Pull 小报童后台: 新增订阅、退订、收入
- [ ] Pull 知识星球后台: 新增、活跃、收入
- [ ] Pull Substack analytics: opens, CTR, unsubscribes, top referrers
- [ ] Pull Twitter/LinkedIn analytics: impressions, profile clicks
- [ ] Pull 公众号/小红书/知乎后台: 阅读量、互动、新增关注
- [ ] Update this dashboard with actuals
- [ ] Compare vs. `metrics/experiment_tracker.csv`
- [ ] Identify top-performing content (highest open/CTR/中文互动)
- [ ] Identify worst-performing content (investigate why)
- [ ] Adjust next week's content calendar based on data
- [ ] Update `docs/revenue_experiment_7d.md` if experiment is running
- [ ] File weekly summary to `reports/weekly_kpi_summary_YYYY-MM-DD.md`
- [ ] 复盘本周 3 件赚钱动作是否完成，写入下周计划

---

## 9. Alert Escalation Matrix

||| Alert Condition | Severity | Notify | Response Time | Action |
|-------------------|----------|--------|---------------|--------|
||| MRR (EN+CN) drops > 20% vs last week | P1 | dev-optimizer, dev-architect | 1 hr | Emergency content + retention push |
||| 中文收入归零 (小报童/星球被封) | P0 | dev-optimizer, dev-security, dev-architect | 1 hr | 立即切换微信个人收款 + 公众号导流 |
||| **销售页离线超过 24 小时 (部署阻塞)** | **P0** | **dev-optimizer, dev-deploy, user** | **1 hr** | **执行 `docs/deployment_blockers.md` 解封步骤；若用户授权缺失，记录为 BLOCKED_BY_USER** |
||| Churn rate > 12% monthly (EN) | P1 | dev-optimizer, dev-architect | 4 hrs | Exit survey + win-back email |
||| 中文退订率 > 20%/月 | P1 | dev-optimizer, dev-architect | 4 hrs | 发问卷调查 + 私聊挽留 |
||| Unsubscribe spike > 5% on single email | P2 | dev-optimizer | 4 hrs | Review content; pause similar topics |
||| Open rate < 30% for 2 consecutive emails | P2 | dev-optimizer | 24 hrs | A/B test subject lines; segment inactive |
||| Stripe payout failed / account issue | P1 | dev-optimizer, dev-deploy | 1 hr | Check Stripe dashboard; contact support |
||| Substack publish failure | P2 | dev-optimizer | 2 hrs | Manual publish backup; check `docs/incident_runbook.md` |
||| Hacker News front-page traffic spike | P0 | All hands | Immediate | Capture emails; enable landing page CTA |
||| Support ticket > 24 hrs unanswered | P2 | dev-optimizer | Immediate | See `docs/customer_support.md` escalation |
||| 微信私域被封/限流 | P1 | dev-optimizer, dev-security | 2 hrs | 切换小红书/即刻/抖音; 通知社群管理员 |

---

## 10. Data Sources & Access

|| Source | URL / Location | Access Method | Update Frequency |
|--------|---------------|---------------|------------------|
|| Stripe Dashboard | dashboard.stripe.com | Login required | Real-time |
|| 小报童创作者后台 | xiaobot.net/pay | 微信扫码登录 | Daily |
|| 知识星球后台 | zsxq.com | 手机号登录 | Daily |
|| 微信公众号后台 | mp.weixin.qq.com | 微信扫码登录 | Daily |
|| 小红书创作者中心 | creator.xiaohongshu.com | 手机号登录 | Daily |
|| 知乎创作者中心 | zhihu.com/creator | 登录 | Daily |
|| Substack Analytics | substack.com/manage | Login required | Daily |
|| Twitter Analytics | analytics.twitter.com | Login required | Daily |
|| LinkedIn Analytics | linkedin.com/analytics | Login required | Weekly |
|| Experiment Tracker | `metrics/experiment_tracker.csv` | Git / local file | Daily |
|| KPI Dashboard | `docs/kpi_dashboard.md` | Git / local file | Daily |
|| Daily Auto Report | `reports/daily/DAILY_REPORT_*.md` | `python scripts/daily_metrics_update.py` | Daily |

---

**Next Review**: 2026-05-28  
**Owner**: dev-optimizer (profitability-analyst)  
**Backup Owner**: dev-architect
