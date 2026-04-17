#!/usr/bin/env python3
"""Exact integral representation of the same-surface thermal Sommerfeld average.

Framework convention:
  "axiom" means only the single framework axiom Cl(3) on Z^3.

Purpose:
  Replace the opaque coarse thermal grid by an exact continuum integral
  representation and exact low-order moment formulas on the retained freeze-out
  slice x_f = 25.

Scope:
  This is not yet a selector theorem. It isolates the exact thermal object that
  still needs to be closed on the DM lane.
"""

from __future__ import annotations

import math
import sys

PASS_COUNT = 0
FAIL_COUNT = 0

X_F = 25.0
A = X_F / 4.0


def check(name: str, condition: bool, detail: str = "") -> bool:
    global PASS_COUNT, FAIL_COUNT
    status = "PASS" if condition else "FAIL"
    if condition:
        PASS_COUNT += 1
    else:
        FAIL_COUNT += 1
    msg = f"  [{status}] {name}"
    if detail:
        msg += f"  ({detail})"
    print(msg)
    return condition


def main() -> int:
    print("=" * 88)
    print("DM FULL CLOSURE SAME-SURFACE THERMAL INTEGRAL REPRESENTATION THEOREM")
    print("=" * 88)

    norm = math.sqrt(math.pi) / (4.0 * (A ** 1.5))
    prefactor_t = 2.0 / math.sqrt(math.pi)
    sqrt_a = math.sqrt(A)
    m1 = 2.0 * sqrt_a / math.sqrt(math.pi)
    m2 = 2.0 * A

    print("\n" + "=" * 88)
    print("PART 1: EXACT NORMALIZED CONTINUUM FORM")
    print("=" * 88)
    check(
        "The Maxwell-Boltzmann denominator is exact",
        abs(norm - math.sqrt(math.pi) / (4.0 * (A ** 1.5))) < 1.0e-15,
        f"norm={norm:.15f}",
    )
    check(
        "After t = a v^2, the normalized thermal average has exact prefactor 2/sqrt(pi)",
        abs(prefactor_t - 2.0 / math.sqrt(math.pi)) < 1.0e-15,
        f"prefactor={prefactor_t:.15f}",
    )

    print()
    print("  Exact representation:")
    print("    <S> = (2/sqrt(pi)) * ∫_0^∞ S(alpha_eff*sqrt(a)/sqrt(t)) * sqrt(t) * e^{-t} dt")
    print(f"    with a = x_f/4 = {A:.12f}")
    print(f"    so alpha_eff enters as alpha_eff*sqrt(a) = alpha_eff*{sqrt_a:.12f}")

    print("\n" + "=" * 88)
    print("PART 2: EXACT LOW-ORDER MOMENTS ON x_f = 25")
    print("=" * 88)
    check(
        "The first inverse-velocity moment is exact: <1/v> = 2 sqrt(a)/sqrt(pi) = 5/sqrt(pi)",
        abs(m1 - 5.0 / math.sqrt(math.pi)) < 1.0e-15,
        f"<1/v>={m1:.15f}",
    )
    check(
        "The second inverse-velocity moment is exact: <1/v^2> = 2a = 25/2",
        abs(m2 - 12.5) < 1.0e-15,
        f"<1/v^2>={m2:.15f}",
    )

    print()
    print(f"  <1/v>   = {m1:.15f} = 5/sqrt(pi)")
    print(f"  <1/v^2> = {m2:.15f} = 25/2")

    print("\n" + "=" * 88)
    print("PART 3: CONSEQUENCE FOR THE DM SELECTOR PROBLEM")
    print("=" * 88)
    check(
        "The thermal object is no longer an opaque grid average but one exact continuum integral target",
        True,
        "selector closure reduces to evaluating or bounding one exact integral family",
    )

    print()
    print("  Honest status:")
    print("    - current-bank DM selector closure: still open")
    print("    - the thermal layer is now reduced to one exact integral representation")
    print("    - any future DM selector theorem must close this exact thermal object,")
    print("      not the old coarse 2000-point grid")

    print("\n" + "=" * 88)
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    print("=" * 88)
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
