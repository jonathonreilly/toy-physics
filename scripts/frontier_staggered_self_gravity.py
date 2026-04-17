#!/usr/bin/env python3
"""
Staggered Fermion Self-Gravity Probe — Retained
=================================================
True self-gravity: no external source. The matter density |psi|^2
generates its own gravitational potential via screened Poisson, which
acts back on the wavepacket.

Tests on all 3 cycle-bearing bipartite graph families:
  S1: Force TOWARD (self-generated potential always inward)
  S2: Contraction (self-gravitating packet narrower than free)
  S3: Norm conservation
  S4: Stability across iterations (force doesn't flip)
  S5: State-family robustness (gauss, color-0, color-1)
"""

from __future__ import annotations
import math, time, random
import numpy as np
from scipy.sparse import lil_matrix, csr_matrix, eye as speye
from scipy.sparse.linalg import spsolve
from collections import deque

MASS=0.30; MU2=0.22; DT=0.12; G_SELF=50.0; N_ITER=20


# ============================================================================
# Graph families (reuse from cycle battery)
# ============================================================================

def _ae(adj,a,b): adj.setdefault(a,set()).add(b); adj.setdefault(b,set()).add(a)

def _bfs(adj,src,n):
    d=np.full(n,np.inf); d[src]=0; q=deque([src])
    while q:
        i=q.popleft()
        for j in adj.get(i,[]):
            if d[j]==np.inf: d[j]=d[i]+1; q.append(j)
    return d

def make_random_geometric(seed=42, side=6):
    rng=random.Random(seed); coords=[]; colors=[]; index={}; adj={}; idx=0
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
    adj_l={k:list(v) for k,v in adj.items()}; n=len(pos); src=n//2
    return "random_geometric", pos, col, adj_l, n, src

def make_growing(seed=42, n_target=48):
    rng=random.Random(seed); coords=[(0.,0.),(1.,0.)]; colors=[0,1]; adj={0:{1},1:{0}}; cur=2
    while cur<n_target:
        px=rng.uniform(-3,3); py=rng.uniform(-3,3); nc=cur%2
        coords.append((px,py)); colors.append(nc)
        opp=[i for i in range(cur) if colors[i]!=nc]
        if opp:
            ds=[(math.hypot(px-coords[i][0],py-coords[i][1]),i) for i in opp]; ds.sort()
            for _,j in ds[:min(4,len(ds))]: _ae(adj,cur,j)
        cur+=1
    pos=np.array(coords); col=np.array(colors,dtype=int); adj_l={k:list(v) for k,v in adj.items()}
    return "growing", pos, col, adj_l, len(pos), 0

def make_layered_cycle(seed=42, layers=6, width=4):
    rng=random.Random(seed); coords=[]; colors=[]; layer_nodes=[]; idx=0
    for layer in range(layers):
        count=max(2,width); this_layer=[]
        for k in range(count):
            y=float(k)+0.05*(rng.random()-0.5)
            coords.append((float(layer),y)); colors.append(layer%2)
            this_layer.append(idx); idx+=1
        layer_nodes.append(this_layer)
    pos=np.array(coords); col=np.array(colors,dtype=int); n=len(pos)
    adj={i:set() for i in range(n)}
    for layer in range(layers-1):
        curr=layer_nodes[layer]; nxt=layer_nodes[layer+1]
        for i_pos,i in enumerate(curr):
            j1=nxt[i_pos%len(nxt)]; adj[i].add(j1); adj[j1].add(i)
            j2=nxt[(i_pos+1)%len(nxt)]
            if j2!=j1: adj[i].add(j2); adj[j2].add(i)
    adj_l={k:list(v) for k,v in adj.items()}; src=layer_nodes[0][0]
    return "layered_cycle", pos, col, adj_l, n, src


# ============================================================================
# Physics tools
# ============================================================================

def _laplacian(pos,adj,n):
    L=lil_matrix((n,n),dtype=float)
    for i,nbs in adj.items():
        for j in nbs:
            if i>=j: continue
            d=math.hypot(pos[j,0]-pos[i,0],pos[j,1]-pos[i,1])
            w=1./max(d,0.5); L[i,j]-=w; L[j,i]-=w; L[i,i]+=w; L[j,j]+=w
    return L.tocsr()

def _solve_phi(L,n,rho):
    if np.allclose(rho,0): return np.zeros(n)
    A=(L+MU2*speye(n,format='csr')).tocsc(); return spsolve(A,rho)

def _build_H(pos,col,adj,n,mass,phi):
    H=lil_matrix((n,n),dtype=complex)
    # Parity (scalar 1⊗1) coupling: Φ modulates mass gap, not energy level.
    par=np.where(col==0,1.,-1.); H.setdiag((mass+phi)*par)
    for i,nbs in adj.items():
        for j in nbs:
            if i>=j: continue
            d=math.hypot(pos[j,0]-pos[i,0],pos[j,1]-pos[i,1])
            w=1./max(d,0.5); hop=-0.5j*w; H[i,j]+=hop; H[j,i]+=np.conj(hop)
    return H.tocsr()

def _cn_step(H,n,psi):
    ap=(speye(n,format='csc')+1j*H*DT/2).tocsc(); am=speye(n,format='csr')-1j*H*DT/2
    return spsolve(ap,am.dot(psi))

def _width(psi,pos):
    rho=np.abs(psi)**2; rho/=np.sum(rho)
    cx=np.sum(rho*pos[:,0]); cy=np.sum(rho*pos[:,1])
    return np.sqrt(np.sum(rho*((pos[:,0]-cx)**2+(pos[:,1]-cy)**2)))

def _shell_force(depth,max_d,n,psi,phi):
    if max_d<=0: return 0.
    rho=np.abs(psi)**2; ps=np.zeros(max_d+1); rs=np.zeros(max_d+1); cnt=np.zeros(max_d+1)
    for i in range(n):
        d_=int(depth[i]) if np.isfinite(depth[i]) else -1
        if 0<=d_<=max_d: ps[d_]+=phi[i]; rs[d_]+=rho[i]; cnt[d_]+=1
    for d_ in range(max_d+1):
        if cnt[d_]>0: ps[d_]/=cnt[d_]; rs[d_]/=cnt[d_]
    grad=np.zeros(max_d+1)
    for d_ in range(max_d+1):
        if d_==0: grad[d_]=ps[0]-ps[min(1,max_d)]
        elif d_==max_d: grad[d_]=ps[d_-1]-ps[d_]
        else: grad[d_]=0.5*(ps[d_-1]-ps[d_+1])
    return float(np.sum(rs*grad))

def _gauss_state(pos,src,sigma=1.15):
    center=pos[src]; rel=pos-center
    psi=np.exp(-0.5*(rel[:,0]**2+rel[:,1]**2)/sigma**2).astype(complex)
    return psi/np.linalg.norm(psi)

def _color_state(pos,col,src,target):
    psi=_gauss_state(pos,src); psi[col!=target]=0
    nm=np.linalg.norm(psi); return psi/nm if nm>0 else psi


# ============================================================================
# Self-gravity probe
# ============================================================================

def run_self_gravity(name, pos, col, adj, n, src):
    print(f"\n{'='*70}")
    print(f"SELF-GRAVITY: {name} ({n} nodes)")
    print(f"{'='*70}")

    L = _laplacian(pos, adj, n)
    depth = _bfs(adj, src, n)
    max_d = int(np.max(depth[np.isfinite(depth)])) if np.any(np.isfinite(depth)) else 0
    H_free = _build_H(pos,col,adj,n,MASS,np.zeros(n))

    score = 0

    # Self-gravity loop
    psi_self = _gauss_state(pos, src)
    psi_free = psi_self.copy()
    forces=[]; widths_self=[]; widths_free=[]; norms=[]

    for it in range(N_ITER):
        # Self-gravity: rho -> Phi -> H -> psi
        rho = np.abs(psi_self)**2
        phi = _solve_phi(L, n, G_SELF * rho)
        H = _build_H(pos,col,adj,n,MASS,phi)
        psi_self = _cn_step(H, n, psi_self)
        psi_free = _cn_step(H_free, n, psi_free)

        forces.append(_shell_force(depth,max_d,n,psi_self,phi))
        widths_self.append(_width(psi_self,pos))
        widths_free.append(_width(psi_free,pos))
        norms.append(float(np.linalg.norm(psi_self)))

    # S1: Force TOWARD
    n_tw = sum(1 for f in forces if f > 0)
    p1 = n_tw == N_ITER; score += p1
    print(f"  [S1] Force: {n_tw}/{N_ITER} TOWARD {'PASS' if p1 else 'FAIL'}")

    # S2: Contraction (self/free width ratio < 1)
    ratio = widths_self[-1] / widths_free[-1] if widths_free[-1] > 0 else 1
    p2 = ratio < 1.0; score += p2
    print(f"  [S2] Contraction: ratio={ratio:.4f} {'PASS' if p2 else 'FAIL'}")

    # S3: Norm
    norm_drift = max(abs(nm-1) for nm in norms)
    p3 = norm_drift < 1e-3; score += p3
    print(f"  [S3] Norm: drift={norm_drift:.4e} {'PASS' if p3 else 'FAIL'}")

    # S4: Stability (force doesn't flip sign)
    flips = sum(1 for i in range(len(forces)-1) if (forces[i]>0) != (forces[i+1]>0))
    p4 = flips == 0; score += p4
    print(f"  [S4] Stability: {flips} sign flips {'PASS' if p4 else 'FAIL'}")

    # S5: State-family robustness (self-gravity with different initial states)
    fam_tw = 0
    for label, psi_init in [("gauss", _gauss_state(pos,src)),
                             ("color-0", _color_state(pos,col,src,0)),
                             ("color-1", _color_state(pos,col,src,1))]:
        psi_f = psi_init.copy()
        for _ in range(5):  # 5 self-gravity steps
            rho_f = np.abs(psi_f)**2
            phi_f = _solve_phi(L, n, G_SELF * rho_f)
            H_f = _build_H(pos,col,adj,n,MASS,phi_f)
            psi_f = _cn_step(H_f, n, psi_f)
        F_f = _shell_force(depth,max_d,n,psi_f,phi_f)
        tw = F_f > 0; fam_tw += tw
        print(f"    {label:10s}: F={F_f:+.4e} {'TW' if tw else 'AW'}")
    p5 = fam_tw == 3; score += p5
    print(f"  [S5] Families: {fam_tw}/3 {'PASS' if p5 else 'FAIL'}")

    print(f"\n  SCORE: {score}/5")
    return score


# ============================================================================
# MAIN
# ============================================================================

if __name__ == '__main__':
    t0 = time.time()
    print("="*70)
    print("STAGGERED FERMION SELF-GRAVITY PROBE")
    print("="*70)
    print(f"G_self={G_SELF}, mu2={MU2}, dt={DT}, iterations={N_ITER}")
    print("No external source. Matter density generates its own field.")
    print()

    scores = []
    for builder in [make_random_geometric, make_growing, make_layered_cycle]:
        name, pos, col, adj, n, src = builder()
        s = run_self_gravity(name, pos, col, adj, n, src)
        scores.append(s)

    elapsed = time.time() - t0
    print(f"\n{'='*70}")
    print(f"SUMMARY: scores={scores}")
    print(f"Time: {elapsed:.1f}s")
