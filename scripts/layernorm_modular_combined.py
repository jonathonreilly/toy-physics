#!/usr/bin/env python3
"""Layer norm + modular DAG combined: do the two improvements stack?

Layer norm alone: pur_min 0.80 at N=40 (vs 0.95 linear) on uniform DAGs.
Modular gap alone: pur_min 0.89 at N=40 (vs 0.95 uniform) on linear propagator.

If they stack: pur_min could reach ~0.70 at N=40.
If they don't: one dominates and the other is redundant.

Also: fit the scaling law for layer norm to see if the exponent changes.
"""

from __future__ import annotations
import math
import cmath
import sys
import os
import time
from collections import defaultdict, deque

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.generative_causal_dag_interference import generate_causal_dag
from scripts.topology_families import generate_modular_dag

BETA = 0.8
N_YBINS = 8
LAM = 10.0


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


def compute_field(positions, adj, mass_nodes):
    n = len(positions)
    field = [0.0] * n
    for m in mass_nodes:
        mx, my = positions[m]
        for i in range(n):
            ix, iy = positions[i]
            r = math.sqrt((ix - mx) ** 2 + (iy - my) ** 2) + 0.1
            field[i] += 0.1 / r
    return field


def propagate_layernorm(positions, adj, field, src, k, blocked=None):
    """Propagate with per-layer amplitude normalization."""
    n = len(positions)
    blocked = blocked or set()
    by_layer = defaultdict(list)
    for idx, (x, y) in enumerate(positions):
        by_layer[round(x)].append(idx)
    layers = sorted(by_layer.keys())

    amps = [0j] * n
    for s in src:
        amps[s] = 1.0 / len(src)

    for li, lk in enumerate(layers):
        for i in by_layer[lk]:
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

        # Normalize next layer
        if li + 1 < len(layers):
            next_nodes = by_layer[layers[li + 1]]
            total_sq = sum(abs(amps[i]) ** 2 for i in next_nodes)
            if total_sq > 1e-30:
                norm = math.sqrt(total_sq)
                for i in next_nodes:
                    amps[i] /= norm

    return amps


def cl_purity_min(amps_a, amps_b, det_list):
    rho = {}
    for d1 in det_list:
        for d2 in det_list:
            rho[(d1, d2)] = (
                amps_a[d1].conjugate() * amps_a[d2]
                + amps_b[d1].conjugate() * amps_b[d2]
            )
    tr = sum(rho[(d, d)] for d in det_list).real
    if tr <= 1e-30:
        return math.nan
    for key in rho:
        rho[key] /= tr
    return sum(abs(v) ** 2 for v in rho.values()).real


def run_one(positions, adj, k_band, n_layers, use_layernorm=False):
    by_layer = defaultdict(list)
    for idx, (x, y) in enumerate(positions):
        by_layer[round(x)].append(idx)
    layers = sorted(by_layer.keys())
    if len(layers) < 7:
        return None
    src = by_layer[layers[0]]
    det_list = list(by_layer[layers[-1]])
    if not det_list:
        return None
    cy = sum(y for _, y in positions) / len(positions)
    bl_idx = len(layers) // 3
    bi = by_layer[layers[bl_idx]]
    sa = [i for i in bi if positions[i][1] > cy + 3][:3]
    sb = [i for i in bi if positions[i][1] < cy - 3][:3]
    if not sa or not sb:
        return None
    blocked = set(bi) - set(sa + sb)

    grav_layer = layers[2 * len(layers) // 3]
    grav_mass = [i for i in by_layer[grav_layer] if positions[i][1] > cy + 1]
    start = bl_idx + 1
    stop = min(len(layers) - 1, start + max(1, round(n_layers / 6)))
    mass_nodes = []
    for layer in layers[start:stop]:
        mass_nodes.extend(i for i in by_layer[layer] if abs(positions[i][1] - cy) <= 3.0)
    field = compute_field(positions, adj, list(set(mass_nodes) | set(grav_mass)))

    prop = propagate_layernorm if use_layernorm else None

    pm_vals = []
    for k in k_band:
        if use_layernorm:
            aa = propagate_layernorm(positions, adj, field, src, k, blocked | set(sb))
            ab = propagate_layernorm(positions, adj, field, src, k, blocked | set(sa))
        else:
            # Linear propagator (inline to avoid import complexity)
            from scripts.nonlinear_pareto import propagate_mixed
            aa = propagate_mixed(positions, adj, field, src, k,
                                  blocked | set(sb), "layer_norm", 0.0, 999999)
            ab = propagate_mixed(positions, adj, field, src, k,
                                  blocked | set(sa), "layer_norm", 0.0, 999999)

        pm = cl_purity_min(aa, ab, det_list)
        if not math.isnan(pm):
            pm_vals.append(pm)

    if not pm_vals:
        return None
    return sum(pm_vals) / len(pm_vals)


def main():
    print("=" * 78)
    print("LAYER NORM + MODULAR DAG COMBINED")
    print("  Do the two improvements stack?")
    print(f"  CL bath lambda={LAM}, k-band [3,5,7], 16 seeds")
    print("=" * 78)
    print()

    k_band = [3.0, 5.0, 7.0]
    n_seeds = 16
    seeds = [s * 7 + 3 for s in range(n_seeds)]

    configs = [
        ("Uniform + linear", generate_causal_dag, {}, False),
        ("Uniform + layernorm", generate_causal_dag, {}, True),
        ("Modular gap=4 + linear", generate_modular_dag, {"gap": 4.0}, False),
        ("Modular gap=4 + layernorm", generate_modular_dag, {"gap": 4.0}, True),
        ("Modular gap=2 + layernorm", generate_modular_dag, {"gap": 2.0}, True),
    ]

    for name, gen, kwargs, use_ln in configs:
        print(f"  [{name}]")
        print(f"  {'N':>4s}  {'pur_min':>8s}  {'1-pm':>7s}  {'n_ok':>4s}  {'time':>5s}")
        print(f"  {'-' * 36}")

        for nl in [25, 40, 60, 80]:
            t0 = time.time()
            pm_all = []
            for seed in seeds:
                positions, adj, _ = gen(
                    n_layers=nl, nodes_per_layer=25, y_range=12.0,
                    connect_radius=3.0, rng_seed=seed, **kwargs,
                )
                r = run_one(positions, adj, k_band, nl, use_ln)
                if r is not None:
                    pm_all.append(r)

            dt = time.time() - t0
            if pm_all:
                apm = sum(pm_all) / len(pm_all)
                print(f"  {nl:4d}  {apm:8.4f}  {1-apm:7.4f}  {len(pm_all):4d}  {dt:4.0f}s")
            sys.stdout.flush()

        print()

    print("STACKING = modular+layernorm < min(modular+linear, uniform+layernorm)")
    print("If yes: the two mechanisms are complementary")


if __name__ == "__main__":
    main()
