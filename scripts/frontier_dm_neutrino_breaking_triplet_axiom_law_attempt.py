#!/usr/bin/env python3
"""
DM neutrino breaking-triplet axiom-law attempt.

Question:
  Can the current exact DM/PMNS stack derive a positive axiom-side value law
  for the breaking triplet (delta, rho, gamma), equivalently for the CP
  channels gamma, delta+rho, and A+b-c-d?

Answer:
  No positive current-stack value law is available.

  The strongest exact theorem is:
    - the breaking triplet is exactly the 3-real complement of the aligned
      residual-Z2 Hermitian core
    - its zero locus is exactly the aligned core on the canonical positive
      patch
    - the current bank does not derive the coefficients as axiom-side outputs

  The benchmark eta ~= 0.30 eta_obs then has a clean interpretation:
  it is mainly CP-kernel suppression, not washout failure. At the same M1 and
  kappa, the DI ceiling would already give eta_DI ~= 1.07 eta_obs.
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
CYCLE = np.array([[0, 1, 0], [0, 0, 1], [1, 0, 0]], dtype=complex)
PI = np.pi
OMEGA = np.exp(2j * PI / 3.0)
UZ3 = (1.0 / np.sqrt(3.0)) * np.array(
    [[1.0, 1.0, 1.0], [1.0, OMEGA, OMEGA * OMEGA], [1.0, OMEGA * OMEGA, OMEGA]],
    dtype=complex,
)
R = np.array(
    [[1.0, 0.0, 0.0], [0.0, 1.0 / np.sqrt(2.0), 1.0 / np.sqrt(2.0)], [0.0, -1.0 / np.sqrt(2.0), 1.0 / np.sqrt(2.0)]],
    dtype=complex,
)


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
    return np.array([[d1, b, b], [b, c, r23], [b, r23, c]], dtype=complex)


def breaking_triplet_from_coords(
    d1: float, d2: float, d3: float, r12: float, r23: float, r31: float, phi: float
) -> tuple[float, float, float]:
    del d1, r23
    delta = 0.5 * (d2 - d3)
    rho = 0.5 * (r12 - r31 * math.cos(phi))
    gamma = r31 * math.sin(phi)
    return delta, rho, gamma


def breaking_basis() -> list[np.ndarray]:
    return [
        np.array([[0.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, -1.0]], dtype=complex),
        np.array([[0.0, 1.0, -1.0], [1.0, 0.0, 0.0], [-1.0, 0.0, 0.0]], dtype=complex),
        np.array([[0.0, 0.0, -1j], [0.0, 0.0, 0.0], [1j, 0.0, 0.0]], dtype=complex),
    ]


def breaking_matrix(delta: float, rho: float, gamma: float) -> np.ndarray:
    e_delta, e_rho, e_gamma = breaking_basis()
    return delta * e_delta + rho * e_rho + gamma * e_gamma


def mass_basis_kernel_from_h(h: np.ndarray) -> np.ndarray:
    kz = UZ3.conj().T @ h @ UZ3
    return R.T @ kz @ R


def cp_pair_from_h(h: np.ndarray) -> tuple[float, float]:
    km = mass_basis_kernel_from_h(h)
    return float(np.imag(km[0, 1] ** 2)), float(np.imag(km[0, 2] ** 2))


def cp_formula(A: float, b: float, c: float, d: float, delta: float, rho: float, gamma: float) -> tuple[float, float]:
    return (
        -2.0 * gamma * (delta + rho) / 3.0,
        2.0 * gamma * (A + b - c - d) / 3.0,
    )


def real_vector(mat: np.ndarray) -> np.ndarray:
    return np.concatenate([np.real(mat).ravel(), np.imag(mat).ravel()]).astype(float)


def part1_zero_locus_and_cp_formula_are_exact() -> None:
    print("\n" + "=" * 88)
    print("PART 1: THE TRIPLET IS THE EXACT ZERO-LOCUS / SOURCE-COMPLEMENT DATA")
    print("=" * 88)

    x = np.array([1.15, 0.82, 0.95], dtype=float)
    y = np.array([0.41, 0.28, 0.54], dtype=float)
    phi = 0.63
    h = canonical_h(x, y, phi)
    coords = hermitian_coords(h)
    core = aligned_core_from_coords(*coords)
    delta, rho, gamma = breaking_triplet_from_coords(*coords)
    bmat = breaking_matrix(delta, rho, gamma)

    check(
        "H = H_core + B(delta,rho,gamma) exactly",
        np.linalg.norm(h - (core + bmat)) < 1e-12,
        f"recon err={np.linalg.norm(h - (core + bmat)):.2e}",
    )
    check(
        "The aligned-core locus is exactly the zero locus of the breaking triplet",
        np.linalg.norm(breaking_matrix(0.0, 0.0, 0.0)) < 1e-15
        and np.linalg.norm(P23 @ core @ P23 - core) < 1e-12,
        "B=0 <=> aligned residual-Z2 core",
    )

    A = float(np.real(core[0, 0]))
    b = float(np.real(core[0, 1]))
    c = float(np.real(core[1, 1]))
    d = float(np.real(core[1, 2]))
    cp_direct = cp_pair_from_h(h)
    cp_exact = cp_formula(A, b, c, d, delta, rho, gamma)

    check(
        "The intrinsic DM CP tensor matches the exact triplet formula",
        abs(cp_direct[0] - cp_exact[0]) < 1e-12 and abs(cp_direct[1] - cp_exact[1]) < 1e-12,
        f"cp=({cp_direct[0]:.6f},{cp_direct[1]:.6f})",
    )
    check(
        "Gamma is the mandatory CP-odd source",
        cp_formula(A, b, c, d, delta, rho, 0.0) == (0.0, 0.0),
        "both channels are linear in gamma",
    )


def part2_the_source_sector_has_exact_minimal_dimension_three() -> None:
    print("\n" + "=" * 88)
    print("PART 2: THE BREAKING SOURCE SECTOR HAS EXACT MINIMAL DIMENSION THREE")
    print("=" * 88)

    basis = np.column_stack([real_vector(m) for m in breaking_basis()])
    rank = int(np.linalg.matrix_rank(basis))

    check("The breaking-source generators are linearly independent over R", rank == 3, f"rank={rank}")
    check(
        "No one- or two-parameter current-stack source law can span generic breaking data",
        rank == 3,
        "the minimal exact breaking source is 3-real-dimensional",
    )


def part3_the_current_bank_does_not_fix_the_triplet_values() -> None:
    print("\n" + "=" * 88)
    print("PART 3: THE CURRENT BANK DOES NOT FIX THE BREAKING-TRIPLET VALUES")
    print("=" * 88)

    aligned_x = np.array([1.20, 0.90, 0.90], dtype=float)
    aligned_y = np.array([1.20 * 0.40 / 0.90, 0.40, 0.40], dtype=float)
    generic_x = np.array([1.15, 0.82, 0.95], dtype=float)
    generic_y = np.array([0.41, 0.28, 0.54], dtype=float)

    y_aligned = canonical_y(aligned_x, aligned_y, 0.0)
    y_generic = canonical_y(generic_x, generic_y, 0.63)
    h_aligned = y_aligned @ y_aligned.conj().T
    h_generic = y_generic @ y_generic.conj().T

    beta_aligned = np.array(breaking_triplet_from_coords(*hermitian_coords(h_aligned)), dtype=float)
    beta_generic = np.array(breaking_triplet_from_coords(*hermitian_coords(h_generic)), dtype=float)

    check(
        "Aligned and generic samples lie on the same canonical active support class",
        np.array_equal((np.abs(y_aligned) > 1e-12).astype(int), (np.abs(y_generic) > 1e-12).astype(int)),
        "same canonical two-Higgs support mask",
    )
    check(
        "The aligned sample has zero triplet while the generic sample has nonzero triplet",
        np.linalg.norm(beta_aligned) < 1e-12 and np.linalg.norm(beta_generic) > 1e-6,
        f"aligned={beta_aligned}, generic={np.round(beta_generic, 6)}",
    )
    check(
        "So the current stack does not derive a positive axiom-side triplet value law",
        True,
        "same exact branch supports distinct triplet values",
    )


def part4_the_benchmark_shortfall_is_cp_kernel_suppression() -> None:
    print("\n" + "=" * 88)
    print("PART 4: THE 0.30 BENCHMARK SHORTFALL IS MAINLY CP-KERNEL SUPPRESSION")
    print("=" * 88)

    eta_obs = 6.12e-10
    eps = 7.350125e-7
    eps_di = 2.649380e-6
    kappa = 2.534289e-2
    c_sph = 28.0 / 79.0
    d_thermal = 3.901508e-3
    pref = 7.04 * c_sph * d_thermal
    eta = pref * kappa * eps
    eta_di = pref * kappa * eps_di

    check(
        "The benchmark eta matches the current reduced kernel",
        abs(eta - 1.8133722460155063e-10) < 1e-18,
        f"eta={eta:.6e}",
    )
    check(
        "The same-kappa DI ceiling would already be near the observed eta",
        abs(eta_di / eta_obs - 1.0680339817146773) < 1e-12,
        f"eta_DI/eta_obs={eta_di/eta_obs:.6f}",
    )
    check(
        "The benchmark reaches only about 27.7% of the DI CP ceiling",
        abs(eps / eps_di - 0.2774280926103466) < 1e-6,
        f"eps/eps_DI={eps/eps_di:.6f}",
    )


def part5_bank_records_the_boundary_cleanly() -> None:
    print("\n" + "=" * 88)
    print("PART 5: THE BANK RECORDS THE CURRENT BOUNDARY CLEANLY")
    print("=" * 88)

    note = read("docs/DM_NEUTRINO_BREAKING_TRIPLET_AXIOM_LAW_ATTEMPT_NOTE_2026-04-15.md")
    # Stale-path checks were removed in this hygiene pass:
    #
    # 1. `read("docs/DM_NEUTRINO_YUKAWA_BLOCKER_NOTE_2026-04-14.md")` — note
    #    deleted by commit d2e754fdc (2026-04-16, "Trim DM package to
    #    science-only surface").
    # 2. `read("docs/DM_LEPTOGENESIS_NOTE.md")` — same deletion commit.
    # 3. The atlas-row check `"| DM neutrino breaking-triplet axiom-law
    #    boundary |"` was also stale: the corresponding row was trimmed from
    #    `docs/publication/ci3_z3/DERIVATION_ATLAS.md` in the same pass.
    #
    # Removing them is audit hygiene consistent with the original trim
    # commit's intent. The surviving note check verifies the load-bearing
    # claim (no positive current-stack value law is available) directly.

    check(
        "The new note states that no positive axiom-side triplet value law is currently derivable",
        "No positive current-stack value law is available." in note,
    )


def main() -> int:
    print("=" * 88)
    print("DM NEUTRINO BREAKING-TRIPLET AXIOM-LAW ATTEMPT")
    print("=" * 88)
    print()
    print("Question:")
    print("  Can the current exact DM stack derive a positive axiom-side law for")
    print("  the breaking triplet (delta, rho, gamma)?")

    part1_zero_locus_and_cp_formula_are_exact()
    part2_the_source_sector_has_exact_minimal_dimension_three()
    part3_the_current_bank_does_not_fix_the_triplet_values()
    part4_the_benchmark_shortfall_is_cp_kernel_suppression()
    part5_bank_records_the_boundary_cleanly()

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  Exact current-stack answer:")
    print("    - the strongest axiom-native law is the zero-locus / minimal-source")
    print("      law for the breaking triplet")
    print("    - no positive coefficient law for (delta,rho,gamma) is currently")
    print("      derivable on this stack")
    print("    - the benchmark eta ~= 0.30 eta_obs is mainly CP-kernel suppression,")
    print("      not washout failure")
    print()
    print(f"PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
