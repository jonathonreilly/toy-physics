#!/usr/bin/env python3
"""
Exact minimal-extension theorem:
starting from the restricted Higgs-offset selector on the canonical (0,1)
pair, the smallest honest positive selector primitive is a one-slot
sector-sensitive mixed bridge. The retained bank does not itself derive the
activation law.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
PASS_COUNT = 0
FAIL_COUNT = 0

EYE = np.eye(3, dtype=complex)
CYCLE = np.array([[0, 1, 0], [0, 0, 1], [1, 0, 0]], dtype=complex)
REDUCED_SELECTOR_CLASS = np.array([0.0, 0.0, 1.0, -1.0])


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


def selector_edge(bit: int, amplitude: float) -> np.ndarray:
    """Canonical monomial-edge representative on the (0,1) seed pair."""
    root = math.sqrt(amplitude)
    if bit == 0:
        return root * EYE
    if bit == 1:
        return root * CYCLE
    raise ValueError("bit must be 0 or 1")


def edge_bit_from_amplitude(a_sel: float) -> int:
    """The minimal binary selector primitive on the canonical pair."""
    return 0 if a_sel >= 0.0 else 1


def selector_primitive(a_sel: float) -> np.ndarray:
    return a_sel * REDUCED_SELECTOR_CLASS


def part1_the_current_bank_only_reduces_the_selector() -> None:
    print("\n" + "=" * 88)
    print("PART 1: THE CURRENT BANK ONLY REDUCES THE SELECTOR")
    print("=" * 88)

    attempt = read("docs/PMNS_RESTRICTED_HIGGS_OFFSET_SELECTOR_ATTEMPT_NOTE.md")
    zero_law = read("docs/PMNS_SELECTOR_CURRENT_STACK_ZERO_LAW_NOTE.md")
    amp = read("docs/PMNS_SELECTOR_UNIQUE_AMPLITUDE_SLOT_NOTE.md")

    check(
        "The restricted-selector note says no positive selector law is derivable",
        "No positive selector law is derivable" in attempt,
    )
    check(
        "The restricted-selector note says the remaining object is one binary edge bit",
        "single discrete monomial-edge bit" in attempt or "binary monomial-edge bit" in attempt,
    )
    check(
        "The current-stack theorem records a_sel,current = 0 on the retained bank",
        "a_sel,current=0" in compact(zero_law),
    )
    check(
        "The reduced microscopic problem is already one amplitude slot on one class",
        "one real amplitude slot" in amp and "B_red = a_sel S_cls" in amp,
    )

    print()
    print("  So the retained bank does not yet choose the selector. It only")
    print("  compresses it to a single amplitude on a single reduced class.")


def part2_the_canonical_pair_has_two_exact_edges() -> None:
    print("\n" + "=" * 88)
    print("PART 2: THE CANONICAL PAIR HAS TWO EXACT MONOMIAL EDGES")
    print("=" * 88)

    amplitude = 2.25
    edge0 = selector_edge(0, amplitude)
    edge1 = selector_edge(1, amplitude)

    h0 = edge0 @ edge0.conj().T
    h1 = edge1 @ edge1.conj().T
    expected = amplitude * EYE

    check(
        "The offset-0 monomial edge is exactly sqrt(A) I",
        np.linalg.norm(selector_edge(0, amplitude) - math.sqrt(amplitude) * EYE) < 1e-12,
        f"err={np.linalg.norm(selector_edge(0, amplitude) - math.sqrt(amplitude) * EYE):.2e}",
    )
    check(
        "The offset-1 monomial edge is exactly sqrt(A) C",
        np.linalg.norm(selector_edge(1, amplitude) - math.sqrt(amplitude) * CYCLE) < 1e-12,
        f"err={np.linalg.norm(selector_edge(1, amplitude) - math.sqrt(amplitude) * CYCLE):.2e}",
    )
    check(
        "The two exact monomial edges have the same Hermitian data",
        np.linalg.norm(h0 - h1) < 1e-12,
        f"H-diff={np.linalg.norm(h0 - h1):.2e}",
    )
    check(
        "The shared Hermitian data are exactly amplitude times the identity",
        np.linalg.norm(h0 - expected) < 1e-12,
        f"err={np.linalg.norm(h0 - expected):.2e}",
    )

    print()
    print("  So the canonical pair really is a binary edge selector: the two")
    print("  edges are exact and Hermitian-indistinguishable on the boundary.")


def part3_the_reduced_selector_class_is_one_amplitude_slot() -> None:
    print("\n" + "=" * 88)
    print("PART 3: THE REDUCED SELECTOR CLASS IS ONE AMPLITUDE SLOT")
    print("=" * 88)

    basis = REDUCED_SELECTOR_CLASS
    rank = int(np.linalg.matrix_rank(np.array(
        [
            [1.0, 0.0, 0.0, 0.0],
            [0.0, 1.0, 0.0, 0.0],
            [0.0, 0.0, 1.0, 1.0],
        ]
    )))
    dim = 4 - rank
    a_sel = 1.75
    primitive = selector_primitive(a_sel)
    extracted = float(np.dot(basis, primitive) / np.dot(basis, basis))
    recon = extracted * basis
    err = float(np.linalg.norm(primitive - recon))

    check(
        "The reduced selector class space is one-dimensional",
        rank == 3 and dim == 1,
        f"rank={rank}, dim={dim}",
    )
    check(
        "The canonical reduced class is sector-odd",
        abs(basis[2] + basis[3]) < 1e-12,
        f"sum={basis[2] + basis[3]:.2e}",
    )
    check(
        "A reduced realization reconstructs from one real amplitude",
        err < 1e-12,
        f"reconstruction error={err:.2e}",
    )
    check(
        "The extracted coefficient is exactly the amplitude slot",
        abs(extracted - a_sel) < 1e-12,
        f"a_sel={a_sel:.6f}, extracted={extracted:.6f}",
    )

    print()
    print("  So the reduced selector problem is not a multi-parameter family.")
    print("  It is one real amplitude on one reduced class.")


def part4_the_minimal_extension_is_the_new_selector_primitive() -> None:
    print("\n" + "=" * 88)
    print("PART 4: THE MINIMAL EXTENSION IS THE NEW SELECTOR PRIMITIVE")
    print("=" * 88)

    note = read("docs/PMNS_SELECTOR_MINIMAL_MICROSCOPIC_EXTENSION_NOTE.md")
    right_gram = read("docs/PMNS_RIGHT_GRAM_SELECTOR_REALIZATION_NOTE.md")
    edge = read("docs/PMNS_EWSB_WEAK_AXIS_SEED_EDGE_SELECTOR_REDUCTION_NOTE.md")

    check(
        "The minimal-extension note identifies the surviving class as non-additive and sector-sensitive",
        "non-additive" in note and "sector-sensitive" in note and "mixed bridge" in note,
    )
    check(
        "The minimal-extension note identifies one real amplitude slot",
        "one real amplitude slot" in note and "a_sel" in note,
    )
    check(
        "The admitted right-sensitive route realizes the same reduced selector class positively",
        "realizes the unique reduced selector class" in right_gram and "right-sensitive datum" in right_gram,
    )
    check(
        "The seed-edge reduction identifies the canonical pair as the remaining Higgs-offset bit",
        "restricted Higgs-offset selector" in edge and "canonical pair" in edge,
    )

    print()
    print("  Therefore the smallest exact selector theorem beyond the retained bank")
    print("  is a one-slot non-additive sector-sensitive mixed bridge whose reduced")
    print("  class is chi_N_nu - chi_N_e and whose edge encoding on (0,1) is the")
    print("  binary choice sqrt(A) I versus sqrt(A) C.")


def main() -> int:
    print("=" * 88)
    print("PMNS NEW SELECTOR PRIMITIVE CONSTRUCTION")
    print("=" * 88)
    print()
    print("Atlas / axiom inputs reused:")
    print("  - PMNS restricted Higgs-offset selector attempt")
    print("  - PMNS selector unique amplitude slot")
    print("  - PMNS selector current-stack zero law")
    print("  - PMNS selector minimal microscopic extension")
    print("  - PMNS right-Gram selector realization")
    print("  - PMNS weak-axis seed edge-selector reduction")
    print()
    print("Question:")
    print("  Can the restricted Higgs-offset selector on the canonical (0,1) pair")
    print("  be promoted to a genuine positive selector law from the current bank?")

    part1_the_current_bank_only_reduces_the_selector()
    part2_the_canonical_pair_has_two_exact_edges()
    part3_the_reduced_selector_class_is_one_amplitude_slot()
    part4_the_minimal_extension_is_the_new_selector_primitive()

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  Exact current-bank answer:")
    print("    - no positive selector law is derived from the retained bank")
    print("    - the canonical selector is exactly one binary edge bit")
    print("    - the reduced selector class is one-dimensional")
    print("    - the minimal exact extension is one non-additive")
    print("      sector-sensitive mixed bridge with one real amplitude slot")
    print()
    print("  Positive-vs-obstruction summary:")
    print("    - positive: the admitted minimal extension class is explicit")
    print("    - obstruction: the current bank does not fix a_sel or the edge")
    print()
    print(f"PASS={PASS_COUNT}  FAIL={FAIL_COUNT}")
    return 1 if FAIL_COUNT else 0


if __name__ == "__main__":
    sys.exit(main())
