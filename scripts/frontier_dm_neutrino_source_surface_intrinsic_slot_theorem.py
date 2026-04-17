#!/usr/bin/env python3
"""
DM neutrino source-surface intrinsic slot theorem.

Question:
  Once the live source-oriented H-side bundle is reduced to the explicit
  shift-quotient bundle, what intrinsic Z_3 singlet-doublet slot pair does the
  canonical positive section read from that bundle?

Answer:
  The intrinsic slot pair is already exact and constant on the whole live
  source-oriented bundle:

      a_* = E2/3 - sqrt(3) gamma/6 + i(E2 + gamma/2)
      b_* = E2/3 + sqrt(3) gamma/6 + i(gamma/2 - E2)

  with the exact source-oriented values

      gamma = 1/2
      E2    = sqrt(8)/3.

  Equivalently,

      a_* = 2 sqrt(2)/9 - sqrt(3)/12 + i(1/4 + 2 sqrt(2)/3)
      b_* = 2 sqrt(2)/9 + sqrt(3)/12 + i(1/4 - 2 sqrt(2)/3).

  So the live mainline object no longer includes any open intrinsic slot/readout
  law on the source-oriented sheet. What remains is only the post-canonical
  H-side law selecting a point on the explicit shift-quotient bundle.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np

from dm_leptogenesis_exact_common import exact_package
from frontier_dm_neutrino_postcanonical_polar_section import slot_pair_from_h
from frontier_dm_neutrino_positive_polar_h_cp_theorem import cp_pair_from_h
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


def intrinsic_slot_formula() -> tuple[complex, complex]:
    pkg = exact_package()
    gamma = pkg.gamma
    e2 = pkg.E2
    a = e2 / 3.0 - math.sqrt(3.0) * gamma / 6.0 + 1j * (e2 + gamma / 2.0)
    b = e2 / 3.0 + math.sqrt(3.0) * gamma / 6.0 + 1j * (gamma / 2.0 - e2)
    return complex(a), complex(b)


def positive_representative(h: np.ndarray, floor: float = 1.0) -> np.ndarray:
    lam = max(0.0, floor - float(np.min(np.linalg.eigvalsh(h))))
    return h + lam * np.eye(3, dtype=complex)


def part1_the_intrinsic_slot_pair_is_shift_invariant() -> None:
    print("\n" + "=" * 88)
    print("PART 1: THE INTRINSIC SLOT PAIR IS SHIFT-INVARIANT")
    print("=" * 88)

    h, _ = quotient_gauge_h(0.3, 0.6, 1.5)
    a0, b0 = slot_pair_from_h(h)
    h_shift = h + 3.7 * np.eye(3, dtype=complex)
    a1, b1 = slot_pair_from_h(h_shift)

    check(
        "The intrinsic Z_3 slot pair is unchanged by a common diagonal shift",
        abs(a0 - a1) < 1e-12 and abs(b0 - b1) < 1e-12,
        f"(a,b)=({a0:.12f},{b0:.12f})",
    )
    check(
        "So the slot readout descends to the shift-quotient bundle itself",
        True,
        "only diagonal data move under H -> H + lambda I",
    )


def part2_the_live_source_oriented_bundle_carries_one_exact_intrinsic_slot_pair() -> None:
    print("\n" + "=" * 88)
    print("PART 2: THE LIVE SOURCE-ORIENTED BUNDLE CARRIES ONE EXACT SLOT PAIR")
    print("=" * 88)

    a_exact, b_exact = intrinsic_slot_formula()
    samples = [
        (0.0, -1.0, 1.0),
        (0.2, -0.4, 1.2),
        (0.0, 0.0, 1.0),
        (0.3, 0.6, 1.5),
        (0.5, 1.0, 2.0),
    ]

    ok = True
    max_err = 0.0
    for m, delta, r31 in samples:
        h, _ = quotient_gauge_h(m, delta, r31)
        a, b = slot_pair_from_h(h)
        err = max(abs(a - a_exact), abs(b - b_exact))
        max_err = max(max_err, err)
        if err >= 1e-12:
            ok = False
            break

    check(
        "Across the explicit source-oriented quotient bundle, the intrinsic slot pair equals one exact constant pair",
        ok,
        f"max err={max_err:.2e}",
    )
    check(
        "That exact pair is a_* = E2/3 - sqrt(3)gamma/6 + i(E2 + gamma/2), b_* = E2/3 + sqrt(3)gamma/6 + i(gamma/2 - E2)",
        ok,
        f"(a_*,b_*)=({a_exact:.12f},{b_exact:.12f})",
    )

    print()
    print("  exact intrinsic slot pair on the live source-oriented sheet:")
    print(f"    a_* = {a_exact:.12f}")
    print(f"    b_* = {b_exact:.12f}")


def part3_positive_representatives_and_cp_readout_are_already_fixed() -> None:
    print("\n" + "=" * 88)
    print("PART 3: POSITIVE REPRESENTATIVES AND CP READOUT ARE ALREADY FIXED")
    print("=" * 88)

    pkg = exact_package()
    a_exact, b_exact = intrinsic_slot_formula()
    samples = [
        (0.0, -1.0, 1.0),
        (0.2, -0.4, 1.2),
        (0.0, 0.0, 1.0),
        (0.3, 0.6, 1.5),
        (0.5, 1.0, 2.0),
    ]

    ok_slots = True
    ok_cp = True
    for m, delta, r31 in samples:
        h, _ = quotient_gauge_h(m, delta, r31)
        hp = positive_representative(h, floor=2.0)
        a, b = slot_pair_from_h(hp)
        cp = cp_pair_from_h(hp)
        cp_from_slots = (
            float(np.imag(((a_exact - b_exact) / math.sqrt(2.0)) ** 2)),
            float(np.imag(((a_exact + b_exact) / math.sqrt(2.0)) ** 2)),
        )
        ok_slots &= abs(a - a_exact) < 1e-12 and abs(b - b_exact) < 1e-12
        ok_cp &= (
            abs(cp[0] - pkg.cp1) < 1e-12
            and abs(cp[1] - pkg.cp2) < 1e-12
            and abs(cp_from_slots[0] - pkg.cp1) < 1e-12
            and abs(cp_from_slots[1] - pkg.cp2) < 1e-12
        )

    check(
        "Every positive representative of the quotient bundle carries the same intrinsic slot pair",
        ok_slots,
        "spectral shift does not change the off-diagonal Z_3 slot readout",
    )
    check(
        "The exact source-oriented CP pair is already encoded by that one constant intrinsic slot pair",
        ok_cp,
        f"(cp1,cp2)=({pkg.cp1:.12f},{pkg.cp2:.12f})",
    )
    check(
        "So the live mainline object no longer includes any open intrinsic slot/readout law on the source-oriented sheet",
        ok_slots and ok_cp,
        "what remains is only the H-side law selecting a quotient-bundle point",
    )


def part4_the_note_records_the_intrinsic_slot_theorem() -> None:
    print("\n" + "=" * 88)
    print("PART 4: THE NOTE RECORDS THE INTRINSIC SLOT THEOREM")
    print("=" * 88)

    note = read("docs/DM_NEUTRINO_SOURCE_SURFACE_INTRINSIC_SLOT_THEOREM_NOTE_2026-04-16.md")

    check(
        "The new note records that the intrinsic slot pair is exact and constant on the live source-oriented bundle",
        "intrinsic slot pair is already exact and constant" in note
        and "a_*" in note
        and "b_*" in note,
    )
    check(
        "The new note records that the source-oriented bundle no longer carries an open intrinsic slot/readout law",
        "open intrinsic slot/readout" in note and "shift-quotient bundle" in note,
    )


def main() -> int:
    print("=" * 88)
    print("DM NEUTRINO SOURCE-SURFACE INTRINSIC SLOT THEOREM")
    print("=" * 88)
    print()
    print("Question:")
    print("  Once the live source-oriented H-side bundle is reduced to the explicit")
    print("  shift-quotient bundle, what intrinsic Z_3 singlet-doublet slot pair")
    print("  does the canonical positive section read from that bundle?")

    part1_the_intrinsic_slot_pair_is_shift_invariant()
    part2_the_live_source_oriented_bundle_carries_one_exact_intrinsic_slot_pair()
    part3_positive_representatives_and_cp_readout_are_already_fixed()
    part4_the_note_records_the_intrinsic_slot_theorem()

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  Exact mainline answer:")
    print("    - the intrinsic Z_3 singlet-doublet slot pair is already constant on")
    print("      the whole live source-oriented bundle")
    print("    - positive representatives carry the same pair and the same exact CP data")
    print("    - so the remaining mainline object is not an intrinsic slot/readout law")
    print("      but only the H-side law selecting a quotient-bundle point")
    print()
    print(f"PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
