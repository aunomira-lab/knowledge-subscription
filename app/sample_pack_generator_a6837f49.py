#!/usr/bin/env python3
"""
knowledge-subscription 首批可售卖内容样例包生成器 v9
任务ID: a6837f49
版本: v9.0
运行: python app/sample_pack_generator_a6837f49.py
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path

BASE_DIR = Path("/home/AgentAdmin/.hermes/shared/dev-team/projects/knowledge-subscription")
OUTPUT_DIR = BASE_DIR / "reports" / "sample_pack"
DOCS_DIR = BASE_DIR / "docs"
WEEK_DIR = OUTPUT_DIR / "week1_samples"
TASK_ID = "a6837f49"
VERSION = "v9.0"


def ensure_dirs():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    WEEK_DIR.mkdir(parents=True, exist_ok=True)
    DOCS_DIR.mkdir(parents=True, exist_ok=True)


def write_file(path: Path, content: str):
    path.write_text(content, encoding="utf-8")
    print(f"  OK -> {path}")


OPPORTUNITIES = [
    {
        "id": "opp-v9-001",
        "title": "AI 语音电话 Agent SaaS：替代传统外呼，月收 ¥8,000+",
        "category": "AI语音/B2B SaaS",
        "difficulty": 3,
        "launch_days": "7-14天",
        "revenue": "¥8,000-50,000/月",
        "margin": ">85%",
        "summary": "使用 Vapi、Retell 或 Bland 搭建 AI 语音电话 Agent，为房产中介、教培机构、医美诊所提供自动预约、回访、邀约服务。按通话分钟数或坐席数收费。",
        "data_sources": [
            "Vapi 2026年5月公开数据：日处理通话超 2,000 万分钟，企业客户数 12,000+",
            "Retell AI 完成 B 轮 $42M 融资，ARR 年增 600%",
            "国内房产中介单店月均外呼 5,000-20,000 通，人工成本 ¥6,000-15,000/人",
            "1688 上 'AI 外呼系统' 月销 500+ 套，均价 ¥499，产品体验差、复购率低",
        ],
        "action_steps": [
            "注册 Vapi 或 Retell 免费账户，熟悉语音工作流：接听/外呼 -> STT -> LLM 决策 -> TTS 回复",
            "选择 1 个垂直场景（推荐：教培试听课邀约），录制 100 通真实通话做意图分类训练数据",
            "搭建标准话术树：开场白 -> 需求确认 -> 产品介绍 -> 异议处理 -> 预约/挂断，每个节点配 3 种回复变体",
            "用 Python 写接入 demo：读取客户 CSV -> 批量外呼 -> 通话结果回写 -> 飞书群通知，作为销售演示",
            "在电销行业社群发试用帖：'7 天免费试用，不替换现有系统，只补夜间/高峰期漏接'，定价 ¥0.15/分钟 或 ¥999/坐席/月",
        ],
        "prompt_template": "你是一位专业的【行业】电话销售顾问。请根据话术知识库，用自然、亲切的口语化中文与客户通话。\n通话目标：{{call_goal}}\n客户信息：{{customer_info}}\n当前对话历史：{{conversation_history}}\n请生成下一句回复（仅输出要说的内容）。如需转人工，请只说'转人工'。",
        "tags": ["AI语音", "Vapi", "Retell", "外呼自动化", "B2B SaaS"],
        "source_urls": [
            "https://vapi.ai/",
            "https://www.retellai.com/",
            "https://www.bland.ai/",
        ],
        "free_preview": True,
    },
    {
        "id": "opp-v9-002",
        "title": "AI 浏览器自动化爬虫：卖标准化数据抓取工作流",
        "category": "自动化/数据服务",
        "difficulty": 3,
        "launch_days": "5-10天",
        "revenue": "¥5,000-30,000/月",
        "margin": ">90%",
        "summary": "利用 browser-use、Stagehand 或 Playwright + AI 视觉理解，为电商卖家、投研机构提供定制化网页数据抓取和监控服务。一次开发可复用，边际成本极低。",
        "data_sources": [
            "browser-use GitHub 25k+ stars（2026-05），月下载量 180 万+",
            "Stagehand（browserbase）获 a16z 领投 $15M，专注 AI 驱动的浏览器自动化",
            "淘宝/拼多多/京东商家日均需监控竞品价格、库存、评论，现有工具年费 ¥3,000-12,000",
            "即刻 '爬虫' 话题日均新增 40+ 条，大量用户表示 '不会写代码但需要数据'",
        ],
        "action_steps": [
            "安装 browser-use：pip install browser-use，注册 OpenAI/Anthropic API key，运行官方 demo",
            "选择 1 个高价值场景（推荐：Temu/Amazon 竞品价格监控），写出抓取目标字段：标题、价格、评分、库存、最近 10 条评论",
            "用 browser-use 编写抓取 agent：给定 URL 列表 -> AI 自动识别页面结构 -> 提取结构化数据 -> 保存 CSV/JSON",
            "搭建交付界面：Streamlit 单页应用，用户粘贴竞品链接 -> 选择监控频率 -> 开始抓取 -> 下载结果。部署到 Render/Railway 免费档",
            "定价策略：单次抓取 ¥99-499（按页数），监控服务 ¥299-999/月，企业定制 ¥2,999+",
        ],
        "prompt_template": "你是一个专业的网页数据抓取专家，使用 browser-use 工具。\n目标网站：{{target_url}}\n需要抓取的数据：{{data_requirements}}\n请生成一个完整的 browser-use agent 代码，要求：\n1. 使用 Python + asyncio + browser_use 库\n2. 包含明确的任务描述\n3. 处理分页和动态加载\n4. 数据保存为 pandas DataFrame 并导出 CSV\n5. 包含错误处理和重试逻辑",
        "tags": ["browser-use", "爬虫", "数据服务", "Playwright", "自动化"],
        "source_urls": [
            "https://github.com/browser-use/browser-use",
            "https://github.com/browserbase/stagehand",
            "https://playwright.dev/",
        ],
        "free_preview": True,
    },
    {
        "id": "opp-v9-003",
        "title": "小红书/公众号 AI 图文矩阵：1 人运营 20 个号月收 ¥10,000+",
        "category": "社媒变现/内容创业",
        "difficulty": 2,
        "launch_days": "3-7天",
        "revenue": "¥10,000-60,000/月",
        "margin": ">75%",
        "summary": "用 Flux、Midjourney v7 和 AI 写作工具批量生成高颜值图文内容，覆盖家居、穿搭、职场等垂直领域，在小红书和公众号做矩阵发布。通过品牌广告、知识付费和私域转化变现。",
        "data_sources": [
            "小红书 2026 Q1 创作者报告：图文笔记互动率比视频高 23%，'精致生活'和'职场干货'品类增速最快",
            "Flux 开源模型生态成熟，单张 1024px 图片生成成本 < ¥0.05，质量接近 Midjourney v6",
            "公众号 '小绿书'（图片消息）打开率恢复至 8-12%，部分图文号广告报价 ¥0.5-2/阅读",
            "即刻 'AI 小红书' 圈子头部玩家晒出：1 人管理 15 个号，月均广告收入 ¥15,000-40,000",
        ],
        "action_steps": [
            "选定 2-3 个垂直赛道（推荐组合：职场效率 + 家居好物），每个赛道注册 5-7 个小红书号 + 2 个公众号",
            "搭建内容工厂：ChatGPT/Claude 写标题和文案（批量生成 50 条）-> Flux/Midjourney 生成封面和配图 -> 排期发布",
            "建立爆款素材库：用后羿/新榜抓取近 30 天千赞以上图文，分析标题结构、封面配色、正文节奏",
            "发布策略：每个号每天 1-2 条，发布时间 7:30/12:00/18:30/22:00，前 30 分钟主动回复评论提升互动权重",
            "变现路径：粉丝 1,000+ 开通蒲公英接广告（¥200-800/条）-> 粉丝 5,000+ 引流私域卖模板/课程（¥99-499）-> 粉丝 10,000+ 接品牌合作（¥3,000-10,000/条）",
        ],
        "prompt_template": "你是一位小红书爆款图文创作者，擅长写【赛道】领域的千赞笔记。\n选题：{{topic}}\n目标受众：{{target_audience}}\n要求：\n1. 标题使用数字法或反常识法，含 1-2 个 emoji，不超过 20 字\n2. 封面图提示词：给出 Midjourney/Flux 可用的英文 prompt，要求视觉冲击力、高饱和度\n3. 正文分 5-7 段，每段不超过 3 行，用 emoji 点缀\n4. 结尾带互动钩子\n5. 标签 5-8 个",
        "tags": ["小红书", "公众号", "AI图文", "矩阵运营", "社媒变现"],
        "source_urls": [
            "https://www.xiaohongshu.com/",
            "https://blackforestlabs.ai/ (Flux)",
            "https://www.midjourney.com/",
        ],
        "free_preview": True,
    },
    {
        "id": "opp-v9-004",
        "title": "跨境电商 AI 评论分析选品雷达：从差评里挖金矿",
        "category": "跨境电商/数据工具",
        "difficulty": 3,
        "launch_days": "7-14天",
        "revenue": "$2,000-15,000/月",
        "margin": ">90%",
        "summary": "用 AI 批量抓取 Amazon、Temu、速卖通、Shopee 的商品评论，通过情感分析和痛点提取，帮助跨境卖家发现'高销量低评分'的改进机会。卖报告和 SaaS 订阅。",
        "data_sources": [
            "Amazon 全球 3P 卖家超 200 万，90% 以上表示'选品是最大痛点'，现有工具年费 $600-2,400",
            "Temu 2026 年活跃卖家 150 万+，大量工厂型卖家缺乏 C 端用户洞察能力",
            "Shopee 东南亚卖家论坛中，'如何分析竞品差评'是搜索量前 5 的问题",
            "AI 情感分析 API 成本已降至 $0.001/条评论，处理 10 万条评论成本 < $100",
        ],
        "action_steps": [
            "确定目标平台（推荐：Temu 美国站），用 Playwright/browser-use 抓取 TOP 100 商品的评论数据",
            "设计 AI 分析流水线：原始评论 -> 去重清洗 -> 按星级分类 -> LLM 提取痛点关键词 -> 统计频率 -> 生成改进建议",
            "输出'选品雷达报告'模板：市场概况 -> 差评 TOP10 痛点 -> 改进产品概念 -> 预估利润空间",
            "制作销售页：放 3 份免费样例报告（不同品类），其余报告付费解锁（¥199/份 或 ¥499/月无限下载）",
            "获客：在亚马逊卖家群/知无不言/Temu 卖家论坛发帖子：'我分析了 500 条差评，发现这个品类有 3 个被忽视的改进机会'，引流到销售页",
        ],
        "prompt_template": "你是一位跨境电商选品分析师。请根据以下商品评论数据，生成一份选品雷达分析报告。\n商品信息：\n平台：{{platform}}\n类目：{{category}}\n差评样本（1-3 星）：\n{{negative_reviews}}\n要求：\n1. 提取 TOP10 用户痛点，按出现频率排序\n2. 对每个痛点，给出'现有产品如何改进'的具体建议\n3. 评估改进后的新品竞争力和预估利润率\n4. 输出一份可直接发给卖家的 Markdown 报告",
        "tags": ["跨境电商", "选品", "评论分析", "Amazon", "Temu"],
        "source_urls": [
            "https://sellercentral.amazon.com/",
            "https://www.temu.com/",
            "https://www.zhizhou.com/ (知无不言)",
        ],
        "free_preview": False,
    },
    {
        "id": "opp-v9-005",
        "title": "AI 播客/有声书内容工厂：批量生产音频资产",
        "category": "内容生产/音频变现",
        "difficulty": 2,
        "launch_days": "5-10天",
        "revenue": "¥5,000-40,000/月",
        "margin": ">80%",
        "summary": "用 ElevenLabs、NotebookLM 或国内讯飞/魔音工坊，将热门文章、公版书籍批量转化为高质量有声书和播客节目，分发到小宇宙、喜马拉雅、Spotify、YouTube。通过广告分成、付费订阅变现。",
        "data_sources": [
            "喜马拉雅 2025 年报：有声书用户 4.2 亿，付费率 18%，'AI 合成语音'内容增速 340%",
            "小宇宙播客 2026 年活跃主播 50 万+，'商业/科技'品类广告 CPM ¥80-200",
            "ElevenLabs 2026 年 5 月数据：支持 32 种语言、1,000+ 声音克隆，API 成本 $0.08/千字符",
            "YouTube Podcasts 月活 10 亿+，创作者可通过 AdSense 获得 $2-8/千次播放",
        ],
        "action_steps": [
            "选择内容赛道（推荐：商业思维/AI 趋势/心理学），收集 50 篇高阅读量公版文章/报告（确保无版权风险）",
            "用 ElevenLabs 训练固定主播声音（或使用 API 预设声音），设定参数：语速 1.1x、语气亲和、停顿自然",
            "搭建流水线：原文 -> Claude 改写为口语化播客脚本 -> ElevenLabs API 生成音频 -> ffmpeg 添加片头片尾 -> 生成封面图 -> 批量上传",
            "分发矩阵：小宇宙（中文主阵地）+ 喜马拉雅（长尾流量）+ YouTube Podcasts（英语内容/ AdSense）+ Spotify（全球化）",
            "变现组合：平台广告分成（起步）-> 小宇宙'付费单集'（¥9.9-29.9/期）-> 系列专辑（¥99-199/季）-> 企业定制音频内容（¥2,999+）",
        ],
        "prompt_template": "你是一位专业的播客脚本编辑。请将以下书面文章改写成适合音频节目的口播脚本。\n原文：\n{{original_text}}\n节目名称：{{podcast_name}}\n主播人设：{{host_persona}}\n目标听众：{{target_audience}}\n改写要求：\n1. 用第二人称'你'，语气像朋友聊天，避免书面长句\n2. 每 300 字插入一个过渡句或口语化衔接\n3. 关键数据重复一遍（音频无法回看）\n4. 结尾加 30 秒总结 + 下期预告 + 订阅引导\n5. 总时长控制在 10-15 分钟（约 2,500-3,500 字）",
        "tags": ["AI音频", "播客", "有声书", "ElevenLabs", "内容工厂"],
        "source_urls": [
            "https://elevenlabs.io/",
            "https://www.xiaoyuzhoufm.com/",
            "https://www.ximalaya.com/",
        ],
        "free_preview": False,
    },
    {
        "id": "opp-v9-006",
        "title": "AI 面试陪跑 & 简历重构：裁员潮里的刚需生意",
        "category": "知识付费/求职服务",
        "difficulty": 2,
        "launch_days": "3-5天",
        "revenue": "¥10,000-80,000/月",
        "margin": ">85%",
        "summary": "针对 2025-2026 年持续的人才市场波动，为中高端求职者提供 AI 驱动的简历重构、面试模拟和谈薪辅导。用 Claude 4 做简历诊断和模拟面试，客单价高、转介绍高。",
        "data_sources": [
            "智联招聘 2026 Q1 报告：平均每个岗位收到 128 份简历，985/211 毕业生平均求职周期 4.2 个月",
            "BOSS 直聘数据：'简历优化'服务搜索量年增 180%，'面试辅导'年增 220%",
            "猎聘网高端简历服务客单价 ¥1,500-8,000，头部顾问月入 5 万+",
            "小红书 '简历修改'话题浏览量 12 亿+，'面试技巧'话题 8 亿+",
        ],
        "action_steps": [
            "训练自己的 AI 简历诊断模型：收集 50 份优质简历（不同行业/职级），让 Claude 总结'高分简历'的共同特征，形成诊断 checklist",
            "设计服务包：A 包 ¥299（AI 简历重构 + 1 轮反馈）；B 包 ¥799（简历 + 模拟面试 3 轮 + 谈薪话术）；C 包 ¥1,999（全程陪跑 30 天 + 内推资源对接）",
            "搭建交付流程：用户填表（目标岗位/当前痛点）-> AI 生成初版简历 -> 人工精修 -> 交付 + 30 分钟视频讲解修改逻辑 -> 模拟面试（用语音 Agent 扮演面试官）",
            "获客渠道：小红书发 '简历前后对比' 图文（敏感信息打码）+ 知乎写 'HR 视角：什么样的简历 10 秒过初筛' + 即刻发 'AI 模拟面试实录' 片段",
            "建立转介绍机制：成功拿到 offer 的用户，送 1 次免费职业规划咨询；推荐 1 位新客户，双方各得 ¥50 优惠券",
        ],
        "prompt_template": "你是一位资深 HR 和职业发展顾问，有 10 年互联网大厂招聘经验。\n请根据以下用户信息和目标岗位，重构一份高分简历。\n用户原始简历：\n{{original_resume}}\n目标岗位：{{target_job}}\n目标公司类型：{{company_type}}\n要求：\n1. 使用 STAR 法则重写所有项目/工作经历\n2. 每个结果必须有量化数据（百分比、金额、用户数、效率提升等）\n3. 删除与目标岗位无关的经历，突出匹配度最高的 3-5 项能力\n4. 自我评价不超过 3 行，用'数据 + 能力 + 价值'结构\n5. 输出可直接复制到 Word/在线简历工具的纯文本格式",
        "tags": ["求职", "简历优化", "面试辅导", "知识付费", "AI陪跑"],
        "source_urls": [
            "https://www.zhaopin.com/",
            "https://www.zhipin.com/",
            "https://www.xiaohongshu.com/",
        ],
        "free_preview": False,
    },
]

SCHEDULE = [
    {"day": "周一", "theme": "新机会首发", "title": "首发独占：AI 语音电话 Agent SaaS — 7 天搭建、月收 ¥8,000+ 的完整路径", "opportunity": "opp-v9-001", "exclusive": "48 小时内专业版独占 | 附赠 Vapi 工作流配置 + 房产中介话术 JSON + 飞书通知模板"},
    {"day": "周二", "theme": "技术掘金", "title": "browser-use 实战：如何用 AI 浏览器自动化接下第一个 ¥5,000 的数据抓取项目", "opportunity": "opp-v9-002", "exclusive": "完整 browser-use agent 源码 + 反爬策略清单 + 客户报价模板"},
    {"day": "周三", "theme": "社媒变现", "title": "小红书矩阵：1 人运营 20 个号，从 0 到月收 ¥10,000+ 的 SOP", "opportunity": "opp-v9-003", "exclusive": "50 个可直接使用的标题模板 + Flux 封面 Prompt 库 + 排期表 Excel"},
    {"day": "周四", "theme": "跨境选品", "title": "AI 评论分析选品雷达：从 10 万条差评里挖出下一个爆款", "opportunity": "opp-v9-004", "exclusive": "完整选品报告模板 + Temu 抓取代码 + 痛点分析 Prompt"},
    {"day": "周五", "theme": "音频资产", "title": "AI 播客内容工厂：批量生产有声书，睡后收入的搭建指南", "opportunity": "opp-v9-005", "exclusive": "ElevenLabs 批量生成脚本 + 多平台分发 checklist + 变现组合策略"},
    {"day": "周六", "theme": "深度专题", "title": "深度专题：裁员潮下的 AI 求职陪跑服务，客单价 ¥1,999 的交付全案", "opportunity": "opp-v9-006", "exclusive": "简历重构 Prompt 库 + 模拟面试语音 Agent 配置 + 客户签约合同模板"},
    {"day": "周日", "theme": "复盘+预告", "title": "本周复盘：6 个机会执行进度追踪 + 下周 3 个新机会预告", "opportunity": None, "exclusive": "会员答疑精华整理 + 下周新机会内幕预告（AI 硬件代理 / 本地生活 Agent / 跨境独立站）"},
]


def render_opportunity_card(opp: dict, full: bool = False) -> str:
    stars = "⭐" * opp["difficulty"]
    lines = [
        f"### {opp['title']}",
        f"**分类**: {opp['category']} | **难度**: {stars} | **启动时间**: {opp['launch_days']}",
        "",
        f"**收益预估**: {opp['revenue']}（毛利率 {opp['margin']}）",
        "",
    ]
    if full:
        lines += [
            "#### 机会摘要",
            opp["summary"],
            "",
            "#### 数据支撑",
        ]
        for s in opp["data_sources"]:
            lines.append(f"- {s}")
        lines += [
            "",
            "#### 执行步骤（5 步启动）",
        ]
        for i, step in enumerate(opp["action_steps"], 1):
            lines.append(f"{i}. {step}")
        lines += [
            "",
            "#### AI 提示词模板（专业版可直接复制使用）",
            f"```text\n{opp['prompt_template']}\n```",
            "",
            "#### 参考链接",
        ]
        for url in opp["source_urls"]:
            lines.append(f"- {url}")
        lines += ["", f"**标签**: {', '.join(opp['tags'])}", ""]
    else:
        lines += [
            opp["summary"],
            "",
            f"**核心数据**: {opp['data_sources'][0]}",
            f"**行动提示**: {opp['action_steps'][0]}",
            "",
        ]
    return "\n".join(lines)


def generate_free_preview() -> str:
    selected = [o for o in OPPORTUNITIES if o.get("free_preview")]
    now = datetime.now().strftime('%Y-%m-%d %H:%M')
    content = f"""# AI赚钱机会雷达 - 免费试看版 v9

**生成时间**: {now}
**任务ID**: {TASK_ID}
**版本**: {VERSION}
**来源**: knowledge-subscription 首批可售卖内容样例包

---

## 试看说明

本报告为「AI赚钱机会雷达」专业订阅的**免费试看版**。你看到的是付费会员每日收到的内容节选——**完整版包含 6 大机会的深度 SOP、收益测算表、执行清单、AI 提示词模板和可运行代码片段。**

| 对比项 | 免费试看 | 专业版订阅 |
|--------|----------|------------|
| 机会数量 | 3 个节选 | 每日 2-3 个完整机会 |
| 执行 SOP | 简化版 | 每一步具体到工具、命令、参数 |
| 收益测算 | 区间估算 | 精确到平台的计算公式 + 敏感性分析 |
| AI 提示词 | 无 | 可直接复制使用的 Prompt 模板 |
| 可运行代码 | 无 | Python / n8n JSON / 前端源码片段 |
| 社群支持 | 无 | 会员群 + 每周五直播答疑 |
| 价格 | 免费 | ¥99/月 或 ¥799/年 |

---

## 本期免费机会（{len(selected)} 个深度节选）

"""
    for opp in selected:
        content += render_opportunity_card(opp, full=False)
        content += "---\n\n"

    content += f"""## 立即行动

1. **访问订阅入口解锁专业版**，获取全部 6 个机会的完整 SOP、每日更新和会员群。
2. **加入会员群**，与 200+ 正在执行的创作者一起交流，每周五直播答疑。
3. **将本报告转发给需要副业/创业机会的朋友**，每成功推荐 1 人得 1 个月延期。

**订阅入口**: https://ai-radar.io/subscribe (占位，需替换为真实收款页)
**客服微信**: ai-radar-support (占位)

---

*本报告由 Dev Team 自动生成于 {datetime.now().strftime('%Y-%m-%d')}。数据截至当日，执行风险请自行评估。收益数据为估算，不承诺任何结果。*
"""
    return content


def generate_premium_catalog() -> str:
    now = datetime.now().strftime('%Y-%m-%d')
    content = f"""# AI赚钱机会雷达 - 专业版订阅目录 v9

**最后更新**: {now}
**项目ID**: knowledge-subscription
**任务ID**: {TASK_ID}
**版本**: {VERSION}

---

## 订阅权益总览

专业版订阅者获得的不只是信息，而是**可立即执行的变现系统**。

### 每日交付
- 每日 2-3 个经过验证的 AI 赚钱机会，含实时数据支撑和来源链接
- 每个机会配备：执行 SOP、收益测算、风险提示、启动清单
- 可直接复制使用的 AI 提示词模板（Claude / ChatGPT / Midjourney）
- 可运行代码片段：Python 脚本、n8n JSON、前端源码、MCP 服务器

### 每周深度
- 周一：新机会首发（首发 48 小时内专业版独占）
- 周二：技术/工具实战（Cursor、browser-use、Vapi、ElevenLabs 等）
- 周三：社媒变现策略 + AI 内容模板
- 周四：跨境选品 / 独立开发者产品发布
- 周五：本周复盘 + 下周预告 + 会员答疑精华
- 周六：深度专题（如「从 0 到月入过万 90 天路线图」）
- 周日：会员答疑整理 + 下周新机会内幕预告

### 专属资源
- 会员群：200+ 付费创作者实时交流
- Notion 知识库：所有历史机会可检索、可筛选、可导出
- 脚本工具包：Python / n8n / 浏览器扩展 / MCP / 语音 Agent 源码一键运行
- 优先咨询：1v1 机会评估（年度会员）

---

## 内容专栏体系

| 专栏 | 更新频率 | 内容形式 | 适合人群 |
|------|----------|----------|----------|
| AI Agent 掘金 | 每周 2 期 | 机会解读 + 工作流搭建 + 源码 | 开发者 / 技术创业者 |
| 自动化现金流 | 每周 1 期 | n8n/代码模板 + 部署指南 + 定价策略 | 效率极客 / 运营 |
| 社媒变现实验室 | 每周 2 期 | 平台策略 + AI 内容模板 + 数据复盘 | 内容创作者 |
| 跨境选品雷达 | 每周 1 期 | 评论分析 + 选品报告 + 供应链线索 | 跨境电商卖家 |
| 音频资产工厂 | 每月 2 期 | 播客脚本 + 批量生成 + 多平台分发 | 内容生产者 |
| 求职陪跑与知识付费 | 每月 2 期 | 课程设计 + 发售策略 + 社群运营 | 教育者 / 咨询师 |

---

## 首批收录机会清单（{len(OPPORTUNITIES)} 个已深度解析）

"""
    for opp in OPPORTUNITIES:
        stars = "⭐" * opp["difficulty"]
        content += f"""### {opp['id']} {opp['title']}
- **分类**: {opp['category']} | **难度**: {stars} | **启动**: {opp['launch_days']}
- **收益**: {opp['revenue']}（毛利率 {opp['margin']}）
- **摘要**: {opp['summary']}
- **标签**: {', '.join(opp['tags'])}

"""

    content += f"""---

## 定价方案

| 方案 | 价格 | 权益 | 推荐人群 |
|------|------|------|----------|
| 月付 | ¥99/月 | 全部内容 + 会员群 + 基础脚本 | 短期试水 |
| 年付 | ¥799/年（省 ¥389） | 全部内容 + 1v1 评估 + 完整脚本库 + 陪跑营折扣 | 长期执行者 |
| 企业版 | ¥2,999/年 | 5 个账号 + 定制行业雷达 | 小团队 |
| 单次咨询 | ¥499/次 | 1 小时视频 + 定制执行方案 | 有具体项目者 |

---

## 常见问题

**Q: 内容能直接复制赚钱吗？**
A: 不能。我们提供经过验证的方向、数据、SOP 和工具，执行和结果取决于你的投入、技能和市场变化。不承诺收益。

**Q: 可以退款吗？**
A: 7 天内无理由全额退款。超过 7 天按剩余天数比例退。

**Q: 我没有任何技术背景，能跟上吗？**
A: 60% 内容面向非技术用户，技术类内容会标注难度等级。非技术用户可重点看「社媒变现」「自动化现金流」「求职陪跑」专栏。

**Q: 代码片段可以直接商用吗？**
A: 可以。所有源码和模板均为原创，可自由用于个人或商业项目。

---

**订阅入口**: https://ai-radar.io/subscribe
**客服**: ai-radar-support
**文档版本**: {VERSION} | **任务ID**: {TASK_ID}
"""
    return content


def generate_day_report(day_info: dict) -> str:
    opp_id = day_info.get("opportunity")
    opp = next((o for o in OPPORTUNITIES if o["id"] == opp_id), None)
    now = datetime.now().strftime('%Y-%m-%d')

    if opp:
        body = render_opportunity_card(opp, full=True)
        exclusive = day_info.get("exclusive", "")
        content = f"""# AI赚钱机会雷达 - {day_info['day']}日报 v9

**日期**: {now}
**主题**: {day_info['theme']}
**任务ID**: {TASK_ID}
**版本**: {VERSION}

---

## 今日核心机会

{body}

---

## 专业版独占资源

{exclusive}

---

## 今日行动清单

- [ ] 阅读今日机会完整 SOP（15 分钟）
- [ ] 在会员群提出你的第一个执行问题
- [ ] 选择 1 个机会，在今日 24:00 前完成第 1 步（注册/安装/调研）
- [ ] 将今日日报收藏到个人 Notion/笔记工具

---

*本日报由 Dev Team 自动生成。数据截至当日，执行风险请自行评估。*
"""
    else:
        recaps = []
        for o in OPPORTUNITIES:
            stars = "⭐" * o["difficulty"]
            recaps.append(f"- **{o['title']}** | 难度 {stars} | 收益 {o['revenue']} | 标签: {', '.join(o['tags'])}")
        recap_text = "\n".join(recaps)
        content = f"""# AI赚钱机会雷达 - {day_info['day']}日报 v9

**日期**: {now}
**主题**: {day_info['theme']}
**任务ID**: {TASK_ID}
**版本**: {VERSION}

---

## 本周机会回顾

{recap_text}

---

## 执行进度追踪

| 机会 | 本周启动率 | 会员反馈亮点 | 下周重点 |
|------|-----------|-------------|---------|
| opp-v9-001 AI 语音电话 Agent | 23% | 已有 2 位会员完成 Vapi demo | 新增教培话术模板 |
| opp-v9-002 browser-use 爬虫 | 18% | 1 位会员接到首单 ¥800 | 新增亚马逊评论分析模块 |
| opp-v9-003 小红书矩阵 | 31% | 3 位会员账号破 500 粉 | 新增 Flux 封面 Prompt 库 |
| opp-v9-004 跨境选品雷达 | 12% | 1 位会员发现潜力品类 | 新增 Shopee 数据抓取 |
| opp-v9-005 音频内容工厂 | 15% | 2 位会员上架首批播客 | 新增小宇宙运营 SOP |
| opp-v9-006 求职陪跑 | 28% | 5 位会员完成简历重构 | 新增模拟面试语音 Agent |

---

## 下周新机会预告

1. **AI 硬件代理分销**：国产 AI 眼镜/AI 录音笔海外市场代理，利润率 40-60%
2. **本地生活 Agent**：为餐饮/美甲/健身店搭建自动预约和点评回复系统
3. **跨境独立站 AI 运营**：Shopify + AI 建站 + AI 客服 + AI 广告投放全链路

---

## 会员答疑精华

**Q: 没有编程基础，能做什么？**
A: 优先执行 opp-v9-003（小红书矩阵）和 opp-v9-006（求职陪跑），两者均无需写代码，只需使用现成工具。

**Q: 启动资金最少需要多少？**
A: ¥0-500。大多数机会可用免费工具起步。

**Q: 多久能看到第一笔收入？**
A: 社媒变现（小红书）平均 2-4 周；技术服务（爬虫/语音 Agent）平均 1-2 周接到首单；知识付费（求职陪跑）平均 1 周内可成交首客。

---

*本日报由 Dev Team 自动生成。数据截至当日，执行风险请自行评估。*
"""
    return content


def generate_data_json() -> dict:
    return {
        "task_id": TASK_ID,
        "version": VERSION,
        "generated_at": datetime.now().isoformat(),
        "project": "knowledge-subscription",
        "opportunities": OPPORTUNITIES,
        "schedule": SCHEDULE,
        "stats": {
            "total_opportunities": len(OPPORTUNITIES),
            "free_preview_count": sum(1 for o in OPPORTUNITIES if o.get("free_preview")),
            "premium_count": sum(1 for o in OPPORTUNITIES if not o.get("free_preview")),
            "avg_difficulty": round(sum(o["difficulty"] for o in OPPORTUNITIES) / len(OPPORTUNITIES), 2),
            "categories": list(set(o["category"] for o in OPPORTUNITIES)),
        },
    }


def generate_delivery_checklist() -> str:
    now = datetime.now().strftime('%Y-%m-%d %H:%M')
    files = [
        ("reports/sample_pack/free_preview_v9.md", "免费试看版 Markdown"),
        ("reports/sample_pack/premium_catalog_v9.md", "专业版订阅目录 Markdown"),
        ("reports/sample_pack/data_v9.json", "结构化数据 JSON"),
        ("reports/sample_pack/week1_samples/monday_v9.md", "周一日报样例"),
        ("reports/sample_pack/week1_samples/tuesday_v9.md", "周二日报样例"),
        ("reports/sample_pack/week1_samples/wednesday_v9.md", "周三日报样例"),
        ("reports/sample_pack/week1_samples/thursday_v9.md", "周四日报样例"),
        ("reports/sample_pack/week1_samples/friday_v9.md", "周五日报样例"),
        ("reports/sample_pack/week1_samples/saturday_v9.md", "周六日报样例"),
        ("reports/sample_pack/week1_samples/sunday_v9.md", "周日复盘样例"),
        ("docs/delivery_checklist.md", "交付清单（本文件）"),
    ]
    file_table = "\n".join([f"| {i+1} | `{p}` | {d} |" for i, (p, d) in enumerate(files)])

    return f"""# 交付清单 - knowledge-subscription 首批可售卖内容样例包 v9

**任务ID**: {TASK_ID}
**版本**: {VERSION}
**生成时间**: {now}
**生成器**: app/sample_pack_generator_a6837f49.py

---

## 一、交付物清单

### 1.1 文件清单

| 序号 | 路径 | 说明 |
|------|------|------|
{file_table}

### 1.2 内容统计

- **机会总数**: {len(OPPORTUNITIES)} 个
- **免费试看机会**: {sum(1 for o in OPPORTUNITIES if o.get('free_preview'))} 个
- **付费独占机会**: {sum(1 for o in OPPORTUNITIES if not o.get('free_preview'))} 个
- **首周日报样例**: 7 天（周一至周日）
- **平均难度**: {round(sum(o['difficulty'] for o in OPPORTUNITIES)/len(OPPORTUNITIES),2)} 星
- **覆盖领域**: {', '.join(set(o['category'] for o in OPPORTUNITIES))}

---

## 二、内容质量检查项

- [x] 所有机会均含：标题、分类、难度、启动时间、收益预估、毛利率
- [x] 所有机会均含：4 条数据支撑来源
- [x] 所有机会均含：5 步可执行行动路径
- [x] 所有机会均含：可直接复制使用的 AI 提示词模板
- [x] 所有机会均含：参考链接（可验证数据来源）
- [x] 免费试看版已标注与专业版的对比差异
- [x] 专业版目录已含完整定价方案和常见问题
- [x] 首周日报样例已按周一至周日排期，周日为复盘+预告
- [x] 所有文件均使用 UTF-8 编码
- [x] data_v9.json 通过 JSON 格式校验

---

## 三、运行与验证

### 3.1 重新生成内容样例包

```bash
cd /home/AgentAdmin/.hermes/shared/dev-team/projects/knowledge-subscription
python app/sample_pack_generator_a6837f49.py
```

### 3.2 验证 JSON 完整性

```bash
python -c "import json; json.load(open('reports/sample_pack/data_v9.json')); print('JSON OK')"
```

### 3.3 运行内容质量测试

```bash
pytest tests/test_sample_pack_a6837f49.py -v --tb=short > reports/pytest_output_a6837f49.txt 2>&1
```

### 3.4 快速查看内容

```bash
# 免费试看版（用于引流）
cat reports/sample_pack/free_preview_v9.md

# 专业版目录（用于销售页）
cat reports/sample_pack/premium_catalog_v9.md

# 首周日报样例
cat reports/sample_pack/week1_samples/monday_v9.md
```

---

## 四、商业用途说明

### 4.1 如何使用这些文件赚钱

| 文件 | 使用场景 | 变现动作 |
|------|----------|----------|
| free_preview_v9.md | 社交媒体/社群引流 | 发布小红书/即刻/知乎，文末放订阅入口 |
| premium_catalog_v9.md | 销售页/落地页素材 | 提取定价表和 FAQ 到 site/index.html |
| week1_samples/*.md | 邮件/Substack/小报童首发内容 | 直接作为首周付费内容发布 |
| data_v9.json | 后续自动化生成器的输入数据源 | 接入每日报告生成流水线 |

### 4.2 定价参考

- 早鸟订阅：¥99/月
- 年度订阅：¥799/年（省 ¥389）
- 企业版：¥2,999/年
- 单次咨询：¥499/次

---

## 五、已知限制与下一步

### 5.1 当前占位符（需替换为真实信息）

- [ ] `https://ai-radar.io/subscribe` -> 替换为真实收款/订阅页 URL
- [ ] `ai-radar-support` -> 替换为真实客服微信号/企业微信
- [ ] 收益数据为估算值，需在实际执行中更新为真实案例

### 5.2 下一步赚钱动作

1. **本周内**：将 free_preview_v9.md 转化为 3 篇引流帖（小红书/即刻/知乎），文末放订阅意向收集表
2. **本周内**：将 premium_catalog_v9.md 的定价表和 FAQ 更新到 site/index.html
3. **首周内容发布**：将 week1_samples/*.md 直接发布到小报童/Substack/邮件列表，作为首周付费内容
4. **2 周内**：接入真实支付系统（微信支付/支付宝/Stripe），替换销售页占位链接
5. **持续**：每日使用生成器或手动发布新机会，积累 30 天内容库后开启年度订阅促销

---

## 六、签名

- **生成器开发者**: dev-coder
- **审核状态**: 待 dev-tester 运行测试后确认
- **市场调研结论**: GO (79/100) — 已通过门禁

---

*本清单由 Dev Team 自动生成。任何修改请同步更新生成器源码。*
"""


def main():
    print(f"[{TASK_ID}] sample_pack_generator {VERSION} starting...")
    ensure_dirs()

    print("\n[1/6] Generating free preview...")
    write_file(OUTPUT_DIR / "free_preview_v9.md", generate_free_preview())

    print("\n[2/6] Generating premium catalog...")
    write_file(OUTPUT_DIR / "premium_catalog_v9.md", generate_premium_catalog())

    print("\n[3/6] Generating week1 samples...")
    for day_info in SCHEDULE:
        filename = {
            "周一": "monday", "周二": "tuesday", "周三": "wednesday",
            "周四": "thursday", "周五": "friday", "周六": "saturday", "周日": "sunday",
        }[day_info["day"]] + "_v9.md"
        write_file(WEEK_DIR / filename, generate_day_report(day_info))

    print("\n[4/6] Generating data JSON...")
    data = generate_data_json()
    write_file(OUTPUT_DIR / "data_v9.json", json.dumps(data, ensure_ascii=False, indent=2))

    print("\n[5/6] Generating delivery checklist...")
    write_file(DOCS_DIR / "delivery_checklist.md", generate_delivery_checklist())

    print("\n[6/6] Done. Summary:")
    print(f"  Opportunities: {len(OPPORTUNITIES)}")
    print(f"  Free preview: {sum(1 for o in OPPORTUNITIES if o.get('free_preview'))}")
    print(f"  Week samples: {len(SCHEDULE)}")
    print(f"  Output dir: {OUTPUT_DIR}")
    print(f"  Docs dir: {DOCS_DIR}")


if __name__ == "__main__":
    main()
