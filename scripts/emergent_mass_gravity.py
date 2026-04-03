#!/usr/bin/env python3
"""Emergent mass: amplitude concentration as gravitational source.

Axiom 2: "Stable objects are persistent self-maintaining patterns."
In the path-sum framework, a "pattern" is a region where amplitude
concentrates. This concentration creates a natural mass source.

The test: on a grown geometric DAG:
1. Propagate amplitude from source with NO field
2. Identify nodes where |amplitude|² is highest (the "pattern")
3. Use those nodes as mass sources for a SECOND propagation
4. Measure whether the second propagation deflects toward the pattern

If yes: gravity is self-sourced — amplitude concentration creates
its own gravitational field, which in turn focuses more amplitude.
This is the discrete analogue of "mass tells spacetime how to curve,
spacetime tells mass how to move."

The growth rule provides the geometry (Axioms 1, 3, 6).
The path-sum provides the dynamics (propagator).
The amplitude concentration provides the mass (Axiom 2).
Gravity emerges from the phase valley in the mass-sourced field (Axiom 8).
"""

from __future__ import annotations
import math
import cmath
import random as rng_mod
from collections import defaultdict, deque

BETA = 0.8


def grow_geometric_dag(n_layers=20, npl=25, d_growth=3,
                        connect_radius=3.0, spread=1.0, rng_seed=42):
    """Same as geometric_growth.py — local geometric DAG."""
    rng = rng_mod.Random(rng_seed)
    positions = []
    adj = defaultdict(list)
    layer_indices = []

    for layer in range(n_layers):
        x = float(layer)
        layer_nodes = []
        if layer == 0:
            pos = [x] + [0.0] * d_growth
            positions.append(tuple(pos))
            layer_nodes.append(0)
        else:
            prev_nodes = []
            for pl in layer_indices[max(0, layer - 2):]:
                prev_nodes.extend(pl)
            for _ in range(npl):
                parent = rng.choice(prev_nodes)
                pp = positions[parent]
                pos = [x]
                for d in range(d_growth):
                    pos.append(pp[1 + d] + rng.gauss(0, spread))
                pos = tuple(pos)
                idx = len(positions)
                positions.append(pos)
                layer_nodes.append(idx)
                for prev_idx in prev_nodes:
                    ppos = positions[prev_idx]
                    dist = math.sqrt(sum((a - b) ** 2 for a, b in zip(pos, ppos)))
                    if dist <= connect_radius:
                        adj[prev_idx].append(idx)
        layer_indices.append(layer_nodes)

    return positions, dict(adj)


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


def propagate(positions, adj, field, src, k, blocked=None):
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
            ip, jp = positions[i], positions[j]
            dsq = sum((a - b) ** 2 for a, b in zip(ip, jp))
            L = math.sqrt(dsq)
            if L < 1e-10:
                continue
            lf = 0.5 * (field[i] + field[j])
            dl = L * (1 + lf)
            ret = math.sqrt(max(dl * dl - L * L, 0))
            act = dl - ret
            dx = jp[0] - ip[0]
            trans = math.sqrt(dsq - dx * dx)
            theta = math.atan2(trans, max(dx, 1e-10))
            w = math.exp(-BETA * theta * theta)
            ea = cmath.exp(1j * k * act) * w / L
            amps[j] += amps[i] * ea
    return amps


def compute_field_from_nodes(positions, mass_nodes, strength=0.3):
    n = len(positions)
    field = [0.0] * n
    for m in mass_nodes:
        mp = positions[m]
        for i in range(n):
            ip = positions[i]
            r = math.sqrt(sum((a - b) ** 2 for a, b in zip(ip, mp))) + 0.1
            field[i] += strength / r
    return field


def run_emergent_mass_test(nl, d_growth, seed, strength=0.3):
    """Full emergent mass test on one grown graph.

    1. Grow geometric DAG
    2. Propagate with no field → find amplitude concentration
    3. Use concentrated nodes as mass → compute field
    4. Propagate WITH field → measure deflection
    5. Compare deflection to no-field propagation
    """
    positions, adj = grow_geometric_dag(nl, 25, d_growth, 3.0, 1.0, seed)
    n = len(positions)

    by_layer = defaultdict(list)
    for idx in range(n):
        by_layer[round(positions[idx][0])].append(idx)
    layers = sorted(by_layer.keys())
    if len(layers) < 7:
        return None

    src = by_layer[layers[0]]
    det_list = list(by_layer[layers[-1]])
    if not det_list:
        return None

    bl_idx = len(layers) // 3
    bi = by_layer[layers[bl_idx]]
    cy = sum(positions[i][1] for i in bi) / len(bi) if bi else 0
    sa = sorted(bi, key=lambda i: -positions[i][1])[:3]
    sb = sorted(bi, key=lambda i: positions[i][1])[:3]
    if set(sa) & set(sb):
        return None
    blocked = set(bi) - set(sa + sb)

    # Step 1: propagate with no field to find amplitude concentration
    flat_field = [0.0] * n
    k = 5.0
    amps_free = propagate(positions, adj, flat_field, src, k, blocked)

    # Step 2: identify mass nodes — top 10% amplitude in mid-graph layers
    mid_start = len(layers) // 2
    mid_end = min(len(layers) - 1, mid_start + 5)
    mid_nodes = []
    for layer in layers[mid_start:mid_end]:
        mid_nodes.extend(by_layer[layer])

    if not mid_nodes:
        return None

    amp_sq = [(i, abs(amps_free[i]) ** 2) for i in mid_nodes]
    amp_sq.sort(key=lambda x: -x[1])
    n_mass = max(1, len(amp_sq) // 10)  # top 10%
    mass_nodes = [i for i, _ in amp_sq[:n_mass]]

    if not mass_nodes:
        return None

    # Record mass centroid position (y-coordinate)
    mass_y = sum(positions[m][1] for m in mass_nodes) / len(mass_nodes)

    # Step 3: compute field from emergent mass
    field = compute_field_from_nodes(positions, mass_nodes, strength)

    # Step 4: propagate WITH field, measure deflection
    results = {}
    for k in [3.0, 5.0, 7.0]:
        amps_mass = propagate(positions, adj, field, src, k, blocked)
        amps_flat = propagate(positions, adj, flat_field, src, k, blocked)

        pm = sum(abs(amps_mass[d]) ** 2 for d in det_list)
        pf = sum(abs(amps_flat[d]) ** 2 for d in det_list)
        if pm > 1e-30 and pf > 1e-30:
            ym = sum(abs(amps_mass[d]) ** 2 * positions[d][1] for d in det_list) / pm
            yf = sum(abs(amps_flat[d]) ** 2 * positions[d][1] for d in det_list) / pf
            delta = ym - yf
            # Check: is deflection TOWARD the mass?
            toward_mass = (delta > 0 and mass_y > cy) or (delta < 0 and mass_y < cy)
            results[k] = {"delta": delta, "toward": toward_mass, "mass_y": mass_y}

    if not results:
        return None

    deltas = [r["delta"] for r in results.values()]
    toward = [r["toward"] for r in results.values()]
    avg_delta = sum(deltas) / len(deltas)
    frac_toward = sum(toward) / len(toward)

    return {
        "delta": avg_delta,
        "toward_frac": frac_toward,
        "mass_y": mass_y,
        "n_mass": len(mass_nodes),
    }


def main():
    import time

    print("=" * 70)
    print("EMERGENT MASS: Amplitude Concentration as Gravitational Source")
    print("  Axiom 2: persistent pattern = mass")
    print("  Does amplitude-sourced gravity produce deflection?")
    print("=" * 70)
    print()

    n_seeds = 16

    for d_growth in [1, 2, 3]:
        print(f"  [d_growth={d_growth} ({d_growth+1}D)]")
        print(f"  {'N':>4s}  {'delta':>8s}  {'toward':>7s}  {'mass_y':>7s}  "
              f"{'n_mass':>6s}  {'n_ok':>4s}")
        print(f"  {'-' * 46}")

        for nl in [18, 25, 30]:
            t0 = time.time()
            delta_all, toward_all = [], []
            for seed_i in range(n_seeds):
                seed = seed_i * 7 + 3
                r = run_emergent_mass_test(nl, d_growth, seed, strength=0.3)
                if r:
                    delta_all.append(r["delta"])
                    toward_all.append(r["toward_frac"])

            dt = time.time() - t0
            if delta_all:
                n_ok = len(delta_all)
                ad = sum(delta_all) / n_ok
                se = (sum((d - ad) ** 2 for d in delta_all) / n_ok) ** 0.5 / math.sqrt(n_ok)
                at = sum(toward_all) / n_ok
                ratio = ad / se if se > 0 else 0
                print(f"  {nl:4d}  {ad:+8.4f}  {at:7.1%}  {'':>7s}  "
                      f"{'':>6s}  {n_ok:4d}  (d/SE={ratio:+.1f})")
            else:
                print(f"  {nl:4d}  FAIL")
            import sys
            sys.stdout.flush()
        print()

    print("toward > 50%: amplitude-sourced gravity deflects TOWARD the pattern")
    print("This would close Axiom 2: persistent pattern = mass source")


if __name__ == "__main__":
    main()
