#!/usr/bin/env python3
"""Controlled gravity on S4 mirror: field source at specific y-offset.

The flat mass scaling came from mass clustered at high y (all > 10).
Adding more mass at the same y doesn't change the field gradient.

Fix: place a SINGLE mass source at a CONTROLLED y-position and vary it.
This creates a clean field gradient that changes with y_mass.

For distance law: vary y_mass from 2 to 10 (closer to farther from beam).
For mass scaling: vary field strength (n_sources × strength) at fixed y.

The mirror graph keeps its Z₂ symmetry — only the FIELD breaks it.
The field source is at +y only (no mirror mass at -y).
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
NL = 40


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


def compute_field_at_y(positions, grav_layer_nodes, y_target, n_sources, strength=0.1):
    """Create field from n_sources nodes nearest to y_target on the gravity layer."""
    # Find nodes closest to y_target
    candidates = sorted(grav_layer_nodes,
                        key=lambda i: abs(positions[i][1] - y_target))
    selected = candidates[:n_sources]
    n = len(positions)
    field = [0.0] * n
    for m in selected:
        mx, my, mz = positions[m]
        for i in range(n):
            ix, iy, iz = positions[i]
            r = math.sqrt((ix-mx)**2 + (iy-my)**2 + (iz-mz)**2) + 0.1
            field[i] += strength / r
    return field, selected


def propagate(positions, adj, field, src, k, blocked):
    n = len(positions); order = _topo_order(adj, n); amps = [0j] * n
    for s in src: amps[s] = 1.0 / len(src)
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
            amps[j] += amps[i]*cmath.exp(1j*k*act)*math.exp(-BETA*theta*theta)/L
    return amps


def measure_gravity_at_y(positions, adj, src, det, blocked, grav_nodes, y_target,
                          n_sources, k):
    """Measure gravity with mass placed near y_target."""
    field_m, selected = compute_field_at_y(positions, grav_nodes, y_target, n_sources)
    field_f = [0.0] * len(positions)
    am = propagate(positions, adj, field_m, src, k, blocked)
    af = propagate(positions, adj, field_f, src, k, blocked)
    pm = sum(abs(am[d])**2 for d in det); pf = sum(abs(af[d])**2 for d in det)
    if pm < 1e-30 or pf < 1e-30: return None
    ym = sum(abs(am[d])**2*positions[d][1] for d in det)/pm
    yf = sum(abs(af[d])**2*positions[d][1] for d in det)/pf
    mean_mass_y = sum(positions[m][1] for m in selected)/len(selected)
    return {"delta": ym - yf, "mass_y": mean_mass_y}


def _mean_se(vals):
    vals = [v for v in vals if v is not None]
    if not vals: return float('nan'), float('nan')
    m = sum(vals)/len(vals)
    if len(vals)<2: return m, 0.0
    return m, math.sqrt(sum((v-m)**2 for v in vals)/(len(vals)-1)/len(vals))


def main():
    print("=" * 100)
    print("CONTROLLED GRAVITY ON S4 MIRROR")
    print(f"  N={NL}, NPL_HALF={NPL_HALF}, r={CONNECT_RADIUS}, k={K}, {N_SEEDS} seeds")
    print("=" * 100)
    print()

    seeds = [s*7+3 for s in range(N_SEEDS)]

    # Build graphs
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
        grav_nodes = by_layer[gl]
        graphs.append((pos, adj, src, det, blocked, grav_nodes))

    print(f"  {len(graphs)} valid graphs")
    print()

    # TEST 1: DISTANCE LAW — vary y_target (impact parameter)
    print("TEST 1: DISTANCE LAW (n_sources=3, vary y_target)")
    print(f"  {'y_target':>8s}  {'actual_y':>8s}  {'delta':>10s}  {'SE':>8s}  {'t':>6s}")
    print(f"  {'-' * 48}")

    y_targets = [2.0, 3.0, 4.0, 5.0, 6.0, 8.0, 10.0]
    b_data, d_data = [], []

    for yt in y_targets:
        deltas, mass_ys = [], []
        for pos, adj, src, det, blocked, grav_nodes in graphs:
            r = measure_gravity_at_y(pos, adj, src, det, blocked, grav_nodes, yt, 3, K)
            if r:
                deltas.append(r["delta"]); mass_ys.append(r["mass_y"])
        md, se = _mean_se(deltas)
        t = md/se if se > 0 else 0
        my = sum(mass_ys)/len(mass_ys) if mass_ys else 0
        print(f"  {yt:8.1f}  {my:8.2f}  {md:+8.4f}  {se:8.4f}  {t:+5.2f}")
        if md > 0:
            b_data.append(my); d_data.append(md)

    if len(b_data) >= 3:
        peak_idx = max(range(len(d_data)), key=lambda i: d_data[i])
        peak_b = b_data[peak_idx]
        falloff = [(b,d) for b,d in zip(b_data, d_data) if b > peak_b and d > 0]
        if len(falloff) >= 2:
            lx = [math.log(b) for b,_ in falloff]
            ly = [math.log(d) for _,d in falloff]
            nn = len(lx); mx = sum(lx)/nn; my_val = sum(ly)/nn
            sxx = sum((x-mx)**2 for x in lx)
            sxy = sum((x-mx)*(y-my_val) for x,y in zip(lx,ly))
            slope = sxy/sxx if sxx > 1e-10 else 0
            print(f"\n  Peak at y≈{peak_b:.1f}, falloff ~ b^({slope:.2f})")
        else:
            print(f"\n  Peak at y≈{peak_b:.1f}, not enough falloff points")

    # TEST 2: MASS SCALING — vary n_sources at fixed y_target=4
    print()
    print("TEST 2: MASS SCALING (y_target=4.0, vary n_sources)")
    print(f"  {'M':>4s}  {'delta':>10s}  {'SE':>8s}  {'t':>6s}")
    print(f"  {'-' * 34}")

    m_data, g_data = [], []
    for M in [1, 2, 3, 5, 8, 12]:
        deltas = []
        for pos, adj, src, det, blocked, grav_nodes in graphs:
            r = measure_gravity_at_y(pos, adj, src, det, blocked, grav_nodes, 4.0, M, K)
            if r: deltas.append(r["delta"])
        md, se = _mean_se(deltas)
        t = md/se if se > 0 else 0
        print(f"  {M:4d}  {md:+8.4f}  {se:8.4f}  {t:+5.2f}")
        if md > 0: m_data.append(M); g_data.append(md)

    if len(m_data) >= 3:
        lx = [math.log(m) for m in m_data]
        ly = [math.log(g) for g in g_data]
        nn = len(lx); mx = sum(lx)/nn; my_val = sum(ly)/nn
        sxx = sum((x-mx)**2 for x in lx)
        sxy = sum((x-mx)*(y-my_val) for x,y in zip(lx,ly))
        alpha = sxy/sxx if sxx > 1e-10 else 0
        print(f"\n  Mass scaling: delta ~ M^{alpha:.2f}")

    # k=0 control
    print()
    print("k=0 CONTROL (y_target=4.0, M=3)")
    deltas_k0 = []
    for pos, adj, src, det, blocked, grav_nodes in graphs[:8]:
        r = measure_gravity_at_y(pos, adj, src, det, blocked, grav_nodes, 4.0, 3, 0.0)
        if r: deltas_k0.append(r["delta"])
    if deltas_k0:
        mk0, _ = _mean_se(deltas_k0)
        print(f"  gravity at k=0: {mk0:+.6e} (must be zero)")


if __name__ == "__main__":
    main()
