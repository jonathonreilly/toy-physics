#!/usr/bin/env python3
"""Build baseline-side feature rows for rescued rows and basis-distance-zero baseline peers."""

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
from pocket_wrap_suppressor_low_overlap_center_spine_bucket00_support_topology import (  # noqa: E402
    evaluate_rules,
    render_rules,
)
from pocket_wrap_suppressor_low_overlap_center_spine_bucket00_support_edge_identity_pocket_subfamily_decomposition import (  # noqa: E402
    build_rows as build_pocket_rows,
)
from pocket_wrap_suppressor_low_overlap_center_spine_hardest_bucket_rules import (  # noqa: E402
    load_bucket_rows,
)
from pocket_wrap_suppressor_low_overlap_support_family_transfer_common import (  # noqa: E402
    support_edge_identity_own_metrics,
)


BASIS = [
    "delta_count_pocket_present0",
    "delta_count_pocket_present1",
    "delta_count_pocket_role_pocket_only__pocket_only",
    "delta_count_pocket_joined_pocket_only__pocket_only__present0",
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
    parser.add_argument("--predicate-limit", type=int, default=16)
    parser.add_argument("--max-terms", type=int, default=3)
    parser.add_argument("--row-limit", type=int, default=8)
    return parser


def _feature_distance(left: object, right: object, names: list[str]) -> float:
    return sum(abs(float(getattr(left, name)) - float(getattr(right, name))) for name in names)


def _own_metrics(nodes: set[tuple[int, int]]) -> dict[str, float]:
    return support_edge_identity_own_metrics(nodes)


def dataclass_feature_names(row: object) -> list[str]:
    return [
        name
        for name in row.__dataclass_fields__  # type: ignore[attr-defined]
        if name not in ("source_name", "group", "subtype")
    ]


def load_zero_distance_feature_rows(
    frontier_log: Path,
    bucket_log: Path,
    *,
    bucket_key: str,
    left_subtype: str,
    right_subtype: str,
) -> tuple[list[object], list[str], list[str]]:
    bucket_rows = [row for row in load_bucket_rows(bucket_log) if row.bucket_key == bucket_key]
    selected_sources = {row.source_name for row in bucket_rows}
    frontier_rows = {
        row.source_name: row
        for row in reconstruct_low_overlap_rows(frontier_log)
        if row.source_name in selected_sources
    }
    pocket_rows = build_pocket_rows(
        frontier_rows,
        bucket_rows,
        left_subtype=left_subtype,
        right_subtype=right_subtype,
    )

    rescued = [
        row for row in pocket_rows
        if getattr(row, "subtype") == left_subtype
        and float(getattr(row, "delta_edge_identity_support_edge_density")) > 0.018
        and float(getattr(row, "delta_count_pocket_total")) <= -14.5
    ]
    baseline_add1 = [
        row for row in pocket_rows
        if getattr(row, "subtype") == left_subtype
        and float(getattr(row, "delta_edge_identity_support_edge_density")) <= 0.018
    ]
    rescued_names = [getattr(row, "source_name") for row in rescued]
    zero_distance_names = set()
    for rescued_row in rescued:
        for other in baseline_add1:
            if _feature_distance(rescued_row, other, BASIS) == 0.0:
                zero_distance_names.add(getattr(other, "source_name"))

    selected = rescued_names + sorted(zero_distance_names)
    feature_dicts = []
    all_feature_names: set[str] = set()
    for source_name in selected:
        group = "rescued" if source_name in rescued_names else "baseline_peer"
        metrics = _own_metrics(set(frontier_rows[source_name].nodes))
        feature_dicts.append((source_name, group, metrics))
        all_feature_names.update(metrics)

    row_cls = make_dataclass(
        "BaselineZeroDistanceRow",
        [("source_name", str), ("group", str), ("subtype", str)]
        + [(name, float) for name in sorted(all_feature_names)],
        frozen=True,
    )
    rows = []
    for source_name, group, metrics in feature_dicts:
        values = {name: 0.0 for name in sorted(all_feature_names)}
        values.update(metrics)
        rows.append(row_cls(source_name=source_name, group=group, subtype=group, **values))
    rows.sort(key=lambda row: (getattr(row, "group"), getattr(row, "source_name")))
    return rows, rescued_names, sorted(zero_distance_names)


def render_rows(rows: list[object], feature_names: list[str]) -> str:
    shown = [
        "source_name",
        "group",
        "edge_identity_support_edge_density",
        "support_edge_count",
        "support_node_count",
        "edge_identity_closed_pair_count",
        "edge_identity_open_pair_count",
        "support_role_bridge_count",
        "support_role_pocket_only_count",
        "support_edge_role_bridge__bridge_count",
        "support_edge_role_bridge__pocket_only_count",
        "support_edge_role_pocket_only__pocket_only_count",
    ]
    lines = [
        "Baseline-side zero-distance feature rows",
        "=======================================",
        " | ".join(shown),
        " | ".join("-" * len(name) for name in shown),
    ]
    for row in rows:
        values = []
        for name in shown:
            value = getattr(row, name, 0.0)
            if isinstance(value, float):
                values.append(f"{value:.3f}")
            else:
                values.append(str(value))
        lines.append(" | ".join(values))
    return "\n".join(lines)


def main() -> None:
    args = build_parser().parse_args()
    started = datetime.now().isoformat(timespec="seconds")
    print(f"center-spine bucket00 baseline zero-distance features started {started}", flush=True)
    total_start = time.time()

    frontier_log = Path(args.frontier_log).resolve()
    bucket_log = Path(args.bucket_log).resolve()
    rows, rescued_names, zero_distance_names = load_zero_distance_feature_rows(
        frontier_log,
        bucket_log,
        bucket_key=args.bucket_key,
        left_subtype=args.left_subtype,
        right_subtype=args.right_subtype,
    )

    feature_names = dataclass_feature_names(rows[0])
    rescued_rules = evaluate_rules(
        rows,
        target_subtype="rescued",
        feature_names=feature_names,
        predicate_limit=args.predicate_limit,
        max_terms=args.max_terms,
        row_limit=args.row_limit,
    )
    baseline_rules = evaluate_rules(
        rows,
        target_subtype="baseline_peer",
        feature_names=feature_names,
        predicate_limit=args.predicate_limit,
        max_terms=args.max_terms,
        row_limit=args.row_limit,
    )

    print()
    print("Center-Spine Bucket 00 Baseline Zero-Distance Features")
    print("======================================================")
    print(f"frontier_log={frontier_log}")
    print(f"bucket_log={bucket_log}")
    print(f"bucket_key={args.bucket_key}")
    print(f"rescued_sources={', '.join(rescued_names)}")
    print(f"baseline_peer_sources={', '.join(zero_distance_names)}")
    print()
    print(render_rows(rows, feature_names))
    print()
    print(render_rules("Best rescued-vs-baseline zero-distance rules", rescued_rules))
    print()
    print(render_rules("Best baseline-vs-rescued zero-distance rules", baseline_rules))
    print()
    print(
        "center-spine bucket00 baseline zero-distance features completed "
        + datetime.now().isoformat(timespec="seconds")
        + f" total_elapsed={time.time() - total_start:.1f}s",
        flush=True,
    )


if __name__ == "__main__":
    main()
