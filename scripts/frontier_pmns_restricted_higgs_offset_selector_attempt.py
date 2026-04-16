#!/usr/bin/env python3
"""
Exact boundary theorem:
on the canonical PMNS seed pair (0,1), the current bank does not derive a
positive restricted Higgs-offset selector law. The remaining selector is a
single discrete monomial-edge bit.
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
EYE = np.eye(3, dtype=complex)


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
    """
    Compatible weak-axis seed coefficients for diag(A,B,B), written in the
    canonical positive gauge patch.
    """
    mu = (a + 2.0 * b) / 3.0
    nu = (a - b) / 3.0
    delta = mu * mu - 4.0 * nu * nu
    x2 = (mu + math.sqrt(delta)) / 2.0
    y2 = (mu - math.sqrt(delta)) / 2.0
    return math.sqrt(x2), math.sqrt(y2)


def seed_y(x: float, y: float) -> np.ndarray:
    return x * EYE + y * CYCLE


def seed_h(y: np.ndarray) -> np.ndarray:
    return y @ y.conj().T


def part1_the_current_bank_only_reduces_qh_not_selects_it() -> None:
    print("\n" + "=" * 88)
    print("PART 1: THE CURRENT BANK ONLY REDUCES q_H, IT DOES NOT SELECT IT")
    print("=" * 88)

    higgs = read("docs/NEUTRINO_HIGGS_Z3_UNDERDETERMINATION_NOTE.md")
    trichotomy = read("docs/NEUTRINO_DIRAC_Z3_SUPPORT_TRICHOTOMY_NOTE.md")
    edge = read("docs/PMNS_EWSB_WEAK_AXIS_SEED_EDGE_SELECTOR_REDUCTION_NOTE.md")

    check(
        "The single-Higgs lane still reduces q_H to the exact discrete set",
        "q_H in {0,+1,-1}" in higgs or "{0,+1,-1}" in compact(higgs),
    )
    check(
        "The Dirac support trichotomy assigns the three q_H cases to three exact patterns",
        "diagonal support" in trichotomy and "forward cyclic support" in trichotomy and "backward cyclic support" in trichotomy,
    )
    check(
        "The seed-edge note identifies the remaining selector as a monomial-edge selector",
        "monomial-edge selector" in edge or "monomial-edgeselector" in compact(edge),
    )
    check(
        "The seed-edge note identifies the restricted single-Higgs Higgs-Z3 choice on the canonical pair",
        "restricted Higgs-offset selector" in edge or "restrictedsingle-HiggsHiggs-Z_3selector" in compact(edge),
    )


def part2_the_compatible_seed_patch_has_two_exchange_sheets() -> None:
    print("\n" + "=" * 88)
    print("PART 2: THE COMPATIBLE SEED PATCH HAS TWO EXACT EXCHANGE SHEETS")
    print("=" * 88)

    a, b = 1.0, 0.7
    x, y = seed_sheet_coefficients(a, b)
    y_plus = seed_y(x, y)
    y_minus = seed_y(y, x)
    h_plus = seed_h(y_plus)
    h_minus = seed_h(y_minus)

    check(
        "The compatible seed patch is actually compatible (A <= 4B)",
        a <= 4.0 * b,
        f"A={a}, B={b}",
    )
    check(
        "The two canonical sheets are distinct on the interior compatible patch",
        np.linalg.norm(y_plus - y_minus) > 1e-6,
        f"sheet-separation={np.linalg.norm(y_plus - y_minus):.3e}",
    )
    check(
        "The two exchange sheets have exactly the same Hermitian data",
        np.linalg.norm(h_plus - h_minus) < 1e-12,
        f"H-diff={np.linalg.norm(h_plus - h_minus):.2e}",
    )
    check(
        "The shared Hermitian data are of the exact weak-axis seed form",
        np.linalg.norm(h_plus - ((a + 2.0 * b) / 3.0 * EYE + (a - b) / 3.0 * (CYCLE + CYCLE.conj().T))) < 1e-12,
        f"seed-error={np.linalg.norm(h_plus - ((a + 2.0 * b) / 3.0 * EYE + (a - b) / 3.0 * (CYCLE + CYCLE.conj().T))):.2e}",
    )


def part3_the_equal_split_edge_is_exactly_the_two_monomial_endpoints() -> None:
    print("\n" + "=" * 88)
    print("PART 3: THE EQUAL-SPLIT EDGE IS EXACTLY THE TWO MONOMIAL ENDPOINTS")
    print("=" * 88)

    a, b = 1.0, 1.0
    x, y = seed_sheet_coefficients(a, b)
    y_plus = seed_y(x, y)
    y_minus = seed_y(y, x)

    check(
        "At A=B the plus sheet is exactly the identity monomial edge",
        np.linalg.norm(y_plus - EYE) < 1e-12,
        f"err={np.linalg.norm(y_plus - EYE):.2e}",
    )
    check(
        "At A=B the exchanged sheet is exactly the cycle monomial edge",
        np.linalg.norm(y_minus - CYCLE) < 1e-12,
        f"err={np.linalg.norm(y_minus - CYCLE):.2e}",
    )


def part4_the_missing_selector_input_is_one_binary_edge_bit() -> None:
    print("\n" + "=" * 88)
    print("PART 4: THE MISSING SELECTOR INPUT IS ONE BINARY EDGE BIT")
    print("=" * 88)

    note = read("docs/PMNS_RESTRICTED_HIGGS_OFFSET_SELECTOR_ATTEMPT_NOTE.md")
    current = read("docs/PMNS_SELECTOR_CURRENT_STACK_ZERO_LAW_NOTE.md")
    seed_edge = read("docs/PMNS_EWSB_WEAK_AXIS_SEED_EDGE_SELECTOR_REDUCTION_NOTE.md")

    check(
        "The note states that no positive selector law is derived from the current exact bank",
        "No positive selector law is derivable" in note,
    )
    check(
        "The note states the remaining selector is a single discrete monomial-edge bit",
        "single discrete Higgs-offset / monomial-edge bit" in note or "single discrete monomial-edge bit" in note,
    )
    check(
        "The current-stack selector amplitude theorem is still zero on the retained bank",
        "a_sel,current=0" in current.replace(" ", ""),
    )
    check(
        "The seed-edge reduction note identifies the residual boundary as the canonical monomial edges",
        "sqrt(A) I" in seed_edge and "sqrt(A) C" in seed_edge,
    )


def main() -> int:
    print("=" * 88)
    print("PMNS RESTRICTED HIGGS-OFFSET SELECTOR ATTEMPT")
    print("=" * 88)
    print()
    print("Atlas / axiom inputs reused:")
    print("  - Neutrino Higgs Z3 underdetermination")
    print("  - Neutrino Dirac Z3 support trichotomy")
    print("  - PMNS EWSB weak-axis Z3 seed")
    print("  - PMNS EWSB weak-axis seed coefficient closure")
    print("  - PMNS EWSB weak-axis seed edge-selector reduction")
    print("  - PMNS selector current-stack zero law")
    print()
    print("Question:")
    print("  Can the current exact bank derive a positive restricted Higgs-offset")
    print("  selector law on the canonical seed pair (0,1)?")

    part1_the_current_bank_only_reduces_qh_not_selects_it()
    part2_the_compatible_seed_patch_has_two_exchange_sheets()
    part3_the_equal_split_edge_is_exactly_the_two_monomial_endpoints()
    part4_the_missing_selector_input_is_one_binary_edge_bit()

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  Exact current-bank answer on the canonical PMNS seed pair (0,1):")
    print("    - the selector reduces to a single discrete monomial-edge bit")
    print("    - equivalently, the restricted Higgs-offset choice q_H in {0,+1}")
    print("    - the current exact bank does not determine that bit")
    print("    - so no positive selector law is derived yet")
    print()
    print(f"PASS={PASS_COUNT}  FAIL={FAIL_COUNT}")
    return 1 if FAIL_COUNT else 0


if __name__ == "__main__":
    sys.exit(main())
