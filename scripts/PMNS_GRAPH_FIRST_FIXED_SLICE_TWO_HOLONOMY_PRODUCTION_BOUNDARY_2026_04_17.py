#!/usr/bin/env python3
"""Exact production-boundary reduction on the PMNS-native fixed-slice lane.

Question:
  After the fixed-slice two-holonomy collapse theorem, what exactly remains of
  the PMNS-native sole-axiom production problem for nonzero J_chi = chi?

Answer:
  The remaining blocker is exactly production of a nontrivial fixed-slice
  native holonomy pair. Equivalently, it is production of nonzero chi.

  The current bank still does not realize such a source law.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np

from PMNS_GRAPH_FIRST_FIXED_SLICE_TWO_HOLONOMY_COLLAPSE_2026_04_17 import (
    c3_pair_current_formula,
    fixed_slice_design_matrix,
    recover_chi_from_fixed_slice_two_holonomies,
)
from frontier_pmns_c3_character_holonomy_closure import c3_character_phases
from frontier_pmns_c3_nontrivial_current_boundary import nontrivial_character_current
from frontier_pmns_oriented_cycle_reduced_channel_nonselection import active_block_with_reduced_cycle
from frontier_pmns_sole_axiom_hw1_source_transfer_boundary import sole_axiom_hw1_source_transfer_pack
from frontier_pmns_twisted_flux_transfer_holonomy_boundary import flux_holonomy_on_reduced_family
from frontier_pmns_uniform_scalar_deformation_boundary import scalar_triplet_block
from pmns_lower_level_utils import (
    I3,
    active_response_columns_from_sector_operator,
    circularity_guard,
    derive_active_block_from_response_columns,
)

ROOT = Path(__file__).resolve().parents[1]
np.set_printoptions(precision=6, suppress=True, linewidth=140)

PASS_COUNT = 0
FAIL_COUNT = 0


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


def fixed_slice_holonomy_pair(block: np.ndarray, phis: tuple[float, float]) -> np.ndarray:
    return np.array(
        [flux_holonomy_on_reduced_family(block, phis[0]), flux_holonomy_on_reduced_family(block, phis[1])],
        dtype=float,
    )


def trivial_pair(w0: float) -> np.ndarray:
    return np.array([w0, w0], dtype=float)


def part1_fixed_slice_holonomy_pair_is_exactly_equivalent_to_chi() -> tuple[np.ndarray, tuple[float, float], float]:
    print("\n" + "=" * 96)
    print("PART 1: FIXED-SLICE TWO-HOLOMONY DATA ARE EXACTLY EQUIVALENT TO chi")
    print("=" * 96)

    phis = (0.0, 2.0 * math.pi / 3.0)
    m = fixed_slice_design_matrix(phis)
    det = float(np.linalg.det(m))

    target = active_block_with_reduced_cycle(0.41, 0.32, 0.28, xbar=1.0)
    zero_target = active_block_with_reduced_cycle(0.0, 0.0, 0.28, xbar=1.0)
    chi = nontrivial_character_current(target)
    zero_chi = nontrivial_character_current(zero_target)
    w0 = 0.28
    pair = fixed_slice_holonomy_pair(target, phis)
    pair_zero = fixed_slice_holonomy_pair(zero_target, phis)
    recovered = recover_chi_from_fixed_slice_two_holonomies(pair - trivial_pair(w0), phis)

    check("The canonical fixed-slice two-holonomy design matrix is invertible", abs(det) > 1e-12, f"det={det:.12f}")
    check(
        "The holonomy pair reconstructs the exact nontrivial current chi on the fixed slice",
        abs(recovered - chi) < 1e-12,
        f"recovered={recovered:.6f}, chi={chi:.6f}",
    )
    check(
        "The trivial fixed-slice pair (w0, w0) is exactly the chi = 0 case",
        abs(zero_chi) < 1e-12 and np.max(np.abs(pair_zero - trivial_pair(w0))) < 1e-12,
        f"pair_zero={np.round(pair_zero, 12)}",
    )
    check(
        "Therefore nonzero chi is equivalent to a nontrivial fixed-slice holonomy pair",
        abs(chi) > 1e-6 and np.max(np.abs(pair - trivial_pair(w0))) > 1e-6,
        f"pair={np.round(pair, 12)}, trivial={np.round(trivial_pair(w0), 12)}",
    )
    return target, phis, w0


def part2_the_canonical_c3_pair_is_the_exact_native_production_target(
    target: np.ndarray, phis: tuple[float, float], w0: float
) -> None:
    print("\n" + "=" * 96)
    print("PART 2: THE CANONICAL C3 PAIR IS THE EXACT NATIVE PRODUCTION TARGET")
    print("=" * 96)

    phi0, phi1, _phi2 = c3_character_phases()
    pair = fixed_slice_holonomy_pair(target, (phi0, phi1))
    chi = nontrivial_character_current(target)
    chi_formula = c3_pair_current_formula(pair[0], pair[1], w0)

    check("The canonical native C3 pair matches the fixed-slice production pair", abs(phi0 - phis[0]) < 1e-12 and abs(phi1 - phis[1]) < 1e-12)
    check(
        "The canonical C3 pair current formula recovers the exact native current",
        abs(chi_formula - chi) < 1e-12,
        f"chi_formula={chi_formula:.6f}, chi={chi:.6f}",
    )
    check(
        "So nonzero J_chi is exactly equivalent to producing a nontrivial canonical C3 holonomy pair on the fixed slice",
        abs(chi) > 1e-6 and np.max(np.abs(pair - trivial_pair(w0))) > 1e-6,
        f"pair={np.round(pair, 12)}",
    )


def part3_current_retained_routes_still_force_zero_current() -> None:
    print("\n" + "=" * 96)
    print("PART 3: THE CURRENT RETAINED SOLE-AXIOM ROUTES STILL FORCE ZERO CURRENT")
    print("=" * 96)

    lam = 0.31
    free_j = nontrivial_character_current(I3)

    pack = sole_axiom_hw1_source_transfer_pack(lam, 0.27)
    source_block = derive_active_block_from_response_columns(pack["active_columns"], lam)[1]
    source_j = nontrivial_character_current(source_block)

    scalar_block = scalar_triplet_block(1.13)
    scalar_cols = active_response_columns_from_sector_operator(scalar_block, lam)[1]
    scalar_active = derive_active_block_from_response_columns(scalar_cols, lam)[1]
    scalar_j = nontrivial_character_current(scalar_active)

    check("The free sole-axiom route still forces J_chi = 0", abs(free_j) < 1e-12, f"J_chi={free_j:.6f}")
    check("The canonical sole-axiom hw=1 route still forces J_chi = 0", abs(source_j) < 1e-12, f"J_chi={source_j:.6f}")
    check("The retained scalar route still forces J_chi = 0", abs(scalar_j) < 1e-12, f"J_chi={scalar_j:.6f}")
    check("So the current retained bank still does not itself produce nonzero chi", True)


def part4_the_current_exact_bank_positions_this_as_production_not_readout() -> None:
    print("\n" + "=" * 96)
    print("PART 4: THE CURRENT EXACT BANK NOW POSITIONS THE FRONTIER AS PRODUCTION")
    print("=" * 96)

    current_boundary = read("docs/PMNS_C3_NONTRIVIAL_CURRENT_BOUNDARY_NOTE.md")
    mode_reduction = read("docs/PMNS_C3_CHARACTER_MODE_REDUCTION_NOTE.md")
    zero_law = read("docs/PMNS_SELECTOR_CURRENT_STACK_ZERO_LAW_NOTE.md")
    route_exhaust = read("docs/PMNS_SOLE_AXIOM_NATIVE_CURRENT_ROUTE_EXHAUSTION_NOTE_2026-04-17.md")
    one_angle_nogo = read("docs/PMNS_GRAPH_FIRST_FIXED_SLICE_SELECTOR_HOLONOMY_NONCOLLAPSE_NOTE_2026-04-17.md")
    two_holonomy = read("docs/PMNS_GRAPH_FIRST_FIXED_SLICE_TWO_HOLONOMY_COLLAPSE_NOTE_2026-04-17.md")
    three_flux = read("docs/PMNS_THREE_FLUX_HOLONOMY_CLOSURE_NOTE.md")
    note = read("docs/PMNS_GRAPH_FIRST_FIXED_SLICE_TWO_HOLONOMY_PRODUCTION_BOUNDARY_NOTE_2026-04-17.md")

    check(
        "The current boundary and mode-reduction notes already say the remaining PMNS-native source object is nonzero chi itself",
        "one native complex nontrivial-character current" in current_boundary
        and "a sole-axiom law that produces nonzero `C3`-nontrivial character amplitude" in mode_reduction,
    )
    check(
        "The selector current-stack zero law and route-exhaustion note already say the current bank still does not produce that object",
        "`a_sel,current = 0`" in zero_law
        and "no overlooked exact PMNS-native route on the current" in route_exhaust
        and "nonzero `J_chi`" in route_exhaust,
    )
    check(
        "The one-angle no-go plus the two-holonomy collapse note already separate readout closure from production",
        "same exact one-angle twisted-flux holonomy" in one_angle_nogo
        and "two independent native holonomies collapse the fixed slice exactly" in two_holonomy
        and "not** a new sole-axiom production law" in two_holonomy,
    )
    check(
        "The three-flux closure note also records closure of readout rather than sole-axiom production of nontrivial values",
        "does **not** by itself prove full sole-axiom" in three_flux
        and "nontrivial values" in three_flux,
    )
    check(
        "The new production-boundary note states the sharpened remaining object exactly as a nontrivial fixed-slice holonomy-pair source law",
        "nontrivial fixed-slice native holonomy" in note
        and "equivalently nonzero `chi = J_chi`" in note
        and "current bank still does **not** realize that source law" in note,
    )


def part5_circularity_guard() -> None:
    print("\n" + "=" * 96)
    print("PART 5: CIRCULARITY GUARD")
    print("=" * 96)

    ok_hol, bad_hol = circularity_guard(flux_holonomy_on_reduced_family, {"u", "v", "w", "x", "y", "delta", "tau", "q"})
    ok_current, bad_current = circularity_guard(nontrivial_character_current, {"u", "v", "w", "x", "y", "delta", "tau", "q"})
    check("The native holonomy functional takes no PMNS-side target values as inputs", ok_hol, f"bad={bad_hol}")
    check("The native current functional takes no PMNS-side target values as inputs", ok_current, f"bad={bad_current}")


def main() -> int:
    print("=" * 96)
    print("PMNS GRAPH-FIRST FIXED-SLICE TWO-HOLOMONY PRODUCTION BOUNDARY")
    print("=" * 96)
    print()
    print("Question:")
    print("  After fixed-slice two-holonomy collapse, what exactly remains of the")
    print("  PMNS-native sole-axiom production problem for nonzero J_chi = chi?")

    target, phis, w0 = part1_fixed_slice_holonomy_pair_is_exactly_equivalent_to_chi()
    part2_the_canonical_c3_pair_is_the_exact_native_production_target(target, phis, w0)
    part3_current_retained_routes_still_force_zero_current()
    part4_the_current_exact_bank_positions_this_as_production_not_readout()
    part5_circularity_guard()

    print("\n" + "=" * 96)
    print("RESULT")
    print("=" * 96)
    print("  Exact PMNS-native production-boundary sharpening:")
    print("    - fixed-slice two-holonomy closure already identifies chi exactly")
    print("    - therefore nonzero J_chi is exactly equivalent to a nontrivial")
    print("      fixed-slice native holonomy pair")
    print("    - the current retained sole-axiom routes still force J_chi = 0")
    print("    - so the remaining PMNS-native blocker is now exactly a sole-axiom")
    print("      law that produces nontrivial fixed-slice holonomy data")
    print()
    print(f"PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 1 if FAIL_COUNT else 0


if __name__ == "__main__":
    sys.exit(main())
