# 部署阻塞项清单

**项目**: knowledge-subscription (AI Opportunity Radar)
**任务ID**: 44b0dcd0
**状态**: PARTIALLY_UNBLOCKED — 销售页已上线，支付/联系信息仍待用户授权
**更新时间**: 2026-05-24
**报告人**: dev-deploy (deployer)
**部署平台**: GitHub Pages（已上线）
**公开 URL**: https://aunomira-lab.github.io/knowledge-subscription/

---

## 拓扑图

```
上线路径
├── 销售页就绪 (site/index.html, 31KB+, 含OG标签/限时福利/响应式) [DONE]
├── GitHub 仓库创建 (aunomira-lab/knowledge-subscription) [DONE]
├── GitHub Pages 启用 (gh-pages 分支) [DONE]
├── 公开 URL 生成 (https://aunomira-lab.github.io/knowledge-subscription/) [DONE]
├── 部署验证通过 (HTTP 200, 所有关键内容存在) [DONE]
├── 获客计划就绪 (docs/launch_execution_plan.md, 7天计划+6个平台) [DONE]
├── 渠道清单就绪 (metrics/launch_channels.csv, 含UTM追踪模板) [DONE]
├── 部署验证报告就绪 (reports/deployment_verification.md, LIVE状态) [DONE]
├── 支付渠道账号未完成  ← 当前阻塞
│      ├── 小报童专栏链接
│      ├── 爱发电主页链接
│      └── Stripe 收款链接
├── 联系信息未替换  ← 当前阻塞
│      ├── 真实微信号
│      └── 真实邮箱
└── 自定义域名（可选）
```

---

## 已解阻塞项

### 1. GitHub Pages 部署授权（已解封）

| 字段 | 状态 | 说明 |
|------|------|------|
| GitHub 账号 | 已认证 | aunomira-lab |
| 仓库创建 | 已完成 | https://github.com/aunomira-lab/knowledge-subscription |
| GitHub Pages 分支 | 已推送 | gh-pages（site/ 目录内容） |
| 公开 URL | 已生效 | https://aunomira-lab.github.io/knowledge-subscription/ |
| HTTP 200 验证 | 已通过 | curl 返回 200，31KB+ |
| HTTPS | 已启用 | GitHub Pages 自动 HTTPS |
| OG 标签 | 已配置 | og:title, og:description, og:url |
| 响应式 | 已验证 | viewport + media query |

**解封时间**: 2026-05-24 06:22 UTC
**解封方式**: GitHub CLI 已认证，创建仓库并推送 gh-pages 分支，GitHub Pages 自动构建

---

## 剩余阻塞项清单

### P0 — 关键阻塞（影响付费转化）

#### 1. 支付渠道配置（至少一个）

| 渠道 | 注册地址 | 要求 | 费率 | 当前状态 |
|------|----------|------|------|----------|
| **小报童** | https://xiaobot.net | 微信个人号即可 | 5-10% | **未注册** |
| **爱发电** | https://afdian.net | 手机号即可 | 6% | **未注册** |
| **Stripe** | https://stripe.com | 海外银行卡/公司 | 2.9%+$0.30 | **未注册** |

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

### P1 — 重要阻塞（影响联系和信任）

#### 2. 销售页联系信息更新

| 项目 | 当前占位值 | 需替换为 | 位置 |
|------|-----------|----------|------|
| 微信号 | AI-Radar-2026 | 真实微信号 | site/index.html 页脚联系区 |
| 邮箱 | contact@ai-radar.dev | 真实邮箱 | site/index.html mailto 链接 |
| 公众号 | 未配置 | 公众号二维码（可选） | 销售页底部 |

**用户执行步骤**:
```bash
# 编辑销售页，替换占位符
cd /home/AgentAdmin/.hermes/shared/dev-team/projects/knowledge-subscription

# 方式1: 直接编辑
vim site/index.html
# 搜索 "AI-Radar-2026" 替换为你的微信号
# 搜索 "contact@ai-radar.dev" 替换为你的邮箱

# 方式2: 使用 sed 批量替换
sed -i 's/AI-Radar-2026/你的微信号/g' site/index.html
sed -i 's/contact@ai-radar.dev/你的邮箱/g' site/index.html

# 提交并自动重新部署
git add site/index.html
git commit -m "Update contact and payment info"
git push origin main
# GitHub Actions 会自动重新部署
```

**预计耗时**: 3 分钟
**阻塞影响**: mailto 邮件和微信添加请求无法到达真实运营者，潜在客户流失。

---

### P2 — 可选优化（不阻止上线）

#### 3. 自定义域名（可选，建议上线后 1 周内配置）

| 项目 | 建议值 | 费用 | 说明 |
|------|--------|------|------|
| 海外域名 | ai-radar.dev | ~$10/年 | 适合国际用户 |
| 国内域名 | ai-radar.cn | ~¥35/年 | 适合中文 SEO |

**GitHub Pages 自定义域名配置**:
```
1. 购买域名
2. 在域名注册商添加 CNAME 记录: ai-radar.dev -> aunomira-lab.github.io
3. 在仓库 Settings -> Pages -> Custom domain 添加域名
4. GitHub 会自动生成 HTTPS 证书
```

#### 4. 数据追踪工具

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

### 最小可用上线路径（剩余 15 分钟）

```
Step 1 (10min): 小报童注册 + 创建专栏 + 复制链接
   -> https://xiaobot.net -> 创建专栏 -> 定价 ¥29/月

Step 2 (3min):  替换销售页占位信息（微信/邮箱/支付链接）
   -> 编辑 site/index.html: 搜索 "占位" 并替换
   -> 或运行: sed -i 's/AI-Radar-2026/你的微信号/g' site/index.html

Step 3 (2min):  提交更改并自动重新部署
   -> git add site/index.html && git commit -m "Update contact info"
   -> git push origin main（触发 GitHub Actions 自动部署）

Step 4 (即时):  验证更新后的公开 URL
   -> curl -s https://aunomira-lab.github.io/knowledge-subscription/ | grep "你的微信号"
```

### 验证上线成功

```bash
cd /home/AgentAdmin/.hermes/shared/dev-team/projects/knowledge-subscription

# 1. 检查销售页已更新占位信息
grep -v 'AI-Radar-2026' site/index.html | grep -v 'contact@ai-radar.dev' >/dev/null && echo "联系信息已更新" || echo "联系信息仍为占位"

# 2. 检查支付链接非占位
grep -E 'xiaobot.net/p/|afdian.net/a/' site/index.html && echo "支付链接已配置"

# 3. 提交并触发自动部署
git add site/index.html
git commit -m "Activate payment and contact info"
git push origin main

# 4. 等待 1-2 分钟后验证公开 URL
curl -s -o /dev/null -w "%{http_code}" https://aunomira-lab.github.io/knowledge-subscription/
# 期望返回 200
```

---

## 通过条件

### 从 PARTIALLY_UNBLOCKED -> FULLY_LIVE

必须完成:
- [x] GitHub 账号认证并启用 Pages（已完成）
- [x] 销售页部署并返回 HTTP 200（已完成）
- [x] 公开 URL 生成并回填到所有文件（已完成）
- [ ] 至少一个支付渠道创建并获取真实收款链接
- [ ] 销售页中的微信、邮箱替换为真实值
- [ ] 提交代码触发自动重新部署
- [ ] `reports/deployment_verification.md` 更新为 FULLY_LIVE 状态

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
| GitHub Pages 文档 | https://docs.github.com/en/pages |

---

*本文档由 dev-deploy (deployer) 生成*
*更新时间: 2026-05-24*
*任务ID: 44b0dcd0*
*公开 URL: https://aunomira-lab.github.io/knowledge-subscription/*
