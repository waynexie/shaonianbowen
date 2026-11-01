#!/usr/bin/env python3
"""Audit local visual-cache metadata and assets without contacting Figma."""

from __future__ import annotations

import argparse
import datetime as dt
import json

import yaml


from runtime_support import METADATA, cache_freshness, cache_asset_exists, aware_timestamp, LOCAL_TIMEZONE

CACHE_FILE = METADATA / "visual-cache.yaml"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--now", default=None, help="ISO timestamp used by deterministic tests")
    parser.add_argument("--strict", action="store_true", help="fail on missing assets, stale or expired records")
    args = parser.parse_args()
    now = aware_timestamp(args.now) if args.now else dt.datetime.now(LOCAL_TIMEZONE)
    data = yaml.safe_load(CACHE_FILE.read_text(encoding="utf-8"))
    results = []
    for entry in data.get("entries", []):
        item = {
            "cache_id": entry.get("cache_id"),
            "metadata_status": entry.get("cache_status"),
            "freshness": cache_freshness(entry, now),
        }
        item["asset_exists"] = cache_asset_exists(entry)
        if item["freshness"] not in {"missing", "invalid"}:
            captured = aware_timestamp(str(entry["captured_at"]))
            item["expires_at"] = (captured + dt.timedelta(days=float(entry["max_age_days"]))).isoformat()
        results.append(item)

    counts: dict[str, int] = {}
    for result in results:
        counts[result["freshness"]] = counts.get(result["freshness"], 0) + 1
    payload = {"now": now.isoformat(), "counts": counts, "entries": results}
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    failures = [result for result in results if not result["asset_exists"] and result["freshness"] != "missing"]
    if args.strict:
        failures.extend(result for result in results if result["freshness"] != "fresh")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
