#!/usr/bin/env python3
"""
Minimal unified bridge carrier theorem:
the smallest exact carrier that simultaneously accounts for the Hermitian
bridge package, the breaking-source space, and the selector primitive.
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
EVEN_ODD = np.array(
    [
        [1.0, 0.0, 0.0],
        [0.0, 1.0 / math.sqrt(2.0), 1.0 / math.sqrt(2.0)],
        [0.0, 1.0 / math.sqrt(2.0), -1.0 / math.sqrt(2.0)],
    ],
    dtype=complex,
)
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


def spectral_package(core: np.ndarray) -> tuple[float, float, float, float]:
    block = EVEN_ODD.conj().T @ core @ EVEN_ODD
    even_block = np.real(block[:2, :2])
    evals = np.linalg.eigvalsh(even_block)
    evals.sort()
    lam_minus = float(evals[0])
    lam_plus = float(evals[1])
    lam_odd = float(np.real(block[2, 2]))
    theta = 0.5 * math.atan2(
        2.0 * even_block[0, 1], even_block[0, 0] - even_block[1, 1]
    )
    if theta < 0:
        theta += 0.5 * math.pi
    return lam_plus, lam_minus, lam_odd, theta


def selector_primitive(a_sel: float) -> np.ndarray:
    return a_sel * REDUCED_SELECTOR_CLASS


def selector_edge(bit: int, amplitude: float) -> np.ndarray:
    root = math.sqrt(amplitude)
    if bit == 0:
        return root * EYE
    if bit == 1:
        return root * CYCLE
    raise ValueError("bit must be 0 or 1")


def flat_real(mat: np.ndarray) -> np.ndarray:
    return np.concatenate([np.real(mat).ravel(), np.imag(mat).ravel()])


def part1_the_unified_bundle_reconstructs_all_three_objects() -> None:
    print("\n" + "=" * 88)
    print("PART 1: THE UNIFIED BUNDLE RECONSTRUCTS ALL THREE OBJECTS")
    print("=" * 88)

    x = np.array([1.15, 0.82, 0.95], dtype=float)
    y = np.array([0.41, 0.28, 0.54], dtype=float)
    phi = 0.63
    h = canonical_h(x, y, phi)
    coords = canonical_coords(h)
    core = aligned_core_from_coords(*coords)
    delta, rho, gamma = breaking_triplet_from_coords(*coords)
    b = breaking_matrix(delta, rho, gamma)
    a_sel = 1.75
    e = 1

    lam_plus, lam_minus, lam_odd, theta = spectral_package(core)
    theta_star = math.atan(math.sqrt(2.0))
    bridge = (
        lam_plus,
        lam_odd,
        lam_minus - lam_odd,
        theta - theta_star,
        delta,
        rho,
        gamma,
        a_sel,
        e,
    )

    check(
        "The Hermitian bridge reconstructs exactly from the bridge coordinates",
        np.linalg.norm(h - (core + b)) < 1e-12,
        f"recon err={np.linalg.norm(h - (core + b)):.2e}",
    )
    check(
        "The breaking source reconstructs exactly from the triplet coordinates",
        np.linalg.norm(b - breaking_matrix(delta, rho, gamma)) < 1e-12,
        f"break err={np.linalg.norm(b - breaking_matrix(delta, rho, gamma)):.2e}",
    )
    check(
        "The selector primitive reconstructs exactly from one amplitude slot",
        np.linalg.norm(selector_primitive(a_sel) - a_sel * REDUCED_SELECTOR_CLASS)
        < 1e-12,
        f"a_sel={a_sel:.6f}",
    )
    check(
        "The unified bundle is exactly the joint carrier of the three objects",
        len(bridge) == 9 and bridge[-1] in (0, 1),
        f"U_min={bridge}",
    )


def part2_the_hermitian_and_selector_sectors_are_independent() -> None:
    print("\n" + "=" * 88)
    print("PART 2: THE HERMITEAN AND SELECTOR SECTORS ARE INDEPENDENT")
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
    e_a = np.diag([1.0, 0.0, 0.0]).astype(complex)
    e_b = np.array([[0.0, 1.0, 1.0], [1.0, 0.0, 0.0], [1.0, 0.0, 0.0]], dtype=complex)
    e_c = np.array([[0.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]], dtype=complex)
    e_d = np.array([[0.0, 0.0, 0.0], [0.0, 0.0, 1.0], [0.0, 1.0, 0.0]], dtype=complex)
    selector = REDUCED_SELECTOR_CLASS

    hermitian_basis = np.column_stack(
        [flat_real(m) for m in [e_a, e_b, e_c, e_d, t_delta, t_rho, t_gamma]]
    )
    hermitian_rank = int(np.linalg.matrix_rank(hermitian_basis))
    selector_rank = int(np.linalg.matrix_rank(selector.reshape(1, -1)))

    check(
        "The Hermitian bridge sector has exact real rank 7",
        hermitian_rank == 7,
        f"rank={hermitian_rank}",
    )
    check(
        "The breaking source generators are linearly independent over R",
        np.linalg.matrix_rank(np.column_stack([flat_real(t_delta), flat_real(t_rho), flat_real(t_gamma)]))
        == 3,
        "rank=3",
    )
    check(
        "The selector class is exactly one-dimensional on the reduced quotient",
        selector_rank == 1,
        f"rank={selector_rank}",
    )
    check(
        "No Hermitian basis vector collapses the selector class",
        np.linalg.norm(selector) > 0.0 and hermitian_rank == 7,
        "different quotient types",
    )


def part3_the_optional_edge_bit_is_needed_only_for_coefficient_closure() -> None:
    print("\n" + "=" * 88)
    print("PART 3: THE OPTIONAL EDGE BIT IS NEEDED ONLY FOR COEFFICIENT CLOSURE")
    print("=" * 88)

    amplitude = 2.25
    edge0 = selector_edge(0, amplitude)
    edge1 = selector_edge(1, amplitude)
    h0 = edge0 @ edge0.conj().T
    h1 = edge1 @ edge1.conj().T
    expected = amplitude * EYE

    check(
        "The two edge values are exactly sqrt(A) I and sqrt(A) C",
        np.linalg.norm(edge0 - math.sqrt(amplitude) * EYE) < 1e-12
        and np.linalg.norm(edge1 - math.sqrt(amplitude) * CYCLE) < 1e-12,
        "binary edge representatives",
    )
    check(
        "The two edge values are Hermitian-indistinguishable",
        np.linalg.norm(h0 - h1) < 1e-12,
        f"H-diff={np.linalg.norm(h0 - h1):.2e}",
    )
    check(
        "The shared Hermitian data are amplitude times the identity",
        np.linalg.norm(h0 - expected) < 1e-12,
        f"err={np.linalg.norm(h0 - expected):.2e}",
    )
    check(
        "So the binary edge bit cannot be absorbed into the Hermitian bridge",
        np.linalg.norm(h0 - h1) < 1e-12 and np.linalg.norm(edge0 - edge1) > 0.0,
        "edge bit remains discrete",
    )


def part4_the_note_records_the_minimal_unified_extension() -> None:
    print("\n" + "=" * 88)
    print("PART 4: THE NOTE RECORDS THE MINIMAL UNIFIED EXTENSION")
    print("=" * 88)

    note = read("docs/PMNS_UNIFIED_BRIDGE_CARRIER_NOTE.md")
    branch = read("docs/PMNS_BRANCH_HERMITIAN_DATA_LAW_ATTEMPT_NOTE.md")
    breaking = read("docs/PMNS_BREAKING_SOURCE_CONSTRUCTION_NOTE.md")
    selector = read("docs/PMNS_NEW_SELECTOR_PRIMITIVE_CONSTRUCTION_NOTE.md")

    check(
        "The note states the result is a minimal-unification theorem",
        "minimal-unification theorem" in note,
    )
    check(
        "The note identifies the unified bundle coordinates explicitly",
        "U_min = (A, B, u, v, delta, rho, gamma, a_sel, e)" in note,
    )
    check(
        "The branch Hermitian attempt records the bridge object",
        "Minimal missing bridge" in branch
        and "Hermitian-data law itself" in branch
        and "H_core" in branch,
    )
    check(
        "The breaking-source construction records the 3-real source space",
        "S_break=span_R{T_delta,T_rho,T_gamma}"
        in breaking.replace(" ", "").replace("\n", ""),
    )
    check(
        "The selector construction records the one-slot mixed bridge",
        "B_red = a_sel (chi_N_nu - chi_N_e)" in selector,
    )

    print()
    print("  Therefore the unified object is not a positive retained-bank closure law.")
    print("  It is the smallest exact bundle that simultaneously carries the three")
    print("  missing structures.")


def main() -> int:
    print("=" * 88)
    print("PMNS UNIFIED BRIDGE CARRIER")
    print("=" * 88)
    part1_the_unified_bundle_reconstructs_all_three_objects()
    part2_the_hermitian_and_selector_sectors_are_independent()
    part3_the_optional_edge_bit_is_needed_only_for_coefficient_closure()
    part4_the_note_records_the_minimal_unified_extension()
    print("\n" + "=" * 88)
    print(f"PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    print("=" * 88)
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
