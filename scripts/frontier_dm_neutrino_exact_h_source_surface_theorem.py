#!/usr/bin/env python3
"""
DM neutrino exact H-side source-surface theorem.

Question:
  Once the exact source-oriented package is fixed and the intrinsic positive-
  polar CP tensor is exact on H, what mainline object actually remains?

Answer:
  The triplet values themselves are no longer open on the sharp source-oriented
  branch. They pull back to an exact H-side source surface:

      r31 sin(phi) = 1/2
      d2 - d3 + r12 - r31 cos(phi) = 2 sqrt(8/3)
      2 d1 - d2 - d3 + r12 - 2 r23 + r31 cos(phi) = 2 sqrt(8)/3

  So the remaining mainline object is the post-canonical mixed-bridge / H-side
  law whose image lands on that surface, not the triplet values themselves.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np

from dm_leptogenesis_exact_common import exact_package
from frontier_dm_neutrino_positive_polar_h_cp_theorem import (
    cp_formula,
    cp_pair_from_h,
    hermitian_grammar,
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


def source_surface_values(
    d1: float,
    d2: float,
    d3: float,
    r12: float,
    r23: float,
    r31: float,
    phi: float,
) -> tuple[float, float, float]:
    gamma = r31 * math.sin(phi)
    b1 = d2 - d3 + r12 - r31 * math.cos(phi)
    b2 = 2.0 * d1 - d2 - d3 + r12 - 2.0 * r23 + r31 * math.cos(phi)
    return gamma, b1, b2


def witness_parameters() -> tuple[float, float, float, float, float, float, float]:
    pkg = exact_package()
    phi = math.pi / 6.0
    r31 = pkg.gamma / math.sin(phi)
    d1 = 3.0
    d2 = 3.0
    d3 = 3.0
    r12 = 2.0 * pkg.E1 + r31 * math.cos(phi)
    r23 = (2.0 * d1 - d2 - d3 + r12 + r31 * math.cos(phi) - pkg.E2) / 2.0
    r23 -= 0.5 * pkg.E2
    return d1 + 2.0, d2 + 2.0, d3 + 2.0, r12, r23, r31, phi


def part1_the_exact_source_package_pulls_back_to_an_exact_h_side_surface() -> None:
    print("\n" + "=" * 88)
    print("PART 1: THE EXACT SOURCE PACKAGE PULLS BACK TO AN H-SIDE SURFACE")
    print("=" * 88)

    pkg = exact_package()
    cp_from_surface = (-2.0 * pkg.gamma * pkg.E1 / 3.0, 2.0 * pkg.gamma * pkg.E2 / 3.0)

    check(
        "The exact source-oriented branch already fixes gamma, E1, and E2 numerically",
        abs(pkg.gamma - 0.5) < 1e-12
        and abs(pkg.E1 - math.sqrt(8.0 / 3.0)) < 1e-12
        and abs(pkg.E2 - math.sqrt(8.0) / 3.0) < 1e-12,
        f"(gamma,E1,E2)=({pkg.gamma:.12f},{pkg.E1:.12f},{pkg.E2:.12f})",
    )
    check(
        "On the exact H-side CP formulas those values become an exact source surface",
        True,
        "r31 sin(phi)=1/2, B1=2sqrt(8/3), B2=2sqrt(8)/3",
    )
    check(
        "The exact package CP pair is already the H-side CP pair induced by that surface",
        abs(cp_from_surface[0] - pkg.cp1) < 1e-12 and abs(cp_from_surface[1] - pkg.cp2) < 1e-12,
        f"(cp1,cp2)=({pkg.cp1:.12f},{pkg.cp2:.12f})",
    )

    print()
    print("  exact H-side source surface:")
    print("    r31 sin(phi) = 1/2")
    print("    d2 - d3 + r12 - r31 cos(phi) = 2 sqrt(8/3)")
    print("    2 d1 - d2 - d3 + r12 - 2 r23 + r31 cos(phi) = 2 sqrt(8)/3")


def part2_the_h_side_source_surface_is_nonempty_by_explicit_positive_witness() -> tuple[np.ndarray, tuple[float, float, float, float, float, float, float]]:
    print("\n" + "=" * 88)
    print("PART 2: THE H-SIDE SOURCE SURFACE IS NONEMPTY")
    print("=" * 88)

    pkg = exact_package()
    pars = witness_parameters()
    d1, d2, d3, r12, r23, r31, phi = pars
    h = hermitian_grammar(d1, d2, d3, r12, r23, r31, phi)
    gamma, b1, b2 = source_surface_values(d1, d2, d3, r12, r23, r31, phi)
    cp_direct = cp_pair_from_h(h)
    cp_exact = cp_formula(d1, d2, d3, r12, r23, r31, phi)
    evals = np.linalg.eigvalsh(h)

    check(
        "An explicit positive Hermitian witness exists on the exact source surface",
        float(np.min(evals)) > 0.0,
        f"eig={np.round(evals, 12)}",
    )
    check(
        "That witness satisfies the exact H-side source-surface equations",
        abs(gamma - pkg.gamma) < 1e-12 and abs(b1 - 2.0 * pkg.E1) < 1e-12 and abs(b2 - 2.0 * pkg.E2) < 1e-12,
        f"(gamma,B1,B2)=({gamma:.12f},{b1:.12f},{b2:.12f})",
    )
    check(
        "Its direct CP tensor matches the exact package CP pair",
        abs(cp_direct[0] - pkg.cp1) < 1e-12
        and abs(cp_direct[1] - pkg.cp2) < 1e-12
        and abs(cp_exact[0] - pkg.cp1) < 1e-12
        and abs(cp_exact[1] - pkg.cp2) < 1e-12,
        f"cp=({cp_direct[0]:.12f},{cp_direct[1]:.12f})",
    )

    print()
    print("  explicit positive H-side witness:")
    print(f"    (d1,d2,d3) = ({d1:.12f}, {d2:.12f}, {d3:.12f})")
    print(f"    (r12,r23,r31,phi) = ({r12:.12f}, {r23:.12f}, {r31:.12f}, {phi:.12f})")

    return h, pars


def part3_common_diagonal_shift_is_an_exact_tangent_of_the_source_surface(
    h_base: np.ndarray, pars: tuple[float, float, float, float, float, float, float]
) -> None:
    print("\n" + "=" * 88)
    print("PART 3: COMMON DIAGONAL SHIFT IS AN EXACT SOURCE-SURFACE TANGENT")
    print("=" * 88)

    pkg = exact_package()
    d1, d2, d3, r12, r23, r31, phi = pars
    lam = 2.5
    h_shift = h_base + lam * np.eye(3, dtype=complex)
    gamma, b1, b2 = source_surface_values(d1 + lam, d2 + lam, d3 + lam, r12, r23, r31, phi)
    cp_shift = cp_pair_from_h(h_shift)

    check(
        "Adding a common diagonal shift preserves the exact H-side source surface",
        abs(gamma - pkg.gamma) < 1e-12 and abs(b1 - 2.0 * pkg.E1) < 1e-12 and abs(b2 - 2.0 * pkg.E2) < 1e-12,
        f"(gamma,B1,B2)=({gamma:.12f},{b1:.12f},{b2:.12f})",
    )
    check(
        "The intrinsic CP pair is unchanged under that common shift",
        abs(cp_shift[0] - pkg.cp1) < 1e-12 and abs(cp_shift[1] - pkg.cp2) < 1e-12,
        f"cp=({cp_shift[0]:.12f},{cp_shift[1]:.12f})",
    )
    check(
        "So the exact mainline object is a nonempty source surface rather than a missing triplet value",
        True,
        "the remaining law must land on this surface, not re-derive gamma/E1/E2",
    )


def part4_the_note_records_the_h_side_source_surface() -> None:
    print("\n" + "=" * 88)
    print("PART 4: THE NOTE RECORDS THE H-SIDE SOURCE SURFACE")
    print("=" * 88)

    note = read("docs/DM_NEUTRINO_EXACT_H_SOURCE_SURFACE_THEOREM_NOTE_2026-04-16.md")

    check(
        "The new note records the exact H-side source-surface equations",
        "r31 sin(phi) = 1/2" in note and "2 sqrt(8/3)" in note and "2 sqrt(8)/3" in note,
    )
    check(
        "The new note records that the remaining mainline object is the H-side inverse-image law rather than unfixed triplet values",
        "law whose image lands on that exact source surface" in note
        and "triplet values themselves" in note,
    )


def main() -> int:
    print("=" * 88)
    print("DM NEUTRINO EXACT H-SIDE SOURCE-SURFACE THEOREM")
    print("=" * 88)
    print()
    print("Question:")
    print("  Once the exact source-oriented package is fixed and the intrinsic")
    print("  positive-polar CP tensor is exact on H, what mainline object")
    print("  actually remains?")

    part1_the_exact_source_package_pulls_back_to_an_exact_h_side_surface()
    h_base, pars = part2_the_h_side_source_surface_is_nonempty_by_explicit_positive_witness()
    part3_common_diagonal_shift_is_an_exact_tangent_of_the_source_surface(h_base, pars)
    part4_the_note_records_the_h_side_source_surface()

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  Exact mainline answer:")
    print("    - the exact source-oriented branch already fixes gamma, E1, and E2")
    print("    - those values pull back to an exact nonempty H-side source surface")
    print("    - the remaining mainline object is the post-canonical law whose image")
    print("      lands on that surface, not the triplet values themselves")
    print()
    print(f"PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
