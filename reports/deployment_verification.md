# Deployment verification（task 24f44a36）

## 公开URL
- URL: https://aunomira-lab.github.io/knowledge-subscription/
- 验证命令: `curl -L -s -o /tmp/ks_index.html -w '%{http_code} %{url_effective}
' https://aunomira-lab.github.io/knowledge-subscription/`
- 最近验证结果: 200 https://aunomira-lab.github.io/knowledge-subscription/
- 说明: 公开URL可访问；本轮本地文件已更新。若要确保远端页面完全等于本轮文件，需要运行 `deploy/deploy_github_pages_24f44a36.sh` 推送本轮提交。

## 未完成授权
- Cloudflare Pages: `wrangler whoami` 返回未登录，需要 `wrangler login`。
- 真实收款/自动开通: 需要用户提供支付和客服账号。

## 回填位置
- `site/index.html` og:url/footer
- `docs/launch_execution_plan.md` 部署路径
- `metrics/launch_channels.csv` 每个平台发布后 `url_or_location` 字段
