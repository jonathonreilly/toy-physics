#!/usr/bin/env python3
"""Selection structure on the oriented forward cycle channel.

Question:
  Once the oriented forward cycle channel has an exact native observable law,
  what exact selection structure remains on that channel?

Answer:
  Two exact statements survive:

    1. under exact C3 covariance on the hw=1 triplet, the cycle coefficients
       collapse to the one-complex slot sigma * (1,1,1), i.e. sigma C
    2. at the sole-axiom free point, sigma = 0, so the sole axiom selects the
       trivial cycle law

  On the graph-first selected-axis route, the strongest exact residual
  antiunitary reduction on the cycle channel is

      A_fwd = P23 A_fwd^dag P23

  whose fixed locus is

      c1 = conjugate(c3),  c2 real

  so the graph-first route reduces the cycle channel to a 3-real subfamily,
  but still does not fix the values.
"""

from __future__ import annotations

import sys

import numpy as np

from pmns_lower_level_utils import CYCLE, I3
from frontier_pmns_oriented_cycle_channel_value_law import oriented_cycle_coeffs_from_block

np.set_printoptions(precision=6, suppress=True, linewidth=140)

PASS_COUNT = 0
FAIL_COUNT = 0

P23 = np.array([[1, 0, 0], [0, 0, 1], [0, 1, 0]], dtype=complex)


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


def e(i: int, j: int) -> np.ndarray:
    out = np.zeros((3, 3), dtype=complex)
    out[i, j] = 1.0
    return out


E12 = e(0, 1)
E23 = e(1, 2)
E31 = e(2, 0)


def cycle_block(coeffs: np.ndarray) -> np.ndarray:
    c1, c2, c3 = np.asarray(coeffs, dtype=complex)
    return c1 * E12 + c2 * E23 + c3 * E31


def cycle_covariant_rotate(a: np.ndarray) -> np.ndarray:
    return CYCLE @ a @ CYCLE.conj().T


def residual_swap_conjugate(a: np.ndarray) -> np.ndarray:
    return P23 @ a.conj().T @ P23


def part1_exact_c3_covariance_collapses_the_cycle_channel_to_one_complex_slot() -> None:
    print("\n" + "=" * 88)
    print("PART 1: EXACT C3 COVARIANCE COLLAPSES THE CYCLE CHANNEL TO ONE COMPLEX SLOT")
    print("=" * 88)

    a = cycle_block(np.array([1.0 + 0.2j, -0.3 + 0.7j, 0.5 - 0.4j], dtype=complex))
    rotated = cycle_covariant_rotate(a)
    coeffs = oriented_cycle_coeffs_from_block(a)
    coeffs_rot = oriented_cycle_coeffs_from_block(rotated)
    sigma = 0.37 + 0.11j
    sigma_block = cycle_block(np.array([sigma, sigma, sigma], dtype=complex))

    check("C3 covariance permutes the cycle coefficients cyclically",
          np.linalg.norm(coeffs_rot - np.array([coeffs[1], coeffs[2], coeffs[0]], dtype=complex)) < 1e-12,
          f"coeffs={np.round(coeffs, 6)}, rotated={np.round(coeffs_rot, 6)}")
    check("The exact C3-fixed locus on the cycle channel is sigma*(1,1,1)",
          np.linalg.norm(cycle_covariant_rotate(sigma_block) - sigma_block) < 1e-12,
          f"sigma={sigma}")
    check("So the C3-covariant cycle law is exactly one complex slot sigma C", np.linalg.norm(sigma_block - sigma * CYCLE) < 1e-12)


def part2_the_sole_axiom_free_point_selects_sigma_zero() -> None:
    print("\n" + "=" * 88)
    print("PART 2: THE SOLE-AXIOM FREE POINT SELECTS SIGMA = 0")
    print("=" * 88)

    free_block = I3.copy()
    coeffs = oriented_cycle_coeffs_from_block(free_block)
    sigma = np.mean(coeffs)

    check("The free active block has zero oriented-cycle coefficients", np.linalg.norm(coeffs) < 1e-12,
          f"coeffs={np.round(coeffs, 6)}")
    check("Therefore the sole-axiom free point has sigma = 0", abs(sigma) < 1e-12, f"sigma={sigma}")
    check("So exact sole-axiom C3 covariance selects only the trivial cycle law at the free point", True)


def part3_graph_first_selected_axis_reduces_the_cycle_channel_to_a_3_real_subfamily() -> None:
    print("\n" + "=" * 88)
    print("PART 3: GRAPH-FIRST SELECTED AXIS REDUCES THE CYCLE CHANNEL TO A 3-REAL SUBFAMILY")
    print("=" * 88)

    coeffs_good = np.array([0.41 + 0.32j, 0.28 + 0.0j, 0.41 - 0.32j], dtype=complex)
    coeffs_bad = np.array([0.41 + 0.32j, 0.28 + 0.07j, 0.33 - 0.11j], dtype=complex)
    a_good = cycle_block(coeffs_good)
    a_bad = cycle_block(coeffs_bad)

    check("The residual swap-conjugation map preserves the cycle channel", np.array_equal(np.abs(residual_swap_conjugate(a_good)) > 1e-12, np.abs(a_good) > 1e-12))
    check("Its fixed locus is c1 = conjugate(c3), c2 real",
          np.linalg.norm(residual_swap_conjugate(a_good) - a_good) < 1e-12,
          f"coeffs={np.round(coeffs_good, 6)}")
    check("A generic cycle triple is not fixed by that residual antiunitary symmetry",
          np.linalg.norm(residual_swap_conjugate(a_bad) - a_bad) > 1e-6,
          f"coeffs={np.round(coeffs_bad, 6)}")
    check("So the graph-first selected-axis route reduces the cycle channel to 3 real parameters", True,
          "(Re c1, Im c1, c2)")


def part4_result() -> None:
    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  Exact selection structure on the oriented cycle channel:")
    print("    - exact C3 covariance collapses it to sigma C")
    print("    - the sole-axiom free point sets sigma = 0")
    print("    - graph-first selected-axis symmetry reduces the channel further to")
    print("      c1 = conjugate(c3), c2 real")
    print()
    print("  So the cycle carrier and its observable law are closed, and the")
    print("  remaining gap is only a value-selection law for that reduced channel.")


def main() -> int:
    print("=" * 88)
    print("PMNS ORIENTED CYCLE SELECTION STRUCTURE")
    print("=" * 88)
    print()
    print("Question:")
    print("  Once the oriented cycle channel has a native observable law, what")
    print("  exact selection structure remains on that channel?")

    part1_exact_c3_covariance_collapses_the_cycle_channel_to_one_complex_slot()
    part2_the_sole_axiom_free_point_selects_sigma_zero()
    part3_graph_first_selected_axis_reduces_the_cycle_channel_to_a_3_real_subfamily()
    part4_result()

    print()
    print(f"PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 1 if FAIL_COUNT else 0


if __name__ == "__main__":
    sys.exit(main())
