#!/usr/bin/env python3
"""
Asymmetry Scaling — Does the sign-sensitive gap grow with G and n?
====================================================================
Two questions:
  Q1: Width asymmetry vs G (coupling strength sweep)
      If asymmetry grows with G, it's a real gravitational effect.
      If constant, it might be numerical noise.

  Q2: Width asymmetry vs n (graph size sweep)
      If asymmetry persists or grows with n, it survives the continuum limit.
      If it shrinks, it's a finite-size artifact.

  Q3: Shapiro delay ratio vs G
      The delay ratio (attract_delay / repulse_delay) was 4-14x in the
      initial test. Is this ratio stable and G-dependent?

All on the random geometric family (cleanest bipartite structure).
"""

from __future__ import annotations
import math, time, random
import numpy as np
from scipy.sparse import lil_matrix, eye as speye
from scipy.sparse.linalg import spsolve
from collections import deque

MASS = 0.30
MU2 = 0.22
DT = 0.12
DT_SHAPIRO = 0.05
N_ITER = 40
N_SHAPIRO_STEPS = 200
SHAPIRO_THRESHOLD = 1e-4


def _ae(adj, a, b):
    adj.setdefault(a, set()).add(b)
    adj.setdefault(b, set()).add(a)


def make_random_geometric(seed=42, side=8):
    rng = random.Random(seed)
    coords, colors, index, adj = [], [], {}, {}; idx = 0
    for x in range(side):
        for y in range(side):
            coords.append((x+0.08*(rng.random()-0.5), y+0.08*(rng.random()-0.5)))
            colors.append((x+y)%2); index[(x,y)] = idx; idx += 1
    pos = np.array(coords); col = np.array(colors, dtype=int)
    for i in range(side):
        for j in range(side):
            a = index[(i,j)]
            for di,dj in ((1,0),(0,1),(1,1),(1,-1)):
                ii,jj = i+di,j+dj
                if (ii,jj) not in index: continue
                b = index[(ii,jj)]
                if col[a]==col[b]: continue
                if math.hypot(pos[b,0]-pos[a,0],pos[b,1]-pos[a,1])<=1.28: _ae(adj,a,b)
    return pos, col, {k:list(v) for k,v in adj.items()}


def _build_L(pos, adj, n):
    L = lil_matrix((n,n), dtype=float)
    for i, nbs in adj.items():
        for j in nbs:
            if i>=j: continue
            d=math.hypot(pos[j,0]-pos[i,0],pos[j,1]-pos[i,1])
            w=1./max(d,0.5); L[i,j]-=w; L[j,i]-=w; L[i,i]+=w; L[j,j]+=w
    return L.tocsr()


def _build_H(pos, col, adj, n, phi):
    H = lil_matrix((n,n), dtype=complex)
    par = np.where(col==0,1.,-1.)
    H.setdiag((MASS+phi)*par)
    for i, nbs in adj.items():
        for j in nbs:
            if i>=j: continue
            d=math.hypot(pos[j,0]-pos[i,0],pos[j,1]-pos[i,1])
            w=1./max(d,0.5); H[i,j]+=-0.5j*w; H[j,i]+=0.5j*w
    return H.tocsr()


def _cn_step(H, psi, dt):
    n=H.shape[0]
    ap=(speye(n,format='csc')+1j*H*dt/2).tocsc()
    am=speye(n,format='csr')-1j*H*dt/2
    return spsolve(ap, am.dot(psi))


def _width(psi, pos):
    rho=np.abs(psi)**2; rho/=np.sum(rho)
    cx=np.sum(rho*pos[:,0]); cy=np.sum(rho*pos[:,1])
    return np.sqrt(np.sum(rho*((pos[:,0]-cx)**2+(pos[:,1]-cy)**2)))


def width_asymmetry(pos, col, adj, G, n_iter=N_ITER):
    """Return width asymmetry ratio (attract/repulse contraction factor)."""
    n = len(pos)
    center = np.mean(pos, axis=0)
    dists_c = np.sqrt(np.sum((pos-center)**2, axis=1))
    L = _build_L(pos, adj, n)

    psi0 = np.exp(-0.5*dists_c**2/1.15**2).astype(complex)
    psi0 /= np.linalg.norm(psi0)

    widths = {}
    for label, phi_sign in [("a", +1.0), ("r", -1.0), ("f", 0.0)]:
        psi = psi0.copy()
        for _ in range(n_iter):
            rho = np.abs(psi)**2
            phi = phi_sign * spsolve((L+MU2*speye(n,format='csr')).tocsc(), G*rho) if phi_sign != 0 else np.zeros(n)
            H = _build_H(pos, col, adj, n, phi)
            psi = _cn_step(H, psi, DT)
        widths[label] = _width(psi, pos)

    ctr_a = widths["a"] / widths["f"]
    ctr_r = widths["r"] / widths["f"]
    return ctr_a / ctr_r if ctr_r > 0 else float('nan')


def shapiro_ratio(pos, col, adj, G):
    """Return Shapiro delay ratio (attract_delay / repulse_delay)."""
    n = len(pos)
    L = _build_L(pos, adj, n)

    # Source at center
    center = np.mean(pos, axis=0)
    dists_c = np.sqrt(np.sum((pos-center)**2, axis=1))
    src = np.argmin(dists_c)
    rho_ext = np.zeros(n); rho_ext[src] = 1.0
    phi_ext = spsolve((L+MU2*speye(n,format='csr')).tocsc(), G*rho_ext)

    # Start: corner nodes
    start_nodes = list(np.argsort(dists_c)[-5:])
    # Detect: opposite corner
    far_from_start = np.sqrt(np.sum((pos - pos[start_nodes[0]])**2, axis=1))
    detect_nodes = list(np.argsort(far_from_start)[-5:])

    psi0 = np.zeros(n, dtype=complex)
    for s in start_nodes: psi0[s] = 1.0
    psi0 /= np.linalg.norm(psi0)

    delays = {}
    for label, phi in [("a", phi_ext), ("r", -phi_ext), ("f", np.zeros(n))]:
        H = _build_H(pos, col, adj, n, phi)
        psi = psi0.copy()
        prob_history = []
        for step in range(N_SHAPIRO_STEPS):
            psi = _cn_step(H, psi, DT_SHAPIRO)
            prob_history.append(sum(np.abs(psi[d])**2 for d in detect_nodes))
        prob_arr = np.array(prob_history)
        hm = 0.5 * np.max(prob_arr) if np.max(prob_arr) > 0 else 0
        hm_time = N_SHAPIRO_STEPS
        for step, p in enumerate(prob_arr):
            if p >= hm: hm_time = step; break
        delays[label] = hm_time

    d_a = delays["a"] - delays["f"]
    d_r = delays["r"] - delays["f"]

    if d_r > 0:
        return d_a / d_r
    elif d_r == 0 and d_a > 0:
        return float('inf')
    else:
        return float('nan')


if __name__ == '__main__':
    t0 = time.time()
    print("=" * 78)
    print("ASYMMETRY SCALING — G AND SIZE DEPENDENCE")
    print("=" * 78)

    # ── Q1: Width asymmetry vs G ────────────────────────────────────
    print("\n--- Q1: Width Asymmetry vs Coupling Strength G ---")
    print(f"{'G':>6s} {'asym_s42':>9s} {'asym_s43':>9s} {'asym_s44':>9s} {'mean':>9s}")
    print("-" * 45)

    pos42, col42, adj42 = make_random_geometric(seed=42, side=8)
    pos43, col43, adj43 = make_random_geometric(seed=43, side=8)
    pos44, col44, adj44 = make_random_geometric(seed=44, side=8)

    for G in [5, 10, 20, 50, 100, 200]:
        a42 = width_asymmetry(pos42, col42, adj42, G)
        a43 = width_asymmetry(pos43, col43, adj43, G)
        a44 = width_asymmetry(pos44, col44, adj44, G)
        mean = np.mean([a42, a43, a44])
        print(f"{G:6.0f} {a42:9.4f} {a43:9.4f} {a44:9.4f} {mean:9.4f}")

    # ── Q2: Width asymmetry vs graph size ───────────────────────────
    print("\n--- Q2: Width Asymmetry vs Graph Size n ---")
    print(f"{'side':>6s} {'n':>5s} {'asym_s42':>9s} {'asym_s43':>9s} {'mean':>9s}")
    print("-" * 42)

    for side in [6, 8, 10, 12]:
        p42, c42, a42_ = make_random_geometric(seed=42, side=side)
        p43, c43, a43_ = make_random_geometric(seed=43, side=side)
        n_ = len(p42)
        wa42 = width_asymmetry(p42, c42, a42_, 50.0)
        wa43 = width_asymmetry(p43, c43, a43_, 50.0)
        mean = np.mean([wa42, wa43])
        print(f"{side:6d} {n_:5d} {wa42:9.4f} {wa43:9.4f} {mean:9.4f}")

    # ── Q3: Shapiro delay ratio vs G ────────────────────────────────
    print("\n--- Q3: Shapiro Delay Ratio vs G ---")
    print(f"{'G':>6s} {'ratio_s42':>10s} {'ratio_s43':>10s} {'mean':>10s}")
    print("-" * 38)

    for G in [5, 10, 20, 50, 100]:
        sr42 = shapiro_ratio(pos42, col42, adj42, G)
        sr43 = shapiro_ratio(pos43, col43, adj43, G)
        vals = [v for v in [sr42, sr43] if np.isfinite(v)]
        mean = np.mean(vals) if vals else float('nan')
        print(f"{G:6.0f} {sr42:10.2f} {sr43:10.2f} {mean:10.2f}")

    print(f"\nTotal time: {time.time()-t0:.1f}s")
