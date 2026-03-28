#!/usr/bin/env python3
"""Probe candidate-anchored bridge-closure contrasts inside shared bucket `rc0|ml0|c2`."""

from __future__ import annotations

import argparse
from collections import defaultdict
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

from pocket_wrap_suppressor_low_overlap_boundary_axes import reconstruct_low_overlap_rows  # noqa: E402
from pocket_wrap_suppressor_low_overlap_center_spine_bucket00_support_topology import (  # noqa: E402
    evaluate_rules,
    render_rules,
)
from pocket_wrap_suppressor_low_overlap_support_family_transfer_common import (  # noqa: E402
    build_rows,
    is_rc0_ml0_c2_core_like,
    RC0_ML0_C2_BUCKET,
    support_edges,
)
from pocket_wrap_suppressor_low_overlap_center_spine_bucket00_support_edge_identity_add1_selector import (  # noqa: E402
    support_roles,
)
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


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--frontier-log",
        default="/Users/jonreilly/Projects/Physics/logs/2026-03-26-pocket-wrap-suppressor-nonpocket-subtype-rules-5504-max5600.txt",
    )
    parser.add_argument("--predicate-limit", type=int, default=22)
    parser.add_argument("--max-terms", type=int, default=3)
    parser.add_argument("--row-limit", type=int, default=8)
    return parser


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


def build_bucket_rows(frontier_log: Path) -> list[object]:
    coarse_rows = build_rows(frontier_log)
    allowed = {
        row.source_name
        for row in coarse_rows
        if is_rc0_ml0_c2_core_like(row)
    }
    frontier_rows = {
        row.source_name: row
        for row in reconstruct_low_overlap_rows(frontier_log)
        if row.source_name in allowed
    }

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

    by_source = {row.source_name: row for row in coarse_rows}
    out = []
    for source_name in sorted(allowed):
        coarse = by_source[source_name]
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


def main() -> None:
    args = build_parser().parse_args()
    started = datetime.now().isoformat(timespec="seconds")
    print(f"support family transfer rc0|ml0|c2 candidate-anchor contrast started {started}", flush=True)
    total_start = time.time()

    frontier_log = Path(args.frontier_log).resolve()
    rows = build_bucket_rows(frontier_log)

    print()
    print("Support Family Transfer rc0|ml0|c2 Candidate-Anchor Contrast")
    print("============================================================")
    print(f"frontier_log={frontier_log}")
    print(f"bucket={RC0_ML0_C2_BUCKET}")
    print(f"bucket_rows={len(rows)}")
    print()
    for subtype in sorted({row.subtype for row in rows}):
        rules = evaluate_rules(
            rows,
            target_subtype=subtype,
            feature_names=FEATURE_NAMES,
            predicate_limit=args.predicate_limit,
            max_terms=args.max_terms,
            row_limit=args.row_limit,
        )
        print(render_rules(f"Best rules for {TARGET_BUCKET} -> {subtype}", rules))
        print()
    print(
        "support family transfer rc0|ml0|c2 candidate-anchor contrast completed "
        + datetime.now().isoformat(timespec="seconds")
        + f" total_elapsed={time.time() - total_start:.1f}s",
        flush=True,
    )


if __name__ == "__main__":
    main()
