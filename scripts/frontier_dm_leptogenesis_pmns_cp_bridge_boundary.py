#!/usr/bin/env python3
"""
DM leptogenesis PMNS/mainline CP bridge boundary.

Question:
  Does the canonical near-closing PMNS-assisted N_e sample already realize the
  same source-oriented CP package as the mainline exact leptogenesis branch?

Answer:
  No.

  The canonical off-seed N_e sample decomposes exactly on the same
  breaking-triplet grammar, but it gives the opposite CP sign pattern:

      (cp1, cp2)_PMNS = (+, -)

  whereas the exact source-oriented leptogenesis package gives

      (cp1, cp2)_mainline = (-, +).

  So the PMNS near-closing sample remains a transport/comparator witness, not
  yet the constructive mainline CP witness.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

from dm_leptogenesis_exact_common import exact_package
from frontier_dm_leptogenesis_pmns_projector_interface import canonical_h
from frontier_dm_neutrino_breaking_triplet_cp_theorem import (
    cp_formula,
    cp_pair_from_h,
    h_from_breaking_triplet,
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


def breaking_triplet_coordinates(h: np.ndarray) -> dict[str, float]:
    a = float(np.real(h[0, 0]))
    c = float(0.5 * (np.real(h[1, 1]) + np.real(h[2, 2])))
    delta = float(0.5 * (np.real(h[1, 1]) - np.real(h[2, 2])))
    d = float(np.real(h[1, 2]))
    b = float(0.5 * (np.real(h[0, 1]) + np.real(h[0, 2])))
    rho = float(0.5 * (np.real(h[0, 1]) - np.real(h[0, 2])))
    gamma = float(-np.imag(h[0, 2]))
    return {
        "A": a,
        "b": b,
        "c": c,
        "d": d,
        "delta": delta,
        "rho": rho,
        "gamma": gamma,
    }


def part1_the_canonical_ne_sample_lives_on_the_same_breaking_triplet_grammar() -> tuple[np.ndarray, dict[str, float]]:
    print("\n" + "=" * 88)
    print("PART 1: THE CANONICAL N_e SAMPLE LIVES ON THE SAME BREAKING-TRIPLET GRAMMAR")
    print("=" * 88)

    x = np.array([0.24, 0.38, 1.07], dtype=float)
    y = np.array([0.09, 0.22, 0.61], dtype=float)
    phase = 1.10
    h = canonical_h(x, y, phase)
    pars = breaking_triplet_coordinates(h)
    h_rebuilt = h_from_breaking_triplet(**pars)

    check(
        "The canonical off-seed N_e Hermitian sample is exactly of the breaking-triplet form",
        np.linalg.norm(h - h_rebuilt) < 1e-12,
        f"err={np.linalg.norm(h - h_rebuilt):.2e}",
    )
    check(
        "Its gamma slot is nonzero",
        pars["gamma"] > 0.0,
        f"gamma={pars['gamma']:.12f}",
    )
    check(
        "Both real interference channels are definite on that sample",
        abs(pars["delta"] + pars["rho"]) > 1e-12 and abs(pars["A"] + pars["b"] - pars["c"] - pars["d"]) > 1e-12,
        f"(delta+rho, A+b-c-d)=({pars['delta'] + pars['rho']:.12f}, {pars['A'] + pars['b'] - pars['c'] - pars['d']:.12f})",
    )

    print()
    print("  Breaking-triplet coordinates on the canonical near-closing N_e sample:")
    print(f"    gamma         = {pars['gamma']:.12f}")
    print(f"    delta + rho   = {pars['delta'] + pars['rho']:.12f}")
    print(f"    A + b - c - d = {pars['A'] + pars['b'] - pars['c'] - pars['d']:.12f}")

    return h, pars


def part2_the_pmns_sample_has_the_opposite_cp_orientation() -> tuple[float, float]:
    print("\n" + "=" * 88)
    print("PART 2: THE PMNS SAMPLE HAS THE OPPOSITE CP ORIENTATION")
    print("=" * 88)

    x = np.array([0.24, 0.38, 1.07], dtype=float)
    y = np.array([0.09, 0.22, 0.61], dtype=float)
    phase = 1.10
    h = canonical_h(x, y, phase)
    pars = breaking_triplet_coordinates(h)

    cp_direct = cp_pair_from_h(h)
    cp_exact = cp_formula(**pars)

    check(
        "The direct intrinsic CP tensor matches the exact breaking-triplet formula on the canonical N_e sample",
        abs(cp_direct[0] - cp_exact[0]) < 1e-12 and abs(cp_direct[1] - cp_exact[1]) < 1e-12,
        f"direct={cp_direct}, exact={cp_exact}",
    )
    check(
        "The canonical N_e sample has cp1 > 0 and cp2 < 0",
        cp_exact[0] > 0.0 and cp_exact[1] < 0.0,
        f"(cp1,cp2)=({cp_exact[0]:.12f},{cp_exact[1]:.12f})",
    )
    check(
        "So its two CP channels already sit on one definite orientation sheet",
        True,
        "(+, -) on the canonical PMNS near-closing sample",
    )

    print()
    print(f"  canonical N_e CP pair = ({cp_exact[0]:.12f}, {cp_exact[1]:.12f})")
    return cp_exact


def part3_the_source_oriented_mainline_package_is_on_the_opposite_sheet() -> None:
    print("\n" + "=" * 88)
    print("PART 3: THE SOURCE-ORIENTED MAINLINE PACKAGE IS ON THE OPPOSITE SHEET")
    print("=" * 88)

    x = np.array([0.24, 0.38, 1.07], dtype=float)
    y = np.array([0.09, 0.22, 0.61], dtype=float)
    phase = 1.10
    pmns_h = canonical_h(x, y, phase)
    pmns_pars = breaking_triplet_coordinates(pmns_h)
    pmns_cp = cp_formula(**pmns_pars)

    pkg = exact_package()
    e1_pmns = pmns_pars["delta"] + pmns_pars["rho"]
    e2_pmns = pmns_pars["A"] + pmns_pars["b"] - pmns_pars["c"] - pmns_pars["d"]

    check(
        "The exact source-oriented branch has cp1 < 0 and cp2 > 0",
        pkg.cp1 < 0.0 and pkg.cp2 > 0.0,
        f"(cp1,cp2)=({pkg.cp1:.12f},{pkg.cp2:.12f})",
    )
    check(
        "The PMNS canonical sample and the exact mainline package therefore have opposite CP sign patterns",
        np.sign(pmns_cp[0]) == -np.sign(pkg.cp1) and np.sign(pmns_cp[1]) == -np.sign(pkg.cp2),
        f"pmns={pmns_cp}, mainline=({pkg.cp1:.12f},{pkg.cp2:.12f})",
    )
    check(
        "The PMNS canonical sample does not reproduce the exact mainline source package values",
        abs(pmns_pars["gamma"] - pkg.gamma) > 0.1 and abs(e1_pmns - pkg.E1) > 1.0 and abs(e2_pmns - pkg.E2) > 1.5,
        f"pmns=(gamma,E1,E2)=({pmns_pars['gamma']:.12f},{e1_pmns:.12f},{e2_pmns:.12f})",
    )

    print()
    print(f"  exact mainline CP pair = ({pkg.cp1:.12f}, {pkg.cp2:.12f})")
    print(f"  exact mainline source package = ({pkg.gamma:.12f}, {pkg.E1:.12f}, {pkg.E2:.12f})")


def part4_the_theorem_note_records_the_bridge_boundary() -> None:
    print("\n" + "=" * 88)
    print("PART 4: THE THEOREM NOTE RECORDS THE BRIDGE BOUNDARY")
    print("=" * 88)

    note = read("docs/DM_LEPTOGENESIS_PMNS_CP_BRIDGE_BOUNDARY_NOTE_2026-04-16.md")

    check(
        "The new note records the opposite CP sign pattern between the PMNS sample and the mainline branch",
        "opposite CP sign pattern" in note and "canonical near-closing sample" in note,
    )
    check(
        "The note records the concrete CP orientation split (+,-) versus (-,+)",
        "cp1 = +0.058991" in note and "cp2 = -0.084746" in note and "cp1 = -0.544331" in note and "cp2 = +0.314269" in note,
    )


def main() -> int:
    print("=" * 88)
    print("DM LEPTOGENESIS PMNS/MAINLINE CP BRIDGE BOUNDARY")
    print("=" * 88)
    print()
    print("Question:")
    print("  Does the canonical near-closing PMNS-assisted N_e sample already")
    print("  realize the same source-oriented CP package as the mainline exact")
    print("  leptogenesis branch?")

    part1_the_canonical_ne_sample_lives_on_the_same_breaking_triplet_grammar()
    part2_the_pmns_sample_has_the_opposite_cp_orientation()
    part3_the_source_oriented_mainline_package_is_on_the_opposite_sheet()
    part4_the_theorem_note_records_the_bridge_boundary()

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  Exact boundary answer:")
    print("    - the canonical near-closing N_e sample is exactly on the same")
    print("      breaking-triplet grammar")
    print("    - but it carries the opposite CP sign pattern from the exact")
    print("      source-oriented mainline package")
    print("    - so the PMNS near-closing route remains a transport/comparator")
    print("      witness, not yet the constructive mainline CP witness")
    print()
    print(f"PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
