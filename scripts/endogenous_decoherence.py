#!/usr/bin/env python3
"""Endogenous decoherence: oscillating mass nodes toggle the DAG.

Phase noise is a proof-of-concept, not the final mechanism.
The actual decoherence should come from the model's own dynamics.

Mechanism: persistent patterns oscillate (period-3 in the CA).
During propagation, different mass nodes are "active" (opaque) at
different times. This creates an effective environment: the path-sum
averages over the pattern's internal states.

Implementation:
- Mass has N nodes. At each "phase" of the oscillation, a subset
  of size N×f_active are opaque (block paths).
- The path-sum is computed for each oscillation phase separately.
- The ensemble-averaged probability = average over oscillation phases.
- If different phases produce different fringe positions, V drops.

This is endogenous: the mass's own dynamics create the decoherence.
No external noise parameter η.

PStack experiment: endogenous-decoherence
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


def pathsum_with_opaque(positions, adj, field, src, det, k,
                        opaque_set, barrier_idx=None, slit_idx=None):
    """Corrected propagator with opaque (blocking) nodes."""
    n = len(positions)
    blocked = set(opaque_set)
    if barrier_idx is not None and slit_idx is not None:
        blocked |= (set(barrier_idx) - set(slit_idx))

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


def oscillation_phases(mass_indices, n_phases=3, f_active=0.5, rng=None):
    """Generate oscillation phases: different subsets of mass are opaque.

    Each phase has f_active fraction of mass nodes opaque.
    Models period-3 oscillator where different cells are active at
    different times.
    """
    rng = rng or random.Random(42)
    mass_list = list(mass_indices)
    phases = []
    for p in range(n_phases):
        # Rotate which nodes are active
        n_active = max(1, int(len(mass_list) * f_active))
        start = (p * n_active) % len(mass_list)
        active = set()
        for i in range(n_active):
            active.add(mass_list[(start + i) % len(mass_list)])
        phases.append(active)
    return phases


def main():
    n_layers = 15
    npl = 25
    y_range = 15.0
    radius = 3.0
    n_seeds = 12
    k_band = [3.0, 5.0, 7.0]

    print("=" * 70)
    print("ENDOGENOUS DECOHERENCE: Oscillating mass toggles DAG")
    print(f"  Corrected propagator (1/L^p)")
    print(f"  Mass oscillation: period-3, 50% active per phase")
    print("=" * 70)
    print()

    # ================================================================
    # TEST 1: Oscillation phase count sweep
    # ================================================================
    for n_phases in [1, 2, 3, 5, 8]:
        print(f"  n_phases = {n_phases} (f_active = 0.5):")
        print(f"    {'seed':>4s}  {'grav':>7s}  {'V_ens':>7s}  {'V_base':>7s}  "
              f"{'V_drop':>7s}  {'all3':>4s}")
        print(f"    {'-' * 44}")

        grav_yes = interf_yes = decoh_yes = all3_count = n_valid = 0

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
            if len(mass_idx) < 4:
                continue
            mass_cy_val = sum(positions[i][1] for i in mass_idx)/len(mass_idx)
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

            # Generate oscillation phases
            phases = oscillation_phases(mass_idx, n_phases=n_phases, f_active=0.5,
                                        rng=random.Random(seed*17+3))

            # ---- GRAVITY: average centroid shift over oscillation phases ----
            avg_free = {d: 0.0 for d in det}
            avg_mass = {d: 0.0 for d in det}
            for phase_set in phases:
                for k in k_band:
                    fp = pathsum_with_opaque(positions, adj, free_f, src, det, k, set())
                    mp = pathsum_with_opaque(positions, adj, field, src, det, k, phase_set)
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
            toward = mass_cy_val - cy
            attracts = (toward > 0 and grav_shift > 0.05)

            # ---- INTERFERENCE + DECOHERENCE ----
            # Baseline: no oscillation (transparent mass)
            avg_base = {d: 0.0 for d in det}
            for k in k_band:
                pb = pathsum_with_opaque(positions, adj, free_f, src, det, k,
                                         set(), bi, si)
                for d in det:
                    avg_base[d] += pb.get(d, 0)
            tb = sum(avg_base.values())
            if tb > 0:
                avg_base = {d: p/tb for d, p in avg_base.items()}
            v_base = visibility(avg_base, positions, det)

            # Oscillation-averaged: each phase blocks different mass nodes
            avg_osc = {d: 0.0 for d in det}
            for phase_set in phases:
                for k in k_band:
                    po = pathsum_with_opaque(positions, adj, field, src, det, k,
                                             phase_set, bi, si)
                    for d in det:
                        avg_osc[d] += po.get(d, 0)
            to = sum(avg_osc.values())
            if to > 0:
                avg_osc = {d: p/to for d, p in avg_osc.items()}
            v_osc = visibility(avg_osc, positions, det)

            v_drop = v_base - v_osc
            has_interf = v_osc > 0.05
            has_decoh = v_drop > 0.02
            has_all3 = attracts and has_interf and has_decoh

            if attracts: grav_yes += 1
            if has_interf: interf_yes += 1
            if has_decoh: decoh_yes += 1
            if has_all3: all3_count += 1
            n_valid += 1

            print(f"    {seed:4d}  {grav_shift:+7.2f}  {v_osc:7.3f}  {v_base:7.3f}  "
                  f"{v_drop:+7.3f}  "
                  f"{'Y' if has_all3 else 'n':>4s}")

        if n_valid > 0:
            print(f"    ---")
            print(f"    G:{grav_yes}/{n_valid} I:{interf_yes}/{n_valid} "
                  f"D:{decoh_yes}/{n_valid} ALL:{all3_count}/{n_valid}")
        print()

    print("=" * 70)
    print("CONCLUSION")
    print("=" * 70)
    print()
    print("If oscillation produces V_drop > 0.02:")
    print("  → Endogenous decoherence from pattern dynamics")
    print("  → No external noise needed")
    print("  → The mass's own oscillation creates which-path information")
    print()
    print("TEST COMPLETE")


if __name__ == "__main__":
    main()
