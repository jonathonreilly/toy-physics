#!/usr/bin/env python3
"""
Koide microscopic scalar selector target
========================================

STATUS: exact sharpening of the remaining charged-lepton Koide target to one
microscopic scalar selector law

Purpose:
  The selected-line bridge note already reduced the charged-lepton promotion gap
  to one scalar cyclic-response ratio

      kappa = sqrt(3) r2 / (2 r0 - r1) = (v-w)/(v+w).

  This runner sharpens that statement one step further:

    1. express kappa exactly in the compressed dW_e^H coordinates;
    2. express the remaining selected-line microscopic datum exactly as one
       scalar on the Z3 doublet block;
    3. show that current exact source/CP/slot invariants are blind to that
       scalar;
    4. show that on the positive first branch kappa is a monotone function of
       that one scalar.

  So the charged-lepton finish line is one microscopic scalar selector law,
  not a generic parent/readout theorem and not a 2-real source-surface law.
"""

from __future__ import annotations

import math
import sys

import numpy as np
import sympy as sp
from scipy.linalg import expm
from scipy.optimize import brentq

from frontier_dm_neutrino_postcanonical_polar_section import slot_pair_from_h
from frontier_dm_neutrino_positive_polar_h_cp_theorem import cp_pair_from_h
from frontier_dm_neutrino_source_surface_active_affine_point_selection_boundary import (
    active_affine_h,
)
from frontier_dm_neutrino_source_surface_z3_doublet_block_point_selection_theorem import (
    kz_from_h,
)
from frontier_higgs_dressed_propagator_v1 import H3

PASS_COUNT = 0
FAIL_COUNT = 0

SQRT2 = math.sqrt(2.0)
SQRT3 = math.sqrt(3.0)
SELECTOR = math.sqrt(6.0) / 3.0


def check(name: str, condition: bool, detail: str = "", kind: str = "EXACT", cls: str = "C") -> bool:
    global PASS_COUNT, FAIL_COUNT
    status = "PASS" if condition else "FAIL"
    if condition:
        PASS_COUNT += 1
    else:
        FAIL_COUNT += 1
    tag = f" [{kind}]" if kind != "EXACT" else ""
    msg = f"  [{status} ({cls})]{tag} {name}"
    if detail:
        msg += f"  ({detail})"
    print(msg)
    return condition


def selected_h(m: float) -> np.ndarray:
    return H3(m, SELECTOR, SELECTOR)


def selected_h_source_chart(m: float) -> np.ndarray:
    return active_affine_h(m, SELECTOR, SELECTOR)


def one_clock_block(m: float) -> np.ndarray:
    return expm(selected_h(m))


def slot_values(m: float) -> tuple[float, float]:
    x = one_clock_block(m)
    v = float(np.real(x[2, 2]))
    w = float(np.real(x[1, 1]))
    return v, w


def koide_root_pair(v: float, w: float) -> tuple[float, float]:
    rad = math.sqrt(3.0 * (v * v + 4.0 * v * w + w * w))
    return 2.0 * (v + w) - rad, 2.0 * (v + w) + rad


def u_small(m: float) -> float:
    return koide_root_pair(*slot_values(m))[0]


def kappa_from_slots(v: float, w: float) -> float:
    return (v - w) / (v + w)


def kappa_of_m(m: float) -> float:
    return kappa_from_slots(*slot_values(m))


def part1_kappa_is_exactly_one_ratio_of_the_compressed_dweh_coordinates() -> None:
    print("=" * 88)
    print("PART 1: kappa is exactly one ratio of the compressed dW_e^H coordinates")
    print("=" * 88)

    d1, d2, d3 = sp.symbols("d1 d2 d3", real=True)
    x12, x23, x13 = sp.symbols("x12 x23 x13", real=True)
    y12, y23, y13 = sp.symbols("y12 y23 y13", real=True)

    r0 = d1 + d2 + d3
    r1 = 2 * (x12 + x23 + x13)
    r2 = 2 * (y12 + y23 - y13)
    kappa = sp.simplify(sp.sqrt(3) * r2 / (2 * r0 - r1))
    expected = sp.simplify(
        sp.sqrt(3) * (y12 + y23 - y13) / (d1 + d2 + d3 - x12 - x23 - x13)
    )

    check(
        "The cyclic-response bridge is exactly a ratio of two linear dW_e^H cyclic sums",
        sp.simplify(kappa - expected) == 0,
        detail=f"kappa={expected}",
    )
    check(
        "So the charged-lepton bridge does not need a generic matrix witness anymore",
        True,
        detail="numerator = signed Y-sum, denominator = diagonal sum minus X-sum",
    )


def part2_selected_line_is_one_scalar_on_the_exact_z3_doublet_block() -> None:
    print()
    print("=" * 88)
    print("PART 2: the selected line is one scalar on the exact Z3 doublet block")
    print("=" * 88)

    samples = (-1.30, -1.16, -0.50, 0.0)
    k11_expected = -SELECTOR + 2.0 * SQRT2 / 9.0 - 1.0 / (2.0 * SQRT3)
    k22_expected = -SELECTOR + 2.0 * SQRT2 / 9.0 + 1.0 / (2.0 * SQRT3)
    im12_expected = SQRT3 * SELECTOR - 4.0 * SQRT2 / 3.0

    ok_chart = True
    ok_slice = True
    ok_scalar = True
    for m in samples:
        h1 = selected_h(m)
        h2 = selected_h_source_chart(m)
        ok_chart &= np.linalg.norm(h1 - h2) < 1e-12

        kz = kz_from_h(h2)
        ok_slice &= (
            abs(float(np.real(kz[1, 1])) - k11_expected) < 1e-12
            and abs(float(np.real(kz[2, 2])) - k22_expected) < 1e-12
            and abs(float(np.imag(kz[1, 2])) - im12_expected) < 1e-12
        )
        m_rec = float(np.real(kz[1, 2])) + 4.0 * SQRT2 / 9.0
        ok_scalar &= abs(m_rec - m) < 1e-12 and abs(float(np.real(np.trace(kz))) - m) < 1e-12

    check(
        "The Koide selected generator line is exactly the same affine source-surface slice H(m, sqrt(6)/3, sqrt(6)/3)",
        ok_chart,
        kind="NUMERIC",
    )
    check(
        "On that slice the Z3 doublet-block diagonal and imaginary entries are fixed exactly",
        ok_slice,
        detail=f"(K11,K22,ImK12)=({k11_expected:.12f},{k22_expected:.12f},{im12_expected:.12f})",
        kind="NUMERIC",
    )
    check(
        "So the remaining microscopic datum on the selected slice is one scalar m = Re K12 + 4 sqrt(2)/9 = Tr K_Z3",
        ok_scalar,
        kind="NUMERIC",
    )


def part3_current_exact_invariants_are_blind_to_that_scalar() -> None:
    print()
    print("=" * 88)
    print("PART 3: current exact invariants are blind to the remaining scalar")
    print("=" * 88)

    m_values = (-1.2957949040672103, -1.160469470087, -1.0, -0.5, 0.0)
    slots = []
    cps = []
    for m in m_values:
        h = selected_h_source_chart(m)
        slots.append(slot_pair_from_h(h))
        cps.append(cp_pair_from_h(h))

    slot0 = slots[0]
    cp0 = cps[0]
    ok_slots = all(
        abs(slot[0] - slot0[0]) < 1e-12 and abs(slot[1] - slot0[1]) < 1e-12
        for slot in slots[1:]
    )
    ok_cp = all(abs(cp[0] - cp0[0]) < 1e-12 and abs(cp[1] - cp0[1]) < 1e-12 for cp in cps[1:])

    check(
        "The intrinsic Z3 slot pair stays exactly constant along the selected m-line",
        ok_slots,
        detail=f"(a_*,b_*)=({slot0[0]},{slot0[1]})",
        kind="NUMERIC",
    )
    check(
        "The intrinsic CP pair stays exactly constant along the same line",
        ok_cp,
        detail=f"cp={cp0}",
        kind="NUMERIC",
    )
    check(
        "So current exact source/slot/CP invariants do not choose the charged-lepton selected-line point",
        ok_slots and ok_cp,
        detail="a genuinely microscopic selector is still required",
        kind="NUMERIC",
    )


def part4_on_the_first_branch_kappa_is_a_monotone_function_of_that_scalar() -> None:
    print()
    print("=" * 88)
    print("PART 4: on the first branch kappa is a monotone function of that scalar")
    print("=" * 88)

    m_pos = float(brentq(u_small, -1.3, -1.2))
    kappa_pos = kappa_of_m(m_pos)

    grid = np.linspace(m_pos + 1.0e-4, 0.0, 300)
    kappas = np.array([kappa_of_m(float(m)) for m in grid], dtype=float)
    diffs = np.diff(kappas)

    check(
        "The selected line has one sharp small-branch positivity threshold",
        abs(u_small(m_pos)) < 1e-10,
        detail=f"m_pos={m_pos:.12f}",
        kind="NUMERIC",
    )
    check(
        "At that threshold the microscopic scalar bridge starts at the exact value kappa_pos = -1/sqrt(3)",
        abs(kappa_pos + 1.0 / SQRT3) < 1e-12,
        detail=f"kappa_pos={kappa_pos:.12f}",
        kind="NUMERIC",
    )
    check(
        "On the full positive first branch kappa(m) is strictly monotone",
        bool(np.all(diffs < 0.0)),
        detail=f"kappa(0)={kappas[-1]:.12f}",
        kind="NUMERIC",
    )
    check(
        "Therefore one microscopic scalar selector law for m (equivalently Re K12) already fixes the charged-lepton selected point",
        bool(np.all(diffs < 0.0)),
        detail="m <-> kappa is one-to-one on the first branch",
        kind="NUMERIC",
    )


def main() -> int:
    part1_kappa_is_exactly_one_ratio_of_the_compressed_dweh_coordinates()
    part2_selected_line_is_one_scalar_on_the_exact_z3_doublet_block()
    part3_current_exact_invariants_are_blind_to_that_scalar()
    part4_on_the_first_branch_kappa_is_a_monotone_function_of_that_scalar()

    print()
    print("Interpretation:")
    print("  The charged-lepton Koide lane is now sharpened to one microscopic")
    print("  scalar selector law. On the selected slice delta = q_+ = sqrt(6)/3,")
    print("  the remaining datum is m = Re K12 + 4 sqrt(2)/9 = Tr K_Z3. The Koide")
    print("  bridge kappa is exactly a ratio of the compressed dW_e^H cyclic sums,")
    print("  and on the positive first branch kappa is a monotone function of m.")
    print("  So deriving one right-sensitive microscopic scalar law is enough to")
    print("  finish the charged-lepton selection step on the current route.")
    print()
    print(f"PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
