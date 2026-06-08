#!/usr/bin/env python3
"""
知识付费订阅 — 上线可用性检查脚本
任务ID: eff3f092
从付费用户视角检查销售页、样例内容、订阅入口、交付流程和阻塞项。
"""

import json
import os
import re
import subprocess
import sys
from pathlib import Path

BASE = Path("/home/AgentAdmin/.hermes/shared/dev-team/projects/knowledge-subscription")
SITE_DIR = BASE / "site"
REPORTS_DIR = BASE / "reports"
DOCS_DIR = BASE / "docs"
APP_DIR = BASE / "app"
SAMPLE_DIR = REPORTS_DIR / "sample_pack"
WEEK_DIR = SAMPLE_DIR / "week1_samples"

def log(msg, level="INFO"):
    print(f"[{level}] {msg}")

class UsabilityChecker:
    def __init__(self):
        self.score = 0
        self.max_score = 100
        self.passed = []
        self.failed = []
        self.blockers = []

    def check(self, name, condition, points=1, critical=False):
        if condition:
            self.score += points
            self.passed.append(name)
            log(f"✅ {name} (+{points})")
        else:
            self.failed.append(name)
            if critical:
                self.blockers.append(name)
            log(f"❌ {name} (0/{points})", "WARN" if not critical else "CRITICAL")

    def run(self):
        log("=" * 60)
        log("启动可用性检查 — 付费用户视角")
        log("=" * 60)

        # 1. 销售页基础可用性 (20分)
        log("\n--- 1. 销售页基础可用性 ---")
        html_path = SITE_DIR / "index.html"
        html = html_path.read_text(encoding="utf-8") if html_path.exists() else ""
        self.check("销售页存在", html_path.exists() and len(html) > 10000, 3, critical=True)
        self.check("DOCTYPE声明", "<!DOCTYPE html>" in html, 1)
        self.check("Viewport响应式", "width=device-width" in html, 2, critical=True)
        self.check("OG社交标签", "og:title" in html and "og:description" in html, 2)
        self.check("标题关键词", "商机雷达" in html, 1)
        self.check("移动端适配", "@media" in html, 1)
        self.check("主CTA按钮", "立即订阅" in html or "选择" in html, 2, critical=True)
        self.check("样例预览区域", "样例" in html or "#sample" in html, 2, critical=True)
        self.check("FAQ区域", "退款" in html and ("FAQ" in html or "常见问题" in html), 2, critical=True)
        self.check("联系入口", "mailto" in html or "微信" in html or "Telegram" in html, 2)
        self.check("紧迫感元素", "早鸟剩余" in html or "限量" in html or "限时" in html, 1)
        self.check("信任信号", "7天" in html or "免费试读" in html, 1)
        self.check("定价三档", "¥29" in html and "¥99" in html and "¥499" in html, 2, critical=True)

        # 2. 占位状态声明 (15分)
        log("\n--- 2. 占位状态与防误导 ---")
        self.check("页面顶部声明", "演示版本" in html or "待用户授权激活" in html, 3, critical=True)
        self.check("表单提交提示", "演示页面" in html or "实际支付系统需配置" in html, 3, critical=True)
        self.check("微信占位符", "AI-Radar-2026" in html, 2, critical=True)
        self.check("邮箱占位符", "contact@ai-radar.dev" in html, 2, critical=True)
        self.check("小报童占位链接", "xiaobot.net" in html, 2)
        self.check("爱发电占位链接", "afdian.net" in html, 2)
        self.check("隐私政策入口", "privacy" in html, 1)

        # 3. 样例内容交付物 (20分)
        log("\n--- 3. 样例内容与交付物 ---")
        self.check("免费试看版存在", (SAMPLE_DIR / "free_preview.md").exists(), 3, critical=True)
        self.check("专业版目录存在", (SAMPLE_DIR / "premium_catalog.md").exists(), 3, critical=True)
        self.check("结构化数据存在", (SAMPLE_DIR / "data.json").exists(), 2, critical=True)
        self.check("周一样例", (WEEK_DIR / "monday.md").exists(), 1)
        self.check("周二样例", (WEEK_DIR / "tuesday.md").exists(), 1)
        self.check("周三样例", (WEEK_DIR / "wednesday.md").exists(), 1)
        self.check("周四样例", (WEEK_DIR / "thursday.md").exists(), 1)
        self.check("周五样例", (WEEK_DIR / "friday.md").exists(), 1)
        self.check("周六样例", (WEEK_DIR / "saturday.md").exists(), 1)
        self.check("周日报样例", (WEEK_DIR / "sunday.md").exists(), 1)
        self.check("雷达脚本存在", (WEEK_DIR / "resources" / "scripts" / "opportunity_radar.py").exists(), 2)
        self.check("生成器存在", (APP_DIR / "sample_pack_generator.py").exists(), 2)
        self.check("免费试看无过度承诺", self._no_overpromise(), 2)
        self.check("免费试看有收益数据", self._has_revenue_data(), 2)
        self.check("免费试看有CTA", self._has_cta(), 2)
        self.check("JSON数据完整", self._json_valid(), 2)

        # 4. 订阅与定价一致性 (10分)
        log("\n--- 4. 订阅与定价一致性 ---")
        self.check("README定价一致", self._pricing_consistent(), 3, critical=True)
        self.check("订阅模块可导入", self._subscription_importable(), 3, critical=True)
        self.check("收入预测递增", self._revenue_monotonic(), 2)
        self.check("定价不冲突", self._no_pricing_conflict(), 2)

        # 5. 运营支持文档 (15分)
        log("\n--- 5. 运营支持文档 ---")
        self.check("支持SOP", (DOCS_DIR / "support_sop.md").exists(), 3, critical=True)
        self.check("事故手册", (DOCS_DIR / "incident_runbook.md").exists(), 3, critical=True)
        self.check("客户支持", (DOCS_DIR / "customer_support.md").exists(), 3, critical=True)
        self.check("上线计划", (DOCS_DIR / "launch_execution_plan.md").exists(), 2)
        self.check("阻塞清单", (DOCS_DIR / "deployment_blockers.md").exists(), 2, critical=True)
        self.check("KPI看板", (DOCS_DIR / "kpi_dashboard.md").exists(), 1)
        self.check("收入实验", (DOCS_DIR / "revenue_experiment_7d.md").exists(), 1)

        # 6. 阻塞项与上线Readiness (10分)
        log("\n--- 6. 阻塞项与上线Readiness ---")
        self.check("阻塞项已记录", self._blockers_documented(), 3, critical=True)
        self.check("支付未伪装", self._payment_not_faked(), 3, critical=True)
        self.check("部署验证存在", (REPORTS_DIR / "deployment_verification.md").exists(), 2)
        self.check("公开URL已记录", self._public_url_documented(), 2)

        # 7. 可用性静态检查 (10分)
        log("\n--- 7. 可用性静态检查 ---")
        self.check("锚点链接完整", self._anchors_valid(), 2)
        self.check("mailto作为回退", "mailto:" in html, 2)
        self.check("表单提交逻辑", "handleSubmit" in html, 2)
        self.check("部署脚本可执行", self._deploy_script_ok(), 2)
        self.check("样例报告8个机会", self._data_has_8(), 2)

        self._report()

    def _no_overpromise(self):
        try:
            text = (SAMPLE_DIR / "free_preview.md").read_text(encoding="utf-8")
            forbidden = ["稳赚", "躺赚", "guaranteed", "包赚", "必赚", "零风险"]
            return not any(w in text.lower() for w in forbidden)
        except Exception:
            return False

    def _has_revenue_data(self):
        try:
            text = (SAMPLE_DIR / "free_preview.md").read_text(encoding="utf-8")
            matches = re.findall(r"[\u00a5$]\d[\d,]*", text)
            return len(matches) >= 3
        except Exception:
            return False

    def _has_cta(self):
        try:
            text = (SAMPLE_DIR / "free_preview.md").read_text(encoding="utf-8")
            return "订阅" in text or "专业版" in text or "付费" in text
        except Exception:
            return False

    def _json_valid(self):
        try:
            with open(SAMPLE_DIR / "data.json", "r", encoding="utf-8") as f:
                data = json.load(f)
            if "opportunities" not in data or len(data["opportunities"]) < 6:
                return False
            for opp in data["opportunities"]:
                for field in ["id", "title", "category", "difficulty", "profit_estimate", "margin_rate", "action_steps"]:
                    if field not in opp:
                        return False
            return True
        except Exception:
            return False

    def _pricing_consistent(self):
        try:
            readme = (BASE / "README.md").read_text(encoding="utf-8")
            return "¥99" in readme or "¥29" in readme
        except Exception:
            return False

    def _subscription_importable(self):
        try:
            sys.path.insert(0, str(BASE))
            from app.subscription import SubscriptionPlan, PlanType
            return (SubscriptionPlan.get_plan(PlanType.EARLY_BIRD)["price"] == 29 and
                    SubscriptionPlan.get_plan(PlanType.PROFESSIONAL)["price"] == 99 and
                    SubscriptionPlan.get_plan(PlanType.CUSTOM)["price"] == 499)
        except Exception:
            return False

    def _revenue_monotonic(self):
        try:
            sys.path.insert(0, str(BASE))
            from app.subscription import get_revenue_projections
            proj = get_revenue_projections()
            revenues = [proj[k]["revenue"] for k in ["month_1", "month_3", "month_6", "month_12"]]
            return all(revenues[i] > revenues[i-1] for i in range(1, len(revenues)))
        except Exception:
            return False

    def _no_pricing_conflict(self):
        try:
            html = (SITE_DIR / "index.html").read_text(encoding="utf-8")
            readme = (BASE / "README.md").read_text(encoding="utf-8")
            return "¥99" in html and "¥99" in readme
        except Exception:
            return False

    def _blockers_documented(self):
        try:
            text = (DOCS_DIR / "deployment_blockers.md").read_text(encoding="utf-8")
            return "BLOCKED_BY_USER" in text or "阻塞" in text or "待用户" in text
        except Exception:
            return False

    def _payment_not_faked(self):
        try:
            html = (SITE_DIR / "index.html").read_text(encoding="utf-8")
            has_real = "stripe.com/checkout" in html or "weixin.qq.com" in html or "alipay.com" in html
            has_notice = ("待用户授权激活" in html or "演示" in html or
                          "实际支付系统需配置" in html or "AI-Radar-2026" in html)
            # 如果有真实支付，则不算通过；如果没有真实支付，必须有占位声明
            if has_real:
                return False
            return has_notice
        except Exception:
            return False

    def _public_url_documented(self):
        try:
            text = (DOCS_DIR / "deployment_blockers.md").read_text(encoding="utf-8")
            return "aunomira-lab.github.io" in text
        except Exception:
            return False

    def _anchors_valid(self):
        try:
            html = (SITE_DIR / "index.html").read_text(encoding="utf-8")
            hrefs = re.findall(r'href="(#\w+)"', html)
            ids = re.findall(r'id="(\w+)"', html)
            for h in set(hrefs):
                if h.lstrip("#") not in ids:
                    return False
            return True
        except Exception:
            return False

    def _deploy_script_ok(self):
        try:
            script = BASE / "deploy" / "deploy.sh"
            if not script.exists():
                script = BASE / "scripts" / "deploy.sh"
            if not script.exists():
                return False
            result = subprocess.run(["bash", "-n", str(script)], capture_output=True, text=True)
            return result.returncode == 0
        except Exception:
            return False

    def _data_has_8(self):
        try:
            with open(SAMPLE_DIR / "data.json", "r", encoding="utf-8") as f:
                data = json.load(f)
            return len(data.get("opportunities", [])) == 8
        except Exception:
            return False

    def _report(self):
        log("\n" + "=" * 60)
        log("可用性检查报告")
        log("=" * 60)
        log(f"综合得分: {self.score}/{self.max_score}")
        if self.score >= 80:
            verdict = "PASS (通过)"
        elif self.score >= 60:
            verdict = "CONDITIONAL_PASS (条件通过)"
        else:
            verdict = "FAIL (不通过)"
        log(f"判定结果: {verdict}")
        if self.blockers:
            log(f"⚠️ 存在 {len(self.blockers)} 项 BLOCKED_BY_USER 阻塞项")
            for b in self.blockers:
                log(f"   - {b}")
        log(f"通过项: {len(self.passed)}")
        log(f"未通过项: {len(self.failed)}")
        log("=" * 60)

        # 写报告文件
        report_path = REPORTS_DIR / "usability_check_eff3f092_v2.txt"
        with open(report_path, "w", encoding="utf-8") as f:
            f.write("# 可用性检查报告\n")
            f.write(f"任务ID: eff3f092\n")
            f.write(f"检查时间: {os.popen('date -Iseconds').read().strip()}\n")
            f.write(f"综合得分: {self.score}/{self.max_score}\n")
            f.write(f"判定结果: {verdict}\n\n")
            f.write("## 通过项\n")
            for p in self.passed:
                f.write(f"- ✅ {p}\n")
            f.write("\n## 未通过项\n")
            for p in self.failed:
                f.write(f"- ❌ {p}\n")
            if self.blockers:
                f.write("\n## BLOCKED_BY_USER 阻塞项\n")
                for b in self.blockers:
                    f.write(f"- ⚠️ {b}\n")
        log(f"报告已保存至: {report_path}")

        if self.score >= 60:
            sys.exit(0)
        else:
            sys.exit(1)


if __name__ == "__main__":
    checker = UsabilityChecker()
    checker.run()
