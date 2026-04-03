#!/usr/bin/env python3
"""Higher symmetry DAGs: exploratory symmetry comparison only.

This file compares a few symmetry families on a decoherence-side proxy.
It does **not** establish a Born-safe or gravity-safe retained lane by
itself, and it should not be read as a rank-theorem proof.

The current interesting question is narrower:
does Z2xZ2 improve the decoherence-side proxy relative to the weaker
mirror and random baselines on this harness?

Use the hardened mirror chokepoint scripts for review-safe Born/gravity
claims.
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
XYZ_RANGE = 12.0
CONNECT_RADIUS = 5.0
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


def generate_z2_dag(n_layers, npl_half, xyz_range, cr, rng_seed):
    """Z₂: y → -y mirror."""
    rng = random.Random(rng_seed); positions = []; adj = defaultdict(list)
    layer_indices = []; bl = n_layers // 3
    for layer in range(n_layers):
        x = float(layer); ln = []
        if layer == 0:
            positions.append((x, 0, 0)); ln.append(len(positions)-1)
        else:
            up, lo = [], []
            for _ in range(npl_half):
                y = rng.uniform(0.5, xyz_range); z = rng.uniform(-xyz_range, xyz_range)
                iu = len(positions); positions.append((x, y, z)); up.append(iu)
                il = len(positions); positions.append((x, -y, z)); lo.append(il)
            ln = up + lo
            lb = max(0, len(layer_indices) - (1 if layer == bl+1 else 2))
            for ci in up:
                cx, cy, cz = positions[ci]
                for pl in layer_indices[lb:]:
                    for pi in pl:
                        px, py, pz = positions[pi]
                        if math.sqrt((cx-px)**2+(cy-py)**2+(cz-pz)**2) <= cr:
                            adj[pi].append(ci)
                            # Find mirror of pi
                            mi = pi  # source maps to self
                            for iu2, il2 in zip(up, lo):
                                pass  # can't easily find mirror of prev layer
                            # Just also connect mirrors by checking distance
                for ci_m in lo:
                    cx, cy, cz = positions[ci_m]
                    for pl in layer_indices[lb:]:
                        for pi in pl:
                            px, py, pz = positions[pi]
                            if math.sqrt((cx-px)**2+(cy-py)**2+(cz-pz)**2) <= cr:
                                adj[pi].append(ci_m)
        layer_indices.append(ln)
    return positions, dict(adj), bl


def generate_z2z2_dag(n_layers, npl_quarter, xyz_range, cr, rng_seed):
    """Z₂×Z₂: y → -y AND z → -z. 4 copies per base node."""
    rng = random.Random(rng_seed); positions = []; adj = defaultdict(list)
    layer_indices = []; bl = n_layers // 3
    for layer in range(n_layers):
        x = float(layer); ln = []
        if layer == 0:
            positions.append((x, 0, 0)); ln.append(len(positions)-1)
        else:
            all_nodes = []
            for _ in range(npl_quarter):
                y = rng.uniform(0.5, xyz_range); z = rng.uniform(0.5, xyz_range)
                for sy, sz in [(1,1), (1,-1), (-1,1), (-1,-1)]:
                    idx = len(positions); positions.append((x, sy*y, sz*z))
                    all_nodes.append(idx)
            ln = all_nodes
            lb = max(0, len(layer_indices) - (1 if layer == bl+1 else 2))
            for ci in ln:
                cx, cy, cz = positions[ci]
                for pl in layer_indices[lb:]:
                    for pi in pl:
                        px, py, pz = positions[pi]
                        if math.sqrt((cx-px)**2+(cy-py)**2+(cz-pz)**2) <= cr:
                            adj[pi].append(ci)
        layer_indices.append(ln)
    return positions, dict(adj), bl


def generate_ring_dag(n_layers, n_ring, xyz_range, cr, rng_seed):
    """Approximate rotational symmetry: nodes placed on rings at random radii."""
    rng = random.Random(rng_seed); positions = []; adj = defaultdict(list)
    layer_indices = []; bl = n_layers // 3
    for layer in range(n_layers):
        x = float(layer); ln = []
        if layer == 0:
            positions.append((x, 0, 0)); ln.append(len(positions)-1)
        else:
            for _ in range(n_ring // 8 + 1):  # multiple radii
                r = rng.uniform(1.0, xyz_range)
                for i in range(8):  # 8 nodes per ring
                    angle = 2 * math.pi * i / 8 + rng.uniform(-0.1, 0.1)
                    y = r * math.cos(angle); z = r * math.sin(angle)
                    idx = len(positions); positions.append((x, y, z)); ln.append(idx)
                    if len(ln) >= n_ring: break
                if len(ln) >= n_ring: break
            ln = ln[:n_ring]
            lb = max(0, len(layer_indices) - (1 if layer == bl+1 else 2))
            for ci in ln:
                cx, cy, cz = positions[ci]
                for pl in layer_indices[lb:]:
                    for pi in pl:
                        px, py, pz = positions[pi]
                        if math.sqrt((cx-px)**2+(cy-py)**2+(cz-pz)**2) <= cr:
                            adj[pi].append(ci)
        layer_indices.append(ln)
    return positions, dict(adj), bl


def generate_random_dag(n_layers, npl, xyz_range, cr, rng_seed):
    """Standard random (no symmetry)."""
    rng = random.Random(rng_seed); positions = []; adj = defaultdict(list)
    layer_indices = []; bl = n_layers // 3
    for layer in range(n_layers):
        x = float(layer); ln = []
        if layer == 0:
            positions.append((x, 0, 0)); ln.append(len(positions)-1)
        else:
            for _ in range(npl):
                y = rng.uniform(-xyz_range, xyz_range); z = rng.uniform(-xyz_range, xyz_range)
                idx = len(positions); positions.append((x, y, z)); ln.append(idx)
                lb = max(0, len(layer_indices) - (1 if layer == bl+1 else 2))
                for pl in layer_indices[lb:]:
                    for pi in pl:
                        px, py, pz = positions[pi]
                        if math.sqrt((x-px)**2+(y-py)**2+(z-pz)**2) <= cr:
                            adj[pi].append(idx)
        layer_indices.append(ln)
    return positions, dict(adj), bl


def propagate(positions, adj, field, src, k, blocked):
    n = len(positions); order = _topo_order(adj, n); amps = [0j]*n
    for s in src: amps[s] = 1.0/len(src)
    for i in order:
        if abs(amps[i]) < 1e-30 or i in blocked: continue
        for j in adj.get(i, []):
            if j in blocked: continue
            x1,y1,z1 = positions[i]; x2,y2,z2 = positions[j]
            dx,dy,dz = x2-x1,y2-y1,z2-z1; L = math.sqrt(dx*dx+dy*dy+dz*dz)
            if L < 1e-10: continue
            lf = 0.5*(field[i]+field[j]); dl = L*(1+lf)
            ret = math.sqrt(max(dl*dl-L*L,0)); act = dl-ret
            theta = math.atan2(math.sqrt(dy*dy+dz*dz),max(dx,1e-10))
            amps[j] += amps[i] * cmath.exp(1j*k*act) * math.exp(-BETA*theta*theta) / L
    return amps


def compute_field(positions, mass):
    n = len(positions); field = [0.0]*n
    for m in mass:
        mx,my,mz = positions[m]
        for i in range(n):
            ix,iy,iz = positions[i]
            field[i] += 0.1/(math.sqrt((ix-mx)**2+(iy-my)**2+(iz-mz)**2)+0.1)
    return field


def measure(positions, adj, nl, k):
    n = len(positions); by_layer = defaultdict(list)
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
    gl = layers[2*len(layers)//3]; mass = [i for i in by_layer[gl] if positions[i][1]>cy+1]
    if not mass: return None
    ed = max(1,round(nl/6)); st = bl_idx+1; sp = min(len(layers)-1,st+ed)
    mid = [];
    for l in layers[st:sp]: mid.extend(by_layer[l])
    field = compute_field(positions, mass)
    pa = propagate(positions,adj,field,src,k,blocked|set(sb))
    pb = propagate(positions,adj,field,src,k,blocked|set(sa))
    da = {d:abs(pa[d])**2 for d in det}; db = {d:abs(pb[d])**2 for d in det}
    na = sum(da.values()); nb = sum(db.values())
    if na<1e-30 or nb<1e-30: return None
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
    if tr<1e-30: return None
    for key in rho: rho[key] /= tr
    return {"dtv": dtv, "pur_cl": sum(abs(v)**2 for v in rho.values()).real}


def _mean_se(vals):
    vals = [v for v in vals if v is not None and not math.isnan(v)]
    if not vals: return float('nan'), float('nan')
    m = sum(vals)/len(vals)
    if len(vals)<2: return m, 0.0
    return m, math.sqrt(sum((v-m)**2 for v in vals)/(len(vals)-1)/len(vals))


def main():
    print("=" * 100)
    print("SYMMETRY GROUP COMPARISON: none < Z₂ < Z₂×Z₂ < ring?")
    print(f"  k={K}, {N_SEEDS} seeds, ~50 nodes/layer, r={CONNECT_RADIUS}")
    print("=" * 100)
    print()
    seeds = [s*7+3 for s in range(N_SEEDS)]
    configs = [
        ("random (none)", lambda s,nl: generate_random_dag(nl, 50, XYZ_RANGE, CONNECT_RADIUS, s)),
        ("Z₂ (y mirror)", lambda s,nl: generate_z2_dag(nl, 25, XYZ_RANGE, CONNECT_RADIUS, s)),
        ("Z₂×Z₂ (y+z)", lambda s,nl: generate_z2z2_dag(nl, 12, XYZ_RANGE, CONNECT_RADIUS, s)),
        ("ring (approx rot)", lambda s,nl: generate_ring_dag(nl, 48, XYZ_RANGE, CONNECT_RADIUS, s)),
    ]
    print(f"  {'N':>4s}  {'symmetry':>18s}  {'d_TV':>8s}  {'pur_cl':>8s}  {'ok':>3s}  {'time':>5s}")
    print(f"  {'-' * 55}")
    for nl in [25, 40, 60, 80]:
        for label, gen_fn in configs:
            t0 = time.time(); dtv_all, pur_all = [], []
            for seed in seeds:
                pos, adj, bl = gen_fn(seed, nl)
                r = measure(pos, adj, nl, K)
                if r: dtv_all.append(r["dtv"]); pur_all.append(r["pur_cl"])
            dt = time.time()-t0
            if pur_all:
                md,_ = _mean_se(dtv_all); mp,sp = _mean_se(pur_all)
                print(f"  {nl:4d}  {label:>18s}  {md:8.4f}  {mp:7.4f}±{sp:.02f}  {len(pur_all):3d}  {dt:4.0f}s")
            else:
                print(f"  {nl:4d}  {label:>18s}  FAIL  {dt:4.0f}s")
        print()
    print("Exploratory read: compare decoherence-side ordering only.")
    print("Do not infer Born or gravity retention from this script alone.")


if __name__ == "__main__":
    main()
