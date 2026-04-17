#!/usr/bin/env python3
"""Endogenous decoherence via field fluctuation.

Opacity blocks paths → hurts gravity. Instead: oscillating field.

The mass's delay field fluctuates: at each oscillation phase,
the field strength varies (e.g., between 0.5× and 1.5× the mean).
Paths accumulate different action depending on the field state.
Average over states → fringes wash out. Mean field → gravity survives.

This models: the persistent pattern's internal dynamics modulate
the local delay, creating a time-dependent environment for passing
amplitude.

PStack experiment: endogenous-field-fluctuation
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


def pathsum_corrected(positions, adj, field, src, det, k,
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
            ea = cmath.exp(1j*k*act)/(L**1.0)
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


def fluctuated_field(base_field, mass_idx, amplitude, phase_idx, n_phases):
    """Modulate mass field strength: f_mod = f × (1 + A × sin(2π × phase/n_phases))."""
    ms = set(mass_idx)
    mod = 1.0 + amplitude * math.sin(2 * math.pi * phase_idx / n_phases)
    return [f * mod if i in ms or f > 0.01 else f
            for i, f in enumerate(base_field)]


def main():
    n_layers = 15
    npl = 25
    y_range = 15.0
    radius = 3.0
    n_seeds = 12
    k_band = [3.0, 5.0, 7.0]
    n_phases = 6  # oscillation states

    print("=" * 70)
    print("ENDOGENOUS DECOHERENCE: Field Fluctuation")
    print(f"  Corrected propagator (1/L^p)")
    print(f"  Field oscillation: {n_phases} phases, amplitude A varied")
    print("=" * 70)
    print()

    for A in [0.0, 0.1, 0.3, 0.5, 0.8, 1.0]:
        print(f"  Fluctuation amplitude A = {A}:")
        print(f"    {'seed':>4s}  {'grav':>7s}  {'V_ens':>7s}  {'V_base':>7s}  "
              f"{'V_drop':>7s}  {'attr':>4s}  {'dcoh':>4s}  {'all3':>4s}")
        print(f"    {'-' * 52}")

        grav_yes = interf_yes = decoh_yes = all3_c = n_valid = 0

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

            mass_layers = [layers[mid-1], layers[mid], layers[mid+1]]
            mass_idx = []
            for l in mass_layers:
                mass_idx.extend(i for i in by_layer[l] if positions[i][1] > cy+1)
            if len(mass_idx) < 3:
                continue
            mass_cy_val = sum(positions[i][1] for i in mass_idx)/len(mass_idx)
            base_field = compute_field(positions, adj, mass_idx)
            free_f = [0.0]*n

            if mid < 3:
                continue
            bl = layers[mid-3]
            bi = by_layer[bl]
            sa = [i for i in bi if positions[i][1] > cy+2][:3]
            sb = [i for i in bi if positions[i][1] < cy-2][:3]
            if not sa or not sb:
                continue
            si = sa + sb

            # ---- Average over oscillation phases ----
            avg_free_g = {d: 0.0 for d in det}
            avg_mass_g = {d: 0.0 for d in det}
            avg_slit_base = {d: 0.0 for d in det}
            avg_slit_fluct = {d: 0.0 for d in det}

            for phase_i in range(n_phases):
                fluct = fluctuated_field(base_field, mass_idx, A, phase_i, n_phases)

                for k in k_band:
                    # Gravity
                    fp = pathsum_corrected(positions, adj, free_f, src, det, k)
                    mp = pathsum_corrected(positions, adj, fluct, src, det, k)
                    for d in det:
                        avg_free_g[d] += fp.get(d, 0)
                        avg_mass_g[d] += mp.get(d, 0)

                    # Interference baseline (mass present, no fluctuation)
                    pb = pathsum_corrected(positions, adj, base_field, src, det, k, bi, si)
                    for d in det:
                        avg_slit_base[d] += pb.get(d, 0)

                    # Interference with fluctuating mass
                    pf = pathsum_corrected(positions, adj, fluct, src, det, k, bi, si)
                    for d in det:
                        avg_slit_fluct[d] += pf.get(d, 0)

            # Normalize
            for avg in [avg_free_g, avg_mass_g, avg_slit_base, avg_slit_fluct]:
                t = sum(avg.values())
                if t > 0:
                    for d in avg:
                        avg[d] /= t

            grav_shift = centroid_y(avg_mass_g, positions) - centroid_y(avg_free_g, positions)
            toward = mass_cy_val - cy
            attracts = (toward > 0 and grav_shift > 0.05)

            v_base = visibility(avg_slit_base, positions, det)
            v_fluct = visibility(avg_slit_fluct, positions, det)
            v_drop = v_base - v_fluct
            has_interf = v_fluct > 0.05
            has_decoh = v_drop > 0.02
            has_all3 = attracts and has_interf and has_decoh

            if attracts: grav_yes += 1
            if has_interf: interf_yes += 1
            if has_decoh: decoh_yes += 1
            if has_all3: all3_c += 1
            n_valid += 1

            print(f"    {seed:4d}  {grav_shift:+7.2f}  {v_fluct:7.3f}  {v_base:7.3f}  "
                  f"{v_drop:+7.3f}  "
                  f"{'Y' if attracts else 'n':>4s}  "
                  f"{'Y' if has_decoh else 'n':>4s}  "
                  f"{'Y' if has_all3 else 'n':>4s}")

        if n_valid > 0:
            print(f"    ---")
            print(f"    G:{grav_yes}/{n_valid} I:{interf_yes}/{n_valid} "
                  f"D:{decoh_yes}/{n_valid} ALL:{all3_c}/{n_valid}")
        print()

    print("TEST COMPLETE")


if __name__ == "__main__":
    main()
