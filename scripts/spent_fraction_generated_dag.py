#!/usr/bin/env python3
"""Spent_fraction amplitude attraction on GENERATED causal DAGs.

The rectangular grid showed attraction. But does it survive on random
graphs without lattice symmetry? This tests whether gravitational
attraction is a robust emergent property or a lattice artifact.

Also investigates the counterintuitive mass-size dependence.

PStack experiment: spent-fraction-generated-dag
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


def compute_field_on_dag(positions, adj, mass_indices, iterations=50):
    """Discrete Laplacian relaxation on undirected adjacency.

    mass_indices have field=1.0 (fixed). Others relax to avg of neighbors.
    """
    n = len(positions)
    # Build undirected adjacency
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


def pathsum_spent_fraction(
    positions, adj, field, source_indices, detector_indices,
    phase_k=2.5, atten_power=0.5,
):
    """Propagate amplitude using spent_fraction action on a generated DAG.

    Returns: dict mapping detector index → probability
    """
    n = len(positions)

    # Topological order via in-degree
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

    # Initialize amplitude at source nodes
    amplitudes = [0.0 + 0.0j] * n
    for s in source_indices:
        amplitudes[s] = 1.0 / len(source_indices) + 0.0j

    # Propagate
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
            retained = math.sqrt(max(delay * delay - link_length * link_length, 0.0))

            action = (delay - retained) / delay if delay > 0 else 0.0
            edge_amp = cmath.exp(1j * phase_k * action) / (delay ** atten_power)
            amplitudes[j] += amp * edge_amp

    # Collect at detectors
    probs = {}
    for d in detector_indices:
        probs[d] = abs(amplitudes[d]) ** 2
    total = sum(probs.values())
    if total > 0:
        probs = {d: p / total for d, p in probs.items()}
    return probs


def centroid_y(probs, positions):
    """Probability-weighted mean y."""
    total = sum(probs.values())
    if total == 0:
        return 0.0
    return sum(positions[d][1] * p for d, p in probs.items()) / total


def main() -> None:
    n_layers = 12
    nodes_per_layer = 20
    connect_radius = 3.0
    n_seeds = 15
    phase_k = 2.5
    atten_power = 0.5

    print("=" * 80)
    print("SPENT FRACTION AMPLITUDE ATTRACTION ON GENERATED DAGs")
    print("=" * 80)
    print(f"DAG params: {n_layers} layers × {nodes_per_layer} nodes, radius={connect_radius}")
    print(f"Action: spent_fraction, k={phase_k}, atten_power={atten_power}")
    print(f"Seeds: {n_seeds}")
    print()

    # ================================================================
    # TEST 1: Does attraction exist on random DAGs?
    # ================================================================
    print("TEST 1: Mass above beam center — does amplitude shift toward?")
    print()

    attract_count = 0
    repel_count = 0
    neutral_count = 0
    shifts = []

    print(f"  {'seed':>4s}  {'free_cy':>8s}  {'mass_cy_pos':>11s}  {'det_cy':>8s}  {'shift':>8s}  {'toward?':>7s}")
    print(f"  {'-' * 54}")

    for seed in range(n_seeds):
        positions, adj, arrival = generate_causal_dag(
            n_layers=n_layers,
            nodes_per_layer=nodes_per_layer,
            connect_radius=connect_radius,
            rng_seed=seed * 7 + 42,
        )

        # Group by layer (x-coordinate)
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

        # Center y of all nodes
        all_ys = [y for _, y in positions]
        center_y = sum(all_ys) / len(all_ys)

        # Mass: nodes above center in middle layer
        mass_indices = [i for i in mid_indices if positions[i][1] > center_y + 0.5]
        if len(mass_indices) < 2:
            continue

        mass_cy = sum(positions[i][1] for i in mass_indices) / len(mass_indices)

        # Free field
        free_field = [0.0] * len(positions)
        free_probs = pathsum_spent_fraction(
            positions, adj, free_field, source_indices, detector_indices,
            phase_k, atten_power,
        )
        fcy = centroid_y(free_probs, positions)

        # Mass field
        mass_field = compute_field_on_dag(positions, adj, mass_indices)
        mass_probs = pathsum_spent_fraction(
            positions, adj, mass_field, source_indices, detector_indices,
            phase_k, atten_power,
        )
        mcy = centroid_y(mass_probs, positions)

        shift = mcy - fcy
        shifts.append(shift)

        toward_dir = mass_cy - center_y
        toward = "YES" if (toward_dir > 0 and shift > 0.05) or \
                          (toward_dir < 0 and shift < -0.05) else "no"

        if toward == "YES":
            attract_count += 1
        elif abs(shift) > 0.05:
            repel_count += 1
        else:
            neutral_count += 1

        print(f"  {seed:4d}  {fcy:8.2f}  {mass_cy:11.2f}  {mcy:8.2f}  {shift:+8.3f}  {toward:>7s}")

    print()
    print(f"  Attract: {attract_count}/{len(shifts)}, Repel: {repel_count}/{len(shifts)}, "
          f"Neutral: {neutral_count}/{len(shifts)}")
    if shifts:
        print(f"  Mean |shift|: {sum(abs(s) for s in shifts)/len(shifts):.4f}")
        pos_shifts = [s for s in shifts if s > 0.05]
        neg_shifts = [s for s in shifts if s < -0.05]
        print(f"  Mean positive shift: {sum(pos_shifts)/len(pos_shifts):.4f}" if pos_shifts else "")
        print(f"  Mean negative shift: {sum(neg_shifts)/len(neg_shifts):.4f}" if neg_shifts else "")

    # ================================================================
    # TEST 2: Mass BELOW center — does shift reverse?
    # ================================================================
    print()
    print("TEST 2: Mass above vs below — does shift flip?")
    print()

    above_shifts = []
    below_shifts = []

    print(f"  {'seed':>4s}  {'above_shift':>12s}  {'below_shift':>12s}  {'flips?':>6s}")
    print(f"  {'-' * 42}")

    for seed in range(n_seeds):
        positions, adj, arrival = generate_causal_dag(
            n_layers=n_layers,
            nodes_per_layer=nodes_per_layer,
            connect_radius=connect_radius,
            rng_seed=seed * 7 + 42,
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
        free_probs = pathsum_spent_fraction(
            positions, adj, free_field, source_indices, detector_indices,
            phase_k, atten_power,
        )
        fcy = centroid_y(free_probs, positions)

        # Above
        above_field = compute_field_on_dag(positions, adj, above)
        above_probs = pathsum_spent_fraction(
            positions, adj, above_field, source_indices, detector_indices,
            phase_k, atten_power,
        )
        a_shift = centroid_y(above_probs, positions) - fcy

        # Below
        below_field = compute_field_on_dag(positions, adj, below)
        below_probs = pathsum_spent_fraction(
            positions, adj, below_field, source_indices, detector_indices,
            phase_k, atten_power,
        )
        b_shift = centroid_y(below_probs, positions) - fcy

        above_shifts.append(a_shift)
        below_shifts.append(b_shift)

        flips = "YES" if (a_shift > 0.05 and b_shift < -0.05) or \
                         (a_shift < -0.05 and b_shift > 0.05) else "no"
        print(f"  {seed:4d}  {a_shift:+12.4f}  {b_shift:+12.4f}  {flips:>6s}")

    if above_shifts:
        print()
        flip_count = sum(1 for a, b in zip(above_shifts, below_shifts)
                        if (a > 0.05 and b < -0.05) or (a < -0.05 and b > 0.05))
        print(f"  Flips: {flip_count}/{len(above_shifts)}")
        print(f"  Mean above shift: {sum(above_shifts)/len(above_shifts):+.4f}")
        print(f"  Mean below shift: {sum(below_shifts)/len(below_shifts):+.4f}")

    # ================================================================
    # TEST 3: k sweep on generated DAGs
    # ================================================================
    print()
    print("TEST 3: k sweep on generated DAGs (5 seeds averaged)")
    print()

    print(f"  {'k':>6s}  {'mean_shift':>10s}  {'attract%':>9s}")
    print(f"  {'-' * 30}")

    for k in [0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 4.0, 6.0, 8.0]:
        k_shifts = []
        k_attract = 0
        k_valid = 0

        for seed in range(5):
            positions, adj, arrival = generate_causal_dag(
                n_layers=n_layers,
                nodes_per_layer=nodes_per_layer,
                connect_radius=connect_radius,
                rng_seed=seed * 7 + 42,
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
            free_probs = pathsum_spent_fraction(
                positions, adj, free_field, source_indices, detector_indices,
                k, atten_power,
            )
            mass_field = compute_field_on_dag(positions, adj, mass_indices)
            mass_probs = pathsum_spent_fraction(
                positions, adj, mass_field, source_indices, detector_indices,
                k, atten_power,
            )

            fcy = centroid_y(free_probs, positions)
            mcy = centroid_y(mass_probs, positions)
            shift = mcy - fcy
            k_shifts.append(shift)
            k_valid += 1

            toward_dir = mass_cy - center_y
            if (toward_dir > 0 and shift > 0.05):
                k_attract += 1

        if k_shifts:
            mean = sum(k_shifts) / len(k_shifts)
            pct = 100 * k_attract / k_valid if k_valid > 0 else 0
            print(f"  {k:6.1f}  {mean:+10.4f}  {pct:8.0f}%")

    # ================================================================
    # TEST 4: Mass-size investigation on rectangular grid
    # ================================================================
    print()
    print("=" * 80)
    print("TEST 4: Why does more mass = weaker attraction? (rectangular grid)")
    print("=" * 80)
    print()

    from toy_event_physics import (
        build_rectangular_nodes,
        derive_local_rule,
        derive_node_field,
        RulePostulates,
        infer_arrival_times_from_source,
        build_causal_dag,
    )

    width = 40
    height = 15
    grid_nodes = build_rectangular_nodes(width=width, height=height)
    grid_screen_ys = list(range(-height, height + 1))
    grid_source = (0, 0)
    grid_postulates = RulePostulates(phase_per_action=2.5, attenuation_power=0.5)
    grid_detector_xs = [15, 20, 25, 30]

    def launch_grid_packet(field):
        rule = derive_local_rule(persistent_nodes=frozenset(), postulates=grid_postulates)
        arrival_times = infer_arrival_times_from_source(grid_nodes, grid_source, rule)
        dag = build_causal_dag(grid_nodes, arrival_times)
        order = sorted(arrival_times, key=arrival_times.get)

        amplitudes = {grid_source: 1.0 + 0.0j}
        for node in order:
            if node not in amplitudes:
                continue
            amp = amplitudes[node]
            for nb in dag.get(node, []):
                link_length = math.dist(node, nb)
                local_field = 0.5 * (field.get(node, 0.0) + field.get(nb, 0.0))
                delay = link_length * (1.0 + local_field)
                retained = math.sqrt(max(delay * delay - link_length * link_length, 0.0))
                action = (delay - retained) / delay if delay > 0 else 0.0
                edge_amp = cmath.exp(1j * 2.5 * action) / (delay ** 0.5)
                if nb not in amplitudes:
                    amplitudes[nb] = 0.0 + 0.0j
                amplitudes[nb] += amp * edge_amp

        result = {}
        for dx in grid_detector_xs:
            dist = {}
            total = 0
            for y in grid_screen_ys:
                p = abs(amplitudes.get((dx, y), 0.0)) ** 2
                dist[y] = p
                total += p
            if total > 0:
                dist = {y: p / total for y, p in dist.items()}
            result[dx] = dist
        return result

    def cy(dist):
        total = sum(dist.values())
        if total == 0:
            return 0.0
        return sum(y * p for y, p in dist.items()) / total

    free_field = {n: 0.0 for n in grid_nodes}
    free_r = launch_grid_packet(free_field)

    # A: Fixed center, varying height
    print("  A) Fixed center y=6, varying column height:")
    print(f"    {'height':>8s}  {'n_nodes':>8s}  {'avg_shift':>10s}  {'field@src':>10s}  {'field@(20,0)':>12s}")
    print(f"    {'-' * 56}")

    for h in [1, 3, 5, 7, 9, 11]:
        half = h // 2
        mn = frozenset((20, y) for y in range(6 - half, 6 + half + 1))
        mr = derive_local_rule(persistent_nodes=mn, postulates=grid_postulates)
        mf = derive_node_field(grid_nodes, mr)
        mr_result = launch_grid_packet(mf)
        shifts = [cy(mr_result[dx]) - cy(free_r[dx]) for dx in grid_detector_xs]
        avg = sum(shifts) / len(shifts)
        f_src = mf.get(grid_source, 0.0)
        f_mid = mf.get((20, 0), 0.0)
        print(f"    {h:8d}  {len(mn):8d}  {avg:+10.2f}  {f_src:10.6f}  {f_mid:12.6f}")

    # B: Fixed size, varying distance
    print()
    print("  B) Fixed 5 nodes, varying distance from beam (y-center):")
    print(f"    {'y_center':>8s}  {'avg_shift':>10s}  {'field@(20,0)':>12s}  {'gradient':>10s}")
    print(f"    {'-' * 48}")

    for yc in [2, 4, 6, 8, 10, 12]:
        mn = frozenset((20, y) for y in range(yc - 2, yc + 3))
        mr = derive_local_rule(persistent_nodes=mn, postulates=grid_postulates)
        mf = derive_node_field(grid_nodes, mr)
        mr_result = launch_grid_packet(mf)
        shifts = [cy(mr_result[dx]) - cy(free_r[dx]) for dx in grid_detector_xs]
        avg = sum(shifts) / len(shifts)
        f_mid = mf.get((20, 0), 0.0)
        f_above = mf.get((20, 1), 0.0)
        f_below = mf.get((20, -1), 0.0)
        gradient = f_above - f_below
        print(f"    {yc:8d}  {avg:+10.2f}  {f_mid:12.6f}  {gradient:+10.6f}")

    print()
    print("TEST COMPLETE")


if __name__ == "__main__":
    main()
