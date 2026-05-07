"""
Cl(3) → KS two-plaquette computation via Monte Carlo Haar sampling.

Geometry: dumbbell — two squares sharing one edge.
After tree gauge fixing, 2 physical SU(3) link variables (U_AD, U_BE).
Plaquettes: U_p1 = U_BE U_AD^{-1}, U_p2 = U_BE^{-1}.
Magnetic operator: M = -(1/(g²N_c)) [Re Tr(U_BE U_AD^{-1}) + Re Tr U_BE]

Basis: χ_λ(U_AD) χ_μ(U_BE) for (λ, μ) in truncated set, gauge-invariant
under simultaneous conjugation (each character is class-invariant on its
own variable; products are simultaneously-conjugation-invariant).

Note: this basis is INCOMPLETE for L²(SU(3)²)^{global SU(3)} because it
omits "linked" invariants like Tr(U_AD U_BE) which couple the variables.
The result is a VARIATIONAL UPPER BOUND on ground-state energy and
provides a test of how multi-plaquette correlations affect ⟨P⟩.

Matrix elements computed via Monte Carlo numerical integration on
Haar-distributed SU(3) samples.
"""

from __future__ import annotations

import numpy as np
from numpy.linalg import eigh, qr

from cl3_ks_single_plaquette_2026_05_07 import (
    casimir,
    dim_irrep,
    fund_tensor_pq,
    antifund_tensor_pq,
    build_basis as build_irrep_basis,
)


# -------------------------------------------------------------------
# SU(3) Haar sampling
# -------------------------------------------------------------------

def sample_su3(N: int, seed: int = 42) -> np.ndarray:
    """
    Generate N matrices uniformly distributed on SU(3) (Haar measure).

    Method: QR decomposition of complex Gaussian random matrices, with
    phase fixing for uniform U(N), then projecting to SU(N) by adjusting
    the determinant phase.
    """
    rng = np.random.default_rng(seed)
    Z = rng.standard_normal((N, 3, 3)) + 1j * rng.standard_normal((N, 3, 3))
    Q, R = np.linalg.qr(Z)
    # Phase fixing: ensure diagonal of R is positive real
    diag_R = np.diagonal(R, axis1=1, axis2=2)
    phases = diag_R / np.abs(diag_R)  # shape (N, 3)
    # Q' = Q · diag(conj(phases))
    Q = Q * np.conj(phases)[:, np.newaxis, :]  # broadcasting
    # Now project to SU(3): det(Q) is on unit circle; multiply last column
    # by conj(det(Q)) to make det = 1.
    detQ = np.linalg.det(Q)  # shape (N,)
    # multiply last column of Q by conj(detQ)
    Q[:, :, -1] *= np.conj(detQ)[:, np.newaxis]
    return Q


def verify_haar_distribution(N: int = 5000):
    """Sanity check: integrals against characters should match Haar values."""
    print("=== SU(3) Haar sampling sanity check ===")
    samples = sample_su3(N, seed=1)

    # Check unitarity
    products = samples @ np.conj(samples.transpose(0, 2, 1))
    err_unit = np.max(np.abs(products - np.eye(3)[np.newaxis]))
    print(f"  unitarity err (max ||UU† - I||): {err_unit:.2e}")

    # Check det = 1
    dets = np.linalg.det(samples)
    err_det = np.max(np.abs(dets - 1.0))
    print(f"  determinant err (max |det U - 1|): {err_det:.2e}")

    # ∫ Tr(U) dU should be 0 (orthogonality with trivial)
    traces = np.trace(samples, axis1=1, axis2=2)
    avg_trace = np.mean(traces)
    print(f"  ⟨Tr U⟩ (should be 0): {avg_trace.real:.4f} + {avg_trace.imag:.4f}i")

    # ∫ |Tr U|² dU = 1 (orthogonality of fundamental)
    avg_trace_sq = np.mean(np.abs(traces)**2)
    print(f"  ⟨|Tr U|²⟩ (should be 1): {avg_trace_sq:.4f}")

    # ∫ Re(Tr U)² dU = 1/2 (since |Tr U|² = (Re Tr)² + (Im Tr)² and avg same)
    avg_re_sq = np.mean(traces.real**2)
    print(f"  ⟨(Re Tr U)²⟩ (should be 1/2): {avg_re_sq:.4f}")

    print()


# -------------------------------------------------------------------
# Character evaluation
# -------------------------------------------------------------------

def chi_pq(U: np.ndarray, p: int, q: int) -> np.ndarray:
    """
    Compute χ_(p,q)(U) for an array of SU(3) matrices U with shape (N, 3, 3).

    Uses the character formula via traces of fundamental rep.
    For low-dim irreps:
        (0,0): trivial → 1
        (1,0): fundamental → Tr U
        (0,1): antifundamental → Tr U* = (Tr U)*
        (1,1): adjoint = (Tr U)(Tr U*) - 1 = |Tr U|² - 1
        (2,0): symmetric tensor square = (Tr U² + (Tr U)²) / 2
        (0,2): antisymmetric tensor square = (Tr U² + (Tr U)²)* / 2 ... wait this is wrong.

    Actually:
        (2,0) (= "6" of SU(3)): χ = (1/2)(Tr U)² + (1/2) Tr(U²)
        (0,2) (= "6̄"): conjugate, χ = (1/2)(Tr U*)² + (1/2) Tr(U^{*2})
        (2,1) (= "15"): more complicated
        (2,2) (= "27"): more complicated
    """
    N_c = 3
    if (p, q) == (0, 0):
        return np.ones(U.shape[0], dtype=complex)

    tr_U = np.trace(U, axis1=1, axis2=2)
    tr_Ustar = np.conj(tr_U)

    if (p, q) == (1, 0):
        return tr_U
    if (p, q) == (0, 1):
        return tr_Ustar
    if (p, q) == (1, 1):
        return tr_U * tr_Ustar - 1.0

    # Higher: use Tr(U^k)
    U2 = U @ U
    tr_U2 = np.trace(U2, axis1=1, axis2=2)
    tr_U2star = np.conj(tr_U2)

    if (p, q) == (2, 0):
        return (tr_U**2 + tr_U2) / 2.0
    if (p, q) == (0, 2):
        return (tr_Ustar**2 + tr_U2star) / 2.0
    # Note: explicit (2,1) and (1,2) formulas previously coded here were
    # WRONG. The Jacobi-Trudi formula below handles all (p,q) correctly.

    # General formula via Weyl character: chi_(p,q) for SU(3)
    # The Weyl character formula for SU(3) gives, for irrep (p,q):
    #   chi_(p,q) = det[s_{i+lambda_j}] / det[s_{i-1}]
    # which expands as a polynomial in the eigenvalues of U.
    # Numerically, evaluate using Weyl character via power-sum
    # symmetric polynomials (Newton's identities).
    #
    # For SU(3), eigenvalues e1, e2, e3 with e1*e2*e3 = 1.
    # Define power sums:
    #   p_k = e1^k + e2^k + e3^k = Tr U^k
    # Use determinant formula or Schur polynomials.
    #
    # For arbitrary (p, q), use: chi_(p,q)(U) = s_(p,q)(eigenvalues),
    # where s_(p,q) is the Schur polynomial for partition associated with
    # SU(3) Young diagram. For SU(3), the dominant integral weight (p,q)
    # corresponds to partition (p+q, q, 0).
    # Schur via Jacobi-Trudi:
    #   s_lambda = det[h_{lambda_i + j - i}]
    # where h_k = complete homogeneous power sum.
    #
    # h_k can be computed via Newton's recursion from power sums p_k.

    # Get power sums up to k = p+q+2
    max_k = p + q + 2
    Uk = [np.eye(3, dtype=complex)[np.newaxis] * np.ones((U.shape[0], 1, 1))]
    Uk.append(U.copy())
    for k in range(2, max_k + 1):
        Uk.append(np.einsum('nij,njk->nik', Uk[-1], U))
    p_pow = [np.trace(Uk[k], axis1=1, axis2=2) if k > 0
              else 3.0 * np.ones(U.shape[0], dtype=complex)
              for k in range(0, max_k + 1)]

    # Newton's identities to compute h_k:
    # h_0 = 1, h_k = (1/k) sum_{i=1..k} p_i h_{k-i}
    h = [np.ones(U.shape[0], dtype=complex)]
    for k in range(1, max_k + 1):
        h_k = np.zeros(U.shape[0], dtype=complex)
        for i in range(1, k + 1):
            h_k = h_k + p_pow[i] * h[k - i]
        h.append(h_k / k)

    # SU(3) partition lambda = (p+q, q, 0); use Jacobi-Trudi for s_lambda:
    # s_(p+q, q, 0) = det[[h_(p+q), h_(p+q+1), h_(p+q+2)],
    #                       [h_(q-1), h_q,       h_(q+1)],
    #                       [h_(-2),  h_(-1),    h_0]]
    # where h_k = 0 for k < 0.
    # The SU(3) character corresponds to truncating to first n=3 rows.
    def safe_h(k):
        if k < 0:
            return np.zeros(U.shape[0], dtype=complex)
        if k > len(h) - 1:
            return np.zeros(U.shape[0], dtype=complex)
        return h[k]

    # Jacobi-Trudi 3x3 determinant for partition (p+q, q, 0)
    a, b, c = p + q, q, 0
    M = np.zeros((3, 3, U.shape[0]), dtype=complex)
    M[0, 0] = safe_h(a)
    M[0, 1] = safe_h(a + 1)
    M[0, 2] = safe_h(a + 2)
    M[1, 0] = safe_h(b - 1)
    M[1, 1] = safe_h(b)
    M[1, 2] = safe_h(b + 1)
    M[2, 0] = safe_h(c - 2)
    M[2, 1] = safe_h(c - 1)
    M[2, 2] = safe_h(c)

    # 3x3 determinant
    det = (M[0, 0] * (M[1, 1] * M[2, 2] - M[1, 2] * M[2, 1])
            - M[0, 1] * (M[1, 0] * M[2, 2] - M[1, 2] * M[2, 0])
            + M[0, 2] * (M[1, 0] * M[2, 1] - M[1, 1] * M[2, 0]))
    return det


# -------------------------------------------------------------------
# Build truncated character basis
# -------------------------------------------------------------------

def build_two_link_basis(casimir_cutoff: float = 4.0):
    """Tensor product basis: (λ_AD, λ_BE) with both Casimirs ≤ cutoff."""
    irreps = []
    for p in range(4):
        for q in range(4):
            if casimir(p, q) <= casimir_cutoff:
                irreps.append((p, q))
    pairs = [(a, b) for a in irreps for b in irreps]
    return irreps, pairs


# -------------------------------------------------------------------
# Build Hamiltonian via Monte Carlo
# -------------------------------------------------------------------

def build_hamiltonian_dumbbell(g_squared: float, casimir_cutoff: float = 4.0,
                                N_samples: int = 20000, seed: int = 7,
                                N_c: int = 3):
    """
    Build the 2-plaquette dumbbell Hamiltonian in the truncated
    χ_λ(U_AD) χ_μ(U_BE) basis via Monte Carlo Haar integration.

    H = (g²/2) (Ĉ_AD + Ĉ_BE)  [diagonal]
      - (1/(g² N_c)) [Re Tr(U_BE U_AD^{-1}) + Re Tr U_BE]

    Returns: H, Gram matrix, basis_pairs.
    """
    irreps, pairs = build_two_link_basis(casimir_cutoff)
    n = len(pairs)

    print(f"  Basis: {n} pairs ({len(irreps)} irreps each link)")

    # Sample Haar pairs
    print(f"  Sampling {N_samples} (U, V) pairs from Haar²...")
    U_AD = sample_su3(N_samples, seed=seed)
    U_BE = sample_su3(N_samples, seed=seed + 1)

    # Compute basis functions at each sample
    print(f"  Evaluating basis functions...")
    chi_table = np.zeros((len(irreps), N_samples), dtype=complex)
    chi_table_BE = np.zeros((len(irreps), N_samples), dtype=complex)
    for i, lam in enumerate(irreps):
        chi_table[i] = chi_pq(U_AD, *lam)
        chi_table_BE[i] = chi_pq(U_BE, *lam)

    # Basis function values: f_(λ, μ)(U, V) = χ_λ(U) χ_μ(V)
    # Index pair (λ, μ) → flat index i*len(irreps) + j
    F = np.zeros((n, N_samples), dtype=complex)
    for k, (a, b) in enumerate(pairs):
        ia = irreps.index(a)
        ib = irreps.index(b)
        F[k] = chi_table[ia] * chi_table_BE[ib]

    # Gram matrix G_{αβ} = <f_α | f_β> = mean over samples of f_α* f_β
    print(f"  Computing Gram matrix...")
    Gram = (np.conj(F) @ F.T) / N_samples

    # Magnetic operator at each sample
    print(f"  Evaluating magnetic operator at samples...")
    # Re Tr(U_BE U_AD^{-1}) = Re Tr(U_BE @ U_AD^*) for U_AD ∈ SU(3)
    UAD_inv = np.conj(U_AD.transpose(0, 2, 1))  # for unitary, U^{-1} = U†
    prod_BE_AD_inv = np.einsum('nij,njk->nik', U_BE, UAD_inv)
    re_tr_p1 = np.trace(prod_BE_AD_inv, axis1=1, axis2=2).real
    re_tr_p2 = np.trace(U_BE, axis1=1, axis2=2).real
    M_values = -(1.0 / (g_squared * N_c)) * (re_tr_p1 + re_tr_p2)

    # Magnetic matrix: M_{αβ} = <f_α | M | f_β> = mean of f_α* M f_β
    print(f"  Computing magnetic matrix...")
    H_mag = (np.conj(F) * M_values[np.newaxis, :]) @ F.T / N_samples

    # Electric (Casimir) matrix: diagonal in irrep basis
    H_E = np.zeros((n, n), dtype=complex)
    for k, (a, b) in enumerate(pairs):
        H_E[k, k] = (g_squared / 2.0) * (casimir(*a) + casimir(*b))

    H = H_E + H_mag
    H = 0.5 * (H + np.conj(H.T))  # Hermitize

    return H, Gram, pairs, F, U_AD, U_BE


def diagonalize_with_gram(H: np.ndarray, Gram: np.ndarray):
    """Solve generalized eigenvalue problem H ψ = E G ψ."""
    # Symmetrize Gram (numerical)
    Gram = 0.5 * (Gram + np.conj(Gram.T))
    # Diagonalize Gram first to find a non-singular basis
    g_evals, g_evecs = eigh(Gram)
    # Keep modes with eigenvalue > tol
    tol = 1e-6
    keep = g_evals > tol
    g_inv_sqrt = np.zeros_like(g_evals)
    g_inv_sqrt[keep] = 1.0 / np.sqrt(g_evals[keep])
    P = g_evecs[:, keep] * g_inv_sqrt[keep][np.newaxis, :]
    # Transformed H in orthonormalized basis
    H_orth = np.conj(P.T) @ H @ P
    H_orth = 0.5 * (H_orth + np.conj(H_orth.T))
    evals, evecs_orth = eigh(H_orth)
    # Bring back to original basis
    evecs = P @ evecs_orth
    return evals, evecs, np.sum(keep)


def expectation_P(psi, F, U_BE, U_AD, N_c: int = 3):
    """⟨ψ | (1/N_c) Re Tr U_p1 + (1/N_c) Re Tr U_p2 | ψ⟩ / norm — average plaquette."""
    UAD_inv = np.conj(U_AD.transpose(0, 2, 1))
    prod_BE_AD_inv = np.einsum('nij,njk->nik', U_BE, UAD_inv)
    re_tr_p1 = np.trace(prod_BE_AD_inv, axis1=1, axis2=2).real
    re_tr_p2 = np.trace(U_BE, axis1=1, axis2=2).real
    P_values = (re_tr_p1 + re_tr_p2) / (2.0 * N_c)  # average of the two plaquettes

    # ψ in original basis: <P>_ψ = mean over samples of |ψ(U,V)|² P(U,V)
    psi_at_samples = np.conj(psi) @ F  # shape (N_samples,)
    norm = np.mean(np.abs(psi_at_samples)**2)
    expectation = np.mean(np.abs(psi_at_samples)**2 * P_values) / norm
    return expectation


# -------------------------------------------------------------------
# Run
# -------------------------------------------------------------------

if __name__ == "__main__":
    verify_haar_distribution(N=5000)

    print("=== 2-plaquette dumbbell, Cl(3) → KS Hamiltonian ===")
    print()

    # Convergence test: sweep N_samples at fixed g²=1
    print("--- Convergence: N_samples sweep at g²=1, Casimir cutoff = 4 ---")
    print(f"{'N':>8}  {'#basis':>8}  {'E_0':>14}  {'⟨P⟩_avg':>10}")
    for N in [5000, 10000, 20000, 50000]:
        H, G, pairs, F, U1, U2 = build_hamiltonian_dumbbell(
            g_squared=1.0, casimir_cutoff=4.0, N_samples=N, seed=7
        )
        evals, evecs, nkeep = diagonalize_with_gram(H, G)
        psi0 = evecs[:, 0]
        P = expectation_P(psi0, F, U2, U1)
        print(f"{N:>8}  {len(pairs):>8}  {evals[0].real:>14.6f}  {P:>10.6f}  "
              f"({nkeep} kept)")

    print()
    print("--- Cutoff sweep at g²=1, N=50000 (capped at C2≤5 since χ_(0,3) not coded) ---")
    print(f"{'cutoff':>8}  {'#basis':>8}  {'E_0':>14}  {'⟨P⟩_avg':>10}")
    for cut in [3.0, 4.0, 5.0]:
        H, G, pairs, F, U1, U2 = build_hamiltonian_dumbbell(
            g_squared=1.0, casimir_cutoff=cut, N_samples=50000, seed=7
        )
        evals, evecs, nkeep = diagonalize_with_gram(H, G)
        psi0 = evecs[:, 0]
        P = expectation_P(psi0, F, U2, U1)
        print(f"{cut:>8.1f}  {len(pairs):>8}  {evals[0].real:>14.6f}  {P:>10.6f}  "
              f"({nkeep} kept)")

    print()
    print("--- Per-plaquette breakdown at g²=1, cutoff=4, N=50000 ---")
    H, G, pairs, F, U1, U2 = build_hamiltonian_dumbbell(
        g_squared=1.0, casimir_cutoff=4.0, N_samples=50000, seed=7
    )
    evals, evecs, nkeep = diagonalize_with_gram(H, G)
    psi0 = evecs[:, 0]
    UAD_inv = np.conj(U1.transpose(0, 2, 1))
    p1 = np.trace(np.einsum('nij,njk->nik', U2, UAD_inv), axis1=1, axis2=2).real / 3
    p2 = np.trace(U2, axis1=1, axis2=2).real / 3
    psi_at_samples = np.conj(psi0) @ F
    norm = np.mean(np.abs(psi_at_samples)**2)
    P1_exp = np.mean(np.abs(psi_at_samples)**2 * p1) / norm
    P2_exp = np.mean(np.abs(psi_at_samples)**2 * p2) / norm
    print(f"  ⟨P_1⟩ = ⟨(1/N_c) Re Tr (U_BE U_AD^-1)⟩ = {P1_exp:>10.6f}")
    print(f"  ⟨P_2⟩ = ⟨(1/N_c) Re Tr U_BE⟩            = {P2_exp:>10.6f}")
    print(f"  Average = {(P1_exp + P2_exp)/2:>10.6f}")
    print()
    print("  If P_1 ≈ 0 in product basis: indicates the basis cannot capture")
    print("  U_BE-U_AD correlations; multi-plaquette correlation requires")
    print("  'linked' invariants (Tr U_BE U_AD etc.) beyond single-edge characters.")

    print()
    print("--- Coupling sweep at cutoff=4, N=50000 ---")
    print(f"{'g²':>6}  {'E_0':>14}  {'⟨P⟩_avg':>10}")
    for g2 in [0.50, 0.75, 1.00, 1.50, 2.00]:
        H, G, pairs, F, U1, U2 = build_hamiltonian_dumbbell(
            g_squared=g2, casimir_cutoff=4.0, N_samples=50000, seed=7
        )
        evals, evecs, nkeep = diagonalize_with_gram(H, G)
        psi0 = evecs[:, 0]
        P = expectation_P(psi0, F, U2, U1)
        print(f"{g2:>6.2f}  {evals[0].real:>14.6f}  {P:>10.6f}")

    print()
    print("=== Comparison to single-plaquette toy ===")
    print(f"  Single-plaq toy (g²=1): ⟨P⟩ = 0.218104")
    print(f"  This 2-plaquette dumbbell: see results above")
    print()
    print("If ⟨P⟩_2plaq > 0.218 at g²=1, multi-plaquette correlations")
    print("push the framework's prediction toward the MC value 0.5934.")
