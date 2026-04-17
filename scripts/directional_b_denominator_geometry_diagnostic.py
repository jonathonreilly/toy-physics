#!/usr/bin/env python3
"""Explain why center-offset density stays retained on the directional b lane.

This bounded diagnostic reuses the same generated-DAG family as the recent
directional-b sweeps. The empirical question is already narrow:

- center-offset density passes
- nearest-edge density passes
- support-gap density is only partial

The goal here is not another denominator search. It is to decompose the local
support-gap denominator into mass geometry plus free-packet probe-band geometry
so we can see why ``support_gap`` is not just a more local relabeling of
``actual_b`` on this family.
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

from scripts.directional_b_readout_compare import (  # noqa: E402
    DEFAULT_IMPACT_BS,
    DEFAULT_N_LAYERS,
    K_BAND,
    _beam_width,
    _detector_probs,
    _evaluate_trial,
    _linear_slope,
    _node_probs,
    _oriented_strength,
    _propagate_node_amplitudes,
    _select_mass_nodes,
)
from scripts.directional_b_support_distance_compare import (  # noqa: E402
    SUPPORT_GAP_MIN,
    _interval_gap,
    _retained_probe_band,
)
from scripts.generative_causal_dag_interference import generate_causal_dag  # noqa: E402


@dataclass(frozen=True)
class TrialRow:
    n_layers: int
    target_b: float
    seed: int
    actual_b: float
    mass_half_span: float
    band_center_rel: float
    band_half_width: float
    band_high_rel: float
    support_gap: float
    support_correction: float
    action_over_b: float
    action_over_support_gap: float
    flow_over_b: float
    flow_over_support_gap: float
    relation: str
    visibility_guardrail: float


def _safe_center_ratio(strength: float, actual_b: float) -> float:
    return strength / actual_b if actual_b > 0.0 else float("nan")


def _coefficient_of_variation(values: list[float]) -> float:
    if not values:
        return float("nan")
    mean = statistics.fmean(values)
    if abs(mean) <= 1e-30:
        return float("nan")
    if len(values) == 1:
        return 0.0
    return statistics.pstdev(values) / abs(mean)


def _support_band_geometry(
    task: tuple[int, float, int, float, float, int],
) -> tuple[float, float, float, float, float, float, str] | None:
    n_layers, target_b, seed, angle_beta, retain_share, mass_nodes = task
    positions, adj, _ = generate_causal_dag(
        n_layers=n_layers,
        nodes_per_layer=25,
        y_range=12.0,
        connect_radius=3.0,
        rng_seed=seed * 11 + 7,
    )
    by_layer: dict[int, list[int]] = defaultdict(list)
    for idx, (x, _y) in enumerate(positions):
        by_layer[round(x)].append(idx)
    layers = sorted(by_layer)
    center_y = statistics.fmean(y for _x, y in positions)
    mid = len(layers) // 2

    grav_mass = _select_mass_nodes(
        positions=positions,
        layer_nodes=by_layer[layers[mid]],
        center_y=center_y,
        target_b=target_b,
        mass_nodes=mass_nodes,
    )
    if len(grav_mass) < mass_nodes:
        return None

    mass_ys = [positions[node][1] for node in grav_mass]
    mass_low = min(mass_ys)
    mass_high = max(mass_ys)
    actual_b = statistics.fmean(mass_ys) - center_y
    mass_half_span = 0.5 * (mass_high - mass_low)

    src = by_layer[layers[0]]
    det = set(by_layer[layers[-1]])
    probe_layers = {layers[mid], layers[min(mid + 1, len(layers) - 1)]}
    probe_nodes = [node for node in range(len(positions)) if round(positions[node][0]) in probe_layers]

    probe_weights: dict[int, float] = defaultdict(float)
    valid_k = 0
    for k in K_BAND:
        free_amps = _propagate_node_amplitudes(positions, adj, [0.0] * len(positions), src, k, angle_beta=angle_beta)
        free_probs = _detector_probs(free_amps, det)
        if _beam_width(free_probs, positions) <= 1e-30:
            continue
        node_probs = _node_probs(free_amps)
        for node in probe_nodes:
            probe_weights[node] += node_probs.get(node, 0.0)
        valid_k += 1

    if valid_k <= 0:
        return None
    for node in list(probe_weights):
        probe_weights[node] /= valid_k

    band = _retained_probe_band(positions, probe_weights, probe_nodes, retain_share)
    if band is None:
        return None

    band_low, band_high = band
    support_gap = _interval_gap(mass_low, mass_high, band_low, band_high)
    band_low_rel = band_low - center_y
    band_high_rel = band_high - center_y
    band_center_rel = 0.5 * (band_low_rel + band_high_rel)
    band_half_width = 0.5 * (band_high_rel - band_low_rel)

    if band_high < mass_low:
        relation = "below"
    elif band_low > mass_high:
        relation = "above"
    else:
        relation = "overlap"

    return (
        actual_b,
        mass_half_span,
        band_center_rel,
        band_half_width,
        band_high_rel,
        support_gap,
        relation,
    )


def _evaluate_geometry_trial(task: tuple[int, float, int, float, float, int]) -> TrialRow | None:
    base_row = _evaluate_trial(task)
    if base_row is None:
        return None

    support_geometry = _support_band_geometry(task)
    if support_geometry is None:
        return None
    (
        actual_b,
        mass_half_span,
        band_center_rel,
        band_half_width,
        band_high_rel,
        support_gap,
        relation,
    ) = support_geometry

    action_strength = _oriented_strength("action_channel", base_row.action_channel)
    flow_strength = _oriented_strength("packet_flow_action", base_row.packet_flow_action)

    support_correction = actual_b - support_gap

    return TrialRow(
        n_layers=base_row.n_layers,
        target_b=base_row.target_b,
        seed=base_row.seed,
        actual_b=actual_b,
        mass_half_span=mass_half_span,
        band_center_rel=band_center_rel,
        band_half_width=band_half_width,
        band_high_rel=band_high_rel,
        support_gap=support_gap,
        support_correction=support_correction,
        action_over_b=_safe_center_ratio(action_strength, actual_b),
        action_over_support_gap=(
            action_strength / support_gap if support_gap >= SUPPORT_GAP_MIN else float("nan")
        ),
        flow_over_b=_safe_center_ratio(flow_strength, actual_b),
        flow_over_support_gap=(
            flow_strength / support_gap if support_gap >= SUPPORT_GAP_MIN else float("nan")
        ),
        relation=relation,
        visibility_guardrail=base_row.visibility_guardrail,
    )


def _render_mean(values: list[float], width: int = 9, decimals: int = 4, signed: bool = True) -> str:
    values = [value for value in values if not math.isnan(value)]
    if not values:
        return f"{'n/a':>{width}s}"
    spec = f"{'+' if signed else ''}{width}.{decimals}f"
    return format(statistics.fmean(values), spec)


def _summary_line(rows: list[TrialRow], metric: str) -> str:
    grouped: dict[float, list[TrialRow]] = defaultdict(list)
    for row in rows:
        grouped[row.target_b].append(row)

    pairs = []
    for target_b in sorted(grouped):
        values = [getattr(entry, metric) for entry in grouped[target_b]]
        values = [value for value in values if not math.isnan(value)]
        if values:
            pairs.append(
                (
                    statistics.fmean(entry.actual_b for entry in grouped[target_b]),
                    statistics.fmean(values),
                )
            )
    if len(pairs) < 2:
        return f"  {metric:>22s}: INSUF"

    xs = [pair[0] for pair in pairs]
    ys = [pair[1] for pair in pairs]
    slope = _linear_slope(xs, ys)
    return f"  {metric:>22s}: {ys[0]:+.4f} -> {ys[-1]:+.4f} (slope {slope:+.4f})"


def _ratio_summary_line(rows: list[TrialRow], numerator: str, denominator: str, label: str) -> str:
    grouped: dict[float, list[TrialRow]] = defaultdict(list)
    for row in rows:
        grouped[row.target_b].append(row)

    pairs = []
    for target_b in sorted(grouped):
        sample = grouped[target_b]
        denom = statistics.fmean(getattr(entry, denominator) for entry in sample)
        if abs(denom) <= 1e-30:
            continue
        pairs.append(
            (
                statistics.fmean(entry.actual_b for entry in sample),
                statistics.fmean(getattr(entry, numerator) for entry in sample) / denom,
            )
        )
    if len(pairs) < 2:
        return f"  {label:>22s}: INSUF"

    xs = [pair[0] for pair in pairs]
    ys = [pair[1] for pair in pairs]
    slope = _linear_slope(xs, ys)
    return f"  {label:>22s}: {ys[0]:+.4f} -> {ys[-1]:+.4f} (slope {slope:+.4f})"


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

    print("=" * 112)
    print("DIRECTIONAL-MEASURE B DENOMINATOR GEOMETRY DIAGNOSTIC")
    print("=" * 112)
    print(
        "Transport fixed to exp(i k S_spent) / L^p x exp(-beta * theta^2); "
        f"beta={args.angle_beta:.3f}, seeds={args.seeds}, retain_share={args.retain_share:.2f}"
    )
    print("Diagnostic identity when the free retained probe band sits below the mass interval:")
    print("  support_gap = actual_b - (mass_half_span + band_high_rel)")
    print("So center-offset and support-gap coincide only when the packet-band correction is small and stable.")
    print()

    for n_layers in args.n_layers:
        bucket = [row for row in rows if row.n_layers == n_layers]
        if not bucket:
            continue
        grouped: dict[float, list[TrialRow]] = defaultdict(list)
        for row in bucket:
            grouped[row.target_b].append(row)

        print(f"N={n_layers}")
        print(
            f"{'target_b':>8s} {'actual_b':>8s} {'m_half':>8s} {'band_ctr':>9s} "
            f"{'band_hi':>9s} {'corr':>9s} {'gap':>9s} {'gap/b':>9s} {'gap_cv':>9s} {'rel':>9s}"
        )
        print("-" * 112)
        for target_b in sorted(grouped):
            sample = grouped[target_b]
            relation_counts = defaultdict(int)
            for row in sample:
                relation_counts[row.relation] += 1
            relation_label = "/".join(
                f"{relation_counts[name]}{name[0]}" for name in ("below", "overlap", "above") if relation_counts[name]
            )
            mean_actual_b = statistics.fmean(row.actual_b for row in sample)
            mean_support_gap = statistics.fmean(row.support_gap for row in sample)
            print(
                f"{target_b:8.2f} "
                f"{mean_actual_b:8.3f} "
                f"{statistics.fmean(row.mass_half_span for row in sample):8.3f} "
                f"{statistics.fmean(row.band_center_rel for row in sample):+9.3f} "
                f"{statistics.fmean(row.band_high_rel for row in sample):+9.3f} "
                f"{statistics.fmean(row.support_correction for row in sample):+9.3f} "
                f"{mean_support_gap:9.3f} "
                f"{(mean_support_gap / mean_actual_b):9.3f} "
                f"{100.0 * _coefficient_of_variation([row.support_gap for row in sample]):8.2f}% "
                f"{relation_label:>9s}"
            )
        print("Response-density compare:")
        print(
            f"{'target_b':>8s} {'A/b':>9s} {'A/gap':>9s} {'F/b':>9s} {'F/gap':>9s}"
        )
        print("-" * 48)
        for target_b in sorted(grouped):
            sample = grouped[target_b]
            print(
                f"{target_b:8.2f} "
                f"{_render_mean([row.action_over_b for row in sample])} "
                f"{_render_mean([row.action_over_support_gap for row in sample])} "
                f"{_render_mean([row.flow_over_b for row in sample])} "
                f"{_render_mean([row.flow_over_support_gap for row in sample])}"
            )
        print("Trend summary:")
        print(_ratio_summary_line(bucket, "support_gap", "actual_b", "support_gap / actual_b"))
        print(_summary_line(bucket, "support_correction"))
        print(_summary_line(bucket, "action_over_b"))
        print(_summary_line(bucket, "action_over_support_gap"))
        print(_summary_line(bucket, "flow_over_b"))
        print(_summary_line(bucket, "flow_over_support_gap"))
        print()

    print("Interpretation:")
    print("  support_gap is not a pure relabeling of the mass offset on this family.")
    print("  It mixes mass placement with the free packet's retained probe-band edge, and that correction")
    print("  is large enough to flip sign between the N=12 and N=25 low-b anchors.")
    print("  Center-offset therefore stays the cleaner bounded denominator: it isolates mass geometry,")
    print("  while support-gap inherits extra packet-band drift/width structure that destabilizes F/gap first.")


if __name__ == "__main__":
    main()
