#!/usr/bin/env python3
"""Boundary-law unscreened recheck: mu^2=0.001 (screening length ~31.6 sites).

The original boundary_law_robustness test used mu^2=0.22 (screening length ~2.13
sites). At that screening length the Poisson potential decays within ~2 lattice
spacings, so the boundary-law result could be a screening artifact rather than a
genuine property of the self-consistent gravity.

This script reruns the SAME test at mu^2=0.001 where the screening length is
sqrt(1/0.001) ~ 31.6 sites -- far larger than any lattice tested -- so the
gravitational potential is effectively unscreened across the full lattice.

Checks:
  1. Boundary-law fit S = alpha * |dA| + const  (R^2 > 0.95?)
  2. Coefficient alpha_gravity vs alpha_random (Anderson disorder, matched variance)
  3. Sigma-separation between gravity and random alpha distributions
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

# ---------------------------------------------------------------------------
# Physical parameters
# ---------------------------------------------------------------------------
MASS = 0.30
MU2 = 0.001          # screening length sqrt(1/0.001) ~ 31.6 sites
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
    """Build a 2D periodic square lattice with optional position jitter."""
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
    """Planar cut at ix < cut_x. Returns (A_nodes, boundary_edges)."""
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


# ---------------------------------------------------------------------------
# Hamiltonian and evolution
# ---------------------------------------------------------------------------

def solve_poisson(adj: dict, n: int, rho: np.ndarray, mu2: float,
                  G: float) -> np.ndarray:
    """Solve screened Poisson (L + mu^2 I) Phi = G * rho on the graph."""
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

    for i, nbs in adj.items():
        for j in nbs:
            if i >= j:
                continue
            d = math.hypot(pos[j, 0] - pos[i, 0], pos[j, 1] - pos[i, 1])
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
        phi = solve_poisson(adj, n, rho, mu2=MU2, G=G)
        H = build_hamiltonian(n, pos, adj, col, phi)
        psi = cn_step(psi, H, DT)
        psi /= np.linalg.norm(psi)
        H_final = H

    return psi, H_final


def build_anderson_H(n: int, pos: np.ndarray, adj: dict, col: np.ndarray,
                     phi_variance: float, seed: int) -> sparse.csc_matrix:
    """Build Hamiltonian with Anderson disorder matching gravity phi variance."""
    rng = np.random.default_rng(seed + 10000)
    phi_random = rng.normal(0.0, np.sqrt(phi_variance), size=n)

    H = sparse.lil_matrix((n, n), dtype=complex)
    par = np.where(col == 0, 1.0, -1.0)
    H.setdiag((MASS + phi_random) * par)

    for i, nbs in adj.items():
        for j in nbs:
            if i >= j:
                continue
            d = math.hypot(pos[j, 0] - pos[i, 0], pos[j, 1] - pos[i, 1])
            d = min(d, 2.0)
            w = 1.0 / max(d, 0.5)
            H[i, j] += -0.5j * w
            H[j, i] += 0.5j * w

    return H.tocsc()


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
    print("BOUNDARY-LAW UNSCREENED RECHECK")
    print("mu^2 = 0.001 (screening length ~ 31.6 sites)")
    print("=" * 80)
    print()
    print(f"Parameters: MASS={MASS}, MU2={MU2}, DT={DT}, N_STEPS={N_STEPS}")
    print(f"Screening length: sqrt(1/MU2) = {1.0/np.sqrt(MU2):.1f} sites")
    print(f"Sides: {SIDES}  (all << screening length)")
    print(f"Seeds: {SEEDS} (jitter={JITTER})")
    print(f"G values: {G_VALUES}")
    print()

    # ===================================================================
    # SECTION 1: BFS-ball boundary law -- gravity vs Anderson disorder
    # ===================================================================
    print("=" * 80)
    print("SECTION 1: BFS-ball S vs |boundary| -- gravity vs Anderson disorder")
    print("=" * 80)

    # results[(side, G)] = list of (alpha, r2) over seeds
    grav_results: dict[tuple[int, int], list[tuple[float, float]]] = defaultdict(list)
    rand_results: dict[tuple[int, int], list[tuple[float, float]]] = defaultdict(list)

    for side in SIDES:
        for G in G_VALUES:
            for seed in SEEDS:
                n, pos, adj, col = build_lattice_2d(side, seed=seed, jitter=JITTER)
                center = (side // 2) * side + (side // 2)

                # --- Gravity ---
                psi, H_grav = evolve_and_get_final_H(n, pos, adj, col, float(G))
                C_grav, _, n_filled = dirac_sea_correlation_matrix(H_grav)

                # Measure phi variance for matched Anderson disorder
                rho = np.abs(psi)**2
                phi_grav = solve_poisson(adj, n, rho, MU2, float(G))
                phi_var = np.var(phi_grav) if G > 0 else 0.01

                # --- Anderson disorder (matched variance) ---
                H_rand = build_anderson_H(n, pos, adj, col, phi_var, seed)
                C_rand, _, _ = dirac_sea_correlation_matrix(H_rand)

                max_R = side // 2 - 1
                radii = list(range(1, max_R + 1))

                bnds_g, S_g = [], []
                bnds_r, S_r = [], []

                for R in radii:
                    A_nodes, bnd_edges = bfs_ball(adj, center, R, n)
                    nA = len(A_nodes)
                    if nA == 0 or nA >= n:
                        continue
                    s_grav, _ = entanglement_entropy_from_C(C_grav, A_nodes)
                    s_rand, _ = entanglement_entropy_from_C(C_rand, A_nodes)
                    bnds_g.append(bnd_edges); S_g.append(s_grav)
                    bnds_r.append(bnd_edges); S_r.append(s_rand)

                alpha_g, _, r2_g, se_g = safe_linregress(bnds_g, S_g)
                alpha_r, _, r2_r, se_r = safe_linregress(bnds_r, S_r)

                grav_results[(side, G)].append((alpha_g, r2_g))
                rand_results[(side, G)].append((alpha_r, r2_r))

                print(f"  side={side:>2} G={G:>2} seed={seed}: "
                      f"grav alpha={alpha_g:.6f} R2={r2_g:.6f} | "
                      f"rand alpha={alpha_r:.6f} R2={r2_r:.6f}")

    # ===================================================================
    # SECTION 2: Summary tables
    # ===================================================================
    print("\n" + "=" * 80)
    print("SECTION 2: Summary -- gravity alpha and R^2")
    print("=" * 80)

    print(f"\n{'side':>4} {'G':>4} {'alpha_grav':>12} {'std':>10} "
          f"{'R2_grav':>10} {'alpha_rand':>12} {'R2_rand':>10} {'sigma_sep':>10}")
    print("-" * 85)

    for side in SIDES:
        for G in G_VALUES:
            gk = (side, G)
            rk = (side, G)
            if gk not in grav_results or len(grav_results[gk]) == 0:
                continue
            ag = np.array([x[0] for x in grav_results[gk]])
            rg = np.array([x[1] for x in grav_results[gk]])
            ar = np.array([x[0] for x in rand_results[rk]])
            rr = np.array([x[1] for x in rand_results[rk]])

            # Sigma separation of alpha_grav from alpha_rand
            pooled_std = np.sqrt((np.std(ag)**2 + np.std(ar)**2) / 2) if (np.std(ag) + np.std(ar)) > 1e-12 else 1e-12
            sigma_sep = abs(np.mean(ag) - np.mean(ar)) / pooled_std

            print(f"{side:>4} {G:>4} {np.mean(ag):>12.6f} {np.std(ag):>10.6f} "
                  f"{np.mean(rg):>10.6f} {np.mean(ar):>12.6f} "
                  f"{np.mean(rr):>10.6f} {sigma_sep:>10.2f}")

    # ===================================================================
    # SECTION 3: Planar partition cross-check
    # ===================================================================
    print("\n" + "=" * 80)
    print("SECTION 3: Planar partition cross-check (side=10, G=10)")
    print("=" * 80)

    test_side = 10
    test_G = 10.0
    planar_grav_alphas, planar_grav_r2s = [], []
    planar_rand_alphas, planar_rand_r2s = [], []

    for seed in SEEDS:
        n, pos, adj, col = build_lattice_2d(test_side, seed=seed, jitter=JITTER)
        psi, H_grav = evolve_and_get_final_H(n, pos, adj, col, test_G)
        C_grav, _, _ = dirac_sea_correlation_matrix(H_grav)

        rho = np.abs(psi)**2
        phi_grav = solve_poisson(adj, n, rho, MU2, test_G)
        phi_var = np.var(phi_grav)

        H_rand = build_anderson_H(n, pos, adj, col, phi_var, seed)
        C_rand, _, _ = dirac_sea_correlation_matrix(H_rand)

        bnds_g, S_g, bnds_r, S_r = [], [], [], []
        for cut_x in range(1, test_side):
            A_nodes, bnd = planar_partition(test_side, n, adj, cut_x)
            nA = len(A_nodes)
            if nA == 0 or nA >= n:
                continue
            sg, _ = entanglement_entropy_from_C(C_grav, A_nodes)
            sr, _ = entanglement_entropy_from_C(C_rand, A_nodes)
            bnds_g.append(bnd); S_g.append(sg)
            bnds_r.append(bnd); S_r.append(sr)

        ag, _, rg, _ = safe_linregress(bnds_g, S_g)
        ar, _, rr, _ = safe_linregress(bnds_r, S_r)
        planar_grav_alphas.append(ag); planar_grav_r2s.append(rg)
        planar_rand_alphas.append(ar); planar_rand_r2s.append(rr)
        print(f"  seed={seed}: grav alpha={ag:.6f} R2={rg:.6f} | "
              f"rand alpha={ar:.6f} R2={rr:.6f}")

    planar_grav_alphas = np.array(planar_grav_alphas)
    planar_rand_alphas = np.array(planar_rand_alphas)
    planar_grav_r2s = np.array(planar_grav_r2s)

    pooled = np.sqrt((np.std(planar_grav_alphas)**2 + np.std(planar_rand_alphas)**2) / 2)
    if pooled < 1e-12:
        pooled = 1e-12
    planar_sigma = abs(np.mean(planar_grav_alphas) - np.mean(planar_rand_alphas)) / pooled
    print(f"\n  Planar partition sigma-separation: {planar_sigma:.2f}")
    print(f"  Planar gravity R^2 mean: {np.mean(planar_grav_r2s):.6f}")

    # ===================================================================
    # SECTION 4: Overall verdict
    # ===================================================================
    print("\n\n" + "=" * 80)
    print("VERDICT")
    print("=" * 80)

    # Collect all gravity R^2 values (BFS-ball)
    all_grav_r2 = []
    all_grav_alpha = []
    all_rand_alpha = []
    for key, vals in grav_results.items():
        for alpha, r2 in vals:
            all_grav_r2.append(r2)
            all_grav_alpha.append(alpha)
    for key, vals in rand_results.items():
        for alpha, r2 in vals:
            all_rand_alpha.append(alpha)

    all_grav_r2 = np.array(all_grav_r2)
    all_grav_alpha = np.array(all_grav_alpha)
    all_rand_alpha = np.array(all_rand_alpha)

    total_configs = len(all_grav_r2)
    high_r2 = int(np.sum(all_grav_r2 > 0.95))
    very_high = int(np.sum(all_grav_r2 > 0.99))

    print(f"\n  Total (side, G, seed) configs tested: {total_configs}")
    print(f"  Configs with R^2 > 0.95: {high_r2} ({100*high_r2/max(total_configs,1):.1f}%)")
    print(f"  Configs with R^2 > 0.99: {very_high} ({100*very_high/max(total_configs,1):.1f}%)")
    print(f"  R^2 range: [{all_grav_r2.min():.6f}, {all_grav_r2.max():.6f}]")
    print(f"  R^2 mean +/- std: {all_grav_r2.mean():.6f} +/- {all_grav_r2.std():.6f}")

    # Alpha comparison (gravity vs random), excluding G=0
    mask_nonzero_G = []
    idx = 0
    for key, vals in grav_results.items():
        side, G = key
        for _ in vals:
            mask_nonzero_G.append(G > 0)
            idx += 1
    mask_nonzero_G = np.array(mask_nonzero_G)

    if np.any(mask_nonzero_G):
        ag_nz = all_grav_alpha[mask_nonzero_G]
        ar_nz = all_rand_alpha[mask_nonzero_G]
        pooled_std = np.sqrt((np.std(ag_nz)**2 + np.std(ar_nz)**2) / 2)
        if pooled_std < 1e-12:
            pooled_std = 1e-12
        overall_sigma = abs(np.mean(ag_nz) - np.mean(ar_nz)) / pooled_std

        print(f"\n  Alpha (G>0): gravity mean={np.mean(ag_nz):.6f}, "
              f"random mean={np.mean(ar_nz):.6f}")
        print(f"  Alpha sigma-separation (gravity vs random, G>0): {overall_sigma:.2f}")
    else:
        overall_sigma = 0.0

    # Comparison with original mu^2=0.22 result
    print(f"\n  --- Comparison with original test (mu^2=0.22) ---")
    print(f"  Original: 100/100 R^2>0.95, 2.7-sigma separation")
    print(f"  This test (mu^2={MU2}): {high_r2}/{total_configs} R^2>0.95, "
          f"{overall_sigma:.1f}-sigma separation")

    if high_r2 == total_configs and overall_sigma > 2.0:
        print(f"\n  ==> BOUNDARY LAW CONFIRMED at mu^2={MU2} (unscreened)")
        print(f"      Result is NOT a screening artifact.")
    elif high_r2 / max(total_configs, 1) > 0.9:
        print(f"\n  ==> Boundary law holds at mu^2={MU2}, but separation weakened")
        print(f"      Screening may partially enhance the original signal.")
    else:
        print(f"\n  ==> Boundary law DEGRADED at mu^2={MU2}")
        print(f"      Original result may be partly a screening artifact.")

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
        fig.suptitle('Boundary-Law Unscreened Recheck\n'
                     f'mu^2={MU2} (screening length={1/np.sqrt(MU2):.1f}), '
                     f'MASS={MASS}, {N_STEPS} CN steps, {len(SEEDS)} seeds',
                     fontsize=13)

        # --- Panel (a): alpha_grav vs side for each G ---
        ax = axes[0, 0]
        for G in G_VALUES:
            sides_plot, means, stds = [], [], []
            for side in SIDES:
                key = (side, G)
                if key in grav_results and len(grav_results[key]) > 0:
                    alphas = np.array([x[0] for x in grav_results[key]])
                    sides_plot.append(side)
                    means.append(np.mean(alphas))
                    stds.append(np.std(alphas))
            if len(sides_plot) > 0:
                ax.errorbar(sides_plot, means, yerr=stds, marker='o',
                            capsize=3, label=f'G={G}')
        ax.set_xlabel('Lattice side')
        ax.set_ylabel('Boundary-law coefficient alpha')
        ax.set_title('(a) Gravity alpha vs lattice size')
        ax.legend()

        # --- Panel (b): R^2 vs side for each G ---
        ax = axes[0, 1]
        for G in G_VALUES:
            sides_plot, means, stds = [], [], []
            for side in SIDES:
                key = (side, G)
                if key in grav_results and len(grav_results[key]) > 0:
                    r2s = np.array([x[1] for x in grav_results[key]])
                    sides_plot.append(side)
                    means.append(np.mean(r2s))
                    stds.append(np.std(r2s))
            if len(sides_plot) > 0:
                ax.errorbar(sides_plot, means, yerr=stds, marker='s',
                            capsize=3, label=f'G={G}')
        ax.set_xlabel('Lattice side')
        ax.set_ylabel('R^2 (S vs |boundary|)')
        ax.set_title('(b) R^2 stability')
        ax.axhline(0.95, color='gray', linestyle='--', alpha=0.5, label='R^2=0.95')
        ax.legend()

        # --- Panel (c): alpha gravity vs alpha random (G=10) ---
        ax = axes[1, 0]
        grav_means, rand_means = [], []
        for side in SIDES:
            key = (side, 10)
            if key in grav_results and len(grav_results[key]) > 0:
                ag = np.array([x[0] for x in grav_results[key]])
                ar = np.array([x[0] for x in rand_results[key]])
                grav_means.append(np.mean(ag))
                rand_means.append(np.mean(ar))
        if grav_means:
            ax.scatter(SIDES[:len(grav_means)], grav_means, marker='o',
                       color='blue', label='Gravity', s=60)
            ax.scatter(SIDES[:len(rand_means)], rand_means, marker='x',
                       color='red', label='Anderson random', s=60)
        ax.set_xlabel('Lattice side')
        ax.set_ylabel('Boundary-law coefficient alpha')
        ax.set_title('(c) Gravity vs Anderson disorder (G=10)')
        ax.legend()

        # --- Panel (d): sigma-separation vs G ---
        ax = axes[1, 1]
        g_plot, sigs = [], []
        for G in G_VALUES:
            if G == 0:
                continue
            ag_all, ar_all = [], []
            for side in SIDES:
                key = (side, G)
                if key in grav_results:
                    ag_all.extend([x[0] for x in grav_results[key]])
                    ar_all.extend([x[0] for x in rand_results[key]])
            if len(ag_all) > 1:
                ag_all = np.array(ag_all)
                ar_all = np.array(ar_all)
                ps = np.sqrt((np.std(ag_all)**2 + np.std(ar_all)**2) / 2)
                if ps < 1e-12:
                    ps = 1e-12
                sig = abs(np.mean(ag_all) - np.mean(ar_all)) / ps
                g_plot.append(G)
                sigs.append(sig)
        if g_plot:
            ax.bar(range(len(g_plot)), sigs, tick_label=[str(g) for g in g_plot],
                   color='darkgreen', alpha=0.7)
            ax.axhline(2.0, color='orange', linestyle='--', label='2-sigma')
            ax.axhline(3.0, color='red', linestyle='--', label='3-sigma')
        ax.set_xlabel('Gravitational coupling G')
        ax.set_ylabel('Sigma separation (grav vs random)')
        ax.set_title('(d) Alpha separation by G')
        ax.legend()

        plt.tight_layout()
        out_path = __file__.replace('.py', '.png')
        plt.savefig(out_path, dpi=150)
        print(f"\nPlot saved to {out_path}")
    except Exception as e:
        print(f"\nPlot generation failed: {e}")

    print("\nDone.")


if __name__ == '__main__':
    run_experiment()
