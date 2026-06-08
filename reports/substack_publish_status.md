# Substack 发布队列监控报告

## 自动化进度

- Hermes Kanban dev-team：todo=0、ready=0、running=0、blocked=0、done=26；diagnostics 无活跃问题。本轮无可 dispatch 的 ready/todo 任务。
- 内容生成脚本可用，`python3 projects/knowledge-subscription/scripts/generate_substack_issue.py --auto` 执行成功。
- Social publisher CLI 可用：`auto-process` 执行成功但 processed=0；`status` 与 `credentials-check` 已完成。
- 指定读取项中，`reports/substack_automation_final_decision.md` 与 `docs/substack_cron_automation.md` 不存在；已跳过，不作为错误。
- 发布边界不变：当前只能自动生成内容包；Substack 真实发布仍需账号/Publication URL/登录态或人工确认，不得伪装已发布。

## 已自动生成

本轮已生成 4 个 Substack 内容草稿：

- `/home/AgentAdmin/.hermes/shared/content/substack_drafts/2026-06-07_从单次提示词到可复用AI工作流一套可审计的_SOP_设计_free_post.md`
- `/home/AgentAdmin/.hermes/shared/content/substack_drafts/2026-06-07_从单次提示词到可复用AI工作流一套可审计的_SOP_设计_paid_deep_dive.md`
- `/home/AgentAdmin/.hermes/shared/content/substack_drafts/2026-06-07_从单次提示词到可复用AI工作流一套可审计的_SOP_设计_video_script_60s.md`
- `/home/AgentAdmin/.hermes/shared/content/substack_drafts/2026-06-07_从单次提示词到可复用AI工作流一套可审计的_SOP_设计_video_script_3min.md`

主题：从单次提示词到可复用AI工作流：一套可审计的 SOP 设计法。

## 已排队 / 已发布 / 待人工

- 已排队：social publisher 本轮未处理出新的可发布项；`auto-process` 返回 processed=0。
- 已发布：没有检测到真实 Substack 已发布记录；未执行 mark-published。
- 待人工：真实 Substack 发布处于 `READY_MANUAL_PUBLISH` / `NEEDS_CREDENTIALS` 边界，需要用户提供账号与发布路径后才能继续。
- 旧队列状态：当前队列仍以 PAUSED_BY_USER / REJECTED 为主，不作为本轮可自动发布对象推进。

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
