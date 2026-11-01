#!/usr/bin/env python3
"""Print one authority-YAML section instead of loading an entire large file."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import yaml


SKILL_ROOT = Path(__file__).resolve().parents[1]
METADATA = SKILL_ROOT / "references" / "metadata"
ALLOWED = {path.name: path for path in METADATA.glob("*.yaml")}


def select(value: Any, dotted_path: str) -> Any:
    current = value
    for part in dotted_path.split(".") if dotted_path else []:
        if isinstance(current, dict) and part in current:
            current = current[part]
        elif isinstance(current, list) and part.isascii() and part.isdecimal() and int(part) < len(current):
            current = current[int(part)]
        else:
            raise KeyError(part)
    return current


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("file", choices=sorted(ALLOWED))
    parser.add_argument("section", nargs="?", default="")
    args = parser.parse_args()
    data = yaml.safe_load(ALLOWED[args.file].read_text(encoding="utf-8"))
    try:
        result = select(data, args.section)
    except KeyError as error:
        raise SystemExit(f"section not found: {args.section} (missing {error.args[0]})")
    print(json.dumps({"source": args.file, "section": args.section or "$", "value": result}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
