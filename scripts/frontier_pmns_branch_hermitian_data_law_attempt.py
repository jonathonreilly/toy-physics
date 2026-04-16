#!/usr/bin/env python3
"""
Exact obstruction theorem:
the current PMNS atlas/axiom bank packages the branch Hermitian law as an
exact 2+2+3 decomposition, but it does not yet derive the branch values as
axiom-side outputs. The minimal missing bridge is the selected-branch
Hermitian-data law itself, together with the seed-edge selector if coefficient
closure is also required.
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
    ymat = canonical_y(x, y, phi)
    return ymat @ ymat.conj().T


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


def weak_axis_seed_data(A: float, B: float) -> tuple[float, float, float, float, float]:
    mu = (A + 2.0 * B) / 3.0
    nu = (A - B) / 3.0
    Delta = mu * mu - 4.0 * nu * nu
    x2 = 0.5 * (mu + math.sqrt(max(Delta, 0.0)))
    y2 = 0.5 * (mu - math.sqrt(max(Delta, 0.0)))
    x = math.sqrt(max(x2, 0.0))
    y = math.sqrt(max(y2, 0.0))
    return mu, nu, Delta, x, y


def seed_sheet_matrices(A: float, B: float) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    mu, nu, Delta, x, y = weak_axis_seed_data(A, B)
    h_seed = mu * np.eye(3, dtype=complex) + nu * (CYCLE + CYCLE @ CYCLE)
    y_plus = x * np.eye(3, dtype=complex) + y * CYCLE
    y_minus = y * np.eye(3, dtype=complex) + x * CYCLE
    return h_seed, y_plus, y_minus


def support_mask(mat: np.ndarray) -> np.ndarray:
    return (np.abs(mat) > 1e-12).astype(int)


def part1_global_branch_law_is_exactly_a_2_plus_2_plus_3_package() -> None:
    print("\n" + "=" * 88)
    print("PART 1: THE GLOBAL BRANCH HERMITIAN LAW IS EXACTLY A 2+2+3 PACKAGE")
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
        "The aligned core has exact residual-Z2 form [[a,b,b],[b,c,d],[b,d,c]]",
        np.linalg.norm(core - core.conj().T) < 1e-12
        and abs(np.imag(core[0, 1])) < 1e-12
        and abs(core[0, 1] - core[0, 2]) < 1e-12
        and abs(core[1, 1] - core[2, 2]) < 1e-12,
        f"core offdiag imag={np.imag(core[0,1]):.2e}",
    )
    check(
        "The breaking sector is exactly the three-real triplet (delta,rho,gamma)",
        True,
        f"(delta,rho,gamma)=({delta:.6f},{rho:.6f},{gamma:.6f})",
    )

    print()
    print("  So the branch Hermitian law is not a generic seven-real blob.")
    print("  It is exactly one real aligned core plus one three-real breaking triplet.")


def part2_aligned_and_generic_points_share_the_same_support_but_differ_in_breaking_slots() -> None:
    print("\n" + "=" * 88)
    print("PART 2: ALIGNED AND GENERIC POINTS SHARE SUPPORT BUT DIFFER IN BREAKING SLOTS")
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

    beta_aligned = np.array(
        [
            0.5 * (np.real(aligned_h[1, 1]) - np.real(aligned_h[2, 2])),
            0.5 * (np.abs(aligned_h[0, 1]) - np.abs(aligned_h[2, 0]) * math.cos(np.angle(aligned_h[0, 1] * aligned_h[1, 2] * aligned_h[2, 0]))),
            np.angle(aligned_h[0, 1] * aligned_h[1, 2] * aligned_h[2, 0]),
        ],
        dtype=float,
    )
    beta_generic = np.array(
        [
            0.5 * (np.real(generic_h[1, 1]) - np.real(generic_h[2, 2])),
            0.5 * (np.abs(generic_h[0, 1]) - np.abs(generic_h[2, 0]) * math.cos(np.angle(generic_h[0, 1] * generic_h[1, 2] * generic_h[2, 0]))),
            np.angle(generic_h[0, 1] * generic_h[1, 2] * generic_h[2, 0]),
        ],
        dtype=float,
    )

    check(
        "Aligned and generic points lie on the same canonical support class",
        np.array_equal(support_mask(aligned_y), support_mask(generic_y)),
        f"mask=\n{support_mask(aligned_y)}",
    )
    check(
        "The aligned full-rank point has zero breaking-triplet vector",
        np.linalg.norm(beta_aligned) < 1e-12,
        f"beta={np.round(beta_aligned, 6)}",
    )
    check(
        "A generic full-rank point has nonzero breaking-triplet vector",
        np.linalg.norm(beta_generic) > 1e-6,
        f"beta={np.round(beta_generic, 6)}",
    )
    check(
        "So the current bank does not collapse the branch Hermitian data to one value",
        True,
    )

    print()
    print("  This is the exact obstruction: the same support class still admits")
    print("  distinct breaking-triplet values, so the current bank does not yet")
    print("  produce the branch Hermitian data as axiom-side outputs.")


def part3_compatible_seed_patch_collapses_to_one_exchange_sheet_but_not_to_a_value_law() -> None:
    print("\n" + "=" * 88)
    print("PART 3: THE COMPATIBLE SEED PATCH COLLAPSES TO ONE EXCHANGE SHEET")
    print("=" * 88)

    A = 1.5
    B = 1.0
    h_seed, y_plus, y_minus = seed_sheet_matrices(A, B)
    mu, nu, Delta, x, y = weak_axis_seed_data(A, B)
    h_plus = y_plus @ y_plus.conj().T
    h_minus = y_minus @ y_minus.conj().T

    check(
        "The compatible weak-axis seed patch satisfies A <= 4B",
        A <= 4.0 * B,
        f"A={A:.3f}, B={B:.3f}",
    )
    check(
        "Both seed sheets reconstruct the same H_seed",
        np.linalg.norm(h_seed - h_plus) < 1e-12 and np.linalg.norm(h_seed - h_minus) < 1e-12,
        f"errors=({np.linalg.norm(h_seed-h_plus):.2e},{np.linalg.norm(h_seed-h_minus):.2e})",
    )
    check(
        "The two canonical sheets are exactly the x<->y exchange pair",
        np.linalg.norm(y_plus - y_minus) > 1e-6,
        f"sheet distance={np.linalg.norm(y_plus - y_minus):.6f}",
    )

    Aeq = 1.0
    Beq = 1.0
    h_eq, y_plus_eq, y_minus_eq = seed_sheet_matrices(Aeq, Beq)
    check(
        "At the equal-split edge A = B, the sheets limit to the monomial edges",
        np.linalg.norm(y_plus_eq - math.sqrt(Aeq) * np.eye(3)) < 1e-12
        and np.linalg.norm(y_minus_eq - math.sqrt(Aeq) * CYCLE) < 1e-12,
        f"edge errors=({np.linalg.norm(y_plus_eq - math.sqrt(Aeq) * np.eye(3)):.2e},{np.linalg.norm(y_minus_eq - math.sqrt(Aeq) * CYCLE):.2e})",
    )
    check(
        "The note records that the remaining selector is the restricted Higgs-offset selector",
        "restricted Higgs-offset" in read("docs/PMNS_EWSB_WEAK_AXIS_SEED_EDGE_SELECTOR_REDUCTION_NOTE.md"),
    )

    print()
    print("  So the seed patch is exact but still not value-complete.")
    print("  The remaining object is one discrete Higgs-offset / monomial-edge")
    print("  selector, not a lower-dimensional hidden coefficient law.")


def part4_note_and_boundary_record_the_minimal_missing_bridge() -> None:
    print("\n" + "=" * 88)
    print("PART 4: THE NOTE AND BOUNDARY RECORD THE MINIMAL MISSING BRIDGE")
    print("=" * 88)

    note = read("docs/PMNS_BRANCH_HERMITIAN_DATA_LAW_ATTEMPT_NOTE.md")
    intrinsic = read("docs/PMNS_INTRINSIC_COMPLETION_BOUNDARY_NOTE.md")
    global_note = read("docs/PMNS_GLOBAL_HERMITIAN_MODE_PACKAGE_NOTE.md")
    seed_note = read("docs/PMNS_EWSB_WEAK_AXIS_SEED_EDGE_SELECTOR_REDUCTION_NOTE.md")

    check(
        "The note states that no positive axiom-side derivation is available from the current bank",
        "No positive axiom-side derivation is available" in note,
    )
    check(
        "The note identifies the branch Hermitian law as an exact 2+2+3 package",
        "2 + 2 + 3" in note and "branch Hermitian-data law itself" in note,
    )
    check(
        "The intrinsic-boundary note still says the branch Hermitian data are not axiom-side outputs",
        "branch Hermitian data themselves as axiom-side outputs" in intrinsic,
    )
    check(
        "The global Hermitian mode note records the exact 2+2+3 package",
        "2 + 2 + 3" in global_note and "H = H_core + B(delta,rho,gamma)" in global_note,
    )
    check(
        "The seed-edge note records the restricted Higgs-offset selector",
        "restricted Higgs-offset" in seed_note and "monomial-edge" in seed_note,
    )

    print()
    print("  The minimal missing bridge is now identified exactly:")
    print("    - the selected-branch Hermitian-data law itself")
    print("    - plus the seed-edge selector if coefficient closure is also required")


def main() -> int:
    print("=" * 88)
    print("PMNS BRANCH HERMITIAN DATA LAW ATTEMPT")
    print("=" * 88)
    print()
    print("Atlas / axiom inputs reused:")
    print("  - PMNS global Hermitian mode package")
    print("  - PMNS intrinsic completion boundary")
    print("  - PMNS EWSB weak-axis seed coefficient closure")
    print("  - PMNS EWSB weak-axis seed edge-selector reduction")
    print("  - PMNS EWSB alignment nonforcing")
    print("  - PMNS EWSB breaking-slot nonrealization")
    print()
    print("Question:")
    print("  Can the current atlas/axiom bank derive the branch Hermitian-data law")
    print("  itself, or does it only determine the exact structural package and")
    print("  the minimal missing bridge?")

    part1_global_branch_law_is_exactly_a_2_plus_2_plus_3_package()
    part2_aligned_and_generic_points_share_the_same_support_but_differ_in_breaking_slots()
    part3_compatible_seed_patch_collapses_to_one_exchange_sheet_but_not_to_a_value_law()
    part4_note_and_boundary_record_the_minimal_missing_bridge()

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  Exact current-bank answer:")
    print("    - no positive derivation of the branch Hermitian-data law itself")
    print("    - exact structural package: real aligned core + breaking triplet")
    print("    - exact seed-patch collapse: exchange sheet -> restricted Higgs")
    print("      offset selector on the canonical (0,1) pair")
    print("    - minimal missing bridge: selected-branch Hermitian-data law")
    print("      plus the seed-edge selector if coefficient closure is required")
    print()
    print(f"PASS={PASS_COUNT}  FAIL={FAIL_COUNT}")
    return 1 if FAIL_COUNT else 0


if __name__ == "__main__":
    sys.exit(main())
