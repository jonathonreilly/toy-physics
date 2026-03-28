#!/usr/bin/env python3
"""Decompose baseline-covered add1 rows using support totals plus branch-cell motifs."""

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
from pocket_wrap_suppressor_low_overlap_support_family_transfer_common import (  # noqa: E402
    support_edge_identity_own_metrics,
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
from toy_event_physics import pocket_candidate_cells  # noqa: E402


MOTIF_CELLS = [
    (1, -2),
    (2, 1),
    (4, 2),
    (5, 0),
]
PEER_MOTIF_CELL = MOTIF_CELLS[0]
BASELINE_ADD1_RESCUE_EDGE_DENSITY = 0.018
BASELINE_ADD1_RESCUE_POCKET_TOTAL = -14.5


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
    parser.add_argument("--max-terms", type=int, default=2)
    parser.add_argument("--row-limit", type=int, default=8)
    return parser


def has_candidate_motif_like(nodes: set[tuple[int, int]], cell: tuple[int, int]) -> bool:
    pocket_cells, deep_cells = pocket_candidate_cells(nodes, wrap_y=False)
    return cell in pocket_cells or cell in deep_cells


def is_peer_motif_like(nodes: set[tuple[int, int]]) -> bool:
    return has_candidate_motif_like(nodes, PEER_MOTIF_CELL)


def split_baseline_add1_pocket_rows(
    pocket_rows: list[object],
    *,
    left_subtype: str,
) -> tuple[list[object], list[str]]:
    rescued_names = [
        getattr(row, "source_name")
        for row in pocket_rows
        if getattr(row, "subtype") == left_subtype
        and float(getattr(row, "delta_edge_identity_support_edge_density"))
        > BASELINE_ADD1_RESCUE_EDGE_DENSITY
        and float(getattr(row, "delta_count_pocket_total"))
        <= BASELINE_ADD1_RESCUE_POCKET_TOTAL
    ]
    baseline_rows = [
        row
        for row in pocket_rows
        if getattr(row, "subtype") == left_subtype
        and float(getattr(row, "delta_edge_identity_support_edge_density"))
        <= BASELINE_ADD1_RESCUE_EDGE_DENSITY
    ]
    return baseline_rows, rescued_names


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
        "BaselineAdd1BranchRow",
        [
            ("source_name", str),
            ("subtype", str),
            ("edge_identity_closed_pair_count", float),
            ("support_role_bridge_count", float),
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
        metrics = support_edge_identity_own_metrics(nodes)
        motif_hits = [float(has_candidate_motif_like(nodes, cell)) for cell in MOTIF_CELLS]
        peer_motif = is_peer_motif_like(nodes)
        out_rows.append(
            row_cls(
                source_name=source_name,
                subtype="peer_motif" if peer_motif else "non_peer",
                edge_identity_closed_pair_count=metrics["edge_identity_closed_pair_count"],
                support_role_bridge_count=metrics["support_role_bridge_count"],
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
    shown = [
        "source_name",
        "subtype",
        "edge_identity_closed_pair_count",
        "support_role_bridge_count",
        "motif_1_m2",
        "motif_2_1",
        "motif_4_2",
        "motif_5_0",
        "motif_count",
    ]
    lines = [
        "Baseline-covered add1 branch rows",
        "=================================",
        " | ".join(shown),
        " | ".join("-" * len(name) for name in shown),
    ]
    for row in rows:
        values = []
        for name in shown:
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
    print(f"baseline add1 branch decomposition started {started}", flush=True)
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
    print("Center-Spine Bucket 00 Baseline Add1 Branch Decomposition")
    print("=========================================================")
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
    print(render_rules("Best peer-motif branch rules", branch_rules))
    print()
    print(render_rules("Best non-peer rules", core_rules))
    print()
    print(
        "baseline add1 branch decomposition completed "
        + datetime.now().isoformat(timespec="seconds")
        + f" total_elapsed={time.time() - total_start:.1f}s",
        flush=True,
    )


if __name__ == "__main__":
    main()
