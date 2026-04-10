#!/usr/bin/env python3
"""
Two-Field Wave Coupling: Scalar Φ (wave) + Staggered ψ (CN)
==============================================================
Hardens the two-field prototype by replacing relaxation Φ dynamics
with a proper wave equation:

  d²Φ/dt² = -c² (L + mu²) Φ + beta |ψ|²

This is a Klein-Gordon-like equation for the gravitational field,
sourced by the matter density. The field Φ propagates as a wave
(not just relaxation), giving it causal structure.

Leapfrog for Φ (symplectic), CN for ψ (unitary).
Tested on all 3 cycle-bearing bipartite graph families.

Battery:
  W1: Φ responds to matter (grows from zero)
  W2: Force TOWARD across all iterations
  W3: ψ norm conservation
  W4: Φ bounded (no runaway)
  W5: Width response vs free evolution (diagnostic, not a hard gate)
  W6: State-family robustness
"""

from __future__ import annotations
import math, time, random
import numpy as np
from scipy.sparse import lil_matrix, csr_matrix, eye as speye
from scipy.sparse.linalg import spsolve
from collections import deque

MASS=0.30; MU2=0.22; C_PHI=1.0  # Phi wave speed
DT_PSI=0.12; DT_PHI=0.03  # smaller dt for Phi stability
BETA=5.0; N_ITER=30


# ============================================================================
# Graph families (from cycle battery)
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
# Physics
# ============================================================================

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
    par=np.where(col==0,1.,-1.); H.setdiag(mass*par-mass*phi)
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

def _gauss(pos,src):
    center=pos[src]; rel=pos-center
    psi=np.exp(-0.5*(rel[:,0]**2+rel[:,1]**2)/1.15**2).astype(complex)
    return psi/np.linalg.norm(psi)

def _color_state(pos,col,src,target):
    psi=_gauss(pos,src); psi[col!=target]=0
    nm=np.linalg.norm(psi); return psi/nm if nm>0 else psi


# ============================================================================
# Two-field wave coupling
# ============================================================================

def run_wave_coupling(name, pos, col, adj, n, src):
    print(f"\n{'='*70}")
    print(f"WAVE COUPLING: {name} ({n} nodes)")
    print(f"{'='*70}")

    L = _laplacian(pos, adj, n)
    depth = _bfs(adj, src, n)
    max_d = int(np.max(depth[np.isfinite(depth)])) if np.any(np.isfinite(depth)) else 0

    # Operator for Phi: -c^2 * (L + mu^2)
    phi_op = -C_PHI**2 * (L + MU2 * speye(n, format='csr'))

    # Initial states
    psi = _gauss(pos, src)
    phi = np.zeros(n)      # Phi field
    pi_phi = np.zeros(n)   # Phi conjugate momentum (dPhi/dt)
    H_free = _build_H(pos,col,adj,n,MASS,np.zeros(n))
    psi_free = psi.copy()

    forces=[]; widths_c=[]; widths_f=[]; norms=[]; phi_norms=[]; phi_energies=[]
    hard_score = 0

    for it in range(N_ITER):
        rho = np.abs(psi)**2
        source = BETA * rho

        # Leapfrog for Phi wave equation:
        # d²Phi/dt² = phi_op . Phi + source
        # Half-step pi, full-step phi, half-step pi
        force_phi = phi_op.dot(phi) + source
        pi_phi = pi_phi + 0.5 * DT_PHI * force_phi
        phi = phi + DT_PHI * pi_phi
        force_phi = phi_op.dot(phi) + source
        pi_phi = pi_phi + 0.5 * DT_PHI * force_phi

        # CN step for psi with current Phi
        H = _build_H(pos,col,adj,n,MASS,phi)
        psi = _cn_step(H, n, psi)
        psi_free = _cn_step(H_free, n, psi_free)

        F = _shell_force(depth,max_d,n,psi,phi)
        forces.append(F)
        widths_c.append(_width(psi,pos))
        widths_f.append(_width(psi_free,pos))
        norms.append(float(np.linalg.norm(psi)))
        phi_norms.append(float(np.linalg.norm(phi)))
        # Phi field energy: KE + PE
        phi_energies.append(0.5*np.sum(pi_phi**2) + 0.5*float(phi @ (-phi_op).dot(phi)))

        if it < 5 or it % 10 == 0 or it == N_ITER-1:
            print(f"  it={it:2d}: F={F:+.4e}, w={widths_c[-1]/widths_f[-1]:.4f}, "
                  f"|Phi|={phi_norms[-1]:.3e}, E_phi={phi_energies[-1]:.3e}, "
                  f"|psi|={norms[-1]:.10f}")

    # Battery
    # W1: Phi responds
    phi_grew = phi_norms[-1] > 1e-6
    p = phi_grew; hard_score += p
    print(f"\n  [W1] Phi responds: {phi_norms[0]:.3e} -> {phi_norms[-1]:.3e} {'PASS' if p else 'FAIL'}")

    # W2: Force TOWARD
    n_tw = sum(1 for f in forces if f > 0)
    p = n_tw == N_ITER; hard_score += p
    print(f"  [W2] Force: {n_tw}/{N_ITER} TOWARD {'PASS' if p else 'FAIL'}")

    # W3: Norm
    norm_drift = max(abs(nm-1) for nm in norms)
    p = norm_drift < 1e-3; hard_score += p
    print(f"  [W3] Norm: drift={norm_drift:.4e} {'PASS' if p else 'FAIL'}")

    # W4: Phi bounded
    p = phi_norms[-1] < 1e6 and not np.any(np.isnan(phi))
    hard_score += p
    print(f"  [W4] Phi bounded: max={np.max(np.abs(phi)):.3e} {'PASS' if p else 'FAIL'}")

    # W5: Width response (diagnostic only)
    ratio = widths_c[-1] / widths_f[-1] if widths_f[-1] > 0 else 1
    print(f"  [W5] Width ratio: {ratio:.4f} ({'contracted' if ratio<1 else 'expanded'}) [diagnostic]")

    # W6: State families
    fam_tw = 0
    for label, psi_init in [("gauss", _gauss(pos,src)),
                             ("color-0", _color_state(pos,col,src,0)),
                             ("color-1", _color_state(pos,col,src,1))]:
        psi_f = psi_init.copy()
        phi_f = phi.copy(); pi_f = pi_phi.copy()  # use current Phi field
        for _ in range(5):
            H_f = _build_H(pos,col,adj,n,MASS,phi_f)
            psi_f = _cn_step(H_f, n, psi_f)
            rho_f = np.abs(psi_f)**2
            force_f = phi_op.dot(phi_f) + BETA*rho_f
            pi_f += 0.5*DT_PHI*force_f; phi_f += DT_PHI*pi_f
            force_f = phi_op.dot(phi_f) + BETA*rho_f
            pi_f += 0.5*DT_PHI*force_f
        F_f = _shell_force(depth,max_d,n,psi_f,phi_f)
        tw = F_f > 0; fam_tw += tw
        print(f"    {label:10s}: F={F_f:+.4e} {'TW' if tw else 'AW'}")
    p = fam_tw == 3; hard_score += p
    print(f"  [W6] Families: {fam_tw}/3 {'PASS' if p else 'FAIL'}")

    print(f"\n  HARD SCORE: {hard_score}/5 + W5 diagnostic")
    return hard_score, ratio


if __name__ == '__main__':
    t0 = time.time()
    print("="*70)
    print("TWO-FIELD WAVE COUPLING — ALL CYCLE FAMILIES")
    print("="*70)
    print(f"Phi: wave eq d²Phi/dt² = -c²(L+mu²)Phi + beta|psi|²")
    print(f"psi: CN staggered Dirac with V=-m*Phi")
    print(f"c_phi={C_PHI}, beta={BETA}, dt_phi={DT_PHI}, dt_psi={DT_PSI}, N={N_ITER}")
    print()

    scores = []
    ratios = []
    for builder in [make_random_geometric, make_growing, make_layered_cycle]:
        name, pos, col, adj, n, src = builder()
        s, ratio = run_wave_coupling(name, pos, col, adj, n, src)
        scores.append(s)
        ratios.append(ratio)

    ratio_fmt = [float(f"{r:.4f}") for r in ratios]
    print(f"\n{'='*70}")
    print(f"SUMMARY: hard_scores={scores}, width_ratios={ratio_fmt}")
    print(f"Time: {time.time()-t0:.1f}s")
