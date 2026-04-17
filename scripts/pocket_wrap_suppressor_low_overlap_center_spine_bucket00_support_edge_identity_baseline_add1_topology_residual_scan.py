#!/usr/bin/env python3
"""Probe richer support-layout topology for baseline-covered add1 peer-branch closure."""

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
    has_candidate_motif_like,
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
from toy_event_physics import pocket_candidate_cells  # noqa: E402


SHOW_COLUMNS = [
    "source_name",
    "subtype",
    "edge_identity_closed_pair_count",
    "support_role_bridge_count",
    "support_bridge_deg1_count",
    "support_bridge_deg3_plus_count",
    "support_edge_span_ge4_count",
    "support_edge_orientation_diag_count",
    "support_edge_orientation_skew_count",
    "bridge_bridge_span_ge4_count",
    "bridge_bridge_orientation_diag_count",
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


def _role_pair(a: str, b: str) -> str:
    return "__".join(sorted((a, b)))


def _orientation_bin(dx: int, dy: int) -> str:
    adx = abs(dx)
    ady = abs(dy)
    if adx == 0 or ady == 0:
        return "axis"
    if adx == ady:
        return "diag"
    return "skew"


def _span_bin(span: int) -> str:
    if span <= 1:
        return "span1"
    if span == 2:
        return "span2"
    if span == 3:
        return "span3"
    return "span_ge4"


def _layout_metrics(nodes: set[tuple[int, int]]) -> dict[str, float]:
    pocket_cells, deep_cells = pocket_candidate_cells(nodes, wrap_y=False)
    roles = support_roles(nodes, pocket_cells, deep_cells)
    support_nodes = set(roles)
    support_edge_set = support_edges(support_nodes)

    metrics: dict[str, float] = {
        "support_bridge_deg0_count": 0.0,
        "support_bridge_deg1_count": 0.0,
        "support_bridge_deg2_count": 0.0,
        "support_bridge_deg3_plus_count": 0.0,
        "support_edge_span1_count": 0.0,
        "support_edge_span2_count": 0.0,
        "support_edge_span3_count": 0.0,
        "support_edge_span_ge4_count": 0.0,
        "support_edge_orientation_axis_count": 0.0,
        "support_edge_orientation_diag_count": 0.0,
        "support_edge_orientation_skew_count": 0.0,
        "bridge_bridge_span1_count": 0.0,
        "bridge_bridge_span2_count": 0.0,
        "bridge_bridge_span3_count": 0.0,
        "bridge_bridge_span_ge4_count": 0.0,
        "bridge_bridge_orientation_axis_count": 0.0,
        "bridge_bridge_orientation_diag_count": 0.0,
        "bridge_bridge_orientation_skew_count": 0.0,
    }

    support_degree = {node: 0 for node in support_nodes}
    for left, right in support_edge_set:
        support_degree[left] += 1
        support_degree[right] += 1

    for node, role in roles.items():
        if role != "bridge":
            continue
        deg = support_degree[node]
        if deg <= 0:
            metrics["support_bridge_deg0_count"] += 1.0
        elif deg == 1:
            metrics["support_bridge_deg1_count"] += 1.0
        elif deg == 2:
            metrics["support_bridge_deg2_count"] += 1.0
        else:
            metrics["support_bridge_deg3_plus_count"] += 1.0

    for left, right in support_edge_set:
        dx = right[0] - left[0]
        dy = right[1] - left[1]
        span = abs(dx) + abs(dy)
        span_key = _span_bin(span)
        orient_key = _orientation_bin(dx, dy)
        metrics[f"support_edge_{span_key}_count"] += 1.0
        metrics[f"support_edge_orientation_{orient_key}_count"] += 1.0

        if _role_pair(roles[left], roles[right]) == "bridge__bridge":
            metrics[f"bridge_bridge_{span_key}_count"] += 1.0
            metrics[f"bridge_bridge_orientation_{orient_key}_count"] += 1.0

    return metrics


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
        "BaselineAdd1TopologyResidualRow",
        [
            ("source_name", str),
            ("subtype", str),
            ("edge_identity_closed_pair_count", float),
            ("support_role_bridge_count", float),
            ("support_edge_role_bridge__bridge_count", float),
            ("support_bridge_deg0_count", float),
            ("support_bridge_deg1_count", float),
            ("support_bridge_deg2_count", float),
            ("support_bridge_deg3_plus_count", float),
            ("support_edge_span1_count", float),
            ("support_edge_span2_count", float),
            ("support_edge_span3_count", float),
            ("support_edge_span_ge4_count", float),
            ("support_edge_orientation_axis_count", float),
            ("support_edge_orientation_diag_count", float),
            ("support_edge_orientation_skew_count", float),
            ("bridge_bridge_span1_count", float),
            ("bridge_bridge_span2_count", float),
            ("bridge_bridge_span3_count", float),
            ("bridge_bridge_span_ge4_count", float),
            ("bridge_bridge_orientation_axis_count", float),
            ("bridge_bridge_orientation_diag_count", float),
            ("bridge_bridge_orientation_skew_count", float),
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
        layout_metrics = _layout_metrics(nodes)
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
                support_bridge_deg0_count=layout_metrics["support_bridge_deg0_count"],
                support_bridge_deg1_count=layout_metrics["support_bridge_deg1_count"],
                support_bridge_deg2_count=layout_metrics["support_bridge_deg2_count"],
                support_bridge_deg3_plus_count=layout_metrics["support_bridge_deg3_plus_count"],
                support_edge_span1_count=layout_metrics["support_edge_span1_count"],
                support_edge_span2_count=layout_metrics["support_edge_span2_count"],
                support_edge_span3_count=layout_metrics["support_edge_span3_count"],
                support_edge_span_ge4_count=layout_metrics["support_edge_span_ge4_count"],
                support_edge_orientation_axis_count=layout_metrics[
                    "support_edge_orientation_axis_count"
                ],
                support_edge_orientation_diag_count=layout_metrics[
                    "support_edge_orientation_diag_count"
                ],
                support_edge_orientation_skew_count=layout_metrics[
                    "support_edge_orientation_skew_count"
                ],
                bridge_bridge_span1_count=layout_metrics["bridge_bridge_span1_count"],
                bridge_bridge_span2_count=layout_metrics["bridge_bridge_span2_count"],
                bridge_bridge_span3_count=layout_metrics["bridge_bridge_span3_count"],
                bridge_bridge_span_ge4_count=layout_metrics["bridge_bridge_span_ge4_count"],
                bridge_bridge_orientation_axis_count=layout_metrics[
                    "bridge_bridge_orientation_axis_count"
                ],
                bridge_bridge_orientation_diag_count=layout_metrics[
                    "bridge_bridge_orientation_diag_count"
                ],
                bridge_bridge_orientation_skew_count=layout_metrics[
                    "bridge_bridge_orientation_skew_count"
                ],
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
        "Baseline-covered add1 topology residual rows",
        "===========================================",
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
    print(f"baseline add1 topology residual scan started {started}", flush=True)
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
        "support_edge_role_bridge__bridge_count",
        "support_bridge_deg1_count",
        "support_bridge_deg2_count",
        "support_bridge_deg3_plus_count",
        "support_edge_span2_count",
        "support_edge_span3_count",
        "support_edge_span_ge4_count",
        "support_edge_orientation_diag_count",
        "support_edge_orientation_skew_count",
        "bridge_bridge_span2_count",
        "bridge_bridge_span3_count",
        "bridge_bridge_span_ge4_count",
        "bridge_bridge_orientation_diag_count",
        "bridge_bridge_orientation_skew_count",
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
    print("Center-Spine Bucket 00 Baseline Add1 Topology Residual Scan")
    print("===========================================================")
    print(f"frontier_log={frontier_log}")
    print(f"bucket_log={bucket_log}")
    print(f"bucket_key={args.bucket_key}")
    print(f"rescued_sources={', '.join(sorted(rescued_names))}")
    print(f"baseline_add1_rows={len(rows)}")
    print(f"peer_branch_rows={branch_count}")
    print(f"non_peer_core_rows={core_count}")
    print()
    print(render_rows(rows))
    print()
    print(render_rules("Candidate peer-branch topology residual rules", branch_rules))
    print()
    print(render_rules("Candidate non-peer-core topology residual rules", core_rules))
    print()
    print(
        "baseline add1 topology residual scan completed "
        + datetime.now().isoformat(timespec="seconds")
        + f" total_elapsed={time.time() - total_start:.1f}s",
        flush=True,
    )


if __name__ == "__main__":
    main()
