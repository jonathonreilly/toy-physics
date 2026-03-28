#!/usr/bin/env python3
"""Probe candidate-anchored local topology residuals for baseline-covered add1 peer closure."""

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
from pocket_wrap_suppressor_low_overlap_center_spine_bucket00_support_edge_identity_baseline_add1_branch_decomposition import (  # noqa: E402
    MOTIF_CELLS,
    has_candidate_motif_like,
    is_peer_motif_like,
    split_baseline_add1_pocket_rows,
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
from pocket_wrap_suppressor_low_overlap_support_family_transfer_common import (  # noqa: E402
    support_edge_identity_own_metrics,
    support_edges,
)
from pocket_wrap_suppressor_low_overlap_center_spine_bucket00_support_edge_identity_add1_selector import (  # noqa: E402
    support_roles,
)
from toy_event_physics import graph_neighbors, pocket_candidate_cells  # noqa: E402


ANCHOR_CELL = (1, -2)
RING_CELLS = ((0, -2), (2, -2), (1, -1), (1, -3))
SHOW_COLUMNS = [
    "source_name",
    "subtype",
    "edge_identity_closed_pair_count",
    "support_role_bridge_count",
    "anchor_is_candidate",
    "anchor_adj_bridge_count",
    "anchor_adj_support_count",
    "anchor_adj_support_edge_count",
    "anchor_ring_candidate_count",
    "anchor_ring_bridge_touch_count",
    "anchor_ring_support_degree_mean",
    "motif_1_m2",
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


def _anchor_local_metrics(nodes: set[tuple[int, int]]) -> dict[str, float]:
    pocket_cells, deep_cells = pocket_candidate_cells(nodes, wrap_y=False)
    candidate_cells = pocket_cells | deep_cells
    roles = support_roles(nodes, pocket_cells, deep_cells)
    support_nodes = set(roles)
    support_edge_set = support_edges(support_nodes)

    candidate_to_supports: dict[tuple[int, int], set[tuple[int, int]]] = {}
    support_to_candidates: dict[tuple[int, int], set[tuple[int, int]]] = {node: set() for node in support_nodes}
    for support in support_nodes:
        adjacent = set(graph_neighbors(support, support_nodes | candidate_cells, wrap_y=False))
        attached_candidates = adjacent & candidate_cells
        support_to_candidates[support] = attached_candidates
        for cell in attached_candidates:
            candidate_to_supports.setdefault(cell, set()).add(support)

    anchor_supports = candidate_to_supports.get(ANCHOR_CELL, set())
    anchor_adj_support_edge_count = 0.0
    for left, right in support_edge_set:
        if left in anchor_supports and right in anchor_supports:
            anchor_adj_support_edge_count += 1.0

    ring_candidate_count = 0.0
    ring_bridge_touch_count = 0.0
    ring_support_degree_total = 0.0
    ring_support_degree_count = 0.0
    ring_support_edge_count = 0.0

    ring_support_union: set[tuple[int, int]] = set()
    for cell in RING_CELLS:
        supports = candidate_to_supports.get(cell, set())
        if cell in candidate_cells:
            ring_candidate_count += 1.0
        if any(roles.get(s) == "bridge" for s in supports):
            ring_bridge_touch_count += 1.0
        ring_support_degree_total += float(len(supports))
        ring_support_degree_count += 1.0
        ring_support_union |= supports

    for left, right in support_edge_set:
        if left in ring_support_union and right in ring_support_union:
            ring_support_edge_count += 1.0

    anchor_adj_bridge_count = float(sum(1 for support in anchor_supports if roles.get(support) == "bridge"))
    anchor_adj_pocket_only_count = float(
        sum(1 for support in anchor_supports if roles.get(support) == "pocket_only")
    )
    anchor_adj_deep_only_count = float(sum(1 for support in anchor_supports if roles.get(support) == "deep_only"))

    return {
        "anchor_is_candidate": float(ANCHOR_CELL in candidate_cells),
        "anchor_adj_support_count": float(len(anchor_supports)),
        "anchor_adj_bridge_count": anchor_adj_bridge_count,
        "anchor_adj_pocket_only_count": anchor_adj_pocket_only_count,
        "anchor_adj_deep_only_count": anchor_adj_deep_only_count,
        "anchor_adj_support_edge_count": anchor_adj_support_edge_count,
        "anchor_ring_candidate_count": ring_candidate_count,
        "anchor_ring_bridge_touch_count": ring_bridge_touch_count,
        "anchor_ring_support_degree_mean": (
            ring_support_degree_total / ring_support_degree_count if ring_support_degree_count else 0.0
        ),
        "anchor_ring_support_edge_count": ring_support_edge_count,
    }


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
        "BaselineAdd1CandidateAnchorResidualRow",
        [
            ("source_name", str),
            ("subtype", str),
            ("edge_identity_closed_pair_count", float),
            ("support_role_bridge_count", float),
            ("support_edge_role_bridge__bridge_count", float),
            ("anchor_is_candidate", float),
            ("anchor_adj_support_count", float),
            ("anchor_adj_bridge_count", float),
            ("anchor_adj_pocket_only_count", float),
            ("anchor_adj_deep_only_count", float),
            ("anchor_adj_support_edge_count", float),
            ("anchor_ring_candidate_count", float),
            ("anchor_ring_bridge_touch_count", float),
            ("anchor_ring_support_degree_mean", float),
            ("anchor_ring_support_edge_count", float),
            ("motif_1_m2", float),
            ("motif_2_1", float),
            ("motif_4_2", float),
            ("motif_5_0", float),
            ("motif_count", float),
            ("motif_other_count", float),
        ],
        frozen=True,
    )

    out_rows: list[object] = []
    for row in baseline_rows:
        source_name = getattr(row, "source_name")
        nodes = set(frontier_rows[source_name].nodes)
        core_metrics = support_edge_identity_own_metrics(nodes)
        anchor_metrics = _anchor_local_metrics(nodes)
        motif_hits = [float(has_candidate_motif_like(nodes, cell)) for cell in MOTIF_CELLS]
        peer_motif = is_peer_motif_like(nodes)

        out_rows.append(
            row_cls(
                source_name=source_name,
                subtype="peer_motif" if peer_motif else "non_peer",
                edge_identity_closed_pair_count=core_metrics["edge_identity_closed_pair_count"],
                support_role_bridge_count=core_metrics["support_role_bridge_count"],
                support_edge_role_bridge__bridge_count=core_metrics.get(
                    "support_edge_role_bridge__bridge_count", 0.0
                ),
                anchor_is_candidate=anchor_metrics["anchor_is_candidate"],
                anchor_adj_support_count=anchor_metrics["anchor_adj_support_count"],
                anchor_adj_bridge_count=anchor_metrics["anchor_adj_bridge_count"],
                anchor_adj_pocket_only_count=anchor_metrics["anchor_adj_pocket_only_count"],
                anchor_adj_deep_only_count=anchor_metrics["anchor_adj_deep_only_count"],
                anchor_adj_support_edge_count=anchor_metrics["anchor_adj_support_edge_count"],
                anchor_ring_candidate_count=anchor_metrics["anchor_ring_candidate_count"],
                anchor_ring_bridge_touch_count=anchor_metrics["anchor_ring_bridge_touch_count"],
                anchor_ring_support_degree_mean=anchor_metrics["anchor_ring_support_degree_mean"],
                anchor_ring_support_edge_count=anchor_metrics["anchor_ring_support_edge_count"],
                motif_1_m2=motif_hits[0],
                motif_2_1=motif_hits[1],
                motif_4_2=motif_hits[2],
                motif_5_0=motif_hits[3],
                motif_count=float(sum(motif_hits)),
                motif_other_count=float(sum(motif_hits[1:])),
            )
        )

    out_rows.sort(key=lambda item: getattr(item, "source_name"))
    return out_rows, rescued_names


def render_rows(rows: list[object]) -> str:
    lines = [
        "Baseline-covered add1 candidate-anchor residual rows",
        "===================================================",
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
    print(f"baseline add1 candidate-anchor residual scan started {started}", flush=True)
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
    rows, rescued_names = build_rows(
        frontier_rows,
        bucket_rows,
        left_subtype=args.left_subtype,
        right_subtype=args.right_subtype,
    )

    feature_names = [
        "edge_identity_closed_pair_count",
        "support_role_bridge_count",
        "support_edge_role_bridge__bridge_count",
        "anchor_adj_support_count",
        "anchor_adj_bridge_count",
        "anchor_adj_pocket_only_count",
        "anchor_adj_deep_only_count",
        "anchor_adj_support_edge_count",
        "anchor_ring_candidate_count",
        "anchor_ring_bridge_touch_count",
        "anchor_ring_support_degree_mean",
        "anchor_ring_support_edge_count",
        "motif_2_1",
        "motif_4_2",
        "motif_5_0",
        "motif_other_count",
        "motif_count",
    ]

    branch_rules = evaluate_rules(
        rows,
        target_subtype="peer_motif",
        feature_names=feature_names,
        predicate_limit=args.predicate_limit,
        max_terms=args.max_terms,
        row_limit=args.row_limit,
    )
    core_rules = evaluate_rules(
        rows,
        target_subtype="non_peer",
        feature_names=feature_names,
        predicate_limit=args.predicate_limit,
        max_terms=args.max_terms,
        row_limit=args.row_limit,
    )

    branch_count = sum(1 for row in rows if getattr(row, "subtype") == "peer_motif")
    core_count = sum(1 for row in rows if getattr(row, "subtype") == "non_peer")

    print()
    print("Center-Spine Bucket 00 Baseline Add1 Candidate-Anchor Residual Scan")
    print("===================================================================")
    print(f"frontier_log={frontier_log}")
    print(f"bucket_log={bucket_log}")
    print(f"bucket_key={args.bucket_key}")
    print(f"rescued_sources={', '.join(sorted(rescued_names))}")
    print(f"baseline_add1_rows={len(rows)}")
    print(f"peer_motif_rows={branch_count}")
    print(f"non_peer_rows={core_count}")
    print()
    print(render_rows(rows))
    print()
    print(render_rules("Best peer-motif candidate-anchor residual rules", branch_rules))
    print()
    print(render_rules("Best non-peer candidate-anchor residual rules", core_rules))
    print()
    print(
        "baseline add1 candidate-anchor residual scan completed "
        + datetime.now().isoformat(timespec="seconds")
        + f" total_elapsed={time.time() - total_start:.1f}s",
        flush=True,
    )


if __name__ == "__main__":
    main()
