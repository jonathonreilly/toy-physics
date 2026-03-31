#!/usr/bin/env python3
"""Priority 1: Why does compact density (y_range=3) kill attraction?

Hypotheses:
A. Field saturation: compact graph → field ≈ 1 everywhere → no gradient
B. Path crowding: too many short paths → phase averages to zero
C. Insufficient phase separation: short paths = small action difference
D. Symmetric flooding: mass is too close to beam center, affects both sides

Also investigate: the flat distance scaling (shift ~ b^0.01) suggests
the "attraction" is a phase-polarity flip, not gentle deflection.
What controls whether the phase tips positive or negative?

PStack experiment: compact-density-diagnosis
"""

from __future__ import annotations
import math
import cmath
from collections import defaultdict
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.generative_causal_dag_interference import generate_causal_dag


def compute_field_on_dag(positions, adj, mass_indices, iterations=50):
    n = len(positions)
    undirected = defaultdict(set)
    for i, nbs in adj.items():
        for j in nbs:
            undirected[i].add(j)
            undirected[j].add(i)
    mass_set = set(mass_indices)
    field = [1.0 if i in mass_set else 0.0 for i in range(n)]
    for _ in range(iterations):
        new_field = [0.0] * n
        for i in range(n):
            if i in mass_set:
                new_field[i] = 1.0
                continue
            nbs = undirected.get(i, set())
            if nbs:
                new_field[i] = sum(field[j] for j in nbs) / len(nbs)
        field = new_field
    return field


def pathsum_corrected_dag(positions, adj, field, source_indices, detector_indices,
                          phase_k, atten_power=1.0):
    n = len(positions)
    in_degree = [0] * n
    for i, nbs in adj.items():
        for j in nbs:
            in_degree[j] += 1
    from collections import deque
    queue = deque(i for i in range(n) if in_degree[i] == 0)
    order = []
    while queue:
        i = queue.popleft()
        order.append(i)
        for j in adj.get(i, []):
            in_degree[j] -= 1
            if in_degree[j] == 0:
                queue.append(j)

    amplitudes = [0.0 + 0.0j] * n
    for s in source_indices:
        amplitudes[s] = 1.0 / len(source_indices) + 0.0j

    for i in order:
        amp = amplitudes[i]
        if abs(amp) < 1e-30:
            continue
        for j in adj.get(i, []):
            x1, y1 = positions[i]
            x2, y2 = positions[j]
            L = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
            if L < 1e-10:
                continue
            lf = 0.5 * (field[i] + field[j])
            delay = L * (1.0 + lf)
            retained = math.sqrt(max(delay * delay - L * L, 0.0))
            action = delay - retained
            atten = 1.0 / (L ** atten_power)
            ea = cmath.exp(1j * phase_k * action) * atten
            amplitudes[j] += amp * ea

    probs = {}
    for d in detector_indices:
        probs[d] = abs(amplitudes[d]) ** 2
    total = sum(probs.values())
    if total > 0:
        probs = {d: p / total for d, p in probs.items()}
    return probs


def centroid_y(probs, positions):
    total = sum(probs.values())
    if total == 0:
        return 0.0
    return sum(positions[d][1] * p for d, p in probs.items()) / total


def main() -> None:
    n_layers = 12
    nodes_per_layer = 20
    connect_radius = 3.0
    k_band = [3.0, 5.0, 7.0]
    n_seeds = 5

    print("=" * 80)
    print("COMPACT DENSITY DIAGNOSIS")
    print("=" * 80)
    print()

    # ================================================================
    # TEST A: Field saturation
    # ================================================================
    print("TEST A: Field gradient vs y_range")
    print("  Is the field gradient destroyed in compact graphs?")
    print()

    print(f"  {'y_range':>8s}  {'mean_field':>10s}  {'field_std':>10s}  {'grad_mag':>10s}")
    print(f"  {'-' * 44}")

    for yr in [3.0, 5.0, 8.0, 10.0, 15.0, 20.0]:
        field_means = []
        field_stds = []
        grads = []

        for seed in range(n_seeds):
            positions, adj, arrival = generate_causal_dag(
                n_layers=n_layers, nodes_per_layer=nodes_per_layer,
                y_range=yr, connect_radius=connect_radius,
                rng_seed=seed * 13 + 5,
            )

            by_layer = defaultdict(list)
            for idx, (x, y) in enumerate(positions):
                by_layer[round(x)].append(idx)
            layers = sorted(by_layer.keys())
            if len(layers) < 4:
                continue

            mid = len(layers) // 2
            mid_idx = by_layer[layers[mid]]
            all_ys = [y for _, y in positions]
            center_y = sum(all_ys) / len(all_ys)
            mass_idx = [i for i in mid_idx if positions[i][1] > center_y + 0.5]
            if len(mass_idx) < 2:
                continue

            field = compute_field_on_dag(positions, adj, mass_idx)

            # Stats at detector layer
            det_layer = layers[-1]
            det_idx = by_layer[det_layer]
            det_fields = [field[i] for i in det_idx]
            if det_fields:
                mean_f = sum(det_fields) / len(det_fields)
                std_f = (sum((f - mean_f) ** 2 for f in det_fields) / len(det_fields)) ** 0.5
                field_means.append(mean_f)
                field_stds.append(std_f)

            # Field gradient at detector: difference between y>0 and y<0
            above = [field[i] for i in det_idx if positions[i][1] > center_y]
            below = [field[i] for i in det_idx if positions[i][1] < center_y]
            if above and below:
                grad = sum(above) / len(above) - sum(below) / len(below)
                grads.append(grad)

        if field_means:
            print(f"  {yr:8.1f}  {sum(field_means)/len(field_means):10.4f}  "
                  f"{sum(field_stds)/len(field_stds):10.4f}  "
                  f"{sum(grads)/len(grads) if grads else 0:+10.4f}")

    # ================================================================
    # TEST B: Phase action difference above vs below beam
    # ================================================================
    print()
    print("TEST B: Action difference (mass-side vs free-side)")
    print("  How much does the action differ for paths above vs below?")
    print()

    print(f"  {'y_range':>8s}  {'action_above':>12s}  {'action_below':>12s}  {'diff':>10s}  {'attract':>7s}")
    print(f"  {'-' * 54}")

    for yr in [3.0, 5.0, 8.0, 10.0, 15.0, 20.0]:
        all_diffs = []
        attract_count = 0
        total_count = 0

        for seed in range(n_seeds):
            positions, adj, arrival = generate_causal_dag(
                n_layers=n_layers, nodes_per_layer=nodes_per_layer,
                y_range=yr, connect_radius=connect_radius,
                rng_seed=seed * 13 + 5,
            )

            by_layer = defaultdict(list)
            for idx, (x, y) in enumerate(positions):
                by_layer[round(x)].append(idx)
            layers = sorted(by_layer.keys())
            if len(layers) < 4:
                continue

            src = by_layer[layers[0]]
            det = by_layer[layers[-1]]
            mid = len(layers) // 2
            mid_idx = by_layer[layers[mid]]
            all_ys = [y for _, y in positions]
            center_y = sum(all_ys) / len(all_ys)
            mass_idx = [i for i in mid_idx if positions[i][1] > center_y + 0.5]
            if len(mass_idx) < 2:
                continue

            mass_cy = sum(positions[i][1] for i in mass_idx) / len(mass_idx)
            field = compute_field_on_dag(positions, adj, mass_idx)

            # Compute total action along "above" and "below" edges
            action_above = []
            action_below = []
            for i, nbs in adj.items():
                for j in nbs:
                    x1, y1 = positions[i]
                    x2, y2 = positions[j]
                    L = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
                    if L < 1e-10:
                        continue
                    lf = 0.5 * (field[i] + field[j])
                    delay = L * (1 + lf)
                    ret = math.sqrt(max(delay**2 - L**2, 0))
                    action = delay - ret
                    avg_y = 0.5 * (y1 + y2)
                    if avg_y > center_y:
                        action_above.append(action)
                    else:
                        action_below.append(action)

            if action_above and action_below:
                mean_above = sum(action_above) / len(action_above)
                mean_below = sum(action_below) / len(action_below)
                all_diffs.append(mean_above - mean_below)

            # Also measure attraction
            free_f = [0.0] * len(positions)
            k_shifts = []
            for k in k_band:
                fp = pathsum_corrected_dag(positions, adj, free_f, src, det, k)
                mp = pathsum_corrected_dag(positions, adj, field, src, det, k)
                fcy = centroid_y(fp, positions)
                mcy = centroid_y(mp, positions)
                k_shifts.append(mcy - fcy)
            avg_shift = sum(k_shifts) / len(k_shifts)
            total_count += 1
            if (mass_cy - center_y > 0 and avg_shift > 0.05):
                attract_count += 1

        if all_diffs:
            mean_diff = sum(all_diffs) / len(all_diffs)
            apct = f"{attract_count}/{total_count}"
            mean_a = sum(d for d in all_diffs) / len(all_diffs) if all_diffs else 0
            # Use a representative value for above/below
            print(f"  {yr:8.1f}  {'(varies)':>12s}  {'(varies)':>12s}  "
                  f"{mean_diff:+10.4f}  {apct:>7s}")

    # ================================================================
    # TEST C: Per-detector-node probability distribution
    # ================================================================
    print()
    print("TEST C: Probability concentration at compact vs spread")
    print("  How concentrated is the detector probability distribution?")
    print()

    print(f"  {'y_range':>8s}  {'entropy_free':>12s}  {'entropy_mass':>12s}  {'entropy_drop':>12s}")
    print(f"  {'-' * 52}")

    for yr in [3.0, 5.0, 8.0, 10.0, 15.0, 20.0]:
        ent_free_list = []
        ent_mass_list = []

        for seed in range(n_seeds):
            positions, adj, arrival = generate_causal_dag(
                n_layers=n_layers, nodes_per_layer=nodes_per_layer,
                y_range=yr, connect_radius=connect_radius,
                rng_seed=seed * 13 + 5,
            )

            by_layer = defaultdict(list)
            for idx, (x, y) in enumerate(positions):
                by_layer[round(x)].append(idx)
            layers = sorted(by_layer.keys())
            if len(layers) < 4:
                continue

            src = by_layer[layers[0]]
            det = by_layer[layers[-1]]
            mid = len(layers) // 2
            mid_idx = by_layer[layers[mid]]
            all_ys = [y for _, y in positions]
            center_y = sum(all_ys) / len(all_ys)
            mass_idx = [i for i in mid_idx if positions[i][1] > center_y + 0.5]
            if len(mass_idx) < 2:
                continue

            free_f = [0.0] * len(positions)
            field = compute_field_on_dag(positions, adj, mass_idx)

            # k=5.0 single measurement
            fp = pathsum_corrected_dag(positions, adj, free_f, src, det, 5.0)
            mp = pathsum_corrected_dag(positions, adj, field, src, det, 5.0)

            def entropy(probs):
                return -sum(p * math.log(p + 1e-30) for p in probs.values() if p > 0)

            ent_free_list.append(entropy(fp))
            ent_mass_list.append(entropy(mp))

        if ent_free_list:
            ef = sum(ent_free_list) / len(ent_free_list)
            em = sum(ent_mass_list) / len(ent_mass_list)
            print(f"  {yr:8.1f}  {ef:12.3f}  {em:12.3f}  {em - ef:+12.3f}")

    # ================================================================
    # SUMMARY
    # ================================================================
    print()
    print("=" * 80)
    print("DIAGNOSIS SUMMARY")
    print("=" * 80)
    print()
    print("| regime       | field_grad | action_diff | attract | mechanism          |")
    print("|-------------|------------|-------------|---------|---------------------|")
    print("| compact y=3 | ???        | ???         | 0%      | to be determined    |")
    print("| sweet y=10  | ???        | ???         | 100%    | phase deflection    |")
    print("| spread y=30 | ???        | ???         | 20%     | gradient too weak   |")
    print()
    print("TEST COMPLETE")


if __name__ == "__main__":
    main()
