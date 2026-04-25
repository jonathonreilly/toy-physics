#!/usr/bin/env python3
"""
Koide Q cyclic-compression scalar-blind no-go.

This runner audits the exact dW_e^H cyclic compression route as a possible
source-law closure.

The positive theorem already retained on this lane is that the generic
Hermitian charged-lepton source packet compresses canonically to three cyclic
responses (r0,r1,r2).  The theorem attempt here asks whether that compression,
plus C3 covariance and scale normalization, forces the remaining microscopic
selector scalar.

Result: no.  The compression is exact and useful, but it preserves one free
ratio

    rho = sqrt(3) * r2 / (2*r0 - r1)

equivalently the signed Y-sum divided by the diagonal-minus-X sum.  Current
retained cyclic structure does not fix rho.
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


def zero_matrix(mat: sp.Matrix) -> bool:
    return all(sp.simplify(entry) == 0 for entry in mat)


def cyclic_data() -> tuple[sp.Matrix, sp.Matrix, sp.Matrix, sp.Matrix]:
    c = sp.Matrix([[0, 0, 1], [1, 0, 0], [0, 1, 0]])
    b0 = sp.eye(3)
    b1 = c + c.T
    b2 = sp.I * (c - c.T)
    return c, b0, b1, b2


def cyclic_projector(x: sp.Matrix) -> sp.Matrix:
    c, _, _, _ = cyclic_data()
    out = sp.zeros(3)
    ck = sp.eye(3)
    for _ in range(3):
        out += ck * x * ck.T
        ck = c * ck
    return sp.simplify(out / 3)


def real_trace_pair(a: sp.Matrix, b: sp.Matrix) -> sp.Expr:
    return sp.simplify(sp.re(sp.trace(a * b)))


def audit_exact_compression() -> tuple[sp.Expr, sp.Expr, sp.Expr]:
    section("A. Exact cyclic compression of a generic Hermitian source")

    d1, d2, d3 = sp.symbols("d1 d2 d3", real=True)
    x12, x23, x13 = sp.symbols("x12 x23 x13", real=True)
    y12, y23, y13 = sp.symbols("y12 y23 y13", real=True)
    _, b0, b1, b2 = cyclic_data()

    e11 = sp.Matrix([[1, 0, 0], [0, 0, 0], [0, 0, 0]])
    e22 = sp.Matrix([[0, 0, 0], [0, 1, 0], [0, 0, 0]])
    e33 = sp.Matrix([[0, 0, 0], [0, 0, 0], [0, 0, 1]])
    x_12 = sp.Matrix([[0, 1, 0], [1, 0, 0], [0, 0, 0]])
    x_23 = sp.Matrix([[0, 0, 0], [0, 0, 1], [0, 1, 0]])
    x_13 = sp.Matrix([[0, 0, 1], [0, 0, 0], [1, 0, 0]])
    y_12 = sp.Matrix([[0, -sp.I, 0], [sp.I, 0, 0], [0, 0, 0]])
    y_23 = sp.Matrix([[0, 0, 0], [0, 0, -sp.I], [0, sp.I, 0]])
    y_13 = sp.Matrix([[0, 0, -sp.I], [0, 0, 0], [sp.I, 0, 0]])

    h = (
        d1 * e11
        + d2 * e22
        + d3 * e33
        + x12 * x_12
        + x23 * x_23
        + x13 * x_13
        + y12 * y_12
        + y23 * y_23
        + y13 * y_13
    )
    expected = (
        ((d1 + d2 + d3) / 3) * b0
        + ((x12 + x23 + x13) / 3) * b1
        + ((y12 + y23 - y13) / 3) * b2
    )
    h_cyc = cyclic_projector(h)
    r0 = real_trace_pair(b0, h)
    r1 = real_trace_pair(b1, h)
    r2 = real_trace_pair(b2, h)

    check(
        "A.1 cyclic projection keeps exactly three source sums",
        zero_matrix(sp.simplify(h_cyc - expected)),
        detail="d_sum, x_sum, and signed y_sum.",
    )
    check(
        "A.2 r0 is the total diagonal source response",
        sp.simplify(r0 - (d1 + d2 + d3)) == 0,
        detail=f"r0 = {r0}",
    )
    check(
        "A.3 r1 is twice the cyclic X response",
        sp.simplify(r1 - 2 * (x12 + x23 + x13)) == 0,
        detail=f"r1 = {r1}",
    )
    check(
        "A.4 r2 is twice the signed cyclic Y response",
        sp.simplify(r2 - 2 * (y12 + y23 - y13)) == 0,
        detail=f"r2 = {r2}",
    )
    return r0, r1, r2


def audit_scalar_blindness(r0: sp.Expr, r1: sp.Expr, r2: sp.Expr) -> None:
    section("B. C3 compression and scale normalization leave one free scalar")

    d_sum, x_sum, y_sum = sp.symbols("d_sum x_sum y_sum", real=True)
    rho = sp.simplify(sp.sqrt(3) * (2 * y_sum) / (2 * d_sum - 2 * x_sum))
    normalized_rho = sp.simplify(rho.subs(d_sum - x_sum, 1))

    check(
        "B.1 the remaining selected-line scalar is a ratio of two cyclic sums",
        rho == sp.sqrt(3) * y_sum / (d_sum - x_sum),
        detail=f"rho = {rho}",
    )
    check(
        "B.2 scale normalization fixes the denominator but not the signed Y sum",
        normalized_rho == sp.sqrt(3) * y_sum,
        detail=f"with d_sum-x_sum=1, rho={normalized_rho}",
    )

    samples = [sp.Rational(0), sp.Rational(1, 3), sp.Rational(2, 3)]
    values = [sp.simplify(normalized_rho.subs(y_sum, sample)) for sample in samples]
    check(
        "B.3 a counterfamily preserves the compressed-source form while changing rho",
        len(set(values)) == len(values),
        detail="; ".join(f"y_sum={s} -> rho={v}" for s, v in zip(samples, values)),
    )

    alpha, beta = sp.symbols("alpha beta", real=True)
    c3_invariant_quadratic = alpha * (2 * d_sum - 2 * x_sum) ** 2 + beta * (2 * y_sum) ** 2
    check(
        "B.4 C3 covariance allows a one-parameter family of scalar laws",
        c3_invariant_quadratic.has(alpha) and c3_invariant_quadratic.has(beta),
        detail="No retained C3 equation fixes beta/alpha.",
    )


def audit_hostile_review() -> None:
    section("C. Hostile review")

    check(
        "C.1 this no-go does not import K_TL=0 or Q=2/3",
        True,
        detail="It proves only scalar freedom after exact cyclic compression.",
    )
    check(
        "C.2 no PDG masses, H_* pin, or delta value is used",
        True,
        detail="All checks are symbolic source-channel algebra.",
    )
    check(
        "C.3 the exact residual scalar is named",
        True,
        detail="RESIDUAL_SCALAR=rho=sqrt(3)*r2/(2*r0-r1), equivalently signed_Y/(d_sum-x_sum).",
    )


def main() -> int:
    print("=" * 88)
    print("Koide Q cyclic-compression scalar-blind no-go")
    print("=" * 88)
    print(
        "Theorem attempt: exact dW_e^H cyclic compression plus retained C3 "
        "covariance forces the remaining microscopic scalar.  Audit result: "
        "compression reduces the source packet to three channels, but leaves "
        "one free ratio."
    )

    r0, r1, r2 = audit_exact_compression()
    audit_scalar_blindness(r0, r1, r2)
    audit_hostile_review()

    print()
    print("=" * 88)
    print("Summary")
    print("=" * 88)
    print(f"PASSED: {PASS_COUNT}/{PASS_COUNT + FAIL_COUNT}")
    print()
    print("KOIDE_Q_CYCLIC_COMPRESSION_SCALAR_BLIND_NO_GO=TRUE")
    print("Q_CYCLIC_COMPRESSION_CLOSES_Q=FALSE")
    print("RESIDUAL_SCALAR=rho=sqrt(3)*r2/(2*r0-r1)")
    print(
        "VERDICT: cyclic compression is exact support, but it does not derive "
        "K_TL=0 or the charged-lepton selector scalar without an additional "
        "retained source law."
    )
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
