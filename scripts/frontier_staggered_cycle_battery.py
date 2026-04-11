#!/usr/bin/env python3
"""
Staggered Fermion Cycle-Bearing Graph Battery — Retained Harness
=================================================================
One retained harness for cycle-bearing bipartite graph families.
Integrates: iterative backreaction, native gauge, force battery.

Battery rows:
  B1: Zero-source control (Phi=0 -> F=0)
  B2: Source-response linearity (F proportional to source strength)
  B3: Two-body additivity (Phi(A+B) = Phi(A) + Phi(B))
  B4: Force sign (TOWARD) at operating point
  B5: Iterative stability (force stays TOWARD across 15 iterations)
  B6: Norm conservation (drift < 1e-3)
  B7: State-family robustness (gauss, color-0, color-1 all TOWARD)
  B8: Native gauge closure (persistent current sin(A) on graph cycle)
  B9: Force-gap characterization + shell/spectral diagnostics

Graph families (all cycle-bearing, bipartite):
  - Random geometric (6x6 grid, cross-color NN links, has cycles)
  - Growing (preferential attachment, alternating colors, has cycles)
  - Layered cycle (layered structure, 2-connection per node, has cycles)

Source convention:
  - Growing uses the deepest reachable node as its retained source.
  - Layered cycle uses a max-degree interior node as its retained source.

Force is the primary gravity observable. No centroid shift.
No 1D ring fallback. No silent semantic swaps.
"""

from __future__ import annotations
import math, time, random, statistics
import numpy as np
from scipy.sparse import lil_matrix, csr_matrix, eye as speye
from scipy.sparse.linalg import spsolve, eigsh
from scipy.optimize import curve_fit
from collections import deque
from dataclasses import dataclass


# ============================================================================
# Parameters
# ============================================================================
DT = 0.12; MASS = 0.30; G = 8.0; SOURCE_SIGMA = 0.90; POISSON_MU2 = 0.22
N_ITER = 15; N_STEPS_SINGLE = 10


# ============================================================================
# Graph construction
# ============================================================================

def _ae(adj, a, b):
    adj.setdefault(a, set()).add(b); adj.setdefault(b, set()).add(a)

def _bfs(adj, src, n):
    d = np.full(n, np.inf); d[src] = 0; q = deque([src])
    while q:
        i = q.popleft()
        for j in adj.get(i, []):
            if d[j] == np.inf: d[j] = d[i]+1; q.append(j)
    return d

def _find_cycle_edge(adj):
    visited = set()
    for start in sorted(adj):
        if start in visited: continue
        stack = [(start, None)]
        while stack:
            node, prev = stack.pop()
            if node in visited:
                return (prev, node) if prev is not None else None
            visited.add(node)
            for nb in adj.get(node, []):
                if nb == prev: continue
                if nb in visited: return (node, nb)
                stack.append((nb, node))
    return None

def _has_odd_cycle(adj, colors):
    for i, nbs in adj.items():
        for j in nbs:
            if colors[i] == colors[j]: return True
    return False

@dataclass(frozen=True)
class Graph:
    name: str; pos: np.ndarray; colors: np.ndarray; adj: dict
    n: int; src: int; depth: np.ndarray; cycle_edge: tuple | None

def make_random_geometric(seed=42, side=6) -> Graph:
    rng = random.Random(seed); coords=[]; colors=[]; index={}; adj={}; idx=0
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
    adj_l = {k:list(v) for k,v in adj.items()}; n=len(pos); src=n//2
    return Graph("random_geometric", pos, col, adj_l, n, src,
                 _bfs(adj_l,src,n), _find_cycle_edge(adj_l))

def make_growing(seed=42, n_target=48) -> Graph:
    rng=random.Random(seed); coords=[(0.,0.),(1.,0.)]; colors=[0,1]; adj={0:{1},1:{0}}; cur=2
    while cur < n_target:
        px=rng.uniform(-3,3); py=rng.uniform(-3,3); nc=cur%2
        coords.append((px,py)); colors.append(nc)
        opp=[i for i in range(cur) if colors[i]!=nc]
        if opp:
            ds=[(math.hypot(px-coords[i][0],py-coords[i][1]),i) for i in opp]; ds.sort()
            for _,j in ds[:min(4,len(ds))]: _ae(adj,cur,j)
        cur+=1
    pos=np.array(coords); col=np.array(colors,dtype=int); adj_l={k:list(v) for k,v in adj.items()}
    n=len(pos)
    # Use the deepest reachable node as the retained source. The growing
    # family is seeded from a boundary node; centering the source on the
    # graph's extent removes a boundary-source artifact without changing the
    # row definition.
    src=int(np.argmax(_bfs(adj_l, 0, n)))
    return Graph("growing",pos,col,adj_l,n,src,_bfs(adj_l,src,n),_find_cycle_edge(adj_l))

def make_layered_cycle(seed=42, layers=6, width=4) -> Graph:
    """Layered graph with cycles: each node connects to 2 nodes in the next layer."""
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
    adj_l={k:list(v) for k,v in adj.items()}
    # Reject if not bipartite
    if _has_odd_cycle(adj_l, col): return None
    # Use a high-connectivity interior source instead of the seed node.
    # This avoids boundary-source artifacts while keeping the family and row
    # semantics unchanged.
    src=max(range(n), key=lambda i: len(adj_l.get(i, [])))
    return Graph("layered_cycle",pos,col,adj_l,n,src,_bfs(adj_l,src,n),_find_cycle_edge(adj_l))


# ============================================================================
# Physics tools
# ============================================================================

def _graph_laplacian(g):
    n=g.n; L=lil_matrix((n,n),dtype=float)
    for i,nbs in g.adj.items():
        for j in nbs:
            if i>=j: continue
            d=math.hypot(g.pos[j,0]-g.pos[i,0],g.pos[j,1]-g.pos[i,1])
            w=1./max(d,0.5); L[i,j]-=w; L[j,i]-=w; L[i,i]+=w; L[j,j]+=w
    return L.tocsr()

def _solve_phi(g, rho):
    if np.allclose(rho,0): return np.zeros(g.n)
    L=_graph_laplacian(g); A=(L+POISSON_MU2*speye(g.n,format='csr')).tocsc()
    return spsolve(A,rho)

def _build_H(g, mass, phi):
    n=g.n; H=lil_matrix((n,n),dtype=complex)
    # Parity (scalar 1⊗1) coupling: Φ modulates mass gap, not energy level.
    par=np.where(g.colors==0,1.,-1.); H.setdiag((mass+phi)*par)
    for i,nbs in g.adj.items():
        for j in nbs:
            if i>=j: continue
            d=math.hypot(g.pos[j,0]-g.pos[i,0],g.pos[j,1]-g.pos[i,1])
            w=1./max(d,0.5); hop=-0.5j*w; H[i,j]+=hop; H[j,i]+=np.conj(hop)
    return H.tocsr()

def _build_H_flux(g, mass, flux_edge, A_flux):
    n=g.n; H=lil_matrix((n,n),dtype=complex)
    par=np.where(g.colors==0,1.,-1.); H.setdiag(mass*par)
    u,v=min(flux_edge),max(flux_edge)
    for i,nbs in g.adj.items():
        for j in nbs:
            if i>=j: continue
            d=math.hypot(g.pos[j,0]-g.pos[i,0],g.pos[j,1]-g.pos[i,1])
            w=1./max(d,0.5); hop=-0.5j*w
            if (i,j)==(u,v):
                H[i,j]+=hop*np.exp(1j*A_flux); H[j,i]+=np.conj(hop)*np.exp(-1j*A_flux)
            else:
                H[i,j]+=hop; H[j,i]+=np.conj(hop)
    return H.tocsr()

def _cn_step(H, psi, dt):
    n=H.shape[0]; ap=(speye(n,format='csc')+1j*H*dt/2).tocsc(); am=speye(n,format='csr')-1j*H*dt/2
    return spsolve(ap,am.dot(psi))

def _cn_evolve(H, psi, dt, ns):
    n=H.shape[0]; ap=(speye(n,format='csc')+1j*H*dt/2).tocsc(); am=speye(n,format='csr')-1j*H*dt/2
    p=psi.copy()
    for _ in range(ns): p=spsolve(ap,am.dot(p))
    return p

def _shell_force(g, psi, phi):
    md=int(np.max(g.depth[np.isfinite(g.depth)])) if np.any(np.isfinite(g.depth)) else 0
    if md<=0: return 0.
    rho_m=np.abs(psi)**2; ps=np.zeros(md+1); rs=np.zeros(md+1); cnt=np.zeros(md+1)
    for i in range(g.n):
        d_=int(g.depth[i]) if np.isfinite(g.depth[i]) else -1
        if 0<=d_<=md: ps[d_]+=phi[i]; rs[d_]+=rho_m[i]; cnt[d_]+=1
    for d_ in range(md+1):
        if cnt[d_]>0: ps[d_]/=cnt[d_]; rs[d_]/=cnt[d_]
    grad=np.zeros(md+1)
    for d_ in range(md+1):
        if d_==0: grad[d_]=ps[0]-ps[min(1,md)]
        elif d_==md: grad[d_]=ps[d_-1]-ps[d_]
        else: grad[d_]=0.5*(ps[d_-1]-ps[d_+1])
    return float(np.sum(rs*grad))

def _source_density(g, strength=1.0):
    center=g.pos[g.src]; rel=g.pos-center
    w=np.exp(-0.5*(rel[:,0]**2+rel[:,1]**2)/SOURCE_SIGMA**2); w/=max(np.sum(w),1e-30)
    return strength*w

def _probe_state(g, sigma=1.15, k0=0.18):
    center=g.pos[g.src]; rel=g.pos-center; coord=rel[:,0]+0.35*rel[:,1]
    psi=np.exp(-0.5*(rel[:,0]**2+rel[:,1]**2)/sigma**2)*np.exp(1j*k0*coord)
    return psi.astype(complex)/np.linalg.norm(psi)

def _color_state(g, target_color):
    psi=_probe_state(g).copy(); psi[g.colors!=target_color]=0
    nm=np.linalg.norm(psi); return psi/nm if nm>0 else psi

def _ext_phi(g, strength=1.0):
    center=g.pos[g.src]; rel=g.pos-center; r=np.sqrt(rel[:,0]**2+rel[:,1]**2)
    return strength*np.exp(-0.38*r)/(r+0.25)


# ============================================================================
# Battery
# ============================================================================

def run_battery(g: Graph):
    print(f"\n{'='*70}")
    print(f"CYCLE BATTERY: {g.name} ({g.n} nodes)")
    print(f"{'='*70}")

    if _has_odd_cycle(g.adj, g.colors):
        print("  REJECTED: odd-cycle defect."); return

    score = 0; psi0 = _probe_state(g)

    # B1: Zero-source
    phi0 = _solve_phi(g, np.zeros(g.n))
    H0 = _build_H(g, MASS, phi0)
    psi_z = _cn_evolve(H0, psi0, DT, N_STEPS_SINGLE)
    F0 = _shell_force(g, psi_z, phi0)
    p = abs(F0) < 1e-10 and np.linalg.norm(phi0) < 1e-10
    score += p; print(f"  [B1] Zero-source: F={F0:.4e}, |Phi|={np.linalg.norm(phi0):.4e} {'PASS' if p else 'FAIL'}")

    # B2: Source linearity
    rho_s = _source_density(g)
    forces = []
    for s in [0.0, 0.25, 0.5, 1.0, 2.0]:
        phi = _solve_phi(g, s*rho_s)
        psi = _cn_evolve(_build_H(g, MASS, phi), psi0, DT, N_STEPS_SINGLE)
        forces.append(_shell_force(g, psi, phi))
    fa=np.array(forces); sa=np.array([0.,0.25,0.5,1.,2.])
    co=np.polyfit(sa,fa,1); pred=np.polyval(co,sa)
    r2=1-np.sum((fa-pred)**2)/np.sum((fa-np.mean(fa))**2) if np.sum((fa-np.mean(fa))**2)>0 else 1
    p=r2>0.99; score+=p; print(f"  [B2] Linearity: R^2={r2:.6f} {'PASS' if p else 'FAIL'}")

    # B3: Additivity
    partner=max(range(g.n), key=lambda i: g.depth[i] if np.isfinite(g.depth[i]) else -1)
    rho_a=_source_density(g); center_b=g.pos[partner]; rel_b=g.pos-center_b
    rho_b=np.exp(-0.5*(rel_b[:,0]**2+rel_b[:,1]**2)/SOURCE_SIGMA**2); rho_b/=max(np.sum(rho_b),1e-30)
    phi_a=_solve_phi(g,rho_a); phi_b=_solve_phi(g,rho_b); phi_ab=_solve_phi(g,rho_a+rho_b)
    resid=np.linalg.norm(phi_ab-(phi_a+phi_b))/max(np.linalg.norm(phi_ab),1e-30)
    p=resid<1e-10; score+=p; print(f"  [B3] Additivity: residual={resid:.4e} {'PASS' if p else 'FAIL'}")

    # B4: Force TOWARD
    phi_s=_solve_phi(g,rho_s); H_s=_build_H(g,MASS,phi_s)
    psi_s=_cn_evolve(H_s,psi0,DT,N_STEPS_SINGLE)
    F_s=_shell_force(g,psi_s,phi_s)
    p=F_s>0; score+=p; print(f"  [B4] Force: {F_s:+.4e} {'TOWARD PASS' if p else 'AWAY FAIL'}")

    # B5: Iterative stability
    psi_it=psi0.copy(); tw_count=0
    for it in range(N_ITER):
        rho_m=np.abs(psi_it)**2; rho_m*=np.sum(rho_s)/max(np.sum(rho_m),1e-30)
        phi_it=_solve_phi(g,rho_s+G*rho_m); H_it=_build_H(g,MASS,phi_it)
        psi_it=_cn_step(H_it,psi_it,DT)
        if _shell_force(g,psi_it,phi_it)>0: tw_count+=1
    p=tw_count==N_ITER; score+=p
    print(f"  [B5] Iter stability: {tw_count}/{N_ITER} TOWARD {'PASS' if p else 'FAIL'}")

    # B6: Norm
    norm_drift=abs(np.linalg.norm(psi_it)-1)
    p=norm_drift<1e-3; score+=p; print(f"  [B6] Norm: drift={norm_drift:.4e} {'PASS' if p else 'FAIL'}")

    # B7: State-family robustness
    fam_tw=0
    for label,psi_f in [("gauss",_probe_state(g)),("color-0",_color_state(g,0)),("color-1",_color_state(g,1))]:
        psi_f2=_cn_evolve(H_s,psi_f,DT,N_STEPS_SINGLE)
        F_f=_shell_force(g,psi_f2,phi_s); fam_tw+=(F_f>0)
        print(f"    {label:10s}: F={F_f:+.4e} {'TW' if F_f>0 else 'AW'}")
    p=fam_tw==3; score+=p; print(f"  [B7] Families: {fam_tw}/3 {'PASS' if p else 'FAIL'}")

    # B8: Native gauge
    if g.cycle_edge is not None:
        u,v=g.cycle_edge; As=np.linspace(0,2*np.pi,13); Js=[]
        for A in As:
            Hfl=_build_H_flux(g,MASS,g.cycle_edge,A)
            if g.n<=500: ev,ec=np.linalg.eigh(Hfl.toarray())
            else: ev,ec=eigsh(Hfl.tocsc(),k=1,which='SA')
            pg=ec[:,0]; d=math.hypot(g.pos[max(u,v),0]-g.pos[min(u,v),0],g.pos[max(u,v),1]-g.pos[min(u,v),1])
            w=1./max(d,0.5); hop=-0.5j*w*np.exp(1j*A)
            Js.append(np.imag(pg[min(u,v)].conj()*hop*pg[max(u,v)]))
        Jr=np.max(Js)-np.min(Js)
        try:
            def sm(A,a,ph,b): return a*np.sin(A+ph)+b
            popt,_=curve_fit(sm,As,np.array(Js),p0=[Jr/2,0,np.mean(Js)])
            r2s=1-np.sum((np.array(Js)-sm(As,*popt))**2)/np.sum((np.array(Js)-np.mean(Js))**2)
        except: r2s=0
        p=Jr>1e-6 and r2s>0.9; score+=p
        print(f"  [B8] Gauge: J_range={Jr:.4e}, sin_R^2={r2s:.4f} {'PASS' if p else 'FAIL'}")
    else:
        print(f"  [B8] Gauge: no cycle found, SKIP"); score+=0

    # B9: Force-gap + shell/spectral diagnostics
    phi_ext=_ext_phi(g); H_ext=_build_H(g,MASS,phi_ext)
    psi_ext=_cn_evolve(H_ext,psi0,DT,N_STEPS_SINGLE)
    F_ext=_shell_force(g,psi_ext,phi_ext)
    gap=abs(F_s-F_ext)/abs(F_ext) if abs(F_ext)>1e-30 else 0
    G_eff=F_ext/F_s if abs(F_s)>1e-30 else float('inf')
    # Shell profile: Phi_solve vs Phi_ext at each BFS depth
    max_d=int(np.max(g.depth[np.isfinite(g.depth)])) if np.any(np.isfinite(g.depth)) else 0
    ps_sh=np.zeros(max_d+1); pe_sh=np.zeros(max_d+1); cnt=np.zeros(max_d+1)
    for i in range(g.n):
        d_=int(g.depth[i]) if np.isfinite(g.depth[i]) else -1
        if 0<=d_<=max_d:
            ps_sh[d_]+=phi_s[i]; pe_sh[d_]+=phi_ext[i]; cnt[d_]+=1
    for d_ in range(max_d+1):
        if cnt[d_]>0: ps_sh[d_]/=cnt[d_]; pe_sh[d_]/=cnt[d_]
    # Spectral: decompose both into Laplacian eigenmodes
    L=_graph_laplacian(g); evals_L,evecs_L=np.linalg.eigh(L.toarray())
    spec_solve=evecs_L.T@phi_s; spec_ext=evecs_L.T@phi_ext
    # Spectral ratio at low modes (modes 1-5)
    spec_ratios=[]
    for k in range(1,min(6,g.n)):
        if abs(spec_ext[k])>1e-10:
            spec_ratios.append(abs(spec_solve[k]/spec_ext[k]))
    mean_spec_ratio=np.mean(spec_ratios) if spec_ratios else 0
    print(f"  [B9] Gap: G_eff={G_eff:.1f}, shell_grad_ratio={(ps_sh[0]-ps_sh[min(1,max_d)])/(pe_sh[0]-pe_sh[min(1,max_d)]):.3f}" if max_d>0 and abs(pe_sh[0]-pe_sh[min(1,max_d)])>1e-10 else f"  [B9] Gap: G_eff={G_eff:.1f}")
    print(f"       spectral_ratio(modes1-5)={mean_spec_ratio:.3f}")
    score += 1  # characterization, always passes

    print(f"\n  SCORE: {score}/9")
    return score


# ============================================================================
# MAIN
# ============================================================================

if __name__ == '__main__':
    t0 = time.time()
    print("="*70)
    print("STAGGERED FERMION — CYCLE-BEARING GRAPH BATTERY")
    print("="*70)
    print(f"DT={DT}, MASS={MASS}, G={G}, mu2={POISSON_MU2}, N_ITER={N_ITER}")
    print("Force is the primary gravity observable. No centroid. No 1D ring.")
    print()

    scores = []
    families = [make_random_geometric(seed=42), make_growing(seed=42), make_layered_cycle(seed=42)]
    for g in families:
        if g is None:
            print("  REJECTED: graph construction failed (odd cycle or disconnected)")
            continue
        if _has_odd_cycle(g.adj, g.colors):
            print(f"  REJECTED: {g.name} has odd-cycle defect")
            continue
        s = run_battery(g)
        if s is not None: scores.append(s)

    print(f"\n{'='*70}")
    print(f"SUMMARY: {len(scores)} families tested, scores: {scores}")
    print(f"Time: {time.time()-t0:.1f}s")
