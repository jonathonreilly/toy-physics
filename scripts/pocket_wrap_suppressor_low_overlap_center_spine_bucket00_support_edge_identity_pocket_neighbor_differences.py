#!/usr/bin/env python3
"""Compare rescued rows to nearest non-rescued add1 neighbors in the visible pocket basis."""

from __future__ import annotations

import argparse
from datetime import datetime
from math import sqrt
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
    parser.add_argument("--neighbors", type=int, default=3)
    return parser


BASIS = [
    "delta_count_pocket_present0",
    "delta_count_pocket_present1",
    "delta_count_pocket_role_pocket_only__pocket_only",
    "delta_count_pocket_joined_pocket_only__pocket_only__present0",
]


def _distance(left: object, right: object) -> float:
    total = 0.0
    for feature in BASIS:
        delta = float(getattr(left, feature)) - float(getattr(right, feature))
        total += delta * delta
    return sqrt(total)


def _feature_deltas(left: object, right: object) -> list[str]:
    lines = []
    for feature in BASIS:
        lval = float(getattr(left, feature))
        rval = float(getattr(right, feature))
        lines.append(f"{feature}: {lval:.1f} -> {rval:.1f} (delta {rval - lval:+.1f})")
    return lines


def main() -> None:
    args = build_parser().parse_args()
    started = datetime.now().isoformat(timespec="seconds")
    print(f"center-spine bucket00 pocket-neighbor differences started {started}", flush=True)
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
    raw_by_name = {row.source_name: row for row in frontier_rows.values()}

    rows = build_rows(
        frontier_rows,
        bucket_rows,
        left_subtype=args.left_subtype,
        right_subtype=args.right_subtype,
    )
    by_name = {getattr(row, "source_name"): row for row in rows}

    rescued = [
        row for row in rows
        if getattr(row, "subtype") == args.left_subtype
        and float(getattr(row, "delta_edge_identity_support_edge_density")) > 0.018
    ]
    non_rescued_add1 = [
        row for row in rows
        if getattr(row, "subtype") == args.left_subtype
        and float(getattr(row, "delta_edge_identity_support_edge_density")) <= 0.018
    ]

    print()
    print("Center-Spine Bucket 00 Pocket Neighbor Differences")
    print("==================================================")
    print(f"frontier_log={frontier_log}")
    print(f"bucket_log={bucket_log}")
    print(f"bucket_key={args.bucket_key}")
    print(f"rescued_rows={', '.join(getattr(row, 'source_name') for row in rescued)}")
    print()

    for rescued_row in rescued:
        rescued_name = getattr(rescued_row, "source_name")
        raw_rescued = raw_by_name[rescued_name]
        ranked = sorted(
            (
                _distance(rescued_row, other),
                getattr(other, "source_name"),
                other,
            )
            for other in non_rescued_add1
        )
        print(rescued_name)
        print(f"  node_count={len(raw_rescued.nodes)}")
        print(f"  basis={', '.join(f'{feature}={float(getattr(rescued_row, feature)):.1f}' for feature in BASIS)}")
        for idx, (distance, neighbor_name, neighbor_row) in enumerate(ranked[: args.neighbors], start=1):
            raw_neighbor = raw_by_name[neighbor_name]
            removed = sorted(set(raw_rescued.nodes) - set(raw_neighbor.nodes))
            added = sorted(set(raw_neighbor.nodes) - set(raw_rescued.nodes))
            print(f"  neighbor {idx}: {neighbor_name} distance={distance:.3f}")
            for line in _feature_deltas(rescued_row, neighbor_row):
                print(f"    {line}")
            print(f"    removed_nodes={removed[:12]}")
            print(f"    added_nodes={added[:12]}")
        print()

    print(
        "center-spine bucket00 pocket-neighbor differences completed "
        + datetime.now().isoformat(timespec="seconds")
        + f" total_elapsed={time.time() - total_start:.1f}s",
        flush=True,
    )


if __name__ == "__main__":
    main()
