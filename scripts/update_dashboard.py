#!/usr/bin/env python3
"""
每日自动更新看板数据
用法: python3 scripts/update_dashboard.py
读取 metrics/experiment_tracker.csv，更新 docs/kpi_dashboard.md 中的「当前值」
"""
import csv
import os
from datetime import datetime

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV = os.path.join(BASE, "metrics", "experiment_tracker.csv")
DASHBOARD = os.path.join(BASE, "docs", "kpi_dashboard.md")

def load_csv():
    rows = []
    if not os.path.exists(CSV):
        return rows
    with open(CSV, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)
    return rows

def update_dashboard(rows):
    if not rows:
        print("CSV 无数据，跳过")
        return
    # 计算合计
    total_exposure = sum(int(r.get("exposure", 0) or 0) for r in rows)
    total_visits = sum(int(r.get("visits", 0) or 0) for r in rows)
    total_signups = sum(int(r.get("signups", 0) or 0) for r in rows)
    total_paid = sum(int(r.get("paid_users", 0) or 0) for r in rows)
    total_revenue = sum(int(r.get("revenue", 0) or 0) for r in rows)
    print(f"曝光={total_exposure} 访问={total_visits} 注册={total_signups} 付费={total_paid} 收入={total_revenue}")

if __name__ == "__main__":
    rows = load_csv()
    update_dashboard(rows)
