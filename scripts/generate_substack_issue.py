#!/usr/bin/env python3
"""High-end Substack content generator for knowledge-subscription.

User direction: produce high-end, deep, reusable-asset content. Do not generate
mass-market "AI only chats / ordinary people gap" topics or low-level office tips
as the main product.
"""
from __future__ import annotations

import argparse
import json
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

BRAND_NAME = "AI工作流深度研究"
BANNED_PATTERNS = ["AI只会聊天", "偷偷拉开普通人", "普通人的差距", "普通人的人工智能课"]

CONTENT_PILLARS: Dict[str, Dict] = {
    "workflow_systems": {
        "name": "系统化AI工作流",
        "description": "把AI从聊天工具升级为可复用业务系统",
        "topics": [
            {
                "title": "从单次提示词到可复用AI工作流：一套可审计的 SOP 设计法",
                "hook": "输入标准、处理步骤、质量门禁、复盘指标四件套",
                "tools": ["Kimi", "飞书多维表格", "腾讯文档", "扣子/Coze"],
                "pain_point": "团队会零散使用AI，但无法复用、交接和验证质量",
                "deliverable": "AI工作流SOP模板 + 质量门禁清单 + 复盘表",
            },
            {
                "title": "把客户话术做成AI知识库：从素材堆积到销售资产",
                "hook": "客户画像、异议库、案例库、跟进节奏的结构化方法",
                "tools": ["飞书知识库", "腾讯文档", "Kimi", "豆包"],
                "pain_point": "销售和客服话术靠个人经验，无法沉淀成团队资产",
                "deliverable": "客户话术知识库结构 + 异议处理SOP + 质检规则",
            },
        ],
    },
    "knowledge_assets": {
        "name": "知识资产与资料库",
        "description": "面向咨询、运营、培训和内容团队的资料资产化",
        "topics": [
            {
                "title": "高价值资料库不是素材库：如何设计能产生收入的知识资产",
                "hook": "从资料收集到交付物包装、定价和迭代的完整链路",
                "tools": ["Notion/飞书", "Kimi长文本", "腾讯元宝", "WPS AI"],
                "pain_point": "资料很多但不可售、不可交付、不可持续更新",
                "deliverable": "资料库分层模型 + 交付物包装清单 + 更新节奏表",
            },
            {
                "title": "选题库的高级做法：用AI建立可持续的内容研究系统",
                "hook": "信号源、证据链、差异化角度、商业化入口",
                "tools": ["RSS", "微信搜一搜", "小红书搜索", "Kimi"],
                "pain_point": "每天找选题，但缺少稳定的研究框架和商业判断",
                "deliverable": "选题库字段设计 + 证据评级规则 + 选题评分表",
            },
        ],
    },
    "automation_ops": {
        "name": "自动化运营与交付",
        "description": "把内容、销售和交付流程做成可运行系统",
        "topics": [
            {
                "title": "AI订阅业务的后台系统：内容生产、审核、发布、交付如何闭环",
                "hook": "从人工创作到半自动发布队列的安全架构",
                "tools": ["GitHub", "Hermes Agent", "Substack", "飞书表格"],
                "pain_point": "内容能写出来，但审核、发布、交付、复盘断裂",
                "deliverable": "发布队列设计 + 审核状态机 + 人工介入清单",
            }
        ],
    },
}

PAID_DEEP_DIVE_TOPICS: Dict[str, Dict] = {
    "workflow_sop": {
        "title": "付费专题：AI工作流SOP资产包——从需求到质量门禁",
        "description": "把一次性AI使用变成团队可复用流程资产",
        "outline": [
            "为什么单个提示词无法形成复利",
            "工作流SOP的五层结构：目标、输入、步骤、验收、复盘",
            "质量门禁：事实核查、格式校验、风险过滤、人工确认",
            "团队交接：角色分工、版本记录、异常处理",
            "商业化包装：如何把SOP变成咨询/培训/订阅交付物",
        ],
        "deliverables": ["工作流SOP模板", "质量门禁清单", "复盘指标表", "异常处理Runbook"],
    },
    "knowledge_base": {
        "title": "付费专题：可售知识库架构——资料、案例、话术、SOP的分层设计",
        "description": "把零散资料整理为可交付、可更新、可定价的知识资产",
        "outline": [
            "素材库、资料库、知识库、交付库的区别",
            "字段设计：来源、证据等级、适用场景、更新时间、输出形态",
            "客户价值映射：哪些内容可以免费，哪些内容值得付费",
            "更新机制：周更、月度复盘、过期淘汰",
            "打包方式：模板包、案例库、诊断表、陪跑服务",
        ],
        "deliverables": ["知识库字段模板", "证据评级规则", "付费交付物包装清单", "更新节奏表"],
    },
}

CTA_TEMPLATES = {
    "engagement": [
        "如果你已经有一个真实业务场景，可以用本文模板先做一版，再用质量门禁逐项检查。",
        "建议不要收藏完就结束：把你的一个流程拆成输入、处理、验收、复盘四列，今天先跑一遍。",
    ],
    "free_to_paid": [
        "---\n\n付费版会提供可直接复制的模板、字段表和检查清单，重点不是学概念，而是把它落成可复用资产。"
    ],
}

WELCOME_EMAIL_TEMPLATE = """# 欢迎订阅「AI工作流深度研究」

这里不做浅层工具清单，也不把“改邮件、写纪要、写文案”当成主要卖点。

本订阅聚焦三件事：

1. **系统化工作流**：把AI使用沉淀成可复用SOP。
2. **知识资产**：把资料、案例、话术、模板做成可交付资产。
3. **商业闭环**：让内容生产、审核、发布、交付、复盘能跑起来。

你会看到更多模板、清单、字段设计、质量门禁和真实业务流程拆解。
"""


def assert_quality(text: str) -> None:
    for pattern in BANNED_PATTERNS:
        if pattern in text:
            raise ValueError(f"Banned shallow positioning detected: {pattern}")
    if "今晚就能试" in text or "普通人" in text:
        raise ValueError("Content quality gate failed: mass-market wording detected")


def slugify(title: str) -> str:
    return re.sub(r"[^\w\s-]", "", title)[:28].strip().replace(" ", "_")


class SubstackContentGenerator:
    """Generate high-end Substack content packs."""

    def __init__(self, output_dir: str = "../content/substack_drafts"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def generate_frontmatter(
        self,
        title: str,
        subtitle: str = "",
        description: str = "",
        author: str = BRAND_NAME,
        date: Optional[str] = None,
        tags: Optional[List[str]] = None,
        is_paid: bool = False,
    ) -> str:
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")
        if tags is None:
            tags = ["AI工作流", "知识资产", "深度方法论"]
        return f"""---
title: "{title}"
subtitle: "{subtitle}"
description: "{description}"
author: "{author}"
date: "{date}"
tags: {json.dumps(tags, ensure_ascii=False)}
is_paid: {str(is_paid).lower()}
---

"""

    def _topic(self, pillar: str, topic_index: int) -> Dict:
        pillar_data = CONTENT_PILLARS.get(pillar, CONTENT_PILLARS["workflow_systems"])
        return pillar_data["topics"][topic_index % len(pillar_data["topics"])]

    def generate_free_post(self, pillar: str, topic_index: int = 0, date: Optional[str] = None) -> str:
        pillar_data = CONTENT_PILLARS.get(pillar, CONTENT_PILLARS["workflow_systems"])
        topic = self._topic(pillar, topic_index)
        body = f"""# {topic['title']}

## 先给结论

{topic['pain_point']}，通常不是“工具不会用”的问题，而是缺少一套可复用、可审核、可交接的流程资产。

本文给出一套高端内容/知识产品可用的设计框架：**输入标准 → 处理流程 → 质量门禁 → 复盘指标**。

## 为什么低阶AI用法不够

低阶用法关注“让AI帮我做一件事”，高阶用法关注“让团队以后稳定复用同一套能力”。差别在于：

- 是否有明确输入标准，避免每次都从零解释背景。
- 是否有固定处理步骤，避免结果依赖某个人的临场发挥。
- 是否有质量门禁，避免幻觉、事实错误、格式错误和品牌风险。
- 是否有复盘指标，判断这套流程是不是值得继续投入。

## 可复用框架

### 1. 输入标准

把任务输入拆成五类字段：

- 目标：这次输出要服务哪个业务结果。
- 背景：行业、客户、产品、约束条件。
- 原料：文档、对话、数据、案例、参考链接。
- 输出格式：文章、SOP、清单、话术、表格、JSON。
- 验收标准：事实准确性、可执行性、风险边界、交付对象。

### 2. 处理流程

推荐使用四段式流程：

1. **结构化原料**：先让AI整理事实，不急着生成观点。
2. **生成初稿**：要求明确受众、深度、边界和反例。
3. **质量审查**：逐项检查事实、逻辑、可执行性和商业价值。
4. **资产沉淀**：把可复用部分拆成模板、清单、字段表或SOP。

### 3. 质量门禁

每篇内容发布前至少过四道门：

- 证据门：关键判断是否有来源或业务经验支撑。
- 深度门：是否提供框架、步骤、反例和适用边界。
- 资产门：读者是否能拿走一个模板、清单、字段表或流程图。
- 商业门：是否能连接到咨询、订阅、模板包或陪跑服务。

## 本期可复制资产

- 主题：{topic['hook']}
- 工具：{', '.join(topic['tools'])}
- 交付物：{topic['deliverable']}

## 最小落地动作

今天不要再生成泛泛文章。请选择一个真实业务流程，填完下面四列：

```text
业务目标：
输入材料：
处理步骤：
验收标准：
复盘指标：
```

{CTA_TEMPLATES['engagement'][0]}

{CTA_TEMPLATES['free_to_paid'][0]}
"""
        text = self.generate_frontmatter(
            title=topic["title"],
            subtitle=topic["hook"],
            description=topic["pain_point"],
            date=date,
            tags=[pillar_data["name"], "AI工作流", "知识资产"],
            is_paid=False,
        ) + body
        assert_quality(text)
        return text

    def generate_paid_deep_dive(self, topic_key: str = "workflow_sop", date: Optional[str] = None) -> str:
        topic = PAID_DEEP_DIVE_TOPICS.get(topic_key, PAID_DEEP_DIVE_TOPICS["workflow_sop"])
        outline = "\n".join(f"{i}. {item}" for i, item in enumerate(topic["outline"], 1))
        deliverables = "\n".join(f"- {item}" for item in topic["deliverables"])
        body = f"""# {topic['title']}

## 适合谁

适合已经意识到：单个提示词、工具清单、每日素材都无法形成壁垒的内容团队、咨询顾问、培训主理人和小型业务负责人。

## 核心框架

{outline}

## 关键方法

### A. 先定义资产，而不是先写内容

每一篇深度内容都必须回答：读者看完后能带走什么资产？可以是模板、SOP、检查清单、字段设计、案例库或自动化脚本。

### B. 给每个资产设置质量门禁

资产不是“看起来很完整”的文档，而是能在真实场景中减少决策成本和执行成本的工具。建议门禁：

- 输入是否清楚：别人是否知道该填什么。
- 输出是否稳定：换一个人执行结果是否接近。
- 风险是否可控：是否标注不能自动化、不能发布、需要人工确认的环节。
- 价值是否可感知：是否能节省时间、降低错误、提升转化或支持收费。

### C. 建立更新机制

高端内容的价值来自持续校准。每个资产都要有：版本号、最近更新时间、适用范围、废弃条件。

## 本期交付物

{deliverables}

## 付费读者作业

选择一个你准备收费或反复交付的场景，写出：

```text
目标用户：
他们原来的低效流程：
你提供的新流程：
可复用资产：
质量门禁：
收费入口：
```
"""
        text = self.generate_frontmatter(
            title=topic["title"],
            subtitle=topic["description"],
            description=f"付费深度专题：{topic['description']}",
            date=date,
            tags=["付费内容", "深度方法论", "AI工作流资产"],
            is_paid=True,
        ) + body
        assert_quality(text)
        return text

    def generate_welcome_email(self, date: Optional[str] = None) -> str:
        text = self.generate_frontmatter(
            title="欢迎订阅「AI工作流深度研究」",
            subtitle="高端深度内容、方法论和可复用资产",
            description="新订阅者欢迎邮件",
            date=date,
            tags=["欢迎邮件", "定位"],
        ) + WELCOME_EMAIL_TEMPLATE
        assert_quality(text)
        return text

    def generate_video_script(self, pillar: str, topic_index: int = 0, duration: str = "60s") -> str:
        topic = self._topic(pillar, topic_index)
        body = f"""---
title: "{topic['title']} - 高密度口播提纲"
duration: "{duration}"
platform: ["视频号", "小红书", "B站"]
type: "executive_briefing"
---

# {topic['title']}

## 开场

不要再把AI内容做成工具清单。真正有付费价值的是：方法论、流程、模板、清单和可复用资产。

## 三个观点

1. 单次提示词没有壁垒，工作流SOP才有复利。
2. 素材库不等于知识资产，必须有字段、质量门禁和更新机制。
3. 内容生产只是前台，审核、发布、交付、复盘才决定能不能收费。

## 落地动作

围绕「{topic['hook']}」建立一张表：输入、处理、验收、复盘。先让流程跑通，再谈规模化。

## 结尾

如果你要做高端AI知识内容，先问自己：这篇内容能不能变成一个别人愿意付费使用的资产？
"""
        assert_quality(body)
        return body

    def generate_content_pack(self, pillar: str = "workflow_systems", topic_index: int = 0, date: Optional[str] = None) -> Dict[str, str]:
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")
        return {
            "free_post": self.generate_free_post(pillar, topic_index, date),
            "paid_deep_dive": self.generate_paid_deep_dive("workflow_sop", date),
            "video_script_60s": self.generate_video_script(pillar, topic_index, "60s"),
            "video_script_3min": self.generate_video_script(pillar, topic_index, "3min"),
        }

    def save_content_pack(self, pillar: str, topic_index: int = 0, date: Optional[str] = None) -> List[str]:
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")
        topic = self._topic(pillar, topic_index)
        topic_slug = slugify(topic["title"])
        saved_files: List[str] = []
        for content_type, content in self.generate_content_pack(pillar, topic_index, date).items():
            assert_quality(content)
            filename = f"{date}_{topic_slug}_{content_type}.md"
            filepath = self.output_dir / filename
            filepath.write_text(content, encoding="utf-8")
            saved_files.append(str(filepath))
            print(f"✓ 已生成: {filename}")
        return saved_files


def main() -> None:
    parser = argparse.ArgumentParser(description="生成高端深度Substack内容包")
    parser.add_argument("--day", type=int, help="生成第N天内容")
    parser.add_argument("--week", type=int, help="批量生成第N周内容")
    parser.add_argument("--pillar", choices=list(CONTENT_PILLARS.keys()), default="workflow_systems")
    parser.add_argument("--topic", type=int, default=0)
    parser.add_argument("--type", choices=["free", "paid", "video", "welcome", "all"], default="all")
    parser.add_argument("--output-dir", default="../content/substack_drafts")
    parser.add_argument("--date")
    parser.add_argument("--auto", action="store_true", help="自动模式：默认生成高端深度完整内容包")
    args = parser.parse_args()

    generator = SubstackContentGenerator(args.output_dir)
    date = args.date or datetime.now().strftime("%Y-%m-%d")

    if args.week:
        all_files: List[str] = []
        pillars = list(CONTENT_PILLARS.keys())
        for i in range(7):
            pillar = pillars[i % len(pillars)]
            all_files.extend(generator.save_content_pack(pillar, i, date))
        print(f"\n✅ 已生成第{args.week}周高端深度内容包（{len(all_files)}个文件）")
    elif args.day or args.auto or args.type == "all":
        files = generator.save_content_pack(args.pillar, args.topic, date)
        print(f"\n✅ 已生成高端深度完整内容包（{len(files)}个文件）")
    elif args.type == "free":
        print(generator.generate_free_post(args.pillar, args.topic, date))
    elif args.type == "paid":
        print(generator.generate_paid_deep_dive("workflow_sop", date))
    elif args.type == "video":
        print(generator.generate_video_script(args.pillar, args.topic))
    elif args.type == "welcome":
        path = generator.output_dir / f"{date}_welcome_email.md"
        path.write_text(generator.generate_welcome_email(date), encoding="utf-8")
        print(f"✓ 已生成: {path}")

    print(f"📁 输出目录: {generator.output_dir}")


if __name__ == "__main__":
    main()
