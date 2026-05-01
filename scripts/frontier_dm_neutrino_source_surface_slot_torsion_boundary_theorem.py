#!/usr/bin/env python3
"""
DM neutrino source-surface slot-torsion boundary theorem.

Question:
  Can the current exact one-phase real-slot family from the atlas,

      a = (u+v) e^{-i phi},   b = (u-v) e^{+i phi},   u,v in R,

  populate the live source-oriented intrinsic slot pair on the post-canonical
  H-side sheet?

Answer:
  No.

  The one-phase real-slot family has exact slot torsion

      T_slot(a,b) = Im(a b) = 0

  because a b = u^2 - v^2 is real.

  But on the live source-oriented sheet the intrinsic slot pair is already the
  exact constant pair (a_*, b_*), and its slot torsion is

      T_slot(a_*, b_*) = Im(a_* b_*) = (sqrt(2) + sqrt(6)) / 9 != 0.

  Therefore the live source-oriented sheet lies outside the current exact
  one-phase real-slot family. In particular it lies outside the source-faithful
  character-transfer branches lambda in {-1,0,+1} with phase phi = lambda 2pi/3.

  So the remaining mainline law cannot close by reusing that old one-phase
  slot-family atlas subroute. Any future constructive law must carry nonzero
  slot torsion, equivalently go beyond the current one-phase real-slot family.
"""

from __future__ import annotations

import cmath
import math
import sys
from pathlib import Path

from frontier_dm_neutrino_postcanonical_polar_section import slot_pair_from_h
from frontier_dm_neutrino_source_surface_intrinsic_slot_theorem import intrinsic_slot_formula
from frontier_dm_neutrino_source_surface_shift_quotient_bundle_theorem import quotient_gauge_h

ROOT = Path(__file__).resolve().parents[1]

PASS_COUNT = 0
FAIL_COUNT = 0


def check(name: str, condition: bool, detail: str = "", cls: str = "C") -> bool:
    global PASS_COUNT, FAIL_COUNT
    status = "PASS" if condition else "FAIL"
    if condition:
        PASS_COUNT += 1
    else:
        FAIL_COUNT += 1
    msg = f"  [{status} ({cls})] {name}"
    if detail:
        msg += f"  ({detail})"
    print(msg)
    return condition


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def slot_torsion(a: complex, b: complex) -> float:
    return float((a * b).imag)


def slot_decomposition(a: complex, b: complex, phi: float) -> tuple[complex, complex]:
    u = 0.5 * (a * cmath.exp(1j * phi) + b * cmath.exp(-1j * phi))
    v = 0.5 * (a * cmath.exp(1j * phi) - b * cmath.exp(-1j * phi))
    return u, v


def part1_one_phase_real_slot_families_have_zero_slot_torsion() -> None:
    print("\n" + "=" * 88)
    print("PART 1: ONE-PHASE REAL-SLOT FAMILIES HAVE ZERO SLOT TORSION")
    print("=" * 88)

    samples = [
        (0.7, 0.2, 0.0),
        (0.9, -0.3, math.pi / 7.0),
        (1.4, 0.5, 2.0 * math.pi / 3.0),
        (-0.8, 0.6, -math.pi / 5.0),
    ]

    ok = True
    max_err = 0.0
    for u, v, phi in samples:
        a = (u + v) * cmath.exp(-1j * phi)
        b = (u - v) * cmath.exp(+1j * phi)
        prod = a * b
        err = max(abs(prod.imag), abs(prod.real - (u * u - v * v)))
        max_err = max(max_err, err)
        ok &= err < 1e-12

    check(
        "For any one-phase real-slot family, a b = u^2 - v^2 is exactly real",
        ok,
        f"max err={max_err:.2e}",
    )
    check(
        "So the exact slot torsion invariant T_slot(a,b) = Im(a b) vanishes on the whole one-phase real-slot family",
        ok,
        "T_slot = 0 is a necessary condition for one-phase real-slot realizability",
    )


def part2_the_live_source_oriented_slot_pair_has_exact_nonzero_torsion() -> None:
    print("\n" + "=" * 88)
    print("PART 2: THE LIVE SOURCE-ORIENTED SLOT PAIR HAS NONZERO TORSION")
    print("=" * 88)

    a_exact, b_exact = intrinsic_slot_formula()
    t_exact = (math.sqrt(2.0) + math.sqrt(6.0)) / 9.0

    samples = [
        (-0.4, -1.0, 1.0),
        (0.0, 0.0, 1.0),
        (0.3, 0.6, 1.5),
        (0.5, 1.0, 2.0),
    ]

    ok_pair = True
    ok_torsion = True
    for m, delta, r31 in samples:
        h, _ = quotient_gauge_h(m, delta, r31)
        a, b = slot_pair_from_h(h)
        ok_pair &= max(abs(a - a_exact), abs(b - b_exact)) < 1e-12
        ok_torsion &= abs(slot_torsion(a, b) - t_exact) < 1e-12

    check(
        "Across the live source-oriented bundle, the intrinsic slot pair is the exact constant pair (a_*, b_*)",
        ok_pair,
        f"(a_*,b_*)=({a_exact:.12f},{b_exact:.12f})",
    )
    check(
        "That exact slot pair carries nonzero slot torsion T_slot(a_*,b_*) = (sqrt(2)+sqrt(6))/9",
        ok_torsion and abs(slot_torsion(a_exact, b_exact) - t_exact) < 1e-12,
        f"T_slot={slot_torsion(a_exact, b_exact):.12f}",
    )
    check(
        "So the live source-oriented intrinsic slot pair cannot lie on the one-phase real-slot family",
        ok_pair and ok_torsion and abs(slot_torsion(a_exact, b_exact)) > 1e-12,
        "the necessary one-phase condition T_slot = 0 fails exactly",
    )


def part3_exact_source_faithful_character_branches_fail_as_well() -> None:
    print("\n" + "=" * 88)
    print("PART 3: THE EXACT SOURCE-FAITHFUL CHARACTER BRANCHES FAIL AS WELL")
    print("=" * 88)

    a_exact, b_exact = intrinsic_slot_formula()
    branches = [-1, 0, 1]
    ok = True
    max_score = 0.0
    details = []
    for lam in branches:
        phi = lam * 2.0 * math.pi / 3.0
        u, v = slot_decomposition(a_exact, b_exact, phi)
        score = abs(u.imag) + abs(v.imag)
        max_score = max(max_score, score)
        ok &= score > 1e-6
        details.append(f"lam={lam}: |Im u|+|Im v|={score:.6f}")

    check(
        "On the exact source-faithful branches lambda in {-1,0,+1}, the live slot pair does not decompose with real u and v",
        ok,
        "; ".join(details),
    )
    check(
        "So the old source-faithful one-phase slot family is comparator/support only, not a constructive selector for the live source-oriented sheet",
        ok,
        f"max imaginary defect={max_score:.6f}",
    )


def part4_the_note_records_the_slot_torsion_boundary() -> None:
    print("\n" + "=" * 88)
    print("PART 4: THE NOTE RECORDS THE SLOT-TORSION BOUNDARY")
    print("=" * 88)

    note = read("docs/DM_NEUTRINO_SOURCE_SURFACE_SLOT_TORSION_BOUNDARY_THEOREM_NOTE_2026-04-16.md")

    check(
        "The new note records the nonzero slot torsion and the one-phase-family incompatibility",
        "slot torsion" in note and "(sqrt(2) + sqrt(6)) / 9" in note and "one-phase real-slot family" in note,
    )
    check(
        "The new note records that the old one-phase source-faithful slot family cannot populate the live source-oriented sheet",
        "one-phase real-slot family" in note and "not the constructive selector" in note,
    )


def main() -> int:
    print("=" * 88)
    print("DM NEUTRINO SOURCE-SURFACE SLOT-TORSION BOUNDARY THEOREM")
    print("=" * 88)
    print()
    print("Question:")
    print("  Can the current exact one-phase real-slot atlas family populate the")
    print("  live source-oriented intrinsic slot pair on the post-canonical H-side sheet?")

    part1_one_phase_real_slot_families_have_zero_slot_torsion()
    part2_the_live_source_oriented_slot_pair_has_exact_nonzero_torsion()
    part3_exact_source_faithful_character_branches_fail_as_well()
    part4_the_note_records_the_slot_torsion_boundary()

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  Exact mainline answer:")
    print("    - the old one-phase real-slot family has exact slot torsion T_slot = 0")
    print("    - the live source-oriented intrinsic slot pair has exact nonzero torsion")
    print("      T_slot = (sqrt(2) + sqrt(6)) / 9")
    print("    - therefore the current source-faithful one-phase slot family cannot")
    print("      populate the live source-oriented sheet")
    print()
    print("  So the remaining mainline law must go beyond that atlas subfamily and")
    print("  carry nonzero slot torsion, or work directly on the active carrier-side")
    print("  bundle rather than on the old one-phase slot route.")
    print()
    print(f"PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
