#!/usr/bin/env python3
"""Shared row builders for frozen-5504 baseline add1 follow-on scans."""

from __future__ import annotations

from dataclasses import make_dataclass
from pathlib import Path
import sys

SCRIPTS_DIR = Path(__file__).resolve().parent
PROJECT_DIR = SCRIPTS_DIR.parent
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))
if str(PROJECT_DIR) not in sys.path:
    sys.path.insert(0, str(PROJECT_DIR))

from pocket_wrap_suppressor_low_overlap_center_spine_bucket00_support_edge_identity_baseline_add1_branch_decomposition import (  # noqa: E402
    MOTIF_CELLS,
    is_peer_motif_like,
    split_baseline_add1_pocket_rows,
)
from pocket_wrap_suppressor_low_overlap_center_spine_bucket00_support_edge_identity_pocket_subfamily_decomposition import (  # noqa: E402
    build_rows as build_pocket_rows,
)
from pocket_wrap_suppressor_low_overlap_support_family_transfer_common import (  # noqa: E402
    high_bridge_band_metrics,
    high_bridge_cells,
    support_edge_identity_own_metrics,
    support_edges,
)
from pocket_wrap_suppressor_low_overlap_center_spine_bucket00_support_edge_identity_add1_selector import (  # noqa: E402
    support_roles,
)
from toy_event_physics import graph_neighbors, pocket_candidate_cells  # noqa: E402


def candidate_local_metrics(nodes: set[tuple[int, int]]) -> tuple[dict[str, float], tuple[int, int]]:
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


def build_coordinate_agnostic_rows(
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
        local_metrics, _top = candidate_local_metrics(nodes)
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


def build_coordinate_band_rows(
    frontier_rows: dict[str, object],
    bucket_rows: list[object],
    *,
    left_subtype: str,
    right_subtype: str,
) -> list[object]:
    pocket_rows = build_pocket_rows(
        frontier_rows,
        bucket_rows,
        left_subtype=left_subtype,
        right_subtype=right_subtype,
    )
    baseline_rows, _rescued_names = split_baseline_add1_pocket_rows(
        pocket_rows,
        left_subtype=left_subtype,
    )

    row_cls = make_dataclass(
        "BaselineAdd1CoordinateBandRow",
        [("source_name", str), ("subtype", str)] + [
            ("edge_identity_closed_pair_count", float),
            ("support_role_bridge_count", float),
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
        nodes = set(frontier_rows[source_name].nodes)
        cells = high_bridge_cells(nodes)
        core_metrics = support_edge_identity_own_metrics(nodes)
        rows.append(
            row_cls(
                source_name=source_name,
                subtype="peer_motif" if is_peer_motif_like(nodes) else "non_peer",
                edge_identity_closed_pair_count=core_metrics["edge_identity_closed_pair_count"],
                support_role_bridge_count=core_metrics["support_role_bridge_count"],
                **high_bridge_band_metrics(cells),
            )
        )
    rows.sort(key=lambda item: getattr(item, "source_name"))
    return rows
