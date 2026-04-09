#!/usr/bin/env python3
"""Test geometry-normalized directional-b transfer on a second dense family.

This bounded follow-on keeps the retained directional propagator and the same
action-style observables fixed. Instead of widening the denominator search
again, it asks a narrower transfer question:

- do the retained geometry-normalized response densities still decrease with
  actual impact parameter on the existing second dense-family holdout?

The comparison reuses the original dense generated-DAG family and the older
second dense-family holdout from the overlap-onset cards. The retained read is
family-local monotonicity, not one merged universal fit across both families.
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
    NEGATIVE_SLOPE_EPS,
    _beam_width,
    _detector_probs,
    _linear_slope,
    _node_probs,
    _oriented_strength,
    _propagate_action_means,
    _propagate_node_amplitudes,
    _select_mass_nodes,
)
from scripts.generative_causal_dag_interference import generate_causal_dag  # noqa: E402
from scripts.gravity_observable_readout_scaling_compare import (  # noqa: E402
    _action_channel_bias,
    _visibility_guardrail,
)
from scripts.gravity_packet_local_action_flow_transfer_compare import (  # noqa: E402
    _packet_flow_action_bias,
)
from scripts.two_register_decoherence import compute_field  # noqa: E402


EDGE_B_MIN = 0.5
EPS = 1e-9


@dataclass(frozen=True)
class FamilyConfig:
    label: str
    nodes_per_layer: int
    y_range: float
    connect_radius: float
    seed_offset: int


@dataclass(frozen=True)
class TrialRow:
    family: str
    n_layers: int
    target_b: float
    seed: int
    actual_b: float
    mass_span: float
    edge_b: float
    action_strength: float
    flow_strength: float
    action_over_b: float
    action_over_edge_b: float
    flow_over_b: float
    flow_over_edge_b: float
    visibility_guardrail: float


@dataclass(frozen=True)
class TrendSummary:
    start: float
    end: float
    slope: float
    status: str


BASELINE_FAMILY = FamilyConfig(
    label="baseline",
    nodes_per_layer=25,
    y_range=12.0,
    connect_radius=3.0,
    seed_offset=7,
)

HOLDOUT_FAMILY = FamilyConfig(
    label="holdout",
    nodes_per_layer=28,
    y_range=13.0,
    connect_radius=3.0,
    seed_offset=701,
)


def _safe_ratio(strength: float, denominator: float) -> float:
    return strength / denominator if denominator > 0.0 else float("nan")


def _evaluate_trial(
    task: tuple[FamilyConfig, int, float, int, float, float, int],
) -> TrialRow | None:
    family, n_layers, target_b, seed, angle_beta, retain_share, mass_nodes = task
    positions, adj, _meta = generate_causal_dag(
        n_layers=n_layers,
        nodes_per_layer=family.nodes_per_layer,
        y_range=family.y_range,
        connect_radius=family.connect_radius,
        rng_seed=seed * 11 + family.seed_offset,
    )
    by_layer: dict[int, list[int]] = defaultdict(list)
    for idx, (x, _y) in enumerate(positions):
        by_layer[round(x)].append(idx)
    layers = sorted(by_layer)
    if len(layers) < 5:
        return None

    src = by_layer[layers[0]]
    det = set(by_layer[layers[-1]])
    if not det:
        return None

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
    actual_b = statistics.fmean(mass_ys) - center_y
    mass_span = max(mass_ys) - min(mass_ys)
    edge_b = actual_b - 0.5 * mass_span

    n = len(positions)
    free_field = [0.0] * n
    mass_field = compute_field(positions, adj, grav_mass)
    source_layers = {layers[mid - 1], layers[mid]} if mid > 0 else {layers[mid]}
    probe_layers = {layers[mid], layers[min(mid + 1, len(layers) - 1)]}

    free_action_mean = _propagate_action_means(positions, adj, free_field, src, angle_beta=angle_beta)
    mass_action_mean = _propagate_action_means(positions, adj, mass_field, src, angle_beta=angle_beta)
    action_delta = {node: mass_action_mean.get(node, 0.0) - free_action_mean.get(node, 0.0) for node in range(n)}

    action_values: list[float] = []
    flow_values: list[float] = []
    visibility_values: list[float] = []

    for k in K_BAND:
        free_amps = _propagate_node_amplitudes(positions, adj, free_field, src, k, angle_beta=angle_beta)
        mass_amps = _propagate_node_amplitudes(positions, adj, mass_field, src, k, angle_beta=angle_beta)

        free_probs = _detector_probs(free_amps, det)
        mass_probs = _detector_probs(mass_amps, det)
        width_ref = _beam_width(free_probs, positions)
        if width_ref <= 1e-30:
            continue

        mass_node_probs = _node_probs(mass_amps)
        action_values.append(
            _oriented_strength(
                "action_channel",
                _action_channel_bias(positions, action_delta, mass_node_probs, probe_layers, center_y) / width_ref,
            )
        )
        flow_values.append(
            _oriented_strength(
                "packet_flow_action",
                _packet_flow_action_bias(
                    positions=positions,
                    adj=adj,
                    field=mass_field,
                    amps=mass_amps,
                    action_delta=action_delta,
                    source_layers=source_layers,
                    probe_layers=probe_layers,
                    center_y=center_y,
                    k=k,
                    retain_share=retain_share,
                    angle_beta=angle_beta,
                ) / width_ref,
            )
        )
        visibility_values.append(_visibility_guardrail(free_probs, positions))

    if not action_values or not flow_values:
        return None

    action_strength = statistics.fmean(action_values)
    flow_strength = statistics.fmean(flow_values)
    return TrialRow(
        family=family.label,
        n_layers=n_layers,
        target_b=target_b,
        seed=seed,
        actual_b=actual_b,
        mass_span=mass_span,
        edge_b=edge_b,
        action_strength=action_strength,
        flow_strength=flow_strength,
        action_over_b=_safe_ratio(action_strength, actual_b),
        action_over_edge_b=action_strength / edge_b if edge_b >= EDGE_B_MIN else float("nan"),
        flow_over_b=_safe_ratio(flow_strength, actual_b),
        flow_over_edge_b=flow_strength / edge_b if edge_b >= EDGE_B_MIN else float("nan"),
        visibility_guardrail=statistics.fmean(visibility_values),
    )


def _trend_summary(rows: list[TrialRow], field: str) -> TrendSummary | None:
    grouped: dict[float, list[TrialRow]] = defaultdict(list)
    for row in rows:
        grouped[row.target_b].append(row)

    pairs = []
    for target_b in sorted(grouped):
        sample = grouped[target_b]
        values = [getattr(entry, field) for entry in sample]
        values = [value for value in values if not math.isnan(value)]
        if values:
            pairs.append(
                (
                    statistics.fmean(entry.actual_b for entry in sample),
                    statistics.fmean(values),
                )
            )

    if len(pairs) < 2:
        return None

    xs = [pair[0] for pair in pairs]
    ys = [pair[1] for pair in pairs]
    slope = _linear_slope(xs, ys)
    start = ys[0]
    end = ys[-1]
    status = "PASS" if slope < -NEGATIVE_SLOPE_EPS and end < start else "FAIL"
    return TrendSummary(start=start, end=end, slope=slope, status=status)


def _mean_text(values: list[float], width: int = 9, decimals: int = 4) -> str:
    valid = [value for value in values if not math.isnan(value)]
    if not valid:
        return f"{'n/a':>{width}s}"
    return format(statistics.fmean(valid), f"+{width}.{decimals}f")


def _print_trend_block(rows: list[TrialRow]) -> dict[str, TrendSummary | None]:
    summaries = {
        "A/b": _trend_summary(rows, "action_over_b"),
        "A/edge": _trend_summary(rows, "action_over_edge_b"),
        "F/b": _trend_summary(rows, "flow_over_b"),
        "F/edge": _trend_summary(rows, "flow_over_edge_b"),
    }
    print("Trend summary (desired: normalized attraction density decreases as actual b increases):")
    for label, summary in summaries.items():
        if summary is None:
            print(f"  {label:>6s}: INSUF")
            continue
        print(
            f"  {label:>6s}: {summary.status} "
            f"({summary.start:+.4f} -> {summary.end:+.4f}, slope {summary.slope:+.4f})"
        )
    return summaries


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

    families = [BASELINE_FAMILY, HOLDOUT_FAMILY]
    tasks = [
        (family, n_layers, target_b, seed, args.angle_beta, args.retain_share, args.mass_nodes)
        for family in families
        for n_layers in args.n_layers
        for target_b in args.impact_bs
        for seed in range(args.seeds)
    ]

    ctx = mp.get_context("fork")
    if args.workers <= 1:
        rows = [_evaluate_trial(task) for task in tasks]
    else:
        try:
            with ProcessPoolExecutor(max_workers=args.workers, mp_context=ctx) as pool:
                rows = list(pool.map(_evaluate_trial, tasks))
        except (OSError, PermissionError):
            rows = [_evaluate_trial(task) for task in tasks]
    rows = [row for row in rows if row is not None]

    print("=" * 120)
    print("DIRECTIONAL-MEASURE B GEOMETRY-NORMALIZED HOLDOUT TRANSFER")
    print("=" * 120)
    print(
        "Transport fixed to exp(i k S_spent) / L^p x exp(-beta * theta^2); "
        f"beta={args.angle_beta:.3f}, seeds={args.seeds}, mass_nodes={args.mass_nodes}"
    )
    print("The readout family is unchanged: action_channel and packet_flow_action near the mass side.")
    print("This asks whether the retained center-offset and nearest-edge response densities transfer")
    print("from the original dense random-DAG family to the second dense-family holdout.")
    print()

    family_rollup: dict[tuple[str, int], dict[str, TrendSummary | None]] = {}
    for family in families:
        print(f"FAMILY: {family.label}")
        print("-" * 120)
        for n_layers in args.n_layers:
            bucket = [row for row in rows if row.family == family.label and row.n_layers == n_layers]
            if not bucket:
                continue

            grouped: dict[float, list[TrialRow]] = defaultdict(list)
            for row in bucket:
                grouped[row.target_b].append(row)

            print(f"N={n_layers}")
            print(
                f"{'target_b':>8s} {'actual_b':>8s} {'span':>8s} {'edge_b':>8s} "
                f"{'A_raw':>9s} {'F_raw':>9s} {'A/b':>9s} {'A/edge':>9s} {'F/b':>9s} {'F/edge':>9s}"
            )
            print("-" * 104)
            for target_b in sorted(grouped):
                sample = grouped[target_b]
                print(
                    f"{target_b:8.2f} "
                    f"{statistics.fmean(row.actual_b for row in sample):8.3f} "
                    f"{statistics.fmean(row.mass_span for row in sample):8.3f} "
                    f"{statistics.fmean(row.edge_b for row in sample):8.3f} "
                    f"{_mean_text([row.action_strength for row in sample])} "
                    f"{_mean_text([row.flow_strength for row in sample])} "
                    f"{_mean_text([row.action_over_b for row in sample])} "
                    f"{_mean_text([row.action_over_edge_b for row in sample])} "
                    f"{_mean_text([row.flow_over_b for row in sample])} "
                    f"{_mean_text([row.flow_over_edge_b for row in sample])}"
                )
            summaries = _print_trend_block(bucket)
            family_rollup[(family.label, n_layers)] = summaries
            print()

    print("Transfer reading:")
    print("  1. Raw action-style strengths can still grow with b; the question here is the normalized density trend.")
    print("  2. A retained transfer pass means each family separately keeps a decreasing trend with actual b.")
    for n_layers in args.n_layers:
        baseline = family_rollup.get((BASELINE_FAMILY.label, n_layers), {})
        holdout = family_rollup.get((HOLDOUT_FAMILY.label, n_layers), {})
        shared_passes = []
        for label in ("A/b", "A/edge", "F/b", "F/edge"):
            left = baseline.get(label)
            right = holdout.get(label)
            if left is not None and right is not None and left.status == "PASS" and right.status == "PASS":
                shared_passes.append(label)
        if shared_passes:
            joined = ", ".join(shared_passes)
        else:
            joined = "none"
        print(f"  3. N={n_layers}: shared family-local passes -> {joined}")
    print("  4. If nearest-edge density transfers while center-offset density stays cleaner,")
    print("     that keeps the existing hierarchy intact: b is the asymptotic leading term and")
    print("     b - h_mass is the safer finite-source correction.")


if __name__ == "__main__":
    main()
