#!/usr/bin/env python3
"""Regression tests for compact routing, lookup and cache freshness."""

from __future__ import annotations

import json
import datetime as dt
import copy
import re
import tempfile
from unittest.mock import patch
import subprocess
import sys
import unittest
from pathlib import Path

import yaml


SKILL_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = SKILL_ROOT / "scripts"
CACHE_ENTRIES = yaml.safe_load((SKILL_ROOT / "references/metadata/visual-cache.yaml").read_text())["entries"]
PROFILE_CACHE = next(entry for entry in CACHE_ENTRIES if entry["cache_id"] == "screen_profile_normal_light")
NOW = (dt.datetime.fromisoformat(PROFILE_CACHE["captured_at"]) + dt.timedelta(days=1)).isoformat()


def run_json(*args: str) -> tuple[dict, int]:
    process = subprocess.run([sys.executable, *args], check=True, capture_output=True, text=True)
    return json.loads(process.stdout), len(process.stdout.encode("utf-8"))


class RuntimeIndexTests(unittest.TestCase):
    def test_indexes_are_current(self) -> None:
        subprocess.run(
            [sys.executable, str(SCRIPTS / "build_runtime_indexes.py"), "--check"],
            check=True,
            capture_output=True,
            text=True,
        )

    def test_exact_cached_screen_lookup_stays_small_and_skips_live(self) -> None:
        result, size = run_json(
            str(SCRIPTS / "query_runtime_index.py"),
            str(PROFILE_CACHE["source_node_id"]),
            "--kind",
            "screen",
            "--state",
            "normal_user_light",
            "--limit",
            "1",
            "--now",
            NOW,
        )
        self.assertLessEqual(size, 10_240)
        self.assertEqual(result["matches"][0]["node_id"], str(PROFILE_CACHE["source_node_id"]))
        self.assertFalse(result["matches"][0]["live_figma_required"])
        self.assertEqual(result["matches"][0]["cache"][0]["freshness"], "fresh")
        self.assertEqual(result["requested_appearance_mode"], "light_default")
        self.assertEqual(result["matches"][0]["cache"][0]["appearance_mode"], "light_default")
        self.assertEqual(result["matches"][0]["delivery_status"], "verified_cache_ready")

    def test_unspecified_visual_lookup_defaults_to_verified_light(self) -> None:
        result, _ = run_json(
            str(SCRIPTS / "query_runtime_index.py"),
            str(PROFILE_CACHE["source_node_id"]),
            "--kind",
            "screen",
            "--limit",
            "1",
            "--now",
            NOW,
        )
        match = result["matches"][0]
        self.assertEqual(result["requested_appearance_mode"], "light_default")
        self.assertEqual(result["requested_mode_source"], "default_unspecified_current_turn")
        self.assertFalse(match["live_figma_required"])
        self.assertTrue(all(cache["appearance_mode"] == "light_default" for cache in match["cache"]))

    def test_explicit_dark_lookup_never_uses_light_cache(self) -> None:
        result, _ = run_json(
            str(SCRIPTS / "query_runtime_index.py"),
            str(PROFILE_CACHE["source_node_id"]),
            "--mode",
            "dark",
            "--kind",
            "screen",
            "--limit",
            "1",
            "--now",
            NOW,
        )
        match = result["matches"][0]
        self.assertEqual(result["requested_appearance_mode"], "dark")
        self.assertNotIn("cache", match)
        self.assertTrue(match["live_figma_required"])
        self.assertEqual(match["delivery_status"], "live_mode_verification_required")
        self.assertEqual(match["unavailable_status_if_live_fails"], "requested_appearance_unavailable")

    def test_latest_always_forces_live(self) -> None:
        result, _ = run_json(
            str(SCRIPTS / "query_runtime_index.py"),
            "首页",
            "--kind",
            "screen",
            "--state",
            "light_default",
            "--limit",
            "1",
            "--latest",
            "--now",
            NOW,
        )
        self.assertTrue(result["matches"][0]["live_figma_required"])
        self.assertEqual(result["matches"][0]["live_fallback_reason"], "latest_or_realtime_requested")

    def test_render_state_mismatch_forces_live(self) -> None:
        result, _ = run_json(
            str(SCRIPTS / "query_runtime_index.py"),
            str(PROFILE_CACHE["source_node_id"]),
            "--kind",
            "screen",
            "--state",
            "dark",
            "--limit",
            "1",
            "--now",
            NOW,
        )
        self.assertTrue(result["matches"][0]["live_figma_required"])
        self.assertEqual(result["matches"][0]["live_fallback_reason"], "render_state_or_appearance_mode_mismatch_or_missing")

    def test_business_page_count_regression_is_dynamic_and_scope_labeled(self) -> None:
        source = yaml.safe_load((SKILL_ROOT / "references" / "metadata" / "source-frames.yaml").read_text(encoding="utf-8"))
        expected_ids = {
            str(frame["node_id"])
            for group in source.get("source_groups", {}).values()
            for frame in group.get("frames", [])
            if frame.get("node_role") == "screen_frame"
            and frame.get("exportable") is True
            and frame.get("status", "active") not in {"stale", "missing"}
        }
        runtime = json.loads((SKILL_ROOT / "references" / "runtime" / "lookup-index.json").read_text(encoding="utf-8"))
        runtime_ids = {
            str(record["node_id"])
            for record in runtime.get("records", [])
            if record.get("kind") == "screen" and str(record.get("node_id")) in expected_ids
        }
        self.assertGreater(len(expected_ids), 0)
        self.assertEqual(runtime_ids, expected_ids)

        ambiguity, _ = run_json(
            str(SCRIPTS / "read_metadata_section.py"),
            "task-routes.yaml",
            "global_defaults.semantic_ambiguity_routing",
        )
        example = ambiguity["value"]["regression_examples"][0]
        self.assertEqual(example["query"], "目前共有多少页面")
        self.assertIn("source-frames.yaml", example["primary_authority"])
        self.assertIn("hardcode_expected_count", example["forbidden"])

    def test_figma_page_count_requires_document_root_inventory(self) -> None:
        result, size = run_json(
            str(SCRIPTS / "read_execution_profile.py"),
            "profile",
            "lookup_profile",
            "--compact",
        )
        self.assertLessEqual(size, 10_240)
        policy, _ = run_json(str(SCRIPTS / "read_metadata_section.py"), "task-routes.yaml", "global_defaults.semantic_ambiguity_routing")
        contract = policy["value"]["technical_page_count_contract"]
        self.assertEqual(contract["authority"], "live Figma target-file Document root")
        self.assertIn(
            "a single Page or Canvas subtree",
            contract["rejected_evidence"],
        )
        self.assertEqual(
            contract["fallback_status"],
            "figma_document_page_inventory_unavailable",
        )
        validation = run_json(str(SCRIPTS / "read_metadata_section.py"), "validation.yaml", "semantic_authority_ambiguity_check")[0]["value"]
        self.assertIn(
            "a Figma Page or Canvas count is reported without an auditable Document-root page inventory",
            validation["fail_condition"],
        )

    def test_invalid_limit_is_rejected(self) -> None:
        process = subprocess.run(
            [sys.executable, str(SCRIPTS / "query_runtime_index.py"), "首页", "--limit", "-1"],
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertNotEqual(process.returncode, 0)
        self.assertIn("--limit must be between 1 and 20", process.stderr)

    def test_chinese_component_alias_resolves(self) -> None:
        result, size = run_json(
            str(SCRIPTS / "query_runtime_index.py"),
            "导航栏",
            "--kind",
            "component",
            "--limit",
            "1",
            "--now",
            NOW,
        )
        self.assertLessEqual(size, 10_240)
        self.assertEqual(result["matches"][0]["name"], "NavigationBar")

    def test_project_asset_alias_resolves(self) -> None:
        result, _ = run_json(
            str(SCRIPTS / "query_runtime_index.py"),
            "星星人",
            "--kind",
            "asset",
            "--limit",
            "2",
            "--now",
            NOW,
        )
        self.assertGreaterEqual(result["count"], 2)
        self.assertTrue({item["node_id"] for item in result["matches"]} & {"224:12087", "2373:5101"})

    def test_two_stage_generation_contract_is_compact(self) -> None:
        result, size = run_json(
            str(SCRIPTS / "read_metadata_section.py"),
            "task-routes.yaml",
            "global_defaults.speed_tier_routing.smart_two_stage_delivery",
        )
        self.assertLessEqual(size, 10_240)
        self.assertTrue(result["value"]["enabled"])
        self.assertEqual(result["value"]["stage_1"]["tier"], "fast_visual_exploration")
        self.assertEqual(result["value"]["stage_2"]["tier"], "productionization")

    def test_quality_tier_is_compiled_and_compact(self) -> None:
        result, size = run_json(
            str(SCRIPTS / "read_execution_profile.py"),
            "quality",
            "inspiration_draft",
            "--compact",
        )
        self.assertLessEqual(size, 10_240)
        self.assertIn("universal_basic_visual_check", result["definition"]["required"])
        self.assertIn("dark_mode_not_verified", result["definition"]["non_blocking_production_gaps"])

    def test_visual_delivery_contract_is_machine_readable(self) -> None:
        result, size = run_json(
            str(SCRIPTS / "read_metadata_section.py"),
            "task-routes.yaml",
            "global_defaults.visual_query_delivery",
        )
        self.assertLessEqual(size, 10_240)
        contract = result["value"]
        self.assertEqual(contract["failure_status"], "visual_attachment_unavailable")
        self.assertIn("final_attachment_markdown", contract["required_delivery_evidence"])




    def test_visual_attachment_validator_requires_platform_delivery_url(self) -> None:
        image_path = SKILL_ROOT / PROFILE_CACHE["asset_path"]
        result, _ = run_json(
            str(SCRIPTS / "validate_visual_attachment.py"),
            str(image_path),
            "--label",
            "首页",
        )
        self.assertTrue(result["valid"])
        self.assertEqual(result["visual_attachment_format"], "png")
        self.assertFalse(result["delivery_ready"])
        self.assertIsNone(result["markdown_image"])
        self.assertIn("delivery_url_missing", result["delivery_errors"])

    def test_visual_attachment_validator_returns_public_markdown(self) -> None:
        image_path = SKILL_ROOT / PROFILE_CACHE["asset_path"]
        delivery_url = "https://example.invalid/workspace/profile-normal.png"
        result, _ = run_json(
            str(SCRIPTS / "validate_visual_attachment.py"),
            str(image_path),
            "--label",
            "首页",
            "--delivery-url",
            delivery_url,
        )
        self.assertTrue(result["delivery_ready"])
        self.assertEqual(result["markdown_image"], f"![首页]({delivery_url})")

    def test_visual_attachment_validator_rejects_missing_image(self) -> None:
        missing = SKILL_ROOT / "missing-preview.png"
        process = subprocess.run(
            [sys.executable, str(SCRIPTS / "validate_visual_attachment.py"), str(missing)],
            check=False,
            capture_output=True,
            text=True,
        )
        result = json.loads(process.stdout)
        self.assertNotEqual(process.returncode, 0)
        self.assertEqual(result["status"], "visual_attachment_unavailable")
        self.assertIn("file_missing", result["errors"])

    def test_visual_attachment_validator_rejects_path_outside_allowed_root(self) -> None:
        image_path = SKILL_ROOT / PROFILE_CACHE["asset_path"]
        process = subprocess.run(
            [
                sys.executable,
                str(SCRIPTS / "validate_visual_attachment.py"),
                str(image_path),
                "--allowed-root",
                str(SKILL_ROOT / "references"),
            ],
            check=False,
            capture_output=True,
            text=True,
        )
        result = json.loads(process.stdout)
        self.assertNotEqual(process.returncode, 0)
        self.assertIn("path_outside_allowed_root", result["errors"])


class PackageIntegrityTests(unittest.TestCase):
    def test_authority_yaml_has_no_duplicate_keys(self) -> None:
        class UniqueLoader(yaml.SafeLoader):
            pass
        def mapping(loader, node, deep=False):
            pairs = loader.construct_pairs(node, deep=deep)
            result = {}
            for key, value in pairs:
                if key in result:
                    raise ValueError(f"duplicate YAML key: {key}")
                result[key] = value
            return result
        UniqueLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, mapping)
        for path in (SKILL_ROOT / "references/metadata").glob("*.yaml"):
            self.assertIsInstance(yaml.load(path.read_text(), Loader=UniqueLoader), dict)

    def test_scope_and_context_contracts_remain_distinct(self) -> None:
        routes = yaml.safe_load((SKILL_ROOT / "references/metadata/task-routes.yaml").read_text())
        validation = yaml.safe_load((SKILL_ROOT / "references/metadata/validation.yaml").read_text())
        scope = routes["global_defaults"]["persistent_write_scope"]
        self.assertIn("formal_component_maintenance_scope", scope)
        self.assertIn("scene_index_maintenance_scope", scope)
        strategy = routes["global_defaults"]["context_strategy_routing"]
        self.assertEqual(strategy["default_by_delivery"]["new_page_or_production_native_output"], "direct_native_construction")
        self.assertEqual(strategy["default_by_delivery"]["visible_draft_or_multi_option"], "source_locked_visual_draft")
        self.assertIn("selected_context_strategy_check", routes["route_profiles"]["local_mutation_profile"]["required_fields"])
        decision = validation["pre_generation_checks"]["decision_records"]
        self.assertEqual(decision["required_by_profile_ref"], "task-routes.yaml#route_profiles")
        self.assertNotIn("required_by_profile", decision)

    def test_scene_references_have_single_source_and_preserve_family_links(self) -> None:
        from build_runtime_indexes import build_lookup_index, load_yaml, SOURCE_FILES
        documents = {name: load_yaml(path) for name, path in SOURCE_FILES.items()}
        index = build_lookup_index(documents)
        frames = {str(f["node_id"]): f for g in documents["source_frames"]["source_groups"].values() for f in g["frames"]}
        for scene in documents["scene_index"]["screens"]:
            self.assertEqual(set(scene), {"node_id", "component_families"})
            self.assertIn(str(scene["node_id"]), frames)
        self.assertTrue(all(record["node_id"] != "None" for record in index["records"]))
        self.assertTrue(all(record["node_id"] or record.get("locator_role") == "unresolved" for record in index["records"]))
        self.assertTrue(all(not term.startswith("[") and term != "None" for record in index["records"] for term in record["terms"]))
        by_name = {record["name"]: record for record in index["records"] if record["kind"] == "component"}
        self.assertEqual(by_name["BottomBar"]["locator_role"], "unresolved")
        self.assertIsNone(by_name["BottomBar"]["node_id"])
        self.assertTrue(any(record["node_id"] == by_name["BottomBar"]["legacy_node_id"] and record["status"] == "active" for record in index["records"]))
        malformed = copy.deepcopy(documents)
        malformed["scene_index"]["screens"][0]["node_id"] = "missing:screen"
        with self.assertRaisesRegex(ValueError, "scene screen reference"):
            build_lookup_index(malformed)

    def test_policy_is_compiled_from_authority(self) -> None:
        from build_runtime_indexes import build_execution_index, load_yaml, SOURCE_FILES
        documents = {name: load_yaml(path) for name, path in SOURCE_FILES.items()}
        documents["validation"]["universal_basic_visual_qa_check"]["universal_blocking_failures"].append("fixture_new_failure")
        result = build_execution_index(documents)
        self.assertIn("fixture_new_failure", result["quality_policy"]["basic_failures"])
        self.assertEqual(result["quality_policy"]["production_gaps"], documents["validation"]["production_gaps_check"]["allowed_values"])
        self.assertEqual(documents["validation"]["gate_level_check"]["levels_ref"], "task-routes.yaml#gate_levels")
        self.assertNotIn("levels", documents["validation"]["gate_level_check"])

    def test_markdown_and_metadata_file_references_exist(self) -> None:
        paths = [SKILL_ROOT / "SKILL.md", *sorted((SKILL_ROOT / "references").rglob("*.md")), *sorted((SKILL_ROOT / "references/metadata").glob("*.yaml"))]
        for path in paths:
            for match in re.finditer(r"(?<![\w/.-])((?:references/|scripts/|metadata/|assets/)[A-Za-z0-9_./-]+\.(?:md|yaml|py|json|png))", path.read_text()):
                ref = match.group(1)
                target = SKILL_ROOT / ("references/" + ref if ref.startswith("metadata/") else ref)
                self.assertTrue(target.is_file(), f"{path.name}: missing {ref}")

    def test_markdown_section_references_exist(self) -> None:
        for path in [SKILL_ROOT / "SKILL.md", *sorted((SKILL_ROOT / "references").rglob("*.md")), *sorted((SKILL_ROOT / "references/metadata").glob("*.yaml"))]:
            for match in re.finditer(r"((?:references/)?[A-Za-z0-9_-]+\.md) > ([^`\n]+)", path.read_text()):
                ref, heading = match.groups()
                target = SKILL_ROOT / ref if ref.startswith("references/") or ref == "SKILL.md" else SKILL_ROOT / "references" / ref
                self.assertTrue(target.is_file(), f"missing section file {ref}")
                headings = [line.lstrip("# ").strip() for line in target.read_text().splitlines() if line.startswith("#")]
                if heading.startswith("profile_id:"):
                    profile = heading.split()[1].strip("`'\"")
                    self.assertIn(f"profile_id: {profile}", target.read_text())
                else:
                    self.assertTrue(any(heading.strip().startswith(h) for h in headings), f"{path.name}: {ref} > {heading}")

    def test_document_gate_names_are_real(self) -> None:
        gates = yaml.safe_load((SKILL_ROOT / "references/metadata/validation.yaml").read_text())
        for path in (SKILL_ROOT / "references").glob("*.md"):
            for name in re.findall(r"`([a-z][a-z0-9_]*_check)`", path.read_text()):
                self.assertIn(name, gates, f"{path.name}: unknown gate {name}")

    def test_cache_time_edges_and_missing_assets(self) -> None:
        from runtime_support import cache_freshness, cache_asset_exists
        entry = dict(PROFILE_CACHE)
        captured = dt.datetime.fromisoformat(entry["captured_at"])
        self.assertEqual(cache_freshness(entry, captured - dt.timedelta(seconds=1)), "future")
        self.assertEqual(cache_freshness(entry, captured), "fresh")
        self.assertEqual(cache_freshness(entry, captured + dt.timedelta(days=entry["max_age_days"])), "expired")
        entry["captured_at"] = "not-a-time"
        self.assertEqual(cache_freshness(entry, captured), "invalid")
        self.assertFalse(cache_asset_exists({"asset_path": "assets/missing.png"}))
        self.assertTrue(cache_asset_exists(PROFILE_CACHE))

    def test_index_loader_rebuilds_once_and_rejects_invalid_output(self) -> None:
        import runtime_support as support
        from unittest.mock import Mock
        expected = {name: support.digest(support.SOURCE_FILES[name]) for name in support.INDEX_SOURCES["lookup"]}
        # All test files stay under this Skill's local runtime directory.
        with tempfile.TemporaryDirectory(dir=SKILL_ROOT / "references/runtime") as directory:
            index_path = Path(directory) / "lookup-index.json"
            index_path.write_text("partial json")
            def rebuild(*args, **kwargs):
                index_path.write_text(json.dumps({"generated_from": expected, "records": []}))
            with patch.object(support, "RUNTIME", Path(directory)), patch.object(support.subprocess, "run", side_effect=rebuild) as process:
                self.assertEqual(support.load_current_index("lookup")["records"], [])
                self.assertEqual(process.call_count, 1)
                support.load_current_index("lookup")
                self.assertEqual(process.call_count, 1)
            index_path.write_text("[]")
            with patch.object(support, "RUNTIME", Path(directory)), patch.object(support.subprocess, "run", Mock()) as process:
                with self.assertRaises(ValueError):
                    support.load_current_index("lookup")
                self.assertEqual(process.call_count, 1)

    def test_query_intents_keep_write_and_dark_evidence_separate(self) -> None:
        for intent, live in [("locate", False), ("visualize", False), ("write", True)]:
            result, size = run_json(str(SCRIPTS / "query_runtime_index.py"), str(PROFILE_CACHE["source_node_id"]), "--intent", intent, "--compact", "--now", NOW)
            self.assertEqual(result["matches"][0]["live_figma_required"], live)
            self.assertLess(size, 10240)
        result, _ = run_json(str(SCRIPTS / "query_runtime_index.py"), str(PROFILE_CACHE["source_node_id"]), "--mode", "dark", "--now", NOW)
        self.assertTrue(result["matches"][0]["live_figma_required"])
        self.assertNotIn("cache", result["matches"][0])


if __name__ == "__main__":
    unittest.main()
