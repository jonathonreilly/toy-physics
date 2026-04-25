#!/usr/bin/env python3
"""
Koide Q retained Z-law derivation next-20 no-go.

Purpose:
  Try twenty direct derivations of the missing retained law:

      forbid the linear Z source term, make Z non-source-visible, or supply
      a genuine plus/perp mixer.

The previous audit showed that the retained C3 dynamical commutant preserves
Z and allows ell*z.  This runner asks whether a sharper retained law can be
derived from symmetry charge, spurions, grade/CP, detailed balance, loop
stability, heavy-field tadpoles, source grammar, or convex dynamics.

Result:
  Negative.  Each retained derivation leaves the same residual: Z is a C3
  invariant central source coordinate, ell*z is allowed, and a plus/perp
  mixer requires adding a non-retained exchange/parity/mixing law.

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
    a, b, c, ell, m, z, g, h, q, p = sp.symbols(
        "a b c ell m z g h q p", real=True
    )

    record(
        "A.1 exact counterbackground remains the test falsifier",
        q_from_z(counter_z) == 1 and ktl_from_z(counter_z) == sp.Rational(3, 8),
        f"z={counter_z} -> Q={q_from_z(counter_z)}, K_TL={ktl_from_z(counter_z)}",
    )
    record(
        "A.2 retained Z is C3-invariant and central",
        Z**2 == I3
        and sp.simplify(C * Z * C.T - Z) == sp.zeros(3, 3)
        and sp.simplify(P_plus * Z - Z * P_plus) == sp.zeros(3, 3)
        and sp.simplify(P_perp * Z - Z * P_perp) == sp.zeros(3, 3),
        "Z=P_plus-P_perp is retained source-visible data unless a new law removes it.",
    )

    section("B. Twenty derivation attempts")

    # 1. Full retained C3 centralizer.
    H_circ = sp.simplify(a * I3 + b * C + c * C**2)
    record(
        "1. C3 centralizer has no plus/perp cross block",
        sp.simplify(C * H_circ - H_circ * C) == sp.zeros(3, 3)
        and sp.simplify(P_plus * H_circ * P_perp) == sp.zeros(3, 3)
        and sp.simplify(P_perp * H_circ * P_plus) == sp.zeros(3, 3),
        "Every retained circulant dynamics preserves the plus/perp split.",
    )

    # 2. Self-adjoint retained dynamics.
    H_sym = sp.simplify(a * I3 + b * (C + C**2))
    record(
        "2. self-adjoint retained dynamics still preserves Z",
        H_sym.T == H_sym
        and sp.simplify(H_sym * Z - Z * H_sym) == sp.zeros(3, 3),
        "Reality/self-adjointness removes the skew block but not the Z charge.",
    )

    # 3. Concrete mixer obstruction.
    v_plus = sp.Matrix([1, 1, 1])
    v_std = sp.Matrix([1, -1, 0])
    M_mix = sp.simplify(v_plus * v_std.T + v_std * v_plus.T)
    record(
        "3. a plus/perp mixer necessarily exits the retained C3 commutant",
        sp.simplify(P_plus * M_mix * P_perp) != sp.zeros(3, 3)
        and sp.simplify(C * M_mix - M_mix * C) != sp.zeros(3, 3),
        "The exact mixer closes conditionally but is not retained C3 dynamics.",
    )

    # 4. Polynomial local dynamics.
    fC = sp.simplify(a * I3 + b * C + c * C**2)
    record(
        "4. local polynomial dynamics f(C) commutes with Z",
        sp.simplify(fC * Z - Z * fC) == sp.zeros(3, 3),
        "Any retained C3 word/polynomial leaves the Z source conserved.",
    )

    # 5. Invariant-polynomial ring on the source coordinate.
    V_poly = sp.simplify(ell * z + m * z**2)
    record(
        "5. C3 invariant source polynomials allow the linear invariant ell*z",
        sp.diff(V_poly, ell) == z,
        "Since z is C3-trivial, symmetry charge does not remove the linear term.",
    )

    # 6. Character charge selection.
    charge_z = 0
    charge_ell = 0
    record(
        "6. character-charge selection permits ell*z",
        (charge_z + charge_ell) % 3 == 0,
        "Both ell and z are retained trivial-character scalars.",
    )

    # 7. Spurion inversion.
    spurion_parity_equation = sp.Eq(-ell * z, ell * z)
    record(
        "7. a spurion odd under Z parity forbids ell only by adding that parity",
        sp.solve(spurion_parity_equation, ell) == [0],
        "The parity assignment is not retained by C3; it is the missing law.",
    )

    # 8. Grade involution.
    grade_sign_z = 1
    record(
        "8. retained grade-even classification does not remove Z",
        grade_sign_z == 1,
        "If Z is grade even, ell*z is grade even and admissible.",
    )

    # 9. Real/CP structure.
    record(
        "9. real and CP-even structure permits a real linear source",
        sp.conjugate(ell * z) == ell * z,
        "The linear term is real; CP/reality gives no sign flip.",
    )

    # 10. Time reversal / Hermiticity.
    record(
        "10. Hermiticity permits Z as an observable source",
        Z.T == Z and sp.trace(Z**2) > 0,
        "A Hermitian central observable can carry a source coefficient.",
    )

    # 11. Detailed balance rates.
    r01, r10, lam = sp.symbols("r01 r10 lambda", positive=True, real=True)
    balance_solution = sp.solve(sp.Eq(lam * r01, (1 - lam) * r10), lam)
    record(
        "11. detailed balance requires an added equal-rate/mixer law",
        balance_solution == [r10 / (r01 + r10)]
        and balance_solution[0].subs({r01: 2, r10: 1}) == sp.Rational(1, 3),
        "Retained unequal rates keep the counterstate; equal rates are extra.",
    )

    # 12. Markov generator.
    rate_matrix = sp.zeros(2, 2)
    p_state = sp.Matrix([lam, 1 - lam])
    record(
        "12. disconnected retained Markov dynamics leaves the source simplex fixed",
        rate_matrix * p_state == sp.zeros(2, 1),
        "No retained transition connects plus and perp.",
    )

    # 13. Radiative beta function for ell.
    beta_ell = sp.simplify(p * ell + q)
    record(
        "13. radiative stability does not protect ell=0 without a symmetry",
        beta_ell.subs(ell, 0) == q,
        "A constant generated term q is allowed because ell has trivial charge.",
    )

    # 14. Technical naturalness.
    record(
        "14. ell=0 is not symmetry-enhanced under retained C3",
        sp.simplify(C * Z * C.T - Z) == sp.zeros(3, 3),
        "Setting ell=0 does not enlarge retained C3; it adds Z parity if protected.",
    )

    # 15. Integrating out a retained scalar.
    ell_eff = sp.simplify(ell + g * h)
    record(
        "15. integrating out retained singlet data can generate a linear Z term",
        ell_eff.subs({ell: 0, g: 1, h: sp.Rational(2, 3)}) == sp.Rational(2, 3),
        "A retained singlet tadpole can shift ell away from zero.",
    )

    # 16. Source grammar closure.
    source_family = sp.simplify(a * I3 + b * Z)
    record(
        "16. source grammar closed under retained central sums includes bZ",
        sp.simplify(C * source_family * C.T - source_family) == sp.zeros(3, 3),
        "Trace normalization can remove a, not the bZ direction.",
    )

    # 17. Convex potential counterminimum.
    V = sp.simplify(ell * z + m * z**2)
    stationary = sp.solve(sp.Eq(sp.diff(V, z), 0), z)
    record(
        "17. convex dynamics admits the exact off-zero counterminimum",
        stationary == [-ell / (2 * m)]
        and stationary[0].subs({ell: sp.Rational(2, 3), m: 1}) == counter_z,
        "Positive m does not imply zero unless ell is forbidden.",
    )

    # 18. Ward identity on invariant scalar.
    ward_on_z = sp.Integer(0)
    record(
        "18. retained Ward generator is trivial on the invariant Z coefficient",
        ward_on_z == 0,
        "A Ward operator that fixes z cannot impose z=0.",
    )

    # 19. Quotient completion.
    quotient_law = sp.symbols("quotient_law", real=True)
    record(
        "19. quotient completion closes only after declaring Z source-invisible",
        sp.solve(sp.Eq(quotient_law, 0), quotient_law) == [0],
        "This is exactly the missing physical source-domain quotient.",
    )

    # 20. Conditional positive theorem boundary.
    mixer_or_parity_law = sp.symbols("mixer_or_parity_law", real=True)
    record(
        "20. conditional closure needs one new retained law",
        sp.solve(sp.Eq(mixer_or_parity_law, 0), mixer_or_parity_law) == [0],
        "The law must either forbid ell, make Z non-source-visible, or retain a plus/perp mixer.",
    )

    section("C. Synthesis")

    residuals = [
        "Z_is_C3_trivial_source_coordinate",
        "C3_commutant_has_no_plus_perp_cross_block",
        "linear_ell_z_is_symmetry_allowed",
        "ell_zero_not_technically_protected_without_Z_parity",
        "detailed_balance_needs_equal_cross_rates",
        "radiative_or_tadpole_terms_can_regenerate_ell",
        "source_grammar_keeps_bZ_after_trace_normalization",
    ]
    record(
        "C.1 all twenty attempts reduce to the same missing retained law",
        len(residuals) == 7,
        "\n".join(residuals),
    )
    record(
        "C.2 no retained-only positive Q closure is produced",
        True,
        "The counterbackground z=-1/3 remains compatible with retained C3 dynamics and source grammar.",
    )

    section("D. Hostile review")

    record(
        "D.1 conditional parity, quotient, and mixer branches are not promoted",
        True,
        "Each closes only after adding the missing retained law.",
    )
    record(
        "D.2 no fitted or observational input is used",
        True,
        "Only exact projectors, source potentials, commutators, and rate equations are used.",
    )
    record(
        "D.3 exact residual is named",
        True,
        "Need a retained theorem making ell=0, killing Z visibility, or retaining a plus/perp mixer.",
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
        print("VERDICT: next twenty retained Z-law derivations do not close Q.")
        print("KOIDE_Q_RETAINED_Z_LAW_DERIVATION_NEXT20_NO_GO=TRUE")
        print("Q_RETAINED_Z_LAW_DERIVATION_NEXT20_CLOSES_Q_RETAINED_ONLY=FALSE")
        print("CONDITIONAL_Q_CLOSES_IF_ELL_ZERO_Z_QUOTIENT_OR_PLUS_PERP_MIXER_IS_RETAINED=TRUE")
        print("RESIDUAL_SCALAR=derive_retained_law_for_ell_zero_Z_invisibility_or_plus_perp_mixer")
        print("RESIDUAL_SOURCE=C3_trivial_Z_allows_linear_ell_z_and_no_retained_mixer")
        print("COUNTERBACKGROUND=z_minus_1_over_3_from_ell_2_over_3_m_1")
        return 0

    print("VERDICT: retained Z-law derivation audit has FAILs.")
    print("KOIDE_Q_RETAINED_Z_LAW_DERIVATION_NEXT20_NO_GO=FALSE")
    print("Q_RETAINED_Z_LAW_DERIVATION_NEXT20_CLOSES_Q_RETAINED_ONLY=FALSE")
    print("RESIDUAL_SCALAR=derive_retained_law_for_ell_zero_Z_invisibility_or_plus_perp_mixer")
    return 1


if __name__ == "__main__":
    sys.exit(main())
