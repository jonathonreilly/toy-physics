#!/usr/bin/env python3
"""4D mirror DAGs: does the decoherence exponent improve with dimension?

3D mirror gives exponent -0.27 (vs -1.0 random). If higher dimension
slows the CLT rate AND mirror forces rank-2, the combination should
give an even better exponent.

4D DAG: (x, y, z, w) where x=causal, y=slit axis (Z₂ mirror in y),
z and w are free spatial dimensions.

Also test: 4D Z₂ vs 3D Z₂ vs 3D random head-to-head.
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
NPL_HALF = 25  # per half = 50 total
COORD_RANGE = 12.0
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


def generate_nd_mirror(n_layers, npl_half, coord_range, connect_radius,
                        rng_seed, n_spatial):
    """N-dimensional mirror DAG with Z₂ symmetry in y (coord index 1).

    Nodes: (x, y, z1, z2, ...) where x=causal, y=slit axis.
    Mirror: y → -y, all other coords unchanged.
    Explicit edge mirroring.
    Hybrid chokepoint at barrier layer.
    """
    rng = random.Random(rng_seed)
    positions = []  # list of tuples, length n_spatial + 1
    adj = defaultdict(list)
    layer_indices = []
    mirror_map = {}
    bl = n_layers // 3

    for layer in range(n_layers):
        x = float(layer)
        layer_nodes = []

        if layer == 0:
            pos = tuple([x] + [0.0] * n_spatial)
            idx = len(positions); positions.append(pos)
            layer_nodes.append(idx); mirror_map[idx] = idx
        else:
            up_nodes, lo_nodes = [], []
            for _ in range(npl_half):
                y = rng.uniform(0.5, coord_range)
                extra = [rng.uniform(-coord_range, coord_range) for _ in range(n_spatial - 1)]

                # Upper node: positive y
                pos_up = tuple([x, y] + extra)
                iu = len(positions); positions.append(pos_up); up_nodes.append(iu)

                # Mirror node: negative y, same z/w
                pos_lo = tuple([x, -y] + extra)
                il = len(positions); positions.append(pos_lo); lo_nodes.append(il)

                mirror_map[iu] = il; mirror_map[il] = iu

            layer_nodes = up_nodes + lo_nodes

            # Connect with explicit edge mirroring
            lb = max(0, len(layer_indices) - (1 if layer == bl + 1 else 2))
            for ci in up_nodes:
                ci_pos = positions[ci]
                for prev_layer in layer_indices[lb:]:
                    for pi in prev_layer:
                        pi_pos = positions[pi]
                        dist = math.sqrt(sum((a-b)**2 for a,b in zip(ci_pos, pi_pos)))
                        if dist <= connect_radius:
                            adj[pi].append(ci)
                            adj[mirror_map[pi]].append(mirror_map[ci])

        layer_indices.append(layer_nodes)

    return positions, dict(adj), bl


def propagate_nd(positions, adj, field, src, k, blocked, n_spatial):
    n = len(positions); order = _topo_order(adj, n); amps = [0j] * n
    for s in src: amps[s] = 1.0 / len(src)
    for i in order:
        if abs(amps[i]) < 1e-30 or i in blocked: continue
        for j in adj.get(i, []):
            if j in blocked: continue
            pi, pj = positions[i], positions[j]
            dx = pj[0] - pi[0]
            transverse_sq = sum((pj[k2]-pi[k2])**2 for k2 in range(1, n_spatial+1))
            L = math.sqrt(dx*dx + transverse_sq)
            if L < 1e-10: continue
            lf = 0.5 * (field[i] + field[j])
            dl = L * (1 + lf); ret = math.sqrt(max(dl*dl - L*L, 0)); act = dl - ret
            theta = math.atan2(math.sqrt(transverse_sq), max(dx, 1e-10))
            amps[j] += amps[i] * cmath.exp(1j*k*act) * math.exp(-BETA*theta*theta) / L
    return amps


def compute_field_nd(positions, mass, n_spatial):
    n = len(positions); field = [0.0] * n
    for m in mass:
        pm = positions[m]
        for i in range(n):
            pi = positions[i]
            r = math.sqrt(sum((a-b)**2 for a,b in zip(pi,pm))) + 0.1
            field[i] += 0.1 / r
    return field


def measure_nd(positions, adj, nl, k, n_spatial):
    n = len(positions)
    by_layer = defaultdict(list)
    for idx, pos in enumerate(positions):
        by_layer[round(pos[0])].append(idx)
    layers = sorted(by_layer.keys())
    if len(layers) < 7: return None
    src = by_layer[layers[0]]; det = list(by_layer[layers[-1]])
    if not det: return None
    # y is coord index 1
    cy = sum(positions[i][1] for i in range(n)) / n
    bl_idx = len(layers) // 3; bi = by_layer[layers[bl_idx]]
    sa = [i for i in bi if positions[i][1] > cy + 3][:3]
    sb = [i for i in bi if positions[i][1] < cy - 3][:3]
    if not sa or not sb: return None
    blocked = set(bi) - set(sa + sb)
    gl = layers[2*len(layers)//3]
    mass = [i for i in by_layer[gl] if positions[i][1] > cy + 1][:5]
    if not mass: return None
    ed = max(1, round(nl/6)); st = bl_idx+1; sp = min(len(layers)-1, st+ed)
    mid = []
    for l in layers[st:sp]: mid.extend(by_layer[l])
    field = compute_field_nd(positions, mass, n_spatial)
    field_f = [0.0] * n

    pa = propagate_nd(positions, adj, field, src, k, blocked | set(sb), n_spatial)
    pb = propagate_nd(positions, adj, field, src, k, blocked | set(sa), n_spatial)

    da = {d: abs(pa[d])**2 for d in det}; db = {d: abs(pb[d])**2 for d in det}
    na_a = sum(da.values()); nb_a = sum(db.values())
    if na_a < 1e-30 or nb_a < 1e-30: return None
    dtv = 0.5 * sum(abs(da[d]/na_a - db[d]/nb_a) for d in det)

    # CL bath (bin by y)
    ba = [0j]*N_YBINS; bb = [0j]*N_YBINS; bw = 24.0/N_YBINS
    for m in mid:
        b = max(0, min(N_YBINS-1, int((positions[m][1]+12)/bw)))
        ba[b] += pa[m]; bb[b] += pb[m]
    S = sum(abs(a-b)**2 for a,b in zip(ba,bb))
    NA = sum(abs(a)**2 for a in ba); NB = sum(abs(b)**2 for b in bb)
    Sn = S/(NA+NB) if (NA+NB) > 0 else 0
    Dcl = math.exp(-LAM**2 * Sn)
    rho = {}
    for d1 in det:
        for d2 in det:
            rho[(d1,d2)] = (pa[d1].conjugate()*pa[d2] + pb[d1].conjugate()*pb[d2]
                           + Dcl*pa[d1].conjugate()*pb[d2] + Dcl*pb[d1].conjugate()*pa[d2])
    tr = sum(rho[(d,d)] for d in det).real
    if tr < 1e-30: return None
    for key in rho: rho[key] /= tr
    pur = sum(abs(v)**2 for v in rho.values()).real

    # Gravity
    am = propagate_nd(positions, adj, field, src, k, blocked, n_spatial)
    af = propagate_nd(positions, adj, field_f, src, k, blocked, n_spatial)
    pm = sum(abs(am[d])**2 for d in det); pf = sum(abs(af[d])**2 for d in det)
    grav = 0
    if pm > 1e-30 and pf > 1e-30:
        grav = (sum(abs(am[d])**2*positions[d][1] for d in det)/pm
               - sum(abs(af[d])**2*positions[d][1] for d in det)/pf)

    return {"dtv": dtv, "pur_cl": pur, "gravity": grav}


def _mean_se(vals):
    vals = [v for v in vals if v is not None and not math.isnan(v)]
    if not vals: return float('nan'), float('nan')
    m = sum(vals)/len(vals)
    if len(vals) < 2: return m, 0.0
    return m, math.sqrt(sum((v-m)**2 for v in vals)/(len(vals)-1)/len(vals))


def fit_power_law(xs, ys):
    pairs = [(x,y) for x,y in zip(xs,ys) if y > 0.001 and not math.isnan(y)]
    if len(pairs) < 3: return float('nan'), float('nan'), float('nan')
    lx = [math.log(x) for x,_ in pairs]; ly = [math.log(y) for _,y in pairs]
    nn = len(lx); mx = sum(lx)/nn; my = sum(ly)/nn
    sxx = sum((x-mx)**2 for x in lx); sxy = sum((x-mx)*(y-my) for x,y in zip(lx,ly))
    if sxx < 1e-10: return float('nan'), float('nan'), float('nan')
    b = sxy/sxx; a = my-b*mx
    ss_res = sum((y-(a+b*x))**2 for x,y in zip(lx,ly))
    ss_tot = sum((y-my)**2 for y in ly)
    return math.exp(a), b, 1-ss_res/ss_tot if ss_tot > 0 else 0


def main():
    print("=" * 100)
    print("DIMENSIONAL MIRROR COMPARISON: 3D vs 4D Z₂")
    print(f"  k={K}, {N_SEEDS} seeds, NPL_HALF={NPL_HALF}")
    print("=" * 100)
    print()

    seeds = [s*7+3 for s in range(N_SEEDS)]
    # Scale connect_radius with dimension for similar connectivity
    configs = [
        ("3D random", 3, False, 5.0),
        ("3D mirror", 3, True, 5.0),
        ("4D mirror", 4, True, 6.0),  # larger radius for 4D connectivity
    ]

    print(f"  {'d':>3s}  {'N':>4s}  {'mode':>12s}  {'d_TV':>8s}  {'pur_cl':>8s}  "
          f"{'1-pur':>8s}  {'gravity':>10s}  {'ok':>3s}  {'time':>5s}")
    print(f"  {'-' * 72}")

    fit_data = {}

    for label, d, use_mirror, cr in configs:
        fit_data[label] = ([], [])
        for nl in [15, 25, 40, 60]:
            t0 = time.time()
            dtv_all, pur_all, grav_all = [], [], []

            for seed in seeds:
                if use_mirror:
                    pos, adj, bl = generate_nd_mirror(nl, NPL_HALF, COORD_RANGE, cr, seed, d)
                else:
                    # Random (no mirror) — use mirror generator but don't pair edges
                    rng = random.Random(seed); positions = []; adj_r = defaultdict(list)
                    layer_indices = []
                    for layer in range(nl):
                        x = float(layer); ln = []
                        if layer == 0:
                            pos_t = tuple([x]+[0.0]*d)
                            positions.append(pos_t); ln.append(len(positions)-1)
                        else:
                            for _ in range(NPL_HALF*2):
                                coords = [x] + [rng.uniform(-COORD_RANGE,COORD_RANGE) for _ in range(d)]
                                idx = len(positions); positions.append(tuple(coords)); ln.append(idx)
                                lb = max(0,len(layer_indices)-(1 if layer==nl//3+1 else 2))
                                for pl in layer_indices[lb:]:
                                    for pi in pl:
                                        dist = math.sqrt(sum((a-b)**2 for a,b in zip(coords,positions[pi])))
                                        if dist <= cr: adj_r[pi].append(idx)
                        layer_indices.append(ln)
                    pos = positions; adj = dict(adj_r); bl = nl//3

                r = measure_nd(pos, adj, nl, K, d)
                if r:
                    dtv_all.append(r["dtv"])
                    pur_all.append(r["pur_cl"])
                    grav_all.append(r["gravity"])

            dt = time.time() - t0
            if pur_all:
                md, _ = _mean_se(dtv_all)
                mp, sp = _mean_se(pur_all)
                mg, sg = _mean_se(grav_all)
                omp = 1 - mp
                print(f"  {d:3d}  {nl:4d}  {label:>12s}  {md:8.4f}  {mp:7.4f}±{sp:.02f}  "
                      f"{omp:8.4f}  {mg:+7.4f}±{sg:.3f}  {len(pur_all):3d}  {dt:4.0f}s")
                if omp > 0.001:
                    fit_data[label][0].append(nl)
                    fit_data[label][1].append(omp)
            else:
                print(f"  {d:3d}  {nl:4d}  {label:>12s}  FAIL  {dt:4.0f}s")

        print()

    # Power law fits
    print("DECOHERENCE EXPONENT COMPARISON")
    print(f"  {'mode':>12s}  {'A':>8s}  {'alpha':>8s}  {'R²':>6s}")
    print(f"  {'-' * 38}")
    for label, _, _, _ in configs:
        ns, ys = fit_data[label]
        A, alpha, r2 = fit_power_law(ns, ys)
        if not math.isnan(alpha):
            print(f"  {label:>12s}  {A:8.3f}  {alpha:8.2f}  {r2:6.3f}")
        else:
            print(f"  {label:>12s}  insufficient data")

    print()
    print("PREDICTION: 4D mirror exponent < 3D mirror exponent (-0.27)")
    print("  If confirmed: 4D mirror is the ultimate architecture")


if __name__ == "__main__":
    main()
