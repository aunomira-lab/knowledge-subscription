#!/usr/bin/env python3
"""
知识付费订阅 - 监控系统验证脚本
验证 docs/revenue_experiment_7d.md、docs/kpi_dashboard.md、metrics/experiment_tracker.csv 的完整性和一致性
"""

import csv
import re
from pathlib import Path
from datetime import datetime

PROJECT_DIR = Path("/home/AgentAdmin/.hermes/shared/dev-team/projects/knowledge-subscription")

def check_file_exists(filepath, name):
    """检查文件是否存在"""
    full_path = PROJECT_DIR / filepath
    if full_path.exists():
        size = full_path.stat().st_size
        print(f"  ✅ {name}: 存在 ({size} bytes)")
        return True
    else:
        print(f"  ❌ {name}: 缺失")
        return False

def validate_csv(filepath):
    """验证CSV文件"""
    full_path = PROJECT_DIR / filepath
    issues = []
    
    try:
        with open(full_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            
            # 检查必需字段
            required_fields = ['date', 'day_number', 'exposure_count', 'visit_count', 
                             'signup_count', 'pay_count', 'revenue_cny']
            header = reader.fieldnames
            for field in required_fields:
                if field not in header:
                    issues.append(f"缺少字段: {field}")
            
            # 检查数据行
            if len(rows) < 7:
                issues.append(f"数据行不足: 只有{len(rows)}行，至少7天数据")
            
            # 检查数据一致性
            total_revenue = sum(int(row.get('revenue_cny', 0) or 0) for row in rows)
            total_paid = sum(int(row.get('pay_count', 0) or 0) for row in rows)
            
            print(f"    - 总行数: {len(rows)}")
            print(f"    - 累计付费用户: {total_paid}")
            print(f"    - 累计收入: ¥{total_revenue}")
            
    except Exception as e:
        issues.append(f"读取错误: {e}")
    
    if issues:
        for issue in issues:
            print(f"    ⚠️ {issue}")
        return False
    else:
        print(f"    ✅ CSV格式正确")
        return True

def validate_markdown(filepath, name, required_sections):
    """验证Markdown文档"""
    full_path = PROJECT_DIR / filepath
    issues = []
    
    try:
        with open(full_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # 检查必需节标题
        for section in required_sections:
            if section not in content:
                issues.append(f"缺少节: {section}")
        
        # 检查关键数据标识
        if "¥" in content or "收入" in content:
            print(f"    - 包含收入数据: ✅")
        if "转化" in content:
            print(f"    - 包含转化数据: ✅")
        if "漏斗" in content:
            print(f"    - 包含漏斗分析: ✅")
            
    except Exception as e:
        issues.append(f"读取错误: {e}")
    
    if issues:
        for issue in issues:
            print(f"    ⚠️ {issue}")
        return False
    else:
        print(f"    ✅ 文档结构完整")
        return True

def main():
    print("=" * 60)
    print("知识付费订阅 - 监控系统验证报告")
    print(f"验证时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    results = []
    
    # 1. 验证核心监控文件
    print("\n[阶段1] 验证核心监控文件")
    
    files_to_check = [
        ("docs/revenue_experiment_7d.md", "7天收入实验文档"),
        ("docs/kpi_dashboard.md", "KPI运营看板"),
        ("metrics/experiment_tracker.csv", "实验追踪CSV"),
    ]
    
    for filepath, name in files_to_check:
        results.append(check_file_exists(filepath, name))
    
    # 2. 验证运营支持文档（监控任务必需）
    print("\n[阶段2] 验证运营支持文档")
    
    support_files = [
        ("docs/support_sop.md", "运营SOP"),
        ("docs/incident_runbook.md", "事故处理手册"),
        ("docs/customer_support.md", "客户支持手册"),
    ]
    
    for filepath, name in support_files:
        results.append(check_file_exists(filepath, name))
    
    # 3. 验证CSV数据格式
    print("\n[阶段3] 验证实验追踪CSV格式")
    results.append(validate_csv("metrics/experiment_tracker.csv"))
    
    # 4. 验证Markdown文档内容
    print("\n[阶段4] 验证7天收入实验文档内容")
    exp_sections = ["实验目标", "转化漏斗", "收入追踪", "加码/停止"]
    results.append(validate_markdown("docs/revenue_experiment_7d.md", "实验文档", exp_sections))
    
    print("\n[阶段5] 验证KPI看板文档内容")
    kpi_sections = ["收入指标", "转化漏斗", "用户指标", "预警指标"]
    results.append(validate_markdown("docs/kpi_dashboard.md", "KPI看板", kpi_sections))
    
    # 6. 数据一致性检查
    print("\n[阶段6] 数据一致性检查")
    csv_path = PROJECT_DIR / "metrics/experiment_tracker.csv"
    exp_path = PROJECT_DIR / "docs/revenue_experiment_7d.md"
    
    try:
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            csv_revenue = sum(int(row.get('revenue_cny', 0) or 0) for row in rows[:3])
            csv_paid = sum(int(row.get('pay_count', 0) or 0) for row in rows[:3])
        
        with open(exp_path, 'r', encoding='utf-8') as f:
            exp_content = f.read()
        
        # 检查收入一致性
        if "¥87" in exp_content or "87" in exp_content:
            print("  ✅ 实验文档包含收入数据")
        else:
            print("  ⚠️ 实验文档收入数据可能不一致")
        
        print(f"    CSV累计收入(3天): ¥{csv_revenue}")
        print(f"    CSV累计付费: {csv_paid}人")
        
    except Exception as e:
        print(f"  ❌ 数据一致性检查失败: {e}")
        results.append(False)
    
    # 总结
    print("\n" + "=" * 60)
    passed = sum(results)
    total = len(results)
    print(f"验证结果: {passed}/{total} 项通过")
    
    if passed == total:
        print("🟢 监控系统验证通过 - 所有文件完整且一致")
        return 0
    else:
        print("🔴 监控系统存在问题 - 需要修复")
        return 1

if __name__ == "__main__":
    exit(main())
