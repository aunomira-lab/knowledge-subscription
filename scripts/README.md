# 知识付费订阅 - 运营工具包

## 目录

```
knowledge-subscription/
├── docs/
│   ├── revenue_experiment_7d.md  # 7天收入实验计划
│   └── kpi_dashboard.md           # 运营看板
├── metrics/
│   └── experiment_tracker.csv     # 实验数据追踪表
└── scripts/
    ├── daily_update.py             # 每日数据更新脚本
    └── README.md                   # 本文件
```

## 快速开始

### 1. 更新每日数据

```bash
# 基本用法
python scripts/daily_update.py --date 2026-04-28 --exposure 100 --clicks 20 --orders 2 --revenue 58

# 完整参数
python scripts/daily_update.py \
  --date 2026-04-28 \
  --exposure 200 \
  --clicks 30 \
  --reads 25 \
  --pricing 10 \
  --orders 3 \
  --revenue 87 \
  --new-paid 3 \
  --total-paid 3 \
  --open-rate 45 \
  --ctr 15 \
  --notes "第一天效果不错"
```

### 2. 查看汇总数据

```bash
python scripts/daily_update.py --summary
```

输出示例:
```
════════════════════════════════════════════
📊 实验数据汇总
════════════════════════════════════════════
  总曝光: 200
  总点击: 30
  点击率: 15.00%
  总订单: 3
  总收入: ¥87
  新付费用户: 3
  转化率: 10.00%
```

## 每日运营流程

### Morning Routine
1. 查看昨日数据 (收入、新订单)
2. 运行汇总检查: `python scripts/daily_update.py --summary`
3. 根据预警调整今日策略

### Evening Routine
1. 收集今日数据 (曝光、点击、订单)
2. 更新CSV: `python scripts/daily_update.py --date YYYY-MM-DD --exposure X --clicks Y ...`
3. 检查是否触发停止/加码条件

### 每周复盘
1. 导出CSV数据到Excel或Notion
2. 分析渠道效果
3. 调整下周内容策略

## 停止/加码决策

脚本会自动检测以下情况:

### 🛑 停止预警
- 7天付费用户 < 3人
- 转化率 < 1%
- 退款率 > 10%

### ⬆️ 加码机会
- 7天付费用户 ≥ 20人
- 转化率 ≥ 5%
- 续订率 ≥ 70%

## 数据字段说明

| 字段 | 说明 | 示例 |
|-----|-----|-----|
| date | 日期 | 2026-04-28 |
| day_of_experiment | 实验天数 | 1-7 |
| exposure | 曝光量 | 200 |
| clicks | 点击量 | 30 |
| content_reads | 内容阅读 | 25 |
| pricing_views | 定价页访问 | 10 |
| orders | 订单数 | 3 |
| revenue | 收入(元) | 87 |
| new_paid_users | 新增付费用户 | 3 |
| total_paid_users | 总付费用户 | 3 |
| open_rate | 打开率(%) | 45 |
| ctr | 点击率(%) | 15 |
| channel_* | 各渠道数据 | 自填 |
| notes | 备注 | 文本 |

## 扩展建议

### 自动化接入
- 对接支付平台API自动获取订单数据
- 对接邮件服务商API获取打开率
- 对接网站统计API获取访问数据

### 可视化升级
- 使用matplotlib/plotly生成趋势图
- 导出到Notion Database
- 搭建Streamlit交互式看板

## 支持

问题反馈: dev-optimizer (小优)  
创建时间: 2026-04-28
