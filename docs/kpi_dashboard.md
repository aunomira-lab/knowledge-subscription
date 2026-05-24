# KPI Dashboard: AI Architecture Weekly

**Project ID**: knowledge-subscription  
**Task ID**: ab047a39  
**Type**: monitoring  
**Last Updated**: 2026-05-24  
**Refresh Frequency**: Daily at 21:00 UTC  
**Owner**: dev-optimizer (profitability-analyst)

---

## 1. North Star Metrics

> Phase 2 (2026-05-24 to 2026-05-31) uses manual collection. North Star = revenue captured via WeChat/Alipay QR codes.

| Metric | Definition | Target (Week 1) | Target (Month 1) | Target (Month 3) | Data Source |
|--------|-----------|-----------------|------------------|------------------|-------------|
| MRR (Manual CNY) | Monthly Recurring Revenue — manual WeChat/Alipay | ¥200 | ¥1,000 | ¥5,000 | WeChat/支付宝收款记录 + `metrics/experiment_tracker.csv` |
| Paid Conversions (Manual) | Users who sent money via personal QR | 3 | 15 | 60 | 收款记录 |
| Free Contacts (WeChat) | New WeChat friends from content | 30 | 150 | 600 | 微信通讯录 |
| Content Impressions | 小红书+知乎+即刻+公众号 曝光 | 2,000 | 15,000 | 60,000 | 各平台创作者后台 |
| Engagement Rate | (赞+藏+评+转) / 曝光 | > 3% | > 4% | > 5% | 各平台后台 |
| Free→Paid Conversion Rate | 付费人数 / 加微人数 | > 5% | > 8% | > 10% | `metrics/experiment_tracker.csv` |
| Offer Acceptance Rate | 付款人数 / 明确报价人数 | > 20% | > 25% | > 30% | 微信聊天记录 |
| Testimonials Collected | 用户原话截图或文字授权 | 1 | 5 | 20 | `reports/testimonials/` |

---

## 2. Conversion Funnel Metrics (Phase 2 — Manual / WeChat-native)

| Stage | Metric | Target (7d) | Alert Threshold | Source |
|-------|--------|-------------|-----------------|--------|
| Awareness | 小红书+知乎+即刻 周曝光 | 2,000 | < 500 | 小红书创作者中心 / 知乎创作者中心 / 即刻后台 |
| Interest | 加微信人数/周 | 30 | < 10 | 微信通讯录 |
| Trust | 接收免费资料人数/周 | 20 | < 5 | 微信发送记录 |
| Conversion | 微信/支付宝付款笔数/周 | 3 | < 1 | 收款码记录 |
| Retention | 7天内复购或升级人数 | 0 | — | 收款记录 |
| Referral | 推荐新用户人数/周 | 0 | — | 用户主动提及 |
| 英文 Gumroad | Pay-what-you-want 收入/周 | $5-20 | $0 | Gumroad dashboard (if active) |

---

## 3. Content Performance Metrics

### 中文内容 (小红书 / 知乎 / 即刻 / 微信群)

| Metric | Definition | Target | Alert | Source |
|--------|-----------|--------|-------|--------|
| 小红书曝光 | 笔记被看到次数 | > 500/篇 | < 100/篇 | 小红书创作者中心 |
| 小红书互动率 | (赞+藏+评) / 曝光 | > 5% | < 2% | 小红书创作者中心 |
| 知乎阅读量 | 回答/文章阅读 | > 300/篇 | < 50/篇 | 知乎创作者中心 |
| 知乎赞同率 | 赞同 / 阅读 | > 3% | < 1% | 知乎创作者中心 |
| 即刻赞评比 | (赞+评) / 曝光 | > 4% | < 1% | 即刻后台 |
| 微信群互动 | 群内消息数 + 被@次数 | > 5条/天 | < 1条/天 | 微信 |
| 朋友圈可见互动 | 赞+评 / 好友数 | > 2% | < 0.5% | 微信 |
| 私域加微率 | 新加好友 / 内容曝光 | > 1% | < 0.3% | 微信 + 平台后台 |

### 英文内容 (Twitter / LinkedIn)

| Metric | Definition | Target | Alert | Source |
|--------|-----------|--------|-------|--------|
| Impressions | Twitter + LinkedIn 曝光 | > 1,000/周 | < 300/周 | Twitter Analytics / LinkedIn Analytics |
| Profile clicks | 个人资料点击 | > 20/周 | < 5/周 | Twitter Analytics |
| Replies/engagement | 回复和互动数 | > 10/周 | < 3/周 | Twitter / LinkedIn |
| Gumroad views (if active) | 产品页访问 | > 50/周 | < 10/周 | Gumroad dashboard |
| Gumroad conversions | 付款笔数 (any amount) | >= 1/周 | 0/2周 | Gumroad dashboard |

---

## 4. Financial Metrics

| Metric | Formula | Week 1 Target | Month 1 Target | Month 3 Target | Source |
|--------|---------|---------------|----------------|----------------|--------|
| Gross Revenue (CNY) | Sum of all manual payments | ¥200 | ¥1,000 | ¥5,000 | 收款记录 |
| Gross Revenue (USD) | Gumroad + Stripe (when active) | $5 | $50 | $500 | Gumroad / Stripe |
| Average Revenue Per User (ARPU) | Revenue / paid users | ¥40-67 | ¥67 | ¥83 | Derived |
| Cost per Acquisition (CAC) | Time cost + any ad spend / new paid user | < ¥50 | < ¥40 | < ¥30 | Derived |
| Gross Margin | (Revenue - 0) / Revenue | 100% | 100% | ~85% | Derived |
| Time Invested | Hours/day on content + DM + support | ~1.2 hrs | ~1.5 hrs | ~2.0 hrs | Manual log |
| Hourly Yield | Revenue / time invested | > ¥30/hr | > ¥50/hr | > ¥80/hr | Derived |
| Cumulative Revenue | Running total since experiment start | ¥200 | ¥1,000 | ¥5,000 | `metrics/experiment_tracker.csv` |

---

## 5. Operational Health Metrics

| Metric | Definition | Green | Yellow | Red | Action |
|--------|-----------|-------|--------|-----|--------|
| Content Buffer |  tomorrow's post ready before 07:00 UTC | Ready | Draft only | Nothing | Emergency writing sprint (30 min) |
| Publish On-Time Rate | Post published by 08:00 UTC | 100% | >= 80% | < 80% | Adjust wake-up time / batch write |
| Daily DM Quota | 5 target DMs sent/day | 5/5 | 3-4/5 | < 3/5 | Review targeting criteria; expand pool |
| WeChat Reply SLA | First reply to new contact | < 2 hrs | < 8 hrs | > 8 hrs | Set phone alert for new friend requests |
| Revenue Logged | experiment_tracker.csv updated by 21:30 UTC | Yes | — | No | 21:00 UTC alarm |
| Payment Screenshots | Every payment screenshotted + filed | 100% | >= 80% | < 80% | Screenshot before anything else |
| Platform Risk | 小红书/知乎/微信 账号状态 | Healthy | Warning | Banned/limited | Switch channel immediately |

---

## 6. Daily Operations Board (Manual + Auto)

### Auto-Generation
```bash
cd /home/AgentAdmin/.hermes/shared/dev-team/projects/knowledge-subscription
python3 scripts/daily_metrics_update.py
```
Output: `reports/daily/DAILY_REPORT_YYYY-MM-DD.md`

### Manual Daily Tracker (Copy-paste row daily)

```
| Date | Platform | Post Topic | Impressions | Engagements | New WeChat | DMs Sent | Offers Made | Conv | Revenue | Cum Rev | Notes |
|------|----------|------------|-------------|-------------|------------|----------|-------------|------|---------|---------|-------|
| YYYY-MM-DD | 小红书 | ... | 0 | 0 | 0 | 0 | 0 | 0 | ¥0 | ¥0 | — |
```

### Live Rows (Phase 2 — Zero-Infrastructure Sprint)

| Date | Platform | Post Topic | Impressions | Engagements | New WeChat | DMs Sent | Offers Made | Conv | Revenue | Cum Rev | Notes |
|------|----------|------------|-------------|-------------|------------|----------|-------------|------|---------|---------|-------|
| 2026-05-24 | 小红书+即刻 | AI独立开发者5月新机会：3个被低估的MCP工具 | — | — | — | — | — | — | ¥0 | ¥0 | Phase 2 START. No infrastructure blockers. |
| 2026-05-25 | 小红书+知乎 | 我花了3天测试Cursor Agent模式，这是真实ROI | — | — | — | — | — | — | ¥0 | ¥0 | — |
| 2026-05-26 | 小红书+微信群 | 副业警报：AI客服月入2万的路径拆解 | — | — | — | — | — | — | ¥0 | ¥0 | First收款试探日 |
| 2026-05-27 | 小红书+即刻 | 长期上下文 vs RAG：一个架构决策省了$400/月 | — | — | — | — | — | — | ¥0 | ¥0 | — |
| 2026-05-28 | 小红书+朋友圈 | 上周帮一个读者省了2000块推理成本 | — | — | — | — | — | — | ¥0 | ¥0 | 转化冲刺日 |
| 2026-05-29 | 小红书+即刻 | AI赚钱雷达 Week 1 复盘 | — | — | — | — | — | — | ¥0 | ¥0 | 第二期预售 |
| 2026-05-30 | 小红书+朋友圈 | 下周预告 + 本周读者成果 | — | — | — | — | — | — | ¥0 | ¥0 | 收尾 |
| 2026-05-31 | — | REST + retrospective | — | — | — | — | — | — | ¥0 | ¥0 | Phase 2 review |

> **Action**: 每天 21:00 UTC 前，根据各平台后台数据填入上表。然后运行 `python scripts/daily_metrics_update.py` 生成日报。
> **Current Status (2026-05-24)**: Phase 2 ACTIVE. No deployment blockers. Target = ¥200 revenue in 7 days.

---

## 7. This Week's 3 Money-Making Actions (MUST DO)

1. **Day 3 第一次收款试探 (2026-05-26)**: 朋友圈发"7天AI副业陪伴营，早鸟¥29，限10人"。这是7天内第一个明确要钱动作，必须发。不发 = 实验失败。
2. **Day 5 转化冲刺 (2026-05-28)**: 私信所有加微的人，用具体价值点触发付款。话术模板："你之前对Cursor/AI客服/省钱架构感兴趣，我整理了一份实战步骤，29块，今天给你。" 这是收入决定日。
3. **收集第一条用户 testimonial**: 无论付款与否，找一位深度互动用户问"最近我分享的内容里，哪一条对你最有用？" 截图保存到 `reports/testimonials/raw_001.md`，用于未来销售页。

---

## 8. Weekly Review Checklist

Every Monday at 09:00 UTC:
- [ ] 汇总微信/支付宝收款记录，核对 `metrics/experiment_tracker.csv`
- [ ] 拉取小红书/知乎/即刻后台数据：曝光、阅读、互动、新增关注
- [ ] 统计新增微信联系人、报价次数、成交次数、拒绝原因（如果有）
- [ ] 更新此 dashboard 实际值
- [ ] 对比 `metrics/experiment_tracker.csv` 一致性
- [ ] 识别本周最佳内容（最高互动/最高引流微信）
- [ ] 识别本周最差内容（低于100曝光）
- [ ] 调整下周内容日历基于数据
- [ ] 更新 `docs/revenue_experiment_7d.md` 如果实验进行中
- [ ] 输出 `reports/weekly_kpi_summary_YYYY-MM-DD.md`
- [ ] 复盘本周 3 件赚钱动作完成率，写入下周计划

---

## 9. Alert Escalation Matrix

| Alert Condition | Severity | Notify | Response Time | Action |
|-----------------|----------|--------|---------------|--------|
| 3天收入为0且新增微信<5 | P1 | dev-optimizer, dev-architect | 4 hrs | 立即更换内容话题；review是否过于技术 |
| 微信被举报/限流/封号 | P0 | dev-optimizer, dev-security | 1 hr | 切备用微信号；暂停群发；review话术 |
| 小红书账号被封 | P1 | dev-optimizer, dev-architect | 2 hrs | 切知乎/即刻；注册新号(不同手机号) |
| 用户投诉"诈骗/诱导付费" | P0 | dev-optimizer, dev-security | 1 hr | 停止收款；确认有实际交付；review offer话术 |
| 收款码被冻结 | P1 | dev-optimizer | 2 hrs | 切换另一平台收款码(微信↔支付宝)；联系客服 |
| 某平台内容进热榜/大量曝光 | P0 | All hands | Immediate | 立刻置顶"加微信"CTA；加大DM力度；准备收款 |
| 日耗时长 > 3 hrs | P2 | dev-optimizer | 24 hrs | 简化内容形式(纯文字→截图)；减少DM数量 |
| 连续2天无内容发布 | P1 | dev-optimizer | 4 hrs | 启用储备内容；或发简单朋友圈/即刻短内容 |
| 支付截图未保存/丢失 | P2 | dev-optimizer | 4 hrs | 从微信/支付宝账单补录；建立自动截图习惯 |

---

## 10. Data Sources & Access

| Source | URL / Location | Access Method | Update Frequency |
|--------|---------------|---------------|------------------|
| 微信收款记录 | 微信 → 我 → 服务 → 钱包 → 账单 | 手机 | Daily |
| 支付宝收款记录 | 支付宝 → 我的 → 账单 | 手机 | Daily |
| 小红书创作者中心 | creator.xiaohongshu.com | 手机号登录 | Daily |
| 知乎创作者中心 | zhihu.com/creator | 登录 | Daily |
| 即刻后台 | jike.city APP | APP | Daily |
| Gumroad (if active) | gumroad.com/dashboard | 登录 | Daily |
| Twitter Analytics | analytics.twitter.com | 登录 | Daily |
| LinkedIn Analytics | linkedin.com/analytics | 登录 | Weekly |
| Experiment Tracker | `metrics/experiment_tracker.csv` | Git / local file | Daily |
| KPI Dashboard | `docs/kpi_dashboard.md` | Git / local file | Daily |
| Daily Auto Report | `reports/daily/DAILY_REPORT_*.md` | `python scripts/daily_metrics_update.py` | Daily |

---

**Next Review**: 2026-05-31  
**Owner**: dev-optimizer (profitability-analyst)  
**Backup Owner**: dev-architect
