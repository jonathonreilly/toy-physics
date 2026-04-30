#!/usr/bin/env python3
"""
Weak-Coupling Battery — Full Sign-Sensitivity Test at G=5-10
==============================================================
The asymmetry scaling showed sign sensitivity is strongest at weak
coupling (G=5-10: 13-20% width asymmetry). Run the full battery at
this operating point to verify all properties survive.

Tests at G=5 and G=10:
  T1: Width asymmetry (attract/repulse) — should be < 0.90
  T2: Force sign (shell force) — both should be TOWARD (structural)
  T3: Norm conservation — both should be < 1e-10
  T4: Spectral gap ratio — attract should have wider gap
  T5: Iterative stability — 20 iterations, force stays TOWARD
  T6: Multi-family — random geo, growing, layered cycle
  T7: Multi-seed — 5 seeds per family

The claim: at G=5-10, the parity-coupled staggered fermion produces
measurably sign-sensitive self-gravity on irregular bipartite graphs,
with 13-20% contraction asymmetry that grows with graph size.
"""

from __future__ import annotations
import math, time, random
import numpy as np
from scipy.sparse import lil_matrix, eye as speye
from scipy.sparse.linalg import spsolve, eigsh
from collections import deque

MASS = 0.30
MU2 = 0.22
DT = 0.12
N_ITER = 40


def _ae(adj, a, b):
    adj.setdefault(a, set()).add(b)
    adj.setdefault(b, set()).add(a)


def make_random_geometric(seed=42, side=8):
    rng = random.Random(seed)
    coords,colors,index,adj=[],[],{},{}; idx=0
    for x in range(side):
        for y in range(side):
            coords.append((x+0.08*(rng.random()-0.5),y+0.08*(rng.random()-0.5)))
            colors.append((x+y)%2); index[(x,y)]=idx; idx+=1
    pos=np.array(coords); col=np.array(colors,dtype=int)
    for i in range(side):
        for j in range(side):
            a=index[(i,j)]
            for di,dj in ((1,0),(0,1),(1,1),(1,-1)):
                ii,jj=i+di,j+dj
                if (ii,jj) not in index: continue
                b=index[(ii,jj)]
                if col[a]==col[b]: continue
                if math.hypot(pos[b,0]-pos[a,0],pos[b,1]-pos[a,1])<=1.28: _ae(adj,a,b)
    return "random_geometric", pos, col, {k:list(v) for k,v in adj.items()}


def make_growing(seed=42, n_target=64):
    rng=random.Random(seed)
    coords=[(0.,0.),(1.,0.)]; colors=[0,1]; adj={0:{1},1:{0}}; cur=2
    while cur<n_target:
        px=rng.uniform(-3,3); py=rng.uniform(-3,3); nc=cur%2
        coords.append((px,py)); colors.append(nc)
        opp=[i for i in range(cur) if colors[i]!=nc]
        if opp:
            ds=[(math.hypot(px-coords[i][0],py-coords[i][1]),i) for i in opp]; ds.sort()
            for _,j in ds[:min(4,len(ds))]: _ae(adj,cur,j)
        cur+=1
    return "growing", np.array(coords), np.array(colors,dtype=int), {k:list(v) for k,v in adj.items()}


def make_layered_cycle(seed=42, layers=8, width=8):
    rng=random.Random(seed)
    coords,colors,layer_nodes=[],[],[]; idx=0
    for layer in range(layers):
        this_layer=[]
        for k in range(width):
            coords.append((float(layer),float(k)+0.05*(rng.random()-0.5)))
            colors.append(layer%2); this_layer.append(idx); idx+=1
        layer_nodes.append(this_layer)
    pos=np.array(coords); col=np.array(colors,dtype=int); n=len(pos)
    adj={i:set() for i in range(n)}
    for layer in range(layers-1):
        curr=layer_nodes[layer]; nxt=layer_nodes[layer+1]
        for i_pos,i in enumerate(curr):
            j1=nxt[i_pos%len(nxt)]; adj[i].add(j1); adj[j1].add(i)
            j2=nxt[(i_pos+1)%len(nxt)]
            if j2!=j1: adj[i].add(j2); adj[j2].add(i)
    return "layered_cycle", pos, col, {k:list(v) for k,v in adj.items()}


def _build_L(pos,adj,n):
    L=lil_matrix((n,n),dtype=float)
    for i,nbs in adj.items():
        for j in nbs:
            if i>=j: continue
            d=math.hypot(pos[j,0]-pos[i,0],pos[j,1]-pos[i,1])
            w=1./max(d,0.5); L[i,j]-=w; L[j,i]-=w; L[i,i]+=w; L[j,j]+=w
    return L.tocsr()


def _build_H(pos,col,adj,n,phi):
    H=lil_matrix((n,n),dtype=complex)
    par=np.where(col==0,1.,-1.); H.setdiag((MASS+phi)*par)
    for i,nbs in adj.items():
        for j in nbs:
            if i>=j: continue
            d=math.hypot(pos[j,0]-pos[i,0],pos[j,1]-pos[i,1])
            w=1./max(d,0.5); H[i,j]+=-0.5j*w; H[j,i]+=0.5j*w
    return H.tocsr()


def _cn_step(H,psi,dt):
    n=H.shape[0]
    ap=(speye(n,format='csc')+1j*H*dt/2).tocsc()
    am=speye(n,format='csr')-1j*H*dt/2
    return spsolve(ap,am.dot(psi))


def _width(psi,pos):
    rho=np.abs(psi)**2; rho/=np.sum(rho)
    cx=np.sum(rho*pos[:,0]); cy=np.sum(rho*pos[:,1])
    return np.sqrt(np.sum(rho*((pos[:,0]-cx)**2+(pos[:,1]-cy)**2)))


def _shell_force(depth,n,psi,phi):
    max_d=int(np.max(depth[np.isfinite(depth)])) if np.any(np.isfinite(depth)) else 0
    if max_d<=0: return 0.
    rho=np.abs(psi)**2; rho_n=rho/np.sum(rho)
    ps=np.zeros(max_d+1); P=np.zeros(max_d+1); cnt=np.zeros(max_d+1)
    for i in range(n):
        d_=int(depth[i]) if np.isfinite(depth[i]) else -1
        if 0<=d_<=max_d: ps[d_]+=phi[i]; P[d_]+=rho_n[i]; cnt[d_]+=1
    for d_ in range(max_d+1):
        if cnt[d_]>0: ps[d_]/=cnt[d_]
    grad=np.zeros(max_d+1)
    for d_ in range(max_d+1):
        if d_==0: grad[d_]=ps[0]-ps[min(1,max_d)]
        elif d_==max_d: grad[d_]=ps[d_-1]-ps[d_]
        else: grad[d_]=0.5*(ps[d_-1]-ps[d_+1])
    return float(np.sum(P*grad))


def run_full_test(name, pos, col, adj, G, seed_label):
    n = len(pos)
    center = np.mean(pos, axis=0)
    dists_c = np.sqrt(np.sum((pos-center)**2, axis=1))
    src = np.argmin(dists_c)
    L = _build_L(pos, adj, n)

    depth = np.full(n, np.inf); depth[src] = 0; q = deque([src])
    while q:
        i = q.popleft()
        for j in adj.get(i, []):
            if depth[j] == np.inf: depth[j] = depth[i]+1; q.append(j)

    psi0 = np.exp(-0.5*dists_c**2/1.15**2).astype(complex)
    psi0 /= np.linalg.norm(psi0)
    w0 = _width(psi0, pos)

    results = {}
    for label, phi_sign in [("a", +1.0), ("r", -1.0), ("f", 0.0)]:
        psi = psi0.copy()
        forces = []
        for it in range(N_ITER):
            rho = np.abs(psi)**2
            phi = phi_sign*spsolve((L+MU2*speye(n,format='csr')).tocsc(),G*rho) if phi_sign!=0 else np.zeros(n)
            F = _shell_force(depth, n, psi, phi)
            forces.append(F)
            H = _build_H(pos, col, adj, n, phi)
            psi = _cn_step(H, psi, DT)

        wf = _width(psi, pos)
        norm = np.linalg.norm(psi)
        tw = sum(1 for f in forces if f > 0)

        # Final spectral gap
        rho_f = np.abs(psi)**2
        phi_f = phi_sign*spsolve((L+MU2*speye(n,format='csr')).tocsc(),G*rho_f) if phi_sign!=0 else np.zeros(n)
        H_f = _build_H(pos, col, adj, n, phi_f)
        try:
            evals = eigsh(H_f.tocsc(), k=min(6,n-2), which='SM', return_eigenvectors=False)
            gap = float(np.min(np.abs(evals[evals != 0]))) if any(evals != 0) else float('nan')
        except Exception:
            gap = float('nan')

        results[label] = {"w": wf, "norm": norm, "tw": tw, "gap": gap, "forces": forces}

    w_asym = (results["a"]["w"]/results["f"]["w"]) / (results["r"]["w"]/results["f"]["w"])
    gap_ratio = results["a"]["gap"] / results["r"]["gap"] if results["r"]["gap"] > 0 else float('nan')

    return {
        "name": name, "seed": seed_label, "G": G,
        "w_asym": w_asym,
        "gap_ratio": gap_ratio,
        "tw_a": results["a"]["tw"], "tw_r": results["r"]["tw"],
        "norm_a": results["a"]["norm"], "norm_r": results["r"]["norm"],
        "w_a": results["a"]["w"]/w0, "w_r": results["r"]["w"]/w0, "w_f": results["f"]["w"]/w0,
    }


if __name__ == '__main__':
    t0 = time.time()
    print("=" * 82)
    print("WEAK-COUPLING BATTERY — FULL SIGN-SENSITIVITY AT G=5, G=10")
    print("=" * 82)
    print()

    for G in [5, 10]:
        print(f"{'='*82}")
        print(f"G = {G}")
        print(f"{'='*82}")
        print(f"{'family':<18s} {'seed':>4s} {'w_asym':>8s} {'gap_r':>8s} "
              f"{'tw_a':>5s} {'tw_r':>5s} {'norm_a':>8s} "
              f"{'w_a':>7s} {'w_r':>7s} {'w_f':>7s}")
        print("-" * 88)

        all_asym = []
        for make_fn, seeds in [
            (lambda s: make_random_geometric(seed=s, side=8), [42,43,44,45,46]),
            (lambda s: make_growing(seed=s, n_target=64), [42,43,44,45,46]),
            (lambda s: make_layered_cycle(seed=s, layers=8, width=8), [42,43,44,45,46]),
        ]:
            for s in seeds:
                fname, pos, col, adj = make_fn(s)
                r = run_full_test(fname, pos, col, adj, G, str(s))
                all_asym.append(r["w_asym"])
                print(f"{fname:<18s} {r['seed']:>4s} {r['w_asym']:8.4f} "
                      f"{r['gap_ratio']:8.4f} "
                      f"{r['tw_a']:5d} {r['tw_r']:5d} {r['norm_a']:8.6f} "
                      f"{r['w_a']:7.4f} {r['w_r']:7.4f} {r['w_f']:7.4f}")

        all_lt1 = sum(1 for a in all_asym if a < 1.0)
        mean_asym = np.mean(all_asym)
        print(f"\n  Summary G={G}: {all_lt1}/{len(all_asym)} have w_asym < 1, "
              f"mean={mean_asym:.4f}, "
              f"effect={(1-mean_asym)*100:.1f}%")
        print()

    print(f"Total time: {time.time()-t0:.1f}s")
