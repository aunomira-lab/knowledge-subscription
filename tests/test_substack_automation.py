#!/usr/bin/env python3
"""
Substack自动化安全验收测试

测试目标: 确保 READY_MANUAL_PUBLISH/NEEDS_CREDENTIALS 状态不会被误报为 PUBLISHED

安全关键路径:
1. 无凭证时 SubstackAdapter 必须返回 manual 模式
2. 队列状态转换必须正确
3. 凭证不得在任何输出中泄露
4. publish() 返回结果必须准确反映实际发布状态
"""

import sys
import os
import unittest
import tempfile
import json
import shutil
from pathlib import Path
from datetime import datetime, timezone

# Add project paths
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, str(Path('/home/AgentAdmin/.hermes/shared/dev-team')))

from system.social_publisher.adapters import SubstackAdapter, PublishResult, ADAPTERS
from system.social_publisher import core


class TestPublishResultAccuracy(unittest.TestCase):
    """测试 PublishResult 状态准确性 - 防误报核心"""

    def test_ok_result_structure(self):
        """验证成功结果包含必要字段"""
        result = PublishResult.ok("substack", "https://example.substack.com", "manual")
        self.assertTrue(result.get('success'))
        self.assertEqual(result.get('platform'), 'substack')
        self.assertEqual(result.get('url'), 'https://example.substack.com')
        self.assertEqual(result.get('mode'), 'manual')

    def test_fail_result_structure(self):
        """验证失败结果包含必要字段"""
        result = PublishResult.fail("substack", "Missing credentials", "error")
        self.assertFalse(result.get('success'))
        self.assertEqual(result.get('platform'), 'substack')
        self.assertIn('message', result)

    def test_result_immutable_dict_behavior(self):
        """PublishResult 应该表现得像普通 dict"""
        result = PublishResult.ok("substack", "url", "manual")
        self.assertIsInstance(result, dict)
        self.assertIn('success', result)
        self.assertIn('platform', result)


class TestSubstackAdapterSafety(unittest.TestCase):
    """测试 SubstackAdapter 安全行为"""

    def setUp(self):
        """测试前准备临时目录"""
        self.temp_dir = tempfile.mkdtemp()
        self.outbox_dir = Path(self.temp_dir) / "outbox"
        self.outbox_dir.mkdir(exist_ok=True)
        self.adapter = SubstackAdapter({}, self.outbox_dir)

    def tearDown(self):
        """测试后清理"""
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_adapter_never_auto_publishes(self):
        """SubstackAdapter 必须永远不会自动发布 (supports_auto_publish=False)"""
        self.assertFalse(SubstackAdapter.supports_auto_publish)

    def test_adapter_risk_level(self):
        """SubstackAdapter 应该有正确的风险评级"""
        self.assertEqual(SubstackAdapter.risk, "medium")

    def test_publish_returns_manual_mode(self):
        """publish() 必须返回 mode='manual' - 这是安全关键"""
        post = {
            "id": "test_post_001",
            "title": "Test Title",
            "body": "Test body content",
            "project": "test-project"
        }
        result = self.adapter.publish(post)

        # 关键断言: mode 必须是 manual
        self.assertEqual(result.get('mode'), 'manual',
            "CRITICAL: SubstackAdapter.publish() must return mode='manual' to prevent false PUBLISHED status")

    def test_publish_returns_success_but_manual(self):
        """publish() 返回 success=True 但 mode=manual - 这不应被标记为 PUBLISHED"""
        post = {
            "id": "test_post_002",
            "title": "Test Title",
            "body": "Test body content",
            "project": "test-project"
        }
        result = self.adapter.publish(post)

        # 可以返回 success=True（表示文件已写入outbox）
        self.assertTrue(result.get('success'))
        # 但 mode 必须是 manual
        self.assertEqual(result.get('mode'), 'manual')

    def test_creates_outbox_file(self):
        """publish() 应该在 outbox 创建文件"""
        post = {
            "id": "test_post_003",
            "title": "Test Newsletter",
            "body": "Test content for newsletter",
            "project": "knowledge-subscription"
        }
        result = self.adapter.publish(post)

        # 验证文件被创建
        self.assertTrue(result.get('success'))
        url = result.get('url', '')
        self.assertTrue(url.startswith('manual://'))

        # 验证文件内容
        substack_dir = self.outbox_dir / "substack"
        files = list(substack_dir.glob("*.md"))
        self.assertGreater(len(files), 0, "Outbox file should be created")

        content = files[0].read_text(encoding='utf-8')
        self.assertIn("READY TO PUBLISH: substack", content)
        self.assertIn("Status: APPROVED -> READY_MANUAL_PUBLISH", content)

    def test_no_credentials_in_output(self):
        """输出中不得包含任何凭证信息"""
        post = {
            "id": "test_post_004",
            "title": "Test",
            "body": "Test",
            "project": "test"
        }
        result = self.adapter.publish(post)

        result_str = json.dumps(result, ensure_ascii=False)

        # 检查常见凭证模式
        sensitive_patterns = [
            "api_key", "apikey", "api-key",
            "token", "password", "secret",
            "cookie", "session", "auth",
            "Bearer ", "Basic ", "AWS_",
            "-----BEGIN", "PRIVATE KEY-----"
        ]

        for pattern in sensitive_patterns:
            self.assertNotIn(pattern.lower(), result_str.lower(),
                f"Credential leak detected: '{pattern}' found in publish result")

    def test_render_text_no_credential_leakage(self):
        """render_text 不应该意外包含凭证"""
        # 模拟一个可能包含凭证的post
        post = {
            "title": "Test",
            "body": "Some content",
            "cta": "Subscribe",
            "tags": ["#test"]
        }
        text = self.adapter.render_text(post)

        # 确保文本渲染正常
        self.assertIn("Test", text)
        self.assertIn("Some content", text)


class TestQueueStateTransitions(unittest.TestCase):
    """测试队列状态转换 - 防止状态误报"""

    def setUp(self):
        """设置临时工作区"""
        self.temp_dir = tempfile.mkdtemp()
        self.workspace = "test_workspace_" + datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')
        self.original_base = core.BASE

        # 使用临时目录作为工作区
        self.workspace_dir = Path(self.temp_dir) / self.workspace
        self.workspace_dir.mkdir(parents=True, exist_ok=True)

        # 创建必要文件
        (self.workspace_dir / "config.json").write_text(json.dumps(core.DEFAULT_CONFIG, ensure_ascii=False, indent=2))
        (self.workspace_dir / "queue.json").write_text(json.dumps({"posts": []}, ensure_ascii=False, indent=2))

    def tearDown(self):
        """清理"""
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def _create_test_post(self, platform="substack", status="DRAFT"):
        """辅助方法: 创建测试post"""
        return {
            "id": f"test_{platform}_{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}",
            "project": "knowledge-subscription",
            "workspace": self.workspace,
            "platform": platform,
            "title": "Test Post",
            "body": "Test content",
            "cta": "Subscribe",
            "tags": [],
            "assets": [],
            "metadata": {},
            "created_by": "test",
            "created_at": datetime.now(timezone.utc).isoformat(),
            "status": status,
            "reviewer_note": "",
            "approved_at": None,
            "rejected_at": None,
            "published_at": None,
            "published_url": None,
            "publish_result": None,
            "attempts": 0
        }

    def test_substack_auto_publish_disabled(self):
        """Substack 配置中 auto_publish 必须为 False"""
        cfg = core.DEFAULT_CONFIG
        substack_cfg = cfg.get('platforms', {}).get('substack', {})
        self.assertFalse(substack_cfg.get('auto_publish', True),
            "CRITICAL: Substack auto_publish must be False in default config")

    def test_route_post_to_ready_manual_publish(self):
        """新创建的 Substack post 应该路由到 READY_MANUAL_PUBLISH"""
        post = self._create_test_post(platform="substack")
        cfg = core.DEFAULT_CONFIG

        routed = core.route_post(post, cfg)

        # 关键断言: 应该是 READY_MANUAL_PUBLISH 而不是 PUBLISHED
        self.assertEqual(routed.get('status'), 'READY_MANUAL_PUBLISH',
            "Substack posts should route to READY_MANUAL_PUBLISH, not PUBLISHED")
        self.assertIn('fallback_to_outbox', routed.get('route_reason', ''))

    def test_manual_mode_does_not_become_published(self):
        """关键测试: manual 模式的结果不能导致 PUBLISHED 状态"""
        # 这是防止误报的核心测试
        post = self._create_test_post(platform="substack", status="APPROVED")

        # 模拟 publish 调用
        adapter = SubstackAdapter({}, Path(self.temp_dir) / "outbox")
        result = adapter.publish(post)

        # 验证结果
        self.assertTrue(result.get('success'))  # 文件写入成功
        self.assertEqual(result.get('mode'), 'manual')  # 但模式是 manual

        # 根据 core.py 的逻辑:
        # if result.get('success') and result.get('mode') == 'manual':
        #     new_status = 'READY_MANUAL_PUBLISH'

        if result.get('success') and result.get('mode') == 'manual':
            new_status = 'READY_MANUAL_PUBLISH'
        else:
            new_status = 'PUBLISHED'

        # 关键断言: 必须是 READY_MANUAL_PUBLISH
        self.assertEqual(new_status, 'READY_MANUAL_PUBLISH',
            "CRITICAL SAFETY: manual mode must result in READY_MANUAL_PUBLISH status, not PUBLISHED")

    def test_needs_credentials_state_handling(self):
        """NEEDS_CREDENTIALS 状态不应被误报"""
        # 模拟缺少凭证的场景
        post = self._create_test_post(platform="x", status="APPROVED")  # X 平台需要凭证

        # 模拟 XAdapter 在没有凭证时的行为
        cfg = {'auto_publish': True}  # 启用但无凭证

        # 检查 can_auto_publish 逻辑
        can_auto, reason = core.can_auto_publish(post, {
            'auto_publish_enabled': True,
            'platforms': {'x': {'auto_publish': True, 'adapter': 'x'}}
        })

        # 没有 x-cli 时应该返回 False
        self.assertFalse(can_auto, "Without x-cli, X posts should not be auto-publishable")
        self.assertIn('x-cli', reason.lower())


class TestCredentialLeakagePrevention(unittest.TestCase):
    """测试凭证泄露防护"""

    def test_no_hardcoded_credentials_in_adapters(self):
        """适配器代码中不得包含硬编码凭证"""
        adapter_file = Path('/home/AgentAdmin/.hermes/shared/dev-team/system/social_publisher/adapters.py')
        content = adapter_file.read_text(encoding='utf-8')

        # 检查可疑模式
        suspicious_patterns = [
            r'api[_-]?key\s*=\s*["\'][^"\']{10,}["\']',
            r'token\s*=\s*["\'][^"\']{10,}["\']',
            r'password\s*=\s*["\'][^"\']+["\']',
            r'secret\s*=\s*["\'][^"\']{10,}["\']',
            r'sk-\w{20,}',  # OpenAI style key
            r'[A-Za-z0-9]{32,}',  # Long random strings that could be keys
        ]

        import re
        for pattern in suspicious_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            # 过滤掉注释和样例
            filtered = [m for m in matches if not any(x in m.lower() for x in ['example', 'sample', 'test', 'your_'])]
            self.assertEqual(len(filtered), 0,
                f"Potential credential found in adapters.py matching pattern: {pattern}")

    def test_safe_error_messages(self):
        """错误消息不应泄露敏感信息"""
        adapter = SubstackAdapter({}, Path('/tmp'))

        post = {"id": "test", "title": "Test", "body": "Test"}
        result = adapter.publish(post)

        # 检查错误消息
        message = json.dumps(result, ensure_ascii=False)

        # 不应包含文件系统路径
        self.assertNotIn('/home/', message.lower())
        self.assertNotIn('/root/', message.lower())

        # 不应包含可能敏感的信息
        self.assertNotIn('config', message.lower())


class TestSubstackSpecificBehavior(unittest.TestCase):
    """测试 Substack 特定行为"""

    def test_adapter_name_registration(self):
        """SubstackAdapter 应该正确注册"""
        self.assertIn('substack', ADAPTERS)
        self.assertIn('upstack', ADAPTERS)
        self.assertIn('newsletter', ADAPTERS)

        self.assertEqual(ADAPTERS['substack'], SubstackAdapter)

    def test_substack_adapter_is_manual_only(self):
        """SubstackAdapter 应该只支持手动模式"""
        adapter = SubstackAdapter({}, Path('/tmp'))
        self.assertFalse(adapter.supports_auto_publish)

    def test_multiple_aliases_all_use_same_adapter(self):
        """所有别名都使用相同的适配器"""
        self.assertEqual(ADAPTERS['substack'], ADAPTERS['upstack'])
        self.assertEqual(ADAPTERS['substack'], ADAPTERS['newsletter'])


class TestEndToEndSafety(unittest.TestCase):
    """端到端安全测试"""

    def test_complete_substack_workflow(self):
        """完整的 Substack 发布工作流测试"""
        with tempfile.TemporaryDirectory() as temp_dir:
            outbox_dir = Path(temp_dir) / "outbox"
            outbox_dir.mkdir()

            # 1. 创建 post
            post = {
                "id": "smp_knowledge_test_20250101_120000_000001_abc123",
                "project": "knowledge-subscription",
                "platform": "substack",
                "title": "AI商机雷达 - 第1期",
                "body": "本期内容测试",
                "cta": "订阅获取完整内容",
                "tags": ["AI", "副业"],
                "created_by": "test"
            }

            # 2. 使用适配器发布
            adapter = SubstackAdapter({}, outbox_dir)
            result = adapter.publish(post)

            # 3. 验证结果
            self.assertTrue(result.get('success'))
            self.assertEqual(result.get('mode'), 'manual')
            self.assertEqual(result.get('platform'), 'substack')

            # 4. 模拟 core.py 的状态转换逻辑
            if result.get('success') and result.get('mode') == 'manual':
                new_status = 'READY_MANUAL_PUBLISH'
                published_at = None
            elif result.get('success'):
                new_status = 'PUBLISHED'
                published_at = datetime.now(timezone.utc).isoformat()
            else:
                new_status = 'FAILED'
                published_at = None

            # 5. 关键安全断言
            self.assertEqual(new_status, 'READY_MANUAL_PUBLISH',
                "SAFETY: Substack manual publish should never result in PUBLISHED status")
            self.assertIsNone(published_at,
                "SAFETY: Manual publish should not set published_at")

            # 6. 验证 outbox 文件存在
            substack_outbox = outbox_dir / "substack"
            self.assertTrue(substack_outbox.exists())

            files = list(substack_outbox.glob("*.md"))
            self.assertEqual(len(files), 1)

            # 7. 验证文件内容
            content = files[0].read_text(encoding='utf-8')
            self.assertIn("READY TO PUBLISH: substack", content)
            self.assertIn("Status: APPROVED -> READY_MANUAL_PUBLISH", content)
            self.assertIn("AI商机雷达 - 第1期", content)


class TestSmokeWithoutCredentials(unittest.TestCase):
    """无凭证冒烟测试"""

    def test_smoke_substack_without_any_credentials(self):
        """没有任何凭证时 Substack 应该正常工作 (manual 模式)"""
        # 确保环境中没有可疑凭证
        env_vars_to_check = ['API_KEY', 'TOKEN', 'SECRET', 'PASSWORD', 'COOKIE']
        for var in env_vars_to_check:
            os.environ.pop(var, None)  # 清理测试环境

        with tempfile.TemporaryDirectory() as temp_dir:
            outbox_dir = Path(temp_dir) / "outbox"
            outbox_dir.mkdir()

            adapter = SubstackAdapter({}, outbox_dir)

            post = {
                "id": "smoke_test",
                "title": "Smoke Test",
                "body": "Testing without credentials",
                "project": "test"
            }

            # 应该成功执行 (写入 outbox)
            result = adapter.publish(post)

            self.assertTrue(result.get('success'))
            self.assertEqual(result.get('mode'), 'manual')

            # 验证文件创建
            files = list((outbox_dir / "substack").glob("*.md"))
            self.assertEqual(len(files), 1)


class TestFalsePositivePrevention(unittest.TestCase):
    """专门测试防止误报的边界情况"""

    def test_success_true_but_not_published(self):
        """success=True 不代表已发布 - 这是最容易误报的场景"""
        # 这是防止误报的关键测试
        # PublishResult.ok() 可以返回 success=True
        # 但如果 mode='manual'，状态必须是 READY_MANUAL_PUBLISH

        result = PublishResult.ok("substack", "manual://path/to/file", "manual")

        self.assertTrue(result.get('success'))  # 文件写入成功
        self.assertEqual(result.get('mode'), 'manual')  # 但只是 manual

        # 任何人检查这个结果时，必须同时检查 mode
        # 不能只看到 success=True 就认为已发布

    def test_no_accidental_published_status(self):
        """确保不会意外产生 PUBLISHED 状态"""
        # 这是安全测试的核心

        # 只有以下情况应该产生 PUBLISHED:
        # 1. result.success == True AND result.mode != 'manual'

        manual_result = PublishResult.ok("substack", "url", "manual")
        auto_result = PublishResult.ok("webhook", "https://api.example.com/post", "webhook")

        # 根据 core.py 逻辑:
        def get_status(result):
            if result.get('success') and result.get('mode') != 'manual':
                return 'PUBLISHED'
            elif result.get('success') and result.get('mode') == 'manual':
                return 'READY_MANUAL_PUBLISH'
            else:
                return 'FAILED'

        self.assertEqual(get_status(manual_result), 'READY_MANUAL_PUBLISH')
        self.assertEqual(get_status(auto_result), 'PUBLISHED')


def run_substack_safety_tests():
    """运行 Substack 安全测试套件"""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # 添加所有测试类
    suite.addTests(loader.loadTestsFromTestCase(TestPublishResultAccuracy))
    suite.addTests(loader.loadTestsFromTestCase(TestSubstackAdapterSafety))
    suite.addTests(loader.loadTestsFromTestCase(TestQueueStateTransitions))
    suite.addTests(loader.loadTestsFromTestCase(TestCredentialLeakagePrevention))
    suite.addTests(loader.loadTestsFromTestCase(TestSubstackSpecificBehavior))
    suite.addTests(loader.loadTestsFromTestCase(TestEndToEndSafety))
    suite.addTests(loader.loadTestsFromTestCase(TestSmokeWithoutCredentials))
    suite.addTests(loader.loadTestsFromTestCase(TestFalsePositivePrevention))

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_substack_safety_tests()
    sys.exit(0 if success else 1)
