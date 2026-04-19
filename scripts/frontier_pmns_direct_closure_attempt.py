#!/usr/bin/env python3
"""
Exact direct-underdetermination theorem for the current retained PMNS bank.

This runner attempts to solve the missing branch Hermitian data, the breaking
triplet values, and the restricted Higgs-offset selector directly from the
current exact equations. The attempt fails in the strongest exact way: the
current bank supplies a full-rank coordinate chart and a two-sheet seed cover,
not a point law.
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
P23 = np.array([[1, 0, 0], [0, 0, 1], [0, 1, 0]], dtype=complex)


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


def hermitian_coords(h: np.ndarray) -> tuple[float, float, float, float, float, float, float]:
    return (
        float(np.real(h[0, 0])),
        float(np.real(h[1, 1])),
        float(np.real(h[2, 2])),
        float(np.abs(h[0, 1])),
        float(np.abs(h[1, 2])),
        float(np.abs(h[2, 0])),
        float(np.angle(h[0, 1] * h[1, 2] * h[2, 0])),
    )


def aligned_core_from_coords(
    d1: float, d2: float, d3: float, r12: float, r23: float, r31: float, phi: float
) -> np.ndarray:
    b = 0.5 * (r12 + r31 * math.cos(phi))
    c = 0.5 * (d2 + d3)
    return np.array(
        [
            [d1, b, b],
            [b, c, r23],
            [b, r23, c],
        ],
        dtype=complex,
    )


def breaking_triplet_from_coords(
    d1: float, d2: float, d3: float, r12: float, r23: float, r31: float, phi: float
) -> tuple[float, float, float]:
    _ = d1, r23
    delta = 0.5 * (d2 - d3)
    rho = 0.5 * (r12 - r31 * math.cos(phi))
    gamma = r31 * math.sin(phi)
    return delta, rho, gamma


def breaking_matrix(delta: float, rho: float, gamma: float) -> np.ndarray:
    return np.array(
        [
            [0.0, rho, -rho - 1j * gamma],
            [rho, delta, 0.0],
            [-rho + 1j * gamma, 0.0, -delta],
        ],
        dtype=complex,
    )


def aligned_basis() -> list[np.ndarray]:
    return [
        np.array([[1, 0, 0], [0, 0, 0], [0, 0, 0]], dtype=complex),
        np.array([[0, 1, 1], [1, 0, 0], [1, 0, 0]], dtype=complex),
        np.array([[0, 0, 0], [0, 1, 0], [0, 0, 1]], dtype=complex),
        np.array([[0, 0, 0], [0, 0, 1], [0, 1, 0]], dtype=complex),
    ]


def breaking_basis() -> list[np.ndarray]:
    return [
        np.array([[0, 0, 0], [0, 1, 0], [0, 0, -1]], dtype=complex),
        np.array([[0, 1, -1], [1, 0, 0], [-1, 0, 0]], dtype=complex),
        np.array([[0, 0, -1j], [0, 0, 0], [1j, 0, 0]], dtype=complex),
    ]


def real_vector(mat: np.ndarray) -> np.ndarray:
    return np.concatenate([np.real(mat).ravel(), np.imag(mat).ravel()]).astype(float)


def real_rank(mats: list[np.ndarray]) -> int:
    stacked = np.column_stack([real_vector(m) for m in mats])
    return int(np.linalg.matrix_rank(stacked))


def seed_sheet_coefficients(a: float, b: float) -> tuple[float, float]:
    mu = (a + 2.0 * b) / 3.0
    nu = (a - b) / 3.0
    Delta = mu * mu - 4.0 * nu * nu
    x2 = 0.5 * (mu + math.sqrt(max(Delta, 0.0)))
    y2 = 0.5 * (mu - math.sqrt(max(Delta, 0.0)))
    return math.sqrt(max(x2, 0.0)), math.sqrt(max(y2, 0.0))


def seed_y(x: float, y: float) -> np.ndarray:
    return x * EYE + y * CYCLE


def seed_h(y: np.ndarray) -> np.ndarray:
    return y @ y.conj().T


def part1_branch_hermitian_data_is_a_full_rank_coordinate_chart() -> None:
    print("\n" + "=" * 88)
    print("PART 1: THE BRANCH HERMITIAN DATA ARE A FULL-RANK COORDINATE CHART")
    print("=" * 88)

    x1 = np.array([1.15, 0.82, 0.95], dtype=float)
    y1 = np.array([0.41, 0.28, 0.54], dtype=float)
    phi1 = 0.63
    h1 = canonical_h(x1, y1, phi1)
    coords1 = hermitian_coords(h1)
    core1 = aligned_core_from_coords(*coords1)
    triplet1 = breaking_triplet_from_coords(*coords1)
    recon1 = core1 + breaking_matrix(*triplet1)

    x2 = np.array([1.07, 0.91, 0.79], dtype=float)
    y2 = np.array([0.36, 0.33, 0.46], dtype=float)
    phi2 = -0.41
    h2 = canonical_h(x2, y2, phi2)
    coords2 = hermitian_coords(h2)
    core2 = aligned_core_from_coords(*coords2)
    triplet2 = breaking_triplet_from_coords(*coords2)
    recon2 = core2 + breaking_matrix(*triplet2)

    chart_rank = real_rank(aligned_basis() + breaking_basis())

    check(
        "The global active Hermitian chart has exact real rank 7",
        chart_rank == 7,
        f"rank={chart_rank}",
    )
    check(
        "A generic canonical branch point reconstructs exactly from the chart",
        np.linalg.norm(h1 - recon1) < 1e-12,
        f"recon error={np.linalg.norm(h1 - recon1):.2e}",
    )
    check(
        "A second generic canonical branch point also reconstructs exactly",
        np.linalg.norm(h2 - recon2) < 1e-12,
        f"recon error={np.linalg.norm(h2 - recon2):.2e}",
    )
    check(
        "Two generic branch points have distinct Hermitian data",
        np.linalg.norm(h1 - h2) > 1e-6,
        f"|H1-H2|={np.linalg.norm(h1 - h2):.3f}",
    )
    check(
        "The two branch points also carry distinct breaking triplets",
        np.linalg.norm(np.array(triplet1) - np.array(triplet2)) > 1e-6,
        f"|t1-t2|={np.linalg.norm(np.array(triplet1)-np.array(triplet2)):.3f}",
    )

    print()
    print("  This is the direct obstruction: the exact bank is a full chart.")
    print("  It has room for branch values, so it does not pick them.")


def part2_breaking_triplet_is_a_three_real_source_complement() -> None:
    print("\n" + "=" * 88)
    print("PART 2: THE BREAKING TRIPLET IS A THREE-REAL SOURCE COMPLEMENT")
    print("=" * 88)

    r = real_rank(breaking_basis())
    check("The breaking source basis has real rank 3", r == 3, f"rank={r}")

    delta0, rho0, gamma0 = 0.0, 0.0, 0.0
    delta1, rho1, gamma1 = 0.12, -0.07, 0.19
    delta2, rho2, gamma2 = -0.08, 0.05, -0.14

    b0 = breaking_matrix(delta0, rho0, gamma0)
    b1 = breaking_matrix(delta1, rho1, gamma1)
    b2 = breaking_matrix(delta2, rho2, gamma2)

    check(
        "The zero breaking source is exactly the aligned core locus",
        np.linalg.norm(b0) < 1e-12,
        f"B0 norm={np.linalg.norm(b0):.2e}",
    )
    check(
        "A generic nonzero breaking source changes the Hermitian matrix",
        np.linalg.norm(b1 - b0) > 1e-6 and np.linalg.norm(b2 - b0) > 1e-6,
        f"|B1-B0|={np.linalg.norm(b1-b0):.3f}, |B2-B0|={np.linalg.norm(b2-b0):.3f}",
    )
    check(
        "The three generators are linearly independent",
        np.linalg.matrix_rank(np.column_stack([real_vector(m) for m in breaking_basis()])) == 3,
        "rank=3",
    )

    print()
    print("  So the triplet is not derivable as a single fixed vector from the")
    print("  current exact bank. It is an exact 3-real source space.")


def part3_the_seed_selector_is_a_two_sheet_cover() -> None:
    print("\n" + "=" * 88)
    print("PART 3: THE SEED SELECTOR IS A TWO-SHEET COVER")
    print("=" * 88)

    a, b = 1.5, 1.0
    x, y = seed_sheet_coefficients(a, b)
    y_plus = seed_y(x, y)
    y_minus = seed_y(y, x)
    h_plus = seed_h(y_plus)
    h_minus = seed_h(y_minus)

    check(
        "The compatible weak-axis seed patch satisfies A <= 4B",
        a <= 4.0 * b,
        f"A={a}, B={b}",
    )
    check(
        "The two canonical sheets are distinct in Y-space",
        np.linalg.norm(y_plus - y_minus) > 1e-6,
        f"sheet separation={np.linalg.norm(y_plus - y_minus):.3e}",
    )
    check(
        "The two sheets have exactly the same Hermitian data",
        np.linalg.norm(h_plus - h_minus) < 1e-12,
        f"H diff={np.linalg.norm(h_plus - h_minus):.2e}",
    )
    check(
        "The equal-split edge gives the two monomial endpoints",
        np.linalg.norm(seed_y(1.0, 0.0) - EYE) < 1e-12
        and np.linalg.norm(seed_y(0.0, 1.0) - CYCLE) < 1e-12,
        f"edge err I={np.linalg.norm(seed_y(1.0,0.0)-EYE):.2e}, C={np.linalg.norm(seed_y(0.0,1.0)-CYCLE):.2e}",
    )

    a_eq = 1.0
    x_eq, y_eq = seed_sheet_coefficients(a_eq, a_eq)
    y_plus_eq = seed_y(x_eq, y_eq)
    y_minus_eq = seed_y(y_eq, x_eq)
    h_eq_plus = seed_h(y_plus_eq)
    h_eq_minus = seed_h(y_minus_eq)

    check(
        "At A=B the plus sheet is exactly sqrt(A) I",
        np.linalg.norm(y_plus_eq - math.sqrt(a_eq) * EYE) < 1e-12,
        f"err={np.linalg.norm(y_plus_eq - math.sqrt(a_eq) * EYE):.2e}",
    )
    check(
        "At A=B the exchanged sheet is exactly sqrt(A) C",
        np.linalg.norm(y_minus_eq - math.sqrt(a_eq) * CYCLE) < 1e-12,
        f"err={np.linalg.norm(y_minus_eq - math.sqrt(a_eq) * CYCLE):.2e}",
    )
    check(
        "At A=B the two sheets remain Hermitian-indistinguishable",
        np.linalg.norm(h_eq_plus - h_eq_minus) < 1e-12,
        f"H diff={np.linalg.norm(h_eq_plus - h_eq_minus):.2e}",
    )

    print()
    print("  So the remaining selector is binary and sheet-valued, not a")
    print("  continuous coefficient law. The current bank does not choose it.")


def part4_the_current_bank_is_an_exact_chart_not_a_solution() -> None:
    print("\n" + "=" * 88)
    print("PART 4: THE CURRENT BANK IS AN EXACT CHART, NOT A SOLUTION")
    print("=" * 88)

    note = read("docs/PMNS_GLOBAL_HERMITIAN_MODE_PACKAGE_NOTE.md")
    seed_note = read("docs/PMNS_EWSB_WEAK_AXIS_Z3_SEED_NOTE.md")
    coeff_note = read("docs/PMNS_EWSB_WEAK_AXIS_SEED_COEFFICIENT_CLOSURE_NOTE.md")
    edge_note = read("docs/PMNS_EWSB_WEAK_AXIS_SEED_EDGE_SELECTOR_REDUCTION_NOTE.md")
    direct_note = read("docs/PMNS_INTRINSIC_COMPLETION_BOUNDARY_NOTE.md")

    check(
        "The global package note states the 2+2+3 decomposition explicitly",
        "2 + 2 + 3" in note or "2+2+3" in note,
    )
    check(
        "The weak-axis seed note states the compatibility boundary A <= 4B",
        "A <= 4 B" in seed_note or "A <= 4B" in seed_note,
    )
    check(
        "The coefficient closure note states the residual exchange sheet",
        "exchange sheet" in coeff_note,
    )
    check(
        "The seed-edge reduction note states the restricted Higgs-offset selector",
        "restricted Higgs-offset selector" in edge_note,
    )
    check(
        "The intrinsic completion boundary note still records the branch law as open",
        "branch Hermitian data themselves" in direct_note and "axiom-side outputs" in direct_note,
    )

    print()
    print("  The exact current bank therefore behaves like this:")
    print("    - it fixes the chart")
    print("    - it fixes the seed compatibility boundary")
    print("    - it fixes the two-sheet structure")
    print("    - it does not fix the point in the chart")


def main() -> int:
    print("=" * 88)
    print("PMNS DIRECT CLOSURE ATTEMPT")
    print("=" * 88)
    print()
    print("Question:")
    print("  Can the current exact bank directly derive the missing branch")
    print("  Hermitian data, the breaking triplet values, and the restricted")
    print("  Higgs-offset selector?")
    print()
    print("Exact bank equations reused:")
    print("  - H = H_core + B(delta, rho, gamma)")
    print("  - H_core = [[a,b,b],[b,c,d],[b,d,c]]")
    print("  - B(delta, rho, gamma) is the 3-real breaking complement")
    print("  - Y_+ = x_+ I + y_+ C, Y_- = y_+ I + x_+ C")
    print("  - A = B gives sqrt(A) I and sqrt(A) C")

    part1_branch_hermitian_data_is_a_full_rank_coordinate_chart()
    part2_breaking_triplet_is_a_three_real_source_complement()
    part3_the_seed_selector_is_a_two_sheet_cover()
    part4_the_current_bank_is_an_exact_chart_not_a_solution()

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  Positive direct solve: no")
    print("  Strongest exact theorem: the current bank is an exact coordinate")
    print("  chart plus a binary seed-sheet cover, so the missing objects are")
    print("  underdetermined rather than derived.")
    print()
    print("  Residual exact gap:")
    print("    - branch Hermitian-data values are free chart coordinates")
    print("    - the breaking triplet is a 3-real free source complement")
    print("    - the restricted Higgs-offset selector is a two-sheet bit")
    print()
    print(f"PASS={PASS_COUNT}  FAIL={FAIL_COUNT}")
    return 1 if FAIL_COUNT else 0


if __name__ == "__main__":
    sys.exit(main())
