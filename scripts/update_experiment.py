#!/usr/bin/env python3
"""
update_experiment.py - 知识订阅 7天收入实验数据更新脚本
作者: 小优 (dev-optimizer)
用途: 每日自动更新 experiment_tracker.csv，生成看板摘要
运行: python3 scripts/update_experiment.py
"""

import csv
import sys
import os
from datetime import datetime, timedelta
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent.parent
METRICS_DIR = PROJECT_DIR / "metrics"
TRACKER_CSV = METRICS_DIR / "experiment_tracker.csv"
DASHBOARD_SUMMARY = METRICS_DIR / "dashboard_summary.json"


def read_tracker():
    """读取实验追踪数据"""
    if not TRACKER_CSV.exists():
        print(f"ERROR: {TRACKER_CSV} 不存在")
        sys.exit(1)
    rows = []
    with open(TRACKER_CSV, "r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)
    return rows


def validate_tracker(rows):
    """验证数据结构"""
    assert len(rows) == 7, f"必须有 7 行，实际有 {len(rows)} 行"
    required_fields = [
        "date", "day_number", "exposure", "visits", "signups",
        "paid_users", "revenue", "cac", "channel", "content_type",
        "notes", "stop_signal", "boost_signal",
        "actual_cvr_visit", "actual_cvr_signup", "actual_cvr_paid",
    ]
    for row in rows:
        for field in required_fields:
            assert field in row, f"缺少字段: {field}"
    print("验证通过: experiment_tracker.csv 结构正确, 7 行数据")
    return True


def compute_summary(rows):
    """计算实验摘要"""
    total_exposure = sum(int(r["exposure"] or 0) for r in rows)
    total_visits = sum(int(r["visits"] or 0) for r in rows)
    total_signups = sum(int(r["signups"] or 0) for r in rows)
    total_paid = sum(int(r["paid_users"] or 0) for r in rows)
    total_revenue = sum(int(r["revenue"] or 0) for r in rows)
    total_cac = sum(int(r["cac"] or 0) for r in rows)

    cvr_visit = (total_visits / total_exposure * 100) if total_exposure else 0
    cvr_signup = (total_signups / total_visits * 100) if total_visits else 0
    cvr_paid = (total_paid / total_signups * 100) if total_signups else 0

    return {
        "experiment_id": "KS-7D-2026-06-15",
        "generated_at": datetime.now().isoformat(),
        "total_exposure": total_exposure,
        "total_visits": total_visits,
        "total_signups": total_signups,
        "total_paid_users": total_paid,
        "total_revenue": total_revenue,
        "total_cac": total_cac,
        "conversion_rate_visit": round(cvr_visit, 2),
        "conversion_rate_signup": round(cvr_signup, 2),
        "conversion_rate_paid": round(cvr_paid, 2),
        "target_revenue": 500,
        "revenue_gap": 500 - total_revenue,
        "status": "running" if total_revenue < 500 else "completed",
    }


def write_summary(summary):
    """写入看板摘要 JSON"""
    import json
    with open(DASHBOARD_SUMMARY, "w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
    print(f"看板摘要已写入: {DASHBOARD_SUMMARY}")


def main():
    print("=" * 50)
    print("知识订阅 7天收入实验 - 数据更新脚本")
    print("=" * 50)

    rows = read_tracker()
    validate_tracker(rows)
    summary = compute_summary(rows)
    write_summary(summary)

    print("\n实验摘要:")
    print(f"  总曝光: {summary['total_exposure']}")
    print(f"  总访问: {summary['total_visits']}")
    print(f"  总注册: {summary['total_signups']}")
    print(f"  总付费: {summary['total_paid_users']}")
    print(f"  总收入: ¥{summary['total_revenue']}")
    print(f"  目标收入: ¥{summary['target_revenue']}")
    print(f"  收入差距: ¥{summary['revenue_gap']}")
    print(f"  状态: {summary['status']}")
    print("=" * 50)
    print("更新完成")


if __name__ == "__main__":
    main()
