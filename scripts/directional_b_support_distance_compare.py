#!/usr/bin/env python3
"""Compare local support-distance normalization on the directional b lane.

This bounded follow-on keeps the corrected directional transport fixed and
reuses the same generated-DAG family as the earlier impact-parameter compares.
The question here is narrower than in the geometry-normalized pass:

- center-offset density already passes
- nearest-edge density already passes

Can a more local denominator tied to the actual free packet support do at least
as well?  We define a support-distance gap as the nearest vertical separation
between the mass-cluster interval and the free packet's retained probe-layer
support band, then compare:

- action_channel / support_gap
- packet_flow_action / support_gap

against the previously retained center-offset and nearest-edge densities.
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

from scripts.directional_b_geometry_normalized_compare import (  # noqa: E402
    EDGE_B_MIN,
    EPS,
)
from scripts.directional_b_readout_compare import (  # noqa: E402
    DEFAULT_IMPACT_BS,
    DEFAULT_N_LAYERS,
    K_BAND,
    NEGATIVE_SLOPE_EPS,
    _beam_width,
    _detector_probs,
    _evaluate_trial,
    _linear_slope,
    _node_probs,
    _oriented_strength,
    _propagate_node_amplitudes,
    _select_mass_nodes,
)
from scripts.generative_causal_dag_interference import generate_causal_dag  # noqa: E402


SUPPORT_GAP_MIN = 0.5


def _safe_center_ratio(strength: float, actual_b: float) -> float:
    return strength / actual_b if actual_b > 0.0 else float("nan")


@dataclass(frozen=True)
class TrialRow:
    n_layers: int
    target_b: float
    seed: int
    actual_b: float
    mass_span: float
    edge_b: float
    support_gap: float
    action_channel: float
    packet_flow_action: float
    action_over_b: float
    action_over_edge_b: float
    action_over_support_gap: float
    flow_over_b: float
    flow_over_edge_b: float
    flow_over_support_gap: float
    visibility_guardrail: float


def _interval_gap(a_low: float, a_high: float, b_low: float, b_high: float) -> float:
    if a_high < b_low:
        return b_low - a_high
    if b_high < a_low:
        return a_low - b_high
    return 0.0


def _retained_probe_band(
    positions: list[tuple[float, float]],
    node_weights: dict[int, float],
    probe_nodes: list[int],
    retain_share: float,
) -> tuple[float, float] | None:
    weighted = [(node, node_weights.get(node, 0.0)) for node in probe_nodes]
    weighted = [(node, weight) for node, weight in weighted if weight > 1e-30]
    if not weighted:
        return None

    peak_node = max(weighted, key=lambda item: item[1])[0]
    peak_y = positions[peak_node][1]
    total_weight = sum(weight for _node, weight in weighted)
    target = max(1e-30, retain_share * total_weight)
    ordered = sorted(
        weighted,
        key=lambda item: (abs(positions[item[0]][1] - peak_y), -item[1], item[0]),
    )

    kept: list[int] = []
    carried = 0.0
    for node, weight in ordered:
        kept.append(node)
        carried += weight
        if carried >= target:
            break

    ys = [positions[node][1] for node in kept]
    return min(ys), max(ys)


def _support_geometry(
    task: tuple[int, float, int, float, float, int],
) -> tuple[float, float, float]:
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
    mass_ys = [positions[node][1] for node in grav_mass]
    mass_low = min(mass_ys)
    mass_high = max(mass_ys)
    mass_span = mass_high - mass_low
    actual_b = statistics.fmean(mass_ys) - center_y
    edge_b = max(actual_b - 0.5 * mass_span, EPS)

    src = by_layer[layers[0]]
    det = set(by_layer[layers[-1]])
    probe_layers = {layers[mid], layers[min(mid + 1, len(layers) - 1)]}
    probe_nodes = [node for node in range(len(positions)) if round(positions[node][0]) in probe_layers]

    probe_weights: dict[int, float] = defaultdict(float)
    valid_k = 0
    for k in K_BAND:
        free_amps = _propagate_node_amplitudes(positions, adj, [0.0] * len(positions), src, k, angle_beta=angle_beta)
        free_probs = _detector_probs(free_amps, det)
        width_ref = _beam_width(free_probs, positions)
        if width_ref <= 1e-30:
            continue
        node_probs = _node_probs(free_amps)
        for node in probe_nodes:
            probe_weights[node] += node_probs.get(node, 0.0)
        valid_k += 1

    if valid_k <= 0:
        return actual_b, mass_span, 0.0
    for node in list(probe_weights):
        probe_weights[node] /= valid_k

    band = _retained_probe_band(positions, probe_weights, probe_nodes, retain_share)
    if band is None:
        support_gap = 0.0
    else:
        support_gap = _interval_gap(mass_low, mass_high, band[0], band[1])

    return actual_b, mass_span, support_gap


def _evaluate_support_trial(task: tuple[int, float, int, float, float, int]) -> TrialRow | None:
    base_row = _evaluate_trial(task)
    if base_row is None:
        return None

    actual_b, mass_span, support_gap = _support_geometry(task)
    edge_b = max(actual_b - 0.5 * mass_span, EPS)
    action_strength = _oriented_strength("action_channel", base_row.action_channel)
    flow_strength = _oriented_strength("packet_flow_action", base_row.packet_flow_action)

    return TrialRow(
        n_layers=base_row.n_layers,
        target_b=base_row.target_b,
        seed=base_row.seed,
        actual_b=actual_b,
        mass_span=mass_span,
        edge_b=edge_b,
        support_gap=support_gap,
        action_channel=base_row.action_channel,
        packet_flow_action=base_row.packet_flow_action,
        action_over_b=_safe_center_ratio(action_strength, actual_b),
        action_over_edge_b=action_strength / edge_b if edge_b >= EDGE_B_MIN else float("nan"),
        action_over_support_gap=(
            action_strength / support_gap if support_gap >= SUPPORT_GAP_MIN else float("nan")
        ),
        flow_over_b=_safe_center_ratio(flow_strength, actual_b),
        flow_over_edge_b=flow_strength / edge_b if edge_b >= EDGE_B_MIN else float("nan"),
        flow_over_support_gap=(
            flow_strength / support_gap if support_gap >= SUPPORT_GAP_MIN else float("nan")
        ),
        visibility_guardrail=base_row.visibility_guardrail,
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


def _print_trend_summary(rows: list[TrialRow], metric_names: list[str]) -> None:
    print("Trend summary (desired: normalized attraction density decreases as actual b increases):")
    for metric in metric_names:
        summary = _metric_summary(rows, metric)
        if summary is None:
            print(f"  {metric:>23s}: INSUF (too few non-singular points)")
            continue
        status, start, end, slope = summary
        print(
            f"  {metric:>23s}: {status} "
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
        rows = [_evaluate_support_trial(task) for task in tasks]
    else:
        try:
            with ProcessPoolExecutor(max_workers=args.workers, mp_context=ctx) as pool:
                rows = list(pool.map(_evaluate_support_trial, tasks))
        except (OSError, PermissionError):
            rows = [_evaluate_support_trial(task) for task in tasks]
    rows = [row for row in rows if row is not None]

    metric_names = [
        "action_over_b",
        "action_over_edge_b",
        "action_over_support_gap",
        "flow_over_b",
        "flow_over_edge_b",
        "flow_over_support_gap",
    ]

    print("=" * 112)
    print("DIRECTIONAL-MEASURE B SUPPORT-DISTANCE COMPARE")
    print("=" * 112)
    print(
        "Transport fixed to exp(i k S_spent) / L^p x exp(-beta * theta^2); "
        f"beta={args.angle_beta:.3f}, seeds={args.seeds}, retain_share={args.retain_share:.2f}"
    )
    print("Support gap = nearest vertical separation between the mass interval and the free packet's retained probe band.")
    print(f"Nearest-edge and support-gap densities are reported only when the denominator >= {SUPPORT_GAP_MIN:.1f}.")
    print()

    for n_layers in args.n_layers:
        bucket = [row for row in rows if row.n_layers == n_layers]
        if not bucket:
            continue
        grouped: dict[float, list[TrialRow]] = defaultdict(list)
        for row in bucket:
            grouped[row.target_b].append(row)

        def render_mean(values: list[float]) -> str:
            values = [value for value in values if not math.isnan(value)]
            return f"{statistics.fmean(values):+9.4f}" if values else f"{'n/a':>9s}"

        print(f"N={n_layers}")
        print(
            f"{'target_b':>8s} {'actual_b':>8s} {'span':>8s} {'edge_b':>8s} {'supp_gap':>9s} "
            f"{'A/b':>9s} {'A/edge':>9s} {'A/gap':>9s} {'F/b':>9s} {'F/edge':>9s} {'F/gap':>9s}"
        )
        print("-" * 112)
        for target_b in sorted(grouped):
            sample = grouped[target_b]
            print(
                f"{target_b:8.2f} "
                f"{statistics.fmean(row.actual_b for row in sample):8.3f} "
                f"{statistics.fmean(row.mass_span for row in sample):8.3f} "
                f"{statistics.fmean(row.edge_b for row in sample):8.3f} "
                f"{statistics.fmean(row.support_gap for row in sample):9.3f} "
                f"{statistics.fmean(row.action_over_b for row in sample):+9.4f} "
                f"{render_mean([row.action_over_edge_b for row in sample])} "
                f"{render_mean([row.action_over_support_gap for row in sample])} "
                f"{statistics.fmean(row.flow_over_b for row in sample):+9.4f} "
                f"{render_mean([row.flow_over_edge_b for row in sample])} "
                f"{render_mean([row.flow_over_support_gap for row in sample])}"
            )
        _print_trend_summary(bucket, metric_names)
        print()

    print("Interpretation:")
    print("  If support-gap density survives the same bounded trend test, it is a stronger candidate than")
    print("  center or edge offset because its denominator is tied to the free packet's actual local support.")


if __name__ == "__main__":
    main()
