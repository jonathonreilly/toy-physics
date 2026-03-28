#!/usr/bin/env python3
"""Shared support-family transfer helpers for frozen low-overlap suppressor rows."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import sys

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
    edge_identity_signature,
    support_roles,
)
from toy_event_physics import graph_neighbors, pocket_candidate_cells  # noqa: E402


PRIMARY_SUPPORT_FAMILY_BUCKETS = ("rc0|ml0|c2", "rc0|ml1|c3")
RC0_ML0_C2_BUCKET = "rc0|ml0|c2"
RC0_ML0_C2_MAX_LEFT_LOW = 0.5
SUPPORT_ROLE_BRIDGE_HIGH_THRESHOLD = 19.0
EDGE_IDENTITY_CLOSED_PAIR_HIGH_THRESHOLD = 71.0
HIGH_SUPPORT_ML0_MIN_CELL_COUNT = 3.0
HIGH_SUPPORT_ML0_C4P_SPLIT_THRESHOLD = 3.5
HIGH_BRIDGE_THRESHOLD = 7.0


@dataclass(frozen=True)
class SupportFamilyTransferRow:
    source_name: str
    subtype: str
    edge_identity_closed_pair_count: float
    support_role_bridge_count: float
    high_bridge_cell_count: float
    high_bridge_left_count: float
    high_bridge_right_count: float
    high_bridge_mid_count: float
    high_bridge_low_count: float
    high_bridge_center_count: float
    high_bridge_high_count: float
    high_bridge_left_low_count: float
    high_bridge_left_center_count: float
    high_bridge_right_low_count: float
    high_bridge_right_center_count: float
    high_bridge_mid_low_count: float
    high_bridge_mid_center_count: float
    high_bridge_mid_high_count: float
    family_bucket_key: str
    residual_bucket_key: str


def _mid_low_bin(value: float) -> str:
    if value <= 0.5:
        return "ml0"
    if value <= 1.5:
        return "ml1"
    return "ml2p"


def _cell_bin(value: float) -> str:
    if value <= 2.5:
        return "c2"
    if value <= 3.5:
        return "c3"
    return "c4p"


def _bucket_metric(row: object, name: str) -> float:
    return float(getattr(row, name))


def support_edges(
    support_nodes: set[tuple[int, int]],
) -> set[tuple[tuple[int, int], tuple[int, int]]]:
    edges: set[tuple[tuple[int, int], tuple[int, int]]] = set()
    for left in sorted(support_nodes):
        for right in graph_neighbors(left, support_nodes, wrap_y=False):
            if right not in support_nodes or right <= left:
                continue
            edges.add((left, right))
    return edges


def support_edge_identity_own_metrics(nodes: set[tuple[int, int]]) -> dict[str, float]:
    pocket_cells, deep_cells = pocket_candidate_cells(nodes, wrap_y=False)
    roles = support_roles(nodes, pocket_cells, deep_cells)
    support_nodes = set(roles)
    support_edge_set = support_edges(support_nodes)
    _events, numeric = edge_identity_signature(nodes)

    metrics: dict[str, float] = {
        "pocket_candidate_count": float(len(pocket_cells)),
        "deep_candidate_count": float(len(deep_cells)),
        "candidate_count": float(len(pocket_cells | deep_cells)),
        "support_node_count": float(len(support_nodes)),
        "support_edge_count": float(len(support_edge_set)),
        "support_role_bridge_count": float(sum(1 for role in roles.values() if role == "bridge")),
        "support_role_pocket_only_count": float(sum(1 for role in roles.values() if role == "pocket_only")),
        "support_role_deep_only_count": float(sum(1 for role in roles.values() if role == "deep_only")),
        "edge_identity_event_count": numeric["edge_identity_event_count"],
        "edge_identity_closed_pair_count": numeric["edge_identity_closed_pair_count"],
        "edge_identity_open_pair_count": numeric["edge_identity_open_pair_count"],
        "edge_identity_candidate_closed_fraction": numeric["edge_identity_candidate_closed_fraction"],
        "edge_identity_candidate_open_fraction": numeric["edge_identity_candidate_open_fraction"],
        "edge_identity_closed_pair_ratio": numeric["edge_identity_closed_pair_ratio"],
        "edge_identity_closed_span_mean": numeric["edge_identity_closed_span_mean"],
        "edge_identity_support_edge_density": numeric["edge_identity_support_edge_density"],
    }

    role_edge_counts: dict[str, float] = {}
    for left, right in support_edge_set:
        key = "__".join(sorted((roles[left], roles[right])))
        role_edge_counts[key] = role_edge_counts.get(key, 0.0) + 1.0
    for key, value in role_edge_counts.items():
        metrics[f"support_edge_role_{key}_count"] = value
    return metrics


def high_bridge_cells(nodes: set[tuple[int, int]]) -> list[tuple[int, int]]:
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


def high_bridge_band_metrics(cells: list[tuple[int, int]]) -> dict[str, float]:
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


def family_bucket_key(row: SupportFamilyTransferRow) -> str:
    return "|".join(
        [
            f"rc{int(row.high_bridge_right_center_count >= 0.5)}",
            _mid_low_bin(row.high_bridge_mid_low_count),
            _cell_bin(row.high_bridge_cell_count),
        ]
    )


def residual_bucket_key(row: SupportFamilyTransferRow) -> str:
    return "|".join(
        [
            f"rc{int(row.high_bridge_right_center_count >= 0.5)}",
            f"sbh{int(row.support_role_bridge_count >= SUPPORT_ROLE_BRIDGE_HIGH_THRESHOLD)}",
            f"cp_hi{int(row.edge_identity_closed_pair_count >= EDGE_IDENTITY_CLOSED_PAIR_HIGH_THRESHOLD)}",
            _mid_low_bin(row.high_bridge_mid_low_count),
            _cell_bin(row.high_bridge_cell_count),
        ]
    )


def family_bucket_key_like(row: object) -> str:
    return "|".join(
        [
            f"rc{int(_bucket_metric(row, 'high_bridge_right_center_count') >= 0.5)}",
            _mid_low_bin(_bucket_metric(row, "high_bridge_mid_low_count")),
            _cell_bin(_bucket_metric(row, "high_bridge_cell_count")),
        ]
    )


def residual_bucket_key_like(row: object) -> str:
    return "|".join(
        [
            f"rc{int(_bucket_metric(row, 'high_bridge_right_center_count') >= 0.5)}",
            f"sbh{int(_bucket_metric(row, 'support_role_bridge_count') >= SUPPORT_ROLE_BRIDGE_HIGH_THRESHOLD)}",
            f"cp_hi{int(_bucket_metric(row, 'edge_identity_closed_pair_count') >= EDGE_IDENTITY_CLOSED_PAIR_HIGH_THRESHOLD)}",
            _mid_low_bin(_bucket_metric(row, "high_bridge_mid_low_count")),
            _cell_bin(_bucket_metric(row, "high_bridge_cell_count")),
        ]
    )


def is_rc0_ml0_c2_core_like(row: object) -> bool:
    return (
        getattr(row, "family_bucket_key") == RC0_ML0_C2_BUCKET
        and float(getattr(row, "high_bridge_left_low_count")) < RC0_ML0_C2_MAX_LEFT_LOW
    )


def is_peer_band_like(row: object) -> bool:
    return float(getattr(row, "high_bridge_left_low_count")) >= RC0_ML0_C2_MAX_LEFT_LOW


def build_rows(frontier_log: Path) -> list[SupportFamilyTransferRow]:
    rows = reconstruct_low_overlap_rows(frontier_log)
    out: list[SupportFamilyTransferRow] = []
    for row in rows:
        nodes = set(row.nodes)
        core_metrics = support_edge_identity_own_metrics(nodes)
        band_metrics = high_bridge_band_metrics(high_bridge_cells(nodes))
        out_row = SupportFamilyTransferRow(
            source_name=row.source_name,
            subtype=row.subtype,
            edge_identity_closed_pair_count=core_metrics["edge_identity_closed_pair_count"],
            support_role_bridge_count=core_metrics["support_role_bridge_count"],
            high_bridge_cell_count=band_metrics["high_bridge_cell_count"],
            high_bridge_left_count=band_metrics["high_bridge_left_count"],
            high_bridge_right_count=band_metrics["high_bridge_right_count"],
            high_bridge_mid_count=band_metrics["high_bridge_mid_count"],
            high_bridge_low_count=band_metrics["high_bridge_low_count"],
            high_bridge_center_count=band_metrics["high_bridge_center_count"],
            high_bridge_high_count=band_metrics["high_bridge_high_count"],
            high_bridge_left_low_count=band_metrics["high_bridge_left_low_count"],
            high_bridge_left_center_count=band_metrics["high_bridge_left_center_count"],
            high_bridge_right_low_count=band_metrics["high_bridge_right_low_count"],
            high_bridge_right_center_count=band_metrics["high_bridge_right_center_count"],
            high_bridge_mid_low_count=band_metrics["high_bridge_mid_low_count"],
            high_bridge_mid_center_count=band_metrics["high_bridge_mid_center_count"],
            high_bridge_mid_high_count=band_metrics["high_bridge_mid_high_count"],
            family_bucket_key="",
            residual_bucket_key="",
        )
        out.append(
            SupportFamilyTransferRow(
                **{
                    **out_row.__dict__,
                    "family_bucket_key": family_bucket_key(out_row),
                    "residual_bucket_key": residual_bucket_key(out_row),
                }
            )
        )
    out.sort(key=lambda item: item.source_name)
    return out


def build_rc0_ml0_c2_core_inputs(
    frontier_log: Path,
) -> tuple[dict[str, SupportFamilyTransferRow], dict[str, object]]:
    coarse_rows = build_rows(frontier_log)
    allowed = {
        row.source_name
        for row in coarse_rows
        if is_rc0_ml0_c2_core_like(row)
    }
    coarse_by_source = {
        row.source_name: row
        for row in coarse_rows
        if row.source_name in allowed
    }
    frontier_rows = {
        row.source_name: row
        for row in reconstruct_low_overlap_rows(frontier_log)
        if row.source_name in allowed
    }
    return coarse_by_source, frontier_rows
