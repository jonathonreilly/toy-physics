#!/usr/bin/env python3
"""IF kernel sweep: compare angle-only, multi-obs, and CA-microstate kernels.

Landed generator script for the kernel comparison results.
Tests three kernels in the influence-functional framework:
  1. Angle-only: K = ∏ cos(α × Δθ_k)
  2. Multi-obs: K = ∏ cos(α × (Δθ + Δsector + Δy))
  3. Multi-obs+CA: K = ∏ cos(α × (Δθ + Δsector + Δy + Δca_phase))

Uses promoted propagator: 1/L^p × exp(-0.8×θ²)

PStack experiment: if-kernel-sweep
"""

from __future__ import annotations
import math
import cmath
import time
from collections import defaultdict, deque
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scripts.generative_causal_dag_interference import generate_causal_dag
from scripts.density_matrix_analysis import build_post_barrier_setup

BETA = 0.8
MAX_HIST = 3
ALPHA = 2.0
N_CA = 3


def propagate_with_obs(positions, adj, field, src, det, k, mass_set, blocked):
    n = len(positions)
    layer_of = {idx: round(x) for idx, (x, y) in enumerate(positions)}
    in_deg = [0]*n
    for i, nbs in adj.items():
        for j in nbs: in_deg[j] += 1
    q = deque(i for i in range(n) if in_deg[i] == 0)
    order = []
    while q:
        i = q.popleft(); order.append(i)
        for j in adj.get(i, []):
            in_deg[j] -= 1
            if in_deg[j] == 0: q.append(j)
    state = {}
    for s in src: state[(s, ())] = 1.0/len(src)+0.0j
    processed = set()
    for i in order:
        if i in processed: continue
        processed.add(i)
        entries = {h: a for (nd,h), a in list(state.items()) if nd==i and abs(a)>1e-30}
        if not entries or i in blocked: continue
        for hist, amp in entries.items():
            for j in adj.get(i, []):
                if j in blocked: continue
                x1,y1=positions[i]; x2,y2=positions[j]
                dx,dy=x2-x1,y2-y1; L=math.sqrt(dx*dx+dy*dy)
                if L<1e-10: continue
                te=math.atan2(abs(dy),max(dx,1e-10))
                lf=0.5*(field[i]+field[j])
                dl=L*(1+lf); ret=math.sqrt(max(dl*dl-L*L,0)); act=dl-ret
                w=math.exp(-BETA*te*te); ea=cmath.exp(1j*k*act)*w/(L**1.0)
                if j in mass_set and len(hist)<MAX_HIST:
                    sector = int(math.atan2(dy,dx)*4/math.pi+0.5)%8
                    y_bin = int((positions[j][1]+12)/3)
                    ca_phase = layer_of.get(j, 0) % N_CA
                    obs = (te, sector, y_bin, ca_phase)
                    new_hist = hist+(obs,)
                else:
                    new_hist = hist
                key=(j,new_hist)
                if key not in state: state[key]=0.0+0.0j
                state[key] += amp*ea
    return {(d,h): a for (d,h), a in state.items() if d in det}


def angle_kernel(ha, hb, alpha):
    m = max(len(ha), len(hb))
    if m == 0: return 1.0
    v = 1.0
    for i in range(m):
        ta = ha[i][0] if i<len(ha) else 0.0
        tb = hb[i][0] if i<len(hb) else 0.0
        v *= math.cos(alpha*(ta-tb))
    return v


def multi_kernel(ha, hb, alpha):
    m = max(len(ha), len(hb))
    if m == 0: return 1.0
    v = 1.0
    for i in range(m):
        if i < len(ha) and i < len(hb):
            ta,sa,ya,ca = ha[i]; tb,sb,yb,cb = hb[i]
            d = abs(ta-tb) + min(abs(sa-sb),8-abs(sa-sb))/4.0 + abs(ya-yb)/8.0
            v *= math.cos(alpha*d)
        else:
            v *= math.cos(alpha*0.5)
    return v


def ca_kernel(ha, hb, alpha):
    m = max(len(ha), len(hb))
    if m == 0: return 1.0
    v = 1.0
    for i in range(m):
        if i < len(ha) and i < len(hb):
            ta,sa,ya,ca = ha[i]; tb,sb,yb,cb = hb[i]
            d = abs(ta-tb) + min(abs(sa-sb),8-abs(sa-sb))/4.0 + abs(ya-yb)/8.0
            d += (0 if ca==cb else 1.0)
            v *= math.cos(alpha*d)
        else:
            v *= math.cos(alpha*0.5)
    return v


def if_purity(ds_a, ds_b, det_list, kernel_fn, alpha):
    aa = defaultdict(list)
    bb = defaultdict(list)
    for (d,h),a in ds_a.items(): aa[d].append((h,a))
    for (d,h),a in ds_b.items(): bb[d].append((h,a))
    rho = {}
    for d1 in det_list:
        for d2 in det_list:
            v = 0.0+0.0j
            for h1,a1 in aa.get(d1,[]):
                for h2,a2 in aa.get(d2,[]): v += a1.conjugate()*a2
            for h1,a1 in bb.get(d1,[]):
                for h2,a2 in bb.get(d2,[]): v += a1.conjugate()*a2
            for ha,aA in aa.get(d1,[]):
                for hb,aB in bb.get(d2,[]):
                    v += aA.conjugate()*aB*kernel_fn(ha,hb,alpha)
            for hb,aB in bb.get(d1,[]):
                for ha,aA in aa.get(d2,[]):
                    v += aB.conjugate()*aA*kernel_fn(hb,ha,alpha)
            rho[(d1,d2)] = v
    tr = sum(rho.get((d,d),0) for d in det_list).real
    if tr <= 1e-30: return math.nan
    for k in rho: rho[k] /= tr
    return sum(abs(vv)**2 for vv in rho.values()).real


def main():
    k = 5.0
    t0 = time.time()

    print("=" * 70)
    print("IF KERNEL SWEEP")
    print(f"  α={ALPHA}, cap={MAX_HIST}, k={k}")
    print("=" * 70)
    print()
    print(f"  {'N':>4s}  {'angle':>8s}  {'multi':>8s}  {'multi+CA':>8s}  {'time':>5s}")
    print(f"  {'-' * 36}")

    for nl in [8, 12, 18]:
        da, dm, dc = [], [], []
        for seed in range(3):
            positions, adj, _ = generate_causal_dag(n_layers=nl, nodes_per_layer=25,
                y_range=12.0, connect_radius=3.0, rng_seed=seed*11+7)
            setup = build_post_barrier_setup(positions, adj,
                env_depth_layers=max(1,round(nl/6)))
            if setup is None: continue
            mass_set = set(setup["mass_set"])-setup["blocked"]
            blocked = setup["blocked"]
            bl_idx = len(setup["layers"])//3
            bi = setup["by_layer"][setup["layers"][bl_idx]]
            cy = setup["cy"]
            sa = set(i for i in bi if positions[i][1] > cy+3)
            sb = set(i for i in bi if positions[i][1] < cy-3)

            ds_a = propagate_with_obs(positions, adj, setup["field"],
                setup["src"], setup["det"], k, mass_set, blocked|sb)
            ds_b = propagate_with_obs(positions, adj, setup["field"],
                setup["src"], setup["det"], k, mass_set, blocked|sa)

            p0 = if_purity(ds_a, ds_b, setup["det_list"], lambda h1,h2,a: 1.0, 0)
            pa = if_purity(ds_a, ds_b, setup["det_list"], angle_kernel, ALPHA)
            pm = if_purity(ds_a, ds_b, setup["det_list"], multi_kernel, ALPHA)
            pc = if_purity(ds_a, ds_b, setup["det_list"], ca_kernel, ALPHA)

            if not math.isnan(pa): da.append(p0-pa)
            if not math.isnan(pm): dm.append(p0-pm)
            if not math.isnan(pc): dc.append(p0-pc)

        dt = time.time()-t0
        if da:
            print(f"  {nl:4d}  {sum(da)/len(da):+8.4f}  {sum(dm)/len(dm):+8.4f}  "
                  f"{sum(dc)/len(dc):+8.4f}  {dt:4.0f}s")

    print()
    print("angle = edge angle only")
    print("multi = angle + sector + y_bin")
    print("multi+CA = angle + sector + y_bin + CA phase")
    print()
    print("TEST COMPLETE")


if __name__ == "__main__":
    main()
