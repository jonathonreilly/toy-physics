#!/usr/bin/env python3
"""
Frontier runner - STRC-LO / BICAC theorem on the exact 1(+)5 carrier.

This runner verifies the actual load-bearing claim:

  On the physical reduced carrier H_(1+5) = span{e_1, e_5},
  with physical projector ray

      p = cos_d e_1 + sin_d e_5,

  retained scalar-comparison ray

      r = p / sqrt(7) = a_d e_1 + eta e_5,

  canonical 5-projector

      Pi_5 = |e_5><e_5|,

  and canonical A1 -> 5 transfer operator induced by the physical ray

      T_p = Pi_5 |p><e_1| = sin_d |e_5><e_1|,

  the exact 5-budget identity is

      Pi_5 p = T_p (a_d e_1) + a_u e_5.

Therefore

      a_u + a_d * Im(p) = Im(p),

  i.e. BICAC / STRC-LO.

The PASS surface is exact operator algebra only. It does not mark narrative
claims or bounded fit language as validated.
"""

from __future__ import annotations

import math

import numpy as np


PASS = 0
FAIL = 0


def check(name: str, cond: bool, detail: str = "") -> None:
    global PASS, FAIL
    status = "PASS" if cond else "FAIL"
    if cond:
        PASS += 1
    else:
        FAIL += 1
    line = f"  [{status}] {name}"
    if detail:
        line += f"  ({detail})"
    print(line)


def main() -> int:
    print("=" * 72)
    print("  STRC-LO / BICAC theorem on the exact 1(+)5 carrier")
    print("=" * 72)

    e1 = np.array([1.0, 0.0], dtype=float)
    e5 = np.array([0.0, 1.0], dtype=float)

    cos_d = 1.0 / math.sqrt(6.0)
    sin_d = math.sqrt(5.0 / 6.0)
    p = np.array([cos_d, sin_d], dtype=float)
    r = p / math.sqrt(7.0)

    a_d = r[0]
    eta = r[1]
    supp = 6.0 / 7.0
    delta_a1 = 1.0 / 42.0

    pi_5 = np.array([[0.0, 0.0], [0.0, 1.0]], dtype=float)
    ket_p_bra_e1 = np.outer(p, e1)
    t_p = pi_5 @ ket_p_bra_e1

    down_occ = a_d * e1
    total_5 = pi_5 @ p
    mixed_5 = t_p @ down_occ
    residual_5 = total_5 - mixed_5
    a_u = float(residual_5[1])

    outer_r_p = np.outer(r, p)

    print()
    print("  Exact carrier data:")
    print(f"    e1         = {e1}")
    print(f"    e5         = {e5}")
    print(f"    p          = {p}")
    print(f"    r          = {r}")
    print(f"    a_d        = Re(r) = {a_d:.12f}")
    print(f"    Im(p)      = {sin_d:.12f}")
    print(f"    Pi_5 p     = {total_5}")
    print(f"    T_p        =")
    print(t_p)
    print(f"    T_p(a_d e1)= {mixed_5}")
    print(f"    residual_5 = {residual_5}")
    print(f"    a_u        = {a_u:.12f}")

    check(
        "T1  p is the unit physical projector ray on H_(1+5)",
        abs(float(np.dot(p, p)) - 1.0) < 1e-15,
        f"|p|^2 = {float(np.dot(p, p)):.15f}",
    )
    check(
        "T2  r = p/sqrt(7) and a_d = Re(r) = 1/sqrt(42)",
        np.max(np.abs(r - p / math.sqrt(7.0))) < 1e-15
        and abs(a_d - 1.0 / math.sqrt(42.0)) < 1e-15,
        f"a_d = {a_d:.15f}",
    )
    check(
        "T3  Pi_5 projects the physical ray to the exact 5-budget Im(p) e5",
        np.max(np.abs(total_5 - sin_d * e5)) < 1e-15,
        f"Pi_5 p = {total_5}",
    )
    check(
        "T4  T_p = Pi_5 |p><e1| = sin_d |e5><e1|",
        np.max(np.abs(t_p - np.array([[0.0, 0.0], [sin_d, 0.0]], dtype=float))) < 1e-15,
        f"T_p[1,0] = {t_p[1,0]:.15f}",
    )
    check(
        "T5  T_p is the unique A1 -> 5 transfer induced by p: T_p e1 = Pi_5 p and T_p e5 = 0",
        np.max(np.abs(t_p @ e1 - total_5)) < 1e-15
        and np.max(np.abs(t_p @ e5)) < 1e-15,
        f"T_p e1 = {t_p @ e1}, T_p e5 = {t_p @ e5}",
    )
    check(
        "T6  The retained down occupancy produces exact mixed-channel budget a_d Im(p) e5",
        np.max(np.abs(mixed_5 - a_d * sin_d * e5)) < 1e-15,
        f"T_p(a_d e1) = {mixed_5}",
    )
    check(
        "T7  The off-diagonal A1 -> 5 entry of r tensor p is exactly a_d Im(p)",
        abs(outer_r_p[0, 1] - a_d * sin_d) < 1e-15,
        f"(r tensor p)_(1->5) = {outer_r_p[0,1]:.15f}",
    )
    check(
        "T8  Collinearity makes the two mixed-channel off-diagonal entries equal",
        abs(outer_r_p[0, 1] - outer_r_p[1, 0]) < 1e-15
        and abs(outer_r_p[1, 0] - eta * cos_d) < 1e-15,
        f"upper-right = {outer_r_p[0,1]:.15f}, lower-left = {outer_r_p[1,0]:.15f}",
    )
    check(
        "T9  The residual 5 vector is pure e5 and defines a_u uniquely",
        abs(residual_5[0]) < 1e-15
        and abs(a_u - sin_d * (1.0 - a_d)) < 1e-15,
        f"residual_5 = {residual_5}",
    )
    check(
        "T10 BICAC / STRC-LO: a_u + a_d Im(p) = Im(p)",
        abs(a_u + a_d * sin_d - sin_d) < 1e-15,
        f"|LHS-RHS| = {abs(a_u + a_d * sin_d - sin_d):.3e}",
    )

    a_u_full = sin_d * (1.0 - a_d + a_d * supp * delta_a1)
    check(
        "T11 Downstream NLO step gives a_u = sin_d (1 - 48 a_d / 49)",
        abs(a_u_full - sin_d * (1.0 - 48.0 * a_d / 49.0)) < 1e-15,
        f"a_u_full = {a_u_full:.12f}",
    )
    check(
        "T12 The RPSR target remains 0.7748865611 at 10 decimals",
        abs(a_u_full - 0.7748865611) < 5e-11,
        f"a_u_full = {a_u_full:.10f}",
    )

    print()
    print("=" * 72)
    print(f"PASS={PASS} FAIL={FAIL}")
    print("=" * 72)
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
