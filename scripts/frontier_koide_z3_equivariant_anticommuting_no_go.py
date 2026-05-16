#!/usr/bin/env python3
"""Koide Z_3-Equivariant Anti-Commuting Operator No-Go.

Verifies the algebraic content of
`docs/KOIDE_Z3_EQUIVARIANT_ANTICOMMUTING_NO_GO_NOTE_2026-05-16.md`.

Theorem: let H be Hermitian (real symmetric) on R^3 such that
(i) [H, R] = 0 (Z_3-equivariance, R = cyclic shift), AND
(ii) {H, Γ_χ} = 0 (anti-commutation with Z_3 character grading
     Γ_χ = (2/3)J − I).
Then H = 0.

Corollary (Connes-Lott): the Yukawa Dirac off-diagonal block in any
finite spectral triple on Cl(3) ⋊ Z_3, if forced to be Z_3-equivariant
by Connes' first-order condition AND if identified to anti-commute
with Γ_χ on the 3-generation triplet, must be zero. Hence the
Connes-Lott construction cannot directly realize the anti-commuting
Hermitian H of `KOIDE_ANTICOMMUTING_OPERATOR_DERIVATION_THEOREM_NOTE_2026-05-10`.

The runner verifies (purely algebraic, no measured masses):

  (1) Setup: R cyclic shift, R^3 = I; Γ_χ = (2/3) J - I
  (2) Γ_χ is a circulant: Γ_χ = (-1/3) I + (2/3) R + (2/3) R²
  (3) Circulant H = a I + b R + c R²; verify [H, Γ_χ] = 0 identically
  (4) {H, Γ_χ} = 2 H Γ_χ when H, Γ_χ both circulant; reduces to H Γ_χ = 0
  (5) Z_3 Fourier basis: H, Γ_χ both diagonal; HΓ_χ = 0 ⟹ 3-equation
      linear system on (a, b, c) with invertible Z_3 character matrix
      forcing a = b = c = 0
  (6) Explicit examples: non-trivial circulants (e.g. R, R-R^T)
      give non-vanishing {·, Γ_χ}
  (7) Connes-Lott corollary: off-diagonal Yukawa block forced to zero
  (8) Disjointness from anti-commuting 2-dim family: H = (1/3)(1⊗h+h⊗1)
      with Σh = 0 has [H, R] = 0 only at h = 0

All algebraic verifications use sympy on arbitrary symbolic parameters;
no PDG / measured / empirical lepton masses are consumed.
"""

from __future__ import annotations

import sys

import sympy as sp

PASS_COUNT = 0
FAIL_COUNT = 0
CLASS_A_HITS = 0


def check(label: str, condition: bool, detail: str = "", class_a: bool = False) -> bool:
    global PASS_COUNT, FAIL_COUNT, CLASS_A_HITS
    status = "PASS" if condition else "FAIL"
    if condition:
        PASS_COUNT += 1
        if class_a:
            CLASS_A_HITS += 1
    else:
        FAIL_COUNT += 1
    tag = " [A]" if class_a else ""
    msg = f"  [{status}]{tag} {label}"
    if detail:
        msg += f"  ({detail})"
    print(msg)
    return condition


# ============================================================================
# Setup: cyclic shift R, all-ones matrix J, Γ_χ
# ============================================================================

R = sp.Matrix(
    [
        [0, 0, 1],
        [1, 0, 0],
        [0, 1, 0],
    ]
)
J = sp.ones(3, 3)
I3 = sp.eye(3)
Gamma_chi = sp.Rational(2, 3) * J - I3


def part1_setup() -> None:
    """Verify the basic algebraic identities R^3 = I, J = I + R + R²."""
    print()
    print("=" * 78)
    print("PART 1: SETUP — R CYCLIC SHIFT, R^3 = I, J = I + R + R²")
    print("=" * 78)

    R3 = R * R * R
    check(
        "R^3 = I",
        sp.simplify(R3 - I3) == sp.zeros(3),
        class_a=True,
    )

    R2 = R * R
    sum_RR = I3 + R + R2
    check(
        "I + R + R² = J (all-ones)",
        sp.simplify(sum_RR - J) == sp.zeros(3),
        class_a=True,
    )

    # R^T = R^{-1} = R²
    Rt = R.T
    check(
        "R^T = R²",
        sp.simplify(Rt - R2) == sp.zeros(3),
        class_a=True,
    )


def part2_gamma_chi_is_circulant() -> None:
    """Verify Γ_χ = (-1/3) I + (2/3) R + (2/3) R² (a circulant)."""
    print()
    print("=" * 78)
    print("PART 2: Γ_χ IS A CIRCULANT")
    print("=" * 78)

    R2 = R * R
    expected = -sp.Rational(1, 3) * I3 + sp.Rational(2, 3) * R + sp.Rational(2, 3) * R2

    print(f"  Γ_χ = (2/3) J - I = ")
    print(f"  {Gamma_chi}")
    print(f"  Expected: (-1/3) I + (2/3) R + (2/3) R² = ")
    print(f"  {expected}")

    check(
        "Γ_χ = (-1/3) I + (2/3) R + (2/3) R²  (circulant)",
        sp.simplify(Gamma_chi - expected) == sp.zeros(3),
        class_a=True,
    )

    # Commutativity: [Γ_χ, R] = 0
    comm_Gamma_R = Gamma_chi * R - R * Gamma_chi
    check(
        "[Γ_χ, R] = 0  (Γ_χ commutes with R since both circulant)",
        sp.simplify(comm_Gamma_R) == sp.zeros(3),
        class_a=True,
    )

    comm_Gamma_R2 = Gamma_chi * R2 - R2 * Gamma_chi
    check(
        "[Γ_χ, R²] = 0",
        sp.simplify(comm_Gamma_R2) == sp.zeros(3),
        class_a=True,
    )


def part3_circulant_H_commutes_with_Gamma() -> None:
    """For Z_3-equivariant H = a I + b R + c R², verify [H, Γ_χ] = 0."""
    print()
    print("=" * 78)
    print("PART 3: CIRCULANT H = a I + b R + c R² COMMUTES WITH Γ_χ")
    print("=" * 78)

    a, b, c = sp.symbols("a b c", real=True)
    R2 = R * R
    H = a * I3 + b * R + c * R2

    print(f"  H = a I + b R + c R² (symbolic Z_3-equivariant Hermitian)")
    print(f"  Note: H is Hermitian iff coefficient of R^T = coefficient of R")
    print(f"        i.e., c = b for real Hermitian; this restricts to a 2-param")
    print(f"        Hermitian subspace inside the 3-param circulant algebra.")

    # General circulant commutes with Γ_χ
    comm_HR = H * Gamma_chi - Gamma_chi * H
    check(
        "[H, Γ_χ] = 0  for all (a, b, c)  (commutative circulant algebra)",
        sp.simplify(comm_HR) == sp.zeros(3),
        class_a=True,
    )

    # Z_3-equivariance: [H, R] = 0 automatic
    comm_HR2 = H * R - R * H
    check(
        "[H, R] = 0  for all (a, b, c)  (Z_3-equivariance of circulants)",
        sp.simplify(comm_HR2) == sp.zeros(3),
        class_a=True,
    )


def part4_anticommutation_reduces_to_product() -> None:
    """Verify {H, Γ_χ} = 2 H Γ_χ when both H, Γ_χ are circulant."""
    print()
    print("=" * 78)
    print("PART 4: {H, Γ_χ} REDUCES TO 2 H Γ_χ (BOTH CIRCULANT)")
    print("=" * 78)

    a, b, c = sp.symbols("a b c", real=True)
    R2 = R * R
    H = a * I3 + b * R + c * R2

    anticomm = H * Gamma_chi + Gamma_chi * H
    twoHGamma = 2 * H * Gamma_chi

    check(
        "{H, Γ_χ} = 2 H Γ_χ  (since [H, Γ_χ] = 0)",
        sp.simplify(anticomm - twoHGamma) == sp.zeros(3),
        class_a=True,
    )

    print("  Therefore {H, Γ_χ} = 0  ⟺  H Γ_χ = 0  for Z_3-equivariant H")


def part5_fourier_basis_forces_zero() -> None:
    """In Z_3 Fourier basis, H Γ_χ = 0 ⟹ 3-equation system forcing a = b = c = 0."""
    print()
    print("=" * 78)
    print("PART 5: Z_3 FOURIER BASIS — H Γ_χ = 0 FORCES a = b = c = 0")
    print("=" * 78)

    a, b, c = sp.symbols("a b c", real=True)
    omega = sp.exp(2 * sp.pi * sp.I / 3)

    # H diagonal eigenvalues in Z_3 Fourier basis
    h_eigs = [
        a + b + c,                          # singlet (k=0)
        a + b * omega + c * omega**2,       # doublet k=1
        a + b * omega**2 + c * omega,       # doublet k=2
    ]
    # Γ_χ diagonal eigenvalues: +1, -1, -1
    gamma_eigs = [1, -1, -1]

    # H Γ_χ = 0 in diagonal basis: each component = 0
    product = [sp.simplify(h * g) for h, g in zip(h_eigs, gamma_eigs)]
    print(f"  H eigenvalues in Z_3 Fourier basis: {h_eigs}")
    print(f"  Γ_χ eigenvalues in Z_3 Fourier basis: {gamma_eigs}")
    print(f"  H Γ_χ component-wise: {product}")

    # Three equations
    eqs = [
        a + b + c,                          # singlet eq
        a + b * omega + c * omega**2,       # doublet k=1 eq
        a + b * omega**2 + c * omega,       # doublet k=2 eq
    ]

    # Solve over R (require a, b, c real)
    sols = sp.solve(eqs, [a, b, c], dict=True)
    print(f"  Solutions over R: {sols}")

    # The system has unique solution a = b = c = 0
    sol_check = (
        len(sols) == 1
        and sols[0].get(a) == 0
        and sols[0].get(b) == 0
        and sols[0].get(c) == 0
    )
    check(
        "Z_3 Fourier system forces a = b = c = 0",
        sol_check,
        f"unique solution = {sols}",
        class_a=True,
    )

    # Verify the Z_3 character matrix is invertible
    F = sp.Matrix(
        [
            [1, 1, 1],
            [1, omega, omega**2],
            [1, omega**2, omega],
        ]
    )
    det_F = sp.simplify(F.det())
    check(
        "Z_3 character matrix F has non-zero determinant (Schur orthogonality)",
        det_F != 0,
        f"det(F) = {det_F}",
        class_a=True,
    )


def part6_explicit_examples() -> None:
    """Explicit examples: non-trivial circulants give non-zero {·, Γ_χ}."""
    print()
    print("=" * 78)
    print("PART 6: EXPLICIT EXAMPLES — NON-TRIVIAL CIRCULANTS DON'T ANTI-COMMUTE")
    print("=" * 78)

    R2 = R * R

    # Example A: H = R
    anticomm_R = R * Gamma_chi + Gamma_chi * R
    check(
        "{R, Γ_χ} ≠ 0  (R alone does not anti-commute)",
        sp.simplify(anticomm_R) != sp.zeros(3),
        f"{{R, Γ_χ}} = {anticomm_R.tolist()}",
        class_a=True,
    )

    # Example B: H = R - R² (anti-Hermitian in real basis)
    H_circ = R - R2
    anticomm_circ = H_circ * Gamma_chi + Gamma_chi * H_circ
    check(
        "{R - R², Γ_χ} ≠ 0  (anti-Hermitian circulant)",
        sp.simplify(anticomm_circ) != sp.zeros(3),
        f"{{R-R², Γ_χ}} = {anticomm_circ.tolist()}",
        class_a=True,
    )

    # Example C: H = (R + R²)/2 (real symmetric circulant)
    H_sym = (R + R2) / 2
    anticomm_sym = H_sym * Gamma_chi + Gamma_chi * H_sym
    print(f"  For H = (R+R²)/2 (real symmetric circulant):")
    print(f"    {{H, Γ_χ}} = {anticomm_sym.tolist()}")
    # This is NOT zero (and not all the same), confirming anti-commutation fails
    # for non-trivial Hermitian circulants
    check(
        "{(R+R²)/2, Γ_χ} ≠ 0  (Hermitian circulant)",
        sp.simplify(anticomm_sym) != sp.zeros(3),
        class_a=True,
    )


def part7_connes_lott_corollary() -> None:
    """Connes-Lott: off-diagonal Yukawa M forced to be Z_3-equivariant; with
    identification of γ = Γ_χ on 3-gen triplet, anti-commutation forces M = 0."""
    print()
    print("=" * 78)
    print("PART 7: CONNES-LOTT COROLLARY — Z_3-EQUIVARIANT YUKAWA FORCED TO ZERO")
    print("=" * 78)

    # M is a complex circulant (Z_3-equivariant 3x3): M = α I + β R + γ_M R²
    alpha, beta, gamma_M = sp.symbols("alpha beta gamma_M", complex=True)
    R2 = R * R
    M = alpha * I3 + beta * R + gamma_M * R2

    # M Z_3-equivariant by construction
    comm_MR = M * R - R * M
    check(
        "M = α I + β R + γ R² is Z_3-equivariant: [M, R] = 0",
        sp.simplify(comm_MR) == sp.zeros(3),
        class_a=True,
    )

    # Identification: {M, Γ_χ} = 0 (treating M as the 3-gen restriction of D)
    # Since M is complex circulant, {M, Γ_χ} = 2 M Γ_χ (same argument as part 4)
    anticomm_M = M * Gamma_chi + Gamma_chi * M
    twoMGamma = 2 * M * Gamma_chi
    check(
        "{M, Γ_χ} = 2 M Γ_χ  (M circulant ⟹ [M, Γ_χ] = 0)",
        sp.simplify(anticomm_M - twoMGamma) == sp.zeros(3),
        class_a=True,
    )

    # Solve {M, Γ_χ} = 0 ⟺ M Γ_χ = 0 over complex (α, β, γ)
    # Same Fourier analysis as part 5 but over C
    omega = sp.exp(2 * sp.pi * sp.I / 3)
    eqs = [
        alpha + beta + gamma_M,
        alpha + beta * omega + gamma_M * omega**2,
        alpha + beta * omega**2 + gamma_M * omega,
    ]
    sols = sp.solve(eqs, [alpha, beta, gamma_M], dict=True)
    print(f"  Solutions of M Γ_χ = 0 over C: {sols}")

    sol_check = (
        len(sols) == 1
        and sols[0].get(alpha) == 0
        and sols[0].get(beta) == 0
        and sols[0].get(gamma_M) == 0
    )
    check(
        "Connes-Lott Yukawa M forced to M = 0 by Z_3-equiv + γ↔Γ_χ identification",
        sol_check,
        f"unique solution = {sols}",
        class_a=True,
    )


def part8_disjoint_from_2dim_family() -> None:
    """Verify the 2-dim anti-commuting family H = (1/3)(1⊗h + h⊗1) with Σh=0
    intersects the circulant algebra only at H = 0."""
    print()
    print("=" * 78)
    print("PART 8: 2-DIM ANTI-COMMUTING FAMILY DISJOINT FROM CIRCULANTS")
    print("=" * 78)

    h1, h2, h3 = sp.symbols("h1 h2 h3", real=True)
    h = sp.Matrix([h1, h2, h3])
    ones = sp.Matrix([1, 1, 1])

    # H = (1/3)(1⊗h + h⊗1) means H_{ij} = (h_j + h_i) / 3
    H = sp.Matrix(3, 3, lambda i, j: (h[j] + h[i]) / 3)

    # Verify H is Hermitian (real symmetric)
    check(
        "H = (1/3)(1⊗h + h⊗1) is real symmetric",
        sp.simplify(H - H.T) == sp.zeros(3),
        class_a=True,
    )

    # H anti-commutes with Γ_χ when Σh = 0 (from retained L4 theorem)
    sum_h = h1 + h2 + h3
    anticomm = H * Gamma_chi + Gamma_chi * H
    # Substitute Σh = 0
    anticomm_with_constraint = anticomm.subs(h3, -h1 - h2)
    check(
        "{H, Γ_χ} = 0 when Σh = 0  (retained L4 theorem)",
        sp.simplify(anticomm_with_constraint) == sp.zeros(3),
        class_a=True,
    )

    # Z_3-equivariance: [H, R] = 0?
    comm_HR = H * R - R * H
    # Solve [H, R] = 0 for (h1, h2, h3) under Σh = 0
    comm_simplified = comm_HR.subs(h3, -h1 - h2)
    eqs_list = []
    for i in range(3):
        for j in range(3):
            entry = sp.simplify(comm_simplified[i, j])
            if entry != 0:
                eqs_list.append(entry)
    # eqs_list contains the non-trivial [H, R]_{ij} entries under Σh = 0
    if eqs_list:
        sols = sp.solve(eqs_list, [h1, h2], dict=True)
    else:
        sols = []

    print(f"  [H, R] = 0 equations under Σh = 0: {eqs_list}")
    print(f"  Solutions: {sols}")

    # Should force h1 = h2 = 0, hence h3 = 0, hence H = 0
    sol_check = (
        len(sols) == 1
        and sols[0].get(h1) == 0
        and sols[0].get(h2) == 0
    )
    check(
        "[H, R] = 0  +  Σh = 0  ⟹  h = 0  (anti-commuting family disjoint from circulants)",
        sol_check,
        f"unique solution = {sols}",
        class_a=True,
    )


# ============================================================================
# Main
# ============================================================================


def main() -> int:
    print("=" * 78)
    print("KOIDE Z_3-EQUIVARIANT ANTI-COMMUTING OPERATOR NO-GO RUNNER")
    print("=" * 78)
    print("Verifies docs/KOIDE_Z3_EQUIVARIANT_ANTICOMMUTING_NO_GO_NOTE_2026-05-16.md")
    print()

    part1_setup()
    part2_gamma_chi_is_circulant()
    part3_circulant_H_commutes_with_Gamma()
    part4_anticommutation_reduces_to_product()
    part5_fourier_basis_forces_zero()
    part6_explicit_examples()
    part7_connes_lott_corollary()
    part8_disjoint_from_2dim_family()

    print()
    print("=" * 78)
    print(f"SUMMARY: {PASS_COUNT} PASS / {FAIL_COUNT} FAIL")
    print(f"Class-A pattern hits: {CLASS_A_HITS}")
    print("=" * 78)
    print()
    print("VERDICT:")
    if FAIL_COUNT == 0:
        print("  ALGEBRAIC NO-GO VERIFIED — Z_3-equivariance + {·,Γ_χ}=0 forces H=0")
        print("  Connes-Lott corollary: off-diagonal Yukawa block forced to zero")
        print("  2-dim anti-commuting family disjoint from circulant algebra")
        print(f"  dominant_class: A ({CLASS_A_HITS} class-A pattern hits)")
        return 0
    else:
        print(f"  NO-GO NOT VERIFIED — {FAIL_COUNT} algebraic FAILs")
        return 1


if __name__ == "__main__":
    sys.exit(main())
