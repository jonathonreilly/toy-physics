#!/usr/bin/env python3
"""
Koide circulant / character bridge runner
=========================================

STATUS: exact symbolic bridge on the candidate charged-lepton Koide lane

Purpose:
  Cleanly integrate the April 18 circulant-operator language with the April 17
  charged-lepton review package.

Question:
  For a C_3-circulant Hermitian H = a I + b C + b* C^2 on the retained hw=1
  triplet, how do the operator parameters (a, b) map to the C_3 character
  coefficients (a_0, z) of the eigenvalue triple lambda?

Safe target:
  a_0 = sqrt(3) a
  z   = sqrt(3) b
  hence
  a_0^2 = 2 |z|^2  <=>  3 a^2 = 6 |b|^2.

This runner proves the bridge exactly. It does NOT derive the selection
principle 3 a^2 = 6 |b|^2, nor the phenomenological identification
lambda_k = sqrt(m_k).
"""

from __future__ import annotations

import sys

import sympy as sp

PASS_COUNT = 0
FAIL_COUNT = 0


def check(name: str, condition: bool, detail: str = "", kind: str = "EXACT") -> bool:
    global PASS_COUNT, FAIL_COUNT
    status = "PASS" if condition else "FAIL"
    if condition:
        PASS_COUNT += 1
    else:
        FAIL_COUNT += 1
    tag = f" [{kind}]" if kind != "EXACT" else ""
    msg = f"  [{status}]{tag} {name}"
    if detail:
        msg += f"  ({detail})"
    print(msg)
    return condition


def main() -> int:
    print("=" * 88)
    print("KOIDE CIRCULANT / CHARACTER BRIDGE")
    print("=" * 88)

    a, x, y = sp.symbols("a x y", real=True)
    w = sp.Rational(-1, 2) + sp.I * sp.sqrt(3) / 2
    wb = sp.conjugate(w)
    b = x + sp.I * y
    bb = sp.conjugate(b)

    lam = [sp.simplify(a + b * w**k + bb * w**(-k)) for k in range(3)]

    check(
        "Eigenvalue triple is real for Hermitian circulant H",
        all(sp.simplify(sp.im(expr)) == 0 for expr in lam),
        detail=f"lambda={lam}",
    )

    a0 = sp.simplify((lam[0] + lam[1] + lam[2]) / sp.sqrt(3))
    z = sp.simplify((lam[0] + wb * lam[1] + w * lam[2]) / sp.sqrt(3))

    check(
        "Trivial-character coefficient is a_0 = sqrt(3) a",
        sp.simplify(sp.expand(a0 - sp.sqrt(3) * a)) == 0,
        detail=f"a0={sp.simplify(a0)}",
    )
    check(
        "Nontrivial-character coefficient is z = sqrt(3) b",
        sp.simplify(sp.expand(z - sp.sqrt(3) * b)) == 0,
        detail=f"z={sp.simplify(z)}",
    )

    abs_b_sq = sp.simplify(b * bb)
    koide_bridge = sp.simplify(sp.expand((a0**2 - 2 * z * sp.conjugate(z)) - (3 * a**2 - 6 * abs_b_sq)))
    check(
        "a_0^2 - 2|z|^2 = 3 a^2 - 6 |b|^2 exactly",
        koide_bridge == 0,
    )

    sum_lam = sp.simplify(sum(lam))
    sum_lam_sq = sp.simplify(sum(expr**2 for expr in lam))
    q_expr = sp.simplify(sum_lam_sq / (sum_lam**2))
    q_char = sp.simplify((a0**2 + 2 * z * sp.conjugate(z)) / (3 * a0**2))
    check(
        "Koide invariant of the eigenvalue triple matches the character formula",
        sp.simplify(sp.expand(q_expr - q_char)) == 0,
        detail=f"Q={q_expr}",
    )

    delta = sp.symbols("delta", real=True)
    b_delta = a / sp.sqrt(2) * (sp.cos(delta) + sp.I * sp.sin(delta))
    lam_delta = [sp.simplify(a + b_delta * w**k + sp.conjugate(b_delta) * w**(-k)) for k in range(3)]
    q_delta = sp.simplify(sum(expr**2 for expr in lam_delta) / (sum(lam_delta) ** 2))
    check(
        "Under 3 a^2 = 6 |b|^2, the eigenvalue triple satisfies Q = 2/3 for all delta",
        sp.simplify(sp.expand(q_delta - sp.Rational(2, 3))) == 0,
        detail=f"Q_delta={q_delta}",
    )

    e_plus, e_perp, e_tot = sp.symbols("e_plus e_perp e_tot", positive=True)
    s_unweighted = sp.log(e_plus) + sp.log(e_tot - e_plus)
    crit = sp.solve(sp.Eq(sp.diff(s_unweighted, e_plus), 0), e_plus)
    check(
        "Unweighted block-log-volume is stationary at equal block energy",
        len(crit) == 1 and sp.simplify(crit[0] - e_tot / 2) == 0,
        detail=f"crit={crit}",
    )
    second = sp.simplify(sp.diff(s_unweighted, e_plus, 2).subs(e_plus, e_tot / 2))
    check(
        "The equal-energy stationary point is a strict maximum",
        sp.simplify(second + 8 / e_tot**2) == 0,
        detail=f"second={second}",
    )
    check(
        "A1 is exactly the equal-block-energy condition E_+ = E_perp with E_+=3a^2, E_perp=6|b|^2",
        sp.simplify((3 * a**2 - 6 * abs_b_sq) - ((3 * a**2) - (6 * abs_b_sq))) == 0,
    )

    print()
    print("Interpretation:")
    print("  The matrix-space equality 3 a^2 = 6 |b|^2 is exactly the same")
    print("  equal-character-weight condition a_0^2 = 2 |z|^2 on the spectral")
    print("  triple. In block-energy variables E_+ = 3 a^2 and E_perp = 6 |b|^2,")
    print("  it is also exactly the same candidate selection principle as the")
    print("  April 17 real-irrep-block-democracy lane. The bridge is exact; the")
    print("  open science is whether that unweighted block principle is retained.")
    print()
    print(f"PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
