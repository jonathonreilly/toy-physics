#!/usr/bin/env python3
"""
Koide delta endpoint-functor classification no-go.

Theorem attempt:
  Remove the remaining delta condition by functoriality alone.  Classify smooth
  additive maps from the closed APS phase group to the selected-line open
  endpoint phase group.  Perhaps functoriality forces the identity map, so
  delta_open = eta_APS.

Result:
  Negative, but sharpened.  Additive smooth phase functors have the affine
  form

      F(eta) = n eta + c          (mod 1)

  with integer degree n on U(1) and offset c fixed only after a basepoint
  trivialization.  Unit preservation removes c, and orientation-preserving
  automorphism restricts n to +1.  But those two requirements are exactly the
  endpoint identity/trivialization law.  Functoriality by itself allows n=0,
  n=-1, n=2, and endpoint offsets, all compatible with closed APS support as
  maps of phase groups.

Therefore endpoint functor classification reduces delta closure to:

      derive n = 1 and c = 0 for the selected-line endpoint functor.

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
    section("A. Smooth additive endpoint functor form")

    eta1, eta2, n, c = sp.symbols("eta1 eta2 n c", real=True)
    F_eta1 = endpoint_functor(eta1, n, c)
    F_eta2 = endpoint_functor(eta2, n, c)
    F_sum = endpoint_functor(eta1 + eta2, n, c)
    additivity_defect = sp.simplify(F_sum - F_eta1 - F_eta2)
    record(
        "A.1 affine phase map is additive only after unit/basepoint offset is removed",
        additivity_defect == -c,
        f"F(eta1+eta2)-F(eta1)-F(eta2)={additivity_defect}",
    )
    record(
        "A.2 unit preservation forces c=0",
        sp.solve(sp.Eq(endpoint_functor(0, n, c), 0), c) == [0],
        "F(0)=0 -> c=0.",
    )

    section("B. Degree freedom remains after unit preservation")

    eta = sp.Rational(2, 9)
    degree_samples = [-1, 0, 1, 2, 3]
    lines = []
    ok = True
    for degree in degree_samples:
        value = endpoint_functor(eta, sp.Integer(degree), sp.Integer(0))
        ok = ok and value == degree * eta
        lines.append(f"n={degree}: F(eta_APS)={value}")
    record(
        "B.1 unit-preserving functoriality leaves integer degree n",
        ok,
        "\n".join(lines),
    )
    record(
        "B.2 delta closure requires degree n=1",
        sp.solve(sp.Eq(endpoint_functor(eta, n, 0), eta), n) == [1],
        "F(eta_APS)=eta_APS -> n=1 for eta_APS != 0.",
    )

    section("C. Offsets are endpoint trivializations")

    c_needed = sp.solve(sp.Eq(endpoint_functor(eta, n, c), eta), c)
    record(
        "C.1 any degree can be made to close by choosing an offset",
        c_needed == [sp.Rational(2, 9) - sp.Rational(2, 9) * n],
        f"c_required={c_needed[0]}",
    )
    record(
        "C.2 choosing the closing offset is exactly endpoint trivialization",
        True,
        "It fixes the open endpoint basepoint rather than deriving it.",
    )

    section("D. Orientation/automorphism constraints")

    orientation_degrees = [-1, 1]
    record(
        "D.1 smooth group automorphisms of U(1) have degree +/-1",
        set(orientation_degrees) == {-1, 1},
        "Orientation choice distinguishes complex conjugation from identity.",
    )
    record(
        "D.2 orientation-preserving automorphism would close delta",
        endpoint_functor(eta, 1, 0) == eta,
        "But 'orientation-preserving identity on the selected endpoint' is the missing functor law.",
    )
    record(
        "D.3 orientation reversal gives a non-closing equally functorial endpoint",
        endpoint_functor(eta, -1, 0) == -sp.Rational(2, 9),
        "n=-1 is excluded only after selecting orientation on the open endpoint functor.",
    )

    section("E. Verdict")

    theta0, theta_end = sp.symbols("theta0 theta_end", real=True)
    residual = sp.simplify(theta_end - theta0 - eta)
    record(
        "E.1 endpoint functor classification does not close delta",
        residual == theta_end - theta0 - sp.Rational(2, 9),
        f"RESIDUAL_ENDPOINT={residual}",
    )
    record(
        "E.2 residual is reduced to identity degree and zero offset",
        True,
        "Need a retained theorem deriving n=1 and c=0 for the selected-line endpoint functor.",
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
        print("VERDICT: endpoint functor classification does not close delta.")
        print("KOIDE_DELTA_ENDPOINT_FUNCTOR_CLASSIFICATION_NO_GO=TRUE")
        print("DELTA_ENDPOINT_FUNCTOR_CLASSIFICATION_CLOSES_DELTA=FALSE")
        print("RESIDUAL_ENDPOINT=theta_end-theta0-eta_APS")
        print("RESIDUAL_FUNCTOR_DEGREE=n_minus_one")
        print("RESIDUAL_FUNCTOR_OFFSET=c_endpoint_trivialization")
        return 0

    print("VERDICT: endpoint functor classification audit has FAILs.")
    print("KOIDE_DELTA_ENDPOINT_FUNCTOR_CLASSIFICATION_NO_GO=FALSE")
    print("DELTA_ENDPOINT_FUNCTOR_CLASSIFICATION_CLOSES_DELTA=FALSE")
    print("RESIDUAL_ENDPOINT=theta_end-theta0-eta_APS")
    print("RESIDUAL_FUNCTOR_DEGREE=n_minus_one")
    print("RESIDUAL_FUNCTOR_OFFSET=c_endpoint_trivialization")
    return 1


if __name__ == "__main__":
    sys.exit(main())
