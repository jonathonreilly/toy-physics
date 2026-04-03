#!/usr/bin/env python3
"""Approximate vs exact mirror symmetry.

The exact mirror DAG enforces y → -y by construction. But if the
model's laws don't distinguish +y from -y, an ordinary random DAG
with a y-symmetric growth rule should have APPROXIMATE mirror symmetry.

On a standard random DAG, the y-positions are drawn from
Uniform(-range, +range), which IS y-symmetric. So the graph has
statistical mirror symmetry — each realization breaks it randomly,
but the ensemble average is symmetric.

Question: does the decoherence improvement from exact mirror symmetry
survive when the symmetry is only statistical (approximate)?

Test:
  1. Exact mirror: forced y → -y pairing (our generator)
  2. Standard random: statistical y-symmetry (no enforcement)
  3. Forced asymmetric: nodes placed preferentially at y > 0
     (breaks even statistical symmetry)

If exact >> random ≈ asymmetric: the exact pairing matters
If exact ≈ random >> asymmetric: statistical symmetry is enough
If exact >> random >> asymmetric: partial benefit from statistics

Also: measure the ACTUAL y-symmetry of each graph type.
Quantify: Σ|n_upper(layer) - n_lower(layer)| / total_nodes
(perfect mirror = 0, fully asymmetric = 1)
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
NPL_HALF = 25  # For mirror: 25 per half = 50 total
NPL_FULL = 50  # For random/asymmetric: 50 total
XYZ_RANGE = 12.0
CONNECT_RADIUS = 5.0
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


def generate_mirror_hybrid(n_layers, npl_half, xyz_range, connect_radius, rng_seed):
    """Exact mirror DAG with hybrid chokepoint."""
    rng = random.Random(rng_seed)
    positions = []
    adj = defaultdict(list)
    layer_indices = []
    mirror_map = {}
    barrier_layer = n_layers // 3
    for layer in range(n_layers):
        x = float(layer)
        layer_nodes = []
        if layer == 0:
            idx = len(positions); positions.append((x, 0.0, 0.0))
            layer_nodes.append(idx); mirror_map[idx] = idx
        else:
            upper, lower = [], []
            for _ in range(npl_half):
                y = rng.uniform(0.5, xyz_range)
                z = rng.uniform(-xyz_range, xyz_range)
                iu = len(positions); positions.append((x, y, z)); upper.append(iu)
                il = len(positions); positions.append((x, -y, z)); lower.append(il)
                mirror_map[iu] = il; mirror_map[il] = iu
            layer_nodes = upper + lower
            lookback = max(0, len(layer_indices) - (1 if layer == barrier_layer + 1 else 2))
            for ci in upper:
                cx, cy, cz = positions[ci]
                for pl in layer_indices[lookback:]:
                    for pi in pl:
                        px, py, pz = positions[pi]
                        if math.sqrt((cx-px)**2+(cy-py)**2+(cz-pz)**2) <= connect_radius:
                            adj[pi].append(ci); adj[mirror_map[pi]].append(mirror_map[ci])
        layer_indices.append(layer_nodes)
    return positions, dict(adj), barrier_layer


def generate_random_dag(n_layers, npl, xyz_range, connect_radius, rng_seed):
    """Standard random DAG (statistical y-symmetry only)."""
    rng = random.Random(rng_seed)
    positions = []
    adj = defaultdict(list)
    layer_indices = []
    barrier_layer = n_layers // 3
    for layer in range(n_layers):
        x = float(layer)
        layer_nodes = []
        if layer == 0:
            positions.append((x, 0.0, 0.0)); layer_nodes.append(len(positions)-1)
        else:
            for _ in range(npl):
                y = rng.uniform(-xyz_range, xyz_range)
                z = rng.uniform(-xyz_range, xyz_range)
                idx = len(positions); positions.append((x, y, z)); layer_nodes.append(idx)
                lookback = max(0, len(layer_indices) - (1 if layer == barrier_layer + 1 else 2))
                for pl in layer_indices[lookback:]:
                    for pi in pl:
                        px, py, pz = positions[pi]
                        if math.sqrt((x-px)**2+(y-py)**2+(z-pz)**2) <= connect_radius:
                            adj[pi].append(idx)
        layer_indices.append(layer_nodes)
    return positions, dict(adj), barrier_layer


def generate_asymmetric_dag(n_layers, npl, xyz_range, connect_radius, rng_seed):
    """Asymmetric DAG: 75% of nodes placed at y > 0."""
    rng = random.Random(rng_seed)
    positions = []
    adj = defaultdict(list)
    layer_indices = []
    barrier_layer = n_layers // 3
    for layer in range(n_layers):
        x = float(layer)
        layer_nodes = []
        if layer == 0:
            positions.append((x, 0.0, 0.0)); layer_nodes.append(len(positions)-1)
        else:
            for ni in range(npl):
                if ni < npl * 3 // 4:
                    y = rng.uniform(0, xyz_range)  # upper bias
                else:
                    y = rng.uniform(-xyz_range, 0)
                z = rng.uniform(-xyz_range, xyz_range)
                idx = len(positions); positions.append((x, y, z)); layer_nodes.append(idx)
                lookback = max(0, len(layer_indices) - (1 if layer == barrier_layer + 1 else 2))
                for pl in layer_indices[lookback:]:
                    for pi in pl:
                        px, py, pz = positions[pi]
                        if math.sqrt((x-px)**2+(y-py)**2+(z-pz)**2) <= connect_radius:
                            adj[pi].append(idx)
        layer_indices.append(layer_nodes)
    return positions, dict(adj), barrier_layer


def propagate_3d(positions, adj, field, src, k, blocked):
    n = len(positions)
    order = _topo_order(adj, n)
    amps = [0j] * n
    for s in src: amps[s] = 1.0 / len(src)
    for i in order:
        if abs(amps[i]) < 1e-30 or i in blocked: continue
        for j in adj.get(i, []):
            if j in blocked: continue
            x1,y1,z1 = positions[i]; x2,y2,z2 = positions[j]
            dx,dy,dz = x2-x1,y2-y1,z2-z1
            L = math.sqrt(dx*dx+dy*dy+dz*dz)
            if L < 1e-10: continue
            lf = 0.5*(field[i]+field[j]); dl = L*(1+lf)
            ret = math.sqrt(max(dl*dl-L*L,0)); act = dl-ret
            theta = math.atan2(math.sqrt(dy*dy+dz*dz),max(dx,1e-10))
            w = math.exp(-BETA*theta*theta)
            amps[j] += amps[i] * cmath.exp(1j*k*act) * w / L
    return amps


def compute_field_3d(positions, mass_nodes):
    n = len(positions); field = [0.0]*n
    for m in mass_nodes:
        mx,my,mz = positions[m]
        for i in range(n):
            ix,iy,iz = positions[i]
            field[i] += 0.1 / (math.sqrt((ix-mx)**2+(iy-my)**2+(iz-mz)**2)+0.1)
    return field


def measure(positions, adj, n_layers, k):
    n = len(positions)
    by_layer = defaultdict(list)
    for idx,(x,y,z) in enumerate(positions): by_layer[round(x)].append(idx)
    layers = sorted(by_layer.keys())
    if len(layers) < 7: return None
    src = by_layer[layers[0]]; det = list(by_layer[layers[-1]])
    if not det: return None
    cy = sum(positions[i][1] for i in range(n))/n
    bl_idx = len(layers)//3; bi = by_layer[layers[bl_idx]]
    sa = [i for i in bi if positions[i][1] > cy+3][:3]
    sb = [i for i in bi if positions[i][1] < cy-3][:3]
    if not sa or not sb: return None
    blocked = set(bi)-set(sa+sb)
    gl = layers[2*len(layers)//3]
    mass = [i for i in by_layer[gl] if positions[i][1] > cy+1]
    if not mass: return None
    ed = max(1,round(n_layers/6)); st = bl_idx+1; sp = min(len(layers)-1,st+ed)
    mid = [];
    for l in layers[st:sp]: mid.extend(by_layer[l])
    field = compute_field_3d(positions, mass)
    pa = propagate_3d(positions,adj,field,src,k,blocked|set(sb))
    pb = propagate_3d(positions,adj,field,src,k,blocked|set(sa))
    da = {d:abs(pa[d])**2 for d in det}; db = {d:abs(pb[d])**2 for d in det}
    na = sum(da.values()); nb = sum(db.values())
    if na < 1e-30 or nb < 1e-30: return None
    dtv = 0.5*sum(abs(da[d]/na-db[d]/nb) for d in det)
    ba = [0j]*N_YBINS; bb = [0j]*N_YBINS; bw = 24.0/N_YBINS
    for m in mid:
        b = max(0,min(N_YBINS-1,int((positions[m][1]+12)/bw)))
        ba[b] += pa[m]; bb[b] += pb[m]
    S = sum(abs(a-b)**2 for a,b in zip(ba,bb))
    NA = sum(abs(a)**2 for a in ba); NB = sum(abs(b)**2 for b in bb)
    Sn = S/(NA+NB) if (NA+NB)>0 else 0; Dcl = math.exp(-LAM**2*Sn)
    rho = {}
    for d1 in det:
        for d2 in det:
            rho[(d1,d2)] = (pa[d1].conjugate()*pa[d2]+pb[d1].conjugate()*pb[d2]
                           +Dcl*pa[d1].conjugate()*pb[d2]+Dcl*pb[d1].conjugate()*pa[d2])
    tr = sum(rho[(d,d)] for d in det).real
    if tr < 1e-30: return None
    for key in rho: rho[key] /= tr
    pur = sum(abs(v)**2 for v in rho.values()).real
    # Symmetry metric
    bl_val = layers[bl_idx]
    sym = 0; tot = 0
    for lk in layers:
        if lk <= bl_val: continue
        nodes = by_layer[lk]
        n_up = sum(1 for i in nodes if positions[i][1] > 0)
        n_lo = sum(1 for i in nodes if positions[i][1] < 0)
        sym += abs(n_up - n_lo); tot += n_up + n_lo
    sym_metric = sym / tot if tot > 0 else 0
    return {"dtv": dtv, "pur_cl": pur, "s_norm": Sn, "sym": sym_metric}


def _mean_se(vals):
    vals = [v for v in vals if v is not None and not math.isnan(v)]
    if not vals: return float('nan'), float('nan')
    m = sum(vals)/len(vals)
    if len(vals) < 2: return m, 0.0
    return m, math.sqrt(sum((v-m)**2 for v in vals)/(len(vals)-1)/len(vals))


def main():
    print("=" * 100)
    print("APPROXIMATE vs EXACT MIRROR SYMMETRY")
    print(f"  k={K}, {N_SEEDS} seeds, 50 nodes/layer, r={CONNECT_RADIUS}")
    print("=" * 100)
    print()
    seeds = [s*7+3 for s in range(N_SEEDS)]
    configs = [
        ("exact mirror", lambda s,nl: generate_mirror_hybrid(nl,NPL_HALF,XYZ_RANGE,CONNECT_RADIUS,s)),
        ("random (stat sym)", lambda s,nl: generate_random_dag(nl,NPL_FULL,XYZ_RANGE,CONNECT_RADIUS,s)),
        ("asymmetric (75/25)", lambda s,nl: generate_asymmetric_dag(nl,NPL_FULL,XYZ_RANGE,CONNECT_RADIUS,s)),
    ]
    print(f"  {'N':>4s}  {'mode':>20s}  {'d_TV':>8s}  {'pur_cl':>8s}  {'S_norm':>8s}  "
          f"{'sym':>6s}  {'ok':>3s}  {'time':>5s}")
    print(f"  {'-' * 72}")
    for nl in [25, 40, 60, 80]:
        for label, gen_fn in configs:
            t0 = time.time()
            dtv_all,pur_all,sn_all,sym_all = [],[],[],[]
            for seed in seeds:
                pos,adj,bl = gen_fn(seed,nl)
                r = measure(pos,adj,nl,K)
                if r:
                    dtv_all.append(r["dtv"]); pur_all.append(r["pur_cl"])
                    sn_all.append(r["s_norm"]); sym_all.append(r["sym"])
            dt = time.time()-t0
            if pur_all:
                md,_ = _mean_se(dtv_all); mp,sp = _mean_se(pur_all)
                ms,_ = _mean_se(sn_all); msym,_ = _mean_se(sym_all)
                print(f"  {nl:4d}  {label:>20s}  {md:8.4f}  {mp:7.4f}±{sp:.02f}  "
                      f"{ms:8.4f}  {msym:6.3f}  {len(pur_all):3d}  {dt:4.0f}s")
            else:
                print(f"  {nl:4d}  {label:>20s}  FAIL  {dt:4.0f}s")
        print()
    print("sym: node count asymmetry (0=perfect mirror, 1=fully one-sided)")
    print("If exact >> random: the forced pairing is essential")
    print("If exact ≈ random: statistical symmetry is enough")


if __name__ == "__main__":
    main()
