#!/usr/bin/env python3
"""Summarize repeated baseline-peer extras between rescued rows and basis-identical baseline peers."""

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

from pocket_wrap_suppressor_low_overlap_boundary_axes import (  # noqa: E402
    reconstruct_low_overlap_rows,
)
from pocket_wrap_suppressor_low_overlap_center_spine_bucket00_support_edge_identity_add1_selector import (  # noqa: E402
    _support_edges,
    support_roles,
)
from pocket_wrap_suppressor_low_overlap_center_spine_bucket00_support_edge_identity_pocket_subfamily_decomposition import (  # noqa: E402
    build_rows as build_pocket_rows,
)
from pocket_wrap_suppressor_low_overlap_center_spine_hardest_bucket_rules import (  # noqa: E402
    load_bucket_rows,
)
from toy_event_physics import graph_neighbors, pocket_candidate_cells  # noqa: E402


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
    parser.add_argument("--show-limit", type=int, default=12)
    return parser


def _feature_distance(left: object, right: object, names: list[str]) -> float:
    return sum(abs(float(getattr(left, name)) - float(getattr(right, name))) for name in names)


def _role_pair(a: str, b: str) -> str:
    return "__".join(sorted((a, b)))


def _support_summary(nodes: set[tuple[int, int]]) -> dict[str, Counter]:
    pocket_cells, deep_cells = pocket_candidate_cells(nodes, wrap_y=False)
    roles = support_roles(nodes, pocket_cells, deep_cells)
    support_nodes = set(roles)
    support_edges = _support_edges(support_nodes)

    support_role_counts = Counter(roles.values())
    support_edge_role_counts = Counter(_role_pair(roles[left], roles[right]) for left, right in support_edges)

    return {
        "support_role_counts": support_role_counts,
        "support_edge_role_counts": support_edge_role_counts,
        "support_nodes": Counter(support_nodes),
        "support_edges": Counter(support_edges),
        "pocket_cells": Counter(pocket_cells),
        "deep_cells": Counter(deep_cells),
    }


def _positive_delta(a: Counter, b: Counter) -> list[tuple[str, int]]:
    items = []
    for key in set(a) | set(b):
        delta = b[key] - a[key]
        if delta > 0:
            items.append((str(key), int(delta)))
    items.sort(key=lambda item: (-item[1], item[0]))
    return items


def main() -> None:
    args = build_parser().parse_args()
    started = datetime.now().isoformat(timespec="seconds")
    print(f"center-spine bucket00 baseline zero-distance layout diff started {started}", flush=True)
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

    repeated_role = Counter()
    repeated_edge_role = Counter()
    repeated_pocket = Counter()
    repeated_deep = Counter()

    print()
    print("Center-Spine Bucket 00 Baseline Zero-Distance Layout Difference")
    print("==============================================================")
    print(f"frontier_log={frontier_log}")
    print(f"bucket_log={bucket_log}")
    print(f"bucket_key={args.bucket_key}")
    print(f"rescued_sources={', '.join(rescued_names)}")
    print(f"baseline_peer_sources={', '.join(zero_distance_names)}")
    print()

    for rescued_name in rescued_names:
        rescued_summary = _support_summary(set(frontier_rows[rescued_name].nodes))
        print(f"Rescued row={rescued_name}")
        for peer_name in zero_distance_names:
            peer_summary = _support_summary(set(frontier_rows[peer_name].nodes))
            print(f"  peer={peer_name}")
            role_delta = _positive_delta(rescued_summary["support_role_counts"], peer_summary["support_role_counts"])
            edge_role_delta = _positive_delta(rescued_summary["support_edge_role_counts"], peer_summary["support_edge_role_counts"])
            pocket_delta = _positive_delta(rescued_summary["pocket_cells"], peer_summary["pocket_cells"])
            deep_delta = _positive_delta(rescued_summary["deep_cells"], peer_summary["deep_cells"])
            for key, value in role_delta:
                repeated_role[key] += 1
                print(f"    peer+{value} support_role[{key}]")
            for key, value in edge_role_delta[: args.show_limit]:
                repeated_edge_role[key] += 1
                print(f"    peer+{value} support_edge_role[{key}]")
            for key, value in pocket_delta[: args.show_limit]:
                repeated_pocket[key] += 1
                print(f"    peer+{value} pocket_cell[{key}]")
            for key, value in deep_delta[: args.show_limit]:
                repeated_deep[key] += 1
                print(f"    peer+{value} deep_cell[{key}]")
        print()

    print("Repeated positive peer-minus-rescued deltas across rescued/peer comparisons")
    print("--------------------------------------------------------------------------")
    print("support roles:")
    for key, count in repeated_role.most_common(args.show_limit):
        print(f"  {key}: {count}")
    print("support edge roles:")
    for key, count in repeated_edge_role.most_common(args.show_limit):
        print(f"  {key}: {count}")
    print("pocket cells:")
    for key, count in repeated_pocket.most_common(args.show_limit):
        print(f"  {key}: {count}")
    print("deep cells:")
    for key, count in repeated_deep.most_common(args.show_limit):
        print(f"  {key}: {count}")
    print()

    print(
        "center-spine bucket00 baseline zero-distance layout diff completed "
        + datetime.now().isoformat(timespec="seconds")
        + f" total_elapsed={time.time() - total_start:.1f}s",
        flush=True,
    )


if __name__ == "__main__":
    main()
