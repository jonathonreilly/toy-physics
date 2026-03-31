#!/usr/bin/env python3
"""Definitive test: geometry-only attenuation restores gravitational attraction.

The insight chain:
1. Standard propagator: exp(ikS) / delay^p → REPELS (attenuation dominates)
2. Decoherence doesn't help: repulsion is from attenuation, not interference
3. (1+field)^p boost: attracts but UNSTABLE (exponential blow-up)
4. Fix: use exp(ikS) / L^p — attenuation depends only on geometry, not field

Physical motivation: In GR, the path integral measure √(-g) compensates
for the metric. Amplitude per unit proper time is constant. The field-
dependent attenuation 1/delay^p has no GR analog — it's an artifact.

Test: spent_delay action + geometry-only attenuation 1/L^p on both
rectangular grid and generated DAGs. Full characterization: distance
scaling, Born rule, flip test, stability.

PStack experiment: geometry-attenuation-definitive
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


def edge_amp_geom_atten(node, nb, node_field, phase_k, atten_power):
    """Edge amplitude: spent_delay action, geometry-only attenuation."""
    link_length = math.dist(node, nb) if isinstance(node, tuple) else 0
    local_field = 0.5 * (node_field.get(node, 0.0) + node_field.get(nb, 0.0)) \
                  if isinstance(node_field, dict) else \
                  0.5 * (node_field[node] + node_field[nb])
    delay = link_length * (1.0 + local_field)
    retained = math.sqrt(max(delay * delay - link_length * link_length, 0.0))
    action = delay - retained  # spent_delay

    # KEY CHANGE: attenuation uses L, not delay
    atten = 1.0 / (link_length ** atten_power) if link_length > 0 else 1.0
    return cmath.exp(1j * phase_k * action) * atten


def launch_packet_grid(
    nodes, source, node_field, phase_k, atten_power,
    detector_xs, screen_ys,
):
    """Launch amplitude packet on rectangular grid with geometry attenuation."""
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
            ea = edge_amp_geom_atten(node, nb, node_field, phase_k, atten_power)
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
    return result, amplitudes


def centroid_y_grid(distribution):
    total = sum(distribution.values())
    if total == 0:
        return 0.0
    return sum(y * p for y, p in distribution.items()) / total


def centroid_y_dag(probs, positions):
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


def launch_packet_dag(
    positions, adj, field, source_indices, detector_indices,
    phase_k, atten_power,
):
    """Launch amplitude packet on generated DAG with geometry attenuation."""
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
            local_field = 0.5 * (field[i] + field[j])
            delay = L * (1.0 + local_field)
            retained = math.sqrt(max(delay * delay - L * L, 0.0))
            action = delay - retained

            atten = 1.0 / (L ** atten_power) if L > 0 else 1.0
            edge_amp = cmath.exp(1j * phase_k * action) * atten
            amplitudes[j] += amp * edge_amp

    probs = {}
    for d in detector_indices:
        probs[d] = abs(amplitudes[d]) ** 2
    total = sum(probs.values())
    if total > 0:
        probs = {d: p / total for d, p in probs.items()}
    return probs


def main() -> None:
    width = 40
    height = 15
    nodes = build_rectangular_nodes(width=width, height=height)
    source = (0, 0)
    screen_ys = list(range(-height, height + 1))

    postulates_ref = RulePostulates(phase_per_action=4.0, attenuation_power=1.0)
    free_field = {n: 0.0 for n in nodes}

    mass_nodes = frozenset((20, y) for y in range(4, 9))
    mass_rule = derive_local_rule(persistent_nodes=mass_nodes, postulates=postulates_ref)
    mass_field = derive_node_field(nodes, mass_rule)

    print("=" * 80)
    print("GEOMETRY-ONLY ATTENUATION: Definitive attraction test")
    print("  Propagator: exp(i*k*S_spent) / L^p  (field ONLY in phase, not atten)")
    print("=" * 80)
    print()

    # ================================================================
    # TEST 1: k sweep on rectangular grid
    # ================================================================
    print("TEST 1: Phase wavenumber sweep — rectangular grid")
    print(f"  Mass at x=20, y=4..8. Attenuation power p=1.0")
    print()

    detector_xs = [15, 20, 25, 30, 35]
    print(f"  {'k':>6s}", end="")
    for dx in detector_xs:
        print(f"  {'@'+str(dx):>8s}", end="")
    print(f"  {'avg':>8s}  {'dir':>8s}")
    print(f"  {'-' * 60}")

    for k in [0.5, 1.0, 2.0, 3.0, 4.0, 6.0, 8.0, 12.0, 16.0]:
        free_r, _ = launch_packet_grid(
            nodes, source, free_field, k, 1.0, detector_xs, screen_ys)
        mass_r, _ = launch_packet_grid(
            nodes, source, mass_field, k, 1.0, detector_xs, screen_ys)
        shifts = [centroid_y_grid(mass_r[dx]) - centroid_y_grid(free_r[dx]) for dx in detector_xs]
        avg = sum(shifts) / len(shifts)
        d = "ATTRACT" if avg > 0.3 else "REPEL" if avg < -0.3 else "~0"
        print(f"  {k:6.1f}", end="")
        for s in shifts:
            print(f"  {s:+8.2f}", end="")
        print(f"  {avg:+8.2f}  {d:>8s}")

    # ================================================================
    # TEST 2: Stability check
    # ================================================================
    print()
    print("TEST 2: Amplitude stability (geometry attenuation)")
    print()

    _, free_amps = launch_packet_grid(
        nodes, source, free_field, 4.0, 1.0, [40], screen_ys)
    _, mass_amps = launch_packet_grid(
        nodes, source, mass_field, 4.0, 1.0, [40], screen_ys)

    max_free = max(abs(a) for a in free_amps.values())
    max_mass = max(abs(a) for a in mass_amps.values())
    print(f"  Max |amp| free: {max_free:.4e}")
    print(f"  Max |amp| mass: {max_mass:.4e}")
    print(f"  Ratio: {max_mass/max_free:.2f}")
    print(f"  Stable: {'YES' if max_mass/max_free < 100 else 'NO'}")

    # ================================================================
    # TEST 3: Distance falloff on rectangular grid
    # ================================================================
    print()
    print("TEST 3: Distance falloff — does attraction decrease with distance?")
    print(f"  k=4.0, p=1.0")
    print()

    detector_xs_dist = [20, 25, 30]
    print(f"  {'y_center':>8s}  {'avg_shift':>10s}")
    print(f"  {'-' * 22}")

    for yc in [2, 4, 6, 8, 10, 12]:
        mn = frozenset((20, y) for y in range(yc - 1, yc + 2))
        mr = derive_local_rule(persistent_nodes=mn, postulates=postulates_ref)
        mf = derive_node_field(nodes, mr)
        free_r, _ = launch_packet_grid(nodes, source, free_field, 4.0, 1.0, detector_xs_dist, screen_ys)
        mass_r, _ = launch_packet_grid(nodes, source, mf, 4.0, 1.0, detector_xs_dist, screen_ys)
        shifts = [centroid_y_grid(mass_r[dx]) - centroid_y_grid(free_r[dx]) for dx in detector_xs_dist]
        avg = sum(shifts) / len(shifts)
        print(f"  {yc:8d}  {avg:+10.3f}")

    # ================================================================
    # TEST 4: Flip test — mass above vs below
    # ================================================================
    print()
    print("TEST 4: Flip test (k=4.0, p=1.0)")
    print()

    mass_below = frozenset((20, y) for y in range(-8, -3))
    below_rule = derive_local_rule(persistent_nodes=mass_below, postulates=postulates_ref)
    below_field = derive_node_field(nodes, below_rule)

    free_r, _ = launch_packet_grid(nodes, source, free_field, 4.0, 1.0, detector_xs, screen_ys)
    above_r, _ = launch_packet_grid(nodes, source, mass_field, 4.0, 1.0, detector_xs, screen_ys)
    below_r, _ = launch_packet_grid(nodes, source, below_field, 4.0, 1.0, detector_xs, screen_ys)

    above_shifts = [centroid_y_grid(above_r[dx]) - centroid_y_grid(free_r[dx]) for dx in detector_xs]
    below_shifts = [centroid_y_grid(below_r[dx]) - centroid_y_grid(free_r[dx]) for dx in detector_xs]
    above_avg = sum(above_shifts) / len(above_shifts)
    below_avg = sum(below_shifts) / len(below_shifts)
    print(f"  Mass above: avg shift = {above_avg:+.2f}")
    print(f"  Mass below: avg shift = {below_avg:+.2f}")
    flips = (above_avg > 0.3 and below_avg < -0.3) or (above_avg < -0.3 and below_avg > 0.3)
    print(f"  Flips: {'YES' if flips else 'no'}")

    # ================================================================
    # TEST 5: Born rule (Sorkin I₃)
    # ================================================================
    print()
    print("TEST 5: Born rule — Sorkin I₃ with geometry attenuation")
    print()

    barrier_x = 20
    slit_ys_test = [-3, 3]
    det_x = 35

    def run_slits(open_slits, field, k=4.0, p=1.0):
        postulates = RulePostulates(phase_per_action=k, attenuation_power=p)
        rule = derive_local_rule(persistent_nodes=frozenset(), postulates=postulates)
        arrival_times = infer_arrival_times_from_source(nodes, source, rule)
        dag = build_causal_dag(nodes, arrival_times)
        order = sorted(arrival_times, key=arrival_times.get)

        blocked = set()
        for y in range(-height, height + 1):
            if (barrier_x, y) in nodes:
                is_slit = any(abs(y - sy) <= 1 for sy in open_slits)
                if not is_slit:
                    blocked.add((barrier_x, y))

        amplitudes = {source: 1.0 + 0.0j}
        for node in order:
            if node not in amplitudes or node in blocked:
                continue
            amp = amplitudes[node]
            for nb in dag.get(node, []):
                if nb in blocked:
                    continue
                ea = edge_amp_geom_atten(node, nb, field, k, p)
                if nb not in amplitudes:
                    amplitudes[nb] = 0.0 + 0.0j
                amplitudes[nb] += amp * ea

        return {y: abs(amplitudes.get((det_x, y), 0.0)) ** 2 for y in screen_ys}

    p_both = run_slits(slit_ys_test, free_field)
    p_a = run_slits([slit_ys_test[0]], free_field)
    p_b = run_slits([slit_ys_test[1]], free_field)
    p_none = run_slits([], free_field)

    max_i3 = max(abs(p_both.get(y, 0) - p_a.get(y, 0) - p_b.get(y, 0) + p_none.get(y, 0))
                 for y in screen_ys)
    max_p = max(max(p_both.values()), 1e-30)
    print(f"  Max |I₃|: {max_i3:.2e}")
    print(f"  Max P:    {max_p:.2e}")
    print(f"  |I₃|/P:  {max_i3/max_p:.2e}")
    print(f"  Born rule: {'PRESERVED' if max_i3/max_p < 1e-10 else 'VIOLATED'}")

    # ================================================================
    # TEST 6: Generated DAGs
    # ================================================================
    print()
    print("=" * 80)
    print("TEST 6: Generated DAGs — attraction with geometry attenuation")
    print("=" * 80)
    print()

    n_seeds = 12
    print(f"  {'k':>6s}  {'attract':>8s}  {'mean_shift':>10s}  {'flips':>6s}")
    print(f"  {'-' * 36}")

    for k in [1.0, 2.0, 3.0, 4.0, 6.0, 8.0]:
        attract = 0
        shifts = []
        flip_yes = 0
        flip_total = 0

        for seed in range(n_seeds):
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
            above = [i for i in mid_indices if positions[i][1] > center_y + 0.5]
            below = [i for i in mid_indices if positions[i][1] < center_y - 0.5]

            if len(above) < 2:
                continue

            mass_cy = sum(positions[i][1] for i in above) / len(above)

            free_field_dag = [0.0] * len(positions)
            free_probs = launch_packet_dag(
                positions, adj, free_field_dag, source_indices, detector_indices,
                k, 1.0,
            )
            fcy = centroid_y_dag(free_probs, positions)

            above_field = compute_field_on_dag(positions, adj, above)
            above_probs = launch_packet_dag(
                positions, adj, above_field, source_indices, detector_indices,
                k, 1.0,
            )
            acy = centroid_y_dag(above_probs, positions)
            shift = acy - fcy
            shifts.append(shift)

            toward_dir = mass_cy - center_y
            if (toward_dir > 0 and shift > 0.05):
                attract += 1

            # Flip test
            if len(below) >= 2:
                below_field = compute_field_on_dag(positions, adj, below)
                below_probs = launch_packet_dag(
                    positions, adj, below_field, source_indices, detector_indices,
                    k, 1.0,
                )
                bcy = centroid_y_dag(below_probs, positions)
                b_shift = bcy - fcy
                flip_total += 1
                if (shift > 0.05 and b_shift < -0.05) or (shift < -0.05 and b_shift > 0.05):
                    flip_yes += 1

        if shifts:
            mean = sum(shifts) / len(shifts)
            pct_attract = f"{attract}/{len(shifts)}"
            flip_str = f"{flip_yes}/{flip_total}" if flip_total > 0 else "n/a"
            print(f"  {k:6.1f}  {pct_attract:>8s}  {mean:+10.4f}  {flip_str:>6s}")

    # ================================================================
    # COMPARISON: Standard vs geometry attenuation on grid
    # ================================================================
    print()
    print("=" * 80)
    print("COMPARISON: Standard (1/delay^p) vs geometry (1/L^p) attenuation")
    print("  Same action (spent_delay), same k=4.0, same mass")
    print("=" * 80)
    print()

    for label, use_geom in [("1/delay^p (standard)", False), ("1/L^p (geometry)", True)]:
        if use_geom:
            free_r, _ = launch_packet_grid(
                nodes, source, free_field, 4.0, 1.0, detector_xs, screen_ys)
            mass_r, _ = launch_packet_grid(
                nodes, source, mass_field, 4.0, 1.0, detector_xs, screen_ys)
        else:
            # Standard attenuation: use the built-in propagator
            from toy_event_physics import local_edge_properties
            postulates = RulePostulates(phase_per_action=4.0, attenuation_power=1.0)
            rule = derive_local_rule(persistent_nodes=frozenset(), postulates=postulates)
            arrival_times = infer_arrival_times_from_source(nodes, source, rule)
            dag = build_causal_dag(nodes, arrival_times)
            order = sorted(arrival_times, key=arrival_times.get)

            def run_standard(field):
                amps = {source: 1.0 + 0.0j}
                for node in order:
                    if node not in amps:
                        continue
                    amp = amps[node]
                    for nb in dag.get(node, []):
                        L = math.dist(node, nb)
                        lf = 0.5 * (field.get(node, 0.0) + field.get(nb, 0.0))
                        dl = L * (1.0 + lf)
                        ret = math.sqrt(max(dl*dl - L*L, 0.0))
                        act = dl - ret
                        ea = cmath.exp(1j * 4.0 * act) / (dl ** 1.0)
                        if nb not in amps:
                            amps[nb] = 0.0 + 0.0j
                        amps[nb] += amp * ea
                result = {}
                for dx in detector_xs:
                    dist = {}
                    total = 0
                    for y in screen_ys:
                        p = abs(amps.get((dx, y), 0.0)) ** 2
                        dist[y] = p
                        total += p
                    if total > 0:
                        dist = {y: p / total for y, p in dist.items()}
                    result[dx] = dist
                return result

            free_r = run_standard(free_field)
            mass_r = run_standard(mass_field)

        shifts = [centroid_y_grid(mass_r[dx]) - centroid_y_grid(free_r[dx]) for dx in detector_xs]
        avg = sum(shifts) / len(shifts)
        d = "ATTRACT" if avg > 0.3 else "REPEL" if avg < -0.3 else "~0"
        print(f"  {label}: avg shift = {avg:+.2f} ({d})")

    print()
    print("=" * 80)
    print("CONCLUSION")
    print("=" * 80)
    print()
    print("Standard 1/delay^p attenuation: REPELS (attenuation dominates phase)")
    print("Geometry 1/L^p attenuation: removes field from denominator")
    print()
    print("If geometry attenuation → attraction: the phase structure (spent_delay")
    print("action) naturally produces gravitational attraction, but it's HIDDEN")
    print("by the unphysical field-dependent attenuation in the standard model.")
    print()
    print("Physical interpretation: the delay field should only affect PHASE")
    print("(like GR's metric affects geodesic equation), not AMPLITUDE MAGNITUDE")
    print("(which is set by the measure √(-g), compensating the metric).")
    print()
    print("TEST COMPLETE")


if __name__ == "__main__":
    main()
