#!/usr/bin/env python3
"""Two-register decoherence with mass BETWEEN slits.

Previous finding: mass downstream of slits can't distinguish which slit
amplitude came from (both paths traverse same mass nodes).

Fix: place mass nodes in the barrier layer, between the two slits.
Slit-A paths pass near upper mass nodes, slit-B near lower mass nodes.
The environment records which mass region was traversed → which-slit info.

On generated DAGs: place mass in the barrier layer, between the slit
groups. Each slit's amplitude passes through different mass nodes.

PStack experiment: between-slit-decoherence
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


def pathsum_two_register(positions, adj, field, src, det_set, k, mass_set,
                         blocked=None):
    """Two-register: env = last mass node index. Partial trace at detector."""
    n = len(positions)
    blocked = blocked or set()

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

    state: dict[tuple[int, int], complex] = {}
    for s in src:
        state[(s, -1)] = 1.0/len(src) + 0.0j

    processed = set()
    for i in order:
        if i in processed:
            continue
        processed.add(i)
        entries = {env: amp for (node, env), amp in list(state.items())
                   if node == i and abs(amp) > 1e-30}
        if not entries or i in blocked:
            continue

        for env, amp in entries.items():
            new_env = i if i in mass_set else env
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
                state[key] += amp*ea

    # Partial trace
    probs = defaultdict(float)
    for (node, env), amp in state.items():
        if node in det_set:
            probs[node] += abs(amp)**2
    total = sum(probs.values())
    if total > 0:
        probs = {d: p/total for d, p in probs.items()}
    return dict(probs)


def pathsum_coherent(positions, adj, field, src, det_set, k, blocked=None):
    """Standard coherent propagation."""
    n = len(positions)
    blocked = blocked or set()
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

    probs = {d: abs(amps[d])**2 for d in det_set}
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
    n_layers = 15
    npl = 25
    y_range = 12.0
    radius = 3.0
    n_seeds = 12
    k_band = [3.0, 5.0, 7.0]

    print("=" * 70)
    print("BETWEEN-SLIT DECOHERENCE")
    print(f"  Mass in barrier layer, between slit groups")
    print(f"  Two-register: env = last mass node, partial trace")
    print("=" * 70)
    print()

    print(f"  {'seed':>4s}  {'grav':>7s}  {'V_2reg':>7s}  {'V_coh':>7s}  "
          f"{'V_drop':>7s}  {'n_mass':>6s}  {'attr':>4s}  {'dcoh':>4s}  {'all3':>4s}")
    print(f"  {'-' * 60}")

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
        det = set(by_layer[layers[-1]])
        if not det:
            continue

        all_ys = [y for _, y in positions]
        cy = sum(all_ys)/len(all_ys)

        # Barrier at 1/3 of the way through
        barrier_layer_idx = len(layers) // 3
        bl = layers[barrier_layer_idx]
        bi = by_layer[bl]

        # Slits: top and bottom groups
        sa = [i for i in bi if positions[i][1] > cy + 3][:3]
        sb = [i for i in bi if positions[i][1] < cy - 3][:3]
        if not sa or not sb:
            continue
        si = set(sa + sb)

        # Mass: nodes in the barrier layer BETWEEN the slits
        # (not in slit groups, near center)
        mass_in_barrier = [i for i in bi
                           if i not in si
                           and abs(positions[i][1] - cy) < 4]
        if len(mass_in_barrier) < 2:
            continue
        mass_set = set(mass_in_barrier)
        mass_cy = sum(positions[i][1] for i in mass_in_barrier)/len(mass_in_barrier)

        # Also add mass in a downstream layer for gravity
        grav_layer = layers[2 * len(layers) // 3]
        grav_mass = [i for i in by_layer[grav_layer] if positions[i][1] > cy + 1]
        full_mass = mass_set | set(grav_mass)

        field = compute_field(positions, adj, list(full_mass))
        free_f = [0.0]*n

        blocked = set(bi) - si

        # ---- GRAVITY ----
        grav_shifts = []
        for k in k_band:
            fp = pathsum_coherent(positions, adj, free_f, src, det, k)
            mp = pathsum_two_register(positions, adj, field, src, det, k, mass_set)
            fcy = centroid_y(fp, positions)
            mcy = centroid_y(mp, positions)
            grav_shifts.append(mcy - fcy)
        avg_grav = sum(grav_shifts)/len(grav_shifts)
        # Use grav_mass centroid for direction check
        if grav_mass:
            grav_cy = sum(positions[i][1] for i in grav_mass)/len(grav_mass)
            attracts = (grav_cy - cy > 0 and avg_grav > 0.05) or \
                       (grav_cy - cy < 0 and avg_grav < -0.05)
        else:
            attracts = False

        # ---- INTERFERENCE + DECOHERENCE ----
        avg_coh = defaultdict(float)
        avg_2reg = defaultdict(float)
        for k in k_band:
            # Coherent baseline: mass field present, no env register
            pc = pathsum_coherent(positions, adj, field, src, det, k, blocked)
            # Two-register: env at barrier-mass nodes
            p2 = pathsum_two_register(positions, adj, field, src, det, k,
                                       mass_set, blocked)
            for d in det:
                avg_coh[d] += pc.get(d, 0)
                avg_2reg[d] += p2.get(d, 0)

        for avg in [avg_coh, avg_2reg]:
            t = sum(avg.values())
            if t > 0:
                for d in avg:
                    avg[d] /= t

        v_coh = visibility(dict(avg_coh), positions, list(det))
        v_2reg = visibility(dict(avg_2reg), positions, list(det))
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
              f"{v_drop:+7.3f}  {len(mass_in_barrier):6d}  "
              f"{'Y' if attracts else 'n':>4s}  "
              f"{'Y' if has_decoh else 'n':>4s}  "
              f"{'Y' if has_all3 else 'n':>4s}")

    if nv > 0:
        print(f"  ---")
        print(f"  G:{gy}/{nv} I:{iy}/{nv} D:{dy}/{nv} ALL:{a3}/{nv}")

    print()
    print("GEOMETRY: mass between slits → each slit couples to different mass nodes")
    print("→ env distinguishes which slit → partial trace produces decoherence")
    print()
    print("TEST COMPLETE")


if __name__ == "__main__":
    main()
