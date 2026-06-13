#!/usr/bin/env python3
"""
验证知识付费订阅监控文档完整性
任务ID: 2d17707b
执行角色: dev-monitor
"""

import os
import csv
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

REQUIRED_FILES = [
    ("docs/revenue_experiment_7d.md", 200, "7天收入实验"),
    ("docs/kpi_dashboard.md", 150, "KPI 看板"),
    ("docs/support_sop.md", 100, "运营支持 SOP"),
    ("docs/incident_runbook.md", 150, "事故手册"),
    ("docs/customer_support.md", 100, "客户支持"),
    ("metrics/experiment_tracker.csv", 50, "实验追踪器"),
]

KEYWORD_CHECKS = [
    ("docs/revenue_experiment_7d.md", ["STOP", "ACCELERATE", "PIVOT", "绕过收款", "收入实验"]),
    ("docs/kpi_dashboard.md", ["MRR", "转化漏斗", "CAC", "LTV", "预警"]),
    ("docs/support_sop.md", ["运营流程", "质量红线", "用户入口"]),
    ("docs/incident_runbook.md", ["S1", "S2", "S3", "S4", "恢复流程"]),
    ("docs/customer_support.md", ["FAQ", "投诉", "升级路径"]),
]

def validate_files():
    all_ok = True
    print("=" * 60)
    print("文件存在性检查")
    print("=" * 60)
    for rel_path, min_lines, desc in REQUIRED_FILES:
        full_path = os.path.join(BASE_DIR, rel_path)
        if not os.path.exists(full_path):
            print(f"  ❌ {rel_path}: 缺失 ({desc})")
            all_ok = False
            continue
        with open(full_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
        line_count = len(lines)
        size = os.path.getsize(full_path)
        if line_count < min_lines:
            print(f"  ⚠️  {rel_path}: {line_count} 行 (建议 >= {min_lines}) 大小 {size} bytes")
        else:
            print(f"  ✅ {rel_path}: {line_count} 行, {size} bytes ({desc})")
    return all_ok

def validate_keywords():
    all_ok = True
    print("\n" + "=" * 60)
    print("关键词覆盖检查")
    print("=" * 60)
    for rel_path, keywords in KEYWORD_CHECKS:
        full_path = os.path.join(BASE_DIR, rel_path)
        if not os.path.exists(full_path):
            all_ok = False
            continue
        with open(full_path, "r", encoding="utf-8") as f:
            content = f.read()
        for kw in keywords:
            if kw not in content:
                print(f"  ❌ {rel_path}: 缺少关键词 '{kw}'")
                all_ok = False
            else:
                print(f"  ✅ {rel_path}: 包含 '{kw}'")
    return all_ok

def validate_csv():
    print("\n" + "=" * 60)
    print("CSV 数据结构检查")
    print("=" * 60)
    csv_path = os.path.join(BASE_DIR, "metrics/experiment_tracker.csv")
    if not os.path.exists(csv_path):
        print("  ❌ CSV 文件缺失")
        return False
    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    if len(rows) == 0:
        print("  ❌ CSV 无数据")
        return False
    required_cols = ["day", "date", "status", "revenue_cny", "paid_users", "decision"]
    headers = list(rows[0].keys())
    missing = [c for c in required_cols if c not in headers]
    if missing:
        print(f"  ❌ 缺少列: {missing}")
        return False
    print(f"  ✅ 列数: {len(headers)}, 行数: {len(rows)}")
    total_revenue = sum(int(r.get("revenue_cny", "0") or "0") for r in rows)
    print(f"  ✅ 总收入: ¥{total_revenue}")
    # 检查每行都有必填字段
    for r in rows:
        if not r.get("day") or not r.get("date"):
            print(f"  ❌ 缺少 day/date 的行: {r}")
            return False
    print("  ✅ 所有行都有必填字段")
    return True

def main():
    print("知识付费订阅监控文档验证工具")
    print("任务ID: 2d17707b | 角色: dev-monitor")
    print("=" * 60)
    ok1 = validate_files()
    ok2 = validate_keywords()
    ok3 = validate_csv()
    print("\n" + "=" * 60)
    if ok1 and ok2 and ok3:
        print("🎉 所有验证通过")
        return 0
    else:
        print("⚠️ 部分验证未通过")
        return 1

if __name__ == "__main__":
    sys.exit(main())
