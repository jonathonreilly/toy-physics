#!/usr/bin/env python3
"""
Emergent Geometry G-Threshold Sweep
====================================
Sweep coupling strength G to find the threshold where the grown graph
produces ROBUST_TOWARD gravity (all three force measures agree: positive).

Measures: shell_mean, shell_prob, edge_radial
ROBUST_TOWARD = all three > 0
"""

from __future__ import annotations
import math, time, random
import numpy as np
from scipy.sparse import lil_matrix, csr_matrix, eye as speye
from scipy.sparse.linalg import spsolve
from scipy.stats import linregress
from collections import deque

MASS = 0.30
MU2 = 0.22
DT = 0.12
N_TARGET = 100
N_EVOLVE = 3  # Crank-Nicolson steps per growth iteration

G_VALUES = [10, 20, 30, 50, 75, 100, 125, 150, 200, 250, 300]
SEEDS = [42, 43, 44, 45, 46]


def grow_graph(n_final, G_self, n_evolve=N_EVOLVE, seed=42):
    """Grow graph with matter-coupled preferential attachment (2D seed)."""
    rng = random.Random(seed)

    coords = [(0,0),(1,0),(0,1),(1,1),(0.5,0.5),(1.5,0.5),(0.5,1.5),(1.5,1.5)]
    colors = [0,1,1,0,1,0,0,1]
    n_seed = len(coords)

    adj = {i: set() for i in range(n_seed)}
    for i in range(n_seed):
        for j in range(i+1, n_seed):
            if colors[i] != colors[j]:
                d = math.sqrt(sum((a-b)**2 for a,b in zip(coords[i],coords[j])))
                if d < 1.2:
                    adj[i].add(j)
                    adj[j].add(i)

    pos = list(coords)
    col = list(colors)
    cur = n_seed

    psi = np.ones(n_seed, dtype=complex)
    center_seed = np.mean(np.array(pos), axis=0)
    pos_arr = np.array(pos)
    for i in range(n_seed):
        r2 = (pos_arr[i,0]-center_seed[0])**2 + (pos_arr[i,1]-center_seed[1])**2
        psi[i] = np.exp(-0.5*r2/0.8**2)
    psi /= np.linalg.norm(psi)

    while cur < n_final:
        n = len(pos)
        pos_arr = np.array(pos)
        col_arr = np.array(col, dtype=int)

        adj_l = {k: list(v) for k, v in adj.items()}
        L = lil_matrix((n,n), dtype=float)
        for i, nbs in adj_l.items():
            for j in nbs:
                if i >= j:
                    continue
                d = math.sqrt((pos_arr[j,0]-pos_arr[i,0])**2 + (pos_arr[j,1]-pos_arr[i,1])**2)
                w = 1./max(d, 0.3)
                L[i,j] -= w; L[j,i] -= w; L[i,i] += w; L[j,j] += w
        L = L.tocsr()

        rho = np.abs(psi)**2
        phi = spsolve((L + MU2*speye(n,format='csr')).tocsc(), G_self*rho)

        H = lil_matrix((n,n), dtype=complex)
        par = np.where(col_arr==0, 1., -1.)
        # Parity coupling: (mass + phi) * parity
        H.setdiag((MASS + phi) * par)
        for i, nbs in adj_l.items():
            for j in nbs:
                if i >= j:
                    continue
                d = math.sqrt((pos_arr[j,0]-pos_arr[i,0])**2 + (pos_arr[j,1]-pos_arr[i,1])**2)
                w = 1./max(d, 0.3)
                H[i,j] += -0.5j*w
                H[j,i] += 0.5j*w
        H = H.tocsr()

        ap = (speye(n,format='csc') + 1j*H*DT/2).tocsc()
        am = speye(n,format='csr') - 1j*H*DT/2
        for _ in range(n_evolve):
            psi = spsolve(ap, am.dot(psi))

        # Growth step
        rho = np.abs(psi)**2
        rho_n = rho / np.sum(rho)
        nc = cur % 2
        parent = rng.choices(range(n), weights=rho_n, k=1)[0]
        new_pos = (
            pos_arr[parent,0] + 0.3*(rng.random()-0.5),
            pos_arr[parent,1] + 0.3*(rng.random()-0.5),
        )
        pos.append(new_pos)
        col.append(nc)
        adj[cur] = set()

        dists = []
        for i in range(n):
            if col[i] != nc:
                d = math.sqrt((new_pos[0]-pos_arr[i,0])**2 + (new_pos[1]-pos_arr[i,1])**2)
                dists.append((d, i))
        dists.sort()
        for _, j in dists[:min(3, len(dists))]:
            adj[cur].add(j)
            adj[j].add(cur)

        psi_new = np.zeros(cur+1, dtype=complex)
        psi_new[:n] = psi
        psi_new[cur] = 0.01*psi[parent]
        psi_new /= np.linalg.norm(psi_new)
        psi = psi_new
        cur += 1

    return np.array(pos), np.array(col, dtype=int), {k: list(v) for k, v in adj.items()}, psi


def force_battery(pos, col, adj, psi, G_self):
    """Measure three radial-force observables on the grown graph.

    Returns dict with shell_mean, shell_prob, edge_radial, robust_toward.
    """
    n = len(pos)
    center = np.mean(pos, axis=0)
    dists = np.sqrt(np.sum((pos - center)**2, axis=1))
    src = np.argmin(dists)

    adj_l = adj if isinstance(adj, dict) else adj
    L = lil_matrix((n,n), dtype=float)
    for i, nbs in adj_l.items():
        for j in nbs:
            if i >= j:
                continue
            d = math.sqrt((pos[j,0]-pos[i,0])**2 + (pos[j,1]-pos[i,1])**2)
            w = 1./max(d, 0.3)
            L[i,j] -= w; L[j,i] -= w; L[i,i] += w; L[j,j] += w
    L = L.tocsr()

    rho = np.abs(psi)**2
    phi = spsolve((L + MU2*speye(n,format='csr')).tocsc(), G_self*rho)

    # BFS depth from center
    depth = np.full(n, np.inf)
    depth[src] = 0
    q = deque([src])
    while q:
        i = q.popleft()
        for j in adj_l.get(i, []):
            if depth[j] == np.inf:
                depth[j] = depth[i] + 1
                q.append(j)
    max_d = int(np.max(depth[np.isfinite(depth)]))
    if max_d <= 0:
        return {"shell_mean": 0.0, "shell_prob": 0.0, "edge_radial": 0.0, "robust_toward": False}

    # Shell averages
    ps = np.zeros(max_d+1)
    rs_mean = np.zeros(max_d+1)
    rs_prob = np.zeros(max_d+1)
    cnt = np.zeros(max_d+1)
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
        if d_ == 0:
            grad[d_] = ps[0] - ps[min(1, max_d)]
        elif d_ == max_d:
            grad[d_] = ps[d_-1] - ps[d_]
        else:
            grad[d_] = 0.5*(ps[d_-1] - ps[d_+1])

    shell_mean = float(np.sum(rs_mean * grad))
    shell_prob = float(np.sum(rs_prob * grad))

    # Edge-based radial gradient
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
            d = math.sqrt((pos[j,0]-pos[i,0])**2 + (pos[j,1]-pos[i,1])**2)
            w = 1./max(d, 0.3)
            edge_radial += 0.5 * (rho_n[i] + rho_n[j]) * w * (phi[i] - phi[j]) * sign

    robust_toward = (shell_mean > 0) and (shell_prob > 0) and (edge_radial > 0)
    return {
        "shell_mean": shell_mean,
        "shell_prob": shell_prob,
        "edge_radial": float(edge_radial),
        "robust_toward": robust_toward,
    }


if __name__ == '__main__':
    t0 = time.time()
    print("="*72)
    print("EMERGENT GEOMETRY — G-THRESHOLD SWEEP")
    print(f"N_TARGET={N_TARGET}, MASS={MASS}, MU2={MU2}, DT={DT}")
    print(f"G values: {G_VALUES}")
    print(f"Seeds: {SEEDS}")
    print("="*72)

    # Store results: results[G] = list of dicts per seed
    results = {}

    for G in G_VALUES:
        results[G] = []
        print(f"\n--- G = {G} ---")
        for seed in SEEDS:
            ts = time.time()
            pos, col, adj, psi = grow_graph(N_TARGET, G_self=G, seed=seed)
            out = force_battery(pos, col, adj, psi, G)
            elapsed = time.time() - ts
            results[G].append(out)

            tag = "ROBUST_TOWARD" if out["robust_toward"] else "MIXED/AWAY"
            sm_sign = "+" if out["shell_mean"] > 0 else "-"
            sp_sign = "+" if out["shell_prob"] > 0 else "-"
            er_sign = "+" if out["edge_radial"] > 0 else "-"
            print(
                f"  seed={seed}: shell_mean={out['shell_mean']:+.4e} [{sm_sign}]  "
                f"shell_prob={out['shell_prob']:+.4e} [{sp_sign}]  "
                f"edge_radial={out['edge_radial']:+.4e} [{er_sign}]  "
                f"=> {tag}  ({elapsed:.1f}s)"
            )

    # Summary table
    print("\n" + "="*72)
    print("SUMMARY: ROBUST_TOWARD count per G value (out of 5 seeds)")
    print("="*72)
    print(f"{'G':>6s}  {'Robust':>6s}  {'Frac':>6s}  {'shell_mean':>12s}  {'shell_prob':>12s}  {'edge_radial':>12s}")
    print("-"*72)
    for G in G_VALUES:
        n_robust = sum(1 for r in results[G] if r["robust_toward"])
        frac = n_robust / len(SEEDS)
        # Average signs
        avg_sm = np.mean([r["shell_mean"] for r in results[G]])
        avg_sp = np.mean([r["shell_prob"] for r in results[G]])
        avg_er = np.mean([r["edge_radial"] for r in results[G]])
        print(
            f"{G:6d}  {n_robust:6d}/5  {frac:6.1%}  "
            f"{avg_sm:+.4e}  {avg_sp:+.4e}  {avg_er:+.4e}"
        )

    # Find threshold
    print("\n" + "-"*72)
    threshold_G = None
    for G in G_VALUES:
        n_robust = sum(1 for r in results[G] if r["robust_toward"])
        if n_robust >= 3:  # majority robust
            threshold_G = G
            break
    if threshold_G is not None:
        print(f"THRESHOLD: G >= {threshold_G} gives majority ROBUST_TOWARD (>=3/5 seeds)")
    else:
        print("NO THRESHOLD FOUND: no G value achieves majority ROBUST_TOWARD")

    # Also find unanimous threshold
    unanimous_G = None
    for G in G_VALUES:
        n_robust = sum(1 for r in results[G] if r["robust_toward"])
        if n_robust == 5:
            unanimous_G = G
            break
    if unanimous_G is not None:
        print(f"UNANIMOUS:  G >= {unanimous_G} gives 5/5 ROBUST_TOWARD")

    print(f"\nTotal time: {time.time()-t0:.1f}s")
