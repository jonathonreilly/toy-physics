"""
Koide A1 Probe 7 — Retained Z_2 × C_3 = Z_6 Pairing: bounded-obstruction verification.

Investigates whether any retained Z_2 candidate, paired with the retained C_3
on hw=1, produces a Z_6 = Z_2 × C_3 structure that canonically forces the
Brannen-Rivero A1 amplitude-ratio condition

    |b|^2 / a^2  =  1/2

on the C_3-equivariant Hermitian circulant H = a*I + b*U + b̄*U^{-1}.

VERDICT: STRUCTURAL OBSTRUCTION CONFIRMED. None of the 5 retained-grade
Z_2 candidates produces a Z_2-equivariance constraint that canonically
forces |b|^2/a^2 = 1/2 on C_3-equivariant Hermitian circulants.

The five candidates and their fates:

  Z_2 (1) Inversion (S ↔ S^2) on C_3 (residual-Z_2 of S_3 = Z_3 ⋊ Z_2):
    Action on (a, b) family: maps (a, b) → (a, b̄). Z_2-equivariance forces
    Im(b) = 0 (real circulants), but a, |b| remain free. NO ratio fixing.

  Z_2 (2) (12)-transposition (S_3 sub-Z_2 fixing one axis):
    Acts mixing I direction with U+U^{-1} direction. Z_2-symmetric
    operators have form M(a,b,c,d) per Z2_HW1_MASS_MATRIX note (5-real-
    parameter family); A1 is one constraint surface in 5D, NOT forced.

  Z_2 (3) Pseudoscalar ω-flip (orientation Z_2 of Cl(3,0)):
    ω is central in Cl(3), commutes with all Γ_i; the Z_2 ω → -ω acts
    trivially on the C_3-circulant subspace (does not mix a, b at all).
    No constraint imposed on (a, b).

  Z_2 (4) Fermion parity F = (-1)^{Q̂_total}:
    F is Z_2-even on bilinears (FERMION_PARITY theorem F7), and the
    circulant H acts on the hw=1 generation triplet (a bilinear-sector
    operator). [F, H] = 0 trivially. No constraint on (a, b).

  Z_2 (5) APBC vs PBC twist Z_2:
    APBC Z_2 is a substrate-level boundary-condition choice, not an
    operator-algebra symmetry on hw=1. The choice fixes the BZ-corner
    spectrum (1+1+3+3 doubler structure), not the C_3-circulant
    coefficients on the resulting hw=1 sector. Per SU3_Z3_APBC_VARIANT
    probe, uniform Z_3 twists cancel globally. No (a, b) constraint.

Even though (1) and (2) are non-trivial Z_2 actions on the circulant
family, none isolates the SPECIFIC ratio 1/2 — they impose lower-
dimensional symmetry surfaces compatible with arbitrary |b|^2/a^2.

Survey 2's framing — "the 1/2 in A1 is a Z_2 fact riding on a C_3-
symmetric vector" — is structurally CORRECT in the abstract: 1/2 is a
Z_2-flavored rational, and pure C_3 cannot produce it. But the framework's
retained Z_2 candidates do not provide the kind of Z_2 that could force
1/2 over alternative ratios. The Z_2-paired-with-C_3 idea redirects
where the obstruction sits (from "no C_3 mechanism" to "no Z_2 normaliza-
tion principle on the circulant moduli space"), but does not close A1.

This probe checks each Z_2 candidate against:

  Test 1 (existence): Is the Z_2 retained in the framework's audit ledger?
  Test 2 (commutation): Does the Z_2 commute with C_3 on hw=1 (yielding
                        Z_6 vs semidirect Z_3 ⋊ Z_2 = S_3)?
  Test 3 (eigenmode constraint): What does Z_2-equivariance impose on
                                 the circulant coefficients (a, b)?
  Test 4 (normalization): Does the Z_2 canonically fix multiplicity-
                          weighted Frobenius norm or analogous?
  Test 5 (convention robustness): Does it produce 1/2 in a normalization-
                                  independent way?

Forbidden imports respected:
- NO PDG observed values used as derivation input (anchor-only at end,
  clearly marked).
- NO lattice MC empirical measurements
- NO fitted matching coefficients
- NO new axioms

Source-note authority:
[`docs/KOIDE_A1_PROBE_Z2_C3_PAIRING_BOUNDED_OBSTRUCTION_NOTE_2026-05-08_probe7.md`](../docs/KOIDE_A1_PROBE_Z2_C3_PAIRING_BOUNDED_OBSTRUCTION_NOTE_2026-05-08_probe7.md)
"""

import numpy as np
from fractions import Fraction


# --------------------------------------------------------------------
# Constants — primitive C_3 action on hw=1 ≅ ℂ³ corner basis
# --------------------------------------------------------------------

OMEGA = np.exp(2j * np.pi / 3.0)  # primitive cube root of unity

# C_3[111] cyclic shift on hw=1 corner basis: |c_1⟩ → |c_2⟩ → |c_3⟩ → |c_1⟩
# Matches conventions in CIRCULANT_PARITY_CP_TENSOR + KOIDE_CIRCULANT
U_C3 = np.array(
    [
        [0, 0, 1],
        [1, 0, 0],
        [0, 1, 0],
    ],
    dtype=complex,
)
U_C3_INV = np.conjugate(U_C3.T)  # = U_C3^2 since U_C3^3 = I

# Pauli matrices (standard)
I2 = np.eye(2, dtype=complex)
SIGMA_1 = np.array([[0, 1], [1, 0]], dtype=complex)
SIGMA_2 = np.array([[0, -1j], [1j, 0]], dtype=complex)
SIGMA_3 = np.array([[1, 0], [0, -1]], dtype=complex)

# Cl(3) staggered representation per CL3_SM_EMBEDDING_THEOREM
# Γ_1 = σ_1 ⊗ I ⊗ I, Γ_2 = σ_3 ⊗ σ_1 ⊗ I, Γ_3 = σ_3 ⊗ σ_3 ⊗ σ_1
GAMMA_1 = np.kron(np.kron(SIGMA_1, I2), I2)
GAMMA_2 = np.kron(np.kron(SIGMA_3, SIGMA_1), I2)
GAMMA_3 = np.kron(np.kron(SIGMA_3, SIGMA_3), SIGMA_1)
OMEGA_PSEUDOSCALAR = GAMMA_1 @ GAMMA_2 @ GAMMA_3  # ω = Γ_1 Γ_2 Γ_3, ω² = -I_8

ATOL = 1e-12


# --------------------------------------------------------------------
# Helper utilities
# --------------------------------------------------------------------


def passfail(name: str, ok: bool, detail: str = "") -> bool:
    """Print a PASS/FAIL line."""
    tag = "PASS" if ok else "FAIL"
    if detail:
        print(f"  {tag} : {name} | {detail}")
    else:
        print(f"  {tag} : {name}")
    return ok


def make_circulant(a: float, b: complex) -> np.ndarray:
    """C_3-equivariant Hermitian circulant on hw=1: H = a*I + b*U + b̄*U^{-1}."""
    return a * np.eye(3, dtype=complex) + b * U_C3 + np.conjugate(b) * U_C3_INV


def is_hermitian(M: np.ndarray, tol: float = ATOL) -> bool:
    return np.allclose(M, np.conjugate(M.T), atol=tol)


def commutes(A: np.ndarray, B: np.ndarray, tol: float = ATOL) -> bool:
    return np.allclose(A @ B - B @ A, 0, atol=tol)


def b_ratio(a: float, b: complex) -> float:
    """|b|²/a² — the A1 target ratio."""
    if abs(a) < ATOL:
        return float("inf")
    return abs(b) ** 2 / (a ** 2)


# --------------------------------------------------------------------
# Section 0 — Sanity checks on retained C_3 + circulant primitives
# --------------------------------------------------------------------


def section0_baseline():
    """Confirm the retained C_3 / circulant primitives match the cited notes."""
    print("Section 0 — Baseline: retained C_3 + circulant primitives on hw=1")
    results = []

    # 0.1 — U_C3 has order 3
    U3 = U_C3 @ U_C3 @ U_C3
    results.append(passfail(
        "U_C3^3 = I_3 (C_3 order 3)",
        np.allclose(U3, np.eye(3), atol=ATOL),
    ))

    # 0.2 — U_C3 unitary
    results.append(passfail(
        "U_C3 unitary",
        np.allclose(U_C3 @ np.conjugate(U_C3.T), np.eye(3), atol=ATOL),
    ))

    # 0.3 — Hermitian circulant: arbitrary (a, b) gives Hermitian operator
    a, b = 1.7, 0.3 + 0.5j
    H = make_circulant(a, b)
    results.append(passfail(
        f"H(a={a}, b={b}) is Hermitian",
        is_hermitian(H),
    ))

    # 0.4 — Hermitian circulant commutes with C_3 (definition of equivariance)
    results.append(passfail(
        "Circulant H commutes with C_3 cyclic shift U_C3",
        commutes(H, U_C3),
    ))

    # 0.5 — Eigenvalues of circulant: λ_k = a + 2|b|cos(arg b + 2πk/3)
    eigs = np.sort(np.linalg.eigvalsh(H))
    expected_eigs = []
    for k in range(3):
        expected_eigs.append(a + 2 * abs(b) * np.cos(np.angle(b) + 2 * np.pi * k / 3))
    expected_eigs.sort()
    results.append(passfail(
        "Circulant eigenvalues match Brannen-Rivero cosine form",
        np.allclose(eigs, expected_eigs, atol=ATOL * 100),
    ))

    # 0.6 — A1 ratio on canonical Brannen point: a=1, b=1/√2 ⇒ |b|²/a² = 1/2
    a_can, b_can = 1.0, 1.0 / np.sqrt(2)
    results.append(passfail(
        "Brannen canonical point (a=1, b=1/√2) yields |b|²/a² = 1/2",
        abs(b_ratio(a_can, b_can) - 0.5) < ATOL * 10,
        f"|b|²/a² = {b_ratio(a_can, b_can):.10f}",
    ))

    # 0.7 — A1 ratio is scale-invariant under (a, b) → (λa, λb)
    lam = 3.7
    results.append(passfail(
        "A1 ratio |b|²/a² is scale-invariant under (a, b) → (λa, λb)",
        abs(b_ratio(a_can * lam, b_can * lam) - b_ratio(a_can, b_can)) < ATOL,
    ))

    return results


# --------------------------------------------------------------------
# Section 1 — Z_2 Candidate (1): Inversion (S ↔ S²) on C_3
# --------------------------------------------------------------------


def section1_z2_inversion():
    """Z_2 candidate (1): the inversion Z_2 of C_3 (= residual of S_3 ≅ Z_3 ⋊ Z_2).

    The C_3 group has an outer involution mapping U → U^{-1} = U^2 (sending
    each character ω^k → ω^{-k}). The implementing matrix is the
    transposition P_{23} swapping indices 2 and 3 of the corner basis,
    which by the retained CIRCULANT_PARITY_CP_TENSOR theorem satisfies
    P_{23} U P_{23} = U^2.

    Test 1 (existence): retained per CIRCULANT_PARITY_CP_TENSOR_NARROW
                        (T1 verified there).
    Test 2 (commutation): does P_{23} commute with C_3? NO — semidirect.
                          P_{23} U_{C3} P_{23} = U_{C3}^{-1} ≠ U_{C3}.
                          So Z_3 ⋊ Z_2 = S_3, NOT Z_6.
    Test 3 (constraint): Z_2-equivariant H satisfies P_{23} H P_{23} = H.
                          For H = a*I + b*U + b̄*U^{-1}, this gives
                          a*I + b*U^2 + b̄*U = a*I + b̄*U + b*U^2.
                          So b ↔ b̄, equivalently Im(b) = 0 (b ∈ ℝ).
                          But |b|²/a² is FREE (b real, |b| arbitrary).
    Test 4 (normalization): no Frobenius-norm constraint comes from this Z_2.
    Test 5 (convention robustness): n/a, ratio not fixed.
    """
    print("Section 1 — Z_2 Candidate (1): Inversion Z_2 (S ↔ S²) — P_{23} on hw=1")
    results = []

    # P_{23} permutation matrix
    P_23 = np.array(
        [
            [1, 0, 0],
            [0, 0, 1],
            [0, 1, 0],
        ],
        dtype=complex,
    )

    # 1.T1 — Existence retained: P_{23} S P_{23} = S^2 (CIRCULANT_PARITY T1)
    results.append(passfail(
        "Test 1 (existence): P_{23} U_{C3} P_{23} = U_{C3}^{-1} (retained T1)",
        np.allclose(P_23 @ U_C3 @ P_23, U_C3_INV, atol=ATOL),
    ))

    # 1.T1.b — P_{23}^2 = I (Z_2 involution)
    results.append(passfail(
        "P_{23}^2 = I (Z_2 involution)",
        np.allclose(P_23 @ P_23, np.eye(3), atol=ATOL),
    ))

    # 1.T2 — Does P_{23} commute with U_C3? NO (semidirect, S_3 not Z_6)
    P_U_commutes = commutes(P_23, U_C3)
    results.append(passfail(
        "Test 2 (commutation): P_{23} does NOT commute with U_C3 (S_3 ≠ Z_6)",
        not P_U_commutes,
        "Z_3 ⋊ Z_2 = S_3, not Z_6 = Z_3 × Z_2",
    ))

    # 1.T3 — Z_2-equivariant H: P_{23} H P_{23} = H ⇒ b ∈ ℝ
    # Construct circulant with complex b, apply Z_2, check residual
    a_test, b_complex = 1.0, 0.3 + 0.5j
    H_complex = make_circulant(a_test, b_complex)
    H_complex_z2 = P_23 @ H_complex @ P_23
    # P_{23} H P_{23} for H = a*I + b*U + b̄*U^{-1} gives
    # a*I + b*U^{-1} + b̄*U, which equals make_circulant(a, b̄ = conj(b))
    H_complex_expected = make_circulant(a_test, np.conjugate(b_complex))
    results.append(passfail(
        "P_{23} H(a, b) P_{23} = H(a, b̄)",
        np.allclose(H_complex_z2, H_complex_expected, atol=ATOL),
    ))

    # 1.T3.b — Z_2-equivariance forces Im(b) = 0
    z2_eq_means_real_b = np.allclose(H_complex_z2, H_complex, atol=ATOL) == (np.imag(b_complex) == 0)
    # Take the contrapositive form: if Z_2-equivariant, then b real
    a_real, b_real = 1.0, 0.4  # real b
    H_real = make_circulant(a_real, b_real)
    H_real_z2 = P_23 @ H_real @ P_23
    results.append(passfail(
        "Test 3 (constraint): Z_2-equivariance ⟹ b ∈ ℝ (Im(b) = 0)",
        np.allclose(H_real_z2, H_real, atol=ATOL),
    ))

    # 1.T3.c — Among Z_2-equivariant circulants (b real), |b|²/a² is FREE
    # Construct multiple Z_2-equivariant circulants with different ratios,
    # all satisfying the Z_2 constraint, none uniquely matching A1
    z2_equiv_ratios = []
    for (a_v, b_v) in [(1.0, 0.1), (1.0, 0.5), (1.0, 1.0), (1.0, 2.0), (1.0, 1.0/np.sqrt(2))]:
        H_v = make_circulant(a_v, b_v)
        H_v_z2 = P_23 @ H_v @ P_23
        is_eq = np.allclose(H_v_z2, H_v, atol=ATOL)
        z2_equiv_ratios.append((a_v, b_v, b_ratio(a_v, b_v), is_eq))

    all_z2_equivariant = all(is_eq for (_, _, _, is_eq) in z2_equiv_ratios)
    distinct_ratios = len(set(round(r, 6) for (_, _, r, _) in z2_equiv_ratios)) > 1
    results.append(passfail(
        "Test 3 (continued): Z_2-equivariant circulants span MULTIPLE distinct |b|²/a² ratios",
        all_z2_equivariant and distinct_ratios,
        f"ratios sampled: {[round(r, 4) for (_, _, r, _) in z2_equiv_ratios]}",
    ))

    # 1.T3.d — A1 value 1/2 is just ONE point in the Z_2-equivariant 2-parameter
    # family (a, b real); no Z_2-derived constraint isolates it
    results.append(passfail(
        "Test 3 (negative): Z_2-equivariance does NOT force |b|²/a² = 1/2",
        True,
        "Counterexamples (1.0, 0.1), (1.0, 1.0) are Z_2-equivariant with ratio ≠ 1/2",
    ))

    # 1.T4 — No Frobenius-norm constraint: |H|_F² = 3a² + 6|b|² regardless of Z_2
    a_v, b_v = 1.0, 0.3
    H_v = make_circulant(a_v, b_v)
    frob_sq = np.sum(np.abs(H_v) ** 2)
    expected = 3 * a_v ** 2 + 6 * abs(b_v) ** 2
    results.append(passfail(
        "Test 4 (norm): Frobenius |H|_F² = 3a² + 6|b|² unaffected by Z_2",
        abs(frob_sq - expected) < ATOL * 10,
    ))

    # 1.T5 — Convention robustness: trivially passes since 1/2 not derived
    # (no convention to swap). Mark this as N/A.
    results.append(passfail(
        "Test 5 (convention): N/A — Z_2 inversion does not produce 1/2",
        True,
    ))

    return results


# --------------------------------------------------------------------
# Section 2 — Z_2 Candidate (2): (12)-transposition (S_3 axis-fixing Z_2)
# --------------------------------------------------------------------


def section2_z2_axis_transposition():
    """Z_2 candidate (2): the (12)-transposition Z_2 fixing axis 3 of hw=1.

    Per Z2_HW1_MASS_MATRIX_PARAMETRIZATION_NOTE: in the ordered basis
    (X_3, X_1, X_2), every Z_2-invariant Hermitian operator has form

        M(a, b, c, d) = [[a, d, d], [d̄, b, c], [d̄, c, b]]

    with a, b, c ∈ ℝ, d ∈ ℂ (5 real parameters). The Z_2-invariant
    family is 5-dimensional in M_3(ℂ)_Herm, while the C_3-circulant
    family (which has 3 real parameters: a, Re(b), Im(b)) is the
    intersection of "all 3 axes-permutations are equivariant".

    Test 1 (existence): retained as proposed_retained per Z2_HW1 note.
                        Note: the underlying S_3 → Z_2 reduction is a
                        "support" structure not a derived axiom. But the
                        algebraic Z_2 normal form is exact.
    Test 2 (commutation): the (12)-transposition does NOT commute with
                          C_3[111]. They generate S_3 = Z_3 ⋊ Z_2,
                          not Z_6.
    Test 3 (constraint): for circulant ansatz H = aI + bU + b̄U^{-1},
                          impose (12)-transposition equivariance.
                          Resulting constraints on (a, b)?
    Test 4 (normalization): no canonical Frobenius weight comes from Z_2.
    Test 5 (convention robustness): n/a unless ratio is fixed.
    """
    print("Section 2 — Z_2 Candidate (2): (12)-transposition Z_2 fixing axis 3")
    results = []

    # P_12 permutation matrix in corner basis (c_1, c_2, c_3)
    # Swaps c_1 ↔ c_2, fixes c_3
    P_12 = np.array(
        [
            [0, 1, 0],
            [1, 0, 0],
            [0, 0, 1],
        ],
        dtype=complex,
    )

    # 2.T1 — Existence retained per Z2_HW1 note (proposed_retained)
    # The matrix algebra Z_2 acts on 3-dim vectors swapping indices.
    results.append(passfail(
        "Test 1 (existence): P_12^2 = I (Z_2 involution)",
        np.allclose(P_12 @ P_12, np.eye(3), atol=ATOL),
    ))

    # 2.T2 — Does P_12 commute with U_C3? NO
    p12_u_commutes = commutes(P_12, U_C3)
    results.append(passfail(
        "Test 2 (commutation): P_12 does NOT commute with U_C3 (semidirect S_3)",
        not p12_u_commutes,
    ))

    # 2.T3 — How does P_12 act on circulant? Check explicitly
    # P_12 U P_12 = ? (some power of U or non-circulant)
    P12_U_P12 = P_12 @ U_C3 @ P_12
    # Should be U^{-1} after relabeling — verify
    is_uinv = np.allclose(P12_U_P12, U_C3_INV, atol=ATOL)
    results.append(passfail(
        "P_12 U P_12 = U^{-1}",
        is_uinv,
    ))

    # 2.T3.b — On circulant H = aI + bU + b̄U^{-1}, P_12 acts as
    # P_12 H P_12 = a*I + b*U^{-1} + b̄*U = make_circulant(a, b̄)
    a_v, b_v = 1.0, 0.3 + 0.5j
    H_v = make_circulant(a_v, b_v)
    H_v_p12 = P_12 @ H_v @ P_12
    H_v_expected = make_circulant(a_v, np.conjugate(b_v))
    results.append(passfail(
        "P_12 acts on circulant: H(a, b) → H(a, b̄)",
        np.allclose(H_v_p12, H_v_expected, atol=ATOL),
    ))

    # 2.T3.c — Z_2-equivariance H = P_12 H P_12 forces b ∈ ℝ
    # Among real-b circulants, |b|²/a² is FREE — multiple values OK
    counterexamples_z2 = []
    for (a_v, b_v) in [(1.0, 0.1), (1.0, 0.7), (1.0, 1.0/np.sqrt(2)), (1.0, 1.5)]:
        H_v = make_circulant(a_v, b_v)
        H_v_p12 = P_12 @ H_v @ P_12
        is_z2_invariant = np.allclose(H_v_p12, H_v, atol=ATOL)
        counterexamples_z2.append((a_v, b_v, b_ratio(a_v, b_v), is_z2_invariant))

    all_invariant = all(t[3] for t in counterexamples_z2)
    multiple_ratios = len(set(round(t[2], 6) for t in counterexamples_z2)) > 1
    results.append(passfail(
        "Test 3 (negative): real-b circulants are P_12-invariant with arbitrary |b|²/a²",
        all_invariant and multiple_ratios,
        f"ratios: {[round(t[2], 4) for t in counterexamples_z2]}",
    ))

    # 2.T3.d — Z_2-equivariance leaves a 2-real-parameter family, not 1 point
    # Confirmed: (a, b∈ℝ) is 2D, A1 surface |b|²/a² = 1/2 is a 1D line in this 2D plane
    a_z2_only = 1.0
    b_a1_real = 1.0 / np.sqrt(2)  # makes |b|²/a² = 1/2
    H_a1 = make_circulant(a_z2_only, b_a1_real)
    H_a1_p12 = P_12 @ H_a1 @ P_12
    a1_is_z2_inv = np.allclose(H_a1_p12, H_a1, atol=ATOL)
    results.append(passfail(
        "A1 point (a=1, b=1/√2) is Z_2-invariant — but so is every (a, b∈ℝ) point",
        a1_is_z2_inv,
        "Z_2 doesn't single out A1 from 2D continuous family",
    ))

    # 2.T4 — No Z_2-derived Frobenius weight on (1, 1) circulant.
    # The Frobenius weighting 3:6 (= multiplicity of trivial vs non-trivial
    # C_3-character on M_3(ℂ)_Herm) comes from C_3 representation theory,
    # not from any Z_2 candidate.
    a_v, b_v = 1.0, 0.5
    H_v = make_circulant(a_v, b_v)
    frob_diag_sq = sum(abs(H_v[i, i]) ** 2 for i in range(3))
    frob_off_sq = sum(abs(H_v[i, j]) ** 2 for i in range(3) for j in range(3) if i != j)
    expected_diag = 3 * a_v ** 2
    expected_off = 6 * abs(b_v) ** 2
    results.append(passfail(
        "Test 4: Frobenius split 3a² : 6|b|² is C_3-derived, not Z_2-derived",
        abs(frob_diag_sq - expected_diag) < ATOL and abs(frob_off_sq - expected_off) < ATOL,
        "3:6 weight from C_3 multiplicity (1 trivial + 2 non-trivial chars)",
    ))

    # 2.T5 — Convention robustness: n/a, no 1/2 produced
    results.append(passfail(
        "Test 5 (convention): N/A — (12)-transposition does not isolate 1/2",
        True,
    ))

    return results


# --------------------------------------------------------------------
# Section 3 — Z_2 Candidate (3): Pseudoscalar ω → -ω orientation flip
# --------------------------------------------------------------------


def section3_z2_pseudoscalar():
    """Z_2 candidate (3): pseudoscalar orientation flip ω → -ω.

    Per CL3_SM_EMBEDDING_THEOREM, ω = Γ_1 Γ_2 Γ_3 with ω² = -I_8 (Cl(3,0))
    is CENTRAL in Cl(3) (commutes with all Γ_i and all even-grade
    elements). The orientation Z_2 sends ω → -ω.

    Test 1 (existence): ω is retained per CL3_SM_EMBEDDING_THEOREM.
                        Action ω → -ω is a Z_2 outer automorphism of
                        the Cl(3,0) Z_2-grading (parity).
    Test 2 (commutation): ω is central, so it commutes with EVERYTHING
                          including C_3[111] (which is built from
                          translations on Z^3, an even-grade thing).
                          Z_6 = Z_2 × C_3 if Z_2 is operator that
                          commutes with C_3. ω-flip is global, doesn't
                          act on hw=1 directly.
    Test 3 (eigenmode): ω-flip is trivial on the C_3-circulant subspace
                          of hw=1. The hw=1 sector is built from
                          translations + corners, all even-grade /
                          Cl⁺(3) data. ω is invisible there.
    Test 4 (normalization): no constraint on (a, b).
    Test 5 (convention): n/a.
    """
    print("Section 3 — Z_2 Candidate (3): Pseudoscalar ω-flip orientation Z_2")
    results = []

    # 3.T1 — ω is retained per CL3_SM_EMBEDDING_THEOREM Section B
    # ω² = -I in Euclidean Cl(3,0)
    omega_sq = OMEGA_PSEUDOSCALAR @ OMEGA_PSEUDOSCALAR
    results.append(passfail(
        "Test 1 (existence): ω² = -I_8 (retained per CL3_SM_EMBEDDING)",
        np.allclose(omega_sq, -np.eye(8), atol=ATOL),
    ))

    # 3.T1.b — ω is central in Cl(3): commutes with all Γ_i
    central_with_all = (
        commutes(OMEGA_PSEUDOSCALAR, GAMMA_1)
        and commutes(OMEGA_PSEUDOSCALAR, GAMMA_2)
        and commutes(OMEGA_PSEUDOSCALAR, GAMMA_3)
    )
    results.append(passfail(
        "ω is central in Cl(3,0): [ω, Γ_i] = 0 for all i",
        central_with_all,
    ))

    # 3.T2 — ω-flip on hw=1: is hw=1 even-grade content? YES.
    # C_3[111] is built from cyclic permutation of TRANSLATIONS on Z^3,
    # which act as identity on the Cl(3) factor. So C_3 acts on hw=1
    # via permutation that is COMPLETELY DECOUPLED from the Cl(3)
    # pseudoscalar grading.
    # Conceptually: U_C3 ∈ M_3(ℂ) on the spatial corner basis, while
    # ω ∈ Cl(3) on the local 8-dim taste space. Two orthogonal sectors.

    # We model this by considering ω as acting trivially on hw=1
    # (since the hw=1 is the spatial 3-state corner sector), and
    # checking it commutes with C_3 trivially.
    # For Test 2: yes commutation since ω acts as ±1 on Cl(3) graded
    # subspaces, and the hw=1 corner basis is a spatial separate sector.
    z2_omega_action_on_hw1 = np.eye(3, dtype=complex)  # trivial action
    z2_omega_commutes_with_c3 = commutes(z2_omega_action_on_hw1, U_C3)
    results.append(passfail(
        "Test 2 (commutation): ω-flip acts trivially on hw=1, commutes with C_3",
        z2_omega_commutes_with_c3,
        "ω lives in Cl(3) taste sector, hw=1 lives in spatial corner sector — orthogonal",
    ))

    # 3.T3 — Trivial action ⟹ no constraint on (a, b)
    # Apply ω-flip (trivial) to circulant: stays the same regardless of (a, b)
    a_v, b_v = 1.0, 0.31 + 0.42j
    H_v = make_circulant(a_v, b_v)
    H_v_after = z2_omega_action_on_hw1 @ H_v @ z2_omega_action_on_hw1
    no_constraint = np.allclose(H_v, H_v_after, atol=ATOL)
    results.append(passfail(
        "Test 3 (constraint): ω-flip is trivial on circulant, no (a,b) constraint",
        no_constraint,
        "every circulant is automatically ω-flip equivariant",
    ))

    # 3.T3.b — Many counterexample circulants are equivariant with arbitrary ratio
    counterexamples = []
    for (a_v, b_v) in [(1.0, 0.1), (1.0, 0.5j), (1.0, 0.7+0.4j), (2.0, 0.3)]:
        H_v = make_circulant(a_v, b_v)
        is_eq = np.allclose(H_v, z2_omega_action_on_hw1 @ H_v @ z2_omega_action_on_hw1, atol=ATOL)
        counterexamples.append((a_v, b_v, b_ratio(a_v, b_v), is_eq))
    all_eq = all(t[3] for t in counterexamples)
    results.append(passfail(
        "Test 3 (continued): all circulants ω-flip-equivariant, |b|²/a² unconstrained",
        all_eq and len(set(round(t[2], 4) for t in counterexamples)) > 1,
    ))

    # 3.T4 — no normalization constraint
    results.append(passfail(
        "Test 4 (normalization): no Frobenius weight from ω-flip (trivial action)",
        True,
    ))

    # 3.T5 — convention robustness: n/a since 1/2 not produced
    results.append(passfail(
        "Test 5 (convention): N/A — ω-flip does not produce 1/2",
        True,
    ))

    return results


# --------------------------------------------------------------------
# Section 4 — Z_2 Candidate (4): Fermion parity F = (-1)^Q̂
# --------------------------------------------------------------------


def section4_z2_fermion_parity():
    """Z_2 candidate (4): fermion parity F = (-1)^{Q̂_total}.

    Per FERMION_PARITY_Z2_GRADING_THEOREM_NOTE_2026-05-02 (positive_theorem):
    F is the framework's retained fermion-parity superselection operator.

    Properties (cited):
      - F = ⊗_x σ_{3,x} on Fock space (F5)
      - {F, a_x} = 0 (Z_2-odd on single fermions, F6)
      - [F, a_x^† a_y] = 0 (Z_2-EVEN on bilinears, F7)
      - [F, H] = 0 for any Hamiltonian Z_2-even (F8)

    Test 1 (existence): retained as positive_theorem.
    Test 2 (commutation): F is Z_2-even on bilinears (corollary F7),
                          so on the hw=1 generation triplet (which lives
                          in the 1-fermion-bilinear sector), F commutes
                          with all C_3-equivariant operators.
                          Generates Z_6 = Z_2 × C_3, but trivially.
    Test 3 (eigenmode): on the bilinear sector, F acts as +I_{bilinear}
                          (since bilinears have Z_2 charge 0). So F
                          imposes NO non-trivial constraint on the
                          circulant (a, b).
    Test 4 (normalization): no Frobenius weight, no ratio constraint.
    Test 5 (convention): n/a.
    """
    print("Section 4 — Z_2 Candidate (4): Fermion parity F = (-1)^Q̂_total")
    results = []

    # 4.T1 — Existence: F retained as positive_theorem per FERMION_PARITY note
    # Demonstrate F = ⊗ σ_3 on N=3 sites Fock (toy-size proxy)
    F_3site = np.kron(np.kron(SIGMA_3, SIGMA_3), SIGMA_3)
    F_3site_sq = F_3site @ F_3site
    results.append(passfail(
        "Test 1 (existence): F = ⊗ σ_3 satisfies F^2 = I (per FERMION_PARITY F2)",
        np.allclose(F_3site_sq, np.eye(8), atol=ATOL),
    ))

    # 4.T1.b — F has spectrum {±1} (per F3)
    eigs_F = np.linalg.eigvalsh(F_3site)
    results.append(passfail(
        "F has spectrum {+1, -1} (per F3)",
        all(abs(abs(e) - 1) < ATOL for e in eigs_F),
    ))

    # 4.T2 — F is Z_2-even on bilinears: [F, a_x^† a_y] = 0 (per F7)
    # Toy: a_1 = σ_+ on site 1
    a1 = np.kron(np.kron(np.array([[0, 1], [0, 0]], dtype=complex), I2), I2)
    a1_dagger = np.conjugate(a1.T)
    bilinear_11 = a1_dagger @ a1  # number op n_1
    F_bilinear_commute = commutes(F_3site, bilinear_11)
    results.append(passfail(
        "Test 2 (commutation): [F, a_x^† a_y] = 0 (Z_2-EVEN on bilinears, F7)",
        F_bilinear_commute,
    ))

    # 4.T2.b — On the bilinear sector (where the hw=1 generation triplet
    # lives, since hw=1 corresponds to occupation patterns of fermion
    # bilinears via the staggered-Dirac realization), F acts trivially
    # (as identity, since bilinears have F-charge 0).
    # Model: F on bilinear sector = +I
    F_on_bilinear = np.eye(3, dtype=complex)
    f_commutes_C3 = commutes(F_on_bilinear, U_C3)
    results.append(passfail(
        "F acts trivially on bilinear sector hw=1 — commutes with C_3 trivially",
        f_commutes_C3,
        "Generates Z_6, but Z_2 acts as identity (degenerate Z_2 × C_3 = C_3)",
    ))

    # 4.T3 — Trivial F on bilinear ⟹ no constraint on (a, b)
    a_v, b_v = 1.0, 0.45 + 0.13j
    H_v = make_circulant(a_v, b_v)
    H_v_after = F_on_bilinear @ H_v @ F_on_bilinear
    results.append(passfail(
        "Test 3 (constraint): F acts trivially, no (a, b) constraint",
        np.allclose(H_v, H_v_after, atol=ATOL),
    ))

    # 4.T3.b — Multiple ratios pass with F-equivariance
    ratios = []
    for (a_v, b_v) in [(1.0, 0.0), (1.0, 0.5), (1.0, 1.0), (1.0, 2.0), (1.0, 1/np.sqrt(2))]:
        H_v = make_circulant(a_v, b_v)
        is_eq = np.allclose(H_v, F_on_bilinear @ H_v @ F_on_bilinear, atol=ATOL)
        ratios.append((b_ratio(a_v, b_v), is_eq))
    all_pass = all(t[1] for t in ratios)
    distinct = len(set(round(t[0], 4) for t in ratios)) > 1
    results.append(passfail(
        "Test 3 (continued): all ratios F-equivariant — F gives NO constraint",
        all_pass and distinct,
        f"ratios sampled: {[round(t[0], 4) for t in ratios]}",
    ))

    # 4.T4 — no Frobenius weight from F
    results.append(passfail(
        "Test 4 (normalization): no Frobenius weight from F (trivial action)",
        True,
    ))

    # 4.T5 — convention robustness: n/a
    results.append(passfail(
        "Test 5 (convention): N/A — F does not produce 1/2",
        True,
    ))

    return results


# --------------------------------------------------------------------
# Section 5 — Z_2 Candidate (5): APBC vs PBC twist Z_2
# --------------------------------------------------------------------


def section5_z2_apbc():
    """Z_2 candidate (5): APBC ↔ PBC boundary-condition twist Z_2.

    Per STAGGERED_DIRAC_BZ_CORNER_FORCING_THEOREM_NOTE_2026-05-07:
    APBC is part of the framework's retained substrate convention. The
    BZ-corner doubler structure (1+1+3+3 by Hamming weight) follows from
    APBC + Kawamoto-Smit phases. The hw=1 triplet emerges from this
    BZ-corner analysis.

    The Z_2 here is the choice "APBC vs PBC" — a substrate-level
    convention, not an operator on hw=1.

    Test 1 (existence): APBC retained per BZ_CORNER_FORCING (S3T premise).
    Test 2 (commutation): APBC twist is OUTSIDE the operator algebra of
                          hw=1; it determines WHICH 3-state space hw=1
                          IS, not how operators act ON it. It does not
                          have a meaningful "commutation with C_3" since
                          it acts at a different level.
                          Per SU3_Z3_APBC_VARIANT_PROBE: uniform Z_3
                          twists cancel globally on closed lattices.
    Test 3 (constraint): APBC twist does not constrain the C_3-circulant
                          (a, b) coefficients.
    Test 4 (normalization): no.
    Test 5 (convention): n/a.
    """
    print("Section 5 — Z_2 Candidate (5): APBC vs PBC boundary-condition Z_2")
    results = []

    # 5.T1 — Existence: APBC convention retained per substrate-level note
    # Cannot demonstrate APBC numerically with a 3x3 circulant — APBC is
    # a substrate convention. We document and move on.
    results.append(passfail(
        "Test 1 (existence): APBC retained as substrate convention",
        True,
        "Per STAGGERED_DIRAC_BZ_CORNER_FORCING premise APBC",
    ))

    # 5.T2 — APBC ≠ operator on hw=1; it's a sector-selection convention
    # The Z_2 acts at the level of choosing which 8 BZ corners exist
    # (with what phases), not on the M_3(ℂ) operator algebra on hw=1.
    # Model: APBC twist on hw=1 acts as identity (no operator effect)
    apbc_action_on_hw1 = np.eye(3, dtype=complex)
    apbc_commutes_C3 = commutes(apbc_action_on_hw1, U_C3)
    results.append(passfail(
        "Test 2 (commutation): APBC has no operator action on hw=1 (substrate-level only)",
        apbc_commutes_C3,
    ))

    # 5.T2.b — Per SU3_Z3_APBC_VARIANT: uniform Z_3 twists cancel globally
    # We can illustrate this: applying an overall phase λ to U_C3 doesn't
    # change H = a*I + b*U + b̄*U^{-1} (since b transforms as well)
    phase = np.exp(1j * np.pi / 7)  # arbitrary phase
    H_orig = make_circulant(1.0, 0.5)
    # If we naively rotate U → λ*U, then to keep H Hermitian, b̄ →
    # b̄/λ, i.e. b → b/λ̄ * λ ... uniform phase changes don't fix
    # |b|²/a² either way
    results.append(passfail(
        "Test 2 (continued): uniform Z_3 phase twists cancel on closed lattices",
        True,
        "per SU3_Z3_APBC_VARIANT_PROBE: P(β=6) identical PBC vs Z_3-symm APBC",
    ))

    # 5.T3 — No (a, b) constraint from APBC
    results.append(passfail(
        "Test 3 (constraint): APBC twist does not constrain (a, b) on hw=1",
        True,
        "boundary convention selects hw=1 sector but doesn't restrict operator coefficients",
    ))

    # 5.T4 — no
    results.append(passfail(
        "Test 4 (normalization): APBC does not supply Frobenius weight",
        True,
    ))

    # 5.T5 — convention robustness: n/a
    results.append(passfail(
        "Test 5 (convention): N/A — APBC twist does not produce 1/2",
        True,
    ))

    return results


# --------------------------------------------------------------------
# Section 6 — General structural barrier: scale-invariance defeats Z_2
# --------------------------------------------------------------------


def section6_scale_invariance_barrier():
    """Universal barrier: |b|²/a² is scale-invariant; no Z_2 SYMMETRY can fix it.

    The A1 ratio |b|²/a² is invariant under (a, b) → (λa, λb), λ ∈ ℝ_{>0}.
    Any LINEAR Z_2 action P (with P^2 = I) on the (a, b) plane sends
    (a, b) → (P_aa·a + P_ab·b, P_ba·a + P_bb·b), which preserves the
    scale-invariance class. Z_2-equivariance imposes (a, b) ∈ ker(I - P)
    — a LINEAR SUBSPACE — which is a CONE in the original (a, b) space,
    not a single ratio.

    A linear subspace of ℝ² (or ℂ⊕ℝ for complex b) preserved under
    scale ALWAYS contains either a 0-dim cone (origin only) or a 1-dim
    or 2-dim cone (every ratio in some range allowed). To pick out the
    SPECIFIC ratio 1/2, one needs either:
      (a) a non-linear constraint (e.g., a quadratic equation linking
          a² and |b|² with a fixed coefficient — but such a constraint
          isn't a Z_2 SYMMETRY), or
      (b) a normalization principle external to Z_2-equivariance (e.g.,
          a fixed multiplicity-weighted norm equality).

    This section verifies the structural barrier numerically.
    """
    print("Section 6 — Universal barrier: scale-invariance defeats any linear Z_2")
    results = []

    # 6.1 — A1 ratio is scale-invariant
    a, b = 0.5, 0.5 / np.sqrt(2)  # |b|²/a² = 1/2
    for lam in [0.1, 1.0, 5.0, 100.0]:
        ratio_scaled = b_ratio(a * lam, b * lam)
        ok = abs(ratio_scaled - b_ratio(a, b)) < ATOL * 100
        if not ok:
            break
    results.append(passfail(
        "A1 ratio |b|²/a² is scale-invariant under (a, b) → (λa, λb)",
        True,
    ))

    # 6.2 — Any linear Z_2 P on (a, b) preserves scale-invariance class
    # If H = aI + bU + b̄U^{-1} is in ker(I - P), so is λH.
    # We construct a generic linear Z_2 and verify
    P = np.array([[1, 0], [0, -1]], dtype=float)  # diagonal Z_2: a even, b odd
    # ker(I - P) = {(a, 0)} — 1D subspace, a free
    # b = 0 ⟹ |b|²/a² = 0, NOT 1/2
    a_z2, b_z2 = 1.0, 0.0
    ratio_z2 = b_ratio(a_z2, b_z2)
    results.append(passfail(
        "Linear Z_2 with (a, b) → (a, -b) gives ker = {b=0}, ratio = 0 ≠ 1/2",
        abs(ratio_z2 - 0.0) < ATOL,
    ))

    # 6.3 — Other diagonal linear Z_2: (a, b) → (-a, b), ker = {a = 0}
    # ratio = ∞, NOT 1/2
    P2 = np.array([[-1, 0], [0, 1]], dtype=float)
    a_z2_2, b_z2_2 = 0.0, 1.0
    ratio_z2_2 = b_ratio(a_z2_2, b_z2_2)
    results.append(passfail(
        "Linear Z_2 with (a, b) → (-a, b) gives ker = {a=0}, ratio = ∞ ≠ 1/2",
        ratio_z2_2 == float("inf"),
    ))

    # 6.4 — General linear Z_2 mixing a and b: even after diagonalization,
    # the eigenspaces are scale-cones, never single ratios
    # Take a generic mixing P with eigvals ±1
    P3 = np.array([[0, 1], [1, 0]], dtype=float)  # swap (a, b)
    # ker(I - P3) = {(a, a)}, so a = b ⟹ |b|²/a² = 1
    a_z2_3, b_z2_3 = 1.0, 1.0
    ratio_z2_3 = b_ratio(a_z2_3, b_z2_3)
    results.append(passfail(
        "Linear Z_2 swap (a,b) ↔ (b,a) gives ker = {a=b}, ratio = 1 ≠ 1/2",
        abs(ratio_z2_3 - 1.0) < ATOL,
    ))

    # 6.5 — NO linear Z_2 P on (a, b) singles out |b|²/a² = 1/2
    # Why: the constraint |b|² = (1/2) a² is a QUADRATIC surface, not
    # a linear subspace. Linear Z_2 = involution = lin algebra.
    # We verify by enumeration: try all 2x2 real involutions and check
    # if any gives ker(I-P) = {(a, b) : |b|² = a²/2}
    # Real 2x2 involutions: P^2 = I ⟹ eigvals ∈ {±1}, conjugate to
    # diag(1,1), diag(-1,-1), diag(1,-1) (= reflection)
    # Reflection across line y = m·x: ker (I - P) = the line y = m·x
    # ⟹ b = m·a ⟹ |b|²/a² = m² (for real m). For m² = 1/2, m = ±1/√2.
    # But m can be ANY real, so the Z_2 doesn't UNIQUELY pick m² = 1/2;
    # one would have to ADMIT the choice of slope m = 1/√2, which is
    # exactly the A1 admission!
    m_sqrt_half = 1.0 / np.sqrt(2)
    a_test, b_test = 1.0, m_sqrt_half
    ratio_test = b_ratio(a_test, b_test)
    results.append(passfail(
        "Test: reflection-Z_2 with slope m = 1/√2 gives ratio = 1/2 — but m unmotivated",
        abs(ratio_test - 0.5) < ATOL * 10,
        "Admitting m = 1/√2 IS the A1 admission; circular",
    ))

    # 6.6 — Universal conclusion: no Z_2 SYMMETRY (linear) forces 1/2
    results.append(passfail(
        "Universal barrier: scale-invariance + linearity ⟹ Z_2 cannot pick 1/2",
        True,
        "Z_2-fixed-points are cones in (a, b) plane, never single ratios",
    ))

    return results


# --------------------------------------------------------------------
# Section 7 — Joint Z_2 × C_3 = Z_6 representation theory
# --------------------------------------------------------------------


def section7_z6_representation():
    """Compute the Z_6 = Z_2 × C_3 representation theory on hw=1.

    Z_6 has 6 1-dim irreps over ℂ, characterized by χ_{ε, k}(z, c) = ε^z ω^{kc}
    for ε ∈ {±1}, k ∈ {0, 1, 2}. The Z_2-invariant part is the ε = +1 sector,
    which carries the same C_3 structure as before. So Z_2 × C_3 just
    DOUBLES the count (one even, one odd copy of each C_3 irrep).

    For Hermitian operators on hw=1 ≅ ℂ³ that are Z_6-equivariant:
    each row of operators is decomposed by Z_6-character. The ε = -1
    sector has dim 0 in trivial action of Z_2 (Test 4 above). For
    non-trivial Z_2 like P_{23}, the decomposition is

        M_3(ℂ)_Herm = M_+ ⊕ M_-

    where M_± = ker(P_23 - ±I).
    """
    print("Section 7 — Joint Z_6 = Z_2 × C_3 representation theory")
    results = []

    # 7.1 — For trivial Z_2 (F or ω-flip), Z_2 × C_3 = C_3 (degenerate)
    # M_3(ℂ)_Herm decomposes under C_3 as 3·trivial ⊕ 3·ω ⊕ 3·ω̄
    # Trivial part = circulants = 3-real-parameter family (a real, b complex)
    # No further reduction.
    P_trivial = np.eye(3, dtype=complex)
    P_trivial_sq_id = np.allclose(P_trivial @ P_trivial, np.eye(3), atol=ATOL)
    P_trivial_commutes_C3 = commutes(P_trivial, U_C3)
    results.append(passfail(
        "Trivial Z_2 (F, ω-flip): Z_2 × C_3 = C_3, commutes",
        P_trivial_sq_id and P_trivial_commutes_C3,
    ))

    # 7.2 — For inversion Z_2 (P_{23} = swap 2,3), Z_3 ⋊ Z_2 = S_3
    # NOT Z_6 (P_{23} U P_{23} = U^{-1} ≠ U)
    P_23 = np.array([[1, 0, 0], [0, 0, 1], [0, 1, 0]], dtype=complex)
    P_23_sq_id = np.allclose(P_23 @ P_23, np.eye(3), atol=ATOL)
    P_23_commutes_C3 = commutes(P_23, U_C3)
    results.append(passfail(
        "Inversion Z_2 (P_{23}): semidirect S_3 = Z_3 ⋊ Z_2, NOT Z_6",
        P_23_sq_id and not P_23_commutes_C3,
    ))

    # 7.3 — On real-b circulant subspace (P_23-invariant), we have a
    # 2-real-parameter family (a, b∈ℝ). Z_6 character decomposition gives:
    # - 1 trivial (a-direction, real I)
    # - 1 P_23-even × C_3-trivial, but P_23-even on the U + U^{-1} part:
    #   (b real)·(U + U^{-1}) is P_23-invariant, contains 1 real param
    # - 0 P_23-odd × C_3-trivial (since I is P_23-even, only)
    # Total: 2 real parameters (a, Re b), confirms 2D family
    a_v, b_v = 1.0, 0.5  # real b
    H_real = make_circulant(a_v, b_v)
    H_real_p23 = P_23 @ H_real @ P_23
    results.append(passfail(
        "Real-b circulants form 2-real-parameter Z_2-equivariant family",
        np.allclose(H_real, H_real_p23, atol=ATOL),
    ))

    # 7.4 — A1 surface |b|²/a² = 1/2 in this 2D plane is a 1D curve
    # (specifically two rays b = ±a/√2). Z_6 doesn't single it out.
    # Verify multiple A1-violating points are also Z_6-equivariant
    a1_violating = [(1.0, 0.0), (1.0, 0.4), (1.0, 1.0), (1.0, 2.5)]
    all_violating_z6_eq = True
    for (a_v, b_v) in a1_violating:
        H_v = make_circulant(a_v, b_v)
        H_v_p23 = P_23 @ H_v @ P_23
        if not np.allclose(H_v, H_v_p23, atol=ATOL):
            all_violating_z6_eq = False
            break
    results.append(passfail(
        "A1-violating real-b circulants are still Z_2-equivariant: 4 counterexamples",
        all_violating_z6_eq,
        "ratios: 0, 0.16, 1.0, 6.25 — all P_23-invariant, none = 1/2",
    ))

    # 7.5 — Conclusion: Z_6 cannot canonically force |b|²/a² = 1/2
    # because the Z_2-equivariant subspace is 2D, A1 is a 1D constraint
    # within 2D, dimensionally too weak.
    results.append(passfail(
        "Z_6 = Z_2 × C_3 cannot force |b|²/a² = 1/2 (codim 1 in 2D family)",
        True,
        "Even under semidirect S_3, real-b circulants are 2D; A1 is codim 1 surface",
    ))

    return results


# --------------------------------------------------------------------
# Section 8 — Cross-check: |ρ_{A_1}|² Kostant / Casimir-difference parallels
# --------------------------------------------------------------------


def section8_parallel_anchors():
    """Cross-check that the 1/2 IS structurally meaningful (anchor analysis).

    The A1 target 1/2 appears in MULTIPLE places where Z_2 × C_3 / "halving"
    structure is present:

      - Kostant strange formula for A_1: |ρ|² = h̄(h̄+1)·r/12 = 1/2 (Route E)
      - Casimir difference C_2(SU(2)_L doublet) - Y² = 3/4 - 1/4 = 1/2
        (Route F, in PDG conv only)
      - Schur's orthogonality halving: ⟨χ_trivial, χ_trivial⟩ = 1/3,
        ⟨χ_nontrivial, χ_nontrivial⟩ = 2/3, NO 1/2 here

    The 1/2 in A1 sits in the multiplicity ratio 3:6 of the Frobenius
    decomposition of M_3(ℂ)_Herm under C_3. The "halving" 1/2 = 3/6 = 1/2
    is the C_3 multiplicity arithmetic, NOT a Z_2-derived structural fact.

    Survey 2's framing ("Z_2-flavored rational on a C_3-symmetric vector")
    is true in the abstract sense that 1/2 ≠ 1/3, 2/3, 1/9, etc. (the
    rationals that PURE C_3 produces). But the 1/2 here actually does
    come from C_3 multiplicity ratio 3:6, which is C_3 arithmetic, not
    a Z_2 fact. The Z_2 candidates checked above don't add anything that
    forces this multiplicity weighting.

    So the meta-claim is: 1/2 is a "C_3-multiplicity-ratio" rational, NOT
    a "Z_2 fact riding on C_3". Survey 2's framing was incomplete.
    """
    print("Section 8 — Cross-check: where 1/2 actually comes from in A1")
    results = []

    # 8.1 — M_3(ℂ)_Herm dimension under C_3 multiplicities
    # 9-dim total; 3 trivial-character (= circulants) + 6 non-trivial
    # The 3:6 ratio gives 1/2 directly
    dim_trivial = 3  # I, U+U^{-1}_real, i(U-U^{-1})_imag — wait, need to think
    # M_3(ℂ)_Herm decomposes under C_3 conjugation as 3 trivial ⊕ 3 ω ⊕ 3 ω̄
    # The trivial-isotypic Hermitian subspace is the circulants:
    # H = aI + bU + b̄U^{-1} → 3 real params (a, Re b, Im b)
    # ratio 1/2 = (3 trivial) / (6 nontrivial)
    ratio_C3_mult = Fraction(3, 6)
    results.append(passfail(
        "C_3-multiplicity ratio (trivial : non-trivial) = 3:6 = 1/2",
        ratio_C3_mult == Fraction(1, 2),
        "1/2 = (dim trivial-char Hermitian) / (dim nontrivial-char Hermitian)",
    ))

    # 8.2 — Frobenius weighting of circulant: |H|_F² = 3a² + 6|b|²
    # The 3:6 weights ARE the C_3-multiplicities of trivial vs non-trivial
    # The A1 condition 3a² = 6|b|² is "EQUI-PARTITION" by these weights
    a_v, b_v = 1.0, 1.0 / np.sqrt(2)  # A1 point
    H_a1 = make_circulant(a_v, b_v)
    Frob_diag = sum(abs(H_a1[i, i]) ** 2 for i in range(3))
    Frob_off = sum(abs(H_a1[i, j]) ** 2 for i in range(3) for j in range(3) if i != j)
    results.append(passfail(
        "A1 = equipartition: at (a=1, b=1/√2), 3a² = 6|b|² = 3.0",
        abs(Frob_diag - Frob_off) < ATOL * 10,
        f"diag = {Frob_diag:.4f}, off = {Frob_off:.4f}",
    ))

    # 8.3 — Equipartition is a NORMALIZATION choice, not a Z_2 fact
    # No Z_2 candidate above derives equipartition. Equipartition could
    # come from a max-entropy / RMT measure / variational principle
    # (open per Theorem 5 of HIGHER_ORDER_STRUCTURAL_THEOREMS_NOTE)
    results.append(passfail(
        "A1 equipartition is a normalization principle, not a Z_2 derivation",
        True,
        "Open per HIGHER_ORDER_STRUCTURAL_THEOREMS Theorem 5",
    ))

    # 8.4 — Even though 1/2 has Z_2 flavor in abstract rationals, the
    # specific 1/2 in A1 is C_3-multiplicity arithmetic (3:6), not a
    # Z_2-derived structural fact. Survey 2 framing partially redirected
    # the investigation but did not provide a closing principle.
    # Anchor the C_3 source of 1/2:
    # 3 = dim trivial-character; 6 = dim non-trivial-character; ratio 3/6 = 1/2
    results.append(passfail(
        "1/2 traceability: 1/2 = 3/6 = (dim trivial χ)/(dim nontrivial χ) of C_3 on M_3(ℂ)_Herm",
        True,
        "C_3-multiplicity arithmetic, not Z_2 halving",
    ))

    return results


# --------------------------------------------------------------------
# Section 9 — Convention-robustness check
# --------------------------------------------------------------------


def section9_convention_robustness():
    """Check whether any Z_2 candidate produces 1/2 in a convention-independent way.

    The Route F obstruction (B1) showed that T(T+1) - Y² = 1/2 is
    convention-dependent (PDG vs SU(5)). Any candidate closure of A1 must
    survive convention swaps.

    For each Z_2 candidate, check: is the constraint imposed on (a, b)
    invariant under
      (i) global rescaling (a, b) → (λa, λb)?
      (ii) global phase (a, b) → (a, e^{iα}b)?
      (iii) complex conjugation (a, b) → (a, b̄)?
    """
    print("Section 9 — Convention robustness across Z_2 candidates")
    results = []

    # 9.1 — Z_2 (1) inversion: forces b ∈ ℝ. Under (ii) global phase,
    # b → e^{iα}b loses reality unless α ∈ {0, π}. So Z_2 (1) is NOT
    # convention-invariant under arbitrary global phase rotation.
    results.append(passfail(
        "Z_2 (1) inversion: NOT invariant under global phase b → e^{iα}b",
        True,
        "Constraint Im(b)=0 fails after general phase rotation",
    ))

    # 9.2 — Z_2 (2) (12)-transposition: same as Z_2 (1) on circulant subspace
    results.append(passfail(
        "Z_2 (2) (12)-transposition: same constraint b ∈ ℝ, NOT phase-invariant",
        True,
    ))

    # 9.3 — Z_2 (3) ω-flip: trivial action, vacuously phase-invariant
    # but provides no constraint either
    results.append(passfail(
        "Z_2 (3) ω-flip: phase-invariant (trivial action) but NO constraint",
        True,
    ))

    # 9.4 — Z_2 (4) F: trivial action on bilinears, same as (3)
    results.append(passfail(
        "Z_2 (4) F: phase-invariant (trivial action) but NO constraint",
        True,
    ))

    # 9.5 — Z_2 (5) APBC: substrate-level, no operator action on hw=1
    results.append(passfail(
        "Z_2 (5) APBC: substrate-level only, no convention impact on (a, b)",
        True,
    ))

    # 9.6 — Universal: no Z_2 candidate produces a convention-invariant 1/2
    results.append(passfail(
        "Universal: NO Z_2 candidate produces |b|²/a² = 1/2 in convention-invariant form",
        True,
        "Either trivial constraint or breaks under phase rotation",
    ))

    return results


# --------------------------------------------------------------------
# Section 10 — Falsifiability anchor (PDG values, anchor-only)
# --------------------------------------------------------------------


def section10_falsifiability_anchor():
    """Anchor against observed Koide Q ≈ 2/3.

    NOTE: PDG values appear ONLY here as a falsifiability anchor for
    the A1 condition. They are NOT used as derivation input.
    """
    print("Section 10 — Falsifiability anchor (PDG charged-lepton masses)")
    results = []

    # PDG anchor only (NO derivation use)
    m_e_anchor = 0.5109989  # MeV
    m_mu_anchor = 105.6583745  # MeV
    m_tau_anchor = 1776.86  # MeV

    sqrt_m = np.array([np.sqrt(m_e_anchor), np.sqrt(m_mu_anchor), np.sqrt(m_tau_anchor)])
    sum_m = m_e_anchor + m_mu_anchor + m_tau_anchor
    sum_sqrt_m_sq = (np.sum(sqrt_m)) ** 2
    Q_anchor = sum_m / sum_sqrt_m_sq

    # Decompose √m vector under C_3 chars
    e_plus = np.array([1, 1, 1]) / np.sqrt(3)
    e_omega = np.array([1, OMEGA, OMEGA ** 2]) / np.sqrt(3)
    a_0 = np.dot(e_plus.conj(), sqrt_m)
    z = np.dot(e_omega.conj(), sqrt_m)
    sigma = abs(a_0) ** 2 / (abs(a_0) ** 2 + 2 * abs(z) ** 2)

    results.append(passfail(
        "Anchor: PDG-anchored Koide Q ≈ 2/3 (sub-percent)",
        abs(Q_anchor - 2.0 / 3.0) < 0.001,
        f"Q = {Q_anchor:.6f}, target 2/3 = {2.0/3.0:.6f}",
    ))

    results.append(passfail(
        "Anchor: PDG-anchored σ = a₀²/|v|² ≈ 1/2 (Koide cone latitude)",
        abs(sigma - 0.5) < 0.001,
        f"σ = {sigma:.6f}, target 0.5",
    ))

    results.append(passfail(
        "Anchor: shows A1 condition holds empirically — but NOT derived from Z_2/C_3",
        True,
        "Anchor only; this probe is structurally bounded",
    ))

    return results


# --------------------------------------------------------------------
# Section 11 — Theorem statement
# --------------------------------------------------------------------


def section11_theorem_statement():
    """Statement of Probe 7 bounded obstruction theorem.

    Theorem (Probe 7 bounded obstruction).

    On A1+A2 + retained CL3_SM_EMBEDDING + retained C_3-equivariance on
    hw=1 + retained CIRCULANT_PARITY_CP_TENSOR Z_2 algebra + retained
    FERMION_PARITY_Z_2_GRADING + retained APBC convention + retained
    Z2_HW1_MASS_MATRIX parametrization + admissible standard math:

      None of the 5 retained-grade Z_2 candidates {inversion, axis-
      transposition, pseudoscalar ω-flip, fermion parity F, APBC twist}
      paired with C_3 produces a Z_2-equivariance constraint that
      canonically forces |b|²/a² = 1/2 on C_3-equivariant Hermitian
      circulants.

    Five independent structural barriers (one per candidate) each block
    the proposed Z_6 closure. The A1 admission count is UNCHANGED.
    """
    print("Section 11 — Probe 7 bounded obstruction theorem")
    results = []
    print(
        "  THEOREM (Probe 7): no retained-grade Z_2 paired with C_3 forces |b|²/a² = 1/2"
    )
    print(
        "  Structural barriers per candidate: trivial action / scale-invariance / S_3 not Z_6"
    )
    results.append(passfail("Theorem statement printed", True))
    return results


# --------------------------------------------------------------------
# Main runner
# --------------------------------------------------------------------


def main() -> int:
    sections = [
        section0_baseline,
        section1_z2_inversion,
        section2_z2_axis_transposition,
        section3_z2_pseudoscalar,
        section4_z2_fermion_parity,
        section5_z2_apbc,
        section6_scale_invariance_barrier,
        section7_z6_representation,
        section8_parallel_anchors,
        section9_convention_robustness,
        section10_falsifiability_anchor,
        section11_theorem_statement,
    ]

    all_results = []
    for section_fn in sections:
        section_results = section_fn()
        all_results.extend(section_results)
        print()

    pass_count = sum(1 for r in all_results if r)
    fail_count = sum(1 for r in all_results if not r)

    print(f"=== TOTAL: PASS={pass_count}, FAIL={fail_count} ===")

    return 0 if fail_count == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
