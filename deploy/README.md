# knowledge-subscription 部署指南

**项目**: AI Opportunity Radar / 知识付费订阅
**项目ID**: knowledge-subscription
**任务ID**: 5fc6593c
**部署平台**: Cloudflare Pages（主推）/ Vercel / GitHub Pages
**当前状态**: BLOCKED_BY_USER — 需用户完成账号授权后方可上线
**更新日期**: 2026-05-23
**负责人**: dev-deploy (deployer)

---

## 一、部署平台选择（三选一，推荐 Cloudflare Pages）

| 平台 | 国内速度 | HTTPS | 自定义域名 | 后端支持 | 费用 | 推荐度 |
|------|----------|-------|-----------|---------|------|--------|
| **Cloudflare Pages** | 快 | 自动 | 免费支持 | Workers/KV | 免费 | 首推 |
| **Vercel** | 一般 | 自动 | 免费支持 | Serverless | 免费 | 海外用户为主 |
| **GitHub Pages** | 不稳定 | 自动 | 支持 | 无 | 免费 | 纯静态备选 |

**结论**: 选择 Cloudflare Pages。国内访问体验最佳，支持 Workers 做表单后端，且免费额度充足。

---

## 二、用户账号授权步骤（必须完成）

### 2.1 Cloudflare 账号注册与授权（两种模式）

#### 模式 A：OAuth 交互登录（推荐用于本地开发）

```bash
# 步骤1: 注册账号
# 访问 https://dash.cloudflare.com/sign-up
# 需要：邮箱 + 密码 + 手机验证（部分区域）

# 步骤2: 安装 Wrangler CLI
npm install -g wrangler

# 步骤3: 登录授权（浏览器会弹出 OAuth 页面）
wrangler login

# 步骤4: 验证登录
wrangler whoami
# 期望输出: 你的邮箱 + Account ID

# 步骤5: 记录 Account ID（部署和配置域名时需要）
# 在 Cloudflare Dashboard 右侧边栏复制
```

#### 模式 B：API Token 无头登录（推荐用于 CI/服务器/无浏览器环境）

```bash
# 步骤1: 在 Cloudflare Dashboard 创建 API Token
# 访问: https://dash.cloudflare.com/profile/api-tokens
# 点击 "Create Token" -> "Custom token"
# 权限设置:
#   - Account: Cloudflare Pages: Edit
#   - Zone: (如使用自定义域名) Zone: Read
# 账户资源: 包含你的账户
# 然后 "Continue to summary" -> "Create Token"
# 复制生成的 Token（只显示一次）

# 步骤2: 设置环境变量（当前终端会话）
export CLOUDFLARE_API_TOKEN="你的Token字符串"

# 步骤3: 验证 Token 有效
wrangler whoami
# 期望输出包含你的邮箱和 Account ID

# 步骤4: 执行部署（无需浏览器交互）
./deploy/deploy.sh production
```

**注意**: 模式 B 是服务器/CI 环境的唯一可行方式。本项目当前环境没有浏览器，必须使用模式 B 或用户手动 OAuth 后返回继续。

### 2.2 支付渠道账号（收款用，至少配置一个）

| 渠道 | 注册地址 | 要求 | 费率 | 适合阶段 |
|------|----------|------|------|----------|
| **小报童** | https://xiaobot.net | 微信个人号即可 | 5-10% | 首推，内容付费专用 |
| **爱发电** | https://afdian.net | 手机号即可 | 6% | 备选，创作者支持 |
| **Stripe** | https://stripe.com | 海外银行卡/公司 | 2.9%+$0.30 | 海外用户 |

> 第一阶段建议：先开小报童专栏，0 成本启动，有收入后再升级正式支付。

### 2.3 联系信息填充（销售页必填）

编辑 `site/index.html`，搜索以下占位符并替换为真实信息：

| 占位符 | 替换为 | 位置 |
|--------|--------|------|
| `AI-Radar-2026` | 你的真实微信号 | 页脚联系区 |
| `contact@ai-radar.dev` | 你的真实邮箱 | 页脚联系区 + mailto 链接 |
| `https://xiaobot.net` | 你的小报童专栏链接 | 支付区 #pay |
| `https://afdian.net` | 你的爱发电主页链接 | 支付区 #pay |
| `https://stripe.com` | 你的 Stripe 收款链接 | 支付区 #pay |

---

## 三、可执行部署脚本

### 3.1 一键部署脚本（已就绪）

文件: `deploy/deploy.sh`

**使用方法**:

```bash
# 进入项目目录
cd /home/AgentAdmin/.hermes/shared/dev-team/projects/knowledge-subscription

# 赋予执行权限（首次）
chmod +x deploy/deploy.sh

# 部署到测试环境
./deploy/deploy.sh staging

# 部署到生产环境
./deploy/deploy.sh production
```

**脚本行为**:
1. 检查 Node.js 和 Wrangler 是否安装
2. 检查 Cloudflare 登录状态（支持 OAuth 和 API Token 两种模式）
3. 检查 `site/index.html` 是否存在
4. 自动创建 Cloudflare Pages 项目（如果不存在）
5. 执行部署并返回公开 URL
6. 部署后自动 curl 验证 HTTP 200
7. 生成部署记录到 `reports/deploy_YYYYMMDD_HHMMSS.log`

### 3.2 定时自动部署脚本（内容更新后自动重新部署）

文件: `deploy/cron-deploy.sh`（已就绪）

```bash
#!/bin/bash
# deploy/cron-deploy.sh
# 用途: 每日自动检查内容更新，如有更新则重新部署销售页
# 建议配合 crontab 每日 08:00 执行

set -euo pipefail
PROJECT_DIR="/home/AgentAdmin/.hermes/shared/dev-team/projects/knowledge-subscription"
BUILD_DIR="$PROJECT_DIR/site"
LAST_DEPLOY_FILE="$PROJECT_DIR/.last_deploy_hash"
LOG_FILE="/tmp/cron-deploy.log"

# 计算当前内容哈希（包含 HTML、CSS、JS）
CURRENT_HASH=$(find site -type f | sort | xargs md5sum | md5sum | awk '{print $1}')

# 如果存在上次哈希且相同，则跳过
if [ -f "$LAST_DEPLOY_FILE" ] && [ "$CURRENT_HASH" == "$(cat $LAST_DEPLOY_FILE)" ]; then
    echo "[$(date)] 内容未变更，跳过部署"
    exit 0
fi

# 执行部署
bash deploy/deploy.sh production

# 记录哈希
echo "$CURRENT_HASH" > "$LAST_DEPLOY_FILE"

echo "[$(date)] 自动部署完成"
```

**赋予权限并加入 crontab**:

```bash
chmod +x deploy/cron-deploy.sh

# 编辑 crontab
crontab -e

# 添加以下行（每天早8点自动部署）
0 8 * * * /home/AgentAdmin/.hermes/shared/dev-team/projects/knowledge-subscription/deploy/cron-deploy.sh >> /tmp/cron-deploy.log 2>&1

# 查看 crontab 是否添加成功
crontab -l | grep cron-deploy
```

### 3.3 GitHub Actions CI/CD 自动部署

创建 `.github/workflows/deploy.yml`:

```yaml
name: Deploy to Cloudflare Pages

on:
  push:
    branches: [main]
  schedule:
    # 每天 UTC 00:00 执行（北京时间 08:00）
    - cron: '0 0 * * *'

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'

      - name: Install Wrangler
        run: npm install -g wrangler

      - name: Deploy to Cloudflare Pages
        env:
          CLOUDFLARE_API_TOKEN: ${{ secrets.CLOUDFLARE_API_TOKEN }}
          CLOUDFLARE_ACCOUNT_ID: ${{ secrets.CLOUDFLARE_ACCOUNT_ID }}
        run: |
          wrangler pages deploy site --project-name=ai-opportunity-radar

      - name: Notify on success
        run: echo "Deployment completed at $(date)"
```

**配置 Secrets**:
1. GitHub Repo -> Settings -> Secrets and variables -> Actions
2. 添加 `CLOUDFLARE_API_TOKEN`（从 Cloudflare Dashboard -> My Profile -> API Tokens 创建）
3. 添加 `CLOUDFLARE_ACCOUNT_ID`

---

## 四、公开 URL 回填位置

部署成功后，Cloudflare 会输出类似 `https://ai-opportunity-radar.pages.dev` 的 URL。

必须回填到以下文件（否则获客链接会 404）:

| 文件 | 回填内容示例 | 说明 |
|------|-------------|------|
| `site/index.html` | 页脚链接、OG url、表单 action | 所有外部链接需要真实域名 |
| `reports/deployment_verification.md` | 验证结果 + 公开 URL | 本任务强制产出文件 |
| `docs/launch_execution_plan.md` | 获客计划中的网站地址 | 否则宣传时没有落地页 |
| `README.md` | 项目主页链接 | 方便 GitHub 访问者 |
| `metrics/launch_channels.csv` | 渠道跟踪参数 | 用于区分各渠道流量来源 |

**回填命令示例**:

```bash
# 假设部署后 URL 为 https://ai-opportunity-radar.pages.dev
URL="https://ai-opportunity-radar.pages.dev"

# 1. 回填到 launch_execution_plan.md
sed -i "s|your-actual-domain.com|$URL|g" docs/launch_execution_plan.md

# 2. 回填到 README.md
sed -i "s|your-actual-domain.com|$URL|g" README.md

# 3. 回填到 metrics/launch_channels.csv（utm_source 参数）
# CSV 中已预留占位，替换为真实域名即可
```

---

## 五、收款/联系入口配置

### 5.1 当前销售页入口状态

| 入口 | 类型 | 状态 | 说明 |
|------|------|------|------|
| 早鸟版 CTA | 按钮 | 占位 | 点击弹出模态框提示"支付渠道配置中" |
| 专业版 CTA | 按钮 | 占位 | 同上 |
| 定制版 CTA | 按钮 | 跳转至表单 | 可直接使用 |
| 联系表单 | mailto | 可用 | 用户提交后打开邮件客户端发送申请 |
| 支付链接 | 外部链接 | 占位 | 指向 xiaobot.net / afdian.net / stripe.com，需替换 |

### 5.2 最小可用收款方案（无需后端，1 小时上线）

**方案 A: 纯 mailto 方案（当前已启用）**
- 用户点击"提交订阅申请" -> 打开邮件客户端 -> 发送预填邮件
- 优点: 零成本、零配置、立即可用
- 缺点: 需要用户有邮件客户端

**方案 B: Tally.so 表单（推荐作为下一步）**

```html
<!-- 在 site/index.html 的 #contact 区域替换原有 form -->
<iframe
  src="https://tally.so/embed/your-form-id?alignLeft=1&hideTitle=1&transparentBackground=1"
  width="100%"
  height="500"
  frameborder="0"
  marginheight="0"
  marginwidth="0"
  title="订阅申请">
</iframe>
```

步骤:
1. 注册 https://tally.so（免费额度 1000 条/月）
2. 创建表单：姓名、联系方式、方案选择、来源
3. 设置通知：表单提交后邮件/Slack 通知你
4. 复制嵌入代码替换 site/index.html 中的 form

**方案 C: 小报童直接收款（目标状态）**
1. 注册小报童 -> 创建专栏 -> 设置价格（¥29/月）
2. 获取专栏链接: `https://xiaobot.net/p/xxx`
3. 替换 site/index.html 中所有指向 xiaobot.net 的占位链接
4. 用户点击"立即订阅" -> 直接跳转小报童 -> 微信支付 -> 完成

---

## 六、宣传平台与获客渠道（>=3个平台）

已规划 6 个核心宣传平台，覆盖中文和海外流量：

| 优先级 | 平台 | 获客成本 | 预期日流量 | 转化率预估 | 内容形式 | 启动日期 |
|--------|------|----------|-----------|-----------|----------|----------|
| **P0** | **知乎** | ¥0-10 | 100-300 | 2% | 深度回答+专栏 | Day 1 |
| **P0** | **小红书** | ¥0-5 | 200-500 | 1.5% | 图文笔记+短视频 | Day 1 |
| **P0** | **即刻** | ¥0 | 50-150 | 3% | 动态+圈子+AMA | Day 1 |
| **P1** | **Twitter/X** | ¥0-20 | 50-200 | 2% | Thread+互动 | Day 2 |
| **P1** | **V2EX** | ¥0 | 30-100 | 5% | 项目分享 | Day 2 |
| **P1** | **微信社群** | ¥0 | 20-50 | 5% | 价值输出 | Day 2 |

详细获客策略、每日执行计划、风险预案见 `docs/launch_execution_plan.md`。
渠道 UTM 追踪链接见 `metrics/launch_channels.csv`。

---

## 七、7天获客执行计划

已制定完整的 7 天获客执行计划，包含：
- Day 1: 部署日 + 内容基建（知乎/小红书/即刻账号准备）
- Day 2: 内容爆发（多平台同步发布）
- Day 3: 社群深耕 + 技术博客
- Day 4: 广告投放准备 + A/B 测试
- Day 5: 付费推广启动（小红书薯条）
- Day 6: 裂变增长（推荐奖励 + AMA）
- Day 7: 复盘与放大（数据复盘 + 下周计划）

完整计划见 `docs/launch_execution_plan.md`。

---

## 八、广告投放前置条件

### 8.1 必须准备清单

| 条件 | 状态 | 说明 | 责任人 | 截止日 |
|------|------|------|--------|--------|
| 公开可访问的网站 | 等待授权 | 部署到 Cloudflare Pages，有 HTTPS | 用户 | Day 0 |
| 支付通道 | 等待授权 | 小报童专栏链接就绪 | 用户 | Day 1 |
| 转化追踪 | 建议配置 | Google Analytics 或百度统计 | dev-monitor | Day 2 |
| 广告素材 | 模板已就绪 | 3-5 套图文素材（小红书 3:4） | dev-deploy | Day 4 |
| 日预算 | 已确定 | ¥50-100/天测试 | dev-deploy | — |
| 测试资金 | 已确定 | ¥200 启动资金 | dev-deploy | — |

### 8.2 平台开户要求

**小红书薯条**:
- 个人号即可投放
- 最低充值 ¥100
- 审核时间：即时
- 适合测试素材效果

**知乎知+**:
- 个人/企业账号均可
- 需要实名认证
- 最低充值 ¥1000
- 适合加热已有爆款回答

**Twitter Ads**:
- 需要海外支付方式（Visa/Mastercard）
- 最低充值 $50
- 适合海外市场测试

---

## 九、验证命令（部署前/后必须执行）

### 9.1 部署前验证

```bash
cd /home/AgentAdmin/.hermes/shared/dev-team/projects/knowledge-subscription

# 1. 检查销售页存在且大小合理
ls -lh site/index.html
# 期望: 文件存在，大小 > 15KB

# 2. 检查 HTML 结构完整性
python3 -c "
from html.parser import HTMLParser
class Validator(HTMLParser):
    def error(self, message): raise Exception(message)
with open('site/index.html', 'r') as f:
    Validator().feed(f.read())
print('HTML 语法检查通过')
"

# 3. 检查关键内容是否存在
grep -q '¥29' site/index.html && echo '定价存在: 通过'
grep -q 'handleSubmit' site/index.html && echo '表单逻辑存在: 通过'
grep -q 'viewport' site/index.html && echo '响应式存在: 通过'
grep -q 'mailto' site/index.html && echo '联系入口存在: 通过'

# 4. 检查部署脚本语法
bash -n deploy/deploy.sh && echo '部署脚本语法: 通过'
bash -n deploy/cron-deploy.sh && echo '定时脚本语法: 通过'

# 5. 检查脚本权限
[ -x deploy/deploy.sh ] && echo 'deploy.sh 可执行: 通过'
[ -x deploy/cron-deploy.sh ] && echo 'cron-deploy.sh 可执行: 通过'

# 6. 本地预览
python3 -m http.server 8080 --directory site &
# 打开浏览器访问 http://localhost:8080
```

### 9.2 部署后验证

```bash
# 假设部署后的 URL
URL="https://ai-opportunity-radar.pages.dev"

# 1. HTTP 200 检查
curl -s -o /dev/null -w "%{http_code}\n" "$URL"
# 期望: 200

# 2. 关键内容检查
curl -s "$URL" | grep -o 'AI Opportunity Radar' | head -1
curl -s "$URL" | grep -o '¥29' | head -1
curl -s "$URL" | grep -o 'handleSubmit' | head -1

# 3. 移动端 viewport 检查
curl -s "$URL" | grep -q 'viewport' && echo '移动端适配: 通过'

# 4. 响应头检查（确认 HTTPS + Cloudflare）
curl -I "$URL" 2>/dev/null | grep -E '(HTTP/2|cloudflare|cf-ray)'

# 5. 端到端转化测试
URL_WITH_UTM="https://ai-opportunity-radar.pages.dev?utm_source=zhihu&utm_medium=answer&utm_campaign=launch"
curl -s "$URL_WITH_UTM" | grep -q 'AI Opportunity Radar' && echo 'UTM 链接落地正常: 通过'

# 6. 表单字段存在性检查
curl -s "$URL" | grep -o '<input' | wc -l
# 期望: >= 3 个输入字段
```

---

## 十、当前部署状态

| 检查项 | 状态 | 说明 |
|--------|------|------|
| 销售页 HTML | 就绪 | site/index.html (30KB+)，含定价/表单/FAQ/CTA/OG标签/响应式 |
| 部署脚本 | 就绪 | deploy/deploy.sh (4.8KB)，可执行，已修复 whoami 检测bug |
| 定时脚本 | 就绪 | deploy/cron-deploy.sh，待加入 crontab |
| CI/CD 配置 | 待配置 | .github/workflows/deploy.yml 模板已提供 |
| Cloudflare 账号 | 未授权 | 需用户执行 `wrangler login` 或提供 API Token |
| 支付渠道 | 未配置 | 需用户注册小报童/爱发电并替换链接 |
| 联系信息 | 占位符 | 微信/邮箱为占位，需替换为真实信息 |
| 公开 URL | 未生成 | 部署成功后自动生成 .pages.dev 域名 |
| 自定义域名 | 可选 | 建议后续购买 .com/.cn 域名 |
| 部署验证报告 | 已更新 | 见 reports/deployment_verification.md |
| 获客计划 | 已就绪 | 见 docs/launch_execution_plan.md |
| 渠道清单 | 已就绪 | 见 metrics/launch_channels.csv |

**已知问题修复**:
- 2026-05-22: 修复 deploy.sh 中 `wrangler whoami` 在未登录时返回 exit 0 导致误判为已登录的 bug。现在同时检测 API Token 环境变量和 whoami 输出中的 "not authenticated" 字符串。

**结论**: 技术层面全部就绪，BLOCKED_BY_USER 等待账号授权。用户完成授权后 5 分钟内可上线。

---

## 十一、快速上线 checklist（用户侧）

用户按以下步骤操作，预计 30 分钟可完成上线：

```
1. 注册 Cloudflare 账号 (5min)
   -> https://dash.cloudflare.com/sign-up

2. 安装 Wrangler 并登录 (5min)
   -> npm install -g wrangler && wrangler login

3. 注册小报童专栏（至少一个支付渠道）(10min)
   -> https://xiaobot.net -> 创建专栏 -> 定价 ¥29/月

4. 替换销售页占位信息 (5min)
   -> 编辑 site/index.html: 微信、邮箱、支付链接

5. 运行部署脚本 (3min)
   -> ./deploy/deploy.sh production

6. 记录公开 URL 并回填 (2min)
   -> 更新 launch_execution_plan.md、README.md

7. 验证部署 (5min)
   -> curl 检查 + 浏览器访问 + 手机端检查
```

---

## 十二、故障排除

| 问题 | 原因 | 解决方案 |
|------|------|----------|
| `wrangler: command not found` | Node.js 或 wrangler 未安装 | `npm install -g wrangler` |
| `wrangler login` 无反应 | 终端不支持浏览器弹出 | 复制输出的 URL 手动在浏览器打开 |
| 部署后 404 | 项目名已存在但属于其他账号 | 换一个 PROJECT_NAME 或删除旧项目 |
| 页面中文乱码 | HTML 未指定 charset | 确认 `<meta charset="UTF-8">` 存在 |
| 表单提交无反应 | mailto 被浏览器阻止 | 检查用户是否安装了邮件客户端；或改用 Tally.so |
| 支付链接跳转后 404 | 占位链接未替换 | 按 2.3 节替换为真实小报童/爱发电链接 |
| `not authenticated` 错误 | API Token 无效或过期 | 重新在 Dashboard 创建 Token 并 export |

---

**文档维护**: dev-deploy
**下次更新时机**: 用户完成授权并首次部署后，更新此文件中的状态和 URL。
**任务ID**: 5fc6593c
