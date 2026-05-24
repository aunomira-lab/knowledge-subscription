# Substack 自动发布架构与账号授权边界

**文档版本**: 1.0  
**更新日期**: 2026-05-11  
**项目**: knowledge-subscription  
**目的**: 设计 Substack 发布链路的自动化方案，明确可/不可自动化项、账号授权边界、安全风控、MVP步骤及验证命令

---

## 1. 执行摘要

### 1.1 核心结论

| 维度 | 结论 |
|------|------|
| **官方API** | ❌ Substack **无公开官方API** 用于程序化发布 |
| **推荐方案** | 半自动发布 (内容生成自动化 + 人工最终确认发布) |
| **自动化等级** | Level 2/5 (内容生成+草稿创建全自动化，发布需人工确认) |
| **支付方案** | 必须使用 Substack原生Stripe Connect，外部支付仅作fallback |

### 1.2 方案对比矩阵

| 方案 | 自动化程度 | 稳定性 | 风险 | 推荐度 | 适用场景 |
|------|-----------|--------|------|--------|----------|
| **A. 邮件发布** | ⭐⭐⭐ | 高 | 低 | ⭐⭐⭐⭐⭐ | **首选方案** |
| **B. 浏览器自动化** | ⭐⭐⭐⭐ | 中 | 中 | ⭐⭐⭐⭐ | 备用方案 |
| **C. Webhook集成** | ⭐⭐⭐⭐⭐ | 中 | 中 | ⭐⭐⭐ | 需配合API端点 |
| **D. RSS同步** | ⭐⭐⭐ | 高 | 低 | ⭐⭐⭐⭐ | 外部→Substack单向 |
| **E. 第三方服务** | ⭐⭐⭐⭐ | 低 | 高 | ⭐⭐ | 不推荐 |

### 1.3 自动化边界总览

```
┌─────────────────────────────────────────────────────────────────────┐
│                      Substack 发布流程                               │
├─────────────────────────────────────────────────────────────────────┤
│  内容生成 → 草稿创建 → 预览审核 → 发布确认 → 邮件发送 → 数据分析   │
│     ✅         ✅         ⚠️         ⚠️         ✅         ✅       │
│   全自动     全自动    半自动     半自动     全自动     全自动      │
└─────────────────────────────────────────────────────────────────────┘

图例: ✅ 可全自动  ⚠️ 需人工介入  ❌ 不可自动化
```

---

## 2. 可自动化项 vs 不可自动化项

### 2.1 可全自动化的项目

| 功能 | 实现方式 | 复杂度 | 备注 |
|------|----------|--------|------|
| **内容生成** | AI模板 + 数据源 | 低 | 已实现在 `content_generator.py` |
| **Markdown格式化** | 模板引擎 | 低 | 标准Substack格式 |
| **草稿创建** | 邮件发送到草稿地址 | 低 | 每个Substack有专属草稿邮箱 |
| **封面图生成** | AI绘图API | 中 | 可自动生成配图 |
| **SEO元数据** | 自动提取 | 低 | 标题/摘要/标签 |
| **邮件列表导出** | CSV导出 | 低 | 定期备份订阅者数据 |
| **RSS Feed同步** | RSS解析 | 低 | 外部内容→Substack |
| **数据统计** | 导出CSV分析 | 低 | Stripe + Substack Analytics |
| **定时提醒** | Cron + 通知 | 低 | 提醒人工发布 |

### 2.2 需半自动化的项目 (人工最终确认)

| 功能 | 自动化程度 | 原因 | 实现方式 |
|------|-----------|------|----------|
| **发布确认** | 80% | 内容合规检查 | 生成预览→人工确认→API/脚本发布 |
| **付费墙设置** | 70% | 需要策略判断 | 模板配置 + 人工审核 |
| **发布时间选择** | 60% | 需要考虑受众时区 | AI建议 + 人工调整 |
| **邮件标题优化** | 80% | A/B测试需要 | 生成多版本→人工选择 |
| **标签/分类** | 70% | 内容分类需判断 | AI建议 + 人工确认 |

### 2.3 不可自动化项 (必须人工操作)

| 功能 | 原因 | 用户必须操作 |
|------|------|--------------|
| **Stripe KYC验证** | 金融监管要求 | 提交身份证件、银行信息 |
| **税务信息(W-9/W-8BEN)** | 法律合规 | 填写税务表格 |
| **提现操作** | 资金安全 | 手动发起/确认提现 |
| **争议处理** | 需要人工判断 | 退款、投诉处理 |
| **订阅者管理** | 隐私合规 | 删除数据请求处理 |
| **重大内容决策** | 品牌风险 | 内容方向调整 |
| **平台政策更新应对** | 需人工理解 | 调整策略以符合新规 |

---

## 3. 账号与授权清单 (用户必须提供)

### 3.1 Substack账号信息

```yaml
# 基础信息 - 注册时必须提供
substack_account:
  email: "_______"                    # Substack登录邮箱
  password: "_______"                 # 密码 (用于浏览器自动化)
  publication_name: "_______"         # 发布名称 (如: AI Money Brief)
  subdomain: "_______"                # 子域名 (如: aimoneybrief)
  full_url: "_______"                 # 完整URL (如: https://aimoneybrief.substack.com)
  
# 草稿邮箱 - 用于邮件发布
automation:
  draft_email: "_______"              # 格式: [pub-name]+draft@substack.com
                                      # 在 Substack Settings > Emails 中查看
```

### 3.2 Stripe Connect授权

```yaml
# Stripe连接状态
stripe_connect:
  onboarding_status: "_______"        # not_started / in_progress / verified / blocked
  account_id: "_______"               # acct_xxxxx (连接后可见)
  payout_country: "_______"           # 提现国家 (HK/SG/US等)
  payout_currency: "_______"          # 结算货币 (USD)
  
# 验证文件 - 必须上传
verification:
  identity_document: "_______"        # 护照/身份证/驾照
  proof_of_address: "_______"         # 地址证明 (部分国家)
  tax_form: "_______"                 # W-9(美国) / W-8BEN(国际)
  bank_account: "_______"             # 银行账户信息
```

### 3.3 自动化工具授权

```yaml
# 邮件发送配置 (用于草稿发布)
email_smtp:
  host: "smtp.gmail.com"              # SMTP服务器
  port: 587                           # 端口
  username: "_______"                 # 邮箱账号
  password: "_______"                 # 应用专用密码/App Password
  
# 浏览器自动化 (备用方案)
browser_automation:
  session_cookie: "_______"           # 登录后的session cookie
  csrf_token: "_______"               # 防跨站请求伪造token
  
# API/Webhook (如使用第三方)
webhook:
  endpoint_url: "_______"             # 接收发布状态的webhook
  secret_key: "_______"               # 验证签名密钥
```

### 3.4 检查清单 - 用户必须确认

- [ ] Substack publication 已创建并可访问
- [ ] Stripe Connect onboarding 已完成
- [ ] 银行账户已验证通过
- [ ] 税务信息已提交
- [ ] 草稿邮箱地址已获取
- [ ] 至少完成一次测试发布
- [ ] 确认提现流程正常工作
- [ ] 已备份登录凭据到安全位置

---

## 4. 安全与风控边界

### 4.1 平台限制与红线

| 限制类型 | 具体限制 | 违规后果 |
|----------|----------|----------|
| **发布频率** | 建议 ≤ 3篇/天 | 账号标记/限制 |
| **内容原创** | 严禁抄袭/洗稿 | 删除内容/封号 |
| **垃圾信息** | 禁止未经请求的邮件 | 退订率上升/信誉下降 |
| **自动化强度** | 无明显机器人行为 | 验证码/CAPTCHA挑战 |
| **支付欺诈** | 禁止自刷/虚假交易 | Stripe封号/资金冻结 |

### 4.2 浏览器自动化风险

| 风险 | 概率 | 缓解措施 |
|------|------|----------|
| **账号验证挑战** | 中 | 使用真实浏览器指纹，避免headless |
| **IP封禁** | 低 | 使用固定IP，避免频繁切换 |
| **行为检测** | 中 | 添加随机延迟，模拟人工操作 |
| **Cookie失效** | 高 | 定期更新登录状态 |
| **UI变更** | 高 | 使用稳定的CSS选择器，添加监控 |

### 4.3 数据安全边界

```
┌──────────────────────────────────────────────────────────────┐
│                     数据安全等级                              │
├──────────────────────────────────────────────────────────────┤
│ 🔴 极高风险: Stripe私钥、银行账户密码 → 仅用户本地保存       │
│ 🟠 高风险: Substack密码、Cookie → 加密存储，定期轮换         │
│ 🟡 中风险: API密钥、Webhook secret → 环境变量管理            │
│ 🟢 低风险: 内容模板、发布日志 → 可版本控制                   │
└──────────────────────────────────────────────────────────────┘
```

### 4.4 合规检查点

| 检查点 | 验证方式 | 频率 |
|--------|----------|------|
| **Stripe账户状态** | 检查payout是否pending | 每次发布前 |
| **订阅者同意** | 确认opt-in记录 | 定期审计 |
| **内容合规** | 敏感词/版权检查 | 每篇发布前 |
| **税务状态** | Stripe税务设置 | 季度检查 |
| **数据备份** | 订阅者列表导出 | 每周 |

---

## 5. 技术架构方案

### 5.1 推荐架构: 邮件发布优先

```
┌──────────────────────────────────────────────────────────────────────┐
│                        自动化发布架构                                 │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│   ┌──────────────┐     ┌──────────────┐     ┌──────────────┐        │
│   │ Content Gen  │────▶│  Markdown    │────▶│ Email Client │        │
│   │  (AI/Template)│    │  Formatter   │     │  (SMTP)      │        │
│   └──────────────┘     └──────────────┘     └──────┬───────┘        │
│                                                    │                  │
│                                                    ▼                  │
│   ┌──────────────┐     ┌──────────────┐     ┌──────────────┐        │
│   │   Substack   │◀────│ Draft Queue  │◀────│ draft+pub@   │        │
│   │   Published  │     │  (Pending)   │     │ substack.com │        │
│   └──────────────┘     └──────────────┘     └──────────────┘        │
│          │                                                          │
│          ▼                                                          │
│   ┌──────────────┐     ┌──────────────┐     ┌──────────────┐        │
│   │  Notification│────▶│  Human       │────▶│  Final       │        │
│   │  (Ready to   │     │  Review      │     │  Publish     │        │
│   │   Publish)   │     │  (Approve)   │     │  (Manual)    │        │
│   └──────────────┘     └──────────────┘     └──────────────┘        │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```

### 5.2 组件说明

| 组件 | 技术选型 | 职责 |
|------|----------|------|
| **Content Generator** | Python + Jinja2 | 生成Markdown内容 |
| **Email Client** | smtplib / sendgrid | 发送草稿到Substack |
| **Draft Queue** | SQLite/JSON | 追踪待发布草稿状态 |
| **Notification** | Webhook/Email | 通知人工审核 |
| **Analytics** | Pandas + CSV | 分析发布效果 |

### 5.3 备用方案: 浏览器自动化

当邮件方案不可用时启用:

```python
# 使用 Playwright 的浏览器自动化示例 (伪代码)
async def publish_to_substack(title, content, cookies):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)  # 非headless降低检测
        context = await browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)...'
        )
        # 加载登录cookie
        await context.add_cookies(cookies)
        
        page = await context.new_page()
        await page.goto('https://substack.com/home')
        
        # 等待并点击 "New post"
        await page.click('text=New post')
        await page.wait_for_selector('[data-testid="post-title"]')
        
        # 填写内容
        await page.fill('[data-testid="post-title"]', title)
        await page.fill('[contenteditable="true"]', content)
        
        # 设置付费墙 (可选)
        await page.click('text=Paid subscribers only')
        
        # 发布
        await page.click('text=Publish')
        await page.click('text=Publish now')
```

### 5.4 发布流程状态机

```
                    ┌─────────────┐
                    │   START     │
                    └──────┬──────┘
                           │
                           ▼
                    ┌─────────────┐
                    │   GENERATE  │  ← 全自动 (AI生成内容)
                    └──────┬──────┘
                           │
                           ▼
                    ┌─────────────┐
                    │    DRAFT    │  ← 全自动 (发送到草稿)
                    └──────┬──────┘
                           │
                           ▼
                    ┌─────────────┐
                    │   QUEUED    │  ← 等待人工审核
                    └──────┬──────┘
                           │
              ┌────────────┼────────────┐
              │            │            │
              ▼            ▼            ▼
        ┌─────────┐  ┌─────────┐  ┌─────────┐
        │ APPROVE │  │  EDIT   │  │  REJECT │
        └────┬────┘  └────┬────┘  └────┬────┘
             │            │            │
             ▼            │            ▼
        ┌─────────┐       │       ┌─────────┐
        │ PUBLISH │◀──────┘       │  DISCARD│
        └────┬────┘               └─────────┘
             │
             ▼
        ┌─────────┐
        │ NOTIFY  │  ← 通知订阅者
        └────┬────┘
             │
             ▼
        ┌─────────┐
        │ ANALYZE │  ← 统计数据分析
        └─────────┘
```

---

## 6. MVP步骤

### 6.1 Phase 1: 基础自动化 (Week 1)

**目标**: 实现内容生成到草稿的全自动化

| 任务 | 时长 | 验证命令 |
|------|------|----------|
| 配置SMTP邮箱 | 1h | `python -c "import smtplib; smtplib.SMTP('smtp.gmail.com', 587).starttls()"` |
| 获取草稿邮箱 | 30m | 在 Substack Settings > Emails 查看 |
| 编写邮件发布脚本 | 4h | `python scripts/substack_email_publish.py --dry-run` |
| 测试草稿创建 | 1h | 检查Substack后台是否出现草稿 |
| 集成到内容生成器 | 2h | `python app/content_generator.py --output substack` |

**Phase 1完成标准**:
- [ ] 运行内容生成器可自动发送草稿到Substack
- [ ] 草稿在Substack后台正确显示
- [ ] 人工可一键发布

### 6.2 Phase 2: 半自动工作流 (Week 2)

**目标**: 建立审核→发布的半自动流程

| 任务 | 时长 | 说明 |
|------|------|------|
| 创建草稿队列系统 | 4h | SQLite表存储待发布草稿 |
| 实现通知机制 | 2h | 发布提醒到微信/邮件 |
| 编写预览生成器 | 3h | 生成HTML预览供审核 |
| 创建发布CLI工具 | 3h | `python scripts/publish.py --id [draft-id]` |
| 测试完整流程 | 2h | 端到端测试 |

**Phase 2完成标准**:
- [ ] 内容生成后自动通知人工审核
- [ ] 人工确认后一键发布
- [ ] 发布后自动记录到数据库

### 6.3 Phase 3: 定时与优化 (Week 3-4)

**目标**: 实现定时发布和效果追踪

| 任务 | 时长 | 说明 |
|------|------|------|
| 配置定时任务 | 2h | Cron或类似调度 |
| 实现发布时间优化 | 4h | 根据数据选择最佳发布时间 |
| 集成Analytics | 4h | 导出Substack数据并分析 |
| 创建Dashboard | 4h | 展示发布状态和效果 |
| 优化迭代 | 4h | 根据使用反馈改进 |

**Phase 3完成标准**:
- [ ] 可定时自动生成和发送草稿
- [ ] 发布数据分析自动化
- [ ] 完整的发布仪表盘

---

## 7. 验证命令

### 7.1 前置条件验证

```bash
#!/bin/bash
# substack_preflight_check.sh
# Substack自动化前置检查

echo "=== Substack 自动化发布前置检查 ==="
echo ""

# 1. 检查Substack可访问
echo "[1/8] 检查 Substack 可访问性..."
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" "https://substack.com")
if [ "$HTTP_CODE" = "200" ]; then
    echo "✅ Substack 可访问 (HTTP 200)"
else
    echo "❌ Substack 不可访问 (HTTP $HTTP_CODE)"
fi

# 2. 检查Publication
echo ""
echo "[2/8] 检查 Publication..."
PUB_URL="${SUBSTACK_PUB_URL:-https://example.substack.com}"
PUB_CODE=$(curl -s -o /dev/null -w "%{http_code}" "$PUB_URL")
if [ "$PUB_CODE" = "200" ]; then
    echo "✅ Publication 可访问 ($PUB_URL)"
else
    echo "⚠️ Publication 检查失败 (HTTP $PUB_CODE)"
    echo "    请确认 PUB_URL 环境变量已设置"
fi

# 3. 检查RSS Feed
echo ""
echo "[3/8] 检查 RSS Feed..."
RSS_CODE=$(curl -s -o /dev/null -w "%{http_code}" "$PUB_URL/feed")
if [ "$RSS_CODE" = "200" ]; then
    echo "✅ RSS Feed 可用"
else
    echo "⚠️ RSS Feed 检查失败 (HTTP $RSS_CODE)"
fi

# 4. 检查Stripe支持国家
echo ""
echo "[4/8] 检查 Stripe 支持国家列表..."
curl -s "https://stripe.com/global" | grep -oP 'country=[A-Z]{2}' | sed 's/country=//' | sort -u > /tmp/stripe_countries.txt
COUNTRY_COUNT=$(wc -l < /tmp/stripe_countries.txt)
echo "    找到 $COUNTRY_COUNT 个支持国家"

# 5. 检查SMTP配置
echo ""
echo "[5/8] 检查 SMTP 配置..."
if [ -n "$SMTP_HOST" ] && [ -n "$SMTP_USER" ]; then
    echo "✅ SMTP 环境变量已设置"
else
    echo "⚠️ SMTP 环境变量未设置 (SMTP_HOST, SMTP_USER, SMTP_PASS)"
fi

# 6. 检查草稿邮箱
echo ""
echo "[6/8] 检查草稿邮箱配置..."
if [ -n "$SUBSTACK_DRAFT_EMAIL" ]; then
    echo "✅ 草稿邮箱已配置: $SUBSTACK_DRAFT_EMAIL"
else
    echo "⚠️ 草稿邮箱未配置 (SUBSTACK_DRAFT_EMAIL)"
fi

# 7. 检查Python依赖
echo ""
echo "[7/8] 检查 Python 依赖..."
python3 -c "import smtplib, email, jinja2" 2>/dev/null && echo "✅ Python依赖已安装" || echo "❌ 缺少Python依赖"

# 8. 汇总
echo ""
echo "=== 检查汇总 ==="
echo "请确认以下项目:"
echo "  ⬜ Substack publication 已创建"
echo "  ⬜ Stripe Connect 已完成"
echo "  ⬜ 银行账户已验证"
echo "  ⬜ 税务信息已提交"
echo "  ⬜ 草稿邮箱地址已获取"
echo "  ⬜ SMTP邮箱可发送邮件"
echo "  ⬜ 测试发布已完成"
```

### 7.2 邮件发布验证

```bash
#!/bin/bash
# test_substack_email.sh
# 测试邮件发布功能

echo "=== Substack 邮件发布测试 ==="

# 测试邮件发送
python3 << 'EOF'
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

smtp_host = os.getenv('SMTP_HOST', 'smtp.gmail.com')
smtp_port = int(os.getenv('SMTP_PORT', '587'))
smtp_user = os.getenv('SMTP_USER')
smtp_pass = os.getenv('SMTP_PASS')
draft_email = os.getenv('SUBSTACK_DRAFT_EMAIL')

if not all([smtp_user, smtp_pass, draft_email]):
    print("❌ 缺少必要的环境变量")
    print("需要: SMTP_USER, SMTP_PASS, SUBSTACK_DRAFT_EMAIL")
    exit(1)

msg = MIMEMultipart()
msg['From'] = smtp_user
msg['To'] = draft_email
msg['Subject'] = '测试: Substack自动化发布'

body = """
# 这是一篇测试文章

这是Substack自动化发布系统的测试内容。

如果看到这篇文章，说明邮件发布功能正常。
"""

msg.attach(MIMEText(body, 'plain', 'utf-8'))

try:
    server = smtplib.SMTP(smtp_host, smtp_port)
    server.starttls()
    server.login(smtp_user, smtp_pass)
    server.send_message(msg)
    server.quit()
    print(f"✅ 测试邮件已发送到: {draft_email}")
    print("   请检查Substack后台的草稿箱")
except Exception as e:
    print(f"❌ 发送失败: {e}")
EOF
```

### 7.3 浏览器自动化验证

```bash
#!/bin/bash
# test_browser_automation.sh
# 测试浏览器自动化 (需要安装playwright)

echo "=== 浏览器自动化测试 ==="

python3 << 'EOF'
import asyncio
from playwright.async_api import async_playwright

async def test_login():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, slow_mo=100)
        context = await browser.new_context()
        page = await context.new_page()
        
        print("正在访问 Substack...")
        await page.goto('https://substack.com/sign-in')
        
        # 检查登录表单是否存在
        try:
            await page.wait_for_selector('input[type="email"]', timeout=5000)
            print("✅ 登录页面可访问")
        except:
            print("❌ 无法加载登录页面")
            
        await browser.close()

asyncio.run(test_login())
EOF
```

### 7.4 集成测试

```bash
#!/bin/bash
# full_pipeline_test.sh
# 完整流程测试

echo "=== 完整发布流程测试 ==="

# 1. 生成测试内容
echo "[1/4] 生成测试内容..."
python3 app/content_generator.py --test --output /tmp/test_post.md

# 2. 发送到草稿
echo "[2/4] 发送草稿到Substack..."
python3 scripts/substack_email_publish.py --input /tmp/test_post.md --dry-run

# 3. 检查队列
echo "[3/4] 检查发布队列..."
python3 scripts/queue.py list

# 4. 验证状态
echo "[4/4] 验证状态..."
echo "请手动检查:"
echo "  1. Substack后台是否出现草稿"
echo "  2. 邮件通知是否收到"
echo "  3. 队列状态是否正确"
```

---

## 8. 实施建议

### 8.1 推荐配置

```yaml
# config/substack_automation.yaml
automation:
  # 发布模式: email (推荐) | browser (备用)
  mode: "email"
  
  # 邮件发布配置
  email:
    draft_address: "your-pub+draft@substack.com"  # 从Substack后台获取
    smtp:
      host: "smtp.gmail.com"
      port: 587
      use_tls: true
      
  # 浏览器配置 (备用)
  browser:
    headless: false
    slow_mo: 1000  # 毫秒延迟
    viewport:
      width: 1920
      height: 1080
      
  # 工作流配置
  workflow:
    require_approval: true      # 是否需人工确认
    auto_schedule: false        # 是否自动定时
    notify_channels:            # 通知渠道
      - email
      - wechat
      
  # 内容设置
  content:
    default_tags: ["AI", "变现", "自动化"]
    paywall_after_paragraphs: 3
    send_email: true
```

### 8.2 启动检查清单

- [ ] 用户已创建Substack账号并设置publication
- [ ] Stripe Connect已完成且验证通过
- [ ] 草稿邮箱地址已获取并测试
- [ ] SMTP邮箱配置完成并测试发送
- [ ] 至少完成一次手动测试发布
- [ ] 发布流程文档已更新
- [ ] 监控和告警已配置

### 8.3 常见问题和解决

| 问题 | 原因 | 解决方案 |
|------|------|----------|
| 草稿未出现 | 邮箱错误 | 确认draft+pub@substack.com格式正确 |
| 邮件被拒 | SMTP限制 | 使用App Password而非主密码 |
| 格式错乱 | Markdown解析 | 使用标准Markdown语法，避免复杂HTML |
| 图片未显示 | 外链限制 | 上传到图床或使用Substack自带上传 |
| 发布失败 | 登录过期 | 更新cookie或重新登录 |

---

## 9. 结论

### 9.1 核心决策

1. **优先方案**: 邮件发布 (Level 2自动化)
   - 内容生成 → 草稿创建: 全自动
   - 发布确认: 需人工审核 (合规要求)

2. **支付方案**: 必须使用Substack原生Stripe Connect
   - 外部支付(微信/支付宝)仅作fallback
   - 需用户解决HK/SG/US身份问题

3. **安全边界**: 
   - 不存储Stripe私钥
   - 不自动化KYC/税务流程
   - 人工最终确认所有发布

### 9.2 下一步行动

1. **立即**: 用户确认Substack账号和Stripe状态
2. **本周**: 实现Phase 1 (邮件发布自动化)
3. **下周**: 实现Phase 2 (审核工作流)
4. **Month 1**: 实现完整自动化并优化

### 9.3 资源需求

| 资源 | 说明 | 成本 |
|------|------|------|
| SMTP邮箱 | 用于发送草稿 | 免费 (Gmail) |
| 图床 | 图片托管 | 免费/低成本 |
| 服务器 | 运行自动化脚本 | 现有基础设施 |
| 用户时间 | 审核和确认 | ~30分钟/周 |

---

**文档维护**: 此文档应随Substack平台更新而更新，建议每季度审查一次。

**验证状态**: ⬜ 待用户确认账号信息后执行验证命令
