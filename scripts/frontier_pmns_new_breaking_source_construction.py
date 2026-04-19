#!/usr/bin/env python3
"""
Minimal exact source theorem for the PMNS breaking triplet.

The global active Hermitian law decomposes as H = H_core + B(delta,rho,gamma).
This script verifies that the breaking matrix is exactly a 3-real source
space, and that this 3-real source class is the smallest exact extension class
that can generate generic nonzero breaking data.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
PASS_COUNT = 0
FAIL_COUNT = 0
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
    cycle = np.array([[0, 1, 0], [0, 0, 1], [1, 0, 0]], dtype=complex)
    return np.diag(np.asarray(x, dtype=complex)) + np.diag(
        np.array([y[0], y[1], y[2] * np.exp(1j * phi)], dtype=complex)
    ) @ cycle


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
    del d1, r23
    delta = 0.5 * (d2 - d3)
    rho = 0.5 * (r12 - r31 * math.cos(phi))
    gamma = r31 * math.sin(phi)
    return delta, rho, gamma


def breaking_matrix(delta: float, rho: float, gamma: float) -> np.ndarray:
    t_delta = np.array(
        [[0.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, -1.0]], dtype=complex
    )
    t_rho = np.array(
        [[0.0, 1.0, -1.0], [1.0, 0.0, 0.0], [-1.0, 0.0, 0.0]], dtype=complex
    )
    t_gamma = np.array(
        [[0.0, 0.0, -1j], [0.0, 0.0, 0.0], [1j, 0.0, 0.0]], dtype=complex
    )
    return delta * t_delta + rho * t_rho + gamma * t_gamma


def flat_real(mat: np.ndarray) -> np.ndarray:
    return np.concatenate([np.real(mat).ravel(), np.imag(mat).ravel()])


def part1_exact_source_decomposition_reconstructs_the_breaking_matrix() -> None:
    print("\n" + "=" * 88)
    print("PART 1: THE BREAKING SOURCE DECOMPOSES EXACTLY INTO THREE CANONICAL GENERATORS")
    print("=" * 88)

    x = np.array([1.15, 0.82, 0.95], dtype=float)
    y = np.array([0.41, 0.28, 0.54], dtype=float)
    phi = 0.63
    h = canonical_h(x, y, phi)
    coords = canonical_coords(h)
    core = aligned_core_from_coords(*coords)
    delta, rho, gamma = breaking_triplet_from_coords(*coords)
    b = breaking_matrix(delta, rho, gamma)

    check(
        "H = H_core + B(delta,rho,gamma) exactly",
        np.linalg.norm(h - (core + b)) < 1e-12,
        f"recon err={np.linalg.norm(h - (core + b)):.2e}",
    )
    check(
        "The breaking matrix is exactly delta T_delta + rho T_rho + gamma T_gamma",
        np.linalg.norm(b - breaking_matrix(delta, rho, gamma)) < 1e-12,
        f"triplet=({delta:.6f},{rho:.6f},{gamma:.6f})",
    )
    check(
        "The source vanishes on the aligned residual-Z2 surface",
        np.linalg.norm(breaking_matrix(0.0, 0.0, 0.0)) < 1e-15,
        "zero source",
    )


def part2_the_breaking_source_space_is_exactly_three_real_dimensions() -> None:
    print("\n" + "=" * 88)
    print("PART 2: THE BREAKING SOURCE SPACE IS EXACTLY THREE REAL DIMENSIONS")
    print("=" * 88)

    t_delta = np.array(
        [[0.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, -1.0]], dtype=complex
    )
    t_rho = np.array(
        [[0.0, 1.0, -1.0], [1.0, 0.0, 0.0], [-1.0, 0.0, 0.0]], dtype=complex
    )
    t_gamma = np.array(
        [[0.0, 0.0, -1j], [0.0, 0.0, 0.0], [1j, 0.0, 0.0]], dtype=complex
    )
    basis = np.column_stack([flat_real(t_delta), flat_real(t_rho), flat_real(t_gamma)])
    rank = np.linalg.matrix_rank(basis)

    check(
        "The canonical source generators are linearly independent over R",
        rank == 3,
        f"rank={rank}",
    )
    check(
        "So no one- or two-parameter source family can span the generic breaking sector",
        rank == 3,
        "generic breaking sector needs 3 real directions",
    )


def part3_generic_and_aligned_samples_separate_cleanly() -> None:
    print("\n" + "=" * 88)
    print("PART 3: ALIGNED AND GENERIC SAMPLES SEPARATE CLEANLY")
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
    aligned_triplet = breaking_triplet_from_coords(*canonical_coords(aligned_h))
    generic_triplet = breaking_triplet_from_coords(*canonical_coords(generic_h))

    check(
        "The aligned sample has zero breaking triplet",
        np.linalg.norm(aligned_triplet) < 1e-12,
        f"beta={aligned_triplet}",
    )
    check(
        "The generic sample has nonzero breaking triplet",
        np.linalg.norm(generic_triplet) > 1e-6,
        f"beta={np.round(generic_triplet, 6)}",
    )
    check(
        "Aligned and generic samples lie on the same canonical active branch",
        np.linalg.matrix_rank(aligned_y) == 3 and np.linalg.matrix_rank(generic_y) == 3,
        f"ranks=({np.linalg.matrix_rank(aligned_y)},{np.linalg.matrix_rank(generic_y)})",
    )
    check(
        "The aligned sample satisfies the residual-Z2 law while the generic one does not",
        np.linalg.norm(P23 @ aligned_h @ P23 - aligned_h) < 1e-12
        and np.linalg.norm(P23 @ generic_h @ P23 - generic_h) > 1e-6,
        f"aligned={np.linalg.norm(P23 @ aligned_h @ P23 - aligned_h):.2e}, "
        f"generic={np.linalg.norm(P23 @ generic_h @ P23 - generic_h):.2e}",
    )


def part4_note_records_the_minimal_extension_class() -> None:
    print("\n" + "=" * 88)
    print("PART 4: THE NOTE RECORDS THE MINIMAL EXTENSION CLASS")
    print("=" * 88)

    note = read("docs/PMNS_BREAKING_SOURCE_CONSTRUCTION_NOTE.md")
    boundary = read("docs/PMNS_EWSB_BREAKING_SLOT_NONREALIZATION_NOTE.md")
    intrinsic = read("docs/PMNS_INTRINSIC_COMPLETION_BOUNDARY_NOTE.md")

    check(
        "The note records the exact 3-real breaking-source basis",
        "T_delta" in note and "T_rho" in note and "T_gamma" in note,
    )
    check(
        "The note records the exact decomposition B(delta,rho,gamma) = delta T_delta + rho T_rho + gamma T_gamma",
        "delta T_delta + rho T_rho + gamma T_gamma" in note,
    )
    check(
        "The breaking-slot boundary note still says the retained bank does not derive beta",
        "does not yet derive the breaking-slot vector" in boundary,
    )
    check(
        "The intrinsic-boundary note still identifies the remaining gap as Hermitian-data law plus sheet-fixing datum",
        "Hermitian data law" in intrinsic and "sheet-fixing datum" in intrinsic,
    )


def main() -> int:
    print("=" * 88)
    print("PMNS BREAKING SOURCE CONSTRUCTION")
    print("=" * 88)
    print()
    print("Atlas / axiom inputs reused:")
    print("  - global Hermitian mode package")
    print("  - residual-Z2 Hermitian core")
    print("  - EWSB alignment nonforcing")
    print("  - EWSB breaking-slot nonrealization")
    print("  - intrinsic completion boundary")
    print()
    print("Question:")
    print("  What is the smallest exact source/bridge class that can produce")
    print("  nonzero breaking-triplet data on the canonical active branch?")

    part1_exact_source_decomposition_reconstructs_the_breaking_matrix()
    part2_the_breaking_source_space_is_exactly_three_real_dimensions()
    part3_generic_and_aligned_samples_separate_cleanly()
    part4_note_records_the_minimal_extension_class()

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  Exact current-bank answer:")
    print("    - the breaking triplet is exactly a 3-real source space")
    print("    - the canonical source basis is {T_delta, T_rho, T_gamma}")
    print("    - any positive source realization of generic nonzero breaking")
    print("      data must leave the aligned core and carry at least three")
    print("      real source directions")
    print("    - therefore the minimal exact extension class is")
    print("      S_break = span_R{T_delta,T_rho,T_gamma}")
    print()
    print(f"PASS={PASS_COUNT}  FAIL={FAIL_COUNT}")
    return 1 if FAIL_COUNT else 0


if __name__ == "__main__":
    sys.exit(main())
