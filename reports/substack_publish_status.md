# Substack 发布队列监控报告

## 自动化进度

- Hermes Kanban `dev-team`: `todo=0`、`ready=0`、`running=0`、`blocked=0`、`done=26`；无可 dispatch 的 Substack 自动化任务，本轮未触发 `dispatch`。
- 内容生成脚本存在并已运行：`python3 projects/knowledge-subscription/scripts/generate_substack_issue.py --auto`，exit=0。
- Social publisher CLI 可用并已运行：`auto-process` 本轮处理 `0` 条；`status`/`credentials-check` 已复核。
- 最终决策保持 `PIVOT-GO`：内容生成全自动，Substack 发布为半自动/人工最终确认；不得伪装已发布。

## 已自动生成

本轮已生成 4 个 Substack 内容草稿：

- `/home/AgentAdmin/.hermes/shared/content/substack_drafts/2026-05-24_你以为AI只会聊天它正在偷偷拉开普通人的_free_post.md`
- `/home/AgentAdmin/.hermes/shared/content/substack_drafts/2026-05-24_你以为AI只会聊天它正在偷偷拉开普通人的_paid_deep_dive.md`
- `/home/AgentAdmin/.hermes/shared/content/substack_drafts/2026-05-24_你以为AI只会聊天它正在偷偷拉开普通人的_video_script_60s.md`
- `/home/AgentAdmin/.hermes/shared/content/substack_drafts/2026-05-24_你以为AI只会聊天它正在偷偷拉开普通人的_video_script_3min.md`

## 已排队 / 队列状态

Social publisher 全局队列：

- `PENDING_REVIEW`: 9
- `READY_MANUAL_PUBLISH`: 6
- `NEEDS_CREDENTIALS`: 2
- Substack 平台项总数：4
- knowledge-subscription 项目总数：2

knowledge-subscription / Substack 当前队列：

- `smp_knowledge-subscription_substack_20260507_162525_583863_88aa81` — `PENDING_REVIEW` — 知识订阅测试newsletter
- `smp_knowledge-subscription_substack_20260511_163903_466090_5dc431` — `NEEDS_CREDENTIALS` — Test Newsletter - 1778517543；缺失 `publication_url`、`api_key`/可用发布凭证或登录态

## 已发布

- `PUBLISHED`: 0
- 本轮没有自动发布成功记录；未执行 `mark-published`。

## 待人工

- 审核 `PENDING_REVIEW` 内容，确认是否进入手动发布。
- 对可发布草稿执行人工 Substack 编辑器检查、点击 Publish，并在发布后提供真实 Substack URL 执行标记。
- 当前 Substack 仍按半自动发布路径运行：系统可生成草稿/Outbox，但最终发布确认需要人工完成。

## 缺凭证

- `NEEDS_CREDENTIALS`: 全局 2 条，其中 knowledge-subscription / Substack 1 条。
- Substack/newsletter/upstack 平台已启用，但 `auto_publish=false`，当前 `can_auto_publish=false`。
- Substack 缺失字段：`publication_url`、`api_key`/可用发布凭证或登录态。

## 需要用户提供/完成的动作

1. `NEEDS_CREDENTIALS`: 提供 Substack Publication URL。
2. `NEEDS_CREDENTIALS`: 提供可用的 Substack 登录态/session cookie，或 API key/发布凭证（如采用可用发布方案）。
3. 完成 Substack 登录状态确认，保证浏览器辅助发布可进入目标 publication。
4. 完成 Stripe Connect/KYC、税务信息、提现账户配置。
5. 确认是否开启 Substack 付费订阅开关，以及免费/付费内容比例。
6. 首次人工发布后，提供真实 Substack post URL，再执行 `mark-published`；在此之前不能标记为已发布。
