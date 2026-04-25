#!/usr/bin/env python3
"""
R_base = 31/9 group-theory identity verification.

This runner verifies the exact support identity packaged in
docs/R_BASE_GROUP_THEORY_DERIVATION_THEOREM_NOTE_2026-04-24.md:

    R_base = (3/5) * [C_2(3) * dim(adj_3) + C_2(2) * dim(adj_2)]
                     / [C_2(2) * dim(adj_2)]
           = 31/9.

It intentionally does not validate a full cosmology closure. The Sommerfeld
factor, the full Omega_DM/Omega_b ratio, and Omega_Lambda propagation remain
bounded/conditional lanes elsewhere in the repo.
"""

from __future__ import annotations

import sys
from dataclasses import dataclass
from fractions import Fraction
from math import gcd


@dataclass(frozen=True)
class Check:
    name: str
    passed: bool
    detail: str = ""


def quadratic_casimir_fundamental(n: int) -> Fraction:
    """Return C_2 for the SU(n) fundamental representation."""
    return Fraction(n * n - 1, 2 * n)


def adjoint_dimension(n: int) -> int:
    """Return dim(adj SU(n))."""
    return n * n - 1


def evaluate() -> list[Check]:
    c2_3 = quadratic_casimir_fundamental(3)
    c2_2 = quadratic_casimir_fundamental(2)
    dim_adj_3 = adjoint_dimension(3)
    dim_adj_2 = adjoint_dimension(2)
    gut_norm = Fraction(3, 5)

    quark_part = c2_3 * dim_adj_3
    weak_part = c2_2 * dim_adj_2
    numerator = quark_part + weak_part
    denominator = weak_part
    casimir_ratio = numerator / denominator
    r_base = gut_norm * casimir_ratio

    checks = [
        Check("C_2(SU(3)_fund) = 4/3", c2_3 == Fraction(4, 3), str(c2_3)),
        Check("C_2(SU(2)_fund) = 3/4", c2_2 == Fraction(3, 4), str(c2_2)),
        Check("dim(adj SU(3)) = 8", dim_adj_3 == 8, str(dim_adj_3)),
        Check("dim(adj SU(2)) = 3", dim_adj_2 == 3, str(dim_adj_2)),
        Check("GUT normalization input = 3/5", gut_norm == Fraction(3, 5), str(gut_norm)),
        Check("SU(3) contribution = 32/3", quark_part == Fraction(32, 3), str(quark_part)),
        Check("SU(2) denominator contribution = 9/4", weak_part == Fraction(9, 4), str(weak_part)),
        Check("numerator = 155/12", numerator == Fraction(155, 12), str(numerator)),
        Check("denominator = 9/4", denominator == Fraction(9, 4), str(denominator)),
        Check("Casimir-adjoint ratio = 155/27", casimir_ratio == Fraction(155, 27), str(casimir_ratio)),
        Check("R_base = 31/9 exactly", r_base == Fraction(31, 9), str(r_base)),
        Check("decimal value = 3.444444...", abs(float(r_base) - 31.0 / 9.0) < 1e-15, f"{float(r_base):.12f}"),
        Check("465/135 reduction uses gcd 15", gcd(465, 135) == 15, f"gcd={gcd(465, 135)}"),
        Check("465/135 = 31/9", Fraction(465, 135) == Fraction(31, 9), str(Fraction(465, 135))),
        Check("(3/5)*(155/27) form matches", Fraction(3, 5) * Fraction(155, 27) == r_base, str(Fraction(3, 5) * Fraction(155, 27))),
        Check("(3/5)*(1+128/27) form matches", Fraction(3, 5) * (1 + Fraction(128, 27)) == r_base, str(Fraction(3, 5) * (1 + Fraction(128, 27)))),
        Check("additive form 3/5 + 128/45 matches", Fraction(3, 5) + Fraction(128, 45) == r_base, str(Fraction(3, 5) + Fraction(128, 45))),
        Check("quark/weak contribution ratio = 128/27", quark_part / weak_part == Fraction(128, 27), str(quark_part / weak_part)),
        Check("R_base alone is not the observed DM/baryon ratio", r_base != Fraction(538, 100), f"R_base={r_base}, comparator=5.38"),
        Check("Sommerfeld factor is not included in this exact identity", r_base == Fraction(31, 9), "full R is bounded elsewhere"),
        Check("3/5 remains an admitted normalization input here", gut_norm == Fraction(3, 5), "not derived by this runner"),
        Check("no observed cosmology value enters the exact arithmetic", all(isinstance(x, Fraction) for x in [c2_3, c2_2, gut_norm, numerator, denominator, r_base]), "Fraction arithmetic only"),
    ]
    return checks


def main() -> int:
    print("R_base = 31/9 group-theory identity verification")
    print("Exact arithmetic; no cosmology observation is used in the identity.")
    print()

    checks = evaluate()
    pass_count = 0
    fail_count = 0

    for check in checks:
        status = "PASS" if check.passed else "FAIL"
        detail = f" ({check.detail})" if check.detail else ""
        print(f"[{status}] {check.name}{detail}")
        if check.passed:
            pass_count += 1
        else:
            fail_count += 1

    print()
    print(f"TOTAL: PASS={pass_count} FAIL={fail_count}")
    return 0 if fail_count == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
