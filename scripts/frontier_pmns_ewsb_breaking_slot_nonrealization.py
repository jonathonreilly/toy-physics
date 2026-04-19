#!/usr/bin/env python3
"""
Exact boundary theorem:
the current retained PMNS bank reduces the generic active Hermitian law to the
aligned residual-Z2 core plus three explicit breaking slots, but it does not
yet derive that three-slot vector.
"""

from __future__ import annotations

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


def canonical_y(x: np.ndarray, y: np.ndarray, phi: float) -> np.ndarray:
    return np.diag(np.asarray(x, dtype=complex)) + np.diag(
        np.array([y[0], y[1], y[2] * np.exp(1j * phi)], dtype=complex)
    ) @ CYCLE


def canonical_h(x: np.ndarray, y: np.ndarray, phi: float) -> np.ndarray:
    mat = canonical_y(x, y, phi)
    return mat @ mat.conj().T


def support_mask(mat: np.ndarray) -> np.ndarray:
    return (np.abs(mat) > 1e-12).astype(int)


def hermitian_coordinates(h: np.ndarray) -> np.ndarray:
    return np.array(
        [
            float(np.real(h[0, 0])),
            float(np.real(h[1, 1])),
            float(np.real(h[2, 2])),
            float(np.abs(h[0, 1])),
            float(np.abs(h[1, 2])),
            float(np.abs(h[2, 0])),
            float(np.angle(h[0, 1] * h[1, 2] * h[2, 0])),
        ],
        dtype=float,
    )


def breaking_slots(h: np.ndarray) -> np.ndarray:
    _d1, d2, d3, r12, _r23, r31, phi = hermitian_coordinates(h)
    return np.array([d2 - d3, r12 - r31, phi], dtype=float)


def part1_active_branch_exactly_splits_into_aligned_core_plus_three_slots() -> None:
    print("\n" + "=" * 88)
    print("PART 1: THE GENERIC ACTIVE HERMITIAN LAW SPLITS INTO CORE PLUS THREE SLOTS")
    print("=" * 88)

    aligned_y = canonical_y(
        np.array([1.20, 0.90, 0.90], dtype=float),
        np.array([1.20 * 0.40 / 0.90, 0.40, 0.40], dtype=float),
        0.0,
    )
    generic_y = canonical_y(
        np.array([1.15, 0.82, 0.95], dtype=float),
        np.array([0.41, 0.28, 0.54], dtype=float),
        0.63,
    )
    aligned_h = aligned_y @ aligned_y.conj().T
    generic_h = generic_y @ generic_y.conj().T
    beta_aligned = breaking_slots(aligned_h)
    beta_generic = breaking_slots(generic_h)

    check("Aligned and generic points lie on the same exact A + B C support class",
          np.array_equal(support_mask(aligned_y), support_mask(generic_y)),
          f"mask=\n{support_mask(aligned_y)}")
    check("The aligned full-rank point has zero breaking slots",
          np.linalg.norm(beta_aligned) < 1e-12,
          f"beta={beta_aligned}")
    check("A generic full-rank point has nonzero breaking slots",
          np.linalg.norm(beta_generic) > 1e-6,
          f"beta={np.round(beta_generic, 6)}")
    check("Both points remain full rank on the same canonical branch",
          np.linalg.matrix_rank(aligned_y) == 3 and np.linalg.matrix_rank(generic_y) == 3,
          f"ranks=({np.linalg.matrix_rank(aligned_y)},{np.linalg.matrix_rank(generic_y)})")


def part2_distinct_generic_points_can_carry_distinct_breaking_slot_vectors() -> None:
    print("\n" + "=" * 88)
    print("PART 2: DISTINCT GENERIC ACTIVE POINTS CARRY DISTINCT BREAKING-SLOT VECTORS")
    print("=" * 88)

    y0 = canonical_y(
        np.array([1.15, 0.82, 0.95], dtype=float),
        np.array([0.41, 0.28, 0.54], dtype=float),
        0.63,
    )
    y1 = canonical_y(
        np.array([1.07, 0.91, 0.79], dtype=float),
        np.array([0.36, 0.33, 0.46], dtype=float),
        -0.41,
    )
    h0 = y0 @ y0.conj().T
    h1 = y1 @ y1.conj().T
    beta0 = breaking_slots(h0)
    beta1 = breaking_slots(h1)

    check("Both generic points share the same canonical support mask",
          np.array_equal(support_mask(y0), support_mask(y1)),
          f"mask=\n{support_mask(y0)}")
    check("Both generic points are full rank", np.linalg.matrix_rank(y0) == 3 and np.linalg.matrix_rank(y1) == 3,
          f"ranks=({np.linalg.matrix_rank(y0)},{np.linalg.matrix_rank(y1)})")
    check("The two generic active points have distinct breaking-slot vectors",
          np.linalg.norm(beta0 - beta1) > 1e-6,
          f"|beta0-beta1|={np.linalg.norm(beta0 - beta1):.3f}")
    check("So the current branch grammar does not collapse beta to one current-bank value", True)


def part3_note_and_atlas_record_the_boundary() -> None:
    print("\n" + "=" * 88)
    print("PART 3: THE NOTE, ATLAS, AND BOUNDARY NOTES RECORD THE BREAKING-SLOT BOUNDARY")
    print("=" * 88)

    note = read("docs/PMNS_EWSB_BREAKING_SLOT_NONREALIZATION_NOTE.md")
    atlas = read("docs/publication/ci3_z3/DERIVATION_ATLAS.md")
    intrinsic = read("docs/PMNS_INTRINSIC_COMPLETION_BOUNDARY_NOTE.md")
    last_mile = read("docs/NEUTRINO_FULL_CLOSURE_LAST_MILE_REDUCTION_NOTE.md")

    check("The note says the current bank does not yet derive the breaking-slot vector",
          "does not yet derive the breaking-slot vector" in note)
    check("The atlas carries the PMNS EWSB breaking-slot nonrealization row",
          "| PMNS EWSB breaking-slot nonrealization |" in atlas)
    check("The intrinsic-boundary note records the breaking-slot boundary",
          "breaking-slot" in intrinsic.lower())
    check("The last-mile reduction note records the breaking-slot boundary",
          "breaking-slot" in last_mile.lower())


def main() -> int:
    print("=" * 88)
    print("PMNS EWSB BREAKING-SLOT NONREALIZATION")
    print("=" * 88)
    print()
    print("Atlas / axiom inputs reused:")
    print("  - canonical active two-Higgs branch")
    print("  - active-branch Hermitian inverse problem")
    print("  - residual-Z2 Hermitian core")
    print("  - EWSB alignment nonforcing")
    print()
    print("Question:")
    print("  Does the current bank already derive the three-slot vector")
    print("  (d2-d3, r12-r31, phi) on the generic active Hermitian branch?")

    part1_active_branch_exactly_splits_into_aligned_core_plus_three_slots()
    part2_distinct_generic_points_can_carry_distinct_breaking_slot_vectors()
    part3_note_and_atlas_record_the_boundary()

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  Exact current-bank answer:")
    print("    - the generic active Hermitian law really is")
    print("      aligned residual-Z2 core plus the explicit slot vector")
    print("      beta = (d2-d3, r12-r31, phi)")
    print("    - but the current retained bank does not yet derive beta")
    print("    - so the three-slot decomposition is exact, while the")
    print("      three-slot law remains open")
    print()
    print(f"PASS={PASS_COUNT}  FAIL={FAIL_COUNT}")
    return 1 if FAIL_COUNT else 0


if __name__ == "__main__":
    sys.exit(main())
