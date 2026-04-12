#!/usr/bin/env python3
"""Gravitational decoherence rate on a 2D staggered lattice.

Computes the decoherence rate for a mass in spatial superposition of two
locations and compares to the Diosi-Penrose prediction:
    Gamma_DP ~ G * m^2 / d

Protocol:
  1. On a 2D periodic lattice (side=10), prepare superposition:
       |psi> = (|L> + |R>) / sqrt(2)
     where |L> is Gaussian at (3, side/2), |R> at (7, side/2).

  2. Evolve under self-gravity with parity coupling:
       H_diag = (MASS + Phi) * epsilon(x),
       Phi from screened Poisson (L + mu^2) Phi = G * |psi|^2

  3. At each step, compute coherence:
       C(t) = |<psi_L|psi(t)> * <psi(t)|psi_R>|

  4. Fit decoherence rate: C(t) = C(0) * exp(-Gamma * t)

  5. Sweep G, separation d, and MASS. Compare to Diosi-Penrose:
       Gamma_DP ~ G * MASS^2 / separation

PStack experiment: gravitational-decoherence-rate
"""

from __future__ import annotations

import numpy as np
from scipy import sparse
from scipy.sparse.linalg import spsolve


# ---------------------------------------------------------------------------
# Default physical parameters
# ---------------------------------------------------------------------------
SIDE = 10
MASS = 0.30
MU2 = 0.22
DT = 0.12
N_STEPS = 60
SIGMA = 1.5  # Gaussian width in lattice units


# ---------------------------------------------------------------------------
# 2D periodic lattice helpers
# ---------------------------------------------------------------------------
def build_lattice(side: int):
    """Build 2D periodic lattice: positions, colors, adjacency.

    Returns:
        pos: list of (x, y) tuples
        col: array of parity colors (x+y) % 2
        adj: dict mapping site index -> list of neighbor indices
        n: total number of sites
    """
    pos = [(x, y) for x in range(side) for y in range(side)]
    n = len(pos)
    col = np.array([(x + y) % 2 for x, y in pos], dtype=float)

    idx = {}
    for i, (x, y) in enumerate(pos):
        idx[(x, y)] = i

    adj = {}
    for i, (x, y) in enumerate(pos):
        neighbors = []
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            nx, ny = (x + dx) % side, (y + dy) % side
            neighbors.append(idx[(nx, ny)])
        adj[i] = neighbors

    return pos, col, adj, n


def make_laplacian_2d(adj: dict, n: int) -> sparse.csc_matrix:
    """Graph Laplacian for periodic 2D lattice."""
    rows, cols, vals = [], [], []
    for i in range(n):
        nbrs = adj[i]
        rows.append(i)
        cols.append(i)
        vals.append(-float(len(nbrs)))
        for j in nbrs:
            rows.append(i)
            cols.append(j)
            vals.append(1.0)
    return sparse.csc_matrix((vals, (rows, cols)), shape=(n, n))


def solve_phi(rho: np.ndarray, L: sparse.csc_matrix, mu2: float,
              G: float, n: int) -> np.ndarray:
    """Screened Poisson: (L + mu^2 I) phi = G * rho."""
    A = (L + mu2 * sparse.eye(n)).tocsc()
    return spsolve(A, G * rho)


def build_hamiltonian(pos, col, adj, n, phi, mass):
    """Staggered 2D Hamiltonian with parity coupling.

    H_diag = (mass + phi) * epsilon,  epsilon = (-1)^(x+y)
    H_hop  = -i/2 forward, +i/2 backward (nearest-neighbor)
    """
    par = np.where(col == 0, 1.0, -1.0)
    diag = (mass + phi) * par

    rows, cols_arr, vals = [], [], []
    for i in range(n):
        rows.append(i)
        cols_arr.append(i)
        vals.append(diag[i])

    for i in range(n):
        for j in adj[i]:
            rows.append(i)
            cols_arr.append(j)
            # Antisymmetric hopping: sign from ordering
            if j > i or (j < i and (j == 0 and i == n - 1)):
                vals.append(-0.5j)
            else:
                vals.append(0.5j)

    H = sparse.csc_matrix((vals, (rows, cols_arr)), shape=(n, n), dtype=complex)
    return H


def cn_step(H: sparse.csc_matrix, psi: np.ndarray, dt: float) -> np.ndarray:
    """Crank-Nicolson time step: (I + iHdt/2) psi_new = (I - iHdt/2) psi_old."""
    n = len(psi)
    I = sparse.eye(n, dtype=complex, format="csc")
    A_plus = (I + 1j * H * dt / 2).tocsc()
    A_minus = I - 1j * H * dt / 2
    rhs = A_minus.dot(psi)
    return spsolve(A_plus, rhs)


# ---------------------------------------------------------------------------
# Gaussian wavepacket on 2D lattice
# ---------------------------------------------------------------------------
def gaussian_2d(cx: float, cy: float, sigma: float, pos, n: int) -> np.ndarray:
    """Normalized 2D Gaussian centered at (cx, cy)."""
    psi = np.zeros(n, dtype=complex)
    for i, (x, y) in enumerate(pos):
        psi[i] = np.exp(-0.5 * ((x - cx)**2 + (y - cy)**2) / sigma**2)
    norm = np.sqrt(np.sum(np.abs(psi)**2))
    return psi / norm


# ---------------------------------------------------------------------------
# Coherence measurement
# ---------------------------------------------------------------------------
def measure_coherence(psi, psi_L_init, psi_R_init):
    """Coherence C = |<psi_L|psi> * <psi|psi_R>|."""
    overlap_L = np.vdot(psi_L_init, psi)  # <psi_L|psi>
    overlap_R = np.vdot(psi, psi_R_init)  # <psi|psi_R>
    return np.abs(overlap_L * overlap_R)


# ---------------------------------------------------------------------------
# Single decoherence run
# ---------------------------------------------------------------------------
def run_decoherence(side, mass, G, separation, n_steps=N_STEPS, dt=DT,
                    mu2=MU2, sigma=SIGMA):
    """Evolve superposition under self-gravity, return coherence time series.

    Places left packet at (side/2 - separation/2, side/2)
          right packet at (side/2 + separation/2, side/2)
    """
    pos, col, adj, n = build_lattice(side)
    L = make_laplacian_2d(adj, n)

    cy = side / 2.0
    cx_L = side / 2.0 - separation / 2.0
    cx_R = side / 2.0 + separation / 2.0

    psi_L_init = gaussian_2d(cx_L, cy, sigma, pos, n)
    psi_R_init = gaussian_2d(cx_R, cy, sigma, pos, n)

    # Initial superposition
    psi = (psi_L_init + psi_R_init) / np.sqrt(2)
    psi /= np.sqrt(np.sum(np.abs(psi)**2))

    coherence = np.zeros(n_steps + 1)
    coherence[0] = measure_coherence(psi, psi_L_init, psi_R_init)

    for step in range(n_steps):
        rho = np.abs(psi)**2
        phi = solve_phi(rho, L, mu2, G, n)
        H = build_hamiltonian(pos, col, adj, n, phi, mass)
        psi = cn_step(H, psi, dt)
        psi /= np.sqrt(np.sum(np.abs(psi)**2))  # re-normalize
        coherence[step + 1] = measure_coherence(psi, psi_L_init, psi_R_init)

    return coherence


# ---------------------------------------------------------------------------
# Fit decoherence rate
# ---------------------------------------------------------------------------
def fit_gamma(coherence, dt):
    """Fit C(t) = C(0) * exp(-Gamma*t) via log-linear regression.

    Returns Gamma (positive = decaying).
    """
    c0 = coherence[0]
    if c0 < 1e-30:
        return 0.0

    # Use points where coherence is still measurable
    valid = []
    for i, c in enumerate(coherence):
        if c > 1e-20 and c / c0 > 1e-10:
            valid.append((i * dt, np.log(c / c0)))

    if len(valid) < 3:
        return 0.0

    times = np.array([v[0] for v in valid])
    log_ratio = np.array([v[1] for v in valid])

    # Linear fit: log(C/C0) = -Gamma * t
    coeffs = np.polyfit(times, log_ratio, 1)
    gamma = -coeffs[0]  # slope is -Gamma
    return gamma


# ---------------------------------------------------------------------------
# Main sweeps
# ---------------------------------------------------------------------------
def main():
    print("=" * 76)
    print("Gravitational Decoherence Rate on 2D Staggered Lattice")
    print("=" * 76)
    print(f"  SIDE={SIDE}, default MASS={MASS}, MU2={MU2}, DT={DT}")
    print(f"  N_STEPS={N_STEPS}, SIGMA={SIGMA}")
    print(f"  T_total = {N_STEPS * DT:.2f}")
    print()

    side = SIDE
    pos, col, adj, n = build_lattice(side)
    print(f"  Lattice: {side}x{side} = {n} sites, periodic BC")
    print()

    # ===================================================================
    # SWEEP 1: G coupling strength
    # ===================================================================
    G_values = [1, 2, 5, 10, 20, 50]
    sep_default = 4
    mass_default = MASS

    print("-" * 76)
    print(f"SWEEP 1: Gamma vs G  (d={sep_default}, MASS={mass_default})")
    print("-" * 76)

    gammas_G = []
    for G in G_values:
        coherence = run_decoherence(side, mass_default, G, sep_default)
        gamma = fit_gamma(coherence, DT)
        gammas_G.append(gamma)
        print(f"  G={G:>4d}  Gamma={gamma:>12.6e}  C(0)={coherence[0]:.6f}  "
              f"C(end)={coherence[-1]:.6f}")

    # Power-law fit: Gamma vs G
    valid_G = [(g, gam) for g, gam in zip(G_values, gammas_G) if gam > 1e-20]
    if len(valid_G) >= 2:
        log_g = np.log([v[0] for v in valid_G])
        log_gam = np.log([v[1] for v in valid_G])
        slope_G = np.polyfit(log_g, log_gam, 1)[0]
        print(f"\n  Power-law fit: Gamma ~ G^{slope_G:.3f}  (DP predicts G^1.0)")
    else:
        slope_G = float("nan")
        print("\n  Insufficient data for power-law fit")
    print()

    # ===================================================================
    # SWEEP 2: separation d
    # ===================================================================
    d_values = [2, 4, 6, 8]
    G_default = 10

    print("-" * 76)
    print(f"SWEEP 2: Gamma vs separation d  (G={G_default}, MASS={mass_default})")
    print("-" * 76)

    gammas_d = []
    for d in d_values:
        coherence = run_decoherence(side, mass_default, G_default, d)
        gamma = fit_gamma(coherence, DT)
        gammas_d.append(gamma)
        print(f"  d={d:>2d}  Gamma={gamma:>12.6e}  C(0)={coherence[0]:.6f}  "
              f"C(end)={coherence[-1]:.6f}")

    valid_d = [(d, gam) for d, gam in zip(d_values, gammas_d) if gam > 1e-20]
    if len(valid_d) >= 2:
        log_d = np.log([v[0] for v in valid_d])
        log_gam = np.log([v[1] for v in valid_d])
        slope_d = np.polyfit(log_d, log_gam, 1)[0]
        print(f"\n  Power-law fit: Gamma ~ d^{slope_d:.3f}  (DP predicts d^-1.0)")
    else:
        slope_d = float("nan")
        print("\n  Insufficient data for power-law fit")
    print()

    # ===================================================================
    # SWEEP 3: mass
    # ===================================================================
    mass_values = [0.1, 0.2, 0.3, 0.5]

    print("-" * 76)
    print(f"SWEEP 3: Gamma vs MASS  (G={G_default}, d={sep_default})")
    print("-" * 76)

    gammas_m = []
    for m in mass_values:
        coherence = run_decoherence(side, m, G_default, sep_default)
        gamma = fit_gamma(coherence, DT)
        gammas_m.append(gamma)
        print(f"  MASS={m:.2f}  Gamma={gamma:>12.6e}  C(0)={coherence[0]:.6f}  "
              f"C(end)={coherence[-1]:.6f}")

    valid_m = [(m, gam) for m, gam in zip(mass_values, gammas_m) if gam > 1e-20]
    if len(valid_m) >= 2:
        log_m = np.log([v[0] for v in valid_m])
        log_gam = np.log([v[1] for v in valid_m])
        slope_m = np.polyfit(log_m, log_gam, 1)[0]
        print(f"\n  Power-law fit: Gamma ~ m^{slope_m:.3f}  (DP predicts m^2.0)")
    else:
        slope_m = float("nan")
        print("\n  Insufficient data for power-law fit")
    print()

    # ===================================================================
    # Diosi-Penrose comparison table
    # ===================================================================
    print("=" * 76)
    print("DIOSI-PENROSE COMPARISON")
    print("  Gamma_DP = G * MASS^2 / d   (lattice units)")
    print("=" * 76)
    print()

    print(f"{'G':>6} {'d':>4} {'MASS':>6} {'Gamma':>14} {'Gamma_DP':>14} {'ratio':>10}")
    print("-" * 76)

    # Run a cross-section of the parameter space
    all_results = []
    for G in [1, 5, 10, 20, 50]:
        for d in [2, 4, 6, 8]:
            for m in [0.2, 0.3, 0.5]:
                coherence = run_decoherence(side, m, G, d)
                gamma = fit_gamma(coherence, DT)
                gamma_dp = G * m**2 / d
                ratio = gamma / gamma_dp if gamma_dp > 0 else float("inf")
                all_results.append((G, d, m, gamma, gamma_dp, ratio))
                print(f"{G:>6d} {d:>4d} {m:>6.2f} {gamma:>14.6e} "
                      f"{gamma_dp:>14.6e} {ratio:>10.4f}")

    print()

    # ===================================================================
    # Summary of scaling exponents
    # ===================================================================
    print("=" * 76)
    print("SCALING SUMMARY")
    print("=" * 76)
    print(f"  Gamma ~ G^alpha:    alpha = {slope_G:+.3f}   (DP: +1.0)")
    print(f"  Gamma ~ d^beta:     beta  = {slope_d:+.3f}   (DP: -1.0)")
    print(f"  Gamma ~ m^delta:    delta = {slope_m:+.3f}   (DP: +2.0)")
    print()

    # Check overall consistency
    if not np.isnan(slope_G) and not np.isnan(slope_d) and not np.isnan(slope_m):
        dp_match = (abs(slope_G - 1.0) < 0.5 and
                    abs(slope_d + 1.0) < 0.5 and
                    abs(slope_m - 2.0) < 0.5)
        if dp_match:
            print("  RESULT: Scaling is CONSISTENT with Diosi-Penrose "
                  "(Gamma ~ G*m^2/d)")
        else:
            print("  RESULT: Scaling DEVIATES from Diosi-Penrose prediction")
            if abs(slope_G - 1.0) >= 0.5:
                print(f"    - G exponent off: {slope_G:+.3f} vs +1.0")
            if abs(slope_d + 1.0) >= 0.5:
                print(f"    - d exponent off: {slope_d:+.3f} vs -1.0")
            if abs(slope_m - 2.0) >= 0.5:
                print(f"    - m exponent off: {slope_m:+.3f} vs +2.0")
    else:
        print("  RESULT: Insufficient data for scaling assessment")

    print()
    print("=" * 76)
    print("DONE")
    print("=" * 76)


if __name__ == "__main__":
    main()
