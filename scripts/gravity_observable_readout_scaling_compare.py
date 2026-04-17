#!/usr/bin/env python3
"""Compare readout-only gravity observables on the retained scaling testbench.

This script keeps the corrected microscopic propagator fixed and changes only
the extracted gravity observable. The goal is to test whether a mesoscopic
readout can avoid the `N=12 -> N=25` response collapse without changing the
unitary transport law.

Compared readouts:
- detector centroid shift (current baseline)
- detector channel shift (coarse detector bins only)
- near-mass packet-current bias (local vertical flow proxy)
- near-mass action-channel bias (local cumulative action-deficit proxy)
"""

from __future__ import annotations

from concurrent.futures import ProcessPoolExecutor
from collections import defaultdict, deque
from dataclasses import dataclass
import argparse
import cmath
import math
import multiprocessing as mp
import os
import statistics
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.generative_causal_dag_interference import generate_causal_dag  # noqa: E402
from scripts.two_register_decoherence import compute_field, centroid_y  # noqa: E402


K_BAND = (3.0, 5.0, 7.0)
N_LAYERS = (8, 12, 15, 20, 25)


@dataclass(frozen=True)
class TrialRow:
    n_layers: int
    seed: int
    detector_centroid: float
    detector_channel: float
    packet_current: float
    action_channel: float
    width: float
    visibility_guardrail: float


def _topological_order(adj: dict[int, list[int]], n: int) -> list[int]:
    in_deg = [0] * n
    for i, nbs in adj.items():
        for j in nbs:
            in_deg[j] += 1
    q = deque(i for i in range(n) if in_deg[i] == 0)
    order: list[int] = []
    while q:
        i = q.popleft()
        order.append(i)
        for j in adj.get(i, []):
            in_deg[j] -= 1
            if in_deg[j] == 0:
                q.append(j)
    return order


def _edge_terms(
    positions: list[tuple[float, float]],
    field: list[float],
    i: int,
    j: int,
    k: float,
    angle_beta: float = 0.0,
) -> tuple[complex, float, float]:
    x1, y1 = positions[i]
    x2, y2 = positions[j]
    length = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    if length < 1e-10:
        return 0.0 + 0.0j, 0.0, 0.0
    local_field = 0.5 * (field[i] + field[j])
    delay = length * (1.0 + local_field)
    retained = math.sqrt(max(delay * delay - length * length, 0.0))
    action = delay - retained
    angle_weight = 1.0
    if angle_beta > 0.0:
        dx = x2 - x1
        dy = y2 - y1
        theta = math.atan2(abs(dy), max(dx, 1e-10))
        angle_weight = math.exp(-angle_beta * theta * theta)
    edge_amp = cmath.exp(1j * k * action) * angle_weight / (length ** 1.0)
    return edge_amp, action, length


def _propagate_node_amplitudes(
    positions: list[tuple[float, float]],
    adj: dict[int, list[int]],
    field: list[float],
    src: list[int],
    k: float,
    angle_beta: float = 0.0,
) -> list[complex]:
    n = len(positions)
    order = _topological_order(adj, n)
    amps = [0.0 + 0.0j] * n
    for s in src:
        amps[s] = 1.0 / len(src)
    for i in order:
        amp = amps[i]
        if abs(amp) < 1e-30:
            continue
        for j in adj.get(i, []):
            edge_amp, _, _ = _edge_terms(positions, field, i, j, k, angle_beta=angle_beta)
            if edge_amp == 0:
                continue
            amps[j] += amp * edge_amp
    return amps


def _propagate_action_means(
    positions: list[tuple[float, float]],
    adj: dict[int, list[int]],
    field: list[float],
    src: list[int],
    angle_beta: float = 0.0,
) -> dict[int, float]:
    n = len(positions)
    order = _topological_order(adj, n)
    weights = [0.0] * n
    action_sum = [0.0] * n
    for s in src:
        weights[s] = 1.0 / len(src)
    for i in order:
        w = weights[i]
        if w <= 1e-30:
            continue
        for j in adj.get(i, []):
            edge_amp, action, length = _edge_terms(positions, field, i, j, 1.0, angle_beta=angle_beta)
            if length == 0:
                continue
            atten = abs(edge_amp)
            next_weight = w * atten
            weights[j] += next_weight
            action_sum[j] += atten * (action_sum[i] + action * w)
    means: dict[int, float] = {}
    for i, w in enumerate(weights):
        means[i] = action_sum[i] / w if w > 1e-30 else 0.0
    return means


def _detector_probs(amps: list[complex], det: set[int]) -> dict[int, float]:
    probs = {d: abs(amps[d]) ** 2 for d in det}
    total = sum(probs.values())
    if total > 0:
        probs = {d: p / total for d, p in probs.items()}
    return probs


def _node_probs(amps: list[complex]) -> dict[int, float]:
    probs = {idx: abs(amp) ** 2 for idx, amp in enumerate(amps) if abs(amp) > 0.0}
    total = sum(probs.values())
    if total > 0:
        probs = {idx: p / total for idx, p in probs.items()}
    return probs


def _beam_width(probs: dict[int, float], positions: list[tuple[float, float]]) -> float:
    total = sum(probs.values())
    if total <= 1e-30:
        return 1.0
    mean = sum(positions[d][1] * p for d, p in probs.items()) / total
    second = sum((positions[d][1] ** 2) * p for d, p in probs.items()) / total
    var = max(0.0, second - mean * mean)
    return max(math.sqrt(var), 0.1)


def _visibility_guardrail(probs: dict[int, float], positions: list[tuple[float, float]]) -> float:
    by_y: dict[float, float] = defaultdict(float)
    for d, p in probs.items():
        by_y[positions[d][1]] += p
    ys = sorted(by_y)
    vals = [by_y[y] for y in ys]
    peaks = [vals[i] for i in range(1, len(vals) - 1) if vals[i] > vals[i - 1] and vals[i] > vals[i + 1]]
    troughs = [vals[i] for i in range(1, len(vals) - 1) if vals[i] < vals[i - 1] and vals[i] < vals[i + 1]]
    if peaks and troughs:
        top = max(peaks)
        bottom = min(troughs)
        denom = top + bottom
        if denom > 1e-30:
            return (top - bottom) / denom
    return 0.0


def _detector_channel_shift(
    probs: dict[int, float],
    positions: list[tuple[float, float]],
    n_bins: int = 8,
) -> float:
    ys = [positions[d][1] for d in probs]
    if not ys:
        return 0.0
    y_min = min(ys)
    y_max = max(ys)
    width = (y_max - y_min) / max(n_bins, 1) + 1e-10
    bin_probs: dict[int, float] = defaultdict(float)
    for d, p in probs.items():
        idx = min(int((positions[d][1] - y_min) / width), n_bins - 1)
        bin_probs[idx] += p
    return sum(idx * p for idx, p in bin_probs.items())


def _packet_current_bias(
    positions: list[tuple[float, float]],
    adj: dict[int, list[int]],
    field: list[float],
    amps: list[complex],
    source_layers: set[int],
    angle_beta: float = 0.0,
) -> float:
    numerator = 0.0
    denominator = 0.0
    by_layer = {idx: round(pos[0]) for idx, pos in enumerate(positions)}
    for i, nbs in adj.items():
        if by_layer[i] not in source_layers:
            continue
        amp_i = amps[i]
        if abs(amp_i) < 1e-30:
            continue
        for j in nbs:
            edge_amp, _, _ = _edge_terms(positions, field, i, j, 5.0, angle_beta=angle_beta)
            if edge_amp == 0:
                continue
            flow = abs(amp_i * edge_amp) ** 2
            dy = positions[j][1] - positions[i][1]
            numerator += flow * dy
            denominator += flow
    return numerator / denominator if denominator > 1e-30 else 0.0


def _action_channel_bias(
    positions: list[tuple[float, float]],
    action_delta: dict[int, float],
    mass_node_probs: dict[int, float],
    probe_layers: set[int],
    center_y: float,
) -> float:
    by_layer = {idx: round(pos[0]) for idx, pos in enumerate(positions)}
    upper_weights: list[float] = []
    upper_values: list[float] = []
    lower_weights: list[float] = []
    lower_values: list[float] = []
    for node, prob in mass_node_probs.items():
        if prob <= 1e-30 or by_layer[node] not in probe_layers:
            continue
        value = action_delta.get(node, 0.0)
        if positions[node][1] >= center_y:
            upper_weights.append(prob)
            upper_values.append(value)
        else:
            lower_weights.append(prob)
            lower_values.append(value)
    upper_total = sum(upper_weights)
    lower_total = sum(lower_weights)
    upper_mean = (
        sum(w * v for w, v in zip(upper_weights, upper_values)) / upper_total if upper_total > 1e-30 else 0.0
    )
    lower_mean = (
        sum(w * v for w, v in zip(lower_weights, lower_values)) / lower_total if lower_total > 1e-30 else 0.0
    )
    return upper_mean - lower_mean


def _evaluate_trial(task: tuple[int, int]) -> TrialRow | None:
    n_layers, seed = task
    positions, adj, _ = generate_causal_dag(
        n_layers=n_layers,
        nodes_per_layer=25,
        y_range=12.0,
        connect_radius=3.0,
        rng_seed=seed * 11 + 7,
    )
    n = len(positions)
    by_layer: dict[int, list[int]] = defaultdict(list)
    for idx, (x, _y) in enumerate(positions):
        by_layer[round(x)].append(idx)
    layers = sorted(by_layer.keys())
    if len(layers) < 5:
        return None

    src = by_layer[layers[0]]
    det = set(by_layer[layers[-1]])
    if not det:
        return None

    all_ys = [y for _, y in positions]
    center_y = statistics.fmean(all_ys)
    mid = len(layers) // 2
    grav_mass = [i for i in by_layer[layers[mid]] if positions[i][1] > center_y + 2.0]
    if len(grav_mass) < 2:
        return None

    free_field = [0.0] * n
    mass_field = compute_field(positions, adj, grav_mass)
    source_layers = {layers[mid - 1], layers[mid]} if mid > 0 else {layers[mid]}
    probe_layers = {layers[mid], layers[min(mid + 1, len(layers) - 1)]}

    detector_centroid_values: list[float] = []
    detector_channel_values: list[float] = []
    packet_current_values: list[float] = []
    action_channel_values: list[float] = []
    visibility_values: list[float] = []
    width_ref = 1.0

    free_action_mean = _propagate_action_means(positions, adj, free_field, src)
    mass_action_mean = _propagate_action_means(positions, adj, mass_field, src)
    action_delta = {node: mass_action_mean.get(node, 0.0) - free_action_mean.get(node, 0.0) for node in range(n)}

    for k in K_BAND:
        free_amps = _propagate_node_amplitudes(positions, adj, free_field, src, k)
        mass_amps = _propagate_node_amplitudes(positions, adj, mass_field, src, k)

        free_probs = _detector_probs(free_amps, det)
        mass_probs = _detector_probs(mass_amps, det)
        mass_node_probs = _node_probs(mass_amps)
        width_ref = _beam_width(free_probs, positions)

        detector_centroid_values.append((centroid_y(mass_probs, positions) - centroid_y(free_probs, positions)) / width_ref)
        detector_channel_values.append((_detector_channel_shift(mass_probs, positions) - _detector_channel_shift(free_probs, positions)) / width_ref)
        packet_current_values.append(
            (_packet_current_bias(positions, adj, mass_field, mass_amps, source_layers) -
             _packet_current_bias(positions, adj, free_field, free_amps, source_layers)) / width_ref
        )
        action_channel_values.append(
            _action_channel_bias(positions, action_delta, mass_node_probs, probe_layers, center_y) / width_ref
        )
        visibility_values.append(_visibility_guardrail(free_probs, positions))

    return TrialRow(
        n_layers=n_layers,
        seed=seed,
        detector_centroid=statistics.fmean(detector_centroid_values),
        detector_channel=statistics.fmean(detector_channel_values),
        packet_current=statistics.fmean(packet_current_values),
        action_channel=statistics.fmean(action_channel_values),
        width=width_ref,
        visibility_guardrail=statistics.fmean(visibility_values),
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workers", type=int, default=min(8, max(1, os.cpu_count() or 1)))
    parser.add_argument("--seeds", type=int, default=5)
    args = parser.parse_args()

    tasks = [(n_layers, seed) for n_layers in N_LAYERS for seed in range(args.seeds)]
    ctx = mp.get_context("fork")
    if args.workers <= 1:
        rows = [_evaluate_trial(task) for task in tasks]
    else:
        with ProcessPoolExecutor(max_workers=args.workers, mp_context=ctx) as pool:
            rows = list(pool.map(_evaluate_trial, tasks))
    rows = [row for row in rows if row is not None]

    metrics = (
        ("detector_centroid", lambda row: row.detector_centroid),
        ("detector_channel", lambda row: row.detector_channel),
        ("packet_current", lambda row: row.packet_current),
        ("action_channel", lambda row: row.action_channel),
    )

    grouped: dict[int, list[TrialRow]] = defaultdict(list)
    for row in rows:
        grouped[row.n_layers].append(row)

    print("=" * 88)
    print("GRAVITY OBSERVABLE READOUT SCALING COMPARE")
    print("=" * 88)
    print(f"Retained micro transport only; workers={args.workers}, seeds={args.seeds}, k_band={K_BAND}")
    print()
    print(
        f"{'N':>4s} {'n':>3s} {'R_det':>9s} {'R_chan':>9s} "
        f"{'R_curr':>9s} {'R_act':>9s} {'V_free':>9s}"
    )
    print("-" * 66)
    for n_layers in N_LAYERS:
        bucket = grouped.get(n_layers, [])
        if not bucket:
            continue
        print(
            f"{n_layers:4d} {len(bucket):3d} "
            f"{statistics.fmean(row.detector_centroid for row in bucket):+9.4f} "
            f"{statistics.fmean(row.detector_channel for row in bucket):+9.4f} "
            f"{statistics.fmean(row.packet_current for row in bucket):+9.4f} "
            f"{statistics.fmean(row.action_channel for row in bucket):+9.4f} "
            f"{statistics.fmean(row.visibility_guardrail for row in bucket):9.4f}"
        )
    print()
    print("N=25 / N=12 retention:")
    base_bucket = grouped.get(12, [])
    high_bucket = grouped.get(25, [])
    if base_bucket and high_bucket:
        for label, getter in metrics:
            base = statistics.fmean(getter(row) for row in base_bucket)
            high = statistics.fmean(getter(row) for row in high_bucket)
            ratio = high / base if abs(base) > 1e-12 else float("inf")
            abs_ratio = abs(high) / abs(base) if abs(base) > 1e-12 else float("inf")
            sign_stable = (base == 0.0 and high == 0.0) or (base > 0 and high > 0) or (base < 0 and high < 0)
            print(f"  {label:>17s}: signed={ratio:+.4f} |mag|={abs_ratio:.4f} sign_stable={sign_stable}")
    print()
    if base_bucket and high_bucket:
        ranked = []
        for label, getter in metrics:
            base = statistics.fmean(getter(row) for row in base_bucket)
            high = statistics.fmean(getter(row) for row in high_bucket)
            abs_ratio = abs(high) / abs(base) if abs(base) > 1e-12 else float("-inf")
            sign_stable = (base == 0.0 and high == 0.0) or (base > 0 and high > 0) or (base < 0 and high < 0)
            ranked.append((1 if sign_stable else 0, abs_ratio, label, base, high))
        ranked.sort(reverse=True)
        sign_flag, best_abs_ratio, best_label, base, high = ranked[0]
        print("Interpretation:")
        print(
            f"  Best scaling retention on this bounded family is {best_label}: "
            f"N=12 {base:+.4f} -> N=25 {high:+.4f} "
            f"(|mag| ratio {best_abs_ratio:.4f}, sign_stable={bool(sign_flag)})."
        )
        print("  Visibility is unchanged by construction because the microscopic propagator is unchanged;")
        print("  the `V_free` column is only a guardrail readout on the same underlying micro run.")


if __name__ == "__main__":
    main()
