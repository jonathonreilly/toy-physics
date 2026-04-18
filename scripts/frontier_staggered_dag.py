#!/usr/bin/env python3
"""
Staggered Fermion on Layered DAG-Derived Family — Bounded Control
=================================================================
Tests the staggered architecture on a layered acyclic template derived from a
causal DAG construction.

Important scope boundary:
  - layers still provide a causal ordering / depth coordinate
  - color still comes from layer parity
  - the Hamiltonian uses a symmetrized Hermitian adjacency, not a genuinely
    directed operator
  - so this is a layered-DAG-derived compatibility control, not a proof of
    true directed-Hamiltonian DAG transport

Battery:
  D1: Force TOWARD (gravity)
  D2: N-stability (force stays TOWARD)
  D3: Norm conservation
  D4: Born (linearity)
  D5: Forward-depth bias (probability moves toward later layers)
  D6: State-family robustness
"""

from __future__ import annotations
import math, time, random
import numpy as np
from scipy.sparse import lil_matrix, csr_matrix, eye as speye
from scipy.sparse.linalg import spsolve
from collections import deque

MASS=0.30; DT=0.12; NS=10; G=50.0; S=5e-4


def build_dag(n_layers=8, width=5, seed=42):
    rng=random.Random(seed); coords=[]; colors=[]; layer_nodes=[]; idx=0
    for layer in range(n_layers):
        count = 1 if layer==0 else width
        this_layer = []
        for k in range(count):
            coords.append((float(layer), float(k)+0.1*(rng.random()-0.5)))
            colors.append(layer%2); this_layer.append(idx); idx+=1
        layer_nodes.append(this_layer)
    pos=np.array(coords); col=np.array(colors,dtype=int); n=len(pos)
    adj={i:set() for i in range(n)}
    for layer in range(n_layers-1):
        curr=layer_nodes[layer]; nxt=layer_nodes[layer+1]
        for i_pos,i in enumerate(curr):
            j1=nxt[i_pos%len(nxt)]; adj[i].add(j1); adj[j1].add(i)
            j2=nxt[(i_pos+1)%len(nxt)]
            if j2!=j1: adj[i].add(j2); adj[j2].add(i)
    adj_l={k:list(v) for k,v in adj.items()}
    src=layer_nodes[0][0]; depth=np.array([pos[i,0] for i in range(n)])
    return pos, col, adj_l, n, src, depth, layer_nodes


def _build_H(pos,col,adj,n,mass,V=None):
    H=lil_matrix((n,n),dtype=complex)
    par=np.where(col==0,1.,-1.); diag=mass*par
    if V is not None: diag=diag+V*par
    H.setdiag(diag)
    for i,nbs in adj.items():
        for j in nbs:
            if i>=j: continue
            d=math.hypot(pos[j,0]-pos[i,0],pos[j,1]-pos[i,1])
            w=1./max(d,0.5); H[i,j]+=-0.5j*w; H[j,i]+=0.5j*w
    return H.tocsr()


def _cn(H,n,psi,ns):
    ap=(speye(n,format='csc')+1j*H*DT/2).tocsc(); am=speye(n,format='csr')-1j*H*DT/2
    p=psi.copy()
    for _ in range(ns): p=spsolve(ap,am.dot(p))
    return p


def _gauss(pos,src):
    center=pos[src]; rel=pos-center
    psi=np.exp(-0.5*(rel[:,0]**2+rel[:,1]**2)/1.15**2).astype(complex)
    return psi/np.linalg.norm(psi)


def _shell_force(depth,max_d,n,psi,phi):
    if max_d<=0: return 0.
    rho=np.abs(psi)**2; ps=np.zeros(max_d+1); rs=np.zeros(max_d+1); cnt=np.zeros(max_d+1)
    for i in range(n):
        d_=int(depth[i])
        if 0<=d_<=max_d: ps[d_]+=phi[i]; rs[d_]+=rho[i]; cnt[d_]+=1
    for d_ in range(max_d+1):
        if cnt[d_]>0: ps[d_]/=cnt[d_]; rs[d_]/=cnt[d_]
    grad=np.zeros(max_d+1)
    for d_ in range(max_d+1):
        if d_==0: grad[d_]=ps[0]-ps[min(1,max_d)]
        elif d_==max_d: grad[d_]=ps[d_-1]-ps[d_]
        else: grad[d_]=0.5*(ps[d_-1]-ps[d_+1])
    return float(np.sum(rs*grad))


def run_dag_battery(n_layers=8, width=5, seed=42):
    pos,col,adj,n,src,depth,layers = build_dag(n_layers,width,seed)
    max_d = int(np.max(depth))
    mass_node = layers[-1][len(layers[-1])//2]

    V = np.zeros(n)
    for i in range(n):
        r = math.hypot(pos[i,0]-pos[mass_node,0], pos[i,1]-pos[mass_node,1])
        V[i] = -MASS*G*S/(r+0.1)

    H_flat = _build_H(pos,col,adj,n,MASS)
    H_grav = _build_H(pos,col,adj,n,MASS,V)
    psi0 = _gauss(pos,src)

    print(f"{'='*70}")
    print(f"LAYERED DAG-DERIVED CONTROL ({n} nodes, {n_layers} layers, width={width})")
    print(f"{'='*70}")
    print(f"  Bipartite: {all(col[i]!=col[j] for i,nbs in adj.items() for j in nbs)}")

    score = 0

    # D1: Force TOWARD
    pg = _cn(H_grav,n,psi0,NS)
    F = _shell_force(depth,max_d,n,pg,V)
    p=F>0; score+=p
    print(f"  [D1] Force: {F:+.4e} {'TOWARD' if p else 'AWAY'} {'PASS' if p else 'FAIL'}")

    # D2: N-stability
    n_tw=0
    for ns_ in range(2,16):
        pg_=_cn(H_grav,n,psi0,ns_)
        if _shell_force(depth,max_d,n,pg_,V)>0: n_tw+=1
    p=n_tw>=12; score+=p
    print(f"  [D2] N-stability: {n_tw}/14 TOWARD {'PASS' if p else 'FAIL'}")

    # D3: Norm
    norm_err=abs(np.linalg.norm(pg)-1)
    p=norm_err<1e-10; score+=p
    print(f"  [D3] Norm: {norm_err:.4e} {'PASS' if p else 'FAIL'}")

    # D4: Born
    psi_a=psi0; psi_b=np.roll(psi0,n//3); psi_b/=np.linalg.norm(psi_b)
    psi_sum=(psi_a+psi_b)/np.sqrt(2)
    pa=_cn(H_flat,n,psi_a,NS); pb=_cn(H_flat,n,psi_b,NS); ps=_cn(H_flat,n,psi_sum,NS)
    lin=np.linalg.norm(ps-(pa+pb)/np.sqrt(2))/np.linalg.norm(ps)
    p=lin<1e-6; score+=p
    print(f"  [D4] Born: {lin:.4e} {'PASS' if p else 'FAIL'}")

    # D5: Forward-depth bias
    psi_pt=np.zeros(n,dtype=complex); psi_pt[src]=1.0
    psi_c=_cn(H_flat,n,psi_pt,5)
    rho_c=np.abs(psi_c)**2
    p_by_layer=np.zeros(max_d+1)
    for i in range(n): p_by_layer[int(depth[i])]+=rho_c[i]
    forward_frac=np.sum(p_by_layer[1:])/np.sum(p_by_layer) if np.sum(p_by_layer)>0 else 0
    p=forward_frac>0.01; score+=p
    print(f"  [D5] Forward-depth: forward_frac={forward_frac:.4f} {'PASS' if p else 'FAIL'}")

    # D6: State families
    psi_even=psi0.copy(); psi_even[col==1]=0; psi_even/=np.linalg.norm(psi_even)
    psi_odd=psi0.copy(); psi_odd[col==0]=0; psi_odd/=np.linalg.norm(psi_odd)
    fam_tw=0
    for label,psi_f in [("gauss",psi0),("even",psi_even),("odd",psi_odd)]:
        pg_f=_cn(H_grav,n,psi_f,NS)
        F_f=_shell_force(depth,max_d,n,pg_f,V)
        tw=F_f>0; fam_tw+=tw
        print(f"    {label:6s}: F={F_f:+.4e} {'TW' if tw else 'AW'}")
    p=fam_tw==3; score+=p
    print(f"  [D6] Families: {fam_tw}/3 {'PASS' if p else 'FAIL'}")

    print(f"\n  SCORE: {score}/6")
    return score


if __name__ == '__main__':
    t0=time.time()
    print("="*70)
    print("STAGGERED FERMION ON LAYERED DAG-DERIVED FAMILY")
    print("="*70)
    print("Layered acyclic template with causal ordering and symmetrized transport.")
    print()

    scores=[]
    for layers,width in [(8,5),(12,4),(6,8)]:
        s=run_dag_battery(layers,width,seed=42)
        scores.append(s)
        print()

    print(f"SUMMARY: scores={scores}")
    print(f"Time: {time.time()-t0:.1f}s")
