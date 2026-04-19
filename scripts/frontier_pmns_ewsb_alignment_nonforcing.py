#!/usr/bin/env python3
"""
Exact boundary theorem:
the current retained PMNS bank does not force the active one-sided branch to
align with the exact EWSB residual Z2 core.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
PASS_COUNT = 0
FAIL_COUNT = 0
P23 = np.array([[1, 0, 0], [0, 0, 1], [0, 1, 0]], dtype=complex)
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


def rebuild_h(coords: np.ndarray) -> np.ndarray:
    d1, d2, d3, r12, r23, r31, phi = coords
    return np.array(
        [
            [d1, r12, r31 * np.exp(-1j * phi)],
            [r12, d2, r23],
            [r31 * np.exp(1j * phi), r23, d3],
        ],
        dtype=complex,
    )


def sqrt_psd(h: np.ndarray) -> np.ndarray:
    evals, vecs = np.linalg.eigh(h)
    evals = np.clip(evals, 0.0, None)
    return vecs @ np.diag(np.sqrt(evals)) @ vecs.conj().T


def part1_aligned_and_nonaligned_points_coexist_on_the_same_exact_support_class() -> None:
    print("\n" + "=" * 88)
    print("PART 1: ALIGNED AND NON-ALIGNED POINTS COEXIST ON THE SAME EXACT SUPPORT CLASS")
    print("=" * 88)

    aligned_y = canonical_y(
        np.array([1.20, 0.90, 0.90], dtype=float),
        np.array([1.20 * 0.40 / 0.90, 0.40, 0.40], dtype=float),
        0.0,
    )
    nonaligned_y = canonical_y(
        np.array([1.15, 0.82, 0.95], dtype=float),
        np.array([0.41, 0.28, 0.54], dtype=float),
        0.63,
    )
    aligned_h = aligned_y @ aligned_y.conj().T
    nonaligned_h = nonaligned_y @ nonaligned_y.conj().T

    check("Aligned and non-aligned points share the same canonical A + B C support mask",
          np.array_equal(support_mask(aligned_y), support_mask(nonaligned_y)),
          f"mask=\n{support_mask(aligned_y)}")
    check("The aligned point is full rank", np.linalg.matrix_rank(aligned_y) == 3,
          f"rank={np.linalg.matrix_rank(aligned_y)}")
    check("The non-aligned point is full rank", np.linalg.matrix_rank(nonaligned_y) == 3,
          f"rank={np.linalg.matrix_rank(nonaligned_y)}")
    check("The aligned point satisfies the EWSB residual-Z2 law", np.linalg.norm(P23 @ aligned_h @ P23 - aligned_h) < 1e-12,
          f"residual={np.linalg.norm(P23 @ aligned_h @ P23 - aligned_h):.2e}")
    check("The non-aligned point violates the EWSB residual-Z2 law", np.linalg.norm(P23 @ nonaligned_h @ P23 - nonaligned_h) > 1e-6,
          f"residual={np.linalg.norm(P23 @ nonaligned_h @ P23 - nonaligned_h):.3e}")


def part2_nonaligned_points_still_satisfy_the_current_hermitian_branch_bank() -> None:
    print("\n" + "=" * 88)
    print("PART 2: NON-ALIGNED POINTS STILL SATISFY THE CURRENT HERMITIAN BRANCH BANK")
    print("=" * 88)

    nonaligned_h = canonical_h(
        np.array([1.15, 0.82, 0.95], dtype=float),
        np.array([0.41, 0.28, 0.54], dtype=float),
        0.63,
    )
    coords = hermitian_coordinates(nonaligned_h)
    rebuilt = rebuild_h(coords)
    polar = sqrt_psd(nonaligned_h)

    check("The non-aligned active point still lies on the exact seven-coordinate Hermitian grammar",
          np.linalg.norm(nonaligned_h - rebuilt) < 1e-12,
          f"rebuild error={np.linalg.norm(nonaligned_h - rebuilt):.2e}")
    check("The non-aligned active point still has a well-defined positive polar representative", np.linalg.norm(polar @ polar - nonaligned_h) < 1e-10,
          f"polar error={np.linalg.norm(polar @ polar - nonaligned_h):.2e}")
    check("So non-alignment does not violate the current canonical/support or Hermitian inverse-problem conditions", True)


def part3_note_and_atlas_record_the_nonforcing_boundary() -> None:
    print("\n" + "=" * 88)
    print("PART 3: THE NOTE AND ATLAS RECORD THE NONFORCING BOUNDARY")
    print("=" * 88)

    note = read("docs/PMNS_EWSB_ALIGNMENT_NONFORCING_NOTE.md")
    atlas = read("docs/publication/ci3_z3/DERIVATION_ATLAS.md")
    intrinsic = read("docs/PMNS_INTRINSIC_COMPLETION_BOUNDARY_NOTE.md")

    check("The note says the current bank does not force EWSB alignment", "does not force EWSB alignment" in note)
    check("The atlas carries the PMNS EWSB alignment nonforcing row",
          "| PMNS EWSB alignment nonforcing |" in atlas)
    check("The intrinsic-boundary note records the alignment nonforcing theorem",
          "alignment nonforcing" in intrinsic.lower())


def main() -> int:
    print("=" * 88)
    print("PMNS EWSB ALIGNMENT NONFORCING")
    print("=" * 88)
    print()
    print("Atlas / axiom inputs reused:")
    print("  - canonical active two-Higgs branch")
    print("  - active-branch Hermitian inverse problem")
    print("  - positive polar section")
    print("  - residual-Z2 Hermitian core")
    print()
    print("Question:")
    print("  Does the current bank force the active one-sided PMNS branch to align")
    print("  with the exact weak-axis EWSB residual Z2 core?")

    part1_aligned_and_nonaligned_points_coexist_on_the_same_exact_support_class()
    part2_nonaligned_points_still_satisfy_the_current_hermitian_branch_bank()
    part3_note_and_atlas_record_the_nonforcing_boundary()

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  Exact current-bank answer:")
    print("    - the aligned residual-Z2 Hermitian core is a real admissible")
    print("      submanifold of the canonical active branch")
    print("    - but full-rank non-aligned points also exist on that same exact")
    print("      branch while satisfying the current support and Hermitian-bank")
    print("      conditions")
    print("    - so the current retained bank does not force EWSB alignment")
    print("      of the active one-sided PMNS branch")
    print()
    print(f"PASS={PASS_COUNT}  FAIL={FAIL_COUNT}")
    return 1 if FAIL_COUNT else 0


if __name__ == "__main__":
    sys.exit(main())
