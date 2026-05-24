# knowledge-subscription 部署指南

**项目**: AI Opportunity Radar / 知识付费订阅
**项目ID**: knowledge-subscription
**任务ID**: 44b0dcd0
**部署平台**: GitHub Pages（已上线）
**当前状态**: LIVE — 销售页已公开访问
**公开 URL**: https://aunomira-lab.github.io/knowledge-subscription/
**更新日期**: 2026-05-24
**负责人**: dev-deploy (deployer)

---

## 一、部署平台选择

| 平台 | 国内速度 | HTTPS | 自定义域名 | 后端支持 | 费用 | 状态 |
|------|----------|-------|-----------|---------|------|------|
| **GitHub Pages** | 一般 | 自动 | 支持 | 无 | 免费 | **已上线** |
| **Cloudflare Pages** | 快 | 自动 | 免费支持 | Workers/KV | 免费 | 备选（需 API Token） |
| **Vercel** | 一般 | 自动 | 免费支持 | Serverless | 免费 | 备选 |

**当前选择**: GitHub Pages。
- 优点: 无需额外账号授权（GitHub 已认证），零成本，自动 HTTPS
- 缺点: 国内访问速度一般，无后端支持（可用 GitHub Actions 补充）
- 后续可迁移至 Cloudflare Pages 提升国内速度

---

## 二、用户账号授权步骤（已完成/待完成）

### 2.1 GitHub Pages 部署授权（已完成）

| 字段 | 状态 | 说明 |
|------|------|------|
| GitHub 账号 | 已认证 | aunomira-lab |
| 仓库创建 | 已完成 | https://github.com/aunomira-lab/knowledge-subscription |
| GitHub Pages 启用 | 已完成 | 从 gh-pages 分支部署 |
| 公开 URL 生成 | 已完成 | https://aunomira-lab.github.io/knowledge-subscription/ |

### 2.2 支付渠道账号（收款用，BLOCKED_BY_USER）

| 渠道 | 注册地址 | 要求 | 费率 | 当前状态 |
|------|----------|------|------|----------|
| **小报童** | https://xiaobot.net | 微信个人号即可 | 5-10% | **未注册** |
| **爱发电** | https://afdian.net | 手机号即可 | 6% | **未注册** |
| **Stripe** | https://stripe.com | 海外银行卡/公司 | 2.9%+$0.30 | **未注册** |

> 第一阶段建议：先开小报童专栏，0 成本启动，有收入后再升级正式支付。

### 2.3 联系信息填充（销售页必填，BLOCKED_BY_USER）

编辑 `site/index.html`，搜索以下占位符并替换为真实信息：

| 占位符 | 替换为 | 位置 |
|--------|--------|------|
| `AI-Radar-2026` | 你的真实微信号 | 页脚联系区 |
| `contact@ai-radar.dev` | 你的真实邮箱 | 页脚联系区 + mailto 链接 |
| `https://xiaobot.net` | 你的小报童专栏链接 | 支付区 #pay |
| `https://afdian.net` | 你的爱发电主页链接 | 支付区 #pay |
| `https://stripe.com` | 你的 Stripe 收款链接 | 支付区 #pay |

---

## 三、可执行部署/定时脚本

### 3.1 一键部署脚本

文件: `deploy/deploy.sh`（Cloudflare Pages 方案）

使用方法:

```bash
cd /home/AgentAdmin/.hermes/shared/dev-team/projects/knowledge-subscription
chmod +x deploy/deploy.sh
./deploy/deploy.sh production
```

### 3.2 GitHub Pages 自动部署脚本（已配置）

GitHub Actions workflow 文件: `.github/workflows/deploy.yml`

行为:
1. 每次 push 到 main 分支时自动触发
2. 上传 `site/` 目录为 artifact
3. 部署到 GitHub Pages
4. 公开 URL: https://aunomira-lab.github.io/knowledge-subscription/

**手动触发**:
```bash
gh workflow run deploy.yml --repo aunomira-lab/knowledge-subscription
```

### 3.3 定时自动部署脚本（内容更新后自动重新部署）

文件: `deploy/cron-deploy.sh`

```bash
#!/bin/bash
# deploy/cron-deploy.sh
# 用途: 每日自动检查内容更新，如有更新则重新部署销售页
# 建议配合 crontab 每日 08:00 执行

set -euo pipefail
PROJECT_DIR="/home/AgentAdmin/.hermes/shared/dev-team/projects/knowledge-subscription"
BUILD_DIR="$PROJECT_DIR/site"
LAST_DEPLOY_FILE="$PROJECT_DIR/.last_deploy_hash"
LOG_FILE="/tmp/cron-deploy.log"

# 计算当前内容哈希（包含 HTML、CSS、JS）
CURRENT_HASH=$(find site -type f | sort | xargs md5sum | md5sum | awk '{print $1}')

# 如果存在上次哈希且相同，则跳过
if [ -f "$LAST_DEPLOY_FILE" ] && [ "$CURRENT_HASH" == "$(cat $LAST_DEPLOY_FILE)" ]; then
    echo "[$(date)] 内容未变更，跳过部署"
    exit 0
fi

# 重新推送触发 GitHub Actions 部署
cd "$PROJECT_DIR"
git add site/
git commit -m "Auto-deploy: update sales page $(date '+%Y-%m-%d %H:%M')" || true
git push origin main

# 记录哈希
echo "$CURRENT_HASH" > "$LAST_DEPLOY_FILE"

echo "[$(date)] 自动部署触发完成"
```

**赋予权限并加入 crontab**:

```bash
chmod +x deploy/cron-deploy.sh

# 编辑 crontab
crontab -e

# 添加以下行（每天早8点自动检查并部署）
0 8 * * * /home/AgentAdmin/.hermes/shared/dev-team/projects/knowledge-subscription/deploy/cron-deploy.sh >> /tmp/cron-deploy.log 2>&1

# 查看 crontab 是否添加成功
crontab -l | grep cron-deploy
```

---

## 四、公开 URL 回填位置

部署成功后，公开 URL 为: `https://aunomira-lab.github.io/knowledge-subscription/`

已回填到以下文件:

| 文件 | 回填内容 | 状态 |
|------|---------|------|
| `site/index.html` | OG url、页脚链接 | 已回填 |
| `reports/deployment_verification.md` | 验证结果 + 公开 URL | 已更新 |
| `docs/launch_execution_plan.md` | 获客计划中的网站地址 | 已回填 |
| `metrics/launch_channels.csv` | 渠道跟踪参数（UTM） | 已回填 |
| `deploy/README.md` | 部署说明中的 URL | 已回填 |

---

## 五、收款/联系入口配置

### 5.1 当前销售页入口状态

| 入口 | 类型 | 状态 | 说明 |
|------|------|------|------|
| 早鸟版 CTA | 按钮 | 占位 | 点击弹出模态框提示"支付渠道配置中" |
| 专业版 CTA | 按钮 | 占位 | 同上 |
| 定制版 CTA | 按钮 | 跳转至表单 | 可直接使用 |
| 联系表单 | mailto | 可用 | 用户提交后打开邮件客户端发送申请 |
| 支付链接 | 外部链接 | 占位 | 指向 xiaobot.net / afdian.net / stripe.com 首页，需替换为具体收款页 |

### 5.2 最小可用收款方案（无需后端，1 小时上线）

**方案 A: 纯 mailto 方案（当前已启用）**
- 用户点击"提交订阅申请" -> 打开邮件客户端 -> 发送预填邮件
- 优点: 零成本、零配置、立即可用
- 缺点: 需要用户有邮件客户端

**方案 B: 小报童直接收款（目标状态）**
1. 注册小报童 -> 创建专栏 -> 设置价格（¥29/月）
2. 获取专栏链接: `https://xiaobot.net/p/xxx`
3. 替换 site/index.html 中占位链接
4. 用户点击"立即订阅" -> 直接跳转 -> 微信支付 -> 完成

---

## 六、宣传平台与获客渠道（>=3个平台）

已规划 6 个核心宣传平台，覆盖中文和海外流量：

| 优先级 | 平台 | 获客成本 | 预期日流量 | 转化率预估 | 内容形式 | 启动日期 | 状态 |
|--------|------|----------|-----------|-----------|----------|----------|------|
| **P0** | **知乎** | ¥0-10 | 100-300 | 2% | 深度回答+专栏 | Day 1 | 待启动 |
| **P0** | **小红书** | ¥0-5 | 200-500 | 1.5% | 图文笔记+短视频 | Day 1 | 待启动 |
| **P0** | **即刻** | ¥0 | 50-150 | 3% | 动态+圈子+AMA | Day 1 | 待启动 |
| **P1** | **Twitter/X** | ¥0-20 | 50-200 | 2% | Thread+互动 | Day 2 | 待启动 |
| **P1** | **V2EX** | ¥0 | 30-100 | 5% | 项目分享 | Day 2 | 待启动 |
| **P1** | **微信社群** | ¥0 | 20-50 | 5% | 价值输出 | Day 2 | 待启动 |

详细获客策略、每日执行计划、风险预案见 `docs/launch_execution_plan.md`。
渠道 UTM 追踪链接见 `metrics/launch_channels.csv`。

---

## 七、7天获客执行计划

已制定完整的 7 天获客执行计划，包含：
- Day 1: 部署日 + 内容基建（知乎/小红书/即刻账号准备）
- Day 2: 内容爆发（多平台同步发布）
- Day 3: 社群深耕 + 技术博客
- Day 4: 广告投放准备 + A/B 测试
- Day 5: 付费推广启动（小红书薯条）
- Day 6: 裂变增长（推荐奖励 + AMA）
- Day 7: 复盘与放大（数据复盘 + 下周计划）

完整计划见 `docs/launch_execution_plan.md`。

---

## 八、广告投放前置条件

### 8.1 必须准备清单

| 条件 | 状态 | 说明 | 责任人 | 截止日 |
|------|------|------|--------|--------|
| 公开可访问的网站 | **已完成** | GitHub Pages 已上线，HTTPS 就绪 | dev-deploy | Day 0 |
| 支付通道 | BLOCKED_BY_USER | 小报童专栏链接待创建 | 用户 | Day 1 |
| 转化追踪 | 建议配置 | Google Analytics 或百度统计 | dev-monitor | Day 2 |
| 广告素材 | 模板已就绪 | 3-5 套图文素材（小红书 3:4） | dev-deploy | Day 4 |
| 日预算 | 已确定 | ¥50-100/天测试 | dev-deploy | — |
| 测试资金 | 已确定 | ¥200 启动资金 | dev-deploy | — |

### 8.2 平台开户要求

**小红书薯条**:
- 个人号即可投放
- 最低充值 ¥100
- 审核时间：即时
- 适合测试素材效果

**知乎知+**:
- 个人/企业账号均可
- 需要实名认证
- 最低充值 ¥1000
- 适合加热已有爆款回答

**Twitter Ads**:
- 需要海外支付方式（Visa/Mastercard）
- 最低充值 $50
- 适合海外市场测试

---

## 九、验证命令（部署前/后必须执行）

### 9.1 部署前验证

```bash
cd /home/AgentAdmin/.hermes/shared/dev-team/projects/knowledge-subscription

# 1. 检查销售页存在且大小合理
ls -lh site/index.html
# 期望: 文件存在，大小 > 15KB

# 2. 检查 HTML 结构完整性
python3 -c "
from html.parser import HTMLParser
class Validator(HTMLParser):
    def error(self, message): raise Exception(message)
with open('site/index.html', 'r') as f:
    Validator().feed(f.read())
print('HTML 语法检查通过')
"

# 3. 检查关键内容是否存在
grep -q '¥29' site/index.html && echo '定价存在: 通过'
grep -q 'handleSubmit' site/index.html && echo '表单逻辑存在: 通过'
grep -q 'viewport' site/index.html && echo '响应式存在: 通过'
grep -q 'mailto' site/index.html && echo '联系入口存在: 通过'

# 4. 检查部署脚本语法
bash -n deploy/deploy.sh && echo '部署脚本语法: 通过'
bash -n deploy/cron-deploy.sh && echo '定时脚本语法: 通过'

# 5. 检查脚本权限
[ -x deploy/deploy.sh ] && echo 'deploy.sh 可执行: 通过'
[ -x deploy/cron-deploy.sh ] && echo 'cron-deploy.sh 可执行: 通过'

# 6. 本地预览
python3 -m http.server 8080 --directory site &
# 打开浏览器访问 http://localhost:8080
```

### 9.2 部署后验证（已执行，结果见 reports/deploy_verify_44b0dcd0.txt）

```bash
URL="https://aunomira-lab.github.io/knowledge-subscription/"

# 1. HTTP 200 检查
curl -s -o /dev/null -w "%{http_code}\n" "$URL"
# 期望: 200

# 2. 关键内容检查
curl -s "$URL" | grep -o 'AI Opportunity Radar' | head -1
curl -s "$URL" | grep -o '¥29' | head -1
curl -s "$URL" | grep -o 'handleSubmit' | head -1

# 3. 移动端 viewport 检查
curl -s "$URL" | grep -q 'viewport' && echo '移动端适配: 通过'

# 4. 响应头检查（确认 HTTPS + GitHub Pages）
curl -I "$URL" 2>/dev/null | grep -E '(HTTP/2|GitHub)'

# 5. 端到端转化测试
URL_WITH_UTM="${URL}?utm_source=zhihu&utm_medium=answer&utm_campaign=launch"
curl -s "$URL_WITH_UTM" | grep -q 'AI Opportunity Radar' && echo 'UTM 链接落地正常: 通过'

# 6. 表单字段存在性检查
curl -s "$URL" | grep -o '<input' | wc -l
# 期望: >= 3 个输入字段
```

---

## 十、当前部署状态

| 检查项 | 状态 | 说明 |
|--------|------|------|
| 销售页 HTML | 已上线 | site/index.html (31KB+)，含定价/表单/FAQ/CTA/OG标签/响应式 |
| 部署脚本 | 就绪 | deploy/deploy.sh (Cloudflare 方案) |
| GitHub Actions 部署 | 已上线 | `.github/workflows/deploy.yml` 自动触发 |
| 定时脚本 | 就绪 | deploy/cron-deploy.sh，待加入 crontab |
| GitHub Pages 域名 | 已生成 | https://aunomira-lab.github.io/knowledge-subscription/ |
| 公开 URL 验证 | 通过 | HTTP 200，所有关键内容存在 |
| 支付渠道 | BLOCKED_BY_USER | 需用户注册小报童/爱发电并替换链接 |
| 联系信息 | 占位符 | 微信/邮箱为占位，需替换为真实信息 |
| 自定义域名 | 可选 | 建议后续购买 .com/.cn 域名 |
| 部署验证报告 | 已更新 | 见 reports/deployment_verification.md |
| 获客计划 | 已就绪 | 见 docs/launch_execution_plan.md |
| 渠道清单 | 已就绪 | 见 metrics/launch_channels.csv |

---

## 十一、快速上线 checklist（用户侧 — 剩余 BLOCKED 项）

用户按以下步骤操作，预计 20 分钟可完成剩余配置：

```
Step 1 (10min): 注册小报童专栏（至少一个支付渠道）
   -> https://xiaobot.net -> 创建专栏 -> 定价 ¥29/月

Step 2 (5min):  替换销售页占位信息（微信/邮箱/支付链接）
   -> 编辑 site/index.html: 搜索 "占位" 并替换
   -> 或运行: sed -i 's/AI-Radar-2026/你的微信号/g' site/index.html

Step 3 (3min):  提交更改并自动重新部署
   -> git add site/index.html && git commit -m "Update contact info"
   -> git push origin main（触发 GitHub Actions 自动部署）

Step 4 (2min):  验证部署
   -> curl 检查 + 浏览器访问 + 手机端检查
```

---

## 十二、故障排除

| 问题 | 原因 | 解决方案 |
|------|------|----------|
| 网站 404 | gh-pages 分支未生成或构建中 | 等待 1-2 分钟，或检查 GitHub Actions 状态 |
| 样式不生效 | GitHub Pages CDN 缓存 | 强制刷新 (Ctrl+Shift+R) 或加 `?v=2` |
| 支付链接无效 | 未替换占位链接 | 编辑 site/index.html 替换为小报童真实链接 |
| 邮件无法发送 | 用户无邮件客户端 | 改用微信/表单联系 |
| 国内访问慢 | GitHub Pages 服务器在海外 | 后续可迁移至 Cloudflare Pages |

---

**结论**: 销售页已上线并可公开访问。剩余 BLOCKED_BY_USER 项：支付渠道配置、联系信息替换。用户完成替换后，提交代码即可自动重新部署。
