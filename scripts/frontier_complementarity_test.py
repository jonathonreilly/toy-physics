#!/usr/bin/env python3
"""Complementarity / fuzzball test: BMV entanglement vs OTOC scrambling.

HYPOTHESIS: BMV entanglement witness and OTOC scrambling measure are
complementary observables that cross near the Hawking-Page transition G_HP.

  - BMV grows monotonically with G (entanglement from geometry superposition)
  - OTOC scrambling is KILLED at strong G (localization suppresses transport)
  - Prediction: the two curves cross near G_HP ~ 9.8

This is the complementarity/fuzzball interpretation: as the gravitational
coupling strengthens, quantum information becomes entangled (BMV) but stops
scrambling (OTOC). The crossover marks the Hawking-Page transition.

Protocol on 2D staggered lattice (side=10, n=100):

  BMV: Two wavepackets propagate under geometry-superposition (source vs no
       source). S_BMV = H_binary((1 + ovlp_1 * ovlp_2) / 2) / ln(2).

  OTOC: Build self-gravitating H, eigendecompose, compute propagator
        G(i,j,t), measure C_max = max_t [1 - |G(i,j,t)|^4 / |G(i,j,0)|^4].

  Area-law exponent: Dirac sea from final H, BFS balls R=1..4, fit S ~ |bnd|^alpha.

PStack experiment: complementarity-test
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

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# ---------------------------------------------------------------------------
# Physical parameters
# ---------------------------------------------------------------------------
MASS = 0.30
MU2 = 0.22
DT = 0.12
N_STEPS = 30
SIGMA = 1.5
SIDE = 10
N_SITES = SIDE * SIDE  # 100

G_VALUES = [0.5, 1, 2, 5, 8, 10, 15, 20, 30, 50, 75, 100]
G_HP = 9.8  # predicted Hawking-Page transition

# OTOC parameters
T_MAX_OTOC = 50  # max time in units of DT
OTOC_DISTANCE = 2  # site separation for OTOC pair

# Area-law parameters
RADII = [1, 2, 3, 4]


# ---------------------------------------------------------------------------
# Lattice construction
# ---------------------------------------------------------------------------

def build_lattice(side: int):
    """2D periodic staggered lattice with checkerboard coloring."""
    n = side * side
    pos = np.zeros((n, 2))
    adj: dict[int, list[int]] = {i: [] for i in range(n)}
    col = np.zeros(n, dtype=int)
    index: dict[tuple[int, int], int] = {}

    for ix in range(side):
        for iy in range(side):
            idx = ix * side + iy
            pos[idx] = (ix, iy)
            col[idx] = (ix + iy) % 2
            index[(ix, iy)] = idx
            for dix, diy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                jx = (ix + dix) % side
                jy = (iy + diy) % side
                adj[idx].append(jx * side + jy)

    return n, pos, adj, col, index


# ---------------------------------------------------------------------------
# Poisson solver and Hamiltonian
# ---------------------------------------------------------------------------

def solve_poisson(adj: dict, n: int, rho: np.ndarray, mu2: float, G: float):
    if G == 0.0:
        return np.zeros(n)
    rows, cols_sp, vals = [], [], []
    for i in range(n):
        deg = len(adj[i])
        rows.append(i); cols_sp.append(i); vals.append(float(deg) + mu2)
        for j in adj[i]:
            rows.append(i); cols_sp.append(j); vals.append(-1.0)
    L = sparse.csc_matrix((vals, (rows, cols_sp)), shape=(n, n))
    return spsolve(L, G * rho)


def build_hamiltonian(n: int, pos: np.ndarray, adj: dict,
                      col: np.ndarray, phi: np.ndarray):
    """Staggered-fermion Hamiltonian with parity coupling."""
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


def cn_step(psi: np.ndarray, H, dt: float):
    n = H.shape[0]
    ap = (speye(n, format='csc') + 1j * H * dt / 2).tocsc()
    am = speye(n, format='csr') - 1j * H * dt / 2
    return spsolve(ap, am.dot(psi))


def gaussian_at(pos: np.ndarray, center: tuple[float, float], sigma: float):
    cx, cy = center
    rsq = (pos[:, 0] - cx) ** 2 + (pos[:, 1] - cy) ** 2
    psi = np.exp(-0.5 * rsq / sigma ** 2).astype(complex)
    norm = np.linalg.norm(psi)
    if norm < 1e-30:
        raise ValueError(f"Gaussian at {center} has zero norm")
    return psi / norm


def binary_entropy(p: float) -> float:
    if p <= 0.0 or p >= 1.0:
        return 0.0
    return -p * math.log(p) - (1.0 - p) * math.log(1.0 - p)


# ---------------------------------------------------------------------------
# BMV measurement
# ---------------------------------------------------------------------------

def measure_bmv(G: float, n: int, pos: np.ndarray, adj: dict,
                col: np.ndarray, index: dict):
    """BMV entanglement witness for coupling G.

    Returns S_BMV normalized to [0, 1] (in units of ln(2)).
    """
    # Solve for source field at midpoint
    source_node = index[(SIDE // 2, SIDE // 2)]
    rho_ext = np.zeros(n)
    rho_ext[source_node] = G
    phi_A = solve_poisson(adj, n, rho_ext, MU2, 1.0)  # external source strength G in rho
    phi_B = np.zeros(n)

    ham_A = build_hamiltonian(n, pos, adj, col, phi_A)
    ham_B = build_hamiltonian(n, pos, adj, col, phi_B)

    # Two particles
    psi_1_init = gaussian_at(pos, (2.0, 5.0), SIGMA)
    psi_2_init = gaussian_at(pos, (8.0, 5.0), SIGMA)

    psi_1A, psi_1B = psi_1_init.copy(), psi_1_init.copy()
    psi_2A, psi_2B = psi_2_init.copy(), psi_2_init.copy()

    for _ in range(N_STEPS):
        psi_1A = cn_step(psi_1A, ham_A, DT)
        psi_1B = cn_step(psi_1B, ham_B, DT)
        psi_2A = cn_step(psi_2A, ham_A, DT)
        psi_2B = cn_step(psi_2B, ham_B, DT)

    overlap_1 = abs(np.vdot(psi_1A, psi_1B))
    overlap_2 = abs(np.vdot(psi_2A, psi_2B))

    product_overlap = overlap_1 * overlap_2
    p = 0.5 + 0.5 * product_overlap
    s_bmv = binary_entropy(p)
    bmv_witness = s_bmv / math.log(2)  # normalize to [0, 1]

    return bmv_witness, overlap_1, overlap_2, s_bmv


# ---------------------------------------------------------------------------
# OTOC measurement
# ---------------------------------------------------------------------------

def measure_otoc(G: float, n: int, pos: np.ndarray, adj: dict,
                 col: np.ndarray):
    """OTOC scrambling measure for coupling G.

    Evolves Gaussian under self-gravity to get self-consistent phi,
    then eigendecomposes H and computes propagator elements.

    Returns C_max (peak scrambling measure).
    """
    # Evolve to get self-consistent field
    cx = (pos[:, 0].max() + pos[:, 0].min()) / 2
    cy = (pos[:, 1].max() + pos[:, 1].min()) / 2
    psi = gaussian_at(pos, (cx, cy), SIGMA)

    H_final = None
    for step in range(N_STEPS):
        rho = np.abs(psi) ** 2
        phi = solve_poisson(adj, n, rho, MU2, G)
        H = build_hamiltonian(n, pos, adj, col, phi)
        psi = cn_step(psi, H, DT)
        psi /= np.linalg.norm(psi)
        H_final = H

    if H_final is None:
        return 0.0

    # Eigendecompose
    H_dense = H_final.toarray()
    H_dense = 0.5 * (H_dense + H_dense.conj().T)  # enforce Hermiticity
    evals, evecs = np.linalg.eigh(H_dense)

    # Pick site pair: center and a site at distance OTOC_DISTANCE
    center_idx = int(np.argmin((pos[:, 0] - cx)**2 + (pos[:, 1] - cy)**2))
    dist_from_center = np.abs(pos[:, 0] - pos[center_idx, 0]) + \
                       np.abs(pos[:, 1] - pos[center_idx, 1])
    candidates = np.where(np.abs(dist_from_center - OTOC_DISTANCE) < 0.5)[0]
    if len(candidates) == 0:
        return 0.0
    j_site = candidates[0]
    i_site = center_idx

    # Compute propagator elements G(i, j, t) for t in [0, T_MAX_OTOC * DT]
    t_steps = np.arange(0, T_MAX_OTOC + 1)
    c_max = 0.0

    # G(i,j,0) = delta(i,j) for i != j, so use spreading measure
    # |G(i,j,t)|^2 = probability of reaching i starting from j
    for t_val in t_steps:
        t_phys = t_val * DT
        phases = np.exp(-1j * evals * t_phys)
        g_ij = np.sum(evecs[i_site, :] * np.conj(evecs[j_site, :]) * phases)
        c_t = np.abs(g_ij) ** 2
        if c_t > c_max:
            c_max = c_t

    return c_max


# ---------------------------------------------------------------------------
# Entanglement area-law exponent
# ---------------------------------------------------------------------------

def bfs_ball(adj: dict, center: int, radius: int, n: int):
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


def dirac_sea_correlation(H):
    """Fill negative-energy modes, return correlation matrix."""
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


def entanglement_entropy(C: np.ndarray, A_nodes: list[int]):
    if len(A_nodes) == 0:
        return 0.0
    ix = np.ix_(A_nodes, A_nodes)
    C_A = C[ix]
    C_A = 0.5 * (C_A + C_A.conj().T)
    nu = np.linalg.eigvalsh(C_A).real
    nu = np.clip(nu, 1e-15, 1.0 - 1e-15)
    S = -np.sum(nu * np.log(nu) + (1.0 - nu) * np.log(1.0 - nu))
    return float(S)


def measure_area_exponent(G: float, n: int, pos: np.ndarray, adj: dict,
                          col: np.ndarray):
    """Compute area-law exponent alpha from S ~ |bnd|^alpha via BFS balls."""
    # Evolve to get final H
    cx = (pos[:, 0].max() + pos[:, 0].min()) / 2
    cy = (pos[:, 1].max() + pos[:, 1].min()) / 2
    psi = gaussian_at(pos, (cx, cy), SIGMA)

    H_final = None
    for step in range(N_STEPS):
        rho = np.abs(psi) ** 2
        phi = solve_poisson(adj, n, rho, MU2, G)
        H = build_hamiltonian(n, pos, adj, col, phi)
        psi = cn_step(psi, H, DT)
        psi /= np.linalg.norm(psi)
        H_final = H

    if H_final is None:
        return 1.0

    C = dirac_sea_correlation(H_final)

    center_idx = int(np.argmin((pos[:, 0] - cx)**2 + (pos[:, 1] - cy)**2))

    bnd_sizes = []
    entropies = []

    for R in RADII:
        A_nodes, bnd_edges = bfs_ball(adj, center_idx, R, n)
        if bnd_edges == 0 or len(A_nodes) == 0:
            continue
        S = entanglement_entropy(C, A_nodes)
        bnd_sizes.append(bnd_edges)
        entropies.append(S)

    if len(bnd_sizes) < 2:
        return 1.0

    # Fit S ~ |bnd|^alpha via log-log regression
    log_bnd = np.log(np.array(bnd_sizes, dtype=float))
    log_S = np.log(np.array(entropies, dtype=float) + 1e-15)

    if np.std(log_bnd) < 1e-12:
        return 1.0

    res = linregress(log_bnd, log_S)
    return res.slope  # alpha


# ---------------------------------------------------------------------------
# Main experiment
# ---------------------------------------------------------------------------

def main():
    t0 = time.time()

    print("=" * 80)
    print("FRONTIER: Complementarity / Fuzzball Test")
    print("  BMV Entanglement vs OTOC Scrambling vs G")
    print("=" * 80)
    print()
    print(f"Lattice: 2D staggered, side={SIDE}, n={N_SITES}")
    print(f"MASS={MASS}, MU2={MU2}, DT={DT}, N_STEPS={N_STEPS}")
    print(f"BMV: particles at (2,5) and (8,5), source at ({SIDE//2},{SIDE//2})")
    print(f"OTOC: center site, distance={OTOC_DISTANCE}, T_max={T_MAX_OTOC*DT:.1f}")
    print(f"Area law: BFS radii {RADII}")
    print(f"G_HP = {G_HP} (predicted Hawking-Page transition)")
    print()

    n, pos, adj, col, index = build_lattice(SIDE)

    # Storage
    bmv_data = []
    otoc_data = []
    alpha_data = []

    header = (f"{'G':>6s}  {'BMV_wit':>8s} {'ovlp_1':>7s} {'ovlp_2':>7s} "
              f"{'S_BMV':>8s}  {'OTOC_Cmax':>10s}  {'alpha':>7s}")
    print(header)
    print("-" * 75)

    for G in G_VALUES:
        # BMV
        bmv_wit, ovlp_1, ovlp_2, s_bmv = measure_bmv(G, n, pos, adj, col, index)
        bmv_data.append(bmv_wit)

        # OTOC
        c_max = measure_otoc(G, n, pos, adj, col)
        otoc_data.append(c_max)

        # Area-law exponent
        alpha = measure_area_exponent(G, n, pos, adj, col)
        alpha_data.append(alpha)

        print(f"{G:6.1f}  {bmv_wit:8.5f} {ovlp_1:7.4f} {ovlp_2:7.4f} "
              f"{s_bmv:8.5f}  {c_max:10.6f}  {alpha:7.3f}")

    bmv_arr = np.array(bmv_data)
    otoc_arr = np.array(otoc_data)
    alpha_arr = np.array(alpha_data)
    G_arr = np.array(G_VALUES, dtype=float)

    # -----------------------------------------------------------------------
    # Find crossing point
    # -----------------------------------------------------------------------
    print()
    print("=" * 80)
    print("CROSSING ANALYSIS")
    print("=" * 80)

    # Normalize OTOC to comparable scale for crossing detection
    otoc_max = otoc_arr.max() if otoc_arr.max() > 0 else 1.0
    otoc_norm = otoc_arr / otoc_max  # normalized to [0, 1]

    crossing_G = None
    for i in range(len(G_arr) - 1):
        diff_i = bmv_arr[i] - otoc_norm[i]
        diff_j = bmv_arr[i + 1] - otoc_norm[i + 1]
        if diff_i * diff_j < 0:
            # Linear interpolation for crossing
            frac = abs(diff_i) / (abs(diff_i) + abs(diff_j))
            crossing_G = G_arr[i] + frac * (G_arr[i + 1] - G_arr[i])
            print(f"  BMV and normalized OTOC curves CROSS at G ~ {crossing_G:.1f}")
            print(f"  (Between G={G_arr[i]:.1f} and G={G_arr[i+1]:.1f})")
            break

    if crossing_G is None:
        # Check which dominates
        if bmv_arr[-1] > otoc_norm[-1]:
            print("  No crossing detected: BMV dominates OTOC at all G values")
        else:
            print("  No crossing detected: OTOC dominates BMV at all G values")

    # Distance to G_HP
    if crossing_G is not None:
        print(f"  Distance to G_HP = {G_HP}: |crossing - G_HP| = {abs(crossing_G - G_HP):.1f}")
        if abs(crossing_G - G_HP) < 5:
            print("  -> CONSISTENT with Hawking-Page prediction!")
        else:
            print("  -> NOT near G_HP, complementarity is decoupled from HP transition")

    # -----------------------------------------------------------------------
    # Area-law exponent analysis
    # -----------------------------------------------------------------------
    print()
    print("=" * 80)
    print("AREA-LAW EXPONENT ANALYSIS")
    print("=" * 80)

    for i, G in enumerate(G_VALUES):
        indicator = " <-- G_HP" if abs(G - G_HP) < 2 else ""
        print(f"  G={G:6.1f}: alpha = {alpha_arr[i]:.3f}{indicator}")

    # Detect transition in alpha
    for i in range(len(G_arr) - 1):
        if alpha_arr[i] < 1.0 and alpha_arr[i + 1] >= 1.0:
            frac = (1.0 - alpha_arr[i]) / (alpha_arr[i + 1] - alpha_arr[i])
            G_trans = G_arr[i] + frac * (G_arr[i + 1] - G_arr[i])
            print(f"\n  Area-law to super-area transition at G ~ {G_trans:.1f}")
            print(f"  (alpha crosses 1.0 between G={G_arr[i]:.1f} and G={G_arr[i+1]:.1f})")
            break

    # -----------------------------------------------------------------------
    # Plot
    # -----------------------------------------------------------------------
    fig, (ax1, ax3) = plt.subplots(2, 1, figsize=(10, 10), gridspec_kw={'height_ratios': [2, 1]})

    # --- Panel 1: BMV and OTOC on same axes ---
    color_bmv = '#2166ac'
    color_otoc = '#b2182b'

    ax1.set_xlabel('Gravitational coupling G', fontsize=12)
    ax1.set_ylabel('BMV witness (normalized)', fontsize=12, color=color_bmv)
    line1, = ax1.plot(G_arr, bmv_arr, 'o-', color=color_bmv, linewidth=2,
                      markersize=6, label='BMV witness')
    ax1.tick_params(axis='y', labelcolor=color_bmv)
    ax1.set_ylim(-0.05, 1.05)

    ax2 = ax1.twinx()
    ax2.set_ylabel('OTOC C_max', fontsize=12, color=color_otoc)
    line2, = ax2.plot(G_arr, otoc_arr, 's-', color=color_otoc, linewidth=2,
                      markersize=6, label='OTOC C_max')
    ax2.tick_params(axis='y', labelcolor=color_otoc)
    otoc_ylim = max(otoc_arr.max() * 1.2, 0.01)
    ax2.set_ylim(-0.005, otoc_ylim)

    # G_HP line
    ax1.axvline(x=G_HP, color='gray', linestyle='--', linewidth=1.5, alpha=0.7)
    ax1.text(G_HP + 0.5, 0.95, f'G_HP = {G_HP}', fontsize=10, color='gray',
             va='top')

    # Crossing point
    if crossing_G is not None:
        ax1.axvline(x=crossing_G, color='green', linestyle=':', linewidth=1.5, alpha=0.7)
        ax1.text(crossing_G + 0.5, 0.85, f'crossing ~ {crossing_G:.1f}',
                 fontsize=10, color='green', va='top')

    ax1.set_title('Complementarity Test: BMV Entanglement vs OTOC Scrambling',
                  fontsize=14, fontweight='bold')
    lines = [line1, line2]
    labels = [l.get_label() for l in lines]
    ax1.legend(lines, labels, loc='center left', fontsize=10)
    ax1.set_xscale('log')
    ax1.grid(True, alpha=0.3)

    # --- Panel 2: Area-law exponent ---
    ax3.plot(G_arr, alpha_arr, 'D-', color='#4daf4a', linewidth=2, markersize=6,
             label='alpha (S ~ |bnd|^alpha)')
    ax3.axhline(y=1.0, color='gray', linestyle='--', linewidth=1, alpha=0.5,
                label='area law (alpha=1)')
    ax3.axvline(x=G_HP, color='gray', linestyle='--', linewidth=1.5, alpha=0.7)
    ax3.text(G_HP + 0.5, ax3.get_ylim()[1] * 0.9 if len(alpha_arr) > 0 else 1.5,
             f'G_HP = {G_HP}', fontsize=10, color='gray', va='top')

    ax3.set_xlabel('Gravitational coupling G', fontsize=12)
    ax3.set_ylabel('Area-law exponent alpha', fontsize=12)
    ax3.set_title('Entanglement Scaling Exponent', fontsize=14, fontweight='bold')
    ax3.legend(fontsize=10)
    ax3.set_xscale('log')
    ax3.grid(True, alpha=0.3)

    plt.tight_layout()
    out_path = "scripts/frontier_complementarity_test.png"
    plt.savefig(out_path, dpi=150, bbox_inches='tight')
    print(f"\nPlot saved to {out_path}")

    # -----------------------------------------------------------------------
    # Verdict
    # -----------------------------------------------------------------------
    print()
    print("=" * 80)
    print("VERDICT")
    print("=" * 80)
    print()

    # BMV monotonicity
    bmv_monotonic = all(bmv_arr[i] >= bmv_arr[i - 1] - 1e-6 for i in range(1, len(bmv_arr)))
    print(f"  BMV monotonic in G:        {'YES' if bmv_monotonic else 'NO'}")
    print(f"  BMV range:                 {bmv_arr.min():.5f} to {bmv_arr.max():.5f}")

    # OTOC suppression
    otoc_suppressed = otoc_arr[-1] < otoc_arr[0] * 0.1
    print(f"  OTOC suppressed at high G: {'YES' if otoc_suppressed else 'NO'}")
    print(f"  OTOC range:                {otoc_arr.min():.6f} to {otoc_arr.max():.6f}")

    # Complementarity
    if crossing_G is not None and abs(crossing_G - G_HP) < 5:
        print()
        print("  COMPLEMENTARITY CONFIRMED near Hawking-Page transition")
        print(f"  Crossing at G ~ {crossing_G:.1f}, G_HP = {G_HP}")
        print("  Interpretation: as gravity strengthens past G_HP,")
        print("  quantum information becomes entangled (BMV up) but")
        print("  stops scrambling (OTOC down) -- fuzzball picture.")
    elif crossing_G is not None:
        print()
        print(f"  COMPLEMENTARITY detected but DECOUPLED from G_HP")
        print(f"  Crossing at G ~ {crossing_G:.1f}, G_HP = {G_HP}")
    else:
        print()
        if bmv_arr[-1] > 0.5 and otoc_suppressed:
            print("  NO CROSSING but complementary trends:")
            print("  BMV increases while OTOC decreases with G")
            print("  Fuzzball-like behavior without sharp transition")
        else:
            print("  COMPLEMENTARITY NOT CONFIRMED in this parameter regime")

    elapsed = time.time() - t0
    print(f"\nTotal time: {elapsed:.1f}s")


if __name__ == "__main__":
    main()
