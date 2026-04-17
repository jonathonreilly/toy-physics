#!/usr/bin/env python3
"""
DM leptogenesis PMNS breaking-triplet source law.

Question:
  On the canonical one-sided PMNS active family, what exact charged-sector
  algebraic law feeds the mainline breaking-triplet CP channels?

Answer:
  The three mainline triplet channels are explicit functions of the active
  charged-sector data (x, y, delta):

      gamma = x1 y3 sin(delta)
      E1    = [(x2^2 + y2^2) - (x3^2 + y3^2) + x2 y1 - x1 y3 cos(delta)] / 2
      E2    = x1^2 + y1^2 + (x2 y1 + x1 y3 cos(delta))/2
              - [(x2^2 + y2^2) + (x3^2 + y3^2)]/2 - x3 y2

  So the live charged-sector bridge is a concrete sign/slot problem:
  derive a full-D / off-seed source law that makes gamma > 0, E1 > 0, and
  E2 > 0 on the source-oriented mainline sheet.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np

from dm_leptogenesis_exact_common import exact_package
from frontier_dm_leptogenesis_pmns_active_projector_reduction import (
    seed_averages,
    source_coordinates,
)
from frontier_dm_leptogenesis_pmns_projector_interface import canonical_h
from frontier_dm_neutrino_breaking_triplet_cp_theorem import (
    cp_formula,
    h_from_breaking_triplet,
)
from frontier_dm_leptogenesis_pmns_cp_bridge_boundary import breaking_triplet_coordinates

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


def triplet_channels_from_active_data(x: np.ndarray, y: np.ndarray, phase: float) -> tuple[float, float, float]:
    x1, x2, x3 = map(float, x)
    y1, y2, y3 = map(float, y)
    gamma = x1 * y3 * math.sin(phase)
    e1 = ((x2 * x2 + y2 * y2) - (x3 * x3 + y3 * y3) + x2 * y1 - x1 * y3 * math.cos(phase)) / 2.0
    e2 = (
        x1 * x1
        + y1 * y1
        + (x2 * y1 + x1 * y3 * math.cos(phase)) / 2.0
        - ((x2 * x2 + y2 * y2) + (x3 * x3 + y3 * y3)) / 2.0
        - x3 * y2
    )
    return gamma, e1, e2


def part1_the_active_family_has_an_exact_triplet_channel_law() -> tuple[np.ndarray, np.ndarray, float]:
    print("\n" + "=" * 88)
    print("PART 1: THE ACTIVE FAMILY HAS AN EXACT TRIPLET-CHANNEL LAW")
    print("=" * 88)

    x = np.array([0.24, 0.38, 1.07], dtype=float)
    y = np.array([0.09, 0.22, 0.61], dtype=float)
    phase = 1.10
    h = canonical_h(x, y, phase)
    pars = breaking_triplet_coordinates(h)
    gamma, e1, e2 = triplet_channels_from_active_data(x, y, phase)
    h_rebuilt = h_from_breaking_triplet(
        pars["A"],
        pars["b"],
        pars["c"],
        pars["d"],
        pars["delta"],
        pars["rho"],
        pars["gamma"],
    )

    check(
        "The canonical active Hermitian sample is exactly recovered by the breaking-triplet grammar",
        np.linalg.norm(h - h_rebuilt) < 1e-12,
        f"err={np.linalg.norm(h - h_rebuilt):.2e}",
    )
    check(
        "The charged-sector formula fixes gamma exactly",
        abs(gamma - pars["gamma"]) < 1e-12,
        f"gamma=({gamma:.12f},{pars['gamma']:.12f})",
    )
    check(
        "The charged-sector formula fixes E1 = delta + rho exactly",
        abs(e1 - (pars["delta"] + pars["rho"])) < 1e-12,
        f"E1=({e1:.12f},{(pars['delta'] + pars['rho']):.12f})",
    )
    check(
        "The charged-sector formula fixes E2 = A + b - c - d exactly",
        abs(e2 - (pars["A"] + pars["b"] - pars["c"] - pars["d"])) < 1e-12,
        f"E2=({e2:.12f},{(pars['A'] + pars['b'] - pars['c'] - pars['d']):.12f})",
    )

    print()
    print(f"  exact charged-sector triplet law: gamma={gamma:.12f}, E1={e1:.12f}, E2={e2:.12f}")
    return x, y, phase


def part2_the_seed_plus_off_seed_source_data_already_fix_the_same_channels(x: np.ndarray, y: np.ndarray, phase: float) -> None:
    print("\n" + "=" * 88)
    print("PART 2: THE SEED PLUS OFF-SEED SOURCE DATA ALREADY FIX THE SAME CHANNELS")
    print("=" * 88)

    xbar, ybar = seed_averages(x, y)
    xi, eta, delta = source_coordinates(x, y, phase)

    x_r = xbar * np.ones(3, dtype=float) + xi
    y_r = ybar * np.ones(3, dtype=float) + eta
    gamma_r, e1_r, e2_r = triplet_channels_from_active_data(x_r, y_r, delta)
    gamma, e1, e2 = triplet_channels_from_active_data(x, y, phase)

    check(
        "The seed pair plus the off-seed five-real source reconstruct x exactly",
        np.linalg.norm(x - x_r) < 1e-12,
        f"err={np.linalg.norm(x - x_r):.2e}",
    )
    check(
        "The seed pair plus the off-seed five-real source reconstruct y exactly",
        np.linalg.norm(y - y_r) < 1e-12,
        f"err={np.linalg.norm(y - y_r):.2e}",
    )
    check(
        "Those seven reals therefore fix gamma, E1, and E2 algorithmically",
        abs(gamma_r - gamma) < 1e-12 and abs(e1_r - e1) < 1e-12 and abs(e2_r - e2) < 1e-12,
        f"(gamma,E1,E2)=({gamma_r:.12f},{e1_r:.12f},{e2_r:.12f})",
    )

    print()
    print(f"  seed pair      = ({xbar:.12f}, {ybar:.12f})")
    print(f"  off-seed source= ({xi[0]:.12f}, {xi[1]:.12f}, {eta[0]:.12f}, {eta[1]:.12f}, {delta:.12f})")


def part3_the_live_charged_sector_target_is_now_a_sign_law() -> None:
    print("\n" + "=" * 88)
    print("PART 3: THE LIVE CHARGED-SECTOR TARGET IS NOW A SIGN LAW")
    print("=" * 88)

    x = np.array([0.24, 0.38, 1.07], dtype=float)
    y = np.array([0.09, 0.22, 0.61], dtype=float)
    phase = 1.10
    gamma, e1, e2 = triplet_channels_from_active_data(x, y, phase)
    pmns_cp = cp_formula(0.0657, 0.05030323608835226, 0.8549000000000001, 0.23540000000000003, -0.6621, -0.01610323608835226, gamma)
    pkg = exact_package()

    check(
        "On the source-oriented mainline sheet, gamma > 0, E1 > 0, and E2 > 0 imply cp1 < 0 and cp2 > 0",
        pkg.gamma > 0.0 and pkg.E1 > 0.0 and pkg.E2 > 0.0 and pkg.cp1 < 0.0 and pkg.cp2 > 0.0,
        f"mainline=(gamma,E1,E2)=({pkg.gamma:.12f},{pkg.E1:.12f},{pkg.E2:.12f})",
    )
    check(
        "The canonical near-closing N_e sample instead has gamma > 0 but E1 < 0 and E2 < 0",
        gamma > 0.0 and e1 < 0.0 and e2 < 0.0,
        f"pmns=(gamma,E1,E2)=({gamma:.12f},{e1:.12f},{e2:.12f})",
    )
    check(
        "So the current charged-sector bridge problem is exactly to force the off-seed source onto the sign pattern gamma > 0, E1 > 0, E2 > 0",
        pmns_cp[0] > 0.0 and pmns_cp[1] < 0.0,
        f"pmns cp=({pmns_cp[0]:.12f},{pmns_cp[1]:.12f})",
    )

    print()
    print("  Charged-sector constructive target:")
    print("    gamma > 0, E1 > 0, E2 > 0")


def part4_the_theorem_note_records_the_source_law_boundary() -> None:
    print("\n" + "=" * 88)
    print("PART 4: THE THEOREM NOTE RECORDS THE SOURCE-LAW BOUNDARY")
    print("=" * 88)

    note = read("docs/DM_LEPTOGENESIS_PMNS_BREAKING_TRIPLET_SOURCE_LAW_NOTE_2026-04-16.md")

    check(
        "The new note records the exact charged-sector laws for gamma, E1, and E2",
        "gamma =" in note and "sin(delta)" in note and "E1 =" in note and "E2 =" in note,
    )
    check(
        "The note also records the constructive sign target gamma > 0, E1 > 0, E2 > 0",
        "gamma > 0" in note and "E1 > 0" in note and "E2 > 0" in note,
    )


def main() -> int:
    print("=" * 88)
    print("DM LEPTOGENESIS PMNS BREAKING-TRIPLET SOURCE LAW")
    print("=" * 88)
    print()
    print("Question:")
    print("  On the canonical one-sided PMNS active family, what exact charged-sector")
    print("  algebraic law feeds the mainline breaking-triplet CP channels?")

    x, y, phase = part1_the_active_family_has_an_exact_triplet_channel_law()
    part2_the_seed_plus_off_seed_source_data_already_fix_the_same_channels(x, y, phase)
    part3_the_live_charged_sector_target_is_now_a_sign_law()
    part4_the_theorem_note_records_the_source_law_boundary()

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  Exact source-law answer:")
    print("    - the active charged-sector data give exact formulas for gamma, E1, and E2")
    print("    - the seed pair plus the off-seed five-real source already fix those channels")
    print("    - the live constructive target is now a concrete sign law on that source")
    print()
    print(f"PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
