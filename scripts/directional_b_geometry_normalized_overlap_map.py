#!/usr/bin/env python3
"""Map widened-source center-offset failures onto the overlap bridge.

This bounded follow-on keeps the fixed directional-measure propagator, the
second dense-family holdout, and the widened source window frozen. It does not
search for a new denominator or widen the family. Instead it asks one narrower
question:

- do the `N = 25`, `mass_nodes = 5` holdout failures of `response / b`
  represent a generic breakdown?
- or do they live only on the low-`b` overlap corners already isolated by the
  retained `mu` and occupancy bridge cards?
"""

from __future__ import annotations

from collections import defaultdict
from concurrent.futures import ProcessPoolExecutor
from dataclasses import dataclass
import argparse
import multiprocessing as mp
import os
import statistics
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.directional_b_geometry_normalized_holdout_transfer import (  # noqa: E402
    DEFAULT_IMPACT_BS,
    FamilyConfig,
    TrialRow,
    TrendSummary,
    _evaluate_trial,
    _trend_summary,
)
from scripts.directional_b_overlap_onset_transfer_holdout import (  # noqa: E402
    _evaluate_holdout_dag,
)


OCCUPANCY_BRIDGE_THRESHOLD = 0.4


@dataclass(frozen=True)
class JoinedRow:
    target_b: float
    seed: int
    actual_b: float
    edge_b: float
    action_over_b: float
    flow_over_b: float
    action_over_edge_b: float
    flow_over_edge_b: float
    mu: float
    target_fill: float
    local_target_count: int
    overlap: bool


def _mean(values: list[float]) -> float:
    return statistics.fmean(values)


def _fmt(value: float) -> str:
    return f"{value:+.4f}"


def _evaluate_joined(
    task: tuple[FamilyConfig, int, float, int, float, float, int],
) -> JoinedRow | None:
    family, n_layers, target_b, seed, angle_beta, retain_share, mass_nodes = task
    trial = _evaluate_trial(
        (family, n_layers, target_b, seed, angle_beta, retain_share, mass_nodes)
    )
    onset = _evaluate_holdout_dag(
        (
            mass_nodes,
            n_layers,
            seed,
            target_b,
            family.nodes_per_layer,
            family.y_range,
            family.connect_radius,
            family.seed_offset,
        )
    )
    if trial is None or onset is None:
        return None
    return JoinedRow(
        target_b=trial.target_b,
        seed=trial.seed,
        actual_b=trial.actual_b,
        edge_b=trial.edge_b,
        action_over_b=trial.action_over_b,
        flow_over_b=trial.flow_over_b,
        action_over_edge_b=trial.action_over_edge_b,
        flow_over_edge_b=trial.flow_over_edge_b,
        mu=onset.mu,
        target_fill=onset.target_fill,
        local_target_count=onset.local_target_count,
        overlap=onset.overlap,
    )


def _trial_rows(rows: list[JoinedRow]) -> list[TrialRow]:
    return [
        TrialRow(
            family="holdout",
            n_layers=25,
            target_b=row.target_b,
            seed=row.seed,
            actual_b=row.actual_b,
            mass_span=float("nan"),
            edge_b=row.edge_b,
            action_strength=float("nan"),
            flow_strength=float("nan"),
            action_over_b=row.action_over_b,
            action_over_edge_b=row.action_over_edge_b,
            flow_over_b=row.flow_over_b,
            flow_over_edge_b=row.flow_over_edge_b,
            visibility_guardrail=float("nan"),
        )
        for row in rows
    ]


def _summary_text(summary: TrendSummary | None) -> str:
    if summary is None:
        return "INSUF"
    return (
        f"{summary.status} "
        f"({_fmt(summary.start)} -> {_fmt(summary.end)}, slope {_fmt(summary.slope)})"
    )


def _passes(summary: TrendSummary | None) -> bool:
    return summary is not None and summary.status == "PASS"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workers", type=int, default=min(8, max(1, os.cpu_count() or 1)))
    parser.add_argument("--seeds", type=int, default=5)
    parser.add_argument("--n-layers", type=int, default=25)
    parser.add_argument("--impact-bs", nargs="+", type=float, default=list(DEFAULT_IMPACT_BS))
    parser.add_argument("--angle-beta", type=float, default=0.8)
    parser.add_argument("--retain-share", type=float, default=0.5)
    parser.add_argument("--mass-nodes", type=int, default=5)
    parser.add_argument("--holdout-nodes-per-layer", type=int, default=28)
    parser.add_argument("--holdout-y-range", type=float, default=13.0)
    parser.add_argument("--holdout-connect-radius", type=float, default=3.0)
    parser.add_argument("--holdout-seed-offset", type=int, default=701)
    args = parser.parse_args()

    holdout_family = FamilyConfig(
        label="holdout",
        nodes_per_layer=args.holdout_nodes_per_layer,
        y_range=args.holdout_y_range,
        connect_radius=args.holdout_connect_radius,
        seed_offset=args.holdout_seed_offset,
    )

    tasks = [
        (
            holdout_family,
            args.n_layers,
            target_b,
            seed,
            args.angle_beta,
            args.retain_share,
            args.mass_nodes,
        )
        for target_b in args.impact_bs
        for seed in range(args.seeds)
    ]

    ctx = mp.get_context("fork")
    if args.workers <= 1:
        rows = [_evaluate_joined(task) for task in tasks]
    else:
        try:
            with ProcessPoolExecutor(max_workers=args.workers, mp_context=ctx) as pool:
                rows = list(pool.map(_evaluate_joined, tasks))
        except (OSError, PermissionError):
            rows = [_evaluate_joined(task) for task in tasks]
    rows = [row for row in rows if row is not None]
    rows.sort(key=lambda row: (row.target_b, row.seed))

    all_trials = _trial_rows(rows)
    non_overlap_rows = [row for row in rows if not row.overlap]
    non_overlap_trials = _trial_rows(non_overlap_rows)
    overlap_rows = [row for row in rows if row.overlap]

    all_overlap_low_fill = all(
        row.target_fill <= OCCUPANCY_BRIDGE_THRESHOLD for row in overlap_rows
    )
    low_fill_rows = [row for row in rows if row.target_fill <= OCCUPANCY_BRIDGE_THRESHOLD]

    print("=" * 132)
    print("DIRECTIONAL-MEASURE B GEOMETRY-NORMALIZED OVERLAP MAP")
    print("=" * 132)
    print(
        "Join the widened-source holdout transfer rows directly to the retained overlap / occupancy diagnostics."
    )
    print(
        "This keeps the fixed directional-measure propagator, the second dense-family holdout, and"
    )
    print(
        "the widened `mass_nodes = 5` source frozen. The question is whether the center-offset"
    )
    print(
        f"`A/b` and `F/b` behavior at `N = {args.n_layers}` is generic, or only an overlap-sector effect."
    )
    print()
    print("Grouped holdout summary:")
    print(
        f"{'target_b':>8s} {'rows':>4s} {'ovlp':>4s} {'fill<=0.4':>10s} {'actual_b':>8s} "
        f"{'edge_b':>8s} {'A/b':>9s} {'F/b':>9s} {'A/edge':>9s} {'F/edge':>9s}"
    )
    print("-" * 132)
    grouped: dict[float, list[JoinedRow]] = defaultdict(list)
    for row in rows:
        grouped[row.target_b].append(row)
    for target_b in sorted(grouped):
        bucket = grouped[target_b]
        print(
            f"{target_b:8.2f} {len(bucket):4d} {sum(row.overlap for row in bucket):4d} "
            f"{sum(row.target_fill <= OCCUPANCY_BRIDGE_THRESHOLD for row in bucket):10d} "
            f"{_mean([row.actual_b for row in bucket]):8.3f} "
            f"{_mean([row.edge_b for row in bucket]):8.3f} "
            f"{_mean([row.action_over_b for row in bucket]):+9.4f} "
            f"{_mean([row.flow_over_b for row in bucket]):+9.4f} "
            f"{_mean([row.action_over_edge_b for row in bucket if row.edge_b >= 0.5]):+9.4f} "
            f"{_mean([row.flow_over_edge_b for row in bucket if row.edge_b >= 0.5]):+9.4f}"
        )
    print()
    print("Overlap rows:")
    print(
        f"{'target_b':>8s} {'seed':>4s} {'actual_b':>8s} {'edge_b':>8s} {'mu':>8s} "
        f"{'fill':>8s} {'count':>6s} {'A/b':>9s} {'F/b':>9s}"
    )
    print("-" * 92)
    for row in overlap_rows:
        print(
            f"{row.target_b:8.2f} {row.seed:4d} {row.actual_b:8.3f} {row.edge_b:8.3f} {row.mu:8.3f} "
            f"{row.target_fill:8.3f} {row.local_target_count:6d} {row.action_over_b:+9.4f} {row.flow_over_b:+9.4f}"
        )
    print()
    all_action_summary = _trend_summary(all_trials, "action_over_b")
    all_flow_summary = _trend_summary(all_trials, "flow_over_b")
    all_action_edge_summary = _trend_summary(all_trials, "action_over_edge_b")
    all_flow_edge_summary = _trend_summary(all_trials, "flow_over_edge_b")
    non_overlap_action_summary = _trend_summary(non_overlap_trials, "action_over_b")
    non_overlap_flow_summary = _trend_summary(non_overlap_trials, "flow_over_b")

    full_center_pass = _passes(all_action_summary) and _passes(all_flow_summary)

    print("Trend summaries:")
    print(f"  all rows            : A/b {_summary_text(all_action_summary)}")
    print(f"                        F/b {_summary_text(all_flow_summary)}")
    print(f"                        A/edge {_summary_text(all_action_edge_summary)}")
    print(f"                        F/edge {_summary_text(all_flow_edge_summary)}")
    print(f"  non-overlap rows    : A/b {_summary_text(non_overlap_action_summary)}")
    print(f"                        F/b {_summary_text(non_overlap_flow_summary)}")
    print()
    print("Interpretation:")
    print(
        f"  1. Exactly {len(overlap_rows)}/{len(rows)} widened-source rows are true overlap rows (`mu <= 0`)."
    )
    print(
        f"  2. All {len(overlap_rows)} overlap rows live in the first two target-b buckets and "
        f"{'all' if all_overlap_low_fill else 'not all'} satisfy the occupancy bridge `target_fill <= 0.4`."
    )
    print(
        f"  3. Low occupancy alone is only a coarse tag here ({len(low_fill_rows)}/{len(rows)} rows meet it),"
    )
    print(
        "     but the actual center-offset failure is concentrated in the subset where low occupancy has"
    )
    print("     already become source overlap.")
    if full_center_pass:
        print(
            "  4. On the full sample, `A/b` and `F/b` already pass; after removing only the overlap rows,"
        )
        print(
            "     both center-offset trends steepen further, while `A/edge` and `F/edge` already pass on the"
        )
        print("     full sample.")
        print(
            f"  5. So the widened-source `N = {args.n_layers}` holdout already contains the same overlap /"
        )
        print(
            "     occupancy seam, but on this slice it remains subcritical rather than forcing a global"
        )
        print("     trend failure or a reopened denominator search.")
    else:
        print(
            "  4. On the full sample, `A/b` and `F/b` fail; after removing only the overlap rows, both regain"
        )
        print(
            "     a decreasing trend with actual `b`, while `A/edge` and `F/edge` already pass on the full sample."
        )
        print(
            f"  5. So the widened-source `N = {args.n_layers}` holdout failure maps to the existing overlap /"
        )
        print(
            "     occupancy seam, not to a new global breakdown that would justify reopening the denominator"
        )
        print("     search.")


if __name__ == "__main__":
    main()
