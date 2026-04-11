#!/usr/bin/env python3
"""
Emergent Geometry v2 — Full Analysis
======================================
Four questions about the matter-coupled graph growth:

Q1: Does the node density profile match the gravitational potential Φ(r)?
    If yes: the geometry IS the potential — Einstein-like.

Q2: Does d_eff change with gravity coupling G_self?
    If yes: stronger gravity = more curvature = different geometry.

Q3: Does the grown graph's staggered physics still pass the force battery?
    If yes: the physics survives on emergent geometry.

Q4: Can the growth rule produce d_eff = 3 (our universe)?
    If yes with 3D seed: emergent dimensionality is seed-determined.
"""

from __future__ import annotations
import math, time, random
import numpy as np
from scipy.sparse import lil_matrix, csr_matrix, eye as speye
from scipy.sparse.linalg import spsolve
from scipy.optimize import curve_fit
from scipy.stats import linregress
from collections import deque

MASS = 0.3; MU2 = 0.22; DT = 0.12


def _ae(adj, a, b):
    adj.setdefault(a, set()).add(b); adj.setdefault(b, set()).add(a)


def grow_graph(n_final, G_self, n_evolve=3, seed=42, dim=2):
    """Grow graph with matter-coupled preferential attachment."""
    rng = random.Random(seed)

    if dim == 2:
        # 2D seed
        coords = [(0,0),(1,0),(0,1),(1,1),(0.5,0.5),(1.5,0.5),(0.5,1.5),(1.5,1.5)]
        colors = [0,1,1,0,1,0,0,1]
    else:
        # 3D seed
        coords = [(i,j,k) for i in range(2) for j in range(2) for k in range(2)]
        colors = [(i+j+k)%2 for i in range(2) for j in range(2) for k in range(2)]

    n_seed = len(coords)
    adj = {i: set() for i in range(n_seed)}
    for i in range(n_seed):
        for j in range(i+1, n_seed):
            if colors[i] != colors[j]:
                d = math.sqrt(sum((a-b)**2 for a,b in zip(coords[i],coords[j])))
                if d < 1.2: adj[i].add(j); adj[j].add(i)

    pos = list(coords); col = list(colors); cur = n_seed
    d_dim = len(coords[0]) if isinstance(coords[0], tuple) else 2

    psi = np.ones(n_seed, dtype=complex)
    center_seed = np.mean(np.array(pos), axis=0)
    pos_arr = np.array(pos)
    for i in range(n_seed):
        r2 = sum((pos_arr[i,d]-center_seed[d])**2 for d in range(d_dim))
        psi[i] = np.exp(-0.5*r2/0.8**2)
    psi /= np.linalg.norm(psi)

    while cur < n_final:
        n = len(pos); pos_arr = np.array(pos); col_arr = np.array(col, dtype=int)

        # Build Laplacian + H
        adj_l = {k: list(v) for k, v in adj.items()}
        L = lil_matrix((n,n), dtype=float)
        for i, nbs in adj_l.items():
            for j in nbs:
                if i >= j: continue
                d = math.sqrt(sum((pos_arr[j,d_]-pos_arr[i,d_])**2 for d_ in range(d_dim)))
                w = 1./max(d, 0.3)
                L[i,j] -= w; L[j,i] -= w; L[i,i] += w; L[j,j] += w
        L = L.tocsr()

        rho = np.abs(psi)**2
        phi = spsolve((L + MU2*speye(n,format='csr')).tocsc(), G_self*rho)
        H = lil_matrix((n,n), dtype=complex)
        par = np.where(col_arr==0, 1., -1.)
        # Parity (scalar 1⊗1) coupling: Φ modulates mass gap via ε(x).
        H.setdiag((MASS+phi)*par)
        for i, nbs in adj_l.items():
            for j in nbs:
                if i >= j: continue
                d = math.sqrt(sum((pos_arr[j,d_]-pos_arr[i,d_])**2 for d_ in range(d_dim)))
                w = 1./max(d, 0.3)
                H[i,j] += -0.5j*w; H[j,i] += 0.5j*w
        H = H.tocsr()
        ap = (speye(n,format='csc')+1j*H*DT/2).tocsc()
        am = speye(n,format='csr')-1j*H*DT/2
        for _ in range(n_evolve):
            psi = spsolve(ap, am.dot(psi))

        # Growth
        rho = np.abs(psi)**2; rho_n = rho/np.sum(rho)
        nc = cur % 2
        parent = rng.choices(range(n), weights=rho_n, k=1)[0]
        if d_dim == 2:
            new_pos = (pos_arr[parent,0]+0.3*(rng.random()-0.5), pos_arr[parent,1]+0.3*(rng.random()-0.5))
        else:
            new_pos = tuple(pos_arr[parent,d_]+0.3*(rng.random()-0.5) for d_ in range(d_dim))
        pos.append(new_pos); col.append(nc)
        adj[cur] = set()
        dists = []
        for i in range(n):
            if col[i] != nc:
                d = math.sqrt(sum((new_pos[d_]-pos[i][d_] if isinstance(pos[i],tuple) else new_pos[d_]-pos_arr[i,d_])**2 for d_ in range(d_dim)))
                dists.append((d, i))
        dists.sort()
        for _, j in dists[:min(3, len(dists))]:
            adj[cur].add(j); adj[j].add(cur)

        psi_new = np.zeros(cur+1, dtype=complex)
        psi_new[:n] = psi; psi_new[cur] = 0.01*psi[parent]
        psi /= np.linalg.norm(psi_new); psi = psi_new/np.linalg.norm(psi_new)
        cur += 1

    return np.array(pos), np.array(col,dtype=int), {k:list(v) for k,v in adj.items()}, psi


def measure_d_eff(pos, adj, n):
    """Measure effective dimension from BFS shell volumes."""
    d_dim = pos.shape[1] if pos.ndim > 1 else 2
    center = np.mean(pos, axis=0)
    dists = np.sqrt(np.sum((pos - center)**2, axis=1))
    ci = np.argmin(dists)
    depth = np.full(n, np.inf); depth[ci] = 0; q = deque([ci])
    adj_l = adj if isinstance(adj, dict) else adj
    while q:
        i = q.popleft()
        for j in adj_l.get(i, []):
            if depth[j] == np.inf: depth[j] = depth[i]+1; q.append(j)
    max_d = int(np.max(depth[np.isfinite(depth)]))
    if max_d < 3: return 0, 0
    shells = np.zeros(max_d+1)
    for i in range(n):
        d_ = int(depth[i]) if np.isfinite(depth[i]) else -1
        if 0 <= d_ <= max_d: shells[d_] += 1
    cum = np.cumsum(shells); r = np.arange(1, max_d+1); v = cum[1:]
    valid = v > 0
    if np.sum(valid) < 3: return 0, 0
    lr = linregress(np.log(r[valid]), np.log(v[valid]))
    return lr.slope, lr.rvalue**2


def force_battery_on_grown(pos, col, adj, psi, G_self):
    """Quick force audit on the grown graph.

    Returns three radial-force variants:
      - shell_mean: legacy shell-averaged proxy used in early probes
      - shell_prob: shell-gradient weighted by total shell probability
      - edge_radial: edge-based radial gradient weighted by local probability

    The last two are the defensible observables on highly nonuniform graphs.
    """
    n = len(pos); d_dim = pos.shape[1]
    center = np.mean(pos, axis=0); dists = np.sqrt(np.sum((pos-center)**2, axis=1))
    src = np.argmin(dists)

    adj_l = adj if isinstance(adj, dict) else adj
    L = lil_matrix((n,n), dtype=float)
    for i, nbs in adj_l.items():
        for j in nbs:
            if i >= j: continue
            d = math.sqrt(sum((pos[j,d_]-pos[i,d_])**2 for d_ in range(d_dim)))
            w = 1./max(d, 0.3)
            L[i,j] -= w; L[j,i] -= w; L[i,i] += w; L[j,j] += w
    L = L.tocsr()

    # Self-gravity force
    rho = np.abs(psi)**2
    phi = spsolve((L + MU2*speye(n,format='csr')).tocsc(), G_self*rho)

    depth = np.full(n, np.inf); depth[src] = 0; q = deque([src])
    while q:
        i = q.popleft()
        for j in adj_l.get(i, []):
            if depth[j] == np.inf: depth[j] = depth[i]+1; q.append(j)
    max_d = int(np.max(depth[np.isfinite(depth)]))
    if max_d <= 0:
        return {"shell_mean": 0.0, "shell_prob": 0.0, "edge_radial": 0.0, "toward": False}

    ps = np.zeros(max_d+1); rs_mean = np.zeros(max_d+1); rs_prob = np.zeros(max_d+1); cnt = np.zeros(max_d+1)
    for i in range(n):
        d_ = int(depth[i]) if np.isfinite(depth[i]) else -1
        if 0 <= d_ <= max_d:
            ps[d_] += phi[i]
            rs_mean[d_] += rho[i]
            rs_prob[d_] += rho[i]
            cnt[d_] += 1
    for d_ in range(max_d+1):
        if cnt[d_] > 0:
            ps[d_] /= cnt[d_]
            rs_mean[d_] /= cnt[d_]
    grad = np.zeros(max_d+1)
    for d_ in range(max_d+1):
        if d_ == 0: grad[d_] = ps[0] - ps[min(1,max_d)]
        elif d_ == max_d: grad[d_] = ps[d_-1] - ps[d_]
        else: grad[d_] = 0.5*(ps[d_-1] - ps[d_+1])
    shell_mean = float(np.sum(rs_mean * grad))
    shell_prob = float(np.sum(rs_prob * grad))

    edge_radial = 0.0
    rho_n = rho / np.sum(rho)
    for i, nbs in adj_l.items():
        di = int(depth[i]) if np.isfinite(depth[i]) else -1
        for j in nbs:
            if i >= j:
                continue
            dj = int(depth[j]) if np.isfinite(depth[j]) else -1
            dd = dj - di
            if dd == 0:
                continue
            sign = 1.0 if dd > 0 else -1.0
            d = math.sqrt(sum((pos[j,d_]-pos[i,d_])**2 for d_ in range(d_dim)))
            w = 1./max(d, 0.3)
            edge_radial += 0.5 * (rho_n[i] + rho_n[j]) * w * (phi[i] - phi[j]) * sign

    # Require the probability-weighted and edge-based observables to agree.
    toward = shell_prob > 0 and edge_radial > 0
    return {
        "shell_mean": shell_mean,
        "shell_prob": shell_prob,
        "edge_radial": float(edge_radial),
        "toward": toward,
    }


if __name__ == '__main__':
    t0 = time.time()
    print("="*70)
    print("EMERGENT GEOMETRY v2 — FOUR QUESTIONS")
    print("="*70)

    # Q1: Does node density match Phi(r)?
    print("\n--- Q1: Node Density vs Gravitational Potential ---")
    pos, col, adj, psi = grow_graph(120, G_self=50, seed=42)
    n = len(pos); center = np.mean(pos, axis=0)
    dists = np.sqrt((pos[:,0]-center[0])**2 + (pos[:,1]-center[1])**2)

    L = lil_matrix((n,n), dtype=float)
    for i, nbs in adj.items():
        for j in nbs:
            if i >= j: continue
            d = math.hypot(pos[j,0]-pos[i,0], pos[j,1]-pos[i,1])
            w = 1./max(d, 0.3)
            L[i,j] -= w; L[j,i] -= w; L[i,i] += w; L[j,j] += w
    phi = spsolve((L.tocsr() + MU2*speye(n,format='csr')).tocsc(), 50*np.abs(psi)**2)

    r_bins = np.linspace(0.1, 0.8, 8)
    density_profile = []; phi_profile = []
    for i in range(len(r_bins)-1):
        mask = (dists >= r_bins[i]) & (dists < r_bins[i+1])
        area = np.pi*(r_bins[i+1]**2 - r_bins[i]**2)
        density_profile.append(np.sum(mask)/area if area > 0 else 0)
        phi_profile.append(np.mean(phi[mask]) if np.sum(mask) > 0 else 0)

    d_arr = np.array(density_profile); p_arr = np.array(phi_profile)
    valid = (d_arr > 0) & (p_arr > 0)
    if np.sum(valid) >= 3:
        lr = linregress(p_arr[valid], d_arr[valid])
        print(f"  Density vs Phi correlation: R^2={lr.rvalue**2:.4f}, slope={lr.slope:.2f}")
        print(f"  {'POSITIVE' if lr.slope > 0 else 'NEGATIVE'} correlation: denser where Phi is stronger")
    else:
        print(f"  Not enough data for correlation")

    # Q2: d_eff vs G_self
    print("\n--- Q2: Effective Dimension vs Gravity Coupling ---")
    for G in [0, 10, 25, 50, 100, 200]:
        pos_g, col_g, adj_g, psi_g = grow_graph(100, G_self=G, seed=42)
        d_eff, r2 = measure_d_eff(pos_g, adj_g, len(pos_g))
        print(f"  G={G:4d}: d_eff={d_eff:.3f} (R^2={r2:.4f})")

    # Q3: Force battery on grown graph
    print("\n--- Q3: Force Battery on Grown Graph ---")
    for G in [25, 50, 100]:
        pos_g, col_g, adj_g, psi_g = grow_graph(100, G_self=G, seed=42)
        out = force_battery_on_grown(pos_g, col_g, adj_g, psi_g, G)
        norm = np.linalg.norm(psi_g)
        print(
            f"  G={G:4d}: shell_mean={out['shell_mean']:+.4e}, "
            f"shell_prob={out['shell_prob']:+.4e}, edge_radial={out['edge_radial']:+.4e} "
            f"{'ROBUST_TOWARD' if out['toward'] else 'MIXED/AWAY'}, |psi|={norm:.6f}"
        )

    # Q4: Can we get d_eff = 3 from 3D seed?
    print("\n--- Q4: 3D Seed → d_eff=3? ---")
    for G in [0, 50, 100]:
        pos_3, col_3, adj_3, psi_3 = grow_graph(100, G_self=G, seed=42, dim=3)
        d_eff, r2 = measure_d_eff(pos_3, adj_3, len(pos_3))
        print(f"  3D seed, G={G:4d}: d_eff={d_eff:.3f} (R^2={r2:.4f})")

    print(f"\nTotal time: {time.time()-t0:.1f}s")
