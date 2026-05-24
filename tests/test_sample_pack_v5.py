#!/usr/bin/env python3
"""
测试脚本：验证 knowledge-subscription 内容样例包质量
任务ID: 994f3629
运行: pytest tests/test_sample_pack_v5.py -v
"""

import json
import os
import re
from pathlib import Path

import pytest

BASE_DIR = Path("/home/AgentAdmin/.hermes/shared/dev-team/projects/knowledge-subscription")
SAMPLE_DIR = BASE_DIR / "reports" / "sample_pack"
WEEK_DIR = SAMPLE_DIR / "week1_samples"
DOCS_DIR = BASE_DIR / "docs"
TASK_ID = "994f3629"


class TestFileExistence:
    """验证所有必要文件存在"""

    def test_free_preview_exists(self):
        assert (SAMPLE_DIR / "free_preview_v5.md").exists()

    def test_premium_catalog_exists(self):
        assert (SAMPLE_DIR / "premium_catalog_v4.md").exists()

    def test_week1_samples_exist(self):
        days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
        for day in days:
            assert (WEEK_DIR / f"{day}_v5.md").exists()

    def test_data_json_exists(self):
        assert (SAMPLE_DIR / "data_v5.json").exists()

    def test_delivery_checklist_exists(self):
        assert (DOCS_DIR / "delivery_checklist.md").exists()

    def test_generator_exists(self):
        assert (BASE_DIR / "app" / "sample_pack_generator_v5.py").exists()


class TestContentQuality:
    """验证内容质量硬性指标"""

    @pytest.fixture(scope="class")
    def free_preview(self):
        return (SAMPLE_DIR / "free_preview_v5.md").read_text(encoding="utf-8")

    @pytest.fixture(scope="class")
    def premium_catalog(self):
        return (SAMPLE_DIR / "premium_catalog_v4.md").read_text(encoding="utf-8")

    @pytest.fixture(scope="class")
    def data_json(self):
        with open(SAMPLE_DIR / "data_v5.json", "r", encoding="utf-8") as f:
            return json.load(f)

    def test_free_preview_has_task_id(self, free_preview):
        assert TASK_ID in free_preview

    def test_free_preview_no_guaranteed_promise(self, free_preview):
        forbidden = ["稳赚", "躺赚", " guaranteed ", "包赚", "必赚"]
        lower = free_preview.lower()
        for word in forbidden:
            assert word not in lower, f"发现禁用词: {word}"

    def test_free_preview_has_conversion_entry(self, free_preview):
        assert "订阅" in free_preview
        assert "专业版" in free_preview

    def test_free_preview_has_revenue_data(self, free_preview):
        # 至少出现 3 次收益/月收入/月估算
        matches = re.findall(r"[¥$]\d[\d,]*-\d[\d,]*", free_preview)
        assert len(matches) >= 3

    def test_premium_catalog_has_pricing(self, premium_catalog):
        assert "¥99/月" in premium_catalog
        assert "¥799/年" in premium_catalog

    def test_premium_catalog_has_faq(self, premium_catalog):
        assert "Q:" in premium_catalog
        assert "退款" in premium_catalog

    def test_premium_catalog_has_columns(self, premium_catalog):
        assert "专栏" in premium_catalog
        assert "AI Agent 掘金" in premium_catalog

    def test_data_json_valid_structure(self, data_json):
        assert "meta" in data_json
        assert data_json["meta"]["task_id"] == TASK_ID
        assert "opportunities" in data_json
        assert len(data_json["opportunities"]) == 6
        assert "schedule" in data_json
        assert len(data_json["schedule"]) == 7
        assert "pricing" in data_json
        assert "target_metrics" in data_json

    def test_all_opportunities_have_required_fields(self, data_json):
        required = ["id", "title", "category", "difficulty", "launch_days",
                    "revenue", "margin", "summary", "tags", "source_urls",
                    "data_sources", "action_steps", "prompt_template"]
        for opp in data_json["opportunities"]:
            for field in required:
                assert field in opp, f"{opp['id']} 缺少 {field}"
            assert opp["difficulty"] >= 1 and opp["difficulty"] <= 5
            assert len(opp["action_steps"]) == 5
            assert len(opp["data_sources"]) >= 3

    def test_week_reports_have_risk_disclaimer(self):
        for day in ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]:
            text = (WEEK_DIR / f"{day}_v5.md").read_text(encoding="utf-8")
            assert "风险" in text
            assert "不保证" in text or "不承诺" in text
            assert TASK_ID in text

    def test_week_reports_have_checklist(self):
        for day in ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]:
            text = (WEEK_DIR / f"{day}_v5.md").read_text(encoding="utf-8")
            assert "[ ]" in text or "检查清单" in text or "行动" in text

    def test_delivery_checklist_has_verification_commands(self):
        text = (DOCS_DIR / "delivery_checklist.md").read_text(encoding="utf-8")
        assert "验证命令" in text
        assert "pytest" in text or "python" in text

    def test_delivery_checklist_has_profit_analysis(self):
        text = (DOCS_DIR / "delivery_checklist.md").read_text(encoding="utf-8")
        assert "盈利空间" in text
        assert "下一步赚钱动作" in text

    def test_free_preview_opportunities_match_json(self, free_preview, data_json):
        free_opps = [o["title"] for o in data_json["opportunities"] if o.get("free_preview")]
        for title in free_opps:
            assert title in free_preview

    def test_content_minimum_length(self, free_preview, premium_catalog):
        assert len(free_preview) > 1500
        assert len(premium_catalog) > 3000


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
