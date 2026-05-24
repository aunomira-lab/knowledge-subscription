#!/bin/bash
#
# AI Opportunity Radar - Cloudflare Pages 部署脚本
# 使用: ./deploy.sh [staging|production]
#

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 配置
PROJECT_NAME="ai-opportunity-radar"
BUILD_DIR="site"
DEPLOY_ENV="${1:-production}"

echo -e "${BLUE}=== AI Opportunity Radar 部署脚本 ===${NC}"
echo -e "环境: $DEPLOY_ENV"
echo ""

# 检查命令
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# 检查 Node.js
if ! command_exists node; then
    echo -e "${RED}错误: 需要安装 Node.js${NC}"
    echo "安装指南: https://nodejs.org/"
    exit 1
fi

# 检查 wrangler
if ! command_exists wrangler; then
    echo -e "${YELLOW}Wrangler CLI 未安装，正在安装...${NC}"
    npm install -g wrangler
fi

# 检查登录状态（支持 OAuth 和 API Token 两种模式）
echo -e "${BLUE}检查 Cloudflare 登录状态...${NC}"

AUTH_OK=false
if [ -n "$CLOUDFLARE_API_TOKEN" ]; then
    echo -e "${GREEN}✅ 检测到 CLOUDFLARE_API_TOKEN 环境变量${NC}"
    AUTH_OK=true
elif wrangler whoami 2>&1 | grep -q "not authenticated"; then
    echo -e "${RED}❌ 未登录 Cloudflare${NC}"
    echo ""
    echo "请执行以下步骤之一："
    echo "  方式A (交互式): wrangler login"
    echo "  方式B (无头/CI): export CLOUDFLARE_API_TOKEN=你的Token"
    echo ""
    echo "获取 API Token: https://dash.cloudflare.com/profile/api-tokens"
    echo "所需权限: Account > Cloudflare Pages > Edit"
    exit 1
else
    echo -e "${GREEN}✅ 已登录 Cloudflare${NC}"
    AUTH_OK=true
fi

if [ "$AUTH_OK" != "true" ]; then
    exit 1
fi

# 检查项目目录
if [ ! -d "$BUILD_DIR" ]; then
    echo -e "${RED}错误: 找不到构建目录 $BUILD_DIR${NC}"
    echo "请确保在正确的项目目录中运行此脚本"
    exit 1
fi

# 检查必要文件
if [ ! -f "$BUILD_DIR/index.html" ]; then
    echo -e "${RED}错误: 找不到 $BUILD_DIR/index.html${NC}"
    exit 1
fi

echo -e "${GREEN}✅ 构建目录检查通过${NC}"

# 创建 Pages 项目（如果不存在）
echo -e "${BLUE}检查 Pages 项目...${NC}"
if ! wrangler pages project list 2>/dev/null | grep -q "$PROJECT_NAME"; then
    echo -e "${YELLOW}项目不存在，正在创建...${NC}"
    wrangler pages project create "$PROJECT_NAME"
    echo -e "${GREEN}✅ 项目创建成功${NC}"
else
    echo -e "${GREEN}✅ 项目已存在${NC}"
fi

# 执行部署
echo ""
echo -e "${BLUE}=== 开始部署 ===${NC}"
echo -e "项目: $PROJECT_NAME"
echo -e "目录: $BUILD_DIR"
echo -e "环境: $DEPLOY_ENV"
echo ""

if [ "$DEPLOY_ENV" == "staging" ]; then
    # 测试环境部署
    echo -e "${YELLOW}正在部署到测试环境...${NC}"
    wrangler pages deploy "$BUILD_DIR" \
        --project-name="$PROJECT_NAME" \
        --branch="staging" \
        --commit-hash="$(git rev-parse --short HEAD 2>/dev/null || echo 'unknown')"
else
    # 生产环境部署
    echo -e "${YELLOW}正在部署到生产环境...${NC}"
    wrangler pages deploy "$BUILD_DIR" \
        --project-name="$PROJECT_NAME" \
        --branch="main" \
        --commit-hash="$(git rev-parse --short HEAD 2>/dev/null || echo 'unknown')"
fi

# 获取部署URL
echo ""
echo -e "${BLUE}=== 部署完成 ===${NC}"

if [ "$DEPLOY_ENV" == "staging" ]; then
    DEPLOY_URL="https://staging.$PROJECT_NAME.pages.dev"
else
    DEPLOY_URL="https://$PROJECT_NAME.pages.dev"
fi

echo -e "${GREEN}✅ 部署成功!${NC}"
echo ""
echo -e "🔗 访问地址: ${BLUE}$DEPLOY_URL${NC}"
echo ""

# 验证部署
echo -e "${BLUE}=== 验证部署 ===${NC}"
echo "正在检查网站可访问性..."

if command_exists curl; then
    HTTP_STATUS=$(curl -s -o /dev/null -w "%{http_code}" "$DEPLOY_URL" || echo "000")
    if [ "$HTTP_STATUS" == "200" ]; then
        echo -e "${GREEN}✅ 网站返回 200 OK${NC}"
    else
        echo -e "${YELLOW}⚠️ 网站返回状态码: $HTTP_STATUS (DNS可能还在生效中)${NC}"
    fi
else
    echo -e "${YELLOW}⚠️ 未安装 curl，跳过验证${NC}"
fi

# 生成部署记录
DEPLOY_TIME=$(date '+%Y-%m-%d %H:%M:%S')
DEPLOY_LOG="reports/deploy_$(date '+%Y%m%d_%H%M%S').log"

mkdir -p reports
cat > "$DEPLOY_LOG" << EOF
# 部署记录

- 时间: $DEPLOY_TIME
- 项目: $PROJECT_NAME
- 环境: $DEPLOY_ENV
- URL: $DEPLOY_URL
- 执行人: $(whoami)
- 状态: 成功

## 验证
- [ ] 页面正常显示
- [ ] 表单提交测试
- [ ] 响应式正常
- [ ] 支付流程测试
EOF

echo ""
echo -e "📝 部署记录已保存到: ${BLUE}$DEPLOY_LOG${NC}"
echo ""
echo -e "${GREEN}=== 部署流程完成 ===${NC}"

# 提示下一步
echo ""
echo "💡 下一步建议:"
echo "  1. 访问 $DEPLOY_URL 确认页面显示正常"
echo "  2. 测试表单提交功能"
echo "  3. 配置自定义域名（如需要）"
echo "  4. 更新 docs/launch_execution_plan.md 中的URL"
echo ""
