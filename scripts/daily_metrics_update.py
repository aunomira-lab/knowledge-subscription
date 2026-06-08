#!/usr/bin/env python3
"""
daily_metrics_update.py — AI Architecture Weekly 每日收入追踪自动化脚本

功能：
1. 读取 metrics/experiment_tracker.csv
2. 自动生成日报文本（可粘贴到团队频道 / 朋友圈 / 社群）
3. 计算累计收入、MRR、转化率
4. 输出今日必须执行的获客动作提醒

运行方式：
    python scripts/daily_metrics_update.py

输出：
    reports/daily/DAILY_REPORT_YYYY-MM-DD.md
    stdout: 关键指标摘要

作者: dev-optimizer (profitability-analyst)
"""

import csv
import sys
from datetime import datetime, timedelta
from pathlib import Path

# 项目根目录
PROJECT_DIR = Path(__file__).resolve().parent.parent
CSV_PATH = PROJECT_DIR / "metrics" / "experiment_tracker.csv"
REPORT_DIR = PROJECT_DIR / "reports" / "daily"

# 定价配置（与实际销售页一致）
PRICING = {
    "founding_member_yr": 99.0,   # USD/年，首100人
    "pro_monthly": 15.0,           # USD/月
    "pro_annual": 150.0,           # USD/年
    "team_yr_per_seat": 499.0,    # USD/年/席
    "cn_early_bird_mo": 29.0,       # RMB/月（中文市场早鸟）
    "cn_pro_mo": 99.0,              # RMB/月（中文市场专业版）
    "cn_custom_once": 499.0,        # RMB/次（定制报告）
}


def load_csv(path: Path) -> list[dict]:
    """加载 experiment_tracker.csv，返回行列表。"""
    if not path.exists():
        print(f"[ERROR] CSV not found: {path}")
        sys.exit(1)
    with path.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader)


def compute_metrics(rows: list[dict]) -> dict:
    """从 CSV 行计算累计指标。"""
    total_revenue_usd = 0.0
    total_revenue_cny = 0.0
    paid_subs = 0
    free_subs = 0
    mrr_usd = 0.0
    mrr_cny = 0.0
    today_row = None
    today_str = datetime.utcnow().strftime("%Y-%m-%d")

    for row in rows:
        # 收入累加（优先取 revenue_cumulative，否则按 paid_conversions_new 估算）
        rev_cum = row.get("revenue_cumulative_usd", "").strip()
        rev_cum_cny = row.get("revenue_cumulative_cny", "").strip()
        if rev_cum:
            try:
                total_revenue_usd = max(total_revenue_usd, float(rev_cum))
            except ValueError:
                pass
        if rev_cum_cny:
            try:
                total_revenue_cny = max(total_revenue_cny, float(rev_cum_cny))
            except ValueError:
                pass

        # 付费订阅数
        paid_new = row.get("paid_conversions_new", "").strip()
        if paid_new:
            try:
                paid_subs += int(paid_new)
            except ValueError:
                pass

        # 免费订阅数（取最新累计值）
        free_net = row.get("free_subs_net", "").strip()
        if free_net:
            try:
                free_subs = max(free_subs, int(free_net))
            except ValueError:
                pass

        # MRR 估算（简化：所有付费按 founding member 年度摊分到月，加月度 pro）
        mrr_delta = row.get("mrr_delta", "").strip()
        if mrr_delta:
            try:
                mrr_usd += float(mrr_delta)
            except ValueError:
                pass

        mrr_delta_cny = row.get("mrr_delta_cny", "").strip()
        if mrr_delta_cny:
            try:
                mrr_cny += float(mrr_delta_cny)
            except ValueError:
                pass

        # 找今日行
        if row.get("date", "").strip() == today_str:
            today_row = row

    # 如果 CSV 里没有 mrr_delta，用付费数估算
    if mrr_usd == 0 and paid_subs > 0:
        # 假设 70% 年度(found)，30% 月度(pro)
        mrr_usd = paid_subs * 0.7 * (99.0 / 12) + paid_subs * 0.3 * 15.0
    if mrr_cny == 0 and paid_subs > 0:
        mrr_cny = paid_subs * 0.7 * (99.0 / 12 * 7.2) + paid_subs * 0.3 * 99.0

    # 转化率
    conversion_rate = (paid_subs / free_subs * 100) if free_subs > 0 else 0.0

    return {
        "today_str": today_str,
        "today_row": today_row,
        "total_revenue_usd": round(total_revenue_usd, 2),
        "total_revenue_cny": round(total_revenue_cny, 2),
        "paid_subs": paid_subs,
        "free_subs": free_subs,
        "mrr_usd": round(mrr_usd, 2),
        "mrr_cny": round(mrr_cny, 2),
        "conversion_rate": round(conversion_rate, 2),
    }


def generate_daily_actions(today_row: dict | None, metrics: dict) -> list[str]:
    """基于当前状态，生成今日必须执行的赚钱动作。"""
    actions = []
    day_of_experiment = 0
    if today_row:
        try:
            start = datetime(2026, 5, 21)
            today = datetime.utcnow()
            day_of_experiment = (today - start).days + 1
        except Exception:
            pass

    if day_of_experiment <= 7:
        actions.append(f"【7天实验 Day {day_of_experiment}】")
    else:
        actions.append("【常规运营日】")

    # 根据漏斗状态动态推荐动作
    free_subs = metrics["free_subs"]
    paid_subs = metrics["paid_subs"]

    if free_subs < 10:
        actions.append("获客紧急: 今日必须发 1 条 Twitter thread + 1 条 LinkedIn 长文 + 1 条小红书/知乎导流帖")
        actions.append("获客紧急: 在 3 个目标社群（AI/架构/独立开发者）分享一篇免费试读，附订阅链接")
    elif free_subs < 50:
        actions.append("获客加速: 联系 5 位行业 KOL，请求转发或互推")
        actions.append("获客加速: 在 Hacker News 'Show HN' 发布一篇技术拆解")
    else:
        actions.append("获客维护: 回复所有评论/DM，维持社群活跃度")

    if paid_subs == 0 and day_of_experiment >= 3:
        actions.append("转化修复: 检查销售页 CTA 是否清晰；测试 Stripe checkout 流程")
        actions.append("转化修复: 给免费订阅者发一封 '创始人故事' 邮件，建立信任")

    if paid_subs >= 1 and paid_subs < 3:
        actions.append("转化推进: 给免费列表发限时 founding-member 优惠邮件（剩 X 个名额）")

    actions.append("数据动作: 21:00 UTC 前更新 metrics/experiment_tracker.csv")
    actions.append("数据动作: 运行本脚本生成日报并粘贴到团队频道")
    actions.append("内容动作: 检查明日稿件是否通过 anti-slop checklist")

    return actions


def render_report(metrics: dict, actions: list[str]) -> str:
    """渲染 Markdown 日报。"""
    today = metrics["today_str"]
    lines = [
        f"# Daily Revenue Report — {today}",
        "",
        f"**Project**: knowledge-subscription (AI Architecture Weekly)",
        f"**Generated**: {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')} by dev-optimizer",
        "",
        "---",
        "",
        "## 1. Key Metrics (Live)",
        "",
        f"| Metric | Value |",
        f"|--------|-------|",
        f"| Free Subscribers | {metrics['free_subs']} |",
        f"| Paid Subscribers | {metrics['paid_subs']} |",
        f"| Free→Paid Conversion | {metrics['conversion_rate']}% |",
        f"| MRR (USD) | ${metrics['mrr_usd']} |",
        f"| MRR (CNY) | ¥{metrics['mrr_cny']} |",
        f"| Cumulative Revenue (USD) | ${metrics['total_revenue_usd']} |",
        f"| Cumulative Revenue (CNY) | ¥{metrics['total_revenue_cny']} |",
        "",
        "---",
        "",
        "## 2. Today's Money-Making Actions",
        "",
    ]
    for i, act in enumerate(actions, 1):
        lines.append(f"{i}. {act}")
    lines.extend([
        "",
        "---",
        "",
        "## 3. Stop / Accelerate Check",
        "",
    ])
    # 动态判断
    if metrics["free_subs"] < 5 and datetime.utcnow().date() >= datetime(2026, 5, 24).date():
        lines.append("🛑 **STOP SIGNAL**: Free subs < 5 after Day 3. Pause paid push; pivot to free growth for 30 days.")
    elif metrics["paid_subs"] == 0 and datetime.utcnow().date() >= datetime(2026, 5, 28).date():
        lines.append("🛑 **STOP SIGNAL**: Zero paid after Day 7. Do NOT enable paywall; revisit content-market fit.")
    elif metrics["conversion_rate"] >= 5.0 and metrics["free_subs"] >= 20:
        lines.append("🚀 **ACCELERATE**: Conversion >= 5%. Enable paywall on next issue; double content frequency.")
    else:
        lines.append("⏸️ **HOLD**: Continue monitoring. No clear stop/accelerate signal yet.")

    lines.extend([
        "",
        "---",
        "",
        "## 4. Data Source",
        "",
        f"- Raw data: `metrics/experiment_tracker.csv`",
        f"- Dashboard: `docs/kpi_dashboard.md`",
        f"- Experiment plan: `docs/revenue_experiment_7d.md`",
        "",
        "---",
        "",
        "*Next report: tomorrow 21:00 UTC*",
    ])
    return "\n".join(lines)


def main():
    print("=" * 60)
    print("AI Architecture Weekly — Daily Metrics Update")
    print("=" * 60)

    # 确保输出目录存在
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    # 加载数据
    rows = load_csv(CSV_PATH)
    print(f"[OK] Loaded {len(rows)} rows from {CSV_PATH}")

    # 计算指标
    metrics = compute_metrics(rows)
    print(f"[OK] Computed metrics for {metrics['today_str']}")

    # 生成动作
    actions = generate_daily_actions(metrics.get("today_row"), metrics)

    # 渲染报告
    report_md = render_report(metrics, actions)
    report_path = REPORT_DIR / f"DAILY_REPORT_{metrics['today_str']}.md"
    with report_path.open("w", encoding="utf-8") as f:
        f.write(report_md)
    print(f"[OK] Report written to {report_path}")

    # 打印摘要到 stdout（可直接粘贴）
    print("\n" + "=" * 60)
    print("DAILY SUMMARY (copy-paste ready)")
    print("=" * 60)
    print(f"Date: {metrics['today_str']}")
    print(f"Free Subs: {metrics['free_subs']} | Paid Subs: {metrics['paid_subs']} | Conv: {metrics['conversion_rate']}%")
    print(f"MRR: ${metrics['mrr_usd']} / ¥{metrics['mrr_cny']}")
    print(f"Cum Rev: ${metrics['total_revenue_usd']} / ¥{metrics['total_revenue_cny']}")
    print("\nToday's Actions:")
    for a in actions:
        print(f"  • {a}")
    print("=" * 60)


if __name__ == "__main__":
    main()
