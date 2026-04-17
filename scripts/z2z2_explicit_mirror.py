#!/usr/bin/env python3
"""Z₂×Z₂ with explicit edge mirroring.

Prediction from derivation: explicit edge mirroring on Z₂×Z₂ should
give BOTH strong decoherence (from 4-fold symmetry sectors) AND strong
gravity (from geometric noise elimination).

The S4 (Z₂-only) mirror family has explicit edge mirroring and gives
gravity +3.96 SE + pur_cl=0.780 at N=60.

The Z₂×Z₂ (implicit) has decoherence pur_cl=0.682 but weak gravity.

Z₂×Z₂ with explicit mirroring should combine: pur_cl < 0.75 AND
gravity > 2.0 SE at N=60.

Implementation: for each "base" node at (x, +y, +z), create 3 mirrors:
  (x, +y, -z), (x, -y, +z), (x, -y, -z)
For each edge from base node to prev layer, create 3 mirror edges.
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
N_SEEDS = 24
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


def generate_z2z2_explicit(n_layers, npl_quarter, xyz_range, connect_radius, rng_seed):
    """Z₂×Z₂ with EXPLICIT edge mirroring.

    For each base node at (x, +y, +z):
      Mirror 1: (x, +y, -z)  [z-flip]
      Mirror 2: (x, -y, +z)  [y-flip]
      Mirror 3: (x, -y, -z)  [y+z flip]

    For each edge (prev → base), create:
      (z_mirror(prev) → z_mirror(base))
      (y_mirror(prev) → y_mirror(base))
      (yz_mirror(prev) → yz_mirror(base))
    """
    rng = random.Random(rng_seed)
    positions = []
    adj = defaultdict(list)
    layer_indices = []
    barrier_layer = n_layers // 3

    # Mirror maps: node_idx → {transform: mirror_node_idx}
    y_mirror = {}   # y → -y
    z_mirror = {}   # z → -z
    yz_mirror = {}  # y → -y, z → -z

    for layer in range(n_layers):
        x = float(layer)
        layer_nodes = []

        if layer == 0:
            idx = len(positions)
            positions.append((x, 0.0, 0.0))
            layer_nodes.append(idx)
            y_mirror[idx] = idx
            z_mirror[idx] = idx
            yz_mirror[idx] = idx
        else:
            base_nodes = []
            zf_nodes = []
            yf_nodes = []
            yzf_nodes = []

            for _ in range(npl_quarter):
                y = rng.uniform(0.5, xyz_range)
                z = rng.uniform(0.5, xyz_range)

                # Base: (+y, +z)
                i_base = len(positions); positions.append((x, y, z)); base_nodes.append(i_base)
                # Z-flip: (+y, -z)
                i_zf = len(positions); positions.append((x, y, -z)); zf_nodes.append(i_zf)
                # Y-flip: (-y, +z)
                i_yf = len(positions); positions.append((x, -y, z)); yf_nodes.append(i_yf)
                # YZ-flip: (-y, -z)
                i_yzf = len(positions); positions.append((x, -y, -z)); yzf_nodes.append(i_yzf)

                # Mirror maps
                y_mirror[i_base] = i_yf;  y_mirror[i_yf] = i_base
                y_mirror[i_zf] = i_yzf;   y_mirror[i_yzf] = i_zf
                z_mirror[i_base] = i_zf;   z_mirror[i_zf] = i_base
                z_mirror[i_yf] = i_yzf;    z_mirror[i_yzf] = i_yf
                yz_mirror[i_base] = i_yzf; yz_mirror[i_yzf] = i_base
                yz_mirror[i_zf] = i_yf;    yz_mirror[i_yf] = i_zf

            layer_nodes = base_nodes + zf_nodes + yf_nodes + yzf_nodes

            # Connect base nodes to previous layers, then mirror all edges
            lookback = max(0, len(layer_indices) - (1 if layer == barrier_layer + 1 else 2))

            for ci in base_nodes:
                cx, cy_val, cz = positions[ci]
                for prev_layer in layer_indices[lookback:]:
                    for pi in prev_layer:
                        px, py, pz = positions[pi]
                        dist = math.sqrt((cx-px)**2 + (cy_val-py)**2 + (cz-pz)**2)
                        if dist <= connect_radius:
                            # Base edge
                            adj[pi].append(ci)
                            # Z-mirror edge
                            adj[z_mirror.get(pi, pi)].append(z_mirror.get(ci, ci))
                            # Y-mirror edge
                            adj[y_mirror.get(pi, pi)].append(y_mirror.get(ci, ci))
                            # YZ-mirror edge
                            adj[yz_mirror.get(pi, pi)].append(yz_mirror.get(ci, ci))

        layer_indices.append(layer_nodes)

    return positions, dict(adj), barrier_layer


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
    gl = layers[2*len(layers)//3]
    # ASYMMETRIC mass: only upper y
    mass = [i for i in by_layer[gl] if positions[i][1] > cy+2][:5]
    if not mass: return None
    ed = max(1,round(nl/6)); st = bl_idx+1; sp = min(len(layers)-1,st+ed)
    mid = [];
    for l in layers[st:sp]: mid.extend(by_layer[l])
    field_m = compute_field(positions, mass); field_f = [0.0]*n

    pa = propagate(positions,adj,field_m,src,k,blocked|set(sb))
    pb = propagate(positions,adj,field_m,src,k,blocked|set(sa))
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
    pur_cl = sum(abs(v)**2 for v in rho.values()).real

    # Gravity
    am = propagate(positions,adj,field_m,src,k,blocked)
    af = propagate(positions,adj,field_f,src,k,blocked)
    pm = sum(abs(am[d])**2 for d in det); pf = sum(abs(af[d])**2 for d in det)
    grav = 0.0
    if pm>1e-30 and pf>1e-30:
        grav = (sum(abs(am[d])**2*positions[d][1] for d in det)/pm
               -sum(abs(af[d])**2*positions[d][1] for d in det)/pf)

    # k=0 control
    am0 = propagate(positions,adj,field_m,src,0.0,blocked)
    af0 = propagate(positions,adj,field_f,src,0.0,blocked)
    pm0 = sum(abs(am0[d])**2 for d in det); pf0 = sum(abs(af0[d])**2 for d in det)
    grav_k0 = 0.0
    if pm0>1e-30 and pf0>1e-30:
        grav_k0 = (sum(abs(am0[d])**2*positions[d][1] for d in det)/pm0
                  -sum(abs(af0[d])**2*positions[d][1] for d in det)/pf0)

    return {"dtv": dtv, "pur_cl": pur_cl, "gravity": grav, "grav_k0": grav_k0, "s_norm": Sn}


def _mean_se(vals):
    vals = [v for v in vals if v is not None and not math.isnan(v)]
    if not vals: return float('nan'), float('nan')
    m = sum(vals)/len(vals)
    if len(vals)<2: return m, 0.0
    return m, math.sqrt(sum((v-m)**2 for v in vals)/(len(vals)-1)/len(vals))


def main():
    print("=" * 110)
    print("Z₂×Z₂ WITH EXPLICIT EDGE MIRRORING")
    print(f"  k={K}, {N_SEEDS} seeds, NPL_QUARTER=12 (48 total), r={CONNECT_RADIUS}")
    print(f"  Prediction: pur_cl < 0.75 AND gravity > 2.0 SE at N=60")
    print("=" * 110)
    print()

    seeds = [s * 7 + 3 for s in range(N_SEEDS)]

    print(f"  {'N':>4s}  {'d_TV':>8s}  {'pur_cl':>8s}  {'gravity':>12s}  "
          f"{'grav_t':>7s}  {'k=0':>10s}  {'ok':>3s}  {'time':>5s}")
    print(f"  {'-' * 68}")

    for nl in [25, 40, 60, 80]:
        t0 = time.time()
        dtv_all, pur_all, grav_all, k0_all = [], [], [], []

        for seed in seeds:
            pos, adj, bl = generate_z2z2_explicit(nl, 12, XYZ_RANGE, CONNECT_RADIUS, seed)
            r = measure(pos, adj, nl, K)
            if r:
                dtv_all.append(r["dtv"])
                pur_all.append(r["pur_cl"])
                grav_all.append(r["gravity"])
                k0_all.append(r["grav_k0"])

        dt = time.time() - t0
        if grav_all:
            md, _ = _mean_se(dtv_all)
            mp, sp = _mean_se(pur_all)
            mg, seg = _mean_se(grav_all)
            gt = mg / seg if seg > 0 else 0
            mk0, _ = _mean_se(k0_all)
            print(f"  {nl:4d}  {md:8.4f}  {mp:7.4f}±{sp:.02f}  {mg:+8.4f}±{seg:.3f}  "
                  f"{gt:+6.2f}  {mk0:+10.2e}  {len(grav_all):3d}  {dt:4.0f}s")
        else:
            print(f"  {nl:4d}  FAIL  {dt:4.0f}s")

    print()
    print("PREDICTION CHECK:")
    print("  pur_cl < 0.75 at N=60: Z₂×Z₂ decoherence maintained")
    print("  gravity > 2.0 SE at N=60: explicit mirroring eliminates geometric noise")
    print("  k=0 ≈ 0: gravity is phase-mediated")
    print("  If BOTH pass: derivation CONFIRMED")


if __name__ == "__main__":
    main()
