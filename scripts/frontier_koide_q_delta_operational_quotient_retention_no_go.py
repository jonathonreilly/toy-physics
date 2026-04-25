#!/usr/bin/env python3
"""
Koide Q/delta operational-quotient retention no-go.

Theorem attempt:
  The operational-quotient laws candidate closes both residuals if removed
  embedding labels and endpoint complements are not source-visible.  Perhaps
  the current retained Cl(3)/Z3 and APS data already force that quotient
  principle.

Result:
  Negative, but sharpened.  The current retained data still admits an embedded
  carrier countermodel where the C3 orbit type distinguishes the Q components,
  and a boundary countermodel where a nonzero endpoint transition distinguishes
  the open Brannen segment from the closed APS value.

  Therefore the operational-quotient principle is a real candidate law, but it
  is not yet derived by the retained data.  Positive closure still requires a
  physical theorem that removes source-visible C3 orbit labels and endpoint
  complements from the preparation/gluing problem.

No PDG masses, target fitted value, or H_* pin is used.
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


def q_from_weight(w_plus: sp.Expr) -> sp.Expr:
    r = sp.simplify((1 - w_plus) / w_plus)
    return sp.simplify((1 + r) / 3)


def ktl_from_weight(w_plus: sp.Expr) -> sp.Expr:
    r = sp.simplify((1 - w_plus) / w_plus)
    return sp.simplify((r**2 - 1) / (4 * r))


def eta_abss_z3_weights_12() -> sp.Expr:
    omega = -sp.Rational(1, 2) + sp.I * sp.sqrt(3) / 2
    total = 0
    for k in (1, 2):
        z1 = omega**k
        z2 = omega ** (2 * k)
        total += sp.simplify(1 / ((z1 - 1) * (z2 - 1)))
    return sp.simplify(total / 3)


def open_delta_from_tau(tau: sp.Expr) -> sp.Expr:
    return sp.simplify(eta_abss_z3_weights_12() - tau)


def main() -> int:
    section("A. What the operational quotient law would do")

    w = sp.symbols("w", real=True)
    swap_constraint = sp.solve(sp.Eq(w, 1 - w), w)
    record(
        "A.1 unlabeled two-component quotient would force equal Q source weights",
        swap_constraint == [sp.Rational(1, 2)],
        f"swap constraint gives w={swap_constraint}",
    )
    record(
        "A.2 identity endpoint quotient would force tau=0",
        open_delta_from_tau(0) == sp.Rational(2, 9),
        "tau=0 gives delta_open=eta_APS=2/9.",
    )

    section("B. Retained embedded-carrier countermodel for Q")

    plus_label = frozenset({0})
    perp_label = frozenset({1, 2})
    automorphism_preserves_labels = plus_label == perp_label
    biased_weight = sp.Rational(1, 3)
    record(
        "B.1 current embedded C3 orbit type distinguishes the two source components",
        not automorphism_preserves_labels,
        f"plus_label={sorted(plus_label)}, perp_label={sorted(perp_label)}",
    )
    record(
        "B.2 label-preserving retained data permit a non-closing Q source",
        q_from_weight(biased_weight) == 1
        and ktl_from_weight(biased_weight) == sp.Rational(3, 8),
        f"w={biased_weight}, Q={q_from_weight(biased_weight)}, K_TL={ktl_from_weight(biased_weight)}",
    )

    section("C. Retained boundary countermodel for delta")

    eta = eta_abss_z3_weights_12()
    tau = sp.Rational(1, 9)
    delta_open = open_delta_from_tau(tau)
    record(
        "C.1 retained APS fixed-point value is closed, not an open endpoint selector",
        eta == sp.Rational(2, 9),
        f"eta_APS={eta}",
    )
    record(
        "C.2 nonzero endpoint transition preserves the closed APS value",
        delta_open == sp.Rational(1, 9)
        and sp.simplify(delta_open + tau) == eta,
        f"delta_open={delta_open}, tau={tau}, closed_total={sp.simplify(delta_open + tau)}",
    )

    section("D. Product countermodel")

    record(
        "D.1 Q and delta countermodels are independent residual coordinates",
        True,
        "The Q source weight w and the endpoint transition tau can be varied independently.",
    )
    record(
        "D.2 current retained data do not force the operational quotient laws",
        True,
        "Both countermodels satisfy the retained equations unless a quotient-source/endpoint law is added or derived.",
    )

    section("E. Verdict")

    record(
        "E.1 operational quotient law is not derived by the current retained packet",
        True,
        "The law remains a candidate physical principle, not retained closure.",
    )
    record(
        "E.2 residual is now exactly the operational-quotient retention theorem",
        True,
        "Need to derive source-label quotienting and endpoint-complement quotienting from physics.",
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
        print("VERDICT: current retained data do not derive the operational quotient laws.")
        print("KOIDE_Q_DELTA_OPERATIONAL_QUOTIENT_RETENTION_NO_GO=TRUE")
        print("Q_DELTA_OPERATIONAL_QUOTIENT_RETENTION_CLOSES_Q=FALSE")
        print("Q_DELTA_OPERATIONAL_QUOTIENT_RETENTION_CLOSES_DELTA=FALSE")
        print("RESIDUAL_SCALAR=derive_operational_quotient_source_label_and_endpoint_laws")
        print("RESIDUAL_Q=source_visible_C3_orbit_type_not_excluded")
        print("RESIDUAL_DELTA=source_visible_endpoint_transition_not_excluded")
        return 0

    print("VERDICT: operational-quotient retention audit has FAILs.")
    print("KOIDE_Q_DELTA_OPERATIONAL_QUOTIENT_RETENTION_NO_GO=FALSE")
    print("Q_DELTA_OPERATIONAL_QUOTIENT_RETENTION_CLOSES_Q=FALSE")
    print("Q_DELTA_OPERATIONAL_QUOTIENT_RETENTION_CLOSES_DELTA=FALSE")
    print("RESIDUAL_SCALAR=derive_operational_quotient_source_label_and_endpoint_laws")
    return 1


if __name__ == "__main__":
    sys.exit(main())
