#!/usr/bin/env python3
"""Compare center-spine hardest-bucket add4 rows to their nearest visible add1 neighbors."""

from __future__ import annotations

import argparse
from datetime import datetime
from math import sqrt
from pathlib import Path
import statistics
import time

from pocket_wrap_suppressor_low_overlap_center_spine_hardest_bucket_rules import (
    VISIBLE_FEATURES,
    BucketRow,
    load_bucket_rows,
    mixed_buckets,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--log",
        default="/Users/jonreilly/Projects/Physics/logs/2026-03-26-pocket-wrap-suppressor-low-overlap-center-spine-micro-buckets-5504-add1-vs-add4.txt",
    )
    parser.add_argument("--left-subtype", default="add1-sensitive")
    parser.add_argument("--right-subtype", default="add4-sensitive")
    return parser


def zscore_stats(rows: list[BucketRow]) -> dict[str, tuple[float, float]]:
    stats: dict[str, tuple[float, float]] = {}
    for feature in VISIBLE_FEATURES:
        values = [row.features[feature] for row in rows]
        mean = statistics.mean(values)
        std = statistics.pstdev(values)
        stats[feature] = (mean, std if std > 0 else 1.0)
    return stats


def zdistance(left: BucketRow, right: BucketRow, stats: dict[str, tuple[float, float]]) -> float:
    total = 0.0
    for feature in VISIBLE_FEATURES:
        mean, std = stats[feature]
        delta = (left.features[feature] - right.features[feature]) / std
        total += delta * delta
    return sqrt(total)


def render_match(add4_row: BucketRow, add1_row: BucketRow, *, stats: dict[str, tuple[float, float]]) -> str:
    lines = [
        f"add4={add4_row.source_name}",
        f"nearest_add1={add1_row.source_name}",
        f"distance={zdistance(add4_row, add1_row, stats):.3f}",
    ]
    for feature in VISIBLE_FEATURES:
        delta = add4_row.features[feature] - add1_row.features[feature]
        lines.append(
            f"  {feature}: add4={add4_row.features[feature]:.3f} "
            f"add1={add1_row.features[feature]:.3f} delta={delta:+.3f}"
        )
    return "\n".join(lines)


def main() -> None:
    args = build_parser().parse_args()
    started = datetime.now().isoformat(timespec="seconds")
    print(f"center-spine hardest bucket neighbors started {started}", flush=True)
    total_start = time.time()

    log_path = Path(args.log).resolve()
    rows = load_bucket_rows(log_path)
    mixed = mixed_buckets(rows, add4_subtype=args.right_subtype)
    hardest_key, hardest_rows = max(
        mixed,
        key=lambda item: (len(item[1]), sum(row.subtype == args.right_subtype for row in item[1])),
    )

    stats = zscore_stats(hardest_rows)
    add4_rows = [row for row in hardest_rows if row.subtype == args.right_subtype]
    add1_rows = [row for row in hardest_rows if row.subtype == args.left_subtype]

    print()
    print("Center-Spine Hardest-Bucket Nearest Neighbors")
    print("============================================")
    print(f"log={log_path}")
    print(f"selected_bucket={hardest_key} rows={len(hardest_rows)}")
    print(f"counts={args.left_subtype}:{len(add1_rows)} {args.right_subtype}:{len(add4_rows)}")
    print()

    for add4_row in add4_rows:
        nearest = min(add1_rows, key=lambda row: zdistance(add4_row, row, stats))
        print(render_match(add4_row, nearest, stats=stats))
        print()

    print(
        "center-spine hardest bucket neighbors completed "
        + datetime.now().isoformat(timespec="seconds")
        + f" total_elapsed={time.time() - total_start:.1f}s",
        flush=True,
    )


if __name__ == "__main__":
    main()
