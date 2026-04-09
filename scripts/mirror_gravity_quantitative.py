#!/usr/bin/env python3
"""Quantitative gravity on S4 mirror: mass scaling + distance law.

S4 mirror gives gravity at 6.5 SE (N=60, 24 seeds) with the standard
mass placement. Now measure:
  1. Mass scaling: delta ~ M^alpha at fixed b
  2. Distance law: delta vs impact parameter b

Uses the natural mass placement (nodes at y > threshold on gravity
layer) rather than artificial y-offset. Varies M by selecting
different numbers of mass nodes, and b by varying the y-threshold.
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
NPL_HALF = 40
XYZ_RANGE = 12.0
CONNECT_RADIUS = 5.0
NL = 40  # Fixed graph size


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


def generate_mirror_hybrid(n_layers, npl_half, xyz_range, cr, rng_seed):
    rng = random.Random(rng_seed); positions = []; adj = defaultdict(list)
    layer_indices = []; mm = {}; bl = n_layers // 3
    for layer in range(n_layers):
        x = float(layer); ln = []
        if layer == 0:
            idx = len(positions); positions.append((x,0,0)); ln.append(idx); mm[idx]=idx
        else:
            up, lo = [], []
            for _ in range(npl_half):
                y = rng.uniform(0.5, xyz_range); z = rng.uniform(-xyz_range, xyz_range)
                iu = len(positions); positions.append((x,y,z)); up.append(iu)
                il = len(positions); positions.append((x,-y,z)); lo.append(il)
                mm[iu]=il; mm[il]=iu
            ln = up+lo
            lb = max(0, len(layer_indices)-(1 if layer==bl+1 else 2))
            for ci in up:
                cx,cy,cz = positions[ci]
                for pl in layer_indices[lb:]:
                    for pi in pl:
                        px,py,pz = positions[pi]
                        if math.sqrt((cx-px)**2+(cy-py)**2+(cz-pz)**2) <= cr:
                            adj[pi].append(ci); adj[mm[pi]].append(mm[ci])
        layer_indices.append(ln)
    return positions, dict(adj), bl


def propagate(positions, adj, field, src, k, blocked):
    n = len(positions); order = _topo_order(adj, n); amps = [0j]*n
    for s in src: amps[s] = 1.0/len(src)
    for i in order:
        if abs(amps[i])<1e-30 or i in blocked: continue
        for j in adj.get(i,[]):
            if j in blocked: continue
            x1,y1,z1=positions[i]; x2,y2,z2=positions[j]
            dx,dy,dz=x2-x1,y2-y1,z2-z1; L=math.sqrt(dx*dx+dy*dy+dz*dz)
            if L<1e-10: continue
            lf=0.5*(field[i]+field[j]); dl=L*(1+lf)
            ret=math.sqrt(max(dl*dl-L*L,0)); act=dl-ret
            theta=math.atan2(math.sqrt(dy*dy+dz*dz),max(dx,1e-10))
            amps[j]+=amps[i]*cmath.exp(1j*k*act)*math.exp(-BETA*theta*theta)/L
    return amps


def compute_field_selected(positions, mass_indices):
    n = len(positions); field = [0.0]*n
    for m in mass_indices:
        mx,my,mz = positions[m]
        for i in range(n):
            ix,iy,iz = positions[i]
            field[i] += 0.1/(math.sqrt((ix-mx)**2+(iy-my)**2+(iz-mz)**2)+0.1)
    return field


def measure_gravity(positions, adj, src, det, blocked, mass_indices, k):
    field_m = compute_field_selected(positions, mass_indices)
    field_f = [0.0]*len(positions)
    am = propagate(positions, adj, field_m, src, k, blocked)
    af = propagate(positions, adj, field_f, src, k, blocked)
    pm = sum(abs(am[d])**2 for d in det); pf = sum(abs(af[d])**2 for d in det)
    if pm < 1e-30 or pf < 1e-30: return None
    ym = sum(abs(am[d])**2*positions[d][1] for d in det)/pm
    yf = sum(abs(af[d])**2*positions[d][1] for d in det)/pf
    return ym - yf


def _mean_se(vals):
    vals = [v for v in vals if v is not None]
    if not vals: return float('nan'), float('nan')
    m = sum(vals)/len(vals)
    if len(vals)<2: return m, 0.0
    return m, math.sqrt(sum((v-m)**2 for v in vals)/(len(vals)-1)/len(vals))


def main():
    print("=" * 95)
    print("QUANTITATIVE GRAVITY ON S4 MIRROR")
    print(f"  N={NL}, NPL_HALF={NPL_HALF}, r={CONNECT_RADIUS}, k={K}, {N_SEEDS} seeds")
    print("=" * 95)
    print()

    seeds = [s*7+3 for s in range(N_SEEDS)]

    # Pre-generate graphs and extract structures
    graphs = []
    for seed in seeds:
        pos, adj, bl = generate_mirror_hybrid(NL, NPL_HALF, XYZ_RANGE, CONNECT_RADIUS, seed)
        n = len(pos)
        by_layer = defaultdict(list)
        for idx,(x,y,z) in enumerate(pos): by_layer[round(x)].append(idx)
        layers = sorted(by_layer.keys())
        if len(layers) < 7: continue
        src = by_layer[layers[0]]; det = list(by_layer[layers[-1]])
        if not det: continue
        cy = sum(pos[i][1] for i in range(n))/n
        bl_idx = len(layers)//3; bi = by_layer[layers[bl_idx]]
        sa = [i for i in bi if pos[i][1] > cy+3][:3]
        sb = [i for i in bi if pos[i][1] < cy-3][:3]
        if not sa or not sb: continue
        blocked = set(bi)-set(sa+sb)
        gl = layers[2*len(layers)//3]
        # All upper-y nodes on gravity layer, sorted by y
        all_mass_cands = sorted([i for i in by_layer[gl] if pos[i][1] > 0],
                                 key=lambda i: -pos[i][1])
        if not all_mass_cands: continue
        graphs.append((pos, adj, src, det, blocked, all_mass_cands, gl, by_layer, layers))

    print(f"  {len(graphs)} valid graphs")
    print()

    # TEST 1: Mass scaling (vary M at natural placement)
    print("TEST 1: MASS SCALING (vary M, natural placement)")
    print(f"  {'M':>4s}  {'delta':>10s}  {'SE':>8s}  {'t':>6s}  {'mean_b':>8s}")
    print(f"  {'-' * 44}")

    m_vals, g_vals = [], []
    for M in [1, 2, 3, 5, 8, 12]:
        deltas = []
        b_vals = []
        for pos, adj, src, det, blocked, mass_cands, gl, by_layer, layers in graphs:
            selected = mass_cands[:M]
            if len(selected) < M: continue
            delta = measure_gravity(pos, adj, src, det, blocked, selected, K)
            if delta is not None:
                deltas.append(delta)
                # Mean y-position of mass (impact parameter proxy)
                b_vals.append(sum(pos[m][1] for m in selected)/len(selected))
        md, se = _mean_se(deltas)
        mb = sum(b_vals)/len(b_vals) if b_vals else 0
        t = md/se if se > 0 else 0
        print(f"  {M:4d}  {md:+8.4f}  {se:8.4f}  {t:+5.2f}  {mb:8.2f}")
        if md > 0:
            m_vals.append(M); g_vals.append(md)

    if len(m_vals) >= 3:
        lx = [math.log(m) for m in m_vals]
        ly = [math.log(g) for g in g_vals]
        nn = len(lx); mx = sum(lx)/nn; my = sum(ly)/nn
        sxx = sum((x-mx)**2 for x in lx)
        sxy = sum((x-mx)*(y-my) for x,y in zip(lx,ly))
        alpha = sxy/sxx if sxx > 1e-10 else 0
        print(f"\n  Mass scaling: delta ~ M^{alpha:.2f}")

    # TEST 2: Distance (vary y-threshold to change effective b)
    print()
    print("TEST 2: DISTANCE SCALING (vary y-threshold)")
    print(f"  {'y_min':>6s}  {'M_avg':>6s}  {'delta':>10s}  {'SE':>8s}  {'t':>6s}")
    print(f"  {'-' * 44}")

    b_data, d_data = [], []
    for y_min in [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 8.0, 10.0]:
        deltas = []
        m_counts = []
        for pos, adj, src, det, blocked, mass_cands, gl, by_layer, layers in graphs:
            selected = [m for m in mass_cands if pos[m][1] > y_min][:5]
            if not selected: continue
            delta = measure_gravity(pos, adj, src, det, blocked, selected, K)
            if delta is not None:
                deltas.append(delta); m_counts.append(len(selected))
        md, se = _mean_se(deltas)
        t = md/se if se > 0 else 0
        mm = sum(m_counts)/len(m_counts) if m_counts else 0
        print(f"  {y_min:6.1f}  {mm:6.1f}  {md:+8.4f}  {se:8.4f}  {t:+5.2f}")
        if md > 0:
            b_data.append(y_min); d_data.append(md)

    if len(b_data) >= 3:
        # Find peak
        peak_idx = max(range(len(d_data)), key=lambda i: d_data[i])
        peak_b = b_data[peak_idx]
        # Fit falloff after peak
        falloff = [(b,d) for b,d in zip(b_data, d_data) if b > peak_b and d > 0]
        if len(falloff) >= 2:
            lx = [math.log(b) for b,_ in falloff]
            ly = [math.log(d) for _,d in falloff]
            nn = len(lx); mx = sum(lx)/nn; my = sum(ly)/nn
            sxx = sum((x-mx)**2 for x in lx)
            sxy = sum((x-mx)*(y-my) for x,y in zip(lx,ly))
            slope = sxy/sxx if sxx > 1e-10 else 0
            print(f"\n  Peak at y_min≈{peak_b}, falloff ~ b^({slope:.2f})")


if __name__ == "__main__":
    main()
