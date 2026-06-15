# 知识订阅事故处理手册

**项目**: knowledge-subscription
**版本**: 2.0
**更新日期**: 2026-06-15
**责任人**: dev-optimizer (profitability-analyst)

---

## 事故分级

| 级别 | 定义 | 响应时间 | 通知范围 | 影响评定 |
|------|------|----------|----------|----------|
| P0 | 收入中断、订阅系统崩溃、平台封号 | <15分钟 | 全体运营+开发 | 直接影响当日收入 |
| P1 | 内容生成失败、收款码封禁、数据丢失 | <1小时 | 运营+开发 | 影响当日交付 |
| P2 | 打开率下降>50%、客户投诉集中 | <4小时 | 运营 | 影响用户体验 |
| P3 | 单个平台限流、单个用户退款 | <24小时 | 运营 | 局部影响 |

---

## P0 级事故：收入中断

### 触发条件
- 8小时内收入为0且应有付费流水
- 订阅系统无法访问
- 微信/支付宝收款码显示异常
- 小报童后台提示账号异常

### 应急处理
1. **00:00-08:00** 检查微信收款码状态，尝试扫码收款
   ```bash
   # 检查收款码图片是否存在
   ls -la /home/AgentAdmin/.hermes/shared/dev-team/projects/knowledge-subscription/assets/wechat_pay_qr.png
   ```
2. **08:05** 检查支付宝收款码状态
3. **08:10** 如主收款码异常，立即切换到备用收款码
   ```bash
   # 检查备份收款码
   ls -la /home/AgentAdmin/.hermes/shared/dev-team/projects/knowledge-subscription/assets/wechat_pay_qr_backup*.png
   ```
4. **08:15** 更新订阅页面收款码信息
   ```bash
   # 检查销售页是否可访问
   curl -s -o /dev/null -w "%{http_code}" https://aunomira-lab.github.io/knowledge-subscription/
   ```
5. **08:20** 私聊活跃用户，告知临时收款方式
6. **08:30** 记录事故到本手册
7. **08:45** 检查平台封号风险，如异常立即迁移到备用渠道

### 恢复确认
- [ ] 收款码可正常收款
- [ ] 测试支付流程（自己扫码¥0.01测试）
- [ ] 客户可正常订阅
- [ ] 数据已同步到 tracker
- [ ] 记录事故处理记录

### 升级路径
若15分钟内未解决，升级至开发团队主负责人，启动备用支付渠道方案。

---

## P1 级事故：内容生成失败

### 触发条件
- 报告生成脚本报错超过 30分钟
- 生成的报告为空或质量异常低
- 数据库或源文件丢失

### 应急处理
1. 检查脚本运行日志，确认错误原因
   ```bash
   # 检查最新报告是否生成
   ls -la /home/AgentAdmin/.hermes/shared/dev-team/projects/knowledge-subscription/reports/daily/*.md | tail -5
   # 检查脚本运行记录
   python /home/AgentAdmin/.hermes/shared/dev-team/projects/knowledge-subscription/app/report_generator.py 2>&1 | tail -20
   ```
2. 如数据源问题，切换到备份源或人工编写
3. 如脚本崩溃，手动生成简化版报告
4. 发送延迟通知给用户，说明情况
5. 记录故障详情

### 恢复确认
- [ ] 脚本可正常运行
- [ ] 内容质量达标
- [ ] 用户收到正常报告
- [ ] 数据已恢复
- [ ] 记录事故处理记录

### 升级路径
若1小时未解决，升级至开发团队开发人员查看脚本代码问题。

---

## P2 级事故：打开率崩塌

### 触发条件
- 内容打开率下降 >50% 连续 2 天
- 用户退订率突然上涨 >20%
- 收到集中负面反馈 ≥ 5 条

### 应急处理
1. 检查是否是标题党封面问题
2. 检查是否是内容质量问题（广告化、冗余、过时）
3. 检查是否是发送时间问题
4. 采集用户反馈，确认根因
5. 调整内容策略或发送时间
6. 发送调查问卷
7. 更新到 `docs/kpi_dashboard.md`

### 恢复确认
- [ ] 打开率回升至正常范围
- [ ] 用户反馈改善
- [ ] 退订率回落
- [ ] 记录事故处理记录

### 升级路径
若4小时未改善，升级至运营负责人和开发团队讨论产品方向调整。

---

## P3 级事故：单平台限流

### 触发条件
- 单个平台触达量下降 >50%
- 单个平台无法发布内容
- 单个用户大额退款

### 应急处理
1. 检查平台政策是否变更
2. 检查是否触发平台限流机制
3. 调整内容或发布频率
4. 如平台封号风险，减少对该平台依赖
5. 用户退款：主动沟通，记录原因
6. 更新到 `docs/kpi_dashboard.md`

### 恢复确认
- [ ] 平台可正常使用或已迁移
- [ ] 限流原因明确并解决
- [ ] 记录事故处理记录

### 升级路径
若24小时未改善或平台封号，升级至运营负责人。

---

## 通用应急联系方式

| 角色 | 联系方式 | 响应时间 | 备注 |
|------|----------|----------|------|
| 运营负责人 | 微信/飞书 | 工作日 2h内 | 事故总协调 |
| 开发团队 | 工单/邮件 | 4h内 | 技术故障处理 |
| 支付平台客服 | 微信客服/支付宝客服 | 24h内 | 收款码异常 |
| 平台客服 | 平台后台工单 | 24h内 | 平台限流/封号 |

---

## 事故记录模板

```
事故编号：INC-YYYY-MM-DD-NNN
时间：
级别：P0/P1/P2/P3
描述：
影响：
处理过程：
恢复时间：
根本原因：
预防措施：
责任人：
盈利影响：
```

---

## 常用故障排查命令

```bash
# 检查应用是否可访问
curl -s -o /dev/null -w "%{http_code}" https://aunomira-lab.github.io/knowledge-subscription/

# 检查最新报告是否生成
ls -la /home/AgentAdmin/.hermes/shared/dev-team/projects/knowledge-subscription/reports/daily/*.md | tail -1

# 检查追踪器数据完整性
wc -l /home/AgentAdmin/.hermes/shared/dev-team/projects/knowledge-subscription/metrics/experiment_tracker.csv
head -1 /home/AgentAdmin/.hermes/shared/dev-team/projects/knowledge-subscription/metrics/experiment_tracker.csv

# 检查系统磁盘空间
df -h /home/AgentAdmin/.hermes/shared/dev-team/projects/knowledge-subscription/

# 检查运营文件是否存在
ls -la /home/AgentAdmin/.hermes/shared/dev-team/projects/knowledge-subscription/docs/revenue_experiment_7d.md
ls -la /home/AgentAdmin/.hermes/shared/dev-team/projects/knowledge-subscription/docs/kpi_dashboard.md
ls -la /home/AgentAdmin/.hermes/shared/dev-team/projects/knowledge-subscription/docs/support_sop.md
ls -la /home/AgentAdmin/.hermes/shared/dev-team/projects/knowledge-subscription/docs/customer_support.md
```

---

## 预防性维护

### 每日检查（预防P0/P1）
- [ ] 检查收款码图片是否可正常显示
- [ ] 检查最新报告是否已生成
- [ ] 检查磁盘空间是否充足
- [ ] 检查后备文件是否完整

### 每周检查（预防P2/P3）
- [ ] 检查各平台触达量趋势
- [ ] 检查用户反馈是否有集中负面
- [ ] 检查收款码有无异常记录
- [ ] 检查各备份渠道是否可用

---

## 事故后复盘

### 复盘要求
1. 所有P0/P1事故必须在恢复后24小时内完成复盘
2. 复盘报告保存到 `reports/incidents/INC-YYYY-MM-DD-NNN.md`
3. 复盘内容必须包含：根本原因、盈利影响、预防措施
4. 如事故影响收入，必须更新收入预测模型

---

**状态**: 运营就绪
**最近更新**: 2026-06-15
**复核人**: dev-optimizer
