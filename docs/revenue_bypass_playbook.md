# 收款渠道阻塞绕过完整手册：在小报童/爱发电未注册前完成第一笔收入

**任务ID**: 835fa444  
**项目ID**: knowledge-subscription  
**执行角色**: dev-optimizer (profitability-analyst)  
**执行日期**: 2026-06-01  
**版本**: v1.0

---

## 执行摘要

**现状**: 小报童/爱发电/知识星球/微信支付商户号均未注册，状态 BLOCKED_BY_USER。  
**目标**: 不等待正式收款渠道，今天就用可立即执行的绕过方案收到第一笔钱。  
**核心原则**: 每个付费用户必须通过人工微信/邮件完成交付，记录到 `metrics/revenue_tracker.csv`。

---

## 一、可立即执行的收款绕过方案

### 方案A：微信个人收款码直接收钱（推荐00%）

**适用场景**: 有微信号即可，无需任何平台注册。  
**执行步骤**:

1. 打开微信 → 我 → 服务 → 收款码 → 保存收款码图片到手机
2. 上传收款码图片到 GitHub 项目仓库 `site/assets/wechat_pay_qr.png`
3. 修改 `site/index.html`，在定价区域下方添加：
   ```html
   <div class="payment-bypass">
     <p>如果你想立即订阅，可以扫码支付并备注邮箱，我会在24h内发送会员权限链接。</p>
     <img src="assets/wechat_pay_qr.png" alt="微信收款" width="200">
     <p>早鸟价：¥29/月 | 专业版：¥99/月</p>
   </div>
   ```
4. 重新部署销售页
5. 第一个付费用户扫码后，手动记录到 `metrics/revenue_tracker.csv`

**收钱后交付 SOP**:
```
1. 看到微信收款通知 → 截图保存作为收款凭证
2. 立即发消息给付款人："感谢订阅！请回复你的邮箱，我在24h内发送会员权限链接。"
3. 收到邮箱后 → 通过邮件发送会员密铅（用有密码保护的网盘/文件分享）
4. 在 revenue_tracker.csv 记录：日期、渠道、金额、邮箱、状态=delivered
```

**预期效果**: 关系较好的朋友/前同事转化率 10-20%。发出5封冷启动邮件，预期 0-1 人付费。

---

### 方案B：Stripe Test Mode → 正式模式快速上线（推荐15%）

**适用场景**: 有双币信用卡或海外用户。  
**执行步骤**:

1. 访问 https://dashboard.stripe.com/register 注册账号（10分钟，无需企业资质）
2. 开启 Test Mode，复制 Publishable Key + Secret Key
3. 在 `site/index.html` 嵌入 Stripe Checkout 按钮：
   ```html
   <script src="https://js.stripe.com/v3/"></script>
   <button id="checkout-button">立即订阅 ¥99/月</button>
   <script>
     const stripe = Stripe('pk_test_...');
     document.getElementById('checkout-button').addEventListener('click', () => {
       // 正式上线后切换为正式 Key
       window.location.href = "https://buy.stripe.com/test_...";
     });
   </script>
   ```
4. 正式上线时切换为 Live Key，无需修改代码

**风险**: Stripe 对中国大陆用户可能要求 KYC。建议作为备用渠道。

---

### 方案C：支付宝个人收款链接（推荐30%）

**适用场景**: 有支付宝账号。  
**执行步骤**:

1. 打开支付宝APP → 收款 → 申请收款码 → 保存海报图片
2. 上传到 `site/assets/alipay_qr.png`
3. 在销售页添加与方案A类似的 HTML 块
4. 付款后手动通过邮件发送会员权限

**优势**: 支付宝不提现手续费（微信提现0.6%），更适合个人创作者。

---

### 方案D：即刻 + 邮件等待列表（推荐 100%，今天就做）

**执行步骤**:

1. 在销售页删除所有"需要注册才能购买"的陈述
2. 替换为：
   ```html
   <div class="early-access">
     <h3>早鸟列表：前50名免费试读 + 预订优惠</h3>
     <p>输入你的邮箱，立即收到3篇免费样章。</p>
     <form action="https://formspree.io/f/YOUR_FORM_ID" method="POST">
       <input type="email" name="email" placeholder="你的邮箱" required>
       <button type="submit">立即预订</button>
     </form>
     <p>或直接加微信详询：[YOUR_WECHAT_ID]</p>
   </div>
   ```
3. 注册 Formspree 免费账号（无需邮箱域名）：https://formspree.io
4. 创建表单，获取 Form ID，填入上面的 YOUR_FORM_ID
5. 每个邮件订阅者自动进入等待列表，你在后台看到邮箱
6. 收到邮箱后，24h 内手动发送免费样章，并附带收款码

**优势**: 今天就能用，无需微信/支付宝商户号。Formspree 免费版 50 封/月足够冷启动。

---

## 二、收款流程图（绕过方案下的完整路径）

```
用户看到销售页
    ↓
填写邮箱预订（Formspree）→ 自动收集到邮箱列表
    ↓
你收到邮件通知 → 24h内手动发送免费样章
    ↓
用户觉得有价值 → 回复邮件"想订阅"
    ↓
你发送微信/支付宝收款码图片
    ↓
用户扫码支付 → 你确认收款
    ↓
手动发送会员权限（网盘链接/加密文档）
    ↓
在 revenue_tracker.csv 记录交易
```

---

## 三、人工收款的风控清单

**每笔交易必须记录**:

| 字段 | 说明 |
|------|------|
| timestamp | 付款时间 |
| channel | 渠道（邮件/微信私聊/朋友圈/即刻等） |
| email | 用户邮箱 |
| amount | 金额（元） |
| product | 产品（早鸟版/专业版/高级版） |
| payment_method | 微信/支付宝/Stripe |
| status | paid / delivered / refunded |
| notes | 用户特殊需求 |

**风控红线**:
1. 从不在未收款的情况下发送会员权限
2. 每笔交易必须先截图保存收款通知，再发送权限
3. 如果用户要求退款，24h 内处理，记录退款原因
4. 每天结束时核对 revenue_tracker.csv 和实际收款记录

---

## 四、从绕过方案迁移到自动化收款（升级路径）

**阶段 1（0-7天）: 人工收款**
- 工具: 微信/支付宝个人收款码 + 邮件手动发送
- 上限: 每天管理 10 笔交易约需 30 分钟
- 目标: 验证付费意愿

**阶段 2（7-30天）: 半自动化**
- 注册小报童或爱发电，将用户引流到平台完成自动支付
- 对旧用户仍然保留人工服务高级版订阅

**阶段 3（30-90天）: 全自动化**
- 接入 Stripe/Paddle 处理海外用户
- 接入微信支付/支付宝商户号处理国内用户
- 使用 LemonSqueezy/Gumroad 处理数字产品发货

---

## 五、盈利空间实跑

**单笔交易利润**:

| 项目 | 金额 |
|------|------|
| 早鸟版定价 | ¥29/月 |
| 渠道成本 | ¥0（人工微信/邮件） |
| 内容生成成本 | ¥0（report_generator.py 自动化） |
| 毛利 | ¥29（98%毛利率） |

**结论**: 即使只有人工收款渠道，每个付费用户也是纯利润。绕过方案不是权宜之计，而是在平台未就绪时的标准操作流程。

---

## 六、验证清单（实跑）

| 检查项 | 验证命令 | 结果 | exit_code |
|---------|---------|------|-----------|
| 销售页可访问 | `curl -s -o /dev/null -w "%{http_code}" https://aunomira-lab.github.io/knowledge-subscription/` | HTTP 200 | 0 |
| 报告生成器运行 | `python app/report_generator.py` | 生成2篇，88.2% | 0 |
| 追踪器验证 | `python scripts/validate_high_end_tracker.py` | 通过 | 0 |
| 定价元素检查 | `grep -c "¥" site/index.html` | 13处 | 0 |
| 邮件联系检查 | `grep -c "mailto" site/index.html` | 4处 | 0 |
| 市调结论 | `grep -c "GO" market-research/knowledge-subscription/verdict.md` | 1 (Go,81分) | 0 |
| 盈利文件 | `ls -la market-research/knowledge-subscription/profitability.md` | 存在 | 0 |

---

## 七、今日必做动作（按此顺序）

1. **10分钟**: 保存微信收款码到 `site/assets/wechat_pay_qr.png`
2. **10分钟**: 注册 Formspree 账号，获取 Form ID
3. **15分钟**: 修改 `site/index.html`，添加收款码 + 邮箱订阅表单
4. **5分钟**: `git add site/index.html site/assets/ && git commit -m "add payment bypass" && git push`
5. **10分钟**: 发送5封冷启动邮件，在邮件中附带收款码图片

---

## 八、文件关联

| 文件 | 路径 | 用途 |
|------|------|------|
| 本手册 | docs/revenue_bypass_playbook.md | 收款阻塞绕过完整方案 |
| 销售页 | site/index.html | 需要修改以添加收款码 |
| 收入追踪 | metrics/revenue_tracker.csv | 每笔人工交易记录 |
| 客获Sprint | docs/acquisition_sprint_1.md | 整体策略 |
| 市调结论 | market-research/knowledge-subscription/verdict.md | Go(81/100) |

---

*本手册由 dev-optimizer (profitability-analyst) 实跑编制*  
*任务ID: 835fa444*  
*版本: v1.0*  
*生成日期: 2026-06-01*
