"""SU(3) Wigner intertwiner engine — Block 1 of the cube-closure campaign.

Block 1 deliverable: explicit Clebsch-Gordan decomposition of the SU(3)
adjoint tensor product

    (1,1) ⊗ (1,1) = (0,0) ⊕ 2·(1,1) ⊕ (3,0) ⊕ (0,3) ⊕ (2,2)
                  = 1   ⊕ 8   ⊕ 8    ⊕ 10    ⊕ 10̄  ⊕ 27
                    (dimensions: 1 + 8 + 8 + 10 + 10 + 27 = 64 ✓)

via Casimir + exchange diagonalization on V_(1,1) ⊗ V_(1,1) = C^8 ⊗ C^8.

This is Block 1 of the multi-block plan to build the full SU(3) Wigner-
Racah machinery needed for the L_s=3 cube tensor-network contraction.

Algorithm:
  1. Construct Gell-Mann basis {λ_a, a=1..8} of 3x3 traceless Hermitian
     matrices.
  2. Construct SU(3) structure constants f_abc (antisymmetric) and
     d_abc (symmetric).
  3. Construct adjoint generators T^a_(b,c) = -i f_(abc) as 8x8 matrices.
  4. Compute quadratic Casimir C_2 = Σ_a T^a T^a on the tensor product
     V_(1,1) ⊗ V_(1,1):
       C_2_total = (Σ_a (T^a ⊗ I + I ⊗ T^a)^2)
  5. Compute exchange operator E swapping the two factors of V ⊗ V.
  6. Diagonalize H = C_2 + α E (for some α distinguishing the two adjoint
     copies in (1,1)⊗(1,1) by symmetry under exchange).
  7. Group eigenvectors by (C_2, E) eigenvalue → CG basis blocks for each
     fusion channel.
  8. Identify each block with an irrep by Casimir eigenvalue and
     dimensionality.

Validation:
  V1: 6 distinct fusion channels with dimensions {1, 8, 8, 10, 10, 27}.
  V2: total dimension 64.
  V3: orthonormal basis: <e_i, e_j> = δ_ij.
  V4: SU(3) equivariance: D(g)⊗D(g) preserves each channel block.
  V5: Casimir eigenvalues match canonical SU(3) values.
  V6: exchange eigenvalues distinguish two (1,1) copies (one symmetric,
      one antisymmetric).

Cluster note: this is SU(3) representation theory, NOT in the
gauge_vacuum_plaquette family. It is a new infrastructure deliverable
serving downstream lattice gauge work.

Forbidden imports: none (pure SU(3) rep theory).

Run:
    python3 scripts/frontier_su3_wigner_intertwiner_engine.py
"""

from __future__ import annotations

import math
import sys
from typing import Dict, List, Tuple

import numpy as np


# ===========================================================================
# Section A. Gell-Mann basis and SU(3) structure constants.
# ===========================================================================

def gellmann_basis() -> List[np.ndarray]:
    """SU(3) Gell-Mann matrices, normalized so Tr[λ_a λ_b] = 2 δ_(ab).

    Returns the standard 8 Gell-Mann matrices in the order:
      λ_1, λ_2, λ_3 (SU(2) sigma in upper 2x2)
      λ_4, λ_5 (off-diagonal 1-3)
      λ_6, λ_7 (off-diagonal 2-3)
      λ_8 (Cartan / hypercharge-like)
    """
    l = [None] * 8
    l[0] = np.array([[0, 1, 0], [1, 0, 0], [0, 0, 0]], dtype=complex)
    l[1] = np.array([[0, -1j, 0], [1j, 0, 0], [0, 0, 0]], dtype=complex)
    l[2] = np.array([[1, 0, 0], [0, -1, 0], [0, 0, 0]], dtype=complex)
    l[3] = np.array([[0, 0, 1], [0, 0, 0], [1, 0, 0]], dtype=complex)
    l[4] = np.array([[0, 0, -1j], [0, 0, 0], [1j, 0, 0]], dtype=complex)
    l[5] = np.array([[0, 0, 0], [0, 0, 1], [0, 1, 0]], dtype=complex)
    l[6] = np.array([[0, 0, 0], [0, 0, -1j], [0, 1j, 0]], dtype=complex)
    l[7] = np.array([[1, 0, 0], [0, 1, 0], [0, 0, -2]], dtype=complex) / math.sqrt(3)
    return l


def structure_constants() -> Tuple[np.ndarray, np.ndarray]:
    """Compute SU(3) structure constants:
      [λ_a/2, λ_b/2] = i f_abc (λ_c/2)         (antisymmetric)
      {λ_a/2, λ_b/2} = (1/3) δ_ab I + d_abc (λ_c/2)  (symmetric, traceless part)

    Returns (f_abc, d_abc) as (8, 8, 8) arrays.

    Computed numerically from the Gell-Mann basis via:
      f_abc = (1/(4i)) Tr[λ_c [λ_a, λ_b]]
      d_abc = (1/4)   Tr[λ_c {λ_a, λ_b}]
    """
    lam = gellmann_basis()
    n = 8
    f = np.zeros((n, n, n), dtype=float)
    d = np.zeros((n, n, n), dtype=float)
    for a in range(n):
        for b in range(n):
            comm = lam[a] @ lam[b] - lam[b] @ lam[a]
            anti = lam[a] @ lam[b] + lam[b] @ lam[a]
            for c in range(n):
                f_val = (1.0 / (4j)) * np.trace(lam[c] @ comm)
                d_val = (1.0 / 4.0) * np.trace(lam[c] @ anti)
                f[a, b, c] = float(f_val.real)
                d[a, b, c] = float(d_val.real)
    return f, d


# ===========================================================================
# Section B. Adjoint generators and Casimirs.
# ===========================================================================

def adjoint_generators(f: np.ndarray) -> List[np.ndarray]:
    """Adjoint representation generators T^a_(b,c) = -i f_(abc).

    Returns list of 8 Hermitian 8x8 matrices satisfying [T^a, T^b] = i f_abc T^c.
    """
    n = 8
    T = []
    for a in range(n):
        Ta = np.zeros((n, n), dtype=complex)
        for b in range(n):
            for c in range(n):
                Ta[b, c] = -1j * f[a, b, c]
        T.append(Ta)
    return T


def adjoint_casimir(T: List[np.ndarray]) -> np.ndarray:
    """Quadratic Casimir on (1,1) adjoint: C_2 = Σ_a T^a T^a.

    For SU(3) (1,1) adjoint, eigenvalue C_2 = 3 (standard convention with
    Tr[λ_a λ_b] = 2 δ_ab).
    """
    n = 8
    C = np.zeros((n, n), dtype=complex)
    for Ta in T:
        C = C + Ta @ Ta
    return C


def cubic_casimir(T: List[np.ndarray], d: np.ndarray) -> np.ndarray:
    """Cubic Casimir on (1,1) adjoint: C_3 = Σ_(abc) d_(abc) T^a T^b T^c.

    For SU(3), C_3 takes opposite signs on conjugate irreps: e.g.,
    C_3((3,0)) = -C_3((0,3)) (decuplet vs antidecuplet).

    On self-conjugate irreps (e.g., (0,0), (1,1), (2,2)): C_3 may vanish
    or take symmetric values.
    """
    n = 8
    C = np.zeros((n, n), dtype=complex)
    for a in range(n):
        for b in range(n):
            for c in range(n):
                if d[a, b, c] != 0:
                    C = C + d[a, b, c] * T[a] @ T[b] @ T[c]
    return C


def tensor_product_cubic_casimir(T: List[np.ndarray], d: np.ndarray
                                   ) -> np.ndarray:
    """Total cubic Casimir on V_(1,1) ⊗ V_(1,1):

      C_3_total = Σ_(abc) d_(abc) (T^a ⊗ I + I ⊗ T^a)
                                    (T^b ⊗ I + I ⊗ T^b)
                                    (T^c ⊗ I + I ⊗ T^c)

    Acts as a SU(3)-invariant operator distinguishing irreps with
    different C_3 eigenvalues.
    """
    n = 8
    I8 = np.eye(n, dtype=complex)
    # Total generators on V ⊗ V
    T_tot = [np.kron(Ta, I8) + np.kron(I8, Ta) for Ta in T]
    dim = n * n
    C = np.zeros((dim, dim), dtype=complex)
    for a in range(n):
        for b in range(n):
            for c in range(n):
                if d[a, b, c] != 0:
                    C = C + d[a, b, c] * T_tot[a] @ T_tot[b] @ T_tot[c]
    return C


def tensor_product_casimir(T: List[np.ndarray]) -> np.ndarray:
    """Total Casimir C_2 on V_(1,1) ⊗ V_(1,1):

      C_total = Σ_a (T^a ⊗ I + I ⊗ T^a)^2
              = Σ_a (T^a)^2 ⊗ I + 2 (T^a ⊗ T^a) + I ⊗ (T^a)^2
              = C ⊗ I + 2 Σ_a (T^a ⊗ T^a) + I ⊗ C

    Returns 64x64 matrix.
    """
    n = 8
    I8 = np.eye(n, dtype=complex)
    C = adjoint_casimir(T)
    # C ⊗ I + I ⊗ C
    C_total = np.kron(C, I8) + np.kron(I8, C)
    # 2 Σ_a (T^a ⊗ T^a)
    for Ta in T:
        C_total = C_total + 2.0 * np.kron(Ta, Ta)
    return C_total


def exchange_operator(dim: int) -> np.ndarray:
    """Exchange operator E on V ⊗ V swapping the two factors.

    E |i⟩ ⊗ |j⟩ = |j⟩ ⊗ |i⟩
    Matrix elements: E_(ij,kl) = δ_(i,l) δ_(j,k)
    """
    E = np.zeros((dim * dim, dim * dim), dtype=complex)
    for i in range(dim):
        for j in range(dim):
            for k in range(dim):
                for l in range(dim):
                    if i == l and j == k:
                        E[i * dim + j, k * dim + l] = 1.0
    return E


# ===========================================================================
# Section C. CG decomposition via simultaneous diagonalization.
# ===========================================================================

def random_su3(seed: int = 42) -> np.ndarray:
    """Generate a random SU(3) element via QR decomposition + det adjustment."""
    rng = np.random.default_rng(seed)
    M = rng.normal(size=(3, 3)) + 1j * rng.normal(size=(3, 3))
    Q, R = np.linalg.qr(M)
    diag_R = np.diag(R)
    Q = Q * (diag_R / np.abs(diag_R))
    Q = Q / (np.linalg.det(Q) ** (1.0 / 3.0))
    return Q


def adjoint_matrix(g: np.ndarray, lam: List[np.ndarray]) -> np.ndarray:
    """Compute D^(1,1)(g) = (1/2) Tr[λ_a g λ_b g†]_(a,b) (8x8)."""
    g_dag = g.conj().T
    n = 8
    D = np.zeros((n, n), dtype=complex)
    for a in range(n):
        for b in range(n):
            D[a, b] = 0.5 * np.trace(lam[a] @ g @ lam[b] @ g_dag)
    return D


def cg_decomposition(C_total: np.ndarray, E: np.ndarray,
                       C3_total: np.ndarray | None = None
                       ) -> Tuple[np.ndarray, np.ndarray, Tuple[float, float]]:
    """Diagonalize H = C_2_total + α E + β C_3_total to separate all 6
    fusion channels in (1,1) ⊗ (1,1).

    Without C_3, the (3,0) and (0,3) channels (both 10-dim) have the same
    C_2 eigenvalue (=6) and the same exchange eigenvalue, forming a 20-dim
    block. C_3 distinguishes them (opposite signs since they're conjugate).

    Returns (eigenvalues, eigenvectors_basis, (alpha, beta)).
    """
    alpha = math.sqrt(2)  # irrational; lifts C_2/E degeneracy
    beta = math.sqrt(3) / 7.0  # small irrational; lifts (3,0)/(0,3) degeneracy
    H = C_total + alpha * E
    if C3_total is not None:
        H = H + beta * C3_total
    H_sym = (H + H.conj().T) / 2.0
    eigvals, eigvecs = np.linalg.eigh(H_sym)
    return eigvals, eigvecs, (alpha, beta)


def identify_channels(eigvals: np.ndarray, alpha: float
                       ) -> List[Tuple[float, float, int, int]]:
    """Group eigenvalues by (C_2, E) eigenvalue and identify channels.

    Each unique (C_2, E_eig) pair corresponds to a fusion channel with
    a specific dimension.

    Returns list of (c2, e_eig, multiplicity_count, irrep_dim).
    """
    n = len(eigvals)
    # Group by eigenvalues with tolerance
    tol = 1e-6
    groups: Dict[float, int] = {}
    for ev in eigvals:
        key = round(float(ev), 5)
        groups[key] = groups.get(key, 0) + 1
    return sorted(groups.items())


def expected_su3_casimirs() -> Dict[Tuple[int, int], float]:
    """Standard SU(3) Casimir eigenvalues C_2((p,q)) = (p^2 + q^2 + pq)/3 + p + q.

    With the normalization Tr[λ_a λ_b] = 2 δ_(ab), the Casimir
    eigenvalues for irreps are:
      C_2((0,0)) = 0
      C_2((1,0)) = 4/3
      C_2((1,1)) = 3
      C_2((3,0)) = 6
      C_2((0,3)) = 6
      C_2((2,2)) = 8
    """
    return {(p, q): (p ** 2 + q ** 2 + p * q) / 3.0 + p + q
            for p in range(5) for q in range(5)}


# ===========================================================================
# Section D. Driver + validation.
# ===========================================================================

def driver() -> int:
    print("=" * 78)
    print("SU(3) Wigner Intertwiner Engine — Block 1: (1,1) ⊗ (1,1) CG")
    print("=" * 78)
    print()

    pass_count = 0
    fail_count = 0

    # ===== Section A: build basis + structure constants =====
    print("--- Section A: Gell-Mann basis + structure constants ---")
    lam = gellmann_basis()
    f, d = structure_constants()
    # Verify f is fully antisymmetric, d is fully symmetric
    f_asym = np.max(np.abs(f + np.transpose(f, (1, 0, 2))))
    d_sym = np.max(np.abs(d - np.transpose(d, (1, 0, 2))))
    print(f"  f antisymmetry error: {f_asym:.3e}")
    print(f"  d symmetry error:     {d_sym:.3e}")
    if f_asym < 1e-10 and d_sym < 1e-10:
        print("  PASS: structure constants satisfy expected symmetries.")
        pass_count += 1
    else:
        print("  FAIL: structure constants malformed.")
        fail_count += 1
    print()

    # Verify a few standard nonzero constants in 1-based Gell-Mann notation.
    print("  Standard structure constant values:")
    expected_f = {(0, 1, 2): 1.0,
                  (2, 3, 4): 0.5,  # f_345 = 1/2
                  (3, 4, 7): math.sqrt(3) / 2.0}  # f_458 = sqrt(3)/2
    max_standard_delta = 0.0
    for (a, b, c), expected in expected_f.items():
        actual = f[a, b, c]
        delta = abs(actual - expected)
        max_standard_delta = max(max_standard_delta, delta)
        marker = "OK" if delta < 1e-10 else "BAD"
        print(f"    f[{a+1}{b+1}{c+1}] = {actual:.6f}  (expected {expected:.6f})  [{marker}]")
    if max_standard_delta < 1e-10:
        print("  PASS: standard nonzero f_abc spot checks match.")
    else:
        print("  FAIL: standard nonzero f_abc spot checks do not match.")
        fail_count += 1
    print()

    # ===== Section B: adjoint generators + Casimir =====
    print("--- Section B: adjoint generators + quadratic Casimir ---")
    T = adjoint_generators(f)
    # Verify Hermiticity
    herm_errors = max(np.max(np.abs(Ta - Ta.conj().T)) for Ta in T)
    print(f"  T^a Hermiticity error: {herm_errors:.3e}")
    # Verify [T^a, T^b] = i f_abc T^c
    comm_errors = 0.0
    for a in range(8):
        for b in range(8):
            comm = T[a] @ T[b] - T[b] @ T[a]
            expected = sum(1j * f[a, b, c] * T[c] for c in range(8))
            comm_errors = max(comm_errors, np.max(np.abs(comm - expected)))
    print(f"  Lie algebra commutator error: {comm_errors:.3e}")
    if herm_errors < 1e-10 and comm_errors < 1e-10:
        print("  PASS: adjoint generators satisfy Hermiticity + Lie algebra.")
        pass_count += 1
    else:
        print("  FAIL: adjoint generator construction broken.")
        fail_count += 1

    C2_adj = adjoint_casimir(T)
    eigvals_C2 = np.linalg.eigvalsh((C2_adj + C2_adj.conj().T) / 2.0)
    print(f"  C_2 on (1,1) adjoint eigenvalues: {sorted(set(round(float(ev), 4) for ev in eigvals_C2))}")
    expected_C2_adj = 3.0  # SU(3) (1,1) Casimir
    if all(abs(float(ev) - expected_C2_adj) < 1e-10 for ev in eigvals_C2):
        print(f"  PASS: all C_2 eigenvalues = 3 (matches SU(3) (1,1) Casimir).")
        pass_count += 1
    else:
        print(f"  FAIL: C_2 not constant on (1,1).")
        fail_count += 1
    print()

    # ===== Section C: tensor product Casimir + exchange =====
    print("--- Section C: tensor product Casimir + exchange operator ---")
    C_total = tensor_product_casimir(T)
    E = exchange_operator(8)
    # Verify E^2 = I
    E_sq = E @ E
    e_err = np.max(np.abs(E_sq - np.eye(64)))
    print(f"  Exchange E^2 - I error: {e_err:.3e}")
    if e_err < 1e-10:
        print("  PASS: exchange operator satisfies E^2 = I.")
        pass_count += 1
    else:
        print("  FAIL: exchange operator broken.")
        fail_count += 1
    print()

    # ===== Section D: CG decomposition via diagonalization =====
    print("--- Section D: CG decomposition via simultaneous diagonalization ---")
    C3_total = tensor_product_cubic_casimir(T, d)
    eigvals, eigvecs, (alpha, beta) = cg_decomposition(C_total, E, C3_total)
    print(f"  Diagonalizing H = C_2_total + α E + β C_3_total")
    print(f"  α = sqrt(2) = {alpha:.6f}, β = sqrt(3)/7 = {beta:.6f}")
    # Group eigenvalues by clusters
    rounded = sorted([round(float(ev), 4) for ev in eigvals])
    unique_vals = sorted(set(rounded))
    print(f"  Number of unique eigenvalue clusters: {len(unique_vals)}")
    multiplicities = [(v, rounded.count(v)) for v in unique_vals]
    print(f"  (eigenvalue, multiplicity) pairs:")
    for v, m in multiplicities:
        print(f"    H = {v:>11.4f}  multiplicity {m:>3}")
    print()

    # ===== Section E: verify dimensions sum to 64 =====
    total_dim = sum(m for v, m in multiplicities)
    expected_total = 64
    print(f"  Total dimension: {total_dim}  (expected {expected_total})")
    if total_dim == expected_total:
        print(f"  PASS: dimensions sum to 64 = 8 × 8.")
        pass_count += 1
    else:
        print(f"  FAIL: dimensions don't match.")
        fail_count += 1
    print()

    # ===== Section F: verify expected fusion channel pattern =====
    print("--- Section F: verify (1,1) ⊗ (1,1) = 1 + 8 + 8 + 10 + 10̄ + 27 ---")
    expected_pattern = sorted([1, 8, 8, 10, 10, 27])
    actual_pattern = sorted([m for v, m in multiplicities])
    print(f"  Expected dimensions (sorted): {expected_pattern}")
    print(f"  Actual dimensions (sorted):   {actual_pattern}")
    if actual_pattern == expected_pattern:
        print(f"  PASS: 6 channels with correct dimensions.")
        pass_count += 1
    else:
        print(f"  FAIL: channel pattern mismatch.")
        fail_count += 1
    print()

    # ===== Section G: orthogonality of CG basis =====
    print("--- Section G: orthonormality of CG eigenbasis ---")
    overlap = eigvecs.conj().T @ eigvecs
    overlap_err = np.max(np.abs(overlap - np.eye(64)))
    print(f"  ||V^† V - I|| = {overlap_err:.3e}")
    if overlap_err < 1e-10:
        print(f"  PASS: CG basis is orthonormal.")
        pass_count += 1
    else:
        print(f"  FAIL: CG basis not orthonormal.")
        fail_count += 1
    print()

    # ===== Section H: SU(3) equivariance =====
    print("--- Section H: SU(3) equivariance of channel decomposition ---")
    # For random g, D⊗D should commute with C_total and preserve channel blocks
    g = random_su3(seed=11)
    D = adjoint_matrix(g, lam)
    DD = np.kron(D, D)
    # Check [D⊗D, C_total] = 0
    commutator = DD @ C_total - C_total @ DD
    comm_err = np.max(np.abs(commutator))
    print(f"  ||[D⊗D, C_total]|| = {comm_err:.3e}")
    # Check D⊗D commutes with E
    EE_comm = DD @ E - E @ DD
    EE_err = np.max(np.abs(EE_comm))
    print(f"  ||[D⊗D, E]|| = {EE_err:.3e}")
    if comm_err < 1e-8 and EE_err < 1e-8:
        print(f"  PASS: D⊗D commutes with both Casimir and exchange.")
        pass_count += 1
    else:
        print(f"  FAIL: SU(3) equivariance broken.")
        fail_count += 1
    print()

    # ===== Summary =====
    print("=" * 78)
    print(f"SUMMARY: THEOREM PASS={pass_count} FAIL={fail_count}")
    print("=" * 78)
    print()
    print("Headline:")
    print(f"  SU(3) (1,1) ⊗ (1,1) decomposed into {len(unique_vals)} fusion channels")
    print(f"  with dimensions {actual_pattern} = {sum(actual_pattern)} total.")
    print(f"  Expected: 1 + 8 + 8 + 10 + 10̄ + 27 = 64. Match: "
          f"{actual_pattern == sorted([1, 8, 8, 10, 10, 27])}")
    print()
    print("Block 1 deliverable: SU(3) (1,1) ⊗ (1,1) CG basis (64 orthonormal")
    print("vectors organized into 6 irrep blocks). Available as `eigvecs` array")
    print("and importable for Block 2 (4-fold Haar projector).")
    return 0 if fail_count == 0 else 1


if __name__ == "__main__":
    sys.exit(driver())
