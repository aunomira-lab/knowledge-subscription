# knowledge-subscription 内容样例包生成器

**最新任务ID**: 16513ba1  
**项目ID**: knowledge-subscription  
**版本**: v10.0  
**角色**: dev-coder

---

## 功能

一键生成首批可售卖内容样例包，v10版本全面升级：
- 免费试看版报告 (free_preview_v10.md) — 3个高价值机会节选
- 专业版订阅目录 (premium_catalog_v10.md) — 权益/专栏/定价/FAQ
- 首周7天日报样例 (monday_v10.md … sunday_v10.md) — 每日SOP+行动清单+工具测评
- 结构化数据 (data_v10.json) — 含机会、日报、Prompt、代码片段、风险提示
- 交付清单 (docs/delivery_checklist.md) — 完整交付说明、盈利空间、下一步动作

---

## 环境要求

- Python 3.9+（仅需标准库，无第三方依赖）

---

## 运行方式

```bash
cd /home/AgentAdmin/.hermes/shared/dev-team/projects/knowledge-subscription

# 运行 v10 生成器（推荐，当前版本）
python app/sample_pack_generator_v10.py --all

# 强制覆盖已有文件
python app/sample_pack_generator_v10.py --all --force

# 仅验证文件是否存在
python app/sample_pack_generator_v10.py --check

# 旧版本（兼容）
python app/sample_pack_generator_v4.py
python app/sample_pack_generator.py
```

---

## 输出路径

| 文件 | 路径 |
|------|------|
| 免费试看版 | reports/sample_pack/free_preview_v10.md |
| 专业版目录 | reports/sample_pack/premium_catalog_v10.md |
| 周一日报 | reports/sample_pack/week1_samples/monday_v10.md |
| 周二日报 | reports/sample_pack/week1_samples/tuesday_v10.md |
| 周三日报 | reports/sample_pack/week1_samples/wednesday_v10.md |
| 周四日报 | reports/sample_pack/week1_samples/thursday_v10.md |
| 周五日报 | reports/sample_pack/week1_samples/friday_v10.md |
| 周六日报 | reports/sample_pack/week1_samples/saturday_v10.md |
| 周日日报 | reports/sample_pack/week1_samples/sunday_v10.md |
| 结构化数据 | reports/sample_pack/data_v10.json |
| 交付清单 | docs/delivery_checklist.md |

---

## 验证

```bash
# 检查文件存在
ls -la reports/sample_pack/free_preview_v10.md
ls -la reports/sample_pack/premium_catalog_v10.md
ls -la reports/sample_pack/week1_samples/*_v10.md

# 检查JSON有效
python -c "import json; d=json.load(open('reports/sample_pack/data_v10.json')); print(f'JSON OK: {len(d[\"opportunities\"])} opps, {len(d[\"week1\"])} days')"

# 统计字数
wc -m reports/sample_pack/*.md
wc -m reports/sample_pack/week1_samples/*.md

# 运行测试套件
python -m pytest tests/test_sample_pack_16513ba1.py -v
```

---

## 自定义内容

编辑 `app/sample_pack_generator_v10.py` 中的以下变量：
- `OPPORTUNITIES_DB`: 修改/新增机会条目（支持id/title/category/description/数据来源/执行SOP/收益/难度/标签/来源链接/是否免费/提示词模板/代码片段/风险提示/毛利率）
- `WEEK1_SCHEDULE`: 调整日报主题、关联机会、SOP、行动清单、工具测评

重新运行脚本即可生成新版内容。

---

## 市场调研结论

本项目已通过市场调研门禁：
- verdict: **GO (79/100)**
- 路径: `/home/AgentAdmin/.hermes/shared/dev-team/projects/ai-opportunity-radar/market-research/knowledge-subscription/verdict.md`
- 路径: `/home/AgentAdmin/.hermes/shared/dev-team/projects/knowledge-subscription/market-research/knowledge-subscription/verdict.md`
