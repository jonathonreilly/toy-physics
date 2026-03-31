#!/usr/bin/env python3
"""Test attenuation-based gravitational attraction on generated DAGs.

Previous finding: spent_fraction action attracts on lattices but NOT
on random DAGs. The issue: random graph path-length diversity destroys
phase coherence even with bounded action.

New idea: instead of fighting phase incoherence, USE it. Make
high-field regions have LOWER attenuation (amplitude survives better
near mass). Then regardless of phase, more amplitude passes through
the mass region → probability shifts toward mass = attraction.

This decouples attraction from phase coherence entirely.

Attenuation modes to test:
1. Standard: 1/delay^p (high field = more attenuation = repulsion)
2. Inverse: delay^p (high field = less attenuation = attraction?)
3. Retained: retained^p / delay^p (proper time fraction amplification)
4. Gradient: exp(-gradient_magnitude) (flat-field paths attenuated)

PStack experiment: amplitude-attenuation-attraction
"""

from __future__ import annotations
import math
import cmath
import random
from collections import defaultdict
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.generative_causal_dag_interference import generate_causal_dag
from toy_event_physics import (
    build_rectangular_nodes,
    derive_local_rule,
    derive_node_field,
    RulePostulates,
    infer_arrival_times_from_source,
    build_causal_dag,
)


# ================================================================
# Attenuation functions: (delay, link_length, local_field) → real multiplier
# ================================================================

def atten_standard(delay, link_length, local_field, power=1.0):
    """Standard: 1/delay^p. High field = high delay = stronger attenuation."""
    return 1.0 / (delay ** power) if delay > 0 else 1.0

def atten_flat(delay, link_length, local_field, power=1.0):
    """No attenuation (control). Amplitude only changes via phase."""
    return 1.0

def atten_field_boost(delay, link_length, local_field, power=1.0):
    """Boost near mass: (1 + field)^power. High field = AMPLIFICATION."""
    return (1.0 + local_field) ** power

def atten_retained_fraction(delay, link_length, local_field, power=1.0):
    """retained/delay = sqrt(1 - (L/delay)²). DECREASES in high field
    (retained grows but delay grows faster). Standard normalization."""
    retained = math.sqrt(max(delay * delay - link_length * link_length, 0.0))
    frac = retained / delay if delay > 0 else 1.0
    return frac ** power / (link_length ** power) if link_length > 0 else 1.0

def atten_inv_spent(delay, link_length, local_field, power=1.0):
    """1/(1 + spent_fraction). High field = high spent = LESS amplitude.
    But bounded: never goes below 0.5. Gentle attenuation."""
    retained = math.sqrt(max(delay * delay - link_length * link_length, 0.0))
    sf = (delay - retained) / delay if delay > 0 else 0.0
    return 1.0 / ((1.0 + sf) ** power * link_length ** power) if link_length > 0 else 1.0

def atten_link_only(delay, link_length, local_field, power=1.0):
    """1/L^p. Pure geometry, no field dependence (another control)."""
    return 1.0 / (link_length ** power) if link_length > 0 else 1.0


ATTEN_MODES = [
    ("1/delay^p (standard)", atten_standard),
    ("flat (phase only)", atten_flat),
    ("(1+field)^p (boost)", atten_field_boost),
    ("retained_frac^p", atten_retained_fraction),
    ("1/(1+sf)^p", atten_inv_spent),
    ("1/L^p (geometry)", atten_link_only),
]


def pathsum_custom_atten_dag(
    positions, adj, field, source_indices, detector_indices,
    phase_k, action_func, atten_func,
):
    """Propagate amplitude on generated DAG with custom action + attenuation."""
    n = len(positions)

    in_degree = [0] * n
    for i, nbs in adj.items():
        for j in nbs:
            in_degree[j] += 1

    from collections import deque
    queue = deque()
    for i in range(n):
        if in_degree[i] == 0:
            queue.append(i)

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
            link_length = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
            if link_length < 1e-10:
                continue
            local_field = 0.5 * (field[i] + field[j])
            delay = link_length * (1.0 + local_field)

            action = action_func(delay, link_length, local_field)
            atten = atten_func(delay, link_length, local_field)

            edge_amp = cmath.exp(1j * phase_k * action) * atten
            amplitudes[j] += amp * edge_amp

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


# Action functions
def action_spent_delay(delay, link_length, local_field):
    retained = math.sqrt(max(delay * delay - link_length * link_length, 0.0))
    return delay - retained

def action_spent_fraction(delay, link_length, local_field):
    retained = math.sqrt(max(delay * delay - link_length * link_length, 0.0))
    return (delay - retained) / delay if delay > 0 else 0.0

def action_link_length(delay, link_length, local_field):
    return link_length


def run_dag_test(n_seeds=10, phase_k=2.5, action_func=action_spent_fraction,
                 atten_func=atten_standard, label=""):
    """Run attraction test on generated DAGs, return (attract_count, total, mean_shift)."""
    n_layers = 12
    nodes_per_layer = 20
    connect_radius = 3.0

    shifts = []
    attract = 0
    total = 0

    for seed in range(n_seeds):
        positions, adj, arrival = generate_causal_dag(
            n_layers=n_layers, nodes_per_layer=nodes_per_layer,
            connect_radius=connect_radius, rng_seed=seed * 7 + 42,
        )

        by_layer = defaultdict(list)
        for idx, (x, y) in enumerate(positions):
            by_layer[round(x)].append(idx)

        layers = sorted(by_layer.keys())
        if len(layers) < 3:
            continue

        source_indices = by_layer[layers[0]]
        detector_indices = by_layer[layers[-1]]
        mid_layer = layers[len(layers) // 2]
        mid_indices = by_layer[mid_layer]

        if not mid_indices or not detector_indices:
            continue

        all_ys = [y for _, y in positions]
        center_y = sum(all_ys) / len(all_ys)
        mass_indices = [i for i in mid_indices if positions[i][1] > center_y + 0.5]
        if len(mass_indices) < 2:
            continue

        mass_cy = sum(positions[i][1] for i in mass_indices) / len(mass_indices)

        free_field = [0.0] * len(positions)
        free_probs = pathsum_custom_atten_dag(
            positions, adj, free_field, source_indices, detector_indices,
            phase_k, action_func, atten_func,
        )

        mass_field = compute_field_on_dag(positions, adj, mass_indices)
        mass_probs = pathsum_custom_atten_dag(
            positions, adj, mass_field, source_indices, detector_indices,
            phase_k, action_func, atten_func,
        )

        fcy = centroid_y(free_probs, positions)
        mcy = centroid_y(mass_probs, positions)
        shift = mcy - fcy
        shifts.append(shift)
        total += 1

        toward_dir = mass_cy - center_y
        if (toward_dir > 0 and shift > 0.05) or (toward_dir < 0 and shift < -0.05):
            attract += 1

    mean = sum(shifts) / len(shifts) if shifts else 0.0
    return attract, total, mean


def main() -> None:
    print("=" * 80)
    print("ATTENUATION-BASED GRAVITATIONAL ATTRACTION ON GENERATED DAGs")
    print("=" * 80)
    print()

    # ================================================================
    # TEST 1: Attenuation mode sweep (fixed action = spent_fraction)
    # ================================================================
    print("TEST 1: Attenuation sweep with spent_fraction action, k=2.5")
    print()
    print(f"  {'attenuation':>25s}  {'attract':>8s}  {'total':>6s}  {'mean_shift':>10s}")
    print(f"  {'-' * 56}")

    for name, atten_func in ATTEN_MODES:
        attract, total, mean = run_dag_test(
            n_seeds=10, phase_k=2.5,
            action_func=action_spent_fraction,
            atten_func=atten_func,
        )
        pct = f"{100*attract//total}%" if total > 0 else "n/a"
        print(f"  {name:>25s}  {attract:>5d}/{total:<2d}  {total:6d}  {mean:+10.4f}")

    # ================================================================
    # TEST 2: Best attenuation × action × k combinations
    # ================================================================
    print()
    print("TEST 2: Combinatorial sweep — action × attenuation × k")
    print()

    actions = [
        ("spent_fraction", action_spent_fraction),
        ("spent_delay", action_spent_delay),
        ("link_length", action_link_length),
    ]

    best_combo = ("", "", 0, 0, 0, -999)

    print(f"  {'action':>15s}  {'attenuation':>20s}  {'k':>5s}  {'attr':>5s}  {'mean':>8s}")
    print(f"  {'-' * 62}")

    for act_name, act_func in actions:
        for att_name, att_func in ATTEN_MODES:
            for k in [1.0, 2.5, 4.0, 8.0]:
                attract, total, mean = run_dag_test(
                    n_seeds=8, phase_k=k,
                    action_func=act_func,
                    atten_func=att_func,
                )
                if total == 0:
                    continue
                pct = 100 * attract / total
                if pct >= 50 or mean > 0.05:
                    print(f"  {act_name:>15s}  {att_name:>20s}  {k:5.1f}  "
                          f"{attract:2d}/{total:<2d}  {mean:+8.4f}")
                if attract > best_combo[3] or (attract == best_combo[3] and mean > best_combo[5]):
                    best_combo = (act_name, att_name, k, attract, total, mean)

    print()
    print(f"  BEST: action={best_combo[0]}, atten={best_combo[1]}, k={best_combo[2]}")
    print(f"        attract={best_combo[3]}/{best_combo[4]}, mean_shift={best_combo[5]:+.4f}")

    # ================================================================
    # TEST 3: Flip test for best combo
    # ================================================================
    print()
    print("TEST 3: Flip test for best combo (mass above vs below)")
    print()

    # Find the best action and attenuation functions
    best_act = next(f for n, f in actions if n == best_combo[0])
    best_att = next(f for n, f in ATTEN_MODES if n == best_combo[1])
    best_k = best_combo[2]

    n_layers = 12
    nodes_per_layer = 20
    connect_radius = 3.0
    flip_count = 0
    total_count = 0

    print(f"  {'seed':>4s}  {'above':>8s}  {'below':>8s}  {'flips?':>6s}")
    print(f"  {'-' * 32}")

    for seed in range(12):
        positions, adj, arrival = generate_causal_dag(
            n_layers=n_layers, nodes_per_layer=nodes_per_layer,
            connect_radius=connect_radius, rng_seed=seed * 7 + 42,
        )

        by_layer = defaultdict(list)
        for idx, (x, y) in enumerate(positions):
            by_layer[round(x)].append(idx)

        layers = sorted(by_layer.keys())
        if len(layers) < 3:
            continue

        source_indices = by_layer[layers[0]]
        detector_indices = by_layer[layers[-1]]
        mid_layer = layers[len(layers) // 2]
        mid_indices = by_layer[mid_layer]

        if not mid_indices or not detector_indices:
            continue

        all_ys = [y for _, y in positions]
        center_y = sum(all_ys) / len(all_ys)
        above = [i for i in mid_indices if positions[i][1] > center_y + 0.5]
        below = [i for i in mid_indices if positions[i][1] < center_y - 0.5]

        if len(above) < 2 or len(below) < 2:
            continue

        free_field = [0.0] * len(positions)
        free_probs = pathsum_custom_atten_dag(
            positions, adj, free_field, source_indices, detector_indices,
            best_k, best_act, best_att,
        )
        fcy = centroid_y(free_probs, positions)

        above_field = compute_field_on_dag(positions, adj, above)
        above_probs = pathsum_custom_atten_dag(
            positions, adj, above_field, source_indices, detector_indices,
            best_k, best_act, best_att,
        )
        a_shift = centroid_y(above_probs, positions) - fcy

        below_field = compute_field_on_dag(positions, adj, below)
        below_probs = pathsum_custom_atten_dag(
            positions, adj, below_field, source_indices, detector_indices,
            best_k, best_act, best_att,
        )
        b_shift = centroid_y(below_probs, positions) - fcy

        total_count += 1
        flips = "YES" if (a_shift > 0.05 and b_shift < -0.05) or \
                         (a_shift < -0.05 and b_shift > 0.05) else "no"
        if flips == "YES":
            flip_count += 1

        print(f"  {seed:4d}  {a_shift:+8.4f}  {b_shift:+8.4f}  {flips:>6s}")

    print()
    print(f"  Flips: {flip_count}/{total_count}")

    print()
    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print()
    print("Key question: can attenuation (not just phase) produce attraction")
    print("on random graphs where phase coherence fails?")
    print()
    print("TEST COMPLETE")


if __name__ == "__main__":
    main()
