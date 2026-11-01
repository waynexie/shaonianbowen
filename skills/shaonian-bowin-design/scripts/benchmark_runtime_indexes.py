#!/usr/bin/env python3
"""Measure compact-index query latency without contacting Figma or changing metadata."""

from __future__ import annotations

import argparse
import json
import statistics
import subprocess
import sys
import time
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
QUERY_SCRIPT = SKILL_ROOT / "scripts" / "query_runtime_index.py"


def percentile(values: list[float], ratio: float) -> float:
    ordered = sorted(values)
    index = min(len(ordered) - 1, max(0, int(round((len(ordered) - 1) * ratio))))
    return ordered[index]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("query", nargs="?", default="个人中心")
    parser.add_argument("--kind", choices=["screen", "component", "asset", "source"], default="screen")
    parser.add_argument("--state")
    parser.add_argument("--runs", type=int, default=20)
    args = parser.parse_args()
    if args.runs < 3 or args.runs > 500:
        raise SystemExit("--runs must be between 3 and 500")

    command = [sys.executable, str(QUERY_SCRIPT), args.query, "--kind", args.kind, "--limit", "1"]
    if args.state:
        command.extend(["--state", args.state])

    durations_ms: list[float] = []
    output_bytes: list[int] = []
    for _ in range(args.runs):
        started = time.perf_counter()
        process = subprocess.run(command, check=True, capture_output=True, text=True)
        durations_ms.append((time.perf_counter() - started) * 1000)
        output_bytes.append(len(process.stdout.encode("utf-8")))

    result = {
        "query": args.query,
        "kind": args.kind,
        "state": args.state,
        "runs": args.runs,
        "p50_ms": round(statistics.median(durations_ms), 3),
        "p95_ms": round(percentile(durations_ms, 0.95), 3),
        "max_ms": round(max(durations_ms), 3),
        "max_output_bytes": max(output_bytes),
        "context_budget_pass": max(output_bytes) <= 10_240,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
