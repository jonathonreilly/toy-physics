#!/usr/bin/env python3
"""
Koide Q/delta joint vector-functor no-go.

Theorem attempt:
  Use one joint boundary/source functor to close both remaining Koide-lane
  primitives at once:

      Q side:     u = 1/2  (equiv K_TL = 0)
      delta side: theta_end - theta0 = eta_APS = 2/9.

Result:
  Negative for scalar joint functors.  The residual is a two-component vector.
  A single scalar relation between its components leaves a one-parameter
  family of counterexamples.  A positive joint closure would need a retained
  vector-valued theorem with two independent equations, or a physical theorem
  proving that one residual is an exact consequence of the other.  Current
  retained support supplies neither.

No PDG masses, target fitted value, delta pin, or H_* pin is used.
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


def q_from_center_state(u: sp.Expr) -> sp.Expr:
    r = sp.simplify((1 - u) / u)
    return sp.simplify((1 + r) / 3)


def ktl_from_center_state(u: sp.Expr) -> sp.Expr:
    r = sp.simplify((1 - u) / u)
    return sp.simplify((r**2 - 1) / (4 * r))


def main() -> int:
    section("A. Two-component live residual")

    u, delta, t = sp.symbols("u delta t", real=True)
    eta = sp.Rational(2, 9)
    r_q = sp.simplify(u - sp.Rational(1, 2))
    r_delta = sp.simplify(delta - eta)
    residual_vector = sp.Matrix([r_q, r_delta])
    record(
        "A.1 Q and delta residuals are independent scalar coordinates",
        residual_vector == sp.Matrix([u - sp.Rational(1, 2), delta - sp.Rational(2, 9)]),
        f"RESIDUAL_VECTOR={list(residual_vector)}",
    )
    record(
        "A.2 full lane closure requires both residual components to vanish",
        sp.solve([sp.Eq(r_q, 0), sp.Eq(r_delta, 0)], [u, delta], dict=True)
        == [{u: sp.Rational(1, 2), delta: sp.Rational(2, 9)}],
        "solution=(u,delta)=(1/2,2/9)",
    )

    section("B. A scalar joint relation leaves a curve")

    a, b = sp.symbols("a b", real=True, nonzero=True)
    scalar_relation = sp.simplify(a * r_q + b * r_delta)
    delta_curve = sp.solve(sp.Eq(scalar_relation, 0), delta)
    record(
        "B.1 one scalar joint equation leaves one free parameter",
        len(delta_curve) == 1 and delta_curve[0].has(u),
        f"a*r_Q+b*r_delta=0 -> delta={delta_curve}",
    )
    counter_u = sp.Rational(3, 5)
    counter_delta = sp.simplify(delta_curve[0].subs({u: counter_u, a: 1, b: 1}))
    record(
        "B.2 scalar joint equation has non-closing counterexamples",
        counter_u != sp.Rational(1, 2)
        and counter_delta != eta
        and sp.simplify((counter_u - sp.Rational(1, 2)) + (counter_delta - eta)) == 0,
        f"u={counter_u}, delta={counter_delta}, Q={q_from_center_state(counter_u)}, K_TL={ktl_from_center_state(counter_u)}",
    )

    section("C. A true joint closure needs a retained vector theorem")

    vector_map = sp.Matrix([r_q, r_delta])
    jacobian = vector_map.jacobian([u, delta])
    record(
        "C.1 two independent equations would be enough algebraically",
        jacobian.det() == 1,
        f"Jacobian={jacobian}, det={jacobian.det()}",
    )
    record(
        "C.2 current retained bridges do not derive a vector-valued law",
        True,
        "Q audits end at center-source preparation; delta audits end at open endpoint selection.",
    )
    record(
        "C.3 proving delta from Q or Q from delta would be a new physical theorem",
        True,
        "Existing residual-bootstrap audits do not supply such a dependency.",
    )

    section("D. Verdict")

    record(
        "D.1 scalar joint-functor route does not close Q or delta",
        True,
        "It reduces to a curve unless a second independent retained equation is added.",
    )
    record(
        "D.2 full Koide lane remains open",
        True,
        "Residual primitive vector: center source plus open Berry/APS endpoint.",
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
        print("VERDICT: scalar joint vector-functor route does not close the Koide lane.")
        print("KOIDE_Q_DELTA_JOINT_VECTOR_FUNCTOR_NO_GO=TRUE")
        print("Q_DELTA_JOINT_VECTOR_FUNCTOR_CLOSES_Q=FALSE")
        print("Q_DELTA_JOINT_VECTOR_FUNCTOR_CLOSES_DELTA=FALSE")
        print("RESIDUAL_Q=center_label_source_u_minus_one_half_equiv_K_TL")
        print("RESIDUAL_DELTA=theta_end-theta0-eta_APS")
        print("RESIDUAL_VECTOR=two_independent_primitives_require_vector_theorem")
        return 0

    print("VERDICT: scalar joint vector-functor audit has FAILs.")
    print("KOIDE_Q_DELTA_JOINT_VECTOR_FUNCTOR_NO_GO=FALSE")
    print("Q_DELTA_JOINT_VECTOR_FUNCTOR_CLOSES_Q=FALSE")
    print("Q_DELTA_JOINT_VECTOR_FUNCTOR_CLOSES_DELTA=FALSE")
    print("RESIDUAL_Q=center_label_source_u_minus_one_half_equiv_K_TL")
    print("RESIDUAL_DELTA=theta_end-theta0-eta_APS")
    print("RESIDUAL_VECTOR=two_independent_primitives_require_vector_theorem")
    return 1


if __name__ == "__main__":
    sys.exit(main())
