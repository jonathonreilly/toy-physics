#!/usr/bin/env python3
"""Probe compact subtype rules inside shared support-family buckets."""

from __future__ import annotations

import argparse
from collections import Counter
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

from pocket_wrap_suppressor_low_overlap_center_spine_bucket00_support_topology import (  # noqa: E402
    evaluate_rules,
    render_rules,
)
from pocket_wrap_suppressor_low_overlap_support_family_transfer_common import (  # noqa: E402
    build_rows,
)


FEATURE_NAMES = [
    "edge_identity_closed_pair_count",
    "support_role_bridge_count",
    "high_bridge_cell_count",
    "high_bridge_left_count",
    "high_bridge_right_count",
    "high_bridge_mid_count",
    "high_bridge_low_count",
    "high_bridge_left_low_count",
    "high_bridge_mid_low_count",
    "high_bridge_right_center_count",
]


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--frontier-log",
        default="/Users/jonreilly/Projects/Physics/logs/2026-03-26-pocket-wrap-suppressor-nonpocket-subtype-rules-5504-max5600.txt",
    )
    parser.add_argument("--predicate-limit", type=int, default=18)
    parser.add_argument("--max-terms", type=int, default=3)
    parser.add_argument("--row-limit", type=int, default=6)
    parser.add_argument("--min-bucket-size", type=int, default=6)
    return parser


def main() -> None:
    args = build_parser().parse_args()
    started = datetime.now().isoformat(timespec="seconds")
    print(f"support family transfer bucket rules started {started}", flush=True)
    total_start = time.time()

    frontier_log = Path(args.frontier_log).resolve()
    rows = build_rows(frontier_log)
    grouped: dict[str, list[object]] = {}
    for row in rows:
        grouped.setdefault(row.family_bucket_key, []).append(row)

    kept = [
        (bucket_key, bucket_rows)
        for bucket_key, bucket_rows in grouped.items()
        if len(bucket_rows) >= args.min_bucket_size and len({row.subtype for row in bucket_rows}) > 1
    ]
    kept.sort(key=lambda item: (-len(item[1]), item[0]))

    print()
    print("Support Family Transfer Bucket Rules")
    print("====================================")
    print(f"frontier_log={frontier_log}")
    print(f"kept_buckets={[(key, len(rows0)) for key, rows0 in kept]}")
    print()
    for bucket_key, bucket_rows in kept:
        counts = Counter(row.subtype for row in bucket_rows)
        print(f"Bucket {bucket_key} count={len(bucket_rows)} subtype_counts={dict(counts)}")
        for subtype in sorted(counts):
            rules = evaluate_rules(
                bucket_rows,
                target_subtype=subtype,
                feature_names=FEATURE_NAMES,
                predicate_limit=args.predicate_limit,
                max_terms=args.max_terms,
                row_limit=args.row_limit,
            )
            print(render_rules(f"Best rules for {bucket_key} -> {subtype}", rules))
            print()
    print(
        "support family transfer bucket rules completed "
        + datetime.now().isoformat(timespec="seconds")
        + f" total_elapsed={time.time() - total_start:.1f}s",
        flush=True,
    )


if __name__ == "__main__":
    main()
