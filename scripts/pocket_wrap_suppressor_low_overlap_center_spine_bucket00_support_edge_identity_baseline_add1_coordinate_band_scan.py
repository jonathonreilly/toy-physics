#!/usr/bin/env python3
"""Test whether the baseline add1 peer branch compresses to coarse position bands over high-bridge candidate cells."""

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
from pocket_wrap_suppressor_low_overlap_center_spine_bucket00_support_edge_identity_add1_selector import (  # noqa: E402
    _support_edges,
    support_roles,
)
from pocket_wrap_suppressor_low_overlap_center_spine_bucket00_support_edge_identity_baseline_add1_branch_decomposition import (  # noqa: E402
    MOTIF_CELLS,
    _has_motif,
)
from pocket_wrap_suppressor_low_overlap_center_spine_bucket00_support_edge_identity_pocket_subfamily_decomposition import (  # noqa: E402
    build_rows as build_pocket_rows,
)
from pocket_wrap_suppressor_low_overlap_center_spine_bucket00_support_topology import (  # noqa: E402
    evaluate_rules,
    render_rules,
)
from pocket_wrap_suppressor_low_overlap_center_spine_hardest_bucket_rules import (  # noqa: E402
    load_bucket_rows,
)
from toy_event_physics import graph_neighbors, pocket_candidate_cells  # noqa: E402


HIGH_BRIDGE_THRESHOLD = 7.0


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
    parser.add_argument("--predicate-limit", type=int, default=24)
    parser.add_argument("--max-terms", type=int, default=3)
    parser.add_argument("--row-limit", type=int, default=10)
    return parser


def _high_bridge_cells(nodes: set[tuple[int, int]]) -> list[tuple[int, int]]:
    pocket_cells, deep_cells = pocket_candidate_cells(nodes, wrap_y=False)
    candidate_cells = pocket_cells | deep_cells
    roles = support_roles(nodes, pocket_cells, deep_cells)
    support_nodes = set(roles)

    candidate_to_supports: dict[tuple[int, int], set[tuple[int, int]]] = {}
    for support in support_nodes:
        adjacent = set(graph_neighbors(support, support_nodes | candidate_cells, wrap_y=False))
        attached = adjacent & candidate_cells
        for cell in attached:
            candidate_to_supports.setdefault(cell, set()).add(support)

    out = []
    for cell in sorted(candidate_cells):
        attached = candidate_to_supports.get(cell, set())
        bridge_count = float(sum(1 for node in attached if roles.get(node) == "bridge"))
        if bridge_count >= HIGH_BRIDGE_THRESHOLD:
            out.append(cell)
    return out


def _band_metrics(cells: list[tuple[int, int]]) -> dict[str, float]:
    def count(fn) -> float:
        return float(sum(1 for cell in cells if fn(cell)))

    return {
        "high_bridge_cell_count": float(len(cells)),
        "high_bridge_left_count": count(lambda cell: cell[0] <= 1),
        "high_bridge_right_count": count(lambda cell: cell[0] >= 5),
        "high_bridge_mid_count": count(lambda cell: 2 <= cell[0] <= 4),
        "high_bridge_low_count": count(lambda cell: cell[1] <= -1),
        "high_bridge_center_count": count(lambda cell: cell[1] == 0),
        "high_bridge_high_count": count(lambda cell: cell[1] >= 1),
        "high_bridge_left_low_count": count(lambda cell: cell[0] <= 1 and cell[1] <= -1),
        "high_bridge_left_center_count": count(lambda cell: cell[0] <= 1 and cell[1] == 0),
        "high_bridge_right_low_count": count(lambda cell: cell[0] >= 5 and cell[1] <= -1),
        "high_bridge_right_center_count": count(lambda cell: cell[0] >= 5 and cell[1] == 0),
        "high_bridge_mid_low_count": count(lambda cell: 2 <= cell[0] <= 4 and cell[1] <= -1),
        "high_bridge_mid_center_count": count(lambda cell: 2 <= cell[0] <= 4 and cell[1] == 0),
        "high_bridge_mid_high_count": count(lambda cell: 2 <= cell[0] <= 4 and cell[1] >= 1),
    }


def main() -> None:
    args = build_parser().parse_args()
    started = datetime.now().isoformat(timespec="seconds")
    print(f"baseline add1 coordinate band scan started {started}", flush=True)
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
    baseline_rows = [
        row
        for row in pocket_rows
        if getattr(row, "subtype") == args.left_subtype
        and float(getattr(row, "delta_edge_identity_support_edge_density")) <= 0.018
    ]

    row_cls = make_dataclass(
        "BaselineAdd1CoordinateBandRow",
        [("source_name", str), ("subtype", str)] + [
            ("high_bridge_cell_count", float),
            ("high_bridge_left_count", float),
            ("high_bridge_right_count", float),
            ("high_bridge_mid_count", float),
            ("high_bridge_low_count", float),
            ("high_bridge_center_count", float),
            ("high_bridge_high_count", float),
            ("high_bridge_left_low_count", float),
            ("high_bridge_left_center_count", float),
            ("high_bridge_right_low_count", float),
            ("high_bridge_right_center_count", float),
            ("high_bridge_mid_low_count", float),
            ("high_bridge_mid_center_count", float),
            ("high_bridge_mid_high_count", float),
        ],
        frozen=True,
    )

    rows = []
    for row in baseline_rows:
        source_name = getattr(row, "source_name")
        cells = _high_bridge_cells(set(frontier_rows[source_name].nodes))
        rows.append(
            row_cls(
                source_name=source_name,
                subtype="peer_motif" if _has_motif(set(frontier_rows[source_name].nodes), MOTIF_CELLS[0]) else "non_peer",
                **_band_metrics(cells),
            )
        )
    rows.sort(key=lambda item: getattr(item, "source_name"))

    feature_names = [name for name in rows[0].__dataclass_fields__ if name not in ("source_name", "subtype")]
    peer_rules = evaluate_rules(
        rows,
        target_subtype="peer_motif",
        feature_names=feature_names,
        predicate_limit=args.predicate_limit,
        max_terms=args.max_terms,
        row_limit=args.row_limit,
    )
    non_peer_rules = evaluate_rules(
        rows,
        target_subtype="non_peer",
        feature_names=feature_names,
        predicate_limit=args.predicate_limit,
        max_terms=args.max_terms,
        row_limit=args.row_limit,
    )

    print()
    print("Center-Spine Bucket 00 Baseline Add1 Coordinate Band Scan")
    print("=========================================================")
    print(f"high_bridge_threshold={HIGH_BRIDGE_THRESHOLD:.1f}")
    print(f"baseline_add1_rows={len(rows)}")
    print(f"peer_motif_rows={sum(1 for row in rows if getattr(row, 'subtype') == 'peer_motif')}")
    print()
    print(render_rules("Best peer-motif coordinate-band rules", peer_rules))
    print()
    print(render_rules("Best non-peer coordinate-band rules", non_peer_rules))
    print()
    print("Rows")
    print("----")
    for row in rows:
        print(
            f"{getattr(row, 'source_name')} subtype={getattr(row, 'subtype')} "
            f"left_low={float(getattr(row, 'high_bridge_left_low_count')):.1f} "
            f"left_center={float(getattr(row, 'high_bridge_left_center_count')):.1f} "
            f"right_center={float(getattr(row, 'high_bridge_right_center_count')):.1f} "
            f"mid_low={float(getattr(row, 'high_bridge_mid_low_count')):.1f} "
            f"cells={float(getattr(row, 'high_bridge_cell_count')):.1f}"
        )
    print()
    print(
        "baseline add1 coordinate band scan completed "
        + datetime.now().isoformat(timespec="seconds")
        + f" total_elapsed={time.time() - total_start:.1f}s",
        flush=True,
    )


if __name__ == "__main__":
    main()
