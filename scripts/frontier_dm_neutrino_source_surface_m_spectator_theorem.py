#!/usr/bin/env python3
"""
DM neutrino source-surface m-spectator theorem.

Question:
  On the live source-oriented shift-quotient bundle over (m, delta, r31), does
  every quotient coordinate remain active for the exact leptogenesis-facing
  mainline data?

Answer:
  No.

  The quotient coordinate m is an exact spectator tangent:

      H(m + dm, delta, r31) = H(m, delta, r31) + dm T_m

  with

      T_m =
      [ 1  0  0 ]
      [ 0  0  1 ]
      [ 0  1  0 ].

  Along that tangent, the exact source-surface values, the intrinsic CP pair,
  and the intrinsic Z_3 slot pair are all unchanged. So the current exact
  leptogenesis-facing mainline object already factors through the active bundle
  over (delta, r31), not the full three-real bundle over (m, delta, r31).

  On the positive carrier chart, if

      q_+(delta, r31) = sqrt(8/3) - delta + sqrt(r31^2 - 1/4),

  then the active response is already exact:

      gamma = 1/2
      rho = sqrt(8/3) - delta
      sigma sin(2v) = 8/9
      sigma cos(2v) = sqrt(8)/9 - 3 q_+.

  So the live mainline object is already an exact 2-real active bundle over
  (delta, r31), equivalently over (delta, q_+), with m only a spectator line.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np

from dm_leptogenesis_exact_common import exact_package
from frontier_dm_neutrino_exact_h_source_surface_theorem import source_surface_values
from frontier_dm_neutrino_postcanonical_polar_section import slot_pair_from_h
from frontier_dm_neutrino_positive_polar_h_cp_theorem import cp_pair_from_h
from frontier_dm_neutrino_source_surface_carrier_normal_form import (
    source_surface_data_in_carrier_normal_form,
)
from frontier_dm_neutrino_source_surface_shift_quotient_bundle_theorem import quotient_gauge_h

ROOT = Path(__file__).resolve().parents[1]

PASS_COUNT = 0
FAIL_COUNT = 0

T_M = np.array(
    [
        [1.0, 0.0, 0.0],
        [0.0, 0.0, 1.0],
        [0.0, 1.0, 0.0],
    ],
    dtype=complex,
)


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


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def q_plus(delta: float, r31: float) -> float:
    pkg = exact_package()
    return pkg.E1 - delta + math.sqrt(r31 * r31 - pkg.gamma * pkg.gamma)


def positive_chart_m(delta: float, r31: float, offset: float) -> float:
    pkg = exact_package()
    sqrt_leg = math.sqrt(r31 * r31 - pkg.gamma * pkg.gamma)
    threshold = delta - pkg.E1 + pkg.E2 - sqrt_leg
    return threshold + offset


def part1_m_is_an_exact_h_side_spectator_tangent() -> None:
    print("\n" + "=" * 88)
    print("PART 1: m IS AN EXACT H-SIDE SPECTATOR TANGENT")
    print("=" * 88)

    samples = [
        (-0.4, 0.6, 0.6, 1.5),
        (0.2, -0.2, 1.0, 0.9),
        (0.7, 0.4, 1.7, 1.1),
    ]

    ok_tangent = True
    ok_source = True
    ok_cp = True
    ok_slot = True
    for m0, delta, r31, dm in samples:
        h0, pars0 = quotient_gauge_h(m0, delta, r31)
        h1, pars1 = quotient_gauge_h(m0 + dm, delta, r31)
        d1_0, d2_0, d3_0, r12_0, r23_0, _r31_0, phi_0 = pars0
        d1_1, d2_1, d3_1, r12_1, r23_1, _r31_1, phi_1 = pars1

        surf0 = source_surface_values(d1_0, d2_0, d3_0, r12_0, r23_0, r31, phi_0)
        surf1 = source_surface_values(d1_1, d2_1, d3_1, r12_1, r23_1, r31, phi_1)
        cp0 = cp_pair_from_h(h0)
        cp1 = cp_pair_from_h(h1)
        slot0 = slot_pair_from_h(h0)
        slot1 = slot_pair_from_h(h1)

        ok_tangent &= np.linalg.norm(h1 - h0 - dm * T_M) < 1e-12
        ok_source &= max(abs(a - b) for a, b in zip(surf0, surf1)) < 1e-12
        ok_cp &= max(abs(a - b) for a, b in zip(cp0, cp1)) < 1e-12
        ok_slot &= max(abs(slot0[0] - slot1[0]), abs(slot0[1] - slot1[1])) < 1e-12

    check(
        "Changing m moves the quotient bundle only along the exact spectator tangent T_m",
        ok_tangent,
        "H(m+dm)-H(m)=dm T_m",
    )
    check(
        "The exact source-surface values are unchanged along that tangent",
        ok_source,
        "(gamma,B1,B2) are m-invariant",
    )
    check(
        "The intrinsic CP pair is unchanged along that tangent",
        ok_cp,
        "the current leptogenesis-facing CP tensor is m-invariant",
    )
    check(
        "The intrinsic Z_3 slot pair is unchanged along that tangent",
        ok_slot,
        "the current singlet-doublet readout is m-invariant",
    )


def part2_current_exact_mainline_outputs_factor_through_delta_and_r31() -> None:
    print("\n" + "=" * 88)
    print("PART 2: THE CURRENT EXACT MAINLINE OUTPUTS FACTOR THROUGH (delta, r31)")
    print("=" * 88)

    pkg = exact_package()
    grid = [
        (-1.0, 0.7),
        (-0.3, 0.9),
        (0.4, 1.3),
        (1.1, 2.0),
    ]
    ok = True
    for delta, r31 in grid:
        values = []
        for m in (-1.4, -0.2, 0.7, 1.9):
            h, pars = quotient_gauge_h(m, delta, r31)
            d1, d2, d3, r12, r23, _r31, phi = pars
            values.append(
                (
                    source_surface_values(d1, d2, d3, r12, r23, r31, phi),
                    cp_pair_from_h(h),
                    slot_pair_from_h(h),
                )
            )
        ref = values[0]
        for cur in values[1:]:
            ok &= max(abs(a - b) for a, b in zip(ref[0], cur[0])) < 1e-12
            ok &= max(abs(a - b) for a, b in zip(ref[1], cur[1])) < 1e-12
            ok &= max(abs(ref[2][0] - cur[2][0]), abs(ref[2][1] - cur[2][1])) < 1e-12

    check(
        "Across the live quotient bundle, the current exact source/CP/slot outputs already factor through (delta, r31) rather than the full (m, delta, r31)",
        ok,
        f"(gamma,E1,E2,cp)=({pkg.gamma:.12f},{pkg.E1:.12f},{pkg.E2:.12f},{pkg.cp1:.12f},{pkg.cp2:.12f})",
    )
    check(
        "So the live leptogenesis-facing mainline object is already a 2-real active bundle with a spectator m-line",
        ok,
        "m is no longer a live active coordinate for the current exact stack",
    )


def part3_the_positive_carrier_chart_has_exact_two_real_active_formulas() -> None:
    print("\n" + "=" * 88)
    print("PART 3: THE POSITIVE CARRIER CHART HAS EXACT TWO-REAL ACTIVE FORMULAS")
    print("=" * 88)

    pkg = exact_package()
    samples = [
        (-1.0, 0.7),
        (-0.2, 1.0),
        (0.5, 1.5),
        (1.1, 2.3),
    ]

    ok_invariant = True
    ok_formulas = True
    for delta, r31 in samples:
        q = q_plus(delta, r31)
        data = []
        for offset in (0.7, 1.8):
            m = positive_chart_m(delta, r31, offset)
            h, _ = quotient_gauge_h(m, delta, r31)
            data.append(source_surface_data_in_carrier_normal_form(h))

        ref = data[0]
        for cur in data[1:]:
            ok_invariant &= max(abs(a - b) for a, b in zip(ref[3:], cur[3:])) < 1e-12

        _lam_plus, _lam_odd, _u, v, d, rho, gamma, sigma = ref
        ok_formulas &= (
            abs(d - delta) < 1e-12
            and abs(rho - (pkg.E1 - delta)) < 1e-12
            and abs(gamma - pkg.gamma) < 1e-12
            and abs(sigma * math.sin(2.0 * v) - 8.0 / 9.0) < 1e-12
            and abs(sigma * math.cos(2.0 * v) - (pkg.E2 / 3.0 - 3.0 * q)) < 1e-12
        )

    check(
        "Within the positive carrier chart, changing m does not change the active carrier data (delta, rho, gamma, sigma, v)",
        ok_invariant,
        "the carrier-side active response is m-invariant on the live chart",
    )
    check(
        "On that chart the active response is exact: rho = E1-delta, gamma = 1/2, sigma sin(2v) = 8/9, sigma cos(2v) = E2/3 - 3 q_+",
        ok_formulas,
        "q_+ = E1 - delta + sqrt(r31^2 - 1/4)",
    )
    check(
        "So the live mainline carrier response is already an exact 2-real bundle over (delta, q_+), equivalently over (delta, r31)",
        ok_invariant and ok_formulas,
        "m is only a spectator line on top of that active bundle",
    )


def part4_the_note_records_the_m_spectator_reduction() -> None:
    print("\n" + "=" * 88)
    print("PART 4: THE NOTE RECORDS THE m-SPECTATOR REDUCTION")
    print("=" * 88)

    note = read("docs/DM_NEUTRINO_SOURCE_SURFACE_M_SPECTATOR_THEOREM_NOTE_2026-04-16.md")

    check(
        "The new note records m as an exact spectator tangent and the live object as a 2-real active bundle",
        "exact spectator tangent" in note and "2-real active bundle" in note and "q_+" in note,
    )
    check(
        "The new note records that m is spectator and the remaining active object is 2-real",
        "`m` only a spectator line" in note and "2-real active bundle" in note,
    )


def main() -> int:
    print("=" * 88)
    print("DM NEUTRINO SOURCE-SURFACE m-SPECTATOR THEOREM")
    print("=" * 88)
    print()
    print("Question:")
    print("  On the live source-oriented shift-quotient bundle over (m, delta, r31),")
    print("  does every quotient coordinate remain active for the exact")
    print("  leptogenesis-facing mainline data?")

    part1_m_is_an_exact_h_side_spectator_tangent()
    part2_current_exact_mainline_outputs_factor_through_delta_and_r31()
    part3_the_positive_carrier_chart_has_exact_two_real_active_formulas()
    part4_the_note_records_the_m_spectator_reduction()

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  Exact mainline answer:")
    print("    - the quotient coordinate m is an exact spectator tangent of the live")
    print("      source-oriented bundle for the current exact source/CP/slot outputs")
    print("    - the live leptogenesis-facing mainline object already reduces to a")
    print("      2-real active bundle over (delta, r31)")
    print("    - on the positive carrier chart this is equivalently the 2-real bundle")
    print("      over (delta, q_+) with q_+ = E1 - delta + sqrt(r31^2 - 1/4)")
    print()
    print("  So the remaining mainline task is not to populate the spectator m-line.")
    print("  It is to derive the post-canonical law selecting the active two-real")
    print("  bundle itself.")
    print()
    print(f"PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
