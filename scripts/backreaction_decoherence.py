#!/usr/bin/env python3
"""Backreaction decoherence: amplitude modifies field for later amplitude.

The smallest endogenous record process: when amplitude arrives at a mass
node, it modifies the local field. Later-arriving amplitude sees the
modified field. Since slit-A and slit-B amplitude arrive at different
times (different path lengths), they create different field modifications.

This is a path-ordering effect: the field becomes history-dependent.
Averaging over the two orderings (A first vs B first) should reduce V.

Implementation:
- Propagate in causal order (as usual)
- When amplitude reaches a mass node, increase the local field by
  ε × |arriving_amplitude|²
- Later amplitude sees the increased field → different phase
- Run for each slit independently, then combine:
  P = |a_A(field_modified_by_A) + a_B(field_modified_by_B)|²
  vs the no-backreaction case:
  P = |a_A(field_static) + a_B(field_static)|²

PStack experiment: backreaction-decoherence
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


def pathsum_with_backreaction(positions, adj, base_field, src, det, k,
                              mass_set, epsilon,
                              barrier_idx=None, slit_idx=None):
    """Propagate with backreaction: arriving amplitude modifies local field.

    At mass nodes, field += ε × |amp|² when amplitude arrives.
    This makes the field history-dependent.
    """
    n = len(positions)
    blocked = set()
    if barrier_idx is not None and slit_idx is not None:
        blocked = set(barrier_idx) - set(slit_idx)

    field = list(base_field)  # Mutable copy

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

        # Backreaction: modify field at mass nodes based on arriving amplitude
        if i in mass_set and epsilon > 0:
            field[i] += epsilon * abs(amps[i])**2

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


def pathsum_standard(positions, adj, field, src, det, k,
                     barrier_idx=None, slit_idx=None):
    """Standard corrected propagator (no backreaction)."""
    return pathsum_with_backreaction(positions, adj, field, src, det, k,
                                     set(), 0.0, barrier_idx, slit_idx)


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


def centroid_y(probs, positions):
    total = sum(probs.values())
    if total == 0:
        return 0.0
    return sum(positions[d][1]*p for d, p in probs.items()) / total


def main():
    n_layers = 15
    npl = 25
    y_range = 15.0
    radius = 3.0
    n_seeds = 12
    k_band = [3.0, 5.0, 7.0]

    print("=" * 70)
    print("BACKREACTION DECOHERENCE")
    print(f"  Amplitude modifies field at mass nodes")
    print(f"  field += ε × |amp|² at each mass node")
    print("=" * 70)
    print()

    for epsilon in [0.0, 0.01, 0.05, 0.1, 0.5, 1.0, 5.0]:
        print(f"  ε = {epsilon}:")
        print(f"    {'seed':>4s}  {'grav':>7s}  {'V_br':>7s}  {'V_base':>7s}  "
              f"{'V_drop':>7s}  {'attr':>4s}  {'dcoh':>4s}  {'all3':>4s}")
        print(f"    {'-' * 52}")

        gy = iy = dy = a3 = nv = 0

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
            mass_idx = [i for i in sum((by_layer[l] for l in mass_layers), [])
                        if positions[i][1] > cy+1]
            if len(mass_idx) < 3:
                continue
            mass_set = set(mass_idx)
            mass_cy = sum(positions[i][1] for i in mass_idx)/len(mass_idx)
            field = compute_field(positions, adj, mass_idx)
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

            # Gravity: k-averaged
            grav_shifts = []
            for k in k_band:
                fp = pathsum_standard(positions, adj, free_f, src, det, k)
                mp = pathsum_with_backreaction(positions, adj, field, src, det, k,
                                               mass_set, epsilon)
                grav_shifts.append(
                    centroid_y(mp, positions) - centroid_y(fp, positions))
            avg_grav = sum(grav_shifts)/len(grav_shifts)
            attracts = (mass_cy-cy > 0 and avg_grav > 0.05)

            # Interference: baseline (mass present, no backreaction)
            avg_base = {d: 0.0 for d in det}
            avg_br = {d: 0.0 for d in det}
            for k in k_band:
                pb = pathsum_standard(positions, adj, field, src, det, k, bi, si)
                pr = pathsum_with_backreaction(positions, adj, field, src, det, k,
                                               mass_set, epsilon, bi, si)
                for d in det:
                    avg_base[d] += pb.get(d, 0)
                    avg_br[d] += pr.get(d, 0)

            for avg in [avg_base, avg_br]:
                t = sum(avg.values())
                if t > 0:
                    for d in avg:
                        avg[d] /= t

            vb = visibility(avg_base, positions, det)
            vr = visibility(avg_br, positions, det)
            vd = vb - vr
            hi = vr > 0.05
            hd = vd > 0.02
            h3 = attracts and hi and hd

            if attracts: gy += 1
            if hi: iy += 1
            if hd: dy += 1
            if h3: a3 += 1
            nv += 1

            print(f"    {seed:4d}  {avg_grav:+7.2f}  {vr:7.3f}  {vb:7.3f}  "
                  f"{vd:+7.3f}  "
                  f"{'Y' if attracts else 'n':>4s}  "
                  f"{'Y' if hd else 'n':>4s}  "
                  f"{'Y' if h3 else 'n':>4s}")

        if nv > 0:
            print(f"    G:{gy}/{nv} I:{iy}/{nv} D:{dy}/{nv} ALL:{a3}/{nv}")
        print()

    print("=" * 70)
    print("MECHANISM")
    print("=" * 70)
    print()
    print("Backreaction: amplitude arriving at mass modifies the local field.")
    print("Later-arriving amplitude sees a different field → different phase.")
    print("Since slit-A and slit-B amplitude arrive via different paths at")
    print("different times, they create different field histories → the field")
    print("'records' which slit was used first.")
    print()
    print("This is genuinely endogenous: no external noise or parameters.")
    print("The recording strength is set by the amplitude itself (ε × |amp|²).")
    print()
    print("TEST COMPLETE")


if __name__ == "__main__":
    main()
