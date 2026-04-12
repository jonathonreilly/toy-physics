#!/usr/bin/env python3
"""Penrose gravity-induced collapse threshold on 2D periodic lattices.

Tests whether the Quantum Zeno threshold G_Zeno maps to Penrose's
gravity-induced collapse timescale:  Gamma = E_G / hbar.

Protocol:
  1. On 2D periodic lattices (side = 6, 8, 10, 12):
     - Initialize Gaussian at center (sigma = 1.5)
     - Sweep G in [1, 5, 10, 20, 50, 100, 200, 500]
     - Measure Zeno time t_Z and gravitational self-energy E_self
  2. Test Penrose prediction: t_Z ~ 1/E_self  (linear plot)
  3. Check t_Z vs G (should be ~ 1/G)
  4. Compute Penrose ratio R_P = t_Z * |E_self| (should be constant)
  5. Compare across lattice sizes for finite-size vs physical effects

PStack experiment: penrose-zeno-threshold
"""

from __future__ import annotations

import numpy as np
from scipy import sparse
from scipy.sparse.linalg import spsolve

# ---------------------------------------------------------------------------
# Physical parameters
# ---------------------------------------------------------------------------
MASS = 0.30
MU2 = 0.22
DT = 0.12
N_STEPS = 60
SIGMA = 1.5

G_VALUES = [1, 5, 10, 20, 50, 100, 200, 500]
SIZE_SCAN = [6, 8, 10, 12]


# ---------------------------------------------------------------------------
# 2D periodic lattice
# ---------------------------------------------------------------------------
def make_2d_periodic_lattice(side: int):
    """Build a 2D periodic square lattice."""
    n = side * side
    pos = np.zeros((n, 2))
    col = np.zeros(n, dtype=int)
    idx = {}

    for ix in range(side):
        for iy in range(side):
            i = ix * side + iy
            pos[i] = [ix, iy]
            col[i] = (ix + iy) % 2
            idx[(ix, iy)] = i

    adj = [[] for _ in range(n)]
    rows, cols_sp, vals = [], [], []

    for ix in range(side):
        for iy in range(side):
            i = idx[(ix, iy)]
            neighbors = [
                idx[((ix + 1) % side, iy)],
                idx[((ix - 1) % side, iy)],
                idx[(ix, (iy + 1) % side)],
                idx[(ix, (iy - 1) % side)],
            ]
            adj[i] = neighbors
            deg = len(neighbors)
            rows.append(i); cols_sp.append(i); vals.append(-float(deg))
            for j in neighbors:
                rows.append(i); cols_sp.append(j); vals.append(1.0)

    L = sparse.csc_matrix((vals, (rows, cols_sp)), shape=(n, n))
    return pos, col, L, adj, n


# ---------------------------------------------------------------------------
# Operators
# ---------------------------------------------------------------------------
def solve_phi(rho, L, mu2, G, n):
    """Screened Poisson: (L + mu^2 I) phi = G * rho."""
    A = (L + mu2 * sparse.eye(n)).tocsc()
    return spsolve(A, G * rho)


def make_hamiltonian(phi, col, adj, n):
    """Staggered Hamiltonian with parity coupling.

    H[i,i] = (MASS + phi[i]) * par[i]   (par = +1 even / -1 odd)
    H[i,j] = -i/2 for neighbors (antisymmetric hopping)
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


def cn_step(psi, H, dt, n):
    """Crank-Nicolson time step."""
    I = sparse.eye(n, dtype=complex, format="csc")
    A_plus = (I + 1j * H * dt / 2).tocsc()
    A_minus = I - 1j * H * dt / 2
    return spsolve(A_plus, A_minus.dot(psi))


# ---------------------------------------------------------------------------
# Wavepacket utilities
# ---------------------------------------------------------------------------
def gaussian_2d(pos, center, sigma, n):
    """Normalized 2D Gaussian."""
    dx = pos[:, 0] - center[0]
    dy = pos[:, 1] - center[1]
    psi = np.exp(-0.5 * (dx**2 + dy**2) / sigma**2).astype(complex)
    psi /= np.sqrt(np.sum(np.abs(psi)**2))
    return psi


def width(psi, pos):
    """RMS width of wavepacket."""
    prob = np.abs(psi)**2
    prob /= np.sum(prob)
    cx = np.sum(prob * pos[:, 0])
    cy = np.sum(prob * pos[:, 1])
    dx = pos[:, 0] - cx
    dy = pos[:, 1] - cy
    return np.sqrt(np.sum(prob * (dx**2 + dy**2)))


# ---------------------------------------------------------------------------
# Self-energy measurement
# ---------------------------------------------------------------------------
def measure_self_energy(psi, G, L, col, adj, n):
    """Gravitational self-energy: E_self = <psi|H_grav|psi> - <psi|H_free|psi>.

    This is the energy cost of the gravitational self-interaction.
    """
    rho = np.abs(psi)**2
    phi = solve_phi(rho, L, MU2, G, n)
    H_grav = make_hamiltonian(phi, col, adj, n)
    H_free = make_hamiltonian(np.zeros(n), col, adj, n)
    e_grav = np.real(np.conj(psi) @ H_grav.dot(psi))
    e_free = np.real(np.conj(psi) @ H_free.dot(psi))
    return e_grav - e_free


# ---------------------------------------------------------------------------
# Zeno time measurement
# ---------------------------------------------------------------------------
def measure_zeno_time(psi0, G, L, col, adj, n, pos, n_steps=N_STEPS):
    """Evolve under self-gravity, find Zeno time.

    t_Z: first step where width(t+1) <= width(t) * 1.001
    Also returns full width trajectory.
    """
    psi = psi0.copy().astype(complex)
    widths = [width(psi, pos)]

    for step in range(n_steps):
        rho = np.abs(psi)**2
        phi = solve_phi(rho, L, MU2, G, n) if G > 0 else np.zeros(n)
        H = make_hamiltonian(phi, col, adj, n)
        psi = cn_step(psi, H, DT, n)
        psi /= np.sqrt(np.sum(np.abs(psi)**2))
        widths.append(width(psi, pos))

    widths = np.array(widths)

    # Zeno time: first step where width stops growing
    t_z = n_steps  # default: never freezes
    for t in range(1, len(widths)):
        if widths[t] <= widths[t - 1] * 1.001:
            t_z = t
            break

    return t_z, widths


# ---------------------------------------------------------------------------
# Main experiment
# ---------------------------------------------------------------------------
def main():
    print("=" * 72)
    print("FRONTIER: Penrose Gravity-Induced Collapse Threshold")
    print("=" * 72)
    print(f"  MASS={MASS}, MU2={MU2}, DT={DT}, N_STEPS={N_STEPS}, SIGMA={SIGMA}")
    print(f"  Penrose conjecture: t_Z ~ 1/E_self => R_P = t_Z * |E_self| ~ const")
    print()

    # Storage for all results
    results = {}  # (side, G) -> (t_z, E_self, R_P)

    # ===================================================================
    # Part 1: Sweep G on each lattice size
    # ===================================================================
    for side in SIZE_SCAN:
        n = side * side
        print(f"[side={side}] {side}x{side} periodic lattice (n={n})")
        print("-" * 72)

        pos, col, L, adj, _ = make_2d_periodic_lattice(side)
        center = np.array([side / 2.0, side / 2.0])
        psi0 = gaussian_2d(pos, center, SIGMA, n)
        w0 = width(psi0, pos)
        print(f"  Initial width: {w0:.4f}")
        print()

        header = (f"  {'G':>6s}  {'t_Z':>5s}  {'E_self':>12s}  "
                  f"{'|E_self|':>12s}  {'R_P':>12s}  {'w_final':>8s}")
        print(header)
        print("  " + "-" * 65)

        for G in G_VALUES:
            # Measure self-energy at initial state
            E_self = measure_self_energy(psi0, G, L, col, adj, n)

            # Measure Zeno time
            t_z, widths = measure_zeno_time(psi0, G, L, col, adj, n, pos)

            # Penrose ratio
            abs_E = abs(E_self)
            R_P = t_z * abs_E if abs_E > 1e-15 else float("inf")

            results[(side, G)] = (t_z, E_self, R_P)
            w_final = widths[-1]

            print(f"  {G:>6d}  {t_z:>5d}  {E_self:>12.6f}  "
                  f"{abs_E:>12.6f}  {R_P:>12.4f}  {w_final:>8.4f}")

        print()

    # ===================================================================
    # Part 2: Penrose prediction check: t_Z vs 1/|E_self|
    # ===================================================================
    print("=" * 72)
    print("ANALYSIS: Penrose Prediction t_Z ~ 1/|E_self|")
    print("=" * 72)

    for side in SIZE_SCAN:
        n = side * side
        t_zs = []
        inv_Es = []
        for G in G_VALUES:
            t_z, E_self, R_P = results[(side, G)]
            abs_E = abs(E_self)
            if abs_E > 1e-15 and t_z < N_STEPS:
                t_zs.append(t_z)
                inv_Es.append(1.0 / abs_E)

        if len(t_zs) >= 3:
            t_zs = np.array(t_zs, dtype=float)
            inv_Es = np.array(inv_Es)
            # Linear fit: t_Z = a * (1/|E_self|) + b
            A = np.vstack([inv_Es, np.ones(len(inv_Es))]).T
            slope, intercept = np.linalg.lstsq(A, t_zs, rcond=None)[0]
            # Correlation coefficient
            corr = np.corrcoef(inv_Es, t_zs)[0, 1] if len(t_zs) > 1 else 0.0
            print(f"  side={side}: slope={slope:.4f}, intercept={intercept:.2f}, "
                  f"r={corr:.4f} (N={len(t_zs)} points)")
            if abs(corr) > 0.9:
                print(f"    -> STRONG linear: Penrose prediction CONFIRMED")
            elif abs(corr) > 0.7:
                print(f"    -> Moderate linear: partial Penrose agreement")
            else:
                print(f"    -> Weak/no linear: Penrose prediction FAILS")
        else:
            print(f"  side={side}: insufficient data (need >= 3 points with t_Z < N_STEPS)")
    print()

    # ===================================================================
    # Part 3: t_Z vs G (should be ~ 1/G)
    # ===================================================================
    print("=" * 72)
    print("ANALYSIS: t_Z vs G (expect ~ 1/G)")
    print("=" * 72)

    for side in SIZE_SCAN:
        t_zs = []
        Gs = []
        for G in G_VALUES:
            t_z, E_self, R_P = results[(side, G)]
            if t_z < N_STEPS:
                t_zs.append(t_z)
                Gs.append(G)

        if len(t_zs) >= 3:
            t_zs_arr = np.array(t_zs, dtype=float)
            Gs_arr = np.array(Gs, dtype=float)
            inv_Gs = 1.0 / Gs_arr

            # Fit t_Z = a / G + b
            A = np.vstack([inv_Gs, np.ones(len(inv_Gs))]).T
            slope, intercept = np.linalg.lstsq(A, t_zs_arr, rcond=None)[0]
            corr = np.corrcoef(inv_Gs, t_zs_arr)[0, 1] if len(t_zs) > 1 else 0.0
            print(f"  side={side}: t_Z ~ {slope:.2f}/G + {intercept:.2f}, "
                  f"r={corr:.4f}")
        else:
            print(f"  side={side}: insufficient data")
    print()

    # ===================================================================
    # Part 4: t_Z vs lattice size (weak = physical, strong = finite-size)
    # ===================================================================
    print("=" * 72)
    print("ANALYSIS: t_Z vs lattice size (finite-size check)")
    print("=" * 72)

    print(f"  {'G':>6s}", end="")
    for side in SIZE_SCAN:
        print(f"  {'n='+str(side*side):>8s}", end="")
    print(f"  {'spread':>8s}  {'verdict':>12s}")
    print("  " + "-" * (6 + 10 * len(SIZE_SCAN) + 22))

    for G in G_VALUES:
        row = f"  {G:>6d}"
        t_zs_across = []
        for side in SIZE_SCAN:
            t_z, _, _ = results[(side, G)]
            row += f"  {t_z:>8d}"
            t_zs_across.append(t_z)

        vals = np.array(t_zs_across, dtype=float)
        spread = np.max(vals) - np.min(vals)
        mean_t = np.mean(vals)
        rel_spread = spread / mean_t if mean_t > 0 else 0
        verdict = "PHYSICAL" if rel_spread < 0.3 else "FINITE-SIZE"
        row += f"  {spread:>8.1f}  {verdict:>12s}"
        print(row)
    print()

    # ===================================================================
    # Part 5: Penrose ratio R_P = t_Z * |E_self|
    # ===================================================================
    print("=" * 72)
    print("PENROSE RATIO: R_P = t_Z * |E_self| (should be ~ constant)")
    print("=" * 72)

    for side in SIZE_SCAN:
        R_Ps = []
        print(f"\n  side={side}:")
        print(f"    {'G':>6s}  {'t_Z':>5s}  {'|E_self|':>12s}  {'R_P':>12s}")
        print(f"    " + "-" * 40)
        for G in G_VALUES:
            t_z, E_self, R_P = results[(side, G)]
            abs_E = abs(E_self)
            if t_z < N_STEPS and abs_E > 1e-15:
                R_Ps.append(R_P)
            print(f"    {G:>6d}  {t_z:>5d}  {abs_E:>12.6f}  {R_P:>12.4f}")

        if len(R_Ps) >= 2:
            R_arr = np.array(R_Ps)
            mean_R = np.mean(R_arr)
            std_R = np.std(R_arr)
            cv = std_R / mean_R if mean_R > 0 else float("inf")
            print(f"    mean(R_P)={mean_R:.4f}, std={std_R:.4f}, "
                  f"CV={cv:.3f}")
            if cv < 0.2:
                print(f"    -> R_P CONSTANT: Penrose conjecture CONFIRMED")
            elif cv < 0.5:
                print(f"    -> R_P moderately stable: partial Penrose")
            else:
                print(f"    -> R_P varies: collapse differs from Penrose")
    print()

    # ===================================================================
    # Grand Summary
    # ===================================================================
    print("=" * 72)
    print("GRAND SUMMARY")
    print("=" * 72)

    # Aggregate Penrose ratio across all valid points
    all_R_Ps = []
    for side in SIZE_SCAN:
        for G in G_VALUES:
            t_z, E_self, R_P = results[(side, G)]
            if t_z < N_STEPS and abs(E_self) > 1e-15:
                all_R_Ps.append(R_P)

    if all_R_Ps:
        R_all = np.array(all_R_Ps)
        mean_all = np.mean(R_all)
        std_all = np.std(R_all)
        cv_all = std_all / mean_all if mean_all > 0 else float("inf")
        print(f"  Global Penrose ratio: R_P = {mean_all:.4f} +/- {std_all:.4f} "
              f"(CV={cv_all:.3f}, N={len(all_R_Ps)})")
        if cv_all < 0.2:
            print(f"  -> Penrose conjecture CONFIRMED: t_Z * |E_self| ~ const")
        elif cv_all < 0.5:
            print(f"  -> Partial agreement with Penrose")
        else:
            print(f"  -> Penrose conjecture NOT confirmed: R_P varies too much")
    else:
        print("  No valid data points (all t_Z = N_STEPS)")

    # E_self scaling check
    print()
    print("  E_self scaling with G (expect E_self ~ G):")
    for side in SIZE_SCAN:
        Es = []
        Gs_valid = []
        for G in G_VALUES:
            _, E_self, _ = results[(side, G)]
            Es.append(abs(E_self))
            Gs_valid.append(G)
        Es = np.array(Es)
        Gs_arr = np.array(Gs_valid, dtype=float)
        if len(Es) >= 2:
            # Fit |E_self| = a * G
            slope = np.sum(Es * Gs_arr) / np.sum(Gs_arr**2)
            residuals = Es - slope * Gs_arr
            r2 = 1 - np.sum(residuals**2) / np.sum((Es - np.mean(Es))**2)
            print(f"    side={side}: |E_self| ~ {slope:.6f} * G  (R^2={r2:.4f})")

    print()
    print("=" * 72)
    print("DONE")
    print("=" * 72)


if __name__ == "__main__":
    main()
