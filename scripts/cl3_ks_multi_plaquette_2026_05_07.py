"""
Cl(3) → KS multi-plaquette estimator.

The single-plaquette toy in cl3_ks_single_plaquette_2026_05_07.py has 1
plaquette per gauge link. A real 3D spatial lattice has more plaquettes
per link.

For a 3D cubic lattice (L³ sites, periodic):
- 3 L³ links (3 directions × L³ sites)
- 3 L³ plaquettes (3 plaquette directions × L³ sites)
- ratio plaquettes/links = 1
- but each LINK is shared by 4 plaquettes (2 plaquette directions
  containing the link × 2 plaquettes per direction containing each
  endpoint)

Per-link ratio of plaquette terms is 4 in the magnetic-energy sum.

Mean-field "K-rescaling" approximation: in the gauge-invariant single-link
effective theory, treat the magnetic term as having effective coupling
K times that of the single-plaquette toy:

    H_K = (g²/2) Ĉ - (K / (g² N_c)) Re Tr U

where K = 4 for 3D cubic, K = 1 for the single-plaquette toy.

This is a mean-field / ignoring-correlations estimate. The TRUE
multi-plaquette computation would couple multiple link variables
through shared plaquettes; this is computationally heavier.

We compute ⟨P⟩_K(g²) for K ∈ {1, 2, 3, 4, 6} and g² across the
canonical range. K=4 corresponds to the 3D-cubic mean-field estimate.
"""

from __future__ import annotations

import numpy as np
from numpy.linalg import eigh

from cl3_ks_single_plaquette_2026_05_07 import (
    casimir,
    fund_tensor_pq,
    antifund_tensor_pq,
    build_basis,
    expectation_re_tr_U_over_Nc,
)


def build_hamiltonian_K(basis, g_squared: float, K: float, N_c: int = 3):
    """
    H = (g²/2) Ĉ - (K / (g² N_c)) Re Tr U   [Wilson-form magnetic, scaled by K]
    """
    n = len(basis)
    idx = {pq: i for i, pq in enumerate(basis)}
    H = np.zeros((n, n), dtype=float)

    for i, (p, q) in enumerate(basis):
        H[i, i] += (g_squared / 2.0) * casimir(p, q)

    coef_mag = -(K / (g_squared * N_c)) * 0.5  # 0.5 because Re Tr = (Tr+Tr*)/2

    for j, mu in enumerate(basis):
        for lam in fund_tensor_pq(*mu):
            if lam in idx:
                H[idx[lam], j] += coef_mag
        for lam in antifund_tensor_pq(*mu):
            if lam in idx:
                H[idx[lam], j] += coef_mag

    H = 0.5 * (H + H.T)
    return H


def scan_K_and_g(basis, g_values, K_values):
    print(f"{'K\\g²':<6}", end="")
    for g2 in g_values:
        print(f"{g2:>10.3f}", end="")
    print()
    print("-" * (6 + 10 * len(g_values)))
    rows = []
    for K in K_values:
        print(f"K={K:<3.1f}", end="")
        row = [K]
        for g2 in g_values:
            H = build_hamiltonian_K(basis, g2, K)
            evals, evecs = eigh(H)
            P = expectation_re_tr_U_over_Nc(evecs[:, 0], basis)
            print(f"{P:>10.6f}", end="")
            row.append(P)
        print()
        rows.append(row)
    return rows


def find_g_match(basis, K: float, target_P: float, g_lo=0.05, g_hi=4.0,
                 tol=1e-8, max_iter=80):
    """Bisect g² to make ⟨P⟩_K(g²) = target_P."""
    def P_at(g2):
        H = build_hamiltonian_K(basis, g2, K)
        evals, evecs = eigh(H)
        return expectation_re_tr_U_over_Nc(evecs[:, 0], basis)

    P_lo = P_at(g_lo)
    P_hi = P_at(g_hi)
    # ⟨P⟩ decreases with increasing g²
    if (P_lo - target_P) * (P_hi - target_P) > 0:
        return None, None  # target not bracketed

    for _ in range(max_iter):
        g_mid = 0.5 * (g_lo + g_hi)
        P_mid = P_at(g_mid)
        if abs(P_mid - target_P) < tol:
            return g_mid, P_mid
        if (P_lo - target_P) * (P_mid - target_P) < 0:
            g_hi = g_mid
            P_hi = P_mid
        else:
            g_lo = g_mid
            P_lo = P_mid
    return 0.5 * (g_lo + g_hi), P_at(0.5 * (g_lo + g_hi))


if __name__ == "__main__":
    basis = build_basis(20.0)
    print(f"Basis: {len(basis)} irreps with C_2 ≤ 20\n")

    print("=== K-scan: ⟨P⟩_GS(g², K) for various plaquette/link ratios ===\n")
    g_values = [0.25, 0.50, 0.75, 1.00, 1.50, 2.00, 4.00]
    K_values = [1, 2, 3, 4, 6, 9]
    rows = scan_K_and_g(basis, g_values, K_values)

    print()
    print("=== K=4 (3D cubic spatial mean-field): canonical g²=1 ===")
    H = build_hamiltonian_K(basis, 1.0, 4)
    evals, evecs = eigh(H)
    P_4_g1 = expectation_re_tr_U_over_Nc(evecs[:, 0], basis)
    print(f"⟨P⟩_K=4(g²=1) = {P_4_g1:.10f}")

    print()
    print("=== Coupling matching: at what g² does each K give ⟨P⟩=0.5934 (MC value)? ===")
    print(f"{'K':>4}  {'g²(MC=0.5934)':>16}  {'⟨P⟩_check':>12}")
    for K in [1, 2, 3, 4, 6, 9]:
        g_match, P_match = find_g_match(basis, K, 0.5934)
        if g_match is None:
            print(f"{K:>4}  {'(not bracketed)':>16}")
        else:
            print(f"{K:>4}  {g_match:>16.6f}  {P_match:>12.6f}")

    print()
    print("=== Coupling matching: at what g² does each K give ⟨P⟩=0.5134 (HK 1-plaq)? ===")
    print(f"{'K':>4}  {'g²(HK=0.5134)':>16}  {'⟨P⟩_check':>12}")
    for K in [1, 2, 3, 4, 6, 9]:
        g_match, P_match = find_g_match(basis, K, 0.5134)
        if g_match is None:
            print(f"{K:>4}  {'(not bracketed)':>16}")
        else:
            print(f"{K:>4}  {g_match:>16.6f}  {P_match:>12.6f}")

    print()
    print("=== Predictions table: framework's ⟨P⟩_KS at canonical g²=1 vs K ===")
    print(f"{'K':>4}  {'⟨P⟩_K(g²=1)':>14}  {'comparator gap':>16}")
    for K in [1, 2, 3, 4, 6, 9]:
        H = build_hamiltonian_K(basis, 1.0, K)
        evals, evecs = eigh(H)
        P = expectation_re_tr_U_over_Nc(evecs[:, 0], basis)
        gap_mc = abs(P - 0.5934)
        print(f"{K:>4}  {P:>14.6f}  {gap_mc:>16.6f}  (vs MC 0.5934)")
