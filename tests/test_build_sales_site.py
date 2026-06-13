#!/usr/bin/env python3
"""
Test build_sales_site.py
Task: 889b251b
"""

import json
import os
import sys
from pathlib import Path

PROJECT_DIR = Path("/home/AgentAdmin/.hermes/shared/dev-team/projects/knowledge-subscription")
OUTPUT_DIR = PROJECT_DIR / "site" / "sample_pack"

def test_index_html():
    p = OUTPUT_DIR / "index.html"
    assert p.exists(), "index.html missing"
    text = p.read_text(encoding="utf-8")
    assert "<!DOCTYPE html>" in text
    assert "AI赚钱机会雷达" in text
    assert "¥99/月" in text
    assert "免费试看版" in text
    assert "立即订阅" in text
    assert "</html>" in text
    assert "<style>" in text
    print("✅ index.html passed")

def test_free_preview_html():
    p = OUTPUT_DIR / "free_preview.html"
    assert p.exists(), "free_preview.html missing"
    text = p.read_text(encoding="utf-8")
    assert "免费试看版" in text
    assert "index.html" in text  # 返回链接
    assert "</html>" in text
    assert "<table>" in text
    print("✅ free_preview.html passed")

def test_premium_catalog_html():
    p = OUTPUT_DIR / "premium_catalog.html"
    assert p.exists(), "premium_catalog.html missing"
    text = p.read_text(encoding="utf-8")
    assert "专业版目录" in text
    assert "¥799/年" in text
    assert "</html>" in text
    assert "<table>" in text
    print("✅ premium_catalog.html passed")

def test_html_sizes():
    for f in ["index.html","free_preview.html","premium_catalog.html"]:
        p = OUTPUT_DIR / f
        size = p.stat().st_size
        assert size > 3000, f"{f} too small ({size} bytes)"
    print("✅ HTML sizes passed")

def test_generator_runnable():
    script = PROJECT_DIR / "app" / "build_sales_site.py"
    assert script.exists(), "build_sales_site.py missing"
    result = os.system(f"cd {PROJECT_DIR} && python {script} > /dev/null 2>&1")
    assert result == 0, "build_sales_site.py exit code non-zero"
    print("✅ build_sales_site.py runnable passed")

def test_all():
    test_index_html()
    test_free_preview_html()
    test_premium_catalog_html()
    test_html_sizes()
    test_generator_runnable()
    print("\n🎉 All HTML build tests passed for task 889b251b")

if __name__ == "__main__":
    test_all()
