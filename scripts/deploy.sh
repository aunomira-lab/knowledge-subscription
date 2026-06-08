#!/bin/bash
# AI商机雷达 - Cloudflare Pages 一键部署脚本
# 使用: bash scripts/deploy.sh

set -euo pipefail

PROJECT_NAME="ai-opportunity-radar"
SITE_DIR="site"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

echo "=== AI商机雷达部署脚本 ==="
echo "时间: $TIMESTAMP"
echo "项目: $PROJECT_NAME"
echo "目录: $SITE_DIR"
echo ""

# 检查 Wrangler CLI
if ! command -v wrangler &> /dev/null; then
    echo "错误: 未找到 wrangler CLI。请先安装:"
    echo "  npm install -g wrangler"
    exit 1
fi

# 检查登录状态
if ! wrangler whoami &> /dev/null; then
    echo "错误: 未登录 Cloudflare。请运行:"
    echo "  wrangler login"
    exit 1
fi

# 检查 site 目录
if [ ! -d "$SITE_DIR" ]; then
    echo "错误: 未找到 $SITE_DIR 目录"
    exit 1
fi

if [ ! -f "$SITE_DIR/index.html" ]; then
    echo "错误: 未找到 $SITE_DIR/index.html"
    exit 1
fi

# 部署
echo "正在部署到 Cloudflare Pages..."
wrangler pages deploy "$SITE_DIR" --project-name="$PROJECT_NAME" --branch=main

echo ""
echo "=== 部署成功 ==="
echo "公开 URL: https://$PROJECT_NAME.pages.dev"
echo ""
echo "接下来请检查:"
echo "1. 页面是否正常打开"
echo "2. 邮箱订阅表单是否正常提交"
echo "3. 所有链接是否正确"
