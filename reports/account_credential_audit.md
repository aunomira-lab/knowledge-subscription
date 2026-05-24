# Substack 账号/凭证核查与自主推进状态

更新时间(UTC): 2026-05-21T05:50:38.528932+00:00
项目: knowledge-subscription

## 结论
- 已验证 Gmail OAuth token 可用：可以读取 Aunomira Gmail，用于接收/轮询 Substack magic link 或验证邮件。
- 本机 pass vault 中未发现单独的 Substack 登录态/API 凭证/publication URL 条目。
- 已实际尝试访问 `https://substack.com/sign-in`；结果被 Cloudflare/Turnstile 安全验证挡住。此类人机验证不得绕过。
- AI商机雷达已暂停，当前只统计 knowledge-subscription 的 Substack 队列，避免旧项目动作误报。

## 已有权限
- Gmail 登录邮箱: aunomira@gmail.com
- Gmail OAuth: 可刷新、可读取邮箱
- 凭证位置: `pass:google/aunomira/gmail-oauth-token` 与 `pass:google/aunomira/oauth-client-secret`

## 当前 knowledge-subscription Substack 队列
- `smp_knowledge-subscription_substack_20260507_162525_583863_88aa81` — substack — PENDING_REVIEW — 知识订阅测试newsletter
- `smp_knowledge-subscription_substack_20260511_163903_466090_5dc431` — substack — NEEDS_CREDENTIALS — Test Newsletter - 1778517543

## 当前唯一真实用户动作
1. 完成 Substack Cloudflare/Turnstile/登录确认一次，或提供可复用的 Substack 登录态/session cookie/API 发布凭证。
2. 回填/确认 publication URL，例如 `https://<publication>.substack.com`。
3. 如果开启 paid subscription，再完成 Stripe/KYC/税务/提现配置。

## 团队下一步自动动作
- 继续自动生成 free post / paid deep dive / 视频脚本草稿。
- 凭证一旦可用，使用现有 Gmail token 读取登录邮件，进入 publication 配置与草稿发布流程。
- 不再把“Gmail/token缺失”当作阻塞。
