#!/usr/bin/env python3
"""知识付费订阅核心模块

功能:
- 订阅计划管理
- 用户订阅状态检查
- 付费内容访问控制
- 订阅续期/取消处理

定价:
- 早鸟版: ¥29/月
- 专业版: ¥99/月
- 定制版: ¥499/次
"""

import json
from datetime import datetime, timedelta
from enum import Enum
from typing import Dict, List, Optional, Tuple


class PlanType(Enum):
    """订阅计划类型"""
    FREE = "free"
    EARLY_BIRD = "early_bird"  # 早鸟版 ¥29/月
    PROFESSIONAL = "professional"  # 专业版 ¥99/月
    CUSTOM = "custom"  # 定制版 ¥499/次


class SubscriptionStatus(Enum):
    """订阅状态"""
    ACTIVE = "active"
    EXPIRED = "expired"
    CANCELLED = "cancelled"
    PENDING = "pending"
    TRIAL = "trial"


class SubscriptionPlan:
    """订阅计划"""
    
    PLANS = {
        PlanType.FREE: {
            "name": "免费版",
            "price": 0,
            "price_cny": 0,
            "duration_days": None,
            "features": [
                "每日1条AI商机",
                "基础摘要",
                "公开内容访问"
            ],
            "daily_opportunities": 1,
            "include_scripts": False,
            "include_templates": False,
        },
        PlanType.EARLY_BIRD: {
            "name": "早鸟版",
            "price": 29,
            "price_cny": 29,
            "duration_days": 30,
            "features": [
                "每日3条AI商机",
                "完整市场分析",
                "基础Prompt模板",
                "邮件+微信推送",
                "专属社群资格"
            ],
            "daily_opportunities": 3,
            "include_scripts": False,
            "include_templates": True,
        },
        PlanType.PROFESSIONAL: {
            "name": "专业版",
            "price": 99,
            "price_cny": 99,
            "duration_days": 30,
            "features": [
                "每日10条AI商机",
                "深度市场分析",
                "完整Prompt模板库",
                "自动化脚本工具",
                "执行步骤手册",
                "邮件+微信+API推送",
                "1对1答疑(每月1次)"
            ],
            "daily_opportunities": 10,
            "include_scripts": True,
            "include_templates": True,
        },
        PlanType.CUSTOM: {
            "name": "定制版",
            "price": 499,
            "price_cny": 499,
            "duration_days": None,  # 一次性
            "features": [
                "专属领域机会雷达",
                "定制化分析报告",
                "1对1咨询(1小时)",
                "7天交付"
            ],
            "daily_opportunities": None,
            "include_scripts": True,
            "include_templates": True,
        }
    }
    
    @classmethod
    def get_plan(cls, plan_type: PlanType) -> Dict:
        """获取计划详情"""
        return cls.PLANS.get(plan_type, cls.PLANS[PlanType.FREE])
    
    @classmethod
    def get_all_plans(cls) -> Dict:
        """获取所有计划"""
        return cls.PLANS
    
    @classmethod
    def get_paid_plans(cls) -> Dict:
        """获取付费计划"""
        return {k: v for k, v in cls.PLANS.items() if v["price"] > 0}
    
    @classmethod
    def validate_plan_access(cls, plan_type: PlanType, feature: str) -> bool:
        """验证计划是否包含某功能"""
        plan = cls.get_plan(plan_type)
        if feature == "scripts":
            return plan.get("include_scripts", False)
        elif feature == "templates":
            return plan.get("include_templates", False)
        return False


class UserSubscription:
    """用户订阅管理"""
    
    def __init__(self, user_id: str, plan_type: PlanType = PlanType.FREE):
        self.user_id = user_id
        self.plan_type = plan_type
        # 初始状态：FREE计划直接激活，付费计划需要支付后激活
        self.status = SubscriptionStatus.ACTIVE
        self.start_date = datetime.now()
        self.end_date = None
        self.auto_renew = False
        self.payment_method = None
        self.trial_used = False
        
        # 计算结束日期
        plan = SubscriptionPlan.get_plan(plan_type)
        if plan["duration_days"]:
            self.end_date = self.start_date + timedelta(days=plan["duration_days"])
    
    def is_active(self) -> bool:
        """检查订阅是否有效"""
        # FREE计划总是活跃的
        if self.plan_type == PlanType.FREE:
            return True
        if self.status != SubscriptionStatus.ACTIVE:
            return False
        if self.end_date and datetime.now() > self.end_date:
            self.status = SubscriptionStatus.EXPIRED
            return False
        return True
    
    def can_access_content(self, content_tier: str = "free") -> bool:
        """检查用户能否访问特定层级内容"""
        if not self.is_active():
            return False
        
        tier_requirements = {
            "free": [PlanType.FREE, PlanType.EARLY_BIRD, PlanType.PROFESSIONAL, PlanType.CUSTOM],
            "early_bird": [PlanType.EARLY_BIRD, PlanType.PROFESSIONAL, PlanType.CUSTOM],
            "professional": [PlanType.PROFESSIONAL, PlanType.CUSTOM],
            "custom": [PlanType.CUSTOM]
        }
        
        allowed_plans = tier_requirements.get(content_tier, [PlanType.FREE])
        return self.plan_type in allowed_plans
    
    def get_daily_limit(self) -> int:
        """获取每日内容限额"""
        plan = SubscriptionPlan.get_plan(self.plan_type)
        return plan.get("daily_opportunities", 1)
    
    def days_remaining(self) -> Optional[int]:
        """获取剩余天数"""
        if not self.end_date:
            return None
        remaining = (self.end_date - datetime.now()).days
        return max(0, remaining)
    
    def to_dict(self) -> Dict:
        """转换为字典"""
        return {
            "user_id": self.user_id,
            "plan_type": self.plan_type.value,
            "status": self.status.value,
            "start_date": self.start_date.isoformat(),
            "end_date": self.end_date.isoformat() if self.end_date else None,
            "auto_renew": self.auto_renew,
            "days_remaining": self.days_remaining(),
            "is_active": self.is_active()
        }


class SubscriptionManager:
    """订阅管理器"""
    
    def __init__(self, storage_path: str = None):
        self.storage_path = storage_path or "/tmp/subscriptions.json"
        self._subscriptions: Dict[str, UserSubscription] = {}
        self._load_subscriptions()
    
    def _load_subscriptions(self):
        """加载订阅数据"""
        try:
            with open(self.storage_path, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                if not content:
                    return
                data = json.loads(content)
                for user_id, sub_data in data.items():
                    sub = UserSubscription(
                        user_id=sub_data["user_id"],
                        plan_type=PlanType(sub_data["plan_type"])
                    )
                    sub.status = SubscriptionStatus(sub_data["status"])
                    sub.start_date = datetime.fromisoformat(sub_data["start_date"])
                    if sub_data.get("end_date"):
                        sub.end_date = datetime.fromisoformat(sub_data["end_date"])
                    sub.auto_renew = sub_data.get("auto_renew", False)
                    self._subscriptions[user_id] = sub
        except (FileNotFoundError, json.JSONDecodeError):
            pass
    
    def _save_subscriptions(self):
        """保存订阅数据"""
        data = {uid: sub.to_dict() for uid, sub in self._subscriptions.items()}
        with open(self.storage_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def create_subscription(self, user_id: str, plan_type: PlanType, 
                          auto_renew: bool = False) -> UserSubscription:
        """创建新订阅"""
        subscription = UserSubscription(user_id, plan_type)
        subscription.auto_renew = auto_renew
        if plan_type != PlanType.FREE:
            subscription.status = SubscriptionStatus.ACTIVE
        self._subscriptions[user_id] = subscription
        self._save_subscriptions()
        return subscription
    
    def get_subscription(self, user_id: str) -> Optional[UserSubscription]:
        """获取用户订阅"""
        return self._subscriptions.get(user_id)
    
    def upgrade_subscription(self, user_id: str, new_plan: PlanType) -> bool:
        """升级订阅"""
        sub = self._subscriptions.get(user_id)
        if not sub:
            return False
        
        # 创建新订阅，保留开始时间
        new_sub = UserSubscription(user_id, new_plan)
        new_sub.start_date = sub.start_date
        new_sub.status = SubscriptionStatus.ACTIVE
        self._subscriptions[user_id] = new_sub
        self._save_subscriptions()
        return True
    
    def cancel_subscription(self, user_id: str) -> bool:
        """取消订阅"""
        sub = self._subscriptions.get(user_id)
        if not sub:
            return False
        sub.status = SubscriptionStatus.CANCELLED
        sub.auto_renew = False
        self._save_subscriptions()
        return True
    
    def get_stats(self) -> Dict:
        """获取订阅统计"""
        stats = {
            "total_users": len(self._subscriptions),
            "active_subscriptions": 0,
            "expired_subscriptions": 0,
            "by_plan": {},
            "monthly_recurring_revenue": 0
        }
        
        for sub in self._subscriptions.values():
            plan_name = sub.plan_type.value
            stats["by_plan"][plan_name] = stats["by_plan"].get(plan_name, 0) + 1
            
            if sub.is_active():
                stats["active_subscriptions"] += 1
                plan = SubscriptionPlan.get_plan(sub.plan_type)
                if plan["duration_days"]:
                    stats["monthly_recurring_revenue"] += plan["price_cny"]
            else:
                stats["expired_subscriptions"] += 1
        
        return stats


def check_payment_gateway() -> Dict:
    """检查支付网关状态"""
    return {
        "wechat_pay": {
            "available": True,
            "requires": ["商户号", "API证书", "回调配置"],
            "setup_status": "pending"
        },
        "alipay": {
            "available": True,
            "requires": ["应用ID", "私钥", "公钥", "回调配置"],
            "setup_status": "pending"
        },
        "stripe": {
            "available": True,
            "requires": ["API Key", "Webhook配置"],
            "setup_status": "pending"
        }
    }


def get_revenue_projections() -> Dict:
    """获取收入预测"""
    return {
        "month_1": {
            "early_bird_users": 50,
            "professional_users": 10,
            "custom_orders": 2,
            "revenue": 50 * 29 + 10 * 99 + 2 * 499
        },
        "month_3": {
            "early_bird_users": 150,
            "professional_users": 50,
            "custom_orders": 10,
            "revenue": 150 * 29 + 50 * 99 + 10 * 499
        },
        "month_6": {
            "early_bird_users": 300,
            "professional_users": 120,
            "custom_orders": 25,
            "revenue": 300 * 29 + 120 * 99 + 25 * 499
        },
        "month_12": {
            "early_bird_users": 500,
            "professional_users": 250,
            "custom_orders": 50,
            "revenue": 500 * 29 + 250 * 99 + 50 * 499
        }
    }


if __name__ == "__main__":
    # 测试代码
    print("=== 知识付费订阅模块测试 ===\n")
    
    # 显示所有计划
    print("1. 可用订阅计划:")
    for plan_type, plan in SubscriptionPlan.get_all_plans().items():
        print(f"   {plan['name']}: ¥{plan['price_cny']}/月")
        for feature in plan['features'][:3]:
            print(f"      - {feature}")
    
    # 创建订阅管理器
    manager = SubscriptionManager()
    
    # 创建测试用户
    print("\n2. 创建测试订阅:")
    sub = manager.create_subscription("user_001", PlanType.EARLY_BIRD)
    print(f"   用户: {sub.user_id}")
    print(f"   计划: {sub.plan_type.value}")
    print(f"   状态: {sub.status.value}")
    print(f"   剩余天数: {sub.days_remaining()}")
    
    # 检查权限
    print("\n3. 权限检查:")
    print(f"   访问免费内容: {sub.can_access_content('free')}")
    print(f"   访问早鸟内容: {sub.can_access_content('early_bird')}")
    print(f"   访问专业内容: {sub.can_access_content('professional')}")
    
    # 统计
    print("\n4. 订阅统计:")
    stats = manager.get_stats()
    print(f"   总用户数: {stats['total_users']}")
    print(f"   活跃订阅: {stats['active_subscriptions']}")
    print(f"   月度收入: ¥{stats['monthly_recurring_revenue']}")
    
    # 收入预测
    print("\n5. 收入预测:")
    projections = get_revenue_projections()
    for month, proj in projections.items():
        print(f"   {month}: ¥{proj['revenue']:,}")
    
    print("\n=== 测试完成 ===")
