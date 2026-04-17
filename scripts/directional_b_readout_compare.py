#!/usr/bin/env python3
"""Compare bounded impact-parameter readouts under the directional path measure.

This keeps the retained unitary transport fixed as:

    exp(i k S_spent) / L^p × exp(-beta * theta^2)

and changes only the gravity readout. The question is whether any current
readout yields a more physical impact-parameter trend on the generated-DAG
family, where the target is that attraction strength should decrease as the
mass region moves farther off-axis.

Compared readouts:
- detector centroid shift
- detector channel shift
- near-mass packet-current bias
- near-mass action_channel
- packet_action_channel
- packet_flow_action
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

from scripts.generative_causal_dag_interference import generate_causal_dag  # noqa: E402
from scripts.gravity_observable_readout_scaling_compare import (  # noqa: E402
    K_BAND,
    _action_channel_bias,
    _beam_width,
    _detector_channel_shift,
    _detector_probs,
    _node_probs,
    _packet_current_bias,
    _propagate_action_means,
    _propagate_node_amplitudes,
    _visibility_guardrail,
)
from scripts.gravity_packet_local_action_flow_transfer_compare import (  # noqa: E402
    _packet_action_channel_bias,
    _packet_flow_action_bias,
)
from scripts.two_register_decoherence import compute_field, centroid_y  # noqa: E402


DEFAULT_N_LAYERS = (12, 25)
DEFAULT_IMPACT_BS = (1.5, 3.0, 4.5, 6.0, 7.5)
ACTION_LIKE_METRICS = {"action_channel", "packet_action_channel", "packet_flow_action"}
NEGATIVE_SLOPE_EPS = 1e-3


@dataclass(frozen=True)
class TrialRow:
    n_layers: int
    target_b: float
    seed: int
    actual_b: float
    detector_centroid: float
    detector_channel: float
    packet_current: float
    action_channel: float
    packet_action_channel: float
    packet_flow_action: float
    visibility_guardrail: float


def _select_mass_nodes(
    positions: list[tuple[float, float]],
    layer_nodes: list[int],
    center_y: float,
    target_b: float,
    mass_nodes: int,
) -> list[int]:
    target_y = center_y + target_b
    ordered = sorted(
        layer_nodes,
        key=lambda node: (abs(positions[node][1] - target_y), positions[node][1]),
    )
    return ordered[:mass_nodes]


def _evaluate_trial(task: tuple[int, float, int, float, float, int]) -> TrialRow | None:
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

    actual_b = statistics.fmean(positions[node][1] for node in grav_mass) - center_y
    n = len(positions)
    free_field = [0.0] * n
    mass_field = compute_field(positions, adj, grav_mass)
    source_layers = {layers[mid - 1], layers[mid]} if mid > 0 else {layers[mid]}
    probe_layers = {layers[mid], layers[min(mid + 1, len(layers) - 1)]}

    free_action_mean = _propagate_action_means(positions, adj, free_field, src, angle_beta=angle_beta)
    mass_action_mean = _propagate_action_means(positions, adj, mass_field, src, angle_beta=angle_beta)
    action_delta = {node: mass_action_mean.get(node, 0.0) - free_action_mean.get(node, 0.0) for node in range(n)}

    detector_centroid_values: list[float] = []
    detector_channel_values: list[float] = []
    packet_current_values: list[float] = []
    action_channel_values: list[float] = []
    packet_action_values: list[float] = []
    packet_flow_values: list[float] = []
    visibility_values: list[float] = []

    for k in K_BAND:
        free_amps = _propagate_node_amplitudes(positions, adj, free_field, src, k, angle_beta=angle_beta)
        mass_amps = _propagate_node_amplitudes(positions, adj, mass_field, src, k, angle_beta=angle_beta)

        free_probs = _detector_probs(free_amps, det)
        mass_probs = _detector_probs(mass_amps, det)
        mass_node_probs = _node_probs(mass_amps)
        width_ref = _beam_width(free_probs, positions)

        detector_centroid_values.append((centroid_y(mass_probs, positions) - centroid_y(free_probs, positions)) / width_ref)
        detector_channel_values.append(
            (_detector_channel_shift(mass_probs, positions) - _detector_channel_shift(free_probs, positions)) / width_ref
        )
        packet_current_values.append(
            (_packet_current_bias(positions, adj, mass_field, mass_amps, source_layers, angle_beta=angle_beta) -
             _packet_current_bias(positions, adj, free_field, free_amps, source_layers, angle_beta=angle_beta)) / width_ref
        )
        action_channel_values.append(
            _action_channel_bias(positions, action_delta, mass_node_probs, probe_layers, center_y) / width_ref
        )
        packet_action_values.append(
            _packet_action_channel_bias(
                positions,
                action_delta,
                mass_node_probs,
                probe_layers,
                center_y,
                retain_share,
            ) / width_ref
        )
        packet_flow_values.append(
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
            ) / width_ref
        )
        visibility_values.append(_visibility_guardrail(free_probs, positions))

    return TrialRow(
        n_layers=n_layers,
        target_b=target_b,
        seed=seed,
        actual_b=actual_b,
        detector_centroid=statistics.fmean(detector_centroid_values),
        detector_channel=statistics.fmean(detector_channel_values),
        packet_current=statistics.fmean(packet_current_values),
        action_channel=statistics.fmean(action_channel_values),
        packet_action_channel=statistics.fmean(packet_action_values),
        packet_flow_action=statistics.fmean(packet_flow_values),
        visibility_guardrail=statistics.fmean(visibility_values),
    )


def _linear_slope(xs: list[float], ys: list[float]) -> float:
    if len(xs) < 2:
        return 0.0
    mean_x = statistics.fmean(xs)
    mean_y = statistics.fmean(ys)
    cov = sum((x - mean_x) * (y - mean_y) for x, y in zip(xs, ys))
    var = sum((x - mean_x) ** 2 for x in xs)
    return cov / var if var > 1e-30 else 0.0


def _oriented_strength(metric: str, value: float) -> float:
    return -value if metric in ACTION_LIKE_METRICS else value


def _print_trend_summary(rows: list[TrialRow], metric_names: list[str]) -> None:
    grouped: dict[float, list[TrialRow]] = defaultdict(list)
    for row in rows:
        grouped[row.target_b].append(row)

    actual_bs = [statistics.fmean(entry.actual_b for entry in grouped[target_b]) for target_b in sorted(grouped)]
    print("Trend summary (desired: attraction strength decreases as actual b increases):")
    for metric in metric_names:
        strengths = [
            statistics.fmean(_oriented_strength(metric, getattr(entry, metric)) for entry in grouped[target_b])
            for target_b in sorted(grouped)
        ]
        slope = _linear_slope(actual_bs, strengths)
        start = strengths[0]
        end = strengths[-1]
        status = "PASS" if slope < -NEGATIVE_SLOPE_EPS and end < start else "FAIL"
        print(
            f"  {metric:>21s}: {status} "
            f"(strength {start:+.4f} -> {end:+.4f}, slope {slope:+.4f})"
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
        rows = [_evaluate_trial(task) for task in tasks]
    else:
        try:
            with ProcessPoolExecutor(max_workers=args.workers, mp_context=ctx) as pool:
                rows = list(pool.map(_evaluate_trial, tasks))
        except (OSError, PermissionError):
            rows = [_evaluate_trial(task) for task in tasks]
    rows = [row for row in rows if row is not None]

    metric_names = [
        "detector_centroid",
        "detector_channel",
        "packet_current",
        "action_channel",
        "packet_action_channel",
        "packet_flow_action",
    ]

    print("=" * 104)
    print("DIRECTIONAL-MEASURE B-READOUT COMPARE")
    print("=" * 104)
    print(
        "Transport fixed to exp(i k S_spent) / L^p × exp(-beta * theta^2); "
        f"beta={args.angle_beta:.3f}, seeds={args.seeds}, k_band={K_BAND}, retain_share={args.retain_share:.2f}"
    )
    print("Mass region is chosen by nearest mid-layer nodes to the target impact parameter.")
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
            f"{'target_b':>8s} {'actual_b':>8s} {'n':>3s} {'R_det':>9s} {'R_chan':>9s} "
            f"{'R_curr':>9s} {'R_act':>9s} {'R_pact':>9s} {'R_pflow':>9s} {'V_free':>8s}"
        )
        print("-" * 95)
        for target_b in sorted(grouped):
            sample = grouped[target_b]
            print(
                f"{target_b:8.2f} "
                f"{statistics.fmean(row.actual_b for row in sample):8.3f} "
                f"{len(sample):3d} "
                f"{statistics.fmean(row.detector_centroid for row in sample):+9.4f} "
                f"{statistics.fmean(row.detector_channel for row in sample):+9.4f} "
                f"{statistics.fmean(row.packet_current for row in sample):+9.4f} "
                f"{statistics.fmean(row.action_channel for row in sample):+9.4f} "
                f"{statistics.fmean(row.packet_action_channel for row in sample):+9.4f} "
                f"{statistics.fmean(row.packet_flow_action for row in sample):+9.4f} "
                f"{statistics.fmean(row.visibility_guardrail for row in sample):8.4f}"
            )
        _print_trend_summary(bucket, metric_names)
        print()

    print("Interpretation:")
    print("  A PASS would require a negative slope in attraction strength versus actual impact parameter.")
    print("  Detector-side observables read attraction directly; action-style observables are sign-flipped internally")
    print("  so a more negative raw action contrast counts as a stronger attraction readout.")


if __name__ == "__main__":
    main()
