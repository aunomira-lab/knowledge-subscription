#!/usr/bin/env python3
"""pytest 验证样例包完整性"""
import json
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PACK = os.path.join(ROOT, "reports", "sample_pack")


def test_free_preview_exists():
    path = os.path.join(PACK, "free_preview.md")
    assert os.path.exists(path)
    assert os.path.getsize(path) > 1000


def test_premium_catalog_exists():
    path = os.path.join(PACK, "premium_catalog.md")
    assert os.path.exists(path)
    assert os.path.getsize(path) > 5000


def test_week1_samples_exist():
    for day in ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]:
        path = os.path.join(PACK, "week1_samples", f"{day}.md")
        assert os.path.exists(path), f"missing {day}.md"
        assert os.path.getsize(path) > 1000


def test_data_json_exists():
    path = os.path.join(PACK, "data.json")
    assert os.path.exists(path)
    with open(path, "r", encoding="utf-8") as f:
        d = json.load(f)
    assert len(d["opportunities"]) == 8
    assert len(d["week1"]) == 7


def test_delivery_checklist_exists():
    path = os.path.join(ROOT, "docs", "delivery_checklist.md")
    assert os.path.exists(path)
    assert os.path.getsize(path) > 1000


def test_no_empty_files():
    for name in ["free_preview.md", "premium_catalog.md", "data.json"]:
        path = os.path.join(PACK, name)
        assert os.path.getsize(path) > 500


def test_free_preview_has_cta():
    path = os.path.join(PACK, "free_preview.md")
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()
    assert "专业版" in text
    assert "¥99" in text or "¥799" in text


def test_generator_script_runnable():
    result = subprocess.run(
        [sys.executable, "app/sample_pack_generator.py", "--check"],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr
    assert ("OK" in result.stdout or "✅" in result.stdout)


def test_premium_catalog_has_all_opportunities():
    path = os.path.join(PACK, "premium_catalog.md")
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()
    assert "Claude 4 智能客服" in text
    assert "跨境电商评论分析" in text
    assert "小红书AI养生" in text
    assert "面试陪跑" in text


def test_sunday_has_all_opportunities():
    path = os.path.join(PACK, "week1_samples", "sunday.md")
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()
    assert "Claude 4 智能客服" in text
    assert "跨境电商评论分析" in text
    assert "小红书AI养生" in text
    assert "面试陪跑" in text


if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v"])
