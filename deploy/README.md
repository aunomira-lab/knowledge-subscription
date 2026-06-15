# AI商机雷达 · 部署说明

> 项目: knowledge-subscription  
> 目标: 将销售页和订阅入口部署为可访问的公开服务  
> 部署平台: **Cloudflare Pages** (推荐) / Vercel / GitHub Pages  
> 最新更新: 2026-06-15

---

## 一、部署平台选择

| 平台 | 费用 | 自定义域名 | 全球 CDN | 构建方式 | 推荐指数 |
|------|------|----------|----------|----------|----------|
| **Cloudflare Pages** | 免费 | 支持 | 有 | 推送自动构建 | ⭐⭐⭐⭐⭐ |
| Vercel | 免费 | 支持 | 有 | 推送自动构建 | ⭐⭐⭐⭐ |
| GitHub Pages | 免费 | 支持 | 有 | 推送自动构建 | ⭐⭐⭐⭐ |
| 自建 VPS | $5-20/月 | 全控 | 需自配 | 手动上传 | ⭐⭐⭐ |

推荐理由:
- Cloudflare Pages 对静态页免费、全球每个节点快、支持自定义域名、与 Cloudflare 安全服务无缝拼接
- 不需要服务器运维、不需要骑瓦、不需要维护

---

## 二、前置条件

### 必需账号
1. **Cloudflare 账号** (免费注册): https://dash.cloudflare.com/sign-up
2. **GitHub 账号** (存库托管代码): https://github.com/signup
3. **域名** (可选): 建议购买一个简短域名如 `ai-radar.dev` 或 `aichance.com`

### 待进一步接入
4. **支付接口** (微信商户号/支付宝开放平台)
5. **邮件服务** (邮件投递定时发送简报)
6. **收款账号** (对公对私账户用于提现)

---

## 三、部署步骤

### 方式 A: Cloudflare Pages (推荐)

```bash
# 1. 安装 Wrangler CLI
npm install -g wrangler

# 2. 登录 Cloudflare
wrangler login

# 3. 进入项目目录
cd /home/AgentAdmin/.hermes/shared/dev-team/projects/knowledge-subscription

# 4. 创建页面项目
wrangler pages project create ai-radar-sales

# 5. 发布 site/
wrangler pages deploy site --project-name=ai-radar-sales

# 6. 记录返回的公开 URL
# 示例: https://ai-radar-sales.pages.dev
```

### 方式 B: GitHub Pages (更简单)

```bash
# 1. 创建 GitHub 存库
# 2. 将 site/ 内容推送到 gh-pages 分支或启用 Pages 功能
# 3. 配置自定义域名（如有）
# 4. 访问 https://<username>.github.io/<repo>
```

### 方式 C: 自建 VPS (Nginx)

见下方 deploy.sh 脚本。

---

## 四、自动化脚本

### deploy.sh 一键部署

```bash
#!/bin/bash
# deploy.sh - 一键部署到 Cloudflare Pages

set -e

PROJECT_DIR="/home/AgentAdmin/.hermes/shared/dev-team/projects/knowledge-subscription"
SITE_DIR="$PROJECT_DIR/site"
PROJECT_NAME="ai-radar-sales"

echo "[部署开始] AI商机雷达销售页..."

# 检查必需文件
if [ ! -f "$SITE_DIR/index.html" ]; then
    echo "[ERROR] 缺少 site/index.html"
    exit 1
fi

# 检查 Wrangler
if ! command -v wrangler &> /dev/null; then
    echo "[ERROR] 未安装 wrangler CLI，请先运行: npm install -g wrangler"
    exit 1
fi

# 检查登录
if ! wrangler whoami &> /dev/null; then
    echo "[ERROR] 未登录 Cloudflare，请先运行: wrangler login"
    exit 1
fi

# 部署
echo "[构建] 正在部署到 Cloudflare Pages..."
wrangler pages deploy "$SITE_DIR" --project-name="$PROJECT_NAME"

echo "[完成] 部署成功！请记录公开 URL。"
```

运行方式:
```bash
chmod +x /home/AgentAdmin/.hermes/shared/dev-team/projects/knowledge-subscription/deploy/deploy.sh
./deploy/deploy.sh
```

---

## 五、收款/联系入口

销售页已集成以下联系方式:

| 入口 | 状态 | 说明 |
|------|------|------|
| 邮件订阅 | ✅ 可用 | subscribe@ai-radar-dev.com |
| Telegram 机器人 | ⚠️ 占位 | 需要注册 Bot |
| 微信支付 | ⚠️ 占位 | 需要微信商户号 |
| 支付宝 | ⚠️ 占位 | 需要支付宝开放平台 |
| 定时自动发送简报 | ⚠️ 占位 | 需要邮件服务 + 定时任务 |

---

## 六、定时任务 (待激活)

当报告生成器完全自动化后，可添加以下 cron:

```bash
# 每日 09:00 生成并发送简报
0 9 * * * cd /home/AgentAdmin/.hermes/shared/dev-team/projects/knowledge-subscription/app && python generate_report.py >> /var/log/ai-radar.log 2>&1

# 每周一 09:00 发送深度报告
0 9 * * 1 cd /home/AgentAdmin/.hermes/shared/dev-team/projects/knowledge-subscription/app && python generate_deep_report.py >> /var/log/ai-radar.log 2>&1
```

---

## 七、公开 URL 回填

| 环境 | URL | 状态 |
|------|-----|------|
| 测试 | https://ai-radar-sales.pages.dev | 待部署 |
| 正式 | https://ai-radar.dev | 待购买域名 |
| 回填日期 | -- | 待部署后填写 |

---

## 八、排查清单

- [ ] Cloudflare 账号已注册
- [ ] GitHub 存库已创建
- [ ] Wrangler CLI 已安装
- [ ] site/index.html 已确认
- [ ] 第一次部署已完成
- [ ] 自定义域名已配置 (可选)
- [ ] 支付接口已测试
- [ ] 定时发送已验证
- [ ] 公开 URL 已回填
- [ ] 收入追踪已配置

---

## 九、当前阻塞

当前状态: **BLOCKED_BY_USER**

缺少以下账号授权，无法完成真实线上部署:
1. Cloudflare 账号（登录信息）
2. 微信商户号（收款）
3. 支付宝开放平台（收款）
4. 实名认证完整的微信号/电话号（用于注册微信商户号和小报童）

详细阻塞清单见 `../docs/deployment_blockers.md`

---

**Dev Team · deploy角色 维护**  
**最后更新: 2026-06-15**
