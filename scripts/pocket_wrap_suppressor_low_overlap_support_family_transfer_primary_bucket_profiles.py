#!/usr/bin/env python3
"""Profile subtype means inside the shared primary support-family buckets."""

from __future__ import annotations

import argparse
from collections import defaultdict
from datetime import datetime
from pathlib import Path
import statistics
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
FEATURES = (
    "edge_identity_closed_pair_count",
    "support_role_bridge_count",
    "high_bridge_left_count",
    "high_bridge_mid_count",
    "high_bridge_low_count",
    "high_bridge_right_count",
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--frontier-log",
        default="/Users/jonreilly/Projects/Physics/logs/2026-03-26-pocket-wrap-suppressor-nonpocket-subtype-rules-5504-max5600.txt",
    )
    return parser


def main() -> None:
    args = build_parser().parse_args()
    started = datetime.now().isoformat(timespec="seconds")
    print(f"support family transfer primary bucket profiles started {started}", flush=True)
    total_start = time.time()

    frontier_log = Path(args.frontier_log).resolve()
    rows = build_rows(frontier_log)

    print()
    print("Support Family Transfer Primary Bucket Profiles")
    print("===============================================")
    print(f"frontier_log={frontier_log}")
    print()
    for bucket_key in PRIMARY_SUPPORT_FAMILY_BUCKETS:
        bucket_rows = [
            row
            for row in rows
            if row.family_bucket_key == bucket_key and row.high_bridge_left_low_count < 0.5
        ]
        grouped: dict[str, list[object]] = defaultdict(list)
        for row in bucket_rows:
            grouped[row.subtype].append(row)
        print(f"Bucket {bucket_key} count={len(bucket_rows)}")
        for subtype in sorted(grouped):
            subtype_rows = grouped[subtype]
            print(f"  {subtype} count={len(subtype_rows)}")
            for feature in FEATURES:
                values = [float(getattr(row, feature)) for row in subtype_rows]
                print(
                    f"    {feature}: min={min(values):.1f} max={max(values):.1f} "
                    f"mean={statistics.mean(values):.2f}"
                )
        print()
    print(
        "support family transfer primary bucket profiles completed "
        + datetime.now().isoformat(timespec="seconds")
        + f" total_elapsed={time.time() - total_start:.1f}s",
        flush=True,
    )


if __name__ == "__main__":
    main()
