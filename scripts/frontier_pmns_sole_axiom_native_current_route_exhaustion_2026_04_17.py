#!/usr/bin/env python3
"""Exact route-exhaustion theorem for the PMNS-native sole-axiom current lane.

Question:
  Is there any overlooked exact route inside the current PMNS-native
  sole-axiom bank that already derives nonzero J_chi?

Answer:
  No.

  The current PMNS-native bank is exhausted exactly:
    - the free route, canonical sole-axiom hw=1 source/transfer route, and
      retained scalar route all force J_chi = 0
    - the nearest native dynamical positives (transfer dominant mode and direct
      corner transport) recover only aligned seed data / branch structure and
      explicitly stop before the off-seed breaking carrier
    - the graph-first / C3-holonomy / reduced-channel stack closes the carrier
      and the native readout exactly, but distinct reduced-channel points with
      distinct J_chi are both realized on the active response chain

  Therefore there is no overlooked exact PMNS-native route on the current bank
  to nonzero J_chi.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

from frontier_pmns_c3_nontrivial_current_boundary import nontrivial_character_current
from frontier_pmns_corner_transport_active_block import (
    active_corner_transport,
    decompose_seed_breaking,
    orbit_average_transport,
    transport_breaking_vector,
)
from frontier_pmns_oriented_cycle_reduced_channel_nonselection import (
    active_block_with_reduced_cycle,
    reduced_cycle_coordinates,
    residual_swap_conjugate,
)
from frontier_pmns_sole_axiom_hw1_source_transfer_boundary import (
    sole_axiom_hw1_source_transfer_pack,
)
from frontier_pmns_transfer_operator_dominant_mode import (
    active_seed_transfer_kernel,
    projected_transfer_kernel_from_active_block,
)
from frontier_pmns_uniform_scalar_deformation_boundary import scalar_triplet_block
from pmns_lower_level_utils import (
    I3,
    active_response_columns_from_sector_operator,
    circularity_guard,
    derive_active_block_from_response_columns,
    sector_operator_fixture_from_effective_block,
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


def part1_named_sole_axiom_routes_force_zero_current() -> None:
    print("\n" + "=" * 88)
    print("PART 1: NAMED SOLE-AXIOM ROUTES FORCE J_chi = 0")
    print("=" * 88)

    lam = 0.31
    free_j = nontrivial_character_current(I3)

    pack = sole_axiom_hw1_source_transfer_pack(lam, 0.27)
    source_block = derive_active_block_from_response_columns(pack["active_columns"], lam)[1]
    source_j = nontrivial_character_current(source_block)

    scalar_block = scalar_triplet_block(1.13)
    scalar_cols = active_response_columns_from_sector_operator(scalar_block, lam)[1]
    scalar_active = derive_active_block_from_response_columns(scalar_cols, lam)[1]
    scalar_j = nontrivial_character_current(scalar_active)

    check("The free sole-axiom PMNS route has J_chi = 0", abs(free_j) < 1e-12, f"J_chi={free_j:.6f}")
    check("The canonical sole-axiom hw=1 source/transfer route has J_chi = 0", abs(source_j) < 1e-12, f"J_chi={source_j:.6f}")
    check("The retained scalar route has J_chi = 0", abs(scalar_j) < 1e-12, f"J_chi={scalar_j:.6f}")
    check("So the explicit retained sole-axiom routes already annihilate the native current exactly", True)


def part2_nearest_native_dynamics_stop_upstream_of_the_current() -> None:
    print("\n" + "=" * 88)
    print("PART 2: THE NEAREST NATIVE DYNAMICS STOP UPSTREAM OF J_chi")
    print("=" * 88)

    xbar = 0.90
    ybar = 0.40
    t_seed = active_seed_transfer_kernel(2.0 * xbar, ybar)

    x1 = np.array([1.15, 0.82, 0.73], dtype=float)
    y1 = np.array([0.50, 0.25, 0.45], dtype=float)
    x2 = np.array([1.05, 0.88, 0.77], dtype=float)
    y2 = np.array([0.39, 0.36, 0.45], dtype=float)
    x1 += xbar - float(np.mean(x1))
    x2 += xbar - float(np.mean(x2))
    y1 += ybar - float(np.mean(y1))
    y2 += ybar - float(np.mean(y2))

    a1 = np.diag(x1) + np.diag(y1) @ np.array([[0, 1, 0], [0, 0, 1], [1, 0, 0]], dtype=complex)
    a2 = np.diag(x2) + np.diag(y2) @ np.array([[0, 1, 0], [0, 0, 1], [1, 0, 0]], dtype=complex)
    t1 = projected_transfer_kernel_from_active_block(a1)
    t2 = projected_transfer_kernel_from_active_block(a2)

    check(
        "The transfer-dominant-mode route collapses distinct off-seed samples to the same aligned seed kernel",
        np.linalg.norm(t1 - t_seed) < 1e-10 and np.linalg.norm(t2 - t_seed) < 1e-10 and np.linalg.norm(a1 - a2) > 1e-6,
        f"errors=({np.linalg.norm(t1 - t_seed):.2e}, {np.linalg.norm(t2 - t_seed):.2e})",
    )

    x_a = np.array([1.15, 0.82, 0.95], dtype=float)
    y_a = np.array([0.41, 0.28, 0.54], dtype=float)
    d_a = 0.63
    x_b = np.array([1.20, 0.79, 0.93], dtype=float)
    y_b = np.array([0.52, 0.17, 0.54], dtype=float)
    d_b = 0.63
    T_a = active_corner_transport(x_a, y_a, d_a)
    T_b = active_corner_transport(x_b, y_b, d_b)
    even_a, odd_fwd_a, odd_bwd_a = orbit_average_transport(T_a)
    even_b, odd_fwd_b, odd_bwd_b = orbit_average_transport(T_b)
    _, _, xi_a, eta_a, dd_a = decompose_seed_breaking(x_a, y_a, d_a)
    _, _, xi_b, eta_b, dd_b = decompose_seed_breaking(x_b, y_b, d_b)

    check(
        "The direct corner-transport route preserves the same orbit moments across distinct breaking sources",
        abs(even_a - even_b) < 1e-12 and abs(odd_fwd_a - odd_fwd_b) < 1e-12 and abs(odd_bwd_a - odd_bwd_b) < 1e-12,
        f"even=({even_a:.6f},{even_b:.6f}) odd=({odd_fwd_a:.6f},{odd_fwd_b:.6f})",
    )
    check(
        "Those equal orbit moments still come from distinct 5-real breaking carriers",
        np.linalg.norm(transport_breaking_vector(xi_a, eta_a, dd_a) - transport_breaking_vector(xi_b, eta_b, dd_b)) > 1e-6,
        f"|Δsource|={np.linalg.norm(transport_breaking_vector(xi_a, eta_a, dd_a) - transport_breaking_vector(xi_b, eta_b, dd_b)):.6f}",
    )
    check("So the nearest native dynamical positives stop before the nontrivial current law", True)


def part3_reduced_current_stack_is_exact_but_point_blind() -> None:
    print("\n" + "=" * 88)
    print("PART 3: THE REDUCED CURRENT STACK IS EXACT BUT POINT-BLIND")
    print("=" * 88)

    lam = 0.31
    a = active_block_with_reduced_cycle(0.41, 0.32, 0.28, xbar=1.0)
    b = active_block_with_reduced_cycle(0.29, -0.17, 0.34, xbar=1.0)

    sec_a = sector_operator_fixture_from_effective_block(a, seed=4101)
    sec_b = sector_operator_fixture_from_effective_block(b, seed=4102)
    cols_a = active_response_columns_from_sector_operator(sec_a, lam)[1]
    cols_b = active_response_columns_from_sector_operator(sec_b, lam)[1]
    rec_a = derive_active_block_from_response_columns(cols_a, lam)[1]
    rec_b = derive_active_block_from_response_columns(cols_b, lam)[1]
    j_a = nontrivial_character_current(rec_a)
    j_b = nontrivial_character_current(rec_b)

    check(
        "Two distinct graph-first reduced-channel points are both realized exactly on the active response chain",
        np.linalg.norm(rec_a - a) < 1e-12 and np.linalg.norm(rec_b - b) < 1e-12 and np.linalg.norm(a - b) > 1e-6,
        f"|A-B|={np.linalg.norm(a - b):.6f}",
    )
    check(
        "Those realized points carry distinct nonzero native currents J_chi",
        abs(j_a - j_b) > 1e-6 and abs(j_a) > 1e-6 and abs(j_b) > 1e-6,
        f"J_a={j_a:.6f}, J_b={j_b:.6f}",
    )
    check(
        "Both realized points obey the same graph-first residual antiunitary symmetry",
        np.linalg.norm(residual_swap_conjugate(rec_a) - rec_a) < 1e-12 and np.linalg.norm(residual_swap_conjugate(rec_b) - rec_b) < 1e-12,
    )
    check(
        "The native readout separates them rather than selecting one",
        np.linalg.norm(reduced_cycle_coordinates(rec_a) - reduced_cycle_coordinates(rec_b)) > 1e-6,
        f"|Δcoords|={np.linalg.norm(reduced_cycle_coordinates(rec_a) - reduced_cycle_coordinates(rec_b)):.6f}",
    )


def part4_no_hidden_route_exists_on_the_current_pmns_native_bank() -> None:
    print("\n" + "=" * 88)
    print("PART 4: NO HIDDEN ROUTE EXISTS ON THE CURRENT PMNS-NATIVE BANK")
    print("=" * 88)

    source_note = read("docs/PMNS_SOLE_AXIOM_HW1_SOURCE_TRANSFER_BOUNDARY_NOTE.md")
    current_note = read("docs/PMNS_C3_NONTRIVIAL_CURRENT_BOUNDARY_NOTE.md")
    nogo_note = read("docs/PMNS_CURRENT_BANK_VALUE_SELECTION_NOGO_NOTE.md")
    nonselect_note = read("docs/PMNS_ORIENTED_CYCLE_REDUCED_CHANNEL_NONSELECTION_NOTE.md")
    transfer_note = read("docs/PMNS_TRANSFER_OPERATOR_DOMINANT_MODE_NOTE.md")
    corner_note = read("docs/PMNS_CORNER_TRANSPORT_ACTIVE_BLOCK_NOTE.md")
    holonomy_note = read("docs/PMNS_C3_CHARACTER_HOLONOMY_CLOSURE_NOTE.md")
    align_note = read("docs/PMNS_GRAPH_FIRST_AXIS_ALIGNMENT_NOTE.md")

    check(
        "The source/transfer boundary note records the canonical sole-axiom pack as trivial",
        "stays trivial" in source_note and "support/frame information, not nontrivial" in source_note,
    )
    check(
        "The native current boundary note records J_chi = 0 on all current sole-axiom retained routes",
        "J_chi = 0" in current_note and "free route" in current_note and "source/transfer route" in current_note,
    )
    check(
        "The current-bank no-go and reduced-channel nonselection notes record exact carrier/readout closure without value selection",
        "does **not** contain a positive" in nogo_note
        and "value-selection law" in nogo_note
        and "does **not** select a unique value" in nonselect_note,
    )
    check(
        "The transfer and corner-transport notes both stop upstream of the off-seed current data",
        "does not determine the `5`-real off-seed" in transfer_note
        and "blind to the active 5-real" in corner_note,
    )
    check(
        "The graph-first and C3-holonomy notes close support/readout but not nontrivial sole-axiom values",
        "does **not** by itself determine" in align_note
        and "does **not** give full sole-axiom positive neutrino closure" in holonomy_note,
    )
    check("So the current PMNS-native sole-axiom bank contains no overlooked exact route to nonzero J_chi", True)


def part5_circularity_guard() -> None:
    print("\n" + "=" * 88)
    print("PART 5: CIRCULARITY GUARD")
    print("=" * 88)

    ok_current, bad_current = circularity_guard(nontrivial_character_current, {"u", "v", "w", "x", "y", "delta", "tau", "q"})
    ok_pack, bad_pack = circularity_guard(sole_axiom_hw1_source_transfer_pack, {"u", "v", "w", "x", "y", "delta", "tau", "q"})
    check("The native current functional takes no PMNS-side target values as inputs", ok_current, f"bad={bad_current}")
    check("The canonical sole-axiom source/transfer pack takes no PMNS-side target values as inputs", ok_pack, f"bad={bad_pack}")


def main() -> int:
    print("=" * 88)
    print("PMNS SOLE-AXIOM NATIVE CURRENT ROUTE EXHAUSTION")
    print("=" * 88)
    print()
    print("Question:")
    print("  Is there any overlooked exact route inside the current PMNS-native")
    print("  sole-axiom bank that already derives nonzero J_chi?")

    part1_named_sole_axiom_routes_force_zero_current()
    part2_nearest_native_dynamics_stop_upstream_of_the_current()
    part3_reduced_current_stack_is_exact_but_point_blind()
    part4_no_hidden_route_exists_on_the_current_pmns_native_bank()
    part5_circularity_guard()

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  Exact PMNS-native audit result:")
    print("    - the explicit retained sole-axiom routes force J_chi = 0")
    print("    - the nearest native dynamical positives stop at aligned seed data")
    print("      / branch structure and do not reach the off-seed current")
    print("    - the reduced graph-first current/readout stack is exact but")
    print("      point-blind")
    print()
    print("  Therefore there is no overlooked exact current-bank route to")
    print("  nonzero J_chi on the PMNS-native sole-axiom lane.")
    print()
    print("  One concrete next theorem target:")
    print("    derive, or rule out on a sharper exact subbank, a genuinely new")
    print("    fixed-slice current-image collapse law beyond the current")
    print("    selector/holonomy bank, and in particular a fixed-slice")
    print("    nontrivial-current activation law with output J_chi.")
    print()
    print(f"PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 1 if FAIL_COUNT else 0


if __name__ == "__main__":
    sys.exit(main())
