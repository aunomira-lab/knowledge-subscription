#!/usr/bin/env python3
"""
测试脚本: report_generator.py V2 核心功能测试
运行: pytest tests/test_report_generator_v2.py -v
任务ID: c74f6491
"""
import sys
from pathlib import Path

APP_DIR = Path("/home/AgentAdmin/.hermes/shared/dev-team/projects/knowledge-subscription/app")
sys.path.insert(0, str(APP_DIR))

from report_generator import ReportGeneratorV2, QualityGate, load_data_sources


def test_load_data_sources():
    ds = load_data_sources()
    assert "meta" in ds
    assert "evidence_rating_rules" in ds
    assert "banned_keywords" in ds
    assert "quality_gates" in ds
    assert "content_structures" in ds
    print("✓ data_sources.json 结构完整")


def test_quality_gate_banned():
    ds = load_data_sources()
    qg = QualityGate(ds)
    clean = "这是高端深度内容，包含方法论、框架和可复用资产"
    r = qg.check_banned(clean)
    assert r["passed"] is True
    assert r["score"] == 1.0
    assert len(r["hits"]) == 0

    dirty = "AI只会聊天，普通人今晚就能试，快来学"
    r2 = qg.check_banned(dirty)
    assert r2["passed"] is False
    assert r2["score"] == 0.0
    assert len(r2["hits"]) > 0
    print("✓ 禁止词检测通过")


def test_quality_gate_evidence():
    ds = load_data_sources()
    qg = QualityGate(ds)
    text = (
        "Substack 官方 2026 年 5 月数据 https://on.substack.com \n"
        "增长率 45%\n"
        "CB Insights State of AI 2026 报告显示\n"
        "适用于企业团队，不适合个人玩家"
    )
    r = qg.check_evidence_gate(text)
    assert r["passed"] is True
    assert r["score"] >= 3
    print("✓ 证据门检测通过")


def test_quality_gate_depth():
    ds = load_data_sources()
    qg = QualityGate(ds)
    text = (
        "本文提供四段式SOP框架：结构化原料→生成初稿→质量审查→资产沉淀\n"
        "适用于B2B SaaS团队，反例：不适合个人玩家\n"
        "异常处理：当AI产生幻觉时需要人工确认\n"
        "```json\n{\"template\": \"value\"}\n```\n"
        "模板清单字段表"
    )
    r = qg.check_depth_gate(text)
    assert r["passed"] is True
    assert r["score"] >= 3
    print("✓ 深度门检测通过")


def test_quality_gate_asset():
    ds = load_data_sources()
    qg = QualityGate(ds)
    text = (
        "本期交付物包含模板、清单和字段表\n"
        "```markdown\n- [ ] 检查1\n- [ ] 检查2\n```\n"
        "人工确认环节：部分内容不能自动化\n"
        "版本 v2.0，更新时间 2026-06-01"
    )
    r = qg.check_asset_gate(text)
    assert r["passed"] is True
    assert r["score"] >= 3
    print("✓ 资产门检测通过")


def test_quality_gate_business():
    ds = load_data_sources()
    qg = QualityGate(ds)
    text = (
        "定价 ¥99/月订阅\n"
        "目标用户为B2B SaaS团队\n"
        "风险提示：本文不构成投资建议，不承诺稳赚"
    )
    r = qg.check_business_gate(text)
    assert r["passed"] is True
    assert r["score"] >= 3
    print("✓ 商业门检测通过")


def test_generator_runs():
    gen = ReportGeneratorV2()
    result = gen.run()
    assert result["overall_passed"] is True
    assert result["total_score"] >= 28
    assert result["score_pct"] >= 80
    assert len(result["reports"]) == 2
    for p in result["reports"]:
        assert Path(p).exists()
    print("✓ 生成器全流程通过")


def test_generated_content_quality():
    gen = ReportGeneratorV2()
    r1 = gen.generate_report_1_workflow_sop()
    r2 = gen.generate_report_2_knowledge_asset()
    q1 = gen.qg.run_all(r1)
    q2 = gen.qg.run_all(r2)
    assert q1["overall_passed"] is True
    assert q2["overall_passed"] is True
    assert q1["score_pct"] >= 70
    assert q2["score_pct"] >= 70
    print("✓ 生成内容质量检查通过")


if __name__ == "__main__":
    test_load_data_sources()
    test_quality_gate_banned()
    test_quality_gate_evidence()
    test_quality_gate_depth()
    test_quality_gate_asset()
    test_quality_gate_business()
    test_generator_runs()
    test_generated_content_quality()
    print("\n✅ 所有测试通过！")
