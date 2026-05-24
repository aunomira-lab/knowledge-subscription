# 知识付费订阅：MVP 规格与 7 天交付计划

**Project ID**: knowledge-subscription
**Task ID**: cf4702da
**类型**: research
**状态**: 市场门禁 GO (79/100)，已有可运行代码
**日期**: 2026-05-24
**MVP 上线目标**: 2026-05-31 (7 天)

---

## 1. MVP 定义

MVP = **一个已部署到公网、可立即收款的付费内容订阅产品**，包含：
- 1 个已部署的销售页（site/index.html -> Cloudflare Pages）
- 1 个已开通的支付渠道（小报童/爱发电）
- 1 份已发布的免费试看内容（reports/sample_pack/free_preview_v3.md）
- 1 套可运行的内容生成脚本（app/sample_pack_generator.py）
- 7 天内容缓冲（已生成：reports/sample_pack/week1_samples/）
- 至少 3 个社交媒体渠道启动引流

### 已完成资产清单

| 组件 | 路径 | 验证结果 | 状态 |
|------|------|----------|------|
| 销售页 HTML | `/site/index.html` | 31KB+, 含OG标签/限时福利/定价表 | 已完成 |
| 内容生成器 | `/app/sample_pack_generator.py` | 可运行，生成数据文件 | 已验证 |
| 订阅管理模块 | `/app/subscription.py` | pytest 107 passed | 已验证 |
| 免费试看版 | `/reports/sample_pack/free_preview_v3.md` | 3个机会节选+付费对比表 | 已生成 |
| 首周7天内容 | `/reports/sample_pack/week1_samples/` | 7份日报(Mon-Sun) | 已生成 |
| 专业版目录 | `/reports/sample_pack/premium_catalog_v3.md` | 完整栏目体系 | 已生成 |
| 部署脚本 | `/deploy/deploy.sh` | 支持production/staging | 已就绪 |
| Cron脚本 | `/deploy/cron-deploy.sh` | 定时部署模板 | 已就绪 |

### 待完成（阻塞项）

| 组件 | 阻塞原因 | 解决路径 |
|------|----------|----------|
| 公开 URL | 无 Cloudflare 账号 | 用户注册 + 创建 API Token |
| 收款功能 | 无小报童/爱发电/Stripe账号 | 用户注册小报童，配置专栏价格 |
| 联系信息 | 销售页为占位符 | 用户替换微信/邮箱/支付链接 |

---

## 2. MVP 栏目体系

### 栏目 A：每日「AI赚钱机会简报」（核心付费产品）
- **频率**: 每日1-2期（早鸟版1期/天，专业版2-3期/天）
- **格式**: 机会标题 -> 分类 -> 难度 -> 启动时间 -> 收益测算 -> 执行SOP -> 数据来源 -> 风险提醒
- **长度**: 3-5分钟阅读，800-1,500字/期
- **资产**: 每个机会附带可直接复制的Prompt、工具链接、收益计算公式
- **付费墙**: 免费层每周1期节选；早鸟版每日完整1期；专业版每日2-3期+脚本

### 栏目 B：「周末复盘」周刊（所有付费用户）
- **频率**: 每周日1期
- **格式**: 本周3个最佳机会深度拆解 + 1个失败案例 + 下周预告
- **长度**: 10分钟阅读，2,000-3,000字

### 栏目 C：代码与模板仓库（专业版专属）
- **位置**: GitHub repo 或 小报童附件
- **内容**: n8n工作流模板、MCP Server源码、自动化脚本、Prompt集合
- **付费墙**: 专业版订阅者获得下载链接

### 已生成内容样例

| # | 标题 | 文件路径 | 变现潜力 |
|---|------|----------|----------|
| 1 | MCP Server 电商数据查询服务 | `week1_samples/monday_v2.md` | 高（可执行） |
| 2 | n8n自动化工作流模板商店 | `week1_samples/tuesday_v2.md` | 高（可执行） |
| 3 | 小红书AI时尚穿搭账号矩阵 | `week1_samples/wednesday_v2.md` | 高（可执行） |
| 4 | AI短剧批量生成+分发 | `week1_samples/thursday_v2.md` | 中（需资源） |
| 5 | Temu半托管模式套利 | `week1_samples/friday_v2.md` | 中（需资金） |
| 6 | 本周新出AI工具测评 | `week1_samples/saturday_v2.md` | 中（信息差） |
| 7 | 真实跑通案例拆解 | `week1_samples/sunday_v2.md` | 高（信任建立） |

---

## 3. 7 天交付计划（精确到小时级产出）

### Day 1 — 部署上线（销售页公网可访问）

- [ ] **09:00-10:00**: 用户注册 Cloudflare 账号（https://dash.cloudflare.com/sign-up）
- [ ] **10:00-10:30**: 创建 Custom API Token（Account > Cloudflare Pages > Edit）
- [ ] **10:30-11:00**: 执行部署：
  ```bash
  export CLOUDFLARE_API_TOKEN="你的Token"
  cd /home/AgentAdmin/.hermes/shared/dev-team/projects/knowledge-subscription
  ./deploy/deploy.sh production
  ```
- [ ] **11:00-11:30**: 验证部署：
  ```bash
  curl -s -o /dev/null -w "%{http_code}" https://ai-opportunity-radar.pages.dev
  # 期望返回 200
  ```
- [ ] **11:30-12:00**: 将公开 URL 写入 `reports/deployment_verification.md`
- **交付物**: 可公开访问的销售页 URL
- **阻塞检查**: 如 Cloudflare 注册需手机验证，记录到 `/docs/deployment_blockers.md`

### Day 2 — 支付渠道开通（可收款）

- [ ] **09:00-10:00**: 注册小报童（https://xiaobot.net），微信扫码登录
- [ ] **10:00-10:30**: 创建专栏：
  - 名称：AI赚钱机会雷达
  - 简介：每天发现一个可执行的AI变现机会
  - 价格：早鸟版 ¥29/月，专业版 ¥99/月
- [ ] **10:30-11:00**: 发布第一篇内容：
  ```bash
  cat /home/AgentAdmin/.hermes/shared/dev-team/projects/knowledge-subscription/reports/sample_pack/free_preview_v3.md
  # 复制内容到小报童编辑器
  ```
- [ ] **11:00-11:30**: 替换销售页占位符：
  ```bash
  # 编辑 site/index.html，将 "xiaobot.net/p/PLACEHOLDER" 替换为真实链接
  ```
- [ ] **11:30-12:00**: 重新部署 `./deploy/deploy.sh production`
- [ ] **14:00-15:00**: 测试端到端付费流程：销售页点击 -> 支付 -> 收到内容
- **交付物**: 小报童专栏URL + 销售页已更新支付链接
- **阻塞检查**: 如微信商户号审核受阻，启用爱发电（https://afdian.net）备用

### Day 3 — 社交媒体引爆（获客启动）

- [ ] **09:00-10:30**: 小红书：制作3条图文笔记
  - 笔记1：「我发现了一个AI副业机会：MCP Server月入$500-3000」
  - 笔记2：「n8n工作流模板商店：3天做出第一个产品」
  - 笔记3：「2026年AI副业做什么？这个雷达每天更新」
- [ ] **10:30-12:00**: 知乎：回答2个问题
  - 「2026年AI副业做什么能赚钱？」
  - 「普通人如何用AI月入过万？」
- [ ] **14:00-15:00**: 即刻：发布动态 + 加入相关圈子
  - 动态：「我做了个AI赚钱机会雷达，每天更新一个可执行机会」
- **交付物**: 3条小红书笔记URL + 2条知乎回答URL + 即刻动态截图

### Day 4 — 内容引擎启动（可持续生产）

- [ ] **09:00-09:30**: 运行内容生成器：
  ```bash
  cd /home/AgentAdmin/.hermes/shared/dev-team/projects/knowledge-subscription
  python3 app/sample_pack_generator.py
  ```
- [ ] **09:30-11:30**: 人工审核生成的7天内容：
  - 检查收益测算是否过于乐观（保守区间）
  - 检查数据来源是否真实（GitHub stars、Reddit讨论量）
  - 检查执行SOP是否具体（工具、命令、Prompt）
  - 检查风险提醒是否完整（合规、封号、竞争）
- [ ] **11:30-12:00**: 将审核后的内容排入发布队列
- [ ] **14:00-15:00**: 公众号发布首篇试看内容（节选版）
- **交付物**: 下周7天内容已审核并排期 + 公众号推文已发布

### Day 5 — 多渠道分发（扩大曝光）

- [ ] **09:00-10:00**: V2EX：发布「Show」帖
  - 标题：「我做了个AI赚钱机会雷达，每天更新一个可执行机会」
- [ ] **10:00-11:00**: 掘金：发布技术文章
  - 标题：「从0到1：我用Python做了一个AI副业机会雷达」
- [ ] **11:00-12:00**: Twitter/X：发布5条 thread
- [ ] **14:00-15:00**: GitHub：创建公开 repo
  - Repo名：ai-opportunity-radar
  - README + 免费试看版 + 销售页链接
- **交付物**: V2EX帖URL + 掘金文章URL + Twitter thread链接 + GitHub repo URL

### Day 6 — 转化优化（提升付费率）

- [ ] **09:00-10:00**: 检查销售页数据（Cloudflare Analytics）
- [ ] **10:00-11:00**: 给已注册免费用户发推送：创始会员¥199/年限时锁定
- [ ] **11:00-12:00**: 在社交媒体回复所有评论和私信，建立信任
- [ ] **14:00-15:00**: 销售页A/B测试
  - A版标题：「每天发现一个AI赚钱机会」
  - B版标题：「AI副业实战情报」
- **交付物**: 用户互动记录 + 转化优化调整清单

### Day 7 — 数据复盘（决定下周方向）

- [ ] **09:00-10:00**: 汇总7天数据：
  ```bash
  vim /home/AgentAdmin/.hermes/shared/dev-team/projects/knowledge-subscription/metrics/launch_channels.csv
  ```
- [ ] **10:00-11:00**: 填写各渠道数据：曝光、点击、免费订阅、付费订阅、收入
- [ ] **11:00-12:00**: 决策：哪个渠道流量最大？哪个转化最高？哪个ROI为0？
- [ ] **14:00-15:00**: 更新 `docs/strategy.md` 和 `docs/mvp_spec.md`
- **交付物**: 7天数据汇总表 + 下周执行计划

---

## 4. 技术栈

| 层级 | 工具 | 成本 | 状态 | 验证命令 |
|------|------|------|------|----------|
| 销售页 | 静态 HTML/CSS | ¥0 | 已就绪 | `python3 -m http.server 8080 --directory site` |
| 部署平台 | Cloudflare Pages | ¥0 | 待配置 | `./deploy/deploy.sh production` |
| 中文支付 | 小报童 | 平台抽成5-10% | 待注册 | 访问 https://xiaobot.net |
| 备用支付 | 爱发电 | 平台抽成6% | 待注册 | 访问 https://afdian.net |
| 域名 | Cloudflare/Namecheap | ~$12/年 | 可选 | 建议上线后1周内配置 |
| 内容生成 | Python 脚本 | ¥0 | 已就绪 | `python3 app/sample_pack_generator.py` |
| 代码仓库 | GitHub public | ¥0 | 待创建 | `gh repo create ai-opportunity-radar --public` |
| 分析 | Cloudflare Analytics | ¥0 | 内置 | 部署后自动可用 |
| 邮件列表 | 小报童内置 | ¥0 | 待配置 | 小报童后台导出 |

---

## 5. 质量门禁（每期必查）

### 内容 Checklist
- [ ] 机会标题明确：做什么、赚多少
- [ ] 难度星级1-5，匹配目标用户能力
- [ ] 启动时间具体：3天/1周/2周
- [ ] 收益测算保守（用区间而非固定值）
- [ ] 执行SOP具体到工具、命令、Prompt
- [ ] 数据来源可追溯（GitHub/Reddit/平台截图）
- [ ] 风险提醒完整（合规、封号、竞争）
- [ ] 通过无废话审查（见 `/docs/anti_ai_slop_checklist.md`）

### 技术 Checklist
- [ ] 销售页在手机端正常渲染
- [ ] 支付链接可点击、可完成支付
- [ ] 小报童内容排版正常（图片、代码块、链接）
- [ ] sample_pack_generator.py 运行无报错
- [ ] pytest 全部通过

### 上线验收标准
- [ ] 销售页公开 URL 可访问（curl 返回200）
- [ ] 小报童专栏已创建，至少1篇内容已发布
- [ ] 销售页支付链接已替换为真实链接
- [ ] 至少3个社交媒体渠道已启动
- [ ] 7天内 30+ 免费订阅 或 1+ 付费订阅
- [ ] GitHub repo 已创建（用于SEO引流）
- [ ] `reports/deployment_verification.md` 已更新为 LIVE 状态

---

## 6. 预算

### 一次性成本

| 项目 | 成本 | 状态 |
|------|------|------|
| 域名（可选） | $12/年 | 未购买 |
| Logo（Canva自制） | ¥0 | 未制作 |
| **合计** | **$0-12** | |

### 月度成本

| 项目 | 成本 | 状态 |
|------|------|------|
| 域名摊销 | ~$1 | 未购买 |
| 托管（Cloudflare Pages） | ¥0 | 未部署 |
| 分析（Cloudflare Analytics） | ¥0 | 未部署 |
| 小报童平台费 | 有收入才扣 | 未注册 |
| **固定合计** | **$1** | |

### 盈亏平衡

| 月份 | 需付费订阅 | MRR | 覆盖固定成本？ |
|------|-----------|-----|---------------|
| M1 | 1 | ¥29 | 是 |
| M3 | 2 | ¥58 | 是 |
| M6 | 5 | ¥145 | 是 + 内容成本缓冲 |

---

## 7. MVP 后 30 天验证计划

| 周次 | 动作 | 成功指标 |
|------|------|----------|
| Week 2 | 发布 Issue #8-14；启用付费墙；给免费列表发创始会员 offer | 10 付费订阅 |
| Week 3 | 为付费会员开微信群/Discord；收集反馈 | 5 活跃付费成员 |
| Week 4 | 首次与其他newsletter/博主互推；第二次多平台发帖 | 200 免费订阅；20 付费 |
| Week 5-6 | A/B测试定价页；推出模板商店 | 模板销售 3 单 |

**30 天底线**: 如果 Day 30 时 <100 免费订阅 或 <5 付费订阅：
- Pivot A: 降低价格到 ¥9.9/月
- Pivot B: 从"日报"改为"周报"
- Pivot C: 转为 AI Architecture Weekly 海外方向

---

## 8. 产出文件索引

| 文件 | 路径 | 说明 |
|------|------|------|
| 商业策略 | `/docs/strategy.md` | 用户画像、定价、渠道、盈利预测 |
| MVP 规格 | `/docs/mvp_spec.md` | 本文件：栏目、7天计划、技术栈 |
| 销售页 | `/site/index.html` | 31KB+ 静态HTML |
| 免费试看版 | `/reports/sample_pack/free_preview_v3.md` | 3个机会节选+付费对比表 |
| 首周7天内容 | `/reports/sample_pack/week1_samples/` | 7份日报(Mon-Sun) |
| 专业版目录 | `/reports/sample_pack/premium_catalog_v3.md` | 完整栏目体系 |
| 内容生成器 | `/app/sample_pack_generator.py` | 可运行Python脚本 |
| 订阅管理 | `/app/subscription.py` | 可运行Python模块 |
| 部署脚本 | `/deploy/deploy.sh` | Cloudflare Pages 部署 |
| Cron脚本 | `/deploy/cron-deploy.sh` | 定时部署模板 |
| 质量清单 | `/docs/anti_ai_slop_checklist.md` | 内容质量门禁 |
| 部署阻塞清单 | `/docs/deployment_blockers.md` | 待用户授权/外部依赖 |
| 部署验证报告 | `/reports/deployment_verification.md` | 待更新为LIVE |

---

**MVP 状态**: 核心代码和内容已就绪，等待用户完成Cloudflare/小报童注册后即可上线
**目标上线**: 2026-05-31
**当前阶段**: Day 0（等待部署授权）
**下一步赚钱动作**: 见 strategy.md "立即赚钱动作"
