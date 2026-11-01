#!/usr/bin/env python3
"""Regression checks for rule ownership, resolvable references and tier boundaries."""

from __future__ import annotations

import re
import json
import subprocess
import sys
import unittest
from pathlib import Path

import yaml

from evaluate_quality_gate import evaluate
from read_metadata_section import select


ROOT = Path(__file__).resolve().parents[1]
METADATA = ROOT / "references" / "metadata"


def load(name: str) -> dict:
    return yaml.safe_load((METADATA / name).read_text(encoding="utf-8"))


def resolve(ref: str):
    file, section = ref.split("#", 1)
    path = ROOT / file if file.startswith("references/") else METADATA / file
    return select(yaml.safe_load(path.read_text(encoding="utf-8")), section)


def evidence(tier: str) -> dict:
    return {
        "quality_tier": tier,
        "screenshot_checked": True,
        "detected_basic_failures": [],
        "production_gaps": [],
        "reference_sources": [],
        "component_resolution_checked": True,
        "registered_component_families": [],
    }


class BindingPolicyTests(unittest.TestCase):
    def setUp(self):
        self.validation = load("validation.yaml")
        self.routes = load("task-routes.yaml")
        self.policy = self.validation["minimum_token_binding_check"]

    def test_binding_consumers_share_one_enforcement_policy(self):
        references = [
            load("tokens.yaml")["source"]["binding_policy_ref"],
            self.routes["global_defaults"]["minimum_token_binding"]["enforcement_ref"],
            self.validation["bound_variable_check"]["enforcement_ref"],
            self.validation["bound_variable_check"]["applicability_ref"],
            self.validation["figma_design_system_gate_check"]["binding_policy_ref"],
            self.validation["radius_check"]["binding_policy_ref"],
            self.validation["failure_remediation"]["hard_stop_cases"]["token_binding_gap"]["enforcement_ref"],
        ]
        for ref in references:
            with self.subTest(ref=ref):
                self.assertEqual(resolve(ref), self.policy)
        self.assertNotIn("fallback", load("tokens.yaml")["source"])
        self.assertNotIn("required", self.validation["bound_variable_check"])
        self.assertNotIn("fail_condition", self.validation["bound_variable_check"])
        self.assertNotIn("enforcement_by_quality_tier", self.routes["global_defaults"]["minimum_token_binding"])

    def test_policy_covers_exactly_the_declared_quality_tiers(self):
        tiers = self.routes["global_defaults"]["quality_tier_routing"]["values"]
        outcomes = self.policy["enforcement_by_quality_tier"]
        self.assertEqual(set(outcomes), set(tiers))
        for tier in ("inspiration_draft", "precision_draft"):
            self.assertEqual(outcomes[tier]["outcome"], "record_production_gap")
        self.assertEqual(outcomes["production"]["outcome"], "block_unresolved_core_binding")

    def test_source_verification_and_formal_maintenance_are_not_draft_exemptions(self):
        self.assertEqual(self.policy["dependency_verification"]["unavailable"]["outcome"], "block_dependent_write")
        self.assertEqual(self.policy["formal_component_maintenance"]["outcome"], "block_unresolved_core_binding")
        allowed = self.validation["production_gaps_check"]["allowed_values"]
        self.assertNotIn("design_system_unavailable", allowed)
        self.assertNotIn("required_component_unavailable", allowed)
        self.assertEqual(
            resolve(self.policy["dependency_verification"]["component_policy_ref"]),
            self.validation["registered_component_family_gate_check"],
        )

    def test_both_binding_gap_kinds_follow_tier_outcome_in_evaluator(self):
        allowed = resolve(self.policy["gap_policy_ref"])["allowed_values"]
        for gap in self.policy["gap_mapping"].values():
            self.assertIn(gap, allowed)
            for tier, definition in self.policy["enforcement_by_quality_tier"].items():
                with self.subTest(gap=gap, tier=tier):
                    record = evidence(tier)
                    record["production_gaps"] = [gap]
                    result = evaluate(record)
                    self.assertEqual(result["passed"], definition["outcome"] == "record_production_gap")
                    self.assertFalse(result["production_delivery_authorized"])

    def test_binding_gaps_do_not_hide_component_or_visual_failures(self):
        for tier in ("inspiration_draft", "precision_draft"):
            for failure in ("registered_component_family_gate_failed", "locked_context_changed", "content_clipped_or_overflowing"):
                with self.subTest(tier=tier, failure=failure):
                    record = evidence(tier)
                    record["production_gaps"] = ["token_binding_incomplete"]
                    record["detected_basic_failures"] = [failure]
                    self.assertIn(failure, evaluate(record)["blocking_failures"])

    def test_unavailable_sources_cannot_be_reported_as_allowed_binding_gaps(self):
        for tier in self.policy["enforcement_by_quality_tier"]:
            for failure in ("design_system_unavailable", "required_component_unavailable"):
                with self.subTest(tier=tier, failure=failure):
                    record = evidence(tier)
                    record["production_gaps"] = [failure]
                    self.assertFalse(evaluate(record)["passed"])


class ReferenceAndEvidenceTests(unittest.TestCase):
    def test_nested_route_gates_resolve(self):
        validation = load("validation.yaml")
        for name, route in load("task-routes.yaml")["routes"].items():
            for gate in route.get("validation_gates", []):
                if "." in gate and " " not in gate:
                    with self.subTest(route=name, gate=gate):
                        self.assertIsNotNone(select(validation, gate))

    def test_settings_route_requires_registered_row_without_local_substitution(self):
        row = load("components.yaml")["components"]["SettingsRow"]
        route = load("task-routes.yaml")["routes"]["settings_modification"]
        self.assertEqual(row["node_id"], "7596:9566")
        self.assertTrue(row["required_instance"])
        self.assertEqual(row["fallback_policy"], "use_existing_instance_or_stop")
        self.assertIn("SettingsRow", route["must_use_components"])
        self.assertFalse(any("SettingsRow" in item for item in route["allowed_local_layout"]))
        self.assertTrue(any("PermissionSwitch" in item["name"] for item in row["live_variants"]))

    def test_settings_sources_match_route_purpose_without_losing_profile_alias(self):
        groups = load("source-frames.yaml")["source_groups"]
        frames = {frame["node_id"]: frame for group in groups.values() for frame in group.get("frames", [])}
        sheets = {"7469:4610", "7469:4668", "7469:6147", "7469:6243"}
        for node_id in sheets | {"7469:6019", "7469:6475"}:
            with self.subTest(node_id=node_id):
                frame = frames[node_id]
                self.assertEqual(frame["experience_profile"], "settings")
                self.assertIn("settings", frame["use_for"])
                self.assertIn("profile_mine", frame["use_for"])
                if node_id in sheets:
                    self.assertIn("settings_sheets", frame["use_for"])

    def test_settings_row_queries_resolve_one_registered_family(self):
        for query in ("SettingsRow", "SettingsRow_7596_9566"):
            with self.subTest(query=query):
                result = subprocess.run(
                    [sys.executable, str(ROOT / "scripts/query_runtime_index.py"), query,
                     "--kind", "component", "--intent", "locate", "--limit", "1"],
                    check=True, capture_output=True, text=True,
                )
                self.assertEqual(json.loads(result.stdout)["matches"][0]["node_id"], "7596:9566")

    def test_metadata_selector_handles_list_entries_without_ambiguity(self):
        self.assertEqual(select({"rows": [{"name": "first"}]}, "rows.0.name"), "first")
        self.assertEqual(select({"0": "dictionary key"}, "0"), "dictionary key")
        for path in ("rows.-1", "rows.1", "rows.first", "rows.0.missing"):
            with self.subTest(path=path), self.assertRaises(KeyError):
                select({"rows": [{"name": "first"}]}, path)

    def test_date_divider_reference_resolves_to_the_output_utility(self):
        policy = load("task-routes.yaml")["global_defaults"]["canvas_placement_policy"]
        target = resolve(policy["date_divider"]["pattern_ref"])
        self.assertEqual(target["node_role"], "date_divider_pattern")
        self.assertEqual(target["status"], "output_only")

    def test_local_yaml_fragment_references_resolve(self):
        paths = [ROOT / "SKILL.md", *sorted((ROOT / "references").rglob("*.md")), *sorted(METADATA.glob("*.yaml"))]
        pattern = r"(?<![\w/.-])((?:references/metadata/)?[A-Za-z0-9_-]+\.yaml#[A-Za-z0-9_.:-]+)"
        for path in paths:
            for ref in re.findall(pattern, path.read_text(encoding="utf-8")):
                with self.subTest(file=path.name, ref=ref):
                    self.assertIsNotNone(resolve(ref))

    def test_binding_check_reuses_the_shared_evidence_contract(self):
        validation = load("validation.yaml")
        shared = validation["pre_generation_checks"]["decision_records"]["evidence_reuse_contract"]
        self.assertEqual(resolve(validation["bound_variable_check"]["evidence_ref"]), shared)
        self.assertEqual(shared["selection"], "union_of_selected_profile_fields_and_applicable_gate_fields_only")
        records = validation["pre_generation_checks"]["decision_records"]
        self.assertNotIn("required_by_profile", records)
        self.assertEqual(resolve(records["required_by_profile_ref"]), load("task-routes.yaml")["route_profiles"])

    def test_icon_fallback_has_registered_candidate_sources(self):
        catalog = load("components.yaml")["components"]
        for name in ("Icon16", "Icon20", "Icon24"):
            self.assertEqual(catalog[name]["fallback_policy"], "use_iconsax_candidate_or_stop")
        candidates = [node for node in load("source-registry.yaml")["nodes"] if "iconsax_candidate" in node.get("use_for", [])]
        self.assertTrue(candidates)
        self.assertTrue(all(node.get("node_id") for node in candidates))
        scope = load("task-routes.yaml")["global_defaults"]["persistent_write_scope"]
        self.assertIn("formal_component_maintenance_scope", scope)

    def test_migrated_observations_do_not_claim_live_verification(self):
        catalog = load("components.yaml")["components"]
        for name in ("AudioProgressControl", "CommentCell", "VoiceCommentCell"):
            observations = catalog[name]["historical_measurements"]
            self.assertEqual(observations["use_policy"], "locator_hint_only_verify_before_use")
            self.assertNotIn("verified_at", observations)


if __name__ == "__main__":
    unittest.main()
