#!/bin/bash
#
# deploy/validate-deployment.sh
# 用途: 一键验证 knowledge-subscription 部署状态
# 任务ID: 0e135fef
# 更新日期: 2026-06-01
# 负责人: dev-deploy (deployer)
#
# 运行方式:
#   chmod +x deploy/validate-deployment.sh
#   ./deploy/validate-deployment.sh
#

set -euo pipefail

PROJECT_DIR="/home/AgentAdmin/.hermes/shared/dev-team/projects/knowledge-subscription"
SITE_URL="https://aunomira-lab.github.io/knowledge-subscription/"
REPORT_FILE="$PROJECT_DIR/reports/deployment_verification.md"
RESULT_JSON="$PROJECT_DIR/runs/0e135fef_result.json"

PASS=0
FAIL=0
checks=()

log_pass() {
    echo "  ✅ $1"
    checks+=("{\"check\":\"$1\",\"status\":\"PASS\",\"exit_code\":0}")
    ((PASS++)) || true
}

log_fail() {
    echo "  ❌ $1"
    checks+=("{\"check\":\"$1\",\"status\":\"FAIL\",\"exit_code\":1}")
    ((FAIL++)) || true
}

echo "========================================"
echo "  knowledge-subscription 部署验证套件"
echo "  任务ID: 0e135fef"
echo "  时间: $(date '+%Y-%m-%d %H:%M:%S')"
echo "========================================"
echo ""

cd "$PROJECT_DIR"

# 1. 销售页文件存在性和大小
echo "[1/15] 检查销售页文件..."
if [ -f "site/index.html" ]; then
    SIZE=$(stat -c%s "site/index.html")
    if [ "$SIZE" -gt 15000 ]; then
        log_pass "site/index.html 存在且大小合理 ($SIZE bytes)"
    else
        log_fail "site/index.html 存在但大小异常 ($SIZE bytes)"
    fi
else
    log_fail "site/index.html 不存在"
fi

# 2. HTML 语法验证
echo "[2/15] HTML 语法检查..."
if python3 -c "
from html.parser import HTMLParser
class Validator(HTMLParser):
    def error(self, message): raise Exception(message)
with open('site/index.html', 'r') as f:
    Validator().feed(f.read())
" 2>/dev/null; then
    log_pass "HTML 语法正确"
else
    log_fail "HTML 语法错误"
fi

# 3. 关键内容存在性
echo "[3/15] 检查关键内容..."
grep -q 'AI Opportunity Radar' site/index.html && log_pass "标题关键词存在" || log_fail "标题关键词缺失"
grep -q '¥29' site/index.html && log_pass "定价信息存在" || log_fail "定价信息缺失"
grep -q 'handleSubmit' site/index.html && log_pass "表单逻辑存在" || log_fail "表单逻辑缺失"
grep -q 'viewport' site/index.html && log_pass "响应式 meta 存在" || log_fail "响应式 meta 缺失"
grep -q 'og:title' site/index.html && log_pass "OG 社交标签存在" || log_fail "OG 标签缺失"
grep -q 'mailto' site/index.html && log_pass "联系入口存在" || log_fail "联系入口缺失"

# 4. 部署脚本检查
echo "[4/15] 检查部署脚本..."
for script in deploy/deploy.sh deploy/cron-deploy.sh deploy/activate-contact.sh deploy/run_daily.sh; do
    if [ -f "$script" ]; then
        if bash -n "$script" 2>/dev/null; then
            log_pass "$script 语法正确"
        else
            log_fail "$script 语法错误"
        fi
        if [ -x "$script" ]; then
            log_pass "$script 具有执行权限"
        else
            log_fail "$script 缺少执行权限"
        fi
    else
        log_fail "$script 文件不存在"
    fi
done

# 5. 公开 URL 可访问性
echo "[5/15] 公开 URL 端到端验证..."
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" "$SITE_URL" 2>/dev/null || echo "000")
if [ "$HTTP_CODE" = "200" ]; then
    log_pass "公开 URL 返回 HTTP 200"
else
    log_fail "公开 URL 返回 HTTP $HTTP_CODE"
fi

# 6. 公开页面内容验证
echo "[6/15] 公开页面内容验证..."
PAGE_CONTENT=$(curl -s "$SITE_URL" 2>/dev/null || echo "")
if echo "$PAGE_CONTENT" | grep -q 'AI Opportunity Radar'; then
    log_pass "线上页面包含标题"
else
    log_fail "线上页面缺少标题"
fi
if echo "$PAGE_CONTENT" | grep -q '¥29'; then
    log_pass "线上页面包含定价"
else
    log_fail "线上页面缺少定价"
fi
if echo "$PAGE_CONTENT" | grep -q 'handleSubmit'; then
    log_pass "线上页面包含表单逻辑"
else
    log_fail "线上页面缺少表单逻辑"
fi

# 7. UTM 链接落地验证
echo "[7/15] UTM 链接落地验证..."
UTM_URL="${SITE_URL}?utm_source=zhihu&utm_medium=answer&utm_campaign=launch"
UTM_CONTENT=$(curl -s "$UTM_URL" 2>/dev/null || echo "")
if echo "$UTM_CONTENT" | grep -q 'AI Opportunity Radar'; then
    log_pass "UTM 参数链接落地正常"
else
    log_fail "UTM 参数链接落地异常"
fi

# 8. 必要文档文件存在性
echo "[8/15] 检查必要文档..."
for doc in deploy/README.md docs/launch_execution_plan.md metrics/launch_channels.csv docs/deployment_blockers.md reports/deployment_verification.md; do
    if [ -f "$doc" ]; then
        DOC_SIZE=$(stat -c%s "$doc")
        log_pass "$doc 存在 ($DOC_SIZE bytes)"
    else
        log_fail "$doc 不存在"
    fi
done

# 9. GitHub Actions workflow 检查
echo "[9/15] 检查 CI/CD 配置..."
if [ -f ".github/workflows/deploy.yml" ]; then
    log_pass "GitHub Actions workflow 存在"
else
    log_fail "GitHub Actions workflow 缺失"
fi

# 10. 支付入口检查（预期为占位状态）
echo "[10/15] 检查支付入口状态..."
if grep -q 'https://xiaobot.net' site/index.html; then
    log_pass "小报童支付入口占位已设置"
else
    log_fail "小报童支付入口缺失"
fi
if grep -q 'https://afdian.net' site/index.html; then
    log_pass "爱发电支付入口占位已设置"
else
    log_fail "爱发电支付入口缺失"
fi
if grep -q 'AI-Radar-2026' site/index.html; then
    log_pass "微信号占位符存在（待用户替换）"
else
    log_fail "微信号占位符缺失"
fi

# 11. 响应式断点检查
echo "[11/15] 响应式设计检查..."
if grep -q '@media (max-width: 640px)' site/index.html; then
    log_pass "移动端断点样式存在"
else
    log_fail "移动端断点样式缺失"
fi

# 12. 健康检查脚本运行
echo "[12/15] 运行健康检查脚本..."
HEALTH_OUTPUT=$(bash scripts/health_check.sh 2>&1 || true)
if [ -z "$HEALTH_OUTPUT" ]; then
    log_pass "health_check.sh 运行正常（无异常）"
else
    log_fail "health_check.sh 发现异常: $HEALTH_OUTPUT"
fi

# 13. 日运营脚本语法
echo "[13/15] 日运营脚本检查..."
if bash -n deploy/run_daily.sh 2>/dev/null; then
    log_pass "run_daily.sh 语法正确"
else
    log_fail "run_daily.sh 语法错误"
fi

# 14. 任务ID一致性检查
echo "[14/15] 任务ID一致性检查..."
TASK_ID_COUNT=$(grep -h 'd718d905' site/index.html deploy/README.md docs/launch_execution_plan.md docs/deployment_blockers.md reports/deployment_verification.md 2>/dev/null | wc -l)
if [ "$TASK_ID_COUNT" -ge "3" ]; then
    log_pass "任务ID d718d905 在关键文件中一致出现 ($TASK_ID_COUNT 次)"
else
    log_fail "任务ID d718d905 出现次数不足 ($TASK_ID_COUNT 次)"
fi

# 15. 盈利能力信号检查
echo "[15/15] 盈利空间信号检查..."
if grep -q '毛利率' site/index.html; then
    log_pass "销售页包含盈利/毛利率信号"
else
    log_fail "销售页缺少盈利信号"
fi
if grep -q 'LTV' docs/launch_execution_plan.md || grep -q 'CAC' docs/launch_execution_plan.md; then
    log_pass "获客计划包含 LTV/CAC 指标"
else
    log_fail "获客计划缺少 LTV/CAC 指标"
fi

echo ""
echo "========================================"
echo "  验证完成"
echo "  通过: $PASS"
echo "  失败: $FAIL"
echo "========================================"

if [ "$FAIL" -eq 0 ]; then
    echo "  状态: 🟢 全部通过"
    exit 0
else
    echo "  状态: 🔴 存在 $FAIL 项失败"
    exit 1
fi
