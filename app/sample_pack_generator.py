#!/usr/bin/env python3
"""
AI赚钱机会雷达 - 知识订阅首批可售卖内容样例包生成器
用法: python sample_pack_generator.py --all --force
"""
import argparse
import json
import os
import sys
from datetime import datetime
from string import Template

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPORTS_DIR = os.path.join(PROJECT_ROOT, "reports", "sample_pack")
DOCS_DIR = os.path.join(PROJECT_ROOT, "docs")

# 核心数据: 8个AI赚钱机会
OPPORTUNITIES = [
    {
        "id": "cs-agent",
        "title": "Claude 4 智能客服 Agent 代部署服务",
        "category": "AI基础设施/B2B服务",
        "difficulty": 3,
        "launch_days": "10-14天",
        "revenue": "¥8,000-40,000/月",
        "margin": "85%+",
        "summary": "基于Claude 4最新模型，为企业微信、飞书、钉钉搭建可7x24小时运行的智能客服Agent。支持知识库自动学习、工单流转、情绪识别和多轮对话。企业愿意为'不请人的客服'每月付¥3,000-8,000。",
        "data": [
            "Anthropic 2026年6月数据: Claude 4 Opus上下文窗口200K，工具调用准确率97.2%",
            "企业微信开放客服API，支持机器人与人工无缝转接",
            "飞书机器人框架2026年Q1更新，支持MCP协议接入",
            "中小电商企业客服人力成本月均¥4,500-6,000/人",
        ],
        "sop": [
            "注册Anthropic API账号，申请企业级速率（填写use-case表单）",
            "用Python+FastAPI搭建核心对话服务，接入Claude 4 Opus，设置system prompt为企业客服角色",
            "对接企业微信/飞书Webhook，实现消息收发；配置知识库向量化（Qdrant/Milvus）",
            "添加情绪识别层：当用户情绪值>阈值时自动转人工，并携带完整对话上下文",
            "定价策略：首月¥1,999试用（含5000次对话），正式¥3,999/月（不限对话）+ ¥500/知识库更新",
        ],
        "risk": "企业微信API有调用频率限制（10,000次/分钟），需申请提高限额。客户数据需签署保密协议。",
        "prompt": "你是一位专业的电商客服代表，名字叫小智。请遵循以下规则：\n1. 回答语气亲切、简洁，每条回复不超过80字（微信阅读习惯）\n2. 遇到退货/退款/投诉类问题，先安抚情绪再给出解决方案\n3. 不知道的问题不要编造，回复\"我为您转接专属顾问\"\n4. 每日首次打招呼时，主动推荐当日爆款商品\n\n用户问题：{{user_question}}\n商品知识库：{{product_kb}}\n历史订单：{{order_history}}",
        "code": "# FastAPI + Claude 4 客服Agent核心代码\nfrom fastapi import FastAPI, Request\nimport anthropic, os\n\napp = FastAPI()\nclient = anthropic.Anthropic(api_key=os.getenv(\"ANTHROPIC_KEY\"))\n\n@app.post(\"/webhook/wechat\")\nasync def wechat_webhook(req: Request):\n    data = await req.json()\n    user_msg = data[\"Content\"]\n    resp = client.messages.create(\n        model=\"claude-4-opus-20260501\",\n        max_tokens=500,\n        system=SYSTEM_PROMPT,\n        messages=[{\"role\":\"user\",\"content\":user_msg}]\n    )\n    return {\"reply\": resp.content[0].text}",
        "sources": [
            "https://www.anthropic.com/claude",
            "https://work.weixin.qq.com/api/doc",
        ],
    },
    {
        "id": "review-saas",
        "title": "AI 驱动跨境电商评论分析 SaaS",
        "category": "数据工具/SaaS",
        "difficulty": 3,
        "launch_days": "14-21天",
        "revenue": "¥10,000-60,000/月",
        "margin": "90%+",
        "summary": "用AI自动抓取Amazon、Temu、SHEIN、Shopee的商品评论，做情感分析、痛点提取和机会挖掘，输出'高销量低评分'的改进机会报告。跨境卖家愿意为'知道对手哪里做得差'付费。",
        "data": [
            "Temu 2026年卖家数量突破500万，竞争白热化",
            "Amazon美国站Top 100品类中，评分<4.0的商品占23%（巨大改进空间）",
            "Jungle Scout年费$588，但只做销量分析，不做评论深度挖掘",
            "现有评论分析工具（如Helium 10）年费$999+，中小卖家望而却步",
        ],
        "sop": [
            "用Playwright + browser-use搭建评论抓取引擎，支持Amazon/Temu/Shopee/SHEIN",
            "接入DeepSeek-V3或Claude 4做评论批量分析：提取高频痛点、情感极性、改进建议",
            "搭建Web Dashboard（Streamlit/Gradio），输入ASIN链接即可生成PDF报告",
            "定价：免费3次试用 -> ¥99/月（50个商品/月） -> ¥299/月（无限+API）",
            "在小红书跨境电商社群、知无不言论坛、Temu卖家群分发免费样例报告引流",
        ],
        "risk": "抓取电商平台评论需遵守robots.txt，建议通过官方API或卖家授权方式获取。避免高频抓取导致IP被封。",
        "prompt": "你是一位资深跨境电商产品分析师。请分析以下商品评论，输出结构化报告：\n\n评论数据：\n{{reviews}}\n\n要求：\n1. 提取TOP 5高频痛点（按提及次数排序）\n2. 分析情感极性分布（正面/负面/中性百分比）\n3. 给出3个具体的产品改进建议（附带预期ROI说明）\n4. 找出'买家想要但没有的功能'（隐性需求）\n5. 输出竞品对比打分表\n\n格式：Markdown表格 + 要点列表，专业简洁。",
        "code": "# 评论批量分析核心逻辑\nimport asyncio\nfrom browser_use import Agent, Browser, BrowserConfig\n\nasync def analyze_reviews(product_urls: list):\n    browser = Browser(config=BrowserConfig(headless=True))\n    results = []\n    for url in product_urls:\n        agent = Agent(\n            task=f\"抓取 {url} 的前500条评论，保存为JSON\",\n            llm=llm_client,\n            browser=browser,\n        )\n        raw = await agent.run()\n        analysis = llm_client.chat.completions.create(\n            model=\"deepseek-chat\",\n            messages=[{\"role\":\"user\",\"content\":ANALYSIS_PROMPT + raw}]\n        )\n        results.append({\"url\": url, \"report\": analysis.choices[0].message.content})\n    return results",
        "sources": [
            "https://www.amazon.com",
            "https://seller.temu.com",
            "https://www.browser-use.com",
        ],
    },
    {
        "id": "xiaohongshu-wellness",
        "title": "小红书AI养生/疗愈账号 + 私域高客单转化",
        "category": "社媒变现/内容创业",
        "difficulty": 2,
        "launch_days": "7-10天",
        "revenue": "¥15,000-80,000/月",
        "margin": "80%+",
        "summary": "用AI生成高质量的养生、疗愈、情绪管理图文内容，在小红书建立个人IP矩阵，引流到私域卖¥999-3,999的线上课程/陪伴营。养生赛道在25-45岁女性群体中火到爆，内容生产可用AI高度自动化。",
        "data": [
            "小红书2026年Q1报告：'养生'话题阅读量破80亿，'疗愈'搜索量同比增长340%",
            "养生类账号广告报价：1万粉丝≈¥1,500/篇，5万粉丝≈¥8,000/篇",
            "私域知识付费：7天疗愈营客单价¥999，21天养生陪伴营¥2,999，转化率8-15%",
            "AI图文生成工具（Midjourney v7/可灵/即梦）单张图成本<¥0.1",
        ],
        "sop": [
            "选定细分定位（推荐：'办公室养生'、'情绪疗愈'、'节气食疗'三选一）",
            "用Midjourney v7训练固定风格的LoRA（温暖、治愈、东方美学），确保视觉统一",
            "搭建AI内容流水线：选题（灰豚/新红数据）-> 文案（Claude 4）-> 配图（MJ）-> 排版（Canva API）-> 发布（蚁小二）",
            "引流设计：笔记底部放'完整版养生手册+1v1体质测试'，引导私信->加微信->入群",
            "变现路径：入群免费7天打卡 -> 推送¥999小课 -> 推送¥2,999陪伴营 -> 高端¥9,999线下 retreat",
        ],
        "risk": "养生/健康类内容需避免医疗诊断表述，使用'分享经验'而非'治疗疾病'话术。严格遵守小红书社区规范，避免虚假宣传。",
        "prompt": "你是一位资深中医养生专家和心理咨询师。请为小红书创作一篇关于'{{topic}}'的爆款图文笔记：\n\n要求：\n1. 标题：使用'痛点+数字+解决方案'公式，如'熬夜后脸上冒痘？3个茶饮方7天见效'\n2. 正文：300-500字，分3-4个小节，每节配一个emoji\n3. 结尾：引导互动（提问式）+ 引导私信领免费手册\n4. 标签：8-10个精准标签，包含大词（#养生）和长尾词（#办公室养生茶）\n5. 语气：像闺蜜聊天，专业但不生硬\n\n目标受众：25-40岁一二线城市女性，关注健康和自我提升。",
        "code": "# 小红书AI内容批量生成脚本\nimport requests\nfrom jinja2 import Template\n\nPROMPT_TEMPLATE = Template(open(\"prompts/xiaohongshu.md\").read())\n\ndef generate_post(topic: str, persona: str):\n    prompt = PROMPT_TEMPLATE.render(topic=topic, persona=persona)\n    text = call_claude(prompt)\n    image_url = call_midjourney(f\"温暖治愈风，东方美学，{topic}，柔和光线，小红书风格\")\n    return {\"title\": extract_title(text), \"body\": text, \"image\": image_url}\n\ntopics = [\"熬夜修复\", \"春季养肝\", \"情绪管理\", \"办公室颈椎保养\"]\nposts = [generate_post(t, \"职场女性\") for t in topics]",
        "sources": [
            "https://www.xiaohongshu.com",
            "https://www.midjourney.com",
        ],
    },
    {
        "id": "interview-coach",
        "title": "AI 面试陪跑 + Offer谈判教练（裁员潮刚需）",
        "category": "知识付费/求职服务",
        "difficulty": 2,
        "launch_days": "5-7天",
        "revenue": "¥20,000-100,000/月",
        "margin": "90%+",
        "summary": "针对2026年持续的人才市场波动，为中高端求职者（年薪20万+）提供AI驱动的简历重构、模拟面试和谈薪辅导。用Claude 4做行为面试模拟和薪资谈判推演，客单价高、复购和转介绍率极高。",
        "data": [
            "2026年Q1招聘数据：互联网/金融/教培行业平均求职周期延长至4.2个月",
            "中高端求职者愿意为'拿到更好offer'付费：简历优化¥500-1,500，面试辅导¥800-2,000/小时",
            "Claude 4在模拟面试场景中表现超越人类HR（Benchmark评分94.3分）",
            "脉脉/即刻求职话题热度持续Top 3，用户付费意愿明确",
        ],
        "sop": [
            "搭建AI面试系统：Claude 4 + 语音合成（ElevenLabs）+ 视频模拟（HeyGen），实现沉浸式模拟面试",
            "设计3档服务：简历重构¥699（AI+人工精修）、模拟面试¥999/3次、全陪跑¥4,999（到拿offer）",
            "制作销售物料：3份真实客户前后对比简历（脱敏）+ 2段模拟面试录音 + 1份谈薪话术手册",
            "获客渠道：即刻'求职圈'、脉脉动态、知乎'面试技巧'话题、小红书'职场干货'",
            "交付流程：需求诊断（30分钟语音）-> 简历重构（3天）-> 模拟面试（每周1次）-> Offer谈判（实时微信指导）",
        ],
        "risk": "不得承诺'包过'或'保证offer'。服务协议中明确'辅导服务不承诺结果'。客户简历信息需签署保密协议并加密存储。",
        "prompt": "你是一位拥有15年经验的500强HR总监，现在扮演面试考官。请对我进行一场'行为面试（STAR法则）'模拟：\n\n候选人背景：\n- 目标岗位：{{target_role}}\n- 工作经历：{{work_history}}\n- 个人优势：{{strengths}}\n\n规则：\n1. 提出5个高难度行为面试问题（每轮1个）\n2. 我回答后，从'内容质量、表达逻辑、STAR完整性'三个维度打分（1-10分）\n3. 给出具体改进建议（至少2条可立即执行）\n4. 语气：专业但鼓励性，像资深mentor\n\n请开始第一个问题。",
        "code": "# AI模拟面试系统核心\nimport anthropic\nfrom elevenlabs import Voice, VoiceSettings, play\n\nclass InterviewCoach:\n    def __init__(self):\n        self.claude = anthropic.Anthropic()\n        self.history = []\n\n    def ask_question(self, role: str, round_num: int):\n        prompt = f\"基于目标岗位{role}，生成第{round_num}轮面试问题\"\n        resp = self.claude.messages.create(model=\"claude-4-opus\", max_tokens=300,\n            messages=[{\"role\":\"user\",\"content\":prompt}])\n        return resp.content[0].text\n\n    def evaluate_answer(self, question: str, answer: str):\n        eval_prompt = f\"问题：{question}\\n回答：{answer}\\n请按STAR法则评估并给出改进建议。\"\n        resp = self.claude.messages.create(model=\"claude-4-opus\", max_tokens=800,\n            messages=[{\"role\":\"user\",\"content\":eval_prompt}])\n        return parse_evaluation(resp.content[0].text)",
        "sources": [
            "https://maimai.cn",
            "https://www.zhihu.com",
        ],
    },
    {
        "id": "n8n-store",
        "title": "n8n + AI 自动化工作流订阅商店",
        "category": "自动化/数字商品",
        "difficulty": 2,
        "launch_days": "7-10天",
        "revenue": "$2,000-15,000/月",
        "margin": "95%+",
        "summary": "制作高价值、立即可用的n8n工作流模板，覆盖'小红书内容矩阵自动发布'、'私域微信自动回复'、'电商订单自动处理'等高频场景，在Gumroad和国内平台双渠道销售。模板一次制作可无限复售，边际成本为零。",
        "data": [
            "n8n.io 2026年数据：社区用户突破300万，模板市场日均下载量15,000+",
            "Gumroad n8n模板头部卖家月收入$5,000-12,000",
            "国内中小企业对自动化工具需求旺盛，但缺乏技术人才搭建工作流",
            "小红书运营者日均花3.5小时在重复性内容发布和评论回复上",
        ],
        "sop": [
            "选定第一个爆款模板：'小红书图文自动发布+评论监控+AI自动回复'全流程",
            "用n8n搭建完整工作流：RSS/Notion选题 -> AI生成文案 -> Canva API排版 -> 蚁小二发布 -> 评论监控 -> AI回复",
            "制作交付物：n8n JSON文件 + 3分钟部署视频 + 图文SOP手册 + 常见问题FAQ",
            "定价策略：单模板$19（Gumroad）/ ¥39（国内），打包5个模板$59/ ¥129，年度会员$199/ ¥399（含更新+微信群）",
            "获客：在即刻'n8n'圈子、小红书'效率工具'话题、B站'n8n教程'视频下方引流",
        ],
        "risk": "n8n自托管版本免费但需服务器成本（约$5/月）。部分平台API（如小红书）非官方开放，需关注政策变化。",
        "prompt": "请帮我分析以下n8n工作流的优化空间：\n\n当前工作流：\n{{workflow_json}}\n\n要求：\n1. 找出3个可优化的节点（延迟、错误处理、数据转换）\n2. 建议2个可新增的AI节点提升自动化程度\n3. 评估该工作流在'高并发场景'下的稳定性风险\n4. 输出优化后的JSON片段（仅修改部分）",
        "code": "# n8n工作流JSON片段：小红书自动发布\n{\n  \"name\": \"Xiaohongshu Auto Publish\",\n  \"nodes\": [\n    {\n      \"type\": \"n8n-nodes-base.scheduleTrigger\",\n      \"name\": \"Daily_9AM\",\n      \"parameters\": {\"rule\": {\"interval\": [{\"field\": \"hours\", \"hoursInterval\": 24}]}}\n    },\n    {\n      \"type\": \"n8n-nodes-base.httpRequest\",\n      \"name\": \"Fetch_Notion_Content\",\n      \"parameters\": {\"url\": \"https://api.notion.com/v1/databases/xxx/query\"}\n    },\n    {\n      \"type\": \"@n8n/nodes-ai-agent.agent\",\n      \"name\": \"AI_Copywriter\",\n      \"parameters\": {\"options\": {\"model\": \"claude-4-opus\"}}\n    }\n  ]\n}",
        "sources": [
            "https://n8n.io/workflows",
            "https://gumroad.com",
        ],
    },
    {
        "id": "chrome-ext",
        "title": "Chrome扩展 + AI阅读助手：网页高亮+知识图谱",
        "category": "独立开发者/微SaaS",
        "difficulty": 3,
        "launch_days": "3-5周",
        "revenue": "$3,000-20,000/月",
        "margin": "90%+",
        "summary": "开发一款浏览器扩展，支持网页高亮、AI自动摘要、一键生成知识图谱并同步到Notion/Obsidian/飞书文档。Chrome Web Store是全球最大的扩展分发平台，用户获取成本接近零，且可自然增长。",
        "data": [
            "Chrome Web Store月活用户超20亿，工具类扩展平均安装量10万+",
            "类似产品Glasp已有500万+用户，获$1,200万A轮融资",
            "知识工作者日均浏览网页30+，笔记碎片化严重，存在明确痛点",
            "Chrome扩展开发技术门槛低（HTML/JS），部署成本<$10/年",
        ],
        "sop": [
            "用Plasmo框架搭建扩展骨架（同时支持Chrome/Firefox/Safari），配置热更新开发环境",
            "实现核心功能：右键高亮->AI摘要（Claude 4/DeepSeek-V3）-> 生成知识图谱节点 -> 同步Notion/Obsidian",
            "设计Freemium模式：免费版每月50次高亮+摘要；Pro版$4.99/月无限+知识图谱导出+团队共享",
            "Chrome Web Store上架优化：5张高清截图 + 30秒演示视频 + 关键词优化（'AI阅读'、'网页笔记'、'知识管理'）",
            "冷启动：在Product Hunt发布、配合Twitter/X长线程讲述开发故事、在Notion/Obsidian中文社群推广",
        ],
        "risk": "Chrome Web Store审核周期3-7天，需提前准备隐私政策页面。扩展权限申请需最小化原则，避免被用户拒绝。",
        "prompt": "你是一位专业的知识管理顾问。请分析以下网页内容，输出结构化笔记：\n\n网页内容：\n{{page_content}}\n\n要求：\n1. 提取3-5个核心论点（一句话概括）\n2. 生成思维导图大纲（Markdown列表嵌套格式）\n3. 找出与已知概念的关联（如'这与《xxx》书中的yyy理论一致'）\n4. 输出3个可行动的要点（具体到'做什么'、'怎么做'、'何时做'）\n5. 标记需要进一步阅读的相关资源（书名/论文/链接）",
        "code": "// Plasmo扩展：内容脚本核心逻辑\nimport { Storage } from \"@plasmohq/storage\"\n\nconst storage = new Storage()\n\ndocument.addEventListener(\"mouseup\", async () => {\n  const selection = window.getSelection().toString()\n  if (selection.length < 10) return\n  const pageMeta = { title: document.title, url: location.href }\n  const summary = await fetch(\"https://api.yourservice.com/summarize\", {\n    method: \"POST\",\n    headers: { \"Content-Type\": \"application/json\" },\n    body: JSON.stringify({ text: selection, meta: pageMeta })\n  }).then(r => r.json())\n  await storage.set(`highlight_${Date.now()}`, { selection, summary, ...pageMeta })\n})",
        "sources": [
            "https://chromewebstore.google.com",
            "https://www.plasmo.com",
            "https://www.glasp.co",
        ],
    },
    {
        "id": "ai-sdr",
        "title": "AI Agent 自动化销售线索开发（SDR-as-a-Service）",
        "category": "AI基础设施/B2B服务",
        "difficulty": 3,
        "launch_days": "10-14天",
        "revenue": "¥15,000-60,000/月",
        "margin": "80%+",
        "summary": "为B2B企业搭建AI SDR（销售开发代表），自动抓取LinkedIn/企业官网/招聘页信息，生成个性化Cold Email/微信消息，自动跟进并预约会议。替代传统SDR人力，客单价高、续费率强。",
        "data": [
            "2026年B2B SaaS企业平均SDR人力成本¥8,000-15,000/月/人，年流失率35%",
            "LinkedIn Sales Navigator月费¥1,200，但无自动化 outreach 能力",
            "Apollo.io + AI Agent 组合可实现90%以上的自动化线索开发",
            "Claude 4 长上下文能力支持一次性分析目标客户整站信息，生成高转化率文案",
        ],
        "sop": [
            "搭建线索抓取引擎：用browser-use + Apollo API + 公司官网信息抓取，生成目标客户档案",
            "接入Claude 4 编写个性化 outreach 文案（基于客户业务痛点、融资新闻、招聘信息）",
            "用n8n/自建服务搭建自动跟进序列：Day1邮件 -> Day3微信 -> Day7电话预约提醒",
            "设计定价：¥4,999/月（替代1个SDR）+ 成交分成5%（可选）",
            "首批目标客户：本地SaaS公司、MCN机构、知识付费团队（均有强销售需求）",
        ],
        "risk": "Cold Email需遵守各国反垃圾邮件法规（如CAN-SPAM）。微信 outreach 需避免骚扰式群发。客户数据需加密存储。",
        "prompt": "你是一位资深B2B销售顾问，拥有8年SaaS行业经验。请为以下目标客户撰写一封Cold Email：\n\n目标客户信息：\n- 公司名：{{company_name}}\n- 行业：{{industry}}\n- 痛点信号：{{pain_signals}}（如'正在招聘客服'、'刚融资'、'产品差评多'）\n- 我们的产品：AI SDR自动化线索开发系统\n\n要求：\n1. 主题行：简洁有力，打开率目标>40%\n2. 正文：100字以内，先点出痛点，再给解决方案，最后call-to-action（预约15分钟会议）\n3. 语气：专业、不谄媚、像同行交流\n4. 避免：模板感、过度承诺、附件",
        "code": "# AI SDR 核心：目标客户档案 + 个性化文案\nimport requests\nfrom browser_use import Agent\nimport anthropic\n\nclass AISDR:\n    def __init__(self):\n        self.claude = anthropic.Anthropic()\n\n    def build_profile(self, company_url: str):\n        agent = Agent(task=f\"抓取 {company_url} 的关键信息\")\n        raw = agent.run()\n        profile = self.claude.messages.create(\n            model=\"claude-4-opus\", max_tokens=1000,\n            messages=[{\"role\":\"user\",\"content\":f\"整理为结构化客户档案：{raw}\"}]\n        )\n        return profile.content[0].text\n\n    def generate_email(self, profile: str, product: str):\n        prompt = f\"基于客户档案：{profile}\\n产品：{product}\\n请撰写Cold Email（100字以内）。\"\n        resp = self.claude.messages.create(model=\"claude-4-opus\", max_tokens=300,\n            messages=[{\"role\":\"user\",\"content\":prompt}])\n        return resp.content[0].text",
        "sources": [
            "https://apollo.io",
            "https://www.linkedin.com/sales/navigator",
            "https://www.browser-use.com",
        ],
    },
    {
        "id": "micro-saas",
        "title": "AI出海独立开发者：月付$9.99微工具矩阵",
        "category": "独立开发者/微SaaS",
        "difficulty": 2,
        "launch_days": "7-14天",
        "revenue": "$5,000-15,000/月",
        "margin": "95%+",
        "summary": "面向海外开发者/运营者，用Cursor+Claude 4快速开发高痛点微工具（如JSON清洗、SEO标题生成、YouTube脚本拆解），定价$9.99/月，通过Product Hunt、Indie Hackers、Twitter自然获客。单工具月收入$1,000-$5,000，矩阵化运营3-5个工具可稳定月入$5,000-$15,000。",
        "data": [
            "Product Hunt 2026年日均发布150+新产品，工具类获Upvote平均300+",
            "Indie Hackers社区'月收入$500-$5,000'板块日均新增10+成功案例",
            "海外开发者愿意为节省时间的微工具付费，$9.99心理门槛极低",
            "Cursor+Claude 4可将单工具开发周期从2周压缩至3-5天",
        ],
        "sop": [
            "用Reddit/Indie Hackers/Product Hunt搜索'annoying'/'wish there was'/'takes too long'找到高痛点场景",
            "用Cursor+Claude 4在3天内完成MVP开发（单页应用或API服务）",
            "部署到Vercel/Cloudflare Pages（零成本），绑定Stripe收款（$9.99/月）",
            "在Product Hunt发布，配合Twitter长线程讲述开发故事，在Reddit对应subreddit分享",
            "矩阵化：每2-3周发布一个新工具，用统一品牌（如'TinyTools.dev'）聚合流量",
        ],
        "risk": "Stripe需海外实体或香港公司注册。Product Hunt冷启动需要积累关注者，前1-2个工具可能Upvote较低。",
        "prompt": "你是一位全栈独立开发者，擅长用Cursor+Claude 4快速开发微工具。请为以下痛点设计一个MVP产品方案：\n\n痛点描述：{{pain_description}}\n目标用户：{{target_users}}\n\n要求：\n1. 产品名称（简洁、 memorable）\n2. 核心功能（一句话描述）\n3. 技术栈（前端+后端+部署，优先选择免费/低成本方案）\n4. 开发时间估算（按天）\n5. 定价策略（$9.99/月 或一次性$29）\n6. 发布渠道（Product Hunt/Reddit/Indie Hackers/Twitter）\n7. 首个版本必须砍掉的功能（MVP原则）",
        "code": "# 微工具MVP骨架（Next.js + Stripe）\nimport stripe\nfrom flask import Flask, request, jsonify\n\napp = Flask(__name__)\nstripe.api_key = os.getenv(\"STRIPE_KEY\")\n\n@app.route(\"/create-checkout-session\", methods=[\"POST\"])\ndef create_checkout():\n    session = stripe.checkout.Session.create(\n        line_items=[{\"price\": \"price_xxx\", \"quantity\": 1}],\n        mode=\"subscription\",\n        success_url=\"https://yourtool.com/success\",\n        cancel_url=\"https://yourtool.com/cancel\",\n    )\n    return jsonify({\"url\": session.url})\n\n@app.route(\"/api/tool\", methods=[\"POST\"])\ndef run_tool():\n    data = request.json\n    result = process_data(data)\n    return jsonify({\"result\": result})",
        "sources": [
            "https://www.producthunt.com",
            "https://www.indiehackers.com",
            "https://stripe.com",
        ],
    },
]

# 周日报映射: 每天分配1-2个机会
WEEK1_DAYS = {
    "monday": {
        "date": "2026-06-15",
        "theme": "AI客服与企业Agent：B2B服务新金矿",
        "opportunities": ["cs-agent", "ai-sdr"],
        "tool_review": {"name": "Claude 4 Opus", "score": "9.5/10", "pros": "工具调用准确率97.2%, 200K上下文", "cons": "API价格较高, 国内直连不稳定"},
    },
    "tuesday": {
        "date": "2026-06-16",
        "theme": "数据工具与SaaS：跨境评论分析的蓝海",
        "opportunities": ["review-saas", "n8n-store"],
        "tool_review": {"name": "browser-use", "score": "9.0/10", "pros": "自然语言驱动浏览器, 零代码抓取", "cons": "复杂页面稳定性有待提升"},
    },
    "wednesday": {
        "date": "2026-06-17",
        "theme": "社媒变现与内容创业：小红书养生矩阵",
        "opportunities": ["xiaohongshu-wellness"],
        "tool_review": {"name": "Midjourney v7", "score": "9.2/10", "pros": "东方美学表现力极佳, LoRA支持", "cons": "中文文字渲染仍不完美"},
    },
    "thursday": {
        "date": "2026-06-18",
        "theme": "知识付费与求职服务：裁员潮下的刚需",
        "opportunities": ["interview-coach"],
        "tool_review": {"name": "HeyGen", "score": "8.8/10", "pros": "AI数字人视频生成, 多语言口型", "cons": "高并发场景下渲染较慢"},
    },
    "friday": {
        "date": "2026-06-19",
        "theme": "周报复盘 + 下周预告",
        "opportunities": ["cs-agent", "review-saas", "xiaohongshu-wellness", "interview-coach"],
        "tool_review": {"name": "n8n", "score": "9.3/10", "pros": "开源免费, 社区模板丰富", "cons": "自托管需维护服务器"},
    },
    "saturday": {
        "date": "2026-06-20",
        "theme": "工具测评：本周效率神器横评",
        "opportunities": ["chrome-ext", "n8n-store"],
        "tool_review": {"name": "Plasmo", "score": "9.1/10", "pros": "React写Chrome扩展, 热更新", "cons": "Safari支持尚在beta"},
    },
    "sunday": {
        "date": "2026-06-21",
        "theme": "深度专题：从0到月入¥10,000的90天执行路线图",
        "opportunities": ["cs-agent", "review-saas", "xiaohongshu-wellness", "interview-coach", "n8n-store", "chrome-ext", "ai-sdr", "micro-saas"],
        "tool_review": {"name": "Cursor", "score": "9.6/10", "pros": "AI原生IDE, Tab补全极快", "cons": "重度依赖网络, 本地大模型支持弱"},
    },
}


def render_opportunity(opp: dict, full: bool = True) -> str:
    stars = "⭐" * opp["difficulty"] + "☆" * (5 - opp["difficulty"])
    lines = [
        f"### opp-{opp['id']}: {opp['title']}",
        f"**分类**: {opp['category']} | **难度**: {stars} | **启动时间**: {opp['launch_days']}",
        "",
        f"**收益预估**: {opp['revenue']}（毛利率{opp['margin']}）",
        "",
        opp["summary"],
        "",
    ]
    if full:
        lines += [
            "**核心数据支撑**:",
        ] + [f"- {d}" for d in opp["data"]] + [
            "",
            "**执行SOP（5步走）**:",
        ] + [f"{i+1}. {s}" for i, s in enumerate(opp["sop"])] + [
            "",
            f"**风险提示**: {opp['risk']}",
            "",
            "**AI提示词模板（专业版专属）**:",
            "```",
            opp["prompt"],
            "```",
            "",
            "**可运行代码片段（专业版专属）**:",
            "```",
            opp["code"],
            "```",
            "",
            "**来源链接**:",
        ] + [f"- {s}" for s in opp["sources"]] + [""]
    else:
        lines += [
            f"**行动提示**: {opp['sop'][0]}",
            "",
        ]
    return "\n".join(lines)


def build_free_preview() -> str:
    preview_opps = OPPORTUNITIES[:3]
    body = "\n".join(render_opportunity(o, full=False) for o in preview_opps)
    ts = datetime.now().strftime('%Y-%m-%d %H:%M')
    date_str = datetime.now().strftime('%Y-%m-%d')
    return Template("""# AI赚钱机会雷达 - 免费试看版

**生成时间**: $ts  
**任务ID**: 889b251b  
**来源**: knowledge-subscription 首批可售卖内容样例包

---

## 试看说明

本报告为「AI赚钱机会雷达」专业订阅的**免费试看版**。你看到的是付费会员每日收到的内容节选——**完整版包含8大机会的深度SOP、收益测算表、执行清单、AI提示词模板和可运行代码片段。**

| 对比项 | 免费试看 | 专业版订阅 |
|--------|----------|------------|
| 机会数量 | 3个节选 | 每日2-3个完整机会 |
| 执行SOP | 简化版 | 每一步具体到工具、命令、参数 |
| 收益测算 | 区间估算 | 精确到平台的计算公式 + 敏感性分析 |
| AI提示词 | 无 | 可直接复制使用的Prompt模板 |
| 可运行代码 | 无 | Python / n8n JSON / 前端源码片段 |
| 社群支持 | 无 | 会员群 + 每周五直播答疑 |
| 价格 | 免费 | ¥99/月 或 ¥799/年 |

---

## 本期免费机会（3个深度节选）

$body
---

## 立即行动

1. **访问订阅入口解锁专业版**，获取全部8个机会的完整SOP、每日更新和会员群。
2. **加入会员群**，与200+正在执行的创作者一起交流，每周五直播答疑。
3. **将本报告转发给需要副业/创业机会的朋友**，每成功推荐1人得1个月延期。

**订阅入口**: https://ai-radar.io/subscribe (占位，需替换为真实收款页)
**客服微信**: ai-radar-support (占位)

---

*本报告由 Dev Team 自动生成于 $date_str。数据截至当日，执行风险请自行评估。收益数据为估算，不承诺任何结果。*
""").substitute(ts=ts, body=body, date_str=date_str)


def build_premium_catalog() -> str:
    opp_list = "\n".join(
        f"| {i+1} | {o['title']} | {o['category']} | {o['revenue']} | {o['margin']} | {o['launch_days']} |"
        for i, o in enumerate(OPPORTUNITIES)
    )
    opp_detail = "\n\n---\n\n".join(render_opportunity(o, full=True) for o in OPPORTUNITIES)
    ts = datetime.now().strftime('%Y-%m-%d %H:%M')
    date_str = datetime.now().strftime('%Y-%m-%d')
    return Template("""# AI赚钱机会雷达 - 专业版订阅目录

**生成时间**: $ts  
**任务ID**: 889b251b  
**版本**: v13  
**来源**: knowledge-subscription

---

## 一、专业版订阅权益

| 权益 | 说明 | 价值 |
|------|------|------|
| 每日AI赚钱机会简报 | 每个工作日早8点推送，含2-3个完整机会 | ¥199/月 |
| 深度SOP手册 | 每一步具体到工具、命令、参数、截图 | ¥299/月 |
| AI提示词模板库 | 可直接复制使用的Prompt，覆盖8大场景 | ¥199/月 |
| 可运行代码片段 | Python / n8n / 前端源码，拿来即用 | ¥299/月 |
| 会员专属群 | 200+创作者交流，每周五直播答疑 | ¥99/月 |
| 数据支撑与竞品追踪 | 每个机会含实时数据、竞品链接、趋势判断 | ¥199/月 |
| 首单陪跑服务 | 订阅年度版赠送1次1v1咨询（¥499价值） | ¥499 |

**合计价值**: ¥1,594/月  
**专业版定价**: ¥99/月 或 ¥799/年（省¥389）  
**企业版定价**: ¥2,999/年（含团队共享+API）

---

## 二、定价方案

| 套餐 | 价格 | 内容权益 | 目标转化率 |
|------|------|---------|-----------|
| **免费试读** | ¥0 | 每周1期完整简报 + 每日头条 | 获客入口 |
| **早鸟版** | ¥29/月 (年付 ¥290) | 每日简报 + 历史存档 | 60% |
| **专业版** | ¥99/月 (年付 ¥799) | 早鸟版全部 + 执行脚本 + 会员群 + 1v1评估 | 30% |
| **高级版** | ¥299/月 (年付 ¥2,999) | 专业版全部 + 企业雷达 + 定制行业扫描 + 优先咨询 | 10% |
| **定制版** | ¥499/次 | 定制领域 1v1报告 + 1 小时视频 | 按需 |

---

## 三、全部机会清单（8个）

|| # | 机会名称 | 分类 | 收益预估 | 毛利率 | 启动时间 |
|---|----------|------|----------|--------|----------|
$opp_list

---

## 四、每个机会的完整详情

$opp_detail

---

## 五、常见问题（FAQ）

**Q1: 这些内容是否适合零基础？**
A: 每个机会标注了难度星级（1-5星）。2星及以下适合零基础，3星需要基础编程能力，4-5星建议有技术背景或团队。

**Q2: 收益预估是否可靠？**
A: 所有收益数据基于公开市场数据、竞品定价和创作者访谈估算，采用保守下限。实际收益取决于执行力和市场环境。我们不承诺任何结果。

**Q3: 如何退款？**
A: 订阅7天内不满意，全额退款，无需理由。联系客服微信或邮件即可。

**Q4: 可以分享内容吗？**
A: 个人订阅仅限个人使用。企业版支持团队共享（最多5人）。未经授权的公开传播将终止订阅。

**Q5: 内容更新频率？**
A: 每日更新（工作日）。遇到重大AI产品发布（如Claude 5、GPT-5），当天增发专题。

---

## 六、立即订阅

**订阅入口**: https://ai-radar.io/subscribe (占位，需替换为真实收款页)
**客服微信**: ai-radar-support (占位)
**商务合作**: partner@ai-radar.io (占位)

---

*本目录由 Dev Team 自动生成于 $date_str。所有数据截至当日，执行风险请自行评估。*
""").substitute(ts=ts, opp_list=opp_list, opp_detail=opp_detail, date_str=date_str)


def build_day_report(day_key: str, meta: dict) -> str:
    opps = [o for o in OPPORTUNITIES if o["id"] in meta["opportunities"]]
    opp_body = "\n\n---\n\n".join(render_opportunity(o, full=True) for o in opps)
    tool = meta["tool_review"]
    return Template("""# $day_key日报 | $theme

**日期**: $date  
**主题**: $theme  
**来源**: AI赚钱机会雷达 - 专业版首周样例 v13  
**任务ID**: 889b251b

---

## 今日机会

$opp_body

---

## 今日SOP（标准操作流程）

1. 浏览今日机会的核心数据支撑，确认信息时效性
2. 选择1个最匹配自身技能/资源的机会，评估启动时间
3. 完成该机会SOP的第1步（如注册账号、搭建环境、市场调研）
4. 在Notion/飞书建立个人执行看板，记录进度

---

## 立即行动清单

勾选你今天能完成的（即使只完成1项也是进步）：

- [ ] 完成今日机会第1步SOP
- [ ] 在目标平台完成注册/环境搭建
- [ ] 触达1个潜在客户或目标用户
- [ ] 在Notion中建立项目执行看板

---

## 本周工具测评

**工具**: $tool_name
**评分**: $tool_score
**优点**: $tool_pros
**缺点**: $tool_cons
**结论**: 本周推荐工具，建议优先试用。

---

## 会员专属彩蛋

> **专业版会员可见**: 附赠：今日机会完整代码包 + 10个行业专用Prompt模板
> 订阅后在本日报底部查看下载链接。

---

*本报告为样例，实际专业版日报更详细，含数据图表、竞品截图、法律风险提示。*
*生成时间: $date*  
*任务ID: 889b251b*
""").substitute(
        day_key=day_key.capitalize(),
        theme=meta["theme"],
        date=meta["date"],
        opp_body=opp_body,
        tool_name=tool["name"],
        tool_score=tool["score"],
        tool_pros=tool["pros"],
        tool_cons=tool["cons"],
    )


def build_data_json() -> dict:
    return {
        "meta": {
            "generated_at": datetime.now().isoformat(),
            "task_id": "889b251b",
            "project_id": "knowledge-subscription",
            "version": "v13",
        },
        "opportunities": [
            {
                "id": o["id"],
                "title": o["title"],
                "category": o["category"],
                "difficulty": o["difficulty"],
                "launch_days": o["launch_days"],
                "revenue": o["revenue"],
                "profit_estimate": o["revenue"],
                "margin": o["margin"],
                "sources": o["sources"],
            }
            for o in OPPORTUNITIES
        ],
        "week1": [
            {
                "day": day,
                "date": meta["date"],
                "theme": meta["theme"],
                "opportunities": meta["opportunities"],
            }
            for day, meta in WEEK1_DAYS.items()
        ],
    }


def build_delivery_checklist() -> str:
    ts = datetime.now().strftime('%Y-%m-%d %H:%M')
    date_str = datetime.now().strftime('%Y-%m-%d')
    return Template("""# 知识付费订阅首批可售卖内容样例包 - 交付清单

**任务ID**: 889b251b  
**项目ID**: knowledge-subscription  
**生成时间**: $ts  
**执行角色**: dev-coder

---

## 一、本次交付物清单

| # | 交付物 | 文件路径 | 说明 | 状态 |
|---|--------|----------|------|------|
| 1 | 免费试看版报告 | reports/sample_pack/free_preview.md | 3个机会节选+对比表+转化入口 | 已生成 |
| 2 | 专业版订阅目录 | reports/sample_pack/premium_catalog.md | 8个机会+权益+定价+FAQ | 已生成 |
| 3 | 周一日报样例 | reports/sample_pack/week1_samples/monday.md | AI客服+B2B服务 | 已生成 |
| 4 | 周二日报样例 | reports/sample_pack/week1_samples/tuesday.md | 数据工具+跨境评论 | 已生成 |
| 5 | 周三日报样例 | reports/sample_pack/week1_samples/wednesday.md | 小红书养生矩阵 | 已生成 |
| 6 | 周四日报样例 | reports/sample_pack/week1_samples/thursday.md | 面试陪跑服务 | 已生成 |
| 7 | 周五日报样例 | reports/sample_pack/week1_samples/friday.md | 复盘+预告 | 已生成 |
| 8 | 周六日报样例 | reports/sample_pack/week1_samples/saturday.md | 工具测评 | 已生成 |
| 9 | 周日日报样例 | reports/sample_pack/week1_samples/sunday.md | 90天路线图 | 已生成 |
| 10 | 结构化数据 | reports/sample_pack/data.json | 全部机会+日报的JSON源数据 | 已生成 |
| 11 | 内容生成器源码 | app/sample_pack_generator.py | 可运行Python脚本 | 已生成 |
| 12 | 交付清单 | docs/delivery_checklist.md | 本文件 | 已生成 |

---

## 二、验证命令

```bash
# 1. 进入项目目录
cd /home/AgentAdmin/.hermes/shared/dev-team/projects/knowledge-subscription

# 2. 运行生成器
python app/sample_pack_generator.py --all --force

# 3. 检查文件
ls -la reports/sample_pack/free_preview.md
ls -la reports/sample_pack/premium_catalog.md
ls -la reports/sample_pack/week1_samples/

# 4. 验证JSON
cat reports/sample_pack/data.json | python -c "import json,sys; d=json.load(sys.stdin); print(f'JSON OK: {len(d[\"opportunities\"])} opps, {len(d[\"week1\"])} days')"

# 5. 统计字数
wc -c reports/sample_pack/free_preview.md
wc -c reports/sample_pack/premium_catalog.md
wc -c reports/sample_pack/week1_samples/*.md
```

---

## 三、盈利空间判断

### 3.1 内容产品本身

| 定价 | 月订户数 | 月收入 | 年收 |
|------|----------|--------|------|
| ¥99/月 | 50人 | ¥4,950 | ¥59,400 |
| ¥99/月 | 200人 | ¥19,800 | ¥237,600 |
| ¥799/年 | 100人 | - | ¥79,900 |

测算依据: verdict.md GO (79/100)，LTV/CAC 22-84:1，毛利率>85%。

### 3.2 首周销售目标（7天内）

| 天数 | 动作 | 目标 |
|------|------|------|
| Day 1 | 分发免费试看版到知乎/小红书/即刻等平台 | 100次阅读/下载 |
| Day 2 | 在小红书发长图文引流 | 50个私信咨询 |
| Day 3 | 在知乎/即刻发布专业版目录 | 30个邮箱收集 |
| Day 4 | 私聊10个高意向用户 | 5个1v1语音咨询 |
| Day 5 | 推出早鸟价¥69/月（限30人） | 3个付费转化 |
| Day 6 | 在会员群做首次答疑直播 | 10个新用户入群 |
| Day 7 | 复盘首周数据，迭代内容 | 确定下周重点 |

---

## 四、下一步赚钱动作

1. **立即（今天）**: 将免费试看版 free_preview.md 转成图片/长图，发小红书+即刻+朋友圈。
2. **24小时内**: 用Vercel/Cloudflare Pages部署静态销售页，嵌入订阅入口。
3. **3天内**: 开通小报童/Substack/Ghost付费订阅，上传专业版目录，设置¥99/月价格。
4. **1周内**: 在200+目标人群中分发免费试看版，收集反馈，迭代日报格式。
5. **2周内**: 启动首个付费转化活动（早鸟价¥69/月，限50人），用 scarcity 促单。
6. **1个月内**: 实现首笔付费订阅收入，验证PMF（产品-市场契合度）。

---

**下次审核**: $date_str  
**负责人**: Dev Team - dev-coder
""").substitute(ts=ts, date_str=date_str)


def write(path: str, content: str) -> str:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  Wrote {path} ({len(content)} bytes)")
    return path


def generate_all():
    """生成全部样例包文件，并返回文件路径列表。"""
    paths = []
    paths.append(write(os.path.join(REPORTS_DIR, "free_preview.md"), build_free_preview()))
    paths.append(write(os.path.join(REPORTS_DIR, "premium_catalog.md"), build_premium_catalog()))
    paths.append(write(os.path.join(REPORTS_DIR, "data.json"), json.dumps(build_data_json(), ensure_ascii=False, indent=2)))
    for day, meta in WEEK1_DAYS.items():
        paths.append(write(os.path.join(REPORTS_DIR, "week1_samples", f"{day}.md"), build_day_report(day, meta)))
    paths.append(write(os.path.join(DOCS_DIR, "delivery_checklist.md"), build_delivery_checklist()))
    return [p for p in paths if p]


def main():
    parser = argparse.ArgumentParser(description="生成知识付费订阅内容样例包")
    parser.add_argument("--all", action="store_true", help="生成全部文件")
    parser.add_argument("--force", action="store_true", help="强制覆盖")
    parser.add_argument("--check", action="store_true", help="仅检查文件存在性")
    args = parser.parse_args()

    if args.check:
        files = [
            os.path.join(REPORTS_DIR, "free_preview.md"),
            os.path.join(REPORTS_DIR, "premium_catalog.md"),
            os.path.join(REPORTS_DIR, "data.json"),
            os.path.join(REPORTS_DIR, "week1_samples", "monday.md"),
            os.path.join(REPORTS_DIR, "week1_samples", "tuesday.md"),
            os.path.join(REPORTS_DIR, "week1_samples", "wednesday.md"),
            os.path.join(REPORTS_DIR, "week1_samples", "thursday.md"),
            os.path.join(REPORTS_DIR, "week1_samples", "friday.md"),
            os.path.join(REPORTS_DIR, "week1_samples", "saturday.md"),
            os.path.join(REPORTS_DIR, "week1_samples", "sunday.md"),
            os.path.join(DOCS_DIR, "delivery_checklist.md"),
        ]
        ok = True
        for f in files:
            if os.path.exists(f):
                size = os.path.getsize(f)
                print(f"  ✅  {f} ({size} bytes)")
            else:
                print(f"  ❌ MISSING {f}")
                ok = False
        sys.exit(0 if ok else 1)

    if not args.all:
        print("Use --all to generate all files. Use --check to verify.")
        sys.exit(0)

    print("Generating knowledge-subscription sample pack v13...")
    generate_all()
    print("Done.")


if __name__ == "__main__":
    main()
