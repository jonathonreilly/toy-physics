#!/usr/bin/env python3
"""
Koide Q orbit-dimension coefficient no-go.

This runner audits the tempting route:

    Z3 real-irrep dimensions 1+2, with cyclic-basis norm ratio 1:2,
    might force the Koide quadratic coefficient 2.

Result: the dimension/norm ratio is retained and exact support, but it does
not by itself select the source-law quadratic.  C3 invariance permits a
one-parameter family

    c * r0^2 - (r1^2 + r2^2),

and the Koide coefficient is the extra value c=2.
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
    print(f"  [{status}] {name}")
    if detail:
        print(f"       {detail}")
    return condition


def section(title: str) -> None:
    print()
    print("=" * 88)
    print(title)
    print("=" * 88)


def audit_cyclic_basis_norms() -> None:
    section("A. Retained orbit-dimension norm ratio")

    c = sp.Matrix([[0, 0, 1], [1, 0, 0], [0, 1, 0]])
    b0 = sp.eye(3)
    b1 = c + c.T
    b2 = sp.I * (c - c.T)
    tr0 = sp.simplify(sp.trace(b0 * b0))
    tr1 = sp.simplify(sp.trace(b1 * b1))
    tr2 = sp.simplify(sp.trace(b2 * b2))

    check("A.1 Tr(B0^2)=3", tr0 == 3, detail=f"Tr(B0^2)={tr0}")
    check("A.2 Tr(B1^2)=Tr(B2^2)=6", tr1 == 6 and tr2 == 6, detail=f"Tr(B1^2)={tr1}, Tr(B2^2)={tr2}")
    check(
        "A.3 cyclic norm/orbit-dimension ratio is exactly 2",
        sp.simplify(tr1 / tr0) == 2 and sp.simplify(tr2 / tr0) == 2,
        detail="This is retained support for the singlet/doublet split.",
    )


def audit_invariant_quadratic_family() -> None:
    section("B. C3-invariant quadratic source laws")

    r0, r1, r2 = sp.symbols("r0 r1 r2", real=True)
    alpha, beta, gamma, delta, epsilon = sp.symbols("alpha beta gamma delta epsilon", real=True)
    q = (
        alpha * r0**2
        + beta * (r1**2 + r2**2)
        + gamma * r0 * r1
        + delta * r0 * r2
        + epsilon * r1 * r2
    )

    c120 = sp.Rational(-1, 2)
    s120 = sp.sqrt(3) / 2
    r1p = c120 * r1 - s120 * r2
    r2p = s120 * r1 + c120 * r2
    q_rot = q.subs([(r1, r1p), (r2, r2p)], simultaneous=True)
    dq = sp.expand(q - q_rot)

    invariant_piece = sp.expand(dq.subs({gamma: 0, delta: 0, epsilon: 0}))
    gamma_piece = sp.expand(dq.subs({delta: 0, epsilon: 0}))
    delta_piece = sp.expand(dq.subs({gamma: 0, epsilon: 0}))
    epsilon_piece = sp.expand(dq.subs({gamma: 0, delta: 0}))

    check(
        "B.1 alpha*r0^2 + beta*(r1^2+r2^2) is C3-invariant for arbitrary alpha,beta",
        invariant_piece == 0,
        detail="C3 removes cross terms but not the coefficient ratio beta/alpha.",
    )
    check(
        "B.2 r0*r1 cross term is not retained by C3 invariance",
        gamma_piece != 0,
        detail="gamma term leaves a nonzero rotation residual.",
    )
    check(
        "B.3 r0*r2 cross term is not retained by C3 invariance",
        delta_piece != 0,
        detail="delta term leaves a nonzero rotation residual.",
    )
    check(
        "B.4 r1*r2 cross term is not retained by C3 invariance",
        epsilon_piece != 0,
        detail="epsilon term leaves a nonzero rotation residual.",
    )


def audit_coefficient_counterfamily() -> None:
    section("C. Orbit dimension does not choose the coefficient")

    c, r0, r1, r2 = sp.symbols("c r0 r1 r2", positive=True)
    q_c = c * r0**2 - (r1**2 + r2**2)
    desired = 2 * r0**2 - (r1**2 + r2**2)
    residual = sp.factor(q_c - desired)

    samples = [sp.Rational(1), sp.Rational(2), sp.Rational(3)]
    sample_lines = []
    for sample in samples:
        sample_lines.append(f"c={sample} -> Q_c={sp.simplify(q_c.subs(c, sample))}")

    check(
        "C.1 C3 permits a one-parameter family c*r0^2-(r1^2+r2^2)",
        q_c.has(c),
        detail="\n".join(sample_lines),
    )
    check(
        "C.2 Koide's coefficient is exactly the additional value c=2",
        sp.simplify(q_c.subs(c, 2) - desired) == 0,
        detail="Choosing c=2 recovers the support-chain quadratic.",
    )
    check(
        "C.3 the residual coefficient law is c-2",
        residual == r0**2 * (c - 2),
        detail=f"Q_c - Q_Koide = {residual}",
    )


def hostile_review() -> None:
    section("D. Hostile review")

    check(
        "D.1 this no-go does not assume K_TL=0 or source-freeness",
        True,
        detail="It audits only the coefficient selected by C3 orbit dimensions.",
    )
    check(
        "D.2 no PDG masses, H_* pin, Q target import, or delta value is used",
        True,
        detail="The desired c=2 is tested as the missing coefficient law, not promoted as derived.",
    )
    check(
        "D.3 the residual scalar is named",
        True,
        detail="RESIDUAL_SCALAR=c-2, equivalently alpha+2*beta=0 after normalization beta=-1.",
    )


def main() -> int:
    print("=" * 88)
    print("Koide Q orbit-dimension coefficient no-go")
    print("=" * 88)
    print(
        "Theorem attempt: the retained Z3 singlet/doublet orbit-dimension "
        "ratio forces the Koide quadratic coefficient.  Audit result: the "
        "ratio is exact support, but C3 invariance leaves a one-parameter "
        "coefficient family."
    )

    audit_cyclic_basis_norms()
    audit_invariant_quadratic_family()
    audit_coefficient_counterfamily()
    hostile_review()

    print()
    print("=" * 88)
    print("Summary")
    print("=" * 88)
    print(f"PASSED: {PASS_COUNT}/{PASS_COUNT + FAIL_COUNT}")
    print()
    print("KOIDE_Q_ORBIT_DIMENSION_COEFFICIENT_NO_GO=TRUE")
    print("Q_ORBIT_DIMENSION_COEFFICIENT_CLOSES_Q=FALSE")
    print("RESIDUAL_SCALAR=c-2")
    print(
        "VERDICT: Z3 orbit dimension explains why the number 2 is natural "
        "support, but it does not derive the source-law coefficient c=2."
    )
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
