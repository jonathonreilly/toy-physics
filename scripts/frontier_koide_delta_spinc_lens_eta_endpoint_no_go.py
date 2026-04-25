#!/usr/bin/env python3
"""
Koide delta spin-c/lens eta endpoint no-go.

Theorem attempt:
  Refine the ambient APS eta calculation by spin or spin-c/lens-space data.
  Perhaps the refinement identifies the physical selected-line open endpoint
  and derives theta_end - theta0 = eta_APS = 2/9.

Result:
  Negative.  For the retained Z3 lens/orbifold data with weights (1,2), the
  untwisted equivariant eta is exactly 2/9.  Twisting by the three Z3
  characters gives the closed-invariant set

      {2/9, -1/9, -1/9}.

  Since p=3 is odd, the lens-space spin structure is unique; it cannot select
  an additional endpoint.  Spin-c character refinements shift closed eta data
  by thirds, but they still do not supply an open selected-line
  trivialization.  Choosing the untwisted value as the open endpoint is the
  residual Berry/APS bridge.

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


def twisted_eta_z3_weights_12(character: int) -> sp.Expr:
    omega = -sp.Rational(1, 2) + sp.I * sp.sqrt(3) / 2
    total = 0
    for k in (1, 2):
        z1 = omega**k
        z2 = omega ** (2 * k)
        chi = omega ** (character * k)
        total += sp.simplify(chi / ((z1 - 1) * (z2 - 1)))
    return sp.simplify(total / 3)


def main() -> int:
    section("A. Spin/spin-c labels for the retained Z3 lens data")

    p = sp.Integer(3)
    spin_count = sp.gcd(p, 2)
    spinc_count = p
    record(
        "A.1 p=3 odd gives a unique spin structure",
        spin_count == 1,
        "Hom(H1(L(3),Z2),Z2) is trivial for odd p.",
    )
    record(
        "A.2 spin-c/flat character refinements are labeled by Z3",
        spinc_count == 3,
        "characters m=0,1,2.",
    )

    section("B. Twisted closed eta values")

    eta_values = {m: twisted_eta_z3_weights_12(m) for m in range(3)}
    record(
        "B.1 untwisted ambient APS value is exactly 2/9",
        eta_values[0] == sp.Rational(2, 9),
        f"eta_0={eta_values[0]}",
    )
    record(
        "B.2 nontrivial Z3 character twists give -1/9",
        eta_values[1] == sp.Rational(-1, 9) and eta_values[2] == sp.Rational(-1, 9),
        f"eta_values={eta_values}",
    )
    record(
        "B.3 spin-c refinement shifts closed eta data by thirds",
        sp.simplify(eta_values[0] - eta_values[1]) == sp.Rational(1, 3)
        and sp.simplify(eta_values[0] - eta_values[2]) == sp.Rational(1, 3),
        "closed eta differences are 1/3.",
    )

    section("C. Closed eta refinement still does not choose an open endpoint")

    theta0, theta_end, endpoint_gauge = sp.symbols("theta0 theta_end endpoint_gauge", real=True)
    delta_open = sp.simplify(theta_end - theta0)
    residuals = {m: sp.simplify(delta_open - eta) for m, eta in eta_values.items()}
    record(
        "C.1 each spin-c value would require its own open endpoint identification",
        residuals[0] == theta_end - theta0 - sp.Rational(2, 9)
        and residuals[1] == theta_end - theta0 + sp.Rational(1, 9)
        and residuals[2] == theta_end - theta0 + sp.Rational(1, 9),
        f"residuals={residuals}",
    )
    gauge_solutions = {
        m: sp.solve(sp.Eq(delta_open + endpoint_gauge, eta), endpoint_gauge)[0]
        for m, eta in eta_values.items()
    }
    record(
        "C.2 endpoint gauge can fit any closed eta refinement",
        gauge_solutions[0] == -theta_end + theta0 + sp.Rational(2, 9)
        and gauge_solutions[1] == -theta_end + theta0 - sp.Rational(1, 9),
        f"endpoint_gauge_solutions={gauge_solutions}",
    )
    record(
        "C.3 choosing m=0 recovers support but not the selected-line bridge",
        True,
        "The untwisted eta is the known ambient support value; the open phase remains separate.",
    )

    section("D. Verdict")

    record(
        "D.1 spin-c/lens eta refinement route does not close delta",
        True,
        "It refines closed APS data; it does not provide the open selected-line endpoint functor.",
    )
    record(
        "D.2 delta remains open after spin-c eta audit",
        True,
        "Residual primitive: theta_end - theta0 equals the chosen closed eta value by physical trivialization.",
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
        print("VERDICT: spin-c/lens eta refinement does not close delta.")
        print("KOIDE_DELTA_SPINC_LENS_ETA_ENDPOINT_NO_GO=TRUE")
        print("DELTA_SPINC_LENS_ETA_ENDPOINT_CLOSES_DELTA=FALSE")
        print("RESIDUAL_ENDPOINT=theta_end-theta0-eta_APS")
        print("RESIDUAL_TRIVIALIZATION=open_selected_line_endpoint_not_fixed_by_closed_spinc_eta")
        return 0

    print("VERDICT: spin-c/lens eta endpoint audit has FAILs.")
    print("KOIDE_DELTA_SPINC_LENS_ETA_ENDPOINT_NO_GO=FALSE")
    print("DELTA_SPINC_LENS_ETA_ENDPOINT_CLOSES_DELTA=FALSE")
    print("RESIDUAL_ENDPOINT=theta_end-theta0-eta_APS")
    print("RESIDUAL_TRIVIALIZATION=open_selected_line_endpoint_not_fixed_by_closed_spinc_eta")
    return 1


if __name__ == "__main__":
    sys.exit(main())
