#!/usr/bin/env python3
"""Path-sampling diagnostic for the b-independence mechanism.

This is a review-safe companion to the distance-law closure work.

The point is not to rescue a 1/b law. The point is to ask whether the
current retained modular DAGs preserve transverse path identity locally
while the smooth graph-wide field still acts roughly uniformly across the
connected path ensemble.

We measure two things on the retained 4D modular family:
  1. detector-side channel preservation under upper/lower channel openings
  2. layer-by-layer transverse spread of the amplitude distribution

If the upper-channel run stays mostly on the upper side and the lower-channel
run stays mostly on the lower side, then the flat distance law is not coming
from a simple "paths scramble to the center" story.
"""

from __future__ import annotations

import math
import os
import statistics
import sys
from collections import defaultdict

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.four_d_distance_scaling import (  # noqa: E402
    K_BAND,
    compute_field_4d,
    generate_4d_modular_dag,
    propagate_4d,
    select_mass_nodes,
)

N_SEEDS = 8
N_LAYERS = 18
NODES_PER_LAYER = 40
SPATIAL_RANGE = 8.0
CONNECT_RADIUS = 4.5
GAP = 5.0
TARGET_B = 5.0
MASS_COUNT = 8
FOCUS_LAYERS = 3


def _mean(values: list[float]) -> float:
    return sum(values) / len(values) if values else math.nan


def _se(values: list[float]) -> float:
    if len(values) < 2:
        return math.nan
    return statistics.stdev(values) / math.sqrt(len(values))


def _topo_layers(positions: list[tuple[float, float, float, float]]) -> dict[int, list[int]]:
    by_layer: dict[int, list[int]] = defaultdict(list)
    for idx, (x, *_rest) in enumerate(positions):
        by_layer[round(x)].append(idx)
    return by_layer


def _top_barrier_split(
    positions: list[tuple[float, float, float, float]],
    layer_nodes: list[int],
) -> tuple[list[int], list[int]]:
    upper = [i for i in layer_nodes if positions[i][1] >= 0.0]
    lower = [i for i in layer_nodes if positions[i][1] < 0.0]
    return upper, lower


def _weighted_y_stats(
    amps: list[complex],
    positions: list[tuple[float, float, float, float]],
    nodes: list[int],
) -> tuple[float, float, float]:
    total = 0.0
    wy = 0.0
    wy2 = 0.0
    for i in nodes:
        p = abs(amps[i]) ** 2
        total += p
        wy += p * positions[i][1]
        wy2 += p * positions[i][1] ** 2
    if total <= 1e-30:
        return 0.0, 0.0, 0.0
    mean_y = wy / total
    var_y = max(wy2 / total - mean_y**2, 0.0)
    return mean_y, math.sqrt(var_y), total


def _same_side_fraction(
    amps: list[complex],
    positions: list[tuple[float, float, float, float]],
    nodes: list[int],
    open_sign: int,
) -> float:
    total = 0.0
    same = 0.0
    for i in nodes:
        p = abs(amps[i]) ** 2
        total += p
        if open_sign > 0 and positions[i][1] >= 0.0:
            same += p
        elif open_sign < 0 and positions[i][1] < 0.0:
            same += p
    return same / total if total > 1e-30 else 0.0


def _open_side_metrics(
    positions: list[tuple[float, float, float, float]],
    adj: dict[int, list[int]],
    field: list[float],
    src: list[int],
    det_list: list[int],
    upper_nodes: list[int],
    lower_nodes: list[int],
    open_side: str,
) -> dict[str, float]:
    if open_side == "upper":
        blocked = set(lower_nodes)
        open_sign = 1
    else:
        blocked = set(upper_nodes)
        open_sign = -1

    by_layer = _topo_layers(positions)
    layers = sorted(by_layer)
    barrier_layer = len(layers) // 3
    post_barrier = []
    for layer in layers[barrier_layer + 1 : barrier_layer + 1 + FOCUS_LAYERS]:
        post_barrier.extend(by_layer[layer])

    metrics: dict[str, float] = {
        "det_same": 0.0,
        "det_mean_y": 0.0,
        "det_std_y": 0.0,
        "focus_same": 0.0,
        "focus_mean_y": 0.0,
        "focus_std_y": 0.0,
    }
    n_used = 0
    for k in K_BAND:
        amps = propagate_4d(positions, adj, field, src, k, blocked)
        det_mean_y, det_std_y, _ = _weighted_y_stats(amps, positions, det_list)
        focus_mean_y, focus_std_y, _ = _weighted_y_stats(amps, positions, post_barrier)
        metrics["det_same"] += _same_side_fraction(amps, positions, det_list, open_sign=open_sign)
        metrics["det_mean_y"] += det_mean_y
        metrics["det_std_y"] += det_std_y
        metrics["focus_same"] += _same_side_fraction(amps, positions, post_barrier, open_sign=open_sign)
        metrics["focus_mean_y"] += focus_mean_y
        metrics["focus_std_y"] += focus_std_y
        n_used += 1

    if n_used == 0:
        return metrics
    for key in metrics:
        metrics[key] /= n_used
    return metrics


def main() -> None:
    print("=" * 78)
    print("PATH SAMPLING ANALYSIS")
    print("  Local path preservation on the retained 4D modular family")
    print("  Goal: check whether transverse labels stay local while the")
    print("        path ensemble still spans the graph broadly enough")
    print("=" * 78)
    print()

    buckets = {
        "upper:flat": {"det_same": [], "det_mean_y": [], "det_std_y": [], "focus_same": [], "focus_mean_y": [], "focus_std_y": []},
        "lower:flat": {"det_same": [], "det_mean_y": [], "det_std_y": [], "focus_same": [], "focus_mean_y": [], "focus_std_y": []},
        "upper:mass": {"det_same": [], "det_mean_y": [], "det_std_y": [], "focus_same": [], "focus_mean_y": [], "focus_std_y": []},
        "lower:mass": {"det_same": [], "det_mean_y": [], "det_std_y": [], "focus_same": [], "focus_mean_y": [], "focus_std_y": []},
    }

    for seed in range(N_SEEDS):
        positions, adj, layer_indices = generate_4d_modular_dag(
            n_layers=N_LAYERS,
            nodes_per_layer=NODES_PER_LAYER,
            spatial_range=SPATIAL_RANGE,
            connect_radius=CONNECT_RADIUS,
            rng_seed=seed * 13 + 5,
            gap=GAP,
        )

        by_layer = _topo_layers(positions)
        layers = sorted(by_layer)
        if len(layers) < 7:
            continue
        src = by_layer[layers[0]]
        det_list = list(by_layer[layers[-1]])
        if not det_list:
            continue

        center_y = statistics.fmean(positions[i][1] for i in range(len(positions)))
        grav_layer = layers[2 * len(layers) // 3]
        mass_nodes = select_mass_nodes(by_layer[grav_layer], positions, center_y, TARGET_B, MASS_COUNT)
        if not mass_nodes:
            continue

        field_mass = compute_field_4d(positions, adj, mass_nodes)
        field_flat = [0.0] * len(positions)

        barrier_nodes = by_layer[layers[len(layers) // 3]]
        upper_nodes, lower_nodes = _top_barrier_split(positions, barrier_nodes)
        if not upper_nodes or not lower_nodes:
            continue

        for open_side, field in (("upper", field_flat), ("lower", field_flat), ("upper", field_mass), ("lower", field_mass)):
            metrics = _open_side_metrics(positions, adj, field, src, det_list, upper_nodes, lower_nodes, open_side)
            key = f"{open_side}:{'mass' if field is field_mass else 'flat'}"
            bucket = buckets[key]
            for metric_name, value in metrics.items():
                bucket[metric_name].append(value)

    print(f"{'channel':>10s}  {'det_same':>8s}  {'det_mean_y':>10s}  {'det_std_y':>10s}  {'focus_same':>10s}")
    print(f"{'-' * 60}")
    for key in ("upper:flat", "lower:flat", "upper:mass", "lower:mass"):
        det_same = _mean(buckets[key]["det_same"])
        det_mean_y = _mean(buckets[key]["det_mean_y"])
        det_std_y = _mean(buckets[key]["det_std_y"])
        focus_same = _mean(buckets[key]["focus_same"])
        print(f"{key:>10s}  {det_same:8.3f}  {det_mean_y:10.3f}  {det_std_y:10.3f}  {focus_same:10.3f}")

    print()
    print("INTERPRETATION")
    print("  If the open channel keeps most detector mass on the same side and")
    print("  the post-barrier layers stay channelized, then the force law is not")
    print("  being flattened by path scrambling.")
    print("  That leaves the smooth graph-wide field / phase-valley mechanism as")
    print("  the more plausible source of the broad, topological response.")
    print("  This is a mechanism diagnostic, not a new distance-law rescue.")


if __name__ == "__main__":
    main()
