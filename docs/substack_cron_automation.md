# Substack 内容发布 Cron 自动化方案

**更新时间**: 2026-05-11  
**项目**: knowledge-subscription  
**状态**: 已部署

---

## 1. 架构设计原则

### 1.1 核心理念: 不打扰用户
- **无声运行** (`deliver=local`): 内容生成、队列处理、数据收集
- **通知用户** (`deliver=origin`): 异常告警、需要凭证、每日报告

### 1.2 Cronjob 分类

| 类型 | 频率 | deliver | 目的 |
|------|------|---------|------|
| `内容生成器` | 每日 06:00 | local | 静默生成内容草稿 |
| `发布队列处理` | 每日 08:00, 18:00 | local | Substack 定时发布 |
| `每日数据报告` | 每日 09:00 | origin | 向用户汇报 KPI |
| `异常监控告警` | 每 5 分钟 | origin | 实时异常通知 |
| `凭证续期检查` | 每日 00:00 | origin | 提醒即将过期的 API Key |

---

## 2. 已部署的 Cronjobs

### 2.1 内容生成器 (Content Generator)
```yaml
name: ks-content-generator
schedule: 0 6 * * *  # 每日早晨 6 点
deliver: local
no_agent: false
skills: []
prompt: |
  作为 knowledge-subscription 项目的内容生成器，请执行以下任务：
  
  1. 读取 ~/.hermes/shared/dev-team/projects/knowledge-subscription/app/content_generator.py
  2. 生成今日的内容草稿（根据内容支柱轮转）
  3. 保存到 reports/drafts/YYYY-MM-DD/目录
  4. 更新发布队列 (reports/queue/pending.json)
  5. 记录生成日志 (logs/content_gen_YYYY-MM-DD.log)
  
  输出要求:
  - 如果成功：返回生成的文件路径列表
  - 如果失败：详细错误信息
```

### 2.2 发布队列处理 (Publish Queue Processor)
```yaml
name: ks-publish-queue
schedule: 0 8,18 * * *  # 每日 8:00 和 18:00
deliver: local
no_agent: false
skills: []
prompt: |
  处理 Substack 发布队列：
  
  1. 读取 reports/queue/pending.json
  2. 检查是否有待发布的内容
  3. 如果有，输出以下信息：
     - 待发布内容数量
     - 预计发布时间
     - 需要用户确认的内容列表
  4. 更新队列状态
  
  注意：目前阶段发布需要用户手动确认，请输出待确认内容清单。
```

### 2.3 每日数据报告 (Daily Metrics Report)
```yaml
name: ks-daily-report
schedule: 0 9 * * *  # 每日上午 9 点
deliver: origin
no_agent: false
skills: []
prompt: |
  生成 knowledge-subscription 项目的每日运营报告：
  
  1. 读取 metrics/experiment_tracker.csv
  2. 计算以下指标：
     - 昨日数据（曝光、点击、订单、收入）
     - 7日趋势
     - 累计数据
     - 转化率变化
  3. 检查是否触发预警条件
  4. 生成简洁的每日报告
  
  报告格式：
  ```
  📊 每日运营报告 (YYYY-MM-DD)
  
  昨日数据:
  - 曝光: XXX | 点击: XXX | 转化率: X.X%
  - 订单: XXX | 收入: ¥XXX
  
  7日趋势: ↗/↘/→
  
  预警: [如有则列出]
  ```
```

### 2.4 异常监控告警 (Exception Monitor)
```yaml
name: ks-exception-monitor
schedule: */5 * * * *  # 每 5 分钟
deliver: origin
no_agent: true  # 使用脚本模式，无 LLM 成本
script: projects/knowledge-subscription/scripts/health_check.sh
```

### 2.5 凭证续期检查 (Credential Expiry Check)
```yaml
name: ks-credential-check
schedule: 0 0 * * *  # 每日凌晨
deliver: origin
no_agent: false
skills: []
prompt: |
  检查 knowledge-subscription 项目的所有凭证状态：
  
  1. 检查 Substack 登录状态
  2. 检查 Stripe 连接状态
  3. 检查各渠道 API Key 有效性（如有）
  4. 检查域名/证书过期时间（如有自定义域名）
  
  输出要求:
  - 如果所有凭证正常：返回 "所有凭证状态正常"
  - 如果发现问题：详细列出需要处理的项目和截止日期
```

---

## 3. 目录结构

```
projects/knowledge-subscription/
├── cron/                          # Cron 配置备份
│   ├── content_generator.md
│   ├── publish_queue.md
│   ├── daily_report.md
│   ├── exception_monitor.md
│   └── credential_check.md
├── docs/
│   └── substack_cron_automation.md   # 本文档
├── logs/                          # 日志目录
│   ├── cron/                        # Cron 执行日志
│   └── content_gen/                 # 内容生成日志
├── reports/
│   ├── drafts/                      # 内容草稿
│   └── queue/                       # 发布队列
├── metrics/                       # 数据指标
└── scripts/
    ├── health_check.sh              # 健康检查脚本
    ├── daily_update.py              # 数据更新
    └── generate_content_pack.py     # 内容生成
```

---

## 4. 手动管理命令

### 4.1 查看所有 Cronjobs
```bash
# 列出所有 cronjobs
hermes cronjob list

# 或使用工具
python -c "from hermes.cron import list_jobs; print(list_jobs())"
```

### 4.2 检查任务状态
```bash
# 检查特定 cronjob 执行历史
hermes cronjob show <job_id>

# 查看最近执行日志
ls -la ~/.hermes/shared/dev-team/projects/knowledge-subscription/logs/cron/
```

### 4.3 紧急暂停/恢复
```bash
# 暂停所有自动化
hermes cronjob pause ks-content-generator
hermes cronjob pause ks-publish-queue
hermes cronjob pause ks-daily-report

# 恢复
hermes cronjob resume ks-content-generator
hermes cronjob resume ks-publish-queue
hermes cronjob resume ks-daily-report
```

### 4.4 手动触发
```bash
# 立即执行内容生成
hermes cronjob run ks-content-generator

# 立即生成报告
hermes cronjob run ks-daily-report
```

---

## 5. 异常处理 SOP

### 5.1 内容生成失败
1. 检查日志: `logs/content_gen/YYYY-MM-DD.log`
2. 确认模板文件完整
3. 手动重试: `hermes cronjob run ks-content-generator`
4. 若持续失败，检查 API 限额/凭证

### 5.2 发布队列堵塞
1. 检查待发布数量: `cat reports/queue/pending.json`
2. 确认 Substack 登录状态
3. 检查是否需要用户确认的内容
4. 清理过期草稿

### 5.3 凭证过期
1. 收到通知后立即更新
2. 更新完成后验证: `hermes cronjob run ks-credential-check`
3. 记录到 `docs/credential_rotation_log.md`

---

## 6. 截止标准

以下情况需要用户干预：

| 情况 | 响应时间 | 操作 |
|------|----------|-------|
| 连续 3 次内容生成失败 | 24 小时内 | 检查 API 和模板 |
| Stripe 连接中断 | 立即 | 重新连接 Stripe |
| 转化率下降 < 1% | 7 天内 | 审查内容策略 |
| 网络问题导致无法发布 | 4 小时内 | 切换备用方案 |

---

## 7. 安全与隐私

### 7.1 凭证管理
- 所有 API Key 存储在 Hermes 配置中，不硬编码在脚本中
- 定期轮换（建议 90 天）
- 使用最小权限原则

### 7.2 数据保护
- 用户数据不离开本地工作空间
- 日志脱敏：移除个人身份信息
- 定期清理历史日志（保留 90 天）

---

## 8. 扩展计划

### 8.1 短期（1-2 周）
- [ ] A/B 测试不同发布时间
- [ ] 自动生成社交媒体分享文案
- [ ] 数据可视化仪表盘

### 8.2 中期（1-2 月）
- [ ] 多平台发布（知乎、公众号）
- [ ] 用户行为分析
- [ ] 智能推荐最佳发布时间

### 8.3 长期（3-6 月）
- [ ] 多语言内容生成
- [ ] 自动化客户分层运营
- [ ] AI 驱动的内容优化

---

## 9. 常见问题

### Q: 为什么发布需要手动确认？
A: 目前阶段为了保证内容质量，所有内容需要人工审核后才发布。未来可根据质量评估自动化。

### Q: 如何调整发布时间？
A: 编辑对应 cronjob 的 schedule 字段，使用标准 cron 表达式。

### Q: 可以暂停某个类型的内容吗？
A: 可以，修改 content_generator 的配置文件，或直接暂停对应 cronjob。

---

## 10. 联系与协助

- **技术问题**: dev-deploy
- **内容问题**: dev-content
- **策略问题**: dev-architect

---

**最后更新**: 2026-05-11  
**下次审查**: 2026-05-18
