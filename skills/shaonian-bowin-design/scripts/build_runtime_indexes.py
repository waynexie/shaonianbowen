#!/usr/bin/env python3
"""Compile small, deterministic runtime indexes from the Skill authority YAML."""

from __future__ import annotations

import argparse
import fcntl
import json
import os
import tempfile
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Iterable

import yaml


from runtime_support import SKILL_ROOT, METADATA, RUNTIME, SOURCE_FILES, INDEX_SOURCES, digest

LOCK_FILE = RUNTIME / ".build.lock"


def load_yaml(path: Path) -> dict[str, Any]:
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def unique(values: Iterable[Any]) -> list[Any]:
    result: list[Any] = []
    for value in values:
        if value is None or value == "":
            continue
        if isinstance(value, (list, tuple)):
            candidates = unique(value)
        else:
            candidates = [value]
        for candidate in candidates:
            if candidate not in result:
                result.append(candidate)
    return result


def normalize_terms(values: Iterable[Any]) -> list[str]:
    return [str(value).strip() for value in unique(values) if str(value).strip()]


def build_lookup_index(documents: dict[str, dict[str, Any]]) -> dict[str, Any]:
    source_frames = documents["source_frames"]
    source_registry = documents["source_registry"]
    components = documents["components"]
    visual_cache = documents["visual_cache"]
    frames_by_node = {}
    for group_id, group in source_frames.get("source_groups", {}).items():
        for frame in group.get("frames", []):
            node_id = str(frame["node_id"])
            if node_id in frames_by_node:
                raise ValueError(f"duplicate source frame: {node_id}")
            frames_by_node[node_id] = frame
    scene_by_node = {}
    for scene in documents["scene_index"].get("screens", []):
        node_id = str(scene["node_id"])
        if node_id not in frames_by_node or node_id in scene_by_node:
            raise ValueError(f"missing or duplicate scene screen reference: {node_id}")
        if set(scene) - {"node_id", "component_families"}:
            raise ValueError(f"duplicated source fields in scene: {node_id}")
        family_ids = {str(ref["id"]) for ref in scene.get("component_families", [])}
        if family_ids != set(map(str, frames_by_node[node_id].get("component_family_ids", []))):
            raise ValueError(f"scene family references disagree with source: {node_id}")
        scene_by_node[node_id] = scene

    navigation_by_node = {}
    for scene in documents["scene_index"].get("scene_navigation", []):
        navigation_by_node.setdefault(str(scene["source_screen_id"]), []).append(scene)

    gallery_by_screen: dict[str, list[dict[str, Any]]] = {}
    gallery_by_family: dict[str, list[dict[str, Any]]] = {}
    for group in documents["scene_index"].get("variant_gallery", {}).get("groups", []):
        summary = {
            "id": str(group["id"]),
            "name": group.get("name"),
            "variant_count": group.get("row_count", len(group.get("rows", []))),
            "instance_count": group.get("instance_count"),
            "viewport_width": group.get("viewport_width", 390),
        }
        for screen_id in group.get("source_screen_ids", []):
            gallery_by_screen.setdefault(str(screen_id), []).append(summary)
        for variant in group.get("variant_rows", []):
            gallery_by_family.setdefault(str(variant["family_id"]), []).append({
                "gallery_id": summary["id"],
                "instance_id": str(variant["instance_id"]),
                "card_id": str(variant["card_id"]),
                "variant_master_id": str(variant["variant_master_id"]),
                "variant_name": variant.get("variant_name"),
                "viewport_width": 390,
            })

    cache_by_node: dict[str, list[dict[str, Any]]] = {}
    for entry in visual_cache.get("entries", []):
        cache_by_node.setdefault(str(entry.get("source_node_id")), []).append(
            {
                "cache_id": entry.get("cache_id"),
                "asset_path": entry.get("asset_path"),
                "render_state": entry.get("render_state"),
                "appearance_mode": entry.get("appearance_mode"),
                "captured_at": entry.get("captured_at"),
                "cache_status": entry.get("cache_status"),
                "max_age_days": entry.get("max_age_days"),
            }
        )

    records: list[dict[str, Any]] = []
    seen: set[tuple[str, str]] = set()

    def add_record(record: dict[str, Any]) -> None:
        node_id = record.get("node_id")
        key = (str(record.get("kind")), str(node_id or record.get("name", "")))
        if (not node_id and record.get("kind") != "component") or key in seen:
            return
        seen.add(key)
        navigation = navigation_by_node.get(key[1], []) if record.get("kind") == "screen" else []
        record["terms"] = normalize_terms([record.pop("terms", []), [s["name"] for s in navigation]])
        if navigation:
            record["scene_navigation"] = navigation
        if record.get("kind") == "screen" and key[1] in gallery_by_screen:
            record["scene_variant_galleries"] = gallery_by_screen[key[1]]
        if record.get("kind") == "component" and key[1] in gallery_by_family:
            record["scene_variant_rows"] = gallery_by_family[key[1]]
        record["use_for"] = normalize_terms(record.get("use_for", []))
        record["cache"] = cache_by_node.get(key[1], [])
        if record.get("kind") == "screen" and (key[1] in scene_by_node or navigation or key[1] in gallery_by_screen):
            scene = scene_by_node.get(key[1], {})
            refs = list(scene.get("component_families", []))
            for item in navigation:
                family_id = item.get("component_family_id")
                if family_id:
                    refs.append({
                        "id": family_id,
                        "name": item.get("component_family_name"),
                        "source_instance_id": item.get("source_instance_id"),
                        "example_instance_id": item.get("example_instance_id"),
                        "variant_gallery_id": item.get("variant_gallery_id"),
                    })
            for group in documents["scene_index"].get("variant_gallery", {}).get("groups", []):
                if key[1] not in [str(value) for value in group.get("source_screen_ids", [])]:
                    continue
                for variant in group.get("variant_rows", []):
                    family_id = str(variant["family_id"])
                    if not any(str(ref.get("id")) == family_id for ref in refs):
                        refs.append({
                            "id": family_id,
                            "name": variant.get("family_name"),
                            "variant_gallery_id": str(group["id"]),
                        })
            record["scene_component_refs"] = refs
            record["scene_index_ref"] = "references/metadata/scene-index.yaml"
            record["component_reference_role"] = "locator_only_verify_live_master_before_write"
        records.append(record)

    for group_id, group in source_frames.get("source_groups", {}).items():
        for frame in group.get("frames", []):
            is_primary = str(frame.get("node_id")) == str(group.get("primary_display_frame"))
            add_record(
                {
                    "kind": "screen",
                    "node_id": str(frame.get("node_id")),
                    "name": frame.get("name"),
                    "terms": [
                        frame.get("name"),
                        frame.get("aliases", []),
                        frame.get("use_for", []),
                        str(group_id),
                        group.get("name"),
                        group.get("aliases", []),
                    ],
                    "aliases": normalize_terms(frame.get("aliases", [])),
                    "use_for": frame.get("use_for", []),
                    "source_group_id": str(group_id),
                    "source_group_name": group.get("name"),
                    "source_group_exportable": group.get("exportable", False),
                    "is_primary_display_frame": is_primary,
                    "experience_profile": frame.get("experience_profile"),
                    "state_role": frame.get("state_role"),
                    "authority_role": frame.get("authority_role"),
                    "default_generation_source": frame.get("default_generation_source", True),
                    "exportable": frame.get("exportable", False),
                    "status": frame.get("status", "active"),
                }
            )

    for node in source_registry.get("nodes", []):
        role = str(node.get("node_role", "source"))
        kind = "asset" if any("asset" in str(value) or "icon" in str(value) or "expression" in str(value) for value in node.get("use_for", [])) else "source"
        if role == "screen_frame":
            kind = "screen"
        source_aliases = unique(source_registry.get("lookup_aliases_by_use_for", {}).get(str(value), []) for value in node.get("use_for", []))
        add_record(
            {
                "kind": kind,
                "node_id": str(node.get("node_id")),
                "name": node.get("name"),
                "terms": [node.get("name"), source_aliases, node.get("use_for", [])],
                "aliases": normalize_terms(source_aliases),
                "use_for": node.get("use_for", []),
                "node_role": role,
                "exportable": node.get("exportable", False),
                "status": node.get("status"),
            }
        )

    for component_name, component in components.get("components", {}).items():
        add_record(
            {
                "kind": "component",
                "node_id": component.get("node_id") or component.get("source_node_id"),
                "legacy_node_id": component.get("legacy_node_id"),
                "name": component_name,
                "terms": [component_name, component.get("aliases", []), component.get("family"), component.get("use_for", []), component.get("parameters", {}).get("type")],
                "aliases": component.get("aliases", []),
                "use_for": component.get("use_for", []),
                "family": component.get("family"),
                "component_status": component.get("component_status"),
                "status": "missing" if str(component.get("source_node_status", "")).startswith("missing") else "active",
                "locator_role": "master_candidate" if component.get("node_id") else "source_pattern" if component.get("source_node_id") else "unresolved",
            }
        )

    records.sort(key=lambda item: (item["kind"], str(item.get("name", "")), item["node_id"]))
    return {
        "schema_version": 1,
        "generated_from": {
            name: digest(path)
            for name, path in SOURCE_FILES.items()
            if name in INDEX_SOURCES["lookup"]
        },
        "record_count": len(records),
        "records": records,
    }


def build_execution_index(documents: dict[str, dict[str, Any]]) -> dict[str, Any]:
    routes = documents["task_routes"]
    validation = documents["validation"]
    defaults = routes.get("global_defaults", {})
    speed = defaults.get("speed_tier_routing", {})
    compact_tiers: dict[str, Any] = {}
    keep = {
        "use_when",
        "default_route_profile",
        "write_allowed",
        "read_rule",
        "required_first_step",
        "reuse_before_rerun",
        "required_reads",
        "required_before_write",
        "allowed_shortcuts",
        "must_report",
        "forbidden",
        "required",
    }
    for name, definition in speed.get("tiers", {}).items():
        compact_tiers[name] = {key: value for key, value in definition.items() if key in keep}

    quality_routing = defaults.get("quality_tier_routing", {})
    quality_keep = {
        "use_when",
        "required",
        "non_blocking_production_gaps",
        "always_blocking",
        "protected_even_in_exploration",
    }
    compact_quality_tiers = {
        name: {key: value for key, value in definition.items() if key in quality_keep}
        for name, definition in quality_routing.get("tiers", {}).items()
    }

    for name, definition in quality_routing.get("tiers", {}).items():
        if "non_blocking_production_gaps_ref" in definition:
            compact_quality_tiers[name]["non_blocking_production_gaps"] = validation["production_gaps_check"]["allowed_values"]

    profiles: dict[str, Any] = {}
    for name, definition in routes.get("route_profiles", {}).items():
        profiles[name] = {
            key: value
            for key, value in definition.items()
            if key in {
                "applies_to",
                "write_allowed",
                "minimum_reads",
                "conditional_reads",
                "required_reads",
                "required_fields",
                "orchestration_rule",
                "component_resolution_policy_ref",
                "draft_context_strategy",
                "forbidden",
            }
        }

    compact_routes: dict[str, Any] = {}
    for name, definition in routes.get("routes", {}).items():
        compact_routes[name] = {
            key: value
            for key, value in definition.items()
            if key in {
                "route_type",
                "alias_of",
                "triggers",
                "task_mode",
                "page_type",
                "experience_profile",
                "source_refs",
                "primary_components",
                "must_use_components",
                "local_source_patterns",
                "source_state_resolution",
                "generation_source_rule",
                "validation_gates",
                "forbidden",
            }
        }

    return {
        "schema_version": 1,
        "generated_from": {
            "task_routes": digest(SOURCE_FILES["task_routes"]),
            "validation": digest(SOURCE_FILES["validation"]),
        },
        "default_rule": speed.get("default_rule"),
        "scene_index_first_policy": defaults.get("scene_index_first_policy", {}),
        "scene_index_first_check": validation.get("scene_index_first_check", {}),
        "appearance_mode_routing": defaults.get("appearance_mode_routing", {}),
        "structured_annotation_routing": defaults.get("structured_annotation_routing", {}),
        "structured_annotation_execution_check": validation.get("structured_annotation_execution_check", {}),
        "semantic_ambiguity_routing": defaults.get("semantic_ambiguity_routing", {}),
        "semantic_authority_ambiguity_check": validation.get("semantic_authority_ambiguity_check", {}),
        "tiers": compact_tiers,
        "quality_tier_routing": {
            "selection_precedence": quality_routing.get("selection_precedence", []),
            "ambiguity_policy": quality_routing.get("ambiguity_policy", []),
            "output_contract": quality_routing.get("output_contract", {}),
        },
        "quality_tiers": compact_quality_tiers,
        "quality_assistance": quality_routing["keyword_assistance"],
        "quality_policy": {
            "quality_tiers": quality_routing["values"],
            "basic_failures": validation["universal_basic_visual_qa_check"]["universal_blocking_failures"],
            "component_failures": validation["registered_component_family_gate_check"]["blocking_failures"],
            "component_evidence_fields": validation["registered_component_family_gate_check"]["required_records"],
            "production_gaps": validation["production_gaps_check"]["allowed_values"],
            "excluded_gaps": validation["production_gaps_check"]["excluded_blocking_failures"],
            "difference_axes": validation["multi_solution_check"]["valid_difference_axes"],
            "reference_sources": validation["external_reference_check"]["evidence_source_types"],
            "contract": validation["quality_evaluator_contract"],
        },
        "universal_basic_visual_gate": validation.get("universal_basic_visual_qa_check", {}),
        "reference_evidence_policy": {
            "levels": ["none", *validation["external_reference_check"]["evidence_source_types"]],
            "check": validation.get("external_reference_check", {}),
        },
        "route_profiles": profiles,
        "routes": compact_routes,
    }


@contextmanager
def build_lock() -> Iterable[None]:
    """Serialize index rebuilds so readers never race multiple writers."""
    RUNTIME.mkdir(parents=True, exist_ok=True)
    with LOCK_FILE.open("a+", encoding="utf-8") as handle:
        fcntl.flock(handle.fileno(), fcntl.LOCK_EX)
        try:
            yield
        finally:
            fcntl.flock(handle.fileno(), fcntl.LOCK_UN)


def serialized_json(value: dict[str, Any]) -> str:
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"), sort_keys=True) + "\n"


def write_json(path: Path, value: dict[str, Any]) -> None:
    """Atomically publish a complete index in the destination directory."""
    payload = serialized_json(value)
    fd, temp_name = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temp_name, path)
    finally:
        if os.path.exists(temp_name):
            os.unlink(temp_name)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="fail when checked-in indexes differ from generated output")
    args = parser.parse_args()

    documents = {name: load_yaml(path) for name, path in SOURCE_FILES.items()}
    outputs = {
        RUNTIME / "lookup-index.json": build_lookup_index(documents),
        RUNTIME / "execution-index.json": build_execution_index(documents),
    }
    if args.check:
        failed = []
        for path, value in outputs.items():
            if not path.exists() or path.read_text(encoding="utf-8") != serialized_json(value):
                failed.append(str(path.relative_to(SKILL_ROOT)))
        if failed:
            raise SystemExit("runtime index stale: " + ", ".join(failed))
        print("runtime indexes are current")
        return 0

    with build_lock():
        for path, value in outputs.items():
            write_json(path, value)
            print(f"wrote {path.relative_to(SKILL_ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
