#!/bin/bash
# deploy/activate-contact.sh
# 用途: 一键替换销售页占位符为真实信息并重新部署
# 用法: ./activate-contact.sh <微信号> <邮箱> [小报童链接] [爱发电链接]
# 示例: ./activate-contact.sh mywx123 hello@example.com https://xiaobot.net/p/xxx

set -euo pipefail
PROJECT_DIR="/home/AgentAdmin/.hermes/shared/dev-team/projects/knowledge-subscription"
HTML_FILE="$PROJECT_DIR/site/index.html"

echo "=== AI Opportunity Radar 销售页激活脚本 ==="
echo ""

# 检查参数
if [ $# -lt 2 ]; then
    echo "用法: ./activate-contact.sh <微信号> <邮箱> [小报童链接] [爱发电链接]"
    echo "示例: ./activate-contact.sh mywx123 hello@example.com https://xiaobot.net/p/xxx"
    exit 1
fi

WECHAT="$1"
EMAIL="$2"
XIAOBOT="${3:-https://xiaobot.net}"
AFDIAN="${4:-https://afdian.net}"

echo "正在替换占位符..."

# 备份原文件
cp "$HTML_FILE" "$HTML_FILE.bak.$(date +%s)"

# 替换微信号
sed -i "s/AI-Radar-2026/$WECHAT/g" "$HTML_FILE"

# 替换邮箱
sed -i "s/contact@ai-radar.dev/$EMAIL/g" "$HTML_FILE"

# 替换支付链接（如果提供了具体链接）
if [ -n "$3" ]; then
    sed -i "s|https://xiaobot.net|$XIAOBOT|g" "$HTML_FILE"
fi
if [ -n "$4" ]; then
    sed -i "s|https://afdian.net|$AFDIAN|g" "$HTML_FILE"
fi

echo "验证替换结果:"
grep "$WECHAT" "$HTML_FILE" | head -1 && echo " 微信号已替换" || echo " 微信号替换失败"
grep "$EMAIL" "$HTML_FILE" | head -1 && echo " 邮箱已替换" || echo " 邮箱替换失败"

echo ""
echo "提交并触发自动部署..."
cd "$PROJECT_DIR"
git add site/index.html
git commit -m "Activate: update contact and payment info ($(date '+%Y-%m-%d'))"
git push origin main

echo ""
echo "=== 完成 ==="
echo "GitHub Actions 将在 1-2 分钟内自动重新部署"
echo "验证: curl -s https://aunomira-lab.github.io/knowledge-subscription/ | grep '$WECHAT'"
