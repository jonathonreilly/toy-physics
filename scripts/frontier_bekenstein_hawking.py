#!/usr/bin/env python3
"""Bekenstein-Hawking entropy from self-gravity localization on a 2D lattice.

Tests whether the entanglement entropy of a Zeno-localized state scales with
its boundary area (Bekenstein-Hawking: S = alpha * |boundary|) rather than
its volume.

Protocol:
  1. On 2D periodic staggered lattices (side = 8, 10, 12, 14):
     a. Initialize Gaussian wavepacket at center, sigma=1.5
     b. Evolve 60 steps under self-gravity at G=100 (above G_Zeno ~ 49)
     c. Measure localization width w_final
     d. Define region A = BFS ball of radius R = ceil(w_final) around centroid
     e. Compute Dirac-sea entanglement entropy via correlation matrix method
     f. Record |A|, |boundary|, and S_A

  2. Vary G = [50, 75, 100, 150, 200, 300] to change localization radius.
     Stronger G -> tighter localization -> smaller "black hole"

  3. Bekenstein-Hawking prediction: S = alpha * |boundary| with alpha
     independent of G. If S ~ |boundary| with universal coefficient, that's
     BH entropy from lattice self-gravity.

  4. Check: S ~ |boundary|^p with p=1 (area law) vs sub-area or volume law.

PStack experiment: bekenstein-hawking-entropy
"""

from __future__ import annotations

import math
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
N_STEPS = 60
SIGMA = 1.5

G_VALUES = [50, 75, 100, 150, 200, 300]
SIDES = [8, 10, 12, 14]


# ---------------------------------------------------------------------------
# 2D periodic lattice
# ---------------------------------------------------------------------------

def build_lattice_2d(side: int):
    """Build a 2D periodic square lattice.

    Returns (n, pos, adj, col, L_sparse) where col is checkerboard parity.
    """
    n = side * side
    pos = np.zeros((n, 2))
    adj: dict[int, list[int]] = {i: [] for i in range(n)}
    col = np.zeros(n, dtype=int)

    rows_sp, cols_sp, vals_sp = [], [], []

    for ix in range(side):
        for iy in range(side):
            idx = ix * side + iy
            pos[idx] = (ix, iy)
            col[idx] = (ix + iy) % 2

            neighbors = []
            for dix, diy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                jx = (ix + dix) % side
                jy = (iy + diy) % side
                jdx = jx * side + jy
                neighbors.append(jdx)
            adj[idx] = neighbors

            deg = len(neighbors)
            rows_sp.append(idx); cols_sp.append(idx); vals_sp.append(-float(deg))
            for j in neighbors:
                rows_sp.append(idx); cols_sp.append(j); vals_sp.append(1.0)

    L = sparse.csc_matrix((vals_sp, (rows_sp, cols_sp)), shape=(n, n))
    return n, pos, adj, col, L


# ---------------------------------------------------------------------------
# BFS ball and boundary
# ---------------------------------------------------------------------------

def bfs_ball(adj: dict[int, list[int]], center: int, radius: int, n: int):
    """BFS ball of given radius from center.

    Returns (A_nodes sorted, boundary_edges count).
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

    boundary_edges = 0
    for i in A_nodes:
        for j in adj[i]:
            if j not in A_set:
                boundary_edges += 1

    return A_nodes, boundary_edges


# ---------------------------------------------------------------------------
# Hamiltonian and evolution
# ---------------------------------------------------------------------------

def solve_poisson(L_sp: sparse.csc_matrix, n: int, rho: np.ndarray,
                  mu2: float, G: float) -> np.ndarray:
    """Solve screened Poisson (L + mu^2) phi = G * rho on the graph."""
    A = (L_sp + mu2 * speye(n)).tocsc()
    return spsolve(A, G * rho)


def build_hamiltonian(n: int, adj: dict, col: np.ndarray,
                      phi: np.ndarray) -> sparse.csc_matrix:
    """Build staggered-fermion Hamiltonian with parity coupling.

    H[i,i] = (MASS + phi[i]) * par[i]   where par = +1 (even) / -1 (odd)
    H[i,j] = -i/2 for neighbors with j > i (antisymmetric hopping)
    """
    par = np.where(col == 0, 1.0, -1.0)
    diag = (MASS + phi) * par

    rows, cols_sp, vals = [], [], []
    for i in range(n):
        rows.append(i); cols_sp.append(i); vals.append(diag[i])
        for j in adj[i]:
            if j > i:
                rows.append(i); cols_sp.append(j); vals.append(-0.5j)
                rows.append(j); cols_sp.append(i); vals.append(0.5j)

    return sparse.csc_matrix((vals, (rows, cols_sp)), shape=(n, n), dtype=complex)


def cn_step(psi: np.ndarray, H: sparse.csc_matrix, dt: float,
            n: int) -> np.ndarray:
    """Crank-Nicolson step."""
    I = speye(n, dtype=complex, format="csc")
    A_plus = (I + 1j * H * dt / 2).tocsc()
    A_minus = I - 1j * H * dt / 2
    return spsolve(A_plus, A_minus.dot(psi))


# ---------------------------------------------------------------------------
# Wavepacket utilities
# ---------------------------------------------------------------------------

def gaussian_2d(pos: np.ndarray, center: np.ndarray, sigma: float,
                n: int) -> np.ndarray:
    """Normalized 2D Gaussian."""
    dx = pos[:, 0] - center[0]
    dy = pos[:, 1] - center[1]
    psi = np.exp(-0.5 * (dx**2 + dy**2) / sigma**2).astype(complex)
    psi /= np.sqrt(np.sum(np.abs(psi)**2))
    return psi


def rms_width(psi: np.ndarray, pos: np.ndarray) -> float:
    """RMS width of wavepacket."""
    prob = np.abs(psi)**2
    prob /= np.sum(prob)
    cx = np.sum(prob * pos[:, 0])
    cy = np.sum(prob * pos[:, 1])
    dx = pos[:, 0] - cx
    dy = pos[:, 1] - cy
    return float(np.sqrt(np.sum(prob * (dx**2 + dy**2))))


def centroid_idx(psi: np.ndarray, pos: np.ndarray) -> int:
    """Index of node closest to probability centroid."""
    prob = np.abs(psi)**2
    prob /= np.sum(prob)
    cx = np.sum(prob * pos[:, 0])
    cy = np.sum(prob * pos[:, 1])
    dists = (pos[:, 0] - cx)**2 + (pos[:, 1] - cy)**2
    return int(np.argmin(dists))


# ---------------------------------------------------------------------------
# Self-gravity evolution
# ---------------------------------------------------------------------------

def evolve_self_gravity(n: int, pos: np.ndarray, adj: dict,
                        col: np.ndarray, L_sp: sparse.csc_matrix,
                        G: float):
    """Evolve Gaussian wavepacket under self-gravity for N_STEPS.

    Returns (psi_final, H_final, w_init, w_final).
    """
    center = np.array([pos[:, 0].mean(), pos[:, 1].mean()])
    psi = gaussian_2d(pos, center, SIGMA, n)
    w_init = rms_width(psi, pos)

    H_final = None
    for step in range(N_STEPS):
        rho = np.abs(psi)**2
        phi = solve_poisson(L_sp, n, rho, MU2, G)
        H = build_hamiltonian(n, adj, col, phi)
        psi = cn_step(psi, H, DT, n)
        psi /= np.sqrt(np.sum(np.abs(psi)**2))
        H_final = H

    w_final = rms_width(psi, pos)
    return psi, H_final, w_init, w_final


# ---------------------------------------------------------------------------
# Dirac sea correlation matrix and entropy
# ---------------------------------------------------------------------------

def dirac_sea_correlation_matrix(H: sparse.csc_matrix):
    """Diagonalize H, fill negative-energy modes, return correlation matrix C.

    Returns (C, n_filled).
    """
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
    return C, n_filled


def entropy_from_C(C: np.ndarray, A_nodes: list[int]):
    """Compute entanglement entropy for region A from correlation matrix.

    Returns (S, schmidt_rank).
    """
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
# Linear fitting
# ---------------------------------------------------------------------------

def safe_linregress(x, y):
    """Linear regression with fallback."""
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    if len(x) < 2 or np.std(x) < 1e-12:
        return 0.0, np.mean(y), 0.0
    res = linregress(x, y)
    return res.slope, res.intercept, res.rvalue**2


def log_linregress(x, y):
    """Log-log regression for power law: y = a * x^p."""
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    mask = (x > 0) & (y > 0)
    if np.sum(mask) < 2:
        return 0.0, 0.0, 0.0
    lx = np.log(x[mask])
    ly = np.log(y[mask])
    if np.std(lx) < 1e-12:
        return 0.0, np.mean(ly), 0.0
    res = linregress(lx, ly)
    return res.slope, res.intercept, res.rvalue**2


# ---------------------------------------------------------------------------
# Main experiment
# ---------------------------------------------------------------------------

def main():
    print("=" * 80)
    print("BEKENSTEIN-HAWKING ENTROPY FROM SELF-GRAVITY LOCALIZATION")
    print("Does Zeno-localized state entropy scale with boundary area?")
    print("=" * 80)
    print()
    print("Method:")
    print("  1. Evolve Gaussian under self-gravity (G >> G_Zeno ~ 49)")
    print("  2. Packet localizes (Zeno freeze). Measure w_final.")
    print("  3. For each G, sweep region A = BFS ball of radius R=1..side/2-1")
    print("  4. Compute Dirac-sea entanglement entropy via correlation matrix")
    print("  5. Compare S vs |boundary| (area law) and S vs |A| (volume law)")
    print()
    print(f"Parameters: MASS={MASS}, MU2={MU2}, DT={DT}, "
          f"N_STEPS={N_STEPS}, SIGMA={SIGMA}")
    print(f"G values: {G_VALUES}")
    print(f"Lattice sides: {SIDES}")
    print()

    # ===================================================================
    # Part 1: Main data collection
    # For each (side, G): evolve, compute C once, then sweep R
    # ===================================================================
    all_data: list[dict] = []

    for side in SIDES:
        n, pos, adj, col, L_sp = build_lattice_2d(side)
        max_R = side // 2 - 1
        radii = list(range(1, max_R + 1))

        print(f"\n{'='*70}")
        print(f"  LATTICE SIDE = {side}  (n = {n}), R sweep: 1..{max_R}")
        print(f"{'='*70}")

        for G in G_VALUES:
            t0 = time.time()
            psi_f, H_f, w_init, w_final = evolve_self_gravity(
                n, pos, adj, col, L_sp, G
            )
            status = "FROZEN" if w_final < w_init * 1.05 else "SPREAD"

            # Compute correlation matrix once for this (side, G)
            C, n_filled = dirac_sea_correlation_matrix(H_f)
            c_idx = centroid_idx(psi_f, pos)

            print(f"\n  G={G}, w={w_final:.3f}/{w_init:.3f} ({status}), "
                  f"n_filled={n_filled}")
            print(f"  {'R':>3} {'|A|':>5} {'|bnd|':>5} {'S':>10} {'rank':>5}")
            print("  " + "-" * 38)

            for R in radii:
                A_nodes, bnd_edges = bfs_ball(adj, c_idx, R, n)
                nA = len(A_nodes)
                if nA == 0 or nA >= n:
                    continue

                S_val, srank = entropy_from_C(C, A_nodes)

                print(f"  {R:>3} {nA:>5} {bnd_edges:>5} {S_val:>10.4f} {srank:>5}")

                all_data.append({
                    'side': side, 'G': G, 'R': R,
                    'w_init': w_init, 'w_final': w_final,
                    'nA': nA, 'bnd': bnd_edges, 'S': S_val,
                    'rank': srank, 'n_filled': n_filled, 'status': status,
                })

            dt = time.time() - t0
            print(f"  ({dt:.1f}s)")

    # ===================================================================
    # Part 2: Scaling analysis
    # ===================================================================
    print("\n\n" + "=" * 80)
    print("SCALING ANALYSIS")
    print("=" * 80)

    if len(all_data) < 3:
        print("  Insufficient data for analysis.")
        return

    bnd = np.array([d['bnd'] for d in all_data], dtype=float)
    vol = np.array([d['nA'] for d in all_data], dtype=float)
    S = np.array([d['S'] for d in all_data])

    # 2a. Overall fits: S vs |boundary| and S vs |A|
    print("\n[2a] Overall linear fits (all sides, all G, all R):")
    sl_b, int_b, r2_b = safe_linregress(bnd, S)
    sl_v, int_v, r2_v = safe_linregress(vol, S)
    print(f"  S = {sl_b:.6f} * |boundary| + {int_b:.4f}    R^2 = {r2_b:.6f}")
    print(f"  S = {sl_v:.6f} * |A|        + {int_v:.4f}    R^2 = {r2_v:.6f}")

    if r2_b > r2_v:
        print(f"  ==> AREA LAW preferred (R^2_bnd > R^2_vol)")
    else:
        print(f"  ==> VOLUME LAW preferred (R^2_vol > R^2_bnd)")

    # 2b. Power-law fits: S ~ |boundary|^p
    print("\n[2b] Power-law fits (log-log):")
    p_bnd, _, r2_pb = log_linregress(bnd, S)
    p_vol, _, r2_pv = log_linregress(vol, S)
    print(f"  S ~ |boundary|^{p_bnd:.3f}   R^2(log) = {r2_pb:.4f}")
    print(f"  S ~ |A|^{p_vol:.3f}           R^2(log) = {r2_pv:.4f}")
    if abs(p_bnd - 1.0) < 0.2 and r2_pb > 0.8:
        print(f"  ==> BH area law (p ~ 1) confirmed")
    elif p_bnd < 0.8 and r2_pb > 0.7:
        print(f"  ==> Sub-area law (p < 1)")
    elif p_bnd > 1.2 and r2_pb > 0.7:
        print(f"  ==> Super-area law (p > 1)")
    else:
        print(f"  ==> Power law exponent: {p_bnd:.3f} (not clearly ~1)")

    # 2c. Per-G fits: S vs |boundary| at each G (sweeping R gives range)
    print("\n[2c] Per-G area-law coefficients (S = alpha * |bnd| + beta):")
    print(f"  {'G':>5} {'alpha':>10} {'beta':>8} {'R^2':>8} {'N_pts':>6}")
    print("  " + "-" * 45)

    alphas = []
    for G in G_VALUES:
        gdata = [d for d in all_data if d['G'] == G]
        if len(gdata) < 3:
            continue
        b_g = np.array([d['bnd'] for d in gdata], dtype=float)
        s_g = np.array([d['S'] for d in gdata])
        sl, inter, r2 = safe_linregress(b_g, s_g)
        alphas.append((G, sl, inter, r2, len(gdata)))
        print(f"  {G:>5} {sl:>10.6f} {inter:>8.4f} {r2:>8.4f} {len(gdata):>6}")

    alpha_mean = alpha_std = cv = 0.0
    if len(alphas) >= 2:
        alpha_vals = [a[1] for a in alphas]
        alpha_mean = np.mean(alpha_vals)
        alpha_std = np.std(alpha_vals)
        cv = alpha_std / abs(alpha_mean) if abs(alpha_mean) > 1e-12 else float('inf')
        print(f"\n  Alpha: mean={alpha_mean:.6f}, std={alpha_std:.6f}, CV={cv:.3f}")
        if cv < 0.3:
            print(f"  ==> BH UNIVERSAL COEFFICIENT: alpha ~ {alpha_mean:.4f} (CV < 0.3)")
        else:
            print(f"  ==> Alpha varies with G (CV = {cv:.2f}): NOT universal")

    # 2d. Per-side fits (all G pooled)
    print("\n[2d] Per-lattice-size fits (all G pooled):")
    for side in SIDES:
        sdata = [d for d in all_data if d['side'] == side]
        if len(sdata) < 3:
            continue
        b_s = np.array([d['bnd'] for d in sdata], dtype=float)
        v_s = np.array([d['nA'] for d in sdata], dtype=float)
        s_s = np.array([d['S'] for d in sdata])
        sl_bs, _, r2b = safe_linregress(b_s, s_s)
        sl_vs, _, r2v = safe_linregress(v_s, s_s)
        winner = "AREA" if r2b > r2v else "VOLUME"
        print(f"  side={side:>2}: R^2_bnd={r2b:.4f}, R^2_vol={r2v:.4f}  "
              f"alpha_bnd={sl_bs:.4f}  --> {winner}")

    # 2e. Per-(side, G) fits -- the real test
    print("\n[2e] Per-(side, G) fits -- individual runs:")
    print(f"  {'side':>4} {'G':>5} {'alpha':>10} {'R^2_bnd':>8} "
          f"{'R^2_vol':>8} {'winner':>8}")
    print("  " + "-" * 50)
    for side in SIDES:
        for G in G_VALUES:
            sgdata = [d for d in all_data
                      if d['side'] == side and d['G'] == G]
            if len(sgdata) < 3:
                continue
            b_sg = np.array([d['bnd'] for d in sgdata], dtype=float)
            v_sg = np.array([d['nA'] for d in sgdata], dtype=float)
            s_sg = np.array([d['S'] for d in sgdata])
            sl_sg, _, r2b_sg = safe_linregress(b_sg, s_sg)
            _, _, r2v_sg = safe_linregress(v_sg, s_sg)
            winner = "AREA" if r2b_sg > r2v_sg else "VOLUME"
            print(f"  {side:>4} {G:>5} {sl_sg:>10.6f} {r2b_sg:>8.4f} "
                  f"{r2v_sg:>8.4f} {winner:>8}")

    # ===================================================================
    # Part 3: Localization check
    # ===================================================================
    print("\n\n" + "=" * 80)
    print("LOCALIZATION CHECK")
    print("=" * 80)

    seen = set()
    n_frozen = 0
    n_total_sg = 0
    for d in all_data:
        key = (d['side'], d['G'])
        if key in seen:
            continue
        seen.add(key)
        n_total_sg += 1
        if d['status'] == 'FROZEN':
            n_frozen += 1
        ratio = d['w_final'] / d['w_init'] if d['w_init'] > 0 else 0
        print(f"  side={d['side']:>2}, G={d['G']:>3}: "
              f"w={d['w_final']:.3f}/{d['w_init']:.3f} = {ratio:.3f}  "
              f"{d['status']}")
    print(f"\n  Frozen: {n_frozen}/{n_total_sg}")

    # ===================================================================
    # Part 4: Raw data table (compact)
    # ===================================================================
    print("\n\n" + "=" * 80)
    print("RAW DATA TABLE")
    print("=" * 80)
    print(f"{'side':>4} {'G':>5} {'R':>3} {'|A|':>5} "
          f"{'|bnd|':>5} {'S':>10} {'rank':>5}")
    print("-" * 48)
    for d in all_data:
        print(f"{d['side']:>4} {d['G']:>5} {d['R']:>3} {d['nA']:>5} "
              f"{d['bnd']:>5} {d['S']:>10.4f} {d['rank']:>5}")

    # ===================================================================
    # Part 5: Summary
    # ===================================================================
    print("\n\n" + "=" * 80)
    print("SUMMARY: BEKENSTEIN-HAWKING TEST")
    print("=" * 80)

    print(f"\n  1. Area vs Volume law (overall, all data):")
    print(f"     S vs |boundary|:  R^2 = {r2_b:.4f}")
    print(f"     S vs |A| (vol):   R^2 = {r2_v:.4f}")
    if r2_b > r2_v + 0.05:
        print(f"     ==> AREA LAW (Bekenstein-Hawking scaling)")
    elif r2_v > r2_b + 0.05:
        print(f"     ==> VOLUME LAW (no BH scaling)")
    else:
        print(f"     ==> COMPARABLE (both R^2 close)")

    print(f"\n  2. Power-law exponent:")
    print(f"     S ~ |boundary|^{p_bnd:.3f}   (BH predicts p=1)")
    if abs(p_bnd - 1.0) < 0.2:
        print(f"     ==> Consistent with BH (p ~ 1)")
    else:
        print(f"     ==> Deviates from BH (p != 1)")

    if len(alphas) >= 2:
        print(f"\n  3. Universal coefficient:")
        print(f"     alpha = {alpha_mean:.4f} +/- {alpha_std:.4f} (CV = {cv:.3f})")
        if cv < 0.3:
            print(f"     ==> UNIVERSAL (Bekenstein-Hawking alpha = A/4)")
        else:
            print(f"     ==> G-DEPENDENT (not universal)")

    print(f"\n  4. Localization: {n_frozen}/{n_total_sg} cases frozen (Zeno)")

    # Overall verdict
    bh_score = 0
    if r2_b > r2_v:
        bh_score += 1
    if abs(p_bnd - 1.0) < 0.3:
        bh_score += 1
    if len(alphas) >= 2 and cv < 0.3:
        bh_score += 1
    if n_frozen > n_total_sg * 0.7:
        bh_score += 1

    print(f"\n  BH score: {bh_score}/4")
    if bh_score >= 3:
        print("  ==> STRONG EVIDENCE for Bekenstein-Hawking entropy")
    elif bh_score >= 2:
        print("  ==> MODERATE EVIDENCE for Bekenstein-Hawking entropy")
    elif bh_score >= 1:
        print("  ==> WEAK EVIDENCE for Bekenstein-Hawking entropy")
    else:
        print("  ==> NO EVIDENCE for Bekenstein-Hawking entropy")

    # ===================================================================
    # Part 6: Plot
    # ===================================================================
    try:
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt

        fig, axes = plt.subplots(2, 2, figsize=(14, 11))
        fig.suptitle(
            'Bekenstein-Hawking Entropy from Self-Gravity Localization\n'
            f'Staggered fermion, MASS={MASS}, MU2={MU2}, {N_STEPS} CN steps\n'
            'Dirac-sea correlation matrix method',
            fontsize=13
        )

        colors_G = {50: '#1f77b4', 75: '#ff7f0e', 100: '#2ca02c',
                     150: '#d62728', 200: '#9467bd', 300: '#8c564b'}
        markers_side = {8: 'o', 10: 's', 12: '^', 14: 'D'}

        # Panel (a): S vs |boundary|, colored by G
        ax = axes[0, 0]
        for G in G_VALUES:
            gd = [d for d in all_data if d['G'] == G]
            if not gd:
                continue
            b = [d['bnd'] for d in gd]
            s = [d['S'] for d in gd]
            ax.scatter(b, s, color=colors_G[G], label=f'G={G}', s=40,
                       zorder=3, alpha=0.7)

        # Overall fit line
        if np.std(bnd) > 1e-12:
            xfit = np.linspace(bnd.min(), bnd.max(), 50)
            ax.plot(xfit, sl_b * xfit + int_b, 'k--', alpha=0.5,
                    linewidth=1.5, label=f'Fit R$^2$={r2_b:.3f}')
        ax.set_xlabel('Boundary edges |bnd|')
        ax.set_ylabel('Entanglement entropy S')
        ax.set_title('(a) S vs boundary (area law test)')
        ax.legend(fontsize=7)

        # Panel (b): S vs |A| (volume), colored by G
        ax = axes[0, 1]
        for G in G_VALUES:
            gd = [d for d in all_data if d['G'] == G]
            if not gd:
                continue
            v = [d['nA'] for d in gd]
            s = [d['S'] for d in gd]
            ax.scatter(v, s, color=colors_G[G], label=f'G={G}', s=40,
                       zorder=3, alpha=0.7)

        if np.std(vol) > 1e-12:
            xfit_v = np.linspace(vol.min(), vol.max(), 50)
            ax.plot(xfit_v, sl_v * xfit_v + int_v, 'k--', alpha=0.5,
                    linewidth=1.5, label=f'Fit R$^2$={r2_v:.3f}')
        ax.set_xlabel('Volume |A|')
        ax.set_ylabel('Entanglement entropy S')
        ax.set_title('(b) S vs volume (volume law test)')
        ax.legend(fontsize=7)

        # Panel (c): log-log S vs |boundary|
        ax = axes[1, 0]
        for G in G_VALUES:
            gd = [d for d in all_data
                  if d['G'] == G and d['bnd'] > 0 and d['S'] > 0]
            if not gd:
                continue
            lb = [np.log(d['bnd']) for d in gd]
            ls = [np.log(d['S']) for d in gd]
            ax.scatter(lb, ls, color=colors_G[G], label=f'G={G}', s=40,
                       zorder=3, alpha=0.7)

        mask = (bnd > 0) & (S > 0)
        if np.sum(mask) >= 2 and np.std(np.log(bnd[mask])) > 1e-12:
            lx = np.log(bnd[mask])
            xfit_log = np.linspace(lx.min(), lx.max(), 50)
            res = linregress(lx, np.log(S[mask]))
            ax.plot(xfit_log, res.slope * xfit_log + res.intercept,
                    'r-', alpha=0.6, linewidth=2,
                    label=f'p={res.slope:.2f}, R$^2$={res.rvalue**2:.3f}')

        ax.set_xlabel('ln |boundary|')
        ax.set_ylabel('ln S')
        ax.set_title(f'(c) Power law: S ~ |bnd|^{{{p_bnd:.2f}}}')
        ax.legend(fontsize=7)

        # Panel (d): alpha(G) -- area-law coefficient vs G
        ax = axes[1, 1]
        if len(alphas) >= 2:
            gs = [a[0] for a in alphas]
            als = [a[1] for a in alphas]
            r2s = [a[3] for a in alphas]
            ax.plot(gs, als, 'ko-', markersize=8)
            ax.axhline(y=alpha_mean, color='r', linestyle='--', alpha=0.5,
                       label=f'mean={alpha_mean:.4f}')
            ax.fill_between([min(gs), max(gs)],
                            alpha_mean - alpha_std, alpha_mean + alpha_std,
                            alpha=0.15, color='red')
            ax.set_xlabel('Gravitational coupling G')
            ax.set_ylabel('Area-law coefficient alpha')
            ax.set_title(f'(d) BH coefficient: alpha = {alpha_mean:.4f} '
                         f'(CV={cv:.2f})')
            ax.legend(fontsize=8)

            # Secondary y-axis for R^2
            ax2 = ax.twinx()
            ax2.plot(gs, r2s, 'b^--', markersize=6, alpha=0.5, label='R^2')
            ax2.set_ylabel('R^2 of area-law fit', color='blue')
            ax2.tick_params(axis='y', labelcolor='blue')
            ax2.set_ylim(0, 1.05)

        plt.tight_layout()
        out_path = __file__.replace('.py', '.png')
        plt.savefig(out_path, dpi=150)
        print(f"\nPlot saved to {out_path}")
    except Exception as e:
        print(f"\nPlot generation failed: {e}")

    print("\n" + "=" * 80)
    print("DONE")
    print("=" * 80)


if __name__ == '__main__':
    main()
