#!/usr/bin/env python3
"""
monitor_dashboard.py — knowledge-subscription 每日监控看板脚本

功能：
1. 读取 metrics/experiment_tracker.csv
2. 计算累计收入、MRR、转化率、漏斗指标
3. 检查是否触发预警规则
4. 输出今日必须执行的赚钱动作
5. 生成每日看板报告

运行方式：
    python scripts/monitor_dashboard.py
    # 或添加到 cron 每日9:00运行

输出：
    reports/daily/DASHBOARD_YYYY-MM-DD.md
    stdout: 关键指标摘要 + 预警信号 + 今日动作

作者: dev-monitor
版本: v4.2
任务ID: 2d17707b
"""

import csv
import sys
from datetime import datetime, timedelta
from pathlib import Path

# 项目根目录
PROJECT_DIR = Path(__file__).resolve().parent.parent
CSV_PATH = PROJECT_DIR / "metrics" / "experiment_tracker.csv"
REPORT_DIR = PROJECT_DIR / "reports" / "daily"

# 定价配置
PRICING = {
    "early_bird_mo": 69.0,
    "standard_mo": 99.0,
    "annual_yr": 799.0,
    "custom_once": 499.0,
}

# 预警阈值
ALERTS = {
    "revenue_stall_days": 3,
    "conversion_rate_danger": 0.3,
    "complaint_threshold": 3,
    "refund_threshold": 2,
    "cac_limit": 80,
    "open_rate_low": 30,
    "open_rate_days": 3,
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
    total_revenue_cny = 0.0
    total_revenue_usd = 0.0
    paid_subs = 0
    free_subs = 0
    mrr_cny = 0.0
    mrr_delta_cny = 0.0
    today_row = None
    today_str = datetime.utcnow().strftime("%Y-%m-%d")
    
    # 计算最近多少天的收入演数
    last_7_days_revenue = 0.0
    revenue_days = []
    
    for row in rows:
        # 收入累计
        rev_cum = row.get("cumulative_revenue", "").strip()
        if rev_cum:
            try:
                total_revenue_cny = max(total_revenue_cny, float(rev_cum))
            except ValueError:
                pass
        
        rev_cum_usd = row.get("revenue_cumulative_usd", "").strip()
        if rev_cum_usd:
            try:
                total_revenue_usd = max(total_revenue_usd, float(rev_cum_usd))
            except ValueError:
                pass
        
        # 付费订阅数
        paid_new = row.get("paid_users", "").strip()
        if paid_new:
            try:
                paid_subs += int(paid_new)
            except ValueError:
                pass
        
        # 免费订阅数
        free_net = row.get("free_subs_net", "").strip()
        if free_net:
            try:
                free_subs = max(free_subs, int(free_net))
            except ValueError:
                pass
        
        # MRR变化
        mrr_delta = row.get("mrr_delta_cny", "").strip()
        if mrr_delta:
            try:
                mrr_delta_cny += float(mrr_delta)
            except ValueError:
                pass
        
        # 找今日行
        if row.get("date", "").strip() == today_str:
            today_row = row
        
        # 记录每日收入用于停滞检测
        daily_rev = row.get("daily_revenue", "").strip()
        if daily_rev:
            try:
                revenue_days.append(float(daily_rev))
            except ValueError:
                revenue_days.append(0.0)
        else:
            revenue_days.append(0.0)
    
    # 简化MRR估算
    if paid_subs > 0:
        mrr_cny = paid_subs * 99.0
    
    # 转化率
    conversion_rate = (paid_subs / free_subs * 100) if free_subs > 0 else 0.0
    
    # 检测连续几天收入为0
    revenue_streak = 0
    for rev in reversed(revenue_days):
        if rev == 0:
            revenue_streak += 1
        else:
            break
    
    # 检测是否触发预警
    warnings = []
    if revenue_streak >= ALERTS["revenue_stall_days"]:
        warnings.append(f"RED: 连续{revenue_streak}天收入=0")
    if paid_subs >= 1 and conversion_rate < ALERTS["conversion_rate_danger"]:
        warnings.append(f"RED: 付费转化率{conversion_rate:.2f}% < {ALERTS['conversion_rate_danger']}%")
    
    # 检测是否触发红色预警（仅当有足够数据时）
    if len(rows) >= 3:
        last_3_complaints = sum(int(r.get("complaints", 0) or 0) for r in rows[-3:])
        if last_3_complaints >= ALERTS["complaint_threshold"]:
            warnings.append(f"RED: 近3天累计投诉{last_3_complaints}件")
    
    return {
        "today_str": today_str,
        "today_row": today_row,
        "total_revenue_cny": round(total_revenue_cny, 2),
        "total_revenue_usd": round(total_revenue_usd, 2),
        "paid_subs": paid_subs,
        "free_subs": free_subs,
        "mrr_cny": round(mrr_cny, 2),
        "conversion_rate": round(conversion_rate, 2),
        "revenue_streak": revenue_streak,
        "warnings": warnings,
    }


def generate_daily_actions(metrics: dict) -> list[str]:
    """基于当前状态，生成今日必须执行的赚钱动作。"""
    actions = []
    free_subs = metrics["free_subs"]
    paid_subs = metrics["paid_subs"]
    revenue_streak = metrics["revenue_streak"]
    
    # 基于当前日期判断实验天数
    day_of_experiment = 0
    try:
        start = datetime(2026, 6, 8)
        today = datetime.utcnow()
        day_of_experiment = (today - start).days
    except Exception:
        pass
    
    if 0 <= day_of_experiment <= 7:
        actions.append(f"[绕过收款实验 Day {day_of_experiment}] 重点：收款码上线、每日收款记录")
    else:
        actions.append("【规范运营日】")
    
    # 获客动作
    if free_subs < 10:
        actions.append("获客紧急: 今日必须发 1 篇 小红书 + 1 篇 知乎 + 1 条 即刻 引流贴")
        actions.append("获客紧急: 在3个目标社群分享免费试看版，每条带收款码/定价信息")
    elif free_subs < 50:
        actions.append("获客加速: 联系5位行业KOL请求转发或互推")
        actions.append("获客加速: 在 GitHub README 放入赞助/订阅入口")
    else:
        actions.append("获客维护: 回复所有评论/DM，维持社群活跃度")
    
    # 转化动作
    if paid_subs == 0 and day_of_experiment >= 3:
        actions.append("转化修复: 检查销售顶收款码是否正常可见，测试扫码流程")
        actions.append("转化修复: 给免费列表发一封'创始人故事'邮件建立信任")
    
    if paid_subs >= 1 and paid_subs < 3:
        actions.append("转化推进: 给免费列表发限时早鸟优惠邮件（剩 X 个名额）")
    
    # 绕过收款动作
    if revenue_streak >= 1:
        actions.append("绕过收款动作: 检查昨日是否有用户扫码未被发现，发送一条微信/邮件提醒订阅")
    
    actions.append("数据动作: 21:00 前更新 metrics/experiment_tracker.csv")
    actions.append("数据动作: 运行本脚本生成看板并检查预警")
    actions.append("内容动作: 检查明日稿件是否通过质量门禁")
    
    return actions


def render_report(metrics: dict, actions: list[str]) -> str:
    """渲染 Markdown 看板报告。"""
    today = metrics["today_str"]
    lines = [
        f"# 每日运营看板 — {today}",
        "",
        f"**Project**: knowledge-subscription (AI赚钱机会课堂)",
        f"**Generated**: {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')} by dev-monitor",
        f"**Version**: v4.2",
        f"**TaskID**: 2d17707b",
        "",
        "---",
        "",
        "## 1. 核心指标 (实时)",
        "",
        f"| 指标 | 数值 |",
        f"|--------|-------|",
        f"| 免费订阅 | {metrics['free_subs']} |",
        f"| 付费订阅 | {metrics['paid_subs']} |",
        f"| 免费→付费转化率 | {metrics['conversion_rate']}% |",
        f"| MRR (人民币) | ¥{metrics['mrr_cny']} |",
        f"| 累计收入 (人民币) | ¥{metrics['total_revenue_cny']} |",
        f"| 累计收入 (美元) | ${metrics['total_revenue_usd']} |",
        f"| 连续0收入天数 | {metrics['revenue_streak']} |",
        "",
        "---",
        "",
        "## 2. 预警状态",
        "",
    ]
    
    if metrics["warnings"]:
        for w in metrics["warnings"]:
            lines.append(f"- ❌ {w}")
    else:
        lines.append("- ✅ 无预警")
    
    lines.extend([
        "",
        "---",
        "",
        "## 3. 今日赚钱动作",
        "",
    ])
    for i, act in enumerate(actions, 1):
        lines.append(f"{i}. {act}")
    
    lines.extend([
        "",
        "---",
        "",
        "## 4. 停止 / 加码 / 保持判断",
        "",
    ])
    
    # 动态判断
    if metrics["revenue_streak"] >= 3 and datetime.utcnow().date() >= datetime(2026, 6, 11).date():
        lines.append("可止: 连续3天收入=0。检查收款码可见性+销售页流量。")
    elif metrics["paid_subs"] == 0 and datetime.utcnow().date() >= datetime(2026, 6, 15).date():
        lines.append("可止: Day 7 后仍无付费用户。重新评估产品-市场匹配。")
    elif metrics["conversion_rate"] >= 5.0 and metrics["free_subs"] >= 20:
        lines.append("加码: 转化率≥5%。立即加码投放广告+扩大内容产能。")
    else:
        lines.append("保持观察: 暂无明确可止/加码信号。继续执行绕过收款方案。")
    
    lines.extend([
        "",
        "---",
        "",
        "## 5. 数据来源",
        "",
        f"- Raw data: `metrics/experiment_tracker.csv`",
        f"- Dashboard: `docs/kpi_dashboard.md`",
        f"- Experiment plan: `docs/revenue_experiment_7d.md`",
        f"- Support docs: `docs/support_sop.md` + `docs/incident_runbook.md` + `docs/customer_support.md`",
        "",
        "---",
        "",
        "*下次看板: 明日9:00 UTC*",
    ])
    return "\n".join(lines)


def main():
    print("=" * 60)
    print("knowledge-subscription — 每日运营看板")
    print("=" * 60)
    
    # 确保输出目录存在
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    
    # 加载数据
    rows = load_csv(CSV_PATH)
    print(f"[OK] 已加载 {len(rows)} 行数据从 {CSV_PATH}")
    
    # 计算指标
    metrics = compute_metrics(rows)
    print(f"[OK] 已计算指标 — 日期: {metrics['today_str']}")
    
    # 生成动作
    actions = generate_daily_actions(metrics)
    
    # 检查预警
    if metrics["warnings"]:
        print(f"[WARN] 检测到 {len(metrics['warnings'])} 条预警:")
        for w in metrics["warnings"]:
            print(f"  ⚠️ {w}")
    else:
        print("[OK] 无预警触发")
    
    # 渲染报告
    report_md = render_report(metrics, actions)
    report_path = REPORT_DIR / f"DASHBOARD_{metrics['today_str']}.md"
    with report_path.open("w", encoding="utf-8") as f:
        f.write(report_md)
    print(f"[OK] 看板报告已写入 {report_path}")
    
    # 打印摘要到 stdout
    print("\n" + "=" * 60)
    print("每日摘要 (可复制粘贴)")
    print("=" * 60)
    print(f"日期: {metrics['today_str']}")
    print(f"免费订阅: {metrics['free_subs']} | 付费订阅: {metrics['paid_subs']} | 转化率: {metrics['conversion_rate']}%")
    print(f"MRR: ¥{metrics['mrr_cny']} | 累计收入: ¥{metrics['total_revenue_cny']} / ${metrics['total_revenue_usd']}")
    if metrics["warnings"]:
        print(f"预警: {len(metrics['warnings'])} 条")
    else:
        print("预警: 无")
    print("\n今日动作:")
    for a in actions:
        print(f"  • {a}")
    print("=" * 60)
    
    # 返回码
    return 0 if not metrics["warnings"] else 1


if __name__ == "__main__":
    exit(main())
