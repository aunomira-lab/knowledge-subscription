#!/usr/bin/env python3
"""
Knowledge Subscription - 上线可用性检查脚本

执行全面的可用性检查，输出验收报告
"""

import os
import sys
import re
from pathlib import Path
from datetime import datetime

# 配置
PROJECT_DIR = Path("/home/AgentAdmin/.hermes/shared/dev-team/projects/knowledge-subscription")
REPORTS_DIR = PROJECT_DIR / "reports"

class UsabilityChecker:
    def __init__(self):
        self.results = []
        self.scores = {}
        
    def log(self, status, item, message=""):
        icon = "✅" if status == "PASS" else "❌" if status == "FAIL" else "⚠️"
        self.results.append(f"{icon} {status}: {item} {message}")
        print(f"{icon} {item}")
        
    def check_file_exists(self, path, min_size=0):
        """检查文件是否存在且非空"""
        full_path = PROJECT_DIR / path
        if not full_path.exists():
            self.log("FAIL", f"File: {path}", "文件不存在")
            return False
        size = full_path.stat().st_size
        if size < min_size:
            self.log("FAIL", f"File: {path}", f"文件太小 ({size} bytes)")
            return False
        self.log("PASS", f"File: {path}", f"({size} bytes)")
        return True
        
    def check_html_structure(self):
        """检查销售页HTML结构"""
        html_file = PROJECT_DIR / "site/index.html"
        content = html_file.read_text(encoding='utf-8')
        
        checks = [
            ("DOCTYPE", "<!DOCTYPE html>" in content),
            ("Title", "<title>" in content and "AI商机雷达" in content),
            ("Meta viewport", 'viewport' in content),
            ("Pricing ¥29", "¥29" in content),
            ("Pricing ¥99", "¥99" in content),
            ("CTA Button", 'cta-button' in content),
            ("FAQ Section", '<details' in content or 'FAQ' in content),
            ("Responsive CSS", '@media' in content),
        ]
        
        passed = sum(1 for _, check in checks if check)
        for name, check in checks:
            self.log("PASS" if check else "FAIL", f"HTML: {name}")
            
        self.scores['html_structure'] = (passed / len(checks)) * 100
        return passed == len(checks)
        
    def check_content_assets(self):
        """检查内容资产"""
        content_dir = PROJECT_DIR / "content/substack_drafts"
        if not content_dir.exists():
            self.log("FAIL", "Content Dir", "内容目录不存在")
            return False
            
        md_files = list(content_dir.glob("*.md"))
        welcome_exists = any('welcome' in f.name.lower() for f in md_files)
        free_posts = [f for f in md_files if 'free' in f.name.lower()]
        paid_posts = [f for f in md_files if 'paid' in f.name.lower()]
        
        checks = [
            ("Welcome Email", welcome_exists, len([f for f in md_files if 'welcome' in f.name.lower()])),
            ("Free Posts", len(free_posts) >= 2, len(free_posts)),
            ("Paid Posts", len(paid_posts) >= 2, len(paid_posts)),
        ]
        
        for name, check, count in checks:
            self.log("PASS" if check else "FAIL", f"Content: {name}", f"({count} files)")
            
        self.scores['content_assets'] = (sum(1 for c, _, _ in checks if c) / len(checks)) * 100
        return all(c for c, _, _ in checks)
        
    def check_documentation(self):
        """检查文档完整性"""
        docs = [
            ("docs/pricing_ladder.md", 1000),
            ("docs/deployment_blockers.md", 1000),
            ("README.md", 500),
        ]
        
        passed = 0
        for doc, min_size in docs:
            if self.check_file_exists(doc, min_size):
                passed += 1
                
        self.scores['documentation'] = (passed / len(docs)) * 100
        return passed == len(docs)
        
    def check_deployment_readiness(self):
        """检查部署就绪状态"""
        site_file = PROJECT_DIR / "site/index.html"
        deploy_readme = PROJECT_DIR / "deploy/README.md"
        
        site_ready = site_file.exists() and site_file.stat().st_size > 10000
        deploy_doc = deploy_readme.exists()
        
        checks = [
            ("Sales Page Ready", site_ready),
            ("Deploy Docs Ready", deploy_doc),
        ]
        
        for name, check in checks:
            self.log("PASS" if check else "FAIL", f"Deploy: {name}")
            
        self.scores['deployment'] = (sum(1 for _, c in checks if c) / len(checks)) * 100
        return all(c for _, c in checks)
        
    def check_blocking_issues(self):
        """检查阻塞项"""
        blockers_file = PROJECT_DIR / "docs/deployment_blockers.md"
        if not blockers_file.exists():
            self.log("FAIL", "Blockers Doc", "阻塞清单文档不存在")
            return False
            
        content = blockers_file.read_text()
        
        # 检查关键阻塞项
        blockers = [
            ("小报童账号", "小报童" in content),
            ("支付接入", "支付" in content),
            ("社媒账号", "即刻" in content or "小红书" in content),
            ("阻塞标记", "BLOCKED_BY_USER" in content),
        ]
        
        for name, found in blockers:
            self.log("PASS" if found else "WARN", f"Blocker: {name}")
            
        # 判断是否有阻塞
        has_blockers = "BLOCKED_BY_USER" in content
        self.scores['blockers'] = 50 if has_blockers else 100  # 有阻塞则半分
        return True
        
    def run_tests_summary(self):
        """运行测试摘要"""
        import subprocess
        try:
            result = subprocess.run(
                ["python3", "-m", "pytest", "tests", "-q"],
                cwd=PROJECT_DIR,
                capture_output=True,
                text=True,
                timeout=30
            )
            output = result.stdout + result.stderr
            
            # 解析测试结果
            match = re.search(r'(\d+) passed', output)
            passed = int(match.group(1)) if match else 0
            match = re.search(r'(\d+) failed', output)
            failed = int(match.group(1)) if match else 0
            
            total = passed + failed
            if total > 0:
                rate = (passed / total) * 100
                self.log("PASS" if failed == 0 else "FAIL", 
                        f"Tests: {passed}/{total} passed", 
                        f"({rate:.1f}%)")
                self.scores['tests'] = rate
            else:
                self.log("WARN", "Tests", "无法解析测试结果")
                self.scores['tests'] = 0
                
        except Exception as e:
            self.log("FAIL", "Tests", str(e))
            self.scores['tests'] = 0
            
    def generate_report(self):
        """生成验收报告"""
        print("\n" + "="*60)
        print("KNOWLEDGE SUBSCRIPTION - 上线可用性验收报告")
        print("="*60)
        print(f"执行时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"任务ID: 4c927c2e")
        print(f"验收员: dev-tester")
        print("-"*60)
        
        # 计算总分
        weights = {
            'html_structure': 0.20,
            'content_assets': 0.20,
            'documentation': 0.15,
            'deployment': 0.15,
            'tests': 0.20,
            'blockers': 0.10
        }
        
        total_score = sum(self.scores.get(k, 0) * w for k, w in weights.items())
        
        print("\n【详细结果】")
        for r in self.results:
            print(f"  {r}")
            
        print("\n【评分摘要】")
        for category, score in self.scores.items():
            print(f"  {category:20s}: {score:5.1f}/100")
        print(f"  {'TOTAL':20s}: {total_score:5.1f}/100")
        
        # 判定
        print("\n【最终判定】")
        if total_score >= 80:
            verdict = "PASS (通过)"
        elif total_score >= 60:
            verdict = "CONDITIONAL_PASS (条件通过，存在阻塞项)"
        else:
            verdict = "FAIL (未通过)"
            
        print(f"  综合得分: {total_score:.1f}/100")
        print(f"  判定结果: {verdict}")
        
        # 阻塞项提示
        if self.scores.get('blockers', 100) < 100:
            print("\n  ⚠️ 重要提示: 存在 BLOCKED_BY_USER 阻塞项")
            print("     需用户完成小报童/社媒账号注册后才能上线")
            
        print("\n" + "="*60)
        
        # 将结果写入文件
        report_path = REPORTS_DIR / "usability_check_result.txt"
        with open(report_path, 'w') as f:
            f.write(f"Usability Check Result\n")
            f.write(f"Time: {datetime.now().isoformat()}\n")
            f.write(f"Task ID: 4c927c2e\n")
            f.write(f"Score: {total_score:.1f}/100\n")
            f.write(f"Verdict: {verdict}\n")
            f.write("\nDetails:\n")
            for r in self.results:
                f.write(f"  {r}\n")
                
        print(f"\n报告已保存至: {report_path}")
        return total_score
        
    def run(self):
        """执行完整检查"""
        print("\n开始可用性验收检查...\n")
        
        self.check_html_structure()
        self.check_content_assets()
        self.check_documentation()
        self.check_deployment_readiness()
        self.run_tests_summary()
        self.check_blocking_issues()
        
        return self.generate_report()

if __name__ == "__main__":
    checker = UsabilityChecker()
    score = checker.run()
    sys.exit(0 if score >= 60 else 1)
