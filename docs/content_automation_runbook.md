# 内容自动化运维手册

**版本**: 1.0  
**更新日期**: 2026-05-11  
**项目**: knowledge-subscription  
**定位**: 普通人的AI课

---

## 目录

1. [概述](#1-概述)
2. [内容系统](#2-内容系统)
3. [自动化工具](#3-自动化工具)
4. [工作流程](#4-工作流程)
5. [内容标准](#5-内容标准)
6. [故障排查](#6-故障排查)

---

## 1. 概述

### 1.1 目标

让内容生产全自动化，每日/每周自动生成：
- 免费公开发布内容 (Free Post)
- 付费深度内容 (Paid Deep Dive)  
- 新订阅者欢迎邮件 (Welcome Email)
- 短视频口播稿 (Video Script)

### 1.2 输出格式

所有内容输出为 Markdown + YAML Frontmatter，直接兼容 Substack 发布系统。

### 1.3 内容定位

**主题**: 普通人的人工智能课  
**口腔**: 能听懂的大白话，不堆术语，不用英文  
**工具**: 国内可直接使用（豆包、通义千问、文心一言等）

---

## 2. 内容系统

### 2.1 内容支柱（5大主题）

```
├── ai_cognition          # AI基础认知（20%）
│   ├── AI是什么、为什么会胡说
│   ├── 微信内置AI功能
│   └── 判断AI回答靠不靠谱
├── office_productivity   # 办公提效（40%）
│   ├── 信息整理工作流
│   ├── 周报/会议纪要
│   ├── Excel/PPT辅助
│   └── 文档处理
├── content_creation      # 内容创作（25%）
│   ├── 小红书选题
│   ├── 视频脚本生成
│   ├── AI做图
│   └── 客服/FAQ
├── learning_growth       # 学习成长（15%）
│   ├── AI学英语
│   ├── 速读读书法
│   └── 作业辅导
└── trends_analysis       # 趋势解读（10%）
    ├── 中美AI新闻
    ├── 国内工具对比
    └── 行业变化观察
```

### 2.2 内容分层

| 类型 | 定价 | 频率 | 长度 | 主要目标 |
|------|------|------|------|---------|
| Free Post | 免费 | 周3-5篇 | 800-1500字 | 拉新、建立信任 |
| Paid Deep Dive | ¥99/月 | 周1篇 | 3000-5000字 | 深度付费用户 |
| Welcome Email | 免费 | 新订阅 | 1000字 | 新用户引导 |
| Video Script | 配套 | 随Free发布 | 60s-3min | 流量引导 |

### 2.3 发布节奏

```
周一    →  长文发布 (新周期内容)
周二    →  短视频脚本  
周三    →  短文提示
周四    →  案例/工具测评
周五    →  AI周报/趋势
周六    →  社区互动/答疑
周日    →  休息/备稿
```

---

## 3. 自动化工具

### 3.1 主脚本

**`scripts/generate_substack_issue.py`**

核心生成器，支持以下模式：

```bash
# 生成单日完整内容包
python generate_substack_issue.py --day 1

# 生成指定支柱内容
python generate_substack_issue.py --pillar office_productivity --topic 0

# 生成欢迎邮件
python generate_substack_issue.py --type welcome

# 批量生成一周内容
python generate_substack_issue.py --week 1

# 指定输出目录
python generate_substack_issue.py --day 1 --output-dir ./custom_drafts/
```

### 3.2 输出结构

```
content/substack_drafts/
├── YYYY-MM-DD_topic_free_post.md           # 免费文章
├── YYYY-MM-DD_topic_paid_deep_dive.md       # 付费深度文章
├── YYYY-MM-DD_topic_video_script_60s.md     # 60秒视频脚本
├── YYYY-MM-DD_topic_video_script_3min.md   # 3分钟视频脚本
└── YYYY-MM-DD_welcome_email.md             # 欢迎邮件
```

### 3.3 内容包结构

每个内容包包含4个文件：

1. **Free Post** - 免费公开发布
   - YAML Frontmatter (标题、标签、日期)
   - 钩子开头
   - 问题背景
   - 操作步骤
   - 案例分享
   - 常见问题
   - CTA和付费引导

2. **Paid Deep Dive** - 付费深度内容
   - 付费会员标记
   - 专题介绍
   - 详细教程
   - 实战练习
   - 交付物清单

3. **Video Script (60s)** - 短视频脚本
   - 开头(0-10s)
   - 中间(10-45s)
   - 结尾(45-60s)

4. **Video Script (3min)** - 长视频脚本
   - 痛点引入
   - 问题分析
   - 解决方案
   - 案例演示
   - CTA

---

## 4. 工作流程

### 4.1 日常内容生成

```bash
# 每天自动生成当日内容
0 6 * * * cd /path/to/project && python scripts/generate_substack_issue.py --day $(date +%u)

# 审核后发布
# 1. 打开生成的md文件
# 2. 人工检查调整
# 3. 复制到Substack编辑器
# 4. 设置发布时间
```

### 4.2 周期性内容

```bash
# 每周一生成新周内容
0 5 * * 1 cd /path/to/project && python scripts/generate_substack_issue.py --week $(date +%V)

# 每月生成欢迎邮件更新
0 4 1 * * cd /path/to/project && python scripts/generate_substack_issue.py --type welcome
```

### 4.3 发布前检查清单

- [ ] 标题是否吸引人
- [ ] 内容是否符合"少英文少术语"原则
- [ ] 提示词是否可直接复制使用
- [ ] 案例是否贴近普通人生活
- [ ] CTA是否清晰
- [ ] 付费内容是否有足够价值差异化

---

## 5. 内容标准

### 5.1 写作风格指南

**必须做到**：
- 开头先解释背景，不预设读者懂AI
- 使用"你"而不是"大家"，增加亲近感
- 每篇必须有可立即复制的提示词
- 案例必须贴近普通人工作/生活
- 结尾必须有明确CTA

**禁止使用**：
- "不会用就被淘汰"类焦虑话术
- "一键赚钱"等过度承诺
- 英文术语不加解释
- 国外工具作为主推荐

### 5.2 CTA模板

**免费到付费转化**：
```markdown
---

**想要更系统地学习？**

本文只是入门级技巧。如果你想掌握完整的AI工作系统，
欢迎订阅我的付费专栏。

[**立即订阅**](https://your-substack.substack.com/subscribe)
```

**互动CTA**：
```markdown
---

**你学会了吗？**

在评论区分享你的使用心得，
点赞最高的3条评论，我会专门出教程解答。
```

### 5.3 提示词模板库

脚本内置多种提示词模板，根据主题自动匹配：
- 信息整理模板
- 周报生成模板
- 会议纪要模板
- 小红书选题模板
- 口播稿模板

---

## 6. 故障排查

### 6.1 常见问题

| 问题 | 可能原因 | 解决方法 |
|------|---------|---------|
| 生成内容重复 | 话题索引超出范围 | 检查 --topic 参数 |
| 提示词不匹配 | 主题关键词不在库中 | 手动调整或扩展模板 |
| 内容过于模板化 | 算法随机性不足 | 增加随机组合策略 |
| 输出格式错误 | 特殊字符未转义 | 检查YAML语法 |

### 6.2 维护命令

```bash
# 测试生成
python scripts/generate_substack_issue.py --day 1 --output-dir /tmp/test

# 清理旧草稿（保留最近30天）
find content/substack_drafts -name "*.md" -mtime +30 -delete

# 验证输出格式
python -c "import yaml; yaml.safe_load(open('content/substack_drafts/file.md').read().split('---')[1])"
```

### 6.3 扩展开发

如需添加新内容支柱：

1. 在 `CONTENT_PILLARS` 字典中添加新支柱
2. 定义该支柱的 `topics` 列表
3. 在 `生成方法` 中添加对应的提示词模板
4. 测试生成结果

---

## 附录

### A. 快速参考卡

```bash
# 今天的内容
generate_substack_issue.py --day $(date +%u)

# 本周内容
generate_substack_issue.py --week $(date +%V)

# 特定主题
generate_substack_issue.py --pillar office_productivity --topic 0
```

### B. 目录结构

```
projects/knowledge-subscription/
├── scripts/
│   └── generate_substack_issue.py    # 本文档主角
├── content/
│   └── substack_drafts/               # 自动生成的草稿
└── docs/
    └── content_automation_runbook.md   # 本手册
```

### C. 联系与反馈

如遇到问题或需要新功能，请提交反馈至：
- 项目仓库: knowledge-subscription
- 主要负责人: dev-coder

---

*最后更新: 2026-05-11*  
*版本: 1.0*
