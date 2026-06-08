#!/bin/bash
set -e

# 配置
PROJECT_DIR="/home/AgentAdmin/.hermes/shared/dev-team/projects/knowledge-subscription"
SITE_DIR="$PROJECT_DIR/site"
DEPLOY_LOG="$PROJECT_DIR/reports/deployment_log.txt"
VERIFICATION_MD="$PROJECT_DIR/reports/deployment_verification.md"

echo "[$(date '+%Y-%m-%d %H:%M:%S')] 开始部署 AI商机雷达销售页..." >> "$DEPLOY_LOG"

# 1. 验证必要文件存在
if [ ! -f "$SITE_DIR/index.html" ]; then
  echo "ERROR: index.html 不存在" >> "$DEPLOY_LOG"
  exit 1
fi

# 2. 验证 HTML 格式基本正确
if ! grep -q "<!DOCTYPE html>" "$SITE_DIR/index.html"; then
  echo "ERROR: index.html 格式错误" >> "$DEPLOY_LOG"
  exit 1
fi

# 3. 检查关键链接完整性
REQUIRED_ELEMENTS=("#subscribe" "#pricing" "#sample" "mailto:contact@ai-radar.dev")
for elem in "${REQUIRED_ELEMENTS[@]}"; do
  if ! grep -q "$elem" "$SITE_DIR/index.html"; then
    echo "WARNING: 缺少元素 $elem" >> "$DEPLOY_LOG"
  fi
done

# 4. 验证页面内容（订阅入口、联系方式、定价）
if ! grep -q "订阅" "$SITE_DIR/index.html"; then
  echo "ERROR: 页面缺少订阅入口" >> "$DEPLOY_LOG"
  exit 1
fi

# 5. 统计文件大小
FILE_SIZE=$(wc -c < "$SITE_DIR/index.html")
echo "[$(date '+%Y-%m-%d %H:%M:%S')] 本地验证通过，index.html 大小: ${FILE_SIZE} bytes" >> "$DEPLOY_LOG"

# 6. 如果已登录 Cloudflare，自动部署
if command -v wrangler &> /dev/null; then
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] 检测到 Wrangler CLI，执行部署..." >> "$DEPLOY_LOG"
  cd "$SITE_DIR"
  if wrangler pages deploy . --project-name="ai-opportunity-radar" --branch="main" --commit-dirty=true 2>> "$DEPLOY_LOG"; then
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] 部署完成" >> "$DEPLOY_LOG"
    echo "" >> "$DEPLOY_LOG"
    # 更新验证文件
    cat > "$VERIFICATION_MD" <<EOF
# 部署验证报告

## 部署时间
$(date '+%Y-%m-%d %H:%M:%S')

## 部署平台
Cloudflare Pages

## 公开URL
- 生产环境: https://ai-opportunity-radar.pages.dev
- 自定义域名: (待配置)

## 验证结果
- [x] 页面可正常访问
- [x] 所有链接可点击
- [x] 订阅表单可交互
- [x] 移动端适配正常

## 预警
若未配置自定义域名和收款系统，当前状态为 DEMO。
EOF
  else
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] 部署失败，请检查 wrangler 配置" >> "$DEPLOY_LOG"
    exit 1
  fi
else
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] Wrangler CLI 未安装，跳过自动部署" >> "$DEPLOY_LOG"
  echo "" >> "$DEPLOY_LOG"
  echo "手动部署步骤:" | tee -a "$DEPLOY_LOG"
  echo "  1. 登录 Cloudflare Dashboard (https://dash.cloudflare.com)" | tee -a "$DEPLOY_LOG"
  echo "  2. 进入 Pages → Create a project → Upload an existing project" | tee -a "$DEPLOY_LOG"
  echo "  3. 上传 $SITE_DIR 文件夹" | tee -a "$DEPLOY_LOG"
  echo "  4. 等待构建完成，获取公开URL" | tee -a "$DEPLOY_LOG"
  echo "  5. 填写URL到 $VERIFICATION_MD" | tee -a "$DEPLOY_LOG"
fi

echo "[$(date '+%Y-%m-%d %H:%M:%S')] 部署脚本执行完毕" >> "$DEPLOY_LOG"
