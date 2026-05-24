#!/bin/bash
#
# knowledge-subscription 定时自动部署脚本
# 用途: 每日自动检查 site/ 目录内容变更，如有更新则重新部署到 Cloudflare Pages
# 建议配合 crontab 每天 08:00 执行
# 创建者: dev-deploy
# 日期: 2026-05-21

set -euo pipefail

PROJECT_DIR="/home/AgentAdmin/.hermes/shared/dev-team/projects/knowledge-subscription"
BUILD_DIR="$PROJECT_DIR/site"
LAST_DEPLOY_FILE="$PROJECT_DIR/.last_deploy_hash"
LOG_FILE="/tmp/cron-deploy.log"
PROJECT_NAME="ai-opportunity-radar"

echo "[$(date '+%Y-%m-%d %H:%M:%S')] 开始检查内容更新..." >> "$LOG_FILE"

# 检查目录存在
if [ ! -d "$BUILD_DIR" ]; then
    echo "[ERROR] 构建目录不存在: $BUILD_DIR" >> "$LOG_FILE"
    exit 1
fi

# 计算当前内容哈希（包含 HTML、CSS、图片等）
cd "$PROJECT_DIR"
CURRENT_HASH=$(find site -type f | sort | xargs md5sum 2>/dev/null | md5sum | awk '{print $1}')

# 如果存在上次哈希且相同，则跳过部署
if [ -f "$LAST_DEPLOY_FILE" ] && [ "$CURRENT_HASH" == "$(cat "$LAST_DEPLOY_FILE")" ]; then
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] 内容未变更，跳过部署 (hash=$CURRENT_HASH)" >> "$LOG_FILE"
    exit 0
fi

# 检查 wrangler 是否可用
if ! command -v wrangler >/dev/null 2>&1; then
    echo "[ERROR] wrangler CLI 未安装，请执行: npm install -g wrangler" >> "$LOG_FILE"
    exit 1
fi

# 检查 Cloudflare 登录状态
if ! wrangler whoami >/dev/null 2>&1; then
    echo "[ERROR] 未登录 Cloudflare，请执行: wrangler login" >> "$LOG_FILE"
    exit 1
fi

# 检查 index.html 存在
if [ ! -f "$BUILD_DIR/index.html" ]; then
    echo "[ERROR] 找不到 $BUILD_DIR/index.html" >> "$LOG_FILE"
    exit 1
fi

# 执行部署
echo "[$(date '+%Y-%m-%d %H:%M:%S')] 检测到内容变更，开始部署 (hash=$CURRENT_HASH)..." >> "$LOG_FILE"

if bash "$PROJECT_DIR/deploy/deploy.sh" production >> "$LOG_FILE" 2>&1; then
    echo "$CURRENT_HASH" > "$LAST_DEPLOY_FILE"
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] ✅ 自动部署完成" >> "$LOG_FILE"
else
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] ❌ 自动部署失败，请查看日志" >> "$LOG_FILE"
    exit 1
fi
