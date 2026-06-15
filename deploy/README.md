# AI商机雷达 - 部署说明

> 任务ID: d718d905 | 项目ID: knowledge-subscription | 编制: dev-deploy (deployer) | 更新: 2026-06-15

## 当前部署状态

**平台**: GitHub Pages (已上线)  
**备选平台**: Cloudflare Pages / Vercel / 自建 VPS  
**公开 URL**: https://aunomira-lab.github.io/knowledge-subscription/  
**部署方式**: 静态页面，无后端，适合 GitHub Pages 免费托管，支持自定义域名。

---

## 前置要求

### 已完成的部分

- [x] GitHub Pages 部署：已通过 GitHub Actions 自动部署
- [x] 销售页上线：site/index.html 已上线
- [x] 部署脚本：deploy.sh 可执行
- [x] 每日运营脚本：cron-daily.sh 可执行
- [x] 隐私政策和服务条款页面

### 待用户授权的账号

| 平台 | 用途 | 链接 | 状态 |
|------|------|------|------|
| Cloudflare | 备选部署静态站点 | https://dash.cloudflare.com | 待注册（免费） |
| 自定义域名 | 品牌化访问地址 | Namecheap/Cloudflare/Alibaba | 待购买 |
| 微信商户号 | 收款 | https://pay.weixin.qq.com | 待实名认证（个人/企业） |
| 支付宝开放平台 | 收款 | https://open.alipay.com | 待实名认证 |
| 小报童 | 微信内订阅 | https://xiaobot.net | 待注册（免费开店） |
| 爱发电 | 技术区订阅 | https://afdian.net | 待注册（免费开店） |
| 知识星球 | 社群付费 | https://zsxq.com | 待注册（免费创建，收入分成） |

---

## 快速部署步骤

### 方案 A: GitHub Pages (当前已上线)

当前已通过 GitHub Actions 自动部署到以下地址：

```
https://aunomira-lab.github.io/knowledge-subscription/
```

每次推送到 main 分支时自动更新。

### 方案 B: Cloudflare Pages (备选)

1. 注册 Cloudflare 账号 (https://dash.cloudflare.com/sign-up)
2. 安装 Wrangler CLI:
   ```bash
   npm install -g wrangler
   wrangler login
   ```
3. 进入项目目录:
   ```bash
   cd /home/AgentAdmin/.hermes/shared/dev-team/projects/knowledge-subscription
   ```
4. 执行部署脚本:
   ```bash
   ./deploy/deploy.sh
   ```
5. 返回公开 URL 示例:
   ```
   https://ai-radar-sales.pages.dev
   ```

### 方案 C: 自建 (VPS + Nginx)

1. 购买 VPS（推荐 Vultr $5/月或 Cloudflare Tunnel 免费）
2. 安装 Nginx:
   ```bash
   sudo apt update && sudo apt install nginx
   ```
3. 复制静态文件到 /var/www/ai-radar
4. 配置 Nginx server block
5. 获取公开 URL

---

## 可执行自动化脚本

### 部署脚本: deploy/deploy.sh

```bash
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
    echo "══════════════════════════════════════"
    echo "  部署成功！"
    echo "  公开访问地址: $PUBLIC_URL"
    echo "  管理后台: https://dash.cloudflare.com"
    echo "  请将上述 URL 回填到 README 和 runs/结果文件"
    echo "══════════════════════════════════════"
    echo ""
    echo "$PUBLIC_URL" > "$PROJECT_DIR/reports/public_url.txt"
    log "[完成] 公开 URL 已保存到 $PROJECT_DIR/reports/public_url.txt"
else
    log "[WARNING] 未能自动提取公开 URL，请从上述输出中手动查找"
    echo ""
    echo "══════════════════════════════════════"
    echo "  部署完成，但未能自动提取 URL"
    echo "  请查看上方输出并手动记录公开 URL"
    echo "══════════════════════════════════════"
    echo ""
fi

log "[完成] 部署脚本执行完毕"
```

### 部署验证脚本: deploy/validate-deployment.sh

已存在，运行方式:
```bash
./deploy/validate-deployment.sh
```

### 定时自动部署 (cron)

添加到 crontab:
```bash
# 每日凌晨 3:00 自动部署更新
0 3 * * * cd /home/AgentAdmin/.hermes/shared/dev-team/projects/knowledge-subscription && bash deploy/deploy.sh >> /tmp/ai-radar-deploy.log 2>&1
```

---

## 收款入口替换步骤

在 `site/index.html` 中定位以下待替换字段:

| 占位项 | 替换为 | 位置 |
|---------|--------|------|
| `subscribe@ai-radar-dev.com` | 真实邮箱 | 联系入口区块 |
| `https://t.me/ai_radar_bot` | 真实 Telegram Bot 链接 | 联系入口区块 |
| `AI-Radar-2026` | 真实微信号 | 联系入口区块 |
| 微信支付/支付宝按钮行为 | 小报童订阅链接 / 爱发电链接 / 微信活码链接 | 定价区块 |

### 推荐收款流程

1. 微信区: 使用小报童 (xiaobot.net) 收费推送，微信支付流水直接到个人银行卡。
2. 程序员区: 使用小报童或爱发电 (afdian.net) 收费。
3. 国际区: 使用 Substack 或 Gumroad 收费。

---

## 宣传平台链接替换

在 `site/index.html` 中搜索并替换以下占位:

| 平台 | 占位文字 | 替换为 |
|------|----------|--------|
| 微信公众号 | `onclick="alert('微信公众号尚未创建...')"` | `href="https://mp.weixin.qq.com/s/xxx"` |
| 小红书 | `onclick="alert('小红书账号尚未创建...')"` | `href="https://www.xiaohongshu.com/user/xxx"` |
| 即刻 | `onclick="alert('即刻圈子尚未创建...')"` | `href="https://jike.cn/xxx"` |
| Twitter/X | `onclick="alert('Twitter/X 账号尚未创建...')"` | `href="https://x.com/AI_Radar_2026"` |
| B站 | `onclick="alert('B站账号尚未创建...')"` | `href="https://space.bilibili.com/xxx"` |
| Newsletter | `onclick="alert('Newsletter 尚未配置...')"` | `href="https://ai-radar.substack.com"` |

---

## 验证清单

部署后运行以下检查:

```bash
# 1. 检查页面是否可正确打开
curl -s -o /dev/null -w "%{http_code}" https://aunomira-lab.github.io/knowledge-subscription/

# 2. 检查关键资源是否可访问
curl -s -o /dev/null -w "%{http_code}" https://aunomira-lab.github.io/knowledge-subscription/terms.html

# 3. 检查响应头和证书
curl -I https://aunomira-lab.github.io/knowledge-subscription/

# 4. 查看页面编码中是否含有关键字
curl -s https://aunomira-lab.github.io/knowledge-subscription/ | grep -E "AI商机雷达|¥29/月|GitHub Pages"

# 5. 本地开发预览
python3 -m http.server 8080 --directory site/
```

---

## 常见问题

| 问题 | 原因 | 解决 |
|------|------|------|
| 部署后 404 | 项目名或路径错误 | 检查 `wrangler pages deploy 目录` |
| 域名未生效 | DNS 未配置 | 在 Cloudflare DNS 添加 CNAME |
| 收款码不显示 | 代码未更新 | 替换小报童/爱发电链接后重新部署 |

---

## 联系信息

- 部署问题反馈: 通过当前项目的 docs/deployment_blockers.md 记录
- 任务ID: d718d905
- 项目ID: knowledge-subscription
- 维护角色: dev-deploy
- 公开URL: https://aunomira-lab.github.io/knowledge-subscription/
- 更新日期: 2026-06-15
