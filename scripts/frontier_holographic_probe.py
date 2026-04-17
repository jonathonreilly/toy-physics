#!/usr/bin/env python3
"""Boundary-law probe: does boundary-accessible information scale with area?

Tests whether the entanglement entropy of a Dirac-sea state on a 2D periodic
lattice scales with the boundary area (number of boundary edges) of a BFS-ball
region, rather than with the bulk volume (number of sites in the ball).

Method (Peschel 2003 correlation-matrix approach):
  1. Build staggered-fermion Hamiltonian with parity coupling on a 2D periodic
     lattice, evolve under self-gravity (screened Poisson, G=10).
  2. Diagonalise the final Hamiltonian; fill all negative-energy modes (Dirac sea).
  3. Build the one-body correlation matrix C[i,j] = sum_{filled k} phi_k(i)*conj(phi_k(j)).
  4. For a BFS-ball region A of radius R centred on the lattice, restrict C to A:
     C_A = C[A_nodes, A_nodes].
  5. Eigenvalues nu_k of C_A give the free-fermion entanglement entropy:
     S = -sum_k [nu_k * ln(nu_k) + (1-nu_k) * ln(1-nu_k)]
  6. The Schmidt rank is the number of eigenvalues significantly away from 0 and 1.

Sweeps R = 1..side/2 for sides 8, 10, 12, 14.
Compares S vs |boundary| (area law) and S vs |A| (volume law).
Repeats for G=0 as control.
"""

from __future__ import annotations

import math
import sys
import time
from collections import deque

import numpy as np
from scipy import sparse
from scipy.sparse import eye as speye
from scipy.sparse.linalg import spsolve
from scipy.stats import linregress

# ---------------------------------------------------------------------------
# Physical parameters
# ---------------------------------------------------------------------------
MASS = 0.30
MU2 = 0.22
DT = 0.12
G_SELF = 10.0
N_STEPS = 30
SIGMA = 1.5
SIDES = [8, 10, 12, 14]


# ---------------------------------------------------------------------------
# Lattice construction
# ---------------------------------------------------------------------------

def build_lattice_2d(side: int):
    """Build a 2D periodic square lattice.

    Returns (n, pos, adj, col) where col is checkerboard parity.
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

    return n, pos, adj, col


# ---------------------------------------------------------------------------
# BFS ball and boundary
# ---------------------------------------------------------------------------

def bfs_ball(adj: dict[int, list[int]], center: int, radius: int, n: int):
    """BFS ball of given radius from center.

    Returns (A_nodes, boundary_edges) where boundary_edges is the number
    of edges from A to complement B.
    """
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

    # Count boundary edges (edges from A to B)
    boundary_edges = 0
    for i in A_nodes:
        for j in adj[i]:
            if j not in A_set:
                boundary_edges += 1

    return A_nodes, boundary_edges


# ---------------------------------------------------------------------------
# Hamiltonian and evolution
# ---------------------------------------------------------------------------

def solve_poisson(adj: dict, n: int, rho: np.ndarray, mu2: float, G: float) -> np.ndarray:
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
    """Evolve Gaussian wavepacket under self-gravity, return final Hamiltonian.

    We need the final H (after the last self-gravity update) to define the
    Dirac sea.
    """
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
# Dirac sea correlation matrix
# ---------------------------------------------------------------------------

def dirac_sea_correlation_matrix(H: sparse.csc_matrix):
    """Diagonalise H, fill negative-energy modes, return correlation matrix C.

    C[i,j] = sum_{k: E_k < 0} phi_k(i) * conj(phi_k(j))
    """
    H_dense = H.toarray()
    # Ensure Hermitian
    H_dense = 0.5 * (H_dense + H_dense.conj().T)

    eigenvalues, eigenvectors = np.linalg.eigh(H_dense)
    # Fill negative-energy modes
    filled = eigenvalues < 0
    n_filled = np.sum(filled)

    if n_filled == 0:
        # If no negative eigenvalues, fill lowest half
        n_filled = len(eigenvalues) // 2
        filled = np.zeros(len(eigenvalues), dtype=bool)
        filled[:n_filled] = True

    # Correlation matrix: C = V_filled @ V_filled^dagger
    V = eigenvectors[:, filled]
    C = V @ V.conj().T

    return C, eigenvalues, n_filled


# ---------------------------------------------------------------------------
# Entanglement entropy from correlation matrix
# ---------------------------------------------------------------------------

def entanglement_entropy_from_C(C: np.ndarray, A_nodes: list[int]):
    """Compute free-fermion entanglement entropy from restricted correlation matrix.

    S = -sum_k [nu_k * ln(nu_k) + (1-nu_k) * ln(1-nu_k)]
    where nu_k are eigenvalues of C_A = C[A_nodes, A_nodes].

    Also returns:
      - Schmidt rank: number of nu_k significantly away from 0 and 1
      - The eigenvalues themselves
    """
    if len(A_nodes) == 0:
        return 0.0, 0, np.array([])

    ix = np.ix_(A_nodes, A_nodes)
    C_A = C[ix]

    # Ensure Hermitian
    C_A = 0.5 * (C_A + C_A.conj().T)

    nu = np.linalg.eigvalsh(C_A).real
    nu = np.clip(nu, 1e-15, 1.0 - 1e-15)

    S = -np.sum(nu * np.log(nu) + (1.0 - nu) * np.log(1.0 - nu))

    # Schmidt rank: eigenvalues significantly away from 0 and 1
    threshold = 1e-6
    schmidt_rank = np.sum((nu > threshold) & (nu < 1.0 - threshold))

    return float(S), int(schmidt_rank), nu


# ---------------------------------------------------------------------------
# Linear fitting
# ---------------------------------------------------------------------------

def safe_linregress(x, y):
    """Linear regression with fallback for degenerate cases."""
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    if len(x) < 2 or np.std(x) < 1e-12:
        return 0.0, np.mean(y), 0.0
    res = linregress(x, y)
    return res.slope, res.intercept, res.rvalue**2


# ---------------------------------------------------------------------------
# Main experiment
# ---------------------------------------------------------------------------

def run_experiment():
    print("=" * 80)
    print("HOLOGRAPHIC BOUNDARY-LAW PROBE")
    print("Does Dirac-sea entanglement scale more cleanly with boundary than volume?")
    print("=" * 80)
    print()
    print("Method: Dirac-sea correlation matrix (Peschel 2003)")
    print("  Fill negative-energy eigenstates of staggered-fermion H")
    print("  S = -sum [nu*ln(nu) + (1-nu)*ln(1-nu)] from C_A eigenvalues")
    print()
    print(f"Parameters: MASS={MASS}, MU2={MU2}, DT={DT}, G={G_SELF}, "
          f"N_STEPS={N_STEPS}")
    print(f"Lattice sides: {SIDES}")
    print()

    # Collect all data for fits
    all_data: dict[str, list[dict]] = {'grav': [], 'free': []}

    for side in SIDES:
        t0 = time.time()
        print(f"\n{'='*60}")
        print(f"  LATTICE SIDE = {side}  (n = {side**2})")
        print(f"{'='*60}")

        n, pos, adj, col = build_lattice_2d(side)
        center = (side // 2) * side + (side // 2)

        # Evolve under self-gravity and free
        print("  Evolving with self-gravity (G=10)...")
        psi_grav, H_grav = evolve_and_get_final_H(n, pos, adj, col, G_SELF)
        print("  Evolving free (G=0)...")
        psi_free, H_free = evolve_and_get_final_H(n, pos, adj, col, 0.0)

        # Dirac sea correlation matrices
        print("  Computing Dirac sea correlation matrices...")
        C_grav, eigs_grav, n_filled_g = dirac_sea_correlation_matrix(H_grav)
        C_free, eigs_free, n_filled_f = dirac_sea_correlation_matrix(H_free)

        print(f"  Filled modes: grav={n_filled_g}, free={n_filled_f}")
        print(f"  Energy range: grav=[{eigs_grav[0]:.4f}, {eigs_grav[-1]:.4f}], "
              f"free=[{eigs_free[0]:.4f}, {eigs_free[-1]:.4f}]")

        # Sweep R
        max_R = side // 2
        radii = list(range(1, max_R + 1))

        header = (f"  {'R':>3} {'|A|':>5} {'|bnd|':>5} "
                  f"{'S_grav':>10} {'rank_g':>6} "
                  f"{'S_free':>10} {'rank_f':>6} "
                  f"{'dS':>8}")
        print()
        print(header)
        print("  " + "-" * (len(header) - 2))

        for R in radii:
            A_nodes, bnd_edges = bfs_ball(adj, center, R, n)
            nA = len(A_nodes)

            if nA == 0 or nA >= n:
                continue

            S_g, rank_g, _ = entanglement_entropy_from_C(C_grav, A_nodes)
            S_f, rank_f, _ = entanglement_entropy_from_C(C_free, A_nodes)

            dS = S_g - S_f

            print(f"  {R:>3} {nA:>5} {bnd_edges:>5} "
                  f"{S_g:>10.4f} {rank_g:>6} "
                  f"{S_f:>10.4f} {rank_f:>6} "
                  f"{dS:>+8.4f}")

            all_data['grav'].append({
                'side': side, 'R': R, 'nA': nA, 'bnd': bnd_edges,
                'S': S_g, 'rank': rank_g,
            })
            all_data['free'].append({
                'side': side, 'R': R, 'nA': nA, 'bnd': bnd_edges,
                'S': S_f, 'rank': rank_f,
            })

        dt_sec = time.time() - t0
        print(f"\n  Elapsed: {dt_sec:.1f}s")

    # ------------------------------------------------------------------
    # Scaling analysis
    # ------------------------------------------------------------------
    print("\n\n" + "=" * 80)
    print("SCALING ANALYSIS: S vs |boundary| (area) and S vs |A| (volume)")
    print("=" * 80)

    for tag in ['grav', 'free']:
        label = "SELF-GRAVITY (G=10)" if tag == 'grav' else "FREE (G=0)"
        data = all_data[tag]

        if len(data) < 3:
            print(f"\n  {label}: insufficient data")
            continue

        bnd = np.array([d['bnd'] for d in data], dtype=float)
        vol = np.array([d['nA'] for d in data], dtype=float)
        S = np.array([d['S'] for d in data])
        ranks = np.array([d['rank'] for d in data], dtype=float)

        print(f"\n  --- {label} ---")

        # Entropy fits
        sl_b, int_b, r2_b = safe_linregress(bnd, S)
        sl_v, int_v, r2_v = safe_linregress(vol, S)

        print(f"  S vs |boundary|:  S = {sl_b:.6f} * bnd + {int_b:.4f}  "
              f"R^2 = {r2_b:.6f}")
        print(f"  S vs |A| (vol):   S = {sl_v:.6f} * vol + {int_v:.4f}  "
              f"R^2 = {r2_v:.6f}")

        if r2_b > r2_v:
            print(f"  ==> AREA LAW preferred (R^2_bnd={r2_b:.4f} > R^2_vol={r2_v:.4f})")
        else:
            print(f"  ==> VOLUME LAW preferred (R^2_vol={r2_v:.4f} > R^2_bnd={r2_b:.4f})")

        # Schmidt rank fits
        sl_rb, _, r2_rb = safe_linregress(bnd, ranks)
        sl_rv, _, r2_rv = safe_linregress(vol, ranks)

        print(f"\n  Schmidt rank vs |boundary|: slope={sl_rb:.4f}, R^2={r2_rb:.4f}")
        print(f"  Schmidt rank vs |A| (vol):  slope={sl_rv:.4f}, R^2={r2_rv:.4f}")

        if r2_rb > r2_rv:
            print(f"  ==> Rank scales with BOUNDARY")
        else:
            print(f"  ==> Rank scales with VOLUME")

        # Per-lattice-size fits
        print(f"\n  Per-lattice-size fits:")
        for side in SIDES:
            sd = [d for d in data if d['side'] == side]
            if len(sd) < 3:
                continue
            b = np.array([d['bnd'] for d in sd], dtype=float)
            v = np.array([d['nA'] for d in sd], dtype=float)
            s = np.array([d['S'] for d in sd])

            _, _, r2b = safe_linregress(b, s)
            _, _, r2v = safe_linregress(v, s)

            winner = "AREA" if r2b > r2v else "VOLUME"
            print(f"    side={side:>2}: R^2_bnd={r2b:.4f}, R^2_vol={r2v:.4f}  --> {winner}")

    # ------------------------------------------------------------------
    # Gravity modification
    # ------------------------------------------------------------------
    print("\n\n" + "=" * 80)
    print("GRAVITY EFFECT ON AREA-LAW COEFFICIENT")
    print("=" * 80)

    bnd_g = np.array([d['bnd'] for d in all_data['grav']], dtype=float)
    bnd_f = np.array([d['bnd'] for d in all_data['free']], dtype=float)
    S_g = np.array([d['S'] for d in all_data['grav']])
    S_f = np.array([d['S'] for d in all_data['free']])

    sl_g, _, _ = safe_linregress(bnd_g, S_g)
    sl_f, _, _ = safe_linregress(bnd_f, S_f)

    print(f"  Area-law coefficient (gravity): {sl_g:.6f}")
    print(f"  Area-law coefficient (free):    {sl_f:.6f}")

    if abs(sl_f) > 1e-12:
        ratio = sl_g / sl_f
        diff_pct = (sl_g - sl_f) / abs(sl_f) * 100
        print(f"  Ratio (gravity/free): {ratio:.4f}")
        print(f"  Difference: {diff_pct:+.2f}%")
    else:
        print(f"  Free coefficient too small for ratio")

    # Delta S statistics
    if len(all_data['grav']) == len(all_data['free']):
        dS_all = S_g - S_f
        print(f"\n  Delta S (grav - free) across all points:")
        print(f"    mean = {np.mean(dS_all):+.6f}")
        print(f"    std  = {np.std(dS_all):.6f}")
        print(f"    min  = {np.min(dS_all):+.6f}")
        print(f"    max  = {np.max(dS_all):+.6f}")

    # ------------------------------------------------------------------
    # Raw data table
    # ------------------------------------------------------------------
    print("\n\n" + "=" * 80)
    print("RAW DATA TABLE")
    print("=" * 80)
    print(f"{'side':>4} {'R':>3} {'|A|':>5} {'|bnd|':>5} "
          f"{'S_grav':>10} {'rk_g':>5} {'S_free':>10} {'rk_f':>5} {'dS':>10}")
    print("-" * 68)

    for i in range(len(all_data['grav'])):
        dg = all_data['grav'][i]
        df = all_data['free'][i]
        dS = dg['S'] - df['S']
        print(f"{dg['side']:>4} {dg['R']:>3} {dg['nA']:>5} {dg['bnd']:>5} "
              f"{dg['S']:>10.4f} {dg['rank']:>5} {df['S']:>10.4f} {df['rank']:>5} "
              f"{dS:>+10.4f}")

    # ------------------------------------------------------------------
    # Plot
    # ------------------------------------------------------------------
    try:
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt

        fig, axes = plt.subplots(2, 2, figsize=(14, 11))
        fig.suptitle('Holographic Principle Probe\n'
                     f'Staggered fermion, MASS={MASS}, G={G_SELF}, {N_STEPS} CN steps\n'
                     'Dirac-sea correlation matrix method',
                     fontsize=13)

        markers = {8: 'o', 10: 's', 12: '^', 14: 'D'}
        colors_g = {8: '#d62728', 10: '#e36553', 12: '#ff9896', 14: '#f5b7b1'}
        colors_f = {8: '#1f77b4', 10: '#5ba3cf', 12: '#aec7e8', 14: '#c6dbef'}

        # Panel (a): S vs |boundary|
        ax = axes[0, 0]
        for side in SIDES:
            dg = [d for d in all_data['grav'] if d['side'] == side]
            df_list = [d for d in all_data['free'] if d['side'] == side]
            bnd_g_s = [d['bnd'] for d in dg]
            bnd_f_s = [d['bnd'] for d in df_list]
            s_g_s = [d['S'] for d in dg]
            s_f_s = [d['S'] for d in df_list]

            ax.plot(bnd_g_s, s_g_s, marker=markers[side], color=colors_g[side],
                    label=f'G=10, L={side}', markersize=5, linewidth=1)
            ax.plot(bnd_f_s, s_f_s, marker=markers[side], color=colors_f[side],
                    label=f'G=0, L={side}', markersize=5, linewidth=1, linestyle='--')

        # Overall fit lines
        bnd_all_g = np.array([d['bnd'] for d in all_data['grav']], dtype=float)
        S_all_g = np.array([d['S'] for d in all_data['grav']])
        sl, inter, r2 = safe_linregress(bnd_all_g, S_all_g)
        xfit = np.linspace(bnd_all_g.min(), bnd_all_g.max(), 50)
        ax.plot(xfit, sl * xfit + inter, 'r-', alpha=0.4, linewidth=2,
                label=f'Grav fit R$^2$={r2:.3f}')

        bnd_all_f = np.array([d['bnd'] for d in all_data['free']], dtype=float)
        S_all_f = np.array([d['S'] for d in all_data['free']])
        sl, inter, r2 = safe_linregress(bnd_all_f, S_all_f)
        ax.plot(xfit, sl * xfit + inter, 'b-', alpha=0.4, linewidth=2,
                label=f'Free fit R$^2$={r2:.3f}')

        ax.set_xlabel('Boundary edges |bnd|')
        ax.set_ylabel('Entanglement entropy S')
        ax.set_title('(a) S vs boundary (area)')
        ax.legend(fontsize=6, ncol=2)

        # Panel (b): S vs |A| (volume)
        ax = axes[0, 1]
        for side in SIDES:
            dg = [d for d in all_data['grav'] if d['side'] == side]
            df_list = [d for d in all_data['free'] if d['side'] == side]
            v_g = [d['nA'] for d in dg]
            v_f = [d['nA'] for d in df_list]
            s_g_s = [d['S'] for d in dg]
            s_f_s = [d['S'] for d in df_list]

            ax.plot(v_g, s_g_s, marker=markers[side], color=colors_g[side],
                    label=f'G=10, L={side}', markersize=5, linewidth=1)
            ax.plot(v_f, s_f_s, marker=markers[side], color=colors_f[side],
                    label=f'G=0, L={side}', markersize=5, linewidth=1, linestyle='--')

        vol_all_g = np.array([d['nA'] for d in all_data['grav']], dtype=float)
        sl, inter, r2 = safe_linregress(vol_all_g, S_all_g)
        xfit_v = np.linspace(vol_all_g.min(), vol_all_g.max(), 50)
        ax.plot(xfit_v, sl * xfit_v + inter, 'r-', alpha=0.4, linewidth=2,
                label=f'Grav fit R$^2$={r2:.3f}')

        vol_all_f = np.array([d['nA'] for d in all_data['free']], dtype=float)
        sl, inter, r2 = safe_linregress(vol_all_f, S_all_f)
        ax.plot(xfit_v, sl * xfit_v + inter, 'b-', alpha=0.4, linewidth=2,
                label=f'Free fit R$^2$={r2:.3f}')

        ax.set_xlabel('Volume |A|')
        ax.set_ylabel('Entanglement entropy S')
        ax.set_title('(b) S vs volume')
        ax.legend(fontsize=6, ncol=2)

        # Panel (c): Schmidt rank vs |boundary|
        ax = axes[1, 0]
        for side in SIDES:
            dg = [d for d in all_data['grav'] if d['side'] == side]
            df_list = [d for d in all_data['free'] if d['side'] == side]
            bnd_g_s = [d['bnd'] for d in dg]
            bnd_f_s = [d['bnd'] for d in df_list]
            r_g = [d['rank'] for d in dg]
            r_f = [d['rank'] for d in df_list]

            ax.plot(bnd_g_s, r_g, marker=markers[side], color=colors_g[side],
                    label=f'G=10, L={side}', markersize=5, linewidth=1)
            ax.plot(bnd_f_s, r_f, marker=markers[side], color=colors_f[side],
                    label=f'G=0, L={side}', markersize=5, linewidth=1, linestyle='--')

        ax.set_xlabel('Boundary edges |bnd|')
        ax.set_ylabel('Schmidt rank')
        ax.set_title('(c) Schmidt rank vs boundary')
        ax.legend(fontsize=6, ncol=2)

        # Panel (d): Schmidt rank vs |A| (volume)
        ax = axes[1, 1]
        for side in SIDES:
            dg = [d for d in all_data['grav'] if d['side'] == side]
            df_list = [d for d in all_data['free'] if d['side'] == side]
            v_g = [d['nA'] for d in dg]
            v_f = [d['nA'] for d in df_list]
            r_g = [d['rank'] for d in dg]
            r_f = [d['rank'] for d in df_list]

            ax.plot(v_g, r_g, marker=markers[side], color=colors_g[side],
                    label=f'G=10, L={side}', markersize=5, linewidth=1)
            ax.plot(v_f, r_f, marker=markers[side], color=colors_f[side],
                    label=f'G=0, L={side}', markersize=5, linewidth=1, linestyle='--')

        ax.set_xlabel('Volume |A|')
        ax.set_ylabel('Schmidt rank')
        ax.set_title('(d) Schmidt rank vs volume')
        ax.legend(fontsize=6, ncol=2)

        plt.tight_layout()
        out_path = __file__.replace('.py', '.png')
        plt.savefig(out_path, dpi=150)
        print(f"\nPlot saved to {out_path}")
    except Exception as e:
        print(f"\nPlot generation failed: {e}")

    print("\nDone.")


if __name__ == '__main__':
    run_experiment()
