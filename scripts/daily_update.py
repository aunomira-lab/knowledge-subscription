#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
知识付费订阅 - 每日数据更新脚本
使用: python daily_update.py --date 2026-04-28 --exposure 100 --clicks 20 ...
"""

import csv
import argparse
from datetime import datetime, timedelta
import os

def update_daily_metrics(data_file, date_str, metrics):
    """更新每日数据到CSV"""
    
    rows = []
    date_updated = False
    
    # 读取现有数据
    if os.path.exists(data_file):
        with open(data_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
    
    # 更新或添加新数据
    for row in rows:
        if row['date'] == date_str:
            for key, value in metrics.items():
                if key in row:
                    row[key] = str(value)
            date_updated = True
            break
    
    if not date_updated:
        # 计算实验天数
        day_num = len(rows) + 1
        new_row = {'date': date_str, 'day_of_experiment': day_num}
        new_row.update({k: str(v) for k, v in metrics.items()})
        rows.append(new_row)
    
    # 写回CSV
    if rows:
        fieldnames = ['date', 'day_of_experiment', 'exposure', 'clicks', 'content_reads', 
                     'pricing_views', 'orders', 'revenue', 'new_paid_users', 'total_paid_users',
                     'open_rate', 'ctr', 'cac', 'mrr', 'channel_wechat', 'channel_zhihu',
                     'channel_xiaohongshu', 'channel_private', 'channel_other', 'notes']
        
        with open(data_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)
        
        print(f"\u2705 数据已更新: {date_str}")
        return True
    
    return False

def calculate_summary(data_file):
    """计算实验汇总数据"""
    
    if not os.path.exists(data_file):
        print("❌ 数据文件不存在")
        return None
    
    with open(data_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    
    if not rows:
        return None
    
    total_exposure = sum(int(row.get('exposure', 0) or 0) for row in rows)
    total_clicks = sum(int(row.get('clicks', 0) or 0) for row in rows)
    total_orders = sum(int(row.get('orders', 0) or 0) for row in rows)
    total_revenue = sum(int(row.get('revenue', 0) or 0) for row in rows)
    total_paid = sum(int(row.get('new_paid_users', 0) or 0) for row in rows)
    
    # 计算转化率
    click_rate = (total_clicks / total_exposure * 100) if total_exposure > 0 else 0
    conversion_rate = (total_orders / total_clicks * 100) if total_clicks > 0 else 0
    
    summary = {
        '总曝光': total_exposure,
        '总点击': total_clicks,
        '点击率': f"{click_rate:.2f}%",
        '总订单': total_orders,
        '总收入': f"¥{total_revenue}",
        '新付费用户': total_paid,
        '转化率': f"{conversion_rate:.2f}%"
    }
    
    return summary

def check_stop_go_criteria(summary, day_num):
    """检查停止/加码条件"""
    
    alerts = []
    
    # 停止条件
    if day_num >= 7:
        if summary.get('新付费用户', 0) < 3:
            alerts.append("🛑 停止预警: 7天付费用户<3人，需求验证失败")
    
    if summary.get('转化率', '0%').replace('%', '') != '':
        rate = float(summary.get('转化率', '0%').replace('%', ''))
        if rate < 1:
            alerts.append("⚠️ 警告: 转化率<1%，漏斗可能存在问题")
    
    # 加码条件
    if summary.get('新付费用户', 0) >= 20:
        alerts.append("⬆️ 加码机会: 付费用户达20人，启动第二波推广")
    
    if summary.get('转化率', '0%').replace('%', '') != '':
        rate = float(summary.get('转化率', '0%').replace('%', ''))
        if rate >= 5:
            alerts.append("⬆️ 加码机会: 转化率达5%，复制成功模式")
    
    return alerts

def main():
    parser = argparse.ArgumentParser(description='每日数据更新脚本')
    parser.add_argument('--date', type=str, default=datetime.now().strftime('%Y-%m-%d'),
                       help='日期 (YYYY-MM-DD)')
    parser.add_argument('--exposure', type=int, default=0, help='曝光量')
    parser.add_argument('--clicks', type=int, default=0, help='点击量')
    parser.add_argument('--reads', type=int, default=0, help='内容阅读量')
    parser.add_argument('--pricing', type=int, default=0, help='定价页访问')
    parser.add_argument('--orders', type=int, default=0, help='订单数')
    parser.add_argument('--revenue', type=int, default=0, help='收入(元)')
    parser.add_argument('--new-paid', type=int, default=0, help='新增付费用户')
    parser.add_argument('--total-paid', type=int, default=0, help='总付费用户')
    parser.add_argument('--open-rate', type=float, default=0, help='打开率(%%)')
    parser.add_argument('--ctr', type=float, default=0, help='点击率(%%)')
    parser.add_argument('--notes', type=str, default='', help='备注')
    parser.add_argument('--summary', action='store_true', help='显示汇总')
    
    args = parser.parse_args()
    
    # 数据文件路径
    data_file = os.path.join(os.path.dirname(__file__), '..', 'metrics', 'experiment_tracker.csv')
    data_file = os.path.abspath(data_file)
    
    if args.summary:
        # 只显示汇总
        summary = calculate_summary(data_file)
        if summary:
            print("\n" + "="*50)
            print("📊 实验数据汇总")
            print("="*50)
            for key, value in summary.items():
                print(f"  {key}: {value}")
            
            # 检查预警
            alerts = check_stop_go_criteria(summary, 7)
            if alerts:
                print("\n" + "-"*50)
                print("🔔 预警/机会")
                print("-"*50)
                for alert in alerts:
                    print(f"  {alert}")
        return
    
    # 构建数据字典
    metrics = {
        'exposure': args.exposure,
        'clicks': args.clicks,
        'content_reads': args.reads,
        'pricing_views': args.pricing,
        'orders': args.orders,
        'revenue': args.revenue,
        'new_paid_users': args.new_paid,
        'total_paid_users': args.total_paid,
        'open_rate': args.open_rate,
        'ctr': args.ctr,
        'notes': args.notes
    }
    
    # 更新数据
    if update_daily_metrics(data_file, args.date, metrics):
        # 显示汇总
        summary = calculate_summary(data_file)
        if summary:
            print("\n📊 当前汇总:")
            for key, value in summary.items():
                print(f"  {key}: {value}")

if __name__ == '__main__':
    main()
