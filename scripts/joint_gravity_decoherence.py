#!/usr/bin/env python3
"""Joint gravity + decoherence test on identical modular DAG instances.

The unification check: on the SAME graph, with the SAME propagator,
does the modular DAG simultaneously produce:
  1. Gravitational deflection (positive delta toward mass)
  2. CL bath decoherence (pur_min < 0.95, stable with N)

Also tests whether these two phenomena help or hinder each other.

Phase diagram: sweep gap and crosslink_prob to find the region
of topology space where BOTH work.
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


def compute_field(positions, mass_nodes, strength=0.1):
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


def bin_amplitudes(amps, positions, nodes):
    bins = [0j] * N_YBINS
    bw = 24.0 / N_YBINS
    for m in nodes:
        y = positions[m][1]
        b = int((y + 12.0) / bw)
        b = max(0, min(N_YBINS - 1, b))
        bins[b] += amps[m]
    return bins


def cl_purity_triple(amps_a, amps_b, D, det_list):
    def _pur(Dv):
        rho = {}
        for d1 in det_list:
            for d2 in det_list:
                rho[(d1, d2)] = (
                    amps_a[d1].conjugate() * amps_a[d2]
                    + amps_b[d1].conjugate() * amps_b[d2]
                    + Dv * amps_a[d1].conjugate() * amps_b[d2]
                    + Dv * amps_b[d1].conjugate() * amps_a[d2]
                )
        tr = sum(rho[(d, d)] for d in det_list).real
        if tr <= 1e-30:
            return math.nan
        for key in rho:
            rho[key] /= tr
        return sum(abs(v) ** 2 for v in rho.values()).real
    return _pur(D), _pur(1.0), _pur(0.0)


def run_joint_test(positions, adj, k_band, n_layers):
    """Run both gravity and decoherence on a single graph instance.

    Returns dict with gravity_delta, pur_min, decoh, or None if setup fails.
    """
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

    all_ys = [y for _, y in positions]
    cy = sum(all_ys) / len(all_ys)

    # Barrier setup
    bl_idx = len(layers) // 3
    bl = layers[bl_idx]
    bi = by_layer[bl]
    sa = [i for i in bi if positions[i][1] > cy + 3][:3]
    sb = [i for i in bi if positions[i][1] < cy - 3][:3]
    if not sa or not sb:
        return None
    blocked = set(bi) - set(sa + sb)

    # Mass nodes (for gravity field)
    grav_layer = layers[2 * len(layers) // 3]
    mass_nodes = [i for i in by_layer[grav_layer] if positions[i][1] > cy + 1]
    if not mass_nodes:
        return None

    # Environment mid-nodes (for decoherence)
    env_depth = max(1, round(n_layers / 6))
    start = bl_idx + 1
    stop = min(len(layers), start + env_depth)
    mid_nodes = []
    for layer in layers[start:stop]:
        mid_nodes.extend(by_layer[layer])

    # Fields
    field_with_mass = compute_field(positions, mass_nodes, strength=0.1)
    field_flat = [0.0] * len(positions)

    gravity_deltas = []
    pm_vals = []
    pc_vals = []
    pcoh_vals = []

    for k in k_band:
        # ─── GRAVITY: both slits open, compare with/without mass field ───
        amps_mass = propagate(positions, adj, field_with_mass, src, k, blocked)
        amps_flat = propagate(positions, adj, field_flat, src, k, blocked)

        prob_mass = sum(abs(amps_mass[d]) ** 2 for d in det_list)
        prob_flat = sum(abs(amps_flat[d]) ** 2 for d in det_list)

        if prob_mass > 1e-30 and prob_flat > 1e-30:
            y_mass = sum(abs(amps_mass[d]) ** 2 * positions[d][1] for d in det_list) / prob_mass
            y_flat = sum(abs(amps_flat[d]) ** 2 * positions[d][1] for d in det_list) / prob_flat
            gravity_deltas.append(y_mass - y_flat)

        # ─── DECOHERENCE: per-slit propagation with mass field ───
        amps_a = propagate(positions, adj, field_with_mass, src, k, blocked | set(sb))
        amps_b = propagate(positions, adj, field_with_mass, src, k, blocked | set(sa))

        ba = bin_amplitudes(amps_a, positions, mid_nodes)
        bb = bin_amplitudes(amps_b, positions, mid_nodes)
        S = sum(abs(a - b) ** 2 for a, b in zip(ba, bb))
        NA = sum(abs(a) ** 2 for a in ba)
        NB = sum(abs(b) ** 2 for b in bb)
        Sn = S / (NA + NB) if (NA + NB) > 0 else 0.0
        D = math.exp(-LAM ** 2 * Sn)

        pc, pcoh, pmin = cl_purity_triple(amps_a, amps_b, D, det_list)
        if not math.isnan(pc):
            pm_vals.append(pmin)
            pc_vals.append(pc)
            pcoh_vals.append(pcoh)

    if not gravity_deltas or not pm_vals:
        return None

    return {
        "gravity_delta": sum(gravity_deltas) / len(gravity_deltas),
        "pur_min": sum(pm_vals) / len(pm_vals),
        "pur_cl": sum(pc_vals) / len(pc_vals),
        "decoh": sum(pcoh_vals) / len(pcoh_vals) - sum(pc_vals) / len(pc_vals),
    }


def main():
    print("=" * 78)
    print("JOINT GRAVITY + DECOHERENCE TEST")
    print("  Same graph instances, same propagator, both measurements")
    print(f"  CL bath lambda={LAM}, k-band [3,5,7]")
    print("=" * 78)
    print()

    k_band = [3.0, 5.0, 7.0]
    n_seeds = 16  # More seeds for stability

    # ─── Part 1: N scaling on modular DAG ──────────────────────────
    print("PART 1: Joint N-scaling on modular DAG (gap=4.0, 16 seeds)")
    print(f"  {'N':>4s}  {'grav_d':>8s}  {'grav_SE':>7s}  {'pur_min':>8s}  "
          f"{'decoh':>8s}  {'n_ok':>4s}")
    print(f"  {'-' * 48}")

    for nl in [12, 18, 25, 30, 40]:
        grav_all, pm_all, decoh_all = [], [], []

        for seed in range(n_seeds):
            positions, adj, _ = generate_modular_dag(
                n_layers=nl, nodes_per_layer=25, y_range=12.0,
                connect_radius=3.0, rng_seed=seed * 7 + 3,
                crosslink_prob=0.02, gap=4.0,
            )
            r = run_joint_test(positions, adj, k_band, nl)
            if r:
                grav_all.append(r["gravity_delta"])
                pm_all.append(r["pur_min"])
                decoh_all.append(r["decoh"])

        if grav_all:
            avg_g = sum(grav_all) / len(grav_all)
            se_g = (sum((g - avg_g) ** 2 for g in grav_all) / len(grav_all)) ** 0.5 / math.sqrt(len(grav_all))
            avg_pm = sum(pm_all) / len(pm_all)
            avg_dec = sum(decoh_all) / len(decoh_all)
            print(f"  {nl:4d}  {avg_g:+8.3f}  {se_g:7.3f}  {avg_pm:8.4f}  "
                  f"{avg_dec:+8.4f}  {len(grav_all):4d}")
        else:
            print(f"  {nl:4d}  FAIL")

    # ─── Part 2: Uniform baseline for comparison ───────────────────
    print()
    print("PART 2: Joint N-scaling on uniform DAG (16 seeds)")
    print(f"  {'N':>4s}  {'grav_d':>8s}  {'grav_SE':>7s}  {'pur_min':>8s}  "
          f"{'decoh':>8s}  {'n_ok':>4s}")
    print(f"  {'-' * 48}")

    for nl in [12, 18, 25, 40]:
        grav_all, pm_all, decoh_all = [], [], []

        for seed in range(n_seeds):
            positions, adj, _ = generate_causal_dag(
                n_layers=nl, nodes_per_layer=25, y_range=12.0,
                connect_radius=3.0, rng_seed=seed * 7 + 3,
            )
            r = run_joint_test(positions, adj, k_band, nl)
            if r:
                grav_all.append(r["gravity_delta"])
                pm_all.append(r["pur_min"])
                decoh_all.append(r["decoh"])

        if grav_all:
            avg_g = sum(grav_all) / len(grav_all)
            se_g = (sum((g - avg_g) ** 2 for g in grav_all) / len(grav_all)) ** 0.5 / math.sqrt(len(grav_all))
            avg_pm = sum(pm_all) / len(pm_all)
            avg_dec = sum(decoh_all) / len(decoh_all)
            print(f"  {nl:4d}  {avg_g:+8.3f}  {se_g:7.3f}  {avg_pm:8.4f}  "
                  f"{avg_dec:+8.4f}  {len(grav_all):4d}")
        else:
            print(f"  {nl:4d}  FAIL")

    # ─── Part 3: Phase diagram (gap × crosslink) ──────────────────
    print()
    print("PART 3: Phase diagram at N=25 (gap × crosslink, 12 seeds)")
    print(f"  {'gap':>5s}  {'xlink':>5s}  {'grav_d':>8s}  {'pur_min':>8s}  "
          f"{'decoh':>8s}  {'both_ok':>7s}")
    print(f"  {'-' * 50}")

    for gap in [0.0, 2.0, 4.0, 6.0]:
        for xlink in [0.0, 0.02, 0.05, 0.10]:
            grav_all, pm_all, decoh_all = [], [], []

            for seed in range(12):
                positions, adj, _ = generate_modular_dag(
                    n_layers=25, nodes_per_layer=25, y_range=12.0,
                    connect_radius=3.0, rng_seed=seed * 7 + 3,
                    crosslink_prob=xlink, gap=gap,
                )
                r = run_joint_test(positions, adj, k_band, 25)
                if r:
                    grav_all.append(r["gravity_delta"])
                    pm_all.append(r["pur_min"])
                    decoh_all.append(r["decoh"])

            if grav_all:
                avg_g = sum(grav_all) / len(grav_all)
                avg_pm = sum(pm_all) / len(pm_all)
                avg_dec = sum(decoh_all) / len(decoh_all)

                gravity_ok = avg_g > 0.5
                decoh_ok = avg_pm < 0.96
                both = "YES" if gravity_ok and decoh_ok else "grav" if gravity_ok else "decoh" if decoh_ok else "neither"

                print(f"  {gap:5.1f}  {xlink:5.2f}  {avg_g:+8.3f}  {avg_pm:8.4f}  "
                      f"{avg_dec:+8.4f}  {both:>7s}")
            else:
                print(f"  {gap:5.1f}  {xlink:5.2f}  FAIL")

    print()
    print("both_ok = gravity_delta > 0.5 AND pur_min < 0.96")
    print("YES = both gravity and decoherence work in this topology region")


if __name__ == "__main__":
    main()
