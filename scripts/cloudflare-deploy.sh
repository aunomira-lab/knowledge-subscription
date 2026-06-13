#!/bin/bash
set -euo pipefail

PROJECT_NAME="ai-opportunity-radar"
SITE_DIR="./site"

echo "[deploy] 开始部署到 Cloudflare Pages..."

# 检查 wrangler
if ! command -v wrangler &> /dev/null; then
    echo "[deploy] 安装 wrangler CLI..."
    npm install -g wrangler
fi

# 检查登录
if ! wrangler whoami &> /dev/null; then
    echo "[deploy] 需要登录 Cloudflare，请运行: wrangler login"
    exit 1
fi

echo "[deploy] 上传 site 目录..."
wrangler pages deploy "$SITE_DIR" --project-name="$PROJECT_NAME"

echo "[deploy] 完成。访问: https://$PROJECT_NAME.pages.dev"
echo "[deploy] 请将实际 URL 填入 reports/deployment_verification.md"
