# AI赚钱机会雷达 —— 知识付费订阅

**knowledge-subscription** —— 每天自动收集、验证、拆解 AI 工具、自动化、独立开发者、跨境小生意相关赚钱机会，生成可直接执行的变现简报和线索库。

## 项目概述

本项目是 Dev Team 首个可上线、可收费、可持续运营的微型产品。核心交付物包括：
1. 每日/每周 AI 赚钱机会简报（可售卖内容）
2. 内容样例包（免费试看 + 专业版目录 + 首周日报样例）
3. 可运行的内容生成器（Python 脚本，零依赖）
4. 静态销售页（site/index.html）
5. 运营脚本与监控指标

## 市场调研结论

**Verdict**: GO (79/100)

已通过市场门禁调研：
- 总分 79/100（门槛 70）
- 付费意愿 19/25（门槛 15）
- 风险可控性 11/15（门槛 8）
- LTV/CAC 22:1 ~ 84:1，毛利率 >85%

详见：`/ai-opportunity-radar/market-research/knowledge-subscription/verdict.md`

## 定价假设

| 方案 | 价格 | 权益 |
|------|------|------|
| 免费试看 | ¥0 | 3 个机会节选 |
| 月付 | ¥99/月 | 全部内容 + 会员群 + 基础脚本 |
| 年付 | ¥799/年 | 全部内容 + 1v1 评估 + 完整脚本库 |
| 企业版 | ¥2,999/年 | 5 个账号 + 定制行业雷达 |
| 单次咨询 | ¥499/次 | 1 小时视频 + 定制执行方案 |

## 仓库结构

```
knowledge-subscription/
├── app/
│   ├── sample_pack_generator_v5.py   # 内容样例包生成器（可运行）
│   └── README.md                      # 生成器运行说明
├── reports/
│   ├── sample_pack/                   # 内容样例包
│   │   ├── free_preview_v5.md         # 免费试看版
│   │   ├── premium_catalog_v4.md      # 专业版订阅目录
│   │   ├── data_v5.json               # 结构化数据
│   │   └── week1_samples/             # 首周 7 天日报样例
│   │       ├── monday_v5.md
│   │       ├── tuesday_v5.md
│   │       ├── wednesday_v5.md
│   │       ├── thursday_v5.md
│   │       ├── friday_v5.md
│   │       ├── saturday_v5.md
│   │       └── sunday_v5.md
│   └── pytest_output_994f3629_v2.txt  # 内容质量测试结果
├── docs/
│   ├── delivery_checklist.md           # 交付清单
│   ├── strategy.md                     # 商业策略
│   └── mvp_spec.md                     # MVP 规格
├── site/
│   └── index.html                      # 静态销售页
├── tests/
│   └── test_sample_pack_v5.py         # 内容质量测试脚本
├── content/                            # 已发布的简报内容
├── market-research/                    # 市场调研文件
├── deploy/                             # 部署脚本
└── README.md                           # 本文件
```

## 快速开始

### 1. 生成内容样例包

仅需 Python 3.9+（零第三方依赖）：

```bash
cd /home/AgentAdmin/.hermes/shared/dev-team/projects/knowledge-subscription

# 运行生成器
python app/sample_pack_generator_v5.py

# 验证输出
ls -la reports/sample_pack/free_preview_v5.md
ls -la reports/sample_pack/premium_catalog_v4.md
ls -la reports/sample_pack/week1_samples/*_v5.md
ls -la reports/sample_pack/data_v5.json

# 验证 JSON 完整性
python -c "import json; json.load(open('reports/sample_pack/data_v5.json')); print('JSON OK')"
```

### 2. 运行内容质量测试

```bash
# 安装 pytest（如未安装）
pip install pytest

# 运行测试
pytest tests/test_sample_pack_v5.py -v --tb=short

# 或保存结果到文件
pytest tests/test_sample_pack_v5.py -v --tb=short > reports/pytest_output_994f3629_v2.txt 2>&1
```

### 3. 查看内容

```bash
# 免费试看版（用于引流）
cat reports/sample_pack/free_preview_v5.md

# 专业版目录（用于销售页）
cat reports/sample_pack/premium_catalog_v4.md

# 首周日报样例
cat reports/sample_pack/week1_samples/monday_v5.md
```

## 内容格式

每期简报包含：
1. **机会标题**：一句话说明变现方向
2. **数据支撑**：市场规模、竞品数据、平台信号
3. **执行 SOP**：5 步具体到工具和命令的启动路径
4. **收益测算**：保守/乐观区间 + 毛利率
5. **AI 提示词模板**：可直接复制使用的 Prompt
6. **风险提示**：不承诺收益，公开风险
7. **参考链接**：可追溯的数据来源

## 当前状态

- [x] 市场调研（GO，79/100）
- [x] 内容样例包 v5.0（6 个机会 + 7 天日报 + Prompt 模板）
- [x] 可运行生成器（Python，零依赖）
- [x] 内容质量测试（21 项全部通过）
- [x] 静态销售页（site/index.html）
- [x] 交付清单（docs/delivery_checklist.md）
- [ ] 支付系统接入（微信支付/支付宝）
- [ ] 小报童/Substack 付费专栏开通
- [ ] 首单转化（目标：2 周内 10 人）

## 盈利空间

| 阶段 | 订户数 | 月收入 | 关键动作 |
|------|--------|--------|----------|
| 种子期 | 50 人 | ¥4,950 | 免费试看引流 + 社群转化 |
| 验证期 | 200 人 | ¥19,800 | 小红书/即刻/知乎内容分发 |
| 规模化 | 500 人 | ¥49,500 | 陪跑营 ¥999 + 企业版 |

二次变现：SOP 模板 ¥39-99、单次咨询 ¥499、陪跑营 ¥999/人。

## 贡献

Dev Team 项目。遵循团队宪章协作。

## 许可

内容 © 2026 AI赚钱机会雷达。代码示例采用 MIT License。

---

*Built by the Dev Team • 用 AI 赚钱，一个机会接一个机会*
