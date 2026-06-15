# knowledge-subscription 项目

**项目ID**: knowledge-subscription  
**定位**: AI赚钱机会雷达 - 知识付费订阅  
**当前任务**: 889b251b 首批可售卖内容样例包

---

## 目录结构

```
.
├── app/
│   └── sample_pack_generator.py    # 内容生成器
├── docs/
│   └── delivery_checklist.md        # 交付清单
├── reports/
│   └── sample_pack/
│       ├── free_preview.md          # 免费试看版
│       ├── premium_catalog.md       # 专业版订阅目录
│       ├── data.json                # 结构化数据
│       └── week1_samples/
│           ├── monday.md
│           ├── tuesday.md
│           ├── wednesday.md
│           ├── thursday.md
│           ├── friday.md
│           ├── saturday.md
│           └── sunday.md
├── tests/
│   └── test_sample_pack.py          # pytest 验证脚本
├── runs/
│   └── 889b251b_result.json          # 任务结果文件
└── README.md
```

---

## 运行方式

### 环境要求

- Python 3.9+ （纯标准库，无外部依赖）

### 生成内容样例包

```bash
# 生成全部文件（强制覆盖）
cd /home/AgentAdmin/.hermes/shared/dev-team/projects/knowledge-subscription
python app/sample_pack_generator.py --all --force

# 检查文件完整性
python app/sample_pack_generator.py --check
```

### 运行测试

```bash
python -m pytest tests/test_sample_pack.py -v
```

### 验证JSON

```bash
python -c "import json; d=json.load(open('reports/sample_pack/data.json')); print(f'JSON OK: {len(d[\"opportunities\"])} opps, {len(d[\"week1\"])} days')"
```

---

## 内容产物

| 文件 | 说明 | 大小 |
|------|------|------|
| free_preview.md | 免费试看版：3个机会深度节选+转化对比表 | ~3KB |
| premium_catalog.md | 专业版目录：8个机会完整SOP+权益+定价+FAQ | ~27KB |
| week1_samples/*.md | 7天日报样例，每天含SOP+行动清单+工具测评 | ~2KB-25KB |
| data.json | 结构化元数据（机会+日报） | ~5KB |

---

## 盈利空间

| 定价 | 月订户数 | 月收入 | 年收 |
|------|----------|--------|------|
| ¥99/月 | 50人 | ¥4,950 | ¥59,400 |
| ¥99/月 | 200人 | ¥19,800 | ¥237,600 |
| ¥799/年 | 100人 | - | ¥79,900 |

---

## 下一步赚钱动作

1. 今天：将 free_preview.md 转图发小红书/即刻/朋友圈
2. 24h内：部署静态销售页到 Cloudflare Pages/Vercel
3. 3天内：开通小报童/Substack付费订阅，设置¥99/月
4. 1周内：分发免费试看版给200+人，收集反馈
5. 2周内：启动早鸟价¥69/月活动（限50人）
6. 1个月内：实现首笔付费订阅收入，验证PMF

---

*项目由 Dev Team 维护 | Verdict: GO (79/100)*
