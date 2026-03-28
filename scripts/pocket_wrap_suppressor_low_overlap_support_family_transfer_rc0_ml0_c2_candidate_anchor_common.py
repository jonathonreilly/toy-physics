#!/usr/bin/env python3
"""Shared candidate-anchor helpers for the frozen `rc0|ml0|c2` transfer scans."""

from __future__ import annotations

from collections import defaultdict
from dataclasses import make_dataclass
from pathlib import Path
import sys

SCRIPTS_DIR = Path(__file__).resolve().parent
PROJECT_DIR = SCRIPTS_DIR.parent
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))
if str(PROJECT_DIR) not in sys.path:
    sys.path.insert(0, str(PROJECT_DIR))

from pocket_wrap_suppressor_low_overlap_support_family_transfer_common import (  # noqa: E402
    build_rc0_ml0_c2_core_inputs,
)
from pocket_wrap_suppressor_low_overlap_center_spine_bucket00_support_edge_identity_add1_selector import (  # noqa: E402
    support_roles,
)
from pocket_wrap_suppressor_low_overlap_support_family_transfer_common import support_edges  # noqa: E402
from toy_event_physics import graph_neighbors, pocket_candidate_cells  # noqa: E402

FEATURE_NAMES = [
    "edge_identity_closed_pair_count",
    "support_role_bridge_count",
    "high_bridge_left_count",
    "high_bridge_mid_count",
    "left_candidate_count",
    "mid_candidate_count",
    "left_candidate_bridge_max",
    "mid_candidate_bridge_max",
    "left_candidate_closed_pair_max",
    "mid_candidate_closed_pair_max",
    "left_candidate_bridge_bridge_closed_pair_max",
    "mid_candidate_bridge_bridge_closed_pair_max",
    "left_candidate_closed_ratio_max",
    "mid_candidate_closed_ratio_max",
    "left_candidate_pocket_count",
    "mid_candidate_pocket_count",
    "left_candidate_deep_count",
    "mid_candidate_deep_count",
    "left_candidate_dense_count",
    "mid_candidate_dense_count",
    "delta_mid_left_bridge_max",
    "delta_mid_left_closed_pair_max",
    "delta_mid_left_bridge_bridge_closed_pair_max",
    "delta_mid_left_dense_count",
]


def _ratio(numerator: float, denominator: float) -> float:
    return numerator / denominator if denominator else 0.0


def _candidate_band(cell: tuple[int, int]) -> str:
    x, _y = cell
    if x <= 1:
        return "left"
    if x >= 5:
        return "right"
    return "mid"


def _band_defaults() -> dict[str, float]:
    return {
        "candidate_count": 0.0,
        "pocket_count": 0.0,
        "deep_count": 0.0,
        "bridge_max": 0.0,
        "closed_pair_max": 0.0,
        "bridge_bridge_closed_pair_max": 0.0,
        "closed_ratio_max": 0.0,
        "dense_count": 0.0,
    }


def candidate_anchor_metrics(nodes: set[tuple[int, int]]) -> dict[str, float]:
    pocket_cells, deep_cells = pocket_candidate_cells(nodes, wrap_y=False)
    candidate_cells = pocket_cells | deep_cells
    roles = support_roles(nodes, pocket_cells, deep_cells)
    support_nodes = set(roles)
    support_edge_set = support_edges(support_nodes)

    band_metrics: dict[str, dict[str, float]] = defaultdict(_band_defaults)
    for candidate in sorted(candidate_cells):
        band = _candidate_band(candidate)
        band_metrics[band]["candidate_count"] += 1.0
        if candidate in pocket_cells:
            band_metrics[band]["pocket_count"] += 1.0
        if candidate in deep_cells:
            band_metrics[band]["deep_count"] += 1.0

        attached = [
            support
            for support in graph_neighbors(candidate, support_nodes, wrap_y=False)
            if support in roles
        ]
        bridge_neighbors = [support for support in attached if roles.get(support) == "bridge"]
        bridge_count = float(len(bridge_neighbors))
        band_metrics[band]["bridge_max"] = max(band_metrics[band]["bridge_max"], bridge_count)

        closed_pairs = 0.0
        bridge_bridge_closed_pairs = 0.0
        total_pairs = 0.0
        for idx, left in enumerate(attached):
            for right in attached[idx + 1 :]:
                total_pairs += 1.0
                edge = (left, right) if left < right else (right, left)
                if edge not in support_edge_set:
                    continue
                closed_pairs += 1.0
                if roles.get(left) == "bridge" and roles.get(right) == "bridge":
                    bridge_bridge_closed_pairs += 1.0

        band_metrics[band]["closed_pair_max"] = max(
            band_metrics[band]["closed_pair_max"], closed_pairs
        )
        band_metrics[band]["bridge_bridge_closed_pair_max"] = max(
            band_metrics[band]["bridge_bridge_closed_pair_max"], bridge_bridge_closed_pairs
        )
        band_metrics[band]["closed_ratio_max"] = max(
            band_metrics[band]["closed_ratio_max"], _ratio(closed_pairs, total_pairs)
        )
        if bridge_count >= 3.0 and closed_pairs >= 2.0:
            band_metrics[band]["dense_count"] += 1.0

    out: dict[str, float] = {}
    for band in ("left", "mid"):
        metrics = band_metrics[band]
        out[f"{band}_candidate_count"] = metrics["candidate_count"]
        out[f"{band}_candidate_pocket_count"] = metrics["pocket_count"]
        out[f"{band}_candidate_deep_count"] = metrics["deep_count"]
        out[f"{band}_candidate_bridge_max"] = metrics["bridge_max"]
        out[f"{band}_candidate_closed_pair_max"] = metrics["closed_pair_max"]
        out[f"{band}_candidate_bridge_bridge_closed_pair_max"] = metrics[
            "bridge_bridge_closed_pair_max"
        ]
        out[f"{band}_candidate_closed_ratio_max"] = metrics["closed_ratio_max"]
        out[f"{band}_candidate_dense_count"] = metrics["dense_count"]

    out["delta_mid_left_bridge_max"] = (
        out["mid_candidate_bridge_max"] - out["left_candidate_bridge_max"]
    )
    out["delta_mid_left_closed_pair_max"] = (
        out["mid_candidate_closed_pair_max"] - out["left_candidate_closed_pair_max"]
    )
    out["delta_mid_left_bridge_bridge_closed_pair_max"] = (
        out["mid_candidate_bridge_bridge_closed_pair_max"]
        - out["left_candidate_bridge_bridge_closed_pair_max"]
    )
    out["delta_mid_left_dense_count"] = (
        out["mid_candidate_dense_count"] - out["left_candidate_dense_count"]
    )
    return out


def build_candidate_anchor_rows(frontier_log: Path) -> list[object]:
    coarse_by_source, frontier_rows = build_rc0_ml0_c2_core_inputs(frontier_log)

    row_cls = make_dataclass(
        "TransferAnchorContrastRow",
        [
            ("source_name", str),
            ("subtype", str),
            ("edge_identity_closed_pair_count", float),
            ("support_role_bridge_count", float),
            ("high_bridge_left_count", float),
            ("high_bridge_mid_count", float),
        ]
        + [(name, float) for name in FEATURE_NAMES[4:]],
        frozen=True,
    )

    out = []
    for source_name in sorted(coarse_by_source):
        coarse = coarse_by_source[source_name]
        anchor_metrics = candidate_anchor_metrics(set(frontier_rows[source_name].nodes))
        out.append(
            row_cls(
                source_name=source_name,
                subtype=coarse.subtype,
                edge_identity_closed_pair_count=coarse.edge_identity_closed_pair_count,
                support_role_bridge_count=coarse.support_role_bridge_count,
                high_bridge_left_count=coarse.high_bridge_left_count,
                high_bridge_mid_count=coarse.high_bridge_mid_count,
                **anchor_metrics,
            )
        )
    return out
