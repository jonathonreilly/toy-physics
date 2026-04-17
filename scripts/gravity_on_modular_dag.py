#!/usr/bin/env python3
"""Test gravity on modular vs uniform DAGs.

Question: does the corrected propagator (1/L^p, directional measure,
phase valley) still produce gravitational attraction on modular DAGs?

The modular DAG has a y-gap that separates channels. Gravity requires
paths near mass to accumulate more phase (phase valley mechanism).
Does the channel structure interfere with gravitational deflection?

Test: place mass at y>0, propagate from source, measure mean y at
detectors. Positive mean y = deflection toward mass = gravity works.

Compare:
  1. Uniform random DAG (baseline — gravity known to work)
  2. Modular DAG (does gravity survive channel separation?)
"""

from __future__ import annotations
import math
import cmath
import sys
import os
from collections import defaultdict, deque

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.generative_causal_dag_interference import generate_causal_dag
from scripts.topology_families import generate_modular_dag

BETA = 0.8


def _topo_order(adj, n):
    in_deg = [0] * n
    for nbs in adj.values():
        for j in nbs:
            in_deg[j] += 1
    q = deque(i for i in range(n) if in_deg[i] == 0)
    order = []
    while q:
        i = q.popleft()
        order.append(i)
        for j in adj.get(i, []):
            in_deg[j] -= 1
            if in_deg[j] == 0:
                q.append(j)
    return order


def compute_field(positions, mass_nodes, strength=0.1):
    """Gravitational field from mass nodes: f(i) = sum_m strength / r."""
    n = len(positions)
    field = [0.0] * n
    for m in mass_nodes:
        mx, my = positions[m]
        for i in range(n):
            ix, iy = positions[i]
            r = math.sqrt((ix - mx) ** 2 + (iy - my) ** 2) + 0.1
            field[i] += strength / r
    return field


def propagate(positions, adj, field, src, k, blocked=None):
    """Standard corrected propagator: 1/L, directional beta, field-dependent action."""
    n = len(positions)
    blocked = blocked or set()
    order = _topo_order(adj, n)
    amps = [0j] * n
    for s in src:
        amps[s] = 1.0 / len(src)
    for i in order:
        if abs(amps[i]) < 1e-30 or i in blocked:
            continue
        for j in adj.get(i, []):
            if j in blocked:
                continue
            x1, y1 = positions[i]
            x2, y2 = positions[j]
            dx, dy = x2 - x1, y2 - y1
            L = math.sqrt(dx * dx + dy * dy)
            if L < 1e-10:
                continue
            lf = 0.5 * (field[i] + field[j])
            dl = L * (1 + lf)
            ret = math.sqrt(max(dl * dl - L * L, 0))
            act = dl - ret
            theta = math.atan2(abs(dy), max(dx, 1e-10))
            w = math.exp(-BETA * theta * theta)
            ea = cmath.exp(1j * k * act) * w / L
            amps[j] += amps[i] * ea
    return amps


def measure_deflection(positions, amps, det_list):
    """Measure amplitude-weighted mean y at detectors.

    Positive = deflection toward positive y (toward mass if mass is at y>0).
    Also returns total probability at detectors.
    """
    total_prob = 0.0
    weighted_y = 0.0
    for d in det_list:
        p = abs(amps[d]) ** 2
        total_prob += p
        weighted_y += p * positions[d][1]

    if total_prob < 1e-30:
        return 0.0, 0.0

    mean_y = weighted_y / total_prob
    return mean_y, total_prob


def test_gravity(name, generator, n_layers_list, n_seeds=8, **gen_kwargs):
    """Test gravitational deflection on a graph family."""
    k_band = [3.0, 5.0, 7.0]

    for nl in n_layers_list:
        # Collect PER-SEED paired deltas (average over k within each seed)
        per_seed_deltas = []

        for seed in range(n_seeds):
            positions, adj, _ = generator(
                n_layers=nl, nodes_per_layer=25, y_range=12.0,
                connect_radius=3.0, rng_seed=seed * 13 + 5, **gen_kwargs,
            )

            # Setup
            by_layer = defaultdict(list)
            for idx, (x, y) in enumerate(positions):
                by_layer[round(x)].append(idx)
            layers = sorted(by_layer.keys())
            if len(layers) < 7:
                continue

            src = by_layer[layers[0]]
            det_list = list(by_layer[layers[-1]])
            if not det_list:
                continue

            all_ys = [y for _, y in positions]
            cy = sum(all_ys) / len(all_ys)

            # Mass at y > 0, around 2/3 depth
            grav_layer = layers[2 * len(layers) // 3]
            mass_nodes = [i for i in by_layer[grav_layer] if positions[i][1] > cy + 1]

            if not mass_nodes:
                continue

            # Propagate WITH mass field
            field_with = compute_field(positions, mass_nodes, strength=0.1)
            # Propagate WITHOUT mass (flat field)
            field_without = [0.0] * len(positions)

            # Average delta over k-band WITHIN this seed
            seed_deltas = []
            for k in k_band:
                amps_with = propagate(positions, adj, field_with, src, k)
                amps_without = propagate(positions, adj, field_without, src, k)

                y_with, _ = measure_deflection(positions, amps_with, det_list)
                y_without, _ = measure_deflection(positions, amps_without, det_list)

                seed_deltas.append(y_with - y_without)

            if seed_deltas:
                per_seed_deltas.append(sum(seed_deltas) / len(seed_deltas))

        if per_seed_deltas:
            n_ok = len(per_seed_deltas)
            delta = sum(per_seed_deltas) / n_ok
            se = (sum((d - delta) ** 2 for d in per_seed_deltas) / n_ok) ** 0.5 / math.sqrt(n_ok)

            status = "GRAVITY" if delta > 2 * se and delta > 0 else "FLAT" if abs(delta) < se else "REPULSION?"
            print(f"  {nl:4d}  {delta:+8.4f}  {se:6.4f}  {n_ok:4d}  {status}")
        else:
            print(f"  {nl:4d}  FAIL")


def main():
    print("=" * 74)
    print("GRAVITY ON MODULAR DAG")
    print("  Does the corrected propagator produce gravitational deflection")
    print("  on modular DAGs with channel separation?")
    print(f"  Mass at y>0 (layer 2/3), k-band [3,5,7], 8 seeds")
    print("=" * 74)
    print()

    n_layers_list = [12, 18, 25, 40]

    families = [
        ("Uniform random", generate_causal_dag, {}),
        ("Modular gap=4.0", generate_modular_dag, {"gap": 4.0}),
        ("Modular gap=2.0", generate_modular_dag, {"gap": 2.0}),
    ]

    for name, gen, kwargs in families:
        print(f"  [{name}]")
        print(f"  {'N':>4s}  {'delta':>8s}  {'SE':>6s}  {'n':>4s}  {'verdict'}")
        print(f"  {'':>4s}  (paired per-seed, k-band averaged)")
        print(f"  {'-' * 36}")
        test_gravity(name, gen, n_layers_list, **kwargs)
        print()

    print("delta > 0 with delta > 2*SE = gravitational attraction toward mass")
    print("GRAVITY = corrected propagator works on this topology")
    print("FLAT = no deflection detected")


if __name__ == "__main__":
    main()
