#!/usr/bin/env python3
"""
AI赚钱机会雷达 - 数据采集与分析脚本
用途: 自动收集各渠道机会信息，生成每日机会雷达报告
版本: 1.0.0
作者: AI赚钱机会雷达团队
"""

import os
import json
import csv
import re
import asyncio
import aiohttp
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from dataclasses import dataclass, asdict
from pathlib import Path


@dataclass
class Opportunity:
    """机会数据结构"""
    id: str
    title: str
    category: str
    description: str
    data_sources: List[str]
    action_steps: List[str]
    profit_estimate: str
    difficulty: int  # 1-5
    time_to_start: str
    created_at: str
    source_urls: List[str]
    tags: List[str]
    
    def to_dict(self) -> Dict:
        return asdict(self)
    
    def to_markdown(self) -> str:
        """生成Markdown格式"""
        stars = "⭐" * self.difficulty
        sources_md = "\n".join([f"- {s}" for s in self.data_sources])
        steps_md = "\n".join([f"{i+1}. {step}" for i, step in enumerate(self.action_steps)])
        urls_md = "\n".join([f"- [{url[:50]}...]({url})" if len(url) > 50 else f"- {url}" for url in self.source_urls])
        
        return f"""
## {self.title}

**分类**: {self.category} | **难度**: {stars} | **启动时间**: {self.time_to_start}

### 机会摘要
{self.description}

### 数据支撑
{sources_md}

### 执行步骤
{steps_md}

### 盈利预估
{self.profit_estimate}

### 参考链接
{urls_md}

---
"""


class OpportunityRadar:
    """机会雷达主类"""
    
    def __init__(self, config_path: Optional[str] = None):
        self.config = self._load_config(config_path)
        self.opportunities: List[Opportunity] = []
        self.output_dir = Path(self.config.get('output_dir', './output'))
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def _load_config(self, config_path: Optional[str]) -> Dict:
        """加载配置"""
        default_config = {
            'output_dir': './output',
            'data_sources': {
                'github': True,
                'reddit': True,
                'hackernews': True,
                'producthunt': True
            },
            'categories': [
                'AI工具', '自动化', '独立开发者', '跨境电商'
            ]
        }
        
        if config_path and os.path.exists(config_path):
            with open(config_path, 'r', encoding='utf-8') as f:
                return {**default_config, **json.load(f)}
        return default_config
    
    async def fetch_github_trending(self, language: str = 'python', since: str = 'daily') -> List[Dict]:
        """获取GitHub热门项目"""
        # 注: 实际使用时需要API token
        url = f"https://api.github.com/search/repositories"
        params = {
            'q': f'language:{language} created:>{(datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")}',
            'sort': 'stars',
            'order': 'desc',
            'per_page': 10
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        return data.get('items', [])
        except Exception as e:
            print(f"GitHub API error: {e}")
        return []
    
    async def fetch_hackernews(self) -> List[Dict]:
        """获取Hacker News热门"""
        # 获取top stories IDs
        url = "https://hacker-news.firebaseio.com/v0/topstories.json"
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    if response.status == 200:
                        story_ids = await response.json()
                        stories = []
                        # 只获取前10个
                        for story_id in story_ids[:10]:
                            story_url = f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json"
                            async with session.get(story_url) as story_response:
                                if story_response.status == 200:
                                    story = await story_response.json()
                                    stories.append(story)
                        return stories
        except Exception as e:
            print(f"HackerNews API error: {e}")
        return []
    
    def generate_opportunity_id(self) -> str:
        """生成机会ID"""
        timestamp = datetime.now().strftime("%Y%m%d")
        count = len(self.opportunities) + 1
        return f"OPP-{timestamp}-{count:03d}"
    
    def add_opportunity(self, opportunity: Opportunity):
        """添加机会"""
        self.opportunities.append(opportunity)
    
    def generate_from_trends(self, trends_data: List[Dict], category: str = "AI工具") -> List[Opportunity]:
        """从趋势数据生成机会"""
        opportunities = []
        
        for item in trends_data[:5]:  # 只处理前5个
            opp = Opportunity(
                id=self.generate_opportunity_id(),
                title=f"基于 {item.get('name', '热门项目')} 的变现机会",
                category=category,
                description=f"该项目在GitHub获得 {item.get('stargazers_count', 0)} stars，表明市场关注度高",
                data_sources=[
                    f"GitHub Stars: {item.get('stargazers_count', 0)}",
                    f"创建时间: {item.get('created_at', 'N/A')}",
                    f"语言: {item.get('language', 'Unknown')}"
                ],
                action_steps=[
                    "研究该项目的核心功能",
                    "分析目标用户群体",
                    "设计变现模式（工具/服务/培训）",
                    "创建最小可行产品(MVP)",
                    "发布到目标平台"
                ],
                profit_estimate="$月入500-2000 (根据执行力)",
                difficulty=3,
                time_to_start="1-2周",
                created_at=datetime.now().isoformat(),
                source_urls=[item.get('html_url', '')],
                tags=[category, item.get('language', 'unknown'), 'trending']
            )
            opportunities.append(opp)
            self.add_opportunity(opp)
        
        return opportunities
    
    def export_to_markdown(self, filename: Optional[str] = None) -> str:
        """导出为Markdown报告"""
        if not filename:
            date_str = datetime.now().strftime("%Y-%m-%d")
            filename = f"opportunity_radar_{date_str}.md"
        
        filepath = self.output_dir / filename
        
        # 生成报告头
        header = f"""# AI赚钱机会雷达 | {datetime.now().strftime("%Y-%m-%d")}

**生成时间**: {datetime.now().strftime("%Y-%m-%d %H:%M")}  
**机会数量**: {len(self.opportunities)}  
**数据来源**: GitHub, Hacker News, 内部数据库

---

"""
        
        # 生成机会内容
        content = "\n".join([opp.to_markdown() for opp in self.opportunities])
        
        # 生成摘要
        summary = f"""
## 摘要

| 类别 | 数量 | 平均难度 |
|-----|------|--------|
"""
        categories = {}
        for opp in self.opportunities:
            cat = opp.category
            if cat not in categories:
                categories[cat] = {'count': 0, 'difficulty': 0}
            categories[cat]['count'] += 1
            categories[cat]['difficulty'] += opp.difficulty
        
        for cat, data in categories.items():
            avg_diff = data['difficulty'] / data['count'] if data['count'] > 0 else 0
            stars = "⭐" * int(round(avg_diff))
            summary += f"| {cat} | {data['count']} | {stars} |\n"
        
        full_report = header + content + summary
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(full_report)
        
        return str(filepath)
    
    def export_to_csv(self, filename: Optional[str] = None) -> str:
        """导出为CSV"""
        if not filename:
            date_str = datetime.now().strftime("%Y-%m-%d")
            filename = f"opportunities_{date_str}.csv"
        
        filepath = self.output_dir / filename
        
        if not self.opportunities:
            return ""
        
        fieldnames = ['id', 'title', 'category', 'description', 'profit_estimate', 
                     'difficulty', 'time_to_start', 'created_at', 'tags']
        
        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for opp in self.opportunities:
                row = opp.to_dict()
                row['tags'] = ', '.join(row['tags'])
                row['data_sources'] = ', '.join(row['data_sources'])
                row['action_steps'] = ', '.join(row['action_steps'])
                row['source_urls'] = ', '.join(row['source_urls'])
                writer.writerow({k: row.get(k, '') for k in fieldnames})
        
        return str(filepath)
    
    def export_to_json(self, filename: Optional[str] = None) -> str:
        """导出为JSON"""
        if not filename:
            date_str = datetime.now().strftime("%Y-%m-%d")
            filename = f"opportunities_{date_str}.json"
        
        filepath = self.output_dir / filename
        
        data = {
            'generated_at': datetime.now().isoformat(),
            'count': len(self.opportunities),
            'opportunities': [opp.to_dict() for opp in self.opportunities]
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        return str(filepath)


# 示例机会数据
SAMPLE_OPPORTUNITIES = [
    {
        'title': 'MCP Server开发: 电商数据查询Server',
        'category': 'AI工具',
        'description': '为跨境电商卖家开发MCP Server，支持Temu/Shein/淘宝店铺数据查询',
        'data_sources': [
            'GitHub mcp-servers topic: 12,400+ stars',
            'Reddit r/Claude MCP讨论: 2,300+/月',
            'Claude官方集成Server: 仅15个'
        ],
        'action_steps': [
            '研究目标电商平台API',
            '实现店铺数据查询接口',
            '部署到Smithery/Glama',
            '设计定价策略'
        ],
        'profit_estimate': '$500-3000/月 (按次调用或订阅)',
        'difficulty': 3,
        'time_to_start': '1-2周',
        'source_urls': ['https://smithery.ai', 'https://glama.ai'],
        'tags': ['MCP', '跨境电商', 'API']
    },
    {
        'title': 'n8n自动化工作流模板市场',
        'category': '自动化',
        'description': '制作高价值n8n工作流模板，在Gumroad和国内平台销售',
        'data_sources': [
            'n8n官方模板市场仅200+模板',
            '"n8n workflow" 搜索量月增45%',
            'Gumroad模板售价$9-49'
        ],
        'action_steps': [
            '选择热门场景(小红书/邮件/客服)',
            '制作完整工作流',
            '编写详细使用文档',
            '在多平台上架销售'
        ],
        'profit_estimate': '$300-1500/月 (模板可重复销售)',
        'difficulty': 2,
        'time_to_start': '3-5天',
        'source_urls': ['https://n8n.io', 'https://gumroad.com'],
        'tags': ['n8n', '自动化', '模板']
    },
    {
        'title': 'Newsletter内容运营服务',
        'category': '独立开发者',
        'description': '为企业/个人提供Newsletter代运营服务',
        'data_sources': [
            '全球Newsletter市场$20B',
            '小报童头部作者月入¥5万-20万',
            '企业内容营销需求激增'
        ],
        'action_steps': [
            '确定垂直行业',
            '搭建内容生产SOP',
            '寻找第一个客户',
            '扩展服务范围'
        ],
        'profit_estimate': '¥3000-15000/月',
        'difficulty': 2,
        'time_to_start': '1周',
        'source_urls': ['https://xiaobot.net'],
        'tags': ['Newsletter', '内容', '服务']
    }
]


def create_sample_report():
    """创建示例报告"""
    radar = OpportunityRadar()
    
    # 添加示例机会
    for i, data in enumerate(SAMPLE_OPPORTUNITIES, 1):
        opp = Opportunity(
            id=f"OPP-{datetime.now().strftime('%Y%m%d')}-{i:03d}",
            title=data['title'],
            category=data['category'],
            description=data['description'],
            data_sources=data['data_sources'],
            action_steps=data['action_steps'],
            profit_estimate=data['profit_estimate'],
            difficulty=data['difficulty'],
            time_to_start=data['time_to_start'],
            created_at=datetime.now().isoformat(),
            source_urls=data['source_urls'],
            tags=data['tags']
        )
        radar.add_opportunity(opp)
    
    # 导出各种格式
    md_path = radar.export_to_markdown('sample_report.md')
    json_path = radar.export_to_json('sample_data.json')
    csv_path = radar.export_to_csv('sample_data.csv')
    
    print(f"✅ 示例报告已生成:")
    print(f"   Markdown: {md_path}")
    print(f"   JSON: {json_path}")
    print(f"   CSV: {csv_path}")
    
    return radar


if __name__ == "__main__":
    # 运行示例
    create_sample_report()
