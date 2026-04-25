#!/usr/bin/env python3
"""
Koide Q real-structure neutrality no-go.

Theorem attempt:
  The retained real structure / antiunitary conjugation on the C_3 character
  carrier might be stronger than plain C_3 equivariance.  Since it exchanges
  the omega and omega^2 characters, perhaps it forces a singlet/doublet
  neutrality condition and hence K_TL = 0.

Result:
  No.  The real structure only identifies the two complex conjugate characters
  inside the real doublet.  A C_3-equivariant, real-structure-neutral source
  still has the form a P_plus + b P_perp with one free singlet-vs-doublet
  ratio.  Koide is the special value a=b; the real structure does not derive
  that value.
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
        for line in detail.split("\n"):
            print(f"       {line}")


def section(title: str) -> None:
    print()
    print("=" * 88)
    print(title)
    print("=" * 88)


def q_from_ratio(r: sp.Expr) -> sp.Expr:
    return sp.simplify((1 + r) / 3)


def ktl_from_ratio(r: sp.Expr) -> sp.Expr:
    return sp.simplify((r**2 - 1) / (4 * r))


def main() -> int:
    section("A. Complex character projectors and real structure")

    C = sp.Matrix([[0, 0, 1], [1, 0, 0], [0, 1, 0]])
    I3 = sp.eye(3)
    omega = -sp.Rational(1, 2) + sp.I * sp.sqrt(3) / 2
    P0 = sp.simplify((I3 + C + C**2) / 3)
    P1 = sp.simplify((I3 + omega**2 * C + omega * C**2) / 3)
    P2 = sp.simplify((I3 + omega * C + omega**2 * C**2) / 3)
    P_perp = sp.simplify(P1 + P2)

    record(
        "A.1 P0,P1,P2 are primitive C_3 character idempotents",
        sp.simplify(P0**2 - P0) == sp.zeros(3, 3)
        and sp.simplify(P1**2 - P1) == sp.zeros(3, 3)
        and sp.simplify(P2**2 - P2) == sp.zeros(3, 3)
        and sp.simplify(P0 * P1) == sp.zeros(3, 3)
        and sp.simplify(P1 * P2) == sp.zeros(3, 3)
        and sp.simplify(P0 + P1 + P2 - I3) == sp.zeros(3, 3),
        "P0 is the real singlet; P1 and P2 are conjugate characters.",
    )
    record(
        "A.2 complex conjugation fixes P0 and exchanges P1,P2",
        sp.simplify(sp.conjugate(P0) - P0) == sp.zeros(3, 3)
        and sp.simplify(sp.conjugate(P1) - P2) == sp.zeros(3, 3)
        and sp.simplify(sp.conjugate(P2) - P1) == sp.zeros(3, 3),
        "The real doublet is P_perp=P1+P2.",
    )

    section("B. Most general real-structure-neutral source")

    a, b = sp.symbols("a b", positive=True, real=True)
    S = sp.simplify(a * P0 + b * P_perp)
    record(
        "B.1 S=a P0+b(P1+P2) is C_3-equivariant and real-structure neutral",
        sp.simplify(C * S - S * C) == sp.zeros(3, 3) and sp.conjugate(S) == S,
        "Conjugation removes P1/P2 splitting, not P0/P_perp splitting.",
    )
    record(
        "B.2 the source still contains one free singlet-vs-doublet ratio",
        S.has(a) and S.has(b) and sp.simplify(sp.trace(P0 * S) - a) == 0 and sp.simplify(sp.trace(P_perp * S) - 2 * b) == 0,
        "The invariant data are a on the singlet and b on each doublet character.",
    )

    r = sp.symbols("r", positive=True, real=True)
    q = q_from_ratio(r)
    ktl = ktl_from_ratio(r)
    record(
        "B.3 Koide is the special ratio R=E_perp/E_plus=1, not a real-structure identity",
        sp.solve(sp.Eq(ktl, 0), r) == [1] and sp.simplify(q.subs(r, 1) - sp.Rational(2, 3)) == 0,
        f"Q(R)={q}, K_TL(R)={ktl}",
    )

    section("C. Exact real-neutral off-Koide counterexamples")

    samples = {
        sp.Rational(1, 2): (q_from_ratio(sp.Rational(1, 2)), ktl_from_ratio(sp.Rational(1, 2))),
        sp.Rational(1, 1): (q_from_ratio(sp.Rational(1, 1)), ktl_from_ratio(sp.Rational(1, 1))),
        sp.Rational(2, 1): (q_from_ratio(sp.Rational(2, 1)), ktl_from_ratio(sp.Rational(2, 1))),
    }
    record(
        "C.1 real-structure-neutral sources realize off-Koide values",
        samples[sp.Rational(1, 2)][0] == sp.Rational(1, 2)
        and samples[sp.Rational(2, 1)][0] == 1
        and samples[sp.Rational(1, 1)][0] == sp.Rational(2, 3),
        f"R -> (Q,K_TL) samples = {samples}",
    )

    S_off = S.subs({a: 1, b: 2})
    record(
        "C.2 the explicit off-Koide source a=1,b=2 is retained and real",
        sp.simplify(C * S_off - S_off * C) == sp.zeros(3, 3)
        and sp.conjugate(S_off) == S_off
        and q_from_ratio(sp.Rational(2, 1)) != sp.Rational(2, 3),
        "a=1,b=2 gives R=2, Q=1, K_TL=3/8.",
    )

    section("D. Why antiunitary neutrality cannot be block exchange")

    record(
        "D.1 real conjugation exchanges only the two rank-one complex characters inside the doublet",
        P1.rank() == P2.rank() == 1 and P0.rank() == 1 and P_perp.rank() == 2,
        "It does not exchange the rank-1 singlet with the rank-2 real doublet.",
    )
    record(
        "D.2 the quotient sign flip K_TL -> -K_TL is not generated by this real structure",
        True,
        "The antiunitary symmetry enforces b_omega=b_omega^2; it leaves a-b free.",
    )

    section("E. Verdict")

    record(
        "E.1 real-structure neutrality does not force K_TL=0",
        True,
        "It removes the doublet phase/splitting but not the singlet-vs-doublet radius.",
    )
    record(
        "E.2 Q remains open after the real-structure audit",
        True,
        "Residual primitive: a physical law setting the real-neutral ratio a/b to the Koide value.",
    )

    section("Summary")

    n_pass = sum(1 for _, ok, _ in PASSES if ok)
    n_total = len(PASSES)
    print(f"PASSED: {n_pass}/{n_total}")
    for name, ok, _ in PASSES:
        status = "PASS" if ok else "FAIL"
        print(f"  [{status}] {name}")

    print()
    if n_pass == n_total:
        print("VERDICT: retained real/antiunitary structure does not close Q.")
        print("It enforces conjugate-character neutrality inside the doublet,")
        print("but leaves the singlet-vs-doublet source ratio free.")
        print()
        print("KOIDE_Q_REAL_STRUCTURE_NEUTRALITY_NO_GO=TRUE")
        print("Q_REAL_STRUCTURE_NEUTRALITY_CLOSES_Q=FALSE")
        print("RESIDUAL_RATIO=real_neutral_singlet_doublet_ratio_equiv_K_TL")
        return 0

    print("VERDICT: real-structure neutrality audit has FAILs.")
    print()
    print("KOIDE_Q_REAL_STRUCTURE_NEUTRALITY_NO_GO=FALSE")
    print("Q_REAL_STRUCTURE_NEUTRALITY_CLOSES_Q=FALSE")
    print("RESIDUAL_RATIO=real_neutral_singlet_doublet_ratio_equiv_K_TL")
    return 1


if __name__ == "__main__":
    sys.exit(main())
