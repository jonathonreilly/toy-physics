#!/usr/bin/env python3
"""Explain why many pocket-basis thresholds recover the same rescued-row mask."""

from __future__ import annotations

import argparse
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

from pocket_wrap_suppressor_low_overlap_boundary_axes import (  # noqa: E402
    reconstruct_low_overlap_rows,
)
from pocket_wrap_suppressor_low_overlap_center_spine_bucket00_support_edge_identity_pocket_subfamily_decomposition import (  # noqa: E402
    build_rows,
)
from pocket_wrap_suppressor_low_overlap_center_spine_hardest_bucket_rules import (  # noqa: E402
    load_bucket_rows,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--frontier-log",
        default="/Users/jonreilly/Projects/Physics/logs/2026-03-26-pocket-wrap-suppressor-nonpocket-subtype-rules-5504-max5600.txt",
    )
    parser.add_argument(
        "--bucket-log",
        default="/Users/jonreilly/Projects/Physics/logs/2026-03-26-pocket-wrap-suppressor-low-overlap-center-spine-micro-buckets-5504-add1-vs-add4.txt",
    )
    parser.add_argument("--bucket-key", default="00")
    parser.add_argument("--left-subtype", default="add1-sensitive")
    parser.add_argument("--right-subtype", default="add4-sensitive")
    parser.add_argument(
        "--basis-features",
        nargs="+",
        default=[
            "delta_count_pocket_present0",
            "delta_count_pocket_present1",
            "delta_count_pocket_role_pocket_only__pocket_only",
            "delta_count_pocket_joined_pocket_only__pocket_only__present0",
        ],
    )
    return parser


def main() -> None:
    args = build_parser().parse_args()
    started = datetime.now().isoformat(timespec="seconds")
    print(f"center-spine bucket00 pocket-basis margin profiles started {started}", flush=True)
    total_start = time.time()

    frontier_log = Path(args.frontier_log).resolve()
    bucket_log = Path(args.bucket_log).resolve()
    bucket_rows = [row for row in load_bucket_rows(bucket_log) if row.bucket_key == args.bucket_key]
    selected_sources = {row.source_name for row in bucket_rows}
    frontier_rows = {
        row.source_name: row
        for row in reconstruct_low_overlap_rows(frontier_log)
        if row.source_name in selected_sources
    }
    rows = build_rows(
        frontier_rows,
        bucket_rows,
        left_subtype=args.left_subtype,
        right_subtype=args.right_subtype,
    )

    rescued = [
        row for row in rows
        if getattr(row, "subtype") == args.left_subtype
        and float(getattr(row, "delta_edge_identity_support_edge_density")) > 0.018
    ]
    rescued_names = [getattr(row, "source_name") for row in rescued]
    others = [row for row in rows if getattr(row, "source_name") not in rescued_names]

    print()
    print("Center-Spine Bucket 00 Pocket-Basis Margin Profiles")
    print("===================================================")
    print(f"frontier_log={frontier_log}")
    print(f"bucket_log={bucket_log}")
    print(f"bucket_key={args.bucket_key}")
    print(f"rescued_sources={', '.join(rescued_names)}")
    print()

    for feature in args.basis_features:
        rescued_values = sorted(float(getattr(row, feature)) for row in rescued)
        other_values = sorted(float(getattr(row, feature)) for row in others)
        rescued_min = min(rescued_values)
        rescued_max = max(rescued_values)
        next_above = min((value for value in other_values if value > rescued_max), default=None)
        next_below = max((value for value in other_values if value < rescued_min), default=None)
        left_gap = None if next_below is None else rescued_min - next_below
        right_gap = None if next_above is None else next_above - rescued_max
        print(feature)
        print(f"  rescued_values={rescued_values}")
        print(f"  non_rescued_minmax=[{other_values[0]:.3f}, {other_values[-1]:.3f}]")
        print(f"  next_below={next_below if next_below is not None else 'none'}")
        print(f"  next_above={next_above if next_above is not None else 'none'}")
        print(f"  left_gap={left_gap if left_gap is not None else 'none'}")
        print(f"  right_gap={right_gap if right_gap is not None else 'none'}")
        print()

    print(
        "center-spine bucket00 pocket-basis margin profiles completed "
        + datetime.now().isoformat(timespec="seconds")
        + f" total_elapsed={time.time() - total_start:.1f}s",
        flush=True,
    )


if __name__ == "__main__":
    main()
