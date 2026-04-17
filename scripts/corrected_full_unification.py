#!/usr/bin/env python3
"""Full unification: gravity + interference + decoherence on irregular DAGs.

Previous results:
  - Gravity: 11/12 on DAGs (corrected propagator, k-averaged)
  - Interference: 12/12 (V=0.995)
  - Decoherence: V drops 35% at η=1.0 on spread graphs

This test: all three simultaneously on the same graph, same parameters.

Mass provides gravity. Slits provide interference. Phase noise provides
decoherence. The corrected propagator (1/L^p) handles it all.

Measure at each (seed, η):
  - Gravity: centroid shift toward mass (with noise)
  - Interference: V of ensemble-averaged slit distribution
  - Decoherence: V_baseline - V_noisy

PStack experiment: corrected-full-unification
"""

from __future__ import annotations
import math
import cmath
import random
from collections import defaultdict, deque
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scripts.generative_causal_dag_interference import generate_causal_dag


def compute_field(positions, adj, mass_idx, iterations=50):
    n = len(positions)
    undirected = defaultdict(set)
    for i, nbs in adj.items():
        for j in nbs:
            undirected[i].add(j)
            undirected[j].add(i)
    ms = set(mass_idx)
    field = [1.0 if i in ms else 0.0 for i in range(n)]
    for _ in range(iterations):
        nf = [0.0]*n
        for i in range(n):
            if i in ms:
                nf[i] = 1.0
            elif undirected.get(i):
                nf[i] = sum(field[j] for j in undirected[i]) / len(undirected[i])
        field = nf
    return field


def pathsum_noisy(positions, adj, field, src, det, k, eta, rng,
                  barrier_idx=None, slit_idx=None):
    n = len(positions)
    blocked = set()
    if barrier_idx is not None and slit_idx is not None:
        blocked = set(barrier_idx) - set(slit_idx)

    in_deg = [0]*n
    for i, nbs in adj.items():
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

    amps = [0.0+0.0j]*n
    for s in src:
        amps[s] = 1.0/len(src)
    for i in order:
        if i in blocked or abs(amps[i]) < 1e-30:
            continue
        for j in adj.get(i, []):
            if j in blocked:
                continue
            x1, y1 = positions[i]
            x2, y2 = positions[j]
            L = math.sqrt((x2-x1)**2+(y2-y1)**2)
            if L < 1e-10:
                continue
            lf = 0.5*(field[i]+field[j])
            dl = L*(1+lf)
            ret = math.sqrt(max(dl*dl-L*L, 0))
            act = dl-ret
            noise = eta * rng.gauss(0, 1) if eta > 0 else 0
            ea = cmath.exp(1j*(k*act + noise))/(L**1.0)
            amps[j] += amps[i]*ea

    probs = {d: abs(amps[d])**2 for d in det}
    total = sum(probs.values())
    if total > 0:
        probs = {d: p/total for d, p in probs.items()}
    return probs


def centroid_y(probs, positions):
    total = sum(probs.values())
    if total == 0:
        return 0.0
    return sum(positions[d][1]*p for d, p in probs.items()) / total


def visibility(probs, positions, det):
    py = defaultdict(float)
    for d in det:
        py[positions[d][1]] += probs.get(d, 0)
    ys = sorted(py.keys())
    if len(ys) < 3:
        return 0.0
    vals = [py[y] for y in ys]
    peaks = [vals[i] for i in range(1, len(vals)-1)
             if vals[i] > vals[i-1] and vals[i] > vals[i+1]]
    troughs = [vals[i] for i in range(1, len(vals)-1)
               if vals[i] < vals[i-1] and vals[i] < vals[i+1]]
    if peaks and troughs:
        return (max(peaks)-min(troughs))/(max(peaks)+min(troughs))
    return 0.0


def main():
    n_layers = 15
    npl = 25
    y_range = 15.0  # Moderate spread for both gravity and decoherence
    radius = 3.0
    n_seeds = 12
    N_real = 40  # noise realizations
    k_band = [3.0, 5.0, 7.0]

    print("=" * 70)
    print("FULL UNIFICATION: Gravity + Interference + Decoherence")
    print(f"  {n_layers} layers × {npl} nodes, y_range={y_range}, r={radius}")
    print(f"  Corrected propagator (1/L^p)")
    print(f"  k-band={k_band}, {N_real} noise realizations")
    print("=" * 70)
    print()

    for eta in [0.0, 0.3, 0.7, 1.5]:
        print(f"  η = {eta}:")
        print(f"    {'seed':>4s}  {'grav':>7s}  {'V_ens':>7s}  {'V_ind':>7s}  "
              f"{'attract':>7s}  {'interf':>6s}  {'decoh':>5s}  {'all3':>4s}")
        print(f"    {'-' * 56}")

        grav_yes = interf_yes = decoh_yes = all3 = 0
        n_valid = 0

        for seed in range(n_seeds):
            positions, adj, arrival = generate_causal_dag(
                n_layers=n_layers, nodes_per_layer=npl,
                y_range=y_range, connect_radius=radius,
                rng_seed=seed*11+7,
            )
            n = len(positions)
            by_layer = defaultdict(list)
            for idx, (x, y) in enumerate(positions):
                by_layer[round(x)].append(idx)
            layers = sorted(by_layer.keys())
            if len(layers) < 6:
                continue

            src = by_layer[layers[0]]
            det = by_layer[layers[-1]]
            if not det:
                continue

            mid = len(layers)//2
            all_ys = [y for _, y in positions]
            cy = sum(all_ys)/len(all_ys)

            # Mass
            mass_layers = [layers[mid-1], layers[mid], layers[mid+1]]
            mass_idx = []
            for l in mass_layers:
                mass_idx.extend(i for i in by_layer[l] if positions[i][1] > cy+1)
            if len(mass_idx) < 3:
                continue
            mass_cy = sum(positions[i][1] for i in mass_idx)/len(mass_idx)
            field = compute_field(positions, adj, mass_idx)
            free_f = [0.0]*n

            # Barrier/slits
            if mid < 3:
                continue
            bl = layers[mid-3]
            bi = by_layer[bl]
            sa = [i for i in bi if positions[i][1] > cy+2][:3]
            sb = [i for i in bi if positions[i][1] < cy-2][:3]
            if not sa or not sb:
                continue
            si = sa + sb

            # ---- GRAVITY: k-averaged centroid shift (ensemble-averaged) ----
            avg_free = {d: 0.0 for d in det}
            avg_mass = {d: 0.0 for d in det}
            for i in range(N_real):
                rng_f = random.Random(i*31+seed*7)
                rng_m = random.Random(i*31+seed*7)
                for k in k_band:
                    fp = pathsum_noisy(positions, adj, free_f, src, det, k, eta, rng_f)
                    mp = pathsum_noisy(positions, adj, field, src, det, k, eta, rng_m)
                    for d in det:
                        avg_free[d] += fp.get(d, 0)
                        avg_mass[d] += mp.get(d, 0)

            tf = sum(avg_free.values())
            tm = sum(avg_mass.values())
            if tf > 0:
                avg_free = {d: p/tf for d, p in avg_free.items()}
            if tm > 0:
                avg_mass = {d: p/tm for d, p in avg_mass.items()}

            grav_shift = centroid_y(avg_mass, positions) - centroid_y(avg_free, positions)
            toward = mass_cy - cy
            attracts = (toward > 0 and grav_shift > 0.05) or (toward < 0 and grav_shift < -0.05)

            # ---- INTERFERENCE: ensemble-averaged V through slits ----
            avg_slit_0 = {d: 0.0 for d in det}  # baseline (mass present, η=0)
            avg_slit_n = {d: 0.0 for d in det}  # noisy (mass present, η>0)

            for i in range(N_real):
                rng_0 = random.Random(i*31+seed*7+1000)
                rng_n = random.Random(i*31+seed*7+1000)
                for k in k_band:
                    p0 = pathsum_noisy(positions, adj, field, src, det, k, 0.0,
                                        rng_0, bi, si)
                    pn = pathsum_noisy(positions, adj, field, src, det, k, eta,
                                        rng_n, bi, si)
                    for d in det:
                        avg_slit_0[d] += p0.get(d, 0)
                        avg_slit_n[d] += pn.get(d, 0)

            t0 = sum(avg_slit_0.values())
            tn = sum(avg_slit_n.values())
            if t0 > 0:
                avg_slit_0 = {d: p/t0 for d, p in avg_slit_0.items()}
            if tn > 0:
                avg_slit_n = {d: p/tn for d, p in avg_slit_n.items()}

            v_base = visibility(avg_slit_0, positions, det)
            v_noisy = visibility(avg_slit_n, positions, det)
            has_interf = v_noisy > 0.05
            has_decoh = (v_base - v_noisy) > 0.02

            if attracts:
                grav_yes += 1
            if has_interf:
                interf_yes += 1
            if has_decoh:
                decoh_yes += 1
            if attracts and has_interf and has_decoh:
                all3 += 1
            n_valid += 1

            print(f"    {seed:4d}  {grav_shift:+7.2f}  {v_noisy:7.3f}  {v_base:7.3f}  "
                  f"{'Y' if attracts else 'n':>7s}  "
                  f"{'Y' if has_interf else 'n':>6s}  "
                  f"{'Y' if has_decoh else 'n':>5s}  "
                  f"{'Y' if attracts and has_interf and has_decoh else 'n':>4s}")

        if n_valid > 0:
            print(f"    ---")
            print(f"    Gravity: {grav_yes}/{n_valid}, Interference: {interf_yes}/{n_valid}, "
                  f"Decoherence: {decoh_yes}/{n_valid}, ALL THREE: {all3}/{n_valid}")
        print()

    print("=" * 70)
    print("CONCLUSION")
    print("=" * 70)
    print()
    print("η=0: gravity+interference (no decoherence)")
    print("η>0: gravity+interference+decoherence on irregular graphs")
    print()
    print("If ALL THREE coexist at moderate η:")
    print("  → Complete unified model with corrected propagator")
    print("  → Phase structure → gravity + interference (deterministic)")
    print("  → Phase noise × path irregularity → decoherence (stochastic)")
    print()
    print("TEST COMPLETE")


if __name__ == "__main__":
    main()
