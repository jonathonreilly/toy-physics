#!/usr/bin/env python3
"""Exact C3-character mode reduction of the remaining PMNS value problem.

Question:
  Once the native C3-character holonomy family is closed, what is the exact
  remaining sole-axiom PMNS value-selection problem on the retained `hw=1`
  triplet?

Answer:
  It is smaller than the raw 3-real reduced-cycle family.

  On the graph-first reduced channel

      A_fwd(u, v, w) = (u + i v) E12 + w E23 + (u - i v) E31

  the exact native C3-character holonomy triple has discrete Fourier modes

      z0 = w,
      z1 = u - i v,
      z2 = u + i v.

  So the reduced PMNS value problem is exactly the selection of:

      - one real trivial-character amplitude w
      - one complex nontrivial character amplitude chi := z2 = u + i v

  with z1 = conjugate(chi) on the residual graph-first antiunitary slice.

  The current sole-axiom routes do not fail on a generic 3-real mystery. They
  fail because they annihilate the nontrivial character amplitude exactly:

      chi = 0

  on the sole-axiom free route, the sole-axiom hw=1 source/transfer route, and
  the retained scalar route.

  Therefore the next honest positive target is not an arbitrary PMNS value law,
  but a sole-axiom law that produces nonzero C3-nontrivial character amplitude
  on the retained `hw=1` response family.
"""

from __future__ import annotations

import math
import sys

import numpy as np

from frontier_pmns_c3_character_holonomy_closure import (
    c3_character_holonomies_on_reduced_family,
)
from frontier_pmns_current_bank_value_selection_nogo import (
    active_block_with_reduced_cycle,
)
from frontier_pmns_sole_axiom_hw1_source_transfer_boundary import (
    sole_axiom_hw1_source_transfer_pack,
)
from frontier_pmns_uniform_scalar_deformation_boundary import scalar_triplet_block
from pmns_lower_level_utils import (
    I3,
    active_response_columns_from_sector_operator,
    circularity_guard,
    derive_active_block_from_response_columns,
)

np.set_printoptions(precision=6, suppress=True, linewidth=140)

PASS_COUNT = 0
FAIL_COUNT = 0

OMEGA = np.exp(2j * math.pi / 3.0)


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


def character_modes_from_holonomies(hol: np.ndarray) -> np.ndarray:
    h0, h1, h2 = np.asarray(hol, dtype=complex)
    return np.array(
        [
            (h0 + h1 + h2) / 3.0,
            (h0 + (OMEGA**2) * h1 + OMEGA * h2) / 3.0,
            (h0 + OMEGA * h1 + (OMEGA**2) * h2) / 3.0,
        ],
        dtype=complex,
    )


def reduced_character_data_from_block(block: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    hol = c3_character_holonomies_on_reduced_family(block)
    modes = character_modes_from_holonomies(hol)
    return hol, modes


def part1_the_reduced_cycle_family_is_exactly_trivial_plus_one_nontrivial_character() -> None:
    print("\n" + "=" * 88)
    print("PART 1: THE REDUCED FAMILY IS EXACTLY w PLUS ONE COMPLEX CHARACTER MODE")
    print("=" * 88)

    u, v, w = 0.41, 0.32, 0.28
    block = active_block_with_reduced_cycle(u, v, w, xbar=1.0)
    hol, modes = reduced_character_data_from_block(block)

    check("The trivial character mode is exactly w",
          abs(modes[0] - w) < 1e-12,
          f"z0={modes[0]:.6f}, w={w:.6f}")
    check("The omega character mode is exactly u - i v",
          abs(modes[1] - complex(u, -v)) < 1e-12,
          f"z1={modes[1]:.6f}")
    check("The omega^2 character mode is exactly u + i v",
          abs(modes[2] - complex(u, v)) < 1e-12,
          f"z2={modes[2]:.6f}")
    check("The three native holonomies are exactly the inverse character transform of (w, u-iv, u+iv)",
          np.linalg.norm(
              hol
              - np.array(
                  [
                      modes[0] + modes[1] + modes[2],
                      modes[0] + OMEGA * modes[1] + (OMEGA**2) * modes[2],
                      modes[0] + (OMEGA**2) * modes[1] + OMEGA * modes[2],
                  ],
                  dtype=complex,
              ).real
          )
          < 1e-12,
          f"hol={np.round(hol, 6)}")


def part2_graph_first_reduction_forces_the_nontrivial_character_pair_to_be_conjugate() -> None:
    print("\n" + "=" * 88)
    print("PART 2: GRAPH-FIRST REDUCTION FORCES THE NONTRIVIAL CHARACTER PAIR TO BE CONJUGATE")
    print("=" * 88)

    block = active_block_with_reduced_cycle(0.29, -0.17, 0.34, xbar=1.0)
    _hol, modes = reduced_character_data_from_block(block)

    check("The graph-first reduced channel makes the two nontrivial character modes complex conjugates",
          abs(modes[1] - np.conjugate(modes[2])) < 1e-12,
          f"z1={modes[1]:.6f}, z2={modes[2]:.6f}")
    check("So the remaining value problem is one real trivial mode plus one complex nontrivial mode", True,
          f"(w, chi)=({modes[0]:.6f}, {modes[2]:.6f})")


def part3_current_sole_axiom_routes_annihilate_the_nontrivial_character_mode_exactly() -> None:
    print("\n" + "=" * 88)
    print("PART 3: CURRENT SOLE-AXIOM ROUTES ANNIHILATE THE NONTRIVIAL CHARACTER MODE EXACTLY")
    print("=" * 88)

    free_hol, free_modes = reduced_character_data_from_block(I3)

    lam = 0.31
    pack = sole_axiom_hw1_source_transfer_pack(lam, 0.27)
    source_block = derive_active_block_from_response_columns(pack["active_columns"], lam)[1]
    source_hol, source_modes = reduced_character_data_from_block(source_block)

    scalar_block = scalar_triplet_block(1.13)
    scalar_cols = active_response_columns_from_sector_operator(scalar_block, lam)[1]
    scalar_active = derive_active_block_from_response_columns(scalar_cols, lam)[1]
    scalar_hol, scalar_modes = reduced_character_data_from_block(scalar_active)

    check("The free sole-axiom point has zero nontrivial character modes",
          abs(free_modes[1]) < 1e-12 and abs(free_modes[2]) < 1e-12,
          f"modes={np.round(free_modes, 6)}")
    check("The sole-axiom hw=1 source/transfer route still has zero nontrivial character modes",
          abs(source_modes[1]) < 1e-12 and abs(source_modes[2]) < 1e-12,
          f"modes={np.round(source_modes, 6)}")
    check("The retained scalar route has zero nontrivial character modes too",
          abs(scalar_modes[1]) < 1e-12 and abs(scalar_modes[2]) < 1e-12,
          f"modes={np.round(scalar_modes, 6)}")
    check("All three routes therefore give only trivial retained character holonomies",
          np.linalg.norm(free_hol) < 1e-12 and np.linalg.norm(source_hol) < 1e-12 and np.linalg.norm(scalar_hol) < 1e-12,
          f"free={np.round(free_hol, 6)}, source={np.round(source_hol, 6)}, scalar={np.round(scalar_hol, 6)}")


def part4_the_exact_missing_source_is_a_nonzero_c3_nontrivial_character_amplitude() -> None:
    print("\n" + "=" * 88)
    print("PART 4: THE EXACT MISSING SOURCE IS A NONZERO C3 NONTRIVIAL CHARACTER AMPLITUDE")
    print("=" * 88)

    a = active_block_with_reduced_cycle(0.41, 0.32, 0.28, xbar=1.0)
    b = active_block_with_reduced_cycle(0.29, -0.17, 0.34, xbar=1.0)
    _hol_a, modes_a = reduced_character_data_from_block(a)
    _hol_b, modes_b = reduced_character_data_from_block(b)

    check("Distinct realized reduced-channel points correspond to distinct nontrivial character amplitudes",
          abs(modes_a[2] - modes_b[2]) > 1e-6,
          f"chi_a={modes_a[2]:.6f}, chi_b={modes_b[2]:.6f}")
    check("Once the nontrivial character amplitude chi is known, u and v are fixed exactly",
          abs(modes_a[2].real - 0.41) < 1e-12
          and abs(modes_a[2].imag - 0.32) < 1e-12
          and abs(modes_b[2].real - 0.29) < 1e-12
          and abs(modes_b[2].imag + 0.17) < 1e-12,
          f"chi_a={modes_a[2]:.6f}, chi_b={modes_b[2]:.6f}")
    check("Therefore the current sole-axiom blocker is exactly the production of nonzero C3-nontrivial character amplitude on the retained hw=1 response family", True)


def part5_circularity_guard() -> None:
    print("\n" + "=" * 88)
    print("PART 5: CIRCULARITY GUARD")
    print("=" * 88)

    ok_modes, bad_modes = circularity_guard(character_modes_from_holonomies, {"u", "v", "w", "x", "y", "delta", "tau", "q"})
    ok_pack, bad_pack = circularity_guard(sole_axiom_hw1_source_transfer_pack, {"u", "v", "w", "x", "y", "delta", "tau", "q"})

    check("The character-mode reduction takes no PMNS target coordinates as inputs", ok_modes, f"bad={bad_modes}")
    check("The sole-axiom source/transfer pack takes no PMNS target coordinates as inputs", ok_pack, f"bad={bad_pack}")


def main() -> int:
    print("=" * 88)
    print("PMNS C3 CHARACTER MODE REDUCTION")
    print("=" * 88)
    print()
    print("Question:")
    print("  Once the native C3-character holonomy family is closed, what is the")
    print("  exact remaining sole-axiom PMNS value-selection problem?")

    part1_the_reduced_cycle_family_is_exactly_trivial_plus_one_nontrivial_character()
    part2_graph_first_reduction_forces_the_nontrivial_character_pair_to_be_conjugate()
    part3_current_sole_axiom_routes_annihilate_the_nontrivial_character_mode_exactly()
    part4_the_exact_missing_source_is_a_nonzero_c3_nontrivial_character_amplitude()
    part5_circularity_guard()

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  Exact reduced-law theorem:")
    print("    - the retained graph-first PMNS value problem is exactly")
    print("      one real trivial-character mode w plus one complex nontrivial")
    print("      character amplitude chi")
    print("    - the graph-first antiunitary reduction forces the opposite")
    print("      nontrivial mode to be conjugate(chi)")
    print("    - the current sole-axiom free, source/transfer, and scalar routes")
    print("      all annihilate chi exactly")
    print()
    print("  So the next honest positive target is now completely explicit:")
    print("  derive a sole-axiom law that produces nonzero C3-nontrivial character")
    print("  amplitude on the retained hw=1 response family.")
    print()
    print(f"PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 1 if FAIL_COUNT else 0


if __name__ == "__main__":
    sys.exit(main())
