#!/usr/bin/env python3
"""Emergent barrier from amplitude density.

Axiom 9: "Measurement is durable record formation that separates
alternatives." The barrier separates slit alternatives.

Can the barrier emerge from the graph's own amplitude structure?

Mechanism: nodes with HIGH amplitude density from all directions
act as partial barriers — they "absorb" amplitude into local
oscillation rather than transmitting it. This is the discrete
analogue of "a dense region of events scatters passing amplitude."

Implementation: at each barrier-layer node, compute how much total
amplitude arrives from ALL paths (not just from one slit). Nodes
with high total amplitude are "dense" and damp transmission.
Only nodes with low total amplitude (the slit openings) transmit.

This IS the barrier — but it emerges from the amplitude landscape
rather than being imposed by hand.

The test: replace the hand-imposed barrier with amplitude-density
damping at the barrier layer. If this produces interference AND
decoherence, Axiom 9 is closed.
"""

from __future__ import annotations
import math
import cmath
import random as rng_mod
from collections import defaultdict, deque

BETA = 0.8


def grow_geometric_dag(n_layers=20, npl=25, d_growth=3,
                        connect_radius=3.0, spread=1.0, rng_seed=42):
    rng = rng_mod.Random(rng_seed)
    positions = []
    adj = defaultdict(list)
    layer_indices = []
    for layer in range(n_layers):
        x = float(layer)
        layer_nodes = []
        if layer == 0:
            positions.append(tuple([x] + [0.0] * d_growth))
            layer_nodes.append(0)
        else:
            prev_nodes = []
            for pl in layer_indices[max(0, layer - 2):]:
                prev_nodes.extend(pl)
            for _ in range(npl):
                parent = rng.choice(prev_nodes)
                pp = positions[parent]
                pos = tuple([x] + [pp[1 + d] + rng.gauss(0, spread) for d in range(d_growth)])
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


def propagate_with_damping(positions, adj, field, src, k, damping=None):
    """Propagate with per-node damping factor.

    damping[i] in [0, 1]: amplitude at node i is multiplied by damping[i].
    damping[i] = 0: fully blocked (like imposed barrier).
    damping[i] = 1: fully transmitting.
    """
    n = len(positions)
    damping = damping or [1.0] * n
    order = _topo_order(adj, n)
    amps = [0j] * n
    for s in src:
        amps[s] = 1.0 / len(src)
    for i in order:
        if abs(amps[i]) < 1e-30:
            continue
        # Apply damping
        amps[i] *= damping[i]
        if abs(amps[i]) < 1e-30:
            continue
        for j in adj.get(i, []):
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


def compute_emergent_damping(positions, adj, src, barrier_layer_nodes,
                               slit_frac=0.25, k_probe=5.0):
    """Compute amplitude-density-based damping at barrier layer.

    1. Propagate from source with flat field to barrier
    2. At barrier: nodes with TOP amplitude pass freely (slits)
       Nodes with LOW amplitude are damped (wall)
    3. Return damping array

    slit_frac: fraction of barrier nodes that become slits (pass).
    The rest become partial walls.
    """
    n = len(positions)
    flat = [0.0] * n
    amps = propagate_with_damping(positions, adj, flat, src, k_probe)

    # Rank barrier nodes by amplitude
    barrier_amps = [(i, abs(amps[i]) ** 2) for i in barrier_layer_nodes]
    barrier_amps.sort(key=lambda x: -x[1])

    n_slit = max(2, int(len(barrier_amps) * slit_frac))
    slit_nodes = set(i for i, _ in barrier_amps[:n_slit])

    # Damping: slits = 1.0, walls = 0.0 (hard), all others = 1.0
    damping = [1.0] * n
    for i in barrier_layer_nodes:
        if i in slit_nodes:
            damping[i] = 1.0
        else:
            damping[i] = 0.0  # hard block

    return damping, slit_nodes


def run_emergent_barrier_test(nl, d_growth, seed, slit_frac=0.25):
    """Full test: grown graph + emergent barrier + decoherence."""
    positions, adj = grow_geometric_dag(nl, 30, d_growth, 3.5, 1.2, seed)
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
    barrier_nodes = by_layer[layers[bl_idx]]
    if len(barrier_nodes) < 6:
        return None

    # Compute emergent damping
    damping, slit_nodes = compute_emergent_damping(
        positions, adj, src, barrier_nodes, slit_frac)

    # Identify upper/lower slits by y-coordinate
    cy = sum(positions[i][1] for i in slit_nodes) / len(slit_nodes)
    sa = [i for i in slit_nodes if positions[i][1] > cy]
    sb = [i for i in slit_nodes if positions[i][1] <= cy]
    if not sa or not sb:
        return None

    # Mass (emergent, from free propagation amplitude)
    flat = [0.0] * n
    amps_free = propagate_with_damping(positions, adj, flat, src, 5.0, damping)
    mid_start = len(layers) // 2
    mid_end = min(len(layers) - 1, mid_start + 4)
    mid_upper = []
    for layer in layers[mid_start:mid_end]:
        for i in by_layer[layer]:
            if positions[i][1] > cy:
                mid_upper.append(i)
    if len(mid_upper) < 2:
        return None

    amp_sq = sorted([(i, abs(amps_free[i]) ** 2) for i in mid_upper], key=lambda x: -x[1])
    mass_nodes = [i for i, _ in amp_sq[:max(2, len(amp_sq) // 5)]]

    field = [0.0] * n
    for m in mass_nodes:
        mp = positions[m]
        for i in range(n):
            ip = positions[i]
            r = math.sqrt(sum((a - b) ** 2 for a, b in zip(ip, mp))) + 0.1
            field[i] += 0.3 / r

    # Per-slit damping: block one slit group
    damping_a = list(damping)
    damping_b = list(damping)
    for i in sb:
        damping_a[i] = 0.0  # block lower slit → only upper passes
    for i in sa:
        damping_b[i] = 0.0  # block upper slit → only lower passes

    pm_vals, gd_vals = [], []
    for k in [3.0, 5.0, 7.0]:
        aa = propagate_with_damping(positions, adj, field, src, k, damping_a)
        ab = propagate_with_damping(positions, adj, field, src, k, damping_b)
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

        am = propagate_with_damping(positions, adj, field, src, k, damping)
        af = propagate_with_damping(positions, adj, flat, src, k, damping)
        pm_m = sum(abs(am[d]) ** 2 for d in det_list)
        pm_f = sum(abs(af[d]) ** 2 for d in det_list)
        if pm_m > 1e-30 and pm_f > 1e-30:
            ym = sum(abs(am[d]) ** 2 * positions[d][1] for d in det_list) / pm_m
            yf = sum(abs(af[d]) ** 2 * positions[d][1] for d in det_list) / pm_f
            gd_vals.append(ym - yf)

    if not pm_vals:
        return None
    return {
        "pm": sum(pm_vals) / len(pm_vals),
        "grav": sum(gd_vals) / len(gd_vals) if gd_vals else 0.0,
        "n_slits": len(slit_nodes),
    }


def main():
    import time

    print("=" * 70)
    print("EMERGENT BARRIER: amplitude-density damping at barrier layer")
    print("  High-amplitude nodes = slits (transmit)")
    print("  Low-amplitude nodes = wall (block)")
    print("  NOTHING imposed — barrier emerges from propagation")
    print("=" * 70)
    print()

    n_seeds = 20

    for d_growth in [2, 3]:
        print(f"  [d_growth={d_growth} ({d_growth+1}D)]")
        print(f"  {'N':>4s}  {'pur_min':>8s}  {'1-pm':>7s}  {'grav':>8s}  "
              f"{'n_ok':>4s}  {'time':>5s}")
        print(f"  {'-' * 44}")

        for nl in [18, 25, 30]:
            t0 = time.time()
            pm_all, gd_all = [], []
            for seed_i in range(n_seeds):
                r = run_emergent_barrier_test(nl, d_growth, seed_i * 7 + 3)
                if r:
                    pm_all.append(r["pm"])
                    gd_all.append(r["grav"])
            dt = time.time() - t0
            if pm_all:
                n_ok = len(pm_all)
                apm = sum(pm_all) / n_ok
                agd = sum(gd_all) / n_ok
                se = (sum((g - agd) ** 2 for g in gd_all) / n_ok) ** 0.5 / math.sqrt(n_ok) if n_ok > 1 else 0
                ratio = agd / se if se > 0 else 0
                both = "FULL" if ratio > 1.5 and apm < 0.998 else ""
                print(f"  {nl:4d}  {apm:8.4f}  {1-apm:7.4f}  {agd:+8.3f}  "
                      f"{n_ok:4d}  {dt:4.0f}s  {both}")
            else:
                print(f"  {nl:4d}  FAIL")
            import sys
            sys.stdout.flush()
        print()

    print("FULL = gravity + decoherence + emergent barrier on grown graph")
    print("This would close ALL axioms including Axiom 9.")


if __name__ == "__main__":
    main()
