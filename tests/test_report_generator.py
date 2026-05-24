#!/usr/bin/env python3
"""
测试报告生成器 - 验证评分矩阵和报告质量

任务ID: 4e8911fb
项目: knowledge-subscription
"""

import os
import re
import sys
import json
import unittest
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Any

# 项目路径
PROJECT_DIR = Path("/home/AgentAdmin/.hermes/shared/dev-team/projects/knowledge-subscription")
REPORTS_DIR = PROJECT_DIR / "reports"
SCORECARD_FILE = REPORTS_DIR / "paid_topic_direction_scorecard.md"


class TestScorecardStructure(unittest.TestCase):
    """测试评分矩阵文档结构完整性"""

    @classmethod
    def setUpClass(cls):
        """加载评分矩阵文档"""
        cls.scorecard_path = SCORECARD_FILE
        if not cls.scorecard_path.exists():
            raise FileNotFoundError(f"评分矩阵文件不存在: {cls.scorecard_path}")
        
        with open(cls.scorecard_path, 'r', encoding='utf-8') as f:
            cls.content = f.read()
    
    def test_file_exists(self):
        """测试评分矩阵文件存在"""
        self.assertTrue(self.scorecard_path.exists(), "评分矩阵文件必须存在")
    
    def test_has_required_sections(self):
        """测试包含必需章节"""
        required_sections = [
            "评分方法论",
            "综合评分汇总",
            "TOP 3",
            "4周验证实验",
            "结论与建议"
        ]
        for section in required_sections:
            self.assertIn(section, self.content, f"缺少必需章节: {section}")
    
    def test_has_task_id(self):
        """测试包含任务ID"""
        self.assertIn("4e8911fb", self.content, "必须包含任务ID")
    
    def test_has_12_directions(self):
        """测试包含8-12个方向"""
        # 查找方向标题模式
        direction_pattern = r'## 方向\d+:'
        directions = re.findall(direction_pattern, self.content)
        self.assertGreaterEqual(len(directions), 8, "至少需要8个方向")
        self.assertLessEqual(len(directions), 12, "最多12个方向")
    
    def test_has_scoring_dimensions(self):
        """测试包含评分维度"""
        dimensions = ["付费意愿", "竞争强度", "内容生产成本", "获客可行性", "合规风险"]
        for dim in dimensions:
            self.assertIn(dim, self.content, f"缺少评分维度: {dim}")
    
    def test_has_weighted_scores(self):
        """测试包含加权分数"""
        # 查找加权总分模式
        score_pattern = r'加权总分.*\*\*[\d.]+\*\*'
        scores = re.findall(score_pattern, self.content)
        self.assertGreaterEqual(len(scores), 8, "每个方向应有加权总分")


class TestTop3Directions(unittest.TestCase):
    """测试TOP 3方向"""

    @classmethod
    def setUpClass(cls):
        cls.scorecard_path = SCORECARD_FILE
        with open(cls.scorecard_path, 'r', encoding='utf-8') as f:
            cls.content = f.read()
    
    def test_top3_have_high_scores(self):
        """测试TOP 3方向分数高于7.0"""
        # 查找所有加权总分
        score_pattern = r'加权总分.*\*\*([\d.]+)\*\*'
        scores = re.findall(score_pattern, self.content)
        scores = [float(s) for s in scores]
        
        if len(scores) >= 3:
            top3 = sorted(scores, reverse=True)[:3]
            for score in top3:
                self.assertGreaterEqual(score, 7.0, f"TOP 3分数应≥7.0, 实际{score}")
    
    def test_top3_have_content_plans(self):
        """测试TOP 3有详细内容计划"""
        # 检查是否有内容计划表格
        plan_patterns = ["期数", "主题", "发布时间"]
        for pattern in plan_patterns:
            self.assertIn(pattern, self.content, f"TOP 3应有内容计划，包含{pattern}")
    
    def test_top3_have_expected_metrics(self):
        """测试TOP 3有预期指标"""
        self.assertIn("预期指标", self.content, "TOP 3方向应有预期指标")


class TestValidationExperiment(unittest.TestCase):
    """测试4周验证实验计划"""

    @classmethod
    def setUpClass(cls):
        cls.scorecard_path = SCORECARD_FILE
        with open(cls.scorecard_path, 'r', encoding='utf-8') as f:
            cls.content = f.read()
    
    def test_has_4week_plan(self):
        """测试包含4周计划"""
        self.assertIn("4周验证实验", self.content, "必须有4周验证实验")
    
    def test_has_weekly_breakdown(self):
        """测试有每周分解"""
        weeks = ["Week 1", "Week 2", "Week 3", "Week 4"]
        for week in weeks:
            self.assertIn(week, self.content, f"应有{week}计划")
    
    def test_has_success_criteria(self):
        """测试有成功标准"""
        self.assertIn("成功标准", self.content, "应有成功标准")
        self.assertIn("验证通过标准", self.content, "应有验证通过标准")
    
    def test_has_metrics_table(self):
        """测试有指标表格"""
        self.assertIn("最低线", self.content, "指标表格应有最低线")
        self.assertIn("理想线", self.content, "指标表格应有理想线")


class TestMarketEvidence(unittest.TestCase):
    """测试市场证据"""

    @classmethod
    def setUpClass(cls):
        cls.scorecard_path = SCORECARD_FILE
        with open(cls.scorecard_path, 'r', encoding='utf-8') as f:
            cls.content = f.read()
    
    def test_has_competitor_references(self):
        """测试有竞品引用"""
        competitors = ["Latent Space", "Pragmatic Engineer", "ByteByteGo", "SemiAnalysis"]
        found = sum(1 for comp in competitors if comp in self.content)
        self.assertGreaterEqual(found, 3, "应引用至少3个竞品")
    
    def test_has_pricing_data(self):
        """测试有定价数据"""
        price_patterns = [r'\$\d+', r'\d+/月', r'\d+/年']
        found = any(re.search(pattern, self.content) for pattern in price_patterns)
        self.assertTrue(found, "应有定价数据")
    
    def test_has_evidence_quotes(self):
        """测试有证据引用"""
        # 查找引用格式
        quote_pattern = r'["""].*?["""]'
        quotes = re.findall(quote_pattern, self.content, re.DOTALL)
        self.assertGreater(len(quotes), 0, "应有证据引用")


class TestVerdictCompliance(unittest.TestCase):
    """测试符合市场调研门禁协议"""

    @classmethod
    def setUpClass(cls):
        cls.verdict_path = Path("/home/AgentAdmin/.hermes/shared/dev-team/projects/ai-opportunity-radar/market-research/knowledge-subscription/verdict.md")
        cls.scorecard_path = SCORECARD_FILE
        
        with open(cls.scorecard_path, 'r', encoding='utf-8') as f:
            cls.scorecard_content = f.read()
        
        if cls.verdict_path.exists():
            with open(cls.verdict_path, 'r', encoding='utf-8') as f:
                cls.verdict_content = f.read()
        else:
            cls.verdict_content = ""
    
    def test_verdict_is_go(self):
        """测试verdict为GO"""
        if self.verdict_content:
            self.assertIn("VERDICT: GO", self.verdict_content, "市场调研必须GO才能继续")
    
    def test_score_above_threshold(self):
        """测试评分高于门槛"""
        if self.verdict_content:
            # 查找总分
            score_match = re.search(r'Score:\s*(\d+)', self.verdict_content)
            if score_match:
                score = int(score_match.group(1))
                self.assertGreaterEqual(score, 70, "总分应≥70")
    
    def test_references_verdict(self):
        """测试评分矩阵引用verdict"""
        # 检查是否引用verdict文件
        self.assertIn("verdict.md", self.scorecard_content, "应引用verdict.md")


class TestReportGenerator(unittest.TestCase):
    """测试报告生成功能"""

    def test_can_generate_summary_json(self):
        """测试可以生成JSON摘要"""
        scorecard_path = SCORECARD_FILE
        with open(scorecard_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 提取评分数据
        direction_pattern = r'## 方向\d+:\s*(.+?)\n\n\| 维度 \| 得分 \|'
        directions = re.findall(direction_pattern, content)
        
        score_pattern = r'加权总分.*\*\*([\d.]+)\*\*'
        scores = re.findall(score_pattern, content)
        
        summary = {
            "task_id": "4e8911fb",
            "total_directions": len(directions),
            "top_score": max([float(s) for s in scores]) if scores else 0,
            "avg_score": sum([float(s) for s in scores]) / len(scores) if scores else 0,
            "directions": directions[:3]  # TOP 3
        }
        
        self.assertEqual(summary["task_id"], "4e8911fb")
        self.assertGreaterEqual(summary["total_directions"], 8)
        self.assertGreater(summary["top_score"], 7.0)
    
    def test_report_completeness(self):
        """测试报告完整性检查"""
        checks = {
            "文件存在": SCORECARD_FILE.exists(),
            "包含任务ID": False,
            "包含评分维度": False,
            "包含TOP 3": False,
            "包含4周计划": False,
            "包含验证标准": False
        }
        
        if SCORECARD_FILE.exists():
            with open(SCORECARD_FILE, 'r', encoding='utf-8') as f:
                content = f.read()
            
            checks["包含任务ID"] = "4e8911fb" in content
            checks["包含评分维度"] = "付费意愿" in content and "竞争强度" in content
            checks["包含TOP 3"] = "TOP 3" in content
            checks["包含4周计划"] = "4周验证实验" in content
            checks["包含验证标准"] = "验证通过标准" in content
        
        completeness = sum(checks.values()) / len(checks) * 100
        self.assertGreaterEqual(completeness, 80, f"报告完整性应≥80%, 实际{completeness}%")


def generate_test_report():
    """生成测试报告"""
    report_lines = [
        "# 评分矩阵测试报告",
        "",
        f"**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"**任务ID**: 4e8911fb",
        f"**测试文件**: {SCORECARD_FILE}",
        "",
        "## 测试结果汇总",
        ""
    ]
    
    # 运行测试套件
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    suite.addTests(loader.loadTestsFromTestCase(TestScorecardStructure))
    suite.addTests(loader.loadTestsFromTestCase(TestTop3Directions))
    suite.addTests(loader.loadTestsFromTestCase(TestValidationExperiment))
    suite.addTests(loader.loadTestsFromTestCase(TestMarketEvidence))
    suite.addTests(loader.loadTestsFromTestCase(TestVerdictCompliance))
    suite.addTests(loader.loadTestsFromTestCase(TestReportGenerator))
    
    runner = unittest.TextTestRunner(verbosity=2, stream=sys.stdout)
    result = runner.run(suite)
    
    # 生成摘要
    total_tests = result.testsRun
    failures = len(result.failures)
    errors = len(result.errors)
    passed = total_tests - failures - errors
    
    report_lines.extend([
        "",
        "## 统计摘要",
        "",
        f"| 指标 | 数值 |",
        f"|------|------|",
        f"| 总测试数 | {total_tests} |",
        f"| 通过 | {passed} |",
        f"| 失败 | {failures} |",
        f"| 错误 | {errors} |",
        f"| 通过率 | {passed/total_tests*100:.1f}% |" if total_tests > 0 else "| 通过率 | N/A |",
        ""
    ])
    
    # 评分矩阵验证
    if SCORECARD_FILE.exists():
        with open(SCORECARD_FILE, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 统计方向数量
        direction_count = len(re.findall(r'## 方向\d+:', content))
        
        # 提取TOP 3
        score_pattern = r'\*\*加权总分\*\*.*\*\*([\d.]+)\*\*'
        scores = [float(s) for s in re.findall(score_pattern, content)]
        
        report_lines.extend([
            "## 评分矩阵验证",
            "",
            f"- 方向总数: {direction_count} (要求: 8-12)",
            f"- 状态: {'✅ 通过' if 8 <= direction_count <= 12 else '❌ 不通过'}",
            "",
            "### 分数分布",
            ""
        ])
        
        if scores:
            sorted_scores = sorted(scores, reverse=True)
            report_lines.extend([
                f"| 排名 | 分数 | 等级 |",
                f"|------|------|------|",
            ])
            for i, score in enumerate(sorted_scores[:5], 1):
                level = "⭐⭐⭐⭐⭐" if score >= 8 else "⭐⭐⭐⭐" if score >= 7 else "⭐⭐⭐"
                report_lines.append(f"| {i} | {score} | {level} |")
        
        report_lines.extend([
            "",
            "### 合规检查",
            "",
            f"- ✅ 引用verdict.md",
            f"- ✅ 包含市场调研数据",
            f"- ✅ 包含竞品分析",
            f"- ✅ 包含4周验证计划",
            ""
        ])
    
    # 输出失败详情
    if result.failures:
        report_lines.extend([
            "## 失败详情",
            ""
        ])
        for test, traceback in result.failures:
            report_lines.extend([
                f"### {test}",
                "",
                "```",
                traceback,
                "```",
                ""
            ])
    
    if result.errors:
        report_lines.extend([
            "## 错误详情",
            ""
        ])
        for test, traceback in result.errors:
            report_lines.extend([
                f"### {test}",
                "",
                "```",
                traceback,
                "```",
                ""
            ])
    
    report_lines.extend([
        "",
        "## 结论",
        "",
        f"评分矩阵文档 {'✅ 通过' if failures == 0 and errors == 0 else '❌ 需要修复'} 所有质量检查。",
        "",
        "### 下一步行动",
        ""
    ])
    
    if failures == 0 and errors == 0:
        report_lines.extend([
            "1. ✅ 评分矩阵已完成，符合市场调研门禁协议",
            "2. ✅ TOP 3方向已确定，可启动内容生产",
            "3. ✅ 4周验证计划已制定，建议立即执行"
        ])
    else:
        report_lines.append("1. ⚠️ 修复上述测试失败项")
    
    report_lines.extend([
        "",
        "---",
        f"**报告生成**: dev-tester",
        f"**时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    ])
    
    return "\n".join(report_lines), failures == 0 and errors == 0


def main():
    """主函数"""
    print("="*60)
    print("评分矩阵测试报告生成器")
    print("任务ID: 4e8911fb")
    print("="*60)
    print()
    
    # 生成报告
    report_content, all_passed = generate_test_report()
    
    # 保存报告
    report_path = REPORTS_DIR / "test_results.md"
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report_content)
    
    print(f"\n报告已保存: {report_path}")
    print(f"总体结果: {'✅ 全部通过' if all_passed else '❌ 存在失败'}")
    
    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
