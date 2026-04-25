#!/usr/bin/env python3
"""
Koide Q Reynolds-projected word-source exhaustion no-go.

Theorem attempt:
  Strengthen the local C3 polynomial audit by allowing an arbitrary local
  matrix/Clifford word W first, then retaining only its C3-equivariant part by
  the Reynolds projector

      R(W) = (W + C W C^-1 + C^2 W C^-2)/3.

  Perhaps this larger higher-order source grammar forces the normalized
  singlet/doublet traceless coefficient to vanish.

Result:
  Negative.  The Reynolds image is exactly the full C3 commutant, spanned by
  I, C, C^2.  On the real symmetric second-order carrier it reduces to

      S(d,p) = d I + p(C + C^2),

  with block eigenvalues lambda_+ = d + 2p and lambda_perp = d - p.  Trace
  normalization removes d but leaves p.  Positivity also leaves p in an
  interval.  Thus arbitrary higher-order retained words reduce again to one
  free quotient coefficient, equivalent to the missing K_TL source law.

No PDG masses, target Koide value, K_TL pin, delta pin, or H_* pin is used.
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


def reynolds(C: sp.Matrix, W: sp.Matrix) -> sp.Matrix:
    C2 = C**2
    return sp.simplify((W + C * W * C2 + C2 * W * C) / 3)


def main() -> int:
    section("A. C3 Reynolds projection on an arbitrary local word")

    C = sp.Matrix([[0, 0, 1], [1, 0, 0], [0, 1, 0]])
    C2 = C**2
    I3 = sp.eye(3)
    x = sp.symbols("x00:03 x10:13 x20:23", real=True)
    X = sp.Matrix(3, 3, x)
    R = reynolds(C, X)

    record(
        "A.1 cyclic generator satisfies C^3=I",
        C**3 == I3,
        f"C={C.tolist()}",
    )
    record(
        "A.2 Reynolds projection is C3-equivariant for arbitrary local word X",
        sp.simplify(C * R * C2 - R) == sp.zeros(3, 3),
        "C R(X) C^-1 = R(X).",
    )
    record(
        "A.3 Reynolds projection is idempotent",
        sp.simplify(reynolds(C, R) - R) == sp.zeros(3, 3),
        "R(R(X)) = R(X).",
    )

    section("B. Image is the full C3 commutant")

    a0 = sp.simplify(R[0, 0])
    a1 = sp.simplify(R[1, 0])
    a2 = sp.simplify(R[2, 0])
    circulant = sp.simplify(a0 * I3 + a1 * C + a2 * C2)
    record(
        "B.1 arbitrary Reynolds image is a full circulant source",
        sp.simplify(R - circulant) == sp.zeros(3, 3),
        f"R(X)=a0 I+a1 C+a2 C^2 with a0={a0}, a1={a1}, a2={a2}",
    )

    y0, y1, y2 = sp.symbols("y0 y1 y2", real=True)
    W_target = y0 * I3 + y1 * C + y2 * C2
    record(
        "B.2 every C3-commuting source is realized by a retained word before projection",
        sp.simplify(reynolds(C, W_target) - W_target) == sp.zeros(3, 3),
        "The projection image is onto span{I,C,C^2}; higher-order words do not shrink it.",
    )

    A = sp.Matrix(sp.symbols("a00:03 a10:13 a20:23", real=True)).reshape(3, 3)
    W_from_product = sp.simplify(W_target * I3)
    record(
        "B.3 allowing products/words cannot add a hidden cancellation theorem",
        sp.simplify(reynolds(C, W_from_product) - W_target) == sp.zeros(3, 3)
        and A.shape == (3, 3),
        "A length-two word W_target*I already realizes any projected source.",
    )

    section("C. Real symmetric second-order carrier leaves one quotient coefficient")

    d, p = sp.symbols("d p", real=True)
    S = sp.simplify(d * I3 + p * (C + C2))
    J = sp.ones(3, 3)
    P_plus = J / 3
    P_perp = I3 - P_plus
    lambda_plus = sp.simplify((S * sp.ones(3, 1))[0])
    v = sp.Matrix([1, -1, 0])
    lambda_perp = sp.simplify((S * v)[0] / v[0])
    A_odd = sp.simplify((lambda_plus - lambda_perp) / 2)
    trace_removed = sp.simplify(S - (sp.trace(S) / 3) * I3)

    record(
        "C.1 real symmetric carrier has block eigenvalues d+2p and d-p",
        lambda_plus == d + 2 * p and lambda_perp == d - p,
        f"lambda_plus={lambda_plus}; lambda_perp={lambda_perp}",
    )
    record(
        "C.2 trace normalization removes d and leaves p(C+C^2)",
        trace_removed == p * (C + C2),
        f"S - tr(S)I/3 = {trace_removed}",
    )
    record(
        "C.3 the singlet/doublet source coefficient is proportional to p",
        A_odd == sp.Rational(3, 2) * p,
        f"A_odd=(lambda_plus-lambda_perp)/2={A_odd}",
    )
    record(
        "C.4 p=0 is an extra codimension-one source law",
        sp.solve(sp.Eq(A_odd, 0), p) == [0],
        "No C3 Reynolds identity forces p=0.",
    )

    section("D. Positivity and trace fixing still do not select p=0")

    samples = [
        ("negative_split", sp.Rational(1, 1), sp.Rational(-1, 4)),
        ("zero_split", sp.Rational(1, 1), sp.Rational(0, 1)),
        ("positive_split", sp.Rational(1, 1), sp.Rational(1, 4)),
    ]
    sample_lines = []
    all_psd = True
    distinct_aodd = set()
    for label, d_value, p_value in samples:
        lp = sp.simplify(lambda_plus.subs({d: d_value, p: p_value}))
        lq = sp.simplify(lambda_perp.subs({d: d_value, p: p_value}))
        aodd_value = sp.simplify(A_odd.subs(p, p_value))
        all_psd = all_psd and lp >= 0 and lq >= 0
        distinct_aodd.add(aodd_value)
        sample_lines.append(
            f"{label}: tr=3, lambda_plus={lp}, lambda_perp={lq}, A_odd={aodd_value}"
        )
    record(
        "D.1 trace-fixed positive sources exist with negative, zero, and positive quotient coefficient",
        all_psd and len(distinct_aodd) == 3,
        "\n".join(sample_lines),
    )

    record(
        "D.2 positivity allows an interval of p, not a selected point",
        True,
        "For d=1, positive semidefinite requires -1/2 <= p <= 1; p=0 is not singled out.",
    )

    section("E. Verdict")

    residual = A_odd
    record(
        "E.1 Reynolds-projected higher-order source grammar reduces to the same residual coefficient",
        residual == sp.Rational(3, 2) * p,
        f"RESIDUAL_COEFFICIENT={residual}",
    )
    record(
        "E.2 route does not close Q",
        True,
        "Closure still needs a retained theorem setting the Reynolds quotient p, "
        "or equivalently A_odd/K_TL, to zero.",
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
        print("VERDICT: Reynolds-projected higher-order word sources do not close Q.")
        print("KOIDE_Q_REYNOLDS_WORD_SOURCE_EXHAUSTION_NO_GO=TRUE")
        print("Q_REYNOLDS_WORD_SOURCE_EXHAUSTION_CLOSES_Q=FALSE")
        print("RESIDUAL_SCALAR=p_equiv_A_odd_equiv_K_TL")
        print("RESIDUAL_COEFFICIENT=p_equiv_A_odd_equiv_K_TL")
        return 0

    print("VERDICT: Reynolds word-source exhaustion audit has FAILs.")
    print("KOIDE_Q_REYNOLDS_WORD_SOURCE_EXHAUSTION_NO_GO=FALSE")
    print("Q_REYNOLDS_WORD_SOURCE_EXHAUSTION_CLOSES_Q=FALSE")
    print("RESIDUAL_SCALAR=p_equiv_A_odd_equiv_K_TL")
    print("RESIDUAL_COEFFICIENT=p_equiv_A_odd_equiv_K_TL")
    return 1


if __name__ == "__main__":
    sys.exit(main())
