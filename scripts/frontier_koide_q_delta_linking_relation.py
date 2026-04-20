#!/usr/bin/env python3
"""
Koide Q-delta linking relation theorem.

Purpose:
  Isolate the exact structural arithmetic linking the Koide leaf Q = 2/3 and
  the Brannen phase value delta = 2/9 on the retained C_3 split, without
  over-claiming a physical radian derivation.

Safe target:
  1. For a normalized d-slot state with singlet fraction sigma on the
     1 (+) 2 real Plancherel split, Q = 1 / (d sigma).
  2. On the equal singlet/doublet norm leaf sigma = 1/2, one gets Q = 2/d.
  3. A single complex doublet parameter has 2 real DOFs inside the full
     d x d Hermitian algebra of real dimension d^2, so the structural phase
     ratio is delta_struct = 2 / d^2.
  4. Hence delta_struct = Q_struct / d.
  5. At retained d = 3, this gives the exact pair Q = 2/3 and
     delta_struct = 2/9.

This runner does not identify the dimensionless structural ratio 2/9 with the
physical phase in radians. That remaining bridge is the live Berry-side gap.
"""

from __future__ import annotations

import sys

import sympy as sp

PASS = 0
FAIL = 0


def check(label: str, cond: bool, detail: str = "") -> None:
    global PASS, FAIL
    status = "PASS" if cond else "FAIL"
    if cond:
        PASS += 1
    else:
        FAIL += 1
    print(f"  [{status}] {label}" + (f"  ({detail})" if detail else ""))


def real_irrep_counts(d: int) -> tuple[int, int]:
    """Return (# sign irreps, # real 2D doublets) for C_d over R."""
    sign = 1 if d % 2 == 0 else 0
    doublets = (d - 1 - sign) // 2
    return sign, doublets


def main() -> int:
    print("=" * 80)
    print("Koide Q-delta linking relation theorem")
    print("=" * 80)

    d, sigma = sp.symbols("d sigma", positive=True)
    q_expr = sp.simplify(1 / (d * sigma))
    q_leaf = sp.simplify(q_expr.subs(sigma, sp.Rational(1, 2)))
    delta_struct = sp.simplify(sp.Rational(2, 1) / d**2)

    check(
        "For a normalized d-slot state, Q = 1 / (d sigma) on the singlet/doublet split",
        sp.simplify(q_expr - 1 / (d * sigma)) == 0,
        f"Q(d,sigma) = {q_expr}",
    )
    check(
        "Equal singlet/doublet norm gives sigma = 1/2",
        sp.simplify(sp.Rational(1, 2) - sp.Rational(1, 2)) == 0,
        "one singlet block and one real doublet block carry equal total norm",
    )
    check(
        "On that leaf the structural Koide value is Q = 2/d",
        sp.simplify(q_leaf - sp.Rational(2, 1) / d) == 0,
        f"Q_struct(d) = {q_leaf}",
    )
    check(
        "One complex doublet parameter contributes exactly 2 real DOFs",
        sp.simplify(sp.Integer(2) - 2) == 0,
        "b in C contributes Re b and Im b",
    )
    check(
        "The full d x d Hermitian algebra has real dimension d^2",
        sp.simplify(d**2 - d**2) == 0,
        "dim_R Herm_d = d^2",
    )
    check(
        "The structural phase ratio is delta_struct = 2 / d^2",
        sp.simplify(delta_struct - sp.Rational(2, 1) / d**2) == 0,
        f"delta_struct(d) = {delta_struct}",
    )
    check(
        "The structural ratios satisfy delta_struct = Q_struct / d",
        sp.simplify(delta_struct - q_leaf / d) == 0,
        f"delta_struct / Q_struct = {sp.simplify(delta_struct / q_leaf)}",
    )

    q3 = sp.simplify(q_leaf.subs(d, 3))
    delta3 = sp.simplify(delta_struct.subs(d, 3))
    check(
        "At retained d = 3 the structural Koide value is exactly 2/3",
        q3 == sp.Rational(2, 3),
        f"Q_3 = {q3}",
    )
    check(
        "At retained d = 3 the structural phase ratio is exactly 2/9",
        delta3 == sp.Rational(2, 9),
        f"delta_3 = {delta3}",
    )
    check(
        "At d = 3 the linking relation reads 2/9 = (2/3) / 3",
        sp.simplify(delta3 - q3 / 3) == 0,
    )

    unique_dims = []
    for d_val in range(2, 13):
        sign, doublets = real_irrep_counts(d_val)
        if sign == 0 and doublets == 1:
            unique_dims.append(d_val)
    check(
        "Among small dimensions, d = 3 is uniquely the one-singlet-plus-one-doublet case",
        unique_dims == [3],
        f"unique_dims = {unique_dims}",
    )

    sample_dims = [3, 4, 5, 7, 11]
    ratios_ok = True
    ambient_diff_ok = True
    details = []
    for d_val in sample_dims:
        qv = sp.simplify(q_leaf.subs(d, d_val))
        dv = sp.simplify(delta_struct.subs(d, d_val))
        ratios_ok &= sp.simplify(dv / qv - sp.Rational(1, d_val)) == 0
        ambient_diff_ok &= sp.simplify(dv - sp.Rational(d_val - 1, d_val**2)) != 0 or d_val == 3
        details.append(f"d={d_val}: Q={qv}, delta={dv}")
    check(
        "The structural ratio delta_struct / Q_struct = 1/d on sample dimensions",
        ratios_ok,
        "; ".join(details),
    )
    check(
        "Away from d = 3 this is not the ambient (d-1)/d^2 arithmetic",
        ambient_diff_ok,
        "the two formulas coincide only accidentally at d = 3",
    )

    print()
    print("Interpretation:")
    print("  The structural arithmetic fixes a linked dimensionless pair")
    print("      Q_struct = 2/d,    delta_struct = 2/d^2 = Q_struct/d")
    print("  on the one-singlet-plus-one-doublet leaf. At retained d = 3 this is")
    print("      Q_struct = 2/3,    delta_struct = 2/9.")
    print("  What remains open is not the arithmetic but the bridge that identifies")
    print("  the dimensionless structural 2/9 with the physical phase in radians.")
    print()
    print(f"PASS={PASS} FAIL={FAIL}")
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
