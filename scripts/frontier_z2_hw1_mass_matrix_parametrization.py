#!/usr/bin/env python3
"""
Z_2-Invariant Hw=1 Mass-Matrix Parametrization

Classical math applied:
  - Schur's lemma (Schur 1905), applied to the Z_2 decomposition
    hw=1 ≅ 2·1 ⊕ 1·sgn of the Batch 5 Residual Z_2 Commutant theorem
  - Hermitian matrix spectral theorem (standard linear algebra)
  - 2×2 secular equation (quadratic formula for eigenvalues of a
    Hermitian 2×2 block)
  - Texture analysis of Hermitian mass matrices (Fritzsch 1977; NNI
    form in Gatto–Sartori–Tonin 1968, Ramond–Roberts–Ross 1993)

Framework object:
  The 5-dimensional real space of Z_2-invariant Hermitian operators
  on the hw=1 triplet V_1 = span(X_1, X_2, X_3), where Z_2 = ⟨(12)⟩
  swaps axes 1 and 2 and fixes axis 3.  Established as a 5-dim
  subspace by Batch 5 Residual Z_2 Commutant.  This theorem gives
  the explicit parametrization and spectrum formula.

Theorem (Z_2-invariant hw=1 mass-matrix parametrization):
  (1) In the ordered basis (X_3, X_1, X_2), every Z_2-invariant
      Hermitian operator on V_1 has the form
          M(a, b, c, d)  =  [[ a,     d,     d   ],
                              [ d*,    b,     c   ],
                              [ d*,    c,     b   ]]
      with a, b, c ∈ R and d ∈ C.  The real parameter count is 5,
      matching dim End(V_1)^{Z_2}_{Hermitian} = 2² + 1² = 5 (Batch 5,
      applying Schur's lemma to the Z_2 decomposition hw=1 ≅ 2·1 ⊕ sgn).
  (2) The Z_2-sign-eigenvector (X_1 − X_2)/√2 is always an exact
      eigenvector of M with eigenvalue λ_sgn = b − c.
  (3) On the 2-dim Z_2-trivial subspace spanned by X_3 and
      (X_1 + X_2)/√2, M acts as the 2×2 Hermitian block
          B  =  [[ a,     √2 · d ],
                  [ √2 · d*, b + c ]]
      with eigenvalues given by the secular equation
          λ_±  =  ( (a + b + c) ± √( (a − b − c)² + 8 |d|² ) ) / 2.
  (4) Generic (a, b, c, d) gives three distinct eigenvalues
      {λ_sgn, λ_+, λ_−}.  Degenerate subloci (≥ 2 coincidences) have
      positive codimension in R^5 and hence measure zero.

Proof method:
  (1) Direct solution of M = U M U and M = M† for the 3×3 generator
      U = Z_2-swap of axes 1, 2 (fixing axis 3).
  (2) Direct computation on the sign-eigenvector.
  (3) Hermitian 2×2 secular equation.
  (4) Algebraic analysis of the discriminant.

Applied rather than invented:
  The parametrization is the standard application of Schur's lemma
  to a 3-dim rep with isotypic decomposition 2·1 ⊕ sgn.  The
  eigenvalue formula is the standard 2×2 Hermitian secular equation.
  Neither is novel in isolation — but their combination gives the
  explicit 5-parameter family of Hermitian operators on hw=1 that
  survive the Batch 4 S_3 Mass-Matrix No-Go after S_3 → Z_2 SSB.

Reusability:
  - Explicit parametrization for any framework construction that
    needs a Z_2-invariant mass matrix on hw=1 with prescribed
    spectrum.
  - Companion to Batch 4 S_3 Mass-Matrix No-Go (no-go says SSB is
    necessary) and Batch 5 Residual Z_2 Commutant (dim 2 → 5 relief);
    this theorem exhibits the relief in closed form.
"""

from __future__ import annotations

import numpy as np

PASS_COUNT = 0
FAIL_COUNT = 0


def check(name: str, condition: bool, detail: str = "") -> None:
    global PASS_COUNT, FAIL_COUNT
    if condition:
        PASS_COUNT += 1
        status = "PASS"
    else:
        FAIL_COUNT += 1
        status = "FAIL"
    line = f"  [{status}] {name}"
    if detail:
        line += f"  ({detail})"
    print(line)


# ---------------------------------------------------------------------------
# Z_2 generator on hw=1 in basis (X_3, X_1, X_2): swap indices 1, 2
# ---------------------------------------------------------------------------

U_Z2 = np.array([
    [1.0, 0.0, 0.0],
    [0.0, 0.0, 1.0],
    [0.0, 1.0, 0.0],
], dtype=complex)


def build_M(a: float, b: float, c: float, d: complex) -> np.ndarray:
    """Canonical Z_2-invariant Hermitian 3x3 in basis (X_3, X_1, X_2)."""
    return np.array([
        [a,            d,          d         ],
        [np.conj(d),   b,          c         ],
        [np.conj(d),   c,          b         ],
    ], dtype=complex)


# ---------------------------------------------------------------------------
# Part 1: 5-parameter family spans the full Z_2-invariant Hermitian space
# ---------------------------------------------------------------------------

def part1_parametrization() -> None:
    print("\n" + "=" * 72)
    print("PART 1: 5-parameter family M(a, b, c, d) is complete")
    print("        (applies Schur's lemma to hw=1 ≅ 2·1 ⊕ sgn)")
    print("=" * 72)

    # Construct 10 random parameter tuples, check each M is Z_2-invariant
    # and Hermitian.
    rng = np.random.default_rng(0)
    for _ in range(10):
        a, b, c = rng.normal(size=3)
        d = rng.normal() + 1j * rng.normal()
        M = build_M(a, b, c, d)
        if not np.allclose(M, M.conj().T):
            check("M is Hermitian (random sample)", False); return
        if not np.allclose(U_Z2 @ M @ U_Z2, M):
            check("M is Z_2-invariant (random sample)", False); return
    check("All 10 random M(a,b,c,d) are Hermitian and Z_2-invariant", True)

    # Real-dimension count: span of the 5 basis matrices
    basis = []
    for (a, b, c, dr, di) in [
        (1, 0, 0, 0, 0),
        (0, 1, 0, 0, 0),
        (0, 0, 1, 0, 0),
        (0, 0, 0, 1, 0),
        (0, 0, 0, 0, 1),
    ]:
        d = dr + 1j * di
        basis.append(build_M(a, b, c, d))

    # Real rank: stack real and imaginary parts of 3x3 flattened
    mats = np.stack([M.reshape(9) for M in basis], axis=1)
    stacked = np.vstack([mats.real, mats.imag])
    real_rank = np.linalg.matrix_rank(stacked, tol=1e-10)
    print(f"  Real rank of 5-param basis = {real_rank}")
    check("5-parameter family has real dim 5",
          real_rank == 5)

    # Exhaustive comparison: build the full Z_2-invariant Hermitian subspace
    # by the Schur decomposition and check dim agrees.
    # Basis of 3x3 Hermitian: 3 diagonal (real) + 3 upper off-diag (complex)
    # = 3 + 3·2 = 9 real dim.  Z_2-invariance projects onto a 5-real-dim
    # subspace.
    herm_real_basis = []
    # diagonal entries
    for i in range(3):
        E = np.zeros((3, 3), dtype=complex); E[i, i] = 1.0
        herm_real_basis.append(E)
    # off-diagonal real parts
    for i in range(3):
        for j in range(i + 1, 3):
            E = np.zeros((3, 3), dtype=complex)
            E[i, j] = 1.0
            E[j, i] = 1.0
            herm_real_basis.append(E)
    # off-diagonal imaginary parts
    for i in range(3):
        for j in range(i + 1, 3):
            E = np.zeros((3, 3), dtype=complex)
            E[i, j] = 1j
            E[j, i] = -1j
            herm_real_basis.append(E)
    # Now project each onto Z_2-invariant: M ↦ (M + U M U) / 2
    projected = []
    for E in herm_real_basis:
        proj = 0.5 * (E + U_Z2 @ E @ U_Z2)
        projected.append(proj)
    mats = np.stack([M.reshape(9) for M in projected], axis=1)
    stacked = np.vstack([mats.real, mats.imag])
    proj_rank = np.linalg.matrix_rank(stacked, tol=1e-10)
    print(f"  Projected 9-dim Hermitian basis onto Z_2-inv: rank = {proj_rank}")
    check("Full Z_2-invariant Hermitian subspace has real dim 5",
          proj_rank == 5)


# ---------------------------------------------------------------------------
# Part 2: Sign-eigenvector has eigenvalue b - c
# ---------------------------------------------------------------------------

def part2_sign_eigenvector() -> None:
    print("\n" + "=" * 72)
    print("PART 2: (X_1 − X_2)/√2 is an eigenvector with eigenvalue b − c")
    print("=" * 72)

    # In basis (X_3, X_1, X_2), sign vector = (0, 1, -1)/√2
    v_sgn = np.array([0, 1, -1], dtype=complex) / np.sqrt(2)

    # Verify it's a Z_2 sign eigenvector
    check("(X_1 − X_2)/√2 is Z_2 sign eigenvector",
          np.allclose(U_Z2 @ v_sgn, -v_sgn))

    rng = np.random.default_rng(7)
    for _ in range(5):
        a, b, c = rng.normal(size=3)
        d = rng.normal() + 1j * rng.normal()
        M = build_M(a, b, c, d)
        Mv = M @ v_sgn
        lam = b - c
        expected = lam * v_sgn
        if not np.allclose(Mv, expected, atol=1e-12):
            check("M · v_sgn = (b − c) · v_sgn (random sample)", False)
            return
    check("M · v_sgn = (b − c) · v_sgn  for all 5 random samples", True)


# ---------------------------------------------------------------------------
# Part 3: 2×2 trivial block and secular eigenvalue formula
# ---------------------------------------------------------------------------

def part3_trivial_block() -> None:
    print("\n" + "=" * 72)
    print("PART 3: 2×2 trivial-subspace block and secular equation")
    print("=" * 72)

    # Trivial subspace spanned by X_3 and (X_1 + X_2)/√2:
    # e_0 = (1, 0, 0), e_1 = (0, 1, 1)/√2
    # In this basis, M acts as the 2x2 block B.
    # Direct computation: B = [[a, √2·d], [√2·d*, b + c]]

    rng = np.random.default_rng(13)
    for _ in range(10):
        a, b, c = rng.normal(size=3)
        d = rng.normal() + 1j * rng.normal()
        M = build_M(a, b, c, d)

        e0 = np.array([1, 0, 0], dtype=complex)
        e1 = np.array([0, 1, 1], dtype=complex) / np.sqrt(2)

        # Build B_{ij} = ⟨e_i, M e_j⟩
        B = np.array([
            [e0.conj() @ M @ e0, e0.conj() @ M @ e1],
            [e1.conj() @ M @ e0, e1.conj() @ M @ e1],
        ])

        expected_B = np.array([
            [a,                   np.sqrt(2) * d],
            [np.sqrt(2) * np.conj(d), b + c       ],
        ], dtype=complex)

        if not np.allclose(B, expected_B, atol=1e-12):
            check("Trivial-block form B matches prediction", False)
            return

    check("Trivial-subspace 2x2 block B = [[a, √2 d], [√2 d*, b+c]]  (10 samples)", True)

    # Eigenvalue formula: λ_± = ((a + b + c) ± √((a − b − c)² + 8 |d|²)) / 2
    rng = np.random.default_rng(21)
    for _ in range(10):
        a, b, c = rng.normal(size=3)
        d = rng.normal() + 1j * rng.normal()
        M = build_M(a, b, c, d)
        eigs = np.sort(np.real(np.linalg.eigvalsh(M)))

        lam_sgn = b - c
        disc = (a - b - c) ** 2 + 8 * abs(d) ** 2
        lam_plus = ((a + b + c) + np.sqrt(disc)) / 2.0
        lam_minus = ((a + b + c) - np.sqrt(disc)) / 2.0

        predicted = np.sort([lam_sgn, lam_plus, lam_minus])
        if not np.allclose(eigs, predicted, atol=1e-10):
            check("Spectrum matches {b-c, λ_+, λ_−} formula", False,
                  f"observed={eigs}, predicted={predicted}")
            return
    check("Spectrum matches {b-c, λ_+, λ_−} formula  (10 samples)", True)


# ---------------------------------------------------------------------------
# Part 4: Generic 3-distinct-eigenvalue locus
# ---------------------------------------------------------------------------

def part4_generic_distinct() -> None:
    print("\n" + "=" * 72)
    print("PART 4: Generic 5-parameter family has 3 distinct eigenvalues")
    print("=" * 72)

    rng = np.random.default_rng(99)
    N = 500
    n_distinct_counts = {1: 0, 2: 0, 3: 0}
    for _ in range(N):
        a, b, c = rng.normal(size=3)
        d = rng.normal() + 1j * rng.normal()
        M = build_M(a, b, c, d)
        eigs = np.sort(np.real(np.linalg.eigvalsh(M)))
        # Count distinct up to floating-point tolerance
        unique = 1
        for i in range(1, 3):
            if abs(eigs[i] - eigs[i - 1]) > 1e-6:
                unique += 1
        n_distinct_counts[unique] += 1

    print(f"  Out of {N} random samples:")
    for n in (1, 2, 3):
        print(f"    {n} distinct eigenvalues: {n_distinct_counts[n]}")

    check("Generic 3-distinct-eigenvalue locus contains > 99% of samples",
          n_distinct_counts[3] > 0.99 * N,
          f"{n_distinct_counts[3]} / {N}")
    check("Degenerate loci have measure ≤ 1% in random sampling",
          (n_distinct_counts[1] + n_distinct_counts[2]) < 0.01 * N)

    # Demonstrate 2 distinct eigenvalues on the codim-1 locus b = c
    # (spectrum degenerates to {0, λ_+, λ_−} with one accidental coincidence
    #  only when additionally a = ... — hard to pin without careful algebra).
    # Simpler: S_3-invariant case d = 0, a = b+c, then λ_sgn = b-c, λ_± = ?
    #   With a = b+c: (a − b − c) = 0, disc = 8|d|² = 0, so λ_± = (a+b+c)/2.
    #   Check: b - c vs (a+b+c)/2 = (2b+2c)/2 = b+c.
    #   These differ (unless b-c = b+c, i.e. c = 0, which is codim 2).
    # Demonstrate: choose d = 0, a = b+c, generic b, c; spectrum has 2
    # distinct eigenvalues (S_3-invariant limit).
    a, b, c, d = 1.5 + 0.7, 1.5, 0.7, 0 + 0j
    M = build_M(a, b, c, d)
    eigs = np.sort(np.real(np.linalg.eigvalsh(M)))
    unique = 1
    for i in range(1, 3):
        if abs(eigs[i] - eigs[i - 1]) > 1e-6:
            unique += 1
    print(f"\n  S_3-invariant limit (d=0, a=b+c, b=1.5, c=0.7):")
    print(f"    eigenvalues = {eigs}")
    print(f"    distinct count = {unique}")
    check("S_3-invariant limit (d=0, a=b+c) has exactly 2 distinct eigenvalues "
          "(consistent with Batch 4 no-go)",
          unique == 2)


# ---------------------------------------------------------------------------
# Part 5: Theorem statement
# ---------------------------------------------------------------------------

def part5_theorem() -> None:
    print("\n" + "=" * 72)
    print("PART 5: Z_2-Invariant Hw=1 Mass-Matrix Parametrization (statement)")
    print("=" * 72)

    print("""
  THEOREM (Z_2-invariant hw=1 mass-matrix parametrization).  Let
  Z_2 = ⟨(12)⟩ be the residual subgroup of S_3 fixing axis 3 and
  swapping axes 1 and 2.  On the hw=1 triplet V_1 ≅ 2·1 ⊕ sgn,

  (1) in the ordered basis (X_3, X_1, X_2), every Z_2-invariant
      Hermitian operator on V_1 has the form

         M(a, b, c, d)  =  [[ a,      d,      d   ],
                             [ d*,     b,      c   ],
                             [ d*,     c,      b   ]]

      with a, b, c ∈ R and d ∈ C.  Real parameter count: 5, matching
      dim End(V_1)^{Z_2}_{Hermitian} = 2² + 1² = 5 (Batch 5).

  (2) the Z_2-sign eigenvector (X_1 − X_2)/√2 is an exact eigenvector
      of M with eigenvalue  λ_sgn = b − c.

  (3) on the 2-dim Z_2-trivial subspace spanned by X_3 and
      (X_1 + X_2)/√2, M acts as the 2×2 Hermitian block

         B  =  [[ a,        √2 · d  ],
                 [ √2 · d*,  b + c   ]]

      with eigenvalues

         λ_±  =  ( (a + b + c)  ±  √( (a − b − c)² + 8 |d|² ) ) / 2.

  (4) generic (a, b, c, d) gives three distinct eigenvalues
      {λ_sgn, λ_+, λ_−}.  Degenerate loci are algebraic subvarieties
      of positive codimension in R^5 and hence of Lebesgue measure 0.

  CLASSICAL RESULTS USED.
  - Schur's lemma applied to the Z_2 decomposition V_1 ≅ 2·1 ⊕ sgn.
  - Hermitian matrix spectral theorem.
  - 2×2 secular equation (quadratic formula).
  - Hermitian mass-matrix texture language from the flavor-physics
    literature (Fritzsch 1977; NNI, GST, Ramond–Roberts–Ross).

  FRAMEWORK-SPECIFIC STEP.
  - Identification of V_1 with the hw=1 triplet of the taste cube
    and Z_2 with the residual V_sel subgroup.

  PROOF.  (1) is the fixed-point equation U M U = M on the Hermitian
  3×3 matrices.  (2) is a direct check.  (3) follows by changing basis
  to (X_3, (X_1 + X_2)/√2) on the Z_2-trivial subspace and applying
  the secular equation.  (4) is an algebraic analysis of the
  discriminant.  Each step is verified numerically.  QED.

  REUSABILITY.  Companion to the Batch 4 S_3 Mass-Matrix No-Go (SSB
  is necessary) and the Batch 5 Residual Z_2 Commutant (dim 2 → 5
  relief).  This theorem exhibits the 5-dim relief in closed form,
  with a separated sign-block eigenvalue (b − c) and a 2×2 trivial
  block whose secular equation gives the other two eigenvalues.
  Used whenever a framework claim requires a Z_2-invariant Hermitian
  mass matrix on hw=1 with prescribed spectrum.
""")


def main() -> int:
    print("=" * 72)
    print("  Z_2-Invariant Hw=1 Mass-Matrix Parametrization")
    print("=" * 72)

    part1_parametrization()
    part2_sign_eigenvector()
    part3_trivial_block()
    part4_generic_distinct()
    part5_theorem()

    print("\n" + "=" * 72)
    print(f"  TOTAL: PASS={PASS_COUNT}, FAIL={FAIL_COUNT}")
    print("=" * 72)

    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
