# AI Opportunity Radar — 部署说明
# 任务ID: d718d905
# 项目ID: knowledge-subscription
# 更新日期: 2026-06-13

## 当前部署状态

| 项目 | 状态 | 说明 |
|------|------|------|
| 演示环境 | ✅ 已上线 | GitHub Pages: https://aunomira-lab.github.io/knowledge-subscription |
| 生产环境 | ⏳ 待部署 | Cloudflare Pages 等待用户授权 |
| 微信收款 | ⏳ 待开通 | 需用户完成微信商户号/个人号实名 |
| 邮件服务 | ⏳ 待开通 | 需用户注册 Resend/SendGrid |

---

## 部署平台

### 主平台: GitHub Pages (已上线)

- **URL**: https://aunomira-lab.github.io/knowledge-subscription
- **优点**: 免费、无需额外账号、自动构建
- **缺点**: 国内访问速度一般
- **适用阶段**: MVP 验证期

### 生产环境: Cloudflare Pages (推荐)

- **优点**: 全球CDN、国内访问优化、自定义域名、无限流量
- **费用**: 免费
- **预定URL**: https://ai-opportunity-radar.pages.dev

### 备选平台

| 平台 | 适用场景 | 成本 | 复杂度 |
|------|---------|------|--------|
| Cloudflare Pages | 首选生产环境 | 免费 | 低 |
| Vercel | 需要边缘函数 | 免费 | 低 |
| GitHub Pages | 最简单 | 免费 | 最低 |
| 自建服务器 | 高流量/定制 | ¥50-200/月 | 高 |

---

## 部署脚本

### 1. 一键部署脚本

```bash
# 快速部署到 Cloudflare Pages (使用 Wrangler CLI)
./deploy/deploy.sh
```

脚本功能:
- 验证 site/index.html 存在且格式正确
- 检查关键元素完整性
- 自动调用 wrangler 部署
- 生成部署验证报告

### 2. 每日运营定时脚本

```bash
# 每日自动生成报告、检查网站健康、更新运营数据
./deploy/run_daily.sh
```

建议配置 crontab:
```bash
# 每日早上 8:00 执行
0 8 * * * cd /home/AgentAdmin/.hermes/shared/dev-team/projects/knowledge-subscription && bash deploy/run_daily.sh >> /tmp/knowledge-daily.log 2>&1
```

### 3. 定时自动部署脚本

```bash
# 每日检查 site/ 目录变更，有更新则重新部署到 Cloudflare Pages
./deploy/cron-deploy.sh
```

建议配置 crontab:
```bash
# 每日早上 9:00 检查部署
0 9 * * * cd /home/AgentAdmin/.hermes/shared/dev-team/projects/knowledge-subscription && bash deploy/cron-deploy.sh >> /tmp/cron-deploy.log 2>&1
```

---

## 用户账号授权步骤

以下账号需要用户亲自完成（因涉及个人身份认证、实名认证或银行账户绑定）:

| 步骤 | 账号 | 操作 | 紧急度 | 完成标准 |
|------|------|------|--------|----------|
| 1 | GitHub | 创建仓库并推送代码 | 高 | 能推送并触发 Pages 部署 |
| 2 | Cloudflare | 注册并授权 Pages | 高 | 能部署项目并获得公开URL |
| 3 | 微信商户号 | 申请微信支付 | 高 | 能生成收款二维码 |
| 4 | 邮件服务 | 注册 Resend/SendGrid | 中 | 能发送测试邮件 |
| 5 | 微信公众号 | 注册并认证 | 中 | 能发布文章并做跳转 |

### 详细授权步骤

#### 1. GitHub 账号
- 操作: 访问 https://github.com/signup 注册
- 时间: 5分钟
- 风险: 无
- 验证: 登录后能看到个人主页

#### 2. Cloudflare 账号
- 操作: 访问 https://dash.cloudflare.com/sign-up 注册
- 时间: 5分钟
- 风险: 无
- 验证: 登录后能进入 Dashboard

#### 3. 微信商户号
- 操作: 访问 https://pay.weixin.qq.com 申请
- 时间: 1-3工作日
- 风险: 需要身份证、银行卡、负责人
- 备选: 个人号直接收款（金额限制）
- 验证: 能生成收款二维码

#### 4. 邮件服务
- 操作: 访问 https://resend.com 注册并验证域名
- 时间: 10分钟
- 风险: 无
- 免费额度: 3000封/天
- 验证: 能发送测试邮件

#### 5. 微信公众号
- 操作: 访问 https://mp.weixin.qq.com 注册
- 时间: 1-3工作日
- 风险: 需身份认证
- 验证: 能发布文章

---

## 公开 URL 回填位置

部署完成后，将实际 URL 填入以下位置:

1. **site/index.html**
   - 第 6 行: `<meta property="og:url" content="https://YOUR_URL">`
   - 第 279 行: `<p>已部署于 <a href="https://YOUR_URL">GitHub Pages</a>`

2. **reports/deployment_verification.md**
   - 更新“公开 URL”部分

3. **deploy/README.md**
   - 更新“当前部署状态”表格

---

## 收款 / 联系入口

### 当前收款方式

页面使用微信个人号作为收款和联系入口:
- 微信: `AI_Radar_Dev` (占位，待替换)
- 邮箱: `contact@ai-opportunity-radar.com` (占位，待替换)

### 后续升级

1. 接入微信支付商户号
2. 接入 Stripe（海外用户）
3. 接入小报童/爱发电（中文用户习惯）
4. 接入有赞收费（微信生态）

### 联系入口显示位置

销售页已包含:
- 页面中部“立即订阅 / 联系”区块
- 页面底部邮箱链接
- 订阅弹窗内微信二维码占位
- 页面底部即刻/小红书社群指引

---

## 宣传平台

已在销售页和获客计划中明确以下平台:

1. **小红书** (主阵地)
   - 形式: 图文笔记 + 短视频
   - 频率: 每日1条
   - 预期CAC: ¥5-20

2. **知乎** (长尾流量)
   - 形式: 长文回答 + 专栏
   - 频率: 每周3答
   - 预期CAC: ¥2-10

3. **Twitter/X** (英文/跨境海外)
   - 形式: Thread + 截图
   - 频率: 每日2条
   - 预期CAC: $0-5

更多平台详情见 `metrics/launch_channels.csv` 和 `docs/launch_execution_plan.md`

---

## 广告投放前置条件

| 条件 | 状态 | 阻塞项 |
|------|------|--------|
| 微信商户号 | 待办 | 需营业执照或个人实名 |
| 小红书聚光平台开户 | 待办 | 需企业认证 |
| 知乎知+ 开户 | 待办 | 需企业认证 |
| 投放素材 (3张图+1视频) | 就绪 | 无 |
| 落地页 (销售页) | 就绪 | 无 |
| 转化追踪 (UTM参数) | 待办 | 需配置分析工具 |

---

## 快速部署步骤

### 方案A: GitHub Pages (已完成)

当前已通过项目仓库的 GitHub Pages 完成部署，无需额外操作。

### 方案B: Cloudflare Pages (需用户授权)

```bash
# 1. 在项目目录初始化仓库
cd /home/AgentAdmin/.hermes/shared/dev-team/projects/knowledge-subscription/

# 2. 推送到 GitHub (用户需先在 GitHub 创建私有或公开仓库)
git add site/
git commit -m "deploy: sales page for knowledge-subscription"
git push origin main

# 3. 登录 Cloudflare Dashboard
# https://dash.cloudflare.com → Pages → Create a project → Connect to Git

# 4. 选择仓库，构建输出目录设为 site，构建命令留空

# 5. 保存并部署
```

### 方案C: 使用 Wrangler CLI (需登录)

```bash
# 安装 wrangler (若未安装)
npm install -g wrangler

# 登录 Cloudflare (首次需要)
wrangler login

# 部署
wrangler pages deploy site --project-name="ai-opportunity-radar"
```

---

## 验证命令

```bash
# 1. 验证HTML格式
grep -q "<!DOCTYPE html>" site/index.html && echo "✅ HTML格式正确"

# 2. 验证部署脚本语法
bash -n deploy/deploy.sh && echo "✅ 部署脚本语法正确"
bash -n deploy/run_daily.sh && echo "✅ 每日运营脚本语法正确"
bash -n deploy/cron-deploy.sh && echo "✅ 定时部署脚本语法正确"

# 3. 验证当前公开URL可访问
curl -s -o /dev/null -w "%{http_code}" https://aunomira-lab.github.io/knowledge-subscription/
# 预期返回: 200

# 4. 验证销售页关键内容
grep -q "¥29" site/index.html && echo "✅ 定价信息存在"
grep -q "AI Opportunity Radar" site/index.html && echo "✅ 品牌名称存在"
grep -q "立即订阅" site/index.html && echo "✅ 订阅入口存在"
```

---

## 联系人

如果部署过程中遇到问题，请联系: contact@ai-opportunity-radar.com
