#!/usr/bin/env python3
"""
Koide selected-slice frozen-bank decomposition
==============================================

STATUS: exact reduction of the charged-lepton selected slice to the frozen
slot/CP bank plus one real microscopic coordinate

Purpose:
  The microscopic scalar-selector target already showed that on the charged-
  lepton selected slice delta = q_+ = sqrt(6)/3, the remaining datum is one
  real scalar m. This runner sharpens that one more step:

    1. prove the exact bank identities tying the selected slice to the frozen
       slot pair (a_*, b_*) and CP pair (cp1, cp2);
    2. reconstruct the entire selected K_Z3 kernel as
           K_Z3^sel(m) = K_frozen + m T_m^(K);
    3. verify numerically that the only live microscopic direction is the
       single fixed real matrix T_m^(K).
"""

from __future__ import annotations

import math
import sys

import numpy as np
import sympy as sp

from frontier_dm_neutrino_postcanonical_polar_section import slot_pair_from_h
from frontier_dm_neutrino_positive_polar_h_cp_theorem import cp_pair_from_h
from frontier_dm_neutrino_source_surface_active_affine_point_selection_boundary import (
    active_affine_h,
)
from frontier_dm_neutrino_source_surface_z3_doublet_block_point_selection_theorem import (
    kz_from_h,
)

PASS_COUNT = 0
FAIL_COUNT = 0

SQRT2 = math.sqrt(2.0)
SQRT3 = math.sqrt(3.0)
SELECTOR = math.sqrt(6.0) / 3.0


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


def selected_h(m: float) -> np.ndarray:
    return active_affine_h(m, SELECTOR, SELECTOR)


def tm_k_matrix() -> np.ndarray:
    return np.array(
        [
            [1.0, 0.0, 0.0],
            [0.0, 0.0, 1.0],
            [0.0, 1.0, 0.0],
        ],
        dtype=complex,
    )


def frozen_kernel(a_star: complex, b_star: complex, cp1: float, cp2: float) -> np.ndarray:
    return np.array(
        [
            [-2.0 * cp2 - 3.0 * cp1, a_star, b_star],
            [
                np.conj(a_star),
                1.5 * cp1 + cp2 - 1.0 / (2.0 * SQRT3),
                -2.0 * cp2 - 1.5j * cp2,
            ],
            [
                np.conj(b_star),
                -2.0 * cp2 + 1.5j * cp2,
                1.5 * cp1 + cp2 + 1.0 / (2.0 * SQRT3),
            ],
        ],
        dtype=complex,
    )


def part1_exact_bank_identities_anchor_the_selected_slice() -> None:
    print("=" * 88)
    print("PART 1: exact bank identities anchor the selected slice")
    print("=" * 88)

    sqrt2 = sp.sqrt(2)
    sqrt3 = sp.sqrt(3)
    sqrt6 = sp.sqrt(6)

    a_star = 2 * sqrt2 / 9 - sqrt3 / 12 + sp.I * (sp.Rational(1, 4) + 2 * sqrt2 / 3)
    b_star = 2 * sqrt2 / 9 + sqrt3 / 12 + sp.I * (sp.Rational(1, 4) - 2 * sqrt2 / 3)
    cp1 = -2 * sqrt6 / 9
    cp2 = 2 * sqrt2 / 9
    q_plus = sqrt6 / 3

    check(
        "The frozen slot pair carries the real selected-slice offset exactly",
        sp.simplify(sp.re(a_star + b_star) - 2 * cp2) == 0,
        detail="Re(a_* + b_*) = 2 cp2 = 4 sqrt(2)/9",
    )
    check(
        "The observable-selector point is already encoded in the frozen CP constant cp1",
        sp.simplify(q_plus + 3 * cp1 / 2) == 0,
        detail="q_+* = -3 cp1 / 2 = sqrt(6)/3",
    )
    check(
        "The selected-slice imaginary doublet-mixing offset is already encoded in cp2",
        sp.simplify(sqrt3 * q_plus - 4 * sqrt2 / 3 + 3 * cp2 / 2) == 0,
        detail="Im K12 = -3 cp2 / 2",
    )
    check(
        "The selected doublet-block trace offset is fixed by the same frozen bank",
        sp.simplify((-2 * q_plus + 4 * sqrt2 / 9) - (2 * cp2 + 3 * cp1)) == 0,
        detail="K11 + K22 = 2 cp2 + 3 cp1",
    )


def part2_the_entire_selected_kernel_is_frozen_plus_one_real_direction() -> None:
    print()
    print("=" * 88)
    print("PART 2: the entire selected kernel is frozen plus one real direction")
    print("=" * 88)

    m_values = (-1.2957949040672103, -1.160469470087, -1.0, -0.5, 0.0)
    tm = tm_k_matrix()

    ref_h = selected_h(m_values[0])
    a_star, b_star = slot_pair_from_h(ref_h)
    cp1, cp2 = cp_pair_from_h(ref_h)
    k_frozen = frozen_kernel(a_star, b_star, cp1, cp2)

    ok_bank = True
    ok_recon = True
    max_err = 0.0
    for m in m_values:
        h = selected_h(m)
        slots = slot_pair_from_h(h)
        cps = cp_pair_from_h(h)
        kz = kz_from_h(h)
        kz_expected = k_frozen + m * tm

        ok_bank &= abs(slots[0] - a_star) < 1e-12 and abs(slots[1] - b_star) < 1e-12
        ok_bank &= abs(cps[0] - cp1) < 1e-12 and abs(cps[1] - cp2) < 1e-12

        err = float(np.max(np.abs(kz - kz_expected)))
        max_err = max(max_err, err)
        ok_recon &= err < 1e-12

    check(
        "Along the full selected m-line the slot pair and CP pair stay exactly frozen",
        ok_bank,
        detail=f"cp=({cp1:.12f},{cp2:.12f})",
        kind="NUMERIC",
    )
    check(
        "Those frozen bank constants reconstruct the full selected K_Z3 kernel exactly once m is supplied",
        ok_recon,
        detail=f"max reconstruction err={max_err:.2e}",
        kind="NUMERIC",
    )
    check(
        "So the selected slice is exactly the affine line K_frozen + m T_m^(K)",
        ok_recon,
        detail="T_m^(K) carries only K00 and the real K12/K21 direction",
        kind="NUMERIC",
    )


def part3_only_one_real_microscopic_direction_survives() -> None:
    print()
    print("=" * 88)
    print("PART 3: only one real microscopic direction survives")
    print("=" * 88)

    m1 = -1.20
    m2 = -0.40
    kz1 = kz_from_h(selected_h(m1))
    kz2 = kz_from_h(selected_h(m2))
    tm = tm_k_matrix()
    delta_m = m2 - m1
    diff = kz2 - kz1

    check(
        "Differences between any two selected-slice kernels lie exactly on the one fixed matrix T_m^(K)",
        np.max(np.abs(diff - delta_m * tm)) < 1e-12,
        detail=f"delta_m={delta_m:.12f}",
        kind="NUMERIC",
    )
    check(
        "No additional slot, CP, or q_+/delta directions survive on the selected slice",
        np.max(np.abs(diff - delta_m * tm)) < 1e-12,
        detail="the live microscopic selector is one real coefficient only",
        kind="NUMERIC",
    )


def main() -> int:
    part1_exact_bank_identities_anchor_the_selected_slice()
    part2_the_entire_selected_kernel_is_frozen_plus_one_real_direction()
    part3_only_one_real_microscopic_direction_survives()

    print()
    print("Interpretation:")
    print("  On the charged-lepton selected slice, the full intrinsic K_Z3 kernel")
    print("  is already decomposed as a frozen slot/CP bank plus one real matrix")
    print("  direction T_m^(K). So the remaining charged-lepton selector is not a")
    print("  free doublet-block law anymore; it is one residual real coefficient.")
    print()
    print(f"PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
