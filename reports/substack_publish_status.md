# Substack 发布队列监控报告

## 自动化进度

- Hermes Kanban dev-team：todo=0、ready=0、running=0、blocked=0、done=26；diagnostics 无活跃问题。本轮无可 dispatch 的 ready/todo 任务。
- 内容生成脚本可用，`python3 projects/knowledge-subscription/scripts/generate_substack_issue.py --auto` 已执行成功。
- Social publisher CLI 可用：`auto-process` 执行成功但 processed=0；`status` 与 `credentials-check` 已完成。
- 最终决策仍为 PIVOT-GO / 半自动发布：内容生成、Markdown 格式化、草稿/outbox 可自动化；Substack 最终 Publish 与发布后 mark-published 仍需人工或有效登录态/凭证。
- 发布边界不变：当前不能伪装为已发布；真实发布需 Substack Publication URL、登录态/session 或人工复制确认。

## 已自动生成

本轮已生成 4 个 Substack 内容草稿：

- `/home/AgentAdmin/.hermes/shared/content/substack_drafts/2026-06-13_从单次提示词到可复用AI工作流一套可审计的_SOP_设计_free_post.md`
- `/home/AgentAdmin/.hermes/shared/content/substack_drafts/2026-06-13_从单次提示词到可复用AI工作流一套可审计的_SOP_设计_paid_deep_dive.md`
- `/home/AgentAdmin/.hermes/shared/content/substack_drafts/2026-06-13_从单次提示词到可复用AI工作流一套可审计的_SOP_设计_video_script_60s.md`
- `/home/AgentAdmin/.hermes/shared/content/substack_drafts/2026-06-13_从单次提示词到可复用AI工作流一套可审计的_SOP_设计_video_script_3min.md`

主题：从单次提示词到可复用AI工作流：一套可审计的 SOP 设计法。

## 已排队 / 已发布 / 待人工

- 已排队：social publisher 本轮未处理出新的可发布项；`auto-process` 返回 processed=0。
- 当前队列：17 条旧记录，状态为 PAUSED_BY_USER=15、REJECTED=2；其中 Substack=4，knowledge-subscription 相关 2 条均为 REJECTED，不作为本轮可自动发布对象推进。
- 已发布：没有检测到真实 Substack 已发布记录；未执行 mark-published。
- 待人工：真实 Substack 发布处于 `READY_MANUAL_PUBLISH` / `NEEDS_CREDENTIALS` 边界。

## 缺凭证 / 状态码

- Substack / newsletter / upstack：配置中 `auto_publish=false`，当前不能自动发布。
- Webhook：缺 `webhook_url`。
- X/Twitter：缺 x-cli credentials/tooling。
- 当前 Substack 真实发布状态：`NEEDS_CREDENTIALS` 或 `READY_MANUAL_PUBLISH`。
- 本轮没有 Publication URL、API key、可用登录态/session cookie 或可自动发布适配器凭证，因此没有也不能宣称已发布。

## 需要用户提供或完成的动作

1. Substack Publication URL。
2. Substack 可用登录态/session cookie，或明确选择纯人工复制发布。
3. 如启用付费订阅：完成 Stripe Connect/KYC、税务信息、提现账户配置。
4. 确认 Substack 付费开关与订阅价格策略。
5. 人工发布首篇后，提供真实 Substack post URL，系统才能记录/标记已发布。

如果暂时只做内容打磨和内部样稿，无需额外用户动作。
