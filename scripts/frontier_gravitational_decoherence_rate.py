#!/usr/bin/env python3
"""Gravitational decoherence rate on a 1D staggered lattice.

Computes the decoherence rate for a mass in spatial superposition and
compares to the Diosi-Penrose prediction: Gamma_DP ~ G * m^2 / d.

Protocol:
  1. On a 1D periodic staggered lattice (n=61), prepare a superposition
     of two Gaussian wavepackets separated by distance d.
  2. Evolve each branch independently under its own self-gravity
     (screened Poisson for phi, parity-coupled Hamiltonian).
  3. Evolve the superposition under its combined self-gravity.
  4. Measure decoherence via overlap loss between the coherent
     superposition evolution and the independent-branch sum.
  5. Extract Gamma = -log(overlap) / T and compare to Gamma_DP ~ G/d.

PStack experiment: gravitational-decoherence-rate
"""

from __future__ import annotations

import numpy as np
from scipy import sparse
from scipy.sparse.linalg import spsolve


# ---------------------------------------------------------------------------
# Physical parameters
# ---------------------------------------------------------------------------
N = 61                # lattice sites (odd for clean center)
MASS = 0.30           # bare mass
MU2 = 0.22            # screening mass^2 for Poisson
DT = 0.12             # time step
N_STEPS = 50          # evolution steps
SIGMA = 3.0           # Gaussian width (lattice units)

SEPARATIONS = [2, 4, 6, 8, 12, 16]
COUPLINGS = [1.0, 5.0, 10.0, 20.0, 50.0]


# ---------------------------------------------------------------------------
# Lattice operators
# ---------------------------------------------------------------------------
def make_laplacian(n: int) -> sparse.csc_matrix:
    """1D periodic Laplacian (second-difference)."""
    diag = -2.0 * np.ones(n)
    off = np.ones(n - 1)
    L = sparse.diags([off, diag, off], [-1, 0, 1], shape=(n, n), format="lil")
    L[0, n - 1] = 1.0
    L[n - 1, 0] = 1.0
    return L.tocsc()


def solve_phi(rho: np.ndarray, L: sparse.csc_matrix, mu2: float, G: float) -> np.ndarray:
    """Screened Poisson: (L + mu^2) phi = G * rho."""
    A = (L + mu2 * sparse.eye(N)).tocsc()
    return spsolve(A, G * rho)


def make_hamiltonian(phi: np.ndarray) -> sparse.csc_matrix:
    """1D staggered Hamiltonian with parity coupling.

    H[x,x] = (MASS + phi[x]) * epsilon(x)   where epsilon(x) = (-1)^x
    H[x, x+1] = -i/2,  H[x, x-1] = +i/2    (periodic)
    """
    n = len(phi)
    eps = np.array([(-1) ** x for x in range(n)], dtype=float)

    # Diagonal: parity-coupled mass + field
    diag = (MASS + phi) * eps

    # Hopping: -i/2 forward, +i/2 backward
    hop_fwd = -0.5j * np.ones(n - 1)
    hop_bwd = 0.5j * np.ones(n - 1)

    H = sparse.diags([hop_bwd, diag, hop_fwd], [-1, 0, 1],
                      shape=(n, n), format="lil", dtype=complex)
    # Periodic boundary
    H[0, n - 1] = 0.5j
    H[n - 1, 0] = -0.5j
    return H.tocsc()


def cn_step(psi: np.ndarray, H: sparse.csc_matrix, dt: float) -> np.ndarray:
    """Crank-Nicolson time step: (I + iHdt/2) psi_new = (I - iHdt/2) psi_old."""
    I = sparse.eye(len(psi), dtype=complex, format="csc")
    A_plus = (I + 1j * H * dt / 2).tocsc()
    A_minus = I - 1j * H * dt / 2
    rhs = A_minus.dot(psi)
    return spsolve(A_plus, rhs)


# ---------------------------------------------------------------------------
# Gaussian wavepacket
# ---------------------------------------------------------------------------
def gaussian(center: float, sigma: float, n: int) -> np.ndarray:
    """Normalized Gaussian on the lattice."""
    x = np.arange(n, dtype=float)
    psi = np.exp(-0.5 * ((x - center) / sigma) ** 2)
    norm = np.sqrt(np.sum(np.abs(psi) ** 2))
    return psi / norm


# ---------------------------------------------------------------------------
# Evolve a wavefunction under self-gravity for N_STEPS
# ---------------------------------------------------------------------------
def evolve(psi: np.ndarray, G: float, L: sparse.csc_matrix,
           n_steps: int = N_STEPS) -> np.ndarray:
    """Evolve psi under self-consistent gravity for n_steps CN steps."""
    psi = psi.copy().astype(complex)
    for _ in range(n_steps):
        rho = np.abs(psi) ** 2
        phi = solve_phi(rho, L, MU2, G)
        H = make_hamiltonian(phi)
        psi = cn_step(psi, H, DT)
        # Re-normalize to prevent drift
        psi /= np.sqrt(np.sum(np.abs(psi) ** 2))
    return psi


# ---------------------------------------------------------------------------
# Decoherence measurement
# ---------------------------------------------------------------------------
def measure_decoherence(d: int, G: float, L: sparse.csc_matrix) -> float:
    """Measure gravitational decoherence for separation d and coupling G.

    Returns Gamma = -log(overlap) / T where T = N_STEPS * DT.
    """
    center = N // 2
    left_center = center - d // 2
    right_center = center + d // 2

    psi_L = gaussian(left_center, SIGMA, N)
    psi_R = gaussian(right_center, SIGMA, N)

    # Evolve each branch independently
    psi_L_evolved = evolve(psi_L, G, L)
    psi_R_evolved = evolve(psi_R, G, L)

    # Evolve the superposition under combined self-gravity
    psi_super = (psi_L + psi_R) / np.sqrt(2)
    psi_super /= np.sqrt(np.sum(np.abs(psi_super) ** 2))
    psi_super_evolved = evolve(psi_super, G, L)

    # Coherent sum of independently evolved branches
    psi_coherent = (psi_L_evolved + psi_R_evolved) / np.sqrt(2)
    psi_coherent /= np.sqrt(np.sum(np.abs(psi_coherent) ** 2))

    # Overlap: how much does the self-gravitating superposition
    # differ from the coherent sum?
    overlap = np.abs(np.vdot(psi_super_evolved, psi_coherent)) ** 2

    T = N_STEPS * DT
    # Clamp overlap to avoid log(0)
    overlap = max(overlap, 1e-30)
    gamma = -np.log(overlap) / T
    return gamma


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main() -> None:
    L = make_laplacian(N)

    print("=" * 72)
    print("Gravitational Decoherence Rate on 1D Staggered Lattice")
    print("=" * 72)
    print(f"  N={N}, MASS={MASS}, MU2={MU2}, DT={DT}, N_STEPS={N_STEPS}")
    print(f"  sigma={SIGMA}, T_total={N_STEPS * DT:.2f}")
    print()

    # Collect results
    results: dict[tuple[int, float], float] = {}

    for G in COUPLINGS:
        for d in SEPARATIONS:
            gamma = measure_decoherence(d, G, L)
            results[(d, G)] = gamma

    # --- Print Gamma(d, G) table ---
    print("Gamma(d, G) table  [decoherence rate]")
    print("-" * 72)
    header = f"{'d \\\\ G':>8}"
    for G in COUPLINGS:
        header += f"  {G:>10.1f}"
    print(header)
    print("-" * 72)

    for d in SEPARATIONS:
        row = f"{d:>8d}"
        for G in COUPLINGS:
            row += f"  {results[(d, G)]:>10.4e}"
        print(row)
    print()

    # --- Check Gamma ~ G / d scaling ---
    print("Scaling check: Gamma * d / G  (should be ~ constant if Gamma ~ G/d)")
    print("-" * 72)
    header = f"{'d \\\\ G':>8}"
    for G in COUPLINGS:
        header += f"  {G:>10.1f}"
    print(header)
    print("-" * 72)

    for d in SEPARATIONS:
        row = f"{d:>8d}"
        for G in COUPLINGS:
            gamma = results[(d, G)]
            scaled = gamma * d / G if G > 0 else 0.0
            row += f"  {scaled:>10.4e}"
        print(row)
    print()

    # --- Diosi-Penrose comparison ---
    print("Diosi-Penrose comparison: Gamma_DP = G * m^2 / d")
    print(f"  (using m = MASS = {MASS})")
    print("-" * 72)
    header = f"{'d \\\\ G':>8}  {'Gamma':>10}  {'Gamma_DP':>10}  {'ratio':>10}"
    print(header)
    print("-" * 72)

    for d in SEPARATIONS:
        for G in COUPLINGS:
            gamma = results[(d, G)]
            gamma_dp = G * MASS ** 2 / d
            ratio = gamma / gamma_dp if gamma_dp > 0 else float("inf")
            print(f"{d:>8d}  {gamma:>10.4e}  {gamma_dp:>10.4e}  {ratio:>10.4f}")
    print()

    # --- Power-law fits ---
    print("Power-law fits (log-log regression)")
    print("-" * 72)

    # Fit Gamma vs d at each G
    print("\nGamma vs d  (expect slope ~ -1 for 1/d):")
    for G in COUPLINGS:
        gammas = [results[(d, G)] for d in SEPARATIONS]
        # Filter out zero/tiny values
        valid = [(d, g) for d, g in zip(SEPARATIONS, gammas) if g > 1e-20]
        if len(valid) < 2:
            print(f"  G={G:>6.1f}:  insufficient data")
            continue
        ds, gs = zip(*valid)
        log_d = np.log(np.array(ds, dtype=float))
        log_g = np.log(np.array(gs, dtype=float))
        coeffs = np.polyfit(log_d, log_g, 1)
        slope = coeffs[0]
        print(f"  G={G:>6.1f}:  slope = {slope:>+.3f}  (expect -1.0)")

    # Fit Gamma vs G at each d
    print("\nGamma vs G  (expect slope ~ +1 for linear):")
    for d in SEPARATIONS:
        gammas = [results[(d, G)] for G in COUPLINGS]
        valid = [(G, g) for G, g in zip(COUPLINGS, gammas) if g > 1e-20]
        if len(valid) < 2:
            print(f"  d={d:>3d}:  insufficient data")
            continue
        Gs, gs = zip(*valid)
        log_G = np.log(np.array(Gs, dtype=float))
        log_g = np.log(np.array(gs, dtype=float))
        coeffs = np.polyfit(log_G, log_g, 1)
        slope = coeffs[0]
        print(f"  d={d:>3d}:  slope = {slope:>+.3f}  (expect +1.0)")

    print()
    print("=" * 72)
    print("DONE")
    print("=" * 72)


if __name__ == "__main__":
    main()
