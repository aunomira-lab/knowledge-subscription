#!/usr/bin/env python3
"""
实验追踪数据验证脚本
用途: 验证 metrics/experiment_tracker.csv 的完整性和一致性
"""

import csv
import sys
from datetime import datetime, timedelta

def validate_tracker(filepath='metrics/experiment_tracker.csv'):
    """验证实验追踪CSV数据"""
    errors = []
    warnings = []
    stats = {
        'total_days': 0,
        'days_with_content': 0,
        'total_revenue': 0,
        'total_paid_users': 0,
        'total_visits': 0,
        'total_signups': 0
    }
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            prev_cumulative = 0
            prev_date = None
            
            required_columns = [
                'date', 'content_published', 'content_title', 'impressions', 'visits',
                'signups', 'activations', 'paid_users', 'daily_revenue', 
                'cumulative_revenue', 'open_rate', 'ctr_avg', 'new_followers',
                'shares', 'feedback_count', 'complaints', 'experiment_phase', 'notes'
            ]
            
            # 验证表头
            if reader.fieldnames:
                missing = set(required_columns) - set(reader.fieldnames)
                if missing:
                    errors.append(f"缺少必需列: {missing}")
            
            for row_num, row in enumerate(reader, start=2):
                stats['total_days'] += 1
                
                # 验证日期格式
                try:
                    current_date = datetime.strptime(row['date'], '%Y-%m-%d')
                    if prev_date:
                        expected_date = prev_date + timedelta(days=1)
                        if current_date != expected_date:
                            warnings.append(f"行{row_num}: 日期不连续 {row['date']}")
                    prev_date = current_date
                except ValueError:
                    errors.append(f"行{row_num}: 日期格式错误 {row['date']}")
                
                # 验证数值字段
                numeric_fields = ['visits', 'signups', 'activations', 'paid_users', 
                                  'daily_revenue', 'cumulative_revenue', 'open_rate']
                for field in numeric_fields:
                    try:
                        val = float(row[field])
                        if val < 0:
                            errors.append(f"行{row_num}: {field} 不能为负数")
                    except ValueError:
                        errors.append(f"行{row_num}: {field} 不是有效数字")
                
                # 验证累计收入
                try:
                    daily = float(row['daily_revenue'])
                    cumulative = float(row['cumulative_revenue'])
                    
                    if row_num == 2:  # 第一行数据
                        if cumulative != daily:
                            warnings.append(f"行{row_num}: 首行累计收入应等于当日收入")
                    else:
                        expected_cumulative = prev_cumulative + daily
                        if abs(cumulative - expected_cumulative) > 0.01:
                            errors.append(f"行{row_num}: 累计收入计算错误 期望={expected_cumulative:.2f} 实际={cumulative:.2f}")
                    
                    prev_cumulative = cumulative
                    stats['total_revenue'] += daily
                    
                except ValueError:
                    pass
                
                # 统计
                if int(row.get('content_published', 0)) > 0:
                    stats['days_with_content'] += 1
                stats['total_paid_users'] += int(row.get('paid_users', 0))
                stats['total_visits'] += int(row.get('visits', 0))
                stats['total_signups'] += int(row.get('signups', 0))
    
    except FileNotFoundError:
        errors.append(f"文件不存在: {filepath}")
    except Exception as e:
        errors.append(f"读取文件出错: {e}")
    
    # 输出结果
    print("=" * 60)
    print("🔍 实验追踪数据验证报告")
    print("=" * 60)
    
    print("\n📊 统计概览:")
    print(f"  总天数: {stats['total_days']}")
    print(f"  发布内容天数: {stats['days_with_content']}")
    print(f"  总访问量: {stats['total_visits']}")
    print(f"  总注册数: {stats['total_signups']}")
    print(f"  总付费用户: {stats['total_paid_users']}")
    print(f"  总收入: ¥{stats['total_revenue']:.2f}")
    
    if stats['total_visits'] > 0:
        conversion_rate = (stats['total_paid_users'] / stats['total_visits']) * 100
        print(f"  整体转化率: {conversion_rate:.2f}%")
    
    if errors:
        print("\n❌ 严重错误 (需要立即修复):")
        for e in errors[:10]:  # 最多显示10条
            print(f"  - {e}")
        if len(errors) > 10:
            print(f"  ... 还有 {len(errors)-10} 个错误")
    
    if warnings:
        print("\n⚠️ 警告 (建议检查):")
        for w in warnings[:10]:
            print(f"  - {w}")
        if len(warnings) > 10:
            print(f"  ... 还有 {len(warnings)-10} 个警告")
    
    if not errors and not warnings:
        print("\n✅ 所有验证通过！数据完整无误。")
    
    print("\n" + "=" * 60)
    
    return len(errors) == 0

if __name__ == '__main__':
    filepath = sys.argv[1] if len(sys.argv) > 1 else 'metrics/experiment_tracker.csv'
    success = validate_tracker(filepath)
    sys.exit(0 if success else 1)
