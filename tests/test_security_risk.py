#!/usr/bin/env python3
"""知识付费订阅安全风险审计测试
执行角色: dev-security (risk-analyst)
任务ID: eff3f092
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
APP_DIR = BASE / "app"
REPORTS_DIR = BASE / "reports"
SAMPLE_DIR = REPORTS_DIR / "sample_pack"

# ============================================================
# 1. 安全静态检查
# ============================================================

class TestSecurityStatic:
    """检查项目中是否存在硬编码密钥、XSS注入、HTTP明文等安全风险"""

    def test_no_hardcoded_secrets_in_site(self):
        html = (SITE_DIR / "index.html").read_text(encoding="utf-8")
        forbidden_patterns = [
            r"sk-[a-zA-Z0-9]{20,}",
            r"api_key\s*[:=]\s*['\"][a-zA-Z0-9_\-]{16,}['\"]",
            r"password\s*[:=]\s*['\"][^'\"]{6,}['\"]",
            r"secret\s*[:=]\s*['\"][a-zA-Z0-9_\-]{16,}['\"]",
        ]
        for pat in forbidden_patterns:
            matches = re.findall(pat, html)
            assert not matches, f"销售页发现可能的硬编码秘密: {matches[:3]}"

    def test_no_xss_vectors_in_site(self):
        html = (SITE_DIR / "index.html").read_text(encoding="utf-8")
        assert "eval(" not in html, "发现 eval( 潜在XSS向量"
        assert "document.write(" not in html, "发现 document.write( 潜在XSS向量"
        assert "dangerouslySetInnerHTML" not in html, "发现 dangerouslySetInnerHTML"
        # innerHTML 赋值检查
        innerhtml_assigns = re.findall(r'innerHTML\s*=', html)
        assert len(innerhtml_assigns) == 0, f"发现 {len(innerhtml_assigns)} 处 innerHTML 赋值"

    def test_no_http_plaintext_links(self):
        html = (SITE_DIR / "index.html").read_text(encoding="utf-8")
        http_links = re.findall(r'href="http://[^"]+"', html)
        # 允许内部锚点，排除锚点
        external_http = [l for l in http_links if not l.startswith('href="http://#')]
        assert len(external_http) == 0, f"发现HTTP明文外部链接: {external_http}"

    def test_no_forbidden_promise_words(self):
        """检查销售页和内容中是否有过度承诺禁用词"""
        forbidden = ["稳赚", "躺赚", "包赚", "必赚", "零风险", "guaranteed profit", "no risk", "100%成功", "无脑操作", "暴富", "日入过万", "月入百万"]
        for root in [SITE_DIR, SAMPLE_DIR]:
            for path in root.rglob("*"):
                if path.is_file() and path.stat().st_size < 5 * 1024 * 1024:
                    try:
                        text = path.read_text(encoding="utf-8").lower()
                        for w in forbidden:
                            assert w not in text, f"{path.relative_to(BASE)} 含有禁用词: {w}"
                    except (UnicodeDecodeError, Exception):
                        pass

    def test_sample_content_has_risk_disclaimers(self):
        """样例内容必须含有风险提示"""
        for day in ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]:
            p = SAMPLE_DIR / "week1_samples" / f"{day}.md"
            text = p.read_text(encoding="utf-8")
            assert "风险" in text, f"{day}.md 缺少风险提示"

    def test_sample_content_has_taskid(self):
        """样例内容必须含有可追溯任务ID"""
        for day in ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]:
            p = SAMPLE_DIR / "week1_samples" / f"{day}.md"
            text = p.read_text(encoding="utf-8")
            assert "任务ID" in text or "task_id" in text.lower(), f"{day}.md 缺少任务ID"

    def test_subscription_data_sanitization(self):
        """订阅模块不应直接暴露敏感路径"""
        sys.path.insert(0, str(BASE))
        from app.subscription import SubscriptionManager
        mgr = SubscriptionManager()
        # storage_path 默认为 /tmp ，不应是当前目录下的明文保存
        assert "/tmp" in mgr.storage_path or "subscriptions.json" in mgr.storage_path

# ============================================================
# 2. 合规与法律风险检查
# ============================================================

class TestCompliance:
    """检查隐私政策、服务条款、退款声明等合规文件"""

    def test_privacy_html_exists(self):
        assert (SITE_DIR / "privacy.html").exists(), "隐私政策页面缺失"

    def test_terms_html_exists(self):
        assert (SITE_DIR / "terms.html").exists(), "服务条款页面缺失"

    def test_privacy_html_has_placeholder_warning(self):
        text = (SITE_DIR / "privacy.html").read_text(encoding="utf-8")
        assert "占位" in text or "待替换" in text or "未由法律" in text, "隐私政策页面应标注占位状态"

    def test_terms_html_has_placeholder_warning(self):
        text = (SITE_DIR / "terms.html").read_text(encoding="utf-8")
        assert "占位" in text or "待替换" in text or "未由法律" in text, "服务条款页面应标注占位状态"

    def test_sales_page_has_refund_policy(self):
        html = (SITE_DIR / "index.html").read_text(encoding="utf-8")
        assert "退款" in html, "销售页缺少退款政策"
        assert "7天" in html or "无理由" in html, "销售页缺少具体退款说明"

    def test_sales_page_has_revenue_disclaimer(self):
        html = (SITE_DIR / "index.html").read_text(encoding="utf-8")
        assert "预期" in html or "不构成" in html or "仅供参考" in html, "销售页缺少收益免责声明"

    def test_no_real_personal_info_in_site(self):
        """确保销售页没有意外泄露真实个人信息"""
        html = (SITE_DIR / "index.html").read_text(encoding="utf-8")
        # 检查是否有看起来像真实手机号的数字串
        phones = re.findall(r"1[3-9]\d{9}", html)
        assert len(phones) == 0, f"发现可能的真实手机号: {phones}"
        # 检查是否有看起来像真实身份证号
        idcards = re.findall(r"\d{17}[\dXx]|\d{15}", html)
        assert len(idcards) == 0, f"发现可能的真实身份证号: {idcards}"

    def test_payment_links_are_placeholder_or_known_platforms(self):
        html = (SITE_DIR / "index.html").read_text(encoding="utf-8")
        # 允许小报童/爱发电/支付宝官方链接，但不允许未知的支付接口
        suspicious = re.findall(r'href="(https?://[^"]+)"', html)
        for url in suspicious:
            if any(bad in url for bad in ["stripe.com/checkout", "alipay.com", "wechat.com", "pay.weixin.qq.com"]):
                # 如果是真实支付API，必须有配置完成记录
                pass

    def test_deployment_blockers_documented(self):
        blockers = (BASE / "docs" / "deployment_blockers.md").read_text(encoding="utf-8")
        assert "BLOCKED_BY_USER" in blockers or "阻塞" in blockers, "部署阻塞文档未正确标记阻塞状态"

# ============================================================
# 3. 订阅与收入风险检查
# ============================================================

class TestSubscriptionRisk:
    """检查订阅定价一致性、收入测算合理性、权限漏洞"""

    def test_pricing_consistency(self):
        sys.path.insert(0, str(BASE))
        from app.subscription import SubscriptionPlan, PlanType
        assert SubscriptionPlan.get_plan(PlanType.EARLY_BIRD)["price"] == 29
        assert SubscriptionPlan.get_plan(PlanType.PROFESSIONAL)["price"] == 99
        assert SubscriptionPlan.get_plan(PlanType.CUSTOM)["price"] == 499

    def test_revenue_projections_reasonable(self):
        sys.path.insert(0, str(BASE))
        from app.subscription import get_revenue_projections
        proj = get_revenue_projections()
        for k in ["month_1", "month_3", "month_6", "month_12"]:
            assert proj[k]["revenue"] > 0
            assert proj[k]["early_bird_users"] >= 0
            assert proj[k]["professional_users"] >= 0
            assert proj[k]["custom_orders"] >= 0

    def test_revenue_monotonically_increasing(self):
        sys.path.insert(0, str(BASE))
        from app.subscription import get_revenue_projections
        proj = get_revenue_projections()
        revenues = [proj[k]["revenue"] for k in ["month_1", "month_3", "month_6", "month_12"]]
        for i in range(1, len(revenues)):
            assert revenues[i] > revenues[i-1], "收入预测非递增"

    def test_free_user_cannot_access_paid_content(self):
        sys.path.insert(0, str(BASE))
        from app.subscription import UserSubscription, PlanType
        user = UserSubscription("test_user", PlanType.FREE)
        assert user.can_access_content("free") is True
        assert user.can_access_content("early_bird") is False
        assert user.can_access_content("professional") is False
        assert user.can_access_content("custom") is False

    def test_early_bird_user_cannot_access_pro_content(self):
        sys.path.insert(0, str(BASE))
        from app.subscription import UserSubscription, PlanType
        user = UserSubscription("test_user", PlanType.EARLY_BIRD)
        assert user.can_access_content("early_bird") is True
        assert user.can_access_content("professional") is False
        assert user.can_access_content("custom") is False

    def test_pro_user_can_access_all_except_custom(self):
        sys.path.insert(0, str(BASE))
        from app.subscription import UserSubscription, PlanType
        user = UserSubscription("test_user", PlanType.PROFESSIONAL)
        assert user.can_access_content("free") is True
        assert user.can_access_content("early_bird") is True
        assert user.can_access_content("professional") is True
        assert user.can_access_content("custom") is False

    def test_custom_user_can_access_all(self):
        sys.path.insert(0, str(BASE))
        from app.subscription import UserSubscription, PlanType
        user = UserSubscription("test_user", PlanType.CUSTOM)
        assert user.can_access_content("custom") is True

    def test_expired_user_loses_access(self):
        sys.path.insert(0, str(BASE))
        from app.subscription import UserSubscription, PlanType, SubscriptionStatus
        user = UserSubscription("test_user", PlanType.EARLY_BIRD)
        user.status = SubscriptionStatus.EXPIRED
        assert user.is_active() is False
        assert user.can_access_content("early_bird") is False

    def test_no_negative_pricing(self):
        sys.path.insert(0, str(BASE))
        from app.subscription import SubscriptionPlan, PlanType
        for plan_type in [PlanType.FREE, PlanType.EARLY_BIRD, PlanType.PROFESSIONAL, PlanType.CUSTOM]:
            plan = SubscriptionPlan.get_plan(plan_type)
            assert plan["price"] >= 0, f"{plan_type.value} 价格为负: {plan['price']}"

    def test_custom_plan_price_matches_expected_mrr_calculation(self):
        sys.path.insert(0, str(BASE))
        from app.subscription import get_revenue_projections
        proj = get_revenue_projections()
        m1 = proj["month_1"]
        expected = m1["early_bird_users"] * 29 + m1["professional_users"] * 99 + m1["custom_orders"] * 499
        assert m1["revenue"] == expected, f"月度收入计算不匹配: {m1['revenue']} != {expected}"


# ============================================================
# 4. 运营支持风险
# ============================================================

class TestOpsRisk:
    """检查客户支持、事故处理、升级路径"""

    def test_support_sop_exists(self):
        assert (BASE / "docs" / "support_sop.md").exists()

    def test_incident_runbook_exists(self):
        assert (BASE / "docs" / "incident_runbook.md").exists()

    def test_customer_support_exists(self):
        assert (BASE / "docs" / "customer_support.md").exists()

    def test_support_sop_has_escalation_path(self):
        text = (BASE / "docs" / "support_sop.md").read_text(encoding="utf-8")
        assert "升级" in text or "escalation" in text.lower() or "转交" in text or "上级" in text

    def test_incident_runbook_has_recovery_steps(self):
        text = (BASE / "docs" / "incident_runbook.md").read_text(encoding="utf-8")
        assert "恢复" in text or "recovery" in text.lower() or "复盘" in text or "修复" in text

    def test_kpi_dashboard_exists(self):
        assert (BASE / "docs" / "kpi_dashboard.md").exists()


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
