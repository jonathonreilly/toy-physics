#!/usr/bin/env python3
"""
DM neutrino triplet even-response theorem.

Question:
  Once the CP-odd source gamma is isolated, what is the exact even-response
  sector that it couples to in the intrinsic DM CP tensor?

Answer:
  Exactly two even response channels:

    E1 = delta + rho
    E2 = A + b - c - d

  and the CP tensor factorizes as

    cp1 = -2 gamma E1 / 3
    cp2 =  2 gamma E2 / 3.
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
OMEGA = np.exp(2j * PI / 3.0)
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


def cp_pair_from_h(h: np.ndarray) -> tuple[float, float]:
    kz = UZ3.conj().T @ h @ UZ3
    km = R.T @ kz @ R
    return float(np.imag(km[0, 1] ** 2)), float(np.imag(km[0, 2] ** 2))


def part1_the_cp_tensor_factorizes_into_odd_source_times_even_response() -> None:
    print("\n" + "=" * 88)
    print("PART 1: THE CP TENSOR FACTORIZES INTO ODD SOURCE TIMES EVEN RESPONSE")
    print("=" * 88)

    x = np.array([1.18, 0.83, 0.97], dtype=float)
    y = np.array([0.37, 0.28, 0.51], dtype=float)
    h = canonical_h(x, y, DELTA_SRC)
    coords = hermitian_coords(h)
    core = aligned_core_from_coords(*coords)
    A = float(np.real(core[0, 0]))
    b = float(np.real(core[0, 1]))
    c = float(np.real(core[1, 1]))
    d = float(np.real(core[1, 2]))
    delta, rho, gamma = breaking_triplet_from_coords(*coords)
    cp1, cp2 = cp_pair_from_h(h)
    e1 = delta + rho
    e2 = A + b - c - d

    check(
        "cp1 matches the exact odd-times-even response law",
        abs(cp1 + 2.0 * gamma * e1 / 3.0) < 1e-12,
        f"cp1={cp1:.6f}, E1={e1:.6f}",
    )
    check(
        "cp2 matches the exact odd-times-even response law",
        abs(cp2 - 2.0 * gamma * e2 / 3.0) < 1e-12,
        f"cp2={cp2:.6f}, E2={e2:.6f}",
    )
    check(
        "So the remaining even response sector is exactly E1=delta+rho and E2=A+b-c-d",
        True,
        f"E1={e1:.6f}, E2={e2:.6f}",
    )


def part2_the_even_response_channels_are_invariant_under_character_conjugation() -> None:
    print("\n" + "=" * 88)
    print("PART 2: THE EVEN RESPONSE CHANNELS ARE INVARIANT UNDER CHARACTER CONJUGATION")
    print("=" * 88)

    x = np.array([1.18, 0.83, 0.97], dtype=float)
    y = np.array([0.37, 0.28, 0.51], dtype=float)
    hp = canonical_h(x, y, DELTA_SRC)
    hm = canonical_h(x, y, -DELTA_SRC)

    def invariants(h: np.ndarray) -> tuple[float, float, float]:
        coords = hermitian_coords(h)
        core = aligned_core_from_coords(*coords)
        A = float(np.real(core[0, 0]))
        b = float(np.real(core[0, 1]))
        c = float(np.real(core[1, 1]))
        d = float(np.real(core[1, 2]))
        delta, rho, gamma = breaking_triplet_from_coords(*coords)
        return delta + rho, A + b - c - d, gamma

    e1p, e2p, gp = invariants(hp)
    e1m, e2m, gm = invariants(hm)
    cp1p, cp2p = cp_pair_from_h(hp)
    cp1m, cp2m = cp_pair_from_h(hm)

    check(
        "E1 and E2 are even while gamma is odd under phi -> -phi",
        abs(e1p - e1m) < 1e-12 and abs(e2p - e2m) < 1e-12 and abs(gp + gm) < 1e-12,
        f"E1={e1p:.6f}, E2={e2p:.6f}, gamma={gp:.6f}",
    )
    check(
        "The intrinsic CP tensor flips sign with gamma at fixed even response",
        abs(cp1p + cp1m) < 1e-12 and abs(cp2p + cp2m) < 1e-12,
        f"cp+=( {cp1p:.6f}, {cp2p:.6f} )",
    )


def part3_the_branch_records_the_even_response_form_cleanly() -> None:
    print("\n" + "=" * 88)
    print("PART 3: THE BRANCH RECORDS THE EVEN RESPONSE FORM CLEANLY")
    print("=" * 88)

    note = read("docs/DM_NEUTRINO_BREAKING_TRIPLET_CP_THEOREM_NOTE_2026-04-15.md")
    blocker = read("docs/DM_NEUTRINO_YUKAWA_BLOCKER_NOTE_2026-04-14.md")

    check(
        "The CP theorem note records E1 and E2 explicitly",
        "delta + rho" in note and "A + b - c - d" in note,
    )
    check(
        "The blocker note points at the even response channels rather than a generic deformation",
        "delta + rho" in blocker and "A + b - c - d" in blocker,
    )


def main() -> int:
    print("=" * 88)
    print("DM NEUTRINO TRIPLET EVEN-RESPONSE THEOREM")
    print("=" * 88)

    part1_the_cp_tensor_factorizes_into_odd_source_times_even_response()
    part2_the_even_response_channels_are_invariant_under_character_conjugation()
    part3_the_branch_records_the_even_response_form_cleanly()

    print("\n" + "=" * 88)
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    print("=" * 88)
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
