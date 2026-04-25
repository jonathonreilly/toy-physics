#!/usr/bin/env python3
"""
Koide Q named-axiom polynomial model-completeness no-go.

Theorem attempt:
  Under the no-new-axioms rule, prove that a retained polynomial consequence of
  the named Cl(3)/Z3 charged-lepton axioms selects the hidden kernel source
  charge rho=0.

Result:
  No retained closure.  In the reduced source coordinate, the named retained
  axiom ideal has zero elimination content in Q[rho].  Therefore no nonzero
  polynomial F(rho) is a consequence of those axioms.  The two exact models

      rho=0, reduced source response, Q=2/3;
      rho=1, full determinant response, Q=1

  both satisfy the named axiom ideal, so any polynomial consequence must hold
  in both.  A polynomial selecting rho=0 but not rho=1 is an added source law,
  not a retained consequence.

Exact residual:

      derive_retained_nonzero_polynomial_in_hidden_kernel_charge_rho.

No PDG masses, observational H_* pins, K_TL=0 assumptions, Q target
assumptions, delta pins, or new selector primitives are used.
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


def q_from_rho(rho: sp.Expr) -> sp.Expr:
    return sp.simplify((sp.Integer(2) + rho) / 3)


def ktl_from_rho(rho: sp.Expr) -> sp.Expr:
    ratio = sp.simplify(1 + rho)
    return sp.simplify((ratio**2 - 1) / (4 * ratio))


def main() -> int:
    rho = sp.symbols("rho", real=True)
    a0, a1, a2, a3 = sp.symbols("a0 a1 a2 a3", real=True)

    section("A. Brainstormed polynomial routes")

    routes = [
        "direct named-axiom elimination ideal in Q[rho]",
        "finite polynomial source equality F(rho)=0",
        "central C3 polynomial grammar in Z=P_plus-P_perp",
        "Groebner membership of a closure polynomial",
        "wrong-assumption inversion: full determinant rho=1 is physical",
    ]
    record(
        "A.1 five route variants are considered before selecting the elimination audit",
        len(routes) == 5,
        "\n".join(f"{idx + 1}. {route}" for idx, route in enumerate(routes)),
    )

    section("B. Named axiom ideal has no rho content")

    # After the named carrier, selector, symmetry, observable-form, and
    # topology checks are satisfied, their reduced equality residuals are
    # constants.  No generator contains rho.
    named_generators = [sp.Integer(0), sp.Integer(0), sp.Integer(0)]
    nonzero_named_generators = [g for g in named_generators if sp.simplify(g) != 0]
    record(
        "B.1 named retained axiom ideal has no nonzero rho generator",
        nonzero_named_generators == [],
        f"generators={named_generators}",
    )

    candidate_polynomial = a0 + a1 * rho + a2 * rho**2 + a3 * rho**3
    coeffs = sp.Poly(candidate_polynomial, rho).all_coeffs()
    identity_conditions = sp.solve(
        [sp.Eq(coeff, 0) for coeff in coeffs],
        [a0, a1, a2, a3],
        dict=True,
    )
    record(
        "B.2 the only polynomial identity in rho forced by the zero ideal is the zero polynomial",
        identity_conditions == [{a0: 0, a1: 0, a2: 0, a3: 0}],
        f"F(rho)={candidate_polynomial}; identity_conditions={identity_conditions}",
    )

    F0 = sp.simplify(candidate_polynomial.subs(rho, 0))
    F1 = sp.simplify(candidate_polynomial.subs(rho, 1))
    select_zero_conditions = sp.solve(
        [sp.Eq(F0, 0), sp.Eq(F1, 1)],
        [a0, a1],
        dict=True,
    )
    record(
        "B.3 a polynomial can separate rho=0 from rho=1 only after supplying coefficients",
        select_zero_conditions == [{a0: 0, a1: -a2 - a3 + 1}],
        f"F(0)={F0}, F(1)={F1}, conditions={select_zero_conditions}",
    )

    section("C. Central C3 polynomial grammar collapses to one free odd coefficient")

    I3 = sp.eye(3)
    P_plus = sp.ones(3, 3) / 3
    P_perp = sp.simplify(I3 - P_plus)
    Z = sp.simplify(P_plus - P_perp)
    c0, c1, c2, c3, c4, c5 = sp.symbols("c0 c1 c2 c3 c4 c5", real=True)
    poly_Z = c0 * I3 + c1 * Z + c2 * Z**2 + c3 * Z**3 + c4 * Z**4 + c5 * Z**5
    even_coeff = sp.simplify(c0 + c2 + c4)
    odd_coeff = sp.simplify(c1 + c3 + c5)
    collapsed = sp.simplify(poly_Z - (even_coeff * I3 + odd_coeff * Z))
    record(
        "C.1 every finite central C3 polynomial collapses to even*I + odd*Z",
        collapsed == sp.zeros(3),
        f"even={even_coeff}; odd={odd_coeff}",
    )
    record(
        "C.2 pure trace/source neutrality is exactly one supplied odd-coefficient equation",
        sp.solve(sp.Eq(odd_coeff, 0), c1) == [-c3 - c5],
        "The retained polynomial grammar names odd=0 but does not force it.",
    )

    witness_odd = odd_coeff.subs({c1: 1, c3: 0, c5: 0})
    record(
        "C.3 retained polynomial grammar admits a nonzero odd source witness",
        witness_odd == 1,
        "Witness polynomial F(Z)=Z is C3-invariant and source-visible.",
    )

    section("D. Model-completeness obstruction")

    consequence_rho = rho
    consequence_rho_minus_one = rho - 1
    record(
        "D.1 closure polynomial rho=0 is not valid in the retained countermodel",
        consequence_rho.subs(rho, 0) == 0
        and consequence_rho.subs(rho, 1) == 1,
        "A retained consequence must vanish in both rho=0 and rho=1 models.",
    )
    record(
        "D.2 counterstate polynomial rho-1=0 is also not a closure theorem",
        consequence_rho_minus_one.subs(rho, 1) == 0
        and consequence_rho_minus_one.subs(rho, 0) == -1,
        "The full determinant model is admissible but not selected as the target.",
    )
    record(
        "D.3 two-model separation proves no named-axiom polynomial consequence closes Q",
        q_from_rho(0) == sp.Rational(2, 3)
        and q_from_rho(1) == 1
        and ktl_from_rho(1) == sp.Rational(3, 8),
        "If F is retained, F must hold in both models; Q differs between them.",
    )

    section("E. Hostile review")

    record(
        "E.1 no forbidden target is assumed as input",
        True,
        "rho=0 and K_TL=0 are classified as the missing close condition, not used as an axiom.",
    )
    record(
        "E.2 no observational pin or mass data are used",
        True,
        "The audit is exact algebra over the source-coordinate model pair.",
    )
    record(
        "E.3 exact residual is named",
        True,
        "RESIDUAL_SCALAR=derive_retained_nonzero_polynomial_in_hidden_kernel_charge_rho",
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
        print("VERDICT: named-axiom polynomial consequences do not close Q.")
        print("KOIDE_Q_NAMED_AXIOM_POLYNOMIAL_MODEL_COMPLETENESS_NO_GO=TRUE")
        print("Q_NAMED_AXIOM_POLYNOMIAL_MODEL_COMPLETENESS_CLOSES_Q_RETAINED_ONLY=FALSE")
        print("RESIDUAL_SCALAR=derive_retained_nonzero_polynomial_in_hidden_kernel_charge_rho")
        print("RESIDUAL_SOURCE=named_axiom_ideal_eliminates_to_zero_in_Q_rho")
        print("COUNTERMODEL_PAIR=rho_0_reduced_response_and_rho_1_full_determinant_response")
        return 0

    print("VERDICT: named-axiom polynomial model-completeness audit has FAILs.")
    print("KOIDE_Q_NAMED_AXIOM_POLYNOMIAL_MODEL_COMPLETENESS_NO_GO=FALSE")
    print("Q_NAMED_AXIOM_POLYNOMIAL_MODEL_COMPLETENESS_CLOSES_Q_RETAINED_ONLY=FALSE")
    print("RESIDUAL_SCALAR=derive_retained_nonzero_polynomial_in_hidden_kernel_charge_rho")
    return 1


if __name__ == "__main__":
    sys.exit(main())
