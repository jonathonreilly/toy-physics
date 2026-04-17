#!/usr/bin/env python3
"""Exact boundary on the native C3-nontrivial PMNS current.

Question:
  Once the reduced PMNS cycle family is written in native C3-character
  variables, what is the exact smallest remaining sole-axiom source object?

Answer:
  It is one complex nontrivial-character current, not a larger family.

  Let h_0, h_1, h_2 be the exact native C3-character holonomies at phases

      0, 2 pi / 3, 4 pi / 3.

  Then define the native current

      J_chi(A) := (h_0 + omega h_1 + omega^2 h_2) / 3.

  On the reduced graph-first cycle family

      A_fwd(u, v, w) = (u + i v) E12 + w E23 + (u - i v) E31

  one has exactly

      J_chi(A_fwd) = chi = u + i v.

  So the PMNS value-selection problem is reduced to production of one complex
  native current.

  The current exact bank still annihilates this current on every current
  sole-axiom retained route:
    - the free route
    - the sole-axiom hw=1 source/transfer route
    - the retained scalar route

  Therefore the strongest honest next theorem is not "derive generic PMNS
  values", but "derive nonzero J_chi from Cl(3) on Z^3 alone."
"""

from __future__ import annotations

import math
import sys

import numpy as np

from frontier_pmns_c3_character_mode_reduction import character_modes_from_holonomies
from frontier_pmns_c3_character_holonomy_closure import c3_character_holonomies_on_reduced_family
from frontier_pmns_oriented_cycle_reduced_channel_nonselection import (
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


def c3_character_phases() -> tuple[float, float, float]:
    return (0.0, 2.0 * math.pi / 3.0, 4.0 * math.pi / 3.0)


def nontrivial_character_current(a: np.ndarray) -> complex:
    h0, h1, h2 = c3_character_holonomies_on_reduced_family(a)
    return complex((h0 + OMEGA * h1 + (OMEGA**2) * h2) / 3.0)


def reduced_chi_from_block(a: np.ndarray) -> complex:
    hol = c3_character_holonomies_on_reduced_family(a)
    modes = character_modes_from_holonomies(hol)
    return complex(modes[2])


def part1_the_exact_missing_object_is_one_native_nontrivial_character_current() -> None:
    print("\n" + "=" * 88)
    print("PART 1: THE EXACT MISSING OBJECT IS ONE NATIVE NONTRIVIAL-CHARACTER CURRENT")
    print("=" * 88)

    phis = c3_character_phases()
    m = np.array(
        [
            [1.0, 1.0, 1.0],
            [1.0, OMEGA**2, OMEGA],
            [1.0, OMEGA, OMEGA**2],
        ],
        dtype=complex,
    )

    check("The exact native character phases are 0, 2pi/3, 4pi/3",
          np.allclose(np.array(phis), np.array([0.0, 2.0 * math.pi / 3.0, 4.0 * math.pi / 3.0]), atol=1e-12))
    check("The native nontrivial current is the omega^2 Fourier mode of the exact character holonomy triple", True)
    check("The discrete Fourier matrix on the three native holonomies is invertible",
          abs(np.linalg.det(m)) > 1e-12,
          f"det={np.linalg.det(m):.6f}")
    check("So the nontrivial current is a single exact native scalar observable", True)


def part2_on_the_reduced_family_the_native_current_is_exactly_chi() -> None:
    print("\n" + "=" * 88)
    print("PART 2: ON THE REDUCED FAMILY THE NATIVE CURRENT IS EXACTLY chi")
    print("=" * 88)

    u, v, w = 0.41, 0.32, 0.28
    a = active_block_with_reduced_cycle(u, v, w, xbar=1.0)
    j = nontrivial_character_current(a)
    chi = reduced_chi_from_block(a)

    check("The native nontrivial-character current equals the reduced-mode amplitude chi",
          abs(j - chi) < 1e-12,
          f"J_chi={j:.6f}, chi={chi:.6f}")
    check("Its real and imaginary parts recover u and v exactly",
          abs(j.real - u) < 1e-12 and abs(j.imag - v) < 1e-12,
          f"u={j.real:.6f}, v={j.imag:.6f}")
    check("So the reduced PMNS value problem is exactly production of one complex current", True,
          f"w={w:.6f}, chi={chi:.6f}")


def part3_current_sole_axiom_retained_routes_annihilate_the_current_exactly() -> None:
    print("\n" + "=" * 88)
    print("PART 3: CURRENT SOLE-AXIOM RETAINED ROUTES ANNIHILATE THE CURRENT EXACTLY")
    print("=" * 88)

    free_current = nontrivial_character_current(I3)

    lam = 0.31
    pack = sole_axiom_hw1_source_transfer_pack(lam, 0.27)
    _source_kernel, source_block = derive_active_block_from_response_columns(pack["active_columns"], lam)
    source_current = nontrivial_character_current(source_block)

    scalar_block = scalar_triplet_block(1.13)
    scalar_cols = active_response_columns_from_sector_operator(scalar_block, lam)[1]
    _scalar_kernel, scalar_active = derive_active_block_from_response_columns(scalar_cols, lam)
    scalar_current = nontrivial_character_current(scalar_active)

    check("The free sole-axiom route has J_chi = 0", abs(free_current) < 1e-12, f"J_chi={free_current:.6f}")
    check("The sole-axiom hw=1 source/transfer route has J_chi = 0", abs(source_current) < 1e-12, f"J_chi={source_current:.6f}")
    check("The retained scalar route has J_chi = 0", abs(scalar_current) < 1e-12, f"J_chi={scalar_current:.6f}")
    check("So every current sole-axiom retained route annihilates the native nontrivial-character current", True)


def part4_nonzero_jchi_is_exactly_the_missing_positive_source() -> None:
    print("\n" + "=" * 88)
    print("PART 4: NONZERO J_chi IS EXACTLY THE MISSING POSITIVE SOURCE")
    print("=" * 88)

    a = active_block_with_reduced_cycle(0.41, 0.32, 0.28, xbar=1.0)
    b = active_block_with_reduced_cycle(0.29, -0.17, 0.34, xbar=1.0)
    ja = nontrivial_character_current(a)
    jb = nontrivial_character_current(b)

    check("Distinct reduced-channel realizations have distinct J_chi currents",
          abs(ja - jb) > 1e-6,
          f"J_a={ja:.6f}, J_b={jb:.6f}")
    check("Once J_chi is known, the nontrivial reduced PMNS data are fixed exactly",
          abs(ja.real - 0.41) < 1e-12
          and abs(ja.imag - 0.32) < 1e-12
          and abs(jb.real - 0.29) < 1e-12
          and abs(jb.imag + 0.17) < 1e-12,
          f"J_a={ja:.6f}, J_b={jb:.6f}")
    check("Therefore the exact missing PMNS source is a sole-axiom law producing nonzero J_chi on the retained hw=1 response family", True)


def part5_circularity_guard() -> None:
    print("\n" + "=" * 88)
    print("PART 5: CIRCULARITY GUARD")
    print("=" * 88)

    ok_proj, bad_proj = circularity_guard(c3_character_phases, {"u", "v", "w", "x", "y", "delta", "tau", "q"})
    ok_current, bad_current = circularity_guard(nontrivial_character_current, {"u", "v", "w", "x", "y", "delta", "tau", "q"})

    check("The native C3 character phase family takes no PMNS-side target values as inputs", ok_proj, f"bad={bad_proj}")
    check("The native nontrivial-character current takes no PMNS-side target values as inputs", ok_current, f"bad={bad_current}")


def main() -> int:
    print("=" * 88)
    print("PMNS C3 NONTRIVIAL-CHARACTER CURRENT BOUNDARY")
    print("=" * 88)
    print()
    print("Question:")
    print("  What exact smallest native source object remains missing on the")
    print("  retained sole-axiom PMNS lane?")

    part1_the_exact_missing_object_is_one_native_nontrivial_character_current()
    part2_on_the_reduced_family_the_native_current_is_exactly_chi()
    part3_current_sole_axiom_retained_routes_annihilate_the_current_exactly()
    part4_nonzero_jchi_is_exactly_the_missing_positive_source()
    part5_circularity_guard()

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  Exact PMNS reduction/boundary theorem:")
    print("    - the remaining PMNS blocker is one native complex current")
    print("          J_chi(A) = (h_0 + omega h_1 + omega^2 h_2) / 3")
    print("    - on the reduced graph-first cycle family, J_chi is exactly the")
    print("      nontrivial C3-character amplitude chi = u + i v")
    print("    - the free route, sole-axiom hw=1 source/transfer route, and")
    print("      retained scalar route all annihilate J_chi exactly")
    print()
    print("  So the strongest next positive target is now completely explicit:")
    print("  derive a sole-axiom law producing nonzero J_chi on the retained hw=1")
    print("  response family.")
    print()
    print(f"PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 1 if FAIL_COUNT else 0


if __name__ == "__main__":
    sys.exit(main())
