"""
Cl(3) → KS single-plaquette ground-state computation.

Computes the spatial plaquette ground-state expectation in the
Cl(3)-derived Kogut-Susskind Hamiltonian on the smallest non-trivial
volume (1 effective gauge link, 1 plaquette).

Hamiltonian (canonical Cl(3) Tr-form, single coupling g):

    H(g)  =  (g^2 / 2) * C_hat
          -  (1 / (g^2 * N_c)) * Re chi_(1,0)(U)

Hilbert space: L^2(SU(3)) restricted to class functions = span{chi_lambda}
where lambda = (p,q) labels SU(3) irreps.

Matrix elements:
    <chi_lambda | C_hat | chi_mu>     = C_2(lambda) * delta_{lambda,mu}
    <chi_lambda | chi_alpha | chi_mu> = N^lambda_{alpha, mu}     [CG multiplicity]

For SU(3) tensored with fundamental (1,0):
    (1,0) o (p,q)  =  (p+1, q)  +  (p-1, q+1)[p>=1]  +  (p, q-1)[q>=1]
    (0,1) o (p,q)  =  (p, q+1)  +  (p+1, q-1)[q>=1]  +  (p-1, q)[p>=1]
multiplicity 1 in each summand.

Output: <P>_KS(g) at canonical g=1 and a sweep across g.
"""

from __future__ import annotations

import numpy as np
from numpy.linalg import eigh


# -------------------------------------------------------------------
# SU(3) representation theory utilities
# -------------------------------------------------------------------

def casimir(p: int, q: int) -> float:
    """SU(3) quadratic Casimir at trace-form Tr(T_a T_b) = delta_ab/2."""
    return (p * p + p * q + q * q + 3 * p + 3 * q) / 3.0


def dim_irrep(p: int, q: int) -> int:
    """Dimension of SU(3) irrep (p,q)."""
    return ((p + 1) * (q + 1) * (p + q + 2)) // 2


def fund_tensor_pq(p: int, q: int):
    """Decompose (1,0) tensor (p,q) into SU(3) irreps. Returns list of (p',q')."""
    out = [(p + 1, q)]
    if p >= 1:
        out.append((p - 1, q + 1))
    if q >= 1:
        out.append((p, q - 1))
    return out


def antifund_tensor_pq(p: int, q: int):
    """Decompose (0,1) tensor (p,q)."""
    out = [(p, q + 1)]
    if q >= 1:
        out.append((p + 1, q - 1))
    if p >= 1:
        out.append((p - 1, q))
    return out


# -------------------------------------------------------------------
# Build truncated basis of irreps with Casimir <= cutoff
# -------------------------------------------------------------------

def build_basis(casimir_cutoff: float):
    """Enumerate all (p,q) with C_2(p,q) <= cutoff. Returns sorted list."""
    basis = []
    p_max = int(np.ceil(casimir_cutoff)) + 2
    for p in range(p_max + 1):
        for q in range(p_max + 1):
            if casimir(p, q) <= casimir_cutoff:
                basis.append((p, q))
    basis.sort(key=lambda pq: (casimir(*pq), pq))
    return basis


# -------------------------------------------------------------------
# Build Hamiltonian matrix in character basis
# -------------------------------------------------------------------

def build_hamiltonian(basis, g_squared: float, N_c: int = 3):
    """
    Build H(g^2) in the character basis.

    H = (g^2/2) C_hat - (1/(g^2 N_c)) (1/2) (chi_(1,0) + chi_(0,1))

    Matrix elements:
        <chi_lambda | C_hat | chi_mu> = C_2(lambda) delta
        <chi_lambda | chi_(1,0) | chi_mu> = N^lambda_{(1,0), mu}
        <chi_lambda | chi_(0,1) | chi_mu> = N^lambda_{(0,1), mu}
    """
    n = len(basis)
    idx = {pq: i for i, pq in enumerate(basis)}
    H = np.zeros((n, n), dtype=float)

    # Electric (Casimir) term: diagonal
    for i, (p, q) in enumerate(basis):
        H[i, i] += (g_squared / 2.0) * casimir(p, q)

    # Magnetic term: -(1/(g^2 N_c)) * (1/2) [chi_(1,0) + chi_(0,1)]
    coef_mag = -(1.0 / (g_squared * N_c)) * 0.5

    for j, mu in enumerate(basis):
        # chi_(1,0) * chi_mu = sum over (p',q') in fund_tensor(mu)
        for lam in fund_tensor_pq(*mu):
            if lam in idx:
                i = idx[lam]
                H[i, j] += coef_mag

        # chi_(0,1) * chi_mu
        for lam in antifund_tensor_pq(*mu):
            if lam in idx:
                i = idx[lam]
                H[i, j] += coef_mag

    # Symmetrize (numerical safety)
    H = 0.5 * (H + H.T)
    return H


def expectation_re_tr_U_over_Nc(eigvec, basis, N_c: int = 3):
    """
    <psi | (1/N_c) Re Tr U | psi>
    = (1/(2 N_c)) <psi | chi_(1,0) + chi_(0,1) | psi>

    Where <chi_lam | chi_(1,0) | chi_mu> = N^lam_{(1,0), mu}.
    """
    idx = {pq: i for i, pq in enumerate(basis)}
    n = len(basis)

    # Build matrix M = (1/(2 N_c)) (chi_(1,0) + chi_(0,1)) in char basis
    M = np.zeros((n, n), dtype=float)
    for j, mu in enumerate(basis):
        for lam in fund_tensor_pq(*mu):
            if lam in idx:
                M[idx[lam], j] += 1.0 / (2.0 * N_c)
        for lam in antifund_tensor_pq(*mu):
            if lam in idx:
                M[idx[lam], j] += 1.0 / (2.0 * N_c)

    M = 0.5 * (M + M.T)
    return float(eigvec @ M @ eigvec)


# -------------------------------------------------------------------
# Convergence sweep
# -------------------------------------------------------------------

def sweep_cutoff(g_squared: float = 1.0, cutoffs=(4, 6, 8, 10, 12, 16, 20)):
    """Sweep Casimir cutoff at fixed g^2; report ground state and observable."""
    print(f"\n=== Cl(3) → KS single-plaquette, g^2 = {g_squared} ===")
    print(f"{'C2_cut':>6}  {'#irreps':>8}  {'E_0':>14}  {'<P>_GS':>12}")
    rows = []
    for cut in cutoffs:
        basis = build_basis(float(cut))
        H = build_hamiltonian(basis, g_squared)
        evals, evecs = eigh(H)
        psi0 = evecs[:, 0]
        P_gs = expectation_re_tr_U_over_Nc(psi0, basis)
        rows.append((cut, len(basis), evals[0], P_gs))
        print(f"{cut:>6}  {len(basis):>8}  {evals[0]:>14.10f}  {P_gs:>12.10f}")
    return rows


def sweep_coupling(cutoff: float = 16.0, gs=(0.25, 0.5, 1.0, 2.0, 4.0)):
    """Sweep coupling g^2 at fixed cutoff."""
    basis = build_basis(cutoff)
    print(
        f"\n=== Cl(3) → KS single-plaquette, coupling sweep "
        f"(cutoff C_2 ≤ {cutoff}, {len(basis)} irreps) ==="
    )
    print(f"{'g^2':>6}  {'E_0':>14}  {'<P>_GS':>12}")
    rows = []
    for g2 in gs:
        H = build_hamiltonian(basis, g2)
        evals, evecs = eigh(H)
        psi0 = evecs[:, 0]
        P_gs = expectation_re_tr_U_over_Nc(psi0, basis)
        rows.append((g2, evals[0], P_gs))
        print(f"{g2:>6.2f}  {evals[0]:>14.10f}  {P_gs:>12.10f}")
    return rows


# -------------------------------------------------------------------
# Sanity checks
# -------------------------------------------------------------------

def sanity_checks():
    """Verify standard SU(3) facts."""
    print("=== Sanity checks ===")
    assert casimir(1, 0) == 4.0 / 3.0, f"C_2(1,0) = {casimir(1, 0)}"
    assert casimir(0, 1) == 4.0 / 3.0, f"C_2(0,1) = {casimir(0, 1)}"
    assert casimir(1, 1) == 3.0, f"C_2(1,1) = {casimir(1, 1)}"
    assert casimir(0, 0) == 0.0
    assert dim_irrep(1, 0) == 3
    assert dim_irrep(1, 1) == 8
    assert dim_irrep(2, 0) == 6
    assert dim_irrep(2, 1) == 15

    # Tensor products
    assert set(fund_tensor_pq(0, 0)) == {(1, 0)}
    assert set(fund_tensor_pq(1, 0)) == {(2, 0), (0, 1)}
    assert set(fund_tensor_pq(0, 1)) == {(1, 1), (0, 0)}
    assert set(fund_tensor_pq(1, 1)) == {(2, 1), (0, 2), (1, 0)}

    print("  C_2(1,0) = 4/3 ✓")
    print("  C_2(1,1) = 3 ✓")
    print("  dim(8) = 8 ✓")
    print("  fund tensor products ✓")
    print("All sanity checks passed.\n")


if __name__ == "__main__":
    sanity_checks()

    # Convergence: fix canonical g^2 = 1, vary cutoff
    rows_conv = sweep_cutoff(g_squared=1.0)

    # Coupling sweep at converged cutoff
    rows_g = sweep_coupling(cutoff=20.0)

    print("\n=== Summary at canonical g^2 = 1 ===")
    print(f"<P>_KS, ground-state spatial plaquette, single-link toy:")
    print(f"  {rows_conv[-1][3]:.10f}  (cutoff C_2 ≤ {rows_conv[-1][0]})")
    print(f"\nReference comparators:")
    print(f"  Wilson Euclidean MC, β=6:    0.5934 (from existing repo notes)")
    print(f"  Heat-kernel single-plaquette: 0.5134 (= exp(-2/3))")
    print(f"  Wilson 1-plaq V=1 PF certified: 0.4225")
