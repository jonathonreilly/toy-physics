#!/usr/bin/env python3
"""Probe richer support-edge layout summaries inside the shared `rc0|ml0|c2` bucket."""

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

from pocket_wrap_suppressor_low_overlap_center_spine_bucket00_support_edge_identity_add1_selector import (  # noqa: E402
    edge_identity_signature,
)
from pocket_wrap_suppressor_low_overlap_center_spine_bucket00_support_topology import (  # noqa: E402
    evaluate_rules,
    render_rules,
)
from pocket_wrap_suppressor_low_overlap_support_family_transfer_common import (  # noqa: E402
    build_rc0_ml0_c2_core_inputs,
    RC0_ML0_C2_BUCKET,
)

FEATURE_NAMES = [
    "edge_identity_closed_pair_count",
    "support_role_bridge_count",
    "high_bridge_left_count",
    "high_bridge_mid_count",
    "high_bridge_low_count",
    "high_bridge_right_count",
    "edge_identity_open_pair_count",
    "edge_identity_candidate_closed_fraction",
    "edge_identity_candidate_open_fraction",
    "edge_identity_closed_pair_ratio",
    "edge_identity_closed_span_mean",
    "edge_identity_support_edge_density",
]


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--frontier-log",
        default="/Users/jonreilly/Projects/Physics/logs/2026-03-26-pocket-wrap-suppressor-nonpocket-subtype-rules-5504-max5600.txt",
    )
    parser.add_argument("--predicate-limit", type=int, default=18)
    parser.add_argument("--max-terms", type=int, default=3)
    parser.add_argument("--row-limit", type=int, default=6)
    return parser


def build_bucket_rows(frontier_log: Path) -> list[object]:
    coarse_by_source, frontier_rows = build_rc0_ml0_c2_core_inputs(frontier_log)

    row_cls = make_dataclass(
        "TransferTopologyRow",
        [
            ("source_name", str),
            ("subtype", str),
            ("edge_identity_closed_pair_count", float),
            ("support_role_bridge_count", float),
            ("high_bridge_left_count", float),
            ("high_bridge_mid_count", float),
            ("high_bridge_low_count", float),
            ("high_bridge_right_count", float),
            ("edge_identity_open_pair_count", float),
            ("edge_identity_candidate_closed_fraction", float),
            ("edge_identity_candidate_open_fraction", float),
            ("edge_identity_closed_pair_ratio", float),
            ("edge_identity_closed_span_mean", float),
            ("edge_identity_support_edge_density", float),
        ],
        frozen=True,
    )

    out = []
    for source_name in sorted(coarse_by_source):
        coarse = coarse_by_source[source_name]
        _events, numeric = edge_identity_signature(set(frontier_rows[source_name].nodes))
        out.append(
            row_cls(
                source_name=source_name,
                subtype=coarse.subtype,
                edge_identity_closed_pair_count=coarse.edge_identity_closed_pair_count,
                support_role_bridge_count=coarse.support_role_bridge_count,
                high_bridge_left_count=coarse.high_bridge_left_count,
                high_bridge_mid_count=coarse.high_bridge_mid_count,
                high_bridge_low_count=coarse.high_bridge_low_count,
                high_bridge_right_count=coarse.high_bridge_right_count,
                edge_identity_open_pair_count=numeric["edge_identity_open_pair_count"],
                edge_identity_candidate_closed_fraction=numeric["edge_identity_candidate_closed_fraction"],
                edge_identity_candidate_open_fraction=numeric["edge_identity_candidate_open_fraction"],
                edge_identity_closed_pair_ratio=numeric["edge_identity_closed_pair_ratio"],
                edge_identity_closed_span_mean=numeric["edge_identity_closed_span_mean"],
                edge_identity_support_edge_density=numeric["edge_identity_support_edge_density"],
            )
        )
    return out


def main() -> None:
    args = build_parser().parse_args()
    started = datetime.now().isoformat(timespec="seconds")
    print(f"support family transfer rc0|ml0|c2 topology scan started {started}", flush=True)
    total_start = time.time()

    frontier_log = Path(args.frontier_log).resolve()
    rows = build_bucket_rows(frontier_log)

    print()
    print("Support Family Transfer rc0|ml0|c2 Topology Scan")
    print("===============================================")
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
        print(render_rules(f"Candidate rules for {RC0_ML0_C2_BUCKET} -> {subtype}", rules))
        print()
    print(
        "support family transfer rc0|ml0|c2 topology scan completed "
        + datetime.now().isoformat(timespec="seconds")
        + f" total_elapsed={time.time() - total_start:.1f}s",
        flush=True,
    )


if __name__ == "__main__":
    main()
