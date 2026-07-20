# Deployment blockers / 用户授权清单（task 24f44a36）

状态：BLOCKED_BY_USER（仅限真实收款、自动开通、Cloudflare Pages；GitHub Pages 公开URL当前可访问）

## 已可执行
- 静态销售页：`site/index.html`
- GitHub Pages 公开URL验证脚本：`deploy/verify_public_url_24f44a36.sh`
- 人工预售入口：`mailto:contact@ai-radar.dev`
- 7天获客计划：`docs/launch_execution_plan.md`

## 仍需用户授权/提供
1. 真实客服入口：邮箱或微信二维码/企微链接。
2. 收款入口至少一种：小报童、知识星球、微信收款码、支付宝、Stripe、PayPal。
3. 支付后自动开通方式：小报童专栏、邮件列表、知识星球、Notion/飞书权限或自建会员系统。
4. Cloudflare Pages 备用上线：执行 `wrangler login`，确认账号、项目名、域名。
5. 退款/隐私政策确认：未交付全退，已交付数字内容按平台规则处理。
6. 若需要投广告：提供广告平台账号、预算上限、投放地区和素材审核授权。

## 不能宣称完成的部分
- 未接入真实自动扣款。
- 未自动创建会员账号。
- 未完成 Cloudflare Pages 授权上线。
- 未验证真实付款后的自动交付链路。

## 公开 URL 候选回填
- Cloudflare Pages 候选：https://ai-money-radar.pages.dev/knowledge-subscription/
- GitHub Pages 历史候选：https://aunomira-lab.github.io/knowledge-subscription/
真实投放前必须用用户授权账号验证 200 状态并回填最终公开 URL。
