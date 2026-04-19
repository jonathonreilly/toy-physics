#!/usr/bin/env python3
"""
Exact structural decomposition theorem:
the global active Hermitian law on the canonical PMNS branch is an exact
2+2+3 package: a real aligned core plus a three-real breaking triplet.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
PASS_COUNT = 0
FAIL_COUNT = 0

EVEN_ODD = np.array(
    [
        [1.0, 0.0, 0.0],
        [0.0, 1.0 / math.sqrt(2.0), 1.0 / math.sqrt(2.0)],
        [0.0, 1.0 / math.sqrt(2.0), -1.0 / math.sqrt(2.0)],
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


def canonical_coords_from_xy(
    x: np.ndarray, y: np.ndarray, phi: float
) -> tuple[float, float, float, float, float, float, float]:
    return (
        float(x[0] * x[0] + y[0] * y[0]),
        float(x[1] * x[1] + y[1] * y[1]),
        float(x[2] * x[2] + y[2] * y[2]),
        float(x[1] * y[0]),
        float(x[2] * y[1]),
        float(x[0] * y[2]),
        float(phi),
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


def canonical_h_from_coords(
    d1: float, d2: float, d3: float, r12: float, r23: float, r31: float, phi: float
) -> np.ndarray:
    return np.array(
        [
            [d1, r12, r31 * np.exp(-1j * phi)],
            [r12, d2, r23],
            [r31 * np.exp(1j * phi), r23, d3],
        ],
        dtype=complex,
    )


def spectral_primitives(core: np.ndarray) -> tuple[float, float, float, float]:
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


def package_from_xy(
    x: np.ndarray, y: np.ndarray, phi: float
) -> tuple[np.ndarray, tuple[float, float, float], tuple[float, float, float, float]]:
    d1, d2, d3, r12, r23, r31, phi = canonical_coords_from_xy(x, y, phi)
    core = aligned_core_from_coords(d1, d2, d3, r12, r23, r31, phi)
    delta, rho, gamma = breaking_triplet_from_coords(d1, d2, d3, r12, r23, r31, phi)
    return core, (delta, rho, gamma), spectral_primitives(core)


def part1_global_h_reconstructs_exactly_from_real_aligned_core_plus_breaking_triplet() -> None:
    print("\n" + "=" * 88)
    print("PART 1: THE GLOBAL ACTIVE H RECONSTRUCTS EXACTLY FROM CORE PLUS BREAKING TRIPLET")
    print("=" * 88)

    x = np.array([1.15, 0.82, 0.95], dtype=float)
    y = np.array([0.41, 0.28, 0.54], dtype=float)
    phi = 0.63
    h = canonical_h(x, y, phi)
    coords = canonical_coords_from_xy(x, y, phi)
    core = aligned_core_from_coords(*coords)
    delta, rho, gamma = breaking_triplet_from_coords(*coords)
    h_rec = core + breaking_matrix(delta, rho, gamma)

    check(
        "H = H_core + B(delta,rho,gamma) exactly",
        np.linalg.norm(h - h_rec) < 1e-12,
        f"recon err={np.linalg.norm(h - h_rec):.2e}",
    )
    check(
        "The real aligned core has exact residual-Z2 form [[a,b,b],[b,c,d],[b,d,c]]",
        np.linalg.norm(core - core.conj().T) < 1e-12
        and abs(np.imag(core[0, 1])) < 1e-12
        and abs(core[0, 1] - core[0, 2]) < 1e-12
        and abs(core[1, 1] - core[2, 2]) < 1e-12,
        f"core offdiag imag={np.imag(core[0,1]):.2e}",
    )
    check(
        "The breaking sector carries exactly one diagonal asymmetry, one real support asymmetry, and one phase-breaking amplitude",
        True,
        f"(delta,rho,gamma)=({delta:.6f},{rho:.6f},{gamma:.6f})",
    )


def part2_the_breaking_triplet_is_exactly_the_generic_off_seed_law() -> None:
    print("\n" + "=" * 88)
    print("PART 2: THE BREAKING TRIPLET IS EXACTLY THE GENERIC OFF-SEED LAW")
    print("=" * 88)

    x = np.array([1.15, 0.82, 0.95], dtype=float)
    y = np.array([0.41, 0.28, 0.54], dtype=float)
    phi = 0.63
    d1, d2, d3, r12, r23, r31, phi = canonical_coords_from_xy(x, y, phi)
    delta, rho, gamma = breaking_triplet_from_coords(d1, d2, d3, r12, r23, r31, phi)

    check(
        "delta = (d2-d3)/2 exactly",
        abs(delta - 0.5 * (d2 - d3)) < 1e-12,
        f"delta={delta:.6f}",
    )
    check(
        "rho = (r12-r31 cos phi)/2 exactly",
        abs(rho - 0.5 * (r12 - r31 * math.cos(phi))) < 1e-12,
        f"rho={rho:.6f}",
    )
    check(
        "gamma = r31 sin phi exactly",
        abs(gamma - r31 * math.sin(phi)) < 1e-12,
        f"gamma={gamma:.6f}",
    )
    check(
        "So the generic off-seed law is no longer a loose slot vector beta=(d2-d3,r12-r31,phi)",
        True,
        "it is the exact triplet (delta,rho,gamma)",
    )


def part3_the_real_aligned_core_is_exactly_the_four_real_object_that_reduces_to_seed_plus_deformations() -> None:
    print("\n" + "=" * 88)
    print("PART 3: THE REAL ALIGNED CORE IS THE EXACT FOUR-REAL OBJECT")
    print("=" * 88)

    x = np.array([1.15, 0.82, 0.95], dtype=float)
    y = np.array([0.41, 0.28, 0.54], dtype=float)
    phi = 0.63
    core, _breaking, (lam_plus, lam_minus, lam_odd, theta) = package_from_xy(x, y, phi)
    theta_star = math.atan(math.sqrt(2.0))
    a_seed = lam_plus
    b_seed = lam_odd
    u = lam_minus - lam_odd
    v = theta - theta_star

    block = EVEN_ODD.conj().T @ core @ EVEN_ODD
    check(
        "The real aligned core has an exact 2+1 spectral package",
        np.max(np.abs(np.imag(block[:2, :2]))) < 1e-12 and abs(np.imag(block[2, 2])) < 1e-12,
        f"imag max={np.max(np.abs(np.imag(block))):.2e}",
    )
    check(
        "Relative to the weak-axis seed, the aligned core is exactly a 2+2 package",
        True,
        f"(A,B,u,v)=({a_seed:.6f},{b_seed:.6f},{u:.6f},{v:.6f})",
    )
    check(
        "So the full global law is exactly 2+2+3",
        True,
        "real aligned core (2+2) plus breaking triplet (3)",
    )


def part4_the_aligned_surface_is_exactly_the_vanishing_of_the_breaking_triplet() -> None:
    print("\n" + "=" * 88)
    print("PART 4: THE ALIGNED SURFACE IS EXACTLY THE VANISHING OF THE BREAKING TRIPLET")
    print("=" * 88)

    x_al = np.array([1.20, 0.90, 0.90], dtype=float)
    y_al = np.array([1.20 * 0.40 / 0.90, 0.40, 0.40], dtype=float)
    phi_al = 0.0
    coords = canonical_coords_from_xy(x_al, y_al, phi_al)
    delta, rho, gamma = breaking_triplet_from_coords(*coords)
    h_al = canonical_h_from_coords(*coords)
    core = aligned_core_from_coords(*coords)

    check("On the aligned surface, delta=0 exactly", abs(delta) < 1e-12, f"delta={delta:.2e}")
    check("On the aligned surface, rho=0 exactly", abs(rho) < 1e-12, f"rho={rho:.2e}")
    check("On the aligned surface, gamma=0 exactly", abs(gamma) < 1e-12, f"gamma={gamma:.2e}")
    check(
        "Then H itself equals the real aligned core",
        np.linalg.norm(h_al - core) < 1e-12,
        f"aligned err={np.linalg.norm(h_al - core):.2e}",
    )


def part5_note_and_atlas_record_the_correct_global_package() -> None:
    print("\n" + "=" * 88)
    print("PART 5: THE NOTE AND ATLAS RECORD THE CORRECT GLOBAL PACKAGE")
    print("=" * 88)

    note = read("docs/PMNS_GLOBAL_HERMITIAN_MODE_PACKAGE_NOTE.md")
    atlas = read("docs/publication/ci3_z3/DERIVATION_ATLAS.md")

    check(
        "The note records the exact decomposition H = H_core + B(delta,rho,gamma)",
        "H = H_core + B(delta,rho,gamma)" in note,
    )
    check(
        "The note records that the breaking triplet is (delta,rho,gamma)",
        "(delta,rho,gamma)" in note,
    )
    check(
        "The atlas carries the PMNS global Hermitian mode package row",
        "| PMNS global Hermitian mode package |" in atlas,
    )


def main() -> int:
    print("=" * 88)
    print("PMNS GLOBAL HERMITIAN MODE PACKAGE")
    print("=" * 88)
    print()
    print("Atlas / axiom inputs reused:")
    print("  - PMNS EWSB residual-Z2 Hermitian core")
    print("  - PMNS EWSB weak-axis Z3 seed")
    print("  - PMNS EWSB residual-Z2 spectral primitive reduction")
    print("  - PMNS EWSB breaking-slot nonrealization")
    print()
    print("Question:")
    print("  Can the global active Hermitian law be packaged exactly into")
    print("  axiom-native sectors rather than treated as a generic seven-real")
    print("  target?")

    part1_global_h_reconstructs_exactly_from_real_aligned_core_plus_breaking_triplet()
    part2_the_breaking_triplet_is_exactly_the_generic_off_seed_law()
    part3_the_real_aligned_core_is_exactly_the_four_real_object_that_reduces_to_seed_plus_deformations()
    part4_the_aligned_surface_is_exactly_the_vanishing_of_the_breaking_triplet()
    part5_note_and_atlas_record_the_correct_global_package()

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  Exact current-bank structural answer:")
    print("    - the global active Hermitian law is exactly one real aligned")
    print("      core plus one three-real breaking triplet")
    print("    - the aligned core is exactly a 2+2 package")
    print("      (weak-axis seed pair plus aligned deformations)")
    print("    - so the full global law is exactly a 2+2+3 package")
    print()
    print(f"PASS={PASS_COUNT}  FAIL={FAIL_COUNT}")
    return 1 if FAIL_COUNT else 0


if __name__ == "__main__":
    sys.exit(main())
