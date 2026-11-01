#!/usr/bin/env python3
"""Return only matching Shaonian Bowen runtime-index records."""

from __future__ import annotations

import argparse
import datetime as dt
import json
from typing import Any


from runtime_support import load_current_index, cache_freshness, cache_asset_exists, aware_timestamp, LOCAL_TIMEZONE
GENERIC_EMBEDDED_TERMS = {"首页", "页面", "播客", "电台"}
DARK_MODE_TERMS = ("夜间", "暗色", "深色", "dark mode", "dark", "night mode")
LIGHT_MODE_TERMS = ("日间", "亮色", "浅色", "light mode", "light")


def score(record: dict[str, Any], query: str) -> int:
    q = query.casefold().strip()
    if not q:
        return 0
    if q == str(record.get("node_id", "")).casefold():
        return 200
    name = str(record.get("name") or "").casefold()
    terms = [str(value).casefold() for value in record.get("terms", [])]
    aliases = [str(value).casefold() for value in record.get("aliases", [])]
    score_value = 0
    if q == name:
        score_value += 120
    if q in name:
        score_value += 70
    if q in aliases:
        score_value += 110
    for term in terms:
        if q == term:
            score_value += 80
        elif term in GENERIC_EMBEDDED_TERMS and term in q:
            continue
        elif q in term or term in q:
            score_value += 30
    for token in q.replace("/", " ").replace("_", " ").split():
        if len(token) > 1 and any(token in term for term in terms):
            score_value += 8
    if record.get("is_primary_display_frame") and q in {
        str(record.get("source_group_id") or "").casefold(),
        str(record.get("source_group_name") or "").casefold(),
    }:
        score_value += 50
    return score_value


def resolve_appearance_mode(query: str, override: str | None) -> tuple[str | None, str]:
    if override:
        return override, "explicit_runtime_argument"
    normalized = query.casefold()
    dark = any(term in normalized for term in DARK_MODE_TERMS)
    light = any(term in normalized for term in LIGHT_MODE_TERMS)
    if dark and light:
        return None, "ambiguous_explicit_modes"
    if dark:
        return "dark", "explicit_current_turn"
    if light:
        return "light_default", "explicit_current_turn"
    return "light_default", "default_unspecified_current_turn"


def compact_locator(item: dict[str, Any]) -> dict[str, Any]:
    """Keep IDs and state needed to choose a target without loading gallery details."""
    fields = (
        "kind", "node_id", "name", "score", "source_group_id", "source_group_name",
        "experience_profile", "state_role", "status", "exportable", "component_status",
        "family", "delivery_status", "live_figma_required",
    )
    result = {key: item[key] for key in fields if key in item}
    if "scene_component_refs" in item:
        result["scene_component_refs"] = [
            {key: ref[key] for key in ("id", "name", "master", "source_instance_id") if key in ref}
            for ref in item["scene_component_refs"]
        ]
    if "scene_variant_rows" in item:
        result["variant_row_count"] = len(item["scene_variant_rows"])
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("query")
    parser.add_argument("--kind", choices=["screen", "component", "asset", "source"])
    parser.add_argument("--state", help="render state required for an exact cache hit")
    parser.add_argument("--mode", choices=["light_default", "dark"], help="explicit requested appearance mode; otherwise inferred from the current query and defaults to light_default")
    parser.add_argument("--intent", choices=["locate", "visualize", "write"], default="visualize", help="locate uses index only; visualize validates image evidence; write requires targeted live source/master verification")
    parser.add_argument("--latest", action="store_true", help="force live Figma for latest/realtime/current-version requests")
    parser.add_argument("--limit", type=int, default=5)
    parser.add_argument("--compact", action="store_true", help="trim locate records and JSON whitespace for initial routing")
    parser.add_argument("--now", default=None, help="ISO timestamp used by deterministic tests")
    args = parser.parse_args()

    if args.limit < 1 or args.limit > 20:
        raise SystemExit("--limit must be between 1 and 20")

    index = load_current_index("lookup")
    now = aware_timestamp(args.now) if args.now else dt.datetime.now(LOCAL_TIMEZONE)
    requested_mode, mode_source = resolve_appearance_mode(args.query, args.mode)

    matches = []
    for record in index.get("records", []):
        if args.kind and record.get("kind") != args.kind:
            continue
        rank = score(record, args.query)
        if rank <= 0:
            continue
        item = {key: value for key, value in record.items() if key not in {"terms", "cache"} and value not in (None, [], "")}
        item["score"] = rank
        cache_results = []
        for cache in record.get("cache", []):
            if args.state and cache.get("render_state") != args.state:
                continue
            if requested_mode is None or cache.get("appearance_mode") != requested_mode:
                continue
            cache_item = dict(cache)
            cache_item["freshness"] = cache_freshness(cache, now)
            cache_item["asset_exists"] = cache_asset_exists(cache)
            if not cache_item["asset_exists"]:
                cache_item["freshness"] = "missing"
            cache_item["appearance_mode_verified"] = cache.get("appearance_mode") in {"light_default", "dark"}
            cache_results.append(cache_item)
        if cache_results:
            item["cache"] = cache_results
        item["live_figma_required"] = args.latest or not any(cache.get("freshness") == "fresh" for cache in cache_results)
        item["requested_appearance_mode"] = requested_mode
        item["requested_mode_source"] = mode_source
        item["appearance_mode_verification_required"] = True
        item["delivery_status"] = "verified_cache_ready" if not item["live_figma_required"] else "live_mode_verification_required"
        item["unavailable_status_if_live_fails"] = "requested_appearance_unavailable"
        if args.latest:
            item["live_fallback_reason"] = "latest_or_realtime_requested"
        elif requested_mode is None:
            item["live_fallback_reason"] = "explicit_appearance_modes_ambiguous"
        elif args.state and not cache_results:
            item["live_fallback_reason"] = "render_state_or_appearance_mode_mismatch_or_missing"
        elif item["live_figma_required"]:
            item["live_fallback_reason"] = "fresh_same_node_same_mode_cache_missing"
        item["lookup_intent"] = args.intent
        if args.intent == "locate":
            item["live_figma_required"] = bool(args.latest)
            item["appearance_mode_verification_required"] = False
            item["delivery_status"] = "live_locator_verification_required" if args.latest else "source_index_only"
            item.pop("unavailable_status_if_live_fails", None)
            if not args.latest:
                item.pop("live_fallback_reason", None)
        elif args.intent == "write":
            item["live_figma_required"] = True
            item["delivery_status"] = "targeted_live_source_and_master_verification_required"
            item["live_fallback_reason"] = "design_write_requires_current_authority"
        matches.append(item)

    matches.sort(key=lambda item: (-int(item["score"]), str(item.get("name", ""))))
    if args.compact and args.intent == "locate":
        matches = [compact_locator(item) for item in matches]
    result = {
        "query": args.query,
        "requested_appearance_mode": requested_mode,
        "requested_mode_source": mode_source,
        "count": min(len(matches), args.limit),
        "matches": matches[: args.limit],
    }
    print(json.dumps(result, ensure_ascii=False, separators=(",", ":") if args.compact else None, indent=None if args.compact else 2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
