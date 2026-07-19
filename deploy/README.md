# AI商机雷达销售页部署说明

项目：knowledge-subscription
部署平台：GitHub Pages（首选，静态页免费，可绑定域名）
销售页入口：site/index.html

## 1. 本地预览

```bash
cd /home/AgentAdmin/.hermes/shared/dev-team/projects/knowledge-subscription
python3 -m http.server 8080 --directory site
# 浏览器打开 http://127.0.0.1:8080/
```

## 2. GitHub Pages 部署路径

推荐公开URL：

- 当前可验证URL：`https://aunomira-lab.github.io/knowledge-subscription/`
- 如果迁移仓库：`https://<github_user>.github.io/knowledge-subscription/`

步骤：

1. 用户授权/确认 GitHub 仓库权限：需要能 push 到 `aunomira-lab/knowledge-subscription` 或新建同名公开仓库。
2. 将 `site/index.html` 提交到仓库根目录或配置 Pages 指向 `/site`。
3. 仓库 Settings → Pages：
   - Source: Deploy from a branch
   - Branch: `main`
   - Folder: `/site`（如果GitHub界面不支持 `/site`，则把 site/index.html 同步到 `docs/index.html` 并选 `/docs`）
4. 等待 Pages 构建完成，打开公开URL。
5. 将公开URL回填到：
   - `reports/deployment_verification.md`
   - `docs/launch_execution_plan.md`
   - 宣传渠道所有 UTM 链接

## 3. 可执行部署脚本

本目录包含 `deploy_github_pages.sh`，用于检查文件并在有 git remote 权限时提交。

```bash
cd /home/AgentAdmin/.hermes/shared/dev-team/projects/knowledge-subscription
bash deploy/deploy_github_pages.sh
```

脚本会执行：

- 检查 `site/index.html` 是否存在
- 检查页面是否包含订阅/联系入口、价格、合规提示
- 检查 git remote
- 如果存在 remote：提交变更并提示手动 push
- 如果没有 remote 或没有凭据：退出并提示授权清单

## 4. 收款/联系入口配置

当前页面使用可立即落地的低门槛入口：

- 联系邮箱：`contact@ai-radar.dev`（占位，需用户替换为真实邮箱或表单）
- 轻量版：¥29/月
- 专业版：¥99/月
- 定制报告：¥499/次

正式收款链接优先级：

1. 小报童/知识星球：中文知识付费最短路径，需要用户实名认证和平台账号。
2. 微信/支付宝收款码：最快成交，但需要人工确认订单。
3. Stripe Payment Link / Lemon Squeezy：适合英文 Substack/海外用户，需要主体信息和收款账户。
4. Gumroad：可作为海外备选，需要账号和税务信息。

替换位置：`site/index.html` 中所有 `mailto:contact@ai-radar.dev?...` 链接。

## 5. 广告投放前置条件

未满足以下条件前不建议投放付费广告：

- 公开URL 200可访问，并完成移动端检查。
- 至少发布1份免费样例和3条真实案例内容。
- 收款链路可用：用户能在3步内完成付款或留下联系方式。
- 已配置追踪表：`metrics/launch_channels.csv` 每日更新曝光、点击、线索、付款。
- 已有至少10个自然流量线索或3个付费用户，证明文案不是零转化。
- 明确退款/交付规则，避免知识付费投诉风险。

## 6. 用户账号授权清单

真实上线/收款仍需用户提供：

- GitHub 仓库 push 权限或 Cloudflare/Vercel 项目授权。
- 可公开使用的联系邮箱、微信号或表单链接。
- 微信/支付宝收款码，或小报童/知识星球/Stripe/Lemon Squeezy 链接。
- 如需自定义域名：DNS 管理权限。

阻塞已记录到 `docs/deployment_blockers.md`，不能把“缺少账号授权”伪装成已完成上线。
