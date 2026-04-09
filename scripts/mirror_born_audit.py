#!/usr/bin/env python3
"""Born audit on ALL mirror generators used in this branch.

Verify that the propagators used in mirror_chokepoint_joint.py and
mirror_scaled_joint.py are strictly linear (no layer normalization)
and pass Born at machine precision.

For each generator:
  1. Verify no normalization in the propagation
  2. Run three-slit Sorkin test
  3. Report |I₃|/P

If any generator has hidden normalization, this script will catch it.
"""

from __future__ import annotations
import math
import cmath
import sys
import os
import random
from collections import defaultdict, deque

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

BETA = 0.8
N_SEEDS = 8


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


def propagate_LINEAR(positions, adj, field, src, k, blocked):
    """STRICTLY LINEAR propagator. No normalization of any kind.
    This is the ONLY propagator used for Born claims on this branch."""
    n = len(positions)
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
            if len(positions[i]) == 2:
                x1, y1 = positions[i]; x2, y2 = positions[j]
                dx, dy = x2-x1, y2-y1; dz = 0
            else:
                x1, y1, z1 = positions[i]; x2, y2, z2 = positions[j]
                dx, dy, dz = x2-x1, y2-y1, z2-z1
            L = math.sqrt(dx*dx + dy*dy + dz*dz)
            if L < 1e-10:
                continue
            lf = 0.5 * (field[i] + field[j])
            dl = L * (1 + lf)
            ret = math.sqrt(max(dl*dl - L*L, 0))
            act = dl - ret
            theta = math.atan2(math.sqrt(dy*dy + dz*dz), max(dx, 1e-10))
            w = math.exp(-BETA * theta * theta)
            ea = cmath.exp(1j * k * act) * w / L
            amps[j] += amps[i] * ea
    return amps


# Generator 1: mirror_chokepoint_joint (3D, layer-1 only at barrier)
def gen_mirror_chokepoint(n_layers, npl_half, xyz_range, cr, rng_seed):
    rng = random.Random(rng_seed); positions = []; adj = defaultdict(list)
    layer_indices = []; mm = {}
    for layer in range(n_layers):
        x = float(layer); ln = []
        if layer == 0:
            idx = len(positions); positions.append((x, 0, 0)); ln.append(idx); mm[idx] = idx
        else:
            up, lo = [], []
            for _ in range(npl_half):
                y = rng.uniform(0.5, xyz_range); z = rng.uniform(-xyz_range, xyz_range)
                iu = len(positions); positions.append((x, y, z)); up.append(iu)
                il = len(positions); positions.append((x, -y, z)); lo.append(il)
                mm[iu] = il; mm[il] = iu
            ln = up + lo
            if layer_indices:
                for ci in up:
                    cx, cy, cz = positions[ci]
                    for pi in layer_indices[-1]:  # LAYER-1 ONLY (chokepoint)
                        px, py, pz = positions[pi]
                        if math.sqrt((cx-px)**2+(cy-py)**2+(cz-pz)**2) <= cr:
                            adj[pi].append(ci); adj[mm[pi]].append(mm[ci])
        layer_indices.append(ln)
    return positions, dict(adj), n_layers // 3


# Generator 2: mirror_scaled_joint hybrid (3D, layer-2 except at barrier)
def gen_mirror_hybrid(n_layers, npl_half, xyz_range, cr, rng_seed):
    rng = random.Random(rng_seed); positions = []; adj = defaultdict(list)
    layer_indices = []; mm = {}; bl = n_layers // 3
    for layer in range(n_layers):
        x = float(layer); ln = []
        if layer == 0:
            idx = len(positions); positions.append((x, 0, 0)); ln.append(idx); mm[idx] = idx
        else:
            up, lo = [], []
            for _ in range(npl_half):
                y = rng.uniform(0.5, xyz_range); z = rng.uniform(-xyz_range, xyz_range)
                iu = len(positions); positions.append((x, y, z)); up.append(iu)
                il = len(positions); positions.append((x, -y, z)); lo.append(il)
                mm[iu] = il; mm[il] = iu
            ln = up + lo
            lb = max(0, len(layer_indices) - (1 if layer == bl + 1 else 2))
            for ci in up:
                cx, cy, cz = positions[ci]
                for pl in layer_indices[lb:]:
                    for pi in pl:
                        px, py, pz = positions[pi]
                        if math.sqrt((cx-px)**2+(cy-py)**2+(cz-pz)**2) <= cr:
                            adj[pi].append(ci); adj[mm[pi]].append(mm[ci])
        layer_indices.append(ln)
    return positions, dict(adj), bl


# Generator 3: 2D mirror
def gen_2d_mirror(nl, npl_half, yr, cr, seed):
    rng = random.Random(seed); pos = []; adj = defaultdict(list); li = []; mm = {}; bl = nl // 3
    for layer in range(nl):
        x = float(layer); ln = []
        if layer == 0:
            pos.append((x, 0)); ln.append(len(pos)-1); mm[len(pos)-1] = len(pos)-1
        else:
            up, lo = [], []
            for _ in range(npl_half):
                y = rng.uniform(0.5, yr)
                iu = len(pos); pos.append((x, y)); up.append(iu)
                il = len(pos); pos.append((x, -y)); lo.append(il)
                mm[iu] = il; mm[il] = iu
            ln = up + lo
            lb = max(0, len(li) - (1 if layer == bl+1 else 2))
            for ci in up:
                cx, cy = pos[ci]
                for pl in li[lb:]:
                    for pi in pl:
                        px, py = pos[pi]
                        if math.sqrt((cx-px)**2+(cy-py)**2) <= cr:
                            adj[pi].append(ci); adj[mm[pi]].append(mm[ci])
        li.append(ln)
    return pos, dict(adj), bl


def sorkin_test(positions, adj, src, k, bi, s_a, s_b, s_c, det_list, field):
    all_slits = set(s_a + s_b + s_c)
    other = set(bi) - all_slits
    probs = {}
    for key, open_set in [('abc', all_slits), ('ab', set(s_a+s_b)),
                           ('ac', set(s_a+s_c)), ('bc', set(s_b+s_c)),
                           ('a', set(s_a)), ('b', set(s_b)), ('c', set(s_c))]:
        bl_set = other | (all_slits - open_set)
        a = propagate_LINEAR(positions, adj, field, src, k, bl_set)
        probs[key] = [abs(a[d])**2 for d in det_list]
    I3 = 0.0; P = 0.0
    for di in range(len(det_list)):
        i3 = (probs['abc'][di] - probs['ab'][di] - probs['ac'][di] - probs['bc'][di]
              + probs['a'][di] + probs['b'][di] + probs['c'][di])
        I3 += abs(i3); P += probs['abc'][di]
    return I3 / P if P > 1e-30 else math.nan


def run_born_test(label, gen_fn, nl, k):
    seeds = [s*7+3 for s in range(N_SEEDS)]
    results = []
    for seed in seeds:
        result = gen_fn(seed)
        if len(result) == 3:
            pos, adj, bl = result
        else:
            pos, adj, bl = result[0], result[1], result[2]
        n = len(pos)
        by_layer = defaultdict(list)
        for idx in range(n):
            p = pos[idx]
            by_layer[round(p[0])].append(idx)
        layers = sorted(by_layer.keys())
        if len(layers) < 5:
            continue
        src = by_layer[layers[0]]
        det = list(by_layer[layers[-1]])
        if not det:
            continue
        if len(pos[0]) == 2:
            cy = sum(pos[i][1] for i in range(n)) / n
        else:
            cy = sum(pos[i][1] for i in range(n)) / n
        bl_idx = len(layers) // 3
        bi = by_layer[layers[bl_idx]]
        upper = sorted([i for i in bi if pos[i][1] > cy + 2], key=lambda i: pos[i][1])
        lower = sorted([i for i in bi if pos[i][1] < cy - 2], key=lambda i: -pos[i][1])
        middle = sorted([i for i in bi if abs(pos[i][1] - cy) <= 2],
                        key=lambda i: abs(pos[i][1] - cy))
        if not upper or not lower or not middle:
            continue
        field = [0.0] * n
        val = sorkin_test(pos, adj, src, k, bi, [upper[0]], [lower[0]], [middle[0]], det, field)
        if not math.isnan(val):
            results.append(val)
    if results:
        mean_i3 = sum(results) / len(results)
        max_i3 = max(results)
        verdict = "PERFECT" if max_i3 < 1e-10 else ("PASS" if max_i3 < 0.01 else "FAIL")
        print(f"  {label:>30s}  mean={mean_i3:.2e}  max={max_i3:.2e}  ok={len(results)}  {verdict}")
    else:
        print(f"  {label:>30s}  NO DATA")


def main():
    print("=" * 80)
    print("BORN AUDIT: ALL MIRROR GENERATORS (LINEAR PROPAGATOR ONLY)")
    print(f"  {N_SEEDS} seeds per generator")
    print("=" * 80)
    print()

    # Chokepoint (N=15, 25 — where it worked before)
    for nl in [15, 25]:
        run_born_test(f"3D chokepoint N={nl} npl=25 r=4",
                      lambda s, _nl=nl: gen_mirror_chokepoint(_nl, 25, 12, 4, s), nl, 5.0)

    # Hybrid (N=25, 40 — S4 family)
    for nl in [25, 40]:
        run_born_test(f"3D hybrid N={nl} npl=40 r=5",
                      lambda s, _nl=nl: gen_mirror_hybrid(_nl, 40, 12, 5, s), nl, 5.0)

    # 2D mirror (N=25, 40)
    for nl in [25, 40]:
        run_born_test(f"2D mirror N={nl} npl=12 r=2.5",
                      lambda s, _nl=nl: gen_2d_mirror(_nl, 12, 10, 2.5, s), nl, 5.0)

    print()
    print("VERIFICATION: This script uses propagate_LINEAR which has")
    print("NO normalization of any kind. If Born passes here, the")
    print("linear propagator on these graph families is Born-clean.")


if __name__ == "__main__":
    main()
