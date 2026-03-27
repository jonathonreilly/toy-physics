#!/usr/bin/env python3
"""Test whether the zero-distance candidate-cell motif generalizes to the broader baseline-covered add1 pool."""

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
    build_rows as build_pocket_rows,
)
from pocket_wrap_suppressor_low_overlap_center_spine_hardest_bucket_rules import (  # noqa: E402
    load_bucket_rows,
)
from toy_event_physics import pocket_candidate_cells  # noqa: E402


TARGET_CELLS = [
    ("pocket", (1, -2)),
    ("deep", (1, -2)),
    ("pocket", (2, 1)),
    ("deep", (2, 1)),
    ("pocket", (4, 2)),
    ("deep", (4, 2)),
    ("pocket", (5, 0)),
    ("deep", (5, 0)),
]


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
    return parser


def _has_cell(nodes: set[tuple[int, int]], kind: str, cell: tuple[int, int]) -> bool:
    pocket_cells, deep_cells = pocket_candidate_cells(nodes, wrap_y=False)
    if kind == "pocket":
        return cell in pocket_cells
    return cell in deep_cells


def main() -> None:
    args = build_parser().parse_args()
    started = datetime.now().isoformat(timespec="seconds")
    print(f"baseline candidate-cell generalization started {started}", flush=True)
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
    pocket_rows = build_pocket_rows(
        frontier_rows,
        bucket_rows,
        left_subtype=args.left_subtype,
        right_subtype=args.right_subtype,
    )

    rescued = [
        row for row in pocket_rows
        if getattr(row, "subtype") == args.left_subtype
        and float(getattr(row, "delta_edge_identity_support_edge_density")) > 0.018
        and float(getattr(row, "delta_count_pocket_total")) <= -14.5
    ]
    baseline_add1 = [
        row for row in pocket_rows
        if getattr(row, "subtype") == args.left_subtype
        and float(getattr(row, "delta_edge_identity_support_edge_density")) <= 0.018
    ]

    print()
    print("Center-Spine Bucket 00 Baseline Candidate-Cell Generalization")
    print("============================================================")
    print(f"rescued_count={len(rescued)}")
    print(f"baseline_add1_count={len(baseline_add1)}")
    print()

    for kind, cell in TARGET_CELLS:
        rescued_hits = [
            getattr(row, "source_name")
            for row in rescued
            if _has_cell(set(frontier_rows[getattr(row, 'source_name')].nodes), kind, cell)
        ]
        baseline_hits = [
            getattr(row, "source_name")
            for row in baseline_add1
            if _has_cell(set(frontier_rows[getattr(row, 'source_name')].nodes), kind, cell)
        ]
        print(f"{kind}_cell[{cell}]")
        print(f"  rescued_hits={len(rescued_hits)}/{len(rescued)}: {', '.join(rescued_hits) if rescued_hits else '(none)'}")
        print(f"  baseline_hits={len(baseline_hits)}/{len(baseline_add1)}: {', '.join(baseline_hits) if baseline_hits else '(none)'}")
    print()
    print(
        "baseline candidate-cell generalization completed "
        + datetime.now().isoformat(timespec="seconds")
        + f" total_elapsed={time.time() - total_start:.1f}s",
        flush=True,
    )


if __name__ == "__main__":
    main()
