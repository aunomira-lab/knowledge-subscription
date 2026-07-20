# AI商机雷达销售页部署说明（task 24f44a36）

目标：把 `site/index.html` 发布为可访问销售页，承接免费试读、¥29/月早鸟订阅、¥99/月专业订阅和 ¥499/次定制咨询。

## 已选部署平台

首选：GitHub Pages
- 仓库：`git@github.com:aunomira-lab/knowledge-subscription.git`
- 静态站点目录：`site/`
- 当前公开 URL：`https://aunomira-lab.github.io/knowledge-subscription/`
- 生产 URL 回填位置：`.deployed_url`、`reports/deployment_verification.md`、`site/index.html` 的 `og:url`

备用：Cloudflare Pages
- Framework：None / Static HTML
- Build command：空
- Build output directory：`site`
- Root directory：仓库根目录

## 本地预览

```bash
cd /home/AgentAdmin/.hermes/shared/dev-team/projects/knowledge-subscription
python3 -m http.server 8787 --directory site
# 打开 http://127.0.0.1:8787/
```

## 一键验证

```bash
cd /home/AgentAdmin/.hermes/shared/dev-team/projects/knowledge-subscription
python3 scripts/validate_24f44a36_deployment.py
bash -n deploy/deploy_github_pages.sh deploy/run_daily_subscription_ops.sh deploy/verify_public_url.sh
```

## 部署脚本

```bash
cd /home/AgentAdmin/.hermes/shared/dev-team/projects/knowledge-subscription
bash deploy/deploy_github_pages.sh
```

脚本会：
1. 运行 `python3 scripts/validate_24f44a36_deployment.py` 检查销售页、收款/联系入口、渠道 CSV 和广告前置条件。
2. 检查 GitHub remote 是否可访问。
3. 在具备 GitHub push 权限时提交并推送本任务相关文件：`site/index.html`、`deploy/`、`docs/launch_execution_plan.md`、`metrics/launch_channels.csv`、`scripts/validate_24f44a36_deployment.py`、`reports/deployment_verification.md`、`.deployed_url`。
4. 调用 `deploy/verify_public_url.sh` 验证公开 URL，并写入 `reports/deployment_verification.md`。
5. 如果缺少账号授权，则写入 `docs/deployment_blockers.md`，状态为 `BLOCKED_BY_USER`，不得伪装为已上线。

## 用户账号授权步骤

GitHub Pages 需要用户完成：
1. 确认 `aunomira-lab/knowledge-subscription` 仓库存在且 Pages 已开启。
2. 给本机 SSH key 授权仓库写权限，或执行 `gh auth login` 并允许 push。
3. Settings -> Pages：Source 选择 `Deploy from a branch`，branch=`main`，folder=`/site`；若 GitHub 不支持 `/site` 作为 Pages 源，则改用 GitHub Action 把 `site/` 上传为 Pages artifact。
4. 部署成功后把最终公开 URL 写入 `.deployed_url` 并重新运行 `bash deploy/verify_public_url.sh`。

Cloudflare Pages 需要用户完成：
1. 登录 Cloudflare -> Workers & Pages -> Create -> Pages。
2. 连接 GitHub 仓库，Output directory 填 `site`。
3. 完成首次部署，复制 `*.pages.dev` 或自定义域名到 `.deployed_url`。

## 收款/联系入口

当前可立即冷启动的低阻塞方案：
- 销售页统一入口：`mailto:contact@ai-radar.dev`。
- 人工回复微信/支付宝收款码、小报童、知识星球、Stripe Payment Link、LemonSqueezy 或 Ko-fi 链接。
- 付款备注邮箱；24 小时内发送试读包和当周简报。

正式支付替换位置：
- `site/index.html` 所有 `mailto:contact@ai-radar.dev?...`。
- 中文用户优先：小报童/知识星球/微信收款；海外用户优先：Stripe Payment Link/LemonSqueezy/Ko-fi。

## 定时运营脚本

```bash
cd /home/AgentAdmin/.hermes/shared/dev-team/projects/knowledge-subscription
bash deploy/run_daily_subscription_ops.sh
```

建议 crontab：

```cron
15 9 * * * cd /home/AgentAdmin/.hermes/shared/dev-team/projects/knowledge-subscription && bash deploy/run_daily_subscription_ops.sh >> logs/daily_subscription_ops.log 2>&1
```

脚本每日检查公开 URL、生成运营日报，并提醒执行获客动作、记录线索和收入。

## 广告投放前置条件

未满足以下条件前，不允许付费投放：
1. 公开 URL 返回 200；
2. 真实收款链接或收款码可用；
3. 客服邮箱、隐私政策、退款边界已写明；
4. 自然流量至少 20 个线索；
5. 试读到付费转化率 ≥ 5%；
6. 文案不承诺稳赚、不暗示投资收益；
7. 平台账号实名认证和投放资质由用户确认。
