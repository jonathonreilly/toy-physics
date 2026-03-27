#!/usr/bin/env python3
"""Summarize the subtype-specific satellite buckets left after the shared support-family map."""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
import sys
import time

SCRIPTS_DIR = Path(__file__).resolve().parent
PROJECT_DIR = SCRIPTS_DIR.parent
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))
if str(PROJECT_DIR) not in sys.path:
    sys.path.insert(0, str(PROJECT_DIR))

from pocket_wrap_suppressor_low_overlap_support_family_transfer_common import (  # noqa: E402
    PRIMARY_SUPPORT_FAMILY_BUCKETS,
    build_rows,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--frontier-log",
        default="/Users/jonreilly/Projects/Physics/logs/2026-03-26-pocket-wrap-suppressor-nonpocket-subtype-rules-5504-max5600.txt",
    )
    parser.add_argument("--show-limit", type=int, default=10)
    return parser


def main() -> None:
    args = build_parser().parse_args()
    started = datetime.now().isoformat(timespec="seconds")
    print(f"support family transfer satellites started {started}", flush=True)
    total_start = time.time()

    frontier_log = Path(args.frontier_log).resolve()
    rows = build_rows(frontier_log)
    satellites = [
        row
        for row in rows
        if row.high_bridge_left_low_count < 0.5
        and row.family_bucket_key not in PRIMARY_SUPPORT_FAMILY_BUCKETS
    ]
    grouped: dict[str, list[object]] = defaultdict(list)
    for row in satellites:
        grouped[row.residual_bucket_key].append(row)

    ordered = sorted(grouped.items(), key=lambda item: (-len(item[1]), item[0]))

    print()
    print("Support Family Transfer Satellites")
    print("==================================")
    print(f"frontier_log={frontier_log}")
    print(f"satellite_rows={len(satellites)}")
    print()
    for idx, (key, bucket_rows) in enumerate(ordered[: args.show_limit], start=1):
        counts = Counter(row.subtype for row in bucket_rows)
        print(f"{idx}. bucket={key} count={len(bucket_rows)} subtype_counts={dict(counts)}")
        print("   rows=" + ", ".join(row.source_name for row in bucket_rows))
    print()
    print(
        "support family transfer satellites completed "
        + datetime.now().isoformat(timespec="seconds")
        + f" total_elapsed={time.time() - total_start:.1f}s",
        flush=True,
    )


if __name__ == "__main__":
    main()
