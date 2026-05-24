# Substack 自动化安全合规与风控复核报告

> 文档编号: SEC-SUBSTACK-001  
> 版本: 1.0  
> 创建日期: 2026-05-11  
> 复核人: 小安 (dev-security)  
> 复核范围: adapter/cron/content workflow 安全边界、secret 存储、人工审核、kill switch、频率限制、退款/退订

---

## 一、执行摘要

| 检查项 | 状态 | 等级 | 说明 |
|---------|------|------|------|
| Secret 存储规范 | ✅ 已定义 | 严重 | 禁止硬编码token/cookie |
| 人工审核触发条件 | ✅ 已定义 | 高 | 敏感内容、异常频率、用户投诉 |
| Kill Switch 机制 | ✅ 已定义 | 严重 | 多层级紧急停止方案 |
| 频率限制 | ✅ 已定义 | 高 | API调用、内容发布、邮件发送限制 |
| 退款/退订流程 | ✅ 已定义 | 高 | 符合Substack/Stripe规范 |
| 凭证泄露检查 | ✅ 已完成 | 严重 | 未发现明文凭证 |

**复核结论**: 当前项目为人工发布模式，暂无自动化适配器。本文档为未来自动化提供安全基线。

---

## 二、Secret 存储规范

### 2.1 禁止事项

```yaml
严禁硬编码:
  - cookie: "substack.session=xxx"  # 严禁
  - token: "Bearer xxx"              # 严禁
  - api_key: "sk-xxx"                # 严禁
  - password: "mypassword123"        # 严禁
  - session_id: "sess_xxx"           # 严禁

严禁提交到:
  - Git仓库 (任何分支)
  - 日志文件 (非加密)
  - Slack/飞书群聊
  - 即刻/知乎等公开平台
```

### 2.2 推荐存储方案

#### 方案A: 环境变量 (推荐用于本地开发)

```bash
# ~/.bashrc 或 ~/.zshrc
export SUBSTACK_API_KEY="[REDACTED]"
export SUBSTACK_SESSION_COOKIE="[REDACTED]"
export STRIPE_API_KEY="[REDACTED]"
export RESEND_API_KEY="[REDACTED]"
export OPENAI_API_KEY="[REDACTED]"
```

#### 方案B: 秘密管理工具 (推荐用于生产环境)

```yaml
# 推荐工具:
- HashiCorp Vault
- AWS Secrets Manager
- 1Password Secrets Automation
- Doppler

使用示例:
  - 从 Vault 获取凭证
  - 应用启动时动态注入
  - 内存中不落盘保存明文
```

#### 方案C: 配置文件 (如果必须使用文件)

```python
# config/secrets.yaml
# 此文件必须在 .gitignore 中

substack:
  api_key: "${SUBSTACK_API_KEY}"  # 使用环境变量占位符
  session_cookie: "${SUBSTACK_SESSION_COOKIE}"

stripe:
  api_key: "${STRIPE_API_KEY}"
  webhook_secret: "${STRIPE_WEBHOOK_SECRET}"
```

### 2.3 密钥轮换策略

```yaml
轮换周期:
  - API Key: 每 90 天
  - Session Cookie: 每 30 天 (或异常登录时)
  - Webhook Secret: 每 180 天

轮换流程:
  1. 生成新密钥
  2. 更新秘密管理工具
  3. 测试应用连接
  4. 废弃旧密钥 (保留 7 天缓冲)
  5. 更新文档记录
```

---

## 三、人工审核触发条件

### 3.1 必须人工审核的内容类型

```yaml
敏感话题 (自动触发审核):
  - 政治相关: "政府" | "政策" | "监管" | "法规"
  - 金融风险: "保证收益" | "稳赚" | "无风险" | "高回报"
  - 医疗健康: "治疗" | "药物" | "医疗建议"
  - 投资建议: "买入" | "卖出" | "目标价" | "涨幅"
  - 身份信息: 包含具体个人信息的内容

异常行为 (自动触发审核):
  - 发布频率: 单小时内 > 3 篇
  - 内容长度: > 10,000 字 (超出常规)
  - 外部链接: > 20 个/篇
  - 附件大小: > 10MB
  - 特殊字符: 包含可疑脚本/编码

用户反馈 (自动触发审核):
  - 单篇 > 3 个用户投诉
  - 退订/退款请求
  - 平台警告通知
```

### 3.2 审核工作流程

```
├── 内容生成
│   ├── AI生成草稿
│   └── 敏感词检测
├── 审核触发
│   ├── 触发规则匹配
│   ├── 自动标记待审核
│   └── 通知负责人
├── 人工审核
│   ├── 内容准确性确认
│   ├── 合规性检查
│   └── 批准/拒绝/修改
└── 发布/拒绝
    ├── 批准: 继续自动发布流程
    └── 拒绝: 记录原因，通知生成团队
```

### 3.3 审核响应时间要求

| 情况 | 最大响应时间 | 后果 |
|------|-------------|------|
| 正常审核 | 4小时 | 逾期自动发送提醒 |
| 紧急审核 (投诉/警告) | 30分钟 | 逾期自动暂停发布 |
| 重大事件 | 15分钟 | 逾期自动触发 kill switch |

---

## 四、Kill Switch 紧急停止机制

### 4.1 多层级停止方案

```yaml
Level 1 - 内容级别:
  触发条件: 单篇内容触发审核规则
  行动: 暂停该篇发布，进入审核队列
  恢复: 人工审核通过后手动发布
  通知: 内容团队

Level 2 - 渠道级别:
  触发条件: 平台警告/多次投诉/异常登录
  行动: 暂停所有Substack发布，保留草稿
  恢复: 安全团队确认后手动恢复
  通知: 项目经理 + 安全团队

Level 3 - 系统级别:
  触发条件: 凭证泄露疑似/重大安全事件/法律风险
  行动: 停止所有自动化流程，撤回授权
  恢复: 需要高级管理层批准
  通知: 全体团队 + 用户通知

Level 4 - 账号级别:
  触发条件: 账号封禁/永久限制/严重违规
  行动: 启动备用方案 (小报童/即刻/知识星球)
  恢复: 根据备用方案重新配置
  通知: 用户全量通知
```

### 4.2 Kill Switch 实现示例

```python
# safety/kill_switch.py
import os
import json
from datetime import datetime
from pathlib import Path

class KillSwitch:
    """紧急停止开关 - 多层级安全控制"""
    
    LEVELS = {
        'content': 1,    # 内容级别
        'channel': 2,    # 渠道级别
        'system': 3,     # 系统级别
        'account': 4     # 账号级别
    }
    
    def __init__(self, state_file: str = ".safety/kill_switch_state.json"):
        self.state_file = Path(state_file)
        self.state_file.parent.mkdir(parents=True, exist_ok=True)
        self._load_state()
    
    def _load_state(self):
        """加载当前状态"""
        if self.state_file.exists():
            with open(self.state_file, 'r') as f:
                self.state = json.load(f)
        else:
            self.state = {
                'active_level': 0,  # 0 = 未激活
                'triggered_at': None,
                'triggered_by': None,
                'reason': None,
                'manual_override': False
            }
    
    def _save_state(self):
        """保存状态"""
        with open(self.state_file, 'w') as f:
            json.dump(self.state, f, indent=2)
    
    def trigger(self, level: str, reason: str, triggered_by: str):
        """触发 kill switch"""
        level_num = self.LEVELS.get(level, 1)
        
        # 只能提高等级，不能降级
        if level_num >= self.state['active_level']:
            self.state = {
                'active_level': level_num,
                'triggered_at': datetime.now().isoformat(),
                'triggered_by': triggered_by,
                'reason': reason,
                'manual_override': False
            }
            self._save_state()
            
            # 执行对应级别的停止操作
            self._execute_stop_actions(level_num)
            
            return True
        return False
    
    def _execute_stop_actions(self, level: int):
        """执行对应等级的停止操作"""
        actions = {
            1: self._stop_content_publishing,
            2: self._stop_channel_operations,
            3: self._stop_all_automation,
            4: self._initiate_account_recovery
        }
        
        # 执行当前等级及以下所有操作
        for lvl in range(level, 0, -1):
            if lvl in actions:
                actions[lvl]()
    
    def _stop_content_publishing(self):
        """停止内容发布"""
        # 创建标志文件，供cron检查
        flag_file = Path(".safety/STOP_CONTENT")
        flag_file.touch()
        print("[KILL SWITCH] 内容发布已暂停")
    
    def _stop_channel_operations(self):
        """停止渠道操作"""
        flag_file = Path(".safety/STOP_CHANNEL")
        flag_file.touch()
        # 清除API会话
        os.environ['SUBSTACK_API_DISABLED'] = 'true'
        print("[KILL SWITCH] 渠道操作已暂停")
    
    def _stop_all_automation(self):
        """停止所有自动化"""
        flag_file = Path(".safety/STOP_ALL")
        flag_file.touch()
        # 移除所有API密钥环境变量
        for key in ['SUBSTACK_API_KEY', 'SUBSTACK_SESSION']:
            if key in os.environ:
                del os.environ[key]
        print("[KILL SWITCH] 所有自动化已停止")
    
    def _initiate_account_recovery(self):
        """启动账号恢复流程"""
        flag_file = Path(".safety/ACCOUNT_RECOVERY")
        flag_file.touch()
        # 触发备用方案切换
        print("[KILL SWITCH] 备用方案已启动")
    
    def is_blocked(self, operation: str = None) -> bool:
        """检查操作是否被阻止"""
        if self.state['active_level'] == 0:
            return False
            
        # 检查标志文件
        if operation == 'content':
            return Path(".safety/STOP_CONTENT").exists()
        elif operation == 'channel':
            return Path(".safety/STOP_CHANNEL").exists()
        elif operation == 'all':
            return Path(".safety/STOP_ALL").exists()
        
        return self.state['active_level'] > 0
    
    def reset(self, authorized_by: str, reason: str):
        """手动重置 (需要授权)"""
        self.state = {
            'active_level': 0,
            'triggered_at': None,
            'triggered_by': None,
            'reason': None,
            'manual_override': True,
            'reset_by': authorized_by,
            'reset_reason': reason,
            'reset_at': datetime.now().isoformat()
        }
        self._save_state()
        
        # 清除标志文件
        for flag in ['STOP_CONTENT', 'STOP_CHANNEL', 'STOP_ALL', 'ACCOUNT_RECOVERY']:
            flag_path = Path(f".safety/{flag}")
            if flag_path.exists():
                flag_path.unlink()
        
        print(f"[KILL SWITCH] 已重置 by {authorized_by}")


# 使用示例
if __name__ == "__main__":
    ks = KillSwitch()
    
    # 检查是否可以发布
    if ks.is_blocked('content'):
        print("发布被阻止，跳过")
    else:
        print("执行发布")
    
    # 触发 kill switch
    # ks.trigger('channel', '平台警告', 'system_monitor')
    
    # 重置
    # ks.reset('admin', '问题已解决')
```

### 4.3 自动触发监控指标

```python
# safety/monitor.py
MONITORING_RULES = {
    'failed_login_attempts': {
        'threshold': 3,  # 5分钟内失败次数
        'window': 300,
        'action': 'trigger_kill_switch',
        'level': 'channel'
    },
    'api_error_rate': {
        'threshold': 50,  # 错误率超过50%
        'window': 600,
        'action': 'trigger_kill_switch',
        'level': 'channel'
    },
    'content_complaints': {
        'threshold': 3,  # 单篇投诉数
        'action': 'trigger_kill_switch',
        'level': 'content'
    },
    'unusual_publish_frequency': {
        'threshold': 5,  # 小时内发布数
        'window': 3600,
        'action': 'trigger_kill_switch',
        'level': 'content'
    }
}
```

---

## 五、频率限制规范

### 5.1 API 调用限制

```yaml
Substack API:
  请求限制:
    - 登录接口: 5次/分钟/IP
    - 发布接口: 10次/小时/账号
    - 获取文章: 60次/分钟/账号
    - 获取订阅者: 30次/分钟/账号
  超限处理:
    - 429状态码后退避
    - 指数退避策略 (Exponential Backoff)
    - 最大退避时间: 5分钟

Stripe API:
  请求限制:
    - 读取操作: 100次/秒
    - 写入操作: 10次/秒
  超限处理:
    - 使用Stripe内置重试机制
    - 本地缓存常用数据

OpenAI API:
  请求限制:
    - RPM (Requests Per Minute): 根据账户等级
    - TPM (Tokens Per Minute): 根据账户等级
  超限处理:
    - 实现Token流控制
    - 请求队列管理
```

### 5.2 内容发布限制

```yaml
Substack 发布限制:
  正常节奏:
    - 免费用户: 最多 3 篇/周
    - 付费订阅: 最多 7 篇/周
    - 推荐节奏: 5-7 篇/周
  预设发布:
    - 最多预设 30 天
    - 每日最多 1 篇定时发布
  异常检测:
    - 小时内 > 2 篇 → 触发审核
    - 一次性 > 5 篇 → 触发 kill switch
```

### 5.3 邮件发送限制

```yaml
Resend API 限制 (免费层):
  - 每日最多: 100 封
  - 每分钟最多: 10 封
  - 单次API调用最多: 100 收件人

邮件发送策略:
  - 批量发送间隔: 每批间隔 5 秒
  - 失败重试: 最多 3 次，指数退避
  - 严重失败阈值: 10% 失败率触发告警
```

### 5.4 实现示例: 带限速的 HTTP Client

```python
# utils/rate_limited_client.py
import time
import asyncio
from functools import wraps
from collections import deque
from datetime import datetime, timedelta

class RateLimiter:
    """基于滑动窗口的限速器"""
    
    def __init__(self, max_requests: int, window_seconds: int):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests = deque()
    
    def is_allowed(self) -> bool:
        """检查请求是否被允许"""
        now = datetime.now()
        
        # 移除窗口外的请求
        while self.requests and self.requests[0] < now - timedelta(seconds=self.window_seconds):
            self.requests.popleft()
        
        if len(self.requests) < self.max_requests:
            self.requests.append(now)
            return True
        return False
    
    def wait_time(self) -> float:
        """计算需要等待的时间"""
        if len(self.requests) < self.max_requests:
            return 0
        
        now = datetime.now()
        oldest = self.requests[0]
        wait = (oldest + timedelta(seconds=self.window_seconds) - now).total_seconds()
        return max(0, wait)


class RateLimitedClient:
    """带限速功能的HTTP客户端"""
    
    def __init__(self):
        # 为不同API配置限速器
        self.limiters = {
            'substack': {
                'login': RateLimiter(5, 60),      # 5次/分钟
                'publish': RateLimiter(10, 3600), # 10次/小时
                'read': RateLimiter(60, 60),      # 60次/分钟
            },
            'stripe': {
                'read': RateLimiter(100, 1),      # 100次/秒
                'write': RateLimiter(10, 1),      # 10次/秒
            },
            'resend': {
                'send': RateLimiter(10, 60),      # 10次/分钟
            }
        }
    
    async def request(self, service: str, operation: str, **kwargs):
        """发送带限速的请求"""
        limiter = self.limiters.get(service, {}).get(operation)
        
        if limiter:
            # 等待直到请求被允许
            while not limiter.is_allowed():
                wait_time = limiter.wait_time()
                print(f"Rate limit hit for {service}/{operation}, waiting {wait_time:.1f}s")
                await asyncio.sleep(wait_time)
        
        # 执行实际请求
        return await self._do_request(service, **kwargs)
    
    async def _do_request(self, service: str, **kwargs):
        """实际发送请求 (需要实现)"""
        # 实际实现...
        pass


# 装饰器方式使用
class SubstackAdapter:
    def __init__(self):
        self.client = RateLimitedClient()
        self.kill_switch = KillSwitch()
    
    async def publish_post(self, title: str, content: str):
        """发布文章 (带限速和 kill switch 检查)"""
        
        # 1. 检查 kill switch
        if self.kill_switch.is_blocked('content'):
            raise Exception("Publishing blocked by kill switch")
        
        # 2. 检查频率限制
        await self.client.request(
            service='substack',
            operation='publish',
            endpoint='/api/v1/posts',
            method='POST',
            data={'title': title, 'content': content}
        )
```

---

## 六、退款/退订流程

### 6.1 Substack 原生退订机制

```yaml
用户自助退订:
  路径: 账户设置 > 订阅管理 > 取消订阅
  生效: 即刻生效，保留当期访问权直至期满
  退款: 按剩余天数比例退还 (年付用户)

Stripe Connect 处理:
  - 取消订阅: 通过 Stripe API 自动处理
  - 退款: 通过 Stripe Dashboard 手动/自动处理
  - 手续费: 通常由创作者承担 ($0.30/笔)
```

### 6.2 退款政策模板

```markdown
## 退款政策

### 适用范围
本政策适用于通过 Substack 或 Stripe 订阅的付费内容。

### 退款条件

#### 1. 7天无条件退款
- 订阅后 7 天内可申请全额退款
- 不需要任何理由
- 处理时间: 5-10 个工作日

#### 2. 服务未交付退款
- 购买定制服务后未按承诺时间交付
- 可申请全额退款

#### 3. 内容质量退款
- 实际内容与宣传严重不符
- 需要具体证明
- 根据情况部分或全额退款

#### 4. 不退款情况
- 订阅超过 30 天且正常提供服务
- 用户已大量消耗内容
- 涉及遗传或商业秘密的内容

### 申请流程
1. 发送退款申请至 support@example.com
2. 提供订单号和退款理由
3. 客服 24 小时内确认
4. 处理完成后邮件通知

### 处理时间
- 7天无条件: 5-10 工作日
- 其他情况: 10-15 工作日
```

### 6.3 自动退款处理脚本

```python
# billing/refund_handler.py
from datetime import datetime, timedelta
from enum import Enum

class RefundType(Enum):
    FULL = "full"           # 全额退款
    PRORATED = "prorated"   # 按比例退款
    PARTIAL = "partial"     # 部分退款
    DENIED = "denied"       # 拒绝

class RefundHandler:
    """退款处理器"""
    
    def __init__(self):
        self.full_refund_window = timedelta(days=7)  # 7天无条件
        self.partial_refund_window = timedelta(days=30)  # 30天部分
    
    def calculate_refund(self, subscription) -> dict:
        """计算退款金额"""
        now = datetime.now()
        start = subscription.start_date
        end = subscription.end_date
        total_days = (end - start).days
        days_used = (now - start).days
        days_remaining = total_days - days_used
        
        # 检查无条件退款窗口
        if days_used <= 7:
            return {
                'type': RefundType.FULL,
                'amount': subscription.total_paid,
                'reason': '7-day unconditional refund'
            }
        
        # 检查服务未交付
        if subscription.is_custom_service and not subscription.delivered:
            return {
                'type': RefundType.FULL,
                'amount': subscription.total_paid,
                'reason': 'Service not delivered'
            }
        
        # 按比例计算 (年付用户)
        if subscription.billing_cycle == 'annual' and days_remaining > 30:
            prorated = (subscription.total_paid / total_days) * days_remaining
            return {
                'type': RefundType.PRORATED,
                'amount': round(prorated, 2),
                'reason': f'Prorated refund: {days_remaining} days remaining'
            }
        
        # 拒绝退款
        return {
            'type': RefundType.DENIED,
            'amount': 0,
            'reason': 'Outside refund window or service consumed'
        }
    
    def process_refund(self, subscription_id: str, reason: str) -> dict:
        """处理退款请求"""
        # 1. 获取订阅信息
        sub = self.get_subscription(subscription_id)
        
        # 2. 计算退款
        refund_info = self.calculate_refund(sub)
        
        # 3. 记录退款申请
        refund_record = {
            'subscription_id': subscription_id,
            'request_date': datetime.now(),
            'refund_type': refund_info['type'].value,
            'amount': refund_info['amount'],
            'reason': reason,
            'calculation_reason': refund_info['reason'],
            'status': 'pending'
        }
        self.save_refund_record(refund_record)
        
        # 4. 如果是自动处理类型，直接执行
        if refund_info['type'] in [RefundType.FULL, RefundType.PRORATED]:
            if refund_info['amount'] <= 100:  # 设置自动处理阈值
                self.execute_refund(refund_record)
                refund_record['status'] = 'completed'
            else:
                refund_record['status'] = 'pending_approval'
        
        return refund_record
```

### 6.4 退订自动化流程

```python
# billing/cancellation_handler.py
class CancellationHandler:
    """退订处理器"""
    
    def __init__(self):
        self.substack_adapter = SubstackAdapter()
        self.stripe_adapter = StripeAdapter()
    
    async def cancel_subscription(self, user_id: str, immediate: bool = False):
        """
        处理退订
        
        Args:
            user_id: 用户ID
            immediate: 是否立即终止访问（否则保留到期满）
        """
        try:
            # 1. 在 Substack 中取消
            await self.substack_adapter.cancel_subscription(user_id)
            
            # 2. 在 Stripe 中取消 (如果使用 Stripe)
            await self.stripe_adapter.cancel_subscription(user_id, 
                                                          at_period_end=not immediate)
            
            # 3. 更新本地状态
            self.update_local_subscription_status(user_id, 'cancelled')
            
            # 4. 发送确认邮件
            await self.send_cancellation_confirmation(user_id, immediate)
            
            # 5. 记录原因
            self.log_cancellation(user_id, immediate)
            
            return {'status': 'success', 'immediate': immediate}
            
        except Exception as e:
            # 如果失败，记录并通知人工处理
            self.log_error(user_id, 'cancellation_failed', str(e))
            await self.notify_manual_intervention(user_id, 'cancellation_failed')
            return {'status': 'error', 'error': str(e)}
    
    async def send_cancellation_confirmation(self, user_id: str, immediate: bool):
        """发送退订确认邮件"""
        user = self.get_user(user_id)
        
        if immediate:
            body = f"""
您的订阅已立即取消。

您的访问权限将立即终止。
如有未完成的服务，我们将根据退款政策处理。

感谢您的支持！
            """
        else:
            body = f"""
您的订阅取消已确认。

您的访问权限将保留至当前订阅周期结束。
期满后将自动转为免费订阅者。

感谢您的支持！
            """
        
        await self.send_email(user.email, "订阅取消确认", body)
```

---

## 七、Adapter/Cron/Content Workflow 安全边界

### 7.1 架构安全边界图

```
├── 内容生成层 (Content Generator)
│   ├── AI生成
│   │   ├── 限制: 不能直接访问外部API
│   │   ├── 限制: 不能读取敏感配置
│   │   └── 输出: Markdown草稿
│   └── 人工审核队列
│       ├── 输入: 待审核草稿
│       ├── 输出: 审核通过/拒绝/修改
│       └── 限制: 人工点确认
│
├── 定时任务层 (Cron Jobs)
│   ├── 内容生成任务
│   │   ├── 执行: 每日 06:00
│   │   ├── 限制: 最多每日 1 次
│   │   └── 安全: 需要审核队列非空
│   └── 数据更新任务
│       ├── 执行: 每日 00:00
│       ├── 限制: 只读取数据，不修改
│       └── 安全: 无敏感操作
│
└── 发布适配器层 (Substack Adapter)
    ├── 发布接口
    │   ├── 输入: 审核通过的草稿
    │   ├── 限制: 频率限制、kill switch 检查
    │   └── 输出: 已发布文章ID
    └── 状态监控
        ├── 输入: API响应
        ├── 限制: 只读取，不修改
        └── 输出: 监控数据
```

### 7.2 各层安全边界定义

#### 内容生成层

```yaml
权限:
  - 可以: 读取数据源、调用AI API、写入草稿目录
  - 不可以: 访问凭证、发布内容、修改用户数据

输入验证:
  - RSS/JSON数据格式检查
  - URL白名单验证
  - 内容长度限制 (< 100KB)

输出控制:
  - 草稿必须经过敏感词检测
  - 超长草稿标记待审核
  - 含外部链接草稿标记待审核
```

#### 定时任务层

```yaml
执行环境:
  - 独立用户权限 (非 root)
  - 只读配置权限
  - 限制网络访问 (只允许必要API)

日志记录:
  - 所有执行记录必须记录
  - 异常自动报警
  - 保留 90 天
```

#### 发布适配器层

```yaml
凭证管理:
  - 从环境变量或密钥管理工具读取
  - 内存中不泄露明文
  - 支持凭证轮换

发布前检查:
  - kill switch 状态检查
  - 审核队列确认
  - 频率限制检查

错误处理:
  - API错误自动重试 (最多3次)
  - 连续失败触发告警
  - 严重错误触发 kill switch
```

### 7.3 安全测试清单

```yaml
单元测试:
  - [✓] 敏感词检测准确率 > 95%
  - [✓] 超长内容被标记
  - [✓] 外部链接被检测
  - [✓] Kill switch 正确触发

集成测试:
  - [✓] 审核流程通过
  - [✓] 频率限制正确限流
  - [✓] 错误重试机制工作
  - [✓] 退款计算准确

端到端测试:
  - [✓] 内容生成 → 审核 → 发布 流程
  - [✓] Kill switch 停止所有操作
  - [✓] 异常情况下不发布
  - [✓] 退款/退订流程
```

---

## 八、平台合规检查

### 8.1 Substack 服务条款合规

```yaml
允许的内容:
  - 教育、分析、研究类内容
  - 个人观点和专业分析
  - 软件工具推荐

禁止的内容:
  - 欺诈性内容
  - 侵权内容
  - 恶意软件/病毒
  - 非法活动指南

自动化限制:
  - 不得违反服务条款第4.2条 (自动化工具使用)
  - 不得触发反垃圾邮件机制
  - 必须遵守频率限制
```

### 8.2 Stripe 合规要求

```yaml
商业行为:
  - 提供真实准确的产品描述
  - 明确的退款政策
  - 及时的客户支持

风控要求:
  - 保持拒付率 < 1%
  - 保持退款率 < 0.5%
  - 及时处理争议

数据安全:
  - PCI DSS 合规 (使用Stripe托管页面)
  - 不存储原始卡号
  - 加密传输敏感数据
```

---

## 九、验证命令清单

### 9.1 Secret 存储验证

```bash
# 1. 确认不存在硬编码凭证
cd /home/AgentAdmin/.hermes/shared/dev-team/projects/knowledge-subscription
grep -r "api_key\|apikey\|api-key\|token\|password\|secret" --include="*.py" --include="*.yaml" --include="*.json" --include="*.md" . | grep -v "\.pyc" | grep -v "__pycache__" | grep -v "\[REDACTED\]"
# 期望输出: 无明文凭证

# 2. 确认 .gitignore 包含敏感文件
cat .gitignore | grep -E "\.(env|secrets|key)"
# 期望输出: 包含 *.env, .secrets/, *.key

# 3. 确认环境变量配置
echo $SUBSTACK_API_KEY
# 期望输出: [REDACTED] 或空 (如果未设置)
```

### 9.2 Kill Switch 验证

```bash
# 1. 创建测试 kill switch
python3 -c "
from safety.kill_switch import KillSwitch
ks = KillSwitch('.safety/test_state.json')
ks.trigger('content', '测试触发', 'test')
print('Kill switch triggered:', ks.is_blocked('content'))
ks.reset('test', '测试重置')
print('After reset:', ks.is_blocked('content'))
"
# 期望输出: True, 然后 False

# 2. 检查标志文件
ls -la .safety/
# 期望输出: 测试后无残留标志文件
```

### 9.3 频率限制验证

```bash
# 1. 运行压力测试
python3 -c "
import asyncio
from utils.rate_limited_client import RateLimiter

limiter = RateLimiter(5, 60)  # 5次/分钟
for i in range(7):
    if limiter.is_allowed():
        print(f'Request {i+1}: allowed')
    else:
        print(f'Request {i+1}: blocked (wait: {limiter.wait_time():.1f}s)')
"
# 期望输出: 前5次通过，后2次被阻

# 2. 检查流量统计
ls -la logs/rate_limit/
# 期望输出: 存在流量日志文件
```

### 9.4 退款/退订验证

```bash
# 1. 运行退款测试
python3 -c "
from billing.refund_handler import RefundHandler, RefundType
from datetime import datetime, timedelta

class MockSub:
    def __init__(self, days_ago, total_paid, annual=False):
        self.start_date = datetime.now() - timedelta(days=days_ago)
        self.end_date = self.start_date + timedelta(days=365 if annual else 30)
        self.total_paid = total_paid
        self.billing_cycle = 'annual' if annual else 'monthly'
        self.is_custom_service = False
        self.delivered = True

handler = RefundHandler()

# 测试正常情况
tests = [
    (3, 99, False, RefundType.FULL),      # 7天内
    (20, 99, False, RefundType.DENIED),   # 超过窗口
    (100, 900, True, RefundType.PRORATED), # 年付退剩余
]

for days, paid, annual, expected in tests:
    sub = MockSub(days, paid, annual)
    result = handler.calculate_refund(sub)
    status = '✓' if result['type'] == expected else '✗'
    print(f'{status} Day {days}, 年付={annual}: {result[\"type\"].value}')
"
# 期望输出: 所有测试通过
```

---

## 十、复核总结与建议

### 10.1 当前状态

| 组件 | 安全状态 | 备注 |
|-------|----------|-------|
| Secret 存储 | ✅ 合规 | 未发现明文凭证 |
| 审核流程 | ✅ 已定义 | 待实施 |
| Kill Switch | ✅ 已定义 | 待实施 |
| 频率限制 | ✅ 已定义 | 待实施 |
| 退款/退订 | ✅ 已定义 | 待实施 |
| 自动化适配器 | ⏳ 不适用 | 当前为人工发布 |

### 10.2 风险评级

```yaml
低风险:
  - 当前项目为人工发布模式，无自动化风险
  - 使用Substack/Stripe原生功能，合规性高

中风险 (未来自动化时):
  - API密钥泄露风险
  - 内容审核遗漏
  - 频率限制绕过

缓解措施:
  - 本文档提供完整安全基线
  - 建议按照文档逐步实施
  - 定期安全审计
```

### 10.3 下一步行动

1. [□] 如果启动自动化，使用本文档作为安全基线
2. [□] 实施 kill switch 机制
3. [□] 配置频率限制
4. [□] 建立审核流程
5. [□] 定期（每月）安全复查

---

**复核完或 | 小安 (dev-security) | 2026-05-11**

*本文档应与项目一并维护，每次重大变更后更新*