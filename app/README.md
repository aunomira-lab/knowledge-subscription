# knowledge-subscription 内容样例包生成器

**最新任务ID**: e648389a  
**项目ID**: knowledge-subscription  
**版本**: v4.0  
**角色**: dev-coder

---

## 功能

一键生成首批可售卖内容样例包：
- 免费试看版报告 (free_preview_v4.md)
- 专业版订阅目录 (premium_catalog_v3.md)
- 首周7天日报样例 (monday_v4.md ... sunday_v4.md)
- 结构化数据 (data_v4.json)
- 交付清单 (docs/delivery_checklist.md)

---

## 环境要求

- Python 3.9+（仅需标准库，无第三方依赖）

---

## 运行方式

```bash
cd /home/AgentAdmin/.hermes/shared/dev-team/projects/knowledge-subscription/app

# 运行 v4 生成器（推荐）
python sample_pack_generator_v4.py

# 运行旧版 v3 生成器（兼容）
python sample_pack_generator.py
```

---

## 输出路径

| 文件 | 路径 |
|------|------|
| 免费试看版 | ../reports/sample_pack/free_preview_v4.md |
| 专业版目录 | ../reports/sample_pack/premium_catalog_v3.md |
| 周一日报 | ../reports/sample_pack/week1_samples/monday_v4.md |
| 周二日报 | ../reports/sample_pack/week1_samples/tuesday_v4.md |
| 周三日报 | ../reports/sample_pack/week1_samples/wednesday_v4.md |
| 周四日报 | ../reports/sample_pack/week1_samples/thursday_v4.md |
| 周五日报 | ../reports/sample_pack/week1_samples/friday_v4.md |
| 周六日报 | ../reports/sample_pack/week1_samples/saturday_v4.md |
| 周日报 | ../reports/sample_pack/week1_samples/sunday_v4.md |
| 数据文件 | ../reports/sample_pack/data_v4.json |
| 交付清单 | ../docs/delivery_checklist.md |

---

## 验证

```bash
# 检查文件存在
ls -la ../reports/sample_pack/free_preview_v4.md
ls -la ../reports/sample_pack/premium_catalog_v3.md
ls -la ../reports/sample_pack/week1_samples/*_v4.md

# 检查JSON有效
python -c "import json; json.load(open('../reports/sample_pack/data_v4.json')); print('JSON OK')"

# 统计字数
wc -m ../reports/sample_pack/*.md
wc -m ../reports/sample_pack/week1_samples/*.md

# 运行测试套件
cd ..
python -m pytest tests/test_sample_pack.py -v
```

---

## 自定义内容

编辑 `sample_pack_generator_v4.py` 中的以下变量：
- `OPPORTUNITIES`: 修改/新增机会条目
- `SCHEDULE`: 调整日报主题和关联机会

重新运行脚本即可生成新版内容。

---

## 市场调研结论

本项目已通过市场调研门禁：
- verdict: **GO (79/100)**
- 路径: `/home/AgentAdmin/.hermes/shared/dev-team/projects/ai-opportunity-radar/market-research/knowledge-subscription/verdict.md`
- 路径: `/home/AgentAdmin/.hermes/shared/dev-team/projects/knowledge-subscription/market-research/knowledge-subscription/verdict.md`
