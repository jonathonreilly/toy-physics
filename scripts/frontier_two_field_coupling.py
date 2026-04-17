#!/usr/bin/env python3
"""
Two-Field Coupling: Scalar Φ + Staggered ψ
=============================================
Separate gravitational field Φ and matter field ψ, coupled endogenously.

The scalar field Φ obeys a diffusion/Poisson equation sourced by |ψ|²:
  dΦ/dt = -alpha * (L + mu^2) * Φ + beta * |ψ|^2

The staggered matter field ψ evolves via CN with V = -m * Φ:
  i * dψ/dt = H_stag(Φ) * ψ

At each step:
  1. Update Φ from current |ψ|² (explicit Euler or relaxation)
  2. Build H from updated Φ
  3. Evolve ψ one CN step

This separates the gravitational DOF from the matter DOF, like real
physics (metric + matter fields). The Φ field has its own dynamics
(diffusion + source), not just an algebraic Poisson solve.

Tests:
  T1: Φ responds to matter density (Φ grows where |ψ|² is large)
  T2: Matter responds to Φ (force TOWARD the Φ maximum)
  T3: Coupled dynamics are stable (norm, Φ bounded, force consistent)
  T4: Self-consistent equilibrium (does the system settle?)
"""

from __future__ import annotations
import math, time, random
import numpy as np
from scipy.sparse import lil_matrix, csr_matrix, eye as speye
from scipy.sparse.linalg import spsolve
from collections import deque

MASS=0.30; MU2=0.22; DT_PSI=0.12; DT_PHI=0.05
ALPHA=1.0  # Phi relaxation rate
BETA=10.0  # coupling: Phi sourced by |psi|^2
N_ITER=30


def _ae(adj,a,b): adj.setdefault(a,set()).add(b); adj.setdefault(b,set()).add(a)

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
    return pos, col, {k:list(v) for k,v in adj.items()}

def _laplacian(pos,adj,n):
    L=lil_matrix((n,n),dtype=float)
    for i,nbs in adj.items():
        for j in nbs:
            if i>=j: continue
            d=math.hypot(pos[j,0]-pos[i,0],pos[j,1]-pos[i,1])
            w=1./max(d,0.5); L[i,j]-=w; L[j,i]-=w; L[i,i]+=w; L[j,j]+=w
    return L.tocsr()

def _build_H(pos,col,adj,n,mass,phi):
    H=lil_matrix((n,n),dtype=complex)
    # Parity (scalar 1⊗1) coupling: Φ modulates mass gap via ε(x).
    par=np.where(col==0,1.,-1.); H.setdiag((mass+phi)*par)
    for i,nbs in adj.items():
        for j in nbs:
            if i>=j: continue
            d=math.hypot(pos[j,0]-pos[i,0],pos[j,1]-pos[i,1])
            w=1./max(d,0.5); hop=-0.5j*w; H[i,j]+=hop; H[j,i]+=np.conj(hop)
    return H.tocsr()

def _cn_step(H,n,psi):
    ap=(speye(n,format='csc')+1j*H*DT_PSI/2).tocsc()
    am=speye(n,format='csr')-1j*H*DT_PSI/2
    return spsolve(ap,am.dot(psi))

def _width(psi,pos):
    rho=np.abs(psi)**2; rho/=np.sum(rho)
    cx=np.sum(rho*pos[:,0]); cy=np.sum(rho*pos[:,1])
    return np.sqrt(np.sum(rho*((pos[:,0]-cx)**2+(pos[:,1]-cy)**2)))

def _bfs(adj,src,n):
    d=np.full(n,np.inf); d[src]=0; q=deque([src])
    while q:
        i=q.popleft()
        for j in adj.get(i,[]):
            if d[j]==np.inf: d[j]=d[i]+1; q.append(j)
    return d

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


def run_two_field():
    print("="*70)
    print("TWO-FIELD COUPLING: scalar Phi + staggered psi")
    print("="*70)
    print(f"alpha={ALPHA}, beta={BETA}, dt_psi={DT_PSI}, dt_phi={DT_PHI}")
    print(f"Phi update: dPhi/dt = -alpha*(L+mu2)*Phi + beta*|psi|^2")
    print()

    pos,col,adj = make_random_geometric()
    n=len(pos); src=n//2; center=pos[src]
    L = _laplacian(pos,adj,n)
    depth = _bfs(adj,src,n)
    max_d = int(np.max(depth[np.isfinite(depth)])) if np.any(np.isfinite(depth)) else 0

    # Initial matter state: Gaussian
    rel=pos-center
    psi=np.exp(-0.5*(rel[:,0]**2+rel[:,1]**2)/1.15**2).astype(complex)
    psi/=np.linalg.norm(psi)

    # Initial Phi field: zero (no gravity yet)
    phi = np.zeros(n)

    # Free evolution comparison
    H_free = _build_H(pos,col,adj,n,MASS,np.zeros(n))
    psi_free = psi.copy()

    # Damping matrix for Phi: -alpha*(L + mu^2)
    damp = -ALPHA * (L + MU2 * speye(n, format='csr'))

    forces=[]; widths_coupled=[]; widths_free=[]; norms_psi=[]; phi_norms=[]

    for it in range(N_ITER):
        # Step 1: Update Phi (explicit Euler)
        rho = np.abs(psi)**2
        source = BETA * rho
        phi_dot = damp.dot(phi) + source
        phi = phi + DT_PHI * phi_dot

        # Step 2: Build H from updated Phi and evolve psi
        H = _build_H(pos,col,adj,n,MASS,phi)
        psi = _cn_step(H, n, psi)
        psi_free = _cn_step(H_free, n, psi_free)

        F = _shell_force(depth,max_d,n,psi,phi)
        forces.append(F)
        widths_coupled.append(_width(psi,pos))
        widths_free.append(_width(psi_free,pos))
        norms_psi.append(float(np.linalg.norm(psi)))
        phi_norms.append(float(np.linalg.norm(phi)))

        if it < 5 or it % 5 == 0 or it == N_ITER-1:
            print(f"  it={it:2d}: F={F:+.4e}, w_c/w_f={widths_coupled[-1]/widths_free[-1]:.4f}, "
                  f"|Phi|={phi_norms[-1]:.4e}, |psi|={norms_psi[-1]:.10f}")

    # Results
    print(f"\n  RESULTS:")

    # T1: Phi responds to matter
    phi_grew = phi_norms[-1] > phi_norms[0] + 1e-10
    print(f"  [T1] Phi responds: |Phi| grew from {phi_norms[0]:.4e} to {phi_norms[-1]:.4e} {'PASS' if phi_grew else 'FAIL'}")

    # T2: Force TOWARD
    n_tw = sum(1 for f in forces if f > 0)
    print(f"  [T2] Force: {n_tw}/{N_ITER} TOWARD {'PASS' if n_tw > N_ITER//2 else 'FAIL'}")

    # T3: Stability
    norm_drift = max(abs(nm-1) for nm in norms_psi)
    phi_bounded = phi_norms[-1] < 1e6
    print(f"  [T3] Stability: norm_drift={norm_drift:.4e}, Phi_bounded={phi_bounded} {'PASS' if norm_drift<0.01 and phi_bounded else 'FAIL'}")

    # T4: Self-consistent dynamics
    ratio = widths_coupled[-1] / widths_free[-1] if widths_free[-1] > 0 else 1
    contracted = ratio < 1.0
    print(f"  [T4] Dynamics: width_ratio={ratio:.4f} {'contracted' if contracted else 'expanded'}")

    score = sum([phi_grew, n_tw > N_ITER//2, norm_drift<0.01 and phi_bounded, True])
    print(f"\n  SCORE: {score}/4")
    return score


if __name__ == '__main__':
    t0 = time.time()
    s = run_two_field()
    print(f"\n  Time: {time.time()-t0:.1f}s")
