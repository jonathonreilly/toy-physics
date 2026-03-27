#!/usr/bin/env python3
"""Compare rescued low-tail rows to nearest non-rescued rows above pocket cutoffs."""

from __future__ import annotations

import argparse
from collections import defaultdict
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
from pocket_wrap_suppressor_low_overlap_center_spine_bucket00_support_edge_identity_add1_selector import (  # noqa: E402
    edge_identity_signature,
)
from pocket_wrap_suppressor_low_overlap_center_spine_bucket00_support_edge_identity_pocket_subfamily_decomposition import (  # noqa: E402
    _aggregate_pocket,
    build_rows,
)
from pocket_wrap_suppressor_low_overlap_center_spine_hardest_bucket_rules import (  # noqa: E402
    load_bucket_rows,
)


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
    parser.add_argument(
        "--target-features",
        nargs="+",
        default=[
            "delta_count_pocket_present0",
            "delta_count_pocket_present1",
            "delta_count_pocket_role_pocket_only__pocket_only",
        ],
    )
    parser.add_argument("--top-k", type=int, default=3)
    parser.add_argument("--example-limit", type=int, default=8)
    return parser


def _feature_value(row: object, name: str) -> float:
    return float(getattr(row, name))


def _distance_from_cutoffs(row: object, cutoffs: dict[str, float]) -> tuple[float, float]:
    surplus = 0.0
    l1 = 0.0
    for name, cutoff in cutoffs.items():
        value = _feature_value(row, name)
        delta = value - cutoff
        surplus += delta
        l1 += abs(delta)
    return surplus, l1


def _distance_to_reference(row: object, ref: object, features: list[str]) -> float:
    return sum(abs(_feature_value(row, name) - _feature_value(ref, name)) for name in features)


def _nonzero_items(counts: dict[str, float], prefix: str) -> list[tuple[str, float]]:
    return sorted(
        ((name, value) for name, value in counts.items() if name.startswith(prefix) and value != 0.0),
        key=lambda item: (-item[1], item[0]),
    )


def main() -> None:
    args = build_parser().parse_args()
    started = datetime.now().isoformat(timespec="seconds")
    print(f"center-spine bucket00 pocket-basis geometry diff started {started}", flush=True)
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

    rows = build_rows(
        frontier_rows,
        bucket_rows,
        left_subtype=args.left_subtype,
        right_subtype=args.right_subtype,
    )

    baseline_threshold = 0.018
    family_threshold = -14.5

    rescued_rows = [
        row
        for row in rows
        if getattr(row, "subtype") == args.left_subtype
        and _feature_value(row, "delta_edge_identity_support_edge_density") > baseline_threshold
        and _feature_value(row, "delta_count_pocket_total") <= family_threshold
    ]

    rescued_names = {getattr(row, "source_name") for row in rescued_rows}
    non_rescued_rows = [row for row in rows if getattr(row, "source_name") not in rescued_names]

    cutoffs: dict[str, float] = {}
    for feature in args.target_features:
        rescued_max = max(_feature_value(row, feature) for row in rescued_rows)
        next_above = min(
            (_feature_value(row, feature) for row in non_rescued_rows if _feature_value(row, feature) > rescued_max),
            default=rescued_max,
        )
        cutoffs[feature] = next_above

    candidate_rows = [
        row
        for row in non_rescued_rows
        if all(_feature_value(row, name) >= cutoffs[name] for name in args.target_features)
    ]

    rescued_center = defaultdict(float)
    for row in rescued_rows:
        for feature in args.target_features:
            rescued_center[feature] += _feature_value(row, feature)
    for feature in args.target_features:
        rescued_center[feature] /= max(len(rescued_rows), 1)

    candidates_ranked = sorted(
        candidate_rows,
        key=lambda row: (
            _distance_from_cutoffs(row, cutoffs),
            sum(abs(_feature_value(row, f) - rescued_center[f]) for f in args.target_features),
            getattr(row, "source_name"),
        ),
    )

    top_candidates = candidates_ranked[: args.top_k]

    pocket_counts: dict[str, dict[str, float]] = {}
    for source_name in rescued_names | {getattr(row, "source_name") for row in top_candidates}:
        nodes = set(frontier_rows[source_name].nodes)
        events, _numeric = edge_identity_signature(nodes)
        pocket_counts[source_name] = _aggregate_pocket(events)

    print()
    print("Center-Spine Bucket 00 Pocket-Basis Geometry Difference")
    print("======================================================")
    print(f"frontier_log={frontier_log}")
    print(f"bucket_log={bucket_log}")
    print(f"bucket_key={args.bucket_key}")
    print(f"rescued_sources={', '.join(sorted(rescued_names))}")
    print(f"target_features={', '.join(args.target_features)}")
    print()

    print("Low-tail cutoff anchors (next non-rescued values above rescued maxima):")
    for feature in args.target_features:
        print(f"  {feature}: {cutoffs[feature]:.3f}")
    print()

    print("Nearest non-rescued rows above all cutoffs:")
    for row in top_candidates:
        surplus, l1 = _distance_from_cutoffs(row, cutoffs)
        feature_text = ", ".join(f"{name}={_feature_value(row, name):.3f}" for name in args.target_features)
        print(
            "  "
            + f"{getattr(row, 'source_name')} subtype={getattr(row, 'subtype')} "
            + f"surplus={surplus:.3f} l1={l1:.3f} {feature_text}"
        )
    print()

    reference = top_candidates[0] if top_candidates else None
    if reference is None:
        print("No non-rescued row satisfied all cutoff constraints.")
    else:
        reference_name = getattr(reference, "source_name")
        print(f"Reference comparator row={reference_name}")
        print()
        for rescued in sorted(rescued_rows, key=lambda row: getattr(row, "source_name")):
            rescued_name = getattr(rescued, "source_name")
            print(f"Rescued row={rescued_name}")
            print(
                "  feature_deltas_to_reference="
                + ", ".join(
                    f"{name}:{_feature_value(reference, name) - _feature_value(rescued, name):+.3f}"
                    for name in args.target_features
                )
            )
            print(
                f"  l1_distance_on_targets={_distance_to_reference(reference, rescued, args.target_features):.3f}"
            )
            rescued_counts = pocket_counts[rescued_name]
            reference_counts = pocket_counts[reference_name]

            print("  own_pocket_role_counts_rescued(nonzero)")
            for name, value in _nonzero_items(rescued_counts, "count_pocket_role_"):
                print(f"    {name}={value:.0f}")
            print("  own_pocket_role_counts_reference(nonzero)")
            for name, value in _nonzero_items(reference_counts, "count_pocket_role_"):
                print(f"    {name}={value:.0f}")

            print("  own_pocket_joined_counts_rescued(nonzero)")
            for name, value in _nonzero_items(rescued_counts, "count_pocket_joined_"):
                print(f"    {name}={value:.0f}")
            print("  own_pocket_joined_counts_reference(nonzero)")
            for name, value in _nonzero_items(reference_counts, "count_pocket_joined_"):
                print(f"    {name}={value:.0f}")

            role_deltas = sorted(
                (
                    (name, reference_counts.get(name, 0.0) - rescued_counts.get(name, 0.0))
                    for name in set(rescued_counts) | set(reference_counts)
                    if name.startswith("count_pocket_role_")
                ),
                key=lambda item: (-item[1], item[0]),
            )
            joined_deltas = sorted(
                (
                    (name, reference_counts.get(name, 0.0) - rescued_counts.get(name, 0.0))
                    for name in set(rescued_counts) | set(reference_counts)
                    if name.startswith("count_pocket_joined_")
                ),
                key=lambda item: (-item[1], item[0]),
            )

            print("  concrete_own_count_edits_to_match_reference(role)")
            for name, value in role_deltas:
                if value > 0:
                    print(f"    +{value:.0f} {name}")
            print("  concrete_own_count_edits_to_match_reference(joined)")
            shown = 0
            for name, value in joined_deltas:
                if value > 0:
                    print(f"    +{value:.0f} {name}")
                    shown += 1
                    if shown >= args.example_limit:
                        break
            print()

    print(
        "center-spine bucket00 pocket-basis geometry diff completed "
        + datetime.now().isoformat(timespec="seconds")
        + f" total_elapsed={time.time() - total_start:.1f}s",
        flush=True,
    )


if __name__ == "__main__":
    main()
