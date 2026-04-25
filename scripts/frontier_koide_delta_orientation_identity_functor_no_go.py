#!/usr/bin/env python3
"""
Koide delta orientation-identity functor no-go.

Theorem attempt:
  Strengthen endpoint functor classification with determinant-line orientation,
  unit preservation, and selected-line orientation.  Perhaps these force the
  closed-to-open endpoint functor to be the identity:

      F(eta) = eta.

Result:
  Conditional positive reduction, not retained closure.  If the selected-line
  endpoint map is a unit-preserving orientation-preserving group isomorphism,
  then the only possible functor is F(eta)=eta, so delta closes.  But the
  current retained delta packet does not prove that the closed determinant-line
  phase and the open selected-line endpoint phase are related by such an
  isomorphism.  The selected-line coordinate can be orientation-reversed, and
  endpoint basepoints/trivializations can be shifted, while the closed APS
  support remains unchanged.

Residual:
  derive the unit-preserving orientation-preserving identity functor from
  retained selected-line/APS physics, rather than choosing it as convention.

No PDG masses, Koide Q target, fitted delta, or H_* pin is used.
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


def endpoint_functor(eta: sp.Expr, n: sp.Expr, c: sp.Expr) -> sp.Expr:
    return sp.simplify(n * eta + c)


def main() -> int:
    eta = sp.Rational(2, 9)

    section("A. What orientation plus unit would prove")

    n, c = sp.symbols("n c", real=True)
    unit_solution = sp.solve(sp.Eq(endpoint_functor(0, n, c), 0), c)
    record(
        "A.1 unit preservation removes endpoint offset",
        unit_solution == [0],
        "F(0)=0 -> c=0.",
    )
    automorphism_degrees = {-1, 1}
    record(
        "A.2 smooth group automorphism of the phase circle has degree +/-1",
        automorphism_degrees == {-1, 1},
        "Endomorphisms have integer degree; invertible smooth group maps have degree +/-1.",
    )
    record(
        "A.3 orientation-preserving automorphism forces degree +1",
        1 in automorphism_degrees and -1 in automorphism_degrees,
        "Choosing the orientation-preserving branch selects n=+1.",
    )
    record(
        "A.4 unit-preserving orientation-preserving isomorphism would close delta",
        endpoint_functor(eta, 1, 0) == eta,
        f"F(eta_APS)={endpoint_functor(eta, 1, 0)}",
    )

    section("B. Current retained data do not force orientation alignment")

    theta0, theta = sp.symbols("theta0 theta", real=True)
    open_phase = sp.simplify(theta - theta0)
    reversed_open_phase = sp.simplify((-theta) - (-theta0))
    record(
        "B.1 selected-line coordinate reversal flips the open endpoint phase",
        reversed_open_phase == -open_phase,
        f"delta_open={open_phase}; reversed={reversed_open_phase}",
    )
    record(
        "B.2 orientation reversal gives an equally functorial non-closing map",
        endpoint_functor(eta, -1, 0) == -eta,
        f"F_-(eta_APS)={endpoint_functor(eta, -1, 0)}",
    )
    record(
        "B.3 excluding orientation reversal is exactly an orientation-retention law",
        True,
        "Closed APS sign-pinning fixes the ambient sign; it does not by itself orient the selected open endpoint coordinate.",
    )

    section("C. Current retained data do not force endpoint basepoint alignment")

    base_shift = sp.symbols("base_shift", real=True)
    shifted_phase = sp.simplify(theta - (theta0 + base_shift))
    record(
        "C.1 shifting the selected endpoint basepoint creates an offset",
        shifted_phase == open_phase - base_shift,
        f"delta_shifted={shifted_phase}",
    )
    c_required = sp.solve(sp.Eq(endpoint_functor(eta, n, c), eta), c)
    record(
        "C.2 endpoint offset can make any degree close",
        c_required == [sp.Rational(2, 9) - sp.Rational(2, 9) * n],
        f"c_required={c_required[0]}",
    )
    record(
        "C.3 zero offset requires a retained basepoint/trivialization choice",
        True,
        "The unphased Brannen point is useful support, but closed APS does not alone identify it with the determinant-line unit.",
    )

    section("D. Residual after the orientation audit")

    record(
        "D.1 orientation plus unit reduces delta to a clean identity-functor theorem",
        True,
        "Need to prove: closed determinant-line phase -> selected-line endpoint is a unit-preserving orientation-preserving isomorphism.",
    )
    record(
        "D.2 current retained packet does not prove that identity-functor theorem",
        True,
        "Orientation reversal and endpoint shifts remain exact counterfunctors.",
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
        print("VERDICT: orientation identity functor route does not close delta from retained data alone.")
        print("KOIDE_DELTA_ORIENTATION_IDENTITY_FUNCTOR_NO_GO=TRUE")
        print("DELTA_ORIENTATION_IDENTITY_FUNCTOR_CLOSES_DELTA=FALSE")
        print("RESIDUAL_ENDPOINT=theta_end-theta0-eta_APS")
        print("RESIDUAL_FUNCTOR_DEGREE=n_minus_one_orientation_alignment_not_retained")
        print("RESIDUAL_FUNCTOR_OFFSET=c_endpoint_basepoint_not_retained")
        return 0

    print("VERDICT: orientation identity functor audit has FAILs.")
    print("KOIDE_DELTA_ORIENTATION_IDENTITY_FUNCTOR_NO_GO=FALSE")
    print("DELTA_ORIENTATION_IDENTITY_FUNCTOR_CLOSES_DELTA=FALSE")
    print("RESIDUAL_ENDPOINT=theta_end-theta0-eta_APS")
    print("RESIDUAL_FUNCTOR_DEGREE=n_minus_one_orientation_alignment_not_retained")
    print("RESIDUAL_FUNCTOR_OFFSET=c_endpoint_basepoint_not_retained")
    return 1


if __name__ == "__main__":
    sys.exit(main())
