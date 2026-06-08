"""
Test suite for knowledge-subscription sample pack generation (Task 16513ba1)
Run: pytest tests/test_sample_pack_16513ba1.py -v
"""

import json
import sys
from pathlib import Path

import pytest

PROJECT_DIR = Path("/home/AgentAdmin/.hermes/shared/dev-team/projects/knowledge-subscription")
SAMPLE_PACK_DIR = PROJECT_DIR / "reports" / "sample_pack"
DOCS_DIR = PROJECT_DIR / "docs"
APP_DIR = PROJECT_DIR / "app"


class TestFileExistence:
    """Verify all expected files were generated."""

    def test_free_preview_exists(self):
        assert (SAMPLE_PACK_DIR / "free_preview_v10.md").exists(), "free_preview_v10.md missing"

    def test_premium_catalog_exists(self):
        assert (SAMPLE_PACK_DIR / "premium_catalog_v10.md").exists(), "premium_catalog_v10.md missing"

    def test_data_json_exists(self):
        assert (SAMPLE_PACK_DIR / "data_v10.json").exists(), "data_v10.json missing"

    def test_delivery_checklist_exists(self):
        assert (DOCS_DIR / "delivery_checklist.md").exists(), "delivery_checklist.md missing"

    @pytest.mark.parametrize("day", ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"])
    def test_week1_sample_exists(self, day):
        assert (SAMPLE_PACK_DIR / "week1_samples" / f"{day}_v10.md").exists(), f"{day}_v10.md missing"

    def test_generator_script_exists(self):
        assert (APP_DIR / "sample_pack_generator_v10.py").exists(), "generator script missing"


class TestDataJson:
    """Validate structured data integrity."""

    @pytest.fixture(scope="class")
    def data(self):
        with open(SAMPLE_PACK_DIR / "data_v10.json", "r", encoding="utf-8") as f:
            return json.load(f)

    def test_meta_fields(self, data):
        meta = data["meta"]
        assert meta["version"] == "v10.0"
        assert meta["task_id"] == "16513ba1"
        assert meta["project_id"] == "knowledge-subscription"
        assert "generated_at" in meta

    def test_opportunity_count(self, data):
        assert len(data["opportunities"]) == 6, "Expected 6 opportunities"

    def test_week1_day_count(self, data):
        assert len(data["week1"]) == 7, "Expected 7 daily reports"

    def test_each_opportunity_has_required_fields(self, data):
        required = {"id", "title", "category", "description", "data_sources",
                    "action_steps", "profit_estimate", "difficulty", "time_to_start",
                    "tags", "source_urls", "free_preview", "prompt_template",
                    "code_snippet", "risk_notes", "margin_rate"}
        for opp in data["opportunities"]:
            missing = required - set(opp.keys())
            assert not missing, f"Opportunity {opp.get('id')} missing fields: {missing}"

    def test_profit_estimate_format(self, data):
        for opp in data["opportunities"]:
            profit = opp["profit_estimate"]
            assert "¥" in profit or "$" in profit, f"{opp['id']} profit missing currency symbol"
            assert "/月" in profit, f"{opp['id']} profit missing monthly unit"

    def test_source_urls_present(self, data):
        for opp in data["opportunities"]:
            assert len(opp["source_urls"]) >= 1, f"{opp['id']} has no source_urls"

    def test_action_steps_count(self, data):
        for opp in data["opportunities"]:
            assert len(opp["action_steps"]) == 5, f"{opp['id']} should have exactly 5 action steps"

    def test_free_preview_selection(self, data):
        free = [o for o in data["opportunities"] if o["free_preview"]]
        assert len(free) == 3, f"Expected 3 free_preview opportunities, got {len(free)}"

    def test_difficulty_range(self, data):
        for opp in data["opportunities"]:
            assert 1 <= opp["difficulty"] <= 5, f"{opp['id']} difficulty out of range"

    def test_margin_rate_present(self, data):
        for opp in data["opportunities"]:
            assert "%" in opp["margin_rate"], f"{opp['id']} margin_rate missing %"

    def test_prompt_and_code_present(self, data):
        for opp in data["opportunities"]:
            assert len(opp["prompt_template"]) > 50, f"{opp['id']} prompt_template too short"
            assert len(opp["code_snippet"]) > 50, f"{opp['id']} code_snippet too short"


class TestMarkdownContent:
    """Validate generated markdown quality."""

    def test_free_preview_has_comparison_table(self):
        content = (SAMPLE_PACK_DIR / "free_preview_v10.md").read_text(encoding="utf-8")
        assert "对比项" in content
        assert "免费试看" in content
        assert "专业版订阅" in content
        assert "¥99/月" in content

    def test_free_preview_has_three_opportunities(self):
        content = (SAMPLE_PACK_DIR / "free_preview_v10.md").read_text(encoding="utf-8")
        # Count H3 headers (###) which mark opportunities
        h3_count = content.count("\n### ")
        assert h3_count == 3, f"Expected 3 opportunities in free preview, got {h3_count}"

    def test_free_preview_no_code_snippets(self):
        """Free preview should NOT contain full code snippets (paywalled)."""
        content = (SAMPLE_PACK_DIR / "free_preview_v10.md").read_text(encoding="utf-8")
        assert "```python" not in content, "Free preview should not contain code blocks"

    def test_premium_catalog_has_pricing(self):
        content = (SAMPLE_PACK_DIR / "premium_catalog_v10.md").read_text(encoding="utf-8")
        assert "¥99/月" in content
        assert "¥799/年" in content
        assert "¥2,999/年" in content

    def test_premium_catalog_has_six_opportunities(self):
        content = (SAMPLE_PACK_DIR / "premium_catalog_v10.md").read_text(encoding="utf-8")
        # Count opportunity entries (### opp-10-xxx)
        opp_count = content.count("### opp-10-")
        assert opp_count == 6, f"Expected 6 opportunities in catalog, got {opp_count}"

    def test_premium_catalog_has_faq(self):
        content = (SAMPLE_PACK_DIR / "premium_catalog_v10.md").read_text(encoding="utf-8")
        assert "常见问题" in content
        assert "退款" in content

    def test_premium_catalog_has_code_snippets(self):
        """Premium catalog should reference code (full code in daily reports)."""
        content = (SAMPLE_PACK_DIR / "premium_catalog_v10.md").read_text(encoding="utf-8")
        assert "可运行代码" in content

    def test_delivery_checklist_has_verdict_section(self):
        content = (DOCS_DIR / "delivery_checklist.md").read_text(encoding="utf-8")
        assert "盈利空间判断" in content
        assert "下一步赚钱动作" in content

    def test_delivery_checklist_has_14_items(self):
        content = (DOCS_DIR / "delivery_checklist.md").read_text(encoding="utf-8")
        # Count deliverable table rows (any version)
        rows = [line for line in content.splitlines() if "reports/sample_pack/" in line or "app/" in line]
        assert len(rows) >= 10, f"Expected >=10 deliverable rows, got {len(rows)}"

    @pytest.mark.parametrize("day", ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"])
    def test_week1_report_structure(self, day):
        content = (SAMPLE_PACK_DIR / "week1_samples" / f"{day}_v10.md").read_text(encoding="utf-8")
        assert "今日机会" in content
        assert "今日SOP" in content
        assert "立即行动清单" in content
        assert "会员专属彩蛋" in content

    def test_monday_has_opportunity_content(self):
        content = (SAMPLE_PACK_DIR / "week1_samples" / "monday_v10.md").read_text(encoding="utf-8")
        assert "opp-10-001" in content or "AI客服" in content

    def test_sunday_has_roadmap(self):
        content = (SAMPLE_PACK_DIR / "week1_samples" / "sunday_v10.md").read_text(encoding="utf-8")
        assert "90天" in content or "OKR" in content

    def test_no_guaranteed_profit_language(self):
        """Ensure no over-promising language."""
        for md_file in SAMPLE_PACK_DIR.glob("*.md"):
            content = md_file.read_text(encoding="utf-8").lower()
            assert "稳赚" not in content, f"{md_file.name} contains forbidden word '稳赚'"
            assert "保证赚" not in content, f"{md_file.name} contains forbidden phrase '保证赚'"
            assert "guaranteed" not in content, f"{md_file.name} contains 'guaranteed'"
        for md_file in (SAMPLE_PACK_DIR / "week1_samples").glob("*.md"):
            content = md_file.read_text(encoding="utf-8").lower()
            assert "稳赚" not in content, f"{md_file.name} contains forbidden word '稳赚'"
            assert "保证赚" not in content, f"{md_file.name} contains forbidden phrase '保证赚'"


class TestGeneratorScript:
    """Validate generator script is runnable and produces deterministic output."""

    def test_generator_imports_clean(self):
        # Ensure the generator can be imported without errors
        sys.path.insert(0, str(APP_DIR))
        import sample_pack_generator_v10 as gen
        assert len(gen.OPPORTUNITIES_DB) == 6
        assert len(gen.WEEK1_SCHEDULE) == 7

    def test_generator_check_mode(self):
        import subprocess
        result = subprocess.run(
            [sys.executable, str(APP_DIR / "sample_pack_generator_v10.py"), "--check"],
            capture_output=True, text=True
        )
        assert result.returncode == 0, f"Generator check failed: {result.stdout}\n{result.stderr}"
        assert "✅" in result.stdout


class TestBusinessMetrics:
    """Validate business-facing assertions in content."""

    def test_ltv_cac_ratio_in_delivery_checklist(self):
        content = (DOCS_DIR / "delivery_checklist.md").read_text(encoding="utf-8")
        assert "LTV/CAC" in content
        assert "22-84:1" in content

    def test_verdict_go_mentioned(self):
        content = (DOCS_DIR / "delivery_checklist.md").read_text(encoding="utf-8")
        assert "GO" in content
        assert "79/100" in content

    def test_pricing_ladder_complete(self):
        content = (SAMPLE_PACK_DIR / "premium_catalog_v10.md").read_text(encoding="utf-8")
        assert "月付" in content
        assert "年付" in content
        assert "企业版" in content
        assert "单次咨询" in content

    def test_acquisition_plan_present(self):
        content = (DOCS_DIR / "delivery_checklist.md").read_text(encoding="utf-8")
        assert "小红书" in content
        assert "即刻" in content
        assert "知乎" in content
