#!/usr/bin/env python3
"""Crash-recoverably replace one verified visual-cache asset and metadata entry."""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import yaml


SKILL_ROOT = Path(__file__).resolve().parents[1]
CACHE_FILE = SKILL_ROOT / "references" / "metadata" / "visual-cache.yaml"
TRANSACTION_DIR = SKILL_ROOT / ".visual-cache-update-transaction"
JOURNAL_FILE = TRANSACTION_DIR / "journal.json"


def recover_interrupted_transaction() -> None:
    """Roll back a prepared two-file update or clean a committed transaction."""
    if not JOURNAL_FILE.exists():
        if TRANSACTION_DIR.exists():
            shutil.rmtree(TRANSACTION_DIR)
        return
    journal = json.loads(JOURNAL_FILE.read_text(encoding="utf-8"))
    target_asset = Path(journal["target_asset"])
    if journal.get("state") == "prepared":
        backup_yaml = TRANSACTION_DIR / "visual-cache.yaml.bak"
        backup_asset = TRANSACTION_DIR / "asset.bak"
        if backup_yaml.exists():
            os.replace(backup_yaml, CACHE_FILE)
        if journal.get("asset_existed") and backup_asset.exists():
            os.replace(backup_asset, target_asset)
        elif not journal.get("asset_existed") and target_asset.exists():
            target_asset.unlink()
    shutil.rmtree(TRANSACTION_DIR, ignore_errors=True)


def write_journal(value: dict) -> None:
    temp = TRANSACTION_DIR / "journal.tmp"
    temp.write_text(json.dumps(value, ensure_ascii=False), encoding="utf-8")
    os.replace(temp, JOURNAL_FILE)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cache-id", required=True)
    parser.add_argument("--asset", required=True, type=Path)
    parser.add_argument("--captured-at", required=True)
    parser.add_argument("--source-verified-at", required=True)
    parser.add_argument("--render-state")
    args = parser.parse_args()

    recover_interrupted_transaction()
    if not args.asset.is_file() or args.asset.stat().st_size == 0:
        raise SystemExit("verified cache asset is missing or empty")
    subprocess.run(
        [
            sys.executable,
            str(SKILL_ROOT / "scripts" / "validate_visual_attachment.py"),
            str(args.asset.resolve()),
            "--allowed-root",
            str(args.asset.resolve().parent),
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    data = yaml.safe_load(CACHE_FILE.read_text(encoding="utf-8"))
    entry = next((item for item in data.get("entries", []) if item.get("cache_id") == args.cache_id), None)
    if entry is None:
        raise SystemExit(f"unknown cache_id: {args.cache_id}")
    if not entry.get("asset_path"):
        raise SystemExit("missing entries need an explicit metadata design decision before adding an asset path")

    entry["captured_at"] = args.captured_at
    entry["source_verified_at"] = args.source_verified_at
    entry["cache_status"] = "active"
    if args.render_state:
        entry["render_state"] = args.render_state

    target_asset = SKILL_ROOT / entry["asset_path"]
    target_asset.parent.mkdir(parents=True, exist_ok=True)
    yaml_text = yaml.safe_dump(data, allow_unicode=True, sort_keys=False, width=120)

    with tempfile.TemporaryDirectory(prefix="bowen-cache-", dir=str(SKILL_ROOT)) as temp_dir:
        stage = Path(temp_dir)
        staged_asset = stage / target_asset.name
        staged_yaml = stage / CACHE_FILE.name
        shutil.copy2(args.asset, staged_asset)
        staged_yaml.write_text(yaml_text, encoding="utf-8")
        yaml.safe_load(staged_yaml.read_text(encoding="utf-8"))

        TRANSACTION_DIR.mkdir()
        asset_existed = target_asset.exists()
        if asset_existed:
            shutil.copy2(target_asset, TRANSACTION_DIR / "asset.bak")
        shutil.copy2(CACHE_FILE, TRANSACTION_DIR / "visual-cache.yaml.bak")
        journal = {
            "state": "prepared",
            "target_asset": str(target_asset.resolve()),
            "asset_existed": asset_existed,
        }
        write_journal(journal)
        try:
            os.replace(staged_asset, target_asset)
            os.replace(staged_yaml, CACHE_FILE)
            journal["state"] = "committed"
            write_journal(journal)
        except Exception:
            recover_interrupted_transaction()
            raise
        shutil.rmtree(TRANSACTION_DIR, ignore_errors=True)

    subprocess.run([sys.executable, str(SKILL_ROOT / "scripts" / "build_runtime_indexes.py")], check=True)
    print(f"updated {args.cache_id}; runtime indexes rebuilt")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
