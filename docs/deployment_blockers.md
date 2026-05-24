# 部署阻塞项清单

**项目**: knowledge-subscription (AI Opportunity Radar)
**任务ID**: 5fc6593c
**状态**: BLOCKED_BY_USER
**更新时间**: 2026-05-23
**报告人**: dev-deploy (deployer)
**部署平台**: Cloudflare Pages（主推）

---

## 拓扑图

```
上线路径
├── 销售页就绪 (site/index.html, 30KB+, 含OG标签/限时福利/响应式)
├── 部署脚本就绪 (deploy/deploy.sh + cron-deploy.sh, 已修复whoami检测bug)
├── 获客计划就绪 (docs/launch_execution_plan.md, 7天计划+6个平台)
├── 渠道清单就绪 (metrics/launch_channels.csv, 含UTM追踪模板)
├── 部署验证报告就绪 (reports/deployment_verification.md)
├── 用户账号授权未完成  ← 当前阻塞
│      ├── Cloudflare 账号 / wrangler login 或 API Token
│      ├── 支付渠道（小报童/爱发电/Stripe）
│      └── 联系信息（真实微信/邮箱）
└── 公开 URL 尚未生成  ← 依赖上述授权
```

---

## 阻塞项清单

### P0 — 关键阻塞（必须解决才能上线）

#### 1. Cloudflare Pages 部署授权

| 字段 | 当前值 | 需要值 | 获取方式 |
|------|--------|--------|----------|
| Cloudflare 账号 | 未注册 | 有效邮箱 | https://dash.cloudflare.com/sign-up |
| Wrangler CLI 登录 | 未登录 | OAuth 授权 | `npm install -g wrangler && wrangler login` |
| API Token (无头方式) | 空 | 创建 Custom Token | https://dash.cloudflare.com/profile/api-tokens |
| Account ID | 空 | 从 Dashboard 复制 | Dashboard 右侧边栏 |

**用户执行步骤（方案A - 本地/交互式）**:
```bash
# 1. 注册账号（浏览器访问）
open https://dash.cloudflare.com/sign-up

# 2. 安装 CLI
npm install -g wrangler

# 3. 登录（浏览器会弹出授权页）
wrangler login

# 4. 验证
wrangler whoami
```

**用户执行步骤（方案B - 服务器/无头/推荐用于本项目环境）**:
```bash
# 1. 注册账号（浏览器访问）
open https://dash.cloudflare.com/sign-up

# 2. 创建 API Token
# 访问 https://dash.cloudflare.com/profile/api-tokens
# Create Token -> Custom token
# 权限: Account > Cloudflare Pages > Edit
# 复制 Token（只显示一次，务必保存）

# 3. 在本项目环境设置环境变量并部署
export CLOUDFLARE_API_TOKEN="你的Token字符串"
cd /home/AgentAdmin/.hermes/shared/dev-team/projects/knowledge-subscription
./deploy/deploy.sh production
```

**预计耗时**: 5-10 分钟
**阻塞影响**: 无法生成 `*.pages.dev` 公开 URL，销售页无法被互联网访问。

**已知问题与修复**:
- 原 `deploy.sh` 使用 `wrangler whoami >/dev/null 2>&1` 检测登录，但 wrangler 在未登录时 exit code 仍为 0，导致误判。
- 已于 2026-05-22 修复：现在检测 whoami 输出中的 "not authenticated" 字符串，并支持 `CLOUDFLARE_API_TOKEN` 环境变量。

---

#### 2. 支付渠道配置（至少一个）

| 渠道 | 注册地址 | 要求 | 费率 | 当前状态 |
|------|----------|------|------|----------|
| **小报童** | https://xiaobot.net | 微信个人号即可 | 5-10% | 未注册 |
| **爱发电** | https://afdian.net | 手机号即可 | 6% | 未注册 |
| **Stripe** | https://stripe.com | 海外银行卡/公司 | 2.9%+$0.30 | 未注册 |

**用户执行步骤（以小报童为例）**:
```
访问 https://xiaobot.net
使用微信扫码登录
创建专栏 -> 填写名称/简介
设置价格: ¥29/月（早鸟版）
发布第一篇内容（可以是样例报告）
复制专栏链接: https://xiaobot.net/p/xxxxx
替换 site/index.html 中占位链接
```

**预计耗时**: 10-15 分钟
**阻塞影响**: 用户点击"立即订阅"后无法完成付费，转化率为 0。

---

### P1 — 重要阻塞（影响转化和信任）

#### 3. 销售页联系信息更新

| 项目 | 当前占位值 | 需替换为 | 位置 |
|------|-----------|----------|------|
| 微信号 | AI-Radar-2026 | 真实微信号 | site/index.html 页脚联系区 |
| 邮箱 | contact@ai-radar.dev | 真实邮箱 | site/index.html mailto 链接 |
| 公众号 | 未配置 | 公众号二维码（可选） | 销售页底部 |

**用户执行步骤**:
```bash
# 编辑销售页，替换占位符
vim /home/AgentAdmin/.hermes/shared/dev-team/projects/knowledge-subscription/site/index.html

# 搜索 "AI-Radar-2026" 替换为你的微信号
# 搜索 "contact@ai-radar.dev" 替换为你的邮箱
```

**预计耗时**: 3 分钟
**阻塞影响**: mailto 邮件和微信添加请求无法到达真实运营者，潜在客户流失。

---

#### 4. 自定义域名（可选，建议上线后 1 周内配置）

| 项目 | 建议值 | 费用 | 说明 |
|------|--------|------|------|
| 海外域名 | ai-radar.dev | ~$10/年 | 适合国际用户 |
| 国内域名 | ai-radar.cn | ~¥35/年 | 适合中文 SEO |

**配置方法**:
```bash
# 购买域名后，在 Cloudflare Dashboard 添加自定义域
wrangler pages domain add ai-opportunity-radar --domain=ai-radar.dev
# 然后在域名注册商添加 CNAME 指向 ai-opportunity-radar.pages.dev
```

---

### P2 — 可选优化（不阻止上线）

#### 5. 数据追踪工具

| 工具 | 用途 | 配置位置 |
|------|------|----------|
| Google Analytics | 流量分析、转化漏斗 | site/index.html `<head>` |
| 百度统计 | 国内用户补充 | 同上 |
| 腾讯分析 | 微信生态追踪 | 同上 |

**Google Analytics 代码模板**（需替换 `GA_ID`）:
```html
<script async src="https://www.googletagmanager.com/gtag/js?id=GA_ID"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'GA_ID');
</script>
```

---

## 用户授权步骤总览

### 最小上线路径（30 分钟）

```
Step 1 (10min): Cloudflare 注册 + 创建 API Token
Step 2 (10min): 小报童注册 + 创建专栏 + 复制链接
Step 3 (5min):  替换销售页占位信息（微信/邮箱/支付链接）
Step 4 (3min):  export CLOUDFLARE_API_TOKEN=xxx && ./deploy/deploy.sh production
Step 5 (2min):  记录公开 URL，回填到相关文档
```

### 验证上线成功

```bash
cd /home/AgentAdmin/.hermes/shared/dev-team/projects/knowledge-subscription

# 1. 检查销售页已更新占位信息
grep -v 'AI-Radar-2026' site/index.html | grep -v 'contact@ai-radar.dev' >/dev/null && echo "联系信息已更新" || echo "联系信息仍为占位"

# 2. 检查支付链接非占位
grep -E 'xiaobot.net/p/|afdian.net/a/' site/index.html && echo "支付链接已配置"

# 3. 执行部署
./deploy/deploy.sh production

# 4. 验证公开 URL
curl -s -o /dev/null -w "%{http_code}" https://ai-opportunity-radar.pages.dev
# 期望返回 200

# 5. 运行本地测试
python3 -m pytest tests/ -q && echo "测试通过"
```

---

## 通过条件

### 从 BLOCKED_BY_USER -> LIVE

必须完成:
- [ ] Cloudflare 账号注册并获取 API Token（或完成 wrangler login）
- [ ] 至少一个支付渠道创建并获取真实收款链接
- [ ] 销售页中的微信、邮箱、支付链接替换为真实值
- [ ] `./deploy/deploy.sh production` 执行成功并返回 200
- [ ] `reports/deployment_verification.md` 更新为 LIVE 状态并填写公开 URL

建议完成:
- [ ] 配置 Google Analytics
- [ ] 购买并配置自定义域名
- [ ] 测试端到端付费流程（从销售页点击到完成支付）
- [ ] 启动 docs/launch_execution_plan.md 中的 7 天获客计划
- [ ] 在 metrics/launch_channels.csv 中记录首日各渠道数据

---

## 联系支持

| 资源 | 路径 |
|------|------|
| 部署文档 | deploy/README.md |
| 部署验证报告 | reports/deployment_verification.md |
| 获客执行计划 | docs/launch_execution_plan.md |
| 渠道数据 | metrics/launch_channels.csv |
| 小报童帮助 | https://xiaobot.net/help |
| Cloudflare Pages 文档 | https://developers.cloudflare.com/pages/ |

---

*本文档由 dev-deploy (deployer) 生成*
*更新时间: 2026-05-23*
*任务ID: 5fc6593c*
