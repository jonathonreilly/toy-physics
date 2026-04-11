#!/usr/bin/env python3
"""
Emergent Geometry from Matter-Coupled Graph Growth
====================================================
THE NATURE EXPERIMENT: Does a growth rule coupled to quantum matter
produce a graph whose effective geometry looks like curved spacetime?

Setup:
  1. Start with a small seed graph (bipartite, 8 nodes)
  2. Growth rule: add new node, connect to existing nodes with
     probability proportional to |ψ|² (matter density)
  3. After each growth step, re-evolve staggered ψ on the new graph
  4. After N growth steps, measure:
     a. BFS shell volumes V(r) — does it match d-dimensional geometry?
     b. Effective metric: does hopping near high-density regions differ
        from hopping in the bulk?
     c. Does the grown graph's Phi profile match a gravitational potential?

The key prediction: nodes cluster around high-|ψ|² regions because
the growth rule preferentially connects there. This creates a denser
graph near the "mass" — which IS curved geometry on a graph.

If V(r) ~ r^(d-1) for some emergent d, and the density profile
matches a gravitational potential, that's emergent spacetime.
"""

from __future__ import annotations
import math, time, random
import numpy as np
from scipy.sparse import lil_matrix, csr_matrix, eye as speye
from scipy.sparse.linalg import spsolve
from collections import deque

MASS = 0.3; MU2 = 0.22; DT = 0.12; G_SELF = 50.0


def _ae(adj, a, b):
    adj.setdefault(a, set()).add(b); adj.setdefault(b, set()).add(a)


def grow_graph_matter_coupled(n_final=80, n_evolve_steps=5, seed=42):
    """Grow a graph where new nodes connect preferentially to
    regions of high matter density |ψ|²."""
    rng = random.Random(seed)

    # Seed: small bipartite graph (2x2x2 cube-like)
    coords = [(0,0),(1,0),(0,1),(1,1),(0.5,0.5),(1.5,0.5),(0.5,1.5),(1.5,1.5)]
    colors = [0,1,1,0,1,0,0,1]  # checkerboard
    adj = {i: set() for i in range(8)}
    # Connect nearest neighbors of opposite color
    for i in range(8):
        for j in range(i+1,8):
            if colors[i] != colors[j]:
                d = math.hypot(coords[j][0]-coords[i][0], coords[j][1]-coords[i][1])
                if d < 1.2:
                    adj[i].add(j); adj[j].add(i)

    pos = list(coords); col = list(colors)
    cur = len(pos)

    # Initial wavefunction on seed graph
    n_seed = len(pos)
    pos_arr = np.array(pos)
    center = np.mean(pos_arr, axis=0)
    psi = np.exp(-0.5*((pos_arr[:,0]-center[0])**2+(pos_arr[:,1]-center[1])**2)/0.8**2).astype(complex)
    psi /= np.linalg.norm(psi)

    growth_log = []

    while cur < n_final:
        n = len(pos); pos_arr = np.array(pos); col_arr = np.array(col, dtype=int)

        # Evolve ψ on current graph (self-gravity)
        L = lil_matrix((n,n), dtype=float)
        adj_l = {k: list(v) for k, v in adj.items()}
        for i, nbs in adj_l.items():
            for j in nbs:
                if i >= j: continue
                d = math.hypot(pos_arr[j,0]-pos_arr[i,0], pos_arr[j,1]-pos_arr[i,1])
                w = 1./max(d, 0.3)
                L[i,j] -= w; L[j,i] -= w; L[i,i] += w; L[j,j] += w
        L = L.tocsr()

        # Self-gravity: Phi from |psi|^2
        rho = np.abs(psi)**2
        phi = spsolve((L + MU2*speye(n,format='csr')).tocsc(), G_SELF*rho)

        # Build H and evolve
        H = lil_matrix((n,n), dtype=complex)
        par = np.where(col_arr==0, 1., -1.)
        # Parity (scalar 1⊗1) coupling: Φ modulates mass gap via ε(x).
        H.setdiag((MASS+phi)*par)
        for i, nbs in adj_l.items():
            for j in nbs:
                if i >= j: continue
                d = math.hypot(pos_arr[j,0]-pos_arr[i,0], pos_arr[j,1]-pos_arr[i,1])
                w = 1./max(d, 0.3)
                H[i,j] += -0.5j*w; H[j,i] += 0.5j*w
        H = H.tocsr()
        ap = (speye(n,format='csc')+1j*H*DT/2).tocsc()
        am = speye(n,format='csr')-1j*H*DT/2
        for _ in range(n_evolve_steps):
            psi = spsolve(ap, am.dot(psi))

        # Growth: add a new node connected to high-|psi|^2 regions
        rho = np.abs(psi)**2
        rho_norm = rho / np.sum(rho)

        # Choose new color (alternate to maintain bipartite-ish structure)
        new_color = cur % 2

        # Position: near a high-density node + small random offset
        parent = rng.choices(range(n), weights=rho_norm, k=1)[0]
        offset_x = 0.3 * (rng.random() - 0.5)
        offset_y = 0.3 * (rng.random() - 0.5)
        new_pos = (pos_arr[parent, 0] + offset_x, pos_arr[parent, 1] + offset_y)
        pos.append(new_pos); col.append(new_color)

        # Connect to k nearest nodes of OPPOSITE color
        k_connect = min(3, n)
        dists = [(math.hypot(new_pos[0]-pos_arr[i,0], new_pos[1]-pos_arr[i,1]), i) for i in range(n) if col[i] != new_color]
        dists.sort()
        adj[cur] = set()
        for _, j in dists[:k_connect]:
            adj[cur].add(j); adj[j].add(cur)

        # Extend psi to new node (small amplitude)
        psi_new = np.zeros(cur+1, dtype=complex)
        psi_new[:n] = psi
        psi_new[cur] = 0.01 * psi[parent]  # inherit a bit from parent
        psi_new /= np.linalg.norm(psi_new)
        psi = psi_new

        growth_log.append((cur, parent, rho[parent], new_pos))
        cur += 1

    return np.array(pos), np.array(col,dtype=int), {k:list(v) for k,v in adj.items()}, psi, growth_log


def analyze_geometry(pos, col, adj, psi, growth_log):
    """Analyze the geometry of the grown graph."""
    n = len(pos)
    center = np.mean(pos, axis=0)

    # 1. Where did the new nodes go? Density profile
    print("\n--- Node Density Profile ---")
    distances = np.sqrt((pos[:,0]-center[0])**2 + (pos[:,1]-center[1])**2)
    r_bins = np.linspace(0, np.max(distances)*0.8, 8)
    for i in range(len(r_bins)-1):
        mask = (distances >= r_bins[i]) & (distances < r_bins[i+1])
        count = np.sum(mask)
        area = np.pi * (r_bins[i+1]**2 - r_bins[i]**2)
        density = count / area if area > 0 else 0
        print(f"  r=[{r_bins[i]:.2f},{r_bins[i+1]:.2f}): nodes={count}, density={density:.2f}")

    # 2. BFS shell volumes from center node
    print("\n--- BFS Shell Volumes ---")
    center_node = np.argmin(distances)
    depth = np.full(n, np.inf); depth[center_node] = 0; q = deque([center_node])
    while q:
        i = q.popleft()
        for j in adj.get(i, []):
            if depth[j] == np.inf:
                depth[j] = depth[i] + 1; q.append(j)
    max_d = int(np.max(depth[np.isfinite(depth)]))
    shell_counts = np.zeros(max_d+1)
    for i in range(n):
        d = int(depth[i]) if np.isfinite(depth[i]) else -1
        if 0 <= d <= max_d: shell_counts[d] += 1
    for d in range(max_d+1):
        print(f"  shell {d}: {int(shell_counts[d])} nodes")

    # 3. Effective dimension from shell growth: V(r) ~ r^(d-1) => d = 1 + log(V)/log(r)
    if max_d >= 3:
        cum_vol = np.cumsum(shell_counts)
        r_vals = np.arange(1, max_d+1)
        vol_vals = cum_vol[1:]
        valid = vol_vals > 0
        if np.sum(valid) >= 3:
            from scipy.stats import linregress
            lr = linregress(np.log(r_vals[valid]), np.log(vol_vals[valid]))
            d_eff = lr.slope
            print(f"\n  Effective dimension (V ~ r^d): d_eff = {d_eff:.2f} (R² = {lr.rvalue**2:.4f})")

    # 4. Where is the matter? |ψ|² profile
    print("\n--- Matter Density Profile ---")
    rho = np.abs(psi)**2; rho /= np.sum(rho)
    for i in range(len(r_bins)-1):
        mask = (distances >= r_bins[i]) & (distances < r_bins[i+1])
        p_in = np.sum(rho[mask])
        print(f"  r=[{r_bins[i]:.2f},{r_bins[i+1]:.2f}): P={p_in:.4f}")

    # 5. Growth pattern: did new nodes cluster around the matter?
    print("\n--- Growth Clustering ---")
    if len(growth_log) > 0:
        parent_rhos = [g[2] for g in growth_log]
        mean_parent_rho = np.mean(parent_rhos)
        mean_uniform_rho = 1.0 / len(pos)
        clustering = mean_parent_rho / mean_uniform_rho if mean_uniform_rho > 0 else 0
        print(f"  Mean parent rho: {mean_parent_rho:.6f}")
        print(f"  Uniform rho: {mean_uniform_rho:.6f}")
        print(f"  Clustering ratio: {clustering:.2f}x")
        print(f"  (>1 means nodes preferentially grew near matter)")

    # 6. Degree profile: does connectivity increase near the center?
    print("\n--- Degree vs Distance ---")
    for i in range(len(r_bins)-1):
        mask = (distances >= r_bins[i]) & (distances < r_bins[i+1])
        if np.sum(mask) > 0:
            indices = np.where(mask)[0]
            degrees = [len(adj.get(j, [])) for j in indices]
            print(f"  r=[{r_bins[i]:.2f},{r_bins[i+1]:.2f}): mean_degree={np.mean(degrees):.1f}")

    return distances, depth, shell_counts


if __name__ == '__main__':
    t0 = time.time()
    print("=" * 70)
    print("EMERGENT GEOMETRY FROM MATTER-COUPLED GRAPH GROWTH")
    print("=" * 70)
    print("Growth rule: new nodes connect preferentially to high-|ψ|² regions.")
    print("After growth, analyze: node density, shell volumes, effective dimension.")
    print()

    # Grow the graph
    pos, col, adj, psi, log = grow_graph_matter_coupled(n_final=120, n_evolve_steps=3, seed=42)
    n = len(pos)
    print(f"Grown graph: {n} nodes")

    # Bipartite check
    odd = any(col[i]==col[j] for i,nbs in adj.items() for j in nbs if len(nbs)>0)
    print(f"Bipartite: {not odd}")

    # Analyze
    distances, depth, shells = analyze_geometry(pos, col, adj, psi, log)

    # Compare with UNIFORM growth (no matter coupling)
    print(f"\n{'='*70}")
    print("CONTROL: Uniform Random Growth (no matter coupling)")
    print(f"{'='*70}")

    rng = random.Random(43)
    pos_u = list([(0,0),(1,0),(0,1),(1,1),(0.5,0.5),(1.5,0.5),(0.5,1.5),(1.5,1.5)])
    col_u = [0,1,1,0,1,0,0,1]
    adj_u = {i:set() for i in range(8)}
    for i in range(8):
        for j in range(i+1,8):
            if col_u[i] != col_u[j]:
                d = math.hypot(pos_u[j][0]-pos_u[i][0], pos_u[j][1]-pos_u[i][1])
                if d < 1.2: adj_u[i].add(j); adj_u[j].add(i)
    for cur in range(8, 120):
        nc = cur % 2
        px = rng.uniform(-2, 3); py = rng.uniform(-2, 3)
        pos_u.append((px,py)); col_u.append(nc)
        adj_u[cur] = set()
        dists = [(math.hypot(px-pos_u[i][0],py-pos_u[i][1]),i) for i in range(cur) if col_u[i]!=nc]
        dists.sort()
        for _,j in dists[:3]: adj_u[cur].add(j); adj_u[j].add(cur)

    pos_u_arr = np.array(pos_u); col_u_arr = np.array(col_u, dtype=int)
    adj_u_l = {k:list(v) for k,v in adj_u.items()}
    psi_u = np.ones(120, dtype=complex)/np.sqrt(120)
    analyze_geometry(pos_u_arr, col_u_arr, adj_u_l, psi_u, [])

    elapsed = time.time() - t0
    print(f"\nTotal time: {elapsed:.1f}s")
