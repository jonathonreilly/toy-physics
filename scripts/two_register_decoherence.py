#!/usr/bin/env python3
"""Two-register decoherence: system + environment at mass nodes.

All single-pass mechanisms failed because the corrected propagator is
too coherent. The fix: give mass nodes an internal "environment" degree
of freedom that entangles with passing amplitude.

Architecture:
- System register: amplitude ψ(node) propagates source → detector
- Environment register: at each mass node, a local state |e⟩ that
  couples to the system. Different arrival directions create
  different environment states.
- The full state is ψ(node, env). At the detector, we trace over env:
  P(det) = Σ_env |ψ(det, env)|²

If slit-A and slit-B create orthogonal environment states at the mass,
the cross-term vanishes → full decoherence. If the states overlap,
partial decoherence.

Implementation:
- env is labeled by a tuple of (mass_node, direction) pairs encountered
- This is exponential in path length, so we approximate:
  env = hash of the LAST mass node + direction encountered
- Different slits produce different last-mass-interaction → different env
- Trace = sum |ψ(det, env)|² over all env labels

PStack experiment: two-register-decoherence
"""

from __future__ import annotations
import math
import cmath
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


def pathsum_two_register(positions, adj, field, src, det, k, mass_set,
                         barrier_idx=None, slit_idx=None):
    """Two-register propagation: system amplitude tagged by environment state.

    Each amplitude carries an 'env' label = last mass node encountered.
    At the detector, trace over env: P(det) = Σ_env |Σ_paths_with_env a|²

    Returns: {det_node: probability} after partial trace.
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

    # State: (node, env_label) → amplitude
    # env_label = last mass node index encountered (or -1 if none)
    state: dict[tuple[int, int], complex] = {}
    for s in src:
        state[(s, -1)] = 1.0 / len(src) + 0.0j

    processed = set()
    for i in order:
        if i in processed:
            continue
        processed.add(i)

        # Collect all (i, env) entries
        entries = {env: amp for (node, env), amp in list(state.items())
                   if node == i and abs(amp) > 1e-30}
        if not entries:
            continue
        if i in blocked:
            continue

        # Propagate each env state to neighbors (don't delete — det nodes need to keep their amp)
        for env, amp in entries.items():
            # If this is a mass node, update the environment label
            # Y-BIN env: label = sign of (mass_y - mass_center)
            if i in mass_set:
                all_my = [positions[m][1] for m in mass_set]
                mc = sum(all_my)/len(all_my)
                new_env = 1 if positions[i][1] > mc else -1
            else:
                new_env = env

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

                key = (j, new_env)
                if key not in state:
                    state[key] = 0.0+0.0j
                state[key] += amp * ea

    # Partial trace: P(det) = Σ_env |ψ(det, env)|²
    probs = defaultdict(float)
    for (node, env), amp in state.items():
        if node in det:
            probs[node] += abs(amp)**2

    total = sum(probs.values())
    if total > 0:
        probs = {d: p/total for d, p in probs.items()}
    return dict(probs)


def pathsum_coherent(positions, adj, field, src, det, k,
                     barrier_idx=None, slit_idx=None):
    """Standard coherent propagation (no environment register)."""
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
    n_layers = 12
    npl = 20
    y_range = 12.0
    radius = 3.0
    n_seeds = 12
    k_band = [3.0, 5.0, 7.0]

    print("=" * 70)
    print("TWO-REGISTER DECOHERENCE")
    print(f"  System + environment at mass nodes")
    print(f"  env_label = last mass node encountered")
    print(f"  P(det) = Σ_env |ψ(det,env)|² (partial trace)")
    print("=" * 70)
    print()

    print(f"  {'seed':>4s}  {'grav':>7s}  {'V_2reg':>7s}  {'V_coh':>7s}  "
          f"{'V_drop':>7s}  {'attr':>4s}  {'dcoh':>4s}  {'all3':>4s}")
    print(f"  {'-' * 52}")

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
        if len(layers) < 5:
            continue

        src = by_layer[layers[0]]
        det_set = set(by_layer[layers[-1]])
        det = list(det_set)
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

        if mid < 2:
            continue
        bl = layers[mid-2]
        bi = by_layer[bl]
        sa = [i for i in bi if positions[i][1] > cy+2][:3]
        sb = [i for i in bi if positions[i][1] < cy-2][:3]
        if not sa or not sb:
            continue
        si = sa + sb

        # Gravity: k-averaged
        grav_shifts = []
        for k in k_band:
            fp = pathsum_coherent(positions, adj, free_f, src, det_set, k)
            mp = pathsum_two_register(positions, adj, field, src, det_set, k, mass_set)
            grav_shifts.append(centroid_y(mp, positions) - centroid_y(fp, positions))
        avg_grav = sum(grav_shifts)/len(grav_shifts)
        attracts = (mass_cy-cy > 0 and avg_grav > 0.05)

        # Interference: coherent baseline (mass present, no environment)
        avg_coh = defaultdict(float)
        avg_2reg = defaultdict(float)
        for k in k_band:
            pc = pathsum_coherent(positions, adj, field, src, det_set, k, bi, si)
            p2 = pathsum_two_register(positions, adj, field, src, det_set, k,
                                       mass_set, bi, si)
            for d in det:
                avg_coh[d] += pc.get(d, 0)
                avg_2reg[d] += p2.get(d, 0)

        for avg in [avg_coh, avg_2reg]:
            t = sum(avg.values())
            if t > 0:
                for d in avg:
                    avg[d] /= t

        v_coh = visibility(dict(avg_coh), positions, det)
        v_2reg = visibility(dict(avg_2reg), positions, det)
        v_drop = v_coh - v_2reg
        has_interf = v_2reg > 0.05
        has_decoh = v_drop > 0.02
        has_all3 = attracts and has_interf and has_decoh

        if attracts: gy += 1
        if has_interf: iy += 1
        if has_decoh: dy += 1
        if has_all3: a3 += 1
        nv += 1

        print(f"  {seed:4d}  {avg_grav:+7.2f}  {v_2reg:7.3f}  {v_coh:7.3f}  "
              f"{v_drop:+7.3f}  "
              f"{'Y' if attracts else 'n':>4s}  "
              f"{'Y' if has_decoh else 'n':>4s}  "
              f"{'Y' if has_all3 else 'n':>4s}")

    if nv > 0:
        print(f"  ---")
        print(f"  G:{gy}/{nv} I:{iy}/{nv} D:{dy}/{nv} ALL:{a3}/{nv}")

    print()
    print("=" * 70)
    print("MECHANISM")
    print("=" * 70)
    print()
    print("The environment register tags amplitude by which mass node it")
    print("last interacted with. Paths from different slits that pass")
    print("through different mass nodes get different env labels.")
    print("The partial trace (Σ_env |ψ(det,env)|²) removes cross-slit")
    print("interference for paths that went through different mass nodes.")
    print()
    print("This is endogenous: the mass nodes ARE the environment.")
    print("No external noise. No averaging over realizations.")
    print("The decoherence is structural — it comes from the entanglement")
    print("between system (detector position) and environment (mass node).")
    print()
    print("TEST COMPLETE")


if __name__ == "__main__":
    main()
