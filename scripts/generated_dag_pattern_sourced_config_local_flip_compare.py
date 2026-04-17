#!/usr/bin/env python3
"""Inspect a config-local slice of the late-support sign-flip residual.

This is the next bounded step after the rule-local `self` compare. The goal is
to see whether one noisy config, starting with `sparse-25`, closes more cleanly
than the pooled `self` rows, and whether the pooled self-local rule still
describes the slice.
"""

from __future__ import annotations

import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.generated_dag_pattern_sourced_late_support_flip_compare import (  # noqa: E402
    FEATURE_NAMES,
    _render_group,
    run_rows,
)


def _threshold_predictions(rows, feature, comparator, threshold):
    values = [float(getattr(row, feature)) for row in rows]
    if comparator == ">=":
        return [value >= threshold for value in values]
    return [value <= threshold for value in values]


def _accuracy(rows, predictions):
    truth = [row.flipped for row in rows]
    return sum(pred == target for pred, target in zip(predictions, truth)) / len(rows)


def _best_single_rules(rows, top_n=5):
    candidates = []
    for feature in FEATURE_NAMES:
        values = sorted(set(float(getattr(row, feature)) for row in rows))
        for comparator in (">=", "<="):
            for threshold in values:
                pred = _threshold_predictions(rows, feature, comparator, threshold)
                candidates.append((feature, comparator, threshold, _accuracy(rows, pred)))
    candidates.sort(key=lambda item: (item[3], item[0], -item[2]), reverse=True)
    unique = []
    seen = set()
    for feature, comparator, threshold, accuracy in candidates:
        key = (feature, comparator, round(threshold, 4))
        if key in seen:
            continue
        seen.add(key)
        unique.append((feature, comparator, threshold, accuracy))
        if len(unique) >= top_n:
            break
    return unique


def _render_threshold_split(rows, feature, comparator, threshold):
    matched = [
        row
        for row in rows
        if (getattr(row, feature) >= threshold if comparator == ">=" else getattr(row, feature) <= threshold)
    ]
    unmatched = [row for row in rows if row not in matched]

    def render_group(label, subset):
        if not subset:
            return f"{label}: total=0"
        flips = sum(row.flipped for row in subset)
        mean_shift = sum(row.last6_shift for row in subset) / len(subset)
        return (
            f"{label}: total={len(subset)} flips={flips} stays={len(subset) - flips} "
            f"flip_fraction={flips / len(subset):.4f} mean_last6_shift={mean_shift:.4f}"
        )

    return f"{render_group('matched', matched)} | {render_group('unmatched', unmatched)}"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mover-rule", default="self")
    parser.add_argument("--config", default="sparse-25")
    parser.add_argument("--reference-feature", default="extra_packet_side_gap")
    parser.add_argument("--reference-comparator", default="<=")
    parser.add_argument("--reference-threshold", type=float, default=-0.0962)
    parser.add_argument("--seed-start", type=int, default=0)
    parser.add_argument("--seed-count", type=int, default=5)
    parser.add_argument("--steps", type=int, default=50)
    parser.add_argument("--source-steps", type=int, default=12)
    parser.add_argument("--neighbor-radius", type=float, default=2.5)
    parser.add_argument("--coupling", type=float, default=3.0)
    parser.add_argument("--workers", type=int, default=max(1, os.cpu_count() or 1))
    args = parser.parse_args()

    rows = [
        row
        for row in run_rows(
            seeds=range(args.seed_start, args.seed_start + args.seed_count),
            workers=max(1, args.workers),
            steps=args.steps,
            source_steps=args.source_steps,
            coupling=args.coupling,
            neighbor_radius=args.neighbor_radius,
            source_offsets=[-3.0, 3.0],
        )
        if row.mover_rule == args.mover_rule and row.config == args.config
    ]
    best_rules = _best_single_rules(rows, top_n=5)

    print("=" * 80)
    print("GENERATED DAG CONFIG-LOCAL LATE-SUPPORT FLIP COMPARE")
    print("=" * 80)
    print(
        f"mover_rule={args.mover_rule} config={args.config} rows={len(rows)} "
        f"neighbor_radius={args.neighbor_radius:.1f} coupling={args.coupling:.3f}"
    )
    print()
    print(_render_group(rows, "stable_toward", lambda row: not row.flipped))
    print(_render_group(rows, "flip_to_away", lambda row: row.flipped))
    print()
    print("Pooled-rule split on this config:")
    print(
        "  "
        + _render_threshold_split(
            rows,
            args.reference_feature,
            args.reference_comparator,
            args.reference_threshold,
        )
    )
    print()
    print("Best config-local single-threshold rules:")
    for feature, comparator, threshold, accuracy in best_rules:
        print(
            "  "
            f"{feature} {comparator} {threshold:.4f} (accuracy={accuracy:.4f})"
        )
    print()
    print("Interpretation:")
    print(
        "  This compare asks whether the pooled self-rule separator already closes on "
        "the noisiest config, or whether the noisy slice has its own simpler local "
        "packet-bias law."
    )


if __name__ == "__main__":
    main()
