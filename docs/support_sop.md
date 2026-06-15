# 知识订阅运营 SOP（标准作业程序）

**项目**: knowledge-subscription
**版本**: 2.0
**更新日期**: 2026-06-15
**责任人**: dev-optimizer (profitability-analyst)

---

## 1. 日常运营流程

### 每日内容生产标准

1. **08:00** 自动运行报告生成脚本
   ```bash
   cd /home/AgentAdmin/.hermes/shared/dev-team/projects/knowledge-subscription
   python app/report_generator.py
   ```
2. **08:30** 运营人员审核内容：检查可执行性、去除过期机会、补充个人见解
3. **09:00** 审核通过后，发送到订阅用户群体
4. **09:30** 同步发布到公开平台（即刻/小红书/Twitter）做引流

### 每日数据录入

1. **21:00** 从各平台导出当日数据
2. **21:15** 填写 `metrics/experiment_tracker.csv`
   ```bash
   # 检查当日数据是否已录入
   tail -5 /home/AgentAdmin/.hermes/shared/dev-team/projects/knowledge-subscription/metrics/experiment_tracker.csv
   ```
3. **21:30** 更新 `docs/kpi_dashboard.md`
4. **22:00** 检查预警灯是否触发

### 每周复盘

1. **周日 22:00** 统计本周数据
   ```bash
   # 计算本周总收入
   awk -F',' 'NR>1 && $2>=1 && $2<=7 {sum+=$10} END {print "本周总收入: ¥", sum}' /home/AgentAdmin/.hermes/shared/dev-team/projects/knowledge-subscription/metrics/experiment_tracker.csv
   ```
2. 计算：收入、获客、转化、续订、CAC、LTV
3. 对比目标，记录偏差和原因
4. 制定下周优化动作

---

## 2. 收入追踪 SOP

### 每日收入检查

1. 检查微信收款码/支付宝收款记录
2. 核对小报童后台订单（若已接入）
3. 在 `metrics/experiment_tracker.csv` 记录收入金额和渠道
   ```bash
   # 检查当日收入
   grep "$(date +%Y-%m-%d)" /home/AgentAdmin/.hermes/shared/dev-team/projects/knowledge-subscription/metrics/experiment_tracker.csv | awk -F',' '{sum+=$10} END {print "当日收入: ¥", sum}'
   ```
4. 更新 `docs/kpi_dashboard.md` 收入数据

### 收入异常处理

| 异常类型 | 触发条件 | 响应动作 | 升级路径 |
|----------|----------|----------|----------|
| 收入突然下降 >50% | 当日收入低于昨日的50% | 检查平台封禁、收款码可用性 | L2技术运维 |
| 收入突然上涨 >200% | 当日收入高于昨日的200% | 检查是否有刷单、活动机器人 | L3主管决策 |
| 未收到应付款 | 用户已付款但未录入 | 检查用户付款状态，私聊确认 | L1一线支持 |

---

## 3. 用户增长 SOP

### 获客检查清单

- [ ] 每日至少发布 1 条内容到至少 3 个平台
- [ ] 每日至少在 1 个群内互动
- [ ] 每日至少回复 3 条用户评论/私信
- [ ] 每周至少发布 1 条「用户口碑」到社媒
- [ ] 每周至少测试 1 个新渠道

### 转化检查清单

- [ ] 群内每日推送限时优惠
- [ ] 高意向用户每日 1对1私聊
- [ ] 体验卡用户付费前 3天提醒
- [ ] 月度续订前 7天发送续订优惠

---

## 4. 内容质量 SOP

### 内容三检原则

1. 可执行：每条机会必须包含可操作步骤
2. 可验证：每条机会必须有可以核实的信息源
3. 可量化：每条机会必须有收入参考或时间成本估算

### 内容迭代流程

- 收集反馈 → 标记优化点 → 下期调整 → 验证打开率变化

### 内容验证命令

```bash
# 检查昨日报告质量
python /home/AgentAdmin/.hermes/shared/dev-team/projects/knowledge-subscription/tests/test_report_generator_v2.py
# 检查内容是否满足三检原则
grep -c "可执行" /home/AgentAdmin/.hermes/shared/dev-team/projects/knowledge-subscription/reports/daily/*.md
grep -c "收入" /home/AgentAdmin/.hermes/shared/dev-team/projects/knowledge-subscription/reports/daily/*.md
```

---

## 5. 平台合规 SOP

### 封禁防范

- 不发布违法信息、证券建议、医疗健康类内容
- 不使用刷量软件、自动评论机器人
- 所有外链内容先用自己域名过滤
- 微信收款码备份 2 个，切换时间 <5分钟

### 实名认证备份

- 微信收款码已实名认证
- 小报童账户已实名认证
- 备用支付方式：支付宝收款码

---

## 6. 财务对账 SOP

### 每日对账

- 收款码记录 vs tracker.csv 金额
- 支付平台记录 vs tracker.csv 金额
- 差异 > ¥0 则立即排查

### 每日对账命令

```bash
# 统计tracker.csv当日总收入
awk -F',' 'NR>1 && $1=="'$(date +%Y-%m-%d)'" {sum+=$10} END {print "tracker当日收入: ¥", sum}' /home/AgentAdmin/.hermes/shared/dev-team/projects/knowledge-subscription/metrics/experiment_tracker.csv
```

### 每月对账

- 统计当月收入、退款、折扣
- 计算毛利率、运营利润率
- 生成月度收入报告

---

## 7. 客户支持响应与升级路径

### 响应时效标准

| 问题类型 | 响应时间 | 备注 |
|----------|----------|------|
| 普通咨询 | 2小时内 | 工作日 |
| 付费用户问题 | 30分钟内 | 5×24响应 |
| 技术故障 | 15分钟内 | 启动排查 |
| 重大事故 | 5分钟内 | 立即升级 |

### 升级路径

1. **L1 一线支持**：处理常见咨询、账户问题、内容疑问
   - 联系方式: 微信群/私聊
   - 处理时间: 工作日 2h内
   - 转升条件: 同一问题用户重复提问 >2 次 → 升级至 L2

2. **L2 技术运维**：处理系统故障、支付异常、数据问题
   - 联系方式: 工单/邮件
   - 处理时间: 4h内
   - 转升条件: 系统故障影响付费用户 → 立即升级至 L3

3. **L3 主管决策**：处理退款争议、重大投诉、平台封禁
   - 联系方式: 微信/飞书
   - 处理时间: 工作日 2h内
   - 转升条件: 涉及法律风险 → 立即升级至人工/上级

4. **转交人工**：当AI无法解决或用户明确要求时，立即转交人工处理
   - 联系方式: 微信私聊
   - 处理时间: 5分钟内响应
   - 备注: 不能让用户等待超过15分钟

### 升级触发条件汇总

| 触发条件 | 处理动作 | 升级目标 |
|----------|----------|----------|
| 同一问题重复提问 >2 次 | 记录并转升 | L2 |
| 用户明确要求退款或补偿 | 记录并转升 | L3 |
| 涉及平台合规风险 | 直接升级并通知上级 | L3 |
| 系统故障影响付费用户 | 立即升级并启动事故响应 | L3 |
| 用户明确要求人工处理 | 立即转交 | 人工/上级 |

---

## 8. 常见问题快速处理表

| 问题 | 判断方法 | 处理动作 | 处理时限 |
|------|----------|----------|----------|
| 用户未收到简报 | 检查发送日志 | 重新发送并补偿1期 | 30分钟 |
| 收款码无法扫码 | 尝试自己扫码测试 | 切换备份收款码 | 5分钟 |
| 内容质量投诉 | 检查具体投诉点 | 记录并下期调整 | 2小时内回复 |
| 退款申请 | 核实购买时间和原因 | 7天内全额退款 | 24小时内处理 |
| 群内纠纷 | 审查涉及内容 | 私信调解或移除 | 5分钟内响应 |

---

## 9. 验证检查

```bash
# 验证运营文件存在
ls -la /home/AgentAdmin/.hermes/shared/dev-team/projects/knowledge-subscription/docs/support_sop.md
ls -la /home/AgentAdmin/.hermes/shared/dev-team/projects/knowledge-subscription/docs/incident_runbook.md
ls -la /home/AgentAdmin/.hermes/shared/dev-team/projects/knowledge-subscription/docs/customer_support.md

# 验证追踪器可读取
wc -l /home/AgentAdmin/.hermes/shared/dev-team/projects/knowledge-subscription/metrics/experiment_tracker.csv
head -2 /home/AgentAdmin/.hermes/shared/dev-team/projects/knowledge-subscription/metrics/experiment_tracker.csv

# 验证看板存在
ls -la /home/AgentAdmin/.hermes/shared/dev-team/projects/knowledge-subscription/docs/kpi_dashboard.md
```

---

**状态**: 运营就绪
**响应标准**: 2h/30min/15min/5min 分级
**升级路径**: L1 → L2 → L3 → 人工/上级
