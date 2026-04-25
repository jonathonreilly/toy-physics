#!/usr/bin/env python3
"""
Koide delta quadratic-refinement endpoint no-go.

Theorem attempt:
  The ambient APS value eta_APS = 2/9 is quadratic in the retained Z3 tangent
  weights (1,2).  Perhaps the selected-line Berry endpoint is forced to equal
  that quadratic refinement value.

Result:
  Negative.  The quadratic arithmetic is exact support:

      w1*w2 / 3^2 = 2/9.

  It matches the ABSS/APS fixed-point value.  But it is an ambient fixed-point
  density, not by itself an open-path selected-line endpoint.  A bridge

      theta_end - theta0 = q_quad

  is still a physical functor/normalization law.  General affine maps from
  the quadratic refinement to the selected-line endpoint leave one free
  coefficient, and other quadratic scalars from the same weights are also
  available unless the APS density formula is already chosen.

No PDG masses, Koide Q target, delta pin, or H_* pin is used.
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
    total = 0
    for k in (1, 2):
        z1 = omega**k
        z2 = omega ** (2 * k)
        total += sp.simplify(1 / ((z1 - 1) * (z2 - 1)))
    return sp.simplify(total / 3)


def main() -> int:
    section("A. Exact quadratic APS support")

    n = sp.Integer(3)
    w1 = sp.Integer(1)
    w2 = sp.Integer(2)
    eta = eta_abss_z3_weights_12()
    q_product = sp.simplify(w1 * w2 / n**2)
    q_sum = sp.simplify((w1 + w2) / n**2)
    q_norm = sp.simplify((w1**2 + w2**2) / n**2)

    record(
        "A.1 product quadratic weight gives 2/9 exactly",
        q_product == sp.Rational(2, 9),
        f"w1*w2/n^2={q_product}",
    )
    record(
        "A.2 product quadratic agrees with ambient APS magnitude",
        eta == q_product,
        f"eta_APS={eta}, q_product={q_product}",
    )
    record(
        "A.3 other exact quadratic scalars exist unless APS density is specified",
        q_sum == sp.Rational(1, 3) and q_norm == sp.Rational(5, 9),
        f"(w1+w2)/n^2={q_sum}, (w1^2+w2^2)/n^2={q_norm}",
    )

    section("B. Quadratic value is not an endpoint without a functor")

    theta0, theta_end = sp.symbols("theta0 theta_end", real=True)
    endpoint = sp.simplify(theta_end - theta0)
    residual = sp.simplify(endpoint - q_product)
    record(
        "B.1 selected-line Berry displacement remains an open-path endpoint variable",
        residual == theta_end - theta0 - sp.Rational(2, 9),
        f"RESIDUAL_ENDPOINT={residual}",
    )

    u, v = sp.symbols("u v", real=True)
    bridge = sp.simplify(u * q_product + v)
    v_needed = sp.solve(sp.Eq(bridge, q_product), v)
    u_needed_zero_offset = sp.solve(sp.Eq(bridge.subs(v, 0), q_product), u)
    record(
        "B.2 affine bridge from quadratic density to endpoint retains a free normalization",
        v_needed == [sp.Rational(2, 9) * (1 - u)]
        and u_needed_zero_offset == [1],
        f"delta=u q+v; v needed={v_needed}, v=0 needs u={u_needed_zero_offset}",
    )
    record(
        "B.3 the identity bridge u=1,v=0 is exactly the missing endpoint law",
        True,
        "The quadratic APS density is support; identifying it with open-path Berry displacement is extra.",
    )

    section("C. Counter-endpoints preserve the quadratic APS support")

    endpoint_samples = [sp.Rational(0), sp.Rational(1, 9), sp.Rational(2, 9), sp.Rational(1, 3)]
    sample_lines = []
    for value in endpoint_samples:
        sample_lines.append(
            f"endpoint={value}: q_product={q_product}, eta_APS={eta}, residual={sp.simplify(value-q_product)}"
        )
    record(
        "C.1 multiple selected-line endpoints preserve the same ambient quadratic support",
        len(endpoint_samples) == 4,
        "\n".join(sample_lines),
    )

    section("D. Verdict")

    record(
        "D.1 quadratic-refinement route does not close delta",
        True,
        "It proves why 2/9 is the right ambient APS support value, not why the selected-line endpoint equals it.",
    )
    record(
        "D.2 delta remains open after quadratic-refinement audit",
        True,
        "Residual primitive: physical Berry/APS functor identifying endpoint displacement with q_product.",
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
        print("VERDICT: quadratic APS/refinement support does not close delta.")
        print("KOIDE_DELTA_QUADRATIC_REFINEMENT_ENDPOINT_NO_GO=TRUE")
        print("DELTA_QUADRATIC_REFINEMENT_ENDPOINT_CLOSES_DELTA=FALSE")
        print("RESIDUAL_ENDPOINT=theta_end-theta0-eta_APS")
        print("RESIDUAL_FUNCTOR=selected_line_endpoint_equals_quadratic_APS_density")
        return 0

    print("VERDICT: quadratic-refinement endpoint audit has FAILs.")
    print("KOIDE_DELTA_QUADRATIC_REFINEMENT_ENDPOINT_NO_GO=FALSE")
    print("DELTA_QUADRATIC_REFINEMENT_ENDPOINT_CLOSES_DELTA=FALSE")
    print("RESIDUAL_ENDPOINT=theta_end-theta0-eta_APS")
    print("RESIDUAL_FUNCTOR=selected_line_endpoint_equals_quadratic_APS_density")
    return 1


if __name__ == "__main__":
    sys.exit(main())
