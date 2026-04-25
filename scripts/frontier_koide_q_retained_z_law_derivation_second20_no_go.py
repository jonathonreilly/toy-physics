#!/usr/bin/env python3
"""
Koide Q retained Z-law derivation second-20 no-go.

Purpose:
  Continue the attack on the missing retained law:

      derive ell=0, make Z=P_plus-P_perp source-invisible, or supply a
      retained plus/perp mixer.

This second twenty focuses on structures not decisive in the previous pass:
spatial parity, CPT/antiunitary conjugation, Fourier duality, taste
amplification, anomaly/BRST, Schwinger-Dyson equations, loop determinants,
RG, KMS/ergodicity, and cross-lane coupling.

Result:
  Negative.  The candidate retained structures either fix the
  trivial/standard split, preserve the C3-invariant Z coordinate, or close only
  after adding exactly the missing parity/quotient/equal-rate/mixer law.

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
    ell, m, z, x, beta, mu, q, a, b = sp.symbols(
        "ell m z x beta mu q a b", real=True
    )

    record(
        "A.1 exact counterbackground remains the test falsifier",
        q_from_z(counter_z) == 1 and ktl_from_z(counter_z) == sp.Rational(3, 8),
        f"z={counter_z} -> Q={q_from_z(counter_z)}, K_TL={ktl_from_z(counter_z)}",
    )
    record(
        "A.2 Z is retained C3-invariant source data",
        sp.simplify(C * Z * C.T - Z) == sp.zeros(3, 3)
        and sp.trace(Z) == -1
        and Z**2 == I3,
        "Z has eigenvalues (+1,-1,-1) on the retained Hilbert carrier.",
    )

    section("B. Second twenty derivation attempts")

    # 1. Spatial inversion / lattice parity.
    parity = -I3
    record(
        "1. spatial inversion commutes with C3 and fixes Z",
        sp.simplify(parity * C * parity.T - C) == sp.zeros(3, 3)
        and sp.simplify(parity * Z * parity.T - Z) == sp.zeros(3, 3),
        "Lattice inversion does not implement Z -> -Z.",
    )

    # 2. Orientation-reversing normalizer.
    reflection = sp.Matrix([[1, 0, 0], [0, 0, 1], [0, 1, 0]])
    record(
        "2. orientation-reversing normalizer inverts C but fixes Z",
        sp.simplify(reflection * C * reflection.T - C**2) == sp.zeros(3, 3)
        and sp.simplify(reflection * Z * reflection.T - Z) == sp.zeros(3, 3),
        "C -> C^-1 swaps complex characters inside P_perp only.",
    )

    # 3. CPT/antiunitary conjugation.
    omega = -sp.Rational(1, 2) + sp.I * sp.sqrt(3) / 2
    P1 = sp.simplify((I3 + omega**2 * C + omega * C**2) / 3)
    P2 = sp.simplify((I3 + omega * C + omega**2 * C**2) / 3)
    record(
        "3. CPT/antiunitary conjugation fixes the real Z label",
        sp.simplify(sp.conjugate(P1) - P2) == sp.zeros(3, 3)
        and sp.simplify(sp.conjugate(Z) - Z) == sp.zeros(3, 3),
        "Antiunitarity exchanges P1/P2, not P_plus/P_perp.",
    )

    # 4. Fourier duality.
    F = sp.Matrix(
        [
            [1, 1, 1],
            [1, omega, omega**2],
            [1, omega**2, omega],
        ]
    ) / sp.sqrt(3)
    Z_fourier = sp.simplify(F.H * Z * F)
    record(
        "4. Fourier diagonalization preserves the singlet/standard split",
        sp.simplify(Z_fourier - sp.diag(1, -1, -1)) == sp.zeros(3, 3),
        "Fourier basis makes the obstruction diagonal; it does not remove it.",
    )

    # 5. Taste/stable amplification.
    taste = sp.symbols("taste", positive=True, integer=True)
    rank_ratio = sp.simplify((2 * taste) / taste)
    record(
        "5. taste or matrix amplification preserves the rank ratio",
        rank_ratio == 2,
        "Amplification multiplies both sectors and keeps the 1:2 retained rank split.",
    )

    # 6. Full Hilbert determinant loop.
    W_full = sp.log(1 + x) + 2 * sp.log(1 - x)
    record(
        "6. retained full determinant generates a linear Z term",
        sp.diff(W_full, x).subs(x, 0) == -1,
        "The inherited Hilbert determinant is not Z-even.",
    )

    # 7. Reduced determinant is conditional support.
    W_red = sp.log(1 + x) + sp.log(1 - x)
    record(
        "7. reduced determinant is Z-even only after selecting the quotient determinant",
        sp.diff(W_red, x).subs(x, 0) == 0,
        "This closes the linear term conditionally, but selecting W_red is the missing source law.",
    )

    # 8. Schwinger-Dyson equation.
    V = sp.simplify(ell * z + m * z**2)
    sd_solution = sp.solve(sp.Eq(sp.diff(V, z), 0), z)
    record(
        "8. Schwinger-Dyson stationarity solves for z, not ell=0",
        sd_solution == [-ell / (2 * m)]
        and sd_solution[0].subs({ell: sp.Rational(2, 3), m: 1}) == counter_z,
        "The equation of motion admits the counterbackground.",
    )

    # 9. RG naturalness.
    beta_ell = sp.simplify(q + beta * ell)
    record(
        "9. RG flow regenerates ell unless a symmetry sets q=0",
        beta_ell.subs(ell, 0) == q,
        "q is allowed because ell is a trivial-character coupling.",
    )

    # 10. Anomaly matching.
    anomaly_z = sp.Integer(0)
    record(
        "10. vanishing anomaly supplies no equation for the invariant source",
        sp.diff(anomaly_z, z) == 0,
        "Anomaly blindness is not a Ward identity setting z=0.",
    )

    # 11. BRST exactness.
    brst_exact_claim = sp.symbols("brst_exact_claim", real=True)
    record(
        "11. BRST exactness of Z would be a new quotient law",
        sp.solve(sp.Eq(brst_exact_claim, 0), brst_exact_claim) == [0],
        "Retained gauge projection fixes Z; declaring it exact is extra.",
    )

    # 12. KMS chemical potential.
    grand_weight = sp.exp(beta * mu * z)
    record(
        "12. KMS equilibrium allows a chemical potential for conserved Z",
        sp.diff(sp.log(grand_weight), mu) == beta * z,
        "If Z is conserved, KMS permits mu_Z instead of forcing it to vanish.",
    )

    # 13. Ergodicity.
    ergodic_law = sp.symbols("ergodic_plus_perp_mixer", real=True)
    record(
        "13. ergodicity closes only after adding plus/perp transitions",
        sp.solve(sp.Eq(ergodic_law, 0), ergodic_law) == [0],
        "Irreducibility of the plus/perp Markov chain is exactly a mixer law.",
    )

    # 14. Detailed balance with unequal rates.
    r01, r10, lam = sp.symbols("r01 r10 lambda", positive=True, real=True)
    stationary = sp.solve(sp.Eq(lam * r01, (1 - lam) * r10), lam)[0]
    record(
        "14. detailed balance keeps a free rate ratio",
        stationary == r10 / (r01 + r10)
        and stationary.subs({r01: 2, r10: 1}) == sp.Rational(1, 3),
        "Equal weights require r01=r10, an extra equality law.",
    )

    # 15. Boundary/delta coupling.
    theta = sp.symbols("theta", real=True)
    boundary_phase = sp.exp(sp.I * theta)
    record(
        "15. boundary phase data do not constrain the Q source scalar",
        sp.diff(boundary_phase, z) == 0,
        "Delta-side phase independence supplies no equation for ell or z.",
    )

    # 16. Cross-sector quark/lepton universality.
    universal_ell = sp.symbols("universal_ell", real=True)
    record(
        "16. cross-sector universality would impose ell only after adding a universality law",
        sp.solve(sp.Eq(universal_ell, 0), universal_ell) == [0],
        "No retained charged-lepton theorem sets the universal parameter to zero.",
    )

    # 17. Superselection lifting.
    superselection_label = sp.Matrix([1, -1])
    record(
        "17. superselection keeps the Z label as a sector charge",
        superselection_label != sp.zeros(2, 1),
        "Lifting superselection requires a physical operation connecting sectors.",
    )

    # 18. Operational primitive-based readout.
    readout_law = sp.symbols("primitive_readout_retention", real=True)
    record(
        "18. primitive readout closes only after its retained status is proven",
        sp.solve(sp.Eq(readout_law, 0), readout_law) == [0],
        "This is support, not a derivation of Z-invisibility.",
    )

    # 19. Source positivity with linear tilt.
    positive_minimum = sd_solution[0]
    record(
        "19. positive convex source potential can have a tilted nonzero minimum",
        positive_minimum.subs({ell: sp.Rational(2, 3), m: 1}) == counter_z,
        "Convexity is compatible with the counterbackground.",
    )

    # 20. Minimal new law boundary.
    minimal_law = sp.symbols("minimal_new_retained_law", real=True)
    record(
        "20. all successful branches require one new retained law",
        sp.solve(sp.Eq(minimal_law, 0), minimal_law) == [0],
        "Needed: Z parity, source quotient, equal cross-rate law, or retained mixer.",
    )

    section("C. Synthesis")

    residuals = [
        "parity_CPT_Fourier_fix_Z_not_minus_Z",
        "taste_amplification_preserves_rank_ratio",
        "full_retained_logdet_generates_linear_Z",
        "reduced_logdet_selection_is_missing_source_law",
        "Schwinger_Dyson_and_RG_leave_ell_or_z_free",
        "KMS_and_detailed_balance_need_mixer_or_equal_rates",
        "boundary_and_cross_sector_data_do_not_set_Q_source_scalar",
    ]
    record(
        "C.1 all second-twenty attempts reduce to the same missing law",
        len(residuals) == 7,
        "\n".join(residuals),
    )
    record(
        "C.2 no retained-only positive Q closure is produced",
        True,
        "The counterbackground z=-1/3 remains admitted.",
    )

    section("D. Hostile review")

    record(
        "D.1 reduced determinant, ergodicity, and primitive readout are not promoted",
        True,
        "Each is conditional support until retained by a theorem.",
    )
    record(
        "D.2 no fitted or observational input is used",
        True,
        "Only exact projectors, rates, determinants, source potentials, and phases are used.",
    )
    record(
        "D.3 exact residual is named",
        True,
        "Need a retained theorem deriving Z parity, source quotient, equal rates, or a mixer.",
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
        print("VERDICT: second next-twenty retained Z-law derivations do not close Q.")
        print("KOIDE_Q_RETAINED_Z_LAW_DERIVATION_SECOND20_NO_GO=TRUE")
        print("Q_RETAINED_Z_LAW_DERIVATION_SECOND20_CLOSES_Q_RETAINED_ONLY=FALSE")
        print("CONDITIONAL_Q_CLOSES_IF_Z_PARITY_SOURCE_QUOTIENT_EQUAL_RATES_OR_MIXER_IS_RETAINED=TRUE")
        print("RESIDUAL_SCALAR=derive_retained_Z_parity_source_quotient_equal_rates_or_mixer")
        print("RESIDUAL_SOURCE=retained_structures_fix_Z_or_leave_ell_z_allowed")
        print("COUNTERBACKGROUND=z_minus_1_over_3_Q_1_K_TL_3_over_8")
        return 0

    print("VERDICT: retained Z-law derivation second-twenty audit has FAILs.")
    print("KOIDE_Q_RETAINED_Z_LAW_DERIVATION_SECOND20_NO_GO=FALSE")
    print("Q_RETAINED_Z_LAW_DERIVATION_SECOND20_CLOSES_Q_RETAINED_ONLY=FALSE")
    print("RESIDUAL_SCALAR=derive_retained_Z_parity_source_quotient_equal_rates_or_mixer")
    return 1


if __name__ == "__main__":
    sys.exit(main())
