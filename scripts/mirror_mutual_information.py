#!/usr/bin/env python3
"""Mutual information on mirror DAGs: committed audit-grade script.

Computes I(slit_label; detector_y_bin) on:
  1. 3D S4 mirror (hybrid chokepoint, NPL_HALF=25, r=5)
  2. 3D random baseline (NPL=50, r=5)
  3. 2D mirror (NPL_HALF=12, r=2.5)
  4. 2D random baseline (NPL=24, r=2.5)

All measurements at single k=5.0 using strictly linear propagator.
Output: MI in bits, H(detector), H(detector|slit) for each N.
"""

from __future__ import annotations
import math
import cmath
import sys
import os
import random
import time
from collections import defaultdict, deque

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

BETA = 0.8
K = 5.0
N_SEEDS = 16
N_YBINS = 8
LAM = 10.0


def _topo_order(adj, n):
    in_deg = [0] * n
    for nbs in adj.values():
        for j in nbs: in_deg[j] += 1
    q = deque(i for i in range(n) if in_deg[i] == 0); order = []
    while q:
        i = q.popleft(); order.append(i)
        for j in adj.get(i, []):
            in_deg[j] -= 1
            if in_deg[j] == 0: q.append(j)
    return order


# ---- 3D generators ----

def gen_3d_mirror(nl, npl_half, yr, cr, seed):
    rng = random.Random(seed); pos = []; adj = defaultdict(list); li = []; mm = {}; bl = nl//3
    for layer in range(nl):
        x = float(layer); ln = []
        if layer == 0:
            pos.append((x, 0, 0)); ln.append(len(pos)-1); mm[len(pos)-1] = len(pos)-1
        else:
            up, lo = [], []
            for _ in range(npl_half):
                y = rng.uniform(0.5, yr); z = rng.uniform(-yr, yr)
                iu = len(pos); pos.append((x, y, z)); up.append(iu)
                il = len(pos); pos.append((x, -y, z)); lo.append(il)
                mm[iu] = il; mm[il] = iu
            ln = up + lo
            lb = max(0, len(li) - (1 if layer == bl+1 else 2))
            for ci in up:
                cx, cy, cz = pos[ci]
                for pl in li[lb:]:
                    for pi in pl:
                        px, py, pz = pos[pi]
                        if math.sqrt((cx-px)**2+(cy-py)**2+(cz-pz)**2) <= cr:
                            adj[pi].append(ci); adj[mm[pi]].append(mm[ci])
        li.append(ln)
    return pos, dict(adj), bl


def gen_3d_random(nl, npl, yr, cr, seed):
    rng = random.Random(seed); pos = []; adj = defaultdict(list); li = []; bl = nl//3
    for layer in range(nl):
        x = float(layer); ln = []
        if layer == 0:
            pos.append((x, 0, 0)); ln.append(len(pos)-1)
        else:
            for _ in range(npl):
                y = rng.uniform(-yr, yr); z = rng.uniform(-yr, yr)
                idx = len(pos); pos.append((x, y, z)); ln.append(idx)
                lb = max(0, len(li) - (1 if layer == bl+1 else 2))
                for pl in li[lb:]:
                    for pi in pl:
                        px, py, pz = pos[pi]
                        if math.sqrt((x-px)**2+(y-py)**2+(z-pz)**2) <= cr:
                            adj[pi].append(idx)
        li.append(ln)
    return pos, dict(adj), bl


# ---- 2D generators ----

def gen_2d_mirror(nl, npl_half, yr, cr, seed):
    rng = random.Random(seed); pos = []; adj = defaultdict(list); li = []; mm = {}; bl = nl//3
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


def gen_2d_random(nl, npl, yr, cr, seed):
    rng = random.Random(seed); pos = []; adj = defaultdict(list); li = []; bl = nl//3
    for layer in range(nl):
        x = float(layer); ln = []
        if layer == 0:
            pos.append((x, 0)); ln.append(len(pos)-1)
        else:
            for _ in range(npl):
                y = rng.uniform(-yr, yr)
                idx = len(pos); pos.append((x, y)); ln.append(idx)
                lb = max(0, len(li) - (1 if layer == bl+1 else 2))
                for pl in li[lb:]:
                    for pi in pl:
                        px, py = pos[pi]
                        if math.sqrt((x-px)**2+(y-py)**2) <= cr:
                            adj[pi].append(idx)
        li.append(ln)
    return pos, dict(adj), bl


# ---- propagator (strictly linear, NO normalization) ----

def propagate(positions, adj, field, src, k, blocked):
    n = len(positions); order = _topo_order(adj, n); amps = [0j] * n
    for s in src: amps[s] = 1.0 / len(src)
    ndim = len(positions[0])
    for i in order:
        if abs(amps[i]) < 1e-30 or i in blocked: continue
        for j in adj.get(i, []):
            if j in blocked: continue
            pi, pj = positions[i], positions[j]
            dx = pj[0] - pi[0]
            if ndim == 2:
                dy = pj[1] - pi[1]; dz = 0
            else:
                dy = pj[1] - pi[1]; dz = pj[2] - pi[2]
            L = math.sqrt(dx*dx + dy*dy + dz*dz)
            if L < 1e-10: continue
            lf = 0.5*(field[i]+field[j]); dl = L*(1+lf)
            ret = math.sqrt(max(dl*dl-L*L, 0)); act = dl-ret
            theta = math.atan2(math.sqrt(dy*dy+dz*dz), max(dx, 1e-10))
            amps[j] += amps[i] * cmath.exp(1j*k*act) * math.exp(-BETA*theta*theta) / L
    return amps


# ---- measurement ----

def compute_mi(positions, adj, nl, k):
    n = len(positions); ndim = len(positions[0])
    by_layer = defaultdict(list)
    for idx in range(n): by_layer[round(positions[idx][0])].append(idx)
    layers = sorted(by_layer.keys())
    if len(layers) < 5: return None
    src = by_layer[layers[0]]; det = list(by_layer[layers[-1]])
    if not det: return None
    cy = sum(positions[i][1] for i in range(n)) / n
    slit_thresh = 2 if ndim == 2 else 3
    bl_idx = len(layers) // 3; bi = by_layer[layers[bl_idx]]
    sa = [i for i in bi if positions[i][1] > cy + slit_thresh][:3]
    sb = [i for i in bi if positions[i][1] < cy - slit_thresh][:3]
    if not sa or not sb: return None
    blocked = set(bi) - set(sa + sb)
    gl = layers[2*len(layers)//3]
    mass = [i for i in by_layer[gl] if positions[i][1] > cy + 1][:5]
    if not mass: return None
    field = [0.0] * n
    for m in mass:
        pm = positions[m]
        for i in range(n):
            pi = positions[i]
            r = math.sqrt(sum((a-b)**2 for a, b in zip(pi, pm))) + 0.1
            field[i] += 0.1 / r

    pa = propagate(positions, adj, field, src, k, blocked | set(sb))
    pb = propagate(positions, adj, field, src, k, blocked | set(sa))

    yr = 10 if ndim == 2 else 12
    bw = 2*yr / N_YBINS
    prob_a = [0.0]*N_YBINS; prob_b = [0.0]*N_YBINS
    for d in det:
        b = max(0, min(N_YBINS-1, int((positions[d][1]+yr)/bw)))
        prob_a[b] += abs(pa[d])**2; prob_b[b] += abs(pb[d])**2
    na = sum(prob_a); nb = sum(prob_b)
    if na < 1e-30 or nb < 1e-30: return None
    prob_a = [p/na for p in prob_a]; prob_b = [p/nb for p in prob_b]

    H_det = 0; H_cond = 0
    for b in range(N_YBINS):
        pm = 0.5*prob_a[b] + 0.5*prob_b[b]
        if pm > 1e-30: H_det -= pm * math.log2(pm)
        if prob_a[b] > 1e-30: H_cond -= 0.5*prob_a[b]*math.log2(prob_a[b])
        if prob_b[b] > 1e-30: H_cond -= 0.5*prob_b[b]*math.log2(prob_b[b])
    MI = H_det - H_cond
    return {"MI": MI, "H_det": H_det, "H_cond": H_cond}


def _mean_se(vals):
    if not vals: return float('nan'), float('nan')
    m = sum(vals)/len(vals)
    if len(vals) < 2: return m, 0.0
    return m, math.sqrt(sum((v-m)**2 for v in vals)/(len(vals)-1)/len(vals))


def main():
    print("=" * 90)
    print("MUTUAL INFORMATION AUDIT: MIRROR vs RANDOM (LINEAR PROPAGATOR)")
    print(f"  k={K}, {N_SEEDS} seeds, {N_YBINS} y-bins")
    print("=" * 90)
    print()

    seeds = [s*7+3 for s in range(N_SEEDS)]

    families = [
        ("3D mirror S4", lambda s, nl: gen_3d_mirror(nl, 25, 12, 5, s)),
        ("3D random", lambda s, nl: gen_3d_random(nl, 50, 12, 5, s)),
        ("2D mirror", lambda s, nl: gen_2d_mirror(nl, 12, 10, 2.5, s)),
        ("2D random", lambda s, nl: gen_2d_random(nl, 24, 10, 2.5, s)),
    ]

    print(f"  {'family':>16s}  {'N':>4s}  {'MI (bits)':>10s}  {'H(det)':>8s}  "
          f"{'H(det|s)':>8s}  {'ok':>3s}")
    print(f"  {'-' * 58}")

    for label, gen_fn in families:
        for nl in [15, 25, 40, 60, 80]:
            mi_all, hd_all, hc_all = [], [], []
            for seed in seeds:
                pos, adj, bl = gen_fn(seed, nl)
                r = compute_mi(pos, adj, nl, K)
                if r:
                    mi_all.append(r["MI"])
                    hd_all.append(r["H_det"])
                    hc_all.append(r["H_cond"])
            if mi_all:
                mmi, semi = _mean_se(mi_all)
                mhd, _ = _mean_se(hd_all)
                mhc, _ = _mean_se(hc_all)
                print(f"  {label:>16s}  {nl:4d}  {mmi:7.4f}±{semi:.3f}  {mhd:8.4f}  "
                      f"{mhc:8.4f}  {len(mi_all):3d}")
        print()

    print("NOTE: All measurements use propagate() which is STRICTLY LINEAR.")
    print("MI = H(detector) - H(detector|slit) in bits (max = 1.0 for binary slit).")


if __name__ == "__main__":
    main()
