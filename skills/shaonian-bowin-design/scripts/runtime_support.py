"""Shared local index loading and visual-cache eligibility helpers."""

from __future__ import annotations

import datetime as dt
import hashlib
import json
import subprocess
import sys
from pathlib import Path
from typing import Any


SKILL_ROOT = Path(__file__).resolve().parents[1]
METADATA = SKILL_ROOT / "references" / "metadata"
RUNTIME = SKILL_ROOT / "references" / "runtime"
SOURCE_FILES = {
    "task_routes": METADATA / "task-routes.yaml",
    "validation": METADATA / "validation.yaml",
    "source_frames": METADATA / "source-frames.yaml",
    "source_registry": METADATA / "source-registry.yaml",
    "components": METADATA / "components.yaml",
    "scene_index": METADATA / "scene-index.yaml",
    "visual_cache": METADATA / "visual-cache.yaml",
}
INDEX_SOURCES = {
    "execution": ("task_routes", "validation"),
    "lookup": ("source_frames", "source_registry", "components", "scene_index", "visual_cache"),
}
LOCAL_TIMEZONE = dt.timezone(dt.timedelta(hours=8))


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_current_index(kind: str) -> dict[str, Any]:
    """Rebuild once on missing, malformed or stale data, then verify it again."""
    names = INDEX_SOURCES[kind]
    path = RUNTIME / f"{kind}-index.json"
    for attempt in range(2):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            expected = {name: digest(SOURCE_FILES[name]) for name in names}
            payload_key = "records" if kind == "lookup" else "route_profiles"
            expected_type = list if kind == "lookup" else dict
            if (isinstance(data, dict) and data.get("generated_from") == expected
                    and isinstance(data.get(payload_key), expected_type)):
                return data
        except (OSError, ValueError, TypeError):
            pass
        if attempt == 0:
            subprocess.run(
                [sys.executable, str(SKILL_ROOT / "scripts" / "build_runtime_indexes.py")],
                check=True, capture_output=True, text=True,
            )
    raise ValueError(f"runtime index invalid after rebuild: {path.name}")


def aware_timestamp(value: str | dt.datetime) -> dt.datetime:
    result = dt.datetime.fromisoformat(value) if isinstance(value, str) else value
    return result.replace(tzinfo=LOCAL_TIMEZONE) if result.tzinfo is None else result


def cache_freshness(entry: dict[str, Any], now: dt.datetime) -> str:
    """Future, malformed, missing and explicitly stale captures never qualify."""
    if entry.get("cache_status") == "missing" or not entry.get("asset_path") or not entry.get("captured_at"):
        return "missing"
    if entry.get("cache_status") == "stale":
        return "stale"
    if entry.get("cache_status") != "active":
        return "invalid"
    try:
        captured = aware_timestamp(str(entry["captured_at"]))
        days = float(entry.get("max_age_days", 0))
        expires = captured + dt.timedelta(days=days)
        current = aware_timestamp(now)
        if days <= 0:
            return "invalid"
        if current < captured:
            return "future"
        return "fresh" if current < expires else "expired"
    except (TypeError, ValueError, OverflowError):
        return "invalid"


def cache_asset_exists(entry: dict[str, Any]) -> bool:
    value = entry.get("asset_path")
    if not isinstance(value, str) or not value:
        return False
    relative = Path(value)
    if relative.is_absolute() or ".." in relative.parts:
        return False
    candidate = SKILL_ROOT / relative
    # Cache files are shipped assets, not external symlinks.
    part = candidate
    while part != SKILL_ROOT:
        if part.is_symlink():
            return False
        part = part.parent
    return candidate.is_file()
