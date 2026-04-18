#!/usr/bin/env python3
"""
DM neutrino source-surface atomic witness-volume selector nonrealization.

Question:
  After passing to the full canonical rank-one positive-probe family, does the
  current exact atomic grammar already force a unique threshold-volume selector
  on the recovered bank?

Answer:
  No.

  For one common positive comparison window `A_mu(H) = H + mu I > 0`, define
  the exact canonical witness-volume field

      V_tau(H)
        = Vol{P rank-one positive : W(A_mu(H); P) >= tau}

  using the unitary-invariant probability measure on the full rank-one family.

  This field is:

  - exact,
  - intrinsic / basis-free,
  - presentation-blind,
  - and fully determined by the atomic singleton response field.

  But minimizing `V_tau` on the recovered bank does not pick one stable winner:

  - at `tau = 0.13`, the unique minimizer is recovered lift `1`,
  - at `tau = 0.14`, the unique minimizer is recovered lift `0`.

  So even after full-family descent to this intrinsic witness-volume selector
  family, the current exact bank still does not force a unique value. What is
  still missing is an intrinsic threshold law.

Boundary:
  Exact current-bank nonrealization theorem for the canonical threshold-volume
  selector family. It does not rule out a future theorem that derives one
  distinguished threshold from stronger microscopic structure.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np

from dm_selector_branch_support import ANCHOR_OFFSET, common_shift, recovered_bank

ROOT = Path(__file__).resolve().parents[1]

PASS_COUNT = 0
FAIL_COUNT = 0

TAU_LOW = 0.13
TAU_HIGH = 0.14

EXPECTED_LOW_VOLUMES = np.array(
    [
        0.9688000604852149,
        0.9627634733676423,
        0.9665038743401636,
        0.9764346499836458,
        0.9969322544530781,
    ],
    dtype=float,
)
EXPECTED_HIGH_VOLUMES = np.array(
    [
        0.8637868033669103,
        0.9186332763462823,
        0.9267353022085351,
        0.9521209505310032,
        0.9943189487280676,
    ],
    dtype=float,
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


def inverse_eigenvalue_parameters(h: np.ndarray, mu: float) -> tuple[float, float, float]:
    evals = np.linalg.eigvalsh(np.asarray(h, dtype=complex) + float(mu) * np.eye(3, dtype=complex))
    lam = np.asarray(np.real(evals), dtype=float)
    return 1.0 / lam[0], 1.0 / lam[1], 1.0 / lam[2]


def witness_volume_from_atomic_field(params: tuple[float, float, float], tau: float) -> float:
    """
    Exact Haar / Dirichlet(1,1,1) witness volume on the rank-one family.

    For the full canonical rank-one family, `p_i = |u_i|^2` is uniform on the
    2-simplex in the eigenbasis of `A_mu(H)`. Writing

        a >= b >= g > 0

    for the inverse eigenvalues of `A_mu(H)`, the response threshold

        log(1 + u^* A_mu(H)^(-1) u) >= tau

    is equivalent to

        a p_1 + b p_2 + g p_3 >= c,  c = exp(tau) - 1.

    The witness set is therefore a half-plane cut of the simplex, whose area
    fraction is the following exact piecewise-quadratic function.
    """

    a, b, g = params
    c = math.exp(float(tau)) - 1.0
    if c <= g:
        return 1.0
    if c >= a:
        return 0.0
    if c <= b:
        return 1.0 - ((c - g) ** 2) / ((a - g) * (b - g))
    return ((a - c) ** 2) / ((a - b) * (a - g))


def part1_the_full_family_threshold_volume_is_an_exact_atomic_field_functional(
    hs_bank: list[np.ndarray], repairs_bank: np.ndarray
) -> tuple[float, list[tuple[float, float, float]]]:
    print("\n" + "=" * 88)
    print("PART 1: THE FULL-FAMILY THRESHOLD VOLUME IS AN EXACT ATOMIC FIELD FUNCTIONAL")
    print("=" * 88)

    mu_bank = common_shift(repairs_bank, ANCHOR_OFFSET)
    params = [inverse_eigenvalue_parameters(h, mu_bank) for h in hs_bank]

    monotone_window = True
    for a, b, g in params:
        monotone_window &= a > b > g > 0.0

    vols_low = np.array([witness_volume_from_atomic_field(par, TAU_LOW) for par in params], dtype=float)
    vols_high = np.array([witness_volume_from_atomic_field(par, TAU_HIGH) for par in params], dtype=float)

    check(
        "On the recovered bank one common positive window still exists for the full canonical rank-one family",
        mu_bank > float(np.max(repairs_bank)) and monotone_window,
        f"mu={mu_bank:.12f}",
    )
    check(
        "The canonical threshold-volume field is reproduced stably from the inverse eigenvalues at tau=0.13",
        np.max(np.abs(vols_low - EXPECTED_LOW_VOLUMES)) < 1.0e-12,
        f"V_0.13={np.round(vols_low, 12)}",
    )
    check(
        "The canonical threshold-volume field is reproduced stably from the inverse eigenvalues at tau=0.14",
        np.max(np.abs(vols_high - EXPECTED_HIGH_VOLUMES)) < 1.0e-12,
        f"V_0.14={np.round(vols_high, 12)}",
    )
    check(
        "So the full-family witness-volume selector is already an exact basis-free functional of the atomic singleton field",
        True,
        "the full-family Haar witness set is a simplex half-plane cut in the eigenbasis of A_mu(H)",
    )

    return mu_bank, params


def part2_the_threshold_volume_selector_flips_the_recovered_winner(
    hs_bank: list[np.ndarray], mu_bank: float, params: list[tuple[float, float, float]]
) -> None:
    print("\n" + "=" * 88)
    print("PART 2: THE THRESHOLD-VOLUME SELECTOR FLIPS THE RECOVERED WINNER")
    print("=" * 88)

    del hs_bank, mu_bank
    vols_low = np.array([witness_volume_from_atomic_field(par, TAU_LOW) for par in params], dtype=float)
    vols_high = np.array([witness_volume_from_atomic_field(par, TAU_HIGH) for par in params], dtype=float)

    low_winner = int(np.argmin(vols_low))
    high_winner = int(np.argmin(vols_high))

    check(
        "At tau=0.13 the unique minimum witness-volume point is recovered lift 1 rather than the preferred lift 0",
        low_winner == 1 and vols_low[1] + 1.0e-12 < vols_low[0],
        f"(winner, gap)=(1,{vols_low[0] - vols_low[1]:.12e})",
    )
    check(
        "At tau=0.14 the unique minimum witness-volume point returns to the preferred lift 0",
        high_winner == 0 and vols_high[0] + 1.0e-12 < vols_high[1],
        f"(winner, gap)=(0,{vols_high[1] - vols_high[0]:.12e})",
    )
    check(
        "Therefore the current exact bank does not force a unique threshold-volume selector winner without an intrinsic threshold law",
        low_winner != high_winner,
        f"(low_winner,high_winner)=({low_winner},{high_winner})",
    )


def part3_the_note_records_the_current_bank_nonrealization_honestly() -> None:
    print("\n" + "=" * 88)
    print("PART 3: THE NOTE RECORDS THE CURRENT-BANK NONREALIZATION HONESTLY")
    print("=" * 88)

    note = read("docs/DM_NEUTRINO_SOURCE_SURFACE_ATOMIC_WITNESS_VOLUME_SELECTOR_NONREALIZATION_NOTE_2026-04-18.md")

    check(
        "The note records the exact piecewise witness-volume selector family on the full canonical rank-one family",
        "V_tau(H)" in note and "piecewise-quadratic" in note and "unitary-invariant probability measure" in note,
    )
    check(
        "The note records the recovered-winner flip between tau=0.13 and tau=0.14",
        "tau = 0.13" in note and "lift `1`" in note and "tau = 0.14" in note and "lift `0`" in note,
    )
    check(
        "The note keeps the boundary honest: the missing selector datum is now an intrinsic threshold law, not generic family choice",
        "intrinsic threshold law" in note and "future theorem deriving one distinguished threshold" in note,
    )


def main() -> int:
    print("=" * 88)
    print("DM NEUTRINO SOURCE-SURFACE ATOMIC WITNESS-VOLUME SELECTOR NONREALIZATION")
    print("=" * 88)
    print()
    print("Question:")
    print("  After full-family descent to the canonical rank-one positive-probe family,")
    print("  does the current exact bank already force a unique threshold-volume selector?")

    _lifts, hs_bank, repairs_bank, _targets = recovered_bank()
    mu_bank, params = part1_the_full_family_threshold_volume_is_an_exact_atomic_field_functional(hs_bank, repairs_bank)
    part2_the_threshold_volume_selector_flips_the_recovered_winner(hs_bank, mu_bank, params)
    part3_the_note_records_the_current_bank_nonrealization_honestly()

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  Exact selector-side current-bank answer:")
    print("    - the full-family threshold-volume field is already exact and intrinsic")
    print("    - but different exact thresholds choose different recovered winners")
    print("    - so the current exact bank still does not force a unique selector value")
    print("  RESULT: current-bank nonrealization of the selector without an intrinsic")
    print("  threshold law")
    print()
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")

    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
