#!/usr/bin/env python3
"""Test the directional b denominator hierarchy on the branching-tree control.

This is the first second-family check after the random-DAG asymptotic bridge
card.  It keeps the corrected directional transport fixed and asks whether the
same bounded hierarchy survives on the minimal-path branching-tree family:

    b
    b - h_mass
    b - (h_mass + delta_packet)

where ``h_mass`` is the mass half-span and ``delta_packet`` is the retained
free probe-band edge.
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

from scripts.directional_b_geometry_normalized_compare import EDGE_B_MIN, EPS  # noqa: E402
from scripts.directional_b_readout_compare import (  # noqa: E402
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
from scripts.directional_b_support_distance_compare import (  # noqa: E402
    SUPPORT_GAP_MIN,
    _interval_gap,
    _retained_probe_band,
)
from scripts.gravity_observable_readout_scaling_compare import _action_channel_bias, _visibility_guardrail  # noqa: E402
from scripts.gravity_packet_local_action_flow_transfer_compare import _packet_flow_action_bias  # noqa: E402
from scripts.scaling_testbench import build_branching_tree  # noqa: E402


DEFAULT_TREE_SIZES = (8, 10, 12)
DEFAULT_IMPACT_BS = (1.0, 2.0, 3.0, 4.0, 5.0)


@dataclass(frozen=True)
class TrialRow:
    n_layers: int
    target_b: float
    actual_b: float
    mass_span: float
    mass_half_span: float
    edge_b: float
    support_gap: float
    band_high_rel: float
    action_over_b: float
    action_over_edge_b: float
    action_over_support_gap: float
    flow_over_b: float
    flow_over_edge_b: float
    flow_over_support_gap: float
    visibility_guardrail: float


def _evaluate_tree_trial(task: tuple[int, float, float, int, int, float]) -> TrialRow | None:
    n_layers, target_b, angle_beta, branching_factor, mass_nodes, retain_share = task

    positions, adj, layer_indices = build_branching_tree(
        n_layers,
        branching_factor=branching_factor,
        y_range=10.0,
    )
    layers = list(range(len(layer_indices)))
    if len(layers) < 5:
        return None

    by_layer = {layer: nodes for layer, nodes in enumerate(layer_indices)}
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
    mass_half_span = 0.5 * mass_span
    edge_b = max(actual_b - mass_half_span, EPS)

    n = len(positions)
    free_field = [0.0] * n
    # Same simple seeded field construction used on the tree control elsewhere.
    from scripts.scaling_testbench import compute_field_simple  # local import to avoid broad dependency at import time
    mass_field = compute_field_simple(positions, adj, grav_mass)

    source_layers = {layers[mid - 1], layers[mid]} if mid > 0 else {layers[mid]}
    probe_layers = {layers[mid], layers[min(mid + 1, len(layers) - 1)]}
    probe_nodes = [node for node in range(n) if round(positions[node][0]) in probe_layers]

    free_action_mean = _propagate_action_means(positions, adj, free_field, src, angle_beta=angle_beta)
    mass_action_mean = _propagate_action_means(positions, adj, mass_field, src, angle_beta=angle_beta)
    action_delta = {
        node: mass_action_mean.get(node, 0.0) - free_action_mean.get(node, 0.0)
        for node in range(n)
    }

    action_values: list[float] = []
    flow_values: list[float] = []
    visibility_values: list[float] = []
    probe_weights: dict[int, float] = defaultdict(float)
    valid_k = 0

    for k in K_BAND:
        free_amps = _propagate_node_amplitudes(positions, adj, free_field, src, k, angle_beta=angle_beta)
        mass_amps = _propagate_node_amplitudes(positions, adj, mass_field, src, k, angle_beta=angle_beta)
        free_probs = _detector_probs(free_amps, det)
        mass_probs = _detector_probs(mass_amps, det)
        width_ref = _beam_width(free_probs, positions)
        if width_ref <= 1e-30:
            continue

        node_probs = _node_probs(free_amps)
        for node in probe_nodes:
            probe_weights[node] += node_probs.get(node, 0.0)

        mass_node_probs = _node_probs(mass_amps)
        action_values.append(
            _action_channel_bias(positions, action_delta, mass_node_probs, probe_layers, center_y) / width_ref
        )
        flow_values.append(
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
            )
            / width_ref
        )
        visibility_values.append(_visibility_guardrail(free_probs, positions))
        valid_k += 1

    if valid_k <= 0:
        return None

    for node in list(probe_weights):
        probe_weights[node] /= valid_k

    band = _retained_probe_band(positions, probe_weights, probe_nodes, retain_share)
    if band is None:
        return None
    band_low, band_high = band
    support_gap = _interval_gap(min(mass_ys), max(mass_ys), band_low, band_high)
    band_high_rel = band_high - center_y

    action_strength = _oriented_strength("action_channel", statistics.fmean(action_values))
    flow_strength = _oriented_strength("packet_flow_action", statistics.fmean(flow_values))

    return TrialRow(
        n_layers=n_layers,
        target_b=target_b,
        actual_b=actual_b,
        mass_span=mass_span,
        mass_half_span=mass_half_span,
        edge_b=edge_b,
        support_gap=support_gap,
        band_high_rel=band_high_rel,
        action_over_b=action_strength / max(actual_b, EPS),
        action_over_edge_b=action_strength / edge_b if edge_b >= EDGE_B_MIN else float("nan"),
        action_over_support_gap=action_strength / support_gap if support_gap >= SUPPORT_GAP_MIN else float("nan"),
        flow_over_b=flow_strength / max(actual_b, EPS),
        flow_over_edge_b=flow_strength / edge_b if edge_b >= EDGE_B_MIN else float("nan"),
        flow_over_support_gap=flow_strength / support_gap if support_gap >= SUPPORT_GAP_MIN else float("nan"),
        visibility_guardrail=statistics.fmean(visibility_values),
    )


def _metric_summary(rows: list[TrialRow], metric: str) -> tuple[str, float, float, float] | None:
    grouped: dict[float, list[TrialRow]] = defaultdict(list)
    for row in rows:
        grouped[row.target_b].append(row)

    pairs = []
    for target_b in sorted(grouped):
        values = [getattr(entry, metric) for entry in grouped[target_b]]
        values = [value for value in values if not math.isnan(value)]
        if values:
            pairs.append((statistics.fmean(entry.actual_b for entry in grouped[target_b]), statistics.fmean(values)))
    if len(pairs) < 2:
        return None

    xs = [pair[0] for pair in pairs]
    ys = [pair[1] for pair in pairs]
    slope = _linear_slope(xs, ys)
    start = ys[0]
    end = ys[-1]
    status = "PASS" if slope < -NEGATIVE_SLOPE_EPS and end < start else "FAIL"
    return status, start, end, slope


def _print_trend_summary(rows: list[TrialRow], metric_names: list[str]) -> dict[str, str]:
    verdicts: dict[str, str] = {}
    print("Trend summary (desired: normalized attraction density decreases as actual b increases):")
    for metric in metric_names:
        summary = _metric_summary(rows, metric)
        if summary is None:
            verdicts[metric] = "INSUF"
            print(f"  {metric:>23s}: INSUF (too few non-singular points)")
            continue
        status, start, end, slope = summary
        verdicts[metric] = status
        print(
            f"  {metric:>23s}: {status} "
            f"(strength {start:+.4f} -> {end:+.4f}, slope {slope:+.4f})"
        )
    return verdicts


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workers", type=int, default=min(8, max(1, os.cpu_count() or 1)))
    parser.add_argument("--n-layers", nargs="+", type=int, default=list(DEFAULT_TREE_SIZES))
    parser.add_argument("--impact-bs", nargs="+", type=float, default=list(DEFAULT_IMPACT_BS))
    parser.add_argument("--angle-beta", type=float, default=0.8)
    parser.add_argument("--branching-factor", type=int, default=2)
    parser.add_argument("--mass-nodes", type=int, default=2)
    parser.add_argument("--retain-share", type=float, default=0.5)
    args = parser.parse_args()

    tasks = [
        (n_layers, target_b, args.angle_beta, args.branching_factor, args.mass_nodes, args.retain_share)
        for n_layers in args.n_layers
        for target_b in args.impact_bs
    ]

    ctx = mp.get_context("fork")
    if args.workers <= 1:
        rows = [_evaluate_tree_trial(task) for task in tasks]
    else:
        try:
            with ProcessPoolExecutor(max_workers=args.workers, mp_context=ctx) as pool:
                rows = list(pool.map(_evaluate_tree_trial, tasks))
        except (OSError, PermissionError):
            rows = [_evaluate_tree_trial(task) for task in tasks]
    rows = [row for row in rows if row is not None]

    metric_names = [
        "action_over_b",
        "action_over_edge_b",
        "action_over_support_gap",
        "flow_over_b",
        "flow_over_edge_b",
        "flow_over_support_gap",
    ]
    family_verdicts: dict[int, dict[str, str]] = {}

    print("=" * 112)
    print("DIRECTIONAL-MEASURE B TREE HIERARCHY COMPARE")
    print("=" * 112)
    print(
        "Second-family check on the branching-tree control with corrected directional transport fixed; "
        f"beta={args.angle_beta:.3f}, bf={args.branching_factor}, mass_nodes={args.mass_nodes}"
    )
    print("Hierarchy under test: b, b - h_mass, b - (h_mass + delta_packet)")
    print()

    for n_layers in args.n_layers:
        bucket = [row for row in rows if row.n_layers == n_layers]
        if not bucket:
            continue
        grouped: dict[float, list[TrialRow]] = defaultdict(list)
        for row in bucket:
            grouped[row.target_b].append(row)

        def render(value: float) -> str:
            return f"{value:+9.4f}" if not math.isnan(value) else f"{'n/a':>9s}"

        print(f"N={n_layers}")
        print(
            f"{'target_b':>8s} {'actual_b':>8s} {'span':>8s} {'edge_b':>8s} {'supp_gap':>9s} {'band_hi':>9s} "
            f"{'A/b':>9s} {'A/edge':>9s} {'A/gap':>9s} {'F/b':>9s} {'F/edge':>9s} {'F/gap':>9s}"
        )
        print("-" * 120)
        for target_b in sorted(grouped):
            row = grouped[target_b][0]
            print(
                f"{target_b:8.2f} "
                f"{row.actual_b:8.3f} "
                f"{row.mass_span:8.3f} "
                f"{row.edge_b:8.3f} "
                f"{row.support_gap:9.3f} "
                f"{row.band_high_rel:+9.3f} "
                f"{render(row.action_over_b)} "
                f"{render(row.action_over_edge_b)} "
                f"{render(row.action_over_support_gap)} "
                f"{render(row.flow_over_b)} "
                f"{render(row.flow_over_edge_b)} "
                f"{render(row.flow_over_support_gap)}"
            )
        family_verdicts[n_layers] = _print_trend_summary(bucket, metric_names)
        print()

    print("Hierarchy verdict across tree sizes:")
    for metric in metric_names:
        counts = defaultdict(int)
        for verdicts in family_verdicts.values():
            counts[verdicts.get(metric, "INSUF")] += 1
        print(
            f"  {metric:>23s}: "
            f"PASS {counts['PASS']}/{len(family_verdicts)}, "
            f"FAIL {counts['FAIL']}/{len(family_verdicts)}, "
            f"INSUF {counts['INSUF']}/{len(family_verdicts)}"
        )

    print()
    print("Interpretation:")
    print("  If center-offset and edge-corrected densities survive on the tree control while support-gap does not,")
    print("  the current hierarchy transfers beyond the random-DAG family instead of being just one bounded fit.")


if __name__ == "__main__":
    main()
