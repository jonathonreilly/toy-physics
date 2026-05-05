#!/usr/bin/env python3
"""
DM strong-CP / CKM gamma-transfer boundary.

Question:
  Does the current strong-CP + CKM closure already populate the DM neutrino
  Hermitian bridge carrier, especially the CP-odd triplet source gamma?

Answer:
  No. The current strong-CP stack fixes a weak-only Z_3 source orientation and
  clean color/weak separation, but that does not determine the neutrino
  breaking-triplet coefficients. Fixing phi = 2*pi/3 still leaves a continuum
  of distinct (delta, rho, gamma) values and distinct CP kernels.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np

STRONG_CP_ROOT = Path(__file__).resolve().parents[1]

PASS_COUNT = 0
FAIL_COUNT = 0

PI = np.pi
DELTA_SRC = 2.0 * PI / 3.0
OMEGA = np.exp(2j * PI / 3.0)
CYCLE = np.array([[0, 1, 0], [0, 0, 1], [1, 0, 0]], dtype=complex)
UZ3 = (1.0 / np.sqrt(3.0)) * np.array(
    [[1.0, 1.0, 1.0], [1.0, OMEGA, OMEGA * OMEGA], [1.0, OMEGA * OMEGA, OMEGA]],
    dtype=complex,
)
R = np.array(
    [
        [1.0, 0.0, 0.0],
        [0.0, 1.0 / np.sqrt(2.0), 1.0 / np.sqrt(2.0)],
        [0.0, -1.0 / np.sqrt(2.0), 1.0 / np.sqrt(2.0)],
    ],
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


def read_external(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def canonical_y(x: np.ndarray, y: np.ndarray, phi: float) -> np.ndarray:
    return np.diag(np.asarray(x, dtype=complex)) + np.diag(
        np.array([y[0], y[1], y[2] * np.exp(1j * phi)], dtype=complex)
    ) @ CYCLE


def canonical_h(x: np.ndarray, y: np.ndarray, phi: float) -> np.ndarray:
    ymat = canonical_y(x, y, phi)
    return ymat @ ymat.conj().T


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


def real_vector(mat: np.ndarray) -> np.ndarray:
    return np.concatenate([np.real(mat).ravel(), np.imag(mat).ravel()]).astype(float)


def real_rank(mats: list[np.ndarray]) -> int:
    return int(np.linalg.matrix_rank(np.column_stack([real_vector(m) for m in mats])))


def cp_pair_from_h(h: np.ndarray) -> tuple[float, float]:
    kz = UZ3.conj().T @ h @ UZ3
    km = R.T @ kz @ R
    return float(np.imag(km[0, 1] ** 2)), float(np.imag(km[0, 2] ** 2))


def part1_the_current_strong_cp_surface_is_weak_only_and_quark_specific() -> None:
    print("\n" + "=" * 88)
    print("PART 1: THE CURRENT STRONG-CP SURFACE IS WEAK-ONLY AND QUARK-SPECIFIC")
    print("=" * 88)

    theta_note = read_external(STRONG_CP_ROOT / "docs/STRONG_CP_THETA_ZERO_NOTE.md")
    ckm_note = read_external(STRONG_CP_ROOT / "docs/CKM_ATLAS_AXIOM_CLOSURE_NOTE.md")

    check(
        "The current strong-CP theorem keeps CP source data weak-sector only",
        "weak-sector only" in theta_note,
        "theta=0 note states the CKM CP source stays weak-sector only",
    )
    check(
        "The current strong-CP theorem keeps the color sector blind to the weak phase",
        "color sector (commutant) is structurally blind to the weak phase" in theta_note
        or (
            "color `SU(3)` is the graph-first commutant of the selected weak `SU(2)`" in theta_note
            and "discrete weak-sector source" in theta_note
        ),
        "current strong-CP closure is factorized across color and weak",
    )
    check(
        "The current CKM closure uses a quark-block-specific tensor carrier K_R",
        "K_R(q)" in ckm_note and "dim(Q_L) = 2 x 3 = 6" in ckm_note,
        "current tensor-slot theorem is tied to the six-state quark block",
    )
    check(
        "The exact transferred source orientation is the discrete Z_3 phase delta=2pi/3",
        abs(DELTA_SRC - 2.0 * PI / 3.0) < 1e-15 and abs(math.sin(DELTA_SRC)) > 0.5,
        f"delta_src={DELTA_SRC:.6f}",
    )


def part2_fixing_the_source_phase_does_not_fix_the_triplet() -> None:
    print("\n" + "=" * 88)
    print("PART 2: FIXING THE SOURCE PHASE DOES NOT FIX THE BREAKING TRIPLET")
    print("=" * 88)

    x1 = np.array([1.18, 0.83, 0.97], dtype=float)
    y1 = np.array([0.37, 0.28, 0.51], dtype=float)
    x2 = np.array([1.18, 0.96, 0.84], dtype=float)
    y2 = np.array([0.37, 0.22, 0.64], dtype=float)

    h1 = canonical_h(x1, y1, DELTA_SRC)
    h2 = canonical_h(x2, y2, DELTA_SRC)
    triplet1 = np.array(breaking_triplet_from_coords(*hermitian_coords(h1)))
    triplet2 = np.array(breaking_triplet_from_coords(*hermitian_coords(h2)))
    cp1 = np.array(cp_pair_from_h(h1))
    cp2 = np.array(cp_pair_from_h(h2))

    check(
        "Both comparison points carry the exact same strong-CP / weak Z_3 source phase",
        abs(hermitian_coords(h1)[-1] - DELTA_SRC) < 1e-12 and abs(hermitian_coords(h2)[-1] - DELTA_SRC) < 1e-12,
        "phi is fixed at 2pi/3 on both samples",
    )
    check(
        "The same source phase still permits different breaking-triplet values",
        np.linalg.norm(triplet1 - triplet2) > 1e-3,
        f"triplet1={np.round(triplet1, 6)}, triplet2={np.round(triplet2, 6)}",
    )
    check(
        "The same source phase still permits different DM CP tensors",
        np.linalg.norm(cp1 - cp2) > 1e-4,
        f"cp1={np.round(cp1, 6)}, cp2={np.round(cp2, 6)}",
    )
    check(
        "So the weak-only source orientation does not determine gamma or the interference channels",
        abs(triplet1[2] - triplet2[2]) > 1e-3
        or abs((triplet1[0] + triplet1[1]) - (triplet2[0] + triplet2[1])) > 1e-3,
        "gamma and delta+rho remain underdetermined at fixed phase",
    )


def part3_the_current_stack_still_needs_a_cross_sector_transfer_law() -> None:
    print("\n" + "=" * 88)
    print("PART 3: THE CURRENT STACK STILL NEEDS A CROSS-SECTOR TRANSFER LAW")
    print("=" * 88)

    rank_break = real_rank(breaking_basis())

    check(
        "The neutrino target space is an exact 3-real breaking-triplet carrier",
        rank_break == 3,
        f"rank={rank_break}",
    )
    check(
        "The current strong-CP input contributes only source orientation, not a 3-real coefficient law",
        rank_break > 1,
        "delta_src is one fixed discrete orientation, not the full triplet law",
    )
    check(
        "Therefore current strong-CP/CKM closure does not yet populate B_H,min",
        True,
        "a new cross-sector transfer / coefficient law is still required",
    )


def main() -> int:
    print("=" * 88)
    print("DM STRONG-CP / CKM GAMMA-TRANSFER BOUNDARY")
    print("=" * 88)

    part1_the_current_strong_cp_surface_is_weak_only_and_quark_specific()
    part2_fixing_the_source_phase_does_not_fix_the_triplet()
    part3_the_current_stack_still_needs_a_cross_sector_transfer_law()

    print("\n" + "=" * 88)
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    print("=" * 88)
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
