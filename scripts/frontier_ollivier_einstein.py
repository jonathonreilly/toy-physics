#!/usr/bin/env python3
"""
Potential-Weighted Ollivier Curvature vs Stress-Energy Proxy
============================================================

Audit whether self-consistent gravity induces a bounded linearized proxy

    Delta_kappa ~ G * T

on a screened periodic staggered lattice.

Protocol on 2D staggered lattice (side=10):

1. Compute Ollivier-Ricci curvature kappa(e) on every edge BEFORE gravity
   (free Hamiltonian, Phi=0) -- both unweighted and density-weighted.
2. Evolve 30 steps under self-gravity (G, parity coupling).
3. Compute kappa(e) AFTER gravity using THREE approaches:
   (a) Density-weighted: mu_i proportional to |psi|^2 on neighbors
   (b) Potential-weighted: edge distances d_eff(i,j) = 1 + alpha*Phi_avg(e)
   (c) Combined: density-weighted measures on potential-weighted graph
4. Compute Delta_kappa(e) = kappa_after - kappa_before.
5. Compute local stress-energy proxy T(e) = average |psi|^2 at two endpoints.
6. Fit:  Delta_kappa vs G*T.  Report R^2.

Sweep G = [1, 5, 10, 20, 50]. Does the slope scale linearly with G?

Ollivier-Ricci curvature kappa(i,j) = 1 - W_1(mu_i, mu_j) / d(i,j).

Important caveat:
- on this surface, only the potential-weighted metric definition produces a
  strong signal
- this runner is therefore a curvature-density proxy audit, not a derivation
  of Einstein's equation
"""

from __future__ import annotations

import math
import time
from collections import deque

import numpy as np
from scipy import sparse
from scipy.optimize import linprog
from scipy.sparse import eye as speye, lil_matrix
from scipy.sparse.linalg import spsolve
from scipy.stats import linregress

# ── Physical parameters ────────────────────────────────────────────
MASS = 0.30
MU2 = 0.22
DT = 0.12
N_STEPS = 30
SIGMA = 1.5
SIDE = 10

G_VALUES = [1, 5, 10, 20, 50]


# ── Lattice ────────────────────────────────────────────────────────

def build_lattice_2d(side: int):
    """2D periodic square lattice with checkerboard parity."""
    n = side * side
    pos = np.zeros((n, 2))
    adj: dict[int, list[int]] = {i: [] for i in range(n)}
    col = np.zeros(n, dtype=int)

    for ix in range(side):
        for iy in range(side):
            idx = ix * side + iy
            pos[idx] = (ix, iy)
            col[idx] = (ix + iy) % 2
            for dix, diy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                jx = (ix + dix) % side
                jy = (iy + diy) % side
                adj[idx].append(jx * side + jy)

    return n, pos, adj, col


def minimum_image_delta(a: float, b: float, side: int) -> float:
    """Periodic displacement on a 1D torus."""
    delta = b - a
    half = side / 2.0
    if delta > half:
        delta -= side
    elif delta < -half:
        delta += side
    return delta


# ── Hamiltonian and evolution ──────────────────────────────────────

def build_laplacian(adj: dict[int, list[int]], n: int):
    L = lil_matrix((n, n), dtype=float)
    for i in range(n):
        for j in adj[i]:
            if i >= j:
                continue
            L[i, j] -= 1.0
            L[j, i] -= 1.0
            L[i, i] += 1.0
            L[j, j] += 1.0
    return L.tocsr()


def build_hamiltonian(pos: np.ndarray, col: np.ndarray,
                      adj: dict[int, list[int]], n: int,
                      phi: np.ndarray) -> sparse.csc_matrix:
    """Staggered-fermion Hamiltonian with parity coupling."""
    H = lil_matrix((n, n), dtype=complex)
    par = np.where(col == 0, 1.0, -1.0)
    H.setdiag((MASS + phi) * par)

    for i in range(n):
        for j in adj[i]:
            if i >= j:
                continue
            dx = minimum_image_delta(pos[i, 0], pos[j, 0], SIDE)
            dy = minimum_image_delta(pos[i, 1], pos[j, 1], SIDE)
            d = math.hypot(dx, dy)
            d = min(d, 2.0)
            w = 1.0 / max(d, 0.5)
            H[i, j] += -0.5j * w
            H[j, i] += 0.5j * w

    return H.tocsc()


def cn_step(psi: np.ndarray, H: sparse.csc_matrix, dt: float) -> np.ndarray:
    """Crank-Nicolson time step."""
    n = H.shape[0]
    ap = (speye(n, format='csc') + 1j * H * dt / 2).tocsc()
    am = speye(n, format='csr') - 1j * H * dt / 2
    return spsolve(ap, am.dot(psi))


def make_gaussian(pos: np.ndarray, n: int):
    cx = (pos[:, 0].max() + pos[:, 0].min()) / 2
    cy = (pos[:, 1].max() + pos[:, 1].min()) / 2
    r2 = (pos[:, 0] - cx)**2 + (pos[:, 1] - cy)**2
    psi = np.exp(-r2 / (2 * SIGMA**2)).astype(complex)
    psi /= np.linalg.norm(psi)
    return psi


# ── Shortest paths (weighted) ─────────────────────────────────────

def bfs_distances(adj: dict[int, list[int]], src: int, n: int) -> np.ndarray:
    dist = np.full(n, -1, dtype=int)
    dist[src] = 0
    q = deque([src])
    while q:
        u = q.popleft()
        for v in adj[u]:
            if dist[v] == -1:
                dist[v] = dist[u] + 1
                q.append(v)
    return dist


def all_pairs_bfs(adj: dict[int, list[int]], n: int) -> np.ndarray:
    D = np.zeros((n, n), dtype=int)
    for i in range(n):
        D[i] = bfs_distances(adj, i, n)
    return D


def dijkstra(adj: dict[int, list[int]], edge_weight: dict[tuple[int, int], float],
             src: int, n: int) -> np.ndarray:
    """Dijkstra with arbitrary positive edge weights."""
    import heapq
    dist = np.full(n, np.inf)
    dist[src] = 0.0
    pq = [(0.0, src)]
    while pq:
        d, u = heapq.heappop(pq)
        if d > dist[u]:
            continue
        for v in adj[u]:
            key = (min(u, v), max(u, v))
            w = edge_weight.get(key, 1.0)
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                heapq.heappush(pq, (nd, v))
    return dist


def all_pairs_dijkstra(adj, edge_weight, n):
    D = np.zeros((n, n))
    for i in range(n):
        D[i] = dijkstra(adj, edge_weight, i, n)
    return D


# ── Wasserstein-1 distance ────────────────────────────────────────

def wasserstein_1(support_i: list[int], weights_i: np.ndarray,
                  support_j: list[int], weights_j: np.ndarray,
                  D: np.ndarray) -> float:
    """W_1 distance between two discrete probability measures via LP."""
    m = len(support_i)
    k = len(support_j)
    if m == 0 or k == 0:
        return 0.0

    cost = np.zeros((m, k))
    for a in range(m):
        for b in range(k):
            cost[a, b] = D[support_i[a], support_j[b]]

    n_vars = m * k
    c = cost.flatten()

    A_eq = np.zeros((m + k, n_vars))
    b_eq = np.zeros(m + k)

    for a in range(m):
        for b in range(k):
            A_eq[a, a * k + b] = 1.0
        b_eq[a] = weights_i[a]

    for b in range(k):
        for a in range(m):
            A_eq[m + b, a * k + b] = 1.0
        b_eq[m + b] = weights_j[b]

    result = linprog(c, A_eq=A_eq, b_eq=b_eq,
                     bounds=(0, None), method='highs')

    return result.fun if result.success else 0.0


# ── Ollivier-Ricci curvature ──────────────────────────────────────

def compute_OR_uniform(adj, n, D):
    """Standard Ollivier-Ricci with uniform measures on neighbors."""
    kappa = {}
    for i in range(n):
        for j in adj[i]:
            if i >= j:
                continue
            d_ij = D[i, j]
            if d_ij == 0:
                continue
            nb_i = adj[i]
            nb_j = adj[j]
            m_i = len(nb_i)
            m_j = len(nb_j)
            w_i = np.ones(m_i) / m_i
            w_j = np.ones(m_j) / m_j
            w1 = wasserstein_1(nb_i, w_i, nb_j, w_j, D)
            kappa[(i, j)] = 1.0 - w1 / d_ij
    return kappa


def compute_OR_density_weighted(adj, n, D, rho):
    """Ollivier-Ricci with density-weighted measures on neighbors."""
    kappa = {}
    for i in range(n):
        for j in adj[i]:
            if i >= j:
                continue
            d_ij = D[i, j]
            if d_ij == 0:
                continue
            nb_i = adj[i]
            nb_j = adj[j]
            w_i = np.array([rho[v] for v in nb_i])
            w_j = np.array([rho[v] for v in nb_j])
            s_i, s_j = w_i.sum(), w_j.sum()
            if s_i < 1e-30 or s_j < 1e-30:
                kappa[(i, j)] = 0.0
                continue
            w_i /= s_i
            w_j /= s_j
            w1 = wasserstein_1(nb_i, w_i, nb_j, w_j, D)
            kappa[(i, j)] = 1.0 - w1 / d_ij
    return kappa


def compute_OR_potential_weighted(adj, n, phi):
    """
    Ollivier-Ricci on effective metric: edge distance = 1 + Phi_avg(e).
    The gravitational potential stretches/compresses the effective geometry.
    Uses uniform measures but weighted graph distances.
    """
    # Build effective edge weights: d_eff(i,j) = 1 + phi_avg(i,j)
    # Ensure all weights are positive
    phi_min = phi.min()
    offset = max(0.0, -phi_min + 0.01)  # ensure positivity

    edge_weight = {}
    for i in range(n):
        for j in adj[i]:
            if i >= j:
                continue
            key = (i, j)
            phi_avg = 0.5 * (phi[i] + phi[j])
            edge_weight[key] = 1.0 + phi_avg + offset

    # Weighted all-pairs shortest paths
    D_w = all_pairs_dijkstra(adj, edge_weight, n)

    kappa = {}
    for i in range(n):
        for j in adj[i]:
            if i >= j:
                continue
            key = (i, j)
            d_ij = edge_weight[key]
            if d_ij < 1e-15:
                continue
            nb_i = adj[i]
            nb_j = adj[j]
            m_i = len(nb_i)
            m_j = len(nb_j)
            w_i = np.ones(m_i) / m_i
            w_j = np.ones(m_j) / m_j
            w1 = wasserstein_1(nb_i, w_i, nb_j, w_j, D_w)
            kappa[(i, j)] = 1.0 - w1 / d_ij

    return kappa


# ── Self-consistent gravity evolution ─────────────────────────────

def evolve_with_gravity(pos, col, adj, n, G, L_csr):
    """Evolve N_STEPS with self-consistent gravity. Return final psi, phi."""
    solve_op = (L_csr + MU2 * speye(n, format='csr')).tocsc()
    psi = make_gaussian(pos, n)
    phi = np.zeros(n)

    for step in range(N_STEPS):
        rho = np.abs(psi)**2
        phi = spsolve(solve_op, G * rho)
        H = build_hamiltonian(pos, col, adj, n, phi)
        psi = cn_step(psi, H, DT)
        psi /= np.linalg.norm(psi)

    return psi, phi


def get_edges(adj, n):
    edges = []
    for i in range(n):
        for j in adj[i]:
            if i < j:
                edges.append((i, j))
    return edges


# ═══════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════

def main():
    t0 = time.time()

    print("=" * 78)
    print("POTENTIAL-WEIGHTED OLLIVIER CURVATURE vs STRESS-ENERGY PROXY")
    print("Does self-consistent gravity induce a bounded Delta_kappa ~ G*T proxy?")
    print("=" * 78)
    print()
    print(f"Lattice: {SIDE}x{SIDE} periodic staggered (n={SIDE**2})")
    print(f"MASS={MASS}, MU2={MU2}, DT={DT}, N_STEPS={N_STEPS}")
    print(f"G values: {G_VALUES}")
    print()

    n, pos, adj, col = build_lattice_2d(SIDE)
    L = build_laplacian(adj, n)
    edges = get_edges(adj, n)
    n_edges = len(edges)
    print(f"Graph: {n} nodes, {n_edges} edges")

    # ── All-pairs BFS (unweighted baseline) ───────────────────────
    print("Computing all-pairs BFS distances...")
    D0 = all_pairs_bfs(adj, n)

    # ── Step 1: Curvature BEFORE gravity ──────────────────────────
    print("Computing Ollivier-Ricci curvature BEFORE gravity (uniform, flat)...")
    kappa_before = compute_OR_uniform(adj, n, D0)
    kb_vals = np.array([kappa_before[e] for e in edges])
    print(f"  kappa_before: mean={kb_vals.mean():.6f}, std={kb_vals.std():.6f}")
    print(f"  (On a regular torus, kappa=0 everywhere by symmetry.)")
    print()

    # ── Sweep G values ────────────────────────────────────────────
    print("=" * 78)
    print("SWEEP OVER G VALUES — THREE CURVATURE METHODS")
    print("=" * 78)

    methods = ['density', 'potential', 'combined']
    all_results = {m: {} for m in methods}

    for G in G_VALUES:
        print(f"\n{'='*40} G = {G} {'='*40}")
        tg = time.time()

        psi_final, phi_final = evolve_with_gravity(pos, col, adj, n, G, L)
        rho = np.abs(psi_final)**2
        print(f"  Evolved {N_STEPS} steps ({time.time()-tg:.1f}s)")
        print(f"  rho: mean={rho.mean():.6f}, std={rho.std():.6f}, "
              f"max/mean={rho.max()/rho.mean():.2f}")
        print(f"  phi: mean={phi_final.mean():.6f}, std={phi_final.std():.6f}")

        T_vals = np.array([0.5 * (rho[i] + rho[j]) for (i, j) in edges])

        # Method (a): Density-weighted measures, flat metric
        ka_density = compute_OR_density_weighted(adj, n, D0, rho)
        dk_density = np.array([ka_density[e] - kappa_before[e] for e in edges])

        # Method (b): Uniform measures, potential-weighted metric
        ka_potential = compute_OR_potential_weighted(adj, n, phi_final)
        dk_potential = np.array([ka_potential[e] - kappa_before[e] for e in edges])

        # Method (c): Density-weighted measures, potential-weighted metric
        phi_min = phi_final.min()
        offset = max(0.0, -phi_min + 0.01)
        ew = {}
        for i in range(n):
            for j in adj[i]:
                if i >= j:
                    continue
                ew[(i, j)] = 1.0 + 0.5 * (phi_final[i] + phi_final[j]) + offset
        D_w = all_pairs_dijkstra(adj, ew, n)
        ka_combined = {}
        for i in range(n):
            for j in adj[i]:
                if i >= j:
                    continue
                key = (i, j)
                d_ij = ew[key]
                nb_i, nb_j = adj[i], adj[j]
                w_i = np.array([rho[v] for v in nb_i])
                w_j = np.array([rho[v] for v in nb_j])
                s_i, s_j = w_i.sum(), w_j.sum()
                if s_i < 1e-30 or s_j < 1e-30:
                    ka_combined[key] = 0.0
                    continue
                w_i /= s_i
                w_j /= s_j
                w1 = wasserstein_1(nb_i, w_i, nb_j, w_j, D_w)
                ka_combined[key] = 1.0 - w1 / d_ij
        dk_combined = np.array([ka_combined[e] - kappa_before[e] for e in edges])

        for label, dk_vals in [('density', dk_density),
                               ('potential', dk_potential),
                               ('combined', dk_combined)]:
            GT_vals = G * T_vals
            mask = np.isfinite(dk_vals) & np.isfinite(GT_vals)
            dk_f = dk_vals[mask]
            GT_f = GT_vals[mask]
            T_f = T_vals[mask]

            if len(dk_f) > 2 and np.std(GT_f) > 1e-15:
                res_GT = linregress(GT_f, dk_f)
                r2_GT = res_GT.rvalue**2
                slope_GT = res_GT.slope
            else:
                r2_GT, slope_GT = 0.0, 0.0

            if len(dk_f) > 2 and np.std(T_f) > 1e-15:
                res_T = linregress(T_f, dk_f)
                r2_T = res_T.rvalue**2
                slope_T = res_T.slope
            else:
                r2_T, slope_T = 0.0, 0.0

            all_results[label][G] = {
                'dk': dk_vals, 'T': T_vals, 'GT': GT_vals,
                'slope_GT': slope_GT, 'r2_GT': r2_GT,
                'slope_T': slope_T, 'r2_T': r2_T,
                'dk_mean': dk_vals.mean(), 'dk_std': dk_vals.std(),
            }

            print(f"  [{label:>10s}]  mean_dk={dk_vals.mean():+.4f}  "
                  f"R2(dk,GT)={r2_GT:.4f}  R2(dk,T)={r2_T:.4f}  "
                  f"slope_T={slope_T:.4f}")

    # ═══════════════════════════════════════════════════════════════
    # SUMMARY TABLE
    # ═══════════════════════════════════════════════════════════════
    print("\n" + "=" * 78)
    print("SUMMARY TABLE")
    print("=" * 78)

    for method in methods:
        print(f"\n--- Method: {method} ---")
        print(f"{'G':>5s}  {'slope(dk,GT)':>14s}  {'R2(dk,GT)':>10s}  "
              f"{'slope(dk,T)':>14s}  {'R2(dk,T)':>10s}")
        print("-" * 60)

        slopes_T = []
        for G in G_VALUES:
            r = all_results[method][G]
            slopes_T.append(r['slope_T'])
            print(f"{G:>5d}  {r['slope_GT']:>14.6f}  {r['r2_GT']:>10.4f}  "
                  f"{r['slope_T']:>14.6f}  {r['r2_T']:>10.4f}")

        G_arr = np.array(G_VALUES, dtype=float)
        slopes_arr = np.array(slopes_T)
        if np.std(G_arr) > 0 and np.std(slopes_arr) > 1e-15:
            meta = linregress(G_arr, slopes_arr)
            print(f"  slope_T vs G:  slope={meta.slope:.6f}  "
                  f"intercept={meta.intercept:.6f}  R2={meta.rvalue**2:.4f}")
        print()

    # ═══════════════════════════════════════════════════════════════
    # VERDICT
    # ═══════════════════════════════════════════════════════════════
    print("=" * 78)
    print("VERDICT")
    print("=" * 78)
    print()

    best_method = None
    best_score = -1

    for method in methods:
        r2s = [all_results[method][G]['r2_GT'] for G in G_VALUES]
        mean_r2 = np.mean(r2s)

        slopes_T = [all_results[method][G]['slope_T'] for G in G_VALUES]
        G_arr = np.array(G_VALUES, dtype=float)
        slopes_arr = np.array(slopes_T)
        if np.std(slopes_arr) > 1e-15:
            meta = linregress(G_arr, slopes_arr)
            meta_r2 = meta.rvalue**2
        else:
            meta_r2 = 0.0

        score = mean_r2 + meta_r2
        print(f"  {method:>10s}:  mean_R2(dk,GT)={mean_r2:.4f}  "
              f"R2(slope_T vs G)={meta_r2:.4f}  score={score:.4f}")

        if score > best_score:
            best_score = score
            best_method = method

    print(f"\n  Best method: {best_method}")
    print()

    # Final assessment using best method
    r2s = [all_results[best_method][G]['r2_GT'] for G in G_VALUES]
    mean_r2 = np.mean(r2s)
    slopes_T = [all_results[best_method][G]['slope_T'] for G in G_VALUES]
    meta = linregress(np.array(G_VALUES, dtype=float), np.array(slopes_T))
    meta_r2 = meta.rvalue**2

    if mean_r2 > 0.5 and meta_r2 > 0.8:
        print("  STRONG PROXY EVIDENCE: Delta_kappa ~ G*T on the")
        print("  potential-weighted Ollivier metric.")
    elif mean_r2 > 0.3 or meta_r2 > 0.5:
        print("  MODERATE PROXY EVIDENCE: partial curvature-stress-energy")
        print("  correlation on the potential-weighted observable.")
    else:
        print("  WEAK/NO EVIDENCE: this proxy does not track G*T cleanly.")

    # Diagnostic: is the SIGN correct?
    # In GR, positive energy density causes positive curvature.
    # Check: where T is large, is Delta_kappa positive or negative?
    print("\n  Sign check (does positive T give positive Delta_kappa?):")
    for method in methods:
        for G in [10, 50]:
            r = all_results[method][G]
            high_T = r['T'] > np.median(r['T'])
            dk_high = r['dk'][high_T].mean()
            dk_low = r['dk'][~high_T].mean()
            print(f"    {method:>10s} G={G:>2d}: dk(high_T)={dk_high:+.4f}  "
                  f"dk(low_T)={dk_low:+.4f}  "
                  f"{'correct' if dk_high > dk_low else 'WRONG sign'}")

    elapsed = time.time() - t0
    print(f"\n  Total time: {elapsed:.1f}s")

    # ── Plot ───────────────────────────────────────────────────────
    try:
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt

        fig, axes = plt.subplots(3, len(G_VALUES), figsize=(4*len(G_VALUES), 12))
        fig.suptitle('Ollivier-Ricci Curvature vs Einstein Equation\n'
                     r'$\Delta\kappa$ vs $G \cdot T$ for three curvature methods',
                     fontsize=14, fontweight='bold')

        for row, method in enumerate(methods):
            for col_idx, G in enumerate(G_VALUES):
                ax = axes[row, col_idx]
                r = all_results[method][G]
                ax.scatter(r['GT'], r['dk'], alpha=0.4, s=12, c='steelblue')

                if r['r2_GT'] > 0:
                    x_line = np.linspace(r['GT'].min(), r['GT'].max(), 50)
                    ax.plot(x_line,
                            r['slope_GT'] * x_line + (r['dk'].mean() - r['slope_GT'] * r['GT'].mean()),
                            'r-', linewidth=2)

                ax.set_title(f'{method} G={G}\nR2={r["r2_GT"]:.3f}', fontsize=9)
                if col_idx == 0:
                    ax.set_ylabel(r'$\Delta\kappa$')
                if row == 2:
                    ax.set_xlabel(r'$G \cdot T$')

        plt.tight_layout()
        out_path = __file__.replace('.py', '.png')
        plt.savefig(out_path, dpi=150)
        print(f"\nPlot saved to {out_path}")

        # Second plot: slope_T vs G for each method
        fig2, axes2 = plt.subplots(1, 3, figsize=(15, 5))
        fig2.suptitle(r'Does slope($\Delta\kappa$ vs T) scale linearly with G?',
                      fontsize=13, fontweight='bold')

        for idx, method in enumerate(methods):
            ax = axes2[idx]
            slopes = [all_results[method][G]['slope_T'] for G in G_VALUES]
            ax.plot(G_VALUES, slopes, 'ko-', markersize=8)

            G_arr = np.array(G_VALUES, dtype=float)
            slopes_arr = np.array(slopes)
            if np.std(slopes_arr) > 1e-15:
                meta = linregress(G_arr, slopes_arr)
                G_line = np.linspace(0, max(G_VALUES), 50)
                ax.plot(G_line, meta.slope * G_line + meta.intercept,
                        'r--', linewidth=2,
                        label=f'R2={meta.rvalue**2:.3f}')
            ax.set_xlabel('G')
            ax.set_ylabel(r'slope($\Delta\kappa$ vs T)')
            ax.set_title(f'{method}')
            ax.legend()

        plt.tight_layout()
        out2 = __file__.replace('.py', '_slopes.png')
        plt.savefig(out2, dpi=150)
        print(f"Slope plot saved to {out2}")

    except Exception as e:
        print(f"\nPlot generation failed: {e}")

    print("\nDone.")


if __name__ == '__main__':
    main()
