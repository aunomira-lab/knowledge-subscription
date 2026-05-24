# Substack 原生付费订阅 - 启动执行清单

**更新时间**: 2026-05-11  
**对应方案**: docs/substack_native_plan.md  
**状态**: 待账号验证完成

---

## 0. 执行前必须确认

> ⚠️ **重要**: 以下 4 项必须全部通过才能进入执行阶段

| # | 检查项 | 状态 | 验证命令/方法 |
|---|--------|------|---------------|
| 1 | Substack publication 可创建 | ⬜ | 访问 substack.com 登录创建 |
| 2 | Paid subscription 功能可开启 | ⬜ | Settings > Monetization > Enable paid |
| 3 | Stripe onboarding 可完成 | ⬜ | 见下方 Stripe 检查清单 |
| 4 | 至少 1 名目标用户可完成支付测试 | ⬜ | 邀请测试用户订阅 |

---

## 1. 用户必须提供的信息

### 1.1 Substack 账号信息
```yaml
substack_account:
  email: "_______"  # Substack 登录邮箱
  publication_name: "_______"  # 如: AI Money Brief
  publication_url: "_______"  # 如: https://aimoneybrief.substack.com
  subdomain: "_______"  # 如: aimoneybrief
```

### 1.2 Stripe 连接状态
```yaml
stripe_status:
  onboarding_status: "_______"  # not_started / in_progress / verified / blocked
  payout_country: "_______"  # 如: US, HK, SG
  bank_account_added: "_______"  # yes / no
  tax_info_submitted: "_______"  # yes / no
  first_payout_estimated: "_______"  # 日期或 unknown
```

### 1.3 定价确认
```yaml
pricing:
  monthly: "_______"  # $5 或 $9
  annual: "_______"  # $50 或 $90
  founding_member: "_______"  # $99 或 $149
  currency: "USD"  # 确认接受美元定价
```

---

## 2. Substack 后台配置清单

### 2.1 Publication 基础设置
- [ ] **Name**: AI Money Brief (或用户指定的中文名)
- [ ] **Tagline**: 每周筛选、验证、拆解可执行的 AI 变现机会
- [ ] **About page**: 说明核心价值主张 (不是泛泛 AI 新闻，而是机会筛选+验证+执行)
- [ ] **Logo**: 上传方形 logo (建议 256x256px)
- [ ] **Cover image**: 上传封面图 (建议 1200x400px)
- [ ] **Custom domain** (可选): 如有域名，配置 CNAME

**验证命令**:
```bash
# 检查 publication 主页可访问
curl -s -o /dev/null -w "%{http_code}" https://[your-pub].substack.com
# 期望输出: 200

# 检查 RSS 可用
curl -s -o /dev/null -w "%{http_code}" https://[your-pub].substack.com/feed
# 期望输出: 200
```

### 2.2 Paid Subscription 设置
路径: Settings > Monetization > Paid subscriptions

- [ ] **Enable paid subscriptions**: 开启
- [ ] **Monthly price**: 设置 (如 $9)
- [ ] **Annual price**: 设置 (如 $90, 比月付便宜15-25%)
- [ ] **Founding member price**: 设置 (如 $149/年)
- [ ] **Trial period** (可选): 7天免费试用
- [ ] **Connect Stripe account**: 完成连接

### 2.3 Stripe Onboarding 详细步骤

#### 步骤 1: 启动连接
```
Substack Settings > Monetization > Connect with Stripe
```

#### 步骤 2: Stripe Connect 验证清单
必须提供:
- [ ] 政府签发身份证件 (护照/身份证/驾照)
- [ ] 出生日期
- [ ] 居住地址证明 (部分国家需要)
- [ ] 银行账户信息 (必须位于 Stripe 支持的 44 个国家)
- [ ] 税务信息:
  - 美国公民/居民: W-9 表格
  - 非美国居民: W-8BEN 表格

#### 步骤 3: 支持的银行国家验证
```bash
# 检查创作者所在国家是否在支持列表
curl -s "https://stripe.com/global" | grep -oP 'country=[A-Z]{2}' | sed 's/country=//' | sort -u > /tmp/stripe_countries.txt

# 检查特定国家 (如中国 CN)
if grep -q "^CN$" /tmp/stripe_countries.txt; then
    echo "✅ CN supported"
else
    echo "❌ CN not directly supported - need alternative"
fi
```

**当前支持的国家代码** (44个):
```
AE AT AU BE BG BR CA CH CY CZ DE DK EE ES FI FR GB GI GR HK HR HU IE IT JP LI LT LU LV MT MX MY NL NO NZ PL PT RO SE SG SI SK TH US
```

> **重要**: 中国大陆大陆 (CN) 不在直接支持列表。解决方案:
> 1. 香港银行账户 + 香港身份证
> 2. 新加坡银行账户 + 新加坡身份
> 3. 美国银行账户 + ITIN/EIN
> 4. 使用第三方服务商 (如 Mercury, Wise Business)

#### 步骤 4: 完成测试支付
```bash
# 方法: 使用测试卡完成一次 $1 订阅，然后立即取消
# Stripe 测试卡号: 4242 4242 4242 4242
# 任意未来日期 + 任意 3 位 CVC + 任意邮编
```

### 2.4 内容设置

#### Welcome Email
路径: Settings > Emails > Welcome email

必须包含:
- [ ] 感谢订阅
- [ ] 说明免费用户会收到什么 (每周 1 篇免费文章)
- [ ] 付费内容预览/升级理由
- [ ] 1 个 "样例" 链接 (指向一篇付费文章的 teaser)
- [ ] 升级按钮

#### Paywall / Teaser 设置
路径: 发布文章时选择

- [ ] 免费文章末尾添加付费内容预览
- [ ] 设置 "Read more" 按钮指向付费订阅页面
- [ ] 在文章中使用 Substack 原生 paywall 功能

---

## 3. 内容发布计划

### Day 0: 准备 (发布前)
- [ ] 将现有 sample_pack 改写成 1 篇免费 launch post
- [ ] 将 premium 内容改写成 1 篇 paid teaser
- [ ] 从 week1_samples 选 1 篇改成 paid-only deep dive
- [ ] 准备 welcome email 文案
- [ ] 准备 3 个外部渠道导流帖文案

**文件位置要求**:
```
/home/AgentAdmin/.hermes/shared/dev-team/projects/knowledge-subscription/
├── content/
│   ├── launch_post.md (免费发布文章)
│   ├── paid_teaser.md (付费预览)
│   └── paid_deep_dive.md (付费深度内容)
└── docs/
    └── substack_launch_checklist.md (本文件)
```

### Day 1: 上线
- [ ] 发布 1 篇免费 public post
- [ ] 发布 1 篇 paid-only post
- [ ] 配置并启用 welcome email
- [ ] 测试从外部点击到 Substack 的完整流程
- [ ] 更新所有社交渠道 bio 指向 Substack URL

### Day 2-7: 获客导流

#### P0 渠道 (必须执行)
| 渠道 | 动作 | 频次 | 检查命令 |
|------|------|------|----------|
| 即刻 | 短帖 + Substack 链接 | 每天 1-2 条 | 手动检查链接可点击 |
| 知乎 | 回答/文章 + Substack 链接 | 3-5 个回答/周 | 检查链接状态 |
| V2EX | 问题导向帖 + Substack 链接 | 1-2 帖/周 | 检查流量来源 |
| 微信私域 | 分享免费帖链接 | 随内容发布 | 不直接收款 |

#### 不做 (标记为后续可选)
- [ ] 小红书自动发布 (封号风险高)
- [ ] 微信群硬广
- [ ] 自建支付页
- [ ] 付费广告 (验证期不投入)

---

## 4. 7天验证指标

### 每日数据记录
记录到: `metrics/experiment_tracker.csv`

```csv
date,exposure,clicks,content_reads,pricing_views,orders,revenue,new_paid_users,total_paid_users,open_rate,ctr,notes
```

### Go / Pivot / Stop 判断

#### Go (继续推进)
```
免费订阅 >= 50 AND 付费订阅 >= 3
OR
付费订阅 >= 1 AND 明确愿付费用户 >= 5
```

#### Pivot-Go (调整再试)
```
免费订阅 >= 30 AND 付费 < 3
→ 调整: 标题、价格、内容定位、发布渠道
```

#### Stop (终止项目)
```
曝光充足 BUT 免费订阅 < 20 AND 无人愿付费
→ 记录原因，归档项目
```

---

## 5. 旧方案降级说明

| 原方案 | 新定位 | 原因 |
|--------|--------|------|
| site/index.html | 备用中文介绍页 | 不再作为主支付入口 |
| 小报童/知识星球 | 仅当 Stripe 不可用时评估 | Substack 原生优先 |
| 微信/支付宝收款 | Fallback 方案 | 不是主路径 |
| 小红书 | 不作为 P0 | 封号风险 |

---

## 6. 阻塞点升级流程

如果以下任一检查失败，立即 `kanban_block`:

| 阻塞点 | 升级条件 | 需要用户提供 |
|--------|----------|--------------|
| Stripe 国家不支持 | 创作者所在国家不在 44 国列表 | 替代银行账户方案 |
| KYC 失败 | Stripe 身份验证被拒绝 | 其他身份文件 |
| 税务信息问题 | W-9/W-8BEN 提交失败 | 税务顾问协助 |
| 支付测试失败 | 测试用户无法完成订阅 | 支付方式排查 |

---

## 7. 验证命令汇总

```bash
#!/bin/bash
# Substack 启动前验证脚本

PUB_URL="https://[your-pub].substack.com"

echo "=== Substack 启动验证 ==="
echo ""

echo "1. 检查 Publication 可访问性..."
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" "$PUB_URL")
if [ "$HTTP_CODE" = "200" ]; then
    echo "✅ Publication 可访问 (HTTP 200)"
else
    echo "❌ Publication 不可访问 (HTTP $HTTP_CODE)"
fi

echo ""
echo "2. 检查 RSS Feed..."
RSS_CODE=$(curl -s -o /dev/null -w "%{http_code}" "$PUB_URL/feed")
if [ "$RSS_CODE" = "200" ]; then
    echo "✅ RSS Feed 可用"
else
    echo "❌ RSS Feed 不可用 (HTTP $RSS_CODE)"
fi

echo ""
echo "3. Stripe 支持国家列表 (44个)..."
curl -s "https://stripe.com/global" | grep -oP 'country=[A-Z]{2}' | sed 's/country=//' | sort -u | tr '\n' ' '
echo ""

echo ""
echo "4. 检查清单..."
echo "⬜ Substack publication 创建完成"
echo "⬜ Paid subscription 功能开启"
echo "⬜ Stripe Connect 完成 onboarding"
echo "⬜ 银行账户验证通过"
echo "⬜ 税务信息提交"
echo "⬜ 测试支付完成"
echo "⬜ Welcome email 配置"
echo "⬜ Launch post 准备"
echo "⬜ Paid content 准备"
```

---

## 8. 完成确认

当所有检查项完成后，更新本文件状态:

```yaml
status: COMPLETED
completed_at: "2026-XX-XX"
verified_by: "_______"
next_action: "Day 1 内容发布"
```

然后执行: `kanban_complete` 标记本任务完成。
