#!/usr/bin/env python3
"""Tests for Substack Enhanced Adapter.

Usage:
    cd /home/AgentAdmin/.hermes/shared/dev-team
    python3 projects/knowledge-subscription/tests/test_substack_adapter.py
"""
from __future__ import annotations

import sys
import tempfile
from pathlib import Path

# Add system directory to path for imports
sys.path.insert(0, '/home/AgentAdmin/.hermes/shared/dev-team/system')

from social_publisher.substack_adapter import (
    SubstackEnhancedAdapter,
    CredentialStatus,
)


def test_no_credentials():
    """Test that missing credentials are properly detected."""
    with tempfile.TemporaryDirectory() as tmpdir:
        adapter = SubstackEnhancedAdapter({}, Path(tmpdir))
        status = adapter.check_credentials()
        
        assert not status.has_credentials, "Should not have credentials"
        assert not status.can_auto_publish, "Should not be able to auto publish"
        assert not status.can_semi_auto, "Should not be able to semi-auto"
        assert "publication_url" in status.missing_fields, "Should be missing publication_url"
        print("  ✓ test_no_credentials passed")


def test_publication_url_only():
    """Test that publication_url enables semi-auto mode."""
    with tempfile.TemporaryDirectory() as tmpdir:
        adapter = SubstackEnhancedAdapter(
            {"credentials": {"publication_url": "https://test.substack.com"}},
            Path(tmpdir)
        )
        status = adapter.check_credentials()
        
        assert not status.has_credentials, "Should not have full credentials"
        assert not status.can_auto_publish, "Should not be able to auto publish"
        assert status.can_semi_auto, "Should be able to semi-auto"
        assert "api_key" in status.missing_fields, "Should be missing api_key"
        print("  ✓ test_publication_url_only passed")


def test_full_credentials():
    """Test that full credentials enable auto mode."""
    with tempfile.TemporaryDirectory() as tmpdir:
        adapter = SubstackEnhancedAdapter(
            {"credentials": {
                "publication_url": "https://test.substack.com",
                "api_key": "test_key_123"
            }},
            Path(tmpdir)
        )
        status = adapter.check_credentials()
        
        assert status.has_credentials, "Should have credentials"
        assert status.can_auto_publish, "Should be able to auto publish"
        assert status.can_semi_auto, "Should be able to semi-auto"
        assert len(status.missing_fields) == 0, "Should have no missing fields"
        print("  ✓ test_full_credentials passed")


def test_invalid_publication_url():
    """Test validation catches invalid URLs."""
    with tempfile.TemporaryDirectory() as tmpdir:
        adapter = SubstackEnhancedAdapter(
            {"credentials": {"publication_url": "not-a-url"}},
            Path(tmpdir)
        )
        is_valid, errors = adapter.validate_config()
        assert not is_valid, "Should not be valid"
        assert any("https://" in e for e in errors), "Should mention https requirement"
        print("  ✓ test_invalid_publication_url passed")


def test_basic_render():
    """Test basic post rendering."""
    with tempfile.TemporaryDirectory() as tmpdir:
        adapter = SubstackEnhancedAdapter({}, Path(tmpdir))
        
        post = {
            "title": "Test Title",
            "body": "Test body content",
            "cta": "Subscribe now",
            "tags": ["tag1", "tag2"],
        }
        
        rendered = adapter.render_post(post)
        
        assert rendered["title"] == "Test Title", "Title should match"
        assert "Test body content" in rendered["content"], "Body should be in content"
        assert "Subscribe now" in rendered["content"], "CTA should be in content"
        assert "#tag1" in rendered["content"], "Tag1 should be in content"
        assert "#tag2" in rendered["content"], "Tag2 should be in content"
        print("  ✓ test_basic_render passed")


def test_render_no_cta():
    """Test rendering without CTA."""
    with tempfile.TemporaryDirectory() as tmpdir:
        adapter = SubstackEnhancedAdapter({}, Path(tmpdir))
        
        post = {
            "title": "Test",
            "body": "Body",
            "cta": "",
            "tags": [],
        }
        
        rendered = adapter.render_post(post)
        
        assert rendered["title"] == "Test", "Title should match"
        assert rendered["content"] == "Body", "Content should be just body"
        print("  ✓ test_render_no_cta passed")


def test_render_tags_formatting():
    """Test that tags are properly formatted."""
    with tempfile.TemporaryDirectory() as tmpdir:
        adapter = SubstackEnhancedAdapter({}, Path(tmpdir))
        
        post = {
            "title": "Test",
            "body": "Body",
            "cta": "",
            "tags": ["#AI", "newsletter", "#test"],
        }
        
        rendered = adapter.render_post(post)
        
        # Should handle tags with or without # prefix
        assert "#AI" in rendered["content"], "AI tag should be present"
        assert "#newsletter" in rendered["content"], "newsletter tag should be present"
        assert "#test" in rendered["content"], "test tag should be present"
        # Should not have double ##
        assert "##" not in rendered["content"], "Should not have double hash"
        print("  ✓ test_render_tags_formatting passed")


def test_publish_no_credentials_creates_manual_outbox():
    """Test that publishing without credentials creates manual outbox."""
    with tempfile.TemporaryDirectory() as tmpdir:
        adapter = SubstackEnhancedAdapter({}, Path(tmpdir))
        
        post = {
            "id": "test_post_123",
            "project": "knowledge-subscription",
            "platform": "substack",
            "title": "Test Newsletter",
            "body": "This is test content.",
            "cta": "Subscribe!",
            "tags": ["test"],
        }
        
        result = adapter.publish(post)
        
        assert not result["success"], "Should not succeed without credentials"
        assert result["status"] == "NEEDS_CREDENTIALS", "Status should be NEEDS_CREDENTIALS"
        assert result["mode"] == "manual", "Mode should be manual"
        assert "NEEDS_CREDENTIALS" in result["message"], "Message should indicate missing credentials"
        
        # Check that outbox file was created
        outbox_path = Path(tmpdir) / "substack"
        assert outbox_path.exists(), "Outbox directory should exist"
        files = list(outbox_path.glob("*.md"))
        assert len(files) == 1, "Should create exactly one markdown file"
        
        # Check content includes missing fields info
        content = files[0].read_text()
        assert "NEEDS_CREDENTIALS" in content, "File should have NEEDS_CREDENTIALS header"
        assert "publication_url" in content, "File should mention publication_url"
        print("  ✓ test_publish_no_credentials_creates_manual_outbox passed")


def test_publish_with_url_creates_semi_auto():
    """Test that publishing with publication_url creates semi-auto script."""
    with tempfile.TemporaryDirectory() as tmpdir:
        adapter = SubstackEnhancedAdapter(
            {"credentials": {"publication_url": "https://test.substack.com"}},
            Path(tmpdir)
        )
        
        post = {
            "id": "test_post_456",
            "project": "knowledge-subscription",
            "platform": "substack",
            "title": "Semi-Auto Test",
            "body": "Content for semi-auto test.",
            "cta": "",
            "tags": [],
        }
        
        result = adapter.publish(post)
        
        assert result["success"], "Should succeed (ready for manual)"
        assert result["status"] == "READY_MANUAL_PUBLISH", "Status should be READY_MANUAL_PUBLISH"
        assert result["mode"] == "semi_auto", "Mode should be semi_auto"
        assert "script_path" in result, "Should have script_path"
        assert "markdown_path" in result, "Should have markdown_path"
        
        # Check both files created
        outbox_path = Path(tmpdir) / "substack"
        md_files = list(outbox_path.glob("*.md"))
        py_files = list(outbox_path.glob("*.py"))
        
        assert len(md_files) == 1, "Should create exactly one markdown file"
        assert len(py_files) == 1, "Should create exactly one python file"
        
        # Check Python script is executable
        assert py_files[0].stat().st_mode & 0o111, "Script should be executable"
        print("  ✓ test_publish_with_url_creates_semi_auto passed")


def test_valid_config():
    """Test that valid config passes validation."""
    with tempfile.TemporaryDirectory() as tmpdir:
        adapter = SubstackEnhancedAdapter(
            {"credentials": {
                "publication_url": "https://test.substack.com",
                "api_key": "key"
            }},
            Path(tmpdir)
        )
        
        is_valid, errors = adapter.validate_config()
        assert is_valid, f"Should be valid, got errors: {errors}"
        assert len(errors) == 0, "Should have no errors"
        print("  ✓ test_valid_config passed")


def test_unknown_credential_fields():
    """Test that unknown fields are flagged."""
    with tempfile.TemporaryDirectory() as tmpdir:
        adapter = SubstackEnhancedAdapter(
            {"credentials": {
                "publication_url": "https://test.substack.com",
                "unknown_field": "value"
            }},
            Path(tmpdir)
        )
        
        is_valid, errors = adapter.validate_config()
        assert not is_valid, "Should not be valid with unknown fields"
        assert any("unknown" in e.lower() for e in errors), "Should mention unknown field"
        print("  ✓ test_unknown_credential_fields passed")


def smoke_test():
    """Run all smoke tests."""
    print("\nSubstack Adapter Smoke Tests")
    print("=" * 60)
    
    tests = [
        test_no_credentials,
        test_publication_url_only,
        test_full_credentials,
        test_invalid_publication_url,
        test_basic_render,
        test_render_no_cta,
        test_render_tags_formatting,
        test_publish_no_credentials_creates_manual_outbox,
        test_publish_with_url_creates_semi_auto,
        test_valid_config,
        test_unknown_credential_fields,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            print(f"  ✗ {test.__name__}: {e}")
            failed += 1
        except Exception as e:
            print(f"  ✗ {test.__name__}: {type(e).__name__}: {e}")
            failed += 1
    
    print("\n" + "=" * 60)
    print(f"Results: {passed} passed, {failed} failed")
    
    return failed == 0


if __name__ == "__main__":
    success = smoke_test()
    sys.exit(0 if success else 1)
