# 24f44a36 部署说明：知识付费订阅销售页

## 部署目标

项目：knowledge-subscription / AI赚钱机会雷达
平台主选：GitHub Pages（当前已有公开URL）
备用平台：Cloudflare Pages（需要用户授权 Token）
公开URL回填位置：
- site/index.html 的 og:url 和页脚
- metrics/launch_channels.csv 的 landing_url
- reports/deployment_verification.md 的验证结果

当前已验证公开URL：
https://aunomira-lab.github.io/knowledge-subscription/

## 本次落地文件

- site/index.html：可上线销售页，含订阅入口、价格、样例、7天获客计划、合规边界。
- deploy/prepare_static_site.sh：打包静态站到 dist/，同步 reports/sample_pack/free_preview.md 供销售页引用。
- deploy/deploy_github_pages.sh：GitHub Pages 部署脚本，默认只部署当前仓库根目录对应页面；不会自动提交未指定文件。
- deploy/deploy_cloudflare_pages.sh：Cloudflare Pages 部署脚本，要求先设置 CLOUDFLARE_ACCOUNT_ID 和 CLOUDFLARE_API_TOKEN。
- deploy/verify_deployment.sh：公开URL和本地文件冒烟验证脚本。
- docs/launch_execution_plan.md：获客平台计划、7天执行、广告投放条件。
- metrics/launch_channels.csv：至少3个平台的渠道计划、UTM和指标。

## 运行/验证命令

```bash
cd /home/AgentAdmin/.hermes/shared/dev-team/projects/knowledge-subscription
bash deploy/prepare_static_site.sh
bash -n deploy/prepare_static_site.sh deploy/deploy_github_pages.sh deploy/deploy_cloudflare_pages.sh deploy/verify_deployment.sh
bash deploy/verify_deployment.sh https://aunomira-lab.github.io/knowledge-subscription/
python3 -m html.parser site/index.html >/dev/null
python3 - <<'PY'
import csv
rows=list(csv.DictReader(open('metrics/launch_channels.csv', encoding='utf-8')))
assert len(rows) >= 3
assert all(r['platform'] and r['landing_url'] for r in rows)
print('launch_channels rows', len(rows))
PY
```

## GitHub Pages 部署步骤（当前可用路径）

1. 确认 GitHub SSH 权限可用：`ssh -T git@github.com`。
2. 仅提交本任务文件，避免污染团队已有改动：
   ```bash
   git add site/index.html deploy/README.md deploy/prepare_static_site.sh deploy/deploy_github_pages.sh deploy/deploy_cloudflare_pages.sh deploy/verify_deployment.sh docs/launch_execution_plan.md docs/deployment_blockers.md metrics/launch_channels.csv reports/deployment_verification.md
   git commit -m "deploy: launch subscription landing page task 24f44a36"
   git push origin main
   ```
3. GitHub Pages 设置：仓库 Settings → Pages → Source 选择 `Deploy from a branch`，Branch 选择 `main` 和 `/root`（或现有 Pages 配置）。
4. 等待 1-3 分钟后运行：
   `bash deploy/verify_deployment.sh https://aunomira-lab.github.io/knowledge-subscription/`
5. 若公开页未更新，检查 GitHub Actions/Pages build 日志。

## Cloudflare Pages 部署步骤（备用，更适合后续自定义域名）

用户/账号授权前置：
1. 提供 Cloudflare 账户，创建 API Token，权限至少包含 Account:Cloudflare Pages:Edit。
2. 在本地/CI 设置：
   ```bash
   export CLOUDFLARE_ACCOUNT_ID="<account_id>"
   export CLOUDFLARE_API_TOKEN="<pages_edit_token>"
   ```
3. 执行：
   ```bash
   bash deploy/prepare_static_site.sh
   bash deploy/deploy_cloudflare_pages.sh
   ```
4. 将输出中的 `https://<deployment>.pages.dev` 回填到 site/index.html、metrics/launch_channels.csv、reports/deployment_verification.md。

## 收款/联系入口

当前可立即运行的低阻塞预售闭环：
- 联系入口：mailto:contact@ai-radar.dev?subject=订阅AI赚钱机会雷达
- 问卷占位：https://wj.qq.com/s2/AI-Radar-2026
- 收款占位：PAYMENT_URL_TO_FILL_AFTER_USER_AUTH

自动收款需要用户提供微信/支付宝/小报童/知识星球/Stripe/Paddle 等账号授权。授权前不得在页面宣称“自动开通”，只能人工收款和交付。

## 广告投放前置条件

付费广告前必须同时满足：
1. 公开URL返回 HTTP 200，页面含订阅CTA和退款边界。
2. 真实收款链接可用，付款后可追踪订单号。
3. 客服入口可响应，首响 SLA < 12h。
4. 至少3篇免费样例内容上线。
5. metrics/launch_channels.csv 能记录 UTM、访问、留资、付费。
6. 页面包含“不承诺收益/非投资建议/数字内容退款边界”。

## 今日赚钱动作

先不等自动支付：把公开URL和 free_preview.md 发到知乎、小红书、即刻/V2EX、微信群，收集50个线索；私信高意向用户先卖 ¥29 早鸟和 ¥499 定制诊断。
