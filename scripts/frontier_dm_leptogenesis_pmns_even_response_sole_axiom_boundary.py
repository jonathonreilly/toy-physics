#!/usr/bin/env python3
"""
DM leptogenesis PMNS even-response sole-axiom boundary.

Question:
  After the residual PMNS sheet selector has been reduced to the odd bit
  `sign(sin(delta))` on the fixed native seed surface, does the current
  sole-axiom bank already force the remaining even-response pair?

Answer:
  No.

  On the same exact native `N_e` seed surface, and with the same positive odd
  selector bit `sin(delta) > 0`, the canonical near-closing sample and the
  constructive projected-source witness still carry opposite even-response
  pairs:

      canonical:     E1 < 0, E2 < 0
      constructive:  E1 > 0, E2 > 0

  So after the odd selector is fixed, the exact remaining PMNS sole-axiom
  object is the even-response law for `(E1, E2)`, equivalently the carrier-side
  pair `(delta + rho, sigma sin(2v))`.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np

from frontier_dm_leptogenesis_pmns_active_projector_reduction import seed_averages
from frontier_dm_leptogenesis_pmns_breaking_triplet_source_law import (
    triplet_channels_from_active_data,
)
from frontier_dm_leptogenesis_pmns_constructive_projected_source_selector_theorem import (
    WITNESS_DELTA,
    WITNESS_X,
    WITNESS_Y,
)
from frontier_dm_leptogenesis_pmns_projector_interface import canonical_h
from frontier_dm_neutrino_source_surface_carrier_normal_form import (
    source_surface_data_in_carrier_normal_form,
)

ROOT = Path(__file__).resolve().parents[1]

PASS_COUNT = 0
FAIL_COUNT = 0

CANONICAL_X = np.array([0.24, 0.38, 1.07], dtype=float)
CANONICAL_Y = np.array([0.09, 0.22, 0.61], dtype=float)
CANONICAL_DELTA = 1.10


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


def carrier_even_response(
    x: np.ndarray, y: np.ndarray, phase: float
) -> tuple[float, float, float, float]:
    h = canonical_h(x, y, phase)
    _lam_plus, _lam_odd, _u, v, delta, rho, gamma, sigma = (
        source_surface_data_in_carrier_normal_form(h)
    )
    e1 = delta + rho
    sigma_sin_2v = sigma * math.sin(2.0 * v)
    e2 = 0.75 * math.sqrt(2.0) * sigma_sin_2v
    return e1, e2, gamma, sigma_sin_2v


def triplet_data(
    x: np.ndarray, y: np.ndarray, phase: float
) -> tuple[float, float, float, float, float]:
    xbar, ybar = seed_averages(x, y)
    gamma, e1, e2 = triplet_channels_from_active_data(x, y, phase)
    return xbar, ybar, gamma, e1, e2


def part1_the_fixed_native_seed_surface_and_positive_odd_bit_do_not_yet_close_the_pmns_object() -> None:
    print("\n" + "=" * 88)
    print("PART 1: SAME NATIVE SEED SURFACE, SAME POSITIVE ODD BIT")
    print("=" * 88)

    c_xbar, c_ybar, c_gamma, _c_e1, _c_e2 = triplet_data(
        CANONICAL_X, CANONICAL_Y, CANONICAL_DELTA
    )
    w_xbar, w_ybar, w_gamma, _w_e1, _w_e2 = triplet_data(
        WITNESS_X, WITNESS_Y, WITNESS_DELTA
    )

    check(
        "The canonical near-closing sample and the constructive witness lie on the same exact native seed surface",
        abs(c_xbar - w_xbar) < 1e-12 and abs(c_ybar - w_ybar) < 1e-12,
        f"(xbar,ybar)=({c_xbar:.12f},{c_ybar:.12f})",
    )
    check(
        "Both samples already satisfy the same positive odd selector bit sin(delta) > 0",
        math.sin(CANONICAL_DELTA) > 0.0 and math.sin(WITNESS_DELTA) > 0.0,
        f"(sin delta)_samples=({math.sin(CANONICAL_DELTA):.12f},{math.sin(WITNESS_DELTA):.12f})",
    )
    check(
        "Equivalently, both samples already sit on the same positive projected-source odd sheet gamma > 0",
        c_gamma > 0.0 and w_gamma > 0.0,
        f"gamma_samples=({c_gamma:.12f},{w_gamma:.12f})",
    )


def part2_the_even_response_pair_still_varies_on_that_same_odd_sheet() -> None:
    print("\n" + "=" * 88)
    print("PART 2: THE EVEN-RESPONSE PAIR STILL VARIES ON THAT SAME ODD SHEET")
    print("=" * 88)

    _c_xbar, _c_ybar, _c_gamma, c_e1, c_e2 = triplet_data(
        CANONICAL_X, CANONICAL_Y, CANONICAL_DELTA
    )
    _w_xbar, _w_ybar, _w_gamma, w_e1, w_e2 = triplet_data(
        WITNESS_X, WITNESS_Y, WITNESS_DELTA
    )

    check(
        "The canonical near-closing sample remains on the negative even-response chamber",
        c_e1 < 0.0 and c_e2 < 0.0,
        f"(E1,E2)=({c_e1:.12f},{c_e2:.12f})",
    )
    check(
        "The constructive projected-source witness lies on the positive even-response chamber",
        w_e1 > 0.0 and w_e2 > 0.0,
        f"(E1,E2)=({w_e1:.12f},{w_e2:.12f})",
    )
    check(
        "So fixing the odd selector bit alone does not yet choose the constructive PMNS sheet",
        abs(c_e1 - w_e1) > 1e-6 and abs(c_e2 - w_e2) > 1e-6,
        "the remaining native object is not the odd bit anymore",
    )

    print()
    print("  canonical sample:")
    print(f"    (E1,E2)=({c_e1:.12f},{c_e2:.12f})")
    print("  constructive witness:")
    print(f"    (E1,E2)=({w_e1:.12f},{w_e2:.12f})")


def part3_the_remaining_object_is_equivalently_the_carrier_side_even_response_pair() -> None:
    print("\n" + "=" * 88)
    print("PART 3: CARRIER-SIDE EQUIVALENT OF THE SAME REMAINING OBJECT")
    print("=" * 88)

    _c_xbar, _c_ybar, c_gamma, c_e1, c_e2 = triplet_data(
        CANONICAL_X, CANONICAL_Y, CANONICAL_DELTA
    )
    _w_xbar, _w_ybar, w_gamma, w_e1, w_e2 = triplet_data(
        WITNESS_X, WITNESS_Y, WITNESS_DELTA
    )
    c_e1_car, c_e2_car, c_gamma_car, c_sigma_sin_2v = carrier_even_response(
        CANONICAL_X, CANONICAL_Y, CANONICAL_DELTA
    )
    w_e1_car, w_e2_car, w_gamma_car, w_sigma_sin_2v = carrier_even_response(
        WITNESS_X, WITNESS_Y, WITNESS_DELTA
    )

    check(
        "On the active PMNS family the carrier-side delta + rho coordinate equals E1 exactly",
        abs(c_e1_car - c_e1) < 1e-12 and abs(w_e1_car - w_e1) < 1e-12,
        f"carrier E1=({c_e1_car:.12f},{w_e1_car:.12f})",
    )
    check(
        "The carrier-side sigma sin(2v) channel is exactly equivalent to E2",
        abs(c_e2_car - c_e2) < 1e-12
        and abs(w_e2_car - w_e2) < 1e-12
        and abs(c_gamma_car - c_gamma) < 1e-12
        and abs(w_gamma_car - w_gamma) < 1e-12,
        f"sigma sin(2v)=({c_sigma_sin_2v:.12f},{w_sigma_sin_2v:.12f})",
    )
    check(
        "So after the odd bit is fixed, the remaining PMNS sole-axiom object is the even-response law (E1,E2), equivalently (delta + rho, sigma sin(2v))",
        c_e1_car < 0.0
        and c_sigma_sin_2v < 0.0
        and w_e1_car > 0.0
        and w_sigma_sin_2v > 0.0,
        "the residual native problem is even-response, not odd-sheet orientation",
    )


def part4_the_theorem_note_records_the_new_boundary_cleanly() -> None:
    print("\n" + "=" * 88)
    print("PART 4: THE THEOREM NOTE RECORDS THE NEW BOUNDARY")
    print("=" * 88)

    note = read(
        "docs/DM_LEPTOGENESIS_PMNS_EVEN_RESPONSE_SOLE_AXIOM_BOUNDARY_NOTE_2026-04-16.md"
    )

    check(
        "The new theorem note records that same-seed positive-phase samples can still carry opposite even-response pairs",
        "same exact native `N_e` seed surface" in note
        and "canonical:     E1 < 0, E2 < 0" in note
        and "constructive:  E1 > 0, E2 > 0" in note,
    )
    check(
        "The note identifies the residual native problem as the even-response law (E1,E2)",
        "remaining PMNS sole-axiom object" in note and "even-response law" in note and "`(E1, E2)`" in note,
    )


def main() -> int:
    print("=" * 88)
    print("DM LEPTOGENESIS PMNS EVEN-RESPONSE SOLE-AXIOM BOUNDARY")
    print("=" * 88)
    print()
    print("Question:")
    print("  After the residual PMNS sheet selector has been reduced to the odd bit")
    print("  sign(sin(delta)) on the fixed native seed surface, does the current")
    print("  sole-axiom bank already force the remaining even-response pair?")

    part1_the_fixed_native_seed_surface_and_positive_odd_bit_do_not_yet_close_the_pmns_object()
    part2_the_even_response_pair_still_varies_on_that_same_odd_sheet()
    part3_the_remaining_object_is_equivalently_the_carrier_side_even_response_pair()
    part4_the_theorem_note_records_the_new_boundary_cleanly()

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  Exact boundary answer:")
    print("    - no, not from the current sole axiom on the PMNS comparator lane")
    print("    - the odd sheet selector sign(sin(delta)) is already closed")
    print("    - the remaining native object is the even-response law for (E1,E2)")
    print("      equivalently the carrier-side pair (delta + rho, sigma sin(2v))")
    print()
    print(f"PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
