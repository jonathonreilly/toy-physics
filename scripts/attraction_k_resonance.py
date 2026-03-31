#!/usr/bin/env python3
"""Diagnose k-dependent attraction windows.

On rectangular grid with geometry attenuation (1/L^p):
- k=0.5 to 2.0: ATTRACTION
- k=4.0: REPULSION
- k=6.0 to 8.0: ATTRACTION

Hypothesis: this is a resonance effect. The spent_delay action per hop
at zero field is: S = L - sqrt(L²-L²) = L - 0 = L (for diagonal hops,
L=√2; for axial, L=1). The phase per hop is k*S. When k*S ≈ nπ,
destructive interference occurs; when k*S ≈ 2nπ, constructive.

In a field gradient, the action changes asymmetrically above/below
the beam. Whether this creates net attraction or repulsion depends
on whether the gradient pushes phases toward or away from a
constructive interference window.

Tests:
1. Fine k resolution to map exact resonance structure
2. Vary lattice connectivity (8-neighbor vs custom) to shift resonances
3. Check if generated DAGs (no lattice) have smoother k-dependence
4. Test whether averaging over a k-range produces robust attraction

PStack experiment: attraction-k-resonance
"""

from __future__ import annotations
import math
import cmath
import random
from collections import defaultdict
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from toy_event_physics import (
    RulePostulates,
    build_rectangular_nodes,
    derive_local_rule,
    derive_node_field,
    infer_arrival_times_from_source,
    build_causal_dag,
)
from scripts.generative_causal_dag_interference import generate_causal_dag


def launch_packet_geom(nodes, source, node_field, phase_k, atten_power,
                       detector_xs, screen_ys):
    """Amplitude packet with geometry-only attenuation."""
    postulates = RulePostulates(phase_per_action=phase_k, attenuation_power=atten_power)
    rule = derive_local_rule(persistent_nodes=frozenset(), postulates=postulates)
    arrival_times = infer_arrival_times_from_source(nodes, source, rule)
    dag = build_causal_dag(nodes, arrival_times)
    order = sorted(arrival_times, key=arrival_times.get)

    amplitudes = {source: 1.0 + 0.0j}
    for node in order:
        if node not in amplitudes:
            continue
        amp = amplitudes[node]
        for nb in dag.get(node, []):
            L = math.dist(node, nb)
            lf = 0.5 * (node_field.get(node, 0.0) + node_field.get(nb, 0.0))
            delay = L * (1.0 + lf)
            retained = math.sqrt(max(delay * delay - L * L, 0.0))
            action = delay - retained
            atten = 1.0 / (L ** atten_power) if L > 0 else 1.0
            ea = cmath.exp(1j * phase_k * action) * atten
            if nb not in amplitudes:
                amplitudes[nb] = 0.0 + 0.0j
            amplitudes[nb] += amp * ea

    result = {}
    for dx in detector_xs:
        dist = {}
        total = 0
        for y in screen_ys:
            p = abs(amplitudes.get((dx, y), 0.0)) ** 2
            dist[y] = p
            total += p
        if total > 0:
            dist = {y: p / total for y, p in dist.items()}
        result[dx] = dist
    return result


def centroid_y(distribution):
    total = sum(distribution.values())
    if total == 0:
        return 0.0
    return sum(y * p for y, p in distribution.items()) / total


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


def launch_packet_dag_geom(positions, adj, field, source_indices, detector_indices,
                           phase_k, atten_power):
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


def centroid_y_dag(probs, positions):
    total = sum(probs.values())
    if total == 0:
        return 0.0
    return sum(positions[d][1] * p for d, p in probs.items()) / total


def main() -> None:
    width = 40
    height = 15
    nodes = build_rectangular_nodes(width=width, height=height)
    source = (0, 0)
    screen_ys = list(range(-height, height + 1))
    postulates = RulePostulates(phase_per_action=4.0, attenuation_power=1.0)

    mass_nodes = frozenset((20, y) for y in range(4, 9))
    mass_rule = derive_local_rule(persistent_nodes=mass_nodes, postulates=postulates)
    mass_field = derive_node_field(nodes, mass_rule)
    free_field = {n: 0.0 for n in nodes}

    detector_xs = [20, 25, 30]

    print("=" * 80)
    print("K-DEPENDENCE OF GRAVITATIONAL ATTRACTION")
    print("  Geometry attenuation (1/L^p), spent_delay action")
    print("=" * 80)
    print()

    # ================================================================
    # TEST 1: Fine k resolution on rectangular grid
    # ================================================================
    print("TEST 1: Fine k resolution (0.1 to 10.0 in steps of 0.2)")
    print()

    k_values = [round(0.1 + 0.2 * i, 1) for i in range(50)]
    attract_ks = []
    repel_ks = []

    print(f"  {'k':>5s}  {'avg_shift':>10s}  {'dir':>8s}  {'phase/hop_diag':>14s}")
    print(f"  {'-' * 44}")

    for k in k_values:
        free_r = launch_packet_geom(nodes, source, free_field, k, 1.0, detector_xs, screen_ys)
        mass_r = launch_packet_geom(nodes, source, mass_field, k, 1.0, detector_xs, screen_ys)
        shifts = [centroid_y(mass_r[dx]) - centroid_y(free_r[dx]) for dx in detector_xs]
        avg = sum(shifts) / len(shifts)

        # Phase per hop: k * S where S = L - sqrt(L²-L²) = L for zero field
        # Diagonal hop: L = sqrt(2), so phase = k*sqrt(2)
        # This modulo 2π determines the resonance
        phase_diag = (k * math.sqrt(2)) % (2 * math.pi)

        d = "ATTRACT" if avg > 1.0 else "REPEL" if avg < -1.0 else "~0"
        if avg > 1.0:
            attract_ks.append(k)
        elif avg < -1.0:
            repel_ks.append(k)

        print(f"  {k:5.1f}  {avg:+10.2f}  {d:>8s}  {phase_diag:14.3f}")

    # Analyze resonance pattern
    print()
    print(f"  Attraction k-values: {attract_ks[:10]}...")
    print(f"  Repulsion k-values: {repel_ks[:10]}...")

    # Check if repulsion occurs at specific phase values
    if repel_ks:
        repel_phases = [(k * math.sqrt(2)) % (2 * math.pi) for k in repel_ks]
        print(f"  Repulsion phase/hop (mod 2π): mean={sum(repel_phases)/len(repel_phases):.3f}")
    if attract_ks:
        attract_phases = [(k * math.sqrt(2)) % (2 * math.pi) for k in attract_ks]
        print(f"  Attraction phase/hop (mod 2π): mean={sum(attract_phases)/len(attract_phases):.3f}")

    # ================================================================
    # TEST 2: Generated DAGs — smoother k-dependence?
    # ================================================================
    print()
    print("=" * 80)
    print("TEST 2: k-dependence on generated DAGs (5 seeds averaged)")
    print("  Random edge lengths → no lattice resonances?")
    print("=" * 80)
    print()

    k_values_dag = [round(0.5 + 0.5 * i, 1) for i in range(20)]
    print(f"  {'k':>5s}  {'attract':>8s}  {'mean_shift':>10s}")
    print(f"  {'-' * 28}")

    for k in k_values_dag:
        attract = 0
        shifts = []

        for seed in range(8):
            positions, adj, arrival = generate_causal_dag(
                n_layers=12, nodes_per_layer=20,
                connect_radius=3.0, rng_seed=seed * 7 + 42,
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
            mass_idx = [i for i in mid_indices if positions[i][1] > center_y + 0.5]
            if len(mass_idx) < 2:
                continue

            mass_cy = sum(positions[i][1] for i in mass_idx) / len(mass_idx)
            free_field_dag = [0.0] * len(positions)
            mass_field_dag = compute_field_on_dag(positions, adj, mass_idx)

            free_probs = launch_packet_dag_geom(
                positions, adj, free_field_dag, source_indices, detector_indices, k, 1.0)
            mass_probs = launch_packet_dag_geom(
                positions, adj, mass_field_dag, source_indices, detector_indices, k, 1.0)

            fcy = centroid_y_dag(free_probs, positions)
            mcy = centroid_y_dag(mass_probs, positions)
            shift = mcy - fcy
            shifts.append(shift)

            toward = mass_cy - center_y
            if (toward > 0 and shift > 0.05):
                attract += 1

        if shifts:
            mean = sum(shifts) / len(shifts)
            print(f"  {k:5.1f}  {attract:>5d}/{len(shifts):<2d}  {mean:+10.4f}")

    # ================================================================
    # TEST 3: k-averaged propagator — does summing over k-band help?
    # ================================================================
    print()
    print("=" * 80)
    print("TEST 3: k-averaged propagator (sum over k-band)")
    print("  Average probability over k in [k_low, k_high]")
    print("=" * 80)
    print()

    k_bands = [
        (0.5, 3.0, "low k"),
        (1.0, 6.0, "mid k"),
        (3.0, 9.0, "high k"),
        (0.5, 10.0, "full range"),
    ]

    for k_low, k_high, label in k_bands:
        k_steps = [k_low + (k_high - k_low) * i / 9 for i in range(10)]

        # Average probability distributions across k values
        avg_free = {y: 0.0 for y in screen_ys}
        avg_mass = {y: 0.0 for y in screen_ys}

        for k in k_steps:
            free_r = launch_packet_geom(nodes, source, free_field, k, 1.0, [25], screen_ys)
            mass_r = launch_packet_geom(nodes, source, mass_field, k, 1.0, [25], screen_ys)

            for y in screen_ys:
                avg_free[y] += free_r[25].get(y, 0)
                avg_mass[y] += mass_r[25].get(y, 0)

        # Normalize
        tf = sum(avg_free.values())
        tm = sum(avg_mass.values())
        if tf > 0:
            avg_free = {y: p / tf for y, p in avg_free.items()}
        if tm > 0:
            avg_mass = {y: p / tm for y, p in avg_mass.items()}

        fcy = sum(y * p for y, p in avg_free.items())
        mcy = sum(y * p for y, p in avg_mass.items())
        shift = mcy - fcy
        d = "ATTRACT" if shift > 0.3 else "REPEL" if shift < -0.3 else "~0"
        print(f"  k=[{k_low:.1f}, {k_high:.1f}] ({label:>10s}): shift = {shift:+.2f} ({d})")

    # ================================================================
    # TEST 4: Same k-averaging on generated DAGs
    # ================================================================
    print()
    print("TEST 4: k-averaged propagator on generated DAGs (5 seeds)")
    print()

    k_band = [0.5 + 0.5 * i for i in range(20)]  # 0.5 to 10.0

    attract = 0
    shifts = []

    for seed in range(8):
        positions, adj, arrival = generate_causal_dag(
            n_layers=12, nodes_per_layer=20,
            connect_radius=3.0, rng_seed=seed * 7 + 42,
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
        mass_idx = [i for i in mid_indices if positions[i][1] > center_y + 0.5]
        if len(mass_idx) < 2:
            continue

        mass_cy = sum(positions[i][1] for i in mass_idx) / len(mass_idx)
        free_field_dag = [0.0] * len(positions)
        mass_field_dag = compute_field_on_dag(positions, adj, mass_idx)

        # Average over k-band
        avg_free_cy = 0.0
        avg_mass_cy = 0.0
        n_k = 0

        for k in k_band:
            free_probs = launch_packet_dag_geom(
                positions, adj, free_field_dag, source_indices, detector_indices, k, 1.0)
            mass_probs = launch_packet_dag_geom(
                positions, adj, mass_field_dag, source_indices, detector_indices, k, 1.0)

            fcy = centroid_y_dag(free_probs, positions)
            mcy = centroid_y_dag(mass_probs, positions)
            avg_free_cy += fcy
            avg_mass_cy += mcy
            n_k += 1

        if n_k > 0:
            avg_free_cy /= n_k
            avg_mass_cy /= n_k
            shift = avg_mass_cy - avg_free_cy
            shifts.append(shift)

            toward = mass_cy - center_y
            if (toward > 0 and shift > 0.05):
                attract += 1

            print(f"  seed={seed}: k-avg shift = {shift:+.4f} "
                  f"({'ATTRACT' if toward > 0 and shift > 0.05 else 'repel/neutral'})")

    if shifts:
        print()
        print(f"  k-averaged: attract={attract}/{len(shifts)}, "
              f"mean={sum(shifts)/len(shifts):+.4f}")

    print()
    print("=" * 80)
    print("ANALYSIS")
    print("=" * 80)
    print()
    print("If lattice shows sharp resonances but DAGs show smooth k-dependence:")
    print("  → Resonances are lattice artifacts, DAGs give true behavior")
    print()
    print("If k-averaging produces robust attraction:")
    print("  → Wavepackets (which span a k-range) naturally attract")
    print("  → Single-k is unphysical; real packets have k-bandwidth")
    print()
    print("TEST COMPLETE")


if __name__ == "__main__":
    main()
