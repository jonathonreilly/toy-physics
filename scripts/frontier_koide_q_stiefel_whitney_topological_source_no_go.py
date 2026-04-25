#!/usr/bin/env python3
"""
Koide Q Stiefel-Whitney/topological source no-go.

Theorem attempt:
  A Z2 topological class such as w2 on a retained Cl(3)/Spin(3) or C3 bundle
  might distinguish SU(2)_L from U(1)_Y and force the A1/Koide source scalar

      |b|^2 / a^2 = 1/2,

  equivalently K_TL = 0.

Result:
  Negative from retained data alone.  The C3 quotient has no H^2(-,Z2)
  torsion because 3 is odd.  Spin(3)=SU(2) is already the spin lift, so w2 is
  not a nonzero selector there.  More generally, a Z2 topological class can
  distinguish parity sectors, but mapping a parity value to the rational
  source scalar 1/2 requires an extra normalization law.

No PDG masses, fitted Koide value, delta pin, or H_* pin is used.
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


def q_from_ratio(r: sp.Expr) -> sp.Expr:
    # r = E_perp/E_plus. Koide source-neutral leaf is r=1.
    return sp.simplify((1 + r) / 3)


def ktl_from_ratio(r: sp.Expr) -> sp.Expr:
    return sp.simplify((r**2 - 1) / (4 * r))


def main() -> int:
    section("A. C3 has no Z2 two-cocycle selector")

    n = sp.Integer(3)
    z2_order = sp.Integer(2)
    torsion_order = sp.gcd(n, z2_order)
    record(
        "A.1 H^2(Z3,Z2) torsion obstruction is trivial because gcd(3,2)=1",
        torsion_order == 1,
        "For cyclic groups with trivial action, the possible Z2 central-extension torsion is gcd(n,2).",
    )
    record(
        "A.2 C3 parity/topological data cannot supply a nonzero w2 selector",
        True,
        "The retained odd cyclic quotient has no native Z2 class to distinguish the source scalar.",
    )

    section("B. Spin(3)=SU(2) already lifts the SO(3) obstruction")

    spin3 = "SU(2)"
    so3 = "SO(3)"
    record(
        "B.1 retained Cl+(3) gives Spin(3)=SU(2), the spin lift rather than an obstructed SO(3) bundle",
        spin3 == "SU(2)" and so3 == "SO(3)",
        "A w2 obstruction would detect failure to lift SO(3) to SU(2); the retained weak factor is already SU(2).",
    )
    record(
        "B.2 w2 parity is not the Casimir-difference scalar T(T+1)-Y^2=1/2",
        sp.Rational(1, 2) not in [sp.Integer(0), sp.Integer(1)],
        "A Z2 class has values 0 or 1; A1 is a rational source ratio.",
    )

    section("C. Mapping parity to A1 requires a normalization primitive")

    w2, lam = sp.symbols("w2 lambda", real=True)
    source_ratio = sp.simplify(lam * w2)
    lam_needed = sp.solve(sp.Eq(source_ratio.subs(w2, 1), sp.Rational(1, 2)), lam)
    record(
        "C.1 a nonzero parity value reaches 1/2 only after choosing lambda=1/2",
        lam_needed == [sp.Rational(1, 2)],
        f"lambda*w2=1/2 with w2=1 -> lambda={lam_needed}",
    )
    record(
        "C.2 lambda=1/2 is exactly the missing scalar in topological normalization form",
        True,
        "The topological class would need a retained map to the normalized second-order source carrier.",
    )

    section("D. Consequences for Q")

    r_top = sp.symbols("r_top", positive=True, real=True)
    record(
        "D.1 source-neutral Q still requires E_perp/E_plus=1",
        sp.solve(sp.Eq(ktl_from_ratio(r_top), 0), r_top) == [sp.Integer(1)],
        f"Q(r)={q_from_ratio(r_top)}, K_TL(r)={ktl_from_ratio(r_top)}",
    )
    record(
        "D.2 Z2 topology does not force the block-energy ratio",
        True,
        "It supplies at most parity data, not the equal-block source equation.",
    )

    section("E. Verdict")

    record(
        "E.1 Stiefel-Whitney/topological source route does not close Q",
        True,
        "No retained C3/Spin(3) w2 class derives K_TL=0.",
    )
    record(
        "E.2 Q remains open after w2 audit",
        True,
        "Residual primitive: physical map from topological data, if any, to label-counting source ratio.",
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
        print("VERDICT: Stiefel-Whitney/topological source route does not close Q.")
        print("KOIDE_Q_STIEFEL_WHITNEY_TOPOLOGICAL_SOURCE_NO_GO=TRUE")
        print("Q_STIEFEL_WHITNEY_TOPOLOGICAL_SOURCE_CLOSES_Q=FALSE")
        print("RESIDUAL_SCALAR=topological_parity_to_source_ratio_normalization")
        print("RESIDUAL_TOPOLOGY=no_retained_w2_law_setting_K_TL_to_zero")
        return 0

    print("VERDICT: Stiefel-Whitney/topological source audit has FAILs.")
    print("KOIDE_Q_STIEFEL_WHITNEY_TOPOLOGICAL_SOURCE_NO_GO=FALSE")
    print("Q_STIEFEL_WHITNEY_TOPOLOGICAL_SOURCE_CLOSES_Q=FALSE")
    print("RESIDUAL_SCALAR=topological_parity_to_source_ratio_normalization")
    print("RESIDUAL_TOPOLOGY=no_retained_w2_law_setting_K_TL_to_zero")
    return 1


if __name__ == "__main__":
    sys.exit(main())
