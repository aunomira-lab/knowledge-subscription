# Knowledge Subscription 48小时执行计划

**文档版本**: 1.0  
**更新日期**: 2026-05-11  
**执行前提**: launch_decision.md 决策为 CONDITIONAL_PASS  
**关键目标**: 完成所有准备，待Stripe就绪后立即启动

---

## 执行摘要

本计划分为两个24小时阶段：
- **第一个24小时** (Hour 0-24): 账户创建与内容准备
- **第二个24小时** (Hour 24-48): 渠道部署与启动前验证

**成功标准**:
- ✅ Substack免费Publication创建完成
- ✅ 3篇发布就绪内容准备完成
- ✅ P0获客渠道(即刻App)设置完成
- ✅ 用户完成Stripe账户方案选择

---

## 阶段一: 第一个24小时 (Hour 0-24)

### Hour 0-2: 账户创建阶段

**目标**: 创建Substack免费账号

#### 必须提供的信息 (用户)

```yaml
# 填写模板 - 由用户完成
substack_setup:
  email: "__________"  # 必填: 可收验证邮件的邮箱
  publication_name: "AI变现情报"  # 建议填写
  subdomain: "aimoneybrief"  # 建议填写
  tagline: "每周筛选、验证、拆解可执行的AI变现机会"  # 建议填写
  about_page_summary: |
    你是不是每天看到各种"靠AI月入十万"的标题，
    却不知道哪些真的能做，哪些是骗局？
    这里每周筛选出真实可验证的AI变现机会，
    附带具体执行步骤和工具推荐。
    不讲虚的，只讲能落地的。
```

#### 执行步骤

| 步骤 | 动作 | 验证方式 | 预计时间 |
|------|------|----------|----------|
| 1 | 访问 https://substack.com | 验证网站可访问 | 5分钟 |
| 2 | 点击 Sign Up | 使用用户提供的邮箱注册 | 10分钟 |
| 3 | 验证邮箱 | 确认收到验证邮件 | 5分钟 |
| 4 | 创建Publication | 填写上方模板信息 | 15分钟 |
| 5 | 配置About页面 | 粘贴about_page_summary | 20分钟 |
| 6 | 上传Logo(可选) | 使用AI生成或简单设计 | 30分钟 |
| 7 | 测试访问URL | 验证主页可打开 | 5分钟 |

#### 验证命令

```bash
# 测试Publication可访问性
PUB_URL="https://[subdomain].substack.com"
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" "$PUB_URL")
if [ "$HTTP_CODE" = "200" ]; then
    echo "✅ Publication可访问: $PUB_URL"
else
    echo "❌ 访问失败 (HTTP $HTTP_CODE)"
fi

# 测试RSS Feed
RSS_CODE=$(curl -s -o /dev/null -w "%{http_code}" "$PUB_URL/feed")
if [ "$RSS_CODE" = "200" ]; then
    echo "✅ RSS Feed可用"
else
    echo "❌ RSS不可用"
fi
```

#### 完成标志
- [ ] Substack账户创建完成
- [ ] Publication主页可访问
- [ ] About页面内容已填写
- [ ] URL已记录: `https://[subdomain].substack.com`

---

### Hour 2-4: Stripe方案决策阶段

**目标**: 用户确认Stripe账户方案

#### 方案选择流程图

```
用户是否有香港身份/护照?
┌───────────────┐
│  YES         │  NO
│   │           │
│   ▼           │
│ 香港方案A     │
│ ⭐⭐⭐⭐⭐    │
│  (1-2周)     │
│               │
└───────────────┘
                    │
                    ▼
        用户是否有新加坡身份?
        ┌───────────────┐
        │  YES         │  NO
        │   │           │
        │   ▼           │
        │ 新加坡方案B   │
        │ ⭐⭐⭐⭐     │
        │  (1-2周)     │
        │               │
        └───────────────┘
                        │
                        ▼
            使用第三方服务?
            ┌───────────────┐
            │  YES         │  NO
            │   │           │
            │   ▼           │
            │ Mercury方案D │
            │ ⭐⭐⭐⭐    │
            │  (1-3周)     │
            │               │
            └───────────────┘
                            │
                            ▼
                        小报童方案E
                        ⭐⭐⭐
                        (即时)
```

#### 用户必填表格

```yaml
# Stripe账户方案选择
stripe_solution:
  selected_option: "___"  # A/B/D/E 四选一
  
  # 若选择A香港方案
  hk_details:
    has_hk_id: "___"  # yes/no
    id_type: "___"  # 香港身份证/护照/其他
    has_hk_bank: "___"  # yes/no
    bank_name: "___"  # 如有
  
  # 若选择B新加坡方案
  sg_details:
    has_sg_id: "___"  # yes/no
    has_sg_bank: "___"  # yes/no
  
  # 若选择DMercury方案
  mercury_details:
    has_us_company: "___"  # yes/no
    willing_to_register: "___"  # yes/no
  
  # 若选择E小报童方案
  xiaobaotong_details:
    wechat_pay_ready: "___"  # yes/no
    reason_fallback: "___"  # 说明
```

#### 完成标志
- [ ] 用户已确认Stripe方案
- [ ] 已录入上方选择表格
- [ ] 若选择主流方案(A/B/D)：用户已开始账户申请流程
- [ ] 若选择备选方案(E)：已创建小报童账号

---

### Hour 4-12: 内容准备阶段

**目标**: 准备3篇发布就绪内容

#### 内容清单

| 序号 | 内容类型 | 使用文件 | 状态 | 准备工作 |
|------|----------|----------|------|----------|
| 1 | 首篇免费发布 | `first_video_script_cn_public_v3.md` | ✅ 存在 | 改写为文章格式 |
| 2 | 首篇付费预览 | `paid_deep_dive_outline.md` | ✅ 存在 | 扩展为完整文章 |
| 3 | Launch Post | `launch_post_free.md` | ✅ 存在 | 适配Substack格式 |

#### Hour 4-8: 首篇内容准备

**基础文件**: `docs/first_video_script_cn_public_v3.md`

**改写任务**:
1. 将视频脚本改写为阅读文章
2. 添加小标题和段落分隔
3. 添加CTA(Call to Action): 订阅按钮
4. 添加相关链接

**输出位置**: `/home/AgentAdmin/.hermes/shared/dev-team/projects/knowledge-subscription/content/launch_post_ready.md`

**验证检查清单**:
- [ ] 文章字数 > 800字
- [ ] 包含 > 3个小标题
- [ ] 结尾有明确CTA
- [ ] 内容符合合规清单(`content_compliance_checklist.md`)

#### Hour 8-12: 付费内容预览准备

**基础文件**: `docs/paid_deep_dive_outline.md`

**扩展任务**:
1. 根据大纲扩展为完整文章
2. 添加具体案例和数据
3. 添加可执行步骤
4. 设置Paywall截断点(前30%免费，后70%付费)

**输出位置**: `/home/AgentAdmin/.hermes/shared/dev-team/projects/knowledge-subscription/content/paid_teaser_ready.md`

**验证检查清单**:
- [ ] 文章字数 > 2000字
- [ ] 包含 >= 3个具体案例
- [ ] 包含可执行清单
- [ ] 已设计Paywall截断点

#### 验证命令

```bash
# 验证内容完整性
echo "=== 内容准备验证 ==="

# 检查内容文件存在
echo "1. 检查内容文件:"
for file in content/launch_post_ready.md content/paid_teaser_ready.md; do
    if [ -f "$file" ]; then
        echo "   ✅ $file (字数: $(wc -m < $file))"
    else
        echo "   ❌ $file (缺失)"
    fi
done

# 验证合规性
echo ""
echo "2. 内容合规检查:"
echo "   ⬜ 无禁词列表检查 (参见content_compliance_checklist.md)"
echo "   ⬜ 风险提示语句检查"
echo ""
```

---

### Hour 12-24: 渠道准备阶段

**目标**: 设置P0获客渠道(即刻App)

#### 即刻App账号设置

**执行步骤**:

| 步骤 | 动作 | 验证 | 预计时间 |
|------|------|------|----------|
| 1 | 下载即刻App | 安装完成 | 10分钟 |
| 2 | 注册账号 | 使用手机号注册 | 10分钟 |
| 3 | 完善个人资料 | 填写头像、简介 | 15分钟 |
| 4 | 修改个人介绍 | 放入Substack链接 | 10分钟 |
| 5 | 关注目标圈子 | 搜索"独立开发者"、"AI"等 | 30分钟 |
| 6 | 发布首条内容 | 分享价值观点 | 30分钟 |

**个人简介模板**:
```
分享AI变现机会、自动化工具、低代码创业。
每周筛选真实可验证的机会，附带执行清单。
更多: https://[subdomain].substack.com
```

#### 推荐关注圈子

1. **独立开发者** - 精准用户集中地
2. **AI创业/低代码** - 目标用户大量聚集
3. **跨境电商/副业探索** - 变现意愿强
4. **产品经理之旅** - 工具使用者

#### 验证命令

```bash
# 即刻App设置验证 (手动检查清单)
echo "=== 即刻App设置验证 ==="
echo "⬜ 账号已注册并验证"
echo "⬜ 头像已上传"
echo "⬜ 个人简介已填写，包含Substack链接"
echo "⬜ 已关注 >= 3个目标圈子"
echo "⬜ 首条内容已发布"
echo "⬜ 内容中无直接广告词"
```

---

## 阶段二: 第二个24小时 (Hour 24-48)

### Hour 24-32: 最终准备阶段

**目标**: 完成所有发布前准备

#### Substack后台配置清单

**路径**: Settings 菜单

| 配置项 | 设置内容 | 状态 |
|--------|----------|------|
| Publication Name | AI变现情报 | ⬜ |
| Tagline | 每周筛选、验证、拆解可执行的AI变现机会 | ⬜ |
| About Page | 已填写核心价值主张 | ⬜ |
| Logo | 已上传(或使用默认) | ⬜ |
| Cover Image | 已上传(可选) | ⬜ |
| Welcome Email | 待配置 | ⏳ |
| Paid Subscriptions | 待Stripe连接 | ⏳ |

#### Welcome Email配置

**必含元素**:
1. 感谢订阅
2. 说明免费用户内容(每周1篇免费文章)
3. 付费内容预览/升级理由
4. 1个"样例"链接(指向付费文章预览)
5. 升级按钮

**模板**:
```
亲爱的订阅者，

欢迎加入AI变现情报！

作为免费订阅者，你每周会收到1篇精选内容，
筛选真实可验证的AI变现机会。

如果你想获得更多：
- 每周2-3篇深度分析
- 每周"本周可执行清单"
- 完整SOP、提示词、工具链

可以这里查看付费内容样例:
[insert link to paid teaser]

升级付费订阅: [Upgrade Button]

感谢支持！
[Your Name]
```

---

### Hour 32-40: Stripe连接阶段 (条件性)

**目标**: 根据用户选择的方案执行

#### 方案A: 香港账户流程

**条件**: 用户已选择方案A并有香港身份

**执行步骤**:

| 步骤 | 动作 | 预计时间 | 验证 |
|------|------|----------|------|
| 1 | 登录Substack | 进入Monetization设置 | 5分钟 |
| 2 | 点击Connect with Stripe | 跳转Stripe Connect | 5分钟 |
| 3 | 选择香港为开户国家 | 确认HK在支持列表 | 5分钟 |
| 4 | 提交身份证件 | 上传香港身份证/护照 | 10分钟 |
| 5 | 提交银行账户 | 填写香港银行账户信息 | 10分钟 |
| 6 | 填写税务信息 | 选择W-8BEN(非美税务居民) | 10分钟 |
| 7 | 提交审核 | 等待Stripe审核 | 1-7天 |

#### 方案E: 小报童备选流程

**条件**: 用户无法解决Stripe问题

**执行步骤**:

| 步骤 | 动作 | 预计时间 |
|------|------|----------|
| 1 | 访问小报童 | xiaobaotong.com |
| 2 | 注册账号 | 使用微信扫码登录 |
| 3 | 创建专栏 | 填写标题、简介、定价 |
| 4 | 配置支付 | 绑定微信收款 |
| 5 | 发布内容 | 同步Substack内容 |

---

### Hour 40-48: 启动前验证阶段

**目标**: 完成所有发布前检查

#### 验证清单

| 检查类别 | 检查项 | 验证方式 | 目标状态 |
|----------|--------|----------|----------|
| **账户** | Substack可登录 | 手动登录测试 | ✅ 通过 |
| | Publication可访问 | curl HTTP 200 | ✅ 通过 |
| | RSS Feed可用 | curl HTTP 200 | ✅ 通过 |
| **内容** | 首篇文章就绪 | 文件存在+字数 | ✅ 就绪 |
| | 付费预览就绪 | 文件存在+字数 | ✅ 就绪 |
| | 合规检查通过 | 人工阅读 | ✅ 无禁词 |
| **渠道** | 即刻App设置完成 | 手动检查 | ✅ 就绪 |
| | 首条内容已发布 | 检查App后台 | ✅ 已发布 |
| **支付** | Stripe连接 | 根据方案状态 | 可选 |
| | 测试支付(如可用) | 测试卡验证 | 可选 |

#### 最终验证脚本

```bash
#!/bin/bash
# 48小时执行计划验证脚本
# 运行时间: Hour 48

echo "==================================="
echo "   48小时执行计划验证报告"
echo "==================================="
echo ""

PUB_URL="https://[subdomain].substack.com"
ERRORS=0

# 1. 账户验证
echo "🔍 1. 账户验证"
echo "   - Substack Publication: $PUB_URL"
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" "$PUB_URL")
if [ "$HTTP_CODE" = "200" ]; then
    echo "   ✅ Publication可访问 (HTTP 200)"
else
    echo "   ❌ 访问失败 (HTTP $HTTP_CODE)"
    ERRORS=$((ERRORS+1))
fi

RSS_CODE=$(curl -s -o /dev/null -w "%{http_code}" "$PUB_URL/feed")
if [ "$RSS_CODE" = "200" ]; then
    echo "   ✅ RSS Feed可用"
else
    echo "   ❌ RSS不可用"
    ERRORS=$((ERRORS+1))
fi
echo ""

# 2. 内容验证
echo "🔍 2. 内容验证"
if [ -f "content/launch_post_ready.md" ]; then
    WORDS=$(wc -m < content/launch_post_ready.md)
    echo "   ✅ 首篇文章就绪 ($WORDS 字)"
else
    echo "   ❌ 首篇文章缺失"
    ERRORS=$((ERRORS+1))
fi

if [ -f "content/paid_teaser_ready.md" ]; then
    WORDS=$(wc -m < content/paid_teaser_ready.md)
    echo "   ✅ 付费预览就绪 ($WORDS 字)"
else
    echo "   ❌ 付费预览缺失"
    ERRORS=$((ERRORS+1))
fi
echo ""

# 3. 渠道验证
echo "🔍 3. 渠道验证"
echo "   ⬜ 即刻App账号已设置 (手动验证)"
echo "   ⬜ 首条内容已发布 (手动验证)"
echo ""

# 4. 支付验证
echo "🔍 4. 支付验证 (根据方案)"
echo "   ⬜ Stripe连接状态: [填写实际状态]"
echo "   ⬜ 测试支付状态: [填写实际状态]"
echo ""

# 5. 总结
echo "==================================="
if [ $ERRORS -eq 0 ]; then
    echo "   ✅ 所有验证通过"
    echo "   状态: 准备就绪，可启动"
else
    echo "   ⚠️ 发现 $ERRORS 个问题"
    echo "   状态: 需补充完善"
fi
echo "==================================="
```

---

## 升级触发条件

### 立即升级 (kanban_block)

**触发条件**:
- [ ] 用户确认无法提供任何海外身份
- [ ] 用户拒绝使用小报童备选方案
- [ ] Stripe KYC被拒且无法解决
- [ ] 内容合规检查发现严重违规

**升级内容**:
需要用户提供以下信息才能继续:
1. 具体的Stripe账户解决方案
2. 备选的收款渠道确认

---

## 滚回方案

### 场景1: Stripe无法解决

**滚回动作**:
1. 启用小报童备选方案
2. 将Substack作为内容沉淀和SEO渠道
3. 主收款移至微信/小报童

### 场景2: 内容不足

**滚回动作**:
1. 延长准备时间至72小时
2. 使用现有文档快速改写
3. 先发布免费内容验证

### 场景3: 渠道限制

**滚回动作**:
1. 切换至其他P1渠道(知乎/V2EX)
2. 增加SEO投入
3. 减少对即刻App依赖

---

## 成功标准

### 必须达标 (Hour 48)

- [ ] Substack Publication已创建并可访问
- [ ] 3篇发布就绪内容已准备
- [ ] 即刻App账号已设置并发布首条内容
- [ ] 用户已确认Stripe账户方案
- [ ] Welcome Email已配置 (如支付已就绪)

### 可选标准

- [ ] Logo和Cover Image已设计
- [ ] 微信公众号已创建
- [ ] 知乎账号已注册
- [ ] Stripe连接已完成 (如选择主流方案)

---

## 验证命令汇总

```bash
#!/bin/bash
# 完整验证脚本 - 在Hour 48执行

cd /home/AgentAdmin/.hermes/shared/dev-team/projects/knowledge-subscription

echo "=========================================="
echo "   48小时执行计划完成验证"
echo "=========================================="
echo ""

# 文档验证
echo "📋 1. 必要文档"
ls -la docs/launch_decision.md docs/next_48h_execution_plan.md 2>/dev/null && echo "   ✅ 决策文档存在" || echo "   ❌ 文档缺失"
echo ""

# 内容验证
echo "📝 2. 内容准备"
for f in content/launch_post_ready.md content/paid_teaser_ready.md; do
    if [ -f "$f" ]; then
        wc=$(wc -m < $f)
        echo "   ✅ $f ($wc 字)"
    else
        echo "   ❌ $f (缺失)"
    fi
done
echo ""

# 内容原始文件验证
echo "📁 3. 原始内容文件"
for f in docs/first_video_script_cn_public_v3.md docs/paid_deep_dive_outline.md docs/launch_post_free.md; do
    [ -f "$f" ] && echo "   ✅ $f" || echo "   ❌ $f"
done
echo ""

# 风险文档验证
echo "🛡️  4. 风险评估"
for f in docs/risk_register.md docs/low_risk_channels.md docs/content_compliance_checklist.md; do
    [ -f "$f" ] && echo "   ✅ $f" || echo "   ❌ $f"
done
echo ""

# 支付文档验证
echo "💳 5. 支付准备"
for f in docs/account_payment_blockers.md docs/pricing_ladder.md metrics/revenue_experiment.csv; do
    [ -f "$f" ] && echo "   ✅ $f" || echo "   ❌ $f"
done
echo ""

# 执行清单检查
echo "✅ 6. 执行清单状态"
echo "   ⬜ Substack账号创建: [填写实际状态]"
echo "   ⬜ 3篇内容就绪: [填写实际状态]"
echo "   ⬜ 即刻App设置: [填写实际状态]"
echo "   ⬜ Stripe方案选择: [填写实际状态]"
echo ""

echo "=========================================="
echo "验证完毕。请确认上方所有项目已完成。"
echo "=========================================="
```

---

## 执行完成标志

**当以下所有项目打勾时，执行计划完成**:

- [ ] Substack Publication已创建 (`https://[subdomain].substack.com`)
- [ ] About页面内容已填写
- [ ] 首篇发布内容已就绪 (content/launch_post_ready.md)
- [ ] 付费预览内容已就绪 (content/paid_teaser_ready.md)
- [ ] 即刻App账号已设置
- [ ] 即刻App首条内容已发布
- [ ] 用户已确认Stripe账户方案
- [ ] (Stripe就绪后) Welcome Email已配置
- [ ] (Stripe就绪后) 定价已配置 ($5/$9/$149)

**完成后操作**:
1. 执行验证脚本确认所有项目
2. 更新 `docs/launch_decision.md` 状态为 READY_TO_LAUNCH
3. 使用 `kanban_complete` 标记任务完成

---

**文档路径**: `/home/AgentAdmin/.hermes/shared/dev-team/projects/knowledge-subscription/docs/next_48h_execution_plan.md`

**相关文档**:
- 上线决策: `docs/launch_decision.md`
- 风险登记册: `docs/risk_register.md`
- 账户阻塞点: `docs/account_payment_blockers.md`
- 内容支柱: `docs/content_pillars_30d.md`
- 定价阶梯: `docs/pricing_ladder.md`
