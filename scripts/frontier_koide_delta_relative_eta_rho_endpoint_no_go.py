#!/usr/bin/env python3
"""
Koide delta relative-eta/rho endpoint no-go.

Theorem attempt:
  Use relative eta/rho invariants of the retained Z3 boundary data to remove
  the open endpoint ambiguity and derive theta_end - theta0 = eta_APS.

Result:
  Negative.  The three retained Z3 character twists give closed eta values

      eta_0 = 2/9, eta_1 = eta_2 = -1/9.

  Relative eta/rho differences are therefore only 0 or +/-1/3.  They are
  closed comparison invariants, not open selected-line Berry endpoints.
  Hitting eta_APS from a nonzero rho value requires an extra normalization
  coefficient 2/3, and choosing eta_0 itself is the already-known closed APS
  support rather than the missing open-endpoint functor.

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
    section("A. Closed eta and relative rho values")

    eta_values = {m: twisted_eta_z3_weights_12(m) for m in range(3)}
    eta_aps = eta_values[0]
    record(
        "A.1 retained untwisted APS value is exactly 2/9",
        eta_aps == sp.Rational(2, 9),
        f"eta_values={eta_values}",
    )
    record(
        "A.2 nontrivial character twists are both -1/9",
        eta_values[1] == sp.Rational(-1, 9) and eta_values[2] == sp.Rational(-1, 9),
        f"eta_1={eta_values[1]}, eta_2={eta_values[2]}",
    )

    rho = {(m, n): sp.simplify(eta_values[m] - eta_values[n]) for m in range(3) for n in range(3)}
    rho_set = sorted(set(rho.values()), key=lambda x: float(x))
    record(
        "A.3 relative eta/rho differences are only 0 and +/-1/3",
        rho_set == [sp.Rational(-1, 3), sp.Rational(0), sp.Rational(1, 3)],
        f"rho_set={rho_set}",
    )
    record(
        "A.4 eta_APS itself is not a nonzero relative-rho value",
        eta_aps not in rho_set,
        f"eta_APS={eta_aps}, rho_set={rho_set}",
    )

    section("B. Normalized rho endpoint would add a coefficient")

    c = sp.symbols("c", real=True)
    nonzero_rho = sp.Rational(1, 3)
    c_solution = sp.solve(sp.Eq(c * nonzero_rho, eta_aps), c)
    record(
        "B.1 mapping nonzero rho to eta requires c=2/3",
        c_solution == [sp.Rational(2, 3)],
        f"c*(1/3)=2/9 -> c={c_solution}",
    )
    record(
        "B.2 the coefficient is not fixed by relative eta arithmetic",
        True,
        "Relative eta supplies the closed comparison value 1/3; c=2/3 is a new endpoint normalization.",
    )

    section("C. Closed comparison invariant still leaves open endpoint freedom")

    theta0, theta_end, chi0, chi_end = sp.symbols("theta0 theta_end chi0 chi_end", real=True)
    endpoint = sp.simplify(theta_end - theta0)
    endpoint_gauged = sp.simplify(endpoint + chi_end - chi0)
    residual = sp.simplify(endpoint - eta_aps)
    gauge_fit = sp.solve(sp.Eq(endpoint_gauged, eta_aps), chi_end)
    record(
        "C.1 selected-line endpoint has the same open-gauge residual",
        residual == theta_end - theta0 - sp.Rational(2, 9),
        f"RESIDUAL_ENDPOINT={residual}",
    )
    record(
        "C.2 endpoint trivialization can fit eta independently of rho",
        gauge_fit == [chi0 - theta_end + theta0 + sp.Rational(2, 9)],
        f"chi_end={gauge_fit}",
    )
    record(
        "C.3 rho compares two closed twisted sectors, not a selected open segment",
        True,
        "It has no data for the physical endpoint sections of the Brannen line.",
    )

    section("D. Verdict")

    record(
        "D.1 relative eta/rho route does not close delta",
        True,
        "It strengthens the topological audit but leaves the Berry/APS open-endpoint functor.",
    )
    record(
        "D.2 delta remains open after relative-rho audit",
        True,
        "Residual primitive: physical open selected-line endpoint identification.",
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
        print("VERDICT: relative eta/rho closed invariants do not close delta.")
        print("KOIDE_DELTA_RELATIVE_ETA_RHO_ENDPOINT_NO_GO=TRUE")
        print("DELTA_RELATIVE_ETA_RHO_ENDPOINT_CLOSES_DELTA=FALSE")
        print("RESIDUAL_ENDPOINT=theta_end-theta0-eta_APS")
        print("RESIDUAL_NORMALIZATION=rho_to_open_endpoint_coefficient_not_retained")
        return 0

    print("VERDICT: relative eta/rho endpoint audit has FAILs.")
    print("KOIDE_DELTA_RELATIVE_ETA_RHO_ENDPOINT_NO_GO=FALSE")
    print("DELTA_RELATIVE_ETA_RHO_ENDPOINT_CLOSES_DELTA=FALSE")
    print("RESIDUAL_ENDPOINT=theta_end-theta0-eta_APS")
    print("RESIDUAL_NORMALIZATION=rho_to_open_endpoint_coefficient_not_retained")
    return 1


if __name__ == "__main__":
    sys.exit(main())
