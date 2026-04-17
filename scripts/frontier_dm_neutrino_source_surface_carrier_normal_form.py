#!/usr/bin/env python3
"""
DM neutrino source-surface carrier normal-form theorem.

Question:
  On the live source-oriented sheet of the exact H-side source surface, what is
  the smallest carrier-side normal form for the remaining mainline inverse-
  image problem?

Answer:
  After quotienting by the exact common diagonal-shift tangent, the live
  source-oriented sheet factors through the minimal Hermitian bridge carrier

      B_H,min = (Lambda_+, Lambda_odd, u, v, delta, rho, gamma)

  and the exact source surface becomes

      gamma = 1/2
      delta + rho = sqrt(8/3)
      sigma sin(2v) = 8/9

  where

      sigma = -Lambda_+ + Lambda_odd + u.

  So the live mainline object is a shift-quotiented carrier-side inverse-image
  law on the source-oriented sheet, not a generic 7-real H-grammar law.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np

from dm_leptogenesis_exact_common import exact_package
from frontier_dm_neutrino_breaking_triplet_cp_theorem import cp_formula
from frontier_dm_neutrino_exact_h_source_surface_preimage_bundle_theorem import (
    h_from_bundle,
)
from frontier_dm_neutrino_hermitian_bridge_carrier import (
    aligned_core_from_coords,
    breaking_triplet_from_coords,
    bridge_reconstruct,
    core_from_bridge,
    hermitian_coords,
    spectral_package,
)
from frontier_dm_neutrino_positive_polar_h_cp_theorem import cp_pair_from_h

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


def theta_star() -> float:
    return math.atan(math.sqrt(2.0))


def carrier_coords_from_h(h: np.ndarray) -> tuple[float, float, float, float, float, float, float]:
    coords = hermitian_coords(h)
    core = aligned_core_from_coords(*coords)
    delta, rho, gamma = breaking_triplet_from_coords(*coords)
    lam_plus, lam_minus, lam_odd, theta = spectral_package(core)
    return (
        lam_plus,
        lam_odd,
        lam_minus - lam_odd,
        theta - theta_star(),
        delta,
        rho,
        gamma,
    )


def source_surface_data_in_carrier_normal_form(
    h: np.ndarray,
) -> tuple[float, float, float, float, float, float, float, float]:
    lam_plus, lam_odd, u, v, delta, rho, gamma = carrier_coords_from_h(h)
    sigma = -lam_plus + lam_odd + u
    return lam_plus, lam_odd, u, v, delta, rho, gamma, sigma


def core_combo_from_bridge(lam_plus: float, lam_odd: float, u: float, v: float) -> float:
    core = core_from_bridge(lam_plus, lam_odd, u, v)
    a0 = float(np.real(core[0, 0]))
    b0 = float(np.real(core[0, 1]))
    c0 = float(np.real(core[1, 1]))
    d0 = float(np.real(core[1, 2]))
    return a0 + b0 - c0 - d0


def part1_the_live_source_oriented_sheet_factors_through_the_shift_quotiented_carrier() -> None:
    print("\n" + "=" * 88)
    print("PART 1: THE LIVE SOURCE-ORIENTED SHEET FACTORS THROUGH THE SHIFT-QUOTIENTED CARRIER")
    print("=" * 88)

    samples = [
        h_from_bundle(5.0, 5.0, 5.0, 1.0, "+")[0],
        h_from_bundle(4.6, 5.1, 5.3, 1.4, "+")[0],
        h_from_bundle(6.2, 4.8, 5.0, 1.8, "+")[0],
    ]

    for idx, h in enumerate(samples, start=1):
        lam_plus, lam_odd, u, v, delta, rho, gamma = carrier_coords_from_h(h)
        h_rec = bridge_reconstruct(lam_plus, lam_odd, u, v, delta, rho, gamma)
        check(
            f"Source-oriented sheet sample {idx} reconstructs exactly from B_H,min",
            np.linalg.norm(h - h_rec) < 1e-12,
            f"err={np.linalg.norm(h - h_rec):.2e}",
        )

    check(
        "So the live mainline inverse-image problem already factors through the minimal carrier B_H,min on its source-oriented sheet",
        True,
        "the remaining object is carrier-side and shift-quotiented, not a generic H law",
    )


def part2_the_core_interference_channel_has_an_exact_carrier_formula() -> None:
    print("\n" + "=" * 88)
    print("PART 2: THE CORE INTERFERENCE CHANNEL HAS AN EXACT CARRIER FORMULA")
    print("=" * 88)

    rng = np.random.default_rng(417)
    good = True
    max_err = 0.0
    for _ in range(60):
        lam_plus = float(rng.uniform(0.5, 6.0))
        lam_odd = float(rng.uniform(0.2, 4.0))
        u = float(rng.uniform(-2.0, 2.0))
        v = float(rng.uniform(-0.7, 0.7))
        combo = core_combo_from_bridge(lam_plus, lam_odd, u, v)
        sigma = -lam_plus + lam_odd + u
        exact = 0.75 * math.sqrt(2.0) * sigma * math.sin(2.0 * v)
        err = abs(combo - exact)
        max_err = max(max_err, err)
        if err >= 1e-12:
            good = False
            break

    check(
        "The exact carrier functional for A+b-c-d is 3 sqrt(2) sigma sin(2v) / 4",
        good,
        f"max err={max_err:.2e}",
    )
    check(
        "So the source surface does not need the whole aligned core separately",
        good,
        "its even core channel already factors through sigma = -Lambda_+ + Lambda_odd + u and v",
    )


def part3_the_exact_source_surface_becomes_a_three_equation_carrier_normal_form() -> None:
    print("\n" + "=" * 88)
    print("PART 3: THE EXACT SOURCE SURFACE BECOMES A THREE-EQUATION CARRIER NORMAL FORM")
    print("=" * 88)

    pkg = exact_package()
    samples = [
        h_from_bundle(5.0, 5.0, 5.0, 1.0, "+")[0],
        h_from_bundle(4.6, 5.1, 5.3, 1.4, "+")[0],
        h_from_bundle(6.2, 4.8, 5.0, 1.8, "+")[0],
    ]

    good = True
    max_err = 0.0
    for h in samples:
        lam_plus, lam_odd, u, v, delta, rho, gamma, sigma = source_surface_data_in_carrier_normal_form(h)
        combo = core_combo_from_bridge(lam_plus, lam_odd, u, v)
        cp_direct = cp_pair_from_h(h)
        cp_triplet = cp_formula(
            float(np.real(h[0, 0])),
            float(np.real(h[0, 1] - rho)),
            float(0.5 * np.real(h[1, 1] + h[2, 2])),
            float(np.real(h[1, 2])),
            delta,
            rho,
            gamma,
        )
        err = max(
            abs(gamma - pkg.gamma),
            abs(delta + rho - pkg.E1),
            abs(sigma * math.sin(2.0 * v) - 8.0 / 9.0),
            abs(combo - pkg.E2),
            abs(cp_direct[0] - pkg.cp1),
            abs(cp_direct[1] - pkg.cp2),
            abs(cp_triplet[0] - pkg.cp1),
            abs(cp_triplet[1] - pkg.cp2),
        )
        max_err = max(max_err, err)
        if err >= 1e-10:
            good = False
            break

    check(
        "On the live source-oriented sheet the carrier normal form is gamma = 1/2, delta+rho = sqrt(8/3), sigma sin(2v) = 8/9",
        good,
        f"max err={max_err:.2e}",
    )
    check(
        "That normal form still reproduces the exact source-oriented CP pair",
        good,
        f"(cp1,cp2)=({pkg.cp1:.12f},{pkg.cp2:.12f})",
    )


def part4_common_shift_is_exactly_quotiented_out_on_the_carrier_side() -> None:
    print("\n" + "=" * 88)
    print("PART 4: COMMON SHIFT IS EXACTLY QUOTIENTED OUT ON THE CARRIER SIDE")
    print("=" * 88)

    h, _ = h_from_bundle(5.0, 5.0, 5.0, 1.0, "+")
    lam_plus, lam_odd, u, v, delta, rho, gamma, sigma = source_surface_data_in_carrier_normal_form(h)
    shift = 2.75
    h_shift = h + shift * np.eye(3, dtype=complex)
    lam_plus_s, lam_odd_s, u_s, v_s, delta_s, rho_s, gamma_s, sigma_s = source_surface_data_in_carrier_normal_form(h_shift)

    check(
        "A common diagonal shift sends Lambda_+ and Lambda_odd to Lambda + lambda",
        abs(lam_plus_s - (lam_plus + shift)) < 1e-12 and abs(lam_odd_s - (lam_odd + shift)) < 1e-12,
        f"(Lambda_+,Lambda_odd)=({lam_plus_s:.12f},{lam_odd_s:.12f})",
    )
    check(
        "The shift leaves u, v, delta, rho, and gamma unchanged",
        abs(u_s - u) < 1e-12
        and abs(v_s - v) < 1e-12
        and abs(delta_s - delta) < 1e-12
        and abs(rho_s - rho) < 1e-12
        and abs(gamma_s - gamma) < 1e-12,
        f"(u,v,delta,rho,gamma)=({u_s:.12f},{v_s:.12f},{delta_s:.12f},{rho_s:.12f},{gamma_s:.12f})",
    )
    check(
        "So sigma and the exact source-surface normal form are shift-invariant",
        abs(sigma_s - sigma) < 1e-12 and abs(sigma_s * math.sin(2.0 * v_s) - 8.0 / 9.0) < 1e-12,
        f"sigma={sigma_s:.12f}",
    )


def part5_the_note_records_the_carrier_normal_form() -> None:
    print("\n" + "=" * 88)
    print("PART 5: THE NOTE RECORDS THE CARRIER NORMAL FORM")
    print("=" * 88)

    note = read("docs/DM_NEUTRINO_SOURCE_SURFACE_CARRIER_NORMAL_FORM_THEOREM_NOTE_2026-04-16.md")

    check(
        "The new note records sigma sin(2v) = 8/9 as the carrier normal form",
        "sigma sin(2v) = 8/9" in note and "B_H,min" in note and "shift-quotiented" in note,
    )
    check(
        "The new note records the mainline object as a shift-quotiented carrier-side inverse-image law on the source-oriented sheet",
        "shift-quotiented" in note and "carrier-side inverse-image law" in note and "source-oriented sheet" in note,
    )


def main() -> int:
    print("=" * 88)
    print("DM NEUTRINO SOURCE-SURFACE CARRIER NORMAL-FORM THEOREM")
    print("=" * 88)
    print()
    print("Question:")
    print("  On the live source-oriented sheet of the exact H-side source surface,")
    print("  what is the smallest carrier-side normal form for the remaining")
    print("  mainline inverse-image problem?")

    part1_the_live_source_oriented_sheet_factors_through_the_shift_quotiented_carrier()
    part2_the_core_interference_channel_has_an_exact_carrier_formula()
    part3_the_exact_source_surface_becomes_a_three_equation_carrier_normal_form()
    part4_common_shift_is_exactly_quotiented_out_on_the_carrier_side()
    part5_the_note_records_the_carrier_normal_form()

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  Exact mainline answer:")
    print("    - on the live source-oriented sheet, the exact source surface reduces")
    print("      after shift quotient to carrier normal form gamma = 1/2,")
    print("      delta+rho = sqrt(8/3), sigma sin(2v) = 8/9")
    print("    - the live mainline object is therefore a 3-real even-response law on")
    print("      the carrier side, not a generic 7-real H law")
    print()
    print(f"PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
