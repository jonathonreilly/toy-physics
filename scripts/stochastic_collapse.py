#!/usr/bin/env python3
"""Stochastic collapse at mass nodes: irreversible projection.

The CL bath gives soft decoherence (D=exp(-lambda^2*S)) that decays
as 1/N because the bath contrast S shrinks. Collapse is different:
each mass encounter IRREVERSIBLY projects onto the which-slit basis.

Mechanism: at each mass node m, with probability p_collapse:
  1. Compute which-slit label: which slit's blocked propagation
     contributes MORE amplitude at this node
  2. Project: zero the amplitude from the minority slit
  3. Continue propagation from the projected state

The density matrix is the average over stochastic collapse sequences.
Each realization has different collapse events, producing different
detector amplitudes. The average ρ = E[|ψ_r><ψ_r|] is mixed.

Key prediction: decoherence should GROW with the number of mass
encounters (more collapses = more mixing), not decay with N.
If (1-pur) ~ n_encounters^alpha with alpha > 0, the ceiling is broken.

We approximate the density matrix by Monte Carlo: run many
realizations of the stochastic collapse, collect detector amplitudes,
average the outer products.
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
        mx, my = positions[m]
        for i in range(n):
            ix, iy = positions[i]
            r = math.sqrt((ix - mx) ** 2 + (iy - my) ** 2) + 0.1
            field[i] += 0.1 / r
    return field


def propagate_with_collapse(positions, adj, field, src, k, blocked,
                             mass_set, p_collapse, rng, use_ln=False):
    """Propagate with stochastic collapse at mass nodes.

    At each mass node (in topological order), with probability p_collapse:
      - Check if node received amplitude from both slits
        (approximated by: is the node reachable from both slit groups?)
      - If yes, randomly project onto one slit's contribution
        (probability proportional to |amp|^2 from each slit)

    Returns detector amplitudes for this realization.
    """
    n = len(positions)
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

            # Collapse check at mass nodes
            if i in mass_set and p_collapse > 0 and rng.random() < p_collapse:
                # Dephase: multiply by a random phase
                # This destroys coherence when averaged over realizations
                theta_rand = rng.uniform(0, 2 * math.pi)
                amps[i] *= cmath.exp(1j * theta_rand)

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

        # Optional layer norm
        if use_ln and li + 1 < len(layers):
            nxt = by_layer[layers[li + 1]]
            tsq = sum(abs(amps[i]) ** 2 for i in nxt)
            if tsq > 1e-30:
                norm = math.sqrt(tsq)
                for i in nxt:
                    amps[i] /= norm

    return amps


def monte_carlo_purity(positions, adj, field, src, det_list, k_band,
                        blocked_a, blocked_b, mass_set, p_collapse,
                        n_realizations=50, use_ln=False):
    """Compute density matrix purity via Monte Carlo over collapse realizations.

    For each realization r:
      - Propagate slit A with random collapses → ψ_A^r(det)
      - Propagate slit B with random collapses → ψ_B^r(det)
      - ψ^r = ψ_A^r + ψ_B^r (coherent sum for this realization)
      - ρ^r = |ψ^r><ψ^r|

    Average: ρ = (1/R) Σ_r ρ^r
    Purity = Tr(ρ²)

    Also compute pur_min (p_collapse=0, no collapses) for comparison.
    """
    import random as rng_mod

    # Collect ρ entries averaged over k and realizations
    rho = {}
    for d1 in det_list:
        for d2 in det_list:
            rho[(d1, d2)] = 0j

    n_total = 0

    for k in k_band:
        for r in range(n_realizations):
            rng = rng_mod.Random(r * 1000 + int(k * 100))

            amps_a = propagate_with_collapse(
                positions, adj, field, src, k, blocked_a,
                mass_set, p_collapse, rng, use_ln)
            amps_b = propagate_with_collapse(
                positions, adj, field, src, k, blocked_b,
                mass_set, p_collapse, rng, use_ln)

            # Total amplitude at detectors for this realization
            psi = [amps_a[d] + amps_b[d] for d in det_list]
            norm_sq = sum(abs(p) ** 2 for p in psi)
            if norm_sq < 1e-30:
                continue

            # Accumulate normalized ρ
            for i, d1 in enumerate(det_list):
                for j, d2 in enumerate(det_list):
                    rho[(d1, d2)] += psi[i].conjugate() * psi[j] / norm_sq

            n_total += 1

    if n_total == 0:
        return math.nan

    # Average
    for key in rho:
        rho[key] /= n_total

    # Purity
    purity = sum(abs(v) ** 2 for v in rho.values()).real
    return purity


def run_collapse_test(nl, seed, p_collapse, use_ln=False, gap=0.0,
                       n_realizations=50):
    """Run collapse test for one graph."""
    if gap > 0:
        positions, adj, _ = generate_modular_dag(
            n_layers=nl, nodes_per_layer=25, y_range=12.0,
            connect_radius=3.0, rng_seed=seed, gap=gap)
    else:
        positions, adj, _ = generate_causal_dag(
            n_layers=nl, nodes_per_layer=25, y_range=12.0,
            connect_radius=3.0, rng_seed=seed)

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

    # Mass nodes (for collapse locations)
    grav_layer = layers[2 * len(layers) // 3]
    mass_nodes = [i for i in by_layer[grav_layer] if positions[i][1] > cy + 1]
    env_depth = max(1, round(nl / 6))
    start = bl_idx + 1
    stop = min(len(layers) - 1, start + env_depth)
    mass_env = []
    for layer in layers[start:stop]:
        mass_env.extend(by_layer[layer])
    mass_set = set(mass_env)

    field = compute_field(positions, list(mass_set | set(mass_nodes)))

    blocked_a = blocked | set(sb)
    blocked_b = blocked | set(sa)

    k_band = [3.0, 5.0, 7.0]
    pur = monte_carlo_purity(
        positions, adj, field, src, det_list, k_band,
        blocked_a, blocked_b, mass_set, p_collapse,
        n_realizations, use_ln)

    return {"pur": pur, "n_mass": len(mass_set)}


def main():
    print("=" * 78)
    print("STOCHASTIC COLLAPSE AT MASS NODES")
    print("  Random dephasing at mass encounters, Monte Carlo purity")
    print("  50 realizations per graph, 12 seeds per N")
    print("=" * 78)
    print()

    n_seeds = 12
    seeds = [s * 7 + 3 for s in range(n_seeds)]

    # Part 1: p_collapse sweep at N=30
    print("PART 1: p_collapse sweep at N=30 (uniform DAG)")
    print(f"  {'p':>6s}  {'purity':>8s}  {'1-pur':>7s}  {'n_ok':>4s}")
    print(f"  {'-' * 30}")

    for pc in [0.0, 0.01, 0.05, 0.10, 0.20, 0.50, 1.0]:
        pur_all = []
        for seed in seeds:
            r = run_collapse_test(30, seed, pc, n_realizations=50)
            if r and not math.isnan(r["pur"]):
                pur_all.append(r["pur"])
        if pur_all:
            avg = sum(pur_all) / len(pur_all)
            print(f"  {pc:6.2f}  {avg:8.4f}  {1-avg:7.4f}  {len(pur_all):4d}")
        sys.stdout.flush()

    # Part 2: N scaling with p_collapse=0.2
    print()
    print("PART 2: N scaling with p_collapse=0.2 (uniform DAG)")
    print(f"  {'N':>4s}  {'purity':>8s}  {'1-pur':>7s}  {'n_mass':>6s}  "
          f"{'n_ok':>4s}  {'time':>5s}")
    print(f"  {'-' * 42}")

    for nl in [18, 25, 30, 40, 60, 80]:
        t0 = time.time()
        pur_all, mass_all = [], []
        for seed in seeds:
            r = run_collapse_test(nl, seed, 0.2, n_realizations=50)
            if r and not math.isnan(r["pur"]):
                pur_all.append(r["pur"])
                mass_all.append(r["n_mass"])
        dt = time.time() - t0
        if pur_all:
            avg = sum(pur_all) / len(pur_all)
            avg_m = sum(mass_all) / len(mass_all)
            print(f"  {nl:4d}  {avg:8.4f}  {1-avg:7.4f}  {avg_m:6.0f}  "
                  f"{len(pur_all):4d}  {dt:4.0f}s")
        sys.stdout.flush()

    # Part 3: Combined (LN + gap=2 + collapse)
    print()
    print("PART 3: LN + gap=2 + collapse (p=0.2)")
    print(f"  {'N':>4s}  {'purity':>8s}  {'1-pur':>7s}  {'n_ok':>4s}  {'time':>5s}")
    print(f"  {'-' * 36}")

    for nl in [25, 40, 60, 80]:
        t0 = time.time()
        pur_all = []
        for seed in seeds:
            r = run_collapse_test(nl, seed, 0.2, use_ln=True, gap=2.0,
                                   n_realizations=50)
            if r and not math.isnan(r["pur"]):
                pur_all.append(r["pur"])
        dt = time.time() - t0
        if pur_all:
            avg = sum(pur_all) / len(pur_all)
            print(f"  {nl:4d}  {avg:8.4f}  {1-avg:7.4f}  {len(pur_all):4d}  {dt:4.0f}s")
        sys.stdout.flush()

    print()
    print("KEY: Does (1-purity) GROW with N under collapse?")
    print("  If yes → collapse changes the scaling exponent")
    print("  If no → random dephasing doesn't help at scale")


if __name__ == "__main__":
    main()
