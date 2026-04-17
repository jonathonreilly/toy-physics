#!/usr/bin/env python3
"""Search exact candidate-cell presence rules on the zero-distance rescued/peer rows."""

from __future__ import annotations

import argparse
from dataclasses import make_dataclass
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
from pocket_wrap_suppressor_low_overlap_center_spine_bucket00_support_edge_identity_baseline_zero_distance_equivalence_scan import (  # noqa: E402
    Predicate,
    _critical_thresholds,
    _mask_for,
    _metrics,
    _stable_interval,
)
from pocket_wrap_suppressor_low_overlap_center_spine_bucket00_support_edge_identity_baseline_zero_distance_features import (  # noqa: E402
    BASIS,
)
from pocket_wrap_suppressor_low_overlap_center_spine_bucket00_support_edge_identity_pocket_subfamily_decomposition import (  # noqa: E402
    build_rows as build_pocket_rows,
)
from pocket_wrap_suppressor_low_overlap_center_spine_hardest_bucket_rules import (  # noqa: E402
    load_bucket_rows,
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
    parser.add_argument("--bucket-key", default="00")
    parser.add_argument("--left-subtype", default="add1-sensitive")
    parser.add_argument("--right-subtype", default="add4-sensitive")
    parser.add_argument("--row-limit", type=int, default=16)
    return parser


def _feature_distance(left: object, right: object, names: list[str]) -> float:
    return sum(abs(float(getattr(left, name)) - float(getattr(right, name))) for name in names)


def _cell_feature_name(prefix: str, cell: tuple[int, int]) -> str:
    x, y = cell
    y_label = f"n{abs(y)}" if y < 0 else str(y)
    return f"{prefix}_cell_{x}_{y_label}"


def main() -> None:
    args = build_parser().parse_args()
    started = datetime.now().isoformat(timespec="seconds")
    print(f"baseline zero-distance candidate-cell rules started {started}", flush=True)
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
    rescued_names = [getattr(row, "source_name") for row in rescued]
    zero_distance_names = sorted(
        {
            getattr(other, "source_name")
            for rescued_row in rescued
            for other in baseline_add1
            if _feature_distance(rescued_row, other, BASIS) == 0.0
        }
    )
    selected_names = rescued_names + zero_distance_names

    row_cells = {}
    feature_to_cell: dict[str, tuple[str, tuple[int, int]]] = {}
    all_cell_names: set[str] = set()
    for source_name in selected_names:
        pocket_cells, deep_cells = pocket_candidate_cells(set(frontier_rows[source_name].nodes), wrap_y=False)
        features = {}
        for cell in sorted(pocket_cells):
            name = _cell_feature_name("pocket", cell)
            features[name] = 1.0
            all_cell_names.add(name)
            feature_to_cell[name] = ("pocket", cell)
        for cell in sorted(deep_cells):
            name = _cell_feature_name("deep", cell)
            features[name] = 1.0
            all_cell_names.add(name)
            feature_to_cell[name] = ("deep", cell)
        row_cells[source_name] = features

    row_cls = make_dataclass(
        "BaselineZeroDistanceCellRow",
        [("source_name", str), ("group", str), ("subtype", str)] + [(name, float) for name in sorted(all_cell_names)],
        frozen=True,
    )
    rows = []
    for source_name in selected_names:
        group = "rescued" if source_name in rescued_names else "baseline_peer"
        values = {name: 0.0 for name in sorted(all_cell_names)}
        values.update(row_cells[source_name])
        rows.append(row_cls(source_name=source_name, group=group, subtype=group, **values))
    rows.sort(key=lambda row: (getattr(row, "group"), getattr(row, "source_name")))

    rescued_mask = 0
    baseline_mask = 0
    for idx, row in enumerate(rows):
        if getattr(row, "group") == "rescued":
            rescued_mask |= 1 << idx
        else:
            baseline_mask |= 1 << idx

    exact_rows = []
    feature_names = [name for name in rows[0].__dataclass_fields__ if name not in ("source_name", "group", "subtype")]
    for name in feature_names:
        for threshold in _critical_thresholds(rows, name):
            for op in ("<=", ">="):
                pred = Predicate(name=name, op=op, threshold=threshold, mask=_mask_for(rows, name, op, threshold))
                metrics = _metrics(pred.mask, rescued_mask, baseline_mask, len(rows))
                if metrics != (2, 0, 0):
                    continue
                interval = _stable_interval(rows, pred)
                exact_rows.append((interval[2], pred, interval))
    exact_rows.sort(key=lambda item: (-item[0], item[1].text))

    print()
    print("Center-Spine Bucket 00 Baseline Zero-Distance Candidate Cell Rules")
    print("==================================================================")
    print(f"rescued_sources={', '.join(rescued_names)}")
    print(f"baseline_peer_sources={', '.join(zero_distance_names)}")
    print()
    print("Exact candidate-cell one-term rules")
    print("-----------------------------------")
    if not exact_rows:
        print("none")
    else:
        for idx, (width, pred, interval) in enumerate(exact_rows[: args.row_limit], start=1):
            kind, cell = feature_to_cell[pred.name]
            print(
                f"{idx}. {pred.text} [{kind} cell {cell}] "
                + f"width={width:.3f} interval={interval[3]}"
            )
    print()
    print("Per-row candidate cells")
    print("-----------------------")
    for row in rows:
        present = [name for name in feature_names if float(getattr(row, name)) > 0.5]
        print(f"{getattr(row, 'source_name')} ({getattr(row, 'group')})")
        for name in present:
            kind, cell = feature_to_cell[name]
            print(f"  {name} [{kind} cell {cell}]")
    print()
    print(
        "baseline zero-distance candidate-cell rules completed "
        + datetime.now().isoformat(timespec="seconds")
        + f" total_elapsed={time.time() - total_start:.1f}s",
        flush=True,
    )


if __name__ == "__main__":
    main()
