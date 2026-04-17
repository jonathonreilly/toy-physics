#!/usr/bin/env python3
"""
DM neutrino triplet character-source theorem.

Question:
  When the exact weak-only Z_3 source phase is transferred onto the canonical
  active neutrino branch, where does the nontrivial character enter the DM
  Hermitian carrier?

Answer:
  Uniquely through the CP-odd triplet slot gamma. Under character conjugation
  phi -> -phi, the odd Hermitian increment is exactly gamma * T_gamma, while
  the remaining triplet/core data are even.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]

PASS_COUNT = 0
FAIL_COUNT = 0

PI = np.pi
DELTA_SRC = 2.0 * PI / 3.0
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


def breaking_basis() -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    t_delta = np.array([[0.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, -1.0]], dtype=complex)
    t_rho = np.array([[0.0, 1.0, -1.0], [1.0, 0.0, 0.0], [-1.0, 0.0, 0.0]], dtype=complex)
    t_gamma = np.array([[0.0, 0.0, -1j], [0.0, 0.0, 0.0], [1j, 0.0, 0.0]], dtype=complex)
    return t_delta, t_rho, t_gamma


def part1_the_character_odd_increment_is_exactly_gamma_t_gamma() -> None:
    print("\n" + "=" * 88)
    print("PART 1: THE CHARACTER-ODD HERMITIAN INCREMENT IS EXACTLY GAMMA*T_GAMMA")
    print("=" * 88)

    x = np.array([1.18, 0.83, 0.97], dtype=float)
    y = np.array([0.37, 0.28, 0.51], dtype=float)
    hp = canonical_h(x, y, DELTA_SRC)
    hm = canonical_h(x, y, -DELTA_SRC)
    h_odd = 0.5 * (hp - hm)
    coords = hermitian_coords(hp)
    _, _, gamma = breaking_triplet_from_coords(*coords)
    _, _, t_gamma = breaking_basis()

    check(
        "The odd increment under phi -> -phi is exactly gamma*T_gamma",
        np.linalg.norm(h_odd - gamma * t_gamma) < 1e-12,
        f"odd err={np.linalg.norm(h_odd - gamma * t_gamma):.2e}",
    )
    check(
        "The exact weak Z3 source phase gives a nonzero gamma on a generic branch point",
        abs(gamma) > 1e-6 and abs(math.sin(DELTA_SRC) - math.sqrt(3.0) / 2.0) < 1e-12,
        f"gamma={gamma:.6f}",
    )


def part2_the_remaining_triplet_and_core_data_are_character_even() -> None:
    print("\n" + "=" * 88)
    print("PART 2: THE REMAINING TRIPLET AND CORE DATA ARE CHARACTER-EVEN")
    print("=" * 88)

    x = np.array([1.18, 0.83, 0.97], dtype=float)
    y = np.array([0.37, 0.28, 0.51], dtype=float)
    hp = canonical_h(x, y, DELTA_SRC)
    hm = canonical_h(x, y, -DELTA_SRC)
    h_even = 0.5 * (hp + hm)
    coords_p = hermitian_coords(hp)
    coords_m = hermitian_coords(hm)
    core_p = aligned_core_from_coords(*coords_p)
    core_m = aligned_core_from_coords(*coords_m)
    delta_p, rho_p, gamma_p = breaking_triplet_from_coords(*coords_p)
    delta_m, rho_m, gamma_m = breaking_triplet_from_coords(*coords_m)
    t_delta, t_rho, _ = breaking_basis()

    check(
        "The aligned Hermitian core is invariant under character conjugation",
        np.linalg.norm(core_p - core_m) < 1e-12,
        f"core diff={np.linalg.norm(core_p - core_m):.2e}",
    )
    check(
        "Delta and rho are even while gamma is odd under phi -> -phi",
        abs(delta_p - delta_m) < 1e-12
        and abs(rho_p - rho_m) < 1e-12
        and abs(gamma_p + gamma_m) < 1e-12,
        f"(delta,rho,gamma)+=({delta_p:.6f},{rho_p:.6f},{gamma_p:.6f})",
    )
    check(
        "The even increment is exactly delta*T_delta + rho*T_rho",
        np.linalg.norm(h_even - (core_p + delta_p * t_delta + rho_p * t_rho)) < 1e-12,
        f"even err={np.linalg.norm(h_even - (core_p + delta_p * t_delta + rho_p * t_rho)):.2e}",
    )


def part3_the_branch_records_gamma_as_the_unique_character_odd_transfer_slot() -> None:
    print("\n" + "=" * 88)
    print("PART 3: THE BRANCH RECORDS GAMMA AS THE UNIQUE CHARACTER-ODD SLOT")
    print("=" * 88)

    note = read("docs/DM_NEUTRINO_BREAKING_TRIPLET_CP_THEOREM_NOTE_2026-04-15.md")
    blocker = read("docs/DM_NEUTRINO_YUKAWA_BLOCKER_NOTE_2026-04-14.md")

    check(
        "The triplet CP note records gamma as the mandatory CP-odd source",
        "mandatory CP-odd source" in note and "`gamma`" in note,
    )
    check(
        "The blocker note carries the phase-fixed triplet-side object",
        "phi = 2 pi / 3" in blocker and "gamma" in blocker,
    )


def main() -> int:
    print("=" * 88)
    print("DM NEUTRINO TRIPLET CHARACTER-SOURCE THEOREM")
    print("=" * 88)

    part1_the_character_odd_increment_is_exactly_gamma_t_gamma()
    part2_the_remaining_triplet_and_core_data_are_character_even()
    part3_the_branch_records_gamma_as_the_unique_character_odd_transfer_slot()

    print("\n" + "=" * 88)
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    print("=" * 88)
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
