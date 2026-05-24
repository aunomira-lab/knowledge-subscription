# Substack 发布运维手册

本文档描述 knowledge-subscription 项目如何通过 social_publisher 框架将内容发布到 Substack。

## 快速开始

### 1. 检查当前状态

```bash
cd /home/AgentAdmin/.hermes/shared/dev-team
python3 scripts/submit_substack_post.py status
```

输出示例（无凭证时）：
```
Substack Publishing Status
============================================================

Platform Configuration:
  Enabled: true
  Adapter: substack
  Auto-publish: false
  Approval required: false

Credential Status:
  Has credentials: false
  Can auto-publish: false
  Can semi-auto: false
  Missing fields: publication_url
  Message: No credentials configured...

Recommendation: Configure credentials for better automation
```

### 2. 配置凭证

编辑 `social_publisher/config.json`，在 `platforms.substack` 下添加：

```json
{
  "platforms": {
    "substack": {
      "adapter": "substack",
      "enabled": true,
      "auto_publish": false,
      "approval_required": false,
      "credentials": {
        "publication_url": "https://yourpublication.substack.com",
        "api_key": "your_api_key_if_available"
      }
    }
  }
}
```

**注意**：Substack 目前没有公开的发布 API，因此 `api_key` 是可选的。当仅有 `publication_url` 时，系统将进入**半自动模式**（浏览器辅助）。

### 3. 提交内容

#### 方式一：命令行直接提交

```bash
python3 scripts/submit_substack_post.py submit \
    --project knowledge-subscription \
    --title "AI商机雷达周报 #1" \
    --body "本期内容要点..." \
    --cta "订阅获取更多AI赚钱机会" \
    --tags AI 副业 独立开发
```

#### 方式二：从 Markdown 文件提交

```bash
python3 scripts/submit_substack_post.py submit \
    --project knowledge-subscription \
    --from-file ./content/newsletter_issue_1.md
```

Markdown 文件格式：
```markdown
---
title: "AI商机雷达周报 #1"
tags: [AI, 副业, 独立开发]
cta: "订阅获取更多AI赚钱机会"
---

# AI商机雷达周报 #1

## 本周精选

本周我们发现...

> 订阅获取更多AI赚钱机会
```

### 4. 发布流程

提交后，系统会根据凭证状态决定发布路径：

#### 路径 A：无凭证 → NEEDS_CREDENTIALS

- 状态：`NEEDS_CREDENTIALS`
- 动作：在 `social_publisher/outbox/substack/` 生成手动发布指南
- 人工操作：按指南复制内容到 Substack 后台发布

#### 路径 B：有 publication_url → READY_MANUAL_PUBLISH

- 状态：`READY_MANUAL_PUBLISH`
- 动作：生成半自动发布脚本
- 人工操作：运行生成的 Python 脚本，浏览器自动打开并预填内容

#### 路径 C：有完整凭证 → READY_AUTO_PUBLISH

- 状态：`READY_AUTO_PUBLISH`
- 动作：尝试自动发布（通过 webhook 或 API）
- 人工操作：确认发布成功

### 5. 标记已发布

手动发布后，需要更新系统状态：

```bash
python3 scripts/submit_substack_post.py mark-published POST_ID \
    --url "https://yourpublication.substack.com/p/ai-radar-weekly-1"
```

获取 POST_ID：
```bash
python3 scripts/submit_substack_post.py list --status READY_MANUAL_PUBLISH
```

## 三种发布模式详解

### 模式 1：NEEDS_CREDENTIALS（纯手动）

**触发条件**：未配置任何凭证

**流程**：
1. 用户提交内容
2. 系统生成 Markdown 指南文件
3. 用户按指南手动复制内容到 Substack
4. 用户运行 `mark-published` 命令更新状态

**适用场景**：首次使用、测试环境、临时发布

**文件位置**：`social_publisher/outbox/substack/YYYYMMDD_HHMMSS_*.md`

### 模式 2：READY_MANUAL_PUBLISH（半自动）

**触发条件**：配置了 `publication_url` 但未配置 API 凭证

**流程**：
1. 用户提交内容
2. 系统生成 Markdown 文件和 Python 脚本
3. 用户运行 Python 脚本：
   ```bash
   python3 social_publisher/outbox/substack/YYYYMMDD_HHMMSS_*_publish.py
   ```
4. 脚本自动打开浏览器并预填内容（需安装 Playwright）
5. 用户审核并点击发布
6. 用户运行 `mark-published` 命令

**自动化程度**：自动打开浏览器、自动复制标题到剪贴板（可选）、自动填充内容（如 Playwright 可用）

**启用全自动化**：
```bash
pip install playwright
playwright install chromium
```

### 模式 3：READY_AUTO_PUBLISH（全自动）

**触发条件**：配置了完整的 API 凭证或 webhook

**流程**：
1. 用户提交内容，添加 `--auto-process` 标志
2. 系统自动调用 API 或 webhook 发布
3. 状态直接变为 `PUBLISHED`

**当前限制**：Substack 目前没有公开的发布 API。此模式需要：
- 自建中转服务接收 webhook
- 或使用第三方 Newsletter 平台（如 Buttondown、ConvertKit）的 API

## 批量处理

### 查看待处理内容

```bash
# 需要凭证的
python3 scripts/submit_substack_post.py list --status NEEDS_CREDENTIALS

# 准备手动发布的
python3 scripts/submit_substack_post.py list --status READY_MANUAL_PUBLISH

# 已批准的
python3 scripts/submit_substack_post.py list --status APPROVED
```

### 批量处理就绪内容

```bash
# 处理所有 READY_MANUAL_PUBLISH 内容
python3 scripts/submit_substack_post.py process-ready

# 仅查看不执行
python3 scripts/submit_substack_post.py process-ready --dry-run
```

## 与 knowledge-subscription 工作流集成

### 从内容包自动生成

在 `scripts/generate_content_pack.py` 中，内容生成后可自动提交：

```python
import subprocess

def publish_to_substack(title: str, body: str, issue_number: int):
    result = subprocess.run([
        'python3', 'scripts/submit_substack_post.py', 'submit',
        '--project', 'knowledge-subscription',
        '--title', title,
        '--body', body,
        '--tags', 'AI', '副业', '独立开发',
    ], capture_output=True, text=True)
    return result.returncode == 0
```

### 定时发布

添加 cronjob 检查并处理就绪内容：

```cron
# 每小时检查一次待发布内容
0 * * * * cd /home/AgentAdmin/.hermes/shared/dev-team && python3 scripts/submit_substack_post.py process-ready >> logs/substack_publish.log 2>&1
```

## 故障排除

### 问题：提交后状态为 NEEDS_CREDENTIALS

**原因**：未配置 publication_url

**解决**：
1. 编辑 `social_publisher/config.json`
2. 添加 `platforms.substack.credentials.publication_url`
3. 重新提交内容，或运行 `process-ready`

### 问题：半自动脚本无法打开浏览器

**原因**：缺少 Playwright 或浏览器驱动

**解决**：
```bash
pip install playwright
playwright install chromium
```

或改用纯手动模式：直接打开 Markdown 文件复制内容。

### 问题：标记已发布时提示 Post not found

**原因**：POST_ID 错误或内容已归档

**解决**：
```bash
# 列出最近的内容
python3 scripts/submit_substack_post.py list --status PUBLISHED

# 在 queue.json 中搜索
grep -r "your-title" social_publisher/queue.json
```

### 问题：内容被标记为需要审核

**原因**：触发了审核策略（如包含敏感词）

**解决**：
```bash
# 跳过审核直接提交
python3 scripts/submit_substack_post.py submit ... --skip-review
```

## 配置参考

### 完整配置示例

```json
{
  "version": 2,
  "mode": "auto_publish_first",
  "auto_publish_enabled": true,
  "platforms": {
    "substack": {
      "adapter": "substack",
      "enabled": true,
      "approval_required": false,
      "auto_publish": false,
      "credentials": {
        "publication_url": "https://ai-radar-newsletter.substack.com",
        "api_key": "",
        "cookie_session": "",
        "csrf_token": "",
        "author_id": ""
      },
      "webhook_url": ""
    }
  },
  "review_policy": {
    "enabled": true,
    "require_review_for_platforms": [],
    "require_review_on_risk_words": true
  },
  "publish_policy": {
    "auto_publish_on_create": false,
    "fallback_to_outbox": true,
    "retry_count": 1,
    "max_posts_per_day_per_platform": 5
  },
  "policy": {
    "forbidden_terms": ["稳赚", "保赚", "暴富", "躺赚", "无风险"],
    "risk_terms": ["保证收益", "稳赚", "躺赚", "无风险", "暴富"]
  }
}
```

### 环境变量支持（未来扩展）

计划支持通过环境变量配置凭证：

```bash
export SUBSTACK_PUBLICATION_URL="https://yourpublication.substack.com"
export SUBSTACK_API_KEY="your_api_key"
```

## 更新日志

- **2025-05-11**: 初始版本，支持三种发布模式（NEEDS_CREDENTIALS、READY_MANUAL_PUBLISH、READY_AUTO_PUBLISH）
- **未来**: 计划支持 Playwright 全自动化、Webhook 集成、环境变量配置

## 相关文件

- `system/social_publisher/substack_adapter.py` - 适配器实现
- `scripts/submit_substack_post.py` - CLI 工具
- `social_publisher/config.json` - 配置文件
- `social_publisher/queue.json` - 发布队列
- `social_publisher/outbox/substack/` - 待发布内容输出目录

## 获取帮助

```bash
# 查看命令帮助
python3 scripts/submit_substack_post.py --help
python3 scripts/submit_substack_post.py submit --help

# 检查系统状态
python3 scripts/submit_substack_post.py status
```
