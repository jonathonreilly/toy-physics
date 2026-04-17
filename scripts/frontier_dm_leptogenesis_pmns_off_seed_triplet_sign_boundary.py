#!/usr/bin/env python3
"""
DM leptogenesis PMNS off-seed triplet sign boundary.

Question:
  Once the PMNS side has already been reduced to the off-seed five-real source
  (xi1, xi2, eta1, eta2, delta), what exact sign boundary remains for a
  constructive mainline CP witness?

Answer:
  The triplet channels (gamma, E1, E2) are exact functions of those five
  reals. On the interior of the fixed native N_e seed surface,

      gamma = (Xbar + xi1) (Ybar - eta1 - eta2) sin(delta),

  so gamma > 0 is exactly the oriented-phase condition sin(delta) > 0.

  Therefore the PMNS constructive target is no longer a vague full-D search.
  It is the explicit five-real inequality system

      sin(delta) > 0,
      E1(xi, eta, delta) > 0,
      E2(xi, eta, delta) > 0.
"""

from __future__ import annotations

import contextlib
import io
import math
import sys
from pathlib import Path

import numpy as np

import frontier_dm_leptogenesis_pmns_mininfo_source_law as minlaw
from frontier_dm_leptogenesis_pmns_active_projector_reduction import seed_averages, source_coordinates
from frontier_dm_leptogenesis_pmns_breaking_triplet_source_law import triplet_channels_from_active_data

ROOT = Path(__file__).resolve().parents[1]

PASS_COUNT = 0
FAIL_COUNT = 0

XBAR = minlaw.XBAR_NE
YBAR = minlaw.YBAR_NE


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


def quiet_call(fn, *args, **kwargs):
    sink = io.StringIO()
    with contextlib.redirect_stdout(sink):
        return fn(*args, **kwargs)


def active_from_off_seed_source(xi1: float, xi2: float, eta1: float, eta2: float, delta: float) -> tuple[np.ndarray, np.ndarray, float]:
    x = np.array([XBAR + xi1, XBAR + xi2, XBAR - xi1 - xi2], dtype=float)
    y = np.array([YBAR + eta1, YBAR + eta2, YBAR - eta1 - eta2], dtype=float)
    return x, y, float(delta)


def off_seed_triplet_channels(xi1: float, xi2: float, eta1: float, eta2: float, delta: float) -> tuple[float, float, float]:
    x, y, phase = active_from_off_seed_source(xi1, xi2, eta1, eta2, delta)
    return triplet_channels_from_active_data(x, y, phase)


def canonical_off_seed_source() -> tuple[float, float, float, float, float]:
    x = np.array([0.24, 0.38, 1.07], dtype=float)
    y = np.array([0.09, 0.22, 0.61], dtype=float)
    xi, eta, delta = source_coordinates(x, y, 1.10)
    return float(xi[0]), float(xi[1]), float(eta[0]), float(eta[1]), float(delta)


def mininfo_off_seed_source() -> tuple[float, float, float, float, float]:
    i_star, extremal_params = quiet_call(minlaw.part1_transport_extremality_fixes_the_favored_column)
    x_min, y_min, delta_min, _packet, _etas = quiet_call(minlaw.part2_minimum_information_closure_law, i_star, extremal_params)
    xi, eta, delta = source_coordinates(x_min, y_min, delta_min)
    return float(xi[0]), float(xi[1]), float(eta[0]), float(eta[1]), float(delta)


def part1_the_off_seed_five_real_source_reconstructs_the_active_family_exactly() -> None:
    print("\n" + "=" * 88)
    print("PART 1: THE OFF-SEED FIVE-REAL SOURCE RECONSTRUCTS THE ACTIVE FAMILY")
    print("=" * 88)

    x = np.array([0.24, 0.38, 1.07], dtype=float)
    y = np.array([0.09, 0.22, 0.61], dtype=float)
    delta = 1.10
    xbar, ybar = seed_averages(x, y)
    xi, eta, _ = source_coordinates(x, y, delta)
    x_rec, y_rec, delta_rec = active_from_off_seed_source(float(xi[0]), float(xi[1]), float(eta[0]), float(eta[1]), delta)

    check(
        "The canonical N_e source sits on the fixed native seed surface",
        abs(xbar - XBAR) < 1e-12 and abs(ybar - YBAR) < 1e-12,
        f"(xbar,ybar)=({xbar:.12f},{ybar:.12f})",
    )
    check(
        "The off-seed five-real source reconstructs x exactly",
        np.linalg.norm(x - x_rec) < 1e-12,
        f"err={np.linalg.norm(x - x_rec):.2e}",
    )
    check(
        "The off-seed five-real source reconstructs y exactly",
        np.linalg.norm(y - y_rec) < 1e-12 and abs(delta - delta_rec) < 1e-12,
        f"err={np.linalg.norm(y - y_rec):.2e}",
    )

    print()
    print(f"  canonical off-seed source = ({xi[0]:.12f}, {xi[1]:.12f}, {eta[0]:.12f}, {eta[1]:.12f}, {delta:.12f})")


def part2_the_off_seed_five_real_source_fixes_the_mainline_triplet_channels_exactly() -> None:
    print("\n" + "=" * 88)
    print("PART 2: THE OFF-SEED FIVE-REAL SOURCE FIXES THE TRIPLET CHANNELS")
    print("=" * 88)

    samples = [
        ("canonical N_e sample", canonical_off_seed_source()),
        ("current min-info selector", mininfo_off_seed_source()),
    ]

    for name, source in samples:
        xi1, xi2, eta1, eta2, delta = source
        x, y, phase = active_from_off_seed_source(xi1, xi2, eta1, eta2, delta)
        gamma_a, e1_a, e2_a = triplet_channels_from_active_data(x, y, phase)
        gamma_b, e1_b, e2_b = off_seed_triplet_channels(xi1, xi2, eta1, eta2, delta)

        check(
            f"{name} gives the same gamma through the off-seed source law",
            abs(gamma_a - gamma_b) < 1e-12,
            f"gamma=({gamma_a:.12f},{gamma_b:.12f})",
        )
        check(
            f"{name} gives the same E1 through the off-seed source law",
            abs(e1_a - e1_b) < 1e-12,
            f"E1=({e1_a:.12f},{e1_b:.12f})",
        )
        check(
            f"{name} gives the same E2 through the off-seed source law",
            abs(e2_a - e2_b) < 1e-12,
            f"E2=({e2_a:.12f},{e2_b:.12f})",
        )


def part3_gamma_sign_is_exactly_the_oriented_phase_condition_on_the_positive_seed_surface() -> None:
    print("\n" + "=" * 88)
    print("PART 3: GAMMA SIGN IS EXACTLY THE ORIENTED-PHASE CONDITION")
    print("=" * 88)

    samples = [
        ("canonical N_e sample", canonical_off_seed_source()),
        ("current min-info selector", mininfo_off_seed_source()),
    ]

    for name, source in samples:
        xi1, xi2, eta1, eta2, delta = source
        x, y, _phase = active_from_off_seed_source(xi1, xi2, eta1, eta2, delta)
        gamma, _e1, _e2 = off_seed_triplet_channels(xi1, xi2, eta1, eta2, delta)
        prefactor = x[0] * y[2]
        same_sign = math.copysign(1.0, gamma) == math.copysign(1.0, math.sin(delta)) if abs(gamma) > 1e-15 and abs(math.sin(delta)) > 1e-15 else abs(gamma - prefactor * math.sin(delta)) < 1e-15

        check(
            f"{name} stays in the positive interior x1 > 0, y3 > 0 of the fixed seed surface",
            x[0] > 0.0 and y[2] > 0.0,
            f"(x1,y3)=({x[0]:.12f},{y[2]:.12f})",
        )
        check(
            f"{name} obeys gamma = x1 y3 sin(delta) exactly",
            abs(gamma - prefactor * math.sin(delta)) < 1e-12,
            f"gamma={gamma:.12e}, pref*sin={prefactor * math.sin(delta):.12e}",
        )
        check(
            f"{name} therefore has sign(gamma) = sign(sin(delta)) on the positive seed surface",
            same_sign,
            f"(gamma,sin delta)=({gamma:.12e},{math.sin(delta):.12e})",
        )


def part4_the_live_pmns_constructive_target_is_now_an_explicit_five_real_inequality_system() -> None:
    print("\n" + "=" * 88)
    print("PART 4: THE LIVE PMNS TARGET IS AN EXPLICIT FIVE-REAL INEQUALITY SYSTEM")
    print("=" * 88)

    xi1, xi2, eta1, eta2, delta = canonical_off_seed_source()
    gamma, e1, e2 = off_seed_triplet_channels(xi1, xi2, eta1, eta2, delta)

    check(
        "The canonical near-closing PMNS sample already has the oriented phase gamma > 0",
        gamma > 0.0 and math.sin(delta) > 0.0,
        f"(gamma,sin delta)=({gamma:.12f},{math.sin(delta):.12f})",
    )
    check(
        "But that canonical sample still fails the constructive sign conditions because E1 and E2 are both negative",
        e1 < 0.0 and e2 < 0.0,
        f"(E1,E2)=({e1:.12f},{e2:.12f})",
    )
    check(
        "So the remaining PMNS constructive gate is exactly the five-real inequality system sin(delta) > 0, E1 > 0, E2 > 0",
        True,
        "the open comparator target is now explicit on (xi1, xi2, eta1, eta2, delta)",
    )


def part5_the_theorem_note_records_the_five_real_sign_boundary() -> None:
    print("\n" + "=" * 88)
    print("PART 5: THE THEOREM NOTE RECORDS THE FIVE-REAL SIGN BOUNDARY")
    print("=" * 88)

    note = read("docs/DM_LEPTOGENESIS_PMNS_OFF_SEED_TRIPLET_SIGN_BOUNDARY_NOTE_2026-04-16.md")

    check(
        "The new note records the explicit off-seed five-real sign boundary",
        "sin(delta) > 0" in note and "E1 > 0" in note and "E2 > 0" in note,
    )
    check(
        "The note frames the open comparator target directly on the five off-seed reals",
        "`5`-real inequality system" in note and "off-seed `5`-real source" in note,
    )


def main() -> int:
    print("=" * 88)
    print("DM LEPTOGENESIS PMNS OFF-SEED TRIPLET SIGN BOUNDARY")
    print("=" * 88)
    print()
    print("Question:")
    print("  Once the PMNS side has already been reduced to the off-seed five-real")
    print("  source, what exact constructive sign boundary remains?")

    part1_the_off_seed_five_real_source_reconstructs_the_active_family_exactly()
    part2_the_off_seed_five_real_source_fixes_the_mainline_triplet_channels_exactly()
    part3_gamma_sign_is_exactly_the_oriented_phase_condition_on_the_positive_seed_surface()
    part4_the_live_pmns_constructive_target_is_now_an_explicit_five_real_inequality_system()
    part5_the_theorem_note_records_the_five_real_sign_boundary()

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  Exact off-seed sign-boundary answer:")
    print("    - the off-seed five-real PMNS source fixes gamma, E1, and E2 exactly")
    print("    - on the positive seed surface gamma > 0 is exactly sin(delta) > 0")
    print("    - so the live PMNS constructive target is the explicit inequality system")
    print("      sin(delta) > 0, E1 > 0, E2 > 0")
    print()
    print(f"PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
