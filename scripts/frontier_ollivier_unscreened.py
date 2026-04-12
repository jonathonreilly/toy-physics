#!/usr/bin/env python3
"""
Low-Screening Ollivier-Ricci Curvature vs Stress-Energy Proxy
=============================================================

Reruns the Ollivier-Ricci curvature proxy at mu^2=0.001
(screening length ~31.6 sites) to test whether the screened torus result
survives into the long-screening regime.

Protocol on 2D staggered lattice (side=10):

1. Compute Ollivier-Ricci curvature kappa(e) BEFORE gravity (Phi=0).
2. For each G in [1, 5, 10, 20, 50]:
   (a) SELF-CONSISTENT: Evolve 30 steps with (L + mu^2 I) Phi = G rho,
       parity coupling, Crank-Nicolson. Compute potential-weighted
       Ollivier-Ricci curvature. Fit Delta_kappa vs G*T.
   (b) RANDOM-MATCHED: 10 random Phi fields with same mean/std as (a),
       evolve under fixed random Phi. Compute same curvature. Fit.

This runner only checks the random/unstructured-control separation. Structured
controls at the same mu^2 are handled in frontier_ollivier_control.py.
3. Report R^2 for self-consistent and random, plus separation ratio.

Parity coupling: par = where(col==0, 1, -1); H.diag = (MASS + phi) * par
Screened Poisson: (L + mu^2 I) Phi = G rho
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
MU2 = 0.001          # screening length = 1/sqrt(0.001) ~ 31.6 sites
DT = 0.12
N_STEPS = 30
SIGMA = 1.5
SIDE = 10

G_VALUES = [1, 5, 10, 20, 50]
N_RANDOM_SEEDS = 10


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


def build_hamiltonian(pos, col, adj, n, phi):
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


def cn_step(psi, H, dt):
    """Crank-Nicolson time step."""
    n = H.shape[0]
    ap = (speye(n, format='csc') + 1j * H * dt / 2).tocsc()
    am = speye(n, format='csr') - 1j * H * dt / 2
    return spsolve(ap, am.dot(psi))


def make_gaussian(pos, n):
    cx = (pos[:, 0].max() + pos[:, 0].min()) / 2
    cy = (pos[:, 1].max() + pos[:, 1].min()) / 2
    r2 = (pos[:, 0] - cx)**2 + (pos[:, 1] - cy)**2
    psi = np.exp(-r2 / (2 * SIGMA**2)).astype(complex)
    psi /= np.linalg.norm(psi)
    return psi


# ── Shortest paths ────────────────────────────────────────────────

def dijkstra(adj, edge_weight, src, n):
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


def bfs_distances(adj, src, n):
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


def all_pairs_bfs(adj, n):
    D = np.zeros((n, n), dtype=int)
    for i in range(n):
        D[i] = bfs_distances(adj, i, n)
    return D


# ── Wasserstein-1 distance ────────────────────────────────────────

def wasserstein_1(support_i, weights_i, support_j, weights_j, D):
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


# ── Ollivier-Ricci curvature ─────────────────────────────────────

def compute_OR_uniform(adj, n, D):
    """Standard Ollivier-Ricci with uniform measures on flat graph."""
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


def compute_OR_potential_weighted(adj, n, phi):
    """
    Ollivier-Ricci on effective metric: edge distance = 1 + Phi_avg(e).
    Uniform measures, weighted graph distances.
    """
    phi_min = phi.min()
    offset = max(0.0, -phi_min + 0.01)

    edge_weight = {}
    for i in range(n):
        for j in adj[i]:
            if i >= j:
                continue
            key = (i, j)
            phi_avg = 0.5 * (phi[i] + phi[j])
            edge_weight[key] = 1.0 + phi_avg + offset

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
            kappa[key] = 1.0 - w1 / d_ij

    return kappa


# ── Evolution ─────────────────────────────────────────────────────

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


# ── Analysis helper ───────────────────────────────────────────────

def analyze_curvature(kappa_after, kappa_before, edges, rho, G):
    """Compute R^2(Dk vs GT), R^2(Dk vs T), and slope."""
    T_vals = np.array([0.5 * (rho[i] + rho[j]) for (i, j) in edges])
    dk_vals = np.array([kappa_after[e] - kappa_before[e] for e in edges])
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

    return {
        'r2_GT': r2_GT, 'slope_GT': slope_GT,
        'r2_T': r2_T, 'slope_T': slope_T,
        'dk_mean': dk_vals.mean(), 'dk_std': dk_vals.std(),
        'dk': dk_vals, 'T': T_vals, 'GT': GT_vals,
    }


# ═══════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════

def main():
    t0 = time.time()

    screening_length = 1.0 / np.sqrt(MU2)

    print("=" * 78)
    print("LOW-SCREENING OLLIVIER-RICCI CURVATURE vs STRESS-ENERGY PROXY")
    print("Rerun at mu^2=0.001 (screening length ~31.6)")
    print("to test the long-screening regime against the screened torus result")
    print("=" * 78)
    print()
    print(f"Lattice: {SIDE}x{SIDE} periodic staggered (n={SIDE**2})")
    print(f"MASS={MASS}, MU2={MU2} (screening length={screening_length:.1f})")
    print(f"DT={DT}, N_STEPS={N_STEPS}")
    print(f"G values: {G_VALUES}")
    print(f"Random seeds per condition: {N_RANDOM_SEEDS}")
    print()

    n, pos, adj, col = build_lattice_2d(SIDE)
    L = build_laplacian(adj, n)
    edges = get_edges(adj, n)
    n_edges = len(edges)
    print(f"Graph: {n} nodes, {n_edges} edges")

    # Baseline curvature (flat, no gravity)
    print("Computing baseline curvature (flat graph, Phi=0)...")
    D0 = all_pairs_bfs(adj, n)
    kappa_before = compute_OR_uniform(adj, n, D0)
    kb_vals = np.array([kappa_before[e] for e in edges])
    print(f"  kappa_before: mean={kb_vals.mean():.6f}, std={kb_vals.std():.6f}")
    print()

    # Storage
    results_sc = {}
    results_rand = {}

    for G in G_VALUES:
        print(f"\n{'='*35} G = {G} {'='*35}")
        tg = time.time()

        # ── SELF-CONSISTENT ───────────────────────────────────────
        print("  [SELF-CONSISTENT] Evolving with self-consistent gravity...")
        psi_sc, phi_sc = evolve_with_gravity(pos, col, adj, n, G, L)
        rho_sc = np.abs(psi_sc)**2
        print(f"    rho: mean={rho_sc.mean():.6f}, std={rho_sc.std():.6f}")
        print(f"    phi: mean={phi_sc.mean():.6f}, std={phi_sc.std():.6f}")

        kappa_sc = compute_OR_potential_weighted(adj, n, phi_sc)
        res_sc = analyze_curvature(kappa_sc, kappa_before, edges, rho_sc, G)
        results_sc[G] = res_sc
        print(f"    R2(Dk,GT)={res_sc['r2_GT']:.4f}  "
              f"R2(Dk,T)={res_sc['r2_T']:.4f}  "
              f"slope_GT={res_sc['slope_GT']:.6f}")

        # ── RANDOM-MATCHED (10 seeds) ─────────────────────────────
        print(f"  [RANDOM-MATCHED] {N_RANDOM_SEEDS} random Phi samples "
              f"(same mean/std as self-consistent)...")
        r2_GT_list = []
        r2_T_list = []
        slope_GT_list = []

        phi_mean = phi_sc.mean()
        phi_std = phi_sc.std()

        for seed in range(N_RANDOM_SEEDS):
            rng = np.random.default_rng(seed + 1000)
            phi_rand = rng.normal(phi_mean, phi_std, size=n)

            psi_rand = make_gaussian(pos, n)
            for step in range(N_STEPS):
                H = build_hamiltonian(pos, col, adj, n, phi_rand)
                psi_rand = cn_step(psi_rand, H, DT)
                psi_rand /= np.linalg.norm(psi_rand)

            rho_rand = np.abs(psi_rand)**2

            kappa_rand = compute_OR_potential_weighted(adj, n, phi_rand)
            res_rand = analyze_curvature(
                kappa_rand, kappa_before, edges, rho_rand, G)
            r2_GT_list.append(res_rand['r2_GT'])
            r2_T_list.append(res_rand['r2_T'])
            slope_GT_list.append(res_rand['slope_GT'])

        results_rand[G] = {
            'r2_GT_mean': np.mean(r2_GT_list),
            'r2_GT_std': np.std(r2_GT_list),
            'r2_T_mean': np.mean(r2_T_list),
            'r2_T_std': np.std(r2_T_list),
            'slope_GT_mean': np.mean(slope_GT_list),
            'slope_GT_std': np.std(slope_GT_list),
        }
        print(f"    R2(Dk,GT)={np.mean(r2_GT_list):.4f} +/- {np.std(r2_GT_list):.4f}  "
              f"R2(Dk,T)={np.mean(r2_T_list):.4f} +/- {np.std(r2_T_list):.4f}")

        print(f"  G={G} done ({time.time()-tg:.1f}s)")

    # ═══════════════════════════════════════════════════════════════
    # SUMMARY TABLE
    # ═══════════════════════════════════════════════════════════════
    print("\n" + "=" * 78)
    print("SUMMARY TABLE: R^2(Delta_kappa vs G*T)")
    print(f"mu^2 = {MU2}  (screening length = {screening_length:.1f} sites)")
    print("=" * 78)
    print(f"\n{'G':>5s}  {'SELF-CONSIST':>14s}  {'RANDOM-MATCH':>20s}  {'RATIO':>8s}")
    print("-" * 60)

    for G in G_VALUES:
        sc_r2 = results_sc[G]['r2_GT']
        rm_r2 = results_rand[G]['r2_GT_mean']
        rm_std = results_rand[G]['r2_GT_std']
        ratio = sc_r2 / max(rm_r2, 1e-10)
        print(f"{G:>5d}  {sc_r2:>14.4f}  "
              f"{rm_r2:>8.4f} +/- {rm_std:.4f}  "
              f"{ratio:>8.1f}x")

    # ═══════════════════════════════════════════════════════════════
    # SLOPE SCALING: slope(Dk vs T) vs G
    # ═══════════════════════════════════════════════════════════════
    print("\n" + "=" * 78)
    print("SLOPE SCALING: slope(Delta_kappa vs T) vs G")
    print("=" * 78)

    G_arr = np.array(G_VALUES, dtype=float)

    slopes_sc = [results_sc[G]['slope_T'] for G in G_VALUES]
    slopes_sc_arr = np.array(slopes_sc)
    if np.std(slopes_sc_arr) > 1e-15:
        meta_sc = linregress(G_arr, slopes_sc_arr)
        meta_r2_sc = meta_sc.rvalue**2
    else:
        meta_r2_sc = 0.0
    print(f"  Self-consistent: R2(slope_T vs G) = {meta_r2_sc:.4f}")

    slopes_rm = [results_rand[G]['slope_GT_mean'] for G in G_VALUES]
    slopes_rm_arr = np.array(slopes_rm)
    if np.std(slopes_rm_arr) > 1e-15:
        meta_rm = linregress(G_arr, slopes_rm_arr)
        meta_r2_rm = meta_rm.rvalue**2
    else:
        meta_r2_rm = 0.0
    print(f"  Random-matched:  R2(slope_T vs G) = {meta_r2_rm:.4f}")

    # ═══════════════════════════════════════════════════════════════
    # OVERALL VERDICT
    # ═══════════════════════════════════════════════════════════════
    print("\n" + "=" * 78)
    print("VERDICT")
    print("=" * 78)

    sc_r2s = [results_sc[G]['r2_GT'] for G in G_VALUES]
    rm_r2s = [results_rand[G]['r2_GT_mean'] for G in G_VALUES]

    mean_sc = np.mean(sc_r2s)
    mean_rm = np.mean(rm_r2s)
    ratio_overall = mean_sc / max(mean_rm, 1e-10)

    print(f"\n  Mean R^2(Dk vs GT) across G values:")
    print(f"    SELF-CONSISTENT: {mean_sc:.4f}")
    print(f"    RANDOM-MATCHED:  {mean_rm:.4f}")
    print(f"    Separation ratio: {ratio_overall:.2f}x")
    print(f"    Slope scaling R2 (self-consistent): {meta_r2_sc:.4f}")

    # Sign check
    print("\n  Sign check (does positive T give positive Delta_kappa?):")
    for G in [10, 50]:
        r = results_sc[G]
        high_T = r['T'] > np.median(r['T'])
        dk_high = r['dk'][high_T].mean()
        dk_low = r['dk'][~high_T].mean()
        print(f"    G={G:>2d}: dk(high_T)={dk_high:+.6f}  "
              f"dk(low_T)={dk_low:+.6f}  "
              f"{'correct' if dk_high > dk_low else 'WRONG sign'}")

    # Comparison with screened result
    print("\n  Comparison with original screened run:")
    print(f"    Original mu^2=0.22 (screening length=2.13): R^2 ~ 0.97 per G")
    print(f"    This run mu^2={MU2} (screening length={screening_length:.1f}): "
          f"mean R^2 = {mean_sc:.4f}")

    if mean_sc > 0.5 and ratio_overall > 2.0:
        print("\n  RESULT: Signal survives at long screening length.")
        print("  Self-consistent Phi gives much higher R^2 than random controls.")
        print("  This does not by itself isolate dynamic backreaction;")
        print("  structured controls must be checked separately.")
    elif mean_sc > 0.3 and ratio_overall > 1.5:
        print("\n  RESULT: Moderate signal at long screening length.")
        print("  Self-consistent Phi gives higher R^2 than controls,")
        print("  but weaker than the heavily-screened case.")
    elif mean_sc < 0.1:
        print("\n  RESULT: Signal collapses without screening.")
        print("  The original R^2=0.97 was likely an artifact of heavy screening")
        print("  confining the potential to a ~2-site radius.")
    else:
        print(f"\n  RESULT: Ambiguous. Mean R^2={mean_sc:.4f}, ratio={ratio_overall:.2f}x")

    elapsed = time.time() - t0
    print(f"\n  Total time: {elapsed:.1f}s")

    # ── Plot ───────────────────────────────────────────────────────
    try:
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt

        fig, axes = plt.subplots(2, len(G_VALUES),
                                 figsize=(4 * len(G_VALUES), 8))
        fig.suptitle(
            f'Unscreened Ollivier-Ricci: mu^2={MU2} '
            f'(screening length={screening_length:.1f})\n'
            r'$\Delta\kappa$ vs $G \cdot T$: '
            r'Self-Consistent vs Random $\Phi$',
            fontsize=13, fontweight='bold')

        for col_idx, G in enumerate(G_VALUES):
            # Self-consistent row
            ax = axes[0, col_idx]
            r = results_sc[G]
            ax.scatter(r['GT'], r['dk'], alpha=0.4, s=12, c='steelblue')
            if r['r2_GT'] > 0:
                x_line = np.linspace(r['GT'].min(), r['GT'].max(), 50)
                sl = r['slope_GT']
                inter = r['dk'].mean() - sl * r['GT'].mean()
                ax.plot(x_line, sl * x_line + inter, 'r-', lw=2)
            ax.set_title(f'Self-Consist G={G}\nR2={r["r2_GT"]:.3f}', fontsize=9)
            if col_idx == 0:
                ax.set_ylabel(r'$\Delta\kappa$')

            # Random row
            ax2 = axes[1, col_idx]
            rm = results_rand[G]
            ax2.text(0.5, 0.5,
                     f'R2 = {rm["r2_GT_mean"]:.3f}\n+/- {rm["r2_GT_std"]:.3f}',
                     transform=ax2.transAxes, ha='center', va='center',
                     fontsize=14, fontweight='bold', color='firebrick')
            ax2.set_title(f'Random G={G}', fontsize=9)
            if col_idx == 0:
                ax2.set_ylabel(r'$\Delta\kappa$')
            ax2.set_xlabel(r'$G \cdot T$')

        plt.tight_layout()
        out_path = __file__.replace('.py', '.png')
        plt.savefig(out_path, dpi=150)
        print(f"\nPlot saved to {out_path}")

    except Exception as e:
        print(f"\nPlot generation failed: {e}")

    print("\nDone.")


if __name__ == '__main__':
    main()
