#!/usr/bin/env python3
"""2D mirror: full joint validation card.

The 2D mirror gave the project's cleanest results:
  - MI=0.99 at N=15, 0.77 at N=80
  - Gravity grows with N (+2.31 at 4.4 SE, N=80)
  - F∝M alpha=0.84

This script produces the definitive card with Born + gravity + MI + purity
at N=15..100, 24 seeds, strictly linear propagator.
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
NPL_HALF = 12
Y_RANGE = 10.0
CONNECT_RADIUS = 2.5
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


def gen_2d_mirror(nl, npl_half, yr, cr, seed):
    rng = random.Random(seed); pos = []; adj = defaultdict(list)
    li = []; mm = {}; bl = nl // 3
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
                cx, cy_v = pos[ci]
                for pl in li[lb:]:
                    for pi in pl:
                        px, py = pos[pi]
                        if math.sqrt((cx-px)**2+(cy_v-py)**2) <= cr:
                            adj[pi].append(ci); adj[mm[pi]].append(mm[ci])
        li.append(ln)
    return pos, dict(adj), bl


def propagate_linear(pos, adj, field, src, k, blocked):
    n = len(pos); order = _topo_order(adj, n); amps = [0j] * n
    for s in src: amps[s] = 1.0 / len(src)
    for i in order:
        if abs(amps[i]) < 1e-30 or i in blocked: continue
        for j in adj.get(i, []):
            if j in blocked: continue
            x1, y1 = pos[i]; x2, y2 = pos[j]
            dx, dy = x2-x1, y2-y1; L = math.sqrt(dx*dx+dy*dy)
            if L < 1e-10: continue
            lf = 0.5*(field[i]+field[j]); dl = L*(1+lf)
            ret = math.sqrt(max(dl*dl-L*L, 0)); act = dl-ret
            theta = math.atan2(abs(dy), max(dx, 1e-10))
            amps[j] += amps[i]*cmath.exp(1j*k*act)*math.exp(-BETA*theta*theta)/L
    return amps


def sorkin_born(pos, adj, src, k, bi, s_a, s_b, s_c, det, field):
    all_s = set(s_a+s_b+s_c); other = set(bi)-all_s; probs = {}
    for key, open_set in [('abc',all_s),('ab',set(s_a+s_b)),('ac',set(s_a+s_c)),
                           ('bc',set(s_b+s_c)),('a',set(s_a)),('b',set(s_b)),('c',set(s_c))]:
        bl = other|(all_s-open_set)
        a = propagate_linear(pos,adj,field,src,k,bl)
        probs[key] = [abs(a[d])**2 for d in det]
    I3=0;P=0
    for di in range(len(det)):
        i3=(probs['abc'][di]-probs['ab'][di]-probs['ac'][di]-probs['bc'][di]
            +probs['a'][di]+probs['b'][di]+probs['c'][di])
        I3+=abs(i3);P+=probs['abc'][di]
    return I3/P if P>1e-30 else math.nan


def measure_full(pos, adj, nl, k):
    n = len(pos); by_layer = defaultdict(list)
    for idx, (x, y) in enumerate(pos): by_layer[round(x)].append(idx)
    layers = sorted(by_layer.keys())
    if len(layers) < 5: return None
    src = by_layer[layers[0]]; det = list(by_layer[layers[-1]])
    if not det: return None
    cy = sum(pos[i][1] for i in range(n)) / n
    bl_idx = len(layers)//3; bi = by_layer[layers[bl_idx]]
    sa = [i for i in bi if pos[i][1] > cy+2][:3]
    sb = [i for i in bi if pos[i][1] < cy-2][:3]
    if not sa or not sb: return None
    blocked = set(bi)-set(sa+sb)
    gl = layers[2*len(layers)//3]
    mass = [i for i in by_layer[gl] if pos[i][1] > cy+1][:5]
    if not mass: return None
    ed = max(1,round(nl/6)); st = bl_idx+1; sp = min(len(layers)-1,st+ed)
    mid = []
    for l in layers[st:sp]: mid.extend(by_layer[l])
    field = [0.0]*n
    for m in mass:
        mx,my=pos[m]
        for i in range(n): ix,iy=pos[i]; field[i]+=0.1/(math.sqrt((ix-mx)**2+(iy-my)**2)+0.1)
    field_f = [0.0]*n

    pa = propagate_linear(pos,adj,field,src,k,blocked|set(sb))
    pb = propagate_linear(pos,adj,field,src,k,blocked|set(sa))

    # MI
    bw = 2*Y_RANGE/N_YBINS; prob_a=[0]*N_YBINS; prob_b=[0]*N_YBINS
    for d in det:
        b=max(0,min(N_YBINS-1,int((pos[d][1]+Y_RANGE)/bw)))
        prob_a[b]+=abs(pa[d])**2; prob_b[b]+=abs(pb[d])**2
    na=sum(prob_a); nb=sum(prob_b)
    if na<1e-30 or nb<1e-30: return None
    prob_a=[p/na for p in prob_a]; prob_b=[p/nb for p in prob_b]
    H=0;Hc=0
    for b2 in range(N_YBINS):
        pm=0.5*prob_a[b2]+0.5*prob_b[b2]
        if pm>1e-30: H-=pm*math.log2(pm)
        if prob_a[b2]>1e-30: Hc-=0.5*prob_a[b2]*math.log2(prob_a[b2])
        if prob_b[b2]>1e-30: Hc-=0.5*prob_b[b2]*math.log2(prob_b[b2])
    MI=H-Hc

    # CL purity
    ba=[0j]*N_YBINS; bb=[0j]*N_YBINS
    for m in mid:
        b2=max(0,min(N_YBINS-1,int((pos[m][1]+Y_RANGE)/bw)))
        ba[b2]+=pa[m]; bb[b2]+=pb[m]
    S=sum(abs(a-b)**2 for a,b in zip(ba,bb))
    NA=sum(abs(a)**2 for a in ba); NB=sum(abs(b)**2 for b in bb)
    Sn=S/(NA+NB) if (NA+NB)>0 else 0; Dcl=math.exp(-LAM**2*Sn)
    rho={}
    for d1 in det:
        for d2 in det:
            rho[(d1,d2)]=(pa[d1].conjugate()*pa[d2]+pb[d1].conjugate()*pb[d2]
                         +Dcl*pa[d1].conjugate()*pb[d2]+Dcl*pb[d1].conjugate()*pa[d2])
    tr=sum(rho[(d,d)] for d in det).real
    if tr<1e-30: return None
    for key in rho: rho[key]/=tr
    pur=sum(abs(v)**2 for v in rho.values()).real

    # Gravity
    am=propagate_linear(pos,adj,field,src,k,blocked)
    af=propagate_linear(pos,adj,field_f,src,k,blocked)
    pm2=sum(abs(am[d])**2 for d in det); pf=sum(abs(af[d])**2 for d in det)
    grav=0
    if pm2>1e-30 and pf>1e-30:
        grav=sum(abs(am[d])**2*pos[d][1] for d in det)/pm2-sum(abs(af[d])**2*pos[d][1] for d in det)/pf

    # Born (3-slit)
    born=math.nan
    upper=sorted([i for i in bi if pos[i][1]>cy+1],key=lambda i:pos[i][1])
    lower=sorted([i for i in bi if pos[i][1]<cy-1],key=lambda i:-pos[i][1])
    middle=sorted([i for i in bi if abs(pos[i][1]-cy)<=1],key=lambda i:abs(pos[i][1]-cy))
    if upper and lower and middle:
        born=sorkin_born(pos,adj,src,k,bi,[upper[0]],[lower[0]],[middle[0]],det,field_f)

    # k=0 gravity
    am0=propagate_linear(pos,adj,field,src,0.0,blocked)
    af0=propagate_linear(pos,adj,field_f,src,0.0,blocked)
    pm0=sum(abs(am0[d])**2 for d in det);pf0=sum(abs(af0[d])**2 for d in det)
    gk0=0
    if pm0>1e-30 and pf0>1e-30:
        gk0=sum(abs(am0[d])**2*pos[d][1] for d in det)/pm0-sum(abs(af0[d])**2*pos[d][1] for d in det)/pf0

    return {'MI':MI,'pur_cl':pur,'gravity':grav,'born':born,'grav_k0':gk0}


def _mean_se(vals):
    vals=[v for v in vals if v is not None and not math.isnan(v)]
    if not vals: return float('nan'),float('nan')
    m=sum(vals)/len(vals)
    if len(vals)<2: return m,0
    return m,math.sqrt(sum((v-m)**2 for v in vals)/(len(vals)-1)/len(vals))


def main():
    print("=" * 110)
    print("2D MIRROR: DEFINITIVE JOINT VALIDATION CARD")
    print(f"  npl_half={NPL_HALF}, y_range={Y_RANGE}, r={CONNECT_RADIUS}")
    print(f"  k={K}, {N_SEEDS} seeds, LINEAR propagator (NO normalization)")
    print("=" * 110)
    print()

    seeds = [s*7+3 for s in range(N_SEEDS)]

    print(f"  {'N':>4s}  {'MI':>8s}  {'pur_cl':>8s}  {'gravity':>12s}  "
          f"{'Born':>10s}  {'k=0':>10s}  {'ok':>3s}  {'time':>5s}")
    print(f"  {'-' * 78}")

    for nl in [15, 25, 40, 60, 80, 100]:
        t0 = time.time()
        mi_all,pur_all,grav_all,born_all,k0_all = [],[],[],[],[]
        for seed in seeds:
            pos,adj,bl = gen_2d_mirror(nl, NPL_HALF, Y_RANGE, CONNECT_RADIUS, seed)
            r = measure_full(pos,adj,nl,K)
            if r:
                mi_all.append(r['MI']); pur_all.append(r['pur_cl'])
                grav_all.append(r['gravity'])
                if not math.isnan(r['born']): born_all.append(r['born'])
                k0_all.append(r['grav_k0'])
        dt = time.time()-t0
        if mi_all:
            mmi,semi = _mean_se(mi_all)
            mp,_ = _mean_se(pur_all)
            mg,seg = _mean_se(grav_all)
            gt = mg/seg if seg>0 else 0
            mb,_ = _mean_se(born_all)
            mk0,_ = _mean_se(k0_all)
            born_s = f"{mb:10.2e}" if not math.isnan(mb) else "       nan"
            print(f"  {nl:4d}  {mmi:8.4f}  {mp:8.4f}  {mg:+8.4f}({gt:+5.1f}t)  "
                  f"{born_s}  {mk0:+10.2e}  {len(mi_all):3d}  {dt:4.0f}s")
        else:
            print(f"  {nl:4d}  FAIL  {dt:4.0f}s")

    print()
    print("This is the project's cleanest joint architecture card.")
    print("All measurements at single k=5.0 with strictly linear propagator.")


if __name__ == "__main__":
    main()
