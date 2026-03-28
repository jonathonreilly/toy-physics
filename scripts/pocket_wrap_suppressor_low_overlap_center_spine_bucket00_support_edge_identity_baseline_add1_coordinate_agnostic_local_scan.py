#!/usr/bin/env python3
"""Test whether the baseline add1 peer branch closes under coordinate-agnostic candidate-local bridge features."""

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

from pocket_wrap_suppressor_low_overlap_center_spine_bucket00_support_edge_identity_baseline_add1_branch_decomposition import (  # noqa: E402
    MOTIF_CELLS,
    is_peer_motif_like,
    load_bucket_frontier_inputs,
    split_baseline_add1_pocket_rows,
)
from pocket_wrap_suppressor_low_overlap_center_spine_bucket00_support_edge_identity_pocket_subfamily_decomposition import (  # noqa: E402
    build_rows as build_pocket_rows,
)
from pocket_wrap_suppressor_low_overlap_center_spine_bucket00_support_topology import (  # noqa: E402
    evaluate_rules,
    render_rules,
)
from pocket_wrap_suppressor_low_overlap_support_family_transfer_common import (  # noqa: E402
    support_edge_identity_own_metrics,
    support_edges,
)
from pocket_wrap_suppressor_low_overlap_center_spine_bucket00_support_edge_identity_add1_selector import (  # noqa: E402
    support_roles,
)
from toy_event_physics import graph_neighbors, pocket_candidate_cells  # noqa: E402


SHOW_COLUMNS = [
    "source_name",
    "subtype",
    "edge_identity_closed_pair_count",
    "support_role_bridge_count",
    "max_candidate_adj_bridge_count",
    "max_candidate_adj_support_count",
    "max_candidate_adj_support_edge_count",
    "max_candidate_ring_candidate_count",
    "max_candidate_ring_bridge_touch_count",
    "count_candidate_adj_bridge_ge4",
    "count_candidate_adj_bridge_ge6",
    "top_cell_x",
    "top_cell_y",
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
    parser.add_argument("--predicate-limit", type=int, default=24)
    parser.add_argument("--max-terms", type=int, default=3)
    parser.add_argument("--row-limit", type=int, default=10)
    return parser


def _candidate_local_metrics(nodes: set[tuple[int, int]]) -> tuple[dict[str, float], tuple[int, int]]:
    pocket_cells, deep_cells = pocket_candidate_cells(nodes, wrap_y=False)
    candidate_cells = pocket_cells | deep_cells
    roles = support_roles(nodes, pocket_cells, deep_cells)
    support_nodes = set(roles)
    support_edge_set = support_edges(support_nodes)

    candidate_to_supports: dict[tuple[int, int], set[tuple[int, int]]] = {}
    for support in support_nodes:
        adjacent = set(graph_neighbors(support, support_nodes | candidate_cells, wrap_y=False))
        attached = adjacent & candidate_cells
        for cell in attached:
            candidate_to_supports.setdefault(cell, set()).add(support)

    support_edge_set = {tuple(sorted((left, right))) for left, right in support_edge_set}

    per_cell: list[dict[str, float | tuple[int, int]]] = []
    for cell in sorted(candidate_cells):
        attached = candidate_to_supports.get(cell, set())
        bridge_count = float(sum(1 for node in attached if roles.get(node) == "bridge"))
        attached_edge_count = 0.0
        for left, right in support_edge_set:
            if left in attached and right in attached:
                attached_edge_count += 1.0

        x, y = cell
        ring = {
            (x - 1, y),
            (x + 1, y),
            (x, y - 1),
            (x, y + 1),
        }
        ring_candidate_count = float(sum(1 for other in ring if other in candidate_cells and other != cell))
        ring_bridge_touch_count = 0.0
        for other in ring:
            supports = candidate_to_supports.get(other, set())
            if any(roles.get(node) == "bridge" for node in supports):
                ring_bridge_touch_count += 1.0

        per_cell.append(
            {
                "cell": cell,
                "adj_bridge_count": bridge_count,
                "adj_support_count": float(len(attached)),
                "adj_support_edge_count": attached_edge_count,
                "ring_candidate_count": ring_candidate_count,
                "ring_bridge_touch_count": ring_bridge_touch_count,
            }
        )

    if not per_cell:
        return (
            {
                "max_candidate_adj_bridge_count": 0.0,
                "max_candidate_adj_support_count": 0.0,
                "max_candidate_adj_support_edge_count": 0.0,
                "max_candidate_ring_candidate_count": 0.0,
                "max_candidate_ring_bridge_touch_count": 0.0,
                "count_candidate_adj_bridge_ge4": 0.0,
                "count_candidate_adj_bridge_ge6": 0.0,
                "count_candidate_adj_support_edge_ge8": 0.0,
                "top_cell_x": 0.0,
                "top_cell_y": 0.0,
                "top_cell_is_motif": 0.0,
            },
            (0, 0),
        )

    top = max(
        per_cell,
        key=lambda item: (
            float(item["adj_bridge_count"]),
            float(item["adj_support_edge_count"]),
            -float(item["ring_candidate_count"]),
            -float(item["ring_bridge_touch_count"]),
            tuple(item["cell"]),
        ),
    )
    top_cell = tuple(top["cell"])  # type: ignore[arg-type]
    metrics = {
        "max_candidate_adj_bridge_count": float(top["adj_bridge_count"]),
        "max_candidate_adj_support_count": float(top["adj_support_count"]),
        "max_candidate_adj_support_edge_count": float(top["adj_support_edge_count"]),
        "max_candidate_ring_candidate_count": float(top["ring_candidate_count"]),
        "max_candidate_ring_bridge_touch_count": float(top["ring_bridge_touch_count"]),
        "count_candidate_adj_bridge_ge4": float(
            sum(1 for item in per_cell if float(item["adj_bridge_count"]) >= 4.0)
        ),
        "count_candidate_adj_bridge_ge6": float(
            sum(1 for item in per_cell if float(item["adj_bridge_count"]) >= 6.0)
        ),
        "count_candidate_adj_support_edge_ge8": float(
            sum(1 for item in per_cell if float(item["adj_support_edge_count"]) >= 8.0)
        ),
        "top_cell_x": float(top_cell[0]),
        "top_cell_y": float(top_cell[1]),
        "top_cell_is_motif": float(top_cell in MOTIF_CELLS),
    }
    return metrics, top_cell


def build_rows(
    frontier_rows: dict[str, object],
    bucket_rows: list[object],
    *,
    left_subtype: str,
    right_subtype: str,
) -> tuple[list[object], list[str]]:
    pocket_rows = build_pocket_rows(
        frontier_rows,
        bucket_rows,
        left_subtype=left_subtype,
        right_subtype=right_subtype,
    )
    baseline_rows, rescued_names = split_baseline_add1_pocket_rows(
        pocket_rows,
        left_subtype=left_subtype,
    )

    row_cls = make_dataclass(
        "BaselineAdd1CoordinateAgnosticLocalRow",
        [
            ("source_name", str),
            ("subtype", str),
            ("edge_identity_closed_pair_count", float),
            ("support_role_bridge_count", float),
            ("max_candidate_adj_bridge_count", float),
            ("max_candidate_adj_support_count", float),
            ("max_candidate_adj_support_edge_count", float),
            ("max_candidate_ring_candidate_count", float),
            ("max_candidate_ring_bridge_touch_count", float),
            ("count_candidate_adj_bridge_ge4", float),
            ("count_candidate_adj_bridge_ge6", float),
            ("count_candidate_adj_support_edge_ge8", float),
            ("top_cell_x", float),
            ("top_cell_y", float),
            ("top_cell_is_motif", float),
        ],
        frozen=True,
    )

    rows: list[object] = []
    for row in baseline_rows:
        source_name = getattr(row, "source_name")
        nodes = set(frontier_rows[source_name].nodes)
        core_metrics = support_edge_identity_own_metrics(nodes)
        local_metrics, _top = _candidate_local_metrics(nodes)
        peer_motif = is_peer_motif_like(nodes)
        rows.append(
            row_cls(
                source_name=source_name,
                subtype="peer_motif" if peer_motif else "non_peer",
                edge_identity_closed_pair_count=core_metrics["edge_identity_closed_pair_count"],
                support_role_bridge_count=core_metrics["support_role_bridge_count"],
                **local_metrics,
            )
        )
    rows.sort(key=lambda item: getattr(item, "source_name"))
    return rows, rescued_names


def render_rows(rows: list[object]) -> str:
    lines = [
        "Baseline-covered add1 coordinate-agnostic local rows",
        "=====================================================",
        " | ".join(SHOW_COLUMNS),
        " | ".join("-" * len(name) for name in SHOW_COLUMNS),
    ]
    for row in rows:
        values = []
        for name in SHOW_COLUMNS:
            value = getattr(row, name)
            if isinstance(value, float):
                values.append(f"{value:.3f}")
            else:
                values.append(str(value))
        lines.append(" | ".join(values))
    return "\n".join(lines)


def main() -> None:
    args = build_parser().parse_args()
    started = datetime.now().isoformat(timespec="seconds")
    print(f"baseline add1 coordinate-agnostic local scan started {started}", flush=True)
    total_start = time.time()

    frontier_log = Path(args.frontier_log).resolve()
    bucket_log = Path(args.bucket_log).resolve()
    bucket_rows, frontier_rows = load_bucket_frontier_inputs(
        frontier_log,
        bucket_log,
        bucket_key=args.bucket_key,
    )
    rows, rescued_names = build_rows(
        frontier_rows,
        bucket_rows,
        left_subtype=args.left_subtype,
        right_subtype=args.right_subtype,
    )
    feature_names = [
        "edge_identity_closed_pair_count",
        "support_role_bridge_count",
        "max_candidate_adj_bridge_count",
        "max_candidate_adj_support_count",
        "max_candidate_adj_support_edge_count",
        "max_candidate_ring_candidate_count",
        "max_candidate_ring_bridge_touch_count",
        "count_candidate_adj_bridge_ge4",
        "count_candidate_adj_bridge_ge6",
        "count_candidate_adj_support_edge_ge8",
        "top_cell_is_motif",
    ]
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
    peer_count = sum(1 for row in rows if getattr(row, "subtype") == "peer_motif")
    non_peer_count = sum(1 for row in rows if getattr(row, "subtype") == "non_peer")

    print()
    print("Center-Spine Bucket 00 Baseline Add1 Coordinate-Agnostic Local Scan")
    print("===================================================================")
    print(f"frontier_log={frontier_log}")
    print(f"bucket_log={bucket_log}")
    print(f"bucket_key={args.bucket_key}")
    print(f"rescued_sources={', '.join(sorted(rescued_names))}")
    print(f"baseline_add1_rows={len(rows)}")
    print(f"peer_motif_rows={peer_count}")
    print(f"non_peer_rows={non_peer_count}")
    print()
    print(render_rows(rows))
    print()
    print(render_rules("Best peer-motif coordinate-agnostic local rules", peer_rules))
    print()
    print(render_rules("Best non-peer coordinate-agnostic local rules", non_peer_rules))
    print()
    print(
        "baseline add1 coordinate-agnostic local scan completed "
        + datetime.now().isoformat(timespec="seconds")
        + f" total_elapsed={time.time() - total_start:.1f}s",
        flush=True,
    )


if __name__ == "__main__":
    main()
