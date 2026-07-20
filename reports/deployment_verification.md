# Deployment verification（task 24f44a36）

## 公开URL验证结果
- URL: https://aunomira-lab.github.io/knowledge-subscription/
- 部署平台: GitHub Pages
- git commit: 5360b1d `deploy: refresh subscription landing page task 24f44a36`
- 验证命令: `curl -L -s -o /tmp/ks_index_live.html -w '%{http_code}' https://aunomira-lab.github.io/knowledge-subscription/ && grep -c '首周目标：50线索' /tmp/ks_index_live.html`
- 实际结果: HTTP 200；页面大小 21506 bytes；本轮 marker `首周目标：50线索` 命中 1 次。
- 结论: 公开 URL 可访问，并已确认远端页面包含本轮更新后的销售页内容。

## 已验证内容
- 页面包含 AI赚钱机会雷达、¥29/月、¥99/月、¥499/次。
- 页面包含订阅/联系入口 `mailto:contact@ai-radar.dev`。
- 页面包含 GitHub Pages 部署说明、广告投放前置条件、合规边界。

## 未完成授权
- Cloudflare Pages: `wrangler whoami` 返回未登录，需要 `wrangler login` 后才能部署备用 Cloudflare Pages。
- 真实收款/自动开通: 需要用户提供支付和客服账号；未授权前只能走人工预售，不宣称自动扣款完成。

## 回填位置
- `site/index.html` og:url/footer 已回填 GitHub Pages URL。
- `docs/launch_execution_plan.md` 部署路径已回填 GitHub Pages URL。
- `metrics/launch_channels.csv` 每个平台发布后继续回填 `url_or_location` 字段。
