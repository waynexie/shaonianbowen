#!/usr/bin/env python3
"""Regression tests for Bowin three-tier routing and quality policy."""

from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
EVALUATOR = SKILL_ROOT / "scripts" / "evaluate_quality_gate.py"


def run_route(request: str) -> dict:
    process = subprocess.run(
        [sys.executable, str(EVALUATOR), "route", request],
        check=True,
        capture_output=True,
        text=True,
    )
    return json.loads(process.stdout)


def run_validation(evidence: dict) -> tuple[dict, int]:
    process = subprocess.run(
        [sys.executable, str(EVALUATOR), "validate", "--json", json.dumps(evidence, ensure_ascii=False)],
        check=False,
        capture_output=True,
        text=True,
    )
    return json.loads(process.stdout), process.returncode


def valid_evidence(tier: str) -> dict:
    return {
        "quality_tier": tier,
        "screenshot_checked": True,
        "detected_basic_failures": [],
        "production_gaps": [],
        "reference_sources": [],
        "component_resolution_checked": True,
        "registered_component_families": [],
    }


class QualityRouterTests(unittest.TestCase):
    def test_required_examples(self) -> None:
        cases = {
            "重新设计三版看看": "inspiration_draft",
            "在设置页新增一个切换项": "precision_draft",
            "把 B 版做成可上线正式稿": "production",
            "设计一个新的学习总结页": "inspiration_draft",
        }
        for request, expected in cases.items():
            with self.subTest(request=request):
                self.assertEqual(run_route(request)["quality_tier"], expected)

    def test_lookup_does_not_enter_generation_qa(self) -> None:
        result = run_route("这个页面长什么样")
        self.assertIsNone(result["quality_tier"])
        self.assertTrue(result["readonly"])
        dark_result = run_route("这个页面 dark mode 长什么样")
        self.assertIsNone(dark_result["quality_tier"])
        self.assertTrue(dark_result["readonly"])

    def test_precedence_and_existing_shell_lock(self) -> None:
        self.assertEqual(run_route("把重新设计的 B 版做成正式稿")["quality_tier"], "production")
        result = run_route("在已有设置页重新设计三版")
        self.assertEqual(result["quality_tier"], "inspiration_draft")
        self.assertTrue(result["locked_existing_shell"])
        self.assertEqual(run_route("把这个设置页做成高保真草稿")["quality_tier"], "precision_draft")


class UniversalBasicQaTests(unittest.TestCase):
    def test_every_basic_failure_blocks_every_tier(self) -> None:
        failures = [
            "unexpected_visible_overlap",
            "content_clipped_or_overflowing",
            "alignment_drift",
            "spacing_rhythm_failure",
            "safe_area_or_bottom_bar_occlusion",
            "key_entry_unreadable_or_icon_missing",
            "primary_task_or_focus_unclear",
            "locked_context_changed",
            "screenshot_not_checked",
        ]
        for tier in ("inspiration_draft", "precision_draft", "production"):
            for failure in failures:
                with self.subTest(tier=tier, failure=failure):
                    evidence = valid_evidence(tier)
                    evidence["detected_basic_failures"] = [failure]
                    result, code = run_validation(evidence)
                    self.assertNotEqual(code, 0)
                    self.assertIn(failure, result["blocking_failures"])

    def test_intentional_overlap_exclusions_pass(self) -> None:
        evidence = valid_evidence("inspiration_draft")
        evidence["excluded_overlap_pairs"] = [
            {"kind": "button_internal_icon"},
            {"kind": "text_over_media_with_legible_treatment"},
            {"kind": "popover_toast_mask_or_explicit_overlay"},
            {"kind": "inherited_component_decoration"},
            {"kind": "intentional_overlay"},
        ]
        result, code = run_validation(evidence)
        self.assertEqual(code, 0)
        self.assertTrue(result["passed"])

    def test_draft_gaps_report_but_production_gaps_block(self) -> None:
        gaps = [
            "token_binding_incomplete",
            "unregistered_new_componentization_gap",
            "dark_mode_not_verified",
        ]
        for tier in ("inspiration_draft", "precision_draft"):
            with self.subTest(tier=tier):
                evidence = valid_evidence(tier)
                evidence["production_gaps"] = gaps
                result, code = run_validation(evidence)
                self.assertEqual(code, 0)
                self.assertEqual(result["production_gaps"], sorted(gaps))
                self.assertTrue(result["must_not_claim_production"])

        evidence = valid_evidence("production")
        evidence["production_gaps"] = gaps
        result, code = run_validation(evidence)
        self.assertNotEqual(code, 0)
        self.assertEqual(len([item for item in result["blocking_failures"] if item.startswith("unresolved_production_gap:")]), 3)


class OptionAndReferenceTests(unittest.TestCase):
    def test_color_only_options_fail(self) -> None:
        evidence = valid_evidence("inspiration_draft")
        evidence["options"] = [
            {"design_thesis": "同一布局换绿色", "difference_axes": ["color_only"]},
            {"design_thesis": "同一布局换蓝色", "difference_axes": ["color_only"]},
            {"design_thesis": "同一布局换紫色", "difference_axes": ["color_only"]},
        ]
        result, code = run_validation(evidence)
        self.assertNotEqual(code, 0)
        self.assertFalse(result["option_difference_result"]["passed"])

    def test_meaningfully_different_options_pass(self) -> None:
        evidence = valid_evidence("inspiration_draft")
        evidence["options"] = [
            {"design_thesis": "先呈现身份与登录价值", "difference_axes": ["information_hierarchy"]},
            {"design_thesis": "从任务入口直接开始", "difference_axes": ["operation_path"]},
            {"design_thesis": "用连续叙事聚焦成长记录", "difference_axes": ["content_focus"]},
        ]
        result, code = run_validation(evidence)
        self.assertEqual(code, 0)
        self.assertTrue(result["option_difference_result"]["passed"])

    def test_reference_level_is_derived_from_real_sources(self) -> None:
        evidence = valid_evidence("inspiration_draft")
        evidence["reference_sources"] = [{"type": "product_memory", "name": "Apple News"}]
        result, _ = run_validation(evidence)
        self.assertEqual(result["reference_evidence_level"], "pattern_memory_reference")

        evidence["reference_sources"] = [{"type": "user_screenshot", "id": "shot-1"}]
        result, _ = run_validation(evidence)
        self.assertEqual(result["reference_evidence_level"], "visual_reference_checked")

    def test_visual_reference_overclaim_fails(self) -> None:
        evidence = valid_evidence("inspiration_draft")
        evidence["reference_sources"] = [{"type": "product_memory", "name": "Apple News"}]
        evidence["reference_evidence_level"] = "visual_reference_checked"
        result, code = run_validation(evidence)
        self.assertNotEqual(code, 0)
        self.assertIn("reference_evidence_overclaim", result["blocking_failures"])


class ForwardScenarioTests(unittest.TestCase):
    def test_profile_login_inspiration_keeps_shell_and_allows_one_axis_per_option(self) -> None:
        route = run_route("重新设计个人中心登录区，出三版看看")
        self.assertEqual(route["quality_tier"], "inspiration_draft")
        self.assertTrue(route["locked_existing_shell"])
        evidence = valid_evidence("inspiration_draft")
        evidence["production_gaps"] = ["dark_mode_not_verified"]
        evidence["options"] = [
            {"design_thesis": "身份信息先行", "difference_axes": ["information_hierarchy"]},
            {"design_thesis": "登录任务先行", "difference_axes": ["operation_path"]},
            {"design_thesis": "成长内容先行", "difference_axes": ["content_focus"]},
        ]
        result, code = run_validation(evidence)
        self.assertEqual(code, 0)
        self.assertTrue(result["passed"])


    def test_settings_precision_and_paywall_production_apply_different_gates(self) -> None:
        self.assertEqual(run_route("在设置页新增一个切换项")["quality_tier"], "precision_draft")
        precision = valid_evidence("precision_draft")
        precision["production_gaps"] = ["unregistered_new_componentization_gap"]
        result, code = run_validation(precision)
        self.assertEqual(code, 0)
        self.assertTrue(result["passed"])

        self.assertEqual(run_route("把 B 版付费弹窗做成可上线正式稿")["quality_tier"], "production")
        production = valid_evidence("production")
        production["production_gaps"] = ["dark_mode_not_verified"]
        result, code = run_validation(production)
        self.assertNotEqual(code, 0)
        self.assertFalse(result["passed"])


class AuthorityAndBoundaryTests(unittest.TestCase):
    def test_lookup_words_do_not_authorize_production(self) -> None:
        for request in ["有没有正式稿", "查一下可上线版本", "不要生成，只查正式稿", "介绍组件化设计规范", "正式稿", "有没有重新设计的版本"]:
            with self.subTest(request=request):
                result = run_route(request)
                self.assertTrue(result["readonly"])
                self.assertIsNone(result["quality_tier"])
                self.assertFalse(result["write_authorization"])

    def test_semantic_intent_resolves_mixed_wording(self) -> None:
        request = "有没有新版，帮我设计三版"
        result = run_route(request)
        self.assertTrue(result["readonly"])
        process = subprocess.run([sys.executable, str(EVALUATOR), "route", request, "--intent", "design_new"], check=True, capture_output=True, text=True)
        result = json.loads(process.stdout)
        self.assertEqual(result["quality_tier"], "inspiration_draft")
        self.assertFalse(result["write_authorization"])

    def test_registered_family_missing_blocks_all_tiers(self) -> None:
        for tier in ("inspiration_draft", "precision_draft", "production"):
            evidence = valid_evidence(tier)
            evidence["registered_component_families"] = [{"resolved_component_family": "NavigationBar"}]
            result, code = run_validation(evidence)
            self.assertNotEqual(code, 0)
            self.assertTrue(any("component_source_or_delivery_evidence_missing" in x for x in result["blocking_failures"]))
            evidence = valid_evidence(tier)
            evidence["production_gaps"] = ["required_instance_or_source_extension_unresolved"]
            result, code = run_validation(evidence)
            self.assertNotEqual(code, 0)
            self.assertIn("required_instance_or_source_extension_unresolved", result["blocking_failures"])

    def test_registered_family_with_source_and_instance_evidence_passes(self) -> None:
        evidence = valid_evidence("precision_draft")
        evidence["registered_component_families"] = [{
            "resolved_component_family": "NavigationBar",
            "source_component_or_instance_node_id": "557:5165",
            "delivered_instance_or_same_family_extension_node_id": "123:456",
            "component_property_or_variant_changes": [],
            "target_region_screenshot_check": True,
        }]
        result, code = run_validation(evidence)
        self.assertEqual(code, 0)
        self.assertTrue(result["passed"])
        self.assertFalse(result["complete_route_validation"])
        self.assertFalse(result["production_delivery_authorized"])

    def test_malformed_evidence_and_unknown_failures_fail_closed(self) -> None:
        for field, value in [("screenshot_checked", "false"), ("component_resolution_checked", 1), ("production_gaps", "none"), ("registered_component_families", {}), ("detected_basic_failures", ["unknown_failure"])]:
            evidence = valid_evidence("inspiration_draft")
            evidence[field] = value
            result, code = run_validation(evidence)
            self.assertNotEqual(code, 0, field)
            self.assertFalse(result["passed"])

    def test_quality_evaluation_is_only_a_declared_slice(self) -> None:
        result, code = run_validation(valid_evidence("production"))
        self.assertEqual(code, 0)
        self.assertEqual(result["result_scope"], "reported_quality_evidence_only")
        self.assertFalse(result["complete_route_validation"])
        self.assertTrue(result["must_not_claim_production"])


if __name__ == "__main__":
    unittest.main()
