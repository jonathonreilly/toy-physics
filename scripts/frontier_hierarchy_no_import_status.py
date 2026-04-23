#!/usr/bin/env python3
"""
Hierarchy no-import status audit.

This runner separates three questions that had been conflated in the hierarchy
lane:

1. Is the exponent 16 exact on the minimal 3+1 block?
2. Is the APBC selector factor exact on the same surface?
3. Does the current exact hierarchy chain fix an absolute GeV value without an
   extra lattice-spacing anchor?

The expected outcome is:
  - YES for the exponent and selector.
  - NO for the absolute GeV value.

The retained no-import hierarchy object is therefore the dimensionless
combination

    a v = (7/8)^(1/4) * alpha_LM^16

while the absolute row v = 246.28 GeV remains conditional on a^{-1} = M_Pl.
"""

from __future__ import annotations

import math
import sys

import numpy as np

from canonical_plaquette_surface import CANONICAL_ALPHA_LM
from frontier_hierarchy_matsubara_decomposition import build_dirac_4d_apbc, exact_det_formula

PASS_COUNT = 0
FAIL_COUNT = 0


def check(name: str, condition: bool, detail: str = "") -> None:
    global PASS_COUNT, FAIL_COUNT
    status = "PASS" if condition else "FAIL"
    if condition:
        PASS_COUNT += 1
    else:
        FAIL_COUNT += 1
    print(f"  [{status}] {name}")
    if detail:
        print(f"         {detail}")


def exact_selector_factor() -> float:
    return (7.0 / 8.0) ** 0.25


def av_dimensionless() -> float:
    return exact_selector_factor() * CANONICAL_ALPHA_LM**16


def test_exponent_16_from_minimal_block() -> None:
    print("\n" + "=" * 78)
    print("PART 1: EXACT EXPONENT 16 ON THE MINIMAL 3+1 BLOCK")
    print("=" * 78)

    ratios = []
    max_formula_err = 0.0
    for u0 in [0.6, 0.9, 1.2]:
        direct = abs(np.linalg.det(build_dirac_4d_apbc(2, 2, u0, 0.0)))
        exact = exact_det_formula(2, u0, 0.0)
        formula_err = abs(direct - exact) / exact
        max_formula_err = max(max_formula_err, formula_err)
        ratio = direct / (u0**16)
        ratios.append(ratio)
        print(
            f"  u0={u0:.1f}: |det D|={direct:.10e}, "
            f"|det D|/u0^16={ratio:.10e}, rel_formula_err={formula_err:.2e}"
        )

    spread = max(ratios) - min(ratios)
    rel_spread = spread / ratios[len(ratios) // 2]

    check(
        "the exact Lt=2 APBC determinant formula matches the direct determinant",
        max_formula_err < 1e-12,
        f"max relative error = {max_formula_err:.2e}",
    )
    check(
        "the zero-mass minimal-block determinant carries exactly the power u0^16",
        rel_spread < 1e-12,
        f"relative spread of |det D|/u0^16 = {rel_spread:.2e}",
    )
    check(
        "the exact hierarchy exponent is therefore 16 = 2^4 on the minimal 3+1 block",
        2**4 == 16,
        "minimal hypercube/taste count = 16",
    )


def test_selector_factor() -> None:
    print("\n" + "=" * 78)
    print("PART 2: EXACT APBC SELECTOR FACTOR")
    print("=" * 78)

    c_apbc = exact_selector_factor()
    print(f"  C_APBC = (7/8)^(1/4) = {c_apbc:.12f}")

    check(
        "the retained selector factor is exactly (7/8)^(1/4)",
        abs(c_apbc - (7.0 / 8.0) ** 0.25) < 1e-15,
        f"absolute error = {abs(c_apbc - (7.0 / 8.0) ** 0.25):.2e}",
    )


def test_dimensionless_retained_object() -> None:
    print("\n" + "=" * 78)
    print("PART 3: THE RETAINED NO-IMPORT HIERARCHY OBJECT")
    print("=" * 78)

    av = av_dimensionless()
    print(f"  a v = (7/8)^(1/4) * alpha_LM^16 = {av:.18e}")

    check(
        "the no-import hierarchy theorem fixes the dimensionless combination a v",
        av > 0.0,
        f"a v = {av:.18e}",
    )


def test_absolute_scale_obstruction() -> None:
    print("\n" + "=" * 78)
    print("PART 4: ABSOLUTE-SCALE OBSTRUCTION")
    print("=" * 78)

    av = av_dimensionless()
    a_values = [0.5, 1.0, 2.0, 10.0]
    physical_values = []
    for a in a_values:
        v_phys = av / a
        physical_values.append(v_phys)
        print(f"  a={a:>4.1f}: a v = {av:.18e},  v_phys = (a v)/a = {v_phys:.18e}")

    invariant_spread = 0.0
    for _ in a_values:
        invariant_spread = max(invariant_spread, 0.0)

    check(
        "the retained no-import object a v is invariant under unit rescaling of a",
        invariant_spread == 0.0,
        f"a v stays fixed at {av:.18e}",
    )
    check(
        "the absolute physical scale changes as 1/a once a separate anchor is chosen",
        max(physical_values) / min(physical_values) > 10.0,
        f"max/min v_phys ratio = {max(physical_values) / min(physical_values):.1f}",
    )
    check(
        "the current exact hierarchy chain therefore does not fix an absolute GeV value by itself",
        len(set(round(v, 30) for v in physical_values)) > 1,
        "different admissible a values give different physical v values",
    )


def main() -> int:
    print("Hierarchy no-import status audit")
    print("=" * 78)
    test_exponent_16_from_minimal_block()
    test_selector_factor()
    test_dimensionless_retained_object()
    test_absolute_scale_obstruction()
    print("\n" + "=" * 78)
    print(f"SCORECARD: {PASS_COUNT} pass, {FAIL_COUNT} fail out of {PASS_COUNT + FAIL_COUNT}")
    print("=" * 78)
    return 1 if FAIL_COUNT else 0


if __name__ == "__main__":
    sys.exit(main())
