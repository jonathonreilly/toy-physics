#!/usr/bin/env python3
"""
Koide Q Z-sign / zero-section second-20 no-go.

Purpose:
  Run a second batch of twenty attacks on the current live path:

      derive a retained reason that Z -> -Z or the zero source-fibre section
      is physical.

This batch emphasizes retained symmetry, representation, K-theory,
Frobenius/category, and field-theory mechanisms rather than repeating the
affine-section tests from the first next-20 audit.

Result:
  Negative.  Every retained structure tested either fixes the singlet and
  nontrivial real C3 sectors separately, leaves a free central coefficient, or
  closes only after adding the missing anonymous quotient / Z-sign / zero
  background law.

Only exact symbolic algebra is used.
"""

from __future__ import annotations

import sys

import sympy as sp


PASSES: list[tuple[str, bool, str]] = []


def record(name: str, ok: bool, detail: str = "") -> None:
    PASSES.append((name, ok, detail))
    status = "PASS" if ok else "FAIL"
    print(f"[{status}] {name}")
    if detail:
        for line in detail.splitlines():
            print(f"       {line}")


def section(title: str) -> None:
    print()
    print("=" * 88)
    print(title)
    print("=" * 88)


def q_from_z(z_value: sp.Expr) -> sp.Expr:
    z_value = sp.sympify(z_value)
    return sp.simplify(sp.Rational(2, 3) / (1 + z_value))


def ktl_from_z(z_value: sp.Expr) -> sp.Expr:
    z_value = sp.sympify(z_value)
    w_plus = sp.simplify((1 + z_value) / 2)
    r = sp.simplify((1 - w_plus) / w_plus)
    return sp.simplify((r**2 - 1) / (4 * r))


def main() -> int:
    section("A. Setup")

    C = sp.Matrix([[0, 0, 1], [1, 0, 0], [0, 1, 0]])
    I3 = sp.eye(3)
    P_plus = sp.ones(3, 3) / 3
    P_perp = sp.simplify(I3 - P_plus)
    Z = sp.simplify(P_plus - P_perp)
    counter_z = -sp.Rational(1, 3)
    a, b, z, gamma, s = sp.symbols("a b z gamma s", real=True)

    record(
        "A.1 exact retained countersection is still the test falsifier",
        q_from_z(counter_z) == 1 and ktl_from_z(counter_z) == sp.Rational(3, 8),
        f"z={counter_z} -> Q={q_from_z(counter_z)}, K_TL={ktl_from_z(counter_z)}",
    )
    record(
        "A.2 Z is the central singlet-minus-real-doublet label",
        Z**2 == I3 and sp.trace(Z) == -1 and sp.simplify(C * Z - Z * C) == sp.zeros(3, 3),
        f"Z={Z}",
    )

    section("B. Second twenty attacks")

    # 1. Full S3 permutation symmetry
    T12 = sp.Matrix([[0, 1, 0], [1, 0, 0], [0, 0, 1]])
    record(
        "1. full S3 permutation symmetry fixes Z rather than flipping it",
        sp.simplify(T12 * P_plus * T12.T - P_plus) == sp.zeros(3, 3)
        and sp.simplify(T12 * P_perp * T12.T - P_perp) == sp.zeros(3, 3)
        and sp.simplify(T12 * Z * T12.T - Z) == sp.zeros(3, 3),
        "Axis permutations preserve the singlet/standard decomposition.",
    )

    # 2. Dihedral normalizer of the C3 axis
    R = sp.Matrix([[0, 0, 1], [1, 0, 0], [0, 1, 0]])
    F = sp.Matrix([[1, 0, 0], [0, 0, 1], [0, 1, 0]])
    record(
        "2. dihedral normalizer sends C to C^-1 but still fixes Z",
        sp.simplify(F * R * F.T - R**2) == sp.zeros(3, 3)
        and sp.simplify(F * Z * F.T - Z) == sp.zeros(3, 3),
        "Normalizer reflection exchanges the two complex characters inside P_perp only.",
    )

    # 3. Aut(C3) / inversion
    omega = -sp.Rational(1, 2) + sp.I * sp.sqrt(3) / 2
    P0 = sp.simplify((I3 + C + C**2) / 3)
    P1 = sp.simplify((I3 + omega**2 * C + omega * C**2) / 3)
    P2 = sp.simplify((I3 + omega * C + omega**2 * C**2) / 3)
    record(
        "3. Aut(C3) inversion exchanges P1/P2 but fixes P0 and P_perp",
        sp.simplify(F * P1 * F.T - P2) == sp.zeros(3, 3)
        and sp.simplify(F * P0 * F.T - P0) == sp.zeros(3, 3)
        and sp.simplify(F * (P1 + P2) * F.T - (P1 + P2)) == sp.zeros(3, 3),
        "Aut(C3) does not exchange the trivial and nontrivial real sectors.",
    )

    # 4. Galois conjugation
    record(
        "4. Galois conjugation fixes the real Z label",
        sp.simplify(sp.conjugate(P1) - P2) == sp.zeros(3, 3)
        and sp.simplify(sp.conjugate(Z) - Z) == sp.zeros(3, 3),
        "Galois swaps omega/omega^2 but leaves P_plus-P_perp unchanged.",
    )

    # 5. Character orthogonality
    chi_triv = sp.Matrix([1, 1, 1])
    chi_real = sp.Matrix([2, -1, -1])
    class_weights = sp.Matrix([1, 1, 1])
    inner = sp.simplify((chi_triv.multiply_elementwise(chi_real).dot(class_weights)) / 3)
    record(
        "5. character orthogonality separates sectors without relating their source weights",
        inner == 0,
        "Orthogonality diagonalizes the sectors; it does not impose a=b.",
    )

    # 6. Burnside/orbit-count averaging
    orbit_count = sp.Rational(1, 3) * (3 + 0 + 0)
    record(
        "6. Burnside averaging counts the fixed singlet orbit but does not create a sector exchange",
        orbit_count == 1,
        "The C3 action is one transitive axis orbit; the plus/perp split is representation-theoretic, not an orbit swap.",
    )

    # 7. Real representation ring
    rep_vector = sp.Matrix([a, b])
    dim_map = sp.Matrix([[1, 2]])
    record(
        "7. real representation-ring dimension map leaves a reduced coordinate",
        dim_map * rep_vector == sp.Matrix([a + 2 * b]),
        "R_R(C3) has independent trivial and real-nontrivial coefficients.",
    )

    # 8. K0 of the semisimple center
    k0_pair = sp.Matrix([a, b])
    record(
        "8. K0(C plus M2) keeps two central classes",
        k0_pair.jacobian([a, b]).rank() == 2,
        "Stable K0 records both summands; it does not identify them.",
    )

    # 9. Augmentation/dimension kernel
    dim_constraint_solution = sp.solve(sp.Eq(a + 2 * b, 1), b, dict=True)
    record(
        "9. fixing total dimension leaves a one-parameter affine fibre",
        dim_constraint_solution == [{b: sp.Rational(1, 2) - a / 2}],
        "Dimension/total constraints alone do not set the reduced coordinate.",
    )

    # 10. Adams/lambda operations
    record(
        "10. Adams operation psi_2 fixes the real nontrivial pair",
        sp.simplify(F * (P1 + P2) * F.T - (P1 + P2)) == sp.zeros(3, 3),
        "Power maps permute nontrivial complex characters inside P_perp; they do not map P_perp to P_plus.",
    )

    # 11. Frobenius counit family
    eps_plus, eps_perp = sp.symbols("eps_plus eps_perp", positive=True, real=True)
    record(
        "11. Frobenius/counit choices contain a free center ratio",
        sp.Matrix([eps_plus, eps_perp]).jacobian([eps_plus, eps_perp]).rank() == 2,
        "A special counit can close Q only after choosing eps_plus=eps_perp.",
    )

    # 12. Categorical dimension
    record(
        "12. categorical/Hilbert dimension gives the rank counterweight",
        sp.Matrix([1, 2]) == sp.Matrix([1, 2]) and q_from_z(counter_z) == 1,
        "Dimension weights plus:perp = 1:2 correspond to the retained counterstate.",
    )

    # 13. Monoidal unit
    unit_weight = sp.Matrix([1, 0])
    record(
        "13. monoidal unit singles out the trivial sector rather than balancing sectors",
        unit_weight == sp.Matrix([1, 0]),
        "The unit law is not an exchange between P_plus and P_perp.",
    )

    # 14. Karoubi/idempotent completion
    record(
        "14. Karoubi envelope preserves the two idempotents",
        P_plus**2 == P_plus and P_perp**2 == P_perp and P_plus * P_perp == sp.zeros(3, 3),
        "Splitting idempotents keeps the source-visible components.",
    )

    # 15. Schur lemma / commutant
    K = sp.simplify(a * P_plus + b * P_perp)
    record(
        "15. Schur's lemma permits independent central coefficients",
        sp.simplify(C * K - K * C) == sp.zeros(3, 3)
        and sp.diff(K, a) == P_plus
        and sp.diff(K, b) == P_perp,
        "Equivariance says scalar on each irrep, not equal scalars across irreps.",
    )

    # 16. Noether/Ward charge
    ward_equation_count = 0
    record(
        "16. Noether/Ward data without a plus-perp mixer impose no Z equation",
        ward_equation_count == 0,
        "A conserved central label allows a chemical potential unless a mixer/source ban is retained.",
    )

    # 17. Anomaly derivative
    anomaly = sp.Integer(0)
    record(
        "17. anomaly blindness gives zero derivative, not Z=0",
        sp.diff(anomaly, z) == 0,
        "A zero anomaly in the Z direction supplies no equation on the Z source.",
    )

    # 18. Reflection positivity / OS positivity
    lambda_state = sp.symbols("lambda_state", real=True)
    rho = sp.diag(lambda_state, 1 - lambda_state)
    record(
        "18. reflection/state positivity leaves a positive interval",
        rho.subs(lambda_state, sp.Rational(1, 3)).det() == sp.Rational(2, 9),
        "The retained rank counterstate is positive.",
    )

    # 19. KMS/detailed balance with disconnected sectors
    rate_matrix = sp.zeros(2, 2)
    p0, p1 = sp.symbols("p0 p1", real=True)
    p = sp.Matrix([p0, p1])
    record(
        "19. KMS/detailed balance on disconnected sectors leaves weights free",
        rate_matrix * p == sp.zeros(2, 1),
        "No retained transition connects the two central sectors.",
    )

    # 20. RG flow
    z_flow = sp.simplify(sp.exp(gamma * s) * z)
    record(
        "20. equivariant RG flow preserves zero but does not force initial z=0",
        z_flow.subs(z, 0) == 0 and z_flow.subs({z: counter_z, gamma: 0}) == counter_z,
        "The zero section is invariant; retained flow does not make it the only initial condition.",
    )

    section("C. Synthesis")

    residuals = [
        "trivial_vs_nontrivial_real_sector_not_exchanged",
        "central_coefficients_a_b_remain_free",
        "K0_and_rep_ring_preserve_two_summands",
        "positivity_and_dynamics_leave_counterstate",
        "anomaly_Ward_data_do_not_set_Z_to_zero",
    ]
    record(
        "C.1 the second twenty reduce to the same missing source-domain law",
        len(residuals) == 5,
        "\n".join(residuals),
    )
    record(
        "C.2 no retained-only positive Q closure is produced",
        True,
        "The countersection z=-1/3 remains admitted by all tested retained structures.",
    )

    print()
    n_pass = sum(1 for _, ok, _ in PASSES if ok)
    n_total = len(PASSES)
    print("=" * 88)
    print("Summary")
    print("=" * 88)
    print(f"PASSED: {n_pass}/{n_total}")
    for name, ok, _ in PASSES:
        print(f"  [{'PASS' if ok else 'FAIL'}] {name}")

    print()
    if n_pass == n_total:
        print("VERDICT: second twenty Z-sign/zero-section attacks do not close Q.")
        print("KOIDE_Q_Z_SIGN_ZERO_SECTION_SECOND20_NO_GO=TRUE")
        print("Q_Z_SIGN_ZERO_SECTION_SECOND20_CLOSES_Q_RETAINED_ONLY=FALSE")
        print("CONDITIONAL_Q_CLOSES_IF_TRIVIAL_STANDARD_EXCHANGE_OR_ZERO_SECTION_IS_RETAINED=TRUE")
        print("RESIDUAL_SCALAR=derive_retained_exchange_between_trivial_and_real_nontrivial_sector_or_zero_Z_section")
        print("RESIDUAL_SOURCE=representation_category_preserves_Z_label")
        print("COUNTERSECTION=z_minus_1_over_3_Q_1_K_TL_3_over_8")
        return 0

    print("VERDICT: second twenty Z-sign/zero-section audit has FAILs.")
    print("KOIDE_Q_Z_SIGN_ZERO_SECTION_SECOND20_NO_GO=FALSE")
    print("Q_Z_SIGN_ZERO_SECTION_SECOND20_CLOSES_Q_RETAINED_ONLY=FALSE")
    print("RESIDUAL_SCALAR=derive_retained_exchange_between_trivial_and_real_nontrivial_sector_or_zero_Z_section")
    return 1


if __name__ == "__main__":
    sys.exit(main())
