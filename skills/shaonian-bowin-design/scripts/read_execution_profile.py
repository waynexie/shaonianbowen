#!/usr/bin/env python3
"""Read one compact execution tier, profile, or route from the runtime index."""

from __future__ import annotations

import argparse
import json


from runtime_support import load_current_index


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("kind", choices=["tier", "quality", "profile", "route"])
    parser.add_argument("name")
    parser.add_argument("--compact", action="store_true", help="return only the selected definition; load shared policies only when needed")
    args = parser.parse_args()
    data = load_current_index("execution")
    collection = {
        "tier": "tiers",
        "quality": "quality_tiers",
        "profile": "route_profiles",
        "route": "routes",
    }[args.kind]
    value = data.get(collection, {}).get(args.name)
    if value is None:
        choices = sorted(data.get(collection, {}))
        raise SystemExit(f"unknown {args.kind}: {args.name}; choices: {', '.join(choices)}")
    result = {
        args.kind: args.name,
        "definition": value,
    }
    if not args.compact:
        result.update({
            "appearance_mode_routing": data.get("appearance_mode_routing", {}),
            "structured_annotation_routing": data.get("structured_annotation_routing", {}),
            "structured_annotation_execution_check": data.get("structured_annotation_execution_check", {}),
            "semantic_ambiguity_routing": data.get("semantic_ambiguity_routing", {}),
            "semantic_authority_ambiguity_check": data.get("semantic_authority_ambiguity_check", {}),
        })
    print(json.dumps(result, ensure_ascii=False, separators=(",", ":") if args.compact else None, indent=None if args.compact else 2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
