# AI 赚钱机会雷达：部署 README

任务：24f44a36  
项目：knowledge-subscription  
平台选择：GitHub Pages（主推，已验证公开 URL），备选 Cloudflare Pages / Vercel。  
当前公开 URL：https://aunomira-lab.github.io/knowledge-subscription/

## 已产出资产
- `site/index.html`：可上线销售页，含价格、订阅入口、样例、FAQ、退款/隐私/风险边界。
- `deploy/deploy_github_pages.sh`：生成可上传静态目录并回填 URL/支付/邮箱。
- `deploy/verify_public_url.sh`：验证公开 URL HTTP 状态和关键页面文案。
- `deploy/run_daily_subscription_ops.sh`：每日获客/运营记录脚本，可放入 crontab。
- `docs/launch_execution_plan.md`：7 天获客执行计划。
- `metrics/launch_channels.csv`：获客渠道、预算、UTM 和广告前置条件。
- `reports/deployment_verification.md`：公开 URL 验证记录。
- `docs/deployment_blockers.md`：用户授权阻塞清单。

## 本地预览
```bash
cd /home/AgentAdmin/.hermes/shared/dev-team/projects/knowledge-subscription
python3 -m http.server 8080 --directory site
# 打开 http://127.0.0.1:8080/
```

## GitHub Pages 部署
已验证 URL：`https://aunomira-lab.github.io/knowledge-subscription/`。

重新生成待上传目录：
```bash
cd /home/AgentAdmin/.hermes/shared/dev-team/projects/knowledge-subscription
PUBLIC_URL="https://aunomira-lab.github.io/knowledge-subscription/" PAYMENT_URL="https://<real-payment-link-after-user-auth>" CONTACT_EMAIL="<real-support-email>" ./deploy/deploy_github_pages.sh
```

脚本会生成 `deploy/dist/index.html`，并替换：
- `PUBLIC_URL_TO_FILL_AFTER_DEPLOY` → `PUBLIC_URL`
- `PAYMENT_URL_TO_FILL_AFTER_USER_AUTH` → `PAYMENT_URL`
- `contact@ai-radar.dev` → `CONTACT_EMAIL`

如果用户授权 GitHub 账号，可用 gh CLI 推送到 Pages 仓库；否则把 `deploy/dist/` 手动上传到 GitHub Pages / Cloudflare Pages / Vercel。

## Cloudflare Pages
1. 登录 Cloudflare Dashboard。
2. Workers & Pages → Create application → Pages → Upload assets。
3. 上传 `deploy/dist/` 或 `site/`。
4. 回填 URL 到 `site/index.html`、`reports/deployment_verification.md`、`metrics/launch_channels.csv`。

## Vercel
```bash
cd /home/AgentAdmin/.hermes/shared/dev-team/projects/knowledge-subscription
npx vercel site --prod
```
需要用户登录 Vercel 并授权项目。

## 用户账号授权步骤
1. GitHub / Cloudflare / Vercel 任一平台登录授权。
2. 真实收款入口：小报童、知识星球、微信/支付宝收款码、Stripe Payment Link 或 Lemon Squeezy。
3. 可公开客服邮箱/微信/Telegram/飞书表单。
4. 如使用自定义域名，提供 DNS/CNAME 配置权限。
5. 确认退款政策、隐私说明、交付 SLA 可公开展示。

## 收款/联系入口
当前销售页可通过 `mailto:contact@ai-radar.dev` 收集意向；自动收款入口仍是 `PAYMENT_URL_TO_FILL_AFTER_USER_AUTH`，必须由用户授权后替换。付款后 24 小时内交付首周内容包或定制报告。

## 定时运营脚本 / crontab
每天 09:10 生成当日获客行动文件：
```bash
(crontab -l 2>/dev/null; echo '10 9 * * * cd /home/AgentAdmin/.hermes/shared/dev-team/projects/knowledge-subscription && ./deploy/run_daily_subscription_ops.sh') | crontab -
```

## 验证命令
```bash
cd /home/AgentAdmin/.hermes/shared/dev-team/projects/knowledge-subscription
./deploy/verify_public_url.sh https://aunomira-lab.github.io/knowledge-subscription/
python3 scripts/validate_24f44a36_deployment.py
```

## 广告投放前置条件
禁止冷启动直接投广告。必须同时满足：公开 URL 200；真实收款入口和客服入口可用；退款/隐私/免责声明可见；自然流量 ≥100 PV 且 ≥3 条咨询；渠道表能记录曝光、点击、咨询、付款、退款。

## 盈利空间判断
市场门禁 GO，score 79/100。首周保守目标：5 单早鸟 ¥29 + 1 单专业 ¥99 + 1 单定制 ¥499 = ¥743；数字内容毛利预估 80%+。若 7 天无付款且深聊 <5，Pivot 到更垂直的 n8n 自动化模板订阅。
