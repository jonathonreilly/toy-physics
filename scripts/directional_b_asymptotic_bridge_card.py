#!/usr/bin/env python3
"""Render a compact asymptotic bridge card for the directional b lane.

This is a theory-facing closeout for the recent bounded denominator work.  It
does not search new observables.  Instead it reuses the same generated-DAG
family and translates the retained empirical result into a small bridge:

- leading retained mass-geometry term: center offset ``b``
- finite-source correction: nearest-edge ``b - h_mass``
- discrete packet-support correction: ``b - (h_mass + delta_packet)``

where ``delta_packet`` comes from the free packet's retained probe-band edge.
The goal is to say which piece looks asymptotically retainable and which piece
still looks graph-family specific on the current bounded evidence.
"""

from __future__ import annotations

from collections import defaultdict
from concurrent.futures import ProcessPoolExecutor
from dataclasses import dataclass
import argparse
import math
import multiprocessing as mp
import os
import statistics
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.directional_b_denominator_geometry_diagnostic import (  # noqa: E402
    TrialRow,
    _coefficient_of_variation,
    _evaluate_geometry_trial,
)
from scripts.directional_b_readout_compare import DEFAULT_IMPACT_BS, DEFAULT_N_LAYERS  # noqa: E402


@dataclass(frozen=True)
class FamilySummary:
    n_layers: int
    mean_mass_half_span: float
    cv_mass_half_span: float
    mean_band_high_rel: float
    cv_band_high_rel: float
    mean_support_correction: float
    low_b_support_correction: float
    high_b_support_correction: float
    action_b_start: float
    action_b_end: float
    action_gap_start: float
    action_gap_end: float
    flow_b_start: float
    flow_b_end: float
    flow_gap_start: float
    flow_gap_end: float


def _first_last_valid(by_target: dict[float, list[TrialRow]], field: str) -> tuple[float, float]:
    first = None
    last = None
    for target_b in sorted(by_target):
        values = [getattr(row, field) for row in by_target[target_b]]
        values = [value for value in values if not math.isnan(value)]
        if not values:
            continue
        mean_value = statistics.fmean(values)
        if first is None:
            first = mean_value
        last = mean_value
    if first is None or last is None:
        return float("nan"), float("nan")
    return first, last


def _summarize_family(rows: list[TrialRow], n_layers: int) -> FamilySummary:
    bucket = [row for row in rows if row.n_layers == n_layers]
    by_target: dict[float, list[TrialRow]] = defaultdict(list)
    for row in bucket:
        by_target[row.target_b].append(row)
    ordered_targets = sorted(by_target)

    def mean_metric(target_b: float, field: str) -> float:
        return statistics.fmean(getattr(row, field) for row in by_target[target_b])

    action_gap_start, action_gap_end = _first_last_valid(by_target, "action_over_support_gap")
    flow_gap_start, flow_gap_end = _first_last_valid(by_target, "flow_over_support_gap")

    return FamilySummary(
        n_layers=n_layers,
        mean_mass_half_span=statistics.fmean(row.mass_half_span for row in bucket),
        cv_mass_half_span=_coefficient_of_variation([row.mass_half_span for row in bucket]),
        mean_band_high_rel=statistics.fmean(row.band_high_rel for row in bucket),
        cv_band_high_rel=_coefficient_of_variation([row.band_high_rel for row in bucket]),
        mean_support_correction=statistics.fmean(row.support_correction for row in bucket),
        low_b_support_correction=mean_metric(ordered_targets[0], "support_correction"),
        high_b_support_correction=mean_metric(ordered_targets[-1], "support_correction"),
        action_b_start=mean_metric(ordered_targets[0], "action_over_b"),
        action_b_end=mean_metric(ordered_targets[-1], "action_over_b"),
        action_gap_start=action_gap_start,
        action_gap_end=action_gap_end,
        flow_b_start=mean_metric(ordered_targets[0], "flow_over_b"),
        flow_b_end=mean_metric(ordered_targets[-1], "flow_over_b"),
        flow_gap_start=flow_gap_start,
        flow_gap_end=flow_gap_end,
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workers", type=int, default=min(8, max(1, os.cpu_count() or 1)))
    parser.add_argument("--seeds", type=int, default=5)
    parser.add_argument("--n-layers", nargs="+", type=int, default=list(DEFAULT_N_LAYERS))
    parser.add_argument("--impact-bs", nargs="+", type=float, default=list(DEFAULT_IMPACT_BS))
    parser.add_argument("--angle-beta", type=float, default=0.8)
    parser.add_argument("--retain-share", type=float, default=0.5)
    parser.add_argument("--mass-nodes", type=int, default=3)
    args = parser.parse_args()

    tasks = [
        (n_layers, target_b, seed, args.angle_beta, args.retain_share, args.mass_nodes)
        for n_layers in args.n_layers
        for target_b in args.impact_bs
        for seed in range(args.seeds)
    ]

    ctx = mp.get_context("fork")
    if args.workers <= 1:
        rows = [_evaluate_geometry_trial(task) for task in tasks]
    else:
        try:
            with ProcessPoolExecutor(max_workers=args.workers, mp_context=ctx) as pool:
                rows = list(pool.map(_evaluate_geometry_trial, tasks))
        except (OSError, PermissionError):
            rows = [_evaluate_geometry_trial(task) for task in tasks]
    rows = [row for row in rows if row is not None]

    families = [_summarize_family(rows, n_layers) for n_layers in args.n_layers]

    print("=" * 112)
    print("DIRECTIONAL-MEASURE B ASYMPTOTIC BRIDGE CARD")
    print("=" * 112)
    print(
        "Retained directional transport fixed. This card reuses the same bounded random-DAG family and"
    )
    print("translates the denominator results into a compact leading-term / correction hierarchy.")
    print()
    print("Proposed bounded hierarchy:")
    print("  leading term           : b")
    print("  finite-source correction: b - h_mass")
    print("  packet-support correction: b - (h_mass + delta_packet)")
    print("  where h_mass is the mass half-span and delta_packet is the retained free probe-band edge.")
    print()
    print(f"{'N':>4s} {'h_mass':>10s} {'cv(h)':>10s} {'delta_pkt':>11s} {'cv(delta)':>11s} {'corr@low':>10s} {'corr@high':>11s}")
    print("-" * 80)
    for fam in families:
        print(
            f"{fam.n_layers:4d} "
            f"{fam.mean_mass_half_span:+10.4f} "
            f"{fam.cv_mass_half_span:10.2%} "
            f"{fam.mean_band_high_rel:+11.4f} "
            f"{fam.cv_band_high_rel:11.2%} "
            f"{fam.low_b_support_correction:+10.4f} "
            f"{fam.high_b_support_correction:+11.4f}"
        )
    print()
    print("Endpoint density comparison:")
    print(f"{'N':>4s} {'A/b':>18s} {'A/gap':>18s} {'F/b':>18s} {'F/gap':>18s}")
    print("-" * 80)
    def fmt_pair(a: float, b: float) -> str:
        if math.isnan(a) or math.isnan(b):
            return f"{'n/a':>18s}"
        return f"{a:+8.4f}->{b:+8.4f}"
    for fam in families:
        print(
            f"{fam.n_layers:4d} "
            f"{fmt_pair(fam.action_b_start, fam.action_b_end)} "
            f"{fmt_pair(fam.action_gap_start, fam.action_gap_end)} "
            f"{fmt_pair(fam.flow_b_start, fam.flow_b_end)} "
            f"{fmt_pair(fam.flow_gap_start, fam.flow_gap_end)}"
        )
    print()
    print("Retained reading:")
    print("  1. The mass half-span is modest and comparatively stable within each bounded family slice.")
    print("  2. The retained free probe-band edge is even more family-fixed than the mass half-span.")
    print("  3. Therefore support-gap is not a purer local mass law; it is b plus a graph-family packet correction.")
    print("  4. Center-offset density is the cleanest bounded leading term because it isolates mass placement.")
    print("  5. Nearest-edge density stays a sensible finite-source correction.")
    print("  6. Support-gap should stay secondary until a wider asymptotic family shows delta_packet shrinking or transferring.")
    print()
    print("Heuristic asymptotic translation:")
    print("  response density ~ Numerator / b                    (retained leading term)")
    print("  edge-corrected   ~ Numerator / (b - h_mass)         (finite source width)")
    print("  support-corrected~ Numerator / (b - h_mass - delta_packet)")
    print("  The last term should currently be read as discrete packet-support structure, not the main law.")


if __name__ == "__main__":
    main()
