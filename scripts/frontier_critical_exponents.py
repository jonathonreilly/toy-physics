#!/usr/bin/env python3
"""
Critical Exponents vs Graph Topology — Retained Probe
=======================================================
Does the self-gravity phase transition have topology-dependent exponents?
If β differs across graph families, that's a new universality class.

Tests: random geometric, growing, layered cycle, causal DAG.
"""

from __future__ import annotations
import math, time, random
import numpy as np
from scipy.sparse import lil_matrix, csr_matrix, eye as speye
from scipy.sparse.linalg import spsolve
from scipy.optimize import curve_fit
from collections import deque

MASS=0.3; MU2=0.22; DT=0.12; N_STEPS=30


def _ae(adj,a,b): adj.setdefault(a,set()).add(b); adj.setdefault(b,set()).add(a)

def build_rg(seed,side):
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
    return "random_geometric", pos, col, {k:list(v) for k,v in adj.items()}

def build_growing(seed,n_target):
    rng=random.Random(seed); coords=[(0.,0.),(1.,0.)]; colors=[0,1]; adj={0:{1},1:{0}}; cur=2
    while cur<n_target:
        px=rng.uniform(-3,3); py=rng.uniform(-3,3); nc=cur%2
        coords.append((px,py)); colors.append(nc)
        opp=[i for i in range(cur) if colors[i]!=nc]
        if opp:
            ds=[(math.hypot(px-coords[i][0],py-coords[i][1]),i) for i in opp]; ds.sort()
            for _,j in ds[:min(4,len(ds))]: _ae(adj,cur,j)
        cur+=1
    return "growing", np.array(coords), np.array(colors,dtype=int), {k:list(v) for k,v in adj.items()}

def build_layered(seed,layers,width):
    rng=random.Random(seed); coords=[]; colors=[]; layer_nodes=[]; idx=0
    for layer in range(layers):
        count=max(2,width); this_layer=[]
        for k in range(count):
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

def build_dag(seed,layers,width):
    rng=random.Random(seed); coords=[]; colors=[]; layer_nodes=[]; idx=0
    for layer in range(layers):
        count=1 if layer==0 else width
        this_layer=[]
        for k in range(count):
            coords.append((float(layer),float(k)+0.1*(rng.random()-0.5)))
            colors.append(layer%2); this_layer.append(idx); idx+=1
        layer_nodes.append(this_layer)
    pos=np.array(coords); col=np.array(colors,dtype=int); n=len(pos)
    adj={i:set() for i in range(n)}
    for layer in range(layers-1):
        curr=layer_nodes[layer]; nxt=layer_nodes[layer+1]
        for i_pos,i in enumerate(curr):
            j=nxt[(i_pos+layer)%len(nxt)]; adj[i].add(j); adj[j].add(i)
    return "causal_dag", pos, col, {k:list(v) for k,v in adj.items()}


def lap(pos,adj,n):
    L=lil_matrix((n,n),dtype=float)
    for i,nbs in adj.items():
        for j in nbs:
            if i>=j: continue
            d=math.hypot(pos[j,0]-pos[i,0],pos[j,1]-pos[i,1])
            w=1./max(d,0.5); L[i,j]-=w; L[j,i]-=w; L[i,i]+=w; L[j,j]+=w
    return L.tocsr()

def build_H(pos,col,adj,n,mass,V=None):
    H=lil_matrix((n,n),dtype=complex)
    par=np.where(col==0,1.,-1.); diag=mass*par
    if V is not None: diag=diag+V
    H.setdiag(diag)
    for i,nbs in adj.items():
        for j in nbs:
            if i>=j: continue
            d=math.hypot(pos[j,0]-pos[i,0],pos[j,1]-pos[i,1])
            w=1./max(d,0.5); H[i,j]+=-0.5j*w; H[j,i]+=0.5j*w
    return H.tocsr()

def cn(H,n,psi):
    ap=(speye(n,format='csc')+1j*H*DT/2).tocsc(); am=speye(n,format='csr')-1j*H*DT/2
    return spsolve(ap,am.dot(psi))

def width(psi,pos):
    rho=np.abs(psi)**2; rho/=np.sum(rho)
    cx=np.sum(rho*pos[:,0]); cy=np.sum(rho*pos[:,1])
    return np.sqrt(np.sum(rho*((pos[:,0]-cx)**2+(pos[:,1]-cy)**2)))


def measure_transition(name, pos, col, adj):
    n=len(pos); src=n//2; center=pos[src]
    L=lap(pos,adj,n); H_free=build_H(pos,col,adj,n,MASS)
    psi0=np.exp(-0.5*((pos[:,0]-center[0])**2+(pos[:,1]-center[1])**2)/1.15**2).astype(complex)
    psi0/=np.linalg.norm(psi0)

    G_vals=np.concatenate([np.linspace(1,10,10),np.linspace(10,50,20),np.linspace(50,200,10)])
    results=[]
    for G_self in G_vals:
        psi_s=psi0.copy(); psi_f=psi0.copy()
        for _ in range(N_STEPS):
            rho=np.abs(psi_s)**2
            phi=spsolve((L+MU2*speye(n,format='csr')).tocsc(),G_self*rho)
            psi_s=cn(build_H(pos,col,adj,n,MASS,phi),n,psi_s)
            psi_f=cn(H_free,n,psi_f)
        results.append((G_self, width(psi_s,pos)/width(psi_f,pos)))

    G_arr=np.array([r[0] for r in results]); phi_arr=np.array([r[1] for r in results])
    dphi=np.gradient(phi_arr,G_arr)
    valid=~np.isnan(dphi) & ~np.isinf(dphi)
    if np.any(valid):
        G_crit=G_arr[valid][np.argmin(dphi[valid])]
    else:
        G_crit=10.0

    # Fit
    mask=(G_arr>G_crit)&(G_arr<5*G_crit)
    beta_fit=0.5; r2=0; A_fit=0
    if np.sum(mask)>=5:
        G_above=G_arr[mask]; order=np.clip(1-phi_arr[mask],1e-10,None)
        try:
            def pl(G,A,beta): return A*(G-G_crit)**beta
            popt,_=curve_fit(pl,G_above,order,p0=[0.01,0.5],maxfev=5000)
            A_fit,beta_fit=popt
            pred=pl(G_above,*popt); ss_res=np.sum((order-pred)**2); ss_tot=np.sum((order-np.mean(order))**2)
            r2=1-ss_res/ss_tot if ss_tot>0 else 0
        except: pass

    phi_sat=phi_arr[-1]
    return G_crit, beta_fit, r2, phi_sat, n


if __name__=='__main__':
    t0=time.time()
    print("="*70)
    print("CRITICAL EXPONENTS vs GRAPH TOPOLOGY")
    print("="*70)
    print()

    families=[
        build_rg(42,8),
        build_rg(42,10),
        build_growing(42,64),
        build_layered(42,8,8),
        build_dag(42,10,6),
        build_dag(42,8,8),
    ]

    print(f"{'Family':<25s} {'n':>5s} {'G_crit':>8s} {'beta':>8s} {'R^2':>8s} {'phi_sat':>8s}")
    print("-"*70)
    for name,pos,col,adj in families:
        G_c,beta,r2,phi_s,n=measure_transition(name,pos,col,adj)
        print(f"{name:<25s} {n:5d} {G_c:8.1f} {beta:8.4f} {r2:8.4f} {phi_s:8.4f}")

    print(f"\nTime: {time.time()-t0:.1f}s")
    print("\nIf beta varies across families -> new universality class.")
    print("If beta ~ 0.5 everywhere -> mean-field (expected for long-range Poisson).")
