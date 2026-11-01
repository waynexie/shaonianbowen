#!/usr/bin/env python3
"""Validate a durable visual attachment and return final Markdown evidence."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from urllib.parse import urlparse


SKILL_ROOT = Path(__file__).resolve().parents[1]


TEMP_PREFIXES = (
    "/tmp/",
    "/private/tmp/",
    "/var/folders/",
    "/private/var/folders/",
)


def detect_format(header: bytes) -> str | None:
    if header.startswith(b"\x89PNG\r\n\x1a\n"):
        return "png"
    if header.startswith(b"\xff\xd8\xff"):
        return "jpeg"
    if header.startswith((b"GIF87a", b"GIF89a")):
        return "gif"
    if len(header) >= 12 and header[:4] == b"RIFF" and header[8:12] == b"WEBP":
        return "webp"
    return None


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("path", help="absolute durable image path")
    parser.add_argument("--label", default="少年博闻视觉预览")
    parser.add_argument(
        "--allowed-root",
        action="append",
        type=Path,
        help="allowed persistent root; repeat when the platform workspace and Skill assets are both valid",
    )
    parser.add_argument(
        "--delivery-url",
        help="platform-accessible http(s) URL after upload/persistence; required for final Markdown delivery",
    )
    args = parser.parse_args()

    input_path = Path(args.path)
    path = input_path.resolve(strict=False)
    errors: list[str] = []
    if not input_path.is_absolute():
        errors.append("path_not_absolute")

    allowed_roots = [root.resolve(strict=False) for root in (args.allowed_root or [SKILL_ROOT])]
    if not any(path == root or root in path.parents for root in allowed_roots):
        errors.append("path_outside_allowed_root")

    normalized = str(path)
    if any(normalized.startswith(prefix) for prefix in TEMP_PREFIXES):
        errors.append("temporary_path_forbidden")
    if not path.is_file():
        errors.append("file_missing")

    size = path.stat().st_size if path.is_file() else 0
    if size <= 0:
        errors.append("file_empty")

    image_format = None
    if path.is_file() and size > 0:
        with path.open("rb") as handle:
            image_format = detect_format(handle.read(16))
        if image_format is None:
            errors.append("unrecognized_image_signature")

    valid = not errors
    delivery_url = args.delivery_url
    delivery_errors: list[str] = []
    if delivery_url:
        parsed = urlparse(delivery_url)
        if parsed.scheme not in {"http", "https"} or not parsed.netloc:
            delivery_errors.append("delivery_url_invalid")
    else:
        delivery_errors.append("delivery_url_missing")
    delivery_ready = valid and not delivery_errors
    result = {
        "valid": valid,
        "delivery_ready": delivery_ready,
        "status": (
            "visual_attachment_delivery_ready"
            if delivery_ready
            else "local_asset_valid_pending_platform_delivery"
            if valid
            else "visual_attachment_unavailable"
        ),
        "visual_attachment_path": normalized,
        "allowed_roots": [str(root) for root in allowed_roots],
        "visual_attachment_format": image_format,
        "visual_attachment_size_bytes": size,
        "visual_attachment_validation_status": "passed" if valid else "failed",
        "delivery_url": delivery_url,
        "markdown_image": f"![{args.label}]({delivery_url})" if delivery_ready else None,
        "errors": errors,
        "delivery_errors": delivery_errors,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if valid else 1


if __name__ == "__main__":
    raise SystemExit(main())
