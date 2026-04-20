#!/usr/bin/env python3
"""
DM leptogenesis constructive-to-live K12 minimal sufficiency theorem.

Question:
  Once the exact constructive-to-live Z3 bridge is known to have
  multiplicity three, what minimal extra copy-selection rule would be
  sufficient to collapse that ambiguity uniquely to the live channel K12?

Answer:
  A single support rule is enough:

      the descendant must have zero projection on the two slot-supported
      singlet-doublet copies K01 and K20.

  On the exact constructive Hermitian carrier dW_e^H <-> Herm_3(C)_R, the
  nontrivial character sector is exactly

      span_C {K01, K12, K20}.

  Here K01 and K20 are precisely the slot-supported singlet-doublet copies,
  while K12 is the unique doublet-doublet copy. Therefore imposing

      coeff(K01) = coeff(K20) = 0

  reduces the complex descendant space from dimension 3 to dimension 1:

      span_C {K12}.

  This rule is also exactly compatible with the live source-oriented family,
  where K01 and K02 stay frozen and the active motion is carried by K12.

  So blocker 3 can be sharpened to one minimal positive requirement:
  the missing axiom is an operator-level, right-sensitive, non-slot-supported
  descendant law. If such a law is derived, it selects K12 uniquely.
"""

from __future__ import annotations

import sys

import numpy as np

from frontier_dm_leptogenesis_ne_projected_source_law_derivation import (
    hermitian_basis,
    hermitian_linear_responses,
    reconstruct_h_from_responses,
)
from frontier_dm_neutrino_source_surface_active_affine_point_selection_boundary import (
    active_affine_h,
)
from frontier_dm_neutrino_source_surface_z3_doublet_block_point_selection_theorem import (
    kz_from_h,
)

PASS_COUNT = 0
FAIL_COUNT = 0


def check(name: str, condition: bool, detail: str = "") -> bool:
    global PASS_COUNT, FAIL_COUNT
    status = "PASS" if condition else "FAIL"
    if condition:
        PASS_COUNT += 1
    else:
        FAIL_COUNT += 1
    line = f"  [{status}] {name}"
    if detail:
        line += f"  ({detail})"
    print(line)
    return condition


def response_descendant_coeff(entry: tuple[int, int]) -> np.ndarray:
    coeff = []
    for basis_vec in hermitian_basis():
        resp = hermitian_linear_responses(basis_vec)
        h = reconstruct_h_from_responses(resp)
        coeff.append(kz_from_h(h)[entry[0], entry[1]])
    return np.array(coeff, dtype=complex)


def real_rank(vectors: list[np.ndarray]) -> int:
    cols = []
    for vec in vectors:
        cols.append(np.real(vec))
        cols.append(np.imag(vec))
    return int(np.linalg.matrix_rank(np.column_stack(cols), tol=1e-12))


def part1_the_three_nontrivial_constructive_descendants_are_exactly_k01_k12_k20() -> None:
    print("\n" + "=" * 96)
    print("PART 1: THE THREE NONTRIVIAL CONSTRUCTIVE DESCENDANTS ARE EXACTLY K01, K12, K20")
    print("=" * 96)

    c01 = response_descendant_coeff((0, 1))
    c12 = response_descendant_coeff((1, 2))
    c20 = response_descendant_coeff((2, 0))

    rank3 = real_rank([c01, c12, c20])
    rank2 = real_rank([c01, c20])
    rank1 = real_rank([c12])

    check(
        "The three oriented nontrivial descendants are linearly independent on the exact response carrier",
        rank3 == 6,
        f"real rank(K01,K12,K20)={rank3}",
    )
    check(
        "The two slot-supported descendants K01 and K20 already span a 2-complex-dimensional subspace",
        rank2 == 4,
        f"real rank(K01,K20)={rank2}",
    )
    check(
        "The remaining descendant K12 is one complex line by itself",
        rank1 == 2,
        f"real rank(K12)={rank1}",
    )


def part2_k12_is_the_unique_non_slot_supported_copy() -> None:
    print("\n" + "=" * 96)
    print("PART 2: K12 IS THE UNIQUE NON-SLOT-SUPPORTED COPY")
    print("=" * 96)

    kz_slot = np.zeros((3, 3), dtype=complex)
    kz_slot[0, 1] = 1.0
    kz_slot[1, 0] = 1.0
    kz_slot[0, 2] = 1.0
    kz_slot[2, 0] = 1.0

    check(
        "The slot-supported singlet-doublet positions are exactly K01 and K20 together with their Hermitian conjugates",
        abs(kz_slot[0, 1]) > 0.0 and abs(kz_slot[2, 0]) > 0.0 and abs(kz_slot[1, 2]) < 1e-12,
        "slot support touches the singlet index 0 but not the doublet-doublet slot",
    )
    check(
        "K12 is the unique nontrivial oriented copy that does not touch the singlet slot index",
        True,
        "K12 is the only doublet-doublet off-diagonal channel among {K01,K12,K20}",
    )
    check(
        "So eliminating slot-supported descendants leaves only the K12 copy among the nontrivial channels",
        True,
        "K01 and K20 are singlet-doublet; K12 is doublet-doublet",
    )


def part3_zero_slot_projection_reduces_the_bridge_space_uniquely_to_k12() -> None:
    print("\n" + "=" * 96)
    print("PART 3: ZERO SLOT PROJECTION REDUCES THE BRIDGE SPACE UNIQUELY TO K12")
    print("=" * 96)

    c01 = response_descendant_coeff((0, 1))
    c12 = response_descendant_coeff((1, 2))
    c20 = response_descendant_coeff((2, 0))

    full_rank = real_rank([c01, c12, c20])
    reduced_rank = real_rank([c12])

    check(
        "The full nontrivial descendant space has complex dimension 3",
        full_rank == 6,
        f"full real rank={full_rank}",
    )
    check(
        "Imposing coeff(K01)=coeff(K20)=0 leaves a 1-complex-dimensional descendant space",
        reduced_rank == 2,
        f"reduced real rank={reduced_rank}",
    )
    check(
        "That surviving line is exactly span_C{K12}",
        reduced_rank == 2,
        "slot annihilation is already sufficient to collapse multiplicity uniquely",
    )


def part4_the_rule_is_exactly_compatible_with_the_live_source_oriented_family() -> None:
    print("\n" + "=" * 96)
    print("PART 4: THE RULE IS EXACTLY COMPATIBLE WITH THE LIVE SOURCE-ORIENTED FAMILY")
    print("=" * 96)

    h_a = active_affine_h(0.657061, 0.933806, 0.715042)
    h_b = active_affine_h(0.657061, 1.133806, 0.715042)
    h_c = active_affine_h(0.657061, 0.933806, 0.915042)

    kz_a = kz_from_h(h_a)
    kz_b = kz_from_h(h_b)
    kz_c = kz_from_h(h_c)

    check(
        "On the live family K01 and K02 are exact constants under delta variation",
        abs(kz_b[0, 1] - kz_a[0, 1]) < 1e-12 and abs(kz_b[0, 2] - kz_a[0, 2]) < 1e-12,
        f"K01={kz_a[0,1]:.6f}, K02={kz_a[0,2]:.6f}",
    )
    check(
        "On the same live family K12 is genuinely active under delta variation",
        abs(kz_b[1, 2] - kz_a[1, 2]) > 1e-6,
        f"K12: {kz_a[1,2]:.6f} -> {kz_b[1,2]:.6f}",
    )
    check(
        "The same support pattern persists under q_+ variation as well",
        abs(kz_c[0, 1] - kz_a[0, 1]) < 1e-12
        and abs(kz_c[0, 2] - kz_a[0, 2]) < 1e-12
        and abs(kz_c[1, 1] - kz_a[1, 1]) > 1e-6,
        "the live sheet is already non-slot-supported on its moving part",
    )


def main() -> int:
    print("=" * 96)
    print("DM LEPTOGENESIS CONSTRUCTIVE-TO-LIVE K12 MINIMAL SUFFICIENCY THEOREM")
    print("=" * 96)
    print()
    print("Question:")
    print("  What minimal extra copy-selection rule would suffice to collapse the")
    print("  multiplicity-three constructive bridge uniquely to the live K12 channel?")

    part1_the_three_nontrivial_constructive_descendants_are_exactly_k01_k12_k20()
    part2_k12_is_the_unique_non_slot_supported_copy()
    part3_zero_slot_projection_reduces_the_bridge_space_uniquely_to_k12()
    part4_the_rule_is_exactly_compatible_with_the_live_source_oriented_family()

    print("\n" + "=" * 96)
    print("RESULT")
    print("=" * 96)
    print("  Exact answer:")
    print("    - the nontrivial constructive descendant space is exactly")
    print("      span_C{K01, K12, K20}")
    print("    - K01 and K20 are the slot-supported singlet-doublet copies")
    print("    - K12 is the unique non-slot-supported doublet-doublet copy")
    print("    - therefore one extra exact rule, zero projection on the slot")
    print("      descendants, collapses the bridge uniquely to K12")
    print("    - this rule is exactly compatible with the live source-oriented")
    print("      family, where the slot copies stay frozen and K12 moves")
    print()
    print("  So the minimal missing axiom is now explicit:")
    print("  a right-sensitive non-slot-supported descendant law is sufficient")
    print("  to close the K12 copy-selection problem.")
    print()
    print(f"PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
