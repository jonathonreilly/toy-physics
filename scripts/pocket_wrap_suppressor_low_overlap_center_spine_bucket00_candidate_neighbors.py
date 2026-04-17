#!/usr/bin/env python3
"""Compare explicit candidate-cell layouts for the `00` add4 rows and nearest add1 neighbors."""

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
from pocket_wrap_suppressor_low_overlap_center_spine_hardest_bucket_rules import (  # noqa: E402
    BucketRow,
    VISIBLE_FEATURES,
    load_bucket_rows,
    mixed_buckets,
)
from toy_event_physics import pocket_candidate_cells  # noqa: E402


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
    parser.add_argument("--left-subtype", default="add1-sensitive")
    parser.add_argument("--right-subtype", default="add4-sensitive")
    return parser


def zscore_stats(rows: list[BucketRow]) -> dict[str, tuple[float, float]]:
    import statistics

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
        _mean, std = stats[feature]
        delta = (left.features[feature] - right.features[feature]) / std
        total += delta * delta
    return sqrt(total)


def relative_cells(cells: set[tuple[int, int]]) -> list[tuple[int, int]]:
    if not cells:
        return []
    min_x = min(x for x, _y in cells)
    min_y = min(y for _x, y in cells)
    return sorted((x - min_x, y - min_y) for x, y in cells)


def candidate_layout(nodes: frozenset[tuple[int, int]]) -> dict[str, list[tuple[int, int]]]:
    pocket_cells, deep_cells = pocket_candidate_cells(set(nodes), wrap_y=False)
    overlap = pocket_cells & deep_cells
    return {
        "pocket": relative_cells(pocket_cells),
        "deep": relative_cells(deep_cells),
        "overlap": relative_cells(overlap),
        "pocket_only": relative_cells(pocket_cells - deep_cells),
        "deep_only": relative_cells(deep_cells - pocket_cells),
    }


def render_pair(add4_row: BucketRow, add1_row: BucketRow, *, add4_nodes: frozenset[tuple[int, int]], add1_nodes: frozenset[tuple[int, int]], stats: dict[str, tuple[float, float]]) -> str:
    add4_layout = candidate_layout(add4_nodes)
    add1_layout = candidate_layout(add1_nodes)
    lines = [
        f"add4={add4_row.source_name}",
        f"nearest_add1={add1_row.source_name}",
        f"distance={zdistance(add4_row, add1_row, stats):.3f}",
    ]
    for key in ("pocket", "deep", "overlap", "pocket_only", "deep_only"):
        lines.append(f"  add4_{key}={add4_layout[key]}")
        lines.append(f"  add1_{key}={add1_layout[key]}")
        lines.append(
            f"  only_in_add4_{key}={sorted(set(add4_layout[key]) - set(add1_layout[key]))}"
        )
        lines.append(
            f"  only_in_add1_{key}={sorted(set(add1_layout[key]) - set(add4_layout[key]))}"
        )
    return "\n".join(lines)


def main() -> None:
    args = build_parser().parse_args()
    started = datetime.now().isoformat(timespec="seconds")
    print(f"center-spine bucket00 candidate neighbors started {started}", flush=True)
    total_start = time.time()

    frontier_log = Path(args.frontier_log).resolve()
    bucket_log = Path(args.bucket_log).resolve()

    bucket_rows = load_bucket_rows(bucket_log)
    mixed = mixed_buckets(bucket_rows, add4_subtype=args.right_subtype)
    hardest_key, hardest_rows = max(
        mixed,
        key=lambda item: (len(item[1]), sum(row.subtype == args.right_subtype for row in item[1])),
    )
    stats = zscore_stats(hardest_rows)

    frontier_rows = {
        row.source_name: row
        for row in reconstruct_low_overlap_rows(frontier_log)
        if row.source_name in {bucket_row.source_name for bucket_row in hardest_rows}
    }
    add4_rows = [row for row in hardest_rows if row.subtype == args.right_subtype]
    add1_rows = [row for row in hardest_rows if row.subtype == args.left_subtype]

    print()
    print("Center-Spine Bucket 00 Candidate-Cell Neighbors")
    print("===============================================")
    print(f"frontier_log={frontier_log}")
    print(f"bucket_log={bucket_log}")
    print(f"bucket_key={hardest_key} rows={len(hardest_rows)}")
    print()

    for add4_row in add4_rows:
        nearest = min(add1_rows, key=lambda row: zdistance(add4_row, row, stats))
        print(
            render_pair(
                add4_row,
                nearest,
                add4_nodes=frontier_rows[add4_row.source_name].nodes,
                add1_nodes=frontier_rows[nearest.source_name].nodes,
                stats=stats,
            )
        )
        print()

    print(
        "center-spine bucket00 candidate neighbors completed "
        + datetime.now().isoformat(timespec="seconds")
        + f" total_elapsed={time.time() - total_start:.1f}s",
        flush=True,
    )


if __name__ == "__main__":
    main()
