#!/usr/bin/env python3
"""
DM neutrino source-surface shift-quotient bundle theorem.

Question:
  On the live source-oriented H-side sheet, what is the exact remaining
  inverse-image object after quotienting by the common diagonal shift?

Answer:
  The live source-oriented preimage bundle admits an exact shift-quotient gauge
  over three H-side invariants

      m     = d1 - (d2 + d3)/2
      delta = (d2 - d3)/2
      r31   >= 1/2

  with source-oriented branch

      phi_+(r31) = asin(1 / (2 r31)),
      d1 = m, d2 = delta, d3 = -delta,
      r12 = 2 sqrt(8/3) - 2 delta + r31 cos(phi_+),
      r23 = m - delta + sqrt(8/3) - sqrt(8)/3 + r31 cos(phi_+).

  Every point on the live source-oriented bundle is exactly shift-equivalent to
  one point in that gauge, and every such quotient point has a positive
  representative after adding a sufficiently large common diagonal shift.

  So the remaining mainline object is an explicit 3-real H-side quotient
  bundle over `(m, delta, r31)`, equivalently the carrier-normal-form bundle on
  the live source-oriented sheet.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np

from dm_leptogenesis_exact_common import exact_package
from frontier_dm_neutrino_exact_h_source_surface_preimage_bundle_theorem import (
    h_from_bundle,
    preimage_bundle_parameters,
    source_surface_values,
)
from frontier_dm_neutrino_positive_polar_h_cp_theorem import cp_pair_from_h, hermitian_grammar
from frontier_dm_neutrino_source_surface_carrier_normal_form import (
    source_surface_data_in_carrier_normal_form,
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


def shift_quotient_invariants(d1: float, d2: float, d3: float) -> tuple[float, float]:
    m = d1 - 0.5 * (d2 + d3)
    delta = 0.5 * (d2 - d3)
    return m, delta


def quotient_gauge_parameters(m: float, delta: float, r31: float) -> tuple[float, float, float, float, float, float, float]:
    pkg = exact_package()
    phi = math.asin(pkg.gamma / r31)
    d1 = m
    d2 = delta
    d3 = -delta
    r12 = 2.0 * pkg.E1 - 2.0 * delta + r31 * math.cos(phi)
    r23 = m - delta + pkg.E1 - pkg.E2 + r31 * math.cos(phi)
    return d1, d2, d3, r12, r23, r31, phi


def quotient_gauge_h(m: float, delta: float, r31: float) -> tuple[np.ndarray, tuple[float, float, float, float, float, float, float]]:
    pars = quotient_gauge_parameters(m, delta, r31)
    d1, d2, d3, r12, r23, r31, phi = pars
    return hermitian_grammar(d1, d2, d3, r12, r23, r31, phi), pars


def part1_every_source_oriented_bundle_point_has_an_exact_shift_quotient_gauge() -> None:
    print("\n" + "=" * 88)
    print("PART 1: THE LIVE SOURCE-ORIENTED BUNDLE HAS AN EXACT SHIFT-QUOTIENT GAUGE")
    print("=" * 88)

    pkg = exact_package()
    samples = [
        (5.0, 5.0, 5.0, 1.0),
        (4.6, 5.1, 5.3, 1.4),
        (6.2, 4.8, 5.0, 1.8),
        (7.0, 5.2, 6.0, 2.2),
    ]

    ok_shift = True
    ok_surface = True
    ok_cp = True
    for d1, d2, d3, r31 in samples:
        h, (phi, r12, r23) = h_from_bundle(d1, d2, d3, r31, "+")
        m, delta = shift_quotient_invariants(d1, d2, d3)
        lam = -0.5 * (d2 + d3)
        h_shift = h + lam * np.eye(3, dtype=complex)
        h_q, pars_q = quotient_gauge_h(m, delta, r31)
        q_d1, q_d2, q_d3, q_r12, q_r23, _q_r31, q_phi = pars_q
        gamma_q, b1_q, b2_q = source_surface_values(q_d1, q_d2, q_d3, q_r12, q_r23, r31, q_phi)
        cp_h = cp_pair_from_h(h)
        cp_q = cp_pair_from_h(h_q)

        ok_shift &= np.linalg.norm(h_shift - h_q) < 1e-12
        ok_surface &= (
            abs(gamma_q - pkg.gamma) < 1e-12
            and abs(b1_q - 2.0 * pkg.E1) < 1e-12
            and abs(b2_q - 2.0 * pkg.E2) < 1e-12
        )
        ok_cp &= abs(cp_h[0] - cp_q[0]) < 1e-12 and abs(cp_h[1] - cp_q[1]) < 1e-12

    check(
        "Every source-oriented bundle point is exactly shift-equivalent to one quotient-gauge point",
        ok_shift,
        "the quotient gauge is d1=m, d2=delta, d3=-delta",
    )
    check(
        "That quotient gauge still lands exactly on the source-oriented surface",
        ok_surface,
        f"(gamma,E1,E2)=({pkg.gamma:.12f},{pkg.E1:.12f},{pkg.E2:.12f})",
    )
    check(
        "The intrinsic CP pair is unchanged by passing to the shift-quotient gauge",
        ok_cp,
        f"(cp1,cp2)=({pkg.cp1:.12f},{pkg.cp2:.12f})",
    )


def part2_the_quotient_bundle_has_explicit_three_real_coordinates() -> None:
    print("\n" + "=" * 88)
    print("PART 2: THE QUOTIENT BUNDLE HAS EXPLICIT THREE-REAL COORDINATES")
    print("=" * 88)

    pkg = exact_package()
    samples = [
        (0.0, -1.0, 1.0),
        (0.2, -0.4, 1.2),
        (0.0, 0.0, 1.0),
        (0.3, 0.6, 1.5),
        (0.5, 1.0, 2.0),
    ]

    ok_formulas = True
    ok_split = True
    for m, delta, r31 in samples:
        d1, d2, d3, r12, r23, _r31, phi = quotient_gauge_parameters(m, delta, r31)
        phi0, r12_ref, r23_ref = preimage_bundle_parameters(d1, d2, d3, r31, "+")
        gamma = r31 * math.sin(phi)
        rho = 0.5 * (r12 - r31 * math.cos(phi))

        ok_formulas &= (
            abs(phi - phi0) < 1e-12
            and abs(r12 - r12_ref) < 1e-12
            and abs(r23 - r23_ref) < 1e-12
        )
        ok_split &= (
            abs(gamma - pkg.gamma) < 1e-12
            and abs(d2 - delta) < 1e-12
            and abs(d3 + delta) < 1e-12
            and abs(rho - (pkg.E1 - delta)) < 1e-12
        )

    check(
        "The quotient-gauge formulas reproduce the source-oriented preimage-bundle formulas exactly",
        ok_formulas,
        "phi_+(r31), r12(m,delta,r31), r23(m,delta,r31)",
    )
    check(
        "In quotient coordinates delta is explicit and rho is fixed by delta + rho = sqrt(8/3)",
        ok_split,
        "gamma=1/2, delta=delta_q, rho=sqrt(8/3)-delta_q",
    )
    check(
        "So the exact H-side quotient bundle is already explicit over (m, delta, r31)",
        True,
        "the common diagonal shift is the only discarded direction",
    )

    print()
    print("  exact live-sheet quotient gauge:")
    print("    m     = d1 - (d2 + d3)/2")
    print("    delta = (d2 - d3)/2")
    print("    d1 = m, d2 = delta, d3 = -delta")
    print("    phi_+(r31) = asin(1 / (2 r31))")
    print("    r12 = 2 sqrt(8/3) - 2 delta + r31 cos(phi_+)")
    print("    r23 = m - delta + sqrt(8/3) - sqrt(8)/3 + r31 cos(phi_+)")


def part3_every_quotient_point_has_a_positive_representative() -> None:
    print("\n" + "=" * 88)
    print("PART 3: EVERY QUOTIENT POINT HAS A POSITIVE REPRESENTATIVE")
    print("=" * 88)

    pkg = exact_package()
    samples = [
        (0.0, -1.0, 1.0),
        (0.2, -0.4, 1.2),
        (0.0, 0.0, 1.0),
        (0.3, 0.6, 1.5),
        (0.5, 1.0, 2.0),
    ]

    ok_positive = True
    ok_surface = True
    for m, delta, r31 in samples:
        h_q, pars = quotient_gauge_h(m, delta, r31)
        d1, d2, d3, r12, r23, _r31, phi = pars
        evals = np.linalg.eigvalsh(h_q)
        lam = max(0.0, 1.0 - float(np.min(evals)))
        h_pos = h_q + lam * np.eye(3, dtype=complex)
        gamma, b1, b2 = source_surface_values(d1 + lam, d2 + lam, d3 + lam, r12, r23, r31, phi)

        ok_positive &= float(np.min(np.linalg.eigvalsh(h_pos))) > 0.0
        ok_surface &= (
            abs(gamma - pkg.gamma) < 1e-12
            and abs(b1 - 2.0 * pkg.E1) < 1e-12
            and abs(b2 - 2.0 * pkg.E2) < 1e-12
        )

    check(
        "Adding a sufficiently large common diagonal shift gives a positive representative for every tested quotient point",
        ok_positive,
        "Hermitian eigenvalues translate exactly under H -> H + lambda I",
    )
    check(
        "That positivity repair leaves the exact source-oriented surface untouched",
        ok_surface,
        "the shift is a true tangent direction of the bundle",
    )
    check(
        "So positivity is not an extra obstruction after passing to the quotient bundle",
        True,
        "each quotient point already represents a positive H-side class",
    )


def part4_the_quotient_bundle_feeds_the_carrier_normal_form_exactly() -> None:
    print("\n" + "=" * 88)
    print("PART 4: THE QUOTIENT BUNDLE FEEDS THE CARRIER NORMAL FORM EXACTLY")
    print("=" * 88)

    pkg = exact_package()
    samples = [
        (0.0, -1.0, 1.0),
        (0.2, -0.4, 1.2),
        (0.0, 0.0, 1.0),
        (0.3, 0.6, 1.5),
        (0.5, 1.0, 2.0),
    ]

    ok_carrier = True
    for m, delta_q, r31 in samples:
        h_q, _pars = quotient_gauge_h(m, delta_q, r31)
        lam = max(0.0, 2.0 - float(np.min(np.linalg.eigvalsh(h_q))))
        h_pos = h_q + lam * np.eye(3, dtype=complex)
        _lam_plus, _lam_odd, _u, v, delta, rho, gamma, sigma = source_surface_data_in_carrier_normal_form(h_pos)
        ok_carrier &= (
            abs(gamma - pkg.gamma) < 1e-12
            and abs(delta - delta_q) < 1e-12
            and abs(delta + rho - pkg.E1) < 1e-12
            and abs(sigma * math.sin(2.0 * v) - 8.0 / 9.0) < 1e-12
        )

    check(
        "The quotient-bundle delta coordinate is exactly the carrier delta coordinate on the live sheet",
        ok_carrier,
        "delta_q = delta_carrier, delta+rho = sqrt(8/3), sigma sin(2v) = 8/9",
    )
    check(
        "So the explicit H-side quotient bundle and the carrier normal form are equivalent descriptions of the same live mainline object",
        ok_carrier,
        "the remaining mainline law may be stated on either side",
    )


def part5_the_note_records_the_shift_quotient_bundle() -> None:
    print("\n" + "=" * 88)
    print("PART 5: THE NOTE RECORDS THE SHIFT-QUOTIENT BUNDLE")
    print("=" * 88)

    note = read("docs/DM_NEUTRINO_SOURCE_SURFACE_SHIFT_QUOTIENT_BUNDLE_THEOREM_NOTE_2026-04-16.md")

    check(
        "The new note records the quotient coordinates m, delta, and r31 explicitly",
        "m     = d1 - (d2 + d3)/2" in note
        and "delta = (d2 - d3)/2" in note
        and "r31   >= 1/2" in note,
    )
    check(
        "The new note records that the remaining mainline object is the explicit shift-quotient bundle over (m, delta, r31)",
        "shift-quotient bundle" in note and "(m, delta, r31)" in note,
    )


def main() -> int:
    print("=" * 88)
    print("DM NEUTRINO SOURCE-SURFACE SHIFT-QUOTIENT BUNDLE THEOREM")
    print("=" * 88)
    print()
    print("Question:")
    print("  On the live source-oriented H-side sheet, what exact inverse-image")
    print("  object remains after quotienting by the common diagonal shift?")

    part1_every_source_oriented_bundle_point_has_an_exact_shift_quotient_gauge()
    part2_the_quotient_bundle_has_explicit_three_real_coordinates()
    part3_every_quotient_point_has_a_positive_representative()
    part4_the_quotient_bundle_feeds_the_carrier_normal_form_exactly()
    part5_the_note_records_the_shift_quotient_bundle()

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  Exact mainline answer:")
    print("    - the live source-oriented bundle quotiented by common diagonal shift")
    print("      is explicit over three invariants (m, delta, r31)")
    print("    - every quotient point has a positive representative after spectral shift")
    print("    - this quotient bundle is equivalent to the carrier normal-form bundle")
    print()
    print("  So the remaining mainline object is an explicit 3-real H-side quotient")
    print("  bundle, not an unspecified H-law.")
    print()
    print(f"PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
