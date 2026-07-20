# 部署阻塞与用户授权清单

状态：PARTIALLY_DEPLOYED_WITH_USER_BLOCKERS

公开销售页已可访问并验证 HTTP 200：https://aunomira-lab.github.io/knowledge-subscription/

仍然 BLOCKED_BY_USER 的项目：
1. 真实收款入口：小报童、知识星球、微信/支付宝收款码、Stripe Payment Link 或 Lemon Squeezy。
2. 客服入口：可公开邮箱、微信、Telegram 或飞书表单。
3. 平台账号发布权限：知乎、小红书、微信公众号/社群运营账号。
4. 如需自定义域名，DNS 管理权限或 CNAME 配置授权。
5. 用户确认退款政策、隐私说明、交付 SLA 可公开展示。

授权后立即执行：
```bash
cd /home/AgentAdmin/.hermes/shared/dev-team/projects/knowledge-subscription
PUBLIC_URL="https://aunomira-lab.github.io/knowledge-subscription/" PAYMENT_URL="https://<real-payment-link>" CONTACT_EMAIL="<real-email>" ./deploy/deploy_github_pages.sh
./deploy/verify_public_url.sh https://aunomira-lab.github.io/knowledge-subscription/
```

广告投放仍 blocked_until_prereqs：必须有真实收款、客服入口、自然 PV>=100、咨询>=3。

## 公开 URL 候选回填
- Cloudflare Pages 候选：https://ai-money-radar.pages.dev/knowledge-subscription/
- GitHub Pages 历史候选：https://aunomira-lab.github.io/knowledge-subscription/
真实投放前必须用用户授权账号验证 200 状态并回填最终公开 URL。
