# 7-Day Revenue Experiment: AI Architecture Weekly

**Project ID**: knowledge-subscription  
**Task ID**: 96cae9d2  
**Experiment Start Date**: 2026-05-21  
**Experiment End Date**: 2026-05-28  
**Owner**: dev-optimizer (profitability-analyst)  
**Status**: ACTIVE

---

## 1. Experiment Hypothesis

> **H0**: Publishing 1 high-signal ADR-format issue per day + targeted Twitter/LinkedIn distribution for 7 days will generate >= 50 free subscribers and >= 3 paid conversions on Substack.

**Why 7 days**: Short enough to limit burnout, long enough to measure content-market fit signals (open rates, click-through, direct replies, conversion).

---

## 2. Daily Content Publishing Rhythm + Money-Making Actions

Content只是获客手段，**主动推广才是赚钱动作**。每日必须同时执行"内容发布"和"主动获客"两条线。

### Tier A: 英文市场 (Substack + Stripe)

|| Day | Date | Content | Distribution Channels | Free Sub Goal | Paid Conv Goal | Money Action (MUST DO) |
|-----|------|---------|----------------------|---------------|----------------|------------------------|
|| 1 | 2026-05-21 | Pilot Issue #1 repost: "Long Context vs RAG" | Substack, Twitter thread, LinkedIn | 10 | 0 | 发 Twitter thread (3-5 tweets); 在 2 个 Discord 社区分享链接 |
|| 2 | 2026-05-22 | Pilot Issue #2: "Cursor Architecture Teardown" | Substack, Twitter, HN "Show HN" | 15 | 0 | HN Show HN 发帖; LinkedIn 长文; 私信 3 位 KOL 请求互推 |
|| 3 | 2026-05-23 | Deep-dive: "3 Production Mistakes Using Long Context" | Twitter thread, LinkedIn, Substack Note | 5 | 0 | 知乎回答引流; Reddit r/MachineLearning 分享; 小红书技术笔记 |
|| 4 | 2026-05-24 | Pilot Issue #3: "Test-Time Compute Product Guide" | Substack, Twitter | 10 | 0 | Twitter Spaces 或直播预告; 在 indiehackers.com 发布进展 |
|| 5 | 2026-05-25 | Founding-member offer email | Email, Twitter pinned, LinkedIn | 5 | 2 | **转化冲刺**: 限时 founding-member 邮件; 私信高互动免费用户 |
|| 6 | 2026-05-26 | Behind-the-scenes: "How We Write ADRs" | Substack Note, Twitter, LinkedIn | 5 | 1 | 回复所有评论/DM; 在 3 个微信群/QQ群分享试读 |
|| 7 | 2026-05-27 | Week 1 retrospective + paywall tease | Substack, Twitter, LinkedIn | 5 | 1 | 发布转化数据截图(社交证明); 启动 referral program 预告 |
|| 8 | 2026-05-28 | REST DAY — data review only | — | — | — | 写 retrospective; 更新 kpi_dashboard; 规划 Week 2 |

### Tier B: 中文市场 (小报童 / 知识星球 / 微信)

中文市场是独立赛道，同步执行：

|| Day | Date | 中文内容 | 渠道 | 动作 |
|-----|------|---------|------|------|
|| 1-7 | 每日 | 将当日英文 Issue 翻译/改写为 1500 字中文版 | 公众号/小红书/知乎/即刻 | 每篇底部放小报童订阅二维码 |
|| 1-7 | 每日 | 在 3-5 个目标微信群分享"今日 AI 架构洞察" | 微信社群 | 不直接发广告，发价值摘要+"完整版在小报童" |
|| 5 | 2026-05-25 | 早鸟价截止倒计时 | 朋友圈/社群 | ¥29/月早鸟价，限前 50 人 |

### Publishing & Promotion Checklist (per day)
- [ ] 06:00 UTC — 检查昨日 metrics/experiment_tracker.csv 是否已填
- [ ] 07:00 UTC — Draft finalized, anti-AI-slop checklist passed
- [ ] 08:00 UTC — Published on Substack
- [ ] 09:00 UTC — Twitter thread drafted (3-5 tweets, 1 diagram)
- [ ] 10:00 UTC — LinkedIn post published (long-form summary)
- [ ] 11:00 UTC — 中文内容发布（公众号/小红书/知乎，选其一）
- [ ] 12:00 UTC — 在 3 个目标社群分享免费试读（英文+中文各至少1个社群）
- [ ] 18:00 UTC — Engagement check: reply to ALL comments/DMs/知乎回答评论
- [ ] 20:00 UTC — 微信社群互动：回答一个问题，分享一个见解
- [ ] 21:00 UTC — Metric snapshot logged to experiment_tracker.csv
- [ ] 21:30 UTC — 运行 `python scripts/daily_metrics_update.py` 生成日报

---

## 3. Conversion Funnel (7-Day)

```
Impression (Twitter/LinkedIn/HN)
    |
    v
Click → Substack free issue page
    |
    v
Read time > 2 min (measured via Substack analytics)
    |
    v
Free subscription (email capture)
    |
    v
Receive Day 5 founding-member email
    |
    v
Click offer link → Stripe checkout
    |
    v
Paid conversion ($99/yr founding member OR $15/mo Pro)
```

### Funnel Targets (7 days)
| Stage | Target | Current | Source |
|-------|--------|---------|--------|
| Impressions | 3,000 | — | Twitter/LinkedIn analytics + Substack referrer |
| Free subscribers | 50 | — | Substack subscriber count |
| Email open rate (Day 5) | >= 50% | — | Substack email stats |
| Click-through rate (offer) | >= 5% | — | Substack link tracking |
| Paid conversions | >= 3 | — | Stripe dashboard |
| Revenue | >= $297 | — | Stripe |

---

## 4. Revenue Tracking + 双轨收款方案

### 4A: 英文市场收款 (Substack + Stripe)

|| Tier | Price | Notes | Platform |
|------|-------|-------|----------|
| Founding Member | $99/yr | First 100 only; experiment primary offer | Stripe via Substack |
| Pro Monthly | $15/mo | Fallback for price-sensitive | Stripe via Substack |
| Pro Annual | $150/yr | Standard annual | Stripe via Substack |
| Team / Advisory | $499/yr/seat | B2B inbound only | Stripe invoice |

**Stripe 收款前置条件**:
- [ ] Stripe 账户 KYC 完成（个人或公司身份验证）
- [ ] 绑定银行账户（美国 ACH / 香港账户 / Payoneer）
- [ ] Substack paid tier 已启用并关联 Stripe
- [ ] 测试支付流程通过（用 Stripe test card: 4242 4242 4242 4242）
- [ ]  payout 最低限额和手续费确认（通常 2.9% + $0.30 / tx）

### 4B: 中文市场收款 (小报童 / 知识星球 / 微信收款码)

中文市场必须独立处理，Stripe 无法直接收人民币。

|| Tier | Price | Notes | Platform | 开通状态 |
|------|-------|-------|----------|----------|
| 早鸟版 | ¥29/月 | 前 50 人，验证付费意愿 | 小报童 (xiaobot.net) | 待开通 |
| 专业版 | ¥99/月 | 含每日简报 + 脚本模板 + 社群 | 小报童 + 知识星球 | 待开通 |
| 定制版 | ¥499/次 | 按领域出一份机会雷达报告 | 微信/支付宝个人收款码 | 可用 |
| 企业内训 | ¥3,999/次 | 线上 1h 分享 + Q&A | 微信/对公转账 | 可用 |

**小报童开通 checklist**:
- [ ] 注册 xiaobot.net，绑定微信公众号
- [ ] 设置专栏名称: "AI架构周刊" 或 "AI赚钱雷达"
- [ ] 定价设置: 早鸟 ¥29/月，正式 ¥99/月，年度 ¥899/年
- [ ] 上传试读内容（至少 3 篇免费预览）
- [ ] 生成收款二维码，嵌入公众号自动回复
- [ ] 测试从下单 → 支付 → 收到订阅内容 全流程

**知识星球开通 checklist**:
- [ ] 注册 zsxq.com，创建付费星球
- [ ] 定价: ¥99/年（低价年费，降低决策门槛）
- [ ] 设置 3 条免费内容作为诱饵
- [ ] 每日同步 Substack 中文内容到星球
- [ ] 星球专属福利: 每周五直播答疑（承诺，未兑现前不宣传）

**微信/支付宝个人收款（过渡方案）**:
- [ ] 个人微信收款码保存到手机
- [ ] 支付宝收款码保存到手机
- [ ] 定制版/企业内训用个人收款 + 手动发报告
- [ ] 注意: 年收入超 ¥120k 需考虑税务合规; 现阶段优先验证需求

### Revenue Target Breakdown (7-Day Combined)
- 英文: 3 founding members @ $99 = $297 (≈ ¥2,138)
- 中文: 5 早鸟 @ ¥29 = ¥145; 2 专业版 @ ¥99 = ¥198; 1 定制 @ ¥499 = ¥499
- **7天合并目标**: $297 + ¥842 = 约 ¥3,000 或 $415
- Stretch: 英文 5 founding + 中文 10 早鸟 + 3 专业 = ~$500 + ¥1,000 = ~¥4,600

### Cost During Experiment
|| Item | Cost | Notes |
|------|------|-------|
| Substack Pro | $0 | Free tier for now |
| Stripe fees | ~5.4% + $0.30/tx | Deducted at payout |
| 小报童手续费 | ~5% | 平台抽成 |
| 知识星球手续费 | ~20% | 平台抽成较高，但获客能力强 |
| 内容机会成本 | ~$150/day | 3-4 hrs/issue @ $50/hr |
| **Total 7-day cost** | **~$1,050 + ¥0** | Time + platform |
| **Break-even revenue** | **$1,050 / ¥7,560** | 需英文 ~11 founding 或 中文 26 个专业版 |

> **Note**: 7天实验不以盈亏为成功标准。目标是: (1) 验证英文+中文双轨付费意愿 (2) 测出 CAC 和转化率 (3) 收集 3+ 条用户 testimonial。

---

## 5. Stop / Accelerate / Pivot 标准

### 🛑 STOP (Kill the Experiment)
|| Trigger | Threshold | Action |
|---------|-----------|--------|
|| 英文+中文 免费订阅合计 < 10 after Day 3 | < 10 total | 暂停内容; 全面转向免费增长 30 天; 尝试抖音/视频号短视频引流 |
|| 零付费转化 after Day 7 (双轨合计) | 0 paid | 不启用 paywall; 免费增粉至 500 再试转化 |
|| 负面互动信号 | > 20% 退订/取关率 | 调查内容质量; 暂停付费 push |
|| 平台风险 | 公众号/Substack/Stripe 被封 | 立即切备用渠道 (Beehiiv + 个人微信) |
|| 中文社群引流被封 | 微信封号或限流 | 转小红书/即刻/抖音私域 |

### 🚀 ACCELERATE (Double Down)
|| Trigger | Threshold | Action |
|---------|-----------|--------|
|| 付费转化率 > 5% (任一市场) | >=3 paid from <=60 free | Day 8 启用 paywall; 增加发布至 2 期/周 |
|| 有机增长 > 15 free subs/day | >=15/day avg | 启动 referral program; 加大 Twitter/小红书频率 |
|| HN / 知乎热榜 | 任一内容进前 10 | 立即追稿;  landing page 加邮件捕获; 全渠道转载 |
|| Team / 企业内训询盘 | >=1 inquiry | 出 Team tier 报价单; 安排 15min  discovery call |
|| 小报童/知识星球自然搜索来访 | >30% 流量来自搜索 | 优化 SEO 标题; 增加长尾关键词覆盖 |

### ⏸️ HOLD (Continue Monitoring)
|| Trigger | Threshold | Action |
|---------|-----------|--------|
|| 1-2 付费转化, 免费增长 5-10/day | 混合信号 | 续跑 7 天; A/B 测试标题/价格锚点 |
|| 高开信率, 低点击 | >50% open, <2% CTR | 重写 CTA; 测试价格锚点 (¥29 vs ¥99 vs ¥199) |

---

## 6. Daily Metric Logging Protocol

At 21:00 UTC each day, update `metrics/experiment_tracker.csv` with:
- Date
- Content published (title + channel)
- Impressions (Twitter + LinkedIn + Substack referrer)
- Free subscribers gained (net)
- Email open rate (if email sent)
- Email CTR (if email sent)
- Paid conversions (new)
- Revenue (cumulative)
- Notes (qualitative: replies, DMs, HN comments)

---

## 7. Expected Outputs by Day 7

1. `metrics/experiment_tracker.csv` — 7 rows of daily data
2. `reports/revenue_experiment_7d_retrospective.md` — Go/No-Go/Pivot verdict for Month 2
3. Updated `docs/kpi_dashboard.md` with actual vs. projected
4. 7 published content pieces live on Substack/Twitter/LinkedIn

---

## 8. Actual Execution Status (Updated 2026-05-23)

### Day-by-Day Reality

| Day | Date | Planned | Actual | Free Subs | Paid | Revenue | Blocker |
|-----|------|---------|--------|-----------|------|---------|---------|
| 1 | 2026-05-21 | Publish Issue #1 + distribute | Content drafted; no live URL | 0 | 0 | $0 | `BLOCKED_BY_USER`: Cloudflare auth missing |
| 2 | 2026-05-22 | Publish Issue #2 + HN Show HN | Distribution attempted but funnel broken | 0 | 0 | $0 | `BLOCKED_BY_USER`: Payment channel not configured |
| 3 | 2026-05-23 | Deep-dive thread + STOP gate check | STOP gate triggered | 0 | 0 | $0 | `BLOCKED_BY_USER`: sales page still offline |
| 4 | 2026-05-24 | Pilot Issue #3 | **ON HOLD** | — | — | — | Wait for deployment unblock |
| 5 | 2026-05-25 | Founding-member offer | **ON HOLD** | — | — | — | Need >=10 free subs first |

### STOP Gate Triggered (Day 3)

**Condition**: Free subs < 10 after Day 3  
**Actual**: 0 free subs  
**Threshold**: < 10  
**Result**: 🛑 **STOP**

**Immediate Actions Taken**:
1. Halted all new content spend (Day 4-7 content moved to ON HOLD)
2. Updated `metrics/experiment_tracker.csv` with blocker annotations
3. Generated `reports/daily/DAILY_REPORT_2026-05-23.md` documenting zero-revenue state
4. Escalated to user: see `docs/deployment_blockers.md` for unblock checklist

### Root Cause

The experiment assumes a live landing page + payment capture. Neither exists because:
- Cloudflare Pages deployment requires user API Token or `wrangler login`
- 小报童 (or Stripe) payment channel requires user registration and column creation
- `site/index.html` still contains placeholder WeChat ID (`AI-Radar-2026`) and email (`contact@ai-radar.dev`)

Without these, the conversion funnel is physically broken. Content published without a capture mechanism is wasted effort.

### Unblock Path (Must Complete Before Experiment Resumes)

| Step | Action | Owner | ETA |
|------|--------|-------|-----|
| 1 | Register Cloudflare account, create API Token with Pages:Edit permission | User | 10 min |
| 2 | Set `CLOUDFLARE_API_TOKEN` and run `./deploy/deploy.sh production` | User + dev-deploy | 5 min |
| 3 | Register 小报童 (xiaobot.net), create column, set price ¥29/mo | User | 15 min |
| 4 | Replace placeholder WeChat/email/payment links in `site/index.html` | User | 3 min |
| 5 | Re-deploy with real links; verify HTTP 200 + payment links | dev-deploy | 5 min |
| 6 | Restart experiment from Day 1 with live funnel | dev-optimizer | Immediate |

### Financial Impact of Block

| Item | Value |
|------|-------|
| Revenue lost (Day 1-3) | $0 / ¥0 (no funnel = no capture) |
| Content opportunity cost | ~$450 (3 days × $50/hr × 3 hrs) |
| Risk | If unresolved by Day 5, entire Week 1 experiment is invalidated |

---

## 9. Pivot Recommendation

If user cannot complete unblock steps within 48 hours (by 2026-05-25):

1. **Pivot from "Substack-first" to "小报童-first"**: Skip Cloudflare/Substack for now; register 小报童 and start capturing paid subs directly via WeChat ecosystem.
2. **Use personal WeChat收款码 as MVP payment**: Replace complex checkout with simple QR code for ¥29/¥99 manual transactions. Zero platform integration required.
3. **Content channel shifts to 小红书/即刻/知乎**: These do not require a custom landing page; bio link can point to 小报童 or 微信私域.

This pivot preserves the revenue goal while removing the deployment dependency.

---

**Experiment Owner**: dev-optimizer  
**Review Gate**: 2026-05-28 21:00 UTC  
**Next Action if GO**: Scale to 30-day validation plan (see `docs/30_day_validation_plan.md`)  
**Next Action if STOP (current)**: Unblock deployment per `docs/deployment_blockers.md` or pivot to WeChat-native MVP
