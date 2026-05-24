#!/bin/bash
# AI商机雷达 - GitHub Pages部署脚本
# 无需Cloudflare账号即可免费上线
# 执行方式: bash scripts/deploy-github-pages.sh

set -e

# 配置
PROJECT_NAME="ai-opportunity-radar"
SITE_DIR="site"
BRANCH="gh-pages"

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}  AI商机雷达 - GitHub Pages部署脚本${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# 检查环境
echo -e "${YELLOW}[1/6] 检查环境...${NC}"

if ! command -v git &> /dev/null; then
    echo -e "${RED}错误: 未安装 git${NC}"
    exit 1
fi

echo -e "${GREEN}  ✓ git 已安装${NC}"

# 检查是否在git仓库中
if [ ! -d .git ]; then
    echo -e "${YELLOW}  未初始化git仓库, 正在初始化...${NC}"
    git init
    git config user.email "deploy@ai-radar.dev"
    git config user.name "Deployer"
fi

echo -e "${GREEN}  ✓ git 仓库检查完成${NC}"

# 检查销售页
echo -e "${YELLOW}[2/6] 检查销售页...${NC}"
if [ ! -f "$SITE_DIR/index.html" ]; then
    echo -e "${RED}错误: 未找到 $SITE_DIR/index.html${NC}"
    exit 1
fi

# 验证HTML完整性
if ! grep -q "</html>" "$SITE_DIR/index.html"; then
    echo -e "${RED}错误: index.html 可能不完整${NC}"
    exit 1
fi

LINE_COUNT=$(wc -l < "$SITE_DIR/index.html")
echo -e "${GREEN}  ✓ 销售页检查通过 ($LINE_COUNT 行)${NC}"

# 检查GitHub remote
echo -e "${YELLOW}[3/6] 检查GitHub远程仓库...${NC}"

REMOTE_URL=$(git remote get-url origin 2>/dev/null || echo "")

if [ -z "$REMOTE_URL" ]; then
    echo -e "${YELLOW}  未配置远程仓库${NC}"
    echo ""
    echo -e "${YELLOW}请先在GitHub创建仓库, 然后运行:${NC}"
    echo -e "${BLUE}  git remote add origin https://github.com/YOUR_USERNAME/$PROJECT_NAME.git${NC}"
    echo ""
    echo -e "${YELLOW}或使用GitHub CLI创建:${NC}"
    echo -e "${BLUE}  gh repo create $PROJECT_NAME --public --source=. --push${NC}"
    echo ""
    exit 1
fi

echo -e "${GREEN}  ✓ 远程仓库: $REMOTE_URL${NC}"

# 部署到gh-pages分支
echo -e "${YELLOW}[4/6] 部署到 gh-pages 分支...${NC}"

# 确保在正确的目录
cd "$SITE_DIR"

# 创建新的git历史记录(只包含site目录)
git init
git config user.email "deploy@ai-radar.dev"
git config user.name "Deployer"
git add .
git commit -m "Deploy to GitHub Pages - $(date '+%Y-%m-%d %H:%M:%S')"

# 强制推送到gh-pages分支
git push --force "$REMOTE_URL" main:$BRANCH

cd ..

echo -e "${GREEN}  ✓ 部署完成${NC}"

# 显示访问链接
echo -e "${YELLOW}[5/6] 生成访问链接...${NC}"

# 提取用户名和仓库名
if [[ $REMOTE_URL =~ github\.com[/:]([^/]+)/([^/\.]+) ]]; then
    USERNAME="${BASH_REMATCH[1]}"
    REPO="${BASH_REMATCH[2]}"
    PAGES_URL="https://$USERNAME.github.io/$REPO"
    
    echo ""
    echo -e "${GREEN}========================================${NC}"
    echo -e "${GREEN}  🎉 部署成功!${NC}"
    echo -e "${GREEN}========================================${NC}"
    echo ""
    echo -e "${BLUE}线上URL:${NC} $PAGES_URL"
    echo ""
    echo -e "${YELLOW}注意:${NC}"
    echo -e "  1. DNS传播可能需要几分钟"
    echo -e "  2. 首次访问可能有延迟"
    echo -e "  3. 确保仓库 Settings > Pages 已启用"
    echo ""
    echo -e "${YELLOW}验证命令:${NC}"
    echo -e "  curl -I $PAGES_URL"
    echo ""
    
    # 保存URL到文件
    echo "$PAGES_URL" > .deployed_url
    echo "$(date '+%Y-%m-%d %H:%M:%S')" > .deployed_time
    
else
    echo -e "${YELLOW}  无法提取GitHub Pages URL, 请手动检查${NC}"
fi

# 测试部署
echo -e "${YELLOW}[6/6] 验证部署...${NC}"

if [ -f .deployed_url ]; then
    URL=$(cat .deployed_url)
    echo -e "${BLUE}  正在测试 $URL...${NC}"
    
    # 等待几秒让DNS生效
    sleep 3
    
    HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" "$URL" 2>/dev/null || echo "000")
    
    if [ "$HTTP_CODE" = "200" ]; then
        echo -e "${GREEN}  ✓ 网站访问正常 (HTTP 200)${NC}"
    elif [ "$HTTP_CODE" = "000" ]; then
        echo -e "${YELLOW}  ⚠ 暂时无法访问(可能DNS未生效), 请5分钟后重试${NC}"
    else
        echo -e "${YELLOW}  ⚠ HTTP状态码: $HTTP_CODE${NC}"
    fi
fi

echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}  部署流程完成!${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo -e "${BLUE}下一步:${NC}"
echo "  1. 访问GitHub仓库 Settings > Pages 确认已启用"
echo "  2. 更新渠道清单中的公开URL"
echo "  3. 开始执行获客计划"
echo ""
