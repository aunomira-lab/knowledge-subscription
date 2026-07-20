# Deployment blockers

Status: BLOCKED_BY_USER
Task: 24f44a36

## 当前状态

本地销售页、部署脚本、7天获客计划和渠道 CSV 已准备好。当前已知公开 URL 为：

https://aunomira-lab.github.io/knowledge-subscription/

但是本次运行环境无法代表用户完成平台账号授权、收款实名认证或社交平台发帖授权；因此真实生产更新若需要 push/平台发布，必须由用户授权后执行，不得把未授权上线写成完成。

## 需要用户授权清单

1. GitHub Pages 或 Cloudflare Pages 发布权限：
   - GitHub：授权本机 SSH key 或执行 `gh auth login`；确认 Pages source。
   - Cloudflare：授权账号并创建 Pages 项目，output directory=`site`。
2. 收款入口：提供小报童、知识星球、微信/支付宝收款码、Stripe Payment Link、LemonSqueezy 或 Ko-fi 链接。
3. 客服入口：确认 `contact@ai-radar.dev` 是否可收信；若不可用，提供真实邮箱/微信。
4. 社交发布授权：知乎、小红书、即刻/微信群至少 3 个账号的发布或人工代发。
5. 广告投放前置条件：完成实名认证、隐私政策、退款规则，并先拿到 20 个自然线索和 ≥5% 试读付费转化。

## 授权后执行

```bash
cd /home/AgentAdmin/.hermes/shared/dev-team/projects/knowledge-subscription
bash deploy/deploy_github_pages.sh
bash deploy/verify_public_url.sh
```

## 公开 URL 候选回填
- Cloudflare Pages 候选：https://ai-money-radar.pages.dev/knowledge-subscription/
- GitHub Pages 历史候选：https://aunomira-lab.github.io/knowledge-subscription/
真实投放前必须用用户授权账号验证 200 状态并回填最终公开 URL。
