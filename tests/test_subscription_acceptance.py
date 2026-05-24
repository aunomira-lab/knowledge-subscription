#!/usr/bin/env python3
"""
知识付费订阅付费验收测试

测试覆盖:
- 订阅计划验证
- 用户权限检查
- 内容访问控制
- 订阅状态管理
- 支付网关状态
- 交付流程验证
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
from datetime import datetime, timedelta
from app.subscription import (
    SubscriptionPlan, UserSubscription, SubscriptionManager,
    PlanType, SubscriptionStatus, check_payment_gateway, get_revenue_projections
)


class TestSubscriptionPlans(unittest.TestCase):
    """测试订阅计划"""
    
    def test_free_plan_exists(self):
        """测试免费计划存在"""
        plan = SubscriptionPlan.get_plan(PlanType.FREE)
        self.assertEqual(plan["price"], 0)
        self.assertEqual(plan["price_cny"], 0)
        self.assertEqual(plan["daily_opportunities"], 1)
    
    def test_early_bird_plan_pricing(self):
        """测试早鸟版定价正确"""
        plan = SubscriptionPlan.get_plan(PlanType.EARLY_BIRD)
        self.assertEqual(plan["price"], 29)
        self.assertEqual(plan["price_cny"], 29)
        self.assertEqual(plan["duration_days"], 30)
        self.assertEqual(plan["daily_opportunities"], 3)
        self.assertTrue(plan["include_templates"])
        self.assertFalse(plan["include_scripts"])
    
    def test_professional_plan_pricing(self):
        """测试专业版定价正确"""
        plan = SubscriptionPlan.get_plan(PlanType.PROFESSIONAL)
        self.assertEqual(plan["price"], 99)
        self.assertEqual(plan["price_cny"], 99)
        self.assertEqual(plan["duration_days"], 30)
        self.assertEqual(plan["daily_opportunities"], 10)
        self.assertTrue(plan["include_templates"])
        self.assertTrue(plan["include_scripts"])
    
    def test_custom_plan_pricing(self):
        """测试定制版定价正确"""
        plan = SubscriptionPlan.get_plan(PlanType.CUSTOM)
        self.assertEqual(plan["price"], 499)
        self.assertEqual(plan["price_cny"], 499)
        self.assertIsNone(plan["duration_days"])
        self.assertTrue(plan["include_templates"])
        self.assertTrue(plan["include_scripts"])
    
    def test_all_plans_have_required_fields(self):
        """测试所有计划都有必要字段"""
        for plan_type in PlanType:
            plan = SubscriptionPlan.get_plan(plan_type)
            self.assertIn("name", plan)
            self.assertIn("price", plan)
            self.assertIn("features", plan)
            self.assertIsInstance(plan["features"], list)
            self.assertGreater(len(plan["features"]), 0)


class TestUserSubscription(unittest.TestCase):
    """测试用户订阅"""
    
    def test_free_user_can_access_free_content(self):
        """免费用户可以访问免费内容"""
        sub = UserSubscription("test_free", PlanType.FREE)
        self.assertTrue(sub.can_access_content("free"))
    
    def test_free_user_cannot_access_paid_content(self):
        """免费用户不能访问付费内容"""
        sub = UserSubscription("test_free", PlanType.FREE)
        self.assertFalse(sub.can_access_content("early_bird"))
        self.assertFalse(sub.can_access_content("professional"))
        self.assertFalse(sub.can_access_content("custom"))
    
    def test_early_bird_user_access(self):
        """早鸟版用户访问权限"""
        sub = UserSubscription("test_early", PlanType.EARLY_BIRD)
        self.assertTrue(sub.can_access_content("free"))
        self.assertTrue(sub.can_access_content("early_bird"))
        self.assertFalse(sub.can_access_content("professional"))
        self.assertFalse(sub.can_access_content("custom"))
    
    def test_professional_user_access(self):
        """专业版用户访问权限"""
        sub = UserSubscription("test_pro", PlanType.PROFESSIONAL)
        self.assertTrue(sub.can_access_content("free"))
        self.assertTrue(sub.can_access_content("early_bird"))
        self.assertTrue(sub.can_access_content("professional"))
        self.assertFalse(sub.can_access_content("custom"))
    
    def test_custom_user_full_access(self):
        """定制版用户有完全访问权限"""
        sub = UserSubscription("test_custom", PlanType.CUSTOM)
        self.assertTrue(sub.can_access_content("free"))
        self.assertTrue(sub.can_access_content("early_bird"))
        self.assertTrue(sub.can_access_content("professional"))
        self.assertTrue(sub.can_access_content("custom"))
    
    def test_expired_subscription_blocks_access(self):
        """过期订阅阻止访问"""
        sub = UserSubscription("test_expired", PlanType.EARLY_BIRD)
        # 模拟过期
        sub.end_date = datetime.now() - timedelta(days=1)
        self.assertFalse(sub.is_active())
        self.assertFalse(sub.can_access_content("early_bird"))
    
    def test_daily_limit_calculation(self):
        """测试每日限额计算"""
        free_sub = UserSubscription("free", PlanType.FREE)
        early_sub = UserSubscription("early", PlanType.EARLY_BIRD)
        pro_sub = UserSubscription("pro", PlanType.PROFESSIONAL)
        
        self.assertEqual(free_sub.get_daily_limit(), 1)
        self.assertEqual(early_sub.get_daily_limit(), 3)
        self.assertEqual(pro_sub.get_daily_limit(), 10)


class TestSubscriptionManager(unittest.TestCase):
    """测试订阅管理器"""
    
    def setUp(self):
        """测试前初始化"""
        self.manager = SubscriptionManager("/tmp/test_subscriptions.json")
        self.manager._subscriptions = {}  # 清空数据
    
    def test_create_subscription(self):
        """测试创建订阅"""
        sub = self.manager.create_subscription("user_001", PlanType.EARLY_BIRD)
        self.assertEqual(sub.user_id, "user_001")
        self.assertEqual(sub.plan_type, PlanType.EARLY_BIRD)
        self.assertEqual(sub.status, SubscriptionStatus.ACTIVE)
    
    def test_get_subscription(self):
        """测试获取订阅"""
        self.manager.create_subscription("user_002", PlanType.PROFESSIONAL)
        sub = self.manager.get_subscription("user_002")
        self.assertIsNotNone(sub)
        self.assertEqual(sub.plan_type, PlanType.PROFESSIONAL)
    
    def test_upgrade_subscription(self):
        """测试升级订阅"""
        self.manager.create_subscription("user_003", PlanType.EARLY_BIRD)
        result = self.manager.upgrade_subscription("user_003", PlanType.PROFESSIONAL)
        self.assertTrue(result)
        sub = self.manager.get_subscription("user_003")
        self.assertEqual(sub.plan_type, PlanType.PROFESSIONAL)
    
    def test_cancel_subscription(self):
        """测试取消订阅"""
        self.manager.create_subscription("user_004", PlanType.EARLY_BIRD)
        result = self.manager.cancel_subscription("user_004")
        self.assertTrue(result)
        sub = self.manager.get_subscription("user_004")
        self.assertEqual(sub.status, SubscriptionStatus.CANCELLED)
    
    def test_stats_calculation(self):
        """测试统计计算"""
        self.manager.create_subscription("u1", PlanType.EARLY_BIRD)
        self.manager.create_subscription("u2", PlanType.PROFESSIONAL)
        self.manager.create_subscription("u3", PlanType.PROFESSIONAL)
        self.manager.create_subscription("u4", PlanType.FREE)
        
        stats = self.manager.get_stats()
        self.assertEqual(stats["total_users"], 4)
        self.assertEqual(stats["active_subscriptions"], 4)
        # MRR = 29*1 + 99*2 = 227
        self.assertEqual(stats["monthly_recurring_revenue"], 227)


class TestPaymentGateway(unittest.TestCase):
    """测试支付网关"""
    
    def test_payment_gateway_status(self):
        """测试支付网关状态"""
        gateways = check_payment_gateway()
        self.assertIn("wechat_pay", gateways)
        self.assertIn("alipay", gateways)
        self.assertIn("stripe", gateways)
        
        for name, config in gateways.items():
            self.assertIn("available", config)
            self.assertIn("requires", config)
            self.assertIn("setup_status", config)
            self.assertTrue(config["available"])
    
    def test_wechat_pay_requirements(self):
        """测试微信支付要求"""
        gateways = check_payment_gateway()
        wechat = gateways["wechat_pay"]
        required = ["商户号", "API证书", "回调配置"]
        for req in required:
            self.assertIn(req, wechat["requires"])
    
    def test_alipay_requirements(self):
        """测试支付宝要求"""
        gateways = check_payment_gateway()
        alipay = gateways["alipay"]
        required = ["应用ID", "私钥", "公钥", "回调配置"]
        for req in required:
            self.assertIn(req, alipay["requires"])


class TestRevenueProjections(unittest.TestCase):
    """测试收入预测"""
    
    def test_projections_structure(self):
        """测试预测结构"""
        projections = get_revenue_projections()
        self.assertIn("month_1", projections)
        self.assertIn("month_3", projections)
        self.assertIn("month_6", projections)
        self.assertIn("month_12", projections)
    
    def test_month_1_revenue(self):
        """测试第1月收入预测"""
        projections = get_revenue_projections()
        m1 = projections["month_1"]
        expected = 50 * 29 + 10 * 99 + 2 * 499
        self.assertEqual(m1["revenue"], expected)
    
    def test_month_12_revenue(self):
        """测试第12月收入预测"""
        projections = get_revenue_projections()
        m12 = projections["month_12"]
        expected = 500 * 29 + 250 * 99 + 50 * 499
        self.assertEqual(m12["revenue"], expected)
    
    def test_growth_trajectory(self):
        """测试增长轨迹"""
        projections = get_revenue_projections()
        revenues = [
            projections["month_1"]["revenue"],
            projections["month_3"]["revenue"],
            projections["month_6"]["revenue"],
            projections["month_12"]["revenue"]
        ]
        # 确保收入递增
        for i in range(1, len(revenues)):
            self.assertGreater(revenues[i], revenues[i-1])


class TestContentDelivery(unittest.TestCase):
    """测试内容交付"""
    
    def test_content_tiers_defined(self):
        """测试内容层级定义"""
        tiers = ["free", "early_bird", "professional", "custom"]
        sub = UserSubscription("test", PlanType.PROFESSIONAL)
        for tier in tiers:
            result = sub.can_access_content(tier)
            self.assertIsInstance(result, bool)
    
    def test_paid_content_protection(self):
        """测试付费内容保护"""
        free_sub = UserSubscription("free", PlanType.FREE)
        
        # 验证付费内容不被未授权用户访问
        self.assertFalse(free_sub.can_access_content("early_bird"))
        self.assertFalse(free_sub.can_access_content("professional"))
        self.assertFalse(free_sub.can_access_content("custom"))


class TestBlockingIssues(unittest.TestCase):
    """测试阻塞问题"""
    
    def test_payment_gateway_pending(self):
        """验证支付网关需要配置"""
        gateways = check_payment_gateway()
        for name, config in gateways.items():
            if config["setup_status"] == "pending":
                self.assertGreater(len(config["requires"]), 0, 
                    f"{name} 需要配置才能使用")
    
    def test_subscription_persistence(self):
        """测试订阅数据持久化"""
        import tempfile
        import os
        
        # 使用临时文件测试
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            temp_path = f.name
        
        try:
            manager1 = SubscriptionManager(temp_path)
            manager1.create_subscription("persist_test", PlanType.EARLY_BIRD)
            
            # 新实例加载同一文件
            manager2 = SubscriptionManager(temp_path)
            sub = manager2.get_subscription("persist_test")
            self.assertIsNotNone(sub)
            self.assertEqual(sub.plan_type, PlanType.EARLY_BIRD)
        finally:
            os.unlink(temp_path)


def run_acceptance_tests():
    """运行验收测试"""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # 添加所有测试类
    suite.addTests(loader.loadTestsFromTestCase(TestSubscriptionPlans))
    suite.addTests(loader.loadTestsFromTestCase(TestUserSubscription))
    suite.addTests(loader.loadTestsFromTestCase(TestSubscriptionManager))
    suite.addTests(loader.loadTestsFromTestCase(TestPaymentGateway))
    suite.addTests(loader.loadTestsFromTestCase(TestRevenueProjections))
    suite.addTests(loader.loadTestsFromTestCase(TestContentDelivery))
    suite.addTests(loader.loadTestsFromTestCase(TestBlockingIssues))
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_acceptance_tests()
    sys.exit(0 if success else 1)
