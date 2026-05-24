# Substack 原生付费订阅方案 (知识变现项目)

**更新时间**: 2026-05-11  
**项目ID**: knowledge-subscription  
**状态**: 待账号验证 — 必须完成 Substack/Stripe 账号可用性确认后方可执行

---

## 1. 核心方案定位

### 1.1 平台选择
- **主平台**: Substack (发布 + 订阅 + 付费墙 + 邮件触达)
- **支付底层**: Stripe Connect (处理订阅、账单、创作者提现)
- **获客渠道**: 即刻、知乎、V2EX、微信私域 (仅导流，不处理交易)

### 1.2 费用结构 (已核实)
| 费用项 | 比例 | 说明 |
|--------|------|------|
| Substack 平台费 | **10%** | 仅对付费订阅收入抽取 |
| Stripe 处理费 | **~2.9% + $0.30/笔** | 信用卡处理费用 |
| **创作者实收** | **~87%** | 扣除上述费用后的净收入 |

> 来源: Substack Help Center + Stripe Official Documentation

---

## 2. 账号与支付前置条件

### 2.1 Substack Publication 创建
**必须提供的字段**:
- Publication name (建议: AI Money Brief / AI变现情报)
- Subdomain (如: aimoneybrief.substack.com)
- Tagline (一句话描述)
- About page (详细说明)
- Logo/封面图

**验证命令**:
```bash
# 检查 Publication URL 是否可访问
curl -s -o /dev/null -w "%{http_code}" https://[your-pub].substack.com
# 应返回 200
```

### 2.2 Stripe Connect Onboarding (关键阻塞点)
**必须完成**:
1. 身份验证 (政府签发身份证件)
2. 银行账户验证 (必须在 Stripe 支持的 44 个国家/地区)
3. 税务信息 (美国: W-9, 国际: W-8BEN)

**Stripe 支持的国家/地区 (44个)**:
```
AE(阿联酋) AT(奥地利) AU(澳大利亚) BE(比利时) BG(保加利亚) BR(巴西) 
CA(加拿大) CH(瑞士) CY(塞浦路斯) CZ(捷克) DE(德国) DK(丹麦) 
EE(爱沙尼亚) ES(西班牙) FI(芬兰) FR(法国) GB(英国) GI(直布罗陀) 
GR(希腊) HK(香港) HR(克罗地亚) HU(匈牙利) IE(爱尔兰) IT(意大利) 
JP(日本) LI(列支敦士登) LT(立陶宛) LU(卢森堡) LV(拉脱维亚) 
MT(马耳他) MX(墨西哥) MY(马来西亚) NL(荷兰) NO(挪威) NZ(新西兰) 
PL(波兰) PT(葡萄牙) RO(罗马尼亚) SE(瑞典) SG(新加坡) SI(斯洛文尼亚) 
SK(斯洛伐克) TH(泰国) US(美国)
```

> **重要**: 中国大陆大陆地区目前**不在** Stripe 直接支持列表中。若创作者位于中国大陆，需要:
> - 香港/新加坡/美国等地区的银行账户
> - 对应地区的身份验证文件

**验证命令**:
```bash
# 检查 Stripe 是否支持特定国家
curl -s "https://dashboard.stripe.com/register?country=CN" | grep -i "not supported\|currently available"
# 若返回限制信息，则该国家不支持
```

---

## 3. 订阅层级设计

### 3.1 免费层 (Free)
**目的**: 获客和建立信任
- 每周 1 篇免费公开文章
- 每篇展示: 1个机会摘要 + 1个工具推荐 + 1个可执行步骤
- 文末引导升级付费订阅

**Substack 设置**:
- Post type: Public
- Enable email capture
- Use teaser / paywall to guide to paid

### 3.2 付费层 (Paid)
**目的**: 核心收入
- 每周 2-3 篇付费文章
- 内容包含: 机会描述、需求证据、竞品分析、变现路径、执行SOP、风险点
- 每周 1 份 "本周可执行清单"
- 每月 1 份深度报告

**推荐定价**:
| 层级 | 月付 | 年付 | 备注 |
|------|------|------|------|
| 入门版 | $5/月 | $50/年 | 降低支付阻力，验证付费意愿 |
| 标准版 | $9/月 | $90/年 | 覆盖平台费后仍有足够毛利 |
| 高阶支持者 | - | $99-$149/年 | 测试强需求用户，非主要收入 |

**年付折扣建议**: 15%-25% (提高现金流)

### 3.3 收入估算
| 付费用户数 | 月总收入 | 扣除 10% 平台费 | 扣除 Stripe 费后(约) |
|------------|----------|-----------------|---------------------|
| 10 x $9/月 | $90 | $81 | ~$78 |
| 50 x $9/月 | $450 | $405 | ~$391 |
| 100 x $9/月 | $900 | $810 | ~$783 |

---

## 4. 内容交付形态

### 4.1 Substack 原生功能使用
| 功能 | 用途 |
|------|------|
| Public posts | 免费内容，获客 |
| Paid-only posts | 付费内容，收入核心 |
| Paywall / Teaser | 免费文章中展示付费内容预览 |
| Welcome email | 新订阅者欢迎邮件，包含升级引导 |
| Email capture | 收集免费用户邮箱 |
| Thread discussions | 社区互动 |
| Chat | 付费订阅者群组聊天 |

### 4.2 不再需要的 (相比原方案降级)
- ❌ 自建销售页/支付系统
- ❌ 小报童/知识星球作为主要收款
- ❌ 微信/支付宝人工转账 (仅作 Stripe 不可用的 fallback)
- ❌ 小红书自动发布 (封号风险，不作为 P0)

---

## 5. 执行时间表

### Day 0: 账号验证 (阻塞点检查)
```bash
# 检查清单 — 必须全部通过才能进入 Day 1

echo "=== Substack 账号检查 ==="
# 1. 确认 publication URL 可访问
curl -s -o /dev/null -w "HTTP Status: %{http_code}\n" https://[your-pub].substack.com

# 2. 确认 Stripe 连接状态
echo "手动检查: Substack Settings > Payments > Stripe 连接状态"

# 3. 确认 payout 国家/银行可用
echo "手动检查: Stripe Dashboard > Settings > Bank accounts and scheduling"

# 4. 确认税务信息提交
echo "手动检查: Stripe Dashboard > Settings > Tax settings"
```

### Day 1: 内容上线
- [ ] 发布 1 篇免费 launch post
- [ ] 发布 1 篇 paid-only 深度样例
- [ ] 设置 welcome email
- [ ] 配置 subscription tiers 和定价
- [ ] 更新所有外部渠道 bio 指向 Substack URL

### Day 2-7: 获客验证
**P0 渠道**:
- 即刻: 短帖 + Substack 链接
- 知乎: 回答/文章 + Substack 链接
- V2EX/独立开发者社区: 问题导向帖 + Substack 链接
- 微信私域: 只分享免费帖链接，不在微信内主收款

**不主推**:
- 小红书 (封号风险)
- 付费广告 (早期不投入)

---

## 6. 7天验证指标 (Go/No-Go)

### Go (继续)
- 免费订阅 ≥ 50, 且 付费订阅 ≥ 3; 或
- 付费订阅 ≥ 1 且 明确愿付费用户 ≥ 5

### Pivot-Go (调整)
- 免费订阅 ≥ 30, 但付费 < 3
- 调整: 标题、价格、内容定位、发布渠道

### Stop (终止)
- 有足够曝光但免费订阅 < 20
- 无人愿为 paid post 付费

---

## 7. 必须创建的检查清单文件

完成本方案后，必须生成以下文件:
1. `docs/substack_launch_checklist.md` — 详细执行步骤
2. `docs/account_payment_blockers.md` — 账号/支付阻塞点清单

---

## 8. 数据追踪字段

每日记录到 `metrics/experiment_tracker.csv`:
```csv
date,exposure,clicks,content_reads,pricing_views,orders,revenue,new_paid_users,total_paid_users,open_rate,ctr,notes
```

---

## 9. 关键决策记录

| 决策 | 内容 | 时间 |
|------|------|------|
| 平台选择 | Substack 原生付费为主路径 | 2026-05-09 |
| 定价策略 | 美元定价 $5-9/月起测 | 2026-05-09 |
| 获客策略 | 外部渠道仅导流，不处理交易 | 2026-05-09 |
| 账号要求 | 必须完成 Stripe KYC 才能启动 | 2026-05-11 |

---

## 10. 下一步行动

1. [ ] 用户确认 Substack publication 创建状态
2. [ ] 用户确认 Stripe onboarding 状态
3. [ ] 若 Stripe 不可用，记录替代方案决策
4. [ ] 执行 Day 0 账号验证
5. [ ] 进入 Day 1 内容发布

---

**验证命令汇总**:
```bash
# 1. 检查 Stripe 全球支持状态
curl -s "https://stripe.com/global" | grep -oP 'country=[A-Z]{2}' | sort -u

# 2. 检查 Substack 域名可用性
curl -s "https://substack.com" | head -1

# 3. 检查特定 publication (替换 [pub-name])
curl -s -o /dev/null -w "%{http_code}" https://[pub-name].substack.com
```
