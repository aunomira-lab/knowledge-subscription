# knowledge-subscription 首批可售卖内容样例包

|**项目ID**: knowledge-subscription  
|**任务ID**: 889b251b  
|**市场调研结论**: Verdict: GO (79/100) | 允许进入开发与上线  
|**执行角色**: dev-coder

|---

## 项目简介

本项目产出一套可直接售卖的知识付费内容样例包：
- 免费试看版报告（引流、普及、种子用户获取）
- 专业版订阅目录（权益说明、定价、常见问题）
- 首周日报样例（7天专业版日报）
- 结构化数据与可运行生成器

|---

## 目录结构

```
.
├── app/
│   ├── sample_pack_generator.py          # 主生成器（可运行，生成无版本号文件）
│   └── sample_pack_generator_v12.py    # 备份（生成带版本号文件）
├── docs/
│   └── delivery_checklist.md             # 交付清单
├── reports/
│   └── sample_pack/
│       ├── free_preview.md                 # 免费试看版
│       ├── premium_catalog.md              # 专业版目录
│       ├── data.json                       # 结构化数据
│       └── week1_samples/
│           ├── monday.md                     # 周一：AI客服
│           ├── tuesday.md                    # 周二：数据工具
│           ├── wednesday.md                  # 周三：社媒变现
│           ├── thursday.md                   # 周四：面试陪跑
│           ├── friday.md                     # 周五：复盘
│           ├── saturday.md                   # 周六：工具测评
│           └── sunday.md                     # 周日：90天路线图
└── tests/
    ├── test_sample_pack_current.py         # 主测试脚本（当前版本）
    ├── test_sample_pack.py                 # 历史测试脚本
    └── test_sample_pack_v12.py             # 备份测试（带版本号）
```

|---

## 如何运行

### 环境要求
- Python 3.9+（仅需标准库）

### 生成所有交付物

```bash
# 进入项目目录
cd /home/AgentAdmin/.hermes/shared/dev-team/projects/knowledge-subscription

# 生成所有文件（强制覆盖）
python app/sample_pack_generator.py --all --force
```

### 检查生成结果

```bash
python app/sample_pack_generator.py --check
```

### 运行测试

```bash
python tests/test_sample_pack_current.py
```

或

```bash
python -m pytest tests/test_sample_pack_current.py -v
```

|---

## 盈利测算

| 定价 | 月订户数 | 月收入 | 年收 |
|------|----------|--------|------|
| ¥99/月 | 50人 | ¥4,950 | ¥59,400 |
| ¥99/月 | 200人 | ¥19,800 | ¥237,600 |
| ¥799/年 | 100人 | - | ¥79,900 |

测算依据: verdict.md GO (79/100)，LTV/CAC 22-84:1，毛利率>85%。

|---

## 下一步赚钱动作

1. 立即：将 free_preview.md 转图片/长图，发小红书/即刻/知乎引流
2. 24h内：部署静态销售页（Vercel/Cloudflare Pages）
3. 3天内：开通小报童/Substack付费订阅，设¥99/月
4. 1周内：在200+目标人群分发免费试看版，收集反馈
5. 2周内：早鸟价¥69/月限50人，验证PMF

|---

**最后更新**: 2026-06-08  
**负责人**: Dev Team - dev-coder
