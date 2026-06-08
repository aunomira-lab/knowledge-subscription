#!/usr/bin/env python3
"""
Test suite for knowledge-subscription sample pack (no-version)
Task: 889b251b
"""

import json
import os
import re
from pathlib import Path

PROJECT_DIR = Path("/home/AgentAdmin/.hermes/shared/dev-team/projects/knowledge-subscription")
SAMPLE_DIR = PROJECT_DIR / "reports" / "sample_pack"
WEEK1_DIR = SAMPLE_DIR / "week1_samples"


def test_free_preview_exists():
    fp = SAMPLE_DIR / "free_preview.md"
    assert fp.exists(), "free_preview.md missing"
    text = fp.read_text(encoding="utf-8")
    assert "免费试看" in text
    assert "¥99/月" in text
    assert "889b251b" in text
    assert "立即行动" in text
    print("✅ free_preview.md passed")


def test_premium_catalog_exists():
    pc = SAMPLE_DIR / "premium_catalog.md"
    assert pc.exists(), "premium_catalog.md missing"
    text = pc.read_text(encoding="utf-8")
    assert "专业版订阅目录" in text
    assert "定价方案" in text
    assert "¥99/月" in text
    assert "889b251b" in text
    print("✅ premium_catalog.md passed")


def test_week1_samples_exist():
    days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
    for day in days:
        f = WEEK1_DIR / f"{day}.md"
        assert f.exists(), f"{day}.md missing"
        text = f.read_text(encoding="utf-8")
        assert "日报" in text or "专题" in text or "测评" in text
        assert len(text) > 1000, f"{day}.md too short ({len(text)} bytes)"
    print("✅ week1_samples passed")


def test_data_json_exists():
    dj = SAMPLE_DIR / "data.json"
    assert dj.exists(), "data.json missing"
    data = json.loads(dj.read_text(encoding="utf-8"))
    assert "opportunities" in data
    assert len(data["opportunities"]) >= 6
    assert data["meta"]["task_id"] == "889b251b"
    assert data["meta"]["version"] == "final"
    print("✅ data.json passed")


def test_delivery_checklist_exists():
    dc = PROJECT_DIR / "docs" / "delivery_checklist.md"
    assert dc.exists(), "delivery_checklist.md missing"
    text = dc.read_text(encoding="utf-8")
    assert "889b251b" in text
    assert "免费试看版报告" in text
    assert "专业版订阅目录" in text
    assert "交付清单" in text
    print("✅ delivery_checklist.md passed")


def test_code_generator_exists():
    gen = PROJECT_DIR / "app" / "sample_pack_generator.py"
    assert gen.exists(), "sample_pack_generator.py missing"
    text = gen.read_text(encoding="utf-8")
    assert "889b251b" in text
    assert "def generate_all" in text
    print("✅ sample_pack_generator.py passed")


def test_revenue_mentions():
    fp = SAMPLE_DIR / "free_preview.md"
    text = fp.read_text(encoding="utf-8")
    matches = re.findall(r"[\u00a5$][\d,]+[\-~][\d,]+[/月年]*", text)
    assert len(matches) >= 3, f"Expected >=3 revenue mentions, got {len(matches)}"
    print(f"✅ revenue mentions: {len(matches)} found")


def test_opportunity_items_count():
    pc = SAMPLE_DIR / "premium_catalog.md"
    text = pc.read_text(encoding="utf-8")
    opp_count = len(re.findall(r"### opp-", text))
    assert opp_count >= 6, f"Expected >=6 opportunities, got {opp_count}"
    print(f"✅ opportunities in catalog: {opp_count}")


def test_week1_contains_sop():
    mon = WEEK1_DIR / "monday.md"
    text = mon.read_text(encoding="utf-8")
    assert "SOP" in text or "标准操作流程" in text
    assert "行动清单" in text
    assert "会员专属" in text
    print("✅ monday.md contains SOP + checklist + member bonus")


def test_json_data_integrity():
    dj = SAMPLE_DIR / "data.json"
    data = json.loads(dj.read_text(encoding="utf-8"))
    opps = data.get("opportunities", [])
    week1 = data.get("week1", [])
    # Every opportunity has required fields
    for o in opps:
        assert o.get("title")
        assert o.get("description")
        assert o.get("profit_estimate")
        assert o.get("difficulty") is not None
    # Week1 has 7 days
    assert len(week1) == 7, f"Expected 7 days, got {len(week1)}"
    print("✅ JSON data integrity passed")


def test_all():
    test_free_preview_exists()
    test_premium_catalog_exists()
    test_week1_samples_exist()
    test_data_json_exists()
    test_delivery_checklist_exists()
    test_code_generator_exists()
    test_revenue_mentions()
    test_opportunity_items_count()
    test_week1_contains_sop()
    test_json_data_integrity()
    print("\n🎉 All tests passed for task 889b251b")


if __name__ == "__main__":
    test_all()
