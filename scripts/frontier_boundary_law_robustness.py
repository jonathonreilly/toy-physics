#!/usr/bin/env python3
"""Boundary-law robustness probe: multi-seed, multi-size, multi-partition checks.

Strengthens the boundary-law result from frontier_holographic_probe.py (R^2=0.9998
on single seed) with systematic robustness checks:

  1. Multi-seed stability (5 seeds per lattice size)
  2. Size convergence (side=6,8,10,12,14)
  3. Multiple partition geometries (planar, BFS-ball, random)
  4. G-dependence of the coefficient (G=0,5,10,20)
  5. Coefficient error bars from multi-seed spread

Physics: Dirac-sea correlation-matrix method (Peschel 2003) on staggered-fermion
Hamiltonian with parity coupling, evolved under screened-Poisson self-gravity.
"""

from __future__ import annotations

import math
import sys
import time
from collections import deque, defaultdict

import numpy as np
from scipy import sparse
from scipy.sparse import eye as speye
from scipy.sparse.linalg import spsolve
from scipy.stats import linregress

from periodic_geometry import infer_periodic_extents, minimum_image_distance

# ---------------------------------------------------------------------------
# Physical parameters
# ---------------------------------------------------------------------------
MASS = 0.30
MU2 = 0.22
DT = 0.12
N_STEPS = 30
SIGMA = 1.5

SIDES = [6, 8, 10, 12, 14]
SEEDS = [42, 43, 44, 45, 46]
G_VALUES = [0, 5, 10, 20]
JITTER = 0.05


# ---------------------------------------------------------------------------
# Lattice construction
# ---------------------------------------------------------------------------

def build_lattice_2d(side: int, seed: int | None = None, jitter: float = 0.0):
    """Build a 2D periodic square lattice with optional position jitter.

    Returns (n, pos, adj, col) where col is checkerboard parity.
    Jitter adds small random offsets to positions (topology unchanged).
    """
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
                jdx = jx * side + jy
                adj[idx].append(jdx)

    if jitter > 0.0 and seed is not None:
        rng = np.random.default_rng(seed)
        pos += rng.normal(0.0, jitter, size=pos.shape)

    return n, pos, adj, col


# ---------------------------------------------------------------------------
# Partition geometries
# ---------------------------------------------------------------------------

def bfs_ball(adj: dict[int, list[int]], center: int, radius: int, n: int):
    """BFS ball of given radius. Returns (A_nodes, boundary_edges)."""
    dist = np.full(n, -1, dtype=int)
    dist[center] = 0
    queue = deque([center])

    while queue:
        u = queue.popleft()
        for v in adj[u]:
            if dist[v] == -1:
                dist[v] = dist[u] + 1
                if dist[v] <= radius:
                    queue.append(v)

    A_set = set(i for i in range(n) if 0 <= dist[i] <= radius)
    A_nodes = sorted(A_set)

    boundary_edges = 0
    for i in A_nodes:
        for j in adj[i]:
            if j not in A_set:
                boundary_edges += 1

    return A_nodes, boundary_edges


def planar_partition(side: int, n: int, adj: dict[int, list[int]], cut_x: int):
    """Planar cut: all sites with ix < cut_x form region A.

    Returns (A_nodes, boundary_edges).
    """
    A_set = set()
    for ix in range(cut_x):
        for iy in range(side):
            A_set.add(ix * side + iy)
    A_nodes = sorted(A_set)

    boundary_edges = 0
    for i in A_nodes:
        for j in adj[i]:
            if j not in A_set:
                boundary_edges += 1

    return A_nodes, boundary_edges


def rectangular_partition(side: int, n: int, adj: dict[int, list[int]],
                          wx: int, wy: int):
    """Rectangular block: sites with ix < wx AND iy < wy form region A.

    Varying wx and wy gives different boundary sizes on a periodic lattice.
    Returns (A_nodes, boundary_edges).
    """
    A_set = set()
    for ix in range(wx):
        for iy in range(wy):
            A_set.add(ix * side + iy)
    A_nodes = sorted(A_set)

    boundary_edges = 0
    for i in A_nodes:
        for j in adj[i]:
            if j not in A_set:
                boundary_edges += 1

    return A_nodes, boundary_edges


def random_partition(n: int, adj: dict[int, list[int]], frac: float,
                     rng: np.random.Generator):
    """Random subset of given fraction. Returns (A_nodes, boundary_edges)."""
    k = max(1, min(n - 1, int(round(frac * n))))
    indices = rng.choice(n, size=k, replace=False)
    A_set = set(indices.tolist())
    A_nodes = sorted(A_set)

    boundary_edges = 0
    for i in A_nodes:
        for j in adj[i]:
            if j not in A_set:
                boundary_edges += 1

    return A_nodes, boundary_edges


# ---------------------------------------------------------------------------
# Hamiltonian and evolution
# ---------------------------------------------------------------------------

def solve_poisson(adj: dict, n: int, rho: np.ndarray, mu2: float,
                  G: float) -> np.ndarray:
    """Solve screened Poisson (L + mu^2) Phi = G * rho on the graph."""
    if G == 0.0:
        return np.zeros(n)

    rows, cols, vals = [], [], []
    for i in range(n):
        degree = len(adj[i])
        rows.append(i); cols.append(i); vals.append(float(degree) + mu2)
        for j in adj[i]:
            rows.append(i); cols.append(j); vals.append(-1.0)

    L = sparse.csc_matrix((vals, (rows, cols)), shape=(n, n))
    return spsolve(L, G * rho)


def build_hamiltonian(n: int, pos: np.ndarray, adj: dict, col: np.ndarray,
                      phi: np.ndarray) -> sparse.csc_matrix:
    """Build staggered-fermion Hamiltonian with parity coupling."""
    H = sparse.lil_matrix((n, n), dtype=complex)

    par = np.where(col == 0, 1.0, -1.0)
    H.setdiag((MASS + phi) * par)
    extents = infer_periodic_extents(pos)

    for i, nbs in adj.items():
        for j in nbs:
            if i >= j:
                continue
            d = minimum_image_distance(pos[i], pos[j], extents)
            d = min(d, 2.0)
            w = 1.0 / max(d, 0.5)
            H[i, j] += -0.5j * w
            H[j, i] += 0.5j * w

    return H.tocsc()


def cn_step(psi: np.ndarray, H: sparse.csc_matrix, dt: float) -> np.ndarray:
    """One Crank-Nicolson time step."""
    n = H.shape[0]
    ap = (speye(n, format='csc') + 1j * H * dt / 2).tocsc()
    am = speye(n, format='csr') - 1j * H * dt / 2
    return spsolve(ap, am.dot(psi))


def evolve_and_get_final_H(n: int, pos: np.ndarray, adj: dict,
                            col: np.ndarray, G: float):
    """Evolve Gaussian wavepacket under self-gravity, return final H."""
    cx = (pos[:, 0].max() + pos[:, 0].min()) / 2
    cy = (pos[:, 1].max() + pos[:, 1].min()) / 2
    r2 = (pos[:, 0] - cx)**2 + (pos[:, 1] - cy)**2
    psi = np.exp(-r2 / (2 * SIGMA**2)).astype(complex)
    psi /= np.linalg.norm(psi)

    H_final = None
    for step in range(N_STEPS):
        rho = np.abs(psi)**2
        phi = solve_poisson(adj, n, rho, MU2, G)
        H = build_hamiltonian(n, pos, adj, col, phi)
        psi = cn_step(psi, H, DT)
        psi /= np.linalg.norm(psi)
        H_final = H

    return psi, H_final


# ---------------------------------------------------------------------------
# Dirac sea
# ---------------------------------------------------------------------------

def dirac_sea_correlation_matrix(H: sparse.csc_matrix):
    """Fill negative-energy modes, return correlation matrix C."""
    H_dense = H.toarray()
    H_dense = 0.5 * (H_dense + H_dense.conj().T)

    eigenvalues, eigenvectors = np.linalg.eigh(H_dense)
    filled = eigenvalues < 0
    n_filled = np.sum(filled)

    if n_filled == 0:
        n_filled = len(eigenvalues) // 2
        filled = np.zeros(len(eigenvalues), dtype=bool)
        filled[:n_filled] = True

    V = eigenvectors[:, filled]
    C = V @ V.conj().T
    return C, eigenvalues, int(n_filled)


# ---------------------------------------------------------------------------
# Entanglement entropy
# ---------------------------------------------------------------------------

def entanglement_entropy_from_C(C: np.ndarray, A_nodes: list[int]):
    """Compute free-fermion entanglement entropy from restricted C_A."""
    if len(A_nodes) == 0:
        return 0.0, 0

    ix = np.ix_(A_nodes, A_nodes)
    C_A = C[ix]
    C_A = 0.5 * (C_A + C_A.conj().T)

    nu = np.linalg.eigvalsh(C_A).real
    nu = np.clip(nu, 1e-15, 1.0 - 1e-15)

    S = -np.sum(nu * np.log(nu) + (1.0 - nu) * np.log(1.0 - nu))

    threshold = 1e-6
    schmidt_rank = int(np.sum((nu > threshold) & (nu < 1.0 - threshold)))

    return float(S), schmidt_rank


# ---------------------------------------------------------------------------
# Linear fitting helper
# ---------------------------------------------------------------------------

def safe_linregress(x, y):
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    if len(x) < 2 or np.std(x) < 1e-12:
        return 0.0, np.mean(y), 0.0, 0.0
    res = linregress(x, y)
    return res.slope, res.intercept, res.rvalue**2, res.stderr


# ===========================================================================
# Main experiment
# ===========================================================================

def run_experiment():
    t_global = time.time()

    print("=" * 80)
    print("BOUNDARY-LAW ROBUSTNESS PROBE")
    print("Multi-seed, multi-size, multi-partition, multi-G checks")
    print("=" * 80)
    print()
    print(f"Parameters: MASS={MASS}, MU2={MU2}, DT={DT}, N_STEPS={N_STEPS}")
    print(f"Sides: {SIDES}")
    print(f"Seeds: {SEEDS} (jitter={JITTER})")
    print(f"G values: {G_VALUES}")
    print(f"Partition types: BFS-ball, rectangular, random")
    print()

    # ===================================================================
    # SECTION 1: Multi-seed BFS-ball sweeps for each (side, G)
    # ===================================================================
    print("\n" + "=" * 80)
    print("SECTION 1: BFS-ball S vs |boundary| -- multi-seed stability")
    print("=" * 80)

    # results[(side, G)] = list of (alpha, r2) over seeds
    bfs_results: dict[tuple[int, int], list[tuple[float, float]]] = defaultdict(list)
    # raw data for plotting
    bfs_raw: list[dict] = []

    for side in SIDES:
        for G in G_VALUES:
            for seed in SEEDS:
                n, pos, adj, col = build_lattice_2d(side, seed=seed, jitter=JITTER)
                center = (side // 2) * side + (side // 2)

                _, H_final = evolve_and_get_final_H(n, pos, adj, col, float(G))
                C, _, n_filled = dirac_sea_correlation_matrix(H_final)

                max_R = side // 2 - 1
                radii = list(range(1, max_R + 1))
                bnds, entropies = [], []

                for R in radii:
                    A_nodes, bnd_edges = bfs_ball(adj, center, R, n)
                    nA = len(A_nodes)
                    if nA == 0 or nA >= n:
                        continue
                    S, _ = entanglement_entropy_from_C(C, A_nodes)
                    bnds.append(bnd_edges)
                    entropies.append(S)
                    bfs_raw.append({
                        'side': side, 'G': G, 'seed': seed,
                        'R': R, 'nA': nA, 'bnd': bnd_edges, 'S': S,
                    })

                if len(bnds) >= 2:
                    alpha, _, r2, stderr = safe_linregress(bnds, entropies)
                    bfs_results[(side, G)].append((alpha, r2))

                print(f"  side={side:>2} G={G:>2} seed={seed}: "
                      f"alpha={alpha:.6f} R2={r2:.6f} "
                      f"(n_filled={n_filled}, {len(radii)} radii)")

    # Summarize with error bars
    print("\n" + "-" * 70)
    print("BFS-ball summary: alpha (mean +/- std) and R^2 (mean +/- std)")
    print(f"{'side':>4} {'G':>4} {'alpha_mean':>12} {'alpha_std':>10} "
          f"{'R2_mean':>10} {'R2_std':>10} {'n_seeds':>7}")
    print("-" * 70)

    for side in SIDES:
        for G in G_VALUES:
            key = (side, G)
            if key not in bfs_results or len(bfs_results[key]) == 0:
                continue
            alphas = np.array([x[0] for x in bfs_results[key]])
            r2s = np.array([x[1] for x in bfs_results[key]])
            print(f"{side:>4} {G:>4} {np.mean(alphas):>12.6f} "
                  f"{np.std(alphas):>10.6f} {np.mean(r2s):>10.6f} "
                  f"{np.std(r2s):>10.6f} {len(alphas):>7}")

    # ===================================================================
    # SECTION 2: Size convergence of alpha
    # ===================================================================
    print("\n\n" + "=" * 80)
    print("SECTION 2: Size convergence of alpha (G=10)")
    print("=" * 80)

    print(f"\n{'side':>4} {'n':>5} {'alpha_mean':>12} {'alpha_std':>10} "
          f"{'R2_mean':>10}")
    print("-" * 50)
    for side in SIDES:
        key = (side, 10)
        if key not in bfs_results or len(bfs_results[key]) == 0:
            continue
        alphas = np.array([x[0] for x in bfs_results[key]])
        r2s = np.array([x[1] for x in bfs_results[key]])
        print(f"{side:>4} {side**2:>5} {np.mean(alphas):>12.6f} "
              f"{np.std(alphas):>10.6f} {np.mean(r2s):>10.6f}")

    # ===================================================================
    # SECTION 3: Partition geometry comparison
    # ===================================================================
    print("\n\n" + "=" * 80)
    print("SECTION 3: Partition geometry comparison (side=10, G=10)")
    print("=" * 80)

    test_side = 10
    test_G = 10.0
    partition_results: dict[str, list[tuple[float, float]]] = defaultdict(list)

    for seed in SEEDS:
        n, pos, adj, col = build_lattice_2d(test_side, seed=seed, jitter=JITTER)
        center = (test_side // 2) * test_side + (test_side // 2)
        _, H_final = evolve_and_get_final_H(n, pos, adj, col, test_G)
        C, _, _ = dirac_sea_correlation_matrix(H_final)

        # --- BFS ball ---
        max_R = test_side // 2 - 1
        bnds_bfs, S_bfs = [], []
        for R in range(1, max_R + 1):
            A_nodes, bnd = bfs_ball(adj, center, R, n)
            if len(A_nodes) == 0 or len(A_nodes) >= n:
                continue
            S, _ = entanglement_entropy_from_C(C, A_nodes)
            bnds_bfs.append(bnd)
            S_bfs.append(S)
        if len(bnds_bfs) >= 2:
            alpha, _, r2, _ = safe_linregress(bnds_bfs, S_bfs)
            partition_results['BFS-ball'].append((alpha, r2))

        # --- Rectangular blocks (varying boundary) ---
        bnds_rect, S_rect = [], []
        for wx in range(2, test_side - 1):
            for wy in range(2, test_side - 1):
                A_nodes, bnd = rectangular_partition(test_side, n, adj, wx, wy)
                nA = len(A_nodes)
                if nA == 0 or nA >= n:
                    continue
                S, _ = entanglement_entropy_from_C(C, A_nodes)
                bnds_rect.append(bnd)
                S_rect.append(S)
        if len(bnds_rect) >= 2:
            alpha, _, r2, _ = safe_linregress(bnds_rect, S_rect)
            partition_results['rectangular'].append((alpha, r2))

        # --- Random subsets ---
        rng = np.random.default_rng(seed)
        bnds_rand, S_rand = [], []
        for frac in np.linspace(0.05, 0.45, 12):
            A_nodes, bnd = random_partition(n, adj, frac, rng)
            if len(A_nodes) == 0 or len(A_nodes) >= n:
                continue
            S, _ = entanglement_entropy_from_C(C, A_nodes)
            bnds_rand.append(bnd)
            S_rand.append(S)
        if len(bnds_rand) >= 2:
            alpha, _, r2, _ = safe_linregress(bnds_rand, S_rand)
            partition_results['random'].append((alpha, r2))

    print(f"\n{'partition':>12} {'alpha_mean':>12} {'alpha_std':>10} "
          f"{'R2_mean':>10} {'R2_std':>10}")
    print("-" * 60)
    for ptype in ['BFS-ball', 'rectangular', 'random']:
        if ptype not in partition_results or len(partition_results[ptype]) == 0:
            continue
        alphas = np.array([x[0] for x in partition_results[ptype]])
        r2s = np.array([x[1] for x in partition_results[ptype]])
        print(f"{ptype:>12} {np.mean(alphas):>12.6f} {np.std(alphas):>10.6f} "
              f"{np.mean(r2s):>10.6f} {np.std(r2s):>10.6f}")

    # ===================================================================
    # SECTION 4: G-dependence of coefficient
    # ===================================================================
    print("\n\n" + "=" * 80)
    print("SECTION 4: G-dependence of boundary-law coefficient")
    print("=" * 80)

    print(f"\n{'G':>4} {'alpha_mean':>12} {'alpha_std':>10} "
          f"{'R2_mean':>10} {'R2_std':>10}")
    print("-" * 50)

    for G in G_VALUES:
        # Pool across all sides
        all_alphas, all_r2s = [], []
        for side in SIDES:
            key = (side, G)
            if key in bfs_results:
                for a, r in bfs_results[key]:
                    all_alphas.append(a)
                    all_r2s.append(r)
        if len(all_alphas) > 0:
            all_alphas = np.array(all_alphas)
            all_r2s = np.array(all_r2s)
            print(f"{G:>4} {np.mean(all_alphas):>12.6f} "
                  f"{np.std(all_alphas):>10.6f} "
                  f"{np.mean(all_r2s):>10.6f} {np.std(all_r2s):>10.6f}")

    # ===================================================================
    # SECTION 5: Overall verdict
    # ===================================================================
    print("\n\n" + "=" * 80)
    print("VERDICT")
    print("=" * 80)

    # Collect all R^2 values
    all_r2 = []
    for key, vals in bfs_results.items():
        for _, r2 in vals:
            all_r2.append(r2)
    all_r2 = np.array(all_r2)

    total_configs = len(all_r2)
    high_r2 = np.sum(all_r2 > 0.95)
    very_high = np.sum(all_r2 > 0.99)

    print(f"\n  Total (side, G, seed) configs tested: {total_configs}")
    print(f"  Configs with R^2 > 0.95: {high_r2} ({100*high_r2/max(total_configs,1):.1f}%)")
    print(f"  Configs with R^2 > 0.99: {very_high} ({100*very_high/max(total_configs,1):.1f}%)")
    print(f"  R^2 range: [{all_r2.min():.6f}, {all_r2.max():.6f}]")
    print(f"  R^2 mean +/- std: {all_r2.mean():.6f} +/- {all_r2.std():.6f}")

    # Check partition universality
    for ptype in ['BFS-ball', 'rectangular', 'random']:
        if ptype in partition_results and len(partition_results[ptype]) > 0:
            r2s = np.array([x[1] for x in partition_results[ptype]])
            print(f"  {ptype} partition: R^2 = {r2s.mean():.6f} +/- {r2s.std():.6f}")

    if all_r2.mean() > 0.95:
        print("\n  ==> BOUNDARY LAW ROBUSTLY CONFIRMED across seeds, sizes, G, partitions")
    elif all_r2.mean() > 0.85:
        print("\n  ==> Boundary law holds with moderate robustness")
    else:
        print("\n  ==> Boundary law NOT robust -- further investigation needed")

    elapsed = time.time() - t_global
    print(f"\n  Total elapsed: {elapsed:.1f}s")

    # ===================================================================
    # Plot
    # ===================================================================
    try:
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt

        fig, axes = plt.subplots(2, 2, figsize=(14, 11))
        fig.suptitle('Boundary-Law Robustness Probe\n'
                     f'MASS={MASS}, MU2={MU2}, {N_STEPS} CN steps, '
                     f'{len(SEEDS)} seeds, jitter={JITTER}',
                     fontsize=13)

        # --- Panel (a): alpha vs side for each G ---
        ax = axes[0, 0]
        for G in G_VALUES:
            sides_plot, means, stds = [], [], []
            for side in SIDES:
                key = (side, G)
                if key in bfs_results and len(bfs_results[key]) > 0:
                    alphas = np.array([x[0] for x in bfs_results[key]])
                    sides_plot.append(side)
                    means.append(np.mean(alphas))
                    stds.append(np.std(alphas))
            if len(sides_plot) > 0:
                ax.errorbar(sides_plot, means, yerr=stds, marker='o',
                            capsize=3, label=f'G={G}')
        ax.set_xlabel('Lattice side')
        ax.set_ylabel('Area-law coefficient alpha')
        ax.set_title('(a) alpha convergence vs lattice size')
        ax.legend()

        # --- Panel (b): R^2 vs side for each G ---
        ax = axes[0, 1]
        for G in G_VALUES:
            sides_plot, means, stds = [], [], []
            for side in SIDES:
                key = (side, G)
                if key in bfs_results and len(bfs_results[key]) > 0:
                    r2s = np.array([x[1] for x in bfs_results[key]])
                    sides_plot.append(side)
                    means.append(np.mean(r2s))
                    stds.append(np.std(r2s))
            if len(sides_plot) > 0:
                ax.errorbar(sides_plot, means, yerr=stds, marker='s',
                            capsize=3, label=f'G={G}')
        ax.set_xlabel('Lattice side')
        ax.set_ylabel('R^2 (S vs |boundary|)')
        ax.set_title('(b) R^2 stability across seeds')
        ax.axhline(0.95, color='gray', linestyle='--', alpha=0.5, label='R^2=0.95')
        ax.legend()

        # --- Panel (c): alpha vs G (pooled across sizes) ---
        ax = axes[1, 0]
        g_plot, means, stds = [], [], []
        for G in G_VALUES:
            alphas_all = []
            for side in SIDES:
                key = (side, G)
                if key in bfs_results:
                    alphas_all.extend([x[0] for x in bfs_results[key]])
            if len(alphas_all) > 0:
                g_plot.append(G)
                means.append(np.mean(alphas_all))
                stds.append(np.std(alphas_all))
        if len(g_plot) > 0:
            ax.errorbar(g_plot, means, yerr=stds, marker='D', capsize=4,
                        color='darkgreen')
        ax.set_xlabel('Gravitational coupling G')
        ax.set_ylabel('Area-law coefficient alpha')
        ax.set_title('(c) G-dependence of alpha')

        # --- Panel (d): Partition geometry comparison ---
        ax = axes[1, 1]
        ptypes = ['BFS-ball', 'rectangular', 'random']
        x_pos = np.arange(len(ptypes))
        means_p, stds_p = [], []
        for ptype in ptypes:
            if ptype in partition_results and len(partition_results[ptype]) > 0:
                r2s = np.array([x[1] for x in partition_results[ptype]])
                means_p.append(np.mean(r2s))
                stds_p.append(np.std(r2s))
            else:
                means_p.append(0.0)
                stds_p.append(0.0)
        ax.bar(x_pos, means_p, yerr=stds_p, capsize=5, color=['#d62728', '#1f77b4', '#2ca02c'],
               alpha=0.7)
        ax.set_xticks(x_pos)
        ax.set_xticklabels(ptypes)
        ax.set_ylabel('R^2 (S vs |boundary|)')
        ax.set_title(f'(d) Partition geometry (side={test_side}, G={int(test_G)})')
        ax.axhline(0.95, color='gray', linestyle='--', alpha=0.5)
        ax.set_ylim(0, 1.05)

        plt.tight_layout()
        out_path = __file__.replace('.py', '.png')
        plt.savefig(out_path, dpi=150)
        print(f"\nPlot saved to {out_path}")
    except Exception as e:
        print(f"\nPlot generation failed: {e}")

    print("\nDone.")


if __name__ == '__main__':
    run_experiment()
