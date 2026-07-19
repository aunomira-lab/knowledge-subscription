# 部署阻塞与用户授权清单

状态：BLOCKED_BY_USER（仅阻塞“真实发布新版本/真实收款”，不阻塞本地销售页与部署文件产出）

## 已完成

- 已创建可上线销售页：`site/index.html`
- 已选择部署平台：GitHub Pages
- 已创建部署说明和部署脚本：`deploy/README.md`, `deploy/deploy_github_pages.sh`
- 已创建7天获客计划和渠道追踪表：`docs/launch_execution_plan.md`, `metrics/launch_channels.csv`
- 已验证历史公开URL可访问：`https://aunomira-lab.github.io/knowledge-subscription/` 返回 HTTP 200

## 仍需用户提供/授权

1. GitHub push 权限：允许将本次 `site/index.html` 变更推送到 Pages 仓库。
2. 真实联系入口：可公开展示的邮箱、微信号、飞书表单、Notion表单或Tally表单。
3. 真实收款入口：微信/支付宝收款码、小报童/知识星球链接、Stripe Payment Link 或 Lemon Squeezy 链接。
4. 如需绑定域名：域名和 DNS 管理权限。
5. 如需投放广告：广告账户、预算上限、素材审核权限。

## 回填位置

- 销售页按钮：`site/index.html` 中的 `mailto:contact@ai-radar.dev`。
- 公开URL：`deploy/README.md`、`docs/launch_execution_plan.md`、`reports/deployment_verification.md`、`metrics/launch_channels.csv`。
- 渠道发布链接：`metrics/launch_channels.csv` 的 `account_or_url` 字段。

## 不可伪装完成的事项

在没有上述授权前，不得声称已完成“新版本真实上线”或“真实收款接入”。当前交付为上线就绪版本，等待账号/收款授权后可执行发布。
