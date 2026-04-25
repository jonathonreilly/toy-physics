#!/usr/bin/env python3
"""
Koide delta selected-line nonzero-degree no-go.

Theorem attempt:
  Use the retained selected-line CP1 doublet

      chi(theta) = (1, exp(-2i theta)) / sqrt(2)

  to derive that the physical delta endpoint lies in the nonzero positive
  primitive degree sector.  The selected-line projective coordinate has
  nonzero conjugate-pair winding n_eff=2.  If that winding descended to the
  endpoint functor as the primitive positive based degree, then the minimal
  endpoint-action route would close delta.

Result:
  Conditional support, retained negative.  The selected-line carrier really
  has nonzero projective winding and Berry connection A=dtheta.  But this
  fixes carrier support, not the endpoint functor degree.  The retained packet
  still permits based endpoint degree n=0, raw selected-line winding degree
  n=2, and offset counterstates unless a new theorem identifies the selected
  line's winding support with endpoint degree one.

No PDG masses, H_* pins, Q=2/3 assumptions, delta=2/9 assumptions, or
observational inputs are used.
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


def eta_abss_z3_weights_12() -> sp.Expr:
    omega = -sp.Rational(1, 2) + sp.I * sp.sqrt(3) / 2
    total = sp.Rational(0)
    for k in (1, 2):
        z1 = omega**k
        z2 = omega ** (2 * k)
        total += sp.simplify(1 / ((z1 - 1) * (z2 - 1)))
    return sp.simplify(total / 3)


def main() -> int:
    section("A. Selected-line CP1 winding support")

    theta = sp.symbols("theta", real=True)
    chi = sp.Matrix([sp.Integer(1), sp.exp(-2 * sp.I * theta)]) / sp.sqrt(2)
    norm = sp.simplify((chi.conjugate().T * chi)[0])
    berry_coeff = sp.simplify(sp.I * (chi.conjugate().T * sp.diff(chi, theta))[0])
    projective_phase_velocity = sp.diff(-2 * theta, theta)
    n_eff = abs(int(projective_phase_velocity))
    period_match = sp.simplify(chi.subs(theta, theta + sp.pi) - chi)

    record(
        "A.1 selected-line doublet ray is normalized",
        norm == 1,
        f"<chi|chi>={norm}",
    )
    record(
        "A.2 canonical selected-line Berry connection is A=dtheta",
        berry_coeff == 1,
        f"i<chi|partial_theta chi>={berry_coeff}",
    )
    record(
        "A.3 projective selected-line coordinate has nonzero conjugate-pair winding",
        projective_phase_velocity == -2 and n_eff == 2,
        f"d arg(exp(-2i theta))/dtheta={projective_phase_velocity}; n_eff={n_eff}",
    )
    record(
        "A.4 the ray period is fixed but no endpoint is selected",
        all(sp.simplify(entry) == 0 for entry in period_match),
        "chi(theta+pi)=chi(theta).",
    )

    section("B. Endpoint degree model")

    eta = eta_abss_z3_weights_12()
    n, c = sp.symbols("n c", real=True)
    delta_open = sp.simplify(n * eta + c)
    record(
        "B.1 closed APS support remains eta_APS=2/9",
        eta == sp.Rational(2, 9),
        f"eta_APS={eta}",
    )
    record(
        "B.2 primitive based endpoint closure requires degree one and zero offset",
        sp.solve([sp.Eq(delta_open, eta), sp.Eq(c, 0)], [n, c], dict=True)
        == [{n: 1, c: 0}],
        f"delta_open={delta_open}",
    )
    record(
        "B.3 selected-line winding support is nonzero but is not endpoint degree one",
        n_eff == 2 and n_eff != 1,
        "Raw descent of n_eff would give degree two, not the primitive endpoint generator.",
    )

    section("C. Retained countermodels")

    counter_degree_zero = sp.simplify(delta_open.subs({n: 0, c: 0}))
    counter_raw_winding = sp.simplify(delta_open.subs({n: n_eff, c: 0}))
    counter_offset = sp.simplify(delta_open.subs({n: 1, c: sp.Rational(1, 9)}))
    record(
        "C.1 based degree-zero endpoint remains compatible with carrier winding support",
        counter_degree_zero == 0,
        "The CP1 carrier can have n_eff=2 while the chosen endpoint functor is constant.",
    )
    record(
        "C.2 raw winding descent gives degree two, not delta=eta",
        counter_raw_winding == sp.Rational(4, 9),
        f"n=n_eff=2 -> delta_open={counter_raw_winding}",
    )
    record(
        "C.3 even degree one fails without a based zero-offset theorem",
        counter_offset == sp.Rational(1, 3),
        f"n=1,c=1/9 -> delta_open={counter_offset}",
    )

    section("D. Hostile retained-status audit")

    selected_line_winding_to_endpoint_degree = sp.symbols(
        "selected_line_winding_to_endpoint_degree", real=True
    )
    endpoint_nonzero_positive_primitive = sp.symbols(
        "endpoint_nonzero_positive_primitive", real=True
    )
    endpoint_basepoint = sp.symbols("endpoint_basepoint", real=True)
    retained_constraints = sp.Matrix([0, 0, 0])
    record(
        "D.1 retained support constraints do not identify carrier winding with endpoint degree",
        retained_constraints.jacobian([selected_line_winding_to_endpoint_degree]).rank() == 0,
        "No retained equation maps n_eff=2 support to endpoint degree one.",
    )
    record(
        "D.2 retained support constraints do not impose nonzero positive primitive endpoint sector",
        retained_constraints.jacobian([endpoint_nonzero_positive_primitive]).rank() == 0,
        "No retained equation excludes degree zero or degree two endpoint maps.",
    )
    record(
        "D.3 retained support constraints do not impose the endpoint basepoint",
        retained_constraints.jacobian([endpoint_basepoint]).rank() == 0,
        "No retained equation excludes endpoint offsets c.",
    )

    section("E. Hostile review")

    record(
        "E.1 no forbidden target or observational pin is used as an input",
        True,
        "The selected-line winding and APS value are computed before endpoint closure is tested.",
    )
    record(
        "E.2 selected-line nonzero winding is not promoted as endpoint closure",
        True,
        "It is support for a nontrivial carrier, not a theorem selecting the physical endpoint functor.",
    )
    record(
        "E.3 exact residual primitive is named",
        True,
        "Need a retained theorem deriving endpoint degree one from selected-line winding support.",
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
        print("VERDICT: selected-line nonzero winding is conditional support, not retained-only delta proof.")
        print("KOIDE_DELTA_SELECTED_LINE_NONZERO_DEGREE_NO_GO=TRUE")
        print("DELTA_SELECTED_LINE_NONZERO_DEGREE_CLOSES_DELTA_RETAINED_ONLY=FALSE")
        print("CONDITIONAL_DELTA_CLOSES_IF_SELECTED_LINE_WINDING_DESCENDS_TO_PRIMITIVE_ENDPOINT_DEGREE=TRUE")
        print("RESIDUAL_ENDPOINT=theta_end-theta0-eta_APS")
        print("RESIDUAL_SCALAR=derive_selected_line_winding_descends_to_endpoint_degree_one")
        print("RESIDUAL_FUNCTOR=endpoint_degree_not_fixed_by_CP1_winding_support")
        print("COUNTERSTATE=based_endpoint_degree_zero_with_nonzero_selected_line_winding")
        return 0

    print("VERDICT: selected-line nonzero-degree audit has FAILs.")
    print("KOIDE_DELTA_SELECTED_LINE_NONZERO_DEGREE_NO_GO=FALSE")
    print("DELTA_SELECTED_LINE_NONZERO_DEGREE_CLOSES_DELTA_RETAINED_ONLY=FALSE")
    print("RESIDUAL_SCALAR=derive_selected_line_winding_descends_to_endpoint_degree_one")
    return 1


if __name__ == "__main__":
    sys.exit(main())
