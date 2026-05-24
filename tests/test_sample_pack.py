#!/usr/bin/env python3
"""
Sample Pack 质量验证测试
Task: 7691939d
验证: free_preview, premium_catalog, week1_samples, data.json, delivery_checklist
"""

import json
import os
import re
import sys
import unittest
from datetime import datetime
from pathlib import Path

PROJECT_DIR = Path("/home/AgentAdmin/.hermes/shared/dev-team/projects/knowledge-subscription")
SAMPLE_PACK_DIR = PROJECT_DIR / "reports" / "sample_pack"
WEEK1_DIR = SAMPLE_PACK_DIR / "week1_samples"
DOCS_DIR = PROJECT_DIR / "docs"


class TestFileExistence(unittest.TestCase):
    def test_free_preview_exists(self):
        self.assertTrue((SAMPLE_PACK_DIR / "free_preview_v3.md").exists())

    def test_premium_catalog_exists(self):
        self.assertTrue((SAMPLE_PACK_DIR / "premium_catalog_v2.md").exists())

    def test_data_json_exists(self):
        self.assertTrue((SAMPLE_PACK_DIR / "data.json").exists())

    def test_delivery_checklist_exists(self):
        self.assertTrue((DOCS_DIR / "delivery_checklist.md").exists())

    def test_week1_samples_exist(self):
        days = ["monday_v2.md", "tuesday_v2.md", "wednesday_v2.md",
                "thursday_v2.md", "friday_v2.md", "saturday_v2.md", "sunday_v2.md"]
        for day in days:
            self.assertTrue((WEEK1_DIR / day).exists(), f"缺少 {day}")


class TestFreePreviewContent(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        path = SAMPLE_PACK_DIR / "free_preview_v3.md"
        cls.content = path.read_text(encoding="utf-8")

    def test_has_comparison_table(self):
        self.assertIn("免费试看", self.content)
        self.assertIn("专业版订阅", self.content)

    def test_has_three_opportunities(self):
        # 至少3个 ### 标题
        headers = re.findall(r"^### ", self.content, re.MULTILINE)
        self.assertGreaterEqual(len(headers), 3, "免费试看应至少含3个机会")

    def test_has_cta(self):
        self.assertIn("订阅入口", self.content)
        self.assertIn("立即行动", self.content)

    def test_no_overpromise(self):
        bad_words = ["稳赚", " guaranteed", "包赚", "零风险", "无脑", "躺赚"]
        found = [w for w in bad_words if w in self.content]
        self.assertEqual(len(found), 0, f"发现过度承诺词汇: {found}")

    def test_has_profit_estimates(self):
        # 包含收益数字模式
        self.assertTrue(re.search(r"[¥$]\d+", self.content), "应含收益估算")


class TestPremiumCatalogContent(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        path = SAMPLE_PACK_DIR / "premium_catalog_v2.md"
        cls.content = path.read_text(encoding="utf-8")

    def test_has_pricing(self):
        self.assertIn("定价方案", self.content)
        self.assertIn("¥99", self.content)

    def test_has_faq(self):
        self.assertIn("常见问题", self.content)
        self.assertIn("退款", self.content)

    def test_has_columns(self):
        self.assertIn("专栏", self.content)
        self.assertIn("更新频率", self.content)

    def test_has_six_opportunities(self):
        opp_headers = re.findall(r"^### opp-", self.content, re.MULTILINE)
        self.assertGreaterEqual(len(opp_headers), 6, "专业版目录应含6个机会")


class TestWeek1SamplesContent(unittest.TestCase):
    def test_all_have_sop(self):
        days = ["monday_v2.md", "tuesday_v2.md", "wednesday_v2.md",
                "thursday_v2.md", "friday_v2.md", "saturday_v2.md", "sunday_v2.md"]
        for day in days:
            content = (WEEK1_DIR / day).read_text(encoding="utf-8")
            self.assertIn("SOP", content, f"{day} 缺少 SOP")

    def test_all_have_checklist(self):
        days = ["monday_v2.md", "tuesday_v2.md", "wednesday_v2.md",
                "thursday_v2.md", "friday_v2.md", "saturday_v2.md", "sunday_v2.md"]
        for day in days:
            content = (WEEK1_DIR / day).read_text(encoding="utf-8")
            self.assertIn("行动清单", content, f"{day} 缺少行动清单")

    def test_all_have_member_exclusive(self):
        days = ["monday_v2.md", "tuesday_v2.md", "wednesday_v2.md",
                "thursday_v2.md", "friday_v2.md", "saturday_v2.md", "sunday_v2.md"]
        for day in days:
            content = (WEEK1_DIR / day).read_text(encoding="utf-8")
            self.assertIn("会员专属", content, f"{day} 缺少会员专属彩蛋")


class TestDataJson(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.load(open(SAMPLE_PACK_DIR / "data.json", encoding="utf-8"))

    def test_has_opportunities(self):
        self.assertIn("opportunities", self.data)
        self.assertGreaterEqual(len(self.data["opportunities"]), 6)

    def test_each_opportunity_has_required_fields(self):
        required = {"id", "title", "category", "profit_estimate", "difficulty", "time_to_start"}
        for opp in self.data["opportunities"]:
            missing = required - set(opp.keys())
            self.assertEqual(len(missing), 0, f"机会 {opp.get('id')} 缺少字段: {missing}")

    def test_has_schedule(self):
        self.assertIn("week1_schedule", self.data)
        self.assertEqual(len(self.data["week1_schedule"]), 7)


class TestDeliveryChecklist(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.content = (DOCS_DIR / "delivery_checklist.md").read_text(encoding="utf-8")

    def test_has_task_id(self):
        self.assertIn("7691939d", self.content)

    def test_has_verification_commands(self):
        self.assertIn("验证命令", self.content)
        self.assertIn("python app/sample_pack_generator.py", self.content)

    def test_has_profit_analysis(self):
        self.assertIn("盈利空间判断", self.content)
        self.assertIn("月收入", self.content)

    def test_has_next_steps(self):
        self.assertIn("下一步赚钱动作", self.content)


def generate_report(result: unittest.TestResult) -> str:
    lines = [
        "# Sample Pack 质量验证报告",
        "",
        f"**任务ID**: 7691939d",
        f"**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"**执行角色**: dev-coder",
        "",
        "## 测试统计",
        "",
        f"| 指标 | 数值 |",
        f"|------|------|",
        f"| 总测试数 | {result.testsRun} |",
        f"| 通过 | {result.testsRun - len(result.failures) - len(result.errors)} |",
        f"| 失败 | {len(result.failures)} |",
        f"| 错误 | {len(result.errors)} |",
        f"| 通过率 | {(result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100:.1f}% |" if result.testsRun else "",
        "",
        "## 详细结果",
        ""
    ]

    for test, trace in result.failures + result.errors:
        lines.append(f"### ❌ {test}")
        lines.append("```")
        lines.append(trace)
        lines.append("```")
        lines.append("")

    lines.extend([
        "## 结论",
        "",
        f"{'✅ 全部通过，内容质量达标，可进入销售阶段。' if result.wasSuccessful() else '❌ 存在失败项，需修复后再交付。'}",
        "",
        "## 下一步赚钱动作",
        "",
        "1. 将 free_preview_v3.md 转成长图/海报，分发到小红书、即刻、朋友圈引流。",
        "2. 把 premium_catalog_v2.md 作为销售页核心素材，部署到 Vercel/Cloudflare Pages。",
        "3. 用 week1_samples 作为『7天体验营』邮件序列，收集种子用户邮箱。",
        "4. 本周内启动早鸟价 ¥69/月（限50人），用 scarcity 促单，目标首月收入 ¥3,450。",
        ""
    ])

    return "\n".join(lines)


def main():
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    suite.addTests(loader.loadTestsFromModule(sys.modules[__name__]))

    runner = unittest.TextTestRunner(verbosity=2, stream=sys.stdout)
    result = runner.run(suite)

    report = generate_report(result)
    report_path = PROJECT_DIR / "reports" / "sample_pack_test_report_7691939d.md"
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report)
    print(f"\n报告已保存: {report_path}")

    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(main())
