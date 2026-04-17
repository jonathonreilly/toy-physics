#!/usr/bin/env python3
"""Augment the low-overlap order-parameter map with support-layout asymmetry features."""

from __future__ import annotations

import argparse
from dataclasses import make_dataclass
from datetime import datetime
from pathlib import Path
import statistics
import sys
import time

SCRIPTS_DIR = Path(__file__).resolve().parent
PROJECT_DIR = SCRIPTS_DIR.parent
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))
if str(PROJECT_DIR) not in sys.path:
    sys.path.insert(0, str(PROJECT_DIR))

from pocket_wrap_suppressor_low_overlap_center_spine_bucket00_support_topology import (  # noqa: E402
    evaluate_rules,
    render_rules,
)
from pocket_wrap_suppressor_low_overlap_support_family_transfer_common import (  # noqa: E402
    RC0_ML0_C2_BUCKET,
)
from pocket_wrap_suppressor_low_overlap_support_family_transfer_rc0_ml0_c2_candidate_anchor_common import (  # noqa: E402
    build_candidate_anchor_rows,
)


def _ratio(numerator: float, denominator: float) -> float:
    return numerator / denominator if denominator else 0.0


FEATURE_NAMES = [
    "support_load",
    "closure_load",
    "left_mid_support_bias",
    "anchor_bridge_gap",
    "anchor_closure_gap",
    "anchor_density_gap",
    "mid_anchor_closure_peak",
    "left_anchor_density",
    "mid_anchor_density",
    "anchor_count_gap",
    "anchor_count_total",
    "anchor_pocket_share_gap",
    "anchor_deep_share_gap",
    "anchor_dense_share_gap",
    "anchor_closure_intensity_gap",
]


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--frontier-log",
        default="/Users/jonreilly/Projects/Physics/logs/2026-03-26-pocket-wrap-suppressor-nonpocket-subtype-rules-5504-max5600.txt",
    )
    parser.add_argument("--predicate-limit", type=int, default=22)
    parser.add_argument("--max-terms", type=int, default=3)
    parser.add_argument("--row-limit", type=int, default=6)
    return parser


def build_rows(frontier_log: Path) -> list[object]:
    source_rows = build_candidate_anchor_rows(frontier_log)
    row_cls = make_dataclass(
        "LowOverlapOrderParameterAsymmetryRow",
        [
            ("source_name", str),
            ("subtype", str),
            ("support_load", float),
            ("closure_load", float),
            ("left_mid_support_bias", float),
            ("anchor_bridge_gap", float),
            ("anchor_closure_gap", float),
            ("anchor_density_gap", float),
            ("mid_anchor_closure_peak", float),
            ("left_anchor_density", float),
            ("mid_anchor_density", float),
            ("anchor_count_gap", float),
            ("anchor_count_total", float),
            ("anchor_pocket_share_gap", float),
            ("anchor_deep_share_gap", float),
            ("anchor_dense_share_gap", float),
            ("anchor_closure_intensity_gap", float),
        ],
        frozen=True,
    )

    rows = []
    for row in source_rows:
        left_count = float(getattr(row, "left_candidate_count"))
        mid_count = float(getattr(row, "mid_candidate_count"))
        left_pocket_count = float(getattr(row, "left_candidate_pocket_count"))
        mid_pocket_count = float(getattr(row, "mid_candidate_pocket_count"))
        left_deep_count = float(getattr(row, "left_candidate_deep_count"))
        mid_deep_count = float(getattr(row, "mid_candidate_deep_count"))
        left_dense_count = float(getattr(row, "left_candidate_dense_count"))
        mid_dense_count = float(getattr(row, "mid_candidate_dense_count"))
        left_closure_peak = float(getattr(row, "left_candidate_bridge_bridge_closed_pair_max"))
        mid_closure_peak = float(getattr(row, "mid_candidate_bridge_bridge_closed_pair_max"))

        rows.append(
            row_cls(
                source_name=getattr(row, "source_name"),
                subtype=getattr(row, "subtype"),
                support_load=float(getattr(row, "support_role_bridge_count")),
                closure_load=float(getattr(row, "edge_identity_closed_pair_count")),
                left_mid_support_bias=float(getattr(row, "high_bridge_left_count"))
                - float(getattr(row, "high_bridge_mid_count")),
                anchor_bridge_gap=float(getattr(row, "delta_mid_left_bridge_max")),
                anchor_closure_gap=float(getattr(row, "delta_mid_left_bridge_bridge_closed_pair_max")),
                anchor_density_gap=float(getattr(row, "delta_mid_left_dense_count")),
                mid_anchor_closure_peak=float(getattr(row, "mid_candidate_bridge_bridge_closed_pair_max")),
                left_anchor_density=float(getattr(row, "left_candidate_dense_count")),
                mid_anchor_density=float(getattr(row, "mid_candidate_dense_count")),
                anchor_count_gap=mid_count - left_count,
                anchor_count_total=left_count + mid_count,
                anchor_pocket_share_gap=_ratio(mid_pocket_count, mid_count)
                - _ratio(left_pocket_count, left_count),
                anchor_deep_share_gap=_ratio(mid_deep_count, mid_count)
                - _ratio(left_deep_count, left_count),
                anchor_dense_share_gap=_ratio(mid_dense_count, mid_count)
                - _ratio(left_dense_count, left_count),
                anchor_closure_intensity_gap=_ratio(mid_closure_peak, mid_count)
                - _ratio(left_closure_peak, left_count),
            )
        )
    return rows


def render_profiles(rows: list[object]) -> str:
    lines = [
        "Subtype Order-Parameter Profiles (With Asymmetry)",
        "=================================================",
    ]
    for subtype in sorted({getattr(row, "subtype") for row in rows}):
        subtype_rows = [row for row in rows if getattr(row, "subtype") == subtype]
        lines.append(subtype)
        lines.append("-" * len(subtype))
        for feature in FEATURE_NAMES:
            values = [float(getattr(row, feature)) for row in subtype_rows]
            lines.append(
                f"{feature}: mean={statistics.mean(values):.3f} "
                f"median={statistics.median(values):.3f} "
                f"min/max={min(values):.3f}/{max(values):.3f}"
            )
        lines.append("")
    return "\n".join(lines).rstrip()


def main() -> None:
    args = build_parser().parse_args()
    started = datetime.now().isoformat(timespec="seconds")
    print(f"low-overlap order-parameter asymmetry map started {started}", flush=True)
    total_start = time.time()

    frontier_log = Path(args.frontier_log).resolve()
    rows = build_rows(frontier_log)

    print()
    print("Low-Overlap Order-Parameter Asymmetry Map")
    print("=========================================")
    print(f"frontier_log={frontier_log}")
    print(f"bucket={RC0_ML0_C2_BUCKET}")
    print(f"rows={len(rows)}")
    print()
    print(render_profiles(rows))
    print()
    for subtype in sorted({getattr(row, "subtype") for row in rows}):
        rules = evaluate_rules(
            rows,
            target_subtype=subtype,
            feature_names=FEATURE_NAMES,
            predicate_limit=args.predicate_limit,
            max_terms=args.max_terms,
            row_limit=args.row_limit,
        )
        print(render_rules(f"Candidate asymmetry-augmented rules for {subtype}", rules))
        print()
    print(
        "low-overlap order-parameter asymmetry map completed "
        + datetime.now().isoformat(timespec="seconds")
        + f" total_elapsed={time.time() - total_start:.1f}s",
        flush=True,
    )


if __name__ == "__main__":
    main()
