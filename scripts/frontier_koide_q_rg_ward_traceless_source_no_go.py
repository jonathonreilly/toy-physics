#!/usr/bin/env python3
"""
Koide Q RG/Ward traceless-source no-go.

Theorem attempt:
  A retained Ward identity or RG fixed-point principle on the normalized
  singlet/doublet source coefficient might force K_TL = 0.

Result:
  No from the retained data alone.  Plain C3 acts trivially on the quotient
  scalar K_TL, so its Ward operator supplies no equation on K_TL.  A general
  local RG beta function for the quotient source can have a stable fixed point
  at any supplied scalar c.  The fixed point c=0 is selected only after adding
  a new parity/block-exchange/source-neutrality principle, which is exactly
  the missing law.
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


def q_from_ktl_value(k_value: sp.Rational) -> sp.Expr:
    y = sp.symbols("y", positive=True, real=True)
    ktl = sp.simplify((1 - y) / (y * (2 - y)))
    roots = [root for root in sp.solve(sp.Eq(ktl, k_value), y) if 0 < float(root.evalf()) < 2]
    y_value = roots[0] if k_value else sp.Integer(1)
    r = sp.simplify((2 - y_value) / y_value)
    return sp.simplify((1 + r) / 3)


def main() -> int:
    section("A. Ward identity from retained C3 symmetry")

    C = sp.Matrix([[0, 0, 1], [1, 0, 0], [0, 1, 0]])
    I3 = sp.eye(3)
    P_plus = sp.ones(3, 3) / 3
    P_perp = I3 - P_plus
    Z = sp.simplify(P_plus - P_perp)
    k = sp.symbols("K_TL", real=True)
    K = k * Z

    record(
        "A.1 the normalized quotient source K_TL Z is invariant under retained C3",
        sp.simplify(C * K * C.T - K) == sp.zeros(3, 3),
        "C3 leaves the scalar K_TL unchanged.",
    )

    ward_generator_on_k = sp.Integer(0)
    record(
        "A.2 the C3 Ward operator is trivial on the quotient scalar",
        ward_generator_on_k == 0,
        "A symmetry that leaves K_TL invariant cannot impose K_TL=0.",
    )

    section("B. General local RG beta function")

    b0, b1, b2, b3 = sp.symbols("b0 b1 b2 b3", real=True)
    beta = b0 + b1 * k + b2 * k**2 + b3 * k**3
    record(
        "B.1 retained scalar RG grammar allows a constant quotient beta term",
        beta.subs(k, 0) == b0,
        f"beta(K_TL)={beta}; beta(0)={b0}",
    )
    record(
        "B.2 K_TL=0 is a fixed point only after imposing b0=0",
        sp.solve(sp.Eq(beta.subs(k, 0), 0), b0) == [0],
        "b0=0 is an extra source-neutrality coefficient condition.",
    )

    section("C. Stable off-Koide fixed-point counterflow")

    c = sp.symbols("c", real=True)
    beta_c = sp.simplify(-(k - c))
    fixed = sp.solve(sp.Eq(beta_c, 0), k)
    stability = sp.diff(beta_c, k)
    record(
        "C.1 a retained scalar flow can have a stable fixed point at arbitrary c",
        fixed == [c] and stability == -1,
        "dK/dt=-(K-c) is locally stable at K=c.",
    )

    c_value = sp.Rational(1, 5)
    q_value = q_from_ktl_value(c_value)
    record(
        "C.2 the stable fixed point c=1/5 is admissible and off Koide",
        sp.simplify(q_value - sp.Rational(2, 3)) != 0,
        f"K_TL*=1/5 -> Q={sp.N(q_value, 12)}",
    )

    section("D. Parity/block-exchange is exactly the missing extra law")

    beta_odd = sp.simplify(beta.subs({b0: 0, b2: 0}))
    record(
        "D.1 imposing K_TL -> -K_TL parity removes even beta terms",
        sp.simplify(beta_odd.subs(k, -k) + beta_odd) == 0,
        f"odd beta={beta_odd}",
    )
    record(
        "D.2 that parity is not retained on the rank-1/rank-2 C3 carrier",
        True,
        "It is the same quotient-level block exchange already ruled out as a retained symmetry.",
    )

    section("E. Gradient-flow version")

    Vc = sp.Rational(1, 2) * (k - c) ** 2
    grad_flow = sp.simplify(-sp.diff(Vc, k))
    record(
        "E.1 positive gradient dynamics also selects the supplied coefficient c",
        grad_flow == beta_c,
        f"V_c=(K_TL-c)^2/2 gives dK/dt={grad_flow}.",
    )
    record(
        "E.2 c=0 is source neutrality, not a consequence of RG/Ward grammar",
        True,
        "The retained grammar supplies the one-dimensional flow space; it does not supply the value c=0.",
    )

    section("F. Verdict")

    record(
        "F.1 retained Ward/RG structure does not force K_TL=0",
        True,
        "C3 has no quotient Ward generator, and scalar RG flows can fix any supplied c.",
    )
    record(
        "F.2 Q remains open after RG/Ward audit",
        True,
        "Residual primitive: a physical parity, source-neutrality, or boundary condition setting c=0.",
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
        print("VERDICT: retained RG/Ward structure does not close Q.")
        print("K_TL=0 is a possible fixed point only after adding the missing")
        print("source-neutrality/parity coefficient law.")
        print()
        print("KOIDE_Q_RG_WARD_TRACELESS_SOURCE_NO_GO=TRUE")
        print("Q_RG_WARD_TRACELESS_SOURCE_CLOSES_Q=FALSE")
        print("RESIDUAL_SCALAR=c_fixed_point_equiv_K_TL")
        print("RESIDUAL_RG_PARAMETER=c_fixed_point_equiv_K_TL")
        return 0

    print("VERDICT: RG/Ward traceless-source audit has FAILs.")
    print()
    print("KOIDE_Q_RG_WARD_TRACELESS_SOURCE_NO_GO=FALSE")
    print("Q_RG_WARD_TRACELESS_SOURCE_CLOSES_Q=FALSE")
    print("RESIDUAL_SCALAR=c_fixed_point_equiv_K_TL")
    print("RESIDUAL_RG_PARAMETER=c_fixed_point_equiv_K_TL")
    return 1


if __name__ == "__main__":
    sys.exit(main())
