#!/bin/bash
# deploy.sh - 一键部署 AI商机雷达销售页到 Cloudflare Pages
# 创建: deploy (dev-deploy) · 2026-06-15

set -euo pipefail

PROJECT_DIR="/home/AgentAdmin/.hermes/shared/dev-team/projects/knowledge-subscription"
SITE_DIR="$PROJECT_DIR/site"
PROJECT_NAME="ai-radar-sales"
LOG_FILE="/tmp/ai-radar-deploy.log"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

error_exit() {
    log "[ERROR] $1"
    exit 1
}

log "[部署开始] AI商机雷达销售页部署..."

# 检查必需文件
if [ ! -f "$SITE_DIR/index.html" ]; then
    error_exit "缺少 site/index.html，请先完成销售页内容"
fi

log "[检查] 必需文件通过: site/index.html 存在"

# 检查 Wrangler CLI
if ! command -v wrangler &> /dev/null; then
    error_exit "未安装 wrangler CLI。\n请先运行: npm install -g wrangler\n或: npx wrangler@latest"
fi

log "[检查] wrangler CLI 已安装"

# 检查 Cloudflare 登录
if ! wrangler whoami &> /dev/null; then
    error_exit "未登录 Cloudflare。请先运行: wrangler login\n请求用户授权: Cloudflare 账号"
fi

log "[检查] Cloudflare 登录验证通过"

# 检查项目是否已创建
if ! wrangler pages project list 2>/dev/null | grep -q "$PROJECT_NAME"; then
    log "[构建] 项目 $PROJECT_NAME 不存在，创建中..."
    wrangler pages project create "$PROJECT_NAME" || true
else
    log "[构建] 项目 $PROJECT_NAME 已存在"
fi

# 执行部署
log "[构建] 正在部署到 Cloudflare Pages..."
DEPLOY_OUTPUT=$(wrangler pages deploy "$SITE_DIR" --project-name="$PROJECT_NAME" --branch=main 2>&1)

log "[构建] 部署输出:\n$DEPLOY_OUTPUT"

# 提取公开 URL
PUBLIC_URL=$(echo "$DEPLOY_OUTPUT" | grep -oP 'https://[a-zA-Z0-9._-]+\.pages\.dev' | head -1)

if [ -n "$PUBLIC_URL" ]; then
    log "[完成] 公开 URL: $PUBLIC_URL"
    echo ""
    echo "════════════════════════════════════════"
    echo "  部署成功！"
    echo "  公开访问地址: $PUBLIC_URL"
    echo "  管理后台: https://dash.cloudflare.com"
    echo "  请将上述 URL 回填到 README 和 runs/结果文件"
    echo "════════════════════════════════════════"
    echo ""
    echo "$PUBLIC_URL" > "$PROJECT_DIR/reports/public_url.txt"
    log "[完成] 公开 URL 已保存到 $PROJECT_DIR/reports/public_url.txt"
else
    log "[WARNING] 未能自动提取公开 URL，请从上述输出中手动查找"
    echo ""
    echo "════════════════════════════════════════"
    echo "  部署完成，但未能自动提取 URL"
    echo "  请查看上方输出并手动记录公开 URL"
    echo "════════════════════════════════════════"
    echo ""
fi

log "[完成] 部署脚本执行完毕"
