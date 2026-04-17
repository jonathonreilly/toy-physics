#!/usr/bin/env python3
"""Crosswalk the retained wide and self:sparse-25 residual branches.

The current residuals are:

- `wide`: flips when added late support fails to land enough extra field on the packet
- `self:sparse-25`: flips when added late support collapses forward corridor support

This script tests whether those are really one smaller forward-packet-retiming
family or whether they should stay as separate residual mechanisms.
"""

from __future__ import annotations

import argparse
import itertools
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.generated_dag_pattern_sourced_late_support_flip_compare import run_rows  # noqa: E402


FORWARD_FAMILY = [
    "extra_field_mean_on_packet",
    "extra_packet_side_gap",
    "extra_support_corridor_share",
    "extra_support_forward_share",
    "extra_forward_side_gap",
]

WIDE_RULE = ("extra_field_mean_on_packet", "<=", 0.0010)
SELF_SPARSE_RULE = ("extra_support_corridor_share", "<=", 0.0000)


def _mean(values):
    values = list(values)
    return sum(values) / len(values) if values else 0.0


def _apply_clause(row, clause):
    feature, comparator, threshold = clause
    value = getattr(row, feature)
    if comparator == "<=":
        return value <= threshold
    return value >= threshold


def _accuracy(rows, clauses, mode="single"):
    truth = [row.flipped for row in rows]
    pred = []
    for row in rows:
        if mode == "single":
            hit = _apply_clause(row, clauses[0])
        elif mode == "or":
            hit = any(_apply_clause(row, clause) for clause in clauses)
        else:
            hit = all(_apply_clause(row, clause) for clause in clauses)
        pred.append(hit)
    return sum(p == t for p, t in zip(pred, truth)) / len(rows)


def _render_split(rows, clauses, mode="single"):
    matched = []
    unmatched = []
    for row in rows:
        if (mode == "single" and _apply_clause(row, clauses[0])) or (
            mode == "or" and any(_apply_clause(row, clause) for clause in clauses)
        ) or (
            mode == "and" and all(_apply_clause(row, clause) for clause in clauses)
        ):
            matched.append(row)
        else:
            unmatched.append(row)

    def render_group(label, subset):
        if not subset:
            return f"{label}: total=0"
        flips = sum(row.flipped for row in subset)
        return (
            f"{label}: total={len(subset)} flips={flips} stays={len(subset) - flips} "
            f"flip_fraction={flips / len(subset):.4f} "
            f"mean_last6_shift={_mean(row.last6_shift for row in subset):.4f}"
        )

    return f"{render_group('matched', matched)} | {render_group('unmatched', unmatched)}"


def _best_single(rows, features, comparators):
    best = None
    for feature in features:
        values = sorted(set(getattr(row, feature) for row in rows))
        for comparator in comparators:
            for threshold in values:
                clause = (feature, comparator, threshold)
                accuracy = _accuracy(rows, [clause], mode="single")
                candidate = (accuracy, clause)
                if best is None or candidate > best:
                    best = candidate
    return best


def _best_or(rows, features, comparators):
    best = None
    for feature_a, feature_b in itertools.combinations(features, 2):
        values_a = sorted(set(getattr(row, feature_a) for row in rows))
        values_b = sorted(set(getattr(row, feature_b) for row in rows))
        for comparator_a in comparators:
            for comparator_b in comparators:
                for threshold_a in values_a:
                    for threshold_b in values_b:
                        clauses = [
                            (feature_a, comparator_a, threshold_a),
                            (feature_b, comparator_b, threshold_b),
                        ]
                        accuracy = _accuracy(rows, clauses, mode="or")
                        candidate = (accuracy, clauses)
                        if best is None or candidate > best:
                            best = candidate
    return best


def _render_rule(label, clauses, accuracy, mode):
    if mode == "single":
        feature, comparator, threshold = clauses[0]
        expr = f"{feature} {comparator} {threshold:.4f}"
    else:
        expr = " or ".join(
            f"{feature} {comparator} {threshold:.4f}"
            for feature, comparator, threshold in clauses
        )
    return f"{label}: {expr} (accuracy={accuracy:.4f})"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seed-start", type=int, default=0)
    parser.add_argument("--seed-count", type=int, default=5)
    parser.add_argument("--steps", type=int, default=50)
    parser.add_argument("--source-steps", type=int, default=12)
    parser.add_argument("--neighbor-radius", type=float, default=2.5)
    parser.add_argument("--coupling", type=float, default=3.0)
    parser.add_argument("--workers", type=int, default=max(1, os.cpu_count() or 1))
    args = parser.parse_args()

    rows = run_rows(
        seeds=range(args.seed_start, args.seed_start + args.seed_count),
        workers=max(1, args.workers),
        steps=args.steps,
        source_steps=args.source_steps,
        coupling=args.coupling,
        neighbor_radius=args.neighbor_radius,
        source_offsets=[-3.0, 3.0],
    )
    wide_rows = [row for row in rows if row.mover_rule == "wide"]
    self_sparse_rows = [
        row for row in rows if row.mover_rule == "self" and row.config == "sparse-25"
    ]
    pooled_rows = wide_rows + self_sparse_rows

    wide_rule_acc_wide = _accuracy(wide_rows, [WIDE_RULE], mode="single")
    wide_rule_acc_self_sparse = _accuracy(self_sparse_rows, [WIDE_RULE], mode="single")
    self_rule_acc_self_sparse = _accuracy(self_sparse_rows, [SELF_SPARSE_RULE], mode="single")
    self_rule_acc_wide = _accuracy(wide_rows, [SELF_SPARSE_RULE], mode="single")

    pooled_best_single = _best_single(pooled_rows, FORWARD_FAMILY, ["<=", ">="])
    pooled_best_or = _best_or(pooled_rows, FORWARD_FAMILY, ["<=", ">="])
    pooled_best_deficit_or = _best_or(pooled_rows, FORWARD_FAMILY, ["<="])

    print("=" * 80)
    print("GENERATED DAG RESIDUAL BRANCH CROSSWALK COMPARE")
    print("=" * 80)
    print(
        f"Rows: wide={len(wide_rows)}, self_sparse={len(self_sparse_rows)}, "
        f"pooled={len(pooled_rows)}, neighbor_radius={args.neighbor_radius:.1f}, "
        f"coupling={args.coupling:.3f}"
    )
    print()
    print("Branch means:")
    print(
        "  "
        f"wide flips={sum(row.flipped for row in wide_rows)}/{len(wide_rows)} "
        f"mean_last6_shift={_mean(row.last6_shift for row in wide_rows):.4f} "
        f"mean_extra_field_on_packet={_mean(row.extra_field_mean_on_packet for row in wide_rows):.4f} "
        f"mean_extra_forward_share={_mean(row.extra_support_forward_share for row in wide_rows):.4f}"
    )
    print(
        "  "
        f"self_sparse flips={sum(row.flipped for row in self_sparse_rows)}/{len(self_sparse_rows)} "
        f"mean_last6_shift={_mean(row.last6_shift for row in self_sparse_rows):.4f} "
        f"mean_extra_packet_side_gap={_mean(row.extra_packet_side_gap for row in self_sparse_rows):.4f} "
        f"mean_extra_corridor_share={_mean(row.extra_support_corridor_share for row in self_sparse_rows):.4f}"
    )
    print()
    print("Retained branch-local rules on their home branch:")
    print(
        "  "
        + _render_rule(
            "wide-local",
            [WIDE_RULE],
            wide_rule_acc_wide,
            "single",
        )
    )
    print(
        "  "
        + _render_rule(
            "self_sparse-local",
            [SELF_SPARSE_RULE],
            self_rule_acc_self_sparse,
            "single",
        )
    )
    print()
    print("Cross-branch transfer of branch-local rules:")
    print(f"  wide-local on self_sparse: accuracy={wide_rule_acc_self_sparse:.4f}")
    print(f"  self_sparse-local on wide: accuracy={self_rule_acc_wide:.4f}")
    print()
    print(
        "  wide-local split on wide: "
        + _render_split(wide_rows, [WIDE_RULE], mode="single")
    )
    print(
        "  self_sparse-local split on self_sparse: "
        + _render_split(self_sparse_rows, [SELF_SPARSE_RULE], mode="single")
    )
    print()
    single_acc, single_clause = pooled_best_single
    print("Best pooled single rule over forward-family observables:")
    print("  " + _render_rule("pooled-single", [single_clause], single_acc, "single"))
    print(
        f"  branch accuracies: wide={_accuracy(wide_rows, [single_clause], mode='single'):.4f}, "
        f"self_sparse={_accuracy(self_sparse_rows, [single_clause], mode='single'):.4f}"
    )
    print()
    or_acc, or_clauses = pooled_best_or
    print("Best pooled two-clause OR over forward-family observables:")
    print("  " + _render_rule("pooled-or", or_clauses, or_acc, "or"))
    print(
        f"  branch accuracies: wide={_accuracy(wide_rows, or_clauses, mode='or'):.4f}, "
        f"self_sparse={_accuracy(self_sparse_rows, or_clauses, mode='or'):.4f}"
    )
    print()
    deficit_or_acc, deficit_or_clauses = pooled_best_deficit_or
    print("Best pooled deficit-only two-clause OR (all <= directions):")
    print("  " + _render_rule("pooled-deficit-or", deficit_or_clauses, deficit_or_acc, "or"))
    print(
        f"  branch accuracies: wide={_accuracy(wide_rows, deficit_or_clauses, mode='or'):.4f}, "
        f"self_sparse={_accuracy(self_sparse_rows, deficit_or_clauses, mode='or'):.4f}"
    )
    print()
    print("Interpretation:")
    print(
        "  This compare asks whether the retained wide and self:sparse-25 residual "
        "stories really collapse to one smaller forward-packet-retiming language. "
        "If branch-local rules fail to transfer and pooled forward-family rules stay "
        "materially weaker, the right retained picture is two residual mechanisms "
        "with a shared abstract forward-retiming theme rather than one universal law."
    )


if __name__ == "__main__":
    main()
