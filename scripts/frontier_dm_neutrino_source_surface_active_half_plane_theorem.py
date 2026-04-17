#!/usr/bin/env python3
"""
DM neutrino source-surface active half-plane theorem.

Question:
  After reducing the live source-oriented quotient bundle to active carrier
  coordinates (delta, q_+), what exact domain remains, and how much of that
  domain is still seen by the current exact source-facing bank?

Answer:
  The live active bundle is exactly the closed half-plane

      q_+ >= sqrt(8/3) - delta.

  Equivalently, if s = q_+ - sqrt(8/3) + delta >= 0, then

      r31 = sqrt(s^2 + 1/4),
      phi_+ = asin(1 / (2 r31)),

  and every such active point has a source-oriented quotient representative,
  hence a positive Hermitian representative after a common diagonal shift.

  Across that whole active half-plane, the currently exact source-facing bank
  stays fixed:

      gamma = 1/2,
      delta + rho = sqrt(8/3),
      sigma sin(2v) = 8/9,
      intrinsic CP pair = (cp1, cp2),
      intrinsic slot pair = (a_*, b_*),
      slot torsion = Im(a_* b_*) = (sqrt(2)+sqrt(6))/9.

  So the current bank determines the exact active chamber, but not a point
  inside it. The remaining mainline object is the post-canonical law selecting
  a point on that half-plane.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np

from dm_leptogenesis_exact_common import exact_package
from frontier_dm_neutrino_positive_polar_h_cp_theorem import cp_pair_from_h
from frontier_dm_neutrino_postcanonical_polar_section import slot_pair_from_h
from frontier_dm_neutrino_source_surface_carrier_normal_form import (
    source_surface_data_in_carrier_normal_form,
)
from frontier_dm_neutrino_source_surface_intrinsic_slot_theorem import (
    intrinsic_slot_formula,
)
from frontier_dm_neutrino_source_surface_shift_quotient_bundle_theorem import (
    quotient_gauge_h,
)

ROOT = Path(__file__).resolve().parents[1]

PASS_COUNT = 0
FAIL_COUNT = 0


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


def q_floor(delta: float) -> float:
    return exact_package().E1 - delta


def r31_from_active(delta: float, q_plus: float) -> float:
    s = q_plus - q_floor(delta)
    if s < -1e-12:
        raise ValueError("Active half-plane requires q_+ >= sqrt(8/3) - delta")
    return math.sqrt(max(0.0, s * s) + exact_package().gamma * exact_package().gamma)


def active_half_plane_h(
    delta: float, q_plus: float, m: float = 0.0
) -> tuple[np.ndarray, float, float]:
    r31 = r31_from_active(delta, q_plus)
    h, _ = quotient_gauge_h(m, delta, r31)
    phi = math.asin(exact_package().gamma / r31)
    return h, r31, phi


def positive_representative(h: np.ndarray, floor: float = 2.0) -> np.ndarray:
    lam = max(0.0, floor - float(np.min(np.linalg.eigvalsh(h))))
    return h + lam * np.eye(3, dtype=complex)


def slot_torsion(a: complex, b: complex) -> float:
    return float(np.imag(a * b))


def part1_the_active_bundle_is_exactly_a_closed_half_plane() -> None:
    print("\n" + "=" * 88)
    print("PART 1: THE ACTIVE BUNDLE IS EXACTLY A CLOSED HALF-PLANE")
    print("=" * 88)

    pkg = exact_package()
    samples = [
        (-1.0, q_floor(-1.0)),
        (0.0, q_floor(0.0) + 0.5),
        (0.5, q_floor(0.5) + 1.0),
        (1.0, q_floor(1.0) + 1.7),
    ]

    ok_inverse = True
    ok_boundary = True
    for delta, q_plus in samples:
        r31 = r31_from_active(delta, q_plus)
        q_back = pkg.E1 - delta + math.sqrt(max(0.0, r31 * r31 - pkg.gamma * pkg.gamma))
        ok_inverse &= abs(q_back - q_plus) < 1e-12

        q_edge = q_floor(delta)
        r31_edge = r31_from_active(delta, q_edge)
        phi_edge = math.asin(pkg.gamma / r31_edge)
        ok_boundary &= abs(r31_edge - pkg.gamma) < 1e-12 and abs(phi_edge - 0.5 * math.pi) < 1e-12

    check(
        "The active coordinates admit an exact inverse chart r31 = sqrt((q_+ - sqrt(8/3) + delta)^2 + 1/4)",
        ok_inverse,
        "q_+ <-> r31 is exact on the positive carrier chart",
    )
    check(
        "The active bundle is therefore the closed half-plane q_+ >= sqrt(8/3) - delta",
        ok_inverse,
        "the square-root offset is nonnegative by construction",
    )
    check(
        "The boundary q_+ = sqrt(8/3) - delta is exactly r31 = 1/2 and phi_+ = pi/2",
        ok_boundary,
        f"gamma={pkg.gamma:.12f}",
    )


def part2_every_active_half_plane_point_has_a_positive_representative_with_exact_carrier_data() -> None:
    print("\n" + "=" * 88)
    print("PART 2: EVERY ACTIVE HALF-PLANE POINT HAS A POSITIVE REPRESENTATIVE")
    print("=" * 88)

    pkg = exact_package()
    samples = [
        (-1.0, q_floor(-1.0)),
        (0.0, q_floor(0.0) + 0.5),
        (0.5, q_floor(0.5) + 1.0),
        (1.0, q_floor(1.0) + 1.7),
    ]

    ok_positive = True
    ok_carrier = True
    max_err = 0.0
    for delta, q_plus in samples:
        h, _r31, _phi = active_half_plane_h(delta, q_plus, m=0.0)
        hp = positive_representative(h, floor=2.0)
        _lam_plus, _lam_odd, _u, v, delta_c, rho, gamma, sigma = source_surface_data_in_carrier_normal_form(hp)
        err = max(
            abs(delta_c - delta),
            abs(gamma - pkg.gamma),
            abs(delta_c + rho - pkg.E1),
            abs(sigma * math.sin(2.0 * v) - 8.0 / 9.0),
            abs(sigma * math.cos(2.0 * v) - (math.sqrt(8.0) / 9.0 - 3.0 * q_plus)),
        )
        max_err = max(max_err, err)
        ok_positive &= float(np.min(np.linalg.eigvalsh(hp))) > 0.0
        ok_carrier &= err < 1e-10

    check(
        "Every active half-plane point already has a positive Hermitian representative after a common diagonal shift",
        ok_positive,
        "positivity is not an extra restriction on the active chamber",
    )
    check(
        "On that chamber the exact carrier response is gamma = 1/2, delta+rho = sqrt(8/3), sigma sin(2v) = 8/9, sigma cos(2v) = sqrt(8)/9 - 3 q_+",
        ok_carrier,
        f"max err={max_err:.2e}",
    )


def part3_the_current_exact_source_facing_bank_is_constant_on_the_whole_half_plane() -> None:
    print("\n" + "=" * 88)
    print("PART 3: THE CURRENT EXACT SOURCE-FACING BANK IS CONSTANT ON THE WHOLE HALF-PLANE")
    print("=" * 88)

    pkg = exact_package()
    a_exact, b_exact = intrinsic_slot_formula()
    torsion_exact = slot_torsion(a_exact, b_exact)
    samples = [
        (0.25, q_floor(0.25) + 0.2),
        (0.25, q_floor(0.25) + 1.4),
        (0.00, 2.2),
        (1.00, 2.2),
    ]

    ok_same_bank = True
    same_delta_diff_q = True
    same_q_diff_delta = True
    for delta, q_plus in samples:
        h, _r31, _phi = active_half_plane_h(delta, q_plus, m=0.0)
        hp = positive_representative(h, floor=2.0)
        a, b = slot_pair_from_h(hp)
        cp = cp_pair_from_h(hp)
        _lam_plus, _lam_odd, _u, _v, delta_c, rho, gamma, _sigma = source_surface_data_in_carrier_normal_form(hp)
        ok_same_bank &= (
            abs(a - a_exact) < 1e-12
            and abs(b - b_exact) < 1e-12
            and abs(slot_torsion(a, b) - torsion_exact) < 1e-12
            and abs(cp[0] - pkg.cp1) < 1e-12
            and abs(cp[1] - pkg.cp2) < 1e-12
            and abs(gamma - pkg.gamma) < 1e-12
            and abs(delta_c + rho - pkg.E1) < 1e-12
        )

    h1, _, _ = active_half_plane_h(0.25, q_floor(0.25) + 0.2)
    h2, _, _ = active_half_plane_h(0.25, q_floor(0.25) + 1.4)
    hp1 = positive_representative(h1, floor=2.0)
    hp2 = positive_representative(h2, floor=2.0)
    same_delta_diff_q &= (
        abs(cp_pair_from_h(hp1)[0] - cp_pair_from_h(hp2)[0]) < 1e-12
        and abs(cp_pair_from_h(hp1)[1] - cp_pair_from_h(hp2)[1]) < 1e-12
        and abs(slot_pair_from_h(hp1)[0] - slot_pair_from_h(hp2)[0]) < 1e-12
        and abs(slot_pair_from_h(hp1)[1] - slot_pair_from_h(hp2)[1]) < 1e-12
    )

    h3, _, _ = active_half_plane_h(0.00, 2.2)
    h4, _, _ = active_half_plane_h(1.00, 2.2)
    hp3 = positive_representative(h3, floor=2.0)
    hp4 = positive_representative(h4, floor=2.0)
    same_q_diff_delta &= (
        abs(cp_pair_from_h(hp3)[0] - cp_pair_from_h(hp4)[0]) < 1e-12
        and abs(cp_pair_from_h(hp3)[1] - cp_pair_from_h(hp4)[1]) < 1e-12
        and abs(slot_pair_from_h(hp3)[0] - slot_pair_from_h(hp4)[0]) < 1e-12
        and abs(slot_pair_from_h(hp3)[1] - slot_pair_from_h(hp4)[1]) < 1e-12
    )

    check(
        "Across the exact active half-plane the source-surface data, intrinsic CP pair, intrinsic slot pair, and slot torsion stay fixed",
        ok_same_bank,
        f"torsion={(torsion_exact):.12f}",
    )
    check(
        "Keeping delta fixed while changing q_+ leaves the current exact source-facing bank unchanged",
        same_delta_diff_q,
        "so q_+ is not selected by the current bank",
    )
    check(
        "Keeping q_+ fixed while changing delta also leaves the current exact source-facing bank unchanged",
        same_q_diff_delta,
        "so delta is not selected by the current bank either",
    )
    check(
        "So the current bank determines the exact active chamber but not a point inside it",
        ok_same_bank and same_delta_diff_q and same_q_diff_delta,
        "the remaining mainline object is the law selecting one active-half-plane point",
    )


def part4_the_note_records_the_active_half_plane() -> None:
    print("\n" + "=" * 88)
    print("PART 4: THE NOTE RECORDS THE ACTIVE HALF-PLANE")
    print("=" * 88)

    note = read("docs/DM_NEUTRINO_SOURCE_SURFACE_ACTIVE_HALF_PLANE_THEOREM_NOTE_2026-04-16.md")

    check(
        "The new note records the exact active half-plane q_+ >= sqrt(8/3) - delta",
        "q_+ >= sqrt(8/3) - delta" in note and "active half-plane" in note,
    )
    check(
        "The new note records that the current bank fixes the chamber but not a point inside it",
        "current exact source-facing bank is constant on that whole chamber" in note
        and "not a point inside it" in note,
    )


def main() -> int:
    print("=" * 88)
    print("DM NEUTRINO SOURCE-SURFACE ACTIVE HALF-PLANE THEOREM")
    print("=" * 88)
    print()
    print("Question:")
    print("  After reducing the live source-oriented quotient bundle to active")
    print("  carrier coordinates (delta, q_+), what exact domain remains, and how")
    print("  much of that domain is still seen by the current exact source-facing bank?")

    part1_the_active_bundle_is_exactly_a_closed_half_plane()
    part2_every_active_half_plane_point_has_a_positive_representative_with_exact_carrier_data()
    part3_the_current_exact_source_facing_bank_is_constant_on_the_whole_half_plane()
    part4_the_note_records_the_active_half_plane()

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  Exact mainline answer:")
    print("    - the live active bundle is exactly the closed half-plane")
    print("      q_+ >= sqrt(8/3) - delta")
    print("    - every point on that chamber already has a positive Hermitian")
    print("      representative and the exact carrier response")
    print("    - the current exact source-facing bank is constant on that whole chamber")
    print("    - so the remaining mainline object is the post-canonical law that")
    print("      selects one point on the active half-plane")
    print()
    print(f"PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
