# AI商机雷达 - 部署说明

**项目ID**: knowledge-subscription  
**任务ID**: d718d905  
**部署角色**: dev-deploy (deployer)  
**更新日期**: 2026-06-08

---

## 当前部署状态

| 项目 | 状态 | 说明 |
|------|------|------|
| 销售页 site/index.html | ✅ 已完成 | 包含收款入口、订阅表单、UTM跟踪 |
| GitHub Pages 公开站点 | ✅ 已上线 | https://aunomira-lab.github.io/knowledge-subscription/ |
| Cloudflare Pages 备选 | ⏳ 待账号 | 需用户提侜 Cloudflare 邮箱 |
| 自定义域名 | ⏳ 待购买 | 可选，先用免费子域名试运行 |
| 微信/支付宝收款 | ⏳ 待实名认证 | 需用户提侜身份证和银行卡信息 |
| 广告账户 | ⏳ 待实名 | 小红书/知乎/微信广告平台 |

---

## 部署平台

### 主选平台：GitHub Pages（已上线）

- **成本**: 免费
- **中国访问**: 可访问（可能稍慢，建议配合 CDN）
- **自定义域名**: 支持
- **自动 HTTPS**: 支持
- **维护成本**: 零
- **当前公开 URL**: https://aunomira-lab.github.io/knowledge-subscription/

### 备选平台 A：Cloudflare Pages

- **成本**: 免费（每月 500 次构建）
- **中国访问**: 快（全球 CDN）
- **自定义域名**: 支持
- **自动 HTTPS**: 支持
- **优势**: 无需维护服务器

### 备选平台 B：Vercel

- **成本**: 免费（个人项目）
- **中国访问**: 一般
- **自定义域名**: 支持
- **自动 HTTPS**: 支持

---

## 用户账号授权步骤

### 必须授权（P0）

1. **GitHub 账号**
   - 用途: 当前已自动部署到 GitHub Pages
   - 状态: 已通过平台账号完成
   - 结果: 公开 URL 可访问

2. **微信收款实名认证**
   - 用途: 微信收款码收款
   - 注册: 打开微信 → 我 → 服务 → 收款码 → 申请商家收款码
   - 需要: 身份证正反面、银行卡信息
   - 时间: 1-3 工作日
   - 费用: 免费申请，提现手续费 0.6%

3. **小报童创作者注册**
   - 用途: 微信生态内付费订阅
   - 注册: https://xiaobot.net → 微信扫码登录
   - 需要: 微信实名
   - 费用: 平台抽成 10%
   - 操作: 创建专栋 → 设置定价 → 复制链接填回 site/index.html

4. **爱发电创作者注册**
   - 用途: 支付宝/微信打赏支持
   - 注册: https://afdian.net → 微信扫码登录
   - 需要: 微信实名
   - 费用: 平台抽成 6%
   - 操作: 创建专页 → 复制链接填回 site/index.html

### 建议授权（P1）

5. **Cloudflare 账号**
   - 用途: 更快的全球访问速度
   - 注册: https://dash.cloudflare.com/sign-up
   - 需要: 邮箱
   - 费用: 免费
   - 操作: 注册 → 创建 Pages 项目 → 部署 site 目录

6. **小红书企业号**
   - 用途: 广告投放
   - 注册: 小红书 App → 我 → 创佚中心 → 更多服务 → 专业号中心
   - 需要: 营业执照或个人微信实名
   - 费用: 免费注册

7. **知乎广告账户**
   - 用途: 知+广告投放
   - 注册: https://www.zhihu.com → 我的 → 创作中心 → 知+广告
   - 需要: 实名认证
   - 费用: 免费注册

8. **Brevo 邮件服务**
   - 用途: 自动发送每日简报、收费提醒
   - 注册: https://www.brevo.com/
   - 费用: 免费 300 邮件/天
   - 替代方案: 可先用微信公众号/个人邮箱

---

## 部署步骤

### 方式一：命令行部署（推荐）

```bash
# 1. 进入项目目录
cd /home/AgentAdmin/.hermes/shared/dev-team/projects/knowledge-subscription

# 2. 运行部署脚本
bash scripts/deploy-github-pages.sh

# 或使用 Cloudflare（需先安装 wrangler）
bash scripts/deploy.sh
```

### 方式二：GitHub Actions 自动部署

```yaml
# .github/workflows/deploy.yml
name: Deploy to GitHub Pages

on:
  push:
    branches: [main]
  workflow_dispatch:

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Deploy
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./site
```

### 方式三：一键脚本部署

```bash
# 运行已写好的部署脚本
bash /home/AgentAdmin/.hermes/shared/dev-team/projects/knowledge-subscription/scripts/deploy.sh

# 或
bash /home/AgentAdmin/.hermes/shared/dev-team/projects/knowledge-subscription/deploy/deploy.sh
```

---

## 常见操作

```bash
# 检查部署状态
curl -s -o /dev/null -w "%{http_code}" https://aunomira-lab.github.io/knowledge-subscription/

# 检查关键元素
curl -s https://aunomira-lab.github.io/knowledge-subscription/ | grep -o '商机雷达'

# 本地预览
cd /home/AgentAdmin/.hermes/shared/dev-team/projects/knowledge-subscription/site
python3 -m http.server 8080
# 然后访问 http://localhost:8080

# 检查脚本语法
bash -n deploy/deploy.sh
bash -n deploy/cron-deploy.sh
bash -n deploy/validate-deployment.sh
bash -n deploy/run_daily.sh
bash -n deploy/activate-contact.sh
```

---

## 环境变量

如果部署到 Cloudflare Pages，在控制台配置：

| 变量名 | 说明 | 是否必填 |
|--------|------|----------|
| `EMAIL_WEBHOOK` | 邮箱收集后发送到的第三方服务 | 否 |
| `ANALYTICS_ID` | Google Analytics / Plausible 统计 ID | 否 |
| `STRIPE_PK` | Stripe 公开钥匙（后续支付上线后） | 否 |

---

## 安全注意事项

- 所有表单数据请通过 HTTPS 传输
- 生产环境应将邮箱数据发送到可靠后端（如 Airtable / Notion / Brevo）
- 定期更新依赖包
- 收款码不要直接嵌入到页面公开源码中（使用模态弹窗或加载）

---

## 监控与运维

- 使用 GitHub Pages 内置访问统计
- 使用 UptimeRobot 监控站点可用性（免费）
- 每月查看流量和购买转化率
- 每日运营脚本: `bash deploy/run_daily.sh`
- 健康检查: `bash scripts/health_check.sh`

---

## 收款/联系入口

| 入口 | 类型 | 状态 | 说明 |
|------|------|------|------|
| 微信收款码 | 即时收款 | 待激活 | 页面占位符已设置，需用户提侜收款码图片 |
| 小报童 | 定期订阅 | 待激活 | 链接已占位: https://xiaobot.net/p/ai-radar-2026 |
| 爱发电 | 打赏支持 | 待激活 | 链接已占位: https://afdian.net/a/ai-radar-2026 |
| 邮箱意向登记 | 意向收集 | ✅ 已上线 | 页面表单可提交，当前存储于 localStorage |
| 联系邮箱 | 客服 | 占位 | contact@ai-radar.dev（需替换为真实邮箱） |
| 微信号 | 社群 | 占位 | AI-Radar-2026（需替换为真实微信号） |

---

## 宣传平台

已确定至少 7 个宣传平台计划（详见 docs/launch_execution_plan.md）：

1. **知乎答案 + 专栏** — 长文引流
2. **小红书笔记** — 短图文种草
3. **微信公众号** — 深度文章 + 邮件列表沉淀
4. **Twitter/X** — 英文受众、全球游民
5. **GitHub** — 开源模板引流零成本
6. **Indie Hackers** — 英文社区沉淀
7. **Product Hunt** — 发布日活动

---

## 链接

- [GitHub Pages 文档](https://docs.github.com/en/pages)
- [Cloudflare Pages 文档](https://developers.cloudflare.com/pages/)
- [Wrangler CLI 文档](https://developers.cloudflare.com/workers/wrangler/)
- [Vercel 文档](https://vercel.com/docs)

---

*本文档由 dev-deploy 维护。有问题请升级至 Dev Team 或联系小电。*
