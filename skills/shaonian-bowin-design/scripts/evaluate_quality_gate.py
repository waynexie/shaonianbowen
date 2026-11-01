#!/usr/bin/env python3
"""Suggest quality tiers and check a declared slice of supplied QA evidence.

Policies come from the authority-derived execution index. This command neither
inspects pixels nor authorizes Figma writes or complete production delivery.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from typing import Any

from runtime_support import load_current_index


def contains_any(text: str, signals: list[str]) -> bool:
    return any(signal.casefold() in text.casefold() for signal in signals)


def route_quality_tier(text: str, intent: str | None = None) -> dict[str, Any]:
    assistance = load_current_index("execution")["quality_assistance"]
    signals = assistance["signals"]
    found = {key: contains_any(text, values) for key, values in signals.items() if not key.endswith("patterns")}
    negated = any(re.search(pattern, text, re.I) for pattern in signals["negated_generation_patterns"])
    generation = found["generation"] or found["local_change"] or found["exploration"]
    lookup = found["lookup"]
    ambiguous = (lookup and generation) or negated or not (lookup or generation)
    readonly = intent == "lookup_existing" if intent else lookup or negated or not generation
    base = {
        "request": text,
        "semantic_intent": intent,
        "explicit_production_signal": found["production"],
        "explicit_exploration_signal": found["exploration"],
        "existing_target_signal": found["existing_target"],
        "generation_signal": generation,
        "lookup_signal": lookup,
        "readonly": readonly,
        "needs_clarification": ambiguous if intent is None else False,
        "write_authorization": False,
        "routing_scope": "quality_suggestion_requires_semantic_route_confirmation",
    }
    if readonly:
        return {**base, "quality_tier": None}
    if found["production"]:
        tier = "production"
    elif found["exploration"]:
        tier = "inspiration_draft"
    elif (found["local_change"] and found["existing_target"]) or intent == "mutate_existing":
        tier = "precision_draft"
    else:
        tier = "inspiration_draft"
    return {**base, "quality_tier": tier, "locked_existing_shell": found["existing_target"] or intent == "mutate_existing"}


def evaluate(evidence: dict[str, Any]) -> dict[str, Any]:
    policy = load_current_index("execution")["quality_policy"]
    blocking: list[str] = []
    tier = evidence.get("quality_tier")
    if tier not in policy["quality_tiers"]:
        blocking.append("invalid_or_missing_quality_tier")
    for field in policy["contract"]["required_input"]:
        if field not in evidence:
            blocking.append(f"missing_evidence:{field}")

    def array(name: str, strings: bool = False) -> list:
        value = evidence.get(name, [])
        if not isinstance(value, list) or (strings and any(not isinstance(item, str) for item in value)):
            blocking.append(f"invalid_evidence:{name}")
            return []
        return value

    failures = set(array("detected_basic_failures", strings=True))
    if evidence.get("screenshot_checked") is not True:
        failures.add("screenshot_not_checked")
    checks = evidence.get("basic_checks", {})
    if not isinstance(checks, dict):
        blocking.append("invalid_evidence:basic_checks")
    else:
        for name, passed in checks.items():
            if name not in policy["basic_failures"] or not isinstance(passed, bool):
                blocking.append(f"invalid_basic_check:{name}")
            elif passed is False:
                failures.add(name)
    known = set(policy["basic_failures"]) | set(policy["component_failures"])
    blocking.extend(failure if failure in known else f"unrecognized_failure:{failure}" for failure in failures)
    basic_failures = sorted(failures & set(policy["basic_failures"]))

    if evidence.get("component_resolution_checked") is not True:
        blocking.append("component_resolution_not_checked")
    families = array("registered_component_families")
    for index, family in enumerate(families):
        if not isinstance(family, dict):
            blocking.append(f"invalid_component_evidence:{index}")
            continue
        for field in policy["component_evidence_fields"]:
            value = family.get(field)
            if field == "target_region_screenshot_check":
                valid = value is True
            elif field == "component_property_or_variant_changes":
                valid = isinstance(value, list)
            else:
                valid = isinstance(value, str) and bool(value.strip())
            if not valid:
                blocking.append(f"component_source_or_delivery_evidence_missing:{index}:{field}")
        if family.get("gate_result", "pass") != "pass":
            blocking.append("registered_component_family_gate_failed")

    gaps = sorted(set(array("production_gaps", strings=True)))
    for gap in gaps:
        if gap in policy["excluded_gaps"] or gap in policy["component_failures"]:
            blocking.append(gap)
        elif gap not in policy["production_gaps"]:
            blocking.append(f"unrecognized_production_gap:{gap}")
        if tier == "production":
            blocking.append(f"unresolved_production_gap:{gap}")

    options = array("options")
    option_errors: list[str] = []
    if len(options) > 1:
        theses = [" ".join(str(option.get("design_thesis", "")).casefold().split()) if isinstance(option, dict) else "" for option in options]
        if any(not thesis for thesis in theses) or len(set(theses)) != len(theses):
            option_errors.append("design_thesis_missing_or_equivalent")
        for index, option in enumerate(options):
            axes = option.get("difference_axes", []) if isinstance(option, dict) else []
            if not isinstance(axes, list) or not any(axis in policy["difference_axes"] for axis in axes):
                option_errors.append(f"option_{index + 1}_has_no_meaningful_difference_axis")
    blocking.extend(option_errors)

    sources = array("reference_sources")
    source_types = {str(source.get("type")) if isinstance(source, dict) else str(source) for source in sources}
    source_policy = policy["reference_sources"]
    if source_types & set(source_policy["visual_reference_checked"]):
        reference_level = "visual_reference_checked"
    elif source_types & set(source_policy["pattern_memory_reference"]) or evidence.get("reference_products_checked"):
        reference_level = "pattern_memory_reference"
    else:
        reference_level = "none"
    claimed = evidence.get("reference_evidence_level")
    if claimed is not None and claimed not in {"none", *source_policy}:
        blocking.append("invalid_reference_evidence_level")
    if claimed == "visual_reference_checked" and claimed != reference_level:
        blocking.append("reference_evidence_overclaim")

    blocking = sorted(set(blocking))
    return {
        "status": "validation_failed" if blocking else "passed",
        "passed": not blocking,
        "quality_tier": tier,
        "result_scope": policy["contract"]["result_scope"],
        "complete_route_validation": False,
        "production_delivery_authorized": False,
        "basic_visual_gate": {"passed": not basic_failures, "failures": basic_failures},
        "option_difference_result": {"required": len(options) > 1, "passed": not option_errors, "failures": option_errors},
        "reference_evidence_level": reference_level,
        "production_gaps": gaps,
        "must_not_claim_production": True,
        "blocking_failures": blocking,
        "excluded_overlap_pairs": evidence.get("excluded_overlap_pairs", []),
    }


def load_evidence(path: str | None, raw_json: str | None) -> dict[str, Any]:
    from pathlib import Path
    data = json.loads(raw_json) if raw_json is not None else json.loads(Path(path).read_text(encoding="utf-8")) if path and path != "-" else json.load(sys.stdin)
    if not isinstance(data, dict):
        raise ValueError("quality evidence must be a JSON object")
    return data


def main() -> int:
    parser = argparse.ArgumentParser()
    commands = parser.add_subparsers(dest="command", required=True)
    route = commands.add_parser("route")
    route.add_argument("request")
    route.add_argument("--intent", choices=load_current_index("execution")["quality_assistance"]["semantic_intents"])
    validate = commands.add_parser("validate")
    validate.add_argument("path", nargs="?", default="-")
    validate.add_argument("--json", dest="raw_json")
    args = parser.parse_args()
    try:
        result = route_quality_tier(args.request, args.intent) if args.command == "route" else evaluate(load_evidence(args.path, args.raw_json))
    except (ValueError, TypeError, OSError) as error:
        result = {"status": "validation_failed", "passed": False, "blocking_failures": [f"invalid_input:{error}"], "complete_route_validation": False}
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 1 if result.get("status") == "validation_failed" else 0


if __name__ == "__main__":
    raise SystemExit(main())
