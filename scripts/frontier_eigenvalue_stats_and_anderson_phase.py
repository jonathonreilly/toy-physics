#!/usr/bin/env python3
"""
Eigenvalue Statistics & Anderson-Gravity Phase Diagram
======================================================

Two experiments in one script:

Part 1 (Frontier #12): Poisson-to-Wigner-Dyson transition
  Does the staggered Hamiltonian with self-gravity transition from integrable
  (Poisson level statistics) to chaotic (GOE/GUE) as G increases?
  Diagnostic: <r> ratio and KS tests against Wigner surmise / Poisson.

Part 2 (Frontier #9): Anderson-Gravity Phase Diagram
  Map the (G, L) plane showing where self-gravity becomes distinguishable
  from Anderson disorder via boundary-law and sign-selectivity probes.
"""

from __future__ import annotations

import math
import time
from collections import deque

import numpy as np
from scipy import sparse
from scipy.sparse import eye as speye, lil_matrix
from scipy.sparse.linalg import spsolve
from scipy.stats import ks_2samp, linregress

# -- Physical parameters -----------------------------------------------
MASS = 0.30
MU2 = 0.22
DT = 0.12
N_STEPS = 30
SIGMA = 1.5


# -- Lattice ------------------------------------------------------------

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


# -- Hamiltonian and evolution ------------------------------------------

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
            d = math.hypot(pos[j, 0] - pos[i, 0], pos[j, 1] - pos[i, 1])
            d = min(d, 2.0)
            w = 1.0 / max(d, 0.5)
            H[i, j] += -0.5j * w
            H[j, i] += 0.5j * w

    return H.tocsc()


def cn_step(psi: np.ndarray, H: sparse.csc_matrix, dt: float) -> np.ndarray:
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


# -- BFS partition -------------------------------------------------------

def bfs_ball(adj: dict[int, list[int]], center: int, radius: int, n: int):
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
    boundary_edges = sum(
        1 for i in A_nodes for j in adj[i] if j not in A_set
    )
    return A_nodes, boundary_edges


def bfs_depth(adj: dict[int, list[int]], src: int, n: int):
    depth = np.full(n, np.inf)
    depth[src] = 0
    q = deque([src])
    while q:
        i = q.popleft()
        for j in adj[i]:
            if depth[j] == np.inf:
                depth[j] = depth[i] + 1
                q.append(j)
    return depth


# -- Self-gravity evolution ---------------------------------------------

def evolve_self_gravity(pos, col, adj, n, G, n_steps=N_STEPS):
    """Evolve under self-gravity, return final psi, final H, final phi."""
    psi = make_gaussian(pos, n)
    L = build_laplacian(adj, n)
    solve_op = (L + MU2 * speye(n, format='csr')).tocsc()

    phi = np.zeros(n)
    H = None
    for step in range(n_steps):
        rho = np.abs(psi)**2
        phi = spsolve(solve_op, G * rho)
        H = build_hamiltonian(pos, col, adj, n, phi)
        psi = cn_step(psi, H, DT)
        psi /= np.linalg.norm(psi)

    return psi, H, phi


# -- Spectrum unfolding --------------------------------------------------

def unfold(evals, window=10):
    """Unfold spectrum via local mean spacing."""
    n = len(evals)
    unfolded = np.zeros(n)
    for i in range(n):
        lo = max(0, i - window)
        hi = min(n, i + window + 1)
        local_mean = np.mean(np.diff(evals[lo:hi]))
        unfolded[i] = evals[i] / local_mean if local_mean > 0 else evals[i]
    spacings = np.diff(unfolded)
    spacings = spacings[spacings > 0]
    if len(spacings) == 0:
        return np.array([1.0])
    return spacings / np.mean(spacings)


def r_ratio(spacings):
    """Mean ratio of consecutive spacings. Poisson: 0.386, GOE: 0.530, GUE: 0.603."""
    if len(spacings) < 2:
        return 0.0
    ratios = []
    for i in range(len(spacings) - 1):
        s1, s2 = spacings[i], spacings[i + 1]
        if max(s1, s2) > 0:
            ratios.append(min(s1, s2) / max(s1, s2))
    return float(np.mean(ratios)) if ratios else 0.0


def wigner_surmise_samples(n_samples):
    """Generate samples from Wigner surmise P_W(s) = (pi/2) s exp(-pi s^2/4)."""
    # Inverse CDF: F(s) = 1 - exp(-pi s^2 /4), so s = sqrt(-4 ln(1-u)/pi)
    u = np.random.uniform(0, 1, n_samples)
    return np.sqrt(-4.0 * np.log(1.0 - u) / np.pi)


def poisson_samples(n_samples):
    """Generate samples from Poisson P_P(s) = exp(-s)."""
    return np.random.exponential(1.0, n_samples)


# -- Probes for Part 2 --------------------------------------------------

def dirac_sea_correlation_matrix(H: sparse.csc_matrix):
    H_dense = H.toarray()
    H_dense = 0.5 * (H_dense + H_dense.conj().T)
    eigenvalues, eigenvectors = np.linalg.eigh(H_dense)

    filled = eigenvalues < 0
    n_filled = int(np.sum(filled))
    if n_filled == 0:
        n_filled = len(eigenvalues) // 2
        filled = np.zeros(len(eigenvalues), dtype=bool)
        filled[:n_filled] = True

    V = eigenvectors[:, filled]
    C = V @ V.conj().T
    return C


def entanglement_entropy_from_C(C: np.ndarray, A_nodes: list[int]):
    if len(A_nodes) == 0:
        return 0.0
    ix = np.ix_(A_nodes, A_nodes)
    C_A = C[ix]
    C_A = 0.5 * (C_A + C_A.conj().T)
    nu = np.linalg.eigvalsh(C_A).real
    nu = np.clip(nu, 1e-15, 1.0 - 1e-15)
    S = -np.sum(nu * np.log(nu) + (1.0 - nu) * np.log(1.0 - nu))
    return float(S)


def measure_boundary_law(H: sparse.csc_matrix, adj: dict[int, list[int]],
                         n: int, side: int):
    C = dirac_sea_correlation_matrix(H)
    center = (side // 2) * side + (side // 2)
    max_R = side // 2 - 1

    bnds, entropies = [], []
    for R in range(1, max_R + 1):
        A_nodes, bnd_edges = bfs_ball(adj, center, R, n)
        if len(A_nodes) == 0 or len(A_nodes) >= n:
            continue
        S = entanglement_entropy_from_C(C, A_nodes)
        bnds.append(bnd_edges)
        entropies.append(S)

    if len(bnds) < 2:
        return 0.0, 0.0

    x = np.asarray(bnds, dtype=float)
    y = np.asarray(entropies, dtype=float)
    res = linregress(x, y)
    return res.slope, res.rvalue**2


def shell_force_toward(depth: np.ndarray, n: int,
                       psi: np.ndarray, phi: np.ndarray) -> bool:
    finite = depth[np.isfinite(depth)]
    max_d = int(np.max(finite)) if finite.size else 0
    if max_d <= 0:
        return False

    rho = np.abs(psi)**2
    rho_n = rho / np.sum(rho)
    shell_phi = np.zeros(max_d + 1)
    shell_count = np.zeros(max_d + 1)
    shell_prob = np.zeros(max_d + 1)

    for i in range(n):
        d = int(depth[i]) if np.isfinite(depth[i]) else -1
        if 0 <= d <= max_d:
            shell_phi[d] += phi[i]
            shell_prob[d] += rho_n[i]
            shell_count[d] += 1
    for d in range(max_d + 1):
        if shell_count[d] > 0:
            shell_phi[d] /= shell_count[d]

    grad = np.zeros(max_d + 1)
    for d in range(max_d + 1):
        if d == 0:
            grad[d] = shell_phi[0] - shell_phi[min(1, max_d)]
        elif d == max_d:
            grad[d] = shell_phi[d - 1] - shell_phi[d]
        else:
            grad[d] = 0.5 * (shell_phi[d - 1] - shell_phi[d + 1])

    force = float(np.sum(shell_prob * grad))
    return force > 0


def measure_sign_selectivity(pos, col, adj, n, side, phi_static, G_sign, n_iter=20):
    """Measure attract vs repulse toward-counts with a given static potential."""
    center_idx = (side // 2) * side + (side // 2)
    depth = bfs_depth(adj, center_idx, n)
    L = build_laplacian(adj, n)
    solve_op = (L + MU2 * speye(n, format='csr')).tocsc()

    results = {}
    for label, sign in [("attract", +1.0), ("repulse", -1.0)]:
        psi = make_gaussian(pos, n)
        tw = 0
        for step in range(n_iter):
            rho = np.abs(psi)**2

            if phi_static is not None:
                phi = sign * phi_static
            else:
                phi = sign * spsolve(solve_op, G_sign * rho)

            if shell_force_toward(depth, n, psi, phi):
                tw += 1

            H = build_hamiltonian(pos, col, adj, n, phi)
            psi = cn_step(psi, H, DT)

        results[label] = tw

    return results["attract"], results["repulse"]


# ========================================================================
# PART 1: Eigenvalue Statistics (Frontier #12)
# ========================================================================

def run_eigenvalue_statistics():
    print("=" * 78)
    print("PART 1: EIGENVALUE STATISTICS -- Poisson to Wigner-Dyson Transition")
    print("=" * 78)
    print()

    side = 10
    n = side * side
    G_values = [0, 1, 5, 10, 20, 50, 100]

    print(f"Lattice: {side}x{side} periodic staggered (n={n})")
    print(f"MASS={MASS}, MU2={MU2}, DT={DT}, N_STEPS={N_STEPS}")
    print(f"G values: {G_values}")
    print(f"Reference <r>: Poisson=0.386, GOE=0.530, GUE=0.603")
    print()

    n_lat, pos, adj, col = build_lattice_2d(side)

    header = (f"{'G':>6s}  {'<r>':>8s}  {'class':>10s}  "
              f"{'KS_wigner':>10s}  {'p_wigner':>10s}  "
              f"{'KS_poisson':>10s}  {'p_poisson':>10s}  "
              f"{'N_spacings':>10s}")
    print(header)
    print("-" * len(header))

    results_part1 = []
    np.random.seed(42)

    for G in G_values:
        t0 = time.time()

        psi, H_final, phi = evolve_self_gravity(pos, col, adj, n_lat, G)

        H_dense = H_final.toarray()
        H_dense = 0.5 * (H_dense + H_dense.conj().T)
        evals = np.linalg.eigvalsh(H_dense)
        evals = np.sort(evals)

        spacings = unfold(evals, window=10)
        r_val = r_ratio(spacings)

        wigner_ref = wigner_surmise_samples(max(len(spacings), 500))
        poisson_ref = poisson_samples(max(len(spacings), 500))

        ks_w, p_w = ks_2samp(spacings, wigner_ref)
        ks_p, p_p = ks_2samp(spacings, poisson_ref)

        if r_val < 0.44:
            cls = "Poisson"
        elif r_val < 0.50:
            cls = "trans"
        elif r_val < 0.57:
            cls = "GOE"
        else:
            cls = "GUE"

        elapsed = time.time() - t0
        print(f"{G:>6.0f}  {r_val:>8.4f}  {cls:>10s}  "
              f"{ks_w:>10.4f}  {p_w:>10.4f}  "
              f"{ks_p:>10.4f}  {p_p:>10.4f}  "
              f"{len(spacings):>10d}  ({elapsed:.1f}s)")

        results_part1.append({
            'G': G, 'r': r_val, 'class': cls,
            'ks_wigner': ks_w, 'p_wigner': p_w,
            'ks_poisson': ks_p, 'p_poisson': p_p,
            'spacings': spacings,
        })

    print()

    # Find transition point
    r_poisson = 0.386
    r_goe = 0.530
    r_mid = (r_poisson + r_goe) / 2
    crossed = False
    for res in results_part1:
        if res['r'] > r_mid and not crossed:
            print(f"  Transition: <r> crosses midpoint ({r_mid:.3f}) at G={res['G']}")
            crossed = True

    if not crossed:
        max_r = max(res['r'] for res in results_part1)
        print(f"  No clear transition: max <r>={max_r:.4f}, midpoint={r_mid:.3f}")

    # Summary
    print()
    print("  Interpretation:")
    r0 = results_part1[0]['r']
    r_last = results_part1[-1]['r']
    if r_last > r0 + 0.03:
        print(f"  <r> grows from {r0:.4f} (G=0) to {r_last:.4f} (G={G_values[-1]})")
        print("  Self-gravity pushes the spectrum toward quantum chaos.")
    elif abs(r_last - r0) < 0.03:
        print(f"  <r> remains near {r0:.4f} across all G -- no spectral transition.")
    else:
        print(f"  <r> decreases from {r0:.4f} to {r_last:.4f} -- unexpected.")

    return results_part1


# ========================================================================
# PART 2: Anderson-Gravity Phase Diagram (Frontier #9)
# ========================================================================

def run_anderson_phase_diagram():
    print()
    print()
    print("=" * 78)
    print("PART 2: ANDERSON-GRAVITY PHASE DIAGRAM")
    print("=" * 78)
    print()

    sides = [6, 8, 10, 12]
    G_values = [0.5, 1, 2, 5, 10, 20, 50]
    N_RANDOM_SEEDS = 5
    SIGN_ITER = 20

    print(f"Sides: {sides}")
    print(f"G values: {G_values}")
    print(f"Random disorder seeds: {N_RANDOM_SEEDS}")
    print(f"Sign iterations: {SIGN_ITER}")
    print()

    header = (f"{'side':>4s}  {'G':>6s}  "
              f"{'alpha_grav':>10s}  {'alpha_rand':>10s}  {'sigma_alpha':>11s}  "
              f"{'sign_grav':>9s}  {'sign_rand':>9s}  {'sigma_sign':>10s}  "
              f"{'grav_real':>9s}")
    print(header)
    print("-" * len(header))

    phase_map = []

    for side in sides:
        n, pos, adj, col = build_lattice_2d(side)

        for G in G_values:
            t0 = time.time()
            G_sign = G / 5.0

            # Self-gravity reference
            psi_grav, H_grav, phi_grav = evolve_self_gravity(pos, col, adj, n, G)
            alpha_grav, r2_grav = measure_boundary_law(H_grav, adj, n, side)

            tw_a_grav, tw_r_grav = measure_sign_selectivity(
                pos, col, adj, n, side,
                phi_static=None, G_sign=G_sign, n_iter=SIGN_ITER)
            sign_margin_grav = tw_a_grav - tw_r_grav

            # Random disorder controls
            phi_mean = float(np.mean(phi_grav))
            phi_std = float(np.std(phi_grav))

            rand_alphas = []
            rand_sign_margins = []

            for seed in range(N_RANDOM_SEEDS):
                rng = np.random.RandomState(seed + 200)
                phi_random = rng.normal(phi_mean, max(phi_std, 1e-10), n)

                H_rand = build_hamiltonian(pos, col, adj, n, phi_random)
                alpha_r, _ = measure_boundary_law(H_rand, adj, n, side)
                rand_alphas.append(alpha_r)

                tw_a_r, tw_r_r = measure_sign_selectivity(
                    pos, col, adj, n, side,
                    phi_static=phi_random, G_sign=G_sign, n_iter=SIGN_ITER)
                rand_sign_margins.append(tw_a_r - tw_r_r)

            rand_alphas = np.array(rand_alphas)
            rand_sign_margins = np.array(rand_sign_margins)

            # Sigma away
            def sigma_away(grav_val, rand_arr):
                std = rand_arr.std()
                if std < 1e-12:
                    return float('inf') if abs(grav_val - rand_arr.mean()) > 1e-12 else 0.0
                return abs(grav_val - rand_arr.mean()) / std

            sig_alpha = sigma_away(alpha_grav, rand_alphas)
            sig_sign = sigma_away(float(sign_margin_grav), rand_sign_margins)

            is_real = sig_alpha > 3.0 or sig_sign > 3.0
            marker = "YES" if is_real else "no"

            elapsed = time.time() - t0
            print(f"{side:>4d}  {G:>6.1f}  "
                  f"{alpha_grav:>10.4f}  {rand_alphas.mean():>10.4f}  {sig_alpha:>11.1f}  "
                  f"{sign_margin_grav:>+9d}  {rand_sign_margins.mean():>+9.1f}  {sig_sign:>10.1f}  "
                  f"{marker:>9s}  ({elapsed:.1f}s)")

            phase_map.append({
                'side': side, 'G': G, 'n': n,
                'alpha_grav': alpha_grav,
                'alpha_rand_mean': rand_alphas.mean(),
                'sigma_alpha': sig_alpha,
                'sign_margin_grav': sign_margin_grav,
                'sign_margin_rand_mean': rand_sign_margins.mean(),
                'sigma_sign': sig_sign,
                'is_real': is_real,
            })

    print()

    # Phase boundary summary
    print("=" * 78)
    print("PHASE BOUNDARY SUMMARY (sigma > 3 = gravity is real)")
    print("=" * 78)
    print()

    print(f"{'':>6s}", end="")
    for G in G_values:
        print(f"  G={G:<5.1f}", end="")
    print()

    for side in sides:
        print(f"L={side:<3d} ", end="")
        for G in G_values:
            entry = [p for p in phase_map if p['side'] == side and p['G'] == G][0]
            sig_max = max(entry['sigma_alpha'], entry['sigma_sign'])
            if entry['is_real']:
                print(f"  {sig_max:>5.1f}*", end="")
            else:
                print(f"  {sig_max:>5.1f} ", end="")
        print()

    print()
    print("  * = sigma > 3 (gravity distinguishable from Anderson disorder)")
    print()

    # Find approximate boundary
    for side in sides:
        entries = [p for p in phase_map if p['side'] == side]
        boundary_G = None
        for e in entries:
            if e['is_real']:
                boundary_G = e['G']
                break
        if boundary_G is not None:
            print(f"  L={side}: gravity becomes real at G >= {boundary_G}")
        else:
            print(f"  L={side}: gravity not distinguishable at any tested G")

    return phase_map


# ========================================================================
# PLOT
# ========================================================================

def make_plots(results_part1, phase_map):
    try:
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt

        fig, axes = plt.subplots(2, 2, figsize=(14, 11))
        fig.suptitle('Eigenvalue Statistics & Anderson-Gravity Phase Diagram',
                     fontsize=13, fontweight='bold')

        # (a) <r> vs G
        ax = axes[0, 0]
        Gs = [r['G'] for r in results_part1]
        rs = [r['r'] for r in results_part1]
        ax.plot(Gs, rs, 'o-', color='#d62728', linewidth=2, markersize=8)
        ax.axhline(0.386, color='blue', linestyle='--', alpha=0.6, label='Poisson (0.386)')
        ax.axhline(0.530, color='green', linestyle='--', alpha=0.6, label='GOE (0.530)')
        ax.axhline(0.603, color='orange', linestyle='--', alpha=0.6, label='GUE (0.603)')
        ax.set_xlabel('G (self-gravity coupling)')
        ax.set_ylabel('<r> ratio')
        ax.set_title('(a) Spectral <r> ratio vs G')
        ax.legend(fontsize=8)
        ax.set_xscale('symlog', linthresh=1)

        # (b) KS statistics vs G
        ax = axes[0, 1]
        ks_w = [r['ks_wigner'] for r in results_part1]
        ks_p = [r['ks_poisson'] for r in results_part1]
        ax.plot(Gs, ks_w, 's-', color='green', label='KS vs Wigner', linewidth=2)
        ax.plot(Gs, ks_p, 'o-', color='blue', label='KS vs Poisson', linewidth=2)
        ax.set_xlabel('G (self-gravity coupling)')
        ax.set_ylabel('KS statistic')
        ax.set_title('(b) KS distance from reference distributions')
        ax.legend(fontsize=8)
        ax.set_xscale('symlog', linthresh=1)

        # (c) Phase diagram heatmap (sigma_alpha)
        ax = axes[1, 0]
        sides = sorted(set(p['side'] for p in phase_map))
        G_vals = sorted(set(p['G'] for p in phase_map))
        sig_grid = np.zeros((len(sides), len(G_vals)))
        for p in phase_map:
            i = sides.index(p['side'])
            j = G_vals.index(p['G'])
            sig_grid[i, j] = p['sigma_alpha']

        im = ax.imshow(sig_grid, aspect='auto', origin='lower',
                       extent=[0, len(G_vals) - 1, 0, len(sides) - 1],
                       cmap='RdYlGn_r', vmin=0, vmax=10)
        ax.set_xticks(range(len(G_vals)))
        ax.set_xticklabels([f'{g:.1f}' for g in G_vals], fontsize=7)
        ax.set_yticks(range(len(sides)))
        ax.set_yticklabels([str(s) for s in sides])
        ax.set_xlabel('G')
        ax.set_ylabel('L (side)')
        ax.set_title('(c) sigma_alpha (boundary law)')
        plt.colorbar(im, ax=ax, label='sigma away')
        ax.contour(sig_grid, levels=[3.0], colors='white', linewidths=2,
                   extent=[0, len(G_vals) - 1, 0, len(sides) - 1])

        # (d) Phase diagram heatmap (sigma_sign)
        ax = axes[1, 1]
        sig_grid2 = np.zeros((len(sides), len(G_vals)))
        for p in phase_map:
            i = sides.index(p['side'])
            j = G_vals.index(p['G'])
            sig_grid2[i, j] = p['sigma_sign']

        im2 = ax.imshow(sig_grid2, aspect='auto', origin='lower',
                        extent=[0, len(G_vals) - 1, 0, len(sides) - 1],
                        cmap='RdYlGn_r', vmin=0, vmax=10)
        ax.set_xticks(range(len(G_vals)))
        ax.set_xticklabels([f'{g:.1f}' for g in G_vals], fontsize=7)
        ax.set_yticks(range(len(sides)))
        ax.set_yticklabels([str(s) for s in sides])
        ax.set_xlabel('G')
        ax.set_ylabel('L (side)')
        ax.set_title('(d) sigma_sign (sign selectivity)')
        plt.colorbar(im2, ax=ax, label='sigma away')
        ax.contour(sig_grid2, levels=[3.0], colors='white', linewidths=2,
                   extent=[0, len(G_vals) - 1, 0, len(sides) - 1])

        plt.tight_layout()
        out_path = __file__.replace('.py', '.png')
        plt.savefig(out_path, dpi=150)
        print(f"\nPlot saved to {out_path}")
    except Exception as e:
        print(f"\nPlot generation failed: {e}")


# ========================================================================
# MAIN
# ========================================================================

def main():
    t0 = time.time()

    results_part1 = run_eigenvalue_statistics()

    phase_map = run_anderson_phase_diagram()

    make_plots(results_part1, phase_map)

    elapsed = time.time() - t0
    print(f"\nTotal time: {elapsed:.1f}s")
    print("\nDone.")


if __name__ == '__main__':
    main()
