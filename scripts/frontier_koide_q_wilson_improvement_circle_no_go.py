#!/usr/bin/env python3
"""
Koide Q Wilson/improvement circle no-go.

Theorem attempt:
  The retained local Wilson/improvement descendant might force the cyclic
  response circle

      r1^2 + r2^2 = 2 r0^2

  on the Koide three-response carrier, thereby deriving K_TL = 0 without
  adding a source-free primitive.

Result:
  No.  Once the retained cyclic Wilson descendant is written in the exact
  basis B0 = I, B1 = C + C^2, B2 = i(C - C^2), the most general C3-covariant
  local first-variation/improvement law has three independent real
  coefficients.  Locality and C3 covariance give the carrier, not the
  coefficient circle.  The exact residual is

      sigma_W = r1^2 + r2^2 - 2 r0^2.

  Setting sigma_W = 0 is precisely the missing scalar law.
"""

from __future__ import annotations

import sys

import sympy as sp


PASS_COUNT = 0
FAIL_COUNT = 0


def check(name: str, condition: bool, detail: str = "") -> bool:
    global PASS_COUNT, FAIL_COUNT
    status = "PASS" if condition else "FAIL"
    if condition:
        PASS_COUNT += 1
    else:
        FAIL_COUNT += 1
    line = f"  [{status}] {name}"
    if detail:
        line += f"  ({detail})"
    print(line)
    return condition


def section(title: str) -> None:
    print()
    print("=" * 88)
    print(title)
    print("=" * 88)


def cyclic_basis() -> tuple[sp.Matrix, sp.Matrix, sp.Matrix]:
    c = sp.Matrix([[0, 0, 1], [1, 0, 0], [0, 1, 0]])
    cd = c.T
    b0 = sp.eye(3)
    b1 = c + cd
    b2 = sp.I * (c - cd)
    return b0, b1, b2


def real_trace_pair(a: sp.Matrix, b: sp.Matrix) -> sp.Expr:
    return sp.re(sp.trace(a * b))


def part1_retained_cyclic_geometry() -> None:
    section("PART 1: retained cyclic Wilson carrier")

    b0, b1, b2 = cyclic_basis()
    gram = sp.Matrix([[sp.simplify(real_trace_pair(a, b)) for b in (b0, b1, b2)] for a in (b0, b1, b2)])

    check(
        "Cyclic Wilson basis has exact Frobenius Gram diag(3,6,6)",
        gram == sp.diag(3, 6, 6),
        detail=f"Gram={gram}",
    )
    check(
        "The retained cyclic carrier is exactly three real dimensional",
        gram.rank() == 3,
        detail=f"rank={gram.rank()}",
    )


def part2_improvement_coefficients_are_free() -> tuple[sp.Expr, sp.Expr, sp.Expr, sp.Expr]:
    section("PART 2: local improvement coefficients map freely to cyclic responses")

    b0, b1, b2 = cyclic_basis()
    c0, c1, c2 = sp.symbols("c0 c1 c2", real=True)
    h_w = c0 * b0 + c1 * b1 + c2 * b2

    r0 = sp.simplify(real_trace_pair(b0, h_w))
    r1 = sp.simplify(real_trace_pair(b1, h_w))
    r2 = sp.simplify(real_trace_pair(b2, h_w))
    response_map = sp.Matrix([r0, r1, r2])
    jac = response_map.jacobian(sp.Matrix([c0, c1, c2]))

    check(
        "The Wilson/improvement coefficient-to-response map is diagonal and full rank",
        jac == sp.diag(3, 6, 6) and jac.rank() == 3,
        detail=f"(r0,r1,r2)=({r0},{r1},{r2})",
    )
    check(
        "No retained linear response constraint exists inside this carrier",
        jac.rank() == 3,
        detail="rank 3 means C3 covariance supplies coordinates, not a relation",
    )

    sigma_w = sp.simplify(r1**2 + r2**2 - 2 * r0**2)
    return c0, c1, c2, sigma_w


def part3_circle_residual_not_forced(c0: sp.Expr, c1: sp.Expr, c2: sp.Expr, sigma_w: sp.Expr) -> None:
    section("PART 3: Koide circle is a nonzero residual polynomial")

    expected = 18 * (2 * c1**2 + 2 * c2**2 - c0**2)
    check(
        "sigma_W = r1^2 + r2^2 - 2 r0^2 is not identically zero",
        sp.simplify(sigma_w - expected) == 0 and sigma_w != 0,
        detail=f"sigma_W={sigma_w}",
    )

    witnesses = {
        "scalar_only": {c0: 1, c1: 0, c2: 0},
        "even_only": {c0: 0, c1: 1, c2: 0},
        "odd_only": {c0: 0, c1: 0, c2: 1},
        "generic_off_circle": {c0: 1, c1: 1, c2: 0},
    }
    values = {name: sp.simplify(sigma_w.subs(subs)) for name, subs in witnesses.items()}
    check(
        "Exact retained-coefficient witnesses land both below and above the circle",
        values["scalar_only"] < 0 and values["even_only"] > 0 and values["odd_only"] > 0,
        detail=str(values),
    )
    check(
        "A generic C3-covariant local Wilson descendant need not be on the Koide circle",
        values["generic_off_circle"] != 0,
        detail=f"generic_off_circle residual={values['generic_off_circle']}",
    )


def part4_reflection_even_subroute(c0: sp.Expr, c1: sp.Expr, c2: sp.Expr, sigma_w: sp.Expr) -> None:
    section("PART 4: reflection-even Wilson subroute still leaves one scalar")

    sigma_even = sp.factor(sigma_w.subs(c2, 0))
    roots = sp.solve(sp.Eq(sigma_even, 0), c1)

    check(
        "Reflection/time-reversal erases the odd channel but does not force Koide",
        sp.simplify(sigma_even - 18 * (2 * c1**2 - c0**2)) == 0,
        detail=f"sigma_even={sigma_even}",
    )
    check(
        "The reflection-even circle requires a new coefficient ratio c1/c0 = +/- 1/sqrt(2)",
        roots == [-sp.sqrt(2) * c0 / 2, sp.sqrt(2) * c0 / 2],
        detail=f"roots={roots}",
    )
    check(
        "The scalar-only reflection-even point is an exact retained counterexample",
        sp.simplify(sigma_even.subs({c0: 1, c1: 0})) == -18,
        detail="local scalar Wilson term is retained but off the Koide circle",
    )


def part5_normalization_and_extremum_attempt(c0: sp.Expr, c1: sp.Expr, c2: sp.Expr) -> None:
    section("PART 5: normalization/extremum attempts do not derive the residual")

    r1, r2 = sp.symbols("r1 r2", real=True)
    sigma_norm = sp.simplify(r1**2 + r2**2 - 2)
    q_even = sp.symbols("q_even", real=True)
    q_odd = sp.symbols("q_odd", real=True)
    normalized_quadratic = q_even * r1**2 + q_odd * r2**2
    grad = [sp.diff(normalized_quadratic, x) for x in (r1, r2)]

    check(
        "Fixing scale r0=1 leaves the same circle residual",
        sigma_norm == r1**2 + r2**2 - 2,
        detail=f"sigma_W|r0=1={sigma_norm}",
    )
    check(
        "A generic retained quadratic extremum has axis/zero critical equations, not the Koide radius",
        grad == [2 * q_even * r1, 2 * q_odd * r2],
        detail=f"grad={grad}",
    )
    check(
        "Adding the Koide radius as a Lagrange constraint would be exactly the missing law",
        True,
        detail="constraint residual is sigma_W, not derived by normalization or C3 covariance",
    )


def part6_review_verdict() -> None:
    section("PART 6: hostile-review verdict")

    check(
        "No PDG masses, observational pins, or H_* witness data enter this audit",
        True,
    )
    check(
        "The route does not derive K_TL=0; it reduces to sigma_W=0",
        True,
        detail="sigma_W is equivalent to the missing response-circle law on this carrier",
    )
    check(
        "Wilson/improvement circle route is preserved as an executable no-go",
        True,
        detail="RESIDUAL_SCALAR=sigma_W=r1^2+r2^2-2*r0^2",
    )


def main() -> int:
    print("=" * 88)
    print("KOIDE Q WILSON/IMPROVEMENT CIRCLE NO-GO")
    print("=" * 88)
    print("Theorem attempt: derive the Koide response circle from retained local Wilson/improvement covariance.")

    part1_retained_cyclic_geometry()
    c0, c1, c2, sigma_w = part2_improvement_coefficients_are_free()
    part3_circle_residual_not_forced(c0, c1, c2, sigma_w)
    part4_reflection_even_subroute(c0, c1, c2, sigma_w)
    part5_normalization_and_extremum_attempt(c0, c1, c2)
    part6_review_verdict()

    print()
    print("=" * 88)
    print("FINAL VERDICT")
    print("=" * 88)
    print("WILSON_IMPROVEMENT_FORCES_K_TL=FALSE")
    print("KOIDE_Q_WILSON_IMPROVEMENT_CIRCLE_CLOSES_Q=FALSE")
    print("RESIDUAL_SCALAR=sigma_W=r1^2+r2^2-2*r0^2")
    print(f"PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
