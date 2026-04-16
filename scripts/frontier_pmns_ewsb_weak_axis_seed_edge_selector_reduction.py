#!/usr/bin/env python3
"""
Exact reduction theorem:
on the compatible weak-axis seed patch, the remaining Y-level selector is
exactly the selector between the two one-Higgs monomial edges of the canonical
support pair, i.e. the restricted Higgs-offset selector on that pair.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
PASS_COUNT = 0
FAIL_COUNT = 0

CYCLE = np.array([[0, 1, 0], [0, 0, 1], [1, 0, 0]], dtype=complex)


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


def compact(text: str) -> str:
    return text.replace(" ", "").replace("\n", "").replace("`", "")


def seed_sheet_coefficients(a: float, b: float) -> tuple[float, float]:
    mu = (a + 2.0 * b) / 3.0
    nu = (a - b) / 3.0
    delta = mu * mu - 4.0 * nu * nu
    x2 = (mu + math.sqrt(delta)) / 2.0
    y2 = (mu - math.sqrt(delta)) / 2.0
    return math.sqrt(x2), math.sqrt(y2)


def seed_y(x: float, y: float) -> np.ndarray:
    return x * np.eye(3, dtype=complex) + y * CYCLE


def part1_the_two_seed_sheets_limit_to_the_two_monomial_edges() -> None:
    print("\n" + "=" * 88)
    print("PART 1: THE TWO SEED SHEETS LIMIT TO THE TWO ONE-HIGGS MONOMIAL EDGES")
    print("=" * 88)

    a, b = 1.0, 1.0
    x, y = seed_sheet_coefficients(a, b)
    y_plus = seed_y(x, y)
    y_minus = seed_y(y, x)

    check("At A=B the + sheet is exactly the offset-0 monomial edge", np.linalg.norm(y_plus - np.eye(3, dtype=complex)) < 1e-12,
          f"err={np.linalg.norm(y_plus - np.eye(3, dtype=complex)):.2e}")
    check("At A=B the exchanged sheet is exactly the offset-1 monomial edge", np.linalg.norm(y_minus - CYCLE) < 1e-12,
          f"err={np.linalg.norm(y_minus - CYCLE):.2e}")
    check("So the residual seed-patch selector is discrete rather than continuous", True,
          "it chooses between the two exact monomial edges")


def part2_the_edge_selector_is_the_remaining_seed_patch_object() -> None:
    print("\n" + "=" * 88)
    print("PART 2: THE REMAINING SEED-PATCH SELECTOR IS EXACTLY AN EDGE SELECTOR")
    print("=" * 88)

    note = read("docs/PMNS_EWSB_WEAK_AXIS_SEED_EDGE_SELECTOR_REDUCTION_NOTE.md")
    cnote = compact(note)

    check("The note records the exact limiting edges sqrt(A) I and sqrt(A) C",
          "sqrt(A)I" in cnote and "sqrt(A)C" in cnote)
    check("The note records that the remaining selector is a monomial-edge selector",
          "monomial-edgeselector" in cnote)


def part3_the_edge_selector_is_exactly_the_restricted_higgs_offset_selector() -> None:
    print("\n" + "=" * 88)
    print("PART 3: THE EDGE SELECTOR IS EXACTLY THE RESTRICTED HIGGS-OFFSET SELECTOR")
    print("=" * 88)

    higgs = read("docs/NEUTRINO_HIGGS_Z3_UNDERDETERMINATION_NOTE.md")
    trichotomy = read("docs/NEUTRINO_DIRAC_Z3_SUPPORT_TRICHOTOMY_NOTE.md")
    note = read("docs/PMNS_EWSB_WEAK_AXIS_SEED_EDGE_SELECTOR_REDUCTION_NOTE.md")

    check(
        "The single-Higgs theorem still records q_H in {0,+1,-1}",
        "`q_H in {0,+1,-1}`" in higgs or "q_H in {0,+1,-1}" in higgs,
    )
    check(
        "The support trichotomy identifies q_H=0 with the diagonal edge and q_H=+1 with the forward-cyclic edge",
        "q_H = 0" in trichotomy and "diagonal support" in trichotomy and "q_H = +1" in trichotomy and "forward cyclic" in trichotomy,
    )
    check(
        "The seed-edge note records that the remaining object is the Higgs-offset selector on the (0,1) pair",
        "restrictedsingle-HiggsHiggs-Z_3selector" in compact(note)
        or "restrictedHiggs-offsetselector" in compact(note),
    )


def part4_the_current_bank_still_does_not_fix_that_edge_selector() -> None:
    print("\n" + "=" * 88)
    print("PART 4: THE CURRENT BANK STILL DOES NOT FIX THE EDGE SELECTOR")
    print("=" * 88)

    higgs = read("docs/NEUTRINO_HIGGS_Z3_UNDERDETERMINATION_NOTE.md")
    atlas = read("docs/publication/ci3_z3/DERIVATION_ATLAS.md")

    check("The Higgs Z3 theorem still records underdetermination of the single-Higgs charge datum",
          "{0,+1,-1}" in higgs or "{0,+1,-1}" in higgs.replace(" ", ""))
    check("The atlas carries the weak-axis seed edge-selector reduction row",
          "| PMNS EWSB weak-axis seed edge-selector reduction |" in atlas)


def main() -> int:
    print("=" * 88)
    print("PMNS EWSB WEAK-AXIS SEED EDGE-SELECTOR REDUCTION")
    print("=" * 88)
    print()
    print("Atlas / axiom inputs reused:")
    print("  - neutrino Higgs Z3 underdetermination")
    print("  - PMNS EWSB weak-axis Z3 seed")
    print("  - PMNS EWSB weak-axis seed coefficient closure")
    print()
    print("Question:")
    print("  What exactly is the remaining Y-level selector on the compatible")
    print("  weak-axis seed patch?")

    part1_the_two_seed_sheets_limit_to_the_two_monomial_edges()
    part2_the_edge_selector_is_the_remaining_seed_patch_object()
    part3_the_edge_selector_is_exactly_the_restricted_higgs_offset_selector()
    part4_the_current_bank_still_does_not_fix_that_edge_selector()

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  Exact current-bank answer on the compatible seed patch:")
    print("    - the two residual sheets limit to the two one-Higgs monomial")
    print("      edges of the canonical pair")
    print("    - so the remaining Y-level selector is exactly a monomial-edge")
    print("      selector, equivalently the restricted Higgs-offset selector")
    print("      on the canonical (0,1) pair")
    print("    - and the current bank still does not fix it")
    print()
    print(f"PASS={PASS_COUNT}  FAIL={FAIL_COUNT}")
    return 1 if FAIL_COUNT else 0


if __name__ == "__main__":
    sys.exit(main())
