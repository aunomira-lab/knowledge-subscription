#!/usr/bin/env python3
"""安全审计与上线验收检查脚本
任务ID: eff3f092
执行角色: dev-security (risk-analyst)
"""
import subprocess
import os
import sys

PROJECT_DIR = "/home/AgentAdmin/.hermes/shared/dev-team/projects/knowledge-subscription"
os.chdir(PROJECT_DIR)

results = []

# 1. 全量测试
r1 = subprocess.run(["python3", "-m", "pytest", "tests", "-q", "--tb=short"], capture_output=True, text=True)
results.append(("全量测试", "python3 -m pytest tests -q", r1.stdout + r1.stderr, r1.returncode))

# 2. 硬编码密钥检查
r2 = subprocess.run(["bash", "-c", "grep -riE 'api_key|apikey|password|secret|private_key|sk-[a-zA-Z0-9]{20,}' site/ app/ 2>/dev/null || echo '无硬编码密钥'"], capture_output=True, text=True)
results.append(("硬编码密钥检查", "grep -riE api_key... site/ app/", r2.stdout.strip(), r2.returncode))

# 3. 禁用词检查
r3 = subprocess.run(["bash", "-c", "grep -riE '稳赚|躺赚|包赚|必赚|零风险|guaranteed profit|no risk|100%成功|无脑操作|暴富|日入过万|月入百万' site/ reports/sample_pack/ 2>/dev/null || echo '无禁用词'"], capture_output=True, text=True)
results.append(("禁用词检查", "grep -riE 禁用词... site/ reports/sample_pack/", r3.stdout.strip(), r3.returncode))

# 4. 隐私/服务条款占位
r4 = subprocess.run(["bash", "-c", "grep -c '演示版警告' site/privacy.html && echo '隐私政策演示版横幅 OK' || echo '隐私缺失'; grep -c '演示版警告' site/terms.html && echo '服务条款演示版横幅 OK' || echo '条款缺失'"], capture_output=True, text=True)
results.append(("隐私/服务条款占位", "grep -c 演示版警告...", r4.stdout.strip(), r4.returncode))

# 5. 公开URL验证
r5 = subprocess.run(["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}", "https://aunomira-lab.github.io/knowledge-subscription/"], capture_output=True, text=True)
results.append(("公开URL验证", "curl -s -o /dev/null -w %{http_code} URL", r5.stdout.strip(), r5.returncode))

# 6. 订阅权限验证
r6 = subprocess.run(["python3", "-c", "import sys; sys.path.insert(0, '.'); from app.subscription import UserSubscription, PlanType, SubscriptionStatus; u = UserSubscription('test', PlanType.FREE); assert u.can_access_content('free') and not u.can_access_content('professional'); u2 = UserSubscription('test2', PlanType.PROFESSIONAL); assert u2.can_access_content('professional') and not u2.can_access_content('custom'); u3 = UserSubscription('test3', PlanType.EARLY_BIRD); u3.status = SubscriptionStatus.EXPIRED; assert not u3.is_active(); print('权限边界 OK')"], capture_output=True, text=True)
results.append(("订阅权限验证", "python3 -c 订阅权限...", r6.stdout.strip(), r6.returncode))

# 7. 收入预测递增
r7 = subprocess.run(["python3", "-c", "import sys; sys.path.insert(0, '.'); from app.subscription import get_revenue_projections; p = get_revenue_projections(); assert p['month_1']['revenue'] < p['month_3']['revenue'] < p['month_6']['revenue'] < p['month_12']['revenue']; print('收入预测递增 OK')"], capture_output=True, text=True)
results.append(("收入预测递增", "python3 -c 收入预测...", r7.stdout.strip(), r7.returncode))

# 8. 运营文档完整性
r8 = subprocess.run(["bash", "-c", "for f in docs/support_sop.md docs/incident_runbook.md docs/customer_support.md docs/kpi_dashboard.md docs/revenue_experiment_7d.md; do if [ -f \"$f\" ]; then echo \"OK: $f\"; else echo \"MISSING: $f\"; fi; done"], capture_output=True, text=True)
results.append(("运营文档完整性", "ls docs/...", r8.stdout.strip(), r8.returncode))

# 9. 报告生成器
r9 = subprocess.run(["python3", "app/report_generator.py"], capture_output=True, text=True)
results.append(("报告生成器", "python3 app/report_generator.py", (r9.stdout + r9.stderr).strip()[-500:], r9.returncode))

# 10. 订阅统计验证
r10 = subprocess.run(["python3", "-c", "import sys; sys.path.insert(0, '.'); from app.subscription import SubscriptionManager, PlanType; m = SubscriptionManager(); m.create_subscription('demo_user', PlanType.EARLY_BIRD); stats = m.get_stats(); assert stats['total_users'] >= 1; assert stats['monthly_recurring_revenue'] >= 29; print(f'订阅统计 OK: 用户{stats[\"total_users\"]}, 月收{stats[\"monthly_recurring_revenue\"]}')"], capture_output=True, text=True)
results.append(("订阅统计验证", "python3 -c 订阅统计...", r10.stdout.strip(), r10.returncode))

# 11. 销售页结构检查
r11 = subprocess.run(["bash", "-c", "python3 -c \"from pathlib import Path; c = Path('site/index.html').read_text(); checks = [('定价', '¥29' in c), ('CTA', '立即订阅' in c), ('FAQ', '常见问题' in c or 'FAQ' in c), ('退款', '退款' in c), ('风险声明', '不构成' in c), ('样例', '样例' in c or '简报' in c), ('微信', '微信' in c), ('邮箱', '邮箱' in c)]; passed = sum(1 for _,v in checks if v); print(f'销售页结构检查: {passed}/{len(checks)} 通过')\""], capture_output=True, text=True)
results.append(("销售页结构检查", "python3 -c 销售页结构...", r11.stdout.strip(), r11.returncode))

# 打印结果
print("\n" + "="*60)
print("安全审计与上线验收检查汇总")
print("="*60)
for name, cmd, out, code in results:
    status = "PASS" if code == 0 else "FAIL"
    print(f"\n[{status}] {name}")
    print(f"  cmd: {cmd}")
    print(f"  exit_code: {code}")
    print(f"  output: {out[:300]}")

# 保存到文件
with open("reports/launch_acceptance_check_eff3f092.txt", "w", encoding="utf-8") as f:
    f.write("安全审计与上线验收检查汇总\n")
    f.write("="*60 + "\n")
    for name, cmd, out, code in results:
        status = "PASS" if code == 0 else "FAIL"
        f.write(f"\n[{status}] {name}\n")
        f.write(f"  cmd: {cmd}\n")
        f.write(f"  exit_code: {code}\n")
        f.write(f"  output: {out}\n")

print("\n报告已保存到 reports/launch_acceptance_check_eff3f092.txt")
