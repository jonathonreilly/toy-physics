#!/usr/bin/env python3
"""Geometric growth: local rules that respect spatial locality.

Random growth fails because graph dimension ≠ spatial dimension.
The path-sum needs GEOMETRIC locality: edges connect nearby nodes.

This script tests growth rules that use the graph's own structure
to decide where new nodes connect — Axiom 3 compliant.

Rule: DELAY-BASED GEOMETRIC GROWTH
  1. Start with a seed graph (small lattice-like structure)
  2. New nodes are placed at positions inferred from their
     intended parents' positions (local continuation, Axiom 6)
  3. Edges connect to nodes within a fixed radius in the
     INFERRED coordinate system
  4. The coordinate system is the graph's own delay field,
     not an externally imposed space

This should produce a graph that:
  - Has geometric locality (edges = spatial neighbors)
  - Grows organically (no imposed grid)
  - Has effective spatial dimension determined by the growth rule
  - Supports path-sum propagation with decoherence

The key parameter: how many dimensions the growth rule "discovers."
If new nodes can spread in d directions from their parents, the
effective spatial dimension should be d.
"""

from __future__ import annotations
import math
import cmath
import random as rng_mod
from collections import defaultdict, deque


BETA = 0.8


def grow_geometric_dag(n_layers=20, npl=25, d_growth=3,
                        connect_radius=3.0, spread=1.0, rng_seed=42):
    """Grow a geometric DAG where positions emerge from the growth rule.

    d_growth: number of transverse dimensions in which new nodes spread.
    Each new node's position = parent's position + small random offset
    in d_growth dimensions.

    This is Axiom 3 + Axiom 6: space is inferred from the growth
    pattern, and each step is a locally simple continuation.
    """
    rng = rng_mod.Random(rng_seed)
    positions = []  # (x, y1, y2, ..., y_d_growth)
    adj = defaultdict(list)
    layer_indices = []

    for layer in range(n_layers):
        x = float(layer)
        layer_nodes = []

        if layer == 0:
            # Seed: single node at origin
            pos = [x] + [0.0] * d_growth
            positions.append(tuple(pos))
            layer_nodes.append(0)
        else:
            prev_nodes = []
            for pl in layer_indices[max(0, layer - 2):]:
                prev_nodes.extend(pl)

            for _ in range(npl):
                # Pick a random parent
                parent = rng.choice(prev_nodes)
                parent_pos = positions[parent]

                # New position: parent + random offset in d_growth dimensions
                pos = [x]
                for d in range(d_growth):
                    offset = rng.gauss(0, spread)
                    pos.append(parent_pos[1 + d] + offset)
                pos = tuple(pos)

                idx = len(positions)
                positions.append(pos)
                layer_nodes.append(idx)

                # Connect to all nodes in previous layers within radius
                for prev_idx in prev_nodes:
                    pp = positions[prev_idx]
                    dist = math.sqrt(sum((a - b) ** 2 for a, b in zip(pos, pp)))
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


def compute_field(positions, mass_nodes):
    n = len(positions)
    field = [0.0] * n
    for m in mass_nodes:
        mp = positions[m]
        for i in range(n):
            ip = positions[i]
            r = math.sqrt(sum((a - b) ** 2 for a, b in zip(ip, mp))) + 0.1
            field[i] += 0.1 / r
    return field


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


def measure(positions, adj, nl):
    """Measure pur_min and gravity on one grown graph."""
    k_band = [3.0, 5.0, 7.0]
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

    # Use first transverse coordinate (y1 = positions[i][1]) for slits
    bl_idx = len(layers) // 3
    bi = by_layer[layers[bl_idx]]
    cy = sum(positions[i][1] for i in bi) / len(bi) if bi else 0
    slit_sep = 2.0

    sa = [i for i in bi if positions[i][1] > cy + slit_sep][:3]
    sb = [i for i in bi if positions[i][1] < cy - slit_sep][:3]
    if not sa or not sb:
        # Try with smaller separation
        sa = sorted(bi, key=lambda i: -positions[i][1])[:3]
        sb = sorted(bi, key=lambda i: positions[i][1])[:3]
        if set(sa) & set(sb):
            return None
    blocked = set(bi) - set(sa + sb)

    grav_layer = layers[2 * len(layers) // 3]
    mass = [i for i in by_layer[grav_layer] if positions[i][1] > cy]
    start = bl_idx + 1
    stop = min(len(layers) - 1, start + max(1, round(nl / 6)))
    mn = []
    for layer in layers[start:stop]:
        mn.extend(by_layer[layer])
    field = compute_field(positions, list(set(mn) | set(mass)))
    field_flat = [0.0] * n

    pm_vals, gd_vals = [], []
    for k in k_band:
        aa = propagate(positions, adj, field, src, k, blocked | set(sb))
        ab = propagate(positions, adj, field, src, k, blocked | set(sa))
        rho = {}
        for d1 in det_list:
            for d2 in det_list:
                rho[(d1, d2)] = (aa[d1].conjugate() * aa[d2]
                                  + ab[d1].conjugate() * ab[d2])
        tr = sum(rho[(d, d)] for d in det_list).real
        if tr > 1e-30:
            for key in rho:
                rho[key] /= tr
            pm_vals.append(sum(abs(v) ** 2 for v in rho.values()).real)

        am = propagate(positions, adj, field, src, k, blocked)
        af = propagate(positions, adj, field_flat, src, k, blocked)
        pm = sum(abs(am[d]) ** 2 for d in det_list)
        pf = sum(abs(af[d]) ** 2 for d in det_list)
        if pm > 1e-30 and pf > 1e-30:
            ym = sum(abs(am[d]) ** 2 * positions[d][1] for d in det_list) / pm
            yf = sum(abs(af[d]) ** 2 * positions[d][1] for d in det_list) / pf
            gd_vals.append(ym - yf)

    if not pm_vals:
        return None
    return {
        "pm": sum(pm_vals) / len(pm_vals),
        "grav": sum(gd_vals) / len(gd_vals) if gd_vals else 0.0,
    }


def main():
    import time

    print("=" * 70)
    print("GEOMETRIC GROWTH: Axiom-compliant spatial locality")
    print("  Positions emerge from parent + random offset in d dimensions")
    print("  Edges connect within radius (geometric locality)")
    print("=" * 70)
    print()

    n_seeds = 16

    for d_growth in [1, 2, 3, 4]:
        print(f"  [d_growth={d_growth} (= {d_growth+1}D graph)]")
        print(f"  {'N':>4s}  {'pur_min':>8s}  {'1-pm':>7s}  {'grav':>8s}  "
              f"{'n_ok':>4s}  {'time':>5s}")
        print(f"  {'-' * 44}")

        data = {}
        for nl in [12, 18, 25, 30, 40]:
            t0 = time.time()
            pm_all, gd_all = [], []
            for seed_i in range(n_seeds):
                seed = seed_i * 7 + 3
                positions, adj = grow_geometric_dag(
                    nl, 25, d_growth, connect_radius=3.0, spread=1.0, rng_seed=seed)
                r = measure(positions, adj, nl)
                if r:
                    pm_all.append(r["pm"])
                    gd_all.append(r["grav"])

            dt = time.time() - t0
            if pm_all:
                apm = sum(pm_all) / len(pm_all)
                agd = sum(gd_all) / len(gd_all)
                data[nl] = apm
                print(f"  {nl:4d}  {apm:8.4f}  {1-apm:7.4f}  {agd:+8.3f}  "
                      f"{len(pm_all):4d}  {dt:4.0f}s")
            else:
                print(f"  {nl:4d}  FAIL")
            import sys
            sys.stdout.flush()

        fit_ns = [n for n in sorted(data.keys()) if 1 - data[n] > 0.001]
        if len(fit_ns) >= 3:
            xs = [math.log(n) for n in fit_ns]
            ys = [math.log(1 - data[n]) for n in fit_ns]
            nn = len(xs)
            mx = sum(xs) / nn
            my = sum(ys) / nn
            sxx = sum((x - mx) ** 2 for x in xs)
            sxy = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
            syy = sum((y - my) ** 2 for y in ys)
            alpha = sxy / sxx
            r2 = (sxy ** 2) / (sxx * syy) if syy > 0 else 0
            print(f"\n  alpha = {alpha:.3f}, R² = {r2:.3f}")
        print()

    print("=" * 70)
    print("AXIOM CHAIN:")
    print("  If d_growth=3 produces alpha ≈ -0.5 (like imposed 4D):")
    print("    → Geometric locality + local continuation → physics")
    print("  The key axiom: space = inferred from influence neighborhoods")
    print("  The growth rule: new nodes extend parents in d dimensions")


if __name__ == "__main__":
    main()
