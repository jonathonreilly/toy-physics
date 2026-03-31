#!/usr/bin/env python3
"""Run the late-support sign-flip compare on a single mover-rule branch.

This is the rule-local follow-on to the pooled `last3_union` vs `last6_union`
compare. The pooled result said the sign flip is real but not yet closed by a
universal scalar, with the widest residual on the `wide` mover rule.
"""

from __future__ import annotations

import argparse
import os
import sys
from collections import defaultdict

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.generated_dag_packet_tracking_bridge_compare import (  # noqa: E402
    DISCOVERY_CONFIGS,
    HOLDOUT_CONFIGS,
)
from scripts.generated_dag_pattern_sourced_late_support_flip_compare import (  # noqa: E402
    _best_two_feature_rule,
    _render_group,
    _top_single_rules,
    run_rows,
)


def _render_config_breakdown(rows):
    lines = ["Rule-local config breakdown:"]
    buckets = defaultdict(list)
    for row in rows:
        buckets[row.config].append(row)
    for config in sorted(buckets):
        subset = buckets[config]
        flips = sum(row.flipped for row in subset)
        lines.append(
            "  "
            f"{config}: total={len(subset)} flips={flips} stays={len(subset) - flips} "
            f"flip_fraction={flips / len(subset):.4f} "
            f"mean_last6_shift={sum(row.last6_shift for row in subset) / len(subset):.4f}"
        )
    return lines


def _render_threshold_split(rows, feature, comparator, threshold):
    matched = [
        row
        for row in rows
        if (getattr(row, feature) >= threshold if comparator == ">=" else getattr(row, feature) <= threshold)
    ]
    unmatched = [row for row in rows if row not in matched]

    def render_group(label, subset):
        flips = sum(row.flipped for row in subset)
        mean_shift = sum(row.last6_shift for row in subset) / len(subset) if subset else 0.0
        return (
            f"{label}: total={len(subset)} flips={flips} stays={len(subset) - flips} "
            f"flip_fraction={flips / len(subset):.4f} mean_last6_shift={mean_shift:.4f}"
            if subset
            else f"{label}: total=0"
        )

    return f"{render_group('matched', matched)} | {render_group('unmatched', unmatched)}"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mover-rule", default="wide")
    parser.add_argument("--contrast-rule", default="self")
    parser.add_argument("--seed-start", type=int, default=0)
    parser.add_argument("--seed-count", type=int, default=5)
    parser.add_argument("--steps", type=int, default=50)
    parser.add_argument("--source-steps", type=int, default=12)
    parser.add_argument("--neighbor-radius", type=float, default=2.5)
    parser.add_argument("--coupling", type=float, default=3.0)
    parser.add_argument("--workers", type=int, default=max(1, os.cpu_count() or 1))
    args = parser.parse_args()

    all_rows = run_rows(
        seeds=range(args.seed_start, args.seed_start + args.seed_count),
        workers=max(1, args.workers),
        steps=args.steps,
        source_steps=args.source_steps,
        coupling=args.coupling,
        neighbor_radius=args.neighbor_radius,
        source_offsets=[-3.0, 3.0],
    )
    rows = [
        row
        for row in all_rows
        if row.mover_rule == args.mover_rule
    ]
    contrast_rows = [row for row in all_rows if row.mover_rule == args.contrast_rule]
    discovery_rows = [row for row in rows if row.config in DISCOVERY_CONFIGS]
    holdout_rows = [row for row in rows if row.config in HOLDOUT_CONFIGS]

    singles = _top_single_rules(discovery_rows, holdout_rows, top_n=5)
    best_pair = _best_two_feature_rule(discovery_rows, holdout_rows)
    best_single = singles[0]

    print("=" * 80)
    print("GENERATED DAG RULE-LOCAL LATE-SUPPORT FLIP COMPARE")
    print("=" * 80)
    print(
        f"mover_rule={args.mover_rule} rows={len(rows)} "
        f"neighbor_radius={args.neighbor_radius:.1f} coupling={args.coupling:.3f}"
    )
    print(
        f"Discovery configs: {sorted(DISCOVERY_CONFIGS)}; "
        f"holdout configs: {sorted(HOLDOUT_CONFIGS)}"
    )
    print()
    print(_render_group(rows, "stable_toward", lambda row: not row.flipped))
    print(_render_group(rows, "flip_to_away", lambda row: row.flipped))
    print()
    for line in _render_config_breakdown(rows):
        print(line)
    print()
    print("Top single-threshold discovery rules for the sign flip:")
    for rule in singles:
        print(f"  {rule.render()}")
    print()
    print("Best single-rule split on the target branch:")
    print(
        "  "
        + _render_threshold_split(
            rows,
            best_single.feature,
            best_single.comparator,
            best_single.threshold,
        )
    )
    print()
    print("Best two-feature discovery rule for the sign flip:")
    print(f"  {best_pair.render()}")
    print()
    if contrast_rows:
        print(f"Same best single rule on contrast branch ({args.contrast_rule}):")
        print(
            "  "
            + _render_threshold_split(
                contrast_rows,
                best_single.feature,
                best_single.comparator,
                best_single.threshold,
            )
        )
        print()
    print("Interpretation:")
    print(
        "  This rule-local compare asks whether the pooled residual was hiding a "
        "cleaner mover-rule-specific added-support geometry. The main target is the "
        "wide-rule branch, where the pooled flip fraction was largest."
    )


if __name__ == "__main__":
    main()
