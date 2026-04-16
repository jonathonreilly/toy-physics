#!/usr/bin/env python3
"""
DM neutrino positive-polar aligned-core no-go.

Question:
  Once the positive polar section makes the post-canonical DM bridge intrinsic
  from H = Y Y^dag, does the exact residual-Z_2 aligned Hermitian core already
  supply the needed CP support?

Answer:
  No.

  On the aligned active Hermitian core

      H_act =
      [ a  b  b ]
      [ b  c  d ]
      [ b  d  c ],

  the Z_3-basis singlet-doublet slot entries are exactly equal and real:

      (U_Z3^dag H_act U_Z3)_01 = (U_Z3^dag H_act U_Z3)_02 = (a+b-c-d)/3.

  After the current real Majorana doublet rotation, one physical singlet-
  doublet mass-basis entry vanishes and the other is purely real, so

      Im[(K_mass)01^2] = Im[(K_mass)02^2] = 0.

  Therefore the aligned Hermitian core is intrinsically CP-empty even on the
  positive polar section. The remaining DM blocker is now the Hermitian
  symmetry-breaking law away from that aligned core.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]

PASS_COUNT = 0
FAIL_COUNT = 0

PI = np.pi
OMEGA = np.exp(2j * PI / 3.0)
UZ3 = (1.0 / np.sqrt(3.0)) * np.array(
    [
        [1.0, 1.0, 1.0],
        [1.0, OMEGA, OMEGA * OMEGA],
        [1.0, OMEGA * OMEGA, OMEGA],
    ],
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


def aligned_core(a: float, b: float, c: float, d: float) -> np.ndarray:
    return np.array([[a, b, b], [b, c, d], [b, d, c]], dtype=complex)


def z3_kernel_from_h(h: np.ndarray) -> np.ndarray:
    return UZ3.conj().T @ h @ UZ3


def mass_basis_kernel_from_h(h: np.ndarray) -> np.ndarray:
    return R.T @ z3_kernel_from_h(h) @ R


def cp_pair_from_h(h: np.ndarray) -> tuple[float, float]:
    km = mass_basis_kernel_from_h(h)
    return float(np.imag(km[0, 1] ** 2)), float(np.imag(km[0, 2] ** 2))


def part1_exact_z3_slot_formula_on_the_aligned_core() -> None:
    print("\n" + "=" * 88)
    print("PART 1: THE ALIGNED CORE GIVES EQUAL REAL SINGLET-DOUBLET SLOTS")
    print("=" * 88)

    a, b, c, d = 1.7, 0.4, 1.2, 0.3
    h = aligned_core(a, b, c, d)
    kz = z3_kernel_from_h(h)
    q = (a + b - c - d) / 3.0
    expected = np.array(
        [
            [(a + 4.0 * b + 2.0 * c + 2.0 * d) / 3.0, q, q],
            [q, (a - 2.0 * b + 2.0 * c - d) / 3.0, (a - 2.0 * b - c + 2.0 * d) / 3.0],
            [q, (a - 2.0 * b - c + 2.0 * d) / 3.0, (a - 2.0 * b + 2.0 * c - d) / 3.0],
        ],
        dtype=complex,
    )

    check(
        "The Z_3 transform of the aligned core has the exact closed form",
        np.linalg.norm(kz - expected) < 1e-10,
        f"error = {np.linalg.norm(kz - expected):.2e}",
    )
    check(
        "The two singlet-doublet slot entries are equal",
        abs(kz[0, 1] - kz[0, 2]) < 1e-12,
        f"K01={kz[0,1]:.6f}, K02={kz[0,2]:.6f}",
    )
    check(
        "Those slot entries are purely real on the aligned core",
        abs(np.imag(kz[0, 1])) < 1e-12 and abs(np.imag(kz[0, 2])) < 1e-12,
        f"K01={kz[0,1]:.6f}, K02={kz[0,2]:.6f}",
    )

    print()
    print("  So the intrinsic positive-section slot pair collapses on the aligned")
    print("  core to one real repeated scalar q = (a+b-c-d)/3.")


def part2_the_physical_cp_tensor_vanishes_exactly() -> None:
    print("\n" + "=" * 88)
    print("PART 2: THE ALIGNED CORE IS INTRINSICALLY CP-EMPTY")
    print("=" * 88)

    a, b, c, d = 1.7, 0.4, 1.2, 0.3
    h = aligned_core(a, b, c, d)
    kz = z3_kernel_from_h(h)
    km = mass_basis_kernel_from_h(h)
    q = (a + b - c - d) / 3.0

    check(
        "One physical singlet-doublet mass-basis entry vanishes exactly",
        abs(km[0, 1]) < 1e-12,
        f"K01_mass={km[0,1]:.6f}",
    )
    check(
        "The other physical singlet-doublet mass-basis entry is exactly sqrt(2) q and real",
        abs(km[0, 2] - np.sqrt(2.0) * q) < 1e-12 and abs(np.imag(km[0, 2])) < 1e-12,
        f"K02_mass={km[0,2]:.6f}, sqrt(2)q={np.sqrt(2.0)*q:.6f}",
    )
    check(
        "Therefore the exact aligned-core CP tensor vanishes",
        abs(np.imag(km[0, 1] ** 2)) < 1e-12 and abs(np.imag(km[0, 2] ** 2)) < 1e-12,
        f"cp_pair={cp_pair_from_h(h)}",
    )

    print()
    print("  The positive polar section does not rescue the aligned Hermitian core.")
    print("  On that core the DM carrier remains structurally CP-empty.")


def part3_random_aligned_samples_stay_cp_empty() -> None:
    print("\n" + "=" * 88)
    print("PART 3: GENERIC POSITIVE-DEFINITE ALIGNED SAMPLES STAY CP-EMPTY")
    print("=" * 88)

    rng = np.random.default_rng(3)
    all_zero = True
    count = 0
    while count < 80:
        a = float(rng.uniform(1.0, 2.5))
        b = float(rng.uniform(-0.8, 0.8))
        c = float(rng.uniform(0.8, 2.2))
        d = float(rng.uniform(-0.8, 0.8))
        h = aligned_core(a, b, c, d)
        if np.min(np.linalg.eigvalsh(h)) <= 1e-6:
            continue
        cp1, cp2 = cp_pair_from_h(h)
        if abs(cp1) > 1e-10 or abs(cp2) > 1e-10:
            all_zero = False
            break
        count += 1

    check(
        "Random positive-definite aligned cores all give zero intrinsic CP",
        all_zero,
        f"tested = {count}",
    )

    print()
    print("  So the CP-emptiness is not a special point. It is the exact aligned-core law.")


def part4_bank_records_the_new_h_side_blocker() -> None:
    print("\n" + "=" * 88)
    print("PART 4: THE BANK RECORDS THE NEW H-SIDE BLOCKER")
    print("=" * 88)

    note = read("docs/DM_NEUTRINO_POLAR_ALIGNED_CORE_NO_GO_NOTE_2026-04-15.md")
    atlas = read("docs/publication/ci3_z3/DERIVATION_ATLAS.md")
    blocker = read("docs/DM_NEUTRINO_YUKAWA_BLOCKER_NOTE_2026-04-14.md")

    check(
        "The new note states K01 = K02 = (a+b-c-d)/3 on the aligned core",
        "(a+b-c-d)/3" in note or "(a + b - c - d) / 3" in note,
    )
    check(
        "The atlas carries the positive-polar aligned-core no-go row",
        "| DM neutrino positive-polar aligned-core no-go |" in atlas,
    )
    check(
        "The blocker note now points at Hermitian symmetry breaking away from the aligned core",
        "Hermitian-data side" in blocker
        or "breaking slots away from" in blocker
        or "aligned core" in blocker,
    )

    print()
    print("  The remaining last-mile DM object is now cleaner: not right-frame law,")
    print("  but the H-side symmetry-breaking law beyond the residual-Z2 aligned core.")


def main() -> int:
    print("=" * 88)
    print("DM NEUTRINO POSITIVE-POLAR ALIGNED-CORE NO-GO")
    print("=" * 88)
    print()
    print("Question:")
    print("  Does the exact residual-Z2 aligned Hermitian core already give the")
    print("  needed DM CP support once the positive polar section is used?")

    part1_exact_z3_slot_formula_on_the_aligned_core()
    part2_the_physical_cp_tensor_vanishes_exactly()
    part3_random_aligned_samples_stay_cp_empty()
    part4_bank_records_the_new_h_side_blocker()

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  Exact aligned-core answer:")
    print("    - the intrinsic positive-section slots collapse to one repeated real scalar")
    print("    - one physical singlet-doublet mass-basis entry vanishes")
    print("    - the other remains real")
    print("    - therefore the aligned core is intrinsically CP-empty")
    print()
    print("  So the right-frame blocker is gone, but DM still needs the Hermitian")
    print("  symmetry-breaking law away from the aligned core.")
    print()
    print(f"PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
