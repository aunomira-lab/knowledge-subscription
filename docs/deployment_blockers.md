# deployment_blockers.md

## BLOCKED_BY_USER：自动收款和备用Cloudflare部署授权

销售页和公开URL可验证，但以下事项不能由 dev-deploy 擅自完成，需要用户个人/企业账号授权：

1. 真实收款入口
   - 微信支付/支付宝收款码或小报童/知识星球/Stripe/Paddle 账号。
   - 需要实名或企业主体，不能由 Agent 伪造或代注册。
   - 回填位置：site/index.html、deploy/README.md、metrics/launch_channels.csv。

2. 客服/联系账号
   - 当前使用 contact@ai-radar.dev 作为邮件占位。
   - 若要微信客服、公众号、小红书私信承接，需要提供账号或指定入口。

3. Cloudflare Pages 备用部署
   - 需要 CLOUDFLARE_ACCOUNT_ID。
   - 需要 CLOUDFLARE_API_TOKEN，权限至少 Pages Edit。
   - 脚本：deploy/deploy_cloudflare_pages.sh；缺少环境变量会以 exit 42 明确阻塞。

4. 广告投放账号
   - 小红书/知乎/微信/巨量等广告账户必须用户授权。
   - 未满足 docs/launch_execution_plan.md 中广告前置条件前，不建议投放。

## 非阻塞可执行路径

无需等待用户授权的今日动作：
- 使用 GitHub Pages 公开URL做自然流量预售。
- 用 mailto 联系入口收集意向。
- 人工发送付款方式和样例内容。
- 在 metrics/launch_channels.csv 手动记录渠道线索和转化。
