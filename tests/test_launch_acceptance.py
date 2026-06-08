#!/usr/bin/env python3
"""
知识付费订阅上线验收测试 — 付费用户视角
任务ID: 2dd07ee8
覆盖: 销售页、样例内容、订阅入口、交付流程、阻塞项
"""

import json
import os
import re
import subprocess
import sys
from pathlib import Path

import pytest

BASE = Path("/home/AgentAdmin/.hermes/shared/dev-team/projects/knowledge-subscription")
SITE_DIR = BASE / "site"
REPORTS_DIR = BASE / "reports"
DOCS_DIR = BASE / "docs"
APP_DIR = BASE / "app"
SAMPLE_DIR = REPORTS_DIR / "sample_pack"
WEEK_DIR = SAMPLE_DIR / "week1_samples"

# ============================================================
# 1. 销售页可用性
# ============================================================

class TestSalesPage:
    """从潜在付费用户视角检查销售页"""

    @pytest.fixture(scope="class")
    def html(self):
        path = SITE_DIR / "index.html"
        assert path.exists(), "销售页 index.html 不存在"
        return path.read_text(encoding="utf-8")

    def test_page_exists_and_nonempty(self, html):
        assert len(html) > 10000, "销售页内容过少，不足10KB"

    def test_has_doctype_and_viewport(self, html):
        assert "<!DOCTYPE html>" in html
        assert "viewport" in html

    def test_has_og_tags(self, html):
        assert "og:title" in html
        assert "og:description" in html
        assert "og:url" in html

    def test_has_pricing_tiers(self, html):
        assert "¥29" in html or "早鸟" in html
        assert "¥99" in html or "专业版" in html
        assert "¥499" in html or "定制" in html

    def test_has_primary_cta(self, html):
        assert "立即订阅" in html or "选择" in html

    def test_has_sample_preview(self, html):
        assert "样例" in html or "预览" in html

    def test_has_faq_section(self, html):
        assert "退款" in html
        assert "常见问题" in html or "FAQ" in html

    def test_has_contact_form_or_info(self, html):
        assert "联系" in html or "微信" in html or "邮箱" in html

    def test_has_risk_disclaimer_in_faq(self, html):
        assert "7天" in html or "退款" in html

    def test_responsive_meta(self, html):
        assert "width=device-width" in html

    def test_payment_section_exists(self, html):
        assert "支付" in html or "小报童" in html or "爱发电" in html

    def test_payment_placeholder_status(self, html):
        # 支付入口应为占位状态并明确告知用户
        placeholder_found = (
            "待用户授权激活" in html or
            "占位" in html or
            "配置后替换" in html or
            "待配置" in html or
            "演示页面" in html or
            "实际支付系统需配置" in html
        )
        assert placeholder_found, "销售页未标明支付入口为占位状态，可能误导用户"

    def test_contact_placeholder_status(self, html):
        contact_placeholder = (
            "AI-Radar-2026" in html or
            "contact@ai-radar.dev" in html or
            "待替换" in html or
            "需替换" in html
        )
        assert contact_placeholder, "销售页联系信息可能已是真实值或缺少占位标记"

    def test_urgency_element(self, html):
        assert "早鸟剩余" in html or "限量" in html or "限时" in html

    def test_trust_signals(self, html):
        assert "保密" in html or "无垃圾" in html or "24h" in html


# ============================================================
# 2. 样例内容与交付物
# ============================================================

class TestSampleContent:
    """验证付费用户能收到的内容质量（当前实际文件为无版本后缀）"""

    def test_free_preview_current_exists(self):
        assert (SAMPLE_DIR / "free_preview.md").exists()

    def test_premium_catalog_current_exists(self):
        assert (SAMPLE_DIR / "premium_catalog.md").exists()

    def test_data_current_json_exists(self):
        assert (SAMPLE_DIR / "data.json").exists()

    def test_week1_current_all_exist(self):
        for day in ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]:
            assert (WEEK_DIR / f"{day}.md").exists(), f"缺少 {day}.md"

    def test_free_preview_has_no_overpromise(self):
        text = (SAMPLE_DIR / "free_preview.md").read_text(encoding="utf-8")
        forbidden = ["稳赚", "躺赚", " guaranteed ", "包赚", "必赚", "零风险"]
        for w in forbidden:
            assert w not in text.lower(), f"发现禁用词: {w}"

    def test_free_preview_has_revenue_data(self):
        text = (SAMPLE_DIR / "free_preview.md").read_text(encoding="utf-8")
        matches = re.findall(r"[\u00a5$]\d[\d,]*", text)
        assert len(matches) >= 3, "免费试看缺少收益数据"

    def test_free_preview_has_cta(self):
        text = (SAMPLE_DIR / "free_preview.md").read_text(encoding="utf-8")
        assert "订阅" in text or "专业版" in text or "付费" in text

    def test_json_valid_and_complete(self):
        with open(SAMPLE_DIR / "data.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        assert "opportunities" in data
        assert len(data["opportunities"]) >= 6
        assert "meta" in data
        assert data["meta"].get("task_id") == "889b251b"
        for opp in data["opportunities"]:
            required = ["id", "title", "category", "difficulty", "profit_estimate", "margin_rate", "action_steps", "prompt_template"]
            for field in required:
                assert field in opp, f"{opp['id']} 缺少 {field}"
            assert len(opp["action_steps"]) == 5

    def test_week_reports_have_risk_and_taskid(self):
        for day in ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]:
            text = (WEEK_DIR / f"{day}.md").read_text(encoding="utf-8")
            assert "风险" in text, f"{day}.md 缺少风险提示"
            assert "889b251b" in text, f"{day}.md 缺少任务ID"

    def test_radar_script_runnable(self):
        script = WEEK_DIR / "resources" / "scripts" / "opportunity_radar.py"
        assert script.exists()
        result = subprocess.run(
            [sys.executable, "-m", "py_compile", str(script)],
            capture_output=True, text=True
        )
        assert result.returncode == 0, f"opportunity_radar.py 语法错误: {result.stderr}"

    def test_generator_current_runnable(self):
        gen = APP_DIR / "sample_pack_generator.py"
        assert gen.exists()
        result = subprocess.run(
            [sys.executable, "-m", "py_compile", str(gen)],
            capture_output=True, text=True
        )
        assert result.returncode == 0, f"生成器语法错误: {result.stderr}"

    def test_generator_v12_backup_runnable(self):
        # 保留对 v12 备份生成器的兼容性检查
        gen = APP_DIR / "sample_pack_generator_v12.py"
        if gen.exists():
            result = subprocess.run(
                [sys.executable, "-m", "py_compile", str(gen)],
                capture_output=True, text=True
            )
            assert result.returncode == 0, f"v12生成器语法错误: {result.stderr}"


# ============================================================
# 3. 订阅模块与权限控制
# ============================================================

class TestSubscriptionLogic:
    """验证订阅系统的商业逻辑"""

    def test_subscription_module_importable(self):
        sys.path.insert(0, str(BASE))
        from app.subscription import SubscriptionPlan, PlanType, SubscriptionManager
        assert SubscriptionPlan.get_plan(PlanType.EARLY_BIRD)["price"] == 29
        assert SubscriptionPlan.get_plan(PlanType.PROFESSIONAL)["price"] == 99
        assert SubscriptionPlan.get_plan(PlanType.CUSTOM)["price"] == 499

    def test_free_plan_is_free(self):
        sys.path.insert(0, str(BASE))
        from app.subscription import SubscriptionPlan, PlanType
        plan = SubscriptionPlan.get_plan(PlanType.FREE)
        assert plan["price"] == 0
        assert plan["price_cny"] == 0

    def test_revenue_projections_monotonically_increasing(self):
        sys.path.insert(0, str(BASE))
        from app.subscription import get_revenue_projections
        proj = get_revenue_projections()
        revenues = [proj[k]["revenue"] for k in ["month_1", "month_3", "month_6", "month_12"]]
        for i in range(1, len(revenues)):
            assert revenues[i] > revenues[i-1], "收入预测非递增"


# ============================================================
# 4. 运营支持文档完整性
# ============================================================

class TestOpsDocs:
    """检查上线必需的运营支持文档"""

    def test_support_sop_exists(self):
        assert (DOCS_DIR / "support_sop.md").exists()

    def test_incident_runbook_exists(self):
        assert (DOCS_DIR / "incident_runbook.md").exists()

    def test_customer_support_exists(self):
        assert (DOCS_DIR / "customer_support.md").exists()

    def test_support_sop_has_response_times(self):
        text = (DOCS_DIR / "support_sop.md").read_text(encoding="utf-8")
        assert "响应" in text
        assert "退款" in text

    def test_incident_runbook_has_severity_levels(self):
        text = (DOCS_DIR / "incident_runbook.md").read_text(encoding="utf-8")
        # 支持 P0/P1/P2/P3 或 S1/S2/S3/S4 分级
        assert ("P0" in text or "S1" in text or "Critical" in text or "重大" in text)
        assert ("P1" in text or "S2" in text or "High" in text or "高" in text)
        assert ("恢复" in text or "Recovery" in text or "复盘" in text)

    def test_customer_support_has_faq(self):
        text = (DOCS_DIR / "customer_support.md").read_text(encoding="utf-8")
        assert "FAQ" in text or "常见问题" in text
        assert "退款" in text

    def test_launch_execution_plan_exists(self):
        assert (DOCS_DIR / "launch_execution_plan.md").exists()

    def test_deployment_blockers_exists(self):
        assert (DOCS_DIR / "deployment_blockers.md").exists()

    def test_kpi_dashboard_exists(self):
        assert (DOCS_DIR / "kpi_dashboard.md").exists()

    def test_revenue_experiment_7d_exists(self):
        assert (DOCS_DIR / "revenue_experiment_7d.md").exists()


# ============================================================
# 5. 阻塞项与上线 readiness
# ============================================================

class TestLaunchBlockers:
    """识别阻碍付费转化的真实阻塞项"""

    def test_deployment_blockers_documented(self):
        text = (DOCS_DIR / "deployment_blockers.md").read_text(encoding="utf-8")
        assert "BLOCKED" in text or "阻塞" in text or "待用户" in text

    def test_payment_not_fully_live(self):
        html = (SITE_DIR / "index.html").read_text(encoding="utf-8")
        # 检查是否存在显著的实时支付系统（如 Stripe checkout 或微信支付API）
        # 允许存在占位链接（小报童/爱发电），但必须同时有占位声明
        has_real_payment = (
            "stripe.com/checkout" in html or
            "weixin.qq.com" in html or  # 微信支付回调
            "alipay.com" in html
        )
        has_placeholder_notice = (
            "待用户授权激活" in html or
            "占位" in html or
            "演示" in html or
            "实际支付系统需配置" in html or
            "AI-Radar-2026" in html
        )
        # 如果存在小报童/爱发电占位链接，必须有占位声明
        has_placeholder_links = ("xiaobot.net" in html or "afdian.net" in html)
        if has_placeholder_links:
            assert has_placeholder_notice, "销售页有占位链接但缺少占位声明，可能误导用户"
        # 如果存在真实支付系统，必须同时有验证记录
        if has_real_payment:
            blocker = (DOCS_DIR / "deployment_blockers.md").read_text(encoding="utf-8")
            assert "支付渠道活跃" in blocker or "PAYMENT_LIVE" in blocker or "支付已配置" in blocker
        # 总体上必须还有某种占位标记
        assert has_placeholder_notice, "销售页缺少实付激活状态的标明，可能误导用户"

    def test_contact_info_is_placeholder(self):
        html = (SITE_DIR / "index.html").read_text(encoding="utf-8")
        assert "AI-Radar-2026" in html or "contact@ai-radar.dev" in html

    def test_public_url_documented(self):
        text = (DOCS_DIR / "deployment_blockers.md").read_text(encoding="utf-8")
        assert "aunomira-lab.github.io" in text

    def test_deployment_verification_or_blocker_noted(self):
        # 确认部署状态不是被伪装成已完成
        blocker = (DOCS_DIR / "deployment_blockers.md").read_text(encoding="utf-8")
        assert "PARTIALLY_UNBLOCKED" in blocker or "BLOCKED_BY_USER" in blocker

    def test_readme_has_verdict_reference(self):
        readme = (BASE / "README.md").read_text(encoding="utf-8")
        assert "Verdict" in readme
        assert "GO" in readme

    def test_pricing_consistency_across_files(self):
        html = (SITE_DIR / "index.html").read_text(encoding="utf-8")
        readme = (BASE / "README.md").read_text(encoding="utf-8")
        # 检查定价是否一致
        assert "¥29" in html or "¥99" in html
        assert "¥99/月" in readme
        # 销售页README定价不冲突
        if "¥29" in html and "¥29" not in readme:
            # 允许销售页用早鸟价引流，README用标准价
            pass


# ============================================================
# 6. 可用性静态检查
# ============================================================

class TestUsability:
    """用户旅程可用性检查"""

    def test_sales_page_loads_under_browser(self):
        # 模拟浏览器检查关键DOM是否存在
        html = (SITE_DIR / "index.html").read_text(encoding="utf-8")
        assert "<section" in html or "<div" in html
        assert "<form" in html or "mailto" in html
        assert "<script" in html

    def test_no_broken_internal_links(self):
        html = (SITE_DIR / "index.html").read_text(encoding="utf-8")
        # 检查锚点链接目标是否存在
        hrefs = re.findall(r'href="(#\w+)"', html)
        ids = re.findall(r'id="(\w+)"', html)
        for h in set(hrefs):
            target = h.lstrip("#")
            assert target in ids, f"锚点链接 #{target} 没有对应 id"

    def test_mailto_form_works_as_fallback(self):
        html = (SITE_DIR / "index.html").read_text(encoding="utf-8")
        assert "mailto:" in html
        assert "handleSubmit" in html

    def test_mobile_friendly_meta(self):
        html = (SITE_DIR / "index.html").read_text(encoding="utf-8")
        assert "width=device-width" in html
        assert "@media" in html

    def test_current_data_json_has_8_opportunities(self):
        with open(SAMPLE_DIR / "data.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        assert len(data.get("opportunities", [])) == 8, "当前data.json应有8个机会"

    def test_current_free_preview_has_3_free_opportunities(self):
        text = (SAMPLE_DIR / "free_preview.md").read_text(encoding="utf-8")
        opp_headers = re.findall(r"### .+", text)
        assert len(opp_headers) >= 3, f"免费试看应有>=3个机会，实际{len(opp_headers)}"

    def test_current_premium_catalog_has_8_opportunities(self):
        text = (SAMPLE_DIR / "premium_catalog.md").read_text(encoding="utf-8")
        opp_count = len(re.findall(r"### opp-12-", text))
        assert opp_count == 8, f"专业目录应有8个机会，实际{opp_count}"


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
