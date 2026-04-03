#!/usr/bin/env python3
"""Self-consistent mass-field loop.

Current approach: propagate free → identify mass → compute field →
propagate in field. Two separate steps.

Self-consistent: iterate until the mass identified from propagation-in-field
matches the mass used to compute the field. This is the discrete analogue
of "mass tells geometry how to curve, geometry tells mass how to move."

Also tests: does self-consistency IMPROVE or WORSEN the results?
And: does it converge at all?
"""

from __future__ import annotations
import math
import cmath
import random as rng_mod
from collections import defaultdict, deque

BETA = 0.8


def grow_geometric_dag(n_layers=20, npl=25, d_growth=3,
                        connect_radius=3.0, spread=1.0, rng_seed=42):
    rng = rng_mod.Random(rng_seed)
    positions = []
    adj = defaultdict(list)
    layer_indices = []
    for layer in range(n_layers):
        x = float(layer)
        layer_nodes = []
        if layer == 0:
            positions.append(tuple([x] + [0.0] * d_growth))
            layer_nodes.append(0)
        else:
            prev = []
            for pl in layer_indices[max(0, layer - 2):]:
                prev.extend(pl)
            for _ in range(npl):
                parent = rng.choice(prev)
                pp = positions[parent]
                pos = tuple([x] + [pp[1+d] + rng.gauss(0, spread) for d in range(d_growth)])
                idx = len(positions)
                positions.append(pos)
                layer_nodes.append(idx)
                for pi in prev:
                    dist = math.sqrt(sum((a-b)**2 for a,b in zip(pos, positions[pi])))
                    if dist <= connect_radius:
                        adj[pi].append(idx)
        layer_indices.append(layer_nodes)
    return positions, dict(adj)


def _topo_order(adj, n):
    in_deg = [0]*n
    for nbs in adj.values():
        for j in nbs: in_deg[j] += 1
    q = deque(i for i in range(n) if in_deg[i] == 0)
    order = []
    while q:
        i = q.popleft(); order.append(i)
        for j in adj.get(i, []):
            in_deg[j] -= 1
            if in_deg[j] == 0: q.append(j)
    return order


def propagate(positions, adj, field, src, k, damping=None):
    n = len(positions)
    damping = damping or [1.0]*n
    order = _topo_order(adj, n)
    amps = [0j]*n
    for s in src: amps[s] = 1.0/len(src)
    for i in order:
        if abs(amps[i]) < 1e-30: continue
        amps[i] *= damping[i]
        if abs(amps[i]) < 1e-30: continue
        for j in adj.get(i, []):
            ip, jp = positions[i], positions[j]
            dsq = sum((a-b)**2 for a,b in zip(ip,jp))
            L = math.sqrt(dsq)
            if L < 1e-10: continue
            lf = 0.5*(field[i]+field[j])
            dl = L*(1+lf); ret = math.sqrt(max(dl*dl-L*L, 0)); act = dl-ret
            dx = jp[0]-ip[0]; trans = math.sqrt(dsq-dx*dx)
            theta = math.atan2(trans, max(dx, 1e-10))
            w = math.exp(-BETA*theta*theta)
            ea = cmath.exp(1j*k*act)*w/L
            amps[j] += amps[i]*ea
    return amps


def compute_field(positions, mass_nodes, strength=0.3):
    n = len(positions)
    field = [0.0]*n
    for m in mass_nodes:
        mp = positions[m]
        for i in range(n):
            ip = positions[i]
            r = math.sqrt(sum((a-b)**2 for a,b in zip(ip,mp)))+0.1
            field[i] += strength/r
    return field


def identify_mass(amps, positions, by_layer, layers, cy, mid_start, mid_end, frac=0.2):
    """Identify mass nodes from amplitude in upper half of mid-graph."""
    mid_upper = []
    for layer in layers[mid_start:mid_end]:
        for i in by_layer[layer]:
            if positions[i][1] > cy: mid_upper.append(i)
    if len(mid_upper) < 2: return []
    ranked = sorted([(i, abs(amps[i])**2) for i in mid_upper], key=lambda x: -x[1])
    return [i for i,_ in ranked[:max(2, int(len(ranked)*frac))]]


def self_consistent_loop(positions, adj, src, by_layer, layers, cy,
                          mid_start, mid_end, k=5.0, damping=None,
                          max_iter=10, strength=0.3):
    """Iterate mass→field→propagate→mass until convergence.

    Returns: (field, mass_nodes, converged, n_iter)
    """
    n = len(positions)
    field = [0.0]*n
    prev_mass = set()

    for iteration in range(max_iter):
        amps = propagate(positions, adj, field, src, k, damping)
        mass = identify_mass(amps, positions, by_layer, layers, cy, mid_start, mid_end)
        mass_set = set(mass)

        # Check convergence: same mass nodes as previous iteration?
        if mass_set == prev_mass:
            return field, mass, True, iteration + 1

        # Update field
        field = compute_field(positions, mass, strength)
        prev_mass = mass_set

    return field, mass, False, max_iter


def run_test(nl, d_growth, seed):
    positions, adj = grow_geometric_dag(nl, 30, d_growth, 3.5, 1.2, seed)
    n = len(positions)

    by_layer = defaultdict(list)
    for idx in range(n): by_layer[round(positions[idx][0])].append(idx)
    layers = sorted(by_layer.keys())
    if len(layers) < 7: return None

    src = by_layer[layers[0]]
    det_list = list(by_layer[layers[-1]])
    if not det_list: return None

    bl_idx = len(layers)//3
    bi = by_layer[layers[bl_idx]]
    if len(bi) < 6: return None

    # Emergent barrier
    flat = [0.0]*n
    amps_b = propagate(positions, adj, flat, src, 5.0)
    barrier_amps = sorted([(i, abs(amps_b[i])**2) for i in bi], key=lambda x: -x[1])
    n_slit = max(2, len(barrier_amps)//4)
    slit_nodes = set(i for i,_ in barrier_amps[:n_slit])
    damping = [1.0]*n
    for i in bi:
        damping[i] = 1.0 if i in slit_nodes else 0.0

    cy = sum(positions[i][1] for i in slit_nodes)/len(slit_nodes)
    sa = [i for i in slit_nodes if positions[i][1] > cy]
    sb = [i for i in slit_nodes if positions[i][1] <= cy]
    if not sa or not sb: return None

    mid_start = len(layers)//2
    mid_end = min(len(layers)-1, mid_start+4)

    # Self-consistent loop
    field_sc, mass_sc, converged, n_iter = self_consistent_loop(
        positions, adj, src, by_layer, layers, cy, mid_start, mid_end,
        k=5.0, damping=damping, max_iter=10, strength=0.3)

    # Also get the one-shot result for comparison
    amps_free = propagate(positions, adj, flat, src, 5.0, damping)
    mass_oneshot = identify_mass(amps_free, positions, by_layer, layers, cy, mid_start, mid_end)
    field_oneshot = compute_field(positions, mass_oneshot, 0.3)

    # Measure gravity + decoherence for both
    results = {}
    for label, field_use in [("oneshot", field_oneshot), ("self_consistent", field_sc)]:
        pm_vals, gd_vals = [], []
        for k in [3.0, 5.0, 7.0]:
            # Decoherence
            da = list(damping); db = list(damping)
            for i in sb: da[i] = 0.0
            for i in sa: db[i] = 0.0
            aa = propagate(positions, adj, field_use, src, k, da)
            ab = propagate(positions, adj, field_use, src, k, db)
            rho = {}
            for d1 in det_list:
                for d2 in det_list:
                    rho[(d1,d2)] = aa[d1].conjugate()*aa[d2]+ab[d1].conjugate()*ab[d2]
            tr = sum(rho[(d,d)] for d in det_list).real
            if tr > 1e-30:
                for key in rho: rho[key] /= tr
                pm_vals.append(sum(abs(v)**2 for v in rho.values()).real)
            # Gravity
            am = propagate(positions, adj, field_use, src, k, damping)
            af = propagate(positions, adj, flat, src, k, damping)
            pm = sum(abs(am[d])**2 for d in det_list)
            pf = sum(abs(af[d])**2 for d in det_list)
            if pm > 1e-30 and pf > 1e-30:
                ym = sum(abs(am[d])**2*positions[d][1] for d in det_list)/pm
                yf = sum(abs(af[d])**2*positions[d][1] for d in det_list)/pf
                gd_vals.append(ym-yf)

        if pm_vals:
            results[label] = {
                "pm": sum(pm_vals)/len(pm_vals),
                "grav": sum(gd_vals)/len(gd_vals) if gd_vals else 0.0,
            }

    return {
        "converged": converged, "n_iter": n_iter,
        "oneshot": results.get("oneshot"),
        "sc": results.get("self_consistent"),
        "mass_overlap": len(set(mass_sc) & set(mass_oneshot)) / max(1, len(mass_oneshot)),
    }


def main():
    import time

    print("=" * 70)
    print("SELF-CONSISTENT MASS-FIELD LOOP")
    print("  Iterate: propagate → mass → field → propagate → mass...")
    print("  Does it converge? Does it improve results?")
    print("=" * 70)
    print()

    n_seeds = 16

    for d_growth in [3]:
        print(f"  [d_growth={d_growth} ({d_growth+1}D)]")
        print(f"  {'N':>3s}  {'conv':>4s}  {'iter':>4s}  {'overlap':>7s}  "
              f"{'pm_1':>6s}  {'pm_sc':>6s}  {'g_1':>7s}  {'g_sc':>7s}")
        print(f"  {'-' * 56}")

        for nl in [18, 25, 30]:
            t0 = time.time()
            conv_all, iter_all, overlap_all = [], [], []
            pm1_all, pmsc_all, g1_all, gsc_all = [], [], [], []

            for seed_i in range(n_seeds):
                r = run_test(nl, d_growth, seed_i * 7 + 3)
                if r and r["oneshot"] and r["sc"]:
                    conv_all.append(r["converged"])
                    iter_all.append(r["n_iter"])
                    overlap_all.append(r["mass_overlap"])
                    pm1_all.append(r["oneshot"]["pm"])
                    pmsc_all.append(r["sc"]["pm"])
                    g1_all.append(r["oneshot"]["grav"])
                    gsc_all.append(r["sc"]["grav"])

            dt = time.time() - t0
            if pm1_all:
                n_ok = len(pm1_all)
                conv_pct = sum(conv_all) / n_ok
                avg_iter = sum(iter_all) / n_ok
                avg_ov = sum(overlap_all) / n_ok
                apm1 = sum(pm1_all) / n_ok
                apmsc = sum(pmsc_all) / n_ok
                ag1 = sum(g1_all) / n_ok
                agsc = sum(gsc_all) / n_ok
                better = "SC+" if apmsc < apm1 else "1S+"
                print(f"  {nl:3d}  {conv_pct:4.0%}  {avg_iter:4.1f}  {avg_ov:7.1%}  "
                      f"{apm1:.4f}  {apmsc:.4f}  {ag1:+7.3f}  {agsc:+7.3f}  {better}")
            else:
                print(f"  {nl:3d}  FAIL")
            import sys; sys.stdout.flush()
        print()

    print("conv = fraction that converge within 10 iterations")
    print("overlap = fraction of mass nodes shared between oneshot and SC")
    print("SC+ = self-consistent has lower pur_min (better decoherence)")


if __name__ == "__main__":
    main()
