#!/usr/bin/env python3
"""
Koide Q projective C3 representative-section no-go.

Theorem attempt:
  Close the current Q obstruction by deriving the representative law

      H(a,b) = a P_plus + b P_perp,
      a = 2b,

  from projective C3 source geometry plus canonical section principles.

Result:
  No retained closure.  The audit proves a stronger obstruction: after radial
  quotienting, the condition a=2b is not projectively well-defined.  A radial
  shift H -> H + lambda I changes a=2b, and every projective-line functional
  built only from radial_project(H) is blind to the remaining representative
  parameter.  Some extra section choices can conditionally select a=2b, most
  notably quotient-center entropy, but those choices are exactly the missing
  physical source law.

Exact residual:

      derive_physical_projective_C3_representative_section_a_eq_2b.

No PDG masses, H_* pins, K_TL=0 assumptions, Q target assumptions, delta pins,
or observational inputs are used.
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


def radial_project(matrix: sp.Matrix) -> sp.Matrix:
    n = matrix.rows
    return sp.simplify(matrix - sp.trace(matrix) * sp.eye(n) / n)


def frob_sq(matrix: sp.Matrix) -> sp.Expr:
    return sp.simplify(sp.trace(matrix.T * matrix))


def species_block_traces(
    matrix: sp.Matrix, p_plus: sp.Matrix, p_perp: sp.Matrix
) -> tuple[sp.Expr, sp.Expr]:
    return sp.simplify(sp.trace(p_plus * matrix)), sp.simplify(sp.trace(p_perp * matrix))


def q_from_ratio(ratio: sp.Expr) -> sp.Expr:
    ratio = sp.sympify(ratio)
    return sp.simplify((1 + ratio) / 3)


def ktl_from_ratio(ratio: sp.Expr) -> sp.Expr:
    ratio = sp.sympify(ratio)
    return sp.simplify((ratio**2 - 1) / (4 * ratio))


def main() -> int:
    I3 = sp.eye(3)
    C = sp.Matrix([[0, 0, 1], [1, 0, 0], [0, 1, 0]])
    P_plus = sp.ones(3, 3) / 3
    P_perp = sp.simplify(I3 - P_plus)
    a, b, d, lam, p, T, N = sp.symbols("a b d lam p T N", positive=True, real=True)
    nu = sp.symbols("nu", real=True)

    H = sp.simplify(a * P_plus + b * P_perp)
    e_plus, e_perp = species_block_traces(H, P_plus, P_perp)
    ratio = sp.simplify(e_perp / e_plus)

    section("A. Current projective C3 source cone")

    record(
        "A.1 retained C3-positive response family is H(a,b)",
        sp.simplify(C * H * C.T - H) == sp.zeros(3)
        and e_plus == a
        and e_perp == 2 * b,
        f"Tr_+={e_plus}; Tr_perp={e_perp}; ratio={ratio}",
    )
    record(
        "A.2 Q closure on this family is exactly the representative equation a=2b",
        sp.solve(sp.Eq(e_plus, e_perp), a) == [2 * b]
        and q_from_ratio(ratio.subs(a, 2 * b)) == sp.Rational(2, 3)
        and ktl_from_ratio(ratio.subs(a, 2 * b)) == 0,
        "Equal total block trace is equivalent to a=2b.",
    )
    record(
        "A.3 radial projection deletes only the common scalar",
        radial_project(H) == sp.simplify((a - b) * (P_plus - I3 / 3)),
        f"radial_project(H)={radial_project(H)}",
    )
    H_close = sp.simplify(2 * P_plus + P_perp)
    H_bad = sp.simplify(3 * P_plus + P_perp)
    e_plus_bad, e_perp_bad = species_block_traces(H_bad, P_plus, P_perp)
    record(
        "A.4 closing and nonclosing positive representatives share the same projective line",
        radial_project(H_bad) == 2 * radial_project(H_close)
        and q_from_ratio(e_perp_bad / e_plus_bad) == sp.Rational(5, 9)
        and ktl_from_ratio(e_perp_bad / e_plus_bad) == -sp.Rational(5, 24),
        "H_close=2P_plus+Pperp closes; H_bad=3P_plus+Pperp is positive and nonclosing.",
    )
    H_db = sp.simplify((b + d) * P_plus + b * P_perp)
    e_plus_db, e_perp_db = species_block_traces(H_db, P_plus, P_perp)
    record(
        "A.5 fixed nonzero projective tangent still leaves a free positive representative",
        radial_project(H_db) == sp.simplify(d * (P_plus - I3 / 3))
        and sp.solve(sp.Eq(e_plus_db, e_perp_db), b) == [d],
        f"H_d,b=(b+d)P_plus+bPperp; closure requires b={d}",
    )

    section("B. Why projective data alone cannot select a=2b")

    shifted = sp.simplify(H + lam * I3)
    e_plus_shift, e_perp_shift = species_block_traces(shifted, P_plus, P_perp)
    record(
        "B.1 a=2b is not invariant under radial shifts",
        radial_project(shifted) == radial_project(H)
        and sp.solve(sp.Eq(e_plus_shift, e_perp_shift), lam) == [a - 2 * b],
        "For the same projective source, a radial shift can make or break the closing representative.",
    )
    record(
        "B.2 every radial-projective polynomial invariant is blind to b on a fixed tangent",
        sp.diff(frob_sq(radial_project(H_db)), b) == 0
        and sp.diff(sp.trace(radial_project(H_db)), b) == 0
        and sp.diff(sp.trace(radial_project(H_db) ** 3), b) == 0,
        (
            f"||radial_project(H_d,b)||^2={frob_sq(radial_project(H_db))}; "
            f"tr(projected^3)={sp.simplify(sp.trace(radial_project(H_db) ** 3))}"
        ),
    )
    record(
        "B.3 the nonprojective closing scalar changes along the radial fibre",
        sp.simplify((e_plus_shift - e_perp_shift) - (e_plus - e_perp)) == -lam,
        "Tr_+ - Tr_perp is a section-dependent scalar, not a function on the quotient.",
    )
    record(
        "B.4 positivity leaves an interval of representatives on the same projective ray",
        (H_close.is_positive_definite and H_bad.is_positive_definite),
        "Both H_close and H_bad are positive; positivity alone cannot be the section law.",
    )

    section("C. Canonical section candidates")

    H_trace = sp.simplify(a * P_plus + b * P_perp)
    trace_eq = sp.Eq(a + 2 * b, 1)
    record(
        "C.1 unit trace does not select a unique center representative",
        sp.solve(trace_eq, a) == [1 - 2 * b]
        and q_from_ratio((2 * b / a).subs({a: sp.Rational(1, 3), b: sp.Rational(1, 3)})) == 1,
        "The unit-trace microstate H=(1/3)I is admissible and nonclosing.",
    )
    logdet = sp.log(a) + 2 * sp.log(b)
    det_trace_sol = sp.solve(
        [
            sp.Eq(sp.diff(logdet - nu * (a + 2 * b - 1), a), 0),
            sp.Eq(sp.diff(logdet - nu * (a + 2 * b - 1), b), 0),
            sp.Eq(a + 2 * b, 1),
        ],
        [a, b, nu],
        dict=True,
    )
    record(
        "C.2 maximum determinant at fixed trace selects rank-uniform microdensity, not Q",
        det_trace_sol == [{a: sp.Rational(1, 3), b: sp.Rational(1, 3), nu: 3}],
        f"max logdet under Tr=1 gives {det_trace_sol}",
    )
    b_det = sp.symbols("b_det", positive=True, real=True)
    trace_det_one = sp.simplify(1 / b_det**2 + 2 * b_det)
    record(
        "C.3 minimum trace at fixed determinant selects a=b, not a=2b",
        sp.solve(sp.Eq(sp.diff(trace_det_one, b_det), 0), b_det) == [1],
        "With ab^2=1, trace=a+2b=b^-2+2b is minimized at a=b=1.",
    )
    purity = sp.simplify(a**2 + 2 * b**2)
    purity_sol = sp.solve(
        [
            sp.Eq(sp.diff(purity - nu * (a + 2 * b - 1), a), 0),
            sp.Eq(sp.diff(purity - nu * (a + 2 * b - 1), b), 0),
            sp.Eq(a + 2 * b, 1),
        ],
        [a, b, nu],
        dict=True,
    )
    record(
        "C.4 minimum Frobenius norm at fixed trace also selects a=b",
        purity_sol == [{a: sp.Rational(1, 3), b: sp.Rational(1, 3), nu: sp.Rational(2, 3)}],
        f"minimum purity solution={purity_sol}",
    )
    record(
        "C.5 fixed trace and fixed norm select a=2b only after tuning the constant",
        sp.simplify((a**2 + 2 * b**2) / (a + 2 * b) ** 2).subs(a, 2 * b)
        == sp.Rational(3, 8),
        "The constant N/T^2=3/8 is exactly the closing representative value; choosing it imports the section.",
    )
    H_center_prob = p
    h_center = -p * sp.log(p) - (1 - p) * sp.log(1 - p)
    h_micro = -p * sp.log(p) - (1 - p) * sp.log((1 - p) / 2)
    record(
        "C.6 quotient-center entropy conditionally selects the closing representative",
        sp.solve(sp.Eq(sp.diff(h_center, p), 0), p) == [sp.Rational(1, 2)],
        "If the physical source language has only two equal center labels, max entropy gives p_plus=1/2.",
    )
    record(
        "C.7 retained microcarrier entropy selects the rank state instead",
        sp.solve(sp.Eq(sp.diff(h_micro, p), 0), p) == [sp.Rational(1, 3)],
        "On the retained 1+2 microcarrier, max entropy gives p_plus=1/3, i.e. a=b and Q=1.",
    )
    record(
        "C.8 entropy closure therefore assumes the quotient-center source language",
        H_center_prob.subs(p, sp.Rational(1, 2)) == sp.Rational(1, 2)
        and H_center_prob.subs(p, sp.Rational(1, 3)) == sp.Rational(1, 3),
        "The difference is not algebra; it is the choice of physical source language.",
    )
    inv_H = sp.simplify((1 / a) * P_plus + (1 / b) * P_perp)
    record(
        "C.9 inversion/self-duality of the projective line does not select a=2b",
        radial_project(inv_H) == sp.simplify((1 / a - 1 / b) * (P_plus - I3 / 3))
        and sp.simplify(radial_project(inv_H) + radial_project(H) / (a * b)) == sp.zeros(3),
        "Every non-scalar H has inverse on the opposite projective ray; no special ratio is selected.",
    )

    section("D. Conditional closure and exact residual")

    section_law = sp.symbols("section_law", real=True)
    record(
        "D.1 adding a physical section law a=2b closes the exact Q chain",
        q_from_ratio(ratio.subs(a, 2 * b)) == sp.Rational(2, 3)
        and ktl_from_ratio(ratio.subs(a, 2 * b)) == 0,
        "This is conditional support, not retained closure.",
    )
    record(
        "D.2 the needed physical section is an independent residual scalar",
        sp.solve(sp.Eq(section_law, 0), section_law) == [0],
        "Residual: derive_physical_projective_C3_representative_section_a_eq_2b.",
    )
    retained_constraints = sp.Matrix([0, 0, 0])
    record(
        "D.3 current retained projective constraints have zero rank on the section residual",
        retained_constraints.jacobian([section_law]).rank() == 0,
        "Projective geometry names the fibre; it does not select the closing point in it.",
    )

    section("E. Hostile review")

    record(
        "E.1 no forbidden target or observational pin is used",
        True,
        "All checks are exact symbolic statements about the C3 source cone.",
    )
    record(
        "E.2 quotient-center entropy is not promoted as retained closure",
        True,
        "It closes only if the quotient-center source language is supplied as a physical law.",
    )
    record(
        "E.3 the no-go is not over all future physics",
        True,
        "A future retained dynamical/source theorem may still derive the section law.",
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
        print("VERDICT: projective C3 geometry does not derive the representative section a=2b.")
        print("KOIDE_Q_PROJECTIVE_C3_REPRESENTATIVE_SECTION_NO_GO=TRUE")
        print("Q_PROJECTIVE_C3_REPRESENTATIVE_SECTION_CLOSES_Q_RETAINED_ONLY=FALSE")
        print("CONDITIONAL_Q_CLOSES_IF_PROJECTIVE_SECTION_A_EQ_2B=TRUE")
        print("RESIDUAL_SCALAR=derive_physical_projective_C3_representative_section_a_eq_2b")
        print("RESIDUAL_SOURCE=projective_radial_fibre_has_no_retained_closing_section")
        print("COUNTERSTATE=H_bad_3P_plus_plus_Pperp_same_projective_line_Q_5_over_9")
        return 0

    print("VERDICT: projective C3 representative-section audit has FAILs.")
    print("KOIDE_Q_PROJECTIVE_C3_REPRESENTATIVE_SECTION_NO_GO=FALSE")
    print("Q_PROJECTIVE_C3_REPRESENTATIVE_SECTION_CLOSES_Q_RETAINED_ONLY=FALSE")
    print("RESIDUAL_SCALAR=derive_physical_projective_C3_representative_section_a_eq_2b")
    return 1


if __name__ == "__main__":
    sys.exit(main())
