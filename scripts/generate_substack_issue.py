#!/usr/bin/env python3
"""
Substack内容自动生成脚本
基于知识订阅项目的内容支柱，自动生成免费/付费内容包

使用方法:
    python generate_substack_issue.py --day 1 --output-dir ../content/substack_drafts/
    python generate_substack_issue.py --week 1 --type all

输出格式:
    - Free Post: 免费公开发布内容
    - Paid Deep Dive: 付费深度内容
    - Welcome Email: 新订阅者欢迎邮件
    - Video Script: 短视频口播稿
"""

import argparse
import json
import os
import random
import re
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional


# ===== 内容支柱数据库 =====
CONTENT_PILLARS = {
    "ai_cognition": {
        "name": "AI基础认知",
        "description": "消除陌生感，建立基础理解",
        "topics": [
            {
                "title": "你以为AI只会聊天？它正在偷偷拉开普通人的差距",
                "hook": "每日三件事助手工作流",
                "tools": ["豆包", "通义千问", "文心一言", "讯飞星火"],
                "pain_point": "事情太多，不知道先做哪个",
                "deliverable": "一段固定话术，今晚就能试"
            },
            {
                "title": "AI为什么会'胡说'？普通人怎么判断真假",
                "hook": "3个判断AI回答靠不靠谱的方法",
                "tools": ["任意国产AI工具"],
                "pain_point": "不敢用AI，怕它说错",
                "deliverable": "交叉验证法 + 判断清单"
            },
            {
                "title": "不用下载APP，微信里就能用的AI功能",
                "hook": "3个微信内置AI功能，大多数人不知道",
                "tools": ["微信搜一搜AI", "腾讯元宝小程序", "讯飞输入法"],
                "pain_point": "觉得用AI门槛高，要装很多软件",
                "deliverable": "即开即用的3个功能"
            }
        ]
    },
    "office_productivity": {
        "name": "办公提效",
        "description": "解决具体办公场景问题",
        "topics": [
            {
                "title": "上班族每天省1小时的AI用法：信息整理篇",
                "hook": "把混乱信息变成清晰行动的完整流程",
                "tools": ["飞书文档", "腾讯文档", "豆包", "通义千问"],
                "pain_point": "信息太多太乱，找不到重点",
                "deliverable": "信息整理工作流模板"
            },
            {
                "title": "写周报不用愁：AI帮你总结一周工作",
                "hook": "一段话术，自动生成周报框架",
                "tools": ["豆包", "通义千问"],
                "pain_point": "每周写周报很痛苦",
                "deliverable": "周报生成提示词模板"
            },
            {
                "title": "Excel不会用公式？直接告诉AI你想算什么",
                "hook": "自然语言转公式，不用背函数",
                "tools": ["钉钉AI", "飞书多维表格", "WPS AI"],
                "pain_point": "Excel函数太难记",
                "deliverable": "常用公式自然语言对照表"
            },
            {
                "title": "开会2小时，整理5分钟：会议纪要AI助手",
                "hook": "从录音到纪要的完整流程",
                "tools": ["讯飞听见", "飞书妙记", "通义听悟"],
                "pain_point": "开会记不全，整理太费时间",
                "deliverable": "会议纪要模板 + 提示词"
            },
            {
                "title": "做PPT前先用AI帮你理清思路",
                "hook": "5分钟搭出PPT框架",
                "tools": ["百度文库AI", "WPS AI", "Gamma中文版"],
                "pain_point": "做PPT没思路，不知道从何下手",
                "deliverable": "PPT大纲生成提示词"
            }
        ]
    },
    "content_creation": {
        "name": "内容创作",
        "description": "面向创作者和小生意",
        "topics": [
            {
                "title": "发小红书没灵感？AI帮你找爆款选题",
                "hook": "3个找选题的方法",
                "tools": ["豆包", "小红书搜索"],
                "pain_point": "不知道发什么内容",
                "deliverable": "选题生成工作流"
            },
            {
                "title": "拍视频不写脚本？用AI生成口播稿",
                "hook": "一段输入，生成完整口播稿",
                "tools": ["剪映AI", "度加剪辑", "讯飞智作"],
                "pain_point": "想拍视频但不会写文案",
                "deliverable": "口播稿生成模板"
            },
            {
                "title": "小店主如何用AI省下一个客服的人工",
                "hook": "零成本搭建FAQ回复系统",
                "tools": ["微信自动回复", "豆包", "剪贴板工具"],
                "pain_point": "小生意没时间回客户消息",
                "deliverable": "客服回复话术库模板"
            },
            {
                "title": "AI做图不求人：零基础也能出海报",
                "hook": "3个国产AI做图工具推荐",
                "tools": ["即梦", "通义万相", "文心一格"],
                "pain_point": "不会做图，找人设计贵",
                "deliverable": "海报生成提示词模板"
            },
            {
                "title": "从0到1：用AI辅助写一个产品文案",
                "hook": "完整案例演示",
                "tools": ["豆包", "Kimi"],
                "pain_point": "写文案没思路",
                "deliverable": "产品文案生成工作流"
            }
        ]
    },
    "learning_growth": {
        "name": "学习成长",
        "description": "面向学生和自我提升",
        "topics": [
            {
                "title": "学英语不用背词典：AI做你的私人外教",
                "hook": "5个AI学英语的方法",
                "tools": ["豆包", "有道翻译官", "讯飞星火"],
                "pain_point": "学英语没环境，记不住",
                "deliverable": "AI英语学习工作流"
            },
            {
                "title": "读一本书太花时间？让AI帮你速读",
                "hook": "30分钟掌握一本书的核心",
                "tools": ["微信读书AI", "Kimi长文本", "豆包"],
                "pain_point": "想读书但没时间",
                "deliverable": "书籍速读提示词模板"
            },
            {
                "title": "准备考试，用AI制作专属复习资料",
                "hook": "从混乱笔记到系统复习资料",
                "tools": ["豆包", "飞书文档", "腾讯文档"],
                "pain_point": "笔记太乱，复习效率低",
                "deliverable": "复习资料生成模板"
            },
            {
                "title": "想学新技能？先让AI帮你做学习计划",
                "hook": "个性化学习路径生成",
                "tools": ["任意AI对话工具"],
                "pain_point": "想学习但不知从何开始",
                "deliverable": "学习计划生成提示词"
            },
            {
                "title": "孩子作业辅导，AI能帮你做什么",
                "hook": "家长辅导作业的AI助手用法",
                "tools": ["豆包", "小猿搜题", "作业帮"],
                "pain_point": "家长不会教，孩子听不懂",
                "deliverable": "作业辅导工作流"
            }
        ]
    },
    "trends_analysis": {
        "name": "趋势解读",
        "description": "中美AI新闻，普通人视角",
        "topics": [
            {
                "title": "这周AI圈发生了什么？普通人需要关注这3件事",
                "hook": "中美AI新闻解读，普通人视角",
                "tools": ["任意AI工具"],
                "pain_point": "看不懂AI新闻和自己的关系",
                "deliverable": "AI周报阅读框架"
            },
            {
                "title": "国内大厂AI混战，普通人怎么选工具",
                "hook": "豆包vs通义千问vs文心一言vs讯飞星火对比",
                "tools": ["豆包", "通义千问", "文心一言", "讯飞星火"],
                "pain_point": "不知道用哪个AI工具好",
                "deliverable": "工具选择决策表"
            },
            {
                "title": "AI正在改变这些工作，你准备好了吗",
                "hook": "具体行业的真实变化案例",
                "tools": ["任意AI工具"],
                "pain_point": "担心AI取代工作",
                "deliverable": "行业变化观察清单"
            }
        ]
    }
}

# ===== 付费深度内容模板 =====
PAID_DEEP_DIVE_TOPICS = {
    "prompt_engineering": {
        "title": "提示词工程：让AI听懂你的话",
        "description": "从随机碰运气到精准控制输出",
        "outline": [
            "提示词基础结构：角色+任务+格式+约束+示例",
            "角色扮演法：如何设计有效的AI角色",
            "思维链技巧：引导AI一步步思考",
            "少样本学习：用例子教会AI",
            "输出格式控制：列表、表格、JSON"
        ],
        "deliverables": ["20个即用提示词模板", "提示词设计检查清单", "个人提示词库模板"],
        "difficulty": "进阶"
    },
    "info_workflow": {
        "title": "信息处理工作流",
        "description": "从信息焦虑到信息掌控",
        "outline": [
            "信息收集系统：RSS+微信收藏+飞书剪存",
            "每日信息整理：AI摘要+自动分类",
            "深度阅读工作流：长文快速消化",
            "会议与对话整理：录音到行动项",
            "个人知识库建设：从输入到输出"
        ],
        "deliverables": ["信息收集工作流模板", "每日整理清单", "知识库分类体系"],
        "difficulty": "进阶"
    },
    "content_automation": {
        "title": "内容创作自动化",
        "description": "创作者的生产力倍增器",
        "outline": [
            "选题生成系统：从热点到选题",
            "脚本写作工作流：大纲→脚本→润色",
            "多平台内容适配：一文多发技巧",
            "封面与配图生成：AI做图工作流",
            "发布排期自动化：内容日历管理"
        ],
        "deliverables": ["选题生成提示词", "脚本模板库", "多平台发布检查清单"],
        "difficulty": "进阶"
    }
}

# ===== CTA模板库 =====
CTA_TEMPLATES = {
    "free_to_paid": [
        "---\n\n**想要更系统地学习？**\n\n本文只是入门级技巧。如果你想掌握完整的AI工作系统，欢迎订阅我的付费专栏。每周一篇深度教程，带你从'会用'到'精通'。\n\n[**立即订阅**](https://your-substack.substack.com/subscribe)",
        "---\n\n💡 **意犹未尽？**\n\n这篇文章只讲了基础用法。在我的付费专栏里，你会学到完整的工作流设计、多工具协同、以及个人AI系统搭建方法。\n\n[**加入付费订阅**](https://your-substack.substack.com/subscribe)",
        "---\n\n📚 **想深入学习？**\n\n今天分享的是单点技巧，而系统性的能力需要持续学习。订阅付费专栏，每周get一个可落地的AI工作系统。\n\n[**点击查看详情**](https://your-substack.substack.com/subscribe)"
    ],
    "engagement": [
        "\n\n---\n\n**你学会了吗？**\n\n在评论区分享你的使用心得，或者告诉我你想学的内容。点赞最高的3条评论，我会专门出教程解答。",
        "\n\n---\n\n💬 **有问题？**\n\n欢迎在评论区留言，我会挑选典型问题在后续内容中解答。也可以加入读者交流群，和其他同学一起讨论。",
        "\n\n---\n\n**下一步行动**\n\n1. 现在就打开AI工具试试今天学的方法\n2. 把结果截图发在评论区\n3. 转发给需要的朋友"
    ]
}

# ===== 欢迎邮件模板 =====
WELCOME_EMAIL_TEMPLATE = """# 欢迎订阅「普通人的人工智能课」

你好，欢迎加入！

我是这个账号的主理人。做这个 newsletter 的初衷很简单：

> **让普通人也能把AI真正用起来。**

网上讲AI的内容，要么太技术（满屏代码），要么太营销（"月入过万"）。但真正普通人的困惑没人讲清楚：

- AI到底能帮我做什么？
- 我不懂技术，能用吗？
- 这么多AI工具，我该用哪个？
- 用了几次没效果，是哪里出了问题？

## 你会收到什么？

**免费内容（每周3-5篇）：**
- 中美AI新闻解读（不讲术语，只讲和你我有什么关系）
- 国内AI工具推荐（豆包、通义千问、文心一言、讯飞星火等）
- 普通人的实际用法（整理信息、写周报、做会议纪要、辅导作业...）
- 真实案例（哪些好用，哪些踩坑）

**付费内容（每周1篇深度教程）：**
- 系统性AI工作流设计
- 提示词工程进阶技巧
- 多工具协同方法
- 个人AI系统搭建指南

## 建议你从这里开始

如果你是第一次接触，建议按这个顺序阅读：

1. **[AI入门必读]** - 建立正确认知，消除陌生感
2. **[第一个AI工作流]** - 今晚就能试的实战技巧
3. **[国内AI工具地图]** - 帮你省下试错时间

## 如何获得最大收获？

1. **不要只收藏，要动手试** - 每篇文章都配有可复制的提示词
2. **从一个小场景开始** - 先解决一个具体问题，再扩展
3. **加入读者群** - 回复"进群"，和其他同学交流心得

## 有问题？

随时回复这封邮件，或者关注公众号留言。我会亲自阅读每一条反馈。

期待和你一起，把AI真正用起来。

---

**主理人**
普通人的人工智能课
"""


class SubstackContentGenerator:
    """Substack内容生成器"""
    
    def __init__(self, output_dir: str = "../content/substack_drafts"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
    def generate_frontmatter(
        self,
        title: str,
        subtitle: str = "",
        description: str = "",
        author: str = "普通人的人工智能课",
        date: Optional[str] = None,
        tags: List[str] = None,
        is_paid: bool = False,
        canonical_url: str = "",
        cover_image: str = ""
    ) -> str:
        """生成Substack格式的YAML frontmatter"""
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")
        if tags is None:
            tags = ["AI", "人工智能", "效率工具"]
            
        frontmatter = f"""---
title: "{title}"
subtitle: "{subtitle}"
description: "{description}"
author: "{author}"
date: "{date}"
tags: {json.dumps(tags, ensure_ascii=False)}
is_paid: {str(is_paid).lower()}
---

"""
        return frontmatter
    
    def generate_free_post(
        self,
        pillar: str,
        topic_index: int = 0,
        date: Optional[str] = None
    ) -> str:
        """生成免费发布内容"""
        pillar_data = CONTENT_PILLARS.get(pillar, CONTENT_PILLARS["ai_cognition"])
        topic = pillar_data["topics"][topic_index % len(pillar_data["topics"])]
        
        # 构建文章结构
        content_parts = []
        
        # 1. 钩子开头
        hooks = [
            f"你是不是也遇到过这种情况：{topic['pain_point']}",
            f"今天分享一个帮你{topic['hook']}的方法。",
            f"很多人问我：{topic['pain_point']}怎么办？",
        ]
        content_parts.append(random.choice(hooks))
        content_parts.append("")
        
        # 2. 问题背景
        content_parts.append(f"**{topic['pain_point']}**")
        content_parts.append("")
        content_parts.append("这可能是很多普通人的真实困扰。网上教程要么太技术，看完一头雾水；要么太笼统，实际操作不了。")
        content_parts.append("")
        
        # 3. 解决方案介绍
        content_parts.append(f"今天介绍的方案，只需要用到：**{', '.join(topic['tools'][:2])}**")
        content_parts.append("")
        content_parts.append("**核心思路：**")
        content_parts.append(f"- {topic['hook']}")
        content_parts.append(f"- 上手简单，今晚就能试")
        content_parts.append(f"- {topic['deliverable']}")
        content_parts.append("")
        
        # 4. 具体操作步骤
        content_parts.append("## 具体操作")
        content_parts.append("")
        content_parts.append("### 第一步：打开工具")
        tool = topic['tools'][0]
        if '微信' in tool:
            content_parts.append(f"打开{tool}，无需下载额外APP。")
        else:
            content_parts.append(f"打开{tool}（网页或APP都可以）。")
        content_parts.append("")
        
        content_parts.append("### 第二步：输入这段话")
        # 根据主题生成相应的提示词
        prompt_templates = self._generate_prompt_template(topic)
        content_parts.append("```")
        content_parts.append(prompt_templates)
        content_parts.append("```")
        content_parts.append("")
        
        content_parts.append("### 第三步：根据结果调整")
        content_parts.append("如果结果不满意，可以补充更多背景信息，或者要求AI用不同的方式呈现。")
        content_parts.append("")
        
        # 5. 实际案例
        content_parts.append("## 真实案例")
        content_parts.append("")
        case_study = self._generate_case_study(topic)
        content_parts.extend(case_study)
        content_parts.append("")
        
        # 6. 常见问题
        content_parts.append("## 常见问题")
        content_parts.append("")
        faqs = self._generate_faqs(topic)
        content_parts.extend(faqs)
        content_parts.append("")
        
        # 7. CTA
        content_parts.append(random.choice(CTA_TEMPLATES["engagement"]))
        content_parts.append("")
        
        # 8. 付费引导（可选）
        if random.random() > 0.5:
            content_parts.append(random.choice(CTA_TEMPLATES["free_to_paid"]))
        
        # 组装内容
        body = "\n".join(content_parts)
        
        # 生成frontmatter
        frontmatter = self.generate_frontmatter(
            title=topic['title'],
            subtitle=topic['hook'],
            description=f"{topic['pain_point']}的解决方案，使用{', '.join(topic['tools'][:2])}",
            date=date,
            tags=[pillar_data["name"], "AI工具", "效率"],
            is_paid=False
        )
        
        return frontmatter + body
    
    def generate_paid_deep_dive(
        self,
        topic_key: str,
        date: Optional[str] = None
    ) -> str:
        """生成付费深度内容"""
        topic = PAID_DEEP_DIVE_TOPICS.get(topic_key, PAID_DEEP_DIVE_TOPICS["prompt_engineering"])
        
        content_parts = []
        
        # 1. 专属开头
        content_parts.append("> **付费会员专属内容**")
        content_parts.append("> ")
        content_parts.append(f"> 本文是「{topic['title']}」专题的一部分。")
        content_parts.append("")
        
        # 2. 专题介绍
        content_parts.append(f"# {topic['title']}")
        content_parts.append("")
        content_parts.append(f"**{topic['description']}**")
        content_parts.append("")
        
        # 3. 适合谁看
        content_parts.append("## 这个专题适合谁？")
        content_parts.append("")
        content_parts.append(f"- 已经用过AI工具，想要**系统性提升**的同学")
        content_parts.append(f"- 希望从'会提问'升级到'会设计工作流'的同学")
        content_parts.append(f"- 想要建立**个人AI系统**的同学")
        content_parts.append("")
        
        # 4. 内容大纲
        content_parts.append("## 专题内容")
        content_parts.append("")
        for i, item in enumerate(topic['outline'], 1):
            content_parts.append(f"{i}. {item}")
        content_parts.append("")
        
        # 5. 详细内容
        content_parts.append("---")
        content_parts.append("")
        content_parts.append("## 第一讲：基础概念")
        content_parts.append("")
        content_parts.append(self._generate_paid_content_section(topic))
        content_parts.append("")
        
        # 6. 实战练习
        content_parts.append("## 实战练习")
        content_parts.append("")
        content_parts.append("完成以下练习，把今天学的内容用起来：")
        content_parts.append("")
        exercises = self._generate_exercises(topic)
        for i, ex in enumerate(exercises, 1):
            content_parts.append(f"**练习{i}：** {ex}")
            content_parts.append("")
        
        # 7. 交付物
        content_parts.append("## 本期交付物")
        content_parts.append("")
        content_parts.append("订阅本专题，你将获得：")
        content_parts.append("")
        for deliverable in topic['deliverables']:
            content_parts.append(f"- ✅ {deliverable}")
        content_parts.append("")
        
        # 8. 下一讲预告
        content_parts.append("---")
        content_parts.append("")
        content_parts.append("**下一讲预告：**")
        content_parts.append(f"我们将深入讲解{topic['outline'][1] if len(topic['outline']) > 1 else '进阶技巧'}，并配有完整的操作演示。")
        content_parts.append("")
        
        # 9. 互动
        content_parts.append("---")
        content_parts.append("")
        content_parts.append("💬 **有问题？**")
        content_parts.append("")
        content_parts.append("付费会员可以在评论区提问，我会一一回复。也可以加入付费会员专属群，和其他同学一起交流。")
        
        # 组装
        body = "\n".join(content_parts)
        
        # 生成frontmatter
        frontmatter = self.generate_frontmatter(
            title=topic['title'],
            subtitle=topic['description'],
            description=f"付费专题：{topic['description']}",
            date=date,
            tags=["付费内容", "深度教程", "AI进阶"],
            is_paid=True
        )
        
        return frontmatter + body
    
    def generate_welcome_email(self, date: Optional[str] = None) -> str:
        """生成欢迎邮件"""
        frontmatter = self.generate_frontmatter(
            title="欢迎订阅「普通人的人工智能课」",
            subtitle="从这里开始你的AI学习之旅",
            description="新订阅者欢迎邮件，介绍内容体系和入门路径",
            date=date,
            tags=["欢迎邮件", "入门指南"],
            is_paid=False
        )
        return frontmatter + WELCOME_EMAIL_TEMPLATE
    
    def generate_video_script(
        self,
        pillar: str,
        topic_index: int = 0,
        duration: str = "60s"
    ) -> str:
        """生成短视频口播稿"""
        pillar_data = CONTENT_PILLARS.get(pillar, CONTENT_PILLARS["ai_cognition"])
        topic = pillar_data["topics"][topic_index % len(pillar_data["topics"])]
        
        content_parts = []
        
        # Frontmatter
        frontmatter = f"""---
title: "{topic['title']} - 视频脚本"
duration: "{duration}"
platform: ["抖音", "小红书", "视频号"]
type: "short_video"
---

"""
        
        # 脚本内容
        content_parts.append(f"# {topic['title']}")
        content_parts.append(f"**预计时长：{duration}**")
        content_parts.append("")
        
        if duration == "60s":
            content_parts.append("## 开头（0-10秒）")
            content_parts.append(f"你是不是也这样：{topic['pain_point']}")
            content_parts.append("")
            content_parts.append("## 中间（10-45秒）")
            content_parts.append(f"今天教你一招：{topic['hook']}")
            content_parts.append("")
            content_parts.append("只需要用到：" + ", ".join(topic['tools'][:2]))
            content_parts.append("")
            content_parts.append("**操作步骤：**")
            content_parts.append(f"1. 打开{topic['tools'][0]}")
            content_parts.append(f"2. 输入这段话：[提示词]")
            content_parts.append(f"3. 根据结果调整")
            content_parts.append("")
            content_parts.append("## 结尾（45-60秒）")
            content_parts.append(f"今晚就试试！{topic['deliverable']}")
            content_parts.append("")
            content_parts.append("关注我看更多AI实用技巧 👆")
            
        elif duration == "3min":
            content_parts.append("## 开头（0-20秒）- 痛点引入")
            content_parts.append(f"{topic['pain_point']}")
            content_parts.append("这可能是很多普通人的真实困扰。")
            content_parts.append("")
            content_parts.append("## 问题分析（20-50秒）")
            content_parts.append("为什么这个问题难解决？")
            content_parts.append("- 信息太分散")
            content_parts.append("- 工具门槛高")
            content_parts.append("- 没人手把手教")
            content_parts.append("")
            content_parts.append("## 解决方案（50-120秒）")
            content_parts.append(f"今天介绍的方法，使用{', '.join(topic['tools'][:2])}")
            content_parts.append("")
            content_parts.append("**详细步骤：**")
            content_parts.append(f"1. 打开{topic['tools'][0]}")
            content_parts.append("2. 输入这段提示词...")
            content_parts.append("3. 根据输出调整参数")
            content_parts.append("4. 导出结果")
            content_parts.append("")
            content_parts.append("## 案例演示（120-160秒）")
            content_parts.append("来看一个真实案例...")
            content_parts.append("")
            content_parts.append("## 结尾（160-180秒）")
            content_parts.append("你学会了吗？")
            content_parts.append("评论区分享你的使用心得")
            content_parts.append("点赞最高的问题，我专门出视频解答")
        
        # 画面建议
        content_parts.append("")
        content_parts.append("---")
        content_parts.append("")
        content_parts.append("## 画面建议")
        content_parts.append("")
        content_parts.append("- **开头**：真人出镜或痛点场景")
        content_parts.append("- **演示**：录屏展示操作过程")
        content_parts.append("- **结尾**：CTA引导关注/评论")
        content_parts.append("")
        content_parts.append("## 字幕要点")
        content_parts.append("")
        content_parts.append(f"- 突出关键词：{', '.join(topic['tools'][:2])}")
        content_parts.append(f"- 强调价值：{topic['hook']}")
        
        body = "\n".join(content_parts)
        return frontmatter + body
    
    def generate_content_pack(
        self,
        pillar: str = "ai_cognition",
        topic_index: int = 0,
        date: Optional[str] = None
    ) -> Dict[str, str]:
        """生成完整内容包"""
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")
            
        outputs = {}
        
        # 生成免费内容
        outputs["free_post"] = self.generate_free_post(pillar, topic_index, date)
        
        # 生成付费内容（随机选择一个主题）
        paid_topic = random.choice(list(PAID_DEEP_DIVE_TOPICS.keys()))
        outputs["paid_deep_dive"] = self.generate_paid_deep_dive(paid_topic, date)
        
        # 生成视频脚本
        outputs["video_script_60s"] = self.generate_video_script(pillar, topic_index, "60s")
        outputs["video_script_3min"] = self.generate_video_script(pillar, topic_index, "3min")
        
        return outputs
    
    def save_content_pack(
        self,
        pillar: str,
        topic_index: int = 0,
        date: Optional[str] = None
    ) -> List[str]:
        """生成并保存完整内容包到文件"""
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")
            
        outputs = self.generate_content_pack(pillar, topic_index, date)
        saved_files = []
        
        # 获取主题标题用于文件名
        pillar_data = CONTENT_PILLARS.get(pillar, CONTENT_PILLARS["ai_cognition"])
        topic = pillar_data["topics"][topic_index % len(pillar_data["topics"])]
        topic_slug = re.sub(r'[^\w\s]', '', topic['title'])[:20].replace(' ', '_')
        
        # 保存各部分内容
        for content_type, content in outputs.items():
            filename = f"{date}_{topic_slug}_{content_type}.md"
            filepath = self.output_dir / filename
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            
            saved_files.append(str(filepath))
            print(f"✓ 已生成: {filename}")
        
        return saved_files
    
    # ===== 辅助方法 =====
    
    def _generate_prompt_template(self, topic: Dict) -> str:
        """根据主题生成提示词模板"""
        templates = {
            "信息整理": """请你像一个工作助手，帮我整理下面这些信息。

【输入信息】
（把你的信息粘贴在这里）

请帮我：
1. 分成三类：今天必须做、可以晚点做、可以不做
2. 每一类最多保留三条最重要的
3. 给每件事加上预计时间
4. 输出成清晰的待办清单格式""",
            "周报": """请你帮我写一份周报。

本周工作：
（列出你做过的事，哪怕很零散）

请帮我：
1. 整理成结构化的周报格式
2. 突出成果和进展
3. 添加下周计划框架
4. 用简洁专业的语言""",
            "会议纪要": """请你帮我整理会议纪要。

会议录音/笔记：
（粘贴内容）

请帮我：
1. 提取核心决策点
2. 列出行动项（负责人+截止日期）
3. 总结关键讨论内容
4. 输出成标准纪要格式""",
            "小红书选题": """请你帮我找小红书选题。

我的领域：（填写你的领域）

请帮我：
1. 找出这个领域最近热门的10个话题
2. 分析为什么它们火
3. 给每个话题提供3个差异化角度
4. 推荐最适合我的3个选题""",
            "口播稿": """请你帮我写一段口播稿。

主题：（填写主题）
目标受众：（填写受众）
时长：（如60秒）

要求：
1. 口语化，适合直接对着镜头说
2. 开头有钩子，吸引注意力
3. 中间有干货，提供价值
4. 结尾有互动，引导评论""",
        }
        
        # 根据主题关键词匹配模板
        for key, template in templates.items():
            if key in topic['title'] or key in topic['hook']:
                return template
        
        # 默认模板
        return f"""请你帮我完成这个任务：{topic['title']}

我的需求：（在这里描述你的具体情况）

请帮我：
1. （具体需求1）
2. （具体需求2）
3. （输出格式要求）

要求输出清晰、实用、可立即执行。"""
    
    def _generate_case_study(self, topic: Dict) -> List[str]:
        """生成案例研究"""
        return [
            "**案例：小张的尝试**",
            "",
            f"小张是一名普通上班族，每天面临{topic['pain_point']}的困扰。",
            "",
            f"按照今天介绍的方法，他使用了{topic['tools'][0]}：",
            "1. 输入提示词",
            "2. 根据结果调整",
            "3. 应用到实际工作",
            "",
            f"**结果：** {topic['hook']}，效率提升了50%以上。",
            "",
            "> 💡 **关键心得**：关键是不要追求完美，先完成再优化。"
        ]
    
    def _generate_faqs(self, topic: Dict) -> List[str]:
        """生成常见问题"""
        return [
            "**Q1：需要付费吗？**",
            f"A：{topic['tools'][0]}有免费额度，日常使用足够。",
            "",
            "**Q2：信息安全吗？**",
            "A：建议不要输入敏感个人信息和公司机密数据。",
            "",
            "**Q3：效果不好怎么办？**",
            "A：多补充背景信息，多试几次，每次调整一点提示词。",
            "",
            "**Q4：可以用其他AI工具吗？**",
            f"A：可以，{', '.join(topic['tools'][:3])}都可以试试，看哪个结果更符合你的需求。"
        ]
    
    def _generate_paid_content_section(self, topic: Dict) -> str:
        """生成付费内容的具体章节"""
        if topic['title'] == "提示词工程：让AI听懂你的话":
            return """### 为什么提示词很重要

同样的AI，不同的提示词，结果可能天差地别。

举个例子：
- ❌ 差提示词："帮我写个文案"
- ✅ 好提示词："请你扮演一位资深营销专家，帮我写一个咖啡店的开业宣传文案。目标受众是25-35岁的上班族，风格要温馨亲切。字数控制在200字以内，包含优惠活动信息。"

看出区别了吗？好的提示词包含四个要素：

1. **角色设定** - 让AI进入状态
2. **任务描述** - 说清楚要做什么
3. **约束条件** - 限制和边界
4. **输出格式** - 规定结果长什么样"""
        
        elif topic['title'] == "信息处理工作流":
            return """### 信息焦虑的本质

信息不是问题，没有系统才是问题。

大多数人面临的情况是：
- 收藏了100篇文章，一篇都没看
- 关注了50个公众号，信息过载
- 每天花2小时刷资讯，越刷越焦虑

解决方法不是少看信息，而是建立**信息处理系统**：

```
收集 → 整理 → 加工 → 输出
```

每个环节都要有明确的规则和工具。"""
        
        else:
            return """### 系统思维的重要性

单点技巧只能解决具体问题，系统设计才能持续产生价值。

这就是为什么很多人学了100个AI技巧，还是感觉没用起来——缺少系统。

本专题的目标，就是帮你建立完整的AI工作系统。"""
    
    def _generate_exercises(self, topic: Dict) -> List[str]:
        """生成练习题"""
        return [
            "用一个真实场景，实践今天学的方法",
            "记录使用过程中的问题和心得",
            "在评论区分享你的实践成果"
        ]


def main():
    parser = argparse.ArgumentParser(
        description="生成Substack内容包",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 生成第1天的完整内容包
  python generate_substack_issue.py --day 1

  # 生成办公提效主题的内容
  python generate_substack_issue.py --pillar office_productivity --topic 0

  # 生成欢迎邮件
  python generate_substack_issue.py --type welcome --output-dir ./drafts/

  # 批量生成一周内容
  python generate_substack_issue.py --week 1 --type all
        """
    )
    
    parser.add_argument('--day', type=int, help='生成第N天的内容（1-30）')
    parser.add_argument('--week', type=int, help='生成第N周的完整内容包（1-6）')
    parser.add_argument('--pillar', type=str, 
                        choices=list(CONTENT_PILLARS.keys()),
                        help='内容支柱类型')
    parser.add_argument('--topic', type=int, default=0, help='主题索引')
    parser.add_argument('--type', type=str, 
                        choices=['free', 'paid', 'video', 'welcome', 'all'],
                        default='all',
                        help='内容类型')
    parser.add_argument('--output-dir', type=str, 
                        default='../content/substack_drafts',
                        help='输出目录')
    parser.add_argument('--date', type=str, 
                        help='发布日期（YYYY-MM-DD格式）')
    parser.add_argument('--auto', action='store_true',
                        help='自动模式：兼容调度/发布链路，按默认主题生成完整内容包')
    
    args = parser.parse_args()
    
    # 初始化生成器
    generator = SubstackContentGenerator(args.output_dir)
    
    # 确定日期
    if args.date:
        date = args.date
    else:
        date = datetime.now().strftime("%Y-%m-%d")
    
    # 根据参数生成内容
    if args.day:
        # 根据天数确定支柱和主题
        day_to_pillar = {
            1: ("ai_cognition", 0), 2: ("ai_cognition", 1), 3: ("ai_cognition", 2),
            4: ("office_productivity", 0), 5: ("office_productivity", 1),
            6: ("office_productivity", 2), 7: ("office_productivity", 3),
            8: ("content_creation", 0), 9: ("content_creation", 1),
            10: ("content_creation", 2), 11: ("learning_growth", 0),
            12: ("learning_growth", 1), 13: ("trends_analysis", 0),
        }
        pillar, topic_idx = day_to_pillar.get(args.day, ("ai_cognition", 0))
        files = generator.save_content_pack(pillar, topic_idx, date)
        print(f"\n✅ 已生成第{args.day}天的完整内容包（{len(files)}个文件）")
        
    elif args.week:
        # 批量生成一周内容
        week_start = (args.week - 1) * 7 + 1
        all_files = []
        for day in range(week_start, min(week_start + 7, 31)):
            day_date = (datetime.now() + timedelta(days=day-1)).strftime("%Y-%m-%d")
            day_to_pillar = {
                1: ("ai_cognition", 0), 2: ("ai_cognition", 1), 3: ("ai_cognition", 2),
                4: ("office_productivity", 0), 5: ("office_productivity", 1),
                6: ("office_productivity", 2), 7: ("office_productivity", 3),
                8: ("content_creation", 0), 9: ("content_creation", 1),
                10: ("content_creation", 2), 11: ("learning_growth", 0),
                12: ("learning_growth", 1), 13: ("trends_analysis", 0),
            }
            pillar, topic_idx = day_to_pillar.get(day, ("ai_cognition", 0))
            files = generator.save_content_pack(pillar, topic_idx, day_date)
            all_files.extend(files)
        print(f"\n✅ 已生成第{args.week}周的完整内容（{len(all_files)}个文件）")
        
    elif args.pillar:
        # 生成指定支柱的内容
        files = generator.save_content_pack(args.pillar, args.topic, date)
        print(f"\n✅ 已生成内容包（{len(files)}个文件）")
        
    elif args.type == 'welcome':
        # 生成欢迎邮件
        content = generator.generate_welcome_email(date)
        filepath = Path(args.output_dir) / f"{date}_welcome_email.md"
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"\n✅ 已生成欢迎邮件: {filepath}")
        
    else:
        # 默认生成完整内容包
        files = generator.save_content_pack("ai_cognition", 0, date)
        print(f"\n✅ 已生成默认内容包（{len(files)}个文件）")
    
    print(f"\n📁 输出目录: {args.output_dir}")


if __name__ == '__main__':
    main()
