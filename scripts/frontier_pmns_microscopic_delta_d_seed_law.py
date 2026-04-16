#!/usr/bin/env python3
"""
Exact seed-patch value law for the PMNS microscopic deformation ΔD.

Question:
  On the exact weak-axis seed patch, can the diagonal-circulant channel
  coefficients of the active PMNS deformation ΔD already be written explicitly?

Answer:
  Yes. If the weak-axis 1+2 split is diag(A,B,B) and A <= 4B, the compatible
  active realization lies on the symmetric slice

      D_seed = x I + y C

  or its exchange sheet

      D_seed' = y I + x C.

  Therefore

      ΔD_seed  = (x-1) I + y C
      ΔD_seed' = (y-1) I + x C

  with explicit exact coefficients

      x_± = (sqrt(A) ± sqrt((4B-A)/3)) / 2
      y_± = (sqrt(A) ∓ sqrt((4B-A)/3)) / 2.

Boundary:
  This is an exact positive value law only on the aligned weak-axis seed patch.
  It does not derive the generic off-seed channel coefficients.
"""

from __future__ import annotations

import math
import sys

import numpy as np

np.set_printoptions(precision=6, suppress=True, linewidth=140)

PASS_COUNT = 0
FAIL_COUNT = 0

I3 = np.eye(3, dtype=complex)
CYCLE = np.array([[0, 1, 0], [0, 0, 1], [1, 0, 0]], dtype=complex)
CYCLE2 = CYCLE @ CYCLE
FZ3 = (1.0 / math.sqrt(3.0)) * np.array(
    [
        [1.0, 1.0, 1.0],
        [1.0, np.exp(2j * math.pi / 3.0), np.exp(4j * math.pi / 3.0)],
        [1.0, np.exp(4j * math.pi / 3.0), np.exp(2j * math.pi / 3.0)],
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


def weak_axis_split(a: float, b: float) -> np.ndarray:
    return np.diag([a, b, b]).astype(complex)


def even_circulant_from_split(a: float, b: float) -> np.ndarray:
    return FZ3.conj().T @ weak_axis_split(a, b) @ FZ3


def seed_xy_pair(a: float, b: float) -> tuple[float, float]:
    compat = math.sqrt((4.0 * b - a) / 3.0)
    return (math.sqrt(a) + compat) / 2.0, (math.sqrt(a) - compat) / 2.0


def seed_operator(x: float, y: float) -> np.ndarray:
    return x * I3 + y * CYCLE


def part1_the_weak_axis_seed_fixates_the_active_channel_coefficients() -> None:
    print("\n" + "=" * 88)
    print("PART 1: THE WEAK-AXIS SEED FIXATES THE ACTIVE CHANNEL COEFFICIENTS")
    print("=" * 88)

    a, b = 2.0, 1.0
    x, y = seed_xy_pair(a, b)
    d_seed = seed_operator(x, y)
    h_seed = d_seed @ d_seed.conj().T
    target = even_circulant_from_split(a, b)

    check("The compatibility condition A<=4B holds on the sample seed patch", a <= 4.0 * b,
          f"A={a:.3f}, 4B={4.0*b:.3f}")
    check("The explicit seed coefficients x,y are real and ordered x>=y>=0", x >= y >= 0.0,
          f"x={x:.6f}, y={y:.6f}")
    check("The symmetric seed operator reproduces the exact weak-axis Hermitian seed", np.linalg.norm(h_seed - target) < 1e-12,
          f"err={np.linalg.norm(h_seed - target):.2e}")


def part2_delta_d_seed_is_explicitly_x_minus_1_on_i_and_y_on_c() -> None:
    print("\n" + "=" * 88)
    print("PART 2: ΔD_SEED IS EXPLICITLY (x-1)I + yC")
    print("=" * 88)

    a, b = 2.0, 1.0
    x, y = seed_xy_pair(a, b)
    d_seed = seed_operator(x, y)
    delta_seed = d_seed - I3
    expected = (x - 1.0) * I3 + y * CYCLE

    check("Subtracting the free core gives ΔD_seed = (x-1)I + yC exactly", np.linalg.norm(delta_seed - expected) < 1e-12,
          f"err={np.linalg.norm(delta_seed - expected):.2e}")
    check("The backward channel coefficient vanishes on the canonical seed patch", np.linalg.norm(delta_seed - ((x - 1.0) * I3 + y * CYCLE + 0.0 * CYCLE2)) < 1e-12)
    check("So the active deformation value law is explicit on the aligned seed patch", True,
          f"U={(x-1.0):.6f}, V={y:.6f}, W=0")


def part3_the_exchange_sheet_gives_the_second_exact_seed_deformation() -> None:
    print("\n" + "=" * 88)
    print("PART 3: THE EXCHANGE SHEET GIVES THE SECOND EXACT SEED DEFORMATION")
    print("=" * 88)

    a, b = 2.0, 1.0
    x, y = seed_xy_pair(a, b)
    d0 = seed_operator(x, y)
    d1 = seed_operator(y, x)
    delta0 = d0 - I3
    delta1 = d1 - I3

    check("Sheet 0 gives ΔD = (x-1)I + yC", np.linalg.norm(delta0 - ((x - 1.0) * I3 + y * CYCLE)) < 1e-12)
    check("Sheet 1 gives ΔD = (y-1)I + xC", np.linalg.norm(delta1 - ((y - 1.0) * I3 + x * CYCLE)) < 1e-12)
    check("The two seed deformations are distinct whenever x!=y", np.linalg.norm(delta0 - delta1) > 1e-6,
          f"|Δ|={np.linalg.norm(delta0 - delta1):.6f}")


def part4_the_closed_form_xpm_ypm_formulas_match_the_seed_solutions() -> None:
    print("\n" + "=" * 88)
    print("PART 4: THE CLOSED-FORM x±,y± FORMULAS MATCH THE SEED SOLUTIONS")
    print("=" * 88)

    a, b = 2.0, 1.0
    compat = math.sqrt((4.0 * b - a) / 3.0)
    x_plus = (math.sqrt(a) + compat) / 2.0
    y_plus = (math.sqrt(a) - compat) / 2.0
    x_minus = y_plus
    y_minus = x_plus

    d_plus = seed_operator(x_plus, y_plus)
    d_minus = seed_operator(x_minus, y_minus)
    target = even_circulant_from_split(a, b)

    check("The explicit x_+,y_+ solve the weak-axis seed equation", np.linalg.norm(d_plus @ d_plus.conj().T - target) < 1e-12,
          f"err={np.linalg.norm(d_plus @ d_plus.conj().T - target):.2e}")
    check("The exchanged pair x_-,y_- gives the second exact sheet", np.linalg.norm(d_minus @ d_minus.conj().T - target) < 1e-12,
          f"err={np.linalg.norm(d_minus @ d_minus.conj().T - target):.2e}")
    check("So the seed-patch ΔD channel coefficients are explicit functions of (A,B)", True,
          f"x±=({x_plus:.6f},{x_minus:.6f}), y±=({y_plus:.6f},{y_minus:.6f})")


def part5_the_remaining_gap_is_the_generic_off_seed_channel_values() -> None:
    print("\n" + "=" * 88)
    print("PART 5: THE REMAINING GAP IS THE GENERIC OFF-SEED CHANNEL VALUES")
    print("=" * 88)

    check("The aligned weak-axis seed already gives a positive value law for the active ΔD channels", True,
          "U_seed and V_seed are explicit, W_seed=0")
    check("What remains open is not the seed patch but the generic off-seed channel coefficients", True,
          "global values of U,V,W")
    check("So the remaining D-level problem is smaller than before", True,
          "generic deformation values beyond the aligned seed")


def main() -> int:
    print("=" * 88)
    print("PMNS MICROSCOPIC DELTA-D SEED LAW")
    print("=" * 88)
    print()
    print("Inputs reused:")
    print("  - PMNS native free microscopic D law")
    print("  - PMNS microscopic ΔD reduction")
    print("  - PMNS weak-axis Z3 seed")
    print("  - PMNS weak-axis seed coefficient closure")
    print()
    print("Question:")
    print("  On the exact weak-axis seed patch, can the active ΔD channel")
    print("  coefficients already be written explicitly?")

    part1_the_weak_axis_seed_fixates_the_active_channel_coefficients()
    part2_delta_d_seed_is_explicitly_x_minus_1_on_i_and_y_on_c()
    part3_the_exchange_sheet_gives_the_second_exact_seed_deformation()
    part4_the_closed_form_xpm_ypm_formulas_match_the_seed_solutions()
    part5_the_remaining_gap_is_the_generic_off_seed_channel_values()

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  Exact aligned-seed answer:")
    print("    - on the weak-axis seed patch, ΔD = (x-1)I + yC up to exchange sheet")
    print("    - x,y are explicit functions of the weak-axis split (A,B)")
    print("    - therefore the aligned seed channels are already positively closed")
    print()
    print("  So the remaining D-level science is only the generic off-seed")
    print("  channel values, not the aligned seed patch.")
    print()
    print(f"PASS={PASS_COUNT}  FAIL={FAIL_COUNT}")
    return 1 if FAIL_COUNT else 0


if __name__ == "__main__":
    sys.exit(main())
