#!/usr/bin/env python3
"""
每日实验数据更新脚本
用途: 更新 metrics/experiment_tracker.csv 的每日数据
示例: python3 scripts/update_metrics.py --date=2026-05-11 --visits=50 --signups=10 --paid=1 --revenue=30
"""

import csv
import argparse
from datetime import datetime
from pathlib import Path

def update_daily_metrics(date, visits=0, signups=0, paid=0, revenue=0, 
                         content_published=1, content_title="TBD",
                         impressions=0, activations=0, open_rate=0,
                         new_followers=0, shares=0, feedback_count=0, complaints=0):
    """更新单日数据"""
    
    filepath = Path('metrics/experiment_tracker.csv')
    
    # 读取现有数据
    rows = []
    if filepath.exists():
        with open(filepath, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
    
    # 计算累计收入
    prev_cumulative = 0
    for row in rows:
        if row['date'] < date:
            prev_cumulative = float(row.get('cumulative_revenue', 0))
    
    cumulative_revenue = prev_cumulative + revenue
    
    # 确定实验阶段
    today = datetime.strptime(date, '%Y-%m-%d')
    start_date = datetime(2026, 5, 10)
    day_diff = (today - start_date).days
    
    if day_diff <= 0:
        phase = 'prep'
    elif day_diff <= 7:
        phase = f'day_{day_diff}'
    elif day_diff <= 14:
        phase = 'week_2'
    elif day_diff <= 21:
        phase = 'week_3'
    else:
        phase = 'month_1'
    
    # 构建新行
    new_row = {
        'date': date,
        'content_published': content_published,
        'content_title': content_title,
        'impressions': impressions,
        'visits': visits,
        'signups': signups,
        'activations': activations,
        'paid_users': paid,
        'daily_revenue': revenue,
        'cumulative_revenue': cumulative_revenue,
        'open_rate': open_rate,
        'ctr_avg': 0,
        'new_followers': new_followers,
        'shares': shares,
        'feedback_count': feedback_count,
        'complaints': complaints,
        'experiment_phase': phase,
        'notes': f'Updated at {datetime.now().strftime("%H:%M")}'
    }
    
    # 更新或添加行
    updated = False
    for i, row in enumerate(rows):
        if row['date'] == date:
            rows[i] = new_row
            updated = True
            break
    
    if not updated:
        rows.append(new_row)
        rows.sort(key=lambda x: x['date'])
    
    # 写回文件
    fieldnames = [
        'date', 'content_published', 'content_title', 'impressions', 'visits',
        'signups', 'activations', 'paid_users', 'daily_revenue', 'cumulative_revenue',
        'open_rate', 'ctr_avg', 'new_followers', 'shares', 'feedback_count',
        'complaints', 'experiment_phase', 'notes'
    ]
    
    with open(filepath, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    
    print(f"✅ 已更新 {date} 的数据")
    print(f"   访问: {visits} | 注册: {signups} | 付费: {paid} | 日收入: ¥{revenue}")
    print(f"   累计收入: ¥{cumulative_revenue:.2f}")
    print(f"   实验阶段: {phase}")

def show_summary():
    """显示实验摘要"""
    filepath = Path('metrics/experiment_tracker.csv')
    
    if not filepath.exists():
        print("⚠️ 数据文件不存在")
        return
    
    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    
    total_revenue = sum(float(r['daily_revenue']) for r in rows)
    total_paid = sum(int(r['paid_users']) for r in rows)
    total_visits = sum(int(r['visits']) for r in rows)
    total_signups = sum(int(r['signups']) for r in rows)
    
    print("\n" + "="*50)
    print("📊 实验数据摘要")
    print("="*50)
    print(f"记录天数: {len(rows)}")
    print(f"总访问: {total_visits}")
    print(f"总注册: {total_signups}")
    print(f"总付费: {total_paid}")
    print(f"总收入: ¥{total_revenue:.2f}")
    if total_visits > 0:
        print(f"转化率: {(total_paid/total_visits)*100:.2f}%")
    print("="*50)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='更新实验追踪数据')
    parser.add_argument('--date', default=datetime.now().strftime('%Y-%m-%d'), help='日期 (YYYY-MM-DD)')
    parser.add_argument('--visits', type=int, default=0, help='访问数')
    parser.add_argument('--signups', type=int, default=0, help='注册数')
    parser.add_argument('--paid', type=int, default=0, help='付费用户数')
    parser.add_argument('--revenue', type=float, default=0, help='日收入')
    parser.add_argument('--content', type=int, default=1, help='是否发布内容 (0/1)')
    parser.add_argument('--title', default='TBD', help='内容标题')
    parser.add_argument('--impressions', type=int, default=0, help='曝光量')
    parser.add_argument('--activations', type=int, default=0, help='激活数')
    parser.add_argument('--open-rate', type=float, default=0, help='打开率(%)')
    parser.add_argument('--followers', type=int, default=0, help='新增粉丝')
    parser.add_argument('--shares', type=int, default=0, help='分享数')
    parser.add_argument('--feedback', type=int, default=0, help='反馈数')
    parser.add_argument('--complaints', type=int, default=0, help='投诉数')
    parser.add_argument('--summary', action='store_true', help='显示摘要')
    
    args = parser.parse_args()
    
    if args.summary:
        show_summary()
    else:
        update_daily_metrics(
            date=args.date,
            visits=args.visits,
            signups=args.signups,
            paid=args.paid,
            revenue=args.revenue,
            content_published=args.content,
            content_title=args.title,
            impressions=args.impressions,
            activations=args.activations,
            open_rate=args.open_rate,
            new_followers=args.followers,
            shares=args.shares,
            feedback_count=args.feedback,
            complaints=args.complaints
        )
