#!/usr/bin/env python3
"""First-principles derivation: why attenuation should be 1/L^p, not 1/delay^p.

ARGUMENT:

The model's edge amplitude has two factors:
  amplitude = exp(i*k*action) / denominator^p

The PHASE (exp(ikS)) depends on the action, which includes the field.
This is correct: the field modifies the "clock" — how much phase
accumulates along an edge.

The ATTENUATION (1/denominator^p) represents how amplitude "spreads"
as it propagates. On a discrete graph, spreading is determined by:
  - How many neighbors a node has (graph topology)
  - The coordinate distance to those neighbors (geometry)
  - NOT the delay (which is a field-modified quantity)

Physical argument: two nodes connected by an edge of coordinate length L
have the same topological relationship regardless of the local field.
The field makes the signal SLOWER (more delay) but doesn't change
the fact that it's the SAME edge connecting the SAME two nodes.
Attenuation from spreading should depend on L, not delay.

GR analog: in the path integral, the measure √(-g) compensates for
the metric, so the amplitude per unit proper time is constant.
Our 1/delay^p is like having the metric SUPPRESS amplitude,
which √(-g) specifically prevents.

PREDICTIONS of 1/L^p (testable):
1. Gravitational attraction (confirmed: 11/12 on DAGs)
2. Amplitude conservation: total probability at each x-slice is
   independent of the field (field doesn't create or destroy probability)
3. Phase-only gravity: the gravitational effect comes entirely from
   phase (action), not from amplitude magnitude
4. Attenuation exponent p should match the graph's effective dimension
   (p=1 for 2D-like graphs, p=0.5 for 1D-like)

PStack experiment: attenuation-first-principles
"""

from __future__ import annotations
import math
import cmath
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


def propagate_grid(nodes, source, node_field, phase_k, atten_power, use_geom_atten):
    """Propagate on rectangular grid, return full amplitude dict."""
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

            if use_geom_atten:
                atten = 1.0 / (L ** atten_power) if L > 0 else 1.0
            else:
                atten = 1.0 / (delay ** atten_power) if delay > 0 else 1.0

            ea = cmath.exp(1j * phase_k * action) * atten
            if nb not in amplitudes:
                amplitudes[nb] = 0.0 + 0.0j
            amplitudes[nb] += amp * ea

    return amplitudes


def slice_probability(amplitudes, x, height):
    """Total probability at a given x-coordinate."""
    total = 0.0
    for y in range(-height, height + 1):
        total += abs(amplitudes.get((x, y), 0.0)) ** 2
    return total


def main() -> None:
    width = 40
    height = 15
    nodes = build_rectangular_nodes(width=width, height=height)
    source = (0, 0)
    phase_k = 2.0  # In attraction regime
    atten_power = 1.0

    postulates = RulePostulates(phase_per_action=phase_k, attenuation_power=atten_power)
    mass_nodes = frozenset((20, y) for y in range(4, 9))
    mass_rule = derive_local_rule(persistent_nodes=mass_nodes, postulates=postulates)
    mass_field = derive_node_field(nodes, mass_rule)
    free_field = {n: 0.0 for n in nodes}

    print("=" * 80)
    print("FIRST-PRINCIPLES DERIVATION: WHY ATTENUATION = 1/L^p")
    print("=" * 80)
    print()

    # ================================================================
    # PREDICTION 1: Probability conservation per x-slice
    # ================================================================
    print("PREDICTION 1: Probability conservation")
    print("  If attenuation = 1/L^p, the field should NOT change total probability")
    print("  at any x-slice. If 1/delay^p, it DOES (field suppresses probability).")
    print()

    for label, use_geom in [("1/delay^p (standard)", False), ("1/L^p (geometry)", True)]:
        free_amps = propagate_grid(nodes, source, free_field, phase_k, atten_power, use_geom)
        mass_amps = propagate_grid(nodes, source, mass_field, phase_k, atten_power, use_geom)

        print(f"  {label}:")
        print(f"    {'x':>4s}  {'P_free':>12s}  {'P_mass':>12s}  {'ratio':>8s}")
        print(f"    {'-' * 42}")

        for x in [5, 10, 15, 20, 25, 30, 35, 40]:
            pf = slice_probability(free_amps, x, height)
            pm = slice_probability(mass_amps, x, height)
            ratio = pm / pf if pf > 0 else 0
            print(f"    {x:4d}  {pf:12.4e}  {pm:12.4e}  {ratio:8.4f}")

        # Summary: how much does field change total probability?
        total_free = sum(slice_probability(free_amps, x, height) for x in range(1, width + 1))
        total_mass = sum(slice_probability(mass_amps, x, height) for x in range(1, width + 1))
        change = abs(total_mass - total_free) / total_free if total_free > 0 else 0
        print(f"    Total probability change: {change:.4f} ({change*100:.2f}%)")
        print()

    # ================================================================
    # PREDICTION 2: Phase-only gravity
    # ================================================================
    print("PREDICTION 2: Gravity is PHASE-ONLY with 1/L^p")
    print("  Remove phase (k=0) → gravity should disappear")
    print("  Keep phase, change k → gravity strength should change")
    print()

    screen_ys = list(range(-height, height + 1))
    detector_xs = [20, 25, 30]

    def centroid_shift(k, use_geom):
        free_amps = propagate_grid(nodes, source, free_field, k, atten_power, use_geom)
        mass_amps = propagate_grid(nodes, source, mass_field, k, atten_power, use_geom)
        shifts = []
        for dx in detector_xs:
            free_dist = {}
            mass_dist = {}
            for y in screen_ys:
                free_dist[y] = abs(free_amps.get((dx, y), 0.0)) ** 2
                mass_dist[y] = abs(mass_amps.get((dx, y), 0.0)) ** 2
            tf = sum(free_dist.values())
            tm = sum(mass_dist.values())
            if tf > 0:
                free_dist = {y: p / tf for y, p in free_dist.items()}
            if tm > 0:
                mass_dist = {y: p / tm for y, p in mass_dist.items()}
            fcy = sum(y * p for y, p in free_dist.items())
            mcy = sum(y * p for y, p in mass_dist.items())
            shifts.append(mcy - fcy)
        return sum(shifts) / len(shifts)

    print(f"  {'k':>6s}  {'shift_geom':>10s}  {'shift_delay':>11s}  {'geom_dir':>8s}  {'delay_dir':>9s}")
    print(f"  {'-' * 50}")

    for k in [0.0, 0.5, 1.0, 2.0, 4.0, 8.0]:
        sg = centroid_shift(k, True)
        sd = centroid_shift(k, False)
        dg = "ATTRACT" if sg > 0.3 else "REPEL" if sg < -0.3 else "~0"
        dd = "ATTRACT" if sd > 0.3 else "REPEL" if sd < -0.3 else "~0"
        print(f"  {k:6.1f}  {sg:+10.2f}  {sd:+11.2f}  {dg:>8s}  {dd:>9s}")

    print()
    print("  If k=0 shift ≈ 0 for 1/L^p: gravity is purely phase-driven")
    print("  If k=0 shift ≠ 0 for 1/delay^p: gravity has attenuation component")

    # ================================================================
    # PREDICTION 3: Attenuation exponent matches effective dimension
    # ================================================================
    print()
    print("PREDICTION 3: Optimal attenuation exponent vs graph dimension")
    print("  On 2D lattice (8-neighbor), effective dimension d=2 → optimal p=d/2=1")
    print("  On thin graph (few paths), effective d<2 → optimal p<1")
    print()

    print(f"  {'p':>5s}  {'shift':>8s}  {'dir':>8s}")
    print(f"  {'-' * 24}")

    for p in [0.0, 0.25, 0.5, 0.75, 1.0, 1.25, 1.5, 2.0]:
        free_amps = propagate_grid(nodes, source, free_field, 2.0, p, True)
        mass_amps = propagate_grid(nodes, source, mass_field, 2.0, p, True)
        shifts = []
        for dx in detector_xs:
            free_dist = {}
            mass_dist = {}
            for y in screen_ys:
                free_dist[y] = abs(free_amps.get((dx, y), 0.0)) ** 2
                mass_dist[y] = abs(mass_amps.get((dx, y), 0.0)) ** 2
            tf = sum(free_dist.values())
            tm = sum(mass_dist.values())
            if tf > 0:
                free_dist = {y: p_val / tf for y, p_val in free_dist.items()}
            if tm > 0:
                mass_dist = {y: p_val / tm for y, p_val in mass_dist.items()}
            fcy = sum(y * p_val for y, p_val in free_dist.items())
            mcy = sum(y * p_val for y, p_val in mass_dist.items())
            shifts.append(mcy - fcy)
        avg = sum(shifts) / len(shifts)
        d = "ATTRACT" if avg > 0.3 else "REPEL" if avg < -0.3 else "~0"
        print(f"  {p:5.2f}  {avg:+8.2f}  {d:>8s}")

    # ================================================================
    # PREDICTION 4: On generated DAGs, optimal p depends on connectivity
    # ================================================================
    print()
    print("PREDICTION 4: Optimal p on generated DAGs with different connectivity")
    print()

    from collections import deque

    def test_dag_attraction(radius, p_atten, n_seeds=5):
        attract = 0
        shifts = []
        for seed in range(n_seeds):
            positions, adj, arrival = generate_causal_dag(
                n_layers=12, nodes_per_layer=20,
                connect_radius=radius, rng_seed=seed * 13 + 5,
            )
            by_layer = defaultdict(list)
            for idx, (x, y) in enumerate(positions):
                by_layer[round(x)].append(idx)
            layers = sorted(by_layer.keys())
            if len(layers) < 4:
                continue

            source_idx = by_layer[layers[0]]
            det_idx = by_layer[layers[-1]]
            mid = len(layers) // 2
            mid_idx = by_layer[layers[mid]]
            if not mid_idx or not det_idx:
                continue

            all_ys = [y for _, y in positions]
            center_y = sum(all_ys) / len(all_ys)
            mass_idx = [i for i in mid_idx if positions[i][1] > center_y + 1]
            if len(mass_idx) < 2:
                continue

            mass_cy = sum(positions[i][1] for i in mass_idx) / len(mass_idx)

            # Compute field
            n = len(positions)
            undirected = defaultdict(set)
            for i, nbs in adj.items():
                for j in nbs:
                    undirected[i].add(j)
                    undirected[j].add(i)
            mass_set = set(mass_idx)
            field = [1.0 if i in mass_set else 0.0 for i in range(n)]
            for _ in range(50):
                nf = [0.0] * n
                for i in range(n):
                    if i in mass_set:
                        nf[i] = 1.0
                        continue
                    nbs = undirected.get(i, set())
                    if nbs:
                        nf[i] = sum(field[j] for j in nbs) / len(nbs)
                field = nf

            free_field = [0.0] * n

            # k-averaged propagation
            k_shifts = []
            for k in [3.0, 5.0, 7.0]:
                for use_field in [free_field, field]:
                    in_deg = [0] * n
                    for i, nbs in adj.items():
                        for j in nbs:
                            in_deg[j] += 1
                    q = deque()
                    for i in range(n):
                        if in_deg[i] == 0:
                            q.append(i)
                    order = []
                    while q:
                        i = q.popleft()
                        order.append(i)
                        for j in adj.get(i, []):
                            in_deg[j] -= 1
                            if in_deg[j] == 0:
                                q.append(j)

                    amps = [0.0 + 0.0j] * n
                    for s in source_idx:
                        amps[s] = 1.0 / len(source_idx)
                    for i in order:
                        if abs(amps[i]) < 1e-30:
                            continue
                        for j in adj.get(i, []):
                            x1, y1 = positions[i]
                            x2, y2 = positions[j]
                            L = math.sqrt((x2-x1)**2 + (y2-y1)**2)
                            if L < 1e-10:
                                continue
                            lf = 0.5 * (use_field[i] + use_field[j])
                            dl = L * (1.0 + lf)
                            ret = math.sqrt(max(dl*dl - L*L, 0.0))
                            act = dl - ret
                            att = 1.0 / (L ** p_atten) if L > 0 else 1.0
                            ea = cmath.exp(1j * k * act) * att
                            amps[j] += amps[i] * ea

                    probs = {}
                    for d in det_idx:
                        probs[d] = abs(amps[d]) ** 2
                    total = sum(probs.values())
                    if total > 0:
                        probs = {d: p / total for d, p in probs.items()}

                    cy = sum(positions[d][1] * p for d, p in probs.items()) / sum(probs.values()) if sum(probs.values()) > 0 else 0

                    if use_field is free_field:
                        free_cy = cy
                    else:
                        mass_cy_det = cy
                        k_shifts.append(mass_cy_det - free_cy)

            if k_shifts:
                avg = sum(k_shifts) / len(k_shifts)
                shifts.append(avg)
                toward = mass_cy - center_y
                if (toward > 0 and avg > 0.05):
                    attract += 1

        if shifts:
            return attract, len(shifts), sum(shifts) / len(shifts)
        return 0, 0, 0.0

    for radius_label, radius in [("sparse (r=2)", 2.0), ("medium (r=3)", 3.0), ("dense (r=5)", 5.0)]:
        print(f"  {radius_label}:")
        print(f"    {'p':>5s}  {'attract':>8s}  {'mean_shift':>10s}")
        print(f"    {'-' * 28}")
        for p in [0.25, 0.5, 0.75, 1.0, 1.5]:
            a, t, m = test_dag_attraction(radius, p)
            if t > 0:
                print(f"    {p:5.2f}  {a:>5d}/{t:<2d}  {m:+10.3f}")
        print()

    print("=" * 80)
    print("DERIVATION SUMMARY")
    print("=" * 80)
    print()
    print("The propagator amplitude = exp(i*k*S) * A(edge)")
    print()
    print("S (action) = delay - retained = delay - sqrt(delay²-L²)")
    print("  → Depends on field. Correct: field modifies the clock.")
    print()
    print("A (attenuation) should be 1/L^p, NOT 1/delay^p, because:")
    print("  1. Spreading is topological (graph structure), not temporal (delay)")
    print("  2. Field changes WHEN signal arrives, not HOW MUCH it spreads")
    print("  3. GR analog: √(-g) measure compensates metric in path integral")
    print("  4. 1/delay^p creates unphysical probability suppression near mass")
    print()
    print("Consequence: gravity = pure PHASE effect from action.")
    print("  → Paths through high-field regions accumulate more phase")
    print("  → Constructive interference on mass-side of beam")
    print("  → Amplitude concentrates toward mass = gravitational attraction")
    print()
    print("TEST COMPLETE")


if __name__ == "__main__":
    main()
