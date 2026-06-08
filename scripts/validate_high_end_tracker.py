#!/usr/bin/env python3
"""
验证 high_end_experiment_tracker.csv 格弎并生成汇总报告。
运行方式: python scripts/validate_high_end_tracker.py
"""

import csv
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CSV_PATH = PROJECT_ROOT / "metrics" / "high_end_experiment_tracker.csv"
REQUIRED_COLUMNS = [
    "date",
    "phase",
    "content_published",
    "content_title",
    "impressions",
    "visits",
    "free_signups",
    "premium_plus_visits",
    "accelerator_visits",
    "enterprise_visits",
    "premium_plus_signups",
    "accelerator_signups",
    "enterprise_signups",
    "premium_plus_revenue",
    "accelerator_revenue",
    "enterprise_revenue",
    "total_revenue",
    "cumulative_revenue",
    "experiment_decision",
    "notes",
]

def validate():
    if not CSV_PATH.exists():
        print(f"[ERROR] 文件不存在: {CSV_PATH}")
        sys.exit(1)

    with open(CSV_PATH, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        headers = reader.fieldnames or []
        missing = [c for c in REQUIRED_COLUMNS if c not in headers]
        if missing:
            print(f"[ERROR] 缺少字段: {missing}")
            sys.exit(1)

        rows = list(reader)
        def _to_float(val):
            if val is None:
                return 0.0
            s = str(val).strip().replace(",", "").replace("%", "")
            try:
                return float(s) if s else 0.0
            except ValueError:
                return 0.0

        def _to_int(val):
            if val is None:
                return 0
            s = str(val).strip().replace(",", "").replace("%", "")
            try:
                return int(float(s)) if s else 0
            except ValueError:
                return 0

        total_days = len(rows)
        published = sum(1 for r in rows if r.get("content_published") == "1")
        total_impressions = sum(_to_int(r.get("impressions", 0)) for r in rows)
        total_visits = sum(_to_int(r.get("visits", 0)) for r in rows)
        total_revenue = sum(_to_float(r.get("total_revenue", 0)) for r in rows)
        last_decision = rows[-1].get("experiment_decision", "UNKNOWN") if rows else "N/A"

    print("=" * 60)
    print("high_end_experiment_tracker.csv 验证报告")
    print("=" * 60)
    print(f"文件路径: {CSV_PATH}")
    print(f"总行数: {total_days}")
    print(f"字段检查: 通过 (共 {len(headers)} 列)")
    print(f"内容发布天数: {published}/{total_days}")
    print(f"累计曝光: {total_impressions}")
    print(f"累计访问: {total_visits}")
    print(f"累计收入: ¥{total_revenue:.2f}")
    print(f"最终决策: {last_decision}")
    print("=" * 60)
    print("验证通过。")
    return 0

if __name__ == "__main__":
    sys.exit(validate())
