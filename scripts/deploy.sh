#!/bin/bash
set -euo pipefail

# AI商机雷达 - 一键部署脚本
# 任务ID: d718d905
# 部署平台: Cloudflare Pages (首选) / GitHub Pages (备选)
# 用法: ./scripts/deploy.sh [cloudflare|github]

PROJECT_DIR="/home/AgentAdmin/.hermes/shared/dev-team/projects/knowledge-subscription"
SITE_DIR="$PROJECT_DIR/site"
DEPLOY_LOG="$PROJECT_DIR/reports/deployment_log.txt"
PLATFORM="${1:-github}"

echo "[$(date '+%Y-%m-%d %H:%M:%S')] === 部署开始 ===" >> "$DEPLOY_LOG"
echo "[$(date '+%Y-%m-%d %H:%M:%S')] 平台: $PLATFORM" >> "$DEPLOY_LOG"

# 1. 验证必要文件存在
echo "[$(date)] Step 1: 验证文件存在性..."
if [ ! -f "$SITE_DIR/index.html" ]; then
    echo "ERROR: index.html 不存在" >> "$DEPLOY_LOG"
    echo "FAIL: index.html missing"
    exit 1
fi

# 2. 验证 HTML 格式基本正确
echo "[$(date)] Step 2: 验证HTML格式..."
if ! grep -q "<!DOCTYPE html>" "$SITE_DIR/index.html"; then
    echo "ERROR: index.html 缺少DOCTYPE" >> "$DEPLOY_LOG"
    echo "FAIL: DOCTYPE missing"
    exit 1
fi
if ! grep -q "</html>" "$SITE_DIR/index.html"; then
    echo "ERROR: index.html 未闭合" >> "$DEPLOY_LOG"
    echo "FAIL: HTML not closed"
    exit 1
fi

# 3. 检查关键元素
echo "[$(date)] Step 3: 检查关键元素..."
REQUIRED_ELEMENTS=("#subscribe" "#pricing" "#sample" "mailto:contact@ai-radar.dev" "t.me/ai_opportunity_radar" "xiaobot.net")
MISSING=0
for elem in "${REQUIRED_ELEMENTS[@]}"; do
    if ! grep -q "$elem" "$SITE_DIR/index.html"; then
        echo "WARNING: 缺少元素 $elem" >> "$DEPLOY_LOG"
        MISSING=$((MISSING+1))
    fi
done
if [ $MISSING -gt 0 ]; then
    echo "WARNING: 共 $MISSING 个推荐元素缺失" >> "$DEPLOY_LOG"
fi

# 4. 验证页面内容（订阅入口、联系方式、定价）
echo "[$(date)] Step 4: 验证内容完整性..."
if ! grep -q "订阅" "$SITE_DIR/index.html"; then
    echo "ERROR: 页面缺少订阅入口" >> "$DEPLOY_LOG"
    echo "FAIL: no subscribe section"
    exit 1
fi
if ! grep -q "¥29" "$SITE_DIR/index.html"; then
    echo "ERROR: 页面缺少定价信息" >> "$DEPLOY_LOG"
    echo "FAIL: no pricing"
    exit 1
fi

# 5. 本地预览测试
echo "[$(date)] Step 5: 本地预览测试..."
python3 -m http.server 8888 --directory "$SITE_DIR" > /tmp/ai-radar-preview.log 2>&1 &
SERVER_PID=$!
sleep 2
if curl -s http://localhost:8888/ | grep -q "商机雷达"; then
    echo "[$(date)] 本地预览通过: http://localhost:8888" >> "$DEPLOY_LOG"
else
    echo "WARNING: 本地预览可能异常" >> "$DEPLOY_LOG"
fi
kill $SERVER_PID 2>/dev/null || true

# 6. 部署到指定平台
echo "[$(date)] Step 6: 执行部署..."
if [ "$PLATFORM" == "cloudflare" ]; then
    if command -v wrangler &> /dev/null; then
        cd "$SITE_DIR"
        wrangler pages deploy . --project-name="ai-opportunity-radar" --branch="main" 2>&1 | tee -a "$DEPLOY_LOG"
        echo "[$(date)] Cloudflare Pages 部署完成" >> "$DEPLOY_LOG"
    else
        echo "ERROR: wrangler CLI 未安装" >> "$DEPLOY_LOG"
        echo "BLOCKED: 请运行 'npm install -g wrangler' 并登录" >> "$DEPLOY_LOG"
        echo "FAIL: wrangler missing"
        exit 1
    fi
elif [ "$PLATFORM" == "github" ]; then
    # 使用已有的 GitHub Pages 部署脚本
    if [ -f "$PROJECT_DIR/scripts/deploy-github-pages.sh" ]; then
        bash "$PROJECT_DIR/scripts/deploy-github-pages.sh" 2>&1 | tee -a "$DEPLOY_LOG"
        echo "[$(date)] GitHub Pages 部署完成" >> "$DEPLOY_LOG"
    else
        echo "ERROR: deploy-github-pages.sh 不存在" >> "$DEPLOY_LOG"
        echo "FAIL: github deploy script missing"
        exit 1
    fi
else
    echo "ERROR: 未知平台 $PLATFORM" >> "$DEPLOY_LOG"
    echo "用法: ./scripts/deploy.sh [cloudflare|github]"
    exit 1
fi

# 7. 验证公开URL
echo "[$(date)] Step 7: 验证公开URL..."
URL=$(grep -oP 'https?://[^"]+' "$PROJECT_DIR/reports/deployment_verification.md" | head -1)
if [ -z "$URL" ]; then
    URL="https://aunomira-lab.github.io/knowledge-subscription/"
fi
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" "$URL" 2>/dev/null || echo "000")
if [ "$HTTP_CODE" == "200" ]; then
    echo "[$(date)] URL验证通过: $URL (HTTP 200)" >> "$DEPLOY_LOG"
    echo "PASS: $URL is live (HTTP 200)"
else
    echo "WARNING: URL返回 HTTP $HTTP_CODE" >> "$DEPLOY_LOG"
    echo "WARN: HTTP $HTTP_CODE for $URL"
fi

echo "[$(date '+%Y-%m-%d %H:%M:%S')] === 部署完成 ===" >> "$DEPLOY_LOG"
echo "DONE"
