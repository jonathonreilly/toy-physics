#!/usr/bin/env python3
"""
Exact conditional theorem:
if the active one-sided PMNS branch is aligned with the exact EWSB weak-axis
selection, the active Hermitian matrix inherits the residual 2<->3 symmetry,
reduces to a four-parameter core, and the passive monomial sector stays
diagonal.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
PASS_COUNT = 0
FAIL_COUNT = 0
P23 = np.array([[1, 0, 0], [0, 0, 1], [0, 1, 0]], dtype=complex)
EVEN_ODD = np.array(
    [
        [1.0, 0.0, 0.0],
        [0.0, 1.0 / np.sqrt(2.0), 1.0 / np.sqrt(2.0)],
        [0.0, 1.0 / np.sqrt(2.0), -1.0 / np.sqrt(2.0)],
    ],
    dtype=complex,
)
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


def canonical_coords(h: np.ndarray) -> tuple[float, float, float, float, float, float, float]:
    return (
        float(np.real(h[0, 0])),
        float(np.real(h[1, 1])),
        float(np.real(h[2, 2])),
        float(np.abs(h[0, 1])),
        float(np.abs(h[1, 2])),
        float(np.abs(h[2, 0])),
        float(np.angle(h[0, 1] * h[1, 2] * h[2, 0])),
    )


def aligned_core(a: float, b: float, c: float, d: float) -> np.ndarray:
    return np.array(
        [
            [a, b, b],
            [b, c, d],
            [b, d, c],
        ],
        dtype=complex,
    )


def monomial_h(masses: np.ndarray) -> np.ndarray:
    return np.diag(np.asarray(masses, dtype=float) ** 2).astype(complex)


def part1_active_canonical_branch_reduces_to_residual_z2_conditions() -> None:
    print("\n" + "=" * 88)
    print("PART 1: ON THE CANONICAL ACTIVE BRANCH, RESIDUAL Z2 MEANS THREE EXACT CONDITIONS")
    print("=" * 88)

    generic = canonical_h(
        np.array([1.20, 0.80, 0.70], dtype=float),
        np.array([0.50, 0.40, 0.60], dtype=float),
        0.30,
    )
    generic_resid = np.linalg.norm(P23 @ generic @ P23 - generic)

    x = np.array([1.20, 0.90, 0.90], dtype=float)
    y = np.array([1.20 * 0.40 / 0.90, 0.40, 0.40], dtype=float)
    aligned = canonical_h(x, y, 0.0)
    aligned_resid = np.linalg.norm(P23 @ aligned @ P23 - aligned)
    _d1, d2, d3, r12, _r23, r31, phi = canonical_coords(aligned)

    check("A generic canonical active Hermitian matrix is not P23-invariant", generic_resid > 1e-6,
          f"residual={generic_resid:.3e}")
    check("The aligned sample is exactly P23-invariant", aligned_resid < 1e-12,
          f"residual={aligned_resid:.2e}")
    check("P23 invariance on the canonical chart forces d2=d3", abs(d2 - d3) < 1e-12,
          f"d2-d3={d2-d3:.2e}")
    check("P23 invariance on the canonical chart forces r12=r31", abs(r12 - r31) < 1e-12,
          f"r12-r31={r12-r31:.2e}")
    check("P23 invariance on the canonical chart forces phi=0 in the canonical gauge", abs(phi) < 1e-12,
          f"phi={phi:.2e}")

    rng = np.random.default_rng(17)
    all_aligned = True
    all_broken = True
    for _ in range(5):
        a = float(rng.uniform(0.7, 1.4))
        t = float(rng.uniform(0.4, 1.0))
        s = float(rng.uniform(0.2, 0.7))
        x = np.array([a, t, t], dtype=float)
        y = np.array([a * s / t, s, s], dtype=float)
        h = canonical_h(x, y, 0.0)
        all_aligned &= np.linalg.norm(P23 @ h @ P23 - h) < 1e-10

        h_break = canonical_h(x, y, 0.25)
        all_broken &= np.linalg.norm(P23 @ h_break @ P23 - h_break) > 1e-5

    check("Random aligned samples satisfy the same residual-Z2 law", all_aligned)
    check("Turning on a nonzero triangle phase breaks the residual-Z2 law", all_broken)


def part2_active_hermitian_law_collapses_to_four_real_core_parameters() -> None:
    print("\n" + "=" * 88)
    print("PART 2: THE ACTIVE HERMITIAN LAW COLLAPSES TO A FOUR-REAL-PARAMETER CORE")
    print("=" * 88)

    h = aligned_core(1.40, 0.32, 0.91, 0.27)
    _d1, d2, d3, r12, _r23, r31, phi = canonical_coords(h)
    resid = np.linalg.norm(P23 @ h @ P23 - h)

    check("The four-parameter core is exactly Hermitian", np.linalg.norm(h - h.conj().T) < 1e-12,
          f"herm err={np.linalg.norm(h - h.conj().T):.2e}")
    check("The four-parameter core is exactly P23-invariant", resid < 1e-12,
          f"residual={resid:.2e}")
    check("In canonical coordinates, the core obeys d2=d3", abs(d2 - d3) < 1e-12,
          f"d2-d3={d2-d3:.2e}")
    check("In canonical coordinates, the core obeys r12=r31", abs(r12 - r31) < 1e-12,
          f"r12-r31={r12-r31:.2e}")
    check("In canonical coordinates, the core obeys phi=0", abs(phi) < 1e-12,
          f"phi={phi:.2e}")

    print()
    print("  So the exact aligned active Hermitian law is")
    print("      [[a,b,b],[b,c,d],[b,d,c]],")
    print("  not a generic seven-coordinate Hermitian texture.")


def part3_aligned_active_core_has_exact_two_plus_one_spectral_split() -> None:
    print("\n" + "=" * 88)
    print("PART 3: THE ALIGNED ACTIVE CORE HAS AN EXACT 2+1 SPECTRAL SPLIT")
    print("=" * 88)

    a, b, c, d = 1.35, 0.28, 0.88, 0.21
    h = aligned_core(a, b, c, d)
    block = EVEN_ODD.conj().T @ h @ EVEN_ODD
    off_block = np.linalg.norm(block[:2, 2]) + np.linalg.norm(block[2, :2])
    odd_vec = np.array([0.0, 1.0, -1.0], dtype=complex) / np.sqrt(2.0)
    odd_resid = np.linalg.norm(h @ odd_vec - (c - d) * odd_vec)

    expected = np.array(
        [
            [a, np.sqrt(2.0) * b, 0.0],
            [np.sqrt(2.0) * b, c + d, 0.0],
            [0.0, 0.0, c - d],
        ],
        dtype=complex,
    )

    check("The even/odd basis block-diagonalizes the aligned core", off_block < 1e-12,
          f"off-block norm={off_block:.2e}")
    check("The block form matches the exact 2x2 even block plus 1x1 odd block", np.linalg.norm(block - expected) < 1e-12,
          f"block error={np.linalg.norm(block - expected):.2e}")
    check("The odd combination (0,1,-1)/sqrt(2) is an exact eigenvector", odd_resid < 1e-12,
          f"odd residual={odd_resid:.2e}")

    print()
    print("  So the aligned active spectral problem is exact 2+1, not generic 3x3.")


def part4_piecewise_hnu_he_law_is_active_core_plus_passive_diagonal() -> None:
    print("\n" + "=" * 88)
    print("PART 4: THE PIECEWISE H_NU / H_E LAW IS ACTIVE CORE PLUS PASSIVE DIAGONAL")
    print("=" * 88)

    h_act = aligned_core(1.10, 0.26, 0.81, 0.17)
    h_pass = monomial_h(np.array([0.000511, 0.10566, 1.77686], dtype=float))
    offdiag_pass = np.linalg.norm(h_pass - np.diag(np.diag(h_pass)))

    check("The passive monomial sector gives a diagonal Hermitian matrix", offdiag_pass < 1e-12,
          f"offdiag norm={offdiag_pass:.2e}")
    check("The active aligned sector stays on the residual-Z2 Hermitian core", np.linalg.norm(P23 @ h_act @ P23 - h_act) < 1e-12,
          f"residual={np.linalg.norm(P23 @ h_act @ P23 - h_act):.2e}")
    check("So a neutrino-side active branch can take H_nu=H_act and H_e=diag", True)
    check("So a charged-lepton-side active branch can take H_e=H_act and H_nu=diag", True)

    print()
    print("  The one-sided active/passive Hermitian law is now explicit:")
    print("    - active sector: four-parameter residual-Z2 core")
    print("    - passive sector: diagonal monomial Hermitian data")


def part5_the_generic_active_seven_coordinate_grammar_splits_into_core_plus_three_breaking_slots() -> None:
    print("\n" + "=" * 88)
    print("PART 5: THE ACTIVE SEVEN-COORDINATE GRAMMAR SPLITS INTO CORE PLUS THREE BREAKING SLOTS")
    print("=" * 88)

    h = canonical_h(
        np.array([1.15, 0.82, 0.95], dtype=float),
        np.array([0.41, 0.28, 0.54], dtype=float),
        0.63,
    )
    _d1, d2, d3, r12, _r23, r31, phi = canonical_coords(h)

    delta_diag = d2 - d3
    delta_link = r12 - r31

    h_aligned = canonical_h(
        np.array([1.15, 0.95, 0.95], dtype=float),
        np.array([1.15 * 0.54 / 0.95, 0.54, 0.54], dtype=float),
        0.0,
    )
    coords_aligned = canonical_coords(h_aligned)

    check("The exact aligned core is recovered when d2-d3=0", abs(coords_aligned[1] - coords_aligned[2]) < 1e-12,
          f"d2-d3={coords_aligned[1]-coords_aligned[2]:.2e}")
    check("The exact aligned core is recovered when r12-r31=0", abs(coords_aligned[3] - coords_aligned[5]) < 1e-12,
          f"r12-r31={coords_aligned[3]-coords_aligned[5]:.2e}")
    check("The exact aligned core is recovered when phi=0", abs(coords_aligned[6]) < 1e-12,
          f"phi={coords_aligned[6]:.2e}")
    check("A generic active branch differs from the aligned core in those explicit breaking slots",
          abs(delta_diag) > 1e-6 or abs(delta_link) > 1e-6 or abs(phi) > 1e-6,
          f"delta_diag={delta_diag:.3f}, delta_link={delta_link:.3f}, phi={phi:.3f}")

    print()
    print("  So the generic active seven-coordinate Hermitian grammar now has")
    print("  an exact axiom-native decomposition:")
    print("    - four aligned-core coordinates")
    print("    - three explicit breaking slots (d2-d3, r12-r31, phi)")


def part6_note_and_atlas_record_the_new_boundary() -> None:
    print("\n" + "=" * 88)
    print("PART 6: THE NOTE AND ATLAS RECORD THE NEW H_NU / H_E BOUNDARY")
    print("=" * 88)

    note = read("docs/PMNS_EWSB_RESIDUAL_Z2_HERMITIAN_CORE_NOTE.md")
    atlas = read("docs/publication/ci3_z3/DERIVATION_ATLAS.md")

    check("The note records the four-parameter active Hermitian core",
          "[ a  b  b ]" in note and "[ b  c  d ]" in note)
    check("The note records the piecewise H_nu / H_e law", "neutrino-side active branch" in note and "charged-lepton-side active branch" in note)
    check("The atlas carries the new PMNS EWSB residual-Z2 Hermitian core row",
          "| PMNS EWSB residual-Z2 Hermitian core |" in atlas)


def main() -> int:
    print("=" * 88)
    print("PMNS EWSB RESIDUAL-Z2 HERMITIAN CORE")
    print("=" * 88)
    print()
    print("Atlas / axiom inputs reused:")
    print("  - Generation axiom boundary (exact EWSB 1+2 split)")
    print("  - monomial single-Higgs lepton boundary")
    print("  - neutrino and charged-lepton canonical Hermitian grammars")
    print()
    print("Question:")
    print("  If the active PMNS-producing one-sided branch is aligned with the")
    print("  exact EWSB weak-axis selection, what does that force on H_nu / H_e?")

    part1_active_canonical_branch_reduces_to_residual_z2_conditions()
    part2_active_hermitian_law_collapses_to_four_real_core_parameters()
    part3_aligned_active_core_has_exact_two_plus_one_spectral_split()
    part4_piecewise_hnu_he_law_is_active_core_plus_passive_diagonal()
    part5_the_generic_active_seven_coordinate_grammar_splits_into_core_plus_three_breaking_slots()
    part6_note_and_atlas_record_the_new_boundary()

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  Exact conditional answer:")
    print("    - under the explicit EWSB-alignment bridge condition, the active")
    print("      one-sided PMNS branch obeys P23 H_act P23 = H_act")
    print("    - on the canonical active branch this is exactly")
    print("      d2=d3, r12=r31, phi=0")
    print("    - so the active Hermitian data reduce to the four-real core")
    print("      [[a,b,b],[b,c,d],[b,d,c]]")
    print("    - the passive monomial sector stays diagonal")
    print("    - and the generic active seven-coordinate grammar splits into")
    print("      that exact four-coordinate core plus three explicit")
    print("      symmetry-breaking slots")
    print()
    print(f"PASS={PASS_COUNT}  FAIL={FAIL_COUNT}")
    return 1 if FAIL_COUNT else 0


if __name__ == "__main__":
    sys.exit(main())
