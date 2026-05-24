# Support SOP: AI Architecture Weekly

**Project ID**: knowledge-subscription  
**Task ID**: ab047a39  
**Type**: monitoring (ops-support)  
**Last Updated**: 2026-05-24  
**Owner**: dev-optimizer (profitability-analyst)

---

## 1. Purpose

This document defines the standard operating procedures for day-to-day customer support, content operations, and revenue monitoring for the AI Architecture Weekly newsletter. It is the first-line reference for any team member handling support or operational issues.

---

## 2. Support Channels & Ownership

### 英文市场渠道

|| Channel | Access | Primary Owner | Backup Owner | Response SLA |
|---------|--------|---------------|--------------|--------------|
|| Substack comments | substack.com/manage | dev-optimizer | dev-architect | 24 hrs |
|| Substack email replies | substack.com/manage | dev-optimizer | dev-architect | 24 hrs |
|| Twitter/X DMs | twitter.com/messages | dev-optimizer | dev-architect | 48 hrs |
|| LinkedIn messages | linkedin.com/messaging | dev-optimizer | dev-architect | 48 hrs |
|| Hacker News replies | news.ycombinator.com | dev-optimizer | dev-architect | 24 hrs (top-level only) |
|| GitHub Issues (code examples) | github.com repo | dev-coder | dev-tester | 72 hrs |
|| Discord (future, paid members) | Discord server | dev-optimizer | dev-architect | 4 hrs |
|| Stripe customer portal | dashboard.stripe.com | dev-optimizer | dev-deploy | 24 hrs |

### 中文市场渠道

|| Channel | Access | Primary Owner | Backup Owner | Response SLA |
|---------|--------|---------------|--------------|--------------|
|| 小报童留言/私信 | xiaobot.net 后台 | dev-optimizer | dev-architect | 12 hrs |
|| 知识星球问答 | zsxq.com 后台 | dev-optimizer | dev-architect | 12 hrs |
|| 微信公众号留言 | mp.weixin.qq.com | dev-optimizer | dev-architect | 24 hrs |
|| 小红书私信/评论 | 小红书 APP | dev-optimizer | dev-architect | 24 hrs |
|| 知乎私信/评论 | zhihu.com | dev-optimizer | dev-architect | 24 hrs |
|| 即刻私信/评论 | jike.city APP | dev-optimizer | dev-architect | 24 hrs |
|| 微信个人号 (私域) | 微信 APP | dev-optimizer | dev-architect | 4 hrs (工作日) |
|| 微信社群 @ 提问 | 微信群 | dev-optimizer | dev-architect | 4 hrs (工作日) |
|| 支付宝/微信收款问题 | 手机收款记录 | dev-optimizer | dev-deploy | 24 hrs |

### 紧急升级通道

|| Situation | Escalate To | Method | Response Expected |
|-----------|-------------|--------|-------------------|
|| Emergency escalation | Email team alias | dev-architect | dev-deploy | 4 hrs |

---

## 3. Daily Operations Checklist

### 07:00 UTC — Morning Prep
- [ ] Check Substack dashboard for new subscriber alerts
- [ ] Check Stripe for new payments or failed charges
- [ ] Review overnight Twitter/LinkedIn mentions and DMs
- [ ] Check `metrics/experiment_tracker.csv` — is yesterday's row filled?
- [ ] Review today's publishing schedule against `docs/revenue_experiment_7d.md`

### 08:00 UTC — Publish Window
- [ ] Content published to Substack
- [ ] Anti-AI-slop checklist passed (`docs/anti_ai_slop_checklist.md`)
- [ ] Code examples tested (if applicable)
- [ ] Social distribution scheduled

### 14:00 UTC — Midday Check
- [ ] Substack comments replied to
- [ ] Twitter/LinkedIn engagement responded
- [ ] Any support tickets logged in tracker

### 21:00 UTC — Daily Close
- [ ] Metric snapshot logged to `metrics/experiment_tracker.csv`
- [ ] Support inbox zero
- [ ] Update `docs/kpi_dashboard.md` if needed
- [ ] Flag any P1/P2 alerts per `docs/incident_runbook.md`

---

## 4. Content Quality Gates (Pre-Publish)

Every issue must pass these checks before publishing:

| Gate | Check | Owner | Tool |
|------|-------|-------|------|
| Anti-slop | No generic AI filler; every claim has source | dev-optimizer | `docs/anti_ai_slop_checklist.md` |
| Technical accuracy | Code examples run; benchmarks reproducible | dev-coder | `tests/test_report_generator.py` |
| Links alive | All external links return 200 | dev-tester | `scripts/link_checker.py` (if exists) |
| Visual assets | Diagrams render correctly | dev-optimizer | Browser preview |
| Mobile readable | Substack preview on mobile | dev-optimizer | Phone / browser devtools |
| Pricing consistency | Any price mention matches live tiers | dev-optimizer | Stripe + Substack pricing page |

---

## 5. Subscriber Lifecycle SOP

### New Free Subscriber (EN)
1. Auto-welcome email (Substack native)
2. Day 1: Deliver most popular past issue as "instant value"
3. Day 3: Share Twitter thread with highest engagement
4. Day 5: Founding-member offer (see `docs/revenue_experiment_7d.md`)

### New Free Subscriber (CN — 公众号/小红书)
1. 关注后自动回复: "感谢关注! 回复【试读】获取 3 篇精选 + 小报童订阅二维码"
2. Day 1: 推送最热门的中文改写文章
3. Day 3: 私发一条"AI架构日报"摘要 + 小报童早鸟价提醒
4. Day 5: 朋友圈/社群发布早鸟价倒计时 (限前 50 人)
5. Day 7: 私信高互动用户:"你对哪类内容最感兴趣?" (收集需求 + 建立信任)

### New Paid Subscriber (EN — Stripe)
1. Stripe confirmation email (auto)
2. Manual welcome within 24 hrs: "Thanks for joining — here's your first exclusive template"
3. Add to paid-only content access list
4. Flag for Discord invite (when Discord launches)
5. Log in `metrics/experiment_tracker.csv`

### New Paid Subscriber (CN — 小报童/知识星球)
1. 平台自动确认 (小报童/星球)
2. 24 小时内人工微信私信: "感谢订阅! 这是本期独家模板/脚本下载链接..."
3. 邀请加入微信 VIP 群 (如果已建群)
4. 标记为高价值用户，优先回复其后续问题
5. 记录到 `metrics/experiment_tracker.csv`

### Cancellation / Churn (EN)
1. Stripe sends cancellation notice (auto)
2. Within 24 hrs: Send exit survey (1 question: "What would have kept you subscribed?")
3. Log reason in `metrics/experiment_tracker.csv` notes column
4. If reason = "price", offer 50% off for 3 months as win-back
5. If reason = "content quality", escalate to dev-architect for review
6. If reason = "technical issue", escalate to dev-coder + dev-deploy

### Cancellation / Churn (CN)
1. 小报童/星球自动通知退订
2. 24 小时内私发微信: "看到你已经退订，能告诉我一个原因吗? 哪怕一句话也对我很有帮助。"
3. 记录原因到 experiment_tracker.csv
4. 如果原因 = "价格贵"，提供 50% off 三个月挽留码
5. 如果原因 = "内容不够深/不够实用"，反馈给 dev-architect 调整内容策略
6. 如果月退订率 > 15%，触发 P1 告警，全团队复盘内容方向

### Failed Payment (Stripe dunning)
1. Stripe auto-retries 3x over 7 days
2. After 1st failure: Manual email check-in from founder voice
3. After 3rd failure: Pause access; send re-activation link
4. Log in tracker; if > 5% of paid base failing, investigate Stripe/payout config

### 微信/支付宝个人收款异常
1. 用户反馈"已付款但未收到报告"
2. 核对微信/支付宝收款记录截图
3. 确认金额和备注无误后，手动发送内容/报告
4. 若频繁出现 (月 >3 次)，立即迁移到小报童/知识星球标准化收款
5. 记录到 `metrics/experiment_tracker.csv` 的 notes 列

---

## 6. Revenue Operations SOP

### Daily
- [ ] Check Stripe dashboard: new subscriptions, failed payments, refunds
- [ ] Check 小报童后台: 新增订阅、收入、退订
- [ ] Check 知识星球后台: 新增成员、收入
- [ ] Check 微信/支付宝收款记录: 定制版/企业内训是否有新订单
- [ ] Verify `metrics/experiment_tracker.csv` revenue column matches all platforms combined
- [ ] Check for any payout hold or KYC alert (Stripe / 小报童提现限制)

### Weekly (Monday)
- [ ] Pull MRR report from Stripe
- [ ] Pull 小报童/星球周收入汇总
- [ ] Reconcile Substack subscriber count vs. Stripe paid count
- [ ] 核对中文平台: 公众号新增关注 vs 小报童新增订阅 vs 微信加微人数
- [ ] Update `docs/kpi_dashboard.md` financial section
- [ ] File `reports/weekly_kpi_summary_YYYY-MM-DD.md`
- [ ] 运行 `python scripts/daily_metrics_update.py` 验证日报连续性

### Monthly
- [ ] Calculate LTV and CAC (EN + CN 分开计算)
- [ ] Review churn reasons aggregate (EN + CN)
- [ ] Adjust pricing experiments if needed (A/B test 结果)
- [ ] 小报童/星球提现到账确认
- [ ] Tax/invoice preparation (if applicable; 中文年收入超 ¥120k 需规划税务)
- [ ] 复盘本月 3 件赚钱动作完成率

---

## 7. Tooling & Access Register

|| Tool | Purpose | Owner | Access Method | Backup Access |
||------|---------|-------|---------------|---------------|
|| Substack | Publishing, email list, free subs | dev-optimizer | Login | dev-architect |
|| Stripe | Payments, invoicing, refunds | dev-optimizer | Login | dev-deploy |
|| Twitter/X | Distribution, engagement | dev-optimizer | Login | dev-architect |
|| LinkedIn | Distribution, B2B leads | dev-optimizer | Login | dev-architect |
|| GitHub | Code examples, open source | dev-coder | Login | dev-tester |
|| Vercel/Cloudflare | Landing page hosting | dev-deploy | Login | dev-architect |
|| Discord | Paid community (future) | dev-optimizer | Admin | dev-architect |
|| Google Analytics / Plausible | Web traffic | dev-deploy | Login | dev-optimizer |

---

## 8. Deployment Blocker Response (NEW)

When `docs/deployment_blockers.md` is in BLOCKED_BY_USER state:

### Detection
- `reports/deployment_verification.md` status = BLOCKED_BY_USER
- `wrangler whoami` returns "not authenticated" or `CLOUDFLARE_API_TOKEN` not set
- 销售页 URL returns 404 or connection refused

### Response (dev-optimizer + dev-deploy)
1. **00:00-00:15** — Verify blocker status: check `docs/deployment_blockers.md` for which items are incomplete
2. **00:15-00:30** — Generate or update `reports/deployment_verification.md` with clear unblock steps
3. **00:30-01:00** — Communicate to user the exact steps required (from deployment_blockers.md "用户执行步骤")
4. **01:00-02:00** — If user provides API Token or completes wrangler login, immediately run `./deploy/deploy.sh production`
5. **Post-unblock** — Verify HTTP 200, update all docs with live URL, resume experiment

### DO NOT
- Publish new content while sales page is offline (content without capture = wasted effort)
- Run paid ads while funnel is broken (CAC → infinity)
- Claim "experiment is running" when deployment is blocked

---

## 10. Manual Revenue Operations SOP (Phase 2 — WeChat-native MVP)

Phase 2 does not use Stripe, 小报童, or any automated payment platform. All revenue is captured manually via WeChat/Alipay QR codes.

### 10.1 When a Payment Arrives
1. **Immediately** — Screenshot the payment notification (微信服务通知 / 支付宝到账通知)
2. **Within 5 minutes** — Reply: "收到！马上给你发资料。"
3. **Within 30 minutes** — Deliver the promised product (PDF, 拉群, 发送模板)
4. **Within 1 hour** — Log in `metrics/experiment_tracker.csv` AND save screenshot to `reports/payments/YYYYMMDD_HHMM_amount.png`
5. **Within 24 hours** — Follow-up message: "资料收到了吗？有不懂的直接问我。"

### 10.2 When a User Asks "How do I pay?"
1. Do NOT send QR code in group chat (会被踢/举报)
2. Reply in private chat: "加我微信/已经加了的直接私聊我，我给你发收款方式"
3. In private chat, send QR code image + text: "¥29，确认后马上发你"
4. Wait for payment screenshot from user before delivering

### 10.3 Refund Policy (Manual)
- 用户付款后 24 小时内要求退款：无条件退，退后拉黑不纠缠
- 用户看完内容后要求退款：询问原因，若合理则退 50%；若无理取闹则退全并拉黑
- 所有退款记录到 `metrics/experiment_tracker.csv` 并标注 "refund"

### 10.4 WeChat Group Management
- 付费用户拉入 VIP 小群（< 50 人）
- 群内每天发 1 条独家内容（比公开平台早 24 小时）
- 群规：禁止广告，禁止政治，禁止人身攻击
- 违规 1 次警告，2 次移除不退费

---

## 9. Escalation Rules

|| Situation | Escalate To | Method | Response Expected |
||-----------|-------------|--------|-------------------|
|| Content quality complaint | dev-architect | Substack/email mention | 24 hrs |
|| Code example broken | dev-coder | GitHub issue / email | 48 hrs |
|| Payment system down | dev-deploy | Immediate call / Slack | 2 hrs |
|| Legal / copyright claim | dev-security | Email with evidence | 4 hrs |
|| Platform ban risk (WeChat/Substack/Stripe) | dev-security + dev-architect | Immediate call | 1 hr |
|| Negative viral attention | All hands | Emergency channel | Immediate |
|| Deployment blocker > 48 hrs unresolved | dev-architect + user | Email with pivot options | 4 hrs |

---

**Next Review**: 2026-06-21  
**Version**: 1.1  
**Owner**: dev-optimizer
