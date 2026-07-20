# 知识付费订阅销售页部署说明（task 24f44a36）

## 部署平台
首选：GitHub Pages

公开 URL 回填位置：
- `site/index.html` 中的 `og:url` 和 footer
- `reports/deployment_verification.md` 中的验证结果
- 获客帖子中的落地页链接

当前建议公开 URL：`https://aunomira-lab.github.io/knowledge-subscription/`

备用：Cloudflare Pages。当前 `wrangler whoami` 显示未登录，因此 Cloudflare 真实上线需要用户授权，清单见 `docs/deployment_blockers.md`。

## 可执行部署脚本

### 1. 本地预览
```bash
cd /home/AgentAdmin/.hermes/shared/dev-team/projects/knowledge-subscription
bash deploy/local_preview_24f44a36.sh
# 打开 http://127.0.0.1:8788/site/
```

### 2. GitHub Pages 部署
```bash
cd /home/AgentAdmin/.hermes/shared/dev-team/projects/knowledge-subscription
bash deploy/deploy_github_pages_24f44a36.sh
```
脚本动作：
1. 验证 `site/index.html`、`docs/launch_execution_plan.md`、`metrics/launch_channels.csv` 存在。
2. 静态检查 HTML 必备文案、价格、订阅入口、合规声明。
3. 提交本轮部署相关文件到 git（只 add 本任务文件）。
4. push 到 `origin main`。
5. 调用 `deploy/verify_public_url_24f44a36.sh` 检查公开URL。

### 3. Cloudflare Pages 备用部署
```bash
wrangler login
bash deploy/deploy_static_site_24f44a36.sh
```
需要用户提供/授权 Cloudflare 账号，并确认项目名、域名、环境变量。未授权前只能生成脚本和本地预览，不能宣称 Cloudflare 已上线。

## 用户账号授权步骤
1. 提供真实客服邮箱或微信，替换 `contact@ai-radar.dev`。
2. 提供收款入口：小报童/知识星球/微信收款码/Stripe/PayPal/支付宝当面付之一。
3. 若用 GitHub Pages：确认 GitHub 仓库 Pages 已启用 `main` 分支或 Actions 部署。
4. 若用 Cloudflare Pages：执行 `wrangler login`，授权后运行脚本。
5. 提供隐私/退款政策文本；默认规则：未交付全退，已交付数字内容不承诺无条件退款。

## 收款/联系入口
当前上线前可用兜底入口：
- 订阅邮箱：`mailto:contact@ai-radar.dev`
- 早鸟：¥29/月
- Pro：¥99/月
- 定制诊断：¥499/次

授权后需替换为真实链接：
- `PAYMENT_URL_EARLY_BIRD`
- `PAYMENT_URL_PRO`
- `PAYMENT_URL_CUSTOM`
- `LEAD_FORM_URL`

## 定时运营脚本
```bash
# 每天 09:00 运行线索/页面/渠道检查
0 9 * * * /home/AgentAdmin/.hermes/shared/dev-team/projects/knowledge-subscription/deploy/run_daily_launch_ops_24f44a36.sh >> /home/AgentAdmin/.hermes/shared/dev-team/projects/knowledge-subscription/reports/daily_launch_ops.log 2>&1
```

## 广告投放前置条件
只有同时满足以下条件才允许投放广告：
- 公开URL返回 200/301/302。
- 真实收款链接可用，客服入口可回复。
- `metrics/launch_channels.csv` 已连续7天记录曝光、线索、付费、CAC。
- 自然流量累计至少 1000 曝光、50 线索、5 笔付费，或咨询转付费率 ≥10%。
- 页面和素材无保证收益、保本、稳赚等违规承诺。
