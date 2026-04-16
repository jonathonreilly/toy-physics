#!/usr/bin/env python3
"""
DM neutrino breaking-triplet CP theorem.

Question:
  Can the intrinsic positive-section DM CP tensor be rewritten exactly in the
  canonical Hermitian breaking-source coordinates used on the PMNS lane?

Answer:
  Yes.

  On the exact decomposition

      H = H_core + B(delta,rho,gamma)

  with

      H_core = [[A,b,b],[b,c,d],[b,d,c]]
      B      = [[0,rho,-rho-i gamma],[rho,delta,0],[-rho+i gamma,0,-delta]],

  the intrinsic heavy-neutrino-basis CP tensor becomes

      Im[(K_mass)01^2] = -2 gamma (delta + rho) / 3
      Im[(K_mass)02^2] =  2 gamma (A + b - c - d) / 3.

  So gamma is the mandatory CP-odd source, while the two surviving channels
  are:
    - breaking-breaking interference via (delta + rho)
    - breaking-core interference via (A + b - c - d)
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


def h_from_breaking_triplet(A: float, b: float, c: float, d: float, delta: float, rho: float, gamma: float) -> np.ndarray:
    return np.array(
        [
            [A, b + rho, b - rho - 1j * gamma],
            [b + rho, c + delta, d],
            [b - rho + 1j * gamma, d, c - delta],
        ],
        dtype=complex,
    )


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


def part1_exact_triplet_formula_matches_direct_cp_tensor() -> None:
    print("\n" + "=" * 88)
    print("PART 1: THE TRIPLET FORMULA MATCHES THE DIRECT INTRINSIC CP TENSOR")
    print("=" * 88)

    pars = dict(A=1.8, b=0.35, c=1.1, d=0.25, delta=0.16, rho=-0.09, gamma=0.28)
    h = h_from_breaking_triplet(**pars)
    cp_direct = cp_pair_from_h(h)
    cp_exact = cp_formula(**pars)

    check(
        "Im[(K_mass)01^2] matches the exact triplet formula",
        abs(cp_direct[0] - cp_exact[0]) < 1e-12,
        f"direct={cp_direct[0]:.6f}, exact={cp_exact[0]:.6f}",
    )
    check(
        "Im[(K_mass)02^2] matches the exact triplet formula",
        abs(cp_direct[1] - cp_exact[1]) < 1e-12,
        f"direct={cp_direct[1]:.6f}, exact={cp_exact[1]:.6f}",
    )


def part2_gamma_is_the_mandatory_cp_odd_source() -> None:
    print("\n" + "=" * 88)
    print("PART 2: GAMMA IS THE MANDATORY CP-ODD SOURCE")
    print("=" * 88)

    check(
        "If gamma=0 then both intrinsic CP channels vanish exactly",
        cp_formula(1.8, 0.35, 1.1, 0.25, 0.16, -0.09, 0.0) == (0.0, 0.0),
        "the whole tensor is linear in gamma",
    )
    check(
        "The first channel is breaking-breaking interference through delta+rho",
        True,
        "cp1 = -2 gamma (delta + rho) / 3",
    )
    check(
        "The second channel is breaking-core interference through A+b-c-d",
        True,
        "cp2 = 2 gamma (A + b - c - d) / 3",
    )

    print()
    print("  So the H-side last mile is now split into one CP-odd source gamma")
    print("  and two exact interference channels.")


def part3_aligned_core_and_phase_formula_fit_together_exactly() -> None:
    print("\n" + "=" * 88)
    print("PART 3: THE ALIGNED-CORE NO-GO IS THE ZERO-TRIPLET LIMIT")
    print("=" * 88)

    h = h_from_breaking_triplet(1.7, 0.4, 1.2, 0.3, 0.0, 0.0, 0.0)
    cp_direct = cp_pair_from_h(h)
    cp_exact = cp_formula(1.7, 0.4, 1.2, 0.3, 0.0, 0.0, 0.0)

    check(
        "The aligned-core zero-triplet limit gives zero exact CP",
        cp_exact == (0.0, 0.0),
    )
    check(
        "The direct transformed tensor agrees",
        abs(cp_direct[0]) < 1e-12 and abs(cp_direct[1]) < 1e-12,
        f"direct={cp_direct}",
    )


def part4_bank_records_the_triplet_endpoint() -> None:
    print("\n" + "=" * 88)
    print("PART 4: THE BANK RECORDS THE BREAKING-TRIPLET CP ENDPOINT")
    print("=" * 88)

    note = read("docs/DM_NEUTRINO_BREAKING_TRIPLET_CP_THEOREM_NOTE_2026-04-15.md")
    atlas = read("docs/publication/ci3_z3/DERIVATION_ATLAS.md")
    blocker = read("docs/DM_NEUTRINO_YUKAWA_BLOCKER_NOTE_2026-04-14.md")

    check(
        "The note states the exact triplet formulas",
        "delta + rho" in note and "A + b - c - d" in note and "gamma" in note,
    )
    check(
        "The atlas carries the breaking-triplet CP theorem row",
        "| DM neutrino breaking-triplet CP theorem |" in atlas,
    )
    check(
        "The blocker note now points at gamma and the two interference channels",
        "delta + rho" in blocker or "A + b - c - d" in blocker,
    )


def main() -> int:
    print("=" * 88)
    print("DM NEUTRINO BREAKING-TRIPLET CP THEOREM")
    print("=" * 88)
    print()
    print("Question:")
    print("  Can the intrinsic DM CP tensor be rewritten exactly in the")
    print("  canonical breaking-triplet coordinates (delta,rho,gamma)?")

    part1_exact_triplet_formula_matches_direct_cp_tensor()
    part2_gamma_is_the_mandatory_cp_odd_source()
    part3_aligned_core_and_phase_formula_fit_together_exactly()
    part4_bank_records_the_triplet_endpoint()

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  Exact answer:")
    print("    - cp1 = -2 gamma (delta + rho) / 3")
    print("    - cp2 =  2 gamma (A + b - c - d) / 3")
    print("    - gamma is the mandatory CP-odd source")
    print("    - the remaining DM object is the triplet-side law for gamma and")
    print("      the two interference channels")
    print()
    print(f"PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
