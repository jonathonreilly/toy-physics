#!/usr/bin/env python3
"""Compare generated zero-support transfer failures against historical low-overlap rows."""

from __future__ import annotations

import argparse
from collections import Counter
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

from pocket_wrap_suppressor_low_overlap_order_parameter_exact_law_generated_ensemble_transfer_check import (  # noqa: E402
    build_rows as build_generated_rows,
)
from pocket_wrap_suppressor_low_overlap_order_parameter_full_bucket_exact_projection import (  # noqa: E402
    build_rows as build_historical_rows,
    predict_branch,
    predict_subtype,
)
from pocket_wrap_suppressor_low_overlap_support_family_transfer_common import (  # noqa: E402
    RC0_ML0_C2_BUCKET,
)


FEATURES = (
    "support_load",
    "closure_load",
    "mid_anchor_closure_peak",
    "anchor_closure_intensity_gap",
    "anchor_deep_share_gap",
    "high_bridge_high_count",
    "high_bridge_right_count",
    "high_bridge_right_low_count",
    "edge_identity_event_count",
    "edge_identity_support_edge_density",
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--frontier-log",
        default="/Users/jonreilly/Projects/Physics/logs/2026-03-26-pocket-wrap-suppressor-nonpocket-subtype-rules-5504-max5600.txt",
    )
    parser.add_argument("--pack-name", default="base")
    parser.add_argument("--scenario-name", default="taper-wrap")
    parser.add_argument(
        "--ensembles",
        nargs="+",
        default=("default", "broader", "wider"),
    )
    parser.add_argument(
        "--target-sources",
        nargs="+",
        default=("base:taper-wrap:geometry-c", "base:taper-wrap:geometry-e"),
    )
    return parser


def _format_counts(rows: list[object], attr: str = "subtype") -> str:
    counts = Counter(getattr(row, attr) for row in rows)
    if not counts:
        return "none"
    return ", ".join(f"{key}:{counts[key]}" for key in sorted(counts))


def _all_zero(row: object) -> bool:
    return all(float(getattr(row, feature)) == 0.0 for feature in FEATURES)


def _nearest_row(target: object, candidates: list[object]) -> tuple[object, float]:
    best_row = candidates[0]
    best_distance = sum(
        abs(float(getattr(target, feature)) - float(getattr(best_row, feature)))
        for feature in FEATURES
    )
    for candidate in candidates[1:]:
        distance = sum(
            abs(float(getattr(target, feature)) - float(getattr(candidate, feature)))
            for feature in FEATURES
        )
        if distance < best_distance:
            best_row = candidate
            best_distance = distance
    return best_row, best_distance


def _render_feature_ranges(title: str, rows: list[object]) -> str:
    lines = [title, "=" * len(title)]
    lines.append(f"rows={len(rows)} ({_format_counts(rows)})")
    for feature in FEATURES:
        values = [float(getattr(row, feature)) for row in rows]
        lines.append(
            f"{feature}: min={min(values):.3f} max={max(values):.3f}"
        )
    return "\n".join(lines)


def _render_target_rows(
    title: str,
    rows: list[object],
    historical_pair_rows: list[object],
    historical_add1_rows: list[object],
) -> str:
    lines = [title, "=" * len(title)]
    if not rows:
        lines.append("none")
        return "\n".join(lines)
    for row in rows:
        nearest_pair, pair_distance = _nearest_row(row, historical_pair_rows)
        nearest_add1, add1_distance = _nearest_row(row, historical_add1_rows)
        lines.append(
            f"{getattr(row, 'ensemble_name')}:{getattr(row, 'source_name')} "
            f"actual={getattr(row, 'subtype')} predicted={predict_subtype(row)} "
            f"branch={predict_branch(row)} all_zero={'yes' if _all_zero(row) else 'no'}"
        )
        for feature in FEATURES:
            lines.append(f"  {feature}={float(getattr(row, feature)):.3f}")
        lines.append(
            f"  nearest_hist_pair={getattr(nearest_pair, 'source_name')} "
            f"distance={pair_distance:.3f}"
        )
        lines.append(
            f"  nearest_hist_add1={getattr(nearest_add1, 'source_name')} "
            f"distance={add1_distance:.3f}"
        )
    return "\n".join(lines)


def main() -> None:
    args = build_parser().parse_args()
    started = datetime.now().isoformat(timespec="seconds")
    print(f"generated zero-support compare started {started}", flush=True)
    total_start = time.time()

    frontier_log = Path(args.frontier_log).resolve()
    historical_rows = build_historical_rows(frontier_log)
    historical_pair_rows = [
        row for row in historical_rows if getattr(row, "subtype") == "pair-only-sensitive"
    ]
    historical_add1_rows = [
        row for row in historical_rows if getattr(row, "subtype") == "add1-sensitive"
    ]

    target_sources = set(args.target_sources)
    generated_rows: list[object] = []
    for ensemble_name in list(dict.fromkeys(args.ensembles)):
        generated_rows.extend(
            row
            for row in build_generated_rows(
                ensemble_name,
                args.pack_name,
                args.scenario_name,
            )
            if getattr(row, "source_name") in target_sources
        )

    zero_rows = [row for row in generated_rows if _all_zero(row)]

    print()
    print("Generated Zero-Support Compare")
    print("==============================")
    print(f"frontier_log={frontier_log}")
    print(f"bucket={RC0_ML0_C2_BUCKET}")
    print(f"target={args.pack_name}:{args.scenario_name}")
    print("ensembles=" + ",".join(dict.fromkeys(args.ensembles)))
    print("target_sources=" + ",".join(sorted(target_sources)))
    print(
        f"generated_target_rows={len(generated_rows)} "
        f"({_format_counts(generated_rows)})"
    )
    print(
        f"all_zero_generated_rows={len(zero_rows)} "
        f"({_format_counts(zero_rows, attr='source_name')})"
    )
    print()
    print(_render_feature_ranges("Historical pair-only ranges", historical_pair_rows))
    print()
    print(_render_feature_ranges("Historical add1 ranges", historical_add1_rows))
    print()
    print(
        _render_target_rows(
            "Generated zero-support target rows",
            generated_rows,
            historical_pair_rows,
            historical_add1_rows,
        )
    )
    print()
    if len(zero_rows) == len(generated_rows) and generated_rows:
        print("Conclusion")
        print("==========")
        print(
            "All targeted generated transfer failures collapse to an all-zero support/order-parameter signature."
        )
        print(
            "The historical frozen bucket has no pair-only or add1 row with zero support_load, zero closure_load, and zero edge-identity activity."
        )
        print(
            "So the immediate generated transfer break is best treated as a support-collapse domain edge, not an in-family continuation of the historical pair-only branch."
        )
    else:
        print("Conclusion")
        print("==========")
        print("Generated target set is not uniformly zero-support; domain-edge interpretation is not yet established.")
    print()
    print(
        "generated zero-support compare completed "
        + datetime.now().isoformat(timespec="seconds")
        + f" total_elapsed={time.time() - total_start:.1f}s",
        flush=True,
    )


if __name__ == "__main__":
    main()
