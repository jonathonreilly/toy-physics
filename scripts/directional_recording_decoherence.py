#!/usr/bin/env python3
"""Directional recording: mass nodes add direction-dependent phase.

The smallest endogenous decoherence mechanism: when amplitude arrives
at a mass node, it picks up a phase that depends on the DIRECTION of
the incoming edge. Since different slits send amplitude from different
angles, each slit's contribution gets a different phase kick.

Average over N_env "environment states" (random direction→phase mappings).
Each state assigns a random phase offset to each incoming direction at
each mass node. The probability for each state is coherent (path-sum),
but the ensemble average washes out interference between slits.

This is endogenous: mass nodes interact with passing amplitude via
their local geometry. No external noise. The "environment" is the
mass's internal degrees of freedom (which direction it last interacted).

PStack experiment: directional-recording-decoherence
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


def pathsum_directional(positions, adj, field, src, det, k,
                        mass_set, dir_phases,
                        barrier_idx=None, slit_idx=None):
    """Corrected propagator with direction-dependent phase at mass nodes.

    dir_phases: dict mapping (mass_node_idx, incoming_edge_angle_bin) → phase
    """
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

            # Direction-dependent phase at mass nodes
            if j in mass_set:
                dy = y2 - y1
                dx = x2 - x1
                angle_bin = int(math.atan2(dy, dx) * 4 / math.pi + 0.5) % 8
                extra_phase = dir_phases.get((j, angle_bin), 0.0)
                ea *= cmath.exp(1j * extra_phase)

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


def generate_env_state(mass_idx, strength, rng):
    """Generate one environment state: random phase per (mass_node, direction)."""
    phases = {}
    for m in mass_idx:
        for angle_bin in range(8):
            phases[(m, angle_bin)] = strength * rng.gauss(0, 1)
    return phases


def main():
    n_layers = 15
    npl = 25
    y_range = 15.0
    radius = 3.0
    n_seeds = 12
    k_band = [3.0, 5.0, 7.0]
    N_env = 30  # environment states

    print("=" * 70)
    print("DIRECTIONAL RECORDING DECOHERENCE")
    print(f"  Mass nodes add direction-dependent phase")
    print(f"  {N_env} environment states, corrected propagator (1/L^p)")
    print("=" * 70)
    print()

    for strength in [0.0, 0.1, 0.3, 0.5, 1.0, 2.0]:
        print(f"  Recording strength σ = {strength}:")
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
            mass_set = set(mass_idx)
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

            # ---- Ensemble over environment states ----
            avg_free_g = {d: 0.0 for d in det}
            avg_mass_g = {d: 0.0 for d in det}
            avg_slit_base = {d: 0.0 for d in det}
            avg_slit_rec = {d: 0.0 for d in det}

            for env_i in range(N_env):
                rng = random.Random(env_i*31+seed*7)
                dir_phases = generate_env_state(mass_idx, strength, rng)
                null_phases = {}  # no recording

                for k in k_band:
                    # Gravity: free vs mass with recording
                    fp = pathsum_directional(positions, adj, free_f, src, det, k,
                                             set(), null_phases)
                    mp = pathsum_directional(positions, adj, field, src, det, k,
                                             mass_set, dir_phases)
                    for d in det:
                        avg_free_g[d] += fp.get(d, 0)
                        avg_mass_g[d] += mp.get(d, 0)

                    # Interference: baseline (mass present, no recording)
                    pb = pathsum_directional(positions, adj, field, src, det, k,
                                             mass_set, null_phases, bi, si)
                    for d in det:
                        avg_slit_base[d] += pb.get(d, 0)

                    # Interference: with directional recording at mass
                    pr = pathsum_directional(positions, adj, field, src, det, k,
                                             mass_set, dir_phases, bi, si)
                    for d in det:
                        avg_slit_rec[d] += pr.get(d, 0)

            # Normalize
            for avg in [avg_free_g, avg_mass_g, avg_slit_base, avg_slit_rec]:
                t = sum(avg.values())
                if t > 0:
                    for d in avg:
                        avg[d] /= t

            grav_shift = centroid_y(avg_mass_g, positions) - centroid_y(avg_free_g, positions)
            toward = mass_cy_val - cy
            attracts = (toward > 0 and grav_shift > 0.05)

            v_base = visibility(avg_slit_base, positions, det)
            v_rec = visibility(avg_slit_rec, positions, det)
            v_drop = v_base - v_rec
            has_interf = v_rec > 0.05
            has_decoh = v_drop > 0.02
            has_all3 = attracts and has_interf and has_decoh

            if attracts: grav_yes += 1
            if has_interf: interf_yes += 1
            if has_decoh: decoh_yes += 1
            if has_all3: all3_c += 1
            n_valid += 1

            print(f"    {seed:4d}  {grav_shift:+7.2f}  {v_rec:7.3f}  {v_base:7.3f}  "
                  f"{v_drop:+7.3f}  "
                  f"{'Y' if attracts else 'n':>4s}  "
                  f"{'Y' if has_decoh else 'n':>4s}  "
                  f"{'Y' if has_all3 else 'n':>4s}")

        if n_valid > 0:
            print(f"    ---")
            print(f"    G:{grav_yes}/{n_valid} I:{interf_yes}/{n_valid} "
                  f"D:{decoh_yes}/{n_valid} ALL:{all3_c}/{n_valid}")
        print()

    print("=" * 70)
    print("MECHANISM")
    print("=" * 70)
    print()
    print("Directional recording: mass node adds phase that depends on")
    print("which direction amplitude arrived from. Different slits send")
    print("amplitude from different angles → different phases → ensemble")
    print("average washes out cross-slit interference terms.")
    print()
    print("This is endogenous: the mass's spatial embedding creates the")
    print("directional sensitivity. No external noise parameter needed")
    print("(σ is the coupling strength, not an external input).")
    print()
    print("TEST COMPLETE")


if __name__ == "__main__":
    main()
